---
tag: K3B2RT
kind: data-structure
slug: quadtree
name: Quadtree
aliases:
- point quadtree
- quad tree
- region quadtree
area: data-structures/spatial-structures
level: core
summary: Tree in which each internal node splits a 2D square into four equal quadrants.
implements: [spatial-index]
model: word-ram
complexity:
  vars: {n: the number of points, D: the number of halvings from the root square to a unit cell, B: the leaf capacity}
  time: {search: O(D + B), insert: O(D B), delete: O(D B), range_search: O(n D / B + n)}
  space: {total: O(n D / B + n)}
history:
  year: 1974
  people: [Raphael A. Finkel, Jon Louis Bentley]
  note: Finkel and Bentley named the quad tree in 1974, as a tree for points that splits at a stored point.
prereqs: [binary-search-tree, uniform-grid]
see_also: [pr-quadtree, point-quadtree, region-quadtree, octree, kd-tree, linear-quadtree, z-order-curve, space-partitioning]
sources:
  - paper: doi:10.1007/BF00288933
    title: Raphael A. Finkel and Jon Louis Bentley, Quad trees, a data structure for retrieval on composite keys, Acta Informatica 4(1), 1974, pp. 1 to 9
    locator: the definition of the quad tree with four subtrees per node, insertion, and region search
  - paper: doi:10.1145/356924.356930
    title: Hanan Samet, The quadtree and related hierarchical data structures, ACM Computing Surveys 16(2), 1984
    locator: the survey of region, point and PR quadtrees and of the quadtrees for curves
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 14, Quadtrees, Section 14.2 (the quadtree of a point set, the bound on its depth in terms of the smallest distance, and the bound O((d + 1) n) on its size and building time)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 1, Multidimensional Point Data (point quadtrees, trie-based quadtrees and the PR quadtree, with deletion and search)
---

A quadtree is a tree over a square of the plane in which each internal node has four children, the four quadrants of its square, made by cutting the square in half along $x$ and along $y$. It is the two-dimensional form of the [binary search tree](/binary-search-tree/) idea of cutting the key space, and the plane form of the [octree](/octree/). This page treats the point-region (PR) quadtree, which stores points and splits a cell when it holds more than $B$ points, so that its shape depends only on the set of points. With integer coordinates in a square of side $2^D$, its height is at most $D$, and it supports search, insertion, deletion, window queries and nearest neighbor queries. The other members of the family, the [point quadtree](/point-quadtree/) and the [region quadtree](/region-quadtree/), are listed under Variants.

## In plain words

Take a square map with dots on it. If the square has only a few dots, stop. If it has too many, cut it into four equal smaller squares, and treat each small square in the same way. Where the dots are crowded, the squares become small; where the map is empty, one big square covers it.

The squares form a tree: the whole map at the top, and under each square its four parts. To find a dot, start at the top and go down into the part that holds it. To find all dots in a window, open only the squares that touch the window. To find the closest dot to a spot, open the squares in order of how far they are from the spot, and stop when the next square is farther than the best dot found.

## The abstract type

The PR quadtree implements a [spatial index](/spatial-index/) for a set of points in a square: `insert(p)`, `delete(p)`, `contains(p)`, `range_search(ℓ, h)`, which reports the stored points $p$ with $\ell_x \le p_x \le h_x$ and $\ell_y \le p_y \le h_y$, and `nearest(q)`, which returns a stored point at the smallest Euclidean distance from $q$.

## Representation

The root is the square $[0, 2^D)^2$, and points have integer coordinates in it. A node $u$ has a cell, a square with corner $(u.x, u.y)$ and side $u.size$, a count $u.count$ of the points below it, and either

- a list $u.points$ of at most $B$ points, when $u$ is a leaf, or
- four children, when $u$ is internal. With $s = u.size / 2$, child number $k = b_x + 2 b_y$ has corner $(u.x + b_x s,\ u.y + b_y s)$ and side $s$. A point $p$ is in quadrant $k$ where $b_x = 1$ exactly when $p_x \ge u.x + s$, and $b_y = 1$ exactly when $p_y \ge u.y + s$.

