---
tag: CFBNJE
kind: definition
slug: leakage-power
name: Leakage power
aliases:
- static power
- subthreshold leakage
area: eda/power-reliability-and-manufacturability
level: intro
summary: Power drawn when a CMOS circuit does not switch, mostly by subthreshold and gate leakage currents, which grow exponentially as threshold voltage falls.
prereqs: [dynamic-power-dissipation]
see_also: [power-gating, multi-threshold-voltage-assignment, signal-probability-propagation, compact-thermal-model, shichman-hodges-model, clustered-voltage-scaling, switching-activity, gate-sizing]
sources:
  - paper: doi:10.1109/JPROC.2002.808156
    title: Kaushik Roy, Saibal Mukhopadhyay and Hamid Mahmoodi-Meimand, Leakage current mechanisms and leakage reduction techniques in deep-submicrometer CMOS circuits, Proceedings of the IEEE 91(2), 305 to 327, February 2003
    locator: the sections on the transistor leakage mechanisms (weak inversion current with drain-induced barrier lowering and body effect, gate oxide tunneling, junction leakage) and on the circuit techniques, including transistor stacking
  - book: isbn:9780321547743
    title: Neil H. E. Weste and David Money Harris, CMOS VLSI Design, A Circuits and Systems Perspective, 4th edition, Addison-Wesley, 2011
    locator: the chapter on power (static power and its components) and the chapter on MOS transistor theory (the current below threshold)
  - paper: doi:10.1109/92.335013
    title: Farid N. Najm, A survey of power estimation techniques in VLSI circuits, IEEE Transactions on VLSI Systems 2(4), 446 to 455, December 1994
    locator: the introduction, on the components of power in CMOS circuits
---

Leakage power is the power that a CMOS circuit draws from its supply when no node switches. An ideal transistor that is off carries no current, so an ideal static CMOS gate at rest would draw no power. A real transistor that is off still conducts a small current from drain to source below its threshold voltage, and current also flows through the thin gate oxide and through the reverse-biased junctions. The sum of these currents times the supply voltage is the leakage power, also called static power. The current below threshold grows exponentially as the threshold voltage falls or the temperature rises, so as supply and threshold voltages were scaled down, leakage grew from a negligible part of the power to a large one. Unlike [dynamic power](/dynamic-power-dissipation/), it is drawn in every cycle whether the circuit computes or not, and it depends on the logic state of each gate.

## Definition

**Leakage power.** For a circuit at rest in a state $s$ (the values of all its nodes), the leakage power is

$$ P_{\mathrm{leak}}(s) \;=\; V_{DD} \cdot I_{\mathrm{leak}}(s), $$

where $I_{\mathrm{leak}}(s)$ is the total current from the supply to ground in that state. The average leakage power is the mean of $P_{\mathrm{leak}}(s)$ over the states that the circuit visits. It adds to the dynamic and the short-circuit power to give the total power.

**Components.** For one transistor, the main parts of the current are:

- **Weak inversion current.** The drain to source current of a transistor with gate voltage below threshold. Carriers cross the source barrier by diffusion, so the current follows a Boltzmann law in the gate voltage. A standard compact form is

$$ I_{\mathrm{sub}} \;=\; I_0 \, \exp\!\left(\frac{V_{GS} - V_{T} + \eta V_{DS}}{n\, v_T}\right) \left(1 - e^{-V_{DS}/v_T}\right), \qquad v_T = \frac{k T}{q}, $$

where $v_T \approx 25.9$ mV at 300 K is the thermal voltage, $V_T$ the threshold voltage, $n \ge 1$ the slope factor, $\eta$ the drain-induced barrier lowering (DIBL) coefficient and $I_0$ a current that scales with the width over the length of the transistor. The current falls by a factor of 10 for every $S = n\, v_T \ln 10$ of gate voltage below threshold, the *subthreshold swing*, about 60 mV per decade times $n$ at room temperature.
- **Gate leakage.** Tunneling of carriers through the gate oxide. It grows roughly exponentially as the oxide becomes thinner, and it flows in on-state transistors as well. High-k gate dielectrics reduced it.
- **Junction leakage.** The reverse current of the source and drain junctions, including band-to-band tunneling and gate-induced drain leakage (GIDL) at high fields.

