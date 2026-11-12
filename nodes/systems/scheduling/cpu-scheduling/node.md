---
tag: DMSXXK
kind: problem
slug: cpu-scheduling
name: CPU scheduling
aliases:
- process scheduling
- short-term scheduling
area: systems/scheduling
level: intro
summary: "Decide, at each scheduling point, which process in the ready queue runs next on the CPU and for how long, given arrivals, CPU and I/O bursts, and a cost per context switch."
prereqs: [scheduling-problem, scheduling-metrics, queue]
see_also: [fcfs-scheduling, shortest-job-first, round-robin, priority-scheduling, preemption, multilevel-feedback-queue, completely-fair-scheduler, real-time-scheduling]
sources:
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.1 (CPU and I/O burst cycle, the CPU scheduler, preemptive and nonpreemptive scheduling, the dispatcher), Section 5.2 (criteria) and Section 5.3 (algorithms); Chapter 3, Section 3.2 (scheduling queues and swapping)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 2, Section 2.4 (when to schedule, batch, interactive and real-time systems, and the algorithms)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces, version 1.10
    locator: Chapter 7, Scheduling, Introduction (workload assumptions, turnaround and response time, the effect of I/O)
---

CPU scheduling is the problem that an operating system solves each time the CPU becomes free or a process becomes ready: choose the process in the ready queue that runs next, and decide how long it may run. It is the operating-system case of the [scheduling problem](/scheduling-problem/) with one resource, the CPU. Three things make it differ from the offline machine scheduling of [single-machine scheduling](/single-machine-scheduling/): the scheduler is online, it usually does not know how long the next CPU burst is, and each switch from one process to another costs time.

## In plain words

A computer runs many programs, but one CPU can run only one of them at a time. Most programs run on the CPU for a short time, then wait for the disk, the network or the keyboard, then run again. The programs that can run now wait in a line, the ready queue.

The scheduler is the small part of the operating system that picks the next program from this line. It must pick again each time the running program stops to wait, ends, or is interrupted, and each time a waiting program becomes ready. A second part, the dispatcher, then does the switch, and the switch itself takes time.

A good choice keeps the CPU busy, finishes jobs soon after they arrive, and lets an interactive user see an answer quickly. These goals pull in different directions, so there are many schedulers.

## Definition

**Processes.** There are $n$ processes. Process $i$ arrives at time $a_i \ge 0$ and alternates CPU bursts and I/O bursts:

$$b_{i,1},\ d_{i,1},\ b_{i,2},\ d_{i,2},\ \ldots,\ b_{i,k_i}, \qquad b_{i,j} > 0,\ d_{i,j} > 0.$$

A process is *ready* when it waits only for the CPU, *running* when it holds the CPU, and *waiting* while it does an I/O burst. The I/O devices work in parallel with the CPU. The *ready queue* $R(t)$ is the set of ready processes at time $t$.

**Schedules.** A schedule says, for each time $t$, whether the CPU runs one process of $R(t)$, runs the dispatcher, or is idle. A process runs only while it is ready or running, and its CPU burst $b_{i,j}$ ends after it has had $b_{i,j}$ units of CPU time since the burst began.

**The dispatcher.** Each time the CPU passes to another process, the dispatcher saves the state of the old process, loads the state of the new one, switches to user mode and jumps into the new process. The time for this is the *dispatch latency* $\delta \ge 0$. A schedule with $s$ dispatches spends $s\delta$ units on them.

**Decision points.** The scheduler may make a choice at four kinds of events (Silberschatz, Section 5.1.3):

1. the running process starts an I/O burst or waits for an event (running to waiting);
2. an interrupt, for example the timer, moves the running process back to the ready queue (running to ready);
3. a process ends its I/O burst (waiting to ready);
4. the running process ends.

A scheduler that chooses only at events 1 and 4 is *nonpreemptive*, or cooperative: a process keeps the CPU until it gives it up. A scheduler that may also take the CPU away at events 2 and 3 is *preemptive*; see [preemption](/preemption/).

