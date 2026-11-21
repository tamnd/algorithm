---
title: Correctness and convergence of SART
proves: [correctness, convergence]
status: full
---

We use the notation of the page and work in exact arithmetic. $A$ is an $m \times N$ matrix with $a_{ij} \ge 0$, its rows are split into views $V_1, \dots, V_a$, and $r_i = \sum_j a_{ij} > 0$ for every ray (rays with $r_i = 0$ are skipped by the code and can be removed). We do not cover the clipping of line L8.

**What the lines compute.** For the current view $v$, line L5 forms $e = R_v (y_v - A_v x)$, line L6 forms $g = A_v^T e$ and the column sums $c_{vj} = \sum_{i \in V_v} a_{ij}$, and line L7 adds $\lambda g_j / c_{vj}$ to each pixel with $c_{vj} > 0$. Line L5 computes all residuals of the view from the same $x$, because $x$ changes only in line L7, after the loop over the rays. So one view step is
$$x \leftarrow x + \lambda\, C_v A_v^T R_v\, (y_v - A_v x), \tag{1}$$
with $C_v = \operatorname{diag}(1/c_{vj})$ and $1/0 := 0$. A pixel with $c_{vj} = 0$ has $g_j = 0$, so it does not change.

**Proposition 1 (one view of all rays).** If $a = 1$ and $V_1$ holds all rays, one sweep is one SIRT iteration $x \leftarrow x + \lambda C A^T R (y - A x)$.

*Proof.* With one view, $A_1 = A$, $R_1 = R$ and $c_{1j} = c_j$, so (1) is the SIRT step. $\square$

**The assumption.** From now on, all views have the same column sums: $c_{vj} = c_j > 0$ for all $v$ and $j$, and $C = \operatorname{diag}(1/c_j)$. For the pixel-driven matrix of the shared helper, each pixel adds the weights $(1 - f)\,h^2/w$ and $f\,h^2/w$ to two bins of each view, so $c_{vj} = h^2/w$ for all $v$ and $j$ (the code checks this). For strip-integral weights $a_{ij} = |\text{pixel } j \cap \text{strip } i| / w$ with strips of width $w$ that cover the image, $c_{vj} = h^2/w$ as well.

Put $B_v = R_v^{1/2} A_v C^{1/2}$, $b_v = R_v^{1/2} y_v$, $B$ the matrix of all blocks $B_v$ stacked, and $x = C^{1/2} z$. Multiplying (1) by $C^{-1/2}$ gives
$$z \leftarrow z + \lambda B_v^T (b_v - B_v z). \tag{2}$$
Also $\|x\|_{C^{-1}}^2 = \sum_j c_j x_j^2 = \|z\|^2$. Let $M_v = B_v^T B_v$ and $T_v = I - \lambda M_v$.

**Lemma 1.** $\|B_v\| \le 1$ for every view, so $M_v$ is symmetric with eigenvalues in $[0, 1]$.

*Proof.* For a ray $i \in V_v$, the Cauchy-Schwarz inequality with the weights $a_{ij} \ge 0$ gives $\big(\sum_j a_{ij} c_j^{-1/2} z_j\big)^2 \le r_i \sum_j a_{ij} c_j^{-1} z_j^2$. So $(B_v z)_i^2 \le \sum_j a_{ij} c_j^{-1} z_j^2$. Summing over $i \in V_v$ and using $\sum_{i \in V_v} a_{ij} = c_{vj} = c_j$ gives $\|B_v z\|^2 \le \|z\|^2$. $\square$

**Lemma 2 (the decrease).** For $0 < \lambda < 2$ and every $w$, $\|w\|^2 - \|T_v w\|^2 \ge \lambda(2 - \lambda)\,\|B_v w\|^2$.

*Proof.* $\|T_v w\|^2 = \|w\|^2 - 2\lambda\, w^T M_v w + \lambda^2 w^T M_v^2 w$. By Lemma 1, $M_v^2 \preceq M_v$, so $w^T M_v^2 w \le w^T M_v w$. Hence $\|w\|^2 - \|T_v w\|^2 \ge (2\lambda - \lambda^2)\, w^T M_v w = \lambda(2 - \lambda)\|B_v w\|^2$. $\square$

Let $P_0$ be the orthogonal projector onto $\operatorname{null}(B) = \bigcap_v \operatorname{null}(B_v)$, and $W = \operatorname{range}(B^T)$, its orthogonal complement. Each $T_v$ is the identity on $\operatorname{null}(B)$, and since $T_v$ is symmetric it also maps $W$ into $W$. Let $S = T_{v_a} \cdots T_{v_1}$ for the chosen order $v_1, \dots, v_a$.

