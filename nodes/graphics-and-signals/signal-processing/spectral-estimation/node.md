---
tag: C1VCEP
kind: problem
slug: spectral-estimation
name: Spectral estimation
aliases:
- power spectrum estimation
area: graphics-and-signals/signal-processing
level: core
summary: "From N samples of a stationary process, estimate its power spectral density, or the frequencies and powers of the sinusoids in it, with stated resolution, bias and variance."
prereqs: [power-spectral-density, autocorrelation]
see_also: [periodogram, welch-method, burg-method, music-algorithm, esprit, prony-method, wiener-khinchin-theorem, short-time-fourier-transform]
sources:
  - book: isbn:9780131139565
    title: Petre Stoica and Randolph L. Moses, Spectral Analysis of Signals, Pearson Prentice Hall, 2005
    locator: Chapter 2 (nonparametric methods), Chapter 3 (parametric methods for rational spectra), Chapter 4 (parametric methods for line spectra, with the Cramér-Rao bound of Section 4.3) and Section 5.4 (the Capon method)
  - paper: doi:10.1109/PROC.1981.12184
    title: Steven M. Kay and Stanley L. Marple, Spectrum analysis, a modern perspective, Proceedings of the IEEE 69(11), 1981
    locator: pp. 1380 to 1419 (the classical and modern estimators compared on common test data)
  - paper: doi:10.1109/TIT.1974.1055282
    title: David C. Rife and Robert R. Boorstyn, Single tone parameter estimation from discrete-time observations, IEEE Transactions on Information Theory 20(5), 1974
    locator: pp. 591 to 598 (the Cramér-Rao bounds for the frequency, phase and amplitude of one tone and the maximum likelihood estimator)
  - paper: doi:10.1109/PROC.1982.12433
    title: David J. Thomson, Spectrum estimation and harmonic analysis, Proceedings of the IEEE 70(9), 1982
    locator: pp. 1055 to 1096 (the multitaper estimator with discrete prolate spheroidal sequences)
  - paper: doi:10.1109/PROC.1969.7278
    title: Jack Capon, High-resolution frequency-wavenumber spectrum analysis, Proceedings of the IEEE 57(8), 1969
    locator: pp. 1408 to 1418 (the minimum variance distortionless response spectrum)
---

