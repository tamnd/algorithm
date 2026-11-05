---
tag: G1Y1GQ
kind: definition
slug: inversion
name: Inversion
aliases:
- out-of-order pair
area: sequences/inversions-and-permutations
level: intro
summary: A pair of positions i<j with a[i]>a[j]; the number of inversions measures disorder.
prereqs: [permutation, total-order]
see_also: [counting-inversions, inversion-table, lehmer-code, expected-number-of-inversions, mahonian-numbers, sorting-by-adjacent-swaps, kendall-tau-distance, permutation-parity]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (inversions, inversion tables and the distribution of the number of inversions)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 2, Problem 2-4 (inversions and the running time of insertion sort)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 5.3 (counting inversions)
---

An inversion of a sequence is a pair of positions that are in the wrong order: an earlier item that is larger than a later item. The number of inversions is the standard measure of how far a sequence is from sorted. It is 0 for a sorted sequence and $n(n-1)/2$ for a strictly decreasing one, and it is the exact number of exchanges that [insertion sort](/insertion-sort/) and [bubble sort](/bubble-sort/) make. The same pairs, counted between two rankings, give the [Kendall tau distance](/kendall-tau-distance/).

## Definition

Let $a = (a_1, \ldots, a_n)$ be a sequence of items from a [total order](/total-order/). An **inversion** of $a$ is a pair of indices $(i, j)$ with

$$1 \le i < j \le n \quad \text{and} \quad a_i > a_j.$$

The **inversion number** of $a$ is $\operatorname{inv}(a) = |\{(i, j) : i < j,\ a_i > a_j\}|$.

For a [permutation](/permutation/) $\pi$ of $[n]$, an inversion is a pair of positions $i < j$ with $\pi(i) > \pi(j)$. Some books list instead the pair of *values* $(\pi(i), \pi(j))$. The two lists have the same length, so $\operatorname{inv}(\pi)$ does not depend on the choice. The test is strict: two equal items never form an inversion.

**Basic facts.** Let $a$ have distinct items.

1. $0 \le \operatorname{inv}(a) \le \binom{n}{2}$. The lower bound is reached exactly when $a$ is increasing, and the upper bound exactly when $a$ is decreasing, because then each of the $\binom n2$ pairs is an inversion.
2. $\operatorname{inv}(\pi^{-1}) = \operatorname{inv}(\pi)$. *Proof.* The map $(i, j) \mapsto (\pi(j), \pi(i))$ sends an inversion of $\pi$ to an inversion of $\pi^{-1}$: from $i < j$ and $\pi(i) > \pi(j)$ we get $\pi(j) < \pi(i)$ and $\pi^{-1}(\pi(j)) = j > i = \pi^{-1}(\pi(i))$. The same rule for $\pi^{-1}$ is its inverse map, so it is a bijection. $\square$
3. An exchange of two adjacent items $a_k, a_{k+1}$ changes $\operatorname{inv}$ by exactly 1: it removes the inversion $(k, k+1)$ if there was one and creates it otherwise. Each other pair keeps its two items in the same order. Hence a sort that exchanges only adjacent out-of-order items makes exactly $\operatorname{inv}(a)$ exchanges, and no sort by adjacent exchanges makes fewer. This is the [sorting by adjacent swaps](/sorting-by-adjacent-swaps/) problem.
4. Let $i < j$ and $a_i > a_j$, and let $m$ be the number of positions $k$ with $i < k < j$ and $a_j < a_k < a_i$. Exchanging $a_i$ and $a_j$ lowers $\operatorname{inv}$ by exactly $2m + 1$. *Proof.* Pairs that do not use position $i$ or $j$ do not change. The pair $(i, j)$ stops being an inversion. A position $k$ outside $[i, j]$ sees the same two values on the same side, so its two pairs give the same total. A position $k$ between $i$ and $j$ with $a_k > a_i$ has the inversion $(k, j)$ before and $(k, j)$ after, and none with $i$; the case $a_k < a_j$ is symmetric. A position with $a_j < a_k < a_i$ has the two inversions $(i, k)$ and $(k, j)$ before and none after. $\square$ So each exchange of two items, adjacent or not, changes the parity of $\operatorname{inv}$. This is the base of the [parity](/permutation-parity/) of a permutation.

## Examples and non-examples

**A permutation.** $\pi = 3\,1\,4\,5\,2$ has the 4 inversions, written as pairs of values, $(3, 1)$, $(3, 2)$, $(4, 2)$ and $(5, 2)$. As pairs of positions they are $(1, 2)$, $(1, 5)$, $(3, 5)$ and $(4, 5)$. Its inverse $2\,5\,1\,3\,4$ also has 4 inversions.

**One exchange.** Exchanging the first and the last item of $3\,1\,4\,5\,2$ gives $2\,1\,4\,5\,3$, with 3 inversions. No item between them has a value strictly between 2 and 3, so $m = 0$ and the count drops by $2 \cdot 0 + 1 = 1$.

**An array.** The array $[5, 1, 4, 2, 8, 0, 3]$ of the [bubble sort](/bubble-sort/) page has 12 inversions, so bubble sort makes 12 exchanges on it.

**Extremes for $n = 5$.** $1\,2\,3\,4\,5$ has 0 inversions and $5\,4\,3\,2\,1$ has $\binom 52 = 10$.

**Repeated keys.** $(2, 2, 1)$ has 2 inversions, $(1, 3)$ and $(2, 3)$ in positions. The pair $(1, 2)$ of the two equal keys is not one. The sequence $(1, 3, 2, 3, 1)$ has 4 inversions.

**Non-examples.**

- A pair $(i, j)$ with $i > j$ is not an inversion even if $a_i < a_j$: each unordered pair of positions is counted once, with its smaller index first.
- A *descent* is a position $i$ with $a_i > a_{i+1}$. Each descent gives an inversion of two adjacent items, but $3\,1\,4\,5\,2$ has only 2 [descents](/descents/) and 4 inversions. The two measures are different.
- An inversion of a sequence is not the inverse of a permutation. The words are close, the ideas are not.

## Related definitions

- **[Counting inversions](/counting-inversions/).** The problem of computing $\operatorname{inv}(a)$, which takes $\Theta(n \log n)$ comparisons and is solved by a modified [merge sort](/inversion-count-by-merge-sort/) or by a [Fenwick tree](/inversion-count-with-fenwick-tree/).
- **[Inversion table](/inversion-table/) and [Lehmer code](/lehmer-code/).** Two ways to list the inversions item by item. Each gives a bijection from $S_n$ to the sequences $(c_1, \ldots, c_n)$ with $0 \le c_i \le n - i$, and the sum of the entries is $\operatorname{inv}(\pi)$.
- **[Mahonian numbers](/mahonian-numbers/).** The number of permutations of $[n]$ with exactly $k$ inversions.
- **[Expected number of inversions](/expected-number-of-inversions/).** A uniform random permutation has $n(n-1)/4$ inversions on average, which is why insertion sort is quadratic on average.
- **[Kendall tau distance](/kendall-tau-distance/).** The number of pairs that two rankings order differently, which is $\operatorname{inv}$ of one ranking read in the order of the other.
- **[Measures of presortedness](/presortedness/).** $\operatorname{inv}$ is one measure of disorder among several, with runs, removals and exchanges.
- **[Parity](/permutation-parity/).** A permutation is even or odd according to the parity of $\operatorname{inv}(\pi)$.

## References
