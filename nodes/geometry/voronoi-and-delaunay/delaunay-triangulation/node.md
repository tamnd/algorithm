---
tag: SGPK44
kind: data-structure
slug: delaunay-triangulation
name: Delaunay triangulation
aliases:
- Delone triangulation
- Delaunay tessellation
- DT
area: geometry/voronoi-and-delaunay
level: intro
summary: Triangulation of a point set in which no point lies strictly inside any triangle's circumcircle.
model: real-ram
complexity:
  vars: {n: the number of points}
  time: {expected: O(n log n), worst: O(n^3)}
  space: {expected: O(n), worst: O(n^2)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [triangulation-of-point-set, circumcircle, in-circle-test, orientation-test]
see_also: [voronoi-diagram, voronoi-delaunay-duality, delaunay-max-min-angle, bowyer-watson-algorithm, lawson-flip-algorithm, guibas-stolfi-algorithm, randomized-incremental-construction, euclidean-minimum-spanning-tree]
sources:
  - paper: "B. Delaunay, Sur la sphère vide, Bulletin de l'Académie des Sciences de l'URSS, Classe des sciences mathématiques et naturelles 6, 1934, 793-800"
    locator: the empty sphere criterion and the existence of the triangulation
  - paper: doi:10.1007/BF01758770
    title: L. J. Guibas, D. E. Knuth and M. Sharir, Randomized incremental construction of Delaunay and Voronoi diagrams, Algorithmica 7, 1992, 381-413
    locator: the insertion by flips, the history DAG for point location and the expected O(n log n) bound
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 9 (triangulations, legal edges, the randomized incremental algorithm with the history DAG, and its analysis)
  - paper: doi:10.2307/2412323
    title: K. R. Gabriel and R. R. Sokal, A new statistical approach to geographic variation analysis, Systematic Zoology 18(3), 1969, 259-278
    locator: the definition of the Gabriel graph
  - paper: doi:10.1016/0031-3203(80)90066-7
    title: G. T. Toussaint, The relative neighbourhood graph of a finite planar set, Pattern Recognition 12(4), 1980, 261-268
    locator: the relative neighbourhood graph, and the chain from the minimum spanning tree to the Delaunay triangulation
  - paper: doi:10.1109/SFCS.1975.8
    title: M. I. Shamos and D. Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975, 151-162
    locator: the Voronoi diagram and its dual in O(n log n) time, and its use for the closest pair, all nearest neighbours and the Euclidean minimum spanning tree
---

The Delaunay triangulation of a finite set $P$ of points in the plane is a [triangulation](/triangulation-of-point-set/) of $P$ in which no point of $P$ lies strictly inside the [circumcircle](/circumcircle/) of any triangle. It exists for every point set that is not on one line, and it is unique when no four points lie on a circle. It is the dual of the [Voronoi diagram](/voronoi-diagram/), it maximizes the smallest angle over all triangulations of $P$ ([max-min angle property](/delaunay-max-min-angle/)), and it holds the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/), the [relative neighbourhood graph](/relative-neighborhood-graph/) and the [Gabriel graph](/gabriel-graph/). This page gives the structure under insertion of Guibas, Knuth and Sharir: each point is located with a history DAG and inserted with edge flips, in $O(n \log n)$ expected time for $n$ points in random order.

## In plain words

Join a set of dots into triangles so that no dot is inside the circle through the three corners of any triangle. This is the Delaunay triangulation. Its triangles are as fat as possible, and it joins each dot to its natural neighbours, the dots that are near it in some direction.

To build it one dot at a time, first find the triangle that the new dot falls into. Cut that triangle into three, with the new dot as a common corner. Some old neighbours may now have the new dot inside their circle. Fix each one with a swap of the shared side, and check the next neighbours, until no circle holds the new dot.

To find the triangle quickly, keep every old triangle and a pointer from it to the triangles that replaced it. A search starts at the first triangle and follows these pointers down.

## The abstract type

The structure holds a set of points with integer coordinates.

