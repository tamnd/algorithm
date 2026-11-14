---
tag: AWK28P
kind: algorithm
slug: kpss-test
name: KPSS test
aliases:
- Kwiatkowski-Phillips-Schmidt-Shin test
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: Tests the null of stationarity around a level or trend against a unit root, by the partial sums of residuals. It complements the Dickey-Fuller test.
model: real-ram
complexity:
  vars: {n: the length of the series, l: the truncation lag of the long-run variance}
  time: {worst: Θ(n (l + 1)), best: Θ(n (l + 1))}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1992
  people: [Denis Kwiatkowski, Peter C. B. Phillips, Peter Schmidt, Yongcheol Shin]
  note: Kwiatkowski, Phillips, Schmidt and Shin (1992) turned the score test of Nyblom and Makelainen (1983) for a random walk component into a test of stationarity that allows serial correlation, by a nonparametric long-run variance.
prereqs: [augmented-dickey-fuller-test, stationary-process, statistical-hypothesis-test]
see_also: [power-spectral-density, cusum, change-point-detection, arima-model, ljung-box-test, block-bootstrap]
sources:
  - paper: doi:10.1016/0304-4076(92)90104-Y
    title: Denis Kwiatkowski, Peter C. B. Phillips, Peter Schmidt and Yongcheol Shin, Testing the null hypothesis of stationarity against the alternative of a unit root, Journal of Econometrics 54(1-3) (1992), pages 159 to 178
    locator: the components model, the LM statistic, the limits as integrals of Brownian bridges, and Table 1 (page 166) of upper tail critical values
  - paper: doi:10.1080/01621459.1983.10477032
    title: Jukka Nyblom and Timo Makelainen, Comparisons of tests for the presence of random walk coefficients in a simple linear model, Journal of the American Statistical Association 78(384) (1983), pages 856 to 864
    locator: the locally best invariant test of a zero random walk variance, the level case of the KPSS statistic
  - paper: doi:10.2307/1913610
    title: Whitney K. Newey and Kenneth D. West, A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix, Econometrica 55(3) (1987), pages 703 to 708
    locator: the Bartlett weights and the proof that the estimate is nonnegative
  - paper: doi:10.1214/aoms/1177729437
    title: T. W. Anderson and D. A. Darling, Asymptotic theory of certain goodness of fit criteria based on stochastic processes, Annals of Mathematical Statistics 23(2) (1952), pages 193 to 212
    locator: the law of the integral of a squared Brownian bridge (the Cramer-von Mises limit) and its percentage points
  - paper: doi:10.1214/aos/1176344133
    title: Ian B. MacNeill, Properties of sequences of partial sums of polynomial regression residuals with applications to tests for change of regression at unknown times, Annals of Statistics 6(2) (1978), pages 422 to 433
    locator: the limit of partial sums of residuals from a polynomial regression (the second-level Brownian bridge of the trend case)
  - paper: doi:10.1111/j.1467-9574.2004.00272.x
    title: Bart Hobijn, Philip Hans Franses and Marius Ooms, Generalizations of the KPSS-test for stationarity, Statistica Neerlandica 58(4) (2004), pages 483 to 502
    locator: the automatic bandwidth choice for the long-run variance
---

The KPSS test checks whether a time series is stationary around a constant level, or around a straight line, against the alternative that it contains a unit root. It is the reverse of the [augmented Dickey-Fuller test](/augmented-dickey-fuller-test/), whose null is the unit root. The statistic removes the level (or the line) by least squares, adds up the residuals into a running sum $S_t$, and compares the size of that sum with the long-run variance of the residuals: $\eta = \sum_t S_t^2/(n^2 \hat\sigma^2_{\mathrm{LR}})$. A stationary series gives partial sums that keep returning to zero, so $\eta$ stays small. A random walk component makes the partial sums drift, and $\eta$ grows with $n$. Under the null, $\eta$ tends to the integral of a squared Brownian bridge, the same law as the Cramer-von Mises goodness-of-fit statistic.

## In plain words

Draw the best flat line (or the best sloped line) through the series. Then walk along the series and keep a running total of how far each point is above or below the line. If the series really moves around that line, the total goes up and down and keeps coming back near zero. If the series wanders away and does not come back, the total builds up in one direction for long stretches. The test measures how large this running total gets, compared with the normal size of the swings in the data, and calls the series not stationary when the running total is too large. Because nearby points in a series are often alike, the normal size of the swings is measured with that likeness taken into account.

## The problem

