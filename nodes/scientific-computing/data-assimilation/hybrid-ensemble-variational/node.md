---
tag: GBD29Q
kind: algorithm
slug: hybrid-ensemble-variational
name: Hybrid ensemble-variational assimilation
aliases:
- EnVar
- hybrid 3D-Var
area: scientific-computing/data-assimilation
level: research
summary: Blends a static background covariance with a localized ensemble covariance inside a variational cost; used at several operational centers.
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the state dimension, N: the ensemble size, p: the number of observations, m: "the number of conjugate gradient steps, at most p + 1"}
  time: {worst: "Θ(n^3 + p^3 + m (N n^2 + p n + p^2))"}
  space: {extra: "Θ(N n + n^2 + p^2)"}
properties: {deterministic: true, implied_covariance: "beta_c^2 B_c + beta_e^2 L o (X' X'^T)", equals_3dvar: with the hybrid covariance, control_size: n (N + 1), inner_solver: conjugate gradient}
history:
  year: 2000
  people: [Thomas M. Hamill, Chris Snyder, Andrew C. Lorenc]
  note: Hamill and Snyder proposed a hybrid of an ensemble and a static covariance in 3D-Var in 2000, Lorenc gave the alpha control variable form in 2003, and Wang, Snyder and Hamill proved in 2007 that the two forms are equivalent.
prereqs: [three-dimensional-variational-assimilation, covariance-localization]
see_also: [four-dimensional-ensemble-variational, ensemble-kalman-filter, background-error-covariance, control-variable-transform, gaspari-cohn-function, local-ensemble-transform-kalman-filter, incremental-4d-var, covariance-inflation]
sources:
  - paper: doi:10.1175/1520-0493(2000)128<2905:AHEKFV>2.0.CO;2
    title: T. M. Hamill and C. Snyder, A hybrid ensemble Kalman filter-3D variational analysis scheme, Monthly Weather Review 128 (2000) 2905-2919
    locator: the weighted sum of the static and the ensemble covariance in 3D-Var
  - paper: doi:10.1256/qj.02.132
    title: A. C. Lorenc, The potential of the ensemble Kalman filter for NWP, a comparison with 4D-Var, Quarterly Journal of the Royal Meteorological Society 129 (2003) 3183-3203
    locator: the alpha control variable with localization in a variational system
  - paper: doi:10.1175/MWR3282.1
    title: X. Wang, C. Snyder and T. M. Hamill, On the theoretical equivalence of differently proposed ensemble-3DVAR hybrid analysis schemes, Monthly Weather Review 135(1) (2007) 222-227
    locator: the proof that the covariance form and the alpha control variable form give the same analysis
  - paper: doi:10.1002/qj.2982
    title: R. N. Bannister, A review of operational methods of variational and ensemble-variational data assimilation, Quarterly Journal of the Royal Meteorological Society 143(703) (2017) 607-633
    locator: the hybrid and ensemble-variational systems of the operational centers
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189
    locator: the notation used here
---

Hybrid ensemble-variational assimilation is [3D-Var](/three-dimensional-variational-assimilation/) with a background error covariance that mixes two parts: a static covariance $B_c$, modelled once from long statistics, and the sample covariance of an ensemble of forecasts, with [covariance localization](/covariance-localization/) by a matrix $L$:

$$B = \beta_c^2 B_c + \beta_e^2\, L \circ (X'X'^\top).$$

The static part is full rank but the same every day. The ensemble part follows the weather of the day but has rank at most $N - 1$ and sampling noise, which the localization damps. The matrix $B$ is never formed. Instead the analysis increment is written with the alpha control variable of Lorenc (2003), $\delta x = \beta_c U_c v_c + \beta_e \sum_i x'_i \circ (U_L\alpha_i)$, and the cost is minimized over $(v_c, \alpha_1, \ldots, \alpha_N)$. Wang, Snyder and Hamill (2007) showed that this gives the same analysis as 3D-Var with the mixed $B$. Hybrid systems of this kind are used at several operational centers (Bannister 2017).

## In plain words

To combine a forecast with measurements, the system must know how the forecast errors are spread out and linked in space. One source of this knowledge is long statistics, which are reliable but the same every day. Another is a small set of forecasts that start from slightly different states: where they disagree, today's forecast is uncertain. This source changes with the weather, but a small set gives noisy and incomplete links, so links between far apart points are cut off. The hybrid method uses a weighted mix of both sources. It does this without building the large table of links, by searching over a few extra unknowns for each forecast in the set.

## The problem

