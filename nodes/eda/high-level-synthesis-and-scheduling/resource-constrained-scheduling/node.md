---
tag: ZK4WV9
kind: problem
slug: resource-constrained-scheduling
name: Resource-constrained scheduling
aliases:
- minimum-latency resource-constrained scheduling
- ML-RCS
area: eda/high-level-synthesis-and-scheduling
level: core
summary: Assign each operation of a sequencing graph to a control step so that no step uses more units of a type than allowed and the latency is least; NP-hard in general.
prereqs: [control-data-flow-graph, asap-alap-scheduling, np-hard]
see_also: [latency-constrained-scheduling, list-scheduling, hu-algorithm, coffman-graham-algorithm, precedence-constrained-scheduling, ilp-scheduling-formulation, sdc-scheduling, list-scheduling-bound]
sources:
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 5, Scheduling Algorithms (the section on scheduling with resource constraints)
  - paper: doi:10.1016/S0022-0000(75)80008-0
    title: "J. D. Ullman, NP-complete scheduling problems, Journal of Computer and System Sciences 10(3), 1975"
    locator: the NP-completeness of scheduling unit-time tasks with precedence constraints on a given number of processors
  - paper: doi:10.1287/opre.26.1.22
    title: J. K. Lenstra and A. H. G. Rinnooy Kan, Complexity of scheduling under precedence constraints, Operations Research 26(1), 22 to 35, 1978
    locator: deciding whether unit-time tasks with precedences fit in three steps on a given number of processors is NP-complete
  - paper: doi:10.1109/43.31522
    title: Pierre G. Paulin and John P. Knight, Force-directed scheduling for the behavioral synthesis of ASICs, IEEE Transactions on Computer-Aided Design 8(6), 661 to 679, 1989
    locator: resource-constrained scheduling by force-directed list scheduling, and the differential equation example
  - book: isbn:0716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: the list of open problems (precedence-constrained scheduling of unit tasks on a fixed number of processors)
---

Resource-constrained scheduling is the scheduling problem of [high-level synthesis](/high-level-synthesis/) in which the number of functional units of each type is fixed and the goal is the shortest schedule. The input is a sequencing graph of operations, the data flow graph of one block of a [control data flow graph](/control-data-flow-graph/), with a delay and a unit type for each operation. A schedule gives each operation a start step. It must respect the data edges, and in no step may more operations of one type run than there are units of that type. With one type and unit delays it is the classic problem of scheduling unit tasks with precedences on $m$ processors, which Ullman proved NP-complete in 1975. The partner problem, which fixes the latency and minimizes the units, is [latency-constrained scheduling](/latency-constrained-scheduling/).

## In plain words

You have a list of calculations, some of which need the result of others. You have, say, two multipliers and one adder, and each clock tick a unit can start one calculation. You want to finish everything in as few ticks as possible. The order of the needs gives a lower limit, because a long chain of dependent steps cannot be squeezed. The number of units gives another limit, because six multiplies on two multipliers need at least three ticks. The hard part is that both limits act at the same time, and a choice that looks good early can block a long chain later.

## Definition

**Input.**

- A sequencing graph $G = (V, E)$ with no cycle.
- For each operation $v \in V$, an integer delay $d(v) \ge 1$ in clock cycles and a type $t(v)$ from a set $K$ of unit types.
- For each type $k \in K$, a number of units $a_k \ge 1$.

**Feasible solutions.** A schedule is a map $s : V \to \{0, 1, 2, \ldots\}$ of start steps with

- $s(v) \ge s(u) + d(u)$ for each edge $(u, v) \in E$, and
- $\left|\{ v : t(v) = k,\ s(v) \le j < s(v) + d(v) \}\right| \le a_k$ for each type $k$ and each step $j$.

An operation keeps its unit busy for all of its $d(v)$ cycles: units are not pipelined. Each step is one clock cycle, and two dependent operations never share a step: there is no chaining.

