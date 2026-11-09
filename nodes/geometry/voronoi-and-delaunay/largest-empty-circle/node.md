---
tag: QE221C
kind: problem
slug: largest-empty-circle
name: Largest empty circle
aliases:
- largest inscribed circle among points
- maximal empty circle
- maximum empty circle
- largest empty disc
area: geometry/voronoi-and-delaunay
level: core
summary: Find the largest circle whose interior contains no input point and whose center lies in the region of interest.
prereqs: [voronoi-diagram, convex-hull, voronoi-diagram-construction]
see_also: [fortunes-algorithm, empty-circle-property, circumcircle, minimum-enclosing-circle, largest-empty-rectangle, facility-location-problem, delaunay-triangulation, farthest-point-voronoi-diagram]
sources:
  - paper: doi:10.1109/SFCS.1975.8
    title: M. I. Shamos and D. Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975
    locator: the largest empty circle as an application of the Voronoi diagram
  - paper: "G. T. Toussaint, Computing largest empty circles with location constraints, International Journal of Computer and Information Sciences 12(5), 1983"
    locator: the O(n log n) algorithm when the center must lie in a convex polygon, and the list of candidate centers
  - paper: doi:10.1007/BF01840442
    title: D. T. Lee and Y. F. Wu, Geometric complexity of some location problems, Algorithmica 1, 1986
    locator: the lower bound of Omega(n log n) in the algebraic decision tree model for the maximum gap and related location problems
---

The largest empty circle problem asks, for a finite set $P$ of $n$ points in the plane and a region $Q$, for a circle of largest radius whose center lies in $Q$ and whose open disc holds no point of $P$. The usual region is the convex hull of $P$, or a given convex polygon; without a region the radius is unbounded. The answer is the point of $Q$ farthest from its nearest point of $P$. Its center is a vertex of the [Voronoi diagram](/voronoi-diagram/) of $P$ inside $Q$, a point where a Voronoi edge crosses the boundary of $Q$, or a vertex of $Q$. So the problem takes $O(n \log n)$ time with a Voronoi algorithm, and this is optimal in the algebraic decision tree model.

## In plain words

You have a set of shops in a town. You want to open a new shop as far as possible from all the others, but inside the town. Draw a circle around the new place that just touches the nearest old shop. The task is to make this circle as large as possible.

The best place is never in the middle of open ground between two shops: you could move away from the nearest shop and gain. So it is at a corner where three or more shops are equally near, or on the edge of the town at a place halfway between two shops, or at a corner of the town.

## Definition

**Input.** A finite set $P$ of $n \ge 1$ points $p = (x, y)$, and a closed convex region $Q$, usually the convex hull of $P$ or a convex polygon with $m$ vertices.

**Output.** A point $c \in Q$ that maximizes

$$f(c) = \min_{p \in P} |c - p|,$$

and the radius $f(c)$. The open disc of radius $f(c)$ around $c$ holds no point of $P$, and some point of $P$ is on its circle.

Notation: $n = |P|$, $h$ is the number of points on the boundary of the convex hull of $P$, $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside their circle. An *empty* circle has no point of $P$ in its open disc; the [empty circle property](/empty-circle-property/) of Delaunay triangles is the same notion.

**The candidate theorem.** Let $Q$ be a convex polygon. Then the maximum of $f$ over $Q$ is reached at one of these points: (a) a Voronoi vertex in $Q$; (b) a point where a Voronoi edge meets the boundary of $Q$; (c) a vertex of $Q$.

*Proof.* The Voronoi cells of $P$ are closed convex polygons that cover the plane, so $Q$ is the union of the convex polygons $Q \cap V_p$. On $Q \cap V_p$ the function $f$ is $c \mapsto |c - p|$, which is convex, so its maximum on this convex polygon is reached at a vertex of the polygon. A vertex of $Q \cap V_p$ is a vertex of $V_p$ in $Q$, which is (a), a point where an edge of $V_p$ meets the boundary of $Q$, which is (b), or a vertex of $Q$ in $V_p$, which is (c). $\square$

When $Q$ is the convex hull of $P$, its vertices are points of $P$ with $f = 0$, so (c) gives the answer only when $n = 1$. If $P$ is on one line and $Q$ is its hull, the problem is half the largest gap between consecutive points.

## Variants

- **Center in a convex polygon.** The general form above, with $m$ vertices for $Q$; it takes $O((n + m) \log (n + m))$ time.
- **Center in a simple polygon or a union of regions.** The same candidates, with the crossings of Voronoi edges and the boundary of the region, and the vertices of the region.
- **Largest empty circle among obstacles.** With segments or polygons as obstacles, the Voronoi diagram of segments takes the place of the point diagram; see [weighted and segment Voronoi diagrams](/weighted-voronoi-diagram/).
- **Largest empty rectangle.** The axis-parallel rectangle version, with a different structure: [largest empty rectangle](/largest-empty-rectangle/).
- **Smallest enclosing circle.** The opposite problem, the smallest circle that holds all points: [minimum enclosing circle](/minimum-enclosing-circle/). Its center is a vertex of the [farthest-point Voronoi diagram](/farthest-point-voronoi-diagram/) or the midpoint of two points.
- **Dynamic and higher-dimensional.** In $d$ dimensions the candidates are the vertices of the Voronoi diagram and its crossings with the boundary of the region, whose number can be $\Theta(n^{\lceil d/2 \rceil})$.

