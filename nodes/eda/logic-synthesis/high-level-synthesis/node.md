---
tag: 08ZWFD
kind: problem
slug: high-level-synthesis
name: High-level synthesis
aliases:
- behavioral synthesis
- architectural synthesis
area: eda/logic-synthesis
level: core
summary: Turn an algorithmic description into a register transfer design by scheduling operations into clock steps, allocating units and binding operations to them.
prereqs: [dag-longest-path, graph-coloring, np-hard]
see_also: [asap-alap-scheduling, force-directed-scheduling, list-scheduling, left-edge-algorithm, precedence-constrained-scheduling, instruction-scheduling-problem, register-allocation-problem, iterative-modulo-scheduling]
sources:
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 4, Architectural Synthesis; Chapter 5, Scheduling Algorithms; Chapter 6, Resource Sharing and Binding
  - paper: doi:10.1109/43.31522
    title: Pierre G. Paulin and John P. Knight, Force-directed scheduling for the behavioral synthesis of ASICs, IEEE Transactions on Computer-Aided Design 8(6), 661 to 679, 1989
    locator: time-constrained and resource-constrained scheduling, and the differential equation example
  - paper: doi:10.1016/S0022-0000(75)80008-0
    title: "J. D. Ullman, NP-complete scheduling problems, Journal of Computer and System Sciences 10(3), 1975"
    locator: the NP-completeness of scheduling unit-time tasks with precedence constraints on a given number of processors
  - paper: doi:10.1137/0601025
    title: Michael R. Garey, David S. Johnson, Gary L. Miller and Christos H. Papadimitriou, The complexity of coloring circular arcs and chords, SIAM Journal on Algebraic and Discrete Methods 1(2), 216 to 227, 1980
    locator: the NP-completeness of coloring circular-arc graphs, which is register binding for values that live across a loop boundary
---

High-level synthesis turns a description of what a circuit computes, such as a loop body written in C or in a hardware language, into a register transfer design: a datapath of functional units, registers and multiplexers, and a controller that tells the datapath what to do in each clock step. The description is first compiled into a data flow graph, or a control and data flow graph. Then three linked problems are solved: scheduling assigns each operation to a control step, allocation chooses how many units of each type to build, and binding assigns each operation to a unit and each value to a register. The goal is a small design that meets a latency bound, or a fast design within an area bound. Scheduling under a unit limit is [NP-hard](/np-hard/) already for one unit type and unit delays when the number of units is part of the input, while some binding steps are easy, such as register binding for straight-line code, which is interval coloring.

## In plain words

A program says "multiply these, add those, compare the result". A chip that runs it needs multipliers, adders, registers to hold values between clock ticks, and a small controller. High-level synthesis builds that chip from the program. First it decides in which clock tick each operation runs. Then it decides how many multipliers and adders to build, and which operation uses which one. Then it decides which register holds each value. With more hardware, more work runs at the same time and the chip is faster. With less hardware, the chip is smaller but slower. The tool looks for a good balance, and the exact best balance is hard to find.

## Definition

**Input.** A data flow graph $G = (V, E)$ with no cycle, where each operation $v$ has a type, such as multiply or add. A library that gives, for each unit type, the operation types it can do, its delay $\delta$ in control steps, and its area. A constraint, either a latency bound $L$ or a number $a_k$ of units of each type $k$.

**Feasible solutions.** A schedule $t : V \to \{1, 2, \dots\}$ with $t(v) \ge t(u) + \delta(u)$ for each edge $(u, v)$; a binding $\beta$ that maps each operation to a unit instance of a type that can do it, so that two operations on one instance never use the same step; and a register binding that maps each value to a register, so that two values that are live in the same step never share a register.

**Objective.** In the time-constrained form, the latency is at most $L$, and the goal is the least area, the sum of the unit areas plus the registers and multiplexers. In the resource-constrained form, the units are given, and the goal is the least latency, $\max_v (t(v) + \delta(v) - 1)$.

**Decision version of scheduling.** Given $G$, the delays, the unit counts $a_k$ and $L$, is there a schedule with latency at most $L$ that never uses more than $a_k$ units of type $k$ in a step?

## Variants

- **Time-constrained or resource-constrained.** Fix the latency and minimize the units, or fix the units and minimize the latency. Exploring both gives the Pareto curve of area and latency.
- **Chaining and multicycle operations.** Several fast operations may run in one step if their total delay fits the clock period, and slow ones may take several steps.
- **Pipelined units.** A unit with a delay of several steps accepts a new operation every step, which changes the resource constraint.
- **Loops and pipelining.** A loop body runs again before the last iteration ends, with an initiation interval. This is the hardware form of [modulo scheduling](/iterative-modulo-scheduling/).
- **Control flow.** Branches let two operations share a unit in the same step when they are on exclusive paths.
- **Binding objectives.** Fewest registers, fewest multiplexer inputs, or fewest buses.

## Examples

Take the differential equation example of Paulin and Knight, used on the [ASAP and ALAP](/asap-alap-scheduling/) page: six multiplies, $v_1, v_2, v_3, v_6, v_7, v_8$, and five ALU operations, $v_4, v_5, v_9, v_{10}, v_{11}$, each with delay 1.

**Area against latency.** The least latency for each number of multipliers and ALUs, found by an exhaustive search over schedules, is:

| multipliers | 1 ALU | 2 ALUs | 3 ALUs |
|---|---|---|---|
| 1 | 7 | 7 | 7 |
| 2 | 5 | 4 | 4 |
| 3 | 5 | 4 | 4 |
| 4 | 5 | 4 | 4 |

