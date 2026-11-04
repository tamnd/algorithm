---
tag: SFMMBA
kind: data-structure
slug: r-plus-tree
name: R+-tree
aliases:
- R+ tree
area: data-structures/spatial-structures
level: advanced
summary: R-tree variant that clips objects so sibling regions never overlap, at the cost of duplicated entries.
implements: [spatial-index]
model: external-memory-model
complexity:
  vars: {n: the number of stored rectangles, M: the most entries in a node (soft), c: the number of stored copies (at least n), h: the height of the tree, k: the number of reported rectangles}
  time: {search: O(c), insert: O(c M^2), delete: O(c)}
  space: {total: O(c)}
history:
  year: 1987
  people: [Timos Sellis, Nick Roussopoulos, Christos Faloutsos]
  note: Sellis, Roussopoulos and Faloutsos introduced the R+-tree at VLDB 1987, to remove the overlap of sibling boxes that makes R-tree point queries follow several paths.
prereqs: [r-tree, kd-b-tree]
see_also: [r-tree, r-star-tree, kd-b-tree, overlap-and-dead-space, space-partitioning, minimum-bounding-rectangle, bsp-tree, quadtree]
sources:
  - paper: "Timos Sellis, Nick Roussopoulos and Christos Faloutsos, The R+-tree, a dynamic index for multi-dimensional objects, Proceedings of the 13th International Conference on Very Large Data Bases (VLDB), 1987, pp. 507 to 518"
    locator: the definition of the R+-tree, the search, insertion and deletion algorithms, the partition and split procedures, and the analysis against the R-tree
  - paper: doi:10.1145/280277.280279
    title: Volker Gaede and Oliver Günther, Multidimensional access methods, ACM Computing Surveys 30(2), 1998, pp. 170 to 231
    locator: Section 5, the part on the R+-tree, its clipping and the deadlock of the split
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 2, Object-Based and Image-Based Image Representations, the section on disjoint object-based methods and the R+-tree
---

The R+-tree is an [R-tree](/r-tree/) in which the regions of sibling nodes never overlap. To reach this, an object that crosses the border between two regions is *clipped*: it is stored in every leaf whose region it meets. A point query then follows exactly one path from the root to a leaf, as in a [k-d-B tree](/kd-b-tree/), and a window query never visits a region twice. The price is that one object can have many copies, so the tree is larger, a query must remove duplicates, and some nodes cannot be split. Sellis, Roussopoulos and Faloutsos introduced it in 1987.

## In plain words

An R-tree puts boxes into bags, and the frames of two bags can overlap. A search for a point inside the overlap must open both bags.

The R+-tree cuts the plane into rooms that do not overlap, and rooms into smaller rooms. A box that lies across a wall is put into every room it touches, one copy in each. A search for a point then has exactly one room to open at each level. When a room has too many boxes, the tree puts a straight wall through it, and the boxes on the wall go to both sides. A search that reports boxes must take care to report each box once, since it can see the same box in several rooms.

## The abstract type

The R+-tree implements a [spatial index](/spatial-index/) for rectangles: `insert(id, r)`, `delete(id, r)` and `search(q)`, which reports each stored rectangle that meets the closed query rectangle $q$ exactly once. A stabbing query is a search with a point.

## Representation

Each node has a *region*, a half-open rectangle $[x_0, x_1) \times [y_0, y_1)$; the region of the root is the whole plane. An internal node holds its children; a leaf holds pairs (id, rectangle), where the rectangles are closed. The paper stores the [MBR](/minimum-bounding-rectangle/) of the clipped contents with each entry, to skip dead space; the regions are enough for correctness, and the implementation keeps only the regions.

**Invariant (R+).** (1) The regions of the children of a node are disjoint and their union is the region of the node. (2) A leaf holds exactly the stored rectangles that meet its region. (3) All leaves are at the same depth. (4) An internal node has at most $M$ children. A leaf with more than $M$ entries has no *good cut*: no axis-parallel line at a side of one of its rectangles that leaves both sides with fewer entries than the leaf.

