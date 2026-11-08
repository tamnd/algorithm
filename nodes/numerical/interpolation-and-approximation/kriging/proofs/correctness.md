---
title: Correctness of kriging
proves: [correctness, optimality, interpolation, unbiasedness]
status: full
---

Let $K$ be the $n \times n$ matrix $K_{ij} = C(\|x_i - x_j\|)$, assumed positive definite, $k = k(x)$ with $k_i = C(\|x - x_i\|)$, $C_0 = C(0)$ and $\mathbf{1}$ the vector of ones. The field is $Z = m + \varepsilon$ with $\mathbb{E}\varepsilon = 0$ and covariance $C$, and $y_i = Z(x_i)$.

**Claim 1 (mean squared error of a linear predictor).** For weights $\lambda \in \mathbb{R}^n$ with $\sum\lambda_i = 1$, or for the simple kriging form $m + \lambda^T(y - m\mathbf{1})$ with any $\lambda$, the prediction error is $\varepsilon(x) - \lambda^T\varepsilon_{\text{data}}$, and
$$Q(\lambda) = \mathbb{E}\big(\varepsilon(x) - \lambda^T\varepsilon_{\text{data}}\big)^2 = C_0 - 2\lambda^Tk + \lambda^TK\lambda.$$

*Proof.* If $\sum\lambda_i = 1$, then $Z(x) - \lambda^Ty = m + \varepsilon(x) - \lambda^T(m\mathbf{1} + \varepsilon_{\text{data}}) = \varepsilon(x) - \lambda^T\varepsilon_{\text{data}}$; in the simple form the $m$ terms cancel directly. Expand the square and use $\mathbb{E}\varepsilon(x)^2 = C_0$, $\mathbb{E}\varepsilon(x)\varepsilon(x_i) = k_i$, $\mathbb{E}\varepsilon(x_i)\varepsilon(x_j) = K_{ij}$. $\square$

**Claim 2 (simple kriging).** $Q$ has the unique minimizer $\lambda = K^{-1}k$ over $\mathbb{R}^n$, with minimum $C_0 - k^TK^{-1}k$.

*Proof.* $Q(\lambda) = C_0 - k^TK^{-1}k + (\lambda - K^{-1}k)^TK(\lambda - K^{-1}k)$, by expanding the last term. The last term is positive unless $\lambda = K^{-1}k$, since $K$ is positive definite. $\square$

With $K = LL^T$ and $r = L^{-1}k$, $k^TK^{-1}k = r^Tr$, which is the simple kriging variance computed in line L6 without its last term. The prediction is $m + k^TK^{-1}(y - m\mathbf{1}) = m + k^Tw$ with $w = K^{-1}(y - m\mathbf{1})$.

**Claim 3 (ordinary kriging).** Over $\{\lambda : \mathbf{1}^T\lambda = 1\}$, $Q$ has the unique minimizer
$$\lambda^* = K^{-1}k + g\,K^{-1}\mathbf{1}, \qquad g = \frac{1 - \mathbf{1}^TK^{-1}k}{\mathbf{1}^TK^{-1}\mathbf{1}},$$
it solves the bordered system with $\mu = -g$, and the minimum is $C_0 - k^TK^{-1}k + \dfrac{(1 - \mathbf{1}^TK^{-1}k)^2}{\mathbf{1}^TK^{-1}\mathbf{1}}$.

*Proof.* $Q$ is strictly convex and the constraint set is an affine subspace, so a point satisfying the Lagrange conditions $K\lambda + \mu\mathbf{1} = k$, $\mathbf{1}^T\lambda = 1$ is the unique minimizer. From the first, $\lambda = K^{-1}k - \mu K^{-1}\mathbf{1}$; the second gives $\mathbf{1}^TK^{-1}k - \mu\,\mathbf{1}^TK^{-1}\mathbf{1} = 1$, so $\mu = -g$ (note $\mathbf{1}^TK^{-1}\mathbf{1} > 0$). For the minimum, write $\lambda^* = \lambda_s + gK^{-1}\mathbf{1}$ with $\lambda_s = K^{-1}k$. By the identity in the proof of Claim 2, $Q(\lambda^*) = Q(\lambda_s) + g^2\,\mathbf{1}^TK^{-1}\mathbf{1} = C_0 - k^TK^{-1}k + \frac{(1 - \mathbf{1}^TK^{-1}k)^2}{\mathbf{1}^TK^{-1}\mathbf{1}}$. Also, from the Lagrange conditions, $Q(\lambda^*) = C_0 - 2\lambda^{*T}k + \lambda^{*T}(k - \mu\mathbf{1}) = C_0 - \lambda^{*T}k - \mu$, the textbook form. $\square$

**Claim 4 (lines L3 to L6 compute it).** With $a = K^{-1}\mathbf{1}$, $b = K^{-1}y$, $\beta = \mathbf{1}^Tb/\mathbf{1}^Ta$ and $w = b - \beta a$, the ordinary kriging prediction is $\lambda^{*T}y = \beta + k^Tw$, and its variance is the expression of line L6.

*Proof.* $\lambda^{*T}y = k^TK^{-1}y + g\,\mathbf{1}^TK^{-1}y = k^Tb + g\,\mathbf{1}^Tb$, using the symmetry of $K^{-1}$. Substitute $g = (1 - a^Tk)/\mathbf{1}^Ta$: $\lambda^{*T}y = k^Tb + \beta(1 - a^Tk) = \beta + k^T(b - \beta a) = \beta + k^Tw$. For the variance, $k^TK^{-1}k = \|L^{-1}k\|^2 = r^Tr$, $\mathbf{1}^TK^{-1}k = a^Tk$ and $\mathbf{1}^TK^{-1}\mathbf{1} = \mathbf{1}^Ta$, which is line L6 by Claim 3. The triangular solves with $L$ and $L^T$ compute $K^{-1}$ times a vector exactly in exact arithmetic. $\square$

**Claim 5 (interpolation).** If $x = x_j$, then $\lambda^* = e_j$, $\hat Z(x_j) = y_j$ and $\sigma^2(x_j) = 0$, in both simple and ordinary kriging.

*Proof.* $k(x_j)$ is the $j$-th column of $K$, so $K^{-1}k = e_j$ and $\mathbf{1}^TK^{-1}k = 1$, which makes $g = 0$. Then $\hat Z = y_j$ and the variance is $C_0 - K_{jj} + 0 = 0$. $\square$

**Claim 6 (unbiasedness and constants).** In ordinary kriging $\mathbf{1}^T\lambda^* = 1$, so $\mathbb{E}\hat Z(x) = m$ for every $m$, and if all $y_i = c$ then $\hat Z(x) = c$ for all $x$.

*Proof.* The constraint holds by construction. If $y = c\mathbf{1}$, then $\lambda^{*T}y = c$. Equivalently, $b = ca$, $\beta = c$ and $w = 0$. $\square$

**Claim 7 (best linear unbiased predictor).** Any linear predictor $\nu^Ty$ that is unbiased for every $m$ must have $\mathbf{1}^T\nu = 1$, since $\mathbb{E}\nu^Ty = m\,\mathbf{1}^T\nu$. By Claims 1 and 3, $Q(\nu) \ge Q(\lambda^*)$ with equality only for $\nu = \lambda^*$. So ordinary kriging is the BLUP and $\sigma^2(x) = Q(\lambda^*)$ is its exact mean squared error under the model. $\square$

**Termination.** Cholesky, the triangular solves and the inner products are fixed loops; the Cholesky factorization of a positive definite matrix never meets a nonpositive pivot in exact arithmetic, and the implementation raises an error if rounding produces one.
