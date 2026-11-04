---
tag: 4SAGYZ
kind: algorithm
slug: str-packing
name: STR packing
aliases:
- STR packing
- sort-tile-recursive
area: data-structures/spatial-structures
level: advanced
summary: Bulk-loads an R-tree by sorting on one axis, tiling into vertical slices, and recursing on the other axes.
model: external-memory-model
complexity:
  vars: {n: the number of rectangles, M: the node capacity, d: the number of dimensions}
  time: {worst: O(d n log n)}
  space: {total: O(n)}
history:
  year: 1997
  people: [Scott T. Leutenegger, Mario A. López, Jeffrey Edgington]
  note: Leutenegger, López and Edgington introduced Sort-Tile-Recursive at ICDE 1997 and compared it with the nearest-X and Hilbert packings.
prereqs: [r-tree, bulk-loading, sorting-problem]
see_also: [r-tree, hilbert-r-tree, priority-r-tree, bulk-loading, external-merge-sort, r-tree-node-splitting, quadratic-split, z-order-curve]
sources:
  - paper: doi:10.1109/ICDE.1997.582015
    title: Scott T. Leutenegger, Mario A. López and Jeffrey Edgington, STR, a simple and efficient algorithm for R-tree packing, Proceedings of the 13th International Conference on Data Engineering (ICDE), 1997, pp. 497 to 506
    locator: Section 2 (the general packing scheme and the nearest-X and Hilbert sort orders) and Section 3 (the STR order, with P = ceil(r/b) leaves and S = ceil(sqrt(P)) slices, and its form in d dimensions)
  - paper: doi:10.1145/1007568.1007608
    title: Lars Arge, Mark de Berg, Herman J. Haverkort and Ke Yi, The priority R-tree, a practically efficient and worst-case optimal R-tree, Proceedings of ACM SIGMOD 2004
    locator: the introduction and the experiments (inputs on which packed R-trees, among them STR, answer an empty query by visiting a large part of the tree)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, Object-Based and Image-Based Image Representations, the section on bulk loading and packed R-trees
  - paper: doi:10.1145/280277.280279
    title: Volker Gaede and Oliver Günther, Multidimensional access methods, ACM Computing Surveys 30(2), 1998, pp. 170 to 231
    locator: Section 5, the part on the R-tree, its variants and packing methods
---

STR packing, for Sort-Tile-Recursive, builds an [R-tree](/r-tree/) for a fixed set of $n$ rectangles in one pass from the bottom up. It sorts the rectangles by the $x$ coordinate of their centers, cuts the sorted list into about $\sqrt{n/M}$ vertical slices, sorts each slice by $y$, and cuts each slice into runs of $M$, which become the leaves. The same step, applied to the bounding rectangles of the leaves, makes the next level, and so on up to the root. Each node is full except at most one per slice, the leaves are close to squares, and the build costs a few sorts, $O(n \log n)$ time. It was introduced by Leutenegger, López and Edgington in 1997, and it is the bulk load of many spatial libraries.

## In plain words

You have a map with many small boxes on it, all known at the start, and you want to put them into bags of $M$ so that each bag covers a small area.

Cut the map into vertical strips, each with about the same number of boxes. Inside each strip, go from bottom to top and put the next $M$ boxes into a bag. Each bag is then a short piece of a strip, close to a square.

Now treat each bag as one big box, and do the same with the bags, to make bags of bags. Keep going until one bag holds everything. That is the tree.

## The problem

Given $n$ closed rectangles in the plane, or boxes in $\mathbb{R}^d$, each with an identifier, and a node capacity $M \ge 2$, build an R-tree for them: a tree of nodes of at most $M$ entries, with all leaves at one depth and each internal entry holding the bounding rectangle of its child. The goals are full nodes, which give a small height and few pages, and leaf rectangles that are small and overlap little, which give fast queries. This is the [bulk loading](/bulk-loading/) problem for R-trees. Unlike a dynamic R-tree, a packed tree needs no node splits.

## The algorithm

```pseudo id=main
STR(E, M)                                 ▷ E: entries (rectangle, item); start with the input
L1  repeat:                               ▷ one pass builds one level
L2      P ← ⌈|E| / M⌉; S ← ⌈√P⌉           ▷ P nodes on this level, in S slices
L3      sort E by the x coordinate of the center of each rectangle
L4      cut the sorted list into slices of S·M consecutive entries (the last may be shorter)
L5      in each slice: sort by the y coordinate of the center, and cut into runs of M; each run is a new node
L6      E ← the entries (MBR(u), u) for the new nodes u
    until the pass made one node, which is the root

SEARCH(q), as in any R-tree:
L7  for each entry (r, x) of each node reached from the root: if r meets q then
L8      if the node is a leaf then report x
L9      else go into the child x
```

