---
tag: YK71ZH
kind: problem
slug: lower-bound-query
name: Lower bound query
aliases:
- bisect left
- first element not less than a key
area: searching/sequential-and-binary-search
level: core
summary: Return the first position in a sorted array whose value is not less than the key.
model: comparison-model
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(log n)}
prereqs: [search-in-sorted-array, total-order]
see_also: [upper-bound-query, lower-and-upper-bound-search, first-and-last-occurrence, binary-search, predecessor-problem, branchless-binary-search, binary-search-on-answer, search-lower-bound]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.1, binary search in an ordered array (the rank() operation)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an ordered table
  - url: https://docs.python.org/3/library/bisect.html
    title: Python Software Foundation, bisect, Array bisection algorithm
    note: bisect_left returns the lower bound
  - url: https://en.cppreference.com/w/cpp/algorithm/lower_bound
    title: cppreference.com, std::lower_bound
---

A lower bound query asks, for a sorted array $A[0 \ldots n-1]$ and a key $x$, for the first index $\ell$ with $A[\ell] \ge x$, or $n$ when every item is less than $x$. The answer is the number of items less than $x$, and it is the first place where $x$ can be inserted with the array still sorted. A variant of [binary search](/binary-search/) answers it with at most $\lceil \lg(n+1) \rceil$ two-way comparisons, which is optimal in the [comparison model](/comparison-model/). It is the query behind `bisect_left` in Python and `std::lower_bound` in C++, and most other searches in a sorted array are built from it.

## In plain words

You have a row of numbers in increasing order, and a new number. You want to know where the new number fits: how many numbers in the row are smaller than it. The answer is a position between two numbers of the row, or before the first one, or after the last one.

If the new number is already in the row, the answer is the position of its first copy. If it is not in the row, the answer is the place where it would go. So this one question tells you both whether a value is present and where it belongs. It never fails: there is always an answer.

## Definition

**Input.** An array $A[0 \ldots n-1]$ with $n \ge 0$ items from a [total order](/total-order/), with $A[0] \le A[1] \le \cdots \le A[n-1]$, and a key $x$.

**Output.** The index

$$ \ell(A, x) = \min\bigl(\{\, i \in \{0, \ldots, n-1\} : A[i] \ge x \,\} \cup \{n\}\bigr). $$

Because $A$ is sorted, the test $A[i] \ge x$ is false for $i < \ell$ and true for $i \ge \ell$. So the output is the unique $\ell \in \{0, \ldots, n\}$ with

$$ A[i] < x \text{ for each } i < \ell, \qquad A[i] \ge x \text{ for each } i \ge \ell. $$

From this, $\ell(A, x) = |\{\, i : A[i] < x \,\}|$, the *rank* of $x$ in $A$. The output always exists, and $n + 1$ outputs are possible.

## Variants

- **[Upper bound query](/upper-bound-query/).** The first index with $A[i] > x$. It differs from the lower bound only when $x$ is in $A$.
- **With a comparator.** Replace $<$ by any strict weak order, for example "shorter string first". The array must be sorted by the same order.
- **Partition point.** For any test $P$ on items such that $A$ is all true then all false, find the first false item. The lower bound is the case $P(y) = (y < x)$. Rust calls this `partition_point`.
- **Predecessor.** The largest item less than $x$ is $A[\ell - 1]$ when $\ell > 0$. The smallest item not less than $x$ (the ceiling, or successor) is $A[\ell]$ when $\ell < n$. See the [predecessor problem](/predecessor-problem/).
- **Search with membership.** The key is in $A$ if and only if $\ell < n$ and $A[\ell] = x$, and then $\ell$ is the [first occurrence](/first-and-last-occurrence/).

## Examples

The array is $A = [1, 3, 3, 3, 5, 8, 8, 13]$, with $n = 8$.

| $x$ | 0 | 1 | 3 | 4 | 8 | 13 | 20 |
|---|---|---|---|---|---|---|---|
| $\ell(A, x)$ | 0 | 0 | 1 | 4 | 5 | 7 | 8 |

- $x = 3$ gives 1, the first of the three copies of 3.
- $x = 4$ is absent. It goes between the last 3 and the 5, at index 4, and four items are less than 4.
- $x = 20$ is greater than all items, so the answer is $n = 8$, which is not a valid index. A program must test $\ell < n$ before it reads $A[\ell]$.
- For the empty array, $\ell = 0$ for each $x$.

