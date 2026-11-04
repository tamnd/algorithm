---
tag: SKDGZ3
kind: data-structure
slug: r-tree
name: R-tree
aliases:
- rectangle tree
area: data-structures/spatial-structures
level: core
summary: Balanced tree of minimum bounding rectangles for indexing extended spatial objects, as in a disk-based B-tree.
implements: [spatial-index]
model: external-memory-model
complexity:
  vars: {n: the number of stored rectangles, M: the most entries in a node, m: the fewest entries in a non-root node}
  time: {search: O(n), insert: O(M^2 log n / log m), delete: O(n + M^2 log n / log m)}
  space: {total: O(n)}
history:
  year: 1984
  people: [Antonin Guttman]
  note: Guttman introduced the R-tree at ACM SIGMOD 1984, with the linear, quadratic and exhaustive node splits.
prereqs: [b-tree, minimum-bounding-rectangle]
see_also: [r-star-tree, r-plus-tree, quadratic-split, r-tree-node-splitting, str-packing, hilbert-r-tree, priority-r-tree, overlap-and-dead-space]
sources:
  - paper: doi:10.1145/602259.602266
    title: Antonin Guttman, R-trees, a dynamic index structure for spatial searching, Proceedings of ACM SIGMOD 1984, pp. 47 to 57
    locator: Section 2 (the R-tree and its properties), Section 3 (Search, Insert with ChooseLeaf and AdjustTree, Delete with FindLeaf and CondenseTree), Section 3.5 (node splitting) and Section 4 (performance tests)
  - paper: doi:10.1145/280277.280279
    title: Volker Gaede and Oliver Günther, Multidimensional access methods, ACM Computing Surveys 30(2), 1998, pp. 170 to 231
    locator: Section 5, spatial access methods, the part on the R-tree and its variants
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, Object-Based and Image-Based Image Representations (object hierarchies and the R-tree, with insertion, deletion and the splitting rules)
  - paper: doi:10.1145/1007568.1007608
    title: Lars Arge, Mark de Berg, Herman J. Haverkort and Ke Yi, The priority R-tree, a practically efficient and worst-case optimal R-tree, Proceedings of ACM SIGMOD 2004
    locator: the introduction (no worst-case bound for the classic R-tree) and the lower bound for window queries on any R-tree
---

An R-tree is a balanced search tree for rectangles and other objects with extent, in which each node holds between $m$ and $M$ entries, each entry is a [minimum bounding rectangle](/minimum-bounding-rectangle/) and a pointer, and all leaves are at the same depth. It applies the design of the [B-tree](/b-tree/) to space: a node fills one disk page, and a node's rectangle is the smallest box around everything below it. Sibling rectangles may overlap, so a query may have to follow several paths, and the worst case of a query is a scan of the whole tree. Antonin Guttman introduced it in 1984, and it and its variants are the [spatial index](/spatial-index/) of most spatial databases.

## In plain words

You want to store the outlines of thousands of buildings so that you can find the ones in any part of a city. Put each building in the smallest box that holds it. Gather a few nearby boxes into a group, and draw the smallest box around the group. Gather a few groups into a bigger group, and so on, until one box holds everything.

To find the buildings in a window, start at the top. Open each group whose box touches the window, and skip the others. At the bottom, report the buildings whose boxes touch the window.

To add a building, go down into the group whose box needs to grow the least. If a group gets too full, split it into two. Unlike cells of a grid, two group boxes can overlap, so a search sometimes has to open both.

## The abstract type

The R-tree implements a [spatial index](/spatial-index/) for a set of objects, each given by an identifier and a closed rectangle: `insert(id, r)`, `delete(id, r)` and `search(q)`, which reports the identifiers of the stored rectangles that meet the query rectangle $q$. A point query is a search with a rectangle of zero size. For objects of other shapes, the tree stores the bounding rectangle of each object, and a second step tests the exact shape of each candidate.

## Representation