**Lemma 3.** For $0 < \lambda < 2$, the restriction of $S$ to $W$ has norm $q < 1$.

*Proof.* By Lemma 2 each $T_v$ has norm at most 1, so $\|S w\| \le \|w\|$. Suppose $w \in W$ and $\|S w\| = \|w\|$. Put $u_0 = w$ and $u_p = T_{v_p} u_{p-1}$, so $u_a = S w$. The norms $\|u_p\|$ do not increase and the last equals the first, so $\|u_p\| = \|u_{p-1}\|$ for every $p$. By Lemma 2, $B_{v_p} u_{p-1} = 0$, and then $u_p = u_{p-1} - \lambda B_{v_p}^T B_{v_p} u_{p-1} = u_{p-1}$. By induction, $u_p = w$ for every $p$, so $B_v w = 0$ for all $v$ and $w \in \operatorname{null}(B) \cap W = \{0\}$. So $\|S w\| < \|w\|$ for every $w \ne 0$ in $W$. The function $w \mapsto \|S w\|$ is continuous on the unit sphere of the finite-dimensional space $W$, which is compact, so its maximum $q$ is attained and $q < 1$. $\square$

**Theorem 1 (consistent data).** Let $A x = y$ have a solution and $0 < \lambda < 2$. Then for every order and every start $x_0$, the SART iterates converge to the solution $\hat x$ closest to $x_0$ in the $C^{-1}$ norm, and $\|x_k - \hat x\|_{C^{-1}} \le q^k \|x_0 - \hat x\|_{C^{-1}}$ after $k$ sweeps.

*Proof.* The solutions of $A x = y$ are the solutions of $B z = b$ in the variable $z$. Let $\hat z$ be the orthogonal projection of $z_0$ onto this affine set. Then $z_0 - \hat z \in W$, because the set is $\hat z + \operatorname{null}(B)$ and the projection makes the difference orthogonal to $\operatorname{null}(B)$. Since $B_v \hat z = b_v$, the step (2) gives $z - \hat z \leftarrow T_v (z - \hat z)$. So after $k$ sweeps $z_k - \hat z = S^k (z_0 - \hat z)$, and Lemma 3 gives $\|z_k - \hat z\| \le q^k \|z_0 - \hat z\|$. The point $\hat x = C^{1/2} \hat z$ solves $A x = y$ and is closest to $x_0$ in the norm $\|z\|$, which is the $C^{-1}$ norm of $x$. $\square$

**Theorem 2 (any data).** Let $0 < \lambda < 2$. For any data, the iterates at the ends of the sweeps converge, and so do the iterates after the $p$-th view of each sweep, for each $p$. So the iterates approach a cycle of at most $a$ points.

*Proof.* Step (2) is $z \leftarrow T_v z + \lambda B_v^T b_v$, so one sweep is $z \leftarrow S z + t$ with $t$ a sum of terms $T_{v_a} \cdots T_{v_{p+1}} \lambda B_{v_p}^T b_{v_p}$. Each such term lies in $W$, because $B_v^T b_v \in W$ and the maps $T_v$ keep $W$. Write $z = P_0 z + u$ with $u \in W$. Since each $T_v$ is the identity on $\operatorname{null}(B)$ and keeps $W$, the sweep gives $P_0 z_{k+1} = P_0 z_k$ and $u_{k+1} = S u_k + t$. By Lemma 3, the map $u \mapsto S u + t$ is a contraction on $W$ with the factor $q$, so $u_k$ converges to its unique fixed point $u^* = (I - S|_W)^{-1} t$, and $z_k \to P_0 z_0 + u^*$. The iterate after the $p$-th view of sweep $k + 1$ is an affine, hence continuous, function of $z_k$, so it converges too. Map back with $x = C^{1/2} z$. $\square$

The limit of Theorem 2 is a fixed point of the sweep map, which depends on $\lambda$ and on the order. It is not the $R$-weighted least squares solution in general: the test with nine rays and four pixels finds a distance of $0.17$ for $\lambda = 1$ and $0.054$ for $\lambda = 1/4$. These two numbers are measurements, not part of the theorem.

**Cost.** Line L1 reads each nonzero entry of $A$ once. For view $v$, line L5 reads the entries of $A_v$ once and line L6 reads them once more, and line L7 touches at most the pixels that the view meets. So a view step costs $O(\operatorname{nnz}(A_v))$ time and a sweep costs $O(\operatorname{nnz}(A))$, which is $O(a d n)$ for a ray-driven matrix with $O(n)$ entries per ray. The code keeps the row sums, $O(m) = O(a d)$, the image, $O(n^2)$, and two dictionaries for the current view, $O(n^2)$. $\square$
