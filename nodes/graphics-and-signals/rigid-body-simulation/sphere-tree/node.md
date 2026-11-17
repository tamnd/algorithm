---
tag: 0FMTPB
kind: data-structure
slug: sphere-tree
name: Sphere tree
aliases:
- bounding sphere hierarchy
area: graphics-and-signals/rigid-body-simulation
level: advanced
summary: A hierarchy of spheres that cover an object, often built from the medial axis, used for fast and interruptible collision detection.
implements: [spatial-index]
model: real-ram
complexity:
  vars: {n: the number of triangles of the first object, m: the number of triangles of the second object, L: the level at which an interrupted query stops}
  time: {build_expected: O(n log^2 n), sphere_test: O(1), query: O(n m), interrupted_query: O(2^L)}
  space: {total: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1996
  people: [Philip M. Hubbard]
  note: Hubbard built sphere trees from an approximation of the medial axis and gave a breadth-first query that can stop at any level, for time-critical collision detection.
prereqs: [bounding-volume-hierarchy, minimum-enclosing-circle, welzls-algorithm]
see_also: [obb-tree, k-dop-tree, medial-axis, minimum-enclosing-ball, bounding-volume, collision-detection, hausdorff-distance, octree]
sources:
  - paper: doi:10.1145/231731.231732
    title: Philip M. Hubbard, Approximating polyhedra with spheres for time-critical collision detection, ACM Transactions on Graphics 15(3), 1996, 179 to 210
    locator: the build of sphere trees from an approximation of the medial axis, and the interruptible breadth-first collision query
  - paper: "Gareth Bradshaw and Carol O'Sullivan, Adaptive medial-axis approximation for sphere-tree construction, ACM Transactions on Graphics 23(1), 2004, 1 to 26"
    title: Gareth Bradshaw and Carol O'Sullivan, Adaptive medial-axis approximation for sphere-tree construction, ACM Transactions on Graphics 23(1), 2004, 1 to 26
    locator: the build of tighter sphere trees from an adaptive approximation of the medial axis
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: the chapters on bounding volumes (spheres) and on bounding volume hierarchies
---

A sphere tree is a [bounding volume hierarchy](/bounding-volume-hierarchy/) whose volumes are spheres. Each node stores a sphere that holds the part of the object below it. Two spheres overlap exactly when the distance between their centers is at most the sum of their radii, so the test is the cheapest of all volumes. A sphere does not change when the object turns, so a moving object moves only the centers. The fit is poor for long or flat parts. Hubbard built sphere trees from an approximation of the [medial axis](/medial-axis/), so that the spheres of each level follow the shape. He used them for time-critical [collision detection](/collision-detection/): the query goes down the trees one level at a time and can stop at any level, and the overlapping spheres at that level are an approximate answer.

## In plain words

Cover the object with one large ball. Then cover each half of the object with a smaller ball, then each quarter, and so on, until each ball holds one small piece. Two objects can touch only where their balls touch, and to check whether two balls touch you compare one distance with the sum of two radii.

A program that must answer on time, like a game or a simulator, can go down the two trees one level at a time and stop when its time is up. The balls that still touch at that level are its best guess. With more time, the guess gets finer.

## The abstract type

A sphere tree is a static [spatial index](/spatial-index/) over the $n$ triangles of one rigid object. The operations are:

- BUILD$(T)$: make the tree for the triangle set $T$.
- OVERLAP$(A, B, g, L)$: when $B$ is placed by the rigid motion $g(x) = Rx + t$ in the frame of $A$, the pairs of a triangle of $A$ and a triangle of $B$ that meet and that the query resolved, and the pairs of nodes whose spheres still overlap when the query stops at the level $L$.

With no limit, the second list is empty and the first one is the exact answer. The tree does not support insert or delete.

## Representation

A node stores a center $c$ and a radius $r$. An inner node has two children, and a leaf holds one triangle. The invariant is:

- **(B) Bounds.** The sphere of each node contains every triangle below it.

The code is in the plane, with circles. It fits each node with the smallest circle that holds the vertices below it, by [Welzl's algorithm](/welzls-algorithm/) with a fixed seed, and it splits the triangles at the median along the wider spread of their centroids. This top-down build is the code's choice, because it is short and it keeps (B) by construction. Hubbard instead built the spheres of each level from the medial axis of the object, and Bradshaw and O'Sullivan made this fit tighter.

## Operations

```pseudo id=main
BUILD(T)                                    ▷ T: triangles; one per leaf
L1  (c, r) ← the smallest circle that holds the vertices of T
L2  if |T| = 1 then return a leaf with (c, r)
L3  a ← the coordinate axis with the wider spread of the triangle centroids
L4  sort T along a; return a node with (c, r) and the children BUILD(first half), BUILD(second half)
```

```pseudo id=query
OVERLAP(A, B, R, t, L)                      ▷ B placed by x → R x + t
L5  the moved center of a node b of B is R c(b) + t; its radius stays r(b)
L6  frontier ← [(root(A), root(B))]; for the levels 0, 1, 2, ... while the frontier is not empty
L7      for each pair (a, b) in the frontier: if dist(c(a), R c(b) + t) > r(a) + r(b) then skip it
L8      if a and b are leaves then if their triangles meet, report the pair
L9      else if this level is L then add (a, b) to the possible pairs
L10     else put (left(a), b), (right(a), b) in the next frontier if a has the larger sphere and is not a leaf; else (a, left(b)), (a, right(b))
```

The query is breadth first, so it refines all overlapping pairs of one level before it goes to the next. This is what makes it interruptible. A depth-first query that stops early would have resolved a few pairs to the leaves and left the others at the roots.

## Example

Take an object of 4 triangles in a row, $(2k, 0), (2k + 1.5, 0), (2k + 0.5, 1)$ for $k = 0, \dots, 3$. The root circle has the center $(3.75, 0)$ and the radius $3.75$, with the vertices $(0, 0)$ and $(7.5, 0)$ on a diameter. The two inner circles have the centers $(1.75, 0)$ and $(5.75, 0)$ and the radius $1.75$. Each leaf circle has the radius $\sqrt{0.625} \approx 0.79$. Let $B$ be a copy turned by $90°$ and moved by $t = (7, 0.5)$, so that the first triangle of $B$ stands on the last triangle of $A$.

| level limit | circle tests | reported pairs | possible pairs (triangles of a, triangles of b) |
|---|---|---|---|
| 0 | 1 | none | (0 to 3, 0 to 3) |
| 1 | 3 | none | (2 and 3, 0 to 3) |
| 2 | 5 | none | (2 and 3, 0 and 1) |
| 3 | 7 | none | (3, 0 and 1) |
| none | 9 | (3, 0) | none |

Each row narrows the possible contact, and the full query finds the pair $(3, 0)$, like the brute-force method over all 16 pairs. On random scenes of $n = m = 256$ small triangles, with the two objects on top of each other, the full query did between 1209 and 1655 circle tests in 3 trials. A query stopped at the level 8 did between 131 and 169 tests and returned between 28 and 39 possible pairs.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). A disk is convex, so a circle that holds the vertices below a node holds its triangles, and (B) holds for any circle that holds the vertices, even one that is not the smallest. A rigid motion maps a disk to the disk with the moved center and the same radius, so the moved spheres of $B$ hold the moved triangles. If two triangles meet at a point $x$, every pair of their ancestors has two spheres that hold $x$, so the query never prunes such a pair. It either reaches the two leaves and reports the pair, or it stops at the level limit with an ancestor pair in the possible list. So the stopped query never misses a contact, and the full query is exact.

## Complexity

The model is the [real RAM](/real-ram/). Welzl's algorithm takes expected linear time over the random order, so each level of the build costs expected $O(n)$ for the circles and $O(n \log n)$ for the sort, over $O(\log n)$ levels.

| operation | time | case |
|---|---|---|
| build | $O(n \log^2 n)$ | expected over the shuffle |
| sphere test | $O(1)$ | one distance and one sum |
| full query | $O(n m)$ | worst; far fewer tests on typical scenes, as measured above |
| query stopped at the level $L$ | $O(2^L)$ | each level at most doubles the frontier |
| space | $\Theta(n)$ | $2n - 1$ nodes |

The bound $O(2^L)$ does not depend on the size of the objects, so the time of a stopped query is known in advance. This is the point of the time-critical query.

## Variants

- **Medial-axis builds.** Hubbard placed spheres on an approximation of the medial axis, found from the Voronoi diagram of points on the surface, and merged them into the spheres of the higher levels. Bradshaw and O'Sullivan refined the approximation where the fit was poor. These trees follow the shape closely, but they cost much more to build.
- **Octree builds.** A simpler build puts a sphere around each occupied cell of an [octree](/octree/) of the object. It is fast and loose.
- **Fit measures.** A tight tree keeps the spheres from sticking far out of the object. The [Hausdorff distance](/hausdorff-distance/) between the union of the spheres of a level and the object is a natural measure of this error.
- **Other volumes.** [OBB trees](/obb-tree/) and [k-DOP trees](/k-dop-tree/) fit better but cost more to test or to update. Swept sphere volumes add a radius to a segment or a rectangle, and they keep the cheap test for long parts.
- **Deformable objects.** Each sphere can be refitted from the vertices below it, or grown to hold its two child spheres, which is fast but loose.

## When to use it

Use a sphere tree when the test must be cheap, when objects turn often, or when the query must meet a time limit, as in interactive simulation, games and haptics. The level limit gives a direct trade between time and accuracy. For exact contacts between long, flat or tightly fitting parts, an [OBB tree](/obb-tree/) usually needs far fewer tests.

## Pitfalls

- **Loose spheres.** A sphere around a thin rod or a flat plate is mostly empty. On such objects a sphere tree reports many false overlaps and goes deep before it prunes.
- **A stopped query is not a contact.** The possible pairs at the level limit are only overlapping spheres. They can be far from a true contact. Treat them as an approximation and pass them to a response that accepts this.
- **A sphere that does not hold its part.** In a medial-axis build, a child sphere need not be inside its parent. This is fine, but the query is safe only if each sphere holds all the geometry below it. Check this invariant after the build.
- **Rounding.** Grow the radii by a small margin, as in the code, so that a contact on a circle is not lost.
- **A bad seed.** Welzl's algorithm is randomized. The circle does not depend on the seed, but the time is cubic in the worst order. Shuffle the points.

## Implementations

## History

Hubbard (1996) built sphere trees from an approximation of the medial axis and gave the breadth-first, interruptible query, for collision detection that must meet a time limit. Bradshaw and O'Sullivan (2004) gave an adaptive approximation of the medial axis that builds tighter sphere trees. The smallest enclosing circle that the code uses is due to Welzl (1991).

## References
