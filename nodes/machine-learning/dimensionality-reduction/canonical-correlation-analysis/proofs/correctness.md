---
title: The canonical correlations are the singular values of the whitened cross-covariance
proves: [correctness]
status: full
---

We use the pseudocode and notation of the page. After line L3, $C_{XX}$ ($p \times p$) and $C_{YY}$ ($q \times q$) are symmetric positive definite, $R_X = C_{XX}^{-1/2}$ and $R_Y = C_{YY}^{-1/2}$ are their symmetric inverse square roots, $T = R_X C_{XY} R_Y$, and $m = \min(p, q)$. For weight vectors $a \in \mathbb{R}^p$ and $b \in \mathbb{R}^q$, the correlation of the two scores is
$$ \rho(a, b) = \frac{a^{\top} C_{XY} b}{\sqrt{a^{\top} C_{XX} a}\, \sqrt{b^{\top} C_{YY} b}} . $$
With $\kappa_X = \kappa_Y = 0$ this is the sample correlation of $a^{\top} x$ and $b^{\top} y$; with ridge terms it is the regularized criterion.

**Lemma 1 (SVD from the eigenvectors of $T T^{\top}$).** Assume $p \le q$. Let $T T^{\top} = \sum_{k \le p} \sigma_k^2 u_k u_k^{\top}$ with orthonormal $u_k$ and $\sigma_1 \ge \cdots \ge \sigma_p \ge 0$, and for $\sigma_k > 0$ let $v_k = T^{\top} u_k / \sigma_k$. Then the $v_k$ are orthonormal, $T v_k = \sigma_k u_k$ and $T^{\top} u_k = \sigma_k v_k$. If $\sigma_k = 0$ then $T^{\top} u_k = 0$.

*Proof.* $v_i^{\top} v_j = u_i^{\top} T T^{\top} u_j / (\sigma_i \sigma_j) = \sigma_j^2 [i = j] / (\sigma_i \sigma_j) = [i = j]$. $T v_k = T T^{\top} u_k / \sigma_k = \sigma_k u_k$. $T^{\top} u_k = \sigma_k v_k$ by the definition. If $\sigma_k = 0$ then $\lVert T^{\top} u_k \rVert^2 = u_k^{\top} T T^{\top} u_k = 0$. $\square$

The implementation uses this lemma on $T$ when $p \le q$ and on $T^{\top}$ when $p > q$, so lines L6 and L7 give a thin SVD $T = \sum_{k} \sigma_k u_k v_k^{\top}$ over the positive $\sigma_k$.

**Lemma 2 (change of variables).** For $a \ne 0$ and $b \ne 0$ put $u = C_{XX}^{1/2} a$ and $v = C_{YY}^{1/2} b$. Then $\rho(a, b) = u^{\top} T v / (\lVert u \rVert \lVert v \rVert)$, and $a^{\top} C_{XX} a_s = u^{\top} u_s'$ where $u_s' = C_{XX}^{1/2} a_s$.

*Proof.* $a = R_X u$ and $b = R_Y v$, so $a^{\top} C_{XY} b = u^{\top} R_X C_{XY} R_Y v = u^{\top} T v$, $a^{\top} C_{XX} a = u^{\top} R_X C_{XX} R_X u = u^{\top} u$, and the same for $b$. The last identity is $a^{\top} C_{XX} a_s = u^{\top} R_X C_{XX} R_X u_s' = u^{\top} u_s'$. $\square$

**Theorem.** Let $\sigma_1 \ge \sigma_2 \ge \cdots$ be the singular values of $T$ with singular vectors $u_t, v_t$, and $a_t = R_X u_t$, $b_t = R_Y v_t$ as in line L7.

