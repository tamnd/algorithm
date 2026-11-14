---
title: The innovations algorithm computes the best linear one-step predictors, their error variances and the LDL factorization of the covariance matrix
proves: [correctness]
status: full
---

**Setting.** $X_1, \ldots, X_n$ are real random variables with mean 0 and finite variance, and $\kappa(i, j) = \mathbb{E}[X_i X_j]$. The matrix $K_n = [\kappa(i, j)]_{i,j=1}^n$ is positive definite. Work in the Hilbert space $L^2$ with $\langle Y, Z \rangle = \mathbb{E}[YZ]$. Let $H_m = \operatorname{span}\{X_1, \ldots, X_m\}$, with $H_0 = \{0\}$, let $\hat X_{m+1}$ be the orthogonal projection of $X_{m+1}$ on $H_m$, and let $U_{m+1} = X_{m+1} - \hat X_{m+1}$ and $v_m = \lVert U_{m+1} \rVert^2$. In the code, $\theta[m][j]$ is $\theta_{mj}$.

**Claim 1 (the innovations are an orthogonal basis).** For every $m$, $U_1, \ldots, U_m$ are pairwise orthogonal, $v_{m-1} > 0$, and $\operatorname{span}\{U_1, \ldots, U_m\} = H_m$.

*Proof.* By induction on $m$. For $m = 1$, $U_1 = X_1$ and $v_0 = \kappa(1, 1) > 0$. Suppose the claim holds for $m$. Then $U_{m+1} = X_{m+1} - \hat X_{m+1}$ is orthogonal to $H_m$, which contains $U_1, \ldots, U_m$. Since $\hat X_{m+1} \in H_m$, $\operatorname{span}\{U_1, \ldots, U_{m+1}\} = \operatorname{span}(H_m \cup \{X_{m+1}\}) = H_{m+1}$. If $v_m = 0$, then $X_{m+1} = \hat X_{m+1} \in H_m$ almost surely, so $X_{m+1}$ is a linear combination of $X_1, \ldots, X_m$ and $K_{m+1}$ is singular. This contradicts the positive definiteness of $K_n$, because $K_{m+1}$ is a leading principal submatrix. So $v_m > 0$. $\square$

**Claim 2 (the predictor in terms of innovations).** For $m \ge 1$,
$$\hat X_{m+1} = \sum_{k=0}^{m-1} \theta_{m,m-k}\, U_{k+1}, \qquad \theta_{m,m-k} = \frac{\langle X_{m+1}, U_{k+1} \rangle}{v_k},$$
and $v_m = \kappa(m+1, m+1) - \sum_{k=0}^{m-1} \theta_{m,m-k}^2 v_k$.

*Proof.* By Claim 1, $U_1, \ldots, U_m$ is an orthogonal basis of $H_m$ with nonzero vectors, so the projection on $H_m$ is the sum of the projections on each $U_{k+1}$. That is the first formula. By Pythagoras, $\lVert X_{m+1} \rVert^2 = \lVert \hat X_{m+1} \rVert^2 + \lVert U_{m+1} \rVert^2$ and $\lVert \hat X_{m+1} \rVert^2 = \sum_k \theta_{m,m-k}^2 v_k$. This is the formula for $v_m$, which is line L6. $\square$

**Claim 3 (lines L4 and L5).** For $0 \le k \le m - 1$,
$$\langle X_{m+1}, U_{k+1} \rangle = \kappa(m+1, k+1) - \sum_{j=0}^{k-1} \theta_{k,k-j}\, \theta_{m,m-j}\, v_j.$$
So, if lines L3 to L5 compute $\theta_{m,m-k}$ in the order $k = 0, 1, \ldots, m - 1$, every value on the right side is known when it is needed, and line L5 stores the correct $\theta_{m,m-k}$.

*Proof.* By Claim 2 applied to step $k$, $U_{k+1} = X_{k+1} - \sum_{j=0}^{k-1} \theta_{k,k-j} U_{j+1}$ (for $k = 0$ the sum is empty). Hence
$$\langle X_{m+1}, U_{k+1} \rangle = \kappa(m+1, k+1) - \sum_{j=0}^{k-1} \theta_{k,k-j} \langle X_{m+1}, U_{j+1} \rangle,$$
and $\langle X_{m+1}, U_{j+1} \rangle = \theta_{m,m-j} v_j$ by Claim 2. The right side uses $\theta_{k,\cdot}$ from an earlier step and $\theta_{m,m-j}$ with $j < k$, which line L5 set earlier in the same step. Dividing by $v_k > 0$ (Claim 1) gives line L5. $\square$

