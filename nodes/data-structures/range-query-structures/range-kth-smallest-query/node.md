---
tag: JSQ2XM
kind: problem
slug: range-kth-smallest-query
name: Range k-th smallest query
aliases:
- range order statistic query
- range median query
area: data-structures/range-query-structures
level: advanced
summary: Return the k-th smallest value in a subarray, with the median as a special case.
prereqs: [range-query-problem, selection-problem, segment-tree]
see_also: [persistent-segment-tree, wavelet-tree, merge-sort-tree, wavelet-matrix, parallel-binary-search, coordinate-compression, order-statistic-tree, cell-probe-model]
sources:
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: section Preserving the history of its values (Persistent Segment Tree), subsection Finding the k-th smallest number in a range
  - paper: doi:10.1016/j.jda.2013.07.004
    title: "Gonzalo Navarro, Wavelet trees for all, Journal of Discrete Algorithms 25 (2014)"
    locator: the section on range quantile queries over sequences of integers
  - paper: "Allan Gronlund Jorgensen and Kasper Green Larsen, Range selection and median: tight cell probe lower bounds and adaptive data structures, Proceedings of the 22nd Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2011)"
    locator: the Omega(log n / log log n) cell-probe lower bound for range selection with near-linear space, and the matching upper bound
---

The range k-th smallest query asks for the value of rank $k$ among $A[l], \ldots, A[r]$, for many triples $(l, r, k)$ on one array. The range median, with $k = \lceil (r - l + 1)/2 \rceil$, is the most common case. It is the [selection problem](/selection-problem/) asked again and again on subarrays, and it does not fit the monoid form of the [range query problem](/range-query-problem/), since the $k$-th smallest of a union does not follow from one number for each part. After [coordinate compression](/coordinate-compression/), a [persistent segment tree](/persistent-segment-tree/) or a [wavelet tree](/wavelet-tree/) answers each query in $O(\log n)$ time with $O(n \log n)$ preprocessing, and cell-probe bounds of Jorgensen and Larsen show that $\Theta(\log n / \log \log n)$ is the best query time with near-linear space.

## In plain words

You have the scores of a long line of players, in the order they played. A question names a stretch of the line and a number $k$, and asks for the $k$-th lowest score in that stretch. Asking for the middle score of the stretch is the same kind of question.

Sorting the stretch for each question is slow. The fast methods prepare, once, the counts of how many scores of each part of the line fall in each part of the score scale. A question then goes down the score scale in halves: it asks how many scores of the stretch lie in the lower half of the scale, and goes left or right like a game of "higher or lower", one step per halving.

## Definition

**Input.** An array $A[0 \ldots n-1]$ over a totally ordered set. Then queries $(l, r, k)$ with $0 \le l \le r \le n - 1$ and $1 \le k \le r - l + 1$.

**Output.** For each query, the value $\mathrm{sel}(l, r, k)$, the $k$-th item of the sorted list of $A[l], \ldots, A[r]$, counted with repetitions.

**The dual query.** For a value $x$, let $\mathrm{rank}(l, r, x) = |\{ i \in [l, r] : A[i] < x \}|$. Then $\mathrm{sel}(l, r, k)$ is the largest value $x$ in $A$ with $\mathrm{rank}(l, r, x) < k$. So a structure for rank queries gives one for selection by a [binary search](/binary-search/) over the sorted values, at a cost of a factor $O(\log n)$.

## Variants

- **Range median.** The case $k = \lceil (r - l + 1)/2 \rceil$.
- **Static, online.** The array does not change, and each query is answered before the next one is read.
- **Static, offline.** All queries are known first. [Parallel binary search](/parallel-binary-search/) answers all of them together with one Fenwick tree in $O((n + q) \log^2 n)$ time.
- **Point updates.** $A[i] \leftarrow x$ between queries. A Fenwick tree of segment trees over the values, or the offline method with updates as events, gives $O(\log^2 n)$ per operation.
- **Rank and counting queries.** Count the items of $A[l \ldots r]$ that are less than $x$, or that lie in a value range $[x, y]$.
- **Top-$k$ reporting.** Report the $k$ smallest items of the range in sorted order.
- **Paths of trees.** The $k$-th smallest weight on the path between two nodes; persistent trees built along root paths handle it with the lowest common ancestor.

## Examples

Let $A = [5, 2, 8, 1, 9, 3, 7, 4]$.

