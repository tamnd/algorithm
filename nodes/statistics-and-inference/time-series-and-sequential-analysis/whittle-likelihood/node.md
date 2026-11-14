---
tag: F9TJBR
kind: technique
slug: whittle-likelihood
name: Whittle likelihood
aliases:
- Whittle approximation
- Whittle estimator
area: statistics-and-inference/time-series-and-sequential-analysis
level: advanced
summary: Approximates the Gaussian likelihood of a stationary series by a sum over Fourier frequencies of log f plus the periodogram over f, with f the spectral density.
prereqs: [stationary-process, arma-model, periodogram, fast-fourier-transform, maximum-likelihood-estimation]
see_also: [innovations-algorithm, yule-walker-equations, spectral-estimation, power-spectral-density, prediction-error-method, asymptotic-normality-of-mle, toeplitz-system-solving, gaussian-process]
sources:
  - paper: doi:10.1007/BF02590998
    title: Peter Whittle, Estimation and information in stationary time series, Arkiv för Matematik 2(5), 1953
    locator: pp. 423 to 434 (the frequency-domain approximation of the Gaussian likelihood and the asymptotic information)
  - book: isbn:9780387974293
    title: "Peter J. Brockwell and Richard A. Davis, Time Series: Theory and Methods, second edition, Springer, 1991"
    locator: Section 10.3 (asymptotic properties of the periodogram, p. 342), Section 10.7 (the fast Fourier transform, p. 373) and Section 10.8 (asymptotic behaviour of the maximum likelihood and Whittle estimators of ARMA coefficients, p. 375)
  - book: isbn:9783319298528
    title: Peter J. Brockwell and Richard A. Davis, Introduction to Time Series and Forecasting, third edition, Springer, 2016
    locator: Section 4.2 (the periodogram, p. 106)
  - paper: doi:10.1093/biomet/asy071
    title: Adam M. Sykulski, Sofia C. Olhede, Arthur P. Guillaumin, Jonathan M. Lilly and Jeffrey J. Early, The debiased Whittle likelihood, Biometrika 106(2), 2019
    locator: the expected periodogram in place of the spectral density, its O(n log n) computation, and the reduction of the small-sample bias
---

The Whittle likelihood replaces the Gaussian likelihood of a stationary series by a sum over the Fourier frequencies $\omega_j = 2\pi j/n$:

$$-2\log L_W(\theta) = N\log(2\pi) + \sum_{j \in J}\Big[\log\big(2\pi f_\theta(\omega_j)\big) + \frac{I(\omega_j)}{f_\theta(\omega_j)}\Big],$$

where $f_\theta$ is the model [spectral density](/power-spectral-density/), $I(\omega_j) = \lvert\sum_{t=1}^n X_t e^{-it\omega_j}\rvert^2/(2\pi n)$ is the [periodogram](/periodogram/), and $J$ is a set of $N$ frequencies. Whittle (1953) derived it by noting that the discrete Fourier transform nearly diagonalizes the covariance matrix of a stationary series. It is the exact likelihood of a circular version of the process, it costs $O(n \log n)$ with the [fast Fourier transform](/fast-fourier-transform/), and for short-memory models its minimizer has the same asymptotic law as the Gaussian maximum likelihood estimate. For short series and peaked spectra it is biased, and tapering or the debiased Whittle likelihood reduce the bias.

## In plain words

A stationary series can be split into waves of different frequencies. The model says how much power each frequency should carry. The data say how much power each frequency actually carries, as measured by the periodogram. For a long series, the measured power at different frequencies is almost independent, and at each frequency it is about the model power times a random factor with mean 1. So you can score a model by comparing the two at every frequency and adding up, as if each frequency were its own small, independent experiment. This is much faster than working with the full matrix of covariances between all pairs of time points, and for long series it gives almost the same answer.

## When it applies

- The series is weakly [stationary](/stationary-process/) with a known mean, or with the mean removed. The model gives the spectral density $f_\theta$ in closed form, for example the [ARMA](/arma-model/) density $f(\lambda) = \frac{\sigma^2}{2\pi}\lvert\theta(e^{-i\lambda})\rvert^2/\lvert\phi(e^{-i\lambda})\rvert^2$.
- The data are equally spaced with no gaps. Missing values break the Fourier transform.
- The asymptotic theory needs short memory: $f_\theta$ continuous and bounded away from 0, as for a causal invertible ARMA model. Long-memory models need separate theory (see the classic examples).
- $n$ is large enough for $O(1)$ errors to be small next to $n$. The method is most useful when the exact likelihood is expensive: long series, long-memory models, spatial grids and multivariate series.

## The template

