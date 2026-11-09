---
title: The alpha values computed from the Delaunay triangulation are correct
proves: [correctness, termination]
status: full
---

**Claim.** Let $P$ be a finite set of points with no three on a line and no four on a circle, $|P| \ge 3$, and let $D$ be its Delaunay triangulation. For each simplex $\sigma$ of $D$, BUILD-FILTRATION assigns $\rho(\sigma) = \min_{z \in V(\sigma)} |z - p|^2$, where $p$ is a vertex of $\sigma$ and $V(\sigma)$ is the intersection of the closed Voronoi cells of the vertices of $\sigma$. Moreover $\rho(\tau) \le \rho(\sigma)$ for every face $\tau$ of $\sigma$, so each $K_\alpha = \{\sigma : \rho(\sigma) \le \alpha\}$ is a simplicial complex. The procedure ends after $O(n)$ steps once $D$ is known.

**Notation.** $V(p) = \{z : |z - p| \le |z - q| \text{ for all } q \in P\}$. For two distinct points $u, v$, $m = (u + v)/2$ is the midpoint and $B_{uv}$ the open disk with center $m$ and radius $|u - v|/2$, the diametral disk. We use the [Voronoi-Delaunay duality](/voronoi-delaunay-duality/): in general position, $V(t)$ for a triangle $t$ of $D$ is the single point $c_t$, the circumcenter of $t$; for an edge $uv$ of $D$, $V(\{u, v\})$ is the Voronoi edge, a segment on the bisector of $u$ and $v$ whose ends are the circumcenters of the two triangles on $uv$, or a ray from the circumcenter of the one triangle on $uv$ when $uv$ is a hull edge.

**Lemma 1 (vertices and triangles).** $\rho(\{p\}) = 0$ and $\rho(t) = R_t^2$, the squared circumradius.

*Proof.* $p \in V(p)$, so the minimum of $|z - p|^2$ over $V(p)$ is $0$. For a triangle $V(t) = \{c_t\}$ and $|c_t - p| = R_t$ for each vertex $p$. $\square$

**Lemma 2 (distance along the bisector).** For $z$ on the bisector of $u$ and $v$, $|z - u|^2 = |m - u|^2 + |z - m|^2$. So $|z - u|^2$ is a strictly convex function along the bisector with its minimum $|u - v|^2 / 4$ at $m$.

*Proof.* $z - m$ is orthogonal to $u - m$, and Pythagoras gives the formula. $\square$

**Lemma 3 (the midpoint test).** $m \in V(\{u, v\})$ exactly when no point of $P$ lies in $B_{uv}$.

*Proof.* $m$ is on the bisector. It is in $V(u) \cap V(v)$ exactly when no $q \in P$ satisfies $|m - q| < |m - u| = |u - v| / 2$, that is, when no $q$ lies in $B_{uv}$. $\square$

**Lemma 4 (opposite vertices decide).** Let $uv$ be an edge of $D$. If some $q \in P$ lies in $B_{uv}$, then a vertex of a triangle on $uv$, opposite $uv$, lies in $B_{uv}$.

*Proof.* $q$ is not on the line $uv$: a point of $B_{uv}$ on that line is strictly between $u$ and $v$, and no point of $P$ is strictly inside an edge of a triangulation of $P$ with no three points collinear. So $q$ is strictly on one side, say the left of $u \to v$. The convex hull of $P$ contains $q$, so $uv$ is not a hull edge with nothing on its left, and there is a triangle $uvw$ of $D$ on the left. Let $C$ be its open circumdisk. Use affine functions as in the [lifting map](/paraboloid-lifting-map/): for an open disk $X$ through $u$ and $v$ let $f_X$ be the affine function with $z \in X \iff |z|^2 < f_X(z)$. Then $f_C - f_{B}$, with $B = B_{uv}$, is zero on the line $uv$, so it has one sign on the open left side. If $f_C \ge f_B$ there, then $q \in B$ gives $|q|^2 < f_B(q) \le f_C(q)$, so $q \in C$, which contradicts the empty circle property of $D$. So $f_C < f_B$ on the open left side, and $w$, which is on the left and has $|w|^2 = f_C(w)$, satisfies $|w|^2 < f_B(w)$: $w \in B_{uv}$. $\square$

**Lemma 5 (edges).** For an edge $e = uv$ of $D$, lines L5 to L7 assign $\rho(e)$.

*Proof.* By Lemmas 3 and 4, the test of line L5 is true exactly when $m \in V(e)$. In that case Lemma 2 gives $\rho(e) = |u - v|^2 / 4$, which is line L6. Otherwise $m$ is on the bisector but outside the segment or ray $V(e)$. A strictly convex function on a line, restricted to a closed interval that does not hold its minimum point, has its minimum at the end of the interval nearer to that point. That end is the circumcenter $c_t$ of a triangle $t$ on $e$, and the value is $R_t^2$. Every other end gives a larger value. So $\rho(e) = \min_t R_t^2$ over the triangles $t$ on $e$, which is line L7. $\square$

**Lemma 6 (faces enter first).** If $\tau \subseteq \sigma$ then $\rho(\tau) \le \rho(\sigma)$.

*Proof.* $V(\sigma) \subseteq V(\tau)$, because $V(\sigma)$ is an intersection over more cells. Take $p \in \tau$; the minimum of $|z - p|^2$ over a larger set is no larger. $\square$

**Proof of the claim.** Lemmas 1 and 5 show that every value is right. Line L8 sorts the simplices, so $\mathrm{complex}(\alpha)$, the set with value at most $\alpha$, is $K_\alpha$, and by Lemma 6 it is closed under taking faces. For collinear input, $D$ is the sorted path, every Voronoi edge is a full line through the midpoint, and every edge is Gabriel, which the code also gives. **Termination.** Lines L2 to L7 do one step per simplex of $D$, and there are fewer than $6n$ of them.

**Degenerate input.** With four or more points on a circle, the code uses the triangulation of its Delaunay code. A triangle of that triangulation still has $V(t) = \{c_t\}$, so Lemma 1 holds. A diagonal $uv$ of a cocircular polygon has $V(\{u, v\}) = \{c\}$, the common center; if $uv$ is a diameter, it is Gabriel and $|u - v|^2/4 = R^2$, and otherwise the opposite vertex on the shorter arc is in $B_{uv}$ and line L7 gives $R^2$. So the values are the nerve values in that case too; the tests check them against a direct minimum over each Voronoi edge. $\blacksquare$
