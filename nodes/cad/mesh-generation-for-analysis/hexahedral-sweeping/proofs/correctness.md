---
title: An affine sweep with one to one, orientation preserving slab maps gives valid hexahedra
proves: [correctness, termination]
status: full
---

**Setting.** The source face is a polygon $S$ in the plane with a conforming mesh of strictly convex quadrilaterals. Each quad $(a, b, c, d)$ is counterclockwise. The boundary loop of $S$ is the cycle of mesh vertices $\ell_1, \ldots, \ell_n$, and these points are not all on one line. SWEEP gets the positions $B_k[\ell_i] \in \mathbb{R}^3$ of the loop vertices on the layers $k = 0, \ldots, K$, with $K \ge 1$. Line L2 fits the affine map $\varphi_k(p) = L_k p + t_k$, with $L_k$ a $3 \times 2$ matrix, that minimizes $\sum_i \lVert \varphi_k(p_{\ell_i}) - B_k[\ell_i] \rVert^2$. Lines L3 and L4 set $x_{k,v} = B_k[v]$ for a loop vertex and $x_{k,v} = \varphi_k(p_v)$ for the other vertices. Line L8 makes the hex with the corners $x_{k,a}, x_{k,b}, x_{k,c}, x_{k,d}$ and then $x_{k+1,a}, \ldots, x_{k+1,d}$. Its map from the unit cube is the trilinear map $H(u, v, w)$ with these corner images.

We call layer $k$ affine if $x_{k,v} = \varphi_k(p_v)$ for every vertex $v$. For an affine layer pair $k, k + 1$, the slab map is

$$F_k(p, w) = (1 - w)\,\varphi_k(p) + w\,\varphi_{k+1}(p), \qquad p \in S,\ w \in [0, 1].$$

**Claim.**

1. SWEEP stops, and every loop vertex of layer $k$ is at its given position $B_k[v]$.
2. The normal equations of L2 are regular. If the given loop of layer $k$ is $\psi(p_{\ell_i})$ for an affine map $\psi$, then $\varphi_k = \psi$, layer $k$ is affine, and every node of layer $k$ is $\psi(p_v)$. So the target face mesh is the image of the source mesh under $\psi$.
3. Let layers $k$ and $k + 1$ be affine. Every hex of slab $k$ is $H = F_k \circ (P \times \mathrm{id})$, where $P$ is the bilinear map of its source quad, and $\det DH(u, v, w) = \det DF_k(P(u, v), w)\,\det DP(u, v)$.
4. If every layer is affine and $\det DF_k > 0$ on $S \times [0, 1]$ for every $k$, then every hex has $\det J > 0$ at every point of the closed unit cube. If also each $F_k$ is one to one on $S \times [0, 1]$, and the slabs meet only in their common layers, then the hexes have pairwise disjoint interiors, two hexes that touch share a whole face, an edge or a vertex, and the union of the hexes is the swept solid.
5. CERTIFY returns true exactly when every layer is affine and $\det DF_k(p, w) > 0$ for every loop vertex $p$ and every $w \in [0, 1]$. In that case $\det DF_k > 0$ on $S \times [0, 1]$.
6. If the layers are planar, with $\varphi_k(p) = (A_k p + c_k, z_k)$ and $z_0 < z_1 < \cdots < z_K$, and CERTIFY returns true, then every $F_k$ is one to one, so part 4 gives a valid hex mesh.

**Proof of part 1.** The loops of L1, L3, L6 and L7 are finite, so SWEEP stops after $O(Kn)$ steps. L4 copies $B_k[v]$ for a loop vertex.

**Proof of part 2.** The least squares problem for one coordinate has the normal matrix $N = \sum_i q_i q_i^{\mathsf T}$ with $q_i = (x_i, y_i, 1)$. For a vector $z$, $z^{\mathsf T} N z = \sum_i (q_i \cdot z)^2$. This is zero only if all $q_i$ are orthogonal to $z$. The points are not on one line, so three of the $q_i$ are linearly independent, and $z = 0$. So $N$ is positive definite and the minimizer is unique. If the targets are $\psi(p_{\ell_i})$, the map $\psi$ gives the residual $0$, which is the minimum, so $\varphi_k = \psi$. L4 then gives $\psi(p_v)$ for the inner vertices, and the loop vertices are $\psi(p_v)$ by hypothesis.

**Proof of part 3.** Let the source quad have the corners $p_a, p_b, p_c, p_d$ and the bilinear map $P(u, v) = (1 - u)(1 - v) p_a + u (1 - v) p_b + u v\, p_c + (1 - u) v\, p_d$. On an affine layer, the hex corners are $\varphi_k(p_a), \ldots$ and $\varphi_{k+1}(p_a), \ldots$. An affine map commutes with an affine combination, and the bilinear weights add up to $1$. So

$$H(u, v, w) = (1 - w)\,\varphi_k(P(u, v)) + w\,\varphi_{k+1}(P(u, v)) = F_k(P(u, v), w).$$

The chain rule gives $DH = DF_k \cdot G$ with the $3 \times 3$ block matrix $G = \begin{pmatrix} DP & 0 \\ 0 & 1 \end{pmatrix}$, and $\det G = \det DP$.

**Lemma A (a convex quad has $\det DP > 0$).** Write $P(u, v) = p_a + u\,e + v\,f + u v\,g$ with $e = p_b - p_a$, $f = p_d - p_a$ and $g = p_a - p_b + p_c - p_d$. Then $DP$ has the columns $e + v g$ and $f + u g$, and with $s \times t = s_x t_y - s_y t_x$,

