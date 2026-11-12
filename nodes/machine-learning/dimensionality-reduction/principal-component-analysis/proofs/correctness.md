---
title: PCA maximizes the projected variance and minimizes the reconstruction error
proves: [correctness]
status: full
---

**Setup.** The points are $x_1, \ldots, x_n \in \mathbb{R}^d$ with mean $\bar x$. Let $y_i = x_i - \bar x$ and $C = \frac{1}{n}\sum_i y_i y_i^T$. $C$ is symmetric and positive semidefinite, so by the [spectral theorem](/spectral-theorem/) $C = \sum_{j=1}^d \lambda_j v_j v_j^T$ with $\lambda_1 \ge \cdots \ge \lambda_d \ge 0$ and an orthonormal basis $v_1, \ldots, v_d$. Let $V_k = [v_1, \ldots, v_k]$. A *frame* is a $d \times k$ matrix $W$ with $W^T W = I_k$, and $P = W W^T$ is the orthogonal projection onto its column space. For a frame $W$ and an offset $b \in \mathbb{R}^d$ define

$$\operatorname{var}(W) = \frac{1}{n}\sum_i \|W^T y_i\|^2, \qquad \operatorname{err}(W, b) = \frac{1}{n}\sum_i \|(I - P)(x_i - b)\|^2.$$

$\operatorname{err}(W, b)$ is the mean squared distance from the points to the affine subspace $b + \operatorname{range} W$, because the closest point of that subspace to $x$ is $b + P(x - b)$.

**Lemma 1 (variance is a trace).** $\operatorname{var}(W) = \operatorname{tr}(W^T C W)$.

*Proof.* $\|W^T y\|^2 = \operatorname{tr}(W^T y y^T W)$. Sum over $i$, divide by $n$, and use the linearity of the trace. $\square$

**Lemma 2 (the offset).** For each frame $W$ and each $b$, $\operatorname{err}(W, b) = \operatorname{err}(W, \bar x) + \|(I - P)(\bar x - b)\|^2 \ge \operatorname{err}(W, \bar x)$.

*Proof.* Write $x_i - b = y_i + (\bar x - b)$ and expand $\|(I-P)y_i + (I-P)(\bar x - b)\|^2$. The cross term is $\frac{2}{n} (\sum_i y_i)^T (I - P)(\bar x - b) = 0$, because $(I-P)$ is symmetric and $\sum_i y_i = 0$. $\square$

So an optimal affine subspace may be taken through the mean. This is the reason for the centering step L2.

**Lemma 3 (the two views are one).** $\operatorname{err}(W, \bar x) = \operatorname{tr} C - \operatorname{var}(W)$.

*Proof.* $P$ is an orthogonal projection, so $\|y - Py\|^2 = \|y\|^2 - \|Py\|^2$ (Pythagoras, since $Py \perp y - Py$). Also $\|Py\|^2 = y^T W W^T W W^T y = \|W^T y\|^2$. Average over $i$ and use $\frac{1}{n}\sum_i \|y_i\|^2 = \operatorname{tr} C$. $\square$

**Lemma 4 (Ky Fan).** For each frame $W$, $\operatorname{tr}(W^T C W) \le \lambda_1 + \cdots + \lambda_k$, with equality for $W = V_k$.

*Proof.* Let $h_j = \|W^T v_j\|^2$. Then $\operatorname{tr}(W^T C W) = \sum_j \lambda_j \operatorname{tr}(W^T v_j v_j^T W) = \sum_j \lambda_j h_j$. Each $h_j$ is in $[0, 1]$, because $\|W^T v\| = \|P v\| \le \|v\| = 1$. And $\sum_j h_j = \|W^T [v_1, \ldots, v_d]\|_F^2 = \|W^T\|_F^2 = k$, since multiplication by an orthogonal matrix keeps the Frobenius norm. Then

$$\sum_j \lambda_j h_j - \sum_{j \le k}\lambda_j = \sum_{j \le k} \lambda_j (h_j - 1) + \sum_{j > k} \lambda_j h_j \le \lambda_k \sum_{j \le k}(h_j - 1) + \lambda_k \sum_{j > k} h_j = \lambda_k\Big(\sum_j h_j - k\Big) = 0.$$

