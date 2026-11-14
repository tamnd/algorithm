---
title: Delaunay minimises the interpolation error of |x|^2, and each ODT step lowers it
proves: [correctness, termination]
status: full
---

**Setting.** $\Omega$ is a convex polygon. A triangulation $T$ of a finite point set $V \subset \Omega$ that contains the corners of $\Omega$ is a set of triangles with vertices in $V$ that cover $\Omega$, have disjoint interiors and meet edge to edge, and that use every point of $V$ as a vertex. Let $f(x) = |x|^2$ and let $f_{I,T}$ be the piecewise linear function that agrees with $f$ at the vertices of $T$. The energy is

$$E(T) = \int_\Omega \bigl(f_{I,T}(x) - f(x)\bigr)\,dx.$$

Because $f$ is convex, $f_{I,T} \ge f$ on each triangle, so $E(T)$ is the $L^1$ norm of the interpolation error.

**Lemma 1 (one triangle).** For a triangle $\tau$ with vertices $a, b, c$, area $|\tau|$ and edge lengths $\ell_1, \ell_2, \ell_3$,

$$\int_\tau f_{I} = \frac{|\tau|}{3}\bigl(|a|^2 + |b|^2 + |c|^2\bigr), \qquad \int_\tau (f_I - f) = \frac{|\tau|}{12}\bigl(\ell_1^2 + \ell_2^2 + \ell_3^2\bigr).$$

*Proof.* A linear function integrates to $|\tau|$ times its value at the centroid, which is the mean of the three vertex values. For the second formula, $f_I - f$ is a quadratic, and the rule $\int_\tau q = \frac{|\tau|}{3}\sum_{\text{edges}} q(\text{midpoint})$ is exact for quadratics. At the midpoint $m$ of the edge $ab$, $f_I(m) - f(m) = \frac{|a|^2 + |b|^2}{2} - \bigl|\frac{a+b}{2}\bigr|^2 = \frac{|a - b|^2}{4}$. Summing over the three edges and multiplying by $|\tau|/3$ gives the claim. $\square$

**Lemma 2 (lifting).** Let $\tau = abc$ and let $\ell_\tau$ be the affine function with $\ell_\tau = f$ at $a$, $b$, $c$. Then for every point $p$, $f(p) - \ell_\tau(p) = |p - z|^2 - R^2$, where $z$ and $R$ are the circumcentre and circumradius of $\tau$. So the lifted point $(p, |p|^2)$ lies below the plane of the lifted triangle if and only if $p$ is strictly inside the circumcircle.

*Proof.* $f - \ell_\tau$ is a quadratic with leading part $|x|^2$, so it equals $|x - z'|^2 - r$ for some $z'$ and $r$. It is zero at $a$, $b$ and $c$, so these three points are at distance $\sqrt r$ from $z'$. Thus $z' = z$ and $r = R^2$. $\square$

This is the [paraboloid lifting map](/paraboloid-lifting-map/), and it is the reason the [in-circle test](/in-circle-test/) is a $3 \times 3$ determinant.

**Theorem 1 (Delaunay is optimal for fixed vertices).** For every triangulation $T$ of $V$, $E(T) \ge E(D)$ for any Delaunay triangulation $D$ of $V$. Equality holds if and only if no point of $V$ lies strictly inside the circumcircle of a triangle of $T$, that is, if and only if $T$ is itself a Delaunay triangulation.

*Proof.* Let $g$ be the lower convex envelope of the lifted points over $\Omega$:

$$g(x) = \min\Bigl\{\sum_k \lambda_k |v_k|^2 \;:\; v_k \in V,\ \lambda_k \ge 0,\ \sum_k \lambda_k = 1,\ \sum_k \lambda_k v_k = x\Bigr\}.$$

On a triangle of $T$ that contains $x$, $f_{I,T}(x) = \sum \lambda_k |v_k|^2$ with the barycentric coordinates of $x$, which is one of the candidates in the minimum. So $f_{I,T} \ge g$ everywhere.

