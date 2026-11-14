---
title: Johansen's eigenvalue procedure gives the Gaussian maximum likelihood estimate for each cointegration rank, and the trace and maximum eigenvalue statistics are the likelihood ratio statistics
proves: [correctness, termination]
status: full
---

We prove that the reduced rank regression of lines L1 to L6 maximizes the Gaussian likelihood of the error correction model under $\operatorname{rank}\Pi \le r$ (Lemmas 1 and 2 and Theorem 3), that the trace and maximum eigenvalue statistics of line L7 are the likelihood ratio statistics (Corollary 4), that the Cholesky reduction solves the generalized eigenproblem (Lemma 5), that $0 \le \hat\lambda_i \le 1$ (Lemma 6), that the eigenvalues are invariant to invertible linear maps of the data (Lemma 7), and that for $K = 1$ the procedure reduces to the Dickey-Fuller t ratio (Lemma 8). We do not prove the asymptotic null laws of the statistics (Johansen 1988, 1991), the accuracy of the simulated quantiles, the consistency of the sequential rank choice, or the convergence rate of the Jacobi method. Throughout, $S_{00}$ and $S_{11}$ are assumed positive definite, which holds when the regressors of lines L1 and L2 have full rank and no exact linear relation holds among the residuals.

**Lemma 1 (concentrating out the short-run terms).** Let $Z_t$ collect the lagged differences and, in case "c", the constant. For fixed $\Pi$ and $\Omega$, the Gaussian log likelihood of $\nabla Y_t = \Pi Y_{t-1} + \Gamma Z_t + \varepsilon_t$ is maximized over $\Gamma$ by the least squares fit, and the concentrated log likelihood is
$$\ell(\Pi, \Omega) = -\frac{T}{2}\log\det\Omega - \frac12\sum_t(R_{0t} - \Pi R_{1t})^\top\Omega^{-1}(R_{0t} - \Pi R_{1t}) + \text{const},$$
with $R_{0t}$ and $R_{1t}$ the residuals of lines L1 and L2.

*Proof.* Stack the rows: $D = Y_{-1}\Pi^\top + Z\Gamma^\top + E$, where $D$ is $T \times K$. The quadratic form $\operatorname{tr}\{\Omega^{-1}(D - Y_{-1}\Pi^\top - Z\Gamma^\top)^\top(D - Y_{-1}\Pi^\top - Z\Gamma^\top)\}$ is minimized over $\Gamma$ by the least squares fit of $D - Y_{-1}\Pi^\top$ on $Z$, for any positive definite $\Omega$, because generalized least squares with a common regressor matrix in every equation equals least squares equation by equation (this is the result proved on the [vector autoregression](/vector-autoregression/) page). The minimizing residual is $M_Z(D - Y_{-1}\Pi^\top) = R_0 - R_1\Pi^\top$, where $M_Z$ is the projection onto the orthogonal complement of the columns of $Z$, $R_0 = M_ZD$ and $R_1 = M_ZY_{-1}$. These are exactly the residuals of lines L1 and L2. $\square$

**Lemma 2 (fixed $\beta$).** Under $\Pi = \alpha\beta^\top$ with $\beta$ fixed of full rank $r$, the maximum over $\alpha$ and $\Omega$ is attained at $\hat\alpha(\beta) = S_{01}\beta(\beta^\top S_{11}\beta)^{-1}$ and $\hat\Omega(\beta) = S_{00} - S_{01}\beta(\beta^\top S_{11}\beta)^{-1}\beta^\top S_{10}$, and
$$\det\hat\Omega(\beta) = \det S_{00}\cdot\frac{\det\beta^\top(S_{11} - S_{10}S_{00}^{-1}S_{01})\beta}{\det\beta^\top S_{11}\beta}.$$
The concentrated log likelihood is $-\frac T2\log\det\hat\Omega(\beta) - \frac{TK}{2} + \text{const}$.

