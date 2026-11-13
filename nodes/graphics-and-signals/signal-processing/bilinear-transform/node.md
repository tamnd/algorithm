---
tag: CV28SZ
kind: technique
slug: bilinear-transform
name: Bilinear transform
aliases:
- Tustin transform
area: graphics-and-signals/signal-processing
level: core
summary: "Turn an analog filter H(s) into a digital one with s = (2/T)(1 - z^-1)/(1 + z^-1). Stable maps to stable, and Ω = (2/T)tan(ω/2), so prewarp the band edges."
prereqs: [transfer-function, z-transform, frequency-response]
see_also: [butterworth-filter, iir-filter, digital-filter-design, aliasing, sampling-theorem, bibo-stability, minimum-phase]
sources:
  - paper: doi:10.1049/ji-2a.1947.0020
    title: Arnold Tustin, A Method of Analysing the Behaviour of Linear Systems in Terms of Time Series, Journal of the Institution of Electrical Engineers, Part IIA 94(1), 1947
    locator: pp. 130 to 142 (the substitution of a rational function of the unit delay for the operator of differentiation)
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 7.2, Design of Discrete-Time IIR Filters from Continuous-Time Filters (impulse invariance and the bilinear transformation, with the frequency warping and prewarping), and Section 7.3 (Butterworth, Chebyshev and elliptic designs with the bilinear transformation)
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: the chapter on the design of digital filters (design of IIR filters from analog filters by the bilinear transformation)
---

The bilinear transform turns an analog filter $H_a(s)$ into a digital filter $H(z)$ by the substitution

$$s = \frac{2}{T} \cdot \frac{1 - z^{-1}}{1 + z^{-1}}, \qquad z = \frac{1 + sT/2}{1 - sT/2},$$

where $T > 0$ is a sampling interval in seconds. It maps the left half of the $s$ plane one to one onto the inside of the unit circle, so a stable analog filter gives a stable digital filter of the same order. It maps the whole imaginary axis onto the unit circle, so there is no [aliasing](/aliasing/). The price is a warping of frequency: the analog frequency $\Omega$ in radians per second lands at the digital frequency $\omega$ in radians per sample with $\Omega = (2/T)\tan(\omega/2)$. So the band edges must be prewarped before the analog design. Arnold Tustin used the substitution in control in 1947, and it is the standard way to make a digital [IIR filter](/iir-filter/) from a [Butterworth filter](/butterworth-filter/) or another analog prototype.

## In plain words

Analog filter design is old and well understood. There are tables and formulas for filters with a flat pass band, with equal ripple, and so on. The bilinear transform lets you use all of that for digital filters. You take the formula of the analog filter and replace each $s$ by a fixed expression in the delay $z^{-1}$. The result is a digital filter.

The swap keeps the good parts. A filter that is stable stays stable, and a filter of order four stays of order four. But it squeezes the whole infinite range of analog frequencies into the finite range of digital ones. Low frequencies barely move. High frequencies are pressed together near the top. So you first move your band edges to where the squeeze will put them back, and then you design.

## When it applies

- You want a digital IIR filter that meets a magnitude specification with bands that are flat or have equal ripple: low-pass, high-pass, band-pass or band-stop. The classical analog families (Butterworth, Chebyshev, elliptic) give such filters.
- You have an analog system, such as a controller or an audio circuit, and want a digital version with the same response at a few chosen frequencies.
- The response is piecewise constant, so a warping of the frequency axis does not change its shape. The transform is a poor choice when the shape of the response in frequency matters, as for a differentiator or a filter with linear phase.

Frequencies: $\Omega$ is the analog frequency in radians per second, and $\omega \in [-\pi, \pi]$ is the digital frequency in radians per sample.

## The template

