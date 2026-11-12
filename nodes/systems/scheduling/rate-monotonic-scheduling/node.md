---
tag: JM2GFC
kind: algorithm
slug: rate-monotonic-scheduling
name: Rate-monotonic scheduling
aliases:
- RMS
- RM
- rate-monotonic priority assignment
area: systems/scheduling
level: advanced
summary: "Give each periodic task a fixed priority by its rate: the shorter the period, the higher the priority. Then always run the ready job with the highest priority."
solves: [real-time-scheduling]
model: word-ram
complexity:
  vars: {n: the number of tasks, k: the number of jobs released in the simulated window}
  time: {worst: O(n log n + k log k)}
  space: {extra: O(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1973
  people: [C. L. Liu, James W. Layland]
  note: Liu and Layland defined the rate-monotonic priority assignment, proved that it is optimal among fixed priorities for implicit deadlines, and gave the utilization bound n(2^(1/n) - 1).
prereqs: [periodic-task-model, priority-scheduling, preemption]
see_also: [rate-monotonic-optimality, liu-layland-utilization-bound, response-time-analysis, deadline-monotonic-scheduling, earliest-deadline-first, fixed-priority-scheduling, priority-ceiling-protocol, hyperperiod]
sources:
  - paper: doi:10.1145/321738.321743
    title: "C. L. Liu and James W. Layland, Scheduling algorithms for multiprogramming in a hard-real-time environment, Journal of the ACM 20(1) (1973), 46-61"
    locator: the rate-monotonic priority assignment, the critical instant, the optimality among fixed priorities and the utilization bound
  - paper: "John P. Lehoczky, Lui Sha and Ye Ding, The rate monotonic scheduling algorithm: exact characterization and average case behavior, Proceedings of the 10th IEEE Real-Time Systems Symposium, 1989, 166-171"
    locator: the exact test by the time demand at the scheduling points, and the average breakdown utilization of random task sets
  - paper: "Mathai Joseph and Paritosh Pandya, Finding response times in a real-time system, The Computer Journal 29(5) (1986), 390-395"
    locator: the response time of a task under fixed priorities as the least solution of a recurrence
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 4, Periodic Task Scheduling (rate monotonic scheduling, its bounds and its exact tests)
  - book: isbn:9780130996510
    title: Jane W. S. Liu, Real-Time Systems, Prentice Hall, 2000
    locator: Chapter 6, Priority-Driven Scheduling of Periodic Tasks
---

Rate-monotonic scheduling (RM) is the [fixed-priority](/fixed-priority-scheduling/) rule for [periodic tasks](/periodic-task-model/) that gives each task a priority by its rate: the task with the shortest period gets the highest priority. At run time the processor always runs the released job of the highest-priority task, and [preempts](/preemption/) it when a job of a higher-priority task is released. Liu and Layland (1973) proved that, for tasks with deadlines equal to their periods on one processor, no other fixed priority order schedules a task set that RM cannot schedule, and that RM meets all deadlines when the [utilization](/utilization/) is at most $n(2^{1/n} - 1)$.

## In plain words

Several jobs repeat at a steady pace on one computer: one every few milliseconds, another once a second. Rate-monotonic scheduling ranks them once, before the system starts. The job that repeats most often gets the top rank. Whenever the computer chooses what to run, it takes the waiting job with the best rank, and it interrupts a lower one if needed.

The ranks never change, so the rule is easy to build into a simple kernel with fixed priority levels. Among all such fixed rankings, this one is the best when each job must end before its next copy arrives. It cannot always use the whole processor: some loads that fit in time miss a deadline under this rule but not under a rule that ranks by deadlines.

## The problem

The input is a set of $n$ periodic tasks $\tau_i = (C_i, T_i)$ on one preemptive processor, with implicit deadlines $D_i = T_i$, independent jobs and no overheads: the model of Liu and Layland. The tasks are synchronous unless offsets are given. The output is a schedule; the question is whether each job ends by its deadline. This is a case of [real-time scheduling](/real-time-scheduling/).

## The algorithm

The rule has two parts. Before run time, sort the tasks by period, shortest first; ties may go either way. At run time, the scheduler is a [priority scheduler](/priority-scheduling/): on each release and each completion, it runs the pending job whose task comes first in this order.

The procedure below simulates this rule exactly over a window $[0, W)$, for example one [hyperperiod](/hyperperiod/). Time jumps from one event to the next, so integer or fractional times stay exact.

```pseudo id=main
RM(τ, W)                                   ▷ τ: tasks (C, T); W: the window
L1  rank ← the order of τ by period, shortest first (ties by index)
L2  J ← the jobs released in [0, W), sorted by release time
L3  t ← 0, Q ← an empty min-heap keyed by (rank, release)
L4  while J has an unreleased job or Q is not empty do
L5      if Q is empty then t ← max(t, the next release time)
L6      move each job with release ≤ t from J into Q
L7      j ← the top of Q                     ▷ the job of highest priority
L8      δ ← min(remaining(j), next release time − t)
L9      run j in [t, t + δ); t ← t + δ; remaining(j) ← remaining(j) − δ
L10     if remaining(j) = 0 then remove j from Q; finish(j) ← t
```

A job may run after its deadline; the simulation records its finish time, and a finish time after the deadline is a miss.

**The tests.** Three tests decide or bound the result for synchronous tasks with $D_i = T_i$:

- *Simulation.* Run the procedure with $W = H$ and check each deadline. This is exact, but $H$ can be large.
- *[Response-time analysis](/response-time-analysis/).* For each task, with the tasks indexed in RM order, iterate $R \leftarrow C_i + \sum_{j < i} \lceil R / T_j \rceil C_j$ from $R = C_i$, and check $R \le T_i$. This is exact and does not depend on $H$.
- *Utilization bounds.* RM meets all deadlines if $U \le n(2^{1/n} - 1)$ ([Liu-Layland bound](/liu-layland-utilization-bound/)), or if $\prod_i (U_i + 1) \le 2$ (the hyperbolic bound). These tests take $O(n)$ time and are only sufficient.

## Example

Take $\tau_1 = (1, 4)$, $\tau_2 = (2, 6)$ and $\tau_3 = (3, 12)$, so $H = 12$ and $U = 1/4 + 1/3 + 1/4 = 5/6 \approx 0.833$. The RM order is $\tau_1, \tau_2, \tau_3$.

| interval | job | why |
|---|---|---|
| $[0, 1)$ | $\tau_1$ | all tasks release at 0; $\tau_1$ has the shortest period |
| $[1, 3)$ | $\tau_2$ | |
| $[3, 4)$ | $\tau_3$ | |
| $[4, 5)$ | $\tau_1$ | released at 4; it preempts $\tau_3$ |
| $[5, 6)$ | $\tau_3$ | |
| $[6, 8)$ | $\tau_2$ | released at 6; it preempts $\tau_3$ |
| $[8, 9)$ | $\tau_1$ | released at 8 |
| $[9, 10)$ | $\tau_3$ | its last unit; it ends at 10, before the deadline 12 |
| $[10, 12)$ | idle | |

All deadlines are met, and the response times $1, 3, 10$ agree with response-time analysis. Both utilization bounds reject this set: $U = 0.833$ is above $3(2^{1/3} - 1) \approx 0.780$, and $\prod_i (U_i + 1) = \tfrac54 \cdot \tfrac43 \cdot \tfrac54 = \tfrac{25}{12} > 2$. The bounds are sufficient, not necessary.

**A miss.** For $\tau_1 = (2, 5)$ and $\tau_2 = (4, 7)$, with $U = 34/35$, RM runs $\tau_1$ in $[0, 2)$, $\tau_2$ in $[2, 5)$, $\tau_1$ again in $[5, 7)$, and $\tau_2$ ends at 8, after its deadline 7. The other fixed order is worse: $\tau_1$ then ends at 6, after its deadline 5. So no fixed-priority order schedules this set, but [EDF](/earliest-deadline-first/) does.

## Correctness

The loop runs, in each interval $[t, t + \delta)$, the pending job of highest priority, because no job is released inside the interval and the heap holds exactly the pending jobs. For synchronous tasks with $D_i \le T_i$, a schedule that meets each deadline in $(0, H]$ has no pending work at $H$, so it repeats every $H$; hence the simulation over one hyperperiod is an exact test. The exact simulation test and the exact form of the Liu-Layland test are proved below; the bounds themselves are proved on [their page](/liu-layland-utilization-bound/), and the optimality of the RM order on [its own page](/rate-monotonic-optimality/).

## Complexity

- **Priorities.** Sorting the periods takes $O(n \log n)$ time, once.
- **Dispatcher.** With a heap of ready tasks, each release or completion costs $O(\log n)$. With a bitmap of the priority levels, as in many kernels, it costs $O(1)$ for a fixed number of levels.
- **Simulation.** With $k$ jobs in the window, the loop has at most $2k$ rounds, each $O(\log k)$, so $O(k \log k)$ time and $O(k)$ space. Over one hyperperiod, $k = \sum_i H / T_i$, which can be exponential in $n$.
- **Tests.** The utilization bounds take $O(n)$. Response-time analysis takes pseudo-polynomial time. Computing the worst-case response time of a task under fixed priorities is NP-hard (Eisenbrand and Rothvoß 2008; see [schedulability analysis](/schedulability-analysis/)).

## Properties

- **Optimal among fixed priorities** for implicit deadlines on one processor: if any fixed order schedules the set, RM does ([proof](/rate-monotonic-optimality/)). The same holds for $D_i \le T_i$ when all $D_i / T_i$ are equal.
- **Critical instant.** The worst response time of a task occurs when it releases a job together with all higher-priority tasks. So the synchronous case is the worst case, also for [sporadic](/sporadic-task-model/) tasks.
- **Utilization bound.** RM meets all deadlines if $U \le n(2^{1/n} - 1)$. The bound falls from $1$ at $n = 1$ and $0.828$ at $n = 2$ to $\ln 2 \approx 0.693$ as $n \to \infty$, and for each $n$ there is a task set just above it that fails.
- **Harmonic periods.** If each period divides each longer period, RM meets all deadlines if and only if $U \le 1$.
- **Average case.** Lehoczky, Sha and Ding (1989) found that random task sets with many tasks stay schedulable under RM up to a utilization of about 0.88 on average, well above $\ln 2$.
- **Predictable overload.** If a job overruns, only tasks of lower priority can miss deadlines.
- **Not optimal in general.** EDF meets all deadlines for each set with $U \le 1$; RM does not, as the second example shows.

## Variants and improvements

- **Deadline-monotonic.** For $D_i \le T_i$, order by relative deadline instead of period. This is optimal among fixed priorities for constrained deadlines ([deadline-monotonic scheduling](/deadline-monotonic-scheduling/)).
- **Audsley's assignment.** For arbitrary deadlines, or with release jitter, neither RM nor DM is optimal; Audsley's algorithm finds a feasible fixed order if one exists (see [deadline-monotonic scheduling](/deadline-monotonic-scheduling/)).
- **Shared resources.** With locks, a job can wait for a lower-priority job ([priority inversion](/priority-inversion/)). The [priority inheritance](/priority-inheritance-protocol/) and [priority ceiling](/priority-ceiling-protocol/) protocols bound the wait, and the bound enters response-time analysis as a blocking term.
- **Aperiodic jobs.** Servers such as the [sporadic server](/sporadic-server/) and the [deferrable server](/deferrable-server/) run aperiodic work at a fixed priority inside the RM order.
- **Many processors.** Partitioned RM assigns each task to one processor and runs RM there. Global RM suffers from the same effect as global EDF: a set with total utilization close to 1 can fail on $m$ processors (Dhall and Liu 1978).

## When to use it

Use RM for periodic tasks with deadlines equal to their periods, on a kernel with fixed priority levels, when predictable behavior in overload matters more than the last part of the processor. If the utilization is at most the Liu-Layland bound, no further analysis is needed; otherwise use response-time analysis. If the deadlines are shorter than the periods, use deadline-monotonic priorities. If the processor must be used up to 100% and the kernel supports dynamic priorities, use [EDF](/earliest-deadline-first/).

## Pitfalls

- **Reading the bound as necessary.** A set above $n(2^{1/n} - 1)$ can still be schedulable, as the first example shows. Run an exact test before rejecting it.
- **Deadlines shorter than periods.** RM is not optimal then. For $(C, T, D) = (2, 10, 2)$ and $(1, 5, 5)$, RM gives the second task the higher priority, and the first task ends at 3, after its deadline 2. Deadline-monotonic priorities meet both deadlines.
- **Simulating from a wrong start.** With offsets, a simulation of $[0, H)$ is not enough; start from the synchronous release, which is the worst case, or simulate the longer window of the [hyperperiod](/hyperperiod/) page.
- **Ignoring overheads and blocking.** Context switches, interrupts and locks add work that the basic model does not have. Add them to $C_i$, or as blocking terms in response-time analysis.
- **Too few priority levels.** If the kernel has fewer levels than tasks, tasks must share a level; within a level, the order is first come, first served, and the analysis must count a job of the same level as interference.

## Implementations

## History

Liu and Layland (1973) defined the rate-monotonic priority assignment, proved its optimality among fixed priorities with the critical instant argument, and proved the utilization bound $n(2^{1/n} - 1)$. Joseph and Pandya (1986) gave the exact response time of each task as the least solution of a recurrence, and Lehoczky, Sha and Ding (1989) gave an exact test at a finite set of points, with a study of the average case. Devillers and Goossens (2000) closed a gap in the original proof of the bound, and Bini, Buttazzo and Buttazzo (2003) gave the sharper hyperbolic bound.

## References
