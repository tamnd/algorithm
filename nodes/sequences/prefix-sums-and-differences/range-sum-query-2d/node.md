---
tag: 0QFSM4
kind: problem
slug: range-sum-query-2d
name: Two-dimensional range sum query
aliases:
- rectangle sum query
- 2D range sum query
area: sequences/prefix-sums-and-differences
level: intro
summary: Given a static grid, answer many queries for the sum over an axis-aligned rectangle.
prereqs: [range-sum-query, inclusion-exclusion-principle]
see_also: [two-dimensional-prefix-sums, two-dimensional-range-sum-query, integral-image, two-dimensional-fenwick-tree, orthogonal-range-counting, two-dimensional-difference-array, maximum-sum-submatrix, range-sum-query]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 9, Range queries, Section 9.1 Static array queries (the two-dimensional generalization of prefix sums)
  - paper: doi:10.1145/800031.808600
    title: "Franklin C. Crow, Summed-area tables for texture mapping, Proceedings of SIGGRAPH 1984, Computer Graphics 18(3), 207-212"
    locator: the summed-area table and the sum over a rectangle from four table entries
  - url: https://leetcode.com/problems/range-sum-query-2d-immutable/
    title: LeetCode 304, Range Sum Query 2D - Immutable
    locator: the problem statement (a fixed matrix and many rectangle sum queries given by two corners)
---

The two-dimensional range sum query gives a grid $a[0 \ldots R-1][0 \ldots C-1]$ of numbers that does not change, and asks for the sum of the entries inside many axis-aligned rectangles. It is the grid form of the [range sum query](/range-sum-query/). Since addition has an inverse, [two-dimensional prefix sums](/two-dimensional-prefix-sums/) answer each rectangle with four table lookups after $\Theta(RC)$ preprocessing, so $q$ queries cost $\Theta(RC + q)$ time, which is optimal. This page is about the static problem; the version with updates is on the page of the [dynamic two-dimensional range sum query](/two-dimensional-range-sum-query/).

## In plain words

You have a fixed table of numbers, such as the population of each square kilometer of a map. People ask for the total inside a rectangle on the map, many times, with different rectangles.

Adding up every cell for each question is slow when the rectangles are large. The problem asks how to prepare the table once so that each question is fast. The standard answer stores, for each cell, the total of everything above and to the left of it. Any rectangle total is then four lookups with plus and minus signs.

## Definition

**Input.** A grid $a[x][y]$, $0 \le x < R$, $0 \le y < C$, over an abelian group $(G, +, 0)$, usually the integers, followed by $q$ queries $(x_1, y_1, x_2, y_2)$ with $0 \le x_1 \le x_2 < R$ and $0 \le y_1 \le y_2 < C$.

**Output.** For each query, the sum

$$\Sigma(x_1, y_1, x_2, y_2) = \sum_{x = x_1}^{x_2} \sum_{y = y_1}^{y_2} a[x][y].$$

**Cost.** Preprocessing time and space that depend only on the grid, then a query time. Let $N = RC$ be the number of cells. In the online form each query is answered before the next is read.

## Variants

- **Half-open rectangles.** $[x_1, x_2) \times [y_1, y_2)$, with the empty rectangle allowed.
- **Counting.** On a 0/1 grid, the sum is the number of marked cells. With points at small integer coordinates, this is static [orthogonal range counting](/orthogonal-range-counting/) on a grid.
- **Higher dimensions.** Box sums in a $d$-dimensional array, with $2^d$ lookups per query.
- **Fixed-size windows.** All sums of $k \times \ell$ windows, as in a box filter: $(R - k + 1)(C - \ell + 1)$ queries of the same shape.
- **No inverse.** Maximum or minimum over a rectangle: two-dimensional range minimum query, solved for example by a two-dimensional sparse table in $O(N \log R \log C)$ space and $O(1)$ query time.
- **Dynamic.** Point updates between queries: see the [two-dimensional range sum query](/two-dimensional-range-sum-query/), with a [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/). Rectangle additions with point reads are the [two-dimensional difference array](/two-dimensional-difference-array/) in batch form.

## Examples

The grid has $R = 4$ rows and $C = 5$ columns:

