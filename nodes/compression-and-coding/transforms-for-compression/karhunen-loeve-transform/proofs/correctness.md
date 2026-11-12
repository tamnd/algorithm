---
title: The KLT decorrelates, has the best compaction and coding gain, and the Jacobi method computes it
proves: [correctness]
status: full
---

Let $R$ be a real symmetric positive semidefinite $N \times N$ matrix, the covariance of a random vector $x$ with mean $\mu$. By the spectral theorem, $R$ has real eigenvalues $\lambda_1 \ge \dots \ge \lambda_N \ge 0$ and an orthonormal basis of eigenvectors $v_1, \dots, v_N$. Let $T$ be the matrix with rows $v_1^{\mathsf T}, \dots, v_N^{\mathsf T}$. For a matrix $S$ write $\operatorname{off}(S)^2 = \sum_{i \ne j} s_{ij}^2$.

**Theorem 1 (decorrelation and exact inverse).** Let $y = T(x - \mu)$. Then $E[y] = 0$, $E[yy^{\mathsf T}] = \operatorname{diag}(\lambda_1, \dots, \lambda_N)$, and $T^{\mathsf T} y + \mu = x$.

*Proof.* $E[y] = T(E[x] - \mu) = 0$. By linearity of expectation, $E[yy^{\mathsf T}] = T\, E[(x-\mu)(x-\mu)^{\mathsf T}]\, T^{\mathsf T} = TRT^{\mathsf T}$. Entry $(j,k)$ is $v_j^{\mathsf T} R v_k = \lambda_k v_j^{\mathsf T} v_k$, which is $\lambda_k$ if $j = k$ and 0 otherwise. The rows of $T$ are orthonormal, so $TT^{\mathsf T} = I$; a square matrix with a right inverse has the same left inverse, so $T^{\mathsf T}T = I$ and $T^{\mathsf T} y + \mu = (x - \mu) + \mu = x$. $\square$

**Theorem 2 (best compaction, Ky Fan).** Let $A$ be orthogonal with rows $a_1^{\mathsf T}, \dots, a_N^{\mathsf T}$, and let $\sigma_k^2 = a_k^{\mathsf T} R a_k$ be the variance of coefficient $k$ of $A(x - \mu)$. Then for each $m$,

$$\sum_{k=1}^{m} \sigma_k^2 \le \sum_{k=1}^{m} \lambda_k ,$$

with equality for $A = T$.

*Proof.* Write $c_{kj} = a_k^{\mathsf T} v_j$. Then $a_k = \sum_j c_{kj} v_j$ and $\sigma_k^2 = \sum_j \lambda_j c_{kj}^2$. So

$$\sum_{k=1}^{m} \sigma_k^2 = \sum_{j=1}^{N} \lambda_j w_j, \qquad w_j = \sum_{k=1}^{m} c_{kj}^2 .$$

The matrix $(c_{kj})$ is the product $AT^{\mathsf T}$ of two orthogonal matrices, so it is orthogonal, and its columns and rows are unit vectors. Hence $0 \le w_j \le \sum_{k=1}^{N} c_{kj}^2 = 1$, and $\sum_j w_j = \sum_{k=1}^{m} \sum_j c_{kj}^2 = m$. Let $w$ be any such weights with $w_i < 1$ for some $i \le m$. Then the weights sum to $m$, so $w_j > 0$ for some $j > m$. Moving the amount $\min(1 - w_i, w_j)$ from $j$ to $i$ changes the sum by $\min(1 - w_i, w_j)(\lambda_i - \lambda_j) \ge 0$, and it raises the number of indices $i \le m$ with $w_i = 1$ or the number of indices $j > m$ with $w_j = 0$. After finitely many moves, $w_1 = \dots = w_m = 1$ and the other weights are 0, and the sum is $\lambda_1 + \dots + \lambda_m$. The sum never decreased, so the original sum is at most $\lambda_1 + \dots + \lambda_m$. For $A = T$, $\sigma_k^2 = v_k^{\mathsf T} R v_k = \lambda_k$. $\square$

