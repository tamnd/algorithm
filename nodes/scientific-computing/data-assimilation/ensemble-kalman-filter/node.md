---
tag: JS3602
kind: algorithm
slug: ensemble-kalman-filter
name: Ensemble Kalman filter
aliases:
- EnKF
area: scientific-computing/data-assimilation
level: core
summary: Propagates an ensemble of states through the model and uses its sample covariance in the Kalman update, with perturbed observations for each member.
solves: [data-assimilation-problem]
model: real-ram
complexity:
  vars: {n: the size of the state, N: the ensemble size, p: the number of observations}
  time: {worst: "Θ(N p (n + p) + p^3)"}
  space: {extra: "Θ(n p + p^2 + N (n + p))"}
properties: {deterministic: false, perturbed_observations: true, exact_kalman_moments: "mean exact for centred perturbations; covariance exact in expectation, for a linear H", derivative_free: true, randomized: "one draw of N(0, R) for each member and each analysis"}
history:
  year: 1994
  people: [Geir Evensen, Gerrit Burgers, Peter Jan van Leeuwen, Peter L. Houtekamer, Herschel L. Mitchell]
  note: "Evensen proposed the ensemble Kalman filter in 1994. In 1998 Burgers, van Leeuwen and Evensen, and also Houtekamer and Mitchell, used perturbed observations, which give the right analysis spread."
prereqs: [kalman-filter, data-assimilation-problem, monte-carlo-integration]
see_also: [ensemble-square-root-filter, ensemble-transform-kalman-filter, local-ensemble-transform-kalman-filter, covariance-inflation, covariance-localization, ensemble-kalman-smoother, ensemble-kalman-inversion, extended-kalman-filter]
sources:
  - paper: doi:10.1029/94JC00572
    title: "G. Evensen, Sequential data assimilation with a nonlinear quasi-geostrophic model using Monte Carlo methods to forecast error statistics, Journal of Geophysical Research: Oceans 99(C5) (1994) 10143-10162"
    locator: the ensemble forecast of the error statistics and the ensemble form of the Kalman update
  - paper: doi:10.1175/1520-0493(1998)126<1719:ASITEK>2.0.CO;2
    title: "G. Burgers, P. J. van Leeuwen and G. Evensen, Analysis scheme in the ensemble Kalman filter, Monthly Weather Review 126(6) (1998) 1719-1724"
    locator: "the need to perturb the observations, and the expected analysis covariance (I - KH)P"
  - paper: doi:10.1175/1520-0493(1998)126<0796:DAUAEK>2.0.CO;2
    title: "P. L. Houtekamer and H. L. Mitchell, Data assimilation using an ensemble Kalman filter technique, Monthly Weather Review 126(3) (1998) 796-811"
    locator: an EnKF with perturbed observations for atmospheric data assimilation
  - paper: doi:10.1175/1520-0493(2001)129<0123:ASEKFF>2.0.CO;2
    title: "P. L. Houtekamer and H. L. Mitchell, A sequential ensemble Kalman filter for atmospheric data assimilation, Monthly Weather Review 129(1) (2001) 123-137"
    locator: the localized gain with a compactly supported correlation function
  - paper: doi:10.1007/s10492-011-0031-2
    title: "J. Mandel, L. Cobb and J. D. Beezley, On the convergence of the ensemble Kalman filter, Applications of Mathematics 56(6) (2011) 533-541"
    locator: convergence of the EnKF to the Kalman filter as N goes to infinity, for linear models
  - paper: doi:10.1175/1520-0493(2002)130<1913:EDAWPO>2.0.CO;2
    title: "J. S. Whitaker and T. M. Hamill, Ensemble data assimilation without perturbed observations, Monthly Weather Review 130(7) (2002) 1913-1924"
    locator: the sampling error that the perturbed observations add
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: "K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189"
    locator: the notation used here
---

The ensemble Kalman filter (EnKF) is a Monte Carlo form of the [Kalman filter](/kalman-filter/) for large and nonlinear models. It keeps an ensemble of $N$ model states. In the forecast step every member is run through the model, so the ensemble carries the error statistics forward with no tangent linear model and no $n \times n$ covariance matrix. In the analysis step the sample covariance of the ensemble takes the place of the forecast covariance in the Kalman gain, and each member moves towards its own randomly perturbed copy of the observations. The perturbations are needed: without them the analysis spread is too small. With [localization](/covariance-localization/) a few tens of members can be enough for a model with many more variables, as the measurement below shows for a small model.

## In plain words

Instead of carrying one best guess and a large table of its error variances, carry a few dozen possible states and run each through the model. Their spread shows how uncertain the forecast is, and their joint variations show which variables go up and down together. When observations arrive, each member is pulled towards the data by the amount that the Kalman rule gives for that spread. Each member sees a slightly different, randomly disturbed copy of the data. This keeps the cloud of members as wide as the uncertainty after the update really is.

## The problem

