---
tag: 2VDFY7
kind: algorithm
slug: error-state-kalman-filter
name: Error-state Kalman filter
aliases:
- ESKF
- indirect Kalman filter
area: robotics/localization-and-slam
level: advanced
summary: Propagates a nominal state with the full model and a small error state with a Kalman filter, then folds the error into the nominal.
solves: [attitude-estimation, state-estimation]
model: real-ram
complexity:
  vars: {T: the number of gyro samples, m: the number of vector measurements}
  time: {worst: O(T + m)}
  space: {extra: O(1)}
properties: {deterministic: true, exact: false, online: true, recursive: true}
history:
  year: 1982
  people: [E. J. Lefferts, F. Landis Markley, Malcolm D. Shuster]
  note: Lefferts, Markley and Shuster reviewed Kalman filters for spacecraft attitude and kept the attitude as a reference quaternion with a three-component error in the filter, the form now called the multiplicative extended Kalman filter.
prereqs: [extended-kalman-filter, unit-quaternion-rotation, so3-logarithm-map]
see_also: [invariant-extended-kalman-filter, nonlinear-complementary-filter, kalman-filter, attitude-estimation, uncertainty-on-lie-groups, quaternion-kinematic-equation, unscented-kalman-filter, ekf-localization]
sources:
  - paper: "Joan Solà, Quaternion kinematics for the error-state Kalman filter, arXiv:1711.02508, 2017"
    locator: "Section 5 (error-state kinematics and the Jacobians of the discrete-time system), Sections 6.1 to 6.3 (observation, injection of the error and the reset with its Jacobian) and Section 7 (the variant with a global angular error)"
  - paper: doi:10.2514/3.56190
    title: "E. J. Lefferts, F. L. Markley and M. D. Shuster, Kalman filtering for spacecraft attitude estimation, Journal of Guidance, Control, and Dynamics 5(5), 1982, pages 417 to 429"
    locator: "the filters with a reference quaternion and a three-component attitude error, and the gyro bias in the state"
  - paper: "Nikolas Trawny and Stergios I. Roumeliotis, Indirect Kalman filter for 3D attitude estimation, Technical Report 2005-002, University of Minnesota, 2005"
    locator: "the indirect filter for attitude and gyro bias with a quaternion and a small-angle error"
  - book: isbn:9781493908011
    title: "F. Landis Markley and John L. Crassidis, Fundamentals of Spacecraft Attitude Determination and Control, Springer, 2014"
    locator: "Chapter 6 (sequential attitude filtering), the multiplicative extended Kalman filter"
---

The error-state Kalman filter splits the state in two. A nominal state, here a unit quaternion for the attitude and a gyro bias, is propagated with the full nonlinear model and no noise. A small error state, three angles and three bias errors, is estimated by a linear [Kalman filter](/kalman-filter/). After each correction, the estimated error is folded into the nominal state and reset to zero. Because the error is small and lives in a vector space of the right dimension, the linearization is accurate and the covariance has no constraint to respect, unlike a filter on the four quaternion numbers. For attitude with a gyro bias, this is the multiplicative extended Kalman filter of spacecraft practice, and the same design runs inside most visual-inertial and lidar-inertial odometry systems. The [extended Kalman filter](/extended-kalman-filter/) is the general method it refines; the [invariant extended Kalman filter](/invariant-extended-kalman-filter/) picks a different error so that its dynamics do not depend on the estimate.

## In plain words

Tracking an orientation with a standard estimator is awkward, because an orientation is not a plain list of numbers that can be added and averaged. This filter avoids the problem. It keeps a best guess of the orientation and moves it forward with the gyro readings, exactly as if they were perfect. Next to it, it keeps a small correction, a few angles, together with a measure of how unsure it is about that correction. Small angles do behave like plain numbers, so the standard estimator works well on them. When another sensor, such as gravity or a compass, gives new information, the filter updates the small correction, applies it to the best guess, and starts again with a zero correction.

## The problem

The attitude $R_t = R_{sb}$, with quaternion $q_t$, and the gyro bias $b_t$ evolve as follows over a sample of length $\delta t$. The gyro reads $\omega_m = \omega + b_t + n$ with white noise $n$ of standard deviation $\sigma_g$ per axis; the truth turns by $R_t \leftarrow R_t \operatorname{Exp}(\omega \delta t)$; the bias walks as $b_t \leftarrow b_t + w$ with $w$ of variance $\sigma_w^2 \delta t$ per axis. A vector sensor reads $y = R_t^T d + v$ for a known unit direction $d$, with noise $v$ of standard deviation $\sigma_v$ per axis. Estimate $(R_t, b_t)$ with a covariance, online. The error state is $\delta x = (\delta\theta, \delta b)$ with $R_t = R \operatorname{Exp}(\delta\theta)$ and $b_t = b + \delta b$, the local error of Solà (2017).

