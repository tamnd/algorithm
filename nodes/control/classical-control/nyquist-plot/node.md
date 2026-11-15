---
tag: F0QPT3
kind: definition
slug: nyquist-plot
name: Nyquist plot
aliases:
- Nyquist diagram
area: control/classical-control
level: intro
summary: "The closed curve that L(s) draws in the complex plane while s goes once clockwise around the right half plane. Its encirclements of -1 and its distance to -1 measure the loop."
prereqs: [frequency-response, bode-plot]
see_also: [nyquist-stability-criterion, gain-margin, phase-margin, sensitivity-function, nichols-chart, circle-criterion, describing-function, point-in-polygon]
sources:
  - paper: doi:10.1002/j.1538-7305.1932.tb02344.x
    title: Harry Nyquist, Regeneration Theory, Bell System Technical Journal 11(1), 1932
    locator: pp. 126 to 147 (the locus of the loop gain in the complex plane and the rule for when it encloses the critical point)
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Section 10.2, The Nyquist Criterion (the Nyquist contour, the Nyquist plot and the indentation at poles on the imaginary axis)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 6.3, The Nyquist Stability Criterion
  - book: isbn:9780136156734
    title: Katsuhiko Ogata, Modern Control Engineering, fifth edition, Prentice Hall, 2010
    locator: Section 7-3, Polar Plots, and Section 7-5, Nyquist Stability Criterion
---

The Nyquist plot of a loop transfer function $L(s)$ is the closed curve that $L(s)$ draws in the complex plane while $s$ goes once clockwise around the Nyquist contour: up the imaginary axis from $-jR$ to $jR$, then back along a half circle of radius $R$ in the right half plane, with $R \to \infty$. The part for $s = j\omega$ with $\omega \ge 0$ is the polar plot of the [frequency response](/frequency-response/) $L(j\omega)$; the part for $\omega < 0$ is its mirror image in the real axis. Harry Nyquist introduced the curve in 1932 to decide when a feedback amplifier oscillates. The [Nyquist stability criterion](/nyquist-stability-criterion/) counts how often the curve goes around the point $-1$, and the distance from the curve to $-1$ measures how robust the loop is.

## Definition

**Notation.** The loop is the negative feedback loop of the [feedback control loop](/feedback-control-loop/) page, with error $e = r - y$, loop transfer function $L = PC$ and [sensitivity function](/sensitivity-function/) $S = 1/(1 + L)$. $L$ is real rational and proper. Frequencies are in rad/s, and $-1$ is the critical point.

**The Nyquist contour.** For a large $R$ and a small $\varepsilon > 0$, the contour $D$ is the closed path made of:

1. the imaginary axis $s = j\omega$, from $\omega = -R$ up to $\omega = R$;
2. the half circle $s = Re^{j\theta}$, with $\theta$ going from 90 degrees down to $-90$ degrees.

Together these go once clockwise around the part of the open right half plane inside the radius $R$. If $L$ has a pole on the imaginary axis at $j\omega_0$, for example an integrator at $s = 0$, the contour goes around it on a small half circle $s = j\omega_0 + \varepsilon e^{j\theta}$, $\theta$ from $-90$ to $90$ degrees. The detour goes into the right half plane, so the pole is left outside the contour, on the same side as the poles in the left half plane.

**Definition.** The Nyquist plot of $L$ is the image $L(D)$ of the contour, with its direction, in the limit $R \to \infty$ and $\varepsilon \to 0$. Three facts make it easy to draw:

- $L$ has real coefficients, so $L(-j\omega) = \overline{L(j\omega)}$. The curve for $\omega < 0$ is the mirror image of the polar plot in the real axis.
- On the big half circle, $L(s) \to L(\infty)$, a single point. It is 0 if $L$ is strictly proper.
- Near a pole of order $k$ at $j\omega_0$, $L \approx c/(s - j\omega_0)^k$. The small detour maps to an arc of radius $|c|/\varepsilon^k$ that turns clockwise through $180k$ degrees.

