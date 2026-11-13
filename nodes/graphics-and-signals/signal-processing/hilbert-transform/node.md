---
tag: MW0VT7
kind: definition
slug: hilbert-transform
name: Hilbert transform
area: graphics-and-signals/signal-processing
level: advanced
summary: "The linear map that multiplies each frequency by -i sgn(w), turning cos into sin. Its kernel is 1/(pi t) in continuous time and 2/(pi n) for odd n in discrete time."
prereqs: [discrete-time-fourier-transform, discrete-fourier-transform]
see_also: [analytic-signal, minimum-phase, cepstrum, empirical-mode-decomposition, fir-filter, frequency-response, circular-convolution, convolution-theorem]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 12, Discrete Hilbert Transforms (the ideal 90-degree phase shifter, its impulse response, and the relations between the real and imaginary parts of the transform of a causal sequence)
  - paper: doi:10.1109/78.782222
    title: S. Lawrence Marple Jr., Computing the discrete-time analytic signal via FFT, IEEE Transactions on Signal Processing 47(9), 1999, 2600 to 2603
    locator: the DFT multiplier with the DC and Nyquist bins treated apart
  - paper: doi:10.1049/ji-3-2.1946.0074
    title: Dennis Gabor, Theory of communication, Part 1, The analysis of information, Journal of the Institution of Electrical Engineers, Part III 93(26), 1946, 429 to 441
    locator: the complex signal whose imaginary part is the Hilbert transform of the real part (general locator)
---

The Hilbert transform $\mathcal{H}$ is the linear, shift-invariant map that delays every positive frequency of a signal by a quarter period and advances every negative frequency by a quarter period. In the frequency domain it multiplies by $-i\,\mathrm{sgn}(\omega)$, so it turns $\cos(\omega_0 t)$ into $\sin(\omega_0 t)$ and $\sin(\omega_0 t)$ into $-\cos(\omega_0 t)$. Its kernel is $1/(\pi t)$, which decays slowly and is not causal, so in practice the transform is computed with a DFT or approximated by a long FIR filter. It is the step from a real signal $x$ to its [analytic signal](/analytic-signal/) $x + i\,\mathcal{H}x$.

## Definition

**Continuous time.** For a real function $f$ on $\mathbb{R}$ with enough decay,

$$(\mathcal{H}f)(t) = \frac{1}{\pi}\, \mathrm{p.v.} \int_{-\infty}^{\infty} \frac{f(\tau)}{t - \tau}\, d\tau = \lim_{\varepsilon \to 0} \frac{1}{\pi} \int_{|t - \tau| > \varepsilon} \frac{f(\tau)}{t - \tau}\, d\tau,$$

the convolution of $f$ with $1/(\pi t)$ as a principal value. Its Fourier transform is $\widehat{\mathcal{H}f}(\omega) = -i\,\mathrm{sgn}(\omega)\, \hat f(\omega)$, with $\mathrm{sgn}(0) = 0$.

**Discrete time.** For a sequence $x[n]$, the ideal discrete Hilbert transformer is the system with [frequency response](/frequency-response/)

$$H(e^{i\omega}) = \begin{cases} -i, & 0 < \omega < \pi, \\ i, & -\pi < \omega < 0, \end{cases}$$

with $\omega$ in radians per sample, and $H = 0$ at $\omega = 0$ and $\omega = \pm\pi$. Its impulse response, from the inverse [discrete-time Fourier transform](/discrete-time-fourier-transform/), is

$$h[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} H(e^{i\omega})\, e^{i\omega n}\, d\omega = \begin{cases} \dfrac{2}{\pi n}, & n \text{ odd}, \\ 0, & n \text{ even}. \end{cases}$$

**Periodic signals and the DFT.** For a signal of period $N$, with the $N$-point [DFT](/discrete-fourier-transform/) $X[k]$ and bin $k$ at $\omega_k = 2\pi k / N$, the discrete Hilbert transform $y = \mathcal{H}x$ has

$$Y[k] = -i\,\mathrm{sgn}_N(k)\, X[k], \qquad \mathrm{sgn}_N(k) = \begin{cases} 1, & 0 < k < N/2, \\ -1, & N/2 < k < N, \\ 0, & k = 0 \text{ or } k = N/2. \end{cases}$$

This is a [circular convolution](/circular-convolution/) of $x$ with the inverse DFT of the multiplier. For even $N$ that kernel is

$$h_N[m] = \frac{2}{N} \sum_{k=1}^{N/2 - 1} \sin\frac{2\pi k m}{N} = \begin{cases} \dfrac{2}{N} \cot\dfrac{\pi m}{N}, & m \text{ odd}, \\ 0, & m \text{ even}, \end{cases}$$

