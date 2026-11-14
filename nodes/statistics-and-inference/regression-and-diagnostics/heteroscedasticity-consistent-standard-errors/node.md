---
tag: PTWW7S
kind: algorithm
slug: heteroscedasticity-consistent-standard-errors
name: Heteroscedasticity-consistent standard errors
aliases:
- sandwich estimator
- Huber-White standard errors
- Eicker-Huber-White standard errors
- robust standard errors
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: Estimate the covariance of least squares as (X^T X)^(-1) X^T diag(e_i^2) X (X^T X)^(-1), which stays consistent when the error variance varies.
model: real-ram
complexity:
  vars: {n: the number of observations, p: "the number of columns of X, with p < n"}
  time: {worst: Θ(n p^2), best: Θ(n p^2)}
  space: {extra: Θ(n p)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1967
  people: [Friedhelm Eicker, Peter J. Huber, Halbert White, James G. MacKinnon]
  note: Eicker (1967) and Huber (1967) proved the consistency of the sandwich covariance; White (1980) brought it to econometrics, and MacKinnon and White (1985) proposed the small sample corrections HC1 to HC3.
prereqs: [ordinary-least-squares, heteroscedasticity, hat-matrix, leverage-statistics, qr-decomposition]
see_also: [cluster-robust-standard-errors, weighted-least-squares, breusch-pagan-test, m-estimator, generalized-estimating-equations, jackknife-resampling, bootstrap-method, wald-test]
sources:
  - paper: "F. Eicker, Limit theorems for regressions with unequal and dependent errors, Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability, Volume 1, University of California Press, 1967, pp. 59 to 82"
    locator: The whole paper (consistency of the least squares covariance estimate built from squared residuals under unequal error variances)
  - paper: "P. J. Huber, The behavior of maximum likelihood estimates under nonstandard conditions, Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability, Volume 1, University of California Press, 1967, pp. 221 to 233"
    locator: The whole paper (the asymptotic covariance A^(-1) B A^(-T) of an M-estimate when the model is wrong)
  - paper: doi:10.2307/1912934
    title: "Halbert White, A heteroskedasticity-consistent covariance matrix estimator and a direct test for heteroskedasticity, Econometrica 48(4), 1980, pp. 817 to 838"
    locator: The whole paper (the estimator HC0 for least squares, its consistency, and the direct test)
  - paper: doi:10.1016/0304-4076(85)90158-7
    title: "James G. MacKinnon and Halbert White, Some heteroskedasticity-consistent covariance matrix estimators with improved finite sample properties, Journal of Econometrics 29(3), 1985, pp. 305 to 325"
    locator: The whole paper (HC1, HC2, the jackknife estimator and their small sample behavior)
  - paper: doi:10.1080/00031305.2000.10474549
    title: "J. Scott Long and Laurie H. Ervin, Using heteroscedasticity consistent standard errors in the linear regression model, The American Statistician 54(3), 2000, pp. 217 to 224"
    locator: The whole paper (a simulation study of HC0 to HC3 with the advice to use HC3 for samples of 250 or fewer)
---

Heteroscedasticity-consistent (HC) standard errors keep the [ordinary least squares](/ordinary-least-squares/) estimate and replace only its variance estimate. When the errors have unequal variances $\sigma_i^2$, the true covariance of $\hat b$ is the sandwich $(X^\top X)^{-1}X^\top\Sigma X(X^\top X)^{-1}$ with $\Sigma = \operatorname{diag}(\sigma_i^2)$, not $\sigma^2(X^\top X)^{-1}$. The HC estimators put a squared residual, possibly corrected for [leverage](/leverage-statistics/), in place of each unknown $\sigma_i^2$. No model for the variances is needed, and the result is consistent under any pattern of [heteroscedasticity](/heteroscedasticity/). The names Huber-White and Eicker-Huber-White standard errors refer to the same method. The four common versions, HC0 to HC3, differ only in the small sample correction, and with a QR factorization all four cost one least squares fit.

## In plain words

The usual standard error of a regression slope assumes that every point is equally noisy. When the noise is larger for some points, that formula can be far too small or too large. This method keeps the fitted line and estimates the uncertainty in a different way: it looks at how far each point is from the line and lets the points with big misses, at places where they move the slope a lot, count for more uncertainty. It does not need to know why the noise varies. Points that pull the line hard toward themselves look better fitted than they are, so the better versions scale up their misses.

## The problem

**Model.** $y = Xb + \varepsilon$ with $X$ a fixed real $n \times p$ matrix of rank $p < n$ (the intercept is one of the $p$ columns), and independent errors with $\mathrm E[\varepsilon_i] = 0$ and $\operatorname{Var}(\varepsilon_i) = \sigma_i^2$, unknown and possibly all different. Then

$$\operatorname{Cov}(\hat b) = (X^\top X)^{-1}X^\top\Sigma X(X^\top X)^{-1}, \qquad \Sigma = \operatorname{diag}(\sigma_1^2, \dots, \sigma_n^2).$$

**Input.** $X$, $y$ and the choice of version.

**Output.** $\hat b$ and the estimate $\widehat V = (X^\top X)^{-1}X^\top\Omega X(X^\top X)^{-1}$ with $\Omega = \operatorname{diag}(\omega_i)$, where $e_i = y_i - x_i^\top\hat b$, $h_{ii}$ is the leverage, and

| version | $\omega_i$ | idea |
|---|---|---|
| HC0 | $e_i^2$ | White's original |
| HC1 | $e_i^2\,n/(n - p)$ | degrees of freedom correction |
| HC2 | $e_i^2/(1 - h_{ii})$ | unbiased when the variances are equal |
| HC3 | $e_i^2/(1 - h_{ii})^2$ | close to the jackknife |

## The algorithm

```pseudo id=main
HC-COVARIANCE(X[1..n, 1..p], y[1..n], version)
L1  (R, c) ← Householder QR of X, applied to y      ▷ X = Q₁R, c = Qᵀy
L2  b̂ ← solve R b = c[1..p]
L3  eᵢ ← yᵢ - xᵢᵀ b̂ for all i
L4  qᵢ ← R⁻ᵀ xᵢ;  hᵢᵢ ← ‖qᵢ‖² for all i              ▷ qᵢᵀ is row i of Q₁ = X R⁻¹
L5  ωᵢ ← eᵢ² · (1, n/(n - p), 1/(1 - hᵢᵢ) or 1/(1 - hᵢᵢ)²)   ▷ HC0, HC1, HC2, HC3
L6  V ← R⁻¹ (Σᵢ ωᵢ qᵢ qᵢᵀ) R⁻ᵀ
L7  seⱼ ← √Vⱼⱼ for j = 1..p
L8  return (b̂, V, se)
```

Line L4 gets each row of $Q_1$ by one triangular solve, so the leverages come out without the $n \times n$ hat matrix. Line L6 is the sandwich in factored form: $\sum_i\omega_iq_iq_i^\top = Q_1^\top\Omega Q_1$, and $R^{-1}Q_1^\top\Omega Q_1R^{-\top} = (X^\top X)^{-1}X^\top\Omega X(X^\top X)^{-1}$. A $100(1 - \alpha)\%$ interval for $b_j$ is $\hat b_j \pm q\,\mathrm{se}_j$; the implementation takes $q$ as the upper $\alpha/2$ quantile of $t_{n-p}$, which is a convention, since the theory only gives a normal limit. A Wald test of $Cb = d$ uses $(C\hat b - d)^\top(CVC^\top)^{-1}(C\hat b - d)$, as on the [Wald test](/wald-test/) page.

## Example

Take $x = (1, 2, 3, 4, 10)$ and $y = (1, 3, 2, 5, 14)$ with an intercept. Exact arithmetic gives $\hat b = (-21/25, 73/50) = (-0.84, 1.46)$ and

| $i$ | $x_i$ | $e_i$ | $h_{ii}$ |
|---|---|---|---|
| 1 | 1 | 0.38 | 0.38 |
| 2 | 2 | 0.92 | 0.28 |
| 3 | 3 | -1.54 | 0.22 |
| 4 | 4 | 0 | 0.20 |
| 5 | 10 | 0.24 | 0.92 |

The standard error of the slope from each method is:

| method | se of slope |
|---|---|
| usual, $s^2(X^\top X)^{-1}$ | 0.1510 |
| HC0 | 0.0604 |
| HC1 | 0.0780 |
| HC2 | 0.1196 |
| HC3 | 0.3676 |

Point 5 has leverage 0.92, so the line passes close to it and its residual 0.24 says little about its error. HC0 takes that residual at face value, and the slope, which depends mostly on point 5, gets a tiny standard error. HC3 multiplies $e_5^2$ by $1/(1 - 0.92)^2 = 156$. With five points none of these numbers is reliable; the example shows how strongly the versions can differ when the leverages are uneven.

**Measured coverage.** With $n = 25$, $x_i$ drawn once from a lognormal law, $y_i = 1 + x_i + \varepsilon_i$ and $\varepsilon_i \sim N(0, (0.5x_i)^2)$, $r = 2000$ samples from `random.Random(20261114)` gave these coverages of the nominal 95% t interval for the slope:

| method | coverage |
|---|---|
| usual standard error | 0.767 |
| HC0 | 0.858 |
| HC1 | 0.867 |
| HC2 | 0.889 |
| HC3 | 0.912 |

All HC versions improve on the usual standard error, and none reaches 0.95 at this sample size with a skewed design; HC3 comes closest. These are measurements for one design, not theorems.

## Correctness

The proof shows four exact facts. Lines L1 to L6 return exactly $(X^\top X)^{-1}X^\top\Omega X(X^\top X)^{-1}$, with $h_{ii} = \lVert q_i\rVert^2$. If the errors have equal variance $\sigma^2$, then $\mathrm E[e_i^2] = \sigma^2(1 - h_{ii})$, so HC2 is exactly unbiased for $\sigma^2(X^\top X)^{-1}$, HC0 is biased down and HC3 is biased up. By the [Sherman-Morrison formula](/sherman-morrison-formula/), deleting row $i$ moves the estimate by $-(X^\top X)^{-1}x_ie_i/(1 - h_{ii})$, so HC3 is exactly the sum of the outer products of the leave-one-out changes, which links it to the [jackknife](/jackknife-resampling/).

The main statistical property is cited, not proved: under independent errors, bounded higher moments and regularity conditions on $X$ (leverages that go to 0 and a nonsingular limit of $X^\top X/n$), $n\widehat V$ is consistent for the limit of $n\operatorname{Cov}(\hat b)$, for every pattern of variances (Eicker 1967, Huber 1967, White 1980). The resulting t and Wald statistics are asymptotically normal and chi-square.

## Complexity

The QR costs $2np^2 - 2p^3/3$ flops, the $n$ triangular solves of line L4 cost $np^2$, the sum of line L6 costs $np^2$, and the two triangular sandwiches cost $O(p^3)$. The total is $\Theta(np^2)$ time, the order of the fit itself, and $\Theta(np)$ extra space. Forming the $n \times n$ hat matrix would cost $\Theta(n^2p)$ time and $\Theta(n^2)$ space and is never needed.

## Properties

- **No variance model.** The estimate is consistent whatever the $\sigma_i^2$ are, as long as the errors are independent and the leverages become small.
- **Order of the versions.** HC1 equals HC0 times $n/(n - p)$, and since $1 \le 1/(1 - h_{ii}) \le 1/(1 - h_{ii})^2$, the matrices satisfy HC0 $\preceq$ HC2 $\preceq$ HC3 in the Loewner order; the same holds for each standard error.
- **Equivariance.** Replacing $X$ by $XA$ for a nonsingular $A$ maps $\widehat V$ to $A^{-1}\widehat VA^{-\top}$, as for the usual covariance, and the residuals and leverages do not change.
- **Same as the M-estimation sandwich.** For least squares as an [M-estimator](/m-estimator/), the bread is $X^\top X$ and the meat is $\sum e_i^2x_ix_i^\top$, so HC0 is the general sandwich covariance applied to this case.
- **Leverage-one points.** If $h_{ii} = 1$ then $e_i = 0$, HC0 ignores row $i$, and HC2 and HC3 are undefined. The implementation raises an error for HC2 and HC3 in that case.

## Variants and improvements

- **HC4 and HC5.** Cribari-Neto and coauthors raise the leverage exponent with $h_{ii}$ to handle very high leverage points. They are rarely needed when the design has no extreme points.
- **Clustered errors.** If the errors are correlated within groups, replace $\sum_ie_i^2x_ix_i^\top$ by a sum over groups of $(\sum_{i \in g}e_ix_i)(\sum_{i \in g}e_ix_i)^\top$: [cluster-robust standard errors](/cluster-robust-standard-errors/). With one observation per group it reduces to HC0, or HC1 with the matching correction.
- **Serial correlation.** For time series, kernel-weighted sums of cross products of nearby $e_tx_t$ give heteroscedasticity and autocorrelation consistent estimates, of which Newey and West's is the best known.
- **Bootstrap.** The wild bootstrap multiplies each residual by an independent random sign and refits; with HC2 or HC3 studentization it often gives better small sample tests than the normal approximation. The pairs [bootstrap](/bootstrap-method/) resamples whole rows.
- **Other estimators.** The same sandwich form gives the covariance of [generalized estimating equations](/generalized-estimating-equations/), of [quasi-likelihood](/quasi-likelihood/) fits with a wrong variance function, and of [M-estimators](/m-estimator/) in general.

## When to use it

Use HC standard errors for least squares on cross-section data whenever the variance may depend on the regressors, which is most of the time in economics and the social sciences. Long and Ervin (2000) recommend HC3 when $n \le 250$, and argue that the choice should not depend on a pretest such as the [Breusch-Pagan test](/breusch-pagan-test/). If the variance pattern is known or can be modelled well, [weighted least squares](/weighted-least-squares/) gives a more efficient estimate; an HC covariance on top of it protects against a wrong weight model.

## Pitfalls

- **Small samples with high leverage.** HC0 and HC1 can be far too small when some $h_{ii}$ are large, as in the example. Prefer HC3, look at the leverages, and do not trust the nominal level when a few points dominate.
- **It fixes the variance, not the estimate.** OLS stays unbiased under heteroscedasticity but is not efficient. HC standard errors make the inference valid; they do not make the fit better.
- **Correlated errors.** The method assumes independent errors. Within-group or serial correlation needs the clustered or the autocorrelation consistent versions.
- **F tests.** The usual F statistic uses $s^2$ and is wrong under heteroscedasticity. Use the Wald form with $\widehat V$, and treat its F or chi-square reference law as an approximation.
- **Which version.** Software defaults differ: some report HC0, some HC1, some HC3. State the version in reports.
- **Misspecified mean.** If the mean model is wrong, the HC covariance is still a consistent covariance for the best linear approximation, but the coefficients no longer mean what the model says.

## Implementations

## History

Eicker (1963, 1967) proved the consistency of the estimator for least squares with unequal variances, and Huber (1967) gave the general sandwich covariance of an M-estimate under a wrong model in the same Berkeley Symposium volume. White (1980) derived the estimator again for econometric models with random regressors, together with a direct test for heteroscedasticity, and it spread quickly in applied work. MacKinnon and White (1985) studied the small sample behavior and proposed the HC1, HC2 and jackknife versions; the closed form now called HC3 approximates their jackknife. Long and Ervin (2000) made HC3 the usual recommendation for small samples.

## References
