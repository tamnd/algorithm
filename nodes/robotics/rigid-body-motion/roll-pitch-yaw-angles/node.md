---
tag: SBDNF0
kind: definition
slug: roll-pitch-yaw-angles
name: Roll-pitch-yaw angles
aliases:
- Tait-Bryan angles
- RPY angles
- yaw-pitch-roll angles
area: robotics/rigid-body-motion
level: intro
summary: Roll, pitch and yaw are turns about the fixed x, then y, then z axes, so R = Rz(yaw) Ry(pitch) Rx(roll). The chart is singular at a pitch of plus or minus 90 degrees.
prereqs: [special-orthogonal-group, euler-angles]
see_also: [euler-angles, gimbal-lock, unit-quaternion-rotation, stuelpnagel-theorem, attitude-estimation, analytic-jacobian, angular-velocity, dead-reckoning]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Appendix B, Section B.1 (the ZYX Euler angles, equation B.2, and the algorithm of Section B.1.1) and Section B.2 (roll-pitch-yaw angles, equation B.8)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 2, Section 2.4.2 (RPY angles)
  - paper: doi:10.1137/1006093
    title: John Stuelpnagel, On the parametrization of the three-dimensional rotation group, SIAM Review 6(4), 422-430, 1964
    locator: Section 6 (three-dimensional parametrizations, the singularity of roll, pitch and yaw at plus or minus 90 degrees)
---

Roll-pitch-yaw angles describe an orientation by three turns about three different axes.
In the convention used here, the body turns by the roll $\phi$ about the fixed $x$ axis, then by the pitch $\theta$ about the fixed $y$ axis, then by the yaw $\psi$ about the fixed $z$ axis, so the rotation matrix is $R = R_z(\psi)\,R_y(\theta)\,R_x(\phi)$.
The same matrix comes from turns about the moving axes in the reverse order: yaw about the body $z$ axis, then pitch about the new $y$ axis, then roll about the newest $x$ axis.
The angles are unique for a pitch strictly between $-90°$ and $90°$, and the chart is singular at a pitch of $\pm 90°$, where roll and yaw turn about the same line.

Notation on this page: rotations are active, and $R_x$, $R_y$, $R_z$ are the rotations about the fixed axes of the base frame, as on the page on [Euler angles](/euler-angles/).

## Definition

**Definition.** The roll-pitch-yaw angles of a rotation $R$ in the [special orthogonal group](/special-orthogonal-group/) SO(3) are three angles $(\phi, \theta, \psi)$ with

$$R = R_z(\psi)\,R_y(\theta)\,R_x(\phi) = \begin{pmatrix} c_\psi c_\theta & c_\psi s_\theta s_\phi - s_\psi c_\phi & c_\psi s_\theta c_\phi + s_\psi s_\phi \\ s_\psi c_\theta & s_\psi s_\theta s_\phi + c_\psi c_\phi & s_\psi s_\theta c_\phi - c_\psi s_\phi \\ -s_\theta & c_\theta s_\phi & c_\theta c_\phi \end{pmatrix},$$

where $c_\psi = \cos\psi$, $s_\psi = \sin\psi$, and so on.
The usual ranges are $\phi, \psi \in (-\pi, \pi]$ and $\theta \in [-\pi/2, \pi/2]$.

**Fixed and moving axes.** Read from right to left, the product turns a vector about the fixed axes $x$, $y$, $z$ in this order.
Read from left to right, it turns the frame about its own axes $z$, $y'$, $x''$ in this order, which is the ZYX Euler sequence.
So "roll-pitch-yaw about fixed $x, y, z$" and "ZYX Euler angles about moving $z, y', x''$" are one chart with two names.
It is one of the six Tait-Bryan sequences, which use three different axes.

**Inverse.** Given $R = (r_{ij})$ with $r_{31} \ne \pm 1$, the angles with $\theta \in (-\pi/2, \pi/2)$ are

$$\theta = \operatorname{atan2}\Big(-r_{31},\; \sqrt{r_{11}^2 + r_{21}^2}\Big), \qquad \psi = \operatorname{atan2}(r_{21}, r_{11}), \qquad \phi = \operatorname{atan2}(r_{32}, r_{33}),$$

