---
tag: YRJ2PT
kind: definition
slug: cepstrum
name: Cepstrum
aliases:
- homomorphic deconvolution
area: graphics-and-signals/signal-processing
level: advanced
summary: "The inverse Fourier transform of the logarithm of a spectrum. It turns convolution into addition, so echoes and pitch periods show as peaks at their delay, the quefrency."
prereqs: [discrete-fourier-transform, convolution-theorem]
see_also: [pitch-detection, minimum-phase, hilbert-transform, autocorrelation, linear-predictive-coding, yin-algorithm, phase-retrieval, discrete-convolution]
sources:
  - paper: "B. P. Bogert, M. J. R. Healy and J. W. Tukey, The quefrency alanysis of time series for echoes, cepstrum, pseudo-autocovariance, cross-cepstrum and saphe cracking, in M. Rosenblatt (editor), Proceedings of the Symposium on Time Series Analysis, Wiley, New York, 1963, pages 209 to 243"
    locator: the definition of the cepstrum as the spectrum of the log spectrum, and the detection of echoes by its peaks
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 13, Cepstrum Analysis and Homomorphic Deconvolution (the real and complex cepstrum, phase unwrapping, minimum-phase sequences and homomorphic deconvolution)
  - paper: doi:10.1121/1.1910339
    title: A. Michael Noll, Cepstrum pitch determination, Journal of the Acoustical Society of America 41(2), 1967, 293 to 309
    locator: the cepstral peak at the pitch period of voiced speech (general locator)
---

The cepstrum of a signal is the inverse Fourier transform of the logarithm of its spectrum. Bogert, Healy and Tukey named it in 1963 by reversing the first syllable of "spectrum", and called its index the quefrency, which is a time in samples. The logarithm turns a product of spectra into a sum, so the cepstrum turns a [convolution](/discrete-convolution/) into an addition: a source and a filter, or a signal and its echo, add up in the cepstrum and can often be separated there. An echo with delay $d$ gives peaks at quefrencies $d, 2d, 3d, \ldots$, and a voiced sound with pitch period $P$ gives a peak at $P$.

## Definition

**Real cepstrum.** Let $x[0 \ldots N-1]$ be a signal with $N$-point [DFT](/discrete-fourier-transform/) $X[k]$, and suppose $X[k] \ne 0$ for every $k$. The real cepstrum is

$$c[n] = \frac{1}{N} \sum_{k=0}^{N-1} \log|X[k]|\; e^{2\pi i kn/N}, \qquad 0 \le n \le N - 1,$$

the inverse DFT of the log magnitude. The index $n$ is the quefrency, in samples, or $n / f_s$ seconds at a sample rate $f_s$. For a real $x$, $\log|X[k]|$ is real and even in $k$, so $c$ is real and even, $c[n] = c[N - n]$. The version for an infinite signal uses the [discrete-time Fourier transform](/discrete-time-fourier-transform/), $c[n] = \frac{1}{2\pi}\int_{-\pi}^{\pi} \log|X(e^{i\omega})|\, e^{i\omega n}\, d\omega$, and the DFT version equals it with time aliasing, $c_N[n] = \sum_r c[n + rN]$.

**Complex cepstrum.** With the complex logarithm $\log X(e^{i\omega}) = \log|X(e^{i\omega})| + i \arg X(e^{i\omega})$, where the phase $\arg X$ is unwrapped into a continuous odd function and its linear part is removed,

$$\hat{x}[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} \log X(e^{i\omega})\, e^{i\omega n}\, d\omega.$$

The real cepstrum is the even part of the complex cepstrum, $c[n] = \frac{1}{2}(\hat{x}[n] + \hat{x}[-n])$. The complex cepstrum keeps the phase, so it can be inverted: $x$ is the inverse DFT of $\exp(\mathrm{DFT}(\hat{x}))$, up to the delay that was removed with the linear phase.

**Power cepstrum.** Bogert, Healy and Tukey worked with the power spectrum of the log power spectrum, $|\mathcal{F}(\log|X|^2)|^2$. It has its peaks at the same quefrencies as $c$, and it is the form still used in some mechanical and seismic work.

**Convolution becomes addition.** If $y = s * h$, then $Y = S H$, $\log|Y| = \log|S| + \log|H|$, and by linearity of the inverse DFT

$$c_y = c_s + c_h.$$

