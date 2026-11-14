---
tag: D7QMPD
kind: problem
slug: latency-constrained-scheduling
name: Latency-constrained scheduling
aliases:
- time-constrained scheduling
- minimum-resource latency-constrained scheduling
area: eda/high-level-synthesis-and-scheduling
level: core
summary: Schedule the operations of a sequencing graph within a given number of control steps so that the number of functional units needed is least.
prereqs: [control-data-flow-graph, asap-alap-scheduling, np-hard]
see_also: [resource-constrained-scheduling, force-directed-scheduling, ilp-scheduling-formulation, sdc-scheduling, resource-binding, module-selection, precedence-constrained-scheduling]
sources:
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 5, Scheduling Algorithms (the sections on scheduling with resource constraints and on force-directed scheduling)
  - paper: doi:10.1109/43.31522
    title: Pierre G. Paulin and John P. Knight, Force-directed scheduling for the behavioral synthesis of ASICs, IEEE Transactions on Computer-Aided Design 8(6), 661 to 679, 1989
    locator: time-constrained scheduling, the distribution graphs and the differential equation example
  - paper: doi:10.1016/S0022-0000(75)80008-0
    title: "J. D. Ullman, NP-complete scheduling problems, Journal of Computer and System Sciences 10(3), 1975"
    locator: the NP-completeness of scheduling unit-time tasks with precedence constraints on a given number of processors
---

Latency-constrained scheduling is the scheduling problem of [high-level synthesis](/high-level-synthesis/) in which the number of control steps is fixed and the goal is to need as few functional units as possible. The latency bound usually comes from a throughput target or from a real-time deadline. The input is a sequencing graph with a delay and a unit type for each operation, and a cost for each unit type, such as its area. A schedule must respect the data edges and end within the bound. The units of a type that it needs are the largest number of operations of that type that run in one step, and the cost is the weighted sum of these numbers. It is the partner of [resource-constrained scheduling](/resource-constrained-scheduling/), which fixes the units and minimizes the latency, and it is NP-hard for the same reason.

## In plain words

You must finish a set of dependent calculations within a fixed number of clock ticks. You do not care how fast within that limit, but every multiplier and adder that the chip needs costs area. If many multiplies fall in the same tick, you must build many multipliers. So you want to spread the operations of each kind evenly over the ticks, without breaking the order that the data needs. A tight deadline leaves little room to spread, and a loose one leaves a lot.

## Definition

**Input.**

- A sequencing graph $G = (V, E)$ with no cycle.
- For each operation $v$, an integer delay $d(v) \ge 1$ and a type $t(v) \in K$.
- A latency bound $L$, an integer.
- A cost $c_k > 0$ for each type $k$.

**Feasible solutions.** A schedule $s : V \to \{0, 1, \ldots\}$ with $s(v) \ge s(u) + d(u)$ for each edge $(u, v)$ and $s(v) + d(v) \le L$ for each $v$. Units are not pipelined and there is no chaining, as in resource-constrained scheduling.

**Objective.** The schedule needs
$$a_k(s) = \max_{0 \le j < L} \left|\{ v : t(v) = k,\ s(v) \le j < s(v) + d(v) \}\right|$$
units of type $k$. Minimize the cost $\sum_{k \in K} c_k\, a_k(s)$.

**Decision form.** Given the input and a cost $C$, is there a schedule with cost at most $C$?

A feasible schedule exists exactly when $L$ is at least the critical path, the largest sum of delays on a path of $G$, since the ASAP schedule ends at the critical path.

## Variants

- **Registers and interconnect.** Add the registers, which follow the number of values live across a step, and the multiplexers to the cost. The schedule then fixes more of the area.
- **Several unit types per operation.** Each operation may run on more than one type, with different delays and costs. The schedule and the [module selection](/module-selection/) are then chosen together.
- **Pipelined units.** An operation occupies its unit only in its first step, so the count runs over starts only.
- **Chaining.** The clock period is given and dependent operations may share a step. See [operation chaining](/operation-chaining/).
- **Loops with a target initiation interval.** The latency bound is replaced by a bound $II$ on the distance between iterations, and the units are counted modulo $II$.
- **Power.** Minimize the peak or the variance of the number of active units per step, which is the same kind of balancing.

## Examples

Take the differential equation example of Paulin and Knight, with the operations and edges that the [high-level synthesis](/high-level-synthesis/) page gives: six multiplies, five ALU operations, unit delays and a critical path of 4. With the cost 1 for each unit, the optimum for each latency bound is

| latency bound $L$ | multipliers | ALUs | units in total |
|---|---|---|---|
| 3 | none | none | infeasible |
| 4 | 2 | 2 | 4 |
| 5 | 2 | 1 | 3 |
| 6 | 2 | 1 | 3 |
| 7 | 1 | 1 | 2 |

