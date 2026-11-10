---
tag: AYZTA8
kind: algorithm
slug: hochbaum-shmoys-makespan-ptas
name: Hochbaum-Shmoys PTAS for makespan scheduling
aliases:
- Hochbaum-Shmoys scheduling PTAS
- large and small jobs scheme
area: approximation/approximation-schemes
level: advanced
summary: Dual approximation with rounding of job sizes and dynamic programming over large jobs, giving a PTAS for identical-machine makespan minimization.
solves: [makespan-minimization]
model: word-ram
complexity:
  vars: {n: the number of jobs, k: "the integer ⌈1/ε⌉", P: the sum of the processing times}
  time: {worst: "O(n^(2k^2) log P)", average: "O(n^(2k^2) log P)", best: "O(n^(2k^2) log P)"}
  space: {extra: "O(n^(k^2))"}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1987
  people: [Dorit S. Hochbaum, David B. Shmoys]
  note: Hochbaum and Shmoys gave the first PTAS for P||C_max in 1987, as the main example of their dual approximation framework.
prereqs: [makespan-minimization, dual-approximation, ptas, list-scheduling]
see_also: [hochbaum-shmoys-ptas, uniform-machine-scheduling, rounding-and-scaling, eptas, fernandez-de-la-vega-lueker-aptas, configuration-lp, longest-processing-time-first, strong-np-hardness]
sources:
  - paper: "D. S. Hochbaum and D. B. Shmoys, Using dual approximation algorithms for scheduling problems: theoretical and practical results, Journal of the ACM 34(1), 1987, pp. 144-162"
    title: Hochbaum and Shmoys 1987
    locator: the PTAS for identical machines (large and small jobs, rounding, dynamic programming)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 3.2 (scheduling jobs on identical parallel machines)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 10 (minimum makespan scheduling)
  - paper: "N. Alon, Y. Azar, G. J. Woeginger and T. Yadid, Approximation schemes for scheduling on parallel machines, Journal of Scheduling 1(1), 1998, pp. 55-66"
    title: Alon, Azar, Woeginger and Yadid 1998
    locator: the EPTAS with time f(1/ε) + O(n)
---

The Hochbaum-Shmoys PTAS solves [makespan minimization](/makespan-minimization/) on identical machines, $P \mid\mid C_{\max}$, within a factor $1 + \varepsilon$ for each fixed $\varepsilon > 0$. It is the standard example of the [dual approximation](/dual-approximation/) framework: for a target $T$, a test either builds a schedule with makespan at most $(1 + \varepsilon) T$ or proves that $\mathrm{OPT} > T$, and a binary search over $T$ finds a good target. The test splits the jobs into large and small, rounds the large jobs to few sizes, packs them exactly by dynamic programming over *configurations*, and adds the small jobs greedily. This page is the technique view, with every step proved; the scheduling context, the history and the variants are on [Hochbaum-Shmoys PTAS](/hochbaum-shmoys-ptas/).

## In plain words

You must split a pile of tasks among a few identical workers so that the last worker finishes as early as possible. Guess a finishing time. A task longer than a small part of the guess is big. A worker can hold only a few big tasks, so you round the big tasks down to a few standard lengths. Now there are few kinds of big task, and a table can list all ways to fill one worker. A table search finds the least number of workers that hold all big tasks. If that is more than you have, the guess was too low. Else you give out the big tasks and then the small ones, each to the worker with the least work. Rounding and small tasks push each worker only a little past the guess. You repeat with a binary search on the guess.

## The problem

The input is $n$ jobs with positive integer processing times $p_1, \ldots, p_n$, a number $m \ge 1$ of identical machines, and an accuracy $\varepsilon > 0$. A schedule assigns each job to one machine. The load of a machine is the sum of its processing times, and the makespan $C_{\max}$ is the largest load. $\mathrm{OPT}$ is the least makespan. We use $k = \lceil 1/\varepsilon \rceil$, so $1 + 1/k \le 1 + \varepsilon$.

*Ratio convention.* This is minimization: the algorithm guarantees $\mathrm{ALG} \le (1 + 1/k)\,\mathrm{OPT}$ in the worst case, an absolute ratio with no additive term. The lower bounds on $\mathrm{OPT}$ that the analysis uses are the largest job, the average load $\sum_j p_j / m$, and the certificates "OPT > T" that the test gives.

## The algorithm

DUAL-TEST is the $(1 + 1/k)$-dual step. It works with rational numbers; $u = T/k^2$ is the rounding unit.

