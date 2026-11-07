---
title: In exact arithmetic MINRES returns the iterate of least residual norm in x0 + K_k, and it terminates
proves: [correctness, termination]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$ be symmetric, $r_0 = b - A x_0 \ne 0$, $\beta = \|r_0\|_2$ and $\mathcal{K}_k = \mathcal{K}_k(A, r_0)$. Arithmetic is exact. Line numbers refer to the pseudocode.

**Lemma 1 (Lanczos).** Lines L4, L5 and L11 are the symmetric Lanczos process started from $v_1 = r_0/\beta$. While $\gamma_{j+1} \ne 0$ for $j < k$, the vectors $v_1, \ldots, v_k$ are orthonormal and span $\mathcal{K}_k$, and
$$A V_k = V_{k+1} \bar T_k, \qquad \bar T_k = \begin{pmatrix} T_k \\ \gamma_{k+1} e_k^T \end{pmatrix},$$
where $V_k = (v_1 \cdots v_k)$ and $T_k$ is symmetric tridiagonal with diagonal $\delta_1, \ldots, \delta_k$ and off-diagonal $\gamma_2, \ldots, \gamma_k$.

*Proof.* Line L5 computes $\gamma_{k+1} v_{k+1} = A v_k - \delta_k v_k - \gamma_k v_{k-1}$ with $\delta_k = v_k^T A v_k$ (L4, after the normalization of L4). Induction on $k$: $v_{k+1}$ is orthogonal to $v_k$ by the choice of $\delta_k$, to $v_{k-1}$ because $v_{k-1}^T A v_k = (A v_{k-1})^T v_k = \gamma_k$ by symmetry of $A$ and the previous step, and to $v_j$ for $j < k - 1$ because $A v_j \in \mathrm{span}\{v_{j-1}, v_j, v_{j+1}\}$ is orthogonal to $v_k$. Since $v_{k+1}$ is $A v_k$ minus a combination of $v_1, \ldots, v_k$, the spans are the Krylov spaces. Reading L5 column by column gives the matrix identity. $\square$

**Lemma 2 (the least squares problem).** For $x = x_0 + V_k y$,
$$\|b - A x\|_2 = \|\beta e_1 - \bar T_k y\|_2 .$$

*Proof.* $b - A x = r_0 - A V_k y = V_{k+1}(\beta e_1 - \bar T_k y)$ by Lemma 1, and $V_{k+1}$ has orthonormal columns. $\square$

So the minimizer of $\|b - A x\|_2$ over $x_0 + \mathcal{K}_k$ is $x_0 + V_k y_k$ with $y_k$ the least squares solution of $\bar T_k y \approx \beta e_1$, a $(k+1) \times k$ problem.

**Lemma 3 (Givens QR, lines L6 and L7).** Let $Q_k = G_k G_{k-1} \cdots G_1$, where $G_j$ is the rotation $\begin{pmatrix} c_{j+1} & s_{j+1} \\ -s_{j+1} & c_{j+1} \end{pmatrix}$ acting on rows $j$ and $j + 1$. Then $Q_k \bar T_k = \begin{pmatrix} R_k \\ 0 \end{pmatrix}$ with $R_k$ upper triangular, of bandwidth 3, with column $k$ equal to $(\ldots, 0, \alpha_3, \alpha_2, \alpha_1)^T$ in rows $k-2, k-1, k$ for the values computed at step $k$, and $Q_k \beta e_1 = (\tau_1, \ldots, \tau_k, \eta_k)^T$ with $\tau_k = c_{k+1}\eta_{k-1}$, $\eta_k = -s_{k+1}\eta_{k-1}$, $\eta_0 = \beta$.

*Proof.* Column $k$ of $\bar T_k$ has $\gamma_k$ in row $k-1$, $\delta_k$ in row $k$ and $\gamma_{k+1}$ in row $k+1$, and zeros elsewhere. The rotations $G_1, \ldots, G_{k-3}$ touch rows above $k-2$ only, so they leave it unchanged. $G_{k-2}$ (with $c_{k-1}, s_{k-1}$, called `c_old`, `s_old`) maps the pair $(0, \gamma_k)$ in rows $k-2, k-1$ to $(s_{k-1}\gamma_k, c_{k-1}\gamma_k)$, so $\alpha_3 = s_{k-1}\gamma_k$. $G_{k-1}$ (with $c_k, s_k$) maps $(c_{k-1}\gamma_k, \delta_k)$ in rows $k-1, k$ to $(c_k c_{k-1}\gamma_k + s_k\delta_k,\; c_k\delta_k - s_k c_{k-1}\gamma_k) = (\alpha_2, \alpha_0)$. Line L7 chooses $c_{k+1} = \alpha_0/\alpha_1$, $s_{k+1} = \gamma_{k+1}/\alpha_1$ with $\alpha_1 = (\alpha_0^2 + \gamma_{k+1}^2)^{1/2}$, so $G_k$ maps $(\alpha_0, \gamma_{k+1})$ to $(\alpha_1, 0)$ and $R_k$ is upper triangular. The earlier columns were already reduced and $G_k$ touches only their zero rows $k$ and $k + 1$ below the triangle, except that it acts on rows $k$ and $k+1$ of the right side: the entry $\eta_{k-1}$ in row $k$ and $0$ in row $k+1$ become $c_{k+1}\eta_{k-1}$ and $-s_{k+1}\eta_{k-1}$. The start $c_0 = c_1 = 1$, $s_0 = s_1 = 0$ (line L2) makes the rotations of steps $-1$ and $0$ the identity. $\square$

