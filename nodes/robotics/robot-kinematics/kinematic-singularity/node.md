---
tag: 0M3W6Q
kind: definition
slug: kinematic-singularity
name: Kinematic singularity
aliases:
- singular configuration
area: robotics/robot-kinematics
level: core
summary: A configuration where the Jacobian loses rank, so the end effector cannot move in some direction however fast the joints turn.
prereqs: [geometric-jacobian]
see_also: [space-and-body-jacobian, manipulability-ellipsoid, yoshikawa-manipulability-measure, damped-least-squares-inverse-kinematics, robot-workspace, parallel-manipulator, jacobian-statics-duality, condition-number]
sources:
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: Chapter 5, Section 5.3 (singularity analysis, the rank of the Jacobian and the geometric cases of singular open chains)
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics: Modelling, Planning and Control, Springer, 2009"
    locator: Chapter 3, Section 3.3 (kinematic singularities, boundary and internal singularities, the decoupling into arm and wrist singularities)
  - paper: doi:10.1109/70.56660
    title: Clément Gosselin and Jorge Angeles, Singularity analysis of closed-loop kinematic chains, IEEE Transactions on Robotics and Automation 6(3), 281-290, 1990
    locator: the whole paper (the three types of singularities of closed chains)
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, 2nd edition, Wiley, 2020
    locator: Chapter 4 (singularities, with the decoupling of arm and wrist singularities)
---

A kinematic singularity of a robot arm is a configuration $q$ where the Jacobian $J(q)$, the matrix that maps joint velocities to the velocity of the end effector, has a lower rank than it has at most configurations.
At such a point there is a direction in which the end effector cannot move, whatever the joint velocities are, and near such a point some small end effector velocities need very large joint velocities.
The same directions have a dual meaning for forces: some loads at the end effector need no joint torque at all.
A singularity is a property of the arm, the same for the [geometric Jacobian](/geometric-jacobian/) and the [space and body Jacobians](/space-and-body-jacobian/); a singular point of an angle set, such as [gimbal lock](/gimbal-lock/), is a different thing.

## Definition

Let an arm have $n$ joints and a task space of dimension $m$ (6 for a full pose, 3 for a position, 2 or 3 in the plane), and let $J(q)$ be its $m \times n$ Jacobian.
Let $r = \max_q \operatorname{rank} J(q)$ be the generic rank; for a well designed arm, $r = \min(m, n)$.

**Definition.** A configuration $q$ is a kinematic singularity if $\operatorname{rank} J(q) < r$.
The number $r - \operatorname{rank} J(q)$ is the degree, or corank, of the singularity.

The space Jacobian $J_s$, the body Jacobian $J_b$ and the geometric Jacobian differ by invertible $6 \times 6$ factors, so they have the same rank at every $q$ and the same singular configurations.
For a square $J$ ($m = n$), $q$ is singular if and only if $\det J(q) = 0$.
For $m < n$, $q$ is singular if and only if $\det(J J^{\mathsf T}) = 0$, which is the square of the [Yoshikawa measure](/yoshikawa-manipulability-measure/).

**What goes wrong.** Let $J = U \Sigma V^{\mathsf T}$ be the [singular value decomposition](/singular-value-decomposition/), with the singular values $\sigma_1 \ge \dots \ge \sigma_m \ge 0$ and the left singular vectors $u_1, \dots, u_m$.

- At a singularity, $\sigma_m = 0$, and no $\dot q$ gives an end effector velocity with a component along $u_m$: the range of $J$ is a proper subspace.
- Near a singularity, $\sigma_m$ is small, and the smallest $\dot q$ that gives the velocity $u_m$ has the norm $1/\sigma_m$. A controller that inverts $J$ asks for huge joint rates; the [condition number](/condition-number/) $\sigma_1/\sigma_m$ of $J$ is large.
- By the [statics duality](/jacobian-statics-duality/), $\tau = J^{\mathsf T}\mathcal F$, a wrench along $u_m$ needs no joint torque at the singularity: the structure carries it.
- For an arm with $m = n$, two or more inverse kinematic solutions usually merge at a singularity.

**Kinds.** Siciliano et al. separate two kinds.
A boundary singularity occurs when the end effector is on the boundary of the [workspace](/robot-workspace/), as when the arm is stretched out or folded back; they are easy to avoid by keeping the task inside the workspace.
An internal singularity occurs inside the workspace, usually when two or more joint axes line up, and a path planned in the task space can cross one.
For a 6-joint arm with a spherical wrist, $J$ has a block triangular form in a suitable frame, and $\det J = \det J_{11} \det J_{22}$, so the singularities split into arm singularities ($\det J_{11} = 0$) and wrist singularities ($\det J_{22} = 0$).

