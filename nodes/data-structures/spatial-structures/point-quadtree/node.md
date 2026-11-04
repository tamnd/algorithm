---
tag: C2HX1P
kind: data-structure
slug: point-quadtree
name: Point quadtree
aliases:
- point quadtree
area: data-structures/spatial-structures
level: advanced
summary: Quadtree in which each node stores a data point and its split point is that point, not a fixed grid line.
implements: [spatial-index]
model: real-ram
complexity:
  vars: {n: the number of points, h: the height of the tree, r: the number of reported points, s: the size of the subtree of the deleted node}
  time: {build: O(n log n), search: O(h), insert: O(h), delete: O(s h), range_search: O(n)}
  space: {total: Θ(n)}
history:
  year: 1974
  people: [Raphael A. Finkel, Jon Louis Bentley]
  note: Finkel and Bentley introduced the quad tree for retrieval on composite keys in Acta Informatica in 1974, with insertion, region search and a balanced build.
prereqs: [quadtree, binary-search-tree]
see_also: [kd-tree, pr-quadtree, kd-tree-range-query-complexity, octree, orthogonal-range-searching, range-tree, mx-cif-quadtree, region-quadtree]
sources:
  - paper: doi:10.1007/BF00288933
    title: Raphael A. Finkel and Jon Louis Bentley, Quad trees, a data structure for retrieval on composite keys, Acta Informatica 4(1), 1974
    locator: pages 1 to 9 (the tree with four subtrees per stored point, insertion, region search, deletion by reinsertion, and the optimized tree built by medians)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 1, Multidimensional Point Data, the section on point quadtrees (insertion, deletion, search, and the analysis of random trees)
  - paper: doi:10.1145/356924.356930
    title: Hanan Samet, The quadtree and related hierarchical data structures, ACM Computing Surveys 16(2), 1984
    locator: the section on point data and the point quadtree
---

A point quadtree is a tree for points in the plane in which each node holds one point and splits the plane around it into four quadrants: northwest, northeast, southwest and southeast. Each child holds the points of one quadrant, split again around its own point. It is the two-dimensional form of the [binary search tree](/binary-search-tree/), in the same way that the [k-d tree](/kd-tree/) is, but with four children per node instead of two. Finkel and Bentley introduced it in 1974. Unlike the [PR quadtree](/pr-quadtree/), whose cells are fixed squares, its splits fall on the data points, so its shape depends on the order of insertion.

## In plain words

Put the first point on a map and draw a cross through it: a vertical line and a horizontal line. The map now has four parts.

Each new point falls in one of the four parts. If that part is empty, the point goes there. If it has a point already, go to that point, and look at its cross: the new point falls in one of its four smaller parts. Keep going until you reach an empty part.

To find all points in a box, start at the top. Report the point if it is in the box, and go only into the parts that the box touches.

## The abstract type

A point quadtree implements a [spatial index](/spatial-index/) for a set of points in the plane: `insert(p)`, `delete(p)`, `contains(p)`, and `range_search(ℓ, h)`, which reports the points $p$ with $\ell_x \le p_x \le h_x$ and $\ell_y \le p_y \le h_y$. The same branch and bound as in the k-d tree answers nearest neighbor queries. In $k$ dimensions the same idea gives $2^k$ children per node.

## Representation

Each node $t$ holds a point $t.point$ and four children $t.child[0..3]$. The quadrant of a point $q$ around $p$ is
$$\text{quad}(p, q) = [q_x \ge p_x] + 2\,[q_y \ge p_y],$$
so 0 is southwest, 1 southeast, 2 northwest and 3 northeast. Points on the lines through $p$ go east or north.

**Invariant (Q).** For each node $t$ and each point $q$ in the subtree $t.child[i]$, $\text{quad}(t.point, q) = i$. No point is stored twice.

From (Q), each node owns a rectangle, its region: the root owns the plane, and the cross through the point of a node cuts its region into the regions of its four children, each a half-open rectangle.

## Operations

