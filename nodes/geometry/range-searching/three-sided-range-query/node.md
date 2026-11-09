---
tag: 9S1NRM
kind: problem
slug: three-sided-range-query
name: Three-sided range query
aliases:
- 3-sided range reporting
- three-sided range reporting
- grounded range query
area: geometry/range-searching
level: core
summary: Report points in a rectangle that is unbounded on one side, a special case of orthogonal range reporting.
prereqs: [orthogonal-range-searching]
see_also: [priority-search-tree, priority-search-tree-query, orthogonal-range-reporting, dominance-counting, range-minimum-query, cartesian-tree, interval-tree, range-tree]
sources:
  - paper: doi:10.1137/0214021
    title: Edward M. McCreight, Priority search trees, SIAM Journal on Computing 14(2), 1985, pages 257 to 276
    locator: three-sided queries in O(log n + k) time with O(n) space, dynamic updates in O(log n) (DOI to be checked)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 10, Section 10.2, Priority Search Trees (queries unbounded to the left)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.2, the priority search tree and three-sided queries
---

A three-sided range query asks for the points of a planar set $P$ inside a rectangle that is unbounded on one side, such as $[x_1, x_2] \times (-\infty, y_0]$. It is a special case of [orthogonal range reporting](/orthogonal-range-reporting/) that can be solved with linear space and $O(\log n + k)$ query time, which general four-sided queries cannot match on the pointer machine. The standard structure is McCreight's [priority search tree](/priority-search-tree/), and three-sided structures are the building block of the four-sided structures with $O(n \log n / \log \log n)$ space.

## In plain words

A set of points is stored. A question gives a left limit, a right limit and a top limit, and the answer is every point between the left and right limits and below the top limit. The region is a rectangle whose bottom edge has been removed, so it extends downward forever.

Removing one side makes the question easier than a full rectangle. Among the points between the left and right limits, the answer is exactly those whose height is at most the top limit. A structure that can find the lowest point between two limits, then the next lowest, and so on, stops as soon as a point is too high, and each step costs little.

## Definition

**Notation.** $P$ is the input point set, $n = |P|$, $p = (x, y)$ a point, $d = 2$, and $k = |P \cap Q|$ the output size. $\mathrm{orient}$ and $\mathrm{incircle}$ are not used.

**Input.** A multiset $P$ of $n$ points in the plane. Points may share $x$ or $y$ coordinates, and may coincide.

**Query.** Three numbers $x_1, x_2, y_0$, defining the closed three-sided range $Q = [x_1, x_2] \times (-\infty, y_0]$.

**Output.** The points $p \in P$ with $x_1 \le p_x \le x_2$ and $p_y \le y_0$, each copy once.

The open side can be any of the four; reflecting the coordinates maps one form to another. de Berg et al. use the form $(-\infty, q_x] \times [q_y, q'_y]$, open to the left. A *two-sided* or dominance range is the case $x_2 = +\infty$.

## Variants

- **Counting.** Counting the points in a three-sided range is as hard as four-sided counting up to constants, since a four-sided count is the difference of two three-sided counts. The linear-space advantage is for reporting.
- **Minimum in a range.** Return only the lowest point with $x \in [x_1, x_2]$; this is a [range minimum query](/range-minimum-query/) over the points sorted by $x$, and it answers three-sided emptiness.
- **Dynamic.** McCreight's priority search tree, built on a balanced tree, supports insertions and deletions in $O(\log n)$ worst case time.
- **Interval stabbing.** An interval $[l, r]$ contains $q$ if and only if the point $(l, r)$ lies in $(-\infty, q] \times [q, \infty)$, a two-sided range, so stabbing queries on intervals are three-sided queries; this is one route to the [interval tree](/interval-tree/) bounds.

## Examples

Take $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$.

| query $[x_1, x_2] \times (-\infty, y_0]$ | reported points | $k$ |
|---|---|---|
| $[3, 7] \times (-\infty, 4]$ | $(5,4), (7,2)$ | 2 |
| $[3, 7] \times (-\infty, 6]$ | $(5,4), (6,6), (7,2)$ | 3 |
| $[0, 10] \times (-\infty, 2]$ | $(7,2), (8,1)$ | 2 |
| $[5, 6] \times (-\infty, 3]$ | none | 0 |
| $[4, 4] \times (-\infty, 10]$ | $(4,7)$ | 1 |

For the first query, the points with $3 \le x \le 7$ in increasing order of $y$ are $(7,2), (5,4), (6,6), (4,7), (3,8)$. The first two have $y \le 4$, and the third has $y = 6 > 4$, so the listing stops there. The point $(5,4)$ lies on the top side and is reported.

## Known algorithms

All bounds are worst case.

| structure | preprocessing | space | query | update |
|---|---|---|---|---|
| linear scan | none | $O(n)$ | $O(n)$ | $O(1)$ |
| [priority search tree](/priority-search-tree/) with its [query](/priority-search-tree-query/) | $O(n \log n)$ | $O(n)$ | $O(\log n + k)$ | $O(\log n)$ (McCreight's dynamic version) |
| range minimum queries over the $x$-sorted points, recursing on both sides of each minimum | $O(n \log n)$ | $O(n)$ | $O(\log n + k)$ | static |
| [range tree](/range-tree/) | $O(n \log n)$ | $O(n \log n)$ | $O(\log^2 n + k)$ | |

The range minimum method finds the index range of $[x_1, x_2]$ by two binary searches, takes the minimum $y$ in it, reports it if it is at most $y_0$, and recurses on the parts to its left and right. Each recursive call either reports a point or stops, and stopped calls are at most one more than the reported points, so the time is $O(\log n + k)$ with constant-time range minima. The range minimum structure can be a [Cartesian tree](/cartesian-tree/) of the $x$-sorted points with lowest common ancestor queries.

## Bounds

- **Lower bound.** In the comparison model, $\Omega(\log n + k)$ time is needed, by reduction from one-dimensional membership ($y_0 = +\infty$, $x_1 = x_2$).
- **Space.** Linear space is enough, unlike four-sided reporting, where Chazelle's pointer machine lower bound forces $\Omega(n \log n / \log \log n)$ space for polylogarithmic query time; see [range searching lower bounds](/range-searching-lower-bound/).

## Reductions

- **Four-sided from three-sided.** Build a balanced tree on $y$; at each node store two three-sided structures, one for ranges open upward and one for ranges open downward, over the points of its subtree. A four-sided query splits at the node where the $y$-interval separates and asks one three-sided query on each child. This gives $O(n \log n)$ space and $O(\log n + k)$ query time.
- **Dominance reporting** is the case $x_2 = +\infty$.
- **Interval stabbing** reduces to a two-sided query, as above.

## Applications

- Interval stabbing and window queries on sets of intervals, as in [interval trees](/interval-tree/).
- Top-$t$ queries in databases: the $t$ smallest values whose key lies in a range.
- Building block of four-sided reporting structures with near-linear space.

## References
