---
title: DEIM picks distinct indices with an invertible P^T U, and its error is at most the norm of (P^T U)^-1 times the POD projection error
proves: [correctness]
status: full
---

We assume exact arithmetic. $U_l = [u_1, \ldots, u_l]$ and $P_l = [e_{p_1}, \ldots, e_{p_l}]$ are the matrices after step $l$, the columns $u_1, \ldots, u_m$ of length $n$ are linearly independent, and $r_l$ is the residual of step $l$, with $r_1 = u_1$.

**Lemma 1 (the selection is well defined).** For each $l \le m$: $P_{l-1}^T U_{l-1}$ is invertible, $r_l \ne 0$, $r_l(p_i) = 0$ for $i < l$, $r_l(p_l) \ne 0$, and $p_l$ differs from $p_1, \ldots, p_{l-1}$. Moreover $P_l^T U_l = L_l T_l$, where $L_l$ is lower triangular with the diagonal $r_1(p_1), \ldots, r_l(p_l)$ and $T_l$ is upper triangular with a unit diagonal. So $P_l^T U_l$ is invertible.

*Proof.* By induction on $l$. For $l = 1$, $u_1 \ne 0$ by independence, so its largest entry in absolute value is not 0, and $P_1^T U_1 = (u_1(p_1))$. Let $l \ge 2$ and assume the claim for $l - 1$. Then line L3 has a unique solution $c$. The residual $r_l = u_l - U_{l-1} c$ is not 0, since $u_l$ is not in the range of $U_{l-1}$. Its entries at the old indices are $P_{l-1}^T r_l = P_{l-1}^T u_l - (P_{l-1}^T U_{l-1}) c = 0$. Line L5 picks $p_l$ with $|r_l(p_l)| = \max_i |r_l(i)| > 0$, so $p_l$ is not an old index. Let $R_l = [r_1, \ldots, r_l]$. Each $u_j = r_j + U_{j-1} c^{(j)}$, and by induction each column of $U_{j-1}$ is a combination of $r_1, \ldots, r_{j-1}$, so $U_l = R_l T_l$ with $T_l$ upper triangular with a unit diagonal. The entry $(i, j)$ of $P_l^T R_l$ is $r_j(p_i)$, which is 0 for $i < j$ and $r_j(p_j) \ne 0$ for $i = j$. So $L_l = P_l^T R_l$ is lower triangular with a nonzero diagonal, and $P_l^T U_l = L_l T_l$ has the determinant $\prod_j r_j(p_j) \ne 0$. $\square$

Write $U = U_m$, $P = P_m$, $M = P^T U$ and $\mathbb{P} = U M^{-1} P^T$.

**Lemma 2 (interpolation and reproduction).** $\hat{f} = \mathbb{P} f$ is the unique vector in the range of $U$ with $P^T \hat{f} = P^T f$. In particular $\mathbb{P} U = U$, and $\hat{f} = f$ if $f$ is in the range of $U$.

*Proof.* $P^T \mathbb{P} f = M M^{-1} P^T f = P^T f$. If $U a$ and $U b$ both agree with $f$ at the indices, then $M (a - b) = 0$, so $a = b$. For $f = U a$, $\mathbb{P} U a = U M^{-1} M a = U a$. $\square$

**Theorem (error bound).** If the columns of $U$ are orthonormal, then for every $f \in \mathbb{R}^n$

$$\|f - \hat{f}\|_2 \le \|M^{-1}\|_2\, \|(I - U U^T) f\|_2 .$$

*Proof.* If $m = n$, then $U U^T = I$ and $\hat{f} = f$ by Lemma 2, and both sides are 0. Let $m < n$, and complete $U$ to an orthogonal matrix $[U, U_\perp]$ with $U_\perp \in \mathbb{R}^{n \times (n-m)}$. Let $w = (I - U U^T) f = U_\perp t$ with $t = U_\perp^T f$, so $\|w\|_2 = \|t\|_2$. Since $\mathbb{P} U = U$ (Lemma 2), $(I - \mathbb{P})(U U^T f) = 0$, so

$$f - \hat{f} = (I - \mathbb{P}) f = (I - \mathbb{P}) w = U_\perp t - U z, \qquad z = M^{-1} P^T U_\perp t = M^{-1} N t ,$$

with $N = P^T U_\perp \in \mathbb{R}^{m \times (n-m)}$. The two parts are orthogonal, so $\|f - \hat{f}\|_2^2 = \|t\|_2^2 + \|z\|_2^2$.

The matrix $P^T [U, U_\perp] = [M, N]$ has orthonormal rows, because $P^T P = I$ and $[U, U_\perp]$ is orthogonal. So $M M^T + N N^T = I$. Since $M$ is invertible (Lemma 1), $M M^T$ is positive definite, so every eigenvalue of $N N^T$ is below 1, and so is every eigenvalue of $N^T N$, because the two matrices have the same nonzero eigenvalues. Let $\beta = \|N\|_2^2 < 1$. Then $I - N^T N$ is invertible, and the identity $(I - N^T N) N^T = N^T (I - N N^T)$ gives $N^T (I - N N^T)^{-1} = (I - N^T N)^{-1} N^T$. So

$$\|z\|_2^2 = t^T N^T (M M^T)^{-1} N t = t^T N^T (I - N N^T)^{-1} N t = t^T \big((I - N^T N)^{-1} N^T N\big) t = t^T \big((I - N^T N)^{-1} - I\big) t .$$

Hence $\|f - \hat{f}\|_2^2 = t^T (I - N^T N)^{-1} t \le \|t\|_2^2 / (1 - \beta)$, since the eigenvalues of $I - N^T N$ are at least $1 - \beta$. On the other side, $\|M^{-1}\|_2^2 = 1 / \lambda_{\min}(M M^T) = 1 / \lambda_{\min}(I - N N^T) = 1/(1 - \beta)$. So $\|f - \hat{f}\|_2^2 \le \|M^{-1}\|_2^2 \|w\|_2^2$. $\blacksquare$

The bound is attained: with $t$ an eigenvector of $N^T N$ for the eigenvalue $\beta$, the inequality in the last step is an equality, so the factor $\|M^{-1}\|_2$ cannot be lowered for the given indices. The bounds $\|M^{-1}\|_2 \le (1 + \sqrt{2n})^{m-1} / \|u_1\|_\infty$ of Chaturantabut and Sorensen and $\|M^{-1}\|_2 < \sqrt{nm/3}\, 2^m$ of Sorensen and Embree are cited, not proved here, and the tests check both on random bases.
