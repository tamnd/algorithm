---
tag: 2N7KHY
kind: problem
slug: polygon-triangulation
name: Polygon triangulation
aliases:
- Triangulating a simple polygon
- triangulating a polygon
- triangulation of a simple polygon
area: geometry/triangulations
level: intro
summary: Partition a simple polygon into n-2 triangles by non-crossing diagonals.
model: real-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: Θ(n)}
prereqs: [simple-polygon, ear, orientation-test]
see_also: [two-ears-theorem, ear-clipping, monotone-polygon-triangulation, seidel-polygon-triangulation, chazelle-polygon-triangulation, polygon-with-holes-triangulation, triangulation-dual-tree, triangulation]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 3, Polygon Triangulation (3.1 Guarding and Triangulations, 3.2 Partitioning a Polygon into Monotone Pieces, 3.3 Triangulating a Monotone Polygon, and the chapter notes)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Sections 1.2 and 1.6 (theory and ear clipping), and Chapter 2, Polygon Partitioning (monotone partitioning, trapezoidalization, monotone mountains, and the linear-time algorithm)
  - paper: "Bernard Chazelle, Triangulating a simple polygon in linear time, Discrete and Computational Geometry 6, 485 to 524 (1991)"
    locator: the main theorem
  - paper: "Raimund Seidel, A simple and fast incremental randomized algorithm for computing trapezoidal decompositions and for triangulating polygons, Computational Geometry 1(1), 51 to 64 (1991)"
    locator: the O(n log* n) expected time bound
  - paper: "Michael R. Garey, David S. Johnson, Franco P. Preparata and Robert E. Tarjan, Triangulating a simple polygon, Information Processing Letters 7(4), 175 to 179 (1978)"
    locator: the O(n log n) algorithm through monotone pieces
---

Polygon triangulation is the problem of cutting a [simple polygon](/simple-polygon/) into triangles whose corners are vertices of the polygon. The cuts are diagonals, segments between two vertices that run inside the polygon, and they must not cross. Every simple polygon with $n$ vertices can be cut this way, always into exactly $n - 2$ triangles by $n - 3$ diagonals. The problem is a standard first step in geometry: once a polygon is triangulated, area, point location, guarding, shortest paths and rendering become easy.

## In plain words

You have a shape drawn with straight sides that does not cross itself. You want to cut it into triangles, and each cut must go straight from one corner to another and stay inside the shape. Cuts may not cross each other. However you do it, you always end up with two triangles fewer than the number of corners. The question is how fast a computer can find a good set of cuts. A simple method takes time that grows with the square of the number of corners. Better methods are almost linear, and one famous method is exactly linear but too complicated to program.

## Definition

**Input.** A simple polygon $P$ given by its vertices $v_0, \ldots, v_{n-1}$ in boundary order, $n \ge 3$.

**Output.** A set $D$ of diagonals of $P$ that do not cross each other (they may share end points) and that cut $P$ into triangles. A **diagonal** is a segment $v_i v_j$ whose relative interior lies in the interior of $P$. Equivalently, the output is a list of triangles with corners among the vertices, with pairwise disjoint interiors and union $P$.

Every triangulation of $P$ has exactly $n - 3$ diagonals and $n - 2$ triangles. The angles of the triangles add up to the interior angles of $P$, which add up to $(n - 2)\pi$, and each triangle has angle sum $\pi$. Each diagonal adds one piece, so $n - 2$ pieces need $n - 3$ diagonals. A triangulation always exists by the [two ears theorem](/two-ears-theorem/), and a maximal set of non-crossing diagonals is always a triangulation.

The triangles and diagonals form a [maximal outerplanar graph](/outerplanar-graph/) on the vertices of $P$, and its [dual tree](/triangulation-dual-tree/) has one node per triangle.

## Variants

- **Polygons with holes.** The region has an outer boundary and disjoint holes, $n$ vertices in all and $h$ holes. Every triangulation has $n + 2h - 2$ triangles. See [triangulation of polygons with holes](/polygon-with-holes-triangulation/).
- **Point sets.** No boundary is given; the triangles must cover the convex hull of a point set. See [triangulation of a point set](/triangulation-of-point-set/).
- **Optimal triangulations.** Among all triangulations, find one that minimizes a cost that adds up over triangles, such as total diagonal length. For a simple polygon, the [interval dynamic program](/polygon-triangulation-dp/) solves this in $O(n^3)$ time.
- **Steiner triangulations.** Extra vertices may be added, for example to avoid thin triangles. See [Steiner points](/steiner-points/) and [mesh generation](/mesh-generation/).
- **Partition into other shapes.** Into monotone pieces ([monotone polygon partition](/monotone-polygon-partition/)), into convex pieces ([convex decomposition](/convex-decomposition/), [Hertel-Mehlhorn](/hertel-mehlhorn/)), or into trapezoids ([trapezoidal map](/trapezoidal-map/)).
- **Three dimensions.** A polyhedron need not have a tetrahedralization without new vertices; see [tetrahedralization](/tetrahedralization/) and the [Schönhardt polyhedron](/schonhardt-polyhedron/).

## Examples

