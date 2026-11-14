---
tag: BBKYW7
kind: algorithm
slug: cycle-based-simulation
name: Cycle-based simulation
aliases:
- cycle simulation
area: eda/logic-and-circuit-simulation
level: core
summary: Simulates a synchronous design one clock cycle at a time, evaluating the logic between registers once per cycle in levelized order, with no timing inside the cycle.
solves: [logic-simulation]
model: word-ram
complexity:
  vars: {G: the number of gates, P: the number of gate input pins, N: the number of nets, T: the number of clock cycles}
  time: {worst: "O(N + P + T (G + P))", best: "O(N + P + T (G + P))"}
  space: {extra: "O(N + P)"}
properties: {deterministic: true, exact: true, recursive: false}
prereqs: [logic-simulation, compiled-code-logic-simulation, mealy-machine]
see_also: [event-driven-logic-simulation, topological-sort, setup-and-hold-constraints, static-timing-analysis, moore-machine, scan-design, time-frame-expansion, multi-valued-logic-simulation]
sources:
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter Logic Simulation (compiled simulation of synchronous circuits, levelization, and the comparison with event-driven simulation)
  - paper: doi:10.1109/TCAD.1987.1270308
    title: Zeev Barzilai, J. Lawrence Carter, Barry K. Rosen and Joseph D. Rutledge, HSS, a high-speed simulator, IEEE Transactions on Computer-Aided Design 6(4), 601 to 617, 1987
    locator: the simulation of the cycle-free logic between latches as compiled code, once per clock
  - paper: "Gregory F. Pfister, The Yorktown Simulation Engine, introduction, Proceedings of the 19th Design Automation Conference, 51 to 54, 1982"
    title: G. F. Pfister, The Yorktown Simulation Engine, introduction, Proceedings of the 19th Design Automation Conference, 51 to 54, 1982
    locator: a hardware engine that evaluates the whole logic of a synchronous design once per machine cycle from a fixed program
---

Cycle-based simulation runs a synchronous design one clock cycle at a time. The registers cut every loop, so the logic between them has no loops and can be put in levelized order once. In each cycle the simulator evaluates every gate once, in that order, from the primary inputs of the cycle and the register values, and then all registers take the values at their data inputs together, as at a clock edge. This page is in the logic simulation half of [logic and circuit simulation](/logic-simulation/). The delay model is zero delay inside the cycle: the clock edge is the only time, and nothing is computed about when a signal settles. That is enough when [static timing analysis](/static-timing-analysis/) has already shown that every path meets the [setup constraint](/setup-and-hold-constraints/), and it lets the simulator drop the event queue and run the logic as [compiled code](/compiled-code-logic-simulation/).

## In plain words

In a synchronous design all registers change at the clock edge. Between two edges the gates do their work, and if the design is timed right, every signal has its final value before the next edge.

So the simulator does not track time inside the cycle. For each cycle it sets the inputs, runs through the gates once in an order where each gate comes after the gates it reads, and copies the new values into the registers. One cycle costs one evaluation per gate, whatever the delays are.

What it cannot show is anything that happens between the edges: glitches, races, or a path that is too slow.

## The problem

The input is a synchronous design with one clock: primary inputs, D flip-flops $r$ with an output $q_r$, a data input $d_r$ and an initial value, gates, and a list of primary outputs. Every loop of gates must pass through a register. The design is a [Mealy machine](/mealy-machine/): the state $s$ is the vector of register values, and for an input vector $x$ the logic gives the next state $\delta(s, x)$, the values of the $d_r$, and the outputs $\lambda(s, x)$. Given $s_0$ and inputs $x_1, \ldots, x_T$, the output is $\lambda(s_{k-1}, x_k)$ for each cycle $k$, where $s_k = \delta(s_{k-1}, x_k)$.

## The algorithm

```pseudo id=main
CYCLE-SIM(design, s0, x_1, ..., x_T)
L1  cut every register r: q_r becomes an input of the logic L and d_r an output of L
L2  levelize the gates of L by Kahn's algorithm; stop with "loop" if a loop of gates is not cut by a register
L3  s ← s0
L4  for k = 1 to T do
L5      evaluate every gate of L once, in level order, on the inputs x_k and the register values s
L6      record the values of the primary outputs for cycle k
L7      s ← the values of d_r for all registers r, all at once
L8  return the recorded outputs and s
```

Line L7 must take all new register values from the values computed in L5 before it writes any of them. Writing the registers one by one, so that a later register reads the new value of an earlier one, is the classic bug of a shift register simulated in the wrong order.

Line L5 can be the bit-parallel program of [compiled-code simulation](/compiled-code-logic-simulation/). Then each lane of a word runs its own copy of the design, for example with a different random seed of the test bench.

## Example

A serial adder adds two numbers given least significant bit first. It has inputs $a$ and $b$, one register $c$ for the carry, initial value 0, and the gates $x_1 = a \oplus b$, $s = x_1 \oplus c$, $g_1 = ab$, $g_2 = x_1 c$ and $c' = g_1 + g_2$, which is the data input of $c$. Add $6 = 0110_2$ and $7 = 0111_2$, so $a = 0, 1, 1, 0, 0$ and $b = 1, 1, 1, 0, 0$ in cycles 1 to 5.

