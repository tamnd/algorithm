---
tag: 7DA53Q
kind: data-structure
slug: loose-octree
name: Loose octree
aliases:
- loose quadtree
area: data-structures/spatial-structures
level: advanced
summary: Octree whose cells overlap by a margin so each object fits in one node, which eases dynamic updates.
implements: [spatial-index]
model: word-ram
complexity:
  vars: {n: the number of boxes, D: the number of halvings from the root cube to a unit cell, m: the largest number of boxes at one node, v: the number of nodes visited}
  time: {place: O(1), insert: O(D + m), delete: O(D + m), move: O(D + m), query: O(v + v m)}
  space: {total: O(n D)}
history:
  year: 2000
  people: [Thatcher Ulrich]
  note: Ulrich described the loose octree in the first volume of Game Programming Gems, as a fix for the objects that a plain octree keeps near the root because they cross a cell boundary.
prereqs: [octree, axis-aligned-bounding-box]
see_also: [mx-cif-quadtree, collision-detection, bounding-volume-hierarchy, uniform-grid, spatial-hashing, frustum-culling, pr-quadtree, linear-quadtree]
sources:
  - book: isbn:9781584500490
    title: Mark DeLoura (editor), Game Programming Gems, Charles River Media, 2000
    locator: the article Loose octrees by Thatcher Ulrich (loose cells of twice the side, and the choice of the depth from the size of the object)
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 7, Spatial Partitioning (the section on octrees and the part on loose octrees)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 3, Intervals and Small Rectangles (the MX-CIF quadtree and the problem of small objects that cross the center lines of large cells)
---

A loose octree stores boxes, such as the bounding boxes of moving objects, in an [octree](/octree/) whose cells overlap. Each cell is grown on every side by half its side, so the *loose cell* has twice the side of the cell. A box then fits in the loose cell of the cell that holds its center, at the depth whose cell side is about its own size. So the node of a box comes from its size and its center alone, with no search, and a small box is never stuck high in the tree just because it crosses a cell boundary, which is the weak point of the [MX-CIF quadtree](/mx-cif-quadtree/) and of a plain octree of objects. The price is that a query must look at more cells, since the loose cells overlap. Ulrich described it in 2000 for games, where objects move in each frame.

## In plain words

Picture an octree of boxes, where each object goes to the smallest box that holds it whole. A tiny object that sits on the middle wall of the world must go to the top box. Many tiny objects can end up there, and the tree stops helping.

A loose octree makes each box bigger than its place in the grid, so that boxes next to each other overlap. Now an object always fits in a box about its own size: the one whose grid place holds the middle of the object.

When an object moves, you work out its new box from its size and middle, and move it there. A search must look at more boxes, because they overlap.

## The abstract type

The loose octree is a [spatial index](/spatial-index/) for [axis-aligned boxes](/axis-aligned-bounding-box/) in a cube. It supports `insert(b)`, `delete(b)`, `move(b, b')` and `query(q)`, which reports the stored boxes that meet the box $q$. It is used most for the broad phase of [collision detection](/collision-detection/) and for [frustum culling](/frustum-culling/), and its two-dimensional form, the loose quadtree, for maps and 2D games.

## Representation

The root cell is $[0, 2^D)^3$. Boxes are closed, $[lo, hi]$ with integer corners in the root cell. A node at depth $d$ has side $s = 2^{D - d}$ and an index $(i, j, k)$, and its cell is $[is, (i+1)s) \times [js, (j+1)s) \times [ks, (k+1)s)$. Its loose cell, with looseness 2, is
$$[is - s/2,\ (i+1)s + s/2] \times [js - s/2,\ (j+1)s + s/2] \times [ks - s/2,\ (k+1)s + s/2],$$
which has side $2s$. A node has a list of boxes and eight child slots, for the octants $o = b_x + 2b_y + 4b_z$; the child $o$ has index $(2i + b_x, 2j + b_y, 2k + b_z)$.

**Placement.** Let $e$ be the largest extent of the box $b$, the largest of $hi_a - lo_a$ over the three axes $a$, and let $s$ be the least power of two with $s \ge \max(e, 1)$. Then $b$ goes at the depth $D - \lg s$, in the cell whose index is $\lfloor c / s \rfloor$ on each axis, where $c = (lo + hi)/2$ is the center of $b$. The center lies in $[is, (i+1)s)$, and the box reaches at most $e/2 \le s/2$ from it, so $b$ lies in the loose cell.