| query $(l, r, k)$ | the range | sorted | answer |
|---|---|---|---|
| $(1, 5, 2)$ | 2, 8, 1, 9, 3 | 1, 2, 3, 8, 9 | 2 |
| $(0, 7, 4)$ | the whole array | 1, 2, 3, 4, 5, 7, 8, 9 | 4 |
| $(2, 6, 3)$, the median | 8, 1, 9, 3, 7 | 1, 3, 7, 8, 9 | 7 |
| $(3, 3, 1)$ | 1 | 1 | 1 |

**A walk on the persistent tree.** The sorted values are $1, 2, 3, 4, 5, 7, 8, 9$, with the ranks 0 to 7. Version $p$ of the tree counts, for each range of ranks, the items of $A[0 \ldots p - 1]$ with a rank in it. For the query $(1, 5, 2)$, take the difference of the versions 6 and 1, which counts the items of $A[1 \ldots 5]$.

1. At the ranks $[0, 7]$, the left half $[0, 3]$ holds the values 1 to 4, and the range has 3 of them: 2, 1 and 3. Since $k = 2 \le 3$, go left.
2. At $[0, 3]$, the left half $[0, 1]$ holds the values 1 and 2, and the range has 2 of them. Since $k = 2 \le 2$, go left.
3. At $[0, 1]$, the left half $[0, 0]$ holds the value 1, and the range has 1 of it. Since $k = 2 > 1$, set $k \leftarrow 1$ and go right.
4. The leaf is rank 1, the value 2.

## Known algorithms

| method | preprocessing | query | space |
|---|---|---|---|
| copy and [quickselect](/quickselect/) | none | $O(r - l + 1)$ expected | $O(n)$ |
| [persistent segment tree](/persistent-segment-tree/) over the ranks | $O(n \log n)$ | $O(\log n)$ | $O(n \log n)$ words |
| [wavelet tree](/wavelet-tree/) or [wavelet matrix](/wavelet-matrix/) | $O(n \log \sigma)$ | $O(\log \sigma)$ | $n \lg \sigma + o(n \log \sigma)$ bits |
| [merge sort tree](/merge-sort-tree/) and a binary search over the values | $O(n \log n)$ | $O(\log^3 n)$ | $O(n \log n)$ words |
| [square-root decomposition](/square-root-decomposition/) with sorted blocks | $O(n \log n)$ | $O(\sqrt{n \log n} \log n)$ | $O(n)$ |
| [parallel binary search](/parallel-binary-search/), offline | | $O((n + q) \log^2 n)$ in total | $O(n + q)$ |
| the linear-space structure of Brodal and Jorgensen | $O(n \log n)$ | $O(\log n / \log \log n)$ | $O(n)$ words |

Here $\sigma \le n$ is the number of distinct values. The query of the persistent tree is the walk shown above: at each node it reads the counts of the left child in two versions and subtracts them, so it costs one step per level. The wavelet tree does the same walk on bit vectors with rank operations; see [rank and select dictionaries](/rank-select-dictionary/).

## Bounds

**Comparison lower bounds.** One query $(0, n - 1, k)$ is selection, which needs $\Omega(n)$ comparisons. The $n$ queries $(0, n - 1, k)$ for $k = 1, \ldots, n$ sort the array, so preprocessing plus $n$ queries need $\Omega(n \log n)$ comparisons in the [comparison model](/comparison-model/); see the [comparison sort lower bound](/comparison-sort-lower-bound/).

**Cell-probe bounds.** In the [cell-probe model](/cell-probe-model/) with words of $\Theta(\log n)$ bits, Jorgensen and Larsen proved that a static structure of $n \log^{O(1)} n$ space needs $\Omega(\log n / \log \log n)$ probes for a range median query. A structure of linear space with $O(\log n / \log \log n)$ query time, by Brodal and Jorgensen, meets this bound, so it is tight.

**Upper bound.** $O(\log n / \log \log n)$ query time with $O(n)$ words. In practice the $O(\log n)$ methods of the table are simpler and fast.

## Reductions

- **Selection to range selection.** The query $(0, n - 1, k)$ is the [selection problem](/selection-problem/), and $n$ such queries are sorting.
- **Range selection to range rank.** By the binary search over values in the definition.
- **Range rank to orthogonal range counting.** The rank of $x$ in $A[l \ldots r]$ counts the points $(i, A[i])$ in the rectangle $[l, r] \times (-\infty, x)$; see [orthogonal range counting](/orthogonal-range-counting/).

## Applications

- Medians and percentiles of a window of a time series, which are robust to outliers.
- The median filter of signal and image processing, over windows of a fixed size.
- Database queries for quantiles of the rows in a range of keys.
- Subproblems in competitive programming, such as the $k$-th smallest weight on a tree path.

## References
