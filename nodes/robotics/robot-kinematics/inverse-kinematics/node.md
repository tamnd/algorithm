---
tag: M1EW6B
kind: problem
slug: inverse-kinematics
name: Inverse kinematics
aliases:
- IK
- inverse kinematics problem
area: robotics/robot-kinematics
level: intro
summary: Given a desired end effector pose, find joint values that reach it. There may be none, finitely many (at most 16 for a general 6R arm) or infinitely many (a redundant arm).
prereqs: [forward-kinematics]
see_also: [six-r-inverse-kinematics-sixteen-solutions, pieper-criterion, paden-kahan-subproblems, raghavan-roth-method, newton-raphson-inverse-kinematics, damped-least-squares-inverse-kinematics, kinematic-redundancy, robot-workspace]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 6, Inverse Kinematics (analytic inverse kinematics, and numerical inverse kinematics by the Newton-Raphson method)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Section 2.12, Inverse Kinematics Problem, and Section 3.7, Inverse Kinematics Algorithms
  - book: "Donald L. Pieper, The Kinematics of Manipulators Under Computer Control, PhD thesis, Stanford University, 1968 (Stanford Artificial Intelligence Memo AIM-72)"
    locator: the closed form solution for arms with three consecutive revolute axes that meet in a point (general locator)
  - book: "E. J. F. Primrose, On the input-output equation of the general 7R-mechanism, Mechanism and Machine Theory 21(6), 1986"
    locator: pages 509 to 510, the bound of 16 on the number of solutions
  - book: "R. Manseur and K. L. Doty, A robot manipulator with 16 real inverse kinematic solution sets, International Journal of Robotics Research 8(5), 1989"
    locator: an arm and a pose with 16 real solutions (pages 75 to 79; one index gives 75 to 78)
  - book: "H.-Y. Lee and C.-G. Liang, Displacement analysis of the general spatial 7-link 7R mechanism, Mechanism and Machine Theory 23(3), 1988"
    locator: pages 219 to 226, a univariate polynomial of degree 16 for the general 7R loop, which is the inverse kinematics of the general 6R arm
  - book: "M. Raghavan and B. Roth, Inverse kinematics of the general 6R manipulator and related linkages, Journal of Mechanical Design 115(3), 1993"
    locator: pages 502 to 508, the elimination that leads to a polynomial of degree 16
---

Inverse kinematics asks for the joint values that put the end of a robot at a given position and orientation. It is the reverse of [forward kinematics](/forward-kinematics/). Forward kinematics always has one answer for a serial arm. Inverse kinematics can have no answer (the target is out of reach), a finite number (an arm with an elbow up and an elbow down), or infinitely many (an arm with more joints than the task needs). For a general arm with six revolute joints there are at most 16 solutions, and some arms reach 16 real ones. Most industrial arms are built so that a closed form solution exists. Other arms use numerical methods that find one solution near a starting guess.

## In plain words

You know where you want the gripper to be and which way it should point. Which angles must the motors turn to?

For a forward question there is always one answer: set the motors and look. The backward question is harder. The target may be too far away, and then there is no answer. Your own arm can touch a point on a table with the elbow up or down, so there can be several answers. An arm with more joints than it needs can reach the same point in a whole family of ways, so there can be endlessly many.

Some arms are built so that the answers come from a short list of formulas. For other arms you start from a guess, see how far the gripper is from the target, change the angles a little in the right direction, and repeat until the gripper is close enough.

## Definition

**Input.** An open chain robot with $n$ one-freedom joints and forward kinematics $T : \mathbb{R}^n \to SE(3)$, for example in [product of exponentials](/product-of-exponentials-formula/) form; a set $Q$ of allowed joint values (the joint limits); and a target pose $X \in SE(3)$.

**Output.** One of the following, which give the main forms of the problem:

- *all solutions*: the set $\{\, q \in Q : T(q) = X \,\}$;
- *one solution*: some $q \in Q$ with $T(q) = X$, or the answer that none exists;
- *approximate solution*: a $q$ that minimizes a distance from $T(q)$ to $X$, which is the usual form for numerical methods.

A target $X$ has a solution if and only if it is a reachable pose, so the position part must lie in the [workspace](/robot-workspace/).

**Number of solutions.** With $n = 6$ joints and a 6-dimensional target, the equation $T(q) = X$ has as many unknowns as equations, and for a general arm and a general reachable target the solution set is finite. With $n > 6$ the arm is [redundant](/kinematic-redundancy/): if the Jacobian has rank 6 at a solution, the implicit function theorem shows that the solutions near it form a manifold of dimension $n - 6$, the self-motion manifold. With $n < 6$ most poses cannot be reached, and the task is reduced, for example to a position only.

## Variants

| variant | solutions | method | status |
|---|---|---|---|
| planar 2R arm, position of the tip | 0, 1, 2, or a circle when $L_1 = L_2$ and the target is the base | closed form | elementary |
| 6R arm with three consecutive axes that meet in a point (spherical wrist) | at most 8: up to 4 for the position, 2 for the wrist | closed form ([Pieper criterion](/pieper-criterion/), [kinematic decoupling](/kinematic-decoupling/)) | Pieper 1968 |
| general 6R arm | at most 16, and 16 real solutions occur | elimination to one polynomial of degree 16 | [16 solutions theorem](/six-r-inverse-kinematics-sixteen-solutions/) |
| redundant arm, $n > 6$ | infinitely many at regular targets | numerical, with a secondary goal | [kinematic redundancy](/kinematic-redundancy/) |
| velocity inverse kinematics | solve $J(q)\dot q = \mathcal{V}$ | linear algebra | see [resolved rate motion control](/resolved-rate-motion-control/) |