By induction on $m$, Claims 2 and 3 show that after step $m$ the code holds the exact $\theta_{m1}, \ldots, \theta_{mm}$ and $v_m$. Line L1 sets $v_0 = \kappa(1, 1)$, which is correct because $\hat X_1 = 0$.

**Claim 4 (the factorization and the likelihood).** Let $C$ be the unit lower triangular $n \times n$ matrix with $C_{m+1,k+1} = \theta_{m,m-k}$ for $k < m$, and $D = \operatorname{diag}(v_0, \ldots, v_{n-1})$. Then $X = C U$ and $K_n = C D C^\top$. Hence $\det K_n = \prod_{j=0}^{n-1} v_j$ and $x^\top K_n^{-1} x = \sum_{j=1}^n (x_j - \hat x_j)^2 / v_{j-1}$, where $\hat x_j$ is the predictor of Claim 2 evaluated at the data. For Gaussian $X$,
$$-2 \log L = n \log(2\pi) + \sum_{j=1}^n \log v_{j-1} + \sum_{j=1}^n \frac{(x_j - \hat x_j)^2}{v_{j-1}}.$$

*Proof.* $X_{m+1} = \hat X_{m+1} + U_{m+1}$ and Claim 2 give row $m+1$ of $X = CU$. By Claim 1, $\mathbb{E}[UU^\top] = D$, so $K_n = \mathbb{E}[XX^\top] = C D C^\top$. Then $\det K_n = (\det C)^2 \det D = \prod v_j$. The map from $x$ to $u$ with $x = Cu$ is $u = C^{-1}x$, and $u_j = x_j - \hat x_j$ because the predictors computed from the data satisfy the same triangular relation. So $x^\top K_n^{-1} x = u^\top D^{-1} u$. The Gaussian density $(2\pi)^{-n/2} (\det K_n)^{-1/2} \exp(-\frac12 x^\top K_n^{-1} x)$ gives the formula. $\square$

**Claim 5 (banded covariance).** If $\kappa(i, j) = 0$ whenever $|i - j| > q$, then $\theta_{m,m-k} = 0$ for $k < m - q$. So starting the loops in L3, L4 and L6 at $\max(0, m - q)$ gives the same result.

*Proof.* By Claim 1, $U_{k+1} \in H_{k+1} = \operatorname{span}\{X_1, \ldots, X_{k+1}\}$. If $k < m - q$, then $m + 1 - i > q$ for every $i \le k + 1$, so $X_{m+1}$ is orthogonal to each $X_i$ in that span and $\langle X_{m+1}, U_{k+1} \rangle = 0$. By Claim 2, $\theta_{m,m-k} = 0$. The terms dropped from the sums in L4 and L6 all contain such a factor $\theta_{m,m-j}$ with $j < m - q$, so they are 0. $\square$

**Claim 6 (exact arithmetic).** Lines L1 to L7 use only addition, subtraction, multiplication and division by $v_k > 0$. On rational covariances in exact rational arithmetic they return the exact $\theta_{mj}$ and $v_m$.

*Proof.* Claims 1 to 5. No square root or rounding occurs. $\square$

The tests check Claim 4 against an independent $LDL^\top$ factorization of random positive definite matrices in `Fraction` arithmetic, and the likelihood against a direct determinant and quadratic form. They check Claim 5 by comparing the banded and full versions on MA($q$) covariances, and the MA(1) closed form $v_m = S_{m+1}/S_m$ with $S_m = \sum_{i=0}^{m} \theta^{2i}$ in exact arithmetic.

**Cited, not proved here.** For an invertible MA($q$) process, $\theta_{mj} \to \theta_j$ and $v_m \to \sigma^2$ as $m \to \infty$ (Brockwell and Davis 1991, Chapter 5). If $m \to \infty$ with $m^3/n \to 0$, the estimates $\hat\theta_{m1}, \ldots, \hat\theta_{mq}$ from sample autocovariances are consistent and asymptotically normal (Brockwell and Davis 1991, Section 8.3). The simulation on the page measures the finite-sample behaviour for MA(1).
