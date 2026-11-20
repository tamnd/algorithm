---
tag: 1PA4A0
kind: technique
slug: covariance-inflation
name: Covariance inflation
aliases:
- multiplicative inflation
area: scientific-computing/data-assimilation
level: core
summary: Enlarges the ensemble spread by a factor or by added noise to offset the underestimated error from sampling and model error.
prereqs: [ensemble-kalman-filter, covariance-matrix]
see_also: [covariance-localization, ensemble-transform-kalman-filter, ensemble-square-root-filter, local-ensemble-transform-kalman-filter, ensemble-kalman-smoother, kalman-filter, lorenz-96-model]
sources:
  - paper: doi:10.1175/1520-0493(1999)127<2741:AMCIOT>2.0.CO;2
    title: "J. L. Anderson and S. L. Anderson, A Monte Carlo implementation of the nonlinear filtering problem to produce ensemble assimilations and forecasts, Monthly Weather Review 127(12) (1999) 2741-2758"
    locator: the inflation of the prior ensemble about its mean
  - paper: doi:10.1175/1520-0493(2004)132<1238:IOIEAO>2.0.CO;2
    title: "F. Zhang, C. Snyder and J. Sun, Impacts of initial estimate and observation availability on convective-scale data assimilation with an ensemble Kalman filter, Monthly Weather Review 132(5) (2004) 1238-1253"
    locator: the relaxation of the analysis perturbations to the prior perturbations
  - paper: doi:10.1175/MWR-D-11-00276.1
    title: "J. S. Whitaker and T. M. Hamill, Evaluating methods to account for system errors in ensemble data assimilation, Monthly Weather Review 140(9) (2012) 3078-3089"
    locator: the relaxation of the analysis spread to the prior spread, compared with additive and multiplicative inflation
  - paper: doi:10.1111/j.1600-0870.2006.00216.x
    title: "J. L. Anderson, An adaptive covariance inflation error correction algorithm for ensemble filters, Tellus A 59(2) (2007)"
    locator: the Bayesian estimate of the inflation factor from the observations at each analysis time
  - paper: doi:10.1111/j.1600-0870.2008.00361.x
    title: "J. L. Anderson, Spatially and temporally varying adaptive covariance inflation for ensemble filters, Tellus A 61(1) (2009) 72-83"
    locator: the adaptive inflation with a separate factor for each state variable
  - paper: doi:10.1002/qj.371
    title: "H. Li, E. Kalnay and T. Miyoshi, Simultaneous estimation of covariance inflation and observation errors within an ensemble Kalman filter, Quarterly Journal of the Royal Meteorological Society 135(639) (2009) 523-533"
    locator: the estimate of the inflation factor from the observation-minus-forecast statistics, together with the observation errors
  - paper: doi:10.2151/jmsj1965.75.1B_181
    title: "K. Ide, P. Courtier, M. Ghil and A. C. Lorenc, Unified notation for data assimilation, operational, sequential and variational, Journal of the Meteorological Society of Japan 75(1B) (1997) 181-189"
    locator: the notation of the data assimilation pages
---

Covariance inflation makes the spread of an ensemble larger before or after an analysis. An ensemble filter such as the [ensemble Kalman filter](/ensemble-kalman-filter/) uses the sample covariance of a few members as the error covariance of its forecast. With few members this covariance is usually too small, and a model with errors makes it smaller still. A filter that believes its forecast too much gives the observations too little weight and can lose the truth. Inflation corrects this in one of three ways: it multiplies the perturbations by a factor, it adds random noise to the members, or it moves the analysis perturbations back towards the forecast perturbations. The factors are tuned in experiments or estimated from the observations.

## In plain words

An ensemble says how unsure the forecast is by how much its members differ. A small ensemble is often too sure of itself. Then the filter trusts the forecast and ignores new observations, and the error grows without the filter noticing. Inflation spreads the members a little further apart, so the filter keeps listening to the data. You can stretch the members away from their mean, add a little noise to each one, or undo part of the shrinking that the analysis did. How much to inflate is found by trial, or from how far the observations are from the forecast.

