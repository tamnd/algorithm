---
tag: DVASYR
kind: problem
slug: inverse-dynamics
name: Inverse dynamics
aliases:
- inverse dynamics problem
area: robotics/robot-dynamics
level: core
summary: "Given the state q, q' of a robot and a wanted acceleration q'', find the joint torques tau = M q'' + C q' + g. Solved in O(n) by the recursive Newton-Euler algorithm."
prereqs: [manipulator-equation]
see_also: [recursive-newton-euler-algorithm, forward-dynamics, computed-torque-control, newton-euler-equations, composite-rigid-body-algorithm, linearity-in-dynamic-parameters, time-optimal-path-parameterization, floating-base-dynamics]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: "Chapter 8, Section 8.3 (Newton-Euler inverse dynamics: derivation and algorithm) and Section 8.4 (dynamic equations in closed form)"
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: Chapter 5 (inverse dynamics, the recursive Newton-Euler algorithm) and Chapter 10 (accuracy and efficiency)
  - paper: "J. Y. S. Luh, M. W. Walker and R. P. C. Paul, On-line computational scheme for mechanical manipulators, Journal of Dynamic Systems, Measurement, and Control 102(2), 69-76, 1980"
    locator: the whole paper (the recursive Newton-Euler computation of the joint torques)
  - paper: doi:10.1109/TSMC.1980.4308393
    title: John M. Hollerbach, A recursive Lagrangian formulation of manipulator dynamics and a comparative study of dynamics formulation complexity, IEEE Transactions on Systems, Man, and Cybernetics 10(11), 730-736, 1980
    locator: the whole paper (the operation counts of the Lagrangian and Newton-Euler formulations)
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: Chapter 6, Section 6.6 (Newton-Euler formulation)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 7 (direct dynamics and inverse dynamics)
---

Inverse dynamics is the problem of finding the joint torques that give a robot a wanted motion: given its joint positions $q$, velocities $\dot q$ and accelerations $\ddot q$, find $\tau$. For a robot with a fixed base and no contact, the answer is the left side of the manipulator equation, $\tau = M(q)\ddot q + C(q, \dot q)\dot q + g(q)$, and it needs no linear solve. Controllers evaluate it at every control step, and planners use it to check torque limits. The [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/) solves it in $O(n)$; [forward dynamics](/forward-dynamics/) is the opposite problem.

## In plain words

You want the arm to follow a path: at this instant each joint should be at a given angle, turn at a given rate and speed up at a given rate. Which torque must each motor give? Inverse dynamics answers this. The torque has three parts: a part to speed up the links, a part to keep moving links on their curved paths, and a part to hold the links up against gravity. Because the wanted motion is known, the answer is a direct calculation, with no equations to solve.

## Definition

Input:
- A robot model: $n$ joints, each revolute or prismatic, joined into a serial chain or a tree with a fixed base; the joint axes and link frames; and the mass, center of mass and rotational inertia of each link.
- The gravity vector, $(0, 0, -9.81)$ m/s$^2$ in the space frame $\{s\}$.
- The joint positions $q$, velocities $\dot q$ and accelerations $\ddot q$, all in $\mathbb{R}^n$, and optionally known external wrenches $F_{\text{ext}}$ with their Jacobians $J(q)$.

Output: the joint torques and forces $\tau \in \mathbb{R}^n$ with

$$\tau = M(q)\ddot q + C(q, \dot q)\dot q + g(q) - J(q)^T F_{\text{ext}},$$

so that the [manipulator equation](/manipulator-equation/) holds. The output is unique and always exists.

The trajectory version takes a twice-differentiable path $q_d(t)$ and returns $\tau(t)$ for each sampled time, which is the feedforward torque of the path.

## Variants

- Floating base. A robot whose base is not bolted down has six unactuated coordinates. The six base rows of the equation must be satisfied by contact forces, not by motors, so the problem gains unknown contact wrenches and constraints: friction cones and unilateral normal forces. It can have no solution (the motion needs a pull on the ground) or many (several feet share the load). Whole-body controllers solve it as a [quadratic program](/quadratic-programming/); see [floating-base dynamics](/floating-base-dynamics/).
- Redundant actuation and closed chains. A parallel robot with more motors than degrees of freedom has many torque vectors that give the same motion. A common choice is the one with the smallest norm.
- Task-space inverse dynamics. The wanted motion is given as an end-effector acceleration. With the [operational space formulation](/operational-space-formulation/), the wrench is $\Lambda(q)\dot{\mathcal{V}} + \eta(q, \mathcal{V})$ and the torque is $J^T$ times it, plus a null-space term for redundant arms.
- Friction and motors. Joint friction and rotor inertia add known terms to $\tau$ if they are modeled.
- Regressor form. For identification and adaptive control, the output is written as $Y(q, \dot q, \ddot q)\pi$; see [linearity in the dynamic parameters](/linearity-in-dynamic-parameters/).

## Examples

Take the planar 2R arm with $L_1 = L_2 = 1$ m and point masses of 1 kg at the link ends, in a vertical plane, with $q_1$ measured from the horizontal. With $c_2 = \cos q_2$, $s_2 = \sin q_2$, $c_1 = \cos q_1$ and $c_{12} = \cos(q_1 + q_2)$:

