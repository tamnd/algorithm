---
title: Correctness of the hybrid LSQR method
proves: [correctness, termination]
status: full
---

Exact arithmetic. $A: X \to Y$ is a bounded linear operator between Hilbert spaces (a real $m \times n$ matrix in the code), $y \ne 0$ are the data, and $\mathcal{K}_k = \mathrm{span}\{A^* y, (A^* A) A^* y, \dots, (A^* A)^{k-1} A^* y\}$. Lines L1, L3 and L4 compute, with $v_0 = 0$,
$$\beta_1 u_1 = y, \quad \alpha_1 v_1 = A^* u_1, \quad \beta_{j+1} u_{j+1} = A v_j - \alpha_j u_j, \quad \alpha_{j+1} v_{j+1} = A^* u_{j+1} - \beta_{j+1} v_j,$$
where each $\alpha$ and $\beta$ is the norm of the vector on the right, after the vector has been reorthogonalized against the earlier $u$'s or $v$'s. We say that no breakdown has occurred up to step $k$ if $\alpha_1, \dots, \alpha_{k}$ and $\beta_1, \dots, \beta_{k+1}$ are all positive. $B_k$ is the $(k+1) \times k$ matrix with $\alpha_1, \dots, \alpha_k$ on the diagonal and $\beta_2, \dots, \beta_{k+1}$ just below it, $U_{k+1} = [u_1, \dots, u_{k+1}]$ and $V_k = [v_1, \dots, v_k]$.

**Lemma 1 (Golub-Kahan relations).** If no breakdown has occurred up to step $k$, then the reorthogonalization subtracts nothing, $U_{k+1}$ and $V_{k+1}$ (if $\alpha_{k+1} > 0$) have orthonormal columns, and
$$A V_k = U_{k+1} B_k, \qquad A^* u_j = \beta_j v_{j-1} + \alpha_j v_j \ (j \le k+1), \qquad y = \beta_1 U_{k+1} e_1 .$$
Moreover the columns of $V_k$ form an orthonormal basis of $\mathcal{K}_k$.

*Proof.* Induction on $k$. For the start, $u_1 = y/\beta_1$ and $v_1 = A^* u_1/\alpha_1$ are unit vectors and $A^* u_1 = \alpha_1 v_1$.

Assume that $u_1, \dots, u_k$ and $v_1, \dots, v_k$ are orthonormal, that $A v_j = \alpha_j u_j + \beta_{j+1} u_{j+1}$ for $j < k$, and that $A^* u_j = \beta_j v_{j-1} + \alpha_j v_j$ for $j \le k$. Let $w = A v_k - \alpha_k u_k$. For $i \le k$,
$$\langle u_i, A v_k \rangle = \langle A^* u_i, v_k\rangle = \beta_i \langle v_{i-1}, v_k\rangle + \alpha_i\langle v_i, v_k\rangle,$$
which is $\alpha_k$ for $i = k$ and $0$ for $i < k$. So $\langle u_i, w\rangle = 0$ for all $i \le k$. The reorthogonalization subtracts the projections of $w$ on $u_1, \dots, u_k$, which are zero, so it leaves $w$ unchanged. Then $\beta_{k+1} = \|w\| > 0$, $u_{k+1} = w/\beta_{k+1}$ is a unit vector orthogonal to $u_1, \dots, u_k$, and $A v_k = \alpha_k u_k + \beta_{k+1} u_{k+1}$.

Now let $w' = A^* u_{k+1} - \beta_{k+1} v_k$. For $i \le k$,
$$\langle v_i, A^* u_{k+1}\rangle = \langle A v_i, u_{k+1}\rangle = \alpha_i \langle u_i, u_{k+1}\rangle + \beta_{i+1}\langle u_{i+1}, u_{k+1}\rangle,$$
which is $\beta_{k+1}$ for $i = k$ and $0$ for $i < k$. So $w'$ is orthogonal to $v_1, \dots, v_k$, the reorthogonalization again subtracts nothing, and $A^* u_{k+1} = \beta_{k+1} v_k + \alpha_{k+1} v_{k+1}$ with $v_{k+1}$ a unit vector orthogonal to the earlier $v$'s when $\alpha_{k+1} > 0$. This completes the induction.

The relations $A v_j = \alpha_j u_j + \beta_{j+1} u_{j+1}$, $j = 1, \dots, k$, are the columns of $A V_k = U_{k+1} B_k$, and $y = \beta_1 u_1 = \beta_1 U_{k+1} e_1$.

