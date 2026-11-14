---
tag: 0PTARQ
kind: definition
slug: granger-causality
name: Granger causality
aliases:
- Granger causality test
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: X Granger-causes Y when past values of X improve the prediction of Y beyond the past of Y alone. It is tested by an F-test in a vector autoregression.
prereqs: [vector-autoregression, regression-f-test]
see_also: [structural-causal-model, potential-outcomes-framework, wald-test, cointegration, impulse-response, likelihood-ratio-test, akaike-information-criterion, augmented-dickey-fuller-test]
sources:
  - paper: doi:10.2307/1912791
    title: C. W. J. Granger, Investigating causal relations by econometric models and cross-spectral methods, Econometrica 37(3) (1969), pages 424 to 438
    locator: the definitions of causality, feedback and instantaneous causality by the variance of the prediction error
  - paper: "Christopher A. Sims, Money, income, and causality, American Economic Review 62(4) (1972), pages 540 to 552"
    title: Christopher A. Sims, Money, income, and causality, American Economic Review 62(4) (1972), pages 540 to 552
    locator: the equivalence of Granger noncausality with zero coefficients on future values in a two-sided distributed lag
  - paper: doi:10.1080/01621459.1982.10477803
    title: John Geweke, Measurement of linear dependence and feedback between multiple time series, Journal of the American Statistical Association 77(378) (1982), pages 304 to 313
    locator: the measures of linear feedback in each direction and of instantaneous feedback
  - paper: doi:10.1016/0304-4076(94)01616-8
    title: Hiro Y. Toda and Taku Yamamoto, Statistical inference in vector autoregressions with possibly integrated processes, Journal of Econometrics 66(1-2) (1995), pages 225 to 250
    locator: the VAR in levels with extra lags, whose Wald test on the original lags is asymptotically chi-square with unit roots or cointegration
  - paper: doi:10.2307/2999631
    title: Jean-Marie Dufour and Eric Renault, Short run and long run causality in time series, theory, Econometrica 66(5) (1998), pages 1099 to 1125
    locator: causality at horizon h, and how noncausality one step ahead can fail to imply noncausality further ahead with three or more series
  - paper: doi:10.1016/0304-4076(88)90045-0
    title: C. W. J. Granger, Some recent development in a concept of causality, Journal of Econometrics 39(1-2) (1988), pages 199 to 211
    locator: cointegrated series must have Granger causality in at least one direction
  - book: isbn:9783540401728
    title: Helmut Lütkepohl, New Introduction to Multiple Time Series Analysis, Springer, 2005
    locator: Section 2.3 (Granger causality and instantaneous causality in a VAR) and Chapter 3 (Wald tests of the restrictions)
  - paper: doi:10.2307/2938337
    title: Christopher A. Sims, James H. Stock and Mark W. Watson, Inference in linear time series models with some unit roots, Econometrica 58(1) (1990), pages 113 to 144
    locator: the nonstandard limit laws of Wald tests in VARs in levels with unit roots
---

Granger causality is a statement about prediction. A series $X$ Granger-causes a series $Y$ if the past of $X$ helps to forecast $Y$ beyond what the past of $Y$ (and of any other series in the information set) already gives. It is named after Clive Granger, who defined it in 1969 by comparing the variances of prediction errors. In a [vector autoregression](/vector-autoregression/) it holds exactly when some lag coefficient of $X$ in the equation for $Y$ is nonzero, so it is tested by an F or [Wald test](/wald-test/) on those coefficients. Despite the name, it is not causation in the sense of interventions: a hidden common cause, or a variable that reacts to expectations, produces Granger causality with no causal effect at all. For causal effects use a [structural causal model](/structural-causal-model/) or the [potential outcomes framework](/potential-outcomes-framework/).

## Definition

Let $\{(Y_t, X_t, Z_t)\}$ be jointly [stationary](/stationary-process/) with finite variances, where $Z$ holds any other series in the information set. Let $\mathcal{H}_{t}$ be the closed linear span of $\{Y_s, X_s, Z_s : s \le t\}$ and $\mathcal{H}_{t}^{-X}$ the span without the $X$ terms. For a space $\mathcal{G}$, let $\sigma^2(Y_{t+1} \mid \mathcal{G})$ be the mean squared error of the best linear predictor of $Y_{t+1}$ in $\mathcal{G}$ (plus a constant).

