---
tag: NND7DR
kind: problem
slug: resource-constrained-project-scheduling
name: Resource-constrained project scheduling
aliases:
- Project scheduling
- RCPSP
- resource-constrained project scheduling
area: systems/scheduling
level: advanced
summary: Schedule activities with durations, precedence arcs and demands on shared resources of fixed capacity, to minimize the makespan. Strongly NP-hard; solved in practice by the serial SGS and search.
prereqs: [critical-path-method, job-shop-scheduling, strong-np-hardness]
see_also: [list-scheduling, heft, partition-problem, chromatic-number, global-constraint, depth-first-branch-and-bound, genetic-algorithm, simple-temporal-problem]
sources:
  - paper: doi:10.1016/0166-218X(83)90012-4
    title: J. Blazewicz, J. K. Lenstra and A. H. G. Rinnooy Kan, Scheduling subject to resource constraints, classification and complexity, Discrete Applied Mathematics 5(1), 1983
    locator: pages 11 to 24 (the resource-constrained model and its strong NP-hardness)
  - paper: "doi:10.1016/0377-2217(95)00357-6"
    title: Rainer Kolisch, Serial and parallel resource-constrained project scheduling methods revisited, theory and computation, European Journal of Operational Research 90(2), 1996
    locator: pages 320 to 333 (the serial and parallel schedule generation schemes, the schedules each one can produce, and priority rules such as LFT)
  - paper: "doi:10.1016/0377-2217(93)E0294-8"
    title: Arno Sprecher, Rainer Kolisch and Andreas Drexl, Semi-active, active, and non-delay schedules for the resource-constrained project scheduling problem, European Journal of Operational Research 80(1), 1995
    locator: pages 94 to 102 (the classes of schedules, and an optimal schedule among the active ones)
  - paper: "doi:10.1016/S0377-2217(96)00170-1"
    title: Rainer Kolisch and Arno Sprecher, PSPLIB, a project scheduling problem library, European Journal of Operational Research 96(1), 1997
    locator: pages 205 to 216 (the standard benchmark instances)
---

The resource-constrained project scheduling problem (RCPSP) asks for start times for a set of activities that have fixed durations, precedence constraints and demands on a few shared resources, such as workers, machines or memory, each with a fixed capacity per unit of time. The goal is the least makespan. Without the resources it is the problem that the [critical path method](/critical-path-method/) solves in linear time; with them it is strongly NP-hard (Blazewicz, Lenstra and Rinnooy Kan 1983), and it contains the [job shop](/job-shop-scheduling/) and multiprocessor scheduling with precedences as special cases. The standard fast method is the serial schedule generation scheme with a priority rule (Kolisch 1996): order the activities by a rule such as the latest finish time from the critical path method, and start each one as early as precedences and free capacity allow. This page gives that method with an instance where it is not optimal.

## In plain words

A project has tasks. Some tasks must wait for others. Each task takes a known time and needs some amount of shared things while it runs, such as people, machines or memory. Of each shared thing there is only a fixed amount at any moment. Find start times so that each task starts after the tasks it waits for, the amount in use never goes over the limit, and the whole project ends as early as possible. Without the limits, the earliest start of every task is easy to find. With the limits, two tasks that could run at the same time may have to take turns, and choosing who goes first is a hard search. A common method puts the tasks in a list by urgency, then places each task in turn at the first time that has room for it.

## Definition

**Input.**

- Activities $1, \ldots, n$ with integer durations $p_j \ge 0$.
- Precedence arcs $(i, j)$, meaning that $j$ starts only after $i$ finishes. The arcs form a directed acyclic graph.
- Renewable resources $k = 1, \ldots, K$ with capacities $R_k$. Activity $j$ uses $r_{jk}$ units of resource $k$, with $0 \le r_{jk} \le R_k$, during each moment of its run, and releases them when it ends.

**Schedule.** Start times $S_j \ge 0$, with no preemption, such that $S_j \ge S_i + p_i$ for each arc $(i, j)$ and, for every time $t$ and every resource $k$,

