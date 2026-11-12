---
tag: D8VE3N
kind: algorithm
slug: extended-kalman-filter
name: Extended Kalman filter
aliases:
- EKF
- linearized Kalman filter for nonlinear models
area: machine-learning/probabilistic-inference
level: advanced
summary: "Approximate filter for nonlinear state space models: run the Kalman filter on the model linearized with Jacobians at the current estimate. Exact only for linear models."
solves: [filtering]
model: real-ram
complexity:
  vars: {n: the state dimension, m: the observation dimension, T: the number of time steps}
  time: {worst: "O(T (n^3 + n^2 m + n m^2 + m^3))"}
  space: {extra: "O(n^2 + n m)"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 1962
  people: [Stanley F. Schmidt, Gerald L. Smith, Leonard A. McGee]
  note: Schmidt and his group at NASA Ames linearized the Kalman filter around the current estimate for the navigation of the Apollo spacecraft, which gave the extended Kalman filter.
prereqs: [kalman-filter, filtering, state-space-model]
see_also: [unscented-kalman-filter, particle-filter, rauch-tung-striebel-smoother, smoothing, sequential-monte-carlo, newton-method-for-systems]
sources:
  - book: isbn:9781107619289
    title: "Simo Särkkä, Bayesian Filtering and Smoothing, Cambridge University Press, 2013"
    locator: "Chapter 5 (Taylor series linearization, the extended Kalman filter and its iterated form)"
  - book: isbn:9780486462745
    title: "Andrew H. Jazwinski, Stochastic Processes and Filtering Theory, Academic Press, 1970, Dover reprint 2007"
    locator: the chapter on approximate nonlinear filters (the extended and iterated extended Kalman filters, and divergence)
  - paper: doi:10.1109/JPROC.2003.823141
    title: "Simon J. Julier and Jeffrey K. Uhlmann, Unscented filtering and nonlinear estimation, Proceedings of the IEEE 92(3), 2004, pages 401 to 422"
    locator: the section on the limits of linearization in the extended Kalman filter
  - paper: doi:10.1115/1.3662552
    title: "R. E. Kalman, A new approach to linear filtering and prediction problems, Journal of Basic Engineering 82(1), 1960, pages 35 to 45"
    locator: the linear filter that the extended Kalman filter applies to the linearized model
---

The extended Kalman filter (EKF) is an approximate solver for the [filtering](/filtering/) problem in a nonlinear [state space model](/state-space-model/) with additive Gaussian noise. At each step it replaces the transition function $f$ and the observation function $h$ by their first-order Taylor expansions at the current estimate, using the Jacobian matrices, and then runs one step of the [Kalman filter](/kalman-filter/) on the linearized model. It keeps a Gaussian $\mathcal N(m_t, P_t)$ as its belief about the state. When $f$ and $h$ are linear the EKF is the Kalman filter and is exact. In other cases it has no optimality guarantee, it can be badly overconfident, and it can diverge. It is still the most used nonlinear filter in navigation and tracking, because it is cheap and works well when the nonlinearity is mild over the spread of the belief.

## In plain words

The Kalman filter tracks a hidden quantity when the motion and the measurement are straight-line rules with bell-shaped noise. Real systems bend: a radar measures a distance, which is a square root of squares, and a pendulum moves along a sine. The extended filter handles this by pretending that the rule is a straight line near the current guess. It uses the slope of the rule at the guess and then does the usual Kalman step.

This works when the guess is good and the rule is nearly straight over the range of plausible states. When the guess is far off, or the rule curves sharply, the straight-line picture is wrong, and the filter can become sure of a wrong answer and never recover.

## The problem

The model is

$$x_0 \sim \mathcal N(m_0, P_0), \qquad x_t = f(x_{t-1}) + q_t, \quad q_t \sim \mathcal N(0, Q), \qquad y_t = h(x_t) + r_t, \quad r_t \sim \mathcal N(0, R),$$

for $t = 1, \ldots, T$, with all noise terms independent. The state $x_t$ has dimension $n$ and the observation $y_t$ has dimension $m$. The functions $f$ and $h$ are differentiable, with Jacobian matrices $F(x) = \partial f / \partial x$ ($n \times n$) and $H(x) = \partial h / \partial x$ ($m \times n$). The goal is the filtering distribution $p(x_t \mid y_{1:t})$ for each $t$, computed online. The EKF returns a Gaussian approximation $\mathcal N(m_t, P_t)$ of it.

## The algorithm

The base is the linear Kalman filter for $x_t = A x_{t-1} + q_t$, $y_t = H x_t + r_t$. Its predict step is $m^- = A m$, $P^- = A P A^\top + Q$. Its update step is $S = H P^- H^\top + R$, $K = P^- H^\top S^{-1}$, $m = m^- + K (y - H m^-)$, $P = P^- - K S K^\top$. The EKF keeps these equations. It uses the nonlinear functions for the means and the Jacobians in place of $A$ and $H$ for the covariances.

```pseudo id=main
EXTENDED-KALMAN-FILTER(f, F, h, H, Q, R, m_0, P_0, y_1..y_T)
L1  m ← m_0, P ← P_0
L2  for t ← 1 to T do
L3      F_t ← F(m)                                ▷ Jacobian of f at the last estimate
L4      m⁻ ← f(m);  P⁻ ← F_t P F_tᵀ + Q             ▷ predict
L5      H_t ← H(m⁻)                               ▷ Jacobian of h at the prediction
L6      S ← H_t P⁻ H_tᵀ + R;  K ← P⁻ H_tᵀ S⁻¹
L7      m ← m⁻ + K (y_t − h(m⁻));  P ← P⁻ − K S Kᵀ  ▷ update
L8  return the list of (m, P) for t = 0..T
```

Line L4 pushes the mean through the true function $f$, not through its linearization; for the mean the two agree at the expansion point. Line L7 uses the true $h$ in the innovation $y_t - h(m^-)$. Only the covariances and the gain use the Jacobians.

## Example

**One update by hand.** Take a scalar random walk $f(x) = x$ with $Q = 1/10$, observed through its square, $h(x) = x^2$ with $R = 1/10$. The prior is $m_0 = 1$, $P_0 = 1/2$, and the observation is $y_1 = 2$. Then $F = 1$ and $H(x) = 2x$.

- Predict: $m^- = 1$, $P^- = 1/2 + 1/10 = 3/5$.
- Linearize: $H_1 = H(1) = 2$.
- Gain: $S = 2 \cdot \tfrac35 \cdot 2 + \tfrac1{10} = \tfrac52$, and $K = \tfrac35 \cdot 2 / \tfrac52 = \tfrac{12}{25}$.
- Update: $m_1 = 1 + \tfrac{12}{25}(2 - 1) = \tfrac{37}{25} = 1.48$ and $P_1 = \tfrac35 - \tfrac{144}{625} \cdot \tfrac52 = \tfrac{3}{125} = 0.024$.

The exact posterior, found by numerical integration of prior times likelihood on a fine grid, has mean $1.364$ and variance $0.090$. The observation says $x^2 \approx 2$, so $x$ is close to $\sqrt 2$ or to $-\sqrt 2$; about $1\%$ of the posterior mass sits near $-1.41$. The EKF used the slope of $x^2$ at $x = 1$, which is too small for the region where the posterior lies, so it overshoots the mean. It also reports a variance about four times too small, because one Gaussian cannot hold the second mode. Relinearizing at the new estimate until it stops moving (the iterated EKF) gives $m_1 = 1.4057$ and $P_1 = 0.0124$: a better fit to the main mode, but still blind to the second one.

**A hard benchmark.** On the standard model $x_t = x_{t-1}/2 + 25 x_{t-1}/(1 + x_{t-1}^2) + 8 \cos(1.2 t) + q_t$, $y_t = x_t^2/20 + r_t$ with $Q = 10$, $R = 1$, $m_0 = 0$, $P_0 = 5$ (Kitagawa 1996; Gordon, Salmond and Smith 1993), we simulated $T = 50$ steps with Python's `random.Random(0)`. The root mean squared error of the filtered mean against the true states was $12.9$ for the EKF and $4.8$ for a bootstrap [particle filter](/particle-filter/) with $5000$ particles (seed 1). The sign of $x_t$ is not visible in $y_t$, and the EKF often locks onto the wrong sign.

## Correctness

The EKF is not exact in general, so its correctness statement has three parts, proved in [the correctness proof](proofs/correctness.md). First, each step is the exact Bayes step for the model linearized around the current estimate: the predict step is the Gaussian push-forward through an affine map, and the update step is Gaussian conditioning. Second, when $f$ and $h$ are linear the linearization is exact, the Jacobians are constant, and the EKF output equals the Kalman filter output for every $t$; the tests check this with exact fractions. Third, the error of the predicted mean is $\mathbb E f(x) - f(m) = \tfrac12 \mathrm{tr}(\nabla^2 f(m) P) + O(\|P\|^2)$ for $x \sim \mathcal N(m, P)$, so the EKF is accurate when the curvature of $f$ and $h$ is small over the spread of the belief. On a mild nonlinear test model, the EKF means stay within $0.05$ of a bootstrap particle filter with $20000$ particles.

## Complexity

Each step costs $O(n^3 + n^2 m + n m^2 + m^3)$ arithmetic for the matrix products and the $m \times m$ solve, the same as a Kalman filter step, plus one evaluation of $f$, $h$ and the two Jacobians. A Jacobian costs as much as $n$ evaluations of the function if it is computed by finite differences or forward-mode automatic differentiation. Over $T$ steps the time is $O(T(n^3 + n^2 m + n m^2 + m^3))$ plus the function costs. The filter keeps only the current $m$ and $P$, so the memory is $O(n^2 + nm)$.

## Properties

- **Online.** Each step uses only the previous estimate and the new observation.
- **Exact for linear models.** It equals the Kalman filter then.
- **No optimality in general.** The result is not the posterior mean, not the minimum mean squared error estimate, and not a bound on the error. The covariance $P_t$ is often smaller than the true error covariance.
- **Depends on the coordinates.** A nonlinear change of variables changes the linearization and the answer.
- **Unimodal.** The belief is one Gaussian. Multimodal posteriors, as in the example, are lost.
- **Can diverge.** If the estimate moves far from the true state, the linearization is taken at the wrong place, the gain is wrong, and the error can grow without bound.

## Variants and improvements

- **Iterated EKF.** Repeat the update step with $H$ evaluated at the new estimate until it converges. This is a Gauss-Newton iteration on the maximum a posteriori problem of the update, and it helps when $h$ is strongly nonlinear.
- **Second-order EKF.** Keep the Hessian terms of the Taylor expansion, which corrects the mean by $\tfrac12 \mathrm{tr}(\nabla^2 f\, P)$.
- **Extended RTS smoother.** Run the EKF forward and the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/) backward with the Jacobians as the transition matrices.
- **Error-state or multiplicative EKF.** Linearize in a local error variable, for example for rotations, where the state is not in a vector space.
- **Unscented Kalman filter.** Replace the Jacobians by a deterministic set of sigma points; the [unscented Kalman filter](/unscented-kalman-filter/) is accurate to second order and needs no derivatives.
- **Non-additive noise.** For $x_t = f(x_{t-1}, q_t)$, also take the Jacobian with respect to the noise, $L_t$, and use $L_t Q L_t^\top$ in place of $Q$.

