---
tag: CHSTEW
kind: definition
slug: autocorrelation
name: Autocorrelation
aliases:
- self-correlation
area: graphics-and-signals/signal-processing
level: core
summary: "The correlation of a signal with a shifted copy of itself as a function of the lag k: r[k] = E[x[n+k] conj(x[n])] for a stationary process, or a sum over the samples for a finite record."
prereqs: [cross-correlation]
see_also: [power-spectral-density, wiener-khinchin-theorem, periodogram, spectral-estimation, burg-method, levinson-durbin-recursion, linear-prediction, pitch-detection]
sources:
  - book: isbn:9780131139565
    title: Petre Stoica and Randolph L. Moses, Spectral Analysis of Signals, Pearson Prentice Hall, 2005
    locator: Section 1.3 (the covariance sequence of a stationary signal and its properties) and Section 2.2 (the biased and unbiased sample covariances, and why only the biased one gives a positive semidefinite sequence)
  - book: isbn:9780471594314
    title: Monson H. Hayes, Statistical Digital Signal Processing and Modeling, Wiley, 1996
    locator: Chapter 3, Discrete-Time Random Processes (the autocorrelation sequence, wide-sense stationarity and the autocorrelation matrix)
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 10.6.1 (estimates of the autocorrelation sequence computed with the DFT, and the zero padding they need)
---

The autocorrelation of a signal $x[n]$ measures how much the signal looks like a copy of itself shifted by $k$ samples. For a wide-sense stationary random process it is the function $r[k] = \mathbb{E}\,x[n+k]\,\overline{x[n]}$ of the lag alone; for a finite record $x[0], \dots, x[N-1]$ it is the sum $\sum_n x[n+k]\overline{x[n]}$, usually divided by $N$. It is the [cross-correlation](/cross-correlation/) of a signal with itself. Peaks at nonzero lags show periods, the decay with $|k|$ shows memory, and its Fourier transform is the [power spectral density](/power-spectral-density/), by the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/).

## Definition

**Notation.** A signal is a sequence $x[n]$ of complex numbers, sampled at the rate $f_s$ in Hz. The lag $k$ is an integer number of samples, so the lag $k$ is a delay of $k/f_s$ seconds. A bar is the complex conjugate. For a real signal every bar can be dropped.

**For a random process.** A process $x[n]$ is *wide-sense stationary* (WSS) when its mean $\mathbb{E}\,x[n] = \mu$ does not depend on $n$ and $\mathbb{E}\,x[n+k]\overline{x[n]}$ exists and depends only on $k$. Its autocorrelation is

$$r[k] = \mathbb{E}\, x[n+k]\, \overline{x[n]}, \qquad k \in \mathbb{Z}.$$

The *autocovariance* is the same expression for $x[n] - \mu$, so $c[k] = r[k] - |\mu|^2$. Many texts on spectral analysis assume $\mu = 0$, so that the two words mean the same function, and call it the covariance sequence.

**For a finite record.** Given $N$ samples $x[0], \dots, x[N-1]$, the *deterministic* autocorrelation, the *biased* estimate and the *unbiased* estimate are, for $0 \le k \le N - 1$,

$$s[k] = \sum_{n=0}^{N-1-k} x[n+k]\,\overline{x[n]}, \qquad \hat r_b[k] = \frac{1}{N}\, s[k], \qquad \hat r_u[k] = \frac{1}{N - k}\, s[k],$$

and each is extended to negative lags by $r[-k] = \overline{r[k]}$. For $|k| \ge N$ the sum is empty and the value is $0$. The sum $s[k]$ is also the energy form for a signal of finite length, with no randomness at all. If the record has a nonzero mean, subtract the sample mean first; the result is the *sample autocovariance*.

**Properties.** Each of these holds for $r$ of a WSS process and for $s$ and $\hat r_b$ of a finite record.