**Input.** A forecast ensemble $x_1, \ldots, x_N \in \mathbb R^n$, observations $y^o \in \mathbb R^p$, an observation operator $H$ (it may be nonlinear), a symmetric positive definite observation error covariance $R$, a source of random numbers, and optional localization weights. The notation is that of Ide, Courtier, Ghil and Lorenc (1997). In the letters of the [Kalman filter](/kalman-filter/) page, $H$ is its $C$, the model $M$ is its $A$, the forecast $x^f$ and $P^f$ are its predicted $m^-$ and $P^-$, and the analysis $x^a$ and $P^a$ are its filtered $m$ and $P$.

**Output.** An analysis ensemble. For a linear $H$ and no localization, its mean is the Kalman mean $\bar x + K(y^o - H\bar x)$ plus $K$ times the mean of the perturbations, and its expected sample covariance is $(I - KH)P^f$, where $P^f$ is the sample covariance of the forecast and $K = P^f H^\top(HP^fH^\top + R)^{-1}$.

## The algorithm

The forecast step runs each member through the model, $x^f_i \leftarrow M(x^a_i)$, usually followed by [covariance inflation](/covariance-inflation/). The analysis step is below. $X$ and $Y$ hold the unscaled perturbations of the state and of the predicted observations.

```pseudo id=main
EnKF-ANALYSIS(x_1..x_N, y^o, H, R)
L1  y_i <- H(x_i) for each member i
L2  xbar, ybar <- means; X, Y <- perturbations
L3  PH^T <- X Y^T / (N - 1); HPH^T <- Y Y^T / (N - 1)   ▷ times the weights, if localized
L4  draw ε_i ~ N(0, R) for each member i
L5  S <- HPH^T + R
L6  d_i <- y^o + ε_i - y_i
L7  x^a_i <- x_i + PH^T S^-1 d_i for each member i
L8  return x^a_1..x^a_N
```

Line L3 is where the ensemble replaces the covariance. For a linear $H$ the two products are exactly $P^fH^\top$ and $HP^fH^\top$, and the full $n \times n$ matrix $P^f$ is never formed. Line L4 draws a new perturbation for each member and each analysis. Line L7 solves one $p \times p$ system with $N$ right sides.

## Example

Take two members $x = (-1, 1)$, a scalar state observed directly with $y^o = 1$ and $R = 1$, and the perturbations $\varepsilon = (-1/2, 1/2)$. The sample variance is $P^f = 2$, so $K = 2/3$. Line L7 gives $x^a_1 = -1 + \tfrac23(1 - \tfrac12 + 1) = 0$ and $x^a_2 = 1 + \tfrac23(1 + \tfrac12 - 1) = 4/3$. The mean $2/3$ is the Kalman mean, because the perturbations have mean zero. The variance is $8/9$, while the Kalman value is $(1 - K)P^f = 2/3$: with only two members the perturbations add sampling error. Over many draws of $\varepsilon$ the expected variance is $2/3$ (Theorem 3 of the proof).

For the check value of the page group: with two members $\mp 1/\sqrt 2$ (sample mean $0$, variance $1$), $y^o = 1$ and $R = 1$, the mean and the variance over 20000 draws of the perturbations were $0.5$ and $0.5$ within $0.01$.

**A measurement.** On the [Lorenz-96 model](/lorenz-96-model/) with $n = 40$, $F = 8$, RK4 with step $0.05$, every other variable observed every $0.05$ time units with $R = I$, $N = 20$, multiplicative inflation $\rho$ of the forecast covariance and a [Gaspari-Cohn](/gaspari-cohn-function/) weight with half-width $c$ grid units on the gain, the mean analysis RMSE over cycles 501 to 1500 was (one seed, about 3 ms for each analysis in pure Python):

| $c$ | $\rho$ | RMSE |
|---|---|---|
| 4 | 1.02 | 0.398 |
| 4 | 1.05 | 0.384 |
| 4 | 1.1 | 0.409 |
| 6 | 1.05 | 0.352 |
| 8 | 1.02 | 1.486 |
| 8 | 1.05 | 0.347 |
| 8 | 1.1 | 0.355 |
| 10 | 1.1 | 0.345 |
| none | 1.2 | 4.65 |
| none | 1.5 | 4.85 |

The free ensemble mean has an RMSE of about $3.7$. On the same runs the [serial EnSRF](/ensemble-square-root-filter/) had $0.373$ with $c = 4$ and $\rho = 1.02$, and without localization it reached $0.409$ with $\rho = 1.2$, where the EnKF fails. The noise of the perturbed observations costs accuracy, most of all with weak localization.

## Correctness

The [proof](proofs/correctness.md) shows for a linear $H$ that line L3 gives the Kalman gain of the sample prior (Lemma 1), that the analysis mean is the Kalman mean plus $K\bar\varepsilon$ (Lemma 2), and that for independent draws $\varepsilon_i \sim N(0, R)$ the expected analysis covariance is $(I - KH)P^f$ (Theorem 3, from Burgers, van Leeuwen and Evensen 1998). Without the perturbations the covariance is too small by $KRK^\top$ (Corollary 4). For a linear model, Mandel, Cobb and Beezley (2011) prove that the EnKF converges to the Kalman filter as $N \to \infty$. For a finite ensemble, a nonlinear model or localization, the filter is an approximation whose quality is measured, not proved. The update is linear in the data, so for non-Gaussian errors it is not the Bayesian update. A [particle filter](/particle-filter/) aims at the Bayesian posterior, at a much higher cost.

