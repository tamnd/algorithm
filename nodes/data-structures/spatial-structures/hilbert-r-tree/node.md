---
tag: P4XVG6
kind: data-structure
slug: hilbert-r-tree
name: Hilbert R-tree
aliases:
- Hilbert packed R-tree
area: data-structures/spatial-structures
level: advanced
summary: R-tree whose entries are ordered by the Hilbert value of their centers, supporting dynamic updates.
implements: [spatial-index]
model: word-ram
complexity:
  vars: {n: the number of rectangles, C: the node capacity, h: the height, v: the number of nodes visited by a window query}
  time: {insert: O(C h), delete: O(C h), window: O(C v), height: O(log n)}
  space: {total: O(n)}
history:
  year: 1994
  people: [Ibrahim Kamel, Christos Faloutsos]
  note: Kamel and Faloutsos used the Hilbert order to pack static R-trees in 1993, and in 1994 made the order the key of a dynamic R-tree with deferred splitting.
prereqs: [r-tree, hilbert-curve]
see_also: [b-plus-tree, r-star-tree, str-packing, bulk-loading, space-filling-curve, minimum-bounding-rectangle, overlap-and-dead-space, priority-r-tree]
sources:
  - paper: "Kamel and Faloutsos, Hilbert R-tree: An Improved R-tree using Fractals, VLDB 1994"
    title: Ibrahim Kamel and Christos Faloutsos, Hilbert R-tree, an improved R-tree using fractals, Proceedings of the 20th International Conference on Very Large Data Bases, 1994
    locator: the whole paper (the largest Hilbert value of each entry, the choice of a leaf by Hilbert value, the s-to-(s+1) split policy with cooperating siblings, and deletion by borrowing and merging)
  - paper: doi:10.1145/170088.170403
    title: Ibrahim Kamel and Christos Faloutsos, On packing R-trees, Proceedings of the Second International Conference on Information and Knowledge Management (CIKM), 1993
    locator: the whole paper (packing a static R-tree by sorting the rectangles on the Hilbert value of their centers)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, Object-Based and Image-Based Image Representations, the section on R-trees and their packed and Hilbert ordered variants
---

A Hilbert R-tree is an [R-tree](/r-tree/) in which the rectangles are kept sorted by one number: the position of the center of each rectangle on the [Hilbert curve](/hilbert-curve/). With this order, the tree is a [B+ tree](/b-plus-tree/) on that number, and each node also stores the bounding rectangle of everything below it, so a window query works as in any R-tree. Insertion goes to the leaf where the new key belongs in the order, not to the leaf whose rectangle grows the least. An overflowing node first gives entries to a sibling, and only when both are full do two nodes become three, so nodes are about two thirds full or more. Kamel and Faloutsos proposed it in 1994, after using the same order to pack static R-trees in 1993.

## In plain words

An R-tree groups nearby rectangles into boxes, and boxes into larger boxes. The hard part is to choose a group for a new rectangle, and to split a group that is too large.

The Hilbert curve visits every cell of a grid in one long path, and cells close on the path are close in the plane. Give each rectangle the number of its center on the path. Then keep the rectangles sorted by that number, in pages, as a B+ tree keeps sorted keys.

A new rectangle goes where its number belongs. A full page first passes some entries to its neighbor page. Only when both are full do they become three pages. Searches use the boxes, as in any R-tree.

## The abstract type

The Hilbert R-tree is a [spatial index](/spatial-index/) for rectangles. It supports `insert(r)`, `delete(r)`, and `window(q)`, which reports the stored rectangles that meet the rectangle $q$. The same tree also gives the rectangles in Hilbert order, and supports nearest neighbor queries as other R-trees do.

## Representation

Rectangles are closed, with integer corners in $[0, 2^D)^2$, written $(x_1, y_1, x_2, y_2)$. The **key** of $r$ is the pair $(H(r), r)$, where $H(r)$ is the index on the Hilbert curve of order $D + 1$ of the doubled center $(x_1 + x_2, y_1 + y_2)$. Doubling keeps the center on the grid. Two rectangles can have the same center, so the pair breaks ties; keys are then all distinct and totally ordered.

There is a node capacity $C \ge 4$ and a minimum fill $m = \lfloor C/2 \rfloor$.

- A **leaf** holds a list of keys, sorted.
- An **internal node** holds a list of child nodes, sorted by their LHV.
- Each node has an **MBR**, the [minimum bounding rectangle](/minimum-bounding-rectangle/) of all rectangles below it, and an **LHV**, the largest key below it.