A rectangle in the plane is $r = [x_1, x_2] \times [y_1, y_2]$ with $x_1 \le x_2$ and $y_1 \le y_2$; in $d$ dimensions it has one interval per axis. A node is a *leaf* or *internal*, and holds a list of entries:

- a leaf entry $(r, id)$ holds the rectangle of an object and its identifier;
- an internal entry $(r, c)$ holds a pointer to a child node $c$ and the rectangle $r = \operatorname{MBR}(c)$, the smallest rectangle that contains all rectangles in the entries of $c$.

The parameters are $M \ge 2$, the capacity of a node, and $m$ with $1 \le m \le M/2$, the minimum fill. Guttman uses $m \ge 2$, and $m = 40\%$ of $M$ is common.

**Invariant (R).** (1) Every leaf is at the same depth. (2) Every node other than the root has between $m$ and $M$ entries. The root has at most $M$ entries, and at least 2 if it is internal. (3) The rectangle of each internal entry is the MBR of its child.

Part 3 gives the property that searches use: each stored rectangle in the subtree of an entry lies inside the rectangle of that entry, by induction on the height. Part 2 bounds the height. A tree of height $h \ge 1$ has a root with at least 2 children, internal nodes with at least $m$ children, and leaves with at least $m$ entries, so $n \ge 2 m^h$, and $h \le \log_m(n/2)$ for $m \ge 2$.

## Operations

```pseudo id=main
SEARCH(T, q)                               ▷ report the stored rectangles that meet q
L1  for each entry (r, x) of each node u reached, starting at the root: if r meets q then
L2      if u is a leaf then report x
L3      else go into the child x

INSERT(T, r, id)
L4  u ← CHOOSE-LEAF: from the root, follow the entry whose rectangle needs the least
L5      area enlargement to contain r (ties: the smallest area), down to a leaf
L6  add (r, id) to u
L7  while u is not none:                     ▷ ADJUST-TREE, from the leaf up
L8      if u has M + 1 entries then split u into u and a new node v, with the quadratic split
L9          and add (MBR(v), v) to the parent of u
L10         if u is the root then make a new root with the two entries (MBR(u), u) and (MBR(v), v); stop
L11     update the rectangle of u in its parent to MBR(u); u ← the parent of u
```

SEARCH visits a node only when its rectangle meets $q$. Two rectangles $[a_1, a_2] \times [b_1, b_2]$ and $[c_1, c_2] \times [e_1, e_2]$ meet exactly when $a_1 \le c_2$, $c_1 \le a_2$, $b_1 \le e_2$ and $e_1 \le b_2$. Unlike a B-tree, more than one entry of a node may meet $q$, and SEARCH follows each of them.

INSERT goes down one path, chosen by the least growth of area, since a larger rectangle is met by more queries. If the leaf overflows, line L8 splits its $M + 1$ entries into two groups of at least $m$ with the [quadratic split](/quadratic-split/), and the parent receives one more entry, which may make it overflow in turn. The tree grows only at the root, in line L10, so all leaves stay at one depth, as in a B-tree. The choice of the split is a problem of its own: see [R-tree node splitting](/r-tree-node-splitting/).

```pseudo id=delete
DELETE(T, r, id)
L12 find the leaf u that holds (r, id): search every subtree whose rectangle contains r; if there is none then return false
L13 remove (r, id) from u
L14 CONDENSE-TREE: from u up to the root, if a node has fewer than m entries then remove it from its parent and keep it in a list Q; else update its rectangle in its parent
L15 reinsert each entry of each node in Q at the height of that node, with INSERT
L16 while the root is internal and has one entry: make its child the root
return true
```

Guttman's deletion does not merge an underfull node with a sibling, as a B-tree does. It removes the node and inserts its entries again, which also lets them find better places. Entries of an internal node in $Q$ go back at their old height, so that their leaves stay at the depth of the other leaves.

## Example

Take $M = 4$ and $m = 2$, and insert six rectangles, written as $[x_1, x_2] \times [y_1, y_2]$.

