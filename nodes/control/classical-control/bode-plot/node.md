---
tag: P9TTJ8
kind: definition
slug: bode-plot
name: Bode plot
aliases:
- Bode diagram
area: control/classical-control
level: intro
summary: "Two graphs against log frequency: the gain 20 log10 |G(j omega)| in decibels and the phase in degrees. Logs turn a product of factors into a sum of simple curves."
prereqs: [transfer-function, frequency-response, poles-and-zeros]
see_also: [nyquist-plot, nichols-chart, gain-margin, phase-margin, bode-gain-phase-relation, loop-shaping, second-order-system, minimum-phase]
sources:
  - paper: doi:10.1002/j.1538-7305.1940.tb00839.x
    title: Hendrik W. Bode, Relations Between Attenuation and Phase in Feedback Amplifier Design, Bell System Technical Journal 19(3), 1940
    locator: pp. 421 to 454 (attenuation in decibels and phase plotted against the logarithm of frequency)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 6.1, Frequency Response, and Section 6.1.1, Bode Plot Techniques
  - book: isbn:9780136156734
    title: Katsuhiko Ogata, Modern Control Engineering, fifth edition, Prentice Hall, 2010
    locator: Section 7-2, Bode Diagrams
---

A Bode plot of a transfer function $G(s)$ is a pair of graphs against the logarithm of the frequency $\omega$: the gain $20\log_{10}|G(j\omega)|$ in decibels (dB) and the phase $\arg G(j\omega)$ in degrees. The logarithm turns a product into a sum, so the plot of a product of factors is the sum of the plots of the factors, and each factor has a simple shape made of straight-line asymptotes. Hendrik Bode used these plots for feedback amplifiers in 1940. In control they are the usual way to read the loop transfer function $L(j\omega)$, its [gain margin](/gain-margin/) and [phase margin](/phase-margin/), and to do [loop shaping](/loop-shaping/).

## Definition

**Notation.** $G(s)$ is a real rational [transfer function](/transfer-function/) in the Laplace variable $s$, and $j^2 = -1$. The frequency $\omega > 0$ is in rad/s. The values $G(j\omega)$ on the imaginary axis are the continuous-time [frequency response](/frequency-response/): if $G$ is asymptotically stable, the input $\sin(\omega t)$ gives, after the transient dies out, the output $|G(j\omega)|\sin(\omega t + \arg G(j\omega))$. A decade is a factor of 10 in frequency. A factor of 10 in gain is 20 dB, and a factor of 2 is 6.02 dB.

**Definition.** The Bode plot of $G$ is the pair of curves

$$\omega \mapsto 20\log_{10}|G(j\omega)| \ \text{dB}, \qquad \omega \mapsto \arg G(j\omega) \ \text{degrees},$$

drawn on a common horizontal axis in $\log_{10}\omega$. The phase curve is the continuous branch of the argument along $\omega$. It is not folded back into $(-180, 180]$ degrees, so a loop with three poles can show a phase of $-250$ degrees. The plot is defined for any $G$ with no poles on the imaginary axis at the plotted frequencies. For a $G$ that is not asymptotically stable it is still the graph of a function, but it no longer describes a steady sinusoidal response.

**Why the logarithm.** Write $G$ in the Bode form

