---
tag: 2T989J
kind: problem
slug: range-query-problem
name: Range query problem
aliases:
- range aggregation query
- range query
area: data-structures/range-query-structures
level: intro
summary: Preprocess an array so an aggregate over any contiguous index range can be answered quickly.
prereqs: [array, associative-operator, asymptotic-notation]
see_also: [range-query-structure, prefix-sums, segment-tree, fenwick-tree, sparse-table, square-root-decomposition, range-minimum-query, orthogonal-range-searching]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 9 (Range queries), Sections 9.1 (Static array queries), 9.2 (Binary indexed tree) and 9.3 (Segment tree)
  - paper: "Michael A. Bender and Martin Farach-Colton, The LCA problem revisited, LATIN 2000: Theoretical Informatics, Lecture Notes in Computer Science 1776, Springer, 2000"
    locator: the definition of RMQ, the sparse table with O(n log n) preprocessing and O(1) query, and the reductions between RMQ and LCA
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: Section 2.1, the lower bound for dynamic partial sums
  - paper: doi:10.1137/0214022
    title: "Andrew C. Yao, On the Complexity of Maintaining Partial Sums, SIAM Journal on Computing 14(2) (1985), 277-288"
    locator: the semigroup model of partial sums
---

The range query problem asks to preprocess an [array](/array/) $A[0 \ldots n-1]$ so that, for any indices $l \le r$, the aggregate $A[l] \oplus A[l+1] \oplus \cdots \oplus A[r]$ under an [associative operation](/associative-operator/) $\oplus$ can be returned quickly, often while the array also changes. Sum, minimum, maximum, greatest common divisor and bitwise or are the usual operations. The answer depends on what $\oplus$ allows: an operation with an inverse gives $O(1)$ queries by [prefix sums](/prefix-sums/), an idempotent one gives $O(1)$ queries by a [sparse table](/sparse-table/), and any associative one gives $O(\log n)$ queries and updates by a [segment tree](/segment-tree/).

## In plain words

You have a long list of numbers, and you get many questions of the same type: what is the total of the items from position 3 to position 40, what is the smallest item from position 10 to position 12, and so on. Each question names a stretch of the list. Adding up the stretch each time is slow when the list is long and the questions are many.

The fix is to do some work once, before the questions come, and store the results in a helper structure. Then each question takes only a few steps. Sometimes the list also changes between questions, and the helper must be kept up to date at a low cost. The best helper depends on the kind of combining: totals, smallest values and common divisors each allow different tricks.

## Definition

**Input.** An array $A[0 \ldots n-1]$ of elements of a set $S$, and an associative operation $\oplus : S \times S \to S$, so that $(x \oplus y) \oplus z = x \oplus (y \oplus z)$ for all $x, y, z \in S$. Then a sequence of queries $(l, r)$ with $0 \le l \le r \le n-1$, and in the dynamic version also updates.

**Output.** For each query $(l, r)$, the value

$$Q(l, r) = A[l] \oplus A[l+1] \oplus \cdots \oplus A[r] = \bigoplus_{i=l}^{r} A[i],$$

taken over the array as it is at the time of the query. Associativity makes this value well defined without brackets. The operation need not be commutative, so the order of the terms matters, for example for the product of matrices.

**Updates.** A *point update* $(i, x)$ sets $A[i] \leftarrow x$. A *range update* $(l, r, f)$ sets $A[i] \leftarrow f(A[i])$ for each $l \le i \le r$, for example $f(v) = v + c$ or $f(v) = c$.

**Cost.** A solution is measured by its preprocessing time $p(n)$, its space $s(n)$, its query time $q(n)$ and, when updates exist, its update time $u(n)$. We write the cost as $\langle p(n), q(n) \rangle$, and count one application of $\oplus$ as one step.

## Variants

