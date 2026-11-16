---
tag: R2NX8P
kind: problem
slug: stewart-gough-forward-kinematics
name: Forward kinematics of the Stewart-Gough platform
aliases:
- direct kinematics of the hexapod
area: robotics/robot-kinematics
level: advanced
summary: Given the six leg lengths of a Stewart-Gough platform, find the poses of the moving plate. The general case has at most 40 complex solutions, and all 40 can be real.
prereqs: [parallel-manipulator, forward-kinematics]
see_also: [homotopy-continuation, resultant, parallel-manipulator, polynomial-system-solving, groebner-basis, inverse-kinematics, kinematic-singularity, forward-kinematics]
sources:
  - paper: doi:10.1016/0094-114X(95)00091-C
    title: M. L. Husty, An algorithm for solving the direct kinematics of general Stewart-Gough platforms, Mechanism and Machine Theory 31(4), 1996
    locator: pages 365 to 379, elimination in Study's kinematic image space down to one univariate polynomial of degree 40
  - paper: doi:10.1115/1.2919188
    title: M. Raghavan, The Stewart platform of general geometry has 40 configurations, Journal of Mechanical Design 115(2), 1993
    locator: pages 277 to 282, 40 solutions found by polynomial continuation for a platform of general geometry
  - book: "F. Ronga and T. Vust, Stewart platforms without computer?, in Real Analytic and Algebraic Geometry (Trento, 1992), de Gruyter, Berlin, 1995"
    locator: pages 197 to 212, a proof that the general platform has 40 complex solutions
  - paper: doi:10.1007/978-94-015-9064-8_1
    title: P. Dietmaier, The Stewart-Gough platform of general geometry can have 40 real postures, in J. Lenarčič and M. L. Husty (editors), Advances in Robot Kinematics, Analysis and Control, Kluwer, 1998
    locator: the numerical search that found a platform and leg lengths with 40 real solutions (general locator)
  - book: isbn:9781402041327
    title: J.-P. Merlet, Parallel Robots, 2nd edition, Springer, 2006
    locator: the chapter on direct kinematics (elimination, continuation, iterative and interval methods, and extra sensors) (general locator)
  - paper: doi:10.1243/PIME_PROC_1965_180_029_02
    title: D. Stewart, A platform with six degrees of freedom, Proceedings of the Institution of Mechanical Engineers 180(1), 1965
    locator: pages 371 to 386, the platform, with Gough's tyre testing machine in the discussion
---

The Stewart-Gough platform is a [parallel manipulator](/parallel-manipulator/) in which a moving plate is held above a base by six legs of variable length. Its forward kinematics asks: given the six leg lengths, where is the plate? For a serial arm this question has one answer by a product of matrices. Here it means solving six polynomial equations in the six unknowns of the plate pose. A platform of general shape has at most 40 solutions over the complex numbers, and Dietmaier (1998) built one where all 40 are real. The reverse question, from the pose to the leg lengths, is six distance computations. [Homotopy continuation](/homotopy-continuation/) and the [resultant](/resultant/) are general tools for polynomial systems; this page is the particular system on which both were tested, and the bound 40 is specific to it.

## In plain words

A flight simulator cabin sits on six telescopic legs. Each leg can tell how long it is. From these six numbers, can you tell where the cabin is and how it is tilted?

Going the other way is easy. If you know where the cabin is, each leg length is just the distance between its two ends.

But from the lengths alone, the cabin can usually sit in more than one way. Think of a tent held by six poles of fixed length: there can be several shapes that fit. For a platform of a general shape, there are at most forty ways, and some platforms really have forty. In practice, a controller knows roughly where the cabin was a moment ago and searches near that place.

## Definition

**Input.** Six base points $a_1, \dots, a_6 \in \mathbb{R}^3$ in the fixed frame $\{s\}$; six platform points $b_1, \dots, b_6 \in \mathbb{R}^3$ in the platform frame $\{b\}$; and six leg lengths $\ell_1, \dots, \ell_6 > 0$.

**Unknown.** The pose $T_{sb} = (R, p) \in SE(3)$ of the platform.

**Equations.** For $i = 1, \dots, 6$,

$$|p + R\, b_i - a_i|^2 = \ell_i^2 .$$

**Output.** All poses that satisfy the six equations, or the real ones, or the one closest to a given guess.

With $R$ written by a unit quaternion or by Study's parameters, each equation is a polynomial. Six equations in six unknowns give, for a general platform, a finite set of solutions.

**Inverse kinematics.** Given $(R, p)$, the lengths are $\ell_i = |p + R b_i - a_i|$, six closed form computations. This is why the forward problem is the hard direction for parallel robots and the easy one for serial arms.

## Variants

| variant | solutions | status |
|---|---|---|
| general 6-6 platform (six distinct points on each body) | at most 40 complex; 40 real occur | Ronga and Vust 1995, Raghavan 1993, Husty 1996, Dietmaier 1998 |
| planar base and planar platform | real solutions come in mirror pairs (below) | elementary |
| designs with coincident joint centers, such as 3-3 and 6-3 | fewer solutions | special elimination |
| architecturally singular designs | singular in every pose | to be avoided in design |
| tracking: one solution near the previous pose | one | Newton's method, local |
| extra sensors on the passive joints | one | the system becomes overdetermined |

