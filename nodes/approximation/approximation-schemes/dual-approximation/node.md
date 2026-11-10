---
tag: DPDS4B
kind: technique
slug: dual-approximation
name: Dual approximation framework
aliases:
- Dual approximation
- Hochbaum-Shmoys dual approximation
- dual approximation framework
- rho-dual algorithm
area: approximation/approximation-schemes
level: advanced
summary: Guess a target value T and either find a solution within a factor of T or certify that none of value T exists, then binary search on T.
prereqs: [approximation-ratio, binary-search, makespan-minimization]
see_also: [hochbaum-shmoys-makespan-ptas, hochbaum-shmoys-ptas, uniform-machine-scheduling, lenstra-shmoys-tardos, k-center-problem, gonzalez-k-center, binary-search-on-answer, bin-packing]
sources:
  - paper: "D. S. Hochbaum and D. B. Shmoys, Using dual approximation algorithms for scheduling problems: theoretical and practical results, Journal of the ACM 34(1), 1987, pp. 144-162"
    title: Hochbaum and Shmoys 1987
    locator: the definition of a dual approximation algorithm and the binary search
  - paper: "D. S. Hochbaum and D. B. Shmoys, A best possible heuristic for the k-center problem, Mathematics of Operations Research 10(2), 1985, pp. 180-184"
    title: Hochbaum and Shmoys 1985
    locator: the 2-approximation for k-center by a test on each candidate radius
  - paper: "D. S. Hochbaum and D. B. Shmoys, A unified approach to approximation algorithms for bottleneck problems, Journal of the ACM 33(3), 1986, pp. 533-550"
    title: Hochbaum and Shmoys 1986
    locator: bottleneck problems solved by a test on the graph of short edges
  - paper: "D. S. Hochbaum and D. B. Shmoys, A polynomial approximation scheme for scheduling on uniform processors: using the dual approximation approach, SIAM Journal on Computing 17(3), 1988, pp. 539-551"
    title: Hochbaum and Shmoys 1988
    locator: the PTAS for uniform machines
  - paper: "J. K. Lenstra, D. B. Shmoys and E. Tardos, Approximation algorithms for scheduling unrelated parallel machines, Mathematical Programming 46, 1990, pp. 259-271"
    title: Lenstra, Shmoys and Tardos 1990
    locator: the LP test for a deadline T and the binary search
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.2 (k-center) and Section 3.2 (identical parallel machines)
---

The dual approximation framework turns a weak test into an [approximation algorithm](/approximation-ratio/). A *$\rho$-dual algorithm* gets a target value $T$ and either returns a solution of value at most $\rho T$, or answers NO, and it may answer NO only when no solution of value $T$ or less exists. A [binary search](/binary-search/) over $T$ then gives a $\rho$-approximation. Hochbaum and Shmoys introduced the name in 1987 for scheduling, where the test asks "do the jobs fit by time $T$ if each machine may run a little late?", and it is the base of the [makespan PTAS](/hochbaum-shmoys-makespan-ptas/).

## In plain words

Some problems are easier to answer as a yes or no question with a goal. Instead of "what is the best finishing time?", ask "can we finish by this time?" The dual method allows a loose answer to that question. If the answer is yes, you must show a plan that finishes a little late, for example within twice the time. If the answer is no, you must be right: no plan finishes in time.

Such a loose test is enough. Try a goal in the middle of the possible range. A yes means the best goal is at most this one, so search lower. A no means the best goal is higher, so search higher. At the end you have a goal that is at most the best possible, and a plan that is only a little worse than that goal.

## When it applies

The method applies to a minimization problem with these properties.

- **A search range.** $\mathrm{OPT}$ lies in a known sorted finite set $C$ of candidates, for example the integers from a lower bound $LB$ to an upper bound $UB$, or the $O(n^2)$ pairwise distances of a point set.
- **A relaxed test.** For each $T \in C$ there is a $\rho$-dual test. "Dual" refers to the role of the two parts of the problem: the test keeps the *objective* exact (value $T$), but it may break the *constraint* (machine capacity, radius) by the factor $\rho$. A NO must be a proof that $\mathrm{OPT} > T$.
- **Monotone feasibility.** If a solution of value $T$ exists, then one of value $T'$ exists for each $T' \ge T$. This holds when "value at most $T$" is the condition.

It does not need the test to be monotone. A test may accept $T$ and reject a larger $T'$; this can happen only for $T' < \mathrm{OPT}$, and the search handles it.

## The template

