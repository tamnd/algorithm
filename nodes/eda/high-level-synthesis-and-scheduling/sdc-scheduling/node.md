---
tag: 11PCP9
kind: algorithm
slug: sdc-scheduling
name: SDC-based scheduling
aliases:
- system of difference constraints scheduling
- Cong-Zhang scheduling
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Cong and Zhang's scheduler that writes timing, latency and relative constraints as difference constraints, so the LP is totally unimodular and gives integer schedules.
solves: [resource-constrained-scheduling, latency-constrained-scheduling]
model: word-ram
complexity:
  vars: {V: the number of operations, E: the number of data edges, C: the number of difference constraints}
  time: {worst: O(V (V + E) + V C)}
  space: {extra: O(V^2 + C)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2006
  people: [Jason Cong, Zhiru Zhang]
  note: Cong and Zhang gave the SDC formulation of scheduling at the Design Automation Conference in 2006, as the scheduler of the xPilot high-level synthesis system.
prereqs: [difference-constraints, total-unimodularity, asap-alap-scheduling, control-data-flow-graph]
see_also: [resource-constrained-scheduling, operation-chaining, ilp-scheduling-formulation, sdc-modulo-scheduling, bellman-ford, linear-programming-problem, min-cost-flow-problem, list-scheduling]
sources:
  - paper: doi:10.1145/1146909.1147025
    title: Jason Cong and Zhiru Zhang, An efficient and versatile scheduling algorithm based on SDC formulation, Proceedings of the 43rd Design Automation Conference, 433 to 438, 2006
    locator: the dependence, cycle time, timing, latency and resource constraints of Section 3, the objectives of Section 3.4, and the network flow dual of Section 3.5
  - paper: doi:10.1109/43.75629
    title: Cheng-Tsung Hwang, Jiahn-Humg Lee and Yu-Chin Hsu, A formal approach to the scheduling problem in high level synthesis, IEEE Transactions on Computer-Aided Design 10(4), 464 to 475, 1991
    locator: the 0-1 model that SDC scheduling replaces by one integer variable per operation
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 22.4, Difference constraints and shortest paths
---

SDC-based scheduling is a scheduler of [high-level synthesis](/high-level-synthesis/) by Cong and Zhang (2006). It gives each operation one integer variable, its start step, and writes every rule of the schedule as a difference constraint $s_v - s_u \ge w$: data dependences, chaining within the clock period, minimum and maximum distances between operations, and a latency bound. A system of [difference constraints](/difference-constraints/) has a constraint matrix in which each row has one $+1$ and one $-1$. Such a matrix is [totally unimodular](/total-unimodularity/), so a linear program over it has an integral optimal vertex, and a linear objective can be optimized in polynomial time with no integer search. Resource limits do not fit this form, so the scheduler turns them into extra difference constraints from a fixed order of the operations of each type. That step is a heuristic: the schedule always meets the limits, but it is not always the shortest one.

## In plain words

Give each operation a number, the clock step in which it starts. Every rule becomes "this number minus that number is at least so much": the multiply must start two steps after the add that feeds it, the three adds in a row do not fit in one clock, everything must end by step ten. Rules of this simple shape are easy. The smallest numbers that obey them all come from a longest path search, and any other straight-line goal is solved exactly by a linear program, which here never answers with fractions. The one rule that does not fit is "at most two multiplies per step". The trick is to line up the multiplies and say "the third one starts after the first one ends", which keeps the simple shape but may waste a step.

## The problem

The input is one data flow graph $G = (V, E)$ with no cycle. Each operation $v$ has a latency $\ell(v) \ge 0$ in cycles, a combinational delay $\delta(v)$, and a type $k(v)$. An operation with $\ell(v) = 0$ is combinational: it may run in the same step as its predecessors, and its delay must be at most the clock period $T$. An operation with $\ell(v) \ge 1$ registers its result, so it breaks combinational paths, and it keeps its unit busy for $o(v) = \max(1, \ell(v))$ steps. Some types have a limit $a_k$ on their units. A schedule $s : V \to \{0, 1, \ldots\}$ is valid when

- $s_v \ge s_u + \ell(u)$ for each edge $(u, v)$;
- every path of combinational operations that all start in one step has a total delay of at most $T$;
- in each step, at most $a_k$ operations of type $k$ are busy;
- if a latency bound $L$ is given, $s_v + o(v) \le L$ for all $v$.

The goal is a valid schedule that minimizes a linear cost $\sum_v w_v s_v$, such as the sum of the starts, or that has a small latency $\max_v (s_v + o(v))$. With the resource limits this contains [resource-constrained scheduling](/resource-constrained-scheduling/), which is NP-hard, so no polynomial method is exact for it unless P = NP.

## The algorithm

For two combinational operations $u$ and $v$ joined by a path of combinational operations, let $D(u, v)$ be the largest total delay of such a path, counting both ends. Write each constraint as a triple $(u, v, w)$ for $s_v - s_u \ge w$.

```pseudo id=main
SDC-SCHEDULE(G, ℓ, δ, k, a, T, L, w)
L1  C ← ∅
L2  for each edge (u, v) of G do add s_v − s_u ≥ ℓ(u) to C
L3  for each pair (u, v) with D(u, v) > T do add s_v − s_u ≥ ⌈D(u, v) / T⌉ − 1 to C
L4  compute ASAP(v) and ALAP(v) for each v from C, by longest paths
L5  for each type k with a limit a_k do
L6      o ← the operations of type k, sorted by (ALAP, ASAP, topological index)
L7      for i ← 1 to |o| − a_k do add s_{o[i + a_k]} − s_{o[i]} ≥ max(1, ℓ(o[i])) to C
L8  if L is given then add s_v ≤ L − max(1, ℓ(v)) for each v
L9  s* ← the least s ≥ 0 that meets C, by longest paths; if there is none or s* breaks L8 then return "infeasible"
L10 if every w_v ≥ 0 then return s*
L11 return an optimal vertex of the LP: minimize Σ w_v s_v subject to C, the bounds of L8 and s ≥ 0
```

Lines L2 and L3 are exact: they hold for a schedule exactly when its dependences and its clock period hold. Line L7 links the operations of type $k$ into $a_k$ chains, positions $i, i + a_k, i + 2a_k, \ldots$ of the order, and in each chain an operation starts only after the previous one is no longer busy. User constraints, such as a maximum distance $s_v - s_u \le c$, enter $C$ as $s_u - s_v \ge -c$. Line L9 is [Bellman-Ford](/bellman-ford/) for longest paths from an imaginary source with an edge of weight 0 to each operation. Line L11 needs the bound $L$ so that the LP is bounded. Cong and Zhang point out that the dual of this LP is a [minimum cost flow](/min-cost-flow-problem/) problem, which polynomial network algorithms solve. The implementation here uses an exact [simplex method](/simplex-method/) with Bland's rule, which is enough for small graphs.

## Example

Take $T = 5$ and six operations: $v_0 = a + b$, $v_1 = v_0 + c$, $v_2 = v_1 + d$, $v_3 = v_0 \cdot e$, $v_4 = f \cdot g$ and $v_5 = v_3 + v_4$. Adds are combinational with delay 2, and multiplies have latency 2. Lines L2 and L3 give

| constraint | reason |
|---|---|
| $s_1 - s_0 \ge 0$, $s_2 - s_1 \ge 0$, $s_3 - s_0 \ge 0$ | data edges from adds |
| $s_5 - s_3 \ge 2$, $s_5 - s_4 \ge 2$ | data edges from multiplies |
| $s_2 - s_0 \ge 1$ | $D(v_0, v_2) = 6 > 5$, so $\lceil 6/5 \rceil - 1 = 1$ |

The pairs $(v_0, v_1)$ and $(v_1, v_2)$ have $D = 4 \le 5$, so two adds may chain but three may not. With no unit limit, the least solution is $s = (0, 0, 1, 0, 0, 2)$, with latency 3.

Now allow one multiplier. Line L4 gives ALAP 0 for both $v_3$ and $v_4$, and equal ASAP values, so the topological index puts $v_3$ first. Line L7 adds $s_4 - s_3 \ge 2$. The least solution is $s = (0, 0, 1, 0, 2, 4)$ with latency 5, which is optimal: the two multiplies need four steps on one unit, and $v_5$ follows the second one.

With $L = 5$ and the weights $w_v = -1$, line L11 maximizes the sum of the starts, an ALAP-like schedule. The LP gives $s = (0, 4, 4, 0, 2, 4)$, an integer vertex. The adds $v_1$ and $v_2$ chain in step 4, with delay 4.

The resource step can lose. Take three independent operations of one type with two units and latencies 1, 2 and 1. Line L4 gives ALAP starts 1, 0 and 1, so the order is $v_1, v_0, v_2$, and line L7 adds $s_2 - s_1 \ge 2$. The schedule has latency 3. The optimum is 2: $v_1$ on one unit in steps 0 and 1, and $v_0$ then $v_2$ on the other.

## Correctness

What is proved, in the [full proof](proofs/correctness.md):

- **Total unimodularity.** The matrix of $C$ with the bound rows of L8 is totally unimodular. So every vertex of the feasible region is integral, and line L11 returns an integer schedule.
- **Least solution.** The solutions of $C$ with $s \ge 0$ are closed under the componentwise minimum, and line L9 finds the least one or proves that none exists. With all $w_v \ge 0$ it is optimal, so line L10 is exact.
- **Exact chaining.** A schedule meets the rows of L2 and L3 exactly when it meets the dependences and every in-step combinational path fits in $T$.
- **Sound resources.** Every solution of the rows of L7 uses at most $a_k$ units of type $k$ in each step.
- **Always feasible without bounds.** With no latency bound and no user constraint, every row of $C$ goes forward in the order of line L6 extended to all operations, so $C$ has no positive cycle and a schedule always exists.

What is not proved, and is false: that the schedule has the least latency under resource limits. The last example shows a loss of one step. In a measured run of the tests, with 150 random graphs of at most 7 operations, two types and limits of 1 or 2, the latency was above the exhaustive optimum on 4 of them. This is a measurement on small random graphs, not a bound.

## Complexity

Line L3 computes $D$ by one pass over the graph for each combinational operation, in $O(V (V + E))$ time, and adds at most $V^2$ rows. Lines L5 to L7 add fewer than $V$ rows in all. Lines L4 and L9 run Bellman-Ford in $O(V C)$ time, where $C$ is at most $E + V^2 + V$. So the case of nonnegative weights takes $O(V (V + E) + V C)$ time and $O(V^2 + C)$ space. Line L11 solves an LP with $V$ variables and $C + V$ rows. As a minimum cost flow dual it takes polynomial time. The simplex method of the implementation has no polynomial bound in the worst case.

## Properties

- **Exact for timing, heuristic for resources.** All dependence, chaining, latency and relative timing rules are exact. Resource limits are met but may cost latency.
- **Integral without branching.** No integer program is solved. The LP optimum is integral because of the matrix structure, not because of rounding.
- **Global objective.** Unlike [list scheduling](/list-scheduling/), which decides step by step, the LP sees all operations at once, so the objective can be the sum of the starts, the slack of the edges or the lifetimes of values.
- **Incremental.** Adding one constraint changes the least solution by a longest path update from the changed node, so a tool can add and remove constraints cheaply.
- **Deterministic.** The order of line L6 has a full tie-break, and the simplex method uses Bland's rule.

## Variants and improvements

- **Other objectives.** Cong and Zhang list the ASAP and ALAP objectives, the latency of the exit block, an expected latency from a profile, and the total slack of the edges, which is a linear cost with mixed signs and so needs the LP.
- **Several blocks.** For a whole [control data flow graph](/control-data-flow-graph/), each block gets a super source and a super sink, and the control edges become difference constraints between them.
- **Pipelined units.** A unit that accepts a new operation every cycle needs a separation of 1 in line L7, or the initiation interval of the unit.
- **Better resource orders.** The order of line L6 can come from a list schedule, or be repaired after the LP when it causes a loss, in a loop.
- **Loops.** [SDC modulo scheduling](/sdc-modulo-scheduling/) adds constraints with the initiation interval for the edges that cross iterations, and handles the modulo resource limits by an incremental repair.
- **Exact resources.** The [ILP formulation](/ilp-scheduling-formulation/) models the limits exactly, at the cost of one binary variable per operation and step.

## When to use it

Use SDC scheduling when the schedule must meet many timing rules at once: a clock period with chaining, minimum and maximum distances to interface signals, latency bounds. Use it when a global linear objective matters. It is the scheduler of xPilot and of the LegUp system. When resource limits are tight and the latency matters most, check its result against a list scheduler or an exact model on small blocks.

## Pitfalls

- **Not exact under resource limits.** Do not call the schedule optimal when line L7 added rows. The rows depend on the order, and a different order can give a shorter schedule.
- **Separation of combinational operations.** If line L7 used the latency $\ell(o[i])$ as the separation, two combinational operations of one limited type, with $\ell = 0$, could still share a step, and a step could hold more than $a_k$ of them. Use $\max(1, \ell)$.
- **A full tie-break.** If the order of line L6 breaks ties by something other than a topological order, it can put $v$ before its predecessor $u$ when both have the same ALAP and ASAP, and then the rows of L7 and the data edge form a positive cycle.
- **Bounded LP.** Negative weights need upper bounds on the starts, or the LP is unbounded.
- **Floating point.** An LP solver in floating point can return a vertex such as 2.9999999. Round only after checking the result against $C$.
- **Delays on the edges.** Chaining rows must use the largest delay over all combinational paths between two operations, not the delay of one path.

## Implementations

## History

Hwang, Lee and Hsu (1991) had written HLS scheduling as a 0-1 integer program with one variable per operation and step. Cong and Zhang (2006) noticed that most scheduling rules are differences of start times, so one integer variable per operation and an LP suffice when the resource rule is relaxed into an order. They used it in the xPilot system at UCLA, with chaining, timing constraints and several objectives in one model. Zhang and Liu (2013) extended it to loop pipelining. The LegUp system at the University of Toronto also uses SDC scheduling.

## References
