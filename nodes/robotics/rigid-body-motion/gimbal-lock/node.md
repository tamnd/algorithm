---
tag: CTV575
kind: concept
slug: gimbal-lock
name: Gimbal lock
aliases:
- Euler angle singularity
area: robotics/rigid-body-motion
level: intro
summary: The loss of one rotational degree of freedom when two axes of a three-angle chart or a three-ring gimbal line up, where the map to SO(3) is singular.
prereqs: [euler-angles, roll-pitch-yaw-angles]
see_also: [stuelpnagel-theorem, unit-quaternion-rotation, quaternion-kinematic-equation, kinematic-singularity, analytic-jacobian, error-state-kalman-filter, attitude-estimation, kinematic-decoupling]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Appendix B, Section B.1 (Euler angles, the family of solutions at beta = plus or minus 90 degrees in the ZYX form)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 2, Sections 2.4.1 and 2.4.2 (the singular cases of the ZYZ and RPY angles)
  - paper: doi:10.1137/1006093
    title: John Stuelpnagel, On the parametrization of the three-dimensional rotation group, SIAM Review 6(4), 422-430, 1964
    locator: Section 3 (no three-dimensional parametrization is global and nonsingular) and Section 6 (the singularity of roll, pitch and yaw)
---

Gimbal lock is the loss of one rotational degree of freedom that happens when two of the three rotation axes of a three-angle description line up.
In a mechanical gimbal, three nested rings turn about three axes, and when the middle ring turns by $90°$ the inner and the outer axes become parallel, so the platform can no longer turn about the third direction.
In [Euler angles](/euler-angles/) and [roll-pitch-yaw angles](/roll-pitch-yaw-angles/), the same line-up makes the map from the three angles to the rotation matrix singular: two angles turn about one line, only their sum or difference is fixed, and small changes of the orientation need large changes of the angles.
It is not a fault of a particular convention: by [Stuelpnagel's theorem](/stuelpnagel-theorem/) every chart of rotations by three numbers has such a point.

## In plain words

Think of a camera on three motors: one turns it left and right, one tips it up and down, and one rolls it.
Point the camera straight up.
Now the left-and-right motor and the roll motor turn the camera about the same line, so they do the same job.
One direction of turning is lost, and to turn the camera that way the motors must first move far away from this pose.
Three angles that describe an orientation behave in the same way.
Near the bad pose, a very small turn of the object can need a very large change of two angles.
A program that steps the angles, smooths them, or compares them, sees jumps there.
The fix is to store the orientation in a form with no bad pose, such as a quaternion, and to turn it into angles only for display.

## The idea

**Three axes that move with the angles.** For ZYZ Euler angles, $R = R_z(\alpha)\,R_y(\beta)\,R_z(\gamma)$.
A rate of each angle turns the body about one axis, so the [angular velocity](/angular-velocity/) in the fixed frame is

$$\omega_s = \dot\alpha\, \hat z + \dot\beta\, R_z(\alpha)\hat y + \dot\gamma\, R_z(\alpha)R_y(\beta)\hat z = \begin{pmatrix} 0 & -\sin\alpha & \cos\alpha\sin\beta \\ 0 & \cos\alpha & \sin\alpha\sin\beta \\ 1 & 0 & \cos\beta \end{pmatrix} \begin{pmatrix} \dot\alpha \\ \dot\beta \\ \dot\gamma \end{pmatrix}.$$

The three columns are the three gimbal axes.
The determinant of this matrix is $-\sin\beta$.
At $\beta = 0$ or $\beta = \pi$, the first and the third columns are both $\pm\hat z$, the matrix has rank 2, and no rates of the angles give an angular velocity along $R_z(\alpha)\hat x$.

**The roll-pitch-yaw case.** For $R = R_z(\psi)\,R_y(\theta)\,R_x(\phi)$ the axes are $\hat z$, $R_z(\psi)\hat y$ and $R_z(\psi)R_y(\theta)\hat x = (\cos\psi\cos\theta, \sin\psi\cos\theta, -\sin\theta)$, and the determinant is $-\cos\theta$.
The lock is at a pitch of $\theta = \pm 90°$, where the roll axis turns into the yaw axis.

**What it does to computations.**

- *The inverse map.* At the lock, the formulas for the angles read atan2(0, 0), and every pair of angles with the right sum or difference is a solution. Close to the lock, the solution exists but moves fast.
- *The rates.* Solving the matrix equation above for the rates divides by $\sin\beta$ (or $\cos\theta$). For a constant angular velocity the rates grow without bound as the path comes near the lock, and an integrator of the angles loses accuracy or fails.
- *Interpolation and filters.* A straight line between two angle triples is not a uniform turn, and near the lock it can swing far. A Kalman filter on the angles uses a linearization that is wrong near the lock.

**It is a property of the chart, not of the rotation.** The orientation at the lock is an ordinary rotation.
A different axis order puts the lock somewhere else, and a [unit quaternion](/unit-quaternion-rotation/), a rotation matrix or a local chart around the current estimate has no lock at that orientation.
[Stuelpnagel's theorem](/stuelpnagel-theorem/) shows that some lock is unavoidable with three numbers, so the cures all use either more numbers or a chart that moves with the body.

## Examples

- **The rates near the lock.** With roll-pitch-yaw angles, a zero roll and a body that turns about its own $z$ axis at $1$ rad/s, the yaw rate is $1/\cos\theta$. At a pitch of $89°$ it is $57.3$ rad/s, and at $89.9°$ it is $573.0$ rad/s.
- **A small turn, a large change of angles.** At a pitch of $89.9°$, with zero roll and yaw, a further turn of $0.1°$ about the fixed $x$ axis gives the angles yaw $45°$, pitch $89.859°$ and roll $45°$. Two angles jump by $45°$ for a turn of $0.1°$.
- **The lost solution.** In ZYZ Euler angles, $(0.3, 0, 0.2)$ and $(0.5, 0, 0)$ give the same matrix $R_z(0.5)$. The chart cannot tell them apart, so the inverse map must pick one.
- **A robot wrist.** A spherical wrist with joint axes $z$, $y$, $z$ realizes ZYZ Euler angles. With the middle joint at zero, the first and the last axes are collinear, the arm loses one direction of turning, and the [geometric Jacobian](/geometric-jacobian/) drops rank. This is a [kinematic singularity](/kinematic-singularity/) of the robot, not only of a chart.
- **The cure by quaternions.** The [quaternion kinematic equation](/quaternion-kinematic-equation/) $\dot q = \frac12 q\,(0, \omega_b)$ is linear in $q$ with bounded coefficients, so the attitude passes through a pitch of $90°$ with no special case.

## Where it is used

- **Attitude estimation.** [Attitude filters](/attitude-estimation/) such as the [error-state Kalman filter](/error-state-kalman-filter/) keep a quaternion or a matrix as the state and a small three-vector error around it. The error stays near zero, far from the lock of any chart, and the filter never sees the singular set.
- **Robot arms.** The [analytic Jacobian](/analytic-jacobian/) uses the rates of Euler or roll-pitch-yaw angles and inherits the lock of the chart, even at poses where the robot is not singular. The [geometric Jacobian](/geometric-jacobian/) uses the angular velocity and avoids it. A wrist designed with [kinematic decoupling](/kinematic-decoupling/) has a real gimbal lock that motion planning must avoid.
- **Trajectory generation.** Interpolation of orientations in angle space is simple but bends the path near the lock. [Spherical linear interpolation](/spherical-linear-interpolation/) of quaternions gives a uniform turn about a fixed axis.
- **User interfaces.** Angles are easy to read, so systems often store quaternions and show roll, pitch and yaw. The display jumps near the lock, but the state does not.

## References
