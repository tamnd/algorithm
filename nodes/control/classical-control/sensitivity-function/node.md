---
tag: BX9KY0
kind: definition
slug: sensitivity-function
name: Sensitivity function
aliases:
- sensitivity transfer function
area: control/classical-control
level: core
summary: S = 1/(1 + L) for the loop transfer function L. It maps an output disturbance to the output, gives the relative change of the loop per change of the plant, and its peak is 1 over the distance to -1.
history:
  year: 1945
  people: [Hendrik W. Bode]
  note: Bode's 1945 book on feedback amplifiers studied the return difference and the sensitivity of an amplifier to changes of its elements.
prereqs: [feedback-control-loop, frequency-response]
see_also: [complementary-sensitivity-function, bode-sensitivity-integral, nyquist-stability-criterion, gain-margin, phase-margin, loop-shaping, mixed-sensitivity-design, internal-model-principle]
sources:
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 10, Frequency Domain Analysis (stability margins, with the shortest distance s_m from the Nyquist curve to -1), and Chapter 12, Frequency Domain Design (the section Sensitivity Functions)
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Chapter 2, Classical Feedback Control (the closed-loop transfer functions, the peaks M_S and M_T and their bounds on the margins), and Chapter 3 for the input and output sensitivity of multivariable loops
  - book: "Hendrik W. Bode, Network Analysis and Feedback Amplifier Design, Van Nostrand, 1945"
    locator: the chapters on feedback and sensitivity (the return difference and the sensitivity of an amplifier to a change of one element)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Chapter 4, A First Analysis of Feedback (sensitivity of the closed loop to plant changes) and Chapter 6, The Frequency-Response Design Method
---

The sensitivity function of a [feedback control loop](/feedback-control-loop/) is the transfer function $S(s) = 1/(1 + L(s))$, where $L = P C$ is the loop transfer function of the plant $P$ and the controller $C$. It has three readings that are the same formula: it is the transfer function from a disturbance at the plant output to the output, it is the transfer function from the reference to the error $e = r - y$, and it is the relative change of the closed loop per relative change of the plant. Feedback helps where $|S(j\omega)| < 1$ and hurts where $|S(j\omega)| > 1$. Its largest value $M_s$ is the inverse of the distance from the Nyquist curve of $L$ to the critical point $-1$, which makes it a better single measure of robustness than the [gain margin](/gain-margin/) or the [phase margin](/phase-margin/).

## Definition

Let $P(s)$ and $C(s)$ be real rational transfer functions, with negative unity feedback, and let the loop be well posed, that is $1 + L(\infty) \ne 0$. The **sensitivity function** is

$$S(s) = \frac{1}{1 + L(s)} = \frac{1}{1 + P(s)\,C(s)}.$$

With $P = b/a$ and $C = n_c/d_c$ as ratios of coprime polynomials, $S = a\,d_c / (a\,d_c + b\,n_c)$. Its poles are among the closed-loop poles, and its zeros include the poles of $L$.

**Three readings.**

1. *Output disturbance.* If $y = P u + d_o$ and $u = C (r - y)$, then $y = T r + S d_o$, with $T = L/(1 + L)$ the [complementary sensitivity function](/complementary-sensitivity-function/).
2. *Tracking error.* With $d_o = 0$, $e = r - y = S r$.
3. *Relative sensitivity.* For the closed-loop map $T = P C/(1 + P C)$, a change $dP$ of the plant gives
$$\frac{dT}{dP} = \frac{C}{(1 + P C)^2}, \qquad \frac{dT/T}{dP/P} = \frac{dT}{dP} \cdot \frac{P}{T} = \frac{C}{(1 + PC)^2} \cdot (1 + PC) \cdot \frac{1}{C} = S.$$
So $S$ is the ratio of the relative change of the closed loop to the relative change of the plant, for small changes. Some older texts use the inverse ratio, the return difference $1 + L$, under the same name; check the convention of a source before you use its formulas.

**Peak sensitivity.** For an internally stable loop, the peak sensitivity is the [H-infinity norm](/h-infinity-norm/) of $S$,

$$M_s = \|S\|_\infty = \sup_{\omega \ge 0} |S(j\omega)| = \frac{1}{\inf_{\omega} |1 + L(j\omega)|} = \frac{1}{s_m},$$

where $s_m = \inf_\omega |L(j\omega) - (-1)|$ is the smallest distance from the Nyquist curve of $L$ to $-1$, the *stability margin* or *vector margin*. Usual designs have $M_s$ between 1.2 and 2; this is a design rule of thumb from practice (Åström and Murray; Skogestad and Postlethwaite, chapter 2), not a theorem.

**Bounds on the classical margins.** Let $M_s$ be finite. If $L(j\omega_{pc}) = -1/g_m$ at a phase crossover, the distance to $-1$ there is $|1 - 1/g_m| \ge 1/M_s$. If $|L(j\omega_c)| = 1$ at a gain crossover with phase margin $\varphi_m$, then $|1 + L(j\omega_c)| = 2 \sin(\varphi_m/2) \ge 1/M_s$. So, for $g_m > 1$,

