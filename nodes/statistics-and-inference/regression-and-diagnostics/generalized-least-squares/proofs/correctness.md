---
title: Generalized least squares by Cholesky whitening computes the Aitken estimator, which is the best linear unbiased estimator for a known covariance
proves: [correctness, termination]
status: full
---

The arithmetic is exact. The model is $y = Xb + \varepsilon$ with $X$ a fixed real $n \times p$ matrix of rank $p$, $\mathrm E[\varepsilon] = 0$ and $\operatorname{Cov}(\varepsilon) = \sigma^2 V$, where $V$ is a known symmetric positive definite $n \times n$ matrix and $\sigma^2 > 0$ is unknown.

**Lemma 1 (the factor).** Line L1 succeeds and returns the unique lower triangular $L$ with positive diagonal and $LL^\top = V$.

*Proof.* This is the existence and uniqueness of the [Cholesky decomposition](/cholesky-decomposition/) of a positive definite matrix. In the column loop, the pivot $d_j = v_{jj} - \sum_{k<j} l_{jk}^2$ is the ratio of the leading principal minors of orders $j$ and $j - 1$ of $V$, which are positive, so the square root exists and every division is by a positive number. Each entry of $L$ is forced by the equation $(LL^\top)_{ij} = v_{ij}$ once the earlier columns are known, which gives uniqueness. If some $d_j \le 0$, $V$ is not positive definite and the code raises an error. $\square$

**Lemma 2 (the whitened model).** Let $\tilde X = L^{-1}X$, $\tilde y = L^{-1}y$ and $\tilde\varepsilon = L^{-1}\varepsilon$, as line L2 computes by forward substitution. Then $\tilde y = \tilde Xb + \tilde\varepsilon$ with $\mathrm E[\tilde\varepsilon] = 0$, $\operatorname{Cov}(\tilde\varepsilon) = \sigma^2 I$ and $\operatorname{rank}\tilde X = p$.

*Proof.* Multiply the model by $L^{-1}$. Then $\operatorname{Cov}(\tilde\varepsilon) = L^{-1}\sigma^2VL^{-\top} = \sigma^2L^{-1}LL^\top L^{-\top} = \sigma^2 I$, and $L^{-1}$ is nonsingular, so it keeps the rank of $X$. $\square$

**Lemma 3 (GLS equals OLS on whitened data).** Lines L3 and L4 return the unique minimizer of $(y - X\beta)^\top V^{-1}(y - X\beta)$, which is

$$\hat b = (X^\top V^{-1}X)^{-1}X^\top V^{-1}y,$$

and line L5 returns the minimum value $e^\top V^{-1}e$ with $e = y - X\hat b$.

*Proof.* $V^{-1} = L^{-\top}L^{-1}$, so $(y - X\beta)^\top V^{-1}(y - X\beta) = \|\tilde y - \tilde X\beta\|^2$. Lines L3 and L4 are the QR solution of ordinary least squares for $(\tilde X, \tilde y)$: with $Q^\top\tilde X = \binom{R}{0}$ and $c = Q^\top\tilde y$, $\|\tilde y - \tilde X\beta\|^2 = \|c_{1..p} - R\beta\|^2 + \sum_{i>p}c_i^2$, which is smallest exactly at $\beta = R^{-1}c_{1..p}$, with minimum $\sum_{i>p}c_i^2$ (the same argument as Lemma 1 of the proof on the [weighted least squares](/weighted-least-squares/) page). The minimizer solves the normal equations $\tilde X^\top\tilde X\hat b = \tilde X^\top\tilde y$, and $\tilde X^\top\tilde X = X^\top L^{-\top}L^{-1}X = X^\top V^{-1}X$ and $\tilde X^\top\tilde y = X^\top V^{-1}y$. $\square$

**Lemma 4 (Aitken: unbiased and best).** $\mathrm E[\hat b] = b$, $\operatorname{Cov}(\hat b) = \sigma^2(X^\top V^{-1}X)^{-1}$, and for every linear unbiased estimator $\check b = Cy$ the difference $\operatorname{Cov}(\check b) - \operatorname{Cov}(\hat b)$ is positive semidefinite.

*Proof.* By Lemma 2 the whitened model satisfies the hypotheses of the [Gauss-Markov theorem](/gauss-markov-theorem/), and by Lemma 3 $\hat b$ is its least squares estimate. So $\hat b$ is unbiased with covariance $\sigma^2(\tilde X^\top\tilde X)^{-1} = \sigma^2(X^\top V^{-1}X)^{-1}$, and it has the smallest covariance among estimators that are linear in $\tilde y$ and unbiased. An estimator $Cy$ equals $(CL)\tilde y$, and $D\tilde y$ equals $(DL^{-1})y$, so the estimators linear in $y$ and linear in $\tilde y$ are the same random vectors, and so are the unbiased ones. $\square$

