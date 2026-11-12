---
tag: B6C1AP
kind: algorithm
slug: unscented-kalman-filter
name: Unscented Kalman filter
aliases:
- UKF
- unscented filter
area: machine-learning/probabilistic-inference
level: advanced
summary: "Approximate nonlinear filter that pushes 2n+1 weighted sigma points through f and h in place of Jacobians. Exact for linear maps; the mean is right to second order."
solves: [filtering]
model: real-ram
complexity:
  vars: {n: the state dimension, m: the observation dimension, T: the number of time steps}
  time: {worst: "O(T (n^3 + n^2 m + n m^2 + m^3))"}
  space: {extra: "O(n^2 + n m)"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 1997
  people: [Simon J. Julier, Jeffrey K. Uhlmann]
  note: Julier and Uhlmann proposed the unscented transform and the filter built on it as a derivative-free and more accurate replacement for the extended Kalman filter.
prereqs: [kalman-filter, extended-kalman-filter, cholesky-decomposition]
see_also: [filtering, state-space-model, particle-filter, rauch-tung-striebel-smoother, smoothing, sequential-monte-carlo]
sources:
  - paper: doi:10.1117/12.280797
    title: "Simon J. Julier and Jeffrey K. Uhlmann, A new extension of the Kalman filter to nonlinear systems, Proceedings of SPIE 3068, Signal Processing, Sensor Fusion, and Target Recognition VI, 1997"
    locator: the unscented transform with 2n+1 sigma points and the parameter kappa, and the filter built on it
  - paper: doi:10.1109/ASSPCC.2000.882463
    title: "Eric A. Wan and Rudolph van der Merwe, The unscented Kalman filter for nonlinear estimation, Proceedings of the IEEE 2000 Adaptive Systems for Signal Processing, Communications, and Control Symposium, 2000"
    locator: the scaled sigma points with alpha, beta and kappa, the UKF equations, and the unscented smoother and parameter estimation
  - paper: doi:10.1109/ACC.2002.1025369
    title: "Simon J. Julier, The scaled unscented transformation, Proceedings of the American Control Conference, 2002"
    locator: the scaling parameter alpha and the role of beta for the fourth moment
  - paper: doi:10.1109/JPROC.2003.823141
    title: "Simon J. Julier and Jeffrey K. Uhlmann, Unscented filtering and nonlinear estimation, Proceedings of the IEEE 92(3), 2004, pages 401 to 422"
    locator: the accuracy of the unscented transform compared with linearization
  - book: isbn:9781107619289
    title: "Simo Särkkä, Bayesian Filtering and Smoothing, Cambridge University Press, 2013"
    locator: "Chapter 5 (the unscented transform and the unscented Kalman filter), Chapter 9 (the unscented RTS smoother)"
---

The unscented Kalman filter (UKF) is an approximate solver for the [filtering](/filtering/) problem in a nonlinear [state space model](/state-space-model/) with additive Gaussian noise. Like the [extended Kalman filter](/extended-kalman-filter/), it keeps a Gaussian belief $\mathcal N(m_t, P_t)$ and runs the predict and update steps of the [Kalman filter](/kalman-filter/). It does not linearize. It picks $2n + 1$ points, the sigma points, whose weighted mean and covariance equal those of the belief, pushes each point through the nonlinear function, and reads off the mean and covariance of the images. This step is the unscented transform. It is exact for linear maps, it gets the mean right through the second-order (and third-order) Taylor terms where the EKF stops at the first, and it needs no derivatives. Its cost is about that of the EKF.

## In plain words

To know where a cloud of possible states goes under a bent rule, the extended filter replaces the rule by a straight line at the centre of the cloud. The unscented filter keeps the rule and moves a few chosen probes instead: the centre of the cloud, and two probes on each axis of the cloud, one on each side. It moves each probe through the rule and fits a new cloud to where the probes land.

A few well-placed probes give a better picture of a bent rule than one slope. In a straight-line world they give the exact answer, and you never have to work out a derivative.

## The problem

The model is

$$x_0 \sim \mathcal N(m_0, P_0), \qquad x_t = f(x_{t-1}) + q_t, \quad q_t \sim \mathcal N(0, Q), \qquad y_t = h(x_t) + r_t, \quad r_t \sim \mathcal N(0, R),$$

for $t = 1, \ldots, T$, with independent noise terms, state dimension $n$ and observation dimension $m$. The goal is $p(x_t \mid y_{1:t})$ for each $t$, computed online. The UKF returns a Gaussian approximation $\mathcal N(m_t, P_t)$. The functions $f$ and $h$ need not be differentiable; the filter only evaluates them.

## The algorithm

**The unscented transform.** Given $x \sim \mathcal N(m, P)$ of dimension $n$ and a map $g$, choose $\alpha > 0$, $\beta \ge 0$ and $\kappa$, and set $\lambda = \alpha^2 (n + \kappa) - n$ and $c = n + \lambda$. Let $\ell_1, \ldots, \ell_n$ be the columns of a matrix square root $L$ with $L L^\top = c P$, usually the [Cholesky factor](/cholesky-decomposition/). The sigma points and weights are

$$X_0 = m, \quad X_j = m + \ell_j, \quad X_{n+j} = m - \ell_j, \qquad W^m_0 = \frac{\lambda}{c}, \quad W^c_0 = \frac{\lambda}{c} + 1 - \alpha^2 + \beta, \quad W^m_i = W^c_i = \frac{1}{2c}.$$

With $Y_i = g(X_i)$, the transform returns $\hat\mu = \sum_i W^m_i Y_i$, $\hat S = \sum_i W^c_i (Y_i - \hat\mu)(Y_i - \hat\mu)^\top$ and the cross-covariance $\hat C = \sum_i W^c_i (X_i - m)(Y_i - \hat\mu)^\top$. Write UT$(g, m, P) = (\hat\mu, \hat S, \hat C)$.

The parameter $\alpha$ sets the spread of the points around $m$, $\kappa$ is a secondary scale, and $\beta$ adds weight to the centre point in the covariance only. The original choice of Julier and Uhlmann is $\alpha = 1$, $\beta = 0$, $\kappa = 3 - n$. The scaled choice of Wan and van der Merwe is a small $\alpha$ such as $10^{-3}$, $\beta = 2$ and $\kappa = 0$.

**The filter.** The Kalman filter predicts with $m^- = A m$, $P^- = A P A^\top + Q$ and updates with $S = H P^- H^\top + R$, $K = P^- H^\top S^{-1}$, $m = m^- + K(y - H m^-)$, $P = P^- - K S K^\top$. The UKF computes the same moments with the unscented transform. The cross-covariance $\hat C$ plays the role of $P^- H^\top$.

```pseudo id=main
UNSCENTED-KALMAN-FILTER(f, h, Q, R, m_0, P_0, y_1..y_T, α, β, κ)
L1  m ← m_0, P ← P_0
L2  for t ← 1 to T do
L3      (m⁻, P⁻, ·) ← UT(f, m, P);  P⁻ ← P⁻ + Q          ▷ predict
L4      (μ, S, C) ← UT(h, m⁻, P⁻);  S ← S + R            ▷ new sigma points from m⁻, P⁻
L5      K ← C S⁻¹
L6      m ← m⁻ + K (y_t − μ);  P ← P⁻ − K S Kᵀ           ▷ update
L7  return the list of (m, P) for t = 0..T
```

## Example

**Sigma points in one dimension.** With $n = 1$, $\alpha = 1$, $\beta = 0$ and $\kappa = 2$ we get $\lambda = 2$ and $c = 3$. For $x \sim \mathcal N(m, P)$ the points are $m$ and $m \pm \sqrt{3P}$ with weights $2/3$, $1/6$ and $1/6$. They have mean $m$, variance $P$ and fourth central moment $2 \cdot \frac16 (3P)^2 = 3P^2$, which is the Gaussian value.

**One update with a square.** This is the example of the [extended Kalman filter](/extended-kalman-filter/) page: $f(x) = x$, $Q = 1/10$, $h(x) = x^2$, $R = 1/10$, $m_0 = 1$, $P_0 = 1/2$ and $y_1 = 2$, with the parameters above.

- Predict: $f$ is linear, so $m^- = 1$ and $P^- = 3/5$.
- Sigma points of $\mathcal N(1, 3/5)$: $1$ and $1 \pm 3/\sqrt5$, that is $1$, $2.342$ and $-0.342$.
- Transform of $h$: $\mu = m^2 + P = 8/5$, $S = 4 m^2 P + 2P^2 + R = 12/5 + 18/25 + 1/10 = 161/50$ and $C = 2 m P = 6/5$.
- Update: $K = (6/5)/(161/50) = 60/161$, so $m_1 = 1 + \frac{60}{161} \cdot \frac25 = \frac{185}{161} \approx 1.149$ and $P_1 = \frac35 - \frac{72}{161} = \frac{123}{805} \approx 0.153$.

| method | $m_1$ | $P_1$ |
|---|---|---|
| exact posterior (grid integration) | 1.364 | 0.090 |
| extended Kalman filter | 1.480 | 0.024 |
| unscented Kalman filter | 1.149 | 0.153 |

The transform got the predicted observation and its variance exactly, because $x^2$ is a polynomial of degree two and $c = 3$. The EKF predicted $\mu = 1$ and missed the spread. The UKF still ends with a Gaussian, while the true posterior has a large mode near $\sqrt 2$ and a small one near $-\sqrt 2$, so it is not exact. Its error is on the cautious side: the variance is too large, not too small.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). It has four parts.

