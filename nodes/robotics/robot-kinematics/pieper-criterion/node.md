---
tag: 7G7R02
kind: theorem
slug: pieper-criterion
name: Pieper's criterion
aliases:
- spherical wrist solvability
area: robotics/robot-kinematics
level: core
summary: "Pieper showed that a six-joint arm with three consecutive axes that meet in one point has a closed-form inverse kinematics. The condition is sufficient, not necessary."
prereqs: [inverse-kinematics, denavit-hartenberg-convention, paden-kahan-subproblems]
see_also: [kinematic-decoupling, raghavan-roth-method, six-r-inverse-kinematics-sixteen-solutions, product-of-exponentials-formula, euler-angles, kinematic-singularity, robot-workspace, forward-kinematics]
sources:
  - book: "Donald L. Pieper, The kinematics of manipulators under computer control, Stanford Artificial Intelligence Project Memo AIM-72 (PhD thesis), Stanford University, 1968"
    locator: Sections 3.3.3 to 3.3.8, the closed-form solutions for arms with three intersecting axes
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Section 3.3, inverse kinematics by the Paden-Kahan subproblems
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: Section 5.2, Kinematic Decoupling
  - paper: doi:10.1016/j.mechmachtheory.2025.105971
    title: Alexander J. Elias and John T. Wen, IK-Geo, Unified robot inverse kinematics using subproblem decomposition, Mechanism and Machine Theory, 2025
    locator: the closed-form and one-dimensional search solutions for 6R arms with intersecting or parallel axes (general locator)
---

Pieper's criterion says when the [inverse kinematics](/inverse-kinematics/) of an arm with six joints can be solved in closed form.
Pieper (1968) showed that if three consecutive joint axes meet in one point, the problem splits into smaller problems, and the hardest of them is a polynomial of degree at most 4.
The usual case is an arm whose last three axes meet in a point, the spherical wrist; then the arm has at most 8 solutions for a pose.
The criterion is a sufficient condition only.
Many arms that do not meet it, such as arms with three parallel axes, also have closed forms.
This page proves the case of the spherical wrist.

## Statement

Take an arm with six revolute joints, with standard [Denavit-Hartenberg](/denavit-hartenberg-convention/) parameters $(a_i, \alpha_i, d_i)$.
Write $T_i = R_z(\theta_i)\,T_z(d_i)\,T_x(a_i)\,R_x(\alpha_i)$ and $T(\theta) = T_1 \cdots T_6$.
Suppose the axes of joints 4, 5 and 6 meet in one point $c$.
Let the target pose be $(R, p)$.

**Theorem (Pieper, the case of the last three axes).**

1. The point $c$ is fixed in link 3, and its target position $c^\ast$ depends only on $(R, p)$.
The angles $(\theta_1, \theta_2, \theta_3)$ of a solution are exactly the solutions of the position problem $T_1T_2T_3\,c_3 = c^\ast$, where $c_3$ are the coordinates of $c$ in frame 3.
2. If the arm and target are general (see the proof), the angle $\theta_3$ of a solution is a zero of a trigonometric polynomial of degree at most 2 that is not zero everywhere.
So there are at most 4 values of $\theta_3$; with $x_3 = \tan(\theta_3/2)$ they are roots of a polynomial of degree at most 4.
Each value gives exactly one $(\theta_1, \theta_2)$, by a linear system and an $\operatorname{atan2}$.
3. For each $(\theta_1, \theta_2, \theta_3)$, if the axes 4 and 5 are not parallel, the axes 5 and 6 are not parallel, and the target direction of axis 6 is not parallel to axis 4, there are at most 2 wrist solutions $(\theta_4, \theta_5, \theta_6)$, given by [Paden-Kahan](/paden-kahan-subproblems/) subproblems 2 and 1.

So such an arm has a closed-form solution, with at most 8 solutions for a general pose.

Pieper's thesis treats any three consecutive axes that meet in a point; the case of the first three axes follows from this one by inverting the chain.

## In plain words

If the last three joints all turn about lines through one point, those joints can only turn the hand about that point.
They cannot move the point.
So the first three joints alone must carry that point to the right place.
That is a smaller problem with three unknowns, and it has at most four answers.
Then the last three joints must turn the hand to the right direction, and that has at most two answers for each of the four.

## Proof

**Part 1: the wrist point.**
A joint moves the two links it connects relative to each other, but every point of its axis stays a common point of both links.
The axes of joints 4, 5 and 6 all pass through $c$, so $c$ is one point of links 3, 4, 5 and 6 at once.
So $c$ has constant coordinates $c_3$ in frame 3 and $c_6$ in frame 6, and $T_1T_2T_3\,c_3 = T(\theta)\,c_6$ for every $\theta$.
For a solution $T(\theta) = (R, p)$, so $T_1T_2T_3\,c_3 = R\,c_6 + p =: c^\ast$, which depends only on the target.
Conversely, any solution of the position problem gives a candidate for $(\theta_1, \theta_2, \theta_3)$, and Part 3 completes it or shows it has no completion.

