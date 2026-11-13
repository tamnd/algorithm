---
tag: 6TNVNS
kind: definition
slug: continuous-wavelet-transform
name: Continuous wavelet transform
aliases:
- CWT
area: graphics-and-signals/signal-processing
level: advanced
summary: Inner products of a signal with scaled and shifted copies of a mother wavelet.
prereqs: [time-frequency-analysis, parsevals-theorem]
see_also: [haar-wavelet, discrete-wavelet-transform, short-time-fourier-transform, time-frequency-uncertainty, analytic-signal, fast-wavelet-transform, filter-bank]
sources:
  - paper: doi:10.1137/0515056
    title: Alex Grossmann and Jean Morlet, Decomposition of Hardy functions into square integrable wavelets of constant shape, SIAM Journal on Mathematical Analysis 15(4), 1984
    locator: pages 723 to 736 (the admissibility condition and the isometry of the transform)
  - book: isbn:9780898712742
    title: Ingrid Daubechies, Ten Lectures on Wavelets, SIAM, 1992
    locator: Chapter 2 (the continuous wavelet transform, the resolution of the identity and the reproducing kernel) and Chapter 3 (wavelet frames)
  - book: isbn:9780123743701
    title: Stéphane Mallat, A Wavelet Tour of Signal Processing, The Sparse Way, third edition, Academic Press, 2009
    locator: Chapter 4 (time and frequency analysis; the wavelet transform, its admissibility condition and its reconstruction formula)
---

The continuous wavelet transform of a signal $f$ is the function $W_\psi f(a, b) = \int f(t)\, a^{-1/2}\, \overline{\psi((t - b)/a)}\, dt$ of a scale $a > 0$ and a position $b \in \mathbb R$, where $\psi$ is a fixed *mother wavelet*. Grossmann and Morlet (1984) showed that when $\psi$ is *admissible*, the map $f \mapsto W_\psi f$ preserves energy up to a constant and can be inverted. Unlike the [short-time Fourier transform](/short-time-fourier-transform/), whose window has one fixed width, the wavelet gets narrower as the scale goes down, so the transform sees short events at small scales and slow trends at large scales. It describes a function of one variable by a function of two, so it is redundant; the [discrete wavelet transform](/discrete-wavelet-transform/) keeps only dyadic samples of it and has no redundancy.

## Definition

**Setting.** Signals are complex functions in $L^2(\mathbb R)$, with $\langle f, g \rangle = \int f \bar g$. The Fourier transform is $\hat f(\omega) = \int f(t) e^{-i\omega t}\, dt$, with $\omega$ in radians per unit time, so [Plancherel's form of Parseval's theorem](/parsevals-theorem/) reads $\langle f, g \rangle = \tfrac{1}{2\pi} \langle \hat f, \hat g \rangle$.

**Wavelet.** A function $\psi \in L^2(\mathbb R)$ is *admissible* if

$$C_\psi = \int_{-\infty}^{\infty} \frac{|\hat\psi(\omega)|^2}{|\omega|}\, d\omega < \infty.$$

If also $\psi \in L^1$, then $\hat\psi$ is continuous, and admissibility forces $\hat\psi(0) = \int \psi = 0$: the wavelet has mean zero. Conversely, if $\int (1 + |t|)\,|\psi(t)|\, dt < \infty$ and $\int \psi = 0$, then $\psi$ is admissible. Proof: $t\psi \in L^1$ makes $\hat\psi$ continuously differentiable, and $\hat\psi(0) = 0$ gives $|\hat\psi(\omega)| \le c|\omega|$ for $|\omega| \le 1$, so the integrand is at most $c^2 |\omega|$ there. For $|\omega| > 1$ the integrand is at most $|\hat\psi(\omega)|^2$, which is integrable because $\psi \in L^2$.

**Atoms and transform.** For $a > 0$ and $b \in \mathbb R$ let $\psi_{a,b}(t) = a^{-1/2} \psi\big(\tfrac{t - b}{a}\big)$. The factor $a^{-1/2}$ gives $\lVert \psi_{a,b} \rVert = \lVert \psi \rVert$. The continuous wavelet transform of $f$ is

$$W_\psi f(a, b) = \langle f, \psi_{a,b} \rangle = \frac{1}{2\pi} \int \hat f(\omega)\, \sqrt a\, \overline{\hat\psi(a\omega)}\, e^{i\omega b}\, d\omega.$$

