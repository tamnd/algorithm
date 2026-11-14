---
tag: V1JG2T
kind: algorithm
slug: event-driven-logic-simulation
name: Event-driven logic simulation
aliases:
- selective trace simulation
- Ulrich event-driven simulation
area: eda/logic-and-circuit-simulation
level: core
summary: Evaluates only the gates whose inputs changed, taking events in time order from a time wheel and scheduling new events for outputs that change after their delays.
solves: [logic-simulation]
model: word-ram
complexity:
  vars: {E: the number of applied value changes, F: the largest fanout, k: the largest fan-in, S: the number of distinct event times, M: the number of slots of the time wheel, N: the number of nets, P: the number of gate input pins}
  time: {worst: "O(E F k + S M)", best: "O(E F k + S)"}
  space: {extra: "O(N + P)"}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1969
  people: [Ernst G. Ulrich]
  note: Ulrich described selective trace in 1965 and the time mapping, the circular list of time slots now called a time wheel, in his 1969 CACM paper.
prereqs: [logic-simulation, boolean-circuit, event-driven-simulation]
see_also: [timing-wheel, calendar-queue, delta-cycle, inertial-and-transport-delay, compiled-code-logic-simulation, concurrent-fault-simulation, chandy-misra-bryant, parallel-discrete-event-simulation]
sources:
  - paper: "Ernst G. Ulrich, Exclusive simulation of activity in digital networks, Communications of the ACM 12(2), 102 to 110, 1969"
    title: E. G. Ulrich, Exclusive simulation of activity in digital networks, Communications of the ACM 12(2), 102 to 110, February 1969
    locator: the evaluation of only the active elements, and time mapping, a circular list of time slots for the scheduled events
  - paper: "Ernst G. Ulrich, Time-sequenced logical simulation based on circuit delay and selective tracing of active network paths, Proceedings of the 20th ACM National Conference, 437 to 448, 1965"
    title: E. G. Ulrich, Time-sequenced logical simulation based on circuit delay and selective tracing of active network paths, Proceedings of the 20th ACM National Conference, 437 to 448, 1965
    locator: selective trace, the evaluation of the fanout of the elements that changed
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter Logic Simulation (event-driven simulation, delay models, time wheel, two-pass algorithm, hazard detection)
---

Event-driven logic simulation computes the waveforms of a gate-level circuit by evaluating a gate only when one of its inputs changes. A change of value on a net at a time is an *event*. The simulator keeps the future events in a time wheel, takes the events of the earliest time, applies them, evaluates the gates that read the changed nets, and schedules a new event for each gate output whose value will change after the delay of the gate. This page is in the logic simulation half of [logic and circuit simulation](/logic-simulation/): it works on gates, events and the values 0 and 1, not on nodal equations. The delay model is a fixed integer delay for each gate, with zero delay and unit delay as special cases. Transport delay is the default, and inertial delay is a small change, described under Variants. In typical circuits only a few percent of the gates change at each event time, so this method, also called selective trace, does much less work than evaluating every gate at every time.

## In plain words

Most of a large chip is quiet at any moment. Only a few wires change.

So the simulator does not look at every gate at every time step. It keeps a calendar of future changes. It jumps to the next time that has a change, applies the changes, and looks only at the gates that read a changed wire. If such a gate now wants a new output, the simulator writes that new output into the calendar at the current time plus the delay of the gate.

When a gate has no delay, the new change goes into the same moment of the calendar. The simulator then makes another pass at the same time, and it repeats this until nothing more changes at that moment.

## The problem

The input is a gate-level circuit $C$ with $N$ nets, $P$ gate input pins and gates $g$ that each have a Boolean function $f_g$, an output net $\mathrm{out}(g)$ and an integer delay $d(g) \ge 0$. Each net has an initial value in $\{0, 1\}$, and a list gives the changes of the primary inputs as triples (time, net, value). The gates may form loops, as in latches. The output is the value of every net at every time from $0$ to $T_{\text{end}}$, given as the list of changes.

The meaning of the delays is the transport model. Let $z_g(t) = f_g(\text{the values of the inputs of } g \text{ at time } t)$ be the value that the gate function asks for. Then the output follows it after the delay: $\mathrm{out}(g)(t) = z_g(t - d(g))$ for $t \ge d(g)$, and the initial value before. With zero delays this is a set of equations at each time, and the [delta cycles](/delta-cycle/) below solve it.

## The algorithm

```pseudo id=main
EVENT-SIM(C, d, v0, input events, T_end)
L1  val ← v0; proj ← v0                       (proj is the last value scheduled on a net)
L2  W ← a time wheel that holds the input events; do one pass of L7 to L10 at time 0 with G = all gates
L3  while W has events at a time t ≤ T_end, with t the earliest such time, do
L4      U ← the events of time t, taken out of W; a later event on a net replaces an earlier one
L5      A ← the nets n in U with U[n] ≠ val[n]; set val[n] ← U[n] for each n in A
L6      G ← the gates with an input in A                  (selective trace)
L7      for each gate g in G do
L8          v ← f_g(val of the inputs of g)
L9          if v ≠ proj[out(g)] then
L10             proj[out(g)] ← v; schedule (t + d(g), out(g), v) in W
L11 return val and the list of changes made at L5
```

