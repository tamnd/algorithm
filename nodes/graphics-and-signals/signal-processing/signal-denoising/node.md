---
tag: KXXC2V
kind: problem
slug: signal-denoising
name: Signal denoising
aliases:
- noise reduction
- signal smoothing
area: graphics-and-signals/signal-processing
level: core
summary: "Estimate a one-dimensional signal, such as a time series or an audio track, from samples that carry additive noise, with the least error that a model of the signal and the noise allows."
prereqs: [power-spectral-density]
see_also: [image-denoising, wiener-filter, spectral-subtraction, kalman-filter, median-filter, savitzky-golay-filter, discrete-wavelet-transform, moving-average]
sources:
  - paper: doi:10.1093/biomet/81.3.425
    title: "David L. Donoho and Iain M. Johnstone, Ideal spatial adaptation by wavelet shrinkage, Biometrika 81(3), 1994, pages 425 to 455"
    locator: "the universal threshold and the risk of soft thresholding compared with an oracle that knows which coefficients to keep"
  - book: isbn:9780133457117
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume I: Estimation Theory, Prentice Hall, 1993"
    locator: "Chapter 12, Linear Bayesian Estimators (the Wiener smoothing and filtering examples)"
  - book: isbn:9781466504219
    title: "Philipos C. Loizou, Speech Enhancement: Theory and Practice, second edition, CRC Press, 2013"
    locator: "Part II, Algorithms (spectral-subtractive, Wiener, statistical-model-based and subspace methods, and noise estimation)"
  - paper: doi:10.1109/TASSP.1979.1163209
    title: "Steven F. Boll, Suppression of acoustic noise in speech using spectral subtraction, IEEE Transactions on Acoustics, Speech, and Signal Processing 27(2), 1979, pages 113 to 120"
    locator: "the estimate of the noise spectrum from frames without speech, and its subtraction from each frame"
---

Signal denoising is the problem of estimating a one-dimensional signal $x[n]$ from samples $y[n] = x[n] + v[n]$ that carry additive noise $v$. The data are a time series, a sensor trace or an audio track, indexed by one time variable. Samples alone cannot separate signal from noise, so every method assumes something that makes them differ: different power spectra, smoothness, sparsity in a basis, a dynamical model or a separate noise reference. The problem for images, with two-dimensional structure such as edges and textures, is [image denoising](/image-denoising/). The one-dimensional problem adds questions that images do not have: whether the method is causal and online, what delay it adds, and how it follows noise whose statistics change with time.

## In plain words

A recording or a measurement is the true thing plus random disturbance. To clean it, you need some idea of how the true thing differs from the disturbance. Maybe the signal is slow and the noise is fast, so averaging nearby samples helps. Maybe the signal lives in a few frequency bands, so you keep those and weaken the others. Maybe the signal follows a known law of motion, so you can predict it and correct the prediction. Every method trades two errors: smoothing more removes more noise but also removes real detail. Some methods must work live, with no future samples and little delay, as in a phone call. Others can see the whole recording at once and do better.

## Definition

**Input.** Samples $y[0 \ldots N-1]$ with $y[n] = x[n] + v[n]$, or a stream $y[0], y[1], \ldots$. A model of the noise, such as zero-mean white noise of variance $\sigma^2$ or a power spectral density $S_{vv}(\omega)$, and a model or a prior class for the signal. Frequencies $\omega$ are in radians per sample, in $[-\pi, \pi]$.

**Output.** An estimate $\hat x[n]$ for each $n$.

**Criteria.** The usual measure is the mean-square error $E[(\hat x[n] - x[n])^2]$, or its sum over the record, which is the risk. Audio uses measures of perceived quality and intelligibility as well. For a linear filter the error splits into two parts: the squared bias, from the signal that the filter changes, and the variance of the noise that the filter lets through.

**Timing.** An *offline* or *smoothing* estimator uses the whole record. A *causal* estimator uses $y[0..n]$ only, and a *fixed-lag* estimator uses $y[0..n+L]$ and reports $\hat x[n]$ with delay $L$.

