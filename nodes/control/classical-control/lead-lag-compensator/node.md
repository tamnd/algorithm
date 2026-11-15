---
tag: 8T0JHX
kind: technique
slug: lead-lag-compensator
name: Lead-lag compensator
aliases:
- phase-lead compensation
- phase-lag compensation
area: control/classical-control
level: core
summary: A first-order compensator that adds phase near crossover when its zero lies below its pole, or raises the low frequency gain when its pole lies below its zero.
prereqs: [bode-plot, phase-margin]
see_also: [loop-shaping, pid-controller, gain-margin, nichols-chart, bode-gain-phase-relation, root-locus, controller-discretization, sensitivity-function]
sources:
  - book: isbn:9780136156734
    title: Katsuhiko Ogata, Modern Control Engineering, fifth edition, Prentice Hall, 2010
    locator: Section 7-11, Lead Compensation, Section 7-12, Lag Compensation, and Section 7-13, Lag-Lead Compensation (frequency-response design; Ogata writes the lead network with a parameter below 1)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 6.7.2, Lead Compensation, and Section 6.7.4, Lag Compensation
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 12, Frequency Domain Design (lead and lag compensation as part of loop shaping)
---

A lead-lag compensator is a controller built from first-order factors of the form $(1 + \tau_z s)/(1 + \tau_p s)$, one real zero and one real pole, placed in series with the plant $P$ of a unity negative feedback loop with $L = PC$. A lead network has its zero below its pole, $C(s) = (1 + \alpha T s)/(1 + T s)$ with $\alpha > 1$. It adds positive phase in a band of frequencies, and the designer puts that band at the gain crossover to raise the [phase margin](/phase-margin/). A lag network has its pole below its zero, $C(s) = (1 + T s)/(1 + \beta T s)$ with $\beta > 1$. It lowers the gain at high frequency by the factor $\beta$ with little phase loss there, so the gain at low frequency can be $\beta$ times higher for the same crossover. Both factors have $C(0) = 1$, and a separate gain $k$ sets the error constant. These are the standard building blocks of classical [loop shaping](/loop-shaping/) on the [Bode plot](/bode-plot/).

## In plain words

A plant often has too little phase where its gain curve passes through one, so the closed loop rings or is close to instability. A lead network is a small filter that pushes the phase up in a band of frequencies. The designer puts the top of that band where the loop gain passes through one, and the ringing goes away. The cost is more gain at high frequency, so more sensor noise gets through. A lag network does the opposite job. It cuts the gain at high frequency and keeps the phase almost the same there. So the designer can use a high gain for slow signals, which gives small steady errors, and the loop still has a safe crossover. The cost is a slower loop. A lag-lead network uses one of each.

## When it applies

- The plant is linear, time invariant, and single input single output, with a model $P(s)$ or a measured frequency response, and the specifications are an error constant, a phase margin or a peak sensitivity, and a crossover frequency or bandwidth.
- **Lead** fits when the phase margin is too small at the crossover that the error constant gives, and when the plant phase falls slowly near that crossover. One lead network gives at most 90 degrees, and in practice about 50 to 60 degrees; for more, two networks are used in series.
- **Lag** fits when the phase margin is good at a lower frequency and the specifications allow that lower crossover, but the low frequency gain is too small. It does not add phase; it moves the crossover down to a frequency where the plant phase is already good enough.
- Neither network fixes a plant whose phase falls fast near the wanted crossover, for example with a long time delay or a zero in the right half plane. The [Bode gain-phase relation](/bode-gain-phase-relation/) holds for these networks as for any minimum-phase factor, so the phase they add always comes with a gain slope.

## The template

**The lead network.** For $C(s) = (1 + \alpha T s)/(1 + T s)$ with $\alpha > 1$ and $T > 0$, the phase is $\varphi(\omega) = \arctan(\alpha T\omega) - \arctan(T\omega)$, which is positive for all $\omega > 0$. It is largest at the geometric mean of the corner frequencies $1/(\alpha T)$ and $1/T$,

$$\omega_m = \frac{1}{T\sqrt\alpha}, \qquad \sin\varphi_{\max} = \frac{\alpha - 1}{\alpha + 1}, \qquad |C(j\omega_m)| = \sqrt\alpha.$$

The gain rises from 1 at low frequency to $\alpha$ at high frequency, and at $\omega_m$ it is halfway in dB, $10\log_{10}\alpha$. Conversely, a lead of $\varphi$ degrees needs $\alpha = (1 + \sin\varphi)/(1 - \sin\varphi)$:

| $\alpha$ | 2 | 4 | 7.5486 | 10 | 13.928 |
|---|---|---|---|---|---|
| $\varphi_{\max}$ (degrees) | 19.47 | 36.87 | 50 | 54.90 | 60 |
| gain at $\omega_m$ (dB) | 3.01 | 6.02 | 8.78 | 10.00 | 11.44 |

