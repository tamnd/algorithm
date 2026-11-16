---
tag: YKXSQC
kind: definition
slug: phase-margin
name: Phase margin
aliases:
- phase margin of a feedback loop
area: control/classical-control
level: intro
summary: "The extra phase lag 180 + arg L(j omega_c) degrees that the loop can take at the gain crossover before the closed loop loses asymptotic stability. With several crossovers, the smallest counts."
prereqs: [nyquist-stability-criterion, bode-plot]
see_also: [gain-margin, nyquist-plot, sensitivity-function, second-order-system, time-delay-system, lead-lag-compensator, loop-shaping, lqr-stability-margins]
sources:
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Section 10.3, Stability Margins (the phase margin, the stability margin s_m = 1/M_s, and the bound of the phase margin in terms of s_m)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 6.4, Stability Margins (the phase margin and its relation to the damping ratio), and Section 6.8, Time Delay
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Section 2.4.3, Frequency domain performance (gain and phase margins, and the maximum peak criteria)
---

The phase margin of a feedback loop is the extra phase lag that the loop can take at its gain crossover frequency before the closed loop loses asymptotic stability. For a loop transfer function $L$ whose closed loop is asymptotically stable, the gain crossover frequency $\omega_c$ is where $|L(j\omega_c)| = 1$ (0 dB), and the phase margin is $\varphi_m = 180 + \arg L(j\omega_c)$ degrees. On the [Nyquist plot](/nyquist-plot/) it is the angle between the negative real axis and the point where the curve crosses the unit circle. If there are several gain crossovers, the margin is the smallest of the values. Common targets are 30 to 60 degrees, but like the [gain margin](/gain-margin/) it is a heuristic, and the peak sensitivity $M_s$ is the better single number.

## Definition

**Notation.** The loop is the negative feedback loop of the [feedback control loop](/feedback-control-loop/) page with loop transfer function $L = PC$, real rational and proper, and the closed loop is asymptotically stable. The critical point is $-1$. Phase is in degrees here and in radians inside the formulas with $\tan$ and $\sin$.

**Gain crossover.** A gain crossover frequency is an $\omega_c > 0$ with $|L(j\omega_c)| = 1$. On the [Bode plot](/bode-plot/) it is where the gain curve crosses 0 dB. On the Nyquist plot it is where the curve crosses the unit circle.

**Definition.** At each gain crossover $\omega_i$, the phase margin is $\varphi_i = 180 + \arg L(j\omega_i)$, with the argument taken so that $\varphi_i$ lies in $(-180, 180]$ degrees. The phase margin of the loop is $\varphi_m = \min_i \varphi_i$. If $L$ is multiplied by the pure phase shift $e^{-j\varphi}$, then $e^{-j\varphi}L(j\omega_i) = -1$ when $\varphi = \varphi_i$, so $\varphi_m$ is the smallest phase lag, applied at all frequencies, that puts a closed-loop pole on the imaginary axis. A negative phase margin on a loop with no unstable poles and a single gain crossover means that the closed loop is unstable; with several crossovers the [Nyquist stability criterion](/nyquist-stability-criterion/) decides.

**Delay margin.** A real phase lag usually grows with frequency. A [time delay](/time-delay-system/) $\tau$ adds the lag $\omega\tau$ radians at $\omega$, and the loop $e^{-s\tau}L$ first reaches $-1$ when $\omega_i\tau = \varphi_i$ (in radians) at some crossover. So the delay margin is $\tau_m = \min_i \varphi_i/\omega_i$. It can come from a crossover that does not give the smallest $\varphi_i$, because a high crossover frequency makes a small delay costly.

**The bound from the peak sensitivity.** At a gain crossover, $L(j\omega_c)$ is on the unit circle at the angle $\varphi_m$ from $-1$, so the chord gives $|1 + L(j\omega_c)| = 2\sin(\varphi_m/2)$. The Nyquist plot stays at a distance at least $1/M_s$ from $-1$, where $M_s$ is the peak of the [sensitivity function](/sensitivity-function/). Hence

$$\varphi_m \ge 2\arcsin\frac{1}{2M_s}.$$

| $M_s$ | 1.2 | 1.4 | 1.6 | 2.0 |
|---|---|---|---|---|
| phase margin at least (degrees) | 49.25 | 41.85 | 36.42 | 28.96 |
| gain margin at least | 6.0 | 3.5 | 2.667 | 2.0 |

