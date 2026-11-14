---
tag: BY4XK2
kind: theorem
slug: nine-point-path-synthesis
name: Nine-point path synthesis of four-bars
aliases:
- Alt's problem
area: cad/mechanism-and-assembly-design
level: research
summary: Alt's problem of a four-bar whose coupler curve passes through nine points, solved by Wampler, Morgan and Sommese, who found 1442 solutions up to cognates.
prereqs: [path-generation, coupler-curve, homotopy-continuation]
see_also: [roberts-chebyshev-theorem, burmester-theory, optimization-based-linkage-synthesis, polynomial-system-solving, kinematic-synthesis, four-bar-linkage, interval-newton-method, transmission-angle]
sources:
  - paper: doi:10.1002/zamm.19230030103
    title: H. Alt, Über die Erzeugung gegebener ebener Kurven mit Hilfe des Gelenkvierecks, Zeitschrift für Angewandte Mathematik und Mechanik 3(1), 1923, 13 to 19
    locator: the problem of a four-bar coupler curve through nine given points
  - paper: "Charles W. Wampler, Alexander P. Morgan and Andrew J. Sommese, Complete solution of the nine-point path synthesis problem for four-bar linkages, ASME Journal of Mechanical Design 114(1), 1992, 153 to 159"
    locator: equations (1) to (16) (the isotropic formulation and its reduction), Table 1 and the count 286,720, equation (17) (Roberts cognates), the numerical reduction to 4326 solutions in 1442 cognate triples, Tables 2 and 3 (four examples with 21, 45, 64 and 120 real cognate triples)
  - paper: "Bernard Roth and Ferdinand Freudenstein, Synthesis of path-generating mechanisms by numerical methods, ASME Journal of Engineering for Industry 85(3), 1963, 298 to 306"
    locator: the bootstrap continuation method and the first nine-point solutions, found as a special case of geared five-bars
  - paper: "Alexander P. Morgan and Andrew J. Sommese, Coefficient-parameter polynomial continuation, Applied Mathematics and Computation 29, 1989, 123 to 160"
    locator: the generic number of nonsingular solutions of a family of polynomial systems and the parameter homotopy that reuses it
  - paper: arxiv:1011.1091
    title: Jonathan D. Hauenstein and Frank Sottile, Algorithm 921, alphaCertified, certifying solutions to polynomial systems, ACM Transactions on Mathematical Software 38(4), 2012
    locator: the four-bar example (certification of 8652 isolated solutions for one set of nine points and of the real ones among them)
  - paper: arxiv:1908.06020
    title: Jonathan D. Hauenstein and Martin Helmer, Probabilistic saturations and Alt's problem, Experimental Mathematics, 2020
    locator: abstract and introduction (no proof that all solutions were found; upper bounds by probabilistic saturation)
  - paper: arxiv:2609.22003
    title: Taylor Brysiewicz, Alt's problem, preprint, 2026
    locator: abstract (coupler curves as a Zariski open subset of Gr(3,6), mixed volume 5538, 4096 branches escaping the torus, upper bound 1442, certified lower bound 1442 on one instance)
---

Nine-point path synthesis asks for every [four-bar linkage](/four-bar-linkage/) whose [coupler curve](/coupler-curve/) passes through nine given points of the plane, with no condition on when each point is reached. Alt posed the problem in 1923. Nine is the largest number of points for which a solution can be expected, because a four-bar coupler curve has nine free parameters. For nine generic points the answer is 1442 coupler curves. Each curve is traced by three cognate four-bars, so there are 4326 linkages.

The number was found in 1992 by Wampler, Morgan and Sommese, who solved the polynomial system completely with [homotopy continuation](/homotopy-continuation/). Their computation was strong evidence, not a proof, because a numerical method cannot exclude a missed solution. Certified computations later confirmed the lower bound for one instance. A 2026 preprint by Brysiewicz gives a proof of the upper bound. The general problem, with any number of points and with or without timing, is on the [path generation](/path-generation/) page.

## Statement

A four-bar is given by its two fixed pivots $A$ and $B$, its two moving pivots $D$ and $C$, and a coupler point $P$ rigidly attached to the coupler $DC$. The bar $AD$ turns about $A$ and the bar $BC$ about $B$. The *coupler curve* is the set of positions of $P$. In complex numbers, with all vectors measured from the first given point $P_0$, write

