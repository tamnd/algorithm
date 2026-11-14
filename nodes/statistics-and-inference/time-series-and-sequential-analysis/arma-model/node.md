---
tag: 6K4KHK
kind: model
slug: arma-model
name: ARMA model
aliases:
- "autoregressive moving-average model"
- "ARMA(p, q) process"
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: A stationary model with an autoregressive part of order p and a moving-average part of order q, a parsimonious form for many autocorrelation patterns.
history:
  year: 1951
  people: [Peter Whittle, George E. P. Box, Gwilym M. Jenkins]
  note: Whittle studied the mixed autoregressive moving-average model in his 1951 thesis, and Box and Jenkins made it the standard model for forecasting in their 1970 book.
prereqs: [autoregressive-model, moving-average-model]
see_also: [arima-model, whittle-likelihood, innovations-algorithm, box-jenkins-method, armax-model, state-space-model, kalman-filter, wold-decomposition-theorem]
sources:
  - book: isbn:9780387974293
    title: "Peter J. Brockwell and Richard A. Davis, Time Series: Theory and Methods, second edition, Springer, 1991"
    locator: Section 3.1 (causality and invertibility, pp. 77 to 88), Section 3.3 (computing the autocovariance, p. 91), Section 4.4 (rational spectral densities, p. 122), Section 5.3 (recursive prediction of an ARMA process, p. 175), Section 8.7 (maximum likelihood and least squares, p. 256) and Section 8.8 (asymptotic properties, p. 258)
  - book: isbn:9783319298528
    title: Peter J. Brockwell and Richard A. Davis, Introduction to Time Series and Forecasting, third edition, Springer, 2016
    locator: Section 3.1 (ARMA(p, q) processes, p. 73), Section 3.2 (ACF and PACF, p. 77), Section 3.3 (forecasting, p. 87), Section 5.2 (maximum likelihood, p. 139) and Section 5.5 (order selection, p. 149)
  - book: isbn:9781118675021
    title: "George E. P. Box, Gwilym M. Jenkins, Gregory C. Reinsel and Greta M. Ljung, Time Series Analysis: Forecasting and Control, fifth edition, Wiley, 2015"
    locator: Part I (stochastic models and their forecasting) and Part II (model identification, estimation and diagnostic checking)
  - book: isbn:9780691042893
    title: James D. Hamilton, Time Series Analysis, Princeton University Press, 1994
    locator: Chapter 3 (stationary ARMA processes, pp. 43 to 71), Chapter 4 (forecasting, pp. 72 to 116) and Chapter 5 (maximum likelihood estimation, pp. 117 to 151)
---

An ARMA($p$, $q$) model combines an [autoregression](/autoregressive-model/) of order $p$ with a [moving average](/moving-average-model/) of order $q$: $X_t - \phi_1 X_{t-1} - \cdots - \phi_p X_{t-p} = \varepsilon_t + \theta_1 \varepsilon_{t-1} + \cdots + \theta_q \varepsilon_{t-q}$, with white noise $\varepsilon_t$. Its moving-average weights are the coefficients of the rational function $\theta(z)/\phi(z)$, so a model with few parameters can produce autocorrelations that neither a short AR nor a short MA can. An ARMA(1, 1) process is an AR($\infty$) and an MA($\infty$) process at the same time, with only three parameters. The model is the stationary core of the [Box-Jenkins method](/box-jenkins-method/) and of the [ARIMA model](/arima-model/). Its Gaussian likelihood is computed exactly by the [innovations algorithm](/innovations-algorithm/) or the [Kalman filter](/kalman-filter/), and approximately by the [Whittle likelihood](/whittle-likelihood/).

## The machine

**Notation.** $\{\varepsilon_t\} \sim \mathrm{WN}(0, \sigma^2)$, $B$ is the backshift operator, $\phi(z) = 1 - \phi_1 z - \cdots - \phi_p z^p$ and $\theta(z) = 1 + \theta_1 z + \cdots + \theta_q z^q$.

**Definition.** $\{X_t\}$ is an ARMA($p$, $q$) process with mean $\mu$ if it is stationary and

$$\phi(B)(X_t - \mu) = \theta(B)\varepsilon_t,$$

where $\phi_p \ne 0$, $\theta_q \ne 0$, and $\phi(z)$ and $\theta(z)$ have no common roots.

**Parameter space.** $\beta = (\phi_1, \ldots, \phi_p, \theta_1, \ldots, \theta_q)$, $\sigma^2 > 0$ and $\mu$. The standard parameter space is the open set of $\beta$ for which $\phi$ and $\theta$ have all roots outside the unit circle and no common roots.