**Input.** A background $x^b$, an ensemble of forecasts $x_1, \ldots, x_N$, a static covariance $B_c$, a localization matrix $L$ (for example from the [Gaspari-Cohn function](/gaspari-cohn-function/)), weights $\beta_c^2$ and $\beta_e^2$, and observations $y = Hx + \epsilon$ with $\epsilon \sim N(0, R)$. Here $H$ is linear. Notation of Ide, Courtier, Ghil and Lorenc (1997).

**Output.** The analysis $x^a = x^b + \delta x$, where $\delta x = Uw$ and $w$ minimizes

$$J(w) = \tfrac12 |w|^2 + \tfrac12 (d - HUw)^\top R^{-1}(d - HUw), \qquad d = y - Hx^b, \qquad Uw = \beta_c U_cv_c + \beta_e \sum_{i=1}^N x'_i \circ (U_L\alpha_i),$$

with $x'_i = (x_i - \bar x)/\sqrt{N - 1}$, $U_cU_c^\top = B_c$, $U_LU_L^\top = L$, and $\circ$ the entrywise product.

## The algorithm

```pseudo id=main
HYBRID-ENVAR(x^b, {x_i}, B_c, L, beta_c^2, beta_e^2, y, H, R)
L1  x'_i <- (x_i - mean) / sqrt(N - 1) for i = 1..N
L2  U_c <- square root of B_c ; U_L <- square root of L
L3  d <- y - H x^b
L4  U w = beta_c U_c v_c + beta_e sum_i x'_i o (U_L alpha_i)   ▷ w = (v_c, alpha_1..alpha_N)
L5  b <- U^T H^T R^-1 d
L6  A w = w + U^T H^T R^-1 H U w
L7  w <- solve A w = b by conjugate gradients
L8  x^a <- x^b + U w
L9  return x^a
```

The transpose $U^\top$ in lines L5 and L6 maps a vector $g$ of the state space to $(\beta_c U_c^\top g, \beta_e U_L^\top(x'_1 \circ g), \ldots, \beta_e U_L^\top(x'_N \circ g))$. The cost has no $B^{-1}$: the control variable transform makes the background term $\tfrac12|w|^2$. In large systems $U_c$ is a sequence of operators (balance, vertical and horizontal transforms), and $U_L$ is a spectral or recursive filter, not a dense Cholesky factor.

## Example

**One variable.** Take $x^b = 0$, $B_c = 1$, the ensemble $\{-1, 1\}$, $L = 1$, $\beta_c^2 = \beta_e^2 = \tfrac12$, and one observation $y = 1$ with $H = R = 1$. The perturbations are $x'_{1,2} = \mp 1/\sqrt{1} = \mp 1$, so the ensemble variance is 2 and the hybrid variance is $B = \tfrac12 \cdot 1 + \tfrac12 \cdot 2 = 1.5$. The analysis is $x^a = 1.5/(1.5 + 1) = 0.6$, between the static analysis $0.5$ and the ensemble analysis $2/3$. The reference code gives $0.6$ to rounding error.

**Flow-dependent errors.** On a line of 16 points, each case has its own background error variance, a bump of height 4 at a random place over a floor of 0.05, with a Gaspari-Cohn correlation of half-width 3. The static covariance has the right correlation but the mean variance everywhere. Every second point is observed with error variance 0.25. The table gives the mean squared analysis error over 40 cases (a measurement), with localization of half-width 4:

| covariance | $N = 5$ | $N = 10$ |
|---|---|---|
| static only | 0.207 | 0.207 |
| localized ensemble only | 0.173 | 0.139 |
| hybrid, $\beta_c^2 = \beta_e^2 = 0.5$ | 0.176 | 0.168 |
| hybrid, $\beta_c^2 = 0.25$, $\beta_e^2 = 0.75$ | 0.166 | 0.151 |
| the true covariance | 0.112 | 0.112 |

With 5 members the hybrid with weight 0.75 on the ensemble beats both of its parts. With 10 members the localized ensemble alone is better: the best weights depend on the ensemble size and on how good the static covariance is, and they must be tuned.

## Correctness

The [proof](proofs/correctness.md) shows that $UU^\top = \beta_c^2B_c + \beta_e^2 L \circ (X'X'^\top)$, and with a push-through identity that the minimizer of $J$ gives $x^a = x^b + BH^\top(HBH^\top + R)^{-1}d$ with this $B$, the 3D-Var analysis with the hybrid covariance (a theorem; Wang, Snyder and Hamill 2007). The Hessian is the identity plus a matrix of rank at most $p$, so the conjugate gradient method converges in at most $p + 1$ steps in exact arithmetic. The tests check the analysis to $10^{-8}$ against a direct solve with the dense hybrid covariance on random problems, and the limits $\beta_e = 0$ (3D-Var with $B_c$) and $\beta_c = 0$ without localization (the increment lies in the span of the perturbations).

