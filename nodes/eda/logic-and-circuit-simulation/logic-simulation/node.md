---
tag: 272K07
kind: problem
slug: logic-simulation
name: Logic simulation
aliases:
- gate-level simulation
- digital simulation
area: eda/logic-and-circuit-simulation
level: intro
summary: Compute the signal values of a gate-level or register-transfer design over time for given input stimuli, under a chosen delay model and value system.
prereqs: [boolean-circuit]
see_also: [circuit-value-problem, event-driven-logic-simulation, compiled-code-logic-simulation, cycle-based-simulation, ternary-simulation, multi-valued-logic-simulation, inertial-and-transport-delay, fault-simulation]
sources:
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter Logic Simulation (the problem, value systems, delay models, compiled and event-driven simulation, and hazard detection; general locator)
  - paper: doi:10.1145/990518.990519
    title: Richard E. Ladner, The circuit value problem is log space complete for P, ACM SIGACT News 7(1), 18 to 20, 1975
    locator: the reduction from every problem in P to the circuit value problem in logarithmic space
  - book: isbn:9780195085914
    title: Raymond Greenlaw, H. James Hoover and Walter L. Ruzzo, Limits to Parallel Computation, P-Completeness Theory, Oxford University Press, 1995
    locator: the appendix entries for the circuit value problem and its variants, and the chapters on what P-completeness means for parallel speedup (general locator)
---

Logic simulation asks for the values of the signals of a digital design over time, for given inputs, when each signal takes values in a small set such as 0, 1 and X and each gate has a delay from a simple model. It is the logic half of the logic and circuit simulation sub-area. The circuit half asks for node voltages as real functions of time and solves differential equations, as in [transient circuit analysis](/transient-circuit-analysis/). Logic simulation gives up voltages for speed: it can run millions of gates for millions of clock cycles, and it is the main tool to check that a design does what its authors meant before it is built. Every instance fixes three choices: the netlist, the value system and the delay model. With zero delay and one input vector, the problem is the [circuit value problem](/circuit-value-problem/), which is solvable in linear time and P-complete. With delays, the answer is a waveform, and it depends on the delay model as much as on the netlist.

## In plain words

A chip design is a large drawing of logic gates joined by wires. Before anyone builds it, the designers want to know what it will do. So a program plays the inputs that a test asks for and works out, gate by gate, what every wire carries, and when.

The program does not compute voltages. A wire is high, low, or "not known". Each gate takes some time to react, and the program uses a fixed rule for that time.

The answer can depend on these rules. With no gate delays, a short spike may vanish. With delays, it may appear. A loop of gates with no delay may never settle.

## Definition

**Input.**

- A netlist: a set of nets, of which some are primary inputs, and a set of gates. Each gate $g$ has input nets, one output net $\mathrm{out}(g)$, a function $f_g$ over the value set and a delay $d(g) \ge 0$. State elements such as flip-flops are gates whose function reads a clock, or they are loops of gates.
- A value set $V$ that contains 0 and 1, often with X, Z or the nine values of IEEE Std 1164; see [multi-valued logic for simulation](/multi-valued-logic-simulation/).
- A delay model: zero delay, unit delay, or nominal delays $d(g)$, applied as transport or inertial delay; see [inertial and transport delay](/inertial-and-transport-delay/).
- An initial value for every net, often X, and a stimulus: for each primary input, a list of changes $(t, v)$ up to a final time $t_{\mathrm{end}}$.

**Semantics.** Write $z_g(t) = f_g(\text{the input values of } g \text{ at time } t)$. With transport delay, a nonprimary net is $\mathrm{out}(g)(t) = z_g(t - d(g))$ for $t \ge d(g)$, and keeps its initial value before. Inertial delay also removes the pieces of $z_g$ shorter than $d(g)$. With zero delay, the values at each time must satisfy $\mathrm{out}(g) = f_g(\text{inputs of } g)$ for every gate at once, a fixed point, and the order of changes within one time is given by [delta cycles](/delta-cycle/).

**Output.** For each net, its waveform on $[0, t_{\mathrm{end}}]$: its initial value and the list of its changes in time order. A cycle-based variant asks only for the values at each clock edge. With zero delay the fixed point may not exist or may not be unique, and the output must then say so: an oscillation is reported, and a common rule for two or more fixed points is to give X on the nets where they differ.

