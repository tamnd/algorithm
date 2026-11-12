---
tag: 20A95V
kind: algorithm
slug: earliest-deadline-first
name: Earliest deadline first
aliases:
- EDF
- deadline driven scheduling
area: systems/scheduling
level: core
summary: "At each moment, run the released job with the nearest absolute deadline, and preempt it when a job with a nearer deadline arrives. Optimal on one processor."
solves: [real-time-scheduling]
model: word-ram
complexity:
  vars: {n: the number of tasks, k: the number of jobs released in the simulated window}
  time: {worst: O(k log k)}
  space: {extra: O(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1973
  people: [C. L. Liu, James W. Layland, Michael L. Dertouzos]
  note: Liu and Layland analysed the deadline driven scheduling algorithm for periodic tasks in 1973; Dertouzos proved in 1974 that it is optimal on one preemptive processor for any set of jobs.
prereqs: [periodic-task-model, deadline, preemption, utilization]
see_also: [edf-optimality, least-laxity-first, rate-monotonic-scheduling, earliest-due-date-first, schedulability-analysis, constant-bandwidth-server, hyperperiod, sporadic-task-model]
sources:
  - paper: doi:10.1145/321738.321743
    title: "C. L. Liu and James W. Layland, Scheduling algorithms for multiprogramming in a hard-real-time environment, Journal of the ACM 20(1) (1973), 46-61"
    locator: the deadline driven scheduling algorithm and the theorem that it schedules a periodic task set with implicit deadlines if and only if U is at most 1
  - paper: "Michael L. Dertouzos, Control robotics: the procedural control of physical processes, Proceedings of IFIP Congress 1974, North-Holland, 807-813"
    locator: the optimality of EDF on one preemptive processor for any set of jobs
  - paper: doi:10.1007/BF01995675
    title: "Sanjoy K. Baruah, Louis E. Rosier and Rodney R. Howell, Algorithms and complexity concerning the preemptive scheduling of periodic, real-time tasks on one processor, Real-Time Systems 2(4) (1990), 301-324"
    locator: the processor demand criterion for EDF and the bound on the length of the interval to check
  - paper: "Sudarshan K. Dhall and C. L. Liu, On a real-time scheduling problem, Operations Research 26(1) (1978), 127-140"
    locator: global EDF and rate-monotonic priorities on many processors, and the task sets with utilization near 1 that they cannot schedule
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 3 (Horn's algorithm, that is EDF for jobs with release times) and Chapter 4 (EDF for periodic tasks, and the processor demand approach for D at most T)
  - paper: "W. A. Horn, Some simple scheduling algorithms, Naval Research Logistics Quarterly 21(1) (1974), 177-185"
    locator: preemptive scheduling of jobs with release times and due dates on one machine by the earliest due date among the available jobs
---

Earliest deadline first (EDF) is the scheduling rule that, at each moment, runs the released and unfinished job with the earliest absolute [deadline](/deadline/), and [preempts](/preemption/) it when a job with an earlier deadline is released. On one processor it is optimal: if any schedule meets all deadlines of a set of jobs, EDF meets them too ([optimality of EDF](/edf-optimality/)). For [periodic](/periodic-task-model/) or [sporadic](/sporadic-task-model/) tasks with deadlines equal to periods, it meets all deadlines exactly when the [utilization](/utilization/) is at most 1. For tasks with shorter deadlines, the exact test is the processor demand criterion of Baruah, Rosier and Howell.

## In plain words

You have a list of homework, and each piece has a due date. Whenever you choose what to work on, you take the piece that is due first. If a new piece arrives that is due earlier than the one you are doing, you put the current piece aside and start the new one.

On one processor this simple habit is the best possible: if any plan finishes all work on time, this one does too. The priority belongs to each piece of work, not to the task that made it. The next piece of the same task has a later due date, so it can have a lower priority than a piece of another task.

## The problem

The input is a set of jobs on one processor; job $j$ has a release time $r_j$, an execution time $c_j > 0$ and an absolute deadline $d_j$. For a task system, the jobs are those that the tasks release; for [synchronous](/periodic-task-model/) periodic tasks with $D_i \le T_i$, the jobs of one [hyperperiod](/hyperperiod/) are enough. The output is a preemptive schedule; the question is whether each job ends by its deadline. This is the one-processor case of [real-time scheduling](/real-time-scheduling/).

## The algorithm

The procedure simulates EDF exactly. Time advances from one event (a release or a completion) to the next, so the times stay exact with integers or fractions.

```pseudo id=main
EDF(J)                                     ▷ J: jobs (r, c, d) on one processor
L1  sort J by release time
L2  t ← 0, Q ← an empty min-heap keyed by (d, r)
L3  while J has an unreleased job or Q is not empty do
L4      if Q is empty then t ← max(t, the next release time)
L5      move each job with r ≤ t from J into Q
L6      j ← the top of Q                     ▷ the earliest deadline
L7      δ ← min(remaining(j), next release time − t)
L8      run j in [t, t + δ); t ← t + δ; remaining(j) ← remaining(j) − δ
L9      if remaining(j) = 0 then remove j from Q; finish(j) ← t
```

Line L7 stops the run at the next release, because a new job may have an earlier deadline. If it has not, the next round picks $j$ again, and the two pieces join. Ties in the deadline go to the earlier release, then to the lower job number; any fixed tie rule gives a valid EDF schedule.

As a dispatcher in a kernel, the same rule needs only lines L5, L6 and L9: on each release and each completion, it takes the job at the top of the ready queue.

**The tests.** For tasks with implicit deadlines ($D_i = T_i$), EDF meets all deadlines if and only if

$$U = \sum_{i=1}^n \frac{C_i}{T_i} \le 1.$$

For constrained deadlines ($D_i \le T_i$), define the demand bound function

$$h(t) = \sum_{i=1}^n \max\left(0, \left\lfloor \frac{t - D_i}{T_i} \right\rfloor + 1\right) C_i,$$

the work of the jobs that a synchronous release puts with both release and deadline in $[0, t]$. EDF meets all deadlines if and only if $h(t) \le t$ for each $t > 0$. It is enough to check $U \le 1$ and the absolute deadlines $t = k T_i + D_i$ with $t \le L$, where $L = H$ if $U = 1$, and $L = \min(H, L_a)$ if $U < 1$, with

$$L_a = \frac{\sum_{i=1}^n (T_i - D_i)\, U_i}{1 - U}.$$

## Example

Take $\tau_1 = (C_1, T_1) = (2, 5)$ and $\tau_2 = (4, 7)$ with implicit deadlines and synchronous release, so $U = 34/35$. Under [rate-monotonic](/rate-monotonic-scheduling/) priorities the first job of $\tau_2$ ends at 8 and misses its deadline 7. EDF gives:

| interval | job (release, deadline) | why |
|---|---|---|
| $[0, 2)$ | $\tau_1$ (0, 5) | deadline 5 is before 7 |
| $[2, 6)$ | $\tau_2$ (0, 7) | at time 5, the new job of $\tau_1$ has deadline 10, after 7 |
| $[6, 8)$ | $\tau_1$ (5, 10) | at time 7, the new job of $\tau_2$ has deadline 14 |
| $[8, 12)$ | $\tau_2$ (7, 14) | deadline 14 is before 15 |
| $[12, 14)$ | $\tau_1$ (10, 15) | |
| $[14, 15)$ | $\tau_2$ (14, 21) | |
| $[15, 17)$ | $\tau_1$ (15, 20) | deadline 20 is before 21: preemption |
| $[17, 20)$ | $\tau_2$ (14, 21) | |

Over the hyperperiod $[0, 35)$, EDF runs all 12 jobs, meets all 12 deadlines, and preempts once, at time 15. The processor is idle only in $[34, 35)$, because $U = 34/35$.

**Constrained deadlines.** Take $(C, T, D) = (1, 4, 2)$, $(2, 6, 4)$ and $(3, 12, 9)$. Then $U = 5/6$ and $L_a = (2 \cdot \tfrac14 + 2 \cdot \tfrac26 + 3 \cdot \tfrac{3}{12}) / \tfrac16 = 11.5$. The absolute deadlines up to 11.5 are 2, 4, 6, 9 and 10, with $h = 1, 3, 4, 7, 10$. Each is at most $t$, so EDF meets all deadlines. For $(2, 4, 2)$ and $(2, 6, 3)$, also with $U = 5/6$, $h(3) = 4 > 3$, so the system is not feasible: EDF ends the first job of the second task at 4.

## Correctness

Two facts make EDF correct. First, the loop is an exact simulation: during each run of line L8, the running job has the earliest deadline among the released, unfinished jobs, since no job is released inside the interval. Second, the tests are exact. If EDF misses a deadline $d$, let $t_0$ be the end of the last interval before $d$ in which the processor is idle or runs a job with a deadline after $d$. In $[t_0, d)$ the processor runs only jobs with deadlines at most $d$ that were released at or after $t_0$, and their work is more than $d - t_0$. No sporadic release pattern has more such work than $h(d - t_0)$, so $h(d - t_0) > d - t_0$. The full proofs, and the bound $L_a$, are below; the optimality among all algorithms is on [its own page](/edf-optimality/).

## Complexity

- **Simulation.** With $k$ jobs, there are at most $2k$ rounds of the loop: each round ends a job or reaches a release. Each round costs $O(\log k)$ for the heap, so the time is $O(k \log k)$ and the space $O(k)$. For a synchronous task system with $D_i \le T_i$, one hyperperiod has $k = \sum_i H / T_i$ jobs, which can be exponential in the size of the input.
- **Dispatcher.** With $D_i \le T_i$ and no missed deadline, each task has at most one ready job, so the heap holds at most $n$ jobs, and each release or completion costs $O(\log n)$.
- **Preemptions.** A job is preempted only at a release, so the number of preemptions is less than the number of jobs.
- **Tests.** The utilization test takes $O(n)$ operations. The processor demand test takes $O(n)$ operations at each of $\sum_i L / T_i$ points; it is pseudo-polynomial when $U \le c$ for a constant $c < 1$. In general the question is coNP-hard (Eisenbrand and Rothvoß 2010; see [schedulability analysis](/schedulability-analysis/)).

## Properties

- **Optimal on one processor.** EDF meets all deadlines of each feasible job set on one preemptive processor ([proof](/edf-optimality/)). So for implicit deadlines it reaches a utilization of 1, while fixed priorities in general stop at the [Liu-Layland bound](/liu-layland-utilization-bound/) $n(2^{1/n} - 1)$.
- **Fixed job priority.** The priority of a job does not change while it waits. So the run order of two ready jobs never flips, which keeps the number of preemptions small (compare [least laxity first](/least-laxity-first/)).
- **Online and work-conserving.** EDF needs no knowledge of future releases, and it never idles while a job is ready.
- **Not optimal on many processors.** Global EDF on $m \ge 2$ processors misses deadlines of some task sets that a partition schedules easily (the Dhall effect, below).
- **Bad in overload.** When $U > 1$, EDF gives no protection to any task: a job that runs too long can make the jobs of other tasks miss, in a chain. Fixed priorities protect the high-priority tasks; for EDF, servers such as the [constant bandwidth server](/constant-bandwidth-server/) give the protection.

## Variants and improvements

- **Horn's algorithm.** EDF for a finite set of one-shot jobs with release times. It minimizes the maximum lateness, $1 \mid r_j, \text{pmtn} \mid L_{\max}$ (Horn 1974).
- **Earliest due date first.** With all release times at 0, EDF never preempts and runs the jobs in order of their deadlines. This is [Jackson's rule](/earliest-due-date-first/) for $1 \mid\mid L_{\max}$. Jackson's rule orders one fixed batch of jobs; EDF is a dispatcher for jobs that keep arriving, and the analysis of EDF is about recurring tasks and their hard deadlines.
- **Non-preemptive EDF.** It runs each started job to the end. It is not optimal: with jobs $(r, c, d) = (0, 4, 10)$ and $(1, 1, 2)$ it starts the first job at time 0, and the second one misses. A schedule that idles in $[0, 1)$ meets both deadlines.
- **EDF with servers.** The [constant bandwidth server](/constant-bandwidth-server/) gives each task a budget and a deadline that EDF uses. Linux SCHED_DEADLINE works this way.
- **Global and partitioned EDF.** On $m$ processors, global EDF runs the $m$ jobs with the earliest deadlines. Partitioned EDF fixes each task to one processor and runs EDF there; the partition step is a bin packing problem.

## When to use it

Use EDF when the processor must be fully used and the task parameters are known, for example in a control loop with $U$ near 1, or in a kernel that admits tasks by the test $U \le 1$. Use fixed priorities ([rate-monotonic](/rate-monotonic-scheduling/) or [deadline-monotonic](/deadline-monotonic-scheduling/)) when overloads are possible and the most important tasks must keep their deadlines, or when the kernel supports only fixed priorities.

## Pitfalls

- **Using $U \le 1$ for constrained deadlines.** The test is exact only for $D_i = T_i$. With $D_i < T_i$ use the processor demand test; the example above has $U = 5/6$ and is not feasible.
- **Relative and absolute deadlines.** The heap key is the absolute deadline $r + D$, not the relative deadline $D$. With the relative deadline the rule becomes [deadline-monotonic](/deadline-monotonic-scheduling/), a fixed-priority rule.
- **Checking a too short interval.** For tasks with offsets, a simulation of $[0, H)$ is not enough; see [hyperperiod](/hyperperiod/).
- **Many processors.** Do not reuse the one-processor test on $m$ processors. With $m = 2$ and the tasks $(C, T) = (2, 10)$, $(2, 10)$ and $(10, 11)$, global EDF runs both short jobs first, in $[0, 2)$, and the long job ends at 12, after its deadline 11. Two processors with the long task alone on one of them meet all deadlines. Dhall and Liu used tasks of this shape, with short jobs of length $2\varepsilon$, to show that global EDF and global rate-monotonic priorities can fail with a total utilization close to 1 on $m$ processors.
- **Overload.** If a task can run longer than its $C_i$, guard the other tasks with a budget.

## Implementations

## History

Liu and Layland (1973) introduced the "deadline driven scheduling algorithm" for periodic tasks with implicit deadlines and proved that it schedules a task set if and only if $U \le 1$. Horn (1974) gave the rule for one-shot jobs with release times. Dertouzos (1974) proved that the rule is optimal on one preemptive processor for any set of jobs. Baruah, Rosier and Howell (1990) gave the exact test for constrained and arbitrary deadlines. Dhall and Liu (1978) showed that the rule loses its optimality on many processors.

## References
