---
tag: 1YRN1P
kind: algorithm
slug: srpt
name: Shortest remaining processing time
aliases:
- SRPT
- SRTF
- Shortest-remaining-time-first
- preemptive SJF
- shortest remaining time first
area: online-and-streaming/online-scheduling
level: core
summary: Preemptively run the job with the least remaining work; optimal for total flow time on one machine.
solves: [online-flow-time-minimization]
model: real-ram
complexity:
  vars: {n: the number of jobs}
  time: {worst: O(n log n)}
  space: {extra: O(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1968
  people: [Linus Schrage]
  note: Schrage proved in 1968 that SRPT minimizes the total flow time on one machine with preemption.
prereqs: [flow-time, preemptive-scheduling, release-time, online-algorithm]
see_also: [srpt-optimality, flow-time-minimization, shortest-job-first, shortest-processing-time-first, non-clairvoyant-flow-time-minimization, stretch, online-total-completion-time, identical-machines]
sources:
  - paper: "Linus Schrage, A proof of the optimality of the shortest remaining processing time discipline, Operations Research 16(3), 1968"
    locator: pages 687 to 690 (SRPT minimizes the mean flow time on one machine with preemption)
  - paper: "Stefano Leonardi and Danny Raz, Approximating total flow time on parallel machines, Journal of Computer and System Sciences 73(6), 2007 (STOC 1997)"
    locator: pages 875 to 891 (SRPT on m machines is O(log min(n/m, P))-competitive, and the online lower bounds)
  - book: isbn:9781584883975
    title: Joseph Y-T. Leung (ed.), Handbook of Scheduling, Algorithms, Models, and Performance Analysis, Chapman and Hall/CRC, 2004
    locator: Chapter 15, Kirk Pruhs, Jiří Sgall and Eric Torng, Online Scheduling (SRPT and the flow time results)
  - paper: "S. Muthukrishnan, Rajmohan Rajaraman, Anthony Shaheen and Johannes Gehrke, Online scheduling to minimize average stretch, FOCS 1999"
    locator: SRPT is 2-competitive for the total stretch on one machine
  - paper: "Linus E. Schrage and Louis W. Miller, The queue M/G/1 with the shortest remaining processing time discipline, Operations Research 14(4), 1966"
    locator: pages 670 to 684 (the mean flow time of SRPT in the M/G/1 queue)
---

Shortest remaining processing time (SRPT) is a [preemptive](/preemptive-scheduling/) scheduling rule: at each moment, the machine runs the released job with the least remaining work. It is an [online algorithm](/online-algorithm/) that needs only the size of each job at its [release](/release-time/). On one machine it minimizes the total [flow time](/flow-time/), so it is 1-competitive for that objective (Schrage 1968). On $m$ machines it is $O(\log \min(n/m, P))$-competitive, and no online algorithm is better by more than a constant factor (Leonardi and Raz 1997).

## In plain words

Jobs arrive at a machine over time, and each job says how much work it needs. The machine can stop a job at any moment and continue it later with no loss.

SRPT always works on the job that is closest to done. When a new job arrives, the machine compares its size with the work that is left on the current job. If the new job is smaller, the machine puts the current job aside and starts the new one. Otherwise it continues.

Finishing small jobs first makes the number of waiting jobs drop as fast as possible. The total waiting time of all users is the number of waiting jobs, added over time. So SRPT gives the least total waiting time that any schedule can give. The cost is that a long job can wait for a very long time if short jobs keep arriving.

## The problem

The input is a sequence $\sigma$ of $n$ jobs. Job $j$ has a release time $r_j \ge 0$ and a processing time $p_j > 0$. The algorithm learns $(r_j, p_j)$ at time $r_j$ (the [clairvoyant](/clairvoyant-scheduling/) model). One machine of speed 1 runs at most one job at a time, and a job can be preempted and resumed later. The objective is the total flow time $\sum_j (C_j - r_j)$, where $C_j$ is the completion time. In [three-field notation](/graham-three-field-notation/) this is $1 \mid r_j, \text{pmtn} \mid \sum F_j$, in the online setting.

| symbol | meaning |
|---|---|
| $\sigma$ | the sequence of jobs, revealed at the release times |
| ALG$(\sigma)$, OPT$(\sigma)$ | the total flow time of the online schedule and of the best offline schedule |
| $c$ | the [competitive ratio](/competitive-ratio/): ALG$(\sigma) \le c \cdot$ OPT$(\sigma)$ for each $\sigma$, here with additive constant $b = 0$ |
| $P$ | the ratio of the largest to the smallest processing time |

## The algorithm

The algorithm keeps the released, unfinished jobs in a [binary heap](/binary-heap/) keyed by remaining work. It is event driven: the decision can change only at a release or at a completion.

```pseudo id=main
SRPT(jobs (r_j, p_j), in order of release)
L1  H ← empty min-heap of (remaining work, job);  t ← 0;  i ← 1
L2  while i ≤ n or H is not empty do
L3      if H is empty and t < r_i then t ← r_i                ▷ idle until the next release
L4      while i ≤ n and r_i ≤ t do insert (p_i, i) into H;  i ← i + 1
L5      (q, j) ← EXTRACT-MIN(H)                              ▷ least remaining work
L6      next ← r_i if i ≤ n, else ∞
L7      if t + q ≤ next then run j on [t, t + q);  t ← t + q;  C_j ← t
L8      else run j on [t, next);  insert (q − (next − t), j) into H;  t ← next
L9  return C
```

Line L8 does not decide to preempt. It puts the current job back, and the next pass of line L5 compares it with the new jobs. A new job preempts the current one only when its work is smaller. Ties can go either way; the implementation breaks them by the job index.

## Example

Four jobs: $A = (0, 5)$, $B = (1, 2)$, $C = (2, 4)$ and $D = (3, 1)$, written as (release, processing time).

| time | event | remaining work after the event | runs next |
|---|---|---|---|
| 0 | $A$ arrives | $A$: 5 | $A$ |
| 1 | $B$ arrives | $A$: 4, $B$: 2 | $B$ (preempts $A$) |
| 2 | $C$ arrives | $A$: 4, $B$: 1, $C$: 4 | $B$ |
| 3 | $B$ completes, $D$ arrives | $A$: 4, $C$: 4, $D$: 1 | $D$ |
| 4 | $D$ completes | $A$: 4, $C$: 4 | $A$ (tie, smaller index) |
| 8 | $A$ completes | $C$: 4 | $C$ |
| 12 | $C$ completes | | |

The completion times are $C_A = 8$, $C_B = 3$, $C_C = 12$ and $C_D = 4$. The flow times are $8, 2, 10, 1$, with total 21. FIFO without preemption runs $A, B, C, D$ in this order and gets flow times $5, 6, 9, 9$, with total 29. The schedule has one preemption, at time 1.

## Correctness

The loop keeps an invariant: the heap holds exactly the released, unfinished jobs with their remaining work at time $t$. Between two releases, the job with the least remaining work keeps that property while it runs, so the rule needs a new decision only at events. This shows that the loop computes the SRPT schedule.

Optimality uses the sums of the $k$ smallest remaining works. For each $k$ and each time, this sum under SRPT is at most the sum under any other schedule. Between releases, SRPT lowers each such sum at the largest possible rate, and a release changes all schedules in the same monotone way. So SRPT has at least as many complete jobs as any schedule at each moment, and the total flow time is the integral of the number of unfinished jobs. The full proof is in [proofs/correctness.md](proofs/correctness.md). The [SRPT optimality](/srpt-optimality/) page gives a second proof by an [exchange argument](/exchange-argument/).

## Complexity

- **Time.** Sorting by release time takes $O(n \log n)$. Each pass of the loop ends with a completion (at most $n$ times) or at a release that inserts at least one job in the next pass (at most $n$ times). So the loop runs at most $2n$ times, with $O(\log n)$ heap work each. The total is $O(n \log n)$ in the worst case.
- **Space.** The heap and the output take $O(n)$.
- **Preemptions.** A job is preempted only at a release time, by a job that arrives then. So there are at most $n - 1$ preemptions in total, and the schedule has at most $2n - 1$ pieces.

## Properties

- **Online and clairvoyant.** The decision at time $t$ uses only the jobs released by $t$ and their sizes.
- **Optimal on one machine.** It minimizes $\sum F_j$ and $\sum C_j$ with preemption, for every input. It also minimizes the number of unfinished jobs at every moment.
- **Work conserving.** The machine idles only when no released job is unfinished.
- **Not fair.** A long job can starve. With a job of size 3 at time 0 and a job of size 1 at each time $1, 2, \dots, k$, SRPT completes the long job at $k + 3$, while FIFO keeps every flow time at most 3. So SRPT is not competitive for the maximum flow time.
- **Good for stretch.** On one machine, SRPT is 2-competitive for the total [stretch](/stretch/) (Muthukrishnan, Rajaraman, Shaheen and Gehrke 1999, cited here and not proved).
- **Bad with weights.** For the weighted flow time $\sum w_j F_j$, SRPT ignores the weights and can be arbitrarily bad. The [flow time minimization](/flow-time-minimization/) page gives an example.

## Variants and improvements

- **SRPT on $m$ machines.** At each moment, run the $m$ unfinished jobs with the least remaining work, on [identical machines](/identical-machines/). Leonardi and Raz showed that this is $O(\log \min(n/m, P))$-competitive for the total flow time, where $P$ is the ratio of the largest to the smallest processing time. They also showed that each online algorithm, deterministic or randomized, has ratio $\Omega(\log(n/m + P))$ on some inputs. So SRPT is optimal among online algorithms up to a constant factor. These results are cited here and not proved.
- **SPT without preemption.** [Shortest processing time first](/shortest-processing-time-first/) is the non-preemptive rule. It is optimal when all jobs are released at time 0. With release times and no preemption, see [online total completion time](/online-total-completion-time/).
- **Unknown sizes.** If the sizes are not known, SRPT cannot run. See [non-clairvoyant flow time minimization](/non-clairvoyant-flow-time-minimization/) for round robin, shortest elapsed time first and the randomized multilevel feedback rule.
- **Weights.** Highest density first runs the job with the largest $w_j / p_j$. It needs extra speed to be competitive for the weighted flow time.

## When to use it

Use SRPT when the sizes of the jobs are known or well estimated, preemption is cheap, and the goal is a low mean response time. Web servers that serve static files know the file sizes, and size-based scheduling there lowers the mean response time. Do not use pure SRPT when each job needs a guaranteed bound on its delay. Then a rule for the maximum flow time (FIFO) or for deadlines ([earliest deadline first](/earliest-deadline-first/)) fits better, or a mix of SRPT with aging.

## Pitfalls

- **Comparing with the full size.** The rule compares remaining work, not the original sizes. Operating systems texts call SRPT preemptive SJF, but a rule that preempts when the new job has a smaller original size is different and is not optimal. With job $(0, 10)$ and job $(9, 5)$, that rule preempts the first job when it has 1 unit left, for a total flow time of 20. SRPT finishes it first, for a total of 16.
- **Preempting on each tick.** An implementation driven by a clock re-decides at each tick. This is correct, but the work per job grows with its length. The event-driven loop above decides only at releases and completions.
- **Starvation.** Long jobs can wait without bound, as in the example under Properties. Systems that use SRPT often add a bound on the waiting time.
- **Costly preemption.** The optimality proof assumes that preemption is free. If a preemption costs time or a context switch, SRPT can be worse than a non-preemptive rule.
- **More than one machine.** SRPT is not optimal on $m \ge 2$ machines. The competitive ratio grows with $n/m$ and with $P$.

## Implementations

## History

Schrage and Miller analyzed the SRPT discipline in the M/G/1 queue in 1966. Schrage gave a proof in 1968 that SRPT minimizes the mean flow time on one machine for every input with preemption. Leonardi and Raz studied SRPT on parallel machines in 1997 and showed that its logarithmic ratio is optimal for online algorithms. Muthukrishnan, Rajaraman, Shaheen and Gehrke showed in 1999 that SRPT is also good for the total stretch.

## References
