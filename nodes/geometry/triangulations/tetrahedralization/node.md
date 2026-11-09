---
tag: 4SNNKV
kind: definition
slug: tetrahedralization
name: Tetrahedralization
aliases:
- 3D triangulation
- Tetrahedral mesh
- triangulation in three dimensions
area: geometry/triangulations
level: advanced
summary: Subdivision of a three-dimensional region or point set into tetrahedra.
prereqs: [triangulation, triangulation-of-point-set, convex-hull]
see_also: [schonhardt-polyhedron, steiner-points, delaunay-triangulation, delaunay-refinement, mesh-generation, regular-triangulation, flip-graph, minimum-steiner-triangulation]
sources:
  - book: isbn:9783642129704
    title: Jesús A. De Loera, Jörg Rambau and Francisco Santos, Triangulations, Structures for Algorithms and Applications, Springer, 2010
    locator: Chapter 2 (triangulations of point configurations in any dimension) and Chapter 8 (sizes of triangulations of the cube and of 3-polytopes; chapter numbers to be checked)
  - paper: "Erich Schönhardt, Über die Zerlegung von Dreieckspolyedern in Tetraeder, Mathematische Annalen 98, 309 to 312 (1928)"
    locator: the twisted prism with no tetrahedralization
  - paper: "Jim Ruppert and Raimund Seidel, On the difficulty of triangulating three-dimensional nonconvex polyhedra, Discrete and Computational Geometry 7(3), 227 to 253 (1992)"
    locator: NP-completeness of deciding whether a polyhedron has a tetrahedralization without Steiner points
  - paper: "Bernard Chazelle, Convex partitions of polyhedra, a lower bound and worst-case optimal algorithm, SIAM Journal on Computing 13(3), 488 to 507 (1984)"
    locator: polyhedra that need Ω(n^2) tetrahedra
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: Chapters 4 and 5 (Delaunay and constrained Delaunay tetrahedralizations; ISBN to be checked)
---

A tetrahedralization is the three-dimensional analogue of a [triangulation](/triangulation/): a subdivision of a region of space into tetrahedra that meet face to face. For a finite point set it covers the convex hull and uses the points as vertices; for a polyhedron it covers the polyhedron and uses its vertices, plus [Steiner points](/steiner-points/) if allowed. Much of what holds in the plane fails in space: the number of tetrahedra is not fixed by the input, some polyhedra have no tetrahedralization without extra vertices, and the number of tetrahedra can grow quadratically in the number of points.

## Definition

Let $S$ be a finite set of points in $\mathbb{R}^3$, not all on one plane. A **tetrahedralization of $S$** is a finite set $T$ of tetrahedra such that:

1. the corners of every tetrahedron are points of $S$, and every tetrahedron has positive volume;
2. any two tetrahedra of $T$ intersect in a common face (a triangle, an edge, a vertex) or not at all;
3. the union of the tetrahedra is the convex hull $\mathrm{conv}(S)$;
4. every point of $S$ is a vertex of some tetrahedron.

A **tetrahedralization of a polyhedron** $P$ is a set of tetrahedra with the same property 2 whose union is $P$, whose vertices are vertices of $P$, and in which every boundary face of $P$ is a union of triangles of the tetrahedra. If vertices outside the vertex set are allowed, they are Steiner points, and the result is a **Steiner tetrahedralization**. A **tetrahedral mesh** is a Steiner tetrahedralization used for computation, usually with bounds on the shape of the tetrahedra.

The same definition in $\mathbb{R}^d$ with simplices gives a triangulation of a point configuration in dimension $d$. Some authors (De Loera, Rambau and Santos) drop condition 4.

**Size.** With $n$ points, the number $t$ of tetrahedra is not determined by $n$. Euler's relation $V - E + F - t = 1$ for a tetrahedralization of a convex region, together with $4t = 2F_{\mathrm{int}} + F_{\mathrm{hull}}$, gives $t = E - n + 1 - F_{\mathrm{hull}}/2$, so the number of tetrahedra moves with the number $E$ of edges. Since $E \le \binom{n}{2}$, every tetrahedralization of $n$ points has $O(n^2)$ tetrahedra, and this is tight: $p$ points on one line and $q$ on a skew line have a unique tetrahedralization, with $(p - 1)(q - 1)$ tetrahedra.

## Examples and non-examples

- **A tetrahedron.** Four points in general position have exactly one tetrahedralization, with 1 tetrahedron.
- **Five points in convex position.** For a triangular bipyramid, with an edge from apex to apex through the shared triangle, there are two tetrahedralizations: 2 tetrahedra glued along the middle triangle, or 3 tetrahedra around the axis edge. They differ by a 2-3 flip, and they have different sizes, unlike in the plane.
- **The cube.** The unit cube has tetrahedralizations into 5 tetrahedra (a central regular tetrahedron and four corners) and into 6 tetrahedra (all around a main diagonal), and no tetrahedralization into fewer than 5.
- **The Delaunay tetrahedralization.** For points with no five on a common sphere, the tetrahedra whose circumscribed spheres are empty form a tetrahedralization; see [Delaunay triangulation](/delaunay-triangulation/). It can have $\Theta(n^2)$ tetrahedra, as for points on two skew lines.
- **Non-example: the Schönhardt polyhedron.** The [Schönhardt polyhedron](/schonhardt-polyhedron/), a triangular prism with its top twisted, has no tetrahedralization: every tetrahedron on its 6 vertices sticks out of it. It does have a Steiner tetrahedralization.
- **Non-example: missing face condition.** Two tetrahedra that share only part of a triangle, for example a big tetrahedron next to two small ones splitting its face, form a subdivision into tetrahedra but not a tetrahedralization, because condition 2 fails.

## Related definitions

- **[Triangulation](/triangulation/)** is the planar case; there the number of triangles is $2n - h - 2$ for every triangulation.
- **Flips in space.** The 2-3 and 3-2 flips, and the 4-4 flip for degenerate input, are the bistellar flips in dimension 3; the flip graph of a point set in $\mathbb{R}^3$ is not known to be connected. See [flip graph](/flip-graph/).
- **[Regular triangulations](/regular-triangulation/)** are the projections of lower hulls of lifted points; the Delaunay tetrahedralization is the case with lifting to the paraboloid.
- **Constrained Delaunay tetrahedralization.** A tetrahedralization that respects given faces; it exists when every input edge is strongly Delaunay (Shewchuk), but not in general.
- **Slivers.** Tetrahedra with four nearly coplanar vertices spread around a circle; their circumradius to shortest edge ratio is small, so [Delaunay refinement](/delaunay-refinement/) does not remove them.
- **Polyhedra needing Steiner points.** Deciding whether a polyhedron has a tetrahedralization without Steiner points is NP-complete (Ruppert and Seidel). Chazelle's polyhedra need $\Omega(n^2)$ convex pieces, hence $\Omega(n^2)$ tetrahedra and Steiner points; see [minimum Steiner triangulation](/minimum-steiner-triangulation/).

## References
