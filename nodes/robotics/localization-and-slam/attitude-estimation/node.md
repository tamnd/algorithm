---
tag: GP0E4A
kind: problem
slug: attitude-estimation
name: Attitude estimation
aliases:
- orientation estimation
area: robotics/localization-and-slam
level: core
summary: "Estimate the orientation of a body from gyroscopes, accelerometers, magnetometers or star sensors."
prereqs: [special-orthogonal-group, angular-velocity, state-estimation]
see_also: [wahba-problem, triad-method, quest-algorithm, nonlinear-complementary-filter, error-state-kalman-filter, invariant-extended-kalman-filter, quaternion-kinematic-equation, dead-reckoning]
sources:
  - book: isbn:9781493908011
    title: "F. Landis Markley and John L. Crassidis, Fundamentals of Spacecraft Attitude Determination and Control, Springer, 2014"
    locator: "Chapter 5 (static attitude determination) and Chapter 6 (sequential attitude filtering)"
  - paper: doi:10.1137/1007077
    title: "Grace Wahba, A least squares estimate of satellite attitude, SIAM Review 7(3), 1965, Problem 65-1"
    locator: "the statement of the static least squares problem"
  - paper: doi:10.1109/TAC.2008.923738
    title: "Robert Mahony, Tarek Hamel and Jean-Michel Pflimlin, Nonlinear complementary filters on the special orthogonal group, IEEE Transactions on Automatic Control 53(5), 2008"
    locator: "Section V (the explicit complementary filter with gyro bias)"
  - paper: doi:10.2514/3.56190
    title: "E. J. Lefferts, F. L. Markley and M. D. Shuster, Kalman filtering for spacecraft attitude estimation, Journal of Guidance, Control, and Dynamics 5(5), 1982, pages 417 to 429"
    locator: "the attitude filters with a reference quaternion and gyro bias"
  - paper: "Oliver J. Woodman, An introduction to inertial navigation, Technical Report UCAM-CL-TR-696, University of Cambridge Computer Laboratory, 2007"
    locator: "Sections 3.2.1 and 3.2.2 (gyro bias and white noise, and the angle errors they cause)"
---

