---
tag: 18PG2D
kind: definition
slug: gain-margin
name: Gain margin
aliases:
- gain margin of a feedback loop
area: control/classical-control
level: intro
summary: "The factor 1/|L(j omega_pc)| by which the loop gain can grow before the closed loop loses asymptotic stability, read where the phase is -180 degrees. With several crossings, the smallest counts."
prereqs: [nyquist-stability-criterion, bode-plot]
see_also: [phase-margin, nyquist-plot, sensitivity-function, nichols-chart, ziegler-nichols-tuning, relay-autotuning, root-locus, lqr-stability-margins]
sources:
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Section 10.3, Stability Margins (the gain margin, the stability margin s_m = 1/M_s, and the bounds of the margins in terms of s_m)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 6.4, Stability Margins
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Section 2.4.3, Frequency domain performance (gain and phase margins, and the maximum peak criteria)
  - book: "Hendrik W. Bode, Network Analysis and Feedback Amplifier Design, Van Nostrand, 1945"
    locator: the chapters on feedback amplifier design (the margins in gain and phase that a practical amplifier needs); no chapter locator confirmed
---

The gain margin of a feedback loop is the factor by which the loop gain can be multiplied before the closed loop loses asymptotic stability. For a loop transfer function $L$ whose closed loop is asymptotically stable, it is read at a phase crossover frequency $\omega_{pc}$, where the phase of $L(j\omega)$ is $-180$ degrees: there the [Nyquist plot](/nyquist-plot/) crosses the negative real axis at $L(j\omega_{pc})$, and the gain margin is $g_m = 1/|L(j\omega_{pc})|$, or $-20\log_{10}|L(j\omega_{pc})|$ in dB. If there are several crossings, the margin is the smallest factor among them. A common target is $g_m \ge 2$ (6 dB), but the gain margin is a heuristic: a loop can have a large gain margin and still come close to $-1$ at another frequency.

## Definition

**Notation.** The loop is the negative feedback loop of the [feedback control loop](/feedback-control-loop/) page with loop transfer function $L = PC$, real rational and proper, and the closed loop is asymptotically stable. The critical point is $-1$, frequencies are in rad/s, and gains in dB are $20\log_{10}$ of the factor.

**Phase crossover.** A phase crossover frequency is an $\omega_{pc} \ge 0$ where $L(j\omega_{pc})$ is a negative real number, that is, $\arg L(j\omega_{pc}) = -180$ degrees modulo 360 degrees. On the [Bode plot](/bode-plot/) it is where the phase curve crosses $-180$, $-540$, and so on. On the Nyquist plot it is where the curve crosses the negative real axis.

**Definition.** Multiply the loop by a real gain $k > 0$. The closed loop of $kL$ has a pole on the imaginary axis exactly when $kL(j\omega) = -1$ for some $\omega$, that is, when $-1/k$ lies on the Nyquist plot of $L$. By the [Nyquist stability criterion](/nyquist-stability-criterion/), the number of unstable closed-loop poles of $kL$ changes only at these values of $k$. Let $x_1, x_2, \ldots$ be the points where the plot of $L$ crosses the negative real axis. Then:

- the upper gain margin is $k_{\max} = \min\{1/|x_i| : |x_i| < 1\}$, the smallest factor greater than 1, or $\infty$ if there is no crossing between $-1$ and 0;
- the lower gain margin is $k_{\min} = \max\{1/|x_i| : |x_i| > 1\}$, the largest factor less than 1, or 0 if there is no crossing to the left of $-1$.

The closed loop of $kL$ is asymptotically stable for all $k$ with $k_{\min} < k < k_{\max}$. "The gain margin" without a qualifier is $k_{\max}$. When the loop is unstable by itself or is conditionally stable, $k_{\min} > 0$ and both numbers must be given.

**The bound from the peak sensitivity.** Let $M_s = \max_\omega |S(j\omega)|$ be the peak of the [sensitivity function](/sensitivity-function/) $S = 1/(1 + L)$. The Nyquist plot stays at a distance at least $1/M_s$ from $-1$. A crossing $x$ between $-1$ and 0 is therefore at most $1 - 1/M_s$ in size, and

$$g_m \ge \frac{1}{1 - 1/M_s} = \frac{M_s}{M_s - 1}.$$

