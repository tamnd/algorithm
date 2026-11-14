---
title: The minimum zone of flatness is attained by a face and a vertex or by two edges of the convex hull, the exact candidate tests find it, and the vertical Chebyshev fit only bounds it
proves: [correctness, termination]
status: full
---

**Setup.** $P$ is a finite set of points in $\mathbb{R}^3$ and $K$ is its convex hull. For a unit vector $u$ let $h(u) = \max_{x \in P} u \cdot x$, the [support function](/support-function/), and $w(u) = h(u) + h(-u)$, the extent of $P$ in the direction $u$. A zone with unit normal $u$ is a slab $\{x : \ell \le u \cdot x \le \ell + t\}$, and it holds $P$ only if $t \ge w(u)$. So the minimum zone flatness is
$$ F(P) = \min_{\lvert u \rvert = 1} w(u), $$
the width of $P$. The minimum exists because $w$ is continuous on the unit sphere $S^2$. If $P$ lies in a plane, $F(P) = 0$; from now on $K$ has full dimension, so $w(u) > 0$ for every $u$.

**Lemma 1 (the faces met by a direction).** For each $u$, let $F^+(u)$ be the face of $K$ on which $u \cdot x$ is largest and $F^-(u) = F^+(-u)$. The normal cones of the vertices, edges and facets of $K$ cut $S^2$ into open regions (one per vertex), open great circle arcs (one per edge, normal to the edge) and points (the facet normals); this is the Gaussian map of $K$. Overlay it with its image under $u \mapsto -u$. On each cell of the overlay, $F^+$ and $F^-$ are fixed, and $w(u) = u \cdot c$ with $c = a - b$ for any $a \in F^+$ and $b \in F^-$.

*Proof.* $u \cdot x$ is constant on $F^+(u)$ and equal to $h(u)$ there, and $h(-u) = -u \cdot b$ for $b \in F^-(u)$. In a cell of the overlay, both faces are fixed by the definition of the cell. $\square$

**Lemma 2 (where the minimum is).** Let $u^*$ minimize $w$. Then one of these holds:
(a) $u^*$ or $-u^*$ is the outward normal of a facet of $K$ (a face and a vertex, the vertex in the face of the other side);
(b) $u^*$ is normal to an edge $e$ and an edge $f$ of $K$ that are not parallel, $u^*$ is in the normal cone of $e$ and $-u^*$ in the normal cone of $f$ (two edges).

*Proof.* Suppose first that $u^*$ is in an open two-dimensional cell of the overlay. By Lemma 1, $w(u) = u \cdot c$ near $u^*$, and $u^*$ is a local minimum of $u \cdot c$ on $S^2$. The gradient of $u \cdot c$ on the sphere is $c - (u \cdot c) u$, which is zero only at $u = \pm c / \lvert c \rvert$ (or everywhere if $c = 0$). The point $c / \lvert c \rvert$ is the maximum, and at $-c / \lvert c \rvert$ and for $c = 0$ the value is $\le 0$. Each case contradicts $w(u^*) > 0$.

Suppose next that $u^*$ is in an open arc of the overlay. The arc lies on a great circle $C$, and on the arc $w(u) = u \cdot c$ by Lemma 1. Write $u = \cos s \, g_1 + \sin s \, g_2$ for an orthonormal basis $g_1, g_2$ of the plane of $C$. Then $u \cdot c = A \cos s + B \sin s = R \cos(s - s_0)$ with $R \ge 0$, whose local minima on $C$ have the value $-R \le 0$. Again $w(u^*) > 0$ gives a contradiction.

So $u^*$ is a vertex of the overlay: a vertex of the Gaussian map (a facet normal, case (a)), a vertex of its antipodal image ($-u^*$ a facet normal, case (a)), or a point where an arc of an edge $e$ crosses the antipodal image of an arc of an edge $f$. Two arcs on distinct great circles meet in isolated points, which is case (b); $u^*$ is then normal to both $e$ and $f$. If the two great circles are the same ($e$ parallel to $f$), the arcs overlap in an arc, and a vertex of the overlay on it is an end of one of the arcs, which is a facet normal of case (a). $\square$

This is the characterization of Houle and Toussaint (1988); the proof above follows the Gaussian map.

**Lemma 3 (the incremental hull).** The procedure `convex_hull_3d` returns oriented triangles whose union is the boundary of $K$, each with all points of $P$ on its inner side or on it, and no triangle has zero area.

*Proof sketch.* The start is a tetrahedron of four points that are not coplanar, oriented so that the fourth vertex is on the inner side of each face. Assume the triangles bound $K_j = \operatorname{conv}$ of the points so far. A new point $p$ is in $K_j$ exactly when no triangle has $p$ strictly on its outer side, and then $K_{j+1} = K_j$. Otherwise the visible triangles (strictly outer side) are the triangles of the facets of $K_j$ whose planes separate $p$ strictly, and their union is a disk whose boundary is the horizon. The boundary of $K_{j+1}$ is the rest of the old boundary and the cone from $p$ over the horizon; this is the standard incremental argument in de Berg, Cheong, van Kreveld and Overmars, Chapter 11. Treating a triangle whose plane holds $p$ as not visible only adds coplanar neighbor triangles. A new triangle $(u, v, p)$ is never degenerate: $u, v$ lie on a visible triangle, and if $p$ were on the line $uv$ it would be in the plane of that triangle, which then would not be strictly visible. Each signed volume is computed with exact integers or fractions, so all tests are exact. $\square$

