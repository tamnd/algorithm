---
title: One plastering layer on a grid box is a valid conforming hex mesh of the shell exactly when 0 < h < g
proves: [correctness, termination]
status: full
---

**Setting.** The box is $\mathcal{B} = \prod_{t=0}^{2} [l_t, u_t]$. Each axis $t$ has strictly increasing breakpoints $l_t = x_{t,0} < x_{t,1} < \cdots < x_{t,n_t} = u_t$ with $n_t \ge 1$. The front is the boundary quad mesh of this grid, and each quad is listed counterclockwise seen from outside, so for its first three corners $p_0, p_1, p_3$ the vector $(p_1 - p_0) \times (p_3 - p_0)$ points out of the box. For a front vertex $p$, $n_p$ is the sum of the outward unit normals of the box faces that contain $p$. PLASTER-LAYER sets $p' = p - h\,n_p$ (L1 to L3) and makes, for each quad $(a, b, c, d)$, the hex $(a', b', c', d', a, b, c, d)$ (L5 and L6). Let

$$g = \min_t \min\Big(x_{t,1} - x_{t,0},\ x_{t,n_t} - x_{t,n_t - 1},\ \tfrac12 (u_t - l_t)\Big).$$

**Claim.**

1. PLASTER-LAYER stops after $O(V + Q)$ steps for $V$ front vertices and $Q$ front quads, and makes $Q = 2(n_0 n_1 + n_1 n_2 + n_2 n_0)$ hexes.
2. Let $\mu_t(x) = x + h$ for $x = l_t$, $\mu_t(x) = x - h$ for $x = u_t$, and $\mu_t(x) = x$ otherwise. Then $p'_t = \mu_t(p_t)$ for every front vertex and every axis.
3. Take a hex on a face with normal axis $a$, and let $b$ and $c$ be the other two axes. Let $\Delta_b$ and $\Delta_c$ be the side lengths of its front quad, and $\Delta'_b$, $\Delta'_c$ the side lengths of the offset quad. Then at every point of the unit cube

$$\det J(u, v, w) = h\,\beta_b(w)\,\beta_c(w), \qquad \beta_t(w) = (1 - w)\,\Delta'_t + w\,\Delta_t.$$

4. If $0 < h < g$, every hex has $\det J > 0$ on the whole closed cube. The hexes form a conforming mesh of the shell $\mathcal{B} \setminus \operatorname{int} \mathcal{B}'$ with $\mathcal{B}' = \prod_t [l_t + h, u_t - h]$, and the new front is the boundary grid of $\mathcal{B}'$ with the breakpoints $\mu_t(x_{t,i})$.
5. If $h \le 0$ or $h \ge g$, the layer is not a valid mesh of a shell: some offset width $\Delta'_t$ is at most $0$. The corner test of L7 is true exactly when $h > 0$ and $\Delta'_b \Delta'_c > 0$ for every pair of offset widths on two different axes. This can hold when every offset width is negative, so the corner test alone does not prove validity.

**Proof of part 1.** L1 to L3 visit each vertex once and L5 and L6 visit each quad once. The two faces normal to axis $a$ each carry $n_b n_c$ quads, which gives the count.

**Proof of part 2.** The outward normal of the face $x_t = l_t$ is $-e_t$, and of the face $x_t = u_t$ it is $+e_t$. A vertex is on the face $x_t = l_t$ exactly when $p_t = l_t$, and it is not on both faces of an axis because $l_t < u_t$. So the $t$ component of $-h\,n_p$ is $+h$, $-h$ or $0$ in the three cases of $\mu_t$.

**Proof of part 3.** Let the front quad be on the face $x_a = l_a$. The case $x_a = u_a$ is the same with the signs changed. The quad is the rectangle $[x_{b,i}, x_{b,i+1}] \times [x_{c,j}, x_{c,j+1}]$ in the plane $x_a = l_a$. By part 2 the offset quad is the rectangle $[\mu_b(x_{b,i}), \mu_b(x_{b,i+1})] \times [\mu_c(x_{c,j}), \mu_c(x_{c,j+1})]$ in the plane $x_a = l_a + h$. Both are listed in the same corner order. Up to the choice of which of $u$ and $v$ runs along $b$, the trilinear map is