The converse is false: a large phase margin does not bound $M_s$.

**Relation with damping.** For $L(s) = \omega_n^2/(s(s + 2\zeta\omega_n))$, the closed loop is the [second-order system](/second-order-system/) with damping ratio $\zeta$. Setting $|L(j\omega)| = 1$ gives $(\omega_c/\omega_n)^2 = \sqrt{1 + 4\zeta^4} - 2\zeta^2$, and the phase $-90 - \arctan(\omega_c/(2\zeta\omega_n))$ degrees gives

$$\varphi_m = \arctan\frac{2\zeta}{\sqrt{\sqrt{1 + 4\zeta^4} - 2\zeta^2}}.$$

| $\zeta$ | 0.2 | 0.4 | 0.5 | 0.6 | 0.7 |
|---|---|---|---|---|---|
| $\varphi_m$ (degrees) | 22.60 | 43.12 | 51.83 | 59.19 | 65.16 |

So the rule of thumb $\varphi_m \approx 100\zeta$ degrees holds well up to $\zeta = 0.6$, for this loop. For other loops it is only a guide to the overshoot.

## Examples and non-examples

**The check loop.** For $L(s) = 1/(s(s + 1)(s + 2))$, $|L(j\omega)| = 1$ means $\omega\sqrt{1 + \omega^2}\sqrt{4 + \omega^2} = 1$. At $\omega = 0.44575$, $\omega^2 = 0.19869$ and $0.44575 \cdot \sqrt{1.19869 \cdot 4.19869} = 1.0000$, so $\omega_c = 0.44575$. The phase there is $-90 - \arctan(0.44575) - \arctan(0.44575/2) = -90 - 24.03 - 12.57 = -126.59$ degrees, and the phase margin is $53.41$ degrees. The delay margin is $0.93218/0.44575 = 2.0913$ s. The peak sensitivity is $M_s = 1.56838$, which by the bound above guarantees only 37.18 degrees.

**A second-order loop.** For $L(s) = 1/(s(s + 1))$, $\omega_n = 1$ and $\zeta = 0.5$. The crossover is at $\omega_c^2 = \sqrt{1.25} - 0.5$, so $\omega_c = 0.78615$, and $\varphi_m = 90 - \arctan(0.78615) = 51.83$ degrees, the value of the table.

**An unstable loop.** For $L(s) = 4/((s - 1)(s + 2))$, the [Nyquist stability criterion](/nyquist-stability-criterion/) shows that the closed loop $s^2 + s + 2$ is asymptotically stable. The gain crossover is at $\omega_c = 1.33117$ and the phase margin is 19.44 degrees. The peak sensitivity is $M_s = 3$, at $\omega = \sqrt 2$, where $|S| = |-4 + j\sqrt 2|/|j\sqrt 2| = \sqrt{18}/\sqrt 2 = 3$. Here the phase margin alone does not show that the loop is asymptotically stable; that comes from the encirclement count.

**A negative margin.** For $10/(s(s + 1)(s + 2))$ the phase margin is $-13.0$ degrees, and the closed loop has the poles $0.15445 \pm 1.73156j$ in the right half plane.

**A large margin that says little.** The loop $L(s) = 0.38(s^2 + 0.1s + 0.55)/(s(s + 1)(s^2 + 0.06s + 0.5))$, from the section on stability margins in Åström and Murray, has its gain crossover at $\omega_c = 0.40578$ with a phase margin of 69.77 degrees, and no phase crossover at all. Yet its peak sensitivity is $M_s = 3.69101$ at $\omega = 0.7145$: the Nyquist plot passes within $0.27093$ of $-1$, at a frequency where neither margin is read.

## Related definitions

- The [gain margin](/gain-margin/) is read where the phase is $-180$ degrees. The two margins give two points of the Nyquist plot; $1/M_s$ gives the closest point.
- A [lead-lag compensator](/lead-lag-compensator/) is the classical way to raise the phase margin at a chosen crossover.
- [Loop shaping](/loop-shaping/) chooses the crossover frequency and the slope of $|L|$ there, and the [Bode gain-phase relation](/bode-gain-phase-relation/) ties that slope to the phase margin.
- The continuous-time LQR loop has a phase margin of at least 60 degrees per channel; see [LQR stability margins](/lqr-stability-margins/).

## References
