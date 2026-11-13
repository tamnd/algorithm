---
tag: F0XV5Y
kind: concept
slug: analytic-signal
name: Analytic signal
aliases:
- pre-envelope
area: graphics-and-signals/signal-processing
level: advanced
summary: "The complex signal x + iH(x) of a real signal x. It has no negative frequencies, its real part is x, and its modulus and angle give the envelope and the instantaneous phase."
prereqs: [hilbert-transform]
see_also: [discrete-fourier-transform, empirical-mode-decomposition, time-frequency-analysis, fir-filter, sampling-theorem, minimum-phase]
sources:
  - paper: doi:10.1049/ji-3-2.1946.0074
    title: Dennis Gabor, Theory of communication, Part 1, The analysis of information, Journal of the Institution of Electrical Engineers, Part III 93(26), 1946, 429 to 441
    locator: the complex signal formed from a real signal and its Hilbert transform, with a one-sided spectrum (general locator)
  - paper: doi:10.1109/78.782222
    title: S. Lawrence Marple Jr., Computing the discrete-time analytic signal via FFT, IEEE Transactions on Signal Processing 47(9), 1999, 2600 to 2603
    locator: the DFT weights 1 at DC, 2 on the positive bins, 1 at the Nyquist bin and 0 on the negative bins, and the proof that the real part is the input
  - paper: doi:10.1109/PROC.1963.2308
    title: Edward Bedrosian, A product theorem for Hilbert transforms, Proceedings of the IEEE 51(5), 1963, 868 to 869
    locator: the condition on the spectra under which the Hilbert transform of a product acts on the high-frequency factor only
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 12, Discrete Hilbert Transforms (complex sequences with one-sided spectra; section number not confirmed)
---

The analytic signal of a real signal $x$ is the complex signal $z = x + i\,\mathcal{H}x$, where $\mathcal{H}$ is the [Hilbert transform](/hilbert-transform/). Gabor introduced it in 1946. Its spectrum is zero at all negative frequencies and twice the spectrum of $x$ at the positive ones, so it carries the same information as $x$ in half the band. Writing $z[n] = a[n]\, e^{i\varphi[n]}$ gives the envelope $a$ and the instantaneous phase $\varphi$ of $x$, and the step of the phase from sample to sample is the instantaneous frequency.

## In plain words

A real wave, such as a vibrating string seen from the side, goes up and down, and at any one moment you cannot tell how big the swing is or where in its cycle it is. Now imagine the same motion as a point going round a circle, seen from the side. The side view is the real wave. The distance of the point from the centre is the size of the swing, and the angle tells where in the cycle the wave is.

The analytic signal is that point on the circle. It adds to the real wave a second wave a quarter of a cycle behind it. From the pair you read off the loudness and the frequency at every moment. This works well when the signal is one slowly changing oscillation, and badly when several are mixed.

## The idea

**Why the negative half can go.** The spectrum of a real signal is conjugate symmetric, $X(e^{-i\omega}) = \overline{X(e^{i\omega})}$, so the negative frequencies repeat what the positive ones say. The [Hilbert transform](/hilbert-transform/) multiplies by $-i\,\mathrm{sgn}(\omega)$, so $z = x + i\,\mathcal{H}x$ has the spectrum

$$Z(e^{i\omega}) = \bigl(1 + \mathrm{sgn}(\omega)\bigr) X(e^{i\omega}) = \begin{cases} 2 X(e^{i\omega}), & 0 < \omega < \pi, \\ X(e^{i\omega}), & \omega = 0, \\ 0, & -\pi < \omega < 0, \end{cases}$$

with $\omega$ in radians per sample. Taking the real part puts the negative half back, $\operatorname{Re} z = \frac{1}{2}(z + \bar z) = x$.

**The discrete form.** For $N$ samples, Marple (1999) computes $z$ with one DFT and one inverse DFT. With $X[k]$ the $N$-point [DFT](/discrete-fourier-transform/) of $x$, set

$$Z[k] = \begin{cases} X[k], & k = 0, \\ 2X[k], & 1 \le k \le \lceil N/2 \rceil - 1, \\ X[N/2], & k = N/2 \text{ (even } N\text{ only)}, \\ 0, & \text{the other } k, \end{cases}$$

and $z = \mathrm{IDFT}(Z)$. The DC and Nyquist bins keep weight 1 because each is its own mirror image. With these weights $\operatorname{Re} z = x$ exactly, $\operatorname{Im} z$ is the periodic discrete Hilbert transform of $x$, and the bins $N/2 < k < N$ of $z$ are zero. The cost is that of two FFTs, $O(\log N)$ multiplications per sample. Like every DFT method, it treats $x$ as one period of a periodic signal, so the ends of a record that does not wrap smoothly give errors near the ends.

