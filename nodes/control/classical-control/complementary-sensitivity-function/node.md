---
tag: 0WHXZ1
kind: definition
slug: complementary-sensitivity-function
name: Complementary sensitivity function
aliases:
- complementary sensitivity
area: control/classical-control
level: core
summary: T = L/(1 + L), the closed-loop map from reference to output and from sensor noise to output, with S + T = 1. A small peak of W T gives robust stability under multiplicative plant errors.
prereqs: [sensitivity-function]
see_also: [sensitivity-function, feedback-control-loop, model-uncertainty, small-gain-theorem, mixed-sensitivity-design, loop-shaping, gain-margin, phase-margin]
sources:
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 12, Frequency Domain Design (the section Sensitivity Functions), and Chapter 13, Robust Performance (the section Stability in the Presence of Uncertainty, the condition on the complementary sensitivity)
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Chapter 2, Classical Feedback Control (S, T, the peaks M_S and M_T and the bounds on the margins), and Chapter 7, Uncertainty and Robustness for SISO Systems (robust stability with multiplicative uncertainty)
  - book: "John C. Doyle, Bruce A. Francis and Allen R. Tannenbaum, Feedback Control Theory, Macmillan, 1992"
    locator: Chapter 4, Uncertainty and Robustness (robust stability for multiplicative perturbations)
---

The complementary sensitivity function of a [feedback control loop](/feedback-control-loop/) is the transfer function $T(s) = L(s)/(1 + L(s))$, where $L = P C$ is the loop transfer function. In a unity feedback loop it is the closed-loop map from the reference $r$ to the output $y$, and, with a minus sign, the map from the sensor noise $n$ to $y$. Its name comes from the identity $S + T = 1$ with the [sensitivity function](/sensitivity-function/) $S = 1/(1 + L)$. So the two cannot both be small at one frequency: a loop that rejects disturbances (small $|S|$) at a frequency passes the sensor noise (with $|T|$ near 1) at that frequency. The size of $|T(j\omega)|$ also decides how large a relative plant error the loop can tolerate before it loses stability.

## Definition

Let $P(s)$ and $C(s)$ be real rational transfer functions in a negative unity feedback loop that is well posed, $1 + L(\infty) \ne 0$. The **complementary sensitivity function** is

$$T(s) = \frac{L(s)}{1 + L(s)} = \frac{P(s)\,C(s)}{1 + P(s)\,C(s)}, \qquad S(s) + T(s) = 1.$$

With $P = b/a$ and $C = n_c/d_c$ in coprime form, $T = b\,n_c/(a\,d_c + b\,n_c)$. Its denominator is the characteristic polynomial of the loop, and its zeros are the zeros of $L$.

**Readings.** With $u = C (r - y - n)$ and $y = P u + d_o$:

$$y = T\,r + S\,d_o - T\,n.$$

So $T$ is the response of the output to the reference and to the noise, with opposite signs. A noise that the loop cannot tell apart from the output gets the same treatment as a reference.

**Peak.** For an internally stable loop, $M_T = \|T\|_\infty = \sup_\omega |T(j\omega)|$. A large $M_T$ means a resonant closed loop. Bounds on the margins follow from the definitions. At a phase crossover, $L = -1/g_m$, so $|T| = 1/(g_m - 1) \le M_T$. At a gain crossover, $|L| = 1$ and $|1 + L| = 2\sin(\varphi_m/2)$, so $|T| = 1/(2 \sin(\varphi_m/2)) \le M_T$. Hence, for $g_m > 1$,

$$g_m \ge 1 + \frac{1}{M_T}, \qquad \varphi_m \ge 2 \arcsin \frac{1}{2 M_T}.$$

**Robust stability under multiplicative uncertainty.** Let the true plant be $P_\Delta = P\,(1 + W \Delta)$, where the weight $W$ is a stable transfer function and $\Delta$ is any stable transfer function with $\|\Delta\|_\infty \le 1$ (the [H-infinity norm](/h-infinity-norm/)). Assume the nominal loop with $P$ is internally stable and that each $P_\Delta$ has the same number of poles in the closed right half plane as $P$. Then the loop is internally stable for every such $\Delta$ if and only if

$$\|W T\|_\infty = \sup_\omega |W(j\omega)\,T(j\omega)| < 1.$$

