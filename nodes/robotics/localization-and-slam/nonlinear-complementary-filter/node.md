---
tag: R8HFJF
kind: algorithm
slug: nonlinear-complementary-filter
name: Nonlinear complementary filter on SO(3)
aliases:
- Mahony filter
- explicit complementary filter
area: robotics/localization-and-slam
level: advanced
summary: Mahony's attitude observer that corrects integrated gyroscope rates with a feedback term from vector measurements, with gyro bias estimation.
solves: [attitude-estimation]
model: real-ram
complexity:
  vars: {n: the number of measured directions, T: the number of time steps}
  time: {worst: O(T n)}
  space: {extra: O(1)}
properties: {deterministic: true, exact: false, online: true, recursive: true}
history:
  year: 2008
  people: [Robert Mahony, Tarek Hamel, Jean-Michel Pflimlin]
  note: Mahony, Hamel and Pflimlin wrote the complementary filter as an observer on the rotation group, with a correction from vector measurements and an integral bias estimate, and proved almost-global stability with a Lyapunov function.
prereqs: [attitude-estimation, lyapunov-function, angular-velocity]
see_also: [error-state-kalman-filter, invariant-extended-kalman-filter, state-observer, luenberger-observer, lasalle-invariance-principle, quaternion-kinematic-equation, wahba-problem, special-orthogonal-group]
sources:
  - paper: doi:10.1109/TAC.2008.923738
    title: "Robert Mahony, Tarek Hamel and Jean-Michel Pflimlin, Nonlinear complementary filters on the special orthogonal group, IEEE Transactions on Automatic Control 53(5), 2008"
    locator: "Section V (the explicit complementary filter with bias correction, equation 32, Theorem 5.1 and Corollary 5.2)"
  - book: isbn:9781493908011
    title: "F. Landis Markley and John L. Crassidis, Fundamentals of Spacecraft Attitude Determination and Control, Springer, 2014"
    locator: "Chapter 6 (sequential attitude filtering), for the Kalman filter alternatives"
---

The nonlinear complementary filter estimates the attitude of a rigid body, a rotation in $SO(3)$, and the bias of its gyroscope. It integrates the gyro rate and corrects it with a feedback term built from vector measurements, such as gravity from an accelerometer and the magnetic field from a magnetometer. The correction is a weighted sum of cross products between the measured directions and the directions that the current estimate predicts, and an integral of the same term estimates the gyro bias. This page covers the explicit form of Mahony, Hamel and Pflimlin (2008), which uses the vectors directly and needs no attitude reconstruction. It is a deterministic [state observer](/state-observer/) with a Lyapunov proof, not a stochastic filter: it has two gains and no covariance. The [error-state Kalman filter](/error-state-kalman-filter/) solves the same [attitude estimation](/attitude-estimation/) problem with a noise model and a covariance, at more cost.

## In plain words

A gyroscope tells you how fast you are turning, so adding up its readings tracks your orientation. But a small error in each reading adds up, and after a while the estimate drifts away. A gravity sensor and a compass do not drift, but they are noisy and easily disturbed. This filter mixes the two. It follows the gyro from moment to moment, and it keeps nudging the estimate so that the predicted gravity and compass directions turn toward the measured ones. A slow memory of these nudges learns the constant error of the gyro and removes it. Two knobs set how hard it nudges and how fast it learns. It is cheap and needs no model of the sensor noise.

## The problem

The attitude $R = R_{sb}$ follows $\dot R = R [\Omega]_\times$, with $\Omega$ the body angular velocity and $[\cdot]_\times$ the [skew-symmetric matrix of a vector](/skew-symmetric-matrix-of-a-vector/). A gyro reads $\Omega_y = \Omega + b$ with a slowly varying bias $b$. For $i = 1, \ldots, n$, a sensor reads $v_i \approx R^T v_{0i}$, the body form of a known unit direction $v_{0i}$ of the space frame. From these signals, estimate $R$ and $b$ online, with an error that goes to zero when the bias is constant and the measurements are exact.