The cells are half-open, so the four child cells are disjoint and their union is the parent cell. Quadrant 0 is the lower left, 1 the lower right, 2 the upper left and 3 the upper right.

**Invariant (Q).** (1) Each point lies in the cell of its leaf, and each point is stored once. (2) A leaf holds at most $B$ points. (3) The count of each internal node is more than $B$, and it is the sum of the counts of its children.

Part 3 makes the tree *compact*: no internal node could be a leaf. With (Q), the tree of a set $S$ is unique: the root is a leaf when $|S| \le B$, and otherwise it is internal with the trees of the four quadrants as children. Two distinct integer points cannot share a cell of side 1, so the height is at most $D$.

## Operations

```pseudo id=main
INSERT(T, p)                               ▷ p in the root square and not yet stored
L1  u ← the leaf whose cell holds p, by choosing the quadrant of p at each internal node
L2  add 1 to the count of each node on the path above u
L3  add p to u.points; u.count ← u.count + 1
L4  while |u.points| > B:
L5      make u internal with four empty leaf children, the quadrants of its cell
L6      move each point of u.points to the child whose cell holds it, and set the counts
L7      if a child c holds more than B points then u ← c else stop
L8  return

RANGE-SEARCH(u, ℓ, h)                      ▷ report the points of the subtree u in the window
L9  if the cell of u does not meet the window [ℓ, h] then return
L10 if u is a leaf then report each p ∈ u.points inside the window; return
L11 for each child c of u: RANGE-SEARCH(c, ℓ, h)
```

Line L1 makes two comparisons per level. After line L6, the $B + 1$ points are spread over four children, so at most one child can hold more than $B$ of them, and line L7 follows that child. Points that are close together make a chain of splits, at most one per level. A cell of side 1 holds one point, so the loop stops.

**Search** goes down as line L1 does and looks for $p$ in the leaf list.

```pseudo id=delete
DELETE(T, p)
L12 u ← the leaf whose cell holds p, keeping the path; if p ∉ u.points then return false
L13 remove p from u.points; subtract 1 from the count of u and of each node on the path
L14 for each node v of the path, from the bottom up: if v.count > B then stop; else make v a leaf whose points are the points of its four children
L15 return true
```

In line L14, when $v.count \le B$, each child of $v$ has count at most $B$, so by (Q) each child is a leaf, and their points fit in one leaf. Once a node keeps more than $B$ points, so do all nodes above it, and the loop stops.

```pseudo id=nearest
NEAREST(T, q)                              ▷ best-first search with a min-priority queue
L16 best ← none; H ← a priority queue holding the root with key dist(q, cell of root)
L17 while H is not empty:
L18     (d, u) ← extract the node with the smallest key from H
L19     if best ≠ none and d ≥ |q − best| then stop
L20     if u is a leaf then for each p ∈ u.points: if best = none or |q − p| < |q − best| then best ← p
L21     else for each child c with c.count > 0: insert c into H with key dist(q, cell of c)
L22 return best
```

Here $\operatorname{dist}(q, Z)$ is the distance from $q$ to the closest point of the cell $Z$, which is $0$ when $q \in Z$. Each point below $u$ is at distance at least $\operatorname{dist}(q, \text{cell of } u)$, and the keys come out of the [priority queue](/priority-queue/) in increasing order, so once the smallest key is at least the best distance, no cell left can hold a closer point.

## Example

Take $D = 4$, so the root square is $[0, 16)^2$, and $B = 1$. The center of the root is $(8, 8)$. A tree is written as a map from the numbers of the nonempty quadrants to their subtrees; a leaf is its list of points.