$$G(s) = K\, s^{\ell}\, e^{-s\tau}\, \frac{\prod_i (1 + s/z_i) \prod_k \big(1 + 2\zeta_k s/\omega_k + s^2/\omega_k^2\big)}{\prod_i (1 + s/p_i) \prod_k \big(1 + 2\zeta'_k s/\omega'_k + s^2/\omega'^2_k\big)},$$

with an integer $\ell$, a delay $\tau \ge 0$ and real first-order factors and second-order factors with complex roots. Gains in dB of the factors add, and phases add. So the plot of $G$ is the sum of the plots of the pieces below. A factor in the denominator gives the negative of the curves of the same factor in the numerator.

| Factor | Gain | Phase |
|---|---|---|
| $K > 0$ | constant $20\log_{10}K$ | 0 (and $-180$ degrees if $K < 0$) |
| $s^{\ell}$ | straight line of slope $20\ell$ dB per decade through 0 dB at $\omega = 1$ | constant $90\ell$ degrees |
| $1/(1 + s/a)$, $a > 0$ | asymptotes 0 dB below $a$ and $-20$ dB per decade above $a$; the true value at the corner $a$ is $-3.01$ dB | from 0 to $-90$ degrees, $-45$ degrees at $a$ |
| $1/(1 + 2\zeta s/\omega_n + s^2/\omega_n^2)$, $0 < \zeta < 1$ | asymptotes 0 dB and $-40$ dB per decade above $\omega_n$; the value at $\omega_n$ is $-20\log_{10}(2\zeta)$ dB | from 0 to $-180$ degrees, $-90$ degrees at $\omega_n$, with a steeper fall for small $\zeta$ |
| $1 - s/a$, $a > 0$ (a zero in the right half plane) | the same gain as $1 + s/a$ | from 0 to $-90$ degrees, a lag and not a lead |
| $e^{-s\tau}$ (a [time delay](/time-delay-system/)) | 0 dB | $-\omega\tau$ radians, which falls without bound |

For the first-order factor $1/(1 + s)$, the gain is $-0.043$ dB at $\omega = 0.1$, $-3.01$ dB at $\omega = 1$ and $-20.04$ dB at $\omega = 10$. The phase there is $-5.71$, $-45$ and $-84.29$ degrees. So the straight-line gain is off by at most 3.01 dB, at the corner. A common straight-line phase goes from 0 at $a/10$ to $-90$ degrees at $10a$, and it is off by at most 5.71 degrees.

For the second-order factor with $\zeta < 1/\sqrt 2$, the gain has a resonant peak $1/(2\zeta\sqrt{1 - \zeta^2})$ at $\omega_r = \omega_n\sqrt{1 - 2\zeta^2}$. With $\zeta = 0.1$ and $\omega_n = 1$ the peak is $5.02519$ (14.023 dB) at $\omega_r = 0.98995$, and the gain at $\omega_n$ is $1/(2\zeta) = 5$ (13.979 dB). The asymptotes miss this peak completely, so near a lightly damped pair the true curve must be computed. The [second-order system](/second-order-system/) page relates $\zeta$ to the step response.

## Examples and non-examples

**The check loop.** Take $L(s) = 1/(s(s + 1)(s + 2))$. Its Bode form is $L(s) = 0.5/\big(s(1 + s)(1 + s/2)\big)$, with corners at 1 and 2 rad/s. The gain asymptote has slope $-20$ dB per decade below 1, with the value $20\log_{10}0.5 = -6.02$ dB at $\omega = 1$. The slope is $-40$ dB per decade between 1 and 2, and $-60$ dB per decade above 2. The phase starts at $-90$ degrees and goes down to $-270$ degrees.

You can check two points by hand. At $\omega = 1$, $(1 + j)(2 + j) = 1 + 3j$ and $j(1 + 3j) = -3 + j$, so $L(j) = 1/(-3 + j) = -0.3 - 0.1j$. The gain is $20\log_{10}\sqrt{0.1} = -10$ dB, which is the asymptote value $-6.02$ dB plus the corner error $-3.01$ dB of the factor $1 + s$ and $-0.97$ dB of the factor $1 + s/2$. At $\omega = \sqrt 2$, $(1 + j\sqrt 2)(2 + j\sqrt 2) = 3\sqrt 2\, j$ and $j\sqrt 2 \cdot 3\sqrt 2\, j = -6$, so $L(j\sqrt 2) = -1/6$: the phase is exactly $-180$ degrees and the gain is $-15.563$ dB.

| $\omega$ (rad/s) | Gain (dB) | Phase (degrees) |
|---|---|---|
| 0.1 | 13.925 | -98.57 |
| 0.2 | 7.745 | -107.02 |
| 0.44575 | 0 | -126.59 |
| 1 | -10.000 | -161.57 |
| 1.41421 | -15.563 | -180.00 |
| 2 | -22.041 | -198.43 |
| 10 | -60.214 | -252.98 |

The gain curve crosses 0 dB at $\omega_c = 0.44575$, where the phase is $-126.59$ degrees, so the phase margin is $180 - 126.59 = 53.41$ degrees. The phase curve crosses $-180$ degrees at $\sqrt 2$, where the gain is $-15.563$ dB, so the gain margin is 15.563 dB, a factor of 6.

**A plot that is not a Bode plot.** A graph of $|G(j\omega)|$ on a linear frequency axis has the same data, but a product no longer becomes a sum of straight lines, and a wide band of frequencies does not fit on one page. A phase curve folded into $(-180, 180]$ degrees has false jumps of 360 degrees; for the check loop it would jump at $\sqrt 2$, which is the point where the margin is read.

**The gain does not fix the phase.** The all-pass factor $(1 - s)/(1 + s)$ has a gain of 0 dB at every frequency, but its phase is $-2\arctan\omega$, from 0 down to $-180$ degrees. So $1/(1 + s)$ and $(1 - s)/(1 + s)^2$ have the same gain curve and different phase curves. Only for a [minimum-phase](/minimum-phase/) $G$ does the gain curve fix the phase curve; this is the [Bode gain-phase relation](/bode-gain-phase-relation/).

## Related definitions

- The [Nyquist plot](/nyquist-plot/) draws the same values $G(j\omega)$ as one curve in the complex plane, with frequency as a parameter along the curve. It shows the encirclements of $-1$ that the [Nyquist stability criterion](/nyquist-stability-criterion/) counts, which a Bode plot does not show directly.
- The [Nichols chart](/nichols-chart/) plots the same gain in dB against the same phase in degrees, with frequency along the curve, on a grid of closed-loop gain contours.
- The [gain margin](/gain-margin/) and [phase margin](/phase-margin/) are read on the Bode plot of the loop $L$ at the phase crossover and the gain crossover.
- The [Bode gain-phase relation](/bode-gain-phase-relation/) says that for a stable minimum-phase $G$ the phase at a frequency is a weighted average of the slope of the gain curve, so a slope of $-20n$ dB per decade over a wide band gives a phase near $-90n$ degrees.
- A measured Bode plot comes from input and output data, for example by the [empirical transfer function estimate](/empirical-transfer-function-estimate/).
- [Loop shaping](/loop-shaping/) designs a controller by drawing the wanted Bode plot of $L$.

## References
