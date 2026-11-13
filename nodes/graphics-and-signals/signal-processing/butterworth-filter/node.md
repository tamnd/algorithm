---
tag: VAFAXE
kind: definition
slug: butterworth-filter
name: Butterworth filter
aliases:
- maximally flat filter
area: graphics-and-signals/signal-processing
level: core
summary: "The low-pass filter of order N with |H(iΩ)|^2 = 1/(1 + (Ω/Ωc)^(2N)). Its first 2N - 1 derivatives at Ω = 0 vanish, so it is maximally flat, and its gain falls monotonically."
prereqs: [transfer-function, frequency-response]
see_also: [bilinear-transform, iir-filter, digital-filter-design, minimum-phase, chebyshev-polynomials, bibo-stability]
sources:
  - paper: "Stephen Butterworth, On the Theory of Filter Amplifiers, Experimental Wireless and the Wireless Engineer 7, October 1930, pages 536 to 541"
    locator: the filter whose response is flat as long as possible in the pass band, built from stages separated by valves
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 7.3, Discrete-Time Butterworth, Chebyshev and Elliptic Filters, and Section 7.2, Design of Discrete-Time IIR Filters from Continuous-Time Filters
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: the chapter on the design of digital filters (the analog Butterworth filter, its poles and its order)
---

A Butterworth filter of order $N$ is the analog low-pass filter whose squared magnitude is $|H(i\Omega)|^2 = 1/\big(1 + (\Omega/\Omega_c)^{2N}\big)$, where $\Omega$ is the frequency in radians per second and $\Omega_c$ is the cutoff. The gain is 1 at $\Omega = 0$, exactly $1/\sqrt2$ (half power, about $-3.01$ dB) at $\Omega_c$, and it falls monotonically after that, by about $20N$ dB per decade. Among all filters of this form, it is the one whose response is flattest at $\Omega = 0$: the first $2N - 1$ derivatives of $|H|^2$ vanish there. Stephen Butterworth described it in 1930. Its poles lie evenly on a half circle, so its [transfer function](/transfer-function/) is easy to write down, and the [bilinear transform](/bilinear-transform/) turns it into a digital [IIR filter](/iir-filter/).

## Definition

Analog frequencies on this page are $\Omega$ in radians per second, and the analog frequency response is $H(i\Omega)$. Digital frequencies are $\omega$ in radians per sample, $\omega \in [-\pi, \pi]$, used only in the digital form below.

**Magnitude.** For an order $N \ge 1$ and a cutoff $\Omega_c > 0$, the Butterworth low-pass filter is the causal, stable filter with real coefficients, no finite zeros and $H(0) = 1$ that has

$$|H(i\Omega)|^2 = \frac{1}{1 + (\Omega/\Omega_c)^{2N}}.$$

**Poles.** Write $H(s)H(-s) = 1/\big(1 + (s/(i\Omega_c))^{2N}\big)$, which equals $|H(i\Omega)|^2$ on $s = i\Omega$. Its $2N$ poles are the roots of $(s/(i\Omega_c))^{2N} = -1$. They lie on the circle $|s| = \Omega_c$ at the angles $\pi(2k + N - 1)/(2N)$ for $k = 1, \ldots, 2N$. A stable $H(s)$ takes the $N$ of them in the left half plane:

$$s_k = \Omega_c\, e^{i\pi(2k + N - 1)/(2N)}, \quad k = 1, \ldots, N, \qquad H(s) = \frac{\Omega_c^N}{\prod_{k=1}^{N} (s - s_k)}.$$

The poles of the other half are $-s_k$, the poles of $H(-s)$. The poles of $H$ come in conjugate pairs, plus the real pole $-\Omega_c$ when $N$ is odd, so the denominator has real coefficients.

**Maximal flatness.** Let $|H(i\Omega)|^2 = 1/(1 + Q(\Omega))$ with a real polynomial $Q$ of degree $2N$ and $Q(0) = 0$. This is the form of every all-pole filter of order $N$ with $H(0) = 1$. Then the derivatives of orders $1, \ldots, 2N - 1$ of $|H|^2$ at $\Omega = 0$ all vanish if and only if $Q(\Omega) = c\, \Omega^{2N}$ for some $c > 0$, that is, if and only if the filter is a Butterworth filter with $\Omega_c = c^{-1/(2N)}$.

*Proof.* Write $Q(\Omega) = \sum_{j=1}^{2N} q_j \Omega^j$. If $q_1 = \cdots = q_{2N-1} = 0$, then $1/(1 + Q) = 1 - q_{2N}\Omega^{2N} + O(\Omega^{4N})$, so the derivatives of orders 1 to $2N - 1$ vanish. Conversely, let $j$ be the smallest index with $q_j \ne 0$. Then $1/(1 + Q) = 1 - q_j \Omega^j + O(\Omega^{j+1})$, so the derivative of order $j$ is $-j!\, q_j \ne 0$. If the derivatives up to order $2N - 1$ vanish, then $j \ge 2N$, so $Q = q_{2N}\Omega^{2N}$. The gain must stay finite for all $\Omega$, so $q_{2N} > 0$. $\square$

**Monotone gain.** For $\Omega \ge 0$ the function $1 + (\Omega/\Omega_c)^{2N}$ increases, so the gain decreases. It has no ripple in either band. For $\Omega \gg \Omega_c$ the gain is about $(\Omega_c/\Omega)^N$, a fall of $20N$ dB per decade, or about $6.02N$ dB per octave.

