---
tag: HYX6WP
kind: algorithm
slug: kalman-bucy-filter
name: Kalman-Bucy filter
aliases:
- continuous-time Kalman filter
area: control/optimal-and-predictive-control
level: advanced
summary: The continuous-time optimal linear filter, whose gain comes from a Riccati differential equation dual to that of LQR.
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, p: the number of outputs, h: the time step}
  time: {worst: "O(n^3 + n p^2 + p^3 + n m)"}
  space: {extra: "O(n^2 + n p)"}
properties: {deterministic: true, exact: false, recursive: true, online: true}
history:
  year: 1961
  people: [Rudolf E. Kalman, Richard S. Bucy]
  note: "Kalman and Bucy (1961) gave the continuous-time filter with its Riccati differential equation, one year after Kalman's discrete-time filter, and noted its duality with the regulator problem."
prereqs: [kalman-filter, state-observer, continuous-algebraic-riccati-equation, stochastic-differential-equation]
see_also: [lqg-control, separation-principle, finite-horizon-lqr, luenberger-observer, euler-maruyama-method, runge-kutta-methods, wiener-filter, state-estimation]
sources:
  - paper: "R. E. Kalman and R. S. Bucy, New results in linear filtering and prediction theory, Journal of Basic Engineering 83(1), 95-108, 1961"
    locator: the filter equations, the variance equation (the Riccati differential equation) and the duality with the regulator problem
  - book: isbn:9780486457666
    title: Brian D. O. Anderson and John B. Moore, Optimal Control, Linear Quadratic Methods, Prentice Hall, 1990 (Dover reprint, 2007)
    locator: the chapters on the infinite-time regulator and on state estimator design, with the Kalman-Bucy filter as the dual of the regulator
  - paper: doi:10.1109/TAC.1971.1099818
    title: Michael Athans, The role and use of the stochastic linear-quadratic-Gaussian problem in control system design, IEEE Transactions on Automatic Control 16(6), 529-552, 1971
    locator: the steady state Kalman-Bucy filter as the estimator of the LQG controller
---

The Kalman-Bucy filter is the [Kalman filter](/kalman-filter/) for a plant in continuous time. It is a [state observer](/state-observer/) whose gain $L_o(t) = S(t) C^T V^{-1}$ comes from the Riccati differential equation $\dot S = A S + S A^T + W - S C^T V^{-1} C S$, where $S(t)$ is the covariance of the estimation error. No other gain gives a smaller error covariance, and for Gaussian noise the estimate is the conditional mean of the state. As $t$ grows, $S(t)$ settles at the stabilizing solution of the filter algebraic Riccati equation, and the filter becomes a time-invariant observer. This page covers the continuous-time filter; the discrete-time recursion with its predict and update steps is on the [Kalman filter](/kalman-filter/) page.

## In plain words

A machine moves in continuous time, pushed by random forces, and a sensor reports its position with random errors. The filter keeps a running guess of the full state. It moves the guess forward with the model, and at every instant it nudges the guess toward what the sensor says. The size of the nudge depends on how sure the filter is: when its own guess is poor, it trusts the sensor more, and when the sensor is noisy, it trusts it less. A second equation tracks how unsure the filter is, and it does not depend on the data at all, so it can be solved ahead of time. After a while the uncertainty stops changing and the nudge becomes a fixed amount.

## The problem

Input: matrices $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$ of the plant

$$dx = (A x + B u)\, dt + dw, \qquad dz = C x\, dt + dv,$$

the noise intensities $W = W^T \ge 0$ and $V = V^T > 0$ of the independent Wiener processes $w$ and $v$, the mean $\hat x_0$ and covariance $S_0 \ge 0$ of $x(0)$, the known input $u(t)$, and the measurement $z(t)$. In the white noise notation $y = \dot z = C x + \dot v$ is the measured output.

Output: for each $t$, the estimate $\hat x(t)$ that depends only on $z(s)$ and $u(s)$ for $s \le t$ and minimizes the error covariance $\mathbb{E}\,(x - \hat x)(x - \hat x)^T$ in the sense of positive semidefinite matrices, together with that covariance $S(t)$.

**The filter.**

$$d\hat x = (A \hat x + B u)\, dt + L_o(t) \left(dz - C \hat x\, dt\right), \qquad L_o = S C^T V^{-1},$$

$$\dot S = A S + S A^T + W - S C^T V^{-1} C S, \qquad \hat x(0) = \hat x_0, \quad S(0) = S_0.$$

The term $dz - C \hat x\, dt$ is the innovation. Its increments are white with intensity $V$ when the filter is optimal.

**Duality.** Replace $(A, B, Q, R)$ of the regulator by $(A^T, C^T, W, V)$ and run time backward: the regulator Riccati equation becomes the filter equation. So the steady state filter needs the stabilizing solution of the [CARE](/continuous-algebraic-riccati-equation/) for the dual data, and every Riccati solver serves both problems.

