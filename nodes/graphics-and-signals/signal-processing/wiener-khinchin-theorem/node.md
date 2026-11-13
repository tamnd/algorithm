---
tag: QHCYJX
kind: theorem
slug: wiener-khinchin-theorem
name: Wiener-Khinchin theorem
aliases:
- Wiener-Khinchin-Einstein theorem
area: graphics-and-signals/signal-processing
level: advanced
summary: "For a stationary process with summable autocorrelation, the power spectral density is the Fourier transform of the autocorrelation and the limit of the expected periodogram."
prereqs: [autocorrelation, power-spectral-density, discrete-time-fourier-transform]
see_also: [periodogram, spectral-estimation, parsevals-theorem, convolution-theorem, welch-method, discrete-fourier-transform, cross-correlation, spectral-leakage]
sources:
  - paper: doi:10.1007/BF02546511
    title: Norbert Wiener, Generalized harmonic analysis, Acta Mathematica 55, 1930
    locator: pp. 117 to 258 (the spectrum of a single function defined through its time-average autocorrelation)
  - paper: doi:10.1007/BF01449156
    title: A. Khintchine, Korrelationstheorie der stationären stochastischen Prozesse, Mathematische Annalen 109, 1934
    locator: pp. 604 to 615 (the spectral representation of the correlation function of a stationary process)
  - book: isbn:9780131139565
    title: Petre Stoica and Randolph L. Moses, Spectral Analysis of Signals, Pearson Prentice Hall, 2005
    locator: Section 1.3 (the two definitions of the power spectral density, as the transform of the covariance sequence and as the limit of the expected periodogram, and the decay condition under which they agree) and Section 2.2 (the periodogram and the correlogram)
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 10.5 (the expected value of the periodogram as the true spectrum convolved with the transform of the window)
---

The Wiener-Khinchin theorem links the two ways of describing a stationary random signal. One description is its [autocorrelation](/autocorrelation/) $r[k]$, the average product of samples $k$ apart. The other is its [power spectral density](/power-spectral-density/) $S(\omega)$, the power per unit frequency. The theorem says that $S$ is the Fourier transform of $r$, and that $S$ is also the limit of the expected [periodogram](/periodogram/), the squared DFT of longer and longer records. For a finite record the same link holds exactly, with no expectation and no limit: the periodogram is the Fourier sum of the biased sample autocorrelation. That finite identity is what lets every [spectral estimation](/spectral-estimation/) method move between lags and frequencies.

## Statement

**Notation.** $x[n]$ is a complex zero-mean wide-sense stationary process with autocorrelation $r[k] = \mathbb{E}\,x[n+k]\overline{x[n]}$. The frequency $\omega$ is in radians per sample, $\omega \in [-\pi, \pi]$; with the sampling rate $f_s$, $\omega$ is the frequency $\omega f_s/(2\pi)$ Hz. For a record $x[0], \dots, x[N-1]$ write

$$X_N(\omega) = \sum_{n=0}^{N-1} x[n]\, e^{-i\omega n}, \qquad P_N(\omega) = \frac{1}{N}\,|X_N(\omega)|^2, \qquad \hat r[k] = \frac{1}{N}\sum_{n=0}^{N-1-k} x[n+k]\,\overline{x[n]},$$

with $\hat r[-k] = \overline{\hat r[k]}$ and $\hat r[k] = 0$ for $|k| \ge N$. $P_N$ is the periodogram and $\hat r$ the biased sample autocorrelation.

**Theorem (finite form).** For every finite sequence $x[0], \dots, x[N-1]$ of complex numbers and every real $\omega$,

$$P_N(\omega) = \sum_{k=-(N-1)}^{N-1} \hat r[k]\, e^{-i\omega k}.$$

In the DFT form: let $L \ge N$, pad $x$ with zeros to length $L$ and sample at $\omega_m = 2\pi m/L$. Then $P_N(\omega_m)$, $m = 0, \dots, L-1$, is the length-$L$ DFT of the sequence $\hat r$ folded onto $L$ slots (slot $j$ holds the sum of the $\hat r[k]$ with $k \equiv j \pmod L$). If $L \ge 2N - 1$, no two lags share a slot, so the inverse DFT of the sampled periodogram returns $\hat r[k]$ at slot $k$ and $\hat r[-k]$ at slot $L - k$.

**Theorem (Wiener-Khinchin).** Assume $\sum_k |r[k]| < \infty$. Then

1. $S(\omega) = \sum_{k=-\infty}^{\infty} r[k]\, e^{-i\omega k}$ converges absolutely and uniformly to a continuous, real and nonnegative function;
2. $r[k] = \frac{1}{2\pi}\int_{-\pi}^{\pi} S(\omega)\, e^{i\omega k}\, d\omega$ for every $k$;
3. $\mathbb{E}\,P_N(\omega) = \sum_{|k|<N} \left(1 - \frac{|k|}{N}\right) r[k]\, e^{-i\omega k}$, and this tends to $S(\omega)$ uniformly in $\omega$ as $N \to \infty$.