**The lag network.** The lag $C(s) = (1 + T s)/(1 + \beta T s)$ is the reciprocal of the lead with the same parameters, so its phase is the negative of the lead phase and its gain falls from 1 to $1/\beta$. Far above its corners it is almost a pure gain $1/\beta$.

**The design steps.** First set the gain $k$ of $P$ from the error constant. Then:

```pseudo id=main
LEAD-LAG-DESIGN(P, pm, extra)           ▷ P already holds the gain k
L1  (ωc, pm0) ← gain crossover and phase margin of P
L2  if pm0 ≥ pm then return C = 1
L3  if a lead network is chosen then
L4      φ ← pm - pm0 + extra             ▷ extra pays for the move of the crossover
L5      α ← (1 + sin φ)/(1 - sin φ)
L6      ωm ← the highest ω with |P(jω)| = 1/√α
L7      T ← 1/(ωm √α)
L8      return C(s) = (1 + αTs)/(1 + Ts)
L9  else                                 ▷ a lag network
L10     ωc ← the highest ω with arg P(jω) = -180 + pm + extra degrees
L11     β ← |P(jωc)|
L12     T ← 10/ωc                        ▷ the lag zero a decade below ωc
L13     return C(s) = (1 + Ts)/(1 + βTs)
```

Then check the result: compute the margins and the peak $M_s$ of the [sensitivity function](/sensitivity-function/), confirm with the closed-loop poles or the [Nyquist stability criterion](/nyquist-stability-criterion/) that the loop is asymptotically stable, and look at the step response. If the margin is short, raise `extra` and repeat.

**Why it works.** For the lead, the derivative of $\varphi(\omega)$ is zero where $\alpha T^2\omega^2 = 1$, which gives $\omega_m$, and there $\tan\varphi_{\max} = (\alpha - 1)/(2\sqrt\alpha)$, which is the same as the sine formula. Line L6 puts $\omega_m$ at the new crossover: the network adds the gain $\sqrt\alpha$ at $\omega_m$, so $|P(j\omega_m)| = 1/\sqrt\alpha$ makes $|L(j\omega_m)| = 1$. The crossover moves up, where the plant phase is lower, and `extra` pays for that loss. For the lag, at $\omega_c = 10/T$ the network has the gain $1/\beta$ to within 0.5 percent, so $|L(j\omega_c)| \approx 1$ by line L11, and its phase there is about $-(1 - 1/\beta)/10$ radians, at most 5.7 degrees, which is why `extra` is about 5 degrees. The error constant does not change, because $C(0) = 1$.

## Classic examples

**A lead network for a fast loop.** Let $P(s) = 10/(s(s + 1))$, so the velocity constant is $K_v = \lim_{s \to 0} sP(s) = 10$ per second, and ask for a phase margin of at least 45 degrees. Without compensation the crossover is at 3.08423 rad/s, the phase margin is 17.96 degrees and $M_s = 3.35157$. The margin is 27 degrees short; with about 10 degrees extra for the move of the crossover, take a lead of 37 degrees, $\alpha = 4$ ($\varphi_{\max} = 36.87$ degrees). The plant gain is $1/\sqrt 4 = 1/2$ where $\omega^2(\omega^2 + 1) = 400$, that is, at

$$\omega_m = \sqrt{\big(-1 + \sqrt{1601}\big)/2} = 4.41659, \qquad T = \frac{1}{2\omega_m} = 0.11321, \qquad \alpha T = 0.45284.$$

The plant phase there is $-90 - \arctan 4.41659 = -167.24$ degrees, so the new margin is $180 - 167.24 + 36.87 = 49.63$ degrees. The loop

$$L(s) = \frac{10(1 + 0.45284 s)}{s(s + 1)(1 + 0.11321 s)}$$

has its only crossover at 4.41659 rad/s, $M_s = 1.42139$ at 6.613 rad/s, an infinite gain margin, and closed-loop poles $-3.31691 \pm 4.07521j$ and $-3.19936$. You can check the lead formula by hand with $\alpha = 4$ and $T = 1$: at $\omega = 0.5$, $\arctan 2 - \arctan 0.5 = 63.43 - 26.57 = 36.87$ degrees, and $|C| = \sqrt 5/\sqrt{1.25} = 2$.

**A lag network for the same plant.** Keep $K_v = 10$ and ask for a phase margin of 50 degrees with a lag network, with `extra` = 5 degrees. The plant phase is $-90 - \arctan\omega$, which is $-125$ degrees at $\omega_c = \tan 35^\circ = 0.70021$. There $\beta = |P(j\omega_c)| = 11.6987$, and $T = 10/\omega_c = 14.2815$, so

$$C(s) = \frac{1 + 14.2815 s}{1 + 167.07 s}.$$

The network costs 5.22 degrees at $\omega_c$, a little more than the 5 degrees allowed. The loop has its crossover at 0.70279 rad/s, a phase margin of 49.70 degrees, $M_s = 1.48123$ and closed-loop poles $-0.46513 \pm 0.75762j$ and $-0.07573$.

