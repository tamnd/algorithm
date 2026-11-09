---
tag: NSPR4V
kind: theorem
slug: voronoi-delaunay-duality
name: Voronoi-Delaunay duality
aliases:
- Delaunay-Voronoi duality
- Delaunay subdivision as the dual of the Voronoi diagram
area: geometry/voronoi-and-delaunay
level: intro
summary: The Delaunay triangulation is the straight-line dual graph of the Voronoi diagram of the same sites.
prereqs: [voronoi-diagram, voronoi-cell, delaunay-triangulation, planar-subdivision]
see_also: [voronoi-complexity-theorem, empty-circle-property, circumcenter, delaunay-triangulation-uniqueness, paraboloid-lifting-map, voronoi-diagram-construction, delaunay-triangulation-construction, power-diagram]
sources:
  - paper: "B. Delaunay, Sur la sphère vide, Bulletin de l'Académie des Sciences de l'URSS, Classe des sciences mathématiques et naturelles 6, 1934, 793-800"
    locator: the empty sphere criterion and the subdivision dual to the Voronoi (Dirichlet) tessellation
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Section 9.2 (the Delaunay graph as the dual of the Voronoi diagram, its planarity, and the empty circle characterization of its edges and faces)
  - book: isbn:9780471986355
    title: A. Okabe, B. Boots, K. Sugihara and S. N. Chiu, Spatial Tessellations, Concepts and Applications of Voronoi Diagrams, second edition, Wiley, 2000
    locator: Chapter 2 (the Delaunay tessellation as the dual of the Voronoi diagram, with degenerate vertices)
---

Voronoi-Delaunay duality says that the [Voronoi diagram](/voronoi-diagram/) of a set of sites and its Delaunay subdivision describe the same structure. Each site gives a Voronoi cell and a Delaunay vertex. Each Voronoi edge between the cells of $p$ and $q$ gives the Delaunay edge $pq$, at right angles to it. Each Voronoi vertex gives a Delaunay face, the polygon of the sites on the empty circle around the vertex. When no four sites lie on a common empty circle, all these faces are triangles and they form the [Delaunay triangulation](/delaunay-triangulation/); otherwise the faces are larger convex polygons, and the Delaunay triangulations are the ways to cut them into triangles. Because of this duality, each structure is computed from the other in $O(n)$ time.

## Statement

**Setting.** $P$ is a set of $n \ge 3$ distinct sites $p = (x, y)$ in the plane, not all on one line, and $H$ is its convex hull. $V_p$ is the [Voronoi cell](/voronoi-cell/) of $p$. A Voronoi vertex $x$ has the nearest sites $Q_x$, at a common distance $r_x$; the circle $C_x$ of radius $r_x$ around $x$ holds $Q_x$ and has no site strictly inside, and $|Q_x| \ge 3$. A **Delaunay circle** is a circle with no site strictly inside and with at least three sites on it. The **Delaunay face** of $x$ is the convex polygon $F_x = \mathrm{conv}(Q_x)$. Notation: $\mathrm{orient}(p, q, r)$ is positive when $p, q, r$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside the circle through $a, b, c$.

**Theorem.**

1. *Vertices and faces.* The map $x \mapsto C_x$ is a bijection from the Voronoi vertices to the Delaunay circles, and $x$ is the [circumcenter](/circumcenter/) of every triangle with vertices in $Q_x$. A site $p$ is a corner of $F_x$ if and only if $x$ lies on the boundary of $V_p$.
2. *Edges.* For sites $p \ne q$, the cells $V_p$ and $V_q$ share a Voronoi edge if and only if the segment $pq$ is a side of some face $F_x$. The Voronoi edge lies on the bisector of $p$ and $q$, so it is perpendicular to $pq$. Its finite ends are exactly the vertices $x$ for which $pq$ is a side of $F_x$. It is a ray if and only if $pq$ is an edge of the boundary of $H$.
3. *Subdivision.* The faces $F_x$ have pairwise disjoint interiors and their union is $H$. So the sites, the segments $pq$ of item 2 and the faces $F_x$ form a [planar subdivision](/planar-subdivision/) of $H$, the **Delaunay subdivision**, whose graph is drawn with straight edges and no crossings.
4. *Triangulations.* The Delaunay triangulations of $P$ are exactly the triangulations obtained by cutting each face $F_x$ into triangles by diagonals. If no four sites lie on one Delaunay circle, every face is a triangle and the Delaunay triangulation is unique and equal to the Delaunay subdivision.