**What is physics and what is fitted.** The exponential dependence on $V_{GS}$ and the factor $1 - e^{-V_{DS}/v_T}$ come from the diffusion current in weak inversion. The parameters $I_0$, $n$, $\eta$ and $V_T$, its temperature coefficient and the body effect are fitted to measurements of each process, and the gate and junction parts use empirical fits. Tools do not evaluate these formulas at the gate level: the cell library gives a leakage value per cell and per input state, fitted by circuit simulation of the cell at each process, voltage and temperature corner. The numbers in the examples below use the formula with illustrative parameters, not data of a real process.

**State dependence.** The leakage of a gate depends on its input values, because they decide which transistors are off and what voltages they see. For a gate with input state probabilities, the average leakage is $\sum_s P(s)\, I_{\mathrm{leak}}(s)\, V_{DD}$, where the state probabilities come from [signal probabilities](/signal-probability-propagation/) of the inputs.

## Examples and non-examples

All numbers below use $n = 1.5$, $\eta = 0.1$, $V_T = 0.3$ V, $V_{DD} = 1$ V and $T = 300$ K unless stated, with $I_0$ held fixed. They show the shape of the effects, not the values of a process.

**Threshold voltage.** With $n = 1.5$ the swing is $1.5 \cdot 25.9 \cdot \ln 10 \approx 89$ mV per decade. Lowering $V_T$ by 100 mV multiplies the current by $10^{100/89} \approx 13$. This is the reason for the trade-off of [multi-threshold voltage assignment](/multi-threshold-voltage-assignment/): low-threshold cells are faster and leak more.

**Temperature.** At 373 K the thermal voltage is 32.1 mV. With $V_T$ fixed, the current of an off transistor with $V_{DS} = 1$ V grows by a factor of 2.7. If $V_T$ also falls by 1 mV per kelvin, a typical size of the effect but here only an assumed value, the factor is about 12. Since leakage heats the chip and heat raises leakage, power and temperature must be solved together, for example with a [compact thermal model](/compact-thermal-model/).

**The stack effect.** Two off NMOS transistors in series, as in the pull-down of a NAND2 with both inputs at 0, leak much less than one. The node $x$ between them settles at the voltage where both carry the same current. The top transistor then has $V_{GS} = -V_x$ and a smaller $V_{DS}$, which reduces its current. Equating the two currents of the formula and solving for $V_x$ by bisection gives $V_x \approx 85$ mV, and the stack leaks $0.091$ times the current of a single off transistor with $V_{DS} = 1$ V, about 11 times less.

**Average leakage of a NAND2.** Take the leakage of a single off transistor with the full $V_{DD}$ across it as the unit, and the same value for NMOS and PMOS. Input state 11 has both PMOS off in parallel, 2 units. States 01 and 10 have one NMOS off, about 1 unit. State 00 has the stack, 0.091 units. With independent inputs that are 1 with probability $p$:

| $p$ | average leakage (units) |
|---|---|
| 0.1 | 0.27 |
| 0.5 | 1.02 |
| 0.9 | 1.80 |

So the same gate leaks about 7 times more in one workload than in another. Setting the inputs of idle blocks to a low-leakage state is a known technique for this reason.

**Non-example: dynamic power.** The energy to charge a node is spent only when it switches; leakage is drawn when nothing switches. A circuit with the clock stopped by [clock gating](/clock-gating/) has no dynamic power in the gated part but keeps its leakage. Only cutting the supply, by [power gating](/power-gating/), removes the leakage.

**Non-example: short-circuit current.** The current that flows while both networks of a gate conduct during an input transition is part of the switching power. It needs a transition and is zero at rest.

## Related definitions

- **Dynamic power.** The power of charging and discharging nodes; see [dynamic power dissipation](/dynamic-power-dissipation/). Leakage grows in relative terms as voltages scale, because lower supply voltages need lower thresholds to keep speed.
- **Power gating and threshold assignment.** [Power gating](/power-gating/) cuts the supply of idle blocks with sleep transistors, which themselves form a stack. [Multi-threshold voltage assignment](/multi-threshold-voltage-assignment/) uses high-threshold cells off the critical paths.
- **Signal probability.** The average leakage of a gate weights its leakage per input state by the probabilities of the states; see [signal probability propagation](/signal-probability-propagation/).
- **Transistor models.** The [Shichman-Hodges model](/shichman-hodges-model/) gives zero current below threshold; leakage needs a model with the weak inversion region.
- **Switching activity.** Leakage does not depend on the [switching activity](/switching-activity/), only on the time spent in each state.

## References
