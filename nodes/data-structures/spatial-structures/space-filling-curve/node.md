---
tag: XPW4GF
kind: concept
slug: space-filling-curve
name: Space-filling curve
aliases:
- Peano-type curve
- space filling curve
area: data-structures/spatial-structures
level: core
summary: Continuous surjection from the unit interval onto a higher-dimensional region, used to linearize space.
see_also: [z-order-curve, hilbert-curve, peano-curve, hilbert-r-tree, linear-quadtree, geohash, s2-cell-hierarchy, bulk-loading]
sources:
  - book: isbn:9780387942650
    title: Hans Sagan, Space-Filling Curves, Springer, 1994
    locator: Chapter 1 (the definition, and the theorem of Netto that no continuous bijection exists) and the chapters on the curves of Hilbert, Peano, Sierpiński and Lebesgue
  - book: isbn:9783642310454
    title: Michael Bader, Space-Filling Curves, an Introduction with Applications in Scientific Computing, Springer, 2013
    locator: the chapters on the Hilbert and Peano curves (grammars and arithmetic for the iterations), on locality properties (Hölder continuity), and on applications to the ordering and partitioning of grids
  - paper: "Giuseppe Peano, Sur une courbe, qui remplit toute une aire plane, Mathematische Annalen 36, 1890, pp. 157 to 160"
    title: Giuseppe Peano, Sur une courbe, qui remplit toute une aire plane, 1890
    locator: the whole paper (the first curve that fills a square, defined by ternary digits)
  - paper: "David Hilbert, Über die stetige Abbildung einer Linie auf ein Flächenstück, Mathematische Annalen 38, 1891, pp. 459 to 460"
    title: David Hilbert, Über die stetige Abbildung einer Linie auf ein Flächenstück, 1891
    locator: the whole paper (the geometric construction by repeated division into four squares)
  - paper: doi:10.1145/76359.76361
    title: Loren K. Platzman and John J. Bartholdi III, Spacefilling curves and the planar travelling salesman problem, Journal of the ACM 36(4), 1989, pp. 719 to 737
    locator: the heuristic that visits points in the order of a space-filling curve and its bound of O(log n) times the optimal tour
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 1, the section on space-ordering methods (row order, Morton order, Peano-Hilbert order and others)
---

A space-filling curve is a continuous map from the unit interval $[0, 1]$ onto a region of higher dimension, such as the unit square, so that its image covers every point of the region. Peano found the first one in 1890, and Hilbert gave a simpler geometric one in 1891. In computing, the finite stages of such a curve give an order on the cells of a grid in which cells that are close in the order are close in space. This turns multidimensional data into a sequence that can be sorted, stored in a [B-tree](/b-tree/), cut into equal pieces, or scanned with good cache use. The [Z-order curve](/z-order-curve/) and the [Hilbert curve](/hilbert-curve/) are the two orders used most.

## In plain words

Think of a very long thread that you lay on a square sheet in a fixed pattern. Lay it so that it passes through every small square of a grid once. If you make the grid finer and finer, and the thread follows the same rule at each level, then in the limit the thread passes through every point of the sheet.

Computers use the thread at a fixed level. The thread puts the small squares in a line. Squares that are next to each other on the thread are near each other on the sheet. So if you sort your data by the position on the thread, data that is near in space is mostly near in the sorted list.

## The idea

**The curve.** A *curve* is a continuous map $f : [0, 1] \to \mathbb{R}^d$. It is *space-filling* if its image has positive area (positive volume for $d \ge 3$); the classic curves map $[0, 1]$ onto the whole square $[0, 1]^2$. Such a map cannot be one to one: by a theorem of Netto, a continuous bijection from $[0, 1]$ onto $[0, 1]^2$ does not exist, since its inverse would be continuous too, and removing one inner point disconnects the interval but not the square. So some points of the square have two or more preimages.

**Construction by subdivision.** The common curves are defined by a recursive rule. For the Hilbert curve: cut the square into 4 subsquares and the interval into 4 subintervals; map the $k$-th subinterval into the $k$-th subsquare, in an order in which each subsquare shares an edge with the next; and inside each subsquare, use a rotated or mirrored copy of the same rule, chosen so that the end of one piece meets the start of the next. The Peano curve does the same with 9 subsquares in a $3 \times 3$ pattern. The point $f(t)$ is the single point in the nested squares chosen by the digits of $t$ in base 4 (or base 9). The nested squares shrink to a point, which gives continuity.