| object | rectangle | object | rectangle |
|---|---|---|---|
| a | $[0, 2] \times [0, 2]$ | d | $[7, 9] \times [6, 9]$ |
| b | $[1, 3] \times [5, 7]$ | e | $[2, 3] \times [1, 3]$ |
| c | $[6, 8] \times [0, 1]$ | f | $[6, 7] \times [7, 8]$ |

| step | what happens | tree after |
|---|---|---|
| insert a, b, c, d | the root is a leaf with room for four | leaf [a, b, c, d] |
| insert e | the leaf has 5 entries and splits. The quadratic split takes as seeds the pair that wastes the most area: a and d, whose MBR $[0, 9] \times [0, 9]$ has area 81 and wastes $81 - 4 - 6 = 71$. Then e goes with a (enlargement 5 against 50), then b with a (12 against 26), and c must go with d to fill it to $m = 2$ | root [$[0,3] \times [0,7]$, $[6,9] \times [0,9]$]; leaves [a, e, b] and [d, c] |
| insert f | the second rectangle already contains f, so its enlargement is 0, against 35 for the first | leaves [a, e, b] and [d, c, f] |
| search $[2.5, 7] \times [2.5, 7]$ | both root rectangles meet the query. In the first leaf, b and e meet it and a does not; in the second, d and f meet it and c does not | b, d, e, f |
| search $[4, 5] \times [3, 5]$ | the query lies in the gap between the two root rectangles | nothing, after reading only the root |
| delete c | the leaf keeps 2 entries; its rectangle shrinks to $[6, 9] \times [6, 9]$ | leaves [a, e, b] and [d, f] |
| delete d | the leaf has 1 entry, fewer than $m$, so it is removed and f is inserted again; the root now has one child, which becomes the root | leaf [a, e, b, f] |

## Correctness

The key fact is part 3 of (R): every stored rectangle in the subtree of an entry lies inside the rectangle of the entry. So if a stored rectangle meets $q$, every rectangle on the path to it meets $q$, and SEARCH reaches it. INSERT keeps (R): the new entry goes into a leaf, ADJUST-TREE resets each rectangle on the path to the MBR of its child, a split makes two nodes of at least $m$ entries, and only a root split adds a level, on top of all leaves at once. DELETE keeps (R): CONDENSE-TREE removes each underfull node and fixes the rectangles above, the reinsertions are INSERTs at the right height, and line L16 removes roots with one child. The full proof is in the proofs folder.

## Complexity

The model is the [external memory model](/external-memory-model/) with one node per disk page, or the RAM with a cost per entry examined.

- **Height.** $h \le \log_m(n/2)$ for $n \ge 2$ and $m \ge 2$, so $h = O(\log n / \log m)$. For $M = 50$ and $m = 20$, a billion rectangles fit in a tree of height at most 6.
- **Search.** In the worst case SEARCH visits every node, $O(n)$, even when it reports nothing: the rectangles may all overlap at the query and not meet it. The [object partitioning](/object-partitioning/) page gives such an input. On practical data the cost is close to a few paths, which is the reason R-trees are used. The [priority R-tree](/priority-r-tree/) is the variant with a worst-case bound, $O((n/M)^{1 - 1/d} + k/M)$ node visits for $k$ answers, and no R-tree can do better.
- **Insert.** CHOOSE-LEAF examines $O(M)$ entries per level, and each split on the path costs $O(M^2)$ for the quadratic split, so $O(M^2 h) = O(M^2 \log n / \log m)$ in the worst case, and $O(M h)$ when no node splits. The number of disk pages written is $O(h)$.
- **Delete.** Finding the leaf may follow several paths, $O(n)$ in the worst case. CONDENSE-TREE removes at most one node per level, and the reinsertions put back fewer than $m$ entries per removed node, each by INSERT.
- **Space.** Each node other than the root has at least $m$ entries, so there are at most $n/m$ leaves, $n/m^2$ nodes one level up, and so on: fewer than $n/(m - 1) + 1$ nodes for $m \ge 2$, which is $O(n/m)$ pages and $O(n)$ entries.

