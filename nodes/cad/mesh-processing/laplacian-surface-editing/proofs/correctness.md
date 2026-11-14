---
title: The Laplacian editing solve is the unique least squares minimum, and with the handles at rest it returns the input mesh
proves: [correctness, termination]
status: full
---

**Setup.** The mesh is connected, with rest positions $p_1, \ldots, p_n$, and $N(i)$ is the set of the $d_i \ge 1$ neighbours of vertex $i$. The uniform Laplacian is $L(q)_i = q_i - \frac{1}{d_i}\sum_{j \in N(i)} q_j$, applied to each coordinate, and the Laplacian coordinates are $\delta_i = L(p)_i$. The handles are a set $H$ of vertices with targets $h_k$, and $\lambda > 0$ is the weight of the handles. The energy is

$$E(q) = \sum_{i=1}^{n}\bigl|L(q)_i - T_i(q)\,\delta_i\bigr|^2 + \lambda^2\sum_{k \in H}|q_k - h_k|^2.$$

Without rotations, $T_i(q) = I$. With rotations, $T_i(q) = s_i I + [h_i]_\times$, where $[h]_\times x = h \times x$, and $(s_i, h_i, t_i)$ is the least squares solution of $s\,p_j + h \times p_j + t \approx q_j$ for $j$ in the ring $\{i\} \cup N(i)$. The algorithm writes $E$ as $|Mx - r|^2$ for a matrix $M$, forms the normal equations $M^{\mathsf T}M x = M^{\mathsf T} r$, and solves them. It needs no loop.

**Lemma 1 (the kernel of the Laplacian).** For a scalar function $u$ on the vertices, $L(u) = 0$ if and only if $u$ is constant.

*Proof.* A constant $u$ gives $u_i - \frac{1}{d_i} d_i u_i = 0$. Conversely, let $L(u) = 0$, so each $u_i$ is the mean of its neighbours. Let $m$ be the largest value of $u$ and $u_i = m$. A mean of values at most $m$ equals $m$ only if all of them equal $m$, so all neighbours of $i$ have the value $m$. The mesh is connected, so by induction along paths every vertex has the value $m$. $\square$

**Lemma 2 (the solve gives the unique minimum).** $E$ is a quadratic function, and its minima are the solutions of the normal equations $M^{\mathsf T}M x = M^{\mathsf T}r$. If $M^{\mathsf T}M$ is positive definite, the minimum is unique and the solve returns it.

*Proof.* $E(x) = |Mx - r|^2$ has the gradient $2(M^{\mathsf T}Mx - M^{\mathsf T}r)$, and $M^{\mathsf T}M$ is positive semidefinite, so $E$ is convex and its minima are exactly its critical points. If $M^{\mathsf T}M$ is positive definite, the system has one solution, and its Cholesky factorization exists. On rational input, Gaussian elimination solves it exactly. $\square$

**Lemma 3 (the matrix without rotations).** Without rotations and with $H \ne \emptyset$, the coordinates separate, and the matrix of each one is $N = L^{\mathsf T}L + \lambda^2\sum_{k \in H} e_k e_k^{\mathsf T}$. It is positive definite.

*Proof.* For a scalar $u$, $u^{\mathsf T}Nu = |L(u)|^2 + \lambda^2\sum_{k \in H} u_k^2 \ge 0$. If it is 0, then $L(u) = 0$, so $u$ is constant by Lemma 1, and $u_k = 0$ at a handle, so $u = 0$. $\square$

**Lemma 4 (the fit of a ring).** Suppose the ring of vertex $i$ is not contained in a line. Then the fit has exactly one solution $(s, h, t)$, and it is a linear function of the new positions of the ring. If the new ring is $c\,p_j + a$ for a scalar $c$ and a vector $a$, the fit is $(c, 0, a)$.