1. **Specify in the digital domain.** Give the band edges $\omega_p$ and $\omega_s$ in radians per sample and the tolerances in dB.
2. **Prewarp.** Compute $\Omega_p = (2/T)\tan(\omega_p/2)$ and $\Omega_s = (2/T)\tan(\omega_s/2)$. Any $T > 0$ works, because $T$ cancels in the end. Take $T = 1$ or $T = 2$.
3. **Design the analog prototype.** Find $H_a(s) = B(s)/A(s)$ of order $N$ that meets the specification at $\Omega_p$ and $\Omega_s$. For a Butterworth filter, $N$ and $\Omega_c$ come from closed formulas.
4. **Substitute.** Replace $s$ by $(2/T)(1 - z^{-1})/(1 + z^{-1})$ and multiply numerator and denominator by $(1 + z^{-1})^N$. A term $c_j s^j$ becomes $c_j (2/T)^j (1 - z^{-1})^j (1 + z^{-1})^{N-j}$, a polynomial in $z^{-1}$ of degree $N$.
5. **Normalize.** Divide all coefficients by the constant term of the denominator, so that $a[0] = 1$. With rational input, steps 4 and 5 are exact.

Steps 4 and 5 as a procedure, for coefficient lists in ascending powers of $s$, padded to the order $N$:

```pseudo id=main
BILINEAR(b[0 .. N], a[0 .. N], T)            ▷ H_a(s) = Σ b[j] s^j / Σ a[j] s^j
L1  for each coefficient c[j] of B and of A do
L2      t ← (1 − z⁻¹)^j · (1 + z⁻¹)^(N − j)       ▷ a polynomial in z⁻¹ of degree N
L3      add c[j] · (2/T)^j · t to the new numerator or denominator
L4  α ← the constant term of the new denominator
L5  divide every new coefficient by α             ▷ now a[0] = 1
```

Equivalently, map each analog pole $p$ to the digital pole $(1 + pT/2)/(1 - pT/2)$, each finite zero the same way, and each zero at $s = \infty$ to $z = -1$, then fix the gain at one frequency.

**Why it works.** Let $w = sT/2$. Then $z = (1 + w)/(1 - w)$, and

$$|1 + w|^2 - |1 - w|^2 = 4\operatorname{Re} w.$$

So $|z| < 1$ exactly when $\operatorname{Re} s < 0$, and $|z| = 1$ exactly when $\operatorname{Re} s = 0$. The map is a Möbius map with the inverse $s = (2/T)(z - 1)/(z + 1)$, so it is one to one between the left half plane and the open unit disk. Every pole of a stable analog filter goes to a pole inside the unit circle, and the digital filter is [BIBO stable](/bibo-stability/). For $s = i\Omega$, the numerator $1 + i\Omega T/2$ and the denominator $1 - i\Omega T/2$ are conjugates, so $z = e^{i\omega}$ with $\omega = 2\arctan(\Omega T/2)$. Hence

$$H(e^{i\omega}) = H_a\big(i\, (2/T)\tan(\omega/2)\big),$$

and the digital response at $\omega$ is the analog response at $\Omega = (2/T)\tan(\omega/2)$. The values of the response are kept; only the frequency axis is bent. Near $\omega = 0$, $\Omega \approx \omega/T$, so low frequencies keep their place. As $\omega \to \pi$, $\Omega \to \infty$.

**Cost.** The substitution of step 4 costs $O(N^2)$ operations for a filter of order $N$. The digital filter has the same order $N$ and costs $\Theta(N)$ multiplies per output sample. It is causal and, when the prototype is stable, stable. It does not have linear phase.

## Classic examples

**A first-order low-pass filter.** Take $H_a(s) = 1/(s + 1)$ and $T = 1$. Then $s + 1 = (3 - z^{-1})/(1 + z^{-1})$, so

$$H(z) = \frac{1 + z^{-1}}{3 - z^{-1}} = \frac{\tfrac13 + \tfrac13 z^{-1}}{1 - \tfrac13 z^{-1}}.$$

The analog pole $-1$ goes to the digital pole $z = (1 - \tfrac12)/(1 + \tfrac12) = \tfrac13$. The zero at $s = \infty$ goes to $z = -1$, so $H(e^{i\pi}) = 0$. The analog half power frequency $\Omega = 1$ lands at $\omega = 2\arctan(\tfrac12) \approx 0.9273$ radians per sample.

