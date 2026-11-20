---
title: The ETKF gives an ensemble with exactly the Kalman analysis mean and covariance of the sample prior
proves: [correctness, termination]
status: full
---

**Setting.** There are $N \ge 2$ forecast members $x_1, \ldots, x_N \in \mathbb R^n$ and observations $y^o \in \mathbb R^p$ with a symmetric positive definite error covariance $R$. $X$ ($n \times N$) has the columns $x_i - \bar x$ (line L1) and $Y$ ($p \times N$) has the columns $h(x_i) - \bar y$ (line L2). They are unscaled, so the sample covariance is $P^f = X X^\top/(N - 1)$, and $X\mathbf 1 = 0$, $Y \mathbf 1 = 0$ for the vector of ones $\mathbf 1$. Let $\rho > 0$ be the inflation, $\gamma = (N - 1)/\rho$ and $P = \rho P^f = X X^\top/\gamma$. Lines L3 to L7 compute $C = Y^\top R^{-1}$, $A = \gamma I + C Y$, $\tilde P = A^{-1}$, $W = \sqrt{N - 1}\,\tilde P^{1/2}$ (symmetric) and $\bar w = \tilde P C (y^o - \bar y)$. Line L8 returns $x^a_i = \bar x + X(\bar w + W_i)$, with $W_i$ the column $i$ of $W$.

**Lemma 1 (the matrices exist).** $A$ is symmetric positive definite, with eigenvalues at least $\gamma$. So $\tilde P$ and its symmetric square root exist, and $W$ is symmetric positive definite.

*Proof.* $z^\top A z = \gamma \|z\|^2 + (Y z)^\top R^{-1}(Y z) \ge \gamma\|z\|^2$. With $A = Q\Lambda Q^\top$ (line L5), $\tilde P = Q\Lambda^{-1}Q^\top$ and $\tilde P^{1/2} = Q \Lambda^{-1/2} Q^\top$, which is what line L6 forms. $\square$

**Lemma 2 (the transform keeps the mean).** $W \mathbf 1 = \sqrt\rho\,\mathbf 1$ and $\mathbf 1^\top \bar w = 0$.

*Proof.* $A \mathbf 1 = \gamma \mathbf 1 + C Y \mathbf 1 = \gamma\mathbf 1$, so $\mathbf 1$ is an eigenvector of $A$ with eigenvalue $\gamma$, and of every function of $A$: $\tilde P \mathbf 1 = \mathbf 1/\gamma$ and $W\mathbf 1 = \sqrt{(N - 1)/\gamma}\,\mathbf 1 = \sqrt\rho\,\mathbf 1$. Then $\mathbf 1^\top \bar w = (\tilde P \mathbf 1)^\top C (y^o - \bar y) = \gamma^{-1}(Y\mathbf 1)^\top R^{-1}(y^o - \bar y) = 0$. $\square$

**Lemma 3 (push-through identity).** $Y^\top (Y Y^\top + \gamma R)^{-1} = (Y^\top R^{-1} Y + \gamma I)^{-1} Y^\top R^{-1} = \tilde P C$.

*Proof.* $(Y^\top R^{-1} Y + \gamma I) Y^\top = Y^\top R^{-1}(Y Y^\top + \gamma R)$, and both brackets are invertible. $\square$

**Theorem 4 (exact Kalman moments).** Let $h(x) = H x$ be linear and $K = P H^\top (H P H^\top + R)^{-1}$. The analysis ensemble has the mean $\bar x + K(y^o - H \bar x)$ and the sample covariance $(I - KH)P$.

*Proof.* $Y = H X$ and $\bar y = H \bar x$. $K = X Y^\top (Y Y^\top + \gamma R)^{-1} = X \tilde P C$ by Lemma 3, so $K(y^o - H\bar x) = X \bar w$. By Lemma 2 the members have the mean $\bar x + X\bar w + X W\mathbf 1/N = \bar x + X \bar w + \sqrt\rho X \mathbf 1/N = \bar x + X\bar w$. Their perturbations are the columns of $X W$, so the sample covariance is $X W W^\top X^\top/(N - 1) = X \tilde P X^\top$. Finally

$$(I - KH)P = \frac{X X^\top - X \tilde P C Y X^\top}{\gamma} = \frac{X \tilde P (A - C Y) X^\top}{\gamma} = X \tilde P X^\top. \qquad\square$$

With $N = 2$, $x = (-1/\sqrt 2, 1/\sqrt 2)$, $H = 1$, $R = 1$, $\rho = 1$ and $y^o = 1$, $P = 1$ and $K = 1/2$, so the analysis has the mean $1/2$ and the variance $1/2$, which is the check value of the page.

**Corollary 5 (the analysis stays in the ensemble space).** Every analysis member lies in $\bar x + \mathrm{range}(X)$, a space of dimension at most $N - 1$.

*Proof.* $x^a_i - \bar x = X(\bar w + W_i)$. $\square$

**Remarks.** The Kalman update here uses the sample covariance, so it is the true posterior only when $P^f$ is the true forecast covariance and the errors are Gaussian. For a linear Gaussian model and exact forecasts the sample covariance converges as $N \to \infty$, and the ETKF converges to the Kalman filter (Kwiatkowski and Mandel 2015). For a nonlinear $h$ the matrix $Y$ replaces $H X$, which is a heuristic, and Theorem 4 does not apply. Any $W' = W U$ with $U$ orthogonal and $U \mathbf 1 = \mathbf 1$ gives the same mean and covariance. A square root $W'$ with $W'\mathbf 1$ not a multiple of $\mathbf 1$, such as a Cholesky factor of $(N - 1)\tilde P$, gives members with the mean $\bar x + X\bar w + X W'\mathbf 1/N$. In general this is not the Kalman mean, and the sample covariance about the new mean is then smaller than $X\tilde P X^\top$.

**Termination.** Lines L1 to L4 and L6 to L8 are finite sums and one linear solve with the positive definite $R$. Line L5 runs the cyclic Jacobi method for at most a fixed number of sweeps. So the algorithm returns at line L9. $\blacksquare$
