---
tag: BSHG1C
kind: definition
slug: dynamic-power-dissipation
name: Dynamic power dissipation
aliases:
- switching power
- CV^2f power
area: eda/power-reliability-and-manufacturability
level: intro
summary: The power a CMOS gate spends charging and discharging its load, P = alpha C V^2 f, with alpha the switching activity, C the capacitance, V the supply and f the clock.
prereqs: [boolean-circuit]
see_also: [switching-activity, leakage-power, glitch-power, transition-density, clock-gating, speed-scaling, clustered-voltage-scaling, power-grid-analysis]
sources:
  - paper: doi:10.1109/4.126534
    title: Anantha P. Chandrakasan, Samuel Sheng and Robert W. Brodersen, Low-power CMOS digital design, IEEE Journal of Solid-State Circuits 27(4), 473 to 484, April 1992
    locator: the section on the sources of power dissipation in CMOS, with the switching component written as the activity times the load capacitance, the square of the supply voltage and the clock frequency
  - paper: doi:10.1109/92.335013
    title: Farid N. Najm, A survey of power estimation techniques in VLSI circuits, IEEE Transactions on VLSI Systems 2(4), 446 to 455, December 1994
    locator: the introduction, which states the average power of a node in terms of its transitions per unit time and its capacitance
  - book: isbn:9780321547743
    title: Neil H. E. Weste and David Money Harris, CMOS VLSI Design, A Circuits and Systems Perspective, 4th edition, Addison-Wesley, 2011
    locator: the chapter on power (dynamic power, the activity factor, short-circuit current and static power)
  - paper: "Harry J. M. Veendrick, Short-circuit dissipation of static CMOS circuitry and its impact on the design of buffer circuits, IEEE Journal of Solid-State Circuits 19(4), 468 to 473, August 1984"
    title: Harry J. M. Veendrick, Short-circuit dissipation of static CMOS circuitry and its impact on the design of buffer circuits, IEEE Journal of Solid-State Circuits 19(4), 468 to 473, August 1984
    locator: the model of the short-circuit current that flows while both networks of a gate conduct
---

Dynamic power dissipation is the power that a CMOS circuit spends to charge and discharge the capacitances of its nodes when they switch. For a node with load capacitance $C$, supply voltage $V_{DD}$ and clock frequency $f$,

$$ P_{\mathrm{dyn}} \;=\; \alpha\, C\, V_{DD}^2\, f, $$

where $\alpha$ is the mean number of rising transitions of the node per clock cycle. The formula follows from conservation of energy alone: each charge from 0 to $V_{DD}$ draws $C V_{DD}^2$ from the supply, and half of it is lost in the pull-up network whatever its resistance. It is the main part of the power of most digital circuits, and the reason why low-power design lowers the supply voltage, the capacitance and the number of transitions. The activity $\alpha$ is the hard part to know; the [switching activity](/switching-activity/) page defines it, and estimators such as [transition density](/transition-density/) compute it. When the circuit does not switch, the power that remains is [leakage power](/leakage-power/).

## Definition

**Model.** A gate drives an output node $y$. All capacitance that $y$ must charge (the drain junctions of the gate, the wire, and the gate inputs of the fanout) is lumped into one capacitor $C$ from $y$ to ground. A static CMOS gate connects $y$ to the supply $V_{DD}$ through its pull-up network or to ground through its pull-down network. The model assumes:

1. The supply is an ideal source at constant voltage $V_{DD}$.
2. Each transition is a full swing, from 0 to $V_{DD}$ or back.
3. The two networks never conduct at the same time, so no current flows straight from the supply to ground (no short-circuit current).
4. No charge is shared with other nodes, the capacitance is constant, and leakage is ignored.

**Definition.** The dynamic power of node $y$ is the average rate at which the supply delivers energy to charge $y$:

$$ P_{\mathrm{dyn}}(y) \;=\; \lim_{T \to \infty} \frac{1}{T}\, E_{\mathrm{supply}}(y, [0, T]). $$

For a synchronous circuit with clock frequency $f$, let $\alpha_{0 \to 1}(y)$ be the mean number of rising transitions of $y$ per clock cycle. The dynamic power of the circuit is the sum over its nodes.

**Theorem.** Under assumptions 1 to 4, each rising transition of $y$ draws exactly $C V_{DD}^2$ from the supply, so

$$ P_{\mathrm{dyn}}(y) \;=\; \alpha_{0 \to 1}(y)\, C\, V_{DD}^2\, f. $$

*Proof.* During a rising transition the pull-up network carries a current $i(t)$ from the supply into the capacitor, and the node voltage $v(t)$ goes from 0 to $V_{DD}$. The charge that enters the capacitor is $\int i\, dt = C V_{DD}$, so the energy that the supply delivers is

$$ E_{\mathrm{supply}} \;=\; \int V_{DD}\, i(t)\, dt \;=\; V_{DD} \cdot C V_{DD} \;=\; C V_{DD}^2. $$

The energy stored in the capacitor at the end is

$$ E_C \;=\; \int v(t)\, i(t)\, dt \;=\; \int_0^{V_{DD}} C\, v\, dv \;=\; \tfrac{1}{2} C V_{DD}^2, $$

