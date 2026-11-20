---
tag: 5MYERD
kind: algorithm
slug: four-dimensional-ensemble-variational
name: Four-dimensional ensemble-variational assimilation
aliases:
- 4DEnVar
area: scientific-computing/data-assimilation
level: research
summary: Replaces the tangent linear and adjoint models of 4D-Var by ensemble trajectories over the window, so no adjoint code is needed.
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the state dimension, N: the ensemble size, K: the number of time steps in the window, p: the number of observations in the window, c: the cost of one model step, m: "the number of conjugate gradient steps, at most p + 1"}
  time: {worst: "Θ(N K c + n^3 + p^3 + m (K N n^2 + p n))"}
  space: {extra: "Θ(N K n + n^2 + p^2)"}
properties: {deterministic: true, needs_adjoint: false, model_runs: "(N + 1) K, forward only", implied_covariance: "L o (X'_k X'_l^T)", equals_4dvar: "for a linear model, no localization and X'_0 X'_0^T = B", control_size: N n}
history:
  year: 2008
  people: [Chengsi Liu, Qingnong Xiao, Bin Wang, Mark Buehner]
  note: Liu, Xiao and Wang gave an ensemble-based 4D-Var with the analysis in the space of ensemble trajectories in 2008, and Buehner and coworkers tested an ensemble 4D variational scheme against 4D-Var and the EnKF at Environment Canada in 2010.
prereqs: [hybrid-ensemble-variational, four-dimensional-variational-assimilation]
see_also: [incremental-4d-var, ensemble-kalman-smoother, ensemble-kalman-filter, covariance-localization, adjoint-model, local-ensemble-transform-kalman-filter, conjugate-gradient-method, weak-constraint-4d-var]
sources:
  - paper: doi:10.1175/2008MWR2312.1
    title: C. Liu, Q. Xiao and B. Wang, An ensemble-based four-dimensional variational data assimilation scheme. Part I, technical formulation and preliminary test, Monthly Weather Review 136(9) (2008) 3363-3373
    locator: the analysis increment as a combination of ensemble trajectories, without tangent linear and adjoint models
  - paper: doi:10.1175/2009MWR3157.1
    title: M. Buehner, P. L. Houtekamer, C. Charette, H. L. Mitchell and B. He, Intercomparison of variational data assimilation and the ensemble Kalman filter for global deterministic NWP. Part I, description and single-observation experiments, Monthly Weather Review 138(5) (2010) 1550-1566
    locator: the ensemble 4D variational scheme with localized four-dimensional ensemble covariances
  - paper: doi:10.1175/2009MWR3158.1
    title: M. Buehner, P. L. Houtekamer, C. Charette, H. L. Mitchell and B. He, Intercomparison of variational data assimilation and the ensemble Kalman filter for global deterministic NWP. Part II, one-month experiments with real observations, Monthly Weather Review 138(5) (2010) 1567-1586
    locator: the comparison with 4D-Var and the EnKF over one month of real observations
  - paper: doi:10.1256/qj.02.132
    title: A. C. Lorenc, The potential of the ensemble Kalman filter for NWP, a comparison with 4D-Var, Quarterly Journal of the Royal Meteorological Society 129 (2003) 3183-3203
    locator: the alpha control variable with localization
  - paper: doi:10.1002/qj.2982
    title: R. N. Bannister, A review of operational methods of variational and ensemble-variational data assimilation, Quarterly Journal of the Royal Meteorological Society 143(703) (2017) 607-633
    locator: the 4D ensemble-variational systems of the operational centers
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189
    locator: the notation used here
---

Four-dimensional ensemble-variational assimilation (4DEnVar) fits a model state to all observations of a time window, like [4D-Var](/four-dimensional-variational-assimilation/), but it needs no tangent linear and no [adjoint model](/adjoint-model/). An ensemble of $N$ forecasts is run forward over the window with the full model. At each time $k$ the scaled perturbations $x'_i(k)$ of the members about their mean describe how an error at the start of the window has grown by time $k$. The increment at time $k$ is

$$\delta x_k = \sum_{i=1}^N x'_i(k) \circ (U_L\alpha_i),$$

with the same control $\alpha = (\alpha_1, \ldots, \alpha_N)$ at all times and a localization matrix $L = U_LU_L^\top$. The control is found by minimizing a quadratic cost with the conjugate gradient method. This is the alpha control variable of [hybrid ensemble-variational assimilation](/hybrid-ensemble-variational/), applied over the window. The implied covariance between the increments at times $k$ and $l$ is $L \circ (X'_kX'^\top_l)$, and for a linear model without localization and an ensemble with $X'_0X'^\top_0 = B$ the analysis is exactly 4D-Var.

## In plain words

4D-Var finds the start of a forecast that best fits all measurements in a time window. To do this it needs special extra code that runs the model backward, and this code is hard to write and to keep correct. 4DEnVar replaces this code with a set of ordinary forecasts that start from slightly different states. The way these forecasts spread apart over the window shows how a change at the start moves and grows. The method then looks for the best mix of these spreads to fit the measurements. It uses only the normal forecast model, run once for each member of the set, and the runs can all go at the same time.

