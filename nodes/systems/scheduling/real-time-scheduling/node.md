---
tag: NV6SVW
kind: problem
slug: real-time-scheduling
name: Real-time scheduling
aliases:
- real-time task scheduling
- hard real-time scheduling problem
area: systems/scheduling
level: core
summary: "Run recurring tasks with execution times and deadlines so that every job ends by its deadline, and decide in advance that this is always true."
prereqs: [scheduling-problem, deadline, release-time, preemption]
see_also: [periodic-task-model, sporadic-task-model, earliest-deadline-first, rate-monotonic-scheduling, schedulability-analysis, fixed-priority-scheduling, cyclic-executive, maximum-lateness-minimization]
sources:
  - paper: doi:10.1145/321738.321743
    title: "C. L. Liu and James W. Layland, Scheduling algorithms for multiprogramming in a hard-real-time environment, Journal of the ACM 20(1) (1973), 46-61"
    locator: the periodic task model and its assumptions, the rate-monotonic and the deadline driven algorithms
  - book: isbn:9781461406754
    title: "Giorgio C. Buttazzo, Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, third edition, Springer, 2011"
    locator: Chapter 2 (basic concepts, task constraints and the classes of scheduling algorithms), Chapter 3 (aperiodic jobs) and Chapter 4 (periodic tasks)
  - book: isbn:9780130996510
    title: Jane W. S. Liu, Real-Time Systems, Prentice Hall, 2000
    locator: Chapter 3 (the reference model of real-time systems) and Chapter 4 (the approaches to real-time scheduling)
  - paper: doi:10.1007/BF01995675
    title: "Sanjoy K. Baruah, Louis E. Rosier and Rodney R. Howell, Algorithms and complexity concerning the preemptive scheduling of periodic, real-time tasks on one processor, Real-Time Systems 2(4) (1990), 301-324"
    locator: the processor demand test, its pseudo-polynomial bound, and the strong coNP-completeness of feasibility for tasks with offsets
  - paper: doi:10.1137/1.9781611973075.83
    title: "Friedrich Eisenbrand and Thomas Rothvoß, EDF-schedulability of synchronous periodic task systems is coNP-hard, SODA 2010, 1029-1034"
    locator: the main theorem (weak coNP-hardness for constrained deadlines and synchronous release)
---

Real-time scheduling is the problem of running a set of recurring tasks on one or more processors so that each job of each task finishes by its [deadline](/deadline/), and of proving before the system runs that this holds for every legal pattern of arrivals. The input is a task model, most often the [periodic](/periodic-task-model/) or the [sporadic](/sporadic-task-model/) model, in which task $\tau_i$ has a worst-case execution time $C_i$, a period $T_i$ and a relative deadline $D_i$. The goal is not a short schedule or a small average delay, as in the general [scheduling problem](/scheduling-problem/), but a guarantee with no exception. The two classic answers on one processor are [rate-monotonic](/rate-monotonic-scheduling/) priorities and [earliest deadline first](/earliest-deadline-first/).

## In plain words

A car's brake controller must read its sensors every 10 milliseconds and finish the computation within that time. The same processor also updates a display every 100 milliseconds. Each piece of work comes back again and again, and each one has a time limit. If the brake work is late one time, the result can be a crash, so "fast on average" is not good enough.

Real-time scheduling chooses which piece of work runs at each moment so that all time limits are met. Just as important, it asks a yes or no question before the system is built: with these tasks, this processor and this rule, is a late result possible? A good answer needs only the worst-case work of each task and the shortest gap between its arrivals.

## Definition

**Tasks and jobs.** A task system is a finite set $\tau = \{\tau_1, \ldots, \tau_n\}$. Task $\tau_i$ has a worst-case execution time $C_i > 0$, a period or minimum inter-arrival time $T_i > 0$ and a relative deadline $D_i > 0$. It releases an infinite sequence of jobs $J_{i,1}, J_{i,2}, \ldots$ with release times $r_{i,1} < r_{i,2} < \cdots$. Job $J_{i,k}$ needs at most $C_i$ units of processor time, and its absolute deadline is $d_{i,k} = r_{i,k} + D_i$.

- In the [periodic task model](/periodic-task-model/), $r_{i,k} = O_i + (k-1) T_i$ for a known offset $O_i \ge 0$.
- In the [sporadic task model](/sporadic-task-model/), the release times are unknown in advance, and only $r_{i,k+1} - r_{i,k} \ge T_i$ is known.

