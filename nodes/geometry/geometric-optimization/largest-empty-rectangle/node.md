---
tag: CCJB6V
kind: problem
slug: largest-empty-rectangle
name: Largest empty rectangle
aliases:
- maximal empty rectangle
- maximum empty rectangle
- largest empty axis-parallel rectangle
area: geometry/geometric-optimization
level: core
summary: Find the largest-area axis-parallel rectangle inside a box that has no input point in its interior. Simple sweeps take O(n^2) time; the best known bound is O(n log^2 n).
prereqs: [skyline-problem, divide-and-conquer-paradigm]
see_also: [largest-empty-circle, largest-rectangle-in-histogram, minimum-area-enclosing-rectangle, maximum-area-inscribed-triangle, voronoi-diagram, skyline-problem]
sources:
  - paper: doi:10.1016/0166-218X(84)90124-0
    title: A. Naamad, D. T. Lee and W.-L. Hsu, On the maximum empty rectangle problem, Discrete Applied Mathematics 8(3), 1984
    locator: the O(n^2) worst-case algorithm, the O(n^2) bound on the number of maximal empty rectangles, and their expected number O(n log n) for random points
  - paper: doi:10.1137/0215022
    title: Bernard Chazelle, Robert L. Drysdale III and D. T. Lee, Computing the largest empty rectangle, SIAM Journal on Computing 15(1), 1986
    locator: the divide and conquer algorithm in O(n log^3 n) time and O(n log n) space
  - paper: "Alok Aggarwal and Subhash Suri, Fast algorithms for computing the largest empty rectangle, Proceedings of the 3rd ACM Symposium on Computational Geometry, 1987"
    locator: O(n log^2 n) time and O(n) space by divide and conquer with matrix searching
  - paper: "M. Orlowski, A new algorithm for the largest empty rectangle problem, Algorithmica 5, 1990"
    locator: an algorithm in O(n log n + s) time, where s is the number of maximal empty rectangles
---

The largest empty rectangle problem takes $n$ points inside an axis-parallel box and asks for the axis-parallel rectangle of largest area inside the box that has no point in its interior. Points may lie on its sides. The optimum is a maximal empty rectangle, one that cannot grow in any direction, and there are $O(n^2)$ of those; listing them by a sweep gives an $O(n^2)$ algorithm (Naamad, Lee and Hsu 1984). Divide and conquer brings the time to $O(n \log^3 n)$ (Chazelle, Drysdale and Lee 1986) and then $O(n \log^2 n)$ (Aggarwal and Suri 1987). The grid version, the largest block of zeros in a 0-1 matrix, is solved row by row with the [largest rectangle in a histogram](/largest-rectangle-in-histogram/).

## In plain words

A sheet of metal has some holes in it. You want to cut out the biggest rectangular plate with no hole, with its sides parallel to the edges of the sheet. A hole may lie on the edge of the plate but not inside it.

The best plate cannot grow in any direction: each of its four sides is stopped by a hole or by the edge of the sheet. So it is enough to look at the plates that are stuck on all four sides. There are at most about as many of these as there are pairs of holes, and you can find them all by sliding a plate from each hole to the right and shrinking it each time it meets a new hole.

## Definition

Notation: the box is $B = [0, W] \times [0, H]$, and $P$ is a set of $n$ points in $B$. A rectangle $R = [x_1, x_2] \times [y_1, y_2] \subseteq B$ is empty if no point of $P$ lies in its open interior $(x_1, x_2) \times (y_1, y_2)$. It is a maximal empty rectangle if no empty rectangle strictly contains it. The area of $R$ is $(x_2 - x_1)(y_2 - y_1)$.

**Input.** The box $B$ and the points $P$.

**Output.** An empty rectangle of largest area.

**Maximal rectangles.** An empty rectangle is maximal iff each of its four sides lies on the boundary of $B$ or contains a point of $P$ in its relative interior. So the left side of a maximal rectangle has $x_1 = 0$ or $x_1$ equal to the $x$-coordinate of a point, and likewise for the other sides. Every maximal empty rectangle is fixed by its supports, and the largest empty rectangle is maximal, since growing an empty rectangle increases its area.

**Counting.** Take a maximal rectangle whose left side is supported by a point $p$. Its bottom and top are then fixed by its right side: they are the nearest points above and below $p$ among the points with $x$ strictly between $x_1$ and $x_2$. So each pair of a left support and a right support gives at most one maximal rectangle, which bounds their number by $O(n^2)$. The bound is tight, and for $n$ points drawn uniformly at random the expected number is $O(n \log n)$ (Naamad, Lee and Hsu 1984).

General position is not assumed: points may share coordinates, and points on the boundary of $B$ are allowed. Model: real RAM; only comparisons and products of coordinates are used, so the problem can be solved exactly over the rationals.

## Variants

