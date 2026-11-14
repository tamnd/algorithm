---
title: The QR form of the cluster-robust covariance equals the sandwich formula, the cluster scores sum to zero, and the wild cluster bootstrap statistic is even in the signs
proves: [correctness, termination]
status: full
---

The arithmetic is exact. $X$ is a fixed real $n \times p$ matrix of rank $p < n$ with rows $x_i^\top$, the rows are split into $G \ge 2$ clusters, $X_g$ and $e_g$ are the rows of cluster $g$, $\hat b = (X^\top X)^{-1}X^\top y$, $e = y - X\hat b$ and $H = X(X^\top X)^{-1}X^\top$. The cluster score is $s_g = X_g^\top e_g = \sum_{i \in g}x_ie_i$, and the target is

$$\widehat V = a\,(X^\top X)^{-1}\Bigl(\sum_{g=1}^Gs_gs_g^\top\Bigr)(X^\top X)^{-1}, \qquad a = 1 \text{ (CR0)}, \quad a = \frac{G}{G - 1}\cdot\frac{n - 1}{n - p} \text{ (CR1)}.$$

**Lemma 1 (lines L1 to L6 compute the sandwich).** With $X^\top X = R^\top R$ from line L1 and $u_g = R^{-\top}s_g$ from line L4, $aR^{-1}\bigl(\sum_gu_gu_g^\top\bigr)R^{-\top} = \widehat V$.

*Proof.* Line L1 gives an upper triangular nonsingular $R$ with $X = Q_1R$ and $Q_1^\top Q_1 = I$, so $X^\top X = R^\top R$, and line L2 gives $\hat b$ (Lemma 1 of the proof on the [weighted least squares](/weighted-least-squares/) page, with unit weights). Then $\sum_gu_gu_g^\top = R^{-\top}\bigl(\sum_gs_gs_g^\top\bigr)R^{-1}$, and $R^{-1}R^{-\top} = (R^\top R)^{-1} = (X^\top X)^{-1}$ on each side. $\square$

**Lemma 2 (singletons and rank).** (a) If every cluster has one row, CR0 is HC0 and CR1 is HC1. (b) $\sum_gs_g = 0$, so the middle matrix $\sum_gs_gs_g^\top$ has rank at most $\min(p, G - 1)$, and with $G = 1$ it is the zero matrix.

*Proof.* (a) With one row per cluster, $s_i = x_ie_i$ and $s_is_i^\top = e_i^2x_ix_i^\top$, which is the HC0 middle matrix; with $G = n$ the factor of CR1 is $\frac{n}{n - 1}\cdot\frac{n - 1}{n - p} = \frac{n}{n - p}$, the factor of HC1. (b) $\sum_gs_g = X^\top e = X^\top(I - H)y = 0$, the normal equations. So the $G$ vectors $s_g$ lie in a space of dimension at most $G - 1$, and the middle matrix is a sum of outer products of vectors in that space. $\square$

So with $G$ clusters a Wald test of more than $G - 1$ linear restrictions has a singular covariance, and the estimate of any single variance comes from at most $G - 1$ independent pieces of information. This is why the page uses $t_{G-1}$ and why few clusters are a problem.

**Lemma 3 (expected value).** If $\mathrm E[\varepsilon] = 0$ and $\operatorname{Cov}(\varepsilon) = \Sigma$ with any block structure, then

$$\mathrm E\Bigl[\sum_gs_gs_g^\top\Bigr] = \sum_gX_g^\top\bigl[(I - H)\Sigma(I - H)\bigr]_{gg}X_g,$$

where $[\cdot]_{gg}$ is the diagonal block of cluster $g$, while the true covariance is $\operatorname{Cov}(\hat b) = (X^\top X)^{-1}X^\top\Sigma X(X^\top X)^{-1}$.

*Proof.* $e = (I - H)\varepsilon$, so $e_g$ is the $g$ block of $(I - H)\varepsilon$ and $\mathrm E[e_ge_g^\top] = [(I - H)\Sigma(I - H)]_{gg}$. Then $\mathrm E[s_gs_g^\top] = X_g^\top\mathrm E[e_ge_g^\top]X_g$. $\square$

If $\Sigma$ is block diagonal by cluster, $X^\top\Sigma X = \sum_gX_g^\top\Sigma_{gg}X_g$, and the two differ only by the replacement of $\Sigma$ by $(I - H)\Sigma(I - H)$. When some clusters carry a large share of the leverage this shrinks the middle matrix, so CR0 is biased down; the factor of CR1 is a rough correction, not an exact one.

**Lemma 4 (the wild cluster bootstrap statistic is even in the signs).** In the bootstrap with the null $b_j = \beta_0$ imposed, let $\tilde y$ be the restricted fit and $\tilde e = y - \tilde y$, and for a sign vector $v \in \{-1, 1\}^G$ let $y^*(v) = \tilde y + D(v)\tilde e$, where $D(v)$ multiplies the rows of cluster $g$ by $v_g$. Then $|t^*(v)| = |t^*(-v)|$, so $|t^*|$ takes at most $2^{G-1}$ distinct values.

*Proof.* $\tilde y = X\tilde b$ for a vector $\tilde b$ with $\tilde b_j = \beta_0$, so $\hat b^*(v) - \tilde b = (X^\top X)^{-1}X^\top D(v)\tilde e$, which is linear in $v$ and changes sign with $v$. The residuals $e^*(v) = (I - H)D(v)\tilde e$ change sign too, so each $s_g^*$ changes sign and $\sum_gs_g^*s_g^{*\top}$ does not change. Hence $\hat b_j^* - \beta_0$ changes sign and $\mathrm{se}_j^*$ is unchanged. $\square$

With $G = 6$ the bootstrap p-value can take at most 32 values, so it cannot go below about $1/32$; this is a property of the Rademacher weights, not of the data.

**What is cited, not proved.** As $G \to \infty$ with independent clusters, bounded cluster sizes or sizes that do not dominate, and moment and design conditions, $G\widehat V$ is consistent for the limit of $G\operatorname{Cov}(\hat b)$ for any within-cluster correlation, and the t statistics are asymptotically standard normal (Liang and Zeger 1986 for estimating equations, Arellano 1987 for fixed effects panel regressions). That the wild cluster bootstrap gives better small $G$ tests is a simulation finding (Cameron, Gelbach and Miller 2008), with asymptotic support but no exact guarantee. None of these is proved here, and the coverage and size figures on the page are measured.

**Termination.** Line L1 is $p$ Householder steps, line L2 one triangular solve, line L3 $n$ dot products, line L4 $n$ updates of size $p$ and $G$ triangular solves, and lines L5 to L7 finite sums: $\Theta(np^2)$ operations in total, since $G \le n$.
