---
tag: AA2XYN
kind: algorithm
slug: johansen-test
name: Johansen test
aliases:
- Johansen trace test
- Johansen cointegration test
area: statistics-and-inference/time-series-and-sequential-analysis
level: advanced
summary: Finds the number of cointegrating relations in a vector autoregression by the canonical correlations between differences and lagged levels.
model: real-ram
complexity:
  vars: {n: the length of the series, K: the number of series, p: the order of the vector autoregression}
  time: {worst: Θ(n K^2 p^2 + K^3), best: Θ(n K^2 p^2 + K^3)}
  space: {extra: Θ(n K p)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1988
  people: [Søren Johansen]
  note: Johansen (1988) derived the maximum likelihood estimator of the cointegrating vectors in a Gaussian vector autoregression by reduced rank regression, and the likelihood ratio tests for the cointegration rank. Johansen (1991) added deterministic terms.
prereqs: [vector-autoregression, cointegration, canonical-correlation-analysis, maximum-likelihood-estimation]
see_also: [engle-granger-test, generalized-eigenvalue-problem, cholesky-decomposition, jacobi-eigenvalue-algorithm, likelihood-ratio-test, augmented-dickey-fuller-test, granger-causality, symmetric-eigenproblem]
sources:
  - paper: doi:10.1016/0165-1889(88)90041-3
    title: Søren Johansen, Statistical analysis of cointegration vectors, Journal of Economic Dynamics and Control 12(2-3) (1988), pages 231 to 254
    locator: the reduced rank regression, the eigenvalue problem, and the limit law of the likelihood ratio statistic for the rank
  - paper: doi:10.2307/2938278
    title: Søren Johansen, Estimation and hypothesis testing of cointegration vectors in Gaussian vector autoregressive models, Econometrica 59(6) (1991), pages 1551 to 1580
    locator: the models with a constant and the trace and maximum eigenvalue statistics
  - paper: doi:10.1111/j.1468-0084.1992.tb00013.x
    title: Michael Osterwald-Lenum, A note with quantiles of the asymptotic distribution of the maximum likelihood cointegration rank test statistics, Oxford Bulletin of Economics and Statistics 54(3) (1992), pages 461 to 472
    locator: the simulated quantiles for the five cases of deterministic terms
  - paper: doi:10.1002/(SICI)1099-1255(199909/10)14:5<563::AID-JAE530>3.0.CO;2-R
    title: James G. MacKinnon, Alfred A. Haug and Leo Michelis, Numerical distribution functions of likelihood ratio tests for cointegration, Journal of Applied Econometrics 14(5) (1999), pages 563 to 577
    locator: the response surfaces for the quantiles and p-values of the trace and maximum eigenvalue statistics
  - book: isbn:9780691042893
    title: James D. Hamilton, Time Series Analysis, Princeton University Press, 1994
    locator: Chapter 20 (full-information maximum likelihood analysis of cointegrated systems)
  - book: isbn:9783540401728
    title: Helmut Lütkepohl, New Introduction to Multiple Time Series Analysis, Springer, 2005
    locator: the chapters on vector error correction models, their estimation by reduced rank regression, and tests of the cointegration rank
---

The Johansen test finds how many independent stationary linear combinations, or [cointegrating](/cointegration/) relations, a set of $K$ integrated series has. It writes a [vector autoregression](/vector-autoregression/) in error correction form, where the matrix $\Pi$ that multiplies the lagged levels has rank $r$ equal to the number of relations. The maximum likelihood estimate of a rank $r$ matrix comes from a generalized eigenvalue problem: the eigenvalues are the squared [canonical correlations](/canonical-correlation-analysis/) between the differences and the lagged levels, after both are cleaned of the short-run terms. The trace and maximum eigenvalue statistics are likelihood ratio statistics built from the small eigenvalues. Their null laws are nonstandard and depend on $K - r$ and on the deterministic terms. Unlike the [Engle-Granger test](/engle-granger-test/), the method treats all series alike and estimates all the relations at once.

## In plain words

Several series wander, but some mixtures of them may stay put. The test asks how many such mixtures exist. It first strips out the short-term wiggles. Then it looks for the mixtures of the levels that best predict the next changes. Each candidate mixture comes with a score between 0 and 1 that says how strongly it pulls the series back. Real long-run ties give large scores. Directions in which the series just wander give scores near 0. The test counts the scores that are too large to be chance, from the largest down, and stops at the first one that could be noise. The count is the number of long-run ties.

## The problem

**Model and hypotheses.** Let $Y_t \in \mathbb{R}^K$ follow a Gaussian VAR($p$), written in vector error correction form,
$$\nabla Y_t = \Pi Y_{t-1} + \sum_{i=1}^{p-1}\Gamma_i\nabla Y_{t-i} + \mu + \varepsilon_t, \qquad \varepsilon_t \text{ iid } N(0, \Omega),$$
with $\mu = 0$ (case "none") or $\mu$ free (case "c", an unrestricted constant, which gives linear trends in the levels). If $Y_t$ is I(1) with exactly $r$ cointegrating relations, then $\operatorname{rank}\Pi = r$ and $\Pi = \alpha\beta^\top$ with $\alpha, \beta$ of size $K \times r$. The columns of $\beta$ span the cointegrating vectors, and $\alpha$ holds the speeds of adjustment. The hypotheses are nested: $H(r)$: $\operatorname{rank}\Pi \le r$, for $r = 0, \dots, K$. $H(K)$ is the unrestricted VAR, and $H(0)$ is a VAR in differences.

**Statistic.** With $\hat\lambda_1 \ge \dots \ge \hat\lambda_K$ the eigenvalues of the problem in line L5 and $T$ the number of rows,
$$\mathrm{LR}_{\mathrm{trace}}(r) = -T\sum_{i=r+1}^{K}\log(1 - \hat\lambda_i), \qquad \mathrm{LR}_{\max}(r) = -T\log(1 - \hat\lambda_{r+1}).$$
The trace statistic is the likelihood ratio statistic for $H(r)$ against $H(K)$, and the maximum eigenvalue statistic tests $H(r)$ against $H(r + 1)$. Both facts are proved on the correctness page.

**Null distribution.** Asymptotic and nonstandard. Under $H(r)$ with exactly $r$ relations, $\mathrm{LR}_{\mathrm{trace}}(r)$ converges to the trace of a matrix functional of a $(K - r)$-dimensional Brownian motion,
$$\operatorname{tr}\left\{\int_0^1 dW\,F^\top\left(\int_0^1 FF^\top du\right)^{-1}\int_0^1 F\,dW^\top\right\},$$
where $F = W$ in case "none" and $F$ is a demeaned or trend-adjusted $W$ in the other cases (Johansen 1988, 1991). The limit does not depend on $\Omega$, $\alpha$, $\beta$ or $\Gamma_i$. It is cited, not proved here. The quantiles come from simulation: Osterwald-Lenum (1992) tabulated them, and MacKinnon, Haug and Michelis (1999) fitted response surfaces.

**Rejection rule and size.** Reject $H(r)$ when the statistic exceeds the quantile for $K - r$ and the case. The 95% points (MacKinnon, Haug and Michelis 1999):

| $K - r$ | trace, "none" | trace, "c" | max, "none" | max, "c" |
|---|---|---|---|---|
| 1 | 4.1296 | 3.8415 | 4.1296 | 3.8415 |
| 2 | 12.3212 | 15.4943 | 11.2246 | 14.2639 |
| 3 | 24.2761 | 29.7961 | 17.7961 | 21.1314 |
| 4 | 40.1749 | 47.8545 | 24.1592 | 27.5858 |
| 5 | 60.0627 | 69.8189 | 30.4428 | 33.8777 |

For $K - r = 1$ in case "c", the limit is $\chi^2(1)$, with 95% point $1.96^2 = 3.8415$, because the stochastic trend then has a drift that dominates. The rank is chosen by the sequential rule: test $r = 0, 1, \dots$ in turn and stop at the first $r$ that is not rejected. Each test has asymptotic size $\alpha$. For the true rank $r_0$, the procedure picks $\hat r < r_0$ with a probability that goes to 0, and $\hat r = r_0$ with probability tending to $1 - \alpha$.

**p-value.** MacKinnon, Haug and Michelis (1999) give response surface p-values. A Monte Carlo p-value from $K - r$ independent random walks is valid asymptotically for $r = 0$.

**Sensitivity and power.** The trace test has power against any larger rank, the maximum eigenvalue test against one more relation. A relation that adjusts slowly (small $\alpha$) gives a small $\hat\lambda$ and is hard to find. The finite-sample size is above nominal when $K$ or $p$ is large relative to $n$. Bartlett corrections or the bootstrap help there.

## The algorithm

```pseudo id=main
JOHANSEN(Y₁..Y_n ∈ ℝ^K, p, case, α)
L1  R0_t ← residual of ∇Y_t after OLS on ∇Y_{t−1}, …, ∇Y_{t−p+1} (and 1 in case "c")
L2  R1_t ← residual of Y_{t−1} after OLS on the same regressors
L3  S_ij ← (1/T) Σ_t R_i,t R_j,tᵀ for i, j ∈ {0, 1}
L4  L ← Cholesky factor of S11 (S11 = L Lᵀ)
L5  (λ_i, v_i) ← eigenpairs of C = L⁻¹ S10 S00⁻¹ S01 L⁻ᵀ, λ₁ ≥ … ≥ λ_K
L6  β ← L⁻ᵀ [v₁ … v_K];  α ← S01 β
L7  trace(r) ← −T Σ_{i>r} log(1 − λ_i);  max(r) ← −T log(1 − λ_{r+1})
L8  r̂ ← the first r with trace(r) < c_α(K − r, case), or K if none
L9  return (λ, trace, max, r̂, β[:, 1..r̂], α[:, 1..r̂])
```

Lines L4 to L6 turn the generalized problem $\det(\lambda S_{11} - S_{10}S_{00}^{-1}S_{01}) = 0$ into a symmetric eigenvalue problem, which a [Jacobi](/jacobi-eigenvalue-algorithm/) or QR eigensolver handles stably. The vectors satisfy $\beta^\top S_{11}\beta = I$. The estimate of $\Pi$ under $H(r)$ is $\hat\alpha_r\hat\beta_r^\top$ with the first $r$ columns. Since only the span of $\beta_r$ is identified, practice normalizes one entry of each vector to 1 for reporting.

## Example

**By hand.** Take $K = 2$, $n = 7$, $p = 1$ (no lagged differences), case "none", with $Y_1 = (1, 3, 2, 4, 3, 5, 4)$ and $Y_2 = (0, 2, 3, 3, 5, 4, 6)$. Then $T = 6$, $R_{0t} = \nabla Y_t$, $R_{1t} = Y_{t-1}$, and the moment matrices are integers over 6:

| step | value |
|---|---|
| L3: $T S_{00}$ | $\begin{pmatrix}15 & -3\\-3 & 14\end{pmatrix}$ |
| L3: $T S_{01}$ (rows: $\nabla Y$, columns: $Y_{t-1}$) | $\begin{pmatrix}0 & 7\\20 & 11\end{pmatrix}$ |
| L3: $T S_{11}$ | $\begin{pmatrix}64 & 59\\59 & 63\end{pmatrix}$ |
| L5: trace and determinant of $S_{11}^{-1}S_{10}S_{00}^{-1}S_{01}$ | $128672/110751$ and $19600/110751$ |
| L5: $\hat\lambda_1$, $\hat\lambda_2$ | 0.98151, 0.18031 |
| L6: $\hat\beta_1$, scaled so its first entry is 1 | $(1, -0.837)$ |
| L7: trace(0), trace(1) | 25.13, 1.19 |
| L7: max(0), max(1) | 23.94, 1.19 |
| L8: compare with 12.3212 and 4.1296 | reject $r = 0$, keep $r = 1$, so $\hat r = 1$ |

The denominator $110751 = 551 \cdot 201$ is $\det(TS_{11})\det(TS_{00})$. The factor $T$ cancels in the eigenvalues, so they are exact algebraic numbers, the roots of $z^2 - (128672/110751)z + 19600/110751$. With six rows the asymptotic quantiles are not reliable; the example only shows the steps.

**Three series with one relation.** With seed 2026, let $x_1$ and $x_2$ be independent Gaussian random walks of length 200, $u_t = 0.5u_{t-1} + \varepsilon_t$, and $y_t = x_{1t} - x_{2t} + u_t$. With $K = 3$, $p = 1$ and case "none" ($T = 199$):

| $r$ | $\hat\lambda_{r+1}$ | trace($r$) | 95% point | max($r$) | 95% point |
|---|---|---|---|---|---|
| 0 | 0.2836 | 77.99 | 24.28 | 66.36 | 17.80 |
| 1 | 0.0565 | 11.64 | 12.32 | 11.57 | 11.22 |
| 2 | 0.0003 | 0.06 | 4.13 | 0.06 | 4.13 |

The trace sequence stops at $\hat r = 1$, and the first vector, scaled, is $\hat\beta_1 = (1, -0.981, 1.015)$, close to the true $(1, -1, 1)$. The maximum eigenvalue test of $r = 1$ against $r = 2$ rejects narrowly (11.57 against 11.22), so the two rules disagree here. The Engle-Granger regression of $y$ on $x_1$ and $x_2$ gives slopes $0.993$ and $-1.055$ and $\tau = -7.92$, which also finds the relation.

**Size.** With two independent Gaussian random walks of length 200 and 2000 samples, the trace test of $r = 0$ at the 95% point 12.3212 rejected in 5.7% of samples, and the simulated 95% quantile was 12.74. With three walks it rejected in 6.2% at 24.2761. These rates are measured, not derived. With case "c" applied to walks without drift, it rejected in 11.8% at 15.4943. This shows the cost of a wrong deterministic case. With a drift of 0.3 per step, the case "c" rate fell to 6.5% in 1000 samples.

## Correctness

The correctness page proves that the procedure computes the Gaussian maximum likelihood estimate under each rank and the likelihood ratio statistics. First, the short-run terms are concentrated out by the Frisch-Waugh projection of lines L1 and L2. For fixed $\beta$ the best $\alpha$ and $\Omega$ are those of a regression of $R_0$ on $\beta^\top R_1$, and $\det\hat\Omega(\beta) = \det S_{00}\cdot\det\beta^\top(S_{11} - S_{10}S_{00}^{-1}S_{01})\beta/\det\beta^\top S_{11}\beta$. By the Poincaré separation theorem this ratio is minimized by the first $r$ generalized eigenvectors, with minimum $\det S_{00}\prod_{i \le r}(1 - \hat\lambda_i)$. The trace and maximum eigenvalue statistics follow as differences of $-T\log\det\hat\Omega$. The page also proves that the Cholesky reduction of lines L4 to L6 solves the generalized problem with $\beta^\top S_{11}\beta = I$, that $0 \le \hat\lambda_i \le 1$, that the eigenvalues are unchanged when $Y_t$ is replaced by $AY_t$ (and $AY_t + c$ in case "c") for invertible $A$, and that for $K = 1$, $\hat\lambda = t^2/(t^2 + T - 1)$ with $t$ the Dickey-Fuller t ratio. The asymptotic null laws are cited from Johansen (1988, 1991).

## Complexity

On a [real RAM](/real-ram/), lines L1 and L2 regress $2K$ columns on $q = K(p - 1) + d$ regressors ($d = 1$ in case "c"). A QR factorization of the regressors costs $\Theta(Tq^2)$ and the projections $\Theta(TqK)$. Line L3 costs $\Theta(TK^2)$. Lines L4 to L6 cost $\Theta(K^3)$ for the Cholesky factor and the products, and $O(K^3)$ per Jacobi sweep, with a number of sweeps that is small in practice. With $T \approx n$, the total is $\Theta(nK^2p^2 + K^3)$ time and $\Theta(nKp)$ space for the regressors.

**Numerical stability.** Do not form $S_{11}^{-1}S_{10}S_{00}^{-1}S_{01}$ and call a general eigensolver: that matrix is not symmetric and its eigenvectors can be badly conditioned. The Cholesky route keeps the problem symmetric. Levels that are far from 0 make $S_{11}$ badly conditioned in case "none"; scaling each series by its standard deviation changes no eigenvalue, by the invariance result. An eigenvalue that rounds to 1 makes $\log(1 - \lambda)$ infinite; it signals an exact fit, usually too many lags for the sample.

## Properties

- **Maximum likelihood.** Under Gaussian errors, $\hat\beta_r$ spans the maximum likelihood estimate of the cointegrating space, and it is superconsistent, with a mixed normal limit that gives $\chi^2$ tests of linear restrictions on $\beta$.
- **Symmetric in the variables.** No series has to be chosen as the dependent variable. The eigenvalues are invariant to invertible linear maps of $Y_t$.
- **All relations at once.** It estimates the rank and a basis of the cointegrating space, not a single vector.
- **Identification of the space only.** Any $\beta M$ with $M$ invertible fits as well; individual vectors need restrictions to be interpreted.
- **Depends on the deterministic case.** The five standard cases (no constant, restricted constant, unrestricted constant, restricted trend, unrestricted trend) have different null laws.
- **Generalizes Dickey-Fuller.** With $K = 1$ and no deterministic terms, the trace statistic is a monotone function of the squared Dickey-Fuller t ratio.

## Variants and improvements

- **Restricted constant and trends.** A constant inside the cointegrating relation ($\Pi Y_{t-1} + \mu = \alpha(\beta^\top Y_{t-1} + \rho_0)$) and a restricted linear trend avoid quadratic trends in the levels. They use $Y_{t-1}$ augmented by 1 or $t$ in line L2 and their own tables.
- **Bartlett correction.** Johansen (2002) scales the trace statistic by a factor that corrects its mean, which brings the size close to nominal in small samples.
- **Bootstrap.** A recursive residual bootstrap of the VECM under $H(r)$ gives finite-sample critical values.
- **Tests on $\beta$ and $\alpha$.** Linear restrictions on the cointegrating space or on the adjustment speeds are likelihood ratio tests with $\chi^2$ limits, computed by the same reduced rank regression on transformed data.
- **Information criteria.** The rank and the lag order can be chosen jointly by AIC or BIC.
- **Structural breaks.** Johansen, Mosconi and Nielsen (2000) allow for known break dates in the deterministic terms.

## When to use it

Use the Johansen test for three or more I(1) series, or for two when no series is a natural dependent variable, and when the number of relations is itself a question, as in money demand systems or term structures of interest rates. It needs a well-specified VAR: choose the lag order first (by AIC or BIC on the VAR in levels), check the residuals for autocorrelation, and choose the deterministic case from a plot of the series. For a single relation with a known dependent variable the Engle-Granger test is simpler. If a series may be stationary, test it with the [ADF](/augmented-dickey-fuller-test/) or [KPSS](/kpss-test/) test first, because a stationary series adds a trivial "relation".

## Pitfalls

- **Wrong deterministic case.** Using the unrestricted constant tables for series without drift inflated the size from 5% to about 12% in the example. Plot the data and choose the case before testing.
- **Lag order.** Too few lags leave autocorrelated errors and distort the size; too many cost power. The trace statistics can change by a lot with $p$.
- **Small samples.** The asymptotic quantiles are too small when $T$ is small relative to $Kp$, so the rank is overestimated. Use a Bartlett correction or a bootstrap.
- **Trace and max disagree.** The two statistics can point to different ranks, as in the example. Report both and the sequential trace choice.
- **Stationary series in the system.** A stationary variable makes a unit vector a cointegrating vector and raises the rank by one without any economic link.
- **Interpreting raw eigenvectors.** The vectors are only identified up to a basis change. Impose and test restrictions before reading off coefficients.
- **Rank zero is not "no relation found".** Failing to reject $r = 0$ may mean low power, especially when the adjustment is slow.

## Implementations

## History

Søren Johansen worked out the Gaussian likelihood analysis of cointegrated VARs in 1988, building on reduced rank regression (Anderson 1951) and canonical correlations (Hotelling 1936). Johansen and Katarina Juselius applied it to money demand in Denmark and Finland in 1990, and Johansen (1991) gave the full theory with deterministic terms. Osterwald-Lenum (1992) published the tables that most software used for years. MacKinnon, Haug and Michelis (1999) replaced them with response surfaces. Johansen's 1995 monograph collects the theory.

## References
