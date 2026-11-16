---
tag: C37Z8Q
kind: theorem
slug: six-r-inverse-kinematics-sixteen-solutions
name: Sixteen solutions of the general 6R inverse kinematics
aliases:
- Lee-Liang theorem
- 6R sixteen solutions
area: robotics/robot-kinematics
level: advanced
summary: The inverse kinematics of a general six-revolute arm has at most 16 complex solutions, and the bound is reached.
prereqs: [inverse-kinematics, denavit-hartenberg-convention, raghavan-roth-method]
see_also: [pieper-criterion, homotopy-continuation, resultant, stewart-gough-forward-kinematics, polynomial-root-finding, kinematic-decoupling, paden-kahan-subproblems, robot-workspace]
sources:
  - book: "Madhusudan Raghavan and Bernard Roth, Inverse kinematics of the general 6R manipulator and related linkages, Journal of Mechanical Design 115(3), 502-508, 1993"
    locator: the elimination to a polynomial of degree 16 and the back substitution (general locator)
  - book: "Hong-You Lee and Chong-Gao Liang, Displacement analysis of the general spatial 7-link 7R mechanism, Mechanism and Machine Theory 23(3), 219-226, 1988"
    locator: the polynomial of degree 16 for the 7R loop (general locator)
  - book: "E. J. F. Primrose, On the input-output equation of the general 7R-mechanism, Mechanism and Machine Theory 21(6), 509-510, 1986"
    locator: the proof that the 7R loop has at most 16 positions
  - book: "Lung-Wen Tsai and Alexander P. Morgan, Solving the kinematics of the most general six- and five-degree-of-freedom manipulators by continuation methods, Journal of Mechanisms, Transmissions, and Automation in Design 107, 189-200, 1985"
    locator: the 16 solutions found by continuation and the conjecture that 16 is the bound
  - book: "Rachid Manseur and Keith L. Doty, A robot manipulator with 16 real inverse kinematic solution sets, International Journal of Robotics Research 8(5), 1989"
    locator: from page 75, the arm and the pose with 16 real solutions
  - book: "Joseph Duffy and Carl Crane, A displacement analysis of the general spatial 7-link, 7R mechanism, Mechanism and Machine Theory 15(3), 153-169, 1980"
    locator: the first reduction, to a polynomial of degree 32
---

