---
tag: 7WHC1B
kind: definition
slug: frequency-response
name: Frequency response
area: graphics-and-signals/signal-processing
level: core
summary: "The function H(e^(iω)) = sum of h[n] e^(-iωn) of a stable LTI system: the complex gain it applies to the sinusoid of frequency ω, read as a magnitude, a phase and a group delay."
prereqs: [impulse-response, discrete-time-fourier-transform]
see_also: [transfer-function, z-transform, bibo-stability, minimum-phase, fir-filter, digital-filter-design, goertzel-algorithm, horner-rule]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 2.6.1, Eigenfunctions for Linear Time-Invariant Systems (the frequency response, and suddenly applied complex exponentials) and Chapter 5, Transform Analysis of Linear Time-Invariant Systems (magnitude, phase and group delay, and the frequency response of rational system functions)
  - book: isbn:9780138147570
    title: Alan V. Oppenheim, Alan S. Willsky and S. Hamid Nawab, Signals and Systems, second edition, Prentice Hall, 1997
    locator: Chapter 3 (complex exponentials as eigenfunctions of LTI systems) and Chapter 6, Time and Frequency Characterization of Signals and Systems
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: Chapter 5, Frequency-Domain Analysis of LTI Systems
---

The frequency response of a stable [linear time-invariant system](/linear-time-invariant-system/) is the function $H(e^{i\omega}) = \sum_n h[n] e^{-i\omega n}$ of the frequency $\omega$ in radians per sample, the [discrete-time Fourier transform](/discrete-time-fourier-transform/) of the [impulse response](/impulse-response/). The complex sinusoid $e^{i\omega n}$ passes through the system with only one change: the output is $H(e^{i\omega})\, e^{i\omega n}$. So its magnitude is the gain at $\omega$, its phase is the shift, and the derivative of the phase gives the group delay of a narrow-band signal near $\omega$. For a filter with a rational [transfer function](/transfer-function/) $H(z) = B(z)/A(z)$, it is $H$ on the unit circle, and Horner's rule evaluates it at one frequency in $O(p + q)$ operations.

## Definition

**Notation.** Signals are sequences $x[n]$, $n \in \mathbb{Z}$. The frequency $\omega$ is in radians per sample and is taken in $[-\pi, \pi]$; for a signal sampled at the rate $f_s$, it is the frequency $f = \omega f_s / (2\pi)$ Hz, and $\omega = \pi$ is $f_s / 2$.

**Definition.** Let $h \in \ell^1$, that is, the system is [BIBO stable](/bibo-stability/). The frequency response is

$$H(e^{i\omega}) = \sum_{n=-\infty}^{\infty} h[n]\, e^{-i\omega n}, \qquad \omega \in \mathbb{R}.$$

The series converges absolutely and uniformly, so $H$ is continuous and $2\pi$ periodic, and $|H(e^{i\omega})| \le \sum_n |h[n]|$.

**Eigenfunctions.** For the input $x[n] = e^{i\omega_0 n}$ for all $n$,

$$y[n] = \sum_k h[k]\, e^{i\omega_0 (n - k)} = H(e^{i\omega_0})\, e^{i\omega_0 n}.$$

If $h$ is real, then $H(e^{-i\omega}) = \overline{H(e^{i\omega})}$, and the input $\cos(\omega_0 n)$ gives $|H(e^{i\omega_0})| \cos(\omega_0 n + \arg H(e^{i\omega_0}))$.

**Magnitude, phase and delay.** Write $H(e^{i\omega}) = |H(e^{i\omega})|\, e^{i\phi(\omega)}$.

- The *magnitude response* $|H(e^{i\omega})|$ is the gain; in decibels it is $20 \log_{10} |H(e^{i\omega})|$.
- The *phase response* $\phi(\omega)$ is defined modulo $2\pi$. The *unwrapped* phase is the continuous choice of $\phi$ on each interval where $H \ne 0$; at a zero of $H$ on the unit circle it can jump by $\pi$.
- The *group delay* is $\tau(\omega) = -\dfrac{d\phi}{d\omega}$, in samples. A signal whose spectrum is concentrated near $\omega_0$ comes out with its envelope delayed by about $\tau(\omega_0)$ samples.
- The *phase delay* is $-\phi(\omega)/\omega$.

**Linear phase.** A real FIR filter of length $M$ with $h[n] = h[M - 1 - n]$ has $H(e^{i\omega}) = e^{-i\omega (M-1)/2} A(\omega)$ with $A$ real, so its group delay is the constant $(M - 1)/2$ wherever $A(\omega) \ne 0$. All frequencies are delayed alike and the waveform of the passband is kept. A causal IIR filter with a rational $H$ cannot have exactly linear phase, unless it is FIR.

**Rational systems.** For $H(z) = B(z)/A(z)$ with $B(z) = \sum_{k=0}^{q} b_k z^{-k}$ and $A(z) = \sum_{k=0}^{p} a_k z^{-k}$, causal and stable,

$$H(e^{i\omega}) = \frac{\sum_{k=0}^{q} b_k e^{-i\omega k}}{\sum_{k=0}^{p} a_k e^{-i\omega k}}, \qquad |H(e^{i\omega})| = \left|\frac{b_0}{a_0}\right| \frac{\prod_k |e^{i\omega} - c_k|}{\prod_k |e^{i\omega} - d_k|},$$

