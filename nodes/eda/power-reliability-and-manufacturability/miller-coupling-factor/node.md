---
tag: ZQ5VTR
kind: definition
slug: miller-coupling-factor
name: Miller coupling factor
aliases:
- switch factor
- coupling capacitance multiplier
area: eda/power-reliability-and-manufacturability
level: core
summary: The factor, usually 0 to 2, by which a coupling capacitance is scaled when it is grounded for delay analysis, depending on whether the neighbor switches with or against the net.
prereqs: [crosstalk-noise, elmore-delay]
see_also: [devgan-noise-metric, static-timing-analysis, parasitic-extraction, rc-tree, nonlinear-delay-model, dynamic-power-dissipation]
sources:
  - paper: "Andrew B. Kahng, Sudhakar Muddu and Egino Sarto, On switch factor based analysis of coupled RC interconnects, Proceedings of the 37th Design Automation Conference (DAC), 79 to 84, 2000"
    title: Andrew B. Kahng, Sudhakar Muddu and Egino Sarto, On switch factor based analysis of coupled RC interconnects, Proceedings of the 37th ACM/IEEE Design Automation Conference, 79 to 84, June 2000
    locator: the analysis of the switch factor under different slews and alignments of the aggressor, which gives the range from -1 to 3 in place of the usual range from 0 to 2
  - book: isbn:9780130909961
    title: Jan M. Rabaey, Anantha Chandrakasan and Borivoje Nikolic, Digital Integrated Circuits, A Design Perspective, 2nd edition, Prentice Hall, 2003
    locator: the chapter on coping with interconnect, section on capacitive crosstalk and its effect on delay
  - paper: "John M. Miller, Dependence of the input impedance of a three-electrode vacuum tube upon the load in the plate circuit, Scientific Papers of the Bureau of Standards 15(351), 367 to 385, 1920"
    title: John M. Miller, Dependence of the input impedance of a three-electrode vacuum tube upon the load in the plate circuit, Scientific Papers of the Bureau of Standards 15, 1920
    locator: the original Miller effect, a capacitance between the input and the output of an inverting amplifier of gain A that looks 1 + A times larger from the input
---

## Definition

A victim net is joined to a neighbor net, the aggressor, by a coupling capacitance $C_c$, and to ground by $C_g$. Delay calculators work with grounded capacitances. To fold $C_c$ into a grounded model, they replace it by $k\, C_c$ to ground, so the victim sees $C_g + k C_c$. The number $k$ is the *Miller coupling factor*, also called the switch factor. The name comes from the Miller effect of amplifiers, where a capacitor between two nodes whose voltages move in opposite directions looks larger from one of them.

There are two common ways to fix $k$. They agree in the simple cases and disagree in others, so a statement about $k$ must say which one it uses.

**Charge-based factor.** The victim voltage $v(t)$ makes a transition of size $V$ that starts at $t = 0$, and its delay is measured at the threshold $\theta V$, usually $\theta = 1/2$, reached at $t_\theta$. The aggressor voltage is $a(t)$. The charge that the victim driver must put on $C_c$ up to $t_\theta$ is $C_c\, \Delta(v - a)$, where $\Delta$ is the change over $[0, t_\theta]$. A grounded capacitance $k C_c$ would take the charge $k C_c\, \Delta v$, so

$$ k_{\text{charge}} = \frac{\Delta (v - a)}{\Delta v} = 1 - \frac{\Delta a}{\theta V} . $$

**Delay-based factor.** $k_{\text{delay}}$ is the value for which the victim's threshold delay in the grounded model equals its delay in the coupled circuit.

The three textbook values come from the charge-based form with ramps of equal slew that start together: a quiet aggressor ($\Delta a = 0$) gives $k = 1$; an aggressor that switches in the same direction ($\Delta a = \Delta v$) gives $k = 0$; an aggressor that switches in the opposite direction ($\Delta a = -\Delta v$) gives $k = 2$.

**Theorem (equal slews give 0 to 2).** Let the victim be a ramp of rise time $t_r$ and the aggressor a ramp of the same swing $V$ and the same rise time, in either direction, starting at any time. Then $0 \le k_{\text{charge}} \le 2$.

*Proof.* The victim's window is $[0, \theta t_r]$, and $\Delta v = \theta V$. The aggressor's slope is at most $V / t_r$ in absolute value, so over a window of length $\theta t_r$ it changes by at most $\theta V$: $|\Delta a| \le \theta V$. Then $k = 1 - \Delta a / (\theta V) \in [0, 2]$. $\square$

**Unequal slews go beyond 2.** If the aggressor rise time is $t_a$ while the victim's is $t_v$, the same argument gives $|\Delta a| \le \min(\theta V t_v / t_a,\ V)$, so

