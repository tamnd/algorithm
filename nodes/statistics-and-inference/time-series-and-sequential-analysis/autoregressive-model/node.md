---
tag: 7EKFM3
kind: model
slug: autoregressive-model
name: Autoregressive model
aliases:
- AR model
- AR(p) process
area: statistics-and-inference/time-series-and-sequential-analysis
level: intro
summary: A model in which each value is a linear combination of the previous p values plus white noise. It has a causal stationary solution when the roots of phi(z) lie outside the unit circle.
history:
  year: 1927
  people: [G. Udny Yule, Gilbert Walker]
  note: Yule fitted a second-order autoregression to Wolfer's sunspot numbers in 1927, and Walker gave the general equations that link the coefficients to the autocorrelations in 1931.
prereqs: [stationary-process]
see_also: [moving-average-model, arma-model, yule-walker-equations, partial-autocorrelation-function, levinson-durbin-recursion, burg-method, arx-model, vector-autoregression]
sources:
  - paper: doi:10.1098/rsta.1927.0007
    title: G. Udny Yule, On a method of investigating periodicities in disturbed series, with special reference to Wolfer's sunspot numbers, Philosophical Transactions of the Royal Society A 226, 1927
    locator: pp. 267 to 298 (the second-order autoregression fitted to the sunspot numbers)
  - paper: doi:10.1098/rspa.1931.0069
    title: Gilbert Walker, On periodicity in series of related terms, Proceedings of the Royal Society A 131, 1931
    locator: pp. 518 to 532 (the equations between the autoregressive coefficients and the autocorrelations)
  - book: isbn:9780387974293
    title: "Peter J. Brockwell and Richard A. Davis, Time Series: Theory and Methods, second edition, Springer, 1991"
    locator: Section 3.1 (causality and invertibility, pp. 77 to 88), Section 3.3 (computing the autocovariance, p. 91), Section 3.4 (the partial autocorrelation function, pp. 98 to 102), Section 8.1 (the Yule-Walker estimates, p. 239) and Section 8.10 (their asymptotic behaviour, p. 262)
  - book: isbn:9783319298528
    title: Peter J. Brockwell and Richard A. Davis, Introduction to Time Series and Forecasting, third edition, Springer, 2016
    locator: Section 3.1 (ARMA processes, p. 73), Section 3.2 (ACF and PACF, p. 77) and Section 5.1.1 (Yule-Walker estimation, p. 123)
  - book: isbn:9780691042893
    title: James D. Hamilton, Time Series Analysis, Princeton University Press, 1994
    locator: Chapter 3 (stationary ARMA processes, pp. 43 to 71) and Chapter 5 (maximum likelihood estimation, pp. 117 to 151)
---

An autoregressive model of order $p$, written AR($p$), says that each value of a time series is a linear combination of its $p$ previous values plus a new white noise shock: $X_t = \phi_1 X_{t-1} + \cdots + \phi_p X_{t-p} + \varepsilon_t$. It is a regression of the series on its own past, which gives the name. When the roots of the polynomial $\phi(z) = 1 - \phi_1 z - \cdots - \phi_p z^p$ lie outside the unit circle, the equation has one [stationary](/stationary-process/) solution, and that solution depends only on present and past shocks. The coefficients follow from the autocovariances through the [Yule-Walker equations](/yule-walker-equations/), and the [partial autocorrelation function](/partial-autocorrelation-function/) is zero after lag $p$, which is how the order is chosen. The AR model is the simplest member of the [ARMA](/arma-model/) family and the base of [linear prediction](/linear-prediction/) in signal processing.

## The machine

**Notation.** $\{\varepsilon_t\} \sim \mathrm{WN}(0, \sigma^2)$ is white noise: mean 0, variance $\sigma^2$, uncorrelated at different times. $\mathrm{IID}(0, \sigma^2)$ means independent and identically distributed with the same moments. $B$ is the backshift operator, $B X_t = X_{t-1}$.