So the two classical definitions of the power spectral density, the transform of $r$ and $\lim_N \mathbb{E}\,P_N$, give the same function under this hypothesis.

## In plain words

Take a noisy signal. You can ask how much a sample is like the sample $k$ steps later, for every $k$. Or you can ask how much power sits at each frequency. These two lists of numbers carry the same information. The theorem says how to go from one to the other: take the Fourier transform. For a finite record it is an exact identity, and it is why the squared FFT of a record and the lag products of the same record give the same spectrum. For a random process it says that the average of the squared FFT, over longer and longer records, settles down to the true spectrum. The average settles; a single squared FFT does not.

## Proof

**Finite form.** Expand the square and group the terms by the lag $k = m - n$:

$$|X_N(\omega)|^2 = \sum_{m=0}^{N-1}\sum_{n=0}^{N-1} x[m]\,\overline{x[n]}\, e^{-i\omega(m-n)} = \sum_{k=-(N-1)}^{N-1} e^{-i\omega k} \sum_{n} x[n+k]\,\overline{x[n]} = N \sum_{k} \hat r[k]\, e^{-i\omega k}.$$

For $k < 0$ the inner sum is $\overline{N \hat r[-k]}$, which is $N\hat r[k]$ by the convention. Divide by $N$. At $\omega_m = 2\pi m / L$ the factor $e^{-i\omega_m k}$ depends only on $k \bmod L$, so collecting the lags by slot gives the DFT of the folded sequence. If $L \ge 2N - 1$, the $2N - 1$ lags $-(N-1), \dots, N-1$ fall in different slots, the folded sequence is $\hat r$ itself placed cyclically, and the inverse DFT recovers it.

**Claim 3, the expectation.** By linearity and stationarity, $\mathbb{E}\,x[m]\overline{x[n]} = r[m-n]$. There are $N - |k|$ pairs $(m, n)$ in $\{0, \dots, N-1\}^2$ with $m - n = k$. So

$$\mathbb{E}\,P_N(\omega) = \frac{1}{N}\sum_{m,n} r[m-n]\, e^{-i\omega(m-n)} = \sum_{|k|<N} \frac{N - |k|}{N}\, r[k]\, e^{-i\omega k}.$$

**Claim 1.** Each term of the series has modulus $|r[k]|$, and $\sum |r[k]| < \infty$, so the series converges absolutely and uniformly by the Weierstrass M-test, and the limit $S$ is continuous. The terms for $k$ and $-k$ are $r[k]e^{-i\omega k}$ and $\overline{r[k]e^{-i\omega k}}$, so their sum is real, and $S$ is real.

**Convergence in claim 3.** Subtract:

$$\left| S(\omega) - \mathbb{E}\,P_N(\omega) \right| = \left| \sum_{|k|<N} \frac{|k|}{N} r[k] e^{-i\omega k} + \sum_{|k| \ge N} r[k] e^{-i\omega k} \right| \le \sum_{k} \min\!\left(\frac{|k|}{N}, 1\right) |r[k]|.$$

The right side does not depend on $\omega$. Each term tends to $0$ as $N \to \infty$ and is at most $|r[k]|$, a summable sequence, so the sum tends to $0$ by dominated convergence. This is uniform convergence.

**Nonnegativity.** $P_N(\omega) \ge 0$ for every record, so $\mathbb{E}\,P_N(\omega) \ge 0$, and the limit $S(\omega)$ is $\ge 0$.

**Claim 2.** The series for $S$ converges uniformly, so it may be integrated term by term against $e^{i\omega k}$. Since $\frac{1}{2\pi}\int_{-\pi}^{\pi} e^{i\omega(k - j)} d\omega$ is $1$ for $j = k$ and $0$ otherwise, only the term $j = k$ remains, and it is $r[k]$. $\blacksquare$

**Measured check.** The implementation computes the two sides independently. The exact Laurent polynomial identity $X(z)\overline{X}(1/z)/N = \sum_k \hat r[k] z^{-k}$ held in exact rationals for 500 random records with $N \le 9$, at a random rational $z$ (seed 4301). The two sides at random real frequencies agreed to within $10^{-12}$ times the energy for 500 complex Gaussian records with $N \le 24$ (seed 4302). The DFT form against the folded $\hat r$, with a direct $O(L^2)$ DFT and $L \in \{N, 2N-1, 2N+3\}$, agreed to the same tolerance (seed 4303). For the moving average $x[n] = w[n] + \frac{1}{2}w[n-1]$ with fair $\pm 1$ coins, the average of $\hat r[k]$ over all $2^7$ outcomes with $N = 6$ was exactly $(1 - k/6)\, r[k]$, the coefficient in claim 3.

## Consequences