For a Delaunay triangulation $D$, take a triangle $\tau$ of $D$. No point of $V$ is strictly inside its circumcircle, so by Lemma 2 every lifted point lies on or above the plane $\ell_\tau$. Any convex combination of lifted points then lies on or above that plane, so $g \ge \ell_\tau = f_{I,D}$ on $\tau$. With the first part, $f_{I,D} = g$ on $\Omega$.

Hence $E(T) - E(D) = \int_\Omega (f_{I,T} - g) \ge 0$. If equality holds, the integrand is continuous and nonnegative with zero integral, so $f_{I,T} = g$ on $\Omega$. Suppose a point $p \in V$ were strictly inside the circumcircle of a triangle $\tau$ of $T$. By Lemma 2, $|p|^2 < \ell_\tau(p)$. Take $x$ in the interior of $\tau$ and $s > 0$ small, and write $x$ as $(1 - s)$ times a point $y$ plus $s$ times $p$, where $y = (x - s p)/(1 - s)$ is still in $\tau$. Then $g(x) \le (1 - s)\ell_\tau(y) + s|p|^2 < (1 - s)\ell_\tau(y) + s\ell_\tau(p) = \ell_\tau(x) = f_{I,T}(x)$, a contradiction. Conversely, if no point is strictly inside any circumcircle of $T$, the argument above for $D$ applies to $T$ and gives $f_{I,T} = g$. $\square$

**Lemma 3 (flippable edges).** Let $ij$ be an interior edge with triangles $ija$ and $jib$, both counterclockwise. If $b$ is strictly inside the circumcircle of $ija$, then the quadrilateral $i, b, j, a$ is strictly convex, so the edge can be flipped to $ab$.

*Proof.* The chord $ij$ cuts the open disk into two parts. Since $b$ is on the other side of the line $ij$ from $a$, it is in the part away from $a$. That part is bounded by the chord and an arc from $i$ to $j$. The rays from $a$ through $i$ and through $j$ meet the circle only at $i$ and $j$, so the whole part lies in the open angle at $a$ between them, beyond the chord. So the segment $ab$ crosses the open segment $ij$, which means that both $a, i, b$ and $b, j, a$ are counterclockwise. $\square$

**Theorem 2 (a flip lowers the energy).** Flipping an edge $ij$ as in Lemma 3 lowers $E$ strictly.

*Proof.* Only the two triangles on the quadrilateral $Q = i, b, j, a$ change. The four points are in convex position by Lemma 3, so both pairs of triangles cover $Q$, and the change in $E$ is the change of $\int_Q (f_I - f)$. Apply Theorem 1 to the point set $\{i, j, a, b\}$ on the convex polygon $Q$. The old pair is not Delaunay, because $b$ is inside the circumcircle of $ija$. A Delaunay triangulation of four points in convex position exists and is one of the two pairs, so it is the new pair, and the inequality of Theorem 1 is strict. $\square$

**Theorem 3 (the vertex move is a descent step).** Let $x$ be a vertex not on the boundary of $\Omega$, with star triangles $(x, a_\tau, b_\tau)$, all counterclockwise, whose union is the star polygon $\Omega_x$. For a point $y$ let $A_\tau(y) = \frac12\,\mathrm{orient}(y, a_\tau, b_\tau)$, the signed area, and $S_\tau = |a_\tau|^2 + |b_\tau|^2$. Put

$$\Phi(y) = \sum_\tau A_\tau(y)\bigl(|y|^2 + S_\tau\bigr).$$

(a) If every $A_\tau(y) > 0$ (that is, $y$ is in the kernel $K$ of the star), then moving $x$ to $y$ gives a valid triangulation, and $E$ changes by $\frac13\bigl(\Phi(y) - \Phi(x)\bigr)$.

