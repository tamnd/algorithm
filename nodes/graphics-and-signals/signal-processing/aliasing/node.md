---
tag: 2AWSJX
kind: concept
slug: aliasing
name: Aliasing
aliases:
- frequency folding
- jaggies
- spectral folding
area: graphics-and-signals/signal-processing
level: core
summary: "After sampling at rate fs, a frequency f and every f + k fs give the same samples, so content above fs/2 reappears at a false lower frequency."
prereqs: [discrete-time-fourier-transform]
see_also: [sampling-theorem, nyquist-rate, antialiasing, sample-rate-conversion, supersampling-antialiasing, image-resampling, mipmap, circular-convolution]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 4, Sampling of Continuous-Time Signals (the frequency-domain view of sampling as a sum of shifted spectra, aliasing, anti-aliasing prefilters and downsampling)
  - book: isbn:9780138147570
    title: Alan V. Oppenheim, Alan S. Willsky and S. Hamid Nawab, Signals and Systems, second edition, Prentice Hall, 1997
    locator: Chapter 7, Sampling (impulse-train sampling, the effect of undersampling as aliasing, and the stroboscopic effect)
  - paper: doi:10.1109/JRPROC.1949.232969
    title: Claude E. Shannon, Communication in the Presence of Noise, Proceedings of the IRE 37(1), 1949
    locator: Section II, The Sampling Theorem (pp. 11 to 12)
---

Aliasing is what happens when a signal is sampled too slowly: two different frequencies give exactly the same samples, so after sampling they cannot be told apart. With the sampling rate $f_s$ in samples per second and frequencies in Hz, a complex tone at $f$ and a tone at $f + k f_s$ for any integer $k$ have equal samples at every instant $n/f_s$. A real tone above $f_s/2$ therefore shows up at a false frequency between $0$ and $f_s/2$, its *alias*, and the distortion cannot be removed after the fact. This page is the signal processing side; how renderers fight the same effect on the screen is on the page [antialiasing](/antialiasing/).

## In plain words

A camera that takes pictures of a spinning wheel twenty-four times a second does not see the motion between pictures. If the wheel turns almost a full spoke between two pictures, it looks as if it moved a little backwards. The pictures are correct, but they fit a slow backward turn as well as the fast forward one. Sampling any signal works the same way. A fast wave and a slow wave can pass through the same points at the sampling instants. After sampling, only the points remain, and nothing in them says which wave made them. So a sampler must be fast enough, or the fast parts must be removed before sampling.

## The idea

**One identity.** Let $T = 1/f_s$. For every integer $n$ and integer $k$,

$$e^{2\pi i (f + k f_s) n T} = e^{2\pi i f n T}\, e^{2\pi i k n} = e^{2\pi i f n T}.$$

So the frequencies $f, f \pm f_s, f \pm 2f_s, \ldots$ are indistinguishable from their samples. In the normalized frequency $\omega = 2\pi f/f_s$ of the [discrete-time Fourier transform](/discrete-time-fourier-transform/), this is the $2\pi$ periodicity of $e^{i\omega n}$. Each class has exactly one member in the *baseband* $[-f_s/2, f_s/2)$, the alias $f - f_s \lfloor f/f_s + 1/2 \rfloor$.

**Real tones fold.** A real cosine is a pair of complex tones at $\pm f$. Taking the alias of both shows that $\cos(2\pi f t + \varphi)$ and $\cos(2\pi f' t + \varphi')$ have the same samples when $f' = k f_s + f$ with $\varphi' = \varphi$, or $f' = k f_s - f$ with $\varphi' = -\varphi$. The apparent frequency is the distance from $f$ to the nearest multiple of $f_s$, a number in $[0, f_s/2]$. Plotted against $f$, it is a zigzag: it rises from $0$ to $f_s/2$, falls back to $0$ at $f_s$, and repeats. This is why aliasing is also called *frequency folding*, with folds at the odd multiples of $f_s/2$. A sine changes sign when it folds from the falling side: $\sin(2\pi(f_s - f) nT) = -\sin(2\pi f nT)$.

