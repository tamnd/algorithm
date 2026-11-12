---
title: The inexact ALM steps are exact proximal steps, and its limits solve principal component pursuit
proves: [correctness]
status: full
---

**Setup.** $M$ is an $n_1 \times n_2$ matrix and $\lambda > 0$. Principal component pursuit (PCP) is

$$\min_{L, S}\; \|L\|_* + \lambda \|S\|_1 \quad \text{subject to} \quad L + S = M,$$

where $\|L\|_*$ is the sum of the singular values and $\|S\|_1 = \sum_{ij} |S_{ij}|$. The augmented Lagrangian is $\mathcal{L}(L, S, Y, \mu) = \|L\|_* + \lambda\|S\|_1 + \langle Y, M - L - S\rangle + \frac{\mu}{2}\|M - L - S\|_F^2$. One iteration of the method maps $(S_k, Y_k, \mu_k)$ to $L_{k+1}$ (L3), $S_{k+1}$ (L4), $Y_{k+1} = Y_k + \mu_k (M - L_{k+1} - S_{k+1})$ (L5) and $\mu_{k+1} = \min(\rho\mu_k, \bar\mu)$ (L6).

**Lemma 1 (soft thresholding).** For a matrix $W$ and $\tau > 0$, the unique minimizer of $\tau\|S\|_1 + \frac12\|S - W\|_F^2$ is $\operatorname{shrink}_\tau(W)$, with entries $\operatorname{sign}(W_{ij}) \max(|W_{ij}| - \tau, 0)$.

*Proof.* The function is a sum of the strictly convex one-variable functions $\tau|s| + \frac12(s - w)^2$, one per entry. For $s > 0$ the derivative is $\tau + s - w$, zero at $s = w - \tau$, which is positive only if $w > \tau$; for $s < 0$ the same gives $s = w + \tau$ if $w < -\tau$; otherwise $0 \in [-\tau, \tau] - w$ means that $s = 0$ is optimal. $\square$

**Lemma 2 (singular value thresholding).** Let $W = U \operatorname{diag}(\sigma) V^T$ be an SVD. The unique minimizer of $\tau \|L\|_* + \frac12 \|L - W\|_F^2$ is $\operatorname{svt}_\tau(W) = U \operatorname{diag}(\max(\sigma - \tau, 0)) V^T$.

*Proof.* The function is strictly convex, so the minimizer is unique. For any $L$ with singular values $\ell_1 \ge \ell_2 \ge \cdots$, von Neumann's trace inequality gives $\langle L, W \rangle \le \sum_i \ell_i \sigma_i$. So $\frac12\|L - W\|_F^2 = \frac12 \sum_i \ell_i^2 - \langle L, W \rangle + \frac12 \sum_i \sigma_i^2 \ge \frac12 \sum_i (\ell_i - \sigma_i)^2$, and the objective is at least $\sum_i \big(\tau \ell_i + \frac12(\ell_i - \sigma_i)^2\big)$. Each term is smallest at $\ell_i = \max(\sigma_i - \tau, 0)$, by Lemma 1 for one entry with $\ell_i \ge 0$. The matrix $\operatorname{svt}_\tau(W)$ has these singular values and the same singular vectors as $W$, so it attains equality in von Neumann's inequality and reaches the lower bound. $\square$

**Lemma 3 (the steps).** L3 and L4 are exact minimizations: $L_{k+1} = \arg\min_L \mathcal{L}(L, S_k, Y_k, \mu_k)$ and $S_{k+1} = \arg\min_S \mathcal{L}(L_{k+1}, S, Y_k, \mu_k)$. Moreover, $Y_{k+1} \in \lambda\, \partial\|S_{k+1}\|_1$ and $\hat Y_{k+1} := Y_k + \mu_k (M - L_{k+1} - S_k) \in \partial \|L_{k+1}\|_*$.

