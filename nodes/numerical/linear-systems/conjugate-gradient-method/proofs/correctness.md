---
title: CG produces orthogonal residuals and conjugate directions, minimizes the A-norm error and terminates
proves: [correctness, termination]
status: full
---

Exact arithmetic. $A$ is symmetric positive definite, $x$ solves $A x = b$, and $r_k, p_k, x_k, \alpha_k, \beta_k, \rho_k = r_k^T r_k$ are the values of the pseudocode after $k$ passes (with tolerance $0$, so the loop stops only when $r_k = 0$). Write $\mathcal{K}_k = \mathcal{K}_k(A, r_0)$ and $\langle v, w \rangle_A = v^T A w$, an inner product because $A$ is positive definite.

**Theorem.** Let $k \ge 1$ and assume $r_0, \ldots, r_{k-1}$ are all nonzero. Then:

- (S) $\operatorname{span}\{r_0, \ldots, r_{k-1}\} = \operatorname{span}\{p_0, \ldots, p_{k-1}\} = \mathcal{K}_k$, and $x_k - x_0 \in \mathcal{K}_k$;
- (O) $r_k^T p_j = 0$ and $r_k^T r_j = 0$ for all $j < k$;
- (C) $p_k^T A p_j = 0$ for all $j < k$;
- (P) $p_j \ne 0$ and $p_j^T A p_j > 0$ for $j < k$, so each $\alpha_j$ is defined, and $\alpha_j = \rho_j / (p_j^T A p_j)$ with $\rho_j = r_j^T p_j$.

*Proof.* Induction on $k$.

*Base $k = 1$.* $p_0 = r_0 \ne 0$, so $p_0^T A p_0 > 0$ and (P) holds; $\mathcal{K}_1 = \operatorname{span}\{r_0\}$ and $x_1 - x_0 = \alpha_0 p_0$, so (S) holds. $r_1^T p_0 = r_0^T r_0 - \alpha_0 p_0^T A p_0 = \rho_0 - \rho_0 = 0$, and $r_0 = p_0$, so (O) holds. $p_1^T A p_0 = r_1^T A p_0 + \beta_0 p_0^T A p_0$. From line L7, $A p_0 = (r_0 - r_1)/\alpha_0$, so $r_1^T A p_0 = (r_1^T r_0 - \rho_1)/\alpha_0 = -\rho_1/\alpha_0$, and $p_0^T A p_0 = \rho_0/\alpha_0$. With $\beta_0 = \rho_1/\rho_0$ the sum is $-\rho_1/\alpha_0 + \rho_1/\alpha_0 = 0$, so (C) holds.

*Step.* Assume the statements for $1, \ldots, k$ and that $r_k \ne 0$; we prove them for $k + 1$.

(P) for $j = k$: by (O), $r_k^T p_{k-1} = 0$, so $\|p_k\|_2^2 = \|r_k + \beta_{k-1} p_{k-1}\|_2^2 = \|r_k\|_2^2 + \beta_{k-1}^2 \|p_{k-1}\|_2^2 \ge \|r_k\|_2^2 > 0$. So $p_k \ne 0$ and $p_k^T A p_k > 0$. Also $r_k^T p_k = r_k^T r_k + \beta_{k-1} r_k^T p_{k-1} = \rho_k$.

(S): $p_k = r_k + \beta_{k-1} p_{k-1}$ and $r_k = r_{k-1} - \alpha_{k-1} A p_{k-1}$, with $A p_{k-1} \in A \mathcal{K}_k \subseteq \mathcal{K}_{k+1}$. So $r_k, p_k \in \mathcal{K}_{k+1}$ and the spans of the first $k+1$ residuals and directions lie in $\mathcal{K}_{k+1}$. The directions $p_0, \ldots, p_k$ are nonzero and pairwise $A$-orthogonal by (C) and (P), so they are linearly independent, and their span has dimension $k + 1 \ge \dim \mathcal{K}_{k+1}$. So all three spaces are equal. The residuals $r_0, \ldots, r_k$ are nonzero and pairwise orthogonal by (O), so they span the same space too. Finally $x_{k+1} - x_0 = (x_k - x_0) + \alpha_k p_k \in \mathcal{K}_{k+1}$.

(O): $r_{k+1} = r_k - \alpha_k A p_k$. For $j < k$, $r_{k+1}^T p_j = r_k^T p_j - \alpha_k p_k^T A p_j = 0 - 0$ by (O) and (C). For $j = k$, $r_{k+1}^T p_k = \rho_k - \alpha_k p_k^T A p_k = 0$ by the formula for $\alpha_k$. So $r_{k+1}$ is orthogonal to $p_0, \ldots, p_k$, hence to $\mathcal{K}_{k+1}$ by (S), hence to $r_0, \ldots, r_k$.

(C): $p_{k+1}^T A p_j = r_{k+1}^T A p_j + \beta_k p_k^T A p_j$. For $j < k$: $A p_j \in \mathcal{K}_{j+2} \subseteq \mathcal{K}_{k+1}$, so the first term is $0$ by (O), and the second is $0$ by (C). For $j = k$: the computation of the base case, with $k$ in place of $0$, gives $r_{k+1}^T A p_k = -\rho_{k+1}/\alpha_k$ and $\beta_k p_k^T A p_k = (\rho_{k+1}/\rho_k)(\rho_k/\alpha_k)$, which sum to $0$. $\square$

**Corollary 1 (optimality).** Under the same assumption, $x_k$ is the unique minimizer of $\|x - y\|_A$ over $y \in x_0 + \mathcal{K}_k$.

*Proof.* Let $e_k = x - x_k$; then $A e_k = r_k$. For $y = x_k + w$ with $w \in \mathcal{K}_k$, $\|x - y\|_A^2 = \|e_k\|_A^2 - 2 w^T A e_k + \|w\|_A^2 = \|e_k\|_A^2 - 2 w^T r_k + \|w\|_A^2$. By (O) and (S), $w^T r_k = 0$. So $\|x - y\|_A^2 = \|e_k\|_A^2 + \|w\|_A^2$, which is smallest exactly for $w = 0$; and $x_k \in x_0 + \mathcal{K}_k$ by (S). $\square$

**Corollary 2 (termination).** Some $r_k$ with $k \le n$ is zero, so CG returns $x$ after at most $n$ passes of line L2 (if maxit $\ge n + 1$).

*Proof.* If $r_0, \ldots, r_{n-1}$ were all nonzero, then by (O) $r_n$ is orthogonal to the $n$ nonzero, pairwise orthogonal vectors $r_0, \ldots, r_{n-1}$, which span $\mathbb{R}^n$, so $r_n = 0$. If $r_k = 0$, line L3 returns $x_k$, and $A x_k = b$. $\square$

**Remark (fewer steps).** Write $r_0 = \sum_i c_i v_i$ in an orthonormal eigenbasis of $A$, and let $d$ be the number of distinct eigenvalues $\lambda$ with some $c_i \ne 0$ for $v_i$ in the eigenspace of $\lambda$. Then $\mathcal{K}_k$ lies in the span of the $d$ vectors $\sum_{\lambda_i = \lambda} c_i v_i$, so $\dim \mathcal{K}_k \le d$, and the argument of Corollary 2 within this space gives $r_d = 0$. $\blacksquare$
