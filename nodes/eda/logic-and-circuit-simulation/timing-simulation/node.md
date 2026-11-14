---
tag: F3Y8TC
kind: algorithm
slug: timing-simulation
name: Timing simulation
aliases:
- MOTIS timing simulation
- event-driven timing simulation
area: eda/logic-and-circuit-simulation
level: advanced
summary: Chawla, Gummel and Kozak's fast transistor simulation that updates node voltages one at a time with simple models and events, skipping the full Newton solve.
solves: [transient-circuit-analysis]
model: real-ram
complexity:
  vars: {s: the number of time steps, N: the number of circuit nodes, T: the number of transistors}
  time: {worst: "O(s (N + T))", best: "O(s N + T)"}
  space: {extra: "O(N + T)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 1975
  people: [B. R. Chawla, H. K. Gummel, P. Kozak]
  note: MOTIS, the first MOS timing simulator, was described in the IEEE Transactions on Circuits and Systems in December 1975, with a companion paper on its features at the Design Automation Conference of the same year.
prereqs: [transient-circuit-analysis, backward-euler-method, newton-raphson-method, shichman-hodges-model]
see_also: [iterated-timing-analysis, companion-model, modified-nodal-analysis, gauss-seidel-method, mixed-mode-simulation, switch-level-simulation, event-driven-logic-simulation, stiff-ode-problem]
sources:
  - paper: doi:10.1109/TCS.1975.1084003
    title: B. R. Chawla, H. K. Gummel and P. Kozak, MOTIS, an MOS timing simulator, IEEE Transactions on Circuits and Systems CAS-22(12), 901 to 910, 1975
    locator: the node-by-node backward difference update with one Newton step per node, the table models of MOS transistors and the skipping of inactive nodes
  - paper: "P. Kozak, H. K. Gummel and B. R. Chawla, Operational features of an MOS timing simulator, Proceedings of the 12th Design Automation Conference, 95 to 101, 1975"
    title: P. Kozak, H. K. Gummel and B. R. Chawla, Operational features of an MOS timing simulator, Proceedings of the 12th Design Automation Conference, 95 to 101, 1975
    locator: the use of MOTIS on large MOS circuits
  - paper: doi:10.1109/TCAD.1984.1270089
    title: A. R. Newton and A. L. Sangiovanni-Vincentelli, Relaxation-based electrical simulation, IEEE Transactions on Computer-Aided Design 3(4), 308 to 331, 1984
    locator: the analysis of timing simulation as one sweep of nonlinear Gauss-Seidel relaxation, and its relation to iterated timing analysis and waveform relaxation
---

Timing simulation computes the node voltages of a large MOS circuit over time, like a circuit simulator, but at a much lower cost per time step. A circuit simulator solves the whole nonlinear system of the circuit at each time point by Newton's method, with a sparse LU factorization at each iteration. MOTIS (Chawla, Gummel and Kozak, 1975) does not. At each time step it visits the nodes one at a time in a fixed order and moves each node voltage by one Newton step on that node's own equation, using the newest voltages of the other nodes. A node whose surroundings did not move is skipped. This page is in the circuit simulation half of [logic and circuit simulation](/logic-simulation/), at its fast end: it integrates the node equations of [transient circuit analysis](/transient-circuit-analysis/) with [backward Euler](/backward-euler-method/), and borrows selective trace from [event-driven logic simulation](/event-driven-logic-simulation/). There is no delay model as on the logic pages. Delays come out of the integration, from the transistor currents and the node capacitances.

## In plain words

Picture a chain of logic gates. Each wire between gates holds some charge, and the transistors pour current into it or drain it away. A full circuit simulator works out every wire at once at each tick of the clock, which is accurate but slow.

A timing simulator takes the wires one at a time, from the inputs toward the outputs. For each wire it asks how much current flows in now, and how fast that current would change if the wire's voltage moved. From these two numbers it takes one careful step for the wire, then goes to the next wire, which already sees the new value.

Wires far from any activity hardly move. The simulator notices that and leaves them alone until a neighbour moves again.

## The problem

The circuit has $N$ nodes. Node $i$ has a capacitance $C_i$ to ground, and its current $I_i(v)$ is the sum of the currents flowing into it through the channels of the transistors that touch it. Inputs are voltage sources with given waveforms. The node voltages obey $C_i \, dv_i/dt = I_i(v)$ for every $i$, a stiff system of ordinary differential equations. Backward Euler with step $h$ asks, at each time point, for the solution $v^{n+1}$ of

$$\frac{C_i}{h}\left(v_i^{n+1} - v_i^n\right) - I_i(v^{n+1}) = 0 \quad \text{for all } i.$$

In the language of [companion models](/companion-model/), each capacitor becomes a conductance $C_i/h$ with a current source $C_i v_i^n / h$, and the system is the resistive network of [modified nodal analysis](/modified-nodal-analysis/) with only grounded elements. The transistors follow the square-law [Shichman-Hodges model](/shichman-hodges-model/): with overdrive $V_{ov}$ and channel voltage $V_{DS}$, the current is 0 in cutoff, $k(V_{ov} V_{DS} - V_{DS}^2/2)$ in the linear region and $k V_{ov}^2/2$ in saturation. MOTIS itself used tables of the transistor characteristic.

## The algorithm

```pseudo id=main
MOTIS(circuit, init, h, t_end, ε)
L1  v ← the initial node voltages and the input voltages at time 0; every node is awake
L2  for t = h, 2h, ..., t_end
L3      set each input to its value at t; wake the nodes that a moved input feeds
L4      for each node i in the fixed order
L5          if i is asleep: skip it, its voltage stays
L6          (I, D) ← the current into i and its derivative in v_i, at the newest voltages
L7          v_i ← v_i + h I / (C_i − h D)
L8          if v_i moved by more than ε: wake i and the nodes it feeds, later in this step and in the next
L9      the awake nodes of the next step are those woken in this step
L10     record the voltages at t
L11 return the waveforms
```

Line L7 is one Newton step on the backward Euler equation of node $i$ alone, started from its old voltage $v_i^n$. With $g(x) = C_i (x - v_i^n)/h - I_i(\ldots, x, \ldots)$, the step $x_1 = v_i^n - g(v_i^n)/g'(v_i^n)$ is exactly $v_i^n + h I / (C_i - h D)$. The nodes that come earlier in the order already have their values at $t$, and the later ones still have their values at $t - h$. So one time step is one sweep of nonlinear [Gauss-Seidel](/gauss-seidel-method/) iteration with one Newton step per node.

The order matters. MOTIS orders the nodes from the inputs toward the outputs, so that a gate sees its input voltage at the new time. When the current into each node depends only on its own voltage and on nodes earlier in the order, as in a chain of gates with grounded capacitors, the backward Euler system is lower triangular, and a sweep that solves each node equation exactly gives the backward Euler solution itself.

With $\varepsilon = 0$ every node is updated at every step. With $\varepsilon > 0$, a node sleeps once its voltage moves by no more than $\varepsilon$ in a step, until a node or input that it reads moves by more than $\varepsilon$.

## Example

A chain of four CMOS inverters with $V_{DD} = 1.8$ V, threshold 0.5 V, $k = 200\ \mu\mathrm{A/V^2}$ for both transistor types and $C = 10$ fF on each output. The input rises from 0 to 1.8 V between 0.10 and 0.15 ns, and $h = 1$ ps. When $y_1$ is still at 1.8 V and the input has reached 1.8 V, the n transistor is saturated and the p transistor is off, so $I = -0.5 \cdot 200 \cdot 1.3^2 = -169\ \mu$A and $D = 0$, and line L7 moves $y_1$ by $hI/C = -16.9$ mV. The waveforms (volts):

| t (ns) | $y_1$ | $y_2$ | $y_3$ | $y_4$ |
| --- | --- | --- | --- | --- |
| 0.10 | 1.800 | 0.000 | 1.800 | 0.000 |
| 0.14 | 1.719 | 0.000 | 1.800 | 0.000 |
| 0.16 | 1.420 | 0.000 | 1.800 | 0.000 |
| 0.18 | 1.084 | 0.002 | 1.800 | 0.000 |
| 0.20 | 0.777 | 0.031 | 1.800 | 0.000 |
| 0.25 | 0.273 | 0.370 | 1.800 | 0.000 |
| 0.30 | 0.082 | 1.007 | 1.769 | 0.000 |

The outputs cross 0.9 V at 0.1916, 0.2920, 0.3944 and 0.4969 ns. A classical [Runge-Kutta](/classical-runge-kutta-4/) reference with a step of 0.05 ps gives 0.1921, 0.2926, 0.3952 and 0.4979 ns, so each crossing is within 1 ps, and the largest voltage difference on any node is 13 mV.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows three facts exactly.

1. If no transistor touching node $i$ has its gate on node $i$, then $\partial I_i / \partial v_i \le 0$ for the square-law model. So $g'(x) \ge C_i/h > 0$: the node equation has exactly one solution, and the denominator of line L7 is at least $C_i$ for every step size.
2. If the order makes the system lower triangular, a sweep that solves each node equation exactly gives the backward Euler solution, with no further iteration.
3. One Newton step from $v_i^n$ lands within $L h^3 I^2 / (2 C_i^3)$ of the exact solution of the node equation (with the other voltages fixed), where $I$ is the current at the start of the step and $L$, at most the sum of the $k$ of the transistors at the node, bounds how fast $\partial I_i/\partial v_i$ can change.

The rest is measured, not proved. The tests compare with a full backward Euler solve with Newton's method on the whole system and with a Runge-Kutta reference at a step 20 times finer:

- The sweep with exact node solves agrees with the full backward Euler Newton solution to $1.2 \cdot 10^{-12}$ V on the inverter chain (the test asks for $10^{-9}$).
- One Newton step per node stays within 1.2 mV of full backward Euler at $h = 2$ ps.
- Against the reference, the largest error is 13 mV at $h = 1$ ps on the chain and 12 mV on a NAND gate whose internal stack node couples both ways, and every 0.9 V crossing is within 1.5 ps (the stated tolerances are 20 mV and 1.5 ps).
- The error falls by factors of 2.08, 1.98, 2.03 and 2.01 as $h$ halves from 8 ps to 0.5 ps: first order, as backward Euler is.

Whether the Gauss-Seidel sweep converges, or how large its error is, when nodes couple both ways through floating capacitors or pass transistors, depends on the circuit; MOTIS gives no bound, and [iterated timing analysis](/iterated-timing-analysis/) repeats the sweep until it converges.

## Complexity

Each node update reads the transistors at the node, so a sweep costs $O(N + T)$, and $s$ steps cost $O(s(N + T))$. No matrix is built or factored. A full circuit simulator pays for a sparse LU factorization at each Newton iteration, which grows faster than linearly in $N$ for most circuits, and for several iterations per time point. With event skipping, a sleeping node costs only the test of line L5, so the cost of a quiet step is $O(N)$, and an implementation that keeps the awake nodes in a queue makes it proportional to the activity. On a chain of eight inverters with $h = 1$ ps over 1 ns, $\varepsilon = 10^{-4}$ V cut the node updates from 8000 to 3319, with a largest change of 3.9 mV from the unskipped run. These numbers are measured.

## Properties

- **No matrix.** Each step costs a sweep over the nodes. Memory is linear in the circuit size.
- **Implicit per node.** The step size is not limited by the stiffness of a single node, since the update is backward Euler for that node.
- **First order.** The accuracy is that of backward Euler, and the step size must be small against the transition times.
- **Order dependent.** Feedback and two-way coupling are taken with a delay of one step for the nodes that come later in the order.
- **Event driven.** Inactive parts of the circuit cost almost nothing, which is where most of the speed on large digital circuits comes from.

## Variants and improvements

- **Iterated timing analysis.** SPLICE repeats the Gauss-Seidel sweep at each time point until the voltages converge, which removes the error from two-way coupling; see [iterated timing analysis](/iterated-timing-analysis/).
- **Waveform relaxation.** Solve each subcircuit for a whole time window, then exchange waveforms and repeat. It lets each subcircuit use its own step size.
- **Table models.** MOTIS and its successors precompute transistor currents in tables to avoid evaluating the model.
- **Mixed mode.** Simulate parts of the circuit at timing level and the rest at gate level, as in [mixed-mode simulation](/mixed-mode-simulation/).
- **Fast SPICE.** Later commercial simulators combine partitioning, table models, event skipping and per-partition time steps on the same ideas.

## When to use it

Use timing simulation for large digital MOS circuits where gate-level delays are not accurate enough and a full circuit simulator is too slow: memory arrays, custom datapaths, clock trees, checks of the waveforms and delays of whole blocks. Do not use it where strong two-way coupling decides the behavior, as in sense amplifiers, analog circuits and oscillators of coupled nodes, or where accuracy must be guaranteed; use a full transient circuit simulation there.

## Pitfalls

- **Too large a skip threshold.** A node is put to sleep when it moves slowly, and nothing may wake it again. In the tests, $\varepsilon = 0.01$ V on the inverter chain froze the first output at 0.46 V after the input ramp ended, and the edge never reached the end of the chain.
- **A bad order.** If a gate comes before its input node, it sees the input one step late, and with feedback the delay adds up.
- **Two-way coupling.** Floating capacitors and pass transistors couple nodes in both directions. One sweep does not resolve them, so the waveforms can be wrong by much more than the step error.
- **Too large a step.** The update is defined for every step size, but backward Euler damps fast edges and shifts delays when $h$ is not small against the transition time.

## Implementations

## History

Chawla, Gummel and Kozak at Bell Laboratories built MOTIS and described it in 1975, at the Design Automation Conference and in the IEEE Transactions on Circuits and Systems. It brought transistor-level timing to circuits far larger than a circuit simulator of the time could handle. Newton's SPLICE (1979) combined timing and logic simulation with events, and Newton and Sangiovanni-Vincentelli (1984) explained timing simulation as one sweep of a nonlinear relaxation method, which led to iterated timing analysis and waveform relaxation. The fast SPICE simulators of the 1990s and later build on these methods.

## References
