---
title: Correctness of CGLS
proves: [correctness, termination]
status: full
---

Exact arithmetic, finite dimension. $A$ is a real $m \times n$ matrix of rank $r \ge 1$, $M = A^T A$, and $N = \operatorname{range}(A^T)$, which is the orthogonal complement of $\operatorname{null}(A)$. The values $x_k, r_k, s_k, p_k, \gamma_k, \alpha_k, \beta_k$ are those of the pseudocode after $k$ passes of the loop: $r_0 = y - A x_0$, $s_0 = p_0 = A^T r_0$ and $\gamma_0 = \|s_0\|^2$ (line L1), then lines L5 to L11. $\mathcal{K}_k = \operatorname{span}\{s_0, M s_0, \ldots, M^{k-1} s_0\}$ is the Krylov space $\mathcal{K}_k(A^T A, A^T r_0)$. (For an operator between Hilbert spaces the same statements hold before breakdown, with the same proofs; see Engl, Hanke and Neubauer, Chapter 7.)

**Step 1 (CGLS is CG on the normal equations).** Put $z_k = x_k - x_0$ and $b = s_0 = A^T r_0$. Then $r_k = y - A x_k$ and $s_k = A^T r_k = b - M z_k$ for every $k$, and the sequence $(z_k, s_k, p_k)$ is the sequence of the conjugate gradient method for $M z = b$ from $z_0 = 0$.

*Proof.* Induction on $k$. At $k = 0$ this is line L1. Assume it for $k$. Line L8 gives $r_{k+1} = r_k - \alpha_k A p_k = y - A x_k - \alpha_k A p_k = y - A x_{k+1}$ by line L7. Line L9 gives $s_{k+1} = A^T r_{k+1} = s_k - \alpha_k M p_k$, which is the residual update of CG for $M z = b$. Line L6 gives $\alpha_k = \gamma_k/\|A p_k\|^2 = \|s_k\|^2/(p_k^T M p_k)$, the CG step length, and lines L10 and L11 are the CG updates $\beta_k = \|s_{k+1}\|^2/\|s_k\|^2$ and $p_{k+1} = s_{k+1} + \beta_k p_k$. Finally $b - M z_{k+1} = A^T r_0 - A^T A (x_{k+1} - x_0) = A^T (y - A x_{k+1}) = s_{k+1}$. $\square$

**Step 2 (restriction to $N$).** $M$ maps $N$ into $N$, and $M$ is positive definite on $N$: for $0 \ne z \in N$ we have $A z \ne 0$, since $N \cap \operatorname{null}(A) = \{0\}$, so $z^T M z = \|A z\|^2 > 0$. Since $b = A^T r_0 \in N$, all of $s_k$, $p_k$, $z_k$ and $\mathcal{K}_k$ lie in $N$. In an orthonormal basis of $N$, $M$ restricted to $N$ is a symmetric positive definite matrix of order $r$. So the theorem and corollaries of the [conjugate gradient method](/conjugate-gradient-method/) apply to it. As long as $s_0, \ldots, s_{k-1}$ are nonzero:

- the residuals $s_0, \ldots, s_k$ are pairwise orthogonal, and $\operatorname{span}\{s_0, \ldots, s_{k-1}\} = \operatorname{span}\{p_0, \ldots, p_{k-1}\} = \mathcal{K}_k$, of dimension $k$;
- $p_j^T M p_i = 0$ for $i \ne j$, and $p_j \ne 0$ for $j < k$;
- $z_k$ minimizes $\|z - z^*\|_M = \|A(z - z^*)\|$ over $z \in \mathcal{K}_k$, where $z^* \in N$ solves $M z^* = b$;
- some $s_k$ with $k \le r$ is zero.

In particular the division at line L6 is safe: if $\gamma_k \ne 0$, then $p_k \ne 0$ and $p_k \in N$, so $\|A p_k\| > 0$.

**Theorem 1 (residual minimization).** If $s_0, \ldots, s_{k-1} \ne 0$, then $x_k$ minimizes $\|y - A x\|$ over $x \in x_0 + \mathcal{K}_k$, and $\|y - A x_{k+1}\| \le \|y - A x_k\|$.

*Proof.* For $x = x_0 + z$, $y - A x = (r_0 - A z^*) + A(z^* - z)$. The two parts are orthogonal: $\langle r_0 - A z^*, A w\rangle = \langle A^T r_0 - M z^*, w\rangle = \langle b - M z^*, w\rangle = 0$ for every $w$. So $\|y - A x\|^2 = \|r_0 - A z^*\|^2 + \|A(z - z^*)\|^2$, and minimizing the residual over $x_0 + \mathcal{K}_k$ is minimizing $\|z - z^*\|_M$ over $\mathcal{K}_k$, which $z_k$ does by Step 2. The spaces are nested, $\mathcal{K}_k \subseteq \mathcal{K}_{k+1}$, so the minimum does not increase. $\square$

**Theorem 2 (finite termination).** Line L4 returns after at most $r$ passes of the loop (if no earlier return happens), and then $x_k$ is a least squares solution. If $x_0 \in N$ (for example $x_0 = 0$), it is the minimum norm least squares solution $A^\dagger y$.

*Proof.* By Step 2, some $s_k$ with $k \le r$ is zero, so $\gamma_k = 0$ and line L4 returns. Then $A^T(y - A x_k) = s_k = 0$: $x_k$ solves the normal equations, so it is a least squares solution. If $x_0 \in N$, then $x_k = x_0 + z_k \in N = \operatorname{null}(A)^\perp$. The least squares solutions are $A^\dagger y + \operatorname{null}(A)$, and the only one orthogonal to $\operatorname{null}(A)$ is $A^\dagger y$. $\square$

