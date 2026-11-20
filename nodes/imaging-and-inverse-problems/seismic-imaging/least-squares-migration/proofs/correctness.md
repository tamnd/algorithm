---
title: Correctness of least-squares migration
proves: [correctness, termination]
status: full
---

**Setting.** $L$ is a real $N_d \times n$ matrix (the linear modeling operator), $L^{\mathsf T}$ is its transpose (migration), and $d \in \mathbb{R}^{N_d}$ is the data. Least-squares migration asks for a minimizer of $\Phi(m) = \|L m - d\|^2$. All statements are in exact arithmetic. The iteration index $k$ counts the passes of the loop at line L3; $m_k, r_k, s_k, p_k, \gamma_k$ are the values after $k$ passes.

**Lemma 1 (the minimizers).** $m$ minimizes $\Phi$ if and only if $L^{\mathsf T}(d - L m) = 0$ (the normal equations). A minimizer exists, and there is exactly one minimizer in the range of $L^{\mathsf T}$: the minimum-norm solution.

*Proof.* $\Phi$ is a convex quadratic with the gradient $-2L^{\mathsf T}(d - Lm)$, so its minimizers are its stationary points. Write $d = d_1 + d_2$ with $d_1$ in the range of $L$ and $d_2$ orthogonal to it. Then $\Phi(m) = \|Lm - d_1\|^2 + \|d_2\|^2$, and $Lm = d_1$ has a solution. Two solutions differ by an element of the null space of $L$, which is orthogonal to the range of $L^{\mathsf T}$, so at most one solution lies in that range, and the projection of any solution onto it is a solution. $\square$

**Lemma 2 (invariants).** After every pass, $r_k = d - L m_k$ and $s_k = L^{\mathsf T} r_k$.

*Proof.* Induction. At the start $m_0 = 0$, and lines L1 and L2 set $r_0 = d$ and $s_0 = L^{\mathsf T}d$. In a pass, line L5 sets $q = L p$, and lines L7 and L8 change $m$ by $\alpha p$ and $r$ by $-\alpha q$, so $d - L(m + \alpha p) = r - \alpha q$. Line L9 recomputes $s = L^{\mathsf T} r$. $\square$

**Theorem 1 (CGLS is CG on the normal equations).** Let $A = L^{\mathsf T}L$ and $b = L^{\mathsf T}d$. The iterates $m_k$ are the iterates of the conjugate gradient method for $A m = b$ started at 0. Hence:

1. $m_k$ minimizes $\Phi$ over the Krylov space $\mathcal{K}_k = \operatorname{span}\{b, Ab, \ldots, A^{k-1}b\}$;
2. the residual norms $\|r_k\| = \|d - L m_k\|$ returned in the list are non-increasing in $k$;
3. if $\gamma_k > 0$ then $\|L p_k\| > 0$, so line L6 never divides by zero;
4. $\gamma_k = 0$ happens after at most $\operatorname{rank}(L) \le n$ passes, and then $m_k$ is the minimum-norm minimizer of $\Phi$.

*Proof.* By Lemma 2 the CG residual is $b - A m_k = L^{\mathsf T}(d - L m_k) = s_k$, and $\gamma_k = \|s_k\|^2$. The CG step length is $\|s_k\|^2/(p_k^{\mathsf T} A p_k) = \gamma_k/\|L p_k\|^2$, which is line L6, and the CG update $p_{k+1} = s_{k+1} + (\|s_{k+1}\|^2/\|s_k\|^2)\,p_k$ is line L10. So the two methods produce the same sequences.

The standard results for CG on a symmetric positive semidefinite system with $b$ in the range of $A$ (see the conjugate gradient method and CGLS pages) give: the residuals $s_0, s_1, \ldots$ are mutually orthogonal, $p_k^{\mathsf T}s_k = \|s_k\|^2$, and $m_k$ minimizes the $A$-norm error $(m - m^\star)^{\mathsf T}A(m - m^\star)$ over $\mathcal{K}_k$ for any solution $m^\star$. Since $(m - m^\star)^{\mathsf T}A(m - m^\star) = \|Lm - Lm^\star\|^2 = \Phi(m) - \Phi(m^\star)$, this is item 1. The spaces $\mathcal{K}_k$ are nested, so item 2 follows.

For item 3, $\|Lp_k\|^2 = p_k^{\mathsf T}Ap_k$ and, by Lemma 2, $\langle r_k, Lp_k\rangle = \langle s_k, p_k\rangle = \gamma_k > 0$, so $Lp_k \ne 0$.

For item 4, $b = L^{\mathsf T}d$ and all $\mathcal{K}_k$ lie in the range of $L^{\mathsf T}$, which has the dimension $\operatorname{rank}(L)$. The nonzero residuals $s_k$ are orthogonal and lie in this range, so at most $\operatorname{rank}(L)$ of them are nonzero. When $\gamma_k = 0$, $s_k = 0$, so $m_k$ solves the normal equations; it lies in the range of $L^{\mathsf T}$, so by Lemma 1 it is the minimum-norm minimizer. Line L4 then stops the loop, and in any case the loop has at most `iters` passes, and line L11 returns. $\blacksquare$

**Lemma 3 (damping).** For $\varepsilon > 0$, the stacked operator $\tilde L = \begin{bmatrix} L \\ \sqrt{\varepsilon}\, I\end{bmatrix}$ and the stacked data $\tilde d = (d, 0)$ of `damped` satisfy $\|\tilde L m - \tilde d\|^2 = \|Lm - d\|^2 + \varepsilon\|m\|^2$. The transpose $\tilde L^{\mathsf T}(r_1, r_2) = L^{\mathsf T}r_1 + \sqrt{\varepsilon}\, r_2$ is the second function returned. The damped problem has exactly one minimizer, the solution of $(L^{\mathsf T}L + \varepsilon I)m = L^{\mathsf T}d$, and CGLS on $(\tilde L, \tilde d)$ reaches it in at most $n$ passes.

*Proof.* The first identity is the sum of the squared norms of the two blocks. The transpose of a stacked matrix is the row of the transposes. $\tilde L^{\mathsf T}\tilde L = L^{\mathsf T}L + \varepsilon I$ is positive definite, so the normal equations have one solution and $\operatorname{rank}(\tilde L) = n$; apply Theorem 1. $\square$

**Lemma 4 (the sparse operator).** For the sparse rows of `born_kirchhoff_operator`, `matvec` and `rmatvec` are exact transposes: $\langle \mathrm{matvec}(x), y\rangle = \langle x, \mathrm{rmatvec}(y)\rangle$.

*Proof.* Both sides equal $\sum_k \sum_{(c, w) \in \text{row } k} w\, x_c\, y_k$; `rmatvec` skips rows with $y_k = 0$, which add nothing. $\square$

The hypothesis of Theorem 1 that the second operator is the transpose of the first is essential: with an approximate adjoint, the residuals need not decrease. Lemma 4 and the adjoint test of the page check it for the example.

**What is not claimed.** Theorem 1 is about the misfit $\|Lm - d\|$. It does not say that $m_k$ approaches the true reflectivity: the true model and the minimum-norm minimizer differ by a null-space component, and noise in $d$ is fitted too, so in practice the iteration is stopped early or damped (a heuristic choice). The statement that the least-squares image is closer to the true model than the scaled migrated image is a measurement for the example on the page, not a theorem. In floating-point arithmetic the orthogonality of the residuals is lost slowly, so finite termination does not hold exactly.