## Examples

- **Six points.** Let $P = \{(2,8), (6,7), (0,4), (4,5), (8,3), (3,0)\}$ and let $Q$ be its hull, the pentagon $(3,0), (8,3), (6,7), (2,8), (0,4)$. All five Voronoi vertices are in $Q$; their squared radii are $221/50$, $1105/196$, $50/9$, $5525/722$ and $1105/121$. The five Voronoi rays cross the hull edges at their midpoints, with squared radii $17/4$, $5$, $5$, $25/4$ and $17/2$. The largest is $1105/121$, so the answer is the circle with center $(56/11, 24/11)$ through $(3,0)$, $(4,5)$ and $(8,3)$, with radius $(1105)^{1/2}/11 \approx 3.02$.
- **An obtuse triangle.** Let $P = \{(0,0), (4,0), (2,1)\}$ and $Q$ its hull. The only Voronoi vertex, the circumcenter $(2, -3/2)$, is outside $Q$. The bisector of $(0,0)$ and $(2,1)$ crosses the long edge at $(5/4, 0)$, and the bisector of $(4,0)$ and $(2,1)$ crosses it at $(11/4, 0)$; both give radius $5/4$. The crossings with the two short edges are their midpoints, with radius $5^{1/2}/2 < 5/4$. So there are two optimal centers on the boundary, and the answer is not unique.
- **Points on a line.** For $(0,0), (1,0), (5,0), (6,0)$ with $Q$ the segment from $(0,0)$ to $(6,0)$, the answer is the center $(3, 0)$ of the largest gap, with radius $2$.

## Known algorithms

| algorithm | time | kind of bound | notes |
| --- | --- | --- | --- |
| test all candidates against all points | $O(n^4)$ | worst case | every triple of points for (a) and every pair with every edge of $Q$ for (b); a test oracle |
| Voronoi diagram, then the candidates | $O(n \log n)$ | worst case | build the diagram with [Fortune's algorithm](/fortunes-algorithm/) or a Delaunay algorithm, then test $O(n)$ vertices and edges against $Q$ |
| center in a convex polygon $Q$ with $m$ vertices (Toussaint 1983) | $O((n + m) \log (n + m))$ | worst case | the crossings of Voronoi edges with $\partial Q$ are found by walking the cells along $\partial Q$ |

With the [Delaunay triangulation](/delaunay-triangulation/) instead of the Voronoi diagram, candidate (a) is the [circumcenter](/circumcenter/) of a Delaunay triangle, with the circumradius as its radius; the triangle's [circumcircle](/circumcircle/) is empty by definition. When $Q$ is the hull of $P$, the hull edges of the Delaunay triangulation are dual to the Voronoi rays, and a ray meets its own hull edge only at the midpoint of that edge. A Voronoi edge can also cross other hull edges: in the obtuse triangle, the ray of $(0,0)$ and $(2,1)$ crosses the long edge at $(5/4, 0)$. So every Voronoi edge is tested against the boundary.

## Bounds

The problem takes $\Theta(n \log n)$ time in the worst case. The upper bound is the Voronoi method above. For the lower bound, take numbers $x_1, \ldots, x_n$ and the points $(x_i, 0)$, with $Q$ their hull: the answer is half the largest gap between consecutive numbers, and Lee and Wu showed that the maximum gap needs $\Omega(n \log n)$ time in the [algebraic decision tree](/algebraic-decision-tree/) model. In models with the floor function, the maximum gap takes $O(n)$ time by bucketing, so the lower bound depends on the model.

## Reductions

- **To the Voronoi diagram.** By the candidate theorem, in $O(n)$ time after the diagram is built, plus the work to clip it to $Q$.
- **From the maximum gap.** As in the bounds, for points on a line.
- **Relation to the Delaunay triangulation.** Every empty circle through three points of $P$ in general position is the circumcircle of a Delaunay triangle, so the unconstrained candidates of type (a) are exactly the circumcenters of Delaunay triangles.

## Applications

- **Facility location.** Place a new, unwanted facility, such as a dump or a noisy plant, as far as possible from all existing ones; this is the obnoxious [facility location](/facility-location-problem/) problem in its simplest form.
- **Shops and services.** Find the place in a town that is worst served by a set of shops, as a place for a new shop.
- **Sampling and meshing.** The largest empty circle measures how well a point set covers a region; farthest point sampling inserts the next point at the center of a largest empty circle.
- **Motion planning.** The widest gap for a round robot among point obstacles.

## References
