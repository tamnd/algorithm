---
tag: HXWF5C
kind: definition
slug: constrained-delaunay-tetrahedralization
name: Constrained Delaunay tetrahedralization
aliases:
- constrained Delaunay tetrahedral mesh
area: cad/mesh-generation-for-analysis
level: advanced
summary: A tetrahedralization that contains given facets and is Delaunay except where they block visibility. Shewchuk showed it exists when every segment is strongly Delaunay.
prereqs: [constrained-delaunay-triangulation, tetrahedralization, schonhardt-polyhedron]
see_also: [boundary-recovery, conforming-delaunay-triangulation, steiner-points, tetrahedral-delaunay-refinement, regular-triangulation, delaunay-triangulation, sliver-tetrahedron, np-complete]
sources:
  - url: https://people.eecs.berkeley.edu/~jrs/papers/cdtbasic.pdf
    title: Jonathan Richard Shewchuk, Constrained Delaunay tetrahedralizations and provably good boundary recovery, Proceedings of the 11th International Meshing Roundtable, 2002, 193 to 204
    locator: Section 2 (PLCs, the triangulation domain, visibility, Delaunay and strongly Delaunay simplices, constrained Delaunay simplices, the CDT, Figure 9 with a PLC that has no CDT), Section 3 (edge protection, Theorem 1, Schönhardt's polyhedron with cospherical vertices, cube diagonals, grazeable segments and weak edge protection), Section 4 (testing edge protection), Section 5 (the edge protection algorithm, Theorems 2 and 3), Section 6 (gift wrapping and sweep running times)
  - paper: doi:10.1007/s00454-008-9060-3
    title: Jonathan Richard Shewchuk, General-dimensional constrained Delaunay and constrained regular triangulations, I, combinatorial properties, Discrete and Computational Geometry 39(1-3), 2008, 580 to 637
    locator: Section 1.1 (Schönhardt, Ruppert and Seidel, ridge-protected and weakly ridge-protected PLCs), Definition 19 and Corollary 20 (a generic PLC has at most one CDT), Theorem 26 (the CDT Theorem for generic PLCs), the remark before Section 6 (deciding whether a nongeneric three-dimensional PLC has a CDT is NP-complete, citing Grislain and Shewchuk 2003), Section 6 (weight perturbation removes genericity)
  - paper: doi:10.1145/276884.276893
    title: Jonathan Richard Shewchuk, A condition guaranteeing the existence of higher-dimensional constrained Delaunay triangulations, Proceedings of the 14th Annual Symposium on Computational Geometry, 1998, 76 to 85
    locator: the first statement and proof of the CDT Theorem for edge-protected PLCs (general locator)
  - paper: doi:10.1007/BF02187840
    title: Jim Ruppert and Raimund Seidel, On the difficulty of triangulating three-dimensional nonconvex polyhedra, Discrete and Computational Geometry 7(3), 1992, 227 to 253
    locator: the NP-completeness of deciding whether a three-dimensional polyhedron can be tetrahedralized without new vertices (general locator)
  - paper: doi:10.1007/BF01451597
    title: Erich Schönhardt, Über die Zerlegung von Dreieckspolyedern in Tetraeder, Mathematische Annalen 98, 1928, 309 to 312
    locator: the twisted triangular prism that has no tetrahedralization (general locator)
  - paper: doi:10.1002/nme.3016
    title: Hang Si and Klaus Gärtner, 3D boundary recovery by constrained Delaunay tetrahedralization, International Journal for Numerical Methods in Engineering 85(11), 2011, 1341 to 1364
    locator: Theorem 5 (a PLC whose segments are all Delaunay edges of vertices in general position has a unique CDT), Section 6 and Table I (Steiner points on the order of the input size)
  - url: https://wias-berlin.de/software/tetgen/1.5/doc/manual/manual.pdf
    title: Hang Si, TetGen, a quality tetrahedral mesh generator and a 3D Delaunay triangulator, User's Manual, version 1.6, WIAS Berlin, 2020
    locator: the sections on constrained tetrahedralizations and constrained Delaunay tetrahedralizations of PLCs, and on quality tetrahedral meshes (the radius-edge ratio does not remove slivers)
---

A constrained Delaunay tetrahedralization (CDT) is the three-dimensional version of the [constrained Delaunay triangulation](/constrained-delaunay-triangulation/). The input is a piecewise linear complex (PLC): vertices, segments and polygonal facets. A CDT uses exactly the input vertices, contains every segment and facet as a union of its edges and triangles, and is as Delaunay as the facets allow: the empty-sphere condition only counts vertices that are visible through no facet. In the plane a constrained Delaunay triangulation always exists. In space a [tetrahedralization](/tetrahedralization/) without new vertices may not exist at all, as [Schönhardt's polyhedron](/schonhardt-polyhedron/) shows, and deciding whether one exists is NP-complete. Shewchuk's CDT Theorem is an **existence theorem**: if every segment is strongly Delaunay, a CDT exists. It is sufficient, not necessary, and its constants are much worse than what is measured. That theorem is the basis of the [boundary recovery](/boundary-recovery/) used by TetGen.

## Definition

**Piecewise linear complex.** A PLC $X$ in $\mathbb{R}^3$ is a finite set of vertices, segments and facets. Each segment is a closed line segment with its two endpoints in $X$. Each facet is a planar polygon, possibly nonconvex and with holes, whose boundary is a union of segments of $X$. Two members of $X$ meet only in a shared vertex or segment, or in a union of these. The *triangulation domain* is the region to be tetrahedralized, for example the convex hull or the inside of a closed surface. It must be bounded by facets of $X$.

**Visibility.** In Shewchuk's words, "the visibility between two points p and q is occluded if there is a constraining facet f of X such that p and q lie on opposite sides of the plane that includes f, and the line segment pq intersects f." If $p$ or $q$ lies in the plane of $f$, then $f$ does not occlude them. "Segments in X do not occlude visibility."

**Delaunay and strongly Delaunay.** A simplex $s$ whose vertices are vertices of $X$ is *Delaunay* if some circumsphere $S$ of $s$ encloses no vertex of $X$ in its interior. It is *strongly Delaunay* if some circumsphere has no vertex of $X$ inside or on it, apart from the vertices of $s$. Every vertex is strongly Delaunay. A strongly Delaunay simplex is an edge, triangle or tetrahedron of every Delaunay tetrahedralization of the vertices. A merely Delaunay one may be missing from some of them when five or more vertices are cospherical.

**Constrained Delaunay simplex.** A simplex $s$ *respects* $X$ if it lies in the triangulation domain and meets every segment and facet of $X$ in a union of faces of $s$. It is *constrained Delaunay* if

- $s$ respects $X$, and
- some circumsphere $S$ of $s$ has no vertex of $X$ inside it that is visible from a point in the relative interior of $s$.

**Definition (Shewchuk).** A *constrained tetrahedralization* of $X$ is a tetrahedralization with the same vertices as $X$, no more and no fewer, whose tetrahedra respect $X$ and cover the triangulation domain. Each facet is then a union of its triangles. A *constrained Delaunay tetrahedralization* of $X$ is a constrained tetrahedralization whose tetrahedra are all constrained Delaunay.

A *conforming constrained Delaunay tetrahedralization* (CCDT) is a CDT of a PLC obtained from $X$ by adding vertices, the [Steiner points](/steiner-points/), usually on its segments. The TetGen manual gives an equivalent local form of the CDT: every triangle of the tetrahedralization that is not part of a facet is locally Delaunay, so the two tetrahedra on its sides pass the in-sphere test against each other.

**Generic PLCs.** $X$ is *generic* if no five vertices lie on a common sphere (for weighted vertices: no five lift to a common non-vertical hyperplane under the [lifting map](/paraboloid-lifting-map/)). A generic PLC has at most one CDT, Corollary 20 of Shewchuk (2008).

**Edge protection.** "A PLC X is edge-protected if every segment in X is strongly Delaunay." A segment is *grazeable* if two consecutive facets around it are separated by an interior angle of 180 degrees or more, measured inside the triangulation domain, or if the segment lies in fewer than two facets. "A three-dimensional PLC X is weakly edge-protected if each grazeable segment in X is strongly Delaunay." In general dimension Shewchuk calls these conditions *ridge-protected* and *weakly ridge-protected*.

**CDT Theorem (Shewchuk 1998 and 2008; cited, existence theorem).** If $X$ is weakly edge-protected, then $X$ has a CDT. In particular, "If X is edge-protected, then X has a CDT" (Theorem 1 of the 2002 paper). The 2008 proof first treats generic PLCs, Theorem 26, and then removes genericity by perturbing the vertex weights, Section 6. When no five vertices are cospherical, gift wrapping finds the CDT of any PLC that has one. The condition of the theorem is only sufficient. Many PLCs whose segments are not strongly Delaunay still have a CDT.

**Hardness (cited).** Ruppert and Seidel (1992) proved that deciding whether a three-dimensional polyhedron can be tetrahedralized without new vertices is NP-complete; Shewchuk (2008) cites it as NP-hard. Grislain and Shewchuk (2003) proved that deciding whether a nongeneric three-dimensional PLC has a CDT is NP-complete, even without weights. For a generic PLC the question takes polynomial time: try to build the CDT.

**Proposition (proved here).** (a) In the cube $[0,1]^3$, each face diagonal is Delaunay but not strongly Delaunay. (b) Schönhardt's polyhedron has no tetrahedralization without new vertices. (c) In no placement of Schönhardt's polyhedron are all three reflex edges strongly Delaunay.

*Proof.* (a) Take the diagonal from $a = (0,0,0)$ to $b = (1,1,0)$. The circumsphere of the cube passes through all eight vertices and has none inside, so the diagonal is Delaunay. A sphere through $a$ and $b$ has its center $c$ on the bisector plane $x + y = 1$. For a point $p$, the sign of $|p - c|^2 - |a - c|^2 = |p|^2 - 2\, c \cdot p$ tells whether $p$ is outside, on or inside the sphere. For $p = (1,0,0)$ it is $1 - 2c_x$, and for $p = (0,1,0)$ it is $1 - 2c_y$. These sum to $2 - 2(c_x + c_y) = 0$, so one of them is at most zero. Every sphere through $a$ and $b$ has $(1,0,0)$ or $(0,1,0)$ inside or on it.

(b) Label the bottom triangle $a_1 a_2 a_3$ and the top triangle $b_1 b_2 b_3$. Of the 15 pairs of vertices, 12 are edges of the polyhedron: 6 triangle edges and 6 side edges. The side edges form a 6-cycle $a_1 b_1 a_2 b_2 a_3 b_3$ between bottom and top, and the 3 remaining pairs $a_i b_{i+1}$, which complete the bipartite graph $K_{3,3}$, have their midpoints outside the polyhedron. Any 4 of the 6 vertices include one of these 3 pairs. Taking 3 from one triangle and 1 from the other includes the outside pair of that single vertex. Taking 2 and 2 without an outside pair would need all 4 bottom-top pairs to be side edges, a 4-cycle inside a 6-cycle, which does not exist. So every candidate tetrahedron has an edge outside the polyhedron.

(c) Make the polyhedron a PLC: its 6 vertices, 12 edges and 8 triangular facets, with the inside as the domain. At a reflex edge the interior angle between its two facets exceeds 180 degrees, so the reflex edge is grazeable. At the other 9 edges it is below 180 degrees, so they are not grazeable. If all three reflex edges were strongly Delaunay, the PLC would be weakly edge-protected and would have a CDT by the CDT Theorem, which is a tetrahedralization without new vertices. That contradicts (b). $\blacksquare$

Shewchuk notes the converse sharpness: any two reflex edges can be strongly Delaunay. And it is not enough for every segment to be Delaunay: with all six vertices on one sphere, every edge and face of Schönhardt's polyhedron is Delaunay, and there is still no tetrahedralization.

**Bounds, with their constants (cited).** Shewchuk's edge protection inserts vertices on the segments until the PLC is edge-protected. Theorem 2 of his 2002 paper: it "creates no segment shorter than one-quarter the local feature size of any point in that segment". Here the local feature size $\mathrm{lfs}(u)$ is the radius of the smallest ball around $u$ that meets two vertices or segments that do not touch each other; facets are ignored. Theorem 3 extends this to every edge of the resulting CCDT: $|e| \ge \mathrm{lfs}(u) \sin(\varphi/2)/2$ when the ends of $e$ lie on two segments that meet at an angle $\varphi < 60$ degrees, and $|e| \ge \mathrm{lfs}(u)/4$ otherwise. No bound on the number of added vertices is known that is polynomial in the input size; Shewchuk writes that this problem "is unsolved". Gift wrapping builds a CDT in $O(n_v n_f n_s)$ time, for $n_v$ vertices, $n_f$ facet triangles and $n_s$ tetrahedra. Shewchuk's sweep takes $O(n_v n_s)$.

**Proved constants and measured ones.** The proved constant $\frac14$ is far below what happens. On the random segment sets in the tests of the [boundary recovery](/boundary-recovery/) implementation, the smallest ratio of a subsegment's length to the local feature size at a point of it was between 0.315 and 0.413 for each set, and 0.663 on its worked example. On six engineering models, Si and Gärtner report that "the number of Steiner points is in the order of the input size". The existence theorem says nothing about tetrahedron shape. A CDT may contain flat tetrahedra, and refining it until every radius-edge ratio is at most 2, as [tetrahedral Delaunay refinement](/tetrahedral-delaunay-refinement/) does, still does not remove slivers: a [sliver tetrahedron](/sliver-tetrahedron/) has a small circumradius-to-shortest-edge ratio and a dihedral angle near 0. TetGen's manual says the same about its own refinement and adds the minimum dihedral angle as a second measure.

## Examples and non-examples

**A PLC with no CDT.** This is Shewchuk's Figure 9 with explicit coordinates. Take $a = (4,0,0)$, $b = (-2,3,0)$, $c = (-2,-3,0)$, $p = (0,0,4)$, $q = (0,0,-4)$, and one segment $pq$, with no facets and the convex hull as the domain. The segment passes through the triangle $abc$ at the origin, so the only constrained tetrahedralization is the three tetrahedra $pqab$, $pqbc$, $pqca$ around it. With no facets, nothing occludes, so constrained Delaunay means Delaunay, and each of the three has the remaining vertex strictly inside its circumsphere:

| Tetrahedron | Circumcenter | $r^2$ | Other vertex | Its squared distance |
|---|---|---|---|---|
| $pqab$ | $(0, -\frac12, 0)$ | $\frac{65}{4}$ | $c$ | $\frac{41}{4}$ |
| $pqbc$ | $(\frac34, 0, 0)$ | $\frac{265}{16}$ | $a$ | $\frac{169}{16}$ |
| $pqca$ | $(0, \frac12, 0)$ | $\frac{65}{4}$ | $b$ | $\frac{41}{4}$ |
| $abcp$ | $(\frac14, 0, \frac14)$ | $\frac{113}{8}$ | $q$ | $\frac{145}{8}$ |
| $abcq$ | $(\frac14, 0, -\frac14)$ | $\frac{113}{8}$ | $p$ | $\frac{145}{8}$ |

The Delaunay tetrahedralization is $abcp$ and $abcq$, which does not contain $pq$. So this PLC has no CDT. Inserting the midpoint $(0,0,0)$ of $pq$ makes both halves strongly Delaunay, which is what edge protection does here, and the new PLC has a CDT by the theorem. With $p = (0,0,1)$ and $q = (0,0,-1)$ instead, $pq$ is strongly Delaunay and the three tetrahedra around it are the CDT.

**Schönhardt's polyhedron.** Twist the top triangle of a triangular prism by 30 degrees, as in the implementation of [boundary recovery](/boundary-recovery/): bottom vertices $(0,100,0)$, $(-87,-50,0)$, $(87,-50,0)$ and top vertices $(-50,87,100)$, $(-50,-87,100)$, $(100,0,100)$. Each square side folds along a reflex diagonal. The three pairs that are not edges have their midpoints outside, so by part (b) there is no tetrahedralization and no CDT. Here two of the three reflex edges are strongly Delaunay, as part (c) allows. One extra vertex at the centroid sees all eight faces and gives a tetrahedralization with 8 tetrahedra. The tests check all of this in exact arithmetic for twists of 10, 30 and 50 degrees, and on 40 random placements they never find all three reflex edges strongly Delaunay.

**The cube.** The 12 edges of $[0,1]^3$ are strongly Delaunay: the sphere with an edge as diameter has the other 6 vertices outside. So the PLC made of the cube's vertices and edges is edge-protected and has a CDT. If the face diagonals are added as segments, part (a) shows they are not strongly Delaunay, and depending on the choice of diagonals a constrained tetrahedralization may not exist. Facets that are whole squares, with no diagonals, are the right input. The CDT then picks compatible diagonals.

**Facets that block the empty sphere.** Let a horizontal square facet separate a vertex just above it from a vertex just below. A tetrahedron on one side may have the vertex on the other side inside its circumsphere and still be constrained Delaunay, because the facet occludes that vertex from the tetrahedron's interior. This is the difference between a CDT and a Delaunay tetrahedralization, and it is why a CDT can contain facets that a Delaunay tetrahedralization would cut.

**Not a CDT: a conforming Delaunay tetrahedralization.** A [conforming Delaunay triangulation](/conforming-delaunay-triangulation/) adds Steiner points until an ordinary Delaunay tetrahedralization contains all segments and facets. It is Delaunay with no visibility exception, but it has more vertices than $X$, usually many more on the facets. A CDT adds none. A CCDT adds them only where segments are not strongly Delaunay.

## Related definitions

- [Constrained Delaunay triangulation](/constrained-delaunay-triangulation/): the planar case, which always exists without new vertices. Each facet of a CDT is triangulated by a two-dimensional CDT of the facet.
- [Boundary recovery](/boundary-recovery/): the step of a mesher that makes a Delaunay tetrahedralization contain the input segments and facets. Edge protection followed by CDT construction is the version with guarantees.
- [Schönhardt's polyhedron](/schonhardt-polyhedron/) and [Steiner points](/steiner-points/): the reason a CDT may not exist, and the fix.
- [Regular triangulation](/regular-triangulation/): Shewchuk's 2008 paper treats constrained regular triangulations of weighted PLCs, and the CDT is the case with equal weights.
- [Tetrahedral Delaunay refinement](/tetrahedral-delaunay-refinement/): starts from a CDT or a CCDT and inserts circumcenters until the radius-edge ratio is at most a bound, which leaves slivers.
- [NP-complete](/np-complete/): the class of both decision problems above.