- **Largest empty square.** The largest empty axis-parallel square has its center at a vertex of the $L_\infty$ [Voronoi diagram](/voronoi-diagram/) of the points or on the boundary, so it takes $O(n \log n)$ time.
- **Largest empty circle.** With a circle instead of a rectangle, and the center inside the convex hull, this is the [largest empty circle](/largest-empty-circle/), solved from the Euclidean Voronoi diagram.
- **Any orientation.** If the rectangle may be rotated, the sides are no longer fixed by coordinates of single points, and the known algorithms are slower than for the axis-parallel case.
- **0-1 matrix.** In an $r \times c$ grid of cells, each 0 or 1, the largest all-zero block is found in $O(rc)$ time: for each row, the heights of the zero columns ending there form a histogram, and the [largest rectangle in a histogram](/largest-rectangle-in-histogram/) is found with a stack.
- **Inside a polygon.** The largest axis-parallel rectangle inside a simple or orthogonal polygon, or the largest inscribed rectangle of a convex polygon.
- **Higher dimensions.** Largest empty boxes in $\mathbb{R}^d$; the number of maximal empty boxes is $O(n^d)$.

## Examples

**Five points.** Let $B = [0, 10] \times [0, 10]$ and $P = \{(2, 3), (5, 7), (8, 2), (4, 1), (7, 5)\}$. There are 25 maximal empty rectangles. The largest is $[0, 5] \times [3, 10]$, of area 35: its bottom touches $(2, 3)$, its right side touches $(5, 7)$, and its other sides lie on $B$. The next ones have area 30: $[2, 7] \times [1, 7]$, supported by all four sides at $(2, 3)$, $(7, 5)$, $(4, 1)$ and $(5, 7)$, and the strip $[0, 10] \times [7, 10]$ above $(5, 7)$.

**No points.** The answer is $B$ itself.

**Points on one horizontal line.** For points $(x_i, y_0)$ the rectangles are the two strips above and below the line, and the rectangles that cross the line between consecutive points. The answer is the largest of $W \cdot \max(y_0, H - y_0)$ and $H$ times the largest gap between consecutive $x$-values, including the gaps to $0$ and $W$.

## Known algorithms

| method | time | space |
|---|---|---|
| test all $O(n^4)$ candidate rectangles from the coordinates | $O(n^5)$ | $O(n)$ |
| sweep from each left support (Naamad, Lee and Hsu 1984) | $O(n^2)$ | $O(n)$ |
| same, for uniformly random points | $O(n \log^2 n)$ expected | $O(n)$ |
| list all maximal rectangles (Orlowski 1990) | $O(n \log n + s)$ for $s$ maximal rectangles | $O(n)$ |
| divide and conquer (Chazelle, Drysdale and Lee 1986) | $O(n \log^3 n)$ | $O(n \log n)$ |
| divide and conquer with matrix searching (Aggarwal and Suri 1987) | $O(n \log^2 n)$ | $O(n)$ |

**The sweep.** Sort the points by $x$. For each point $p$, keep the interval $(lo, hi)$, initially $(0, H)$, of heights still open to the right of $p$. Scan the points $q$ with $q_x > p_x$ in $x$-order. If $lo < q_y < hi$, then $[p_x, q_x] \times [lo, hi]$ is an empty rectangle with $p$ on its left side and $q$ on its right side; record it, and shrink the interval: set $hi = q_y$ if $q_y > p_y$, $lo = q_y$ if $q_y < p_y$, and stop if $q_y = p_y$. At the end record $[p_x, W] \times [lo, hi]$. Rectangles whose left side lies on $B$ are found by the same sweep from the right, and the strips that span the whole width are the gaps between consecutive $y$-values. Each scan costs $O(n)$, so the total is $O(n^2)$ after sorting.

**Divide and conquer.** Split the points by the median $x$. A rectangle that crosses the split line is determined by a left part and a right part that agree on the top and bottom supports. The supports form staircases of maximal points on each side of the line, and matching them is a search in a [totally monotone matrix](/row-minima-of-totally-monotone-matrices/), which Aggarwal and Suri solve in $O(n \log n)$ time per level of the recursion.

## Bounds

- **Output size.** The number of maximal empty rectangles is $O(n^2)$, and $\Theta(n^2)$ for some inputs, so any method that lists them all takes $\Omega(n^2)$ time in the worst case. The faster methods find the largest rectangle without listing all maximal ones.
- **Expected size.** For $n$ points drawn uniformly in $B$ there are $O(n \log n)$ maximal empty rectangles in expectation, which is why output-sensitive methods are fast on random data.

## Reductions

- **To maximal rectangles.** The optimum is a maximal empty rectangle, so any method that lists all maximal empty rectangles solves the problem in time proportional to that list plus the listing cost.
- **From the 0-1 matrix problem.** The matrix version is a discrete special case: the 1-cells act as points that block, and the histogram stack gives a linear-time solution in the matrix size.
- **To monotone matrix search.** In the divide and conquer step, the best rectangle across the split line for each left support is a row maximum of a totally monotone matrix.

## Applications

- **Cutting stock.** Cut the largest clean rectangular piece from a sheet of material with defects, such as leather, metal or glass.
- **Chip design.** Find the largest free area on a chip floor plan for placing a new module.
- **Document and image analysis.** Find white space, such as columns and gutters, in a page layout, or the largest region free of features in an image.
- **Databases.** Find large empty regions in the space of two numerical attributes, which shows combinations of values that never occur.

## References