For the span, $v_1 \in \mathcal{K}_1$. If $v_1, \dots, v_j \in \mathcal{K}_j$, then $\alpha_{j+1} v_{j+1} = A^* u_{j+1} - \beta_{j+1} v_j$ and $\beta_{j+1} A^* u_{j+1} = A^* A v_j - \alpha_j A^* u_j = A^* A v_j - \alpha_j(\beta_j v_{j-1} + \alpha_j v_j)$, which lies in $\mathcal{K}_{j+1}$ because $A^* A \mathcal{K}_j \subseteq \mathcal{K}_{j+1}$. So $v_{j+1} \in \mathcal{K}_{j+1}$. The $k$ orthonormal vectors $v_1, \dots, v_k$ lie in $\mathcal{K}_k$, whose dimension is at most $k$, so they are a basis of it. $\square$

**Lemma 2 (projection).** Under the assumption of Lemma 1, for every $z \in \mathbb{R}^k$ and $x = V_k z$,
$$\|A x - y\| = \|B_k z - \beta_1 e_1\|, \qquad \|x\| = \|z\| .$$
Hence for $\lambda \ge 0$, $x = V_k z$ minimizes $\|A x - y\|^2 + \lambda\|x\|^2$ over $\mathcal{K}_k$ if and only if $z$ minimizes $\|B_k z - \beta_1 e_1\|^2 + \lambda\|z\|^2$ over $\mathbb{R}^k$.

*Proof.* By Lemma 1, $A x - y = A V_k z - \beta_1 U_{k+1} e_1 = U_{k+1}(B_k z - \beta_1 e_1)$, and $U_{k+1}$ has orthonormal columns, so it preserves norms. Also $\|V_k z\| = \|z\|$ because $V_k$ has orthonormal columns. Since $z \mapsto V_k z$ is a bijection of $\mathbb{R}^k$ onto $\mathcal{K}_k$ (Lemma 1), the two minimization problems correspond. $\square$

**Lemma 3 (the small problem in closed form).** Let $B_k = P \Sigma Q^T$ be a thin SVD, with $P$ of size $(k+1) \times k$ and orthonormal columns $p_i$, $Q$ orthogonal with columns $q_i$, and $\Sigma = \mathrm{diag}(s_1, \dots, s_k)$. Put $g_i = \beta_1 \langle p_i, e_1\rangle$. Under the assumption of Lemma 1, all $s_i > 0$, and for $\lambda \ge 0$ the unique minimizer of $\|B_k z - \beta_1 e_1\|^2 + \lambda\|z\|^2$ is
$$z(\lambda) = \sum_{i=1}^k \frac{s_i g_i}{s_i^2 + \lambda} q_i, \qquad \text{with} \qquad \|B_k z(\lambda) - \beta_1 e_1\|^2 = \sum_{i=1}^k \Big(\frac{\lambda g_i}{s_i^2 + \lambda}\Big)^2 + \Big(\beta_1^2 - \sum_{i=1}^k g_i^2\Big).$$
These are the formulas of `Projected.z` and `Projected.res2` (lines L5 and L7).

*Proof.* $B_k$ is lower bidiagonal with nonzero diagonal $\alpha_1, \dots, \alpha_k$, so its top $k \times k$ block is nonsingular and $B_k$ has full column rank; hence all $s_i > 0$. The functional is strictly convex in $z$ and its gradient vanishes exactly when $(B_k^T B_k + \lambda I) z = B_k^T \beta_1 e_1$. In the coordinates $z = \sum_i c_i q_i$ this reads $(s_i^2 + \lambda) c_i = s_i g_i$, which gives $z(\lambda)$. For the residual, write $\beta_1 e_1 = \sum_i g_i p_i + r_\perp$ with $r_\perp$ orthogonal to all $p_i$, so $\|r_\perp\|^2 = \beta_1^2 - \sum_i g_i^2$. Then $B_k z(\lambda) = \sum_i \frac{s_i^2 g_i}{s_i^2 + \lambda} p_i$ and
$$B_k z(\lambda) - \beta_1 e_1 = -\sum_i \frac{\lambda g_i}{s_i^2 + \lambda} p_i - r_\perp,$$
whose squared norm is the stated sum, by Pythagoras. $\square$

**Theorem 1 (what line L8 returns).** Under the assumption of Lemma 1, for the $\lambda_k$ chosen at line L6, the vector $x_k = V_k z(\lambda_k)$ of line L8 is the unique minimizer of $\|A x - y\|^2 + \lambda_k\|x\|^2$ over $\mathcal{K}_k$, and $\|A x_k - y\|$ equals the projected residual of Lemma 3. For $\lambda_k = 0$ it is the iterate of LSQR and CGLS, the minimizer of $\|A x - y\|$ over $\mathcal{K}_k$.

*Proof.* Lemmas 2 and 3. $\square$