and they are the only angles in the ranges above.
The square root is $\cos\theta > 0$, and the formulas divide it out of both arguments of each atan2.

**The singular set.** At $\theta = 90°$, $R_y(90°)\,R_x(\phi) = R_z(-\phi)\,R_y(90°)$, so $R = R_z(\psi - \phi)\,R_y(90°)$, and only $\psi - \phi$ is fixed.
At $\theta = -90°$, $R = R_z(\psi + \phi)\,R_y(-90°)$, and only $\psi + \phi$ is fixed.
There the first column of $R$ is $(0, 0, \mp 1)$, the formulas for $\psi$ and $\phi$ read atan2(0, 0), and the derivative of the chart has rank 2.
Code must test $|r_{31}|$ against a tolerance and choose one angle, often $\phi = 0$.
This is the [gimbal lock](/gimbal-lock/) of the chart.

**Vehicles.** For aircraft, ships and ground robots, the body $x$ axis points forward, so roll is the bank about the forward axis, pitch is the nose up or down, and yaw is the heading.
Many aerospace texts use a body $z$ axis that points down and write the passive matrix from the world frame to the body frame, which is $R^{\mathsf T}$.
The angles are the same numbers, but the matrix is transposed and the signs in formulas for rates change.

## Examples and non-examples

- **A full example.** Roll $10°$, pitch $20°$ and yaw $30°$ give
  $$R = \begin{pmatrix} 0.81380 & -0.44097 & 0.37852 \\ 0.46985 & 0.88256 & 0.01803 \\ -0.34202 & 0.16318 & 0.92542 \end{pmatrix}.$$
  The inverse formulas give $\theta = \operatorname{atan2}(0.34202, 0.93969) = 20°$, $\psi = \operatorname{atan2}(0.46985, 0.81380) = 30°$ and $\phi = \operatorname{atan2}(0.16318, 0.92542) = 10°$. The [unit quaternion](/unit-quaternion-rotation/) of the same rotation is the product $q_z(30°)\,q_y(20°)\,q_x(10°) = (0.95155, 0.03813, 0.18931, 0.23930)$.
- **Close to the singular set.** Take the pitch $89.9°$ with zero roll and yaw, and turn it by a further $0.1°$ about the fixed $x$ axis. The new angles are a yaw of $45°$, a pitch of $89.859°$ and a roll of $45°$. A change of $0.1°$ in the orientation moved two angles by $45°$. A filter or a controller that works on the angles sees this as a jump.
- **The singular set.** $(\phi, \theta, \psi) = (0.2, 90°, 0.5)$ and $(0, 90°, 0.3)$ give the same matrix, because the difference $\psi - \phi$ is $0.3$ in both.
- **Non-example: the order x, then y, then z about moving axes.** $R_x(\phi)\,R_y(\theta)\,R_z(\psi)$ is a different chart, with different angles for the same orientation. The phrase "x then y then z" is not complete until it says whether the axes are fixed or moving.
- **Non-example: the rates as body rates.** $(\dot\phi, \dot\theta, \dot\psi)$ is not the [angular velocity](/angular-velocity/) of the body. The body rates $(p, q, r)$ give $\dot\phi = p + (q\sin\phi + r\cos\phi)\tan\theta$, which grows without bound near the singular set. Integrating these rates in [dead reckoning](/dead-reckoning/) fails there; integrate a quaternion with the [quaternion kinematic equation](/quaternion-kinematic-equation/).

## Related definitions

- **[Euler angles](/euler-angles/).** The family of three-angle charts, with ZYZ as the proper Euler sequence of robot wrists.
- **[Gimbal lock](/gimbal-lock/).** The singular set at a pitch of $\pm 90°$, in the chart and in a mechanical gimbal.
- **[Stuelpnagel's theorem](/stuelpnagel-theorem/).** No three-parameter chart of SO(3) is free of singular points, so a change of the axis order only moves the singular set.
- **[Analytic Jacobian](/analytic-jacobian/).** The velocity Jacobian written with the rates of the angles, singular at the gimbal lock of the chart even where the robot itself is not singular.
- **[Attitude estimation](/attitude-estimation/).** Filters keep the attitude as a quaternion or a matrix and report roll, pitch and yaw only for display.

## References
