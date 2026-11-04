---
tag: EJADA9
kind: problem
slug: two-dimensional-range-sum-query
name: Two-dimensional range sum query
aliases:
- 2D range sum query
- rectangle sum query
area: data-structures/range-query-structures
level: advanced
summary: Return the sum of values inside an axis-aligned rectangle of a 2D grid.
prereqs: [range-query-problem, prefix-sums, inclusion-exclusion-principle]
see_also: [two-dimensional-prefix-sums, two-dimensional-fenwick-tree, two-dimensional-segment-tree, range-sum-query-2d, orthogonal-range-counting, offline-orthogonal-range-counting, range-tree, quadtree]
sources:
  - url: https://cp-algorithms.com/data_structures/fenwick.html
    title: cp-algorithms, Fenwick Tree
    locator: section Finding sum in two-dimensional array
  - url: https://leetcode.com/problems/range-sum-query-2d-immutable/
    title: LeetCode 304, Range Sum Query 2D - Immutable
    locator: the problem statement
  - paper: "Franklin C. Crow, Summed-area tables for texture mapping, SIGGRAPH 1984, Computer Graphics 18(3) (1984)"
    locator: the summed-area table and the four-lookup rectangle sum
  - paper: "Kasper Green Larsen, The cell probe complexity of dynamic range counting, Proceedings of the 44th Annual ACM Symposium on Theory of Computing (STOC 2012)"
    locator: the Omega((log n / log log n)^2) lower bound for dynamic weighted two-dimensional range counting
---

The two-dimensional range sum query asks for the sum of the entries of a matrix $M$ inside an axis-aligned rectangle $[r_1, r_2] \times [c_1, c_2]$, for many rectangles. It is the [range query problem](/range-query-problem/) on a grid instead of a line. Since addition has an inverse, the [inclusion-exclusion principle](/inclusion-exclusion-principle/) writes each rectangle sum as four sums of rectangles anchored at the corner $(0, 0)$, so [two-dimensional prefix sums](/two-dimensional-prefix-sums/) answer a static query in $O(1)$ time. With point updates, a [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/) or a [two-dimensional segment tree](/two-dimensional-segment-tree/) does both operations in $O(\log n \log m)$ time on an $n \times m$ grid.

## In plain words

Think of a map cut into a grid of squares, with the number of houses written in each square. A question draws a rectangle on the map and asks how many houses are inside.

Adding up every square of a big rectangle is slow. Instead, write in each square the number of houses in the whole block from the top-left corner of the map down to that square. A rectangle is then one big corner block, minus the block above it, minus the block to its left, plus the small corner block that was taken away twice. That is four looked-up numbers for any rectangle. When squares change, a tree of partial blocks keeps these totals up to date with a few steps per change.

## Definition

**Input.** A matrix $M[0 \ldots n-1][0 \ldots m-1]$ of numbers, from an abelian group such as the integers. Then queries $(r_1, c_1, r_2, c_2)$ with $0 \le r_1 \le r_2 \le n - 1$ and $0 \le c_1 \le c_2 \le m - 1$, and in the dynamic version updates $\mathrm{add}(r, c, \delta)$ that set $M[r][c] \leftarrow M[r][c] + \delta$.

**Output.** For each query,

$$S(r_1, c_1, r_2, c_2) = \sum_{i = r_1}^{r_2} \sum_{j = c_1}^{c_2} M[i][j].$$

**Inclusion and exclusion.** Let $P[i][j]$ be the sum of $M$ over the rows $0 \ldots i - 1$ and the columns $0 \ldots j - 1$, so $P[0][\cdot] = P[\cdot][0] = 0$. Then

$$S(r_1, c_1, r_2, c_2) = P[r_2 + 1][c_2 + 1] - P[r_1][c_2 + 1] - P[r_2 + 1][c_1] + P[r_1][c_1]. \tag{1}$$

*Proof.* An entry $(i, j)$ with $i \le r_2$ and $j \le c_2$ is counted in the first term. It is subtracted once for $i < r_1$ and once for $j < c_1$, and added back once when both hold. So its total weight is $1 - [i < r_1] - [j < c_1] + [i < r_1][j < c_1] = (1 - [i < r_1])(1 - [j < c_1])$, which is 1 inside the rectangle and 0 outside. $\square$

## Variants

- **Static.** No updates; build $P$ in $O(nm)$ time by $P[i+1][j+1] = M[i][j] + P[i][j+1] + P[i+1][j] - P[i][j]$, and answer by (1).
- **Point updates.** A two-dimensional Fenwick tree keeps the values $P[i][j]$ implicitly; both operations cost $O(\log n \log m)$.
- **Rectangle add and point query.** Add $\delta$ to a whole rectangle. On the two-dimensional difference array, this is four point updates, and a point query is a prefix sum.
- **Rectangle add and rectangle sum.** Four two-dimensional Fenwick trees, over $d[i][j]$, $i\,d[i][j]$, $j\,d[i][j]$ and $ij\,d[i][j]$, generalize the two-tree method of [range update range query](/range-update-range-query/).
- **Sparse points.** The input is $N$ weighted points with large coordinates. Offline, sort the points and the query corners and sweep with a one-dimensional Fenwick tree, in $O((N + q) \log N)$ time; see [offline orthogonal range counting](/offline-orthogonal-range-counting/). Online, use a [range tree](/range-tree/) or a Fenwick tree over compressed coordinates with sorted lists.
- **Higher dimensions.** In $d$ dimensions, (1) has $2^d$ terms, and the Fenwick tree costs $O(\log^d n)$ per operation.
- **Other operations.** For $\min$ or $\max$, which have no inverse, (1) fails; use a two-dimensional segment tree or a two-dimensional sparse table.

