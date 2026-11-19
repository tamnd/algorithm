---
title: W = U V^T is an orthogonal map of least squared error, and it is the only one when M is nonsingular
proves: [correctness]
status: full
---

Let $X, Y \in \mathbb{R}^{n \times d}$ hold the source vectors $\vec x_i$ and the target vectors $\vec y_i$ as rows (after line L1). Let $M = Y^\top X$ (line L2) and let $M = U \Sigma V^\top$ be a singular value decomposition (line L3): $U$ and $V$ are orthogonal $d \times d$ matrices and $\Sigma = \operatorname{diag}(\sigma_1, \ldots, \sigma_d)$ with $\sigma_k \ge 0$. We prove that $W = U V^\top$ (line L4) is orthogonal and minimizes

$$f(W) = \sum_{i=1}^{n} \|W \vec x_i - \vec y_i\|^2$$

over all orthogonal $W$, and that it is the only minimizer when $M$ is nonsingular.

## Step 1. $W = U V^\top$ is orthogonal.

$W^\top W = V U^\top U V^\top = V V^\top = I$, because $U$ and $V$ are orthogonal. $\square$

## Step 2. Over orthogonal maps, minimizing $f$ is maximizing $\operatorname{tr}(W^\top M)$.

For an orthogonal $W$, $\|W \vec x_i\| = \|\vec x_i\|$, so

$$\|W \vec x_i - \vec y_i\|^2 = \|\vec x_i\|^2 + \|\vec y_i\|^2 - 2\,\vec y_i^\top W \vec x_i.$$

Summing over $i$, $f(W) = \|X\|_F^2 + \|Y\|_F^2 - 2 \sum_i \vec y_i^\top W \vec x_i$. The first two terms do not depend on $W$. For the last term, $\vec y_i^\top W \vec x_i = \operatorname{tr}(W \vec x_i \vec y_i^\top)$, and $\sum_i \vec x_i \vec y_i^\top = X^\top Y = M^\top$, so

$$\sum_i \vec y_i^\top W \vec x_i = \operatorname{tr}(W M^\top) = \operatorname{tr}(M W^\top) = \operatorname{tr}(W^\top M).$$

So $f(W) = \|X\|_F^2 + \|Y\|_F^2 - 2\operatorname{tr}(W^\top M)$, and an orthogonal $W$ minimizes $f$ exactly when it maximizes $g(W) = \operatorname{tr}(W^\top M)$. $\square$

## Step 3. $g(W) \le \sum_k \sigma_k$ for every orthogonal $W$.

Let $Z = V^\top W^\top U$. It is a product of orthogonal matrices, so it is orthogonal. By the cyclic property of the trace,

$$g(W) = \operatorname{tr}(W^\top U \Sigma V^\top) = \operatorname{tr}(V^\top W^\top U \Sigma) = \operatorname{tr}(Z \Sigma) = \sum_{k=1}^{d} z_{kk} \sigma_k.$$

Each column of $Z$ is a unit vector, so $|z_{kk}| \le 1$. Since $\sigma_k \ge 0$, $z_{kk}\sigma_k \le \sigma_k$ for every $k$, and $g(W) \le \sum_k \sigma_k$. $\square$

## Step 4. $W = U V^\top$ reaches the bound.

For $W = U V^\top$, $Z = V^\top V U^\top U = I$, so $g(W) = \sum_k \sigma_k$. With Steps 2 and 3, $f(U V^\top) \le f(W)$ for every orthogonal $W$. With Step 1, line L4 returns an orthogonal minimizer. Line L5 returns it unchanged. $\square$

## Step 5. The minimizer is unique when $M$ is nonsingular.

If $M$ is nonsingular, then every $\sigma_k > 0$. Let $W$ be any orthogonal minimizer. By Step 4, $g(W) = \sum_k \sigma_k$, so $\sum_k (1 - z_{kk})\sigma_k = 0$. Every term is at least 0, so $z_{kk} = 1$ for every $k$. A unit column with the diagonal entry 1 has all other entries 0, so $Z = I$. Then $V^\top W^\top U = I$ gives $W^\top = V U^\top$, that is $W = U V^\top$.

This does not depend on which SVD line L3 returns. When the singular values are distinct, $U$ and $V$ are unique up to the signs of matching columns, and a sign change of column $k$ in both $U$ and $V$ leaves $U V^\top$ unchanged. In every case, the argument above shows that each orthogonal minimizer is equal to $U V^\top$ for the SVD in hand, so all SVDs give the same $W$. $\square$

## Step 6. The singular case.

If some $\sigma_k = 0$, then $z_{kk}$ is free in Step 5, and the minimizer can fail to be unique. Step 4 still holds for any SVD, including one whose columns of $U$ for the zero singular values are any orthonormal completion, which is how the code builds them. So line L4 always returns a minimizer, though not always the only one. For example, with $n = 1$, $d = 2$, $\vec x_1 = (1, 0)$ and $\vec y_1 = (0, 1)$, both the rotation by $90°$ and the reflection that swaps the two axes send $\vec x_1$ to $\vec y_1$ with error 0. $\blacksquare$

**Remark.** The bound of Step 3 uses all orthogonal $Z$, including those with determinant $-1$. If $W$ must be a rotation ($\det W = 1$), the bound is not always reached, and the answer is the Kabsch correction $U \operatorname{diag}(1, \ldots, 1, s) V^\top$ with $s = \det(U V^\top)$. The mapping of word vectors allows reflections, so it does not need this correction.
