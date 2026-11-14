---
tag: TBAQY5
kind: definition
slug: stationary-process
name: Stationary process
aliases:
- weakly stationary process
- covariance stationary process
- second-order stationarity
area: statistics-and-inference/time-series-and-sequential-analysis
level: intro
summary: A process whose mean is constant and whose autocovariance depends only on the lag. Strict stationarity asks that all joint laws be shift invariant.
prereqs: [random-variable, covariance-matrix]
see_also: [autocorrelation, power-spectral-density, wold-decomposition-theorem, arma-model, gaussian-process, ergodic-theorem, augmented-dickey-fuller-test, kpss-test]
sources:
  - book: isbn:9780387974293
    title: "Peter J. Brockwell and Richard A. Davis, Time Series: Theory and Methods, second edition, Springer, 1991"
    locator: Section 1.3 (stationarity and strict stationarity, p. 11), Section 1.5 (the autocovariance function of a stationary process, p. 25), Section 4.3 (Herglotz's theorem, p. 117) and Section 7.2 (estimation of the autocovariance and autocorrelation functions, p. 220)
  - book: isbn:9783319298528
    title: Peter J. Brockwell and Richard A. Davis, Introduction to Time Series and Forecasting, third edition, Springer, 2016
    locator: Section 1.4 (stationary models and the autocorrelation function, p. 13), Section 2.1 (basic properties, p. 39) and Section 2.4 (properties of the sample mean and autocorrelation function, p. 50)
  - book: isbn:9780691042893
    title: James D. Hamilton, Time Series Analysis, Princeton University Press, 1994
    locator: Chapter 3 (stationary ARMA processes, pp. 43 to 71), the definitions of stationarity and ergodicity at the start of the chapter
---

A stationary process is a sequence of random variables $\{X_t\}$ whose statistical behaviour does not change when the time origin moves. There are two common versions. A **strictly stationary** process has the same joint distributions after any shift of time. A **weakly stationary** process, also called covariance stationary or second-order stationary, only needs a constant mean and a covariance $\operatorname{Cov}(X_{t+h}, X_t)$ that depends on the lag $h$ and not on $t$. Most of linear time series analysis ([ARMA models](/arma-model/), [Yule-Walker estimation](/yule-walker-equations/), the [Wold decomposition](/wold-decomposition-theorem/), spectral analysis) uses only the weak version, because it is a statement about the first two moments, and those are what linear prediction uses.

## Definition

**Time series.** A time series model is a family of real random variables $\{X_t : t \in \mathbb{Z}\}$ on one probability space. Data are one observed stretch $x_1, \ldots, x_n$ of one path.

**Strict stationarity.** $\{X_t\}$ is strictly stationary when, for every $k \ge 1$, all times $t_1, \ldots, t_k$ and every shift $s \in \mathbb{Z}$, the random vectors $(X_{t_1}, \ldots, X_{t_k})$ and $(X_{t_1 + s}, \ldots, X_{t_k + s})$ have the same joint distribution.

**Weak stationarity.** $\{X_t\}$ is weakly stationary when

1. $\mathbb{E}[X_t^2] < \infty$ for every $t$,
2. $\mathbb{E}[X_t] = \mu$ for every $t$, and
3. $\operatorname{Cov}(X_{t+h}, X_t)$ is the same for every $t$, for each $h \in \mathbb{Z}$.

The common value in item 3 is the **autocovariance function** $\gamma(h) = \operatorname{Cov}(X_{t+h}, X_t)$. When $\gamma(0) > 0$, the **autocorrelation function** is $\rho(h) = \gamma(h)/\gamma(0)$. The names weakly stationary, covariance stationary and second-order stationary mean the same thing. In this encyclopedia "stationary" without a qualifier means weakly stationary, as in Brockwell and Davis.

**White noise.** $\{\varepsilon_t\}$ is white noise with variance $\sigma^2$, written $\varepsilon_t \sim \mathrm{WN}(0, \sigma^2)$, when it is weakly stationary with mean 0, $\gamma(0) = \sigma^2$ and $\gamma(h) = 0$ for $h \ne 0$. The terms are uncorrelated, not necessarily independent. A sequence of independent and identically distributed variables with mean 0 and variance $\sigma^2$, written $\mathrm{IID}(0, \sigma^2)$, is white noise, but white noise need not be IID.

**Basic facts.** For a weakly stationary process:

- **(a) Symmetry and bound.** $\gamma(-h) = \gamma(h)$ and $|\gamma(h)| \le \gamma(0)$. *Proof.* $\gamma(-h) = \operatorname{Cov}(X_{t-h}, X_t) = \operatorname{Cov}(X_t, X_{t-h}) = \gamma(h)$ by item 3 at time $t - h$. The bound is the Cauchy-Schwarz inequality, $|\operatorname{Cov}(X_{t+h}, X_t)| \le \sqrt{\operatorname{Var}(X_{t+h}) \operatorname{Var}(X_t)} = \gamma(0)$. $\square$
- **(b) Nonnegative definiteness.** For all $k$, times $t_1, \ldots, t_k$ and real $a_1, \ldots, a_k$, $\sum_{i, j} a_i a_j \gamma(t_i - t_j) \ge 0$. So every matrix $\Gamma_k = [\gamma(i - j)]_{i, j = 1}^k$ is a symmetric Toeplitz matrix that is positive semidefinite. *Proof.* The sum equals $\operatorname{Var}(\sum_i a_i X_{t_i})$, which is not negative. $\square$ The converse also holds: a function $\gamma$ on $\mathbb{Z}$ is the autocovariance function of some stationary process if and only if it is even and nonnegative definite. For the converse, take the Gaussian process with mean 0 and these covariances; Kolmogorov's extension theorem says that it exists, because the finite-dimensional normal laws are consistent (Brockwell and Davis 1991, Section 1.5).
- **(c) Strict and weak.** A strictly stationary process with $\mathbb{E}[X_t^2] < \infty$ is weakly stationary, because the mean and the covariances are functions of the one- and two-dimensional laws. A weakly stationary Gaussian process is strictly stationary, because a Gaussian joint law is fixed by its mean vector and covariance matrix, and these do not change under a shift. Without the Gaussian assumption neither version implies the other (see the non-examples).
- **(d) Spectral density.** If $\sum_h |\gamma(h)| < \infty$, the function $f(\lambda) = \frac{1}{2\pi} \sum_{h \in \mathbb{Z}} \gamma(h) e^{-ih\lambda}$, $\lambda \in [-\pi, \pi]$, is the **spectral density**. It is even, nonnegative, and $\gamma(h) = \int_{-\pi}^{\pi} e^{ih\lambda} f(\lambda)\, d\lambda$. In general, Herglotz's theorem gives $\gamma(h) = \int e^{ih\lambda}\, dF(\lambda)$ for a unique bounded spectral distribution $F$ (Brockwell and Davis 1991, Section 4.3). [Power spectral density](/power-spectral-density/) and the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/) give the signal processing view. Note the $1/(2\pi)$: with it, $f$ is the density of the variance over the angular frequency $\lambda$.

**Sample versions.** From data $x_1, \ldots, x_n$ with mean $\bar x$, the **sample autocovariance** is

$$\hat\gamma(h) = \frac{1}{n} \sum_{t = 1}^{n - |h|} (x_{t + |h|} - \bar x)(x_t - \bar x), \qquad |h| < n,$$

and $\hat\rho(h) = \hat\gamma(h)/\hat\gamma(0)$. The divisor is $n$, not $n - |h|$, for a reason that is a theorem: with divisor $n$, every matrix $\hat\Gamma_k = [\hat\gamma(i - j)]_{i, j = 1}^k$ is positive semidefinite, and it is positive definite when $\hat\gamma(0) > 0$. *Proof.* Let $d = (x_1 - \bar x, \ldots, x_n - \bar x)$. Let $T$ be the $k \times (n + k - 1)$ matrix whose row $i$ is $d$ shifted right by $i - 1$ places, with zeros elsewhere. Then $(T T^\top)_{ij} = n \hat\gamma(i - j)$, so $\hat\Gamma_k = T T^\top / n$ is positive semidefinite. If $\hat\gamma(0) > 0$, then $d \ne 0$. Let $m$ be the position of the first nonzero entry of $d$. The first nonzero entry of row $i$ is at column $m + i - 1$, a different column for each row, so the rows are linearly independent and $T T^\top$ is nonsingular. $\square$

**Estimation from one path.** Stationarity alone does not make $\bar x$ a good estimate of $\mu$: the process $X_t = Z$ for all $t$, with one random $Z$, is strictly stationary, and $\bar X = Z$ for every $n$. A sufficient condition is $\gamma(h) \to 0$ as $h \to \infty$. Then $\operatorname{Var}(\bar X_n) = \frac{1}{n} \sum_{|h| < n} (1 - |h|/n) \gamma(h) \to 0$, because the Cesàro means of a sequence that tends to 0 also tend to 0. If $\sum_h |\gamma(h)| < \infty$, then $n \operatorname{Var}(\bar X_n) \to \sum_h \gamma(h) = 2\pi f(0)$, which is the variance to use in a [standard error](/standard-error/) for the mean of a correlated series. Ergodic theory ([ergodic theorem](/ergodic-theorem/)) gives the almost sure version of this law of large numbers.

## Examples and non-examples

- **IID noise and white noise.** IID$(0, \sigma^2)$ noise is strictly and weakly stationary. White noise is weakly stationary by definition.
- **A moving average (by hand).** Let $\varepsilon_t \sim \mathrm{WN}(0, 1)$ and $X_t = \varepsilon_t + 0.5\, \varepsilon_{t-1}$. Then $\mathbb{E}[X_t] = 0$, $\gamma(0) = 1 + 0.25 = 1.25$, $\gamma(\pm 1) = 0.5$ and $\gamma(h) = 0$ for $|h| \ge 2$. So $\rho(1) = 0.4$, and the autocorrelation is 0 after lag 1. This is the [MA(1) model](/moving-average-model/).
- **An autoregression.** If $|\phi| < 1$ and $\varepsilon_t \sim \mathrm{WN}(0, \sigma^2)$, then $X_t = \sum_{j \ge 0} \phi^j \varepsilon_{t-j}$ is the stationary solution of $X_t = \phi X_{t-1} + \varepsilon_t$, with $\gamma(h) = \sigma^2 \phi^{|h|}/(1 - \phi^2)$. See [autoregressive model](/autoregressive-model/).
- **A random sinusoid.** Let $A$ and $B$ be uncorrelated with mean 0 and variance $\sigma^2$, and fix $\omega \in (0, \pi)$. Then $X_t = A \cos(\omega t) + B \sin(\omega t)$ has mean 0 and $\operatorname{Cov}(X_{t+h}, X_t) = \sigma^2 [\cos(\omega(t+h))\cos(\omega t) + \sin(\omega(t+h))\sin(\omega t)] = \sigma^2 \cos(\omega h)$. It is weakly stationary, but each path is an exact sinusoid. Its future is a fixed linear function of two past values: $X_t = 2\cos(\omega) X_{t-1} - X_{t-2}$. It has no spectral density; its spectral distribution puts mass $\sigma^2/2$ at $\pm\omega$. This is the deterministic part of the [Wold decomposition](/wold-decomposition-theorem/).
- **A sample of five numbers.** For $x = (2, 4, 6, 5, 3)$, $\bar x = 4$ and the deviations are $(-2, 0, 2, 1, -1)$. Then $\hat\gamma(0) = 10/5 = 2$, $\hat\gamma(1) = (0 \cdot (-2) + 2 \cdot 0 + 1 \cdot 2 + (-1) \cdot 1)/5 = 0.2$ and $\hat\gamma(2) = (2 \cdot (-2) + 1 \cdot 0 + (-1) \cdot 2)/5 = -1.2$, so $\hat\rho(1) = 0.1$ and $\hat\rho(2) = -0.6$. The matrix $\hat\Gamma_3$ with first row $(2, 0.2, -1.2)$ has determinant $4.864 > 0$. With the divisor $n - h$ instead, the lag values are $0.25$ and $-2$, and the matrix with first row $(2, 0.25, -2)$ has determinant $-0.5$. That "estimate" is not the autocovariance function of any stationary process.
- **Non-example: a random walk.** $S_t = \varepsilon_1 + \cdots + \varepsilon_t$ with $\varepsilon_t \sim \mathrm{IID}(0, \sigma^2)$ has $\operatorname{Var}(S_t) = t\sigma^2$, which grows with $t$. Its differences $S_t - S_{t-1} = \varepsilon_t$ are stationary. This is the case $d = 1$ of the [ARIMA model](/arima-model/), and [unit root tests](/augmented-dickey-fuller-test/) try to detect it.
- **Non-example: a trend.** $X_t = a + bt + \varepsilon_t$ with $b \ne 0$ has a mean that changes with $t$. It is trend stationary: the residuals from the trend are stationary. Differencing also removes the trend, but gives $b + \varepsilon_t - \varepsilon_{t-1}$, a moving average with a unit root, which is a sign of over-differencing.
- **Non-example: a transient start.** If $X_0 = 0$ and $X_t = \phi X_{t-1} + \varepsilon_t$ for $t \ge 1$ with $|\phi| < 1$, then $\operatorname{Var}(X_t) = \sigma^2 (1 - \phi^{2t})/(1 - \phi^2)$ depends on $t$. The process is only asymptotically stationary. Simulations discard a burn-in period for this reason.
- **Strict but not weak.** IID standard Cauchy variables are strictly stationary, but they have no mean or variance, so they are not weakly stationary.
- **Weak but not strict.** Let $X_t$ be independent, with $X_t \sim N(0, 1)$ for odd $t$ and $X_t = \pm 1$ with probability $1/2$ each for even $t$. Every $X_t$ has mean 0 and variance 1, and different times are uncorrelated, so the process is white noise. But $X_1$ and $X_2$ have different distributions, so it is not strictly stationary.

## Related definitions

- **Autocovariance and autocorrelation.** The signal processing page [autocorrelation](/autocorrelation/) covers the same functions for deterministic and random signals, often without removing the mean. In statistics the autocorrelation always uses deviations from the mean.
- **Spectral density and periodogram.** The spectral density $f$ in fact (d) is the Fourier transform of $\gamma$. Its sample version is the [periodogram](/periodogram/). The [Whittle likelihood](/whittle-likelihood/) uses both.
- **Linear and causal processes.** $X_t = \mu + \sum_{j \ge 0} \psi_j \varepsilon_{t-j}$ with $\sum_j \psi_j^2 < \infty$ is stationary, with $\gamma(h) = \sigma^2 \sum_j \psi_j \psi_{j + |h|}$. The [Wold decomposition theorem](/wold-decomposition-theorem/) says that every stationary process is of this form plus a deterministic part.
- **Partial autocorrelation.** The [partial autocorrelation function](/partial-autocorrelation-function/) is the second summary of $\gamma$ used to identify a model.
- **Gaussian process.** A [Gaussian process](/gaussian-process/) indexed by time with a covariance that depends only on the lag is strictly stationary by fact (c).
- **Stationary distribution of a Markov chain.** A [Markov chain](/markov-chain/) started from its [stationary distribution](/stationary-distribution/) is a strictly stationary process. The word means the same shift invariance in both places.
- **Ergodicity.** A stationary process is ergodic when time averages along one path converge to expectations. This is what makes estimation from one series possible ([ergodic theorem](/ergodic-theorem/)).
- **Trend stationary and difference stationary.** A series is trend stationary when it is stationary after a deterministic trend is removed, and difference stationary when its differences are stationary. The [augmented Dickey-Fuller test](/augmented-dickey-fuller-test/) and the [KPSS test](/kpss-test/) test these two hypotheses from opposite sides.
- **Joint stationarity.** Two series are jointly stationary when each is stationary and $\operatorname{Cov}(X_{t+h}, Y_t)$ depends only on $h$. The [vector autoregression](/vector-autoregression/) is the standard model.

## References