## The problem

**Input.** A background state $x^b$ at the start of the window, a model $x_k = \mathcal M_k(x_{k-1})$ for $k = 1, \ldots, K$, an ensemble of start states $x_1(0), \ldots, x_N(0)$, a localization matrix $L$, and observations $y_k = H_kx_k + \epsilon_k$ with $\epsilon_k \sim N(0, R_k)$ at the times $k \in T \subseteq \{1, \ldots, K\}$, with linear $H_k$. Notation of Ide, Courtier, Ghil and Lorenc (1997).

**Output.** The analysis $x^a_k = x^b_k + \delta x_k$ at the start, at the end and at the observation times, where $x^b_k$ is the background trajectory, $\delta x_k$ is as above and $\alpha$ minimizes

$$J(\alpha) = \tfrac12|\alpha|^2 + \sum_{k \in T}\tfrac12(d_k - H_k\delta x_k)^\top R_k^{-1}(d_k - H_k\delta x_k), \qquad d_k = y_k - H_kx^b_k,$$

with $x'_i(k) = (x_i(k) - \bar x(k))/\sqrt{N - 1}$ and $\circ$ the entrywise product.

## The algorithm

```pseudo id=main
FOUR-D-ENVAR(x^b, {x_i(0)}, L, {(H_k, y_k, R_k)}, M, K)
L1  x^b_k <- run the model from x^b for k = 0..K
L2  x_i(k) <- run the model from x_i(0) for i = 1..N    ▷ forward only
L3  x'_i(k) <- (x_i(k) - mean_k) / sqrt(N - 1) ; U_L <- square root of L
L4  d_k <- y_k - H_k x^b_k for every k in T
L5  U_k alpha = sum_i x'_i(k) o (U_L alpha_i)
L6  b <- sum_k U_k^T H_k^T R_k^-1 d_k
L7  A alpha = alpha + sum_k U_k^T H_k^T R_k^-1 H_k U_k alpha
L8  alpha <- solve A alpha = b by conjugate gradients
L9  x^a_k <- x^b_k + U_k alpha for each k
L10 return {x^a_k}
```

The transpose $U_k^\top$ maps a vector $g$ to $(U_L^\top(x'_1(k) \circ g), \ldots, U_L^\top(x'_N(k) \circ g))$. In 4D-Var the same products need the tangent linear model forward and the adjoint model backward at every iteration. Here the time dimension is carried by the stored perturbations $x'_i(k)$, so an iteration costs only products with $U_L$ and with the observation operators. In large systems $U_L$ is a spectral or recursive filter, and only the perturbations at the observation times are stored.

## Example

**One variable.** Take the model $x_1 = 2x_0$, $K = 1$, $x^b = 0$ and the two members $\mp 1/\sqrt 2$. Their perturbations are $x'_{1,2}(0) = \mp 1/\sqrt 2$, so $X'_0X'^\top_0 = 1 = B$, and $x'_{1,2}(1) = \mp\sqrt 2$. One observation $y_1 = 2$ with $H = R = 1$ gives $d_1 = 2$, $C_{11} = 4$, $w = 2/(4 + 1) = 0.4$, and

$$x^a_0 = C_{01}w = 2 \cdot 0.4 = 0.8, \qquad x^a_1 = C_{11}w = 1.6 = 2x^a_0 .$$

This is the 4D-Var analysis $x^a_0 = 1 \cdot 2 \cdot (4 + 1)^{-1} \cdot 2 = 0.8$. The reference code gives $0.8$ and $1.6$ to rounding error.

**Lorenz-63.** A twin run uses the Lorenz-63 equations with forward Euler steps of $0.01$, a window of $K = 25$ steps, a background error of standard deviation 1 in each variable, members drawn about the background with the same spread, and all three variables observed at steps 10 and 25 with error variance 0.25. No localization is used. The table gives the mean error norm over 20 cases (a measurement):

| | start of window | end of window |
|---|---|---|
| background | 1.45 | 2.10 |
| 4DEnVar, $N = 4$ | 1.11 | 0.61 |
| 4DEnVar, $N = 10$ | 0.94 | 0.46 |
| 4DEnVar, $N = 40$ | 0.89 | 0.47 |

The error at the end of the window falls to about a quarter of the background error. More members help up to about $N = 10$; after that the error is limited by the nonlinearity of the model over the window and by the observation errors.

## Correctness

The [proof](proofs/correctness.md) shows that $U_kU_l^\top = L \circ (X'_kX'^\top_l)$, and with a push-through identity that the minimizer gives the conditional mean of the increments given all observations of the window, for a Gaussian prior with these covariance blocks (a theorem). For a linear model with $L$ the matrix of ones and $X'_0X'^\top_0 = B$, the perturbations are $X'_k = M^{(k)}X'_0$, the blocks are $M^{(k)}BM^{(l)\top}$, and the analysis is the strong-constraint 4D-Var analysis (a theorem). The tests check the first result to $10^{-8}$ against a direct solve with the stacked covariance, for a linear and a nonlinear model, the second to $10^{-8}$ against the 4D-Var formula with an ensemble built to have $X'_0X'^\top_0 = B$ exactly, and the count of $(N + 1)K$ forward model calls.

