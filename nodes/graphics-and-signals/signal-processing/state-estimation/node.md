---
tag: S9RKHV
kind: problem
slug: state-estimation
name: State estimation
aliases:
- filtering of dynamical systems
area: graphics-and-signals/signal-processing
level: core
summary: "Estimate the hidden state of a dynamical system from its inputs and noisy outputs, at the current time, a future time or a past time, under a stated error criterion."
prereqs: [state-space-model]
see_also: [kalman-filter, filtering, smoothing, extended-kalman-filter, unscented-kalman-filter, particle-filter, rauch-tung-striebel-smoother, adaptive-filtering]
sources:
  - book: isbn:9780471708582
    title: "Dan Simon, Optimal State Estimation: Kalman, H Infinity, and Nonlinear Approaches, Wiley, 2006"
    locator: "Chapter 1 (linear systems theory, observability), Chapter 5 (the discrete-time Kalman filter), Chapter 9 (optimal smoothing) and Chapter 11 (the H infinity filter)"
  - book: isbn:9780486439389
    title: "Brian D. O. Anderson and John B. Moore, Optimal Filtering, Dover, 2005 (reprint of the Prentice-Hall edition of 1979)"
    locator: "the chapters on the discrete-time Kalman filter, time-invariant filters and smoothing"
  - paper: doi:10.1115/1.3662552
    title: "R. E. Kalman, A new approach to linear filtering and prediction problems, Journal of Basic Engineering 82(1), 1960, pages 35 to 45"
    locator: "the statement of the filtering and prediction problem for a linear dynamical system driven by noise"
  - paper: doi:10.1109/TME.1964.4323124
    title: "David G. Luenberger, Observing the state of a linear system, IEEE Transactions on Military Electronics 8(2), 1964, pages 74 to 80"
    locator: "the observer, a linear system that reconstructs the state from the inputs and outputs"
---

State estimation is the problem of computing the internal state $x_t$ of a dynamical system from its known inputs and its measured outputs $y_1, \ldots, y_s$, when the state itself is not measured. The state is the smallest set of numbers that, with the future inputs, fixes the future behavior: for a moving vehicle, its position and velocity; for a circuit, its capacitor voltages. The problem has three timing cases: *filtering* estimates $x_t$ from data up to $t$, *prediction* estimates a future state, and *smoothing* estimates a past state with later data. It also needs a criterion for a good estimate. With a linear model, Gaussian noise and the mean-square criterion, the [Kalman filter](/kalman-filter/) solves the filtering case exactly. The probability view of the same problem, with the full posterior distribution as the answer, is on the [filtering](/filtering/) page.

## In plain words

Often the quantity you care about cannot be measured. A radar sees the distance to a plane but not its speed, and a thermometer on the outside of an oven does not see the heat inside. If you know the rules by which the hidden quantity changes, and how the measurements depend on it, you can work back from the measurements to the hidden quantity. Measurements are noisy and the rules are not perfect, so the result is an estimate, and a good method also says how sure it is. Some uses need the answer right now, some want a forecast, and some can wait and use later data to look back. Before any of this, you must check that the measurements contain enough information. Some hidden quantities never show up in the output at all.

## Definition

**Model.** A discrete-time state-space model with state $x_t \in \mathbb{R}^n$, input $u_t$ and output $y_t \in \mathbb{R}^m$:

$$x_t = f_t(x_{t-1}, u_t) + q_t, \qquad y_t = h_t(x_t) + r_t,$$

with process noise $q_t$ and measurement noise $r_t$. The linear case is $x_t = A x_{t-1} + B u_t + q_t$ and $y_t = C x_t + r_t$, usually with zero-mean white noises of covariances $Q$ and $R$, independent of each other and of $x_0$, which has mean $m_0$ and covariance $P_0$. The model classes and their graphical form are on the [state-space model](/state-space-model/) page.

**Task.** Given the model, the inputs and the outputs $y_{1:s}$, compute an estimate $\hat x_{t \mid s}$ of $x_t$. The case $s = t$ is filtering, $s < t$ is prediction, and $s > t$ is smoothing. A complete answer also gives a measure of its error, such as the covariance $P_{t \mid s} = E[(x_t - \hat x_{t \mid s})(x_t - \hat x_{t \mid s})^T]$.

**Criteria.**