**Theorem 1 (minimal residual).** If $\alpha_1 \ne 0$ at steps $1, \ldots, k$, the iterate $x_k$ after line L9 of step $k$ is the unique minimizer of $\|b - A x\|_2$ over $x_0 + \mathcal{K}_k$, and $\|b - A x_k\|_2 = |\eta_k|$.

*Proof.* With $Q_k$ orthogonal, $\|\beta e_1 - \bar T_k y\|_2^2 = \|t_k - R_k y\|_2^2 + \eta_k^2$ where $t_k = (\tau_1, \ldots, \tau_k)^T$. The diagonal of $R_k$ is the list of $\alpha_1$ values, all nonzero, so $R_k$ is nonsingular and the unique minimizer is $y_k = R_k^{-1} t_k$, with minimum $|\eta_k|$; Lemma 2 transfers this to $x$. Let $W_k = V_k R_k^{-1}$ with columns $w_1, \ldots, w_k$. From $W_k R_k = V_k$ and the band structure of $R_k$, $v_k = \alpha_3 w_{k-2} + \alpha_2 w_{k-1} + \alpha_1 w_k$, which is line L8 (with $w_0 = w_{-1} = 0$). Then $x_0 + V_k y_k = x_0 + W_k t_k$, and since $t_k$ extends $t_{k-1}$ by the single entry $\tau_k = c_{k+1}\eta_{k-1}$, $x_k = x_{k-1} + \tau_k w_k$, which is line L9. $\square$

**Corollary (monotone residuals).** $|\eta_k| = |s_{k+1}|\,|\eta_{k-1}| \le |\eta_{k-1}|$, as it must be since $\mathcal{K}_{k-1} \subseteq \mathcal{K}_k$. Equality holds when $\alpha_0 = 0$, that is, when $T_k$ is singular; this is the stagnation seen for spectra symmetric about $0$.

**Termination.** The loop at line L3 runs at most `maxiter` times, each step a fixed amount of work, so the algorithm stops. In exact arithmetic it stops earlier: let $d \le n$ be the grade of $r_0$, the dimension of the largest Krylov space. Then $\gamma_{d+1} = 0$, $\mathcal{K}_d$ is invariant under $A$, and $A V_d = V_d T_d$. If $A$ is nonsingular, every eigenvalue of $T_d$ is an eigenvalue of $A$, so $T_d$ is nonsingular, $\alpha_1 \ne 0$ at step $d$, and $s_{d+1} = \gamma_{d+1}/\alpha_1 = 0$ gives $\eta_d = 0$: line L10 returns with $A x_d = b$ after at most $d$ steps, and $d$ is at most the number of distinct eigenvalues of $A$. If $A$ is singular and $\eta_{d-1} \ne 0$, then $T_d$ is singular (otherwise the argument just given would produce an exact solution), so $\alpha_0 = 0$ and $\alpha_1 = 0$ at step $d$, and the implementation returns $x_{d-1}$. After $G_1, \ldots, G_{d-1}$, row $d$ of the reduced $\bar T_d$ is zero (its last entry is $\alpha_0 = 0$ and row $d + 1$ is $\gamma_{d+1} e_d^T = 0$), while rows $1$ to $d-1$ have full row rank. So the least squares minimum over $x_0 + \mathcal{K}_d$ equals $|\eta_{d-1}|$, and $x_{d-1}$ attains it.

**Before step $d$, $\alpha_1 \ne 0$.** For $k < d$, $\gamma_{k+1} \ne 0$, so $\alpha_1 = (\alpha_0^2 + \gamma_{k+1}^2)^{1/2} > 0$. Hence Theorem 1 applies at every step the loop reaches, which proves correctness.
