---
tag: EEHH4A
kind: definition
slug: nichols-chart
name: Nichols chart
aliases:
- Nichols plot
area: control/classical-control
level: core
summary: "A plot of the open-loop gain in dB against the open-loop phase in degrees, on a grid of contours of constant closed-loop gain and phase of T = L/(1 + L). Used to read margins and shape loops."
prereqs: [bode-plot, gain-margin, phase-margin]
see_also: [nyquist-plot, complementary-sensitivity-function, sensitivity-function, loop-shaping, lead-lag-compensator, second-order-system, nyquist-stability-criterion]
sources:
  - book: "Hubert M. James, Nathaniel B. Nichols and Ralph S. Phillips (editors), Theory of Servomechanisms, MIT Radiation Laboratory Series, volume 25, McGraw-Hill, 1947"
    locator: Chapter 4, General Design Principles for Servomechanisms, by Nichols with Manger and Krohn (the plot of the loop gain in decibels against phase, with loci of constant closed-loop gain)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 6.9.1, Nichols Chart
  - book: isbn:9780136156734
    title: Katsuhiko Ogata, Modern Control Engineering, fifth edition, Prentice Hall, 2010
    locator: Section 7-4, Log-Magnitude-versus-Phase Plots, and Section 7-8, on the closed-loop frequency response and the Nichols chart
---

A Nichols chart is a plot of the open-loop gain $20\log_{10}|L(j\omega)|$ in dB against the open-loop phase $\arg L(j\omega)$ in degrees, with the frequency $\omega$ as a parameter along the curve, drawn on a fixed grid of contours of constant closed-loop gain and phase of $T = L/(1 + L)$. One curve then shows the [gain margin](/gain-margin/), the [phase margin](/phase-margin/), the closed-loop resonant peak and the closed-loop bandwidth. A change of the loop gain moves the curve up or down without a change of shape, and a pure phase shift moves it left or right, which makes the chart a good sheet for loop shaping by hand. Nathaniel Nichols and his co-workers introduced it in the 1947 Radiation Laboratory volume Theory of Servomechanisms.

## Definition

**Notation.** The loop is the negative feedback loop of the [feedback control loop](/feedback-control-loop/) page with unity feedback, loop transfer function $L = PC$, and [complementary sensitivity function](/complementary-sensitivity-function/) $T = L/(1 + L)$, the transfer function from the reference $r$ to the output $y$. Phase is in degrees and gain in dB.

**The Nichols plot.** The Nichols plot of $L$ is the curve

$$\omega \mapsto \big(\arg L(j\omega),\ 20\log_{10}|L(j\omega)|\big), \qquad \omega > 0,$$

with phase on the horizontal axis and gain on the vertical axis. The phase is the continuous branch, as on the [Bode plot](/bode-plot/). The curve carries the same data as the two Bode curves, with the frequency moved from an axis to marks along the curve.

**The grid.** A point $(\varphi, g)$ of the plane stands for the complex number $L = 10^{g/20}e^{j\varphi}$. The M-contours are the level sets of $20\log_{10}|L/(1 + L)|$, and the N-contours are the level sets of $\arg(L/(1 + L))$. The grid repeats every 360 degrees of phase and is symmetric about the line $\varphi = -180$ degrees. All N-contours pass through the critical point $(-180, 0\ \text{dB})$, which stands for $L = -1$. The M-contours for $|T| > 1$ are closed curves around it, and they shrink to it as $|T| \to \infty$.

A few contours can be found by hand. $|T| = 1$ means $|L| = |1 + L|$, that is, $\operatorname{Re} L = -1/2$, so the 0 dB M-contour is $|L| = -1/(2\cos\varphi)$ for $-270 < \varphi < -90$ degrees. On the line $\varphi = -180$, where $L = -a$ with $a > 0$, $|T| = a/|1 - a|$, so the contour $|T| = M$ passes through $a = M/(1 + M)$ below the critical point and, for $M > 1$, through $a = M/(M - 1)$ above it.

