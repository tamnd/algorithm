---
tag: 19MBBA
kind: data-structure
slug: x-tree
name: X-tree
aliases:
- extended node tree
area: data-structures/spatial-structures
level: research
summary: R-tree variant for high dimensions that avoids overlapping splits by allowing supernodes.
implements: [spatial-index]
model: external-memory-model
complexity:
  vars: {n: the number of stored rectangles, d: the number of dimensions, M: the entries in one block, m: the fewest entries in a non-root node, S: the most entries in any node (at most n), h: the height of the tree}
  time: {search: O(n d), knn: O(n (d + log n)), insert: O(h d^2 S^2), delete: O(n d + m h^2 d^2 S^2)}
  space: {total: O(n d)}
history:
  year: 1996
  people: [Stefan Berchtold, Daniel A. Keim, Hans-Peter Kriegel]
  note: Berchtold, Keim and Kriegel introduced the X-tree at VLDB 1996, after measuring that the overlap of R*-tree directories grows quickly with the dimension.
prereqs: [r-star-tree]
see_also: [r-star-tree, sr-tree, ss-tree, kd-b-tree, overlap-and-dead-space, curse-of-dimensionality, k-nearest-neighbor-search, minimum-bounding-rectangle]
sources:
  - paper: "Stefan Berchtold, Daniel A. Keim and Hans-Peter Kriegel, The X-tree, an index structure for high-dimensional data, Proceedings of the 22nd International Conference on Very Large Data Bases (VLDB), 1996, pp. 28 to 39"
    locator: the measurement of directory overlap in the R*-tree as the dimension grows, the definition of overlap as a fraction of the volume, the supernodes, the split history and the overlap-minimal split, the split algorithm with MAX_OVERLAP and MIN_FANOUT, and the experiments against the R*-tree and the TV-tree
  - paper: doi:10.1145/93597.98741
    title: Norbert Beckmann, Hans-Peter Kriegel, Ralf Schneider and Bernhard Seeger, The R*-tree, an efficient and robust access method for points and rectangles, Proceedings of ACM SIGMOD 1990, pp. 322 to 331
    locator: ChooseSubtree and the split by margin and then overlap, which the X-tree uses as its topological split
  - paper: doi:10.1145/502807.502809
    title: Christian Böhm, Stefan Berchtold and Daniel A. Keim, Searching in high-dimensional spaces, index structures for improving the performance of multimedia databases, ACM Computing Surveys 33(3), 2001, pp. 322 to 373
    locator: the section on the X-tree among the high-dimensional index structures, and the discussion of the effects of high dimensions on the overlap of bounding boxes
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, High-Dimensional Data, the part on the X-tree
---

The X-tree, or extended node tree, is an [R*-tree](/r-star-tree/) for data in many dimensions that refuses to make splits whose boxes overlap a lot. When a directory node overflows, it first tries the usual R*-tree split. If the two new boxes overlap by more than a threshold, it tries a split along an axis on which the children were split before, which tends to separate them cleanly. If that split is unbalanced, it does not split at all: the node becomes a *supernode*, a node that spans several disk blocks and is read as one sequential run. Berchtold, Keim and Kriegel introduced it in 1996, after they measured that the overlap of R*-tree directories grows quickly with the dimension, until most queries must follow several overlapping boxes, and argued that reading one large node is then cheaper than following them all.

## In plain words

An R-tree puts objects into boxes, the boxes into bigger boxes, and so on, and a search opens only the boxes that touch the question. When a box gets too full it is cut in two. In many dimensions the two halves of a cut often overlap a lot, and then a search has to open both, which wastes the tree.

The X-tree checks each cut. If the two halves would overlap too much, it tries a different cut that it remembers worked before. If that one is lopsided too, it does not cut: it lets the box grow bigger than normal. Reading one big box is faster than opening many boxes that overlap.

## The abstract type

