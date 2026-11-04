---
tag: B6BX68
kind: concept
slug: space-partitioning
name: Space partitioning
aliases:
- space-driven decomposition
area: data-structures/spatial-structures
level: core
summary: Index design that splits the embedding space into disjoint cells regardless of where the data lies.
prereqs: [spatial-index]
see_also: [object-partitioning, uniform-grid, quadtree, kd-tree, bsp-tree, grid-file, overlap-and-dead-space, r-plus-tree]
sources:
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 1, Multidimensional Point Data (grids, quadtrees and k-d trees), and Chapter 2, Object-Based and Image-Based Image Representations (the split between decompositions of the space and of the objects, and the ways to store objects with extent)
  - paper: doi:10.1145/280277.280279
    title: Volker Gaede and Oliver Günther, Multidimensional access methods, ACM Computing Surveys 30(2), 1998, pp. 170 to 231
    locator: Section 4 (point access methods) and Section 5 (the techniques for objects with extent, transformation, overlapping regions, clipping and multiple layers)
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 7, Spatial Partitioning (uniform grids, hierarchical grids, trees of cells such as octrees and k-d trees, and the cost of objects that cross cell boundaries), and Chapter 8 on BSP trees
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: Chapter 5 (k-d trees), Chapter 12 (binary space partitions) and Chapter 14 (quadtrees)
---

Space partitioning is the design of a [spatial index](/spatial-index/) that divides the space itself into disjoint cells that together cover it, and stores each object in the cells it meets. The cells do not depend on how the objects are grouped: a query looks only at the cells it meets, and two cells never share a point, so each point of space has exactly one cell. The other design, [object partitioning](/object-partitioning/), groups the objects and puts a box around each group, as in the [R-tree](/r-tree/), so its regions may overlap but each object is stored once. Grids, quadtrees, k-d trees and BSP trees are space partitions.

## In plain words

There are two ways to sort a big pile of things on a floor so that you can find them later.

The first way is to draw lines on the floor and make boxes of floor. Each thing goes into the box of floor where it lies. Every spot of the floor is in exactly one box, so to find what is at a spot, you look in one box. But a long thing that lies over a line is in two boxes, and you must write it down twice.

The second way is to put close things into bags, and look at the size of each bag. Each thing is in one bag, but two bags can cover the same spot of the floor, so to find what is at a spot, you may have to open both.

Space partitioning is the first way.

## The idea

**Cells.** A space partition of a region $U \subseteq \mathbb{R}^d$ is a set of cells $C_1, \ldots, C_k$ with $C_i \cap C_j = \emptyset$ for $i \ne j$ and $C_1 \cup \cdots \cup C_k = U$. Cells are usually half open boxes, $[a_1, b_1) \times \cdots \times [a_d, b_d)$, so that a point on a boundary has one cell, or convex polygons in a BSP tree. Hierarchical partitions cut each cell again, and their cells form a tree in which the children of a cell partition it.

**Where the cuts go.** In a *regular* partition, the positions of the cuts are fixed in advance: a [uniform grid](/uniform-grid/) cuts at multiples of $h$, and a [quadtree](/quadtree/) cuts each square at its center. Only the depth depends on the data. In an *adaptive* partition, the data chooses the positions: a [k-d tree](/kd-tree/) cuts at the median, a [grid file](/grid-file/) moves its grid lines, and a [BSP tree](/bsp-tree/) cuts along lines through the input segments. Both kinds give disjoint cells. The summary of this page, cells chosen regardless of the data, describes the regular kind in the strict sense, which Samet calls a decomposition of the space as opposed to a decomposition of the objects.

**Locating a point.** Since the cells are disjoint, a point query follows exactly one path: one cell in a grid, by arithmetic, or one root to leaf path in a tree. This is the main gain over object partitioning, where boxes of siblings may overlap and a point query may follow several paths.

**Objects with extent.** A point lies in one cell, but a segment or a polygon may cross many. The design must choose one of these:

- *Clipping*, or duplication: store the object in every cell it meets. Queries stay simple, but an object may be stored many times, deletion must find all copies, and queries must remove duplicates. The [R+-tree](/r-plus-tree/) and [spatial hashing](/spatial-hashing/) do this.
- *Smallest enclosing cell*: store the object in the smallest cell of the hierarchy that contains it. Each object is stored once, but small objects that cross a high cut sit near the root, and every query must check them. The [MX-CIF quadtree](/mx-cif-quadtree/) works this way.
- *Loose cells*: let each cell, for the purpose of storing, extend past its boundary by a fixed factor, so that an object fits the cell of its center at a level that matches its size. The [loose octree](/loose-octree/) works this way.
- *Transformation*: map each box to a point of higher dimension (its two corners), and partition that space instead.

**Empty cells.** A regular partition spends cells on empty space, and its depth can grow without bound when two points are very close. Adaptive partitions follow the data, and a k-d tree on $n$ points has $O(n)$ cells and depth $O(\log n)$. A grid stored in a hash table, as in [spatial hashing](/spatial-hashing/), keeps only the occupied cells.

**Trade-off with object partitioning.** The measures of [overlap and dead space](/overlap-and-dead-space/) state the trade-off: a space partition has zero overlap by construction but may have much dead space and duplicated objects, while an object partition stores each object once but has overlap between sibling regions.

## Examples

Take the square $U = [0, 8)^2$ and the points $p = (1, 1)$, $q = (2, 6)$, $r = (7, 3)$ and $s = (6, 7)$, and the rectangle $R = [3, 5] \times [3, 5]$.

- **Uniform grid of side 4.** The four cells are $[0, 4) \times [0, 4)$ and its three neighbors. Each point lies in one cell: $p$ in the lower left, $q$ in the upper left, $r$ in the lower right and $s$ in the upper right. The rectangle $R$ meets all four cells, so a grid that clips stores it 4 times.
- **Quadtree.** The root square has the same four quadrants. With a capacity of one point per leaf, the quadtree stops at depth 1, the same as the grid. An MX-CIF quadtree stores $R$ at the root, since no quadrant contains it, and every query must look at $R$.
- **k-d tree.** A cut at the median $x$, between 2 and 6, puts $p$ and $q$ on one side and $r$ and $s$ on the other, and then a cut at the median $y$ on each side gives one point per cell. The cells are disjoint and cover $U$, but their sizes follow the data.
- **R-tree, for contrast.** Grouping $\{p, q\}$ and $\{r, s\}$ gives the boxes $[1, 2] \times [1, 6]$ and $[6, 7] \times [3, 7]$. These do not cover $U$: the point $(4, 4)$ is in no box, so a query there stops at once, which a partition cannot do. But if the groups were $\{p, s\}$ and $\{q, r\}$, the boxes $[1, 6] \times [1, 7]$ and $[2, 7] \times [3, 6]$ would overlap, and a query at $(4, 4)$ would search both.

## Where it is used

- **Point data in memory.** [k-d trees](/kd-tree/), [point quadtrees](/point-quadtree/), [PR quadtrees](/pr-quadtree/) and [uniform grids](/uniform-grid/) are the usual structures for range search and near neighbor search on points, since a point lies in exactly one cell.
- **Images and voxels.** A [region quadtree](/region-quadtree/) or an [octree](/octree/) partitions a raster into blocks of one value.
- **Graphics and games.** [BSP trees](/bsp-tree/) give a back to front order of polygons for any viewpoint, grids and octrees speed up [ray casting](/ray-casting/), and grids and [spatial hashing](/spatial-hashing/) are the broad phase of [collision detection](/collision-detection/).
- **Databases.** The [grid file](/grid-file/), the [k-d-B tree](/kd-b-tree/) and the [R+-tree](/r-plus-tree/) bring space partitions to disk pages. Geographic cell systems, such as the [geohash](/geohash/) and the [S2 cell hierarchy](/s2-cell-hierarchy/), partition the sphere into cells with names.
- **Parallel computing.** Partitions of space, often along a [space-filling curve](/space-filling-curve/), give each processor one region of a simulation.

## References
