---
tag: BVYFGY
kind: problem
slug: signal-reconstruction
name: Signal reconstruction
aliases:
- interpolation of samples
- reconstruction from samples
area: graphics-and-signals/signal-processing
level: core
summary: "Given samples of a continuous-time signal and a model of the signal class, compute the signal at every time, exactly when the model allows and with a small error otherwise."
prereqs: [sampling-theorem]
see_also: [sinc-interpolation, reconstruction-filter, image-resampling, cubic-spline-interpolation, piecewise-linear-interpolation, nonuniform-fft, compressed-sensing, phase-retrieval]
sources:
  - paper: doi:10.1109/5.843002
    title: Michael Unser, Sampling, 50 Years After Shannon, Proceedings of the IEEE 88(4), 2000
    locator: pp. 569 to 587 (reconstruction in shift-invariant spaces, splines, consistent and least-squares reconstruction, error rates in the sampling step, and nonuniform sampling)
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 4, Sampling of Continuous-Time Signals (the ideal discrete-to-continuous converter, the practical digital-to-analog converter with a zero-order hold and its compensation)
  - paper: doi:10.1109/JRPROC.1949.232969
    title: Claude E. Shannon, Communication in the Presence of Noise, Proceedings of the IRE 37(1), 1949
    locator: Section II, The Sampling Theorem (reconstruction of a band-limited function from its samples, and the remark on nonuniform sample positions)
---

Signal reconstruction is the problem of computing a continuous-time signal $x(t)$ at every time from a discrete set of its samples, usually $x(nT)$ at the rate $f_s = 1/T$. Samples alone never fix the signal: infinitely many functions pass through any set of points. So the problem always comes with a model, a class of signals that the answer must belong to, such as the signals band-limited to $f_s/2$, splines of some degree, or sparse sums of pulses. For band-limited signals of finite energy the [sampling theorem](/sampling-theorem/) makes the answer unique and [sinc interpolation](/sinc-interpolation/) computes it; the practical methods trade that exactness for short kernels, causality or robustness to noise.

## In plain words

A list of measurements says what a signal was at some moments. Between those moments it says nothing, so we must add a belief about the signal. If we believe the signal is smooth and slow, there is exactly one answer, and we can compute it. If we believe it is made of straight pieces, a different answer fits. In practice we want an answer that is fast to compute, that does not need future measurements, and that does not change much when the measurements have a little noise. Each method of reconstruction is a different balance of these wishes.

## Definition

**Input.** A sampling set $\{t_n\}$, usually $t_n = nT$; the values $y_n = x(t_n) + e_n$, where $e_n$ is a measurement error (zero for exact samples); and a class $\mathcal{V}$ of admissible signals, a space of functions of time in seconds.

**Output.** A signal $\tilde x \in \mathcal{V}$, given as a procedure that returns $\tilde x(t)$ for any $t$.

**Exact version.** When $e_n = 0$ and the samples determine each element of $\mathcal{V}$ uniquely (the sampling set is a *uniqueness set* for $\mathcal{V}$), find the unique $\tilde x \in \mathcal{V}$ with $\tilde x(t_n) = y_n$ for all $n$.

**Approximate version.** When $x$ is not in $\mathcal{V}$, or the samples are noisy, find $\tilde x \in \mathcal{V}$ that minimizes an error, for example $\int |x - \tilde x|^2 dt$ (the orthogonal projection, which needs a prefilter before sampling), or $\sum_n |\tilde x(t_n) - y_n|^2 + \lambda R(\tilde x)$ for a regularizer $R$.

**Linear shift-invariant form.** For uniform samples most methods have the form

$$\tilde x(t) = \sum_n c_n\, \varphi\!\left(\frac{t}{T} - n\right),$$

with a kernel $\varphi$ and coefficients $c_n$ computed from the samples by a digital filter. If $\varphi(0) = 1$ and $\varphi(k) = 0$ at the other integers, the kernel is *interpolating* and $c_n = y_n$. The sinc kernel, the box of the zero-order hold, the tent and the cubic convolution kernels are interpolating; B-splines of degree above one are not, and need a prefilter to compute $c_n$.

## Variants