At $L = 4$, at least 2 multipliers are needed: the paths $v_1 \to v_3 \to v_4 \to v_5$ and $v_2 \to v_3 \to v_4 \to v_5$ have 4 operations each, so the multiplies $v_1$ and $v_2$ must both run in step 0. At $L = 6$, one multiplier is still too few, because six multiplies in a row take steps 0 to 5 and the last one feeds an ALU operation that would end at step 7. The schedule on the [force-directed scheduling](/force-directed-scheduling/) page reaches the optimum at $L = 4$.

A second example shows why the bound matters for balance. Take four independent additions and $L = 2$. A schedule that puts all four in step 0 needs 4 adders. Two in each step need 2, the optimum, which meets the lower bound $\lceil 4 / 2 \rceil$.

## Known algorithms

- **Force-directed scheduling.** Paulin and Knight's heuristic balances the expected use of each type over the steps. See [force-directed scheduling](/force-directed-scheduling/).
- **Integer programming.** The 0-1 program with one variable per operation and step, plus one integer variable $a_k$ per type, gives the optimum for small graphs. See [the ILP formulation](/ilp-scheduling-formulation/).
- **Search over unit vectors.** For each unit vector $a$ in order of cost, run a resource-constrained scheduler and stop at the first $a$ whose latency is at most $L$. This is exact if the inner scheduler is exact. With list scheduling inside it is a heuristic.
- **SDC scheduling.** An LP over difference constraints can minimize a linear proxy, such as the sum of starts or a lifetime cost, under the latency bound. It does not count units exactly. See [SDC scheduling](/sdc-scheduling/).
- **Branch and bound.** Search over the frames of the operations, cut off by the lower bounds below.

## Bounds

Let $a(v)$ and $b(v)$ be the ASAP and ALAP starts of $v$ for the bound $L$, from [ASAP and ALAP scheduling](/asap-alap-scheduling/). Every schedule has $a(v) \le s(v) \le b(v)$.

**Window bound.** For steps $j_1 < j_2$, let $W_k[j_1, j_2]$ be the sum of $d(v)$ over the operations of type $k$ with $a(v) \ge j_1$ and $b(v) + d(v) \le j_2$. In every schedule these operations run entirely inside the steps $j_1$ to $j_2 - 1$, which offer $a_k (j_2 - j_1)$ busy cycles of type $k$. So
$$a_k \ge \max_{j_1 < j_2} \left\lceil \frac{W_k[j_1, j_2]}{j_2 - j_1} \right\rceil.$$
With $j_1 = 0$ and $j_2 = L$ this gives $a_k \ge \lceil W_k / L \rceil$. Narrow windows give better bounds: in the example at $L = 4$, the window from step 0 to 1 holds $v_1$ and $v_2$, which gives 2 multipliers.

**Monotone in $L$.** A schedule for $L$ is also a schedule for $L + 1$, so the optimum cost does not rise as $L$ grows. It reaches $\sum_k c_k$, one unit of each type that occurs, once $L$ is large enough for a schedule that runs one operation of each type at a time.

**Trade-off curve.** For one type, the optimum for $L$ is the least $a$ whose resource-constrained optimum is at most $L$. So the two problems give the same curve of latency against units, read along different axes.

## Reductions

**In NP.** A schedule is a certificate: its starts are below $L$, and the edges, the bound and the cost can be checked in time polynomial in $|V| + |E|$ and $L$. If $L$ exceeds $\sum_v d(v)$, it can be replaced by $\sum_v d(v)$ without changing the answer, since every schedule can be shifted to start each operation no later than that.

**NP-hard.** Take one type with cost 1 and unit delays. The question "is there a schedule within $L$ that needs at most $m$ units" is the question "can unit-time tasks with precedences finish by the deadline $L$ on $m$ processors". Ullman (1975) proved this NP-complete when $m$ and $L$ are part of the input. So the decision form is NP-complete, and minimizing the units is NP-hard. The hard instances have small numbers, so the hardness holds in the strong sense.

**Equivalence with resource-constrained scheduling.** For one type, an algorithm for either optimization problem solves the other with a binary search over $L$ or over $m$, and $L$ and $m$ need not exceed $|V| \cdot \max_v d(v)$ and $|V|$. So the two problems are polynomially equivalent.

## Applications

- **Signal processing datapaths.** A filter or a transform must take a new sample every fixed number of cycles, which fixes $L$. The goal is the smallest datapath.
- **Real-time control.** A control loop has a deadline per period, and the unit count sets the cost of the chip.
- **Low power.** Spreading the operations evenly lowers the peak current and the number of units that must be powered.
- **Design space exploration.** Solving it for each $L$ gives the area side of the area and latency trade-off curve.

## References