| operation | time | case |
|---|---|---|
| search | $O(n)$ | worst |
| insert | $O(M^2 \log n / \log m)$ | worst |
| delete | $O(n + M^2 \log n / \log m)$ | worst |
| space | $O(n)$ | total |

## Variants

- **Split rules.** Guttman gave three: exhaustive (try every partition, exponential in $M$), [quadratic](/quadratic-split/) and linear (seeds by the largest normalized separation, then any order). See [R-tree node splitting](/r-tree-node-splitting/).
- **R*-tree.** Chooses the subtree by least overlap at the level above the leaves, splits by margin and overlap, and reinserts some entries before it splits. It is the variant used in most systems. See the [R*-tree](/r-star-tree/).
- **R+-tree.** Siblings never overlap; objects that cross a cut are stored in several leaves. See the [R+-tree](/r-plus-tree/).
- **Bulk-loaded R-trees.** For a static set, [bulk loading](/bulk-loading/) by [STR packing](/str-packing/) or along a [Hilbert curve](/hilbert-curve/) gives full nodes and little overlap in $O(n \log n)$ time.
- **Hilbert R-tree.** Orders the entries by the Hilbert value of their centers, which gives B-tree style splits with a choice of siblings. See the [Hilbert R-tree](/hilbert-r-tree/).
- **Priority R-tree.** A bulk-loaded R-tree with a worst-case optimal window query. See the [priority R-tree](/priority-r-tree/).
- **High dimensions.** The [X-tree](/x-tree/), the [SS-tree](/ss-tree/) and the [SR-tree](/sr-tree/) change the split or the shape of the regions to reduce overlap when $d$ is large.
- **Nearest neighbor.** A best-first search with a [priority queue](/priority-queue/) ordered by the distance from the query point to each rectangle finds the $k$ nearest objects, by the same argument as in the [quadtree](/quadtree/).

## When to use it

Use an R-tree to index objects with extent (polygons, lines, boxes) when the data changes and lives on disk or in a database: it stores each object once, keeps all leaves at one depth, and fills pages to at least $m/M$. Use the [R*-tree](/r-star-tree/) variant in practice, and [STR packing](/str-packing/) for data that is loaded once. For points in memory, a [k-d tree](/kd-tree/) or a [uniform grid](/uniform-grid/) is simpler and has better bounds. When a worst-case query bound matters, use the [priority R-tree](/priority-r-tree/) or a [range tree](/range-tree/).

## Pitfalls

- **A search that stops at the first match.** As in a B-tree, it is tempting to follow only one child per node. Line L1 must test every entry of the node and follow each one that meets the query.
- **Stale rectangles.** If ADJUST-TREE skips line L11 when no split happens, the parent rectangle no longer contains the new entry, and later searches miss it. Each insertion must enlarge every rectangle on its path.
- **Reinserting at the wrong height.** CONDENSE-TREE must put the entries of a removed internal node back at the same height. Inserting them as leaf entries breaks part 1 of the invariant.
- **Open and closed rectangles.** The overlap test above treats rectangles as closed, so two rectangles that share an edge meet. Use strict tests only if the objects are open sets, and use the same rule in the tree and in the refinement step.
- **Degenerate data.** Many equal or nested rectangles make every split poor, and a query at a common point then visits a large part of the tree. No split rule avoids this.

## Implementations

## History

Antonin Guttman introduced the R-tree at the ACM SIGMOD conference in 1984, for the VLSI design data of his Berkeley thesis, with the linear, quadratic and exhaustive splits and the deletion by reinsertion. Sellis, Roussopoulos and Faloutsos proposed the R+-tree in 1987, and Beckmann, Kriegel, Schneider and Seeger the R*-tree in 1990. Kamel and Faloutsos introduced the Hilbert R-tree in 1994. Arge, de Berg, Haverkort and Yi gave the priority R-tree in 2004, the first R-tree with a worst-case optimal window query.

## References
