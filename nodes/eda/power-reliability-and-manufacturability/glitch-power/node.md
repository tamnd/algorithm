---
tag: NQ600F
kind: concept
slug: glitch-power
name: Glitch power
aliases:
- spurious transitions
- hazard power
area: eda/power-reliability-and-manufacturability
level: core
summary: Power wasted by extra transitions that appear when inputs of a gate arrive at different times, which zero-delay power estimates miss.
prereqs: [switching-activity, dynamic-power-dissipation]
see_also: [inertial-and-transport-delay, event-driven-logic-simulation, bdd-switching-activity-estimation, transition-density, retiming, gate-sizing, operand-isolation, timing-simulation]
sources:
  - paper: doi:10.1109/4.126534
    title: Anantha P. Chandrakasan, Samuel Sheng and Robert W. Brodersen, Low-power CMOS digital design, IEEE Journal of Solid-State Circuits 27(4), 473 to 484, April 1992
    locator: the discussion of spurious transitions (glitching) and of how the structure of a circuit, chain or tree, changes them
  - paper: doi:10.1109/DAC.1992.227826
    title: Abhijit Ghosh, Srinivas Devadas, Kurt Keutzer and Jacob White, Estimation of average switching activity in combinational and sequential circuits, Proceedings of the 29th ACM/IEEE Design Automation Conference, 253 to 259, 1992
    locator: the general delay model, under which the estimated activity includes the transitions caused by unequal path delays
  - paper: doi:10.1109/92.335013
    title: Farid N. Najm, A survey of power estimation techniques in VLSI circuits, IEEE Transactions on VLSI Systems 2(4), 446 to 455, December 1994
    locator: the discussion of delay models and glitches in power estimation
---

Glitch power is the part of the [dynamic power](/dynamic-power-dissipation/) of a circuit that is spent on transitions that the logic function does not need. When the inputs of a gate change at different times, because they come through paths with different delays, the gate output can change several times in one clock cycle before it settles. A node whose final value is the same as before may still pulse to the other value and back, and a node that must change once may change three times. Each extra transition charges or discharges the node capacitance like a needed one. These extra transitions are glitches (also called spurious transitions or hazards), and their power is glitch power. Zero-delay estimates of [switching activity](/switching-activity/) count at most one transition per node per cycle, so they do not see glitch power at all. In arithmetic circuits such as adders and multipliers, glitches can be a large part of the power.

## In plain words

A gate does not wait for all its inputs. It reacts to each input as soon as the change arrives. If one input changes early and another late, the output first reacts to the early one, then to the late one.

Think of an XOR gate whose two inputs both flip. The right answer is no change. But if one flip arrives first, the output flips, and when the second arrives it flips back. The wire switched twice for nothing, and each switch costs energy.

In a long chain of gates, such early and late arrivals are everywhere. The deeper a gate is, and the more its input paths differ in length, the more it glitches. Making the paths equal in length, or cutting long chains with registers, removes most of these useless switches.

## The idea