- The sigma points have total weight $1$, mean $m$, covariance $P$ and zero odd central moments, because they come in symmetric pairs.
- For an affine map $g(x) = A x + b$ the transform returns the exact $A m + b$, $A P A^\top$ and $P A^\top$. So on a linear model the UKF equals the Kalman filter and is exact.
- For a polynomial $g$ of degree at most $3$ the transform mean equals $\mathbb E g(x)$, because both the points and the Gaussian have the same moments up to order $3$. For a smooth $g$, the mean agrees through the third-order Taylor terms. The EKF uses $g(m)$ and misses the second-order term $\frac12 \mathrm{tr}(\nabla^2 g\, P)$.
- For $g(x) = x^2$ in one dimension the transform variance is $4 m^2 P + (\alpha^2 \kappa + \beta) P^2$. The true value is $4m^2P + 2P^2$, so the choice $\alpha^2 \kappa + \beta = 2$ makes it exact.

The covariance is not exact for nonlinear maps in general, and the filter has no optimality guarantee.

## Complexity

Each transform needs one Cholesky factorization, $O(n^3)$, plus $2n + 1$ evaluations of the function and the weighted sums, $O(n^2 k + n k^2)$ for an output of dimension $k$. A filter step does two transforms and one $m \times m$ solve, which gives $O(n^3 + n^2 m + n m^2 + m^3)$ arithmetic plus $2(2n + 1)$ function evaluations. This is the same order as the EKF. The EKF needs Jacobians, which cost about $n$ evaluations each when computed numerically, so the UKF is rarely slower in practice. The filter stores only $m$, $P$ and the points: $O(n^2 + nm)$ memory.