**Invariant (P).** (1) Each box is stored once, at the node given by its placement. (2) The children of a node are its octants. (3) Each node other than the root stores a box or has a child.

By (1) each box is in the loose cell of its node. The loose cell of a child lies in the loose cell of its parent: on one axis, the child $2i$ or $2i + 1$ of side $s/2$ has loose cell inside $[2i \cdot s/2 - s/4,\ (2i+2) s/2 + s/4]$, which lies in $[is - s/2,\ (i+1)s + s/2]$. So every box at or below a node lies in the node's loose cell, and a query can skip a node whose loose cell misses it.

## Operations

```pseudo id=main
INSERT(T, b)
L1  e ← the largest extent of b
L2  s ← the least power of two with s ≥ max(e, 1); t ← D − lg s
L3  (i, j, k) ← ⌊center of b / s⌋ on each axis
L4  walk from the root down t levels, taking at depth d the octant given by bit t − d − 1 of i, j and k; make each missing node
L5  add b to the list of the node reached

QUERY(T, q)                                ▷ report the boxes that meet q
L6  push the root on a stack S; while S is not empty: pop u
L7      if the loose cell of u does not meet q then skip u
L8      for each b in the list of u:
L9          if b meets q then report b
L10     push each child of u on S
```

```pseudo id=delete
DELETE(T, b)
L11 find the node of b by lines L1 to L4, without making nodes; if a node is missing then return false
L12 if b is not in its list then return false; remove b
L13 while the node is not the root and has no boxes and no children:
L14     remove it from its parent and go to the parent
    return true
```

A move is a delete and an insert. In a game, most objects move a little in each frame and stay in the same node, so a program can first check whether the new placement is the same node and do nothing then.

## Example

Take $D = 3$, so the root cube is $[0, 8)^3$, and four boxes.

| box | extent $e$ | side $s$ | depth | center | index |
|---|---|---|---|---|---|
| A = $[1,2] \times [1,2] \times [1,2]$ | 1 | 1 | 3 | $(1.5, 1.5, 1.5)$ | $(1, 1, 1)$ |
| B = $[3,5] \times [3,5] \times [0,0]$ | 2 | 2 | 2 | $(4, 4, 0)$ | $(2, 2, 0)$ |
| C = $[0,7] \times [0,3] \times [0,3]$ | 7 | 8 | 0 | $(3.5, 1.5, 1.5)$ | $(0, 0, 0)$, the root |
| D = $[6,6] \times [1,1] \times [6,6]$, a point | 0 | 1 | 3 | $(6, 1, 6)$ | $(6, 1, 6)$ |

The box B crosses the planes $x = 4$ and $y = 4$ through the center of the root, so a plain octree that stores each box in the smallest cell that holds it would keep B at the root. In the loose octree, B goes to the cell $[4, 6) \times [4, 6) \times [0, 2)$ at depth 2, whose loose cell $[3, 7] \times [3, 7] \times [-1, 3]$ holds it. The path to it takes octant 3 of the root, from bit 1 of the index $(2, 2, 0)$, which is $(1, 1, 0)$, and then octant 0, from bit 0, which is $(0, 0, 0)$.

- **Nodes.** The root, three nodes on the path to A, two on the path to B, and three on the path to D: 9 nodes.
- **Query** $q = [3, 4] \times [3, 4] \times [0, 1]$. The root's list has C, which meets $q$, since its $y$ range $[0, 3]$ touches $3$. The loose cell of the node of B meets $q$, and B meets $q$. The paths to A and D are skipped once their loose cells miss $q$. The answer is B and C.
- **Delete** A. The three nodes of its path are left empty and are removed: 6 nodes.
- **Move** D to the point $(2, 2, 2)$. D is removed with its three nodes, and the point goes to depth 3, index $(2, 2, 2)$; its path goes through octant 0 of the root, which no longer exists, so it adds three new nodes, and the tree again has 6 nodes.

## Correctness