$$a = \begin{pmatrix} 3 & 0 & 1 & 4 & 2 \\ 5 & 6 & 3 & 2 & 1 \\ 1 & 2 & 0 & 1 & 5 \\ 4 & 1 & 0 & 1 & 7 \end{pmatrix}$$

| query $(x_1, y_1, x_2, y_2)$ | the rectangle | answer |
|---|---|---|
| $(1, 1, 2, 3)$ | rows 1 to 2, columns 1 to 3 | $6 + 3 + 2 + 2 + 0 + 1 = 14$ |
| $(0, 0, 0, 4)$ | the first row | $10$ |
| $(2, 4, 3, 4)$ | the last column, bottom two cells | $5 + 7 = 12$ |
| $(0, 2, 3, 2)$ | column 2 | $1 + 3 + 0 + 0 = 4$ |
| $(3, 0, 3, 0)$ | one cell | $4$ |

The table of [two-dimensional prefix sums](/two-dimensional-prefix-sums/) of this grid and the four-term computation of the first query are on that page.

## Known algorithms

| method | preprocessing | query | space |
|---|---|---|---|
| direct sum | none | $O((x_2 - x_1 + 1)(y_2 - y_1 + 1))$ | $O(1)$ extra |
| a [prefix sum](/prefix-sums/) array per row | $\Theta(N)$ | $O(x_2 - x_1 + 1)$ | $N + R$ |
| [two-dimensional prefix sums](/two-dimensional-prefix-sums/) | $\Theta(N)$ | $O(1)$, 4 lookups | $(R+1)(C+1)$ |
| [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/) | $\Theta(N)$ | $O(\log R \log C)$ | $N$ |

All bounds are worst case on a [word RAM](/word-ram/) with each sum in one word. The row-prefix method is the right choice when the grid is too large to copy and the rectangles are short. The Fenwick tree is only worth its cost when updates mix with the queries.

## Bounds

**Upper bound.** $\Theta(N)$ preprocessing, $(R + 1)(C + 1)$ words, and $O(1)$ worst-case time per query, by two-dimensional prefix sums. In $d$ dimensions the same method needs $\Theta(dN)$ preprocessing and $2^d$ lookups per query.

**Lower bound.** Each algorithm reads every cell in the worst case, since an unread cell could change the answer to the query of the whole grid, and it writes $q$ answers. So $\Omega(N + q)$ time is necessary, and the prefix-sum table is optimal up to a constant factor for fixed $d$.

**The role of subtraction.** The four-term formula subtracts. In the semigroup model, where only additions of stored partial sums are allowed, the cost is higher; the one-dimensional case already needs about $\alpha(n)$ additions per query with linear space, as the [range sum query](/range-sum-query/) page explains.

## Reductions

- **To two-dimensional prefix sums.** $\Sigma(x_1, y_1, x_2, y_2) = S[x_2+1][y_2+1] - S[x_1][y_2+1] - S[x_2+1][y_1] + S[x_1][y_1]$, where $S[i][j]$ is the sum of the top-left $i \times j$ block. One query becomes four prefix values.
- **From the one-dimensional problem.** A grid with one row is an array.
- **From grid point counting.** Points with coordinates in $[0, R) \times [0, C)$ and rectangle counting queries reduce to this problem on the grid of point counts, in $O(N + p)$ time for $p$ points. For sparse points with large coordinates this wastes space, and [offline orthogonal range counting](/offline-orthogonal-range-counting/) with a sweep is better.
- **To an inner loop of other problems.** The [maximum sum submatrix](/maximum-sum-submatrix/) and many search problems over rectangles evaluate $\Theta(R^2 C^2)$ or fewer candidate rectangles in $O(1)$ each.

## Applications

- Image processing: local means and variances, box filters, adaptive thresholds, and the Haar-like features of the Viola and Jones face detector, all from an [integral image](/integral-image/).
- Texture mapping with summed-area tables in computer graphics, the use for which Crow introduced the table in 1984.
- Geographic and density data: the population or the number of events inside a map rectangle.
- Grid puzzles and games: the number of obstacles or resources in a rectangle of the board.

## References