1. $X$ **Granger-causes** $Y$ (with respect to the information set) if $\sigma^2(Y_{t+1} \mid \mathcal{H}_t) < \sigma^2(Y_{t+1} \mid \mathcal{H}_t^{-X})$. Otherwise $X$ does **not** Granger-cause $Y$, and the two variances are equal.
2. There is **feedback** if $X$ Granger-causes $Y$ and $Y$ Granger-causes $X$.
3. There is **instantaneous causality** between $X$ and $Y$ if adding the current $X_{t+1}$ to $\mathcal{H}_t$ lowers the error variance for $Y_{t+1}$. This happens exactly when the innovations of $X$ and $Y$ are correlated, so it has no direction.
4. $X$ **causes $Y$ at horizon $h$** if the past of $X$ lowers the error variance of the $h$-step forecast of $Y_{t+h}$ (Dufour and Renault 1998).

The nonlinear version replaces linear predictors by conditional distributions: $X$ does not Granger-cause $Y$ when $Y_{t+1}$ is conditionally independent of $(X_s)_{s \le t}$ given $(Y_s, Z_s)_{s \le t}$. The definition always depends on the information set: adding or removing a series $Z$ can create or destroy Granger causality between $X$ and $Y$.

**In a VAR.** Let $(Y_t, X_t)$ follow a stable VAR($p$), with blocks $A_i^{YX}$ of the coefficient matrices and $\Sigma$ positive definite. Then $X$ does not Granger-cause $Y$ if and only if $A_i^{YX} = 0$ for $i = 1..p$. The "if" part has a short proof: if all $A_i^{YX} = 0$, the $Y$ equations read $Y_t = c_Y + \sum_iA_i^{YY}Y_{t-i} + \varepsilon_{Yt}$, and $\varepsilon_{Yt}$ is uncorrelated with all past values. So the best linear predictor from the full past is $c_Y + \sum_iA_i^{YY}Y_{t-i}$, which uses only the past of $Y$, and both error variances equal $\Sigma_{YY}$. The same closed form shows more: the $Y$ block is then a VAR on its own, so the $h$-step forecasts of $Y$ also use only its own past, and $X$ does not cause $Y$ at any horizon. The "only if" part, that a nonzero coefficient strictly lowers the error variance, is in Lütkepohl (2005, Section 2.3). Instantaneous causality is the condition $\Sigma_{YX} \neq 0$.

### The test

The usual test fits a VAR($p$) and tests $H_0$: $A_1^{YX} = \cdots = A_p^{YX} = 0$.

