---
title: One step of Chorin's projection method on the periodic MAC grid is a discrete orthogonal projection, and the method is forward Euler for the projected equations
proves: [correctness, termination]
status: full
---

**Setting.** The grid is the periodic MAC grid of the main page with $n_x \times n_y = M$ cells of size $\Delta x \times \Delta y$. A velocity field $\mathbf{u} = (u, v)$ has one value $u_k$ on the left face and one value $v_k$ on the bottom face of each cell $k$, and a pressure $p$ has one value per cell center. With $e(k), w(k), n(k), s(k)$ the east, west, north and south neighbors of cell $k$ (with wrap around),

$$(D\mathbf{u})_k = \frac{u_{e(k)} - u_k}{\Delta x} + \frac{v_{n(k)} - v_k}{\Delta y}, \qquad (Gp)^x_k = \frac{p_k - p_{w(k)}}{\Delta x}, \qquad (Gp)^y_k = \frac{p_k - p_{s(k)}}{\Delta y}.$$

The inner products are $\langle \mathbf{u}, \mathbf{w}\rangle = \sum_k (u_k w^x_k + v_k w^y_k)$ on face fields and $(p, q) = \sum_k p_k q_k$ on cell fields; a common factor $\Delta x \Delta y$ does not change any statement below. $F_h(\mathbf{u})$ is the discrete right side of line L2, $-(\mathbf{u}\cdot\nabla)\mathbf{u} + \nu\Delta_h\mathbf{u} + \mathbf{f}$, any function from face fields to face fields. $V_h = \{\mathbf{u} : D\mathbf{u} = 0\}$ is the space of discretely divergence-free fields.

**Lemma 1 (summation by parts).** $\langle \mathbf{u}, Gp\rangle = -(D\mathbf{u}, p)$ for every face field $\mathbf{u}$ and cell field $p$. So $G^{T} = -D$, and $A := -DG$ is symmetric positive semidefinite.

*Proof.* $\sum_k u_k (p_k - p_{w(k)}) = \sum_k u_k p_k - \sum_k u_k p_{w(k)}$. The map $k \mapsto w(k)$ is a bijection with inverse $e$, so the second sum is $\sum_j u_{e(j)} p_j$. Hence $\sum_k u_k (p_k - p_{w(k)})/\Delta x = -\sum_k p_k (u_{e(k)} - u_k)/\Delta x$. The $y$ terms are the same with $n$ and $s$. Adding gives the identity. With $\mathbf{u} = Gq$ it gives $(Ap, q) = -(DGp, q) = \langle Gp, Gq\rangle$, which is symmetric in $p$ and $q$ and nonnegative for $q = p$. Writing out $A$ shows that it is the matrix of minus the 5-point Laplacian with periodic wrap around. $\square$

**Lemma 2 (null space and range).** $Gp = 0$ if and only if $p$ is constant. So the null space of $A$ is the constants, and $Ap = b$ has a solution if and only if $\sum_k b_k = 0$; the solution is unique up to an additive constant, and $Gp$ is unique.

*Proof.* If $Gp = 0$ then $p_k = p_{w(k)}$ and $p_k = p_{s(k)}$ for all $k$; walking west and south reaches every cell, so $p$ is constant. $(Ap, p) = \|Gp\|^2$, so $Ap = 0$ implies $Gp = 0$; the converse is clear. $A$ is symmetric, so its range is the orthogonal complement of its null space, the vectors with zero sum. Two solutions differ by a null vector, a constant, which $G$ maps to $0$. $\square$

**Lemma 3 (the right side is in the range).** $\sum_k (D\mathbf{u})_k = 0$ for every face field.

*Proof.* Take $p \equiv 1$ in Lemma 1: $\sum_k (D\mathbf{u})_k = -\langle \mathbf{u}, G1\rangle = 0$. $\square$

So in exact arithmetic $b = -D\mathbf{u}^*/\Delta t$ (line L3) has zero sum, line L4 has a solution, and $Gp$ in line L5 is well defined. The implementation subtracts the mean of $b$ before calling CG; in exact arithmetic the mean is $0$, and in floating point this removes the rounding part that is outside the range.

**Theorem 1 (the step is the orthogonal projection onto $V_h$).** Let $\mathbf{u}^{n+1} = \mathbf{u}^* - \Delta t\, Gp$ with $Ap = -D\mathbf{u}^*/\Delta t$. Then

1. $D\mathbf{u}^{n+1} = 0$;
2. $\langle \mathbf{u}^{n+1}, Gq\rangle = 0$ for every cell field $q$, so $\mathbf{u}^* = \mathbf{u}^{n+1} + \Delta t\, Gp$ is an orthogonal splitting, and $\|\mathbf{u}^{n+1}\|^2 + \Delta t^2\|Gp\|^2 = \|\mathbf{u}^*\|^2$;
3. $\mathbf{u}^{n+1} = P_h\mathbf{u}^*$, where $P_h$ is the orthogonal projector onto $V_h$; it depends on $\mathbf{u}^*$ only, not on $\Delta t$ and not on which solution $p$ is chosen.