The deadlines are *implicit* if $D_i = T_i$ for each $i$, *constrained* if $D_i \le T_i$, and *arbitrary* otherwise. The utilization is $U = \sum_{i=1}^n C_i / T_i$ (see [utilization](/utilization/)).

**Schedules.** On $m$ identical processors, a schedule assigns to each processor at each time $t \ge 0$ at most one job. A job runs on at most one processor at a time, and never before its release time. In a [preemptive](/preemption/) schedule a job may be stopped and resumed later, with no cost; in a non-preemptive one, a job runs to the end once it starts. The schedule is *feasible* for a job sequence if each job $J_{i,k}$ receives its execution time in $[r_{i,k}, d_{i,k}]$.

**The questions.** For a task system $\tau$, a number of processors $m$ and a scheduling algorithm $A$:

1. *Feasibility.* Does a feasible schedule exist for each job sequence that $\tau$ can generate?
2. *Schedulability under $A$.* Is the schedule that $A$ makes feasible for each job sequence that $\tau$ can generate? A test that answers this question is a [schedulability test](/schedulability-analysis/). It is *exact* if it answers yes exactly for the schedulable systems, and *sufficient* if each yes is correct but some schedulable systems get a no.
3. *Dispatching.* At run time, decide at each moment which released job runs, without knowledge of later releases.

An algorithm $A$ is *optimal* for a class of task systems if each feasible system of the class is schedulable under $A$.

## Variants

- **Task model.** Periodic tasks with given offsets (asynchronous), periodic tasks with all offsets 0 (synchronous), or sporadic tasks. A sporadic system behaves as the synchronous periodic one in the worst case on one processor, under fixed priorities and under EDF.
- **Deadlines.** Implicit, constrained or arbitrary. Many exact results hold only for one of these classes.
- **Priority type.** *Fixed task priority:* each task has one priority for all its jobs, as in [rate-monotonic](/rate-monotonic-scheduling/) and [deadline-monotonic](/deadline-monotonic-scheduling/) scheduling (see [fixed-priority scheduling](/fixed-priority-scheduling/)). *Fixed job priority:* each job has one priority, but jobs of one task can differ, as in [EDF](/earliest-deadline-first/). *Dynamic job priority:* the priority of a job changes while it waits, as in [least laxity first](/least-laxity-first/).
- **Off-line tables.** A [cyclic executive](/cyclic-executive/) or a [time-triggered](/time-triggered-scheduling/) table fixes the whole schedule for one [hyperperiod](/hyperperiod/) before run time.
- **Processors.** One processor; many processors with *partitioned* scheduling (each task fixed to one processor); or *global* scheduling (a job may run on any processor). Optimal rules on one processor are not optimal on many: EDF fails on two processors for some systems with a utilization just above 1.
- **Shared resources.** With locks, a job can be blocked by a lower-priority job; this is [priority inversion](/priority-inversion/), bounded by the [priority inheritance](/priority-inheritance-protocol/) and [priority ceiling](/priority-ceiling-protocol/) protocols.
- **Aperiodic work.** Jobs with no minimum gap are served by a server task with a budget, for example a [sporadic server](/sporadic-server/), a [deferrable server](/deferrable-server/) or a [constant bandwidth server](/constant-bandwidth-server/).
- **Hard and soft deadlines.** A hard deadline must never be missed. A soft deadline may be missed, and the goal is then a bound on the lateness or on the rate of misses.

## Examples

**Feasible under EDF but not under fixed priorities.** Take $\tau_1 = (C_1, T_1) = (2, 5)$ and $\tau_2 = (4, 7)$ with implicit deadlines and synchronous release, so $U = 2/5 + 4/7 = 34/35$. Under rate-monotonic priorities ($\tau_1$ first), $\tau_1$ runs in $[0, 2)$ and $[5, 7)$, and $\tau_2$ gets only 3 units before its deadline 7, so its first job ends at 8. The other fixed-priority order ($\tau_2$ first) makes the first job of $\tau_1$ end at 6, after its deadline 5. So no fixed-priority order works. EDF runs $\tau_1$ in $[0, 2)$, $\tau_2$ in $[2, 6)$, $\tau_1$ in $[6, 8)$, $\tau_2$ in $[8, 12)$, and so on, and it meets all 12 deadlines of the hyperperiod $[0, 35)$. So the system is feasible.

