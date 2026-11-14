---
title: The ADF regression is an exact rewriting of an autoregression, the routine returns its least squares t ratio, the ratio is invariant to level, scale and trend, and the simulated p-value is valid
proves: [correctness, termination]
status: full
---

We prove four things about ADF. The regression is an exact reparametrization of an AR($p + 1$) model in which the null $\rho = 0$ is a unit root and every causal stationary model has $\rho < 0$ (Lemmas 1 and 2). Lines L5 to L8 return the ordinary least squares t ratio (Lemma 3). The ratio is invariant to the transformations of Lemma 4. Under the null with Gaussian errors and $p = 0$, this makes the Monte Carlo p-value valid at every sample size (Theorem 5). We do not prove the Dickey-Fuller limit laws or their extension by Said and Dickey to ARMA errors. We cite them from Dickey and Fuller (1979), Phillips (1987) and Said and Dickey (1984), and Hamilton (1994), Chapter 17, gives a full derivation.

Notation: $\phi(z) = 1 - \sum_{j=1}^{p+1}\phi_j z^j$, $B$ is the backshift operator, $\nabla = 1 - B$.

**Lemma 1 (the ADF form).** For any real $\phi_1, \dots, \phi_{p+1}$, set $\rho = -\phi(1)$ and $\gamma_i = -\sum_{j=i+1}^{p+1}\phi_j$ for $i = 1, \dots, p$. Then, as polynomials,
$$\phi(z) = (1 - z) - \rho z - \sum_{i=1}^{p}\gamma_i (z^i - z^{i+1}). \qquad (1)$$
Hence $\phi(B)U_t = \varepsilon_t$ holds exactly when $\nabla U_t = \rho U_{t-1} + \sum_{i=1}^{p}\gamma_i\nabla U_{t-i} + \varepsilon_t$. The map from $(\phi_1, \dots, \phi_{p+1})$ to $(\rho, \gamma_1, \dots, \gamma_p)$ is one-to-one.

*Proof.* Compare coefficients of the right side of (1). The constant term is 1. Since $-\rho = \phi(1) = 1 - \sum_{j \ge 1}\phi_j$, the coefficient of $z$ is $-1 - \rho - \gamma_1 = -1 + (1 - \sum_{j \ge 1}\phi_j) + \sum_{j \ge 2}\phi_j = -\phi_1$. For $2 \le j \le p$ the coefficient of $z^j$ is $\gamma_{j-1} - \gamma_j = -\sum_{l \ge j}\phi_l + \sum_{l \ge j+1}\phi_l = -\phi_j$. The coefficient of $z^{p+1}$ is $\gamma_p = -\phi_{p+1}$. So both sides of (1) agree. Applying (1) with $z$ replaced by $B$ to $U_t$ gives $\phi(B)U_t = \nabla U_t - \rho U_{t-1} - \sum_i \gamma_i \nabla U_{t-i}$, which is the second claim. The inverse map is $\phi_{p+1} = -\gamma_p$, $\phi_j = \gamma_j - \gamma_{j-1}$ for $2 \le j \le p$, and $\phi_1 = 1 + \rho + \gamma_1$, so the map is one-to-one. $\square$

When $X_t = d_t + U_t$ with $d_t$ a constant or a line, $\nabla X_t = \nabla d_t + \nabla U_t$ and $X_{t-1} = d_{t-1} + U_{t-1}$. Substituting, the deterministic parts combine into a constant (when $d_t = a$) or a constant plus a multiple of $t$ (when $d_t = a + bt$). So the regression with $d^*_t = 1$ or $d^*_t = (1, t)$ contains the true model.

**Lemma 2 (the hypotheses).** (a) $\rho = 0$ if and only if $\phi(1) = 0$, that is, $z = 1$ is a root of $\phi$. In that case $\phi(z) = (1 - z)(1 - \sum_{i=1}^p \gamma_i z^i)$. (b) If every root of $\phi$ has modulus greater than 1, then $\rho < 0$.

*Proof.* (a) The first claim is $\rho = -\phi(1)$. With $\rho = 0$, (1) reads $\phi(z) = (1 - z) - \sum_i\gamma_i z^i(1 - z) = (1 - z)(1 - \sum_i\gamma_i z^i)$. (b) $\phi$ is a real polynomial with $\phi(0) = 1 > 0$. It has no zero in $[0, 1]$, since such a zero would be a root of modulus at most 1. By continuity $\phi$ keeps its sign on $[0, 1]$, so $\phi(1) > 0$ and $\rho = -\phi(1) < 0$. $\square$

Part (a) says that under the null, $\nabla U_t$ is the autoregression $(1 - \sum\gamma_i B^i)\nabla U_t = \varepsilon_t$, so the lagged differences remove exactly the serial correlation in $\nabla X_t$. The converse of (b) is false: $\rho < 0$ also holds for some models with complex roots inside the unit circle. The test's alternative is the set of causal stationary models.

**Lemma 3 (lines L5 to L8).** Let $Z$ be the $T \times k$ matrix with rows $z_t$, of full column rank, and let $Z = QR$ with $Q^\top Q = I_k$ and $R$ upper triangular with positive diagonal. Then $\hat\beta = R^{-1}Q^\top D$ is the least squares solution, $e = D - Z\hat\beta$ is its residual, and $s\,\|(R^{-1})_{1,\cdot}\| = s\sqrt{[(Z^\top Z)^{-1}]_{11}}$. So line L8 returns the ordinary t ratio of the first coefficient.