## Known algorithms

- **[Lower and upper bound search](/lower-and-upper-bound-search/).** The binary search on the test $A[mid] < x$ with the half-open range $[lo, hi)$. It makes $\lfloor \lg n \rfloor$ or $\lfloor \lg n \rfloor + 1$ two-way comparisons, never more than $\lceil \lg(n+1) \rceil$, and uses $\Theta(1)$ space.
- **[Branchless binary search](/branchless-binary-search/).** The same comparisons with a fixed number of steps for each $n$ and no data-dependent branch.
- **[Eytzinger layout](/eytzinger-layout/).** The same query on an array stored in breadth-first order of the search tree, for better use of the cache.
- **[Exponential search](/exponential-search/).** $O(\log \ell)$ comparisons, good when the answer is near the start.
- **[Linear search](/linear-search/).** Scan for the first $A[i] \ge x$. $\ell + 1$ comparisons, or $n$ when $\ell = n$.

## Bounds

**Upper bound.** The binary search of [lower and upper bound search](/lower-and-upper-bound-search/) uses at most $\lceil \lg(n+1) \rceil$ two-way comparisons.

**Lower bound.** Each deterministic algorithm that learns about $A$ and $x$ only by two-way comparisons makes at least $\lceil \lg(n+1) \rceil$ comparisons on some input.

*Proof.* Fix $A = [2, 4, \ldots, 2n]$ and let $x$ range over $1, 3, \ldots, 2n+1$. The key $x = 2j+1$ has $\ell = j$, so these $n + 1$ inputs have $n + 1$ different answers. On a fixed $n$, the algorithm is a decision tree whose inner nodes are comparisons with two answers each, and whose leaves are outputs. The $n + 1$ inputs reach leaves with different outputs, so the tree has at least $n + 1$ leaves. A binary tree of height $h$ has at most $2^h$ leaves, so $2^h \ge n + 1$ and $h \ge \lceil \lg(n+1) \rceil$. The height is the number of comparisons on the longest path. $\blacksquare$

The two bounds are equal, so $\lceil \lg(n+1) \rceil$ is the exact worst-case cost. For $n = 1000$ it is 10, and for $n = 10^6$ it is 20.

Unlike the three-way search of [search in a sorted array](/search-in-sorted-array/), the lower bound query has no early exit: a match does not end the search, because an earlier copy may exist. So the best case is also about $\lg n$ comparisons.

**Other models.** On a [word RAM](/word-ram/) with integer keys and preprocessing allowed, the query is the static [predecessor problem](/predecessor-problem/), with faster structures for large $n$. Interpolation search answers it in $O(\log \log n)$ expected probes on uniform random keys.

## Reductions

- **Membership reduces to it.** Compute $\ell$, then test $\ell < n$ and $A[\ell] = x$: one extra comparison.
- **The upper bound reduces to it** for integer keys: $u(A, x) = \ell(A, x + 1)$. For any keys it reduces with a flipped test, $A[mid] \le x$ in place of $A[mid] < x$.
- **Counting reduces to it.** The number of items in the half-open range $[a, b)$ is $\ell(A, b) - \ell(A, a)$, and the number of copies of $x$ is $u(A, x) - \ell(A, x)$.
- **Search on the answer reduces to it.** Finding the smallest $t$ in a range with a monotone test $P(t)$ is a lower bound query on the implicit array $[P(lo), \ldots, P(hi - 1)]$ of false and true values. See [binary search on the answer](/binary-search-on-answer/).

## Applications

- Insert into a sorted array, or into the binary variant of [insertion sort](/insertion-sort/), at position $\ell$. Insertion at $\ell$ puts the new item before its equal items; insertion at the upper bound keeps the order of arrival, which makes the sort stable.
- Rank queries in an ordered symbol table, as the `rank` operation of Sedgewick and Wayne.
- Range counting and range reporting in a sorted list of values, such as the events between two timestamps.
- The [longest increasing subsequence](/longest-increasing-subsequence/) in $O(n \log n)$ time, which does one lower bound query per item on the array of the smallest tails.

## References