| cycle | $a$ | $b$ | $c$ | $x_1$ | $s$ | $g_1$ | $g_2$ | $c'$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| 2 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| 3 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 1 |
| 4 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The sum bits are $1, 0, 1, 1, 0$, which is $01101_2 = 13$. Each cycle evaluates five gates in the order $x_1, g_1$ (level 1), $s, g_2$ (level 2) and $c'$ (level 3), so 25 gate evaluations for the whole run.

The tests also show what the method gives up. In a design where $q' = \mathrm{NOT}(\mathrm{NOT}(\mathrm{NOT}(q)))$, the logic has depth 3. A unit-delay simulation with a clock period of 4 time units samples settled values and agrees with the cycle-based run. With a period of 2 it samples values that have not settled, and the two runs differ. The cycle-based run cannot see this setup violation.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows two things. First, line L5 computes $\delta(s, x_k)$ and $\lambda(s, x_k)$ exactly, by the argument of compiled-code simulation on the loop-free logic, so by induction on $k$ the run gives the outputs and states of the Mealy machine. Second, it relates the result to timed behavior: if every gate has delay 1 and the clock period is larger than the depth $D$ of the logic, a net of level $\ell$ has its final value from $\ell$ time units after the edge, so the values sampled just before the next edge are the values of the cycle-based run. The tests check the first claim against an explicit next-state table built by direct evaluation of every pair of state and input, and the second against a unit-delay step simulation with period $D + 1$, on random designs.

## Complexity

Levelization costs $O(N + P)$ once. Each cycle evaluates each gate once and reads each input pin once, so it costs $O(G + P)$, and $T$ cycles cost $O(T(G + P))$. The memory is the netlist and one value per net, $O(N + P)$. With bit-parallel words of $W$ bits, $W$ independent runs cost the same as one.

An event-driven simulator of the same design spends work only on the nets that change, but pays for the queue and for every glitch inside the cycle. In designs where a large part of the logic is active in every cycle, cycle-based simulation is faster, by a factor that depends on the activity and on the glitches it avoids; this page does not measure it.

## Properties

- **Exact at the clock edges** for designs that meet their timing, and blind between them.
- **Deterministic order.** Races between registers cannot appear, since all registers update together at L7. A real circuit with clock skew or a hold violation can still have such a race.
- **No initialization by time.** The initial state is given. With unknown initial state the values must be X, which needs [multi-valued logic](/multi-valued-logic-simulation/) and brings X pessimism.

## Variants and improvements

- **Multiple clocks.** With several clocks of fixed ratio, the simulator steps through the clock edges in time order and at each edge evaluates the logic that feeds the registers of that clock.
- **Event-driven cycles.** Evaluate only the cones whose inputs changed since the last cycle. This saves work when most of the design is idle, at the cost of a little bookkeeping.
- **Latches.** Two-phase latch designs can be simulated by evaluating the logic once per phase.
- **Hardware engines and emulators.** Special machines such as the Yorktown Simulation Engine run the same once-per-cycle evaluation in parallel hardware.
- **Unrolling for analysis.** The same cut at the registers gives the [time-frame expansion](/time-frame-expansion/) used in sequential test generation and bounded model checking.

## When to use it

Use cycle-based simulation for long functional runs of synchronous designs: processor regressions, software running on a hardware model, and checks where only the values at the clock edges matter. Use [event-driven simulation](/event-driven-logic-simulation/) when the design has asynchronous parts, combinational loops, latches with transparency that matters, several unrelated clocks, or when glitches and delays are the point of the run. Use static timing analysis, not simulation, to check that the cycle-based assumption holds.

## Pitfalls

- **Updating registers one at a time.** A shift register $q_1 \leftarrow d$, $q_2 \leftarrow q_1$ then shifts the input two places in one cycle. Compute all new values, then write them.
- **Loops not cut by a register.** A cross-coupled latch made of gates has no levelized order. The implementation rejects it.
- **Assuming the timing is fine.** A cycle-based run passes even when a path is longer than the clock period. The match with real timing holds only after static timing analysis.
- **Gated and derived clocks.** A clock that goes through logic makes registers update at times the simple model does not know. Such designs need care in the order of edges, or event-driven simulation.
- **Asynchronous resets.** A reset that acts without a clock edge is outside the model and must be handled as a special case.

## Implementations

## History

Cycle simulation grew with design styles that make every loop pass through a register. IBM's level-sensitive scan design rules ([scan design](/scan-design/)) are one such style, and IBM built engines on this assumption: the Yorktown Simulation Engine (Pfister, 1982) evaluated the whole logic once per machine cycle in special hardware, and HSS (Barzilai, Carter, Rosen and Rutledge, 1987) ran the loop-free logic between latches as compiled code on 16 or 32 patterns at a time. Cycle-based software simulators and hardware emulators then became the usual tools for long functional runs of large synchronous designs, next to event-driven simulators of VHDL and Verilog.

## References