- **A convex polygon.** All diagonals from one vertex form a triangulation, a fan, in $O(n)$ time. A convex polygon has the [Catalan number](/catalan-triangulation-theorem/) $C_{n-2}$ triangulations.
- **The notched rectangle** $(0,0), (6,0), (6,4), (4,4), (3,1), (2,4), (0,4)$ has 7 vertices. [Ear clipping](/ear-clipping/) cuts it into the 5 triangles $(v_5, v_6, v_0)$, $(v_4, v_5, v_0)$, $(v_4, v_0, v_1)$, $(v_4, v_1, v_2)$, $(v_4, v_2, v_3)$ by the 4 diagonals $v_5 v_0$, $v_4 v_0$, $v_4 v_1$, $v_4 v_2$. The doubled areas $8 + 10 + 6 + 12 + 6 = 42$ add up to twice the polygon's area.
- **Few triangulations.** The strip with exactly two ears in the Tightness section of the [two ears theorem](/two-ears-theorem/) has $n = 2k$ vertices and only $2^{k-2}$ triangulations: each of its $k - 2$ inner quadrilaterals can be split by either of two diagonals. A convex polygon with the same $n$ has far more, about $4^n$.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| Diagonal splitting (find a diagonal, recurse) | $O(n^2)$ | follows the existence proof |
| [Ear clipping](/ear-clipping/) | $O(n^2)$ | simple, exact, the usual choice for small polygons |
| [Monotone partition](/monotone-polygon-partition/) plus [monotone triangulation](/monotone-polygon-triangulation/), Garey, Johnson, Preparata and Tarjan 1978 | $O(n \log n)$ | a sweep, then a linear stack pass on each piece; also handles holes |
| [Tarjan and Van Wyk](/tarjan-van-wyk-triangulation/) 1988 | $O(n \log \log n)$ | Jordan sorting with finger search trees |
| Clarkson, Tarjan and Van Wyk 1989 | $O(n \log^* n)$ expected | randomized |
| [Seidel](/seidel-polygon-triangulation/) 1991 | $O(n \log^* n)$ expected | randomized incremental trapezoidal map; practical |
| [Chazelle](/chazelle-polygon-triangulation/) 1991 | $O(n)$ | deterministic; of theoretical interest only |
| Amato, Goodrich and Ramos 2001 | $O(n)$ expected | randomized; simpler than Chazelle's, still not used in practice |

All the algorithms faster than $O(n \log n)$ compute a trapezoidal decomposition (or the closely related horizontal visibility map) of the polygon first. A trapezoidal decomposition turns into a triangulation in $O(n)$ time: draw a diagonal in each trapezoid whose two supporting vertices are not on the same side, which cuts the polygon into monotone mountains, and triangulate each mountain in linear time.

Practical software uses ear clipping for small inputs, the sweep or Seidel's algorithm for large ones, or a constrained Delaunay triangulation when triangle shape matters.

## Bounds

- **Upper bound.** $O(n)$ time on the [real RAM](/real-ram/), by Chazelle's algorithm. The output has size $\Theta(n)$, so this is optimal.
- **Lower bound.** $\Omega(n)$, since every vertex must be read and every diagonal written.
- **Polygons with holes.** $\Theta(n \log n)$ in the [algebraic decision tree](/algebraic-decision-tree/) model: the sweep gives the upper bound, and a reduction from sorting gives the lower bound (Asano, Asano and Pinter 1986).
- **Point sets.** $\Theta(n \log n)$, because every triangulation of a point set contains the convex hull edges, and the hull lower bound applies.
- **Open problem.** Whether a simple, deterministic, linear-time algorithm exists, one practical enough to be implemented, is a long-standing open question.

## Reductions

- **Triangulation to trapezoidal decomposition and back.** Given the trapezoidal decomposition (horizontal visibility map) of a simple polygon, a triangulation follows in $O(n)$ time, and a triangulation gives the visibility map in $O(n)$ time as well (Fournier and Montuno 1984; Chazelle and Incerpi 1984). So the two problems have the same complexity, which is why the fast algorithms attack the visibility map.
- **Sorting to polygon with holes.** Sorting $n$ numbers reduces to triangulating a polygon with holes, which is the source of the $\Omega(n \log n)$ bound above.
- **Simplicity testing.** Chazelle's algorithm can also decide in linear time whether a closed polygonal chain is simple; see [polygon simplicity test](/polygon-simplicity-test/).

## Applications

- **Art galleries.** Fisk's proof of the [art gallery theorem](/art-gallery-theorem/) 3-colors a triangulation, so $\lfloor n/3 \rfloor$ guards suffice.
- **Area and centroid.** Add up the triangles; for a simple polygon the [shoelace formula](/shoelace-formula/) gives the same area directly.
- **Point location.** A triangulated polygon or subdivision feeds [Kirkpatrick's point location](/kirkpatrick-point-location/).
- **Shortest paths.** Shortest paths inside a simple polygon are found by walking the [dual tree](/triangulation-dual-tree/) of a triangulation (the funnel algorithm).
- **Graphics.** GPUs draw triangles, so filled polygons, fonts and map regions are triangulated before rendering.
- **Meshing.** A triangulation of the domain is the starting point for [mesh generation](/mesh-generation/) by refinement.

## References