So $M_s = 2$ guarantees $g_m \ge 2$, and $M_s = 1.4$ guarantees $g_m \ge 3.5$. The converse is false: a large $g_m$ does not bound $M_s$. Values of $g_m$ between 2 and 5 are common targets (Åström and Murray), and $M_s$ is often asked to be between 1.2 and 2.

## Examples and non-examples

**The check loop.** For $L(s) = 1/(s(s + 1)(s + 2))$, the product $(1 + j\sqrt 2)(2 + j\sqrt 2) = 3\sqrt 2\, j$ gives $L(j\sqrt 2) = 1/(j\sqrt 2 \cdot 3\sqrt 2\, j) = -1/6$. The phase crossover is $\omega_{pc} = \sqrt 2$, and the gain margin is $g_m = 6$, or $20\log_{10}6 = 15.563$ dB. With the gain 6, the closed-loop polynomial is $s^3 + 3s^2 + 2s + 6 = (s + 3)(s^2 + 2)$: the poles $\pm j\sqrt 2$ sit on the imaginary axis at the phase crossover frequency, as the definition says. With the gain 10, the poles are $-3.30891$ and $0.15445 \pm 1.73156j$, and the closed loop is unstable. The peak sensitivity of $L$ is $M_s = 1.56838$, and the bound $M_s/(M_s - 1) = 2.7594$ is well below the true margin 6.

**Three equal poles.** For $L(s) = 3/(s + 1)^3$, the phase is $-3\arctan\omega = -180$ degrees at $\omega_{pc} = \sqrt 3$. Since $1 + j\sqrt 3 = 2e^{j\pi/3}$, $(1 + j\sqrt 3)^3 = -8$ and $L(j\sqrt 3) = -3/8$. So $g_m = 8/3 = 2.667$ (8.519 dB). The gain at which the loop of $1/(s + 1)^3$ reaches the stability limit is 8, the ultimate gain used by [Ziegler-Nichols tuning](/ziegler-nichols-tuning/).

**An unstable loop has a lower margin.** For $L(s) = 4/((s - 1)(s + 2))$, the only crossing of the negative real axis is $L(0) = -2$, at $\omega = 0$. So $k_{\max} = \infty$ and $k_{\min} = 1/2$: the closed loop $s^2 + s + (4k - 2)$ is asymptotically stable exactly for $k > 1/2$. The gain can grow without limit but can drop only by a factor of 2 (6.02 dB).

**A conditionally stable loop.** For $L(s) = 3(s + 6)^2/(s(s + 1)^2)$, the plot crosses the negative real axis at $-12$ (at $\omega = 2$) and at $-4.5$ (at $\omega = 3$). Both are to the left of $-1$, so $k_{\max} = \infty$ and $k_{\min} = \max(1/12, 1/4.5) = 0.2222$, or $-13.06$ dB. Reading only the first crossing, $1/12$, would give a false lower margin: the loop is unstable for every $k$ between $1/12$ and $2/9$.

**A large margin that says little.** The loop $L(s) = 0.38(s^2 + 0.1s + 0.55)/(s(s + 1)(s^2 + 0.06s + 0.5))$ is from the section on stability margins in Åström and Murray. Its imaginary part is negative at every $\omega > 0$, so the Nyquist plot never crosses the negative real axis and $g_m = \infty$. Its phase margin is 69.77 degrees, also large. But the lightly damped pole pair near $\omega = 0.7$ pulls the curve close to $-1$: $M_s = 3.69098$ at $\omega = 0.7145$, so the curve comes within $1/M_s = 0.27093$ of the critical point. A small change of the plant near that frequency, not a change of gain, makes this loop unstable.

## Related definitions

- The [phase margin](/phase-margin/) is the other classical margin, read where $|L(j\omega)| = 1$. Together with the gain margin it gives two points of the Nyquist plot; $1/M_s$ gives its smallest distance to $-1$.
- The [Nichols chart](/nichols-chart/) shows the gain margin as the vertical distance below the point (-180 degrees, 0 dB).
- A [root locus](/root-locus/) crosses the imaginary axis at the gain $k_{\max}$ and the frequency $\omega_{pc}$.
- [Relay autotuning](/relay-autotuning/) measures the phase crossover frequency and the gain there by an experiment, and [Ziegler-Nichols tuning](/ziegler-nichols-tuning/) uses them.
- The continuous-time LQR loop has the gain margin interval $(1/2, \infty)$ per channel; see [LQR stability margins](/lqr-stability-margins/).

## References
