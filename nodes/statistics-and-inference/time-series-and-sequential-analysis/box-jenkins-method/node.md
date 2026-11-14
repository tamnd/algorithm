---
tag: ZCWDR4
kind: technique
slug: box-jenkins-method
name: Box-Jenkins method
aliases:
- Box-Jenkins approach
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: The cycle of identifying an ARIMA model from the ACF and PACF, estimating it, and checking its residuals, repeated until the residuals look like white noise.
prereqs: [arima-model, partial-autocorrelation-function, ljung-box-test, autocorrelation]
see_also: [augmented-dickey-fuller-test, kpss-test, akaike-information-criterion, box-cox-transformation, innovations-algorithm, yule-walker-equations, holt-winters-method, stl-decomposition]
sources:
  - book: isbn:9780816210947
    title: "George E. P. Box and Gwilym M. Jenkins, Time Series Analysis: Forecasting and Control, Holden-Day, 1970"
    locator: the iterative cycle of model identification, estimation and diagnostic checking (the first edition)
  - book: isbn:9781118675021
    title: "George E. P. Box, Gwilym M. Jenkins, Gregory C. Reinsel and Greta M. Ljung, Time Series Analysis: Forecasting and Control, fifth edition, Wiley, 2015"
    locator: Part II (stochastic model building, with the chapters on identification, estimation and diagnostic checking) and the chapter on seasonal models
  - book: isbn:9780387974293
    title: "Peter J. Brockwell and Richard A. Davis, Time Series: Theory and Methods, second edition, Springer, 1991"
    locator: Section 9.2 (identification techniques, p. 284), Section 9.3 (order selection, p. 301) and Section 9.4 (diagnostic checking, pp. 306 to 313)
  - book: isbn:9783319298528
    title: Peter J. Brockwell and Richard A. Davis, Introduction to Time Series and Forecasting, third edition, Springer, 2016
    locator: Section 5.1 (preliminary estimation, with the innovations method in Section 5.1.3, p. 132, and the Hannan-Rissanen algorithm in Section 5.1.4, p. 137), Section 5.2 (maximum likelihood, p. 139), Section 5.3 (diagnostic checking, p. 144) and Section 5.5 (order selection, p. 149)
---

The Box-Jenkins method builds an [ARIMA](/arima-model/) model for a time series by a loop of three stages: identification, estimation and diagnostic checking. Identification transforms and differences the series until it looks stationary, and then reads tentative orders $(p, q)$ from the sample [autocorrelation](/autocorrelation/) and [partial autocorrelation](/partial-autocorrelation-function/) functions. Estimation fits the candidate models, usually by Gaussian maximum likelihood. Diagnostic checking asks whether the residuals look like white noise, with the residual autocorrelations and the [Ljung-Box test](/ljung-box-test/). If a check fails, the residuals suggest a better model and the loop starts again. The final model gives forecasts with intervals. Box and Jenkins (1970) set out the method and its principle of parsimony: use the fewest parameters that describe the data adequately. It is a procedure for model building, not an algorithm with a guarantee, and different analysts can reach different adequate models.

## In plain words

You have a series and want a simple model that explains how each value depends on the past. First make the series steady: take logs if the swings grow with the level, and take differences if it wanders without a fixed level. Then look at two plots that show how the steady series is related to its own past, and match their shapes against the known shapes of simple models. Fit the few models that match. Look at what each model leaves unexplained. If the leftovers still show a pattern, the model missed something, and the pattern tells you what to add. Stop when the leftovers look like pure noise, and prefer the simplest model that passes.

## When it applies

- The series is equally spaced, without long gaps, and long enough: a common rule asks for at least about 50 observations, and more for seasonal models.
- After a transformation and $d$ differences, the series is plausibly stationary and linear, so an [ARMA](/arma-model/) model can describe it.
- The goal is short-term forecasting or a compact description of the dependence. For forecasting many series automatically, an automatic version of the loop or exponential smoothing is more practical.
- The method does not handle structural breaks, outliers, changing variance or nonlinear dynamics by itself. Each needs its own model term or a different model.

## The template

The data are $x_1, \ldots, x_n$. The holes are the transformation `T`, the differencing rule `D`, the identification rule `IDENT`, the estimator `FIT`, the diagnostic checks `CHECK` and the final choice `SELECT`.

```pseudo id=main
BOX-JENKINS(x[1..n], T, D, IDENT, FIT, CHECK, SELECT)
L1  y ← T(x)                                        ▷ log or Box-Cox, to make the variance steady
L2  (d, D_s) ← D(y); w ← (1 - B)^d (1 - B^s)^{D_s} y  ▷ difference until the ACF dies out quickly
L3  C ← IDENT(ACF and PACF of w)                    ▷ a few candidate orders (p, q), with or without a constant
L4  for each (p, q) ∈ C do M[p, q] ← FIT(w, p, q)   ▷ Gaussian ML, or conditional least squares
L5  A ← {M[p, q] that pass CHECK}                   ▷ residual ACF, Ljung-Box with h - p - q df, overfitting
L6  if A = ∅ then revise C from the residual ACF and PACF, and go to L4
L7  M* ← SELECT(A)                                  ▷ the most parsimonious, or the smallest AIC
L8  return M* and forecasts of x with intervals     ▷ undo the differencing and T
```