An arm with six revolute joints in general position has at most 16 solutions of its [inverse kinematics](/inverse-kinematics/) for a given pose of the hand, even when complex joint angles are counted.
For a general arm and pose there are exactly 16 complex solutions, and Manseur and Doty (1989) built an arm and a pose for which all 16 are real.
So 16 is the exact bound, both over the complex numbers and over the real numbers.
The number is the degree of the polynomial that the [Raghavan-Roth method](/raghavan-roth-method/) reaches.
Arms with special geometry, such as a spherical wrist, have fewer solutions; see [Pieper's criterion](/pieper-criterion/), which gives at most 8.

## Statement

Take an arm with six revolute joints and Denavit-Hartenberg parameters $(a_i, \alpha_i, d_i)$, $i = 1, \ldots, 6$, and a target pose $T$ in $SE(3)$.
Write the pose equation $A_1(\theta_1) \cdots A_6(\theta_6) = T$ in the half angle tangents $x_i = \tan(\theta_i/2)$.
This turns it into a system of polynomial equations, and a solution is a point $(x_1, \ldots, x_6)$ in $\mathbb{C}^6$, or a point at infinity for an angle of $\pi$.

**Theorem.**

1. (Primrose; Lee and Liang; Raghavan and Roth.) For a general arm and pose, the solution set is finite and has at most 16 points.
2. For the parameters and poses outside a proper algebraic subset, the solution set has exactly 16 points.
3. (Manseur and Doty.) There is an arm and a pose with 16 real solutions.

Since the parameters and the pose are real, the complex solutions that are not real come in conjugate pairs; for general data the number of real solutions is even, from 0 to 16.

## In plain words

Write down the equations that say the hand is at a given pose.
Allow the angles to be complex numbers, which makes the counting clean.
No matter how the six joints are placed, as long as the answers are isolated, there are at most 16 of them.
For almost every arm there are exactly 16, though most of them may be complex and so cannot be used.
Someone has also built an arm where all 16 are real, so 16 real poses of the arm can reach the same hand pose.

## Proof

The proof is the elimination of Raghavan and Roth.
The page gives its steps; the expansion of the large determinant in the last step is a symbolic computation done in their paper, and we do not repeat it here.
The [Raghavan-Roth method](/raghavan-roth-method/) page proves every step in full for the smaller 3R position problem.

**Step 1: equations free of $\theta_6$.**
Write the loop as $A_3A_4A_5 = A_2^{-1}A_1^{-1}\,T\,A_6^{-1}$.
The rotation $A_6^{-1}$ starts with $R_z(-\theta_6)$, which fixes the $z$ axis and the origin.
So the third and fourth columns of both sides, a direction $\mathbf l$ and a point $\mathbf p$, do not contain $\theta_6$.
This gives 6 scalar equations in $\theta_1, \ldots, \theta_5$.

**Step 2: the 14 equations.**
Add $\mathbf p \cdot \mathbf p$, $\mathbf p \cdot \mathbf l$, $\mathbf p \times \mathbf l$ and $(\mathbf p \cdot \mathbf p)\,\mathbf l - 2(\mathbf p \cdot \mathbf l)\,\mathbf p$ of both sides.
These products keep the degree in the sines and cosines low, because a rotation keeps lengths, dot and cross products.
The result is 14 equations of the form
$$A(\theta_3)\,X_{45} = B\,X_{12},$$
where $X_{45}$ holds the 9 terms $s_4s_5, s_4c_5, c_4s_5, c_4c_5, s_4, c_4, s_5, c_5, 1$, $X_{12}$ holds the 8 terms $s_1s_2, s_1c_2, c_1s_2, c_1c_2, s_1, c_1, s_2, c_2$, $B$ is constant, and $A$ is affine in $(\cos\theta_3, \sin\theta_3)$.

**Step 3: eliminate $\theta_1$ and $\theta_2$.**
Use 8 of the 14 equations to solve for $X_{12}$, and put the result into the other 6.
This leaves 6 equations $\Sigma'(\theta_3)\,X_{45} = 0$ that do not contain $\theta_1$ or $\theta_2$.

**Step 4: the dialytic step.**
With $x_4$ and $x_5$, multiply each equation by $(1 + x_4^2)(1 + x_5^2)$.
Each becomes a sum of the 9 terms $x_4^ix_5^j$ with $0 \le i, j \le 2$.
Multiply the 6 equations by $x_4$ as well, which gives 6 more equations.
Together the 12 equations are linear in the 12 terms $x_4^ix_5^j$ with $0 \le i \le 3$ and $0 \le j \le 2$:
$$\Sigma(x_3)\,\big(x_4^3x_5^2, \ldots, 1\big)^T = 0,$$
with a $12 \times 12$ matrix $\Sigma(x_3)$ whose entries are polynomials of degree at most 2 in $x_3$.
A solution gives a nonzero vector in the kernel, so $\det\Sigma(x_3) = 0$.

**Step 5: the degree.**
The determinant has degree at most 24 in $x_3$.
It contains the factor $(1 + x_3^2)^4$, which comes from the conversion of $\cos\theta_3$ and $\sin\theta_3$ and gives no solution.
What is left is a polynomial $f(x_3)$ of degree at most 16.

**Step 6: back substitution.**
For a root $x_3$ at which $\Sigma(x_3)$ has rank 11, the kernel is one dimensional, and its vector fixes $x_4$ and $x_5$ as ratios of its entries.
Then $X_{12}$ follows from the linear system of Step 3, which fixes $\theta_1$ and $\theta_2$, and $\theta_6$ follows from the remaining columns of the loop equation.
So each root gives at most one solution.

**Part 1.**
For a general arm and pose the rank conditions hold, $f$ is not zero everywhere, and the map from solutions to roots of $f$ is one to one, so there are at most 16 solutions.
Primrose (1986) proved the same bound for the general 7R loop, which covers the general 6R arm, since a 6R arm with a fixed hand pose closes a 7R loop.

**Part 2.**
The conditions that fail somewhere are polynomial equations in the data, so they fail only on a proper algebraic subset, provided they hold at one point.
The arm of Manseur and Doty is such a point: there $f$ has 16 distinct real roots, so $f$ has degree 16 and the leading coefficient is not zero.
Outside a proper algebraic subset, $f$ then has degree 16 and 16 distinct roots, and each gives one solution.

**Part 3.**
This is the arm of Manseur and Doty, whose 16 real solutions they list in their paper. $\square$

## Consequences

- **Algorithms that find all solutions.** The [Raghavan-Roth method](/raghavan-roth-method/), in the eigenvalue form of Manocha and Canny (1994), finds all 16 in well under a millisecond.
[Homotopy continuation](/homotopy-continuation/) can track 16 paths, one per solution, from a start system that has the same structure.
- **Special arms have fewer.** An arm that meets [Pieper's criterion](/pieper-criterion/) has at most 8, and simpler arms fewer still.
- **The number of real solutions is even** for general data, because the nonreal ones come in conjugate pairs.
- **The 7R loop.** The same count holds for the positions of a closed loop of seven revolute joints with one input angle fixed, the form in which Duffy and Crane, Primrose, and Lee and Liang studied it.
- **Compare.** The forward kinematics of the general [Stewart-Gough platform](/stewart-gough-forward-kinematics/) is the analogous count for a parallel robot, with the bound 40.

## Tightness

- **Over the complex numbers.** Part 2 says that 16 is reached for almost all data, so the bound cannot be lowered.
- **Over the real numbers.** Part 3 says that 16 real solutions also occur.
For a random arm and pose, most of the 16 solutions are usually complex.
- **The generality hypothesis is needed.** Special arms and poses can have a continuum of solutions.
For example, if two consecutive axes coincide, or an arm with a spherical wrist is in a wrist singularity, only the sum of two angles is fixed.
- **Earlier bounds.** Before the bound of 16, the best elimination, by Duffy and Crane (1980), gave a polynomial of degree 32, so it allowed up to 32 solutions.

## History

Pieper (1968) solved arms with three intersecting axes and left the general 6R arm open.
Duffy and Crane (1980) reduced the equivalent 7R loop to a polynomial of degree 32.
Tsai and Morgan (1985) solved arms by homotopy continuation, found 16 solutions, and conjectured that 16 is the bound.
Primrose (1986) proved that there are at most 16.
Lee and Liang (1988) found a polynomial of degree 16 for the 7R loop.
Manseur and Doty (1989) gave an arm with 16 real solutions.
Raghavan and Roth presented their elimination in 1990 and published it in 1993, and Manocha and Canny (1994) made it fast and accurate as an eigenvalue problem.

## References
