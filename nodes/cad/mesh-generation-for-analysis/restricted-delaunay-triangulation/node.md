---
tag: Y76ET2
kind: definition
slug: restricted-delaunay-triangulation
name: Restricted Delaunay triangulation
aliases:
- restricted Delaunay complex
area: cad/mesh-generation-for-analysis
level: advanced
summary: The subcomplex of a 3D Delaunay triangulation of samples whose dual Voronoi faces meet a surface, which is homeomorphic to the surface for dense samples.
prereqs: [delaunay-triangulation, voronoi-diagram, medial-axis]
see_also: [delaunay-surface-meshing, protecting-balls, surface-reconstruction, chew-second-algorithm, implicit-surface, power-diagram, tetrahedral-delaunay-refinement, sliver-tetrahedron]
sources:
  - paper: doi:10.1142/S0218195997000223
    title: Herbert Edelsbrunner and Nimish R. Shah, Triangulating topological spaces, International Journal of Computational Geometry and Applications 7(4), 1997, 365 to 378
    locator: the restricted Delaunay complex and the closed ball property; the theorem that the complex is homeomorphic to the space (the topological ball theorem) (general locator)
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2013
    locator: Chapter 12 (smooth surfaces, the local feature size and epsilon-samples, pages 261 to 286), Chapter 13 (restricted Delaunay triangulations of surface samples and the topological ball theorem, pages 287 to 316)
  - paper: doi:10.1016/j.gmod.2005.01.004
    title: Jean-Daniel Boissonnat and Steve Oudot, Provably good sampling and meshing of surfaces, Graphical Models 67(5), 2005, 405 to 451
    locator: Section 2.1 (the restricted Delaunay triangulation by facets and surface Delaunay balls), Definitions 2.1 and 2.2 (epsilon-sample, loose epsilon-sample), Theorem 4.4 (ambient isotopy for epsilon at most 0.091), Theorem 4.5 (Hausdorff distance), Figure 1 (an empty restricted triangulation on a torus)
  - paper: doi:10.1007/PL00009475
    title: Nina Amenta and Marshall Bern, Surface reconstruction by Voronoi filtering, Discrete and Computational Geometry 22(4), 1999, 481 to 504
    locator: the epsilon-sample, and Theorem 2, the closed ball property for epsilon below 0.1 (as quoted in the proof of Lemma 2.3 of Boissonnat and Oudot)
  - book: isbn:9780521863704
    title: Tamal K. Dey, Curve and Surface Reconstruction, Algorithms with Mathematical Analysis, Cambridge University Press, 2007
    locator: the restricted Delaunay triangulation of a 0.18-sample is homeomorphic to the surface (general locator, as reported by Shewchuk 2026)
  - paper: doi:10.48550/arXiv.2603.19826
    title: Jonathan Richard Shewchuk, Better sampling bounds for restricted Delaunay triangulations and a star-shaped property for restricted Voronoi cells, arXiv 2603.19826, 2026
    locator: Theorem 21 (homeomorphism for a 0.3245-sample with no Voronoi vertex on the surface), the introduction (the earlier bounds 0.18 and 0.09 and Bjerkevik's counterexamples at 0.72), the generic intersection conditions of the topological ball theorem
---

The restricted Delaunay triangulation of a point set $S$ with respect to a surface $\Sigma$ is the part of the three-dimensional [Delaunay triangulation](/delaunay-triangulation/) of $S$ that the surface "sees": the simplices whose dual [Voronoi](/voronoi-diagram/) faces meet $\Sigma$. When $S$ is a dense enough sample of a smooth closed surface, it is a triangulated surface homeomorphic to $\Sigma$, close to it, and built from Delaunay triangles. That makes it the standard target of [Delaunay surface meshing](/delaunay-surface-meshing/) and of provable [surface reconstruction](/surface-reconstruction/). The topological ball theorem of Edelsbrunner and Shah gives the exact condition for the homeomorphism. Sampling theorems turn it into a density bound with an explicit constant, $0.091$ in Boissonnat and Oudot's version, and these constants are far smaller than the densities that work in practice.

## Definition

Let $S \subset \mathbb{R}^3$ be a finite point set in general position, $\mathrm{Del}\,S$ its Delaunay triangulation and $\mathrm{Vor}\,S$ its Voronoi diagram, with closed cells $V_p$. A simplex $\sigma$ of $\mathrm{Del}\,S$ with vertex set $T$ has the dual Voronoi face $\sigma^* = \bigcap_{p \in T} V_p$: a cell for a vertex, a polygon for an edge, an edge for a triangle and a vertex for a tetrahedron. Let $\Sigma$ be a subset of $\mathbb{R}^3$, in this page a compact smooth surface without boundary.

**Definition (Edelsbrunner and Shah).** The *restricted Delaunay complex* is
$$\mathrm{Del}|_\Sigma S = \{\sigma \in \mathrm{Del}\,S : \sigma^* \cap \Sigma \neq \emptyset\}.$$
It is a subcomplex of $\mathrm{Del}\,S$, because a face of $\sigma$ has a larger dual face. Its simplices are the *restricted Delaunay* vertices, edges, triangles and tetrahedra. The sets $V_p \cap \Sigma$ are the *restricted Voronoi cells*.

**The version used for surface meshing (Boissonnat and Oudot).** Mesh generators keep only the triangles of $\mathrm{Del}\,S$ whose dual Voronoi edge meets $\Sigma$, with their edges and vertices, and drop the vertices and edges with no such triangle. For a triangle $abc$ of this kind and a point $c_0 \in \Sigma \cap (abc)^*$, the closed ball centered at $c_0$ with $a, b, c$ on its boundary is a *surface Delaunay ball* of $abc$. The two versions agree when the theorem below applies, because a complex whose underlying space is a surface without boundary has no vertex or edge outside its triangles.

**Local feature size and samples.** The *local feature size* $\mathrm{lfs}(x)$ of a point $x$ is its distance to the [medial axis](/medial-axis/) of $\Sigma$, the closure of the set of points with two or more nearest points on $\Sigma$. It is $1$-Lipschitz, and positive on a smooth closed surface. A finite $S \subset \Sigma$ is an *$\varepsilon$-sample* (Amenta and Bern) if every $x \in \Sigma$ has a point of $S$ within distance $\varepsilon\, \mathrm{lfs}(x)$. Boissonnat and Oudot's *loose $\varepsilon$-sample* asks this only at the points of $\Sigma$ on Voronoi edges, the centers of the surface Delaunay balls, plus a vertex on every component of $\Sigma$; it is checkable from the mesh.

**Proposition (proved here).** (a) Three points $a, b, c$ of $S$ span a restricted Delaunay triangle exactly when some closed ball centered at a point of $\Sigma$ has $a, b, c$ on its boundary and no point of $S$ in its interior. (b) If $S \subset \Sigma$ is an $\varepsilon$-sample, every surface Delaunay ball $B(c_0, r)$ has $r \le \varepsilon\, \mathrm{lfs}(c_0)$.

*Proof.* (a) A point $x$ lies on the Voronoi face $(abc)^*$ exactly when $|x - a| = |x - b| = |x - c| \le |x - q|$ for every $q \in S$, that is, when the ball $B(x, |x - a|)$ has $a, b, c$ on its boundary and no point of $S$ in its interior. Such a ball also shows that $abc$ is a Delaunay triangle. So a point $x \in \Sigma$ with this property exists exactly when $(abc)^* \cap \Sigma \ne \emptyset$. (b) The ball $B(c_0, r)$ has no point of $S$ inside, so $r$ is the distance from $c_0$ to $S$, which is at most $\varepsilon\, \mathrm{lfs}(c_0)$ since $c_0 \in \Sigma$. $\blacksquare$

Part (a) is the brute-force test that the tests of the [Delaunay surface meshing](/delaunay-surface-meshing/) implementation use.

**Topological ball theorem (Edelsbrunner and Shah, 1997; cited).** Let $\Sigma \subset \mathbb{R}^3$ be a compact $2$-manifold without boundary and $S$ a finite point set. Suppose $\Sigma$ meets the faces of $\mathrm{Vor}\,S$ generically (no Voronoi vertex on $\Sigma$, and $\Sigma$ tangent to no Voronoi edge or polygon), and $\mathrm{Vor}\,S$ has the *closed ball property*: every Voronoi face of dimension $k$ that meets $\Sigma$ meets it in a closed topological $(k-1)$-ball. Then the underlying space of $\mathrm{Del}|_\Sigma S$ is homeomorphic to $\Sigma$.

So a restricted Voronoi cell must be a disk, the intersection of $\Sigma$ with a Voronoi polygon a single arc, and with a Voronoi edge a single point. The proof builds the homeomorphism from a barycentric subdivision and is in Edelsbrunner and Shah, and in Chapter 13 of Cheng, Dey and Shewchuk; it is not repeated here.

**Sampling theorems (cited, with their constants).**

- Amenta and Bern: for an $\varepsilon$-sample with $\varepsilon < 0.1$ the closed ball property holds, so the theorem applies.
- Boissonnat and Oudot, Theorem 4.4: for a loose $\varepsilon$-sample of a smooth closed surface with $\varepsilon \le \varepsilon_0 \approx 0.091$, the projection to the nearest point of $\Sigma$ is a homeomorphism from $\mathrm{Del}|_\Sigma S$ to $\Sigma$, and the two are ambient isotopic. Theorem 4.5: their Hausdorff distance is at most $4.5\, \varepsilon^2 \sup_\Sigma \mathrm{lfs}$.
- Dey (2007): homeomorphism for a $0.18$-sample.
- Shewchuk (2026), Theorem 21: homeomorphism for an $\varepsilon$-sample with $\varepsilon \le 0.3245$ when no Voronoi vertex lies on $\Sigma$. He also reports Bjerkevik's counterexamples, which show that no theorem of this kind can hold for $0.72$-samples.

These are proved bounds with explicit constants, and they are worst-case. Typical samples are homeomorphic at much coarser densities: the four-point example below is a $1.155$-sample, more than ten times coarser than $0.091$, and its restricted Delaunay triangulation is already a sphere.

## Examples and non-examples

**Four points on a sphere.** Let $\Sigma$ be the unit sphere, so $\mathrm{lfs} = 1$ everywhere (the medial axis is the center), and let $S$ be the four vertices of a regular tetrahedron inscribed in it. $\mathrm{Del}\,S$ is that one tetrahedron. Its Voronoi vertex is the center, which is not on $\Sigma$, so the tetrahedron is not restricted. Each Voronoi edge is a ray from the center through the center of a face, and it crosses the sphere once, so all four triangles are restricted. Each Voronoi polygon is a planar wedge and cuts the sphere in an arc, and each cell is a cone that cuts it in a disk. The closed ball property holds, and $\mathrm{Del}|_\Sigma S$ is the boundary of the tetrahedron, a sphere. The point of $\Sigma$ farthest from $S$ is opposite a vertex, at distance $\sqrt{4/3} \approx 1.155$, so this is a $1.155$-sample.

| Voronoi face | Dimension | Meets the sphere in | Dual simplex | Restricted |
|---|---|---|---|---|
| the center | 0 | nothing | the tetrahedron | no |
| 4 rays | 1 | one point each | the 4 triangles | yes |
| 6 wedges | 2 | one arc each | the 6 edges | yes |
| 4 cones | 3 | one disk each | the 4 vertices | yes |

**Points on a circle in the plane.** The same definition works for a curve $\Sigma$ in $\mathbb{R}^2$: an edge $pq$ of the Delaunay triangulation is restricted when its dual Voronoi edge crosses $\Sigma$. For $n \ge 3$ points spread around a circle, the restricted edges are the edges between neighbors along the circle, the inscribed polygon.

**Two poles: the closed ball property fails.** Let $S$ be the north and south poles of the unit sphere. $\mathrm{Vor}\,S$ has one polygon, the plane $z = 0$, which meets the sphere in a circle, not an arc. Edelsbrunner and Shah's complex is the single edge between the poles, which is not a surface; the meshing version has no triangle at all.

**An empty restricted triangulation.** Boissonnat and Oudot's Figure 1 places four points on a torus so that no Voronoi edge meets the torus. Then $\mathrm{Del}|_\Sigma S$ has no triangle, and the condition "every surface Delaunay ball is small" holds vacuously; this is why the loose $\varepsilon$-sample also asks for a vertex on every component.

**A degenerate case.** If a Voronoi vertex lies on $\Sigma$, its tetrahedron is restricted and $\Sigma$ meets the faces around it non-generically. Five or more cospherical points of $S$, as for the vertices of a cube, give a degenerate $\mathrm{Del}\,S$; both cases are excluded by general position.

## Related definitions

- [Delaunay surface meshing](/delaunay-surface-meshing/): inserts centers of large surface Delaunay balls until the sample is a loose $\varepsilon$-sample, which makes the restricted Delaunay triangulation a correct mesh.
- [Protecting balls](/protecting-balls/): weighted points along sharp edges, so that the restricted *weighted* Delaunay triangulation of a piecewise smooth surface keeps its edges.
- [Chew's second algorithm](/chew-second-algorithm/): it comes from Chew's 1993 paper on meshing curved surfaces, and Boissonnat and Oudot say their surface algorithm derives from the surface mesher of that paper.
- [Surface reconstruction](/surface-reconstruction/): Amenta and Bern's crust and its successors select triangles from $\mathrm{Del}\,S$ of an unknown surface; the restricted Delaunay triangulation is what they aim at.
- [Tetrahedral Delaunay refinement](/tetrahedral-delaunay-refinement/): meshes the volume inside a restricted Delaunay surface. Its tetrahedra satisfy only a radius-edge bound, which does not remove [slivers](/sliver-tetrahedron/).
- [Power diagram](/power-diagram/): replacing Voronoi by power cells gives the restricted weighted Delaunay triangulation.

## References