## Complexity

Line L3 costs $\Theta(Np(n + p))$, lines L5 to L7 cost $\Theta(p^3 + p^2N + npN)$, and line L1 costs $N$ calls of $H$. So one analysis costs $\Theta(Np(n + p) + p^3)$. The extra space is $\Theta(np + p^2)$ for the two covariance blocks and $\Theta(N(n + p))$ for the ensembles. The forecast costs $N$ model runs, which usually dominates. With localization, the observations can be processed in local batches, which removes the $p^3$ term.

## Properties

- **Randomized.** The analysis depends on the draws of the perturbations. Two runs with different seeds give different members.
- **Derivative free.** It needs no tangent linear or adjoint model, unlike the [extended Kalman filter](/extended-kalman-filter/).
- **Exact in expectation.** For a linear $H$ the expected analysis mean and covariance are the Kalman values for the sample prior.
- **Low rank.** Without localization the analysis stays in $\bar x + \mathrm{span}(X)$, because the gain $XY^\top S^{-1}/(N - 1)$ has its columns in the span of the forecast perturbations.
- **Consistent as $N \to \infty$.** For linear Gaussian models the filter converges to the Kalman filter.
- **Parallel forecast.** The members are run through the model independently.

## Variants and improvements

- **Square root filters.** The [EnSRF](/ensemble-square-root-filter/), the [EAKF](/ensemble-adjustment-kalman-filter/) and the [ETKF](/ensemble-transform-kalman-filter/) replace the perturbed observations by a deterministic transform, which removes the sampling noise.
- **Localization.** Multiply $PH^\top$ and $HPH^\top$ entry by entry by a [Gaspari-Cohn](/gaspari-cohn-function/) weight of the distance, as Houtekamer and Mitchell (2001) did. For an $H$ that picks grid values this is the Kalman gain of the localized covariance $\rho\circ P^f$. See [covariance localization](/covariance-localization/).
- **Inflation.** Multiply the forecast perturbations by $\sqrt\rho$ or add noise, see [covariance inflation](/covariance-inflation/).
- **Centred perturbations.** Subtract the mean of the $\varepsilon_i$ before line L6, so the mean is the Kalman mean exactly.
- **Smoothing.** The [ensemble Kalman smoother](/ensemble-kalman-smoother/) applies the same update to past states.
- **Inverse problems.** [Ensemble Kalman inversion](/ensemble-kalman-inversion/) applies the update in an artificial time to estimate parameters.

## When to use it

Use the EnKF when the model is large and nonlinear, when no adjoint model is available, and when a flow dependent estimate of the forecast error is needed. It is simple to code around an existing model. If the extra noise of the perturbed observations matters, as with small ensembles or weak localization, use a square root filter. For strongly non-Gaussian errors with a small state, a particle filter may be better. For a small linear model, use the [Kalman filter](/kalman-filter/) itself.

## Pitfalls

- **No perturbed observations (line L4).** Using the same $y^o$ for every member gives the covariance $(I - KH)P(I - KH)^\top$, which is too small. The filter then trusts its forecast too much and can stop using the data.
- **Perturbations with the wrong covariance (line L4).** The perturbations must be drawn from $N(0, R)$ with the same $R$ that is in $S$. With a correlated $R$, use a Cholesky factor to draw them.
- **Small ensembles without localization (line L3).** With $N$ much smaller than $n$, the sample covariance has spurious long range correlations. Distant observations then change the state where they should not. In the measurement, no inflation factor made the filter work without localization.
- **Spread collapse.** The sample error makes the ensemble too confident over many cycles. Use [inflation](/covariance-inflation/).
- **Forming $P^f$.** For large $n$ the $n \times n$ matrix does not fit in memory. Line L3 forms only the $n \times p$ and $p \times p$ blocks.
- **A singular $S$ (line L7).** If the localization weights of the observations are not positive semidefinite, $S$ can lose positive definiteness. Weights from a valid correlation function such as Gaspari-Cohn avoid this.

## Implementations

## History

Evensen proposed the ensemble Kalman filter in 1994 for a quasi-geostrophic ocean model, as a way to forecast the error statistics by Monte Carlo instead of with the extended Kalman filter. In 1998 Burgers, van Leeuwen and Evensen showed that the observations must be perturbed to give the right analysis spread, and in the same year Houtekamer and Mitchell used an EnKF with perturbed observations for atmospheric data assimilation. In 2001 Houtekamer and Mitchell localized the gain with a compactly supported correlation. The square root filters of 2001 to 2003 removed the perturbed observations. In 2011 Mandel, Cobb and Beezley proved that the filter converges to the Kalman filter for linear models as the ensemble grows.

## References