$$\sum_{j \,:\, S_j \le t < S_j + p_j} r_{jk} \le R_k .$$

**Goal.** Minimize the makespan $\max_j (S_j + p_j)$.

**Decision form.** Given $T$, is there a schedule of makespan at most $T$? It is in NP: an activity list is a certificate, since the serial scheme under Known algorithms turns it into a schedule in polynomial time, and some list gives an optimal schedule.

**Active schedules.** A feasible schedule is *active* if no activity can start earlier without delaying another activity or breaking a constraint. Some optimal schedule is active (Sprecher, Kolisch and Drexl 1995), and with integer durations every active schedule has integer start times.

## Variants

- **Multi-mode.** Each activity can run in one of several modes, each with its own duration and resource demand, and nonrenewable resources such as a budget limit the total use over the project.
- **Generalized precedence.** Minimum and maximum time lags between starts. Without resources these are a [simple temporal problem](/simple-temporal-problem/); with resources even finding a feasible schedule is NP-hard.
- **Preemption.** Activities may be split. This helps, but the problem stays NP-hard.
- **Other objectives.** Weighted tardiness against due dates, net present value of cash flows, or resource levelling, where the makespan is fixed and the use of the resources should be as even as possible.
- **Uncertain durations.** The schedule becomes a policy that decides starts as activities finish; see [PERT](/pert-chart/) for the case without resources.
- **Special cases.** One resource of capacity $m$ with $r_j = 1$ for all $j$ is $P \mid prec \mid C_{\max}$, the setting of [list scheduling](/list-scheduling/). Resources of capacity $1$ for machines and chains of precedences for jobs give the [job shop](/job-shop-scheduling/).

## Examples

**The priority rule is not optimal.** Four activities share one resource of $4$ units.

| activity | A | B | C | D |
|---|---|---|---|---|
| $p_j$ | 4 | 3 | 4 | 1 |
| $r_j$ | 3 | 1 | 2 | 0 |
| waits for | | | B | C |

Without the resource, the critical path is B, C, D with length $8$, and the backward pass of the critical path method gives the latest finish times $LF = (8, 3, 7, 8)$ for A, B, C and D. A and C cannot overlap, since $3 + 2 > 4$. The serial scheme with the LFT rule takes the list B, C, A, D:

| step | activity | earliest by precedence | candidate times tried | start | runs |
|---|---|---|---|---|---|
| 1 | B | 0 | 0 | 0 | 0 to 3 |
| 2 | C | 3 | 3 | 3 | 3 to 7 |
| 3 | A | 0 | 0 (C starts at 3 inside A's run), 3, 7 | 7 | 7 to 11 |
| 4 | D | 7 | 7 | 7 | 7 to 8 |

The makespan is $11$. The list A, B, C, D gives A and B at $0$ (using $3 + 1 = 4$ units), C at $4$ and D at $8$, with makespan $9$. That is optimal: C must start at $3$ or later, so if C runs before A, A ends at $11$ or later; if A runs before C, C starts at $4$ or later and D ends at $9$ or later. The LFT rule follows the critical path without resources and puts C first, but C blocks A, which has its own four units of work.

**Bounds on the example.** The critical path gives $8$ and the resource gives $\lceil (4 \cdot 3 + 3 \cdot 1 + 4 \cdot 2) / 4 \rceil = 6$, so the lower bound is $8$; the optimum $9$ is higher, because A and C must take turns.

## Known algorithms

**The serial schedule generation scheme with the LFT rule** (Kolisch 1996).

```pseudo id=main
SERIAL-SGS-LFT(p[1 .. n], arcs, r[1 .. n][1 .. K], R[1 .. K])
L1  LF ← the latest finish times of the critical path method, resources ignored
L2  λ ← the activities in order: each step takes, among the activities whose predecessors are all taken, one with the smallest LF
L3  for each j in λ in order do
L4      t ← max over arcs (i, j) of S[i] + p[i]   (0 if none)
L5      for each c in {t} ∪ {S[i] + p[i] : i scheduled, S[i] + p[i] > t}, in increasing order do
L6          if for each resource k, r[j][k] units are free at every time in [c, c + p[j]) then
L7              S[j] ← c; leave the loop of line L5
L8  return S
```

Line L2 makes a precedence-feasible list, so line L4 only reads start times that are set. Line L5 tries only $t$ and the finish times after it: free capacity grows only when an activity ends, so the first time that has room for $j$ is one of these. The last candidate always works, since after it nothing is scheduled. So the schedule is feasible, and each activity starts as early as the activities before it in the list allow. Each schedule from the serial scheme is active, and every active schedule comes from some list (Kolisch 1996), so the best list gives an optimal schedule. A search over lists is therefore complete, and the priority rule picks one list. With $n$ activities, line L5 tries at most $n$ candidates, and line L6 checks the resource profile; with a profile of the scheduled activities kept as a sorted list of change points, the scheme takes $O(n^2 K)$ time.

**Other methods.**

- **Parallel scheme.** Go forward in time, and at each decision time start eligible activities in priority order while they fit. It makes non-delay schedules, which keep no resource idle when an eligible activity fits. Some instances have no optimal non-delay schedule, so the parallel scheme can miss the optimum for every priority order (Kolisch 1996).
- **Other priority rules.** Latest start time, minimum slack, most total successors, or the greatest rank of positional weight. All are cheap and none is best on every instance.
- **Exact methods.** [Depth-first branch and bound](/depth-first-branch-and-bound/) that adds an activity to a partial schedule or resolves a conflict between activities, integer programs with a binary variable for each activity and start time, and constraint programming with the cumulative [global constraint](/global-constraint/). The PSPLIB library (Kolisch and Sprecher 1997) is the usual set of test instances for them. Exact methods are practical only for small projects.
- **Search over lists.** [Genetic algorithms](/genetic-algorithm/), [simulated annealing](/simulated-annealing/) and [tabu search](/tabu-search/) change the activity list and use the serial scheme to decode it into a schedule.

## Bounds

- **Hardness.** Strongly NP-hard (Blazewicz, Lenstra and Rinnooy Kan 1983). It contains the job shop, which is strongly NP-hard.
- **No good approximation from a single resource.** With unit durations, no arcs and one resource, a schedule of makespan $2$ is a split of the demands into two sets that each fit the capacity, which is the [partition problem](/partition-problem/) when the demands sum to $2R$. So no polynomial algorithm guarantees a makespan below $3/2$ times the optimum unless P = NP.
- **With many resources.** The coloring reduction under Reductions makes the RCPSP at least as hard to approximate as the [chromatic number](/chromatic-number/).
- **Lower bounds.** The critical path length without resources, and $\max_k \lceil \sum_j r_{jk} p_j / R_k \rceil$ for the resources. Both can be far below the optimum, as in the example.
- **Upper bound.** Any feasible list gives at most $\sum_j p_j$, the length of running the activities one at a time.

## Reductions

- **From the partition problem.** As under Bounds: unit durations, one resource of capacity half the total demand, and the target makespan $2$.
- **From graph coloring.** For a graph, make one activity of unit duration for each vertex and one resource of capacity $1$ for each edge, used by its two end vertices. Two activities can overlap exactly when their vertices are not adjacent. Some optimal schedule is active and so has integer start times, so the vertices that start at the same time form color classes, and the least makespan is the chromatic number.
- **From the job shop.** A machine is a resource of capacity $1$, an operation is an activity that uses one unit of its machine, and the route of a job is a chain of arcs.
- **To the critical path method.** If every capacity is at least the sum of all demands for it, the resources never bind, and the earliest start times of the critical path method are optimal.

## Applications

- **Construction and engineering projects.** The original setting: crews and equipment are the resources, and the plan is the precedence network.
- **Build and test pipelines.** A build graph on a fixed pool of build agents is the case with one resource and unit demands. Memory or licences add more resources.
- **Batch jobs on a cluster.** Workflow tasks with CPU and memory demands on a fixed set of nodes, where the scheduler starts each ready task when its demands fit.
- **Software and research projects.** Tasks need people with specific skills, each skill a resource with the number of people as capacity.

## References
