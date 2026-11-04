---
tag: AKGCFN
kind: data-structure
slug: octree
name: Octree
aliases:
- 3D quadtree
- 3D tree
- three-dimensional quadtree
area: data-structures/spatial-structures
level: core
summary: Three-dimensional analogue of the quadtree that splits a cube into eight octants.
implements: [spatial-index]
model: word-ram
complexity:
  vars: {n: the number of points, D: the number of halvings from the root cube to a unit cell, B: the leaf capacity, r: the number of reported points}
  time: {search: O(D + B), insert: O(D B), delete: O(D B), range_search: O(n D / B + n)}
  space: {total: O(n D / B + n)}
history:
  year: 1980
  people: [Chris L. Jackins, Steven L. Tanimoto, Donald Meagher]
  note: Jackins and Tanimoto described oct-trees for three-dimensional objects in 1980, and Meagher developed octree encoding for solid modeling in 1980 and 1982.
prereqs: [quadtree]
see_also: [pr-quadtree, loose-octree, linear-quadtree, kd-tree, z-order-curve, color-quantization, collision-detection, space-partitioning]
sources:
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 1, Multidimensional Point Data (the PR quadtree and its extension to more dimensions), and Chapter 2, Object-Based and Image-Based Image Representations (region octrees)
  - paper: doi:10.1016/0146-664X(82)90104-6
    title: Donald Meagher, Geometric modeling using octree encoding, Computer Graphics and Image Processing 19(2), 1982
    locator: the octree encoding of solids and the Boolean operations on it
  - paper: "Chris L. Jackins and Steven L. Tanimoto, Oct-trees and their use in representing three-dimensional objects, Computer Graphics and Image Processing 14(3), 1980"
    locator: the definition of the oct-tree as the three-dimensional form of the region quadtree
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 7, Spatial Partitioning (the section on octrees, with the octant index computed from three comparisons, and loose octrees)
  - paper: doi:10.1038/324446a0
    title: Josh Barnes and Piet Hut, A hierarchical O(N log N) force-calculation algorithm, Nature 324, 1986
    locator: the octree of cells over the particles and the opening criterion for the far-field approximation
---

An octree is a tree over a cube in which each internal node has eight children, the eight octants of its cube, made by cutting the cube in half along $x$, $y$ and $z$ at once. It is the three-dimensional form of the [quadtree](/quadtree/). This page treats the point-region (PR) octree, which stores points and splits a cell when it holds more than $B$ points, so that its shape depends only on the set of points. With integer coordinates in a cube of side $2^D$, its height is at most $D$, and it supports search, insertion, deletion and box queries. Octrees are used for collision detection, voxel models, point clouds, color quantization and N-body simulation.

## In plain words

Think of a box full of small marbles, and you want to find the marbles near a spot quickly. Cut the box into eight smaller boxes, two along each side. A small box with few marbles stays as it is. A small box with too many marbles is cut into eight again, and so on.

You get a tree: the big box at the top, each box below with its eight parts. Where marbles are packed close, the boxes are small and the tree is deep; where space is empty, one big box covers it.

To find a marble, go down the tree, picking at each box the part that holds the spot. To find all marbles in a region, open only the boxes that touch the region.

## The abstract type

The PR octree implements a [spatial index](/spatial-index/) for a set of points in a cube: `insert(p)`, `delete(p)`, `contains(p)`, and `range_search(ℓ, h)`, which reports the stored points $p$ with $\ell_i \le p_i \le h_i$ for $i = x, y, z$. The same tree also answers nearest neighbor and sphere queries, by the same branch and bound as the [k-d tree](/kd-tree/).

## Representation

The root is the cube $C = [0, 2^D)^3$, and points have integer coordinates in it. A node $u$ has a cell, a cube with corner $(u.x, u.y, u.z)$ and side $u.size$, a count $u.count$ of the points below it, and either

- a list $u.points$ of at most $B$ points, when $u$ is a leaf, or
- eight children, when $u$ is internal. With $s = u.size / 2$, child number $o = b_x + 2 b_y + 4 b_z$ has corner $(u.x + b_x s,\ u.y + b_y s,\ u.z + b_z s)$ and side $s$. A point $p$ is in octant $o$ where $b_x = 1$ exactly when $p_x \ge u.x + s$, and the same for $y$ and $z$.

The cells are half-open, so the eight child cells are disjoint and their union is the parent cell.

**Invariant (O).** (1) Each point lies in the cell of its leaf, and each point is stored once. (2) A leaf holds at most $B$ points. (3) The count of each internal node is more than $B$; it is the sum of the counts of its children.

Part 3 makes the tree *compact*: no internal node could be a leaf. With (O), the tree on a set $S$ is unique. The root is a leaf when $|S| \le B$, and otherwise it is internal with the trees of the eight octants as children. Two distinct integer points cannot share a cell of side 1, so a cell of side 1 never holds more than $B$ points, and the height is at most $D$.

## Operations

