---
tag: 2DFX7M
kind: concept
slug: hilbert-curve
name: Hilbert curve
aliases:
- Hilbert order
- Hilbert space-filling curve
area: data-structures/spatial-structures
level: advanced
summary: Continuous space-filling curve with strong locality, used to order points for spatial indexes.
prereqs: [space-filling-curve, z-order-curve]
see_also: [peano-curve, hilbert-r-tree, morton-encoding, gray-code, s2-cell-hierarchy, linear-quadtree, locality-of-reference, bulk-loading]
sources:
  - paper: doi:10.1007/BF01199431
    title: David Hilbert, Ueber die stetige Abbildung einer Linie auf ein Flächenstück, Mathematische Annalen 38, 1891
    locator: pages 459 and 460 (the construction by repeated division of the interval and the square into four parts, with the figure of the first three steps)
  - book: isbn:9780387942650
    title: Hans Sagan, Space-Filling Curves, Springer, 1994
    locator: Chapter 2, Hilbert's space-filling curve (the definition, continuity and surjectivity, and the analytic description), and the chapters on the Hölder continuity of space-filling curves
  - book: isbn:9783642310454
    title: Michael Bader, Space-Filling Curves, An Introduction with Applications in Scientific Computing, Springer, 2013
    locator: the chapters on the Hilbert curve, its grammar description and the algorithms that map indices to cells, and on the locality of the curve (Hölder continuity)
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley, 2013
    locator: Chapter 16, Hilbert's Curve (the conversion between the distance along the curve and the coordinates, by a state table and by bit operations)
  - paper: doi:10.1109/69.908985
    title: Bongki Moon, H. V. Jagadish, Christos Faloutsos and Joel H. Saltz, Analysis of the clustering properties of the Hilbert space-filling curve, IEEE Transactions on Knowledge and Data Engineering 13(1), 2001
    locator: the number of clusters, runs of consecutive curve cells, that a query region needs under the Hilbert order, compared with other orders
---

The Hilbert curve is a continuous map from the interval $[0, 1]$ onto the unit square, found by David Hilbert in 1891. It is the limit of a sequence of paths: the path of order $m$ visits the $4^m$ cells of a $2^m \times 2^m$ grid one by one, each step going to a cell that shares an edge with the last one, and each path is made of four copies of the one before, turned so that they join end to end. The position of a cell on this path is its *Hilbert index*. Sorting points by Hilbert index puts points that are close in the plane close in the list, more reliably than the [Z-order curve](/z-order-curve/) does, so it is used to order data for [R-trees](/hilbert-r-tree/), disk pages, caches and parallel work.

## In plain words

Draw a square grid and try to walk through every cell exactly once, always stepping to a neighbor, so that cells close on the walk are close on the grid. The Hilbert curve does this in a fixed pattern.

For a grid of two by two cells, walk in a U: up, right, down. For a bigger grid, cut it into four quarters. Walk each quarter with a smaller U-shaped walk, turned so that the end of one quarter's walk is next to the start of the next one. Then repeat this inside each quarter.

The walk number of a cell is its Hilbert index. If you sort points by this number, points that are near each other in the list are near each other on the map.

## The idea

**The discrete curve.** Fix an order $m$ and the grid of cells $(x, y)$ with $0 \le x, y < 2^m$. The Hilbert path $H_m$ is a list of all $4^m$ cells. $H_1$ is $(0,0), (0,1), (1,1), (1,0)$: a U that opens downward. For $m \ge 2$, cut the grid into four quadrants of side $s = 2^{m-1}$ and visit them in the order lower left, upper left, upper right, lower right. Each quadrant is walked by a copy of $H_{m-1}$:

- the lower left copy is reflected in the diagonal $x = y$, so it starts at the corner $(0, 0)$ and ends next to the upper left quadrant;
- the two upper copies are $H_{m-1}$ moved by $(0, s)$ and $(s, s)$, with no turn;
- the lower right copy is reflected in the other diagonal, so it ends at the corner $(2^m - 1, 0)$.

By induction, $H_m$ starts at $(0, 0)$, ends at $(2^m - 1, 0)$, and each two consecutive cells share an edge: inside a copy by induction, and at the three joins because the turns put the end of each copy next to the start of the next one.

**The index.** The Hilbert index $d(x, y) \in \{0, \ldots, 4^m - 1\}$ is the position of the cell in $H_m$. Its base-4 digits, from the top, name the quadrant at each level, in the curve's order. Going from $(x, y)$ to $d$ takes one pass over the $m$ levels, from the top. At level $s = 2^{m-1}, 2^{m-2}, \ldots, 1$:

1. let $r_x = 1$ if $x \ge s$ and $r_y = 1$ if $y \ge s$, else 0;
2. the quadrant number is $q = (3 r_x) \oplus r_y$, which gives 0, 1, 2, 3 for lower left, upper left, upper right, lower right; add $q s^2$ to $d$;
3. replace $x$ and $y$ by $x \bmod s$ and $y \bmod s$, and undo the turn of that quadrant: if $r_y = 0$ and $r_x = 1$, replace $(x, y)$ by $(s - 1 - x, s - 1 - y)$; then, if $r_y = 0$, swap $x$ and $y$.