**Identification patterns.** For a stationary series, the theoretical ACF $\rho(h)$ and PACF $\phi_{hh}$ have these shapes:

| model | ACF | PACF |
|---|---|---|
| [AR](/autoregressive-model/)($p$) | tails off (a mix of decaying exponentials and damped sine waves) | 0 after lag $p$ |
| [MA](/moving-average-model/)($q$) | 0 after lag $q$ | tails off |
| ARMA($p$, $q$), $p, q \ge 1$ | tails off after lag $q - p$ | tails off after lag $p - q$ |

A cut-off is judged against bands. Beyond lag $p$, the sample PACF of an AR($p$) process is about $N(0, 1/n)$, so the bands are $\pm 1.96/\sqrt{n}$. Beyond lag $q$, the sample ACF of an MA($q$) process has variance about $(1 + 2\sum_{k=1}^{q}\rho(k)^2)/n$ by Bartlett's formula, so its bands are wider than $\pm 1.96/\sqrt{n}$. A mixed ARMA model has no cut-off in either function, and its orders are hard to read from the plots. Then fit a few small models and compare them with a criterion such as the [AIC](/akaike-information-criterion/).

**Differencing.** A sample ACF that starts near 1 and decays slowly and almost linearly suggests a unit root, so difference once. A unit-root test such as the [augmented Dickey-Fuller test](/augmented-dickey-fuller-test/) or the [KPSS test](/kpss-test/) makes the choice of $d$ more formal. A lag-1 autocorrelation of the differences near $-0.5$ suggests too much differencing.

**Estimation.** Exact Gaussian maximum likelihood, computed with the [innovations algorithm](/innovations-algorithm/) or a Kalman filter, is the standard. Preliminary estimates come from the [Yule-Walker equations](/yule-walker-equations/) for AR models, from the innovations algorithm for MA models, and from the Hannan-Rissanen regression for mixed models. The fitted model should be causal and invertible, and the standard errors from the information matrix show which coefficients are needed.

**Diagnostic checking.** If the model is right, the residuals are approximately white noise. Check (1) the residual ACF against $\pm 1.96/\sqrt{n}$, remembering that the bands are too wide at small lags for residuals; (2) the [Ljung-Box](/ljung-box-test/) statistic with $h - p - q$ degrees of freedom; (3) overfitting, that is adding one AR or one MA term and checking that it is not significant and that the other estimates do not change much; (4) a plot of the residuals over time, and a normal quantile plot if normal forecast intervals will be used.

## Classic examples

- **A simulated ARIMA(1, 1, 0) series.** 200 values were generated with $(1 - 0.6B)(1 - B)X_t = \varepsilon_t$, $\varepsilon_t \sim N(0, 1)$ (seed 7). This walk-through shows each stage.
  - *Identification.* The ACF of the levels is 0.989 at lag 1 and still 0.799 at lag 10, the slow decay of a nonstationary series. For the $N = 199$ differences, the band is $\pm 1.96/\sqrt{199} = \pm 0.139$.

    | lag | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
    |---|---|---|---|---|---|---|---|---|---|---|
    | ACF of differences | 0.585 | 0.346 | 0.235 | 0.113 | 0.037 | 0.004 | -0.020 | -0.043 | 0.050 | 0.022 |
    | PACF of differences | 0.585 | 0.006 | 0.047 | -0.067 | -0.022 | -0.005 | -0.015 | -0.024 | 0.140 | -0.079 |

    The ACF tails off and the PACF cuts off after lag 1, which points to AR(1) for the differences. The PACF at lag 9 is just outside the band, but one value in ten outside a 95% band is expected by chance, and lag 9 has no meaning for this series. The mean of the differences is 0.150 with a standard error of 0.162 (allowing for the autocorrelation), $t = 0.93$, so the model has no drift.
  - *Estimation and checking.* The models were fitted by Yule-Walker to the differences with mean 0. For a pure AR model this is close to maximum likelihood. The criterion is $N\log\hat\sigma^2 + 2p$.

    | model for the differences | estimates | $\hat\sigma^2$ | Ljung-Box $Q$, $h = 10$ | df | p-value | criterion |
    |---|---|---|---|---|---|---|
    | white noise | | 1.384 | 108.57 | 10 | $1.0 \times 10^{-18}$ | 64.68 |
    | AR(1) | $\hat\phi = 0.5921$ (se 0.0571) | 0.8988 | 7.848 | 9 | 0.550 | -19.24 |
    | AR(2) | $\hat\phi = (0.5852, 0.0118)$ | 0.8987 | 7.762 | 8 | 0.457 | -17.26 |

    White noise fails the check. AR(1) passes. The overfitted AR(2) adds a coefficient of 0.012, far below its standard error of about 0.07, and does not change $\hat\phi_1$ much or lower $\hat\sigma^2$. So the chosen model is ARIMA(1, 1, 0) with $\hat\phi = 0.592$, close to the true 0.6.
  - *Forecasting.* The last level is $X_n = 30.045$ and the last difference $-0.710$. The forecasts of the levels for 1 to 5 steps ahead are 29.624, 29.375, 29.228, 29.140 and 29.089, and they approach $30.045 - 0.710 \cdot \hat\phi/(1 - \hat\phi) = 29.014$. The forecast standard errors $\hat\sigma(\sum_{j<k}\psi_j^2)^{1/2}$ with $\psi_j = 1 + \hat\phi + \cdots + \hat\phi^j$ are 0.948, 1.782 and 2.563 for 1, 2 and 3 steps. They grow without limit, as they must for an integrated model.
