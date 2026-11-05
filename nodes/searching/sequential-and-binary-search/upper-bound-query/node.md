---
tag: XM2DVW
kind: problem
slug: upper-bound-query
name: Upper bound query
aliases:
- bisect right
- first element greater than a key
area: searching/sequential-and-binary-search
level: core
summary: Return the first position in a sorted array whose value is greater than the key.
model: comparison-model
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(log n)}
prereqs: [lower-bound-query]
see_also: [lower-bound-query, lower-and-upper-bound-search, first-and-last-occurrence, binary-search, predecessor-problem, stable-sort, insertion-sort, search-in-sorted-array]
sources:
  - url: https://docs.python.org/3/library/bisect.html
    title: Python Software Foundation, bisect, Array bisection algorithm
    note: bisect_right returns the upper bound
  - url: https://en.cppreference.com/w/cpp/algorithm/upper_bound
    title: cppreference.com, std::upper_bound
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an ordered table
---

An upper bound query asks, for a sorted array $A[0 \ldots n-1]$ and a key $x$, for the first index $u$ with $A[u] > x$, or $n$ when no item is greater than $x$. The answer is the number of items that are less than or equal to $x$, and it is the last place where $x$ can be inserted with the array still sorted. It is the mirror of the [lower bound query](/lower-bound-query/): the two answers differ exactly when $x$ is in the array, and their difference is the number of copies of $x$. A binary search answers it with at most $\lceil \lg(n+1) \rceil$ two-way comparisons, which is optimal; Python calls it `bisect_right` and C++ `std::upper_bound`.

## In plain words

You have a row of numbers in increasing order, and a new number. You want the position just after the last copy of the new number in the row, or the place where it would go if it is not there. In other words, you count the numbers in the row that are smaller than the new number or equal to it.

The lower bound puts a new copy in front of the old copies. The upper bound puts it behind them. When people stand in a queue sorted by arrival time and someone new comes with the same time as others, the upper bound puts the new person after the ones who came first.

## Definition

**Input.** An array $A[0 \ldots n-1]$ with $n \ge 0$ items from a [total order](/total-order/), with $A[0] \le \cdots \le A[n-1]$, and a key $x$.

**Output.** The index

$$ u(A, x) = \min\bigl(\{\, i \in \{0, \ldots, n-1\} : A[i] > x \,\} \cup \{n\}\bigr). $$

Equivalently, $u$ is the unique value in $\{0, \ldots, n\}$ with $A[i] \le x$ for each $i < u$ and $A[i] > x$ for each $i \ge u$. So $u(A, x) = |\{\, i : A[i] \le x \,\}|$.

**Relation to the lower bound.** Let $\ell = \ell(A, x)$ be the lower bound. Then $\ell \le u$, the indices of the copies of $x$ are exactly $\ell, \ell + 1, \ldots, u - 1$, and

$$ u(A, x) - \ell(A, x) = |\{\, i : A[i] = x \,\}|. $$

*Proof.* An index $i$ has $A[i] < x$, $A[i] = x$ or $A[i] > x$. The first set is $\{0, \ldots, \ell - 1\}$ and the union of the first two is $\{0, \ldots, u - 1\}$, by the two definitions. So the second set is $\{\ell, \ldots, u - 1\}$, and its size is $u - \ell$. $\blacksquare$

## Variants

- **Last occurrence.** When $x$ is present, its last index is $u - 1$. See [first and last occurrence](/first-and-last-occurrence/).
- **Equal range.** Return the pair $(\ell, u)$ in one call, as `std::equal_range` does. The two searches can share the first steps, until the middle item is equal to $x$.
- **Floor.** The largest item that is at most $x$ is $A[u - 1]$ when $u > 0$. The smallest item greater than $x$ (the strict successor) is $A[u]$ when $u < n$.
- **With a comparator or a predicate.** As for the lower bound, any strict weak order works, if $A$ is sorted by the same order. The upper bound is the partition point of the test $P(y) = \lnot(x < y)$.

## Examples

The array is $A = [1, 3, 3, 3, 5, 8, 8, 13]$, with $n = 8$.

| $x$ | 0 | 1 | 3 | 4 | 8 | 13 | 20 |
|---|---|---|---|---|---|---|---|
| lower bound $\ell$ | 0 | 0 | 1 | 4 | 5 | 7 | 8 |
| upper bound $u$ | 0 | 1 | 4 | 4 | 7 | 8 | 8 |
| copies, $u - \ell$ | 0 | 1 | 3 | 0 | 2 | 1 | 0 |

- $x = 3$: the copies are at indices 1, 2 and 3, so $u = 4$ and the last copy is at $u - 1 = 3$.
- $x = 4$: absent, so $\ell = u = 4$.
- $x = 13$: the last item, so $u = n = 8$.

## Known algorithms

- **[Lower and upper bound search](/lower-and-upper-bound-search/).** The binary search on the test $A[mid] \le x$, with the half-open range $[lo, hi)$. At most $\lceil \lg(n+1) \rceil$ two-way comparisons and $\Theta(1)$ space.
- **[Branchless binary search](/branchless-binary-search/)** and the **[Eytzinger layout](/eytzinger-layout/)**, with the same test.
- **[Exponential search](/exponential-search/).** $O(\log u)$ comparisons, good when the answer is near the start.
- **[Linear search](/linear-search/).** Scan for the first $A[i] > x$, with $u + 1$ comparisons, or $n$ when $u = n$.

## Bounds

The worst-case cost is exactly $\lceil \lg(n+1) \rceil$ two-way comparisons. The upper bound is the binary search above. The lower bound is the same counting argument as for the [lower bound query](/lower-bound-query/): on $A = [2, 4, \ldots, 2n]$, the $n + 1$ keys $0, 2, 4, \ldots, 2n$ have the $n + 1$ different answers $0, 1, \ldots, n$, so a decision tree with two-way comparisons needs at least $n + 1$ leaves and so height at least $\lceil \lg(n+1) \rceil$.

## Reductions

- **For integer keys it is a lower bound query:** $u(A, x) = \ell(A, x + 1)$, because $A[i] > x$ if and only if $A[i] \ge x + 1$. This fails for real numbers and strings, where $x$ has no next value.
- **For any keys it is a lower bound query with the reverse order.** Let $R$ be $A$ reversed, which is sorted for the order $\ge$. The lower bound of $x$ in $R$ for that order, the first $j$ with $R[j] \le x$, is $j = n - u$.
- **Counting reduces to it.** The number of items in the closed range $[a, b]$ is $u(A, b) - \ell(A, a)$.

## Applications

- **Stable insertion.** Inserting each new item at its upper bound keeps equal items in their order of arrival. So the binary variant of [insertion sort](/insertion-sort/) is a [stable sort](/stable-sort/) when it inserts at the upper bound, and not stable when it inserts at the lower bound.
- **Counting copies** of a value in a sorted list with $u - \ell$.
- **Bucketing.** With sorted bucket edges $e_0 < e_1 < \cdots$, the bucket of a value $v$ is $u(e, v) - 1$, the last edge at most $v$. This finds the interval of a value in a histogram or a piecewise function.
- **Sampling from a discrete distribution.** With the prefix sums $c_0 \le c_1 \le \cdots$ of the weights and a uniform $r \in [0, c_{n-1})$, the item $u(c, r)$ is chosen with probability proportional to its weight.

## References
