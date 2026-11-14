---
tag: W6NWDC
kind: model
slug: arima-model
name: ARIMA model
aliases:
- "autoregressive integrated moving average"
- "ARIMA(p, d, q) model"
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: An ARMA model for the series differenced d times, used for series with stochastic trends. Seasonal ARIMA adds seasonal differences and lags.
history:
  year: 1970
  people: [George E. P. Box, Gwilym M. Jenkins]
  note: Box and Jenkins proposed in their 1970 book to difference a nonstationary series until it looks stationary and to fit an ARMA model to the result, with seasonal versions such as the airline model.
prereqs: [arma-model]
see_also: [box-jenkins-method, augmented-dickey-fuller-test, kpss-test, exponential-moving-average, holt-winters-method, stl-decomposition, moving-average-model, state-space-model]
sources:
  - book: isbn:9780816210947
    title: "George E. P. Box and Gwilym M. Jenkins, Time Series Analysis: Forecasting and Control, Holden-Day, 1970"
    locator: the integrated models, their forecasts and the seasonal models (the first edition)
  - book: isbn:9781118675021
    title: "George E. P. Box, Gwilym M. Jenkins, Gregory C. Reinsel and Greta M. Ljung, Time Series Analysis: Forecasting and Control, fifth edition, Wiley, 2015"
    locator: Part I (nonstationary models and forecasting) and the chapter on seasonal models (the airline model)
  - book: isbn:9780387974293
    title: "Peter J. Brockwell and Richard A. Davis, Time Series: Theory and Methods, second edition, Springer, 1991"
    locator: Section 9.1 (ARIMA models for nonstationary series, p. 274), Section 9.5 (forecasting ARIMA models, p. 314) and Section 9.6 (seasonal ARIMA models, pp. 320 to 325)
  - book: isbn:9783319298528
    title: Peter J. Brockwell and Richard A. Davis, Introduction to Time Series and Forecasting, third edition, Springer, 2016
    locator: Section 6.1 (ARIMA models, p. 158), Section 6.3 (unit roots, p. 169), Section 6.4 (forecasting, p. 173) and Section 6.5 (seasonal ARIMA, p. 177)
---

An ARIMA($p$, $d$, $q$) model says that a time series becomes a stationary [ARMA](/arma-model/)($p$, $q$) process after it is differenced $d$ times. The differences remove a stochastic trend: a series that wanders like a random walk has stationary changes, and the model describes those changes. The "I" stands for integrated, because the original series is the $d$-fold sum of a stationary series. For $d \ge 1$ the process is not stationary, its forecast intervals widen without limit, and its forecasts follow the last level, not a fixed mean. Familiar forecasting rules are ARIMA models: the random walk is ARIMA(0, 1, 0), and [exponential smoothing](/exponential-moving-average/) is the optimal forecast for ARIMA(0, 1, 1). Seasonal ARIMA (SARIMA) adds differences and ARMA terms at the seasonal lag $s$.

## The machine

**Notation.** $B$ is the backshift operator and $\nabla = 1 - B$ the difference operator, so $\nabla X_t = X_t - X_{t-1}$ and $\nabla^2 X_t = X_t - 2X_{t-1} + X_{t-2}$. $\phi(z)$ and $\theta(z)$ are as on the [ARMA model](/arma-model/) page, and $\{\varepsilon_t\} \sim \mathrm{WN}(0, \sigma^2)$.

**Definition.** For an integer $d \ge 0$, $\{X_t\}$ is an ARIMA($p$, $d$, $q$) process if $Y_t = \nabla^d X_t$ is a causal ARMA($p$, $q$) process:

$$\phi(B)(1 - B)^d X_t = \theta(B)\varepsilon_t,$$

