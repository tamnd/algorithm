---
tag: NPBB3C
kind: algorithm
slug: ljung-box-test
name: Ljung-Box test
aliases:
- Ljung-Box Q test
- portmanteau test
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: Tests whether the first h autocorrelations of a series or of model residuals are jointly zero by a weighted sum of their squares, which is approximately chi-squared under IID noise.
model: real-ram
complexity:
  vars: {n: the length of the series, h: the number of lags tested}
  time: {worst: Θ(n h), best: Θ(n h)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1978
  people: [Greta M. Ljung, George E. P. Box, David A. Pierce]
  note: Box and Pierce (1970) proposed n times the sum of the squared residual autocorrelations, with h - p - q degrees of freedom, to check a fitted ARIMA model. Ljung and Box (1978) weighted each term by (n + 2)/(n - k), which brings the small-sample law much closer to chi-square.
prereqs: [statistical-hypothesis-test, p-value, autocorrelation, arma-model]
see_also: [box-jenkins-method, chi-squared-goodness-of-fit-test, durbin-watson-test, partial-autocorrelation-function, garch-model, score-test, bonferroni-correction, central-limit-theorem]
sources:
  - paper: doi:10.1093/biomet/65.2.297
    title: Greta M. Ljung and George E. P. Box, On a measure of lack of fit in time series models, Biometrika 65(2), 1978
    locator: pp. 297 to 303 (the modified statistic and its small-sample behaviour)
  - paper: doi:10.1080/01621459.1970.10481180
    title: George E. P. Box and David A. Pierce, Distribution of residual autocorrelations in autoregressive-integrated moving average time series models, Journal of the American Statistical Association 65(332), 1970
    locator: pp. 1509 to 1526 (the asymptotic law of residual autocorrelations and the portmanteau statistic)
  - book: isbn:9780387974293
    title: "Peter J. Brockwell and Richard A. Davis, Time Series: Theory and Methods, second edition, Springer, 1991"
    locator: Section 9.4 (diagnostic checking, pp. 306 to 313)
  - book: isbn:9783319298528
    title: Peter J. Brockwell and Richard A. Davis, Introduction to Time Series and Forecasting, third edition, Springer, 2016
    locator: Section 1.6 (testing the estimated noise sequence, p. 30) and Section 5.3 (diagnostic checking, p. 144)
---

The Ljung-Box test asks whether a series has no autocorrelation at lags $1$ to $h$. Its main use is to check the residuals of a fitted [ARMA](/arma-model/) model: if the model is right, the residuals should look like IID noise. The statistic is $Q = n(n + 2)\sum_{k=1}^{h} \hat r_k^2/(n - k)$, a weighted sum of the squared sample autocorrelations. Under the null it is approximately chi-squared with $h$ degrees of freedom for a raw series, and with $h - p - q$ for the residuals of an ARMA($p$, $q$) fit. It tests all $h$ lags at once, so it is called a portmanteau test. It replaces the older Box-Pierce statistic $n\sum \hat r_k^2$, whose size is too small for short series. Both tests are approximate.

## In plain words

If a model has captured all the structure in a series, what is left over should be pure noise: knowing one leftover value should tell you nothing about the next one, or the one after that. Measure how strongly the leftovers are related at each delay from 1 to $h$ steps. Square these numbers so that positive and negative relations both count, and add them up with a slightly larger weight on the longer delays. If the total is much larger than chance would give, the model has missed something. A single test covers all $h$ delays, so you do not have to look at each one alone.

## The problem

**Model.** A series $e_1, \ldots, e_n$. In the main use, $e_t$ are the residuals of an ARMA($p$, $q$) model fitted by maximum likelihood or least squares, and $s = p + q$ coefficients were estimated. For a raw series, $s = 0$.

**Hypotheses.** $H_0$: the errors of the model are IID with finite variance (for a raw series, $e_1, \ldots, e_n$ are IID). The alternative is any autocorrelation at lags $1$ to $h$. The test has no power against dependence that leaves all these autocorrelations at 0.

**Statistic.** With $\bar e$ the mean and $\hat r_k = \sum_{t=k+1}^{n}(e_t - \bar e)(e_{t-k} - \bar e)/\sum_{t=1}^n (e_t - \bar e)^2$,

$$Q_{\mathrm{LB}} = n(n + 2)\sum_{k=1}^{h}\frac{\hat r_k^2}{n - k}, \qquad Q_{\mathrm{BP}} = n\sum_{k=1}^{h}\hat r_k^2 .$$

**Null distribution.** Asymptotic only. For an IID series with finite variance and fixed $h$, $\sqrt{n}(\hat r_1, \ldots, \hat r_h) \to N(0, I_h)$, so both statistics tend to $\chi^2_h$ (proved in [proofs/correctness.md](proofs/correctness.md)). For residuals of a fitted ARMA($p$, $q$) model, the law of $Q$ is approximately $\chi^2_{h - p - q}$ when $h$ is large and $h/n$ is small (Box and Pierce 1970). This is an approximation, not a limit theorem for fixed $h$.

**Rejection rule and size.** Reject when $Q \ge \chi^2_{(h - s,\ 1 - \alpha)}$, the upper $\alpha$ point. The size tends to $\alpha$ for a raw IID series. For finite $n$ it is not controlled: the measured sizes below show $Q_{\mathrm{LB}}$ a little above $\alpha$ and $Q_{\mathrm{BP}}$ below it.

**P-values.** $p = P(\chi^2_{h - s} > Q)$, the upper tail only.

**Sensitivity and power.** The test spreads its power over $h$ lags. Against a departure at lag 1 alone, a large $h$ adds noise from lags that carry no signal, and the power falls. A small $h$ misses seasonal or long-lag structure. A common choice is $h$ near $\log n$ or $\min(10, n/5)$, and $h = 2s$ or $3s$ for seasonal period $s$, but there is no rule that is best for all alternatives.

## The algorithm

```pseudo id=main
LJUNG-BOX(e[1..n], h, s)
L1  ē ← (e[1] + ... + e[n]) / n
L2  c0 ← Σ_{t=1}^{n} (e[t] - ē)²
L3  for k ← 1 to h do r[k] ← Σ_{t=k+1}^{n} (e[t] - ē)(e[t-k] - ē) / c0
L4  Q ← n(n + 2) · Σ_{k=1}^{h} r[k]² / (n - k)       ▷ Box-Pierce: Q ← n · Σ r[k]²
L5  df ← h - s                                        ▷ s = p + q fitted ARMA coefficients
L6  return (Q, df, P(χ²_df > Q))
```

The caller passes the residuals and the number $s$ of fitted ARMA coefficients (`fitted` in the code). The mean, a regression intercept or a drift is not counted in $s$. The code computes the Box-Pierce statistic with `statistic="box-pierce"`. Line L6 uses `chi2_sf` from the shared helper module, the regularized upper incomplete gamma function $Q(\mathrm{df}/2, Q/2)$. The code raises an error if $h \ge n$, if $h \le s$, or if the series is constant.

## Example

Take the ten values $e = (3, 5, 6, 4, 2, 1, 3, 6, 7, 5)$ as a raw series and test $h = 3$ lags. The mean is $\bar e = 4.2$ and $\sum (e_t - \bar e)^2 = 33.6$.

| $k$ | $\hat r_k$ | $\hat r_k^2$ | Ljung-Box weight $n(n + 2)/(n - k)$ | Box-Pierce weight $n$ |
|---|---|---|---|---|
| 1 | $69/140 = 0.4929$ | 0.2429 | 13.33 | 10 |
| 2 | $-89/280 = -0.3179$ | 0.1010 | 15.00 | 10 |
| 3 | $-523/840 = -0.6226$ | 0.3877 | 17.14 | 10 |

Then $Q_{\mathrm{LB}} = 11.3998$ on 3 degrees of freedom, with $p = 0.0097$, and $Q_{\mathrm{BP}} = 7.3160$, with $p = 0.0625$. The Ljung-Box test rejects at $\alpha = 0.05$ and the Box-Pierce test does not. With $n = 10$ neither chi-square approximation is reliable; the example only shows how much the weights matter for a short series. The tests check the three autocorrelations against these fractions, and both statistics against an exact `Fraction` computation on random integer series.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). For IID $e_t$ with mean $\mu$ and variance $\sigma^2$, the products $(e_t - \mu)(e_{t-k} - \mu)$, $k = 1, \ldots, h$, form a stationary martingale difference sequence with covariance $\sigma^4 I_h$. The martingale [central limit theorem](/central-limit-theorem/) gives $\sqrt{n}(\hat r_1, \ldots, \hat r_h) \to N(0, I_h)$, after showing that replacing $\mu$ by $\bar e$ changes nothing in the limit. So $Q_{\mathrm{BP}} \to \chi^2_h$, and $Q_{\mathrm{LB}} - Q_{\mathrm{BP}} \to 0$ in probability. The proof also gives the reason for the weights: for IID normal data with known mean 0 (no centering), $\mathrm{Var}(\hat r_k) = (n - k)/(n(n + 2))$ exactly and the $\hat r_k$ are uncorrelated, so $\mathbb{E}[Q_{\mathrm{LB}}] = h$ exactly, while $\mathbb{E}[Q_{\mathrm{BP}}] = \sum_{k=1}^{h}(n - k)/(n + 2) < h$. For $n = 30$ and $h = 10$, $\mathbb{E}[Q_{\mathrm{BP}}] = 245/32 = 7.66$ instead of 10, so its size is too small. The degrees of freedom $h - p - q$ for residuals are cited from Box and Pierce (1970), not proved.

