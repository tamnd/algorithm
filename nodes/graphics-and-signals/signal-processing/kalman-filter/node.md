---
tag: 74AZEE
kind: algorithm
slug: kalman-filter
name: Kalman filter
aliases:
- linear quadratic estimator
- linear-quadratic estimator
area: graphics-and-signals/signal-processing
level: core
summary: "Estimate the state of a linear dynamical system from noisy data by predicting with the model and correcting with the gain K = P C^T S^-1. It is exact for linear Gaussian models."
solves: [state-estimation]
model: real-ram
complexity:
  vars: {n: the size of the state, k: the size of one observation, T: the number of time steps}
  time: {worst: O(T (n^3 + n^2 k + n k^2 + k^3))}
  space: {extra: O(n^2 + n k + k^2)}
properties: {deterministic: true, online: true, recursive: false, exact: true}
history:
  year: 1960
  people: [Rudolf E. Kalman, Richard S. Bucy]
  note: "Kalman published the discrete-time filter in 1960 in the Journal of Basic Engineering, and Kalman and Bucy gave the continuous-time form in 1961; it was soon used for the navigation of the Apollo spacecraft."
prereqs: [state-space-model, state-estimation]
see_also: [extended-kalman-filter, unscented-kalman-filter, particle-filter, rauch-tung-striebel-smoother, rls-algorithm, wiener-filter, schur-complement, hidden-markov-model]
sources:
  - paper: doi:10.1115/1.3662552
    title: "R. E. Kalman, A new approach to linear filtering and prediction problems, Journal of Basic Engineering 82(1), 1960, pages 35 to 45"
    locator: "the state-space formulation, the recursive optimal estimator by orthogonal projection, and the duality with the regulator problem"
  - paper: doi:10.1115/1.3658902
    title: "R. E. Kalman and R. S. Bucy, New results in linear filtering and prediction theory, Journal of Basic Engineering 83(1), 1961, pages 95 to 108"
    locator: "the continuous-time filter and the Riccati differential equation of its covariance"
  - book: isbn:9781107619289
    title: "Simo Särkkä, Bayesian Filtering and Smoothing, Cambridge University Press, 2013"
    locator: "Chapter 4 (the Bayesian filtering equations, and the Kalman filter as their exact solution for linear Gaussian models)"
  - book: isbn:9780471708582
    title: "Dan Simon, Optimal State Estimation, Kalman, H Infinity, and Nonlinear Approaches, Wiley, 2006"
    locator: "Chapter 5 (the discrete-time Kalman filter: derivation, alternate forms, the steady-state filter and the Riccati equation)"
  - book: isbn:9780486439389
    title: "Brian D. O. Anderson and John B. Moore, Optimal Filtering, Dover, 2005, a reprint of the Prentice-Hall edition of 1979"
    locator: "the chapters on the discrete-time Kalman filter, its time-invariant steady state, and its numerical forms"
---

The Kalman filter estimates the hidden state $x_t$ of a linear dynamical system from noisy linear observations $y_1, \ldots, y_t$, one time step at a time. For the [state-space model](/state-space-model/) $x_t = A x_{t-1} + q_t$, $y_t = C x_t + r_t$ with noise covariances $Q$ and $R$, it keeps a mean $m_t$ and a covariance $P_t$. At each step it predicts both with the model, compares the prediction $C m^-$ with the new observation, and corrects the mean by the Kalman gain $K = P^- C^T S^{-1}$ times the difference. When the noise and the initial state are Gaussian, $\mathcal N(m_t, P_t)$ is the exact posterior of $x_t$ given the data, so $m_t$ is the [conditional expectation](/conditional-expectation/) and the best estimate of all. For other noise with the same means and covariances, $m_t$ is still the best estimate that is linear in the data. The cost per step is fixed and does not grow with $t$.

## In plain words