- **Uniform, band-limited, exact.** $\mathcal{V}$ is the space of finite-energy signals with spectrum in $[-f_s/2, f_s/2]$. The answer is unique and equals the cardinal series.
- **Uniform with oversampling.** The signal is band-limited to $B < f_s/2$. Many kernels are then exact, and short, smooth ones can be chosen.
- **Shift-invariant spaces.** $\mathcal{V}$ is spanned by integer shifts of one generator, such as a B-spline of degree $m$. Reconstruction is exact for signals in $\mathcal{V}$ and gives an approximation of order $T^{m+1}$ for smooth signals.
- **Nonuniform samples.** The times $t_n$ are irregular, from jitter, missing data or the geometry of the sensor. For band-limited signals, samples whose average density is above the Nyquist rate still fix the signal; Kadec's theorem gives stability for perturbations $|t_n - nT| \le LT$ with $L < 1/4$.
- **Noisy samples.** The goal is an estimate with small mean-square error; regularization ([Tikhonov regularization](/tikhonov-regularization/)) or Wiener filtering balance fidelity against smoothness.
- **Finite records.** Only $N$ samples exist, so the reconstruction near the ends must assume something about the missing samples, such as zeros, periodicity or a mirror image.
- **Structured signals below the Nyquist rate.** Sparse spike trains, signals with a finite rate of innovation and signals sparse in a basis can be rebuilt from fewer samples than the Nyquist rate of their band, by [sparse signal recovery](/sparse-signal-recovery/) and [compressed sensing](/compressed-sensing/).
- **Magnitude-only samples.** If only $|x|$ or $|X|$ is measured, the problem becomes [phase retrieval](/phase-retrieval/).
- **Images and volumes.** The same problem on a grid in two or three dimensions; the rendering and image versions are on [reconstruction filter](/reconstruction-filter/) and [image resampling](/image-resampling/).

## Examples

**The zero-order hold.** A digital-to-analog converter that holds each sample for one period computes $\tilde x(t) = y_n$ for $nT \le t < (n+1)T$. Its kernel is a box of width $T$, with frequency response $T\,\mathrm{sinc}(fT)\, e^{-i\pi f T}$. Relative to the ideal reconstruction it attenuates a tone at $f$ by $|\mathrm{sinc}(f/f_s)|$, which is $0.9003$ ($-0.91$ dB) at $f_s/4$ and $2/\pi \approx 0.6366$ ($-3.92$ dB) at $f_s/2$. For compact disc audio, $f_s = 44.1$ kHz, a $20$ kHz tone is attenuated to $0.6944$ ($-3.17$ dB). It also delays the signal by $T/2$ and leaves images of the spectrum around multiples of $f_s$, so converters follow it with an analog smoothing filter and often boost high frequencies in a digital filter beforehand.

**Linear interpolation.** Joining the samples by straight lines uses the tent kernel; its error on a signal with a continuous second derivative is at most $\frac{T^2}{8}\max|x''|$. For $\cos(2\pi f t)$ with $T = 1$ and $f = 0.1$ the bound is $(2\pi \cdot 0.1)^2/8 \approx 0.0493$, and the largest error over ten sample intervals, evaluated at a step of $0.001$, is $0.0466$. The frequency response of the tent relative to the ideal is $\mathrm{sinc}^2(f/f_s)$: $-1.82$ dB at $f_s/4$ and $-7.84$ dB at $f_s/2$.

**The band-limited answer.** For the samples of $\mathrm{sinc}(t - 1/2)$ at the integers, the cardinal series reconstructs the pulse exactly, but truncated to $2N + 1$ terms it misses the peak value $1$ at $t = 1/2$ by about $0.2026/N$ (see [sinc interpolation](/sinc-interpolation/) for the measured table).

**Too few samples.** The samples of $\sin(2\pi B t)$ at the rate $2B$ are all zero, the same as those of the zero signal; no method can recover the sine from them. This is the failure case of the [sampling theorem](/sampling-theorem/), and it shows that the model must exclude such signals for the problem to have a unique answer.

## Known algorithms

| method | kernel | exact for | error for smooth signals | locality |
|---|---|---|---|---|
| zero-order hold | box | piecewise constants | $O(T)$ | one sample, causal |
| [linear interpolation](/piecewise-linear-interpolation/) | tent | piecewise linear | $O(T^2)$ | two samples |
| cubic convolution (Keys, Catmull-Rom) | piecewise cubic | quadratics | $O(T^3)$ | four samples |
| [cubic spline interpolation](/cubic-spline-interpolation/) | cubic B-spline with prefilter | cubic splines | $O(T^4)$ | global prefilter, then four samples |
| windowed sinc | sinc times a window | approximately band-limited | set by the window length | $K$ samples |
| [sinc interpolation](/sinc-interpolation/) | sinc | band-limited to $f_s/2$ | exact, truncation $O(1/N)$ | all samples |

