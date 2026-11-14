---
tag: CDK7W8
kind: algorithm
slug: force-directed-scheduling
name: Force-directed scheduling
aliases:
- Paulin-Knight scheduling
- time-constrained force-directed scheduling
area: cad/logic-synthesis
level: core
summary: Paulin and Knight's scheduler that fixes, one at a time, the operation and step with the least force, so the use of each unit type is balanced over steps.
solves: [high-level-synthesis]
model: word-ram
complexity:
  vars: {V: the number of operations, E: the number of data edges, L: the latency bound in steps}
  time: {worst: O(V^2 L (E + V L))}
  space: {extra: O(V L + E)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1989
  people: [Pierre G. Paulin, John P. Knight]
  note: Paulin and Knight gave force-directed scheduling for a fixed latency, and a force-directed list scheduler for fixed unit counts, in IEEE Transactions on Computer-Aided Design in 1989.
prereqs: [asap-alap-scheduling, high-level-synthesis]
see_also: [list-scheduling, expected-value, greedy-algorithm, binary-integer-programming, left-edge-algorithm, iterative-modulo-scheduling, resource-constrained-project-scheduling, simulated-annealing]
sources:
  - paper: doi:10.1109/43.31522
    title: Pierre G. Paulin and John P. Knight, Force-directed scheduling for the behavioral synthesis of ASICs, IEEE Transactions on Computer-Aided Design 8(6), 661 to 679, 1989
    locator: the time frames, the distribution graphs, the self and the predecessor and successor forces, the differential equation example, and force-directed list scheduling
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 5, Scheduling Algorithms (the section on heuristic scheduling algorithms and force-directed scheduling)
---

Force-directed scheduling (FDS) is a heuristic of [high-level synthesis](/high-level-synthesis/). It schedules the operations of a data flow graph within a fixed latency so that few functional units are needed. It starts from the time frames of [ASAP and ALAP scheduling](/asap-alap-scheduling/), and it treats each operation as if its start were spread evenly over its frame. Adding these spreads gives, for each unit type and step, the [expected](/expected-value/) number of operations in that step, the distribution graph. FDS then fixes one operation at one step at a time, the choice that lowers the peaks of the distribution graphs the most, which Paulin and Knight called the least force. The result always meets the precedences and the latency bound. It is not always the schedule with the fewest units.

## In plain words

You must fit a set of operations into a fixed number of clock steps, and you want to buy as few adders and multipliers as possible. That means the multiplies should not all fall into the same step. At the start, most operations can still move. For each operation, pretend that it is spread over all the steps it could use, a little bit in each. Add these bits up for each step, and you see where the crowd is. Now try each operation in each of its possible steps, and see how much the crowd moves toward the empty steps. Take the best move, fix it, and see which other operations lose freedom because of it. Repeat until every operation is fixed.

## The problem

The input is a data flow graph $G = (V, E)$ with no cycle, a unit type $k(v)$ and a delay $\delta(v) \ge 1$ for each operation, and a latency bound $L$. A schedule $t$ starts each $v$ at a step $t(v) \ge 1$, with $t(v) \ge t(u) + \delta(u)$ for each edge $(u, v)$ and $t(v) + \delta(v) - 1 \le L$. Operation $v$ uses the steps $t(v)$ to $t(v) + \delta(v) - 1$. The number of units of type $k$ that $t$ needs is the largest number of operations of type $k$ that use one step. The goal is a schedule that needs few units in total, the time-constrained form of the [high-level synthesis](/high-level-synthesis/) scheduling problem. That problem is NP-hard, and FDS does not solve it exactly.

## The algorithm

The time frame of $v$ is $[a(v), b(v)]$, its ASAP and its ALAP start, given the operations fixed so far. If each start in the frame has the same chance, the chance that $v$ uses step $j$ is
$$P_v(j) = \frac{\#\{ s \in [a(v), b(v)] : s \le j \le s + \delta(v) - 1 \}}{b(v) - a(v) + 1}.$$
The distribution graph of type $k$ is $\mathrm{DG}_k(j) = \sum_{v : k(v) = k} P_v(j)$. If a trial choice changes the frame of some operation $u$ and so changes $P_u$ to $P'_u$, the force of the change on $u$ is $\sum_j \mathrm{DG}_{k(u)}(j)\, (P'_u(j) - P_u(j))$. The total force of starting $v$ at $s$ is the sum of these forces over $v$ itself (the self force) and over all other operations whose frames shrink (the predecessor and successor forces). A negative force moves probability from crowded steps to empty ones.

```pseudo id=main
FORCE-DIRECTED-SCHEDULE(G, k, δ, L)
L1  fixed ← ∅; frames ← TIME-FRAMES(G, δ, L, fixed)
L2  if frames is "infeasible" then return "infeasible"
L3  loop
L4      for each v not in fixed whose frame is one step [s, s] do fixed(v) ← s
L5      if every v is in fixed then return fixed
L6      for each type k and step j do DG_k(j) ← Σ over v with k(v) = k of P_v(j)
L7      for each v not in fixed and each s in the frame of v do
L8          frames' ← TIME-FRAMES(G, δ, L, fixed with v at s)
L9          F(v, s) ← Σ over u with frames'(u) ≠ frames(u) of Σ_j DG_{k(u)}(j) (P'_u(j) - P_u(j))
L10     (v, s) ← the pair with the least F(v, s), the first one in the order of v and s on a tie
L11     fixed(v) ← s; frames ← TIME-FRAMES(G, δ, L, fixed)
```

TIME-FRAMES is the pair of passes of [ASAP and ALAP scheduling](/asap-alap-scheduling/), with the start of each fixed operation as both a lower and an upper bound. It reports "infeasible" when the bounds clash. All values here are exact fractions, so the comparison on line L10 and the tie rule do not depend on rounding.

## Example

Take the differential equation example of Paulin and Knight with $L = 4$ and unit delays. The operations $v_1, v_2, v_3, v_6, v_7, v_8$ are multiplies and $v_4, v_5, v_9, v_{10}, v_{11}$ are ALU operations, with the edges $v_1 \to v_3$, $v_2 \to v_3$, $v_3 \to v_4$, $v_4 \to v_5$, $v_6 \to v_7$, $v_7 \to v_5$, $v_8 \to v_9$ and $v_{10} \to v_{11}$. The frames are on the [ASAP and ALAP](/asap-alap-scheduling/) page. The first distribution graphs are:

| step | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| $\mathrm{DG}_{\text{mul}}$ | 17/6 | 7/3 | 5/6 | 0 |
| $\mathrm{DG}_{\text{alu}}$ | 1/3 | 1 | 2 | 5/3 |

For example, $\mathrm{DG}_{\text{mul}}(1) = 1 + 1 + \tfrac12 + \tfrac13$, from $v_1$ and $v_2$, which must start at step 1, $v_6$ with frame $[1, 2]$, and $v_8$ with frame $[1, 3]$. Some first forces:

| operation | frame | force at each start in the frame |
|---|---|---|
| $v_6$ | $[1, 2]$ | 1/4, −1 |
| $v_8$ | $[1, 3]$ | 5/6, 11/18, −19/18 |
| $v_{11}$ | $[2, 4]$ | −4/3, 0, 1/9 |

The force of $v_{11}$ at step 2 is its self force, $1 \cdot \tfrac23 - 2 \cdot \tfrac13 - \tfrac53 \cdot \tfrac13 = -\tfrac59$, plus the force on $v_{10}$, whose frame shrinks from $[1, 3]$ to $[1, 1]$, $\tfrac13 \cdot \tfrac23 - 1 \cdot \tfrac13 - 2 \cdot \tfrac13 = -\tfrac79$. The sum $-\tfrac43$ is the least force of all, so line L11 fixes $v_{11}$ at step 2, and $v_{10}$ is fixed at step 1 in the next round. The next choices are $v_8$ at step 3 with force $-\tfrac76$, and $v_6$ at step 2 with force $-\tfrac12$. Then all frames have one step, and the schedule is

| step | multiplies | ALU operations |
|---|---|---|
| 1 | $v_1, v_2$ | $v_{10}$ |
| 2 | $v_3, v_6$ | $v_{11}$ |
| 3 | $v_7, v_8$ | $v_4$ |
| 4 | | $v_5, v_9$ |

It needs 2 multipliers and 2 ALUs. A search over all schedules shows that 4 units in total is the least for $L = 4$, so FDS is optimal here. At $L = 5$ and $L = 6$, it finds schedules with 2 multipliers and 1 ALU.

## Correctness

What is proved: TIME-FRAMES returns frames that are exact, that is, a step is in the frame of $v$ exactly when some schedule that meets the fixed starts and $L$ starts $v$ there. So every trial on line L8 succeeds, the frames never become empty, and each round fixes at least one more operation. FDS stops after at most $V$ rounds and returns a schedule that meets all precedences and the latency bound $L$. It reports "infeasible" exactly when $L$ is less than the critical path length. It is deterministic.

What is not proved: FDS is not optimal. The force is a local, greedy estimate, and FDS comes with no proved bound on its distance from the optimum. The [full proof](proofs/correctness.md) gives the proved part.

## Complexity

There are at most $V$ rounds, since each one fixes an operation. A round has at most $VL$ trials. A trial runs TIME-FRAMES in $O(V + E)$ time and then sums over at most $V$ changed frames, each over $O(L)$ steps for unit delays, so it costs $O(E + VL)$. The total is $O(V^2 L (E + VL))$ time for unit delays, and $O(VL + E)$ space for the graph, the frames and the distribution graphs. Each delay $\delta(v) > 1$ adds a factor $\delta(v)$ to the work for its probabilities. Exact fractions make each arithmetic step cost more than a machine operation.

## Properties

- **Always feasible.** The schedule meets the precedences and the latency bound.
- **Not exact.** The schedule may need more units than the best one.
- **Deterministic.** With exact arithmetic and the tie rule of line L10, the same input gives the same schedule.
- **Global view.** Each choice looks at the effect on all operations whose frames change, not only on the one being fixed. This is the main difference from [list scheduling](/list-scheduling/), which decides step by step.

## Variants and improvements

- **Force-directed list scheduling.** For a fixed number of units of each type, Paulin and Knight run [list scheduling](/list-scheduling/) step by step, and when too many operations are ready, they defer those whose deferral has the least force. This is the resource-constrained form.
- **Unit costs.** Weight each distribution graph by the area of its unit type, so that a crowd of multipliers costs more than a crowd of adders.
- **Registers and buses.** Add distribution graphs for the values that are live in each step, or for the bus transfers, so that the forces also balance storage.
- **Look ahead.** Compute the force of a trial with the frames after one more step of propagation, at more cost per trial.
- **Exact methods.** For small graphs, a [0-1 integer programming](/binary-integer-programming/) model, with one variable for each operation and start step, gives the optimum and can check the quality of FDS.

## When to use it

Use FDS when the latency is fixed, for example by a throughput target, and the goal is to need few units. It suits graphs where its $VL$ trials per round are affordable, and it handles many unit types at once. When the unit counts are fixed and the latency should be small, use list scheduling or force-directed list scheduling. When an optimum is needed and the graph is small, use an exact method.

## Pitfalls

- **Not optimal.** Take one unit type, five unit-delay operations, the edges $v_1 \to v_3$, $v_2 \to v_3$, $v_2 \to v_4$, $v_3 \to v_5$ and $v_4 \to v_5$, and $L = 5$. The first least force is $-\tfrac{10}{9}$, for $v_3$ at step 2. It forces $v_1$ and $v_2$ into step 1, and the final schedule $(1, 1, 2, 4, 5)$ needs 2 units. The schedule $(1, 2, 3, 4, 5)$ needs only 1. In a measured run with the random generator of the tests, on 750 instances with at most 6 operations and latencies from the critical path length to 2 more, FDS needed one unit more than the optimum on 16 of them, and was optimal on the rest. This is a measurement on small random graphs, not a bound.
- **Rounding.** Probabilities like $1/3$ in floating point can turn a tie into a strict inequality, so two runs on different machines can give different schedules. Use exact fractions or a fixed tolerance.
- **Stale frames.** After a choice, the frames of other operations shrink. The distribution graphs must be rebuilt from the new frames before the next round, or the forces are computed for a state that no longer exists.
- **Negative forces are relative.** Force values are only compared with each other. A positive least force does not mean that the choice is bad.

## Implementations

## History

Paulin and Knight (1989) gave force-directed scheduling in the HAL system for the behavioral synthesis of ASICs. They described the probabilities as a time frame, the distribution graphs as a load, and the change in load as a force, by analogy with a spring. They also gave the force-directed list scheduler for fixed unit counts, and they used the differential equation example that later became a common benchmark. De Micheli's book (1994) presents FDS as the main heuristic for scheduling under a latency bound.

## References
