---
tag: 9HY90C
kind: problem
slug: convex-polygon-intersection
name: Convex polygon intersection
aliases: [intersection-of-convex-polygons, intersection of two convex polygons]
area: geometry/intersections
level: core
summary: Compute the intersection of two convex polygons with p and q vertices, again a convex polygon; Θ(p + q) time is optimal and is reached by edge chasing or by slabs.
prereqs: [convex-polygon, half-plane-intersection, segment-intersection-point]
see_also: [chazelle-dobkin-algorithm, convex-collision-detection, separating-axis-theorem, half-plane-intersection-deque, polygon-clipping, sutherland-hodgman, rotating-calipers, convex-polyhedra-intersection]
sources:
  - paper: doi:10.1016/0146-664X(82)90023-5
    title: Joseph O'Rourke, Chi-Bin Chien, Thomas Olson and David Naddor, A new linear algorithm for intersecting convex polygons, Computer Graphics and Image Processing 19(4), 1982, 384-391
    locator: the edge-chasing algorithm with its advance rules, in O(p + q) time
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 7, Section 7.6, Intersection of convex polygons (the advance rules, the code ConvexIntersect and its degenerate cases)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 7, Section 7.2.1, Intersection of convex polygons (the slab method of Shamos and Hoey in linear time)
  - paper: doi:10.1109/SFCS.1976.16
    title: Michael Ian Shamos and Dan Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science (FOCS 1976), 208-215
    locator: the linear-time intersection of two convex polygons by slabs
  - paper: doi:10.1145/7531.24036
    title: Bernard Chazelle and David P. Dobkin, Intersection of convex objects in two and three dimensions, Journal of the ACM 34(1), 1987, 1-27
    locator: the O(log(p + q)) test of whether two convex polygons meet, and the linear lower bound for computing the boundary
---

Convex polygon intersection asks for the intersection of two convex polygons $P$ and $Q$ with $p$ and $q$ vertices. The intersection of two convex sets is convex, so the answer is a convex polygon with at most $p + q$ vertices, or a segment, a point or the empty set. It can be computed in optimal $\Theta(p + q)$ time, either by the slab method of Shamos and Hoey or by the edge-chasing algorithm of O'Rourke, Chien, Olson and Naddor (1982), which walks around both boundaries at once. To only decide whether $P$ and $Q$ meet, $O(\log(p + q))$ time is enough, by the [Chazelle-Dobkin algorithm](/chazelle-dobkin-algorithm/).

## In plain words

You have two convex shapes, such as two cut pieces of paper with straight edges and no dents, and you lay one on top of the other. Where do they overlap?

The overlap has no dents either, and its border is made of pieces of the two borders. Each time the two borders cross, the overlap's border switches from one shape to the other. A good method walks around both borders at the same time, like two people who walk around two fences and try to stay close to each other. Each step moves one of them by one edge, and the crossings show up on the way. So the work grows only with the number of edges, not with their product.

## Definition

**Input.** Two convex polygons $P = (p_0, \dots, p_{p-1})$ and $Q = (q_0, \dots, q_{q-1})$, each given by its vertices in counterclockwise order. A polygon is the closed region, boundary included.

**Output.** The region $P \cap Q$, as a list of vertices in counterclockwise order, or a mark that it is empty, a single point or a segment. Its vertices are vertices of $P$ inside $Q$, vertices of $Q$ inside $P$, and crossing points of an edge of $P$ with an edge of $Q$. So it has at most $p + q$ vertices. In general position the two boundaries cross in at most $2 \min(p, q)$ points, because a segment crosses the boundary of a convex polygon at most twice.

**Model.** The [real RAM](/real-ram/). With integer vertices, the inside tests are [orientation tests](/orientation-test/) on integers, and the crossing points are exact rationals, as computed on the [segment intersection point](/segment-intersection-point/) page.

## Variants

- **Detection.** Decide whether $P \cap Q \ne \emptyset$. For convex polygons given as arrays, this takes $O(\log(p + q))$ time ([Chazelle-Dobkin](/chazelle-dobkin-algorithm/)), and the [separating axis theorem](/separating-axis-theorem/) gives a simple $O(p + q)$ test. This is the narrow phase of [convex collision detection](/convex-collision-detection/).
- **Distance and penetration.** If the polygons do not meet, find their distance; if they do, find how deep they overlap. Both are about the [Minkowski difference](/minkowski-sum/) $P - Q$; see the [GJK algorithm](/gjk-algorithm/) and [rotating calipers](/rotating-calipers/).
- **Many convex polygons.** Intersect $m$ convex polygons with $n$ vertices in total: a [half-plane intersection](/half-plane-intersection/) of all edges in $O(n \log n)$ time, or pairwise merging in $O(n \log m)$ time.
- **Clipping by a convex window.** Clip an arbitrary polygon to a convex polygon: [Sutherland-Hodgman](/sutherland-hodgman/), in $O(p q)$ time, which for two convex polygons also gives the intersection. General polygons need the methods on the [polygon clipping](/polygon-clipping/) page.
- **Three dimensions.** Intersect two convex polyhedra: [convex polyhedra intersection](/convex-polyhedra-intersection/), also in linear time, by Chazelle (1992).