**Infeasible with a utilization below 1.** Take $\tau_1 = (C, T, D) = (2, 4, 2)$ and $\tau_2 = (2, 6, 3)$, so $U = 5/6$. The two jobs released at time 0 need 4 units of work by time 3. No algorithm can do that, so the system is infeasible. With constrained deadlines, $U \le 1$ is not enough.

**One-shot jobs.** A finite set of jobs with release times and deadlines on one preemptive processor is the special case where each task releases one job. Then feasibility is the question whether the least maximum lateness of $1 \mid r_j, \text{pmtn} \mid L_{\max}$ is at most 0, and EDF answers it.

## Known algorithms

| algorithm | priority type | optimal for (one processor, preemptive) | exact test |
|---|---|---|---|
| [Rate-monotonic](/rate-monotonic-scheduling/) | fixed task | fixed priorities, implicit deadlines ([proof](/rate-monotonic-optimality/)) | [response-time analysis](/response-time-analysis/) |
| [Deadline-monotonic](/deadline-monotonic-scheduling/) | fixed task | fixed priorities, constrained deadlines | response-time analysis |
| [Earliest deadline first](/earliest-deadline-first/) | fixed job | all algorithms, any job set ([proof](/edf-optimality/)) | $U \le 1$ for implicit deadlines, processor demand for constrained ones |
| [Least laxity first](/least-laxity-first/) | dynamic job | all algorithms, any job set | as for EDF |
| [Cyclic executive](/cyclic-executive/) | off-line table | not applicable | the table itself |

Sufficient tests that cost $O(n)$ time are the [Liu-Layland bound](/liu-layland-utilization-bound/) $U \le n(2^{1/n} - 1)$ and the hyperbolic bound $\prod_i (U_i + 1) \le 2$ for rate-monotonic priorities.

## Bounds

All results below are for one preemptive processor, in the worst case over the input, with the numbers of the input in binary.

- **Implicit deadlines.** A periodic or sporadic system is feasible if and only if $U \le 1$ (Liu and Layland 1973). The test takes $O(n)$ arithmetic operations.
- **Constrained deadlines, synchronous or sporadic.** EDF is optimal, and the processor demand test is exact. It runs in pseudo-polynomial time when $U \le c$ for a constant $c < 1$ (Baruah, Rosier and Howell 1990). In general the problem is coNP-hard (Eisenbrand and Rothvoß 2010).
- **Periodic tasks with offsets.** Feasibility is coNP-complete in the strong sense (Baruah, Rosier and Howell 1990). An exact test simulates EDF over $[0, s + 2H)$, where $s$ is the largest offset and $H$ the [hyperperiod](/hyperperiod/); $H$ can be exponential in $n$.
- **Fixed priorities.** Computing the worst-case response time of one task is NP-hard (Eisenbrand and Rothvoß 2008), even though response-time analysis runs in pseudo-polynomial time.
- **Non-preemptive.** Even for one-shot jobs, $1 \mid r_j \mid L_{\max}$ is strongly NP-hard, so the non-preemptive feasibility of a job set with release times and deadlines is strongly NP-complete; see [scheduling with release times and deadlines](/scheduling-with-release-times-and-deadlines/).

## Reductions

- One-processor preemptive feasibility of a finite job set reduces to $1 \mid r_j, \text{pmtn} \mid L_{\max}$: the set is feasible if and only if the optimum $L_{\max}$ is at most 0. With all release times 0, this is the problem $1 \mid\mid L_{\max}$ of [maximum lateness minimization](/maximum-lateness-minimization/), solved by [earliest due date first](/earliest-due-date-first/). The [three-field notation](/scheduling-notation/) describes such one-shot problems; it has no field for recurring tasks.
- A sporadic task system on one processor reduces to the synchronous periodic system with the same parameters, for fixed priorities and for EDF: the synchronous pattern has the largest demand in each window.
- A periodic system with constrained deadlines and offsets reduces to a finite job set: the jobs released in $[0, s + 2H)$.

## Applications

Real-time scheduling is the base of the kernels of embedded and safety-critical systems: engine and brake controllers, flight control, robots, medical devices and industrial control. Fixed-priority scheduling with response-time analysis is the common practice in automotive and avionics systems, because the priorities are easy to check and an overload hits the low-priority tasks first. Linux offers fixed priorities (SCHED_FIFO and SCHED_RR) and an EDF class (SCHED_DEADLINE) that pairs EDF with a constant bandwidth server. Media players and network stacks use the same ideas with soft deadlines.

## References