**Definition.** $\{X_t : t \in \mathbb{Z}\}$ is an AR($p$) process with mean $\mu$ if it is weakly stationary and

$$X_t - \mu = \sum_{i=1}^{p} \phi_i (X_{t-i} - \mu) + \varepsilon_t, \qquad \text{that is,} \qquad \phi(B)(X_t - \mu) = \varepsilon_t,$$

with $\phi_p \ne 0$. With an intercept $c$, the equation reads $X_t = c + \sum_i \phi_i X_{t-i} + \varepsilon_t$ and $\mu = c/(1 - \phi_1 - \cdots - \phi_p) = c/\phi(1)$.

**Parameter space.** $\phi = (\phi_1, \ldots, \phi_p) \in \mathbb{R}^p$, $\sigma^2 > 0$ and $\mu \in \mathbb{R}$. The model is usually restricted to the causal region below, which is open and bounded.

**Existence and causality.** The equation $\phi(B) X_t = \varepsilon_t$ has a stationary solution if and only if $\phi(z) \ne 0$ for $|z| = 1$, and then the solution is unique. The solution is **causal**, $X_t = \sum_{j \ge 0} \psi_j \varepsilon_{t-j}$ with $\sum_j |\psi_j| < \infty$, if and only if every root of $\phi(z)$ satisfies $|z| > 1$ (Brockwell and Davis 1991, Section 3.1). The weights solve $\psi(z) = 1/\phi(z)$, that is $\psi_0 = 1$ and $\psi_j = \sum_{i=1}^{\min(j, p)} \phi_i \psi_{j-i}$. Some roots inside the unit circle and none on it give a stationary but noncausal solution, which depends on future shocks. A root on the unit circle gives no stationary solution at all: the random walk $X_t = X_{t-1} + \varepsilon_t$ is the case $p = 1$, $\phi_1 = 1$.

For AR(1) the proof is short. If $|\phi| < 1$, iterate the equation $k$ times: $X_t = \sum_{j=0}^{k-1} \phi^j \varepsilon_{t-j} + \phi^k X_{t-k}$. For a stationary $X$, $\mathbb{E}[(\phi^k X_{t-k})^2] = \phi^{2k}\gamma(0) \to 0$, so $X_t = \sum_{j \ge 0} \phi^j \varepsilon_{t-j}$ in mean square, and this series is a solution. If $|\phi| > 1$, write $X_{t} = \phi^{-1} X_{t+1} - \phi^{-1}\varepsilon_{t+1}$ and iterate forward to get $X_t = -\sum_{j \ge 1} \phi^{-j} \varepsilon_{t+j}$.

**AR(2).** The causal region is the triangle $\phi_1 + \phi_2 < 1$, $\phi_2 - \phi_1 < 1$, $|\phi_2| < 1$. The roots are complex when $\phi_1^2 + 4\phi_2 < 0$, and then the autocorrelation is a damped cosine.

**Markov form.** Let $Y_t = (X_t, X_{t-1}, \ldots, X_{t-p+1})^\top$. Then $Y_t = A Y_{t-1} + (\varepsilon_t, 0, \ldots, 0)^\top$, where $A$ has first row $(\phi_1, \ldots, \phi_p)$ and ones on the subdiagonal. The eigenvalues of $A$ are the reciprocals of the roots of $\phi(z)$, so causality means that all eigenvalues lie inside the unit circle. With Gaussian IID noise, $\{Y_t\}$ is a Gaussian Markov chain and a [state-space model](/state-space-model/) with no observation noise.

**A worked case.** Take $\phi = (0.5, 0.3)$ and $\sigma^2 = 1$. The roots of $1 - 0.5z - 0.3z^2$ are $1.1736$ and $-2.8403$, both outside the unit circle, so the process is causal. The weights are $\psi = 1, 0.5, 0.55, 0.425, 0.3775, 0.3163, \ldots$. The variance is $\gamma(0) = \frac{1 - \phi_2}{(1 + \phi_2)[(1 - \phi_2)^2 - \phi_1^2]}\sigma^2 = \frac{0.7}{1.3 \times 0.24} = 2.2436$. The autocorrelations are $\rho(1) = \phi_1/(1 - \phi_2) = 0.7143$, $\rho(2) = 0.6571$, $\rho(3) = 0.5429$, each from $\rho(h) = 0.5\rho(h-1) + 0.3\rho(h-2)$.

