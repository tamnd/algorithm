---
tag: ST4QMH
kind: problem
slug: mesh-self-intersection
name: Mesh self-intersection detection
aliases:
- self-intersecting mesh test
area: cad/mesh-processing
level: core
summary: Decide whether a triangle mesh crosses itself, or list every pair of its triangles that meet in more than the vertices and edges they share.
prereqs: [triangle-triangle-intersection, manifold-mesh]
see_also: [segment-intersection-detection, bounding-volume-hierarchy, mesh-arrangements, mesh-boolean-operations, mesh-repair-problem, element-distinctness, collision-detection, exact-geometric-computation]
sources:
  - book: isbn:9780821849255
    title: Herbert Edelsbrunner and John Harer, Computational Topology, An Introduction, American Mathematical Society, 2010
    locator: Chapter II, Surfaces, Section II.3, Self-intersections
  - paper: doi:10.1145/2431211.2431214
    title: Marco Attene, Marcel Campen and Leif Kobbelt, Polygon mesh repairing, an application perspective, ACM Computing Surveys 45(2), Article 15, 2013
    locator: the parts on self-intersections as a type of defect and on the methods that find and remove them
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 6, Bounding Volume Hierarchies (the broad phase that selects candidate pairs of triangles)
---

Mesh self-intersection detection asks whether the triangles of a mesh, placed in space by the positions of their vertices, meet anywhere except where the mesh says they should: at the vertices and edges they share. A mesh can be a perfect [manifold mesh](/manifold-mesh/) in its connectivity and still pass through itself in space, and then it does not bound a solid. The decision version asks for a yes or no, and the reporting version asks for all pairs of triangles that intersect in a wrong way. The pair test is the [triangle-triangle intersection test](/triangle-triangle-intersection/), and the problem is the 3D form of [segment intersection detection](/segment-intersection-detection/) for a polygon. For a mesh with $m$ triangles, the number of bad pairs can be $\Theta(m^2)$, and the decision version needs $\Omega(m \log m)$ time in the algebraic decision tree model.

## In plain words

A mesh is a list of flat triangles that are glued along their sides. The list says which triangles are neighbours. But the positions of the corners can put two triangles through each other, like a sheet of paper pushed through another sheet, even when the list looks fine.

The problem is to find such places. Two triangles that share a side or a corner touch there, and that is allowed. Anything more is a crossing: one triangle passes through the other, or two neighbours fold onto each other and overlap.

A shape with a crossing has no clear inside and outside at that place. Programs that cut, print, join or fill the shape need to know about each crossing first.

## Definition

**Input.** A triangle mesh: positions $p_0, \ldots, p_{n-1}$ in $\mathbb{R}^3$, with exact coordinates, and $m$ triangles, each a triple of distinct vertex indices. Each triangle $s$ stands for the closed set $|s|$, the convex hull of the positions of its vertices.

**Proper and improper pairs.** For two different triangles $s$ and $t$, let $C = s \cap t$ be the set of vertex indices that they share. The pair is *proper* if

$$|s| \cap |t| = \mathrm{conv}\{p_v : v \in C\},$$

with $\mathrm{conv}(\emptyset) = \emptyset$. So triangles that share no vertex must be disjoint, triangles that share one vertex must meet only at that point, and triangles that share an edge must meet only along that edge. Otherwise the pair is *improper*, or *self-intersecting*.

**Output.** The decision version returns whether every pair is proper. The mesh is then *self-intersection free*, or *embedded*: the union of the triangles is a surface in space with the topology that the connectivity describes. The reporting version returns the set of all improper pairs. The construction version also returns the curves of intersection, the segments of $|s| \cap |t|$, as input for [mesh arrangements](/mesh-arrangements/) and [mesh Boolean operations](/mesh-boolean-operations/).

**Degeneracies are part of the input.** Meshes from CAD and from scans have triangles that touch at one point, edges that lie in another triangle, coplanar neighbours, and two vertices with equal positions. The definition covers each case without general position: two different vertices at the same point make every pair of triangles that uses them improper, and a coplanar fold of two neighbours is improper because the overlap is a region, not the shared edge. Triangles with collinear vertices are degenerate, and the input is assumed to have none, or they are reported apart.

