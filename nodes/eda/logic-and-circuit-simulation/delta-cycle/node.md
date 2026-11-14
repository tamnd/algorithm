---
tag: JMPYQB
kind: definition
slug: delta-cycle
name: Delta cycle
aliases:
- delta delay
- simulation delta cycle
area: eda/logic-and-circuit-simulation
level: core
summary: An infinitesimal step of the VHDL and Verilog simulation cycle in which zero-delay assignments take effect, so events at one time are ordered without advancing time.
prereqs: [event-driven-logic-simulation]
see_also: [inertial-and-transport-delay, logic-simulation, event-driven-simulation, multi-valued-logic-simulation, cycle-based-simulation, timing-wheel]
sources:
  - paper: "IEEE Std 1076-2008, IEEE Standard VHDL Language Reference Manual, IEEE, 2009"
    title: IEEE Standard VHDL Language Reference Manual, IEEE Std 1076-2008
    locator: Section 14.7.5, Model execution (the simulation cycle, the update of signals, the resumption of processes, and the definition of a delta cycle as a simulation cycle that does not advance time)
  - paper: "IEEE Std 1364-2005, IEEE Standard for Verilog Hardware Description Language, IEEE, 2006"
    title: IEEE Standard for Verilog Hardware Description Language, IEEE Std 1364-2005
    locator: Clause 11, Scheduling semantics, and Subclause 11.3, the stratified event queue (active, inactive, nonblocking assign update and monitor events)
---

A delta cycle is one round of the simulation cycle of a hardware description language in which simulated time does not advance. This page is in the logic simulation half of the sub-area: it is about signal values and events, not about node voltages. The delay model is zero delay. A signal assignment with no delay, such as `b <= not a;` in VHDL, does not take effect at once and does not take effect one time unit later. It takes effect one delta later, at the same simulated time. So the simulator orders the events of one time instant by a second counter, and the processes that run in the same delta all see the same values. This makes the result independent of the order in which the simulator runs these processes. The [event-driven logic simulation](/event-driven-logic-simulation/) page shows how the scheduler makes delta passes; this page defines the delta cycle and its rules.

## Definition

**Time with deltas.** Simulated time is a pair $(t, n)$, where $t$ is the physical time and $n \ge 0$ counts the delta cycles at $t$. Pairs are ordered lexicographically: $(t, n) < (t', n')$ if $t < t'$, or $t = t'$ and $n < n'$. An assignment with delay $d > 0$ made at $(t, n)$ is scheduled for $(t + d, 0)$. An assignment with zero delay is scheduled for $(t, n + 1)$.

**Simulation cycle.** The model is a set of processes that talk only through signals. Each signal has one driver per process that assigns it, and a signal with several drivers has a resolution function that combines the driver values. One cycle at $(t, n)$ has two phases.

1. *Update.* Every driver with a transaction for $(t, n)$ takes its new value. Every signal with a changed driver gets its new value, through its resolution function if it has one. A signal whose value changes has an event at $(t, n)$.
2. *Evaluate.* Every process that waits on a signal with an event at $(t, n)$ resumes and runs until it waits again. It reads the values fixed in phase 1. Its assignments only add transactions to its own drivers, for $(t, n + 1)$ or for a later time.

The next cycle is at the earliest pair with a pending transaction. A **delta cycle** is a cycle whose next cycle has the same $t$. IEEE Std 1076-2008, Section 14.7.5, defines the VHDL simulation cycle in this way.

**Determinism (exact).** Suppose the processes share no variables and every resolution function gives the same result for every order of its arguments. Then the signal values at every $(t, n)$ do not depend on the order in which the simulator runs the processes of an evaluate phase.

*Proof.* By induction over the cycles in time order. Suppose that, at the start of the cycle at $(t, n)$, the signal values, the pending transactions of all drivers and the local states of all processes are the same for any choice of orders in the earlier cycles. The update phase applies the transactions for $(t, n)$. Each driver value is then fixed, and each signal value is a function of the multiset of its driver values, so the values after phase 1 do not depend on any order. In phase 2, the set of processes that resume depends only on the events of phase 1. A resumed process reads only the signal values of phase 1, which no process can change during phase 2, and its own local state. It writes only its own drivers and its own local state. So what each process does is the same whatever the other processes do before it, and the state at the start of the next cycle is the same for every order. $\square$

