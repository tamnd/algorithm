---
title: Tearing, deflation, the secular equation and Loewner's formula give the eigendecomposition
proves: [correctness, termination]
status: full
---

Notation of the page. $T$ is symmetric tridiagonal, $T = \operatorname{diag}(T_1, T_2) + \rho v v^T$ with $v = e_m + e_{m+1}$, and $T_i = Q_i D_i Q_i^T$. Exact arithmetic unless stated.

**Lemma 1 (tearing).** $T = \operatorname{diag}(T_1, T_2) + \rho v v^T$ and $T = Q (D + \rho z z^T) Q^T$ with $Q = \operatorname{diag}(Q_1, Q_2)$ and $z = Q^T v$.

*Proof.* $\rho v v^T$ has $\rho$ in positions $(m, m)$, $(m, m+1)$, $(m+1, m)$ and $(m+1, m+1)$. Adding it to $\operatorname{diag}(T_1, T_2)$ restores $a_m$ and $a_{m+1}$ and puts $b_m = \rho$ in the two off-diagonal positions. Then $Q^T T Q = D + \rho (Q^T v)(Q^T v)^T$. $z = Q^T v$ is $Q_1^T e_m$ stacked on $Q_2^T e_1$: the last row of $Q_1$ and the first row of $Q_2$. $\square$

**Lemma 2 (deflation).** (a) If $z_i = 0$, then $(D + \rho z z^T) e_i = d_i e_i$. (b) If $d_i = d_j$ with $i \ne j$, let $G$ be the rotation in the $(i, j)$ plane with $(G z)_j = 0$. Then $G D G^T = D$, so $G (D + \rho z z^T) G^T = D + \rho \hat z \hat z^T$ with $\hat z_j = 0$, and (a) applies. (c) In the inexact case of line L5, the dropped quantities are $\rho z_i$ or $c s (d_i - d_j)$, each at most the tolerance $\tau = 8u \max(\max |d|, \rho)$.

*Proof.* (a) $(D + \rho z z^T) e_i = d_i e_i + \rho z z_i = d_i e_i$. (b) In the $(i, j)$ plane $D$ is $d_i I$, which commutes with $G$. (c) For a small $z_i$, replacing $z_i$ by 0 changes the matrix by $\rho (z z^T - z' z'^T)$, whose norm is at most $2 \rho |z_i| \|z\| \le 2\tau$ for $\|z\| = 1$. For a rotation with $d_i \ne d_j$, $G D G^T$ differs from a diagonal matrix only by the off-diagonal entry $c s (d_j - d_i)$ in positions $(i, j)$ and $(j, i)$; dropping it is a symmetric perturbation of norm at most $\tau$. $\square$

**Lemma 3 (secular equation).** Let $d_1 < \dots < d_K$, every $z_j \ne 0$, and $\rho \ne 0$. Then (a) no $d_j$ is an eigenvalue of $M = D + \rho z z^T$; (b) $\lambda$ is an eigenvalue of $M$ exactly when $f(\lambda) = 1 + \rho \sum_j z_j^2 / (d_j - \lambda) = 0$, with eigenvector $(D - \lambda I)^{-1} z$; (c) for $\rho > 0$, $f$ has exactly one root in each interval $(d_i, d_{i+1})$ and one in $(d_K, d_K + \rho \|z\|_2^2]$.

*Proof.* (a) If $M x = d_j x$, row $j$ gives $\rho z_j (z^T x) = 0$, so $z^T x = 0$, and then $(D - d_j I) x = 0$ forces $x$ to be a multiple of $e_j$; but $z^T e_j = z_j \ne 0$, a contradiction. (b) For $\lambda$ not a pole, $M x = \lambda x$ means $(D - \lambda I) x = -\rho z (z^T x)$. If $z^T x = 0$, then $x = 0$; otherwise $x$ is a multiple of $(D - \lambda I)^{-1} z$, and taking the inner product with $z$ gives $z^T x = -\rho (z^T x) \sum_j z_j^2 / (d_j - \lambda)$, which is $f(\lambda) = 0$. Conversely, a root gives an eigenvector this way. (c) $f'(\lambda) = \rho \sum_j z_j^2 / (d_j - \lambda)^2 > 0$, so $f$ increases on each interval between poles. On $(d_i, d_{i+1})$ it goes from $-\infty$ to $+\infty$, so it has exactly one root there. On $(d_K, \infty)$ it goes from $-\infty$ to 1. At $\lambda = d_K + \rho \|z\|^2$ each term $\rho z_j^2 / (d_j - \lambda)$ is at least $-z_j^2 / \|z\|^2$, so $f(\lambda) \ge 0$. That gives $K$ roots for $K$ eigenvalues. $\square$

