---
tag: R31868
kind: definition
slug: rigid-body-twist
name: Twist
aliases:
- spatial velocity
- velocity twist
area: robotics/rigid-body-motion
level: core
summary: "The 6-vector V = (omega, v) of angular and linear velocity that gives the velocity of every point of a rigid body; an element of the Lie algebra se(3)."
prereqs: [special-euclidean-group, angular-velocity]
see_also: [se3-exponential-map, adjoint-map-se3, wrench, screw-motion, space-and-body-jacobian, spatial-vector-algebra, kinematic-fixture-analysis, infinitesimal-rigidity]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.3.2 (twists, the body and the spatial twist, the screw interpretation of a twist)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Sections 3.2 and 4 (twists, and the velocity of a rigid body); the book writes a twist with the linear part first, as (v, omega)
  - paper: arxiv:1812.01537
    title: Joan Sola, Jeremie Deray and Dinesh Atchuthan, A micro Lie theory for state estimation in robotics, 2018
    locator: the Lie algebra of the rigid motion group and its vector form
---

A twist is a 6-vector $\mathcal{V} = (\omega, v)$ that gives the velocity of a rigid body: $\omega$ is the [angular velocity](/angular-velocity/), and $v$ is a linear velocity.
Every point $x$ of the body has the velocity $\omega \times x + v$, so the six numbers fix the velocity of all points at once.
The twist can be written in the fixed frame, the spatial twist, or in the body frame, the body twist, and the [adjoint map](/adjoint-map-se3/) converts one into the other.
Geometrically, every twist is a rotation about a line plus a sliding along the same line, the instantaneous screw.
The twist is the velocity of a curve in the [special Euclidean group](/special-euclidean-group/) SE(3); as the matrix $[\mathcal{V}]$ it is an element of the Lie algebra $\mathfrak{se}(3)$.

## Definition

We use the conventions of Lynch and Park, with the angular part first.
Let $T(t) = \begin{pmatrix} R(t) & p(t) \\ 0 & 1 \end{pmatrix}$ be a differentiable curve in SE(3), the pose of a body frame $\{b\}$ in a fixed frame $\{s\}$.
Both $T^{-1}\dot T$ and $\dot TT^{-1}$ have the form

$$[\mathcal{V}] = \begin{pmatrix} [\omega] & v \\ 0 & 0 \end{pmatrix}, \qquad \mathcal{V} = (\omega, v) \in \mathbb{R}^6,$$

where $[\omega]$ is the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) of $\omega$.

- The **body twist** $\mathcal{V}_b = (\omega_b, v_b)$ has $[\mathcal{V}_b] = T^{-1}\dot T$. Here $\omega_b$ is the angular velocity in $\{b\}$, and $v_b = R^{\mathsf T}\dot p$ is the velocity of the origin of $\{b\}$, written in $\{b\}$.
- The **spatial twist** $\mathcal{V}_s = (\omega_s, v_s)$ has $[\mathcal{V}_s] = \dot TT^{-1}$. Here $\omega_s = R\omega_b$, and $v_s = \dot p - \omega_s \times p$. This $v_s$ is the velocity of the point of the body, imagined as extending to infinity, that is at the origin of $\{s\}$ at this moment.

The two twists are related by $\mathcal{V}_s = \mathrm{Ad}_T\mathcal{V}_b$, where $\mathrm{Ad}_T$ is the [adjoint map](/adjoint-map-se3/).
A point of the body with the coordinates $x_s$ in $\{s\}$ moves with the velocity $\dot x_s = \omega_s \times x_s + v_s$.

Screw axes.
If $\omega \ne 0$, then $\mathcal{V} = S\dot\theta$ with $\dot\theta = |\omega|$ and the screw axis $S = \mathcal{V}/|\omega|$.
The line of the axis passes through the point $q = \omega \times v / |\omega|^2$ in the direction of $\omega$, and the pitch is $h = \omega \cdot v / |\omega|^2$.
Conversely, the screw axis through $q$ with unit direction $\hat s$ and pitch $h$ is $S = (\hat s, -\hat s \times q + h\hat s)$.
If $\omega = 0$, then $\mathcal{V} = S\dot\theta$ with $\dot\theta = |v|$ and $S = (0, v/|v|)$: a pure translation, with infinite pitch.

Power.
A [wrench](/wrench/) $\mathcal{F} = (m, f)$, a moment and a force, written in the same frame as the twist, delivers the power $\mathcal{F} \cdot \mathcal{V} = m \cdot \omega + f \cdot v$.
This number does not depend on the frame.

## Examples and non-examples

- A wheel turns at 2 rad/s about the vertical axle through $q = (0, 1, 0)$. Its spatial twist is $\mathcal{V}_s = (0, 0, 2, 2, 0, 0)$, because $v_s = -\omega \times q = -(0, 0, 2) \times (0, 1, 0) = (2, 0, 0)$. The point of the wheel at the origin of $\{s\}$ is 1 m from the axle and moves at 2 m/s in the $x$ direction. The formulas above give back $q = \omega \times v / |\omega|^2 = (0, 4, 0)/4 = (0, 1, 0)$ and $h = 0$.
- For the same wheel, take a body frame whose origin is at the origin of $\{s\}$ at time 0. After a quarter turn, $T = (R_z(\pi/2), (1, 1, 0))$, and the body twist $\mathcal{V}_b = \mathrm{Ad}_{T^{-1}}\mathcal{V}_s$ is again $(0, 0, 2, 2, 0, 0)$: the origin of $\{b\}$ is still 1 m from the axle and moves at 2 m/s along its own $x$ axis.
- A nut that turns at 1 rad/s on a bolt along the $z$ axis, and that advances 0.002 m per radian, has the twist $(0, 0, 1, 0, 0, 0.002)$ and the pitch $h = 0.002$ m/rad.
- A prismatic joint that slides at 0.5 m/s along $x$ has the twist $(0, 0, 0, 0.5, 0, 0)$.
- Non-example: the 6-vector $(\omega_s, \dot p)$ is not a twist in either frame, because $\dot p$ is the velocity of the body origin, while the spatial twist needs the velocity of the body point at the fixed origin. Mixing the two is a common error.
- Non-example: the time derivative of six pose coordinates, such as the position and three [Euler angles](/euler-angles/), is not a twist. It differs from the twist by a matrix that depends on the angles.

## Related definitions

- The [exponential map of SE(3)](/se3-exponential-map/) gives the motion $e^{[S]\theta}$ of a body that follows the screw axis $S$, and the [screw motion](/screw-motion/) is its geometry.
- The [adjoint map](/adjoint-map-se3/) changes the frame of a twist.
- The [wrench](/wrench/) is the dual of the twist.
- The [space and body Jacobians](/space-and-body-jacobian/) map joint rates of an arm to the spatial and the body twist of its end.
- [Spatial vector algebra](/spatial-vector-algebra/) uses the same 6-vectors, under the name spatial motion vectors, for the dynamics of chains of bodies.
- In [kinematic fixture analysis](/kinematic-fixture-analysis/), the locators of a fixture fix the place of a part when no nonzero twist keeps all the contacts to first order. In rigidity theory, the [infinitesimal motions](/infinitesimal-rigidity/) of a rigid body are the twists.
- Murray, Li and Sastry write the same twist as $(v, \omega)$, with the linear part first.

## References