**Corollary (best $m$-term approximation).** Keeping the first $m$ coefficients of $A(x - \mu)$ and setting the others to zero gives the mean squared error $\sum_{k > m} \sigma_k^2 = \operatorname{tr} R - \sum_{k \le m} \sigma_k^2 \ge \sum_{k > m} \lambda_k$, because $A$ keeps squared error and $\sum_k \sigma_k^2 = \operatorname{tr}(ARA^{\mathsf T}) = \operatorname{tr} R$.

**Lemma 1 (Hadamard's inequality).** For a symmetric positive semidefinite $S$, $\det S \le \prod_k s_{kk}$, with equality when $S$ is positive definite only if $S$ is diagonal.

*Proof.* If some $s_{kk} = 0$, then row and column $k$ of $S$ are zero (a positive semidefinite matrix with a zero diagonal entry has $s_{kj}^2 \le s_{kk} s_{jj} = 0$), so $\det S = 0$ and the inequality holds. Otherwise let $D = \operatorname{diag}(s_{kk}^{-1/2})$ and $C = DSD$. Then $C$ is positive semidefinite with unit diagonal, so its eigenvalues $\gamma_k \ge 0$ add up to $\operatorname{tr} C = N$. By the inequality of the arithmetic and geometric means, $\det C = \prod_k \gamma_k \le (\frac1N \sum_k \gamma_k)^N = 1$, with equality only if all $\gamma_k = 1$, that is $C = I$. Since $\det C = \det S / \prod_k s_{kk}$, the claim follows, and equality forces $S = D^{-1} I D^{-1}$, which is diagonal. $\square$

**Theorem 3 (best coding gain).** For each orthogonal $A$, the coding gain $G_A = \frac{\frac1N \sum_k \sigma_k^2}{(\prod_k \sigma_k^2)^{1/N}}$ satisfies $G_A \le G_T = \frac{\frac1N \operatorname{tr} R}{(\det R)^{1/N}}$ when $R$ is positive definite. If moreover $ARA^{\mathsf T}$ is not diagonal, the inequality is strict.

*Proof.* The numerator is $\frac1N \operatorname{tr}(ARA^{\mathsf T}) = \frac1N \operatorname{tr} R$ for every orthogonal $A$. By Lemma 1 with $S = ARA^{\mathsf T}$, $\prod_k \sigma_k^2 \ge \det(ARA^{\mathsf T}) = \det(A)^2 \det R = \det R$, with equality only if $ARA^{\mathsf T}$ is diagonal. For $A = T$ the product is $\prod_k \lambda_k = \det R$. $\square$

Under the high-rate model of transform coding with optimal bit allocation, the mean distortion is $c \cdot (\prod_k \sigma_k^2)^{1/N} 2^{-2b}$, so Theorem 3 says that the KLT minimizes it when the constant $c$ is the same for all coefficients. This holds for Gaussian sources, because every linear combination of a Gaussian vector is Gaussian; for other sources $c$ depends on the distribution of each coefficient, and the conclusion can fail.

**Lemma 2 (one Jacobi rotation).** Let $A$ be symmetric with $a_{pq} \ne 0$, $p < q$. Let $\theta = (a_{qq} - a_{pp})/(2a_{pq})$, let $t$ be the root of smaller magnitude of $t^2 + 2\theta t - 1 = 0$, $c = 1/\sqrt{1 + t^2}$ and $s = tc$. Let $J$ be the identity except $J_{pp} = J_{qq} = c$, $J_{pq} = s$ and $J_{qp} = -s$, and let $A' = J^{\mathsf T} A J$. Then $J$ is orthogonal, $a'_{pq} = 0$, and $\operatorname{off}(A')^2 = \operatorname{off}(A)^2 - 2a_{pq}^2$.

*Proof.* $c^2 + s^2 = c^2(1 + t^2) = 1$, so the columns of $J$ are orthonormal. Column $p$ of $J$ is $c e_p - s e_q$ and column $q$ is $s e_p + c e_q$, so

$$a'_{pq} = (c e_p - s e_q)^{\mathsf T} A (s e_p + c e_q) = cs(a_{pp} - a_{qq}) + (c^2 - s^2) a_{pq} = c^2 a_{pq}\big(1 - t^2 - 2\theta t\big) = 0,$$

using $a_{pp} - a_{qq} = -2\theta a_{pq}$ and $1 - t^2 - 2\theta t = 0$. The roots of $t^2 + 2\theta t - 1$ are real with product $-1$, so $t$ exists, and the formula $t = \operatorname{sign}(\theta)/(|\theta| + \sqrt{\theta^2 + 1})$ of line L7 is this root ($t = \sqrt{\theta^2+1} - \theta$ for $\theta \ge 0$ and $t = -\sqrt{\theta^2+1} - \theta$ for $\theta < 0$, rewritten without cancellation). An orthogonal similarity keeps the Frobenius norm: $\|A'\|_F = \|A\|_F$. The diagonal entries $a'_{kk}$ for $k \ne p, q$ equal $a_{kk}$, because $J e_k = e_k$. The $2 \times 2$ block of $A'$ on the indices $p, q$ is $G^{\mathsf T} B G$, where $B$ is the block of $A$ and $G$ is the $2 \times 2$ rotation, so it has the same Frobenius norm as $B$: $a'^2_{pp} + a'^2_{qq} = a_{pp}^2 + a_{qq}^2 + 2a_{pq}^2$, since $a'_{pq} = 0$. So the sum of the squared diagonal entries grows by exactly $2a_{pq}^2$, and the off-diagonal part, which is the rest of the fixed total, shrinks by $2a_{pq}^2$. $\square$

**Theorem 4 (termination and accuracy of JACOBI).** If $N \ge 2$ and $R \ne 0$, then JACOBI stops after at most

$$\left\lceil \frac{2 \ln\!\big(\operatorname{off}(R) / (\text{tol}\, \|R\|_F)\big)}{-\ln\!\big(1 - \frac{2}{N(N-1)}\big)} \right\rceil$$

rotations (zero if the ratio is at most 1). At that point $V$ is orthogonal, $A = V^{\mathsf T} R V$, and the diagonal entries of $A$, sorted, differ from the sorted eigenvalues of $R$ by at most $\operatorname{off}(A) \le \text{tol} \cdot \|R\|_F$.

*Proof.* The off-diagonal part has $N(N-1)$ entries, and the chosen $a_{pq}$ has the largest magnitude among them, so $\operatorname{off}(A)^2 \le N(N-1)\, a_{pq}^2$. By Lemma 2, each rotation gives

$$\operatorname{off}(A')^2 = \operatorname{off}(A)^2 - 2a_{pq}^2 \le \Big(1 - \frac{2}{N(N-1)}\Big) \operatorname{off}(A)^2 .$$

After $r$ rotations, $\operatorname{off}(A)^2 \le (1 - \frac{2}{N(N-1)})^r \operatorname{off}(R)^2$, which is at most $(\text{tol} \|R\|_F)^2$ once $r$ reaches the stated bound. (If $a_{pq} = 0$ the loop has already reached $\operatorname{off}(A) = 0$.) $V$ is a product of orthogonal matrices, and each step replaces $A$ by $J^{\mathsf T} A J$ and $V$ by $VJ$, so $A = V^{\mathsf T} R V$ holds by induction. Write $A = \Lambda + E$ with $\Lambda$ the diagonal part. $A$ has the same eigenvalues as $R$. By Weyl's inequality, the $k$-th largest eigenvalue of $\Lambda + E$ differs from the $k$-th largest of $\Lambda$, which is the $k$-th largest diagonal entry, by at most $\|E\|_2 \le \|E\|_F = \operatorname{off}(A)$. $\square$

Each column of $V$ is then an approximate eigenvector: $\|R v_k - a_{kk} v_k\|_2 = \|A e_k - a_{kk} e_k\|_2 \le \operatorname{off}(A)$, because $RV = VA$ and $V$ is orthogonal. Sorting the columns and fixing their signs (lines L9 and L10) does not change these facts, so KLT returns an orthogonal $T$ with $TRT^{\mathsf T}$ diagonal up to $\operatorname{off}(A)$, and Theorems 1 to 3 apply to it up to that error.

$\blacksquare$