**The policy and its knowledge.** The short-term scheduler is a rule $\pi$ that maps what is known at a decision point to a process of $R(t)$. In a real system it knows the past: the arrival times, the lengths of the bursts that have ended, the priorities. It does not know the length of the burst that is about to run, and it does not know future arrivals. So it is an online and [non-clairvoyant](/clairvoyant-scheduling/) rule. Some policies, such as [shortest-job-first](/shortest-job-first/), use a prediction of the next burst instead.

**The objective.** The goal is one or more of the [scheduling metrics](/scheduling-metrics/): high CPU [utilization](/utilization/) and throughput, low average turnaround and waiting time, and low response time for interactive processes.

### Three levels of scheduling

| level | it decides | how often |
|---|---|---|
| long-term (job) scheduler | which submitted jobs are admitted into memory, and so the degree of multiprogramming | seconds or minutes, in batch systems |
| medium-term scheduler | which processes are swapped out of memory and later swapped back in | when memory is short |
| short-term (CPU) scheduler | which ready process gets the CPU next | at each decision point, often every few milliseconds |

This page is about the short-term scheduler. It runs so often that each decision must take $O(1)$ or $O(\log n)$ time.

## Variants

- **Nonpreemptive or preemptive.** See the decision points above and the page on [preemption](/preemption/).
- **The kind of system.** Tanenbaum and Bos (Section 2.4.1) separate batch systems (throughput, turnaround, CPU utilization), interactive systems (response time, and the delay that users expect), and real-time systems (deadlines). The real-time case has its own models and tests; see [real-time scheduling](/real-time-scheduling/).
- **One CPU or many.** With several CPUs the scheduler also places processes on CPUs, keeps a process near the cache it has warmed (processor affinity) and balances the load. [Gang scheduling](/gang-scheduling/) runs the threads of one program at the same time.
- **Single burst or burst cycle.** The textbook examples often give each process one CPU burst and no I/O. Then the problem is the single-machine problem with release dates, $1 \mid r_j \mid \gamma$ or $1 \mid r_j, \mathrm{pmtn} \mid \gamma$ in the [three-field notation](/scheduling-notation/).
- **Fair share.** The goal is to give each user or group a set share of the CPU, as in [lottery scheduling](/lottery-scheduling/), [stride scheduling](/stride-scheduling/) and the [completely fair scheduler](/completely-fair-scheduler/).

## Examples

Three processes, with times in milliseconds and $\delta = 0$:

| process | arrival | bursts (CPU, I/O, CPU) |
|---|---|---|
| A | 0 | 4, 6, 2 |
| B | 1 | 3, 2, 3 |
| C | 2 | 5 |

**First-come, first-served** ([FCFS](/fcfs-scheduling/)), nonpreemptive. A runs from 0 to 4 and starts its I/O, which ends at 10. B runs from 4 to 7 and starts its I/O, which ends at 9. C runs from 7 to 12. At 12 the ready queue holds B (ready since 9) and then A (ready since 10), so B runs from 12 to 15 and A from 15 to 17.

| time | 0 to 4 | 4 to 7 | 7 to 12 | 12 to 15 | 15 to 17 |
|---|---|---|---|---|---|
| CPU | A | B | C | B | A |

The completion times are A 17, B 15 and C 12, and the times spent in the ready queue are A 5, B 6 and C 5, 16 in total. The CPU is never idle: while A does its I/O from 4 to 10, B and C use the CPU. There are 2 decisions of kind 1, 2 of kind 3 and 3 of kind 4, and 5 dispatches.

**Shortest next burst first**, nonpreemptive. Up to time 12 the choices are the same. At 12 the ready queue holds B, which needs 3, and A, which needs 2, so A runs from 12 to 14 and B from 14 to 17. The ready times become A 2, B 8 and C 5, 15 in total, one less than FCFS. The average waiting time falls, but B now finishes last.

**Round robin with a quantum of 2 and $\delta = 1/2$.** Each dispatch costs half a unit. The schedule has 10 dispatches, so 5 units go to the dispatcher. The completion times grow to C 18, A $20\tfrac12$ and B 22, and only $17/22 \approx 77.3\%$ of the time is useful work. This is the price that [round robin](/round-robin/) pays for its short response time when the quantum is close to the dispatch latency.

