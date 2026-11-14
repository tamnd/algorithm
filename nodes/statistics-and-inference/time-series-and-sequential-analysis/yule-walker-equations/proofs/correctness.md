---
title: The Durbin-Levinson recursion solves the Yule-Walker system of every order, and with the divisor-n autocovariance the fitted autoregression is always causal
proves: [correctness]
status: full
---

**Setting.** $\gamma$ is an even function on the integers, $\Gamma_k = [\gamma(i - j)]_{i,j=1}^{k}$, $\gamma_k = (\gamma(1), \ldots, \gamma(k))^\top$ and $E_k$ is the $k \times k$ exchange matrix, which reverses the order of a vector. For the estimator, $\gamma = \hat\gamma$ is the sample autocovariance with the divisor $n$, computed by lines L1 and L2. For $k \ge 1$ let $\phi_k = (\phi_{k1}, \ldots, \phi_{kk})^\top$ solve $\Gamma_k \phi_k = \gamma_k$, and let $v_k = \gamma(0) - \phi_k^\top \gamma_k$, with $v_0 = \gamma(0)$.

**Claim 1 (the population equations).** If $\{X_t\}$ is a causal AR($p$) process $X_t - \mu = \sum_{i=1}^p \phi_i (X_{t-i} - \mu) + \varepsilon_t$ with $\{\varepsilon_t\} \sim \mathrm{WN}(0, \sigma^2)$, then $\Gamma_p \phi = \gamma_p$ and $\sigma^2 = \gamma(0) - \phi^\top \gamma_p$. If $\Gamma_p$ is nonsingular, these equations determine $\phi$ and $\sigma^2$ from $\gamma(0), \ldots, \gamma(p)$.

*Proof.* Put $\mu = 0$. Causality gives $X_{t-k} = \sum_{j \ge 0} \psi_j \varepsilon_{t-k-j}$, so $\mathbb{E}[\varepsilon_t X_{t-k}] = 0$ for $k \ge 1$, and $\mathbb{E}[\varepsilon_t X_t] = \mathbb{E}[\varepsilon_t (\sum_i \phi_i X_{t-i} + \varepsilon_t)] = \sigma^2$. Multiply the model equation by $X_{t-k}$ and take expectations: $\gamma(k) = \sum_i \phi_i \gamma(k - i)$ for $k = 1, \ldots, p$, which is $\Gamma_p \phi = \gamma_p$. With $k = 0$: $\gamma(0) = \sum_i \phi_i \gamma(i) + \sigma^2$. $\square$

**Claim 2 (the recursion).** Suppose $\Gamma_k$ is nonsingular for $k = 1, \ldots, p$ and $v_{k-1} \ne 0$. Then for each $k$, with

$$a_k = \frac{\gamma(k) - \sum_{j=1}^{k-1} \phi_{k-1,j}\, \gamma(k - j)}{v_{k-1}},$$

the solution of order $k$ is $\phi_{kj} = \phi_{k-1,j} - a_k \phi_{k-1,k-j}$ for $j < k$ and $\phi_{kk} = a_k$, and $v_k = v_{k-1}(1 - a_k^2)$. These are lines L5 to L8, so after step $k$ the variables hold $\phi_k$ and $v_k$, and the value appended to the PACF list is $\phi_{kk}$.

*Proof.* Because $\Gamma_{k-1}$ is a symmetric Toeplitz matrix, $E \Gamma_{k-1} E = \Gamma_{k-1}$ (persymmetry), with $E = E_{k-1}$. Partition

$$\Gamma_k = \begin{pmatrix} \Gamma_{k-1} & E\gamma_{k-1} \\ \gamma_{k-1}^\top E & \gamma(0) \end{pmatrix}, \qquad \gamma_k = \begin{pmatrix} \gamma_{k-1} \\ \gamma(k) \end{pmatrix},$$

and try $\phi_k = (\phi_{k-1} - a E\phi_{k-1},\ a)$ for a scalar $a$. The first block row gives $\Gamma_{k-1}\phi_{k-1} - a \Gamma_{k-1} E \phi_{k-1} + a E\gamma_{k-1} = \gamma_{k-1} - a E \Gamma_{k-1}\phi_{k-1} + a E\gamma_{k-1} = \gamma_{k-1}$, for every $a$. The last row gives

$$\gamma_{k-1}^\top E \phi_{k-1} - a\, \gamma_{k-1}^\top \phi_{k-1} + a\gamma(0) = \sum_{j=1}^{k-1} \phi_{k-1,j}\gamma(k - j) + a v_{k-1},$$

which equals $\gamma(k)$ exactly when $a = a_k$. Since $\Gamma_k$ is nonsingular, this is the unique solution. For the error,

$$v_k = \gamma(0) - (\phi_{k-1} - a_k E\phi_{k-1})^\top \gamma_{k-1} - a_k\gamma(k) = v_{k-1} + a_k\Big(\sum_{j} \phi_{k-1,j}\gamma(k - j) - \gamma(k)\Big) = v_{k-1} - a_k^2 v_{k-1}. \quad \square$$

**Claim 3 (positive definiteness).** If the data $x_1, \ldots, x_n$ are not all equal, then $\hat\Gamma_k$ is positive definite for every $k \ge 1$. Hence every $v_k > 0$ and every $|a_k| < 1$, so lines L5 and L8 never divide by 0 and the code never raises its error on such data.

