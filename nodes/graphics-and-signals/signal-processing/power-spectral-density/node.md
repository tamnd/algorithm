---
tag: C2MZMQ
kind: definition
slug: power-spectral-density
name: Power spectral density
aliases:
- PSD
- power spectrum
area: graphics-and-signals/signal-processing
level: core
summary: "The function S(ω) that tells how the power of a stationary signal is spread over frequency: the Fourier transform of its autocorrelation, with (1/2π) times its integral equal to the power."
prereqs: [autocorrelation, discrete-time-fourier-transform]
see_also: [wiener-khinchin-theorem, spectral-estimation, periodogram, welch-method, burg-method, frequency-response, cross-correlation, parsevals-theorem]
sources:
  - book: isbn:9780131139565
    title: Petre Stoica and Randolph L. Moses, Spectral Analysis of Signals, Pearson Prentice Hall, 2005
    locator: Section 1.3 (the two definitions of the power spectral density) and Section 1.4 (its properties, among them nonnegativity and the effect of a linear filter)
  - book: isbn:9780471594314
    title: Monson H. Hayes, Statistical Digital Signal Processing and Modeling, Wiley, 1996
    locator: Chapter 3, Discrete-Time Random Processes (the power spectrum, its properties and the power spectrum of a filtered process)
  - paper: doi:10.1109/PROC.1981.12184
    title: Steven M. Kay and Stanley L. Marple, Spectrum analysis, a modern perspective, Proceedings of the IEEE 69(11), 1981
    locator: pp. 1380 to 1419 (the definition of the power spectral density and a survey of the classical and model-based estimators)
---

The power spectral density (PSD) of a stationary random signal is a function $S(\omega)$ of the frequency that tells how the average power of the signal is spread over frequency. A narrow peak means a strong tone, a flat $S$ means white noise, and the area under $S$, times $1/(2\pi)$, is the total power. For a process whose [autocorrelation](/autocorrelation/) $r[k]$ decays fast enough, $S$ is the Fourier transform of $r$, and it is also the limit of the expected [periodogram](/periodogram/); the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/) proves that the two definitions agree. Estimating $S$ from one finite record is the problem of [spectral estimation](/spectral-estimation/).

## Definition

**Notation.** $x[n]$ is a complex zero-mean wide-sense stationary process, sampled at the rate $f_s$ in Hz, with autocorrelation $r[k] = \mathbb{E}\,x[n+k]\overline{x[n]}$. The frequency $\omega$ is in radians per sample, and $\omega \in [-\pi, \pi]$ covers all of it, because every function below is $2\pi$ periodic.

**Definition 1 (transform of the autocorrelation).** If $\sum_k |r[k]| < \infty$, the PSD is

$$S(\omega) = \sum_{k=-\infty}^{\infty} r[k]\, e^{-i\omega k}, \qquad r[k] = \frac{1}{2\pi}\int_{-\pi}^{\pi} S(\omega)\, e^{i\omega k}\, d\omega.$$

**Definition 2 (limit of the expected periodogram).**

$$S(\omega) = \lim_{N \to \infty} \mathbb{E}\left[\frac{1}{N}\left|\sum_{n=0}^{N-1} x[n]\, e^{-i\omega n}\right|^2\right].$$

Under the summability condition the two limits exist and are equal for every $\omega$; this is the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/). Definition 2 explains the name: $\frac{1}{N}|X_N(\omega)|^2$ is the power of the record near $\omega$, and $S$ is its average.

**The general case.** Every WSS process has a *spectral distribution*: a bounded nondecreasing function $F$ on $[-\pi, \pi]$ with $r[k] = \frac{1}{2\pi}\int e^{i\omega k}\, dF(\omega)$ (Herglotz). When $F$ has a density, that density is the PSD. A sinusoid gives a jump in $F$, a *spectral line*, which no density can describe; a signal can have both a continuous part and lines, such as a tone in noise.

**Properties.** For a PSD $S$ given by Definition 1:

1. *Real and nonnegative.* $S(\omega) \ge 0$ for every $\omega$. Real because $r[-k] = \overline{r[k]}$; nonnegative because it is a limit of expected squares.
2. *Total power.* $\frac{1}{2\pi}\int_{-\pi}^{\pi} S(\omega)\, d\omega = r[0] = \mathbb{E}\,|x[n]|^2$.
3. *Symmetry.* If $x$ is real, $r$ is even, so $S(-\omega) = S(\omega)$ and the half $[0, \pi]$ holds all of the information.
4. *Filtering.* If $y = h * x$ for a stable filter with [frequency response](/frequency-response/) $H(e^{i\omega})$, then $S_y(\omega) = |H(e^{i\omega})|^2\, S_x(\omega)$. The phase of the filter does not appear.

