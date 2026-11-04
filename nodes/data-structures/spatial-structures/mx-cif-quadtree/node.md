---
tag: RHN2XW
kind: data-structure
slug: mx-cif-quadtree
name: MX-CIF quadtree
area: data-structures/spatial-structures
level: advanced
summary: Quadtree that stores each rectangle at the smallest node that fully contains it, for rectangle data.
implements: [spatial-index]
model: word-ram
complexity:
  vars: {n: the number of rectangles, D: the number of halvings from the root square to a unit cell, m: the largest number of rectangles at one node, v: the number of nodes visited, k: the number of reported rectangles}
  time: {insert: O(D + m), delete: O(D + m), stab: O(D m), window: O(v + v m)}
  space: {total: O(n D)}
history:
  year: 1982
  people: [Gershon Kedem, David J. Abel, John L. Smith]
  note: Kedem introduced the quad-CIF tree in 1982 for the rectangles of VLSI layouts, and Abel and Smith used the same scheme for areal data in geographic databases; Samet gave it the name MX-CIF quadtree.
prereqs: [quadtree, minimum-bounding-rectangle]
see_also: [loose-octree, pr-quadtree, linear-quadtree, r-tree, interval-tree, segment-tree, spatial-join, collision-detection]
sources:
  - paper: "Gershon Kedem, The quad-CIF tree, a data structure for hierarchical on-line algorithms, Proceedings of the 19th Design Automation Conference, 1982"
    title: Gershon Kedem, The quad-CIF tree, a data structure for hierarchical on-line algorithms, Proceedings of the 19th Design Automation Conference, 1982
    locator: the whole paper (rectangles stored at the smallest enclosing quadtree cell, with one-dimensional trees for the rectangles that cross the center lines)
  - paper: "David J. Abel and John L. Smith, A data structure and query algorithm for a database of areal entities, Australian Computer Journal 16(4), 1984"
    title: David J. Abel and John L. Smith, A data structure and query algorithm for a database of areal entities, Australian Computer Journal 16(4), 1984
    locator: the whole paper (each entity keyed by the smallest enclosing quadtree cell, kept in a linear order)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 3, Intervals and Small Rectangles, the section on the MX-CIF quadtree and its relatives
  - paper: doi:10.1145/50020.50021
    title: Hanan Samet, Hierarchical representations of collections of small rectangles, ACM Computing Surveys 20(4), 1988
    locator: the section on the MX-CIF quadtree (insertion, deletion and window search)
---

An MX-CIF quadtree stores a set of rectangles in a square. Each rectangle goes to the smallest cell of the [quadtree](/quadtree/) that holds all of it: the first cell, on the way down from the root, where the rectangle crosses one of the two center lines. So a rectangle is stored once, with no splitting and no copies, and the cells that hold rectangles are made only when needed. A query walks down from the root and tests the rectangles at each cell it visits; the rectangles that hold a given point all lie on one path. Kedem designed it in 1982 for the rectangles of chip layouts, under the name quad-CIF tree, and it is the rectangle counterpart of the [PR quadtree](/pr-quadtree/) for points.

## In plain words

You want to file many rectangles, such as the parts of a map or of a chip drawing. Cut the big square into four. A rectangle that fits in one of the four parts goes down into that part. A rectangle that crosses a cut line stays where it is.

Do the same in each part, again and again. Each rectangle ends up in the smallest square that holds it whole. It is filed once, never cut into pieces.

To find all rectangles that cover a point, walk down through the squares that hold the point. Check the rectangles filed in each one. You never need to look anywhere else.

## The abstract type

The MX-CIF quadtree is a [spatial index](/spatial-index/) for axis-parallel rectangles, such as [minimum bounding rectangles](/minimum-bounding-rectangle/). It supports `insert(r)`, `delete(r)`, `window(q)`, which reports the stored rectangles that meet the rectangle $q$, and `stab(p)`, which reports those that hold the point $p$. The same scheme in three dimensions stores boxes in an [octree](/octree/).

## Representation

The root cell is $[0, 2^D)^2$. Rectangles are half-open, $[x_1, x_2) \times [y_1, y_2)$ with integer corners and $x_1 < x_2$, $y_1 < y_2$. A node $u$ has a cell, a square with corner $(u.x, u.y)$ and side $u.size$, a list $u.rects$, and four child slots, numbered $o = b_x + 2b_y$ (0 southwest, 1 southeast, 2 northwest, 3 northeast), each empty or holding the node of that quadrant.

