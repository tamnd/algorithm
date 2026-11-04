---
tag: KD8QJ4
kind: problem
slug: point-update-range-sum-query
name: Point update range sum query
aliases:
- dynamic range sum query
- range sum with point updates
area: data-structures/range-query-structures
level: intro
summary: Support changing one element and answering range sums in the same structure.
model: cell-probe-model
complexity:
  vars: {n: the length of the array}
  time: {amortized: Ω(log n)}
prereqs: [range-sum-query, prefix-sums, invertible-operation]
see_also: [fenwick-tree, segment-tree, square-root-decomposition, dynamic-partial-sums-lower-bound, range-update-point-query, point-update-range-min-query, counting-inversions, offline-query-processing]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 9, Range queries, Sections 9.2 Binary indexed tree and 9.3 Segment tree
  - paper: doi:10.1002/spe.4380240306
    title: "Peter M. Fenwick, A new data structure for cumulative frequency tables, Software: Practice and Experience 24(3) (1994), 327-336"
    locator: the whole paper (update and prefix sum in O(log n))
  - paper: doi:10.1137/S0097539705447256
    title: "Mihai Patrascu and Erik D. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM Journal on Computing 35(4) (2006), 932-963"
    locator: Section 2.1 (Theorems 2.1 and 2.2, the trade-off between update and query time)
  - paper: doi:10.1145/73007.73040
    title: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st Annual ACM Symposium on Theory of Computing (STOC 1989), 345-354"
    locator: the Omega(log n / log log n) bound for partial sums
---

The point update range sum query problem keeps an array of $n$ numbers under two operations: change one item, and return the sum of the items in a range $[l, r]$. It is the dynamic form of the [range sum query](/range-sum-query/), and the first problem that needs a real data structure rather than a precomputed table. The [Fenwick tree](/fenwick-tree/) and the [segment tree](/segment-tree/) solve it in $O(\log n)$ time per operation, and Patrascu and Demaine proved that $\Omega(\log n)$ amortized time per operation is necessary in the [cell-probe model](/cell-probe-model/), so these structures are optimal.

## In plain words

You keep a row of numbers, such as the sales of each day. Two kinds of requests come in mixed order. One says "the sales of day 5 are now 12". The other asks "what were the total sales from day 3 to day 9?".

If you store only the numbers, a change is fast but a total needs a long loop. If you store all running totals, a total is one subtraction but a change moves many stored totals. The problem asks for a layout in which both requests are fast at the same time. The known good answers take time that grows with the number of digits of the row length, and no layout can do better than that.

## Definition

**Data.** An array $A[1 \ldots n]$ over an abelian group $(G, +, 0)$, usually the integers modulo $2^{64}$ or the integers that fit in a machine word. The array is given at the start, or it is all zeros.

**Operations.** A sequence of operations, each answered before the next one is read (online):

- $\textsc{update}(i, x)$ with $1 \le i \le n$: set $A[i] \leftarrow x$. The additive form $\textsc{add}(i, \delta)$ sets $A[i] \leftarrow A[i] + \delta$.
- $\textsc{sum}(l, r)$ with $1 \le l \le r \le n$: return $\sum_{k=l}^{r} A[k]$ for the current array.

**Cost.** The preprocessing time, the worst-case or amortized time $t_u$ of an update, the time $t_q$ of a query, and the space. A good solution has $O(n)$ space and small $t_u$ and $t_q$ at once.

The two forms of update are equivalent: $\textsc{update}(i, x)$ is $\textsc{add}(i, x - A[i])$ if a copy of $A$ is kept, and $\textsc{add}(i, \delta)$ is $\textsc{update}(i, A[i] + \delta)$. A query $\textsc{sum}(l, r)$ is $\textsc{prefix}(r) - \textsc{prefix}(l - 1)$, so over a group the problem is the same as the *dynamic partial sums* problem, which asks only for prefix sums.

## Variants

- **Prefix sums only.** $\textsc{prefix}(i) = A[1] + \cdots + A[i]$. Equivalent over a group, as above.
- **Without an inverse.** Over a commutative monoid without subtraction, such as $\max$ on non-negative numbers, the range form is harder than the prefix form. With $\min$ it is the [point update range minimum query](/point-update-range-min-query/).
- **Range update, point query.** Add $\delta$ to $A[l \ldots r]$ and read one item. It is the same problem on the [difference array](/difference-array/), see [range update point query](/range-update-point-query/).
- **Range update, range query.** Both operations act on ranges. Two Fenwick trees or a segment tree with [lazy propagation](/lazy-propagation/) solve it in $O(\log n)$, see [range update range query](/range-update-range-query/).
- **Search.** Find the least $i$ with $\textsc{prefix}(i) \ge s$ when all items are non-negative. This is the *select* query of a dynamic multiset of counts.
- **Offline.** All operations are known in advance, as in [offline query processing](/offline-query-processing/). The same structures still apply, and offline order is used mainly to turn other problems into this one.
- **Two dimensions.** Points in a grid with updates and rectangle sums, see the [two-dimensional range sum query](/two-dimensional-range-sum-query/).

## Examples