## Examples

**Square and triangle.** Let $P$ be the square $(0,0), (4,0), (4,4), (0,4)$ and $Q$ the triangle $(2,-1), (6,3), (1,5)$. Then $P \cap Q$ is the hexagon

$$(3, 0),\ (4, 1),\ (4, 19/5),\ (7/2, 4),\ (7/6, 4),\ (11/6, 0).$$

All six vertices are crossing points of the two boundaries: no vertex of $P$ is in $Q$ and no vertex of $Q$ is in $P$. Each edge of $Q$ crosses the square twice. The result agrees with the [sort-and-deque](/half-plane-intersection-deque/) code run on the seven edge half-planes.

**Touching.** The squares $[0, 4]^2$ and $[4, 7] \times [1, 3]$ meet in the segment from $(4, 1)$ to $(4, 3)$, which has zero area. An implementation must say whether such a contact is part of the output; the half-plane code on this site returns the empty list for results of zero area.

**Nested.** If $Q$ lies inside $P$, the boundaries do not cross and the answer is $Q$. An edge-chasing algorithm detects this case after it has walked around both polygons once without a crossing, and then tests one vertex of each polygon for containment.

## Known algorithms

| algorithm | time | idea |
| --- | --- | --- |
| clip by every edge ([Sutherland-Hodgman](/sutherland-hodgman/)) | $O(p q)$ | clip $P$ by the half-plane of each edge of $Q$ in turn |
| [half-plane intersection](/half-plane-intersection-deque/) of all edges | $O((p + q) \log(p + q))$, or $O(p + q)$ with a merge of the two angle orders | treat the $p + q$ edges as half-planes |
| slabs (Shamos and Hoey, 1976) | $O(p + q)$ | cut the plane by vertical lines through all vertices; in each slab both polygons are trapezoids, and their intersection is found in $O(1)$ |
| edge chasing (O'Rourke, Chien, Olson and Naddor, 1982) | $O(p + q)$ | walk both boundaries at once; advance the edge that points toward the other edge's line |
| [rotating calipers](/rotating-calipers/) (Toussaint, 1985) | $O(p + q)$ | find the pockets between the two polygons and the crossing points from the common tangents |
| [Chazelle-Dobkin](/chazelle-dobkin-algorithm/), detection only | $O(\log(p + q))$ | prune and search on the two boundaries |

The edge-chasing algorithm keeps one current edge $a$ of $P$ and one current edge $b$ of $Q$. At each step it tests whether $a$ and $b$ cross, and records the crossing; then it advances $a$ or $b$ by one edge according to whether each edge "aims at" the other, which is a sign of a cross product, and whether the head of each edge is inside the half-plane of the other. O'Rourke et al. prove that after at most $2(p + q)$ steps it has found all crossings, in order around the result. Its degenerate cases, where edges overlap or cross at vertices, need care, and O'Rourke's book lists them.

## Bounds

- **Lower bound.** Computing the boundary needs $\Omega(p + q)$ time, since the output can have $p + q$ vertices, and Chazelle and Dobkin show that even when the output is small, the boundary of the intersection needs linear time in the worst case.
- **Upper bound.** $O(p + q)$ time and space, by slabs, edge chasing or rotating calipers.
- **Detection.** $\Theta(\log(p + q))$ time for convex polygons stored as arrays, by Chazelle and Dobkin.

## Reductions

- **To half-plane intersection.** $P \cap Q$ is the intersection of the $p + q$ half-planes of their edges. Both edge lists are already sorted by angle, so a merge replaces the sort.
- **Merge step of divide and conquer.** The divide-and-conquer algorithm for [half-plane intersection](/half-plane-intersection/) uses convex polygon intersection to merge two halves, which gives $O(n \log n)$ time.
- **Minkowski difference.** $P$ and $Q$ meet if and only if the origin lies in $P - Q = P \oplus (-Q)$, a convex polygon with at most $p + q$ vertices that the [Minkowski sum of convex polygons](/minkowski-sum-convex-polygons/) builds in linear time.

## Applications

- **Collision detection.** Exact tests and contact regions between convex shapes in games and physics engines.
- **Clipping in graphics.** Clipping convex primitives to a convex view region.
- **Polygon operations.** Intersections of convex pieces after a convex decomposition of general polygons.
- **Linear programming and optimization.** Merging feasible regions given by two sets of constraints.

## References
