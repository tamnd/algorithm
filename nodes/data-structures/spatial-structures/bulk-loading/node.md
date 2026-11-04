---
tag: XZN2ET
kind: problem
slug: bulk-loading
name: Bulk loading
aliases:
- bulk construction
- packed index construction
area: data-structures/spatial-structures
level: advanced
summary: Build a spatial index from a static set of objects faster and more compactly than repeated insertion.
prereqs: [r-tree, external-memory-model]
see_also: [str-packing, hilbert-r-tree, priority-r-tree, bulk-loading-b-tree, external-merge-sort, external-sorting-lower-bound, buffer-tree, object-partitioning]
sources:
  - paper: doi:10.1145/318898.318900
    title: Nick Roussopoulos and Daniel Leifker, Direct spatial search on pictorial databases using packed R-trees, Proceedings of ACM SIGMOD 1985
    locator: the packed R-tree, built by sorting the objects on one coordinate and filling the nodes in that order
  - paper: doi:10.1145/170088.170403
    title: Ibrahim Kamel and Christos Faloutsos, On packing R-trees, Proceedings of the Second International Conference on Information and Knowledge Management (CIKM), 1993
    locator: packing by the Hilbert order of the rectangle centers, compared with the low-x packing
  - paper: doi:10.1109/ICDE.1997.582015
    title: Scott T. Leutenegger, Mario A. Lopez and Jeffrey Edgington, STR, a simple and efficient algorithm for R-tree packing, Proceedings of the 13th International Conference on Data Engineering (ICDE), 1997
    locator: the sort-tile-recursive algorithm and its experimental comparison with Hilbert and low-x packing
  - paper: doi:10.1145/1007568.1007608
    title: Lars Arge, Mark de Berg, Herman J. Haverkort and Ke Yi, The priority R-tree, a practically efficient and worst-case optimal R-tree, Proceedings of ACM SIGMOD 2004
    locator: the bulk loading of the PR-tree in O((N/B) log_{M/B}(N/B)) I/Os, its optimal window query bound, and the bad cases of the packed Hilbert and STR trees
  - paper: doi:10.1145/48529.48535
    title: Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9), 1988
    locator: the sorting bound Θ((N/B) log_{M/B}(N/B)) I/Os in the external memory model
---

Bulk loading is the problem of building an index, most often an [R-tree](/r-tree/), from a set of objects that is known in full before the index is used. Inserting the $N$ objects one by one costs $\Theta(\log_B N)$ disk reads each, leaves the nodes partly full, and gives a tree whose shape depends on the insertion order. A bulk loader instead sorts or partitions the objects once, fills each node to capacity, and builds the tree level by level, in about the cost of sorting: $O((N/B) \log_{M/B}(N/B))$ I/Os in the [external memory model](/external-memory-model/). Its goals are speed of the build, full nodes, and a grouping with small [overlap and dead space](/overlap-and-dead-space/), so that later queries are fast.

## In plain words

Suppose you must file ten thousand cards into boxes, and you have all the cards in front of you. Filing them one at a time, each into the box that looks best at that moment, is slow, and leaves many boxes half empty.

It is better to sort all the cards first, then fill each box to the top, in order. For a map, sorting is harder, because a map has two directions. One good way is to sort the cards by east to west, cut them into strips, sort each strip by north to south, and fill boxes from each strip. Each box then holds cards from a small, square-like part of the map. Then you put the boxes into bigger boxes the same way.

## Definition

**Input.** A set of $N$ objects in $\mathbb{R}^d$, each given by its [minimum bounding rectangle](/minimum-bounding-rectangle/), and a node capacity $B$. In the external memory model, a disk block holds $B$ entries and the memory holds $M \ge 2B$ entries.

**Output.** An R-tree on the objects: a tree in which each leaf holds up to $B$ object entries, each internal node holds up to $B$ entries of children with their MBRs, and all leaves are at the same depth. A *packed* tree has every node full except at most one per level, so it has $\lceil N/B \rceil$ leaves and height $\lceil \log_B N \rceil$.

**Goals.** Three measures matter:

1. the I/O cost and time of the build;
2. the space, that is, the fill of the nodes;
3. the quality of the tree: the expected or worst-case number of nodes that a query visits, which depends on the area, perimeter and overlap of the node rectangles.

A bulk loader is good when it builds in about the cost of sorting, fills the nodes, and gives queries at least as fast as a tree built by insertion.

## Variants

- **Static load.** Build once from a static set, the main case. A packed tree from a static load may later take insertions with a normal R-tree insert, but the nodes are full and the first inserts cause splits.
- **Bulk insertion.** Add a large batch to an existing tree, either by building a small tree on the batch and merging it in, or by buffering the inserts as in a [buffer tree](/buffer-tree/).
- **Bottom-up against top-down.** A bottom-up loader groups the objects into leaves and then groups the leaves the same way. A top-down loader splits the whole set into $B$ parts, recurses into each part, and so chooses the split at each level for the whole set.
- **Other index types.** The same problem exists for a [B-tree](/bulk-loading-b-tree/), where it reduces to sorting, and for k-d trees, grid files and quadtrees, where the cuts are chosen from the full set by medians.
- **Worst-case optimal loading.** Build a tree whose window queries meet the best worst-case bound for R-trees, as the [priority R-tree](/priority-r-tree/) does.

## Examples

**Packing a grid.** Take the $N = 16$ points $(i, j)$ with $i, j \in \{0, 1, 2, 3\}$ and $B = 4$, so the packed tree has 4 leaves and a root.