## The algorithm

Write $q\{\phi\}$ for the unit quaternion of the rotation vector $\phi$, $\operatorname{Exp}(\phi)$ for its rotation matrix, and $R(q)$ for the rotation of $q$.

```pseudo id=main
ESKF-STEP(q, b, P, ω_m, δt, {(y, d)})       ▷ one gyro sample, then any direction measurements; returns (q, b, P)
L1  ω̂ ← ω_m - b
L2  q ← q ⊗ q{ω̂ δt}, normalized                              ▷ nominal state, no noise
L3  F ← [[Exp(ω̂ δt)^T, -I δt], [0, I]]
L4  P ← F P F^T + diag(σ_g² δt² I, σ_w² δt I)
L5  for each measured direction (y, d) do  ŷ ← R(q)^T d
L6      H ← [[ŷ]_×, 0]
L7      K ← P H^T (H P H^T + σ_v² I)^{-1}
L8      (δθ̂, δb̂) ← K (y - ŷ)
L9      P ← (I - K H) P (I - K H)^T + σ_v² K K^T                ▷ Joseph form
L10     q ← q ⊗ q{δθ̂}, normalized ;  b ← b + δb̂                ▷ injection
L11     G ← diag(I - [½ δθ̂]_×, I) ;  P ← G P G^T                ▷ reset, δx̂ ← 0
```

Lines L1 to L4 are the prediction. The nominal state takes the whole motion, and the error state has mean zero, so only its covariance moves. The block $\operatorname{Exp}(\hat\omega \delta t)^T$ is exact to first order in the error; the block $-I \delta t$ replaces $-J_r(\hat\omega \delta t) \delta t$, with $J_r$ the right Jacobian of $SO(3)$, which is accurate when $|\hat\omega| \delta t$ is small. Lines L5 to L9 are a linear Kalman correction of the error state with the measurement Jacobian $H$ of the [Jacobian linearization](/jacobian-linearization/). Line L10 moves the estimated error into the nominal state, and line L11 accounts for the change of the error's reference frame. A filter without line L11, $G = I$, is a common and usually harmless simplification.

## Example

The body turns with $\omega(t) = (0.4 \sin 0.7 t, \ 0.3 \cos 0.4 t, \ 0.2)$ rad/s. The gyro runs at 100 Hz with $\sigma_g = 0.05$ rad/s, the bias walk has $\sigma_w = 0.002$, and every $0.1$ s two directions are measured, $d = e_3$ and $d = e_1$, with $\sigma_v = 0.05$. The filter starts $30$ degrees off with zero bias error and $P_0 = \operatorname{diag}(0.3^2 I, 0.05^2 I)$.

| time (s) | attitude error (degrees) |
|---|---|
| 0.1 (after the first correction) | 7.29 |
| 0.2 | 2.15 |
| 0.5 | 1.85 |
| 1 | 2.62 |
| 2 | 2.02 |
| 4 | 0.86 |

The first correction removes three quarters of the error. After that the error stays at the level the noise allows; at $4$ s the filter's own standard deviation of each angle is about $0.7$ to $0.9$ degrees, and the bias error is $0.0045$ rad/s. The normalized estimation error squared, which a consistent filter keeps near the error dimension $6$, averaged $7.3$, $5.1$ and $9.0$ for three random seeds over $4$ runs of $2$ s each. All numbers are measurements of the code.

## Correctness

The filter is correct in the sense of every extended Kalman filter: each line is exact for the first-order model of the error. The proof derives that model. The prediction Jacobian follows from $\operatorname{Exp}(\delta\theta^+) = \operatorname{Exp}(-\hat\omega \delta t) \operatorname{Exp}(\delta\theta) \operatorname{Exp}(\hat\omega \delta t - (\delta b + n) \delta t)$ and the identity $Q \operatorname{Exp}(\phi) Q^T = \operatorname{Exp}(Q \phi)$. The measurement Jacobian follows from $\operatorname{Exp}(\delta\theta)^T \approx I - [\delta\theta]_\times$. The reset Jacobian is the right Jacobian $J_r(\delta\hat\theta) = I - \tfrac{1}{2}[\delta\hat\theta]_\times + O(|\delta\hat\theta|^2)$. The Joseph form gives the error covariance for any gain and stays symmetric positive semidefinite. These are theorems under the assumption that second-order terms can be dropped; [the correctness proof](proofs/correctness.md) has the derivations. Convergence and consistency are not theorems here; the example measures them.