For a cell with center $(c_x, c_y)$, a rectangle $r$ lies in one quadrant when $x_2 \le c_x$ or $x_1 \ge c_x$, and $y_2 \le c_y$ or $y_1 \ge c_y$. Otherwise it crosses the vertical center line, the horizontal one, or both. A cell of side 1 has no quadrants.

**Invariant (M).** (1) Each rectangle is stored once, at a node $u$ whose cell holds it, and it does not lie in any quadrant of $u$. (2) The children of a node are its quadrants. (3) Each node other than the root stores a rectangle or has a child.

By part 1, each rectangle is at the smallest cell of the quadtree that holds it, since a cell that holds $r$ and is not the smallest has a quadrant that holds it. Part 3 says there are no useless nodes. With (M), the tree on a set of rectangles is unique, and does not depend on the order of the updates.

## Operations

```pseudo id=main
INSERT(T, r)
L1  u ← the root; o ← the quadrant of u that holds r, or none
L2  while o is not none:
L3      if child o of u is empty then make it a node for that quadrant
L4      u ← child o of u; o ← the quadrant of u that holds r, or none
L5  add r to u.rects

WINDOW(T, q)                               ▷ report the rectangles that meet q
L6  push the root on a stack S; while S is not empty: pop u
L7      if the cell of u does not meet q then skip u
L8      for each r in u.rects:
L9          if r meets q then report r
L10     push each child of u on S
```

The cell test in line L7 is safe: every rectangle at $u$ or below $u$ lies in the cell of $u$, so if the cell misses $q$, they all do.

```pseudo id=delete
DELETE(T, r)
L11 walk down from the root as in INSERT, keeping the path; if a child on the way is missing then return false
L12 if r is not in u.rects then return false; remove r from u.rects
L13 while u is not the root and u has no rectangles and no children:
L14     remove u from its parent; u ← the parent
    return true
```

A stab query for a point $p$ is a walk down one path: at each node it tests the rectangles there, then goes to the child that holds $p$. Each rectangle that holds $p$ lies in a cell that holds $p$, and these cells are all on that path.

## Example

Take $D = 3$, so the root is $[0, 8)^2$ with center $(4, 4)$, and five rectangles, written as $[x_1, x_2) \times [y_1, y_2)$.

| rectangle | cells on its path | stored at |
|---|---|---|
| A = $[1, 7) \times [2, 5)$ | it crosses $x = 4$ at the root | root |
| B = $[5, 7) \times [5, 7)$ | it goes to NE $[4, 8)^2$, center $(6, 6)$, and crosses $x = 6$ | NE |
| C = $[0, 1) \times [0, 1)$ | SW $[0, 4)^2$, then its SW $[0, 2)^2$, then its SW $[0, 1)^2$, of side 1 | the unit cell at $(0, 0)$ |
| D = $[1, 3) \times [6, 8)$ | it goes to NW $[0, 4) \times [4, 8)$, center $(2, 6)$, and crosses $x = 2$ | NW |
| E = $[4, 8) \times [0, 4)$ | it is the SE quadrant itself; in SE, center $(6, 2)$, it crosses both lines | SE |

The tree has 7 nodes: the root, the four quadrants, and two more cells on the path to C.

- **Window** $q = [5, 6) \times [1, 6)$. The root cell meets $q$, and A meets $q$. Of the quadrants, SW and NW miss $q$ and are skipped with all that lies below them; SE and NE meet it, and E and B meet $q$. The answer is A, B and E.
- **Stab** the point $(2, 7)$. At the root, A does not hold it, since $7 \ge 5$. The point is in NW, and D holds it. The answer is D, found by looking at two nodes.
- **Stab** the point $(5, 3)$. At the root A holds it; in SE, E holds it. The answer is A and E.
- **Delete** C. Its unit cell is now empty and has no children, so it is removed, and then the two cells above it, which are empty too. SW is removed last. The tree has 4 nodes.

## Correctness