*Proof.* (1) $D\mathbf{u}^{n+1} = D\mathbf{u}^* - \Delta t\, DGp = D\mathbf{u}^* + \Delta t\, Ap = D\mathbf{u}^* - D\mathbf{u}^* = 0$. (2) By Lemma 1 and (1), $\langle \mathbf{u}^{n+1}, Gq\rangle = -(D\mathbf{u}^{n+1}, q) = 0$; Pythagoras gives the norm identity. (3) By Lemma 1, the orthogonal complement of $V_h = \ker D$ is the range of $D^T = -G$, the discrete gradients. By (1) and (2), $\mathbf{u}^{n+1} \in V_h$ and $\mathbf{u}^* - \mathbf{u}^{n+1} = \Delta t\, Gp$ is orthogonal to $V_h$. The orthogonal decomposition of $\mathbf{u}^*$ into a part in $V_h$ and a part in $V_h^\perp$ is unique, so $\mathbf{u}^{n+1} = P_h\mathbf{u}^*$. $\square$

This is the discrete form of the [Helmholtz-Hodge decomposition](/helmholtz-hodge-decomposition/) on a periodic domain. The tests check (1) to $10^{-10}$, the orthogonality in (2) and $P_h^2 = P_h$ on random data.

**Theorem 2 (equivalence with forward Euler).** Let $\mathbf{u}^0 \in V_h$. Then the iterates of CHORIN-PROJECTION satisfy $\mathbf{u}^{n+1} = \mathbf{u}^n + \Delta t\, P_h F_h(\mathbf{u}^n)$, which is the [forward Euler method](/euler-method/) for the system of ordinary differential equations $\mathbf{u}' = P_h F_h(\mathbf{u})$ on $V_h$. This system is the method-of-lines form of the discrete Navier-Stokes equations $\mathbf{u}' = F_h(\mathbf{u}) - Gp$, $D\mathbf{u} = 0$.

*Proof.* Line L2 gives $\mathbf{u}^* = \mathbf{u}^n + \Delta t\, F_h(\mathbf{u}^n)$, and Theorem 1 gives $\mathbf{u}^{n+1} = P_h\mathbf{u}^* = P_h\mathbf{u}^n + \Delta t\, P_h F_h(\mathbf{u}^n)$ because $P_h$ is linear. By induction $\mathbf{u}^n \in V_h$, so $P_h\mathbf{u}^n = \mathbf{u}^n$. For the second claim, apply $P_h$ to $\mathbf{u}' = F_h(\mathbf{u}) - Gp$: $P_h G p = 0$ because gradients are orthogonal to $V_h$, and $P_h\mathbf{u}' = \mathbf{u}'$ because $D\mathbf{u}' = (D\mathbf{u})' = 0$. Conversely, a solution of $\mathbf{u}' = P_hF_h(\mathbf{u})$ in $V_h$ solves the pair with $Gp = (I - P_h)F_h(\mathbf{u})$, which is a gradient by Lemma 1. $\square$

**Corollary (first order in time).** For a fixed grid, $F_h$ is a polynomial in the face values, so it is Lipschitz on bounded sets, and $P_h$ has norm $1$. If the exact solution of $\mathbf{u}' = P_hF_h(\mathbf{u})$ stays bounded on $[0, T]$, the standard convergence theorem for forward Euler gives $\max_{n\Delta t \le T}\|\mathbf{u}^n - \mathbf{u}(n\Delta t)\| = O(\Delta t)$ as $\Delta t \to 0$. On the periodic grid the projection adds no splitting error of its own. The pressure $p$ of line L4 equals $p$ of the semi-discrete system evaluated at $\mathbf{u}^n$ up to $O(\Delta t)$, because $Gp = (I - P_h)\mathbf{u}^*/\Delta t = (I - P_h)F_h(\mathbf{u}^n)$.

The spatial error, second order on the MAC grid for smooth solutions, is not proved here; the tests measure it on the Taylor-Green vortex. With walls and an implicit viscous term, Theorem 2 no longer holds as stated, because $\mathbf{u}^*$ then satisfies a boundary condition that $P_h$ changes; this is the splitting error discussed on the main page.

**Termination.** The outer loop (line L1) runs $N$ times. Each step does $O(M)$ arithmetic outside the pressure solve. CG on the symmetric positive semidefinite system of Lemma 2 with a right side in the range ends in at most $M - 1$ iterations in exact arithmetic, because its iterates stay in the range, where $A$ is positive definite. In floating point the implementation stops at the residual tolerance or at a fixed iteration cap of $10M$, so each step ends.