No general position is assumed except in the last sentence. If all sites are on one line, the Voronoi diagram has no vertex and the Delaunay graph is the path of consecutive sites, each edge dual to one of the parallel Voronoi lines.

## In plain words

Draw the regions of the nearest sites. Now join two sites by a straight line whenever their regions share a border piece. These lines never cross, and they cut the area around the sites into polygons.

Each polygon matches one corner of the regions. The sites of the polygon are the sites nearest to that corner, and they all lie on one circle around the corner with nothing inside it. Usually three sites meet at a corner, so the polygons are triangles: these are the Delaunay triangles. When four or more sites meet at one corner, the polygon has more sides, and you can cut it into triangles in more than one way.

## Proof

**Lemma 1 (empty circles and vertices).** A point $x$ is a Voronoi vertex if and only if some Delaunay circle has center $x$, and then that circle is $C_x$.

*Proof.* If $x$ is a vertex, $C_x$ has no site strictly inside, since all sites are at distance $\ge r_x$ from $x$, and it holds the $|Q_x| \ge 3$ nearest sites. Conversely, if a Delaunay circle $C$ has center $x$ and radius $r$, then every site is at distance $\ge r$ from $x$ and at least three are at distance $r$, so $x$ has three or more nearest sites and $C = C_x$. Three sites of $Q_x$ are on the circle $C_x$, so they are not on one line and $x$ is their circumcenter. $\square$

**Lemma 2 (corners).** The sites in $Q_x$ are the corners of $F_x$, and $p \in Q_x$ exactly when $x \in V_p$, which for a vertex $x$ means that $x$ is on the boundary of $V_p$.

*Proof.* Distinct points on a circle are in convex position, so each point of $Q_x$ is a corner of $\mathrm{conv}(Q_x)$. A site $p$ is nearest to $x$ exactly when $x \in V_p$. A vertex $x \in V_p$ has another nearest site $q$, and points near $x$ on the side of $q$ are nearer to $q$ than to $p$, so $x$ is on the boundary of $V_p$. $\square$

**Lemma 3 (edges at a vertex).** Let $x$ be a vertex and let $s_1, \ldots, s_k$ be the sites of $Q_x$ in counterclockwise order on $C_x$. Then exactly $k$ Voronoi edges end at $x$, one between $V_{s_i}$ and $V_{s_{i+1}}$ for each $i$ (indices mod $k$), and no Voronoi edge passes through $x$.

*Proof.* All other sites are farther than $r_x$, so for $y = x + \varepsilon u$ with $|u| = 1$ and small $\varepsilon > 0$ the nearest sites of $y$ are among $Q_x$, and $|y - s_i|^2 = r_x^2 - 2 \varepsilon u \cdot (s_i - x) + \varepsilon^2$. So the nearest sites of $y$ are those whose direction from $x$ is nearest in angle to $u$. As $u$ turns once around, this site changes exactly at the $k$ directions that bisect the angles between the consecutive directions $s_i - x$ and $s_{i+1} - x$, and in each such direction $y$ has the two nearest sites $s_i, s_{i+1}$. So near $x$ the diagram is $k$ segments from $x$ on the bisectors of the consecutive pairs. A Voronoi edge is the relative interior of $V_p \cap V_q$, and on it the only nearest sites are $p$ and $q$ (see the [complexity theorem](/voronoi-complexity-theorem/), Lemma 1), so $x$, which has $k \ge 3$ nearest sites, is not on an edge and is an end of each of the $k$ edges. $\square$

**Lemma 4 (a Delaunay triangulation exists and groups into faces).** $P$ has a Delaunay triangulation $D$. For every such $D$, the circumcircle of each triangle of $D$ is a Delaunay circle, every Delaunay circle $C$ is the circumcircle of some triangle of $D$, and the triangles of $D$ with circumcircle $C$ form a triangulation of the convex polygon $\mathrm{conv}(P \cap C)$.

*Proof.* Existence: the [Lawson flip algorithm](/lawson-flip-algorithm/) turns any triangulation of $P$ into one in which every interior edge is locally Delaunay, after finitely many flips, and by the [local Delaunay criterion](/local-delaunay-criterion/) that triangulation is Delaunay. The circumcircle of a triangle of $D$ passes through three sites and has none strictly inside, so it is a Delaunay circle.

