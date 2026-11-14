---
tag: CKYAFC
kind: model
slug: finite-state-machine-with-datapath
name: Finite state machine with datapath
aliases:
- FSMD
area: eda/high-level-synthesis-and-scheduling
level: intro
summary: Gajski's model of a register-transfer design as a controller FSM whose states issue register transfers on a datapath of registers, units and multiplexers.
prereqs: [mealy-machine, moore-machine]
see_also: [high-level-synthesis, control-data-flow-graph, state-assignment, register-binding, resource-binding, operation-chaining, register-machine, euclidean-algorithm]
sources:
  - book: isbn:0792391942
    title: Daniel D. Gajski, Nikil D. Dutt, Allen C.-H. Wu and Steve Y.-L. Lin, High-Level Synthesis, Introduction to Chip and System Design, Kluwer, 1992
    locator: the chapters on architectural models and design representations (the controller and datapath model and the FSMD)
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 3, Hardware Modeling; Chapter 4, Architectural Synthesis (the data path and the control unit)
  - book: isbn:0131655639
    title: Marvin L. Minsky, Computation, Finite and Infinite Machines, Prentice-Hall, 1967
    locator: the chapter on program machines (two counters suffice to simulate a Turing machine)
---

A finite state machine with datapath (FSMD) describes a register transfer design as two parts that work together. The controller is a finite state machine. The datapath holds registers, functional units such as adders and comparators, and multiplexers that route values between them. In each state, the controller tells the datapath which register transfers to do, such as $x \leftarrow x - y$, and the datapath gives back status bits, such as the result of $x > y$, that choose the next state. Gajski and his coauthors use this model as the target of [high-level synthesis](/high-level-synthesis/): a schedule maps each operation of the [control data flow graph](/control-data-flow-graph/) to a state, and binding maps it to a unit and its values to registers.

## The machine

**Parts.** An FSMD has a finite set of states $S$ with a start state $s_0$, a finite set of registers $R$, where register $r$ has a width $w_r$ in bits, a set of primary inputs and outputs, and a set of functional units. A register transfer is an assignment $r \leftarrow f(r_1, \ldots, r_m)$, where $f$ is a function that one unit or a short chain of units computes. A condition is a Boolean function of the registers and the inputs.

**Behavior.** Each state $s$ has a list of guarded transfers, each of the form "if $c$ then $r \leftarrow f(\ldots)$", and a next state function $\delta(s, c_1, \ldots, c_k)$ of some conditions. In each clock cycle, in state $s$:

1. The datapath computes all conditions and all right-hand sides from the register values at the start of the cycle.
2. At the clock edge, every transfer whose guard is true writes its register, and the controller moves to $\delta(s, \ldots)$.

All reads in a state see the old values. So $x \leftarrow y$ and $y \leftarrow x$ in one state swap the two registers. Two transfers of one state must not write the same register under guards that can both be true.

**Hardware.** The controller is a [Moore](/moore-machine/) or [Mealy](/mealy-machine/) machine. Its inputs are the status bits and its outputs are the control lines: the select inputs of the multiplexers, the load enables of the registers and the function codes of the units. The datapath is a circuit with no state other than the registers.

**Timing.** The clock period $T$ must be at least the longest combinational delay of any state: from a register, through the multiplexers and the units that the state uses, to a register or to the controller. When a state chains two units, as in [operation chaining](/operation-chaining/), their delays add.

## What it counts

- **Cycles.** A run visits states $s_0, s_1, \ldots, s_N$, one per clock cycle, so it takes $N + 1$ cycles. The time is $(N + 1)\,T$.
- **Clock period.** The maximum over states of the combinational delay of that state.
- **Registers.** At least the largest number of values that are live across one clock edge. [Register binding](/register-binding/) finds how many registers suffice.
- **Units.** For each type $k$, at least the largest number of transfers that need type $k$ in one state. [Resource binding](/resource-binding/) maps transfers to unit instances.
- **Multiplexers.** The inputs of the multiplexer in front of each unit port or register, one per distinct source. They cost area and add delay.
- **Controller size.** The number of states and the control lines. [State assignment](/state-assignment/) gives each state a binary code.

