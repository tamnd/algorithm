---
tag: EEQ0M1
kind: concept
slug: edge-flip
name: Edge flip
aliases:
- Diagonal flip
- Lawson flip
area: geometry/triangulations
level: core
summary: Replace the diagonal of a convex quadrilateral formed by two adjacent triangles with the other diagonal.
prereqs: [triangulation, orientation-test, convex-polygon]
see_also: [flip-graph, flip-distance, lawson-flip-algorithm, local-delaunay-criterion, in-circle-test, quad-edge-data-structure, tree-rotation, tetrahedralization]
sources:
  - paper: "Charles L. Lawson, Transforming triangulations, Discrete Mathematics 3(4), 365 to 372 (1972)"
    locator: the flip operation and the connectivity of triangulations of a point set under flips
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 9, Section 9.1 (edge flips, illegal edges, Lemma 9.4 and Algorithm LegalTriangulation)
  - book: isbn:9783642129704
    title: Jesús A. De Loera, Jörg Rambau and Francisco Santos, Triangulations, Structures for Algorithms and Applications, Springer, 2010
    locator: Chapter 3 (flips in the plane) and Chapter 2 (bistellar flips in general dimension); chapter numbers to be checked
  - paper: "Leonidas Guibas and Jorge Stolfi, Primitives for the manipulation of general subdivisions and the computation of Voronoi diagrams, ACM Transactions on Graphics 4(2), 74 to 123 (1985)"
    locator: the Swap operation on the quad-edge structure
---