The time wheel is Ulrich's time mapping. It is an array of $M$ slots, where $M$ is one more than the largest gate delay, and slot $t \bmod M$ holds the events of time $t$. The input events that lie more than $M$ steps ahead wait in an overflow list and move into the wheel when the current time comes near. A gate event always fits, since its time is at most $t + M - 1$. The [timing wheel](/timing-wheel/) page treats the data structure itself, and a [calendar queue](/calendar-queue/) or a [priority queue](/priority-queue/) can take its place when the delays vary widely.

The test at L9 compares with the projected value, not with the present value. With transport delay an output can have several events pending, and the projected value is the value that the output will have after all of them. If the new value equals it, the event would change nothing.

When $d(g) = 0$, line L10 puts the event into the slot of the present time $t$. The loop at L3 then finds time $t$ again and makes one more pass, a delta pass, at the same time. A circuit with a loop of zero-delay gates can make delta passes for ever, so the implementation stops after a fixed number of passes and reports an oscillation.

## Example

Take $y = ab + a'c$ with gates $\bar a = \mathrm{NOT}(a)$, $p = \mathrm{AND}(a, b)$, $q = \mathrm{AND}(\bar a, c)$ and $y = \mathrm{OR}(p, q)$. Let $b = c = 1$, so $y = 1$ for both values of $a$. Every gate has delay 1. At the start $a = 1$, so $\bar a = 0$, $p = 1$, $q = 0$ and $y = 1$, and $a$ falls to 0 at time 10.

| time | changes applied (L5) | gates evaluated (L7) | events scheduled (L10) |
| --- | --- | --- | --- |
| 0 | none | all four, each gives its present value | none |
| 10 | $a = 0$ | $\bar a$, $p$ | $\bar a = 1$ and $p = 0$ at 11 |
| 11 | $\bar a = 1$, $p = 0$ | $q$, $y$ | $q = 1$ at 12; $y = \mathrm{OR}(0, 0) = 0$ at 12 |
| 12 | $q = 1$, $y = 0$ | $y$ | $y = \mathrm{OR}(0, 1) = 1$ at 13 |
| 13 | $y = 1$ | none | none |

The output has a glitch: $y$ is 0 for one time unit from 12 to 13, because the path through $\bar a$ is one gate longer than the path through $p$. This is a static 1-hazard. The run made 9 gate evaluations, 4 of them at time 0. A step-by-step simulator would evaluate 4 gates at each of the 14 time steps from 0 to 13.

With zero delays, the same change at time 10 takes four delta passes at time 10: the changes are $a$, then $\bar a$ and $p$, then $q$ and $y = 0$, then $y = 1$. So even with zero delay, $y$ shows a pulse of zero width at time 10, which a VHDL or Verilog process that waits on $y$ would see. If the OR gate has an inertial delay of 2, the evaluation at time 12 cancels the pending change to 0 at time 13, and the glitch is gone. With a transport delay of 2 it stays, from 13 to 14.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows two facts.

First, with all delays at least 1 and transport delay, the values after time $t$ equal those of a unit-time step simulation with $\mathrm{out}(g)(t) = z_g(t - d(g))$ for every integer $t$, on any circuit, with or without loops. The key invariant is that, after time $t$, the events pending on an output describe exactly the values $z_g(s)$ for $t - d(g) < s \le t$, and the projected value is $z_g(t)$. A gate that L6 does not select has the same inputs as at the previous time, so its $z_g$ did not change and skipping it is safe. The same proof with the cancel rule gives the inertial version.

Second, with all delays 0 on an acyclic circuit, the delta passes at each time stop after at most $D + 1$ passes, where $D$ is the depth of the circuit, and the values then equal the direct evaluation of the circuit on the present inputs. When the passes stop, every gate satisfies $\mathrm{val}[\mathrm{out}(g)] = f_g(\mathrm{val}[\text{inputs}])$, so the values are a fixed point of the circuit equations, and an acyclic circuit has exactly one. With unit delays the values reach the same fixed point at most $D$ time units after the last input change. So event-driven simulation with zero or unit delays and levelized evaluation give the same settled values on acyclic circuits. They do not give the same waveforms: the glitch above appears only in the event-driven run.

The tests check the first fact against a unit-time step simulation on random circuits with loops and delays from 1 to 3, both for transport and inertial delay, and the second fact against direct evaluation of every input vector of random acyclic circuits.

## Complexity

Each change applied at L5 makes L6 select at most $F$ gates, and each evaluation at L8 reads at most $k$ inputs. Each scheduled event costs $O(1)$ in the wheel. Moving to the next event time costs at most $M$ slot checks. So the time is $O(E F k + S M)$, where $E$ is the number of applied changes and $S$ is the number of distinct event times. The space is $O(N + P)$ for the netlist, the values and the projected values, plus the pending events, of which there are at most $N M$.