## The algorithm

Choose weights $k_i > 0$, a proportional gain $k_P > 0$ and an integral gain $k_I > 0$. Start from any $\hat R \in SO(3)$ and $\hat b$, often $0$.

```pseudo id=main
ECF-STEP(R̂, b̂, Ω_y, v_{1..n}, v0_{1..n}, k_{1..n}, k_P, k_I, δt)   ▷ returns the new (R̂, b̂)
L1  v̂_i ← R̂^T v0_i for each i                     ▷ predicted body directions
L2  ω_mes ← Σ_i k_i v_i × v̂_i                      ▷ correction
L3  b̂ ← b̂ - k_I ω_mes δt                           ▷ integral term: bias estimate
L4  R̂ ← R̂ exp([Ω_y - b̂ + k_P ω_mes]_× δt)           ▷ corrected gyro rate
```

Lines L1 and L2 compare each measured direction with its prediction. The cross product $v_i \times \hat v_i$ is the axis about which $\hat R$ must turn to bring $\hat v_i$ toward $v_i$, scaled by the sine of the angle between them. Line L3 integrates that error into the bias estimate, as the integral part of a PI controller. Line L4 integrates the corrected rate with the [matrix exponential](/matrix-exponential/), here the [Rodrigues rotation formula](/rodrigues-rotation-formula/), which keeps $\hat R$ a rotation. In continuous time the filter is $\dot{\hat b} = -k_I \omega_{mes}$ and $\dot{\hat R} = \hat R [\Omega_y - \hat b + k_P \omega_{mes}]_\times$, which is equation 32 of Mahony et al. (2008); L3 and L4 are one step of it. The same filter can run on a unit quaternion with the [quaternion kinematic equation](/quaternion-kinematic-equation/).

## Example

The body turns with $\Omega(t) = (0.3 \sin 0.5 t, \ 0.2 \cos 0.3 t, \ 0.1)$ rad/s, and the gyro has the constant bias $b = (0.02, -0.03, 0.01)$ rad/s. Two directions are measured without noise: $v_{01} = e_3$ (gravity) with $k_1 = 1$, and $v_{02} = e_1$ (a magnetic north) with $k_2 = 0.5$. The gains are $k_P = 2$ and $k_I = 0.5$, the step is $\delta t = 0.02$ s, and the start is $\hat b = 0$ with $\hat R = \exp([(1.5, -1, 0.5)]_\times) R$, an error of $107.2$ degrees. The Lyapunov function of the next section is $V$.

| time (s) | attitude error (degrees) | $V$ |
|---|---|---|
| 0 | 107.2 | |
| 1 | 17.35 | 0.141 |
| 2 | 7.49 | |
| 5 | 6.29 | |
| 10 | 1.03 | |
| 20 | 0.127 | |
| 30 | 0.0033 | $8.4 \times 10^{-9}$ |

The first second removes most of the error by the proportional term. The rest falls slowly while the integral term learns the bias; at $t = 30$ s, $\hat b = (0.0200, -0.0300, 0.0101)$. These numbers are measurements of the code.

## Correctness

Let $\tilde b = \hat b - b$, $E_{mes} = \sum_i k_i (1 - v_i \cdot \hat v_i)$ and $V = E_{mes} + |\tilde b|^2 / (2 k_I)$. For a constant bias and exact measurements, the continuous filter gives $\dot V = -k_P |\omega_{mes}|^2 \le 0$, so the error never grows; [the correctness proof](proofs/correctness.md) derives this identity. Convergence needs more. Mahony et al. (2008), Theorem 5.1, prove that with at least two non-parallel directions, a bounded angular velocity and $M_0 = \sum_i k_i v_{0i} v_{0i}^T$ with three distinct eigenvalues, the estimate converges to the true attitude and bias from almost every start. The exceptions are the starts that lead to three unstable equilibria, where $\hat R R^T$ is a rotation by $\pi$ about an eigenvector of $M_0$. Their Lyapunov function has the same form as $V$, with their own error convention. Almost-global is the best possible for a continuous observer on $SO(3)$.