**Theorem 2 (invariant Krylov space).** Suppose that the loop stops at step $k$ because $\alpha_{k+1} = 0$ or $\beta_{k+1} = 0$ (in the second case, the relations of Lemma 1 hold with $u_{k+1}$ omitted). Then $A^* A \mathcal{K}_k \subseteq \mathcal{K}_k$, and for $\lambda > 0$, $x_k$ is the Tikhonov solution $x_\lambda = (A^* A + \lambda I)^{-1} A^* y$ of the full problem. For a matrix, this happens at some $k \le \mathrm{rank}(A)$.

*Proof.* By Lemma 1, $A^* A v_j \in \mathcal{K}_{j+1} \subseteq \mathcal{K}_k$ for $j < k$. For $j = k$: if $\beta_{k+1} = 0$, then $A v_k = \alpha_k u_k$ and $A^* A v_k = \alpha_k(\beta_k v_{k-1} + \alpha_k v_k) \in \mathcal{K}_k$. If $\alpha_{k+1} = 0$, then $A^* u_{k+1} = \beta_{k+1} v_k$ and $A^* A v_k = \alpha_k A^* u_k + \beta_{k+1} A^* u_{k+1} = \alpha_k(\beta_k v_{k-1} + \alpha_k v_k) + \beta_{k+1}^2 v_k \in \mathcal{K}_k$. So $\mathcal{K}_k$ is invariant under $A^* A$. For $\lambda > 0$ the map $A^* A + \lambda I$ is injective on the finite-dimensional invariant space $\mathcal{K}_k$, hence maps it onto itself, and since $A^* y \in \mathcal{K}_k$, also $x_\lambda = (A^* A + \lambda I)^{-1} A^* y \in \mathcal{K}_k$. The minimizer over the whole space lies in $\mathcal{K}_k$, so it is the minimizer over $\mathcal{K}_k$, which is $x_k$ by Theorem 1. For a matrix, $\mathcal{K}_k \subseteq R(A^*)$, whose dimension is $\mathrm{rank}(A)$; by Lemma 1 $\dim \mathcal{K}_k = k$ as long as there is no breakdown, so a breakdown occurs at some $k \le \mathrm{rank}(A)$. $\square$

**Theorem 3 (the discrepancy rule).** Let $\phi(\lambda) = \|B_k z(\lambda) - \beta_1 e_1\|^2$ and $T = (\tau\delta)^2$. Then $\phi$ is continuous and nondecreasing on $[0, \infty)$ with $\phi(\lambda) \to \beta_1^2 = \|y\|^2$ as $\lambda \to \infty$. If $\phi(0) < T < \|y\|^2$, there is a $\lambda^* > 0$ with $\phi(\lambda^*) = T$, and it is unique if some $g_i \ne 0$. The function `choose_dp` returns $0$ when $\phi(0) \ge T$; otherwise, if $\phi(\lambda_{lo}) < T \le \phi(\lambda_{hi})$ at the two ends of its search interval, every bisection step keeps this property, so after $j$ steps the returned $\lambda$ is within a factor $e^{(\log\lambda_{hi} - \log\lambda_{lo})/2^{j+1}}$ of a solution of $\phi(\lambda) = T$.

*Proof.* By Lemma 3, $\phi(\lambda) = \sum_i g_i^2 (\lambda/(s_i^2 + \lambda))^2 + \|r_\perp\|^2$. Each map $\lambda \mapsto \lambda/(s_i^2 + \lambda)$ is continuous and increasing from $0$ to $1$ because $s_i > 0$, so $\phi$ is continuous, nondecreasing, strictly increasing if some $g_i \ne 0$, and tends to $\sum_i g_i^2 + \|r_\perp\|^2 = \beta_1^2$. The intermediate value theorem gives $\lambda^*$. The bisection replaces the lower end by the midpoint when $\phi(\text{mid}) < T$ and the upper end otherwise, which keeps $\phi(\lambda_{lo}) < T \le \phi(\lambda_{hi})$; by continuity and monotonicity a solution lies in $[\lambda_{lo}, \lambda_{hi}]$, and the length of $[\log\lambda_{lo}, \log\lambda_{hi}]$ halves at each step. $\square$

**Theorem 4 (termination).** `hybrid_lsqr` returns after at most $K$ passes of the loop at line L2. Each pass does a finite amount of work: two operator products, two reorthogonalizations against at most $K + 1$ vectors, one SVD of a $(K + 1) \times K$ matrix, and at most $200$ bisection steps or $81$ grid points plus $60$ golden section steps, each costing $O(k)$.

*Proof.* The loop is a counted loop over $k = 1, \dots, K$ with an early exit on breakdown, and the parameter searches are counted loops. $\square$

**What is not proved here.** The behavior in floating point without reorthogonalization, and rates as $\delta \to 0$ for the hybrid method before the Krylov space becomes invariant. After that point the method is Tikhonov regularization with the chosen rule.
