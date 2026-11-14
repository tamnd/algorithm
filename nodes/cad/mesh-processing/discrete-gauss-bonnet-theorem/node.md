---
tag: Y8Y7EC
kind: theorem
slug: discrete-gauss-bonnet-theorem
name: Discrete Gauss-Bonnet theorem
aliases:
- Descartes theorem on angle defects
area: cad/mesh-processing
level: core
summary: The angle defects of a closed polyhedral surface sum to 2 pi times its Euler characteristic, so 4 pi for any closed surface of genus zero.
prereqs: [discrete-gaussian-curvature, euler-formula, manifold-mesh]
see_also: [surface-curvature, euler-poincare-formula, cotangent-laplacian, convex-polytope, graph-genus, isotropic-remeshing]
sources:
  - book: isbn:9780387907604
    title: Pasquale Joseph Federico, Descartes on Polyhedra, A Study of the De Solidorum Elementis, Springer, 1982
    locator: the text and translation of the De solidorum elementis with Descartes's statement that the exterior solid angles of a convex polyhedron sum to eight right angles, and its relation to Euler's formula (general locator)
  - paper: doi:10.1080/00029890.1970.11992523
    title: Thomas F. Banchoff, Critical points and curvature for embedded polyhedral surfaces, American Mathematical Monthly 77(5), 1970, 475 to 485
    locator: the curvature of a vertex of a polyhedral surface as its angle defect and the polyhedral Gauss-Bonnet theorem
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 4-5, The Gauss-Bonnet Theorem and Its Applications (the smooth theorem, with the geodesic curvature of the border and the exterior angles at its corners)
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 3, Differential Geometry (the angle deficit and the discrete Gauss-Bonnet theorem)
---