*Proof.* With $\beta$ fixed, $R_{0t} = \alpha(\beta^\top R_{1t}) + \varepsilon_t$ is a multivariate regression on the $r$ regressors $\beta^\top R_{1t}$, common to all equations. By the same fact as in Lemma 1, least squares gives $\hat\alpha(\beta)$, and the residual covariance is the Gaussian maximum likelihood estimate of $\Omega$, which is $\hat\Omega(\beta)$. At that $\Omega$ the quadratic term equals $\operatorname{tr}(\hat\Omega^{-1}T\hat\Omega) = TK$. For the determinant, consider the block matrix
$$\begin{pmatrix}S_{00} & S_{01}\beta\\ \beta^\top S_{10} & \beta^\top S_{11}\beta\end{pmatrix}.$$
Its determinant equals $\det(\beta^\top S_{11}\beta)\det(S_{00} - S_{01}\beta(\beta^\top S_{11}\beta)^{-1}\beta^\top S_{10})$ by the Schur complement of the lower right block, and also $\det S_{00}\det(\beta^\top S_{11}\beta - \beta^\top S_{10}S_{00}^{-1}S_{01}\beta)$ by the Schur complement of the upper left block. Equate the two forms and divide. $\square$

**Theorem 3 (reduced rank regression).** Let $\hat\lambda_1 \ge \dots \ge \hat\lambda_K$ solve $\det(\lambda S_{11} - S_{10}S_{00}^{-1}S_{01}) = 0$, with $\hat\lambda_K < 1$. Over all $K \times r$ matrices $\beta$ of rank $r$,
$$\min_\beta\det\hat\Omega(\beta) = \det S_{00}\prod_{i=1}^{r}(1 - \hat\lambda_i),$$
attained by the first $r$ columns of $\hat\beta$ from line L6. Hence $\hat\alpha_r\hat\beta_r^\top$ is the maximum likelihood estimate of $\Pi$ under $H(r)$.

*Proof.* Write $S_{11} = LL^\top$ and $C = L^{-1}S_{10}S_{00}^{-1}S_{01}L^{-\top}$, which is symmetric with eigenvalues $\hat\lambda_i$ (Lemma 5). Put $\gamma = L^\top\beta$. Then the ratio in Lemma 2 is $\det\gamma^\top(I - C)\gamma/\det\gamma^\top\gamma$. Replacing $\gamma$ by $\gamma M$ for invertible $M$ multiplies the numerator and the denominator by $(\det M)^2$, so we may take $\gamma = G$ with orthonormal columns, $G^\top G = I_r$. The matrix $A = I - C$ is symmetric with eigenvalues $a_1 \le \dots \le a_K$, where $a_i = 1 - \hat\lambda_i$, all positive. By the Poincaré separation theorem, a consequence of the Courant-Fischer minimax principle, the eigenvalues $\mu_1 \le \dots \le \mu_r$ of $G^\top AG$ satisfy $\mu_j \ge a_j$ for $j = 1..r$. So $\det G^\top AG = \prod_j\mu_j \ge \prod_{j \le r}a_j = \prod_{i \le r}(1 - \hat\lambda_i)$. Equality holds when the columns of $G$ are the eigenvectors $v_1..v_r$ of $C$ for the $r$ largest $\hat\lambda_i$, since then $G^\top AG = \operatorname{diag}(1 - \hat\lambda_1, \dots, 1 - \hat\lambda_r)$. That $G$ corresponds to $\beta = L^{-\top}[v_1 \dots v_r]$, which is line L6. $\square$

**Corollary 4 (the statistics are likelihood ratios).** The maximized log likelihood under $H(r)$ is $-\frac T2\left(\log\det S_{00} + \sum_{i \le r}\log(1 - \hat\lambda_i)\right)$ plus a constant that does not depend on $r$. Therefore $-2\log$ of the likelihood ratio of $H(r)$ against $H(K)$ is $-T\sum_{i=r+1}^{K}\log(1 - \hat\lambda_i)$, and of $H(r)$ against $H(r + 1)$ is $-T\log(1 - \hat\lambda_{r+1})$.

*Proof.* Theorem 3 with Lemma 2 gives the maximized value for each $r$, including $r = K$, where $\beta$ ranges over all invertible matrices and the model is the unrestricted VAR. Take differences. $\square$

**Lemma 5 (lines L4 to L6).** If $Cv = \lambda v$ with $\lVert v\rVert = 1$ and $\beta = L^{-\top}v$, then $S_{10}S_{00}^{-1}S_{01}\beta = \lambda S_{11}\beta$. For an orthonormal eigenbasis $V$ of $C$, $\hat\beta = L^{-\top}V$ satisfies $\hat\beta^\top S_{11}\hat\beta = I$.

