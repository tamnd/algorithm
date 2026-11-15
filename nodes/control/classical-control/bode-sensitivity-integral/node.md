---
tag: MMBQ6N
kind: theorem
slug: bode-sensitivity-integral
name: Bode sensitivity integral
aliases:
- Bode integral
- waterbed effect
area: control/classical-control
level: advanced
summary: "For L of relative degree at least 2 and an asymptotically stable closed loop, the integral of ln |S(j omega)| from 0 to infinity is pi times the sum of Re p over the open-loop RHP poles."
prereqs: [sensitivity-function, nyquist-stability-criterion]
see_also: [bode-gain-phase-relation, loop-shaping, phase-margin, complementary-sensitivity-function, poles-and-zeros, h-infinity-norm, mixed-sensitivity-design, model-uncertainty]
sources:
  - book: "Hendrik W. Bode, Network Analysis and Feedback Amplifier Design, Van Nostrand, 1945"
    locator: the chapters on feedback amplifier design (the integral of the logarithm of the return difference for a loop with no unstable poles); no chapter locator confirmed
  - paper: doi:10.1109/TAC.1985.1104004
    title: James S. Freudenberg and Douglas P. Looze, Right Half Plane Poles and Zeros and Design Tradeoffs in Feedback Systems, IEEE Transactions on Automatic Control 30(6), 1985
    locator: pp. 555 to 565 (the sensitivity integral with open-loop poles in the right half plane, and the Poisson integral for zeros in the right half plane)
  - paper: doi:10.1109/MCS.2003.1213600
    title: Gunter Stein, Respect the Unstable, IEEE Control Systems Magazine 23(4), 2003
    locator: pp. 12 to 25 (the text of the 1989 Bode Lecture; the cost of unstable poles in the sensitivity integral and the limit set by finite bandwidth)
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 14, Fundamental Limits, the section on Bode's integral formula
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Section 5.2.3, on the sensitivity integrals
  - book: isbn:9780486469331
    title: John C. Doyle, Bruce A. Francis and Allen R. Tannenbaum, Feedback Control Theory, Macmillan, 1992 (Dover reprint, 2009)
    locator: Chapter 6, Design Constraints, Section 6.2, Analytic Constraints
---

The Bode sensitivity integral says that for a feedback loop whose loop transfer function $L$ has relative degree at least 2 and whose closed loop is asymptotically stable, the [sensitivity function](/sensitivity-function/) $S = 1/(1 + L)$ satisfies $\int_0^\infty \ln|S(j\omega)|\,d\omega = \pi\sum_i \operatorname{Re} p_i$, the sum over the poles $p_i$ of $L$ in the open right half plane. If $L$ has no such poles, the integral is 0: every band where feedback makes $|S| < 1$ must be paid for by a band where $|S| > 1$, with the same area under $\ln|S|$ on a linear frequency axis. Unstable open-loop poles raise the price. Bode proved the stable case in 1945, Freudenberg and Looze gave the form with unstable poles in 1985, and for relative degree 1 there is an extra term.

## Statement

**Notation.** The loop is the negative feedback loop of the [feedback control loop](/feedback-control-loop/) page, with loop transfer function $L = PC$, real rational and strictly proper, and $S = 1/(1 + L)$. Let $p_1, \ldots, p_m$ be the poles of $L$ in the open right half plane, with multiplicity. Let $\kappa = \lim_{s \to \infty} sL(s)$. It is 0 when $L$ has relative degree at least 2, and it is the leading gain of $L$ when the relative degree is 1.

**Hypotheses.**

1. $L$ is real rational and strictly proper.
2. The closed loop is asymptotically stable: no unstable cancellation in $PC$, and all closed-loop poles in the open left half plane, as checked by the [Nyquist stability criterion](/nyquist-stability-criterion/).

Poles of $L$ on the imaginary axis, such as integrators, are allowed.

**Theorem.**

$$\int_0^\infty \ln|S(j\omega)|\,d\omega = \pi\sum_{i=1}^{m}\operatorname{Re} p_i - \frac{\pi}{2}\kappa.$$

In particular, if $L$ has relative degree at least 2, the integral is $\pi\sum_i \operatorname{Re} p_i \ge 0$, and if moreover $L$ has no poles in the open right half plane, it is 0.

## In plain words

Feedback makes a loop less sensitive to disturbances at the frequencies where the loop gain is high. This theorem says that the gain in one band is paid for in another. Draw the logarithm of the sensitivity against frequency on an ordinary, not logarithmic, frequency axis. The area below zero, where feedback helps, is equal to the area above zero, where feedback makes things worse, as long as the loop gain falls fast enough at high frequency. If the plant is unstable by itself, the area above zero must be larger, and the faster the unstable modes, the larger the extra area. Since a real loop has high gain only over a limited band, pushing the sensitivity down further must push its peak up somewhere.