```pseudo id=main
INSERT(T, p)
L1  if T.root = nil then T.root ← a new node with point p; return
L2  t ← T.root; loop: if t.point = p then return       ▷ already stored
L3      i ← quad(t.point, p)
L4      if t.child[i] = nil then t.child[i] ← a new node with point p; return
L5      t ← t.child[i]

RANGE-SEARCH(t, ℓ, h)                      ▷ report the points of the subtree t in [ℓx, hx] × [ℓy, hy]
L6  if t = nil then return
L7  if ℓx ≤ t.point_x ≤ hx and ℓy ≤ t.point_y ≤ hy then report t.point
L8  W ← (ℓx < t.point_x); E ← (hx ≥ t.point_x); S ← (ℓy < t.point_y); N ← (hy ≥ t.point_y)
L9  recurse into child 0 if S and W, child 1 if S and E, child 2 if N and W, child 3 if N and E
```

Line L8 tests whether the box can reach each side of the cross. The west side holds points with $x < t.point_x$, so the box reaches it only if $\ell_x < t.point_x$; the east side holds points with $x \ge t.point_x$, so the box reaches it only if $h_x \ge t.point_x$.

**Search** follows the path of INSERT and stops at the point or at an empty child.

**Deletion** is the hard operation. In a binary search tree, a deleted node is replaced by its successor, but a quadtree has no point that can replace the deleted one and keep all four quadrants of all the points below it. The simple method of Finkel and Bentley cuts out the subtree and inserts its points again:

```pseudo id=delete
DELETE(T, p)
L10 find the node t with t.point = p by the path of INSERT; if there is none, return false
L11 R ← the points of all nodes below t
L12 remove the subtree of t from its parent (or make the tree empty if t is the root)
L13 INSERT(T, q) for each q ∈ R; return true
```

The points of $R$ all lie in the region of $t$, so they go back into the same place below the parent of $t$. Samet gave a deletion method in 1980 that chooses a replacement point and reinserts only the points of some quadrants, which is faster on average.

**Balanced build.** For a static set, choose as root the median of the points by $x$, and build the four quadrants the same way. If the $x$ coordinates are distinct, the west half has $\lfloor n/2 \rfloor$ points and the east half $\lceil n/2 \rceil - 1$, so each child has at most half the points of its parent, and the height is at most $\lfloor \lg n \rfloor + 1$.

## Example

Insert, in this order, the points $(35, 40)$, $(50, 10)$, $(60, 75)$, $(80, 65)$, $(85, 15)$, $(5, 45)$, $(25, 35)$, $(90, 5)$. A tree is written as (point, [SW, SE, NW, NE]), and a leaf as its point.

| step | path | where it goes |
|---|---|---|
| (35,40) | | root |
| (50,10) | SE of (35,40) | SE child of the root |
| (60,75) | NE of (35,40) | NE child of the root |
| (80,65) | NE of (35,40), then SE of (60,75): $80 \ge 60$, $65 < 75$ | SE child of (60,75) |
| (85,15) | SE of (35,40), then NE of (50,10) | NE child of (50,10) |
| (5,45) | NW of (35,40) | NW child of the root |
| (25,35) | SW of (35,40) | SW child of the root |
| (90,5) | SE of (35,40), then SE of (50,10) | SE child of (50,10) |

The tree is ((35,40), [(25,35), ((50,10), [nil, (90,5), nil, (85,15)]), (5,45), ((60,75), [nil, (80,65), nil, nil])]), of height 3.

- **Range search** with $[20, 70] \times [30, 80]$. At (35,40) the box reaches all four quadrants, and the point is reported. In SW, (25,35) is reported. In SE, at (50,10), the box has $\ell_y = 30 \ge 10$, so only the north children are searched, and both are empty. In NW, (5,45) is outside the box. In NE, (60,75) is reported; the box reaches all four quadrants of (60,75), so the search visits its SE child (80,65), which is outside the box. The answer is (25,35), (35,40), (60,75).
- **Delete** (50,10). Its subtree holds (90,5) and (85,15). The subtree is cut off, and the two points are inserted again: (85,15) becomes the SE child of the root, and (90,5) the SE child of (85,15).
- **Balanced build** of the same eight points. Sorted by $x$, the point of rank 4 is (60,75), which becomes the root. Its SW quadrant gets the four points with $x < 60$, and its SE quadrant the other three, all below $y = 75$. The tree is ((60,75), [((35,40), [(25,35), (50,10), (5,45), nil]), ((85,15), [nil, (90,5), (80,65), nil]), nil, nil]), of height 3.

## Correctness