**Existence, causality and invertibility** (Brockwell and Davis 1991, Section 3.1). With no common roots:

- a stationary solution exists, and is unique, if and only if $\phi(z) \ne 0$ on $|z| = 1$;
- the solution is causal, $X_t - \mu = \sum_{j \ge 0} \psi_j \varepsilon_{t-j}$, if and only if all roots of $\phi$ satisfy $|z| > 1$; then $\psi(z) = \theta(z)/\phi(z)$, which gives $\psi_0 = 1$ and $\psi_j = \theta_j + \sum_{i=1}^{\min(j, p)} \phi_i \psi_{j-i}$ with $\theta_j = 0$ for $j > q$;
- the process is invertible, $\varepsilon_t = \sum_{j \ge 0} \pi_j (X_{t-j} - \mu)$, if and only if all roots of $\theta$ satisfy $|z| > 1$; then $\pi(z) = \phi(z)/\theta(z)$.

For a causal and invertible ARMA process, $\varepsilon_t$ is the innovation of the [Wold decomposition](/wold-decomposition-theorem/), and $\sigma^2$ is the one-step prediction error from the infinite past.

**Common roots.** The condition matters. $(1 - 0.5B) X_t = (1 - 0.5B)\varepsilon_t$ has the solution $X_t = \varepsilon_t$, which is white noise. Every pair $\phi_1 = -\theta_1 = c$ gives the same process, so the parameters are not identified. Near such a cancellation, estimates of $\phi$ and $\theta$ are unstable.

**A worked case.** Take ARMA(1, 1) with $\phi = 0.5$, $\theta = 0.4$, $\sigma^2 = 1$. Then $\psi_j = (\phi + \theta)\phi^{j-1}$ for $j \ge 1$, so $\psi = 1, 0.9, 0.45, 0.225, \ldots$ From $\gamma(h) = \sigma^2 \sum_j \psi_j \psi_{j+h}$:

$$\gamma(0) = 1 + \frac{(\phi + \theta)^2}{1 - \phi^2} = 1 + \frac{0.81}{0.75} = 2.08, \qquad \gamma(1) = (\phi + \theta) + \frac{(\phi + \theta)^2 \phi}{1 - \phi^2} = 0.9 + 0.54 = 1.44,$$

and $\gamma(h) = \phi\, \gamma(h - 1)$ for $h \ge 2$. So $\rho = 1, 0.6923, 0.3462, 0.1731, \ldots$ The partial autocorrelations are $0.6923, -0.2557, 0.1010, -0.0403, \ldots$ Neither function cuts off.

## What it counts

The model has $p + q + 2$ parameters. The table lists what follows from them.

| quantity | formula | cost from the parameters |
|---|---|---|
| $\psi$ and $\pi$ weights | the recursions above | $O(p + q)$ per weight |
| autocovariance | $\gamma(k) - \sum_i \phi_i \gamma(k - i) = \sigma^2 \sum_{j=k}^{q} \theta_j \psi_{j-k}$: solve it for $0 \le k \le p$ as a linear system in $\gamma(0), \ldots, \gamma(p)$, then use it as a recursion for $k > p$ (the right side is 0 for $k > q$) | $O(p^3 + q(p + q))$, then $O(p)$ per lag |
| spectral density | $f(\lambda) = \dfrac{\sigma^2}{2\pi} \dfrac{\lvert \theta(e^{-i\lambda}) \rvert^2}{\lvert \phi(e^{-i\lambda}) \rvert^2}$ | $O(p + q)$ per frequency |
| forecasts and their errors | the innovations algorithm on $W_t = \sigma^{-1}\phi(B)X_t$ for $t > p$; error variance $\sigma^2 \sum_{j<h} \psi_j^2$ for the infinite past | $O(n \max(p, q)^2)$ for all $n$ one-step forecasts |
| exact Gaussian likelihood | from the same one-step errors and variances | $O(n \max(p, q)^2)$ |
| Whittle approximation | sum over Fourier frequencies | $O(n \log n)$ |

The autocorrelation and partial autocorrelation patterns give the classic identification table:

| model | autocorrelation | partial autocorrelation |
|---|---|---|
| AR($p$) | decays geometrically | zero after lag $p$ |
| MA($q$) | zero after lag $q$ | decays geometrically |
| ARMA($p$, $q$), $p, q \ge 1$ | decays geometrically after lag $q - p$ | decays geometrically after lag $p - q$ |