## Known algorithms

| policy | preemptive | needs the burst length | cost of one decision |
|---|---|---|---|
| [first-come, first-served](/fcfs-scheduling/) | no | no | $O(1)$ with a FIFO [queue](/queue/) |
| [shortest-job-first](/shortest-job-first/) | no | a prediction | $O(\log n)$ with a [binary heap](/binary-heap/) |
| [shortest remaining processing time](/srpt/) | yes | yes, or a prediction | $O(\log n)$ |
| [round robin](/round-robin/) | yes, by a timer | no | $O(1)$ |
| [priority scheduling](/priority-scheduling/) with [aging](/aging/) | either | no | $O(\log n)$, or $O(1)$ with one queue per level |
| [multilevel queue](/multilevel-queue-scheduling/) and [multilevel feedback queue](/multilevel-feedback-queue/) | yes | no, it learns from the past | $O(1)$ for a fixed number of levels |
| [lottery](/lottery-scheduling/), [stride](/stride-scheduling/) and the [completely fair scheduler](/completely-fair-scheduler/) | yes | no | $O(\log n)$ |
| [earliest deadline first](/earliest-deadline-first/) and [rate monotonic](/rate-monotonic-scheduling/) | yes | worst-case execution times | $O(\log n)$ |

## Bounds

- **One burst per process, all present at time 0.** Shortest-job-first minimizes the average waiting time over all schedules; see [optimality of SJF](/sjf-optimality/).
- **Arrivals over time.** With preemption at no cost, SRPT minimizes the total turnaround time on one CPU ([Schrage 1968](/srpt-optimality/)). Without preemption the problem $1 \mid r_j \mid \sum C_j$ is strongly NP-hard even offline (Lenstra, Rinnooy Kan and Brucker 1977); see [flow time minimization](/flow-time-minimization/).
- **No knowledge of burst lengths.** A deterministic non-clairvoyant scheduler cannot be within a constant factor of SRPT for total flow time: the best ratio is $\Omega(n^{1/3})$ (Motwani, Phillips and Torng 1994). The details are on [non-clairvoyant flow time minimization](/non-clairvoyant-flow-time-minimization/).
- **Busy time.** Every [work-conserving](/work-conserving-scheduling/) policy has the same busy periods for the same single-burst trace, so the choice of policy cannot change utilization or throughput there, only the order of the jobs.
- **Context switches.** A schedule of $n$ single-burst processes needs at least $n$ dispatches. A nonpreemptive policy uses exactly one per burst. A preemptive one adds one per preemption, and with a quantum $q$ a burst of length $b$ costs up to $\lceil b/q \rceil$ dispatches.

## Reductions

- With one CPU burst per process, no I/O and $\delta = 0$, CPU scheduling is the machine scheduling problem $1 \mid r_j \mid \gamma$, or $1 \mid r_j, \mathrm{pmtn} \mid \gamma$ with preemption, where $\gamma$ is the chosen metric; see [single-machine scheduling](/single-machine-scheduling/). With $m$ CPUs it is $P \mid r_j \mid \gamma$.
- A process with I/O bursts is a chain of jobs with delays between them: burst $j + 1$ is released $d_{i,j}$ units after burst $j$ ends. The release times then depend on the schedule, which is why the textbook analysis treats each CPU burst as one job.

## Applications

Each general-purpose kernel has a short-term scheduler. Linux used the [completely fair scheduler](/completely-fair-scheduler/) from version 2.6.23 (2007) and replaced it with an EEVDF scheduler in version 6.6 (2023). Windows uses preemptive priority scheduling with 32 priority levels and a quantum for threads of equal priority. Real-time kernels use fixed priorities or deadlines with the tests of [schedulability analysis](/schedulability-analysis/). The same problem appears one level up, in the schedulers of language runtimes, databases and cluster managers ([cluster scheduling](/cluster-scheduling/)), and one level down, in the [disk scheduling](/disk-scheduling/) of I/O requests.

## References