```pseudo id=main
INSERT(T, p)                               ▷ p in the root cube and not yet stored
L1  u ← the leaf whose cell holds p, by choosing the octant of p at each internal node
L2  add 1 to the count of each node on the path above u
L3  add p to u.points; u.count ← u.count + 1
L4  while |u.points| > B:
L5      make u internal with eight empty leaf children, the octants of its cell
L6      move each point of u.points to the child whose cell holds it, and set the counts
L7      if a child c holds more than B points then u ← c else stop
L8  return

RANGE-SEARCH(u, ℓ, h)                      ▷ report the points of the subtree u in the box
L9  if the cell of u does not meet the box [ℓ, h] then return
L10 if u is a leaf then report each p ∈ u.points with ℓi ≤ pi ≤ hi for each i; return
L11 for each child c of u: RANGE-SEARCH(c, ℓ, h)
```

Line L1 takes three comparisons per level to find the octant. After line L6, the $B + 1$ points are spread over eight children, so at most one child can hold more than $B$ of them, and line L7 follows that child. The loop of lines L4 to L7 makes a chain of splits when points are close together, at most one per level. A cell of side 1 holds one point, so the loop stops.

**Search** goes down as line L1 does and looks for $p$ in the leaf list.

**Deletion** removes the point and merges cells that have become too small.

```pseudo id=delete
DELETE(T, p)
L12 u ← the leaf whose cell holds p, keeping the path; if p ∉ u.points then return false
L13 remove p from u.points; subtract 1 from the count of u and of each node on the path
L14 for each node v of the path, from the bottom up: if v.count > B then stop; else make v a leaf whose points are the points of its eight children
L15 return true
```

In line L14, when $v.count \le B$, each child of $v$ has count at most $B$, so by (O) each internal child would have already been merged lower down: all eight children are leaves, and their points fit in one leaf. Once a node keeps more than $B$ points, so do all nodes above it, so the loop can stop.

## Example

Take $D = 3$, so the root cube is $[0, 8)^3$, and $B = 1$. The center of the root is $(4, 4, 4)$. A tree is written as a map from the numbers of the nonempty octants to their subtrees; a leaf is its list of points.

| step | what happens | tree after | nodes |
|---|---|---|---|
| insert (1,1,1) | the root is a leaf with room | [(1,1,1)] | 1 |
| insert (6,1,2) | the root overflows and splits; (1,1,1) goes to octant 0, (6,1,2) to octant 1 ($x \ge 4$) | {0: [(1,1,1)], 1: [(6,1,2)]} | 9 |
| insert (5,2,3) | it goes to octant 1, which overflows; that cell $[4,8) \times [0,4) \times [0,4)$ has center $(6,2,2)$, so (6,1,2) goes to its octant $1 + 4 = 5$ and (5,2,3) to its octant $2 + 4 = 6$ | {0: [(1,1,1)], 1: {5: [(6,1,2)], 6: [(5,2,3)]}} | 17 |
| insert (2,6,6), (7,7,7) | they go to the empty octants 6 and 7 of the root | {0: [(1,1,1)], 1: {5: [(6,1,2)], 6: [(5,2,3)]}, 6: [(2,6,6)], 7: [(7,7,7)]} | 17 |
| range $[4,7] \times [0,3] \times [0,3]$ | of the root's children only octant 1 meets the box; in it, octants 5 and 6 hold (6,1,2) and (5,2,3), both in the box | reports (5,2,3), (6,1,2) | |
| delete (5,2,3) | octant 1 of the root now has count 1, so it merges back into a leaf; the root keeps count 4 and stops the loop | {0: [(1,1,1)], 1: [(6,1,2)], 6: [(2,6,6)], 7: [(7,7,7)]} | 9 |

Inserting the same five points in any order gives the same tree, as (O) implies.

## Correctness

INSERT keeps (O): line L1 finds the only leaf whose cell holds $p$, since the child cells partition the parent cell, and the counts on the path go up by one. A split at line L5 makes a node internal with $B + 1 > B$ points, and line L6 puts each point in the child whose cell holds it. If one child overflows, the loop splits it in turn; the side halves at each pass, and a cell of side 1 cannot overflow, so the loop stops. DELETE keeps (O): after line L13 only the counts on the path change, and line L14 turns into leaves exactly the nodes whose count dropped to $B$ or less, from the bottom up. RANGE-SEARCH skips only subtrees whose cells do not meet the box, and by (O) part 1 such a subtree has no point in the box. The full proof is in the proofs folder.

## Complexity

The model is the word RAM with integer coordinates; the octant of a point takes three comparisons, or three bit tests when the cell sides are powers of two.

