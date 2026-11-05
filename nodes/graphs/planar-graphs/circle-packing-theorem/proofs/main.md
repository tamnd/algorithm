---
title: Proof of the circle packing theorem
proves: [statement]
status: full
---

We prove that every finite simple planar graph $G$ is the tangency graph of a circle packing. The proof follows the variational method of Colin de Verdière. Discs are closed; a packing has discs with pairwise disjoint interiors. Two discs with disjoint interiors *touch* if they have a common point; then they have exactly one.

**Fact 0.** Three discs with pairwise disjoint interiors have no common point. Indeed, if $D_1$ and $D_2$ touch at $p$, they lie on the two sides of their common tangent line at $p$, and every disc that contains $p$ and has nonempty interior meets the interior of $D_1$ or of $D_2$ near $p$.

## Step 1: reduction to triangulations

If $G$ is a single vertex, one disc is a packing. If $G = K_2$, two touching discs are a packing. If $G$ is not connected, pack each component, scale each packing to lie in a unit square, and place the squares far apart; discs of different components then do not meet.

**Lemma 1.** Every connected simple plane graph $G$ with $n \ge 3$ vertices is an induced subgraph of a simple plane triangulation $T$.

*Proof.* Each face $F$ of $G$ has a boundary walk $w_0, w_1, \ldots, w_{k-1}$ (indices mod $k$), with consecutive vertices adjacent and different. Since $G$ is connected and has at least two edges, $k \ge 3$. Inside $F$ add new vertices $x_0, \ldots, x_{k-1}$, forming a cycle, and a vertex $z$ joined to all $x_i$; join $x_i$ to $w_i$ and to $w_{i+1}$. These edges can be drawn inside $F$ without crossings, following the walk. The region of $F$ is now cut into the triangles $w_i w_{i+1} x_i$, $x_{i-1} w_i x_i$ and $z x_i x_{i+1}$. No edge between two old vertices is added, and no parallel edge arises, since $w_i \ne w_{i+1}$ and the new vertices of different faces are different. So the result is a simple plane graph with only triangular faces, in which $G$ is induced. $\square$