- **Periodic band-limited signals.** [Trigonometric interpolation](/trigonometric-interpolation/) by the inverse DFT, or zero padding of the DFT followed by the [FFT](/fast-fourier-transform/), is exact and costs $O(N \log N)$ for $N$ samples.
- **Rate changes.** [Polyphase resampling](/polyphase-resampling/) and [sample-rate conversion](/sample-rate-conversion/) evaluate a windowed sinc at a regular set of new times.
- **Polynomial models.** [Lagrange interpolation](/lagrange-interpolation/) of a few nearby samples gives fractional-delay filters; global polynomials through many equally spaced samples are unstable.
- **Nonuniform samples.** The frame algorithm and conjugate gradient on the normal equations solve for the band-limited signal; the [nonuniform FFT](/nonuniform-fft/) makes each iteration fast. The Papoulis-Gerchberg iteration fills gaps in a band-limited record by alternating between enforcing the known samples and the band limit.
- **Noisy and structured signals.** Regularized least squares, Wiener filtering, and sparse recovery methods.

## Bounds

- **Density.** A uniqueness and stability bound: stable recovery of every signal band-limited to $B$ needs an average sampling density of at least $2B$ samples per second (Landau, 1967). Below it, some nonzero band-limited signal has samples that are arbitrarily small compared with its energy.
- **Approximation order.** A kernel that reproduces polynomials of degree $m$ (the Strang-Fix conditions) gives an error of order $T^{m+1}$ for smooth signals, and no kernel of this form does better without reproducing higher degrees. The zero-order hold has order $1$, linear interpolation order $2$, cubic splines order $4$.
- **Truncation of the ideal kernel.** With $N$ terms of the cardinal series, the error for samples that decay like $1/n$ is of order $1/N$, and the constant can be attained ([sinc interpolation](/sinc-interpolation/)).
- **Extrapolation is ill-posed.** Recovering a band-limited signal outside the interval where it was sampled, or from samples below the Nyquist density, has a condition number that grows exponentially with the length of the gap times the bandwidth, because prolate spheroidal wave functions concentrate almost all of their energy away from the observed interval.
- **Cost.** A kernel of $K$ taps costs $\Theta(K)$ per output time; the full cardinal series costs $\Theta(N)$; a prefilter of a spline method costs $\Theta(N)$ once for the record.

## Reductions

- **Reconstruction is filtering.** For uniform samples and an interpolating kernel, reconstruction equals passing the impulse train $\sum_n y_n \delta(t - nT)$ through an analog filter with impulse response $\varphi(t/T)$. The ideal low-pass filter gives the sinc series, and the design of $\varphi$ is filter design in the frequency domain (see [frequency response](/frequency-response/)).
- **Periodic reconstruction is the inverse DFT.** For a periodic band-limited signal, the samples over one period determine its Fourier coefficients through the DFT, and reconstruction evaluates the trigonometric polynomial.
- **Nonuniform band-limited reconstruction is a linear system.** Writing $\tilde x$ as a finite combination of shifted sincs or of exponentials turns the problem into a least-squares system; its conditioning depends on the largest gap between the times.
- **Upsampling by an integer factor is interpolation on a finer grid.** Inserting $L - 1$ zeros between samples and low-pass filtering at $\pi/L$ is exactly the reconstruction evaluated at the times $nT/L$.

## Applications

- **Digital-to-analog conversion** in audio, video and communications, with a hold circuit, an analog smoothing filter and digital compensation of the hold droop.
- **Image scaling, rotation and texture lookup**, where the choice of kernel sets the balance of blur, ringing and jaggies ([reconstruction filter](/reconstruction-filter/), [image resampling](/image-resampling/)).
- **Medical imaging.** MRI scanners sample the spatial frequency plane along curves; gridding with the [nonuniform FFT](/nonuniform-fft/) rebuilds the image.
- **Sensor networks, geophysics and astronomy**, where samples are irregular or missing and the reconstruction must fill gaps.
- **Audio editing and sample-rate conversion**, where fractional delays and rate changes need values between the samples.

## References
