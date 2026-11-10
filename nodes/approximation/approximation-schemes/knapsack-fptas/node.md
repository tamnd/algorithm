---
tag: 8ZRYG2
kind: algorithm
slug: knapsack-fptas
name: Knapsack FPTAS (Ibarra-Kim)
aliases:
- Ibarra-Kim algorithm
- Ibarra-Kim knapsack approximation
- knapsack approximation scheme by profit scaling
area: approximation/approximation-schemes
level: core
summary: Scale the profits down by K = εP/n, round them down, and solve the rounded instance exactly with the profit-indexed dynamic program. The set has profit at least (1 − ε)·OPT, in O(n^3/ε) time.
solves: [knapsack-problem]
model: word-ram
complexity:
  vars: {n: the number of items, ε: "the accuracy parameter, 0 < ε ≤ 1"}
  time: {worst: O(n^3 / ε)}
  space: {extra: O(n^3 / ε)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1975
  people: [Oscar H. Ibarra, Chul E. Kim]
  note: Ibarra and Kim gave the first fully polynomial-time approximation scheme for the 0/1 knapsack problem in 1975.
prereqs: [knapsack-problem, knapsack-dynamic-programming, profit-indexed-dynamic-programming, approximation-ratio]
see_also: [fptas, rounding-and-scaling, subset-sum-fptas, trimming-technique, no-fptas-for-strongly-np-hard-problems, multiple-knapsack-problem, greedy-fractional-knapsack, pseudo-polynomial-time]
sources:
  - paper: doi:10.1145/321906.321909
    title: Oscar H. Ibarra and Chul E. Kim, Fast approximation algorithms for the knapsack and sum of subset problems, Journal of the ACM 22(4), 1975
    locator: pages 463 to 468
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer, 2001
    locator: Chapter 8 (Knapsack), Section 8.2 (an FPTAS for knapsack)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 3, Section 3.1 (the knapsack problem)
  - book: isbn:9783540402862
    title: Hans Kellerer, Ulrich Pferschy and David Pisinger, Knapsack Problems, Springer, 2004
    locator: the chapter on approximation algorithms for the knapsack problem (approximation schemes)
  - paper: doi:10.1287/moor.4.4.339
    title: Eugene L. Lawler, Fast approximation algorithms for knapsack problems, Mathematics of Operations Research 4(4), 1979
    locator: the 0/1 knapsack scheme in O(n log(1/ε) + 1/ε^4) time
---

The knapsack FPTAS of Ibarra and Kim is a [fully polynomial-time approximation scheme](/fptas/) for the [0/1 knapsack problem](/knapsack-problem/). It divides each profit by $K = \varepsilon P / n$, where $P$ is the largest profit, rounds down, and solves the rounded instance exactly with the [profit-indexed dynamic program](/profit-indexed-dynamic-programming/). The returned set has profit at least $(1 - \varepsilon) \cdot \mathrm{OPT}$, and the time is $O(n^3 / \varepsilon)$. It is the standard example of [rounding and scaling](/rounding-and-scaling/).

## In plain words

The exact table method for the knapsack problem can be slow when the profits are large numbers, because the table has one column for each possible total profit. The fix is to make the profits small. Divide every profit by the same number and drop the fraction. The scaled profits are small whole numbers, so the table is small and fast to fill.

Dropping the fractions changes each profit a little. Pick the divisor so that the total change over all items is at most a chosen small part of the largest profit. The best set for the rounded profits is then almost as good as the best set for the true profits. A smaller error part gives a better answer and a larger table.

## The problem

The input is $n$ items with positive integer profits $p_1, \ldots, p_n$ and weights $w_1, \ldots, w_n$, a capacity $W$, and an accuracy parameter $0 < \varepsilon \le 1$. A set $T$ of items is feasible when $w(T) = \sum_{i \in T} w_i \le W$. The task is a feasible set $S$ with

$$
p(S) \ge (1 - \varepsilon) \cdot \mathrm{OPT}, \qquad \mathrm{OPT} = \max \{ p(T) : w(T) \le W \}.
$$

This is a maximization problem, so the ratio is written as $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha = 1 - \varepsilon \le 1$. The guarantee is absolute and holds in the worst case. The lower bound on $\mathrm{OPT}$ that the analysis uses is the largest profit $P$ of an item that fits alone.

## The algorithm

```pseudo id=main
KNAPSACK-FPTAS(p[1 .. N], w[1 .. N], W, ε)        ▷ 0 < ε ≤ 1
L1  I ← the items i with w_i ≤ W; n ← |I|; renumber them 1 .. n
L2  if n = 0 then return ∅
L3  P ← max { p_j : 1 ≤ j ≤ n }
L4  K ← ε·P / n
L5  for j ← 1 to n do p'_j ← ⌊p_j / K⌋
L6  Q ← p'_1 + ... + p'_n; A[0][0] ← 0; A[0][q] ← ∞ for 1 ≤ q ≤ Q
L7  for j ← 1 to n do
L8      for q ← 0 to Q do
L9          A[j][q] ← A[j − 1][q]
L10         if p'_j ≤ q and A[j − 1][q − p'_j] + w_j < A[j][q] then A[j][q] ← A[j − 1][q − p'_j] + w_j
L11 q* ← max { q : A[n][q] ≤ W }
L12 S ← ∅; q ← q*; for j ← n down to 1: if A[j][q] ≠ A[j − 1][q] then S ← S ∪ {j}; q ← q − p'_j
L13 return S
```

Lines L1 and L2 drop the items that cannot be in any feasible set. Without this step, a heavy item could set $P$ and make $K$ too large. Lines L3 to L5 are the scaling. Lines L6 to L10 are the profit-indexed table: $A[j][q]$ is the least weight of a subset of the first $j$ items whose scaled profit is exactly $q$. The exact weight-indexed table of the [knapsack dynamic program](/knapsack-dynamic-programming/) would have $W + 1$ columns. This one has $Q + 1 \le n \lfloor n / \varepsilon \rfloor + 1$ columns, which does not depend on the size of the numbers. Line L11 picks the largest scaled profit that fits, and line L12 recovers a set with that scaled profit.

## Example

Take $n = 6$ items, $W = 15$ and $\varepsilon = 1/2$. The largest profit is $P = 58$, so $K = \varepsilon P / n = 29/6 \approx 4.83$.

| item | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| profit $p_j$ | 56 | 22 | 12 | 45 | 58 | 53 |
| weight $w_j$ | 2 | 7 | 3 | 8 | 9 | 6 |
| $p_j / K$ | 11.59 | 4.55 | 2.48 | 9.31 | 12.00 | 10.97 |
| scaled $p'_j$ | 11 | 4 | 2 | 9 | 12 | 10 |

So $Q = 48$. The table below gives, for each row $j$, the number of columns $q$ with $A[j][q] \le W$, and the largest such $q$ with its weight.

| row $j$ | columns with $A[j][q] \le 15$ | largest such $q$ | $A[j][q]$ there |
|---|---|---|---|
| 0 | 1 | 0 | 0 |
| 1 | 2 | 11 | 2 |
| 2 | 4 | 15 | 9 |
| 3 | 8 | 17 | 12 |
| 4 | 11 | 22 | 13 |
| 5 | 15 | 25 | 14 |
| 6 | 18 | 25 | 14 |

Line L11 gives $q^* = 25$ with weight 14. The trace back skips item 6 (the entry did not change in row 6), takes item 5 ($q$ becomes 13), skips item 4, takes item 3 ($q$ becomes 11), skips item 2 and takes item 1. The result is $S = \{1, 3, 5\}$, with profit $56 + 12 + 58 = 126$ and weight 14.

The optimum is $\{1, 2, 6\}$, with profit $56 + 22 + 53 = 131$ and weight 15. Its scaled profit is also $11 + 4 + 10 = 25$, so the rounding cannot tell the two sets apart, and the table keeps the lighter one. The loss is $131 - 126 = 5$. The proof allows a loss up to $nK = \varepsilon P = 29$, and $126 \ge (1 - 1/2) \cdot 131$ holds with a wide margin.

## Correctness

Three facts give the result. First, by induction on $j$, the entry $A[j][q]$ is the least weight of a subset of the first $j$ items with scaled profit exactly $q$, so $S$ is feasible and has the largest scaled profit $q^*$ of all feasible sets. Second, each item loses less than $K$ in the rounding: $p_j - K < K p'_j \le p_j$. Third, $P \le \mathrm{OPT}$, because the item of profit $P$ fits alone. For an optimal set $O$,

$$
p(S) \ge K p'(S) \ge K p'(O) > p(O) - nK = \mathrm{OPT} - \varepsilon P \ge (1 - \varepsilon)\,\mathrm{OPT}.
$$

The full proof, with the trace back, is in [the correctness proof](proofs/correctness.md).

## Complexity

The analysis is on the [word RAM](/word-ram/), where an addition or a comparison of two input numbers costs $O(1)$.

- **Table size.** Each scaled profit is $p'_j = \lfloor p_j / K \rfloor \le \lfloor P / K \rfloor = \lfloor n / \varepsilon \rfloor$, so $Q \le n \lfloor n / \varepsilon \rfloor$. The table has $(n + 1)(Q + 1)$ entries.
- **Time.** Each entry takes $O(1)$ time, so lines L6 to L10 take $O(n^3 / \varepsilon)$ time in the worst case. The other lines take $O(n)$ time.
- **Space.** The full table takes $O(n^3 / \varepsilon)$ space, which the trace back of line L12 needs. If only the value is needed, one row of $Q + 1$ entries, updated with $q$ from $Q$ down to $p'_j$, is enough, which is $O(n^2 / \varepsilon)$ space.

The time is polynomial in $n$ and in $1 / \varepsilon$, and it does not depend on the size of the profits or of $W$, so this is an [FPTAS](/fptas/). The exact table by capacity takes $\Theta(nW)$ time, which is only [pseudo-polynomial](/pseudo-polynomial-time/).

## Properties

- **Deterministic.** The output depends only on the input.
- **Feasible on each input.** The rounding changes only the profits, never the weights, so the returned set always fits.
- **Exact for a tiny ε.** For $\varepsilon \le 1 / P$, the bound $\mathrm{OPT} - \mathrm{ALG} < \varepsilon P \le 1$ and integer profits give $\mathrm{ALG} = \mathrm{OPT}$, in $O(n^3 P)$ time. This is the conversion behind [the theorem that strongly NP-hard problems have no FPTAS](/no-fptas-for-strongly-np-hard-problems/).

## Variants and improvements

- **A better lower bound, O(n^2/ε) time.** Let $L$ be the value of the greedy 1/2-approximation: the better of the largest profit and the greedy prefix by profit per weight, as on the [fractional knapsack](/greedy-fractional-knapsack/) page. Then $L \le \mathrm{OPT} \le 2L$. Use $K = \varepsilon L / n$. Each feasible set $T$ has $p'(T) \le p(T) / K \le 2L / K = 2n / \varepsilon$, so the table needs only the columns $q \le \lfloor 2n / \varepsilon \rfloor$. The proof above goes through with $L$ in place of $P$. The time becomes $O(n^2 / \varepsilon)$.
- **Large and small items.** Ibarra and Kim treated the items of large profit by the scaled table and added the small items greedily by profit per weight at the end. This, with further work by Lawler (1979), gives time $O(n \log(1/\varepsilon) + 1/\varepsilon^4)$, so the dependence on $n$ is almost linear.
- **Recent bounds.** A line of work lowered the time to $\tilde O(n + (1/\varepsilon)^2)$ (Chen, Lian, Mao and Zhang, 2024), which matches a conditional lower bound based on the hardness of $(\min, +)$-convolution.
- **Trimming instead of scaling.** Keep a list of (weight, profit) pairs and remove pairs whose profit is within a factor $1 + \varepsilon / (2n)$ of a lighter kept pair. This is the [trimming technique](/trimming-technique/) of the [subset sum FPTAS](/subset-sum-fptas/).
- **Other knapsack problems.** The same scaling gives an FPTAS for the [bounded](/bounded-knapsack/) and [unbounded knapsack](/unbounded-knapsack/). For [several knapsacks](/multiple-knapsack-problem/) it fails: there is no FPTAS even for two knapsacks unless P = NP.

## When to use it

Use the FPTAS when the profits are large numbers and an exact answer is not needed, or when a running time that does not depend on the size of the numbers matters. If $nW$ is small, the exact [capacity-indexed dynamic program](/knapsack-dynamic-programming/) is simpler and exact. If the sum of the profits is small, the [profit-indexed dynamic program](/profit-indexed-dynamic-programming/) without scaling is exact in $O(n \sum_j p_j)$ time. For instances from practice, [branch and bound](/knapsack-branch-and-bound/) with the fractional bound often finds the optimum fast, but it has no polynomial worst-case bound.

## Pitfalls

- **Taking P over all items.** If line L1 is missing and $P$ is the profit of an item that does not fit, then $P \le \mathrm{OPT}$ can fail, and the bound $\mathrm{OPT} - \varepsilon P$ says nothing. Line L1 must come before line L3.
- **Rounding up.** With $p'_j = \lceil p_j / K \rceil$ in line L5, the bound $K p'(S) \le p(S)$ in the proof fails, and the set can be worse than the claim. Round down.
- **Reading the profit from the table.** The value $K q^*$ is only a lower bound on $p(S)$. Report $p(S)$, computed with the true profits of the items in $S$.
- **Scaling the weights.** The weights are the constraint. Rounding them can make an infeasible set look feasible. Only the profits, which are the objective, are rounded.
- **Floating point scale.** With a floating point $K$, the computed value of $p_j / K$ has a rounding error, and its floor can be wrong by 1 near an integer. Exact rational arithmetic, or the integer form $p'_j = \lfloor p_j n / (\varepsilon P) \rfloor$ with $\varepsilon$ rational, avoids this.

## Implementations

## History

Ibarra and Kim published the first fully polynomial-time approximation scheme for the 0/1 knapsack problem and for subset sum in the Journal of the ACM in 1975. Lawler (1979) improved the time and the space with a finer treatment of the small items. The simple form on this page, with $K = \varepsilon P / n$ and the profit-indexed table, is the form in Vazirani's book (Section 8.2) and in Williamson and Shmoys (Section 3.1). The knapsack FPTAS was one of the first results that showed that some NP-hard problems can be approximated to any accuracy in time polynomial in $1/\varepsilon$.

## References
