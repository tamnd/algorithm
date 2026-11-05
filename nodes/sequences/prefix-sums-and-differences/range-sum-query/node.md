---
tag: KF2CAQ
kind: problem
slug: range-sum-query
name: Range sum query
aliases:
- interval sum query
- range sum
- static range sum
- subarray sum query
area: sequences/prefix-sums-and-differences
level: intro
summary: Given a static array, answer many queries for the sum of a contiguous range.
prereqs: [array, range-query-problem]
see_also: [prefix-sums, point-update-range-sum-query, range-sum-query-2d, range-minimum-query, sparse-table, fenwick-tree, partial-sums-problem, subarray]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 9, Range queries, Section 9.1 Static array queries (sum queries with a prefix sum array, and why minimum queries need another method)
  - paper: doi:10.1145/800070.802185
    title: "Andrew C. Yao, Space-time tradeoff for answering range queries (extended abstract), Proceedings of the 14th Annual ACM Symposium on Theory of Computing (STOC 1982), 128-136"
    locator: the one-dimensional case over a semigroup (query cost about the inverse Ackermann function with linear space)
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Algorithm Design Techniques, Section 8.2 (the cumulative array that gives the sum of any subvector in constant time)
---

The range sum query problem gives an [array](/array/) $a[0 \ldots n-1]$ that does not change, and asks for the sum $a[l] + a[l+1] + \cdots + a[r]$ for many ranges $[l, r]$. It is the simplest case of the [range query problem](/range-query-problem/). Since addition can be undone by subtraction, the [prefix sums](/prefix-sums/) of the array answer each query with one subtraction, after $\Theta(n)$ preprocessing, so the problem is solved in $\Theta(n + q)$ time for $q$ queries. The problem becomes harder when the array changes, which is the [point update range sum query](/point-update-range-sum-query/), or when the operation has no inverse, as for the [range minimum query](/range-minimum-query/).

## In plain words

You have a long list of numbers that never changes, such as the rainfall of each day of a year. People ask questions like "how much rain fell from day 40 to day 75?". You could add up the days each time, but with many questions and long ranges that is slow.

The problem asks how to prepare the list once so that each question is fast. The standard answer keeps a running total for each day. The total of a range is then the running total at its last day minus the running total just before its first day: one subtraction, however long the range is.

## Definition

**Input.** An array $a[0 \ldots n-1]$ of elements of an abelian group $(G, +, 0)$, usually integers or integers modulo $2^{w}$, followed by $q$ queries $(l_j, r_j)$ with $0 \le l_j \le r_j \le n - 1$.

**Output.** For each query $j$, the value

$$S(l_j, r_j) = \sum_{i = l_j}^{r_j} a[i].$$

**Cost.** A solution has a preprocessing phase that sees only $a$, with time $p(n)$ and space $s(n)$, and then answers each query in time $t(n)$. The total time is $p(n) + q\,t(n)$. In the *online* form each query must be answered before the next one is read; in the *offline* form all queries are known in advance.

## Variants

- **Half-open ranges.** Many programs use $[l, r)$ with $0 \le l \le r \le n$. The empty range $l = r$ has sum 0.
- **Other groups.** XOR, sums modulo $m$, and vector sums (for example, counts of each letter) work the same way, because each has an inverse.
- **Semigroup operations.** For $\min$, $\max$, $\gcd$ or matrix products, there is no subtraction. This is the [range minimum query](/range-minimum-query/) and its relatives, solved by a [sparse table](/sparse-table/) or a [disjoint sparse table](/disjoint-sparse-table/).
- **Dynamic.** Point updates mix with the queries. This is the [point update range sum query](/point-update-range-sum-query/), and with prefix queries only, the [partial sums problem](/partial-sums-problem/). Range additions with point reads are the [range update point query](/range-update-point-query/).
- **Two and more dimensions.** Rectangle sums in a grid, see the [two-dimensional range sum query](/range-sum-query-2d/).
- **Windows of fixed length.** All $n - k + 1$ sums of length-$k$ ranges, as in the [maximum sum subarray of fixed length](/maximum-sum-subarray-of-fixed-length/).
- **Search by sum.** Find the largest $r$ with $S(l, r) \le s$ for non-negative items. With prefix sums, this is a [binary search](/binary-search/) on the sorted prefix sums, $O(\log n)$ per query.