Part (1) makes the leaves a partition of the plane, so each point lies in exactly one leaf. Part (2) is the clipping. Part (4) states that $M$ is a soft limit for leaves: if more than $M$ rectangles share one point, every cut through the leaf keeps all of them on one side, and no split helps. The paper notes this case, which is the price of no overlap. Internal nodes never have this problem: their children are made by straight cuts, so the first of those cuts is a line that crosses no child and splits the children into two nonempty groups.

## Operations

```pseudo id=main
SEARCH(u, q)
L1  if u is internal then for each child v of u:
L2      if q meets the region of v then SEARCH(v, q)
L3  else for each (id, r) in u with r ∩ q ≠ ∅:
L4      p ← (max(q.x1, r.x1), max(q.y1, r.y1)); if p is in the region of u then report id      ▷ report once
INSERT(id, r)
L5  go down into every child whose region r meets
L6  add (id, r) to every leaf reached
L7  on the way back up, SPLIT-ALL each node that was visited, and put the pieces in its parent
L8  while the root has been cut into several pieces: make a new root with the pieces, and SPLIT-ALL it with clean cuts only
```

```pseudo id=split
SPLIT-ALL(u)
L9  if u has at most M entries, or CHOOSE-CUT(u) is none, then return [u]
L10 CHOOSE-CUT: on each axis, for each side c of an entry strictly inside the region of u,
        count the entries that reach the left of c (nl) and the right of c (nr)
L11 keep the cuts with 0 < nl, nr < size(u) (a clean cut also has nl + nr = size(u)); return the one with the smallest max(nl, nr), ties by nl + nr
L12 CUT(u, axis, c): a leaf gives the two halves of its region, each with the rectangles that meet it
L13     an internal node gives each child to its side, and CUTs each child that crosses c, down to the leaves
        return SPLIT-ALL(left) + SPLIT-ALL(right)
```

```pseudo id=delete
DELETE(id, r)
L14 go down into every child whose region r meets, and remove (id, r) from every leaf reached
```

**Search.** A rectangle $r$ that meets $q$ is stored in each leaf that meets $r$, and several of those may meet $q$. Line L4 reports $r$ only in the leaf that holds the point $p$, the lower left corner of $r \cap q$. The point $p$ lies in $r$ and in $q$, and in exactly one leaf region, so $r$ is reported once, with no set of seen ids. The paper instead removes duplicates by a sort, which works for any output.

**Insert.** An R-tree insert chooses one path. The R+-tree has no choice: the regions partition the plane, so the leaves that $r$ meets are fixed, and $r$ goes into all of them. There is no enlargement of regions either, since the regions already cover the plane.

**Split.** A split puts a straight line through the region. Children on one side go to that side. A child that crosses the line is cut too, and its children, down to the leaves; this is the *downward split* that also happens in the [k-d-B tree](/kd-b-tree/). The pieces of a cut node have no more entries than the node, so the downward cuts never cause an overflow below. The cut can make the parent overflow, which the walk back up then handles. The paper chooses the cut by the coverage and the number of cut entries; the implementation chooses the cut that makes the larger side smallest, then the fewest copies. When the root itself is cut into several pieces, the new root over them is split only with *clean* cuts, which cross no child. Such a cut always exists, and with it the number of pieces goes down each time, so the loop of line L8 stops.

**Delete.** Remove every copy. The paper does not merge underfull nodes, since a merge of two regions that are not adjacent in the right way is not a rectangle; the tree is rebuilt from time to time instead. The implementation keeps empty leaves, whose regions still belong to the partition.

## Example

Take $M = 4$ and insert, as $[x_1, x_2] \times [y_1, y_2]$: a $= [0, 2] \times [0, 2]$, b $= [1, 3] \times [5, 7]$, c $= [6, 8] \times [0, 1]$, d $= [7, 9] \times [6, 9]$, e $= [2, 3] \times [1, 3]$, f $= [6, 7] \times [7, 8]$, g $= [1, 2] \times [3, 4]$, h $= [3, 4] \times [6, 8]$ and i $= [2, 7] \times [2, 4]$.

