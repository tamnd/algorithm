---
title: The eight-point algorithm minimizes the algebraic error, forces rank 2 optimally, and recovers F exactly from exact data in general position
proves: [correctness]
status: full
---

We use the notation of the page. The input is $n \ge 8$ pairs of 2D points, written as $\mathbf{x}_i = (u_i, v_i, 1)^{\mathsf T}$ in image 1 and $\mathbf{x}'_i = (u'_i, v'_i, 1)^{\mathsf T}$ in image 2. For a $3 \times 3$ matrix $G$ we write $\mathbf{g} \in \mathbb{R}^9$ for its rows put one after the other, so $\|\mathbf{g}\| = \|G\|_F$. The canonical form of a nonzero matrix $G$ is $G / \|G\|_F$ times the sign of its entry of largest absolute value (on a tie, the first such entry in row order). The singular values of a matrix are $\sigma_1 \ge \sigma_2 \ge \cdots$.

**Claim.** (a) The vector $\mathbf{f}$ of line L3 minimizes $\|A\mathbf{f}\|$ over all unit vectors. (b) The matrix of line L6 is a matrix of rank at most 2 that is closest to $F_0$ in the Frobenius norm. In the essential variant, it is a matrix with singular values $(m, m, 0)$, $m \ge 0$, that is closest to $F_0$. (c) Let $F$ be a real $3 \times 3$ matrix of rank 2 with $\mathbf{x}'^{\mathsf T}_i F\mathbf{x}_i = 0$ for all $i$, and let $A$ have rank 8. Then EIGHT-POINT returns the canonical form of $F$. (d) If there is an invertible $H$ with $\mathbf{x}'_i \sim H\mathbf{x}_i$ for all $i$ (a planar scene, or a camera that only rotates), then $A$ has rank at most 6, so the hypothesis of (c) fails.

