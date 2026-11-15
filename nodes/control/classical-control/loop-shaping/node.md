---
tag: 266P6R
kind: technique
slug: loop-shaping
name: Loop shaping
aliases:
- classical loop shaping
area: control/classical-control
level: core
summary: "Design a controller C by shaping the Bode plot of L = PC: high gain at low frequency, low gain at high frequency, and a crossover with a slope near -20 dB per decade and enough phase margin."
prereqs: [bode-plot, phase-margin, sensitivity-function, bode-gain-phase-relation]
see_also: [lead-lag-compensator, pid-controller, bode-sensitivity-integral, nichols-chart, gain-margin, h-infinity-loop-shaping, mixed-sensitivity-design, model-uncertainty]
sources:
  - book: "Isaac M. Horowitz, Synthesis of Feedback Systems, Academic Press, 1963"
    locator: the whole book (the design of the loop transmission against plant uncertainty and the cost of feedback in bandwidth); no chapter locator confirmed
  - book: isbn:9780486469331
    title: John C. Doyle, Bruce A. Francis and Allen R. Tannenbaum, Feedback Control Theory, Macmillan, 1992 (Dover reprint, 2009)
    locator: Chapter 7, Loopshaping (performance and robustness specifications turned into bounds on the loop gain)
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Section 2.6, Loop shaping, with Section 2.6.1 on the trade-offs in terms of L and Section 2.6.2 on the fundamentals, including the limits from zeros in the right half plane and from time delays
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 12, Frequency Domain Design, the section on feedback design via loop shaping
---

Loop shaping is a way to design a feedback controller $C$ by choosing the frequency response of the loop transfer function $L = PC$ instead of the closed loop. The designer asks for high gain $|L|$ at low frequency, so that the [sensitivity function](/sensitivity-function/) $|S| \approx 1/|L|$ is small and the loop tracks references and rejects disturbances; low gain at high frequency, so that $|T| \approx |L|$ is small and the loop ignores sensor noise and model errors; and a crossover where $|L|$ passes 0 dB with a slope near $-20$ dB per decade and enough [phase margin](/phase-margin/). On a [Bode plot](/bode-plot/) the factors of $C$ add to the curve of $P$, so the controller is built one factor at a time. The [Bode gain-phase relation](/bode-gain-phase-relation/) and the [Bode sensitivity integral](/bode-sensitivity-integral/) say how far the shape can be pushed.

## In plain words

The loop gain is the controller times the plant, and its curve against frequency tells most of the story. Where the curve is high, the loop follows commands and fights disturbances. Where it is low, the loop ignores noise and does not care about errors in the model. The designer draws the wanted curve: high at slow frequencies, low at fast ones, and a gentle slope where the curve passes through one, because a steep slope there brings too much lag and the loop starts to ring. Then the controller is the wanted curve divided by the plant, built from a few standard pieces such as an integrator, a lead and a lag. Last, the designer checks the margins and the response, and adjusts.

## When it applies

- The plant is linear, time invariant, and single input single output, with a model $P(s)$ or a measured frequency response. For several inputs and outputs the same ideas work with singular values, with more care.
- The specifications are, or can be turned into, bounds on $|S|$ and $|T|$ over frequency bands: an error of at most $\epsilon$ for slow references and disturbances, a noise or uncertainty bound at high frequency, a peak $M_s$ of 1.2 to 2, and a phase margin of 30 to 60 degrees.
- The plant is minimum-phase and stable, or close to it. A zero in the right half plane at $z$, a time delay $\tau$ and an unstable pole at $p$ all limit the crossover frequency $\omega_c$. Common rules of thumb are $\omega_c < z/2$, $\omega_c < 1/\tau$ and $\omega_c > 2p$; an unstable pole and a slower zero in the right half plane together make the design hard or impossible.

## The template

