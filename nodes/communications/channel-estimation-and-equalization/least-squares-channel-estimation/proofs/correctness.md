---
title: The LS channel estimate minimizes the residual, is unbiased, has error covariance N0 (X^H X)^(-1), and orthogonal training minimizes its error
proves: [correctness]
status: full
---

Write $X$ for the $m \times L$ pilot matrix of line L2, with $X_{il} = x[i + L - 1 - l]$ and $m = N_p - L + 1$, and $v = (y[L-1], \ldots, y[N_p - 1])$ for the samples of line L3. Each of these samples depends on pilots only, so the model is

$$v = X h + w, \qquad w \sim \mathcal{CN}(0, N_0 I). \tag{1}$$

Let $G = X^H X$ (line L4) and $b = X^H v$ (line L5). We work in exact complex arithmetic.

**Lemma 1 (when the estimate exists).** $G$ is Hermitian and positive semidefinite. It is positive definite if and only if $X$ has full column rank $L$. This needs $m \ge L$, that is $N_p \ge 2L - 1$.

*Proof.* $G^H = X^H X = G$, and $z^H G z = \|X z\|^2 \ge 0$ for every $z$, with equality if and only if $X z = 0$. So $G$ is positive definite if and only if $X z = 0$ only for $z = 0$, which is full column rank. An $m \times L$ matrix has rank at most $m$, so full column rank needs $m \ge L$. $\square$

When $G$ is positive definite, the Cholesky factor of line L6 exists and $\hat h = G^{-1} b = (X^H X)^{-1} X^H v$. If $G$ is singular, the implementation raises an error.

**Theorem 1 (least squares).** $\hat h$ is the unique minimizer of $\|v - X g\|^2$ over $g \in \mathbb{C}^L$.

*Proof.* For any $g$, write $g = \hat h + d$. Then $v - X g = r - X d$ with $r = v - X \hat h$. By line L6, $X^H r = b - G \hat h = 0$, so the cross terms $(X d)^H r = d^H X^H r$ and $r^H X d$ are zero, and

$$\|v - X g\|^2 = \|r\|^2 + \|X d\|^2 \ge \|r\|^2.$$

Equality holds if and only if $X d = 0$, and by Lemma 1 this means $d = 0$. $\square$

**Theorem 2 (bias and error covariance).** Under (1), $E[\hat h] = h$ and $E[(\hat h - h)(\hat h - h)^H] = N_0 (X^H X)^{-1}$. So the mean squared error is

$$E\|\hat h - h\|^2 = N_0 \operatorname{tr}\big((X^H X)^{-1}\big).$$

*Proof.* Put (1) into $\hat h = G^{-1} X^H v$: $\hat h = G^{-1} X^H X h + G^{-1} X^H w = h + G^{-1} X^H w$. The error is $e = G^{-1} X^H w$, a linear function of $w$, so $E[e] = 0$ and

$$E[e e^H] = G^{-1} X^H E[w w^H] X G^{-1} = N_0\, G^{-1} G\, G^{-1} = N_0\, G^{-1},$$

because $G$ and $G^{-1}$ are Hermitian. The mean squared error is the trace of this matrix. $\square$

In the linear Gaussian model (1), this covariance is equal to the Cramer-Rao bound for unbiased estimators of $h$, so no unbiased estimator does better. Kay proves this for the linear model in Chapter 4 and for complex data in Chapter 15. With a prior on $h$, a biased estimator can do better; that is the LMMSE estimator.

**Theorem 3 (the best training).** Let $T = \operatorname{tr}(X^H X) > 0$, the total energy of the pilot rows. Then

$$\operatorname{tr}\big((X^H X)^{-1}\big) \ge \frac{L^2}{T},$$

with equality if and only if $X^H X = (T/L)\, I$.

*Proof.* $G$ is Hermitian and positive definite, so it has eigenvalues $\lambda_1, \ldots, \lambda_L > 0$ with $\sum_i \lambda_i = T$, and $G^{-1}$ has eigenvalues $1/\lambda_i$. By the Cauchy-Schwarz inequality on the vectors $(\sqrt{\lambda_i})$ and $(1/\sqrt{\lambda_i})$,

$$L^2 = \Big(\sum_i \sqrt{\lambda_i} \cdot \frac{1}{\sqrt{\lambda_i}}\Big)^2 \le \Big(\sum_i \lambda_i\Big)\Big(\sum_i \frac{1}{\lambda_i}\Big) = T\, \operatorname{tr}(G^{-1}).$$

Equality holds if and only if the two vectors are parallel, that is all $\lambda_i$ are equal to $T/L$. A Hermitian matrix with all eigenvalues equal to $c$ is $c I$. $\square$

So for a fixed pilot energy, the mean squared error is at least $L^2 N_0 / T$, and pilots with $X^H X = (T/L) I$ reach it. The page example has $X^T X = 4I$, $T = 8$ and $L = 2$, so its error is $N_0 \cdot 2/4 = N_0/2 = L^2 N_0/T$.

**Remark (the cost).** Lines L2 and L3 copy $m L + m$ numbers. Line L4 forms the $L \times L$ matrix $G$ with $m L^2$ multiplications; it is Hermitian, so half of them suffice. Line L5 costs $m L$, and the Cholesky solve of line L6 costs $O(L^3)$. With $m \ge L$, the total is $O(m L^2)$. When the same pilots are used again, $P = G^{-1} X^H$ is computed once, and each new estimate $\hat h = P v$ costs $m L$ multiplications.
