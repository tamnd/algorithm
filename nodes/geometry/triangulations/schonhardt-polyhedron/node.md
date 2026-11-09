---
tag: DWGGKA
kind: concept
slug: schonhardt-polyhedron
name: Schönhardt polyhedron
aliases:
- Twisted triangular prism
- Schonhardt polyhedron
- Schönhardt's twisted prism
area: geometry/triangulations
level: research
summary: Polyhedron that cannot be tetrahedralised without adding interior Steiner points.
prereqs: [tetrahedralization, steiner-points, simple-polygon]
see_also: [minimum-steiner-triangulation, two-ears-theorem, polygon-triangulation, mesh-generation, delaunay-refinement, conforming-delaunay-triangulation]
sources:
  - paper: "Erich Schönhardt, Über die Zerlegung von Dreieckspolyedern in Tetraeder, Mathematische Annalen 98, 309 to 312 (1928)"
    locator: the twisted prism and the proof that it has no tetrahedralization
  - paper: "Jim Ruppert and Raimund Seidel, On the difficulty of triangulating three-dimensional nonconvex polyhedra, Discrete and Computational Geometry 7(3), 227 to 253 (1992)"
    locator: Schönhardt polyhedra as gadgets in the NP-completeness proof
  - paper: "Bernard Chazelle, Convex partitions of polyhedra, a lower bound and worst-case optimal algorithm, SIAM Journal on Computing 13(3), 488 to 507 (1984)"
    locator: polyhedra needing Ω(n^2) Steiner points
  - paper: "Jörg Rambau, On a generalization of Schönhardt's polyhedron, in Combinatorial and Computational Geometry, MSRI Publications 52, Cambridge University Press, 501 to 516 (2005)"
    locator: twisted prisms over polygons with more vertices are not triangulable (pages to be checked)
  - book: isbn:9783642129704
    title: Jesús A. De Loera, Jörg Rambau and Francisco Santos, Triangulations, Structures for Algorithms and Applications, Springer, 2010
    locator: the section on non-triangulable nonconvex polyhedra (section to be checked)
---

The Schönhardt polyhedron is a nonconvex polyhedron with 6 vertices and 8 triangular faces that cannot be cut into tetrahedra whose vertices are its own vertices. It is obtained from a triangular prism by rotating the top triangle a little and folding each side quadrilateral inward along one diagonal. Erich Schönhardt described it in 1928. It shows that the planar fact that every simple polygon can be triangulated without [Steiner points](/steiner-points/) has no analogue in space: some polyhedra need extra vertices, and deciding whether a polyhedron needs them is NP-complete. One Steiner point at its center is enough.

## In plain words

Every flat shape with straight sides can be cut into triangles using only its own corners. In space you would like to cut a solid with flat faces into pyramids with triangular bases, again using only its corners. The Schönhardt polyhedron shows that this can fail.

Take a prism with triangles on top and bottom, twist the top a bit, and push each side face in along a crease. Now every choice of four corners gives a pyramid that pokes out of the solid. If you add one new corner in the middle, you can cut it into eight pyramids, one per face.

## The idea

**Construction.** Let $a_1 a_2 a_3$ be a triangle in the plane $z = 0$ and $b_1 b_2 b_3$ its copy in the plane $z = h$, rotated about the vertical axis through the center by a small angle. With indices mod 3, the polyhedron $P$ has the 8 faces

- the bottom $a_1 a_2 a_3$ and the top $b_1 b_2 b_3$,
- for each $i$, the two triangles $a_i a_{i+1} b_{i+1}$ and $a_i b_{i+1} b_i$, which share the **fold edge** $a_i b_{i+1}$.

The twist is chosen so that the fold edges are reflex: each side quadrilateral $a_i a_{i+1} b_{i+1} b_i$ is bent inward along $a_i b_{i+1}$. Then the other diagonals $a_{i+1} b_i$ are edges of the convex hull of the six points, and $P$ is the hull with three thin tetrahedra $a_i a_{i+1} b_{i+1} b_i$ removed.

**Why there is no tetrahedralization.** Among the 6 vertices there are $\binom{6}{2} = 15$ pairs. Twelve are edges of $P$ (by Euler's formula, $E = V + F - 2 = 12$). The other three, $a_2 b_1$, $a_3 b_2$, $a_1 b_3$, are segments whose interiors lie outside $P$, in the removed tetrahedra. These three pairs form a perfect matching of the 6 vertices: each vertex is in exactly one of them. A set of 4 vertices contains at most one vertex from each pair only if it has at most 3 vertices, so every set of 4 vertices contains both ends of some exterior pair. Hence every tetrahedron spanned by vertices of $P$ has an edge that leaves $P$, so it is not contained in $P$, and $P$ has no tetrahedralization without Steiner points.

**With one Steiner point.** $P$ is star-shaped: a point $c$ on the axis at mid-height lies strictly on the inner side of all 8 face planes. Joining $c$ to every face gives a tetrahedralization of $P$ with 8 tetrahedra and one Steiner point.

**Generalizations.** Rambau showed that the twisted prism over any convex $n$-gon, folded the same way, has no tetrahedralization. Ruppert and Seidel used Schönhardt-like gadgets to prove that deciding whether a polyhedron has a tetrahedralization without Steiner points is NP-complete. Chazelle's polyhedra, a box with parallel notches cut into its top face and crossing notches cut into its bottom face, need $\Omega(n^2)$ Steiner points.

## Examples

- **Exact coordinates.** Take $a_1 = (6, 0, 0)$, $a_2 = (-3, 5, 0)$, $a_3 = (-3, -5, 0)$, and rotate by the angle with cosine $4/5$ and sine $3/5$, about $36.87°$, lifting to $z = 6$: $b_1 = (24/5, 18/5, 6)$, $b_2 = (-27/5, 11/5, 6)$, $b_3 = (3/5, -29/5, 6)$. Exact computation of the convex hull of the six points gives 8 facets, whose side diagonals are $a_2 b_1$, $a_3 b_2$, $a_1 b_3$. The Schönhardt polyhedron uses the fold edges $a_1 b_2$, $a_2 b_3$, $a_3 b_1$ instead. The midpoints of the hull diagonals lie outside it, and the point $(0, 0, 3)$ lies strictly inside all 8 face planes.
- **The untwisted prism.** Without the twist the side faces are flat squares, and the prism has tetrahedralizations into 3 tetrahedra, so the twist is essential.
- **Folding the other way.** Folding each side along the hull diagonal $a_{i+1} b_i$ instead gives the convex hull itself, which is convex and has tetrahedralizations.
- **The plane.** A polygon with a reflex vertex can always be triangulated, by the [two ears theorem](/two-ears-theorem/); there is no planar Schönhardt polygon.

## Where it is used

- **Lower bounds for meshing.** It is the basic example showing that three-dimensional mesh generators must be allowed to add Steiner points, and that boundary recovery can fail without them.
- **Complexity of tetrahedralization.** It is the gadget in the NP-completeness proof of Ruppert and Seidel, and in hardness proofs for related problems on polyhedra.
- **Constrained Delaunay tetrahedralization.** A Schönhardt polyhedron given as input has no constrained Delaunay tetrahedralization, which is why existence needs conditions such as Shewchuk's edge protection; see [tetrahedralization](/tetrahedralization/).
- **Teaching.** It is the standard picture for the difference between triangulating in two and three dimensions.

## References