**Mirror pairs.** *If all base points lie in the plane $z = 0$ of $\{s\}$ and all platform points lie in the plane $z = 0$ of $\{b\}$, and $(R, p)$ is a solution, then so is $(SRS, Sp)$ with $S = \mathrm{diag}(1, 1, -1)$.* Proof: $Sa_i = a_i$ and $Sb_i = b_i$, so $Sp + SRS\,b_i - a_i = S(p + Rb_i - a_i)$, which has the same length. And $\det(SRS) = \det R = 1$. $\blacksquare$ So the real solutions of such a platform come in pairs, one above the base and one below it.

## Examples

**A platform to check by hand.** Base points on a circle of radius 2 m at the angles $10°, 110°, 130°, 230°, 250°, 350°$. Platform points on a circle of radius 1 m at $50°, 70°, 170°, 190°, 290°, 310°$. Leg $i$ joins the $i$-th base point to the $i$-th platform point, so each leg spans an angle of $40°$ seen from above.

- *Inverse kinematics at the home pose* $R = I$, $p = (0, 0, 1.5)$ m. For every leg, by the law of cosines, $\ell^2 = 2^2 + 1^2 - 2 \cdot 2 \cdot 1 \cdot \cos 40° + 1.5^2 = 5 - 3.0642 + 2.25 = 4.1858$, so $\ell = 2.0459$ m.
- *The Jacobian there* (the $6 \times 6$ matrix of leg length rates by pose rates) has determinant $5.28$, so the home pose is not singular.
- *Forward kinematics.* Take the pose $p = (0.1, -0.2, 1.4)$ m with rotation vector $(0.05, -0.08, 0.12)$ rad. Its leg lengths are $2.0139$, $2.0990$, $2.1724$, $1.7306$, $2.0177$ and $1.8977$ m. Newton's method started at the home pose returns the true pose to machine precision.
- *Other solutions (a measurement).* Newton's method from 400 random starting poses (seed 7) found 8 distinct real solutions for these lengths. They form 4 mirror pairs with heights $\pm 1.4$, $\pm 0.80435$, $\pm 0.84894$ and $\pm 0.88325$ m, as the mirror rule predicts. A random search can miss solutions, so this shows only that there are at least 8 real ones. The number of real solutions is even, because the non-real ones come in conjugate pairs and 40 is even, and it is at most 40.

## Known algorithms

The problem has a fixed size, so the costs below are not functions of an input size. In the [real RAM](/real-ram/) model, the elimination is a fixed number of operations, followed by the numerical roots of one polynomial.

| method | finds | notes |
|---|---|---|
| elimination in Study's kinematic image space (Husty 1996) | all 40 complex solutions | one univariate polynomial of degree 40; back substitution gives each pose |
| [homotopy continuation](/homotopy-continuation/) (Raghavan 1993) | all isolated solutions, with probability one for a random start system | tracks one path per start solution; general but slower |
| [Gröbner bases](/groebner-basis/) | all solutions, exactly for rational data | Lazard studied the problem with Gröbner bases in the early 1990s |
| [resultants](/resultant/) | all solutions | eliminate variables until one polynomial is left |
| Newton's method from the last pose | one solution, near the start | local quadratic convergence at a nonsingular solution; used in real-time control |
| interval analysis | all solutions in a box, certified | Merlet's method; gives guaranteed enclosures |

Newton tracking can jump to another solution branch if the start is far away or the path passes close to a singularity. That is a known risk in practice, not a theorem.

## Bounds

- **Upper bound.** A general platform has at most 40 solutions over $\mathbb{C}$. Ronga and Vust (1995) gave a proof by intersection theory. Husty (1996) reduced the problem to one polynomial of degree 40.
- **Tightness.** Raghavan (1993) found 40 complex solutions for a platform of general geometry by continuation, so 40 is reached over $\mathbb{C}$. Dietmaier (1998) found a platform and leg lengths with 40 real solutions, so 40 is also reached over $\mathbb{R}$.
- **Special designs.** Platforms with coincident joint centers or with special symmetry can have fewer solutions, or a continuum of them if the design is architecturally singular.

## Reductions

- **To a polynomial system.** Write $R$ by a unit quaternion and $p$ by three coordinates, or use Study's 8 parameters with the Study quadric. The six equations become polynomials, and [polynomial system solving](/polynomial-system-solving/) applies.
- **Removing the quadratic part.** Subtracting the first equation from the others removes the term $|p|^2$, which is common to all six, and leaves five equations that are linear in $p$ for a fixed $R$. Many eliminations start this way.
- **From inverse kinematics.** The inverse direction is closed form. A numerical solver for the forward direction calls it at each step, as Newton's method on $\ell(R, p) - \ell^\ast = 0$.

## Applications

Motion simulators, machine tools with hexapod structures, positioning stages for telescopes and surgery, and tyre testing machines all read leg lengths and need the platform pose. The controller computes it by Newton's method from the last pose. The full set of solutions is used offline to check that the platform cannot move into another assembly mode on the way, and to design platforms with a large region free of singularities.

## References