- **Bivariate F form.** Regress $Y_t$ on a constant, $Y_{t-1}, \dots, Y_{t-p}$ and $X_{t-1}, \dots, X_{t-p}$ over $T'$ usable rows (unrestricted, residual sum of squares $\mathrm{RSS}_u$), and again without the $X$ lags ($\mathrm{RSS}_r$). The statistic is
$$F = \frac{(\mathrm{RSS}_r - \mathrm{RSS}_u)/p}{\mathrm{RSS}_u/(T' - 2p - 1)},$$
the [regression F-test](/regression-f-test/) of the $p$ lag coefficients. Reject for large $F$.
- **Wald form.** In a VAR with $K$ series, write the restrictions as $R\operatorname{vec}B = 0$ and use $W = (R\operatorname{vec}\hat B)^\top\left[R(\hat\Sigma \otimes (X^\top X)^{-1})R^\top\right]^{-1}(R\operatorname{vec}\hat B)$, with $\hat B$ the equation-by-equation least squares estimate.
- **Null distribution.** The regressors include lagged $Y$, so the F law is not exact even with Gaussian errors. For a stable VAR with IID errors, $W$ and $pF$ converge to $\chi^2_p$ (Lütkepohl 2005, Chapter 3); the $F(p, T' - 2p - 1)$ reference is a common small-sample choice.
- **Unit roots.** If the series are integrated, the Wald test in a VAR in levels can have a nonstandard law (Sims, Stock and Watson 1990). Differencing is wrong if the series are cointegrated. Toda and Yamamoto (1995) fit a VAR($p + d_{\max}$) in levels, where $d_{\max}$ is the highest order of integration, and test only the first $p$ lags of $X$; that Wald statistic is asymptotically $\chi^2_p$ whatever the integration and cointegration.
- **Lag length.** Choose $p$ by an information criterion such as the [Akaike information criterion](/akaike-information-criterion/), and check that the residuals are white. Too few lags leave the omitted dynamics in the errors and can create or hide causality.
- **Strength.** Geweke (1982) measures the size of the effect by $F_{X \to Y} = \log(\sigma^2(Y_{t+1} \mid \mathcal{H}_t^{-X})/\sigma^2(Y_{t+1} \mid \mathcal{H}_t))$, which is 0 exactly under noncausality.

**Measured size and power.** All runs use seed 2026 and $r = 2000$ samples of $T = 200$ points (after a burn-in of 100), $p = 1$, an intercept, and the 5% point 3.889 of $F(1, 196)$. The VAR is $Y_{1t} = 0.5Y_{1,t-1} + aY_{2,t-1} + \varepsilon_{1t}$, $Y_{2t} = 0.5Y_{2,t-1} + \varepsilon_{2t}$ with independent standard Gaussian errors, and the test is of $Y_2$ to $Y_1$.

| setting | rejection rate |
|---|---|
| $a = 0$ (null true) | 0.0575 |
| $a = 0.1$ | 0.3525 |
| $a = 0.2$ | 0.886 |
| two independent random walks, VAR(1) in levels (null true) | 0.1665 |
| two independent random walks, Toda-Yamamoto VAR(2), test of lag 1 only | 0.0495 |

With $r = 2000$, the Monte Carlo standard error at 0.05 is 0.005. The stationary null rate 0.0575 is within 2 standard errors of 0.05. The levels test on random walks rejects a true null three times too often, while the Toda-Yamamoto version keeps its size. In one sample with $a = 0.5$, $F = 53.85$ for $Y_2$ to $Y_1$, and $F = 0.467$ (p-value 0.495) for $Y_1$ to $Y_2$. These numbers are measured, not derived.

## Examples and non-examples

- **A VAR by hand.** Let $Y_{1t} = \frac12Y_{1,t-1} + \frac12Y_{2,t-1} + \varepsilon_{1t}$ and $Y_{2t} = \frac12Y_{2,t-1} + \varepsilon_{2t}$, with uncorrelated unit-variance errors. Then $Y_2$ Granger-causes $Y_1$ and $Y_1$ does not Granger-cause $Y_2$ (the coefficient of $Y_1$ in the second equation is 0). In numbers: $\operatorname{Var}Y_2 = 1/(1 - \frac14) = 4/3$; the covariance $c = \operatorname{Cov}(Y_1, Y_2)$ solves $c = \frac14c + \frac14 \cdot \frac43$, so $c = 4/9$; and $\operatorname{Var}Y_1 = v$ solves $v = \frac14v + \frac14 \cdot \frac43 + 2 \cdot \frac14 \cdot \frac49 + 1$, so $v = 56/27$. With the full past, the one-step error variance for $Y_1$ is 1. With only $Y_{1,t-1}$, the predictor is $\frac{34/27}{56/27}Y_{1,t-1}$, because $\operatorname{Cov}(Y_{1t}, Y_{1,t-1}) = \frac12v + \frac12c = 34/27$, and its error variance is $56/27 - (34/27)^2/(56/27) = 55/42 \approx 1.3095$. With the whole past of $Y_1$, it is $(3 + \sqrt5)/4 \approx 1.3090$: here $(1 - \frac12B)^2Y_{1t}$ is an MA(1) with autocovariances 1.5 and $-0.5$, whose innovation variance is $-0.5/\theta$ with $\theta = (-3 + \sqrt5)/2$. Geweke's measure is $\log 1.309 = 0.269$.
- **A hidden common cause (not causation).** Let $W_t$, $u_t$ and $v_t$ be independent white noise with variance 1, $X_t = W_{t-1} + u_t$ and $Y_t = W_{t-2} + v_t$. The past of $Y$ is uncorrelated with $Y_t$, so its own-past error variance is $\operatorname{Var}Y_t = 2$. Adding $X_{t-1} = W_{t-2} + u_{t-1}$, with covariance 1 and variance 2, lowers it to $2 - \frac12 = 1.5$. So $X$ Granger-causes $Y$. But $Y$ is not a function of $X$: setting $X$ to any value by intervention leaves $Y$ unchanged. If $W$ is added to the information set, the causality disappears.
- **Expectations (reverse direction).** Weather forecasts Granger-cause rain, and stock prices Granger-cause dividends, because the first series reacts to information about the second before the second happens.
- **Noncausality at one step but not at two.** With three series, let $X_t$ be white noise, $Z_t = X_{t-1} + e_{1t}$ and $Y_t = Z_{t-1} + e_{2t}$. Given the past of $Y$ and $Z$, the past of $X$ does not help to forecast $Y_{t+1} = Z_t + e_{2,t+1}$. But $Y_{t+2} = X_t + e_{1,t+1} + e_{2,t+2}$, so $X_t$ helps two steps ahead. This is why Dufour and Renault (1998) define causality at each horizon. With two series, noncausality at one step implies it at all horizons, as shown above.
- **Cointegration forces causality.** If $Y_1$ and $Y_2$ are [cointegrated](/cointegration/) with $\nabla Y_t = \alpha\beta^\top Y_{t-1} + \sum_{i=1}^{p-1}\Gamma_i\nabla Y_{t-i} + \varepsilon_t$, $\beta = (1, -b)^\top$, $b \neq 0$ and $\alpha \neq 0$, then the levels VAR has $\sum_iA_i = I + \alpha\beta^\top$. Its off-diagonal entries are $-\alpha_1b$ and $\alpha_2$, and at least one of them is nonzero. So some off-diagonal lag coefficient is nonzero, and there is Granger causality in at least one direction (Granger 1988).
- **Non-example: only instantaneous correlation.** If $(Y_t, X_t)$ is white noise with $\operatorname{Corr}(Y_t, X_t) = 0.8$, neither series Granger-causes the other, because no past value helps. There is instantaneous causality, which has no direction.
- **Non-example: missed by sampling.** If $X$ affects $Y$ within an hour and the data are daily, the effect shows up as instantaneous correlation, and Granger causality may be absent at the daily frequency. Temporal aggregation and skip sampling can also create causality in the wrong direction.

## Related definitions

- **Sims causality.** Sims (1972) showed that, for jointly stationary series under regularity conditions, $Y$ does not Granger-cause $X$ if and only if, in the regression of $Y_t$ on past, current and future values of $X$, all coefficients on future $X$ are 0. This gives a second test.
- **[Structural causal model](/structural-causal-model/).** Causation means that intervening on $X$ changes the distribution of $Y$. In a time-series structural causal model, a lagged edge from $X$ to $Y$ shows up as Granger causality given all other series only under strong assumptions: every common cause is observed, there are no effects within one sampling period, and the lag length is right. Without them, Granger causality and causation can differ in both directions, as the examples show.
- **[Potential outcomes framework](/potential-outcomes-framework/).** A causal effect compares outcomes under different treatments. Granger causality is a property of the observed joint distribution and makes no statement about outcomes under a treatment that was not given.
- **[Vector autoregression](/vector-autoregression/) and [impulse responses](/impulse-response/).** Granger noncausality is a zero restriction on the VAR coefficients. Then the response of $Y$ to every shock that enters only $X$ is 0 at all horizons in a bivariate system.
- **Feedback measures.** Geweke (1982) splits the total linear dependence between $X$ and $Y$ into feedback from $X$ to $Y$, feedback from $Y$ to $X$ and instantaneous feedback, and gives a frequency-domain version.
- **[Cointegration](/cointegration/).** Cointegrated series have causality in at least one direction, and the test must then use the Toda-Yamamoto setup or the error correction form.

## References