## Complexity

In the [real RAM](/real-ram/) model, with the state size fixed at 6, a prediction costs $O(1)$: two $6 \times 6$ products and one exponential. A correction costs $O(1)$: a $3 \times 3$ solve and a few $6 \times 6$ products. Over $T$ gyro samples and $m$ measurements the time is $O(T + m)$, and the memory is $O(1)$. For a general error state of dimension $k$ with measurements of dimension $p$, a step costs $O(k^3 + p^3)$, as for any Kalman filter.

## Properties

- **Minimal error.** The error has 3 attitude components, the number of degrees of freedom, so $P$ is $6 \times 6$ and has no singular direction from a unit-norm constraint.
- **Small error, accurate linearization (heuristic).** The error stays near zero, far from any singularity of the parametrization, and the Jacobians are evaluated where the linear model is best.
- **Unit quaternion.** The nominal quaternion is renormalized after each product; after 200 steps its norm differed from $1$ by less than $10^{-14}$ (measurement).
- **Partial observability.** One direction says nothing about rotation about itself, because $[\hat y]_\times \hat y = 0$. If the attitude block of $P$ is a multiple of $I$ and has no correlation with the bias, a correction with $d$ leaves the variance of the error about $\hat y$ unchanged (theorem from $\hat y^T K = 0$; also a test). With correlations, the other states can still carry some information about that angle.
- **Jacobians match.** The rotation block of $F$ and the matrix $H$ matched finite differences to $10^{-8}$; the bias block differed by about $|\hat\omega| \delta t^2 / 2$, the term dropped in $J_r$ (measurement).

## Variants and improvements

- **Global error.** With $R_t = \operatorname{Exp}(\delta\theta) R$ the error is expressed in the space frame. The Jacobians change, and Solà (2017), Section 7, gives them.
- **Full inertial state.** Add position, velocity and accelerometer bias to the nominal and error states for inertial navigation; the same three phases (predict, correct, inject and reset) apply.
- **Invariant error.** Choosing the error as a group difference that the dynamics leave invariant gives the [invariant extended Kalman filter](/invariant-extended-kalman-filter/), whose error propagation does not depend on the estimate.
- **Sigma points.** An [unscented Kalman filter](/unscented-kalman-filter/) on the same error state avoids the Jacobians.
- **No covariance.** When no covariance is needed, the [nonlinear complementary filter](/nonlinear-complementary-filter/) solves the same problem with two gains.

## When to use it

Use it when the attitude, or a pose, must be fused with other states and sensors under a stated noise model, and an uncertainty is needed, for example in visual-inertial odometry or spacecraft attitude determination. It is the default design when the state contains rotations. For very large initial errors, where first-order models fail, start it from a static solution of [Wahba's problem](/wahba-problem/) or use a filter with a global convergence proof.

## Pitfalls

- **Quaternion conventions.** Hamilton and JPL quaternions multiply in opposite orders, and a local error in one is a global error in the other. Solà (2017) uses Hamilton; Trawny and Roumeliotis (2005) use JPL. Mixing formulas from the two breaks the filter silently.
- **Noise units.** A gyro data sheet gives a noise density in rad/s per square root of Hz. The variance per sample of length $\delta t$ is then density$^2 / \delta t$ for the rate, or density$^2 \, \delta t$ for the angle. The code takes $\sigma_g$ as the standard deviation per sample of the rate, so the angle variance is $\sigma_g^2 \delta t^2$.
- **Forgetting the injection.** If the estimated error is not moved into the nominal state, the error state no longer has mean zero and the prediction is wrong.
- **Symmetry of $P$.** The form $P \leftarrow (I - K H) P$ loses symmetry and definiteness in floating point. The Joseph form of line L9 keeps both.
- **Large errors.** With an error of tens of degrees, the first-order model is poor. The example converged from $30$ degrees, but no theorem promises it.

## Implementations

## History

Kalman filters that estimate the error of a navigation solution, rather than the solution itself, were used in inertial navigation from the 1960s and are called indirect filters. Lefferts, Markley and Shuster (1982) wrote the attitude version with a reference quaternion and a three-component error, which became the standard spacecraft attitude filter. Trawny and Roumeliotis (2005) and Solà (2017) wrote detailed tutorials on the design, and Solà's notes made the name error-state Kalman filter common in robotics.

## References