For a circle $C$ with center $c$ and radius $\rho$, let $f_C(z) = 2 c \cdot z + \rho^2 - |c|^2$, so that $|z|^2 - f_C(z) = |z - c|^2 - \rho^2$; this is negative inside $C$, zero on $C$ and positive outside. For a triangle $t$ let $f_t = f_{C_t}$ for its circumcircle $C_t$; it is the affine function equal to $|z|^2$ at the three vertices. Let $C$ be a Delaunay circle and $Q = P \cap C$. Let $t$ be a triangle of $D$ whose interior meets the interior of $\mathrm{conv}(Q)$, a nonempty open set since $|Q| \ge 3$ and $Q$ is on a circle; such $t$ exists because the triangles of $D$ cover $H$. The vertices $z$ of $t$ are sites, not strictly inside $C$, so $f_t(z) = |z|^2 \ge f_C(z)$, and as both functions are affine, $f_t \ge f_C$ on $t$. The points $q \in Q$ are sites, not strictly inside $C_t$, so $f_C(q) = |q|^2 \ge f_t(q)$, and $f_C \ge f_t$ on $\mathrm{conv}(Q)$. On the common open part of the two interiors, $f_t = f_C$, so the affine functions are equal and $C_t = C$. So $C$ is a circumcircle of a triangle of $D$, and every triangle whose interior meets the interior of $\mathrm{conv}(Q)$ has its corners on $C$, so it lies in $\mathrm{conv}(Q)$. Every triangle with circumcircle $C$ has its corners in $Q$ and lies in $\mathrm{conv}(Q)$ too. So the triangles with circumcircle $C$ cover $\mathrm{conv}(Q)$, with disjoint interiors. Every point of $Q$ is a vertex of $D$, and it is a corner of the convex polygon $\mathrm{conv}(Q)$, so it is a corner of one of these triangles. So they form a triangulation of $\mathrm{conv}(Q)$. $\square$

**Proof of item 1.** By Lemma 1, $x \mapsto C_x$ maps vertices to Delaunay circles, it is one-to-one since $x$ is the center of $C_x$, and it is onto since each Delaunay circle has its center as a vertex. The rest is Lemma 1 and Lemma 2. $\square$

**Proof of item 2.** Assume $V_p$ and $V_q$ share an edge $E$. If $E$ had no finite end, it would be a whole line; then for every other site $s$, the affine function $|y - s|^2 - |y - p|^2$ would be $\ge 0$ on the whole line, so constant on it, and $s - p$ would be parallel to $q - p$, which puts all sites on one line. So $E$ has a finite end $x$, a vertex by Lemma 1 of the complexity theorem, and by Lemma 3, $p$ and $q$ are consecutive on $C_x$, so $pq$ is a side of $F_x$. Conversely, if $pq$ is a side of $F_x$, then $p$ and $q$ are consecutive on $C_x$, because the sides of a polygon inscribed in a circle join consecutive points, and by Lemma 3 an edge of $V_p \cap V_q$ ends at $x$. The same two arguments show that the finite ends of $E$ are exactly the vertices $x$ with $pq$ a side of $F_x$. The edge lies on the bisector, which is perpendicular to $pq$.

By item 3, proved next, each segment $pq$ is a side of at most two faces, and it is a side of exactly one face if and only if it lies on the boundary of $H$. A segment $E$ has two finite ends and a ray has one, so $E$ is a ray if and only if $pq$ is a side of exactly one face, that is, a boundary edge of $H$. $\square$

**Proof of item 3.** Take a Delaunay triangulation $D$ by Lemma 4. Its triangles cover $H$ with disjoint interiors, and by Lemma 4 they fall into groups, one for each Delaunay circle $C_x$, each group triangulating $F_x = \mathrm{conv}(Q_x)$. So the faces $F_x$ cover $H$, and two different faces have disjoint interiors, because they are unions of different triangles of $D$. A side $pq$ of a face $F_x$ holds no site other than $p$ and $q$, because the points of an open chord are strictly inside $C_x$; so $pq$ is a single edge of $D$. If $pq$ is not on the boundary of $H$, the triangle of $D$ on its other side contains the whole edge $pq$ and belongs to one face $F_y$, and $pq$ is then a side of $F_y$ as well. So two faces meet in a common side, in a common corner or not at all, and the faces with their sides and corners form a subdivision of $H$. Its edges are the sides of the faces, which by item 2 are exactly the duals of the Voronoi edges, and they do not cross. A side lies on the boundary of $H$ exactly when it is a side of one face only, and otherwise it is a side of exactly two faces, the faces of the two triangles of $D$ at that edge. $\square$