- *Minimum mean-square error.* Minimize $E\|x_t - \hat x_{t \mid s}\|^2$. The answer is the conditional mean $E[x_t \mid y_{1:s}]$. Among estimators that are linear in the data, the answer depends only on the means and covariances.
- *Maximum a posteriori.* Maximize the posterior density over the whole path $x_{0:T}$. For the linear Gaussian model this is a weighted least-squares problem in the path, with the same answer as the mean.
- *Worst case.* For $H^\infty$ estimation, bound the ratio of the estimation-error energy to the energy of the noises and of the initial error, for every noise sequence. No statistics of the noise are assumed.
- *Set membership.* With bounded noise, compute the set of all states that agree with the data, often as an ellipsoid or a polytope.
- *Exact reconstruction.* With no noise, recover $x_t$ exactly after a finite number of outputs, or as $t \to \infty$. This is the task of an observer.

**Observability.** For the linear model with no noise, the outputs $y_1, \ldots, y_n$ fix $x_0$ for every input if and only if the observability matrix $\mathcal{O} = [C; CA; \ldots; CA^{n-1}]$ has rank $n$. Without this condition, some directions of the state never reach the output, and no estimator can recover them. A weaker condition, detectability, asks only that the unobservable modes are stable; it is enough for an error that goes to zero.

## Variants

- **Filtering, prediction and smoothing.** Smoothing comes in three kinds: *fixed interval* (all $x_t$ for $t \le T$ from $y_{1:T}$, done offline), *fixed lag* ($x_{t-L}$ from $y_{1:t}$, with a fixed delay $L$) and *fixed point* (one past state, refined as data arrive). The general probabilistic forms are on [smoothing](/smoothing/).
- **Continuous time.** The state follows a differential equation and the output is continuous. The linear solution is the Kalman-Bucy filter, with a Riccati differential equation for the covariance.
- **Steady state.** For a time-invariant linear model the gain of the optimal filter often converges. A filter with the constant limit gain is a time-invariant system, and the alpha-beta filters used in tracking are of this kind.
- **Colored or correlated noise.** Noise that is not white is modeled by extra states, which makes the problem standard again with a larger state.
- **Unknown parameters.** Joint estimation of state and parameters, by adding the parameters to the state or by a separate identification loop. With a constant state, this is [adaptive filtering](/adaptive-filtering/).
- **Nonlinear models.** The posterior is no longer Gaussian. Approximate filters linearize the model, propagate sample points or use Monte Carlo samples.
- **Constrained states.** Known bounds or equalities on the state, for example a positive concentration, are added to the estimator.

## Examples

**A deadbeat observer for constant velocity.** The state is position and velocity, $x_t = (p_t, v_t)$, with $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$, and only the position is measured, $C = [1\ \ 0]$. The observability matrix $[C; CA] = \begin{bmatrix} 1 & 0 \\ 1 & 1 \end{bmatrix}$ has rank 2, so the velocity can be recovered from positions. A Luenberger observer runs $\hat x_t = A \hat x_{t-1} + L (y_{t-1} - C \hat x_{t-1})$ with a gain $L$. Its error $\epsilon_t = x_t - \hat x_t$ obeys $\epsilon_t = (A - LC)\, \epsilon_{t-1}$. With $L = (2, 1)^T$,

$$A - LC = \begin{bmatrix} -1 & 1 \\ -1 & 1 \end{bmatrix}, \qquad (A - LC)^2 = \begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix},$$

so the error is zero after two steps from any start. With noise, such a fast observer passes on a lot of measurement noise; the [Kalman filter](/kalman-filter/) picks the gain that balances the two.

**An unobservable mode.** If instead only the velocity is measured, $C = [0\ \ 1]$, then $[C; CA] = \begin{bmatrix} 0 & 1 \\ 0 & 1 \end{bmatrix}$ has rank 1. Two tracks with the same velocity and different start positions give the same outputs forever, so no method can estimate the position. The mode is also not stable (its eigenvalue is $1$), so the system is not detectable.

**A scalar random walk.** For $x_t = x_{t-1} + q_t$ and $y_t = x_t + r_t$ with $Q = 1$, $R = 2$ and $P_0 = 4$, the minimum filtering variances are $P_1 = 10/7$, $P_2 = 34/31$, $P_3 = 130/127$, and they converge to $1$. The [Kalman filter](/kalman-filter/) page derives these numbers and the closed form.