- **Height.** At most $D$. If the closest two points are at distance $\delta$, only cells of side at least about $\delta / \sqrt 3$ can hold both, so the height is $O(\log(2^D / \delta))$.
- **Search.** $O(D)$ to reach the leaf and $O(B)$ to scan it.
- **Insert.** $O(D)$ to reach the leaf, then at most $D$ splits of $B + 1$ points each: $O(D B)$ in the worst case, and $O(D + B)$ when no split chain forms.
- **Delete.** $O(D)$ for the path and $O(B)$ for each merge, at most $D$ merges: $O(D B)$.
- **Space.** At each depth, the internal nodes have disjoint cells with more than $B$ points each, so there are fewer than $n / (B + 1)$ of them. There are at most $D$ depths, and each internal node has eight children, so the tree has at most $1 + 8 D n / (B + 1)$ nodes: $O(n D / B + n)$. Two points that are close together cost a chain of nodes; two points at $(0,0,0)$ and $(1,1,1)$ in a cube of side $2^{10}$ need $1 + 8 \cdot 10 = 81$ nodes.
- **Range search.** In the worst case the search visits every node, $O(n D / B + n)$, even when it reports nothing: a box that meets every cell of a long chain does this. For a box with $r$ answers, the leaves inside the box cost $O(r)$ per $B$ points, and the cost of the rest depends on how many cells meet the boundary of the box. No bound like the $O(n^{1 - 1/k} + r)$ of the [k-d tree](/kd-tree/) holds, because the shape follows the data's density and not its count.

| operation | time | case |
|---|---|---|
| search | $O(D + B)$ | worst |
| insert | $O(D B)$ | worst |
| delete | $O(D B)$ | worst |
| range_search | $O(n D / B + n)$ | worst |
| space | $O(n D / B + n)$ | total |

## Variants

- **Region octree.** A voxel model of a solid: the cube is cut until each cell is all inside or all outside the solid, or is one voxel. This is Meagher's octree encoding, used in solid modeling and medical imaging. The [region quadtree](/region-quadtree/) is the two-dimensional form.
- **Point octree.** Split at a stored point instead of the center, as the [point quadtree](/point-quadtree/) does in the plane. The shape then depends on the order of insertion.
- **Linear octree.** Store only the leaves, each as the Morton code of its cell, in a sorted array or a [B-tree](/b-tree/). This is the [linear quadtree](/linear-quadtree/) in three dimensions, and the order is the [Z-order curve](/z-order-curve/).
- **Loose octree.** Each cell is enlarged by a factor, often 2, so that an object can be stored at one node by its center and size; see the [loose octree](/loose-octree/).
- **Sparse voxel octree.** A pointer-based octree over a very large voxel grid that stores only the nonempty cells, used for ray casting in graphics.
- **Barnes and Hut tree.** Each internal node keeps the total mass and center of mass of its particles, and the force on a particle treats a far cell as one particle. This takes $O(n \log n)$ time per step for particles spread evenly.
- **Octree color quantization.** Insert each pixel color as a point of the RGB cube, with depth 8, and merge leaves until $K$ remain; each leaf gives one color of the palette. See [color quantization](/color-quantization/).

## When to use it

Use an octree for points or objects in three dimensions when the data is spread unevenly and you want a structure whose cells follow the density, with no balancing work: point clouds, particles, voxel models, and the broad phase of [collision detection](/collision-detection/). Its shape does not depend on the order of insertion, and the cells have fixed positions, which makes it simple to merge two octrees or to address a cell by its code. Use a [k-d tree](/kd-tree/) when you need a bound on the height that depends on $n$ and not on the coordinates, or worst-case range bounds. Use a [uniform grid](/uniform-grid/) when the objects are of one size and spread evenly. In more than three or four dimensions, the $2^k$ children of each node make the tree wasteful.

## Pitfalls

- **Points too close together.** Two points that differ only in the last bits make a chain of $D$ splits. With floating-point coordinates there is no bound at all, and equal points make the split loop run forever. Fix a maximum depth, or use integer coordinates and store points as a set, as here.
- **Closed cells.** If the cells are closed, a point on a cut lies in two children, and the octant test and the cells disagree. Use half-open cells, and treat the top face of the root cube apart.
- **Forgetting to merge.** A deletion that does not merge small cells leaves empty internal nodes. The tree stays correct, but then its shape depends on the history of operations, and space and query time grow.
- **Objects with extent.** A PR octree stores points. An object that spans a cut must be stored in all the cells it meets, or at the smallest cell that holds it. Small objects that lie on the center plane of the root are then stored at the root; the [loose octree](/loose-octree/) and the [MX-CIF quadtree](/mx-cif-quadtree/) deal with this.
- **Recursion depth.** The depth is at most $D$, but for $D = 60$ or more with recursive code, a chain of close points still uses a deep stack. The implementation uses loops and an explicit stack.

## Implementations

## History

Octrees came out of the work on quadtrees for images in the 1970s. Jackins and Tanimoto described the oct-tree for three-dimensional objects in 1980, and Donald Meagher developed octree encoding for solid modeling in a 1980 report and a 1982 paper. Barnes and Hut used an octree of particles for their $O(n \log n)$ N-body method in 1986, and Gervautz and Purgathofer used one for color quantization in 1988. Samet's books of 1990 and 2006 put the point and region forms into one framework.

## References