**Geometric cases.** Lynch and Park list configurations of revolute axes that always make $J$ lose rank, among them: two collinear axes, three coplanar parallel axes, and four axes through a common point.
Each case gives columns of $J_s$ that are linearly dependent for a geometric reason.

**Closed chains.** For a [parallel manipulator](/parallel-manipulator/) with actuated joints $q$ and output pose $x$, the loop closure gives $A(x, q)\,\dot x + B(x, q)\,\dot q = 0$.
Gosselin and Angeles (1990) define three types: when $B$ is singular, some input motions give no output motion, and the output loses a direction (the type that also occurs in serial arms); when $A$ is singular, the output can move while all actuators are locked, and some wrenches cannot be resisted; and when both are singular, both happen, which needs a special geometry.
This page uses the letters $A$ and $B$ only for the description; the paper writes the two matrices in its own notation.

## Examples and non-examples

**The planar 2R arm.** With link lengths $L_1$ and $L_2$, the position Jacobian has $\det J = L_1 L_2 \sin q_2$.
At the check configuration $q = (0, \pi/2)$ with $L_1 = L_2 = 1$ m, $\det J = 1$, which is the largest value: the arm is as far from singular as it can be.
At $q_2 = 0$ the arm is stretched, the tip is on the outer boundary circle of radius $L_1 + L_2$, and at $q = (0, 0)$, $J = \begin{pmatrix} 0 & 0 \\ 2 & 1 \end{pmatrix}$, whose range is the $y$ axis: the tip cannot move along the arm.
At $q_2 = \pi$ the arm is folded, and the tip is on the inner boundary circle of radius $|L_1 - L_2|$, which is the single point at the base when $L_1 = L_2$.
Both are boundary singularities.

**Close to the singularity.** At $q = (0, 0.01)$, a tip velocity of 0.1 m/s along the arm toward the base, $\dot x = (-0.1, 0)$, needs $\dot q = J^{-1}\dot x \approx (-10.0, 20.0)$ rad/s, since $\det J = \sin 0.01 \approx 0.01$.
A slow, ordinary motion of the tip needs the elbow to turn at 20 rad/s.

**A wrist.** In a spherical wrist with three revolute axes in the ZYZ pattern, the first and the third axes become collinear when the middle angle is 0.
The rotation about the common axis can be done by either joint, and no joint rate gives a rotation about the axis normal to both remaining axes.
This is an internal singularity, so a straight line path in the task space can pass through it.

**A shoulder singularity.** In an anthropomorphic arm, when the wrist center lies on the axis of the first joint, turning the first joint does not move the wrist center, and the arm Jacobian loses rank inside the workspace.

**Non-example: a singular point of the angles.** The ZYZ angles of the end effector orientation are not unique at a middle angle of 0, whatever the arm.
This makes the [analytic Jacobian](/analytic-jacobian/) blow up, but the arm itself may be far from singular there.

**Non-example: several inverse kinematic solutions.** A 6R arm can reach a pose in up to 16 ways (see [inverse kinematics](/inverse-kinematics/)); this alone does not make any of them singular.

**Non-example: self-motion of a redundant arm.** A 7-joint arm doing a 6-dimensional task always has a null space of $J$ of dimension at least 1; that is [kinematic redundancy](/kinematic-redundancy/), not a singularity.
The arm is singular only when the rank of its $6 \times 7$ Jacobian drops below 6.

**Non-example: a joint limit.** A joint that is at its limit cannot move in one direction, but $J$ keeps its rank; the limit is a constraint on $q$, not a loss of rank.

## Related definitions

- [Manipulability ellipsoid](/manipulability-ellipsoid/): the image of the unit ball of joint velocities, which collapses to a lower dimension at a singularity.
- [Yoshikawa manipulability measure](/yoshikawa-manipulability-measure/): $\sqrt{\det(J J^{\mathsf T})}$, zero exactly at the singularities. How small a value counts as "near singular" is a rule of thumb, not a theorem.
- [Damped least squares inverse kinematics](/damped-least-squares-inverse-kinematics/): a way to keep the joint rates bounded near singularities, at the price of a tracking error.
- [Jacobian statics duality](/jacobian-statics-duality/): the dual statement for wrenches and torques.
- [Robot workspace](/robot-workspace/): boundary singularities lie on its boundary.
- [Parallel manipulator](/parallel-manipulator/): the closed chains that have the three types of singularities.

## References