**Part 2: the position problem.**
We have $T_3\,c_3 = R_z(\theta_3)\,u$ with the constant vector $u = (a_3, 0, d_3) + R_x(\alpha_3)\,c_3$.
Then $c^\ast = R_z(\theta_1)\,g$ with
$$g = (a_1, 0, d_1) + R_x(\alpha_1)\,R_z(\theta_2)\,h, \qquad h = (a_2, 0, d_2) + R_x(\alpha_2)\,R_z(\theta_3)\,u.$$
Write $c_i = \cos\theta_i$, $s_i = \sin\theta_i$, and $ca_1$, $sa_1$ for the cosine and sine of $\alpha_1$.
The vector $h$ and its squared length $|h|^2 = a_2^2 + d_2^2 + |u|^2 + 2(a_2, 0, d_2) \cdot R_x(\alpha_2)R_z(\theta_3)u$ are affine in $(c_3, s_3)$.
A rotation about $z$ keeps the length and the $z$ coordinate, so $|c^\ast|^2 = |g|^2$ and $c^\ast_z = g_z$.
Multiplying out, these two equations are
$$E_1:\ 2a_1h_1\,c_2 - 2a_1h_2\,s_2 + K = 0, \qquad E_2:\ sa_1h_2\,c_2 + sa_1h_1\,s_2 + L = 0,$$
with $K = |h|^2 + a_1^2 - d_1^2 - |c^\ast|^2 + 2d_1c^\ast_z$ and $L = d_1 + ca_1h_3 - c^\ast_z$, both affine in $(c_3, s_3)$.
This is the same computation as on the [Raghavan-Roth method](/raghavan-roth-method/) page, where $u = (a_3, 0, d_3)$.

Call the arm and target general if $a_1 \ne 0$, $sa_1 \ne 0$, $h_1^2 + h_2^2 > 0$ for every $\theta_3$, $(c^\ast_x, c^\ast_y) \ne (0, 0)$, and the function $q$ below is not zero everywhere.
Write $E_j$ as $P_jc_2 + Q_js_2 + K_j = 0$.
Then $D = P_1Q_2 - P_2Q_1 = 2a_1sa_1(h_1^2 + h_2^2) \ne 0$, so by Cramer's rule $(c_2, s_2) = (X/D, Y/D)$ with $X = Q_1K_2 - Q_2K_1$ and $Y = K_1P_2 - K_2P_1$.
A $\theta_2$ exists if and only if $X^2 + Y^2 = D^2$.
The cross terms cancel, and
$$X^2 + Y^2 - D^2 = (h_1^2 + h_2^2)\,q, \qquad q = 4a_1^2L^2 + sa_1^2K^2 - 4a_1^2sa_1^2(h_1^2 + h_2^2).$$
Since $h_1^2 + h_2^2 > 0$, the condition on $\theta_3$ is $q = 0$.
Each of $L$, $K$, $h_1$, $h_2$ is affine in $(c_3, s_3)$, so $q$ is a trigonometric polynomial of degree at most 2.
With $x_3 = \tan(\theta_3/2)$, the product $(1 + x_3^2)^2 q$ is a polynomial of degree at most 4 in $x_3$, and the angle $\theta_3 = \pi$ shows up as a drop of its degree.
A trigonometric polynomial of degree 2 that is not zero everywhere has at most 4 zeros in a period, so there are at most 4 values of $\theta_3$.
For each, $\theta_2$ is unique by Cramer's rule.
Then $(g_x, g_y)$ and $(c^\ast_x, c^\ast_y)$ have the same nonzero length, and exactly one $\theta_1$ modulo $2\pi$ rotates one onto the other: $\theta_1 = \operatorname{atan2}(c^\ast_y, c^\ast_x) - \operatorname{atan2}(g_y, g_x)$.
A polynomial of degree at most 4 has roots in radicals, so every step is in closed form.