```pseudo id=main
DUAL-TEST(p[1 .. n], m, T, k)
L1  if some p_j > T then return NO                       ▷ OPT ≥ p_j > T
L2  u ← T / k²
L3  large ← the jobs with p_j > T/k; small ← the other jobs
L4  for each large job j: r_j ← ⌊p_j / u⌋ · u            ▷ round down to a multiple of u
L5  let s_1 < ... < s_d be the distinct values r_j and n_i the number of large jobs with r_j = s_i;
    a configuration is a vector c ≠ 0 with 0 ≤ c_i ≤ n_i and Σ_i c_i s_i ≤ T
L6  for each vector v with 0 ≤ v ≤ (n_1, ..., n_d), in lexicographic order:
        M[v] ← 0 if v = 0, else 1 + min { M[v − c] : c a configuration, c ≤ v }
L7  if M[n_1, ..., n_d] > m then return NO
L8  follow the minimizing choices of L6: machine i gets the large jobs of the i-th configuration
L9  for each small job j: let i be a machine of least load; if load(i) > T then return NO;
        put j on i
L10 return the schedule

HS-PTAS(p[1 .. n], m, k)
B1  LB ← max(max_j p_j, ⌈Σ_j p_j / m⌉)
B2  lo ← LB − 1; hi ← 2·LB; S ← DUAL-TEST(p, m, hi, k)     ▷ OPT > lo and OPT ≤ hi
B3  while hi − lo > 1:
        mid ← ⌊(lo + hi)/2⌋; S' ← DUAL-TEST(p, m, mid, k)
B4      if S' = NO then lo ← mid                          ▷ a proof that OPT > mid
B5      else hi ← mid; S ← S'
B6  return S
```

Three facts make the test work. Each rounded large job has $r_j \ge k u = T/k$, so a machine with rounded load at most $T$ holds at most $k$ large jobs, and the rounding loses less than $u$ on each of them: at most $k u = T/k$ in total. The rounded sizes lie in $\{k u, (k+1) u, \ldots, k^2 u\}$, so $d \le k^2 - k + 1$. And a small job is at most $T/k$, so a small job put on a machine of load at most $T$ ends below $(1 + 1/k) T$.

## Example

Take $p = (7, 7, 6, 6, 5, 4, 4, 3)$, $m = 3$ and $k = 3$. The sum is 42, so $\mathrm{OPT} \ge 14$, and the schedule $\{7, 7\}$, $\{6, 4, 4\}$, $\{6, 5, 3\}$ shows $\mathrm{OPT} = 14$.

DUAL-TEST with $T = 14$:

| step | result |
|---|---|
| L2, L3 | $u = 14/9$; large jobs are those with $p_j > 14/3$: $7, 7, 6, 6, 5$; small jobs $4, 4, 3$ |
| L4 | $7 \mapsto 4u = 56/9$; $6 \mapsto 3u = 42/9$; $5 \mapsto 3u = 42/9$ |
| L5 | $s = (42/9, 56/9)$, $n = (3, 2)$; the 6 configurations are $(1,0), (2,0), (3,0), (0,1), (0,2), (1,1)$ |
| L6 | $(3 + 1)(2 + 1) = 12$ table entries; $M[3, 2] = 2$ by $(0, 2)$ and $(3, 0)$ |
| L8 | machine 1: $\{7, 7\}$, load 14; machine 2: $\{6, 6, 5\}$, rounded load 14, true load 17 |
| L9 | the small jobs $4, 4, 3$ go to machine 3, load 11 |

The makespan is $17 \le (4/3) \cdot 14 \approx 18.67$. The excess of machine 2 is the rounding loss: $6 - 42/9 = 12/9$ twice and $5 - 42/9 = 3/9$ once, so $27/9 = 3$ in total, which is below $T/k = 14/3$.

With $T = 11$ all of $7, 7, 6, 6, 5, 4, 4$ are large, the table needs more than 3 machines, and the test returns NO. That proves $\mathrm{OPT} > 11$.

HS-PTAS starts with $LB = 14$, $lo = 13$ and $hi = 28$, and tests $28, 20, 16, 14$. Each test accepts, so the search ends with $hi = 14$ after 4 calls and returns the schedule above, with makespan $17 \le (4/3)\,\mathrm{OPT}$.

## Correctness

The proof has four steps; the full text is below.

1. **Soundness.** If DUAL-TEST returns a schedule, its makespan is at most $(1 + 1/k) T$. A machine of L8 has rounded load at most $T$ and at most $k$ large jobs, each rounded down by less than $u$. A small job joins a machine of load at most $T$ and is at most $T/k$.
2. **The table is exact.** $M[v]$ is the least number of machines that hold a multiset $v$ of rounded jobs with load at most $T$ each. One machine of an optimal packing of $v$ holds a configuration $c$, and the rest is a packing of $v - c$.
3. **Completeness.** If $\mathrm{OPT} \le T$, DUAL-TEST does not return NO. L1 does not fire. The large jobs of each machine of an optimal schedule form a configuration after rounding down, so $M[n] \le m$. When a small job $j$ is placed, the total load is at most $\sum p - p_j < mT$, so the least load is below $T$.
4. **The search.** The loop keeps $\mathrm{OPT} > lo$ and keeps $S$ a schedule of makespan at most $(1 + 1/k)\,hi$. At the end $hi = lo + 1 \le \mathrm{OPT}$.