**Objective.** Minimize the latency $\lambda(s) = \max_{v \in V} (s(v) + d(v))$, the number of steps until the last operation ends. With a source and a sink of delay 0, as in De Micheli's sequencing graphs, this equals $s(\text{sink}) - s(\text{source})$.

**Decision form.** Given the input and an integer $\lambda_0$, is there a schedule with $\lambda(s) \le \lambda_0$?

## Variants

- **Pipelined units.** A unit of type $k$ accepts a new operation every cycle, even though each result takes $d(v)$ cycles. Then an operation occupies its unit only in its first step, and the resource row counts $s(v) = j$ only.
- **Chaining.** Delays are real numbers and the clock period $T$ is given. Dependent operations may share a step when the sum of their delays fits in $T$. See [operation chaining](/operation-chaining/).
- **Several unit types per operation.** An operation can run on more than one type, for example an add on an adder or on an ALU, with different delays. Choosing the type is [module selection](/module-selection/).
- **Control flow.** Operations on different arms of a branch never run together, so they can share a unit in the same step. Schedulers for a whole CDFG, such as [path-based scheduling](/path-based-scheduling/), use this.
- **Loops.** For a loop body that starts a new iteration every $II$ cycles, the resource rows count operations modulo $II$. This is modulo scheduling, as in [SDC modulo scheduling](/sdc-modulo-scheduling/).
- **Timing constraints.** Upper and lower bounds on the distance between two starts, such as $s(v) - s(u) \le c$, are added rows. They can make the instance infeasible for every latency.

## Examples

Take the differential equation example of Paulin and Knight, with the operations, types and edges that the [high-level synthesis](/high-level-synthesis/) page gives: six multiplies, five ALU operations, unit delays and a critical path of 4 steps. The least latency for each pair of unit counts is

| multipliers | ALUs | least latency |
|---|---|---|
| 1 | 1, 2 or 3 | 7 |
| 2 | 1 | 5 |
| 2 | 2 or 3 | 4 |
| 3 | 1 | 5 |
| 3 | 2 or 3 | 4 |

With one multiplier, the six multiplies need 6 steps, and the last of them feeds an ALU operation, so 7 steps is a lower bound and it is reached. With two multipliers and two ALUs, the latency meets the critical path of 4. A third multiplier never helps here: the multiplies are not the limit once there are two.

For a small case where the choice in one step matters, take one type with two units, a chain $c_1 \to c_2 \to c_3$, and three operations $x, y, z$ with no edges, all of delay 1. Both lower bounds below give 3 steps. If step 0 runs $x$ and $y$, the chain starts one step late and the latency is 4. If step 0 runs $c_1$ and $x$, then step 1 runs $c_2$ and $y$, and step 2 runs $c_3$ and $z$, which gives 3. So a good schedule starts the long chain first, which is why list schedulers rank ready operations by the length of the path below them.

## Known algorithms

- **List scheduling.** Step by step, start the ready operations with the highest priority, up to $a_k$ per type. It is fast and not exact. See [list scheduling](/list-scheduling/), and for the bound for one type, [the list scheduling bound](/list-scheduling-bound/).
- **Hu's algorithm.** Exact when there is one type, unit delays and the graph is an in-tree. See [Hu's algorithm](/hu-algorithm/).
- **Coffman and Graham.** Exact for one type with two units and unit delays. See [the Coffman-Graham algorithm](/coffman-graham-algorithm/).
- **Integer programming.** A 0-1 program with one variable per operation and step gives the optimum for small graphs. See [the ILP formulation](/ilp-scheduling-formulation/).
- **SDC scheduling.** Writes the resource bounds as extra difference constraints from a fixed order and solves an LP. It is fast and not exact under resource bounds. See [SDC scheduling](/sdc-scheduling/).
- **Force-directed list scheduling.** List scheduling that defers the ready operations whose deferral has the least force, by Paulin and Knight. See [force-directed scheduling](/force-directed-scheduling/).
- **Branch and bound.** Search over the choices of each step, cut off by the lower bounds below. See [depth-first branch and bound](/depth-first-branch-and-bound/).

## Bounds