You track something you cannot see directly, such as the position and speed of a car, from noisy measurements, such as GPS fixes. You have a rule for how it moves, which is also uncertain. At each step the filter first uses the rule to guess where the car is now, and its uncertainty grows, because the motion is not exactly known. Then a measurement arrives. The filter compares it with what the guess says the measurement should be and moves the guess part of the way toward it. How far it moves depends on which is more reliable: a precise sensor pulls the guess a long way, and a noisy one only a little. After the correction, the uncertainty shrinks. The filter needs only its current guess and uncertainty, not the old measurements.

## The problem

The inputs are the matrices $A$ ($n \times n$), $Q$ ($n \times n$, positive semidefinite), $C$ ($k \times n$) and $R$ ($k \times k$, positive definite), the mean $m_0$ and covariance $P_0$ of the initial state $x_0$, and the observations $y_1, \ldots, y_T$ of the model

$$x_t = A x_{t-1} + q_t, \qquad y_t = C x_t + r_t, \qquad t = 1, \ldots, T,$$

where $x_0$, $q_t \sim (0, Q)$ and $r_t \sim (0, R)$ are mutually uncorrelated. For each $t$, the output is the mean $m_t$ and the covariance $P_t$ of $x_t$ given $y_1, \ldots, y_t$. This is the filtering form of the [state estimation](/state-estimation/) problem. A known input $B u_t$ added to the state equation changes only line L3.

## The algorithm

```pseudo id=main
KALMAN-FILTER(m₀, P₀, A, Q, C, R, y₁ .. y_T)
L1  m ← m₀; P ← P₀
L2  for t ← 1 to T do
L3      m⁻ ← A m                          ▷ predict the state
L4      P⁻ ← A P Aᵀ + Q
L5      v ← y_t − C m⁻                    ▷ the innovation
L6      S ← C P⁻ Cᵀ + R                   ▷ its covariance
L7      K ← P⁻ Cᵀ S⁻¹                     ▷ the Kalman gain
L8      m ← m⁻ + K v                      ▷ correct the state
L9      P ← P⁻ − K S Kᵀ
L10     output m, P                       ▷ the estimate of x_t from y₁ .. y_t
```

Lines L3 and L4 push the last estimate through the dynamics: the mean moves by $A$, and the covariance moves by $A$ and grows by the process noise $Q$. Line L5 is the innovation, the part of the new observation that the prediction does not explain, and line L6 is its covariance, the uncertainty of the predicted observation plus the sensor noise. Line L7 weighs the two: $K$ is large when $P^-$ is large next to $R$, so the filter trusts the data, and small in the opposite case. Line L8 corrects the mean, and line L9 removes the information gained from the covariance. Lines L4, L6, L7 and L9 do not depend on the data, so the covariances and gains can be computed in advance.

## Example

Take a scalar random walk $x_t = x_{t-1} + q_t$ observed as $y_t = x_t + r_t$, with $Q = 1$, $R = 2$, $m_0 = 0$, $P_0 = 4$, and the data $y = (2, 3, 1)$.

| $t$ | $P^-$ (L4) | $v$ (L5) | $S$ (L6) | $K$ (L7) | $m$ (L8) | $P$ (L9) |
|---|---|---|---|---|---|---|
| 1 | $5$ | $2$ | $7$ | $5/7$ | $10/7$ | $10/7$ |
| 2 | $17/7$ | $11/7$ | $31/7$ | $17/31$ | $71/31$ | $34/31$ |
| 3 | $65/31$ | $-40/31$ | $127/31$ | $65/127$ | $207/127$ | $130/127$ |

At $t = 1$, direct conditioning gives the same answer: $x_1 \sim \mathcal N(0, 5)$ and $y_1 = x_1 + r_1$ have covariance $5$ and $\operatorname{Var}(y_1) = 7$, so $E[x_1 \mid y_1 = 2] = \frac57 \cdot 2 = \frac{10}{7}$ and $\operatorname{Var}(x_1 \mid y_1) = 5 - \frac{25}{7} = \frac{10}{7}$. The covariance follows the map $P \mapsto 2(P + 1)/(P + 3)$, a Möbius map with fixed points $1$ and $-2$, and the closed form is