The placement puts a box in the loose cell of its node, and the loose cells are nested from child to parent, so a query that skips a node whose loose cell misses $q$ skips only boxes that miss $q$. INSERT and DELETE compute the same node from the box, so DELETE finds the box where INSERT put it, and the pruning keeps only nodes with boxes below them. The full proof is in the proofs folder.

## Complexity

The model is the word RAM with integer coordinates.

- **Placement.** $O(1)$ word operations, with the bit length of $e$ for $\lg s$, and no search of the tree. This is the main gain over a plain octree, where finding the node of a box needs a walk that compares it with the center planes.
- **Insert, delete and move.** $O(D)$ for the path and $O(m)$ for the list of the node. With nodes kept in a hash table keyed by depth and index, a program can skip the walk.
- **Box size against node size.** A box at a node of side $s \ge 2$ has $s/2 < e \le s$, so it fills at least a quarter of the side $2s$ of the loose cell on its largest axis. Small boxes are never stored at large nodes, which keeps the lists that a query tests short.
- **Query.** On one axis, a point lies in the loose cells of at most two cells of a level, except on the boundaries, where it can be in three, so a small query meets at most about $2^3 = 8$ loose cells per level, against 1 cell per level for a plain octree. The loose octree pays this to keep each box low in the tree.
- **Space.** Each box is stored once, and each node is on the path of a stored box: at most $1 + nD$ nodes.

| operation | time | case |
|---|---|---|
| place | $O(1)$ | worst |
| insert | $O(D + m)$ | worst |
| delete | $O(D + m)$ | worst |
| move | $O(D + m)$ | worst |
| query | $O(v + v m)$ | worst, $v$ nodes visited |
| space | $O(n D)$ | total |

## Variants

- **Looseness $k$.** With loose cells of side $k s$, a box with extent $e \le (k - 1)s$ fits in the loose cell of the cell of its center. Ulrich chose $k = 2$; a larger $k$ lets a box go one level deeper but makes the loose cells overlap more. Values between 1 and 2 need a search for the node.
- **Loose quadtree.** The same structure in two dimensions, with four children.
- **Fit by search.** Rather than the formula, insert by walking down while some child's loose cell holds the box. This can put a box deeper than the formula, where its center is near the middle of a cell.
- **Hashed cells.** Keep the nodes in a hash table keyed by depth and index, with no pointers, which is a [linear quadtree](/linear-quadtree/) of loose cells; each level is then a loose [spatial hash](/spatial-hashing/).
- **Sphere bounds.** Use the radius of a bounding sphere as $e/2$; a sphere of radius $r \le s/2$ centered in a cell lies in its loose cell.

## When to use it

Use a loose octree for many moving objects of mixed sizes in a bounded world, such as the objects of a game or a simulation, when updates are as frequent as queries. Each update is a constant number of steps to find the node. Use a [uniform grid](/uniform-grid/) or [spatial hashing](/spatial-hashing/) when the objects have about the same size, a [bounding volume hierarchy](/bounding-volume-hierarchy/) when the scene is mostly static, and an [MX-CIF quadtree](/mx-cif-quadtree/) or plain octree when queries are much more frequent than updates and each node must be tested only once per level.

## Pitfalls

- **Testing the cell, not the loose cell.** A query must test the loose cell of a node. Testing the cell itself misses boxes that stick out of it, which is a silent wrong answer.
- **Objects larger than the world.** A box with extent more than the root side cannot be placed. Clamp it to the root, or keep large objects in a separate list.
- **Center on the far boundary.** With half-open cells, a center at exactly $2^D$ is outside the root. Keep the coordinates strictly inside the root cube, as the code does.
- **Rounding with real coordinates.** With floating point positions, the index $\lfloor c / s \rfloor$ can round across a cell boundary. The box is then still in the loose cell of one of the two cells, but insert and delete must use the same computation, or the box is lost.

## Implementations

## History

Octrees of objects, with each object at the smallest cell that holds it, were in use in graphics and in the MX-CIF quadtree of Kedem since the early 1980s, and their trouble with small objects on cell boundaries was known. Ulrich described the loose octree in 2000, in the first Game Programming Gems book, with looseness 2 and the placement by size and center. Ericson's book on real-time collision detection of 2005 treats it with other spatial partitions for games.

## References
