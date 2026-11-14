---
tag: TSB6K9
kind: concept
slug: crosstalk-noise
name: Crosstalk noise
aliases:
- capacitive coupling noise
- coupling noise
area: eda/power-reliability-and-manufacturability
level: core
summary: Unwanted voltage on a net caused by a switching neighbour through coupling capacitance, which can create glitches or change delay, and which grows as wires get closer.
prereqs: [parasitic-extraction, rc-tree]
see_also: [devgan-noise-metric, miller-coupling-factor, static-timing-analysis, elmore-delay, asymptotic-waveform-evaluation, prima, power-grid-analysis]
sources:
  - paper: "Kenneth L. Shepard and Vinod Narayanan, Noise in deep submicron digital design, IEEE/ACM International Conference on Computer-Aided Design, 524 to 531, November 1996"
    title: Kenneth L. Shepard and Vinod Narayanan, Noise in deep submicron digital design, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 524 to 531, 1996
    locator: the sources of noise in digital circuits, among them capacitive coupling, and the idea of a static noise analysis of the whole chip
  - paper: "Takayasu Sakurai, Closed-form expressions for interconnection delay, coupling, and crosstalk in VLSIs, IEEE Transactions on Electron Devices 40(1), 118 to 124, January 1993"
    title: Takayasu Sakurai, Closed-form expressions for interconnection delay, coupling, and crosstalk in VLSIs, IEEE Transactions on Electron Devices 40(1), 118 to 124, January 1993
    locator: the closed-form height of the crosstalk voltage between two coupled distributed RC lines
  - paper: "Anirudh Devgan, Efficient coupled noise estimation for on-chip interconnects, IEEE/ACM International Conference on Computer-Aided Design, 147 to 151, November 1997"
    title: Anirudh Devgan, Efficient coupled noise estimation for on-chip interconnects, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 1997
    locator: the linear-time noise bound for RC trees used to screen nets
  - paper: "Andrew B. Kahng, Sudhakar Muddu and Egino Sarto, On switch factor based analysis of coupled RC interconnects, Proceedings of the 37th Design Automation Conference (DAC), 79 to 84, 2000"
    title: Andrew B. Kahng, Sudhakar Muddu and Egino Sarto, On switch factor based analysis of coupled RC interconnects, Proceedings of the 37th ACM/IEEE Design Automation Conference, 79 to 84, June 2000
    locator: the effect of coupling on delay and the range of the switch factor
  - book: isbn:9780130909961
    title: Jan M. Rabaey, Anantha Chandrakasan and Borivoje Nikolic, Digital Integrated Circuits, A Design Perspective, 2nd edition, Prentice Hall, 2003
    locator: the chapter on coping with interconnect, section on capacitive crosstalk (floating and driven victims, and the ways to reduce crosstalk)
---

Crosstalk noise is the voltage that one net, the *aggressor*, induces on a neighbor net, the *victim*, through the capacitance between the two wires. This page covers capacitive coupling on chip, which is the dominant form for most signal wires. Inductive coupling also exists on long wide wires and buses, and it is not treated here. Crosstalk has two effects: a glitch on a victim that should stay quiet, called *functional noise*, and a change in the delay of a victim that switches at the same time, called *delay noise*.

## In plain words

Two wires that run side by side act like the two plates of a small capacitor. When one wire changes its voltage quickly, it pushes a little charge onto the other wire, and the other wire's voltage moves too.

If the second wire should stay at 0, it gets a short bump. A small bump does no harm, but a large one can be read as a 1 by the gate at the end of the wire, and the chip computes a wrong value.

If the second wire is switching at the same moment, the push either helps it or holds it back. It then arrives earlier or later than the timing tools expected, and the chip can fail at its target clock speed.

Wires on modern chips are tall, thin and close together, so this effect has grown with each new process.

## The idea

Model the victim at one point as a node with capacitance $C_g$ to ground and $C_c$ to the aggressor, and let the aggressor move by $\Delta V_a$.

**Floating victim: charge sharing.** If nothing drives the victim, its charge is conserved. The charge on the node is $C_g v + C_c (v - a)$. If it stays constant while $a$ changes by $\Delta V_a$, then

$$ \Delta v = \frac{C_c}{C_c + C_g}\, \Delta V_a . $$

This is the largest bump the victim can get from one aggressor transition, because any driver can only pull the victim back toward its held value. It does not depend on how fast the aggressor switches.

**Driven victim.** A real victim is held by its driver, modeled as a resistance $R$ to its quiet value. For an aggressor ramp of rise time $t_r$, the node obeys $(C_g + C_c) v' + v / R = C_c a'$, and its peak, at the end of the ramp, is