```pseudo id=template
DUAL-SEARCH(C[0 .. N − 1], TEST)                       ▷ C sorted, OPT ∈ C
L1  lo ← −1; hi ← N − 1                                 ▷ OPT > C[lo] (no bound when lo = −1), OPT ≤ C[hi]
L2  S ← TEST(C[hi])                                     ▷ accepts, since OPT ≤ C[hi]
L3  while hi − lo > 1:
L4      mid ← ⌊(lo + hi)/2⌋; S' ← TEST(C[mid])
L5      if S' = NO then lo ← mid                        ▷ OPT > C[mid]
L6      else hi ← mid; S ← S'                           ▷ value(S') ≤ ρ·C[mid]
L7  return S
```

**Theorem.** Let TEST be a $\rho$-dual algorithm for a minimization problem, and let $C$ be a sorted set of $N$ values with $\mathrm{OPT} \in C$. Then DUAL-SEARCH returns a solution of value at most $\rho \cdot \mathrm{OPT}$ and calls TEST at most $1 + \lceil \log_2 N \rceil$ times.

*Proof.* We show the invariant of the loop of lines L3 to L6: (i) $lo = -1$ or $\mathrm{OPT} > C[lo]$, and (ii) $S$ is a solution of value at most $\rho \cdot C[hi]$.

1. *Initialization.* $C[N-1]$ is the largest candidate and $\mathrm{OPT} \in C$, so $\mathrm{OPT} \le C[N - 1]$. A test may answer NO only when $\mathrm{OPT} > T$, so line L2 returns a solution $S$, of value at most $\rho \cdot C[hi]$ by the definition of a $\rho$-dual test. Part (i) holds because $lo = -1$.
2. *Maintenance.* Line L4 gives $lo < mid < hi$. If TEST answers NO for $C[mid]$, then $\mathrm{OPT} > C[mid]$, so the update of line L5 keeps (i), and $hi$ and $S$ do not change. If it returns $S'$, then $S'$ has value at most $\rho \cdot C[mid]$, so line L6 keeps (ii), and $lo$ does not change.
3. *Termination.* The gap $hi - lo$ is an integer that becomes $\lceil (hi - lo)/2 \rceil$ or $\lfloor (hi - lo)/2 \rfloor$ in each step. It starts at $N$, so after at most $\lceil \log_2 N \rceil$ steps it is 1.

At the end $hi = lo + 1$. If $lo \ge 0$, then $\mathrm{OPT} > C[lo]$, and since $\mathrm{OPT} \in C$ and $C$ is sorted, $\mathrm{OPT} \ge C[lo + 1] = C[hi]$. If $lo = -1$, then $hi = 0$ and $C[0]$ is the least candidate, so again $C[hi] \le \mathrm{OPT}$. So $S$ has value at most $\rho \cdot C[hi] \le \rho \cdot \mathrm{OPT}$. $\blacksquare$

The target that the search ends with is a lower bound on $\mathrm{OPT}$. So the algorithm reports both a solution and a certificate of how good it is: the ratio of its value to $C[hi]$ is at most $\rho$.

When $\mathrm{OPT}$ is a real number with no finite candidate set, search over $T$ on a geometric grid: if $LB \le \mathrm{OPT} \le UB$, test the values $LB (1 + \delta)^i$. The same proof gives a solution of value at most $\rho (1 + \delta)\,\mathrm{OPT}$ after $O\bigl(\log (\log(UB/LB) / \log(1 + \delta))\bigr)$ tests.

## Classic examples

### Makespan with a 2-dual test

For [makespan minimization](/makespan-minimization/) on $m$ identical machines, the test for $T$ answers NO if $\max_j p_j > T$ or $\sum_j p_j > m T$. Both are proofs that $\mathrm{OPT} > T$. Else it puts each job on a least loaded machine. When the last job $j$ of the fullest machine arrives, that machine has load at most $(\sum_i p_i - p_j)/m \le T$, so the makespan is at most $2T$. The candidates are the integers from $LB = \max(\max_j p_j, \lceil \sum_j p_j / m \rceil)$ to $2LB$.

Take $p = (5, 4, 3, 3, 3)$ and $m = 2$. Then $LB = \max(5, 9) = 9$ and $C = (9, 10, \ldots, 18)$. The test at $T = 8$ answers NO, because $18 > 2 \cdot 8$.

| call | $T$ | answer | $lo, hi$ after the call (as values) |
|---|---|---|---|
| 1 | 18 | loads 8 and 10 | none, 18 |
| 2 | 13 | loads 8 and 10 | none, 13 |
| 3 | 10 | loads 8 and 10 | none, 10 |
| 4 | 9 | loads 8 and 10 | none, 9 |

The search ends with $T = 9 \le \mathrm{OPT}$ and a schedule of makespan 10. Here $\mathrm{OPT} = 9$, by $\{5, 4\}$ and $\{3, 3, 3\}$.

### The makespan PTAS