using $i = C\, dv/dt$. The difference $C V_{DD}^2 - \frac{1}{2} C V_{DD}^2 = \frac{1}{2} C V_{DD}^2$ is dissipated in the pull-up network. Only the initial and final voltages enter, so this holds for any resistance, linear or not, and any speed of the transition. During a falling transition the supply delivers nothing, and the pull-down network dissipates the stored $\frac{1}{2} C V_{DD}^2$. So a rising transition costs $C V_{DD}^2$ from the supply, a falling one costs 0, and a full cycle up and down dissipates $C V_{DD}^2$ in the gate. In $T$ seconds there are $f T$ clock cycles and on average $\alpha_{0 \to 1} f T$ rising transitions, so the supply delivers $\alpha_{0 \to 1} f T\, C V_{DD}^2$, and dividing by $T$ gives the formula. $\square$

**Conventions.** Rising and falling transitions alternate, so in the long run each is half of all transitions. If $\alpha$ counts all transitions per cycle (the toggle rate), the same power is $P_{\mathrm{dyn}} = \frac{1}{2} \alpha\, C V_{DD}^2 f$. Texts use both forms, and a factor of 2 is a common error when numbers are taken from one text to another. Glitches are transitions too and are included in $\alpha$; see [glitch power](/glitch-power/).

**What is exact and what is fitted.** The formula is exact under the four assumptions. The numbers that enter it are not exact. The wire part of $C$ comes from parasitic extraction, and the pin capacitances and the *internal power* of each cell, which covers the short-circuit current and the charging of nodes inside the cell, come from the characterization of the cell library, as tables fitted to circuit simulation over input slew and output load. The activity $\alpha$ is measured by simulation or estimated.

## Examples and non-examples

**A gate at 1 GHz.** A node with $C = 10$ fF at $V_{DD} = 1$ V, $f = 1$ GHz and $\alpha_{0 \to 1} = 0.1$ dissipates $0.1 \cdot 10^{-14} \cdot 1 \cdot 10^{9} = 1$ µW. A million such nodes dissipate 1 W.

**A clock net.** A clock rises once per cycle, so $\alpha_{0 \to 1} = 1$, the largest value for a signal without glitches. A clock tree with 1 pF of total capacitance at 0.8 V and 2 GHz dissipates $1 \cdot 10^{-12} \cdot 0.64 \cdot 2 \cdot 10^9 = 1.28$ mW. This is why [clock gating](/clock-gating/), which stops the clock of idle registers, is a main low-power technique.

**Random data.** If a bit is a fresh fair coin in each cycle, it rises when it is 0 in one cycle and 1 in the next, so $\alpha_{0 \to 1} = \frac{1}{2} \cdot \frac{1}{2} = \frac{1}{4}$, and its toggle rate is $\frac{1}{2}$.

**Lowering the supply.** The power is quadratic in $V_{DD}$. Halving $V_{DD}$ at the same frequency divides the dynamic power by 4. Since gates are slower at a lower voltage, the frequency must often drop too, which gives about a factor of 8 in power but only 4 in energy per operation. This is the basis of [voltage and frequency scaling](/speed-scaling/) and of [clustered voltage scaling](/clustered-voltage-scaling/).

**Non-example: a node that does not switch.** A node held at 1 has $\alpha = 0$ and no dynamic power, but its gate still draws [leakage power](/leakage-power/).

**Non-example: short-circuit power.** While the input of a gate moves through the middle of its range, both networks conduct briefly and a current flows from the supply to ground without charging $C$. This violates assumption 3. It grows with the input slew, and models such as Veendrick's (1984) estimate it; in a cell library it is part of the fitted internal power.

**Non-example: adiabatic charging.** If the supply itself ramps slowly from 0 to $V_{DD}$ over a time much longer than $R C$, the energy lost in a resistance $R$ is about $(R C / \tau)\, C V_{DD}^2$ for a ramp of length $\tau$, much less than $\frac{1}{2} C V_{DD}^2$. This violates assumption 1, and the formula does not apply to such circuits.

**Non-example: partial swing.** A node that swings only to $V_s < V_{DD}$ while the supply stays at $V_{DD}$ draws $C V_{DD} V_s$ per rising transition, not $C V_{DD}^2$. Low-swing buses use this.

## Related definitions

- **Switching activity.** The factor $\alpha$ of the formula; the [switching activity](/switching-activity/) page defines it per cycle and per transition type, and [transition density](/transition-density/) is the same idea per second.
- **Leakage power.** The static part of the power, which flows without switching; see [leakage power](/leakage-power/). The total power of a CMOS circuit is the sum of the dynamic, the short-circuit and the leakage power.
- **Glitch power.** The part of the dynamic power that comes from transitions that the final logic values do not need; see [glitch power](/glitch-power/).
- **Energy per operation.** For a computation that takes a fixed number of cycles, the energy is $P / f$ times the cycle count, so it does not depend on $f$ but still on $V_{DD}^2$.
- **Effective capacitance.** The product $\alpha C$ summed over all nodes, often called the switched capacitance. RTL [power macromodels](/rtl-power-macromodeling/) estimate it per block from input statistics.

## References
