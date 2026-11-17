---
tag: ZJ32AH
kind: data-structure
slug: k-dop-tree
name: k-DOP tree
aliases:
- discrete oriented polytope hierarchy
area: graphics-and-signals/rigid-body-simulation
level: advanced
summary: A bounding volume hierarchy whose volumes are intersections of k fixed slabs, so that an overlap test compares k/2 pairs of intervals.
implements: [spatial-index]
model: real-ram
complexity:
  vars: {n: the number of triangles of the first object, m: the number of triangles of the second object, k: the number of bounding directions with their opposites}
  time: {build: O(n log^2 n + k n log n), dop_test: O(k), moved_dop: O(k^2), query: O(k n m + k^2 m)}
  space: {total: Θ(k n)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1998
  people: [James T. Klosowski, Martin Held, Joseph S. B. Mitchell, Henry Sowizral, Karel Zikan]
  note: Klosowski and others built hierarchies of k-DOPs for collision detection of a flying object in a static scene, with a new k-DOP for the moving tree after each turn.
prereqs: [bounding-volume-hierarchy, axis-aligned-bounding-box, separating-axis-theorem]
see_also: [obb-tree, sphere-tree, bounding-volume, bvh-refitting, collision-detection, hill-climbing, convex-hull, sweep-and-prune]
sources:
  - paper: doi:10.1109/2945.675649
    title: James T. Klosowski, Martin Held, Joseph S. B. Mitchell, Henry Sowizral and Karel Zikan, Efficient collision detection using bounding volume hierarchies of k-DOPs, IEEE Transactions on Visualization and Computer Graphics 4(1), 1998, 21 to 36
    locator: the definition of k-DOPs, the interval overlap test, and the update of the k-DOPs of the flying object by hill climbing at the root and by the k-DOP of the rotated k-DOP below it
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: the chapters on bounding volumes (discrete oriented polytopes) and on bounding volume hierarchies
---

A k-DOP tree is a [bounding volume hierarchy](/bounding-volume-hierarchy/) whose volumes are discrete oriented polytopes. A k-DOP is the intersection of $k/2$ slabs whose normals come from a fixed set of directions, the same for every node. It is stored as $k/2$ intervals, one for each direction. An [axis-aligned box](/axis-aligned-bounding-box/) is the 4-DOP in 2D and the 6-DOP in 3D. More directions give a tighter fit, and the overlap test of two k-DOPs still compares $k/2$ pairs of intervals. When an object turns, its k-DOPs are no longer aligned with the fixed directions, so the query computes a new k-DOP that contains each moved volume. The k-DOP tree is a middle phase of [collision detection](/collision-detection/) between triangle meshes.

## In plain words

An upright box around a part is easy to test, but it often holds a lot of empty space. A k-DOP cuts off the corners of the box with more flat sides, at a few fixed angles that every part uses. In the plane, the 8-DOP uses the two axes and the two diagonals.

Because every part uses the same angles, two parts are compared by checking, for each angle, whether their two ranges overlap. If one range pair is apart, the parts are apart. When an object turns, its shapes no longer match the fixed angles, so each one gets a new, slightly larger shape that holds it.

## The abstract type

A k-DOP tree is a static [spatial index](/spatial-index/) over the $n$ triangles of one object. The operations are:

- BUILD$(T)$: make the tree for the triangle set $T$.
- OVERLAP$(A, B, g)$: the pairs of a triangle of $A$ and a triangle of $B$ that meet, when $B$ is placed by the rigid motion $g(x) = Rx + t$ in the frame of $A$.

As in the paper of Klosowski and others, $A$ is a static scene and $B$ is a flying object. The tree of $A$ never changes. The tree of $B$ keeps its shape, and the query computes the moved volumes of its nodes as they are needed. A deformable mesh needs a [refit](/bvh-refitting/), which for a k-DOP is a pass over the vertices with $k/2$ dot products each.

## Representation

Fix $k/2$ directions $d_1, \dots, d_{k/2}$. The code uses the 8-DOP in the plane, with the directions $(1, 0)$, $(0, 1)$, $(1, 1)$ and $(1, -1)$. A node stores the intervals $[\ell_j, h_j]$ with $\ell_j = \min_p d_j \cdot p$ and $h_j = \max_p d_j \cdot p$ over the vertices $p$ below it, so its volume is $\{x : \ell_j \le d_j \cdot x \le h_j \text{ for all } j\}$. An inner node has two children, and a leaf holds one triangle. The invariant is:

- **(B) Bounds.** The k-DOP of each node contains every triangle below it.

In 3D, common choices are $k = 6$ (the box), $k = 14$ (the box with its 8 corners cut), $k = 18$ (the box with its 12 edges cut) and $k = 26$ (both). Klosowski and others studied these sizes.

## Operations

```pseudo id=main
BUILD(T)                                    ▷ T: triangles; one per leaf
L1  D ← for each direction d_j, the range of d_j · p over the vertices p of T
L2  if |T| = 1 then return a leaf with D
L3  d ← the direction with the widest spread of the triangle centroids
L4  sort T by d · centroid; return a node with D and the children BUILD(first half), BUILD(second half)
```

```pseudo id=overlap
OVERLAP(A, B, R, t)                         ▷ B placed by x → R x + t
L5  at the root of B: D ← the k-DOP of the moved vertices of B
L6  at the other nodes b of B: D ← the k-DOP of the moved corners of the stored k-DOP of b
L7  stack ← [(root(A), root(B))]; pop (a, b) while the stack is not empty
L8      if some interval of a is apart from the same interval of the moved k-DOP of b then continue
L9      if a and b are leaves then if their triangles meet, report the pair; continue
L10     if b is a leaf, or a is not a leaf and holds at least as many triangles, push (left(a), b), (right(a), b); else push (a, left(b)), (a, right(b))
```

Line L5 is exact. The paper finds the extreme vertices by [hill climbing](/hill-climbing/) on the convex hull of the object, and the code scans all vertices. Line L6 is cheaper and looser: it moves the corners of the stored k-DOP, which is a convex polygon that holds the triangles, and takes the k-DOP of the moved corners. The code finds the corners by clipping the box with the two diagonal slabs. Both volumes contain the moved triangles, so the query stays exact.

## Example

The triangle $(0, 0), (4, 0), (0, 4)$ has the 8-DOP with $x \in [0, 4]$, $y \in [0, 4]$, $x + y \in [0, 4]$ and $x - y \in [-4, 4]$, which is the triangle itself. The square $[3, 5] \times [3, 5]$ meets the box $[0, 4] \times [0, 4]$ of the triangle, so the box test reports an overlap. The 8-DOP test finds $x + y \ge 6$ on the square and $x + y \le 4$ on the triangle, so it separates them.

For a query, take an object of 4 triangles in a row, $(2k, 0), (2k + 1.5, 0), (2k + 0.5, 1)$ for $k = 0, \dots, 3$. The root has $x \in [0, 7.5]$, $y \in [0, 1]$, $x + y \in [0, 7.5]$ and $x - y \in [-0.5, 7.5]$. Its corners are $(0, 0), (7.5, 0), (6.5, 1), (0.5, 1), (0, 0.5)$. If the object turns by $30°$, the k-DOP of the moved corners has $x \ge -0.25$, from the moved corner $(0, 0.5)$, but the exact k-DOP of the moved vertices has $x \ge -0.067$, from the moved vertex $(0.5, 1)$. This is the price of line L6. Let $B$ be a copy turned by $90°$ and moved by $t = (7, 0.5)$, so that the first triangle of $B$ stands on the last triangle of $A$. The query does 9 tests of two 8-DOPs and 1 triangle test, and it reports the pair $(3, 0)$, like the brute-force method over all 16 pairs. With $t = (20, 0)$, the test at the roots separates the objects. On random scenes of $n = m = 256$ small triangles, with the two objects on top of each other, the query did between 757 and 1969 tests of two 8-DOPs in 5 trials, against 65536 pairs for the brute-force method. An [OBB tree](/obb-tree/) on the same scenes did between 641 and 1619 box tests, each one more costly.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Each interval is the range of the projections of the vertices below the node, so the convex k-DOP contains these vertices and their triangles, and (B) holds. A stored k-DOP is the convex hull of its corners, and a rigid motion maps it to the hull of the moved corners, so the k-DOP of the moved corners contains the moved triangles. If two triangles meet at a point $x$, every pair of their ancestors has two volumes that contain $x$, so all intervals overlap and the traversal reaches the two leaves, where the exact triangle test reports the pair. In the plane the edges of an 8-DOP have normals among the 4 directions, so by the [separating axis theorem](/separating-axis-theorem/) the interval test is exact. In 3D the test is only conservative, which costs extra tests but not correctness. Each pair of nodes is visited at most once, so the query stops after at most $(2n - 1)(2m - 1)$ tests.

## Complexity

The model is the [real RAM](/real-ram/). A k-DOP of $s$ vertices costs $O(k s)$. Each level of the build fits all its nodes in $O(k n)$ and sorts in $O(n \log n)$, and the median split gives $O(\log n)$ levels. A k-DOP has $O(k)$ corners, so a moved k-DOP costs $O(k^2)$, once for each node of $B$.

| operation | time | case |
|---|---|---|
| build | $O(n \log^2 n + k n \log n)$ | median splits |
| test of two k-DOPs | $O(k)$ | $k/2$ interval pairs |
| moved k-DOP | $O(k^2)$ | from the $O(k)$ corners |
| overlap | $O(k n m + k^2 m)$ | worst; far fewer tests on typical scenes, as measured above |
| space | $\Theta(k n)$ | $2n - 1$ nodes of $k$ numbers |

The worst case of the query is real, since two objects can have $\Theta(n m)$ pairs of triangles that meet.

## Variants

- **The number of directions.** More directions give a tighter fit and fewer tests, but each test and each update costs more. The best $k$ depends on the scene.
- **The update of a turning object.** Line L6 can be replaced by an exact refit of the moved vertices of each node, which is tighter and costs a pass over the vertices, or by hill climbing on the hull of each node.
- **Other volumes.** [Sphere trees](/sphere-tree/) need no update when the object turns, but fit poorly. [OBB trees](/obb-tree/) fit long and tilted parts best and turn with the object, but their test is the most costly.
- **A broad phase.** The 4-DOP or 6-DOP of each object is the axis-aligned box that [sweep and prune](/sweep-and-prune/) sorts. More directions give more axes to sort.

## When to use it

Use a k-DOP tree for collision detection between a moving object and a large static scene, for example a tool path through a machine or a virtual object in a walk-through. The static tree is built once, the interval test is cheap and simple, and the fit is better than that of a box tree for surfaces at an angle. For two objects that both turn and are in close contact, an [OBB tree](/obb-tree/) can need fewer tests. For deformable meshes, an [AABB tree](/axis-aligned-bounding-box/) with a [refit](/bvh-refitting/) is simpler.

## Pitfalls

- **Comparing different frames.** The interval test works only for two k-DOPs with the same directions in the same frame. Testing the stored k-DOP of a turned object without the update gives wrong results.
- **A false claim of exactness.** In 3D, two disjoint k-DOPs can have all their intervals overlap, so a test that says overlap must not be taken as a contact.
- **Loose updates.** Each update of line L6 adds empty space, and the error does not grow with depth only because each node is updated from its own stored k-DOP. Updating a child from the moved volume of its parent would make the volumes grow larger at each level.
- **Corners of a degenerate k-DOP.** A flat or point-like k-DOP has repeated corners. The clip must handle them, or the update must start from the vertices.
- **Rounding.** Grow the intervals by a small margin, as in the code, so that a contact on the boundary of a volume is not lost.

## Implementations

## History

Kay and Kajiya (1986) bounded objects by sets of parallel slabs to speed up ray tracing. Klosowski, Held, Mitchell, Sowizral and Zikan (1998) built hierarchies of k-DOPs for collision detection of a flying object in a static scene, studied several values of $k$, and gave the two-level update of the moving tree. They compared their trees with the [OBB tree](/obb-tree/) of Gottschalk, Lin and Manocha.

## References
