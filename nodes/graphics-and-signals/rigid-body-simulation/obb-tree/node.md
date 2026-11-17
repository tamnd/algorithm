---
tag: FZV7G9
kind: data-structure
slug: obb-tree
name: OBB tree
aliases:
- OBBTree
- oriented bounding box tree
area: graphics-and-signals/rigid-body-simulation
level: core
summary: A bounding volume hierarchy of tight oriented boxes fitted by principal axes, tested for overlap with the separating axis test on 15 axes.
implements: [spatial-index]
model: real-ram
complexity:
  vars: {n: the number of triangles of the first object, m: the number of triangles of the second object}
  time: {build_balanced: O(n log^2 n), build_worst: O(n^2 log n), box_test: O(1), query: O(n m)}
  space: {total: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1996
  people: [Stefan Gottschalk, Ming C. Lin, Dinesh Manocha]
  note: Gottschalk, Lin and Manocha fitted boxes by the covariance of the convex hull, built the tree top down, and gave the overlap test of two boxes on 15 separating axes, in the OBBTree system.
prereqs: [bounding-volume-hierarchy, separating-axis-theorem, principal-component-analysis, convex-hull]
see_also: [k-dop-tree, sphere-tree, axis-aligned-bounding-box, bounding-volume, bvh-refitting, collision-detection, covariance-matrix, rotating-calipers]
sources:
  - paper: doi:10.1145/237170.237244
    title: Stefan Gottschalk, Ming C. Lin and Dinesh Manocha, OBBTree, a hierarchical structure for rapid interference detection, SIGGRAPH 1996, 171 to 180
    locator: the fit of a box by the covariance of the hull triangles, the top-down build, and the separating axis test on 15 axes
  - paper: doi:10.1109/2945.675649
    title: James T. Klosowski, Martin Held, Joseph S. B. Mitchell, Henry Sowizral and Karel Zikan, Efficient collision detection using bounding volume hierarchies of k-DOPs, IEEE Transactions on Visualization and Computer Graphics 4(1), 1998, 21 to 36
    locator: the comparison of hierarchies of k-DOPs with the OBB tree
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: the chapters on bounding volumes (oriented boxes) and on bounding volume hierarchies
---

An OBB tree is a [bounding volume hierarchy](/bounding-volume-hierarchy/) whose volumes are oriented bounding boxes. Each node stores a box that can turn freely, with its axes along the principal directions of the geometry below it. For long, thin or tilted parts, such a box fits much tighter than an [axis-aligned box](/axis-aligned-bounding-box/) or a sphere. Two boxes are tested for overlap by the [separating axis test](/separating-axis-theorem/), on 15 axes in 3D and on 4 axes in 2D. A rigid object keeps its tree in its own frame, and the query moves the boxes of one tree into the frame of the other, so the tree is never rebuilt while the object moves. The OBB tree is the broad and middle phase of exact [collision detection](/collision-detection/) between two rigid triangle meshes.

## In plain words

To find where two complex objects touch, you put the object in a box, split it into two halves with their own boxes, and go on until each box holds one triangle. Two objects can touch only where their boxes touch, so you skip all the pairs of parts whose boxes are apart.

The trick of the OBB tree is that each box turns to fit its part. A thin rod that lies at an angle gets a thin box at the same angle, not a large square box with mostly empty space. Tight boxes give fewer false alarms when two objects are close. A test of two turned boxes costs more than a test of two upright ones, but you need far fewer of them.

## The abstract type

An OBB tree is a static [spatial index](/spatial-index/) over the $n$ triangles of one rigid object. The operations are:

- BUILD$(T)$: make the tree for the triangle set $T$.
- OVERLAP$(A, B, g)$: the pairs of a triangle of $A$ and a triangle of $B$ that meet, when $B$ is placed by the rigid motion $g(x) = Rx + t$ in the frame of $A$.

A query for the first contact only, or for all pairs closer than a distance, uses the same traversal with a different test at the leaves. The tree does not support insert or delete. A deformable mesh needs a refit or a rebuild, which is costly for oriented boxes.

## Representation

A node stores a box with a center $c$, a unit axis $u$, the second axis $u^\perp$, and the half extents $h_1, h_2$. In 3D it stores three axes and three half extents. An inner node has two children. A leaf holds one triangle. The invariant is:

- **(B) Bounds.** The box of each node contains every triangle below it.

The build fits the box of a node in two steps. First it chooses the axes as the eigenvectors of the covariance of the convex hull of the vertices below the node. Gottschalk, Lin and Manocha use the hull triangles with a uniform density over their area. The 2D code here uses the hull edges with a uniform density over their length. The hull makes the fit depend on the shape and not on how densely it is sampled. Then it projects all the vertices on the axes and takes the smallest and the largest value on each axis. The axes affect only the tightness of the box. Any axes give a valid box, because the box is the range of the projections.

## Operations

```pseudo id=main
BUILD(T)                                    ▷ T: triangles; one per leaf
L1  H ← the convex hull of the vertices of T
L2  u ← the principal axis of the covariance of the boundary of H
L3  box ← the range of the projections of the vertices on u and on u⊥
L4  if |T| = 1 then return a leaf with box
L5  a ← the longer axis of box; s ← the mean of the projections of the triangle centroids on a
L6  T1, T2 ← the triangles with a centroid below and above s; if one is empty, split at the median
L7  return a node with box and the children BUILD(T1), BUILD(T2)
```

The paper cuts along the longest axis of the box. The code cuts at the mean of the centroids, and falls back to the median when all centroids are on one side, so that each child gets at least one triangle.

```pseudo id=overlap
OVERLAP(A, B, R, t)                         ▷ B placed by x → R x + t
L8  stack ← [(root(A), root(B))]; pop (a, b) while the stack is not empty
L9      if the separating axis test finds an axis between box(a) and R box(b) + t then continue
L10     if a and b are leaves then if their triangles meet, report the pair; continue
L11     if b is a leaf, or a is not a leaf and box(a) is at least as large, push (left(a), b), (right(a), b); else push (a, left(b)), (a, right(b))
```

Line L9 moves the box of $b$: its center goes to $Rc + t$ and its axes to $Ru$, and the half extents stay the same. In 2D, for the boxes $P$ and $Q$ and each of the 4 axes $L$ of the two boxes, the test compares $|L \cdot (c_Q - c_P)|$ with $\sum_k h^P_k |L \cdot u^P_k| + \sum_k h^Q_k |L \cdot u^Q_k|$. In 3D the axes are the 3 face normals of each box and the 9 cross products of an axis of one box with an axis of the other. Gottschalk, Lin and Manocha compute the test in the frame of one box, so that many terms are simple.

## Example

Take a $4 \times 1$ rectangle turned by $30°$, given by 6 points on its boundary. The axis-aligned box of the points is $(2\sqrt{3} + 1/2) \times (2 + \sqrt{3}/2) \approx 3.964 \times 2.866$, with the area $11.36$. The covariance of the hull boundary has its main eigenvector at $30°$, and the fitted box is the rectangle itself, with the area 4. So the oriented box covers less than half the area of the upright box.

For a query, take an object of 4 triangles in a row, $(2k, 0), (2k + 1.5, 0), (2k + 0.5, 1)$ for $k = 0, \dots, 3$. Its tree has a root with the 4 triangles, two inner nodes with 2 triangles each, and 4 leaves. Let $B$ be a copy turned by $90°$ and moved by $t = (7, 0.5)$, so that the first triangle of $B$ stands on the last triangle of $A$. The query does 9 box tests and 1 triangle test, and it reports the pair $(3, 0)$. The brute-force method tests all 16 pairs of triangles and finds the same pair. With $t = (20, 0)$, the first box test at the roots separates the objects, and the query stops. On random scenes of $n = m = 256$ small triangles at a fixed density, with the two objects placed on top of each other, the query did between 641 and 1619 box tests in 5 trials, against $65536$ pairs for the brute-force method, and reported between 14 and 45 pairs.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The box of a node is the range of the projections of all vertices below it, so (B) holds for any choice of axes. A rigid motion keeps containment, so the moved box of a node of $B$ still contains its moved triangles. In the plane, two disjoint convex polygons have a separating line parallel to one of their edges, so the 4 box axes give an exact overlap test. If two triangles meet at a point $x$, then every pair of their ancestors has two boxes that contain $x$. So the traversal never prunes such a pair and reaches the two leaves, where the exact triangle test reports the pair. Each pair of nodes is visited at most once, so the query stops after at most $(2n - 1)(2m - 1)$ box tests.

## Complexity

The model is the [real RAM](/real-ram/). A node with $k$ triangles costs $O(k \log k)$ for the hull and $O(k)$ for the covariance, the projections and the split. A 3D fit also needs the eigenvectors of a $3 \times 3$ symmetric matrix, for example by the [Jacobi method](/jacobi-eigenvalue-algorithm/), in $O(1)$.

| operation | time | case |
|---|---|---|
| build | $O(n \log^2 n)$ | when the splits are balanced |
| build | $O(n^2 \log n)$ | worst, when each split takes off one triangle |
| box test | $O(1)$ | 4 axes in 2D, 15 in 3D |
| overlap | $O(n m)$ | worst; far fewer tests on typical scenes, as measured above |
| space | $\Theta(n)$ | $2n - 1$ nodes |

The worst case of the query is real: two objects can be placed so that $\Theta(n m)$ pairs of triangles meet, and then any method that reports all pairs needs that many steps. The cost on objects in close contact, where many boxes overlap but few triangles meet, depends on the fit, and this is where tight boxes pay off.

## Variants

- **The fit.** The covariance of the vertices is cheaper but depends on the sampling of the mesh. The covariance of the hull triangles, as in the paper, does not. In 2D the smallest box has one side on an edge of the hull, so trying each hull edge with [rotating calipers](/rotating-calipers/) gives the optimal box in linear time after the hull. In 3D the smallest box is much harder to find.
- **Other volumes.** [Sphere trees](/sphere-tree/) have the cheapest test and a poor fit. [k-DOP trees](/k-dop-tree/) have fixed directions, so their test compares intervals only, but they must be refitted when the object turns. Swept sphere volumes add a radius to a rectangle or a segment, and test the distance between their cores.
- **The descent rule.** Line L11 splits the larger box. Other rules split the node with more triangles, or both nodes at once.
- **Distance queries.** The same tree with a lower bound on the distance between two boxes answers the distance of two objects, and the closest pair is found by pruning pairs of boxes that are farther than the best distance so far.

## When to use it

Use an OBB tree for exact collision detection between rigid triangle meshes, in particular when the objects are often close or in contact along a large area, for example parts in an assembly, a robot near an obstacle or a haptic probe on a surface. Then many pairs of loose boxes overlap, and the tight fit of oriented boxes saves many tests. For deformable meshes, or for scenes where the objects are mostly far apart, an [AABB](/axis-aligned-bounding-box/) tree is cheaper to build and to [refit](/bvh-refitting/). For a quick broad phase over many objects, use [sweep and prune](/sweep-and-prune/) first.

## Pitfalls

- **A box from the wrong covariance.** The covariance of the vertices, and not of the hull, gives a bad axis for a mesh with a dense cluster of small triangles on one side.
- **Equal eigenvalues.** For a square or a regular polygon, the covariance is a multiple of the identity, and the eigenvectors are arbitrary. The box is still valid, but it can be loose. Some implementations try a few axes and keep the smallest box.
- **Rounding.** The box test in floating point can miss a contact on the boundary of a box. Grow the boxes by a small margin, as in the code, or compute the test with a small tolerance.
- **The cost of the 3D test.** The 15-axis test costs much more than an AABB test. An early exit on the first separating axis helps, and the order of the axes matters.
- **Deformation.** When the mesh deforms, the boxes must be fitted again from the vertices. A refit that keeps the old axes is valid but grows loose.

## Implementations

## History

Gottschalk, Lin and Manocha (1996) gave a fast overlap test of two oriented boxes on 15 separating axes and a top-down build with boxes fitted by the covariance of the convex hull. Their RAPID library implements the method for exact interference tests between rigid triangle meshes. Klosowski and others (1998) compared it with hierarchies of k-DOPs, which have a cheaper test and a looser fit.

## References