**What prewarping fixes.** Suppose you want half power at $\omega_c = 0.5$ radians per sample, and with $T = 1$ you design the analog filter with $\Omega_c = 0.5$. The half power point lands at $2\arctan(0.25) \approx 0.4900$, not at 0.5. At higher frequencies the error is larger. With prewarping you design with $\Omega_c = 2\tan(0.25) \approx 0.5106$ instead, and the half power point lands exactly at 0.5.

**A digital Butterworth filter.** For order 2 and $\omega_c = \pi/2$, prewarp with $T = 1$ to $\Omega_c = 2\tan(\pi/4) = 2$. The analog filter $4/(s^2 + 2\sqrt2\, s + 4)$ becomes

$$H(z) \approx \frac{0.29289 + 0.58579 z^{-1} + 0.29289 z^{-2}}{1 + 0.17157 z^{-2}},$$

with $|H(e^{i\omega})|^2 = 1/\big(1 + \tan^4(\omega/2)\big)$. See the [Butterworth filter](/butterworth-filter/) page for the general order.

**The trapezoidal rule.** The integrator $1/s$ becomes $(T/2)(1 + z^{-1})/(1 - z^{-1})$, which is the recursion $y[n] = y[n-1] + \tfrac{T}{2}(x[n] + x[n-1])$. This is the trapezoidal rule for $y(t) = \int x$. So the bilinear transform replaces each integrator in an analog system by the trapezoidal rule. This is how Tustin used it for control systems.

## Variations

- **Prewarping at one frequency.** In control, a single frequency matters, such as the crossover frequency $\Omega_0$ of a loop. Use the constant $\Omega_0/\tan(\Omega_0 T/2)$ in place of $2/T$, so that $\Omega_0$ maps exactly to $\Omega_0 T$ radians per sample.
- **Band transformations.** Design an analog low-pass prototype, then turn it into a high-pass ($s \to \Omega_c/s$), band-pass or band-stop analog filter before the bilinear transform. Prewarp all band edges. Digital frequency transformations do the same after the transform, with all-pass substitutions for $z^{-1}$.
- **Impulse invariance.** The other classical route samples the analog impulse response: $h[n] = T h_a(nT)$. It keeps the shape of the response in frequency near $\omega = 0$ and has no warping, but the response aliases, so it is poor for high-pass and band-stop filters. See [aliasing](/aliasing/) and the [sampling theorem](/sampling-theorem/).
- **Matched z-transform.** Map each pole and zero by $z = e^{sT}$ and fix the gain. It is simple but less accurate in frequency than the bilinear transform.

## Pitfalls

- **No prewarping.** Designing at the digital frequency times $1/T$ moves every band edge down, by a small amount at low frequencies and by a large amount near $\omega = \pi$. Always prewarp the edges you specify.
- **Expecting the shape between the edges.** Only the frequencies you prewarp land exactly. A response that is not piecewise constant, such as the linear gain of a differentiator or a linear phase, is bent by $\tan(\omega/2)$.
- **Expecting linear phase.** The phase of the digital filter is the analog phase at the warped frequency. An analog filter with no linear phase gives a digital filter with no linear phase.
- **A pole at $s = 2/T$.** This point maps to $z = \infty$, and step 5 divides by zero. It does not happen for a stable prototype, whose poles have negative real part.
- **High order in one polynomial.** The digital poles of a sharp filter cluster near $z = 1$, and one polynomial of high order loses accuracy. Transform each pair of poles separately and run the filter as a cascade of second-order sections.

## Exercises

1. Show that the map $z = (1 + sT/2)/(1 - sT/2)$ sends the right half plane outside the unit circle, and the point $s = 0$ to $z = 1$.
2. Apply the transform to $H_a(s) = s/(s + 1)$ with $T = 2$. Which digital frequency has half power, and what is $H$ at $z = 1$ and at $z = -1$?
3. A first-order low-pass filter must have half power at 1 kHz for a sampling rate of 8 kHz. Give $\omega_c$ in radians per sample, the prewarped $\Omega_c$ for $T = 1/8000$ s, and the digital filter.
4. Show that the result does not depend on $T$ when you prewarp every band edge with the same $T$ that you use in the substitution.
5. Show that the bilinear transform of a Butterworth filter of order $N$ has $N$ zeros at $z = -1$.

## References