(b) $\Phi(y) = |\Omega_x|\,|y - y^*|^2 + \text{const}$, where $y^* = -\frac{1}{2|\Omega_x|}\sum_\tau S_\tau \nabla A_\tau$ and $\nabla A_\tau = \frac12\bigl(a_{\tau,2} - b_{\tau,2},\ b_{\tau,1} - a_{\tau,1}\bigr)$ is constant.

(c) For $0 < t \le 1$ and $y_t = x + t(y^* - x)$, $\Phi(y_t) - \Phi(x) = -|\Omega_x|\,t(2 - t)\,|x - y^*|^2$. So if $y^* \ne x$, every $y_t$ in $K$ lowers $E$ strictly, and $y_t \in K$ for all small $t$.

*Proof.* (a) If every star triangle stays counterclockwise, the triangles of the star still tile $\Omega_x$, since their outer edges are the fixed edges of the link polygon and consecutive triangles share the edges $x a_\tau$. The other triangles do not change. By Lemma 1, $E = \sum_\tau \frac{|\tau|}{3}\sum_{v \in \tau} |v|^2 - \int_\Omega f$, and only the star terms depend on $x$; with $|\tau| = A_\tau(y)$ they sum to $\frac13\Phi(y)$.

(b) $A_\tau$ is affine in $y$, and $\sum_\tau A_\tau(y)$ is the shoelace sum of the closed link polygon taken from the point $y$, which equals $|\Omega_x|$ for every $y$. So $\Phi(y) = |\Omega_x|\,|y|^2 + \sum_\tau S_\tau A_\tau(y)$, a quadratic with Hessian $2|\Omega_x| I$ and gradient zero at $y^*$.

(c) By (b), $\Phi(y_t) - \Phi(x) = |\Omega_x|\bigl((1 - t)^2 - 1\bigr)|x - y^*|^2$. The kernel $K$ is an intersection of open half-planes, so it is open and convex, and it contains $x$. $\square$

A computation from the circumcentre formula shows that $y^*$ is the area-weighted mean of the circumcentres of the star triangles taken at $y = x$; the tests check this identity exactly. The implementation tries $t = 1, \frac12, \frac14, \dots$, rounds $y_t$ to a dyadic grid, and accepts the rounded point only if the exact tests $A_\tau > 0$ and $\Phi(y) < \Phi(x)$ pass. So an accepted move lowers $E$ strictly, and a rejected vertex leaves $E$ unchanged.

**Theorem 4 (the ODT loop).** Each sweep of ODT-SMOOTH keeps a valid triangulation of $\Omega$, never increases $E$, and ends with a Delaunay triangulation of the current points. Each call of the flip loop stops.

*Proof.* Moves keep validity by Theorem 3(a) and do not increase $E$ by Theorem 3(c) and the exact acceptance test. Each flip keeps validity by Lemma 3 and lowers $E$ strictly by Theorem 2. The vertex set is fixed during the flip loop and has finitely many triangulations, and no triangulation repeats because $E$ goes strictly down, so the flip loop stops. It stops only when every interior edge is locally Delaunay, and a triangulation whose edges are all locally Delaunay is a [Delaunay triangulation](/delaunay-triangulation/) (the Delaunay lemma, Cheng, Dey and Shewchuk, chapter 2). The number of sweeps is a parameter, so the whole method stops. $\square$

**What is not proved.** $E$ is not convex in all vertex positions together, so the sweeps reach a point where no single move helps, not a global minimum. $E$ measures the size of the triangles, not their shape, so no angle bound follows. In a measured run on the square $[0,8]^2$ with only its four corners on the boundary and 20 free points, $E$ fell from 202.5 to 82.3 and the smallest angle fell from $3.0°$ to about $6 \cdot 10^{-6}$ degrees, as free points crowded the long boundary edges. With 28 fixed points on the sides, the smallest angle rose from $7.3°$ to $29.1°$. Both are measurements.
