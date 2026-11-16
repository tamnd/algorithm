---
tag: MGK2K1
kind: algorithm
slug: paden-kahan-subproblems
name: Paden-Kahan subproblems
aliases:
- Paden-Kahan subproblem method
area: robotics/robot-kinematics
level: advanced
summary: Three geometric subproblems of rotating points about one or two axes, with closed solutions, to which many inverse kinematics reduce.
model: real-ram
complexity:
  vars: {n: the number of joints of an arm that splits into subproblems}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1986
  people: [Bradley E. Paden, William Kahan]
  note: Paden wrote the subproblems with exponentials of twists in his Berkeley thesis and used them on the Stanford arm and an elbow arm; the name joins Paden and Kahan, whose part was not published as a paper.
prereqs: [inverse-kinematics, product-of-exponentials-formula, rodrigues-rotation-formula]
see_also: [kinematic-decoupling, pieper-criterion, inverse-kinematics, product-of-exponentials-formula, screw-motion, raghavan-roth-method, newton-raphson-inverse-kinematics, forward-kinematics]
sources:
  - book: "Bradley E. Paden, Kinematics and Control of Robot Manipulators, PhD thesis, University of California, Berkeley, 1986 (Technical Report UCB/ERL M86/5)"
    locator: Chapter 2 (subproblems written with exponentials of twists) and Chapter 3 (the Stanford arm and an elbow arm solved with them)
  - book: isbn:9780849379819
    title: "Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994"
    locator: Chapter 3, Section 3.3 (inverse kinematics, the Paden-Kahan subproblems and their use on an elbow arm)
  - paper: doi:10.1016/j.mechmachtheory.2025.105971
    title: "Alexander J. Elias and John T. Wen, IK-Geo: Unified robot inverse kinematics using subproblem decomposition, Mechanism and Machine Theory 209, 105971, 2025"
    locator: the subproblems 1 to 3 in a least squares form, the new subproblems 4 to 6, and the arms with three intersecting or three parallel axes
---

The Paden-Kahan subproblems are three small geometric problems about rotations of points, each with a closed form solution.
Subproblem 1 finds the angle of one rotation that moves a point to another point.
Subproblem 2 finds the angles of two rotations, about axes that meet, that move a point to another point.
Subproblem 3 finds the angle of one rotation that brings a point to a given distance from another point.
Many arms with six joints, among them most industrial arms, have an [inverse kinematics](/inverse-kinematics/) that splits into a chain of these subproblems.
The method then gives every solution, with no iteration and no starting guess.

## In plain words

Pin a stick to a wall at one end, so that it can only swing in a circle.
If you mark a point on the stick and another point on the circle, there is exactly one swing angle that carries the first point to the second.
That is the first subproblem.
The second subproblem uses two pins at the same place, one after the other, and asks for both angles.
The third asks for the swing angles that put the point at a given distance from a fixed spot.
Each answer comes from a short formula.
For a robot arm, you choose points that some joints leave in place.
Then the joints that do move them form one of these three problems, and you solve the arm a few joints at a time.

## The problem

**Input.**

