---
tag: 9QD5G8
kind: algorithm
slug: multifit-algorithm
name: MULTIFIT
aliases:
- MultiFit
- MULTIFIT algorithm
area: approximation/scheduling-approximation
level: advanced
summary: Binary search on capacity, with first-fit decreasing bin packing as the test.
solves: [makespan-minimization]
model: real-ram
complexity:
  vars: {n: the number of jobs, m: the number of machines, k: the number of search steps}
  time: {worst: Θ(n log n + k n log m), average: Θ(n log n + k n log m), best: Θ(n log n + k n log m)}
  space: {extra: Θ(n + m)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1978
  people: [Edward G. Coffman Jr., Michael R. Garey, David S. Johnson]
  note: Coffman, Garey and Johnson proved the ratio 1.22 + 2^-k; Friesen and Yue later lowered the constant to 13/11, which is tight.
prereqs: [first-fit-decreasing, makespan-lower-bounds, binary-search]
see_also: [multifit-bound, first-fit-decreasing, longest-processing-time-first, dual-approximation, hochbaum-shmoys-ptas, bin-packing, makespan-minimization, list-scheduling]
sources:
  - paper: doi:10.1137/0207001
    title: "E. G. Coffman Jr., M. R. Garey and D. S. Johnson, An application of bin-packing to multiprocessor scheduling, SIAM Journal on Computing 7(1), 1978"
    locator: the definition of MULTIFIT, the initial interval, and the bound 1.22 + 2^-k (pp. 1-17 for the paper)
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 1, L. A. Hall, Approximation algorithms for scheduling (identical parallel machines, MULTIFIT)
  - paper: "M. Yue, On the exact upper bound for the MULTIFIT processor scheduling algorithm, Annals of Operations Research 24, 1990, pp. 233-259"
    title: Yue 1990
    locator: the bound 13/11 for the capacity at which first fit decreasing always succeeds
  - paper: "D. K. Friesen, Tighter bounds for the MULTIFIT processor scheduling algorithm, SIAM Journal on Computing 13, 1984"
    title: Friesen 1984
    locator: the bound 1.2 + 2^-k and the example that shows the constant cannot go below 13/11
---

MULTIFIT is an algorithm for [makespan minimization](/makespan-minimization/) on identical machines that does a [binary search](/binary-search/) over a common capacity $C$ and, at each step, tests whether [first fit decreasing](/first-fit-decreasing/) packs all jobs into $m$ bins of capacity $C$. Coffman, Garey and Johnson introduced it in 1978, and after $k$ steps its makespan is at most $(\frac{13}{11} + 2^{-k})$ times the optimum, by the work of Friesen and Yue. This is better than the $\frac43 - \frac1{3m}$ of [LPT](/longest-processing-time-first/), at the cost of $k$ runs of first fit decreasing. It uses the duality between scheduling and [bin packing](/bin-packing/): a makespan of at most $C$ on $m$ machines is the same as a packing into $m$ bins of capacity $C$.

## In plain words

You want to share tasks among a few equal workers so that everyone ends early. Turn the question around: guess a finish time, and ask whether the tasks fit into the workers when no one may work longer than the guess. To test a guess, sort the tasks from biggest to smallest and put each one with the first worker who still has room.

If the test works, try a smaller guess. If it fails, try a larger one. Each test halves the range of guesses. After a few tests you keep the smallest guess that worked, and its plan is the answer. The test can fail even when a plan exists, but only when the guess is close to the best finish time, so the answer is close to the best.

## The problem

The input is a number $m \ge 1$ of identical machines, $n$ jobs with times $p_1, \ldots, p_n \ge 0$, and a number $k \ge 0$ of search steps. The output is an assignment of jobs to machines with a small [makespan](/makespan/) $C_{\max}$. This is $P \mid\mid C_{\max}$. Here $n$ is the number of jobs and $m$ is the number of machines.

*Ratio convention.* This is a minimization problem, and an algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. For MULTIFIT with $k$ steps, $\rho = \frac{13}{11} + 2^{-k}$. The bound is absolute. The constant $\frac{13}{11}$ is tight for the algorithm: an instance with $m = 13$ gives exactly $\frac{13}{11}$ for every $k \ge 5$. It is not tight for the problem, which has a [PTAS](/hochbaum-shmoys-ptas/). The analysis compares with the [lower bounds](/makespan-lower-bounds/) $\mathrm{OPT} \ge A = \frac1m \sum_j p_j$ and $\mathrm{OPT} \ge \max_j p_j$, which fix the start of the search.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of jobs and the number of machines |
| $p_j$ | the processing time of job $j$ |
| $A$ | the average load $\frac1m \sum_j p_j$ |
| $C$, $\mathrm{lo}$, $\mathrm{hi}$ | the tested capacity and the ends of the search interval |
| $k$ | the number of search steps |
| $\mathrm{OPT}$, $\mathrm{ALG}$ | the optimal makespan and the makespan of MULTIFIT |

## The algorithm

```pseudo id=main
MULTIFIT(p[1 .. n], m, k)
L1  A ← (p[1] + ... + p[n]) / m
L2  lo ← max(A, max_j p[j]), hi ← max(2A, max_j p[j])
L3  repeat k times
L4      C ← (lo + hi) / 2
L5      if FFD(p, C, m) succeeds then hi ← C
L6      else lo ← C
L7  return the bins of FFD(p, hi, m), one bin per machine

FFD(p, C, m): returns at most m bins of capacity C, or fails
L8  sort the jobs so that p[1] ≥ p[2] ≥ ... ≥ p[n]
L9  for j ← 1 to n do
L10     put j into the first open bin whose load plus p[j] is at most C, if there is one
L11     else if fewer than m bins are open and p[j] ≤ C, open a new bin with j; otherwise fail
```

Lines L8 to L11 are [first fit decreasing](/first-fit-decreasing/) with capacity $C$, stopped as soon as it needs bin $m + 1$. The sort at line L8 can be done once for all calls.

## Example

Take $m = 2$ and $p = (3, 3, 2, 2, 2, 2)$. The total is $14$, so $A = 7$, and line L2 gives $\mathrm{lo} = 7$ and $\mathrm{hi} = 14$. The optimum is $7$, with $\{3, 2, 2\}$ twice.

| step | lo | hi | $C$ | bins of FFD at $C$ | result |
|---|---|---|---|---|---|
| 1 | 7 | 14 | 21/2 | $\{3, 3, 2, 2\}$, $\{2, 2\}$ | success, hi ← 21/2 |
| 2 | 7 | 21/2 | 35/4 | $\{3, 3, 2\}$, $\{2, 2, 2\}$ | success, hi ← 35/4 |
| 3 | 7 | 35/4 | 63/8 | needs a third bin | failure, lo ← 63/8 |
| 4 | 63/8 | 35/4 | 133/16 | $\{3, 3, 2\}$, $\{2, 2, 2\}$ | success, hi ← 133/16 |

With $k = 0, 1, 2, 3, 4$ steps the makespan is $14, 10, 8, 8, 8$. Every capacity below $8$ fails, because first fit decreasing puts both jobs of length $3$ in the first bin and then needs room for four jobs of length $2$ in the rest. So MULTIFIT gives $8$ for every $k \ge 2$, and the ratio $\frac87$ meets the bound that Coffman, Garey and Johnson proved for two machines.

**First fit decreasing is not monotone in the capacity.** With $m = 3$ and $p = (44, 24, 24, 22, 21, 17, 8, 8, 6, 6)$, of total $180$, first fit decreasing succeeds at capacity $60$ but fails at capacity $61$. So the set of capacities that succeed is not an interval, and the binary search does not find the smallest one. The analysis below does not need monotonicity.

## Correctness

Two facts hold at each step: first fit decreasing succeeds at $\mathrm{hi}$, and $\mathrm{lo} \le r \cdot \mathrm{OPT}$, where $r$ is a constant such that first fit decreasing succeeds at every capacity $C \ge r \cdot \mathrm{OPT}$. At the start, the first fact holds because first fit leaves at most one bin half full or less, so it cannot fail at a capacity that is at least $2A$ and at least $\max_j p_j$; the second holds because $\mathrm{lo} \le \mathrm{OPT}$. Line L5 keeps the first fact, and line L6 keeps the second, since a failure at $C$ means $C < r \cdot \mathrm{OPT}$. The first interval has length at most $A \le \mathrm{OPT}$, and each step halves it, so

$$\mathrm{ALG} \le \mathrm{hi} \le \mathrm{lo} + 2^{-k} A \le \big(r + 2^{-k}\big)\,\mathrm{OPT}.$$

The full proof, with $r = \frac43 - \frac1{3m}$ proved in full, is in [the correctness proof](proofs/correctness.md). The constants $r = 1.22$ and $r = \frac{13}{11}$ are on [the MULTIFIT bound](/multifit-bound/).

## Complexity

- **Time.** The sort takes $\Theta(n \log n)$ once. Each call of first fit decreasing places $n$ jobs, and with a max tree over the free space of the $m$ bins each placement takes $\Theta(\log m)$. So $k + 1$ calls take $\Theta(k n \log m)$ beyond the sort, in the [real RAM](/real-ram/) model. A linear scan over the open bins gives $\Theta(k n m)$, which is the form of the reference code.
- **Space.** $\Theta(n + m)$ for the sorted order, the bins and their loads.

## Properties

| claim | statement | status |
|---|---|---|
| feasible | the output uses at most $m$ machines and has makespan at most $\mathrm{hi}$ | proved in the correctness proof |
| start interval | first fit decreasing succeeds at $\max(2A, \max_j p_j)$ | proved in the correctness proof |
| simple ratio | $\mathrm{ALG} \le (\frac43 - \frac1{3m} + 2^{-k})\,\mathrm{OPT}$ | proved in the correctness proof |
| ratio of the paper | $\mathrm{ALG} \le (1.22 + 2^{-k})\,\mathrm{OPT}$ | cited (Coffman, Garey and Johnson 1978) |
| best ratio | $\mathrm{ALG} \le (\frac{13}{11} + 2^{-k})\,\mathrm{OPT}$ | cited (Yue 1990); see [the MULTIFIT bound](/multifit-bound/) |
| tight for the algorithm | $m = 13$, $\mathrm{OPT} = 66$, and $\mathrm{ALG} = 78$ for every $k \ge 5$ | shown on [the MULTIFIT bound](/multifit-bound/) |
| two machines | the worst case is $\frac87$, reached by $p = (3, 3, 2, 2, 2, 2)$ | bound cited; example above |
| not monotone | success of first fit decreasing at $C$ does not imply success at a larger capacity | example above |

## Variants and improvements

- **Modified MULTIFIT.** Friesen and Langston (1986) changed the packing rule inside the test and proved the constant $\frac{72}{61} \approx 1.180$, slightly below $\frac{13}{11} \approx 1.182$.
- **Dual approximation.** Hochbaum and Shmoys turned the same idea into a general method: a test that, at capacity $C$, either packs into $m$ bins of capacity $(1 + \varepsilon)C$ or proves $\mathrm{OPT} > C$. With an exact test for the large jobs this gives the [PTAS](/hochbaum-shmoys-ptas/); see [dual approximation](/dual-approximation/).

## When to use it

Use MULTIFIT when all jobs are known in advance and LPT is not good enough, but a full approximation scheme is too slow. A few steps of the search, each a run of first fit decreasing, give a guarantee near $1.2$. In practice, run both LPT and MULTIFIT and keep the better schedule. For online arrival, use [list scheduling](/list-scheduling/) instead, since the test needs all jobs.

## Pitfalls

- **Starting too low at line L2.** If $\mathrm{hi}$ is a capacity at which first fit decreasing fails, line L7 has no packing to return. The value $\max(2A, \max_j p_j)$ is safe; the value $\max(A, \max_j p_j)$ is not.
- **Returning lo at line L7.** The capacity $\mathrm{lo}$ may have failed. Only $\mathrm{hi}$ is known to succeed, so line L7 packs at $\mathrm{hi}$.
- **Assuming monotone success at line L5.** First fit decreasing can succeed at $C$ and fail at a larger capacity. Do not stop the search early, and do not claim that MULTIFIT finds the smallest capacity at which the test succeeds.
- **Forgetting the size check at line L11.** A job longer than $C$ can never be packed, and the test must fail at once rather than open a bin that is too small.
- **Floating-point capacities.** Comparisons like $\mathrm{load} + p_j \le C$ are exact when sums equal $C$. Use integers scaled by $2^k$ or exact fractions.

## Implementations

## History

Coffman, Garey and Johnson (1978) introduced MULTIFIT, proved the ratio $1.22 + 2^{-k}$, and found exact values for a few small $m$, such as $\frac87$ for $m = 2$. Friesen (1984) improved the constant to $1.2$ and gave an example that shows that it cannot be below $\frac{13}{11}$. Yue (1990) proved $\frac{13}{11}$; later authors filled gaps in this proof. Friesen and Langston (1986) gave a modified version with $\frac{72}{61}$.

## References