The proof needs both phases. If a process could see a value written in the same phase, its result would depend on whether the writer ran first.

**How many deltas.** With zero delays on an acyclic circuit of depth $D$, the deltas at one time stop after at most $D + 1$ cycles, and the values are those of a direct evaluation of the circuit. The [event-driven logic simulation](/event-driven-logic-simulation/) page proves this. With a loop of zero-delay assignments the deltas can go on for ever.

## Examples and non-examples

**Example: a zero-width pulse.** Take three VHDL concurrent assignments with no delay, `b <= not a;` and `c <= a and b;`, and a stimulus that sets `a` from 0 to 1 at $t = 10$. Before $t = 10$ the values are $a = 0$, $b = 1$, $c = 0$.

| cycle | update phase | processes that run | new transactions |
|---|---|---|---|
| $(10, 0)$ | $a = 1$ | `b`, `c` | $b = 0$ and $c = 1$ for $(10, 1)$ |
| $(10, 1)$ | $b = 0$, $c = 1$ | `c` | $c = 0$ for $(10, 2)$ |
| $(10, 2)$ | $c = 0$ | none | none |

At $(10, 1)$ the process for `c` read $a = 1$ with the old value $b = 1$, so `c` is 1 for one delta. A waveform viewer shows no pulse, since the pulse has zero width in time. But a process that waits on `c` resumes at $(10, 1)$ and at $(10, 2)$ and sees both events. With real gate delays the same circuit has a static hazard; with zero delay the hazard shrinks to one delta.

**Example: two flip-flops swap.** Two clocked VHDL processes, one with `x <= y;` and one with `y <= x;`, both resume on the same rising edge at $(t, n)$. Both read the old values, and both new values arrive at $(t, n + 1)$. So $x$ and $y$ swap, whichever process runs first. This is the determinism result at work.

**Example: Verilog.** IEEE Std 1364-2005 has no object called a delta cycle. Its scheduling, in Clause 11, puts the events of one time into regions in a fixed order: active events, inactive events (from `#0` delays), nonblocking assign updates and monitor events. A nonblocking assignment `x <= y;` reads `y` at once and writes `x` in the nonblocking assign update region, after all active events of the time. This gives the two-phase behavior above, and the swap of the last example works with `x <= y;` and `y <= x;` in two `always @(posedge clk)` blocks.

**Non-example: Verilog blocking assignments.** With blocking assignments `x = y;` and `y = x;` in the two `always` blocks, each assignment writes in the active region, and the standard does not fix the order of the two blocks. One order gives $x = y = $ the old $y$, the other gives $x = y = $ the old $x$. This is a race, and the determinism result does not apply, because a process can see a value that another process wrote in the same phase.

**Non-example: a zero-delay loop.** The VHDL assignment `b <= not b;` is a process that waits on `b`. Each event on `b` makes it run again and schedule a new value one delta later, so the deltas at the first time go on for ever and time never advances. Simulators stop after a fixed number of deltas at one time and report an error. The event-driven page shows the same loop and a NOR latch that oscillates.

**Non-example: unit delay.** A delta is not a small time step. With unit delays, `b <= not a after 1 ns;` moves the change to $(t + 1, 0)$, and every process that runs at $t$ is done before it. A design that works only because of the order of deltas, for example a clock that passes through a zero-delay assignment and so arrives one delta after the data, can fail in a unit-delay or gate-level simulation and in the real circuit.

## Related definitions

- **[Event-driven logic simulation](/event-driven-logic-simulation/).** The algorithm that schedules events; with zero delays, its passes at one time are delta cycles.
- **[Inertial and transport delay](/inertial-and-transport-delay/).** The rules for assignments with a delay $d > 0$, which go to $(t + d, 0)$.
- **[Multi-valued logic for simulation](/multi-valued-logic-simulation/).** The IEEE 1164 resolution function, which is commutative and associative, as the determinism result needs.
- **[Logic simulation](/logic-simulation/).** The problem that the simulation cycle solves.
- **[Event-driven simulation](/event-driven-simulation/).** The generic event loop, with no gates and no deltas.
- **[Cycle-based simulation](/cycle-based-simulation/).** Evaluates the logic between registers once per clock in a fixed order, so it needs no deltas.
- **[Timing wheel](/timing-wheel/).** The queue that holds the transactions; the deltas of one time can share one slot.

## References
