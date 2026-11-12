---
tag: BHFDS7
kind: concept
slug: fixed-priority-scheduling
name: Fixed-priority scheduling
aliases:
- static priority scheduling
area: systems/scheduling
level: core
summary: "Each task gets one priority before the system runs, and the dispatcher always runs the ready job whose task has the highest priority."
prereqs: [real-time-scheduling, periodic-task-model, priority-scheduling, preemption]
see_also: [rate-monotonic-scheduling, deadline-monotonic-scheduling, response-time-analysis, earliest-deadline-first, priority-inversion, priority-ceiling-protocol, sporadic-server, cyclic-executive]
sources:
  - paper: doi:10.1145/321738.321743
    title: "C. L. Liu and James W. Layland, Scheduling algorithms for multiprogramming in a hard-real-time environment, Journal of the ACM 20(1) (1973), 46-61"
    locator: the fixed priority assignment and the critical instant, compared with the deadline driven algorithm
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 4 (periodic task scheduling) and the comparison of fixed and dynamic priorities
  - paper: doi:10.1007/s11241-007-9012-7
    title: "Robert I. Davis, Alan Burns, Reinder J. Bril and Johan J. Lukkien, Controller Area Network (CAN) schedulability analysis: refuted, revisited and revised, Real-Time Systems 35(3) (2007), 239-272"
    locator: the analysis of non-preemptive fixed priorities over the busy period
  - book: isbn:9780130996510
    title: Jane W. S. Liu, Real-Time Systems, Prentice Hall, 2000
    locator: Chapter 6 (priority-driven scheduling of periodic tasks)
---

Fixed-priority scheduling is the class of [real-time scheduling](/real-time-scheduling/) rules in which each task gets one priority before the system runs, and every job of the task keeps that priority. At each time the dispatcher runs the ready job of highest priority, and with [preemption](/preemption/) it stops a running job as soon as a job of higher priority is released. The class leaves open how the priorities are chosen: [rate monotonic](/rate-monotonic-scheduling/) and [deadline monotonic](/deadline-monotonic-scheduling/) are two answers. It is the policy of almost every real-time kernel, because it is simple to build and its behavior under overload is easy to predict.

## In plain words

A hospital emergency room ranks its cases before the day starts: heart attacks first, broken bones next, small cuts last. A doctor always takes the waiting patient of highest rank. If a heart attack comes in while the doctor treats a cut, the doctor stops and goes to the heart attack.

The rank belongs to the kind of case, not to the patient, and it does not change during the day. So the rule is fast and easy to check. The cost is that the rule does not look at how soon each patient must be treated. A small cut with a very short time limit can still wait behind a long case of higher rank.

## The idea

**The model.** One processor runs $n$ tasks of the [periodic](/periodic-task-model/) or the [sporadic](/sporadic-task-model/) model. Task $\tau_i$ has a worst-case execution time $C_i$, a period or a minimum gap $T_i$ and a relative deadline $D_i$. Each task gets a priority $P_i$, and in the usual case all priorities are distinct. The tasks are independent unless the page says otherwise.

**Three levels of priority.** A rule is *fixed at task level* when all jobs of a task have one priority: this is fixed-priority scheduling. A rule is *fixed at job level* when each job gets a priority at its release and keeps it, but two jobs of the same task can get different priorities: [earliest deadline first](/earliest-deadline-first/) is the main example. A rule is *dynamic* when the priority of a job changes while it waits: [least laxity first](/least-laxity-first/) is an example.

**The dispatcher.** The ready jobs wait in a queue ordered by priority. On a release, the dispatcher puts the job in the queue, and if its priority is higher than that of the running job, it preempts the running job. When a job ends, the dispatcher runs the head of the queue. With $k$ priority levels, a kernel keeps one first-in, first-out list for each level and one word of flags that marks the levels that are not empty. Then each dispatch is a find-first-set on the flags and takes constant time. Jobs at the same level share it in turn, as with `SCHED_FIFO` and `SCHED_RR` in POSIX.

**Critical instant.** Under preemptive fixed priorities on one processor, with independent sporadic tasks and $D_i \le T_i$, the worst response time of a job of $\tau_i$ occurs when it is released at the same time as a job of each task of higher priority, and those tasks then release as fast as they may. Liu and Layland stated this for periodic tasks. So one scenario per task is enough for an exact test, and [response-time analysis](/response-time-analysis/) uses it. That page gives the test, which is exact for this model.