1. $\max_{a \ne 0,\, b \ne 0} \rho(a, b) = \sigma_1$, attained at $(a_1, b_1)$.
2. For each $t \le m$, $\sigma_t = \max \{ \rho(a, b) : a^{\top} C_{XX} a_s = 0 \text{ for all } s < t \}$, attained at $(a_t, b_t)$.
3. $a_i^{\top} C_{XX} a_j = [i = j]$, $b_i^{\top} C_{YY} b_j = [i = j]$, and $a_i^{\top} C_{XY} b_j = \sigma_i [i = j]$. So the canonical variates are uncorrelated within each view and across the views, except in matched pairs.
4. $0 \le \sigma_t \le 1$ when $\kappa_X = \kappa_Y = 0$.

*Proof.* By Lemma 2 we may work with unit vectors $u$ and $v$ and the bilinear form $u^{\top} T v$. Extend $\{u_k\}$ and $\{v_k\}$ to orthonormal bases, with $\sigma_k = 0$ for the added vectors, so $T = \sum_k \sigma_k u_k v_k^{\top}$. Write $\alpha_k = u^{\top} u_k$ and $\beta_k = v_k^{\top} v$. Then
$$ u^{\top} T v = \sum_k \sigma_k \alpha_k \beta_k \le \sum_k \sigma_k |\alpha_k| |\beta_k| . $$

(1) and (2). Under the constraints of (2), Lemma 2 gives $\alpha_s = 0$ for $s < t$. So every term with a nonzero $\alpha_k$ has $k \ge t$ and $\sigma_k \le \sigma_t$, and by the Cauchy-Schwarz inequality and $\sum \alpha_k^2 = \sum \beta_k^2 = 1$,
$$ u^{\top} T v \le \sigma_t \sum_k |\alpha_k| |\beta_k| \le \sigma_t . $$
The pair $u = u_t$, $v = v_t$ meets the constraints and gives $u_t^{\top} T v_t = \sigma_t$. Part (1) is the case $t = 1$ with no constraint.

(3) $a_i^{\top} C_{XX} a_j = u_i^{\top} R_X C_{XX} R_X u_j = u_i^{\top} u_j$, the same for $b$, and $a_i^{\top} C_{XY} b_j = u_i^{\top} T v_j = \sigma_j u_i^{\top} u_j = \sigma_i [i = j]$ by Lemma 1.

(4) $\sigma_t = \rho(a_t, b_t) \ge 0$ by construction. With no ridge terms, $\rho(a, b)$ is a sample correlation, and $|a^{\top} C_{XY} b| = \frac1n |\langle X a, Y b \rangle| \le \frac1n \lVert X a \rVert \lVert Y b \rVert = \sqrt{a^{\top} C_{XX} a}\sqrt{b^{\top} C_{YY} b}$ by the Cauchy-Schwarz inequality in $\mathbb{R}^n$ (with centred $X$ and $Y$). So $\sigma_t \le 1$. $\square$

**Corollary (principal angles).** With no ridge terms, let $Q_X$ ($n \times p$) and $Q_Y$ ($n \times q$) have orthonormal columns that span the column spaces of the centred $X$ and $Y$ (full column rank). Then the canonical correlations are the singular values of $Q_X^{\top} Q_Y$, the cosines of the principal angles between the two column spaces.

*Proof.* Write $X = Q_X G$ and $Y = Q_Y H$ with invertible $G$ and $H$. Then $\rho(a, b) = (G a)^{\top} Q_X^{\top} Q_Y (H b) / (\lVert G a \rVert \lVert H b \rVert)$, and $a \mapsto G a$, $b \mapsto H b$ are bijections. The proof of the theorem, applied to $Q_X^{\top} Q_Y$ in place of $T$, gives the claim. $\square$

So $\rho_1 = 1$ exactly when the two column spaces share a nonzero vector. The centred columns lie in a space of dimension $n - 1$; if $p + q > n - 1$, the two spaces meet in a subspace of dimension at least $p + q - (n - 1)$, and that many canonical correlations equal 1 whatever the data are.

**Cost.** Line L2 takes $\Theta(n (p + q)^2)$ operations. Line L4 takes $\Theta(p^3 + q^3)$ with a symmetric eigensolver. Line L5 takes $\Theta(p q (p + q))$ and line L6 takes $\Theta(p q \min(p, q))$. The extra memory is $\Theta((p + q)^2)$.