The cost follows the activity $E$, not the circuit size times the time. This is the point of the method. The activity can be large, though. A stage $z_s = \mathrm{XOR}(z_{s-1}, \mathrm{BUF}(z_{s-1}))$ in which the buffer has delay $2^{s-1}$ turns each change of its input into two changes of its output. One input change then makes $2^k$ changes at the end of a chain of $k$ stages, which has $2k$ gates. A script with the implementation of this page counted 2, 4, 8, ..., 128 output changes for $k = 1, \ldots, 7$. With unit delays and no loops this cannot happen: a net changes at most $D$ times after one input change.

## Properties

- **Exact for its delay model.** The waveforms are exactly those of the transport (or inertial) model with the given integer delays. They are not the waveforms of the real circuit, whose delays depend on load, slope and process.
- **Order of evaluation.** Within one pass the gates of $G$ see the values of the same pass, so the result does not depend on the order of L7. Across delta passes the order is fixed by the algorithm.
- **Activity.** In typical designs only a few percent of the gates switch at each time, which is why selective trace beats evaluating every gate. In a design with high activity, such as a datapath under random data, the saving is small, and compiled code wins.
- **Glitches.** The method shows hazards and glitches that a zero-delay levelized simulation hides. Power estimation tools use this to count [glitch power](/glitch-power/).

## Variants and improvements

- **Inertial delay.** Line L10 first cancels the pending events of $\mathrm{out}(g)$ and then schedules $v$ only if $v \ne \mathrm{val}[\mathrm{out}(g)]$. A pulse at the gate function that is shorter than $d(g)$ never reaches the output. See [inertial and transport delay](/inertial-and-transport-delay/).
- **Rise and fall delays.** A gate can have one delay for a change to 1 and another for a change to 0. With transport delay this can put events out of time order on one net, so simulators use the inertial rule or keep the events sorted.
- **Two-pass algorithm.** Process all events of a time first, collect the gates to evaluate, and evaluate them in a second pass. The pseudocode already works this way, which stops a gate from being evaluated twice in one pass.
- **More values.** With the values 0, 1, X and Z of [multi-valued logic simulation](/multi-valued-logic-simulation/), L8 uses the tables of the value system, and the initial values can be X instead of a guess.
- **Fault simulation.** [Concurrent fault simulation](/concurrent-fault-simulation/) runs the good circuit and many faulty circuits in one event-driven run and keeps only the gates where a faulty circuit differs.
- **Parallel simulation.** The conservative method of [Chandy, Misra and Bryant](/chandy-misra-bryant/) and the optimistic [Time Warp](/time-warp/) split the circuit among processors. See [parallel discrete-event simulation](/parallel-discrete-event-simulation/).
- **Other engines.** For synchronous designs where timing inside the clock cycle is not of interest, [compiled-code simulation](/compiled-code-logic-simulation/) and [cycle-based simulation](/cycle-based-simulation/) avoid the event queue.

## When to use it

Use event-driven simulation when the delays matter, when the circuit has asynchronous parts or latches, or when the activity is low. It is the engine of every VHDL and Verilog simulator, which also need delta cycles to order the processes that run at the same time. For a synchronous design with high activity and no interest in the timing inside a cycle, a levelized compiled-code or cycle-based simulator is usually several times faster.

## Pitfalls

- **Comparing with the present value instead of the projected value.** With transport delay and pending events, the test $v \ne \mathrm{val}[\mathrm{out}(g)]$ drops real events. For example, an output at 0 with a pending change to 1 must still get a new event back to 0.
- **Zero-delay loops.** A NOT gate that drives itself with delay 0 makes delta passes for ever. A real simulator needs a limit on the delta passes and a clear error message. The tests show this loop, and a NOR latch whose two inputs fall at the same time, which oscillates for ever with equal delays and also with transport delays 1 and 2.
- **Same-time events in the wrong order.** Two events on one net at one time must be applied in the order they were scheduled, or the wrong one wins. A heap that is not stable can break this.
- **Initial values.** With all nets at 0 at the start, the first pass at time 0 makes events everywhere. Without that first pass, gates whose inputs never change keep a wrong output for the whole run.
- **Reading glitches as real.** The glitches come from the delay model. A glitch in a unit-delay simulation may be absent in the real circuit, and the other way round.

## Implementations

## History

Ernst Ulrich described simulation with circuit delays and the selective trace of active paths in 1965, and the time mapping, the circular list of time slots now called a time wheel, in his 1969 paper in the Communications of the ACM. Event-driven gate-level simulation then became the standard method for logic verification and for fault simulation in the 1970s. The hardware description languages VHDL (IEEE Std 1076, first in 1987) and Verilog (IEEE Std 1364, first in 1995) both define their meaning by an event-driven simulation cycle with delta cycles.

## References