Spectral estimation asks for the [power spectral density](/power-spectral-density/) $S(\omega)$ of a wide-sense stationary process, given only a finite record $x[0], \dots, x[N-1]$. The density says how the variance of the process is distributed over frequency $\omega$, in radians per sample. By the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/) it is the Fourier transform of the [autocorrelation](/autocorrelation/), which a finite record determines only approximately and only at lags below $N$. So every estimator makes a trade between three things: resolution (how close two features can be and still be seen as two), bias, and variance. Nonparametric methods, such as the [periodogram](/periodogram/) and the [Welch method](/welch-method/), assume nothing about the shape of $S$. Parametric methods fit a model: an autoregressive model by the [Burg method](/burg-method/), or a sum of sinusoids in noise by [MUSIC](/music-algorithm/), [ESPRIT](/esprit/) or [Prony's method](/prony-method/). A model that is right beats the Fourier limit of resolution; a model that is wrong gives confident errors.

## In plain words

A signal can be thought of as a mixture of waves of every frequency, and its spectrum says how strong each frequency is. With an infinitely long recording the spectrum would be exact. With a short one you must guess. One way is to take the Fourier transform and square it, but the result jumps around, and making it smoother blurs close peaks together. Another way is to assume a simple form, such as a few pure tones plus noise, and fit that form to the data. When the assumption is right, this sees much finer detail than the Fourier transform can. When the assumption is wrong, the answer can be badly wrong.

## Definition

**Input.** Samples $x[0], \dots, x[N-1]$, real or complex, of a zero-mean wide-sense stationary process with autocorrelation $r[k] = \mathbb{E}[x[n+k]\overline{x[n]}]$ and sampling rate $f_s$.

**Output (density form).** A function $\hat S(\omega)$ on $[-\pi, \pi)$, usually on a grid of $L$ frequencies, that estimates $S(\omega) = \sum_k r[k] e^{-i\omega k}$. It is judged by its bias $\mathbb{E}[\hat S(\omega)] - S(\omega)$, its variance, and its resolution. Physical frequency is $f = \omega f_s/(2\pi)$, and power per hertz is $\hat S/f_s$.

**Output (line form).** When $x[n] = \sum_{k=1}^{d} \alpha_k e^{i\omega_k n} + e[n]$ with white or colored noise $e$, the estimates $\hat\omega_k$ of the frequencies and, if needed, $|\hat\alpha_k|^2$ of the powers. Then $S$ has lines of height $2\pi|\alpha_k|^2$ at $\omega_k$ on top of the noise spectrum, and the error is measured directly on the frequencies.

The estimator is **consistent** if $\hat S(\omega) \to S(\omega)$ in probability as $N \to \infty$, and **asymptotically unbiased** if the bias tends to zero.

## Variants

- **Nonparametric (classical).** No model of $S$. The raw periodogram, averaged and windowed periodograms (Bartlett, Welch), lag-window or correlogram estimates (Blackman-Tukey), and multitaper estimates (Thomson).
- **Rational spectra.** $S$ is modeled as $\sigma^2|B(e^{i\omega})|^2/|A(e^{i\omega})|^2$, an autoregressive (AR), moving average or ARMA model. AR estimation is the same as [linear prediction](/linear-prediction/).
- **Line spectra.** A few sinusoids in noise. Frequencies come from subspace methods, nonlinear least squares, or the roots of a prediction polynomial.
- **Filter bank methods.** Capon's minimum variance method estimates the power at each $\omega$ with a data-adaptive filter that passes $\omega$ and suppresses everything else.
- **Spatial spectra.** With an array of sensors, the frequency becomes a direction of arrival, and the same estimators become direction finding methods; see [beamforming](/beamforming/).
- **Time-varying spectra.** For nonstationary signals, estimate on short frames, as in the [short-time Fourier transform](/short-time-fourier-transform/) and [time-frequency analysis](/time-frequency-analysis/).
- **Cross spectra.** For two processes, estimate the cross spectral density and the coherence from the [cross-correlation](/cross-correlation/).

## Examples

All the numbers below were measured with the implementations of the linked pages; the method and seed are on each page.

- **The periodogram is not consistent.** For unit white noise ($S = 1$), the variance of the periodogram at $\omega = \pi/2$ over 300 records (seeds 5000 to 5299) was $0.800$, $1.168$ and $0.933$ for $N = 64$, $256$ and $1024$. It does not fall with $N$. The Welch estimate with Hann segments of 64 samples and 50% overlap (seeds 6000 to 6199) had variance $0.115$, $0.0296$ and $0.0069$ for $N = 256$, $1024$ and $4096$, close to $1/K$ times a factor for the overlap.
- **Resolution.** For two tones at $0.5$ and $0.6$ rad/sample in complex white noise of variance $0.1$ (100 records, seeds 9000 to 9099), counting a record as resolved when both estimates are within $0.05$ of their tones:

| $N$ | separation in units of $2\pi/N$ | periodogram | MUSIC | ESPRIT |
|---|---|---|---|---|
| 32 | 0.51 | 1 | 13 | 42 |
| 64 | 1.02 | 65 | 100 | 100 |

- **An AR spectrum.** The AR(1) process $x[n] = 0.6x[n-1] + e[n]$ with unit noise has $S(\omega) = 1/|1 - 0.6e^{-i\omega}|^2$, which is $6.25$ at $\omega = 0$ and $0.390625$ at $\omega = \pi$. An AR(1) fit estimates two numbers instead of $N$ values of a spectrum.
- **The Cramér-Rao bound for one tone.** For one unit tone in complex white noise of variance $0.1$, the bound on the standard deviation of any unbiased frequency estimate is $0.0121$, $0.00151$ and $0.000274$ rad for $N = 16$, $64$ and $200$. These came from inverting the $3 \times 3$ Fisher information numerically and agree with the closed form below to 15 digits. For two tones at $0.5$ and $0.9$ with $N = 200$, MUSIC and ESPRIT with $m = 32$ reached root mean square errors of $0.00036$ and $0.00034$.

## Known algorithms

| method | type | cost | main property |
|---|---|---|---|
| [Periodogram](/periodogram/) | nonparametric | $O(L\log L)$ | resolution $\approx 2\pi/N$, variance $\approx S^2$, not consistent |
| [Welch method](/welch-method/) | nonparametric | $O(N\log M)$ | variance $\approx S^2/K$ for $K$ segments, resolution $\approx 2\pi/M$ |
| Blackman-Tukey | nonparametric | $O(N\log N)$ | windowed autocorrelation estimate, same trade as Welch |
| Multitaper (Thomson) | nonparametric | $O(KN\log N)$ | $K$ orthogonal tapers, low leakage and controlled bandwidth |
| Yule-Walker AR | rational | $O(Np + p^2)$ | stable, [Levinson-Durbin](/levinson-durbin-recursion/) solve, smears short records |
| [Burg method](/burg-method/) | rational | $O(Np)$ | stable, high resolution on short records, line splitting at high order |
| Capon (MVDR) | filter bank | $O(m^3 + Lm^2)$ | better resolution than the periodogram, no model order |
| [MUSIC](/music-algorithm/) | line spectra | $O(m^3 + Lm)$ | consistent, needs $d$, grid search |
| [ESPRIT](/esprit/) | line spectra | $O(m^3 + d^4)$ | consistent, needs $d$ and shift invariance, no search |
| [Prony's method](/prony-method/) | damped lines | $O(Np^2)$ | exact without noise, biased with noise |
| Nonlinear least squares | line spectra | iterative | maximum likelihood for Gaussian noise, reaches the bound above threshold |

Here $L$ is the number of output frequencies, $M$ the segment length, $p$ the model order, $m$ the size of the covariance matrix and $d$ the number of tones. The [window functions](/window-functions/) page covers the tapers, and [spectral leakage](/spectral-leakage/) the effect they control.

## Bounds

**Resolution of Fourier methods.** The periodogram is the true spectrum convolved with the Fejér kernel $|W(\omega)|^2/N$, whose main lobe has width $4\pi/N$ between its first zeros. Two lines closer than about $2\pi/N$ merge. Windowing widens the main lobe further, by a factor of about 1.5 to 2 for common windows. No nonparametric estimator from $N$ samples does fundamentally better, because the record determines the autocorrelation only for $|k| < N$.

**Variance against resolution.** For Bartlett's method with $K$ segments of length $M = N/K$, the variance is about $S(\omega)^2/K$ and the resolution about $2\pi/M = 2\pi K/N$. The product is about $2\pi S(\omega)^2/N$: halving the variance doubles the width of the blur. The Welch and multitaper methods improve the constant, not the trade.

**The Cramér-Rao bound for a tone.** For $x[n] = \alpha e^{i(\omega n + \phi)} + e[n]$ with complex white Gaussian noise of variance $\sigma^2$ and unknown $\omega$, $|\alpha|$ and $\phi$, every unbiased estimator satisfies

$$\operatorname{var}(\hat\omega) \ge \frac{6\sigma^2}{|\alpha|^2 N(N^2 - 1)}.$$

*Proof sketch.* The mean is $\mu[n] = |\alpha| e^{i(\omega n + \phi)}$, and for complex Gaussian noise the Fisher information is $J_{ij} = \frac{2}{\sigma^2}\operatorname{Re}\sum_n \overline{\partial_i\mu[n]}\,\partial_j\mu[n]$. With $\theta = (\omega, |\alpha|, \phi)$ the derivatives are $i n\mu[n]$, $\mu[n]/|\alpha|$ and $i\mu[n]$, so $J_{\omega\omega} = \frac{2|\alpha|^2}{\sigma^2}\sum n^2$, $J_{\omega\phi} = \frac{2|\alpha|^2}{\sigma^2}\sum n$, $J_{\phi\phi} = \frac{2|\alpha|^2}{\sigma^2}N$, and the amplitude decouples. The $(\omega, \omega)$ entry of the inverse is $\frac{\sigma^2}{2|\alpha|^2}\cdot\frac{N}{N\sum n^2 - (\sum n)^2}$, and $N\sum n^2 - (\sum n)^2 = N^2(N^2-1)/12$ for $n = 0, \dots, N-1$. This gives the bound. The variance falls as $N^{-3}$, much faster than the $N^{-1}$ of averaging, because a longer record also gives a longer lever arm for the phase. The maximum likelihood estimator, the peak of the periodogram refined to full precision, reaches the bound above a threshold signal to noise ratio. Below the threshold, outliers dominate.

**Asymptotics of parametric estimates.** For an AR($p$) model, the Yule-Walker and Burg coefficient estimates have errors of order $N^{-1/2}$, and the asymptotic covariance of the Yule-Walker estimate is $\sigma^2 R_p^{-1}/N$ with $R_p$ the $p \times p$ autocorrelation matrix. For the AR(2) model $x[n] = 0.75x[n-1] - 0.5x[n-2] + e[n]$, that is $A(z) = 1 - 0.75z^{-1} + 0.5z^{-2}$, and $N = 2000$, the measured standard deviations of the Burg estimates were $0.022$ and $0.020$ against the asymptotic $0.0194$.

## Reductions

- **To autocorrelation estimation.** By the Wiener-Khinchin theorem, any estimate $\hat r[k]$ of the autocorrelation for $|k| < N$ gives a spectrum estimate by a Fourier transform, and the biased estimate gives exactly the periodogram. Smoothing the spectrum is the same as tapering the autocorrelation.
- **AR estimation to linear prediction.** Fitting an AR($p$) model is finding the best one-step linear predictor of order $p$, and the Yule-Walker equations are a Toeplitz system solved by the Levinson-Durbin recursion. The AR spectrum is also the maximum entropy spectrum that matches $r[0], \dots, r[p]$.
- **Line spectra to sums of exponentials.** Estimating the frequencies of $d$ tones from samples is fitting $\sum_k h_k z_k^n$. Without noise this is Prony's problem, the same as finding a linear recurrence, and over a finite field it is the problem of [Berlekamp-Massey](/berlekamp-massey/).
- **Line spectra to sparse recovery.** On a grid of candidate frequencies, the record is a sparse combination of the columns of a Fourier matrix, so methods of [compressed sensing](/compressed-sensing/) apply, at the cost of the grid error.
- **Direction finding to spectral estimation.** For a uniform linear array, the signal across the sensors at one time is a sum of complex exponentials in the sensor index, with spatial frequencies $\omega = 2\pi(\Delta/\lambda)\sin\theta$. So every line spectral estimator is a direction finder.

## Applications

- **Vibration and machine monitoring.** Peaks of the spectrum show the rotation rates, gear mesh frequencies and bearing faults.
- **Speech and audio.** AR models of the vocal tract give formants and the coders of [linear predictive coding](/linear-predictive-coding/). The fundamental frequency is a [pitch detection](/pitch-detection/) problem.
- **Radar, sonar and communications.** Doppler shifts, directions of arrival, and the occupancy of radio channels.
- **Geophysics and astronomy.** Periods of variable stars, tides, seismic modes and the climate record, often from short or unevenly sampled data.
- **Biomedicine.** The bands of the electroencephalogram and the variability of the heart rate.
- **Noise characterization.** The noise spectral density of a sensor or a circuit, and the design of whitening and [Wiener filters](/wiener-filter/).

## References