$$x_a = l_a + (1 - w) h, \qquad x_b = (1 - w)(\mu_b(x_{b,i}) + s\,\Delta'_b) + w\,(x_{b,i} + s\,\Delta_b),$$

and the same for $x_c$ with the other parameter $r$, where $s$ and $r$ are $u$ and $v$ or $1 - u$ and $1 - v$. So $x_a$ depends only on $w$, $x_b$ only on $(s, w)$ and $x_c$ only on $(r, w)$. The Jacobian matrix has, up to a permutation of rows and columns, a triangular form with the diagonal $-h$, $\pm\beta_b(w)$, $\pm\beta_c(w)$. So $\det J = \sigma\, h\, \beta_b(w)\, \beta_c(w)$ with a sign $\sigma = \pm 1$ that is the same at every point. To find $\sigma$, take $w = 1$, where $\beta_t = \Delta_t > 0$. There the first two columns are the edge vectors of the front quad, and the third column $\partial_w H$ is the front point minus the offset point. Its $a$ component is $-h$, which is $h$ times the outward normal $-e_a$, and its other components are in the plane of the quad. So $\det J = h\,(\partial_u H \times \partial_v H) \cdot (-e_a)$, which is positive because the quad is counterclockwise seen from outside. So $\sigma = 1$.

**Proof of part 4.** Let $0 < h < g$. On each axis the offset widths are $x_{t,1} - x_{t,0} - h$ and $x_{t,n_t} - x_{t,n_t-1} - h$ at the ends and the unchanged widths inside, or $u_t - l_t - 2h$ if $n_t = 1$. All are positive by the choice of $g$. So $\mu_t$ is strictly increasing on the breakpoints, and $\beta_t(w) > 0$ for all $w \in [0, 1]$. Part 3 gives $\det J > 0$ on the closed cube.

The new points are $\mu(p)$, with $\mu_t(l_t) = l_t + h$ and $\mu_t(u_t) = u_t - h$, and $\mu_t$ keeps the inner breakpoints, which lie in $(l_t + h, u_t - h)$. So the new front is the boundary grid of $\mathcal{B}'$ with the breakpoints $\mu_t(x_{t,i})$.

Conformity. The offset of a vertex depends only on the vertex. Two front quads that share the edge $pq$ give two hexes that share the face $(p, q, q', p')$. The front quads and the offset quads each belong to one hex.

Covering. For a face $F$ of $\mathcal{B}$ with the parallel face $F'$ of $\mathcal{B}'$, let $P_F$ be the convex hull of $F \cup F'$, a frustum. For a point $x$ of the shell, let $d(x)$ be the least of the six distances $x_t - l_t$ and $u_t - x_t$. A point of the shell is not in $\operatorname{int} \mathcal{B}'$, so $d(x) \le h$. Because $\mathcal{B}'$ is $\mathcal{B}$ moved in by the same $h$ on every side, $x$ is in $P_F$ exactly when the distance to $F$ is the least of the six, and $x$ is in the interior of $P_F$ only when that distance is strictly the least. So the six frusta cover the shell and have disjoint interiors. Inside $P_F$ with $F$ on $x_a = l_a$, the hexes of $F$ are the images of the front quads of $F$ under $\Phi(y, w) = (1 - w)\mu(y) + w\,y$. The $a$ coordinate fixes $w$, and for a fixed $w$ the in-plane coordinates are $(1 - w)\mu_t(y_t) + w\,y_t$, which are continuous, piecewise affine and strictly increasing in $y_t$. So $\Phi$ is one to one from $F \times [0, 1]$ onto $P_F$, and the hexes of $F$ tile $P_F$ with disjoint interiors.

**Proof of part 5.** If $h \le 0$, the offset quads are not inside the box, and part 3 gives $\det J = 0$ for $h = 0$ and a negative value at $w = 1$ for $h < 0$. If $h \ge g$, one of the three cases in the definition of $g$ gives an offset width at most $0$, so $\mathcal{B}'$ does not have positive side lengths and the new front is not the boundary of a box inside $\mathcal{B}$. The corner Jacobians are the values of part 3 at $w \in \{0, 1\}$. At $w = 1$ they are $h \Delta_b \Delta_c$. At $w = 0$ they are $h \Delta'_b \Delta'_c$ for every pair of offset widths of the face, and every pair of offset widths of two different axes occurs on some face, because the faces normal to the third axis carry all pairs. This gives the condition for L7. If all offset widths are negative, which needs $n_t \le 2$ on every axis, every product is positive and L7 returns true, but $\mathcal{B}'$ is reflected and the hexes overlap. $\blacksquare$