## Proof

**Step 1. The zeros and poles of $S$.** Write $L = n/d$ in coprime form, so $S = d/(d + n)$. By hypothesis 2 the roots of $d + n$ are in the open left half plane, so $S$ is analytic in an open set that contains the closed right half plane. Its zeros there are the roots of $d$, the poles of $L$: the $p_i$ in the open right half plane and the imaginary-axis poles of $L$. Since $L$ is strictly proper, $S(\infty) = 1$.

**Step 2. Remove the zeros in the right half plane.** Let

$$B(s) = \prod_{i=1}^{m}\frac{s - p_i}{s + \bar p_i}, \qquad S_m = S/B.$$

Each factor has modulus 1 on the imaginary axis, because $|j\omega - p| = |j\omega + \bar p|$. So $|S_m(j\omega)| = |S(j\omega)|$. $S_m$ is analytic in the open right half plane and has no zeros there, and $S_m(\infty) = 1$. The $p_i$ come in conjugate pairs, so $S_m$ is real and positive on the positive real axis. Hence $F = \ln S_m$ has an analytic branch in the open right half plane with $F(\bar s) = \overline{F(s)}$, and $\operatorname{Re} F(j\omega) = \ln|S(j\omega)|$.

**Step 3. The behavior at infinity.** For large $|s|$, $L(s) = \kappa/s + O(1/s^2)$, so $\ln S = -\ln(1 + L) = -\kappa/s + O(1/s^2)$. Also

$$\ln B(s) = \sum_i \Big(\ln(1 - p_i/s) - \ln(1 + \bar p_i/s)\Big) = -\frac{1}{s}\sum_i (p_i + \bar p_i) + O(1/s^2) = -\frac{2\sum_i \operatorname{Re} p_i}{s} + O(1/s^2).$$

So $F(s) = c/s + O(1/s^2)$ with $c = 2\sum_i \operatorname{Re} p_i - \kappa$.

**Step 4. The contour.** Integrate $F$ around the half disk of radius $R$ in the right half plane, clockwise: up the imaginary axis from $-jR$ to $jR$, with small half circles of radius $\varepsilon$ into the right half plane around the imaginary-axis zeros of $S$, and back along the arc. By Cauchy's theorem the integral is 0.

- **The small half circles.** Near a zero of order $k$, $|F| \le k|\ln\varepsilon| + c''$ and the length is $\pi\varepsilon$, so they give 0 as $\varepsilon \to 0$. The singularities of $\ln|S|$ on the axis are logarithmic and integrable.
- **The axis.** With $s = j\omega$, it gives $j\int_{-R}^{R}F(j\omega)\,d\omega$. The imaginary part of $F(j\omega)$ is odd in $\omega$ and drops out, and the real part is even, so this is $2j\int_0^R \ln|S(j\omega)|\,d\omega$.
- **The arc.** With $s = Re^{j\theta}$, $\theta$ from 90 degrees down to $-90$ degrees, $\int (c/s)\,ds = c\int j\,d\theta = -j\pi c$, and the $O(1/s^2)$ term gives $O(1/R)$.

So $2j\int_0^\infty \ln|S(j\omega)|\,d\omega - j\pi c = 0$, and the integral is $\pi c/2 = \pi\sum_i \operatorname{Re} p_i - \pi\kappa/2$. The integral converges: for large $\omega$, $\ln|S(j\omega)| = \operatorname{Re}(-\kappa/(j\omega)) + O(1/\omega^2) = O(1/\omega^2)$. $\square$

**Checks by hand.** The identity $\int_0^\infty \ln\frac{\omega^2 + a^2}{\omega^2 + b^2}\,d\omega = \pi(a - b)$ for $a, b \ge 0$ makes the first-order cases exact.