## The algorithm

The filter is advanced in steps of length $h$. In practice the measurement arrives as samples; $\Delta z_k$ is the integral of $y$ over the step.

```pseudo id=main
KALMAN-BUCY(A, B, C, W, V, x̂₀, S₀, h)
L1   x̂ ← x̂₀;  S ← S₀
L2   for each step k, with input u_k and measurement increment Δz_k do
L3       L_o ← S Cᵀ V⁻¹                                    ▷ gain from the current covariance
L4       x̂ ← x̂ + (A x̂ + B u_k) h + L_o (Δz_k - C x̂ h)       ▷ Euler-Maruyama step of the filter
L5       S ← RK4 step of S' = A S + S Aᵀ + W - S Cᵀ V⁻¹ C S   ▷ needs no data
L6       output (x̂, S)
STEADY-STATE(A, C, W, V, S₀, h, tol)
L7   S ← S₀
L8   repeat S ← RK4 step of the Riccati equation until ‖S'‖ ≤ tol
L9   return S and L_o = S Cᵀ V⁻¹
```

Lines L3 and L5 do not use the measurements, so the gain sequence can be computed before the run and stored. Line L4 is the only line that touches the data. If the filter is run long enough, $S$ reaches its steady state, and lines L3 and L5 can be dropped: the filter is then the time-invariant observer $\dot{\hat x} = A \hat x + B u + L_o (y - C \hat x)$, which is the form used in [LQG control](/lqg-control/). Lines L7 to L9 compute that steady state by integrating the Riccati equation until it stops changing. A direct CARE solver such as the [Schur method](/schur-method-riccati/), applied to the dual data, is faster when only the steady state is needed.

## Example

**Scalar, $a = 0$.** With $\dot x = w$, $y = x + \dot v$, $W = V = 1$ and $S_0 = 0$, the Riccati equation is $\dot S = 1 - S^2$, so $S(t) = \tanh t$, and the gain $L_o = S$ grows from 0 to 1. At $t = 0.5, 1, 2$ the variance is $0.4621, 0.7616, 0.9640$.

**Scalar, $a = 1$.** With $\dot x = x + w$ and the same data, $\dot S = 2 S + 1 - S^2$. Put $S = 1 + \sigma$: $\dot \sigma = 2 - \sigma^2$, so

$$S(t) = 1 + \sqrt2 \tanh\left(\sqrt2\, t - \ln(1 + \sqrt2)\right),$$

which takes the values $0.3159, 0.7560, 1.6895, 2.3578, 2.4108$ at $t = 0.25, 0.5, 1, 2, 3$ and tends to $1 + \sqrt2 \approx 2.4142$. The steady state error dynamics are $\dot e = (1 - L_o) e + \dots = -\sqrt2\, e + \dots$, so the filter is Hurwitz although the plant is not. With $a = -1$ the limit is $\sqrt2 - 1 \approx 0.4142$.

**Double integrator.** With $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$, $W = I$ and $V = 1$, the steady state is

$$S_\infty = \begin{bmatrix} \sqrt3 & 1 \\ 1 & \sqrt3 \end{bmatrix}, \qquad L_o = \begin{bmatrix} \sqrt3 \\ 1 \end{bmatrix},$$

and $A - L_o C$ has the characteristic polynomial $s^2 + \sqrt3\, s + 1$. This is the dual of the LQR problem with $Q = I$ and $R = 1$ for the same plant, whose gain is $K = \begin{bmatrix} 1 & \sqrt3 \end{bmatrix} = L_o^T$.

**Against a fixed gain.** For any constant gain $G$, the error covariance obeys $\dot P = (A - G C) P + P (A - G C)^T + W + G V G^T$. Started from the same $S_0$, $P(t) - S(t)$ stays positive semidefinite for every $t$.

**Sample paths.** Take the scalar plant $a = -1$ with $W = V = 1$, $x(0) \sim N(0, 1)$, $\hat x_0 = 0$ and $S_0 = 1$, and simulate 400 paths with the Euler-Maruyama scheme and $h = 0.04$ (seed 2024). At $t = 2$ the Riccati equation gives $S(2) = 0.4159$. The mean squared error over the paths is $0.450$, and the error lies within $\sqrt{S(2)}$ in 255 of the 400 paths (63.8 percent), against 68.3 percent for a Gaussian error with variance $S(2)$. With 400 paths, Hoeffding's inequality allows a deviation of 0.135 at confidence $1 - 10^{-6}$, so the run agrees with the theory.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). For a gain $G(t)$ the error $e = x - \hat x$ obeys $de = (A - G C) e\, dt + dw - G\, dv$, and the Itô rule gives the covariance equation $\dot P_G = (A - GC) P_G + P_G (A - GC)^T + W + G V G^T$. With $G = S C^T V^{-1}$ this is the Riccati equation, so $S$ is the error covariance. For any other gain, $D = P_G - S$ satisfies