The data are $x_1, \ldots, x_n$. The holes are the spectral family $f_\theta$ for $\theta \in \Theta$, the frequency set $J$, and the minimizer `MINIMIZE`.

```pseudo id=main
WHITTLE(x[1..n], f_θ, Θ, J, MINIMIZE)          ▷ returns θ̂ and -2 log L_W(θ̂)
L1  I[j] ← |Σ_{t=1}^{n} x[t] e^{-itω_j}|² / (2πn) for j = 0, ..., n - 1    ▷ one FFT, ω_j = 2πj/n
L2  ℓ(θ): for each j ∈ J do f_j ← f_θ(ω_j)
L3            term_j ← log(2π f_j) + I[j] / f_j
L4        ℓ(θ) ← |J| log(2π) + Σ_{j ∈ J} term_j
L5  return θ̂ ← MINIMIZE(ℓ, Θ), with ℓ(θ̂)
```

Common choices for $J$:

- *Known mean 0:* all $j = 0, \ldots, n - 1$. Then $N = n$ and the scale matches the exact $-2\log L$.
- *Mean removed:* subtract $\bar x$ and use $j = 1, \ldots, n - 1$, because $I(0) = 0$ after centering. The code does this.
- *Half the frequencies:* $I$ and $f$ are symmetric, $I(\omega_{n-j}) = I(\omega_j)$, so many texts sum over $0 < \omega_j < \pi$ only. This halves the objective and does not change the minimizer.
- *A band:* only the lowest $m$ frequencies, for the local Whittle estimator.

**Profiling the scale.** Write $f_\theta = \frac{\sigma^2}{2\pi} g_\beta$, where $g_\beta$ does not depend on $\sigma^2$. Minimizing over $\sigma^2$ gives $\hat\sigma^2(\beta) = \frac{2\pi}{N}\sum_{j \in J} I(\omega_j)/g_\beta(\omega_j)$, and the profiled objective $N\log(2\pi) + N\log\hat\sigma^2(\beta) + \sum_{j \in J}\log g_\beta(\omega_j) + N$. The code minimizes this over $\beta$. For a causal invertible ARMA model, $\frac1n\sum_{j=0}^{n-1}\log g_\beta(\omega_j)$ is within $O(\rho^n)$ of 0 for some $\rho < 1$, by Kolmogorov's formula on the grid (the tests check $\lvert\cdot\rvert < 10^{-12}$ for $n = 512$). So the minimizer is close to the minimizer of $\sum_j I(\omega_j)/g_\beta(\omega_j)$, a weighted least squares fit of the periodogram.