**Where the extra transitions come from.** Fix a delay model and a pair of consecutive input vectors $x \to x'$, with all inputs changing at time 0. Each node $y$ has a waveform $y(t)$ that starts at $f_y(x)$ and ends at $f_y(x')$. Let $N_y$ be its number of transitions. The *functional* transition count is $[f_y(x) \ne f_y(x')]$, which is what the zero-delay model counts. The glitch count of $y$ is the difference

$$ G_y \;=\; N_y - [f_y(x) \ne f_y(x')], $$

and glitch power is $\frac{1}{2} \sum_y C_y V_{DD}^2 f \cdot E[G_y]$ for clock frequency $f$. This is a part of the dynamic power, not a different kind of power; this page is about that part only.

**Glitches come in pairs.** For every node and every pair of vectors, $G_y$ is even and nonnegative. *Proof.* A 0-1 waveform that starts at $a$ and ends at $b$ changes value an even number of times if $a = b$ and an odd number if $a \ne b$, since each transition flips the value. So $N_y \equiv [a \ne b] \pmod 2$, and $N_y \ge [a \ne b]$. $\square$ A glitch on a node whose value does not change is a pulse, two transitions; a node that must change changes 1, 3, 5, ... times. So the energy of one glitch is that of a full charge and discharge, $C V_{DD}^2$.

**Balanced paths remove glitches under transport delay.** Under the transport delay model (see [inertial and transport delay](/inertial-and-transport-delay/)), a gate with delay $d$ outputs at time $t$ its function of the input values at time $t - d$. Suppose the circuit is *balanced*: for every gate, all its fanins have the same arrival time, so every path from the primary inputs to a node $y$ has the same delay $D_y$. Then every node makes at most one transition per input change. *Proof.* By induction in topological order, $y(t) = f_y(x)$ for $t < D_y$ and $y(t) = f_y(x')$ for $t \ge D_y$. For a primary input $D = 0$ and this is the input step. For a gate $y = g(z_1, \ldots, z_k)$ with delay $d$, all $z_j$ have the same $D_{z_j} = D_y - d$, so at time $t - d$ they all hold their old values if $t < D_y$ and all hold their new values if $t \ge D_y$, which gives $y(t) = g(f_{z_1}(x), \ldots) = f_y(x)$ or $f_y(x')$. $\square$ Without balance this fails: the XOR example above has paths of different length to one gate. The proof also needs all inputs to switch at the same instant; inputs that arrive from registers with different delays are paths of different length too.

**Inertial delay filters short pulses.** A real gate does not pass a pulse that is shorter than about its own delay; the [inertial delay](/inertial-and-transport-delay/) model drops such pulses. So the transport model overestimates glitches, especially in deep logic where pulses get narrow. Power simulators therefore use [event-driven logic simulation](/event-driven-logic-simulation/) with inertial delays from timing data, or [timing simulation](/timing-simulation/), to count glitches.

**How estimators treat glitches.** A zero-delay estimator, such as zero-delay [BDD-based estimation](/bdd-switching-activity-estimation/) or simulation, gives the functional activity only. The same BDD method with symbolic simulation over time steps gives the exact expected transitions under transport delay, glitches included. [Transition density](/transition-density/) counts each input transition that passes a gate as an output transition, so it includes glitches between independent inputs but assumes they are separated in time.

## Examples

The numbers below are exact expected values for fresh uniform random input vectors in every cycle and unit transport delay on every gate, computed by symbolic simulation with BDDs. They are toy circuits, not measurements of real designs, and real gates with inertial delay would filter some of these pulses.

**An XOR gate with skew.** Let $y = a \oplus b$, where $b$ reaches the gate one unit later than $a$. With fresh random inputs, $a$ and $b$ both flip in a quarter of the cycles. Then $y$ flips when $a$ arrives and flips back when $b$ arrives: a glitch of two transitions while the zero-delay value does not change.

**Parity: chain versus tree.** The parity of 8 inputs can be computed by a chain of 7 XOR gates, $c_k = c_{k-1} \oplus x_k$, or by a balanced tree of 7 XOR gates. Under zero delay every gate has activity $1/2$ in both, 3.5 transitions per cycle in total. Under unit delay:

| structure | transitions per cycle, zero delay | transitions per cycle, unit delay | output, unit delay |
|---|---|---|---|
| chain | 3.5 | 14 | 3.5 |
| tree | 3.5 | 3.5 | 0.5 |

In the chain, the input $x_j$ with $j \ge 1$ reaches gate $c_k$ after $k - j + 1$ units, and $x_0$ arrives together with $x_1$, so the new values arrive at $c_k$ in $k$ separate steps, each a flip with probability $1/2$, and $c_k$ makes $k/2$ transitions on average. The chain spends 4 times the zero-delay power, three quarters of it on glitches. The tree is balanced, so by the theorem above it has no glitches.

**Ripple-carry adders.** In a ripple-carry adder the carry of bit $i$ is ready only after the carries below it, so the high sum bits change first on the propagate signal and later on the carry. For a 4-bit adder (17 gates), the zero-delay activity is $1875/256 \approx 7.32$ transitions per cycle and the unit-delay activity is $617/64 \approx 9.64$, so glitches are 24 percent of all transitions. The top sum bit makes $79/64 \approx 1.23$ transitions per cycle where the zero-delay model gives $1/2$. For a 5-bit adder the share of glitches is 29 percent; it grows with the width, because the high bits get more late carry arrivals.

**$y = a \wedge \bar a$.** With a delay on the inverter, each rising edge of $a$ makes a pulse on $y$, a hazard in the classic sense. The function is the constant 0, so all of its power is glitch power.

## Where it is used

- **Power estimation.** Glitches decide how far a zero-delay estimate is from the real power. Sign-off power analysis uses activity from gate-level simulation with timing, and [Monte Carlo power estimation](/monte-carlo-power-estimation/) can use any such simulator.
- **Path balancing.** Inserting buffers or choosing structures so that the inputs of each gate arrive together removes glitches, as in the parity tree. The buffers add capacitance, so balancing pays only where the glitch activity is high.
- **Registers and retiming.** A register passes one clean value per cycle, so it stops glitches from spreading. Pipelining or [retiming](/retiming/) a deep datapath shortens the logic between registers and lowers the glitch power, at the cost of register power.
- **Gate sizing and delay tuning.** [Gate sizing](/gate-sizing/) changes delays and can be used to equalize the arrival times at the inputs of high-activity gates.
- **Operand isolation and guarding.** [Operand isolation](/operand-isolation/) holds the inputs of an unused block steady, which stops both functional and glitch transitions inside it.
- **Arithmetic design.** Multipliers, adders and multiply-accumulate units are chosen and laid out with glitches in mind, since their deep, unbalanced carry and partial-product logic produces most of the glitches of a typical datapath.

## References
