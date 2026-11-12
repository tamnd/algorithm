---
tag: NS9S56
kind: definition
slug: periodic-task-model
name: Periodic task model
aliases:
- Liu-Layland task model
- periodic real-time task
area: systems/scheduling
level: core
summary: "Each task releases a job every T time units, from an offset O. Each job needs at most C units of processor time and must end D units after its release."
prereqs: [real-time-scheduling, release-time, deadline]
see_also: [sporadic-task-model, hyperperiod, utilization, rate-monotonic-scheduling, earliest-deadline-first, schedulability-analysis, cyclic-executive]
sources:
  - paper: doi:10.1145/321738.321743
    title: "C. L. Liu and James W. Layland, Scheduling algorithms for multiprogramming in a hard-real-time environment, Journal of the ACM 20(1) (1973), 46-61"
    locator: the environment and its five assumptions (periodic requests, deadlines at the next request, independent tasks, constant run time, no critical non-periodic tasks)
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 4, Periodic Task Scheduling (the introduction gives the notation and the assumptions)
  - book: isbn:9780130996510
    title: Jane W. S. Liu, Real-Time Systems, Prentice Hall, 2000
    locator: Chapter 3, A Reference Model of Real-Time Systems (periodic tasks, phases, utilization and the hyperperiod)
  - paper: "Joseph Y.-T. Leung and M. L. Merrill, A note on preemptive scheduling of periodic, real-time tasks, Information Processing Letters 11(3) (1980), 115-118"
    locator: periodic tasks with arbitrary start times (offsets), and the feasibility interval for them
---

The periodic task model describes a real-time workload as a set of tasks, each of which releases a job at a fixed rate: task $\tau_i$ releases a job every $T_i$ time units, each job needs at most $C_i$ units of processor time, and each job must end $D_i$ time units after its release. Liu and Layland used it in 1973 to state the first results on [rate-monotonic](/rate-monotonic-scheduling/) and [earliest deadline first](/earliest-deadline-first/) scheduling, and most of [real-time scheduling](/real-time-scheduling/) theory still starts from it. The [sporadic task model](/sporadic-task-model/) relaxes the fixed rate to a minimum gap.

## Definition

A **periodic task** is a tuple $\tau_i = (O_i, C_i, T_i, D_i)$ of numbers with $O_i \ge 0$, $C_i > 0$, $T_i > 0$ and $D_i > 0$:

- $O_i$ is the *offset* (or *phase*): the release time of the first job;
- $C_i$ is the *worst-case execution time*: an upper bound on the processor time that one job needs;
- $T_i$ is the *period*: the exact time between two releases;
- $D_i$ is the *relative deadline*.

The task releases the jobs $J_{i,1}, J_{i,2}, \ldots$. Job $J_{i,k}$ has

$$r_{i,k} = O_i + (k-1)\,T_i, \qquad d_{i,k} = r_{i,k} + D_i,$$

and an execution time $c_{i,k}$ with $0 < c_{i,k} \le C_i$. A job may not start before $r_{i,k}$, and it meets its deadline if it ends by $d_{i,k}$. Its *response time* is its finish time minus $r_{i,k}$. At time $t \ge r_{i,k}$, a released job with remaining work $e$ has *laxity* $d_{i,k} - t - e$.

A **periodic task system** is a finite set $\tau = \{\tau_1, \ldots, \tau_n\}$ of periodic tasks. Unless the model says otherwise, the tasks are independent: no task waits for another one, shares a lock with it, or suspends itself. The system is

- *synchronous* if $O_1 = \cdots = O_n$ (by a shift of time, all are 0), and *asynchronous* otherwise;
- with *implicit deadlines* if $D_i = T_i$ for each $i$, *constrained deadlines* if $D_i \le T_i$, and *arbitrary deadlines* otherwise.

The *utilization* of task $\tau_i$ is $U_i = C_i / T_i$, and the utilization of the system is $U = \sum_{i=1}^n U_i$ (see [utilization](/utilization/)). The *density* of $\tau_i$ is $C_i / \min(D_i, T_i)$. The [hyperperiod](/hyperperiod/) is $H = \operatorname{lcm}(T_1, \ldots, T_n)$ for integer periods; the release pattern of the system repeats every $H$ time units after the last first release.

Liu and Layland's model is the special case with implicit deadlines and $c_{i,k} = C_i$, and it adds the rule that a job can be preempted at any time, with no cost.

## Examples and non-examples

**A synchronous system.** Take $\tau_1 = (0, 2, 5, 5)$ and $\tau_2 = (0, 4, 7, 7)$: two tasks with implicit deadlines and $U = 2/5 + 4/7 = 34/35$. Task $\tau_1$ releases jobs at $0, 5, 10, \ldots$ with deadlines $5, 10, 15, \ldots$, and $\tau_2$ releases jobs at $0, 7, 14, \ldots$ with deadlines $7, 14, 21, \ldots$. The hyperperiod is $35$, and it holds $7 + 5 = 12$ jobs.

**An asynchronous system with constrained deadlines.** The task $(O, C, T, D) = (2, 1, 2, 2)$ releases at $2, 4, 6, \ldots$; the task $(0, 3, 6, 4)$ releases at $0, 6, 12, \ldots$ with deadlines $4, 10, 16, \ldots$. Here $U = 1/2 + 1/2 = 1$. In the window $[6, 10]$, the jobs released at 6 and 8 by the first task and at 6 by the second task need $1 + 1 + 3 = 5$ units of work in 4 units of time, so no schedule meets all deadlines. This happens although $U \le 1$, and although EDF meets each deadline up to time 8.

**Non-examples.**

- A keyboard interrupt that can come at any time has no period and no minimum gap. It is an *aperiodic* job; a server task such as a [sporadic server](/sporadic-server/) handles it.
- A task whose jobs come at least 10 ms apart, but at times that are not known in advance, is not periodic. It is a [sporadic task](/sporadic-task-model/) with $T = 10$.
- Two tasks where the second one must wait for the output of the first one in each period are not independent. The model then needs precedence constraints, which the basic model does not have.
- A job that suspends itself for I/O breaks the model: the analysis of the basic model does not bound its effect.

## Related definitions

- [Sporadic task model](/sporadic-task-model/): $T_i$ is a minimum gap, not an exact period. Each periodic system is a sporadic system with one fixed arrival pattern.
- [Hyperperiod](/hyperperiod/): the length after which the release pattern of a periodic system repeats.
- [Utilization](/utilization/): $U = \sum_i C_i / T_i$, the long-run fraction of the processor that the tasks need. $U \le 1$ is necessary for feasibility on one processor.
- [Release time](/release-time/) and [deadline](/deadline/): the two time limits of one job, as in online scheduling.
- The *critical instant* of a task under fixed priorities is a release time at which the task meets the largest response time; for constrained deadlines the synchronous release is one (see [optimality of rate-monotonic priorities](/rate-monotonic-optimality/)).
- [Schedulability analysis](/schedulability-analysis/) decides from these parameters whether a given algorithm meets all deadlines.

## References