possibly with a constant $c$ on the right, so that $Y_t$ has mean $\mu = c/\phi(1)$. The autoregressive polynomial $\phi^*(z) = \phi(z)(1 - z)^d$ has a root of multiplicity $d$ at $z = 1$, on the unit circle. So the ARMA theory gives no stationary solution, and the model is completed by a condition on the start: $X_{1-d}, \ldots, X_0$ are uncorrelated with $\{Y_t : t \ge 1\}$ (Brockwell and Davis 1991, Section 9.1). Then $X_t$ for $t \ge 1$ is $X_0$ plus a sum of $Y$ values when $d = 1$, and a repeated sum when $d \ge 2$.

**Parameters.** $\phi$ and $\theta$ in the causal and invertible region, $\sigma^2$, the order $d$, and optionally the drift $\mu$. The orders $(p, d, q)$ are chosen from the data.

**What differencing removes.**

- A random walk $X_t = X_{t-1} + \varepsilon_t$ is ARIMA(0, 1, 0). Given $X_0$, $\operatorname{Var}(X_t) = t\sigma^2$, which grows without bound.
- A drift $\mu \ne 0$ in $\nabla X_t$ gives a linear trend of slope $\mu$ in $X_t$, and with $d = 2$ it gives a quadratic trend.
- A deterministic linear trend plus stationary noise, $X_t = a + bt + Z_t$, also becomes stationary after one difference, but $\nabla Z_t$ then has a moving-average unit root. The two models give different forecast intervals. Tests such as the [augmented Dickey-Fuller test](/augmented-dickey-fuller-test/) and the [KPSS test](/kpss-test/) try to tell them apart.

**Seasonal ARIMA.** With period $s$ (12 for monthly data), the SARIMA$(p, d, q) \times (P, D, Q)_s$ model is

$$\phi(B)\, \Phi(B^s)\, (1 - B)^d (1 - B^s)^D X_t = \theta(B)\, \Theta(B^s)\, \varepsilon_t,$$

where $\Phi$ and $\Theta$ are polynomials of degree $P$ and $Q$. The airline model of Box and Jenkins is $(0, 1, 1) \times (0, 1, 1)_{12}$, usually for the logarithm of the series: $(1 - B)(1 - B^{12}) X_t = (1 + \theta B)(1 + \Theta B^{12}) \varepsilon_t$. It has two parameters besides $\sigma^2$ and fits many monthly series with trend and seasonality.

## What it counts

The parameters are those of the ARMA model for $Y = \nabla^d X$, plus $d$. The main quantities are the forecasts and their error variances.

| quantity | formula | cost |
|---|---|---|
| differenced series | $Y_t = \nabla^d X_t$ for $t = d + 1, \ldots, n$ | $O(nd)$ |
| ARMA quantities of $Y$ | as on the [ARMA model](/arma-model/) page | as there |
| $\psi^*$ weights | coefficients of $\theta(z)/(\phi(z)(1 - z)^d)$, by the ARMA recursion with $\phi^*$ | $O(p + d + q)$ per weight |
| $h$-step forecast | the ARMA forecasts of $Y_{n+1}, \ldots, Y_{n+h}$, then summed back (undifferenced) from the last $d$ observed levels | $O(h(p + d + q))$ after the ARMA forecasts |
| its error variance, for large $n$ | $\sigma^2 \sum_{j=0}^{h-1} (\psi^*_j)^2$ | $O(h)$ |
| Gaussian likelihood | the ARMA likelihood of $Y_{d+1}, \ldots, Y_n$, conditional on the first $d$ values | as for ARMA |

**Forecast errors grow.** The weights $\psi^*_j$ do not tend to 0. For ARIMA(1, 1, 0) with $\phi = 0.6$ and $\sigma^2 = 1$, $\psi^* = 1, 1.6, 1.96, 2.176, 2.306, \ldots \to 1/(1 - \phi) = 2.5$, so the forecast standard errors at $h = 1, 2, 3$ are $1$, $\sqrt{1 + 2.56} = 1.887$ and $\sqrt{1 + 2.56 + 3.8416} = 2.721$, and they grow like $2.5\sqrt{h}$. For ARIMA(0, 2, 0), $\psi^*_j = j + 1$ and the variance is $\sigma^2 h(h + 1)(2h + 1)/6$, so the standard error grows like $h^{3/2}$. For a stationary ARMA model it would converge to $\sqrt{\gamma(0)}$.

