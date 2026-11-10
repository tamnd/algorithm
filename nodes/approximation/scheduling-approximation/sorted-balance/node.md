---
tag: SYMRSF
kind: algorithm
slug: sorted-balance
name: Sorted-Balance load balancing
aliases:
- Sorted-Balance
- sorted greedy load balancing
area: approximation/scheduling-approximation
level: core
summary: A greedy load balancing method that sorts jobs by decreasing size and assigns each to the least loaded machine.
solves: [makespan-minimization]
model: real-ram
complexity:
  vars: {n: the number of jobs, m: the number of machines}
  time: {worst: Θ(n log n + n m), average: Θ(n log n + n m), best: Θ(n log n + n m)}
  space: {extra: Θ(n + m)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1969
  people: [Ronald L. Graham, Jon Kleinberg, Eva Tardos]
  note: Graham analyzed the sorted greedy rule in 1969, and Kleinberg and Tardos named it Sorted-Balance and gave the short 3/2 proof in their 2005 textbook.
prereqs: [list-scheduling, makespan-lower-bounds]
see_also: [longest-processing-time-first, lpt-bound, list-scheduling, list-scheduling-bound, makespan-lower-bounds, multifit-algorithm, makespan-minimization, greedy-algorithm]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 11.1 (Greedy-Balance, Sorted-Balance, the bound T* >= 2 t_(m+1) and the 3/2 analysis)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.3 (the same sorted rule as the longest processing time rule, with the 4/3 analysis)
  - paper: doi:10.1137/0117039
    title: "R. L. Graham, Bounds on multiprocessing timing anomalies, SIAM Journal on Applied Mathematics 17(2), 1969"
    locator: the bound 4/3 - 1/(3m) for the list in decreasing order (pp. 416-429 for the paper)
---

Sorted-Balance is the [greedy](/greedy-algorithm/) load balancing algorithm that sorts the jobs from largest to smallest and gives each job, in that order, to a machine with the smallest current load. It is the name that Kleinberg and Tardos use, and their short proof shows a makespan at most $\frac32$ times the optimum, from the fact that two of the $m + 1$ largest jobs share a machine. Williamson and Shmoys call the same algorithm the longest processing time rule, so Sorted-Balance is [LPT](/longest-processing-time-first/), and its true worst case is the smaller ratio $\frac43 - \frac1{3m}$ of [the LPT bound](/lpt-bound/). This page gives the scan form and the simple $\frac32$ proof.

## In plain words

You have tasks and a few equal workers, and you want the last worker to finish early. Sort the tasks from the biggest to the smallest. Then give each task, in this order, to the worker who has the least work at that moment.

Why this is good: if the worker who ends last got only one task, nobody could do better, because that task has to be done by someone. If he got more than one, then his last task came after every worker had a task. So it is no bigger than the task in place one after the number of workers. Two of these big tasks must go to the same worker in any plan, so his last task is at most half of the best finish time. This gives at most one and a half times the best.

## The problem

The input is a number $m \ge 1$ of identical machines and $n$ jobs with sizes $p_1, \ldots, p_n \ge 0$, all known in advance. The output is an assignment $A(1), \ldots, A(m)$ of the jobs to machines, with loads $T_i = \sum_{j \in A(i)} p_j$. The goal is a small [makespan](/makespan/) $\max_i T_i$. This is $P \mid\mid C_{\max}$, the problem of [makespan minimization](/makespan-minimization/). Here $n$ is the number of jobs and $m$ is the number of machines.

*Ratio convention.* This is a minimization problem, and an algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. This page proves $\rho = \frac32 - \frac1{2m}$, an absolute bound. The analysis is not tight for the algorithm: the true worst case is $\frac43 - \frac1{3m}$, proved on [the LPT bound](/lpt-bound/). It is not tight for the problem, which has a [PTAS](/hochbaum-shmoys-ptas/). The analysis compares with the [lower bounds](/makespan-lower-bounds/) $\mathrm{OPT} \ge \frac1m \sum_j p_j$, $\mathrm{OPT} \ge \max_j p_j$ and $\mathrm{OPT} \ge 2 p_{m+1}$.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $p_j$ | the size of job $j$, sorted so that $p_1 \ge \cdots \ge p_n$ |
| $A(i)$, $T_i$ | the jobs of machine $i$ and its load |
| $\mathrm{OPT}$, $\mathrm{ALG}$ | the optimal makespan and the makespan of Sorted-Balance |

## The algorithm

```pseudo id=main
SORTED-BALANCE(p[1 .. n], m)
L1  sort the jobs so that p[1] ≥ p[2] ≥ ... ≥ p[n]
L2  for i ← 1 to m do T[i] ← 0, A[i] ← ∅
L3  for j ← 1 to n do
L4      i ← a machine with the smallest T[i], by a scan over 1 .. m
L5      A[i] ← A[i] ∪ {j}
L6      T[i] ← T[i] + p[j]
L7  return A[1 .. m] and T[1 .. m]
```

Without line L1, this is Greedy-Balance, which is [list scheduling](/list-scheduling/) in the input order.

## Example

Take $m = 3$ and $p = (6, 5, 4, 4, 3, 3, 2)$, already sorted. Ties at line L4 go to the smallest index.

| job $j$ | $p_j$ | loads before | machine | loads after |
|---|---|---|---|---|
| 1 | 6 | 0, 0, 0 | 1 | 6, 0, 0 |
| 2 | 5 | 6, 0, 0 | 2 | 6, 5, 0 |
| 3 | 4 | 6, 5, 0 | 3 | 6, 5, 4 |
| 4 | 4 | 6, 5, 4 | 3 | 6, 5, 8 |
| 5 | 3 | 6, 5, 8 | 2 | 6, 8, 8 |
| 6 | 3 | 6, 8, 8 | 1 | 9, 8, 8 |
| 7 | 2 | 9, 8, 8 | 2 | 9, 10, 8 |

The result is $A(1) = \{1, 6\}$, $A(2) = \{2, 5, 7\}$, $A(3) = \{3, 4\}$, with loads $9, 10, 8$ and makespan $10$. The optimum is $9 = 27/3$, with $\{6, 3\}$, $\{5, 4\}$ and $\{4, 3, 2\}$. In the proof, the last job is job 7. It starts at $8$, and $p_7 = 2 \le p_4 = 4 \le \mathrm{OPT}/2$.

## Correctness

Each job goes to exactly one machine at line L5, and line L6 keeps $T_i$ equal to the total size of $A(i)$. So the output is an assignment, and its makespan is $\max_i T_i$.

For the ratio, let machine $i$ have the largest final load, and let $l$ be the last job put on $i$. If $i$ had load $0$ before $l$, then $T_i = p_l \le \mathrm{OPT}$. Otherwise all machines had a job before $l$, so $l \ge m + 1$ and $p_l \le p_{m+1} \le \mathrm{OPT}/2$. Then

$$T_i \le \frac1m \sum_j p_j + \Big(1 - \frac1m\Big)p_l \le \Big(\frac32 - \frac1{2m}\Big)\mathrm{OPT}.$$

The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Time.** The sort at line L1 takes $\Theta(n \log n)$. Each scan at line L4 takes $\Theta(m)$, so the loop takes $\Theta(nm)$. The total is $\Theta(n \log n + nm)$ in the [real RAM](/real-ram/) model. A heap for line L4 gives $\Theta(n \log n + m)$, which is the form on the [LPT](/longest-processing-time-first/) page.
- **Space.** $\Theta(n + m)$ for the sorted order, the sets $A(i)$ and the loads.

## Properties

| claim | statement | status |
|---|---|---|
| feasible | each job is on exactly one machine | proved in the correctness proof |
| simple ratio | $\mathrm{ALG} \le (\frac32 - \frac1{2m})\,\mathrm{OPT}$ | proved in the correctness proof |
| true ratio | $\mathrm{ALG} \le (\frac43 - \frac1{3m})\,\mathrm{OPT}$, tight | proved on [the LPT bound](/lpt-bound/) |
| analysis not tight | for $m = 2$ the simple bound is $\frac54$, but the worst case is $\frac76$, for example $p = (3, 3, 2, 2, 2)$ | follows from the true ratio |
| same as LPT | the same schedule as LPT with the same tie rule | by the pseudocode |
| online | no; line L1 needs all jobs | by the pseudocode |

## Variants and improvements

- **Greedy-Balance.** Without the sort, the rule is [list scheduling](/list-scheduling/), with the tight ratio $2 - \frac1m$.
- **A sharper analysis.** The case split at $\mathrm{OPT}/3$ in place of $\mathrm{OPT}/2$, with a counting argument for the case where all jobs are long, gives $\frac43 - \frac1{3m}$; see [the LPT bound](/lpt-bound/).
- **MULTIFIT and schemes.** [MULTIFIT](/multifit-algorithm/) reaches $\frac{13}{11} + 2^{-k}$, and the [Hochbaum-Shmoys PTAS](/hochbaum-shmoys-ptas/) reaches $1 + \varepsilon$.

## When to use it

Use the scan form when the number of machines is small, since it needs no heap and is easy to check by hand. Use it in teaching, because the $\frac32$ proof is short and shows how the pair bound $\mathrm{OPT} \ge 2 p_{m+1}$ is used. For many machines, use the heap form on the [LPT](/longest-processing-time-first/) page. When quoting a guarantee, quote $\frac43 - \frac1{3m}$, not $\frac32$.

## Pitfalls

- **Leaving out line L1.** Without the sort, the last job can be the largest job, and the step $p_l \le p_{m+1}$ in the proof fails. The ratio then is $2 - \frac1m$, as for list scheduling.
- **Sorting in increasing order at line L1.** The proof needs the late jobs to be small. With increasing order and $m = 2$, $p = (1, 1, 2)$ gives makespan $3$ against the optimum $2$.
- **A slow scan at line L4.** The scan costs $\Theta(m)$ per job. With $m$ near $n$, the loop takes $\Theta(n^2)$; a heap takes $\Theta(n \log n)$.
- **Quoting $\frac32$ as the worst case.** The $\frac32$ bound comes from this short proof only. The algorithm is never worse than $\frac43 - \frac1{3m}$.

## Implementations

## History

Graham (1969) proved the bound $\frac43 - \frac1{3m}$ for the decreasing order, and the rule has been known as LPT since then. Kleinberg and Tardos (2005) present load balancing as the first example of their chapter on approximation algorithms: Greedy-Balance with the bound $2$, and then Sorted-Balance with the bound $\frac32$ from the observation $T^* \ge 2 t_{m+1}$.

## References