Start with $A = [2, 7, 1, 8, 2, 8]$.

| operation | array after | answer |
|---|---|---|
| $\textsc{sum}(2, 4)$ | $[2, 7, 1, 8, 2, 8]$ | $7 + 1 + 8 = 16$ |
| $\textsc{update}(3, 5)$ | $[2, 7, 5, 8, 2, 8]$ | |
| $\textsc{sum}(2, 4)$ | $[2, 7, 5, 8, 2, 8]$ | $20$ |
| $\textsc{add}(6, -8)$ | $[2, 7, 5, 8, 2, 0]$ | |
| $\textsc{sum}(1, 6)$ | $[2, 7, 5, 8, 2, 0]$ | $24$ |
| $\textsc{sum}(5, 5)$ | $[2, 7, 5, 8, 2, 0]$ | $2$ |

With prefix sums stored in a plain array, the update of position 3 would have to change the four prefix sums of positions 3 to 6. With only the array, the last-but-one query would need five additions.

## Known algorithms

| method | update | query | space | notes |
|---|---|---|---|---|
| plain array | $O(1)$ | $O(n)$ | $n$ | sum a loop each time |
| [prefix sums](/prefix-sums/) array | $O(n)$ | $O(1)$ | $n + 1$ | rebuild the suffix after each update |
| [square-root decomposition](/square-root-decomposition/) | $O(1)$ | $O(\sqrt n)$ | $n + \sqrt n$ | blocks of size about $\sqrt n$ with block sums |
| [Fenwick tree](/fenwick-tree/) | $O(\log n)$ | $O(\log n)$ | $n$ | needs an inverse for a range |
| [segment tree](/segment-tree/) | $O(\log n)$ | $O(\log n)$ | $2n$ to $4n$ | any monoid, also range updates |

All times are worst case. The Fenwick tree has the smallest constant factor: one update or prefix sum touches at most $\lfloor \lg n \rfloor + 1$ cells. A $b$-ary tree, with $b$ children per node and the prefix sums of the children stored at each node, gives updates in $O(b \log_b n)$ and queries in $O(\log_b n)$, or the reverse when each node stores only the plain child sums. This is how a structure meets the other points of the trade-off below.

## Bounds

**Lower bound.** Patrascu and Demaine (2006) proved that every structure in the cell-probe model, with word-size cells and word-size values, has

$$ t_q \lg \frac{t_u}{t_q} = \Omega(\lg n) \quad \text{and} \quad t_u \lg \frac{t_q}{t_u} = \Omega(\lg n), $$

with the logarithms read as $\log_2(2 + x)$, even with amortization and Las Vegas randomization. So $\max(t_u, t_q) = \Omega(\log n)$, and the Fenwick tree and the segment tree are optimal up to a constant factor. Before this, Fredman and Saks (1989) proved $\Omega(\log n / \log \log n)$. The proofs are on the page of the [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/).

**Upper bound.** $O(\log n)$ worst case per operation with $n$ words of space and $O(n)$ preprocessing, by the Fenwick tree. The trade-off is tight: the $b$-ary trees above meet $t_u = O(b \log_b n)$ with $t_q = O(\log_b n)$ for each $b \ge 2$.

**Extreme points.** With $t_u = O(1)$ the query needs $n^{\Omega(1)}$ time, and with $t_q = O(1)$ the update needs $n^{\Omega(1)}$ time, by the trade-off. Square-root decomposition shows that $t_u = O(1)$ with $t_q = O(\sqrt n)$ is possible, and blocks of size $n^{\varepsilon}$ on $1 / \varepsilon$ levels give $t_u = O(1 / \varepsilon)$ with $t_q = O(n^{\varepsilon} / \varepsilon)$.

## Reductions

- **Ranges to prefixes.** $\textsc{sum}(l, r) = \textsc{prefix}(r) - \textsc{prefix}(l - 1)$, one extra query and one subtraction. Prefixes are ranges with $l = 1$. So the two problems have the same complexity over a group.
- **Range update point query to this problem.** Store $D[i] = A[i] - A[i - 1]$. A range add is two point adds on $D$, and $A[i]$ is a prefix sum of $D$. The reduction works in both directions with $O(1)$ overhead.
- **Counting inversions to this problem.** Scan the array from left to right over the compressed values. For each item $x$, query the number of earlier items greater than $x$, then add 1 at $x$. This gives $n$ updates and $n$ queries, so [counting inversions](/counting-inversions/) takes $O(n \log n)$ time.
- **Offline dominance counting to this problem.** Points $(x, y)$ and queries "how many points have $x' \le x$ and $y' \le y$" are sorted by $x$ and swept, with the $y$ values in a Fenwick tree. This is the base of offline [two-dimensional range sum queries](/two-dimensional-range-sum-query/).

## Applications

- Cumulative frequency tables of adaptive arithmetic coders, the use for which Fenwick designed his tree.
- Order statistics on a dynamic multiset of small integers: counts per value, with select by prefix search.
- Counting inversions, and the many offline problems that sort the queries and sweep, such as the offline count of distinct values in ranges.
- Ranking in leaderboards and histograms that change one bucket at a time.

## References