$$P_t = \frac{1 + 2 c\, 4^{-t}}{1 - c\, 4^{-t}}, \qquad c = \frac{P_0 - 1}{P_0 + 2} = \frac12,$$

which gives $\frac{10}{7}, \frac{34}{31}, \frac{130}{127}$ and tends to $P_\infty = 1$. In steady state $P^- = 2$ and $K = \frac12$: the filter becomes the [exponential moving average](/exponential-moving-average/) $m_t = \frac12 m_{t-1} + \frac12 y_t$.

## Correctness

**Claim.** For every $t$, $m_t$ is the affine function of $y_1, \ldots, y_t$ with the least mean-square error for $x_t$, and $P_t$ is its error covariance. If $x_0$ and the noise terms are independent and Gaussian, then $x_t$ given $y_1, \ldots, y_t$ is exactly $\mathcal N(m_t, P_t)$.

**Key invariant.** Before step $t$, $m$ is the orthogonal projection of $x_{t-1}$ onto the affine functions of $y_1, \ldots, y_{t-1}$, and $P$ is the covariance of its error.

Prediction keeps the invariant because $q_t$ is uncorrelated with the past. The innovation $v$ is orthogonal to the past data, and together with them it spans the same space as $y_1, \ldots, y_t$, so the new projection is the old one plus the projection onto $v$, which is $K v$. In the Gaussian case the error is uncorrelated with the data and jointly Gaussian with them, so it is independent of them, and the projection is the posterior mean. The full proof is below. The tests compare the filter with direct conditioning of the joint Gaussian of $(x_t, y_1, \ldots, y_t)$ by the [Schur complement](/schur-complement/), exactly in fractions, on 500 random models.

## Complexity

Per step, line L3 costs $n^2$ multiplications, line L4 about $2n^3$, line L6 about $n^2 k + n k^2$, line L7 about $n^2 k + n k^2$ plus $O(k^3)$ to factor or invert $S$, and lines L8 and L9 about $nk + n k^2 + n^2 k$. So one step costs $O(n^3 + n^2 k + n k^2 + k^3)$ in the [real RAM](/real-ram/), and $T$ steps cost $T$ times that. The extra space is $O(n^2 + nk + k^2)$ for $P$, $K$ and $S$; the filter keeps no past data. With diagonal $R$, the $k$ observations can be processed one at a time as scalars, which removes the matrix inverse.

## Properties

- **Exact for linear Gaussian models.** The posterior stays Gaussian, so $m_t$ and $P_t$ describe it completely, and $m_t$ minimizes the mean-square error over all estimators.
- **Best linear estimator otherwise.** For noise that is not Gaussian, but uncorrelated with the given covariances, $m_t$ is still the best affine estimate, and $P_t$ is its true error covariance. A nonlinear filter, such as a [particle filter](/particle-filter/), can do better. The tests check both facts by enumeration with two-point noise.
- **Covariance independent of the data.** $P_t$ and $K_t$ follow the Riccati recursion $P \mapsto P^- - P^- C^T (C P^- C^T + R)^{-1} C P^-$ with $P^- = A P A^T + Q$, which does not involve $y$.
- **Steady state.** If $(A, C)$ is detectable and $(A, Q^{1/2})$ is stabilizable, $P_t$ converges to the unique stabilizing solution of the discrete algebraic Riccati equation, and the gain to a constant. The steady-state filter is a fixed linear time-invariant filter, the causal [Wiener filter](/wiener-filter/) for the stationary model.
- **White innovations.** The innovations $v_t$ are uncorrelated with each other and have covariance $S_t$. Testing them for whiteness checks the model; their Gaussian density gives the likelihood of the data, which is used to fit $A$, $C$, $Q$ and $R$.
- **Online and recursive.** Each step uses only $(m, P)$ and the new observation, at a cost that does not grow with $t$.

## Variants and improvements