## Known algorithms

- **[Kalman filter](/kalman-filter/).** Exact MMSE filtering and prediction for linear Gaussian models, and the best linear estimator for any noise with the same means and covariances. $O(n^3 + m^3)$ per step for dense matrices.
- **[Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/).** Exact fixed-interval smoothing for linear Gaussian models, with a backward pass after the Kalman filter.
- **[Extended Kalman filter](/extended-kalman-filter/) and [unscented Kalman filter](/unscented-kalman-filter/).** Gaussian approximations for nonlinear models, by Jacobians or by sigma points.
- **[Particle filter](/particle-filter/).** Monte Carlo filtering for any model that can be simulated.
- **Luenberger observer.** A deterministic estimator with a gain chosen to place the eigenvalues of $A - LC$; it needs observability for arbitrary placement.
- **$H^\infty$ filter.** A Riccati recursion like that of the Kalman filter, with an extra term set by the bound $\gamma$; it exists only for $\gamma$ above a threshold.
- **Moving horizon estimation.** Solve a constrained least-squares or MAP problem over a sliding window of the last $L$ steps at each time. It handles constraints and nonlinear models at the cost of an optimization per step.
- **Batch least squares.** For an offline problem, the whole path $x_{0:T}$ is the solution of one sparse banded [least-squares problem](/least-squares-problem/), which a Cholesky factorization solves in $O(T n^3)$.

## Bounds

- **Optimality of the conditional mean.** For any model, $E[x_t \mid y_{1:s}]$ has the least mean-square error among all functions of $y_{1:s}$. For the linear Gaussian model, the Kalman filter computes it exactly.
- **The Riccati limit.** For a time-invariant linear model with $(A, C)$ detectable and $(A, Q^{1/2})$ stabilizable, the prediction covariance converges to the unique stabilizing solution of the discrete algebraic Riccati equation from any $P_0 \succeq 0$, and the steady filter is stable. The limit is a lower bound on the steady mean-square error of any linear estimator.
- **Information bound.** For nonlinear models, the posterior Cramér-Rao bound gives a lower bound on the mean-square error of any estimator, computed by a recursion of the same shape as the Kalman covariance.
- **Cost.** A step of the Kalman filter needs a few products of $n \times n$ matrices and the inverse of an $m \times m$ matrix, so $O(n^3 + m^3)$ for dense matrices. Structure, such as a sparse $A$ or a scalar output, reduces it.

## Reductions

- **To Bayesian filtering.** With noise distributions given, state estimation under the MMSE criterion reduces to computing the [filtering](/filtering/) or [smoothing](/smoothing/) distribution and taking its mean.
- **To least squares.** For the linear Gaussian model, MAP estimation of the path is a weighted [least-squares problem](/least-squares-problem/) with a block tridiagonal normal matrix. The Kalman filter and the RTS smoother solve it by block elimination in time order.
- **From adaptive filtering.** Estimation of a constant weight vector $w$ from $d_t = u_t^T w + v_t$ is state estimation with $A = I$ and $Q = 0$. The Kalman filter then reduces to the [RLS algorithm](/rls-algorithm/) with forgetting factor 1.
- **To the Wiener filter.** For a stationary model in steady state, the steady Kalman filter is a causal [Wiener filter](/wiener-filter/) for the state, written in state-space form.
- **Duality with control.** The Kalman filter Riccati equation for $(A, C, Q, R)$ is the control Riccati equation of the linear quadratic regulator for $(A^T, C^T)$ with the same weights. Observer gain placement is dual to state-feedback pole placement.

## Applications

- **Navigation.** Position, velocity and attitude from inertial sensors, satellite fixes and odometry.
- **Target tracking.** Radar and sonar tracks from range and bearing, often with constant-velocity or constant-acceleration models.
- **Control.** Output-feedback controllers estimate the state that a state-feedback law needs. With a linear model and quadratic costs, the separation principle makes the estimator and the controller separate designs.
- **Power systems.** Bus voltages and phase angles of an electric grid from redundant meter readings.
- **Battery management.** The state of charge of a cell from its voltage and current.
- **Geophysics and weather.** Data assimilation corrects the state of a large model with measurements.

## References