**Fixed priorities compared with EDF.** On one processor with preemption and independent tasks, EDF is optimal: if any rule meets all deadlines, EDF does. For implicit deadlines, EDF meets all deadlines if and only if the [utilization](/utilization/) $U = \sum_i C_i / T_i$ is at most 1. No fixed-priority rule reaches that: some task sets with $U = 1$, and also some with less, have no feasible fixed order. The [Liu and Layland bound](/liu-layland-utilization-bound/) gives the utilization below which rate monotonic always works. In return, fixed priorities have these advantages:

- The kernel needs no deadline arithmetic. A priority is a small integer, and most hardware and operating systems give only fixed priorities.
- Under overload, the tasks of low priority miss their deadlines first, and a task of high priority does not see the overload. Under EDF, one job that runs too long can make many jobs of all tasks late.
- Interrupts, bus messages and kernel threads all have fixed priorities already, so one analysis can cover them all.

**Non-preemptive fixed priorities.** If a job runs to its end once it starts, a job of higher priority can wait for a job of lower priority that started a moment before it. This is blocking by lower-priority jobs, the same effect as a long [priority inversion](/priority-inversion/). For task $\tau_i$ the blocking term is the longest $C_j$ of a task of lower priority, minus one time unit in discrete time. There are two other changes. The critical instant is no longer enough: a later job in the same busy period can have a longer response time than the first one, so an exact test must check every job in the level-$i$ busy period. Davis, Burns, Bril and Lukkien showed that an earlier analysis of the Controller Area Network bus missed this case. Second, a low utilization is no guarantee: a long job of low priority can make a short job of high priority late.

**Shared resources.** With locks, a job can wait for a job of lower priority that holds a lock. The [priority inheritance protocol](/priority-inheritance-protocol/) and the [priority ceiling protocol](/priority-ceiling-protocol/) bound this wait. Aperiodic work fits in through a server at a fixed priority, such as the [deferrable server](/deferrable-server/) or the [sporadic server](/sporadic-server/).

## Examples

**Preemptive compared with non-preemptive.** Let $\tau_1$ have $C_1 = 1$, $T_1 = D_1 = 3$, first release at 1 and high priority. Let $\tau_2$ have $C_2 = 4$, $T_2 = D_2 = 12$, release at 0 and low priority. The utilization is $1/3 + 1/3 = 2/3$.

| slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| preemptive | $\tau_2$ | $\tau_1$ | $\tau_2$ | $\tau_2$ | $\tau_1$ | $\tau_2$ | idle | $\tau_1$ |
| non-preemptive | $\tau_2$ | $\tau_2$ | $\tau_2$ | $\tau_2$ | $\tau_1$ late | $\tau_1$ | idle | $\tau_1$ |

With preemption every job meets its deadline. Without preemption, the first job of $\tau_1$ (released at 1, deadline 4) waits until $\tau_2$ ends at 4 and finishes at 5, one unit late.

**A set that only EDF can schedule.** Let $\tau_1 = (C, T) = (2, 4)$ and $\tau_2 = (5, 10)$, with implicit deadlines and release at 0, so $U = 1/2 + 1/2 = 1$.

| slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\tau_1$ high | $\tau_1$ | $\tau_1$ | $\tau_2$ | $\tau_2$ | $\tau_1$ | $\tau_1$ | $\tau_2$ | $\tau_2$ | $\tau_1$ | $\tau_1$ |
| EDF | $\tau_1$ | $\tau_1$ | $\tau_2$ | $\tau_2$ | $\tau_1$ | $\tau_1$ | $\tau_2$ | $\tau_2$ | $\tau_2$ | $\tau_1$ |

With $\tau_1$ on top, $\tau_2$ gets only 4 units before its deadline 10 and misses it. With $\tau_2$ on top, $\tau_2$ runs from 0 to 5 and $\tau_1$ misses its deadline 4. So no fixed order works. At time 8, EDF prefers $\tau_2$ (deadline 10) to the third job of $\tau_1$ (deadline 12), and both meet their deadlines.

## Where it is used

- **Real-time kernels.** VxWorks, FreeRTOS, RTEMS, the OSEK and AUTOSAR operating systems and the `SCHED_FIFO` and `SCHED_RR` classes of POSIX and Linux all dispatch by fixed priority.
- **Buses and interrupts.** The Controller Area Network sends the waiting message with the highest priority, and a message is not stopped once it starts, so CAN is a non-preemptive fixed-priority system. Interrupt controllers serve requests by fixed priority levels.
- **Avionics and automotive standards.** Partitioned systems often run fixed priorities inside each partition, and the certification evidence is a [schedulability analysis](/schedulability-analysis/) for fixed priorities.

## References