**Model and hypotheses.** KPSS write the series as a sum of a deterministic trend, a random walk and a stationary error:
$$X_t = \xi t + r_t + \varepsilon_t, \qquad r_t = r_{t-1} + u_t, \qquad t = 1, \dots, n,$$
with $u_t$ iid $(0, \sigma_u^2)$ and $\varepsilon_t$ a [stationary process](/stationary-process/) with long-run variance $\sigma^2 = \sum_{h \in \mathbb Z}\gamma(h) = 2\pi f(0)$, where $f$ is the [power spectral density](/power-spectral-density/) of $\varepsilon_t$. The initial value $r_0$ is a fixed intercept. The null hypothesis is $H_0: \sigma_u^2 = 0$, so $X_t$ is stationary around a line (case "ct") or, when $\xi = 0$ is imposed, around a level (case "c"). The alternative is $H_1: \sigma_u^2 > 0$, a unit root.

**Statistic.** Let $e_t$ be the residuals of the least squares regression of $X_t$ on $1$ (case "c") or on $1$ and $t$ (case "ct"), $S_t = \sum_{s=1}^{t}e_s$, and
$$\hat\sigma^2(\ell) = \hat\gamma_0 + 2\sum_{j=1}^{\ell}\left(1 - \frac{j}{\ell + 1}\right)\hat\gamma_j, \qquad \hat\gamma_j = \frac1n\sum_{t=j+1}^{n}e_te_{t-j}.$$
The statistic is $\eta = \sum_{t=1}^{n}S_t^2\big/\left(n^2\hat\sigma^2(\ell)\right)$. The weights $1 - j/(\ell + 1)$ are the Bartlett (Newey-West) weights. With Gaussian iid $\varepsilon_t$ and $\ell = 0$, $\eta$ is the Lagrange multiplier (score) statistic for $\sigma_u^2 = 0$ (Nyblom and Makelainen 1983).

**Null distribution.** Asymptotic. If $\ell \to \infty$ and $\ell/n \to 0$ (or $\ell = 0$ with iid errors), then under $H_0$
$$\eta \Rightarrow \int_0^1 V(r)^2\,dr,$$
where $V(r) = W(r) - rW(1)$ is a Brownian bridge in case "c", and in case "ct" the second-level bridge $V_2$ with covariance $K(s, t) = \min(s, t) - 4st + 3st^2 + 3s^2t - 3s^2t^2$ (MacNeill 1978). The law is a weighted sum $\sum_k \lambda_k Z_k^2$ of independent squared normals, with $\lambda_k$ the eigenvalues of the covariance kernel. In case "c", $\lambda_k = 1/(k^2\pi^2)$, which is the Cramer-von Mises limit. The mean is $1/6$ in case "c" and $1/15$ in case "ct". These limits are cited from KPSS (1992), not proved here.

**Rejection rule and size.** Reject at level $\alpha$ when $\eta$ exceeds the upper $\alpha$ point:

| case | 10% | 5% | 2.5% | 1% |
|---|---|---|---|---|
| "c", KPSS Table 1 | 0.347 | 0.463 | 0.574 | 0.739 |
| "c", exact limit (Anderson and Darling 1952) | 0.3473 | 0.4614 | 0.5806 | 0.7435 |
| "ct", KPSS Table 1 | 0.119 | 0.146 | 0.176 | 0.216 |
| "ct", limit computed from the kernel eigenvalues | 0.1193 | 0.1479 | 0.1775 | 0.2178 |