*Proof.* Let $d_t = x_t - \bar x$ for $1 \le t \le n$ and $d_t = 0$ otherwise. Not all $d_t$ are 0. Then $\hat\gamma(h) = \frac1n \sum_t d_{t+h} d_t$ over all integers $t$, and for $c \in \mathbb{R}^k$,

$$c^\top \hat\Gamma_k c = \frac1n \sum_{i,j} c_i c_j \sum_t d_{t+i-j} d_t = \frac1n \sum_s \Big(\sum_{i=1}^{k} c_i d_{s-i}\Big)^2 \ge 0.$$

If this is 0, then the convolution of $(d_t)$ with $(c_i)$ is 0, so the polynomial product $(\sum_t d_t z^t)(\sum_i c_i z^i)$ is 0. The first factor is not the zero polynomial, so $c = 0$. Thus $\hat\Gamma_k$ is positive definite. Next, $\Gamma_{k+1}$ can be written with $\gamma(0)$ in the top left corner and $\Gamma_k$ in the bottom right, because it is persymmetric. Its Schur complement is $\gamma(0) - \gamma_k^\top \Gamma_k^{-1}\gamma_k = v_k$, so $v_k = \det\Gamma_{k+1}/\det\Gamma_k > 0$. By Claim 2, $1 - a_k^2 = v_k/v_{k-1} \in (0, 1]$, so $|a_k| < 1$. $\square$

**Claim 4 (the fitted model is causal).** If the data are not all equal, then every root $\zeta$ of $\hat\phi(z) = 1 - \hat\phi_{p1} z - \cdots - \hat\phi_{pp} z^p$ satisfies $|\zeta| > 1$.

*Proof.* The function $\hat\gamma$ (0 for $|h| \ge n$) is even and nonnegative definite, by the computation in Claim 3 for every $k$. So it is the autocovariance of a stationary Gaussian process $\{Y_t\}$ with mean 0 (Brockwell and Davis 1991, Section 1.5). Work in the complex space $L^2$ with $\lVert W \rVert^2 = \mathbb{E}|W|^2$. Because $\hat\Gamma_p$ is real, symmetric and positive definite, the vector $\hat\phi_p$ is the unique minimizer over $b \in \mathbb{C}^p$ of $\lVert Y_t - \sum_{j=1}^p b_j Y_{t-j} \rVert^2$, and the minimum is $v_p$.

Let $\zeta$ be a root, and write $\hat\phi(z) = (1 - z/\zeta)\, c(z)$ with $c(z) = 1 + c_1 z + \cdots + c_{p-1} z^{p-1}$. Put $U_t = c(B) Y_t$. Its variance $s = \lVert U_t \rVert^2$ does not depend on $t$ and is positive, because $c \ne 0$ and $\hat\Gamma_p$ is positive definite. For any $\lambda \in \mathbb{C}$, $U_t - \lambda U_{t-1} = c(B)(1 - \lambda B) Y_t$ is of the form $Y_t - \sum_{j=1}^{p} b_j Y_{t-j}$, so

$$g(\lambda) = \lVert U_t - \lambda U_{t-1} \rVert^2 \ge v_p, \quad \text{with equality at } \lambda = 1/\zeta.$$

The function $g$ is a strictly convex quadratic in $\lambda$, with the unique minimizer $\lambda^* = \mathbb{E}[U_t \overline{U_{t-1}}]/s$ and minimum $g(\lambda^*) = s(1 - |\lambda^*|^2)$. Since $1/\zeta$ attains the smallest possible value $v_p$, it is the minimizer: $1/\zeta = \lambda^*$. By the Cauchy-Schwarz inequality, $|\lambda^*| \le 1$. If $|\lambda^*| = 1$, then $v_p = g(\lambda^*) = 0$, which contradicts Claim 3. So $|1/\zeta| < 1$, that is $|\zeta| > 1$. $\square$

**Claim 5 (exact arithmetic).** Lines L1 to L9 use only addition, subtraction, multiplication and division. On rational inputs in exact rational arithmetic they return the exact solution $\hat\Gamma_p^{-1}\hat\gamma_p$ and the exact $\hat\sigma^2 = v_p$.

*Proof.* Claims 2 and 3 show that each step is defined and computes the stated quantities, and no step uses a square root or a comparison other than the positivity checks. $\square$

The tests check Claim 2 against Gaussian elimination in `Fraction` arithmetic, Claim 1 with exact autocovariances of four AR models (the recursion returns the true $\phi$, $v_p = \sigma^2$, and a PACF that is 0 after lag $p$), Claim 3 through $|\hat\phi_{kk}| < 1$ on random data, and the worked example in exact arithmetic.

**Cited, not proved here.** For a causal AR($p$) process with IID noise of finite variance, $\sqrt{n}(\hat\phi_p - \phi) \to N(0, \sigma^2\Gamma_p^{-1})$, $\hat\sigma^2 \to \sigma^2$ in probability, and for $h > p$, $\sqrt{n}\,\hat\phi_{hh} \to N(0, 1)$ (Brockwell and Davis 1991, Sections 8.2 and 8.10). The simulations on the page measure the finite-sample behaviour.