Attitude estimation asks for the orientation of a rigid body, a rotation in the [special orthogonal group](/special-orthogonal-group/) $SO(3)$, from sensors that see directions or rates. Vector sensors, such as an accelerometer that sees gravity, a magnetometer, a sun sensor or a star tracker, give the body-frame form of known directions. A gyroscope gives the [angular velocity](/angular-velocity/), which must be integrated. With vector sensors alone at one instant, the problem is [Wahba's problem](/wahba-problem/), a static least squares fit. With a gyro and a time series, it is a case of [state estimation](/state-estimation/) on a curved space, and filters on $SO(3)$ solve it. The position analog is [mobile robot localization](/mobile-robot-localization/), and integrating the gyro alone is the rotational half of [dead reckoning](/dead-reckoning/).

## In plain words

You want to know which way an object points: a phone, a drone, a satellite. Some sensors tell you where fixed things are as seen from the object, such as which way is down or which way is north. Two such directions, if they are not parallel, are enough to fix the orientation, but each reading is noisy. Another sensor tells you how fast the object turns. Adding up the turns gives a smooth estimate, but small errors pile up and the estimate drifts. Good methods combine the two kinds of sensor: the turn rate for short-term motion and the fixed directions to stop the drift.

## Definition

Write $R = R_{sb}$ for the attitude, the rotation that takes body coordinates to space coordinates. It follows $\dot R = R [\omega]_\times$, with $\omega$ the body angular velocity.

**Static problem.** Given unit directions $r_i$ known in the space frame, their body-frame measurements $b_i \approx R^T r_i$ and weights $a_i > 0$, for $i = 1, \ldots, n$, find $R \in SO(3)$ that minimizes $\tfrac{1}{2} \sum_i a_i |b_i - R^T r_i|^2$. This is [Wahba's problem](/wahba-problem/).

**Dynamic problem.** Given a gyro signal $\omega_m = \omega + \beta + n$, with a slowly varying bias $\beta$ and white noise $n$, and vector measurements $b_i(t) \approx R(t)^T r_i$ at some times, estimate $R(t)$ and often $\beta(t)$, online. A stochastic version asks for the conditional distribution of $R(t)$, or at least a mean and covariance; a deterministic version asks for an observer whose error converges to zero when the data are exact.

The orientation can be stored as a rotation matrix, a [unit quaternion](/unit-quaternion-rotation/) or a rotation vector. [Euler angles](/euler-angles/) are common in interfaces but have [gimbal lock](/gimbal-lock/), so estimators avoid them internally.

## Variants

- **Single snapshot or sequence.** A star tracker often gives enough directions for a static solution at each frame; an inertial unit on a robot usually needs a filter.
- **Attitude and heading reference.** Gyro, accelerometer and magnetometer. The accelerometer gives gravity only when the body does not accelerate.
- **With gyro bias.** The bias is a slow state that the filter must estimate; without vector measurements, it is not observable.
- **Full navigation.** Attitude with position and velocity, from an inertial unit and position fixes. Attitude is then one block of a larger filter.
- **Reduced attitude.** Only the direction of one vector matters, for example the tilt from gravity; the rotation about that vector is left free.

## Examples

- A phone lies flat and points north. The accelerometer reads gravity as $(0, 0, 1)$ in the body frame (up to sign and scale) and the magnetometer reads a vector in the body $x$-$z$ plane. TRIAD on these two directions gives the identity attitude.
- A gyro with white noise of standard deviation $\sigma$ per sample, integrated over $t / \delta t$ samples of length $\delta t$, has an angle error with standard deviation $\sigma \sqrt{\delta t \, t}$ per axis (theorem for independent noise samples; Woodman 2007, Section 3.2.2). A constant bias $\beta$ adds an error $\beta t$ that grows linearly.
- The [nonlinear complementary filter](/nonlinear-complementary-filter/) page shows a filter that recovers from a 107 degree error with exact data, and the [error-state Kalman filter](/error-state-kalman-filter/) page shows one that settles near 1 degree with noisy data.

## Known algorithms

Static, from one set of vector measurements:

- **[TRIAD](/triad-method/).** Two directions, closed form, exact for exact data but not optimal with noise.
- **[Davenport's q-method](/davenport-q-method/).** The optimal quaternion is the top eigenvector of a $4 \times 4$ symmetric matrix.
- **[QUEST](/quest-algorithm/).** The same optimum by Newton's method on the characteristic polynomial, with a closed-form eigenvector.

Dynamic, from a gyro and vector measurements:

- **[Nonlinear complementary filter](/nonlinear-complementary-filter/).** A deterministic observer on $SO(3)$ with a gyro bias estimate and an almost-global stability proof. Two gains, no covariance.
- **[Error-state Kalman filter](/error-state-kalman-filter/).** The multiplicative extended Kalman filter: a nominal quaternion and a three-angle error in a Kalman filter. The standard choice when a covariance is needed.
- **[Invariant extended Kalman filter](/invariant-extended-kalman-filter/).** An EKF on a matrix Lie group with an invariant error, whose error propagation does not depend on the estimate.
- **Gyro integration only.** The [quaternion kinematic equation](/quaternion-kinematic-equation/) integrates the rate; it is exact for a constant rate over a step, but it drifts.

Other filters, such as the [unscented Kalman filter](/unscented-kalman-filter/) and the [particle filter](/particle-filter/), are also used on the same state.

## Bounds

- **Observability (theorem).** Two non-parallel directions determine the attitude uniquely when the data are exact. One direction leaves the rotation about it free. Proof: if $R_1^T r_i = R_2^T r_i$ for two non-parallel $r_i$, then $R_2 R_1^T$ fixes two independent vectors, so it also fixes their cross product, and it is $I$.
- **Static covariance (theorem, to first order).** With measurement noise of variance $\sigma_i^2$ per axis perpendicular to $b_i$, and weights $a_i = 1 / \sigma_i^2$, the optimal static estimate has an error covariance close to $\left(\sum_i a_i (I - b_i b_i^T)\right)^{-1}$ in body angles, when the noise is small (Markley and Crassidis, 2014, Chapter 5). The matrix is invertible exactly when two of the $b_i$ are not parallel.
- **Gyro drift (theorem).** For white rate noise the angle error grows as $\sqrt{t}$; for a constant bias it grows as $t$. Vector measurements bound the error; without them it is unbounded.
- **Topology (theorem).** No continuous observer on $SO(3)$ can make the true attitude a globally asymptotically stable equilibrium, because $SO(3)$ is not contractible. Almost-global convergence, as in Mahony et al. (2008), is the best possible.

## Reductions

- The static problem reduces to a $4 \times 4$ symmetric eigenproblem (q-method) or a $3 \times 3$ [singular value decomposition](/singular-value-decomposition/), and it is the same as the rotation part of the [Kabsch algorithm](/kabsch-algorithm/) for point sets.
- The dynamic problem with a gyro is a [Bayes filter](/bayes-filter/) on $SO(3)$, or on $SO(3) \times \mathbb{R}^3$ with the bias. Kalman filters approximate it with a mean and a covariance of a small error.
- A static solution can serve as the measurement of a filter, which turns the vector measurements into one attitude measurement.

## Applications

Spacecraft attitude determination with star trackers, sun sensors and gyros; drones and other aerial robots, where the attitude feeds the flight controller; phones, game controllers and headsets; legged robots, which need the direction of gravity for balance; and the inertial part of visual-inertial and lidar-inertial odometry.

## References