**Exponential smoothing.** For ARIMA(0, 1, 1), $X_t - X_{t-1} = \varepsilon_t + \theta \varepsilon_{t-1}$ with $-1 < \theta < 0$. The one-step forecast is $\hat X_{t+1} = X_t + \theta \varepsilon_t$, and $\varepsilon_t = X_t - \hat X_t$, so

$$\hat X_{t+1} = (1 + \theta) X_t - \theta \hat X_t = \alpha X_t + (1 - \alpha)\hat X_t, \qquad \alpha = 1 + \theta.$$

This is the [exponential moving average](/exponential-moving-average/). By hand, with $\theta = -0.7$ ($\alpha = 0.3$), data $X_1, \ldots, X_4 = 10, 12, 11, 15$ and start $\hat X_1 = 10$: $\hat X_2 = 10$, $\hat X_3 = 0.3 \times 12 + 0.7 \times 10 = 10.6$, $\hat X_4 = 0.3 \times 11 + 0.7 \times 10.6 = 10.72$ and $\hat X_5 = 0.3 \times 15 + 0.7 \times 10.72 = 12.004$. Every forecast $\hat X_{4+h}$, $h \ge 1$, is $12.004$.

## Relation to other models

- **[ARMA model](/arma-model/).** ARIMA($p$, 0, $q$) is ARMA($p$, $q$). An ARIMA model with $d \ge 1$ is an ARMA equation whose AR polynomial has a unit root.
- **[Moving-average model](/moving-average-model/).** Differencing a stationary series once too often gives an MA part with a root on the unit circle: the difference of white noise is MA(1) with $\theta = -1$ and lag-1 autocorrelation $-0.5$.
- **Exponential smoothing and [Holt-Winters](/holt-winters-method/).** Simple exponential smoothing is optimal for ARIMA(0, 1, 1), and Holt's linear method is optimal for ARIMA(0, 2, 2). The additive Holt-Winters method corresponds to a seasonal ARIMA model.
- **[State-space model](/state-space-model/).** ARIMA models have state space forms, and the [Kalman filter](/kalman-filter/) handles the nonstationary start with a diffuse prior on the first $d$ levels.
- **Fractional differencing.** ARFIMA models allow a noninteger $d$. For $-1/2 < d < 1/2$ the process is stationary, and for $0 < d < 1/2$ its autocorrelations decay like a power of the lag (long memory), not geometrically.
- **[STL decomposition](/stl-decomposition/).** A nonparametric alternative that removes trend and seasonality by smoothing, not by differencing.

## Known results in the model

- **Fitting.** Choose $d$, difference, then fit an ARMA model to $Y$ by maximum likelihood. The estimates of $\phi$ and $\theta$ have the ARMA limit distribution, because $Y$ is a causal invertible ARMA process. The [Box-Jenkins method](/box-jenkins-method/) is the full identify, estimate and check cycle.
- **Choosing $d$.** A sample autocorrelation that decays slowly and almost linearly suggests a unit root. Unit root tests give a formal check, but they have low power against roots near 1. In practice $d$ is 0, 1 or 2.
- **Over-differencing has a cost.** If $d$ is one too large, the MA part has a unit root, the model is not invertible, and the maximum likelihood estimate of $\theta$ can fall on the boundary $\theta = -1$ with positive probability in finite samples. A lag-1 sample autocorrelation near $-0.5$ after differencing is the usual sign.
- **Forecasts.** With $d = 1$ and no drift, the forecasts converge to a constant level that depends on the last observations. With a drift they follow a line. The error variance grows linearly in $h$ for $d = 1$ and like $h^3$ for $d = 2$, so long-range intervals are very wide.
- **Transformations.** A logarithm or another Box-Cox transformation before differencing often makes the variance of the differences constant. Forecasts on the original scale then need a bias correction.

## References