If $(D_v)$ is a packing with tangency graph $T$, the discs of the vertices of $G$ form a packing whose tangency graph is the subgraph of $T$ induced by $V(G)$, which is $G$. So it suffices to prove the theorem for a simple plane triangulation $T$ with $n \ge 4$ vertices (for $n = 3$ take three pairwise touching unit discs). Fix the outer face $a b c$, and let $I$ be the set of the $n - 3$ inner vertices. By [Euler's formula](/euler-formula/) $T$ has $2n - 4$ faces, so $2n - 5$ inner faces. The orientation of the plane gives each inner face a counterclockwise order of its three vertices.

## Step 2: angles of a triangle of discs

For radii $r_1, r_2, r_3 > 0$, the centers of three pairwise touching discs form a triangle with sides $r_1 + r_2$, $r_2 + r_3$, $r_1 + r_3$; these lengths satisfy the strict triangle inequality. Let $\alpha_i$ be its angle at the center of disc $i$ and $s = r_1 + r_2 + r_3$. The law of cosines gives

$$\cos \alpha_1 = 1 - \frac{2 r_2 r_3}{(r_1 + r_2)(r_1 + r_3)}, \qquad \tan^2 \frac{\alpha_1}{2} = \frac{r_2 r_3}{r_1 s}.$$

**Lemma 2.** Write $r_i = e^{u_i}$. For $i \ne j$, with $k$ the third index,

$$\frac{\partial \alpha_i}{\partial u_j} = c_{ij} := \frac{1}{r_i + r_j} \sqrt{\frac{r_1 r_2 r_3}{s}} > 0,$$

which is symmetric in $i$ and $j$, and $\partial \alpha_i / \partial u_i = -\sum_{j \ne i} c_{ij}$.

*Proof.* Take $i = 1$, $j = 2$, and $t = \tan(\alpha_1/2)$. Then $\partial \log t^2 / \partial u_2 = r_2 \, \partial (\log r_2 - \log s) / \partial r_2 = 1 - r_2/s = (r_1 + r_3)/s$. Since $\alpha_1 = 2 \arctan t$, $\partial \alpha_1 / \partial u_2 = \frac{t}{1 + t^2} \cdot \frac{r_1 + r_3}{s}$. Now $1 + t^2 = (r_1 s + r_2 r_3)/(r_1 s) = (r_1 + r_2)(r_1 + r_3)/(r_1 s)$, so

$$\frac{\partial \alpha_1}{\partial u_2} = \sqrt{\frac{r_2 r_3}{r_1 s}} \cdot \frac{r_1 s}{(r_1 + r_2)(r_1 + r_3)} \cdot \frac{r_1 + r_3}{s} = \frac{r_1}{r_1 + r_2} \sqrt{\frac{r_2 r_3}{r_1 s}} = c_{12}.$$

The other pairs follow by symmetry. The angles add up to $\pi$ for all $u$, so the derivatives of $\alpha_1 + \alpha_2 + \alpha_3$ vanish, and the diagonal entries are as stated. $\square$

**Lemma 3 (limits).** Fix $w \in \mathbb{R}^3$ and put $u = t w$. Then, as $t \to \infty$, $w_1 \alpha_1 + w_2 \alpha_2 + w_3 \alpha_3 \to \pi \min_i w_i$.

*Proof.* Order so that $w_1 \ge w_2 \ge w_3$. From the cosine formula, $\alpha_i \to 0$ if $r_j / r_i \to 0$ for some $j \ne i$, and $\alpha_i \to \pi$ if $r_i / r_j \to 0$ for both $j \ne i$. If $w_2 > w_3$: $\alpha_1, \alpha_2 \to 0$ and $\alpha_3 \to \pi$, so the limit is $\pi w_3$. If $w_1 > w_2 = w_3$: $\alpha_1 \to 0$, and $\alpha_2 = \alpha_3$ by symmetry, so both tend to $\pi/2$, and the limit is $\pi w_2 = \pi w_3$. If $w_1 = w_2 = w_3$: the radii are equal, every angle is $\pi/3$, and the sum is $\pi w_3$. $\square$

## Step 3: the functional

On one triangle, by Lemma 2 the form $\sum_i \alpha_i \, du_i$ on $\mathbb{R}^3$ has a symmetric derivative matrix, so it is closed, and since $\mathbb{R}^3$ is simply connected it is the differential of a smooth function $F(u_1, u_2, u_3)$ with $F(0) = 0$. The Hessian $H$ of $F$ is the matrix of Lemma 2, so for $x \in \mathbb{R}^3$

$$x^{\mathsf T} H x = -\sum_{i < j} c_{ij} (x_i - x_j)^2 \le 0.$$

For $u \in \mathbb{R}^I$, extend $u$ by $u_a = u_b = u_c = 0$ (outer radii 1) and define

$$\Phi(u) = \sum_{\text{inner faces } f} F(u|_f) - 2\pi \sum_{v \in I} u_v,$$

where $u|_f$ is $u$ on the three vertices of $f$. For an inner vertex $v$, $\partial \Phi / \partial u_v = \theta_v(u) - 2\pi$, where $\theta_v$ is the sum of the angles at $v$ over the faces at $v$.

**Lemma 4.** $\Phi$ is strictly concave on $\mathbb{R}^I$.

*Proof.* For $x \in \mathbb{R}^I$, extended by 0 on $a, b, c$, the Hessian form is $-\sum_f \sum_{i < j \in f} c^f_{ij} (x_i - x_j)^2$. It vanishes only if $x_i = x_j$ for every edge $ij$, so $x$ is constant on the connected graph $T$, and $x = 0$ because $x_a = 0$. $\square$

## Step 4: a maximum exists

**Lemma 5.** (a) A set $S \subseteq I$ with $k \ge 1$ vertices contains all three vertices of fewer than $2k$ inner faces. (b) A nonempty set $U \subseteq I$ meets more than $2|U|$ inner faces.

*Proof.* (a) A face of $T$ whose three vertices lie in $S$ is a bounded face of the plane graph $T[S]$, because its interior contains no vertex or edge of $T$. Different faces of $T$ give different faces of $T[S]$. If $k \le 2$ there is no such face. If $k \ge 3$, the simple plane graph $T[S]$ has at most $2k - 4$ faces, one of them unbounded, so there are at most $2k - 5 < 2k$ such faces.

(b) Let $W = V \setminus U$, which contains $a, b, c$. As in (a), the inner faces of $T$ with all vertices in $W$ are bounded faces of $T[W]$, which has at most $2|W| - 4$ faces. The unbounded face of $T[W]$ is outside the triangle $a b c$. A vertex of $U$ lies inside the triangle $a b c$, so it lies in a bounded face of $T[W]$, and that face is not a face of $T$. So at most $2|W| - 6$ inner faces of $T$ avoid $U$, and at least $(2n - 5) - (2|W| - 6) = 2|U| + 1$ meet $U$. $\square$

**Lemma 6.** For every $w \in \mathbb{R}^I \setminus \{0\}$, $\Phi(t w) \to -\infty$ as $t \to \infty$.

*Proof.* The function $g(t) = \Phi(t w)$ is concave, and $g'(t) = \sum_f \sum_{v \in f} w_v \alpha^f_v(t w) - 2\pi \sum_{v \in I} w_v$ with $w = 0$ on $a, b, c$. By Lemma 3, $g'(t) \to L = \pi \sum_f \min_{v \in f} w_v - 2\pi \sum_{v \in I} w_v$. Write each real number $y$ as $y = \int_0^\infty [y \ge \lambda] \, d\lambda - \int_{-\infty}^0 [y < \lambda] \, d\lambda$, with $[\cdot]$ equal to 1 or 0. For $\lambda > 0$ let $S_\lambda = \{v : w_v \ge \lambda\} \subseteq I$, and for $\lambda \le 0$ let $U_\lambda = \{v : w_v < \lambda\} \subseteq I$. Then $\min_{v \in f} w_v \ge \lambda$ exactly when $f \subseteq S_\lambda$, and $\min_{v \in f} w_v < \lambda$ exactly when $f$ meets $U_\lambda$. So

$$\frac{L}{\pi} = \int_0^\infty \bigl(N_{\subseteq}(S_\lambda) - 2|S_\lambda|\bigr) d\lambda - \int_{-\infty}^0 \bigl(N_{\cap}(U_\lambda) - 2|U_\lambda|\bigr) d\lambda,$$

where $N_{\subseteq}(S)$ counts the inner faces inside $S$ and $N_{\cap}(U)$ the inner faces meeting $U$. By Lemma 5 both integrands give a negative contribution whenever the set is nonempty, and they are 0 when it is empty. Since $w \ne 0$, one of the sets is nonempty for all $\lambda$ in an interval of positive length. So $L < 0$, and since $g$ is concave with $g' \to L < 0$, $g(t) \to -\infty$. $\square$

Let $K = \{u : \Phi(u) \ge \Phi(0)\}$. It is closed and convex. If it were unbounded, it would contain a ray $\{t w : t \ge 0\}$ with $w \ne 0$ (a closed convex unbounded set contains a ray from each of its points), which contradicts Lemma 6. So $K$ is compact, and $\Phi$ attains its maximum at some $u^*$. There the gradient vanishes: $\theta_v(u^*) = 2\pi$ for every $v \in I$. By Lemma 4 the maximum, and so the radii with $r_a = r_b = r_c = 1$, are unique. Put $r_v = e^{u^*_v}$.

## Step 5: layout

For each inner face $f = ijk$ (counterclockwise) let $\Delta_f$ be the triangle with sides $r_i + r_j$, $r_j + r_k$, $r_i + r_k$. The inner faces of $T$ form a closed disc $|T|$ (the triangle $a b c$ with its interior). Place one triangle with the correct orientation, then place each face that shares an edge with a placed face across that edge, again with the correct orientation. Around an inner vertex $v$ the triangles at $v$ are placed in rotation order with angles that add up to $\theta_v = 2\pi$, so going once around $v$ brings each triangle back to its first position. Since $|T|$ is simply connected and these loops around inner vertices generate all closed paths of faces, the placement does not depend on the order. This gives a continuous map $\phi : |T| \to \mathbb{R}^2$ that is linear and orientation preserving on each face. It is one-to-one near every point: inside a face and on an inner edge clearly, at an inner vertex because the angles there add up to exactly $2\pi$, and at an outer vertex $x$ because its angle sum $\theta_x$ is less than $2\pi$, as follows.

The angles of all inner faces add up to $\pi (2n - 5)$, and the inner vertices use $2\pi (n - 3)$. So $\theta_a + \theta_b + \theta_c = \pi$, and each is in $(0, \pi)$. The boundary of $|T|$ is mapped to a closed polygon with sides $r_a + r_b = r_b + r_c = r_a + r_c = 2$ and interior angles $\theta_a, \theta_b, \theta_c$; with all angles less than $\pi$ this is a triangle, and since its sides are equal, it is the equilateral triangle $E$ with side 2, traversed once counterclockwise.

For a point $p \notin \partial E$, the number of preimages of $p$ under $\phi$ equals the winding number of $\phi(\partial |T|) = \partial E$ around $p$, because $\phi$ is an orientation preserving local homeomorphism (this is the degree of a map of a disc). So points inside $E$ have exactly one preimage and points outside have none. A point of $\partial E$ has no preimage in the interior of $|T|$, since a neighbourhood of that preimage would be mapped onto a neighbourhood of the point, which contains points outside $E$. So $\phi$ is one-to-one and continuous on the compact $|T|$, hence a homeomorphism onto $E$, and the triangles $\phi(f)$ tile $E$ without overlap. Put $p_v = \phi(v)$ and $D_v$ the disc with center $p_v$ and radius $r_v$.

## Step 6: the discs form the packing

For an edge $uv$, $|p_u - p_v| = r_u + r_v$, so $D_u$ and $D_v$ touch.

**Lemma 7.** In a face triangle $\phi(f)$ with $f = x y z$, $D_x \cap \phi(f)$ is the sector of $D_x$ in the angle of the triangle at $p_x$, and $D_x$ meets the side $p_y p_z$ at no point.

*Proof.* The segment $p_y p_z$ has length $r_y + r_z$, so it is the union of the radius of $D_y$ and the radius of $D_z$ toward each other, and lies in $D_y \cup D_z$. The disc $D_x$ touches $D_y$ only at a point of the segment $p_x p_y$, and $D_z$ only at a point of $p_x p_z$; by Fact 0 neither point is on $p_y p_z$. So $D_x$ misses the side $p_y p_z$. If a point $q$ of the sector were outside the triangle, the segment from $p_x$ to $q$, which lies in $D_x$, would cross the side $p_y p_z$. $\square$

For every vertex $v$, $D_v \cap E$ is the union of the sectors of $D_v$ in the faces at $v$. For an inner vertex this holds because the angles at $v$ add up to $2\pi$, so the sectors make up the whole disc and $D_v \subseteq E$. For an outer vertex the faces at $v$ fill the angle $\pi/3$ of $E$ at $p_v$, and $E$ lies in that angle. Now let $u \ne v$ be vertices with a common point $q \in D_u \cap D_v$.

If $q$ is outside $E$, then $u$ and $v$ are outer, so $uv$ is an edge. Otherwise $q$ is in a sector of $u$ in some face $f$ and in a sector of $v$ in some face $g$. If $f = g$, then $u$ and $v$ are two vertices of one face, so $uv$ is an edge. If $f \ne g$, the faces have disjoint interiors, so $q$ lies on the boundary of both, which is in the union of the edges. By Lemma 7, a sector of $u$ meets the boundary of its face only on the two sides at $p_u$, at distance at most $r_u$ from $p_u$. So $q$ lies on an edge $e$ at $u$, at distance at most $r_u$ from $p_u$, and on an edge $e'$ at $v$, at distance at most $r_v$ from $p_v$. The other end $p_x$ of $e$ is at distance $r_u + r_x > r_u$ from $p_u$, so $q \ne p_x$; in the same way $q$ is not the end of $e'$ other than $p_v$. If $e \ne e'$, the two segments meet only at a common end, which would force $q = p_u = p_v$, impossible since $\phi$ is one-to-one. So $e = e'$ is the edge $uv$.

Interiors: two discs of a common face have disjoint interiors, since the distance of the centers is the sum of the radii; sectors of different faces have disjoint interiors because the faces do; and outer discs are pairwise adjacent. So the interiors of all discs are pairwise disjoint, and two discs touch exactly when their vertices are adjacent. This proves the theorem for $T$, and by Step 1 for every planar graph. $\blacksquare$