*Proof.* Completing the square, $\langle Y, M - L - S\rangle + \frac{\mu}{2}\|M - L - S\|_F^2 = \frac{\mu}{2}\|L - (M - S + Y/\mu)\|_F^2 - \frac{1}{2\mu}\|Y\|_F^2$. Divided by $\mu$, minimizing over $L$ is the problem of Lemma 2 with $\tau = 1/\mu$ and $W = M - S_k + Y_k/\mu_k$, which is L3. In the same way, minimizing over $S$ is Lemma 1 with $\tau = \lambda/\mu$ and $W' = M - L_{k+1} + Y_k/\mu_k$, which is L4.

For the multipliers: $Y_{k+1} = \mu_k (W' - S_{k+1}) = \mu_k(W' - \operatorname{shrink}_{\lambda/\mu_k}(W'))$, so each entry is $\mu_k W'_{ij}$ clipped to $[-\lambda, \lambda]$. Hence $|(Y_{k+1})_{ij}| \le \lambda$, and $(Y_{k+1})_{ij} = \lambda \operatorname{sign}((S_{k+1})_{ij})$ where $(S_{k+1})_{ij} \ne 0$. This is the condition $Y_{k+1} \in \lambda\,\partial\|S_{k+1}\|_1$. For $L$, the optimality condition of the minimization in L3 is $0 \in \partial\|L_{k+1}\|_* + \mu_k (L_{k+1} - W)$, that is $\mu_k (W - L_{k+1}) = \hat Y_{k+1} \in \partial\|L_{k+1}\|_*$. $\square$

**Lemma 4 (certificate).** If $L + S = M$ and a matrix $Y$ satisfies $Y \in \partial\|L\|_*$ and $Y \in \lambda\,\partial\|S\|_1$, then $(L, S)$ is optimal for PCP.

*Proof.* For any feasible $(L', S')$, the subgradient inequalities give $\|L'\|_* \ge \|L\|_* + \langle Y, L' - L\rangle$ and $\lambda\|S'\|_1 \ge \lambda\|S\|_1 + \langle Y, S' - S\rangle$. Add them: the inner products sum to $\langle Y, (L' + S') - (L + S)\rangle = \langle Y, M - M \rangle = 0$. $\square$

**Theorem.** Suppose $0 < \mu_0 \le \mu_k \le \bar\mu$ for all $k$ (true for L6 with the cap $\bar\mu$), and the iterates $(L_k, S_k, Y_k)$ converge to $(L^\star, S^\star, Y^\star)$. Then $L^\star + S^\star = M$ and $(L^\star, S^\star)$ is an optimal solution of PCP. In particular the stopping test of L7 is met after finitely many iterations.

*Proof.* From L5, $M - L_{k+1} - S_{k+1} = (Y_{k+1} - Y_k)/\mu_k$, whose norm is at most $\|Y_{k+1} - Y_k\|_F / \mu_0 \to 0$. So $L^\star + S^\star = M$, and the residual of L7 tends to 0. Next, $\hat Y_{k+1} - Y_{k+1} = \mu_k (S_{k+1} - S_k)$, whose norm is at most $\bar\mu \|S_{k+1} - S_k\|_F \to 0$, so $\hat Y_{k+1} \to Y^\star$ as well. The graph of the subdifferential of a convex function that is finite everywhere is closed: if $G_k \in \partial f(X_k)$, $X_k \to X$ and $G_k \to G$, then passing to the limit in $f(Z) \ge f(X_k) + \langle G_k, Z - X_k\rangle$, by the continuity of $f$, gives $G \in \partial f(X)$. With Lemma 3 this gives $Y^\star \in \partial\|L^\star\|_*$ and $Y^\star \in \lambda\,\partial\|S^\star\|_1$, and Lemma 4 shows that $(L^\star, S^\star)$ is optimal. $\blacksquare$

**Remark (convergence).** That the iterates do converge is Theorem 2 of Lin, Chen and Ma (2010): it holds when $\mu_k$ is nondecreasing and $\sum_k 1/\mu_k = \infty$, which the cap $\bar\mu$ guarantees. Their Theorem 3 shows that without this condition (for example $\mu_{k+1} = \rho\mu_k$ with no cap) the limit may fail to be optimal. That the optimal solution equals the planted pair $(L_0, S_0)$ is the separate recovery theorem of Candès, Li, Ma and Wright (2011), under incoherence and a random support.