The X-tree implements a [spatial index](/spatial-index/) for axis-aligned rectangles in $\mathbb{R}^d$, points being rectangles of zero size: `insert(id, rect)`, `delete(id, rect)`, `search(q)`, which reports the stored rectangles that meet the query rectangle $q$, and `knn(q, k)`, the [$k$ nearest](/k-nearest-neighbor-search/) rectangles to a point $q$.

## Representation

There are three kinds of nodes. A *leaf*, or data node, holds up to $M$ entries (rectangle, id). A *directory node* holds up to $M$ child nodes, each with its [minimum bounding rectangle](/minimum-bounding-rectangle/). A *supernode* is a directory node of $b \ge 2$ blocks, with room for $bM$ children. Each node keeps its MBR and its *split history*, the set of axes along which it, or the node it was split from, was ever split.

**Invariant (X).** (1) Every leaf is at the same depth. (2) Every node other than the root has at least $m$ entries; a leaf has at most $M$, and a directory node of $b$ blocks at most $bM$; an internal root has at least 2 children. (3) The rectangle of each node is the MBR of the rectangles of its entries.

**Overlap.** For the two boxes $R_1$ and $R_2$ of a split, the X-tree measures

$$\operatorname{overlap}(R_1, R_2) = \frac{\operatorname{vol}(R_1 \cap R_2)}{\operatorname{vol}(R_1 \cup R_2)},$$

the fraction of the space covered by the pair that both cover. The paper uses a threshold $\text{MAX\_OVERLAP}$ of about 20%, and a least fanout $\text{MIN\_FANOUT}$ of about 35% for the overlap-minimal split.

## Operations

```pseudo id=main
INSERT(e, level)
L1  u ← root; while height(u) > level:
L2      u ← the child of u chosen as in the R*-tree (least overlap growth above the leaves, else least volume growth)
L3  add e to u
L4  for u and each ancestor, from the bottom: recompute its MBR; then
L5      if it has more entries than its capacity then SPLIT it
SPLIT(u)
L6  a leaf: (axis, G1, G2) ← TOPOLOGICAL-SPLIT(u)
L7  TOPOLOGICAL-SPLIT is the R*-tree split: the axis of least margin sum, then the cut of least overlap
L8  a directory node: try TOPOLOGICAL-SPLIT; if overlap(MBR(G1), MBR(G2)) > MAX_OVERLAP then
L9      A ← the axes in the split history of every child
L10     try the cuts along the axes of A that leave both groups with at least MIN_FANOUT of the entries; take the least overlap
L11     if no such cut has overlap ≤ MAX_OVERLAP then add a block to u and return: u is a supernode
L12 u keeps G1, a new node v gets G2; both get the history of u plus the axis; each gets ⌈size/M⌉ blocks
L13 if u is the root, make a new root with children u and v; else add v to the parent of u
DELETE(id, rect)
L14 find the leaf with (rect, id) through the nodes whose MBRs meet rect; remove the entry
L15 condense as in the R-tree: going up, remove each node with fewer than m entries, keep its entries, and shrink the blocks of the others; then reinsert the kept entries at their heights
L16 while the root is internal with one child, make the child the root
SEARCH(q)
L17 skip a node whose MBR does not meet q; report the entries of a leaf that meet q, or search the children
KNN(q, k)
L18 best-first search with the distance from q to each MBR as the key; stop after k entries
```

**Why the split history helps.** When a node is split along an axis $a$, the two halves are separated along $a$ at that moment, and every node later split from either half inherits $a$ in its history. An axis that is in the history of every child of a directory node is an axis along which all these children came from a single cut. Cutting the directory node along it puts the children from the two sides of that old cut into different groups, and so tends to give two boxes with little overlap. The boxes may grow after the old cut, so the overlap is not always zero, which is why line L11 still measures it.

**Supernodes.** A supernode is stored in consecutive blocks and read with one seek, so its cost in the [external memory model](/external-memory-model/) is about $b$ block transfers, but only one random access. A supernode can grow by one block at each overflow, and it is split again at a later overflow if a good split exists then. In the extreme, for data in very high dimensions with no good splits, the root becomes one supernode over all the leaves, and the X-tree is a linear scan of the leaf boxes.