1. *Hermitian symmetry.* $r[-k] = \overline{r[k]}$, so $r[0]$ is real. For a real signal, $r$ is even.
2. *Peak at zero.* $r[0] \ge 0$ and $|r[k]| \le r[0]$ for every $k$. This is the Cauchy-Schwarz inequality applied to $x[n+k]$ and $x[n]$.
3. *Positive semidefinite.* For every $p$ and every vector $c \in \mathbb{C}^p$, $\sum_{i,j} \overline{c_i}\, r[i-j]\, c_j \ge 0$. So the $p \times p$ Toeplitz matrix $R_p$ with entries $R_p[i][j] = r[i-j]$ is Hermitian and positive semidefinite. For the process, the quadratic form is $\mathbb{E}\,|\sum_j c_j x[n-j]|^2$. For $\hat r_b$ it is $\frac{1}{N}\sum_t |\sum_j c_j x[t-j]|^2$, the energy of the record filtered by $c$, divided by $N$.
4. *Shift and scale.* Delaying the record does not change $s$, and $s$ of $a\,x$ is $|a|^2 s$.

The unbiased estimate keeps property 1 but can lose properties 2 and 3, because its large lags are averages of few products. That is why the matrix in the Yule-Walker equations, and the correlogram on the [periodogram](/periodogram/) page, use $\hat r_b$.

**Bias and variance.** For a zero-mean WSS process, $\mathbb{E}\,\hat r_u[k] = r[k]$ and $\mathbb{E}\,\hat r_b[k] = (1 - |k|/N)\, r[k]$. So $\hat r_b$ is biased toward $0$ by the triangular factor, and the bias vanishes for fixed $k$ as $N \to \infty$. The unbiased estimate pays for its zero bias with variance: $\hat r_u[N-1] = x[N-1]\overline{x[0]}$ is a single product.

**Computation.** The direct sums cost $N - k$ multiplies for lag $k$, so all $N$ lags cost $N(N+1)/2$ multiplies. With the [FFT](/fast-fourier-transform/), pad the record with zeros to a length $L \ge 2N - 1$, compute $X[m]$, form $|X[m]|^2$ and take the inverse DFT; its entry $k$ is $s[k]$ for $0 \le k \le N-1$. The cost is $O(L \log L)$. The padding is needed: with $L = N$ the inverse DFT gives the *cyclic* autocorrelation $s[k] + \overline{s[N-k]}$, in which lag $k$ and lag $k - N$ add up. The finite identity behind this method is proved on the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/) page.

## Examples and non-examples

**A worked record.** Let $x = (3, -1, 2, 1, -2)$, so $N = 5$. The sums are computed with exact rationals by the implementation on this page.

| lag $k$ | products $x[n+k]\,x[n]$ | $s[k]$ | $\hat r_b[k] = s[k]/5$ | $\hat r_u[k] = s[k]/(5-k)$ |
|---|---|---|---|---|
| 0 | $9 + 1 + 4 + 1 + 4$ | 19 | 19/5 | 19/5 |
| 1 | $-3 - 2 + 2 - 2$ | $-5$ | $-1$ | $-5/4$ |
| 2 | $6 - 1 - 4$ | 1 | 1/5 | 1/3 |
| 3 | $3 + 2$ | 5 | 1 | 5/2 |
| 4 | $-6$ | $-6$ | $-6/5$ | $-6$ |

Every $|\hat r_b[k]|$ is at most $\hat r_b[0] = 3.8$. The unbiased value at lag 4 is $-6$, and $|-6| > 3.8$, so $\hat r_u$ breaks property 2 on this record.

**The unbiased estimate is not positive semidefinite.** For $x = (1, 0, -1)$, $\hat r_u = (2/3, 0, -1)$. With $c = (1, 0, 1)$ the quadratic form of the $3 \times 3$ Toeplitz matrix is $2/3 + 2/3 + 2 \cdot (-1) = -2/3 < 0$. No WSS process has this autocorrelation, and an AR model fitted to it can be unstable. The biased estimate of the same record is $(2/3, 0, -1/3)$, and its form at $c$ is $2/3 + 2/3 - 2/3 = 2/3 \ge 0$, as property 3 requires.