**Distance to $-1$.** For $s = j\omega$, the distance from $L(j\omega)$ to $-1$ is $|1 + L(j\omega)| = 1/|S(j\omega)|$. So the smallest distance from the curve to $-1$ is $1/M_s$, where $M_s = \max_\omega |S(j\omega)|$ is the peak sensitivity. A loop with $M_s = 2$ comes within 0.5 of the critical point.

## Examples and non-examples

**The check loop.** Take $L(s) = 1/(s(s + 1)(s + 2))$. The denominator at $s = j\omega$ is $-3\omega^2 + j\omega(2 - \omega^2)$, so

$$L(j\omega) = \frac{-3\omega^2 - j\omega(2 - \omega^2)}{9\omega^4 + \omega^2(2 - \omega^2)^2}, \qquad \operatorname{Re} L(j\omega) = \frac{-3}{9\omega^2 + (2 - \omega^2)^2}.$$

You can check three facts by hand from this formula. As $\omega \to 0^+$, the real part tends to $-3/4$ and the imaginary part to $-\infty$: the curve comes up from far below, along the line $\operatorname{Re} L = -0.75$. The imaginary part is zero at $\omega = \sqrt 2$, where $L = -3/18 = -1/6$: this is the crossing of the negative real axis. As $\omega \to \infty$, the phase tends to $-270$ degrees, so the curve ends at 0, coming from above along the positive imaginary axis.

| $\omega$ (rad/s) | $\operatorname{Re} L$ | $\operatorname{Im} L$ | distance to $-1$ |
|---|---|---|---|
| 0.1 | -0.7407 | -4.9135 | 4.9203 |
| 0.44575 | -0.5961 | -0.8029 | 0.8988 |
| 0.72631 | -0.4338 | -0.2931 | 0.6376 |
| 1 | -0.3 | -0.1 | 0.7071 |
| 1.41421 | -0.1667 | 0 | 0.8333 |
| 2 | -0.075 | 0.025 | 0.9253 |

The integrator gives the detour $s = \varepsilon e^{j\theta}$, on which $L \approx 1/(2s) = e^{-j\theta}/(2\varepsilon)$. As $\theta$ goes from $-90$ to $90$ degrees, this is a half circle of radius $1/(2\varepsilon)$ that goes clockwise from the top, through the far right, to the bottom. It joins the end of the mirror curve at $\omega = 0^-$ to the start of the polar plot at $\omega = 0^+$. The closed curve does not go around $-1$, because it crosses the negative real axis only at $-1/6$, to the right of $-1$. The closest point to $-1$ is at $\omega = 0.72631$, at the distance $1/M_s = 0.63760$ with $M_s = 1.56838$.

For the gain $10L$, the crossing moves to $-10/6 = -1.667$, to the left of $-1$, and the curve now goes twice clockwise around $-1$. The closed-loop polynomial $s^3 + 3s^2 + 2s + 10$ has the roots $-3.30891$ and $0.15445 \pm 1.73156j$, two in the right half plane, as the criterion predicts.

**Not a Nyquist plot.** The polar plot alone, for $\omega \ge 0$, is half of the curve. It is enough to read the margins, but not enough to count encirclements when $L$ has poles on the imaginary axis or in the right half plane, because the closing arcs carry part of the turning. A plot of $S(j\omega)$ or $T(j\omega)$ in the complex plane is a different curve, and the point $-1$ has no special meaning for it. A contour that goes counterclockwise, or that detours to the left of an imaginary-axis pole, gives a valid but different count, and the criterion must then be stated with other signs.

## Related definitions

- The [Nyquist stability criterion](/nyquist-stability-criterion/) is the theorem that reads closed-loop stability from the number of encirclements of $-1$ by this curve.
- The [gain margin](/gain-margin/) is read where the curve crosses the negative real axis, and the [phase margin](/phase-margin/) where it crosses the unit circle.
- The [Bode plot](/bode-plot/) and the [Nichols chart](/nichols-chart/) show the same values $L(j\omega)$ with gain in dB and phase in degrees on separate axes.
- Counting encirclements is computing a winding number, the same count as the winding-number test for a [point in a polygon](/point-in-polygon/).
- The [circle criterion](/circle-criterion/) replaces the point $-1$ by a disk, and the [describing function](/describing-function/) method replaces it by the curve $-1/N(a)$ of a nonlinearity.

## References