Let $\mathrm{CP}$ be the critical path, the largest sum of delays on a path of $G$, and let $W_k = \sum_{t(v) = k} d(v)$ be the work of type $k$.

**Lower bound.** Every schedule has $\lambda \ge \max(\mathrm{CP}, \max_k \lceil W_k / a_k \rceil)$. The first term holds because the operations of a path run one after another. The second holds because each step gives at most $a_k$ busy cycles of type $k$.

**Upper bound for any greedy list schedule.** Call a list schedule greedy if it never leaves a unit of type $k$ idle in a step where an operation of type $k$ is ready and waiting. Then, with $|K|$ unit types,
$$\lambda \le \mathrm{CP} + \sum_{k \in K} \frac{W_k}{a_k} \le (|K| + 1)\,\lambda^*.$$
Proof: let $v_1$ be an operation that ends last. Given $v_i$, let $v_{i+1}$ be a predecessor of $v_i$ that ends last, and stop when $v_i$ has no predecessor. This is a path, so the steps in which some $v_i$ runs number at most $\mathrm{CP}$. Take any other step $j$ before the end. It lies between the end of some $v_{i+1}$ and the start of $v_i$, or before the start of the first one. In that step all predecessors of $v_i$ have ended, so $v_i$ is ready and waiting, and by greed all $a_{t(v_i)}$ units of its type are busy. A step in which all units of type $k$ are busy uses $a_k$ cycles of the work $W_k$, so there are at most $W_k / a_k$ such steps for each $k$. Adding up gives the first inequality, and each term is at most $\lambda^*$ by the lower bound. For one type the bound is $2 \lambda^*$, and Graham's finer analysis gives $2 - 1/a$. With chaining or with timing constraints, this argument fails, because a ready operation may be unable to start for reasons other than busy units.

**Hardness of approximation.** For one type and unit delays, deciding whether $\lambda^* \le 3$ is NP-complete (Lenstra and Rinnooy Kan, 1978). So no polynomial algorithm guarantees a latency below $\tfrac43 \lambda^*$ unless P = NP.

## Reductions

**In NP.** A schedule with $\lambda \le \lambda_0$ has all starts below $\lambda_0$, so it can be written down and checked against every edge and every step in polynomial time when $\lambda_0$ is at most $\sum_v d(v)$. A larger $\lambda_0$ makes the answer trivially yes, because running the operations one at a time in a topological order takes $\sum_v d(v)$ steps.

**NP-hard (Ullman 1975).** The special case with one type, $d(v) = 1$ for all $v$ and $a$ units is the problem of scheduling unit-time tasks with precedences on $a$ processors to finish by a deadline. A schedule here is the same object as a processor schedule there: a start step for each task, with at most $a$ tasks per step, and each task after its predecessors. Ullman proved this problem NP-complete when $a$ is part of the input. So the decision form above is NP-complete, and the optimization form is NP-hard. All numbers in the hard instances are small, so the problem is NP-hard in the strong sense.

**Small cases.** For one type and a fixed number $a \ge 3$ of units, the complexity is a long-standing open problem from the list of Garey and Johnson. For $a = 2$ and unit delays, the Coffman-Graham algorithm solves it, and for in-trees with any $a$, Hu's algorithm does.

**To latency-constrained scheduling.** The decision form is the same question as the decision form of [latency-constrained scheduling](/latency-constrained-scheduling/): units $a_k$ and latency $\lambda_0$. So a polynomial algorithm for either optimization form would answer it, and both are NP-hard.

## Applications

- **High-level synthesis.** Schedule each block of a CDFG when the designer fixes the units, for example to fit an area budget or an FPGA with few DSP blocks.
- **Instruction scheduling.** A compiler for a processor with fixed functional units solves the same problem on each basic block. See [the instruction scheduling problem](/instruction-scheduling-problem/).
- **Project scheduling.** Tasks with precedences and limited crews or machines give the same model with general delays.
- **Design space exploration.** Solving it for each unit vector gives the latency side of the area and latency trade-off curve.

## References