## Variants

- **Stationary Gaussian signal and noise.** Signal and noise are stationary with known spectra. The optimal estimator is linear, the [Wiener filter](/wiener-filter/).
- **Signal with a state model.** The signal is the output of a known linear system driven by noise. The optimal causal estimator is the [Kalman filter](/kalman-filter/), and the optimal offline one is the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/).
- **Smooth or piecewise smooth signals.** The signal is a smooth function with a few jumps. Wavelet shrinkage, local polynomial fits and total variation fit this class.
- **Speech and audio in noise.** The noise is slowly varying and its spectrum is estimated in pauses; methods work on frames of a [short-time Fourier transform](/short-time-fourier-transform/), such as [spectral subtraction](/spectral-subtraction/).
- **Impulse noise.** A few samples are replaced by outliers. Order statistics such as the [median filter](/median-filter/) are robust to them; linear filters are not.
- **Noise with a reference.** A second sensor picks up the noise but not the signal. An [adaptive filter](/adaptive-filtering/) learns the path from the reference to the noise and subtracts it.
- **Multiple sensors.** An array picks up the signal from one direction; [beamforming](/beamforming/) averages the noise down across sensors.
- **Unknown noise level.** The variance $\sigma^2$ must be estimated from the data, for example by the median absolute value of the finest wavelet coefficients divided by $0.6745$.

## Examples

**A moving average on white noise.** Let $v$ be white with variance $\sigma^2$, and take the centered average of length $L$, $\hat x[n] = \frac{1}{L} \sum_{j} y[n - j]$. The noise in the output is an average of $L$ independent values, so its variance is exactly $\sigma^2 / L$. The filter changes the signal too. Its amplitude response is

$$G(\omega) = \left| \frac{\sin(L\omega/2)}{L \sin(\omega/2)} \right|,$$

so a constant passes with gain 1, and a sinusoid of frequency $\omega$ is scaled by $G(\omega)$. For $L = 3$ and the sinusoid $x[n] = \cos(\pi n / 3)$ of power $\tfrac12$, $G(\pi/3) = 1/(3 \cdot \tfrac12) = \tfrac23$. The output has signal power $\tfrac12 \cdot \tfrac49 = \tfrac29$ and noise power $\sigma^2/3$. The signal-to-noise ratio goes from $1/(2\sigma^2)$ to $2/(3\sigma^2)$, a gain of $\tfrac43$, against a gain of $3$ for a constant signal. A filter that is good for slow signals is poor for faster ones.

**Bias on a step.** The same average on a step from $0$ to $1$ gives the ramp $\tfrac13, \tfrac23$ across the edge instead of a jump. The [median filter](/median-filter/) of length 3 keeps the step exactly. This is the reason to choose a nonlinear method for signals with jumps.

## Known algorithms

- **Local averaging.** The [moving average](/moving-average/), the [exponential moving average](/exponential-moving-average/) and other lowpass [FIR filters](/fir-filter/) and [IIR filters](/iir-filter/). Cost $O(1)$ to $O(M)$ per output sample; causal forms exist.
- **Local polynomial fits.** The [Savitzky-Golay filter](/savitzky-golay-filter/) fits a polynomial in a sliding window and keeps peaks better than a plain average. The [smoothing spline](/smoothing-spline/) is the offline, global version.
- **[Wiener filter](/wiener-filter/).** The linear MMSE filter from the signal and noise spectra, as an FIR filter, a causal IIR filter or a noncausal gain $S_{xx}/(S_{xx} + S_{vv})$ on each frequency.
- **[Kalman filter](/kalman-filter/) and [RTS smoother](/rauch-tung-striebel-smoother/).** MMSE estimates for a signal with a linear state model, causal and offline.
- **[Spectral subtraction](/spectral-subtraction/).** Subtracts an estimate of the noise power from each frame of an STFT and keeps the noisy phase. Simple and online with one frame of delay, but it leaves musical noise.
- **Wavelet shrinkage.** Take the [discrete wavelet transform](/discrete-wavelet-transform/), set small coefficients to zero (hard threshold) or shrink all of them toward zero (soft threshold), and invert. Donoho and Johnstone proposed the universal threshold $\sigma \sqrt{2 \ln N}$. Cost $O(N)$ for an orthogonal wavelet.
- **Total variation denoising.** Minimize $\tfrac12 \|\hat x - y\|^2 + \lambda \sum_n |\hat x[n+1] - \hat x[n]|$; it gives a piecewise constant answer and keeps jumps. In one dimension it has exact direct solvers. See [total variation denoising](/total-variation-denoising/).
- **[Median filter](/median-filter/).** Order statistics in a sliding window, for impulse noise.
- **Adaptive noise cancelling.** The [LMS algorithm](/lms-algorithm/) or the [RLS algorithm](/rls-algorithm/) on a reference input.
- **Learned denoisers.** Neural networks trained on pairs of clean and noisy recordings, common for speech.

