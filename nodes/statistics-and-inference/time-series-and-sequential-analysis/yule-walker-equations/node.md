---
tag: Y7J377
kind: algorithm
slug: yule-walker-equations
name: Yule-Walker equations
aliases:
- Yule-Walker estimation
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: Estimates an AR(p) model by solving the Toeplitz system of sample autocovariances Gamma_p phi = gamma_p, in O(p^2) by the Levinson-Durbin recursion.
model: real-ram
complexity:
  vars: {n: the length of the series, p: the autoregressive order}
  time: {worst: Θ(n p), best: Θ(n p)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1931
  people: [G. Udny Yule, Gilbert Walker, Norman Levinson, James Durbin]
  note: Yule (1927) fitted an AR(2) model to sunspot numbers and Walker (1931) gave the general equations. Levinson (1947) and Durbin (1960) gave the order-recursive solution in O(p^2) operations.
prereqs: [autoregressive-model, levinson-durbin-recursion]
see_also: [partial-autocorrelation-function, burg-method, linear-prediction, toeplitz-system-solving, method-of-moments, innovations-algorithm, whittle-likelihood, akaike-information-criterion]
sources:
  - paper: doi:10.1098/rsta.1927.0007
    title: G. Udny Yule, On a method of investigating periodicities in disturbed series, with special reference to Wolfer's sunspot numbers, Philosophical Transactions of the Royal Society A 226, 1927
    locator: pp. 267 to 298 (the AR(2) fit to the sunspot numbers)
  - paper: doi:10.1098/rspa.1931.0069
    title: Gilbert Walker, On periodicity in series of related terms, Proceedings of the Royal Society A 131, 1931
    locator: pp. 518 to 532 (the equations of general order)
  - book: isbn:9780387974293
    title: "Peter J. Brockwell and Richard A. Davis, Time Series: Theory and Methods, second edition, Springer, 1991"
    locator: Section 5.2 (the Durbin-Levinson algorithm, pp. 169 to 174), Section 8.1 (the Yule-Walker equations, p. 239), Section 8.2 (preliminary AR estimation by the Durbin-Levinson algorithm, p. 241) and Section 8.10 (asymptotic behaviour of the Yule-Walker estimates, p. 262)
  - book: isbn:9783319298528
    title: Peter J. Brockwell and Richard A. Davis, Introduction to Time Series and Forecasting, third edition, Springer, 2016
    locator: Section 2.5.3 (the Durbin-Levinson algorithm, p. 60) and Section 5.1.1 (Yule-Walker estimation, p. 123)
---

The Yule-Walker equations link the coefficients of an [autoregressive model](/autoregressive-model/) to its autocovariances: $\Gamma_p \phi = \gamma_p$, where $\Gamma_p$ is the $p \times p$ Toeplitz matrix of autocovariances $\gamma(i - j)$ and $\gamma_p = (\gamma(1), \ldots, \gamma(p))$. The Yule-Walker estimator replaces the autocovariances by their sample values, with the divisor $n$, and solves the system. It is a [method-of-moments](/method-of-moments/) estimator. The [Levinson-Durbin recursion](/levinson-durbin-recursion/) solves the system for all orders $1, \ldots, p$ in $O(p^2)$ operations and gives the sample [partial autocorrelations](/partial-autocorrelation-function/) on the way. The fitted model is always causal, and for an AR process the estimator is as efficient as maximum likelihood in large samples. It is biased toward zero in small samples, and most when a root is near the unit circle. It is the same computation as autocorrelation-method [linear prediction](/linear-prediction/) in signal processing.

## In plain words

Suppose each value of a series is a weighted sum of the last few values plus noise, and you want the weights. Multiply the model equation by an earlier value and average. You get one equation for each lag, which ties the weights to how strongly the series is correlated with itself at that lag. Estimate those correlations from the data and solve the equations. A clever recursion solves them one order at a time: it fits one lag, then two, and so on, and each step costs little. The number it adds at each step is the partial autocorrelation, which tells you whether one more lag helps.

## The problem

**Model.** $X_1, \ldots, X_n$ come from a causal AR($p$) process $\phi(B)(X_t - \mu) = \varepsilon_t$ with $\phi(z) = 1 - \phi_1 z - \cdots - \phi_p z^p$ and $\{\varepsilon_t\} \sim \mathrm{WN}(0, \sigma^2)$. The order $p$ is given.

**Population equations.** Multiply $X_t - \mu = \sum_i \phi_i (X_{t-i} - \mu) + \varepsilon_t$ by $X_{t-k} - \mu$ and take expectations. Causality makes $\varepsilon_t$ uncorrelated with the past, so

$$\gamma(k) = \sum_{i=1}^{p} \phi_i \gamma(k - i) \quad (k = 1, \ldots, p), \qquad \sigma^2 = \gamma(0) - \sum_{i=1}^{p} \phi_i \gamma(i).$$

In matrix form $\Gamma_p \phi = \gamma_p$ and $\sigma^2 = \gamma(0) - \phi^\top \gamma_p$.

**Estimator.** With $\bar x$ the sample mean and $\hat\gamma(h) = \frac1n \sum_{t=1}^{n-h} (x_{t+h} - \bar x)(x_t - \bar x)$,

$$\hat\phi = \hat\Gamma_p^{-1} \hat\gamma_p, \qquad \hat\sigma^2 = \hat\gamma(0) - \hat\phi^\top \hat\gamma_p.$$

**Output.** $\hat\phi_1, \ldots, \hat\phi_p$, $\hat\sigma^2$, and the sample partial autocorrelations $\hat\phi_{11}, \ldots, \hat\phi_{pp}$.

**Requirements.** The data are not all equal. Then $\hat\Gamma_p$ is positive definite and the solution exists and is unique.

## The algorithm

```pseudo id=main
YULE-WALKER(x[1..n], p)
L1  m ← (x[1] + ... + x[n]) / n
L2  for h ← 0 to p do γ[h] ← (1/n) Σ_{t=1}^{n-h} (x[t+h] - m)(x[t] - m)
L3  v ← γ[0]
L4  for k ← 1 to p do
L5      a ← (γ[k] - Σ_{j=1}^{k-1} φ[j] γ[k-j]) / v
L6      for j ← 1 to k-1 do φ'[j] ← φ[j] - a · φ[k-j]
L7      φ'[k] ← a;  φ ← φ';  pacf[k] ← a
L8      v ← v · (1 - a²)
L9  return (φ[1..p], v, pacf[1..k])
```

Lines L1 and L2 compute the sample autocovariances with the divisor $n$. Lines L3 to L8 are the Durbin-Levinson recursion: after step $k$, $\phi[1..k]$ solves the order-$k$ system $\hat\Gamma_k \phi = \hat\gamma_k$ and $v$ is the order-$k$ prediction error. The code works with any field arithmetic, so the tests run it on `Fraction` values and compare with Gaussian elimination. With a known mean, L1 is skipped and $m = \mu$.

## Example

Take $x = (3, 5, 6, 4, 2, 1, 3, 6, 7, 5)$, $n = 10$, $\bar x = 4.2$. The deviations are $-1.2, 0.8, 1.8, -0.2, -2.2, -3.2, -1.2, 1.8, 2.8, 0.8$, and

$$\hat\gamma(0) = 3.36 = \tfrac{84}{25}, \quad \hat\gamma(1) = 1.656 = \tfrac{207}{125}, \quad \hat\gamma(2) = -1.068 = -\tfrac{267}{250}, \quad \hat\gamma(3) = -2.092.$$

| step $k$ | $a = \hat\phi_{kk}$ | $\hat\phi$ after the step | $v$ |
|---|---|---|---|
| 0 | | | 3.36 |
| 1 | $1.656/3.36 = 0.492857$ | $(0.492857)$ | $3.36(1 - 0.492857^2) = 2.543829$ |
| 2 | $(-1.068 - 0.492857 \times 1.656)/2.543829 = -0.740683$ | $(0.857908, -0.740683)$ | 1.148254 |
| 3 | $0.050817/1.148254 = 0.044256$ | $(0.890688, -0.778651, 0.044256)$ | 1.146005 |

In exact arithmetic $\hat\phi_{11} = 69/140$, the AR(2) fit is $(25461/29678, -10991/14839)$ and $\hat\sigma^2 = 2129868/1854875$. The AR(2) polynomial $1 - 0.8579z + 0.7407z^2$ has complex roots $0.579 \pm 1.007i$ of modulus $1.162 > 1$, so the fitted model is causal, as the theory promises. The third partial autocorrelation, $0.044$, reduces $v$ by only 0.2%, which points to $p = 2$. The tests check all of these numbers.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Claim 1 derives the population equations from causality. Claim 2 proves the recursion: the order-$k$ system is persymmetric, so the order-$(k-1)$ solution read backwards solves the reversed system, and a single scalar $a$ fixes the last equation; the prediction error then falls by the factor $1 - a^2$. Claim 3 shows that the divisor-$n$ matrix $\hat\Gamma_p$ is positive definite when the data are not constant, so every $v > 0$ and every $|a| < 1$. Claim 4 proves that the fitted polynomial $\hat\phi(z)$ has all its roots outside the unit circle. The large-sample results below are cited, not proved.

## Complexity

L2 takes $(p + 1)(n - p/2)$ multiplications, which is $\Theta(np)$. The recursion L3 to L8 takes about $p^2$ multiplications. So the total is $\Theta(np + p^2) = \Theta(np)$, since $p < n$. Solving the system by Gaussian elimination instead would cost $\Theta(p^3)$, and by [Cholesky](/cholesky-decomposition/) $p^3/3$. For long series and large $p$, the autocovariances can be computed by the [fast Fourier transform](/fast-fourier-transform/) in $O(n \log n)$. The code keeps a centred copy of the data, $\Theta(n)$ extra space, and $O(p)$ for the coefficients.

## Properties

- **Asymptotically efficient for AR models (cited).** For a causal AR($p$) process with IID noise of finite variance, $\sqrt{n}(\hat\phi - \phi) \to N(0, \sigma^2 \Gamma_p^{-1})$ and $\hat\sigma^2 \to \sigma^2$ in probability (Brockwell and Davis 1991, Section 8.10). This is the same limit as for Gaussian maximum likelihood and conditional least squares. For AR(2) with $\phi = (0.5, 0.3)$, the limit gives $n\operatorname{Var}(\hat\phi_i) = 1 - \phi_2^2 = 0.91$ and $n\operatorname{Cov}(\hat\phi_1, \hat\phi_2) = -\phi_1(1 + \phi_2) = -0.65$. A simulation (seed 32, 1000 series of $n = 400$) gave $0.906$, $0.970$ and $-0.656$ (measured).
- **Bias in small samples (measured).** AR(1) with mean estimated, Gaussian noise, 2000 series per row, seed 31. YW is the Yule-Walker estimate and LS the conditional least squares estimate; "limit sd" is $\sqrt{(1 - \phi^2)/n}$.

  | $\phi$ | $n$ | mean YW | mean LS | sd YW | sd LS | limit sd |
  |---|---|---|---|---|---|---|
  | 0.5 | 50 | 0.4406 | 0.4501 | 0.1279 | 0.1303 | 0.1225 |
  | 0.5 | 200 | 0.4855 | 0.4879 | 0.0599 | 0.0602 | 0.0612 |
  | 0.9 | 50 | 0.7932 | 0.8157 | 0.0925 | 0.0937 | 0.0616 |
  | 0.9 | 200 | 0.8759 | 0.8805 | 0.0351 | 0.0348 | 0.0308 |
  | 0.99 | 50 | 0.8553 | 0.8873 | 0.0793 | 0.0837 | 0.0199 |
  | 0.99 | 200 | 0.9573 | 0.9656 | 0.0229 | 0.0231 | 0.0100 |

  Both estimates are biased toward 0, and Yule-Walker more so, because the divisor $n$ shrinks $\hat\gamma(h)$ by the factor $(n - h)/n$. Near the unit root the bias is several standard deviations and the limit standard deviation is far too small. The [Whittle likelihood](/whittle-likelihood/) page has a table that also compares the exact maximum likelihood estimate.
- **Always causal (proved).** The fitted model has all roots of $\hat\phi(z)$ outside the unit circle. The [Burg method](/burg-method/) also gives a causal fit, but conditional least squares can give a noncausal one.
- **Not efficient for MA or ARMA models.** Moment equations for MA parameters are nonlinear and inefficient; see the [moving-average model](/moving-average-model/) page, where the moment estimator of an MA(1) at $\theta = 0.5$ has 3.6 times the variance of maximum likelihood.
- **Order recursive.** One run to order $p$ gives the fits of all orders $1, \ldots, p$ and their error variances $v_k$, which is what order selection by the PACF or the [Akaike information criterion](/akaike-information-criterion/) needs.

## Variants and improvements

- **Burg's method.** Estimates each $\hat\phi_{kk}$ from forward and backward prediction errors of the data, not from $\hat\gamma$. It has less bias for short series and peaked spectra, and is still causal. See the [Burg method](/burg-method/).
- **Tapered Yule-Walker.** Multiply the data by a taper before computing $\hat\gamma$. This reduces the bias from the edges.
- **Least squares (covariance method).** Regress $x_t$ on $x_{t-1}, \ldots, x_{t-p}$ for $t = p + 1, \ldots, n$. This uses no divisor-$n$ shrinkage and has less bias, but the system is not Toeplitz and the fit may be noncausal.
- **Exact maximum likelihood.** For Gaussian data, maximize the exact likelihood, computed by the [innovations algorithm](/innovations-algorithm/) or by the closed form of the AR density, starting from the Yule-Walker fit.
- **Multivariate.** For a [vector autoregression](/vector-autoregression/) the same equations hold with matrix autocovariances, and Whittle's multivariate recursion solves them.

## When to use it

Use it as a fast and safe first fit of an AR model: as the start of a maximum likelihood search, for order selection with the sample PACF, for AR spectral estimation, or inside other methods that need a causal fit. For final estimates on short series, or when a root may be near the unit circle, prefer the exact maximum likelihood, least squares or Burg estimates. For data with an MA part, use the [innovations algorithm](/innovations-algorithm/) or the [Whittle likelihood](/whittle-likelihood/) instead.

## Pitfalls

- **The divisor $n - h$.** Using $\hat\gamma(h)$ with the divisor $n - h$ can make $\hat\Gamma_p$ indefinite. Then $v$ can become negative, $|\hat\phi_{kk}|$ can exceed 1, and the fit can be noncausal. The [stationary process](/stationary-process/) page gives a five-point example with a negative determinant.
- **A trend or a unit root.** The equations assume stationarity. On a trending or integrated series, $\hat\phi$ estimates nothing useful and is strongly biased. Difference the series first, as in the [ARIMA model](/arima-model/).
- **Forgetting the mean.** The sample mean must be subtracted. If the mean is known to be 0, skip L1; if it is not, subtracting it costs a little bias in small samples.
- **Sign conventions.** Signal processing writes the prediction error filter as $1 + a_1 z^{-1} + \cdots$, so $a_j = -\phi_j$, and the reflection coefficients have the opposite sign to $\hat\phi_{kk}$.
- **Reading the PACF bounds too strictly.** The bounds $\pm 1.96/\sqrt{n}$ hold at each lag for a true AR($p$) process. Over 20 lags, one value outside them is expected by chance.

## Implementations

## History

George Udny Yule (1927) fitted an AR(2) model to Wolfer's sunspot numbers to show that a disturbed oscillation, not a hidden periodicity, explains them. Gilbert Walker (1931) wrote the general equations between the coefficients and the autocorrelations and used them for air pressure at Darwin, a study connected with his work on the Southern Oscillation. Norman Levinson (1947) gave a recursion for Toeplitz systems in Wiener's filtering problem, and James Durbin (1960) gave the version for AR fitting that also returns the partial autocorrelations. John Parker Burg (1967) replaced the autocovariance estimate by a direct estimate of the reflection coefficients.

## References