INSERT goes down while $r$ lies in one quadrant and stops at the first cell where it does not, so it stores $r$ at the smallest cell that holds it, as part 1 asks; it makes only the nodes on that path, which then hold $r$ below them. DELETE finds $r$ on the same path, since the path depends only on $r$, and removes only nodes that are empty, from the bottom up. WINDOW skips only cells that miss $q$, and every rectangle at or below such a cell lies inside it, so it reports each rectangle that meets $q$, exactly once. The full proof is in the proofs folder.

## Complexity

The model is the word RAM with integer coordinates.

- **Height.** At most $D$, since each step halves the cell.
- **Insert and delete.** $O(D)$ to walk the path and $O(m)$ to scan the list at the node, where $m$ is the size of that list. With a hash set per node, the list cost is $O(1)$ expected.
- **Stab.** It visits at most $D + 1$ nodes and tests every rectangle at each one, so $O(D m)$ in the worst case. Kedem's form keeps, at each node, the rectangles that cross the vertical center line in a one-dimensional tree on their $y$ intervals, and those that cross only the horizontal line in a tree on their $x$ intervals, so that the test at a node costs time in the output, not in $m$.
- **Window.** It visits $v$ nodes and tests their lists. A small rectangle that crosses the center line of a big cell is stored high in the tree, so many queries test it.
- **Space.** Each rectangle is stored once, and each node is on the path of a stored rectangle, so there are at most $1 + nD$ nodes and $n$ entries.

| operation | time | case |
|---|---|---|
| insert | $O(D + m)$ | worst |
| delete | $O(D + m)$ | worst |
| stab | $O(D m)$ | worst |
| window | $O(v + v m)$ | worst, $v$ nodes visited |
| space | $O(n D)$ | total |

## Variants

- **Axis trees at a node.** Kedem's original form, and Samet's description, split the list of a node in two: rectangles that cross the vertical center line, kept in a binary tree on their $y$ extent, and the others, in a binary tree on their $x$ extent. These are one-dimensional MX-CIF trees on intervals, close to [interval trees](/interval-tree/) and [segment trees](/segment-tree/).
- **Linear form.** Abel and Smith kept each rectangle under the locational code of its smallest cell, in a B-tree, which is a [linear quadtree](/linear-quadtree/) of cells that hold rectangles.
- **Loose cells.** A small rectangle that crosses a center line near the root is the worst case. The [loose octree](/loose-octree/) and its two-dimensional form enlarge each cell by a margin so that such a rectangle fits in a deeper cell.
- **Splitting the rectangle.** Other quadtrees for rectangles, such as the PMR forms, store a rectangle in every leaf it meets. Queries then never look at large lists high in the tree, but each rectangle can be stored many times.
- **Higher dimensions.** The same rule gives a tree of boxes in an octree, or in any number of dimensions.

## When to use it

Use an MX-CIF quadtree for many small rectangles in a bounded square, with frequent insertions and deletions, when you want each object stored once and the tree independent of the order of updates. Chip layouts, the bounding boxes of map features and the boxes of moving objects in a game fit this. Use an [R-tree](/r-tree/) when the rectangles vary much in size, are large, or must be paged on disk with full nodes. Use a [uniform grid](/uniform-grid/) when all objects have about the same size.

## Pitfalls

- **Rectangles on the center lines.** A small rectangle that crosses the center of the root square is stored at the root, and every query looks at it. With many such rectangles, the root list is long and the tree gives no help; a loose quadtree, or splitting the rectangle, avoids this.
- **Closed against half-open rectangles.** With closed rectangles, a rectangle that touches a center line belongs to two quadrants, and the quadrant test must say which one, or store it higher. Use half-open rectangles and the same convention in all tests.
- **Degenerate rectangles.** A segment or a point has zero width; with half-open intervals it is empty. Give such objects a width of one unit, or use closed intervals with a fixed rule for the center line.
- **Not pruning.** If deletion leaves empty nodes, the tree depends on its history and grows with the number of updates, not with the number of rectangles.

## Implementations

## History

Kedem described the quad-CIF tree in 1982 for hierarchical algorithms on the rectangles of integrated circuit layouts, with CIF the Caltech Intermediate Form, a layout file format. Abel and Smith, in 1984, used the smallest enclosing quadtree cell as the key of areal entities in geographic databases. Samet named the structure the MX-CIF quadtree, by analogy with his MX quadtree for points, and treated it in his survey of 1988 and his books.

## References
