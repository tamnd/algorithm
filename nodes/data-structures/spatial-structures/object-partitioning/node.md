---
tag: G3TW5T
kind: concept
slug: object-partitioning
name: Object partitioning
aliases:
- data-driven partitioning
area: data-structures/spatial-structures
level: core
summary: Index design that groups the objects themselves into possibly overlapping bounding regions, as in R-trees.
prereqs: [minimum-bounding-rectangle, b-tree]
see_also: [space-partitioning, overlap-and-dead-space, r-tree, bounding-volume-hierarchy, priority-r-tree, kd-tree, spatial-index]
sources:
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, Object-Based and Image-Based Image Representations (the split between methods that aggregate objects into hierarchies of bounding boxes and methods that decompose the space into disjoint cells)
  - paper: doi:10.1145/602259.602266
    title: Antonin Guttman, R-trees, a dynamic index structure for spatial searching, Proceedings of ACM SIGMOD 1984
    locator: Sections 2 and 3 (the R-tree, its covering rectangles, and search that may descend more than one subtree)
  - paper: doi:10.1145/1007568.1007608
    title: Lars Arge, Mark de Berg, Herman J. Haverkort and Ke Yi, The priority R-tree, a practically efficient and worst-case optimal R-tree, Proceedings of ACM SIGMOD 2004
    locator: the window query bound O((N/B)^(1-1/d) + T/B) for the PR-tree and the matching lower bound for any R-tree
---

Object partitioning is a way to build a [spatial index](/spatial-index/): put the objects into groups, describe each group by a simple region that contains it, usually its [minimum bounding rectangle](/minimum-bounding-rectangle/), and build a tree of groups of groups. Each object is stored exactly once, but the regions of siblings may overlap and need not cover the space. The [R-tree](/r-tree/) and the [bounding volume hierarchy](/bounding-volume-hierarchy/) are the main examples. The other design, [space partitioning](/space-partitioning/), cuts the space into disjoint cells, as the [k-d tree](/kd-tree/) and the [quadtree](/quadtree/) do.

## In plain words

You have many shapes on a map and want to find the ones near a spot quickly. One way is to cut the map into pieces and file each shape under the piece it lies in. A shape that lies across a cut then goes into two files, or must be handled apart.

Object partitioning works the other way round. It puts shapes that are close together into a bag, and draws the smallest box around each bag. Then it puts close bags into bigger bags, and so on. Each shape is in exactly one bag. But two boxes may overlap, so a search at one spot may have to open several bags. And a box may hold empty space, so a search may open a bag and find nothing.

## The idea

**The two designs.** Let $O = \{o_1, \ldots, o_n\}$ be a set of bounded objects in $\mathbb{R}^d$. A hierarchical index is a tree whose nodes have regions.

- In *space partitioning*, the regions of the children of a node are disjoint and their union is the region of the node. The cells depend on the data (a k-d tree cuts at medians) or not (a quadtree cuts at midpoints), but they always tile the space. An object that crosses a cell boundary is either cut and stored in each cell it meets, or stored at the smallest node whose cell contains it.
- In *object partitioning*, the leaves hold a partition of $O$ into groups $G_1, \ldots, G_k$, and the region of a node is the bounding region of the objects below it. For bounding rectangles, the region of a node is the MBR of the MBRs of its children. The regions of siblings may overlap, and parts of the space are in no region at all.

**What each object costs.** In object partitioning, an object is in exactly one leaf, so the index takes $O(n)$ space and a query never reports an object twice. In space partitioning, an object stored in many cells costs space, and a query must remove duplicate answers.

**What a query costs.** A query with a region $Q$ visits each node whose region meets $Q$, and tests the objects of each leaf it reaches. In space partitioning, a point query follows one path. In object partitioning, a point query follows every path whose regions contain the point, so the number of paths depends on the [overlap](/overlap-and-dead-space/) of the regions. The design of an R-tree variant is mostly the design of a grouping rule that keeps overlap, dead space and margin small: the [R*-tree](/r-star-tree/), the [Hilbert R-tree](/hilbert-r-tree/) and [STR packing](/str-packing/) differ in this rule.

**Balance.** Because the groups are built from the objects, an object-partitioning tree can be kept balanced as a [B-tree](/b-tree/) is: each node holds between $m$ and $M$ entries, and all leaves are at the same depth. A node of $M$ entries fits in one disk page. A space-partitioning tree has its shape fixed by the cells, so clustered data can make it deep.

**Worst case.** No grouping rule protects object partitioning from bad data, since the overlap may come from the objects themselves. For R-trees, Arge, de Berg, Haverkort and Yi built the PR-tree, which answers a window query with $O((N/B)^{1 - 1/d} + T/B)$ disk reads, where $N$ is the number of rectangles, $B$ the page capacity and $T$ the number of rectangles that meet the query. They also showed that no R-tree does better in the worst case. The output $T$ counts the bounding rectangles that meet the query, not the objects.

## Examples

- **Empty space is skipped.** Take eight points, four in $[1, 4] \times [1, 4]$ and four in $[6, 9] \times [1, 4]$, and two leaves of four points. Object partitioning by $x$ gives the leaf boxes $[1, 4] \times [1, 4]$ and $[6, 9] \times [1, 4]$. A query at the point $(5, 2)$ meets neither box, so it stops at the root. A k-d tree with the cut $x = 5$ has the cells $x \le 5$ and $x > 5$, which cover the plane, so the same query enters the left leaf and scans its four points.
- **An object across a cut.** Add the segment from $(3, 0)$ to $(7, 0)$. A k-d tree with the cut $x = 5$ must store it in both leaves, or at the root. In object partitioning it goes into one leaf, say the left one, whose box grows to $[1, 7] \times [0, 4]$. Now the two leaf boxes overlap in $[6, 7] \times [1, 4]$, and a query there searches both leaves.
- **Overlap that no tree avoids.** Take ten segments with slope $-1$: segment $i$, for $i = 0, \ldots, 9$, joins $(-3, c_i + 3)$ and $(3, c_i - 3)$ with $c_i = 1 + i/9$. Each MBR is $[-3, 3] \times [c_i - 3, c_i + 3]$, and each contains the query box $Q = [-0.1, 0.1]^2$. No segment meets $Q$: for $|x| \le 0.1$ the segment $i$ has $y = c_i - x \ge 0.9$. Every node region contains the MBR of some segment and so contains $Q$. So a query with $Q$ visits every node of every R-tree on these segments and reports nothing.
- **Bounding volume hierarchies.** In ray tracing and collision detection, a [bounding volume hierarchy](/bounding-volume-hierarchy/) groups triangles by object partitioning. Each triangle is in one leaf, so the memory is linear in the scene. A ray may enter two overlapping child boxes and must test both.

## Where it is used

- The [R-tree](/r-tree/) family: the [R*-tree](/r-star-tree/), the [Hilbert R-tree](/hilbert-r-tree/), the [priority R-tree](/priority-r-tree/), the [X-tree](/x-tree/), and the trees with other region shapes, the [SS-tree](/ss-tree/) (spheres) and the [SR-tree](/sr-tree/) (spheres and rectangles).
- Metric trees such as the [M-tree](/m-tree/) and the [ball tree](/ball-tree/), where the regions are balls in a metric space.
- The [bounding volume hierarchy](/bounding-volume-hierarchy/) of graphics and physics engines, used in [collision detection](/collision-detection/) and [ray casting](/ray-casting/).
- [Bulk loading](/bulk-loading/) of a static index, where the grouping is computed in one pass over sorted data.
- The [spatial join](/spatial-join/) of two R-trees, which descends both trees and pairs nodes whose regions meet.

## References