The second form follows from $\hat\psi_{a,b}(\omega) = \sqrt a\, \hat\psi(a\omega) e^{-i\omega b}$. So for a fixed scale, $b \mapsto W_\psi f(a, b)$ is $f$ passed through a band-pass filter whose pass band sits near $\omega_0 / a$ if $|\hat\psi|$ peaks at $\omega_0$. Small scales mean high frequencies.

**Theorem (energy and inversion).** Let $\psi$ be admissible and assume that $|\hat\psi(-\omega)| = |\hat\psi(\omega)|$, which holds for every real $\psi$. Then for all $f, g \in L^2(\mathbb R)$,

$$\int_0^\infty \int_{-\infty}^{\infty} W_\psi f(a, b)\, \overline{W_\psi g(a, b)}\, db\, \frac{da}{a^2} = \frac{C_\psi}{2} \langle f, g \rangle,$$

and $f = \tfrac{2}{C_\psi} \int_0^\infty \int W_\psi f(a, b)\, \psi_{a,b}\, db\, \tfrac{da}{a^2}$, with the integral taken in the weak sense.

*Proof.* For fixed $a$, the Fourier transform in $b$ of $W_\psi f(a, \cdot)$ is $\sqrt a\, \hat f(\omega) \overline{\hat\psi(a\omega)}$. Plancherel in $b$ gives $\int W_\psi f\, \overline{W_\psi g}\, db = \tfrac{1}{2\pi} \int a\, \hat f(\omega) \overline{\hat g(\omega)}\, |\hat\psi(a\omega)|^2\, d\omega$. Divide by $a^2$, integrate over $a$, and swap the integrals (Fubini, applied first with $f = g$, where everything is nonnegative). For $\omega \ne 0$ the substitution $u = a|\omega|$ gives $\int_0^\infty |\hat\psi(a\omega)|^2\, \tfrac{da}{a} = \int_0^\infty |\hat\psi(\pm u)|^2\, \tfrac{du}{u} = \tfrac{C_\psi}{2}$, by the symmetry of $|\hat\psi|$. What is left is $\tfrac{C_\psi}{2} \cdot \tfrac{1}{2\pi} \langle \hat f, \hat g \rangle = \tfrac{C_\psi}{2} \langle f, g \rangle$. The inversion formula is the same identity read as $\langle f, g \rangle = \langle \tfrac{2}{C_\psi} \int\!\!\int W_\psi f\, \psi_{a,b}, g \rangle$ for every $g$. $\square$

For a complex $\psi$ with $|\hat\psi(\omega)| \ne |\hat\psi(-\omega)|$, the two half-line integrals differ, and the theorem needs either both to be equal or negative scales as well. An *analytic* wavelet, with $\hat\psi(\omega) = 0$ for $\omega < 0$, recovers only the positive-frequency part of $f$, which is the [analytic signal](/analytic-signal/) of a real $f$ up to a factor.

**Redundancy.** The image of $W_\psi$ is a proper closed subspace of $L^2(\mathbb R_{>0} \times \mathbb R, db\, da/a^2)$. A function $F(a, b)$ in the image satisfies $F(a', b') = \tfrac{2}{C_\psi} \int\!\!\int F(a, b)\, \langle \psi_{a,b}, \psi_{a',b'} \rangle\, db\, \tfrac{da}{a^2}$, so not every function of $(a, b)$ is a wavelet transform. This is why a discrete sample of the transform can still determine $f$.

## Examples and non-examples

**The Mexican hat on a Gaussian.** Let $g(t) = e^{-t^2/2}$ and $\psi = -g''$, so $\psi(t) = (1 - t^2) e^{-t^2/2}$. Then $\hat\psi(\omega) = \sqrt{2\pi}\, \omega^2 e^{-\omega^2/2}$, and

$$C_\psi = 2\pi \int_{-\infty}^{\infty} |\omega|^3 e^{-\omega^2}\, d\omega = 2\pi.$$

Take $f(t) = e^{-t^2/(2\sigma^2)}$, a bump of width $\sigma$, and let $s^2 = \sigma^2 + a^2$. Since $\psi((t - b)/a) = -a^2\, \partial_b^2\, g((t - b)/a)$, the transform is $-a^{3/2}\, \partial_b^2$ of the Gaussian integral $\int f(t) g((t - b)/a)\, dt = \sqrt{2\pi}\, \sigma a\, s^{-1} e^{-b^2/(2s^2)}$, which gives