- `insert(q)`: add the point $q$ and keep the Delaunay property. Return False if $q$ is already a vertex.
- `triangles()`: the triangles, each as a counterclockwise triple of points.
- `find_triangle(q)`: a closed triangle that holds $q$, or nothing when $q$ is outside the convex hull.

**Notation.** $P$ is the set of points, $n = |P|$, and $h$ is the number of points on the boundary of the convex hull, the points inside a hull side included. A point is $p = (x, y)$. $\mathrm{orient}(p, q, r)$ is positive when $p, q, r$ turn counterclockwise. $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $abc$, is positive when $d$ is strictly inside the circle through $a, b, c$, zero on it and negative outside; see the [in-circle test](/in-circle-test/). Both are exact integer determinants.

**Facts.** Let $P$ be finite and not on one line.

1. **Counts.** Every triangulation of $P$, Delaunay or not, has $2n - 2 - h$ triangles and $3n - 3 - h$ edges. With $h \ge 3$, there are at most $2n - 5$ triangles and $3n - 6$ edges. (Euler's formula, and the angle sum: the triangle angles add up to $(n - h) 2\pi + (h - 2)\pi$.)
2. **Existence and uniqueness.** A Delaunay triangulation exists, and all of them have the same strongly Delaunay edges, the pairs $pq$ with a circle through $p$ and $q$ that has every other point strictly outside. With no four points on a circle it is unique; see [uniqueness](/delaunay-triangulation-uniqueness/). For points on a common empty circle, as in a grid, any triangulation of their convex polygon gives a Delaunay triangulation.
3. **Local test.** A triangulation is Delaunay exactly when every interior edge is locally Delaunay: the vertex opposite the edge in one triangle is not strictly inside the circumcircle of the other. This is the [local Delaunay criterion](/local-delaunay-criterion/).
4. **Duality.** The circumcenters of the triangles are the vertices of the Voronoi diagram, and two points share a Voronoi edge exactly when they are joined by a strongly Delaunay edge; see [Voronoi-Delaunay duality](/voronoi-delaunay-duality/).
5. **Lifting.** On the [paraboloid lifting map](/paraboloid-lifting-map/) $p \mapsto (x, y, x^2 + y^2)$, the Delaunay triangles are the projections of the lower faces of the convex hull of the lifted points.
6. **Proximity subgraphs.** $\mathrm{EMST} \subseteq \mathrm{RNG} \subseteq \mathrm{GG} \subseteq \mathrm{DT}$, where every Euclidean minimum spanning tree counts on the left and every Delaunay triangulation on the right. The proof is below.

**The chain of proximity graphs.** The relative neighbourhood graph has the edge $pq$ when no point $r$ has $|pr| < |pq|$ and $|qr| < |pq|$. The Gabriel graph has the edge $pq$ when no other point lies in the closed disk with diameter $pq$.

- *EMST in RNG.* Let $pq$ be an edge of a minimum spanning tree $M$, and assume a point $r$ has $|pr| < |pq|$ and $|qr| < |pq|$. Removing $pq$ splits $M$ into two parts, one with $p$ and one with $q$. If $r$ is in the part of $q$, the tree with $pr$ in place of $pq$ is lighter; if $r$ is in the part of $p$, use $qr$. Both contradict minimality.
- *RNG in GG.* If $r \ne p, q$ lies in the closed disk with diameter $pq$, the angle at $r$ is at least $90$ degrees, so $|pq|^2 \ge |pr|^2 + |qr|^2$, and both $|pr|$ and $|qr|$ are strictly less than $|pq|$.
- *GG in DT.* For a Gabriel edge $pq$, the circle $C$ with diameter $pq$ has every other point strictly outside. Assume $pq$ is not an edge of a Delaunay triangulation $D$. No point is strictly inside the segment $pq$, so the segment enters the interior of a triangle $puv$ of $D$ at $p$ and leaves it at a point $x$ strictly inside the side $uv$. With the affine functions of the lifting map, $g = f_{puv} - f_C$ is zero at $p$ and positive at $u$ and $v$, which are strictly outside $C$, so it is positive at $x$ and, by linearity along the line, at $q$. So $|q|^2 = f_C(q) < f_{puv}(q)$, and $q$ is strictly inside the circle of $puv$, which is false.

So the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) is found in $O(n \log n)$ time by [Kruskal's algorithm](/kruskal/) on the at most $3n - 6$ Delaunay edges, and the [closest pair](/closest-pair-of-points/), which is a Gabriel edge, is a Delaunay edge.

## Representation

The points are stored in a list, with a dictionary from point to index. The triangulation is closed into a sphere with one extra vertex $G$ at infinity. Each hull edge $b \to a$ (counterclockwise along the hull) has a **ghost triangle** $(a, b, G)$ outside it. A dictionary `edge` maps each directed edge $(u, v)$ to the live triangle that has $u \to v$ on its boundary, ghosts included, so every directed edge has its reverse in the neighbouring triangle.

**Conflict.** A real triangle $abc$ is in conflict with $q$ when $\mathrm{incircle}(a, b, c, q) > 0$. A ghost $(u, v, G)$ is in conflict with $q$ when $\mathrm{orient}(u, v, q) > 0$, or when $q$ lies on the line $uv$ strictly between $u$ and $v$. So the "circle" of a ghost is the open half-plane outside its hull edge, plus the open edge.

**The history DAG.** Every triangle ever made is a node, and a triangle that is removed points to the triangles that replace it. Each node has a region. The region of a real triangle is the closed triangle. Let $o$ be the centroid of the first triangle, which stays strictly inside the hull. The region of a ghost $(a, b, G)$ is the set of points $q$ with $\mathrm{orient}(a, b, q) > 0$ in the closed wedge from $o$ between the rays to $b$ and to $a$. The coordinates of $3o$ are integers, so these tests are exact.

**Invariant.** After each insertion with at least three points not on a line:

1. The live real triangles are counterclockwise and form a triangulation of the inserted points. Each hull edge has one live ghost, and each directed edge of a live triangle has its reverse in exactly one other live triangle.
2. No live real triangle is in conflict with an inserted point.
3. The regions of the live triangles cover the plane, and the region of each removed node is covered by the regions of its children.

Before the first three points not on one line arrive, the points wait in a list and there are no triangles.

## Operations

```pseudo id=main
LOCATE(q)
L1  cur ← the root triangle (the first triangle or one of its three ghosts) whose region holds q
L2  while cur has children do
L3      cur ← a child of cur whose region holds q
L4  return cur

INSERT(q)                                      ▷ q is new, and a first triangle exists
L5  t ← LOCATE(q)
L6  if q is not on an edge of t then replace t by three triangles with apex q; push the three edges of t
L7  else replace t and the triangle t2 across that edge by two triangles each; push the four outer edges
L8  while the stack is not empty do pop xy; if the live triangle on x → y is (x, y, q), let t2 = (y, x, r) be across
L9      if t2 is in conflict with q then
L10         replace (x, y, q) and t2 by (q, x, r) and (q, r, y), which become the children of both
L11         push xr and ry
```

- **Lines L1 to L4.** The regions of the roots cover the plane, and each node's region is covered by its children, so line L3 always finds a child. The walk ends at a live triangle, real or ghost.
- **Line L6.** If $q$ is inside a real triangle, the split gives three triangles. If $q$ is in the region of a ghost, so outside the hull, the same split of $(u, v, G)$ gives the real triangle $(u, v, q)$ and two new ghosts.
- **Line L7.** If $q$ is on an edge, the two triangles on that edge, one of them a ghost when the edge is on the hull, are cut in two each.
- **Lines L8 to L11.** These are the flips of Lawson's method, with the new point locked as an apex. A flip of a real pair is the usual [edge flip](/edge-flip/). A flip of two ghosts adds a real triangle to the hull, the way a [beneath-beyond](/beneath-beyond/) hull update does.
- **Random order.** `delaunay_triangulation(points, seed)` shuffles the points with a fixed seed and inserts them one by one.

## Example

Insert $(0,0)$, $(6,0)$, $(3,5)$, $(3,-1)$ and $(3,2)$ in this order.

| step | point | what happens | live real triangles | DAG nodes |
| --- | --- | --- | --- | --- |
| 1, 2 | $(0,0)$, $(6,0)$ | on one line, they wait | none | 0 |
| 3 | $(3,5)$ | first triangle $(0,0), (6,0), (3,5)$ and three ghosts; $o = (3, 5/3)$ | 1 | 4 |
| 4 | $(3,-1)$ | in the region of the ghost below $(0,0)$ to $(6,0)$ (line L6); then line L9 finds $(3,-1)$ inside the circle of the first triangle (center $(3, 8/5)$, squared radius $289/25$, squared distance $169/25$) and line L10 flips $(0,0)$ to $(6,0)$ into $(3,-1)$ to $(3,5)$ | 2 | 9 |
| 5 | $(3,2)$ | LOCATE goes from the first triangle to its child $(3,-1), (6,0), (3,5)$; $(3,2)$ is on the edge from $(3,-1)$ to $(3,5)$, so line L7 cuts both triangles on it; no flip | 4 | 13 |

The result has the triangles $(3,-1), (3,2), (0,0)$, then $(3,2), (3,-1), (6,0)$, then $(3,2), (3,5), (0,0)$ and $(3,5), (3,2), (6,0)$: there are $2n - 2 - h = 10 - 2 - 4 = 4$, as Fact 1 says. `find_triangle((3, 1))` returns $(3,2), (3,-1), (6,0)$. The first triangle is a node with two children, $(3,-1), (6,0), (3,5)$ and $(3,-1), (3,5), (0,0)$, and the real triangle $(6,0), (0,0), (3,-1)$ made in step 4 has the same two children.

## Correctness

The proofs are in [the correctness proof](proofs/correctness/). The main point is that an insertion with flips does the same as the [Bowyer-Watson](/bowyer-watson-algorithm/) cavity step. Let $K$ be the set of live triangles in conflict with $q$. The triangle found by line L5, and the second one of line L7, are in $K$. Each flip of line L10 takes one more triangle of $K$ into the region around $q$ and replaces it by the fan from $q$ to its two outer edges. When the stack is empty, no triangle outside the region is in conflict with $q$ across its border, so the region is all of $K$, because $K$ is connected. The result is the Bowyer-Watson result, which is Delaunay. The DAG regions stay a cover because each replacement covers the region of what it replaces, with care for the ghost wedges.

## Complexity

| quantity | bound | kind |
| --- | --- | --- |
| total time for $n$ points in random order | $O(n \log n)$ | expected, general position |
| triangles made, so DAG nodes | fewer than $9n$ | expected, general position |
| flips in one insertion | $O(n)$ | worst case |
| one location | $O(n^2)$ nodes | worst case |
| total time | $O(n^3)$ | worst case, any order |
| `triangles`, `find_triangle` | $O(n)$, and a location | worst case |

The expected bounds are proved in [the complexity proof](proofs/complexity/) by [backwards analysis](/backwards-analysis/): the last point of a random order has expected degree less than $6$, so each insertion makes few triangles, and a point is visited in the DAG only by triangles whose circles hold it. They need the order to be random and the points to be in general position, with no three on a line and no four on a circle; then the Delaunay triangulation of each prefix is unique. For degenerate input such as grids, the code is still correct, and the expected running time observed in the tests stays small, but the proof does not cover it. The worst-case bounds are simple counts and are not tight. Any algorithm needs $\Omega(n \log n)$ time in the algebraic decision tree model, because sorting reduces to the Delaunay triangulation of points on a parabola; see [the lower bound](/voronoi-construction-lower-bound/).

## Variants

- **Bowyer-Watson.** Remove all conflict triangles at once and connect $q$ to the border of the cavity; see [Bowyer-Watson](/bowyer-watson-algorithm/).
- **Divide and conquer.** [Guibas and Stolfi](/guibas-stolfi-algorithm/) merge two halves in $O(n \log n)$ worst-case time with the [quad-edge structure](/quad-edge-data-structure/); [Dwyer's algorithm](/dwyer-algorithm/) cuts into strips and is fast in expectation for uniform points.
- **Sweep.** [Fortune's algorithm](/fortunes-algorithm/) builds the Voronoi diagram, and so the Delaunay triangulation, in $O(n \log n)$ worst-case time.
- **Flips from any triangulation.** The [Lawson flip algorithm](/lawson-flip-algorithm/) starts from any triangulation and flips until every edge is locally Delaunay, with at most $\binom{n}{2}$ flips.
- **Lifting.** Compute the lower convex hull of the lifted points in three dimensions; see [paraboloid lifting map](/paraboloid-lifting-map/).
- **Point location without a DAG.** Walk from a recent triangle toward $q$ ([triangle walk](/triangle-walk-point-location/)), or locate with a sample of the points (a "jump and walk"). With points sorted along a space-filling curve, walks are short in practice. The DAG is the method with a proved bound.
- **Deletion.** See [dynamic Delaunay triangulation](/dynamic-delaunay-triangulation/).
- **Constraints, weights and dimensions.** The [constrained Delaunay triangulation](/constrained-delaunay-triangulation/) keeps given segments, the [regular triangulation](/regular-triangulation/) is the weighted form, and [higher-dimensional Delaunay](/higher-dimensional-delaunay/) triangulations use circumspheres.

## When to use it

Use a Delaunay triangulation when you need a triangle mesh of scattered points with good angles: [piecewise linear interpolation](/piecewise-linear-interpolation/) of terrain or of measurements, the first step of [mesh generation](/mesh-generation/), and the neighbour structure of a point set. It gives in $O(n)$ extra time the closest pair, all nearest neighbours, the Euclidean minimum spanning tree, the Gabriel and relative neighbourhood graphs, and, by duality, the Voronoi diagram and the [largest empty circle](/largest-empty-circle/). Use the incremental structure when points arrive one by one or when you also need point location. If the input has segments that must be edges, use the constrained form.

## Pitfalls

- **Inexact predicates.** With floating point, the sign of $\mathrm{incircle}$ in line L9 can be wrong for nearly cocircular points, and the flip loop can cycle or make a triangulation that is not valid. Use exact integer arithmetic or an adaptive exact predicate.
- **Cocircular points.** In a grid, $\mathrm{incircle} = 0$ for many quadruples. Line L9 must flip only on a strictly positive value; flipping on zero can loop for ever between two equal choices.
- **A point on an edge.** If line L6 splits a triangle into three when $q$ is on one of its edges, one of the three is flat. Line L7 must cut the two triangles on that edge instead.
- **The hull.** Without ghosts, points outside the hull need a separate update, and collinear hull points are easy to lose. A large enclosing triangle is a common shortcut, but with coordinates that are not large enough it changes the result near the hull.
- **Sorted input.** The expected bound needs a random order. In sorted order, the DAG paths and the flips per insertion can be long; shuffle first, as `delaunay_triangulation` does.
- **Collinear start.** The first triangle needs three points not on one line. The code keeps the earlier collinear points waiting and inserts them after the first triangle is made.

## Implementations

## History

Boris Delaunay (Delone) defined the empty sphere criterion in 1934 and showed that it gives a tiling of space, dual to the tiling of Voronoi (1908). M. I. Shamos and D. Hoey (1975) brought the Voronoi diagram and its dual into computational geometry with an $O(n \log n)$ divide and conquer algorithm and its uses for closest point problems. C. L. Lawson (1977) introduced the flip method, and R. Sibson (1978) linked the local angle rule to the Delaunay property. A. Bowyer and D. F. Watson (1981) gave the cavity insertion. L. Guibas and J. Stolfi (1985) gave the quad-edge divide and conquer, and S. Fortune (1987) the sweep. L. J. Guibas, D. E. Knuth and M. Sharir (1992) analysed the randomized incremental method with the history DAG, following the work of K. L. Clarkson and P. W. Shor on random sampling. The Gabriel graph goes back to K. R. Gabriel and R. R. Sokal (1969), and the relative neighbourhood graph to G. T. Toussaint (1980).

## References