**Simplifications here.** The paper keeps the split history as a binary tree, and takes the axis at its root; the implementation keeps a set of axes, which has the same root axis in common. The paper also uses the forced reinsertion of the R*-tree; the implementation leaves it out. Neither change affects correctness.

## Example

Take $M = 3$ and $m = 1$, in the plane, and insert these rectangles, given as (lower corner, upper corner), in order:

| id | rectangle | id | rectangle |
|---|---|---|---|
| a | $(3, 0), (8, 3)$ | e | $(9, 6), (12, 7)$ |
| b | $(8, 3), (13, 3)$ | f | $(9, 3), (13, 5)$ |
| c | $(2, 3), (7, 7)$ | g | $(7, 1), (10, 6)$ |
| d | $(9, 5), (9, 7)$ | | |

1. After a, b and c, the root is a leaf. Inserting d makes 4 entries, and the leaf splits along the $y$ axis into $\{a, b\}$ and $\{c, d\}$, below a new root. Both leaves have the history $\{y\}$.
2. Inserting e puts it with c and d. Inserting f overflows that leaf, which splits along $x$ into $\{c\}$ and $\{d, e, f\}$, both with history $\{x, y\}$. The root has three children: $\{a, b\}$, $\{c\}$ and $\{d, e, f\}$.
3. Inserting g goes to the leaf $\{d, e, f\}$, which splits into $\{g\}$ and $\{d, e, f\}$. Now the root has 4 children and overflows.
4. The topological split of the root gives $\{c\}$ with box $[2, 7] \times [3, 7]$, of volume 20, against the rest, with box $[3, 13] \times [0, 7]$, of volume 70. They share $[3, 7] \times [3, 7]$, of volume 16, so the overlap is $16 / (20 + 70 - 16) = 16/74 \approx 21.6\%$, above 20%.
5. The axis common to the histories of all four children is $y$. With 4 entries and a least fanout of 35%, each group needs $\lceil 1.4 \rceil = 2$ entries. Sorted by $y$, the children are $\{a, b\}$, $\{g\}$, $\{c\}$ and $\{d, e, f\}$, and the only cut gives the boxes $[3, 13] \times [0, 6]$ and $[2, 13] \times [3, 7]$, of volumes 60 and 44, sharing $[3, 13] \times [3, 6]$, of volume 30. The overlap is $30/74 \approx 40.5\%$.
6. Neither split is good enough, so the root becomes a supernode of 2 blocks with all four leaves, and the tree keeps height 1. An R*-tree would have split it, and made a tree of height 2 whose two directory boxes overlap on a fifth of their union.

Queries work as in the R-tree. SEARCH($[8, 9] \times [4, 6]$) returns d, e, f and g; KNN($(10, 4)$, 3) returns g and f, which contain the point, and b, at distance 1.

## Correctness

The X-tree changes only the split rule of the R*-tree and the capacity of directory nodes, so the argument of the R-tree goes through with the capacity of a node read as $bM$. A split, of either kind, gives two groups of at least $m$ entries each, and the supernode case only raises the capacity, so after an insertion no node is over capacity and none is under $m$; the depth of the leaves changes only when a new root is made. Every node whose entries change is recomputed from the bottom up, which keeps every MBR exact. Then a search that skips only nodes whose MBR misses $q$ cannot miss a stored rectangle that meets $q$, and the best-first search, whose keys are lower bounds, returns the nearest entries in order. Every loop either moves up a level or handles one of finitely many entries, so every operation stops. The full proof is in the proofs folder.

## Complexity

The model is the [external memory model](/external-memory-model/), or the RAM with $O(d)$ for each rectangle operation. Let $S$ be the largest number of entries in a node; without supernodes $S = M$, and in the worst case $S = n$.