Line L2 chooses the shape: $P$ nodes are needed, and $S$ slices of $S$ nodes each make a grid of about $\sqrt{P} \times \sqrt{P}$ tiles, so the tiles are close to squares when the data is spread evenly. Each slice holds $S \cdot M$ entries, a multiple of $M$, so every node is full except the last node of the last slice. The search is the usual R-tree search: the tree is an R-tree, only built in a different way.

**In $d$ dimensions.** Sort by the first coordinate and cut into $S = \lceil P^{1/d} \rceil$ slabs of $M \cdot \lceil P^{(d-1)/d} \rceil$ entries each; then pack each slab in the same way with the other $d - 1$ coordinates, down to the last one, where the runs of $M$ are cut.

## Example

Take $M = 4$ and 16 points, as rectangles of size zero: A (1, 1), B (2, 7), C (3, 4), D (4, 9), E (5, 2), F (6, 6), G (7, 1), H (8, 8), I (9, 3), J (10, 10), K (11, 5), L (12, 2), M (13, 7), N (14, 4), O (15, 9) and P (16, 1).

**Leaves.** $P = \lceil 16/4 \rceil = 4$ leaves and $S = \lceil \sqrt{4} \rceil = 2$ slices of $2 \cdot 4 = 8$ points.

| slice | points by $x$ | sorted by $y$ | leaves |
|---|---|---|---|
| 1 | A to H ($x$ from 1 to 8) | A, G, E, C, F, B, H, D | {A, G, E, C} with MBR $[1, 7] \times [1, 4]$; {F, B, H, D} with MBR $[2, 8] \times [6, 9]$ |
| 2 | I to P ($x$ from 9 to 16) | P, L, I, N, K, M, O, J | {P, L, I, N} with MBR $[9, 16] \times [1, 4]$; {K, M, O, J} with MBR $[10, 15] \times [5, 10]$ |

The sort by $y$ is stable, so A, at $y = 1$ with the smaller $x$, comes before G.

**Root.** The second pass has 4 entries, $P = 1$, and makes one node: the root, with MBR $[1, 16] \times [1, 10]$. The tree has height 1, 5 nodes, and every node is full.

**Query.** SEARCH($[5, 10] \times [5, 9]$) meets two leaves: $[2, 8] \times [6, 9]$, and $[10, 15] \times [5, 10]$, which it touches along $x = 10$. The other two leaves lie below $y = 5$. In the first, F (6, 6) and H (8, 8) are inside the query, while B and D have $x < 5$. In the second, no point has $x \le 10$ and $y \le 9$. The answer is F and H, after reading the root and two leaves.

## Correctness

The output is an R-tree for the input. Each pass partitions its entries into consecutive runs of at most $M$, so each entry goes to exactly one node, and each node has between 1 and $M$ entries. The rectangle stored for a node is its MBR, by line L6. Each pass makes a level, and the entries of a pass are the nodes of the pass before, so all leaves are at the same depth. The number of entries drops from $k$ to $\lceil k/M \rceil < k$ for $k \ge 2$, so the loop stops with one node. SEARCH is then correct by the containment lemma of the R-tree. The full proof is in the proofs folder.

## Complexity

The model is the RAM for the time, and the [external memory model](/external-memory-model/) for the I/O, with $M$ entries per page.

- **Time.** A pass on $k$ entries sorts them once by $x$ and once by $y$ in slices, $O(k \log k)$. The pass sizes are $n, \lceil n/M \rceil, \lceil n/M^2 \rceil, \ldots$, so the total is $O(n \log n)$, dominated by the first pass. In $d$ dimensions, each pass makes $d$ sorts, $O(d n \log n)$.
- **I/O.** Each sort is an [external merge sort](/external-merge-sort/), so the build costs $O(\frac{n}{B} \log_{Z/B} \frac{n}{B})$ I/Os for a page of $B$ entries and a memory of $Z$ entries, which is the sorting bound. The node capacity $M$ is usually equal to $B$.
- **Space.** Level $j$ has $\lceil n/M^{j+1} \rceil$ nodes, so the tree has fewer than $n/(M - 1) + \lceil \log_M n \rceil + 1$ nodes, and its height is $\lceil \log_M n \rceil - 1$ for $n \ge 2$ (that is, $\lceil \log_M n \rceil$ levels), the least possible for nodes of $M$ entries.
- **Query.** The query cost depends on the data. On points spread evenly in the plane, the leaves are about square tiles of $M$ points, and a window query reads a number of leaves close to the number of tiles it meets. There is no worst-case guarantee: Arge and others give inputs on which STR and the other packings read a large part of the tree for a query with no answer, while the [priority R-tree](/priority-r-tree/) reads $O(\sqrt{n/M} + k/M)$ nodes.

