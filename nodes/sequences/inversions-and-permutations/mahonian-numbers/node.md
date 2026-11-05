---
tag: PNASTV
kind: concept
slug: mahonian-numbers
name: Mahonian numbers
aliases:
- inversion-count distribution
area: sequences/inversions-and-permutations
level: core
summary: Number of permutations of n with exactly k inversions.
prereqs: [inversion, lehmer-code]
see_also: [expected-number-of-inversions, descents, eulerian-numbers, inversion-table, kendall-tau-distance, sorting-by-adjacent-swaps, integer-partitions, polynomial-multiplication]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (the number of permutations with k inversions, the generating function as a product, and the table of these numbers)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Sections 1.3 and 1.4 (the inversion generating function, the major index and their equidistribution)
---

The Mahonian number $M(n, k)$ is the number of [permutations](/permutation/) of $[n]$ with exactly $k$ [inversions](/inversion/). Its generating function is the product $\prod_{j=1}^{n} (1 + z + \cdots + z^{j-1})$, because the [Lehmer code](/lehmer-code/) splits a permutation into independent digits, one per factor. The numbers are symmetric, unimodal, and concentrated around $n(n-1)/4$, and a sliding-window recurrence computes the whole table up to $k = K$ in $O(nK)$ time. They are named after Percy MacMahon, who proved that the major index of [descents](/descents/) has the same distribution.

## In plain words

Arrange the numbers 1 to $n$ in every possible order and, for each order, count the pairs that are out of order. How many orders have exactly 3 such pairs? Or exactly 10? The table of these counts is the Mahonian table.

There is a simple way to build it. Each number in the list contributes some count of smaller numbers after it, and these counts can be chosen freely: the first number can have any count from 0 up to $n - 1$, the next from 0 up to $n - 2$, and so on. So the question becomes: in how many ways can you choose such counts that add up to a given total? Each row of the table follows from the row before by adding up a window of neighboring entries.

## The idea

**Definition.** For $n \ge 0$ and $k \ge 0$,
$$M(n, k) = |\{\pi \in S_n : \operatorname{inv}(\pi) = k\}|.$$
It is nonzero exactly for $0 \le k \le \binom n2$, and $\sum_k M(n, k) = n!$.

**Generating function.** By the Lehmer code bijection, $\pi \mapsto (c_1, \ldots, c_n)$ with $0 \le c_i \le n - i$ and $\operatorname{inv}(\pi) = c_1 + \cdots + c_n$. So $M(n, k)$ is the number of such sequences with sum $k$, and
$$\sum_{k} M(n, k)\, z^k = \prod_{j=1}^{n} \big(1 + z + \cdots + z^{j-1}\big) = \prod_{j=1}^{n} \frac{1 - z^j}{1 - z}.$$
This is the $q$-analogue of $n!$, often written $[n]_q!$. The same product counts the permutations by their major index, the sum of their descent positions: MacMahon's theorem says $\operatorname{inv}$ and $\operatorname{maj}$ are equidistributed.

**Recurrence.** Choosing the first digit $c_1 = i$ leaves a code of length $n - 1$, so
$$M(n, k) = \sum_{i=0}^{\min(k, n-1)} M(n-1, k-i), \qquad M(0, 0) = 1.$$
Neighboring sums share all but two terms, which gives the sliding-window form
$$M(n, k) = M(n, k-1) + M(n-1, k) - M(n-1, k-n),$$
with entries of negative index taken as 0.

```pseudo
MAHONIAN-TABLE(N, K)                     ▷ M[n][k] for 0 ≤ n ≤ N, 0 ≤ k ≤ K
1  M[0][0] ← 1, M[0][k] ← 0 for 1 ≤ k ≤ K
2  for n ← 1 to N do
3      for k ← 0 to K do
4          M[n][k] ← M[n−1][k]
5          if k ≥ 1 then M[n][k] ← M[n][k] + M[n][k−1]
6          if k ≥ n then M[n][k] ← M[n][k] − M[n−1][k−n]
7  return M
```