**Insert a to e.** The root leaf has 5 entries, more than $M$. The candidate cuts are the sides of the rectangles. For each cut, the table gives the entries that reach each side.

| cut | left side | right side | max | copies |
|---|---|---|---|---|
| $x = 2$ | a, b | a, b, c, d, e | 5 | 7 |
| $y = 2$ | a, c, e | a, b, d, e | 4 | 7 |
| $x = 3$ | a, b, e | b, c, d, e | 4 | 7 |
| $x = 6$ | a, b, e | c, d | 3 | 5 |
| $x = 7$ | a, b, c, e | c, d | 4 | 6 |
| $y = 3$ | a, c, e | b, d, e | 3 | 6 |
| $y = 5$ | a, c, e | b, d | 3 | 5 |

A rectangle that touches the line goes to the right side too, since the right region $[c, \infty)$ is closed at $c$: so a, with $x_2 = 2$, is on both sides of $x = 2$, and that cut is not good. The cuts $x = 6$ and $y = 5$ tie on both counts, and the implementation then takes the $x$ axis. The sides not in the table give cuts that leave all 5 entries on one side. The root becomes internal, with the leaves $(-\infty, 6) \times \mathbb{R}$ holding a, b, e and $[6, \infty) \times \mathbb{R}$ holding c, d.

**Insert f, g and h.** f goes right and g left. h goes left, which now has a, b, e, g, h, five entries. The best cut there is $y = 5$: a, e, g lie below and b, h above, and no rectangle crosses it; the next best, $y = 4$, puts g on both sides. The root has three leaves: $(-\infty, 6) \times (-\infty, 5)$ with a, e, g; $(-\infty, 6) \times [5, \infty)$ with b, h; and $[6, \infty) \times \mathbb{R}$ with c, d, f. In the R*-tree the same 8 rectangles also gave three leaves with these groups, but here the leaf regions tile the plane.

**Insert i.** The rectangle $[2, 7] \times [2, 4]$ meets the first leaf and the third. It goes into both: the first has a, e, g, i and the third c, d, f, i, 4 entries each, so no split. The tree stores 10 copies of 9 rectangles.

**Search.** SEARCH($[2.5, 7] \times [2.5, 7]$) visits all three leaves. In the first, e and i meet $q$; the corner $p$ for i is $(2.5, 2.5)$, which lies in the first leaf, so i is reported there. In the third, d, f and i meet $q$, but $p = (2.5, 2.5)$ for i is not in that leaf, so i is not reported again. The answer is b, d, e, f, h and i. SEARCH($[6.5, 6.6] \times [2.5, 2.6]$) goes only into the third leaf, where i is the only rectangle that meets it; $p = (6.5, 2.5)$ is in the third leaf, so i is reported. A point query always follows one path: the point $(5, 5)$ lies only in the second leaf.

**Delete.** DELETE(i) goes into the first and third leaves and removes both copies.

## Correctness

Each operation keeps the invariant. INSERT adds $r$ to exactly the leaves it meets, since it goes into every child whose region meets $r$, and the regions of the children of a node cover the node. A CUT of a leaf gives two halves that partition its region, and each half keeps exactly the rectangles that meet it, so parts (1) and (2) hold. A CUT of an internal node partitions the children by the line, cutting the ones that cross it, so the pieces again partition the region, and a cut child gives two pieces at the same depth, so part (3) holds. SPLIT-ALL stops, since every good cut gives two nodes with fewer entries. The children of an internal node always form a *guillotine* partition, one made by repeated straight cuts, so an internal node with more than $M$ children has a clean good cut, and SPLIT-ALL only leaves a leaf over full, when no good cut exists: part (4). A new root over the pieces adds one level above every leaf. Search reports each rectangle that meets $q$ exactly once, by the corner argument above. The full proof is in the proofs folder.

## Complexity

Let $c \ge n$ be the number of stored copies, the sum of the leaf sizes. The model is the [external memory model](/external-memory-model/) with one node per page, or the RAM with a cost per entry examined.

