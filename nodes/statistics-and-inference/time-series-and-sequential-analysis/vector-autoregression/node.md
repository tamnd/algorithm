---
tag: 5NRXN8
kind: model
slug: vector-autoregression
name: Vector autoregression
aliases:
- VAR model
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: An autoregressive model for a vector of series, in which each series depends on lags of all of them. It is fitted equation by equation with least squares.
history:
  year: 1980
  people: [Christopher A. Sims]
  note: Vector autoregressions go back to Quenouille (1957) and Whittle (1963). Sims (1980) proposed small unrestricted VARs, with impulse responses and variance decompositions, as an alternative to large structural macroeconomic models.
prereqs: [autoregressive-model, ordinary-least-squares, covariance-matrix]
see_also: [granger-causality, johansen-test, impulse-response, cholesky-decomposition, generalized-least-squares, spectral-radius, state-space-model, akaike-information-criterion]
sources:
  - paper: doi:10.2307/1912017
    title: Christopher A. Sims, Macroeconomics and reality, Econometrica 48(1) (1980), pages 1 to 48
    locator: the case for unrestricted VARs, orthogonalized impulse responses and variance decompositions
  - book: isbn:9783540401728
    title: Helmut Lütkepohl, New Introduction to Multiple Time Series Analysis, Springer, 2005
    locator: Chapter 2 (stable VAR processes, the companion form, Granger causality, impulse responses and variance decompositions), Chapter 3 (least squares and maximum likelihood estimation and their asymptotic laws) and Chapter 4 (order selection)
  - book: isbn:9780691042893
    title: James D. Hamilton, Time Series Analysis, Princeton University Press, 1994
    locator: Chapter 10 (covariance-stationary vector processes) and Chapter 11 (vector autoregressions)
  - paper: doi:10.1080/01621459.1962.10480664
    title: Arnold Zellner, An efficient method of estimating seemingly unrelated regressions and tests for aggregation bias, Journal of the American Statistical Association 57(298) (1962), pages 348 to 368
    locator: generalized least squares for a system of regressions, which reduces to equation-by-equation least squares when all equations have the same regressors
  - paper: doi:10.2307/2938337
    title: Christopher A. Sims, James H. Stock and Mark W. Watson, Inference in linear time series models with some unit roots, Econometrica 58(1) (1990), pages 113 to 144
    locator: which Wald tests in a VAR in levels keep their standard limit laws when the series have unit roots
  - paper: doi:10.1257/0002828053828518
    title: Òscar Jordà, Estimation and inference of impulse responses by local projections, American Economic Review 95(1) (2005), pages 161 to 182
    locator: impulse responses estimated by one regression per horizon instead of by iterating a VAR
  - paper: doi:10.1080/07350015.1986.10509491
    title: Robert B. Litterman, Forecasting with Bayesian vector autoregressions, five years of experience, Journal of Business and Economic Statistics 4(1) (1986), pages 25 to 38
    locator: the Minnesota prior that shrinks each equation toward a random walk
---

A vector autoregression of order $p$, VAR($p$), models $K$ series together: each series at time $t$ is a linear function of the last $p$ values of all $K$ series plus a noise term, $Y_t = c + A_1Y_{t-1} + \cdots + A_pY_{t-p} + \varepsilon_t$. It is the [autoregressive model](/autoregressive-model/) with vectors in place of numbers and matrices in place of coefficients. The model is stable, and has a stationary solution, exactly when the companion matrix has all eigenvalues inside the unit circle. Because every equation has the same regressors, [ordinary least squares](/ordinary-least-squares/) applied to each equation alone is already the efficient system estimate. Sims (1980) made the VAR the standard tool of empirical macroeconomics. Its outputs are forecasts, [Granger causality](/granger-causality/) tests, [impulse responses](/impulse-response/) and forecast error variance decompositions, and its error correction form is the setting of the [Johansen test](/johansen-test/) for [cointegration](/cointegration/).

## The machine