*Proof.* $Z^\top Z = R^\top Q^\top Q R = R^\top R$, which is invertible since $R$ has a positive diagonal. The normal equations $Z^\top Z\beta = Z^\top D$ read $R^\top R\beta = R^\top Q^\top D$; cancel the invertible $R^\top$ to get $R\beta = Q^\top D$, whose unique solution is $\hat\beta$. Next, $(Z^\top Z)^{-1} = R^{-1}R^{-\top}$, whose $(1,1)$ entry is $\sum_c (R^{-1})_{1c}^2$. $\square$

Modified Gram-Schmidt, used in the implementation, produces the same $Q$ and $R$ as classical Gram-Schmidt in exact arithmetic, with better orthogonality in floating point. The implementation stops with an error if a column is (numerically) a combination of the earlier ones, which is the full rank condition.

**Lemma 4 (invariance).** Let $Y_t = a + bt + cX_t$ with $c \ne 0$. In case "ct", $\tau(Y) = \tau(X)$ for all $a, b$. In case "c", $\tau(Y) = \tau(X)$ when $b = 0$. In case "n", $\tau(Y) = \tau(X)$ when $a = b = 0$.

*Proof.* Take case "ct". The response is $\nabla Y_t = b + c\nabla X_t$, and the regressors are $1$, $t$, $Y_{t-1} = (a - b) + bt + cX_{t-1}$ and $\nabla Y_{t-i} = b + c\nabla X_{t-i}$. Let $M$ be the projection that removes the span of $1$, $t$ and the lagged differences. That span equals the span of $1$, $t$ and the $\nabla X_{t-i}$, because each $\nabla Y_{t-i}$ differs from $c\nabla X_{t-i}$ by a constant. By the Frisch-Waugh-Lovell theorem, $\hat\rho = (MY_{-1})^\top(M\nabla Y)/\|MY_{-1}\|^2$, where $Y_{-1}$ is the column of $Y_{t-1}$. Now $MY_{-1} = cMX_{-1}$ and $M\nabla Y = cM\nabla X$, since $M$ kills the constants and the trend. So $\hat\rho(Y) = c^2(\cdot)/c^2(\cdot) = \hat\rho(X)$. The full residual vector is $M\nabla Y - \hat\rho MY_{-1} = c(M\nabla X - \hat\rho MX_{-1})$, so $s(Y) = |c|s(X)$. The variance factor is $[(Z^\top Z)^{-1}]_{11} = 1/\|MY_{-1}\|^2 = 1/(c^2\|MX_{-1}\|^2)$. Hence $\operatorname{se}(Y) = |c|s(X)/(|c|\|MX_{-1}\|) = \operatorname{se}(X)$ and $\tau(Y) = \tau(X)$. In case "c", with $b = 0$, the same argument works with $M$ removing $1$ and the lagged differences. In case "n", with $a = b = 0$, all columns and the response are multiplied by $c$. $\square$

**Theorem 5 (an exact Monte Carlo test).** Suppose $p = 0$ and, under $H_0$, $X_t = X_0 + \mu t + \sigma S_t$ with $S_t = \sum_{s \le t}\eta_s$, $\eta_s$ iid $N(0, 1)$, $\sigma > 0$, and $\mu = 0$ in case "c". Let $\tau^{(1)}, \dots, \tau^{(R)}$ be the statistics of $R$ independent standard Gaussian random walks of length $n$ started at 0, and $p_{\mathrm{MC}} = (1 + \#\{r : \tau^{(r)} \le \tau\})/(1 + R)$. Then $P(p_{\mathrm{MC}} \le \alpha) \le \alpha$ for every $\alpha \in (0, 1)$ and every $n$.

*Proof.* By Lemma 4, $\tau(X) = \tau(S)$, and $S$ has the same law as each simulated walk. So $\tau, \tau^{(1)}, \dots, \tau^{(R)}$ are iid. Their common law is continuous, since $\tau$ is a nonconstant ratio of smooth functions of a Gaussian vector, so ties have probability 0. The rank of $\tau$ among the $R + 1$ values is then uniform on $\{1, \dots, R + 1\}$, and $p_{\mathrm{MC}}$ equals this rank divided by $R + 1$. Hence $P(p_{\mathrm{MC}} \le \alpha) = \lfloor\alpha(R + 1)\rfloor/(R + 1) \le \alpha$. $\square$

For $p \ge 1$, or for non-Gaussian errors, the finite-sample law of $\tau$ depends on $\gamma$ and on the error law, and the simulated p-value is only approximate.

**Cited: the limit law.** Under $H_0$, with $\varepsilon_t$ iid with finite variance and $p = 0$, the statistic converges in distribution to the functionals of Brownian motion stated on the page (Dickey and Fuller 1979; Phillips 1987 under weaker conditions). Said and Dickey (1984) prove that with ARMA errors and $p \to \infty$, $p^3/T \to 0$, the t ratio has the same limit. The rejection rule $\tau < c_\alpha(T)$ therefore has size tending to $\alpha$. The response surface $c_\alpha(T)$ of MacKinnon (2010) is an empirical fit to simulations. Its fitting error is small next to the Monte Carlo error of a typical study, but it is not an exact formula.

**Termination.** Line L1 runs $n - 1$ times, lines L3 and L4 $T$ times, the QR factorization of line L5 has $k$ outer steps, and lines L6 to L10 are finite. So ADF terminates. The lag search runs ADF at most $p_{\max} + 1$ times. $\square$