Take the subtraction form of the [Euclidean algorithm](/euclidean-algorithm/) for the greatest common divisor of two positive inputs $a$ and $b$, with registers $x, y$ and three states:

| state | transfers | next state |
|---|---|---|
| $s_0$ | $x \leftarrow a$, $y \leftarrow b$ | $s_1$ |
| $s_1$ | if $x > y$ then $x \leftarrow x - y$; if $x < y$ then $y \leftarrow y - x$ | $s_2$ if $x = y$, else $s_1$ |
| $s_2$ | output $x$ | $s_2$ |

The datapath has one subtractor whose two inputs each have a multiplexer, so that it computes $x - y$ or $y - x$, and one comparator that gives $x > y$ and $x = y$. The run for $a = 12$, $b = 18$ is

| cycle | state | $x$ | $y$ |
|---|---|---|---|
| 1 | $s_0$ | ? | ? |
| 2 | $s_1$ | 12 | 18 |
| 3 | $s_1$ | 12 | 6 |
| 4 | $s_1$ | 6 | 6 |
| 5 | $s_2$ | 6 | 6 |

The transfers in $s_1$ have guards that are never both true, so they share one subtractor. The number of cycles depends on the data, which a schedule of a data flow graph alone cannot show. The clock period is the delay of the multiplexer, the subtractor and the register setup, or the comparator and the controller logic, whichever path is longer.

## Relation to other models

- **Finite state machine.** If the registers are folded into the state, an FSMD is a plain [Moore machine](/moore-machine/) with $|S| \cdot \prod_r 2^{w_r}$ states. The FSMD keeps the registers apart, so its description stays small.
- **Control data flow graph.** The [CDFG](/control-data-flow-graph/) is the input of synthesis, and the FSMD is the output. Each block becomes a sequence of states, one per control step, and each control edge becomes a transition that tests a status bit.
- **Register machine.** With unbounded integer registers and no bound on the run, an FSMD is a [register machine](/register-machine/), a model of general computation. Hardware registers have fixed widths, which keeps the FSMD finite.
- **Register transfer level.** A hardware language description at the register transfer level, with one clocked process for the controller and one for the datapath, is an FSMD written as code.
- **Processor.** A microprocessor is an FSMD whose datapath is general and whose controller reads instructions from memory. High-level synthesis builds an FSMD whose datapath and controller fit one program.

## Known results in the model

- **Bounded width gives a finite machine.** The configuration of an FSMD is its state and the values of all registers. With fixed widths there are at most $|S| \cdot 2^{\sum_r w_r}$ configurations, and the next one is a function of the current one and the inputs. So the FSMD is a finite automaton, and questions such as "can state $s$ be reached" are decidable by search over configurations. The number of configurations is exponential in the total width, which is why tools reason about registers as words and not as bits.
- **Unbounded width gives general computation.** If the registers hold unbounded integers and the transfers include add one, subtract one and test for zero, two registers suffice to simulate a two-counter machine, which Minsky showed can simulate a Turing machine. Then whether the FSMD reaches a state is undecidable, by the [halting problem](/halting-problem/).
- **Time is cycles times period.** The run time of a program on an FSMD is the number of cycles times $T$. Chaining lowers the number of cycles and raises $T$. So the best schedule for time is not always the one with the fewest states, and the clock period must be fixed before scheduling or found with it.
- **Registers follow lifetimes.** For a schedule of one block, the values live across each edge form intervals over the steps. The least number of registers equals the largest number of intervals that overlap at one edge, and the [left edge algorithm](/left-edge-algorithm/) reaches it. Across loops, lifetimes become circular arcs, and the problem is NP-hard, as the [high-level synthesis](/high-level-synthesis/) page shows.
- **Guarded transfers can share a unit.** Two transfers in one state whose guards are never both true can use one unit, because only one of them writes its result. This is the sharing of mutually exclusive operations, used in the example above.

## References