**Notation.** $Y_t \in \mathbb{R}^K$. The noise $\varepsilon_t$ is vector white noise, $\varepsilon_t \sim \mathrm{WN}(0, \Sigma)$: $\mathbb{E}\varepsilon_t = 0$, $\mathbb{E}\varepsilon_t\varepsilon_t^\top = \Sigma$ positive definite, and $\mathbb{E}\varepsilon_t\varepsilon_s^\top = 0$ for $s \neq t$. With the backshift $B$, write $A(z) = I_K - A_1z - \cdots - A_pz^p$, so the model is
$$A(B)Y_t = c + \varepsilon_t.$$
The univariate polynomial $\phi(z)$ of the AR model becomes the matrix polynomial $A(z)$, and its roots become the roots of $\det A(z)$.

**Parameters.** The intercept $c \in \mathbb{R}^K$, the coefficient matrices $A_1, \dots, A_p \in \mathbb{R}^{K \times K}$ with $A_p \neq 0$, and $\Sigma$. That is $K + K^2p + K(K + 1)/2$ numbers. Entry $(i, j)$ of $A_\ell$ is the effect of $Y_{j, t-\ell}$ on $Y_{it}$ with all other lags held fixed.

**Companion form.** Stack $\xi_t = (Y_t^\top, Y_{t-1}^\top, \dots, Y_{t-p+1}^\top)^\top \in \mathbb{R}^{Kp}$. Then $\xi_t = \bar c + F\xi_{t-1} + v_t$ with
$$F = \begin{pmatrix} A_1 & A_2 & \cdots & A_{p-1} & A_p \\ I_K & 0 & \cdots & 0 & 0 \\ 0 & I_K & \cdots & 0 & 0 \\ \vdots & & \ddots & & \vdots \\ 0 & 0 & \cdots & I_K & 0 \end{pmatrix}, \qquad v_t = \begin{pmatrix} \varepsilon_t \\ 0 \\ \vdots \\ 0\end{pmatrix},$$
and $\bar c = (c^\top, 0, \dots, 0)^\top$. Every VAR($p$) is a VAR(1) in $Kp$ dimensions, and every AR($p$) is the case $K = 1$.

**Stability.** The VAR is stable when $\det A(z) \neq 0$ for all complex $|z| \le 1$. Theorem 1 below proves that this holds exactly when the [spectral radius](/spectral-radius/) of $F$ is below 1, and that then $Y_t = \mu + \sum_{j \ge 0}\Psi_j\varepsilon_{t-j}$ is the unique stationary solution with $\varepsilon_t$ uncorrelated with the past, where $\mu = A(1)^{-1}c$ and the $\Psi_j$ decay geometrically. If $\det A(1) = 0$, the process has a unit root; with $\Pi = -A(1)$ of rank $r$, $0 < r < K$, the series are cointegrated, and the model is written in error correction form $\nabla Y_t = c + \Pi Y_{t-1} + \sum_{i=1}^{p-1}\Gamma_i\nabla Y_{t-i} + \varepsilon_t$ with $\Gamma_i = -(A_{i+1} + \cdots + A_p)$.

**A worked case.** Take $K = 2$, $p = 1$, $c = 0$,
$$A_1 = \begin{pmatrix} 0.5 & 0.2 \\ 0.3 & 0.4\end{pmatrix}, \qquad \Sigma = \begin{pmatrix} 1 & 0.5 \\ 0.5 & 1\end{pmatrix}.$$
Then $\det(I - A_1z) = 1 - 0.9z + 0.14z^2 = (1 - 0.7z)(1 - 0.2z)$, with roots $1/0.7$ and $5$, both outside the unit circle; the eigenvalues of $F = A_1$ are $0.7$ and $0.2$. The model is stable. Its variance $\Gamma(0)$ solves $\Gamma(0) = A_1\Gamma(0)A_1^\top + \Sigma$, a linear system of 4 equations in the entries:
$$\Gamma(0) = \begin{pmatrix} 7675/4386 & 10675/8772 \\ 10675/8772 & 30275/17544\end{pmatrix} \approx \begin{pmatrix} 1.750 & 1.217 \\ 1.217 & 1.726\end{pmatrix},$$
and $\Gamma(1) = \mathbb{E}Y_tY_{t-1}^\top = A_1\Gamma(0) \approx \begin{pmatrix} 1.118 & 0.954 \\ 1.012 & 1.055\end{pmatrix}$.