## Complexity

- **Table size.** The table has $\prod_i (n_i + 1) \le (n + 1)^d \le (n+1)^{k^2}$ entries, since $d \le k^2 - k + 1$. Each configuration has $c_i \le k$, so there are at most $(k+1)^d$ configurations.
- **One test.** L6 costs $O\bigl((n+1)^d (k+1)^d d\bigr)$, which is $O(n^{2k^2})$ for $n \ge k$; L9 costs $O(n \log m)$ with a heap.
- **The search.** The range $(LB - 1, 2LB]$ halves in each step, so HS-PTAS makes $1 + \lceil \log_2 (LB + 1) \rceil = O(\log P)$ tests. The total is $O(n^{2k^2} \log P)$, polynomial for each fixed $\varepsilon$ and exponential in $1/\varepsilon^2$.
- **Space.** The table has $O(n^{k^2})$ entries.

## Properties

| claim | statement | status |
|---|---|---|
| soundness of the test | a returned schedule has makespan at most $(1 + 1/k) T$ | proved below |
| completeness of the test | $\mathrm{OPT} \le T$ implies that the test does not return NO | proved below |
| guarantee | $\mathrm{ALG} \le (1 + 1/k)\,\mathrm{OPT} \le (1 + \varepsilon)\,\mathrm{OPT}$ | proved below |
| time | $O(n^{2k^2} \log P)$ | proved below |
| no FPTAS | the problem is [strongly NP-hard](/strong-np-hardness/), so no FPTAS exists unless P = NP | cited, see [makespan minimization](/makespan-minimization/) |
| efficient scheme | time $f(1/\varepsilon) + O(n)$ is possible (Alon, Azar, Woeginger and Yadid 1998) | cited |

## Variants and improvements

- **Geometric rounding.** Rounding the large jobs down to powers of $1 + \varepsilon$ instead of multiples of $T/k^2$ gives $O(\log_{1+\varepsilon}(1/\varepsilon))$ sizes instead of $O(1/\varepsilon^2)$, and a smaller exponent.
- **An integer program in fixed dimension.** The rounded large jobs form an integer program with a constant number of configuration variables. Solving it by [Lenstra's algorithm](/integer-programming-fixed-dimension/) instead of the table gives an [EPTAS](/eptas/), with time $f(1/\varepsilon) + O(n)$; this is the approach of Alon, Azar, Woeginger and Yadid.
- **Uniform machines.** Hochbaum and Shmoys extended the method to machines with speeds; see [uniform machine scheduling](/uniform-machine-scheduling/).
- **Bin packing view.** The test answers "do the jobs fit into $m$ bins of size $T$ if each bin may be overfilled by a factor $1 + 1/k$?" The same rounding with linear grouping gives the bin packing scheme of [Fernandez de la Vega and Lueker](/fernandez-de-la-vega-lueker-aptas/).

## When to use it

The scheme proves that $P \mid\mid C_{\max}$ has a PTAS. Even for $\varepsilon = 1/3$ the table can have $(n+1)^7$ entries, so it is not a practical method. In practice [LPT](/longest-processing-time-first/) with ratio $\frac43 - \frac1{3m}$, MULTIFIT, or an integer programming solver is the better choice. The pattern (guess $T$, split large and small, round, enumerate configurations, add small items greedily) is the part to reuse.

## Pitfalls

- **Round down, then add the loss back.** The large jobs are rounded *down*, so a packing of the true sizes into machines of size $T$ is a packing of the rounded sizes. Rounding up would break completeness. The price is the loss of up to $T/k$ per machine, which soundness pays for.
- **The threshold for large and the rounding unit are linked.** The bound $k$ on the number of large jobs per machine needs $r_j \ge T/k$. With $u = T/k^2$ and $p_j > T/k$ this holds; with a coarser unit it does not.
- **Small jobs go on a machine of load at most $T$, not of least final load.** Any machine of load at most $T$ works. The check in L9 is part of the certificate: if it fails, the total load exceeds $mT$.
- **The binary search needs a "no" with proof.** Searching on a test that sometimes fails for feasible $T$ does not give the ratio. Here a NO always comes with a reason why $\mathrm{OPT} > T$.

## Implementations

## History

Hochbaum and Shmoys (1987) introduced dual approximation and used it to give the first PTAS for $P \mid\mid C_{\max}$, and a PTAS for uniform machines in a later paper. The textbook forms of Vazirani (Chapter 10) and Williamson and Shmoys (Section 3.2) use the same split into large and small jobs and a dynamic program over the rounded large jobs. Alon, Azar, Woeginger and Yadid (1998) made the dependence on $n$ linear.

## References
