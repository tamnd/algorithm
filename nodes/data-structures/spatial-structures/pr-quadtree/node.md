---
tag: D4SJDH
kind: data-structure
slug: pr-quadtree
name: PR quadtree
aliases:
- point-region quadtree
area: data-structures/spatial-structures
level: advanced
summary: Quadtree that subdivides a cell until each leaf holds at most a fixed number of points.
implements: [spatial-index]
model: word-ram
complexity:
  vars: {n: the number of points, D: the number of halvings from the root square to a unit cell, B: the leaf capacity, r: the number of reported points}
  time: {search: O(D + B), insert: O(D B), delete: O(D B), range_search: O(n D / B + n)}
  space: {total: O(n D / B + n)}
history:
  year: 1982
  people: [Jack A. Orenstein, Hanan Samet]
  note: The idea of splitting fixed square cells until each holds one point appears in Orenstein's 1982 work on multidimensional tries; Samet named and studied the PR quadtree in his 1984 survey and his books.
prereqs: [quadtree, trie]
see_also: [point-quadtree, octree, region-quadtree, linear-quadtree, mx-cif-quadtree, kd-tree, z-order-curve, uniform-grid]
sources:
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 1, Multidimensional Point Data, the sections on trie-based point quadtrees (the PR quadtree, its bucket form and its analysis)
  - paper: doi:10.1145/356924.356930
    title: Hanan Samet, The quadtree and related hierarchical data structures, ACM Computing Surveys 16(2), 1984
    locator: the section on point data (the PR quadtree, with insertion, deletion and merging of cells)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 14, Quadtrees (the quadtree on a point set with one point per leaf, its depth bound in terms of the spread, and neighbor finding)
---

A PR (point-region) quadtree stores a set of points in a square. A cell that holds more than $B$ points is cut into four equal quadrants, and the cutting goes on until each leaf cell holds at most $B$ points. The cuts are at the centers of the cells, not at data points, so the tree is a [trie](/trie/) on the bits of the coordinates: its shape depends only on the set of points, never on the order of insertion. With integer coordinates in a square of side $2^D$, the height is at most $D$, and search, insertion and deletion take $O(D)$ steps plus the work on the leaves. It is the most common form of quadtree for points.

## In plain words

Draw a square around all your points. If it holds too many points, cut it into four equal squares. Cut again each small square that still holds too many, and stop when every square holds only a few.

Where points are crowded, the squares get small. Where the map is empty, one big square stays.

The squares are always the same, wherever the points are: each cut goes through the middle. So two people who put the same points in any order get the same picture. To find a point, start with the big square and step each time into the quarter that holds it.

## The abstract type

The PR quadtree implements a [spatial index](/spatial-index/) for a set of points in a square: `insert(p)`, `delete(p)`, `contains(p)`, and `range_search(ℓ, h)`, which reports the stored points in the box $[\ell_x, h_x] \times [\ell_y, h_y]$. It also answers nearest neighbor queries by branch and bound, and it is the base of neighbor finding and of the mesh generation methods of computational geometry.

## Representation

The root cell is $[0, 2^D)^2$, and the points have integer coordinates in it. A node $u$ has a cell, a square with corner $(u.x, u.y)$ and side $u.size$, a count $u.count$ of the points below it, and either a list $u.points$ of at most $B$ points (a leaf), or four children (an internal node). With $s = u.size/2$, child $o = b_x + 2b_y$ has corner $(u.x + b_x s, u.y + b_y s)$ and side $s$, so 0 is southwest, 1 southeast, 2 northwest and 3 northeast. A point is in the east half when $p_x \ge u.x + s$, and in the north half when $p_y \ge u.y + s$. The cells are half-open, so the four children partition their parent.

With side a power of two, the quadrant at depth $j$ is given by bit $D - 1 - j$ of $p_x$ and of $p_y$: the path to a leaf is read from the bits of the coordinates, from the top. This is why the PR quadtree is a trie, and why its leaves in the order 0, 1, 2, 3 at each level are sorted by the [Z-order](/z-order-curve/) of their cells.