## Complexity

The model runs cost $\Theta(NKc)$ for $N + 1$ forward runs of $K$ steps, and they are independent, so they can run in parallel. The control has $Nn$ entries. With a dense $U_L$, one product with $A$ costs $\Theta(KNn^2 + pn)$, the Cholesky factorizations of $L$ and of the $R_k$ cost $\Theta(n^3 + p^3)$ once, and $m \le p + 1$ conjugate gradient steps give the time $\Theta(NKc + n^3 + p^3 + m(KNn^2 + pn))$. The stored perturbations take $\Theta(NKn)$ memory, or $\Theta(N|T|n)$ if only the observation times are kept. In 4D-Var each iteration needs one tangent linear and one adjoint run over the window, so 4DEnVar trades $m$ such pairs of runs for $N$ forward runs that run at the same time.

## Properties

- **No adjoint.** The model runs only forward, $(N + 1)K$ steps in total, before the minimization starts.
- **Four-dimensional covariance.** The covariance between the increments at times $k$ and $l$ is $L \circ (X'_kX'^\top_l)$, so an observation at time $k$ changes the state at all times of the window (a theorem).
- **Exact 4D-Var in the linear case.** For a linear model, $L$ the matrix of ones and $X'_0X'^\top_0 = B$, the analysis is the strong-constraint 4D-Var analysis (a theorem).
- **Static localization in time.** The same $L$ is applied at all times. If features move far during the window, the localization does not move with them, unlike 4D-Var with a localized $B$, whose covariance the tangent linear model carries along.
- **The analysis trajectory is not a model trajectory.** For a nonlinear model, $x^a_K = x^b_K + \delta x_K$ is in general not $\mathcal M(x^a_0)$.
- **Parallel.** The ensemble runs are independent, and the minimization has no sequential model runs.

## Variants and improvements

- **Hybrid 4DEnVar.** Add a static covariance part, $\beta_cU_cv_c$, to the increment, as in [hybrid ensemble-variational assimilation](/hybrid-ensemble-variational/). The static part has no time evolution in 4DEnVar unless a model propagates it.
- **Hybrid 4D-Var.** Keep the tangent linear and adjoint models of [incremental 4D-Var](/incremental-4d-var/) and use the hybrid covariance only at the start of the window.
- **Outer loops.** Rerun the background and the ensemble from the new analysis to treat stronger nonlinearity, at the cost of more ensemble runs.
- **Ensemble Kalman smoother.** The [ensemble Kalman smoother](/ensemble-kalman-smoother/) uses the same four-dimensional ensemble covariances, but it updates the members by a sequential formula instead of a variational minimization.
- **Weak constraint.** Model error can be added as in [weak-constraint 4D-Var](/weak-constraint-4d-var/), with an ensemble estimate of its covariance.

## When to use it

Use 4DEnVar when an ensemble is already run and the model has no maintained adjoint, or when the computer is massively parallel and the sequential tangent linear and adjoint runs of 4D-Var are the bottleneck. It is the four-dimensional form of a hybrid system and needs a good ensemble with enough spread. If an adjoint exists and the window has strong nonlinearity or features that move far, [4D-Var](/four-dimensional-variational-assimilation/) with a hybrid covariance can give better results. If no variational system exists, an [ensemble Kalman filter](/ensemble-kalman-filter/) or the [LETKF](/local-ensemble-transform-kalman-filter/) is simpler.

## Pitfalls

- **No localization (line L5).** With $N$ much smaller than $n$, the raw four-dimensional covariance has rank $N - 1$ and spurious long-range links, also between times. Use [covariance localization](/covariance-localization/).
- **Wrong perturbation scaling (line L3).** The perturbations must be divided by $\sqrt{N - 1}$, or the implied covariance is too large or too small.
- **Perturbations about the wrong trajectory (lines L1 to L3).** The perturbations are deviations from the ensemble mean at each time, not from the background trajectory. If the mean and the background drift apart, the increments are wrong.
- **Too long a window.** The ensemble perturbations grow nonlinearly and the linear relation between $\delta x_0$ and $\delta x_k$ breaks down. Shorten the window or use outer loops.
- **Ensemble spread that is too small.** An under-dispersive ensemble gives too small increments; use [covariance inflation](/covariance-inflation/).
- **An inexact transpose of $U_k$ (lines L6 and L7).** Then $A$ is not symmetric and the conjugate gradient method fails. Check $U_k$ and $U_k^\top$ with the dot product test.

## Implementations

## History

Lorenc (2003) introduced the alpha control variable, which brings a localized ensemble covariance into a variational system. Liu, Xiao and Wang (2008) formulated an ensemble-based four-dimensional variational scheme in which the increment is a combination of ensemble trajectories, so no tangent linear and adjoint models are needed. Buehner and coworkers (2010) compared an ensemble four-dimensional variational scheme with 4D-Var and the ensemble Kalman filter at Environment Canada. Several operational centers later adopted 4D ensemble-variational systems (Bannister 2017).

## References
