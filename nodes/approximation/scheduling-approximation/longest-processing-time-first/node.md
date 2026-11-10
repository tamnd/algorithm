---
tag: NPZATW
kind: algorithm
slug: longest-processing-time-first
name: Longest processing time first (LPT)
aliases:
- LPT rule
- largest processing time first
- LPT
area: approximation/scheduling-approximation
level: core
summary: Sort jobs by decreasing processing time, then list-schedule them.
solves: [makespan-minimization]
model: real-ram
complexity:
  vars: {n: the number of jobs, m: the number of machines}
  time: {worst: Θ(n log n + m), average: Θ(n log n + m), best: Θ(n log n + m)}
  space: {extra: Θ(n + m)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1969
  people: [Ronald L. Graham]
  note: Graham proved the tight bound 4/3 - 1/(3m) for the decreasing order in 1969.
prereqs: [list-scheduling, makespan-lower-bounds]
see_also: [lpt-bound, list-scheduling, sorted-balance, multifit-algorithm, machine-covering, first-fit-decreasing, hochbaum-shmoys-ptas, makespan-minimization]
sources:
  - paper: doi:10.1137/0117039
    title: "R. L. Graham, Bounds on multiprocessing timing anomalies, SIAM Journal on Applied Mathematics 17(2), 1969"
    locator: the bound 4/3 - 1/(3m) for the list in decreasing order and its tight example (pp. 416-429 for the paper)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.3 (the longest processing time rule and its 4/3 analysis)
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 1, L. A. Hall, Approximation algorithms for scheduling (identical parallel machines, the LPT rule)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 11.1 (Sorted-Balance, the same rule with the bound 3/2)
---

Longest processing time first (LPT) is the algorithm for [makespan minimization](/makespan-minimization/) that sorts the jobs from longest to shortest and then runs [list scheduling](/list-scheduling/) on this list: each job goes to a machine with the smallest current load. Graham (1969) proved that its makespan is at most $\frac43 - \frac1{3m}$ times the optimum and that this bound is tight. The sort makes it an offline algorithm, and it runs in $O(n \log n + m)$ time with a heap of loads.

## In plain words

You have a pile of tasks and a few equal workers. First you sort the tasks so that the longest one is on top. Then you take them one by one and give each to the worker who has the least work so far.

The long tasks are the dangerous ones. If a long task comes last, it can land on top of a full worker and make him end very late. When the long tasks go first, they are spread out at the start, and the short tasks at the end fill the gaps. In the worst case the result is only one third longer than the best plan, against almost twice as long for an unsorted order.

## The problem

The input is a number $m \ge 1$ of identical machines and $n$ jobs with processing times $p_1, \ldots, p_n \ge 0$, all known in advance. The output is an assignment of jobs to machines, and the goal is a small [makespan](/makespan/) $C_{\max}$, the largest machine load. This is $P \mid\mid C_{\max}$. Here $n$ is the number of jobs and $m$ is the number of machines.

*Ratio convention.* This is a minimization problem, and an algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. For LPT, $\rho = \frac43 - \frac1{3m}$. The bound is absolute and tight for the algorithm. It is not tight for the problem, which has a [PTAS](/hochbaum-shmoys-ptas/). The analysis compares with the [average load bound](/makespan-lower-bounds/) $\mathrm{OPT} \ge \frac1m \sum_j p_j$ and with a counting argument when all jobs are longer than $\mathrm{OPT}/3$.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $p_j$ | the processing time of job $j$ |
| $\pi$ | the sorted order, with $p_{\pi(1)} \ge \cdots \ge p_{\pi(n)}$ |
| $C_{\max}$, $\mathrm{OPT}$, $\mathrm{ALG}$ | the makespan, its optimum, and the makespan of LPT |

## The algorithm

```pseudo id=main
LPT(p[1 .. n], m)
L1  π ← the jobs sorted so that p[π(1)] ≥ p[π(2)] ≥ ... ≥ p[π(n)]
L2  H ← a min-heap of the pairs (0, i) for i = 1 .. m, ordered by load, then by index
L3  for k ← 1 to n do
L4      j ← π(k)
L5      (t, i) ← extract the pair with the smallest load from H
L6      σ(j) ← i
L7      insert (t + p[j], i) into H
L8  return σ and the loads in H; C_max is the largest load
```

Lines L2 to L8 are [list scheduling](/list-scheduling/) on the list $\pi$. The sort at line L1 is stable, so equal jobs keep their input order.

## Example

Take $m = 3$ and $p = (2, 3, 4, 6, 2, 2)$. Line L1 gives the order $\pi = (4, 3, 2, 1, 5, 6)$, that is, the times $6, 4, 3, 2, 2, 2$. Ties at line L5 go to the smallest index.

| $k$ | job $j$ | $p_j$ | loads before | machine | loads after |
|---|---|---|---|---|---|
| 1 | 4 | 6 | 0, 0, 0 | 1 | 6, 0, 0 |
| 2 | 3 | 4 | 6, 0, 0 | 2 | 6, 4, 0 |
| 3 | 2 | 3 | 6, 4, 0 | 3 | 6, 4, 3 |
| 4 | 1 | 2 | 6, 4, 3 | 3 | 6, 4, 5 |
| 5 | 5 | 2 | 6, 4, 5 | 2 | 6, 6, 5 |
| 6 | 6 | 2 | 6, 6, 5 | 3 | 6, 6, 7 |

The makespan is $7$, which is optimal because $\lceil 19/3 \rceil = 7$. [List scheduling](/list-scheduling/) on the input order gives $8$.

**A worst case.** For $m = 2$ and $p = (3, 3, 2, 2, 2)$, LPT puts the two jobs of length $3$ on different machines, then the jobs of length $2$ on machine 1, machine 2 and machine 1. The loads are $7$ and $5$. The optimum is $6$, with $\{3, 3\}$ and $\{2, 2, 2\}$, so the ratio is $\frac76 = \frac43 - \frac16$.

## Correctness

LPT is list scheduling on a reordered list, so its output is a feasible schedule without idle time, by the heap invariant of [list scheduling](/list-scheduling/). For the ratio, cut the list after the job $l$ that ends last; this does not change its end time, and it makes $l$ the shortest job. Then $C_{\max} \le \frac1m \sum_j p_j + (1 - \frac1m) p_l$. If $p_l \le \mathrm{OPT}/3$, this gives the bound. If $p_l > \mathrm{OPT}/3$, then every job is longer than a third of the optimum, and a counting argument shows that LPT is optimal on such an instance. The full proof is in [the correctness proof](proofs/correctness.md), and the theorem with its tight family is on [the LPT bound](/lpt-bound/).

## Complexity

- **Time.** The sort at line L1 takes $\Theta(n \log n)$ comparisons. The heap costs $\Theta(m)$ to build and $\Theta(\log m)$ per job. The total is $\Theta(n \log n + m + n \log m)$, which is $\Theta(n \log n + m)$, in the [real RAM](/real-ram/) model.
- **Space.** $\Theta(n)$ for the order and the output, and $\Theta(m)$ for the heap.

## Properties

| claim | statement | status |
|---|---|---|
| feasible | each job runs once, on one machine, with no overlap | proved in the correctness proof |
| ratio | $\mathrm{ALG} \le (\frac43 - \frac1{3m})\,\mathrm{OPT}$ | proved in the correctness proof |
| tight for the algorithm | two jobs each of length $2m - 1, 2m - 2, \ldots, m + 1$ and three of length $m$: $\mathrm{ALG} = 4m - 1$, $\mathrm{OPT} = 3m$ | proved on [the LPT bound](/lpt-bound/) |
| optimal cases | if $n \le m$, or if every job is longer than $\mathrm{OPT}/3$ | proved in the correctness proof |
| a posteriori bound | if the machine that ends last has $k \ge 3$ jobs, the ratio is at most $\frac{k+1}{k} - \frac1{km}$ | cited (Coffman and Sethi 1976) |
| machine covering | the smallest load is at least $\frac34$ of the best smallest load | cited; see [machine covering](/machine-covering/) |
| online | no; line L1 needs all jobs | by the pseudocode |

## Variants and improvements

- **Sorted-Balance.** Kleinberg and Tardos describe the same rule with a scan for the smallest load and prove the weaker bound $\frac32$ in a few lines; see [Sorted-Balance](/sorted-balance/). Williamson and Shmoys call it the LPT rule.
- **MULTIFIT.** Coffman, Garey and Johnson (1978) use a binary search over capacities with [first fit decreasing](/first-fit-decreasing/) as the test and reach $\frac{13}{11} + 2^{-k}$; see [MULTIFIT](/multifit-algorithm/).
- **Approximation schemes.** For each $\varepsilon > 0$, the [Hochbaum-Shmoys PTAS](/hochbaum-shmoys-ptas/) gets $1 + \varepsilon$ at a much higher cost.
- **Uniform machines.** On machines with speeds, LPT puts each job where it would end first. Gonzalez, Ibarra and Sahni (1977) proved a ratio of at most $\frac{2m}{m+1}$, and later work improved the constant; see [uniform machine scheduling](/uniform-machine-scheduling/).
- **Machine covering.** The same schedule is a good answer for the max-min objective $C_{\min}$, with ratio $\frac{3m - 1}{4m - 2}$ in the worst case; see [machine covering](/machine-covering/).

## When to use it

Use LPT when all jobs are known in advance and a fast, simple rule is needed. It costs little more than a sort, it is optimal on many small instances, and its worst case is $33$ percent above the optimum, often much less in practice. As a first step before an exact method, its makespan is an upper bound that the [lower bounds](/makespan-lower-bounds/) often meet. If jobs arrive one by one, use [list scheduling](/list-scheduling/) instead. If a guarantee better than $\frac43$ is needed, use [MULTIFIT](/multifit-algorithm/).

## Pitfalls

- **Sorting the wrong way at line L1.** Sorting by increasing time is shortest processing time first, which is good for $\sum_j C_j$ but not for the makespan. With $m = 2$ and $p = (1, 1, 2)$, the increasing order gives $3$, while the optimum is $2$.
- **Not the least load at line L5.** The bound needs the machine with the smallest load, not the machine with the fewest jobs and not the next machine in turn. With these rules, a long job can land on a full machine.
- **Expecting optimal answers for two machines.** LPT is not exact even for $m = 2$, as $p = (3, 3, 2, 2, 2)$ shows. The two-machine problem is [partition](/partition-problem/), which is NP-hard.
- **Wrong bound for the truncated list.** The proof cuts the list after the job that ends last. That job is not always the last job of the list, so the term $(1 - \frac1m)p_l$ uses its own length, not $p_n$ of the full list.

## Implementations

## History

Graham (1966) analyzed arbitrary lists, and Graham (1969) proved that the decreasing order guarantees $\frac43 - \frac1{3m}$, with an instance that reaches it for each $m$. Coffman and Sethi (1976) refined the bound by the number of jobs on the critical machine. Coffman, Garey and Johnson (1978) used the same sort in MULTIFIT and improved the guarantee. Deuermeyer, Friesen and Langston (1982) showed that LPT is also good for machine covering, and Csirik, Kellerer and Woeginger (1992) found the exact ratio there.

## References