## Bounds

- **No gain without a model.** With white Gaussian noise and no assumption on $x$, the estimate $\hat x = y$ is the unbiased estimate of least variance for each sample, with error $\sigma^2$. Every gain comes from an assumption about $x$.
- **The Wiener bound.** For stationary $x$ and $v$, uncorrelated, with spectra $S_{xx}$ and $S_{vv}$, no linear estimator from the whole record has a mean-square error per sample below

$$\frac{1}{2\pi} \int_{-\pi}^{\pi} \frac{S_{xx}(\omega)\, S_{vv}(\omega)}{S_{xx}(\omega) + S_{vv}(\omega)}\, d\omega,$$

the error of the noncausal [Wiener filter](/wiener-filter/). If $x$ and $v$ are jointly Gaussian, no estimator of any kind does better, because the conditional mean is then linear. A causal filter has an error at least this large.
- **The oracle bound for shrinkage.** For $N$ coefficients $\theta_i$ in an orthonormal basis with white Gaussian noise of variance $\sigma^2$, soft thresholding at $\sigma\sqrt{2 \ln N}$ has a risk at most $(2 \ln N + 1)(\sigma^2 + \sum_i \min(\theta_i^2, \sigma^2))$. The sum is the risk of an oracle that keeps exactly the coefficients above the noise level, so the threshold loses at most a factor of order $\ln N$ to it (Donoho and Johnstone, 1994).
- **Cost.** Linear filters and wavelet shrinkage cost $O(N)$ or $O(N \log N)$ for $N$ samples; the Kalman filter costs $O(n^3)$ per sample for a state of size $n$.

## Reductions

- **To linear MMSE estimation.** For second-order models, denoising is the [Wiener filter](/wiener-filter/) problem with the desired signal $x$ and the input $y$.
- **To state estimation.** For a signal with a state model, denoising is [state estimation](/state-estimation/): filtering for a causal answer, smoothing for an offline one.
- **To regularized least squares.** Smoothing splines, Tikhonov smoothing and total variation are minimizers of $\|\hat x - y\|^2 + \lambda R(\hat x)$ for a penalty $R$, see [Tikhonov regularization](/tikhonov-regularization/). Soft thresholding is the proximal step of the $\ell_1$ norm, the step of [iterative shrinkage-thresholding](/iterative-shrinkage-thresholding/).
- **Image denoising contains it.** A method for [image denoising](/image-denoising/) that works on rows applies to a signal, but the good image methods use two-dimensional structure that a signal does not have.

## Applications

- **Speech enhancement** for phones, hearing aids and speech recognition in noise.
- **Biomedical signals.** Electrocardiograms and electroencephalograms carry mains hum, muscle noise and drift.
- **Sensor and instrument data.** Accelerometers, strain gauges and spectrometers, often with Savitzky-Golay smoothing.
- **Audio restoration.** Hiss and crackle removal from old recordings.
- **Finance and economics.** Trend extraction from noisy series.
- **Preprocessing.** Detection, [pitch detection](/pitch-detection/) and spectral estimation work better on a cleaner signal.

## References
