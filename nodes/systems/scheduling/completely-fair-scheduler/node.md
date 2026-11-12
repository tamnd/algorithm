---
tag: BQCYGA
kind: algorithm
slug: completely-fair-scheduler
name: Completely Fair Scheduler
aliases:
- CFS
area: systems/scheduling
level: advanced
summary: The Linux scheduler from 2.6.23 to 6.6. It runs the task with the smallest weighted virtual runtime, kept in a red-black tree, for a slice of a target latency in proportion to its weight.
solves: [cpu-scheduling]
model: word-ram
complexity:
  vars: {n: the number of runnable tasks, r: the number of scheduling decisions}
  time: {worst: O(r log n)}
  space: {extra: O(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2007
  people: [Ingo Molnar]
  note: Ingo Molnar wrote the Completely Fair Scheduler in 2007, and it became the default Linux scheduler in kernel 2.6.23.
prereqs: [stride-scheduling, red-black-tree, round-robin]
see_also: [lottery-scheduling, multilevel-feedback-queue, priority-scheduling, generalized-processor-sharing, weighted-fair-queueing, virtual-time, binary-heap, scheduling-metrics]
sources:
  - url: https://docs.kernel.org/scheduler/sched-design-CFS.html
    title: Ingo Molnar and the Linux kernel developers, CFS Scheduler, Linux kernel documentation
    locator: Sections 1 to 4 (the ideal multitasking CPU, vruntime, min_vruntime, the time-ordered red-black tree, and the granularity tunable)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 9, Scheduling, Proportional Share, Section 9.7 (sched_latency of 48 ms, min_granularity of 6 ms, the weight table, equations 9.1 and 9.2, the red-black tree, and the placement of waking tasks)
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.7.1 (Linux scheduling, CFS, nice values, target latency and the red-black tree of vruntime values)
---

The Completely Fair Scheduler (CFS) is the [CPU scheduling](/cpu-scheduling/) policy that Linux used for normal tasks from kernel 2.6.23 (2007) until kernel 6.6 (2023). It models an ideal CPU that runs all $n$ runnable tasks at once, each at a rate in proportion to its weight. Each task keeps a *virtual runtime*: its real run time scaled by $1024 / w$, where $w$ is its weight. CFS always runs the task with the smallest virtual runtime, which it finds as the leftmost node of a [red-black tree](/red-black-tree/) keyed by virtual runtime. The task runs for a slice of a *target latency* in proportion to its weight, but never less than a *minimum granularity*. The idea is the pass of [stride scheduling](/stride-scheduling/), measured in real time instead of in quanta.

## In plain words

Imagine a perfect processor that can run all programs at the same time, each at a speed that matches its importance. A real processor runs only one program at a time, so it keeps a score for each program: how much time the program has had, with the time of an important program counted as smaller.

The program with the lowest score has had the least of its fair part, so it runs next. It runs for a short slice of time, and its score goes up. Then the lowest score is found again. A program that slept for a long time does not get to run alone until it catches up; it starts again from about the lowest score of the others.

## The problem

The model is one CPU and a set of tasks. Task $k$ has a weight $w_k \ge 1$, which comes from its nice value, and alternates between CPU bursts and sleeps. While the set $R$ of runnable tasks does not change, the ideal fair schedule gives task $k$ the CPU at rate $w_k / W$, with $W = \sum_{j \in R} w_j$. A real CPU runs one task at a time and pays for each switch. The goal is to stay close to the ideal, with few switches and with a cost of $O(\log n)$ per decision.

## The algorithm

```pseudo id=main
CFS(tasks, latency, min_gran)
L1  t ← 0; min_vr ← 0; Q ← an empty tree ordered by (vruntime, join order)
L2  while some task is not finished do
L3      for each task j that arrives or wakes at a time ≤ t do vr_j ← max(vr_j, min_vr); INSERT(Q, j)
L4      if Q is empty then t ← the next arrival or wake time; continue
L5      j ← EXTRACT-MIN(Q)                       ▷ the leftmost node: the smallest vruntime
L6      n ← |Q| + 1; W ← w_j + the sum of the weights in Q
L7      slice ← max(latency, n · min_gran) · w_j / W
L8      run j for δ ← min(slice, the rest of its burst); t ← t + δ
L9      vr_j ← vr_j + δ · 1024 / w_j
L10     min_vr ← max(min_vr, min(vr_j, the smallest vruntime in Q))
L11     if the burst of j ended then j finishes or sleeps, and leaves the tree; else INSERT(Q, j)
```

Line L7 is the slice rule. Every runnable task should run once in each *period*, which is the target latency, and the period grows to $n \cdot \mathit{min\_gran}$ when there are many tasks, so that no slice is shorter than the minimum granularity. Line L9 is the weighted clock. A task of weight 1024 (nice 0) gains virtual runtime at the rate of real time, and a heavier task gains it more slowly. Each nice step changes the weight by a factor of about 1.25, so that a task that is one nice level lower gets about 10 percent more CPU than its neighbor.

Line L10 keeps $\mathit{min\_vr}$, the smallest virtual runtime, and it never lets it fall. Line L3 places a task that arrives or wakes at $\mathit{min\_vr}$ if it is behind. Without this rule, a task that slept for 10 seconds would come back 10 seconds behind and keep the CPU until it caught up. The kernel uses a refined form of this rule, with a small credit for sleepers and a small debit for new tasks. The kernel also preempts the current task when a waking task has a much smaller virtual runtime; the simulation here runs each slice to its end.

## Example

Two CPU-bound tasks, A with weight 1024 (nice 0) and B with weight 2048, with the OSTEP values $\mathit{latency} = 48$ ms and $\mathit{min\_gran} = 6$ ms. Then $W = 3072$, the period is 48 ms, A's slice is 16 ms and B's slice is 32 ms. Both slices add the same virtual runtime, $16 \cdot 1024 / 1024 = 32 \cdot 1024 / 2048 = 16$.

| real time | runs | vruntime A after | vruntime B after |
|---|---|---|---|
| 0 to 16 | A | 16 | 0 |
| 16 to 48 | B | 16 | 16 |
| 48 to 64 | A | 32 | 16 |
| 64 to 96 | B | 32 | 32 |

At the end of each period of 48 ms, B has had exactly twice the CPU of A. Between the ends of periods, each task is within one of its own slices of its share: A within 16 ms of a third of the elapsed time, and B within 32 ms of two thirds.

With 10 tasks of weight 1024, the latency rule alone would give slices of 4.8 ms. The minimum granularity raises the period to 60 ms, and each slice to 6 ms.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). They cover a fixed set of CPU-bound tasks that start at the same virtual runtime.

1. **Equal virtual steps.** Each slice adds $V = \mathit{period} \cdot 1024 / W$ to the virtual runtime of the task that runs, the same amount for every task.
2. **The virtual runtime invariant.** At the end of each slice, $m \le \mathit{vr}_k \le m + V$ for every task, where $m$ is the smallest virtual runtime. This is the pass invariant of stride scheduling.
3. **Lag bound.** For every task and at the end of every slice, $|\mathit{cpu}_k - t \cdot w_k / W| \le \mathit{slice}_k$, where $t$ is the elapsed time. So no task is ever more than one of its slices ahead of or behind the ideal fair CPU.
4. **Placement.** Every runnable task has a virtual runtime of at least $\mathit{min\_vr}$, and $\mathit{min\_vr}$ never falls. A task that wakes behind is set to $\mathit{min\_vr}$, so it does not carry the lag of its sleep into the tree.

## Complexity

The red-black tree gives INSERT, delete and find-minimum in $O(\log n)$; the kernel caches the leftmost node, so the minimum is $O(1)$. Each decision does a constant number of these operations, so $r$ decisions take $O(r \log n)$ time, and the space is $O(n)$. The sum of the weights is kept as a running total, so line L6 is $O(1)$. The implementation uses a [binary heap](/binary-heap/) with the same bounds in place of the tree, because it needs only INSERT and EXTRACT-MIN; the kernel needs the tree to remove any task in $O(\log n)$ when it sleeps or migrates.

## Properties

- **Weighted fairness with a bounded lag.** Over each period of a fixed set of tasks, the shares are exact; at all times, the lag of each task is at most one slice.
- **No fixed quantum.** The slice depends on the number and weights of the runnable tasks, so a busy CPU switches less often per task than a fixed round robin with the same latency.
- **No heuristics for interactivity.** Earlier Linux schedulers guessed which tasks were interactive. CFS gives a sleeping task no extra priority; it only keeps the task from falling behind by more than the placement rule allows.
- **Deterministic.** The order depends on the virtual runtimes and a tie rule.
- **Short sleepers lose.** A task that sleeps often is placed at $\mathit{min\_vr}$ when it wakes, so it gives up the share it did not use while asleep.

## Variants and improvements

- **Group scheduling.** With control groups, CFS runs one tree per group and treats each group as one entity in the tree of its parent, so CPU is shared first between groups (for example users or containers) and then between the tasks of each group.
- **Multiprocessors.** Each CPU has its own run queue and tree, and a separate load balancer moves tasks between CPUs.
- **EEVDF.** In Linux 6.6 (2023), the Earliest Eligible Virtual Deadline First scheduler of Stoica and Abdel-Wahab replaced CFS; it adds a virtual deadline to each task, so that latency-sensitive tasks with short slices run sooner.
- **Proportional share in general.** CFS is close to [stride scheduling](/stride-scheduling/) in real time and to [weighted fair queueing](/weighted-fair-queueing/) for links; all three approach [generalized processor sharing](/generalized-processor-sharing/).

## When to use it

Use a CFS-style scheduler for general-purpose time sharing with weights: desktops, servers, and containers where each group must get its part of the CPU. It needs no tuning of quanta or queue levels, and its decisions cost $O(\log n)$. It is not a real-time scheduler: it gives no deadline guarantee, and a task with tight latency needs must use a real-time class or a deadline scheduler such as [earliest deadline first](/earliest-deadline-first/).

## Pitfalls

- **A virtual runtime that only grows.** A new task with virtual runtime 0 in a system that has run for hours would take the CPU for hours. Start and wake tasks at $\mathit{min\_vr}$ (line L3).
- **A falling minimum.** If $\mathit{min\_vr}$ is computed as the smallest key in the tree without the max at line L10, it falls when the leftmost task sleeps, and the next waking task is placed too far back.
- **Rounding the weight scale.** The kernel computes $\delta \cdot 1024 / w$ with fixed-point inverse weights. With plain integer division, light tasks gain virtual runtime too slowly or too fast by a rounding error that adds up. Use exact fractions in a simulation.
- **Too small a minimum granularity.** With many tasks, a tiny minimum granularity makes the CPU spend its time on context switches and on cold caches. The period must grow instead, as line L7 does.

## Implementations

## History

Ingo Molnar wrote CFS in 2007, after fair-scheduling work by Con Kolivas, and it replaced the O(1) scheduler as the default Linux scheduler in kernel 2.6.23, released in October 2007. CFS used a red-black tree of virtual runtimes from the start, and group scheduling was added soon after. In 2023, Linux 6.6 replaced CFS with the EEVDF scheduler, based on a 1995 paper by Ion Stoica and Hussein Abdel-Wahab.

## References
