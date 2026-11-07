---
title: Biorthogonality and finite termination of BiCG
proves: [correctness, termination]
status: full
---

Exact arithmetic. Notation of the page; write $\langle \tilde v, w \rangle = \tilde v^T w$. Indices refer to the values after the $k$th pass of L5 to L10, with $r_0 = b - A x_0$, $p_0 = r_0$, $\tilde p_0 = \tilde r_0$, $\rho_k = \tilde r_k^T r_k$, $\sigma_k = \tilde p_k^T A p_k$. Assume no breakdown up to step $k$: $\rho_j \ne 0$ and $\sigma_j \ne 0$ for $j < k$.

The recurrences are, for $j \ge 0$,
$$r_{j+1} = r_j - \alpha_j A p_j, \quad \tilde r_{j+1} = \tilde r_j - \alpha_j A^T \tilde p_j, \quad p_{j+1} = r_{j+1} + \beta_j p_j, \quad \tilde p_{j+1} = \tilde r_{j+1} + \beta_j \tilde p_j,$$
with $\alpha_j = \rho_j / \sigma_j$ and $\beta_j = \rho_{j+1} / \rho_j$, and $x_{j+1} = x_j + \alpha_j p_j$.

**Lemma 1 (invariant).** $b - A x_j = r_j$ for all $j$.

*Proof.* True for $j = 0$; and $b - A x_{j+1} = r_j - \alpha_j A p_j = r_{j+1}$. $\square$

**Lemma 2 (spaces).** $r_j, p_j \in \mathcal K_{j+1}(A, r_0)$ and $\tilde r_j, \tilde p_j \in \mathcal K_{j+1}(A^T, \tilde r_0)$, and $x_j \in x_0 + \mathcal K_j(A, r_0)$.

*Proof.* Induction from the recurrences: multiplying by $A$ raises the index by one. $\square$

**Theorem 1 (biorthogonality).** For all $i \ne j$ with $i, j \le k$:
$$\text{(a)} \ \tilde r_i^T r_j = 0, \qquad \text{(b)} \ \tilde p_i^T A p_j = 0.$$

*Proof.* Induction on $k$. For $k = 0$ there is nothing to prove. Assume (a) and (b) for indices up to $k$; we show them for pairs involving $k + 1$. By symmetry of the argument (swap the roles of $A$ and $A^T$, primal and shadow), it suffices to show $\tilde r_i^T r_{k+1} = 0$ and $\tilde p_i^T A p_{k+1} = 0$ for $i \le k$; the transposed statements $\tilde r_{k+1}^T r_i = 0$ and $\tilde p_{k+1}^T A p_i = (A^T \tilde p_{k+1})^T p_i = 0$ follow in the same way.

*Step 1: $\tilde p_i^T r_{k+1} = 0$ for $i \le k$.* Note $\tilde p_i = \tilde r_i + \beta_{i-1} \tilde p_{i-1}$ is a combination of $\tilde r_0, \dots, \tilde r_i$. For $i < k$: $\tilde p_i^T r_{k+1} = \tilde p_i^T r_k - \alpha_k \tilde p_i^T A p_k = 0 - 0$, by the induction hypotheses (a) (since $\tilde p_i$ is a combination of $\tilde r_0, \dots, \tilde r_i$, $i < k$) and (b). For $i = k$: $\tilde p_k^T r_k = \tilde r_k^T r_k + \beta_{k-1} \tilde p_{k-1}^T r_k = \rho_k + 0$, so $\tilde p_k^T r_{k+1} = \rho_k - \alpha_k \sigma_k = 0$ by the choice of $\alpha_k$.

*Step 2: (a) for $k + 1$.* $\tilde r_i = \tilde p_i - \beta_{i-1} \tilde p_{i-1}$ (with $\tilde p_{-1} = 0$), so $\tilde r_i^T r_{k+1} = 0$ by Step 1.

*Step 3: (b) for $k + 1$.* For $i \le k$, $A^T \tilde p_i = (\tilde r_i - \tilde r_{i+1}) / \alpha_i$, so
$$\tilde p_i^T A p_{k+1} = \tilde p_i^T A r_{k+1} + \beta_k \tilde p_i^T A p_k = \frac{(\tilde r_i - \tilde r_{i+1})^T r_{k+1}}{\alpha_i} + \beta_k \tilde p_i^T A p_k.$$
For $i < k$ both terms vanish by (a) for $k + 1$ (Step 2) and (b). For $i = k$ the first term is $-\tilde r_{k+1}^T r_{k+1} / \alpha_k = -\rho_{k+1} \sigma_k / \rho_k$ (using $\tilde r_k^T r_{k+1} = 0$) and the second is $\beta_k \sigma_k = \rho_{k+1} \sigma_k / \rho_k$; they cancel. ($\alpha_i \ne 0$ because $\rho_i \ne 0$.) $\square$

**Corollary 1 (Petrov-Galerkin).** $r_k \perp \mathcal K_k(A^T, \tilde r_0)$.

*Proof.* By Lemma 2 and the nonvanishing $\rho_j$, $\tilde r_0, \dots, \tilde r_{k-1}$ are independent (Theorem 1(a) makes the matrix $[\tilde r_i^T r_j]$ diagonal with nonzero diagonal) and lie in $\mathcal K_k(A^T, \tilde r_0)$, so they span it; $r_k$ is orthogonal to each by Theorem 1(a). $\square$

**Theorem 2 (finite termination).** If no breakdown occurs, then $r_k = 0$ for some $k \le n$, and then $x_k = A^{-1} b$.

*Proof.* Suppose $r_0, \dots, r_n$ are all nonzero and no breakdown occurs, so $\rho_0, \dots, \rho_n \ne 0$. The $(n+1) \times (n+1)$ matrix $[\tilde r_i^T r_j]$ is diagonal with nonzero diagonal by Theorem 1(a), hence nonsingular, so $r_0, \dots, r_n$ would be $n + 1$ independent vectors in $\mathbb{R}^n$, a contradiction. So $r_k = 0$ for some $k \le n$ (the L4 test catches it before any division, since $\rho$ is tested after the residual), and $A x_k = b$ by Lemma 1. $\square$

**Theorem 3 (the code terminates).** The loop L3 runs at most $\mathrm{kmax} + 1$ times; each pass either returns in L4 or L5 or completes. So the code always returns, with CONVERGED, a breakdown flag, or NOT-CONVERGED after $\mathrm{kmax}$ updates. $\blacksquare$
