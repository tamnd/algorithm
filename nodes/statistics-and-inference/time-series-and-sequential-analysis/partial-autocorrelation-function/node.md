---
tag: NZ70YH
kind: definition
slug: partial-autocorrelation-function
name: Partial autocorrelation function
aliases:
- PACF
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: The correlation of X_t and X_(t+k) after removing the linear effect of the values between them. It cuts off after lag p for an AR(p) process.
prereqs: [stationary-process, linear-prediction]
see_also: [autoregressive-model, moving-average-model, yule-walker-equations, levinson-durbin-recursion, burg-method, box-jenkins-method, autocorrelation, akaike-information-criterion]
sources:
  - book: isbn:9780387974293
    title: "Peter J. Brockwell and Richard A. Davis, Time Series: Theory and Methods, second edition, Springer, 1991"
    locator: Section 3.4 (the partial autocorrelation function, pp. 98 to 102), Section 5.2 (the Durbin-Levinson algorithm, pp. 169 to 174) and Section 8.2 (the sample PACF and AR order selection, p. 241)
  - book: isbn:9783319298528
    title: Peter J. Brockwell and Richard A. Davis, Introduction to Time Series and Forecasting, third edition, Springer, 2016
    locator: Section 2.5.3 (the Durbin-Levinson algorithm, p. 60) and Section 3.2.3 (the partial autocorrelation function, p. 83)
  - paper: doi:10.1111/j.2517-6161.1949.tb00023.x
    title: M. H. Quenouille, Approximate tests of correlation in time-series, Journal of the Royal Statistical Society B 11(1), 1949
    locator: pp. 68 to 84 (the sample partial autocorrelations beyond the order of an autoregression are approximately independent with variance 1/n)
---

The partial autocorrelation function (PACF) of a [stationary process](/stationary-process/) gives, for each lag $h$, the correlation between $X_t$ and $X_{t+h}$ after the linear effect of the values between them, $X_{t+1}, \ldots, X_{t+h-1}$, is removed from both. It is written $\phi_{hh}$, because it is also the last coefficient of the best linear predictor of $X_{t+h}$ from its $h$ previous values. The [autocorrelation](/autocorrelation/) counts direct and indirect links: in an AR(1) process $X_t$ and $X_{t+2}$ are correlated only through $X_{t+1}$. The PACF counts only the direct link, so it is exactly zero after lag $p$ for an [AR($p$) process](/autoregressive-model/). This makes it the main tool for choosing the order of an autoregression.

## Definition

**Setting.** $\{X_t\}$ is weakly stationary with mean $\mu$, autocovariance $\gamma$ and autocorrelation $\rho$, and with $\gamma(0) > 0$ and $\gamma(h) \to 0$ as $h \to \infty$. These conditions make every covariance matrix $\Gamma_h = [\gamma(i - j)]_{i,j=1}^{h}$ nonsingular (Brockwell and Davis 1991, Section 5.1). Without loss of generality $\mu = 0$. For a set $S$ of times, $P_S Y$ is the best linear predictor of $Y$ from $\{X_s : s \in S\}$, that is the orthogonal projection onto their span, as on the [linear prediction](/linear-prediction/) page.

**Partial autocorrelation.** $\phi_{11} = \rho(1)$, and for $h \ge 2$, with $S = \{t+1, \ldots, t+h-1\}$,

$$\phi_{hh} = \operatorname{Corr}\big(X_{t+h} - P_S X_{t+h},\; X_t - P_S X_t\big).$$

It does not depend on $t$, and $\phi_{hh} = \phi_{-h,-h}$ by convention, so it is enough to give $h \ge 1$.

**Second form.** Let $\phi_h = (\phi_{h1}, \ldots, \phi_{hh})^\top$ be the coefficients of the best linear predictor of $X_{t+h}$ from the $h$ previous values: $P X_{t+h} = \phi_{h1} X_{t+h-1} + \cdots + \phi_{hh} X_t$. They solve $\Gamma_h \phi_h = (\gamma(1), \ldots, \gamma(h))^\top$, the Yule-Walker system of order $h$. Then $\phi_{hh}$, the coefficient of the most distant value, is the partial autocorrelation at lag $h$.

