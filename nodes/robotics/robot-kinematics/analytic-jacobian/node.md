---
tag: S2RAY3
kind: definition
slug: analytic-jacobian
name: Analytic Jacobian
aliases:
- representation Jacobian
area: robotics/robot-kinematics
level: core
summary: The derivative of a minimal pose coordinate vector, such as position and Euler angles, with respect to the joint values.
prereqs: [geometric-jacobian, euler-angles]
see_also: [space-and-body-jacobian, roll-pitch-yaw-angles, gimbal-lock, angular-velocity, kinematic-singularity, operational-space-formulation, unit-quaternion-rotation, jacobian-linearization]
sources:
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics: Modelling, Planning and Control, Springer, 2009"
    locator: Chapter 3, Section 3.6 (the analytical Jacobian and its relation to the geometric Jacobian through the Euler angle rates) and Section 3.7 (inverse kinematics with an orientation error in Euler angles)
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: Chapter 5, Section 5.1.5 (alternative notions of the Jacobian, the analytic Jacobian with minimal coordinates)
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, 2nd edition, Wiley, 2020
    locator: Chapter 4 (the analytical Jacobian, with Euler angles)
---

The analytic Jacobian of a robot arm is the matrix of partial derivatives $J_A(q) = \partial x_e / \partial q$, where $x_e = (p_e, \phi_e)$ is the pose of the end effector written as a position $p_e$ and a set of three orientation angles $\phi_e$, for example [Euler angles](/euler-angles/).
It is an ordinary Jacobian of a map from joint values to six numbers, so the usual calculus applies.
The [geometric Jacobian](/geometric-jacobian/) gives the angular velocity $\omega_e$ in place of $\dot\phi_e$, and $\omega_e$ is not the derivative of any three angles; the two matrices differ by a $3 \times 3$ factor $T(\phi_e)$ that depends only on the angle convention.
At the points where that factor is singular, such as the [gimbal lock](/gimbal-lock/) of the angles, the analytic Jacobian does not exist even if the arm is far from a [kinematic singularity](/kinematic-singularity/).

## Definition

Let $p_e(q) \in \mathbb{R}^3$ be the position of the end effector and $R_e(q) \in SO(3)$ its orientation, both in the base frame {s}.
Fix a minimal representation of the orientation, a smooth map $\phi \mapsto R(\phi)$ from an open set of $\mathbb{R}^3$ onto a part of SO(3), and let $\phi_e(q)$ be the angles of $R_e(q)$ on a region where they are a smooth function of $q$.

**Definition.** The analytic Jacobian is the $6 \times n$ matrix

$$J_A(q) = \frac{\partial}{\partial q}\begin{pmatrix} p_e(q) \\ \phi_e(q) \end{pmatrix} = \begin{pmatrix} J_P(q) \\ J_\phi(q) \end{pmatrix}, \qquad \dot x_e = J_A(q)\,\dot q.$$

The upper block $J_P$ is the same as in the geometric Jacobian.
The lower block is tied to the angular velocity by a representation matrix $T(\phi)$: if $R(\phi(t))$ moves, then its [angular velocity](/angular-velocity/) in {s} is $\omega = T(\phi)\,\dot\phi$.
So, with the geometric Jacobian $J = (J_P, J_O)$,

$$J = \begin{pmatrix} I & 0 \\ 0 & T(\phi_e) \end{pmatrix} J_A, \qquad J_A = \begin{pmatrix} I & 0 \\ 0 & T(\phi_e)^{-1} \end{pmatrix} J \quad \text{where } \det T(\phi_e) \ne 0.$$

**The representation matrix for ZYZ angles.** With $R = R_z(\alpha) R_y(\beta) R_z(\gamma)$ (moving axes), each angle rate turns the body about its own axis at that stage, so $\omega = \dot\alpha\, z + \dot\beta\, R_z(\alpha) y + \dot\gamma\, R_z(\alpha) R_y(\beta) z$, which gives

$$T_{ZYZ}(\alpha, \beta) = \begin{pmatrix} 0 & -\sin\alpha & \cos\alpha \sin\beta \\ 0 & \cos\alpha & \sin\alpha \sin\beta \\ 1 & 0 & \cos\beta \end{pmatrix}, \qquad \det T_{ZYZ} = -\sin\beta.$$

It is singular at $\beta = 0$ and $\beta = \pi$, the same set where the ZYZ angles of a rotation are not unique.

**The representation matrix for roll, pitch and yaw.** With the [roll-pitch-yaw angles](/roll-pitch-yaw-angles/) $R = R_z(\psi) R_y(\theta) R_x(\varphi)$, where $\psi$ is the yaw, $\theta$ the pitch and $\varphi$ the roll, the same steps give, for $\dot\phi = (\dot\psi, \dot\theta, \dot\varphi)$,

