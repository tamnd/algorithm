---
tag: A9ZH8Y
kind: problem
slug: constrained-triangulation
name: Constrained triangulation
aliases:
- Constrained Delaunay triangulation problem
- triangulation of a planar straight-line graph
- triangulation with required edges
area: geometry/triangulations
level: advanced
summary: Triangulate a point set so that prescribed segments appear as edges.
model: real-ram
complexity:
  vars: {n: the number of points and segments}
  time: {worst: Θ(n log n)}
prereqs: [triangulation-of-point-set, polygon-triangulation, orientation-test]
see_also: [constrained-delaunay-triangulation, conforming-delaunay-triangulation, polygon-with-holes-triangulation, steiner-points, mesh-generation, schonhardt-polyhedron, greedy-triangulation, planar-subdivision]
sources:
  - paper: "Der-Tsai Lee and Arthur K. Lin, Generalized Delaunay triangulation for planar graphs, Discrete and Computational Geometry 1, 201 to 217 (1986)"
    locator: the constrained Delaunay triangulation, its max-min angle property and an O(n^2) algorithm
  - paper: "L. Paul Chew, Constrained Delaunay triangulations, Algorithmica 4, 97 to 108 (1989)"
    locator: the O(n log n) divide and conquer algorithm
  - paper: "Jim Ruppert and Raimund Seidel, On the difficulty of triangulating three-dimensional nonconvex polyhedra, Discrete and Computational Geometry 7, 227 to 253 (1992)"
    locator: NP-completeness of deciding whether a polyhedron can be tetrahedralized without Steiner points
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: Chapter 2 (planar straight-line graphs, constrained triangulations and constrained Delaunay triangulations; ISBN to be checked)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 2 (triangulating polygons with holes by the monotone sweep)
---

A constrained triangulation of a point set with some prescribed segments is a triangulation that contains every prescribed segment as an edge and uses no other vertices. The input is a planar straight-line graph, and the output fills each of its faces with triangles. In the plane such a triangulation always exists, and one can be found in $\Theta(n \log n)$ time; the best known one is the [constrained Delaunay triangulation](/constrained-delaunay-triangulation/), which maximizes the smallest angle among all constrained triangulations. [Polygon triangulation](/polygon-triangulation/), with or without holes, is the special case where the segments are the boundary. In three dimensions the analogous problem can have no solution at all.

## In plain words

You have some dots, and some of them are already joined by straight lines that must stay. Join more pairs of dots by straight lines, never crossing anything, until the whole region is cut into triangles. The lines you were given must be among the sides of the triangles, and you may not add new dots.

This is always possible on a flat sheet. The interesting question is which of the many possible answers to pick: the usual choice keeps the triangles as fat as possible, given that the fixed lines cannot move.

## Definition

**Input.** A planar straight-line graph $G = (S, L)$: a set $S$ of points and a set $L$ of segments with end points in $S$, such that two segments meet only at a common end point and no point of $S$ lies inside a segment. Let $n = |S| + |L|$.

**Output.** A [triangulation](/triangulation/) $T$ of the convex hull of $S$ with vertex set exactly $S$ that contains every segment of $L$ as an edge. When a domain is given, such as the inside of a polygon with holes, the triangles outside the domain are dropped.

**Existence.** Start from the edge set $L$ and add segments between points of $S$, each containing no other point and crossing nothing already chosen, until none can be added. The result is a maximal plane straight-line graph, and every bounded face of a maximal one is an empty triangle (the argument is in the [greedy triangulation](/greedy-triangulation/) proof). So every planar straight-line graph has a constrained triangulation, and every constrained triangulation of the hull has $3|S| - h - 3$ edges and $2|S| - h - 2$ triangles, where $h$ is the number of points on the hull boundary, just like an unconstrained one.

## Variants

