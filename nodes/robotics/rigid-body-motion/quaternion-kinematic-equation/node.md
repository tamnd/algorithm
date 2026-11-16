---
tag: F6CXDF
kind: theorem
slug: quaternion-kinematic-equation
name: Quaternion kinematic equation
aliases:
- quaternion derivative
area: robotics/rigid-body-motion
level: core
summary: For a unit quaternion q (Hamilton, scalar first) that maps body to world, dq/dt = (1/2) q (0, w_b) = (1/2) (0, w_s) q, a linear equation with no singular attitude.
prereqs: [unit-quaternion-rotation, angular-velocity]
see_also: [gimbal-lock, roll-pitch-yaw-angles, attitude-estimation, error-state-kalman-filter, nonlinear-complementary-filter, dead-reckoning, runge-kutta-methods, spherical-linear-interpolation]
sources:
  - paper: arxiv:1711.02508
    title: Joan Sola, Quaternion kinematics for the error-state Kalman filter, 2017
    locator: Section 4.5 (the time derivatives, equations 200 and 201, and Section 4.5.1 on global and local angular velocities) and Section 4.6.1 (zeroth-order integration, equation 215)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.2.2 (angular velocities in the space and the body frames)
---

The quaternion kinematic equation gives the rate of change of a unit quaternion attitude in terms of the [angular velocity](/angular-velocity/).
For a [unit quaternion](/unit-quaternion-rotation/) $q(t)$ in the Hamilton convention, with the scalar first, whose rotation $R(q)$ maps body coordinates to world coordinates, it reads

$$\dot q = \tfrac12\, q\,(0, \omega_b) = \tfrac12\, (0, \omega_s)\, q,$$

where $\omega_b$ is the angular velocity in the body frame, $\omega_s = R\,\omega_b$ is the same angular velocity in the world frame, and $(0, \omega)$ is a pure quaternion.
The equation is linear in $q$ with coefficients that stay bounded, so it has no singular attitude, unlike the rate equations of [roll-pitch-yaw angles](/roll-pitch-yaw-angles/).
Gyroscope integration, attitude filters and simulators of rigid bodies use it.

Notation on this page: rotations are active, $[\omega]$ is the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) of $\omega$, $q = (w, u)$ has the scalar part $w$ and the vector part $u$, and the product of quaternions is $(a, u)(b, v) = (ab - u \cdot v,\, av + bu + u \times v)$.

## Statement

**Theorem.** Let $q : [0, T] \to S^3$ be a differentiable curve of unit quaternions, and let $R(t) = R(q(t))$, so that $(0, Rv) = q\,(0, v)\,q^*$.
Define the body and the space angular velocities by $[\omega_b] = R^{\mathsf T}\dot R$ and $[\omega_s] = \dot R R^{\mathsf T}$.
Then

$$\dot q = \tfrac12\, q\,(0, \omega_b) = \tfrac12\, (0, \omega_s)\, q .$$

In matrix form, with $q$ as the column $(w, u)$,

$$\dot q = \tfrac12 \begin{pmatrix} 0 & -\omega_b^{\mathsf T} \\ \omega_b & -[\omega_b] \end{pmatrix} q = \tfrac12 \begin{pmatrix} 0 & -\omega_s^{\mathsf T} \\ \omega_s & [\omega_s] \end{pmatrix} q .$$

Conversely, for every continuous $\omega_b(t)$ and every unit $q(0)$, the linear equation $\dot q = \frac12 q\,(0, \omega_b)$ has a unique solution, the solution keeps $|q(t)| = 1$, and $R(q(t))$ is the attitude that solves $\dot R = R[\omega_b]$.

**Other conventions.** If $q$ maps world to body instead, replace $q$ by $q^*$: then $\dot q = -\frac12 (0, \omega_b)\, q$.
In the JPL convention (scalar last, $ij = -k$), the products appear in the reverse order, and the body form becomes $\dot q = \frac12 (0, \omega_b) \otimes q$ in that algebra.
Many errors in practice come from a formula of one convention used with quaternions of another, so state the convention next to the equation.

## In plain words

A quaternion stores an orientation with four numbers.
When the body turns, the four numbers change, and this equation tells how fast.
The rate is half of the current quaternion times the turning rate of the body, so it needs only a product and a scale.
The factor one half comes from the fact that a quaternion stores half of the angle of a turn.
The turning rate can be measured in the body, as a gyroscope does, or in the world, and the product is then taken on the right or on the left.
Nothing in the equation divides by a quantity that can be zero, so it works at every orientation.
A computer that steps the equation in time slowly lets the length of the quaternion drift from one, so it rescales the quaternion after each step.

## Proof

*Step 1: the derivative of a unit quaternion.*
Put $p = q^* \dot q$.
Differentiating $q^* q = 1$ gives $\dot q^* q + q^* \dot q = p^* + p = 0$, so the scalar part of $p$ is zero and $p = (0, \frac12 a)$ for some $a \in \mathbb{R}^3$.
Then $\dot q = q p = \frac12 q\,(0, a)$.

*Step 2: $a$ is the body angular velocity.*
Differentiate $(0, Rv) = q\,(0, v)\,q^*$ for a fixed $v$.
With $\dot q = qp$ and $\dot q^* = p^* q^* = -p\, q^*$,

$$(0, \dot R v) = \dot q\,(0, v)\,q^* + q\,(0, v)\,\dot q^* = q\,\big(p\,(0, v) - (0, v)\,p\big)\,q^* .$$