- **Joseph form.** Compute line L9 as $(I - KC) P^- (I - KC)^T + K R K^T$. It equals $P^- - KSK^T$ in exact arithmetic for the optimal $K$, and it keeps $P$ symmetric positive semidefinite under rounding and for any gain.
- **Square-root and UD filters.** Propagate a Cholesky factor of $P$, or a factorization $U D U^T$, through orthogonal transformations. They double the effective precision and are used in navigation systems.
- **Information filter.** Propagate $P^{-1}$ and $P^{-1} m$. The update becomes an addition, which suits many sensors and an unknown initial state with $P_0^{-1} = 0$.
- **Steady-state filter.** Solve the algebraic Riccati equation once and use the constant gain, for a cost of $O(n^2 + nk)$ per step.
- **Continuous time.** The Kalman-Bucy filter replaces the recursion by a Riccati differential equation.
- **Smoothing.** The [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/) adds a backward pass that conditions every state on all the data.
- **Nonlinear models.** The [extended Kalman filter](/extended-kalman-filter/) linearizes the model, the [unscented Kalman filter](/unscented-kalman-filter/) propagates sigma points, and the [particle filter](/particle-filter/) represents the posterior by samples.
- **Recursive least squares.** For a constant state, $A = I$ and $Q = 0$, the filter with a regressor as the row $C$ is the [RLS algorithm](/rls-algorithm/).

## When to use it

Use the Kalman filter when a linear model of the dynamics and of the sensors is available, with known or estimable noise covariances, and estimates are needed in real time: tracking, navigation and sensor fusion, the state estimate of a controller, and the likelihood of time series models. It also smooths a noisy signal when its dynamics are known, as an alternative to a fixed filter. Use an [extended](/extended-kalman-filter/) or [unscented](/unscented-kalman-filter/) Kalman filter for mildly nonlinear models, a [particle filter](/particle-filter/) for strongly nonlinear or multimodal ones, and the forward algorithm of a [hidden Markov model](/hidden-markov-model/) for a discrete state.

## Pitfalls

- **The prior at the wrong time.** Line L1 takes the prior of $x_0$, and the first observation is of $x_1$, after one prediction. If the prior is for $x_1$, skip lines L3 and L4 at $t = 1$; otherwise the filter adds $Q$ once too often.
- **Inverting S explicitly.** Line L7 written with a computed inverse of $S$ is slow and loses accuracy when $S$ is ill-conditioned. Solve $K S = P^- C^T$ with a Cholesky factorization of $S$.
- **Rounding in the covariance update.** The short form $P \leftarrow (I - KC) P^-$ for line L9 can make $P$ asymmetric or indefinite in floating point, and the filter then diverges. Use the symmetric form $P^- - K S K^T$ and symmetrize it, or the Joseph form.
- **A process noise that is too small.** With $Q$ much smaller than the true one in line L4, $P$ shrinks too fast, the gain goes to zero, and the filter ignores the data and drifts away from the truth. Tune $Q$ so that the innovations have the covariance $S$ that line L6 predicts.
- **Missing observations.** Setting $y_t = 0$ in line L5 when a measurement is missing corrupts the estimate. Skip lines L5 to L9 for that step and keep $m = m^-$ and $P = P^-$.
- **A nonlinear model.** Running lines L3 to L9 with a linear approximation that is chosen once, far from the true state, gives a biased filter that is too confident. Use the nonlinear variants.

## Implementations

## History

Least squares estimation of orbits goes back to Gauss, and the optimal filter for stationary signals to Wiener and Kolmogorov in the 1940s. The Danish astronomer Thiele described a recursive estimator of this kind as early as 1880, and Swerling wrote a closely related method in 1958. Rudolf Kalman published the discrete-time filter in 1960, in a state-space form that allows nonstationary signals and multiple outputs, and he derived it by orthogonal projection. Kalman and Richard Bucy gave the continuous-time form in 1961. Stanley Schmidt at NASA Ames adapted the filter to nonlinear navigation equations, and it was used in the navigation computer of the Apollo program. The filter became a standard part of navigation, tracking, control and econometrics.

## References