$$x = D - P_0, \quad a = A - P_0, \quad y = C - P_0, \quad b = B - P_0$$

in the position where $P = P_0$. A four-bar is *nondegenerate* if its coupler moves and its curve is not a circle or a point; Wampler, Morgan and Sommese list the degenerate cases explicitly (for example $x = y$, $a = b$).

**Theorem.** Let $P_0, \dots, P_8$ be nine generic points in the plane, allowing complex coordinates.

1. *Count.* The coupler curves of four-bars form a family with 9 parameters, and each given point is one condition. So nine points are the most for which nondegenerate solutions exist in general, and for ten generic points there are none.
2. *Number of solutions.* The nondegenerate four-bars whose coupler curve passes through all nine points trace exactly 1442 distinct coupler curves. By the [Roberts-Chebyshev theorem](/roberts-chebyshev-theorem/) each curve is traced by three cognate four-bars, which gives 4326 four-bars. Each four-bar appears twice among the solutions of the polynomial system below, once for each labeling of its left and right sides, which gives 8652 solutions.
3. *Real points.* For real points, the number of real solutions depends on the points. In the four examples of Wampler, Morgan and Sommese it was 21, 45, 64 and 120 cognate triples.

Status of part 2: the value 1442 was found numerically in 1992 and has been reproduced many times. Lower bounds were certified for single instances, by Hauenstein and Sottile in floating-point arithmetic (what they call a soft certificate) and again by Brysiewicz. The matching upper bound is proved in the 2026 preprint of Brysiewicz, which, as far as I can tell, has not yet been refereed.

## In plain words

A four-bar is four rods hinged in a loop, with one rod bolted down. A point on the rod opposite the bolted one draws a closed curve as the loop moves. Nine numbers fix the shape and place of that curve, so if you mark nine dots on paper, only finitely many such curves pass through all of them.

How many? The equations behind the question are large, and a naive count allowed millions of answers. In 1992 three researchers followed every one of the possible answers numerically and found that only 1442 curves survive, each drawn by three different linkages. For dots on real paper, only some of those are real linkages, and fewer still move through the dots in the right order without jamming.

## Proof

The count of parameters and the formulation are proved below. The number 1442 is not proved on this page; the argument for it is sketched with its sources, and the formulation was checked numerically on a known linkage.

**Step 1, nine parameters.** A four-bar with a coupler point is fixed by the fixed pivots $A$ and $B$ (4 real numbers), the lengths $|AD|$ and $|BC|$ (2), and the triangle $DCP$ on the coupler, given by its three sides (3). That is 9. A generic coupler curve comes from only finitely many choices, the three Roberts cognates, so the coupler curves form a family of dimension 9. Requiring the curve to pass through a given point is one equation. So nine generic points leave finitely many curves.

For ten points, consider all pairs (curve, ten points on it). A curve has dimension 1, so this set has dimension $9 + 10 = 19$. The tuples of ten points in the plane have dimension 20, so the tuples that lie on some coupler curve form a set of lower dimension, and a generic tuple is not among them. $\blacksquare$

**Step 2, the loop equations.** Move the linkage so that $P$ goes to $P_j$, and let $\delta_j = P_j - P_0$. The coupler turns by $\theta_j$ and the bar $AD$ by $\lambda_j$. Going around the loop $A \to D \to P$ gives

$$(x - a) e^{i\lambda_j} = x e^{i\theta_j} + \delta_j - a,$$

and the same with $y, b, \mu_j$ for the right side. Multiply each equation by its complex conjugate, which removes $\lambda_j$ and $\mu_j$, and set $\gamma_j = e^{i\theta_j} - 1$. With $^*$ for the conjugate:

$$(a^* - \delta_j^*)\, x\, \gamma_j + (a - \delta_j)\, x^* \gamma_j^* + \delta_j (a^* - x^*) + \delta_j^* (a - x) - \delta_j \delta_j^* = 0,$$

the same equation with $y, b$ in place of $x, a$, and, because $|1 + \gamma_j| = 1$,

$$\gamma_j \gamma_j^* + \gamma_j + \gamma_j^* = 0.$$

