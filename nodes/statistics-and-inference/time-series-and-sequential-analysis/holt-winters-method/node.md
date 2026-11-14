---
tag: 56FTG8
kind: algorithm
slug: holt-winters-method
name: Holt-Winters method
aliases:
- triple exponential smoothing
- Holt's linear trend method
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: Forecasts by exponentially smoothed updates of a level, a trend and a seasonal component. Holt's method has level and trend only.
model: real-ram
complexity:
  vars: {n: the length of the series, m: the seasonal period, h: the forecast horizon}
  time: {worst: Θ(n + h), best: Θ(n + h)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1957
  people: [Charles C. Holt, Peter R. Winters]
  note: Holt's 1957 Office of Naval Research memorandum smoothed a level and a trend, and sketched seasonal factors. Winters (1960) tested the seasonal version on sales data. Holt's memorandum was published in 2004.
prereqs: [exponential-moving-average, arima-model]
see_also: [moving-average, stl-decomposition, state-space-model, kalman-filter, box-jenkins-method, akaike-information-criterion, autocorrelation, arma-model]
sources:
  - paper: doi:10.1016/j.ijforecast.2003.09.015
    title: Charles C. Holt, Forecasting seasonals and trends by exponentially weighted moving averages, International Journal of Forecasting 20(1) (2004), pages 5 to 10, a reprint of the 1957 ONR memorandum
    locator: the level and trend recursions and the seasonal factors
  - paper: doi:10.1287/mnsc.6.3.324
    title: Peter R. Winters, Forecasting sales by exponentially weighted moving averages, Management Science 6(3) (1960), pages 324 to 342
    locator: the multiplicative seasonal model and its tests on sales series
  - paper: doi:10.1002/for.3980040103
    title: Everette S. Gardner Jr., Exponential smoothing, the state of the art, Journal of Forecasting 4(1) (1985), pages 1 to 28
    locator: the survey of the methods and their equivalences with ARIMA models
  - paper: doi:10.1016/j.ijforecast.2006.03.005
    title: Everette S. Gardner Jr., Exponential smoothing, the state of the art, part II, International Journal of Forecasting 22(4) (2006), pages 637 to 666
    locator: the damped trend, the state space models and the parameter choices
  - paper: doi:10.1016/S0169-2070(01)00110-8
    title: Rob J. Hyndman, Anne B. Koehler, Ralph D. Snyder and Simone Grose, A state space framework for automatic forecasting using exponential smoothing methods, International Journal of Forecasting 18(3) (2002), pages 439 to 454
    locator: the innovations state space models (ETS) behind each method, with likelihoods and prediction intervals
  - paper: doi:10.1080/01621459.1960.10482064
    title: John F. Muth, Optimal properties of exponentially weighted forecasts, Journal of the American Statistical Association 55(290) (1960), pages 299 to 306
    locator: simple exponential smoothing as the optimal forecast of a random walk plus noise
---

The Holt-Winters method forecasts a series by keeping three running estimates: a level, a trend (the change per step), and a seasonal effect for each position in the period. After each observation it moves each estimate a fixed fraction toward what the new value suggests, exactly as an [exponential moving average](/exponential-moving-average/) does. The forecast $h$ steps ahead is the level plus $h$ times the trend, plus the seasonal effect for that position. Without the seasonal part this is Holt's linear method, which gives exactly the same forecasts as an [ARIMA](/arima-model/)(0, 2, 2) model. The method needs $O(1)$ work per observation, handles additive or multiplicative seasons, and has stayed a strong baseline for sales and demand forecasting since the 1960s.

## In plain words

Think of forecasting sales that grow and rise every December. You keep three numbers: where sales are now, how fast they grow, and how much each month is usually above or below normal. When a new month comes in, you compare it with what you expected. You then nudge each number part of the way toward the new evidence: a little if you trust the past, a lot if you think things change fast. To forecast, you start from where sales are now, add the growth for each month ahead, and add that month's usual bump. Three dials, between 0 and 1, set how fast each number reacts.

## The problem

Given $y_1, \dots, y_n$, a seasonal period $m$ (or none), and smoothing constants $\alpha, \beta, \gamma \in [0, 1]$, compute the one-step forecasts $\hat y_{t|t-1}$ for $t = 1..n$ and the forecasts $\hat y_{n+h|n}$, $h = 1, 2, \dots$, of the additive model
$$\hat y_{t|t-1} = \ell_{t-1} + b_{t-1} + s_{t-m}$$
with the level $\ell_t$, the trend $b_t$ and the seasonal states $s_t$ updated by the recursions of the algorithm. In the multiplicative model the season multiplies, $\hat y_{t|t-1} = (\ell_{t-1} + b_{t-1})s_{t-m}$. The constants are chosen by minimizing the sum of squared one-step errors $\sum_te_t^2$, $e_t = y_t - \hat y_{t|t-1}$, which is the Gaussian maximum likelihood estimate in the matching state space model.

## The algorithm

```pseudo id=main
HOLT-WINTERS(y₁..y_n, m, α, β, γ, h; start ℓ₀, b₀, s_{1−m..0})
    for t ← 1 to n
L1      ŷ_t ← ℓ_{t−1} + b_{t−1} + s_{t−m}
L2      e_t ← y_t − ŷ_t
L3      ℓ_t ← α (y_t − s_{t−m}) + (1 − α)(ℓ_{t−1} + b_{t−1})
L4      b_t ← β (ℓ_t − ℓ_{t−1}) + (1 − β) b_{t−1}
L5      s_t ← γ (y_t − ℓ_{t−1} − b_{t−1}) + (1 − γ) s_{t−m}
L6  ŷ_{n+k} ← ℓ_n + k b_n + s_{n+k−m(⌊(k−1)/m⌋+1)}, k = 1..h
L7  return (ŷ, e, ℓ_n, b_n, s, ŷ_{n+1..n+h}, Σ e_t²)
```

Holt's linear method drops line L5 and the $s$ terms. Simple exponential smoothing also drops line L4 and sets $b = 0$. For multiplicative seasons, line L1 becomes $(\ell_{t-1} + b_{t-1})s_{t-m}$, line L3 uses $y_t/s_{t-m}$, and line L5 uses $y_t/(\ell_{t-1} + b_{t-1})$. The classical start sets $\ell_0$ to the mean of the first season, $b_0$ to the difference of the first two season means divided by $m$, and $s_{i-m}$ to $y_i - \ell_0$ for $i = 1..m$. For Holt's method it sets $\ell_0 = y_1$ and $b_0 = y_2 - y_1$. Modern software estimates the start values together with the constants.

Line L3 can be written $\ell_t = \ell_{t-1} + b_{t-1} + \alpha e_t$, line L4 as $b_t = b_{t-1} + \alpha\beta e_t$, and line L5 as $s_t = s_{t-m} + \gamma e_t$. This error correction form shows each state moving by a fixed share of the forecast error. Winters (1960) wrote the seasonal update with $y_t - \ell_t$ in place of $y_t - \ell_{t-1} - b_{t-1}$. That is the same method with $\gamma = \gamma^*(1 - \alpha)$.

## Example

**Holt's method by hand.** Take $y = (10, 12, 15, 14, 18, 21)$, $\alpha = \beta = 1/2$, $\ell_0 = 10$ and $b_0 = 2$.

| $t$ | $y_t$ | $\hat y_t$ (L1) | $e_t$ (L2) | $\ell_t$ (L3) | $b_t$ (L4) |
|---|---|---|---|---|---|
| 1 | 10 | 12 | $-2$ | 11 | 1.5 |
| 2 | 12 | 12.5 | $-0.5$ | 12.25 | 1.375 |
| 3 | 15 | 13.625 | 1.375 | 14.3125 | 1.71875 |
| 4 | 14 | 16.03125 | $-2.03125$ | 15.015625 | 1.2109375 |
| 5 | 18 | 16.2265625 | 1.7734375 | 17.11328125 | 1.654296875 |
| 6 | 21 | 18.767578125 | 2.232421875 | 19.8837890625 | 2.21240234375 |

All values are exact dyadic fractions: $\ell_6 = 20361/1024$ and $b_6 = 4531/2048$. Line L6 gives $\hat y_7 = 22.096$, $\hat y_8 = 24.309$ and $\hat y_9 = 26.521$, a straight line with slope $b_6$. With $\theta_1 = \alpha(1 + \beta) - 2 = -5/4$ and $\theta_2 = 1 - \alpha = 1/2$, the ARIMA(0, 2, 2) recursion $\hat y_{t+1} = 2y_t - y_{t-1} + \theta_1e_t + \theta_2e_{t-1}$ started from $\hat y_2 = 12.5$ and $e_1 = -2$, reproduces every later forecast in the table, and the three forecasts beyond it, exactly.

**With a season.** Take quarterly data $y = (12, 8, 14, 10, 16, 11, 17, 14, 19, 14, 21, 17)$, $m = 4$, additive seasons, $\alpha = 1/2$, $\beta = \gamma = 1/4$. The classical start is $\ell_0 = 11$ (mean of the first year), $b_0 = (14.5 - 11)/4 = 7/8$, and $s = (1, -3, 3, -1)$. Then $\hat y_1 = 11 + 0.875 + 1 = 12.875$, $e_1 = -0.875$, $\ell_1 = 0.5 \cdot 11 + 0.5 \cdot 11.875 = 11.4375$, $b_1 = 0.25 \cdot 0.4375 + 0.75 \cdot 0.875 = 0.765625$, and $s_1 = 0.25 \cdot 0.125 + 0.75 \cdot 1 = 0.78125$. After all 12 points, $\ell_{12} = 18.734$, $b_{12} = 0.727$, $s = (1.978, -3.347, 2.583, -1.509)$, and the forecasts for the next year are $21.44, 16.84, 23.50, 20.13$.

**Simulated monthly data.** With seed 2026, simulate 144 months from the additive model with $\alpha = 0.3$, $\alpha\beta = 0.03$, $\gamma = 0.2$, noise standard deviation 2 and a sine-shaped season of amplitude 10. Fit on the first 120 months by a grid search for the smallest sum of squared errors: it picks $\alpha = 0.2$, $\beta = 0.16$, $\gamma = 0.3$. On the last 24 months, the root mean square error is 2.11 for Holt-Winters, 8.55 for the seasonal naive forecast (the value one year earlier), and 12.0 for Holt's method without seasons. These are measured on one sample.

## Correctness

The correctness page proves the following. The recursions are equivalent to the error correction form. Winters' form is the component form with $\gamma = \gamma^*(1 - \alpha)$. Holt's linear method and ARIMA(0, 2, 2) with $\theta_1 = \alpha(1 + \beta) - 2$ and $\theta_2 = 1 - \alpha$ give identical one-step and $h$-step forecasts from the same start. The MA polynomial is invertible exactly when $0 < \alpha < 2$ and $0 < \alpha\beta < 4 - 2\alpha$. A series that is a line plus a fixed season, or a line times a fixed season, is forecast with zero error for any constants once the start is right. The method is exact arithmetic on its inputs, so the tests check it in rationals. The optimality of the forecasts for the ETS state space models (Hyndman et al. 2002) is cited, not proved.

## Complexity

On a [real RAM](/real-ram/), each observation costs $O(1)$ arithmetic operations, so a pass over $n$ points takes $\Theta(n)$ time and line L6 takes $\Theta(h)$. The state is the level, the trend and $m$ seasonal values, $\Theta(m)$ space; the method is online. Choosing the constants by minimizing the squared errors takes one pass per evaluation: a grid of $G$ values per constant costs $\Theta(G^3n)$, and a quasi-Newton or Nelder-Mead search typically needs a few hundred passes.

**Numerical stability.** The recursions are convex combinations when the constants are in $[0, 1]$, so rounding errors do not grow: each state is a weighted average of past values with weights that sum to 1. The multiplicative form divides by $s_{t-m}$ and by $\ell_{t-1} + b_{t-1}$. It breaks down when the series is near 0 or changes sign, and it should be used only for positive data.

## Properties

- **Exact for its model class.** Lines plus fixed seasons are reproduced with zero error, for any constants.
- **Equivalent to ARIMA models.** Simple exponential smoothing is the optimal forecast of ARIMA(0, 1, 1) (Muth 1960). Holt's method gives the forecasts of ARIMA(0, 2, 2). The additive Holt-Winters method gives the forecasts of a seasonal ARIMA model with differences $\nabla\nabla_m$ and a moving average part of order $m + 1$ with restricted coefficients.
- **State space form.** Each method is the steady forecast recursion of an innovations state space model (ETS), which gives a likelihood, AIC model choice and prediction intervals.
- **Online.** Each new observation updates the states in constant time.
- **Weights decay geometrically.** The level is a weighted average of past values with weights $\alpha(1 - \alpha)^j$ in simple exponential smoothing.
- **Not robust.** One outlier shifts the level, the trend and the season, and the trend carries the error into all later forecasts.

## Variants and improvements

- **Damped trend.** Gardner and McKenzie (1985) multiply the trend by $\phi < 1$ at each step, so long-range forecasts level off. The damped trend is often more accurate than Holt's linear trend for horizons beyond a few steps.
- **Multiplicative seasons.** The seasonal effect scales with the level, which suits series whose swings grow with their size.
- **ETS framework.** Hyndman, Koehler, Snyder and Grose (2002) give fifteen combinations of error, trend and season types, with likelihoods for estimation and selection by AIC.
- **Several seasonal periods.** Taylor's double seasonal method and the TBATS models handle, for example, daily and weekly cycles in hourly data.
- **Robust versions.** Replace the squared error loss by a robust loss, or clean outliers first, for example with [STL](/stl-decomposition/).
- **Brown's double exponential smoothing.** One constant $a$ for level and trend. It is Holt's method with $\alpha = a(2 - a)$ and $\beta = a/(2 - a)$, so both are ARIMA(0, 2, 2) with the double root $\theta(z) = (1 - (1 - a)z)^2$.

## When to use it

Use Holt-Winters for short- to medium-term forecasts of a series with a stable trend and season, especially when there are many series and each needs a cheap, automatic forecast, such as inventory or demand planning. It is a strong baseline: compare any new method with it. Use the damped trend for longer horizons. If the series has several seasonal periods, outliers, or effects of covariates, use STL followed by a forecast of the seasonally adjusted series, a seasonal ARIMA model, or a regression with ARIMA errors.

## Pitfalls

- **Bad start values.** The classical start uses only the first two seasons. With small constants, a poor start biases forecasts for a long time. Estimate the start with the constants.
- **Additive versus multiplicative.** If the seasonal swing grows with the level, additive seasons underfit large values; use multiplicative seasons or take logs.
- **Linear trend extrapolation.** Holt's trend continues forever. Long-horizon forecasts from a recent upswing can be far off; damp the trend.
- **Overfitting the constants.** Minimizing in-sample squared errors with a large $\gamma$ can chase noise. Check the forecasts on a holdout sample.
- **Conflicting parameter conventions.** Different books use $\beta$ for the trend update in $\ell_t - \ell_{t-1}$ (as here) or for $\alpha\beta$ in the error form, and $\gamma$ or $\gamma^*$ for the season. Check the convention before copying constants between programs.
- **Prediction intervals.** The method gives point forecasts only. Intervals need the state space model; naive intervals from in-sample errors are too narrow for long horizons.

## Implementations

## History

Robert Brown used exponential smoothing for inventory control in the U.S. Navy in the 1950s. Charles Holt, at the Carnegie Institute of Technology, wrote the level and trend method and sketched seasonal factors in a 1957 report to the Office of Naval Research; the report circulated for decades and was published in 2004. Peter Winters, also at Carnegie, tested the seasonal method on sales data in 1960. Muth (1960) showed that simple exponential smoothing is optimal for a random walk observed with noise, and Box and Jenkins linked the methods to ARIMA models. Gardner (1985, 2006) surveyed the field, and Hyndman, Koehler, Snyder and Grose (2002) put the methods on a state space footing with likelihoods.

## References