INSERT keeps (Q): the new point is put in the quadrant that $\text{quad}$ gives at each node of its path, and no other node changes. RANGE-SEARCH reports exactly the points in the box: it tests each point it visits, and line L9 skips a quadrant only when no point of that quadrant can lie in the box, by (Q) and the test of line L8. DELETE keeps (Q): after the cut, the tree minus the subtree satisfies (Q), and each point of $R$ is then inserted by INSERT. The full proof is in the proofs folder.

## Complexity

- **Search and insert.** One path: $O(h)$.
- **Height.** After a balanced build on points with distinct $x$ coordinates, $h \le \lfloor \lg n \rfloor + 1$. After insertions in random order, the expected depth of a node is $O(\log n)$, about $\ln n$ for the last point inserted, by the analysis of Devroye and Laforest. After insertions in sorted order, such as $(1,1), (2,2), \ldots$, the tree is a path of height $n$.
- **Build.** The balanced build sorts once by $x$ and splits each group in linear time: $O(n \log n)$.
- **Delete.** The search costs $O(h)$, and the reinsertion costs $O(h)$ for each of the $s$ points below the node: $O(s h)$. Deleting the root of a large tree costs $\Theta(n h)$.
- **Range search.** The worst case is $\Theta(n)$ even when nothing is reported: for points on a path, a thin box can meet all regions. The cost is bounded by the number of regions that meet the box. When each child holds at most a quarter of its parent's points, a vertical or horizontal line meets at most two children of each node it meets, so it meets $O(2^{\log_4 n}) = O(\sqrt n)$ regions, and a range search costs $O(\sqrt n + r)$; but not every set has a tree with this balance.
- **Space.** One node with four pointers per point: $\Theta(n)$.

| operation | time | case |
|---|---|---|
| build | $O(n \log n)$ | worst, balanced build |
| search, insert | $O(h)$ | worst |
| delete | $O(s h)$ | worst, by reinsertion |
| range_search | $O(n)$ | worst |
| space | $\Theta(n)$ | total |

## Variants

- **k-d tree.** Splitting by one coordinate per level, in turn, gives a binary tree with the same kind of regions; Bentley's k-d tree replaced the point quadtree in most uses because it has two children per node in any dimension.
- **Higher dimensions.** The point quadtree in $k$ dimensions has $2^k$ children per node, which wastes space for $k \ge 4$.
- **Pseudo quadtree.** Split at a point that is not one of the data points, such as a median, and store the data in the leaves. This makes deletion easy and allows a balanced dynamic tree.
- **Region-based trees.** The [PR quadtree](/pr-quadtree/) splits at the centers of fixed squares, so that the shape does not depend on the insertion order; the [region quadtree](/region-quadtree/) does the same for images.

## When to use it

Use a point quadtree for points in the plane when the set is built mostly by insertions, the insertion order is not adversarial, and deletions are rare. It is simple, and each node splits in two directions at once. Use a [k-d tree](/kd-tree/) when deletions are frequent, when the dimension is above 3, or when you need worst-case range bounds. Use a [PR quadtree](/pr-quadtree/) when the shape must not depend on the order of the data.

## Pitfalls

- **Points on the cross.** A point with $q_x = p_x$ must always go to the same side. Mixing $>$ and $\ge$ between INSERT and RANGE-SEARCH loses points that lie on a line. Lines L3 and L8 use the same convention: east and north include the line.
- **Deleting like a binary search tree.** Moving one point of a subtree up to replace the deleted point does not keep (Q) for the other points in general. Use reinsertion, or Samet's method, which checks which quadrants must be rebuilt.
- **Sorted input.** Inserting points sorted on both axes makes a path, and the cost of each operation becomes linear. Shuffle the input, or use the balanced build for static data.
- **Recursion depth.** For the same reason, recursive code can overflow its stack; the implementation uses loops and explicit stacks.

## Implementations

## History

Raphael Finkel and Jon Bentley described the quad tree for composite keys in 1974, as a generalization of the binary search tree to records with two or more keys, with insertion, region search and an optimized tree built by medians. The k-d tree, by Bentley in 1975, was its binary form. Samet gave a better deletion algorithm in 1980 and collected the point quadtree and its relatives in his survey of 1984 and his books. Devroye and Laforest analyzed the depth of random point quadtrees in 1990.

## References