The [Hochbaum-Shmoys scheme](/hochbaum-shmoys-makespan-ptas/) is a $(1 + \varepsilon)$-dual test: it rounds the jobs larger than $\varepsilon T$, packs them exactly by dynamic programming, and adds the small jobs greedily. With the theorem above it is a PTAS for $P \mid\mid C_{\max}$. The same method gives a PTAS for [uniform machines](/uniform-machine-scheduling/) (Hochbaum and Shmoys 1988).

### k-center with a 2-dual test

In the [k-center problem](/k-center-problem/), the input is a metric on $n$ points and an integer $k$; the goal is $k$ centers among the points that make the largest distance to the nearest center as small as possible. $\mathrm{OPT}$ is one of the pairwise distances, so these are the candidates. The test for $r$ scans the points and takes a point as a new center when it is more than $2r$ from each center so far. If it takes more than $k$ centers, it answers NO: the chosen points are pairwise more than $2r$ apart, so no ball of radius $r$ holds two of them, and $k$ balls of radius $r$ cannot cover them. Else each point is within $2r$ of a center. This is the 2-approximation of Hochbaum and Shmoys (1985). No ratio $2 - \varepsilon$ is possible unless P = NP (see [k-center hardness](/k-center-hardness/)), so this example is tight for the problem.

Take the points $0, 1, 2, 10, 11, 20$ on a line and $k = 2$. The distinct distances are $0, 1, 2, 8, 9, 10, 11, 18, 19, 20$. At $r = 2$ the test takes $0$, $10$ and $20$ and answers NO, so $\mathrm{OPT} > 2$. The search makes 5 calls and ends at $r = 8$ with the centers $0$ and $20$, of radius $10 \le 2 \cdot 8$. The optimum is 9, with the centers $0$ and $11$.

### Unrelated machines

Lenstra, Shmoys and Tardos (1990) use a test for $R \mid\mid C_{\max}$: for a deadline $T$, solve the assignment LP with only the pairs with $p_{ij} \le T$. If the LP is infeasible, $\mathrm{OPT} > T$. Else a vertex of the LP rounds to a schedule of makespan at most $2T$. The search then gives the [2-approximation](/lenstra-shmoys-tardos/).

## Variations

- **Relaxed constraint versus relaxed objective.** In the bin packing view of Hochbaum and Shmoys, a $\rho$-dual algorithm uses at most $\mathrm{OPT}$ bins but may fill each bin up to $\rho$. A normal $\rho$-approximation keeps the bins at size 1 and may use $\rho\,\mathrm{OPT}$ bins. The makespan problem with deadline $T$ is the same as bin packing with $m$ bins of size $T$, so a dual algorithm for one is a primal algorithm for the other.
- **Bottleneck problems.** Many problems of the form "minimize the largest edge used" have a candidate set of edge weights and a test on the graph of the edges of weight at most $r$. Hochbaum and Shmoys treat k-center and several relatives in this way.
- **Parametric search.** When the test is a combinatorial algorithm whose control flow depends on $T$ only through comparisons, Megiddo's parametric search can find the critical $T$ without a numeric binary search. This is a different tool with the same aim.
- **The search as a certificate.** The final pair (a rejected value just below an accepted one) gives an a posteriori bound, which is often much better than $\rho$.

## Pitfalls

- **A NO must be a proof.** If the test may fail on some $T \ge \mathrm{OPT}$, for example because a heuristic does not find a solution, the search can move above $\mathrm{OPT}$ and the ratio is lost.
- **The candidate set must contain OPT.** If $\mathrm{OPT}$ is not in $C$, the final target can be above $\mathrm{OPT}$. For k-center with centers anywhere in the plane, the pairwise distances are not the right candidates.
- **Do not assume monotone answers.** A $\rho$-dual test may accept $T$ and reject some $T' > T$, when both are below $\mathrm{OPT}$. Code that stops at the first NO after a YES, or that reuses old answers as if they were monotone, is wrong. The proof above uses only the two guarantees of the test.
- **Count the calls.** A binary search over integers up to $\sum_j p_j$ needs $O(\log \sum_j p_j)$ calls, which is polynomial in the input length but not in $n$ alone. A search over the integers $[LB, 2LB]$ is shorter.

## Exercises

1. Show that the makespan test of the first example gives a $(2 - 1/m)$-approximation, not only 2, when it puts each job on a least loaded machine.
2. Give a 3-dual test for the k-supplier problem, where the centers must be chosen from a set of suppliers that is different from the set of clients.
3. Prove that a $\rho$-dual algorithm for bin packing (at most $\mathrm{OPT}$ bins of size $\rho$) gives, by binary search over the bin size, a $\rho$-approximation for $P \mid\mid C_{\max}$.
4. Find a $\rho$-dual test and an input where the test accepts $T$ and rejects $T + 1$.
5. Show that the k-center problem with $k$ given and points in a general metric has no $(2 - \varepsilon)$-dual test that runs in polynomial time, unless P = NP.

## References