| measure | bound |
|---|---|
| build time | $O(d n \log n)$ |
| build I/O | $O(\frac{n}{B} \log_{Z/B} \frac{n}{B})$ |
| height | $\lceil \log_M n \rceil - 1$ for $n \ge 2$ |
| nodes | about $n/(M - 1)$, all full but at most one per level |

## Properties

- **Full nodes.** Every node except the last of each level is full, so the space use is close to 100%, against about 70% for a dynamic R-tree.
- **Minimal height.** The tree has $\lceil \log_M n \rceil$ levels for $n \ge 2$, the fewest possible.
- **Static.** The tree is an ordinary R-tree, so it accepts later inserts and deletes with the usual algorithms, but the full nodes split at the first insert, and the quality slowly drops.
- **Deterministic.** With a stable sort, the tree depends only on the input order of equal coordinates.
- **Ignores extent.** STR sorts by centers. Large rectangles are treated like points, and a leaf that holds one can have a large MBR.

## Variants and improvements

- **Nearest-X.** Sort by $x$ only and cut runs of $M$: Roussopoulos and Leifker in 1985. The leaves are thin vertical strips, which is bad for queries. STR fixes this with the slices.
- **Hilbert packing.** Sort by the [Hilbert curve](/hilbert-curve/) key of the centers and cut runs of $M$: Kamel and Faloutsos in 1993. It is often close to STR, slightly worse on evenly spread points and sometimes better on skewed data. Sorting by the [Z-order](/z-order-curve/) key is similar and simpler.
- **Top-down packings.** Split the whole set into $M$ parts by a cost function, then recurse, as in the top-down greedy split (TGS) of García, López and Leutenegger, or in OMT. These cost more but make better trees for some data.
- **Priority R-tree.** A packing with a worst-case guarantee, $O((n/M)^{1 - 1/d} + k/M)$ nodes per window query. See the [priority R-tree](/priority-r-tree/).
- **Fill factor.** Packing runs of $f M$ with $f < 1$ leaves room for later inserts without splits.

## When to use it

Use STR to build an R-tree when the data is known in advance, as when you load a table, build an index for a map tile, or rebuild an index from time to time. It is much faster than $n$ inserts, it makes a smaller tree, and its queries are usually better than those of a dynamic tree. Use the [priority R-tree](/priority-r-tree/) when adversarial or very skewed data is a risk, and use a dynamic insert, such as the [R*-tree](/r-star-tree/), for data that changes all the time.

## Pitfalls

- **Wrong slice size.** The slice must hold $S \cdot M$ entries, a multiple of $M$. With slices of $\lceil n/S \rceil$ entries, the cuts inside a slice no longer line up, and many nodes are not full.
- **Sorting by corners.** Sorting by the lower left corner instead of the center works, but large rectangles then pull leaves to the left. Use the center, as in the paper.
- **Skewed data.** If most points have nearly the same $x$, the slices are thin and the tiles are long, which hurts queries. STR assumes data that is spread out, and makes no promise otherwise.
- **Recomputing the root.** Stop when a pass makes one node. A loop that stops when the entries fit in one node, and then forgets to make that node, leaves no root.
- **Dimensions above 2.** The slab size uses $\lceil P^{(d-1)/d} \rceil$ nodes, rounded up. Rounding $P^{1/d}$ down leaves too many slabs and partly empty nodes.

## Implementations

## History

Roussopoulos and Leifker proposed packed R-trees in 1985, with a sort by $x$. Kamel and Faloutsos packed R-trees along the Hilbert curve in 1993. Leutenegger, López and Edgington introduced Sort-Tile-Recursive at ICDE 1997, and showed that it beats both on evenly spread data and is close to the Hilbert packing on most real data. Arge, de Berg, Haverkort and Yi showed in 2004 that all these packings can be slow in the worst case, and gave the priority R-tree.

## References
