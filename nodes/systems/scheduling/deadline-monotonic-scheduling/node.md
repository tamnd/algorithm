---
tag: RQ7EFJ
kind: algorithm
slug: deadline-monotonic-scheduling
name: Deadline-monotonic scheduling
aliases:
- DM
- deadline-monotonic priority assignment
area: systems/scheduling
level: advanced
summary: "Give each task a fixed priority by its relative deadline: the shorter the deadline, the higher the priority. Optimal among fixed priorities when each deadline is at most the period."
solves: [real-time-scheduling]
model: word-ram
complexity:
  vars: {n: the number of tasks, k: the number of jobs released in the simulated window}
  time: {worst: O(n log n + k log k)}
  space: {extra: O(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1982
  people: [Joseph Y.-T. Leung, Jennifer Whitehead]
  note: Leung and Whitehead proposed priorities by relative deadline and proved them optimal among fixed priorities for deadlines at most the periods; Audsley gave in 1991 an assignment that is optimal also for longer deadlines.
prereqs: [rate-monotonic-scheduling, response-time-analysis]
see_also: [rate-monotonic-scheduling, rate-monotonic-optimality, response-time-analysis, earliest-deadline-first, fixed-priority-scheduling, schedulability-analysis, sporadic-task-model]
sources:
  - paper: "Joseph Y.-T. Leung and Jennifer Whitehead, On the complexity of fixed-priority scheduling of periodic, real-time tasks, Performance Evaluation 2(4) (1982), 237-250"
    locator: the deadline-monotonic priority assignment and its optimality among fixed priorities for deadlines at most the periods
  - paper: "Neil C. Audsley, Optimal priority assignment and feasibility of static priority tasks with arbitrary start times, Technical Report YCS 164, Department of Computer Science, University of York, 1991"
    locator: the priority assignment from the lowest level up, and its optimality
  - paper: "John P. Lehoczky, Fixed priority scheduling of periodic task sets with arbitrary deadlines, Proceedings of the 11th IEEE Real-Time Systems Symposium, 1990"
    locator: the busy period analysis for deadlines after the periods
  - paper: "Neil C. Audsley, Alan Burns, Mike F. Richardson, Ken Tindell and Andy J. Wellings, Applying new scheduling theory to static priority pre-emptive scheduling, Software Engineering Journal 8(5) (1993), 284-292"
    locator: response-time analysis for deadline-monotonic priorities, with blocking and jitter
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 4, Periodic Task Scheduling (deadline monotonic scheduling and its tests)
---

Deadline-monotonic scheduling (DM) is the [fixed-priority](/fixed-priority-scheduling/) rule that gives each task a priority by its relative deadline: the task with the shortest deadline gets the highest priority. Leung and Whitehead (1982) proved that, for [periodic](/periodic-task-model/) or [sporadic](/sporadic-task-model/) tasks with deadlines at most their periods on one processor, it is optimal among fixed priorities: if any fixed order meets all deadlines, DM does. With deadlines equal to periods it is [rate-monotonic scheduling](/rate-monotonic-scheduling/). For deadlines after the periods it is not optimal, and Audsley's algorithm finds an optimal fixed order instead.

## In plain words

Several jobs repeat on one processor, and each must end within a set time after it starts to wait. Rank them once, before the system runs: the job with the tightest time limit gets the top rank. Then always run the waiting job with the best rank.

A job that repeats rarely may still need a fast answer, like an alarm that comes once an hour but must be handled in a millisecond. Ranking by how often a job repeats would put the alarm last. Ranking by the time limit puts it first. When each job must end before its next copy arrives, no other fixed ranking does better. When jobs may end after the next copy arrives, a different method searches for a good ranking from the bottom up.

## The problem

The input is a set of $n$ independent tasks $\tau_i = (C_i, T_i, D_i)$ on one preemptive processor: worst-case execution time, period or minimum gap, and relative deadline. The tasks are synchronous periodic or sporadic. The output is a fixed priority order and the schedule that it gives; the question is whether each job ends by its deadline. This is a case of [real-time scheduling](/real-time-scheduling/).

## The algorithm

Sort the tasks by relative deadline, shortest first, with ties in any fixed way. At run time, run the pending job of the first task in this order; jobs of one task run in release order. The procedure below simulates the rule exactly over a window $[0, W)$, with events at releases and completions.

```pseudo id=main
DM(τ, W)                                   ▷ τ: tasks (C, T, D); W: the window
L1  order ← τ sorted by D, shortest first (ties by index)
L2  while a job of [0, W) is unreleased or Q is not empty do
L3      if Q is empty then jump t to the next release; move each job with release ≤ t into Q, keyed by (rank, release)
L4      j ← the top of Q                     ▷ the job of highest priority
L5      δ ← min(remaining(j), next release − t); run j in [t, t + δ); t ← t + δ
L6      if remaining(j) = 0 then remove j from Q; finish(j) ← t
```

**The tests.** For $D_i \le T_i$, [response-time analysis](/response-time-analysis/) in DM order is exact: iterate $R \leftarrow C_i + \sum_{j \in \operatorname{hp}(i)} \lceil R / T_j \rceil C_j$ from $R = C_i$ and check $R \le D_i$. A simpler sufficient test replaces each period by the deadline: if $\sum_i C_i / D_i \le n(2^{1/n} - 1)$, DM meets all deadlines, because the tasks $(C_i, D_i, D_i)$ release more work and pass the [Liu-Layland bound](/liu-layland-utilization-bound/).

**Audsley's algorithm** (optimal priority assignment, OPA) fills the priority levels from the lowest one up. At each level, it looks for an unassigned task that meets its deadline when all other unassigned tasks have higher priority, puts it at this level, and goes one level up. If no task fits at some level, no fixed order works. It uses an exact per-task test, such as the busy period analysis of Lehoczky (1990) for any deadlines, and at most $n(n+1)/2$ calls of the test.

## Example

**DM against RM.** Take $\tau_1 = (2, 10, 2)$ and $\tau_2 = (1, 5, 5)$. Rate-monotonic priorities put $\tau_2$ first, so $\tau_2$ runs in $[0, 1)$ and $\tau_1$ ends at 3, after its deadline 2. DM puts $\tau_1$ first: $\tau_1$ runs in $[0, 2)$ and $\tau_2$ in $[2, 3)$, and both meet their deadlines; response-time analysis gives $R_1 = 2$ and $R_2 = 3$.

**DM is not EDF.** Take $(C, T, D) = (1, 4, 2)$, $(2, 6, 4)$ and $(3, 12, 9)$, with $U = 5/6$. DM keeps this order. Response-time analysis gives $R_1 = 1$ and $R_2 = 3$; for $\tau_3$, the iteration runs $3, 6, 7, 9, 10$, and $10 > 9$. The synchronous release confirms it:

| interval | $[0,1)$ | $[1,3)$ | $[3,4)$ | $[4,5)$ | $[5,6)$ | $[6,8)$ | $[8,9)$ | $[9,10)$ |
|---|---|---|---|---|---|---|---|---|
| job | $\tau_1$ | $\tau_2$ | $\tau_3$ | $\tau_1$ | $\tau_3$ | $\tau_2$ | $\tau_1$ | $\tau_3$ |

So the first job of $\tau_3$ ends at 10 and misses its deadline 9. By the optimality of DM, no fixed order works. [EDF](/earliest-deadline-first/) meets all deadlines of this set: it runs $\tau_3$ in $[5, 7)$, before the job of $\tau_2$ released at 6, whose deadline 10 is after 9.

**Deadlines after the periods.** Take $\tau_1 = (2, 4, 6)$ and $\tau_2 = (4, 8, 7)$, so $U = 1$. DM puts $\tau_1$ first: $\tau_1$ runs in $[0, 2)$ and $[4, 6)$, $\tau_2$ in $[2, 4)$ and $[6, 8)$, and $\tau_2$ ends at 8, after 7. Audsley's algorithm tries the lowest level first: $\tau_1$ below $\tau_2$ has response times 6 and 4 in its busy period, at most 6, so it fits; $\tau_2$ above it has response time 4. The order $\tau_2, \tau_1$ meets all deadlines.

## Correctness

The loop runs, in each interval, the pending job of highest priority, since no job is released inside an interval. The optimality of DM for $D_i \le T_i$ is Theorem 2 on the page on [rate-monotonic optimality](/rate-monotonic-optimality/): in a feasible order, a pair of neighbors in the wrong order by deadline can be swapped without a miss, because the task that moves down can use the response time of the task that moves up as its own witness. Audsley's algorithm is correct because the test of a task depends only on the set of tasks above it, and removing a task from that set never hurts. Both arguments, and the busy period analysis, are proved below.

## Complexity

- **Priorities.** Sorting the deadlines takes $O(n \log n)$ time.
- **Dispatcher and simulation.** As for [rate-monotonic scheduling](/rate-monotonic-scheduling/): $O(\log n)$ per event at run time, and $O(k \log k)$ for a simulation with $k$ jobs.
- **Tests.** Response-time analysis is pseudo-polynomial. Audsley's algorithm calls a per-task test at most $n + (n - 1) + \cdots + 1 = n(n+1)/2$ times.

## Properties

- **Optimal among fixed priorities** for constrained deadlines ($D_i \le T_i$), synchronous or sporadic, on one processor.
- **Equal to rate-monotonic** when $D_i = T_i$, or more generally when $D_i / T_i$ is the same for all tasks.
- **Not optimal for $D_i > T_i$**, as the third example shows. Audsley's algorithm is optimal there.
- **Not optimal among all algorithms.** EDF is; the second example is feasible but has no feasible fixed order.
- **Same strengths as RM.** Fixed priorities are cheap to dispatch, and an overrun hurts only tasks of lower priority.

## Variants and improvements

- **Audsley's optimal priority assignment.** As above. It works for any per-task test whose result depends only on the set of tasks of higher priority and does not get worse when that set shrinks; this includes response-time analysis with release jitter, where DM is not always optimal.
- **Shared resources.** Use the [priority ceiling protocol](/priority-ceiling-protocol/) to bound blocking, and add the blocking terms to response-time analysis.
- **With offsets.** For tasks with fixed offsets, the synchronous release may never happen, so the synchronous tests are only sufficient. Audsley's 1991 report treats tasks with arbitrary start times.

## When to use it

Use DM whenever a fixed-priority kernel runs tasks whose deadlines are shorter than their periods, for example a slow sensor that needs a fast answer. With deadlines equal to periods it is the same as rate-monotonic. With deadlines after the periods, with release jitter, or with other effects that break DM's optimality, use Audsley's algorithm with response-time analysis.

## Pitfalls

- **Using the period.** Rate-monotonic priorities with constrained deadlines can fail on sets that DM schedules, as the first example shows.
- **Absolute and relative deadlines.** DM orders by the relative deadline $D_i$, once. Ordering each job by its absolute deadline is [EDF](/earliest-deadline-first/), a dynamic-priority rule.
- **Trusting DM for long deadlines.** For $D_i > T_i$, check the result or use Audsley's algorithm.
- **Using the utilization bound with periods.** The test $\sum_i C_i / T_i \le n(2^{1/n} - 1)$ is not valid for DM with $D_i < T_i$: two tasks $(1, 10, 1)$ have $U = 0.2$ and miss a deadline under each order. Use $C_i / D_i$ instead.

## Implementations

## History

Leung and Whitehead (1982) proposed the deadline-monotonic assignment and proved it optimal among fixed priorities for deadlines at most the periods; they also studied the complexity of fixed-priority scheduling with offsets. Lehoczky (1990) gave the busy period analysis for longer deadlines, where the assignment is not optimal. Audsley (1991) gave the priority assignment from the lowest level up, which is optimal in that case and for many other test models, and Audsley, Burns, Richardson, Tindell and Wellings (1993) combined deadline-monotonic priorities with response-time analysis.

## References