## What it counts

The model has $p + 2$ parameters $(\phi, \sigma^2, \mu)$. Everything else is a function of them.

| quantity | formula | cost from the parameters |
|---|---|---|
| autocovariance $\gamma(0), \ldots, \gamma(p)$ | the Yule-Walker system $\gamma(k) - \sum_i \phi_i \gamma(k - i) = \sigma^2 [k = 0]$, $k = 0, \ldots, p$ | $O(p^3)$ by elimination, $O(p^2)$ by the step-down recursion |
| autocovariance at lag $h > p$ | $\gamma(h) = \sum_i \phi_i \gamma(h - i)$ | $O(p)$ per lag |
| $\psi$ weights | $\psi_j = \sum_i \phi_i \psi_{j-i}$ | $O(p)$ per weight |
| partial autocorrelation | $\phi_{hh}$; equals $\phi_p$ at $h = p$ and 0 for $h > p$ | $O(p^2)$ |
| spectral density | $f(\lambda) = \dfrac{\sigma^2}{2\pi\, \lvert \phi(e^{-i\lambda}) \rvert^2}$ | $O(p)$ per frequency |
| one-step forecast, $n \ge p$ | $\hat X_{n+1} = \mu + \sum_i \phi_i (X_{n+1-i} - \mu)$, error variance $\sigma^2$ | $O(p)$ |
| $h$-step forecast | the same recursion with forecasts in place of unknown values; error variance $\sigma^2 \sum_{j=0}^{h-1} \psi_j^2$ | $O(hp)$ |
| Gaussian likelihood | the density of $(X_1, \ldots, X_p)$ times $\prod_{t > p}$ of the one-step densities | $O(np + p^3)$ |

Three properties follow from the table. The autocorrelation decays geometrically: $|\rho(h)| \le C r^h$ for any $r$ larger than the reciprocal of the smallest root modulus. The partial autocorrelation cuts off after lag $p$. The best linear predictor of $X_{n+1}$ from all of the past uses only the last $p$ values, so the one-step prediction error of the [Wold decomposition](/wold-decomposition-theorem/) is $\sigma^2$ and the AR noise is the Wold innovation.

## Relation to other models

- **[Moving-average model](/moving-average-model/).** A causal AR($p$) is an MA($\infty$) with weights $\psi_j$, and an invertible MA($q$) is an AR($\infty$). AR and MA models are dual: the AR autocorrelation decays and the AR partial autocorrelation cuts off, and the MA has the opposite pattern.
- **[ARMA model](/arma-model/).** AR($p$) is ARMA($p$, 0). Every stationary process with a continuous spectral density is approximated by causal AR processes in the sense that the spectral densities can be made uniformly close (Brockwell and Davis 1991, Section 4.4), but an ARMA model often needs far fewer parameters.
- **[ARIMA model](/arima-model/).** An AR polynomial with a factor $(1 - z)$ is a unit root; ARIMA moves that factor into a difference.
- **[Vector autoregression](/vector-autoregression/).** The same equation with vectors $X_t$ and matrix coefficients.
- **[ARX model](/arx-model/).** The control version, with a known input $u_t$ added on the right. Least squares identification of an ARX model is the conditional least squares fit of an AR model with regressors.
- **[Linear predictive coding](/linear-predictive-coding/).** In speech processing the same model is fitted to short frames, and the coefficients are called the predictor coefficients.
- **[GARCH model](/garch-model/).** The squared residuals of a GARCH process follow an ARMA equation. The AR model describes the mean, and GARCH describes the conditional variance.

## Known results in the model