**Proof of item 4.** By Lemma 4 every Delaunay triangulation cuts each $F_x$ into triangles; within the convex polygon $F_x$ with its corners on a circle, a triangulation uses only diagonals. Conversely, cut each $F_x$ into triangles by diagonals. The result is a triangulation of $P$, because the faces tile $H$ by item 3 and every site is a corner of some face. Each new triangle has its corners on $C_x$, so its circumcircle is $C_x$, which has no site strictly inside. So the triangulation is Delaunay. If no four sites lie on a Delaunay circle, every $|Q_x| = 3$ and every face is a triangle, so there is exactly one way to cut. $\blacksquare$

## Consequences

- **Conversion in linear time.** From a Delaunay triangulation, the Voronoi vertices are the circumcenters of its triangles, merging equal circumcenters, and the Voronoi edges are the bisectors of its edges, cut at the circumcenters of the two neighbouring triangles, or rays out of the hull for hull edges. From a Voronoi diagram stored with adjacencies, the Delaunay subdivision is read off cell by cell. Both take $O(n)$ time, so [Voronoi construction](/voronoi-diagram-construction/) and [Delaunay construction](/delaunay-triangulation-construction/) are the same problem.
- **Sizes.** The Voronoi diagram has as many edges as the Delaunay subdivision and as many vertices as it has faces. With the [complexity theorem](/voronoi-complexity-theorem/), in general position the Delaunay triangulation has $2n - 2 - h$ triangles and $3n - 3 - h$ edges, where $h$ is the number of sites on the hull boundary.
- **Nearest neighbours.** If $q$ is a nearest site of $p$, then $pq$ is a Delaunay edge. Let $m$ be the midpoint of $pq$. For every site $s$, $|m - s| \ge |p - s| - |p - m| \ge |p - q| - |p - q|/2 = |m - p|$, so $m \in V_p \cap V_q$. If this set were the single point $m$, then $m$ would be a vertex whose circle has the diameter $pq$ and a third site $s$, and then $|p - s| < |p - q|$, which is false. So $V_p \cap V_q$ is an edge and $pq$ is in every Delaunay triangulation. All nearest neighbours are then found in $O(n)$ time from the triangulation.
- **Empty circle form.** The segment $pq$ is a Delaunay edge if and only if some circle through $p$ and $q$ has no site strictly inside and no other site on it; the centers of these circles are the inner points of the Voronoi edge. This is the [empty circle property](/empty-circle-property/) for edges.
- **Lifting.** The same duality, seen through the [paraboloid lifting map](/paraboloid-lifting-map/), is the polarity between the lower convex hull of the lifted sites and the upper envelope of their tangent planes.

## Tightness

- **Primal and dual edges need not cross.** For the obtuse triangle $(0,0)$, $(4,0)$, $(2,1)$, the Voronoi vertex is the circumcenter $(2, -3/2)$, outside the triangle, and the Voronoi edge between $(0,0)$ and $(4,0)$ is the ray from $(2, -3/2)$ downward. It does not meet the Delaunay edge from $(0,0)$ to $(4,0)$, which lies on the line $y = 0$ above the ray. The duality is combinatorial; it does not say that dual edges cross.
- **Degenerate vertices.** For the square $(0,0)$, $(2,0)$, $(2,2)$, $(0,2)$, the Voronoi diagram has one vertex $(1,1)$ with four edges, and the Delaunay subdivision has one face, the square. Its two diagonals give two Delaunay triangulations, and neither diagonal is dual to a Voronoi edge, since the diagonal sites share only the point $(1,1)$. In a $k \times k$ grid every unit square is such a face.
- **Six sites.** For $(2,8)$, $(6,7)$, $(0,4)$, $(4,5)$, $(8,3)$, $(3,0)$, the Delaunay triangulation joins $(4,5)$ to the five hull sites. The five triangles have the circumcenters $(56/11, 24/11)$, $(19/3, 14/3)$, $(39/10, 71/10)$, $(12/7, 79/14)$ and $(93/38, 103/38)$, which are the five Voronoi vertices, and the five hull edges are dual to the five Voronoi rays.
- **Collinear sites.** For sites on one line there is no Voronoi vertex and no Delaunay face; the Delaunay graph is a path and the theorem in its face form does not apply.

## History

G. Voronoi described in 1908 the subdivision dual to his cells for lattices, and B. Delaunay defined in 1934 the subdivision by empty spheres and proved that it is dual to the Voronoi (Dirichlet) tessellation. In computational geometry the duality was used from the start: Shamos and Hoey in 1975 computed the Voronoi diagram, and later algorithms such as those of Lee and Schachter in 1980 and Guibas and Stolfi in 1985 compute the Delaunay triangulation and read off the diagram.

## References
