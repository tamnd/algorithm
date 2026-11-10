---
tag: KC7QKZ
kind: algorithm
slug: hochbaum-shmoys-ptas
name: Hochbaum-Shmoys PTAS for makespan
aliases:
- Hochbaum-Shmoys dual approximation scheme
- PTAS for P||Cmax
- Hochbaum-Shmoys scheme
area: approximation/scheduling-approximation
level: research
summary: Polynomial-time approximation scheme for makespan on identical and uniform machines.
solves: [makespan-minimization]
model: word-ram
complexity:
  vars: {n: the number of jobs, m: the number of machines, k: the accuracy parameter 1/ε, P: the sum of the processing times}
  time: {worst: O((n + 1)^(k^2) (k + 1)^(k^2) k^2 log P + n m log P)}
  space: {extra: O((n + 1)^(k^2) k^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1987
  people: [Dorit S. Hochbaum, David B. Shmoys]
  note: Hochbaum and Shmoys introduced dual approximation and gave the first PTAS for identical machines in 1987, and a PTAS for uniform machines in 1988.
prereqs: [makespan-minimization, dual-approximation, ptas, makespan-lower-bounds, list-scheduling]
see_also: [hochbaum-shmoys-makespan-ptas, eptas, uniform-machine-scheduling, lpt-bound, multifit-algorithm, no-fptas-for-strongly-np-hard-problems, configuration-lp, bin-packing]
sources:
  - paper: doi:10.1145/7531.7535
    title: "D. S. Hochbaum and D. B. Shmoys, Using dual approximation algorithms for scheduling problems: theoretical and practical results, Journal of the ACM 34(1), 1987"
    locator: the dual approximation framework and the scheme for identical machines with rounding of the large jobs and a dynamic program
  - paper: doi:10.1137/0217033
    title: "D. S. Hochbaum and D. B. Shmoys, A polynomial approximation scheme for scheduling on uniform processors: using the dual approximation approach, SIAM Journal on Computing 17(3), 1988"
    locator: the extension of the scheme to uniform machines
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 3.2 (a PTAS for minimizing the makespan on identical machines)
  - paper: "N. Alon, Y. Azar, G. J. Woeginger and T. Yadid, Approximation schemes for scheduling on parallel machines, Journal of Scheduling 1(1), 1998"
    locator: the linear time scheme of the form f(1/ε) + O(n) for makespan and other objectives
  - paper: "K. Jansen, An EPTAS for scheduling jobs on uniform processors: using an MILP relaxation with a constant number of integral variables, SIAM Journal on Discrete Mathematics 24(2), 2010"
    locator: the efficient scheme for uniform machines
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 9, D. S. Hochbaum, Various notions of approximations (the efficient scheme by integer programming in fixed dimension)
---

The Hochbaum-Shmoys scheme is a polynomial-time approximation scheme ([PTAS](/ptas/)) for [makespan minimization](/makespan-minimization/) on identical machines, $P \mid\mid C_{\max}$. For each fixed $\varepsilon > 0$ it finds a schedule of makespan at most $(1 + \varepsilon)\,\mathrm{OPT}$ in time polynomial in the input. It was the first use of [dual approximation](/dual-approximation/): for a guess $T$, either build a schedule of makespan at most $(1 + \varepsilon) T$ or prove that $\mathrm{OPT} > T$. The test rounds the long jobs to few sizes, packs them exactly with a dynamic program over configurations, and adds the short jobs greedily. A binary search over $T$ finishes the scheme. This page treats the scheduling side; the page [Hochbaum-Shmoys makespan PTAS](/hochbaum-shmoys-makespan-ptas/) treats it as an example of approximation schemes.

## In plain words

You must share tasks among equal workers so that the last one finishes early, and you accept being a little late, say 10 percent, in exchange for a fast plan.

Guess a finishing time. Call a task long if it takes more than a tenth of the guess. Few long tasks fit on one worker, and if you round their lengths down to a coarse grid, there are only a few kinds. With few kinds, you can try every way to fill a worker and find, exactly, the fewest workers needed for the rounded long tasks. Then hand out the short tasks one by one to the least busy worker. Either everything finishes within 10 percent of the guess, or the guess was too small. Search for the smallest guess that works.

## The problem

There are $n$ jobs with positive integer processing times $p_1, \ldots, p_n$ and $m$ identical machines. A schedule assigns each job to a machine, the load of a machine is the sum of its times, and the makespan is the largest load. $\mathrm{OPT}$ is the least makespan and $\mathrm{ALG}$ the makespan of the output. The accuracy is $\varepsilon = 1/k$ for an integer $k \ge 1$. Let $P = \sum_j p_j$ and $\mathrm{LB} = \max(\max_j p_j, \lceil P/m \rceil)$.

For a guess $T$, a job is *long* if $p_j > T/k$ and *short* otherwise. The *rounded size* of a long job with $p_j \le T$ is the integer $r_j = \lfloor p_j k^2 / T \rfloor$, so $r_j \in \{k, \ldots, k^2\}$ and $r_j T/k^2 \le p_j < (r_j + 1) T/k^2$. A *configuration* is a nonzero multiset of rounded sizes with sum at most $k^2$, which is the set of long jobs that one machine may hold.

## The algorithm

```pseudo id=main
HS-PTAS(p, m, k)                              ▷ ε = 1/k
L1  lo ← LB; hi ← 2 LB                         ▷ OPT lies in [LB, 2 LB]
L2  while lo < hi do
L3      mid ← ⌊(lo + hi)/2⌋
L4      if DUAL(p, m, k, mid) ≠ FAIL then hi ← mid else lo ← mid + 1
L5  return DUAL(p, m, k, hi)

DUAL(p, m, k, T)
L6  if some p_j > T then return FAIL
L7  r_j ← ⌊p_j k² / T⌋ for each long job (p_j > T/k)
L8  M ← the least number of configurations that hold all long jobs     ▷ dynamic program over count vectors
L9  if M > m then return FAIL
L10 put the long jobs on M machines, one configuration on each, as the dynamic program found
L11 for each short job j do
L12     i ← a machine of least load
L13     if load(i) > T then return FAIL
L14     put j on i
L15 return the schedule
```

The dynamic program of line L8 works on count vectors. The long jobs are described by the vector $(a_k, \ldots, a_{k^2})$, where $a_s$ is the number of long jobs of rounded size $s$. With $f(\mathbf{0}) = 0$, it computes

$$f(\mathbf{a}) = 1 + \min \{ f(\mathbf{a} - \mathbf{c}) : \mathbf{c} \text{ a configuration},\ \mathbf{c} \le \mathbf{a} \},$$

so $f(\mathbf{a})$ is the least number of machines that hold the long jobs with each machine in a configuration. The search of lines L1 to L4 runs on integers, because $\mathrm{OPT}$ is an integer. The upper end $2\,\mathrm{LB}$ is safe: list scheduling has makespan at most $P/m + \max_j p_j \le 2\,\mathrm{LB}$, so $\mathrm{OPT} \le 2\,\mathrm{LB}$, and then the test at $2\,\mathrm{LB}$ succeeds.

## Example

Take $m = 2$, $k = 3$ (so $\varepsilon = 1/3$) and $p = (5, 5, 5, 1, 1)$. Then $P = 17$, $\mathrm{LB} = 9$, and the search starts with $lo = 9$ and $hi = 18$.

| guess $T$ | long jobs | rounded sizes | machines needed | result |
|---|---|---|---|---|
| 13 | the three 5s | 3, 3, 3 | 1 | success, so $hi = 13$ |
| 11 | the three 5s | 4, 4, 4 | 2 | success, so $hi = 11$ |
| 10 | the three 5s | 4, 4, 4 | 2 | success, so $hi = 10$ |
| 9 | the three 5s | 5, 5, 5 | 3 | FAIL, so $lo = 10$ |

At $T = 9$, two rounded sizes 5 add up to $10 > 9 = k^2$, so each machine holds one long job, and three machines are needed. This proves $\mathrm{OPT} > 9$. The final test at $T = 10$ puts two long jobs on machine 1 and one on machine 2, with loads 10 and 5, and the short jobs go to machine 2. The makespan is 10, which is optimal here; the guarantee is only $(1 + 1/3) \cdot 10$.

At $T = 13$ the test succeeds with one machine for all three long jobs, a load of 15. This is allowed: the test promises only a makespan of at most $(1 + 1/3) \cdot 13$.

## Correctness

The proof checks the two promises of the test and then the search. The full proof is in the proofs section.

- **A failure proves $\mathrm{OPT} > T$.** Line L6 fails only if one job is longer than $T$. If $\mathrm{OPT} \le T$, the long jobs on each machine of an optimal schedule have rounded sizes with sum at most $\sum p_j k^2/T \le k^2$, so they form a configuration, and line L9 does not fail. Line L13 fails only if every machine already has load above $T$, and then $P > mT$, so $\mathrm{OPT} \ge P/m > T$.
- **A success has makespan at most $(1 + 1/k) T$.** A configuration has at most $k$ jobs, because each rounded size is at least $k$. Each job is shorter than $(r_j + 1) T/k^2$, so the long jobs on one machine take less than $(k^2 + k) T/k^2 = T + T/k$. A short job goes to a machine of load at most $T$, so that machine ends at most at $T + T/k$.
- **The search.** At the end $hi = lo$. Either $lo = \mathrm{LB} \le \mathrm{OPT}$, or the test failed at $lo - 1$, so $\mathrm{OPT} > lo - 1$. In both cases $T = hi \le \mathrm{OPT}$, and $\mathrm{ALG} \le (1 + \varepsilon) T \le (1 + \varepsilon)\,\mathrm{OPT}$.

## Complexity

- There are at most $d = k^2 - k + 1$ rounded sizes, so at most $(n + 1)^{d}$ count vectors and at most $(k + 1)^{d}$ configurations, each with at most $k$ jobs. The dynamic program takes $O((n + 1)^{k^2} (k + 1)^{k^2} k^2)$ time and $O((n + 1)^{k^2} k^2)$ space. This is $n^{O(1/\varepsilon^2)}$ for fixed $\varepsilon$.
- The short jobs take $O(n \log m)$ time with a heap of machine loads, or $O(nm)$ by a scan.
- The search calls the test $O(\log \mathrm{LB}) = O(\log P)$ times. Hochbaum and Shmoys search over real values and stop after $O(\log(1/\varepsilon))$ steps, which removes the dependence on $P$.

The running time is polynomial in $n$ for each fixed $\varepsilon$, but the exponent grows like $1/\varepsilon^2$, so the scheme is practical only for coarse $\varepsilon$.

## Properties

- **A PTAS, not an FPTAS.** The ratio $1 + \varepsilon$ is absolute and holds for every instance, with $\mathrm{ALG}$ compared with the guess $T \le \mathrm{OPT}$. No FPTAS exists unless P = NP, because $P \mid\mid C_{\max}$ is strongly NP-hard; see [no FPTAS for strongly NP-hard problems](/no-fptas-for-strongly-np-hard-problems/).
- **Tight for the problem.** Since the problem has a PTAS, the best ratio for a polynomial algorithm is $1 + \varepsilon$ for every fixed $\varepsilon > 0$, and no constant above 1 is a hardness threshold.
- **Deterministic and offline.** All jobs must be known before the test runs.
- **Dual approximation.** The test may succeed for some $T < \mathrm{OPT}$; then its schedule is still within $(1 + \varepsilon) T < (1 + \varepsilon)\,\mathrm{OPT}$.

## Variants and improvements

- **An efficient PTAS.** The dynamic program is the expensive part. Hochbaum (1997) noted that the long jobs can be packed by an integer program with a fixed number of variables, solved by [Lenstra's algorithm](/lenstra-algorithm/), which gives an [EPTAS](/eptas/) with running time $f(1/\varepsilon) + \mathrm{poly}(n)$. Alon, Azar, Woeginger and Yadid (1998) gave such a scheme in time $f(1/\varepsilon) + O(n)$ for the makespan and for many other objectives. Later work brought $f$ down to $2^{O(1/\varepsilon \cdot \log^4 (1/\varepsilon))}$, close to the lower bound of Chen, Jansen and Zhang (2014): under the exponential time hypothesis, no scheme runs in time $2^{(1/\varepsilon)^{1 - \delta}} \mathrm{poly}(n)$ for any $\delta > 0$.
- **Uniform machines.** Hochbaum and Shmoys (1988) extended dual approximation to $Q \mid\mid C_{\max}$, where machine $i$ has speed $s_i$; the rounding and the packing are harder because the machines have different capacities. Jansen (2010) gave an EPTAS for this case. See [uniform machine scheduling](/uniform-machine-scheduling/).
- **Fixed $m$.** For a constant number of machines, an FPTAS exists (Sahni 1976), because the problem is then only weakly NP-hard.
- **Unrelated machines.** No PTAS exists for $R \mid\mid C_{\max}$ unless P = NP; see [the 3/2 hardness](/unrelated-makespan-inapproximability/).

## When to use it

The scheme matters most in theory: it shows that $P \mid\mid C_{\max}$ can be approximated as well as one likes. In practice, LPT ($4/3 - 1/(3m)$), [MULTIFIT](/multifit-algorithm/) ($13/11$) and integer programming solvers are faster for the same quality. The dual test itself is a useful tool, for example inside a search for the best $T$ with a heuristic packing.

## Pitfalls

- **Rounding up instead of down.** The proof that a failure means $\mathrm{OPT} > T$ needs the rounded sizes of an optimal machine to fit. Rounding up could make them exceed $k^2$, and then the test could fail even when $\mathrm{OPT} \le T$.
- **Forgetting the guarantee is relative to $T$.** A success at $T$ does not mean $\mathrm{OPT} \le T$. Only a failure carries information about $\mathrm{OPT}$.
- **Placing short jobs anywhere.** A short job must go to a machine of load at most $T$. If it goes to a fuller machine, the bound $T + T/k$ fails.
- **Too fine an $\varepsilon$.** With $k = 10$, the dynamic program has up to $(n + 1)^{91}$ states. The scheme is a theorem about polynomial time, not a fast program.

## Implementations

## History

Hochbaum and Shmoys published the scheme in the Journal of the ACM in 1987, in a paper that introduced dual approximation and also gave fast algorithms with ratios $6/5$ and $7/6$ based on bin packing. Earlier, Graham (1969) had a scheme for a fixed number of machines, and Sahni (1976) an FPTAS for fixed $m$. In 1988 they extended the method to uniform machines. Efficient schemes came later: Hochbaum (1997) by integer programming in fixed dimension, Alon, Azar, Woeginger and Yadid (1998) with linear time for fixed $\varepsilon$, and Jansen (2010) for uniform machines.

## References