**Measures of work.** Let $G$ be the number of gates, $P$ the number of gate input pins, and $E$ the number of events, the changes of value on nets in the output. The cost of a method is counted in gate evaluations and queue operations.

## Variants

- **Combinational, zero delay.** One settled output vector per input vector, as in [compiled-code logic simulation](/compiled-code-logic-simulation/). Many vectors can share one run in bit-parallel words.
- **Synchronous, one value per cycle.** The design is a [Mealy machine](/mealy-machine/), and only the register values at each clock edge matter, as in [cycle-based simulation](/cycle-based-simulation/).
- **Timed.** Unit or nominal delays, with the full waveform, as in [event-driven logic simulation](/event-driven-logic-simulation/). Gate-level simulation with delays from timing analysis is of this kind.
- **Hazard and race analysis.** Ask which nets may glitch or end in a value that depends on the delays, for all delays at once, as in [ternary simulation](/ternary-simulation/).
- **Transistor networks.** Nets are nodes with charge, and gates are switches with strengths, as in [switch-level simulation](/switch-level-simulation/).
- **Hardware description languages.** The design is a set of processes in VHDL or Verilog that read and write signals; the gates above are processes of a fixed form.
- **Many machines at once.** [Fault simulation](/fault-simulation/) runs the good circuit and many faulty copies on the same stimulus.

## Examples

**One vector, zero delay.** A full adder with $s = a \oplus b \oplus c$ and $c_{\mathrm{out}} = ab + c(a \oplus b)$, at $a = b = 1$, $c = 0$, gives $s = 0$ and $c_{\mathrm{out}} = 1$. This is one instance of the circuit value problem.

**The delay model changes the answer.** Let $p = \lnot a$ and $y = a \land p$, a pulse generator. Logically $y = 0$ always. Let $a$ rise from 0 to 1 at time 0, so that before it $p = 1$ and $y = 0$.

| delay model | waveform of $y$ |
|---|---|
| zero delay | 0 at every time; a pulse of zero width in delta cycles at time 0 |
| unit delay, transport | 1 on $[1, 2)$ |
| unit delay on NOT, delay 2 on AND, inertial | 0 at every time |
| unit delay on NOT, delay 2 on AND, transport | 1 on $[2, 3)$ |

In the unit-delay case the AND gate sees $a = 1$ and the old $p = 1$ during $[0, 1)$ and asks for 1 from time 0, which appears at time 1. The inverter output falls at time 1, so the AND gate asks for 0 from time 1, which appears at time 2. With an inertial AND delay of 2, the request for 1 lasts only one time unit and is removed. A script checked all four rows with an event-driven simulator. The [event-driven logic simulation](/event-driven-logic-simulation/) page traces the same effect on a multiplexer.

**No fixed point.** A NOT gate whose output is its own input has no zero-delay fixed point over $\{0, 1\}$. An event-driven simulator makes delta cycles for ever, and with unit delay the net oscillates with period 2. Over $\{0, 1, X\}$ the value X is a fixed point, which is the answer of ternary simulation.

**Two fixed points.** A latch of two NOR gates $q = \lnot(r \lor \bar q)$ and $\bar q = \lnot(s \lor q)$ with $r = s = 0$ has the fixed points $(q, \bar q) = (0, 1)$ and $(1, 0)$. Which one a simulation reaches depends on the initial values and the delays. Starting from X, three-valued simulation keeps both nets at X, which says that the state is not known.

## Known algorithms

| Method | Delay model | What is known |
|---|---|---|
| [Compiled-code logic simulation](/compiled-code-logic-simulation/) (levelized code, bit-parallel words) | zero delay, acyclic | exact; $O(G + P)$ word operations per batch of vectors |
| [Cycle-based simulation](/cycle-based-simulation/) | none inside a cycle | exact at the clock edges of a synchronous design |
| [Event-driven logic simulation](/event-driven-logic-simulation/) (Ulrich 1969, time wheel) | zero, unit, nominal; transport or inertial | exact for the delay model; work grows with the events, not with $G$ per time step |
| [Ternary simulation](/ternary-simulation/) (Eichelberger 1965) | all delays at once | sound; detects static hazards and critical races |
| [Switch-level simulation](/switch-level-simulation/) (Bryant 1984) | unit delay per round, or zero | sound with X on transistor networks |
| Parallel discrete-event simulation ([Chandy-Misra-Bryant](/chandy-misra-bryant/), [Time Warp](/time-warp/)) | nominal | the same waveforms, on many processors; speedup measured |
| Fault simulation ([concurrent](/concurrent-fault-simulation/), [parallel](/parallel-fault-simulation/)) | as the base simulator | one run for many faulty circuits |