## When it applies

- An ensemble filter or smoother with fewer members than the number of growing directions of the model.
- A model with errors that the ensemble does not simulate, so the forecast spread is smaller than the forecast error.
- The analysis RMSE is much larger than the ensemble spread, or the spread falls to near zero after many cycles while the error does not.
- A filter that diverges: the gain goes to zero and the analysis stops following the observations.

## The template

$\bar x$ is the ensemble mean, $x_i' = x_i - \bar x$ the perturbation of member $i$, and $\sigma_j$ the ensemble standard deviation of variable $j$. The holes are the factor $\lambda$, the additive covariance $Q$ and the relaxation weight $\alpha$. In the notation of Ide, Courtier, Ghil and Lorenc (1997), $f$ marks the forecast and $a$ the analysis.

```pseudo id=main
CYCLE(x_1..x_N)
L1  x_i <- M(x_i) for each member                         ▷ forecast
L2  multiplicative: x_i <- xbar + lambda (x_i - xbar)    ▷ hole: lambda >= 1
L3  additive: x_i <- x_i + q_i, q_i ~ N(0, Q)            ▷ hole: Q
L4  x^a_i <- ANALYSIS(x_i, y^o)                           ▷ any ensemble filter
L5  RTPP: x'^a_i <- (1 - alpha) x'^a_i + alpha x'^f_i     ▷ hole: alpha in [0, 1]
L6  RTPS: x'^a_i <- x'^a_i (1 + alpha (sigma^f - sigma^a) / sigma^a), for each variable
```

A filter uses one or two of lines L2, L3, L5 and L6, not all of them.

- **Line L2 (multiplicative).** The mean stays the same and the sample covariance becomes $\lambda^2P^f$. All correlations stay the same. This page writes $\lambda$ for the factor on the perturbations and $\rho = \lambda^2$ for the factor on the covariance. The filter pages of this site, for example the [ETKF](/ensemble-transform-kalman-filter/), use $\rho$, the factor on the covariance. Papers use both conventions, so check which one a stated value means.
- **Line L3 (additive).** In expectation the sample covariance becomes $P^f + Q$, because the noise is independent of the members. The mean also moves, by noise with the covariance $Q/N$. $Q$ can have a structure, for example the differences between model states, and so add spread in directions that the ensemble does not have.
- **Line L5 (relaxation to prior perturbations, RTPP).** The analysis perturbations are mixed with the forecast perturbations, member by member. The mean stays the analysis mean. With $\alpha = 1$ the spread is not reduced at all.
- **Line L6 (relaxation to prior spread, RTPS).** For each variable, the analysis perturbations are scaled so that the new standard deviation is $(1 - \alpha)\sigma^a + \alpha\sigma^f$. The correlations of the analysis stay the same. Where the observations reduced the spread most, the inflation is largest.

**Adaptive inflation.** If the forecast mean has the error covariance $\rho HP^fH^\top$ in observation space and the observation errors are independent of it with the covariance $R$, the innovation $d = y^o - H\bar x^f$ has $\mathbb E[dd^\top] = \rho HP^fH^\top + R$ for a linear $H$. Take the trace:

$$\rho \approx \frac{d^\top d - \operatorname{tr}R}{\operatorname{tr}(HP^fH^\top)}.$$

Li, Kalnay and Miyoshi (2009) estimate the factor from these statistics, together with the observation errors, and average the noisy values over time. Anderson (2007) treats the factor as a random variable and updates its distribution with the observations at each time. Anderson (2009) gives each state variable its own factor.

**A worked example.** Take the random walk $x_{t+1} = x_t + w_t$ with $w_t \sim N(0, 1/2)$, observed with $H = 1$ and $R = 1$ at every step. The [Kalman filter](/kalman-filter/) reaches a steady state with $P^f = P^a + 1/2$ and $P^a = P^f/(P^f + 1)$. These give $P^f = 1$, $P^a = 1/2$ and the gain $1/2$. An ensemble whose model ignores $w_t$ has the forecast variance $P^a = 1/2$ instead of $1$.