## What it counts

| quantity | formula | cost from the parameters |
|---|---|---|
| moving average weights | $\Psi_0 = I$, $\Psi_j = \sum_{i=1}^{\min(j, p)}A_i\Psi_{j-i}$; equivalently $\Psi_j = JF^jJ^\top$ with $J = (I_K, 0, \dots, 0)$ | $O(K^3p)$ per lag |
| mean | $\mu = A(1)^{-1}c$ | $O(K^3)$ |
| autocovariances | $\operatorname{vec}\Gamma_\xi(0) = (I - F \otimes F)^{-1}\operatorname{vec}\Sigma_v$ with $\Sigma_v = J^\top\Sigma J$, then $\Gamma(h) = \sum_{i=1}^pA_i\Gamma(h - i)$ for $h \ge 1$ (the multivariate [Yule-Walker equations](/yule-walker-equations/)) | $O(K^6p^6)$ directly, $O(K^3p^3)$ by a Schur method, then $O(K^3p)$ per lag |
| forecasts | $\hat Y_{T+h} = c + \sum_iA_i\hat Y_{T+h-i}$, with $\hat Y_s = Y_s$ for $s \le T$ | $O(K^2p)$ per step |
| forecast error covariance | $\sum_{j=0}^{h-1}\Psi_j\Sigma\Psi_j^\top$ | $O(hK^3)$ |
| impulse responses | $\Psi_j$; orthogonalized $\Theta_j = \Psi_jP$ with $\Sigma = PP^\top$ the [Cholesky factor](/cholesky-decomposition/) | $O(K^3)$ per lag |
| variance decomposition | share of shock $k$ in the $h$-step error of series $i$: $\sum_{j<h}(\Theta_j)_{ik}^2 \big/ \sum_{j<h}\sum_l(\Theta_j)_{il}^2$ | $O(hK^3)$ |
| spectral density | $f(\omega) = \frac{1}{2\pi}A(e^{-i\omega})^{-1}\Sigma A(e^{-i\omega})^{-*}$ | $O(K^2p + K^3)$ per frequency |

**Impulse responses depend on the order.** In the worked case, $\Psi_1 = A_1$ and $\Psi_2 = A_1^2 = \begin{pmatrix}0.31 & 0.18 \\ 0.27 & 0.22\end{pmatrix}$: a unit change in $\varepsilon_{1t}$ alone moves $Y_{1, t+2}$ by 0.31 and $Y_{2, t+2}$ by 0.27. But the errors are correlated, so a change in $\varepsilon_1$ alone is not a typical event. The Cholesky factor in the order $(Y_1, Y_2)$ is $P = \begin{pmatrix}1 & 0 \\ 0.5 & 0.866\end{pmatrix}$: the first orthogonal shock moves $Y_1$ by 1 and $Y_2$ by 0.5 on impact, and the second moves only $Y_2$. In the order $(Y_2, Y_1)$ the impact matrix is $\begin{pmatrix}0.866 & 0.5 \\ 0 & 1\end{pmatrix}$: now a shock to $Y_2$ also moves $Y_1$ by 0.5 on impact, and the other shock moves only $Y_1$. The variance decompositions change with it. At $h = 2$, the order $(Y_1, Y_2)$ attributes 97.8% of $Y_1$'s forecast error to its own shock; the order $(Y_2, Y_1)$ attributes 67.5%. The data cannot tell the two orders apart, because both give the same $\Sigma$. The order is an assumption about which variable can react to which within one period.

## Relation to other models

