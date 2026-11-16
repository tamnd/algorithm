---
tag: 3V43P2
kind: definition
slug: angular-velocity
name: Angular velocity
aliases:
- spatial angular velocity
- body angular velocity
area: robotics/rigid-body-motion
level: intro
summary: "The vector omega of a rotating frame R(t), with dR/dt = [omega_s] R in the fixed frame or dR/dt = R [omega_b] in the body frame, and omega_s = R omega_b."
prereqs: [special-orthogonal-group, skew-symmetric-matrix-of-a-vector]
see_also: [rigid-body-twist, quaternion-kinematic-equation, rodrigues-rotation-formula, euler-angles, gimbal-lock, instant-center-of-velocity, error-state-kalman-filter, runge-kutta-methods]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.2.2 (angular velocities, the spatial and the body angular velocity)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 4 (velocity of a rigid body, the rotational velocity in the spatial and the body frame)
---

The angular velocity of a rotating rigid body is the vector $\omega$ whose direction is the instantaneous axis of rotation and whose length is the rate of turn, in radians per second.
If the orientation of the body at time $t$ is the rotation matrix $R(t)$, then the derivative $\dot R$ is $[\omega_s]R$, where $[\omega_s]$ is the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) of the spatial angular velocity $\omega_s$, written in the fixed frame.
The same motion has the body angular velocity $\omega_b = R^{\mathsf T}\omega_s$, written in the frame of the body, with $\dot R = R[\omega_b]$.
A point fixed in the body moves with the velocity $\omega \times r$, where $r$ is its position relative to a point on the axis.
The angular velocity is not the derivative of any set of three angles; it is a velocity on the rotation group [SO(3)](/special-orthogonal-group/).

## Definition

Let $R(t) \in SO(3)$ be a differentiable curve, the orientation of a body frame $\{b\}$ relative to a fixed frame $\{s\}$.
Differentiate $RR^{\mathsf T} = I$ to get $\dot R R^{\mathsf T} + R\dot R^{\mathsf T} = 0$.
So $\dot R R^{\mathsf T}$ is skew-symmetric, and so is $R^{\mathsf T}\dot R$ by the same argument with $R^{\mathsf T}R = I$.

- The **spatial angular velocity** is the vector $\omega_s \in \mathbb{R}^3$ with $[\omega_s] = \dot R R^{\mathsf T}$, that is $\dot R = [\omega_s] R$.
- The **body angular velocity** is the vector $\omega_b \in \mathbb{R}^3$ with $[\omega_b] = R^{\mathsf T}\dot R$, that is $\dot R = R[\omega_b]$.

Both describe the same physical angular velocity, written in two frames: $\omega_s = R\omega_b$.
This follows from $[\omega_s] = \dot R R^{\mathsf T} = R(R^{\mathsf T}\dot R)R^{\mathsf T} = R[\omega_b]R^{\mathsf T} = [R\omega_b]$.
The spatial angular velocity does not depend on the choice of the body frame, and the body angular velocity does not depend on the choice of the fixed frame.

Velocity of a point.
A point fixed in the body has the constant coordinates $x_b$ in $\{b\}$ and the coordinates $x_s(t) = R(t)x_b$ in $\{s\}$, when the two frames share their origin.
Then $\dot x_s = \dot R x_b = [\omega_s]Rx_b = \omega_s \times x_s$.

Integration.
If $\omega_b$ is constant on $[t, t + h]$, then $R(t + h) = R(t)\,e^{[\omega_b]h}$, which [Rodrigues' formula](/rodrigues-rotation-formula/) computes exactly.
If $\omega_s$ is constant, then $R(t + h) = e^{[\omega_s]h}R(t)$.

## Examples and non-examples

- A rotation about a fixed axis at a constant rate: $R(t) = R_z(\alpha t)$. Then $\omega_s = \omega_b = (0, 0, \alpha)$, because the axis $z$ is the same in both frames.
- A body turned first by $R_0 = R_x(\pi/2)$, which then spins about its own $z$ axis: $R(t) = R_0R_z(t)$. Then $R^{\mathsf T}\dot R = [\hat z]$, so $\omega_b = (0, 0, 1)$ rad/s. And $\omega_s = R\omega_b = R_0\hat z = (0, -1, 0)$ rad/s: the body $z$ axis points along $-y$ in the fixed frame.
- A wheel of radius $r$ that turns at the rate $\alpha$ about a fixed axle has $|\omega| = \alpha$, and its rim moves at the speed $\alpha r$.
- Non-example: the rates of [Euler angles](/euler-angles/) $(\dot\phi, \dot\theta, \dot\psi)$ are not the angular velocity. The two are related by $\omega = E(\phi, \theta)(\dot\phi, \dot\theta, \dot\psi)$, a matrix that depends on the angles and is singular at [gimbal lock](/gimbal-lock/).
- Non-example: there is no orientation vector whose time derivative is $\omega$ in general. Turning by $\pi/2$ about the fixed $x$ axis and then by $\pi/2$ about the fixed $y$ axis gives $R_y(\pi/2)R_x(\pi/2)$, and the opposite order gives $R_x(\pi/2)R_y(\pi/2)$, a different orientation, while the integral of $\omega_s$ is $(\pi/2, \pi/2, 0)$ for both motions.

## Related definitions

- The [twist](/rigid-body-twist/) $(\omega, v)$ adds a linear velocity to the angular velocity and describes the velocity of a full rigid motion.
- The [quaternion kinematic equation](/quaternion-kinematic-equation/) writes the same law as $\dot q = \tfrac12 q \otimes (0, \omega_b)$ for a unit quaternion $q$.
- In the plane, the angular velocity is one number, and the [instant center of velocity](/instant-center-of-velocity/) is the point of the moving plane with zero velocity at that time.
- A gyroscope measures $\omega_b$; an [error-state Kalman filter](/error-state-kalman-filter/) integrates it to track the orientation.
- General ODE methods such as [Runge-Kutta methods](/runge-kutta-methods/) applied to $\dot R = R[\omega_b]$ leave SO(3) slowly; the step $R \leftarrow Re^{[\omega_b]h}$ stays on it.

## References
