---
tag: N60E0J
kind: definition
slug: euler-angles
name: Euler angles
aliases:
- ZYZ Euler angles
- proper Euler angles
area: robotics/rigid-body-motion
level: intro
summary: "Three angles (alpha, beta, gamma) with R = Rz(alpha) Ry(beta) Rz(gamma): turn about the body z, then the new y, then the new z. Singular at beta = 0 and pi."
prereqs: [special-orthogonal-group]
see_also: [roll-pitch-yaw-angles, gimbal-lock, stuelpnagel-theorem, unit-quaternion-rotation, axis-angle-representation, analytic-jacobian, kinematic-decoupling, euler-rotation-theorem]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Appendix B, Section B.1 (Euler angles, the ZYZ form in equation B.6) and Section B.1.2 (other Euler angle representations)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 2, Section 2.4 (Euler angles) and Section 2.4.1 (ZYZ angles)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 2 (rotational motion in R^3, other representations)
---

Euler angles describe an orientation by three angles of rotation about coordinate axes, applied one after the other.
In the ZYZ form used in robotics, the angles $(\alpha, \beta, \gamma)$ give the rotation matrix $R = R_z(\alpha)\,R_y(\beta)\,R_z(\gamma)$: turn the body by $\alpha$ about its $z$ axis, then by $\beta$ about its new $y$ axis, then by $\gamma$ about its new $z$ axis.
Every rotation has such angles, and they are unique when $0 < \beta < \pi$.
At $\beta = 0$ and $\beta = \pi$ the first and the last axes line up, only $\alpha + \gamma$ or $\alpha - \gamma$ is fixed, and the chart is singular; this is [gimbal lock](/gimbal-lock/).

Notation on this page: rotations are active, and $R_x$, $R_y$, $R_z$ are the rotations about the fixed axes of the base frame,

$$R_z(\alpha) = \begin{pmatrix} \cos\alpha & -\sin\alpha & 0 \\ \sin\alpha & \cos\alpha & 0 \\ 0 & 0 & 1 \end{pmatrix}, \qquad R_y(\beta) = \begin{pmatrix} \cos\beta & 0 & \sin\beta \\ 0 & 1 & 0 \\ -\sin\beta & 0 & \cos\beta \end{pmatrix}.$$

## Definition

**Definition.** The ZYZ Euler angles of a rotation $R$ in the [special orthogonal group](/special-orthogonal-group/) SO(3) are three angles $(\alpha, \beta, \gamma)$ with

$$R = R_z(\alpha)\,R_y(\beta)\,R_z(\gamma) = \begin{pmatrix} c_\alpha c_\beta c_\gamma - s_\alpha s_\gamma & -c_\alpha c_\beta s_\gamma - s_\alpha c_\gamma & c_\alpha s_\beta \\ s_\alpha c_\beta c_\gamma + c_\alpha s_\gamma & -s_\alpha c_\beta s_\gamma + c_\alpha c_\gamma & s_\alpha s_\beta \\ -s_\beta c_\gamma & s_\beta s_\gamma & c_\beta \end{pmatrix},$$

where $c_\alpha = \cos\alpha$, $s_\alpha = \sin\alpha$, and so on.
The usual ranges are $\alpha, \gamma \in (-\pi, \pi]$ and $\beta \in [0, \pi]$.

**Two readings of the same product.**

- *Moving axes.* $R_z(\alpha)$ turns the frame about its $z$ axis. The next factor, multiplied on the right, turns about the $y$ axis of the frame that is already turned, and the last factor about the newest $z$ axis. So the angles are applied in the order $\alpha, \beta, \gamma$ about the body axes $z, y', z''$.
- *Fixed axes.* Read from right to left, the product turns a vector by $\gamma$ about the fixed $z$ axis, then by $\beta$ about the fixed $y$ axis, then by $\alpha$ about the fixed $z$ axis.

Both readings give the same matrix, so a sequence about moving axes always equals the reverse sequence about fixed axes.
A statement of Euler angles is complete only when it gives the axis order, says whether the axes are fixed or moving, and says whether the matrix is active or passive.

**Inverse.** Given $R = (r_{ij})$, the angles with $\beta \in [0, \pi]$ are

$$\beta = \operatorname{atan2}\Big(\sqrt{r_{13}^2 + r_{23}^2},\; r_{33}\Big), \qquad \alpha = \operatorname{atan2}(r_{23}, r_{13}), \qquad \gamma = \operatorname{atan2}(r_{32}, -r_{31}),$$