| step | what happens | tree after | nodes |
|---|---|---|---|
| insert (2, 3) | the root is a leaf with room | [(2,3)] | 1 |
| insert (12, 2) | the root overflows and splits; (2,3) goes to quadrant 0, (12,2) to quadrant 1 | {0: [(2,3)], 1: [(12,2)]} | 5 |
| insert (9, 6) | it goes to quadrant 1, which overflows; that cell $[8,16) \times [0,8)$ has center $(12, 4)$, so (12,2) goes to its quadrant 1 and (9,6) to its quadrant 2 | {0: [(2,3)], 1: {1: [(12,2)], 2: [(9,6)]}} | 9 |
| insert (5, 12), (14, 13) | they go to the empty quadrants 2 and 3 of the root | {0: [(2,3)], 1: {1: [(12,2)], 2: [(9,6)]}, 2: [(5,12)], 3: [(14,13)]} | 9 |
| insert (11, 7) | it meets (9,6) in the cell $[8,12) \times [4,8)$ with center $(10, 6)$; (9,6) goes to quadrant 2 and (11,7) to quadrant 3 | {0: [(2,3)], 1: {1: [(12,2)], 2: {2: [(9,6)], 3: [(11,7)]}}, 2: [(5,12)], 3: [(14,13)]} | 13 |
| range $[8,12] \times [4,8]$ | only quadrant 1 of the root meets it, then only its quadrant 2, whose two leaves hold the answers | (9,6), (11,7) | |
| nearest (10, 10) | the squared distances are 10 to (11,7), 17 to (9,6), 25 to (14,13) and 29 to (5,12) | (11,7) | |
| delete (11, 7) | the cell $[8,12) \times [4,8)$ has count 1, so it becomes a leaf again; its parent has count 2 and stops the loop | {0: [(2,3)], 1: {1: [(12,2)], 2: [(9,6)]}, 2: [(5,12)], 3: [(14,13)]} | 9 |

The height after the fifth insertion is 3. Inserting the same points in any order gives the same tree, as (Q) implies.

## Correctness

INSERT keeps (Q): line L1 finds the only leaf whose cell holds $p$, since the child cells partition the parent cell, and the counts on the path go up by one. A split at line L5 makes a node internal with $B + 1 > B$ points, and line L6 puts each point in the child whose cell holds it. If one child overflows, the loop splits it in turn; the side halves at each pass, and a cell of side 1 cannot overflow, so the loop stops. DELETE keeps (Q): line L14 turns into leaves exactly the nodes whose count dropped to $B$ or less, from the bottom up. RANGE-SEARCH skips only subtrees whose cells do not meet the window, and by (Q) part 1 such a subtree has no point in the window. NEAREST stops only when no cell in the queue can hold a point closer than the best one. The full proof is in the proofs folder.

## Complexity

The model is the [word RAM](/word-ram/) with integer coordinates; the quadrant of a point takes two comparisons.

- **Height.** At most $D$. If the closest two points are at distance $\delta$, a cell of side $s$ has diameter $s\sqrt 2$, so only cells with $s \sqrt 2 \ge \delta$ can hold both, and the height is at most $\log_2(2^D \sqrt 2 / \delta) + 1$. De Berg and others give the bound $\log_2(s/c) + 3/2$ for a root side $s$ and smallest distance $c$.
- **Search.** $O(D)$ to reach the leaf and $O(B)$ to scan it.
- **Insert.** $O(D)$ to reach the leaf, then at most $D$ splits of $B + 1$ points each: $O(D B)$ in the worst case, and $O(D + B)$ when no chain of splits forms.
- **Delete.** $O(D)$ for the path and $O(B)$ for each merge, at most $D$ merges: $O(D B)$.
- **Space.** At each depth, the internal nodes have disjoint cells with more than $B$ points each, so there are fewer than $n / (B + 1)$ of them. There are at most $D$ depths, and each internal node has four children, so the tree has at most $1 + 4 D n / (B + 1)$ nodes: $O(n D / B + n)$. Two points at $(0, 0)$ and $(1, 1)$ in a square of side $2^{10}$ need $1 + 4 \cdot 10 = 41$ nodes.
- **Range search.** In the worst case the search visits every node, $O(n D / B + n)$, even when it reports nothing: a thin window along a long chain of cells does this. Unlike the [k-d tree](/kd-tree/), the quadtree has no bound of the form $O(\sqrt n + k)$, because its shape follows the positions of the points and not their number.
- **Nearest.** The queue holds at most all nodes, so the worst case is $O(N \log N)$ for a tree of $N$ nodes. On points spread evenly the search opens only a few cells near $q$.