$$g_m \ge \frac{M_s}{M_s - 1}, \qquad \varphi_m \ge 2 \arcsin \frac{1}{2 M_s}.$$

The converse fails: good gain and phase margins do not bound $M_s$, because the Nyquist curve can pass near $-1$ at a frequency that is neither crossover.

**Multivariable loops.** For a plant with $m$ inputs and $p$ outputs, the output sensitivity is $S_o = (I + P C)^{-1}$, a $p \times p$ matrix, and the input sensitivity is $S_i = (I + C P)^{-1}$, an $m \times m$ matrix. They differ when $P C \ne C P$, which is the usual case. They are related by $P S_i = S_o P$. The disturbance at the plant output sees $S_o$; a disturbance at the plant input sees $P S_i$.

## Examples and non-examples

**Example: a third-order loop.** Let $L(s) = 1/(s (s + 1)(s + 2))$. The closed loop $s^3 + 3 s^2 + 2 s + 1$ has its roots at $-2.3247$ and $-0.3376 \pm 0.5623 j$, so the loop is internally stable. Values of $|S(j\omega)|$:

| $\omega$ (rad/s) | 0.01 | 0.1 | 0.7263 | 1 | 10 |
|---|---|---|---|---|---|
| $\lvert S(j\omega) \rvert$ | 0.0200 | 0.2032 | 1.5684 (peak) | 1.4142 | 1.0003 |

At low frequency $L(s) \approx 1/(2 s)$, so $|S(j\omega)| \approx 2\omega$: a slow disturbance is reduced by a large factor. The peak is $M_s = 1.5684$ at $\omega = 0.7263$ rad/s, so the Nyquist curve passes at the distance $1/M_s = 0.6376$ from $-1$. The bounds give $g_m \ge 2.759$ and $\varphi_m \ge 37.18$ degrees. The true margins are $g_m = 6$ (15.563 dB, at $\omega = \sqrt 2$) and $\varphi_m = 53.41$ degrees (at $\omega_c = 0.44575$ rad/s), so the bounds hold and are not tight here. With $D(s) = s(s + 1)(s + 2)$, $|S|^2 = |D|^2 / |D + 1|^2$, and $|D + 1|^2 - |D|^2 = 1 + 2 \operatorname{Re} D(j\omega) = 1 - 6\omega^2$. So $|S(j\omega)| > 1$ exactly for $\omega > 1/\sqrt 6 = 0.4082$ rad/s: disturbances at those frequencies are amplified by the loop.

**Example: the plant change in Black's amplifier.** With $A = 10^5$ and $\beta = 0.01$, $L = A\beta = 1000$ and $S = 1/1001$. A 1 percent change of $A$ changes the closed-loop gain by about $0.001$ percent.

**Example: integral action.** If $L$ has a pole at $s = 0$, then $S(0) = 0$, and an internally stable loop rejects a constant output disturbance fully. This is the simplest case of the [internal model principle](/internal-model-principle/).

**Non-example: an unstable loop.** For $L(s) = 10/(s (s + 1)(s + 2))$, $S(s) = s(s + 1)(s + 2)/(s^3 + 3s^2 + 2 s + 10)$ has two poles in the right half plane. The function $|S(j\omega)|$ can still be plotted, but it is not the gain from a sinusoidal disturbance to the output, because the response grows without bound. The readings above need an internally stable loop.

**Non-example: the open-loop sensitivity.** Without feedback, $y = P C r$, and the relative change of the map is the relative change of $P$: the sensitivity is 1 at all frequencies. Only feedback can make it smaller.

## Related definitions

- **Complementary sensitivity** $T = L/(1 + L)$, with $S + T = 1$. See [complementary sensitivity function](/complementary-sensitivity-function/).
- **Return difference** $1 + L$, the quantity Bode used; $S$ is its inverse.
- **Interpolation constraints.** For an internally stable loop, $S(p) = 0$ at each pole $p$ of $L$ in the closed right half plane, and $S(z) = 1$ at each zero $z$ of $P$ in the closed right half plane. These limit what a design can do.
- **Bode sensitivity integral.** For $L$ of relative degree at least 2 and an internally stable loop, $\int_0^\infty \ln |S(j\omega)|\, d\omega = \pi \sum_k \operatorname{Re} p_k$, summed over the open-loop poles $p_k$ in the open right half plane. Making $|S|$ small in one band makes it large in another. See [Bode sensitivity integral](/bode-sensitivity-integral/).
- **Weighted sensitivity.** The design condition $\|W_1 S\|_\infty < 1$ for a weight $W_1$ is the performance part of [mixed sensitivity design](/mixed-sensitivity-design/) and of [loop shaping](/loop-shaping/).
- The [Nyquist stability criterion](/nyquist-stability-criterion/) decides internal stability from the same curve $L(j\omega)$ whose distance to $-1$ gives $M_s$.

## References