$$W_\psi f(a, b) = \sqrt{2\pi}\, \sigma\, a^{5/2}\, \frac{s^2 - b^2}{s^5}\, e^{-b^2/(2s^2)}.$$

At the center $b = 0$, the response $\sqrt{2\pi}\, \sigma a^{5/2} (\sigma^2 + a^2)^{-3/2}$ is largest where $5(\sigma^2 + a^2) = 6a^2$, that is at the scale $a = \sqrt 5\, \sigma$. So the scale of the peak grows in proportion to the width of the bump. For $\sigma = 1$ and $a = 1$ the value is $\sqrt\pi / 2 \approx 0.8862$. The response changes sign at $|b| = s$, where the bump leaves the positive center of the hat. The energy identity also holds in closed form: $\int W_\psi f(a, b)^2\, db = \tfrac32 \pi^{3/2} \sigma^2 a^5 s^{-5}$, and $\int_0^\infty \tfrac32 \pi^{3/2} \sigma^2 a^3 (\sigma^2 + a^2)^{-5/2}\, da = \pi^{3/2} \sigma$, which is $\tfrac{C_\psi}{2} \lVert f \rVert^2 = \pi \cdot \sigma\sqrt\pi$.

**The Haar wavelet.** The [Haar wavelet](/haar-wavelet/) is admissible, with $C_\psi = 2 \ln 2$. It is real, so the theorem applies, but its jumps make $|\hat\psi(\omega)|$ decay only like $1/|\omega|$, and its transform has poor frequency resolution.

**Non-example: a Gaussian.** The Gaussian $g$ has $\hat g(0) = \sqrt{2\pi} \ne 0$, so $C_g = \infty$. Its "transform" is a family of blurred copies of $f$. At small scales it is close to $\sqrt{2\pi a}\, f(b)$, so $\int |W_g f(a, b)|^2\, db \approx 2\pi a \lVert f \rVert^2$, and the energy integral with the weight $da/a^2$ diverges at $a = 0$ for every nonzero $f$.

**Non-example: the plain Morlet wavelet.** The function $e^{i\omega_0 t} e^{-t^2/2}$ has Fourier transform $\sqrt{2\pi}\, e^{-(\omega - \omega_0)^2/2}$, which is $\sqrt{2\pi}\, e^{-\omega_0^2/2} \ne 0$ at $\omega = 0$, so it is not admissible for any $\omega_0$. For $\omega_0 = 5$ this value is about $9.3 \times 10^{-6}$, so in practice the defect is small. Subtracting $e^{-\omega_0^2/2} e^{-t^2/2}$ gives a function with mean zero, which is admissible.

## Related definitions

- **[Short-time Fourier transform](/short-time-fourier-transform/).** It uses the atoms $w(t - b) e^{i\omega t}$, all with the same width. The wavelet atom $\psi_{a,b}$ has time spread $a\sigma_t$ and frequency spread $\sigma_\omega / a$, so the product is the same at every scale, and the [uncertainty principle](/time-frequency-uncertainty/) bounds it below in both cases.
- **[Discrete wavelet transform](/discrete-wavelet-transform/).** It samples the transform at $a = 2^{-j}$ and $b = k 2^{-j}$ for integers $j$ and $k$, where $W_\psi f(2^{-j}, k2^{-j}) = \langle f, \psi_{j,k} \rangle$ with $\psi_{j,k}(t) = 2^{j/2}\psi(2^j t - k)$. For special wavelets, such as the [Haar wavelet](/haar-wavelet/) and the Daubechies wavelets, the sampled atoms form an orthonormal basis, and the [fast wavelet transform](/fast-wavelet-transform/) computes all the samples in linear time.
- **Wavelet frames.** For other wavelets, the samples at $a = a_0^j$ and $b = k b_0 a_0^j$ form a frame when $a_0 > 1$ and $b_0 > 0$ are small enough; Daubechies (1992, Chapter 3) gives the conditions.
- **[Time-frequency analysis](/time-frequency-analysis/).** The squared modulus $|W_\psi f(a, b)|^2$, plotted over $b$ and $\log a$, is a time-scale picture of $f$, the wavelet counterpart of the spectrogram.
- **[Filter bank](/filter-bank/).** At a fixed scale the transform is a convolution with $\overline{\psi(-t/a)}/\sqrt a$, so a set of scales is a bank of band-pass filters whose bandwidths are proportional to their center frequencies.

## References