and these are the only angles in the ranges above when $0 < \beta < \pi$.
The second solution $(\alpha + \pi, -\beta, \gamma + \pi)$, with $\beta$ negative, gives the same matrix and is excluded by the range of $\beta$.

**The singular set.** If $\beta = 0$, then $R = R_z(\alpha + \gamma)$, and every pair with the same sum gives the same $R$.
If $\beta = \pi$, then $R_y(\pi) R_z(\gamma) = R_z(-\gamma) R_y(\pi)$, so $R = R_z(\alpha - \gamma) R_y(\pi)$, and only the difference is fixed.
At these orientations the map $(\alpha, \beta, \gamma) \mapsto R$ has a derivative of rank 2, not 3, and the inverse formulas above fail because $r_{13} = r_{23} = 0$.
Code must test for this case and choose one angle, often $\gamma = 0$.

**Other Euler angles.** Any three axes with no two neighbours equal give a chart.
The six proper Euler sequences repeat the first axis (ZYZ, ZXZ, XYX, XZX, YXY, YZY); the six Tait-Bryan sequences use three different axes (such as ZYX, the [roll-pitch-yaw angles](/roll-pitch-yaw-angles/)).
With fixed or moving axes, this gives 24 conventions.
Every one of them is singular somewhere, as [Stuelpnagel's theorem](/stuelpnagel-theorem/) shows for every three-parameter chart.

## Examples and non-examples

- **A full example.** $(\alpha, \beta, \gamma) = (30°, 45°, 60°)$ gives
  $$R = \begin{pmatrix} -0.12683 & -0.78033 & 0.61237 \\ 0.92678 & 0.12683 & 0.35355 \\ -0.35355 & 0.61237 & 0.70711 \end{pmatrix}.$$
  The inverse formulas give $\beta = \operatorname{atan2}(\sqrt{0.61237^2 + 0.35355^2}, 0.70711) = \operatorname{atan2}(0.70711, 0.70711) = 45°$, $\alpha = \operatorname{atan2}(0.35355, 0.61237) = 30°$ and $\gamma = \operatorname{atan2}(0.61237, 0.35355) = 60°$.
- **A cyclic permutation.** The rotation $(x, y, z) \mapsto (z, x, y)$ has the matrix with rows $(0, 0, 1)$, $(1, 0, 0)$, $(0, 1, 0)$. Here $r_{13} = 1$, $r_{23} = 0$, $r_{33} = 0$, $r_{31} = 0$ and $r_{32} = 1$, so $(\alpha, \beta, \gamma) = (0, 90°, 90°)$, and indeed $R_y(90°)\,R_z(90°)$ is this matrix.
- **The same matrix in another convention.** The rotation of the first example has the ZYX angles $(97.792°, 20.705°, 40.893°)$. Angle triples have no meaning without their convention.
- **Non-example: unique angles at $\beta = 0$.** $(0.3, 0, 0.2)$ and $(0.5, 0, 0)$ both give $R_z(0.5)$. No choice of the range removes this, because the problem is the line-up of the axes, not the period of the angles.
- **Non-example: adding angles.** The ZYZ angles of $R_1 R_2$ are not the sums of the angles of $R_1$ and $R_2$. Compose the matrices or [quaternions](/unit-quaternion-rotation/) and convert after.
- **Non-example: the rates as an angular velocity.** $(\dot\alpha, \dot\beta, \dot\gamma)$ is not the [angular velocity](/angular-velocity/). The two are related by a $3 \times 3$ matrix that depends on $\beta$ and is singular where $\sin\beta = 0$; this matrix is part of the [analytic Jacobian](/analytic-jacobian/).

## Related definitions

- **[Roll-pitch-yaw angles](/roll-pitch-yaw-angles/).** The Tait-Bryan ZYX sequence, $R = R_z(\text{yaw}) R_y(\text{pitch}) R_x(\text{roll})$, singular at a pitch of $\pm 90°$.
- **[Gimbal lock](/gimbal-lock/).** The loss of one degree of freedom at the singular set, in a mechanical gimbal and in the chart.
- **[Axis-angle representation](/axis-angle-representation/), [unit quaternions](/unit-quaternion-rotation/) and [Cayley parameters](/cayley-rotation-parameters/).** Other representations of SO(3). Quaternions have no singular orientation, at the price of a fourth number.
- **[Kinematic decoupling](/kinematic-decoupling/).** A wrist with three revolute joints whose axes meet in one point realizes a set of Euler angles, so its inverse kinematics is the inverse formula above, and its singularity is the line-up at $\beta = 0$.

## References