## Complexity

Lines L1 and L2 take $\Theta(n)$ time and L3 takes $\Theta(n h)$, so the test takes $\Theta(n h)$ time. The code keeps the centred series, $\Theta(n)$ extra space. For many lags, all $n - 1$ autocorrelations can be computed in $O(n \log n)$ with a [fast Fourier transform](/fast-fourier-transform/) of the zero-padded series. The p-value is one evaluation of the incomplete gamma function. In practice the cost of the test is small next to the cost of fitting the model.

## Properties

- **Size for a raw IID series (measured).** IID $N(0, 1)$ series, $h = 10$, 10 degrees of freedom, $\alpha = 0.05$, 4000 series per row (seed 11). The Monte Carlo standard error is about 0.0035.

  | $n$ | size of Ljung-Box | size of Box-Pierce |
  |---|---|---|
  | 30 | 0.0785 | 0.0270 |
  | 50 | 0.0668 | 0.0353 |
  | 100 | 0.0553 | 0.0370 |
  | 200 | 0.0535 | 0.0455 |

  Both sizes approach 0.05. The Ljung-Box test is a little liberal for small $n$, and the Box-Pierce test is conservative.
- **Residuals of a fitted AR(1) (measured).** AR(1) series with $n = 100$, fitted by the [Yule-Walker equations](/yule-walker-equations/), $h = 10$, $\alpha = 0.05$ (seed 12):

  | true $\phi$ | Ljung-Box, df 9 | Ljung-Box, df 10 | Box-Pierce, df 9 |
  |---|---|---|---|
  | 0.5 | 0.0450 | 0.0295 | 0.0278 |
  | 0.9 | 0.0498 | 0.0333 | 0.0338 |

  With the correct $h - p = 9$ degrees of freedom, the Ljung-Box size is close to 0.05. With the raw-series value of 10, the test is conservative, because fitting a parameter makes the residual autocorrelations at small lags smaller than for IID noise.