*Proof that the two forms agree.* Let $U = X_t - P_S X_t$. It is orthogonal to the span of $\{X_s : s \in S\}$, so the span of $X_t, X_{t+1}, \ldots, X_{t+h-1}$ is that span plus the line through $U$, an orthogonal sum. So the predictor of $X_{t+h}$ from all $h$ values is $P_S X_{t+h} + a U$ with $a = \mathbb{E}[X_{t+h} U]/\mathbb{E}[U^2]$. Since $P_S X_t$ lies in the span of $S$, the coefficient of $X_t$ in this predictor is $a$. Now $\mathbb{E}[X_{t+h} U] = \mathbb{E}[(X_{t+h} - P_S X_{t+h}) U]$, because $P_S X_{t+h} \perp U$. The process reversed in time, $X_{-t}$, has the same autocovariance, so $\mathbb{E}[(X_{t+h} - P_S X_{t+h})^2] = \mathbb{E}[U^2]$. Hence $a = \operatorname{Corr}(X_{t+h} - P_S X_{t+h}, U) = \phi_{hh}$. $\square$

**Sample PACF.** From data $x_1, \ldots, x_n$, the sample PACF $\hat\phi_{hh}$ is defined by the second form with the divisor-$n$ sample autocovariance $\hat\gamma$ in place of $\gamma$. That $\hat\Gamma_h$ is positive definite whenever the data are not all equal, so $\hat\phi_{hh}$ exists for $h < n$ and $|\hat\phi_{hh}| < 1$. The [Yule-Walker equations](/yule-walker-equations/) page computes all of them in $O(h^2)$ operations with the [Levinson-Durbin recursion](/levinson-durbin-recursion/).

**Basic facts.**

- $|\phi_{hh}| \le 1$, as a correlation. It is strictly less than 1 when $\Gamma_{h+1}$ is nonsingular.
- If $v_h = \mathbb{E}[(X_{t+h} - P X_{t+h})^2]$ is the error of the order-$h$ predictor, with $v_0 = \gamma(0)$, then $v_h = v_{h-1}(1 - \phi_{hh}^2)$. So $\phi_{hh}^2$ is the fraction of the remaining error removed by the $h$-th value. The errors decrease to the one-step error $\sigma^2$ of the [Wold decomposition](/wold-decomposition-theorem/).
- The map from $(\rho(1), \ldots, \rho(h))$ to $(\phi_{11}, \ldots, \phi_{hh})$ is one to one between the autocorrelations that make $\Gamma_{h+1}$ positive definite and the open cube $(-1, 1)^h$. So any values in $(-1, 1)$ are the partial autocorrelations of some stationary process. This follows from the product $\det \Gamma_{h+1} = \prod_{k=0}^{h} v_k$ and the recursion for $v_k$. The [Whittle likelihood](/whittle-likelihood/) code uses this map to search over causal AR models with no constraints.
- For an AR($p$) process, $\phi_{pp} = \phi_p$ and $\phi_{hh} = 0$ for $h > p$: the order-$h$ predictor for $h \ge p$ is $\phi_1 X_{t+h-1} + \cdots + \phi_p X_{t+h-p}$, so its last coefficient is 0 when $h > p$.
- **Quenouille's result.** For an AR($p$) process with IID noise, the sample values $\sqrt{n}\, \hat\phi_{hh}$ for $h > p$ are asymptotically independent $N(0, 1)$ (Quenouille 1949; Brockwell and Davis 1991, Section 8.2). So values outside $\pm 1.96/\sqrt{n}$ at lags past $p$ are rare under the model, and the usual plot draws these bounds.

## Examples and non-examples

