---
tag: 0QHXWM
kind: definition
slug: discrete-time-fourier-transform
name: Discrete-time Fourier transform
aliases:
- DTFT
area: graphics-and-signals/signal-processing
level: core
summary: "The function X(e^(iω)) = sum of x[n] e^(-iωn) of a continuous frequency ω, 2π periodic, that describes a discrete-time sequence as a mix of complex sinusoids."
prereqs: [discrete-fourier-transform]
see_also: [parsevals-theorem, aliasing, sampling-theorem, spectral-leakage, window-functions, fast-fourier-transform, z-transform, frequency-response]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 2 (the frequency-domain representation of sequences, the Fourier transform of a sequence, its convergence in the absolute and mean-square senses, its symmetry properties and theorems) and Chapter 8 (the DFT as samples of the Fourier transform, and time aliasing)
  - book: isbn:9780138147570
    title: Alan V. Oppenheim, Alan S. Willsky and S. Hamid Nawab, Signals and Systems, second edition, Prentice Hall, 1997
    locator: Chapter 5, The Discrete-Time Fourier Transform (the definition, convergence, the table of properties and the transform pairs)
  - book: isbn:9780123743701
    title: Stéphane Mallat, A Wavelet Tour of Signal Processing, The Sparse Way, third edition, Academic Press, 2009
    locator: Chapter 3, Discrete Revolution (the Fourier series of a discrete signal and the link with sampling)
---

The discrete-time Fourier transform (DTFT) of a sequence $x[n]$, $n \in \mathbb{Z}$, is the function $X(e^{i\omega}) = \sum_{n} x[n]\, e^{-i\omega n}$ of a real frequency $\omega$ in radians per sample. It is $2\pi$ periodic in $\omega$, so the interval $[-\pi, \pi]$ holds all of it, and the inverse formula writes $x[n]$ as an integral of complex sinusoids $e^{i\omega n}$ over that interval. The [discrete Fourier transform](/discrete-fourier-transform/) of a finite block is the DTFT sampled at $N$ equally spaced frequencies; this page is about the function of a continuous frequency, and the DFT page is about the finite computation.

## Definition

**Notation.** A *sequence* is a function $x : \mathbb{Z} \to \mathbb{C}$. The frequency $\omega$ is in radians per sample. When $x[n] = x_c(nT)$ comes from a signal sampled at the rate $f_s = 1/T$ in Hz, the frequency $\omega$ corresponds to $f = \omega f_s / (2\pi)$ Hz, so $\omega = \pm\pi$ is the frequency $\pm f_s/2$. The space $\ell^1$ holds the sequences with $\sum_n |x[n]| < \infty$, and $\ell^2$ those with $\sum_n |x[n]|^2 < \infty$; $\ell^1 \subset \ell^2$.

**Definition.** The DTFT of $x$ is

$$X(e^{i\omega}) = \sum_{n=-\infty}^{\infty} x[n]\, e^{-i\omega n}, \qquad \omega \in \mathbb{R},$$

where the sum is understood in one of two senses.