**Order from a specification.** Ask for an attenuation of at most $A_p$ dB at the pass band edge $\Omega_p$ and at least $A_s$ dB at the stop band edge $\Omega_s > \Omega_p$. The attenuation at $\Omega$ is $10\log_{10}\big(1 + (\Omega/\Omega_c)^{2N}\big)$ dB. Both conditions hold for some $\Omega_c$ if and only if

$$N \ge \frac{\log\big((10^{A_s/10} - 1)/(10^{A_p/10} - 1)\big)}{2 \log(\Omega_s/\Omega_p)},$$

so the smallest order is the ceiling of the right side. Then $\Omega_c = \Omega_p / (10^{A_p/10} - 1)^{1/(2N)}$ meets the pass band exactly and the stop band with some margin.

**Digital form.** The [bilinear transform](/bilinear-transform/) with the prewarped cutoff $\Omega_c = (2/T)\tan(\omega_c/2)$ gives a digital filter with

$$|H(e^{i\omega})|^2 = \frac{1}{1 + \big(\tan(\omega/2)/\tan(\omega_c/2)\big)^{2N}},$$

with half power at $\omega_c$ and $N$ zeros at $z = -1$, so $H(e^{i\pi}) = 0$. It is still maximally flat at $\omega = 0$ and monotone. It is causal and stable, and it does not have linear phase.

## Examples and non-examples

**Low orders.** With $\Omega_c = 1$ the denominators $D_N(s) = \prod_k (s - s_k)$ are

| $N$ | $D_N(s)$ |
|---|---|
| 1 | $s + 1$ |
| 2 | $s^2 + \sqrt2\, s + 1$ |
| 3 | $s^3 + 2s^2 + 2s + 1 = (s + 1)(s^2 + s + 1)$ |
| 4 | $s^4 + 2.6131 s^3 + 3.4142 s^2 + 2.6131 s + 1$ |

For $N = 3$, $|D_3(i\Omega)|^2 = (1 - 2\Omega^2)^2 + (2\Omega - \Omega^3)^2 = 1 + \Omega^6$ exactly: the terms in $\Omega^2$ and $\Omega^4$ cancel. So $|H|^2 = 1 - \Omega^6 + \Omega^{12} - \cdots$, and its derivatives of orders 1 to 5 at 0 are zero.

**An order from a specification.** Take $\Omega_p = 1$ rad/s, $\Omega_s = 2$ rad/s, $A_p = 1$ dB and $A_s = 40$ dB. The ratio is $(10^4 - 1)/(10^{0.1} - 1) \approx 38617.3$, and $\log(38617.3)/(2\log 2) \approx 7.618$, so $N = 8$. The cutoff $\Omega_c = 1/(10^{0.1} - 1)^{1/16} \approx 1.0881$ rad/s gives exactly 1 dB at $\Omega_p$ and about 42.30 dB at $\Omega_s$. Order 7 with its own best cutoff gives only about 36.28 dB at $\Omega_s$.

**A digital filter.** For $N = 2$ and $\omega_c = \pi/2$, the bilinear transform gives

$$H(z) = \frac{(1 - 1/\sqrt2)(1 + 2z^{-1} + z^{-2})}{1 + (3 - 2\sqrt2)\, z^{-2}} \approx \frac{0.29289 + 0.58579 z^{-1} + 0.29289 z^{-2}}{1 + 0.17157 z^{-2}}.$$

Here $H(1) = 1$, $|H(e^{i\pi/2})|^2 = 1/2$ and $H(-1) = 0$.

**Non-example: a second-order filter that is not flat.** The filter $1/(s^2 + s + 1)$ also has $H(0) = 1$ and order 2. But $|D(i\Omega)|^2 = 1 - \Omega^2 + \Omega^4$, so $|H|^2 = 1 + \Omega^2 + O(\Omega^4)$, whose second derivative at 0 is 2, not 0. The gain rises to a peak of $4/3$ in $|H|^2$ at $\Omega = 1/\sqrt2$ before it falls. The Butterworth filter of order 2 needs the damping term $\sqrt2\, s$ to cancel the $\Omega^2$ term.

**Non-example: Chebyshev and elliptic filters.** They allow ripple in the pass band, the stop band or both. So they are not maximally flat, but they reach a given specification with a lower order.

## Related definitions

- **Chebyshev filters (type I and II).** Replace $(\Omega/\Omega_c)^{2N}$ by $\varepsilon^2 T_N(\Omega/\Omega_p)^2$ with the [Chebyshev polynomial](/chebyshev-polynomials/) $T_N$, which gives equal ripple in the pass band (type I), or put the ripple in the stop band (type II).
- **Elliptic filters.** Equal ripple in both bands. For a given order they have the narrowest transition band of the classical families.
- **Bessel filters.** Maximally flat group delay at $\Omega = 0$ instead of a maximally flat magnitude.
- **The digital design route.** A Butterworth prototype, prewarping and the [bilinear transform](/bilinear-transform/) give a digital [IIR filter](/iir-filter/). This is one of the methods of [digital filter design](/digital-filter-design/).
- **Minimum phase.** All poles are in the left half plane and there are no finite zeros, so the analog Butterworth filter is [minimum phase](/minimum-phase/). Its digital form has all its zeros at $z = -1$, on the unit circle.

## References