The case $\rho < 0$ reduces to $\rho > 0$ by $D + \rho z z^T = -((-D) + |\rho| z z^T)$, which is what the implementation does.

**Lemma 4 (Loewner's formula).** Let $d_1 < \dots < d_K$, $\rho > 0$, and let $\lambda_1, \dots, \lambda_K$ satisfy $d_i < \lambda_i < d_{i+1}$ for $i < K$ and $d_K < \lambda_K$. Then
$$\hat z_j^2 = \frac{\prod_{i} (\lambda_i - d_j)}{\rho \prod_{i \ne j} (d_i - d_j)}$$
is positive, and $D + \rho \hat z \hat z^T$ has the eigenvalues $\lambda_1, \dots, \lambda_K$.

*Proof.* Signs: $\lambda_i - d_j < 0$ for $i < j$ and $> 0$ for $i \ge j$, so the numerator has sign $(-1)^{j-1}$. In the denominator, $d_i - d_j < 0$ for $i < j$, also $j - 1$ factors, so $\hat z_j^2 > 0$. For any $\hat z$, $\det(D + \rho \hat z \hat z^T - \lambda I) = \prod_i (d_i - \lambda) \cdot \hat f(\lambda)$ by the matrix determinant lemma, where $\hat f$ is the secular function of $\hat z$. So the characteristic polynomial is $p(\lambda) = \prod_i (d_i - \lambda) + \rho \sum_j \hat z_j^2 \prod_{i \ne j} (d_i - \lambda)$. Put $q(\lambda) = \prod_i (\lambda_i - \lambda)$, monic up to the sign $(-1)^K$ like $p$. Both $p - q$ and the interpolation below have degree at most $K - 1$, and at $\lambda = d_j$, $p(d_j) = \rho \hat z_j^2 \prod_{i \ne j} (d_i - d_j) = \prod_i (\lambda_i - d_j) = q(d_j)$. So $p - q$ vanishes at $K$ distinct points and has degree at most $K - 1$; hence $p = q$. $\square$

**Theorem 1 (merge).** In exact arithmetic, with the deflation of Lemma 2 and the exact roots of Lemma 3, lines L6 to L9 give $\hat z = \pm z$ componentwise and orthonormal eigenvectors, and $Q [S, I_{\text{defl}}]$ is an orthogonal matrix of eigenvectors of $T$.

*Proof.* By Lemma 3 the exact roots strictly interlace, so Lemma 4 applies, and the polynomial identity of Lemma 4 for $z$ itself shows $z_j^2 = \hat z_j^2$. The vectors $s_i = (D - \lambda_i I)^{-1} \hat z$ are eigenvectors of the symmetric $D + \rho \hat z \hat z^T$ for distinct eigenvalues, so they are orthogonal; line L8 normalizes them. The deflated unit vectors $e_i$ are eigenvectors and are orthogonal to the others because the reduced problem lives on the complementary coordinates. Multiplying by the orthogonal $Q$ of Lemma 1 (and the deflation rotations) gives eigenvectors of $T$. $\square$

**Theorem 2 (correctness and termination).** DC-EIG returns the eigenvalues of $T$ and an orthogonal matrix of eigenvectors; it terminates.

*Proof.* Induction on $n$. For $n = 1$, line L1 is correct. For $n \ge 2$, $1 \le m < n$, so both halves are smaller, and the induction hypothesis gives their decompositions; Lemma 1 and Theorem 1 finish the merge. Each recursive call works on a strictly smaller matrix, so the recursion has depth $\lceil \log_2 n \rceil$. Each root search runs at most 200 steps, and each step either takes a model point inside the bracket or bisects it. $\square$

**Floating point (statements).** The computed roots satisfy $|f(\hat \lambda_i)| \le 8 K u (1 + \rho \sum_j |z_j^2 / (d_j - \hat \lambda_i)|)$, the stopping test, or the bracket has collapsed to rounding level. Gu and Eisenstat (1995, Section 3) show that, with the differences $d_j - \hat \lambda_i$ computed relative to the nearer pole, $\hat z$ from Lemma 4 is close to $z$ in a normwise sense, and the computed eigenvectors are orthogonal to $O(K u)$ and are exact for $D + \rho \hat z \hat z^T$ to working accuracy. With the deflation bound of Lemma 2(c), the whole method is backward stable: $T + E = \tilde Q \hat \Lambda \tilde Q^T$ for an exactly orthogonal $\tilde Q$ with $\|\tilde Q - \hat Q\|_2 = O(n u)$ and $\|E\|_2 = O(n u \|T\|_2)$, where $\hat Q$ and $\hat \Lambda$ are the computed factors.
