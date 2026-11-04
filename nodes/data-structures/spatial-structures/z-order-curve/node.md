---
tag: D0P36Z
kind: concept
slug: z-order-curve
name: Z-order curve
aliases:
- Morton order
- Morton code
- Lebesgue curve
area: data-structures/spatial-structures
level: core
summary: Space-filling order that interleaves coordinate bits to map multidimensional points to one dimension.
prereqs: [space-filling-curve, bit-interleaving]
see_also: [morton-encoding, hilbert-curve, linear-quadtree, geohash, region-quadtree, octree, s2-cell-hierarchy, cache-oblivious-model]
sources:
  - paper: "G. M. Morton, A computer oriented geodetic data base and a new technique in file sequencing, IBM technical report, Ottawa, 1966"
    title: G. M. Morton, A computer oriented geodetic data base and a new technique in file sequencing, IBM, 1966
    locator: the interleaving of the bits of two coordinates into one key for ordering a file
  - paper: doi:10.1145/588011.588037
    title: Jack A. Orenstein and T. H. Merrett, A class of data structures for associative searching, Proceedings of the 3rd ACM SIGACT-SIGMOD Symposium on Principles of Database Systems (PODS), 1984
    locator: the z order of points and of the elements of a grid, and range search by the decomposition of a box into z order intervals
  - paper: "H. Tropf and H. Herzog, Multidimensional range search in dynamically balanced trees, Angewandte Informatik 23(2), 1981, pp. 71 to 77"
    title: Tropf and Herzog, Multidimensional range search in dynamically balanced trees, 1981
    locator: the computation of the next z value inside a query box (the BIGMIN step) for range search on a one-dimensional index
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 1, the section on space-ordering methods and bit interleaving, and Chapter 2, the sections on the linear quadtree and locational codes
  - book: isbn:9783642310454
    title: Michael Bader, Space-Filling Curves, an Introduction with Applications in Scientific Computing, Springer, 2013
    locator: the chapter on further space-filling curves, the part on the Lebesgue curve and Morton order
---

The Z-order curve orders the cells of a $2^D \times 2^D$ grid, and in general the points of a $d$-dimensional grid, by interleaving the bits of their coordinates into one integer, the *Morton code*. The order visits the four quadrants of a square one after the other, in a Z shape, and does the same inside each quadrant, so it is the preorder of the leaves of a complete [quadtree](/quadtree/). Each aligned square block of side $2^k$ is a run of $4^k$ consecutive codes, which lets a one-dimensional index such as a [B-tree](/b-tree/) store multidimensional data and answer box queries with a few range scans. It was described by G. M. Morton in 1966; as a curve on the unit square it goes back to Henri Lebesgue.

## In plain words

You have a map cut into small squares, and you want to put the squares in one long list so that squares that are near on the map are mostly near in the list.

Cut the map into four parts and number them in a Z: bottom left, bottom right, top left, top right. Inside each part, cut again into four and number again in a Z. Keep going down to the small squares. The list goes through each part completely before it moves to the next part.

There is a fast way to get the number of a square: write its column and row in binary, and take their bits one at a time from each, in turn. The result is the position of the square in the list.

## The idea

Take a point with integer coordinates $x = (x_{D-1} \ldots x_1 x_0)_2$ and $y = (y_{D-1} \ldots y_1 y_0)_2$. Its Morton code is the $2D$ bit integer
$$z(x, y) = (y_{D-1}\, x_{D-1}\, y_{D-2}\, x_{D-2} \ldots y_0\, x_0)_2 = \sum_{i=0}^{D-1} \left( x_i\, 2^{2i} + y_i\, 2^{2i+1} \right).$$
In $d$ dimensions, bit $i$ of coordinate $t$ goes to bit $d\,i + t$ of the code. The map $z$ is one to one from the grid $\{0, \ldots, 2^D - 1\}^2$ onto $\{0, \ldots, 4^D - 1\}$, and its inverse takes the even bits and the odd bits apart. The operation is [bit interleaving](/bit-interleaving/), and fast ways to compute it, with masks and shifts or with a table, are on the [Morton encoding](/morton-encoding/) page.

**Prefixes are blocks.** The top two bits of the code are the top bits of $y$ and $x$, so they tell which quadrant of the grid holds the point. The next two bits tell the quadrant inside that quadrant, and so on. So the first $2(D - k)$ bits of the code name an aligned block of side $2^k$, and the points of that block are exactly the codes with that prefix: a run of $4^k$ consecutive integers. This is why the Z-order is the order of the leaves of a complete quadtree, visited with the children in the order 0, 1, 2, 3, and why a node of a quadtree can be stored as a *locational code*, a prefix and its length.