**Why it works: the circulant approximation.** Let $\Gamma_n = [\gamma(s - t)]$ be the covariance matrix and let $C_n$ be the circulant matrix with first row $\tilde\gamma(h) = \sum_{k \in \mathbb{Z}}\gamma(h + kn)$. Every circulant is diagonalized by the Fourier vectors, and the eigenvalue of $C_n$ at $\omega_j$ is $\sum_{h=0}^{n-1}\tilde\gamma(h)e^{-ih\omega_j} = \sum_{h \in \mathbb{Z}}\gamma(h)e^{-ih\omega_j} = 2\pi f(\omega_j)$. With $d_j = \sum_t x_t e^{-it\omega_j}$, this gives $x^\top C_n^{-1}x = \frac1n\sum_j \lvert d_j\rvert^2/(2\pi f(\omega_j)) = \sum_j I(\omega_j)/f(\omega_j)$ and $\log\det C_n = \sum_j\log(2\pi f(\omega_j))$. So with $J$ all $n$ frequencies, $-2\log L_W$ is exactly the Gaussian $-2\log L$ of a series with covariance $C_n$, a process that wraps around the circle. For short memory, $\Gamma_n$ and $C_n$ differ mainly in the corners, and the two log likelihoods differ by $O_p(1)$ while each grows like $n$ (Brockwell and Davis 1991, Section 10.8). For white noise $C_n = \Gamma_n = \sigma^2 I$, and the Whittle likelihood is exact (this is Parseval's identity, checked in the tests).

**What is proved and what is measured.** For a causal invertible ARMA model with IID noise of finite variance, the Whittle estimator is consistent and $\sqrt{n}(\hat\beta - \beta)$ has the same normal limit as the Gaussian maximum likelihood estimator (Brockwell and Davis 1991, Section 10.8, cited, not proved here). Normal noise is not needed. The values below were measured with the code. At the true parameters of an AR(1) model with $\phi = 0.6$ and $\sigma^2 = 1$ (seed 3), the exact $-2\log L$ was 180.574 and the Whittle value 180.065 for $n = 64$, and 680.140 and 681.014 for $n = 256$. The gap stays of order 1 while the values grow like $n$.

**Cost.** Line L1 is one FFT, $O(n\log n)$ when $n$ is a power of 2. The code uses its own radix-2 FFT, which falls back to the direct sum on an odd factor, and the tests check it against the direct transform. Each evaluation of $\ell$ then costs $O(N(p + q))$ for an ARMA($p$, $q$) model. The exact likelihood costs $O(n\max(p, q)^2)$ per evaluation with the [innovations algorithm](/innovations-algorithm/) or a Kalman filter, $O(n^2)$ for a general stationary model by Durbin-Levinson, and $O(n^3)$ for a general covariance matrix by Cholesky. The gain is small for a low-order ARMA model and large for long-memory models, spatial grids and long multivariate series.

## Classic examples

- **AR(1) has a closed form.** With known mean 0 and all $n$ frequencies, $g(\omega) = \lvert 1 - \phi e^{-i\omega}\rvert^{-2}$ and $\sum_j I(\omega_j)/g(\omega_j) = \frac{1}{2\pi}\big[(1 + \phi^2)\tilde c_0 - 2\phi\tilde c_1\big]$, with $\tilde c_0 = \sum_t x_t^2$ and the circular sum $\tilde c_1 = \sum_{t=1}^{n} x_t x_{t+1}$ (indices mod $n$). The log term is $\sum_j\log g(\omega_j) = -2\log\lvert 1 - \phi^n\rvert$, which is exponentially small. Without it, the profiled objective is minimized at the circular lag-1 autocorrelation $\hat\phi_W = \tilde c_1/\tilde c_0$, which is at most 1 in absolute value. A numerical check on a series of length 200 (seed 9) gave $\tilde c_1/\tilde c_0 = 0.53556015$ and the minimizer of the full Whittle objective $0.53556016$. Compare the [Yule-Walker](/yule-walker-equations/) estimate, which uses the ordinary lag-1 autocorrelation.
- **ARMA fitting.** The code fits a causal invertible ARMA($p$, $q$) model by Nelder-Mead over unconstrained parameters $u$, mapped to $\phi$ and $\theta$ through partial autocorrelations $\tanh(u_k)$ and the Durbin-Levinson step-up recursion, so every candidate is causal and invertible. For AR(1), 100 series per row (seed 21), comparing the Whittle estimate (W), the exact Gaussian maximum likelihood estimate (MLE) and the Yule-Walker estimate (YW):

  | $\phi$ | $n$ | mean W | mean MLE | mean YW | RMSE W | RMSE MLE | RMSE YW | mean $\lvert$W - MLE$\rvert$ |
  |---|---|---|---|---|---|---|---|---|
  | 0.6 | 128 | 0.5920 | 0.5834 | 0.5791 | 0.0756 | 0.0756 | 0.0761 | 0.0120 |
  | 0.6 | 512 | 0.5981 | 0.5962 | 0.5951 | 0.0365 | 0.0368 | 0.0371 | 0.0031 |
  | 0.9 | 128 | 0.8779 | 0.8687 | 0.8594 | 0.0577 | 0.0581 | 0.0651 | 0.0156 |
  | 0.9 | 512 | 0.8961 | 0.8949 | 0.8927 | 0.0203 | 0.0185 | 0.0205 | 0.0045 |

  The three estimators have nearly the same error. The difference between the Whittle and exact estimates falls by about 4 when $n$ grows by 4, faster than the error itself, as the $O_p(1/n)$ gap between them predicts. An ARMA(1,1) fit with $\phi = 0.5$, $\theta = 0.4$ and $n = 1024$ (seed 7) is also in the tests.
- **Long memory.** For a fractionally integrated ARMA model, $f(\lambda) = \frac{\sigma^2}{2\pi}\lvert 1 - e^{-i\lambda}\rvert^{-2d}\lvert\theta(e^{-i\lambda})\rvert^2/\lvert\phi(e^{-i\lambda})\rvert^2$ with $0 < d < 1/2$. The process has no finite state space form, so the exact likelihood costs $O(n^2)$ per evaluation by Durbin-Levinson. The Whittle estimator costs $O(n\log n)$ once and $O(n)$ per evaluation. Fox and Taqqu (1986) proved that it stays consistent and asymptotically normal for Gaussian long-memory processes.
- **Spatial data on a grid.** For a stationary random field on an $n_1 \times n_2$ grid, the exact likelihood needs a factorization of an $N \times N$ matrix with $N = n_1 n_2$, which is $O(N^3)$. The Whittle likelihood uses a two-dimensional FFT, $O(N\log N)$. Here the edge effects are larger: on a $d$-dimensional grid with side $n$, the bias is of order $1/n$ while the standard error is of order $n^{-d/2}$. For $d = 2$ they are of the same order, and for $d \ge 3$ the bias dominates, so tapering or a debiased form is needed for valid $\sqrt{N}$ inference (Guyon 1982; Dahlhaus and Künsch 1987).

## Variations

- **Tapered Whittle.** Multiply the data by a taper $h_t$ that goes smoothly to 0 at both ends before line L1. This reduces the leakage of power from strong frequencies into weak ones, at the cost of some variance (Dahlhaus 1988 for time series; Dahlhaus and Künsch 1987 for random fields).
- **Debiased Whittle.** Sykulski et al. (2019) replace $f_\theta(\omega_j)$ by the expected periodogram $\bar f_\theta(\omega_j) = \mathbb{E}_\theta[I(\omega_j)]$, which is $f_\theta$ smoothed by the Fejér kernel. It can be computed from the autocovariance in $O(n\log n)$. This removes the main bias term and keeps the cost.
- **Local Whittle.** Use only the lowest $m$ frequencies and the model $f(\lambda) \approx G\lambda^{-2d}$ near 0, to estimate the memory parameter $d$ without modelling the short-range part (Künsch 1987; Robinson 1995).
- **Multivariate Whittle.** For a $k$-dimensional series, use $\sum_j[\log\det(2\pi F_\theta(\omega_j)) + \operatorname{tr}(F_\theta(\omega_j)^{-1}\mathcal{I}(\omega_j))]$ with the spectral density matrix $F_\theta$ and the periodogram matrix $\mathcal{I}$.
- **Frequency-domain least squares.** Minimizing $\sum_j I(\omega_j)/g_\beta(\omega_j)$ alone, without the log term, gives the same first-order asymptotics for ARMA models, because the log term averages to about 0.

## Pitfalls

- **The mean.** The periodogram at $\omega_0 = 0$ is $n\bar x^2/(2\pi)$. If the mean is not 0, remove it and drop $j = 0$. Otherwise the fit tries to explain the mean by power at frequency 0.
- **Small samples and peaked spectra.** $\mathbb{E}[I(\omega_j)]$ differs from $f(\omega_j)$ by leakage from nearby frequencies. When the spectrum has a sharp peak or a large dynamic range, the bias can be much larger than the standard error. Use a taper or the debiased form.
- **Nonstationary data.** A trend or a unit root puts huge power at the lowest frequencies, and the fit becomes meaningless. Difference or detrend first, as in the [ARIMA](/arima-model/) approach.
- **Identifiability.** The spectral density does not change when a root of $\theta(z)$ or $\phi(z)$ is replaced by its reciprocal (with a change of $\sigma^2$). Restrict the search to causal and invertible parameters, as the code does with its partial autocorrelation map.
- **The value is not the exact likelihood.** The Whittle value differs from the exact $-2\log L$ by $O_p(1)$. Do not mix Whittle and exact values in one likelihood ratio or information criterion. Within the Whittle family, likelihood ratio tests and AIC work to first order.
- **Sampled continuous-time processes.** For data sampled every $\Delta$ time units, the model spectrum must be the aliased density $\sum_k f_c(\lambda + 2\pi k/\Delta)$, not $f_c$ itself.

## Exercises

1. Show that for white noise, $f \equiv \sigma^2/(2\pi)$, the Whittle value with all $n$ frequencies equals the exact Gaussian $-2\log L$. *Hint:* Parseval's identity gives $\sum_j I(\omega_j) = \frac{1}{2\pi}\sum_t x_t^2$.
2. Derive the profiled scale $\hat\sigma^2(\beta) = \frac{2\pi}{N}\sum_{j \in J} I(\omega_j)/g_\beta(\omega_j)$ and the profiled objective.
3. Show that $\sum_{j=0}^{n-1}\log\lvert 1 - a e^{-i\omega_j}\rvert^2 = 2\log\lvert 1 - a^n\rvert$ for $\lvert a\rvert < 1$. *Hint:* $\prod_j(z - e^{-i\omega_j}) = z^n - 1$.
4. Prove that the AR(1) Whittle estimate with known mean, without the term $-2\log\lvert 1 - \phi^n\rvert$, is $\tilde c_1/\tilde c_0$, and that $\lvert\tilde c_1/\tilde c_0\rvert \le 1$.
5. Show that the circulant $C_n$ with first row $\tilde\gamma(h) = \sum_k\gamma(h + kn)$ has eigenvalues $2\pi f(\omega_j)$.

## References