So 4 steps need 2 multipliers and 2 ALUs, and one ALU fewer costs one step. With unlimited units, the ASAP schedule also reaches 4 steps, but it uses 4 multipliers in step 1.

**Scheduling and unit binding.** [Force-directed scheduling](/force-directed-scheduling/) at $L = 4$ gives the multiplies $v_1, v_2$ in step 1, $v_3, v_6$ in step 2 and $v_7, v_8$ in step 3, and the ALU operations $v_{10}$ in step 1, $v_{11}$ in step 2, $v_4$ in step 3, and $v_5, v_9$ in step 4. Two multipliers and two ALUs suffice, with for example multiplier 1 doing $v_1, v_3, v_7$ and multiplier 2 doing $v_2, v_6, v_8$.

**Register binding.** A value is held in a register from the step after it is computed to the last step that reads it. The intermediate values live as follows: $v_1$, $v_2$ and $v_{10}$ in step 2; $v_3$ and $v_6$ in step 3; $v_4$, $v_7$ and $v_8$ in step 4. At most 3 values are live in one step, so 3 registers are needed, and the [left-edge algorithm](/left-edge-algorithm/) reaches 3: $R_1$ holds $v_1, v_3, v_4$; $R_2$ holds $v_2, v_6, v_7$; and $R_3$ holds $v_{10}, v_8$.

## Known algorithms

- **ASAP and ALAP.** [ASAP and ALAP scheduling](/asap-alap-scheduling/) give the least latency with unlimited units, in $O(V + E)$ time, and the time frame of each operation.
- **List scheduling.** [List scheduling](/list-scheduling/) fills each step with ready operations, by a priority such as the ALAP step or the length of the longest path to a sink, up to the unit limits. It is the usual resource-constrained heuristic.
- **Force-directed scheduling.** [Force-directed scheduling](/force-directed-scheduling/) balances the expected use of each unit type over the steps, for a fixed latency. It is a heuristic.
- **Integer programming.** A [0-1 integer program](/binary-integer-programming/) with a variable for each operation and each step in its time frame expresses precedence, unit limits and latency exactly. It is solved by a general solver, for small graphs.
- **Special cases of scheduling.** With one unit type, unit delays and a tree of operations, [Hu's algorithm](/hu-algorithm/) is optimal. With two units of one type and unit delays, the [Coffman-Graham algorithm](/coffman-graham-algorithm/) is optimal.
- **Register binding.** For straight-line code, the lifetimes are intervals, and the [left-edge algorithm](/left-edge-algorithm/) uses the least number of registers, as in [interval partitioning](/interval-partitioning/).
- **Unit binding.** Group operations into compatible sets, operations of one type in different steps, and pick a grouping that keeps the multiplexers small, by clique partitioning or by matching heuristics.

## Bounds

**Upper bounds (proved).**

- With unlimited units, the least latency is the length of the critical path, found by ASAP in $O(V + E)$ time.
- With one unit type, $m$ units and any priority, list scheduling gives a latency at most $(2 - 1/m)$ times the optimum, by the [list scheduling bound](/list-scheduling-bound/) of Graham.
- For straight-line code and a fixed schedule, the least number of registers equals the largest number of values live in one step, and the left-edge algorithm reaches it in $O(V \log V)$ time.
- The scheduling decision version is in NP: a schedule is a certificate, checked in polynomial time.

**Lower bounds (proved, as hardness).**

- Resource-constrained scheduling is NP-complete already with one unit type, unit delays and the number of units given as part of the input (Ullman 1975). The time-constrained form is NP-hard by the same result, since "is there a schedule of latency $L$ with $m$ units" is the same question.
- For values that live across the boundary of a loop iteration, the lifetimes are arcs of a circle, and the least number of registers is the chromatic number of a circular-arc graph, which is NP-hard to find (Garey, Johnson, Miller and Papadimitriou 1980).

**Measured.** Heuristics such as list scheduling and force-directed scheduling are judged by runs on benchmark graphs such as the differential equation example, not by proved bounds. On 750 small random instances with at most 6 operations, made by the random generator of the force-directed scheduling tests, that heuristic needed one unit more than the optimum on 16 of them. This is a measurement on small random graphs only.

## Reductions

- **From multiprocessor scheduling.** Scheduling unit-time tasks with precedence on $m$ processors is the special case with one unit type, $m$ units and unit delays. This gives the NP-hardness above.
- **To integer programming.** Scheduling with unit limits and binding become 0-1 integer programs.
- **Register binding to interval coloring.** For straight-line code, register binding is the coloring of an interval graph, which is [chordal](/chordal-graph/), so a greedy order by start time is optimal.
- **Related compiler problems.** Scheduling is close to the [instruction scheduling problem](/instruction-scheduling-problem/), and register binding is close to the [register allocation problem](/register-allocation-problem/). The difference is that high-level synthesis can choose how many units and registers to build.

## Applications

- **Hardware accelerators.** HLS tools turn C, C++ or SystemC kernels into hardware for FPGAs and ASICs, for signal processing, image processing and machine learning.
- **Design space exploration.** Running the flow with many constraints gives the area and latency trade-off before any detailed design.
- **DSP datapaths.** Filters and transforms with fixed data flow are the classic case, where the schedule is static.
- **Sequential optimization after HLS.** The result is a register transfer design, which then goes through logic synthesis, [retiming](/retiming/) and [technology mapping](/technology-mapping/).

## References