| operation | time | case |
|---|---|---|
| search | $O(D + B)$ | worst |
| insert | $O(D B)$ | worst |
| delete | $O(D B)$ | worst |
| range_search | $O(n D / B + n)$ | worst |
| space | $O(n D / B + n)$ | total |

## Variants

- **Point quadtree.** Finkel and Bentley's original form: each node stores one point and splits its region at that point into four quadrants of unequal size. The shape depends on the order of insertion, as in a binary search tree, and deletion is hard. See the [point quadtree](/point-quadtree/).
- **PR quadtree.** The form of this page with $B = 1$: split at the center until each cell has at most one point. See the [PR quadtree](/pr-quadtree/).
- **Region quadtree.** For a binary image of $2^D \times 2^D$ pixels: cut each square until it is all black or all white. See the [region quadtree](/region-quadtree/).
- **MX-CIF quadtree.** Store each rectangle at the smallest cell that contains it. See the [MX-CIF quadtree](/mx-cif-quadtree/).
- **Linear quadtree.** Store only the leaves, each by the code of its cell on the [Z-order curve](/z-order-curve/), in a sorted array or a [B-tree](/b-tree/). See the [linear quadtree](/linear-quadtree/).
- **Compressed quadtree.** Replace each chain of internal nodes with only one nonempty child by one edge. The tree then has $O(n)$ nodes whatever the coordinates, and the height bound in terms of $D$ is replaced by a bound in $n$.
- **Higher dimensions.** The [octree](/octree/) has eight children per node. In $d$ dimensions there are $2^d$ children, which becomes wasteful for $d$ above 3 or 4; the [k-d tree](/kd-tree/) cuts one axis at a time instead.

## When to use it

Use a PR quadtree for points in the plane when the data is spread unevenly and you want cells that follow the density, a shape that does not depend on the order of insertion, and cells at fixed positions that are simple to name by a code. This suits map tiles, images, mesh generation and hierarchical summaries such as the Barnes and Hut method of the [octree](/octree/) page. Use a [uniform grid](/uniform-grid/) when the points are spread evenly, and a [k-d tree](/kd-tree/) when you need a height bound in terms of $n$ or worst-case window bounds. For rectangles and other objects with extent in a database, an [R-tree](/r-tree/) is the usual choice.

## Pitfalls

- **Points too close together.** Two points that differ only in the last bits make a chain of $D$ splits. With floating-point coordinates there is no bound at all, and two equal points make the loop of line L4 run forever. Fix a maximum depth, or use integer coordinates and store points as a set, as here.
- **Closed cells.** If cells are closed, a point on a cut line lies in two children. Use half-open cells, and treat the top and right edges of the root square apart.
- **Forgetting to merge.** A deletion that skips line L14 leaves internal nodes with few points. The answers stay correct, but the shape then depends on the history, and space and time grow.
- **Recursion depth.** With $D = 60$, recursive code follows a chain of 60 nodes, which is fine; with floating-point keys and no depth limit it can overflow the stack. The implementation uses loops and an explicit stack.
- **A wrong pruning test in NEAREST.** Pruning with the distance to the center of a cell instead of the distance to the cell can skip the cell that holds the answer. Line L19 must use the distance to the closest point of the cell.

## Implementations

## History

Raphael Finkel and Jon Bentley introduced the quad tree in 1974, as a tree for points with two keys in which each node splits at its point into four parts, with insertion and region search. Region quadtrees for images were used by Klinger and others in the early 1970s, and Hanan Samet's survey of 1984 brought the point, region and PR forms into one framework. De Berg, Cheong, van Kreveld and Overmars use the PR quadtree for mesh generation in their textbook, with the bounds on its depth and size.

## References