- $L = 3/(s - 1)$: relative degree 1, $\kappa = 3$, $p_1 = 1$, closed loop $s + 2$. Here $S = (s - 1)/(s + 2)$, $\ln|S| = \frac12\ln\frac{\omega^2 + 1}{\omega^2 + 4}$, and the integral is $\frac12\pi(1 - 2) = -\pi/2$. The theorem gives $\pi \cdot 1 - \frac{\pi}{2}\cdot 3 = -\pi/2$.
- $L = 1/(s + 1)^2$: relative degree 2, no unstable poles, closed loop $s^2 + 2s + 2$. Here $|S(j\omega)|^2 = (1 + \omega^2)^2/(\omega^4 + 4)$, so $|S| < 1$ exactly when $\omega^2 < 1.5$, that is, below $\omega = 1.22474$, and $|S| > 1$ above it, with the peak $\sqrt 5/2 = 1.11803$ at $\omega = 2$. The two areas are equal, and the integral is 0.
- $L = 4/((s - 1)(s + 2))$: relative degree 2, $p_1 = 1$, closed loop $s^2 + s + 2$. Here $|S(j\omega)|^2 = (\omega^4 + 5\omega^2 + 4)/(\omega^4 - 3\omega^2 + 4)$, which is at least 1 at every frequency: feedback makes the sensitivity worse everywhere, and the integral is $\pi$. The peak is $M_s = 3$ at $\omega = \sqrt 2$.

## Consequences

- **The check loop.** For $L = 1/(s(s + 1)(s + 2))$ the integral is 0. The integrator gives $S(0) = 0$, and $|S| < 1$ below $\omega = 1/\sqrt 6 = 0.40825$; you can check that at $\omega^2 = 1/6$, $|L|^2 = 216/175$ and $\operatorname{Re} L = -108/175$, so $|1 + L|^2 = 1 + 2\operatorname{Re} L + |L|^2 = 1$. Above that frequency $|S| > 1$, with the peak $M_s = 1.56838$ at $\omega = 0.72631$, and $|S| \to 1$ at high frequency.
- **A bound on the peak.** Suppose $|S| \le \epsilon < 1$ on $[0, \omega_1]$, and the loop gain is so small above $\omega_2$ that the integral of $\ln|S|$ there is at most $\delta$. Then $0 \le \omega_1\ln\epsilon + (\omega_2 - \omega_1)\ln M_s + \delta$ for a loop with no unstable poles, so $\ln M_s \ge (\omega_1\ln(1/\epsilon) - \delta)/(\omega_2 - \omega_1)$. Good rejection over a wide band, inside a limited bandwidth, forces a large peak $M_s$, and with it small [stability margins](/phase-margin/). This is Stein's point in "Respect the Unstable": the frequency axis is linear, so the extra area cannot be spread thinly over infinite bandwidth in a real loop.
- **Unstable poles cost bandwidth.** The term $\pi\sum \operatorname{Re} p_i$ grows with the speed of the unstable poles. A plant with a fast unstable pole needs a high crossover frequency and still gets a larger area of $|S| > 1$.
- **Relative degree 1 is not an escape.** The term $-\frac{\pi}{2}\kappa$ can make the integral negative, as for $1/(s + 1)$, where $|S| < 1$ at every frequency. But a physical loop rolls off at high frequency, with relative degree at least 2 once sensors and actuators are included.
- **Related limits.** The [Bode gain-phase relation](/bode-gain-phase-relation/) limits how fast $|L|$ can fall near crossover; this integral limits the shape of $|S|$. Zeros of $L$ in the right half plane give a weighted (Poisson) integral of the same kind (Freudenberg and Looze 1985). These limits also bound what [mixed-sensitivity design](/mixed-sensitivity-design/) can reach: no choice of weights can make $|S|$ small at all frequencies.

## Tightness

- **The closed loop must be asymptotically stable.** For $L = 10/(s + 1)^3$, relative degree 3 and no unstable poles, the closed loop $(s + 1)^3 + 10$ has the poles $0.07722 \pm 1.86580j$ in the right half plane. The integral is $-0.48517$, not 0. The same proof with the unstable closed-loop poles $q_k$ also removed gives $\pi\sum\operatorname{Re} p_i - \pi\sum\operatorname{Re} q_k - \frac{\pi}{2}\kappa$, here $-2\pi \cdot 0.07722 = -0.48517$.
- **Relative degree 1.** For $L = 1/(s + 1)$, $S = (s + 1)/(s + 2)$ and the integral is $-\pi/2$, not 0. The relative degree hypothesis cannot be dropped from the zero-area form.
- **The frequency axis is linear.** The integral is in $d\omega$, not in $d\ln\omega$. On the usual Bode axes the areas above and below 0 dB do not look equal; a small rise of $|S|$ over many decades at high frequency can balance a deep dip at low frequency.

## History

Bode derived the integral in his 1945 book "Network Analysis and Feedback Amplifier Design", for amplifiers with no unstable poles in the loop, as a limit on the feedback that an amplifier can have over a band. Freudenberg and Looze (1985) gave the form with open-loop poles in the right half plane and the Poisson integral for zeros in the right half plane, and they turned the integrals into design trade-offs. Gunter Stein's Bode Lecture of 1989, printed in 2003 as "Respect the Unstable", made the cost of unstable poles widely known among control engineers.

## References
