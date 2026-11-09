---
title: The Voronoi diagram built from a Delaunay triangulation is correct
proves: [correctness]
status: full
---

**Claim.** Let $P$ be a set of $n \ge 3$ distinct sites in the plane, not all on one line, and let $D$ be any Delaunay triangulation of $P$. Then BUILD returns exactly the Voronoi vertices, and for each pair $\{p, q\}$ whose cells $V_p$ and $V_q$ share a piece of positive length, it records exactly that piece, with its ends. $\mathrm{cell}(p)$ returns the vertices of $V_p$ in counterclockwise order and reports correctly whether $V_p$ is bounded. For every point $q$, $\mathrm{nearest}(q)$ returns a site at the smallest distance from $q$. For collinear sites, the build returns the $n - 1$ bisectors of consecutive sites and no vertex, which is the diagram.

No general position is assumed.

**Facts used.** These are proved on the page of [Voronoi-Delaunay duality](/voronoi-delaunay-duality/). For a Voronoi vertex $x$, let $Q_x$ be its nearest sites and $C_x$ the circle around $x$ through them, a circle with no site strictly inside.

- (F1) The circumcircles of the triangles of $D$ are exactly the circles $C_x$, and the triangles with circumcircle $C_x$ triangulate the convex polygon $F_x = \mathrm{conv}(Q_x)$.
- (F2) The cells $V_p$ and $V_q$ share an edge exactly when $pq$ is a side of some $F_x$. The finite ends of that edge are exactly the vertices $x$ with $pq$ a side of $F_x$, and it is a ray exactly when $pq$ is an edge of the hull boundary.
- (F3) The faces $F_x$ form a subdivision of the hull. Each side of a face is a single edge of $D$, and is a side of two faces, or of one face if it is on the hull boundary.

**Vertices (lines L2 and L3).** By (F1), the set of circumcenters of the triangles of $D$ is the set of centers of the circles $C_x$, which is the set of Voronoi vertices. Line L3 keeps each value once.

**Edges (lines L4 to L7).** Let $pq$ be an edge of $D$.