| $\lvert T\rvert$ contour | 0 dB | 1 dB | 3 dB | 6 dB |
|---|---|---|---|---|
| open-loop gain below the critical point, at $-180$ degrees | -6.02 dB | -5.54 dB | -4.65 dB | -3.53 dB |

**Reading the chart.**

- The gain margin is the distance in dB from the critical point down to where the curve crosses the line $\varphi = -180$ degrees.
- The phase margin is the distance in degrees from the critical point to the right, to where the curve crosses the 0 dB line.
- The closed-loop resonant peak $M_t = \max_\omega |T(j\omega)|$ is the value of the highest M-contour that the curve touches.
- The closed-loop bandwidth is the frequency where the curve crosses the $-3$ dB M-contour.
- The [sensitivity function](/sensitivity-function/) is not on the standard grid, but $S(L) = T(1/L)$, and $1/L$ is the point reflection of $(\varphi, g)$ through the critical point. So the contours of $|S|$ are the M-contours reflected through the critical point.

## Examples and non-examples

**The check loop.** For $L(s) = 1/(s(s + 1)(s + 2))$, the Bode values give these points of the Nichols plot:

| $\omega$ (rad/s) | phase (degrees) | gain (dB) |
|---|---|---|
| 0.1 | -98.57 | 13.925 |
| 0.2 | -107.02 | 7.745 |
| 0.44575 | -126.59 | 0 |
| 1 | -161.57 | -10.000 |
| 1.41421 | -180.00 | -15.563 |
| 2 | -198.43 | -22.041 |

The curve crosses the 0 dB line 53.41 degrees to the right of the critical point (the phase margin) and the $-180$ degree line 15.563 dB below it (the gain margin). It touches the M-contour of $|T| = 1.11293$ (0.929 dB) at $\omega = 0.43504$: the closed loop has a small resonant peak. It crosses the $-3$ dB M-contour at $\omega = 0.79609$, at the point $(-150.23, -6.81\ \text{dB})$, so the closed-loop bandwidth is about 0.8 rad/s. Multiplying $L$ by 6 moves the whole curve up by 15.563 dB, and then it passes through the critical point; the closed loop has poles at $\pm j\sqrt 2$.

You can check one closed-loop value by hand. At $\omega = 1$, $L = -0.3 - 0.1j$ and $1 + L = 0.7 - 0.1j$, so $|T| = \sqrt{0.1}/\sqrt{0.5} = \sqrt{0.2} = 0.4472$ ($-6.99$ dB). The phase of $T$ is $-161.57 - (-8.13) = -153.43$ degrees. This is the M-contour and the N-contour through the point $(-161.57, -10\ \text{dB})$.

**Not a Nichols chart.** The [Nyquist plot](/nyquist-plot/) shows the same values in the complex plane, where the M-contours are circles, but a gain change scales the curve instead of shifting it. A Bode plot of $T$ shows the closed-loop gain directly, but it hides how a change of $L$ moves it. A Nichols plot with the phase folded into $(-180, 180]$ degrees breaks the curve at $-180$ degrees, the line where the gain margin is read. The grid assumes unity feedback: with a sensor $F(s)$ in the feedback path the contours give $L/(1 + L)$ with $L = PCF$, which is the transfer function from $r$ to $Fy$, not to $y$.

**What the chart does not show.** The chart does not count encirclements of the critical point, so it does not by itself show that the closed loop is asymptotically stable; that comes from the [Nyquist stability criterion](/nyquist-stability-criterion/). A loop that is unstable by itself can have a curve that looks safe on the chart.

## Related definitions

- The Bode plot, the Nyquist plot and the Nichols chart show the same frequency response $L(j\omega)$ in three ways.
- The resonant peak $M_t$ relates to the overshoot of the step response; for the [second-order system](/second-order-system/) the relation is exact.
- [Loop shaping](/loop-shaping/) and the [lead-lag compensator](/lead-lag-compensator/) are often done on the chart, because a lead network moves the curve to the right near crossover and a gain moves it up or down.

## References