- **Yule-Walker equations.** For a causal AR($p$), $\Gamma_p \phi = \gamma_p$ and $\sigma^2 = \gamma(0) - \phi^\top \gamma_p$, where $\Gamma_p = [\gamma(i - j)]_{i,j=1}^p$ and $\gamma_p = (\gamma(1), \ldots, \gamma(p))^\top$. Multiply the equation by $X_{t-k}$ and take expectations; causality makes $\varepsilon_t$ uncorrelated with $X_{t-k}$ for $k \ge 1$. The [Yule-Walker estimator](/yule-walker-equations/) puts the sample autocovariance into this system and solves it with the [Levinson-Durbin recursion](/levinson-durbin-recursion/) in $O(p^2)$.
- **The fitted model is causal.** With the divisor-$n$ sample autocovariance, $\hat\Gamma_p$ is positive definite whenever the data are not all equal, and the Yule-Walker fit is always causal (Brockwell and Davis 1991, Section 8.1). Conditional least squares does not guarantee this, and the exact likelihood must be maximized over the causal region.
- **Asymptotic normality.** For a causal AR($p$) with IID noise of finite variance, the Yule-Walker, [Burg](/burg-method/), conditional least squares and Gaussian maximum likelihood estimators all satisfy $\sqrt{n}(\hat\phi - \phi) \to N(0, \sigma^2 \Gamma_p^{-1})$ (Brockwell and Davis 1991, Section 8.10). For AR(1) the variance is $(1 - \phi^2)/n$. For Gaussian noise this is the inverse [Fisher information](/fisher-information-matrix/), so all four are efficient. They differ in finite samples: the Yule-Walker estimator has the largest bias when a root is near the unit circle, because the divisor $n$ shrinks the sample autocovariance (see the table on the [Whittle likelihood](/whittle-likelihood/) page).
- **Order selection.** Under an AR($p$) model with IID noise, the sample partial autocorrelation at each lag $h > p$ is approximately $N(0, 1/n)$ (Quenouille 1949). So the order is the last lag outside $\pm 1.96/\sqrt{n}$, or the minimizer of the [Akaike information criterion](/akaike-information-criterion/) or the [Bayesian information criterion](/bayesian-information-criterion/).
- **A unit root changes the rate.** When $\phi = 1$ in AR(1), least squares converges at rate $n$, not $\sqrt{n}$, and the limit is not normal. Tests of $\phi = 1$ use the Dickey-Fuller distribution; see the [augmented Dickey-Fuller test](/augmented-dickey-fuller-test/).
- **Noncausal models are not identified by second moments.** If $|\phi| > 1$, the AR(1) process has the same autocovariance as the causal AR(1) with coefficient $1/\phi$ and noise variance $\sigma^2/\phi^2$. For AR($p$), reflecting a root $z$ to $1/\bar z$ keeps the autocovariance up to a scale. Gaussian methods therefore fit only the causal model.
- **Maximum entropy.** Among all stationary processes with the given $\gamma(0), \ldots, \gamma(p)$, the Gaussian AR($p$) process with those autocovariances has the largest entropy rate. This is why the [Burg method](/burg-method/) and other AR spectral estimators are called maximum entropy methods.

**A hand example.** Take $x = (3, 5, 6, 4, 2, 1, 3, 6, 7, 5)$, $n = 10$. The mean is $4.2$, and the divisor-$n$ autocovariances are $\hat\gamma(0) = 3.36$ and $\hat\gamma(1) = 1.656$. The Yule-Walker AR(1) fit is $\hat\phi = 1.656/3.36 = 69/140 = 0.4929$ and $\hat\sigma^2 = 3.36(1 - \hat\phi^2) = 2.5438$. The one-step forecast is $4.2 + 0.4929 \times (5 - 4.2) = 4.594$, with error variance $2.5438$ if the parameters were known. The [Yule-Walker equations](/yule-walker-equations/) page continues this example to $p = 2$ and $p = 3$.

## References