- **Power depends on $h$ (measured).** Raw AR(1) series with $\phi = 0.2$, $n = 100$, $\alpha = 0.05$ (seed 13): the power was 0.461 for $h = 1$, 0.263 for $h = 5$, 0.207 for $h = 10$ and 0.199 for $h = 20$. All the signal is at lag 1, so each extra lag only adds noise.
- **Invariant to scale and location.** Adding a constant to the series or multiplying it by a nonzero constant does not change $\hat r_k$, so $Q$ does not depend on $\mu$ or $\sigma$.
- **Not consistent against all dependence.** A process with $\rho(1) = \cdots = \rho(h) = 0$ but dependence in the squares, such as an ARCH or [GARCH](/garch-model/) process, has power close to $\alpha$. Apply the test to the squared residuals to detect it.

## Variants and improvements

- **Box-Pierce statistic.** $n \sum \hat r_k^2$, the original form. It has the same limit, but its size is too small in short series. The code computes it with `statistic="box-pierce"`.
- **McLeod-Li test.** The same statistic computed on the squared residuals, as a check for conditional heteroscedasticity (McLeod and Li 1983).
- **Multivariate portmanteau test.** For vector series, Hosking (1980) and Li and McLeod (1981) replaced $\hat r_k^2$ by $\operatorname{tr}(\hat C_k^\top \hat C_0^{-1} \hat C_k \hat C_0^{-1})$, with $\hat C_k$ the residual autocovariance matrices, and $h k^2 - $ (number of fitted coefficients) degrees of freedom.
- **Partial autocorrelation form.** Monti (1994) used the residual [partial autocorrelations](/partial-autocorrelation-function/) in the same weighted sum. It can have more power against MA alternatives.
- **Lagrange multiplier test.** The [score test](/score-test/) of the fitted model against a larger ARMA model is aimed at one direction and is often more powerful against that direction. Breusch and Godfrey gave a regression form for the residuals of a regression model.
- **Monte Carlo p-value.** For a short series, simulate the fitted model many times, refit it to each simulated series, compute $Q$, and use $(1 + \text{count})/(1 + B)$. This removes the error of the chi-square approximation at the cost of $B$ refits.