## Relation to other models

- **AR and MA.** ARMA($p$, 0) is AR($p$) and ARMA(0, $q$) is MA($q$). A causal ARMA process is MA($\infty$), and an invertible one is AR($\infty$).
- **[ARIMA model](/arima-model/).** $X$ is ARIMA($p$, $d$, $q$) when its $d$-th difference is ARMA($p$, $q$). This adds unit roots to $\phi$.
- **[State-space model](/state-space-model/).** Every ARMA process is the output of a linear Gaussian state space model with a state of dimension $r = \max(p, q + 1)$. The [Kalman filter](/kalman-filter/) then gives the exact likelihood and handles missing values.
- **Rational spectra.** ARMA processes are exactly the stationary processes with a rational spectral density. Rational functions are dense among continuous spectral densities, so any such density is approximated by ARMA spectral densities (Brockwell and Davis 1991, Section 4.4).
- **[ARMAX model](/armax-model/).** The system identification version adds a known input $u_t$ with its own polynomial. Its parameters are fitted by the [prediction error method](/prediction-error-method/), which for Gaussian noise is the exact maximum likelihood estimate.
- **[GARCH model](/garch-model/).** The squared shocks of a GARCH process with finite fourth moment follow an ARMA equation, with a white noise that is uncorrelated but not independent. The ARMA model describes the conditional mean and GARCH the conditional variance.

## Known results in the model

- **Maximum likelihood.** For a causal invertible ARMA($p$, $q$) with IID noise of finite variance, the Gaussian [maximum likelihood estimate](/maximum-likelihood-estimation/) $\hat\beta$ is consistent and $\sqrt{n}(\hat\beta - \beta) \to N(0, V(\beta))$, also when the noise is not Gaussian (Brockwell and Davis 1991, Section 8.8). Here $V(\beta) = \sigma^2 \left(\mathbb{E}[\mathbf{U}_t \mathbf{U}_t^\top]\right)^{-1}$, where $\mathbf{U}_t = (U_t, \ldots, U_{t-p+1}, V_t, \ldots, V_{t-q+1})$, $\phi(B) U_t = \varepsilon_t$ and $\theta(B) V_t = \varepsilon_t$.
- **ARMA(1, 1) variance.** From that formula, $\mathbb{E}[U_t^2] = \sigma^2/(1 - \phi^2)$, $\mathbb{E}[V_t^2] = \sigma^2/(1 - \theta^2)$ and $\mathbb{E}[U_t V_t] = \sigma^2/(1 + \phi\theta)$. Inverting the 2 by 2 matrix gives

$$V(\phi, \theta) = \frac{1 + \phi\theta}{(\phi + \theta)^2} \begin{pmatrix} (1 - \phi^2)(1 + \phi\theta) & -(1 - \phi^2)(1 - \theta^2) \\ -(1 - \phi^2)(1 - \theta^2) & (1 - \theta^2)(1 + \phi\theta) \end{pmatrix}.$$

At $\phi = 0.5$ and $\theta = 0.4$, the variances are $1.333/n$ and $1.493/n$ and the correlation is $-0.66$. As $\phi + \theta \to 0$ the variance has no bound: this is the common root problem in numbers.
- **Least squares and Whittle.** Conditional least squares, unconditional least squares and the [Whittle likelihood](/whittle-likelihood/) estimate have the same limit distribution as the maximum likelihood estimate. They differ in finite samples, most near the boundary of the parameter space.
- **Preliminary estimates.** The likelihood is not concave in $\beta$, so a start point matters. The [Yule-Walker equations](/yule-walker-equations/) give a start for the AR part, the [innovations algorithm](/innovations-algorithm/) one for the MA part (Brockwell and Davis 1991, Section 8.4 for the mixed case), and the Hannan-Rissanen method one for both by two least squares regressions.
- **Order selection.** Overfitting is not harmless: ARMA($p + 1$, $q + 1$) fitted to an ARMA($p$, $q$) process has a common root, so its parameters are not identified. Orders are chosen by the corrected [Akaike information criterion](/akaike-information-criterion/) (AICC) or the [Bayesian information criterion](/bayesian-information-criterion/), and the residuals are checked by the [Ljung-Box test](/ljung-box-test/).
- **Forecasts.** The best linear forecast of $X_{n+h}$ converges to $\mu$ geometrically as $h$ grows, and its error variance converges to $\gamma(0)$.

## References