**Part 3: the wrist.**
Use the frame of link 3 for the fixed $(\theta_1, \theta_2, \theta_3)$, and let $\omega_4$, $\omega_5$, $\omega_6$ be the unit directions of the three wrist axes when $\theta_4 = \theta_5 = \theta_6 = 0$, all through $c$.
The orientation part of the pose equation is $e^{\hat\omega_4\theta_4}e^{\hat\omega_5\theta_5}e^{\hat\omega_6\theta_6} = W$ with a known rotation $W$.
Apply both sides to $\omega_6$, which $e^{\hat\omega_6\theta_6}$ keeps:
$$e^{\hat\omega_4\theta_4}e^{\hat\omega_5\theta_5}\,\omega_6 = W\omega_6.$$
This is subproblem 2 for the point $c + \omega_6$ and two axes through $c$.
The unit vector $z = e^{\hat\omega_5\theta_5}\omega_6 = e^{-\hat\omega_4\theta_4}W\omega_6$ must lie on two circles of the unit sphere: the circle of vectors with $\omega_5 \cdot z = \omega_5 \cdot \omega_6$ and the circle with $\omega_4 \cdot z = \omega_4 \cdot W\omega_6$.
When $\omega_4$ and $\omega_5$ are not parallel, the two circles lie in planes that are not parallel, and they meet in at most 2 points.
Each point gives one $\theta_5$, because $\omega_6$ is not on axis 5, and one $\theta_4$, because $W\omega_6$ is not on axis 4.
So there are at most 2 pairs $(\theta_4, \theta_5)$.
For each pair, $M = e^{-\hat\omega_5\theta_5}e^{-\hat\omega_4\theta_4}W$ is a rotation with $M\omega_6 = \omega_6$, so it is a rotation about $\omega_6$.
Take a unit vector $v$ orthogonal to $\omega_6$; subproblem 1, $e^{\hat\omega_6\theta_6}v = Mv$, has exactly one solution $\theta_6$ modulo $2\pi$.
The two rotations $e^{\hat\omega_6\theta_6}$ and $M$ about $\omega_6$ agree on $v$, so they are equal, and the full orientation equation holds.
With Part 1 the position equation holds as well, since $p = c^\ast - Rc_6$ and $c$ is placed correctly.
So each arm solution gives at most 2 full solutions, and the arm has at most $4 \cdot 2 = 8$. $\square$

## Consequences

- **Kinematic decoupling.** The proof is the method of [kinematic decoupling](/kinematic-decoupling/): solve for the wrist center, then for the wrist angles.
For the common wrist with $\alpha_4 = -90°$ and $\alpha_5 = 90°$, Part 3 reduces to [ZYZ Euler angles](/euler-angles/).
- **The first three axes.** If the axes of joints 1, 2 and 3 meet in a point, write the inverse pose $T(\theta)^{-1} = T_6^{-1} \cdots T_1^{-1}$; it is the pose of a chain that runs from the hand to the base, whose last three axes meet, and the theorem applies to it.
- **Industrial arms.** Most six-axis industrial arms are built with a spherical wrist so that this theorem applies and the controller can use a fast closed form.
- **Wrist singularity.** The hypothesis of Part 3 fails when axis 6 lines up with axis 4; then only $\theta_4 + \theta_6$ is fixed, a [kinematic singularity](/kinematic-singularity/) with infinitely many solutions.

## Tightness

- **The bound 8 is reached.** Take the 3R arm of the [Raghavan-Roth example](/raghavan-roth-method/), $(a_i, \alpha_i, d_i) = (0.5\text{ m}, 120°, 0.5\text{ m})$, $(0.5\text{ m}, 30°, 1.0\text{ m})$, $(1.5\text{ m}, 0°, 0\text{ m})$, and add a spherical wrist with rows $(0, -90°, 0)$, $(0, 90°, 0)$, $(0, 0°, 0)$.
The pose made by the joint vector $(1, -0.5, -1, 0.4, 0.8, -0.3)$ rad has the wrist point at $(0.209252, 1.203738, -1.059310)$ m.
The four arm solutions of that page each give two wrist solutions, for example $(1, -0.5, -1, 0.4, 0.8, -0.3)$ and $(1, -0.5, -1, -2.741593, -0.8, 2.841593)$ rad.
All 8 joint vectors reproduce the pose to about $10^{-15}$.
- **The condition is not necessary.** An arm with three consecutive parallel axes also has a closed form, by planar geometry or by subproblems; Elias and Wen (2025) give closed forms for many such families.
Textbooks sometimes treat parallel axes as axes that meet at a point at infinity, but Pieper's proof does not cover that case.
- **The general arm.** Without such special geometry the best known reduction is a polynomial of degree 16, see [the 16 solutions theorem](/six-r-inverse-kinematics-sixteen-solutions/) and the [Raghavan-Roth method](/raghavan-roth-method/).
- **The general conditions matter.** If $a_1 = 0$ or $\sin\alpha_1 = 0$, Part 2 splits into simpler equations, and if the wrist point lies on axis 1, $\theta_1$ is free and there are infinitely many solutions.

## History

Pieper studied the kinematics of computer-controlled arms in his Stanford thesis of 1968.
He showed that an arm with three consecutive intersecting axes has a closed-form solution, built on a quartic, and noted that the general six-joint arm was much harder.
Paden (1986) and later Murray, Li and Sastry (1994) recast these solutions as sequences of subproblems in the product of exponentials form.
Elias and Wen (2025) extend the subproblem approach to arms with parallel axes and to arms that need a one-dimensional search.

## References