- **[Autoregressive model](/autoregressive-model/).** The case $K = 1$. Each equation of a VAR is an autoregressive distributed lag regression.
- **VARMA.** Adding a matrix moving average part gives VARMA($p$, $q$). It is more parsimonious, but its parameters are not identified without extra rules (echelon forms), which is why practice uses VARs. A stable VAR is a VMA($\infty$), and an invertible VARMA is a VAR($\infty$), which a VAR($p$) with $p$ growing slowly approximates.
- **[State space model](/state-space-model/).** The companion form is a state space model with state $\xi_t$ and no observation noise. The [Kalman filter](/kalman-filter/) then handles missing values and mixed frequencies.
- **Error correction form and [cointegration](/cointegration/).** A VAR with unit roots and $\operatorname{rank}\Pi = r$ is a vector error correction model. The [Johansen test](/johansen-test/) estimates $r$ by reduced rank regression, and the [Engle-Granger test](/engle-granger-test/) checks one relation.
- **Seemingly unrelated regressions.** A VAR is a system of regressions with correlated errors and identical regressors. Zellner's (1962) GLS for such systems reduces to OLS here (Theorem 2). With zero restrictions that differ across equations, it does not.
- **Structural VAR.** $B_0Y_t = d + B_1Y_{t-1} + \cdots + u_t$ with uncorrelated structural shocks $u_t$. The reduced form is the VAR with $A_i = B_0^{-1}B_i$, $\Sigma = B_0^{-1}\operatorname{Var}(u_t)B_0^{-\top}$. Recursive (Cholesky), long-run, sign and external-instrument restrictions are different ways to pick $B_0$.
- **Local projections.** Jordà (2005) estimates the response at horizon $h$ by regressing $Y_{t+h}$ on $Y_t, \dots, Y_{t-p+1}$ directly, one regression per $h$. Under a correct VAR both target the same $\Psi_h$; local projections are less efficient but more robust to a wrong lag order.

## Known results in the model

**Theorem 1 (stability and the companion matrix).** (a) $\det(I_{Kp} - Fz) = \det A(z)$ for all $z$. Hence the roots of $\det A(z)$ are exactly the reciprocals $1/\lambda$ of the nonzero eigenvalues $\lambda$ of $F$, and $\det A(z) \neq 0$ on $|z| \le 1$ if and only if every eigenvalue of $F$ has $|\lambda| < 1$. (b) If every eigenvalue of $F$ has $|\lambda| < 1$, then $Y_t = \mu + \sum_{j \ge 0}\Psi_j\varepsilon_{t-j}$, with $\mu = A(1)^{-1}c$ and $\Psi_j = JF^jJ^\top$, converges in mean square, solves the model, and is stationary. It is the only stationary solution in which $\varepsilon_t$ is uncorrelated with $Y_s$ for $s < t$. (c) If some eigenvalue of $F$ has $|\lambda| \ge 1$, there is no stationary solution with $\varepsilon_t$ uncorrelated with the past.

*Proof.* (a) Split $M(z) = I_{Kp} - Fz$ into the first block row and column and the rest: $M_{11} = I - A_1z$, $M_{12} = (-A_2z, \dots, -A_pz)$, $M_{21} = (-zI, 0, \dots, 0)^\top$, and $D$ is block lower bidiagonal with $I$ on the diagonal and $-zI$ below it, so $\det D = 1$. The Schur complement formula gives $\det M = \det D\,\det(M_{11} - M_{12}D^{-1}M_{21})$. Solving $Du = M_{21}$ block by block gives $u_1 = -zI$ and $u_k = zu_{k-1}$, so $u_k = -z^kI$. Then $M_{12}u = \sum_{i=2}^p(-A_iz)(-z^{i-1}I) = \sum_{i=2}^pA_iz^i$ and $M_{11} - M_{12}u = I - \sum_{i=1}^pA_iz^i = A(z)$. For $\lambda \neq 0$, $\det(\lambda I - F) = \lambda^{Kp}\det(I - F/\lambda) = \lambda^{Kp}\det A(1/\lambda)$, so $\lambda$ is an eigenvalue if and only if $1/\lambda$ is a root; $z = 0$ is never a root since $\det A(0) = 1$.