What is proved: the exactness of each method for its delay model, and the bounds below. What is only measured: the speed of event-driven against compiled-code simulation on real designs, which depends on the share of gates that change per time step, and the speedup of parallel simulation.

## Bounds

**Linear time for one vector.** A combinational netlist without loops and with zero delay is evaluated in $O(G + P)$ time by evaluating the gates in [topological order](/topological-sort/). A general algorithm cannot do better: an output can depend on every gate, so every gate must be read. With $T$ time steps of unit delay, step-by-step evaluation takes $O(T (G + P))$ time, and event-driven evaluation takes time proportional to the number of gate evaluations, at most the events times the largest fanout plus the queue cost.

**P-completeness.** The circuit value problem, with zero delay and one vector, is complete for P under logarithmic-space reductions (Ladner 1975). So no algorithm evaluates every circuit in time polylogarithmic in its size on a polynomial number of processors, unless every problem in P has such an algorithm, that is, unless NC = P. What parallel hardware can do is evaluate a circuit of depth $D$ in $D$ rounds with one processor per gate, one level per round. Long chains of logic, and the sequential steps of a design over time, limit the speedup of parallel logic simulation.

**Fixed points of zero-delay loops.** For a zero-delay netlist with loops and fixed inputs, deciding whether a binary fixed point exists is NP-complete. *Proof.* A guessed assignment of all nets is checked gate by gate in linear time, so the problem is in NP. For hardness, take a formula $\varphi(y_1, \ldots, y_n)$, make a gate for each $y_i$ with $i \ge 2$ that copies $y_i$ to itself, and give $y_1$ the gate $y_1 \oplus \lnot \varphi(y)$, built from the gates of $\varphi$ and fed back to $y_1$. The netlist has size linear in $\varphi$, and $y$ is a fixed point exactly when $\lnot\varphi(y) = 0$, that is, when $y$ satisfies $\varphi$. So a fixed point exists if and only if $\varphi$ is satisfiable, and [SAT](/sat/) reduces to the question. $\square$ Ternary simulation avoids this: starting from X on the loop nets, it reaches the least ternary fixed point in at most as many rounds as there are nets, and every 0 or 1 in it holds in every binary fixed point. It may answer X where a binary fixed point exists.

**Lower bound on the output.** A waveform with $E$ events takes $\Omega(E)$ time to write, and $E$ can be as large as $T \cdot G$ for a circuit that changes at every step.

## Reductions

- **From the circuit value problem.** CVP is logic simulation with zero delay, one vector and no loops. So logic simulation is P-hard.
- **Unit delay to zero delay.** Simulation with unit delay for $T$ steps is zero-delay evaluation of the circuit copied $T$ times, where copy $t + 1$ of each gate reads the copies $t$ of its inputs, as in [time-frame expansion](/time-frame-expansion/). The copied circuit has no loops, even if the original has.
- **To discrete-event simulation.** Timed logic simulation is a case of [event-driven simulation](/event-driven-simulation/) in which the entities are gates and the events are changes of net values.
- **From circuit simulation.** Thresholds on node voltages turn the output of [transient circuit analysis](/transient-circuit-analysis/) into logic waveforms. [Timing simulation](/timing-simulation/) and [mixed-mode simulation](/mixed-mode-simulation/) sit between the two halves.

## Applications

- **Functional verification.** Designers run test programs and random stimulus on the register-transfer and gate descriptions and compare the outputs with a model. This is the largest use of logic simulation in chip design.
- **Gate-level timing checks.** After layout, the netlist with delays from [static timing analysis](/static-timing-analysis/) is simulated to check resets, clock gating and asynchronous paths that static analysis does not cover.
- **Test.** [Fault simulation](/fault-simulation/) grades a test set by its [fault coverage](/fault-coverage/), and test generators simulate each new pattern.
- **Power.** The waveforms give the [switching activity](/switching-activity/) of each net, which power estimation multiplies by the net capacitance.
- **Equivalence and debugging.** Simulation finds counterexamples quickly before formal methods such as [sequential equivalence checking](/sequential-equivalence-checking/) are run.

## References