The discrete Gauss-Bonnet theorem says that the [angle defects](/discrete-gaussian-curvature/) of a closed polyhedral surface add up to $2\pi$ times its Euler characteristic $\chi = V - E + F$. A cube has eight corners of defect $\pi/2$, which sum to $4\pi = 2\pi \cdot 2$, and every closed mesh of genus 0, convex or not, also gives $4\pi$. A mesh of a torus gives 0, whatever its shape. With a border, the turning angles of the border vertices join the sum. The identity is exact, it holds for every mesh with planar faces, and it is a rearrangement of [Euler's formula](/euler-formula/): it is the discrete form of the smooth theorem $\int K \, dA + \int k_g \, ds = 2\pi\chi$ on the [surface curvature](/surface-curvature/) page.

## Statement

Let $M$ be a finite mesh with $V$ vertices, $E$ edges and $F$ faces, where each face is a simple planar polygon with $k_f \ge 3$ sides and each vertex lies in some face. For a vertex $i$, let $\Theta_i$ be the sum of the interior angles of the faces at $i$. An edge is a *border edge* if it lies in one face. A vertex on a border edge is a *border vertex*, and the others are *inner vertices*. Assume:

- (H1) each edge lies in one or two faces, and
- (H2) each border vertex lies on exactly two border edges.

**Theorem.** Under (H1) and (H2),

$$\sum_{i \text{ inner}} \left(2\pi - \Theta_i\right) \;+\; \sum_{i \text{ border}} \left(\pi - \Theta_i\right) \;=\; 2\pi\,(V - E + F).$$

In particular, for a closed mesh, with no border edge, the angle defects $K_i = 2\pi - \Theta_i$ satisfy $\sum_i K_i = 2\pi\chi$. For a closed oriented [manifold mesh](/manifold-mesh/) of genus $g$ this is $4\pi(1 - g)$, and for a manifold mesh of genus $g$ with $b$ border loops the right side is $2\pi(2 - 2g - b)$, by the [Euler-Poincaré formula](/euler-poincare-formula/).

The border terms $\kappa_i = \pi - \Theta_i$ are the turning angles of the border inside the surface, the discrete geodesic curvature of the border. They are not Gaussian curvature.

## In plain words

At each corner of a closed mesh, add the angles of the faces that meet there and see how far the total falls short of a full turn. That shortfall is the curvature at the corner. A sharp corner has a large shortfall, a flat spot has none, and a saddle overshoots, which counts as negative.

The theorem says that the shortfalls of all corners always add up to the same amount for a given kind of surface. Every closed surface without holes, such as a cube, a ball or a bunny, gives two full turns. A ring shape gives zero, so its corners that stick out are exactly balanced by the saddle corners on the inside. The shape and the number of faces do not matter, only the number of handles. This shows that curvature cannot be made or removed by moving vertices, only moved around.

## Proof

All angle sums can be counted in two ways, by vertex and by face.

**Step 1 (by face).** A simple planar polygon with $k$ sides has interior angles that sum to $(k - 2)\pi$, since it can be cut into $k - 2$ triangles by diagonals. Each interior angle of each face is at exactly one vertex, so

$$\sum_{i} \Theta_i = \sum_f (k_f - 2)\pi = \pi \sum_f k_f - 2\pi F .$$

**Step 2 (sides and edges).** Each side of a face is one edge, and by (H1) each edge is a side of two faces, or of one face if it is a border edge. With $E_b$ border edges, $\sum_f k_f = 2(E - E_b) + E_b = 2E - E_b$.

**Step 3 (border vertices and border edges).** Let $V_b$ be the number of border vertices. Each border edge has two border vertices as its ends, and by (H2) each border vertex is the end of exactly two border edges. Counting the pairs (border vertex, border edge at it) both ways gives $2E_b = 2V_b$, so $V_b = E_b$.

**Step 4 (sum).** With $V_i = V - V_b$ inner vertices, the left side of the theorem is

$$2\pi V_i + \pi V_b - \sum_i \Theta_i = 2\pi V - \pi V_b - \pi(2E - E_b) + 2\pi F = 2\pi(V - E + F) + \pi(E_b - V_b),$$

and the last term is 0 by Step 3. $\square$

No step uses that the faces at an inner vertex form one fan, that the mesh is oriented, or that it is embedded without crossings. The value $\chi = V - E + F$ is the combinatorial one. Only to read $\chi$ as $2 - 2g$ or $2 - 2g - b$ do we need a manifold mesh.

**Without (H2).** If a border vertex $i$ lies on $e_i$ border edges, Step 3 becomes $\sum_i e_i = 2E_b$, and the same computation gives the identity

$$\sum_i \left( \left(2 - \tfrac{e_i}{2}\right)\pi - \Theta_i \right) = 2\pi\,(V - E + F)$$

over all vertices, with $e_i = 0$ for inner vertices. Under (H2), $e_i = 2$ on the border, and this is the theorem.

## Consequences

- **Descartes's theorem.** For a convex polyhedron, $\chi = 2$, so the defects, all positive, sum to $4\pi$. Descartes stated this as "the exterior solid angles add up to eight right angles". The five Platonic solids on the [discrete Gaussian curvature](/discrete-gaussian-curvature/) page check it.
- **Every closed mesh of genus 0 has a vertex of positive defect**, since the total is $4\pi > 0$. Every closed mesh of genus $g \ge 2$ has a saddle vertex, since the total is negative. A mesh of a torus with one vertex of positive defect must have one of negative defect.
- **Valences of a triangle mesh.** If every face is an equilateral triangle, then $\Theta_i = d_i \pi/3$ for a vertex of valence $d_i$, and the theorem becomes $\sum_i (6 - d_i) = 6\chi$. This also holds for every closed triangle mesh, since it only counts: $\sum_i d_i = 2E$ and $3F = 2E$. So a closed triangle mesh of genus 0 has $\sum_i (6 - d_i) = 12$, and cannot have valence 6 at every vertex: an icosahedral sphere has exactly twelve vertices of valence 5 when all others have valence 6. This is why [isotropic remeshing](/isotropic-remeshing/) only moves valences toward 6 and cannot reach 6 everywhere.
- **A test for mesh code.** Since the identity is exact for every mesh with planar faces, summing the defects and comparing with $2\pi\chi$ catches wrong angle formulas, faces that are not planar, and broken border loops.
- **Curvature is conserved.** Moving vertices, refining or flipping edges changes each defect but not the total, as long as $\chi$ stays the same. A smoothing step can only move curvature around.

## Tightness

Each hypothesis is needed, and removing it gives a wrong total. All the numbers below are exact.

- **Planar faces.** Glue two copies of the skew quadrilateral on the vertices $(1, 1, 1)$, $(1, -1, -1)$, $(-1, 1, -1)$, $(-1, -1, 1)$ along their four sides. The surface is closed with $V = 4$, $E = 4$, $F = 2$, so $\chi = 2$. All sides have the same length, and each angle is $\pi/3$, so each vertex has $\Theta = 2\pi/3$, and the defects sum to $4(2\pi - 2\pi/3) = 16\pi/3$, not $4\pi$. A skew quadrilateral has an angle sum less than $2\pi$, so Step 1 fails.
- **(H1), two faces per edge.** Take a triangular bipyramid of six equilateral triangles and add the middle triangle that it surrounds. The three middle edges now lie in three faces each. $V = 5$, $E = 9$, $F = 7$, so $2\pi\chi = 6\pi$. The seven triangles have angle sum $7\pi$, and all vertices are inner, so the defects sum to $10\pi - 7\pi = 3\pi$.
- **(H2), two border edges per border vertex.** Two equilateral triangles that share one vertex, a bowtie, have $V = 5$, $E = 6$, $F = 2$, $\chi = 1$. The shared vertex lies on four border edges. The sum in the theorem is $(\pi - 2\pi/3) + 4(\pi - \pi/3) = 3\pi$, not $2\pi$. The form without (H2) gives $(2\pi - 2\pi - 2\pi/3) + 8\pi/3 = 2\pi$.
- **Manifold inner vertices are not needed.** Two octahedra that share one vertex form a closed mesh that is not a manifold at that vertex. $V = 11$, $E = 24$, $F = 16$, $\chi = 3$. The shared vertex has eight angles of $\pi/3$ and defect $-2\pi/3$, and the other ten have $2\pi/3$, so the total is $6\pi = 2\pi\chi$, as the proof says.
- **A torus.** The square picture frame with outer side 6, inner side 2 and height 1 has 16 vertices, 32 edges and 16 planar quadrilaterals, so $\chi = 0$. An outer corner has two angles of $\pi/4$ from the trapezoids of the top or the bottom and two right angles, so its defect is $+\pi/2$. An inner corner has two angles of $3\pi/4$ and two right angles, so its defect is $-\pi/2$. There are eight of each, and the total is 0.
- **With a border.** The unit square cut into four triangles at its center has $V = 5$, $E = 8$, $F = 4$, $\chi = 1$. The center has four right angles and defect 0. Each corner has two angles of $\pi/4$, so $\kappa = \pi/2$, and the total is $2\pi = 2\pi\chi$.
- **Only the total is exact.** The theorem says nothing about one vertex. Divided by an area, the defect at a single vertex need not converge to the Gaussian curvature under refinement, as the measured table on the [discrete Gaussian curvature](/discrete-gaussian-curvature/) page shows.

## History

René Descartes wrote, in a manuscript of about 1630, that the exterior solid angles of a convex polyhedron sum to eight right angles. The manuscript was lost. Leibniz had made a copy, which was found and published in the nineteenth century. Federico (1982) gives the text and shows that Descartes's results imply Euler's formula $V - E + F = 2$, which Euler published in 1758. The general form, for any closed polyhedral surface and with $2\pi\chi$ on the right, is a direct consequence of Euler's formula for surfaces. Banchoff (1970) used the angle defect as the curvature of a polyhedral surface and proved the polyhedral Gauss-Bonnet theorem together with a polyhedral critical point theory. In mesh processing, the identity is the reason the angle defect is taken as the discrete Gaussian curvature.

## References