1. **Turn the specifications into bounds on $|L|$.** If $|L| \ge 1/\epsilon$ with $\epsilon < 1$, then $|S| = 1/|1 + L| \le \epsilon/(1 - \epsilon)$. If $|L| \le \delta < 1$, then $|T| = |L|/|1 + L| \le \delta/(1 - \delta)$. So a low-frequency band where $|S|$ must be small becomes a floor under $|L|$, and a high-frequency band where $|T|$ must be small becomes a ceiling over $|L|$. For a relative [model uncertainty](/model-uncertainty/) of size $|W(j\omega)|$, robust stability asks $|T(j\omega)W(j\omega)| < 1$, which is again a ceiling at high frequency.
2. **Choose the crossover frequency $\omega_c$.** It must lie between the floor band and the ceiling band, and below the limits set by zeros in the right half plane and delays. The closed-loop bandwidth is roughly $\omega_c$.
3. **Draw the target loop.** Put an integrator in $L$ if steady state errors to steps must be 0. Give $|L|$ a slope of about $-20$ dB per decade over roughly a decade around $\omega_c$; by the gain-phase relation this keeps the phase near $-90$ to $-135$ degrees there. Let the gain fall faster above that band, for roll-off.
4. **Build $C$.** Write $C = L_{\text{target}}/P$ in terms of standard factors: a gain, an integrator or a PI factor $(T_i s + 1)/(T_i s)$, a [lead-lag compensator](/lead-lag-compensator/) for phase near $\omega_c$, and extra poles for roll-off. Never cancel a pole or zero of $P$ in the closed right half plane.
5. **Check and iterate.** Compute the margins, $M_s$ and $M_t = \max|T|$, confirm with the [Nyquist stability criterion](/nyquist-stability-criterion/) or the closed-loop poles that the loop is asymptotically stable, and look at the step responses to the reference and to a load disturbance.

**Why it works.** At frequencies where $|L| \gg 1$, $S \approx 1/L$ and $T \approx 1$. Where $|L| \ll 1$, $S \approx 1$ and $T \approx L$. So far from crossover, the closed loop is read directly from $L$, and the shape of $|L|$ alone sets performance and noise rejection. Near crossover neither approximation holds, and there the phase of $L$ decides the peaks of $|S|$ and $|T|$; for a minimum-phase loop that phase is fixed by the slope of $|L|$, which is why step 3 asks for a gentle slope. The sensitivity integral adds a global limit: with a finite bandwidth, a deeper floor under $|L|$ costs a higher peak of $|S|$ elsewhere.

## Classic examples

**A PI controller for three equal lags.** Let $P(s) = 1/(s + 1)^3$ and ask for zero steady state error to steps and a phase margin of 60 degrees. Take $C(s) = k_p(T_i s + 1)/(T_i s)$. The integrator gives the floor at low frequency. Put the PI zero a factor 3 below crossover, $T_i\omega_c = 3$, so that the PI factor costs $90 - \arctan 3 = 18.43$ degrees at $\omega_c$. The plant phase is $-3\arctan\omega$, so the margin of 60 degrees needs $3\arctan\omega_c = 180 - 60 - 18.43 = 101.57$ degrees, which gives $\omega_c = \tan(33.86^\circ) = 0.67083$ and $T_i = 4.47205$. The gain from $|L(j\omega_c)| = 1$ is

$$k_p = \frac{(1 + \omega_c^2)^{3/2}}{\sqrt{1 + 1/9}} = \frac{1.45^{1.5}}{1.05409} = 1.65646,$$

so $k_i = k_p/T_i = 0.37040$. You can check the phase by hand: at $\omega_c$ the plant gives $-101.57$ degrees and the PI factor $-18.43$ degrees, $-120$ in total.

The resulting loop has these properties:

| quantity | value |
|---|---|
| phase margin | 60.00 degrees at $\omega_c = 0.67083$ |
| gain margin | 3.7819 (11.554 dB) at $\omega = 1.55612$ |
| peak sensitivity $M_s$ | 1.73168 at $\omega = 1.07547$ |
| peak of $\lvert T\rvert$ | 1.08677 at $\omega = 0.86866$ |
| closed-loop poles | $-2.14048$, $-0.34699 \pm 0.96173j$, $-0.16554$ |

The approximations of step 1 hold away from crossover. At $\omega = 0.01$, $|S| = 0.02695$ and $1/|L| = 0.02697$; at $\omega = 0.1$, $|S| = 0.23604$ and $1/|L| = 0.25016$. At $\omega = 3$, $|T| = 0.05473$ and $|L| = 0.05253$; at $\omega = 10$, $|T| = 0.001633$ and $|L| = 0.001632$.

For comparison, the classic Ziegler-Nichols PID for the same plant ($K_p = 4.8$, $T_i = 1.8138$, $T_d = 0.45345$) has a phase margin of 30.62 degrees at $\omega_c = 1.37545$ and $M_s = 2.13177$: a faster loop with half the phase margin and a higher peak of $|S|$.