*Proof.* $S_{10}S_{00}^{-1}S_{01}\beta = LCL^\top L^{-\top}v = LCv = \lambda Lv = \lambda LL^\top L^{-\top}v = \lambda S_{11}\beta$. Also $\hat\beta^\top S_{11}\hat\beta = V^\top L^{-1}LL^\top L^{-\top}V = V^\top V = I$. $C$ is symmetric because $S_{01} = S_{10}^\top$ and $S_{00}^{-1}$ is symmetric, so an orthonormal eigenbasis exists. $\square$

The implementation symmetrizes $C$ before the Jacobi method, which removes rounding asymmetry and does not change $C$ in exact arithmetic. Each Jacobi rotation is an orthogonal similarity, so the eigenvalues are preserved, and the product of the rotations is orthogonal.

**Lemma 6 (the eigenvalues lie in $[0, 1]$).** $C$ is positive semidefinite, and $I - C$ is positive semidefinite.

*Proof.* $C = (S_{00}^{-1/2}S_{01}L^{-\top})^\top(S_{00}^{-1/2}S_{01}L^{-\top})$ is a Gram matrix. For $I - C = L^{-1}(S_{11} - S_{10}S_{00}^{-1}S_{01})L^{-\top}$, note that $S_{11} - S_{10}S_{00}^{-1}S_{01}$ is the Schur complement of $S_{00}$ in the moment matrix $\frac1T\sum_t(R_{0t}^\top, R_{1t}^\top)^\top(R_{0t}^\top, R_{1t}^\top)$, which is positive semidefinite; the Schur complement of a positive definite block in a positive semidefinite matrix is positive semidefinite. So $0 \le \hat\lambda_i \le 1$. These are the squared canonical correlations between $R_0$ and $R_1$. $\square$

**Lemma 7 (invariance).** Let $A$ be an invertible $K \times K$ matrix. Replacing $Y_t$ by $AY_t$ in case "none", or by $AY_t + c$ in case "c", leaves every $\hat\lambda_i$ unchanged, and $\hat\beta$ becomes $A^{-\top}\hat\beta$ up to the choice of eigenbasis.

*Proof.* The lagged differences become $A\nabla Y_{t-i}$, which span the same column space, and in case "c" the constant $c$ disappears in the differences and is absorbed by the constant regressor in the levels. So $R_0 \mapsto R_0A^\top$ and $R_1 \mapsto R_1A^\top$, and $S_{ij} \mapsto AS_{ij}A^\top$. Then $\det(\lambda AS_{11}A^\top - AS_{10}A^\top(AS_{00}A^\top)^{-1}AS_{01}A^\top) = (\det A)^2\det(\lambda S_{11} - S_{10}S_{00}^{-1}S_{01})$, which has the same roots. The eigenvector equation is solved by $A^{-\top}\beta$. $\square$

**Lemma 8 (one series).** For $K = 1$, $p = 1$ and case "none", $\hat\lambda = t^2/(t^2 + T - 1)$, where $t$ is the t ratio of $\rho$ in $\nabla Y_t = \rho Y_{t-1} + e_t$.

*Proof.* Let $N = (\sum Y_{t-1}\nabla Y_t)^2/\sum Y_{t-1}^2$ and $D = \sum(\nabla Y_t)^2$. Then $\hat\lambda = S_{01}^2/(S_{00}S_{11}) = N/D$. The residual sum of squares is $D - N$, so $t^2 = \hat\rho^2\sum Y_{t-1}^2/s^2 = (T - 1)N/(D - N)$. Then $t^2/(t^2 + T - 1) = N/(N + D - N) = N/D$. $\square$

So the trace statistic for $K = 1$ is $-T\log(1 - t^2/(t^2 + T - 1)) = T\log(1 + t^2/(T - 1))$, a two-sided function of the Dickey-Fuller statistic.

**Termination.** Lines L1 to L4 and L6 to L8 are loops with fixed bounds. Line L5 runs cyclic Jacobi sweeps until the off-diagonal mass is below a relative tolerance, with at most a fixed number of sweeps. The cyclic Jacobi method converges for symmetric matrices, quadratically in the end (Forsythe and Henrici 1960; Wilkinson 1962), which we cite. In the tests a $3 \times 3$ problem needs at most a few sweeps.