**Envelope, phase and frequency.** Write $z[n] = a[n]\, e^{i\varphi[n]}$ with $a[n] = |z[n]| \ge 0$. Then $x[n] = a[n] \cos\varphi[n]$ for every $n$, so $a$ is an envelope that touches $|x|$ where $\cos\varphi = \pm 1$. The instantaneous frequency in radians per sample is the phase step $\varphi[n+1] - \varphi[n] = \arg\bigl(z[n+1]\, \overline{z[n]}\bigr)$, taken in $(-\pi, \pi]$; in Hz it is that number times $f_s / (2\pi)$.

**When the envelope means what it should.** Many pairs $(a, \varphi)$ give the same $x = a \cos\varphi$; the analytic signal picks one. For $x = a[n] \cos(\omega_0 n + \theta)$ it picks the intended pair when the spectrum of $a$ lies in $|\omega| < \omega_0$ and $\omega_0 + $ that band stays below $\pi$, so that the shifted copies do not reach the negative frequencies. That is Bedrosian's theorem for products. When the spectra overlap, part of the signal folds across zero frequency and the envelope is wrong.

**One component at a time.** For a sum of oscillations, the analytic signal is the sum of their analytic signals, but the envelope and the phase of the sum are not those of any part. For two tones $z = e^{i\omega_1 t}(1 + c\, e^{i\Delta t})$ with $0 < c < 1$ and $\Delta = \omega_2 - \omega_1 > 0$, the derivative of the phase is

$$\varphi'(t) = \omega_1 + \Delta \frac{c^2 + c \cos\Delta t}{1 + c^2 + 2c \cos\Delta t},$$

and at $\cos\Delta t = -1$ with $c = \frac{1}{2}$ it is $\omega_1 + \Delta \cdot \frac{-1/4}{1/4} = \omega_1 - \Delta$, a frequency outside the band from $\omega_1$ to $\omega_2$. This is why the [empirical mode decomposition](/empirical-mode-decomposition/) first splits a signal into modes and only then takes their analytic signals.

## Examples

**A worked case.** Let $x = [1, 2, 3, 4]$. Its DFT is $X = [10, -2 + 2i, -2, -2 - 2i]$. The weights $[1, 2, 1, 0]$ give $Z = [10, -4 + 4i, -2, 0]$, and $z[n] = \frac{1}{4}\bigl(10 + (-4 + 4i)\, i^n - 2(-1)^n\bigr)$, that is

$$z = [1 + i,\ 2 - i,\ 3 - i,\ 4 + i].$$

The real part is $x$. The imaginary part $[1, -1, -1, 1]$ is the periodic Hilbert transform of $x$, and it is orthogonal to $x$: $1 - 2 - 3 + 4 = 0$. Bin 3 of $z$ is zero.

**A cosine.** For $x[n] = \cos(\omega_0 n)$ with $0 < \omega_0 < \pi$, $z[n] = e^{i\omega_0 n}$: the envelope is 1, the phase is $\omega_0 n$, and the instantaneous frequency is the constant $\omega_0$.

**An AM signal, spectra apart.** With $N = 64$, $a[n] = 1 + \frac{1}{2}\cos(2\pi \cdot 2n / 64)$ and $x[n] = a[n] \cos(2\pi \cdot 20 n / 64 + 0.3)$, the spectrum of $x$ lies in bins 18 to 22, all positive. The envelope $|z|$ equals $a$ to within $10^{-12}$, and the unwrapped phase is $2\pi \cdot 20 n / 64 + 0.3$.

**An AM signal, spectra overlapping.** With $a[n] = 1 + \frac{1}{2}\cos(2\pi \cdot 6n / 64)$ and a carrier in bin 4, $x$ has the components $\cos(4\theta) + \frac{1}{4}\cos(10\theta) + \frac{1}{4}\cos(2\theta)$, with $\theta = 2\pi n / 64$. The last one came from frequency $4 - 6 = -2$ and now sits at $+2$, so $z$ contains $\frac{1}{4} e^{2i\theta}$ where $a\, e^{4i\theta}$ would need $\frac{1}{4} e^{-2i\theta}$. The envelope $|z|$ differs from $a$ by up to 0.398.

## Where it is used

- **Envelope detection.** The demodulation of AM signals, the envelope of ultrasound echoes in B-mode imaging, and the envelope spectrum of vibration signals, where bearing faults show as periodic bursts.
- **Instantaneous frequency.** FM demodulation, chirp analysis in radar and sonar, and the Hilbert spectrum of the [empirical mode decomposition](/empirical-mode-decomposition/), which is one form of [time-frequency analysis](/time-frequency-analysis/).
- **Complex baseband.** Shifting $z$ down by the carrier, $z[n]\, e^{-i\omega_c n}$, gives the complex baseband or I/Q signal of communications, and halves the needed sample rate compared with the real band-pass signal; see the [sampling theorem](/sampling-theorem/).
- **Single-sideband modulation.** The real part of $z[n]\, e^{i\omega_c n}$ keeps only the upper sideband.
- **Phase synchrony.** In EEG and other biological signals, the phases of the analytic signals of band-filtered channels are compared to measure synchrony.
- **FIR approximations.** Real-time systems that cannot wait for a whole record use an [FIR filter](/fir-filter/) approximation of the Hilbert transform with a matching delay on the real part.

## References