$$ 1 - \min\!\Big(\frac{t_v}{t_a}, \frac{1}{\theta}\Big) \;\le\; k_{\text{charge}} \;\le\; 1 + \min\!\Big(\frac{t_v}{t_a}, \frac{1}{\theta}\Big), $$

and both limits are reached: by an aggressor that ramps during the whole window when $t_a \ge \theta t_v$, and by one whose whole transition lies inside the window when $t_a \le \theta t_v$. For $\theta = 1/2$ and $t_a \le t_v / 2$ the range is $[-1, 3]$. For example, a victim rising in 100 ps and an aggressor falling in 40 ps that starts at 5 ps finishes its whole swing before the victim reaches 50 percent at 50 ps, so $\Delta a = -V$ and $k = 1 + V / (0.5\, V) = 3$. Kahng, Muddu and Sarto (DAC 2000) showed by analysis of coupled RC lines that the switch factor ranges from $-1$ to 3, not from 0 to 2, once slews and alignment vary.

## Examples and non-examples

**Delay-based factor of a step.** The victim driver is a step from 0 to $V$ at $t = 0$ through a resistance $R$ into $C_g$, and $C_c$ joins the victim to an aggressor that steps from $V$ to 0 at the same instant. Let $x = C_c / (C_g + C_c)$ and $\tau = R (C_g + C_c)$. At $0^+$ charge sharing puts the victim at $-xV$, and then $v(t) = V - (1 + x) V e^{-t/\tau}$, so the 50 percent delay is $\tau \ln(2(1 + x))$. The grounded model gives $R (C_g + k C_c) \ln 2$. Setting the two equal gives

$$ k_{\text{delay}} = 1 + \frac{\ln(1 + x)}{x \ln 2}, $$

which lies strictly between 2 and $1 + 1/\ln 2 \approx 2.443$ for $0 < x < 1$. Both edges are steps, so the slews are equal, and still $k > 2$. The theorem above is about the charge-based factor with ramp waveforms that the coupling does not change. Here the coupling changes the victim waveform itself: it starts below 0.

| $C_g$ | $C_c$ | $x$ | $k_{\text{delay}}$, opposite step | $k_{\text{delay}}$, same direction |
|---|---|---|---|---|
| 1 | 0.001 | 0.001 | 2.442 | $-0.443$ |
| 9 | 1 | 0.1 | 2.375 | $-0.520$ |
| 3 | 1 | 0.25 | 2.288 | $-0.660$ |
| 1 | 1 | 0.5 | 2.170 | $-1$ |
| 1 | 3 | 0.75 | 2.077 | delay 0 for any $k \le -1/3$ |

For the same direction, $v(0^+) = xV$ and the delay is $\tau \ln(2(1 - x))$ when $x < 1/2$, which gives $k = 1 + \ln(1 - x)/(x \ln 2)$. When $x \ge 1/2$ the coupling alone lifts the victim to 50 percent at $0^+$, the delay is 0, and any $k \le -C_g / C_c$ reproduces it.

**Charge-based factor, aligned ramps.** With equal ramps that start together and $\theta = 1/2$: quiet aggressor, $\Delta a = 0$, $k = 1$; same direction, $\Delta a = V/2$, $k = 0$; opposite, $\Delta a = -V/2$, $k = 2$.

**Not a Miller factor: the noise on a quiet victim.** When the victim does not switch, $\Delta v = 0$ and $k$ is undefined. The quantity of interest is then the noise peak, which the [Devgan metric](/devgan-noise-metric/) bounds.

**Not a constant of the layout.** $k$ depends on the waveforms, the alignment and the threshold, not only on the geometry. [Parasitic extraction](/parasitic-extraction/) gives $C_c$; the factor comes from timing.

## Related definitions

- **Coupling capacitance** $C_c$: the capacitance between two nets, given by extraction. The victim's total capacitance in a grounded model is $C_g + k C_c$, and the [Elmore delay](/elmore-delay/) or a [nonlinear delay model](/nonlinear-delay-model/) then uses this value.
- **Crosstalk delay.** The change of the victim delay caused by coupling, the delay noise part of [crosstalk noise](/crosstalk-noise/). A factor $k > 1$ slows the victim, and $k < 1$ speeds it up.
- **Timing windows.** In [static timing analysis](/static-timing-analysis/), the aggressor can switch only inside its window of arrival times. If its window does not overlap the victim's transition, $k = 1$ is safe. Tools iterate: the delays set the windows, and the windows set the factors.
- **Switching power.** The energy drawn from the supply per transition of the victim also depends on what the aggressor does, so [dynamic power](/dynamic-power-dissipation/) estimates that use $C_g + C_c$ are an average over aggressor activity.
- **Common practice.** Many flows use $k = 2$ for setup checks (the victim slowed by an opposite aggressor) and $k = 0$ for hold checks (the victim sped up). By the results above these values are not safe bounds in general when slews differ, and the delay-based factor of a step already exceeds 2.

## References