**What happens to a whole spectrum.** Let $x(t)$ have finite energy and a spectrum $X(f) = \int x(t) e^{-2\pi i f t} dt$ that decays fast enough for the sums to converge, for example a continuous $X$ with $|X(f)| = O(|f|^{-2})$ and a summable sequence of samples. The Poisson summation formula gives the DTFT of the samples:

$$\sum_{n} x(nT)\, e^{-2\pi i f n T} = f_s \sum_{k} X(f - k f_s).$$

The spectrum of the sampled signal is the sum of copies of $X$ shifted by every multiple of $f_s$. If $X$ is zero outside $|f| < f_s/2$, the copies do not overlap, and the baseband copy is $X$ itself; that is the [sampling theorem](/sampling-theorem/). Otherwise the tails of the neighbouring copies add into the baseband, and the content of $X$ at $f + kf_s$ is added to the content at $f$. The sum mixes them with their phases, so no later filter can split them again.

**The boundary at $f_s/2$.** A tone exactly at $f_s/2$ is its own alias, since $f_s/2 - f_s = -f_s/2$. Its samples are $\cos(\pi n + \varphi) = (-1)^n \cos\varphi$: the amplitude and the phase are mixed into one number, and the sine $\sin(\pi n) = 0$ vanishes at every sample. This is why the sampling theorem needs $f_s$ strictly above twice the highest frequency for signals that contain a spectral line at the band edge.

**Prevention.** Information lost to aliasing cannot be recovered from the samples, because the map from signals to samples is many to one. There are three remedies, all applied before or during sampling: raise $f_s$ above twice the highest frequency present (the [Nyquist rate](/nyquist-rate/)); remove the content above $f_s/2$ with an analog low-pass *anti-aliasing filter* before the sampler; or, when the signal is computed rather than measured, take many samples per output value and average them, which is [supersampling](/supersampling-antialiasing/) in rendering. A digital filter after the sampler is too late.

**Downsampling aliases too.** Keeping every $M$-th sample, $y[n] = x[Mn]$, is sampling at the rate $f_s/M$. Its DTFT is $Y(e^{i\omega}) = \frac{1}{M}\sum_{k=0}^{M-1} X(e^{i(\omega - 2\pi k)/M})$, so a digital low-pass filter with cutoff $\pi/M$ must come first. This is the job of the decimation filter in [sample-rate conversion](/sample-rate-conversion/) and [polyphase resampling](/polyphase-resampling/).

**The dual: time aliasing.** Sampling the DTFT at $N$ frequencies folds the sequence in time: the $N$-point inverse DFT returns $\sum_r x[n + rN]$. This is why linear convolution done with an $N$-point DFT wraps around into [circular convolution](/circular-convolution/) unless $N$ is at least the length of the result.

**In two dimensions.** An image is sampled on a grid of pixels, and a pattern finer than two pixels per period aliases to a coarser one. Regular fine patterns, such as fabric or a brick wall far away, alias to slow false waves called *moiré*. A sharp edge is not band-limited at all: its spectrum decays only like $1/f$, so no grid rate removes the alias completely, and the edge comes out as a staircase, the *jaggies*. Rendering handles these with prefiltering, [mipmaps](/mipmap/) and supersampling; the rendering methods are on [antialiasing](/antialiasing/) and its pages, and [image resampling](/image-resampling/) covers the image processing side.

**Bandpass sampling.** Aliasing can also be used on purpose. A real signal whose spectrum lies in a band $f_L \le |f| \le f_H$ can be sampled below $2f_H$, as long as the shifted copies of the two bands do not overlap. The admissible rates are $2f_H/k \le f_s \le 2f_L/(k - 1)$ for an integer $k$ with $1 \le k \le \lfloor f_H/(f_H - f_L) \rfloor$, and the band then folds intact into the baseband.

## Examples