the periodic form of $2/(\pi n)$: as $N \to \infty$ with $m$ fixed, $\frac{2}{N}\cot\frac{\pi m}{N} \to \frac{2}{\pi m}$. The DC bin and, for even $N$, the Nyquist bin $k = N/2$ are set to zero because a cosine at those frequencies has no sine partner on the sampling grid: $\sin(0 \cdot n) = 0$ and $\sin(\pi n) = 0$.

## Examples and non-examples

**Cosine to sine.** For $0 < \omega_0 < \pi$, $\mathcal{H}\cos(\omega_0 n + \varphi) = \sin(\omega_0 n + \varphi)$ and $\mathcal{H}\sin(\omega_0 n + \varphi) = -\cos(\omega_0 n + \varphi)$. In the DFT form this holds exactly for every bin frequency $\omega_0 = 2\pi k / N$ with $0 < k < N/2$, on one full period. A worked case with $N = 4$, $k = 1$: $x = \cos(\pi n / 2) = [1, 0, -1, 0]$ has $X = [0, 2, 0, 2]$; the multiplier gives $Y = [0, -2i, 0, 2i]$, and the inverse DFT is $[0, 1, 0, -1] = \sin(\pi n / 2)$.

**Constants and the Nyquist tone vanish.** $\mathcal{H}$ maps a constant to 0, and in the DFT form also $(-1)^n$ to 0. So $\mathcal{H}$ is not invertible on all signals. On signals with no DC and no Nyquist component, $\mathcal{H}(\mathcal{H}x) = -x$, because $(-i\,\mathrm{sgn})^2 = -1$ on the other bins.

**Energy and orthogonality.** By Parseval's identity, $\sum_n |\mathcal{H}x[n]|^2 = \sum_n |x[n]|^2$ minus the energy of the DC and Nyquist parts. For real $x$, the sum $\sum_n x[n]\, \mathcal{H}x[n]$ is zero: the multiplier is odd and purely imaginary, so the cross terms cancel in pairs of bins $k$ and $N - k$.

**A non-example: a delay.** A delay by $d$ samples multiplies by $e^{-i\omega d}$, a phase that grows with the frequency. The Hilbert transform shifts every positive frequency by the same $-\pi/2$, which no delay does. A delay of a quarter period works for one frequency only.

**A non-example: a short FIR filter.** The ideal kernel $2/(\pi n)$ decays like $1/n$, so truncating it converges slowly and with ripple. Truncating at $|n| \le K$ and applying it to $\cos(0.2\pi n)$ gives, at $n = 3$, errors against $\sin(0.2\pi n)$ of about 0.145 for $K = 5$, 0.017 for $K = 21$, 0.0098 for $K = 85$ and 0.00094 for $K = 341$. Good FIR Hilbert transformers are designed with a window or by the [Parks-McClellan algorithm](/parks-mcclellan-algorithm/), and are accurate only in a band away from 0 and $\pi$; see [FIR filter](/fir-filter/).

**A non-example: products.** $\mathcal{H}\bigl(a[n] \cos(\omega_0 n)\bigr) = a[n] \sin(\omega_0 n)$ holds when the spectrum of $a$ lies below $\omega_0$ (Bedrosian's theorem), not in general. The [analytic signal](/analytic-signal/) page gives a case where the envelope comes out wrong by 0.40.

## Related definitions

- **[Analytic signal](/analytic-signal/).** $z = x + i\,\mathcal{H}x$ has no negative frequencies, and its modulus and argument define the envelope and the instantaneous phase.
- **Causality and the real and imaginary parts.** For a causal sequence, the real and the imaginary part of its DTFT determine each other through a Hilbert transform in frequency. For a [minimum-phase](/minimum-phase/) sequence, the log magnitude and the phase form such a pair, which the [cepstrum](/cepstrum/) uses. In physics the same relations are the Kramers-Kronig relations.
- **Fourier multipliers.** $\mathcal{H}$ is the multiplier $-i\,\mathrm{sgn}(\omega)$; by the [convolution theorem](/convolution-theorem/) every such multiplier is a convolution, here with $1/(\pi t)$ or $2/(\pi n)$.
- **Single-sideband modulation.** $x \cos(\omega_c n) - \mathcal{H}x\, \sin(\omega_c n)$ keeps only the upper sideband of $x$ around the carrier $\omega_c$.
- **Instantaneous frequency.** The Hilbert transform of the modes of the [empirical mode decomposition](/empirical-mode-decomposition/) gives their instantaneous frequencies in the Hilbert-Huang spectrum.

## References