## Examples

Let $a = [-2, 0, 3, -5, 2, -1]$. The prefix sums with $P[0] = 0$ are $P = [0, -2, -2, 1, -4, -2, -3]$, and $S(l, r) = P[r+1] - P[l]$.

| query $(l, r)$ | items | answer | from the prefix sums |
|---|---|---|---|
| $(0, 2)$ | $-2, 0, 3$ | $1$ | $P[3] - P[0] = 1 - 0$ |
| $(2, 5)$ | $3, -5, 2, -1$ | $-1$ | $P[6] - P[2] = -3 - (-2)$ |
| $(0, 5)$ | the whole array | $-3$ | $P[6] - P[0] = -3 - 0$ |
| $(3, 3)$ | $-5$ | $-5$ | $P[4] - P[3] = -4 - 1$ |

A non-example: the same table does not give the range *minimum*. The prefix minima of $a$ are $[-2, -2, -2, -5, -5, -5]$, and the minimum of $a[4 \ldots 5] = [2, -1]$, which is $-1$, cannot be found from them.

## Known algorithms

| method | preprocessing | query | space | operations |
|---|---|---|---|---|
| direct sum | none | $O(r - l + 1)$ | $O(1)$ extra | any |
| [prefix sums](/prefix-sums/) | $\Theta(n)$ | $O(1)$ | $n + 1$ | needs an inverse |
| table of all answers | $\Theta(n^2)$ | $O(1)$ | $\Theta(n^2)$ | any |
| [sparse table](/sparse-table/) (disjoint form) | $\Theta(n \log n)$ | $O(1)$ | $\Theta(n \log n)$ | any associative operation |
| [Fenwick tree](/fenwick-tree/) | $\Theta(n)$ | $O(\log n)$ | $n$ | needs an inverse, allows updates |
| [segment tree](/segment-tree/) | $\Theta(n)$ | $O(\log n)$ | $\le 4n$ | any associative operation, allows updates |

All bounds are worst case on a [word RAM](/word-ram/) with each item and each sum in one word. For a static array with an inverse, prefix sums dominate every other line of the table.

## Bounds

**Upper bound.** $\Theta(n)$ preprocessing, $n + 1$ words of space and $O(1)$ worst-case time per query, by prefix sums. The total time for $q$ queries is $\Theta(n + q)$.

**Lower bound.** Each algorithm must read all $n$ items in the worst case, since an unread item could change the answer to the query $(0, n-1)$, and it must write $q$ answers. So $\Omega(n + q)$ time is necessary, and prefix sums are optimal up to a constant factor.

**Without an inverse.** In the semigroup model, where an algorithm may only add stored partial sums and cannot subtract, Yao (1982) proved that with $O(n)$ stored partial sums a query needs about $\alpha(n)$ additions in the worst case, where $\alpha$ is an inverse of the Ackermann function, and that this is achievable. So subtraction is what makes the $O(1)$ query with linear space possible.

## Reductions

- **To prefix sums.** $S(l, r) = P[r+1] - P[l]$: one query becomes two prefix values and one subtraction.
- **From counting.** "How many items in $a[l \ldots r]$ have property $X$" reduces to a range sum on the 0/1 array of the property, in $O(n)$ time.
- **To two dimensions.** A one-row grid is an array, so the [two-dimensional range sum query](/range-sum-query-2d/) contains this problem.
- **From the range mean.** The average of $a[l \ldots r]$ is $S(l, r) / (r - l + 1)$.

## Applications

- Statistics over time series: totals, means and moving averages over intervals of days or samples.
- Counting letters, words or events in a range of a string or log, with one table per letter or event type.
- A first step of many subarray algorithms: [subarray sum equals k](/subarray-sum-equals-k/), [longest zero-sum subarray](/longest-zero-sum-subarray/) and the [maximum subarray problem](/maximum-subarray-problem/) all turn a subarray sum into a difference of two prefix sums.
- The quadratic maximum subvector algorithm in Bentley's Programming Pearls uses a cumulative array to sum each candidate range in $O(1)$ time.

## References