- **The airline model.** Box and Jenkins modelled the logarithm of monthly international airline passenger numbers, 1949 to 1960. After the differences $(1 - B)(1 - B^{12})$, they chose $(1 - B)(1 - B^{12})\log X_t = (1 + \theta B)(1 + \Theta B^{12})\varepsilon_t$, now called the airline model. The theoretical ACF of the differenced series is nonzero only at lags 1, 11, 12 and 13, so a sample ACF with spikes at these lags points to it. With two parameters it fits many monthly series with trend and seasonality.
- **Exponential smoothing as a special case.** If identification gives ARIMA(0, 1, 1), the forecasts are an [exponentially weighted moving average](/exponential-moving-average/) of the past values. The loop thus explains when this common rule is the optimal linear forecast.

## Variations

- **Information criteria in place of pattern reading.** Fit all models with $p, q \le$ a small bound and choose by AIC, AICc or [BIC](/bayesian-information-criterion/). This is easier to automate and often agrees with the ACF and PACF patterns. Compare criteria only between models with the same $d$, because differencing changes the data.
- **Automatic ARIMA.** Programs choose $d$ by unit-root tests and then search over $(p, q)$ and the seasonal orders by a criterion, with checks on the residuals (for example the stepwise search of Hyndman and Khandakar, 2008). They make the loop practical for thousands of series.
- **Extended identification tools.** The extended sample autocorrelation function and the corner method help to read mixed ARMA orders, where neither the ACF nor the PACF cuts off.
- **Transfer function models.** Box and Jenkins extended the same loop to a series driven by an input series, with prewhitening of the input to identify the transfer function. This is the time series form of the [ARMAX model](/armax-model/).
- **Seasonal adjustment programs.** X-13ARIMA-SEATS and TRAMO-SEATS fit a seasonal ARIMA model inside a decomposition, and use it to extend the series before filtering.

## Pitfalls

- **Too much differencing.** Differencing a stationary series introduces an MA unit root. For white noise, $(1 - B)\varepsilon_t$ has $\rho(1) = -1/2$ and a larger variance than $\varepsilon_t$. A lag-1 autocorrelation near $-0.5$ and an estimated MA coefficient near $-1$ are the signs.
- **Too little differencing.** A slowly decaying ACF fitted with a stationary AR model gives a root near 1, poor intervals, and forecasts that return to the mean too fast.
- **Reading the plots too closely.** With 20 lags and 95% bands, about one value falls outside by chance. A single isolated spike at a lag with no meaning is usually noise.
- **Common factors.** ARMA($p + 1$, $q + 1$) can fit as well as ARMA($p$, $q$) with an AR and an MA root that almost cancel. The estimates are then unstable and have huge standard errors. Prefer the smaller model.
- **Model uncertainty.** The forecast intervals are computed as if the chosen model were true. After a search over many models, they are too narrow.
- **Back-transforming forecasts.** If the model is for $\log X_t$, then $\exp$ of the forecast is the median of $X_{n+h}$, not its mean. The mean needs a correction such as $\exp(\hat\mu + \hat\sigma_h^2/2)$ under normality.
- **Drift with $d \ge 1$.** A constant in a model for differences is a deterministic trend in the levels. Include it only if the mean of the differences is clearly not 0, as tested in the example.

## Exercises

1. Show that differencing white noise gives an MA(1) process with $\theta = -1$, $\rho(1) = -1/2$, and twice the variance.
2. For ARIMA(1, 1, 0), show that the $\psi$ weights of the levels are $\psi_j = 1 + \phi + \cdots + \phi^j$, and that the $h$-step forecast variance grows linearly in $h$ for large $h$.
3. For the example, show that the forecasts of the levels converge to $X_n + D_n\phi/(1 - \phi)$, where $D_n$ is the last difference.
4. Explain why the AIC of a model for $x$ cannot be compared with the AIC of a model for $(1 - B)x$.

## References
