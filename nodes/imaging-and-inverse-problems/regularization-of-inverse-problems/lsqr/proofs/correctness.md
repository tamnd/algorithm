---
title: Correctness of LSQR
proves: [correctness, termination]
status: full
---

Exact arithmetic. $A$ is a real $m \times n$ matrix and $y \ne 0$ (for $y = 0$ the code returns $x_0 = 0$ at once). The quantities are those of the pseudocode: line L1 sets $\beta_1 u_1 = y$, $\alpha_1 v_1 = A^T u_1$, $w_1 = v_1$, $x_0 = 0$, $\bar\phi_1 = \beta_1$, $\bar\rho_1 = \alpha_1$, where each $\beta_j, \alpha_j \ge 0$ is the norm that makes $u_j, v_j$ unit vectors. Step $k \ge 1$ computes
$$\beta_{k+1} u_{k+1} = A v_k - \alpha_k u_k, \qquad \alpha_{k+1} v_{k+1} = A^T u_{k+1} - \beta_{k+1} v_k \qquad \text{(L3, L4)},$$
$$\rho_k = \sqrt{\bar\rho_k^2 + \beta_{k+1}^2}, \quad c_k = \bar\rho_k/\rho_k, \quad s_k = \beta_{k+1}/\rho_k \qquad \text{(L5)},$$
$$\theta_{k+1} = s_k \alpha_{k+1}, \quad \bar\rho_{k+1} = -c_k \alpha_{k+1}, \quad \phi_k = c_k \bar\phi_k, \quad \bar\phi_{k+1} = s_k \bar\phi_k \qquad \text{(L6)},$$
$$x_k = x_{k-1} + (\phi_k/\rho_k) w_k, \qquad w_{k+1} = v_{k+1} - (\theta_{k+1}/\rho_k) w_k \qquad \text{(L7)}.$$
"Before breakdown at step $k$" means $\alpha_1, \ldots, \alpha_k$ and $\beta_1, \ldots, \beta_{k+1}$ are all positive. $U_{k+1} = [u_1, \ldots, u_{k+1}]$, $V_k = [v_1, \ldots, v_k]$, and $B_k$ is the $(k+1) \times k$ lower bidiagonal matrix with diagonal $\alpha_1, \ldots, \alpha_k$ and subdiagonal $\beta_2, \ldots, \beta_{k+1}$.

**Lemma 1 (Golub-Kahan bidiagonalization).** Before breakdown at step $k$: the columns of $U_{k+1}$ are orthonormal, the columns of $V_{k+1}$ are orthonormal (where $v_{k+1}$ is defined, that is, $\alpha_{k+1} > 0$), and
$$A V_k = U_{k+1} B_k, \qquad A^T U_{k+1} = V_k B_k^T + \alpha_{k+1} v_{k+1} e_{k+1}^T.$$
Also $\operatorname{span}(V_k) = \mathcal{K}_k(A^T A, A^T y)$.

*Proof.* The two relations are lines L3 and L4 read column by column: $A v_j = \alpha_j u_j + \beta_{j+1} u_{j+1}$ and $A^T u_j = \beta_j v_{j-1} + \alpha_j v_j$ (with $v_0 = 0$). Orthonormality by induction on $k$; the base is that $u_1$ and $v_1$ are unit vectors. Assume $u_1, \ldots, u_k$ and $v_1, \ldots, v_k$ are orthonormal. For $j \le k$,
$$u_j^T A v_k = (A^T u_j)^T v_k = \beta_j v_{j-1}^T v_k + \alpha_j v_j^T v_k = \alpha_k [j = k],$$
so $u_j^T(A v_k - \alpha_k u_k) = 0$, and $u_{k+1} \perp u_1, \ldots, u_k$. Then for $j \le k$,
$$v_j^T A^T u_{k+1} = (A v_j)^T u_{k+1} = \alpha_j u_j^T u_{k+1} + \beta_{j+1} u_{j+1}^T u_{k+1} = \beta_{k+1} [j = k],$$
so $v_j^T(A^T u_{k+1} - \beta_{k+1} v_k) = 0$, and $v_{k+1} \perp v_1, \ldots, v_k$. For the spans: $v_1 \propto A^T y$, and by L3 and L4, $v_{k+1}$ is a combination of $A^T A v_k$, $v_k$ and $v_{k-1}$, so $v_{k+1} \in \mathcal{K}_{k+1}$ by induction. The $v_j$ are orthonormal, hence independent, so $V_k$ spans the $k$-dimensional space $\mathcal{K}_k$. $\square$

**Lemma 2 (the rotations).** Before breakdown at step $k$, every $\rho_j > 0$ for $j \le k$, and there is an orthogonal matrix $Q_k$ of order $k + 1$ with
$$Q_k \begin{bmatrix} B_k & \beta_1 e_1 \end{bmatrix} = \begin{bmatrix} R_k & f_k \\ 0 & \bar\phi_{k+1} \end{bmatrix},$$
where $R_k$ is upper bidiagonal with diagonal $\rho_1, \ldots, \rho_k$ and superdiagonal $\theta_2, \ldots, \theta_k$, and $f_k = (\phi_1, \ldots, \phi_k)^T$. Moreover the last row of $Q_k B_{k+1}$, restricted to the new column $k + 1$, has the entries $\theta_{k+1}$ (row $k$) and $\bar\rho_{k+1}$ (row $k + 1$).