$$T_{ZYX}(\psi, \theta) = \begin{pmatrix} 0 & -\sin\psi & \cos\psi\cos\theta \\ 0 & \cos\psi & \sin\psi\cos\theta \\ 1 & 0 & -\sin\theta \end{pmatrix}, \qquad \det T_{ZYX} = -\cos\theta,$$

singular at $\theta = \pm\pi/2$.
Both matrices depend on the order of the angles and on whether $\omega$ is taken in {s} or in the end effector frame; a source that uses the body angular velocity has a different $T$.

**Conversion from the twist Jacobians.** Lynch and Park write the [space Jacobian](/space-and-body-jacobian/) with the angular part first, $J_s = (J_\omega, J_v)$, where $J_v$ maps to the velocity of the body point at the origin of {s}.
Then $J_P = J_v - [p_e] J_\omega$, $J_O = J_\omega$, and

$$J_A = \begin{pmatrix} J_v - [p_e] J_\omega \\ T(\phi_e)^{-1} J_\omega \end{pmatrix}.$$

**What it is used for.** The analytic Jacobian is the right tool when a task is given as a curve $x_d(t)$ in position and angle coordinates, because then the error $x_d - x_e$ is a plain vector difference, and $\dot x_e = J_A \dot q$ holds exactly.
Siciliano et al. use it in the closed-loop inverse kinematics with an orientation error in Euler angles.
In the [operational space formulation](/operational-space-formulation/), the choice of $J$ or $J_A$ fixes which force and moment vector the controller produces.

## Examples and non-examples

**The planar 2R arm.** For a planar arm, take $x_e = (x, y, \phi)$ with the angle $\phi = q_1 + q_2$ of the last link.
At the check configuration $q = (0, \pi/2)$ with $L_1 = L_2 = 1$ m,

$$J_A = \begin{pmatrix} -1 & -1 \\ 1 & 0 \\ 1 & 1 \end{pmatrix}.$$

Here $\omega_z = \dot\phi$, so $T = 1$ and the analytic and geometric Jacobians agree.
In the plane the orientation has one angle, and angle rates and angular velocity are the same thing; the difference starts in three dimensions.

**A ZYZ wrist.** Take three revolute joints whose axes are $z$, then the rotated $y$, then the rotated $z$, so that the wrist orientation is $R_z(q_1) R_y(q_2) R_z(q_3)$, and use ZYZ angles.
Then $\phi_e = q$, so $J_\phi = I$ at every $q$ with $\sin q_2 \ne 0$, while $J_O = T_{ZYZ}(q_1, q_2)$.
At $q_2 = 0$ the first and the third joint axes are the same line, $J_O$ has rank 2, and no joint rate gives an angular velocity about the axis $R_z(q_1) x$ (the $x$ axis when $q_1 = 0$).
This is a true [kinematic singularity](/kinematic-singularity/) of the wrist, but the analytic Jacobian, extended by continuity, is still $I$.
So the rank of $J_A$ is not a test for kinematic singularities.

**A representation singularity.** At $\alpha = 0$ and $\beta = 0.01$ rad, solving $T_{ZYZ}\dot\phi = (1, 0, 0)$ rad/s gives $\dot\gamma = 1/\sin\beta \approx 100.0$ rad/s and $\dot\alpha = -\cos\beta\,\dot\gamma \approx -100.0$ rad/s.
A slow, smooth turn of the end effector about $x$ needs angle rates of 100 rad/s, and at $\beta = 0$ it needs infinite rates.
An arm that tracks a task given in ZYZ angles near $\beta = 0$ shows this blow up, even when $J$ itself has full rank and a good [manipulability](/yoshikawa-manipulability-measure/).

**Non-example: the geometric Jacobian.** Its lower block maps to $\omega_e$, which is not $\dot\phi_e$ for any angles.

**Non-example: the space and body Jacobians.** They map to twists in {s} or in {b}; the analytic Jacobian maps to the derivative of six coordinates.

**Variant: other coordinates.** The same construction works with exponential coordinates of rotation or with a [unit quaternion](/unit-quaternion-rotation/).
A quaternion has no singular point but has four numbers and the constraint $|q| = 1$, so its representation matrix is $4 \times 3$.

## Related definitions

- [Geometric Jacobian](/geometric-jacobian/): $J = \operatorname{diag}(I, T(\phi_e))\, J_A$.
- [Space and body Jacobians](/space-and-body-jacobian/): the twist form, angular part first.
- [Euler angles](/euler-angles/) and [roll-pitch-yaw angles](/roll-pitch-yaw-angles/): the two angle sets used above.
- [Gimbal lock](/gimbal-lock/): the singular set of the angles, where $T(\phi)$ loses rank.
- [Kinematic singularity](/kinematic-singularity/): a loss of rank of $J$; it is a property of the arm, not of the angle set.
- [Jacobian linearization](/jacobian-linearization/): in control, the Jacobian of any smooth map at a point.

## References