**The predicate.** All decisions are signs of the [orientation test](/orientation-test/) ORIENT3D, or of 2D orientation tests in the coplanar case. In floating point these signs can be wrong for nearly coplanar or nearly touching triangles, through [catastrophic cancellation](/catastrophic-cancellation/). A wrong sign makes a proper pair look improper, which is common for neighbours at a small angle, or hides a real crossing. Exact answers need exact predicates, for example with [Shewchuk's expansion arithmetic](/shewchuk-expansion-sum/) or in the [exact geometric computation](/exact-geometric-computation/) model.

## Variants

- **Decision or reporting.** A yes or no, one improper pair as a witness, or all improper pairs.
- **The intersection curves.** The segments of each improper pair, and their arrangement on each triangle. This needs constructions, not only signs, and new points with rational coordinates.
- **Self or mutual.** Two meshes $A$ and $B$ against each other, as in collision detection and Boolean operations, is the same problem on the union of the two meshes, without the pairs inside one mesh.
- **Polygon meshes.** Faces with more than three vertices are first split into triangles, or tested as planar polygons.
- **Tolerance.** In engineering, pairs that come closer than a distance $\delta$ count as bad. This is a different problem: it asks for near pairs, and it has more pairs than the exact one.

## Examples

Let $p_0 = (0, 0, 0)$, $p_1 = (4, 0, 0)$, $p_2 = (0, 4, 0)$, and $s = (0, 1, 2)$ in the plane $z = 0$.

- **A proper neighbour.** $t = (1, 0, 3)$ with $p_3 = (1, -1, 0)$. The two triangles lie in one plane, on opposite sides of the shared edge, and meet only along the segment from $p_0$ to $p_1$. Proper.
- **A fold.** $t = (1, 0, 3)$ with $p_3 = (1, 1, 0)$. Now $p_3$ is on the same side of the shared edge as $p_2$, and the two triangles overlap in a region of the plane. Improper, although they share an edge and the mesh can be manifold.
- **A poke through a shared vertex.** $t = (0, 3, 4)$ with $p_3 = (2, 2, 2)$ and $p_4 = (2, 2, -2)$. The triangle $t$ lies in the plane $x = y$ and crosses the plane $z = 0$ along the segment from $p_0$ to $(2, 2, 0)$, which lies in $s$. So $|s| \cap |t|$ is a segment, not the shared point $p_0$. Improper.
- **Two closed solids.** Two tetrahedra that overlap in space, stored as one mesh with 8 triangles. Each tetrahedron is a closed manifold, but some triangles of one cross triangles of the other. Improper pairs between the two parts.
- **Quadratically many pairs.** For $i = 0, \ldots, k-1$, let $A_i$ be the thin triangle with the vertices $(i, -1, 0)$, $(i, k, 1)$ and $(i, k, -1)$ in the plane $x = i$. For $j = 0, \ldots, k-1$, let $B_j$ be the triangle with the vertices $(-1, j, 0)$, $(k, j, 1)$ and $(k, j, -1)$ in the plane $y = j$. Each $A_i$ and each $B_j$ contain the point $(i, j, 0)$, and they share no vertex, so each pair is improper. The mesh has $m = 2k$ triangles and $k^2 = m^2/4$ improper pairs.

## Known algorithms

| method | guarantee | time |
|---|---|---|
| test all pairs with the [triangle-triangle test](/triangle-triangle-intersection/) | exact with exact predicates; reports all pairs | $\Theta(m^2)$ |
| [bounding volume hierarchy](/bounding-volume-hierarchy/) of the triangles, then the exact test on each pair of overlapping boxes | exact; reports all pairs | $O(m^2)$ in the worst case; measured near $O(m \log m)$ plus the output on typical meshes |
| [uniform grid](/uniform-grid/) or [octree](/octree/) of the triangles, then the exact test on each pair in a common cell | exact; reports all pairs | $O(m^2)$ in the worst case; fast on meshes of even triangle size, measured |
| exact arrangements with filtered or rational arithmetic, as in [mesh arrangements](/mesh-arrangements/) | exact intersection curves | output sensitive in practice, measured |
| floating point pair tests with a tolerance | none: can report false pairs and miss real ones | as the method it uses |

The broad phase with boxes only removes pairs that cannot meet. Its speed on real meshes is a measured result: there is no proof of a bound better than $O(m^2)$ for the hierarchy methods on all inputs, and the quadratic example above forces $\Omega(m^2)$ for any method that reports all pairs. For triangles that share a vertex or an edge, the exact test must ignore the shared part: one way is to test the edges and the vertices that are not shared against the other triangle.

## Bounds

- **Output size.** The reporting version can have $\Theta(m^2)$ answers, by the example of the crossing slivers. So $\Theta(m^2)$ time is optimal for reporting in the worst case, and only output-sensitive bounds can be better.
- **Lower bound for the decision version.** Deciding whether a mesh is self-intersection free needs $\Omega(m \log m)$ time in the [algebraic decision tree](/algebraic-decision-tree/) model. The proof reduces [element distinctness](/element-distinctness/): for numbers $x_1, \ldots, x_m$, make the triangle with the vertices $(x_i, 0, 0)$, $(x_i, 1, 0)$ and $(x_i, 0, 1)$ for each $i$, with no shared vertex indices. Two of these triangles meet if and only if their $x$ values are equal, because they lie in the parallel planes $x = x_i$. So the mesh is self-intersection free if and only if the numbers are distinct.
- **Upper bound.** $O(m^2)$ pair tests decide and report, each in $O(1)$ time on the [real RAM](/real-ram/).

## Reductions

- **From element distinctness**, as in the lower bound above.
- **To the 2D case.** For a mesh that lies in one plane, the problem is the intersection of triangles in the plane, and for the boundary of a polygon it is [segment intersection detection](/segment-intersection-detection/), which the [Shamos-Hoey algorithm](/shamos-hoey-algorithm/) decides in $O(n \log n)$ time. The sweep does not extend directly to triangles in space: the triangles that cross a sweep plane cut it in segments, and these segments have no above and below order, so the argument of the 2D sweep fails.
- **Into mesh Boolean operations.** The reporting and construction versions are the first step of [mesh Boolean operations](/mesh-boolean-operations/) and of [mesh arrangements](/mesh-arrangements/), which compute all the intersection curves and then classify the pieces.

## Applications

- **3D printing.** Slicing for additive manufacturing needs a closed, embedded surface, so that each layer has a clear inside. A self-intersection makes the slices wrong.
- **Mesh repair.** Finding and removing self-intersections is one of the main steps of [mesh repair](/mesh-repair-problem/).
- **Meshing for simulation.** A [tetrahedralization](/tetrahedralization/) of a solid needs an embedded boundary surface.
- **Animation and cloth.** Self-collision of a deforming surface is the same test at each time step, with a tolerance.

## References