The inequality uses $h_j - 1 \le 0$ with $\lambda_j \ge \lambda_k$ for $j \le k$, and $h_j \ge 0$ with $\lambda_j \le \lambda_k$ for $j > k$. For $W = V_k$, $h_j = 1$ for $j \le k$ and $h_j = 0$ for $j > k$, so equality holds. $\square$

**Lemma 5 (when the subspace is unique).** If $\lambda_k > \lambda_{k+1}$, each optimal frame spans $\operatorname{span}(v_1, \ldots, v_k)$. If $\lambda_k = \lambda_{k+1}$, it does not.

*Proof.* Equality in Lemma 4 forces each dropped term to be zero, in particular $(\lambda_k - \lambda_j) h_j = 0$ for $j > k$. If $\lambda_k > \lambda_{k+1} \ge \lambda_j$, then $h_j = 0$, so $\operatorname{range} W \perp v_j$ for all $j > k$. A $k$-dimensional subspace orthogonal to $v_{k+1}, \ldots, v_d$ is $\operatorname{span}(v_1, \ldots, v_k)$. If $\lambda_k = \lambda_{k+1}$, the frame $[v_1, \ldots, v_{k-1}, v_{k+1}]$ also gives the sum $\lambda_1 + \cdots + \lambda_k$ and spans another subspace. $\square$

**Theorem.** Let the eigensolver of line L4 return the eigenpairs of $C$, sorted. Then the output $W = V_k$ of PCA has these properties.

1. It maximizes $\operatorname{var}(W)$ over all frames, and the maximum is $\lambda_1 + \cdots + \lambda_k$.
2. The pair $(W, \bar x)$ minimizes $\operatorname{err}(W, b)$ over all frames and offsets, and the minimum is $\lambda_{k+1} + \cdots + \lambda_d$.
3. The scores $z_i = W^T y_i$ of line L6 have mean zero and covariance $\operatorname{diag}(\lambda_1, \ldots, \lambda_k)$.
4. The answer is unique up to the signs of the columns when $\lambda_1 > \lambda_2 > \cdots > \lambda_{k+1}$. If two of these eigenvalues are equal, the eigenvectors of that eigenvalue are fixed only up to an orthogonal map of their span.

*Proof.* Lines L1 to L3 compute $\bar x$, the $y_i$ and $C$ by their definitions. Line L4 returns orthonormal eigenvectors by the correctness of the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/), and line L5 keeps the first $k$. Part 1 is Lemmas 1 and 4. For part 2, Lemma 2 reduces each offset to $\bar x$, and Lemma 3 turns the minimum of $\operatorname{err}(W, \bar x)$ into the maximum of $\operatorname{var}(W)$, which part 1 gives; the value is $\operatorname{tr} C - \sum_{j \le k}\lambda_j = \sum_{j > k}\lambda_j$. For part 3, $\frac{1}{n}\sum_i z_i = W^T \frac{1}{n}\sum_i y_i = 0$ and $\frac{1}{n}\sum_i z_i z_i^T = W^T C W = \operatorname{diag}(\lambda_1, \ldots, \lambda_k)$, because $C v_j = \lambda_j v_j$ and the $v_j$ are orthonormal. For part 4, if $\lambda_j$ is a simple eigenvalue, its unit eigenvectors are $\pm v_j$ only. If $\lambda_j$ has multiplicity $m > 1$ and the $d \times m$ matrix $E$ holds an orthonormal basis of its eigenspace, then $E Q$ is again such a basis for each $m \times m$ orthogonal $Q$. The subspace part follows from Lemma 5. $\blacksquare$

**The SVD route.** Let $X_c = U \Sigma V^T$ be a thin [singular value decomposition](/singular-value-decomposition/) of the centered data matrix. Then $C = \frac{1}{n} X_c^T X_c = V \frac{\Sigma^2}{n} V^T$, so the right singular vectors are eigenvectors of $C$, $\lambda_j = \sigma_j^2 / n$, and the scores are $X_c V_k = U_k \Sigma_k$. The minimum error of part 2 is $\frac{1}{n}\sum_{j > k}\sigma_j^2$, which agrees with the Eckart-Young theorem on that page: $U_k \Sigma_k V_k^T$ is the closest matrix of rank at most $k$ to $X_c$ in the Frobenius norm.
