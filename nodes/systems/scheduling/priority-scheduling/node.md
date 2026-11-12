---
tag: RDGF8V
kind: algorithm
slug: priority-scheduling
name: Priority scheduling
aliases:
- priority CPU scheduling
- highest-priority-first scheduling
area: systems/scheduling
level: intro
summary: "Run the ready process with the highest priority, with or without preemption. Simple and flexible, but a low-priority process can starve unless the system uses aging."
solves: [cpu-scheduling]
model: real-ram
complexity:
  vars: {n: the number of processes}
  time: {worst: O(n log n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [cpu-scheduling, preemption, priority-queue, fcfs-scheduling]
see_also: [aging, starvation, shortest-job-first, multilevel-queue-scheduling, fixed-priority-scheduling, priority-inversion, rate-monotonic-scheduling, round-robin]
sources:
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.3.4 (priority scheduling, the example with five processes and mean waiting time 8.2, internal and external priorities, preemption, starvation and aging)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 2, Section 2.4.3 (priority scheduling, priority classes with round robin inside each class, and the dynamic priority 1/f for I/O-bound processes)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched-mlfq.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces, version 1.10
    locator: Chapter 8 (the multilevel feedback queue, where priorities change with the behavior of a job)
---

Priority scheduling gives each process a priority and always runs the ready process of highest priority. In the nonpreemptive form, the choice is made only when the CPU becomes free. In the preemptive form, a newly ready process of higher priority takes the CPU at once. Many policies are priority scheduling with a particular choice of priority: [FCFS](/fcfs-scheduling/) uses the arrival time, [shortest-job-first](/shortest-job-first/) the predicted burst, and [rate-monotonic scheduling](/rate-monotonic-scheduling/) the period. Its main risk is [starvation](/starvation/): a steady stream of high-priority work can keep a low-priority process from ever running, and [aging](/aging/) is the usual cure.

## In plain words

In a hospital emergency room, patients are not seen in the order they came in. The most urgent case goes first. A person with a broken finger waits while people with heart attacks are treated.

This is priority scheduling. Each program gets a number that says how important it is, and the computer always runs the most important program that is ready. In one form, a program keeps the computer until it is done, even when a more important one comes. In the other form, a more important program can take the computer away at once.

The danger is that the person with the broken finger is never seen if urgent patients keep coming. To stop this, many systems raise the importance of a program the longer it waits. This is called aging.

## The problem

The input is $n$ processes on one CPU. Process $i$ arrives at time $a_i \ge 0$, needs one CPU burst of length $b_i > 0$, and has a priority $\pi_i$. Here a smaller number means a higher priority, as in Silberschatz, Galvin and Gagne; some systems, such as Linux for real-time tasks, use the opposite convention. The output is a schedule of [CPU scheduling](/cpu-scheduling/), with or without [preemption](/preemption/), in which the running process has the highest priority among the ready ones: always, in the preemptive form, or at each dispatch, in the nonpreemptive form.

Priorities are *static* if they are fixed when the process is created, and *dynamic* if the system changes them while the process runs or waits. They can be *internal*, computed from measured quantities such as the burst length, memory needs or the ratio of I/O to CPU time, or *external*, set by the user, the administrator or the price paid.

## The algorithm

The ready processes are kept in a [priority queue](/priority-queue/), for example a [binary heap](/binary-heap/), keyed by $(\pi_i, a_i, i)$, so that ties go to the earlier arrival. A process of equal priority does not preempt the running one.

```pseudo id=main
PRIORITY(a, b, π, preemptive)              ▷ arrivals, bursts, priorities; smaller π is higher
L1  P ← the processes in order of a[i], ties by i;  k ← 1;  t ← 0;  H ← an empty min-heap keyed by (π[i], a[i], i)
L2  left[i] ← b[i] for each i
L3  while k ≤ n or H is not empty do
L4      if H is empty and t < a[P[k]] then t ← a[P[k]]          ▷ the CPU is idle
L5      while k ≤ n and a[P[k]] ≤ t do insert P[k] into H;  k ← k + 1
L6      i ← EXTRACT-MIN(H)
L7      if preemptive and k ≤ n then e ← min(t + left[i], a[P[k]]) else e ← t + left[i]
L8      run i on [t, e), joined to the previous slice if that one is also i;  left[i] ← left[i] − (e − t);  t ← e
L9      if left[i] > 0 then insert i into H else C[i] ← t
L10 return C and the slices
```

In the nonpreemptive form, line L7 runs the chosen process to the end of its burst. In the preemptive form, it runs the process only up to the next arrival; at that moment line L5 adds the new process, and line L6 chooses again. If the new process has a lower priority, the same process continues, and line L8 extends its slice. The online form is the same with an arrival handler in place of line L5: in the preemptive form, an arrival of a higher-priority process is decision point 3 of [CPU scheduling](/cpu-scheduling/).

## Example

**All processes at time 0.** This is the example of Silberschatz, Galvin and Gagne, Section 5.3.4.

| process | $P_1$ | $P_2$ | $P_3$ | $P_4$ | $P_5$ |
|---|---|---|---|---|---|
| burst | 10 | 1 | 2 | 1 | 5 |
| priority | 3 | 1 | 4 | 5 | 2 |
| runs | $[6,16)$ | $[0,1)$ | $[16,18)$ | $[18,19)$ | $[1,6)$ |
| waiting | 6 | 0 | 16 | 18 | 1 |

The order is $P_2, P_5, P_1, P_3, P_4$, and the mean waiting time is $41/5 = 8.2$. With all processes present at time 0, the preemptive form gives the same schedule, since no process arrives later.

**Arrivals, with and without preemption.**

| process | A | B | C | D |
|---|---|---|---|---|
| arrival | 0 | 1 | 2 | 4 |
| burst | 6 | 2 | 3 | 1 |
| priority | 3 | 1 | 4 | 2 |

*Nonpreemptive.* A is alone at time 0 and runs on $[0,6)$. At time 6, B, C and D are ready; B has the highest priority and runs on $[6,8)$, then D on $[8,9)$, then C on $[9,12)$. The waiting times are 0, 5, 7 and 4, total 16.

*Preemptive.* A runs on $[0,1)$. B arrives with priority 1 and preempts A: B runs on $[1,3)$. C arrives at 2 with priority 4 and does not preempt. At 3, B finishes, and A, which has a higher priority than C, runs on $[3,4)$. D arrives at 4 with priority 2 and preempts A: D runs on $[4,5)$. Then A runs on $[5,9)$ and C on $[9,12)$. The waiting times are 3, 0, 7 and 0, total 10.

The high-priority processes B and D wait 5 and 4 time units without preemption, and not at all with it. The low-priority process C waits 7 in both.

**Starvation.** Let a process L of priority 9 and burst 3 arrive at time 1, and let processes of priority 1 and burst 2 arrive at times $0, 2, 4, \ldots, 2(K-1)$. At every moment when the CPU becomes free, a priority-1 process is ready, so L first runs at time $2K$, in both forms. As $K$ grows, the wait of L grows without bound. Silberschatz, Galvin and Gagne report a rumor that when the IBM 7094 at MIT was shut down in 1973, a low-priority process submitted in 1967 had still not run.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The loop keeps the invariant that the heap holds exactly the ready processes at the current time $t$. In the nonpreemptive form, each dispatch picks the least key among the processes ready at that moment and runs it to completion. In the preemptive form, a slice ends at the next arrival, and no process arrives inside a slice, so the running process has the least key among the ready processes at every moment. In both forms the CPU is idle only when no process is ready, so the scheduler is [work-conserving](/work-conserving-scheduling/).

## Complexity

Sorting the arrivals takes $O(n \log n)$ time. In the preemptive form, a slice ends either at a completion or at an arrival, so there are at most $2n - 1$ slices; each pass does $O(1)$ heap operations, so the time is $O(n \log n)$ in both forms. The extra space is $\Theta(n)$. Online, each decision costs $O(\log n)$ with a binary heap. With a small fixed number of priority levels, as in most kernels, an array of FIFO queues with a bitmap of nonempty levels gives $O(1)$ per decision.

## Properties

- **Generality.** FCFS, SJF and SRPT are priority scheduling with priority equal to the arrival time, the predicted burst and the remaining time, respectively. So the properties of priority scheduling depend almost fully on how priorities are set.
- **Starvation.** With static priorities and a steady load of high-priority work, a low-priority process can wait without bound, as in the example. This is the [starvation](/starvation/) of process scheduling. [Aging](/aging/) bounds the wait by raising the priority of a waiting process.
- **Preemption and response time.** The preemptive form gives the high-priority processes a response time that does not depend on low-priority work, apart from the time to switch. This is needed for [real-time scheduling](/real-time-scheduling/), where the priorities come from deadlines or periods, as in [fixed-priority scheduling](/fixed-priority-scheduling/).
- **Priority inversion.** When a high-priority process waits for a lock that a low-priority process holds, a medium-priority process can delay both. This is [priority inversion](/priority-inversion/), and the [priority inheritance protocol](/priority-inheritance-protocol/) is one cure.
- **Work conservation.** Both forms are [work-conserving](/work-conserving-scheduling/), so the priorities move waiting time between processes but do not change the busy periods of the CPU.

## Variants and improvements

- **Priority classes with round robin.** Processes of equal priority share the CPU by [round robin](/round-robin/) instead of FCFS. This is how many kernels work, and it is the base of [multilevel queue scheduling](/multilevel-queue-scheduling/).
- **Dynamic priorities.** The priority changes with behavior. Tanenbaum and Bos describe the rule that sets the priority of a process to $1/f$, where $f$ is the fraction of its last quantum that it used, so I/O-bound processes get high priority. The [multilevel feedback queue](/multilevel-feedback-queue/) lowers the priority of a process that uses its full quantum and raises it after a period, which is a form of [aging](/aging/).
- **Aging.** The priority of a waiting process rises with its waiting time, so that it eventually runs; see [aging](/aging/).
- **Proportional share.** Instead of strict priority, the priority sets a share of the CPU: [lottery scheduling](/lottery-scheduling/), [stride scheduling](/stride-scheduling/) and the [completely fair scheduler](/completely-fair-scheduler/), where the nice value sets a weight.

## When to use it

Use priority scheduling when processes differ in importance or urgency, for example interactive work over batch work, or system processes over user processes, and use the preemptive form when high-priority work must respond fast. In real-time systems, preemptive fixed priorities set by [rate-monotonic scheduling](/rate-monotonic-scheduling/) are standard. Avoid plain static priorities when low-priority work must finish in bounded time; add [aging](/aging/) or use a proportional-share scheduler.

## Pitfalls

- **The direction of the numbers.** In some systems a low number is a high priority, in others the opposite. State the convention.
- **Starvation.** Static priorities with a heavy high-priority load starve low-priority work. Test with a long stream of high-priority arrivals, not only with a fixed batch.
- **Equal priorities.** Without a tie rule, the order among equal priorities depends on the heap. Use the arrival time and an index as tie breakers, as here, or round robin.
- **Priority inversion.** Strict priorities interact badly with locks. A schedule that looks right on paper can block a high-priority process behind a low-priority one; see [priority inversion](/priority-inversion/).
- **Preemption costs.** Each preemption costs a context switch. A stream of high-priority processes that each run briefly can cause many switches.

## Implementations

## History

Priorities were part of operating systems from the batch and time-sharing systems of the 1960s, where they came from the price paid, the user class and the measured behavior of a job. The textbooks of Silberschatz, Galvin and Gagne and of Tanenbaum and Bos present priority scheduling as the general case of which FCFS and SJF are special cases, with starvation and aging as its main problem and cure. Fixed priorities in preemptive real-time systems became standard after the analysis of [rate-monotonic scheduling](/rate-monotonic-scheduling/) by Liu and Layland in 1973.

## References