| loop | crossover (rad/s) | phase margin (degrees) | $M_s$ | slowest closed-loop pole | high frequency gain of $C$ |
|---|---|---|---|---|---|
| $P$ alone | 3.08423 | 17.96 | 3.35157 | $-0.5 \pm 3.12250j$ | 1 |
| with the lead | 4.41659 | 49.63 | 1.42139 | $-3.19936$ | 4 |
| with the lag | 0.70279 | 49.70 | 1.48123 | $-0.07573$ | 0.0855 |

Both designs reach about the same margin with the same $K_v$, but in different ways. The lead keeps the loop fast and raises its noise gain by 4. The lag makes the loop about six times slower, and its slowest pole sits near the lag zero at $-1/T = -0.07002$, so the step response has a small slow tail.

## Variations

- **Lag-lead network.** A lag network and a lead network in series, the lag for the error constant and the lead for the margin. A common form is $\big((1 + T_1 s)/(1 + \beta T_1 s)\big)\big((1 + T_2 s)/(1 + T_2 s/\beta)\big)$ with one parameter for both parts.
- **Two leads in series.** For more than about 60 degrees, two networks of half the lead each need a much smaller total $\alpha$: two networks of 30 degrees need $\alpha = 3$ each, so 9 in total, against $\alpha = 13.93$ for one network of 60 degrees.
- **PD and PI as limits.** If $T \to 0$ with $\alpha T = T_d$ fixed, the lead becomes $1 + T_d s$, the PD factor. If $\beta \to \infty$, $\beta$ times the lag becomes $(1 + T s)/(T s)$, the PI factor of a [PID controller](/pid-controller/). The lead is a PD factor with a filter, and the lag is a PI factor with a finite low frequency gain.
- **Design on other charts.** The same networks can be placed on the [Nichols chart](/nichols-chart/), where the lead moves the curve to the right near crossover, or with the [root locus](/root-locus/), where the zero and pole are put to pull the dominant closed-loop poles to a wanted place.
- **Digital lead and lag.** A network for a sampled loop is designed in continuous time and then mapped, for example by the bilinear transform ([controller discretization](/controller-discretization/)), or designed directly in $z$.
- **Notation.** Ogata writes the lead as $(Ts + 1)/(\alpha T s + 1)$ with $0 < \alpha < 1$, the reciprocal of the $\alpha$ used here.

## Pitfalls

- **Too much lead.** A large $\alpha$ moves the crossover far up, where the plant phase is low, so each added degree of lead buys less margin. The high frequency gain $\alpha$ also multiplies sensor noise into the actuator. Above about $\alpha = 10$ to 15, use two networks or change the specifications.
- **Forgetting the move of the crossover.** The lead adds the gain $\sqrt\alpha$ at $\omega_m$, so a design that puts $\omega_m$ at the old crossover ends with a crossover at a higher frequency and a smaller margin than planned.
- **A lag zero too close to crossover.** If the lag zero is put a factor 5 below the crossover instead of 10, the lag costs more phase at the crossover. In the example the margin then falls to 44.43 degrees, and with a factor 20 it rises to 52.36 degrees, but the slow closed-loop pole moves from $-0.16459$ to $-0.03638$, which makes the tail of the step response longer.
- **The slow tail of a lag.** A lag design leaves a closed-loop pole near the lag zero. The pair nearly cancels in the reference response, but the slow pole shows fully in the response to a load disturbance.
- **Trusting the phase margin alone.** Check $M_s$ and the gain margin too, and check stability of the closed loop; a loop with an unstable plant can have a good-looking phase margin and still be unstable.
- **A plant with a delay or a zero in the right half plane.** The phase of such a plant falls fast with frequency, so the lead loses its effect when the crossover moves up. The crossover frequency then has a limit that no lead network can remove.

## Exercises

1. Show that the phase of the lead network is largest at $\omega_m = 1/(T\sqrt\alpha)$ and that $\sin\varphi_{\max} = (\alpha - 1)/(\alpha + 1)$.
2. Which $\alpha$ gives a lead of 50 degrees? (Answer: $\alpha = 7.5486$.)
3. Find the phase of the lead network with $\alpha = 4$ and $T = 1$ at $\omega = 1$. (Answer: $\arctan 4 - \arctan 1 = 30.96$ degrees.)
4. Redo the lead example with $\alpha = 10$. (Answer: $\omega_m = 5.57913$, $T = 0.056680$, a phase margin of 65.06 degrees and $M_s = 1.21983$.)
5. Show that the lag network has the phase $\arctan(T\omega) - \arctan(\beta T\omega)$, that it is the reciprocal of the lead network with the same parameters, and that at $\omega = 10/T$ its phase is close to $-(1 - 1/\beta)/10$ radians.
6. Show that $\beta(1 + T s)/(1 + \beta T s) \to (1 + T s)/(T s)$ as $\beta \to \infty$.
7. Explain why a lag network does not change the velocity constant of the loop, while it lowers the crossover frequency.

## References