- **Static or dynamic.** In the static version the array never changes after preprocessing. In the dynamic version, point or range updates come between the queries, see [point update range sum](/point-update-range-sum-query/), [point update range minimum](/point-update-range-min-query/), [range update range query](/range-update-range-query/) and [range assignment](/range-assignment-query/).
- **By the algebra of the operation.** If $(S, \oplus)$ is a group, so each element has an inverse, then $Q(l, r) = P(l)^{-1} \oplus P(r+1)$ with prefix values $P$; this is the case of [range sum](/range-sum-query/), see [invertible operation](/invertible-operation/). If $\oplus$ is [idempotent](/idempotent-operation/), so $x \oplus x = x$, two overlapping ranges can cover the query; this is the case of [range minimum](/range-minimum-query/) and [range GCD](/range-gcd-query/). If $\oplus$ has only an identity, $(S, \oplus)$ is a [monoid](/monoid/) and tree structures are needed.
- **Decomposable or not.** In all cases above, the answer for a range follows from the answers for two parts. The [range mode](/range-mode-query/), [range distinct count](/range-distinct-count-query/) and [range k-th smallest](/range-kth-smallest-query/) queries are not of this form, and they need other methods.
- **Online or offline.** An [offline](/offline-algorithm/) solution sees all queries first and may answer them in any order, as [Mo's algorithm](/mo-algorithm/) does. An online one must answer each query before it sees the next one.
- **More dimensions.** The array is a grid and the query is a rectangle, see the [two-dimensional range sum query](/two-dimensional-range-sum-query/) and [orthogonal range searching](/orthogonal-range-searching/).

## Examples

Let $A = [5, 2, 8, 1, 9, 3, 7, 4]$, with indices 0 to 7.

| query $(l, r)$ | the range | sum | min | max |
|---|---|---|---|---|
| $(1, 4)$ | 2, 8, 1, 9 | 20 | 1 | 9 |
| $(2, 6)$ | 8, 1, 9, 3, 7 | 28 | 1 | 9 |
| $(0, 3)$ | 5, 2, 8, 1 | 16 | 1 | 8 |
| $(5, 7)$ | 3, 7, 4 | 14 | 3 | 7 |
| $(0, 7)$ | the full array | 39 | 1 | 9 |

The prefix sums are $P = [0, 5, 7, 15, 16, 25, 28, 35, 39]$, with $P(i) = A[0] + \cdots + A[i-1]$. So the sum on $(2, 6)$ is $P(7) - P(2) = 35 - 7 = 28$. The minimum has no inverse: knowing the minimum 1 of the prefix $A[0 \ldots 6]$ and the minimum 2 of the prefix $A[0 \ldots 1]$ tells nothing about the minimum of $A[2 \ldots 6]$.

After the point update $A[3] \leftarrow 6$, the sum on $(1, 4)$ becomes 25 and the minimum on $(2, 6)$ becomes 3.

## Known algorithms

| method | operation | preprocessing | query | update |
|---|---|---|---|---|
| scan the range | any associative | none | $O(n)$ | $O(1)$ point |
| [prefix sums](/prefix-sums/) | group | $O(n)$ | $O(1)$ | $O(n)$ point |
| [sparse table](/sparse-table/) | idempotent | $O(n \log n)$ | $O(1)$ | none |
| [disjoint sparse table](/disjoint-sparse-table/) | any associative | $O(n \log n)$ | $O(1)$ | none |
| [sqrt tree](/sqrt-tree/) | any associative | $O(n \log \log n)$ | $O(1)$ | $O(\sqrt n)$ point |
| [square-root decomposition](/square-root-decomposition/) | any associative | $O(n)$ | $O(\sqrt n)$ | $O(\sqrt n)$ point |
| [Fenwick tree](/fenwick-tree/) | group | $O(n)$ | $O(\log n)$ | $O(\log n)$ point |
| [segment tree](/segment-tree/) | any associative | $O(n)$ | $O(\log n)$ | $O(\log n)$ point |
| segment tree with [lazy propagation](/lazy-propagation/) | monoid with a compatible update | $O(n)$ | $O(\log n)$ | $O(\log n)$ range |
| [Fischer-Heun RMQ](/fischer-heun-rmq/), [Bender-Farach-Colton RMQ](/bender-farach-colton-rmq/) | min or max | $O(n)$ | $O(1)$ | none |

The costs are worst case and count one $\oplus$ as one step. The times for the scan and for the prefix sums with updates come from recomputing the affected values.

## Bounds

**Static, with an inverse.** Prefix sums use $n + 1$ stored values and one subtraction per query, so $\langle O(n), O(1) \rangle$ is reached and is optimal up to constants.

**Static, idempotent or general.** For min and max, $\langle O(n), O(1) \rangle$ is reached on the [word RAM](/word-ram/) by the reduction to the [lowest common ancestor](/lowest-common-ancestor/) problem, see the [RMQ-LCA equivalence](/rmq-lca-equivalence/). For a general semigroup, where only $\oplus$ may be applied to the stored values, Yao studied the trade-off between the space and the number of $\oplus$ steps per query.

**Dynamic.** In the [cell-probe model](/cell-probe-model/) with words of $\Theta(\log n)$ bits, Patrascu and Demaine proved that point updates and prefix sums need $\max(t_u, t_q) = \Omega(\log n)$ per operation, even with amortization and randomization; see the [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/). A range sum query answers a prefix sum, so the bound applies to the dynamic range sum query, and the Fenwick tree and the segment tree are optimal up to a constant factor.

## Reductions

- **Range sum to prefix sums.** With an inverse, one range query costs two prefix queries and one subtraction.
- **Range minimum to lowest common ancestor and back.** Each reduces to the other in $O(n)$ time, with $O(1)$ extra time per query, see the [RMQ-LCA equivalence](/rmq-lca-equivalence/).
- **Range update to point update.** A range add with point queries is a point update with range sums on the [difference array](/difference-array/), see [range update point query](/range-update-point-query/).

## Applications

- The [longest common prefix](/lcp-array/) of two suffixes of a string is a range minimum over the LCP array of a [suffix array](/suffix-array/).
- The [lowest common ancestor](/lowest-common-ancestor/) of two tree nodes is a range minimum over an Euler tour, see [Euler tour LCA](/euler-tour-lca/).
- Path and subtree queries on trees become range queries on arrays by [heavy-light decomposition](/heavy-light-decomposition/) and [Euler tour subtree queries](/euler-tour-subtree-queries/).
- Counting inversions and other order statistics with a [Fenwick tree](/inversion-count-with-fenwick-tree/).
- Time series and databases: totals and extremes over windows of time.

## References