The tests check on random integer sets with many coplanar points that the result is a closed oriented surface, that $V - E + F = 2$, and that every point is on the inner side of every triangle.

**Lemma 4 (the cone test).** Let an edge of the triangulated hull have direction $d$ and the outward normals $N_1$, $N_2$ of its two triangles, both normal to $d$. A vector $u$ normal to $d$ is a combination $\alpha N_1 + \beta N_2$ with $\alpha, \beta \ge 0$ if and only if: when $t = \det(N_1, N_2, d) = 0$, $u$ is a positive multiple of $N_1$ (or $u = 0$); when $t \ne 0$, $\det(N_1, u, d)$ and $\det(u, N_2, d)$ are each $0$ or of the sign of $t$.

*Proof.* If $t \ne 0$, then $N_1, N_2$ are independent and span the plane normal to $d$, so $u = \alpha N_1 + \beta N_2$ for unique $\alpha, \beta$. By linearity of the determinant, $\det(N_1, u, d) = \beta t$ and $\det(u, N_2, d) = \alpha t$. If $t = 0$, then $N_1$ and $N_2$ are parallel; they are not opposite, because two triangles of a closed convex surface with opposite outward normals on a common edge would make $K$ flat. So $N_2$ is a positive multiple of $N_1$ and the cone is the ray of $N_1$. $\square$

**Lemma 5 (every candidate is a zone).** If $u = \alpha N_1 + \beta N_2$ with $\alpha, \beta \ge 0$ for an edge with endpoint $a$, then $u \cdot x \le u \cdot a$ for all $x \in P$. So for each candidate of the code (a triangle with its lowest vertex, or two edges with $u$ in the cone of the first and $-u$ in the cone of the second), the slab between the two planes holds $P$, and its width is at least $F(P)$.

*Proof.* By Lemma 3, $N_k \cdot x \le N_k \cdot a$ for $k = 1, 2$, because $a$ lies on both triangles. Add the inequalities with weights $\alpha, \beta$. For a triangle, the upper plane holds the triangle, all points are on its inner side, and the lower plane is through the point of least $N \cdot x$. $\square$

**Theorem (correctness).** `minimum_zone_flatness` returns a zone of width $F(P)$ that holds $P$.

*Proof.* By Lemma 5 the result holds $P$ and its width is at least $F(P)$. Let $u^*$ be as in Lemma 2. In case (a), the facet with normal $\pm u^*$ is a union of triangles of the code with outward normals that are positive multiples of $\pm u^*$, and the code measures each triangle against the lowest vertex, which gives the width $w(u^*)$. In case (b), the edge $e$ of $K$ is a union of collinear triangle edges, and each one has its two triangles in the two facets of $K$ at $e$, so its cone is the normal cone of $e$; the same holds for $f$. For such a pair the code forms $n = d_e \times d_f$, which is parallel to $u^*$, tries $n$ and $-n$, and by Lemma 4 accepts the sign that points along $u^*$. The width of that candidate is $u^* \cdot (a - b) = w(u^*)$ for points $a \in e$, $b \in f$. So the minimum over the candidates is at most $F(P)$. All values are compared as exact squared widths. $\square$

**Termination.** Every loop runs over finite lists: $n$ insertions, each over the current triangles, then the triangles and the pairs of edges.

**Lemma 6 (straightness).** For points in the plane, the thinnest strip is attained by an edge of the convex hull and the farthest hull vertex. *Proof.* The same argument in one dimension lower: on the unit circle, the cells of the overlay are open arcs and points, on an open arc $w(u) = u \cdot c$ has no local minimum with a positive value, so $u^*$ is the normal of an edge of the hull or the opposite of one. $\square$

**The vertical Chebyshev fit.** The linear program minimize $t$ subject to $\lvert z_i - a x_i - b y_i - c \rvert \le t$ has the optimal value $V^* = \min_{a,b} V(a, b)$ with $V(a, b) = \max_i r_i - \min_i r_i$, $r_i = z_i - a x_i - b y_i$, and the optimum zone has the thickness $2t = V^*$. The zone $\{\, c \le z - a x - b y \le c + V \,\}$ has the normal $(-a, -b, 1)$ and the orthogonal width $V / \sqrt{1 + a^2 + b^2}$.

**Theorem (the vertical fit only bounds flatness).** Let $(a^*, b^*)$ solve the vertical fit, and let the minimum zone have a normal $(-g_1, -g_2, 1)$ that is not horizontal. Then
$$ F(P) \le \frac{V^*}{\sqrt{1 + a^{*2} + b^{*2}}} \le V^* \le F(P) \sqrt{1 + g_1^2 + g_2^2}. $$
*Proof.* The first inequality holds because the vertical zone is a zone. The second is clear. For the third, the minimum zone has the vertical thickness $V(g_1, g_2) = F(P) \sqrt{1 + g_1^2 + g_2^2}$, and $V^*$ is the least vertical thickness. $\square$

The first inequality can be strict: the point set $(1,2,2), (0,0,1), (4,3,10), (3,3,7), (1,3,4)$ has $F^2 = 81/170$, attained by two edges with the normal $(-12, -1, 5)$, while the vertical fit has the unique optimum $V^* = 5/3$ at $(a, b) = (2, 1/3)$ and the orthogonal width $0.7372 > 0.6903 = F$. The tests check these values with exact arithmetic.

**The least-squares plane.** Any plane through the centroid along the smallest eigenvector of the covariance matrix gives a zone, so its width is at least $F(P)$ by the definition of $F$. It is never narrower than the minimum zone, and it is often wider.