**Invariant (R).** (1) Each point lies in the cell of its leaf and is stored once. (2) A leaf holds at most $B$ points. (3) An internal node has more than $B$ points below it, and its count is the sum of those of its children.

Part 3 makes the tree compact: each internal node is needed. With (R), the tree on a set $S$ is unique: the root is a leaf if $|S| \le B$, and otherwise the four children are the trees of the four quadrants. A cell of side 1 holds at most one integer point, so it never needs to split, and the height is at most $D$.

## Operations

```pseudo id=main
INSERT(T, p)                               ▷ p in the root square and not yet stored
L1  u ← the leaf whose cell holds p, by taking the quadrant of p at each internal node
L2  add 1 to the count of each internal node on the path
L3  add p to u.points; u.count ← u.count + 1
L4  while |u.points| > B:
L5      make u internal with four empty leaf children, the quadrants of its cell
L6      move each point of u.points to the child whose cell holds it, and set the counts
L7      if a child c holds more than B points then u ← c else stop
L8  return

RANGE-SEARCH(u, ℓ, h)
L9  if the cell of u does not meet [ℓx, hx] × [ℓy, hy] then return
L10 if u is a leaf then report the points of u.points that lie in the box; return
L11 for each child c of u: RANGE-SEARCH(c, ℓ, h)
```

After line L6 the $B + 1$ points are spread over four children, so at most one of them can hold more than $B$, and line L7 follows it. Two points that are close make a chain of splits, one per level, until a cell separates them.

```pseudo id=delete
DELETE(T, p)
L12 u ← the leaf whose cell holds p, keeping the path; if p ∉ u.points then return false
L13 remove p from u.points; subtract 1 from the count of u and of each node on the path
L14 for each node v of the path, from the bottom up: if v.count > B then stop; else make v a leaf holding the points of its four children
L15 return true
```

When $v.count \le B$ in line L14, each child of $v$ has at most $B$ points, so by (R) it is a leaf, or was just made one; the points of the four leaves fit in one leaf. Once a node keeps more than $B$ points, so do all nodes above it.

## Example

Take $D = 3$, so the root is $[0, 8)^2$ with center $(4, 4)$, and $B = 1$. A tree is written as a map from the numbers of the nonempty quadrants to subtrees, and a leaf as its list.

| step | what happens | tree after | nodes |
|---|---|---|---|
| insert (1,6) | the root is a leaf with room | [(1,6)] | 1 |
| insert (5,5) | the root splits: (1,6) is NW (2), (5,5) is NE (3) | {2: [(1,6)], 3: [(5,5)]} | 5 |
| insert (6,7) | it goes to NE, which splits at its center $(6, 6)$: (5,5) is its SW (0), (6,7) its NE (3) | {2: [(1,6)], 3: {0: [(5,5)], 3: [(6,7)]}} | 9 |
| insert (2,1) | it goes to the empty SW quadrant of the root | {0: [(2,1)], 2: [(1,6)], 3: {0: [(5,5)], 3: [(6,7)]}} | 9 |
| insert (3,2) | SW splits at its center $(2, 2)$: (2,1) is its SE (1), (3,2) its NE (3) | {0: {1: [(2,1)], 3: [(3,2)]}, 2: [(1,6)], 3: {0: [(5,5)], 3: [(6,7)]}} | 13 |
| range $[2, 6] \times [1, 5]$ | the box meets SW, NW and NE of the root; in them it reports (2,1), (3,2) and (5,5); (1,6) and (6,7) are outside | (2,1), (3,2), (5,5) | |
| delete (6,7) | NE now has one point and merges back into a leaf; the root still has 4 points | {0: {1: [(2,1)], 3: [(3,2)]}, 2: [(1,6)], 3: [(5,5)]} | 9 |

The result does not depend on the order of the five insertions.

## Correctness

INSERT keeps (R): line L1 reaches the only leaf whose cell holds $p$, since the children of a node partition its cell, and each split moves points into the child cell that holds them. The loop stops because the side halves at each split and a cell of side 1 never overflows. DELETE turns into leaves exactly the nodes whose count fell to $B$ or less, from the bottom up, so (R) holds after it. RANGE-SEARCH skips only cells that miss the box, and by (R) such a cell holds no point of the box. The full proof is in the proofs folder.