- **Search.** In the worst case, every node is visited: $O(c)$. A point query visits one node per level, so it costs $O(h + M')$, where $M'$ is the size of the leaf reached, which is the main gain over the R-tree, whose point queries can follow many paths. A window query visits only nodes whose region meets $q$, and never reads one region twice.
- **Insert.** The walk down visits the nodes whose regions meet $r$. Each node visited can be split; CHOOSE-CUT tries $O(M)$ lines and counts $O(M)$ entries for each, $O(M^2)$, and a downward cut can touch many nodes. A loose bound is $O(c M^2)$.
- **Delete.** The walk visits the nodes whose regions meet $r$, $O(c)$ in the worst case.
- **Space.** $O(c)$ entries. The number of copies is the weak point. Take $n/2$ long horizontal and $n/2$ long vertical segments that form a grid. They cross at $n^2/4$ points. A leaf with at most $M$ entries holds at most $M^2/4$ of the crossings, so there are at least $n^2/M^2$ nonempty leaves, and $c = \Omega(n^2/M^2)$. Small objects cause few copies; long thin objects many.
- **Height.** No bound like $O(\log n)$ holds in general, since downward splits and copies can make the tree large. On small, spread objects the height is close to that of an R-tree.

| operation | time | case |
|---|---|---|
| search | $O(c)$ | worst |
| point query | $O(h + M')$ | one path |
| insert | $O(c M^2)$ | worst |
| delete | $O(c)$ | worst |
| space | $O(c)$ | total |

## Variants

- **Packed R+-tree.** The paper also gives a packing algorithm for static data, which fills nodes along one axis, much as [STR packing](/str-packing/) does for the R-tree.
- **Cell tree and k-d-B tree.** The [k-d-B tree](/kd-b-tree/) is the same partition scheme for points, where no clipping is needed. The cell tree of Günther partitions space into convex polygons, with clipping, as a [BSP tree](/bsp-tree/) does.
- **Quadtree-like partitions.** Fixed partitions, such as the MX-CIF or PMR [quadtree](/quadtree/), also store an object in each cell it meets; the R+-tree chooses its cuts from the data instead.
- **With MBRs.** The paper stores, for each child, the bounding box of what is inside it, so a query can skip dead space in a region.

## When to use it

Use the R+-tree when point queries dominate, for example a lookup of the map feature under a cursor, and the objects are small relative to the space, so few are clipped. Use the [R-tree](/r-tree/) or [R*-tree](/r-star-tree/) when objects are large or long, when the index must be small, or when deletes are frequent, since the R+-tree does not merge nodes. The [overlap and dead space](/overlap-and-dead-space/) page compares the two goals.

## Pitfalls

- **Duplicates in the output.** A window query sees a clipped rectangle in several leaves. Remove duplicates with the corner test, a sort, or a set.
- **Closed objects and half-open regions.** A rectangle that touches a cut line must go to the side whose half-open region contains the touch point. With closed regions, a point on a line lies in two leaves and the one-path property is lost.
- **The deadlock.** More than $M$ objects that share a point cannot be split apart. The code must allow overfull nodes, or a split loops forever.
- **Downward splits.** A cut in an internal node cuts children far below it, which can create nearly empty nodes. A better cut rule prefers lines that cross few children.
- **No minimum fill.** There is no guarantee like the $m$ of the R-tree, so space use can drop after deletes. Rebuild the tree when it does.

## Implementations

## History

Sellis, Roussopoulos and Faloutsos proposed the R+-tree at VLDB 1987. It took the clipping of objects from earlier spatial structures and joined it to the multiway node of Guttman's R-tree and the partition of the k-d-B tree of Robinson. Their analysis showed fewer page reads than the R-tree for point queries and for small objects, and more storage. Later surveys, such as that of Gaede and Günther, noted the deadlock of the split and the duplicate entries as the main costs. The R*-tree of 1990, which reduces the overlap without removing it, became more widely used.

## References