The KPSS values come from a simulation of the limit. The second and fourth rows are the quantiles of $\sum_k\lambda_kZ_k^2$ computed by numerical inversion of the characteristic function (Imhof's method); in case "ct" the eigenvalues were found numerically from $K$. The differences are below 0.005 and change no decision except at the boundary. The size is asymptotically $\alpha$. In finite samples it is close to $\alpha$ for iid errors, and too large when the errors are strongly autocorrelated and $\ell$ is small.

**p-value.** Interpolate in the table, which only gives $p$ between 0.01 and 0.10. In case "c" the implementation also gives the exact asymptotic tail $P(\sum_k Z_k^2/(k^2\pi^2) > \eta)$.

**Sensitivity and power.** The test reacts to a random walk component, and also to anything that makes the partial sums drift: a shift in level, a missed trend, or long memory. Under $H_1$ with $\ell/n \to 0$, $\eta$ grows at the rate $n/\ell$, so the test is consistent. A larger $\ell$ protects the size under autocorrelation, but it also divides the statistic, so the power falls.

## The algorithm

```pseudo id=main
KPSS(X₁..Xₙ, case, ℓ)                    ▷ case ∈ {c, ct}, 0 ≤ ℓ < n
L1  e ← residuals of X on 1 (case c) or on (1, t) (case ct)
L2  S_t ← e₁ + … + e_t for t = 1..n; N ← Σ_t S_t²
L3  γ̂_j ← (1/n) Σ_{t=j+1..n} e_t e_{t−j} for j = 0..ℓ
L4  σ̂² ← γ̂₀ + 2 Σ_{j=1..ℓ} (1 − j/(ℓ+1)) γ̂_j
L5  η ← N / (n² σ̂²)
L6  c ← upper α point for the case (table)
L7  return (η, reject ⇔ η > c)
```

KPSS proposed two bandwidths, $\ell_4 = \lfloor 4(n/100)^{1/4}\rfloor$ and $\ell_{12} = \lfloor 12(n/100)^{1/4}\rfloor$. At $n = 100$ these are 4 and 12, and at $n = 200$ they are 4 and 14. Hobijn, Franses and Ooms (2004) give a data-driven choice. Line L1 has a closed form: in case "c", $e_t = X_t - \bar X$; in case "ct", $e_t = X_t - \bar X - \hat b(t - \bar t)$ with $\hat b = \sum(t - \bar t)X_t/\sum(t - \bar t)^2$.

## Example

**By hand.** Take $X = (3, 5, 4, 6, 8, 7, 9, 8)$, the series of the [ADF example](/augmented-dickey-fuller-test/), in case "c". The mean is $6.25$:

| step | value |
|---|---|
| L1: $e_t$ | $-3.25, -1.25, -2.25, -0.25, 1.75, 0.75, 2.75, 1.75$ |
| L2: $S_t$ | $-3.25, -4.5, -6.75, -7, -5.25, -4.5, -1.75, 0$ |
| L2: $N = \sum S_t^2$ | $705/4 = 176.25$ |
| L3: $\hat\gamma_0, \hat\gamma_1, \hat\gamma_2$ | $63/16, 243/128, 77/64$ |
| L5: $\eta$ with $\ell = 0$ | $235/336 = 0.6994$ |
| L5: $\eta$ with $\ell = 1$ ($\hat\sigma^2 = 747/128$) | $235/498 = 0.4719$ |
| L5: $\eta$ with $\ell = 2$ ($\hat\sigma^2 = 349/48$) | $2115/5584 = 0.3788$ |

With $\ell = 0$ or $1$ the test rejects level stationarity at 5% ($\eta > 0.463$). With $\ell = 2$ it does not, and the table p-value is about 0.09. The partial sums stay negative for the whole sample, because the series rises: the first half is below the mean and the second half above. In case "ct" the line takes out the rise, the residuals are $-1/2, 5/7, -15/14, 1/7, 19/14, -3/7, 11/14, -1$, $N = 3$, and $\eta = 7/104 = 0.0673$ with $\ell = 0$, far below 0.146. So the data are compatible with stationarity around a line.

**A random walk against a stationary series.** The same 200 shocks as on the ADF page (seed 2026) give:

| series | $\ell$ | $\eta$ | table p-value |
|---|---|---|---|
| random walk | $\ell_4 = 4$ | 3.373 | $\le 0.01$ |
| random walk | $\ell_{12} = 14$ | 1.230 | $\le 0.01$ |
| AR(1), $\phi_1 = 0.5$ | $\ell_4 = 4$ | 0.116 | $\ge 0.10$ |
| AR(1), $\phi_1 = 0.5$ | $\ell_{12} = 14$ | 0.120 | $\ge 0.10$ |

Here the ADF and KPSS tests agree. For the random walk, the larger bandwidth cuts $\eta$ by almost two thirds.

**Size and power (measured, 500 to 2000 samples each).** With iid normal data and $\ell = 0$, the 5% rejection rate was 0.0545 at $n = 100$ and 0.0525 at $n = 400$ in case "c". Against a random walk the 5% power was 0.81 with $\ell_4$ and 0.62 with $\ell_{12}$ at $n = 100$, and 0.94 and 0.71 at $n = 200$. For a stationary AR(1) with $\phi_1 = 0.9$ and $n = 200$, the test wrongly rejected in 50% of samples with $\ell_4$ and 17% with $\ell_{12}$.

## Correctness

The correctness proof shows four facts. The residuals of line L1 sum to zero (and are orthogonal to $t$ in case "ct"), so $S_n = 0$ and the partial sums are a bridge from 0 to 0. The Bartlett estimate of line L4 equals $\frac{1}{n(\ell+1)}\sum_t\left(\sum_{i=0}^{\ell}e_{t+i}\right)^2$ with $e$ set to 0 outside $1..n$, so it is never negative, and lines L3 to L5 compute the stated $\eta$. The statistic is invariant to $X_t \mapsto a + cX_t$ (case "c") and to $X_t \mapsto a + bt + cX_t$ (case "ct"), for $c \ne 0$. For iid errors with variance $\sigma^2$ in case "c", $E\sum_tS_t^2 = \sigma^2(n^2 - 1)/6$ exactly, which matches the limit mean $1/6$. The Brownian bridge limits and the consistency under the alternative are cited from KPSS (1992).

## Complexity

On a [real RAM](/real-ram/), line L1 is one pass for the means and one for the slope, $\Theta(n)$. Line L2 is one pass. Line L3 computes $\ell + 1$ sums of at most $n$ products, $\Theta(n(\ell + 1))$. Lines L4 to L7 cost $\Theta(\ell)$. The total is $\Theta(n(\ell + 1))$ time, which is $\Theta(n^{5/4})$ for the $\ell_4$ and $\ell_{12}$ rules, and $\Theta(n)$ extra space for $e$. The autocovariances can also be computed for all lags at once by an FFT in $\Theta(n\log n)$.

**Numerical stability.** Compute $e_t$ from centered quantities ($X_t - \bar X$ and $t - \bar t$), not from the raw normal equations, because $\sum t^2$ and $(\sum t)^2$ are both of order $n^3$ to $n^4$ and their difference loses digits. The partial sums $S_t$ are sums of numbers of both signs whose total is zero, so their relative error is small only if $e_t$ is accurate.

## Properties

- **The reverse null.** Stationarity is the null and the unit root the alternative, the opposite of the ADF test. Used together, the pair can say "stationary", "unit root" or "the data cannot tell".
- **Locally best invariant.** In the Gaussian components model with iid errors and $\ell = 0$, the test is the locally best invariant test of $\sigma_u^2 = 0$ (Nyblom and Makelainen 1983).
- **Invariant.** $\eta$ does not depend on the level or the scale of the series, nor on an added line in case "ct".
- **Free of nuisance parameters in the limit.** The limit law depends only on the case, because $\hat\sigma^2(\ell)$ estimates the long-run variance consistently when $\ell \to \infty$ and $\ell/n \to 0$.
- **A Cramer-von Mises statistic.** In case "c", $\eta$ is the Cramer-von Mises statistic of the partial-sum process, so its limit is the same as that of the goodness-of-fit test, with 5% point 0.4614.
- **Sensitive to the bandwidth.** The value of $\eta$ can change by a factor of 2 or more between $\ell_4$ and $\ell_{12}$, as in the examples.

## Variants and improvements

- **Leybourne-McCabe test.** Model the short-run correlation by an ARMA fit instead of a nonparametric long-run variance. Its size is better when the autocorrelation is strong (Leybourne and McCabe 1994).
- **Automatic bandwidth.** Choose $\ell$ from the data, as in Newey and West (1994) or Hobijn, Franses and Ooms (2004). Most software uses such a rule by default.
- **Other kernels.** The quadratic spectral kernel or a prewhitened Bartlett kernel estimates the long-run variance with less bias.
- **Tests with breaks.** Allow a known or estimated shift in level or slope, so that a single break is not read as a unit root.
- **Panel versions.** Average the statistic over many series, as in the Hadri test.
- **A CUSUM view.** The same partial sums $S_t$ are the basis of the [CUSUM](/cusum/) test for a change in mean. KPSS uses their sum of squares; CUSUM-type tests use their maximum.

## When to use it

Use the KPSS test together with the ADF test or DF-GLS, before choosing between a model in levels and a model in differences. Use case "ct" when the series has a visible trend. It is also a natural test for the residuals of a cointegrating regression, where the null of interest is that the residuals are stationary. Report the bandwidth with the result.

## Pitfalls

- **Small bandwidth with strong autocorrelation.** A stationary AR(1) with root 0.9 is rejected half the time at $n = 200$ with $\ell_4$. Caner and Kilian (2001) show the same distortion for persistent stationary series. A larger $\ell$ helps the size, at the cost of power.
- **Large bandwidth.** With $\ell$ close to $n$, $\hat\sigma^2(\ell)$ is inflated under the alternative, and the test loses its power.
- **Missing the trend.** A trend-stationary series tested in case "c" is rejected almost always, because the partial sums of a line are a parabola.
- **Level shifts.** One break in the mean makes the partial sums drift, so the test rejects stationarity. Check for breaks with [change-point detection](/change-point-detection/).
- **Reading the table p-value as exact.** Interpolation in a four-row table gives only rough p-values, and values outside 0.01 to 0.10 are clipped.
- **Treating both tests as independent.** The ADF and KPSS tests use the same data. Combining their decisions does not have a simple overall size.

## Implementations

## History

Nyblom and Makelainen (1983) derived the locally best invariant test for a random walk component in a regression with iid errors, and Nabeya and Tanaka (1988) studied its distribution. Kwiatkowski, Phillips, Schmidt and Shin published the version with a nonparametric long-run variance in the Journal of Econometrics in 1992, in response to the many studies that could not reject a unit root in macroeconomic series with the Dickey-Fuller test. Their aim was a test in which stationarity is the null, so that the two tests could be run side by side. The limit in case "c" was already known in goodness-of-fit testing, where Anderson and Darling (1952) had computed its distribution.

## References