- Without inflation, the variances are $P^f_k = 1/(k + 1)$ and $P^a_k = 1/(k + 2)$ after $k$ analyses. The gain $1/(k + 2)$ goes to zero. The filter then averages the observations as if the state were constant, and it does not follow the random walk.
- Multiplicative inflation with $\rho = \lambda^2 = 2$ makes the forecast variance $2 \cdot 1/2 = 1$, which is the steady state of the Kalman filter.
- Additive inflation with $Q = 1/2$ gives the same variance in expectation.
- The adaptive estimate gives the same factor: the true forecast error variance is $1$, so $\mathbb E[d^2] = 1 + 1 = 2$ and $(2 - 1)/(1/2) = 2$.

**Measurements on the other pages.** On the [Lorenz-96 model](/lorenz-96-model/) with $n = 40$ and $N = 20$, the [EnKF](/ensemble-kalman-filter/) with localization half-width $c = 8$ had the RMSE $1.486$ with $\rho = 1.02$ and $0.347$ with $\rho = 1.05$. Without localization the EnKF failed even with $\rho = 1.5$, and the [ETKF](/ensemble-transform-kalman-filter/) and the [EnSRF](/ensemble-square-root-filter/) needed $\rho = 1.2$. So the right factor depends strongly on the ensemble size and on the localization.

## Classic examples

- [Ensemble Kalman filter](/ensemble-kalman-filter/): multiplicative inflation of the forecast before the analysis with perturbed observations.
- [Ensemble square root filter](/ensemble-square-root-filter/): the deterministic analysis reduces the spread exactly as the Kalman filter does, so all the missing spread from sampling and model error must come from inflation.
- [Ensemble transform Kalman filter](/ensemble-transform-kalman-filter/): the factor enters the transform as the prior term $(N - 1)/\rho$, so no member must be changed before the analysis.
- [Local ensemble transform Kalman filter](/local-ensemble-transform-kalman-filter/): the same factor in each local analysis. Adaptive methods can give each grid point its own factor.
- [Ensemble Kalman smoother](/ensemble-kalman-smoother/): only the current forecast is inflated, not the stored past ensembles.
- [Ensemble Kalman inversion](/ensemble-kalman-inversion/): inflation keeps the ensemble from collapsing before the misfit is small.

## Variations

- **Inflation of the analysis.** Line L2 can be applied after the analysis instead of before. For a linear model, inflating the analysis by $\rho$ gives the same next forecast covariance as inflating that forecast by $\rho$.
- **Spatially varying factors.** A separate factor for each variable or region, as in Anderson (2009), inflates more where the observations are dense.
- **Additive inflation from model differences.** Samples of differences between model states, or of model tendencies, can serve as the $q_i$ when the model error has structure.
- **Combinations.** Whitaker and Hamill (2012) found that RTPS together with additive inflation worked better than either method alone.

## Pitfalls

- **Perturbations or covariance (line L2).** A factor of $1.1$ on the perturbations is $1.21$ on the covariance. Mixing the two conventions changes the inflation by much more than the range of values that work.
- **Inflating twice.** A factor in the transform of the ETKF and a factor on the members in the same cycle multiply. Use one place.
- **Too much inflation.** A large factor gives too much weight to noisy observations and makes the analysis noisy. The RMSE grows again past the best factor.
- **Inflation of the mean (line L3).** Additive noise also moves the ensemble mean. Remove the mean of the $q_i$ if the mean must not change.
- **Zero spread (line L6).** RTPS divides by $\sigma^a$. A variable with no spread cannot be inflated by a multiplicative method; only additive noise helps there.
- **Adaptive estimates with a wrong $R$.** The estimate of $\rho$ assumes that $R$ is right. If $R$ is too small, the estimate of $\rho$ is too large, which is why Li, Kalnay and Miyoshi estimate both.

## References