This takes $O(m)$ word operations; the inverse runs the same steps from the bottom. Butz gave the form for any dimension, and Warren and Skilling give versions with bit operations and a small state table.

**The continuous curve.** Map the interval $[q/4^m, (q+1)/4^m]$ to the $q$-th cell of $H_m$. For each $t \in [0, 1]$, the cells of the intervals that hold $t$, at $m = 1, 2, \ldots$, are nested squares whose sides shrink to 0; they meet in one point $h(t)$. This defines the Hilbert curve $h : [0,1] \to [0,1]^2$. It is onto, since each point of the square lies in a nested sequence of cells; and it is continuous, with a Hölder bound:
$$\lVert h(s) - h(t) \rVert \le 2\sqrt 5\, \lvert s - t \rvert^{1/2}.$$
To see this, pick $m$ with $4^{-(m+1)} < |s - t| \le 4^{-m}$. Then $s$ and $t$ lie in one interval of length $4^{-m}$ or in two consecutive ones, whose cells share an edge and so fit in a $2 \times 1$ box of cells of side $2^{-m}$, of diameter $\sqrt 5 \cdot 2^{-m}$. And $2^{-m} < 2|s - t|^{1/2}$. The exponent $1/2$ cannot be raised: the curve preserves area (see below), so the image of an interval of length $\delta$ has area $\delta$ and diameter at least about $\sqrt \delta$.

**What the curve is not.** It is not one to one: a point on the edges of the cells can lie in the cells of two or more intervals, and so has more than one preimage. By a theorem of Netto, no continuous curve maps $[0, 1]$ onto the square in a one-to-one way. The curve is nowhere differentiable, and it preserves area: the preimage of a set of measure $\mu$ has length $\mu$.

**Locality.** Consecutive cells of $H_m$ share an edge, so a run of the index is a connected region; the Z-order, by contrast, makes long jumps between its quadrants. The other direction does not hold: the neighboring cells $(2^{m-1} - 1, 0)$ and $(2^{m-1}, 0)$ lie in the first and the last quadrant, so their indices differ by more than $4^m / 2$. In practice, a query region is cut into fewer *clusters*, runs of consecutive indices, under the Hilbert order than under the Z-order, which Moon, Jagadish, Faloutsos and Saltz analyzed in 2001. Fewer clusters mean fewer seeks on disk.

## Examples

- **Order 2.** The $4 \times 4$ grid, with $y$ going up, has these indices:

  | $y \backslash x$ | 0 | 1 | 2 | 3 |
  |---|---|---|---|---|
  | 3 | 5 | 6 | 9 | 10 |
  | 2 | 4 | 7 | 8 | 11 |
  | 1 | 3 | 2 | 13 | 12 |
  | 0 | 0 | 1 | 14 | 15 |

  The lower left quadrant holds 0 to 3, walked as $(0,0), (1,0), (1,1), (0,1)$, the U of order 1 reflected in the diagonal. Each step from $d$ to $d + 1$ goes to a neighbor. The cells $(1, 0)$ and $(2, 0)$ are neighbors on the grid but have indices 1 and 14.
- **An index.** For the cell $(5, 2)$ in the $8 \times 8$ grid: at $s = 4$, $r_x = 1$ and $r_y = 0$, so $q = 3$ and $d = 48$; the local cell $(1, 2)$ becomes $(2, 1)$ after the reflection and then $(1, 2)$ after the swap. At $s = 2$, $r_x = 0$ and $r_y = 1$, so $q = 1$ and $d = 52$; the local cell is $(1, 0)$, with no turn. At $s = 1$, $r_x = 1$ and $r_y = 0$, so $q = 3$ and $d = 55$.
- **Z-order against Hilbert.** In the $4 \times 4$ grid, the query box $[1, 2] \times [1, 2]$ holds the Hilbert indices 2, 7, 8, 13, which form 3 runs, and the Morton codes 3, 6, 9, 12, which form 4 runs. The box $[0, 1] \times [1, 2]$ holds the Hilbert indices 2, 3, 4, 7, which form 2 runs (2 to 4, and 7), and the Morton codes 2, 3, 8, 9, which also form 2 runs. The difference between the two orders shows in larger queries, where the Z-order has long jumps at every level.

## Where it is used

- **R-trees.** The [Hilbert R-tree](/hilbert-r-tree/) sorts the rectangles by the Hilbert index of their centers, both for [bulk loading](/bulk-loading/) and to choose where an insertion goes.
- **Disk layout and databases.** Storing records in Hilbert order makes a range query read few runs of pages. Some database systems and file formats sort spatial data this way.
- **Geography.** The [S2 cell hierarchy](/s2-cell-hierarchy/) numbers the cells on each face of a cube by a Hilbert curve, so that a cell ID range is a connected area on the sphere.
- **Parallel computing.** Cutting the Hilbert order of the cells of a mesh or a particle set into equal pieces gives each processor a compact region with a short boundary, for load balancing.
- **Cache-friendly loops.** Traversing a matrix or an image in Hilbert order keeps nearby elements in the cache, for [locality of reference](/locality-of-reference/), without knowing the cache size.
- **Image processing.** Scanning an image in Hilbert order for dithering or compression keeps each step between neighboring pixels.

## References