## Complexity

The control has $n(N + 1)$ entries. With dense square roots one product with $U$ or $U^\top$ costs $\Theta(Nn^2)$, the observation term $\Theta(pn + p^2)$, and the Cholesky factorizations of $B_c$, $L$ and $R$ cost $\Theta(n^3 + p^3)$ once. With $m \le p + 1$ conjugate gradient steps the time is $\Theta(n^3 + p^3 + m(Nn^2 + pn + p^2))$, and the memory is $\Theta(Nn + n^2 + p^2)$. In operational systems the square roots are fast operators, so a product costs about $N$ times one application of the localization operator, and the ensemble itself, $N$ forecasts, is the main extra cost over 3D-Var.

## Properties

- **Equivalent to 3D-Var with the hybrid $B$.** The alpha control variable and the explicit covariance give the same analysis (a theorem).
- **Positive semidefinite by construction.** $L \circ (X'X'^\top)$ is positive semidefinite by the Schur product theorem, so the hybrid $B$ is a valid covariance for any weights $\beta_c^2, \beta_e^2 \ge 0$.
- **Full rank.** With $\beta_c > 0$ and $B_c$ positive definite, the hybrid $B$ has full rank, unlike the raw ensemble covariance, whose increments lie in the span of the $N - 1$ independent perturbations.
- **Flow dependence.** The ensemble part gives variances and correlations of the day, which a static $B_c$ cannot.
- **The weights need tuning.** The best $\beta_c^2$ and $\beta_e^2$ depend on the ensemble size and quality (a measurement, as in the example).

## Variants and improvements

- **[4DEnVar](/four-dimensional-ensemble-variational/).** Use ensemble trajectories over a time window instead of a single time, which gives a 4D analysis without tangent linear and adjoint models.
- **Hybrid 4D-Var.** Use the hybrid $B$ at the start of the window of [incremental 4D-Var](/incremental-4d-var/), with the tangent linear and adjoint models for the propagation.
- **Ensemble of data assimilations.** Make the ensemble by running the variational system itself many times with perturbed observations, instead of with a separate [ensemble Kalman filter](/ensemble-kalman-filter/).
- **Scale-dependent localization.** Localize different spatial scales of the perturbations with different length scales.
- **Pure EnVar.** $\beta_c = 0$: the variational analysis with only the localized ensemble covariance.

## When to use it

Use a hybrid when a variational system already exists and an ensemble is available: it adds flow-dependent covariances at the price of the ensemble and $N$ extra control fields. It helps most when the ensemble is small and the static covariance is reasonable. With a large and well-tuned ensemble, the weight on the ensemble part can grow. If no static covariance model exists, an [ensemble Kalman filter](/ensemble-kalman-filter/) or the [LETKF](/local-ensemble-transform-kalman-filter/) is simpler.

## Pitfalls

- **No localization (line L4).** Without $L$, the ensemble part has rank $N - 1$ and spurious long-range correlations, and observations change the state far away.
- **Wrong perturbation scaling (line L1).** The perturbations must be divided by $\sqrt{N - 1}$, or the ensemble part is $N - 1$ times too large or too small.
- **Weights that do not sum to the right total.** If the static and the ensemble covariances are both good estimates of $B$, then $\beta_c^2 + \beta_e^2 = 1$ keeps the variance right; other choices inflate or deflate it.
- **Ensemble spread that is too small.** An under-dispersive ensemble makes the ensemble part too small; use [covariance inflation](/covariance-inflation/) on the ensemble.
- **An adjoint of $U$ that is not exact (lines L5 and L6).** Then the Hessian is not symmetric and the conjugate gradient method fails. Check $U$ and $U^\top$ with the dot product test.

## Implementations

## History

Hamill and Snyder (2000) proposed a hybrid of an ensemble Kalman filter and 3D-Var, with a weighted sum of the static and the ensemble covariance. Lorenc (2003) introduced the alpha control variable, which brings the localized ensemble covariance into a variational system without forming it, and Wang, Snyder and Hamill (2007) proved that the two formulations are equivalent. Hybrid ensemble-variational systems became operational at several weather centers in the following years (Bannister 2017).

## References