- **AR(1).** $X_t = \phi X_{t-1} + \varepsilon_t$ with $|\phi| < 1$. The best predictor from any past window is $\phi X_{t-1}$, so $\phi_{11} = \phi$ and $\phi_{hh} = 0$ for $h \ge 2$. The autocorrelation $\rho(h) = \phi^h$ never reaches 0. With $\phi = 3/5$ the exact values are $3/5, 0, 0, \ldots$
- **AR(2).** With $\phi = (0.5, 0.3)$: $\phi_{11} = \rho(1) = 0.5/0.7 = 0.7143$, $\phi_{22} = \phi_2 = 0.3$, and $\phi_{hh} = 0$ for $h \ge 3$. Check $\phi_{22}$ from the formula $\phi_{22} = (\rho(2) - \rho(1)^2)/(1 - \rho(1)^2)$ with $\rho(2) = 0.6571$: $(0.6571 - 0.5102)/(1 - 0.5102) = 0.3$.
- **MA(1).** $X_t = \varepsilon_t + \theta \varepsilon_{t-1}$ with $|\theta| < 1$. The PACF never cuts off: $\phi_{hh} = -(-\theta)^h (1 - \theta^2)/(1 - \theta^{2(h+1)})$ (Brockwell and Davis 1991, Section 3.4). With $\theta = 1/2$ the exact values are $2/5, -4/21, 8/85, -16/341, \ldots$, with alternating signs and a geometric decay.
- **ARMA(1, 1).** With $\phi = 0.5$ and $\theta = 0.4$: $0.6923, -0.2557, 0.1010, -0.0403, \ldots$ Neither the autocorrelation nor the PACF cuts off.
- **A sample by hand.** $x = (3, 5, 6, 4, 2, 1, 3, 6, 7, 5)$, $n = 10$. The sample autocorrelations are $\hat\rho(1) = 1.656/3.36 = 69/140$ and $\hat\rho(2) = -1.068/3.36 = -89/280$. So $\hat\phi_{11} = 69/140 = 0.4929$, and
$$\hat\phi_{22} = \frac{\hat\rho(2) - \hat\rho(1)^2}{1 - \hat\rho(1)^2} = \frac{-6230/19600 - 4761/19600}{14839/19600} = -\frac{10991}{14839} = -0.7407.$$
The next value is $\hat\phi_{33} = 0.0443$. The bounds $\pm 1.96/\sqrt{10} = \pm 0.62$ suggest an AR(2) model, but ten points are far too few for this rule.
- **Non-example: the autocorrelation.** $\rho(h)$ is not $\phi_{hh}$ except at $h = 1$. In AR(1), $\rho(2) = \phi^2 \ne 0$ while $\phi_{22} = 0$.
- **Non-example: a coefficient of a fixed-order fit.** In the order-$p$ predictor, the coefficient $\phi_{pj}$ of lag $j < p$ is not $\phi_{jj}$. In the sample above, the order-2 fit has lag-1 coefficient $0.8579$, while $\hat\phi_{11} = 0.4929$. Only the last coefficient of each order is a partial autocorrelation.
- **Non-example: a deterministic process.** For the random sinusoid $X_t = A\cos(\omega t) + B\sin(\omega t)$ with $0 < \omega < \pi$, $\rho(h) = \cos(\omega h)$ and $\phi_{22} = (\cos 2\omega - \cos^2\omega)/\sin^2\omega = -1$. Then $X_{t+2} = 2\cos(\omega) X_{t+1} - X_t$ exactly, $\Gamma_3$ is singular, and $\phi_{hh}$ is not defined for $h \ge 3$. Here $\gamma(h)$ does not tend to 0, so the process is outside the setting.
- **Non-example: a random walk.** The sample PACF of a random walk path is close to 1 at lag 1 and small after, which looks like AR(1) with $\phi$ near 1. But the random walk is not stationary, $\phi_{hh}$ is not defined for it, and the sample values do not estimate a fixed function. Difference the series first, as the [ARIMA model](/arima-model/) does.

## Related definitions

- **Partial correlation.** For random variables $Y$, $Z$ and a vector $W$, the partial correlation of $Y$ and $Z$ given $W$ is the correlation of the residuals of the linear regressions of $Y$ and $Z$ on $W$. The PACF is the partial correlation of $X_{t+h}$ and $X_t$ given the values between them. For Gaussian processes it equals the conditional correlation.
- **Reflection coefficients.** In signal processing the partial autocorrelations are the reflection coefficients of the lattice prediction filter, with the opposite sign in the usual convention: the coefficient $\alpha_k$ on the [Levinson-Durbin recursion](/levinson-durbin-recursion/) page is $-\phi_{k+1,k+1}$. The [Burg method](/burg-method/) estimates them directly from the data.
- **Prediction error variances.** $v_h$, the error of the order-$h$ predictor, is the quantity that the Akaike-type order selection criteria compare across orders, for example through the term $n \log v_h$ in the [Akaike information criterion](/akaike-information-criterion/) of an AR($h$) fit.
- **Inverse autocorrelation.** The autocorrelation of the process whose spectral density is $1/f$. For an AR($p$) process it cuts off after lag $p$, like the PACF, but it is a different function.
- **Autocorrelation function.** The ordinary [autocorrelation](/autocorrelation/) $\rho(h)$, which cuts off after lag $q$ for an [MA($q$) process](/moving-average-model/). The pair of plots, autocorrelation and PACF, is the identification step of the [Box-Jenkins method](/box-jenkins-method/).

## References