- If $pq$ has one triangle $t$, it lies on the hull boundary, so it is a side of the face of $t$, and by (F2) the cells of $p$ and $q$ share a ray whose finite end is $c(t)$. It lies on the bisector of $p$ and $q$ and goes away from the hull. Line L5 records it.
- If $pq$ has two triangles $t$ and $t'$ with $c(t) = c(t')$, then both triangles belong to the same face $F_x$, so $pq$ is a diagonal of $F_x$ and not a side of any face, since by (F3) the sides of faces are not inside faces. By (F2), $V_p$ and $V_q$ share no edge. Line L6 skips it.
- If $c(t) \ne c(t')$, then $t$ and $t'$ belong to different faces, so $pq$ is a side of both faces $F_{c(t)}$ and $F_{c(t')}$, and of no other face by (F3). By (F2) the edge of $V_p$ and $V_q$ is the segment with ends $c(t)$ and $c(t')$. Line L7 records it.

Conversely, every Voronoi edge is dual to a side $pq$ of a face by (F2), and that side is an edge of $D$ by (F3), so line L4 visits it. Each pair is recorded once, because the code records an inner edge only for the direction $u < v$.

**Cells.** Let the triangles of $D$ with corner $p$ be $t_1, \ldots, t_m$ in counterclockwise order around $p$, where $t_i$ and $t_{i+1}$ share the edge $p a_i$. A vertex $x$ is on the boundary of $V_p$ exactly when $p \in Q_x$, that is, when $p$ is a corner of $F_x$, and then some triangle of $D$ in $F_x$ has corner $p$, because the triangles of $F_x$ cover a neighbourhood of $p$ in $F_x$. So the distinct values $c(t_i)$ are the vertices of $V_p$. Consecutive values $c(t_i) \ne c(t_{i+1})$ are, by the edge argument, the two ends of the Voronoi edge of $V_p$ dual to $p a_i$. A run of equal values belongs to one face, and the triangles of one face at $p$ are consecutive around $p$, because the face is convex and $p$ is one of its corners. So the list, with repeats dropped, walks along the boundary of $V_p$ from vertex to vertex through its edges. The edge dual to $p a_i$ has outer normal $a_i - p$, and the neighbours $a_i$ turn counterclockwise around $p$; the outer normals of the sides of a convex polygon turn counterclockwise in the counterclockwise order of its sides, so the walk is counterclockwise. If $p$ is an inner site, its triangles surround it and the walk closes; the cell is bounded by Lemma 3 of the [complexity theorem](/voronoi-complexity-theorem/). If $p$ is on the hull boundary, the walk starts and ends at the two hull edges at $p$, whose duals are rays, and the cell is unbounded.

**Nearest site.** Each step of the walk moves to a site strictly closer to $q$, so no site is visited twice and the walk stops. It remains to show that it stops at a nearest site, that is: *if $p$ is not a nearest site of $q$, then some Delaunay neighbour of $p$ in $D$ is strictly closer to $q$.*

Let $p$ not be nearest, so $q \notin V_p$. The segment from $p$ to $q$ starts in $V_p$, which is closed and convex, so it leaves $V_p$ at a point $y$: the points $y + \varepsilon u$ with $u = (q - p)/|q - p|$ and small $\varepsilon > 0$ are not in $V_p$. Let $Q_y$ be the nearest sites of $y$, at distance $r$; it holds $p$. All other sites are farther than $r$ from $y$, so for small $\varepsilon$ the nearest sites of $y + \varepsilon u$ are in $Q_y$, and for $s \in Q_y$, $|y + \varepsilon u - s|^2 = r^2 - 2 \varepsilon \, u \cdot (s - y) + \varepsilon^2$. So these nearest sites are the sites of $Q_y$ with the largest value $g(s) = u \cdot (s - y)$, and as $y + \varepsilon u \notin V_p$, some $s^* \in Q_y$ has $g(s^*) > g(p)$.

If $Q_y = \{p, s^*\}$, then $y$ is on the Voronoi edge of $p$ and $s^*$, and $p s^*$ is an edge of $D$ by (F2) and (F3). Otherwise $y$ is a vertex, and the sites of $Q_y$ lie on the circle $C_y$. On this circle, $g$ is the cosine of the angle to the direction $u$, times $r$, so the set of points $z$ of the circle with $g(z) > g(p)$ is an open arc $A$ with $p$ at one end. Move along the circle from $p$ into $A$, and let $p'$ be the first site of $Q_y$ met. Since $s^* \in A$, $p'$ is met at or before $s^*$, so $p' \in A$ and $g(p') > g(p)$. The sites $p$ and $p'$ are consecutive on $C_y$, so $pp'$ is a side of $F_y$, and an edge of $D$ by (F3). In both cases there is a neighbour $s$ of $p$ in $D$ with $|y - s| = |y - p|$ and $u \cdot (s - y) > u \cdot (p - y)$.

Now the function $\psi(z) = |z - s|^2 - |z - p|^2$ is affine, $\psi(y) = 0$, and its derivative in the direction $u$ is $-2 u \cdot (s - p) < 0$. The point $q$ is $y + \lambda u$ for some $\lambda > 0$, since $y$ is on the segment before $q$ and $y \ne q$, because $y \in V_p$ and $q \notin V_p$. So $\psi(q) < 0$, that is, $|q - s| < |q - p|$. $\square$

**Collinear sites.** If all sites are on one line, sorted along it as $p_1, \ldots, p_n$, the cell of $p_i$ is the strip between the bisectors of $p_{i-1}p_i$ and $p_i p_{i+1}$, so the diagram is the $n - 1$ bisectors of consecutive sites and has no vertex; the code stores exactly these, with both ends at infinity. Its adjacency lists are the path $p_1, \ldots, p_n$, and the nearest walk on a path of sites sorted along a line reaches a nearest site by the same argument with $Q_y = \{p, s\}$. With one site the cell is the plane, and with two sites the diagram is their bisector. $\blacksquare$