(b) Since $A(1)$ is invertible, $X_t = Y_t - \mu$ satisfies the model with $c = 0$, so take $c = 0$. With $r$ strictly between the spectral radius $\rho(F)$ and 1, Gelfand's formula gives a constant $C$ with $\lVert F^j\rVert \le Cr^j$. Then $\mathbb{E}\lVert F^jv_{t-j}\rVert^2 \le C^2r^{2j}\operatorname{tr}\Sigma$, so $\xi_t = \sum_{j\ge0}F^jv_{t-j}$ converges in mean square. It satisfies $\xi_t = F\xi_{t-1} + v_t$ term by term, its mean is 0 and its covariances $\sum_jF^{j+h}\Sigma_vF^{j\top}$ do not depend on $t$, and it is uncorrelated with later $v$. Its first block is $Y_t = \sum_jJF^jJ^\top\varepsilon_{t-j}$, because $v_t = J^\top\varepsilon_t$. For uniqueness, let $\xi'_t$ be any stationary solution with $\varepsilon_t$ uncorrelated with the past. Iterating $k$ times, $\xi'_t = F^k\xi'_{t-k} + \sum_{j<k}F^jv_{t-j}$, and $\mathbb{E}\lVert F^k\xi'_{t-k}\rVert^2 \le C^2r^{2k}\mathbb{E}\lVert\xi'_0\rVert^2 \to 0$. So $\xi'_t = \xi_t$ in mean square.

(c) Let $|\lambda| \ge 1$ and $w \neq 0$ with $w^*F = \lambda w^*$. Write $w = (w_1, \dots, w_p)$ in blocks. The block equations are $w_1^*A_k + w_{k+1}^* = \lambda w_k^*$ for $k < p$ and $w_1^*A_p = \lambda w_p^*$. If $w_1 = 0$, the last one gives $w_p = 0$ and then, going up, all $w_k = 0$; so $w_1 \neq 0$. Let $x_t = w^*\xi_t$. Then $x_t = \lambda x_{t-1} + w_1^*\varepsilon_t$ (plus a constant, which does not change variances). If $\xi_t$ were stationary with $\varepsilon_t$ uncorrelated with $\xi_{t-1}$, then $s = \mathbb{E}|x_t - \mathbb{E}x_t|^2$ would satisfy $s = |\lambda|^2s + w_1^*\Sigma w_1$ with $w_1^*\Sigma w_1 > 0$, so $s(1 - |\lambda|^2) > 0$, which is impossible for $|\lambda| \ge 1$. $\square$

The AR(2) model $X_t = 1.2X_{t-1} - 0.35X_{t-2} + \varepsilon_t$ is a check of part (a) with $K = 1$: $F = \begin{pmatrix}1.2 & -0.35 \\ 1 & 0\end{pmatrix}$ has eigenvalues 0.7 and 0.5, and $1 - 1.2z + 0.35z^2 = (1 - 0.7z)(1 - 0.5z)$.

**Theorem 2 (equation-by-equation OLS is GLS and the Gaussian MLE).** Write the $T$ equations as $Y = XB + E$, with $Y$ of size $T \times K$, the common regressor matrix $X$ of size $T \times m$ (a column of ones and the $p$ lags, $m = 1 + Kp$) of full column rank, and rows of $E$ uncorrelated with covariance $\Sigma$. (a) The GLS estimate of the stacked system $\operatorname{vec}Y = (I_K \otimes X)\operatorname{vec}B + \operatorname{vec}E$, $\operatorname{Cov}(\operatorname{vec}E) = \Sigma \otimes I_T$, is $\hat B = (X^\top X)^{-1}X^\top Y$, which is OLS on each equation, for every positive definite $\Sigma$. (b) For Gaussian errors and conditional on the first $p$ observations, the maximum likelihood estimates are $\hat B$ and $\hat\Sigma = \hat E^\top\hat E/T$ with $\hat E = Y - X\hat B$.

