---
tag: 5S0Z4R
kind: algorithm
slug: asap-alap-scheduling
name: ASAP and ALAP scheduling
aliases:
- as soon as possible scheduling
- as late as possible scheduling
- operation mobility
area: eda/logic-synthesis
level: intro
summary: Schedules each operation of a data flow graph at its earliest or latest step under precedence, which gives the mobility of each operation.
solves: [high-level-synthesis]
model: word-ram
complexity:
  vars: {V: the number of operations, E: the number of data edges}
  time: {worst: O(V + E)}
  space: {extra: O(V + E)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1959
  people: [James E. Kelley Jr., Morgan R. Walker]
  note: The two schedules are the forward and backward passes of the critical path method for project planning. High-level synthesis took them over as the time frames of the operations, for example in the force-directed scheduler of Paulin and Knight (1989).
prereqs: [topological-sort, dag-longest-path]
see_also: [force-directed-scheduling, critical-path-method, list-scheduling, critical-path, precedence-constrained-scheduling, instruction-scheduling-problem, kahns-algorithm, hu-algorithm]
sources:
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 5, Scheduling Algorithms (the sections on scheduling without resource constraints, ASAP and ALAP, and mobility)
  - paper: doi:10.1109/43.31522
    title: Pierre G. Paulin and John P. Knight, Force-directed scheduling for the behavioral synthesis of ASICs, IEEE Transactions on Computer-Aided Design 8(6), 661 to 679, 1989
    locator: the time frames of the operations from the ASAP and ALAP schedules, and the differential equation example
  - paper: doi:10.1145/1460299.1460318
    title: James E. Kelley Jr. and Morgan R. Walker, Critical-path planning and scheduling, Papers presented at the Eastern Joint IRE-AIEE-ACM Computer Conference, December 1959
    locator: the earliest and latest start times of the jobs of a project (general locator)
---

ASAP and ALAP scheduling give each operation of a data flow graph a start step when there is no limit on the number of functional units. The as soon as possible (ASAP) schedule starts every operation at the first step after all its inputs are ready. The as late as possible (ALAP) schedule starts every operation at the last step that still lets all the operations after it end by a latency bound $L$. Both schedules are one pass of a [DAG longest path](/dag-longest-path/) computation in [topological order](/topological-sort/), so each takes $O(V + E)$ time. The difference ALAP minus ASAP is the mobility of an operation, and the interval between them is its time frame. [High-level synthesis](/high-level-synthesis/) uses the ASAP schedule for the least latency, and uses the time frames as the input of resource-constrained schedulers such as [force-directed scheduling](/force-directed-scheduling/).

## In plain words

A program for hardware is a set of operations, such as multiplies and adds. Some operations need the result of others. A clock step is the unit of time, and each operation takes one or more steps. If you have as many adders and multipliers as you want, you can start each operation as soon as its inputs are ready. That is the ASAP schedule, and its length is the shortest possible. If you must finish by some step, you can also start each operation as late as possible, so that the work after it still fits. That is the ALAP schedule. An operation whose two start steps are the same is on the critical path and has no freedom. An operation with a gap between them can move inside that gap.

## The problem

The input is a data flow graph $G = (V, E)$ with no cycles. Each operation $v$ has a delay $\delta(v) \ge 1$ in control steps. An edge $(u, v)$ means that $v$ reads the result of $u$, so a schedule $t : V \to \{1, 2, \dots\}$ must have $t(v) \ge t(u) + \delta(u)$. Operation $v$ uses the steps $t(v)$ to $t(v) + \delta(v) - 1$. The schedule meets the latency bound $L$ when $t(v) + \delta(v) - 1 \le L$ for all $v$. The output is the ASAP schedule $t_S$, the ALAP schedule $t_L$ for a given $L$, and the mobility $\mu(v) = t_L(v) - t_S(v)$. The algorithm has no limit on the number of units. With such a limit, the problem is NP-hard (see the [high-level synthesis](/high-level-synthesis/) page).

## The algorithm

```pseudo id=main
ASAP(G, δ)
L1  order ← a topological order of G       ▷ fails if G has a cycle
L2  for each v in order do
L3      t_S(v) ← max(1, max over edges (u, v) of t_S(u) + δ(u))
L4  return t_S

ALAP(G, δ, L)
L5  for each v in the reverse of order do
L6      t_L(v) ← min(L + 1, min over edges (v, w) of t_L(w)) - δ(v)
L7  if t_L(v) < 1 for some v then return "infeasible"
L8  return t_L

MOBILITY(G, δ, L)
L9  return t_L(v) - t_S(v) for each v
```

Line L3 takes the latest end of an input, so $t_S(v) - 1$ is the largest total delay of a path that ends just before $v$. Line L6 is the mirror image: $L + 1 - t_L(v)$ is the largest total delay of a path that starts at $v$, with $v$ counted. The value $L + 1$ on line L6 stands for a sink after the last step. Line L7 fails exactly when $L$ is less than the length of the critical path.

## Example

Take the differential equation example of Paulin and Knight, one loop step of a solver for $y'' + 3xy' + 3y = 0$. It has six multiplies and five ALU operations, all with delay 1. With $u = y'$, one loop step computes $u_1 = u - 3xu\,dx - 3y\,dx$, $y_1 = y + u\,dx$, $x_1 = x + dx$, and the test $x_1 < a$.

| op | computes | ASAP | ALAP at $L = 4$ | mobility |
|---|---|---|---|---|
| $v_1$ | $3 \cdot x$ | 1 | 1 | 0 |
| $v_2$ | $u \cdot dx$ | 1 | 1 | 0 |
| $v_3$ | $v_1 \cdot v_2$ | 2 | 2 | 0 |
| $v_4$ | $u - v_3$ | 3 | 3 | 0 |
| $v_5$ | $v_4 - v_7$ | 4 | 4 | 0 |
| $v_6$ | $3 \cdot y$ | 1 | 2 | 1 |
| $v_7$ | $v_6 \cdot dx$ | 2 | 3 | 1 |
| $v_8$ | $u \cdot dx$ | 1 | 3 | 2 |
| $v_9$ | $y + v_8$ | 2 | 4 | 2 |
| $v_{10}$ | $x + dx$ | 1 | 3 | 2 |
| $v_{11}$ | $v_{10} < a$ | 2 | 4 | 2 |

The ASAP schedule ends at step 4, so the least latency is 4, and the chain $v_1 \to v_3 \to v_4 \to v_5$ is critical. At $L = 3$, line L6 gives $t_L(v_1) = 0$, and ALAP reports "infeasible". At $L = 6$, every mobility grows by 2: the five critical operations get mobility 2, $v_6$ and $v_7$ get 3, and the rest get 4. The ASAP schedule puts four multiplies at step 1, while the ALAP schedule at $L = 4$ puts three ALU operations at step 4. Neither is a good use of hardware, which is why resource-constrained schedulers move the operations inside their frames.

**A multicycle case.** A multiply of delay 2 feeds an add, and a second add stands alone. ASAP gives the starts $(1, 3, 1)$ and a latency of 3. At $L = 3$, ALAP gives $(1, 3, 3)$. At $L = 5$, it gives $(3, 5, 5)$. At $L = 2$, it fails.

## Correctness

Every schedule that meets $L$ starts each operation between its ASAP and its ALAP step, by induction along the topological order for the lower bound and along the reverse order for the upper bound. Both $t_S$ and $t_L$ are themselves schedules, so they are the earliest and the latest schedule, one operation at a time. The time frame is exact: for every step $s$ with $t_S(v) \le s \le t_L(v)$, some schedule that meets $L$ starts $v$ at $s$. The ASAP schedule has latency equal to the critical path length, and line L7 fails exactly when $L$ is smaller. The [full proof](proofs/correctness.md) gives the details.

## Complexity

Line L1 is [Kahn's algorithm](/kahns-algorithm/) in $O(V + E)$ time. Lines L2 and L3 look at each edge once, from its head, and lines L5 and L6 look at each edge once, from its tail. So each schedule takes $O(V + E)$ time and $O(V + E)$ space for the adjacency lists. Mobility costs one ASAP and one ALAP pass. A new latency bound needs only a new ALAP pass.

## Properties

- **Exact.** Both schedules are optimal for what they compute, and the result is fully determined by the graph, the delays and $L$.
- **Pointwise extremes.** No schedule starts an operation earlier than ASAP or later than ALAP.
- **No resources.** The schedules can use any number of units in one step. The number of units that they need is only a result.
- **Shift with $L$.** Raising $L$ by $k$ raises every ALAP step by $k$ and leaves ASAP unchanged.

## Variants and improvements

- **Fixed starts.** If some operations must start at given steps, apply the same two passes with $t_S(v)$ raised to the fixed value and $t_L(v)$ lowered to it. This is how [force-directed scheduling](/force-directed-scheduling/) updates the frames after each decision, and the frames stay exact.
- **Chaining.** If several fast operations fit into one step, the passes work on delays in time units and pack them into steps with a cycle time, as in [static timing analysis](/static-timing-analysis/).
- **Timing constraints.** Minimum and maximum distances between operations give a graph with cycles. Then the earliest starts are longest paths in a graph with no positive cycle, computed by [Bellman-Ford](/bellman-ford/) style relaxation.
- **List scheduling.** [List scheduling](/list-scheduling/) adds unit limits and uses the mobility, or the ALAP step, as the priority of the ready operations.

## When to use it

Use ASAP to find the least latency of a data flow graph, and ALAP to find how much each operation can move under a latency bound. Use both as the first step of a resource-constrained scheduler, to bound the search, to order the operations, or to fix the critical ones. Do not use the ASAP or ALAP schedule as the final schedule when the number of units matters.

## Pitfalls

- **Off by one.** With steps numbered from 1 and $v$ using $t(v)$ to $t(v) + \delta(v) - 1$, the ALAP start is $L + 1$ minus the path delay from $v$. Many write-ups use steps from 0, and mixing the two forms gives a frame that is one step off.
- **Cycles.** A data flow graph of a loop body has a back edge from one iteration to the next. Remove it, or treat it as a timing constraint, before the passes, or the topological order does not exist.
- **Infeasible bound.** If $L$ is less than the critical path length, the ALAP formula gives starts below 1. Check for this, as line L7 does, and do not use those values.
- **Mobility is not freedom of all operations at once.** Two operations on one path can each move within their frames, but not always at the same time. Moving one may shrink the frame of the other.

## Implementations

## History

The earliest and latest start times of the jobs of a project are the forward and backward passes of the critical path method of Kelley and Walker (1959), and the slack of a job is the mobility of this page. High-level synthesis of the 1980s used the ASAP schedule for the least latency and the ALAP schedule as a priority. Paulin and Knight (1989) used the interval between the two as the time frame of an operation, the base of force-directed scheduling. De Micheli's book (1994) presents both schedules as scheduling without resource constraints.

## References
