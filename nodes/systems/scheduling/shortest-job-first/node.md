---
tag: GK26MR
kind: algorithm
slug: shortest-job-first
name: Shortest-job-first scheduling
aliases:
- shortest job next
- SJF
- shortest-next-CPU-burst scheduling
- shortest process next
area: systems/scheduling
level: intro
summary: "When the CPU is free, run the ready process with the shortest predicted next CPU burst to its end; the prediction is an exponential average of the past bursts."
solves: [cpu-scheduling]
model: real-ram
complexity:
  vars: {n: the number of processes}
  time: {worst: O(n log n)}
  space: {extra: O(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1956
  people: [Wayne E. Smith]
  note: Smith proved in 1956 that the shortest-first order minimizes the mean completion time of jobs that are all present at the start; the operating-system form adds burst prediction.
prereqs: [cpu-scheduling, fcfs-scheduling, exponential-moving-average, priority-queue]
see_also: [sjf-optimality, srpt, shortest-processing-time-first, fcfs-scheduling, round-robin, priority-scheduling, aging, multilevel-feedback-queue]
sources:
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.3.2 (shortest-job-first scheduling, the example with bursts 6, 8, 7 and 3, and the exponential average with alpha 1/2 and tau_0 = 10)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 2, Section 2.4.2 (shortest job first) and Section 2.4.3 (shortest process next, and the estimate that the book calls aging)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces, version 1.10
    locator: Chapter 7, Section 7.4 (shortest job first) and Section 7.5 (the effect of late arrivals and the preemptive version)
  - paper: doi:10.1002/nav.3800030106
    title: Wayne E. Smith, Various optimizers for single-stage production, Naval Research Logistics Quarterly 3(1 to 2), 1956
    locator: pages 59 to 66 (the shortest-first order for jobs all present at the start)
---

Shortest-job-first (SJF) scheduling is the [CPU scheduling](/cpu-scheduling/) policy that, each time the CPU becomes free, runs the ready process whose next CPU burst is predicted to be shortest, and lets it run to the end of that burst. With exact burst lengths and all processes present at once, it gives the least mean waiting time of all schedules ([optimality of SJF](/sjf-optimality/)). A real scheduler does not know the next burst, so it predicts it by an [exponential average](/exponential-moving-average/) of the past bursts, $\tau_{n+1} = \alpha t_n + (1 - \alpha)\tau_n$. This page is the nonpreemptive operating-system policy; the offline rule for $1 \mid\mid \sum C_j$ is [shortest processing time first](/shortest-processing-time-first/), and the preemptive version is [SRPT](/srpt/).

## In plain words

At a supermarket with one till, suppose the cashier could choose who comes next. If one customer has a full cart and three others have one item each, the cashier should take the one-item customers first. They leave quickly, and the full cart waits only a few extra seconds. The average wait drops a lot.

SJF does this with programs. When the processor is free, it picks the program that will need the processor for the shortest time before it stops to wait for something. That program then runs until it stops.

There is a catch: the computer cannot see the future. So it guesses each program's next run from its recent runs. A program that ran briefly the last few times will probably run briefly again. A second catch: a long program can wait forever if short ones keep coming.

## The problem

The input is $n$ processes on one CPU. Process $i$ arrives at time $a_i$ and needs a CPU burst of length $b_i > 0$; the scheduler sees only a prediction $\tau_i$ of $b_i$. The output is a start time $S_i$ and a completion time $C_i = S_i + b_i$ for each process, with no preemption. The goal is a small mean waiting time $\frac1n \sum_i (S_i - a_i)$; see [scheduling metrics](/scheduling-metrics/).

## The algorithm

The main block is the scheduler. The keys go into a min-[priority queue](/priority-queue/), here a [binary heap](/binary-heap/).

```pseudo id=main
SJF(a, b, τ)                         ▷ arrival a[i], burst b[i], predicted burst τ[i]
L1  Q ← processes by (a[i], i);  H ← empty min-heap;  t ← 0;  k ← 1
L2  while k ≤ n or H is not empty do
L3      if H is empty and t < a[Q[k]] then t ← a[Q[k]]   ▷ idle until the next arrival
L4      while k ≤ n and a[Q[k]] ≤ t do
L5          insert Q[k] into H with key (τ[Q[k]], a[Q[k]], Q[k]);  k ← k + 1
L6      i ← EXTRACT-MIN(H)                ▷ least predicted burst, then earliest arrival
L7      S[i] ← t;  t ← t + b[i];  C[i] ← t   ▷ run to the end of the actual burst
L8  return S, C
```

The prediction of the next burst of a process comes from its past bursts $t_0, t_1, \ldots$ and an initial guess $\tau_0$:

```pseudo id=predict
PREDICT(t[0..m−1], α, τ0)           ▷ 0 ≤ α ≤ 1
P1  for n ← 0 to m − 1 do τ[n + 1] ← α · t[n] + (1 − α) · τ[n]
P2  return τ[m]                       ▷ the prediction of burst m
```

Line L3 is the only idle step, and only when no arrived process waits. Lines L4 and L5 admit every process that has arrived by $t$. Line L6 makes the choice: the key orders by predicted burst, and ties go to the earlier arrival, which is FCFS among equals. Line L7 runs the chosen process for its actual burst $b_i$, which may differ from $\tau_i$; when the burst ends, the kernel feeds $b_i$ into PREDICT for the next burst of that process.

Unrolled, the prediction is $\tau_{n+1} = \alpha t_n + (1-\alpha)\alpha t_{n-1} + \cdots + (1-\alpha)^j \alpha t_{n-j} + \cdots + (1-\alpha)^{n+1} \tau_0$. Each older burst has a weight $1 - \alpha$ times smaller. With $\alpha = 0$ the history is ignored; with $\alpha = 1$ only the last burst counts. Silberschatz uses $\alpha = 1/2$.

## Example

**All present at time 0** (Silberschatz, Section 5.3.2). Bursts P1 6, P2 8, P3 7, P4 3. SJF runs P4, P1, P3, P2 on $[0,3)$, $[3,9)$, $[9,16)$, $[16,24)$. The waiting times are P1 3, P2 16, P3 9, P4 0, a mean of 7. FCFS in the order P1 to P4 gives a mean of 10.25.

**With arrivals.** Six processes with exact predictions, $\tau_i = b_i$:

| process | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| arrival | 0 | 2 | 4 | 5 | 6 | 20 |
| burst | 7 | 4 | 1 | 4 | 2 | 3 |

| step | $t$ | heap after L4 and L5 (burst) | chosen | runs on | waiting |
|---|---|---|---|---|---|
| 1 | 0 | A(7) | A | $[0, 7)$ | 0 |
| 2 | 7 | B(4), C(1), D(4), E(2) | C | $[7, 8)$ | 3 |
| 3 | 8 | B(4), D(4), E(2) | E | $[8, 10)$ | 2 |
| 4 | 10 | B(4), D(4) | B, the earlier arrival | $[10, 14)$ | 8 |
| 5 | 14 | D(4) | D | $[14, 18)$ | 9 |
| 6 | 18, then 20 by L3 | F(3) | F | $[20, 23)$ | 0 |

The total waiting time is 22, a mean of $11/3 \approx 3.67$. FCFS on the same input waits 0, 5, 7, 7, 10 and 0, a mean of $29/6 \approx 4.83$. A runs first although it is the longest: it was alone when the CPU became free, and SJF does not preempt.

**The prediction** (Silberschatz, Section 5.3.2). With $\alpha = 1/2$, $\tau_0 = 10$ and measured bursts 6, 4, 6, 4, 13, 13, 13, the predictions are 10, 8, 6, 6, 5, 9, 11, 12. When the bursts jump from 4 to 13, the prediction follows in three steps: 9, 11, 12.

## Correctness

The claim is that SJF returns a nonpreemptive, work-conserving schedule in which each dispatched process has the least key $(\tau_i, a_i, i)$ among the processes that have arrived and not started. The invariant of the loop of line L2 is that $H$ holds exactly the processes that have arrived by $t$ and not started, and that $t$ is the end of the last interval. The proof file gives the full argument and the closed form of the exponential average. Whether the schedule is *optimal* is a separate question, answered on [optimality of SJF](/sjf-optimality/).

## Complexity

- **Time.** The sort in line L1 takes $O(n \log n)$. Each process enters and leaves the heap once, at $O(\log n)$ each. So the worst case is $O(n \log n)$, and each scheduling decision costs $O(\log n)$.
- **Space.** $O(n)$ for $Q$, $H$, $S$ and $C$.
- **Prediction.** $O(1)$ time and one stored number per process.
- **Dispatches.** Exactly one per burst, as for FCFS.

## Properties

- **Nonpreemptive.** Once a burst starts it runs to the end, even if a shorter one arrives.
- **Work-conserving.** So its utilization and busy periods equal those of FCFS on the same trace ([work-conserving scheduling](/work-conserving-scheduling/)).
- **Optimal only with all present.** With exact bursts and all processes present at time 0, SJF minimizes the mean waiting time. With arrivals it is not optimal even among nonpreemptive schedules ([optimality of SJF](/sjf-optimality/)).
- **Starvation.** A long process waits as long as shorter ones keep arriving. In the test of this page, a burst of 5 that arrives at time 1 among short bursts of 2 that arrive at 0, 2, 4, ..., 98 starts only at 100.
- **A special case of priority scheduling** with the priority equal to the predicted burst ([priority scheduling](/priority-scheduling/)).

## Variants and improvements

- **Preemptive SJF.** When a new process arrives with a shorter burst than what is left of the running one, preempt. This is [SRPT](/srpt/), which is optimal for the total turnaround time with arrivals ([Schrage's theorem](/srpt-optimality/)).
- **Highest response ratio next.** Choose by the ratio $(w + \tau)/\tau$ of waiting time plus predicted burst to predicted burst. A process that waits long gets a high ratio, so it cannot starve. This is [aging](/aging/) built into the key.
- **Long-term SJF.** Batch systems use the time limit that the user gives with the job as its length, and the user has a reason to give a tight limit.
- **Learning without a prediction.** The [multilevel feedback queue](/multilevel-feedback-queue/) approximates SJF without any burst prediction: a process that uses its whole quantum moves to a lower level.

## When to use it

Use SJF when the mean waiting time is the goal, the bursts can be predicted well, and preemption is not available or too costly, for example for the batch jobs of a cluster with user time limits. In a general-purpose kernel prefer a preemptive policy: SJF cannot stop a long burst that started just before a short one arrived. If the long jobs must finish, add [aging](/aging/) or use the response ratio.

## Pitfalls

- **Treating the prediction as the truth.** Line L6 orders by $\tau$, but line L7 runs for $b$. With the same six processes and the wrong predictions C 6 and D 1, SJF runs D before C and E and the mean waiting time becomes $31/6 \approx 5.17$, worse than FCFS. Keep $\alpha$ large enough that the prediction follows a change.
- **Calling it optimal with arrivals.** For a burst of 10 at time 0 and a burst of 1 at time 1, SJF waits $0 + 9$; idling for one unit and running the short burst first waits $2 + 0$. The optimality theorem needs all processes present at time 0.
- **Ties without a rule.** Keys $(\tau_i)$ alone leave equal predictions in heap order, which is not FCFS. Add the arrival time and the index to the key, as in line L5.
- **Confusing it with SRPT.** SJF never preempts. The page [SRPT](/srpt/) covers the preemptive rule.

## Implementations

## History

Smith (1956) proved that for jobs all present at the start, the order of increasing processing time minimizes the mean completion time; this is the theory behind SJF. The operating-systems form, with a prediction of the next CPU burst by an exponential average, is the one in the textbooks (Silberschatz, Galvin and Gagne, Section 5.3.2). Tanenbaum and Bos call the same estimate "aging" and the interactive policy "shortest process next", which is not the [aging](/aging/) that prevents starvation.

## References
