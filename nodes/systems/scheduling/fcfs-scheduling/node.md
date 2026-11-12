---
tag: TCCY97
kind: algorithm
slug: fcfs-scheduling
name: First-come, first-served scheduling
aliases:
- FIFO scheduling
- FCFS
- FCFS scheduling
area: systems/scheduling
level: intro
summary: "Run the ready processes in order of arrival, each to the end of its CPU burst. Simple and fair in order, but one long burst makes all later ones wait: the convoy effect."
solves: [cpu-scheduling]
model: real-ram
complexity:
  vars: {n: the number of processes}
  time: {worst: O(n log n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [cpu-scheduling, scheduling-metrics, queue]
see_also: [shortest-job-first, round-robin, sjf-optimality, work-conserving-scheduling, priority-scheduling, preemption, earliest-due-date-first]
sources:
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.3.1 (first-come, first-served scheduling, the example with bursts 24, 3 and 3, and the convoy effect)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces, version 1.10
    locator: Chapter 7, Section 7.3 (first in, first out, and the convoy effect)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 2, Section 2.4.2 (scheduling in batch systems, first-come, first-served)
  - paper: "Mike Blasgen, Jim Gray, Mike Mitoma and Tom Price, The convoy phenomenon, ACM SIGOPS Operating Systems Review 13(2), 1979"
    locator: the whole note (a convoy of processes that queue behind one lock and stay together)
---

First-come, first-served (FCFS) scheduling runs the ready processes in the order in which they arrived, and lets each one keep the CPU until its CPU burst ends. It is the simplest solution of [CPU scheduling](/cpu-scheduling/): the ready queue is a FIFO [queue](/queue/), each decision takes $O(1)$ time, and no process waits behind one that came later. Its weakness is the convoy effect: when a long burst comes first, all shorter ones wait for it, and the mean waiting time can be any factor worse than that of [shortest-job-first](/shortest-job-first/).

## In plain words

FCFS is the line at a post office with one clerk. People are served in the order they came in. Each person stays at the counter until their business is done. Nobody can push ahead.

This is fair in one sense, and very easy to run. But if the first person in line has a big pile of parcels, everyone behind waits a long time, even those who only want one stamp. If the stamp buyers had gone first, they would have waited a little, and the person with parcels would have waited only a little more. The total waiting would be much smaller.

The same thing happens with programs. A long computation at the front of the line holds up many short ones. This is called the convoy effect.

## The problem

The input is $n$ processes on one CPU. Process $i$ arrives at time $a_i \ge 0$ and needs one CPU burst of length $b_i > 0$. The output is a start time $S_i$ and a completion time $C_i = S_i + b_i$ for each process, with the processes run one at a time and never interrupted. This is the single-burst form of [CPU scheduling](/cpu-scheduling/), the problem $1 \mid r_j \mid \gamma$ of [single-machine scheduling](/single-machine-scheduling/). FCFS does not use $b_i$ to make its choices.

## The algorithm

As an online policy, FCFS appends each arriving process to the tail of the ready queue and, whenever the CPU is free, dispatches the process at the head. The offline form below computes the same schedule from the whole input.

```pseudo id=main
FCFS(a, b)                                 ▷ arrivals a[1..n], bursts b[1..n]
L1  Q ← the processes in order of a[i], ties by index i
L2  t ← 0
L3  for each process i in Q, in order do
L4      if t < a[i] then t ← a[i]            ▷ the CPU is idle until i arrives
L5      S[i] ← t                              ▷ i is dispatched
L6      t ← t + b[i]                          ▷ i runs to the end of its burst
L7      C[i] ← t
L8  return S, C
```

Line L1 is the FIFO order of the ready queue: a process that arrives earlier is enqueued earlier. Line L4 is the only place where the CPU is idle, and it is idle only when every process that has arrived is finished. Lines L5 to L7 run the process without a break, which is what nonpreemptive means. With ties broken by index, the result is the one schedule that a FIFO ready queue produces.

## Example

**The convoy effect.** Three processes arrive at time 0 in the order P1, P2, P3 with bursts 24, 3 and 3 ms (Silberschatz, Section 5.3.1).

| order | P1 waits | P2 waits | P3 waits | mean waiting |
|---|---|---|---|---|
| P1, P2, P3 | 0 | 24 | 27 | 17 |
| P2, P3, P1 | 6 | 0 | 3 | 3 |

The same three bursts, in another order, cut the mean waiting time from 17 to 3.

**Arrivals and an idle gap.** Six processes, with times in ms:

| step | process | $a_i$ | $b_i$ | $t$ before | $S_i$ | $C_i$ | waiting $S_i - a_i$ |
|---|---|---|---|---|---|---|---|
| 1 | A | 0 | 5 | 0 | 0 | 5 | 0 |
| 2 | B | 1 | 3 | 5 | 5 | 8 | 4 |
| 3 | C | 2 | 8 | 8 | 8 | 16 | 6 |
| 4 | D | 3 | 2 | 16 | 16 | 18 | 13 |
| 5 | E | 20 | 3 | 18 | 20 | 23 | 0 |
| 6 | F | 21 | 1 | 23 | 23 | 24 | 2 |

At step 5, line L4 moves the clock from 18 to 20: the CPU is idle because nothing has arrived. The total waiting time is 25, a mean of about 4.17. D, with the shortest burst of the first group, waits longest, because it came last.

## Correctness

The claim is that FCFS returns a feasible nonpreemptive schedule that runs the processes in arrival order and is work-conserving, with $S_{q_1} = a_{q_1}$ and $S_{q_k} = \max(C_{q_{k-1}}, a_{q_k})$ for the order $q_1, \ldots, q_n$ of line L1. The invariant of the loop of line L3 is: $t$ is the completion time of the last process placed, the intervals placed so far do not overlap, and the CPU was idle before $t$ only at times when every arrived process was finished. The full proof, with the waiting-time formula, is in the proof file.

## Complexity

- **Time.** Line L1 sorts $n$ processes, $O(n \log n)$ in the worst case. Lines L3 to L7 take $O(1)$ per process, $\Theta(n)$ in total. When the processes come in order of arrival, as they do online, the sort is not needed and the time is $\Theta(n)$, $O(1)$ per enqueue and per dispatch.
- **Space.** $\Theta(n)$ extra for $Q$, $S$ and $C$.
- **Dispatches.** Exactly $n$, one per process, the least possible. FCFS pays the dispatch latency $\delta$ only $n$ times.

**Waiting time.** If all processes arrive at time 0, the $k$-th process waits for the bursts of the $k - 1$ before it, so the total waiting time is $\sum_{k=1}^{n} (n - k)\, b_{q_k}$. Each burst counts once for each process behind it. One long burst at the front counts $n - 1$ times. With one burst $L$ before $k$ bursts $s$, the mean waiting time of FCFS divided by that of the short-first order is $2L/(s(k+1)) + (k-1)/(k+1)$, which has no upper bound as $L/s$ grows.

## Properties

- **Nonpreemptive.** A process keeps the CPU until its burst ends or it starts an I/O burst. So FCFS is unsuitable for time-sharing, where each user must get the CPU at regular intervals.
- **Work-conserving.** The CPU is never idle while a process is ready. So FCFS has the same busy periods, utilization and throughput as any other [work-conserving](/work-conserving-scheduling/) policy on the same single-burst trace.
- **No starvation.** Each process waits at most the sum of the bursts that arrived before it. Unlike [priority scheduling](/priority-scheduling/), FCFS needs no [aging](/aging/).
- **Order fair, not size fair.** No process is passed by a later one, but a short process can wait many times its own length. Its [stretch](/stretch/) is unbounded.
- **Non-clairvoyant.** FCFS needs neither the burst lengths nor a prediction of them.

## Variants and improvements

- **[Round robin](/round-robin/).** FCFS with a timer: after a quantum $q$, the running process goes to the tail of the queue. With $q$ larger than every burst, round robin is FCFS.
- **[Shortest-job-first](/shortest-job-first/).** Choose by the predicted burst instead of the arrival time. It minimizes the mean waiting time when all processes are present ([proof](/sjf-optimality/)).
- **FCFS within a priority level.** [Priority scheduling](/priority-scheduling/) and the [multilevel queue](/multilevel-queue-scheduling/) use FCFS to break ties among processes of equal priority.
- **FIFO in other places.** The same discipline is the default of network queues, of the [disk scheduling](/disk-scheduling/) of requests, and of fair locks.

## When to use it

Use FCFS for batch work in which the jobs are of similar length, or when the order of service must match the order of requests, as for a log, a printer queue or a lock that must not let later requests pass. It is also the base case of a simulator. Do not use it alone for interactive systems: one long CPU burst stops all other processes, including those that only need the CPU for a moment to answer the user.

## Pitfalls

- **Ties.** Two processes that arrive at the same time must be ordered by a fixed rule, such as the index in line L1. A sort that is not stable, or a hash set as the ready queue, gives a different schedule from run to run.
- **Waiting time is not response time in general.** For FCFS, line L5 gives $S_i - a_i$ both as the waiting time and as the response time. This equality holds only for nonpreemptive policies and single bursts; for a process with I/O, add the waits of each burst.
- **The convoy with I/O.** In a mix of one CPU-bound process and many I/O-bound processes, the I/O-bound processes finish their I/O, queue behind the long CPU burst, and leave the I/O devices idle. Then they all run their short bursts and go back to I/O together, and the CPU sits idle. Both the CPU and the devices are less busy than with a preemptive policy (Silberschatz, Section 5.3.1).
- **Idle time at line L4.** Forgetting the jump of line L4, or writing $t \leftarrow t + a_i$, gives start times before the arrival of a process or long false gaps.

## Implementations

## History

Service in order of arrival is the default discipline of queueing theory. The operating-systems textbooks present it as the first CPU scheduling algorithm and use the bursts 24, 3 and 3 to show the convoy effect (Silberschatz, Galvin and Gagne, Section 5.3.1). The word convoy comes from Blasgen, Gray, Mitoma and Price (1979), who described processes in a database system that queue behind one heavily used lock and then stay together as a group for a long time.

## References