For the DFT form this holds for the circular convolution of length $N$, by the [convolution theorem](/convolution-theorem/). A scale factor $\alpha \ne 0$ only adds $\log|\alpha|$ to $c[0]$.

**Liftering.** A filter applied to the cepstrum by multiplying it with a window in quefrency is called a lifter. A low-pass lifter keeps the smooth envelope of the log spectrum, such as the formants of speech; a high-pass lifter keeps the fine structure, such as the pitch harmonics. Removing an echo or a filter this way and transforming back is homomorphic deconvolution.

## Examples and non-examples

**An impulse.** For $x = \delta$, $X[k] = 1$ for all $k$, so $\log|X| = 0$ and $c = 0$.

**An echo.** Let $e[n] = \delta[n] + a\,\delta[n - d]$ with $|a| < 1$. Its spectrum is $1 + a e^{-i\omega d}$, and

$$\log|1 + a e^{-i\omega d}| = \operatorname{Re} \log(1 + a e^{-i\omega d}) = \sum_{k=1}^{\infty} \frac{(-1)^{k+1} a^k}{k} \cos(k\omega d).$$

So the cepstrum has the value $\frac{(-1)^{k+1} a^k}{2k}$ at the quefrencies $\pm kd$, the rahmonics, and zero elsewhere; on $N$ points the indices are taken modulo $N$. For $a = \frac{1}{2}$ and $d = 10$ the first values are $c[10] = \frac{1}{4}$, $c[20] = -\frac{1}{16}$ and $c[30] = \frac{1}{48}$. Any signal with this echo, $y = s * e$, has $c_y = c_s + c_e$, so the peaks at $10, 20, 30$ are added to the cepstrum of $s$. For $s[n] = 0.6^n$ on $N = 64$ points and the circular echo with $a = \frac{1}{2}$, $d = 10$, the largest value of $c_y$ for quefrencies 2 to 31 is at 10, with value 0.2503. For white Gaussian noise of length 512 with an echo at $d = 37$ and $a = \frac{1}{2}$, the largest value for quefrencies 5 to 255 was at 37 on each of five seeds.

**Pitch.** Voiced speech is roughly a pulse train with period $P$ convolved with the response of the vocal tract. The pulse train has a log spectrum with ripples every $f_s / P$ Hz, and its cepstrum has peaks at $P, 2P, \ldots$, while the vocal tract adds a smooth part near quefrency 0. The first strong peak above a few milliseconds gives the period; this is the cepstral method of [pitch detection](/pitch-detection/) (Noll 1967).

**A non-example: spectral zeros.** For $x = [1, -1]$, $X[0] = 0$ and $\log|X[0]|$ is not defined. Zeros and near zeros of the spectrum give huge negative log values that swamp the cepstrum. In practice a small floor is added, $\log(|X| + \epsilon)$, which changes the result.

**A non-example: the autocorrelation.** The inverse DFT of $|X|^2$ without the logarithm is the circular [autocorrelation](/autocorrelation/). It also has a peak at an echo delay, but convolution stays a convolution there, so a source and a filter cannot be separated by a window.

**A non-example: the complex cepstrum by a plain FFT.** Taking the angle of each FFT bin gives a phase in $(-\pi, \pi]$ with jumps of $2\pi$. The jumps make $\log X$ discontinuous and the complex cepstrum wrong. The phase must be unwrapped first, which is hard when the spectrum has zeros near the unit circle.

## Related definitions

- **Minimum phase.** A sequence is [minimum phase](/minimum-phase/) exactly when its complex cepstrum is causal, $\hat{x}[n] = 0$ for $n < 0$. Then $\hat{x}$ follows from the real cepstrum, $\hat{x}[n] = 2c[n]$ for $n > 0$, which recovers a minimum-phase signal from its magnitude alone. This is one solution of [phase retrieval](/phase-retrieval/).
- **Hilbert transform.** For a minimum-phase sequence, the phase is the [Hilbert transform](/hilbert-transform/) of the log magnitude in frequency, which is the same statement in another form.
- **Mel-frequency cepstral coefficients.** Speech recognizers use a variant: the DCT of the log energies of a mel-spaced filter bank. It is a cepstrum on a warped frequency axis.
- **LPC cepstrum.** The cepstrum of an all-pole model from [linear predictive coding](/linear-predictive-coding/) has a recursion from the predictor coefficients, without any FFT.
- **Pitch estimators.** The [YIN algorithm](/yin-algorithm/) uses a difference function in the time domain instead, and is usually more robust than the cepstral peak.

## References