$$ v_{\max} = R\, C_c\, \frac{\Delta V_a}{t_r} \left(1 - e^{-t_r / \tau}\right), \qquad \tau = R\,(C_g + C_c) . $$

Slow aggressors give a peak close to $R C_c \Delta V_a / t_r$, which shrinks as $t_r$ grows. Fast aggressors approach the charge sharing limit. A stronger driver, with a smaller $R$, lowers the peak. On a real net with distributed resistance and several aggressors, the [Devgan metric](/devgan-noise-metric/) gives a proved upper bound of the same form, $\sum_k R_{ik} C_{c,k}\, \Delta V_a / t_r$, over an [RC tree](/rc-tree/).

**Switching victim: delay noise.** When the victim switches too, the charge that its driver must move through $C_c$ depends on the aggressor. An aggressor that switches the opposite way roughly doubles the effective coupling, and one that switches the same way removes it. Delay tools model this by grounding $C_c$ with a [Miller coupling factor](/miller-coupling-factor/) $k$, so the victim sees $C_g + k C_c$. The factor is 1 for a quiet aggressor, about 0 or 2 for aligned edges of equal slew, and can lie outside $[0, 2]$ when slews differ.

**Whether a bump matters.** A glitch causes an error only if it is high and wide enough to switch the receiving gate, and if the wrong value is then latched or propagated. The receiver's noise immunity is described by the pulse heights and widths that it rejects. Noise analysis compares each victim's bump with these limits.

**Timing windows.** An aggressor can switch only inside the window of arrival times that [static timing analysis](/static-timing-analysis/) gives for it. Aggressors whose windows cannot overlap the victim's sensitive time are not added together. Since the delays depend on the coupling and the windows depend on the delays, tools iterate the two analyses until the windows stop changing.

## Examples

Units are kΩ, fF, ps and V. Take $C_g = C_c = 10$ fF and an aggressor that switches by 1 V.

| victim | aggressor rise time | $\tau$ (ps) | peak noise (V) |
|---|---|---|---|
| floating | any | none | $10/20 = 0.500$ |
| $R = 1$ | 2 ps | 20 | 0.476 |
| $R = 1$ | 20 ps | 20 | 0.316 |
| $R = 1$ | 200 ps | 20 | 0.050 |
| $R = 0.25$ (4 times stronger driver) | 20 ps | 5 | 0.123 |

The bound $R C_c \Delta V_a / t_r$ without the factor in parentheses gives 5.0, 0.50, 0.050 and 0.125 V for the four driven rows. It is tight for slow edges and very loose for the 2 ps edge, where the charge sharing limit of 0.5 V is the better bound.

**Delay noise of the same pair.** Let the victim be driven by a step through $R = 1$ kΩ. With a quiet aggressor its 50 percent delay is $R (C_g + C_c) \ln 2 = 13.86$ ps. If the aggressor steps the opposite way at the same instant, the victim starts at $-0.5$ V by charge sharing, and its delay becomes $20 \ln 3 = 21.97$ ps, which a grounded model reproduces with $k \approx 2.17$. If the aggressor steps the same way, the victim jumps to 0.5 V at once, and its 50 percent delay is 0.

**Mitigation, by effect on the formula.**

- *Spacing* the wires lowers $C_c$.
- *Shielding*, a grounded wire between the two, turns most of $C_c$ into $C_g$, which removes the coupling at the cost of a track.
- *Upsizing the victim driver* lowers $R$. *Inserting buffers* cuts a long victim into short segments, each with its own small $R$ and coupling length.
- *Slowing the aggressor* raises $t_r$, at the cost of the aggressor's own delay.
- *Reordering or staggering* bus wires, and *timing windows* that separate switching times, reduce the coupling that can act at once.

## Where it is used

- **Static noise analysis.** Every net of a chip is checked for functional noise after routing and [parasitic extraction](/parasitic-extraction/). A fast bound such as the [Devgan metric](/devgan-noise-metric/) screens the nets, and only the suspicious ones get a transient analysis with reduced models such as [AWE](/asymptotic-waveform-evaluation/) or [PRIMA](/prima/).
- **Signal integrity aware timing.** Delay noise enters [static timing analysis](/static-timing-analysis/) through coupling factors and timing windows, so that setup and hold checks account for the worst switching neighbors.
- **Routing and buffering.** Routers limit the parallel run length of sensitive nets, add spacing or shields, and buffer insertion tools use noise as a constraint next to delay.
- **Power analysis.** The energy a net draws per transition depends on what its neighbors do, so coupling also enters [dynamic power](/dynamic-power-dissipation/) estimates.
- **Not the same as supply noise.** Voltage drop and ground bounce on the supply network are a different noise source, analyzed by [power grid analysis](/power-grid-analysis/). Noise analysis tools combine the two in the noise margin of each receiver.

## References