Conjugation is not a polynomial operation, so treat $x^*, a^*, y^*, b^*$ and $\gamma_j^*$ as new independent unknowns $\hat x, \hat a, \hat y, \hat b, \hat\gamma_j$. These are *isotropic coordinates*. A solution is a real linkage exactly when each hatted unknown equals the conjugate of the plain one. For each $j$ the first two equations are linear in $\gamma_j$ and $\hat\gamma_j$. Solve them by Cramer's rule and substitute into the third. This leaves eight equations, $j = 1, \dots, 8$, in the eight unknowns $x, \hat x, a, \hat a, y, \hat y, b, \hat b$, each of degree 7.

**Step 3, Bezout counts.** *Bezout's theorem* bounds the number of isolated solutions of $n$ polynomial equations in $n$ unknowns by the product of their degrees. Here that is $7^8 = 5{,}764{,}801$. Wampler, Morgan and Sommese reduce it in two ways. They introduce products $n = a\hat x$, $\hat n = \hat a x$, $m = b \hat y$, $\hat m = \hat b y$ as new unknowns, which gives 12 equations (4 quadrics and 8 quartics, total degree $2^4 \cdot 4^8 = 1{,}048{,}576$). They then split the unknowns into the groups $\{x, \hat x, a, \hat a, n, \hat n\}$ and $\{y, \hat y, b, \hat b, m, \hat m\}$. The *two-homogeneous Bezout number* bounds the solutions by the coefficient of $\alpha^6 \beta^6$ in the product, over the equations, of their degrees in each group:

$$(2\alpha)^2 (2\beta)^2 (2\alpha + 2\beta)^8 \ \to\ 2^4 \cdot 2^8 \cdot \binom{8}{4} = 286{,}720.$$

**Step 4, symmetries.** Two symmetries act on the solutions. The swap $S$ exchanges the two groups of unknowns, that is, the left and right sides of the same linkage. The Roberts map

$$R(x, a, y, b) = \left( \frac{(x - a)y}{x - y},\ \frac{bx - ay}{x - y},\ a - x,\ a \right),$$

applied in the same way to the hatted unknowns, sends a solution to one of its cognates, and $R^3$ is the identity. Together they generate a group of six, so the nondegenerate solutions come in sixes.

**Step 5, the computation.** Wampler, Morgan and Sommese built a start system with all 286,720 solutions known and nonsingular, and tracked the paths to random complex points. Because of $S$ only half the paths, 143,360, had to be tracked. After removing degenerate and singular endpoints, 4326 nondegenerate nonsingular solutions remained, falling into 1442 cognate triples; each solution and its swap give 8652 in all. One triple was first found incomplete, and its third member was recovered with the cognate formula. The run took 331.9 hours of CPU time on an IBM 3081. By coefficient-parameter continuation (Morgan and Sommese 1989), the 1442 representatives then serve as start points for any other nine points, so later problems track only 1442 paths.

**Step 6, from evidence to proof.** Coefficient-parameter continuation also gives the logic of a proof. Outside a proper algebraic subset of parameters, the number of nonsingular isolated solutions is the same, and no parameter value has more nonsingular isolated solutions than this generic number. So certifying $N$ distinct nonsingular solutions at one instance proves that the generic number is at least $N$. Hauenstein and Sottile did this with alphaCertified for 8652 solutions of one instance, in floating-point arithmetic. The upper bound is harder, since it must exclude solutions that the numerics missed. Hauenstein and Helmer studied upper bounds by probabilistic saturation. Brysiewicz (2026) identifies the coupler curves with an open subset of the Grassmannian $\mathrm{Gr}(3, 6)$ and writes a new sparse system for the problem. The *mixed volume* of its Newton polytopes is 5538. By Bernstein's theorem this is the number of solutions with all coordinates nonzero for generic coefficients with the same monomials, and an upper bound for the actual coefficients. He proves that 4096 of these solutions escape to coordinates zero or infinity in the specialization, which leaves at most $5538 - 4096 = 1442$. With a certified instance having 1442, this gives the exact count.

**A check of the formulation.** Take the four-bar with $A = (0, 0)$, $B = (9, 0)$, $|AD| = 15$, $|DC| = 5$, $|BC| = 13$, and $P$ the midpoint of $DC$, the linkage of the [path generation](/path-generation/) page. At input angles $30°, 37.5°, \dots, 90°$ its coupler point passes through

| $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $P_j$ | $(15.1618, 8.7389)$ | $(14.3106, 9.7952)$ | $(13.0878, 10.9124)$ | $(11.6313, 11.9224)$ | $(9.9892, 12.7582)$ | $(8.1935, 13.3767)$ | $(6.2682, 13.7421)$ | $(4.2228, 13.8133)$ | $(2, 13.5)$ |