$$\dot D = (A - G C) D + D (A - G C)^T + (G - L_o) V (G - L_o)^T, \qquad D(0) = 0,$$

so $D(t) \ge 0$ for all $t$. By duality with the [finite horizon LQR](/finite-horizon-lqr/), $S(t)$ tends to the stabilizing algebraic solution when $(C, A)$ is detectable and $(A, W^{1/2})$ is stabilizable, from every $S_0 \ge 0$.

## Complexity

One step costs $O(n^3)$ for the products in the Riccati right-hand side (four evaluations per RK4 step), $O(n p^2 + p^3)$ for the gain with $V$ factored once, and $O(n^2 + n m + n p)$ for the estimate. Memory is $O(n^2 + n p)$. With a precomputed gain sequence the online cost per step drops to $O(n^2 + n m + n p)$. Integrating to the steady state takes a number of steps that grows with the ratio of the slowest to the fastest time constant of the Riccati flow.

## Properties

- **Optimal among linear filters,** for every $t$ and in the matrix sense, with no Gaussian assumption. With Gaussian $x(0)$, $w$ and $v$, the estimate is the conditional mean, and so it is optimal among all estimators.
- **The covariance does not depend on the data.** $S(t)$ is known before any measurement arrives. This also means that the filter cannot detect a wrong noise model from $S$; only the innovations can show it.
- **The innovation is white** with intensity $V$ for the optimal filter. Testing this property on data checks the model.
- **Steady state.** Under detectability and stabilizability, $S(t) \to S_\infty$ and $A - L_o C$ is Hurwitz. When $A$ is Hurwitz and the signals are stationary, the steady state filter is the causal [Wiener filter](/wiener-filter/) for the same problem, written in state-space form.
- **Duality.** $S(t)$ for the plant equals the regulator Riccati solution for the dual plant with time reversed. Every property of the LQR Riccati equation has a filter version.

## Variants and improvements

- **Correlated noises.** If $w$ and $v$ have cross intensity $M$, the gain becomes $L_o = (S C^T + M) V^{-1}$, and the Riccati equation uses $A - M V^{-1} C$ and $W - M V^{-1} M^T$.
- **Time-varying plants.** The same equations hold with $A(t)$, $C(t)$, $W(t)$ and $V(t)$; there is then no steady state in general.
- **Square root forms** propagate a factor of $S$ so that it stays positive semidefinite in floating point.
- **Continuous-discrete filter.** The state moves in continuous time and the measurements arrive at sampling instants. Propagate $\hat x$ and $S$ between samples with the plant equation and the Lyapunov equation $\dot S = A S + S A^T + W$, and update at each sample with the discrete [Kalman filter](/kalman-filter/) step.
- **Nonlinear plants.** Linearize along the estimate: the continuous-time [extended Kalman filter](/extended-kalman-filter/). It loses the optimality and the data independence of $S$.

## When to use it

Use the Kalman-Bucy filter when the plant model is in continuous time and the measurements are dense compared with the plant dynamics, or as the estimator of an analog or high rate controller. Use the steady state form inside [LQG control](/lqg-control/) and wherever a fixed observer gain is wanted with a noise based tuning. When the measurements come at a slow, fixed rate, use the discrete-time Kalman filter on the sampled model, or the continuous-discrete form. A pole placement [Luenberger observer](/luenberger-observer/) is the alternative when no noise model exists.

## Pitfalls

- **Discretizing with a large step.** The Euler step of line L4 is accurate only for $h$ small compared with the time constants of $A - L_o C$. For slow sampling, discretize the plant exactly and use the discrete filter.
- **White noise is an idealization.** A measurement with a bandwidth that is not much wider than the filter bandwidth is not white; model its color with a shaping filter as extra states.
- **Losing positive semidefiniteness.** Rounding can make $S$ slightly indefinite; symmetrize after each step, or use a square root form.
- **Wrong intensities.** $S$ reports the covariance under the assumed $W$ and $V$, not the true error. A filter with too small $W$ trusts the model too much and can diverge from the true state while $S$ stays small.
- **Undetectable modes.** If $(C, A)$ is not detectable, the error in the unobservable unstable modes grows without bound, and $S(t)$ grows with it.

## Implementations

## History

Kalman (1960) published the discrete-time filter. Kalman and Bucy (1961) treated the continuous-time case: they derived the filter, the variance equation that is now called the Riccati differential equation, and the duality with the regulator problem that Kalman had solved. The steady state filter became the estimator of the LQG controller, which Athans (1971) presented as a design method.

## References