## Examples

**A planar 2R arm**, $L_1 = L_2 = 1$ m, target point $(x, y)$. The law of cosines gives

$$\cos q_2 = \frac{x^2 + y^2 - L_1^2 - L_2^2}{2L_1L_2}, \qquad q_1 = \operatorname{atan2}(y, x) - \operatorname{atan2}(L_2\sin q_2,\ L_1 + L_2\cos q_2).$$

- Target $(1, 1)$: $\cos q_2 = (2 - 2)/2 = 0$, so $q_2 = \pm\pi/2$. For $q_2 = \pi/2$, $q_1 = \pi/4 - \operatorname{atan2}(1, 1) = 0$. For $q_2 = -\pi/2$, $q_1 = \pi/4 + \pi/4 = \pi/2$. The two solutions are $(0, \pi/2)$ and $(\pi/2, -\pi/2)$, elbow up and elbow down. Both give $(1, 1)$ by the forward formula.
- Target $(2, 0)$: $\cos q_2 = 1$, one solution $(0, 0)$, the arm stretched out. It is on the boundary of the workspace, where the Jacobian is singular.
- Target $(3, 0)$: $\cos q_2 = 2.5$, no solution.
- Target $(0, 0)$: $\cos q_2 = -1$, so $q_2 = \pi$, and every $q_1$ works. The solutions form a circle.

So one arm shows all three cases: none, finitely many, and infinitely many.

**A general 6R arm.** For most arms with six revolute joints and a reachable pose, the solutions are the real roots of one polynomial of degree 16, and Manseur and Doty (1989) gave an arm and a pose with 16 real solutions. An industrial arm such as the PUMA 560 has a spherical wrist and reaches some poses in 8 ways.

## Known algorithms

Costs are counts of arithmetic operations and function calls in the [real RAM](/real-ram/) model, for a 6-dimensional target.

| method | cost | guarantee | notes |
|---|---|---|---|
| closed form by geometry, [Paden-Kahan subproblems](/paden-kahan-subproblems/) | $O(1)$ for a fixed arm | all solutions | needs special geometry, such as a spherical wrist |
| algebraic elimination, [Raghavan-Roth method](/raghavan-roth-method/) | fixed for $n = 6$, plus the roots of a polynomial of degree 16 | all solutions of a general 6R arm | the roots are found numerically, often as eigenvalues |
| [homotopy continuation](/homotopy-continuation/) | fixed for $n = 6$; tracks one path per start solution | all isolated solutions, with probability one for random start systems | slower but general |
| [Newton-Raphson](/newton-raphson-inverse-kinematics/) | $O(n)$ per iteration for the Jacobian and a $6 \times 6$ solve | local quadratic convergence near a solution where $J$ has full rank | needs a good start; finds one solution |
| [Jacobian pseudoinverse](/jacobian-pseudoinverse-method/) and [damped least squares](/damped-least-squares-inverse-kinematics/) | $O(n)$ per iteration | local; damping trades accuracy for robustness near singularities | the damping factor is a tuning parameter |
| [Jacobian transpose](/jacobian-transpose-method/) | $O(n)$ per iteration | descent on the squared error, local | slow near the target |
| [CCD](/cyclic-coordinate-descent-inverse-kinematics/) and [FABRIK](/fabrik/) | $O(n)$ per sweep | none in general; heuristics | popular in animation |

## Bounds

- **Number of solutions (theorem).** A general 6R arm has at most 16 solutions for a given pose (Primrose 1986), and the bound is reached with real solutions (Manseur and Doty 1989). Lee and Liang (1988) and Raghavan and Roth (1993) reduce the problem to one polynomial of degree 16. Special geometries can have fewer solutions, or infinitely many, as the 2R arm at its base shows.
- **Redundant arms.** For $n > 6$ there is no finite bound. At a target where some solution has a Jacobian of rank 6, the solutions near it form a manifold of dimension $n - 6$.
- **Numerical methods (measured, not proved).** The number of Newton iterations needed in practice is a measurement. The proved result is local: quadratic convergence from a start close enough to a solution where the Jacobian has full rank.

## Reductions

- **To a closed loop.** Fix the end effector at the target pose and join it to the ground. The 6R arm then becomes a closed 7R loop, with the ground as the seventh link, and the inverse kinematics is the displacement analysis of that loop. This is the form in which Primrose and Lee and Liang studied the problem.
- **To polynomial equations.** With $c_i = \cos q_i$, $s_i = \sin q_i$ and $c_i^2 + s_i^2 = 1$, or with $t_i = \tan(q_i / 2)$, the equation $T(q) = X$ becomes a polynomial system. [Resultants](/resultant/) and [Gröbner bases](/groebner-basis/) eliminate variables, and [homotopy continuation](/homotopy-continuation/) solves the system numerically.
- **To least squares.** The approximate version minimizes $\|\log(T(q)^{-1}X)\|^2$, a [nonlinear least squares](/nonlinear-least-squares/) problem, which [Gauss-Newton](/gauss-newton-algorithm/) and [Levenberg-Marquardt](/levenberg-marquardt/) solve locally.
- **Decoupling.** For a spherical wrist, the wrist center depends only on the first three joints, so the problem splits into a position problem in 3 unknowns and an orientation problem in 3 unknowns.

## Applications

Robot programs give targets in task space, such as a weld seam or a pick point, and the controller solves inverse kinematics to get joint commands. Offline programming and simulation tools list all solutions to choose the one that avoids joint limits and collisions. Computer animation and motion capture solve inverse kinematics for the limbs of a character. Redundant arms use the extra freedoms for a secondary goal, such as staying away from joint limits, by [null space projection](/null-space-projection/).

## References