- *For $x \in \ell^1$.* The series converges absolutely and uniformly in $\omega$, because each term has modulus $|x[n]|$. So $X$ is a continuous function and $|X(e^{i\omega})| \le \sum_n |x[n]|$ for every $\omega$.
- *For $x \in \ell^2$.* The symmetric partial sums $X_N(e^{i\omega}) = \sum_{|n| \le N} x[n] e^{-i\omega n}$ converge in the mean-square sense on $[-\pi, \pi]$ to a function $X \in L^2[-\pi, \pi]$, defined up to a set of measure zero. This is the Riesz-Fischer theorem for the orthogonal system $e^{-i\omega n}$, and [Parseval's theorem](/parsevals-theorem/) gives the energy of $X$.

**Inverse.** In both cases

$$x[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{i\omega})\, e^{i\omega n}\, d\omega \qquad \text{for each } n \in \mathbb{Z}.$$

For $x \in \ell^1$ the proof is one exchange of sum and integral, allowed by the uniform convergence: $\frac{1}{2\pi}\int_{-\pi}^{\pi} \sum_m x[m] e^{-i\omega m} e^{i\omega n}\, d\omega = \sum_m x[m]\, \frac{1}{2\pi}\int_{-\pi}^{\pi} e^{i\omega(n - m)}\, d\omega = x[n]$, since the last integral is $2\pi$ for $m = n$ and $0$ for each other integer $m$. For $x \in \ell^2$ the same identity holds for each $X_N$ with $N \ge |n|$, and the inner product with $e^{i\omega n}$ is continuous in $L^2$, so it passes to the limit.

**Periodicity.** $e^{-i(\omega + 2\pi)n} = e^{-i\omega n}$ for every integer $n$, so $X(e^{i(\omega + 2\pi)}) = X(e^{i\omega})$. The notation $X(e^{i\omega})$ records this: $X$ depends on $\omega$ only through the point $e^{i\omega}$ of the unit circle. Engineering texts write $j$ for $i$.

**The main properties.** For $x, y \in \ell^1$ with transforms $X, Y$:

| sequence | DTFT | why |
|---|---|---|
| $a\,x[n] + b\,y[n]$ | $a X + b Y$ | linearity of the sum |
| $x[n - n_0]$ | $e^{-i\omega n_0} X(e^{i\omega})$ | substitute $m = n - n_0$ |
| $e^{i\omega_0 n} x[n]$ | $X(e^{i(\omega - \omega_0)})$ | the exponents add |
| $x[-n]$ | $X(e^{-i\omega})$ | substitute $m = -n$ |
| $\overline{x[n]}$ | $\overline{X(e^{-i\omega})}$ | conjugate each term |
| $(x * y)[n] = \sum_k x[k]\, y[n-k]$ | $X(e^{i\omega})\, Y(e^{i\omega})$ | Cauchy product of two absolutely convergent series |
| $x[n]\, y[n]$ | $\frac{1}{2\pi}\int_{-\pi}^{\pi} X(e^{i\theta})\, Y(e^{i(\omega - \theta)})\, d\theta$ | insert the inverse formula of $X$ |
| $n\, x[n]$ (if in $\ell^1$) | $i\, \frac{d}{d\omega} X(e^{i\omega})$ | differentiate term by term |

So a real sequence has $X(e^{-i\omega}) = \overline{X(e^{i\omega})}$: its magnitude is even and its phase is odd, and the band $[0, \pi]$ describes it. The convolution row is the discrete [convolution theorem](/convolution-theorem/), and it is the reason that an LTI system acts on each frequency by one complex factor, its [frequency response](/frequency-response/).

**Samples of the DTFT.** Let $N \ge 1$ and $\omega_k = 2\pi k/N$.

- If $x$ is zero outside $0 \le n \le N - 1$, then $X(e^{i\omega_k}) = \sum_{n=0}^{N-1} x[n] e^{-2\pi i kn/N}$, which is the $k$-th entry of the DFT of $(x[0], \ldots, x[N-1])$. Appending zeros to length $L > N$ and taking the length $L$ DFT gives the samples at $2\pi k/L$: zero padding samples the same function more densely, and it adds no resolution.
- If $x \in \ell^1$ has a longer support, the samples are the DFT of the folded block $\tilde x[j] = \sum_{r} x[j + rN]$, $0 \le j < N$. Proof: split $n = j + rN$; then $e^{-i\omega_k n} = e^{-i\omega_k j}$, and summing over $r$ first gives $X(e^{i\omega_k}) = \sum_{j=0}^{N-1} \tilde x[j] e^{-i\omega_k j}$. So sampling in frequency aliases in time, the mirror image of [aliasing](/aliasing/) in frequency.

**Cost.** The direct sum for a sequence of length $L$ costs $\Theta(L)$ complex multiply-adds for each frequency, and $\Theta(LM)$ for $M$ frequencies. For $M \ge L$ equally spaced frequencies, zero padding and the [FFT](/fast-fourier-transform/) give all of them in $O(M \log M)$. The [Goertzel algorithm](/goertzel-algorithm/) evaluates a few single frequencies in $\Theta(L)$ each with one real multiply per sample.

## Examples and non-examples

**The impulse.** $\delta[n]$, which is $1$ at $n = 0$ and $0$ elsewhere, has $X(e^{i\omega}) = 1$ at every frequency: an impulse contains each frequency with the same weight.

**A short sequence and its DFT.** For $x = (1, 2, 0, -1)$ at $n = 0, 1, 2, 3$, the DTFT is the trigonometric polynomial $1 + 2e^{-i\omega} - e^{-3i\omega}$. At $\omega = 0, \pi/2, \pi, 3\pi/2$ it takes the values $2$, $1 - 3i$, $0$ and $1 + 3i$, which are the four entries of the length 4 DFT. Between these points the function is not zero; for example, at $\omega = \pi/4$ it is $1 + 2e^{-i\pi/4} - e^{-3i\pi/4} \approx 3.1213 - 0.7071i$.

**The box and the Dirichlet kernel.** The box $x[n] = 1$ for $0 \le n \le L - 1$ has the geometric sum

$$X(e^{i\omega}) = \sum_{n=0}^{L-1} e^{-i\omega n} = e^{-i\omega (L-1)/2}\, \frac{\sin(L\omega/2)}{\sin(\omega/2)},$$

for $\omega$ not a multiple of $2\pi$, and $X = L$ at the multiples. Its magnitude has the value $L$ at $\omega = 0$, zeros at $\omega = 2\pi k/L$ for $k = 1, \ldots, L - 1$, and side lobes that fall off like $1/|\omega|$. For $L = 4$, $|X(e^{i\pi/4})| = 1/\sin(\pi/8) \approx 2.6131$. This function is the cause of [spectral leakage](/spectral-leakage/) and the reference shape for [window functions](/window-functions/).

**A decaying exponential.** For $|a| < 1$, $x[n] = a^n$ for $n \ge 0$ and $0$ for $n < 0$ is in $\ell^1$, and the geometric series gives $X(e^{i\omega}) = 1/(1 - a e^{-i\omega})$. With $a = 1/2$, $X = 2$ at $\omega = 0$, $0.8 - 0.4i$ at $\omega = \pi/2$, and $2/3$ at $\omega = \pi$: the sequence is a low-pass signal. Its length 4 DFT is not the DFT of its first four terms, but the DFT of the folded block $\tilde x[j] = \frac{16}{15} 2^{-j}$, $j = 0, \ldots, 3$, and that DFT gives exactly $2$, $0.8 - 0.4i$, $2/3$ and $0.8 + 0.4i$.

**The ideal low-pass filter: in $\ell^2$, not in $\ell^1$.** For $0 < \omega_c < \pi$, the sequence $h[n] = \sin(\omega_c n)/(\pi n)$ for $n \ne 0$ and $h[0] = \omega_c/\pi$ is the inverse DTFT of the indicator of $|\omega| < \omega_c$. It decays only like $1/|n|$, so $\sum_n |h[n]|$ diverges while $\sum_n |h[n]|^2 = \omega_c/\pi$ is finite. Its DTFT exists only in the mean-square sense. The partial sums $H_N$ do not converge uniformly: near the jumps at $\pm\omega_c$ they overshoot by about $9\%$ of the jump for every $N$, which is the [Gibbs phenomenon](/gibbs-phenomenon/).

**Non-example: the constant sequence.** $x[n] = 1$ for all $n$ is in neither $\ell^1$ nor $\ell^2$, and $\sum_n e^{-i\omega n}$ diverges at every $\omega$, since its terms do not tend to zero. It has a DTFT only as a generalized function, $2\pi \sum_k \delta(\omega - 2\pi k)$, which is outside the definition above. The same holds for the unit step and for a pure sinusoid $e^{i\omega_0 n}$, whose generalized transform is a train of impulses at $\omega_0 + 2\pi k$.

**Non-example: growing sequences.** $x[n] = 2^n$ for $n \ge 0$ has no DTFT in any sense, because its terms grow. Its [z-transform](/z-transform/) $1/(1 - 2z^{-1})$ exists for $|z| > 2$, a region of convergence that does not contain the unit circle.

## Related definitions

- **The DFT.** The [discrete Fourier transform](/discrete-fourier-transform/) maps $N$ numbers to $N$ numbers. It equals the DTFT at $\omega_k = 2\pi k/N$ of the block extended by zeros, as shown above. The [FFT](/fast-fourier-transform/) computes it, and hence many DTFT samples at once.
- **The z-transform.** $X(z) = \sum_n x[n] z^{-n}$. When its region of convergence contains the unit circle, the DTFT is its restriction to $z = e^{i\omega}$; this is where the notation $X(e^{i\omega})$ comes from.
- **Fourier series.** The DTFT is a Fourier series in the variable $\omega$, with the sequence as its coefficients. So the theorems on Fourier series apply with time and frequency exchanged: [Parseval's theorem](/parsevals-theorem/), the Gibbs phenomenon at a jump of $X$, and the Fejér means.
- **The Fourier transform of a sampled signal.** If $x[n] = x_c(nT)$, the DTFT is the sum of the shifted copies of the spectrum of $x_c$, scaled by $f_s$. The overlap of the copies is [aliasing](/aliasing/), and the [sampling theorem](/sampling-theorem/) gives the condition under which they do not overlap.
- **The frequency response.** For an LTI system with impulse response $h$, the DTFT $H(e^{i\omega})$ is its [frequency response](/frequency-response/).
- **Short-time transforms.** The [short-time Fourier transform](/short-time-fourier-transform/) takes the DTFT of the signal times a sliding [window](/window-functions/), so that the spectrum can change with time.
- **The finite periodic case.** For an $N$-periodic sequence the DTFT is a train of impulses, and the DFT coefficients are its weights; [trigonometric interpolation](/trigonometric-interpolation/) uses these coefficients to fill in between the samples.

## References
