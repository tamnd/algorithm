---
tag: A3NRM4
kind: algorithm
slug: generalized-least-squares
name: Generalized least squares
aliases:
- Aitken estimator
- feasible generalized least squares
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: Least squares after whitening by the error covariance, b = (X^T V^(-1) X)^(-1) X^T V^(-1) y. It is best linear unbiased for known V; with V estimated it is feasible GLS.
model: real-ram
complexity:
  vars: {n: the number of observations, p: "the number of columns of X, with p <= n"}
  time: {worst: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n^2)}
  flops: {worst: "n^3/3 + (p + 1) n^2 + 2n p^2 + O(p^3)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1935
  people: [Alexander C. Aitken]
  note: Aitken showed that least squares weighted by the inverse covariance matrix of the errors gives the minimum variance linear unbiased estimate, which extends the Gauss-Markov theorem to correlated errors.
prereqs: [weighted-least-squares, ordinary-least-squares, gauss-markov-theorem, cholesky-decomposition, covariance-matrix]
see_also: [autoregressive-model, durbin-watson-test, generalized-estimating-equations, linear-mixed-model, heteroscedasticity-consistent-standard-errors, cluster-robust-standard-errors, kalman-filter, positive-definite-matrix]
sources:
  - paper: doi:10.1017/S0370164600014346
    title: "A. C. Aitken, On least squares and linear combination of observations, Proceedings of the Royal Society of Edinburgh 55, 1935 (volume dated 1936), pp. 42 to 48"
    locator: The whole paper (the estimator weighted by the inverse covariance and its minimum variance among linear unbiased estimators)
  - paper: doi:10.1214/aoms/1177698505
    title: "William Kruskal, When are Gauss-Markov and least squares estimators identical? A coordinate-free approach, Annals of Mathematical Statistics 39(1), 1968, pp. 70 to 75"
    locator: The whole paper (ordinary and generalized least squares agree for every response exactly when the covariance maps the column space of X into itself)
  - paper: "S. J. Prais and C. B. Winsten, Trend estimators and serial correlation, Cowles Commission Discussion Paper Statistics No. 383, Chicago, 1954"
    locator: The whole paper (the AR(1) transformation that keeps the first observation)
  - paper: doi:10.1080/01621459.1949.10483290
    title: "D. Cochrane and G. H. Orcutt, Application of least squares regression to relationships containing auto-correlated error terms, Journal of the American Statistical Association 44(245), 1949, pp. 32 to 61"
    locator: The whole paper (least squares on differences with an estimated autocorrelation of the errors)
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: Chapter 3 (generalized least squares as least squares after a change of variables)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 4.2 (the Cholesky factorization of a positive definite matrix) and Section 5.3 (the full-rank least squares problem by QR)
---

Generalized least squares (GLS) fits $y = Xb + \varepsilon$ when the errors are correlated or have unequal variances with a known pattern, $\operatorname{Cov}(\varepsilon) = \sigma^2V$. It minimizes $(y - X\beta)^\top V^{-1}(y - X\beta)$, and the solution is $\hat b = (X^\top V^{-1}X)^{-1}X^\top V^{-1}y$, the Aitken estimator. The computation never forms $V^{-1}$: it factors $V = LL^\top$, multiplies the model by $L^{-1}$ so that the new errors are uncorrelated with equal variance, and runs [ordinary least squares](/ordinary-least-squares/) on the result. For a known $V$ this is the best linear unbiased estimator. When $V$ is estimated from the data, the same steps give feasible GLS.

## In plain words

Ordinary least squares treats every observation as a fresh, independent piece of information with the same noise. Often that is false: measurements taken one after the other share part of their noise, and measurements from the same unit are alike. Correlated points carry less information than their number suggests, and noisy points should count less. Generalized least squares fixes both at once. It changes the data with a fixed linear map so that the noise of the changed data is plain, independent and equal in size, then fits the ordinary way. For a series where each error carries part of the previous one, the map is simple: subtract a fraction of the previous point from each point.

## The problem

**Model.** $y = Xb + \varepsilon$ with $X$ a fixed real $n \times p$ matrix of rank $p$ (the intercept is one of the $p$ columns, as on the [hat matrix](/hat-matrix/) page), $\mathrm E[\varepsilon] = 0$ and

$$\operatorname{Cov}(\varepsilon) = \sigma^2 V, \qquad V \text{ known, symmetric and positive definite}, \quad \sigma^2 > 0 \text{ unknown}.$$

Here [positive definite](/positive-definite-matrix/) means $z^\top Vz > 0$ for every $z \ne 0$. A diagonal $V$ is the case of [weighted least squares](/weighted-least-squares/), with $w_i = 1/V_{ii}$.

**Input.** $X$, $y$ and $V$.

**Output.** $\hat b = (X^\top V^{-1}X)^{-1}X^\top V^{-1}y$, the whitened residual sum of squares $e^\top V^{-1}e$ with $e = y - X\hat b$, the estimate $s^2 = e^\top V^{-1}e/(n - p)$ and the covariance estimate $s^2(X^\top V^{-1}X)^{-1}$.

## The algorithm

```pseudo id=main
GENERALIZED-LEAST-SQUARES(X[1..n, 1..p], y[1..n], V[1..n, 1..n])
L1  L ← Cholesky factor of V                     ▷ V = L Lᵀ, L lower triangular; fails if V is not positive definite
L2  X̃ ← L⁻¹X;  ỹ ← L⁻¹y                          ▷ p + 1 forward substitutions
L3  (R, c) ← Householder QR of X̃, applied to ỹ    ▷ Qᵀ X̃ = (R; 0), c = Qᵀ ỹ
L4  b̂ ← solve R b = c[1..p] by back substitution
L5  RSS_V ← c[p+1]² + ... + c[n]²                 ▷ = eᵀ V⁻¹ e
L6  s² ← RSS_V / (n - p)
L7  C ← s² · R⁻¹ R⁻ᵀ                              ▷ = s² (Xᵀ V⁻¹ X)⁻¹
L8  return (b̂, RSS_V, s², C)
```

Line L2 is the whitening. Since $\operatorname{Cov}(L^{-1}\varepsilon) = \sigma^2L^{-1}VL^{-\top} = \sigma^2I$, the whitened model $\tilde y = \tilde Xb + \tilde\varepsilon$ has uncorrelated errors of equal variance, and $\|\tilde y - \tilde X\beta\|^2 = (y - X\beta)^\top V^{-1}(y - X\beta)$. Lines L3 to L7 are the QR solution of ordinary least squares on the whitened rows, and inherit its numerical stability. Inverting $V$ explicitly and then forming $X^\top V^{-1}X$ would cost as much and lose accuracy.

**Structured $V$.** For errors from a stationary AR(1) process, $V_{ts} = \rho^{|t-s|}/(1 - \rho^2)$, the inverse Cholesky factor is known in closed form: $L^{-1}$ multiplies the first row by $\sqrt{1 - \rho^2}$ and replaces row $t \ge 2$ by row $t$ minus $\rho$ times row $t - 1$. This is the Prais-Winsten transformation, and lines L1 and L2 then cost $O(np)$. For a general stationary [autoregressive model](/autoregressive-model/) the [Levinson-Durbin recursion](/levinson-durbin-recursion/) or a [Kalman filter](/kalman-filter/) gives the whitening in $O(n)$ per column, and Toeplitz methods ([Toeplitz system solving](/toeplitz-system-solving/)) handle a general stationary covariance.

## Example

Take $t = 1, \dots, 5$, $y = (2, 3, 5, 4, 6)$, the model $y_t = b_0 + b_1 t + u_t$, and AR(1) errors with $\rho = 3/5$, so $\sqrt{1 - \rho^2} = 4/5$ and the whitening is exact in rationals. Line L2 gives:

| $t$ | whitened intercept column | whitened $t$ | whitened $y$ |
|---|---|---|---|
| 1 | 4/5 | 4/5 | 8/5 |
| 2 | 2/5 | 7/5 | 9/5 |
| 3 | 2/5 | 9/5 | 16/5 |
| 4 | 2/5 | 11/5 | 1 |
| 5 | 2/5 | 13/5 | 18/5 |

Ordinary least squares on this table gives

$$\hat b = \Bigl(\tfrac{40}{37}, \tfrac{36}{37}\Bigr) \approx (1.081, 0.973),$$

against $(1.3, 0.9)$ from ordinary least squares on the raw data. The whitened residual sum of squares is $3622/925 \approx 3.9157$, so $s^2 = 1.3052$ with $n - p = 3$, $\operatorname{se}(\hat b_1) = 0.4696$, and the 95% interval for the slope is $0.973 \pm 3.1824 \cdot 0.4696 = (-0.521, 2.467)$. Five correlated points hold little information about a slope.

**Measured behavior.** With $t = 1, \dots, 30$, $y_t = 1 + 0.2t + u_t$ and stationary normal AR(1) errors with $\rho = 0.6$, $r = 1000$ samples from `random.Random(20261114)` gave these coverages of the nominal 95% t interval for the slope:

| method | coverage |
|---|---|
| GLS with the true $V$ | 0.946 |
| OLS with the usual standard error | 0.684 |
| two-step Prais-Winsten feasible GLS | 0.823 |

The GLS interval is exact by the theory below; the measured value is within Monte Carlo error. The variance of the OLS slope was 1.085 times that of the GLS slope (theory 1.084), so for a linear trend OLS loses little efficiency; the damage is in its standard error, which assumes independence and is far too small. Feasible GLS undercovers at $n = 30$ because $\hat\rho$ is biased toward 0 and its sampling error is ignored.

## Correctness

Line L1 succeeds because $V$ is positive definite. By the whitening identity above, lines L3 and L4 minimize $(y - X\beta)^\top V^{-1}(y - X\beta)$, and the normal equations of the whitened problem are $X^\top V^{-1}X\hat b = X^\top V^{-1}y$, so GLS equals OLS on whitened data. The whitened model satisfies the hypotheses of the [Gauss-Markov theorem](/gauss-markov-theorem/), and estimators linear in $y$ and in $L^{-1}y$ are the same class, so $\hat b$ is unbiased with covariance $\sigma^2(X^\top V^{-1}X)^{-1}$ and is best linear unbiased (Aitken's theorem). $s^2$ is unbiased for $\sigma^2$, and under normal errors the t intervals and F tests on the whitened model are exact. The proof also shows that the Prais-Winsten matrix is exactly $L^{-1}$ for the AR(1) covariance, by the uniqueness of the Cholesky factor, and proves Kruskal's condition below.

## Complexity

For a dense $V$, the Cholesky factor costs $n^3/3$ flops, the $p + 1$ forward substitutions $(p + 1)n^2$, the QR $2np^2 - 2p^3/3$ and the covariance $O(p^3)$: $\Theta(n^3)$ time and $\Theta(n^2)$ space for $V$ and $L$. Structure changes this. A diagonal $V$ is weighted least squares at $\Theta(np^2)$. AR(1) and banded $V$ with bandwidth $q$ cost $\Theta(nq^2 + nqp + np^2)$. A block diagonal $V$ with blocks of size $m$, as in repeated measures, costs $\Theta(nm^2 + np^2)$.

## Properties

- **Best linear unbiased.** For known $V$, $\operatorname{Cov}(\hat b) = \sigma^2(X^\top V^{-1}X)^{-1}$ is the smallest covariance, in the Loewner order, among linear unbiased estimators. OLS is still unbiased under correlation, but its covariance is $\sigma^2(X^\top X)^{-1}X^\top VX(X^\top X)^{-1}$, not $\sigma^2(X^\top X)^{-1}$.
- **Scale of $V$ does not matter.** $V$ and $cV$ give the same $\hat b$ and the same covariance estimate.
- **When OLS is already GLS.** Kruskal (1968): OLS equals GLS for every $y$ exactly when the column space of $VX$ equals that of $X$. An equicorrelated $V = (1 - c)I + c\mathbf 1\mathbf 1^\top$ with an intercept in $X$ is such a case, so a common shock shared by all observations does not change the estimate (but it does change which variances can be estimated).
- **Residuals.** The residuals $e = y - X\hat b$ are correlated even under the model. Diagnostics such as [leverage](/leverage-statistics/) and [studentized residuals](/studentized-residual/) belong on the whitened scale $L^{-1}e$.

## Variants and improvements

- **Feasible GLS.** $V = V(\theta)$ depends on a few unknown parameters. Estimate $\theta$ from OLS residuals, then run GLS with $V(\hat\theta)$. For AR(1) errors, $\hat\rho = \sum e_te_{t-1}/\sum e_t^2$ and the Prais-Winsten whitening give the two-step estimator of the implementation. Under regularity conditions feasible GLS has the same limiting distribution as GLS with the true $V$; in finite samples its reported standard errors are too small, as the table above shows.
- **Cochrane-Orcutt.** The older AR(1) method drops the first row and uses only the differences $y_t - \rho y_{t-1}$; in practice it is iterated between $\rho$ and $b$, and the iteration can stop at a local minimum. It loses one observation, which matters for short series and for trending regressors.
- **Joint estimation.** Maximum likelihood or restricted maximum likelihood estimates $b$ and $\theta$ together; for random effects this is the [linear mixed model](/linear-mixed-model/), whose fixed effects are GLS estimates given the variance components.
- **Sandwich standard errors instead of GLS.** Keep OLS and use [heteroscedasticity-consistent](/heteroscedasticity-consistent-standard-errors/) or [cluster-robust](/cluster-robust-standard-errors/) standard errors, which do not need $V$ but give up efficiency. [Generalized estimating equations](/generalized-estimating-equations/) combine both: a working $V$ for efficiency and a sandwich variance that stays valid when the working $V$ is wrong.

## When to use it

Use GLS when the error covariance is known up to a scale, or has a small parametric form that can be estimated well: serially correlated errors in a time series regression, a known measurement covariance in calibration, or blocks of correlated observations. Test for serial correlation first with the [Durbin-Watson test](/durbin-watson-test/) or the [Ljung-Box test](/ljung-box-test/) on the OLS residuals. If the form of $V$ is in doubt, prefer OLS or feasible GLS with a robust sandwich variance.

## Pitfalls

- **Inverting $V$.** Forming $V^{-1}$ explicitly is slower and less accurate than a Cholesky factor and two triangular solves.
- **Feasible GLS treated as GLS.** The standard errors from line L7 assume that $V$ is known. With an estimated $V$ they are too small in short series.
- **A wrong $V$.** GLS with a wrong $V$ stays unbiased if the regressors are fixed, but it is no longer best, and $s^2(X^\top V^{-1}X)^{-1}$ is the wrong covariance. Use a sandwich variance unless the model for $V$ is well checked.
- **Lagged dependent variables.** If $X$ contains $y_{t-1}$ and the errors are autocorrelated, OLS and feasible GLS are both inconsistent; the regressors are correlated with the errors. The fixed-$X$ theory of this page does not apply.
- **Strict exogeneity.** With correlated errors, GLS uses future and past regressors to predict each error. It needs $\mathrm E[\varepsilon_t \mid X] = 0$ for all regressor values, not only those at time $t$; OLS needs less.
- **Nearly singular $V$.** If $V$ is close to singular, the whitening amplifies rounding error, and the Cholesky factor may fail. Check the condition number of $V$, or use a model with a nonsingular covariance.

## Implementations

## History

Aitken (1935) proved that the estimator weighted by the inverse covariance is the minimum variance linear unbiased estimator. Cochrane and Orcutt (1949) applied the idea to time series regressions with autocorrelated errors by differencing with an estimated autocorrelation, and Prais and Winsten (1954) kept the first observation with the factor $\sqrt{1 - \rho^2}$, which makes the transformation the exact inverse Cholesky factor. Kruskal (1968) gave the coordinate-free condition under which ordinary least squares already equals the Aitken estimator.

## References