$$\det DP(u, v) = e \times f + u\,(e \times g) + v\,(g \times f).$$

The term in $uv$ is $g \times g = 0$, so $\det DP$ is affine in $(u, v)$. At the four corners of the unit square it is the cross product of the two edges at the corresponding quad corner. For a strictly convex counterclockwise quad these four values are positive. An affine function on the square takes its minimum at a corner, so $\det DP > 0$ on the closed square.

**Lemma B (the slab determinant).** Write $L_k = [\,l_{k,1}\ l_{k,2}\,]$ and $d(p) = \varphi_{k+1}(p) - \varphi_k(p)$. The columns of $DF_k$ are $(1 - w) l_{k,1} + w\, l_{k+1,1}$, $(1 - w) l_{k,2} + w\, l_{k+1,2}$ and $d(p)$. The determinant is linear in each column, so

$$\det DF_k(p, w) = b_0 (1 - w)^2 + 2 b_1 w (1 - w) + b_2 w^2,$$

$$b_0 = \det[l_{k,1}, l_{k,2}, d], \quad b_2 = \det[l_{k+1,1}, l_{k+1,2}, d], \quad 2 b_1 = \det[l_{k,1}, l_{k+1,2}, d] + \det[l_{k+1,1}, l_{k,2}, d].$$

Each $b_i$ is linear in $d(p)$, and $d$ is affine in $p$. So for a fixed $w$, the function $p \mapsto \det DF_k(p, w)$ is affine in $p$.

**Lemma C (a positive quadratic).** The function $q(w) = b_0 (1 - w)^2 + 2 b_1 w (1 - w) + b_2 w^2$ is positive on $[0, 1]$ exactly when $b_0 > 0$, $b_2 > 0$, and $b_1 \ge 0$ or $b_1^2 < b_0 b_2$. Proof: $q(0) = b_0$ and $q(1) = b_2$, so the first two conditions are necessary. If $b_1 \ge 0$, every term is at least $0$, and $(1 - w)^2$ and $w^2$ are never both $0$, so $q > 0$. Let $b_1 < 0$. For $0 < w < 1$, put $t = w / (1 - w)$, which takes every value in $(0, \infty)$. Then $q(w) / (1 - w)^2 = b_0 + 2 b_1 t + b_2 t^2$. Its minimum over $t > 0$ is at $t^* = -b_1 / b_2 > 0$ and has the value $b_0 - b_1^2 / b_2$. This is positive exactly when $b_1^2 < b_0 b_2$.

**Proof of part 4.** By Lemma A, $\det DP > 0$ on the closed square, and $P$ maps it into $S$. So by part 3, $\det DH > 0$ on the closed cube. Now let each $F_k$ be one to one. Two hexes of the same slab are the images under $F_k$ of the two sets $Q \times [0, 1]$ and $Q' \times [0, 1]$ for source quads $Q$ and $Q'$. The source mesh is conforming, so these sets have disjoint interiors and meet in a common edge times $[0, 1]$, in a vertex times $[0, 1]$, or not at all. A one to one map keeps these relations. Hexes of different slabs meet only in the common layer, where the top face of hex $(k, Q)$ is the bottom face of hex $(k + 1, Q)$, because both use the nodes $x_{k+1, v}$. The union of the sets $Q \times [0, 1]$ is $S \times [0, 1]$, so the union of the hexes is the swept solid.

**Proof of part 5.** CERTIFY first compares every node with $\varphi_k(p_v)$, which is the definition of an affine layer. Then for each slab and each loop vertex it applies the test of Lemma C to the coefficients of Lemma B. With int or Fraction input both tests are exact. So CERTIFY returns true exactly under the stated conditions. Now let them hold and take $p \in S$. The polygon $S$ is in the convex hull of its loop vertices, so $p = \sum_i \lambda_i p_{\ell_i}$ with $\lambda_i \ge 0$ and $\sum_i \lambda_i = 1$. By Lemma B, $\det DF_k(p, w) = \sum_i \lambda_i \det DF_k(p_{\ell_i}, w) > 0$.

**Proof of part 6.** For planar layers, $d(p) = ((A_{k+1} - A_k) p + c_{k+1} - c_k,\ z_{k+1} - z_k)$, and the first two columns of $DF_k$ have the third entry $0$. Expansion along the third row gives $\det DF_k = (z_{k+1} - z_k) \det A(w)$ with $A(w) = (1 - w) A_k + w A_{k+1}$. So $\det A(w) > 0$ for every $w$ in $[0, 1]$. Take two points $(p, w)$ and $(p', w')$ with the same image. The third coordinate $(1 - w) z_k + w z_{k+1}$ is strictly increasing in $w$, so $w = w'$. The first two coordinates are $A(w) p + c(w)$, and $A(w)$ is invertible, so $p = p'$. The slab $k$ has the heights $[z_k, z_{k+1}]$, so two slabs meet only in a common layer.

**Remark (positive corners are not enough).** Take the $2 \times 2$ grid on $[0, 2]^2$, the layer $0$ equal to the source at $z = 0$, and the layer $1$ equal to the source turned by $180$ degrees about $(1, 1)$ at $z = 1$. Every hex has the corner Jacobians $1, \ldots, 1$. Lemma B gives the coefficients $(1, -1, 1)$, so $\det DF_0 = (1 - 2w)^2$ and it is $0$ at $w = 1/2$. All four hexes pass through the point $(1, 1, 1/2)$, and CERTIFY returns false. So the hypothesis of part 4 is needed, and a corner test can not replace it. $\blacksquare$
