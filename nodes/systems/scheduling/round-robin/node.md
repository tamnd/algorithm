---
tag: EHJG6W
kind: algorithm
slug: round-robin
name: Round-robin scheduling
aliases:
- RR
- round-robin CPU scheduling
- time slicing
area: systems/scheduling
level: intro
summary: "Give the ready processes the CPU in FIFO turn, each for at most one time quantum q. A small q gives fast response but more switches; a q larger than every burst gives FCFS."
solves: [cpu-scheduling]
model: real-ram
complexity:
  vars: {n: the number of processes, m: "the number of slices, at most the sum over i of the burst of i divided by q and rounded up"}
  time: {worst: O(n log n + m)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [cpu-scheduling, fcfs-scheduling, preemption, queue]
see_also: [generalized-processor-sharing, deficit-round-robin, multilevel-feedback-queue, completely-fair-scheduler, round-robin-load-balancing, shortest-job-first, scheduling-metrics, work-conserving-scheduling]
sources:
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.3.3 (round-robin scheduling, the example with bursts 24, 3 and 3 and q = 4, the (n - 1) q bound, the quantum and context switches, and the rule that about 80 percent of CPU bursts should be shorter than q)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces, version 1.10
    locator: Chapter 7, Section 7.7 (round robin, response time, and amortizing the cost of a context switch)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 2, Section 2.4.3 (round-robin scheduling, the length of the quantum against the switch time)
  - paper: "Leonard Kleinrock, Time-shared systems: a theoretical treatment, Journal of the ACM 14(2), 1967"
    locator: pages 242 to 261 (round robin and its processor-sharing limit as the quantum goes to zero)
---

Round-robin (RR) scheduling gives the CPU to the ready processes in turn, each for at most a fixed time quantum $q$. When the quantum ends and the process still needs the CPU, the process is [preempted](/preemption/) and goes to the tail of the ready queue. RR is [FCFS](/fcfs-scheduling/) with a timer: its ready queue is a FIFO [queue](/queue/), each decision takes $O(1)$ time, and it does not need to know the bursts. It is the basic policy for time-sharing, because no ready process waits more than $(n - 1)q$ for its next turn when $n$ processes share the CPU. The choice of $q$ is the whole design: a large $q$ makes RR into FCFS, and as $q$ goes to 0, RR approaches processor sharing, where each of the $n$ processes runs at speed $1/n$.

## In plain words

Think of one cook and a row of pots. The cook stirs the first pot for one minute, then moves to the next pot, and so on, and then comes back to the start. A pot that is done leaves the row. A new pot goes at the end of the row.

No pot waits long for the cook: with five pots on the stove and one minute each, a pot waits at most four minutes for its next stir. But each move from pot to pot also takes a little time. If the cook moves every few seconds, much of the time goes into moving. If the cook stays a long time with each pot, the other pots wait long, and the method becomes "first come, first served."

## The problem

The input is $n$ processes on one CPU. Process $i$ arrives at time $a_i \ge 0$ and needs one CPU burst of length $b_i > 0$. The output is a [preemptive](/preemption/) schedule: a list of slices, each a process and a time interval, such that the slices do not overlap, process $i$ runs only after $a_i$, and its slices add up to $b_i$. Process $i$ completes at the end of its last slice, $C_i$. This is the single-burst form of [CPU scheduling](/cpu-scheduling/). RR does not use the $b_i$ to make its choices. Its aim is a short [response time](/scheduling-metrics/), the time from arrival to the first run, and an even share of the CPU, not the least mean waiting time.

## The algorithm

The parameters are the quantum $q > 0$ and the dispatch cost $s \ge 0$, the time that a context switch takes. A process that arrives at the moment when a quantum ends joins the queue before the preempted process. A process whose quantum ends while the queue is empty keeps the CPU, with no switch.

```pseudo id=main
ROUND-ROBIN(a, b, q, s)                   ▷ arrivals a[1..n], bursts b[1..n]
L1  P ← the processes in order of a[i], ties by i;  k ← 1;  t ← 0;  R ← an empty FIFO queue;  last ← none
L2  left[i] ← b[i] for each i
L3  while k ≤ n or R is not empty do
L4      if R is empty and t < a[P[k]] then t ← a[P[k]]          ▷ the CPU is idle
L5      ADMIT(t)                                ▷ append P[k], P[k+1], ... while a[P[k]] ≤ t
L6      i ← the head of R, removed
L7      if i ≠ last then t ← t + s               ▷ context switch to i
L8      d ← min(q, left[i]);  record the slice (i, t, t + d)
L9      t ← t + d;  left[i] ← left[i] − d;  last ← i
L10     ADMIT(t)                                ▷ arrivals during the slice go first
L11     if left[i] > 0 then append i to R else C[i] ← t
L12 return C and the slices
```

Lines L1 and L2 order the arrivals. The loop runs one slice per pass. Line L4 skips idle time, which happens only when no process is ready. Line L7 charges the switch, line L8 runs the process for one quantum or less, and line L11 sends it back to the tail of the queue if it has work left. The online form is the same: a timer interrupt ends the quantum (decision point 2 of [CPU scheduling](/cpu-scheduling/)), and the [dispatcher](/cpu-scheduling/) takes the head of the queue.

## Example

**The textbook example.** Three processes arrive at time 0 with bursts 24, 3 and 3, in the order $P_1, P_2, P_3$, and $q = 4$, $s = 0$ (Silberschatz, Galvin and Gagne, Section 5.3.3).

| slice | $[0,4)$ | $[4,7)$ | $[7,10)$ | $[10,30)$ |
|---|---|---|---|---|
| process | $P_1$ | $P_2$ | $P_3$ | $P_1$ |

$P_2$ and $P_3$ finish in their first quantum. After time 10, $P_1$ is alone, so it keeps the CPU through five more quanta with no switch. The waiting times are 6, 4 and 7, with mean $17/3 \approx 5.67$. FCFS in the same order has mean waiting time 17, and [shortest-job-first](/shortest-job-first/) has 3.

**A hand-worked example with arrivals.** Take $q = 2$, $s = 0$ and five processes.

| process | A | B | C | D | E |
|---|---|---|---|---|---|
| arrival | 0 | 1 | 2 | 3 | 6 |
| burst | 5 | 3 | 1 | 2 | 4 |

Each row below is one pass of the loop. The queue is shown after line L11, head first.

| slice | runs | arrivals admitted | queue after the slice |
|---|---|---|---|
| $[0,2)$ | A, 3 left | B, C | B, C, A |
| $[2,4)$ | B, 1 left | D | C, A, D, B |
| $[4,5)$ | C, done | | A, D, B |
| $[5,7)$ | A, 1 left | E | D, B, E, A |
| $[7,9)$ | D, done | | B, E, A |
| $[9,10)$ | B, done | | E, A |
| $[10,12)$ | E, 2 left | | A, E |
| $[12,13)$ | A, done | | E |
| $[13,15)$ | E, done | | |

| process | A | B | C | D | E | mean |
|---|---|---|---|---|---|---|
| completion | 13 | 10 | 5 | 9 | 15 | |
| waiting | 8 | 6 | 2 | 4 | 5 | 5 |
| response | 0 | 1 | 2 | 4 | 4 | 2.2 |

FCFS on the same input runs A, B, C, D, E to completion and gets completions 5, 8, 9, 11 and 15, mean waiting time 4.2 and mean response time 4.2, since under FCFS each process waits only before it starts. So RR improves the mean response time from 4.2 to 2.2 but makes the mean waiting time worse, from 4.2 to 5. This is the usual trade.

When A goes back to the queue at time 2, two processes are ahead of it, so Claim 2 of the proof gives a next start by $2 + 2q = 6$; A starts at 5. At time 7, three are ahead (D, B, E), so the bound is $7 + 3q = 13$; A starts at 12.

**Turnaround is not monotone in $q$.** For four processes at time 0 with bursts 6, 3, 1 and 7, the mean turnaround time is:

| $q$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| mean turnaround | 11 | 11.5 | 10.75 | 11.5 | 12.25 | 10.5 | 10.5 |

From $q = 6$ on, RR is FCFS for this input. This is the example of Silberschatz, Galvin and Gagne, Section 5.3.3.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows three facts.

1. The slices form a valid preemptive schedule in which each process gets exactly its burst, and the CPU is idle only when no unfinished process has arrived, so RR is [work-conserving](/work-conserving-scheduling/).
2. **The wait between turns.** A process that joins the queue with $m - 1$ processes ahead of it starts its next slice within $(m - 1)(q + s) + s$. So with $n$ processes present and $s = 0$, no process waits more than $(n - 1)q$ for its first slice or between two slices. Processes that arrive later join behind it, so they cannot delay it.
3. **The limits.** If $q \ge \max_i b_i$, RR is FCFS. If all processes arrive at time 0 and $s = 0$, the completion time of each process differs from its completion time under processor sharing by less than $(n - 1)q$, so RR tends to processor sharing as $q \to 0$.

Under processor sharing with all processes present at time 0, the bursts sorted as $b_{(1)} \le \cdots \le b_{(n)}$, the $k$-th finishes at $C_{(k)} = b_{(1)} + \cdots + b_{(k-1)} + (n - k + 1) b_{(k)}$, which is $\sum_i \min(b_i, b_{(k)})$. For bursts 6, 3, 1 and 7 this gives 16, 10, 4 and 17. With $q = 1/m$, RR gives $16 - q$, $10 - q$, $4 - q$ and $17$, which tends to these values.

## Complexity

Each slice takes $O(1)$ time apart from admissions, and each process is admitted once. Process $i$ gets at most $\lceil b_i / q \rceil$ slices, so the number of slices is $m \le \sum_i \lceil b_i / q \rceil$, and the offline form takes $O(n \log n + m)$ time, where the $n \log n$ is the sort of the arrivals. The online scheduler takes $O(1)$ per decision. The extra space is $\Theta(n)$ for the queue.

The real cost is in the switches. If every slice is a full quantum and each one ends in a switch of cost $s$, then the fraction of CPU time spent on switching is

$$\frac{s}{q + s}.$$

With $q = 10$ ms and $s = 0.1$ ms this is about 1 percent; with $q = 1$ ms it is about 9 percent. A smaller quantum also means more cache and TLB misses after each switch, which this formula does not count.

## Properties

- **Preemptive, online and nonclairvoyant.** RR uses only the arrival order and a timer. It never needs a burst length or a prediction.
- **Bounded wait, no starvation.** By Claim 2, every ready process gets the CPU within $(n - 1)(q + s) + s$, so no process can starve.
- **Fair share over long times.** Over any interval in which the same $k$ processes stay ready and use full quanta, each one gets the same CPU time to within one quantum. Weighted forms of this idea are [generalized processor sharing](/generalized-processor-sharing/) and its packet versions.
- **Mean waiting time is often worse than FCFS** when the bursts are about equal: $n$ processes with burst $b$ and $q$ dividing $b$ all finish near the end, at about $nb$, whereas FCFS finishes them at $b, 2b, \ldots, nb$.
- **The value of $q$.** As $q$ grows, RR becomes FCFS. As $q$ shrinks, response time improves and RR approaches processor sharing, but the switch overhead $s/(q + s)$ grows. Silberschatz, Galvin and Gagne give the rule that about 80 percent of the CPU bursts should be shorter than $q$, and quote typical quanta of 10 to 100 ms against switch times of less than 10 microseconds.

## Variants and improvements

- **Virtual round robin** keeps a second queue for processes that come back from I/O before they used up their quantum, and serves it first, so that I/O-bound processes are not hurt by the plain queue.
- **Weighted round robin** gives process $i$ a quantum $w_i q$, which gives CPU shares in proportion to $w_i$. [Deficit round robin](/deficit-round-robin/) is the packet version, where the quantum is a number of bytes and the deficit carries over.
- **Multilevel feedback queues** use RR at each level with a larger quantum at lower levels; see [multilevel feedback queue](/multilevel-feedback-queue/).
- **Proportional share** schedulers such as [stride scheduling](/stride-scheduling/) and the [completely fair scheduler](/completely-fair-scheduler/) approximate weighted processor sharing more closely than fixed quanta do.
- **Round robin in other settings.** The same turn-taking is used to assign requests to servers, [round-robin load balancing](/round-robin-load-balancing/), and to serve packet queues in [fair queueing](/fair-queueing/).

## When to use it

Use RR when processes are interactive or their bursts are unknown, and a short response time and a bounded wait matter more than the least mean waiting time. It is the basic policy of time-sharing systems and the policy at each level of many multilevel schedulers. Do not use plain RR when bursts are known and the mean waiting time is the aim, for example in a batch of jobs: there [shortest-job-first](/shortest-job-first/) is optimal ([optimality of SJF](/sjf-optimality/)), and for arrivals with preemption, [SRPT](/srpt/) is.

## Pitfalls

- **A quantum that is too small.** The switch cost $s/(q+s)$ and the loss of cache contents can take a large part of the CPU. A quantum close to $s$ wastes about half of it.
- **A quantum that is too large.** RR becomes FCFS, with its [convoy effect](/fcfs-scheduling/), and interactive processes wait behind CPU-bound ones.
- **The order at the end of a quantum.** Whether a new arrival goes before or after the preempted process changes the schedule. The convention here, as in Silberschatz, Galvin and Gagne, puts the arrival first. State the convention when you compare results.
- **Counting the switch when a process is alone.** If the queue is empty at the end of a quantum, the process continues. A simulator that charges a switch here overstates the overhead.
- **I/O-bound processes lose their share.** A process that blocks before its quantum ends gives up the rest of the quantum, so CPU-bound processes get more CPU time than an even share. Virtual round robin and the [multilevel feedback queue](/multilevel-feedback-queue/) address this.

## Implementations

## History

Time-sharing systems of the early 1960s gave each user a short slice of the processor in turn, and round robin became the standard policy for this. Kleinrock analyzed round robin in queueing models in the 1960s, and in his 1967 paper he treated the limit in which the quantum goes to zero, which is processor sharing. Today RR is taught in all operating-systems textbooks as the base preemptive policy, and it is the inner policy of the [multilevel feedback queue](/multilevel-feedback-queue/).

## References
