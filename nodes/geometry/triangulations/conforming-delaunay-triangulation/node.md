---
tag: 5GN4W6
kind: concept
slug: conforming-delaunay-triangulation
name: Conforming Delaunay triangulation
aliases:
- Conforming Delaunay
- conforming Delaunay mesh
area: geometry/triangulations
level: research
summary: Delaunay triangulation that contains every input segment, possibly after adding Steiner points.
prereqs: [delaunay-triangulation, steiner-points, constrained-triangulation]
see_also: [constrained-delaunay-triangulation, delaunay-refinement, ruppert-algorithm, mesh-generation, local-delaunay-criterion, in-circle-test, tetrahedralization, chew-second-algorithm]
sources:
  - paper: "Herbert Edelsbrunner and Tiow Seng Tan, An upper bound for conforming Delaunay triangulations, Discrete and Computational Geometry 10(2), 197 to 213 (1993)"
    locator: O(m^2 n) Steiner points always suffice, and Ω(mn) are sometimes needed
  - paper: "Michael Murphy, David M. Mount and Carl W. Gable, A point-placement strategy for conforming Delaunay tetrahedralization, International Journal of Computational Geometry and Applications 11(6), 669 to 682 (2001)"
    locator: the first algorithm for conforming Delaunay tetrahedralizations of three-dimensional inputs
  - paper: doi:10.1016/S0925-7721(01)00047-5
    title: Jonathan Richard Shewchuk, Delaunay refinement algorithms for triangular mesh generation, Computational Geometry 22(1-3), 21 to 74 (2002)
    locator: Section 3 (conforming Delaunay meshes from Ruppert's algorithm) and the comparison of constrained and conforming meshes
  - paper: doi:10.1006/jagm.1995.1021
    title: Jim Ruppert, A Delaunay refinement algorithm for quality 2-dimensional mesh generation, Journal of Algorithms 18(3), 548 to 585 (1995)
    locator: segment splitting until no subsegment is encroached, which yields a conforming Delaunay triangulation
  - paper: "Marshall Bern and David Eppstein, Mesh generation and optimal triangulation, in Computing in Euclidean Geometry, second edition, World Scientific, 47 to 123 (1995)"
    locator: the section on conforming Delaunay triangulations (pages to be checked)
---

A conforming Delaunay triangulation of a planar straight-line graph is a [Delaunay triangulation](/delaunay-triangulation/) of the input vertices plus some [Steiner points](/steiner-points/), chosen so that every input segment is a union of edges of the triangulation. The Delaunay triangulation of the vertices alone may miss a segment; splitting the segment by points on it, and sometimes adding points near it, eventually makes every piece a Delaunay edge. The result is a true Delaunay triangulation, with all of its properties, of a larger point set. It differs from the [constrained Delaunay triangulation](/constrained-delaunay-triangulation/), which keeps the segments without new points but is only Delaunay with respect to visibility. A polynomial number of Steiner points always suffices in the plane, but the gap between the known lower and upper bounds is open.

## In plain words

You have points and some lines between them that must appear in the mesh. The usual best mesh of the points, the Delaunay one, may cut across one of your lines. One fix is to add new points along the line. Short pieces of a line are much more likely to show up in the Delaunay mesh than one long piece, so after enough new points every piece is in the mesh.

The result is an honest Delaunay mesh of the old and new points together, which is what some methods need. The question is how many new points are needed, and nobody knows the exact answer.

## The idea

**Definition.** Let $G$ be a planar straight-line graph with vertex set $V$ ($n$ vertices) and segment set $E$ ($m$ segments). A **conforming Delaunay triangulation** of $G$ is a Delaunay triangulation $D$ of a point set $V \cup S$, where $S$ is a finite set of Steiner points, such that every segment of $E$ is a union of edges of $D$. Points of $S$ may lie on the segments or anywhere else.

**When a segment is present.** An edge $ab$ is in the Delaunay triangulation of a point set whenever its **diametral circle**, the circle with $ab$ as diameter, has no point of the set inside or on it except $a$ and $b$. This sufficient condition is local and easy to reach: if a point $p$ lies in the diametral circle of a segment, split the segment at its midpoint. The two halves have diametral circles of half the radius, which $p$ may avoid. Splitting stops once no point is in any diametral circle. This is the segment step of [Ruppert's algorithm](/ruppert-algorithm/), and its output with no bad-triangle step is a conforming Delaunay triangulation.

**The difficulty.** New points on one segment can enter the diametral circles of other segments, which then split, and their points act on the first one. Near two segments that meet at a small angle this can go on very long, so plain midpoint splitting gives no polynomial bound in general. Edelsbrunner and Tan placed Steiner points more cleverly and proved that $O(m^2 n)$ points always suffice. Edelsbrunner and Tan also gave inputs that need $\Omega(mn)$ points; closing the gap is open.

**Constrained versus conforming.**

| | constrained Delaunay | conforming Delaunay |
|---|---|---|
| vertices | the input only | the input plus Steiner points |
| criterion | empty circumcircle among visible vertices | empty circumcircle among all vertices |
| segments | edges | unions of edges |
| size | $O(n)$ triangles | polynomial but can be $\Omega(mn)$ |
| uses | fewest points, exact boundary | Voronoi-based methods, finite volumes |

**Three dimensions.** For a piecewise linear complex in space, a conforming Delaunay tetrahedralization always exists; Murphy, Mount and Gable gave the first algorithm, and later algorithms by Cohen-Steiner, de Verdière and Yvinec, and by Cheng and Poon, improved the number of points. No polynomial bound is known in space.

## Examples

- **A segment missing from the Delaunay triangulation.** For $a = (0,0)$, $b = (4,0)$, $c = (2,1)$, $d = (2,-1)$ and the segment $ab$, the point $c$ is inside the diametral circle of $ab$ (it lies at distance 1 from the center $(2,0)$, and the radius is 2), and $d$ is inside the circle through $a$, $b$, $c$. So the Delaunay triangulation uses $cd$ and misses $ab$. Adding the midpoint $(2,0)$ splits $ab$ into two halves whose diametral circles, of radius 1 around $(1,0)$ and $(3,0)$, contain neither $c$ nor $d$, since both are at distance $\sqrt{2}$ from each center. The Delaunay triangulation of the five points has four triangles and contains both halves.
- **A segment already present.** If no other vertex lies in the closed diametral circle of a segment, no Steiner point is needed for it.
- **Two segments at a small angle.** Segments from $(0,0)$ to $(10,0)$ and to $(10,1)$ meet at about $5.7°$. A point placed on one of them near the apex lies in the diametral circle of the other near the apex, so midpoint splitting near the apex continues until the pieces are short compared to their distance, many levels down.
- **A conforming triangulation that is not constrained Delaunay.** The output of the first example is not the constrained Delaunay triangulation of the input, which has only the four input vertices and the two triangles $abc$ and $abd$.

## Where it is used

- **Quality mesh generation.** [Ruppert's algorithm](/ruppert-algorithm/) produces conforming Delaunay meshes; its output is Delaunay in the plain sense, so circumcenters of triangles at the boundary lie inside the domain.
- **Voronoi-based methods.** Finite volume methods use the Voronoi cells dual to a Delaunay mesh as control volumes, and need the mesh to be truly Delaunay so that each cell contains its vertex and boundary cells are cut correctly.
- **Interpolation and surface reconstruction.** A conforming Delaunay triangulation of a terrain with break lines keeps the break lines and the good angles of the Delaunay triangulation.
- **Three-dimensional meshing.** Boundary recovery by conforming Delaunay tetrahedralization is an alternative to constrained Delaunay tetrahedralization, which may not exist; see [tetrahedralization](/tetrahedralization/).

## References
