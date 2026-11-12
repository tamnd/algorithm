---
tag: 1E6C07
kind: algorithm
slug: multilevel-feedback-queue
name: Multilevel feedback queue
aliases:
- MLFQ
- multilevel feedback queue scheduling
area: systems/scheduling
level: intro
summary: Several round robin queues in priority order. A new job starts at the top, moves down when it uses up its allotment of CPU time, and all jobs move back to the top at a periodic boost.
solves: [cpu-scheduling]
model: word-ram
complexity:
  vars: {n: the number of jobs, k: the number of queues, T: the number of ticks simulated, S: the boost period in ticks}
  time: {worst: O(k T + n T / S + n log n)}
  space: {extra: O(n + k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1962
  people: [Fernando J. Corbató, Marjorie Merwin-Daggett, Robert C. Daley]
  note: Corbató, Merwin-Daggett and Daley described a multilevel priority scheduler with longer runs at lower levels for the time-sharing system that became CTSS, at the AFIPS Spring Joint Computer Conference of 1962.
prereqs: [multilevel-queue-scheduling, round-robin, priority-scheduling]
see_also: [aging, shortest-job-first, scheduling-metrics, preemption, lottery-scheduling, stride-scheduling, completely-fair-scheduler, cpu-scheduling]
sources:
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 8, Scheduling, The Multi-Level Feedback Queue (Rules 1 to 5, Rules 4a and 4b, the gaming example of Figure 8.5, and the Solaris time-sharing table)
  - paper: "F. J. Corbató, M. Merwin-Daggett and R. C. Daley, An experimental time-sharing system, Proceedings of the AFIPS Spring Joint Computer Conference, volume 21, 1962"
    title: An experimental time-sharing system
    locator: pages 335 to 344 (the multilevel scheduling algorithm, with 2^l quanta at level l and an entry level set by the program size)
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 5, Section 5.3.6 (multilevel feedback queue scheduling and its parameters)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 2, Section 2.4.3 (multiple queues, and the priority classes of CTSS)
---

A multilevel feedback queue (MLFQ) is a [CPU scheduling](/cpu-scheduling/) policy with $k$ [round robin](/round-robin/) queues in strict priority order, in which a job moves between the queues according to how it uses the CPU. A new job starts in the top queue. A job that uses up its allotment of CPU time at a level moves down one level, so long CPU-bound jobs sink and short or interactive jobs stay on top. A periodic boost moves all jobs back to the top, which stops starvation and lets a job that changes its behavior climb back. Unlike [multilevel queue scheduling](/multilevel-queue-scheduling/), the class of a job is learned from its history, not fixed in advance.

## In plain words

The scheduler does not know how long a job will run. So it guesses: each new job is treated as if it were short, and it gets the highest priority. If the job keeps the CPU for a long time, the guess was wrong, and the job moves to a lower queue. Jobs in lower queues run only when the higher queues are empty, but they get longer turns.

Two extra rules make this safe. The first counts all the CPU time a job uses at a level, even when it gives up the CPU many times in short pieces. Without it, a job could give up the CPU just before its turn ends and stay on top forever. The second rule moves every job back to the top from time to time, so a low job cannot wait forever.

## The problem

The model is one CPU and $n$ jobs. Job $j$ arrives at tick $a_j$ and alternates CPU bursts and I/O waits: it runs for some ticks, blocks for some ticks, runs again, and so on. Time goes in integer ticks, and one job runs in each tick. The scheduler is online and non-clairvoyant: it sees a job's CPU use only as it happens, and it does not know the length of the next burst. The parameters are the number of queues $k$, the quantum $q_i$ of queue $i$, the allotment $A_i \ge q_i$ of queue $i$ (the CPU time a job may use at level $i$ before it moves down), and the boost period $S$.

The goal is informal: the response time of short and interactive jobs should be like that of [shortest job first](/shortest-job-first/), which needs the burst lengths, while long jobs still make progress. The [scheduling metrics](/scheduling-metrics/) page defines response time and turnaround time. MLFQ has no optimality guarantee for any of them.

## The algorithm

Arpaci-Dusseau and Arpaci-Dusseau state MLFQ as five rules:

1. If Priority(A) > Priority(B), A runs and B does not.
2. If Priority(A) = Priority(B), A and B run in round robin with the quantum of their queue.
3. When a job enters the system, it is placed in the topmost queue.
4. Once a job uses up its time allotment at a level, regardless of how many times it has given up the CPU, its priority is reduced: it moves down one queue.
5. After some time period $S$, move all the jobs in the system to the topmost queue.

The pseudocode simulates one tick per pass, with queue 0 at the top and $\mathit{lvl}_j$ the level of job $j$.

```pseudo id=main
MLFQ(jobs, q[0 .. k−1], A[0 .. k−1], S)
L1  t ← 0
L2  while some job is not finished do
L3      if S > 0 and t > 0 and t mod S = 0 then move every job to Q[0], with used_j ← 0 and lvl_j ← 0     ▷ Rule 5
L4      append each job whose I/O ends at t to the tail of Q[lvl_j]
L5      append each job with a_j = t to the tail of Q[0]                                             ▷ Rule 3
L6      i ← the smallest index with Q[i] non-empty                                                ▷ Rule 1
L7      if there is no such i then t ← t + 1; continue
L8      j ← the head of Q[i]; run j for one tick; t ← t + 1; used_j ← used_j + 1; slice_j ← slice_j + 1
L9      if used_j = A_i then lvl_j ← min(i + 1, k − 1); used_j ← 0; slice_j ← 0                    ▷ Rule 4
L10     if the CPU burst of j ends then remove j from Q[i]; slice_j ← 0; j finishes or blocks for I/O
L11     else if lvl_j changed at L9 or slice_j = q_i then slice_j ← 0; move j from Q[i] to the tail of Q[lvl_j]   ▷ Rule 2
```

The counter $\mathit{used}_j$ is the CPU time that $j$ has used at its current level. Line L10 does not reset it when the job blocks. This is the accounting fix of Rule 4. The first version of the rules had two rules in its place:

- Rule 4a: if a job uses up its allotment while running, it moves down one queue.
- Rule 4b: if a job gives up the CPU before its allotment is up, it stays at the same level, and its allotment is reset.

Rule 4b is the same as adding $\mathit{used}_j \leftarrow 0$ to line L10 when $j$ blocks. A job can then *game* the scheduler: it runs for a little less than its allotment, does a short I/O, and comes back to the same level with a fresh allotment. The example below shows this.

The order of events in a tick is: the boost, then the I/O completions, then the arrivals, then one tick of CPU.

## Example

**A normal workload.** Two queues: $q_0 = 2$, $A_0 = 4$ and $q_1 = 4$, $A_1 = 8$, with no boost. Job A arrives at tick 0 and needs 12 ticks of CPU. Job B arrives at tick 1 and is interactive: 1 tick of CPU, 3 ticks of I/O, 1 tick of CPU, 3 ticks of I/O, 1 tick of CPU. Job C arrives at tick 5 and needs 3 ticks. The timeline is `AABAACCBCAABAAAAAA`.

| ticks | runs | what happens |
|---|---|---|
| 0 to 1 | A | quantum of 2 ends; A goes behind B in $Q_0$ |
| 2 | B | B blocks for I/O until tick 6 |
| 3 to 4 | A | A has used 4 ticks at level 0, so it moves to $Q_1$ |
| 5 to 6 | C | C arrives in $Q_0$; at tick 6 B returns behind C; C's quantum ends |
| 7 | B | B blocks until tick 11 |
| 8 | C | C ends at 9 |
| 9 to 10 | A | $Q_0$ is empty, so $Q_1$ runs |
| 11 | B | B returns and preempts A; B ends at 12 |
| 12 to 17 | A | A ends at 18 |

B and C each use only 3 ticks in total, less than $A_0 = 4$, so they stay in $Q_0$ and get the CPU soon after they become ready. A moves down after 4 ticks and then runs only when $Q_0$ is empty.

**A gaming job.** Three queues, each with quantum and allotment 10, no boost. Job L needs 60 ticks of CPU. Job G repeats "9 ticks of CPU, then 1 tick of I/O" 12 times and then runs 9 more ticks. Both arrive at tick 0, L first.

- Under Rules 4a and 4b, the timeline starts `LLLLLLLLLL` and then repeats `GGGGGGGGGL`. G never uses a full allotment in one piece, so it stays in $Q_0$ for its whole life, and it gets 81 of the first 100 ticks. L, which has moved down, gets only the ticks in which G does I/O.
- Under Rule 4, G uses 9 ticks, blocks, returns, and moves down after its tenth tick at level 0, at tick 20. It reaches the bottom queue at tick 49, and it gets 40 of the first 100 ticks. L ends at tick 96 and G at tick 185.

## Correctness

MLFQ enforces rules rather than an optimum, so correctness means that the simulation meets Rules 1 to 5, and that Rules 4 and 5 give two guarantees. The proofs are in [proofs/correctness.md](proofs/correctness.md).

- **Rule 1.** The job that runs in a tick has the smallest level among the ready jobs, because line L6 takes the highest non-empty queue and a ready job is always in the queue of its level.
- **The accounting bound.** Between two boosts, a job that has used $u$ ticks of CPU in total is at level $\ell(u) = \min\{k - 1, \max\{\ell : A_0 + \cdots + A_{\ell - 1} \le u\}\}$, whatever its pattern of I/O. So no job, gaming or not, gets more than $A_0 + \cdots + A_{\ell - 1}$ ticks above level $\ell$ in one boost period.
- **The boost bound.** If at most $n$ jobs are in the system, a job that is ready at a boost and stays ready runs within $(n - 1) q_0$ ticks after that boost, when $(n - 1) q_0 < S$.

The invariant behind the accounting bound is that $\mathit{used}_j$ equals the CPU time of $j$ since it reached its current level, which line L10 keeps because it never resets the counter.

## Complexity

Line L6 scans at most $k$ queues, and lines L8 to L11 take $O(1)$ with double-ended queues. A boost at line L3 touches each of the $n$ jobs, and there are at most $T / S$ boosts. I/O completions and arrivals are handled once each, after the arrivals are sorted. So the simulation takes $O(kT + nT/S + n \log n)$ time in the worst case and $O(n + k)$ extra space. A kernel uses a bit mask of the non-empty queues instead of the scan, and runs the scheduler only at events, not at each tick.

## Properties

- **Online and non-clairvoyant.** It needs no estimate of the burst lengths; it learns them from the CPU use.
- **Favors short bursts.** A job whose total CPU use stays below $A_0$ is never below level 0, so it is never behind a job of a lower level.
- **Not strategy-proof without Rule 4.** Under Rules 4a and 4b, a job that blocks just before its allotment ends keeps the top priority forever.
- **Starvation without Rule 5.** A steady stream of new jobs keeps $Q_0$ non-empty, and the lower queues then never run.
- **Many parameters.** The number of queues, the quanta, the allotments and $S$ change the behavior a lot, and no setting is best for all workloads.

## Variants and improvements

- **Longer quanta at lower levels.** Lower queues hold CPU-bound jobs, so they get longer quanta: fewer context switches and the same response time for the top queues. CTSS gave $2^\ell$ quanta at level $\ell$. The Solaris time-sharing class, as described in OSTEP, has 60 queues with slices from 20 milliseconds at the top to a few hundred milliseconds at the bottom, and boosts about every second.
- **Priority by decay.** FreeBSD and older Unix systems compute a priority from the recent CPU use, decayed over time, instead of fixed demotion steps. The effect is the same: heavy CPU use lowers the priority, and waiting raises it.
- **Boost by aging.** Instead of a global boost, raise each job that has waited for a long time; see [aging](/aging/).
- **Proportional share.** [Lottery](/lottery-scheduling/), [stride](/stride-scheduling/) and the [Completely Fair Scheduler](/completely-fair-scheduler/) drop the levels and give each job a share of the CPU in proportion to a weight.

## When to use it

Use MLFQ for a general-purpose, interactive system where the burst lengths are not known and short jobs should get a fast response. It approximates [shortest job first](/shortest-job-first/) without the burst lengths. Use [multilevel queue scheduling](/multilevel-queue-scheduling/) when the classes are known and fixed. Use a proportional-share scheduler when the goal is a guaranteed fraction of the CPU for each job or user, rather than fast response for short bursts.

## Pitfalls

- **Resetting the allotment on I/O.** Writing $\mathit{used}_j \leftarrow 0$ at line L10 when the job blocks is Rule 4b, and it lets a job game the scheduler, as the example shows. Keep the counter until the job moves down (line L9) or the boost (line L3).
- **No boost.** Leaving out line L3 lets a stream of short jobs starve the lower queues forever. Choose $S$ larger than the time the top queue needs for one turn of each job, and small enough for the longest wait that the system accepts.
- **Demotion only at the end of a quantum.** If line L9 checks the allotment only when a quantum ends, a job that blocks one tick before each quantum end is never checked. Check the allotment after every tick of CPU, as line L9 does.
- **A blocked job with a stale level.** A job that is blocked at a boost must also get $\mathit{lvl}_j \leftarrow 0$, or it returns at line L4 to its old low queue.

## Implementations

## History

Corbató, Merwin-Daggett and Daley described the scheduler of their experimental time-sharing system, which became CTSS, in 1962. A program at level $\ell$ ran for up to $2^\ell$ quanta; if it did not finish or respond to its user, it went to the end of the queue at level $\ell + 1$. The entry level depended on the size of the program, so that the run time at a level was at least the time to swap the program in and out. Arpaci-Dusseau and Arpaci-Dusseau cite this paper as the first description of the multilevel feedback queue, and give the modern form with Rules 1 to 5 and the anti-gaming rule. Corbató received the Turing Award in 1990.

## References