**The discrete order.** Stop the recursion at level $D$: the curve then visits the $4^D$ cells of a $2^D \times 2^D$ grid in a fixed order. The index of a cell in that order is its *key*. It can be computed from the bits of the coordinates in $O(D)$ steps, by reading off at each level which subsquare holds the cell and how the copy is turned. The key of an aligned block of side $2^k$ is a prefix of length $2(D - k)$ bits, and the cells of the block form one run of $4^k$ keys. This holds for every curve built by subdivision into quadrants, not only for the Z-order.

**Locality.** If two keys are close, the cells are close: for the Hilbert curve, cells whose keys differ by $m$ are at distance $O(\sqrt{m})$, which is the discrete form of the fact that the curve is Hölder continuous with exponent $1/2$. In $d$ dimensions the exponent is $1/d$. The converse is false for every curve: some cells that share an edge get keys that are far apart, because a curve must cross each boundary between the halves of the grid only a few times. Curves differ in their constants, and in whether consecutive cells always share an edge. The Hilbert and Peano orders do; the Z-order does not, since it jumps at the end of each Z.

**Box queries.** A box query on the key order becomes a set of key intervals, one for each run of cells of the box. The number of runs grows with the size of the boundary of the box, and the Hilbert order makes fewer runs than the Z-order on average.

## Examples

**Z-order and Hilbert order on a $4 \times 4$ grid.** The two tables give the key of each cell, with $y$ going up.

| Z-order | x = 0 | x = 1 | x = 2 | x = 3 | | Hilbert | x = 0 | x = 1 | x = 2 | x = 3 |
|---|---|---|---|---|---|---|---|---|---|---|
| y = 3 | 10 | 11 | 14 | 15 | | y = 3 | 5 | 6 | 9 | 10 |
| y = 2 | 8 | 9 | 12 | 13 | | y = 2 | 4 | 7 | 8 | 11 |
| y = 1 | 2 | 3 | 6 | 7 | | y = 1 | 3 | 2 | 13 | 12 |
| y = 0 | 0 | 1 | 4 | 5 | | y = 0 | 0 | 1 | 14 | 15 |

In both, each $2 \times 2$ quadrant holds four consecutive keys. In the Hilbert order, each key is next to the key before it, so the path through the 16 cells has length 15. In the Z-order, the path has jumps, such as from key 7 at $(3, 1)$ to key 8 at $(0, 2)$, a distance of $\sqrt{10}$, and its total length is about 19.65. On a $16 \times 16$ grid, the lengths are 255 for the Hilbert order and about 397 for the Z-order.

**Row order is not a space-filling order.** Ordering cells row by row is also a bijection onto the keys, but cells $(x, y)$ and $(x, y + 1)$ are always $2^D$ keys apart, and no square block larger than one cell is a run. Space-filling orders are used because the blocks of every size are runs.

**The Peano curve.** It divides the square into 9 subsquares in a $3 \times 3$ pattern and goes through them in a serpentine order, up the first column, down the second and up the third, with the copies mirrored so that the pieces join. See the [Peano curve](/peano-curve/).

**A travelling salesman tour.** Visit the points in the order of their Hilbert keys. Platzman and Bartholdi showed that for $n$ points in the plane this tour is at most $O(\log n)$ times the optimal tour, and much closer on random points, after an $O(n \log n)$ sort.

## Where it is used

- **Spatial indexes.** Sort objects by the key of their center and store them in a B-tree, as in the [Hilbert R-tree](/hilbert-r-tree/), or store the blocks of a quadtree by their keys, as in the [linear quadtree](/linear-quadtree/). Geographic cell systems name their cells by keys: the [geohash](/geohash/) by the Z-order, and the [S2 cell hierarchy](/s2-cell-hierarchy/) by the Hilbert order on each face of a cube.
- **Bulk loading.** Sorting by key and cutting the sorted list into pages gives a fast [bulk loading](/bulk-loading/) of R-trees, with leaves that are compact in space.
- **Load balancing.** In parallel scientific codes, cutting the key order of the cells of a mesh into $p$ equal pieces gives each processor a compact part with little boundary, and the cut is cheap to redo when the mesh changes.
- **Memory and cache layout.** Storing a matrix, an image or a texture in key order keeps each aligned block in one run of memory, which helps blocked algorithms and the [cache-oblivious model](/cache-oblivious-model/).
- **Scanning and dithering.** Scanning an image along a Hilbert curve keeps nearby pixels close in time, which is used in image compression and in error diffusion.

## References