## Complexity

The model is the word RAM with integer coordinates.

- **Height.** At most $D$. In terms of the data, if the closest two points are at distance $\delta$ and the root has side $L$, the height is at most $\lg(L/\delta) + 1$ up to a constant: a cell of side $\sigma$ has diameter $\sigma\sqrt 2$, so it holds two points only if $\sigma \sqrt 2 > \delta$. de Berg and others state this as a bound in terms of the *spread* $L/\delta$.
- **Search.** $O(D)$ to reach the leaf and $O(B)$ to scan it.
- **Insert and delete.** $O(D)$ for the path, and $O(B)$ for each split or merge, at most $D$ of them: $O(D B)$ in the worst case.
- **Space.** At one depth, the internal nodes have disjoint cells with more than $B$ points each, so there are fewer than $n/(B+1)$ of them; with at most $D$ depths and four children each, the tree has at most $1 + 4Dn/(B+1)$ nodes. Two points at $(0, 0)$ and $(1, 1)$ in a square of side $2^{12}$ need $1 + 4 \cdot 12 = 49$ nodes.
- **Range search.** In the worst case it visits all nodes, $O(nD/B + n)$; for well spread points, the cells that meet the boundary of the box dominate.

| operation | time | case |
|---|---|---|
| search | $O(D + B)$ | worst |
| insert | $O(D B)$ | worst |
| delete | $O(D B)$ | worst |
| range_search | $O(n D / B + n)$ | worst |
| space | $O(n D / B + n)$ | total |

## Variants

- **Bucket PR quadtree.** This page already allows $B > 1$ points per leaf; the plain PR quadtree has $B = 1$. Larger buckets make the tree shallower and suit disk pages.
- **Compressed quadtree.** Replace each chain of nodes with one nonempty child by a single edge to the bottom cell. The tree then has $O(n)$ nodes for any point set, whatever $D$ is, and can be built in $O(n \log n)$ time.
- **Linear quadtree.** Store only the leaves, each by the Z-order code of its cell, in a sorted array or a B-tree; see the [linear quadtree](/linear-quadtree/).
- **PMR and PM quadtrees.** Forms for line segments and polygon maps, which split a cell when too many segments cross it.
- **Higher dimensions.** The [octree](/octree/) in three dimensions; in $k$ dimensions a node has $2^k$ children.
- **Balanced quadtree.** For mesh generation, the tree is refined so that neighboring leaves differ by at most a factor 2 in size, which de Berg and others treat in Chapter 14.

## When to use it

Use a PR quadtree for points in the plane when you want a structure that is simple, does not depend on the insertion order, and whose cells have fixed positions, so that two trees can be compared or merged cell by cell. It suits data with integer or bounded coordinates, and uses such as neighbor finding, mesh generation and image-like data. Use a [k-d tree](/kd-tree/) when the points are very unevenly spread or have unbounded coordinates, since the PR quadtree's depth grows with the ratio of the largest to the smallest distance, not with $n$. Use a [uniform grid](/uniform-grid/) for evenly spread points of one density.

## Pitfalls

- **Equal or very close points.** With $B$ or more equal points, or real coordinates with no unit, the split loop never ends. Store points as a set, use integer coordinates, or fix a maximum depth and let the deepest leaves overflow.
- **Points on the edges.** With closed cells, a point on a cut lies in two quadrants. Use half-open cells, and apply the same rule in the quadrant test and in the range test.
- **Not merging.** If deletion does not merge cells, empty internal nodes pile up, the tree is no longer unique, and space grows.
- **Recursion depth.** Use loops for the path and an explicit stack for the range search; a chain of close points can make the tree as deep as $D$.

## Implementations

## History

Quadtrees with cuts at the centers of cells came from image processing in the early 1970s. For points, the trie-like split of fixed cells appears in Orenstein's 1982 work on multidimensional tries, and Samet named the PR quadtree and analyzed it in his survey of 1984 and in his books of 1990 and 2006. de Berg and others use it in their chapter on quadtrees and mesh generation.

## References