**Theorem 3 (the norm of the iterate grows).** Let $x_0 = 0$. Then $\|x_{k+1}\| > \|x_k\|$ for every $k$ with $s_k \ne 0$.

*Proof.* First, $\langle p_i, p_j\rangle > 0$ for $j < i$ before breakdown. Indeed $s_i \perp \mathcal{K}_i \ni p_j$, so $\langle p_i, p_j\rangle = \langle s_i + \beta_{i-1} p_{i-1}, p_j\rangle = \beta_{i-1}\langle p_{i-1}, p_j\rangle$, and by repeating this, $\langle p_i, p_j\rangle = \beta_{i-1} \cdots \beta_j \|p_j\|^2 > 0$, since every $\beta$ is positive before breakdown. Now $x_k = \sum_{j<k} \alpha_j p_j$ with every $\alpha_j > 0$, so $\langle x_k, p_k\rangle \ge 0$ and
$$\|x_{k+1}\|^2 = \|x_k\|^2 + 2\alpha_k\langle x_k, p_k\rangle + \alpha_k^2\|p_k\|^2 > \|x_k\|^2. \qquad \square$$

**Theorem 4 (the discrepancy test passes).** Let $y = A x^\dagger$, $\|y^\delta - y\| \le \delta$ and $\tau > 1$, and run CGLS on $y^\delta$ with $K \ge r$. Then line L3 returns some $x_k$ with $\|y^\delta - A x_k\| \le \tau\delta$, and every earlier iterate has a residual above $\tau\delta$.

*Proof.* If line L3 never returns before the breakdown of Theorem 2, then at breakdown $x_k$ is a least squares solution, so $y^\delta - A x_k$ is the projection of $y^\delta$ onto $\operatorname{range}(A)^\perp$. Since $y \in \operatorname{range}(A)$, this is the projection of $y^\delta - y$, of norm at most $\delta < \tau\delta$. Line L3 comes before line L4 in the loop, so it returns at that $k$ at the latest. It tests the iterates in order of $k$, which gives the last claim. $\square$

**Theorem 5 (filter factors).** Let $x_0 = 0$, let $A = \sum_i \sigma_i u_i v_i^T$ be the SVD, and let $s_0, \ldots, s_{k-1} \ne 0$. Let $\theta_1, \ldots, \theta_k$ be the Ritz values of $M$ on $\mathcal{K}_k$, that is, the eigenvalues of $Q^T M Q$ for an orthonormal basis $Q$ of $\mathcal{K}_k$. Then
$$x_k = \sum_{i=1}^{r} f_i^{(k)} \frac{u_i^T y}{\sigma_i} v_i, \qquad f_i^{(k)} = 1 - \prod_{j=1}^{k}\Big(1 - \frac{\sigma_i^2}{\theta_j}\Big).$$

*Proof.* Since $x_k \in \mathcal{K}_k$, $x_k = q(M) b$ for a polynomial $q$ of degree less than $k$, and $s_k = b - M x_k = R(M) b$ with $R(\lambda) = 1 - \lambda q(\lambda)$, a polynomial of degree at most $k$ with $R(0) = 1$. In the SVD basis, $b = A^T y = \sum_i \sigma_i (u_i^T y) v_i$ and $M v_i = \sigma_i^2 v_i$, so the coefficient of $v_i$ in $x_k$ is $q(\sigma_i^2)\sigma_i (u_i^T y) = (1 - R(\sigma_i^2)) (u_i^T y)/\sigma_i$. It remains to show $R(\lambda) = \prod_j (1 - \lambda/\theta_j)$.

The residuals $s_j = R_j(M) b$ are pairwise orthogonal. In the eigenbasis of $M$ this says $\sum_i R_j(\lambda_i) R_l(\lambda_i) w_i = 0$ for $j \ne l$, with the weights $w_i = |v_i^T b|^2 \ge 0$ at the eigenvalues $\lambda_i = \sigma_i^2$. So $R_0, \ldots, R_k$ are orthogonal polynomials for a discrete measure with positive weights. Since $\dim \mathcal{K}_k = k$, the polynomials of degree less than $k$ are not zero on the support, so the support has at least $k$ points. Then $R = R_k$ has exactly $k$ simple real roots, all in $(0, \|A\|^2]$, which is a standard property of orthogonal polynomials. Write $R(\lambda) = \prod_j (1 - \lambda/\mu_j)$ with these roots $\mu_j$, which is possible because $R(0) = 1$.

For each $j$ put $g_j(\lambda) = \prod_{l \ne j}(1 - \lambda/\mu_l)$ and $w_j = g_j(M) b \in \mathcal{K}_k$. Then $(M - \mu_j I) w_j = -\mu_j R(M) b = -\mu_j s_k$, which is orthogonal to $\mathcal{K}_k$. So $w_j$ satisfies the Galerkin condition of a Ritz pair with Ritz value $\mu_j$: with $w_j = Q c_j$, $(Q^T M Q - \mu_j I) c_j = 0$. The $k$ polynomials $g_j$ are linearly independent (each vanishes at all roots but its own), and $p \mapsto p(M) b$ is one-to-one on the polynomials of degree less than $k$ because $\dim \mathcal{K}_k = k$. So $c_1, \ldots, c_k$ are $k$ independent eigenvectors of the $k \times k$ matrix $Q^T M Q$, with eigenvalues $\mu_1, \ldots, \mu_k$. These are all its eigenvalues: $\{\mu_j\} = \{\theta_j\}$. $\blacksquare$