| method | how the leaves are formed | the four leaf MBRs | each leaf |
|---|---|---|---|
| low-x packing | sort by $x$, then $y$; fill leaves of 4 in order | $[i, i] \times [0, 3]$ for $i = 0, 1, 2, 3$ | area 0, perimeter 6 |
| STR | $\lceil 16/4 \rceil = 4$ leaves; $S = \lceil \sqrt 4 \rceil = 2$ slices of $S B = 8$ points by $x$; sort each slice by $y$, fill leaves of 4 | $[0,1] \times [0,1]$, $[0,1] \times [2,3]$, $[2,3] \times [0,1]$, $[2,3] \times [2,3]$ | area 1, perimeter 4 |
| Hilbert packing | sort by the Hilbert index of the [Hilbert curve](/hilbert-curve/) of order 2, fill leaves of 4 | the same four $2 \times 2$ squares, since the indices 0 to 3, 4 to 7, 8 to 11 and 12 to 15 each fill one quadrant | area 1, perimeter 4 |

A query with the strip $[-1, 4] \times [1.2, 1.8]$, which holds no point, meets all four leaf MBRs of the low-x tree, and none of the STR or Hilbert leaves. The low-x leaves are long and thin, so they meet many queries. This is why low-x packing, the first method, gave way to the others.

**Insertion against loading.** Inserting points one by one into an R-tree with $B = 4$ and the [quadratic split](/quadratic-split/) splits a leaf each time it gets a 5th entry, and each split leaves two leaves with 2 or 3 entries. So the tree has more than the $\lceil N/B \rceil$ leaves of a packed tree. Trees built by insertion are often reported to be about 70% full on large data, so a packed tree needs about 30% fewer pages.

## Known algorithms

- **Low-x packing** (Roussopoulos and Leifker, 1985). Sort the objects by the $x$ coordinate of their centers and fill the leaves in that order; repeat on the leaf MBRs. It is fast, but makes thin slabs, which are good for point queries in $x$ and bad for most others.
- **Hilbert packing** (Kamel and Faloutsos, 1993). Sort by the Hilbert index of the centers and fill the nodes in that order. The [Hilbert R-tree](/hilbert-r-tree/) is the dynamic form. One sort, $O(\text{sort}(N))$ I/Os.
- **Sort-tile-recursive** ([STR packing](/str-packing/), Leutenegger, Lopez and Edgington, 1997). In $d$ dimensions, with $P = \lceil N/B \rceil$ leaves, sort by the first coordinate and cut into $\lceil P^{1/d} \rceil$ slabs, then treat each slab the same way on the remaining coordinates, and fill leaves at the last coordinate. It uses $d$ rounds of sorting per level, $O(\text{sort}(N))$ I/Os in total, and it is the default loader of many libraries.
- **Top-down greedy split** (García, López and Leutenegger, 1998). At each node, split the set by the cut along one axis that minimizes a cost, such as the total area of the two parts, and recurse. It gives better trees on skewed data, at a higher build cost.
- **PR-tree** (Arge, de Berg, Haverkort and Yi, 2004). Build a k-d tree like split of the rectangles, seen as points in $2d$ dimensions, and pull out at each node the $B$ rectangles most extreme in each of the $2d$ directions as priority leaves. It loads in $O(\text{sort}(N))$ I/Os and answers any window query in $O((N/B)^{1 - 1/d} + T/B)$ I/Os, where $T$ is the output size.
- **Buffer tree loading.** Insert all objects into a tree with buffers at its nodes, so that inserts are moved down in batches; this gives the tree that repeated insertion would give, but in $O(\text{sort}(N))$ I/Os.

## Bounds

- **Lower bound from sorting.** In the external memory model with indivisible records, sorting $N$ records takes $\Theta((N/B) \log_{M/B}(N/B))$ I/Os ([external sorting lower bound](/external-sorting-lower-bound/)). Bulk loading a B-tree needs this many, by the reduction below.
- **Upper bounds.** Hilbert packing, STR and the PR-tree each run in $O((N/B) \log_{M/B}(N/B))$ I/Os, which meets the sorting bound, and they make $\lceil N/B \rceil$ leaves and $O(N/B)$ nodes in all.
- **Query quality.** For window queries, no R-tree can guarantee fewer than $\Omega((N/B)^{1 - 1/d} + T/B)$ I/Os in the worst case, and the PR-tree meets this. Arge and others built inputs on which the packed Hilbert tree and the STR tree visit $\Theta(N/B)$ leaves for a query with $T = 0$, so their worst case is linear, even though they do well on common data.

## Reductions

- **From sorting, for B-trees.** Given $N$ keys, build a B-tree by any bulk loader; an in-order walk of the leaves then lists the keys in sorted order in $O(N/B)$ I/Os, since the leaves can be read in order through their parent pointers in a number of I/Os linear in the number of nodes. So a loader faster than sorting would give a sort faster than the lower bound.
- **To sorting.** In the other direction, a B-tree loader is a sort followed by one pass that fills the leaves and builds each level from the one below; see [bulk loading a B-tree](/bulk-loading-b-tree/). Hilbert packing reduces R-tree loading in the same way to sorting by one key. STR reduces it to $d$ rounds of sorting.
- **To one-dimensional order.** Any linear order of the objects, such as a space-filling curve order, gives a packed R-tree by filling the nodes in that order; the quality of the tree is then the locality of the order.

## Applications

- Building the spatial index of a database table after a large load, when the index is created on data that is already there.
- Static map and geographic data, which is built once and queried often, such as the tiles of a map server.
- Indexes for a [spatial join](/spatial-join/), where one or both inputs have no index and a packed tree is built for the join.
- In-memory indexes in libraries, for example the STR tree of a geometry library, used for many queries on a fixed set of shapes.
- Bounding volume hierarchies in graphics, which are built top down from the whole scene in each frame or once per scene, by the same ideas.

## References