An edge flip changes a triangulation in the smallest possible way. Take an edge shared by two triangles. Together they form a quadrilateral, and the edge is one of its two diagonals. If the quadrilateral is convex, delete the edge and insert the other diagonal: the result is again a triangulation of the same points, with two new triangles in place of the old two. Flips are the basic move of [Lawson's algorithm](/lawson-flip-algorithm/) for Delaunay triangulations, they define the [flip graph](/flip-graph/), and they are the local operation of most mesh improvement codes.

## In plain words

Two triangles that share a side make a four-sided shape. The shared side runs between two opposite corners. If the shape has no dent, you can erase that side and draw the line between the other two corners instead, which gives two different triangles covering the same shape. Nothing else in the drawing changes. Doing this over and over lets you walk from any way of cutting a set of points into triangles to any other way.

## The idea

**Definition.** Let $T$ be a [triangulation](/triangulation/) and let $e = ac$ be an edge shared by the triangles $abc$ and $acd$. The four points $a, b, c, d$ form the quadrilateral $Q = abcd$, with $e$ as a diagonal. The edge $e$ is **flippable** if $Q$ is strictly convex, that is, $b$ and $d$ lie on opposite sides of the line $ac$ (always true) **and** $a$ and $c$ lie on opposite sides of the line $bd$. Then the **flip** of $e$ replaces the triangles $abc, acd$ by $abd, bcd$, and the edge $ac$ by $bd$.

With the [orientation test](/orientation-test/), for counterclockwise triangles $abc$ and $acd$:
$$e \text{ is flippable} \iff \mathrm{orient}(b, d, c) < 0 < \mathrm{orient}(b, d, a),$$
that is, the open segments $ac$ and $bd$ cross.

**Why the result is a triangulation.** The segment $bd$ lies inside $Q$ because $Q$ is convex. The two new triangles have positive area because no three of $a, b, c, d$ are collinear (if $a$, $b$, $d$ were collinear, $a$ would be on the line $bd$). They cover exactly $Q$, and everything outside $Q$ is unchanged. The new edge $bd$ cannot already be an edge of $T$, because it would cross $ac$. So the number of triangles and edges stays the same, as the [counting theorem](/triangulation-counting-theorem/) demands.

**Non-flippable edges.** If $Q$ is not convex (one of $a$ or $c$ is a reflex corner, or lies exactly on the segment $bd$), the other diagonal leaves $Q$ or passes through a vertex, and the flip is not allowed. Hull edges and constrained edges are never flipped. In a convex polygon with no three vertices collinear, every diagonal is flippable.

**Flip criteria.** Algorithms decide which flippable edges to flip by a local rule:

- **Delaunay (Lawson) criterion.** Flip $ac$ if $d$ lies strictly inside the circumcircle of $abc$, decided by the [in-circle test](/in-circle-test/). An edge where this does not happen is *locally Delaunay*; when every edge is, the triangulation is the [Delaunay triangulation](/delaunay-triangulation/) ([local Delaunay criterion](/local-delaunay-criterion/)). For a convex quadrilateral exactly one of the two diagonals is locally Delaunay unless the four points are cocircular, and that diagonal has the larger minimum angle among the six angles of its two triangles.
- **Other criteria.** Flip if it shortens the diagonal, lowers the maximum angle, or improves a mesh quality measure. Such greedy flipping stops in a local optimum, which in general is not a global one.

**Termination of Delaunay flips.** Lift each point $p$ to $(p_x, p_y, p_x^2 + p_y^2)$ on the [paraboloid](/paraboloid-lifting-map/). A Delaunay flip replaces two lifted triangles by the two below them, so the lifted surface moves down and never returns to a previous triangulation. With $n$ points, Lawson's algorithm stops after $O(n^2)$ flips, and $\Theta(n^2)$ flips can be necessary.

**Higher dimensions.** In three dimensions the analogue is a bistellar flip on five points: two tetrahedra sharing a triangle are replaced by three tetrahedra sharing an edge (a 2-3 flip) or back (3-2). Flips of type 1-4 and 4-1 insert and remove a vertex. Unlike the planar flip, the 2-3 flip changes the number of tetrahedra; see [tetrahedralization](/tetrahedralization/).

**Data structures.** On a [quad-edge structure](/quad-edge-data-structure/) the flip is the Swap operation: two Splice calls detach the edge from its endpoints and two more attach it to the opposite corners. On a doubly connected edge list it rewires six half-edge records and two faces.

## Examples

- **A square.** In the square $a = (0,0)$, $b = (2,0)$, $c = (2,2)$, $d = (0,2)$, the diagonal $ac$ is flippable; flipping it gives $bd$. The two triangulations of the square are the two endpoints of a single flip, as the [Catalan count](/catalan-triangulation-theorem/) $C_2 = 2$ predicts.
- **A thin rhombus.** Take $a = (0,0)$, $b = (3,-1)$, $c = (6,0)$, $d = (3,1)$ with the long diagonal $ac$. The circumcircle of $abc$ has center $(3,4)$ and radius 5, and $d$ is at distance 3 from the center, so $d$ is inside and the Delaunay criterion flips $ac$ to $bd$. The smallest angle rises from $\arctan(1/3) \approx 18.4°$ (at $a$ in triangle $abc$) to about $36.9°$ (at $a$ in triangle $abd$).
- **A dart.** The triangles $(0,0), (4,0), (1,1)$ and $(0,0), (1,1), (0,4)$ share the edge from $(0,0)$ to $(1,1)$. Their union is the quadrilateral $(0,0), (4,0), (1,1), (0,4)$, which is reflex at $(1,1)$. The other diagonal, from $(4,0)$ to $(0,4)$, runs along the line $x + y = 4$, above the point $(1,1)$, outside the union. The edge is not flippable.
- **A flat corner.** Take $a = (1,1)$, $b = (0,0)$, $c = (2,0)$, $d = (2,2)$. The triangles $abc$ and $acd$ are counterclockwise and share the edge $ac$, but $a$ lies on the segment $bd$: the quadrilateral has an angle of exactly $\pi$ at $a$. Here $\mathrm{orient}(b, d, a) = 0$, the flip would create the flat triangle $abd$, and it is not allowed.
- **Fan to fan.** In a convex polygon $v_0 \ldots v_{n-1}$, the fan at $v_0$ becomes the fan at $v_1$ by $n - 3$ flips: flip $v_0 v_2$ to $v_1 v_3$, then $v_0 v_3$ to $v_1 v_4$, and so on.

## Where it is used

- **Delaunay triangulation.** [Lawson's flip algorithm](/lawson-flip-algorithm/) flips non-locally-Delaunay edges until none remain; incremental algorithms such as [Bowyer-Watson](/bowyer-watson-algorithm/) and the randomized incremental construction restore the Delaunay property by flips after each insertion.
- **Flip graphs and associahedra.** Triangulations as vertices, flips as edges: the [flip graph](/flip-graph/) is connected for planar point sets (Lawson 1972); for a convex polygon it is the graph of the associahedron, with diameter $2n - 10$ for $n \ge 13$ ([flip graph diameter theorem](/flip-graph-diameter-theorem/)).
- **Flip distance.** The least number of flips between two triangulations; NP-hard for point sets and for simple polygons, open for convex polygons ([flip distance](/flip-distance/)).
- **Binary trees.** A flip in a convex polygon is a [rotation](/tree-rotation/) in the corresponding binary tree, which is how Sleator, Tarjan and Thurston studied rotation distance.
- **Constrained triangulations.** Inserting a required segment by flipping away the edges it crosses (Sloan; see [constrained triangulation](/constrained-triangulation/)).
- **Mesh improvement.** Flips to improve angles, combined with vertex smoothing and insertion, in [mesh generation](/mesh-generation/) and [Delaunay refinement](/delaunay-refinement/).
- **Data-dependent triangulations.** For terrain interpolation, flips that reduce a roughness measure of the interpolated surface.

## References