- A revolute joint is a rotation about a line with a unit direction $\omega$ through a point $r$.
The rotation by $\theta$ takes a point $x$ to $r + R(\omega, \theta)(x - r)$, where $R(\omega, \theta) = e^{[\omega]\theta}$ by [Rodrigues' formula](/rodrigues-rotation-formula/).
In twist form this is $e^{[\xi]\theta}x$ with the screw axis $\xi = (\omega, -\omega \times r)$.
- **Subproblem 1:** one axis $(\omega, r)$ and two points $p$, $q$. Find $\theta$ with $e^{[\xi]\theta}p = q$.
- **Subproblem 2:** two axes $(\omega_1, r)$ and $(\omega_2, r)$ that meet at $r$ and are not parallel, and two points $p$, $q$. Find all $(\theta_1, \theta_2)$ with $e^{[\xi_1]\theta_1}e^{[\xi_2]\theta_2}p = q$.
- **Subproblem 3:** one axis $(\omega, r)$, two points $p$, $q$ and a distance $\delta \ge 0$. Find all $\theta$ with $|e^{[\xi]\theta}p - q| = \delta$.

**Output.** The solutions, or the report that there are none.
Subproblem 1 has 0 or 1 solution when $p$ is off the axis.
Subproblems 2 and 3 have 0, 1 or 2.

**Use on an arm.** For an arm in the space form of the [product of exponentials](/product-of-exponentials-formula/), $T(\theta) = e^{[\mathcal S_1]\theta_1}\cdots e^{[\mathcal S_n]\theta_n}M$, and a target pose $T_d$, the inverse kinematics asks for all $\theta$ with $T(\theta) = T_d$.
The trick is to apply both sides to a point that the last joints leave in place, or to compare distances that the first joints do not change.

## The algorithm

```pseudo id=main
SUBPROBLEM-1(ω, r, p, q)              ▷ θ with e^{[ξ]θ} p = q
L1  u ← p - r ;  v ← q - r
L2  u' ← u - ω ω^T u ;  v' ← v - ω ω^T v        ▷ parts orthogonal to the axis
L3  if ω^T u ≠ ω^T v or |u'| ≠ |v'| then return NO SOLUTION
L4  return atan2(ω^T (u' × v'), u'^T v')

SUBPROBLEM-2(ω1, ω2, r, p, q)         ▷ θ1, θ2 with e^{[ξ1]θ1} e^{[ξ2]θ2} p = q
L5  u ← p - r ;  v ← q - r ;  k ← ω1^T ω2
L6  α ← (k ω2^T u - ω1^T v) / (k^2 - 1) ;  β ← (k ω1^T v - ω2^T u) / (k^2 - 1)
L7  γ² ← (|u|^2 - α^2 - β^2 - 2αβk) / |ω1 × ω2|^2
L8  if γ² < 0 then return NO SOLUTION
L9  for γ in {+√γ², -√γ²}                       ▷ one value when γ² = 0
L10     c ← r + α ω1 + β ω2 + γ (ω1 × ω2)        ▷ the point between the two rotations
L11     θ2 ← SUBPROBLEM-1(ω2, r, p, c) ;  θ1 ← SUBPROBLEM-1(ω1, r, c, q)
L12     output (θ1, θ2)

SUBPROBLEM-3(ω, r, p, q, δ)           ▷ θ with |e^{[ξ]θ} p - q| = δ
L13 u ← p - r ;  v ← q - r ;  u', v' as in L2
L14 δ'^2 ← δ^2 - (ω^T (p - q))^2
L15 θ0 ← atan2(ω^T (u' × v'), u'^T v')
L16 c ← (|u'|^2 + |v'|^2 - δ'^2) / (2 |u'| |v'|)
L17 if |c| > 1 then return NO SOLUTION
L18 return θ0 - arccos c and θ0 + arccos c         ▷ one angle when |c| = 1
```

Line L4 is the signed angle from $u'$ to $v'$ about $\omega$.
Line L6 comes from two linear equations: the point $c$ rotates about $\omega_2$ from $p$ and about $\omega_1$ to $q$, so $\omega_2^{\mathsf T}(c - r) = \omega_2^{\mathsf T}u$ and $\omega_1^{\mathsf T}(c - r) = \omega_1^{\mathsf T}v$.
Line L7 then fixes the length of $c - r$ to $|u|$.
Lines L14 to L16 are the law of cosines in the plane orthogonal to the axis.
In floating point, the tests in L3, L8 and L17 use a small tolerance, and the code on this page clamps $c$ into $[-1, 1]$ when it is out by less than the tolerance.

**An elbow arm.** The code on this page solves an arm with six revolute joints in the layout of Murray, Li and Sastry.
Axis 1 is vertical through the base.
Axes 2 and 3 are horizontal and parallel, through the shoulder $q_s$ and the elbow.
Axes 4, 5 and 6 meet at the wrist center $q_w$.
The solution takes four steps.

1. The last three joints fix $q_w$, so $g_1 = T_dM^{-1}$ sends $q_w$ to the place $p_w = g_1q_w$ that the first three joints must reach.
The first two joints turn about axes through $q_s$, so they keep the distance to $q_s$, and $|e^{[\xi_3]\theta_3}q_w - q_s| = |p_w - q_s|$.
Subproblem 3 gives up to two values of $\theta_3$.
2. Subproblem 2 on the axes 1 and 2, which meet at $q_s$, moves $e^{[\xi_3]\theta_3}q_w$ to $p_w$ and gives up to two pairs $(\theta_1, \theta_2)$.
3. Now $g_2 = (e^{[\xi_1]\theta_1}e^{[\xi_2]\theta_2}e^{[\xi_3]\theta_3})^{-1}g_1 = e^{[\xi_4]\theta_4}e^{[\xi_5]\theta_5}e^{[\xi_6]\theta_6}$.
A point $p$ on axis 6 is left in place by joint 6, so subproblem 2 on the axes 4 and 5 with $p$ and $g_2p$ gives up to two pairs $(\theta_4, \theta_5)$.
4. Subproblem 1 on axis 6, with a point off that axis, gives $\theta_6$.

This gives up to $2 \cdot 2 \cdot 2 = 8$ solutions.

## Example

Take the elbow arm with a base height, two arm links and a tool offset of $l_0 = l_1 = l_2 = 1$ and $l_3 = 0.5$.
At $\theta = 0$, the shoulder is $q_s = (0, 0, 1)$, the elbow $(0, 1, 1)$, the wrist center $q_w = (0, 2, 1)$ and the tool point $(0, 2.5, 1)$.
The axes are $\omega_1 = \omega_4 = (0, 0, 1)$, $\omega_2 = \omega_3 = \omega_5 = (-1, 0, 0)$ and $\omega_6 = (0, 1, 0)$.
The target is the pose of $\theta^* = (0.3, -0.4, 0.9, 0.5, 0.7, -0.6)$, with the position $(-0.748090, 1.797966, 0.466418)$.

- Step 1: $p_w = (-0.531536, 1.718310, 0.909993)$ and $|p_w - q_s| = 1.800894$.
With two unit links, $|p_w - q_s|^2 = 2 + 2\cos\theta_3$, so $\cos\theta_3 = 0.621610$, and subproblem 3 returns $\theta_3 = \pm 0.9$.
- Step 2: for $\theta_3 = 0.9$, subproblem 2 returns $(\theta_1, \theta_2) = (0.3, -0.4)$ and $(-2.841593, 2.641593)$, the shoulder turned by $\pi$.
For $\theta_3 = -0.9$ it returns $(0.3, 0.5)$ and $(-2.841593, -2.741593)$.
- Steps 3 and 4 give two wrist solutions for each of the four arm solutions.

| $\theta_1$ | $\theta_2$ | $\theta_3$ | $\theta_4$ | $\theta_5$ | $\theta_6$ |
|---|---|---|---|---|---|
| 0.300000 | -0.400000 | 0.900000 | 0.500000 | 0.700000 | -0.600000 |
| 0.300000 | -0.400000 | 0.900000 | -2.641593 | 2.441593 | 2.541593 |
| 0.300000 | 0.500000 | -0.900000 | -1.336808 | 1.957305 | -2.257324 |
| 0.300000 | 0.500000 | -0.900000 | 1.804785 | 1.184287 | 0.884269 |
| -2.841593 | 2.641593 | 0.900000 | 1.336808 | -1.957305 | 0.884269 |
| -2.841593 | 2.641593 | 0.900000 | -1.804785 | -1.184287 | -2.257324 |
| -2.841593 | -2.741593 | -0.900000 | 2.641593 | -2.441593 | -0.600000 |
| -2.841593 | -2.741593 | -0.900000 | -0.500000 | -0.700000 | 2.541593 |

The forward kinematics of each row matches the target to within $3 \cdot 10^{-15}$.
In each pair of rows, the second wrist solution is the first one with $\theta_4$ and $\theta_6$ moved by $\pi$ and $\theta_5$ replaced by $\pi - \theta_5$, modulo $2\pi$, which is the usual wrist flip.

## Correctness

**Subproblem 1.** A rotation about $\omega$ keeps the component of $u$ along $\omega$ and turns the orthogonal part $u'$ by $\theta$ in the plane orthogonal to $\omega$.
So a solution exists exactly when $\omega^{\mathsf T}u = \omega^{\mathsf T}v$ and $|u'| = |v'|$, and then $\theta$ is the signed angle from $u'$ to $v'$, which L4 computes.
If $u' = 0$, the point is on the axis and every $\theta$ works.

**Subproblem 2.** If $(\theta_1, \theta_2)$ is a solution, put $c = e^{[\xi_2]\theta_2}p$.
Then $z = c - r$ has the same component along $\omega_2$ as $u$, the same component along $\omega_1$ as $v$, and the length $|u|$.
Since $\omega_1$, $\omega_2$ and $\omega_1 \times \omega_2$ form a basis, these three facts give $z = \alpha\omega_1 + \beta\omega_2 + \gamma(\omega_1 \times \omega_2)$ with $\alpha$, $\beta$ from L6 and $\gamma^2$ from L7.
Conversely, each such $c$ meets the conditions of subproblem 1 twice, once for $p \to c$ about $\omega_2$ and once for $c \to q$ about $\omega_1$, so L11 gives a solution.
So the solutions are in one to one correspondence with the real roots $\gamma$, and there are at most 2 when $p$ is off both axes.

**Subproblem 3.** The distance splits into the part along $\omega$, which the rotation does not change, and the part in the orthogonal plane.
So $|e^{[\xi]\theta}p - q|^2 = (\omega^{\mathsf T}(p - q))^2 + |u'|^2 + |v'|^2 - 2|u'||v'|\cos(\theta_0 - \theta)$, and the condition is $\cos(\theta_0 - \theta) = c$ with $c$ from L16.

**The arm.** Every solution of the arm passes the tests of the four steps, and every output of the four steps satisfies $T(\theta) = T_d$, so the method returns exactly the set of solutions.
The proof page gives the details, with the hypotheses that the chosen points are off the axes.

## Complexity

Each subproblem is a fixed number of dot products, cross products, square roots and calls to atan2 and arccos, so it costs $\Theta(1)$ in the [real RAM](/real-ram/).
An arm that splits into subproblems needs a fixed number of them per solution, and the products of the $n$ joint exponentials that form $g_1$, $g_2$ and $g_3$ cost $\Theta(n)$.
For a fixed arm with six joints, all eight solutions take a few hundred arithmetic operations.

## Properties

- **All solutions.** Each subproblem returns all of its solutions, so the arm solution lists the full finite set, not one solution near a guess.
- **No iteration.** There is no starting point, no tolerance on convergence and no failure mode from a poor guess.
- **Frame free.** The formulas use only axes and points, so they work in any base frame and do not need Denavit-Hartenberg parameters.
- **Geometry first.** The method needs the arm to have the right geometry, such as two axes that meet, or a point that some joints leave in place.
- **Degenerate cases.** If $p$ lies on an axis, subproblem 1 has infinitely many solutions; for the arm, this happens at a [kinematic singularity](/kinematic-singularity/), such as the wrist with the axes 4 and 6 in line.

## Variants and improvements

- **More subproblems.** Paden's thesis describes four subproblems, and the textbook form keeps three.
Elias and Wen add subproblems 4 to 6 and use the six of them to solve arms with three intersecting or three parallel axes, among other layouts.
- **Approximate answers.** Elias and Wen also give each subproblem a form that returns an approximate answer when there is no exact solution, which is useful near the edge of the workspace.
- **Translations.** Prismatic joints lead to similar subproblems, such as a translation along an axis followed by a rotation.
- **Other arms.** The Stanford arm, with a prismatic third joint, and arms with offsets also reduce to subproblems with a different order of steps.
- **Arms that do not split.** For a general 6R arm, use an algebraic method such as the [Raghavan-Roth method](/raghavan-roth-method/), or a numerical one such as [Newton-Raphson inverse kinematics](/newton-raphson-inverse-kinematics/).

## When to use it

Use the subproblems when the arm has three axes that meet in a point, or other special geometry that lets you isolate joints, and you want all solutions in closed form.
This covers most industrial arms with a spherical wrist; see [Pieper's criterion](/pieper-criterion/) and [kinematic decoupling](/kinematic-decoupling/).
When the arm does not have such geometry, use an algebraic or a numerical method.

## Pitfalls

- **Points on an axis.** The point given to a subproblem must be off the axes of that subproblem, or the angle is not determined. Choose it once for the arm, not for each target.
- **Tolerances.** The exact tests of L3, L8 and L17 must be tests with a small tolerance in floating point, or a reachable target near the edge of the workspace can be rejected.
- **The order of the rotations.** Subproblem 2 is about $e^{[\xi_1]\theta_1}e^{[\xi_2]\theta_2}$, the second rotation first applied to $p$; swapping the axes swaps the meaning of the output.
- **Duplicate solutions.** When $\gamma = 0$ or $c = \pm 1$, the two branches coincide; return one solution, or the caller counts it twice.
- **Angle ranges.** The angles come out of atan2 and arccos and need wrapping into the range of each joint, and the joint limits must be checked after.

## Implementations

## History

Paden (1986) wrote rigid motions as exponentials of twists in his Berkeley thesis and described a small set of subproblems that occur again and again in robot kinematics.
He solved the Stanford arm and an elbow arm with them.
The name joins Paden and William Kahan, whose part in the idea was not published as a paper.
Murray, Li and Sastry (1994) gave the three subproblems their standard form in their textbook.
Elias and Wen (2025) extended the set to six subproblems and solved many more arm layouts with them.

## References