**Locality, one way.** Points in the same small block have close codes. The other way fails: two cells that are next to each other on the map can be far apart in the order, when they lie on two sides of a high level boundary. Cells $(2^{D-1} - 1, y)$ and $(2^{D-1}, y)$ share an edge, but they are in different halves of the grid, and the codes of a whole quadrant can lie between them. The curve also makes long jumps: from code 7 to code 8 in a $4 \times 4$ grid it goes from $(3, 1)$ to $(0, 2)$. The [Hilbert curve](/hilbert-curve/) has no jumps, since consecutive cells always share an edge, and it keeps neighbors closer on average, but its code is harder to compute.

**Box queries as ranges.** A box query becomes a set of intervals of codes. The codes of the box all lie between $z$ of its lower left and $z$ of its upper right corner, since $z$ is monotone in each coordinate, but that interval also holds many codes outside the box. A query on a sorted list of codes can scan the interval and, at each code outside the box, jump to the next code inside the box. Tropf and Herzog called that next code BIGMIN, and gave a way to compute it in $O(D)$ bit steps. Or the box can be split into aligned blocks, each of which is one run.

**Monotone, not order preserving.** If $x \le x'$ and $y \le y'$ then $z(x, y) \le z(x', y')$, since each bit of the code only rises. But a point with a smaller $x$ can have a larger code, so the order is not the order of either coordinate.

## Examples

**The $4 \times 4$ grid.** With $D = 2$, the code is $z = x_0 + 2 y_0 + 4 x_1 + 8 y_1$. The table gives $z$ for each cell, with $y$ going up:

| | x = 0 | x = 1 | x = 2 | x = 3 |
|---|---|---|---|---|
| y = 3 | 10 | 11 | 14 | 15 |
| y = 2 | 8 | 9 | 12 | 13 |
| y = 1 | 2 | 3 | 6 | 7 |
| y = 0 | 0 | 1 | 4 | 5 |

Codes 0 to 3 fill the lower left $2 \times 2$ block, 4 to 7 the lower right one, 8 to 11 the upper left and 12 to 15 the upper right, each in a small Z. For example, $(x, y) = (2, 1)$ has $x = (10)_2$ and $y = (01)_2$, so $z = (y_1 x_1 y_0 x_0)_2 = (0\,1\,1\,0)_2 = 6$.

**A box that splits into runs.** The box $x \in [1, 2]$, $y \in [1, 2]$ holds the cells with codes 3, 6, 9 and 12. The corner codes are $z(1, 1) = 3$ and $z(2, 2) = 12$, and the interval $[3, 12]$ holds 10 codes, of which 4 are in the box. No two of the four codes are consecutive, so the box is 4 runs. From code 4, which is outside the box, the next code in the box (the BIGMIN) is 6.

**A column.** The cells of one column $x = c$ never have consecutive codes, because a change of $y$ by one changes a bit at an odd position. So a box of one column and $k$ rows always splits into $k$ runs. A box of one row splits into runs of at most 2 cells, since only the cells $x = 2m$ and $x = 2m + 1$ of a row have consecutive codes. Boxes that are aligned blocks are one run.

**Three dimensions.** For the octree of a $2^D$ cube, $z = \sum_i (x_i 2^{3i} + y_i 2^{3i+1} + w_i 2^{3i+2})$ for the coordinates $x$, $y$ and $w$. The cube $(1, 1, 1)$ has code 7 and $(2, 0, 0)$ has code 8.

## Where it is used

- **Linear quadtrees and octrees.** The [linear quadtree](/linear-quadtree/) stores the black blocks of a [region quadtree](/region-quadtree/) as sorted Morton codes, with no pointers. Octrees for voxels and for particle codes in physics are often built by sorting points by Morton code.
- **Spatial keys in databases.** Orenstein and Merrett used the z order to store points and grid elements in a B-tree and to answer range queries with interval scans. Many key value stores and column stores use Morton codes, or the [geohash](/geohash/), which is a Morton code of latitude and longitude written in base 32, as their spatial key.
- **Bulk loading and BVH construction.** Sorting objects by the Morton code of their centers puts close objects into the same leaves. This gives fast [bulk loading](/bulk-loading/) of R-trees and the linear construction of a [bounding volume hierarchy](/bounding-volume-hierarchy/) on graphics hardware.
- **Memory layouts.** Storing a matrix or a texture in Morton order keeps each aligned block of side $2^k$ in a contiguous run, so blocked and recursive algorithms use the cache well in the [cache-oblivious model](/cache-oblivious-model/).
- **Grids on the sphere.** Hierarchical cell systems such as the [S2 cell hierarchy](/s2-cell-hierarchy/) use a space-filling curve to number cells; S2 uses the Hilbert curve, and other [discrete global grid systems](/discrete-global-grid-system/), such as the nested numbering of HEALPix, interleave bits as in the Morton order.
- **Near neighbors.** Points close in Morton order are close in space, so sorting by code and looking at a window of the sorted list gives candidates for [approximate nearest neighbor](/approximate-nearest-neighbor/) search in low dimensions. Several copies of the list, each for a shifted copy of the points, cover the cases where near points fall on two sides of a high level boundary.

## References