**Lemma 5 (variance estimate and exact intervals).** $s^2 = e^\top V^{-1}e/(n - p)$ from line L6 satisfies $\mathrm E[s^2] = \sigma^2$, and line L7 returns $s^2(X^\top V^{-1}X)^{-1}$. If $\varepsilon$ is normal, $(\hat b_j - b_j)/\sqrt{s^2[(X^\top V^{-1}X)^{-1}]_{jj}}$ has the $t_{n-p}$ law.

*Proof.* In the whitened model $c = Q^\top\tilde y$ has mean $\binom{Rb}{0}$ and covariance $\sigma^2 I$, so $\mathrm E\sum_{i>p}c_i^2 = (n - p)\sigma^2$. $R^{-1}R^{-\top} = (R^\top R)^{-1} = (\tilde X^\top\tilde X)^{-1}$. Under normality $\hat b - b = R^{-1}(c_{1..p} - Rb)$ depends on $c_1, \dots, c_p$ only and $s^2$ on $c_{p+1}, \dots, c_n$ only; these are independent normal coordinates, $(n - p)s^2/\sigma^2 \sim \chi^2_{n-p}$, and the ratio is $t_{n-p}$ by definition. $\square$

**Lemma 6 (the Prais-Winsten matrix is the inverse Cholesky factor of the AR(1) covariance).** Let $|\rho| < 1$ and $V_{ts} = \rho^{|t-s|}/(1 - \rho^2)$. Let $P$ be the $n \times n$ matrix with $P_{11} = \sqrt{1 - \rho^2}$, $P_{tt} = 1$ and $P_{t,t-1} = -\rho$ for $t \ge 2$, and zeros elsewhere. Then $PVP^\top = I$ and $P = L^{-1}$, where $L$ is the Cholesky factor of $V$.

*Proof.* $V$ is the covariance of a stationary AR(1) process $u_t = \rho u_{t-1} + a_t$ with uncorrelated innovations $a_t$ of variance 1: then $\operatorname{Var}u_t = 1/(1 - \rho^2)$ and $\operatorname{Cov}(u_t, u_{t-h}) = \rho^h/(1 - \rho^2)$. The vector $Pu$ has entries $\sqrt{1 - \rho^2}\,u_1$ and $u_t - \rho u_{t-1} = a_t$ for $t \ge 2$. The first has variance 1, the $a_t$ have variance 1, and $a_t$ for $t \ge 2$ is uncorrelated with $u_1$ and with the other innovations, so $\operatorname{Cov}(Pu) = PVP^\top = I$. Hence $V = P^{-1}P^{-\top}$. The matrix $P$ is lower triangular with positive diagonal, so $P^{-1}$ is too, and by the uniqueness in Lemma 1, $P^{-1} = L$. $\square$

So for AR(1) errors line L2 is the Prais-Winsten transformation, and it costs $O(np)$ instead of $O(n^3)$.

**Lemma 7 (Kruskal: when OLS and GLS agree).** The ordinary least squares estimate $(X^\top X)^{-1}X^\top y$ equals $\hat b$ for every $y$ if and only if the column space of $VX$ equals the column space of $X$.

*Proof.* Let $H = X(X^\top X)^{-1}X^\top$ and $e_0 = (I - H)y$, the OLS residual. Since $\hat b$ is the unique solution of $X^\top V^{-1}(y - X\beta) = 0$, OLS equals GLS at $y$ exactly when $X^\top V^{-1}e_0 = 0$. If $\operatorname{col}(VX) = \operatorname{col}(X)$, then $V^{-1}$ maps $\operatorname{col}(X)$ onto itself, so $V^{-1}X = XA$ for some $p \times p$ matrix $A$, and $X^\top V^{-1}e_0 = A^\top X^\top e_0 = 0$ because $e_0 \perp \operatorname{col}(X)$. Conversely, if $X^\top V^{-1}(I - H)y = 0$ for every $y$, the columns of $V^{-1}X$ are orthogonal to $\operatorname{col}(I - H) = \operatorname{col}(X)^\perp$, so $\operatorname{col}(V^{-1}X) \subseteq \operatorname{col}(X)$; both have dimension $p$, so they are equal, and applying $V$ gives $\operatorname{col}(X) = \operatorname{col}(VX)$. $\square$

For example, the equicorrelated $V = (1 - c)I + c\mathbf 1\mathbf 1^\top$ satisfies the condition whenever $\mathbf 1 \in \operatorname{col}(X)$, since $Vx = (1 - c)x + c(\mathbf 1^\top x)\mathbf 1$.

**Termination.** Line L1 is $n$ column steps of finite sums ($n^3/3$ flops), line L2 is $p + 1$ forward substitutions ($n^2$ flops each), the QR of line L3 is $p$ Householder steps, and lines L4 to L7 are finite sums. So the algorithm stops after $\Theta(n^3 + n^2p)$ operations for a dense $V$.
