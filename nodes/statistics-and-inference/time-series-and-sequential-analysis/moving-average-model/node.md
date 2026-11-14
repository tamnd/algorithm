---
tag: 7V2BCK
kind: model
slug: moving-average-model
name: Moving-average model
aliases:
- MA model
- MA(q) process
area: statistics-and-inference/time-series-and-sequential-analysis
level: intro
summary: A model in which each value is a linear combination of the current and previous q white noise terms. Its autocorrelation is zero beyond lag q.
history:
  year: 1927
  people: [Eugen Slutsky]
  note: Slutsky showed in 1927 (in Russian, in English in 1937) that moving sums of independent random shocks produce series with irregular cycles, like economic series.
prereqs: [stationary-process]
see_also: [autoregressive-model, arma-model, innovations-algorithm, partial-autocorrelation-function, wold-decomposition-theorem, autocorrelation, moving-average, armax-model]
sources:
  - paper: doi:10.2307/1907241
    title: Eugen Slutzky, The summation of random causes as the source of cyclic processes, Econometrica 5(2), 1937
    locator: pp. 105 to 146 (moving sums of random series and the cycles they produce)
  - book: isbn:9780387974293
    title: "Peter J. Brockwell and Richard A. Davis, Time Series: Theory and Methods, second edition, Springer, 1991"
    locator: Section 3.1 (causality and invertibility, pp. 77 to 88), Section 3.2 (MA processes and autocovariances that vanish after lag q, p. 89), Section 7.2 (Bartlett's formula, p. 220) and Section 8.3 (preliminary MA estimates by the innovations algorithm, p. 245)
  - book: isbn:9783319298528
    title: Peter J. Brockwell and Richard A. Davis, Introduction to Time Series and Forecasting, third edition, Springer, 2016
    locator: Section 2.2 (linear processes, p. 44), Section 3.1 (ARMA processes, p. 73) and Section 5.1.3 (the innovations algorithm for MA estimation, p. 132)
  - book: isbn:9780691042893
    title: James D. Hamilton, Time Series Analysis, Princeton University Press, 1994
    locator: Chapter 3 (moving average processes and invertibility, pp. 43 to 71)
---

A moving-average model of order $q$, written MA($q$), says that each value of a time series is a weighted sum of the current white noise shock and the $q$ shocks before it: $X_t = \varepsilon_t + \theta_1 \varepsilon_{t-1} + \cdots + \theta_q \varepsilon_{t-q}$. Every MA($q$) process is [stationary](/stationary-process/), whatever its coefficients, and two values more than $q$ steps apart are uncorrelated. That cutoff in the [autocorrelation](/autocorrelation/) is how the model is recognized in data. The model is invertible, so that the shocks can be recovered from the past of the series, when the roots of $\theta(z) = 1 + \theta_1 z + \cdots + \theta_q z^q$ lie outside the unit circle. The [Wold decomposition](/wold-decomposition-theorem/) shows that a regular stationary process is an MA($\infty$) process, so finite MA models are a natural first approximation. The name has nothing to do with the [moving average](/moving-average/) used to smooth data, except that both are weighted sums over a window.

## The machine

**Notation.** $\{\varepsilon_t\} \sim \mathrm{WN}(0, \sigma^2)$ is white noise, $B$ is the backshift operator, and $\theta_0 = 1$.

**Definition.** $\{X_t\}$ is an MA($q$) process with mean $\mu$ if

$$X_t = \mu + \sum_{j=0}^{q} \theta_j \varepsilon_{t-j} = \mu + \theta(B)\varepsilon_t,$$

with $\theta_q \ne 0$. The parameters are $\theta = (\theta_1, \ldots, \theta_q) \in \mathbb{R}^q$, $\sigma^2 > 0$ and $\mu$.

**Stationarity.** No condition is needed. $\mathbb{E}[X_t] = \mu$, and

$$\gamma(h) = \sigma^2 \sum_{j=0}^{q - |h|} \theta_j \theta_{j + |h|} \quad \text{for } |h| \le q, \qquad \gamma(h) = 0 \quad \text{for } |h| > q.$$

Neither depends on $t$. If the noise is IID, the process is also strictly stationary and $q$-dependent: blocks more than $q$ apart are independent.

**Invertibility.** The process is invertible, $\varepsilon_t = \sum_{j \ge 0} \pi_j (X_{t-j} - \mu)$ with $\sum_j |\pi_j| < \infty$, if and only if every root of $\theta(z)$ satisfies $|z| > 1$ (Brockwell and Davis 1991, Section 3.1). The weights solve $\pi(z) = 1/\theta(z)$. For MA(1), $\pi_j = (-\theta)^j$.

**Identifiability.** Without invertibility the parameters are not identified from the autocovariance. For MA(1), $\theta$ with noise variance $\sigma^2$ and $1/\theta$ with noise variance $\theta^2 \sigma^2$ give the same $\gamma$: with $\theta = 0.5$ and $\sigma^2 = 1$, and with $\theta = 2$ and $\sigma^2 = 0.25$, both have $\gamma(0) = 1.25$ and $\gamma(1) = 0.5$. In general, a root $z$ of $\theta$ can be replaced by $1/\bar z$ with a change of $\sigma^2$, which gives up to $2^q$ models with one autocovariance. The usual convention picks the invertible one. When $\theta$ has no roots inside the unit circle, the MA noise is the Wold innovation of $X$.

**A hand example.** Let $\theta_1 = 0.5$, $\mu = 0$ and shocks $\varepsilon_1, \ldots, \varepsilon_6 = 1, -2, 0, 3, -1, 2$. Then $X_2, \ldots, X_6 = -1.5, -1, 3, 0.5, 1.5$, for example $X_4 = 3 + 0.5 \times 0 = 3$. Here $\rho(1) = 0.5/1.25 = 0.4$ and $\rho(h) = 0$ for $h \ge 2$. For MA(2) with $\theta = (0.4, 0.2)$ and $\sigma^2 = 1$: $\gamma(0) = 1.2$, $\gamma(1) = 0.4 + 0.4 \times 0.2 = 0.48$, $\gamma(2) = 0.2$, so $\rho = 1, 0.4, 0.1667, 0, 0, \ldots$

## What it counts

| quantity | formula | cost from the parameters |
|---|---|---|
| autocovariance | the sum above; 0 after lag $q$ | $O(q)$ per lag |
| $\pi$ weights | $\pi_0 = 1$, $\pi_j = -\sum_{i=1}^{\min(j, q)} \theta_i \pi_{j-i}$ | $O(q)$ per weight |
| partial autocorrelation | does not cut off; for MA(1), $\phi_{hh} = -(-\theta)^h (1 - \theta^2)/(1 - \theta^{2(h+1)})$ | $O(h^2)$ by Durbin-Levinson |
| spectral density | $f(\lambda) = \dfrac{\sigma^2}{2\pi} \lvert \theta(e^{-i\lambda}) \rvert^2$ | $O(q)$ per frequency |
| $h$-step forecast from the infinite past | $\mu + \sum_{j=h}^{q} \theta_j \varepsilon_{n+h-j}$; equal to $\mu$ for $h > q$ | $O(q)$ |
| its error variance | $\sigma^2 \sum_{j=0}^{\min(h, q+1) - 1} \theta_j^2$; equal to $\gamma(0)$ for $h > q$ | $O(q)$ |
| exact Gaussian likelihood and finite-sample forecasts | the [innovations algorithm](/innovations-algorithm/) with the banded autocovariance | $O(n q^2)$ |

For MA(1) with $\theta = 0.5$, the partial autocorrelations are $0.4, -0.1905, 0.0941, -0.0469, \ldots$: they alternate in sign and decay like $\theta^h$. This is the mirror image of an AR(1) process, whose autocorrelation decays and whose partial autocorrelation cuts off.

## Relation to other models

- **[Autoregressive model](/autoregressive-model/).** An invertible MA($q$) is an AR($\infty$) with weights $-\pi_j$, and a causal AR($p$) is an MA($\infty$). An AR approximation of an MA process needs many lags when a root of $\theta$ is near the unit circle.
- **[ARMA model](/arma-model/).** MA($q$) is ARMA(0, $q$).
- **Linear process.** The MA($\infty$) process $X_t = \sum_j \psi_j \varepsilon_{t-j}$ with $\sum_j |\psi_j| < \infty$ is the general causal linear process. Finite MA models are its truncations, and the [Wold decomposition theorem](/wold-decomposition-theorem/) says that every regular stationary process has this form with $\sum_j \psi_j^2 < \infty$.
- **Over-differencing.** If $X_t$ is white noise, then $\nabla X_t = X_t - X_{t-1}$ is MA(1) with $\theta = -1$ and $\rho(1) = -0.5$. This MA is not invertible. A sample autocorrelation near $-0.5$ at lag 1 after differencing is a sign that the [ARIMA](/arima-model/) model differences once too often.
- **FIR filters.** In signal processing an MA filter is a finite impulse response filter applied to white noise. The [ARMAX model](/armax-model/) in system identification uses an MA part for the noise.

## Known results in the model

- **Characterization by the autocovariance.** A stationary process whose autocovariance is zero after lag $q$ is an MA($q$) process: there is a white noise $\{Z_t\}$ and coefficients with $X_t - \mu = \theta(B) Z_t$, and $\theta$ can be chosen with no roots inside the unit circle (Brockwell and Davis 1991, Section 3.2). So the autocovariance cutoff is both necessary and sufficient.
- **Bounds on the autocorrelation.** For MA(1), $\rho(1) = \theta/(1 + \theta^2)$, so $|\rho(1)| \le 1/2$, with equality only at $\theta = \pm 1$. A sample value outside $[-1/2, 1/2]$ means that MA(1) does not fit, or that the sample is small.
- **Bartlett's formula.** For IID noise and lags $h > q$, the sample autocorrelation $\hat\rho(h)$ is approximately normal with mean 0 and variance $\frac{1}{n}\left(1 + 2\sum_{k=1}^{q} \rho(k)^2\right)$ (Brockwell and Davis 1991, Section 7.2). The usual identification bounds use this variance, not $1/n$.
- **Estimation is nonlinear.** The moment equation $\hat\rho(1) = \theta/(1 + \theta^2)$ for MA(1) has an invertible solution only if $|\hat\rho(1)| \le 1/2$. By the [delta method](/delta-method/) and Bartlett's formula, this moment estimator has asymptotic variance $\frac{1 + \theta^2 + 4\theta^4 + \theta^6 + \theta^8}{n(1 - \theta^2)^2}$, against $(1 - \theta^2)/n$ for the Gaussian maximum likelihood estimator. At $\theta = 0.5$ these are $2.70/n$ and $0.75/n$, so the moment estimator needs about 3.6 times as many observations. The [innovations algorithm](/innovations-algorithm/) gives consistent preliminary estimates (Brockwell and Davis 1991, Section 8.3), and the maximum likelihood estimate refines them.
- **Exact likelihood.** The Gaussian likelihood of $X_1, \ldots, X_n$ is computed exactly by the innovations algorithm in $O(nq^2)$ operations, or by the [Kalman filter](/kalman-filter/) on a state space form with a state of dimension $q + 1$.
- **Slutsky effect.** Repeated moving sums and differences of white noise give MA processes whose spectral density has a sharp peak, so the series look as if they had a period that is not there. This was Slutsky's explanation of business cycles.

## References