The eight degree-7 equations of Step 2 have residuals at most $9 \times 10^{-8}$ at this linkage, while a perturbation of size 0.05 in the unknowns makes them of order $10^5$. Newton's method started from such a perturbation returns to the linkage in five steps with quadratic convergence, so the solution is nonsingular. Applying $R$ and $S$ gives five more solutions with residuals of the same size, and $R^3$ returns the start to within $10^{-14}$. The cognates have fixed pivots $(0, 0)$ and $(4.5, 0)$, and $(4.5, 0)$ and $(9, 0)$, as on the path generation page. Running this check is not a search for the other 1441 curves, which needs a full homotopy.

## Consequences

**Exact path design has a ceiling of nine points.** For nine generic points there is a finite list of four-bars, and it can now be computed in full. A designer can then filter the list instead of guessing. Wampler, Morgan and Sommese stress that most solutions fail in practice: they are complex, or they have a *branch defect* (the points lie on different assembly branches), an *order defect* (the points are visited in the wrong order), or a poor [transmission angle](/transmission-angle/). In their Problem 2 every real solution had a branch or order defect, which proves that the nine points must be moved, something trial and error could not show.

**Fewer points leave freedom.** With fewer than nine points the solutions form a family of dimension $9 - n$, and the freedom is used to meet other goals. With prescribed timing at most five points can be met, and the problem splits into two dyad problems, as on the [Burmester theory](/burmester-theory/) and [path generation](/path-generation/) pages. With many points, or a whole curve, the problem is approximate and becomes [optimization-based synthesis](/optimization-based-linkage-synthesis/).

**A benchmark for numerical algebraic geometry.** The problem was one of the first large engineering systems solved completely by homotopy continuation, and it is used as a test of software for [polynomial system solving](/polynomial-system-solving/) and for certification of solutions, for example by the [interval Newton method](/interval-newton-method/) and Smale's alpha theory.

## Tightness

**Nine cannot be raised.** By Step 1, ten generic points lie on no coupler curve.

**The points must be generic.** No more than six of the nine points may lie on one circle or one line. A coupler curve has degree 6 and passes three times through each circular point at infinity (see the [coupler curve](/coupler-curve/) page). A circle has degree 2 and passes once through each circular point, so by Bezout's theorem it meets the curve in 12 points counted with multiplicity, at least 3 of them at each circular point. That leaves at most 6 finite points unless the circle is part of the curve, which happens only for degenerate four-bars. A line meets a curve of degree 6 in at most 6 points. So if seven of the points are on a circle or a line, there is no nondegenerate solution. Wampler, Morgan and Sommese note that their Problem 1, with eight of the nine points near a circle, is close to this case and took longer to solve than their Problems 2 and 3.

**The Bezout counts are far from tight.** The total degree $7^8 = 5{,}764{,}801$ and the two-homogeneous count 286,720 both exceed 8652 by large factors, because most of their solutions are degenerate. The mixed volume 5538 of Brysiewicz's system exceeds 1442 by exactly the 4096 solutions he shows escape the torus.

**The real count is not fixed.** It was 21, 45, 64 and 120 cognate triples out of 1442 in the four examples. In their fourth example the nine points lie on an ellipse, which also produced singular solutions, Cardan (elliptic) mechanisms with sliders. Hauenstein and Sottile certified, for the nine points of Problem 3, that 64 of the 1442 curves are real. The largest possible number of real solutions is not known to me.

## History

Alt stated the problem in 1923 in a paper on producing given plane curves with the four-bar. Freudenstein and Sandor (1959) used a digital computer for path generation with prescribed timing, which has fewer points. Roth and Freudenstein (1963) attacked the nine-point problem with a numerical continuation they called the bootstrap method, as a special case of geared five-bars. They worked in real variables and found some solutions but did not aim to find them all. Tsai and Lu (1989) used a complex homotopy, again finding some solutions. Wampler, Morgan and Sommese (1992) combined elimination, the two-homogeneous formulation and parameter continuation to find all 1442 cognate triples. Hauenstein and Sottile (2012) certified the solutions of one instance, and Hauenstein and Helmer (2020) noted that a proof that no solution was missed was still lacking. Brysiewicz's 2026 preprint claims to close the problem with a proof of the upper bound.

## References