- **Search.** In the worst case every node is read: $O(n d)$, and $O(n (d + \log n))$ for KNN with its heap. In block transfers, a supernode of $b$ blocks costs $b$ transfers but one seek, and this is where the X-tree gains on an R*-tree with heavy overlap, which would read about as many blocks in random order.
- **Insert.** Choosing the subtree at the level above the leaves costs $O(d S^2)$ for the overlap growth. A topological split, done in the plain way, tries $d$ axes, 2 sort orders and $O(S)$ cuts, each costing $O(d S)$ for the two boxes, so $O(d^2 S^2)$; the overlap-minimal split costs no more. With one split per level, an insertion costs $O(h d^2 S^2)$. Prefix and suffix boxes bring the split down to $O(d^2 S \log S)$.
- **Delete.** $O(n d)$ to find the entry in the worst case, plus up to $m h$ reinsertions.
- **Space.** $O(n d)$; the directory has fewer nodes than an R*-tree, since supernodes stand for groups of nodes.

| operation | time | case |
|---|---|---|
| search | $O(n d)$ | worst |
| $k$ nearest neighbors | $O(n (d + \log n))$ | worst |
| insert | $O(h d^2 S^2)$ | worst |
| delete | $O(n d + m h^2 d^2 S^2)$ | worst |
| space | $O(n d)$ | total |

## Variants

- **R*-tree.** The [R*-tree](/r-star-tree/) is the X-tree without supernodes and split histories: every overflow is split, however much the halves overlap.
- **SS-tree and SR-tree.** The [SS-tree](/ss-tree/) and [SR-tree](/sr-tree/), of the same years, change the shape of the regions to spheres, or spheres and rectangles, rather than the split rule.
- **TV-tree.** The TV-tree of Lin, Jagadish and Faloutsos (1994) uses only a few active dimensions at each level, so that the high levels act on low-dimensional projections.
- **Pyramid technique and VA-file.** Later work by the same group and by Weber, Schek and Blott (1998) maps the data to one dimension, or scans compressed approximations, after the finding that for uniform data in very high dimensions no tree beats a scan.

## When to use it

Use the X-tree for disk-based range and nearest neighbor queries on data of moderate to high dimension, about 4 to 20, where an R*-tree degrades because its directory boxes overlap. In the experiments of the paper, it was much faster than the R*-tree and the TV-tree in high dimensions, and it behaves like an R*-tree in low dimensions, where good splits exist and few supernodes form. In very high dimensions, or for uniformly spread data, it degrades towards a scan of large supernodes, and a sequential scan, a VA-file, or an [approximate](/approximate-nearest-neighbor/) method is then the better choice.

## Pitfalls

- **Supernodes in memory.** In main memory there is no seek to save, and a large supernode is just a long list to test. The X-tree's advantage is about disks.
- **The overlap ratio of empty volume.** Point data gives boxes of zero volume in some axes, and then the ratio is 0/0. Define it, for example as 0, or measure overlap on boxes widened by a small amount; the implementation takes 0 when the union has no volume.
- **History is not a guarantee.** An axis in every child's history gives a separating cut only for the boxes at the time of the old split; later insertions may make them overlap. Measure the overlap of the chosen cut rather than assume it is zero.
- **Shrinking supernodes.** After deletions, a supernode with few entries should give back its blocks. Otherwise the capacity check never fires again and the space is wasted.
- **Thresholds.** MAX_OVERLAP and MIN_FANOUT trade the number of supernodes against overlap. A low MAX_OVERLAP makes many supernodes; a high one gives back the R*-tree.

## Implementations

## History

Berchtold, Keim and Kriegel, at the University of Munich, measured in 1996 that the overlap in the directory of an R*-tree rose quickly with the dimension, so that in high dimensions most queries followed many paths. They argued that for such data, a linear scan of a large node beats a hierarchy of overlapping ones, and designed the X-tree to choose between the two at each node. The paper appeared at VLDB 1996, the same year as the SS-tree and a year before the SR-tree. The group went on to the pyramid technique (1998) and to a cost model for nearest neighbor search in high dimensions, which, with the VA-file paper of Weber, Schek and Blott (1998), made clear how much the curse of dimensionality limits every tree of this kind.

## References