## Examples

Let

$$M = \begin{pmatrix} 2 & 1 & 4 & 3 \\ 0 & 5 & 2 & 1 \\ 3 & 1 & 6 & 2 \\ 1 & 4 & 0 & 5 \end{pmatrix}, \qquad P = \begin{pmatrix} 0 & 0 & 0 & 0 & 0 \\ 0 & 2 & 3 & 7 & 10 \\ 0 & 2 & 8 & 14 & 18 \\ 0 & 5 & 12 & 24 & 30 \\ 0 & 6 & 17 & 29 & 40 \end{pmatrix}.$$

| query $(r_1, c_1, r_2, c_2)$ | by (1) | sum |
|---|---|---|
| $(1, 1, 2, 3)$ | $P[3][4] - P[1][4] - P[3][1] + P[1][1] = 30 - 10 - 5 + 2$ | 17 |
| $(0, 0, 3, 3)$ | $P[4][4]$ | 40 |
| $(2, 0, 3, 1)$ | $P[4][2] - P[2][2] - P[4][0] + P[2][0] = 17 - 8 - 0 + 0$ | 9 |

The first query covers $5 + 2 + 1$ in row 1 and $1 + 6 + 2$ in row 2, so 17 is right. After add$(2, 1, 3)$, the entry $M[2][1]$ becomes 4, every $P[i][j]$ with $i \ge 3$ and $j \ge 2$ grows by 3, and the first query returns 20. A prefix table must change up to $nm$ entries for this update, which is why the dynamic version needs a tree.

## Known algorithms

| method | build | query | point update | space |
|---|---|---|---|---|
| sum the rectangle | none | $O(nm)$ | $O(1)$ | $nm$ |
| [two-dimensional prefix sums](/two-dimensional-prefix-sums/) | $O(nm)$ | $O(1)$ | $O(nm)$ | $(n+1)(m+1)$ |
| one prefix-sum array per row | $O(nm)$ | $O(n)$ | $O(m)$ | $n(m+1)$ |
| [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/) | $O(nm)$ | $O(\log n \log m)$ | $O(\log n \log m)$ | $nm$ |
| [two-dimensional segment tree](/two-dimensional-segment-tree/) | $O(nm)$ | $O(\log n \log m)$ | $O(\log n \log m)$ | $O(nm)$ |
| [quadtree](/quadtree/) over the grid | $O(nm)$ | $O(n + m)$ for $n = m$ a power of 2 | $O(\log n)$ | $O(nm)$ |
| offline sweep for $N$ points and $q$ queries | | $O((N + q) \log N)$ in total | | $O(N + q)$ |

The times are worst case. The Fenwick tree is the usual choice for the dynamic version, because it is short, needs no extra space, and has small constants.

## Bounds

**Static.** Reading the matrix costs $\Omega(nm)$, and a query cannot be faster than $O(1)$, so the prefix table is optimal.

**Dynamic.** The case $n = 1$ is the one-dimensional dynamic partial sums problem, so the $\Omega(\log m)$ cell-probe bound of Patrascu and Demaine applies; see the [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/). For $N$ weighted points in the plane under updates, Larsen proved that $\max(t_u, t_q) = \Omega((\log N / \log \log N)^2)$ in the [cell-probe model](/cell-probe-model/) with words of $\Theta(\log N)$ bits, close to the $O(\log^2 N)$ of the nested trees.

## Reductions

- **One dimension to two.** A $1 \times m$ grid is a one-dimensional array.
- **Rectangle sum to four dominance sums.** By (1); see [dominance counting](/dominance-counting/).
- **Rectangle add to point update.** By the two-dimensional difference array: adding $\delta$ to $[r_1, r_2] \times [c_1, c_2]$ is $+\delta$ at $(r_1, c_1)$ and $(r_2 + 1, c_2 + 1)$, and $-\delta$ at $(r_1, c_2 + 1)$ and $(r_2 + 1, c_1)$.
- **Counting points in rectangles.** Put weight 1 on each point; then a rectangle sum is an [orthogonal range count](/orthogonal-range-counting/).

## Applications

- Summed-area tables in graphics and the integral images of computer vision, where the mean of any box of pixels costs four lookups.
- Counting the points, events or objects in a rectangle of a map, with a grid of counts.
- Dynamic programs over grids, such as counting the squares of a matrix whose sum stays below a limit.
- Game maps and spreadsheets, where a region total must stay current under edits.

## References