## Properties

- **Derivative-free.** Only evaluations of $f$ and $h$ are needed, so they may be black boxes or have kinks.
- **Exact for linear models.** It equals the Kalman filter then.
- **Second-order accurate for the mean.** The mean of a transformed Gaussian is correct through the terms of order three; the EKF is correct through order one.
- **Deterministic.** No random numbers, unlike a [particle filter](/particle-filter/).
- **Unimodal.** The belief is one Gaussian; a multimodal posterior is lost.
- **Not always positive definite.** With $\lambda < 0$, which happens for the default $\kappa = 3 - n$ when $n > 3$, the centre weight is negative and $\hat S$ can fail to be positive semidefinite.

## Variants and improvements

- **Augmented UKF.** For non-additive noise $x_t = f(x_{t-1}, q_t)$, stack the state and the noise into one vector of dimension $n + n_q$ and draw sigma points for the stacked vector.
- **Square-root UKF.** Propagate the Cholesky factor of $P$ with QR updates instead of $P$ itself, which keeps it positive definite and costs the same order.
- **Spherical simplex and other point sets.** Use $n + 2$ points instead of $2n + 1$ to save evaluations.
- **Cubature Kalman filter.** Uses the $2n$ points $m \pm \sqrt{n}\,\ell_j / \sqrt{c}$ with equal weights, which is the UKF with $\alpha = 1$, $\beta = 0$, $\kappa = 0$; it never has a negative weight.
- **Gauss-Hermite Kalman filter.** Uses a product quadrature rule, exact for higher-degree polynomials, at a cost exponential in $n$.
- **Unscented RTS smoother.** Run the UKF forward and a [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/) backward with the gain built from sigma-point cross-covariances.

## When to use it

Use the UKF when the model is nonlinear, the posterior is close to one Gaussian, and Jacobians are hard to write or the nonlinearity is too strong for the EKF: attitude estimation, vehicle tracking with range and bearing sensors, and joint state and parameter estimation. When the posterior is multimodal, as in the example, or the noise is far from Gaussian, use a particle filter if the state dimension allows it. When the model is linear, use the Kalman filter, which gives the same answer for less work.

## Pitfalls

- **Recomputing the points.** Line L4 draws fresh sigma points from $(m^-, P^-)$ after $Q$ is added. Reusing the propagated points from line L3 ignores $Q$ in the observation step.
- **Negative weights.** For $n > 3$ the default $\kappa = 3 - n$ gives a negative centre weight; $P$ can lose positive definiteness. Use $\kappa = 0$ or the scaled form.
- **Tiny $\alpha$.** With $\alpha = 10^{-3}$ the weights are of size $10^{6}$ with opposite signs, and rounding errors grow. Check the sums in floating point.
- **Cholesky failure.** If rounding makes $P$ indefinite, the factorization fails. Symmetrize $P$, or use the square-root form.
- **Angles.** Averages and differences of angles must be wrapped; a plain weighted mean of $179°$ and $-179°$ is $0°$.
- **Mixing the weights.** The mean uses $W^m$ and the covariances use $W^c$; they differ only at the centre point.

## Implementations

## History

Julier and Uhlmann introduced the unscented transform and the filter built on it at an SPIE conference in 1997, after earlier technical reports. Their idea was that it is easier to approximate a probability distribution than an arbitrary nonlinear function. Wan and van der Merwe in 2000 gave the scaled form with $\alpha$, $\beta$ and $\kappa$, and applied it to parameter estimation. Van der Merwe later grouped such methods under the name sigma-point Kalman filters. Julier published the scaled transform in 2002. The filter is now standard in navigation and robotics next to the EKF.

## References