**Lemma 1 (the row).** For every $3 \times 3$ matrix $G$, the row $\mathbf{a}_i^{\mathsf T} = (\mathbf{x}'_i \otimes \mathbf{x}_i)^{\mathsf T}$ of line L2 satisfies $\mathbf{a}_i^{\mathsf T}\mathbf{g} = \mathbf{x}'^{\mathsf T}_i G\mathbf{x}_i$.

*Proof.* Entry $3(j - 1) + k$ of $\mathbf{x}'_i \otimes \mathbf{x}_i$ is $x'_{i,j} x_{i,k}$, and entry $3(j - 1) + k$ of $\mathbf{g}$ is $G_{jk}$. So $\mathbf{a}_i^{\mathsf T}\mathbf{g} = \sum_{j,k} x'_{i,j} G_{jk} x_{i,k} = \mathbf{x}'^{\mathsf T}_i G\mathbf{x}_i$. $\square$

So $A\mathbf{g} = \mathbf{0}$ holds exactly when $G$ satisfies the epipolar constraint on all $n$ pairs.

**Lemma 2 (minimum of the algebraic error).** Let $A$ be an $m \times 9$ real matrix and let $\sigma_{\min} \ge 0$ be its smallest singular value, counted as 0 when $m < 9$. Then $\min_{\|\mathbf{f}\| = 1} \|A\mathbf{f}\| = \sigma_{\min}$, and a right singular vector for $\sigma_{\min}$ attains it.

*Proof.* Let $A^{\mathsf T}A = V \operatorname{diag}(\sigma_1^2, \ldots, \sigma_9^2) V^{\mathsf T}$ with $V$ orthogonal. For a unit vector $\mathbf{f}$ put $\mathbf{c} = V^{\mathsf T}\mathbf{f}$, also a unit vector. Then $\|A\mathbf{f}\|^2 = \sum_j \sigma_j^2 c_j^2 \ge \sigma_9^2$. The last column of $V$ gives $\mathbf{c} = \mathbf{e}_9$ and equality. $\square$

Part (a) is Lemma 2 applied to line L3.

**Lemma 3 (closest matrices with given singular value pattern).** Let $F_0 = U \operatorname{diag}(s_1, s_2, s_3) V^{\mathsf T}$ be an SVD. (i) $U \operatorname{diag}(s_1, s_2, 0) V^{\mathsf T}$ is a matrix of rank at most 2 closest to $F_0$ in the Frobenius norm, at distance $s_3$. (ii) Among the matrices with singular values $(m, m, 0)$ for some $m \ge 0$, $U \operatorname{diag}(\bar m, \bar m, 0) V^{\mathsf T}$ with $\bar m = (s_1 + s_2)/2$ is closest to $F_0$.

*Proof.* We use von Neumann's trace inequality: for real $3 \times 3$ matrices $P$ and $Q$ with singular values $p_j$ and $q_j$, $\operatorname{tr}(P^{\mathsf T}Q) \le \sum_j p_j q_j$. Let $G$ have singular values $g_1 \ge g_2 \ge g_3$. Then
$$\|F_0 - G\|_F^2 = \|F_0\|_F^2 + \|G\|_F^2 - 2\operatorname{tr}(F_0^{\mathsf T}G) \ge \sum_j (s_j - g_j)^2 .$$
For (i), $g_3 = 0$, so the bound is at least $s_3^2$, and $G = U \operatorname{diag}(s_1, s_2, 0) V^{\mathsf T}$ gives $\|F_0 - G\|_F = s_3$. For (ii), $g = (m, m, 0)$, and the bound $(s_1 - m)^2 + (s_2 - m)^2 + s_3^2$ is smallest at $m = \bar m$. The matrix $U \operatorname{diag}(\bar m, \bar m, 0) V^{\mathsf T}$ attains the bound, because $F_0 - G = U \operatorname{diag}(s_1 - \bar m, s_2 - \bar m, s_3) V^{\mathsf T}$. $\square$

Lines L5 and L6 compute exactly these matrices, so part (b) is Lemma 3.

**Proof of part (c).** By Lemma 1, $A\mathbf{f}_{\mathrm{true}} = \mathbf{0}$ for the vector $\mathbf{f}_{\mathrm{true}}$ of $F$. The rank of $A$ is 8, so its null space is the line spanned by $\mathbf{f}_{\mathrm{true}}$, $\sigma_9 = 0$ and $\sigma_8 > 0$. By Lemma 2, line L3 returns a unit vector in this null space, so $F_0 = \lambda F$ with $\lambda \ne 0$. Then $F_0$ has rank 2 and $s_3 = 0$, so line L6 gives $F_0$ back unchanged. Line L7 divides by $\|F_0\|_F = |\lambda|\,\|F\|_F$ and fixes the sign by a rule that depends only on the matrix up to a positive factor. So the output is the canonical form of $F$. In the essential variant, if $F$ has singular values $(s, s, 0)$, then $s_1 = s_2$ for $F_0$ and line L6 again changes nothing. $\blacksquare$

**Proof of part (d).** Let $\mathbf{x}'_i = \kappa_i H\mathbf{x}_i$ with $\kappa_i \ne 0$. For every $\mathbf{a} \in \mathbb{R}^3$ put $G_{\mathbf{a}} = [\mathbf{a}]_\times H$. Then $\mathbf{x}'^{\mathsf T}_i G_{\mathbf{a}}\mathbf{x}_i = \kappa_i^{-1}\,\mathbf{x}'^{\mathsf T}_i(\mathbf{a} \times \mathbf{x}'_i) = 0$, because $\mathbf{a} \times \mathbf{x}'_i$ is orthogonal to $\mathbf{x}'_i$. The map $\mathbf{a} \mapsto [\mathbf{a}]_\times H$ is linear and one to one, because $H$ is invertible and $[\mathbf{a}]_\times = 0$ only for $\mathbf{a} = \mathbf{0}$. By Lemma 1 its image, a space of dimension 3, lies in the null space of $A$. So $A$ has rank at most $9 - 3 = 6$. If the camera only rotates, $\mathbf{x}'_i \sim K' R K^{-1}\mathbf{x}_i$, which is the same case with $H = K' R K^{-1}$. $\blacksquare$

**Remark (what the proof does not give).** On noisy data the output minimizes the algebraic error $\sum_i (\mathbf{x}'^{\mathsf T}_i F_0\mathbf{x}_i)^2$ under $\|F_0\|_F = 1$, and then moves to the nearest matrix of rank 2. That two-step result is in general not the matrix of rank 2 with the least algebraic error, and it is not a geometric optimum. The condition of $A$ on pixel coordinates, which decides how many digits survive in floating point, is the subject of the normalized eight-point algorithm.