This is a theorem (Doyle, Francis and Tannenbaum 1992, chapter 4; Skogestad and Postlethwaite, chapter 7). The idea of the sufficiency part: by the assumption, the open-loop pole count of the Nyquist criterion is the same for $P_\Delta$ and $P$, and on the Nyquist contour $|L_\Delta - L| = |W \Delta L| \le |W L| < |1 + L|$, so as $\Delta$ is scaled from 0 to its full size, the Nyquist curve of $L_\Delta$ never reaches $-1$, and the count of encirclements of the [Nyquist stability criterion](/nyquist-stability-criterion/) does not change. The necessity part builds a $\Delta$ of norm at most 1 that puts a closed-loop pole on the imaginary axis at a frequency where $|W T| \ge 1$. The test is the [small-gain theorem](/small-gain-theorem/) applied to the loop seen by $\Delta$, whose gain is $-W T$; see [model uncertainty](/model-uncertainty/).

## Examples and non-examples

**Example: a third-order loop.** Let $L(s) = 1/(s(s + 1)(s + 2))$, which gives an internally stable loop. Then

- $T(0) = 1$, because $L$ has a pole at 0: a constant reference is followed exactly in steady state.
- The peak is $M_T = 1.1129$ at $\omega = 0.4350$ rad/s, and $|T(j\omega)| = 1/\sqrt 2$ at $\omega = 0.7966$ rad/s, the closed-loop bandwidth.
- At $\omega = 1$ rad/s, $|S| = 1.4142$ and $|T| = 0.4472$. At $\omega = 10$ rad/s, $|T| = 0.00098$: fast noise hardly reaches the output.
- The bounds give $g_m \ge 1.8985$ and $\varphi_m \ge 53.39$ degrees. The true values are $g_m = 6$ and $\varphi_m = 53.41$ degrees. The phase margin bound is almost tight because the peak of $|T|$ is close to the gain crossover $\omega_c = 0.44575$ rad/s.
- With a constant weight $W = 0.5$ (a relative plant error of up to 50 percent at every frequency), $\|W T\|_\infty = 0.5565 < 1$, so the loop stays internally stable for all such errors. The largest constant weight the test allows is $1/M_T = 0.8985$.

**Example: the trade at one frequency.** From $S + T = 1$ and the triangle inequality, $|S(j\omega)| + |T(j\omega)| \ge 1$ at each $\omega$. So $\max(|S|, |T|) \ge 1/2$ at every frequency. A loop cannot reject a disturbance and a sensor noise in the same frequency band.

**Example: a right half plane zero.** If $P$ has a zero at $z$ with $\operatorname{Re} z > 0$, then every internally stable loop has $T(z) = 0$ and $S(z) = 1$. For a real zero $z > 0$ and a loop with integral action, $T(0) = 1$ and $\int_0^\infty e^{-z t}\, y(t)\, dt = T(z)/z = 0$ for the unit step response $y$. Since $y(t) \to 1$, the step response must be negative for some $t$: it starts in the wrong direction. For example, $P(s) = (1 - s)/(s + 1)^2$ has $z = 1$, and every internally stable loop with integral action around it shows this undershoot.

**Non-example: $T$ of an unstable loop.** For $L(s) = 10/(s(s + 1)(s + 2))$ the closed loop has two poles in the right half plane, and $T(j\omega)$ is not a gain from a sinusoidal reference to the output.

**Non-example: $T$ is not the only transfer function to check.** For $P = 1/(s - 1)$ and $C = (s - 1)/(s + 1)$, $T = 1/(s + 2)$ is stable, but the loop is not internally stable, because $P S$ has a pole at $s = 1$. A stable $T$ alone does not prove internal stability.

## Related definitions

- [Sensitivity function](/sensitivity-function/) $S = 1/(1 + L)$, the map from an output disturbance to the output.
- **Multivariable loops.** The output complementary sensitivity is $T_o = P C (I + P C)^{-1}$ and the input one is $T_i = C P (I + C P)^{-1}$, with $S_o + T_o = I$ and $S_i + T_i = I$.
- **Closed-loop bandwidth.** The frequency where $|T(j\omega)|$ first drops to $1/\sqrt 2$ of $T(0)$. For the [standard second-order system](/second-order-system/), $T$ is the whole closed loop, and its bandwidth has a closed form.
- **Weighted complementary sensitivity.** The term $W_3 T$ in [mixed sensitivity design](/mixed-sensitivity-design/) and the high-frequency part of [loop shaping](/loop-shaping/).

## References
