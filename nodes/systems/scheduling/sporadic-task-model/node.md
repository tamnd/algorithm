---
tag: GJNSR6
kind: definition
slug: sporadic-task-model
name: Sporadic task model
aliases:
- sporadic task
- sporadic task system
area: systems/scheduling
level: advanced
summary: "Each task releases jobs at least T time units apart, at times that are not known in advance. Each job needs at most C units of processor time and must end D units after its release."
prereqs: [periodic-task-model]
see_also: [periodic-task-model, sporadic-server, earliest-deadline-first, response-time-analysis, schedulability-analysis, rate-monotonic-optimality, hyperperiod]
sources:
  - paper: "Aloysius K. Mok, Fundamental design problems of distributed systems for the hard-real-time environment, PhD thesis, Massachusetts Institute of Technology, 1983"
    locator: the sporadic process, with a minimum separation between two requests, and its scheduling on one processor
  - paper: doi:10.1007/BF01995675
    title: "Sanjoy K. Baruah, Louis E. Rosier and Rodney R. Howell, Algorithms and complexity concerning the preemptive scheduling of periodic, real-time tasks on one processor, Real-Time Systems 2(4) (1990), 301-324"
    locator: the demand of a task in an interval, and the feasibility of synchronous and asynchronous periodic systems
  - paper: "Sanjoy K. Baruah, Aloysius K. Mok and Louis E. Rosier, Preemptively scheduling hard-real-time sporadic tasks on one processor, Proceedings of the 11th IEEE Real-Time Systems Symposium, 1990"
    locator: the feasibility test for sporadic task systems with arbitrary deadlines by the demand in an interval
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapters 4 and 5 (periodic tasks, and aperiodic and sporadic requests)
---

The sporadic task model describes a real-time task that releases jobs at unknown times, but never closer than a minimum gap: task $\tau_i = (C_i, T_i, D_i)$ releases jobs at least $T_i$ time units apart, each job needs at most $C_i$ units of processor time, and each job must end $D_i$ time units after its release. Mok introduced it in 1983 for events such as interrupts with a known maximum rate. On one processor the worst case of a sporadic system is the [synchronous periodic](/periodic-task-model/) pattern with the same parameters, so most tests for periodic tasks carry over.

## Definition

A **sporadic task** is a tuple $\tau_i = (C_i, T_i, D_i)$ with $C_i > 0$, $T_i > 0$ and $D_i > 0$:

- $C_i$ is the *worst-case execution time* of one job;
- $T_i$ is the *minimum inter-arrival time*: two releases of the task are at least $T_i$ apart;
- $D_i$ is the *relative deadline*.

A **legal job sequence** of $\tau_i$ is a sequence of jobs with release times $r_1 < r_2 < \cdots$ such that $r_{k+1} - r_k \ge T_i$ for each $k$, with execution times $0 < c_k \le C_i$ and deadlines $d_k = r_k + D_i$. A **sporadic task system** $\tau = \{\tau_1, \ldots, \tau_n\}$ is a finite set of independent sporadic tasks. A legal job sequence of the system is the union of one legal job sequence of each task.

A scheduling algorithm **schedules** a sporadic system if it meets each deadline of each legal job sequence of the system. The system is **feasible** on a platform if, for each legal job sequence, some schedule meets all its deadlines. The release times are not known in advance, so a scheduler must decide online.

The words *implicit deadlines* ($D_i = T_i$), *constrained deadlines* ($D_i \le T_i$), *arbitrary deadlines*, *utilization* $U = \sum_i C_i / T_i$ and *density* $\sum_i C_i / \min(D_i, T_i)$ have the same meaning as in the [periodic task model](/periodic-task-model/).

**The worst case on one processor.** For task $\tau_i$ and a length $t > 0$, let

$$\operatorname{dbf}_i(t) = \max\left(0, \left\lfloor \frac{t - D_i}{T_i} \right\rfloor + 1\right) C_i .$$

In a legal job sequence, the jobs of $\tau_i$ with release and deadline in an interval of length $t$ need at most $\operatorname{dbf}_i(t)$ work, since their releases lie in a window of length $t - D_i$ and are $T_i$ apart. The synchronous periodic sequence (all tasks release at 0, then as often as the gaps allow, with $c_k = C_i$) reaches this value for each $t$ at once. Two results follow:

- under [earliest deadline first](/earliest-deadline-first/), a sporadic system meets all deadlines if and only if $\sum_i \operatorname{dbf}_i(t) \le t$ for each $t > 0$, which is true if and only if EDF meets all deadlines of the synchronous periodic sequence;
- under fixed priorities with $D_i \le T_i$, the worst response time of each task occurs when it releases a job together with all tasks of higher priority, which then release as often as they can (the critical instant theorem, proved on the page on [rate-monotonic optimality](/rate-monotonic-optimality/)).

So on one processor, a sporadic system with constrained deadlines is schedulable by EDF or by a fixed-priority order exactly when the synchronous periodic system with the same parameters is. On several processors under global scheduling, the synchronous release is not always the worst case, and the analysis is harder.

## Examples and non-examples

**A legal sequence.** For $\tau = (C, T, D) = (1, 4, 4)$, the releases $0, 4, 9, 20$ form a legal sequence: the gaps are $4, 5, 11$. The releases $0, 3$ do not, because the gap 3 is less than $T = 4$.

**A sporadic system is harder than its periodic one with offsets.** Take two tasks with $C = 2$, $T = 4$ and $D = 2$. As periodic tasks with offsets 0 and 2, they are feasible: the first task runs in $[0, 2)$, $[4, 6)$, and so on, and the second task in $[2, 4)$, $[6, 8)$, and so on, with $U = 1$. As sporadic tasks, both can release a job at time 0. Then 4 units of work must end by time 2, which no schedule can do. The demand bound gives the same answer: $\operatorname{dbf}_1(2) + \operatorname{dbf}_2(2) = 4 > 2$.

**An interrupt with a known rate.** A sensor that raises an interrupt at most once per millisecond, with a handler of at most 50 microseconds that must end in 200 microseconds, is the sporadic task $(0.05, 1, 0.2)$ in milliseconds.

**Non-examples.**

- A job that comes once at an unknown time with no bound on its rate is *aperiodic*. It has no minimum gap, so no hard guarantee is possible from the model alone; a [sporadic server](/sporadic-server/) gives such jobs a share of the processor without harm to the other tasks.
- A task whose jobs come in bursts, for example 3 jobs at the same time once every 100 ms, is not sporadic with $T = 100$. It fits the model only with $T = 0$, which is not allowed; models with arrival curves or several frames describe it.
- A periodic task with known release times is a special case: it has one legal sequence. An analysis for the periodic case with offsets can give a weaker test for the sporadic case, as the second example shows.

## Related definitions

- [Periodic task model](/periodic-task-model/): $T_i$ is an exact period, and the releases are known.
- *Demand bound function*: $\operatorname{dbf}(t) = \sum_i \operatorname{dbf}_i(t)$, the basis of the processor demand test for [EDF](/earliest-deadline-first/).
- *Critical instant*: the release pattern that gives a task its largest response time under fixed priorities; for sporadic tasks with constrained deadlines it is the synchronous release ([rate-monotonic optimality](/rate-monotonic-optimality/)).
- [Response-time analysis](/response-time-analysis/): the exact test for fixed priorities, which holds for sporadic tasks as well.
- [Sporadic server](/sporadic-server/): a server that makes a stream of aperiodic jobs look like a sporadic task to the analysis.
- [Release time](/release-time/) and [deadline](/deadline/): the two time limits of one job.

## References