**White noise.** If the $x[n]$ are uncorrelated with mean $0$ and variance $\sigma^2$, then $r[k] = \sigma^2$ for $k = 0$ and $r[k] = 0$ otherwise. No lag has memory.

**A first-order autoregression.** If $x[n] = a\,x[n-1] + w[n]$ with $|a| < 1$ and $w$ white with variance $\sigma^2$, then $r[k] = \sigma^2 a^{|k|} / (1 - a^2)$. The memory decays geometrically, and the sign alternates when $a < 0$.

**A sinusoid with a random phase.** If $x[n] = A\cos(\omega_0 n + \varphi)$ with $\varphi$ uniform on $[0, 2\pi)$, then $r[k] = \frac{A^2}{2}\cos(\omega_0 k)$, with $\omega_0$ in radians per sample. The autocorrelation does not decay. It is periodic with the period of the signal, which is why [pitch detection](/pitch-detection/) looks for its first large peak after lag 0. Its spectrum is not a function but two point masses at $\pm\omega_0$; see the [power spectral density](/power-spectral-density/) page.

**Non-example: a sequence with $|r[1]| > r[0]$.** The sequence $r[0] = 1$, $r[\pm 1] = 2$, zero elsewhere, is Hermitian, but it is not the autocorrelation of any signal or process, because it breaks property 2. Its Fourier transform $1 + 4\cos\omega$ is negative near $\omega = \pi$, so it is not a power spectrum either.

**Non-example: a process with a drift.** For $x[n] = n + w[n]$ the product $\mathbb{E}\,x[n+k]\,x[n]$ depends on $n$, so the process is not WSS and the autocorrelation as a function of the lag alone does not exist. The sample formula still returns numbers, but they describe the trend and not a stationary memory. Remove the trend, or use a time-varying analysis such as the [short-time Fourier transform](/short-time-fourier-transform/).

### Pitfalls

- *Forgetting the padding.* An FFT of length $N$ gives the cyclic autocorrelation. Pad to $L \ge 2N - 1$ to get the linear one.
- *Forgetting the mean.* A constant offset $\mu$ adds the term $|\mu|^2 (N-k)/N$ to $\hat r_b[k]$, plus cross terms of the offset with the fluctuations. The term is a triangle that hides the structure of the fluctuations. Subtract the sample mean when the autocovariance is wanted.
- *Mixing the conventions.* Some texts define $r[k] = \mathbb{E}\,x[n]\overline{x[n-k]}$, which is the same function, and others $\mathbb{E}\,x[n]\overline{x[n+k]}$, which is its conjugate. For real signals the three agree. For complex signals the sign of every frequency in the spectrum flips.

## Related definitions

- [Cross-correlation](/cross-correlation/): the same sum for two different signals. The autocorrelation is the cross-correlation of $x$ with $x$.
- [Power spectral density](/power-spectral-density/): the Fourier transform of $r[k]$. The [Wiener-Khinchin theorem](/wiener-khinchin-theorem/) gives the link for processes and for finite records.
- [Covariance matrix](/covariance-matrix/): the Toeplitz matrix $R_p$ is the covariance matrix of the vector $(x[n], x[n-1], \dots, x[n-p+1])$ of a zero-mean WSS process.
- [Levinson-Durbin recursion](/levinson-durbin-recursion/) and [Toeplitz system solving](/toeplitz-system-solving/): they solve the Yule-Walker equations $R_p a = -r$ in $O(p^2)$ operations, the step that turns an autocorrelation into a [linear prediction](/linear-prediction/) filter.
- [Burg method](/burg-method/): it estimates the same predictor from the data without forming $\hat r_b$ first.
- [Periodogram](/periodogram/): the DFT of $\hat r_b$, by the finite Wiener-Khinchin identity.

## References