**The slow pole of the PI zero.** The closed-loop pole at $-0.16554$ is close to the PI zero at $-1/T_i = -0.22361$. In the response to a reference step the pair nearly cancels and leaves a small slow tail. In the response to a load disturbance at the plant input, the zero is not in the transfer function $PS$, and the slow pole shows fully. Placing the PI zero closer to $\omega_c$ speeds this pole up but costs phase margin.

**A lead network on a fast plant.** For $P(s) = 10/(s(s + 1))$, the loop without compensation has its crossover at 3.08423 rad/s with a phase margin of only 17.96 degrees. A lead network adds about 37 degrees at a new crossover of 4.41659 rad/s and gives a margin of 49.63 degrees with the same low-frequency gain; the [lead-lag compensator](/lead-lag-compensator/) page works this example through.

## Variations

- **Lead-lag design.** Shape the loop with one or two first-order lead or lag factors, the classical form of loop shaping before computers ([lead-lag compensator](/lead-lag-compensator/)).
- **PID tuning by loop shaping.** Fix the crossover and margin of a [PID controller](/pid-controller/) loop, as in the example above, instead of a tuning table.
- **Design on the Nichols chart.** Work with the curve of $L$ on the [Nichols chart](/nichols-chart/), where a gain change moves the curve up or down and the closed-loop peak is read from the contours.
- **Horowitz's design against uncertainty.** Isaac Horowitz (1963) designed $L$ so that a whole set of plants meets the specifications, by bounds on $L$ at each frequency; he later developed this into quantitative feedback theory.
- **H-infinity loop shaping.** Shape the plant with weights by the classical rules, then compute a controller that robustly stabilizes the shaped plant ([H-infinity loop shaping](/h-infinity-loop-shaping/)).
- **Mixed-sensitivity design.** Write the floor and the ceiling as weights on $S$ and $T$ and minimize an H-infinity norm ([mixed-sensitivity design](/mixed-sensitivity-design/)).
- **Two degrees of freedom.** Shape $L$ for feedback properties only, and shape the reference response with a prefilter ([two-degree-of-freedom control](/two-degree-of-freedom-control/)).

## Pitfalls

- **Cancelling an unstable pole or a zero in the right half plane.** $C = 1/P$ near such a factor gives a nice $L$ but an internally unstable loop: the cancelled mode is still there in $PS$ or $CS$.
- **Shaping the gain and forgetting the phase.** A slope of $-40$ dB per decade at crossover gives a phase near $-180$ degrees for a minimum-phase loop. With a delay or a zero in the right half plane the phase is even lower than the slope suggests.
- **Trusting the two margins.** A loop with good gain and phase margins can still pass close to $-1$ between the crossovers, for example near a lightly damped mode. Check $M_s$ as well (see the example on the [gain margin](/gain-margin/) page).
- **Several crossovers.** If $|L|$ crosses 0 dB more than once, each crossover needs its own phase margin, and the smallest counts.
- **Saturation.** The linear design assumes that the actuator does not saturate. A high gain at low frequency with an integrator needs [anti-windup](/anti-windup/).
- **Pushing the floor too far.** By the sensitivity integral, a deeper or wider floor under $|L|$ raises the peak of $|S|$ when the bandwidth is limited.

## Exercises

1. In the PI example, what does the PI factor cost in phase at $\omega_c$ if $T_i\omega_c = 5$? (Answer: $90 - \arctan 5 = 11.31$ degrees.)
2. Redo the PI design for a phase margin of 45 degrees with $T_i\omega_c = 3$. (Answer: $\omega_c = 0.80560$, $T_i = 3.72392$, $k_p = 2.00886$.)
3. Show that $|L(j\omega)| \ge 10$ implies $|S(j\omega)| \le 1/9$, and that $|L(j\omega)| \le 0.1$ implies $|T(j\omega)| \le 1/9$.
4. For $L(s) = k/(s(s + 1))$, find $k$ for a phase margin of 45 degrees. (Answer: the phase is $-135$ degrees at $\omega = 1$, so $k = \sqrt 2$.)
5. Let $P(s) = 1/(s - 1)$ and $C(s) = 2(s - 1)/(s(s + 1))$. Compute $L$ and its margins, then compute $PS$ and explain why the loop is not usable.

## References