*Proof.* Induction on $k$. Let $G_k$ be the identity except in rows and columns $k, k+1$, where it is $\begin{bmatrix} c_k & s_k \\ s_k & -c_k \end{bmatrix}$; it is orthogonal because $c_k^2 + s_k^2 = 1$. Put $Q_k = G_k Q_{k-1}$ (with $Q_{k-1}$ extended by a $1$ on the diagonal). By the induction hypothesis (or directly for $k = 1$), before $G_k$ acts, rows $k$ and $k+1$ of the matrix are $(0, \ldots, 0, \bar\rho_k \mid \bar\phi_k)$ and $(0, \ldots, 0, \beta_{k+1} \mid 0)$: row $k + 1$ is the new row of $B_k$, which the earlier rotations do not touch. $G_k$ maps the column pair $(\bar\rho_k, \beta_{k+1})$ to $(c_k\bar\rho_k + s_k\beta_{k+1},\ s_k\bar\rho_k - c_k\beta_{k+1}) = (\rho_k, 0)$, and the right side $(\bar\phi_k, 0)$ to $(\phi_k, \bar\phi_{k+1})$. Applied to the next column of $B_{k+1}$, which has $0$ in row $k$ and $\alpha_{k+1}$ in row $k + 1$, it gives $(s_k\alpha_{k+1}, -c_k\alpha_{k+1}) = (\theta_{k+1}, \bar\rho_{k+1})$. Positivity: $\bar\rho_1 = \alpha_1 > 0$. If $\bar\rho_j \ne 0$, then $\rho_j > 0$, $c_j \ne 0$, and $\bar\rho_{j+1} = -c_j\alpha_{j+1} \ne 0$ when $\alpha_{j+1} > 0$. So $\rho_j \ge |\bar\rho_j| > 0$ for all $j \le k$. $\square$

**Theorem 1 (LSQR minimizes the residual over the Krylov space).** Before breakdown at step $k$, $x_k = V_k z_k$ with $z_k = R_k^{-1} f_k$, $x_k$ is the unique minimizer of $\|y - A x\|$ over $\mathcal{K}_k(A^T A, A^T y)$, so it equals the CGLS iterate, and $\|y - A x_k\| = |\bar\phi_{k+1}|$.

*Proof.* Every $x \in \mathcal{K}_k$ is $x = V_k z$ for a unique $z$ (Lemma 1). Then $y - A x = \beta_1 u_1 - U_{k+1} B_k z = U_{k+1}(\beta_1 e_1 - B_k z)$, and since $U_{k+1}$ has orthonormal columns and $Q_k$ is orthogonal,
$$\|y - A x\|^2 = \|Q_k(\beta_1 e_1 - B_k z)\|^2 = \|f_k - R_k z\|^2 + \bar\phi_{k+1}^2.$$
$R_k$ is nonsingular by Lemma 2, so the unique minimizer is $z_k = R_k^{-1} f_k$, with residual norm $|\bar\phi_{k+1}|$. It remains to show that line L7 computes $V_k R_k^{-1} f_k$. Put $D_k = V_k R_k^{-1}$, with columns $d_j$. Reading $D_k R_k = V_k$ column by column gives $\rho_1 d_1 = v_1$ and $\theta_j d_{j-1} + \rho_j d_j = v_j$. With $w_j = \rho_j d_j$ this is $w_1 = v_1$ and $w_j = v_j - (\theta_j/\rho_{j-1}) w_{j-1}$, the update of line L7. The vector $f_k$ extends $f_{k-1}$ by one entry, because $G_k$ does not change rows $1, \ldots, k-1$. So $D_k f_k = \sum_{j \le k} \phi_j d_j = \sum_{j \le k} (\phi_j/\rho_j) w_j$, which is the sum that line L7 builds. By the correctness proof of [CGLS](/cgls/) (Theorem 1 there), the CGLS iterate is the same minimizer. $\square$

**Theorem 2 (breakdown gives the minimum norm solution).** If the loop stops with $\beta_{k+1} = 0$ or $\alpha_{k+1} = 0$ (and all earlier values positive), then $x_k = A^\dagger y$.

*Proof.* If $\beta_{k+1} = 0$, then $s_k = 0$ and $\bar\phi_{k+1} = 0$, so by Theorem 1 the residual is $0$ and $A x_k = y$. If $\alpha_{k+1} = 0$, Lemma 1 gives $A^T U_{k+1} = V_k B_k^T$, so $A^T(y - A x_k) = V_k B_k^T(\beta_1 e_1 - B_k z_k) = 0$, because $z_k$ solves the small least squares problem and so satisfies its normal equations. In both cases $x_k$ is a least squares solution. It lies in $\mathcal{K}_k \subseteq \operatorname{range}(A^T) = \operatorname{null}(A)^\perp$, and the only least squares solution orthogonal to $\operatorname{null}(A)$ is $A^\dagger y$. The process must break down: the $v_j$ are orthonormal in $\operatorname{range}(A^T)$, which has dimension $\operatorname{rank}(A)$, so $\alpha_{k+1} = 0$ or $\beta_{k+1} = 0$ for some $k \le \operatorname{rank}(A)$. $\square$

**Theorem 3 (the discrepancy test).** Let $y = A x^\dagger + e$ with $\|e\| \le \delta$ and $\tau > 1$. Then line L8 stops the loop at the first $k$ with $\|y - A x_k\| \le \tau\delta$, and such a $k \le \operatorname{rank}(A)$ exists.

*Proof.* By Theorem 1 the test of line L8 compares the true residual $|\bar\phi_{k+1}| = \|y - A x_k\|$ with $\tau\delta$. At breakdown, $x_k = A^\dagger y$ by Theorem 2, and $y - A x_k$ is the projection of $y$ onto $\operatorname{range}(A)^\perp$, which is the projection of $e$, of norm at most $\delta < \tau\delta$. So the test passes at the breakdown step at the latest. Since the test is made after every step in order, the first passing $k$ is returned. $\blacksquare$
