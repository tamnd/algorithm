---
tag: MHT5ZY
kind: data-structure
slug: constrained-delaunay-triangulation
name: Constrained Delaunay triangulation
aliases:
- CDT
- generalized Delaunay triangulation
- obstacle Delaunay triangulation
area: geometry/voronoi-and-delaunay
level: advanced
summary: Triangulation that contains prescribed segments while being Delaunay with respect to the visible points.
model: real-ram
complexity:
  vars: {n: the number of points}
  time: {build: O(n^3), query: O(n)}
  space: {extra: O(n^2)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [delaunay-triangulation, constrained-triangulation, in-circle-test, edge-flip]
see_also: [conforming-delaunay-triangulation, ruppert-algorithm, chew-second-algorithm, lawson-flip-algorithm, local-delaunay-criterion, mesh-generation, polygon-with-holes-triangulation, paraboloid-lifting-map]
sources:
  - paper: doi:10.1007/BF02187695
    title: D. T. Lee and A. K. Lin, Generalized Delaunay triangulation for planar graphs, Discrete and Computational Geometry 1, 1986, 201-217
    locator: the definition with visibility, the existence of the triangulation and an O(n^2) construction
  - paper: doi:10.1007/BF01553881
    title: L. P. Chew, Constrained Delaunay triangulations, Algorithmica 4, 1989, 97-108
    locator: the definition, the existence proof and the O(n log n) divide and conquer construction
  - book: isbn:9781584887300
    title: S.-W. Cheng, T. K. Dey and J. R. Shewchuk, Delaunay Mesh Generation, CRC Press, 2013
    locator: the chapter on constrained Delaunay triangulations in the plane (constrained Delaunay edges, the flip algorithm and segment insertion)
---

A constrained Delaunay triangulation (CDT) of a set $P$ of points and a set $S$ of segments between them is a triangulation of $P$ that has every segment of $S$ as an edge and is as near to a [Delaunay triangulation](/delaunay-triangulation/) as the segments allow. A point counts against a triangle only when it is *visible* from the triangle, that is, when no segment of $S$ blocks the line of sight. The rule is that no visible point is strictly inside the circumcircle of a triangle. The CDT exists for every input, it is the [constrained triangulation](/constrained-triangulation/) that maximizes the smallest angle, and it is the usual start for quality [mesh generation](/mesh-generation/) of domains with boundaries and holes. This page builds it from a maximal set of non-crossing edges followed by [Lawson flips](/lawson-flip-algorithm/) on the edges that are not segments, with exact integer predicates.

## In plain words

Some lines must be in the mesh: the walls of a room, the border of a lake, a road. A plain Delaunay mesh of the points may cut across these lines, so we cannot use it.

The constrained version keeps every required line as an edge. For the other edges it uses the usual Delaunay rule, the empty circle, with one change: a point behind a wall does not count. Each triangle must have no point inside its circle that it can see. A wall can hide a point, and then that point is allowed inside.

To build it, first draw any triangle mesh that keeps the walls. Then look at each edge that is not a wall. If the two triangles beside it are a bad pair, swap the edge to the other diagonal. When no edge needs a swap, the mesh is done.

## The abstract type

The structure stores a set of points with integer coordinates and a set of segments between them.

- `insert_point(p)`: add the point $p$. Return False if it is already there.
- `insert_segment(p, q)`: add the segment $pq$ between two stored points. Return False if $p = q$, if a point is missing, if the segment adds nothing, or if it crosses a stored segment at one point inside both.
- `triangles()`: the triangles of the CDT as counterclockwise point triples.
- `constraint_edges()`: the segments, cut at every stored point that lies on them. These pieces are edges of the CDT.

**Notation.** $P$ is the set of points, $n = |P|$, and $h$ is the number of points on the boundary of the convex hull of $P$, those in the middle of a hull side included. A point is $p = (x, y)$. $\mathrm{orient}(p, q, r)$ is positive when $p, q, r$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$ is positive when $d$ is strictly inside the circle through the counterclockwise triangle $abc$; both are exact integer determinants, see the [in-circle test](/in-circle-test/). The **pieces** are the segments of $S$ cut at the points of $P$ on them, so no point is strictly inside a piece, and two pieces meet at most at a common end point. Two points $x$ and $r$ are **visible** to each other when the closed segment $xr$ does not meet the relative interior of any piece. The segment may pass through an end point of a piece.

**Definition.** A triangulation $T$ of $P$ is a constrained Delaunay triangulation of $(P, S)$ when every piece is an edge of $T$ and, for every triangle $t$ of $T$, no point of $P$ that is visible from a point in the interior of $t$ lies strictly inside the circumcircle of $t$. An edge $e$ of $T$ is **locally Delaunay** when it is a hull edge, or when the vertex of one triangle on $e$ opposite to $e$ is not strictly inside the circumcircle of the other triangle on $e$, see the [local Delaunay criterion](/local-delaunay-criterion/). With $S$ empty, the CDT is a Delaunay triangulation.

No general position is assumed. With four or more cocircular points, as in a grid, the CDT is not unique, and the code returns one of them. With fewer than three points, or all points on one line, there are no triangles.

## Representation

The points are a list, and the segments are a list of point pairs. The triangulation is a dictionary `edge` from each directed edge $(u, v)$ to the counterclockwise triangle that has $u \to v$ on its boundary, with points given by index. The two triangles on an edge $uv$ are `edge[(u, v)]` and `edge[(v, u)]`; a hull edge has only one of the two keys. A set `fixed` holds the pieces as unordered index pairs.

**Invariant.** After a build:

1. The triangles of `edge` form a triangulation of $P$: they are counterclockwise, their union is the convex hull of $P$, their interiors are disjoint, and every point of $P$ is a vertex.
2. Every pair in `fixed` is an edge.
3. Every edge that is not in `fixed` is locally Delaunay.

The structure keeps the input and rebuilds the triangulation on the next query after an insertion. The method `check_invariant` tests items 2 and 3 with exact arithmetic.

## Operations

```pseudo id=main
BUILD(P, S)                                   ▷ points with integer coordinates; S pairwise non-crossing
L1  F ← the pieces of S (each segment cut at the points of P on it)
L2  for each pair ab, the pieces first, then the Delaunay edges of P, then all other pairs do
L3      if no point of P is strictly inside ab and ab crosses no chosen edge then
L4          choose ab
L5  T ← the counterclockwise triangles uvw of chosen edges with no other point of P in the closed triangle
L6  push every directed edge of T that is not in F on a stack
L7  while the stack is not empty do pop ab; if ab is an interior edge not in F, let abc and bad be its triangles
L8      if incircle(a, b, c, d) > 0 then flip: replace abc and bad by adc and dbc
L9          push ad, db, bc and ca
L10 return the triangles of T
```

- **Line L1.** A point of $P$ in the middle of a segment cuts it, so every piece is an edge with no point inside it. Without this cut, the segment could not be an edge of any triangulation of $P$.
- **Lines L2 to L4.** A greedy scan makes a maximal set of edges that do not cross and pass through no point. Every piece is chosen, because pieces do not cross each other. Any order gives a triangulation; the Delaunay edges come next only so that few flips are left for later.
- **Line L5.** The faces of a maximal set of non-crossing edges are triangles with no point inside or on their sides, so they are the triangles of three chosen edges that hold no other point.
- **Lines L6 to L9.** This is the Lawson flip loop with the pieces locked. Line L8 flips an edge that is not locally Delaunay; the four outer edges of the quadrilateral get new opposite vertices, so line L9 tests them again.

`insert_point` and `insert_segment` only change the input lists and mark the structure as stale. The segment test of `insert_segment` cuts the new segment and the old ones into pieces and rejects a crossing at one inner point of both.

## Example

Take $P = \{(0, 0), (8, 0), (4, 2), (4, -2), (4, 7)\}$ and one segment from $(0, 0)$ to $(8, 0)$. The plain Delaunay triangulation has the edge from $(4, 2)$ to $(4, -2)$, which crosses the segment, so it is not allowed.

| line | pair | result |
| --- | --- | --- |
| L1 | $(0,0)$ to $(8,0)$ | the only piece, in $F$ |
| L4 | $(0,0)$ to $(8,0)$ | chosen first |
| L3 | $(4,2)$ to $(4,-2)$ | crosses the piece, rejected |
| L4 | the six other Delaunay edges and $(0,0)$ to $(4,7)$ | chosen |
| L3 | $(4,-2)$ to $(4,7)$ | holds $(4,2)$, rejected |
| L5 | 8 chosen edges | 4 triangles |
| L8 | the 3 interior edges not in $F$ | all locally Delaunay, no flip |

The result has the triangles $(0,0), (4,-2), (8,0)$, then $(0,0), (8,0), (4,2)$, then $(0,0), (4,2), (4,7)$ and $(4,2), (8,0), (4,7)$. There are $2n - 2 - h = 10 - 2 - 4 = 4$ of them, as for every triangulation of $5$ points with $4$ on the hull.

The CDT is not Delaunay. The triangle $(0,0), (8,0), (4,2)$ has its circumcenter at $(4, -3)$ with squared radius $25$, and $(4,-2)$ is at distance $1$ from it, so it is strictly inside. The segment hides it: the segment from any inner point of the triangle to $(4,-2)$ crosses the piece. In the same way, the triangle $(0,0), (4,-2), (8,0)$ has center $(4, 3)$ and squared radius $25$, with $(4, 2)$ and $(4, 7)$ inside its circle and both hidden. The triangle $(0,0), (4,2), (4,7)$ has center $(1/4, 9/2)$ and squared radius $325/16$, and $(8, 0)$ is outside, at squared distance $1285/16$. `insert_segment((4, 2), (4, -2))` returns False, because it crosses the first segment at $(4, 0)$.

## Correctness

The full proof is in [the correctness proof](proofs/correctness/). It has four parts.

1. **A triangulation that holds the pieces.** Lines L2 to L4 give a maximal set of non-crossing edges. A face of such a set is a triangle: if a face were not a triangle, an extreme vertex $w$ of the face, with its two edges $wx$ and $wy$ around the face, would give either the edge $xy$ or an edge from $w$ to the point of the triangle $wxy$ next to $w$, and the scan would have chosen it. Hull edges are always chosen, because no edge can cross them.
2. **Flips are legal.** If $\mathrm{incircle}(a, b, c, d) > 0$, the quadrilateral $adbc$ is strictly convex, so the new edge $cd$ is inside it and the two new triangles are counterclockwise. A piece is never flipped.
3. **Termination.** On the [paraboloid lifting map](/paraboloid-lifting-map/), a flip lowers the lifted surface at every point of the quadrilateral and strictly at the crossing of the diagonals. So an edge that is flipped away never returns, and there are at most $n(n-1)/2$ flips.
4. **The result is constrained Delaunay.** When the stack is empty, every edge not in $F$ is locally Delaunay. Take a triangle $t$, a point $r$ visible from an inner point $s$ of $t$, and the first point $u$ of $P$ on the way from $s$ to $r$. The walk from $s$ to $u$ crosses only edges that are not pieces. Each crossing can only raise the affine lifted function of the current triangle along the rest of the walk, and at $u$ the last function is $|u|^2$. So $u$ is not strictly inside the circle of $t$, and then $r$, which is $u$ or lies beyond $u$ on a ray from the inside of the circle, is not strictly inside either.

## Complexity

| operation | time (worst case) | note |
| --- | --- | --- |
| insert_point, insert_segment | $O(n^2)$ | each accepted segment adds a new piece, so there are at most $3n$ segments; the triangulation is rebuilt later |
| build, lines L2 to L5 | $O(n^3)$ | $O(n^2)$ pairs, each tested against $O(n)$ points and $O(n)$ chosen edges |
| build, lines L6 to L9 | $O(n^2)$ | at most $n(n-1)/2$ flips, each with $O(1)$ work and $4$ pushes |
| triangles, constraint_edges | $O(n)$ after a build | at most $2n - 5$ triangles |

The extra space is $O(n^2)$ for the list of candidate pairs. These bounds are for this simple code and are proved in the correctness proof. Chew's divide and conquer algorithm builds the CDT in $O(n \log n)$ time, which is optimal, since the case without segments is the Delaunay triangulation; Seidel gave a sweep with the same bound. Incremental codes insert each segment by removing the triangles that it crosses and retriangulating the two polygons on its sides; the time per segment depends on the number of crossed triangles.

## Variants

- **Conforming Delaunay triangulation.** Add [Steiner points](/steiner-points/) on the segments until the plain Delaunay triangulation holds every piece. It needs no visibility rule, but the number of extra points can be large. See [conforming Delaunay triangulation](/conforming-delaunay-triangulation/).
- **Quality meshes.** [Ruppert's algorithm](/ruppert-algorithm/) and [Chew's second algorithm](/chew-second-algorithm/) start from a CDT and insert circumcenters of bad triangles, a form of [Delaunay refinement](/delaunay-refinement/).
- **Polygons with holes.** For a [polygon with holes](/polygon-with-holes/), take the polygon edges as segments, build the CDT and delete the triangles outside the domain. This gives a [triangulation of the polygon with holes](/polygon-with-holes-triangulation/) with the max-min angle property among all its triangulations.
- **Constrained Voronoi diagram.** The dual of the CDT is a diagram in which the segments block the distance. Joe and Wang describe the duality.
- **Weighted and three-dimensional forms.** A constrained regular triangulation uses the power distance. In three dimensions, a constrained Delaunay tetrahedralization need not exist without extra points; the [Schönhardt polyhedron](/schonhardt-polyhedron/) has no tetrahedralization at all.

## When to use it

Use a CDT when the triangulation must keep given edges: the boundary of a mesh domain, the breaklines of a terrain model, the walls of a map, or the edges of a polygon to be triangulated with good angles. If only the points matter, use the plain [Delaunay triangulation](/delaunay-triangulation/). If the downstream code needs the empty circle property with no visibility exception, for example to read off a Voronoi diagram, use a conforming triangulation instead. This code is for small inputs and for tests; for large inputs use an incremental CDT with fast segment insertion, or Chew's algorithm.

## Pitfalls

- **Points on a segment.** If line L1 does not cut a segment at a point inside it, the segment is not an edge of any triangulation, line L3 rejects every pair that runs through that point, and the result misses the segment.
- **Crossing segments.** Two segments that cross at one inner point cannot both be edges. `insert_segment` rejects the second one. Without that test, line L3 would drop one of the two pieces in silence.
- **Flipping a segment.** Line L7 must skip the edges in $F$. A flip test on a piece would often find it not locally Delaunay, as in the example, and remove it.
- **A wrong visibility test.** A point is hidden only when the line of sight crosses a piece. A test that also counts a touch at an end point of a piece hides too many points and accepts a triangulation that is not constrained Delaunay.
- **Float predicates.** Grids put many points on one circle, and then the sign of $\mathrm{incircle}$ in line L8 is zero. With rounding, the sign can be wrong in both directions and the flip loop of lines L7 to L9 may cycle. The code uses exact integers.

## Implementations

## History

D. T. Lee and A. K. Lin defined the generalized Delaunay triangulation of a planar straight-line graph in 1986 and gave an $O(n^2)$ algorithm. L. Paul Chew gave the $O(n \log n)$ divide and conquer algorithm at the 1987 Symposium on Computational Geometry, with the journal version in Algorithmica in 1989. R. Seidel gave an $O(n \log n)$ sweep at about the same time. B. Joe and C. A. Wang described the dual constrained Voronoi diagram in 1993. The CDT became the base of Delaunay refinement through the work of Chew and of J. Ruppert, and of the 2D mesh generator Triangle of J. R. Shewchuk.

## References
