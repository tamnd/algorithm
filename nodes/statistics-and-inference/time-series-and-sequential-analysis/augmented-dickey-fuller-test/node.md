---
tag: 61BK07
kind: algorithm
slug: augmented-dickey-fuller-test
name: Augmented Dickey-Fuller test
aliases:
- ADF test
- Dickey-Fuller test
- unit root test
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: Tests the null of a unit root by the t-statistic of the lagged level in a regression of differences, with lagged differences added. Its null law is nonstandard.
model: real-ram
complexity:
  vars: {n: the length of the series, k: the number of regressors (the lagged level plus deterministic terms plus lagged differences)}
  time: {worst: Θ(n k^2), best: Θ(n k^2)}
  space: {extra: Θ(n k)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1979
  people: [David A. Dickey, Wayne A. Fuller]
  note: Dickey and Fuller (1979) derived the null law of the least squares estimator and t ratio in an autoregression with a unit root. Said and Dickey (1984) added lagged differences so that the test works for ARMA errors of unknown order.
prereqs: [stationary-process, arima-model, ordinary-least-squares, statistical-hypothesis-test]
see_also: [kpss-test, engle-granger-test, johansen-test, autoregressive-model, akaike-information-criterion, bayesian-information-criterion, change-point-detection, block-bootstrap]
sources:
  - book: isbn:9780691042893
    title: James D. Hamilton, Time Series Analysis, Princeton University Press, 1994
    locator: Chapter 17 (univariate processes with unit roots), the four cases of the Dickey-Fuller regression and the augmented test
  - book: isbn:9780471552390
    title: Wayne A. Fuller, Introduction to Statistical Time Series, second edition, Wiley, 1996
    locator: the chapter on unit root and explosive time series, with the tables of the Dickey-Fuller percentiles
  - paper: doi:10.1080/01621459.1979.10482531
    title: David A. Dickey and Wayne A. Fuller, Distribution of the estimators for autoregressive time series with a unit root, Journal of the American Statistical Association 74(366) (1979), pages 427 to 431
    locator: the limit laws of the coefficient and t statistics in the three regressions
  - paper: doi:10.1093/biomet/71.3.599
    title: Said E. Said and David A. Dickey, Testing for unit roots in autoregressive-moving average models of unknown order, Biometrika 71(3) (1984), pages 599 to 607
    locator: the augmented regression with a number of lags that grows with n
  - paper: "James G. MacKinnon, Critical values for cointegration tests, Queen's Economics Department Working Paper No. 1227, Queen's University, 2010"
    title: MacKinnon 2010
    locator: "Table 2, the response surface coefficients for one variable (N = 1), cases nc, c and ct"
  - paper: "doi:10.1002/(SICI)1099-1255(199611)11:6<601::AID-JAE417>3.0.CO;2-T"
    title: James G. MacKinnon, Numerical distribution functions for unit root and cointegration tests, Journal of Applied Econometrics 11(6) (1996), pages 601 to 618
    locator: response surface p-values for the Dickey-Fuller statistics
  - paper: doi:10.1080/07350015.1989.10509723
    title: G. William Schwert, Tests for unit roots, a Monte Carlo investigation, Journal of Business and Economic Statistics 7(2) (1989), pages 147 to 159
    locator: the size distortion under a negative moving-average root and the rule for the maximum lag
---

The augmented Dickey-Fuller (ADF) test decides whether a time series has a unit root, that is, whether it behaves like a random walk that never returns to a fixed mean. It regresses the first difference $\nabla X_t$ on the lagged level $X_{t-1}$, on deterministic terms (none, a constant, or a constant and a linear trend) and on $p$ lagged differences, and uses the ordinary t ratio $\tau$ of the coefficient of $X_{t-1}$. The null hypothesis is a unit root. The alternative is a stationary (or trend-stationary) autoregression. Under the null, $\tau$ does not have a t or normal law: its limit is a functional of Brownian motion, with 5% points of about $-1.94$, $-2.86$ and $-3.41$ for the three choices of deterministic terms. The lagged differences absorb short-run correlation so that the same table applies to any stationary ARMA dynamics in the differences.

## In plain words

Some series wander. A stock price or the level of a lake can drift away and never feel a pull back to an average. Other series move around a fixed level and always come back. The test asks which kind you have. It looks at how today's change depends on yesterday's level. If high levels are followed by falls and low levels by rises, there is a pull back to a center, and the series is stable. If the level tells you nothing about the next change, the series wanders. The difficulty is that a wandering series fools the usual tables: the pull back looks stronger than it is. So the test uses its own table of cut-off values, built by simulating wandering series. A few past changes are added to the fit so that short-term patterns do not confuse the answer.

## The problem

**Model and hypotheses.** The observed series is $X_t = d_t + U_t$, $t = 1, \dots, n$, where $d_t$ is a deterministic term (zero, a constant $a$, or a line $a + bt$) and $U_t$ is an autoregression $\phi(B)U_t = \varepsilon_t$ of order $p + 1$, with $\phi(z) = 1 - \phi_1 z - \dots - \phi_{p+1}z^{p+1}$, $B$ the backshift operator and $\varepsilon_t \sim \mathrm{WN}(0, \sigma^2)$ as on the [ARMA model](/arma-model/) page. Any such autoregression can be rewritten exactly as
$$\nabla U_t = \rho U_{t-1} + \sum_{i=1}^{p}\gamma_i \nabla U_{t-i} + \varepsilon_t, \qquad \rho = -\phi(1), \qquad \gamma_i = -\sum_{j=i+1}^{p+1}\phi_j.$$
The null hypothesis is $H_0: \rho = 0$, which holds exactly when $z = 1$ is a root of $\phi$. Then $X_t$ is integrated of order one, an [ARIMA](/arima-model/) process with $d = 1$. The alternative is $H_1: \rho < 0$, which holds whenever all roots of $\phi$ lie outside the unit circle, so that $U_t$ is a [stationary process](/stationary-process/) and $X_t$ is stationary around $d_t$. The test is one-sided: explosive roots ($\rho > 0$) are not part of the alternative.

**Statistic.** Fit by [ordinary least squares](/ordinary-least-squares/), over $t = p + 2, \dots, n$ (so $T = n - p - 1$ rows),
$$\nabla X_t = \rho X_{t-1} + \delta^\top d^*_t + \sum_{i=1}^{p}\gamma_i \nabla X_{t-i} + e_t,$$
where $d^*_t$ is empty (case "n"), $1$ (case "c") or $(1, t)$ (case "ct"). The statistic is the t ratio $\tau = \hat\rho/\operatorname{se}(\hat\rho)$, with $\operatorname{se}(\hat\rho) = s\sqrt{[(Z^\top Z)^{-1}]_{11}}$, $Z$ the $T \times k$ regressor matrix and $s^2 = \sum e_t^2/(T - k)$. The deterministic terms in the regression must contain those in the model: case "c" covers $d_t = a$, and case "ct" covers $d_t = a + bt$ and also a random walk with drift.

**Null distribution.** Asymptotic and nonstandard. In case "n" with $p = 0$ and iid errors, Dickey and Fuller (1979) showed
$$T\hat\rho \Rightarrow \frac{W(1)^2 - 1}{2\int_0^1 W(r)^2\,dr}, \qquad \tau \Rightarrow \frac{W(1)^2 - 1}{2\left(\int_0^1 W(r)^2\,dr\right)^{1/2}},$$
where $W$ is a standard Brownian motion. In cases "c" and "ct", $W$ is replaced by its residual after projection on $1$ or on $(1, r)$. Said and Dickey (1984) showed that the same limits hold for ARMA errors when $p \to \infty$ with $p^3/T \to 0$. These limits are cited, not proved here. In finite samples the law of $\tau$ is exact by simulation in one case: with Gaussian errors and $p = 0$, $\tau$ in cases "c" and "ct" does not depend on the start value, the scale or (in case "ct") the drift, so a simulation from a standard Gaussian random walk gives the exact null law at every $n$, up to Monte Carlo error. This is proved below.

**Rejection rule and size.** Reject $H_0$ at level $\alpha$ when $\tau < c_\alpha(T)$, with the response surface of MacKinnon (2010), $c_\alpha(T) = \beta_0 + \beta_1/T + \beta_2/T^2 + \beta_3/T^3$. Some values:

| case | $T = 25$, 1% / 5% / 10% | $T = 100$ | $T = \infty$ |
|---|---|---|---|
| "n" | $-2.661$ / $-1.955$ / $-1.609$ | $-2.588$ / $-1.944$ / $-1.614$ | $-2.566$ / $-1.941$ / $-1.617$ |
| "c" | $-3.724$ / $-2.986$ / $-2.633$ | $-3.498$ / $-2.891$ / $-2.582$ | $-3.430$ / $-2.862$ / $-2.567$ |
| "ct" | $-4.375$ / $-3.603$ / $-3.238$ | $-4.052$ / $-3.455$ / $-3.153$ | $-3.959$ / $-3.410$ / $-3.127$ |

The standard normal 5% point is $-1.645$, far to the right of these. The size is asymptotically $\alpha$. In finite samples it depends on how well the $p$ lags capture the short-run dynamics.

**p-value.** $p = P(\tau_\infty \le \tau)$ for the limiting law. MacKinnon (1996) gives response surface approximations. The implementation gives a Monte Carlo p-value $(1 + \#\{\tau^{(r)} \le \tau\})/(1 + R)$ from $R$ simulated Gaussian random walks of the same length, which is exact for Gaussian errors with $p = 0$ in cases "c" and "ct".

**Sensitivity and power.** The test detects a pull toward the mean, $\rho < 0$. Under a fixed stationary alternative $T\hat\rho \to -\infty$ and the power tends to 1. Near the unit root the power is low: for an AR(1) with $\phi_1 = 0.9$ and $n = 100$, case "c" without lags rejects at 5% in about a third of samples. Large negative moving-average terms in $\nabla X_t$ inflate the size, because the series then looks stationary over short spans.

## The algorithm

```pseudo id=main
ADF(X₁..Xₙ, case, p)                     ▷ case ∈ {n, c, ct}, p lagged differences
L1  for t ← 2 to n: D_t ← X_t − X_{t−1}
L2  T ← n − p − 1
L3  for t ← p + 2 to n:                      ▷ one row per usable time point
L4      z_t ← (X_{t−1}, d*_t, D_{t−1}, …, D_{t−p});  response D_t
L5  Z = QR, with Q of size T×k and R upper triangular   ▷ Gram-Schmidt or Householder
L6  β̂ ← R⁻¹ Qᵀ D;  e ← D − Z β̂;  s² ← eᵀe / (T − k)
L7  se ← s · ‖row 1 of R⁻¹‖                ▷ [(ZᵀZ)⁻¹]₁₁ = Σ_c (R⁻¹)₁c²
L8  τ ← β̂₁ / se
L9  c ← β₀ + β₁/T + β₂/T² + β₃/T³           ▷ MacKinnon (2010), for case and α
L10 return (τ, c, reject ⇔ τ < c)
```

The number of lags $p$ is chosen before line L1. The usual rule fits every $p$ from 0 to $p_{\max}$ on the same rows $t = p_{\max} + 2, \dots, n$, picks the $p$ that minimizes the [AIC](/akaike-information-criterion/) or [BIC](/bayesian-information-criterion/), $T\log(\mathrm{RSS}/T) + \text{penalty} \times k$, and then refits with that $p$ on all usable rows. A common choice is Schwert's $p_{\max} = \lfloor 12(n/100)^{1/4}\rfloor$, which is 12 at $n = 100$ and 14 at $n = 200$. Another is to start at $p_{\max}$ and drop the last lag while its t ratio is below 1.645 in absolute value.

## Example

**By hand.** Take $X = (3, 5, 4, 6, 8, 7, 9, 8)$, case "c" and $p = 0$. Then $T = 7$ and the regression is of $\nabla X_t$ on a constant and $X_{t-1}$:

| step | value |
|---|---|
| L1: $\nabla X_t$, $t = 2..8$ | $2, -1, 2, 2, -1, 2, -1$ (mean $5/7$) |
| L4: $X_{t-1}$ | $3, 5, 4, 6, 8, 7, 9$ (mean 6) |
| $S_{xx} = \sum (X_{t-1} - 6)^2$ | 28 |
| $S_{xd} = \sum (X_{t-1} - 6)(\nabla X_t - 5/7)$ | $-12$ |
| L6: $\hat\rho = S_{xd}/S_{xx}$, constant $5/7 - 6\hat\rho$ | $-3/7 = -0.4286$, $23/7$ |
| L6: residual sum of squares, $s^2 = \mathrm{RSS}/5$ | $72/7$, $72/35 = 2.0571$ |
| L7: $\operatorname{se} = \sqrt{s^2/S_{xx}}$ | 0.27105 |
| L8: $\tau$ | $-\sqrt{5/2} = -1.5811$ |
| L9: $c_{0.05}(7)$ | $-3.4776$ |

Since $-1.58 > -3.48$, the test does not reject the unit root. A one-sided t table with 5 degrees of freedom would put the cut-off at $-2.015$, which is far less strict. The Monte Carlo p-value from 9999 Gaussian random walks of length 8 is about 0.44.

**A random walk against a stationary series.** From the same 200 standard normal shocks (seed 2026), build a random walk $X_t = X_{t-1} + \varepsilon_t$ and an AR(1) series $X_t = 0.5X_{t-1} + \varepsilon_t$. With case "c", AIC lag selection and $p_{\max} = 14$:

| series | chosen $p$ | $T$ | $\tau$ | $c_{0.05}(T)$ | decision |
|---|---|---|---|---|---|
| random walk | 0 | 199 | $-1.99$ | $-2.876$ | keep $H_0$ |
| AR(1), $\phi_1 = 0.5$ | 2 | 197 | $-7.80$ | $-2.876$ | reject |

**Power and size.** With $n = 100$, case "c", $p = 0$ and 1000 samples each, the rejection rate at 5% is 1.000 for $\phi_1 = 0.5$, 0.868 for $\phi_1 = 0.8$, 0.336 for $\phi_1 = 0.9$, 0.128 for $\phi_1 = 0.95$ and 0.055 under the null $\phi_1 = 1$. These rates are measured, not derived.

## Correctness

Three facts are proved in the correctness proof. First, the ADF regression is an exact rewriting of an AR($p + 1$) model, with $\rho = -\phi(1)$, so $\rho = 0$ is the same as a unit root, and $\rho < 0$ holds for every causal stationary autoregression, because $\phi(0) = 1$ and $\phi$ has no zero on $[0, 1]$. Under the null, $\phi(z) = (1 - z)(1 - \sum\gamma_i z^i)$, so the lagged differences are exactly the autoregression of $\nabla X_t$. Second, lines L5 to L8 compute the ordinary least squares t ratio, because $Z = QR$ gives $\hat\beta = R^{-1}Q^\top D$ and $(Z^\top Z)^{-1} = R^{-1}R^{-\top}$. Third, $\tau$ does not change when $X_t$ is replaced by $a + c X_t$ with $c \ne 0$ in case "c", or by $a + bt + cX_t$ in case "ct", because the regressor span and the t ratio are unchanged. Under the null with Gaussian errors and $p = 0$ this makes the simulated law exact, and the Monte Carlo p-value has $P(p \le \alpha) \le \alpha$ for every $n$. The Dickey-Fuller limit law and the Said-Dickey extension are cited, not proved.

## Complexity

On a [real RAM](/real-ram/), one ADF regression with $T$ rows and $k$ regressors costs $\Theta(Tk^2)$ time for the QR factorization and $\Theta(k^3)$ for the triangular solves, so $\Theta(nk^2)$ in total since $T > k$. The design matrix takes $\Theta(nk)$ space. Lag selection over $p = 0, \dots, p_{\max}$ costs $\Theta(n p_{\max}^3)$ if every regression is refitted. Adding one column to an existing QR factorization costs $\Theta(Tk)$, which brings the search down to $\Theta(n p_{\max}^2)$. A Monte Carlo p-value with $R$ replicates costs $R$ more regressions.

**Numerical stability.** The level $X_{t-1}$ and the constant are nearly collinear when the series is far from 0 relative to its spread, and $Z^\top Z$ then has a large condition number. Forming the normal equations squares that condition number. The QR route in lines L5 to L7 works with $Z$ directly. In case "ct", the trend column $t$ and the level are also nearly collinear for a trending series. Centering the trend column ($t - \bar t$) changes neither $\hat\rho$ nor $\tau$, and it improves the conditioning.

## Properties

- **Exact rewriting.** The ADF regression is a reparametrization of an AR($p + 1$) with deterministic terms. Nothing is approximated when the true order is at most $p + 1$.
- **Invariant.** $\tau$ is unchanged by a change of level and scale (case "c"), and also by an added linear trend (case "ct"). In case "n" only a change of scale leaves it unchanged, so the start value matters.
- **Superconsistent under the null.** $\hat\rho - \rho = O_p(1/T)$, not $O_p(1/\sqrt T)$. The coefficients $\gamma_i$ of the stationary lags are still $\sqrt T$-consistent and asymptotically normal (Sims, Stock and Watson 1990).
- **Free of nuisance parameters in the limit.** With enough lags, the limit law of $\tau$ does not depend on $\gamma$ or on $\sigma^2$, so one table serves all ARMA dynamics. The finite-sample law does depend on them.
- **Consistent.** For a fixed stationary alternative the power tends to 1 as $n \to \infty$.
- **Low power near the unit root.** With $n = 100$, a root of 0.9 is detected only about a third of the time.

## Variants and improvements

- **Dickey-Fuller test.** The case $p = 0$. It is valid only when the differences are white noise under the null.
- **Coefficient test.** Use $T\hat\rho/(1 - \sum\hat\gamma_i)$ in place of $\tau$, with its own table. It has better power in some settings and worse size in others.
- **F tests for joint hypotheses.** Dickey and Fuller (1981) give likelihood ratio (F-type) statistics for $\rho = 0$ together with $b = 0$ or $a = 0$, with nonstandard tables.
- **Phillips-Perron test.** Keep $p = 0$ and correct $\tau$ for serial correlation with a nonparametric long-run variance (the same Bartlett kernel estimator as in the [KPSS test](/kpss-test/)). It handles heteroscedastic errors, but its size is poor under negative MA roots.
- **DF-GLS (Elliott, Rothenberg and Stock 1996).** Remove the deterministic terms by a quasi-difference GLS fit at a local alternative $\bar\rho = 1 - \bar c/T$, then run the ADF regression without deterministic terms. Its power is close to the Gaussian power envelope, and it is clearly better than the ADF test near the unit root.
- **Modified information criteria (Ng and Perron 2001).** A lag choice whose penalty depends on $\hat\rho$, which fixes much of the size distortion under negative MA roots.
- **Reversed null.** The [KPSS test](/kpss-test/) takes stationarity as the null. Running both tests separates "clearly stationary", "clearly a unit root" and "the data cannot tell".
- **Bootstrap.** Fit the AR model to $\nabla X_t$, resample its residuals, rebuild random walks, and recompute $\tau$. A [block bootstrap](/block-bootstrap/) of the differences is an alternative.
- **Residual-based cointegration test.** Applied to the residuals of a regression of one I(1) series on others, the same statistic is the [Engle-Granger test](/engle-granger-test/), with different critical values.

## When to use it

Use the ADF test before fitting an ARIMA model, to decide whether to difference, and before a regression of one trending series on another, to see whether the series are I(1) and the [Engle-Granger](/engle-granger-test/) or [Johansen](/johansen-test/) machinery is needed. Choose case "ct" when the series has a visible trend, case "c" when it has a nonzero level and no trend, and case "n" only when theory fixes the mean at 0. For short series near the unit root, prefer DF-GLS, and report the KPSS result as well.

## Pitfalls

- **Normal or t tables.** The 5% point in case "c" is $-2.86$, not $-1.645$. Using a t table rejects the unit root far too often.
- **Wrong deterministic terms.** If the series has a trend and the regression has only a constant, $\tau$ almost never rejects even when the series is trend-stationary. If a random walk has a drift and the regression has only a constant, $\tau$ is asymptotically normal (West 1988), and the Dickey-Fuller table is wrong. With a drift of 1 per step and $n = 100$, case "c" rejected in 0.4% of samples at the nominal 5% level. Use case "ct" for drifting series.
- **Too few lags.** If $\nabla X_t$ is an MA(1) with $\theta = -0.8$, the test with $p = 0$ and $n = 100$ rejects the true unit root in almost every sample. Even with AIC lag selection it rejected in 45% of samples at the nominal 5% level (400 samples; Schwert 1989 reports the same pattern).
- **Too many lags.** Each extra lag costs one observation and some power. Do not fix $p$ large out of caution.
- **Different rows for different lags.** Information criteria must compare fits on the same rows. Comparing a $p = 2$ fit on $n - 3$ rows with a $p = 10$ fit on $n - 11$ rows biases the choice.
- **Structural breaks.** A single shift in level or slope makes a stationary series look like a random walk, and the test then fails to reject (Perron 1989). Look for breaks with [change-point detection](/change-point-detection/) and use a test that allows them.
- **Reading "not rejected" as "unit root".** Failing to reject means the data do not exclude a unit root. A root of 0.95 and a root of 1 are hard to tell apart with 100 observations.

## Implementations

## History

The unit root problem became central in econometrics in the 1970s, when it was noticed that regressions of one trending series on another often gave large t ratios by chance (Granger and Newbold 1974). David Dickey and Wayne Fuller derived the null distributions in Dickey's 1976 thesis at Iowa State; the tables were printed in Fuller's 1976 textbook, and the limit laws appeared in their 1979 paper in the Journal of the American Statistical Association. Their 1981 paper in Econometrica added likelihood ratio tests. Said and Dickey (1984) showed that adding lagged differences extends the test to ARMA errors of unknown order. Nelson and Plosser (1982) applied it to fourteen US macroeconomic series and could not reject a unit root in most, which started a long debate about trends in economic data. Phillips (1987) gave the Brownian motion form of the limits under weak conditions, and MacKinnon (1991, 1996, 2010) replaced the original tables with response surfaces fitted to large simulations.

## References