$$\tau_1 = (3 + 2c_2)\ddot q_1 + (1 + c_2)\ddot q_2 - s_2(2\dot q_1\dot q_2 + \dot q_2^2) + 9.81(2c_1 + c_{12}),$$
$$\tau_2 = (1 + c_2)\ddot q_1 + \ddot q_2 + s_2\dot q_1^2 + 9.81\,c_{12}.$$

| $q$ (rad) | $\dot q$ (rad/s) | $\ddot q$ (rad/s$^2$) | gravity | $\tau$ (N m) |
|---|---|---|---|---|
| $(0, \pi/2)$ | $(1, 1)$ | $(0, 0)$ | no | $(-3, 1)$ |
| $(0, \pi/2)$ | $(1, 1)$ | $(0, 0)$ | yes | $(16.62, 1)$ |
| $(0, 0)$ | $(0, 0)$ | $(0, 0)$ | yes | $(29.43, 9.81)$ |
| $(0.3, 0.7)$ | $(0.5, -1.2)$ | $(2, -1)$ | yes | $(31.184, 7.991)$ |
| $(0, \pi/2)$ | $(1, 1)$ | $(2, -3)$ | no | $(0, 0)$ |

The third row can be checked by hand with the [Newton-Euler equations](/newton-euler-equations/) applied as statics: each mass weighs $9.81$ N, the masses are at horizontal distances 1 m and 2 m from joint 1 and at 1 m from joint 2, so $\tau_1 = 9.81(1 + 2) = 29.43$ N m and $\tau_2 = 9.81$ N m. The last row is the state and acceleration of the [forward dynamics](/forward-dynamics/) example: with $\tau = 0$ the arm accelerates at $(2, -3)$ rad/s$^2$, and inverse dynamics returns $\tau = 0$.

The first row shows that a constant joint rate is not free. Joint 1 needs $-3$ N m and joint 2 needs $1$ N m to keep both rates at 1 rad/s, because the outer mass moves on a curved path.

## Known algorithms

All counts are in the [real-RAM](/real-ram/) model for a serial chain or a tree of $n$ joints with one degree of freedom each.

1. Closed form. Derive $M$, $C$ and $g$ with [Euler-Lagrange manipulator dynamics](/euler-lagrange-manipulator-dynamics/) or [Kane's method](/kanes-method/) and evaluate them. $M$ alone has $n^2$ entries and the Coriolis term has $n^3$ Christoffel symbols, so this is not linear in $n$. Hollerbach (1980) compared the operation counts of the Lagrangian and Newton-Euler formulations. The closed form is best for small arms and for analysis.
2. Recursive Newton-Euler algorithm (Luh, Walker and Paul 1980; Featherstone 2008, Chapter 5; Lynch and Park, Section 8.3). A pass from the base outward computes the twist and acceleration of each link, with gravity entered as an upward acceleration of the base. The [Newton-Euler equations](/newton-euler-equations/) give the net wrench of each link. A pass inward sums the wrenches and projects them on the joint axes. Each pass costs $O(1)$ per link, so the total is $O(n)$.
3. Recursive Lagrangian. Hollerbach (1980) arranged the Lagrangian computation recursively and also reached a cost linear in $n$.

## Bounds

- Upper bound: $O(n)$ arithmetic operations for a serial chain or a tree, by the recursive Newton-Euler algorithm. No factorization is needed.
- Lower bound: $\Omega(n)$, because the output has $n$ numbers. So inverse dynamics of a serial chain or a tree is $\Theta(n)$ in the real-RAM model.
- Exact operation counts depend on the joint types and on the frame conventions. Featherstone (2008, Chapter 10) gives published counts; use those and not a count of your own.

## Reductions

- Forward dynamics to inverse dynamics. Inverse dynamics with $\ddot q = 0$ gives the bias $C\dot q + g$, and calls with $\dot q = 0$, no gravity and $\ddot q = e_j$ give column $j$ of $M$. So $n + 1$ calls and an $O(n^3)$ solve give forward dynamics (Walker and Orin 1982). The [composite-rigid-body algorithm](/composite-rigid-body-algorithm/) is a faster way to get the same columns.
- Inverse dynamics to forward dynamics. The map $\tau \mapsto \ddot q$ is affine, so $n + 1$ forward dynamics calls give $M^{-1}$ and the bias, and $\tau = M(\ddot q - b)$ follows. This reduction is never used in practice, because the direct $O(n)$ algorithm exists.
- Control to inverse dynamics. [Computed-torque control](/computed-torque-control/) evaluates inverse dynamics with the acceleration $\ddot q_d + K_d\dot e + K_pe$ at each step.

## Applications

- Feedforward and [computed-torque control](/computed-torque-control/) of robot arms.
- Checking that a planned trajectory respects the torque limits, and [time-optimal path parameterization](/time-optimal-path-parameterization/), where $\tau$ along a fixed path is affine in the path acceleration.
- Sizing motors and gears from the torques of the worst-case motions.
- [Dynamic parameter identification](/dynamic-parameter-identification/), which fits the regressor form of inverse dynamics to measured torques.
- Biomechanics, which computes the joint torques of a human from motion capture data and measured ground forces.

## References