- **The two estimators are one.** The [periodogram](/periodogram/) and the correlogram built from $\hat r$ are the same function, so the choice between them is a choice of algorithm, not of estimate. The FFT method for the sample [autocorrelation](/autocorrelation/) (pad to $L \ge 2N - 1$, square, invert) is the DFT form read backwards.
- **The bias of the periodogram.** Claim 3 is a convolution in frequency: $\mathbb{E}\,P_N = \frac{1}{2\pi} S \circledast F_N$, where $F_N(\omega) = \frac{1}{N}\left(\frac{\sin(N\omega/2)}{\sin(\omega/2)}\right)^2$ is the Fejér kernel, the transform of the triangle $1 - |k|/N$. Its main lobe has width $4\pi/N$ and causes the smearing and [spectral leakage](/spectral-leakage/) that [window functions](/window-functions/) trade against resolution.
- **Not consistency.** The theorem is about $\mathbb{E}\,P_N$. It does not say that $P_N$ itself converges, and for Gaussian white noise it does not: at each DFT frequency $\omega_m = 2\pi m/N$ with $0 < m < N/2$, the variance of $P_N(\omega_m)$ is $S(\omega_m)^2 = \sigma^4$ for every $N$. The [Welch method](/welch-method/) averages periodograms of segments to fix this.
- **Filtering.** If $y = h * x$ for a stable filter $h$ with frequency response $H$, then $r_y = h * \tilde h * r_x$ and the theorem gives $S_y(\omega) = |H(e^{i\omega})|^2 S_x(\omega)$, the rule behind AR spectra in the [Burg method](/burg-method/).
- **The cross version.** The same proof with $\overline{y[n]}$ in place of $\overline{x[n]}$ shows that $\frac{1}{N}X_N \overline{Y_N}$ is the Fourier sum of the biased [cross-correlation](/cross-correlation/), and that the cross power spectral density is the transform of $r_{xy}$.
- **Relation to Parseval.** Claim 2 at $k = 0$ gives $r[0] = \frac{1}{2\pi}\int S$: the power is the integral of the spectrum. It is the random counterpart of [Parseval's theorem](/parsevals-theorem/); the finite form at $k = 0$ after an inverse DFT is Parseval's theorem for the DFT.

## Tightness

The hypothesis $\sum |r[k]| < \infty$ cannot be dropped from the pointwise statement. Let $x[n] = \cos(\omega_0 n + \varphi)$ with $\varphi$ uniform on $[0, 2\pi)$, so $r[k] = \frac{1}{2}\cos(\omega_0 k)$, which is not summable. Then $\sum_k r[k] e^{-i\omega k}$ diverges, and claim 3 gives $\mathbb{E}\,P_N(\omega) = \frac{1}{4}\left(F_N(\omega - \omega_0) + F_N(\omega + \omega_0)\right)$, which grows like $N/4$ at $\omega = \omega_0$ and tends to $0$ at every other frequency in $(0, \pi)$. With $\omega_0 = 1$ the implementation gives $4.0018$, $16.0047$, $64.0014$ and $256.0000$ for $N = 16, 64, 256, 1024$, and $2.0 \times 10^{-5}$ at $\omega = 2$ for $N = 1024$. The limit exists only as a measure: point masses of weight $\pi/2$ at $\pm\omega_0$, so that $\frac{1}{2\pi}$ times the total mass is $r[0] = \frac{1}{2}$. The general theorem, due to Herglotz for sequences, says that $r$ is the autocorrelation of a WSS process exactly when $r[k] = \frac{1}{2\pi}\int e^{i\omega k}\, dF(\omega)$ for a bounded nondecreasing $F$, the spectral distribution function.

The rate in claim 3 is also sharp in general. For the AR(1) process $x[n] = 0.6\,x[n-1] + w[n]$ with unit noise, $r[k] = 0.6^{|k|}/0.64$ and the error bound of the proof is $\frac{1}{N}\sum_k |k|\,|r[k]| = 11.71875/N$. The largest error of $\mathbb{E}\,P_N$ over 201 frequencies in $[0, \pi]$, computed from claim 3, was $1.440$, $0.3662$, $0.09155$ and $0.02289$ for $N = 8, 32, 128, 512$. Times $N$, these are $11.52$, $11.719$, $11.71875$ and $11.71875$, so the bound is reached at $\omega = 0$ and the bias decays exactly like $1/N$ here.

## History

Norbert Wiener built generalized harmonic analysis in 1930 for a single function: he defined its autocorrelation as a time average and its spectrum through that average, with no probability. Aleksandr Khinchin proved in 1934 that the correlation function of every stationary process (in continuous time) is the Fourier transform of a nondecreasing spectral function, using Bochner's theorem on positive definite functions. The discrete case is Herglotz's theorem of 1911 on positive definite sequences. Albert Einstein had described the same relation for a fluctuating observed quantity in a short note of 1914, which is why some texts add his name. The finite identity between the periodogram and the lag sums was used by Blackman and Tukey in the 1950s to compute spectra from autocorrelations, and the FFT reversed the direction in the 1960s.

## References