where $c_k$ are the zeros and $d_k$ the poles. So the gain is small near a zero close to the circle and large near a pole close to it. The group delay is $\tau_B(\omega) - \tau_A(\omega)$ with $\tau_P(\omega) = \mathrm{Re}\left(\frac{\sum_k k\, p_k e^{-i\omega k}}{\sum_k p_k e^{-i\omega k}}\right)$ for a polynomial with the coefficients $p_k$.

**Computing it.** At one frequency, [Horner's rule](/horner-rule/) in $e^{-i\omega}$ gives $B$ and $A$ with $p + q$ complex multiplications. At $K$ equally spaced frequencies $\omega_j = 2\pi j / K$ with $K > \max(p, q)$, the FFTs of the zero-padded coefficient vectors give all of them in $O(K \log K)$; at a few frequencies, the [Goertzel algorithm](/goertzel-algorithm/) is cheaper.

**Transient and steady state.** For the input $x[n] = e^{i\omega_0 n} u[n]$, which starts at $n = 0$, a causal system gives $y[n] = H(e^{i\omega_0}) e^{i\omega_0 n} - \left(\sum_{k > n} h[k] e^{-i\omega_0 k}\right) e^{i\omega_0 n}$. The second term is the transient. For a stable system it tends to $0$, bounded by $\sum_{k > n} |h[k]|$; for a rational system whose largest pole modulus is $r < 1$, it decays like $n^{m-1} r^n$, where $m$ is the largest multiplicity of a pole of modulus $r$.

## Examples and non-examples

- **Moving average of 3.** $h = [\frac{1}{3}, \frac{1}{3}, \frac{1}{3}]$ gives $H(e^{i\omega}) = \frac{1}{3}(1 + e^{-i\omega} + e^{-2i\omega}) = e^{-i\omega}\, \frac{1 + 2\cos\omega}{3}$. Then $H(1) = 1$, $|H(e^{i\pi/3})| = \frac{2}{3}$, $H(e^{\pm 2\pi i/3}) = 0$, and $|H(e^{i\pi})| = \frac{1}{3}$. It is lowpass, causal, stable and linear phase, with group delay $1$ sample. At $\omega = 2\pi/3$ the real factor $1 + 2\cos\omega$ changes sign, and the phase jumps by $\pi$.
- **First-order recursion.** $y[n] = \frac{1}{2} y[n-1] + x[n]$ gives $H(e^{i\omega}) = \frac{1}{1 - \frac{1}{2} e^{-i\omega}}$. At $\omega = 0$ it is $2$; at $\omega = \pi/2$ it is $\frac{1}{1 + i/2} = 0.8 - 0.4i$, with magnitude $2/\sqrt{5} \approx 0.894$; at $\omega = \pi$ it is $\frac{2}{3}$. The group delay is $\frac{a\cos\omega - a^2}{1 - 2a\cos\omega + a^2}$ with $a = \frac{1}{2}$: $1$ sample at $\omega = 0$, $-0.2$ at $\pi/2$ and $-\frac{1}{3}$ at $\pi$. A negative group delay does not break causality; it is a property of the envelope of narrow-band signals only.
- **Delay.** $h = \delta[n - n_0]$ gives $e^{-i\omega n_0}$: gain $1$, linear phase, group delay $n_0$.
- **First difference.** $y[n] = x[n] - x[n-1]$ gives $1 - e^{-i\omega} = 2i\, e^{-i\omega/2} \sin(\omega/2)$, with gain $2|\sin(\omega/2)|$: $0$ at $\omega = 0$ and $2$ at $\omega = \pi$, a highpass filter.
- **Ideal lowpass.** $H(e^{i\omega}) = 1$ for $|\omega| < \omega_c$ and $0$ otherwise. Its impulse response $\sin(\omega_c n)/(\pi n)$ is in $\ell^2$ but not in $\ell^1$, so the defining series converges only in the mean-square sense, and the system is not BIBO stable.
- **Non-example, unstable.** For $y[n] = 2 y[n-1] + x[n]$, the formula $B/A = 1/(1 - 2e^{-i\omega})$ is finite at every $\omega$, but it is not a frequency response: $h[n] = 2^n u[n]$ is not in $\ell^1$, the series diverges, and the input $e^{i\omega_0 n} u[n]$ gives an output that grows like $2^n$ instead of settling.
- **Non-example, nonlinear.** The [median filter](/median-filter/) maps a sinusoid to a signal that is not a scaled and shifted copy of it, so no frequency response describes it.

## Related definitions

- [Transfer function](/transfer-function/): $H(z)$ off the unit circle, with its poles and zeros.
- [Discrete-time Fourier transform](/discrete-time-fourier-transform/): the transform that the frequency response is, applied to $h$.
- [BIBO stability](/bibo-stability/): the condition $h \in \ell^1$ under which the frequency response exists as a continuous function.
- [Minimum phase](/minimum-phase/): among the systems with one magnitude response, the one with the least phase lag and group delay.
- [FIR filter](/fir-filter/) and [digital filter design](/digital-filter-design/): filters chosen to match a given frequency response.
- [Gibbs phenomenon](/gibbs-phenomenon/): the ripple of a truncated ideal frequency response.

## References