## Complexity

In the [real RAM](/real-ram/) model, one step costs $O(n)$ for lines L1 and L2 (one matrix-vector product and one cross product per direction) and $O(1)$ for lines L3 and L4 (one exponential of a $3 \times 3$ skew-symmetric matrix and one $3 \times 3$ product). Over $T$ steps the time is $O(T n)$. The memory is $O(1)$: the filter keeps only $\hat R$ and $\hat b$.

## Properties

- **Almost-global convergence (theorem).** Under the hypotheses of Theorem 5.1 of Mahony et al. (2008), quoted above.
- **Lyapunov decrease (theorem).** $\dot V = -k_P |\omega_{mes}|^2$ in continuous time. In the discrete code, $V$ rose by less than $10^{-9}$ at any step over 600 steps of the example (measurement).
- **Stays on $SO(3)$.** The exponential update keeps $\hat R$ a rotation; after 600 steps, $\hat R^T \hat R$ differed from $I$ by less than $10^{-12}$ (measurement).
- **Deterministic and cheap.** No covariance, no matrix inverse, no linearization.
- **Bias observability.** With one direction only, the attitude about that direction and the bias along it are not observable. The filter then aligns that one direction and leaves the rest to the gyro.

## Variants and improvements

- **Direct and passive filters.** Mahony et al. (2008) also give a direct and a passive complementary filter, which take a full attitude measurement, for example a solution of [Wahba's problem](/wahba-problem/), in place of the separate vectors.
- **Gains (heuristic).** The filter acts as a low-pass filter on the vector measurements and a high-pass filter on the gyro, with a crossover near $k_P$ rad/s. $k_I$ is usually an order of magnitude below $k_P$, so that the bias estimate is slow.
- **Time-varying weights.** A weight $k_i$ can be lowered when its sensor is unreliable, for example the accelerometer during strong acceleration.
- **Kalman filters.** When a noise model and a covariance are needed, use the [error-state Kalman filter](/error-state-kalman-filter/) or, on matrix Lie groups, the [invariant extended Kalman filter](/invariant-extended-kalman-filter/).

## When to use it

Use it on small embedded systems, such as drones, phones and hobby IMUs, where a few hundred operations per step is the budget, the noise statistics are poorly known, and a proof of convergence from large errors is worth more than optimal noise rejection. Use a Kalman filter when the attitude is fused with other states, such as position and velocity, or when an uncertainty is needed downstream.

## Pitfalls

- **Accelerometers measure more than gravity.** During acceleration, $v_1$ is not the gravity direction, and the filter turns the estimate the wrong way. Lower $k_1$ or ignore the accelerometer when $|a|$ differs from $g$.
- **Magnetic disturbance.** Nearby iron and motor currents bend the magnetic field. Weight the magnetometer low, or use only its horizontal part.
- **Normalize.** The cross product weighs each direction by its length. Use unit vectors, or the weights $k_i$ mean something else.
- **Order of the bias update.** The code uses the new $\hat b$ of line L3 in line L4. Using the old one is also a valid discretization, but the two give slightly different numbers.
- **Equal eigenvalues of $M_0$.** If two eigenvalues of $M_0$ are equal, for example for two orthogonal directions with equal weights, Theorem 5.1 does not apply, and the bad equilibria are no longer three isolated points (heuristic). Choose unequal weights, as in the example.

## Implementations

## History

Complementary filters, which blend a high-frequency sensor with a low-frequency one, are older than this method. Mahony, Hamel and Pflimlin (2008) posed the problem on $SO(3)$, wrote the passive and explicit filters, and proved their almost-global stability with Lyapunov arguments. Their motivation was attitude estimation for small aerial robots with low-cost inertial sensors.

## References