For pure quaternions, $(0, x)(0, y) - (0, y)(0, x) = (0, 2\, x \times y)$, so $p\,(0, v) - (0, v)\,p = (0, a \times v)$.
So $(0, \dot R v) = q\,(0, a \times v)\,q^* = (0, R(a \times v))$, that is $\dot R = R[a]$, and $[a] = R^{\mathsf T}\dot R = [\omega_b]$.
This proves $\dot q = \frac12 q\,(0, \omega_b)$.

*Step 3: the space form.*
$\omega_s = R\,\omega_b$, because $\dot R R^{\mathsf T} = R[\omega_b]R^{\mathsf T} = [R\omega_b]$.
So $(0, \omega_s) = q\,(0, \omega_b)\,q^*$, and $(0, \omega_s)\,q = q\,(0, \omega_b)$.

*Step 4: the matrix forms.*
The vector part of $q\,(0, \omega)$ is $w\,\omega + u \times \omega = w\,\omega - [\omega]u$, and the scalar part is $-\omega \cdot u$.
For $(0, \omega)\,q$ the vector part is $w\,\omega + [\omega]u$.

*Step 5: the converse.*
The equation is linear with a continuous coefficient, so it has a unique solution on $[0, T]$.
The matrix $\Omega$ of Step 4 is skew-symmetric, so $\frac{d}{dt}|q|^2 = 2\, q^{\mathsf T}\dot q = q^{\mathsf T}\Omega\, q = 0$, and $|q|$ stays 1.
Step 2 then applies to the solution and shows $\dot R = R[\omega_b]$. $\square$

### A check by hand

Take a constant $\omega_b = (0, 0, 1)$ and $q(t) = (\cos\frac t2, 0, 0, \sin\frac t2)$, the rotation by $t$ about $z$.
Then $\dot q = \frac12(-\sin\frac t2, 0, 0, \cos\frac t2)$.
The product $q\,(0, 0, 0, 1)$ has the scalar part $-u \cdot \omega = -\sin\frac t2$ and the vector part $\cos\frac t2\,(0, 0, 1) + u \times \omega = (0, 0, \cos\frac t2)$, since $u$ is parallel to $\omega$.
So $\frac12 q\,(0, \omega_b) = \dot q$.
Here $R$ turns about its own $z$ axis, so $\omega_s = \omega_b$, and the space form gives the same result.

## Consequences

- **Integration over a step.** For a constant $\omega$ over a step of length $\Delta t$, the exact solution is $q(t + \Delta t) = q(t)\,\big(\cos\frac{|\omega|\Delta t}{2}, \sin\frac{|\omega|\Delta t}{2}\,\hat\omega\big)$ with $\hat\omega = \omega/|\omega|$. This step keeps $|q| = 1$ up to rounding, and it is the usual way to integrate gyroscope samples.
- **The forward Euler step drifts.** The step $q + \frac{\Delta t}{2} q\,(0, \omega)$ multiplies $|q|^2$ by $1 + (|\omega|\Delta t/2)^2$. At $1$ rad/s with $\Delta t = 0.01$ s, after $1000$ steps, $|q| = 1.01258$, and after normalization the angle is short by $8.3 \cdot 10^{-5}$ rad, while the exact step above is wrong by $1.3 \cdot 10^{-15}$ rad. Normalize after each step of an [Euler](/euler-method/) or [Runge-Kutta](/runge-kutta-methods/) method.
- **No gimbal lock.** The rate equations of [roll-pitch-yaw angles](/roll-pitch-yaw-angles/) divide by the cosine of the pitch and fail at the [gimbal lock](/gimbal-lock/). The quaternion equation has no division, so [dead reckoning](/dead-reckoning/) and [attitude estimation](/attitude-estimation/) use it for all attitudes.
- **Filters.** The prediction step of the [error-state Kalman filter](/error-state-kalman-filter/) integrates this equation for the nominal attitude, and the [nonlinear complementary filter](/nonlinear-complementary-filter/) adds a correction term to $\omega$ before it integrates.
- **Constant angular velocity gives slerp.** For a constant $\omega_b$, the solution is $q(0)\,\exp(\frac t2 (0, \omega_b))$, which is the path of [spherical linear interpolation](/spherical-linear-interpolation/) between its end points.

## Tightness

- **The factor one half.** It cannot be dropped: the quaternion of a rotation by $\theta$ uses $\frac\theta2$, so $\dot q = q\,(0, \omega)$ would turn the body at twice the true rate.
- **The side of the product.** The body form needs $\omega_b$ on the right and the space form needs $\omega_s$ on the left. With $\omega_b$ on the left, the result is correct only when $\omega_b$ is parallel to the axis of $q$, as in the check by hand, where $\omega_s = \omega_b$.
- **The unit constraint.** For a quaternion with $|q| \ne 1$, the equation still holds for $q/|q|$, because the norm is constant along every solution. Numerical methods do not keep the norm, so the normalization step is needed in practice, not in theory.
- **A nonlinear map in disguise.** The equation is linear in $q$, but the map from $q$ to $R$ is quadratic, and $q$ and $-q$ give the same attitude. A filter that compares quaternions must choose the sign first.

## History

William Rowan Hamilton found the quaternions in 1843 and published them from 1844.
The kinematic equation is the derivative of his rotation formula $q\,(0, v)\,q^*$.
Sola collects the Hamilton and the JPL forms of the equation and the integration methods built on it.

## References