**Invariant (H).** (1) All leaves are at the same depth. (2) The keys in the leaves, read from left to right, are strictly increasing, and each rectangle is stored once. (3) Every node other than the root has between $m$ and $C$ entries; the root has at most $C$, and at least 2 if it is internal. (4) The MBR and LHV of each node are correct.

Parts 1 to 3 make the tree a B+ tree on the keys, with separator keys replaced by the LHV of each child. Part 4 is what makes it an R-tree. Since the children of an internal node hold consecutive runs of keys, each child has a sibling next to it, unless it is the only child of the root, which part 3 forbids.

## Operations

```pseudo id=main
INSERT(T, r)
L1  k ← the key of r
L2  u ← the root; while u is not a leaf:
L3      go to the first child of u whose LHV is at least k, or to the last child
L4  put k into the sorted list of the leaf u
L5  while u has more than C entries:
L6      if u is the root then split it into two halves under a new root, and stop
L7      take u and one sibling next to it, the right one if there is one
L8      if the two hold at most 2C entries then deal them evenly between the two, in order, and stop
L9      else make a new node, and deal the entries evenly among the three, in order
L10     u ← the parent of u, which has one more child
L11 update the MBR and LHV of the leaf and of each node on the path, from the bottom up
```

```pseudo id=delete
DELETE(T, r)
L12 find the leaf for the key k of r as in lines L2 and L3; stop if k is not there
L13 remove k from the leaf u
L14 while u is not the root and u has fewer than m entries:
L15     take u and one sibling next to it; if they hold at least 2m entries then deal them evenly between the two, and stop
L16     else move all entries into one of the two, remove the other from the parent, and go on with the parent
L17 update the MBR and LHV on the path; while the root is internal with one child, make that child the root
```

```pseudo id=window
WINDOW(T, q)
L18 push the root on a stack; while it is not empty: pop u
L19     if u is empty or the MBR of u does not meet q then skip u
L20     if u is a leaf then report its rectangles that meet q
L21     else push the children of u
```

Line L3 is the search of a B+ tree: the keys of the $i$th child are greater than the LHV of child $i - 1$ and at most its own LHV. Line L9 is the 2-to-3 split: two full nodes and one extra entry make $2C + 1$ entries, dealt as $\lceil (2C+1)/3 \rceil$ or less per node, which is at least $m$ and at most $C$. Kamel and Faloutsos allow $s$ cooperating siblings and an $s$-to-$(s+1)$ split; the code uses $s = 2$.

## Example

Take $D = 3$, so corners in $[0, 8)^2$ and keys on the Hilbert curve of the $16 \times 16$ grid, and $C = 4$, $m = 2$. The rectangles and the first part of their keys are:

| name | rectangle | doubled center | $H$ |
|---|---|---|---|
| $A$ | (0,0,1,1) | (1,1) | 2 |
| $F$ | (2,0,2,1) | (4,1) | 17 |
| $E$ | (3,3,4,4) | (7,7) | 42 |
| $H$ | (0,3,1,3) | (1,6) | 61 |
| $C$ | (0,6,1,7) | (1,13) | 82 |
| $G$ | (5,5,5,6) | (10,11) | 139 |
| $D$ | (6,6,7,7) | (13,13) | 162 |
| $I$ | (7,3,7,4) | (14,7) | 193 |
| $B$ | (6,0,7,1) | (13,1) | 242 |

Insert $A, B, C, D, E, F, G, H, I$ in this order.

| insert | what happens | leaves after |
|---|---|---|
| $A, B, C, D$ | the root is a leaf with room | $[A, C, D, B]$ |
| $E$ | the root leaf has 5 entries and splits under a new root | $[A, E, C]$, $[D, B]$ |
| $F$ | the first leaf has LHV 82, which is at least 17 | $[A, F, E, C]$, $[D, B]$ |
| $G$ | 139 is above 82, so the last leaf | $[A, F, E, C]$, $[G, D, B]$ |
| $H$ | the first leaf has 5 entries; with its right sibling there are 8, so they are dealt 4 and 4 | $[A, F, E, H]$, $[C, G, D, B]$ |
| $I$ | the second leaf has 5 entries; with its left sibling there are 9, so a 2-to-3 split | $[A, F, E]$, $[H, C, G]$, $[D, I, B]$ |

The three leaves have the MBRs (0,0,4,4), (0,3,5,7) and (6,0,7,7), and the LHVs of $E$, $G$ and $B$.