*Proof.* The map $(s, h, t) \mapsto (s\,p_j + h \times p_j + t)_j$ is linear. Suppose it gives 0. Subtracting the equation at $i$ gives $(sI + [h]_\times)(p_j - p_i) = 0$ for each $j$. The matrix $sI + [h]_\times$ sends a vector $v$ to $sv + h \times v$, and $v \cdot (sv + h \times v) = s|v|^2$. So if $s \ne 0$, it sends no nonzero vector to 0, and all $p_j = p_i$, which is false. So $s = 0$, and $h \times (p_j - p_i) = 0$ means $h$ is parallel to every $p_j - p_i$. The ring is not in a line, so two of these vectors are independent, and $h = 0$. Then $t = 0$. So the map is injective, its normal matrix $G$ is invertible, and the fit $G^{-1}A^{\mathsf T}b$ is linear in the right side $b$. For the new ring $c\,p_j + a$, the choice $(c, 0, a)$ fits with residual 0, so it is the unique least squares solution. $\square$

In a triangle mesh, the ring of a vertex holds the corners of a triangle, so it is not in a line when the triangles are not degenerate.

**Theorem 1 (the unconstrained solve returns the input).** Let every handle stay at its rest position, $h_k = p_k$, with $H \ne \emptyset$. Then $E(p) = 0$, so $p$ is a minimum of $E$. Without rotations the solve returns $p$. With rotations it returns $p$ whenever $M^{\mathsf T}M$ is positive definite. On rational input the result is $p$ exactly.

*Proof.* Without rotations, $L(p)_i - \delta_i = 0$ by the definition of $\delta$. With rotations, Lemma 4 with $c = 1$ and $a = 0$ gives $T_i(p) = I$, so again $L(p)_i - T_i(p)\delta_i = 0$. The handle terms are $|p_k - p_k|^2 = 0$. So $E(p) = 0$, the least possible value. By Lemma 3 without rotations, and by the assumption with rotations, the minimum is unique, and by Lemma 2 the solve returns it. $\square$

**Theorem 2 (no handles).** Without rotations and without handles, the minima of $E$ are exactly the positions $p + a$ for a constant vector $a$. So the system is singular, and one handle is enough to fix the result.

*Proof.* $E(q) = |L(q) - \delta|^2 = |L(q - p)|^2$, which is 0 exactly when $L(q - p) = 0$, that is, by Lemma 1, when $q - p$ is constant. $\square$

**Theorem 3 (a translation of the handles).** Let $h_k = p_k + a$ for all $k \in H$, with $H \ne \emptyset$. Then the solve returns $p + a$, without rotations always, and with rotations whenever $M^{\mathsf T}M$ is positive definite.

*Proof.* $L$ sends the constant $a$ to 0, so $L(p + a) = \delta$. With rotations, Lemma 4 with $c = 1$ gives $T_i(p + a) = I$. The handle terms are 0. So $E(p + a) = 0$, and uniqueness gives the result as in Theorem 1. $\square$

**The kernel with rotations.** With rotations and without handles, $E$ is 0 at every $q_j = c\,p_j + h \times p_j + a$, because $L$ is linear and kills constants, so $L(q)_i = c\,\delta_i + h \times \delta_i$, and $T_i$ is linear in $q$, so by Lemma 4 applied term by term $T_i(q) = cI + [h]_\times$. These are 7 dimensions. Three handles $k$ whose rest positions are not on a line remove them: if $c\,p_k + h \times p_k + a = 0$ at the three handles, then $cI + [h]_\times$ sends two independent differences of their rest positions to 0, and the argument of Lemma 4 gives $c = 0$, $h = 0$ and then $a = 0$. That no other direction of the kernel remains is not proved here. The code lets the Cholesky factorization, or the exact elimination, report a singular matrix, and the tests check that the matrix is positive definite on their meshes.

**Termination.** The algorithm builds a fixed number of rows and does one direct solve, so it stops.

How well the rotations keep the detail under large turns of the handles is measured on the page, not proved. The linearized $T_i$ is a rotation only to first order in the angle.