## When to use it

Use the EKF when the model is close to linear over the spread of the belief, the posterior is close to one Gaussian, derivatives are cheap, and the time budget is tight: inertial navigation, GPS receivers, robot localization with good sensors, and many control loops. Prefer the unscented Kalman filter when the nonlinearity is stronger or Jacobians are hard to get. Use a particle filter when the posterior is multimodal or strongly non-Gaussian, as in the benchmark above, and the state dimension is small.

## Pitfalls

- **Wrong Jacobians.** A sign error or a missing term in a hand-written Jacobian gives a filter that runs and gives wrong answers. Check the Jacobians against finite differences.
- **Linearizing at the wrong point.** $F$ is evaluated at the previous filtered mean and $H$ at the predicted mean, not at the observation or the true state.
- **Overconfidence.** The reported covariance ignores the linearization error. Engineers often add extra process noise to $Q$ to keep the filter from trusting itself too much.
- **Angles and other wrapped quantities.** The innovation $y_t - h(m^-)$ of an angle must be wrapped to $(-\pi, \pi]$, or the update jumps.
- **Lost symmetry.** $P^- - K S K^\top$ can lose symmetry or positive definiteness in floating point. The Joseph form $(I - KH) P^- (I - KH)^\top + K R K^\top$ is more stable.
- **Bad initialization.** With a poor $m_0$ and small $P_0$ the filter can lock onto a wrong mode and stay there.

## Implementations

## History

The Kalman filter appeared in 1960. Stanley Schmidt's group at NASA Ames applied it to the midcourse navigation of the Apollo spacecraft and found that it worked on the nonlinear orbital equations if they relinearized around the current estimate instead of a fixed nominal path. The resulting method was reported by Smith, Schmidt and McGee in 1962 and became the extended Kalman filter. Jazwinski's 1970 book gave the standard analysis of the extended and iterated filters and of their divergence. The unscented Kalman filter of Julier and Uhlmann in 1997 and the bootstrap particle filter of 1993 were both introduced as answers to the failures of the EKF on strong nonlinearities.

## References