- **Window** $q = (0,0,2,2)$: only the first leaf's MBR meets $q$; in it, $A$ and $F$ meet $q$, and $E$ does not. The answer is $A$, $F$.
- **Delete** $E$, then $F$: the first leaf is left with $[A]$, below $m = 2$. With its right sibling there are 4 entries, which is $2m$, so they are dealt 2 and 2: $[A, H]$, $[C, G]$, $[D, I, B]$.
- **Delete** $H$: the first leaf is left with $[A]$ again, and with its sibling there are only 3 entries, so the two merge into $[A, C, G]$. The root still has two children: $[A, C, G]$, $[D, I, B]$.

## Correctness

Inside the leaves the tree is a B+ tree on the keys, and each step keeps that true. Line L3 goes to the only leaf where the key can be, because the children of a node hold consecutive runs of keys and the LHV is the last key of each run. Dealing entries in order among adjacent nodes keeps the leaf order. The counts in lines L8, L9, L15 and L16 keep every node between $m$ and $C$ entries. Line L11 and line L17 recompute the MBR and LHV of every node whose contents changed, so the window query, which skips only nodes whose MBR misses $q$, reports every rectangle that meets $q$. The full proof is in the proofs folder.

## Complexity

- **Height.** Every node other than the root has at least $m \ge 2$ entries, so $h \le \log_m n + 1 = O(\log n)$ for a fixed capacity. With the 2-to-3 split, nodes made by a split hold at least about $2C/3$ entries.
- **Insert and delete.** One path down, with $O(C)$ work per node to choose the child, and $O(C)$ work per level to share, split or merge. That is $O(Ch)$, and $O(h)$ node accesses on disk, plus one sibling per level.
- **Window.** The query visits $v$ nodes and spends $O(C)$ on each. As in every R-tree, $v$ has no good worst-case bound: a window can meet the MBR of every node while meeting no rectangle. The Hilbert order makes the MBRs small and square in practice, which keeps $v$ small.
- **Space.** $n$ keys in the leaves and $O(n/m)$ nodes.

| operation | time | case |
|---|---|---|
| insert | $O(Ch)$ | worst |
| delete | $O(Ch)$ | worst |
| window | $O(Cv)$ | worst, $v$ nodes visited |
| height | $O(\log n)$ | worst, for fixed $C$ |
| space | $O(n)$ | total |

## Variants

- **Hilbert packed R-tree.** For a static set, sort the rectangles by key and fill the leaves in order, then build each level above the same way. This is the packing of Kamel and Faloutsos from 1993, a form of [bulk loading](/bulk-loading/); [STR packing](/str-packing/) is another.
- **More cooperating siblings.** With $s$ siblings sharing before a split, an $s$-to-$(s+1)$ split leaves nodes about $s/(s+1)$ full, at the cost of more nodes touched per overflow.
- **Other curves.** The same idea works with the Z-order of a [space-filling curve](/space-filling-curve/), but the Hilbert curve has no long jumps, so its runs of keys make smaller MBRs.
- **Higher dimensions.** The key is the Hilbert index of the center in $d$ dimensions; the rest of the tree does not change.
- **Large rectangles.** The center alone ignores the size of a rectangle. Some variants map each rectangle to a point in four dimensions, or keep large rectangles apart.

## When to use it

Use a Hilbert R-tree for rectangles or points that change, when good node fill and a simple, predictable insertion rule matter, as on disk. Its updates are those of a B+ tree, with no overlap or area computations, and its order also gives a good linear layout of the data. When the data has rectangles of very different sizes, or queries are very sensitive to [overlap and dead space](/overlap-and-dead-space/), the [R*-tree](/r-star-tree/) can give better MBRs; when a worst-case query bound is needed, use a [priority R-tree](/priority-r-tree/).

## Pitfalls

- **Equal keys.** Different rectangles can have the same center. Use the rectangle itself as a tie breaker, or the leaf order and deletion become ambiguous.
- **The center must be on the grid.** The center of a rectangle with integer corners can be at a half. Double the coordinates and use a curve of one more order, as the key here does.
- **Order of updates.** After a split or a share, the MBR and LHV of the leaf change first, then those of its ancestors. Recomputing a parent from stale children gives wrong values.
- **Small capacities.** With $C < 4$, $m = 1$ and an internal node can have a single child with no sibling to share with. Use $C \ge 4$.
- **No worst-case query bound.** The order controls the shape of the MBRs only in practice.

## Implementations

## History

Kamel and Faloutsos first used the Hilbert curve to pack static R-trees, in a CIKM paper in 1993, and found that sorting on the Hilbert value of the centers gave better trees than earlier packings. In 1994, at VLDB, they made the Hilbert value the key of a dynamic tree: the LHV of each entry turns the R-tree into a B+ tree, and the cooperating siblings give deferred splitting. Samet's book describes it with the other ordered R-trees.

## References