**Three tones, one set of samples.** With $f_s = 10$ Hz, the cosines at $3$, $7$, $13$, $17$ and $23$ Hz all give the samples $\cos(2\pi \cdot 3n/10)$. The sine at $13$ Hz gives the same samples as the sine at $3$ Hz, and the sines at $7$ and $17$ Hz give their negatives, because they fold from the falling side of the zigzag. If the frequencies are kept as exact fractions and the phase $fn/f_s$ is reduced modulo one cycle before the cosine is taken, the samples at $f$ and at $f + kf_s$ are equal as floating-point numbers, bit for bit, for random rational $f$, $f_s$, $k$ and phases.

**Audio.** At the compact disc rate $f_s = 44.1$ kHz, a $30$ kHz tone that reaches the converter appears at $44.1 - 30 = 14.1$ kHz, a clearly audible pitch that was not in the sound. Converters therefore have a steep analog low-pass filter, or they sample much faster and decimate with a digital filter.

**The wagon wheel.** A wheel with $12$ spokes looks the same after $1/12$ of a turn, so at $r$ turns per second its picture repeats $12r$ times per second. Filmed at $24$ frames per second, at $r = 2$ the pattern frequency is $24$ Hz, which aliases to $0$: the wheel seems to stand still. At $r = 1.9$ the pattern frequency is $22.8$ Hz, which aliases to $22.8 - 24 = -1.2$ Hz: the wheel seems to turn backwards at $1.2/12 = 0.1$ turn per second.

**A tone at half the rate.** At $f_s = 10$ Hz, $\cos(2\pi \cdot 5t + \pi/4)$ gives $(-1)^n \cos(\pi/4) \approx \pm 0.7071$, the same samples as $0.7071\cos(2\pi \cdot 5t)$, and $\sin(2\pi \cdot 5t)$ gives only zeros.

**Aliasing of a signal that is not band-limited.** The Gaussian $x(t) = e^{-\pi t^2}$ has the spectrum $X(f) = e^{-\pi f^2}$, which is never exactly zero. By the Poisson formula, the relative error of the sampled spectrum at $f = 0$ is $\sum_{k \ne 0} e^{-\pi k^2 f_s^2}$. Evaluated from the formula and checked against the direct sum over $401$ samples, it is $0.0864348$ at $f_s = 1$ and $2e^{-4\pi} \approx 6.97 \times 10^{-6}$ at $f_s = 2$. Smooth signals alias very little once $f_s$ passes the band where most of their energy lies; signals with jumps alias much more.

**Downsampling by two.** If $x[n] = \cos(0.8\pi n)$ (the frequency $0.4 f_s$) is downsampled by $2$, the result is $\cos(1.6\pi n) = \cos(0.4\pi n)$, at $0.2$ of the new rate instead of the correct tone, which cannot exist at the new rate. A half-band low-pass filter before the downsampler removes it.

## Where it is used

- **Analog-to-digital conversion.** Every converter specifies an anti-aliasing filter, and the margin between the passband edge and $f_s/2$ sets the filter order. Oversampling converters move the problem into the digital domain, where steep filters are cheap.
- **Sample-rate conversion and multirate filter banks.** Decimators, [polyphase resamplers](/polyphase-resampling/) and the analysis banks of subband coders must control aliasing at each rate change; perfect-reconstruction filter banks are designed so that the aliases of the bands cancel.
- **Rendering and images.** Point sampling of geometry and textures produces jaggies, moiré and crawling edges in animation. The remedies, [supersampling](/supersampling-antialiasing/), [multisampling](/multisample-antialiasing/), [temporal antialiasing](/temporal-antialiasing/) and [mipmapping](/mipmap/), are on the rendering pages; [stratified sampling](/stratified-sampling/) turns structured aliases into less visible noise.
- **Spectral analysis.** A spectrum estimate from samples shows energy above $f_s/2$ at folded frequencies, and a true peak can hide under a false one. Time aliasing in the DFT matters for fast convolution with the FFT and for [frequency response](/frequency-response/) sampling.
- **Deliberate undersampling.** Stroboscopes and sampling oscilloscopes use the alias of a fast periodic signal to show it slowly, and radio receivers use bandpass sampling to move a narrow band at a high carrier frequency directly to the baseband.

## References
