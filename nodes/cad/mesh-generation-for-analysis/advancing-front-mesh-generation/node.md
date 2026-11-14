---
tag: NKGVJD
kind: algorithm
slug: advancing-front-mesh-generation
name: Advancing front mesh generation
aliases:
- advancing front method
- moving front method
area: cad/mesh-generation-for-analysis
level: core
summary: Builds a triangle or tetrahedral mesh from the boundary inward, adding one element at a time at an ideal point on the current front, after Lo, Peraire and Löhner.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of vertices of the output mesh}
  time: {worst: O(n^3)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1985
  people: [S. H. Lo, Jaime Peraire, Rainald Löhner, Paresh Parikh]
  note: Lo published an advancing front generator for planar domains in 1985. Peraire, Vahdati, Morgan and Zienkiewicz used one with a background mesh for adaptive flow computations in 1987, and Löhner and Parikh extended the method to tetrahedra in 1988.
prereqs: [mesh-generation, orientation-test, segment-intersection-detection]
see_also: [delaunay-refinement, ruppert-algorithm, chew-second-algorithm, constrained-delaunay-triangulation, mesh-sizing-function, paving, polygon-triangulation, schonhardt-polyhedron]
sources:
  - paper: doi:10.1002/nme.1620210805
    title: S. H. Lo, A new mesh generation scheme for arbitrary planar domains, International Journal for Numerical Methods in Engineering 21(8), 1985, 1403 to 1426
    locator: the generation of triangles from the boundary inward with a front of directed edges and the choice of the new node (general locator)
  - paper: doi:10.1016/0021-9991(87)90093-3
    title: J. Peraire, M. Vahdati, K. Morgan and O. C. Zienkiewicz, Adaptive remeshing for compressible flow computations, Journal of Computational Physics 72(2), 1987, 449 to 466
    locator: the advancing front generator driven by element sizes and stretching from a background mesh, used for adaptive remeshing (general locator)
  - paper: doi:10.1002/fld.1650081003
    title: Rainald Löhner and Paresh Parikh, Generation of three-dimensional unstructured grids by the advancing-front method, International Journal for Numerical Methods in Fluids 8(10), 1988, 1135 to 1149
    locator: the extension to tetrahedra, with the front made of triangles, and the data structures for the search of close points and faces (general locator)
---

Advancing front mesh generation fills a domain with triangles, or with tetrahedra in 3D, starting from its boundary. The boundary edges form the front. The method repeatedly takes one front edge, places an ideal new point inside at the distance that the [mesh sizing function](/mesh-sizing-function/) asks for, or uses a nearby existing front point instead, and adds the triangle if it does not overlap anything. The front then moves inward until it closes up. The result has well shaped triangles near the boundary and sizes that follow the sizing function, but the method has no quality guarantee: the quality of its triangles is only measured, never proved.

## In plain words

Think of tiling a floor from the walls inward. You lay a row of tiles along each wall. The inner edge of the tiles you have laid is the front. You pick a short piece of the front, cut a new tile to fit against it, and lay it down if it does not overlap any tile already there. Then the front has moved a little.

When two parts of the front come close, you use a corner that is already there instead of a new one, so the gaps close. In the end the front shrinks to nothing and the floor is covered.

The tiles near the walls are neat. Where the fronts meet in the middle, a tile can come out thin, and nothing in the method prevents it. A program measures the tiles at the end.

## The problem

This page solves the planar case of [mesh generation](/mesh-generation/), which asks for a triangulation of a domain whose triangles have bounded angles and sizes. Here the input is a simple polygon with rational corners in counterclockwise order and a target edge length $h > 0$. The output is a set of counterclockwise triangles that cover the polygon, have disjoint interiors, and meet edge to edge. Edge lengths should be close to $h$ and angles should be large, but these two wishes are goals, not guarantees.

## The algorithm

ORIENT2D is the [orientation test](/orientation-test/). A front edge $ab$ is directed so that the unmeshed region lies to its left. Coordinates are Fractions, so every test below is exact; floats are used only in L5 and L6 to propose candidates.

```pseudo id=main
ADVANCING-FRONT(P, h)
L1  F ← sides of P, each cut into ⌈|side| / h⌉ equal edges, directed counterclockwise
L2  V ← vertices of F;  h_min ← min(h, shortest edge of F) / 2;  T ← ∅
L3  while F ≠ ∅ do
L4      ab ← a shortest edge of F
L5      δ ← min(max(h, 0.55 |ab|), 2 |ab|);  p ← the point left of ab with |pa| = |pb| = δ, rounded to the grid of step h/64
L6      C ← front vertices c left of ab with |c − p| < 0.8 δ, nearest to p first; then p
L7      append to C all front vertices strictly left of ab, nearest to the midpoint of ab first
L8      c ← the first c in C with VALID(a, b, c)          ▷ the part added in L7 always has one
L9      T ← T ∪ {abc};  if c = p then V ← V ∪ {p}
L10     remove ab from F;  if bc ∈ F then remove it else add cb;  if ca ∈ F then remove it else add ac
L11 return T

VALID(a, b, c)
L12 if ORIENT2D(a, b, c) ≤ 0 then return false
L13 if c is new and |c − v| < h_min for some v ∈ V then return false
L14 if a front vertex other than a, b, c lies in the closed triangle abc then return false
L15 if bc or ca shares with a front edge, other than itself, a point that is not a common endpoint then return false
L16 return true
```

L5 places the ideal point. For an edge of length $h$ it is the apex of an equilateral triangle. For a short edge it is higher, to grow the size toward $h$, and for a long edge it is lower. L6 prefers an existing front vertex near the ideal point, which is how two parts of the front close up without thin gaps. L13 keeps new points away from old ones, which is what makes the method stop. L14 and L15 are the overlap tests, by the [segment intersection test](/segment-intersection-detection/) in exact arithmetic. L10 updates the front: a side of the new triangle that was a front edge is closed, and any other side becomes a new front edge, reversed so that the unmeshed region is on its left.

## Example

Take the square $(0,0)$, $(4,0)$, $(4,4)$, $(0,4)$ and $h = 2$. L1 cuts each side in two, so the front has 8 edges of length 2.

| step | edge $ab$ | ideal point $p$ | chosen $c$ | triangle |
|---|---|---|---|---|
| 1 | $(0,0) \to (2,0)$ | $(1, 55/32)$ | front vertex $(0, 2)$, at distance about 1.04 from $p$ | $(0,0), (2,0), (0,2)$ |
| 2 to 4 | the next shortest edges | | the corner neighbours | the other three corner triangles |
| 5 | $(0,2) \to (2,0)$, length $2\sqrt2$ | $(2, 2)$ | the new point $(2, 2)$ | $(0,2), (2,0), (2,2)$ |
| 6 to 8 | the rest of the diamond | | existing front vertices | three more triangles |

In step 1, $\delta = 2$ and the apex of the equilateral triangle is $(1, \sqrt3)$, which L5 rounds to $(1, 55/32)$. The vertex $(0, 2)$ is within $0.8 \delta = 1.6$ of it, so L6 tries it first, and it passes VALID. After step 4 the front is the diamond $(2,0), (4,2), (2,4), (0,2)$ with edges of length $2\sqrt2$, so in step 5, $\delta = 2$, the height is $\sqrt2$, and the ideal point is exactly the center $(2, 2)$. No front vertex is near it, so the new point is used. The result is 8 right isosceles triangles, each with ORIENT2D equal to 4. They add up to 32, twice the area of the square, and the smallest angle is $45°$.

**No quality guarantee.** On a random convex polygon with 7 integer corners in $[0, 40]^2$, all of whose angles are at least $89°$, and $h = 4$, the method makes 123 valid triangles. One of them, inside the polygon where two parts of the front closed up, has angles of about $4.4°$, $5.4°$ and $170°$. On the ten random convex polygons of the tests, with $h$ from 5 to 10, the smallest angles were between $17°$ and $32°$. These numbers are measurements. Nothing in the method bounds them.

## Correctness

The proof keeps four facts true before each step: front edges meet only at common endpoints; the front is the boundary of the unmeshed region, which lies to the left of each front edge; the triangles made so far are counterclockwise, inside the polygon and interior-disjoint from each other and from the unmeshed region; and no vertex lies on a triangle except at its corners. VALID implies that no front edge enters the new triangle, so the triangle lies in the unmeshed region, and the update of L10 keeps the four facts.

A valid choice always exists. The front edges form a planar straight line graph, and its [constrained Delaunay triangulation](/constrained-delaunay-triangulation/) has a triangle $abc$ on the left of every front edge $ab$. That triangle contains no other front vertex and crosses no front edge, so VALID accepts $c$, and L7 puts every such $c$ into the candidate list. The same fact, that every polygonal region can be triangulated with its own vertices, is the existence theorem of [polygon triangulation](/polygon-triangulation/).

The method stops. New points are at least $h_{\min}$ apart and from all older vertices, so by a packing argument only finitely many are made. The triangles never contain a vertex except at their corners, so they are faces of one triangulation of the final vertex set, which has at most $2|V| - 5$ triangles. Each iteration adds one triangle, so the loop runs at most that many times, and it stops only when the front is empty, when the triangles cover the polygon. The full proof is below.

Nothing in this argument concerns angles. Validity is proved; quality is not.

## Complexity

Each iteration scans the front to find the shortest edge, and each VALID test scans the front once, in $O(f)$ time for a front of $f$ edges. Usually one of the first few candidates is valid, so an iteration costs $O(f)$, and the whole run $O(n f)$, which is $O(n^{3/2})$ for a front of about $\sqrt n$ edges on a fat domain. In the worst case L8 tests all $O(f)$ fallback candidates, each in $O(f)$ time, so the time is $O(n^3)$ with $f = O(n)$. Production codes keep the front in a heap by length and the points and edges in a quadtree or an alternating digital tree, so that each search looks only at nearby entries. With such structures the run time is close to $O(n \log n)$ in practice, but this is not a proved bound. The space is $O(n)$.

## Properties

- **Valid output, proved.** The triangles tile the polygon edge to edge. With exact predicates this holds for every simple polygon.
- **No quality guarantee.** Angles are good near the boundary and can be poor where fronts meet. Unlike [Delaunay refinement](/delaunay-refinement/), which inserts circumcenters of bad triangles until a proved angle bound holds, as in [Ruppert's algorithm](/ruppert-algorithm/) and [Chew's second algorithm](/chew-second-algorithm/), the advancing front proves nothing about angles.
- **Boundary first.** The boundary edges are used as given, so the mesh conforms to the boundary without the boundary recovery that Delaunay methods need.
- **Follows a sizing function.** The ideal point uses the local size, so graded and stretched meshes are natural.
- **Not Delaunay.** The output is not in general a [Delaunay triangulation](/delaunay-triangulation/) of its vertices.

## Variants and improvements

- **Background mesh.** Peraire and coauthors read the size and a stretching direction from a coarse background mesh, which gives meshes adapted to a flow solution.
- **Advancing front Delaunay.** Points are placed by the advancing front rule but connected by Delaunay insertion, which combines good point placement with a Delaunay structure.
- **Three dimensions.** Löhner and Parikh advance a front of triangles with tetrahedra. The existence step of the proof fails in 3D, because a region such as the [Schönhardt polyhedron](/schonhardt-polyhedron/) cannot be split into tetrahedra without new points, so the 3D method can stall and needs repair steps, such as removing nearby elements and trying again.
- **Quadrilaterals.** [Paving](/paving/) advances rows of quadrilaterals from the boundary in the same way.
- **Smoothing after.** Most codes follow the method with [Laplacian smoothing](/laplacian-smoothing/) and edge swaps to improve the measured quality, as measured by the [mesh quality measures](/mesh-quality-measures/).

## When to use it

Use it when the boundary must be kept exactly as given, when the element size must follow a sizing function closely, or when stretched elements are needed near walls, as in flow simulation with the [finite element method](/finite-element-method/). It is also a good choice for surfaces, where the front can advance in the parameter plane or directly on the surface. Use a Delaunay refinement method instead when a proved lower bound on the angles is needed, or a [structured grid](/structured-grid-generation/) when the domain splits into four-sided blocks.

## Pitfalls

- **Inexact predicates.** With float orientation tests, a near-collinear case can accept an overlapping triangle and corrupt the front. Use exact or robust predicates for every validity test.
- **Expecting quality.** The method does not guarantee angles. Measure the mesh and repair it.
- **Front collisions.** Without the fallback of L7, two fronts that meet at a bad angle can leave a gap with no acceptable ideal point, and the method stalls.
- **Size jumps.** A boundary with very different edge lengths in one place gives triangles of very different sizes next to each other. Limit the gradation of the sizing function first.
- **3D failure.** In 3D the method can stall on regions that have no tetrahedralization without new points; a robust code needs a fallback such as local remeshing.

## Implementations

## History

S. H. Lo published a method in 1985 that builds triangles from the boundary of a planar domain inward. Peraire, Vahdati, Morgan and Zienkiewicz developed the advancing front generator with a background mesh for adaptive compressible flow computations in 1987, and Löhner and Parikh extended it to tetrahedra in 1988. The method became the main unstructured mesh generator in computational fluid dynamics in the following years, next to Delaunay methods, and the two families were later combined.

## References