## When to use it

Use it as the standard residual check in the [Box-Jenkins method](/box-jenkins-method/), together with a plot of the residual autocorrelations with bands of $\pm 1.96/\sqrt{n}$, and as a quick test that a raw series has no autocorrelation. A large p-value says only that the test did not detect a misfit at lags $1$ to $h$. For regression residuals with a fixed design and no lagged dependent variable, the [Durbin-Watson test](/durbin-watson-test/) tests lag 1, and its null law can be computed exactly for the given design. For volatility clustering, test the squared residuals.

## Pitfalls

- **Degrees of freedom.** Use $h - p - q$ for the residuals of an ARMA($p$, $q$) fit, not $h$. The mean, a constant and regression coefficients on exogenous variables are not counted, and the $h - p - q$ rule is itself only an approximation that needs $h$ well above $p + q$.
- **Residuals of a regression with a lagged dependent variable.** The chi-square approximation can be poor. A Lagrange multiplier test is better there.
- **Looking at many values of $h$.** Reporting the smallest p-value over $h = 1, \ldots, 20$ is a multiple-testing problem. Choose $h$ before looking, or adjust with a [Bonferroni correction](/bonferroni-correction/).
- **Too large an $h$.** The power falls as $h$ grows, and the chi-square approximation needs $h$ much smaller than $n$.
- **Reading a large p-value as proof of the model.** Many models can pass the test, and the test does not see dependence in the squares, a change of variance over time, or a nonlinear structure.
- **Using the divisor $n - k$ in $\hat r_k$.** The formula above uses the divisor $n$, as in Ljung and Box (1978). Other conventions change $Q$ for short series.

## Implementations

## History

Box and Pierce (1970) studied the residual autocorrelations of a fitted ARIMA model. They showed that these have a smaller variance than the autocorrelations of IID noise at small lags, and that $n\sum_{k=1}^h \hat r_k^2$ is approximately $\chi^2_{h - p - q}$ when $h$ is moderately large. The statistic became part of the diagnostic stage of the Box-Jenkins method published the same year. Simulations in the 1970s showed that its size is much too small in series of the usual length. Ljung and Box (1978) replaced $\hat r_k^2$ by $\hat r_k^2 (n + 2)/(n - k)$, using the exact variance of $\hat r_k$ for normal noise, and showed that the new statistic has a law much closer to chi-square. The Ljung-Box statistic is now the default portmanteau test in most statistical software. McLeod and Li (1983) applied it to squared residuals, and Hosking (1980) extended it to vector series.

## References