- **Constrained Delaunay triangulation.** Among all constrained triangulations, choose one in which every edge not in $L$ is locally Delaunay: its quadrilateral has the fourth vertex outside the circumcircle, or the edge is in $L$. Equivalently, the circumcircle of each triangle contains no point of $S$ that is visible from the inside of the triangle, where segments of $L$ block visibility. It maximizes the smallest angle among constrained triangulations (Lee and Lin).
- **Conforming triangulation.** Allow [Steiner points](/steiner-points/) on the segments, and ask that each segment be a union of edges. A [conforming Delaunay triangulation](/conforming-delaunay-triangulation/) is a true Delaunay triangulation of the enlarged point set.
- **Polygons and polygons with holes.** The segments form one or more cycles and only the inside is kept. See [triangulation of a polygon with holes](/polygon-with-holes-triangulation/).
- **Optimal constrained triangulations.** Minimum total edge length, or the greedy rule, with required edges. The [greedy triangulation](/greedy-triangulation/) with $L$ inserted first is a constrained triangulation.
- **Three dimensions.** Given a polyhedron or a piecewise linear complex, tetrahedralize it with no new vertices. This can be impossible: the [Schönhardt polyhedron](/schonhardt-polyhedron/) has no tetrahedralization, and deciding whether one exists is NP-complete (Ruppert and Seidel).

## Examples

- **One forced edge.** Take $a = (0,0)$, $b = (6,0)$, $c = (5,3)$, $d = (0,4)$ and the required segment $bd$. The Delaunay triangulation uses $ac$, since $d$ lies outside the circle through $a, b, c$. The only constrained triangulation is $abd$, $bcd$, and it is also the constrained Delaunay triangulation, because the only interior edge is required.
- **A polygon.** If $L$ is the boundary cycle of a simple polygon, the triangles inside form a polygon triangulation with $n - 2$ triangles, and the triangles outside fill the pockets between the polygon and its hull.
- **A segment through the middle.** In the square $(0,0)$, $(4,0)$, $(4,4)$, $(0,4)$ with the extra points $(1,2)$ and $(3,2)$ joined by a required segment, the segment is an edge of one triangle above it and one below it. The constrained Delaunay triangulation has 6 triangles, as $2 \cdot 6 - 4 - 2 = 6$ predicts.
- **A non-example.** A set of segments that cross is not a planar straight-line graph. The crossing point must first be added as a vertex, which is a Steiner point.

## Known algorithms

| method | time | note |
|---|---|---|
| greedy fill around the required edges | $O(n^3)$ | add any non-crossing segment until none is left |
| plane sweep (monotone pieces of the faces) | $O(n \log n)$ | the monotone method extended to a planar straight-line graph |
| Lee and Lin | $O(n^2)$ | constrained Delaunay triangulation |
| Chew, divide and conquer | $O(n \log n)$ | constrained Delaunay triangulation |
| segment insertion into a Delaunay triangulation | $O(n^2)$ worst case | remove the triangles crossed by a segment and retriangulate the two sides |
| [Lawson flips](/lawson-flip-algorithm/) of the unconstrained edges | $O(n^2)$ flips | from any constrained triangulation to the constrained Delaunay one |

Segment insertion is what most libraries do: it is short, and in practice the crossed region is small. Shewchuk's Triangle and CGAL use it, with randomized incremental insertion of the points first.

## Bounds

- **Upper bound.** $O(n \log n)$ on the [real RAM](/real-ram/), for an arbitrary constrained triangulation and for the constrained Delaunay one.
- **Lower bound.** $\Omega(n \log n)$ in the [algebraic decision tree](/algebraic-decision-tree/) model, even with no segments, since a triangulation of a point set gives its convex hull. For a simple polygon given as a cycle, the lower bound fails: the problem takes $O(n)$ time by Chazelle's algorithm.
- **Existence in three dimensions.** Deciding whether a polyhedron has a tetrahedralization without Steiner points is NP-complete.

## Reductions

- **From polygon triangulation.** A simple polygon is the constrained triangulation of its boundary cycle restricted to the inside.
- **To a planar subdivision.** The required segments cut the hull into faces, and each face, a polygon possibly with holes, is triangulated on its own.
- **From sorting.** The convex hull reduction gives the lower bound.

## Applications

- **Terrain models.** Breaklines such as ridges, rivers and roads are required segments, so that the interpolated surface follows them.
- **Mesh generation.** Delaunay refinement starts from a constrained Delaunay triangulation of the input planar straight-line graph. See [mesh generation](/mesh-generation/).
- **Rendering and font rasterization.** Outlines with holes are triangulated as planar straight-line graphs.
- **Motion planning and visibility.** A constrained triangulation of the free space is a convenient graph for shortest paths and point location.

## References