**Units.** In terms of the frequency $f = \omega f_s/(2\pi)$ in Hz, the density per hertz is $S_{\mathrm{Hz}}(f) = S(2\pi f / f_s)/f_s$, so that $\int_{-f_s/2}^{f_s/2} S_{\mathrm{Hz}}(f)\, df = r[0]$. If $x$ is in volts, $S_{\mathrm{Hz}}$ is in volts squared per hertz. For a real signal, a *one-sided* PSD $2 S_{\mathrm{Hz}}(f)$ on $[0, f_s/2]$ has the same integral; a plotted PSD must say which form it uses. On a decibel scale the value is $10\log_{10} S$.

**The cross spectrum.** For two jointly WSS processes, $S_{xy}(\omega) = \sum_k r_{xy}[k] e^{-i\omega k}$ is the transform of the [cross-correlation](/cross-correlation/). It is complex in general, and $|S_{xy}|^2 \le S_x S_y$.

## Examples and non-examples

**White noise.** If $r[k] = \sigma^2$ for $k = 0$ and $0$ otherwise, then $S(\omega) = \sigma^2$ for every $\omega$, and the total power is $\frac{1}{2\pi}\cdot 2\pi\sigma^2 = \sigma^2$.

**A moving average.** For $x[n] = w[n] + b\,w[n-1]$ with unit white noise $w$, $r[0] = 1 + b^2$, $r[\pm 1] = b$ and $S(\omega) = 1 + b^2 + 2b\cos\omega = |1 + b\,e^{-i\omega}|^2$. With $b = 1/2$, $S$ falls from $2.25$ at $\omega = 0$ to $0.25$ at $\omega = \pi$, a lowpass shape, as property 4 predicts for the filter $1 + \frac{1}{2}z^{-1}$.

**An autoregression.** For $x[n] = a\,x[n-1] + w[n]$ with $|a| < 1$ and unit white noise, $r[k] = a^{|k|}/(1 - a^2)$ and $S(\omega) = 1/|1 - a\,e^{-i\omega}|^2$. With $a = 0.6$, $S(0) = 6.25$ and $S(\pi) = 0.390625$. Rational spectra of this kind are what the [Burg method](/burg-method/) fits.

**A tone in noise.** $x[n] = A\cos(\omega_0 n + \varphi) + w[n]$ with a random phase and white $w$ of variance $\sigma^2$ has $r[k] = \frac{A^2}{2}\cos(\omega_0 k) + \sigma^2[k = 0]$. The noise gives the density $\sigma^2$; the tone gives two lines of power $A^2/4$ each at $\pm\omega_0$, not a density. Methods for this model, such as [MUSIC](/music-algorithm/) and [ESPRIT](/esprit/), estimate the line frequencies directly.

**Non-example: one periodogram.** The periodogram of one record is a random function. It is not the PSD, even for large $N$, because its variance does not shrink; see the [periodogram](/periodogram/) page.

**Non-example: a finite-energy signal.** A pulse with $\sum |x[n]|^2 < \infty$ has zero average power, so its PSD in the sense above is $0$. The right object is the *energy spectral density* $|X(e^{i\omega})|^2$, whose integral over $[-\pi, \pi]$ divided by $2\pi$ is the energy, by [Parseval's theorem](/parsevals-theorem/).

**Non-example: a Hermitian sequence with a negative transform.** $r[0] = 1$, $r[\pm 1] = 2$ gives $1 + 4\cos\omega$, which is $-3$ at $\omega = \pi$. A PSD is never negative, so this $r$ is not an autocorrelation.

## Related definitions

- [Autocorrelation](/autocorrelation/): the lag-domain description; its transform is the PSD.
- [Wiener-Khinchin theorem](/wiener-khinchin-theorem/): the proof that the two definitions agree, and the exact finite identity for records.
- [Spectral estimation](/spectral-estimation/): the problem of estimating $S$ from one record, with the [periodogram](/periodogram/), the [Welch method](/welch-method/) and the [Burg method](/burg-method/) as solutions.
- [Frequency response](/frequency-response/): the factor $|H|^2$ that a filter applies to a PSD.
- [Discrete-time Fourier transform](/discrete-time-fourier-transform/): the transform used in Definition 1, for deterministic sequences.

## References