*Proof.* (a) Using $(P \otimes Q)(R \otimes S) = PR \otimes QS$ and $(P \otimes Q)^{-1} = P^{-1} \otimes Q^{-1}$,
$$\left[(I \otimes X)^\top(\Sigma^{-1} \otimes I)(I \otimes X)\right]^{-1}(I \otimes X)^\top(\Sigma^{-1} \otimes I) = (\Sigma^{-1} \otimes X^\top X)^{-1}(\Sigma^{-1} \otimes X^\top) = (\Sigma \otimes (X^\top X)^{-1})(\Sigma^{-1} \otimes X^\top) = I \otimes (X^\top X)^{-1}X^\top,$$
and $(I \otimes (X^\top X)^{-1}X^\top)\operatorname{vec}Y = \operatorname{vec}((X^\top X)^{-1}X^\top Y)$. $\Sigma$ has dropped out. (b) The conditional log-likelihood is $-\frac{T}{2}\log\det\Sigma - \frac12\operatorname{tr}(\Sigma^{-1}(Y - XB)^\top(Y - XB))$ plus a constant. Since $X^\top\hat E = 0$, $(Y - XB)^\top(Y - XB) = \hat E^\top\hat E + (B - \hat B)^\top X^\top X(B - \hat B)$, and the second term is positive semidefinite, so for every $\Sigma$ the trace is smallest at $B = \hat B$. With $B = \hat B$, maximizing over $\Sigma$ gives $\hat\Sigma = \hat E^\top\hat E/T$, the standard result for a Gaussian covariance. $\square$

In a fixed-regressor setting, (a) and the Gauss-Markov theorem for [generalized least squares](/generalized-least-squares/) make $\hat B$ the best linear unbiased estimate. In a VAR the regressors are lagged $Y$, so $\hat B$ is biased in small samples (toward less persistence, like the AR(1) estimate), and its optimality is asymptotic.

**Asymptotic law (cited).** If the VAR is stable and $\varepsilon_t$ is IID (or a martingale difference with bounded fourth moments) with covariance $\Sigma$, then $\sqrt T(\operatorname{vec}\hat B - \operatorname{vec}B) \to N(0, \Sigma \otimes Q^{-1})$ with $Q = \operatorname{plim}X^\top X/T$, and $\hat\Sigma \to \Sigma$ in probability (Lütkepohl 2005, Chapter 3; Hamilton 1994, Chapter 11). So Wald tests of linear restrictions, such as Granger noncausality, are asymptotically chi-square. With unit roots, $\hat B$ is still consistent, but Wald tests on coefficients that cannot be written as coefficients of stationary regressors have nonstandard laws (Sims, Stock and Watson 1990). The [Granger causality](/granger-causality/) page measures this in a simulation and gives the Toda-Yamamoto fix.

**A simulated fit.** With seed 2026, simulate 200 points from the worked case (after a burn-in of 100) and fit a VAR(1) with intercept by OLS on 199 rows. The estimates are $\hat A_1 = \begin{pmatrix}0.659 & 0.090 \\ 0.351 & 0.382\end{pmatrix}$, with standard errors about 0.07 for each entry, and $\hat\Sigma = \begin{pmatrix}0.921 & 0.442 \\ 0.442 & 1.052\end{pmatrix}$. The eigenvalues of $\hat A_1$ are 0.746 and 0.295. The entry 0.659 is more than two standard errors from 0.5, which is the sampling noise of one draw, not a property of the method.

**Order selection.** The lag order $p$ is chosen by the [Akaike information criterion](/akaike-information-criterion/) $\log\det\hat\Sigma_p + 2pK^2/T$, by Hannan-Quinn, or by the [Bayesian information criterion](/bayesian-information-criterion/) $\log\det\hat\Sigma_p + pK^2\log T/T$, or by sequential likelihood ratio tests. For a finite true order, BIC and Hannan-Quinn are consistent and AIC overestimates the order with positive probability (Lütkepohl 2005, Chapter 4). Too few lags leave correlated residuals and bias every derived quantity, so check the residuals with a multivariate portmanteau test.

**Dimension.** The number of coefficients, $K^2p$, grows fast: $K = 7$ and $p = 4$ give 196 coefficients besides the intercepts. Large VARs need shrinkage, such as the Minnesota prior of Bayesian VARs, which pulls each equation toward a random walk (Litterman 1986), or factor models.

**Forecasting.** The forecasts above are the best linear forecasts for a stable VAR with known parameters, and their error covariance tends to $\Gamma(0)$ as $h$ grows. With estimated parameters the forecast error has an extra term of order $1/T$.

## References