This takes $O(NK)$ arithmetic operations and, keeping two rows, $O(K)$ space. A full row has $\binom n2 + 1$ entries, so the recurrence spends $\Theta(n^3)$ operations on it. The row is also the product of $n$ polynomials, and multiplying them in a balanced tree with fast [polynomial multiplication](/polynomial-multiplication/) takes $O(n^2 \log^2 n)$ arithmetic operations.

**Shape.**

- **Symmetry.** $M(n, k) = M(n, \binom n2 - k)$, by reversing the permutation, which turns every non-inversion into an inversion.
- **Small $k$.** $M(n, 1) = n - 1$, $M(n, 2) = (n-2)(n+1)/2$ for $n \ge 2$, and $M(n, 3) = n(n^2 - 7)/6$ for $n \ge 3$.
- **Unimodality.** Each row increases up to the middle and then decreases, since it is a product of symmetric unimodal polynomials with nonnegative coefficients.
- **Moments and limit.** The mean is $n(n-1)/4$ and the variance $n(n-1)(2n+5)/72$, see the [expected number of inversions](/expected-number-of-inversions/). The independent digits give a central limit theorem: a row, scaled, approaches the normal curve.
- **Partitions.** For $k \le n$ the factors $1 - z^j$ with $j > n$ do not change the coefficient of $z^k$, so $M(n, k)$ is the coefficient of $z^k$ in $\prod_{j \ge 1} (1 - z^j) / (1 - z)^n$, a formula in terms of [integer partitions](/integer-partitions/) and Euler's pentagonal numbers.

## Examples

**Small rows.**

| $n$ | $M(n, 0), M(n, 1), \ldots$ |
| --- | --- |
| 1 | 1 |
| 2 | 1, 1 |
| 3 | 1, 2, 2, 1 |
| 4 | 1, 3, 5, 6, 5, 3, 1 |
| 5 | 1, 4, 9, 15, 20, 22, 20, 15, 9, 4, 1 |
| 6 | 1, 5, 14, 29, 49, 71, 90, 101, 101, 90, 71, 49, 29, 14, 5, 1 |

**$n = 3$ by hand.** $123$ has 0 inversions, $132$ and $213$ have 1, $231$ and $312$ have 2, and $321$ has 3, which is the row $1, 2, 2, 1$. The product is $(1)(1 + z)(1 + z + z^2) = 1 + 2z + 2z^2 + z^3$.

**One window.** $M(5, 4) = M(4, 0) + M(4, 1) + M(4, 2) + M(4, 3) + M(4, 4) = 1 + 3 + 5 + 6 + 5 = 20$, and the sliding form gives the same: $M(5, 4) = M(5, 3) + M(4, 4) - M(4, -1) = 15 + 5 - 0$.

**The middle.** The largest entries of the rows for $n = 5, 6, 7$ are $22$, $101$ and $573$. Out of $5040$ permutations of 7 items, $573$, about $11\%$, have exactly 10 inversions, and the same number have 11.

## Where it is used

- **Counting permutations with $k$ inversions.** A standard dynamic programming problem, often asked modulo a prime, solved by the sliding-window recurrence.
- **Exact distribution of the Kendall statistic.** The number of discordant pairs between a random ranking and a fixed one has the distribution $M(n, k)/n!$, which gives exact p-values of the [Kendall tau](/kendall-tau-distance/) test for small $n$.
- **Analysis of sorting.** The number of exchanges of [bubble sort](/bubble-sort/) and of moves of [insertion sort](/insertion-sort/) is the inversion count, and its exact distribution on random inputs is the Mahonian row. The cost of [sorting by adjacent swaps](/sorting-by-adjacent-swaps/) is the same.
- **Combinatorics.** The $q$-factorial and the $q$-binomial coefficients built from it count inversions of words with repeated letters, and the equidistribution of $\operatorname{inv}$ and $\operatorname{maj}$ is the start of the theory of Mahonian statistics.

## References
