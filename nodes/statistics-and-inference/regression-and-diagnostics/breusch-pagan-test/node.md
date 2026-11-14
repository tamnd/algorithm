---
tag: R9XRKX
kind: algorithm
slug: breusch-pagan-test
name: Breusch-Pagan test
aliases:
- Koenker-Bassett test
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: Tests for heteroscedasticity by regressing the squared residuals on the predictors; n times the R-squared of that regression is chi-squared under the null.
model: real-ram
complexity:
  vars: {n: the number of observations, p: "the number of columns of X, with p < n", q: the number of variance variables}
  time: {worst: Θ(n (p^2 + q^2)), best: Θ(n (p^2 + q^2))}
  space: {extra: Θ(n (p + q))}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1979
  people: [Trevor S. Breusch, Adrian R. Pagan, Roger Koenker]
  note: Breusch and Pagan (1979) derived the score test for variances that depend on chosen variables. Koenker (1981) showed that it is not robust to non-normal errors and gave the studentized n R^2 form.
prereqs: [heteroscedasticity, ordinary-least-squares, score-test, coefficient-of-determination, statistical-hypothesis-test]
see_also: [heteroscedasticity-consistent-standard-errors, weighted-least-squares, regression-f-test, durbin-watson-test, quantile-regression, studentized-residual, likelihood-ratio-test, p-value]
sources:
  - paper: doi:10.2307/1911963
    title: "T. S. Breusch and A. R. Pagan, A simple test for heteroscedasticity and random coefficient variation, Econometrica 47(5), 1979, pp. 1287 to 1294"
    locator: The whole paper (the score test for a variance h(z_i^T alpha), computed as half the explained sum of squares of the regression of e_i^2 / sigma^2 on z_i)
  - paper: doi:10.1016/0304-4076(81)90062-2
    title: "Roger Koenker, A note on studentizing a test for heteroscedasticity, Journal of Econometrics 17(1), 1981, pp. 107 to 112"
    locator: The whole paper (the sensitivity of the Breusch-Pagan test to the kurtosis of the errors and the studentized n R^2 version)
  - paper: doi:10.2307/1912528
    title: "Roger Koenker and Gilbert Bassett Jr., Robust tests for heteroscedasticity based on regression quantiles, Econometrica 50(1), 1982, pp. 43 to 61"
    locator: The whole paper (tests of heteroscedasticity from regression quantiles that do not assume normal errors)
  - paper: doi:10.2307/1912934
    title: "Halbert White, A heteroskedasticity-consistent covariance matrix estimator and a direct test for heteroskedasticity, Econometrica 48(4), 1980, pp. 817 to 838"
    locator: The whole paper (the direct test, which is n R^2 of the regression of e_i^2 on the predictors, their squares and their products)
---

The Breusch-Pagan test checks whether the error variance of a linear regression depends on chosen variables $z_i$. It fits the model by [ordinary least squares](/ordinary-least-squares/), regresses the squared residuals on $z_i$, and rejects constant variance when that auxiliary regression explains much. The original statistic of Breusch and Pagan (1979) is half the explained sum of squares of $e_i^2/\hat\sigma^2$; it is the [score test](/score-test/) under normal errors, and it is too liberal when the errors have heavy tails. Koenker's studentized form, $nR^2$ of the same regression, keeps its level without normality and is the one most software uses by default; some programs call this form the Koenker-Bassett test. Both are referred to a chi-squared law with $q$ degrees of freedom, and with normal errors a Monte Carlo p-value for the given design is exact.

## In plain words

After fitting a line, look at how big the misses are. If the misses tend to be larger where some variable is large, the noise is not constant, and the usual standard errors are wrong. The test makes this precise: it fits a second line that tries to predict the squared misses from the chosen variables. If that second line predicts them clearly better than a flat line would, the test reports that the noise level changes. The original version assumes bell-shaped noise and raises false alarms when the noise has heavy tails. Koenker's version fixes this and is the safer default.

## The problem

**Model.** $y = Xb + \varepsilon$ with $X$ a fixed real $n \times p$ matrix of rank $p < n$ (the intercept is one of the columns), independent errors with mean 0 and $\operatorname{Var}(\varepsilon_i) = h(\alpha_0 + z_i^\top\alpha)$ for a positive function $h$ that need not be known, and $z_i \in \mathbb R^q$ the variance variables. Often $z_i$ is the row $x_i$ without the intercept. With $Z$ the $n \times (q + 1)$ matrix of rows $(1, z_i^\top)$, of rank $q + 1 < n$:

**Hypotheses.** $H_0$: $\alpha = 0$, so the variance is constant; $H_1$: $\alpha \ne 0$.

**Statistics.** With the residuals $e_i$, $\hat\sigma^2 = \frac1n\sum_ie_i^2$, $g_i = e_i^2/\hat\sigma^2$, and ESS, TSS and $R^2$ the explained and total sums of squares and the [coefficient of determination](/coefficient-of-determination/) of the regression of $g$ on $Z$:

$$\mathrm{LM}_{\mathrm{BP}} = \tfrac12\mathrm{ESS}, \qquad \mathrm{LM}_{\mathrm K} = nR^2 = \frac{n\,\mathrm{ESS}}{\mathrm{TSS}}.$$

The $R^2$ is the same for $e_i^2$ and for $g_i$, so $\mathrm{LM}_{\mathrm K}$ is also $nR^2$ of the regression of $e_i^2$ on $Z$.

**Null distribution.** Under $H_0$, $\mathrm{LM}_{\mathrm{BP}} \to \chi^2_q$ when the errors are normal, and $\mathrm{LM}_{\mathrm K} \to \chi^2_q$ when they are independent and identically distributed with a finite fourth moment. Neither law is exact for finite $n$. Reject at level $\alpha$ when the statistic is at least the upper $\alpha$ point $\chi^2_{q, 1-\alpha}$; the p-value is $P(\chi^2_q \ge \mathrm{LM})$. With normal errors the null law depends only on $X$ and $Z$, so simulating standard normal errors for the given design gives the exact Monte Carlo p-value $(1 + \#\{\mathrm{LM}^* \ge \mathrm{LM}\})/(1 + B)$.

**Power.** The test has power against variances that change with $z_i$ in any smooth way, since $h$ does not enter the statistic. It has little power against variance patterns that do not follow the chosen $z_i$, and little power in small samples.

## The algorithm

```pseudo id=main
BREUSCH-PAGAN(X[1..n, 1..p], y[1..n], z[1..n, 1..q])
L1  e ← residuals of y on X by Householder least squares
L2  σ̂² ← Σᵢ eᵢ² / n;  gᵢ ← eᵢ² / σ̂² for all i       ▷ the mean of g is exactly 1
L3  (R_Z, d) ← Householder QR of Z = [1, z] applied to g    ▷ d = Q_Zᵀ g
L4  ESS ← d₁² + … + d_q²;  TSS ← Σᵢ (gᵢ - 1)²          ▷ d₀ belongs to the constant
L5  LM_BP ← ESS / 2
L6  LM_K ← n · ESS / TSS
L7  p_BP ← P(χ²_q ≥ LM_BP);  p_K ← P(χ²_q ≥ LM_K)
L8  return (LM_BP, LM_K, p_BP, p_K)
```

Line L4 reads the explained sum of squares off the transformed response, as on the [F-test for nested linear models](/regression-f-test/) page, so the auxiliary fit needs no normal equations and no second pass. Lines L1 to L6 do not depend on how $e$ was scaled, which gives the exact Monte Carlo version: repeat lines L1 to L6 for $B$ samples of standard normal $y$ and count how often the simulated statistic is at least the observed one.

## Example

Take $x_i = i$ for $i = 1, \dots, 10$, $y = (3.2, 3.8, 5.5, 5.5, 8, 7, 11, 8, 14, 9)$, an intercept and $z_i = x_i$, so $q = 1$. The residuals are

$$e = (-0.165, -0.484, 0.297, -0.622, 0.959, -0.959, 2.122, -1.797, 3.284, -2.635),$$

which fan out as $x$ grows. The results are:

| statistic | value | chi-squared p-value | Monte Carlo p-value, $B = 9999$ |
|---|---|---|---|
| $\mathrm{LM}_{\mathrm{BP}}$ | 5.1931 | 0.0227 | 0.0077 |
| $\mathrm{LM}_{\mathrm K}$ | 6.8880 | 0.0087 | 0.0020 |

The ratio $\mathrm{LM}_{\mathrm{BP}}/\mathrm{LM}_{\mathrm K} = \hat v/(2\hat\sigma^4) = 0.754$, where $\hat v$ is the variance of the $e_i^2$. Both tests reject at the 5% level. With $n = 10$ the chi-squared p-values are far from the exact Monte Carlo ones for normal errors (seed 7 for `random.Random`), which shows how rough the asymptotic law is in small samples.

**Measured size and power.** With $n = 50$, one regressor drawn once from the uniform law on $[0, 1]$, $z_i = x_i$, and the 5% level:

| errors | $r$ | $\mathrm{LM}_{\mathrm{BP}}$ | $\mathrm{LM}_{\mathrm K}$ |
|---|---|---|---|
| $N(0, 1)$, $H_0$ | 4000 | 0.048 | 0.054 |
| $t_5$, $H_0$ | 4000 | 0.147 | 0.046 |
| $N(0, 1)$ times $0.5 + 2x_i$ | 2000 | 0.861 | 0.805 |
| $t_5$ times $0.5 + 2x_i$ | 2000 | 0.877 | 0.658 |

With heavy-tailed errors the original test rejects three times too often; the higher power of $\mathrm{LM}_{\mathrm{BP}}$ in the last row is not usable, because its size is wrong. The Monte Carlo standard error of a size near 0.05 with $r = 4000$ is 0.0034.

## Correctness

The proof shows four exact facts. Lines L2 to L6 compute $\mathrm{ESS}/2$ and $n\,\mathrm{ESS}/\mathrm{TSS}$ of the auxiliary regression. Under normal errors with $\sigma_i^2 = h(\alpha_0 + z_i^\top\alpha)$, the score test of $\alpha = 0$ is exactly $\mathrm{LM}_{\mathrm{BP}}$ for every $h$, which explains why the test does not need the form of the variance function. The identity

$$\mathrm{LM}_{\mathrm{BP}} = \frac{\hat v}{2\hat\sigma^4}\,\mathrm{LM}_{\mathrm K}, \qquad \hat v = \frac1n\sum_i(e_i^2 - \hat\sigma^2)^2,$$

shows that the two statistics differ by an estimate of $(\kappa - 1)/2$, where $\kappa$ is the kurtosis of the errors; it is 1 for normal errors and 4 for $t_5$ errors. Finally, the residuals of $ay + Xc$ are $ae$ and both statistics are unchanged, so under normal errors their null law does not depend on $b$ or $\sigma$ and the Monte Carlo test has exact size.

The chi-squared limits are cited, not proved: Breusch and Pagan (1979) for the normal case, from the general theory of the score test, and Koenker (1981) for the studentized form.

## Complexity

The two Householder factorizations cost $\Theta(np^2)$ and $\Theta(nq^2)$, and the rest is $\Theta(n)$. The total is $\Theta(n(p^2 + q^2))$ time and $\Theta(n(p + q))$ extra space. The Monte Carlo p-value multiplies this by $B$; the QR factors of $X$ and $Z$ could be reused, since only $y$ changes.

## Properties

- **Invariance.** Both statistics are unchanged by $y \to ay + Xc$ and by any nonsingular linear change of the columns of $Z$ that keeps the constant.
- **No variance function needed.** The score test is the same for every link $h$, so the test detects $\sigma_i^2 = \sigma^2\exp(\gamma z_i)$ and $\sigma_i^2 = \sigma^2(1 + \gamma z_i)^2$ equally.
- **Score test.** It needs only the fit under $H_0$. The likelihood ratio and Wald tests for a specified $h$ need the fit under $H_1$ and agree with it to first order.
- **Non-normal errors.** $\mathrm{LM}_{\mathrm K}$ keeps its asymptotic level under any error law with a finite fourth moment; $\mathrm{LM}_{\mathrm{BP}}$ does not.
- **Uses only $e^2$.** The test does not look at the sign of the residuals, so it has no power against a wrong mean model that leaves the variance constant. It can, however, react to a wrong mean model, since a missing term changes the size of the residuals in a way that may follow $z_i$.

## Variants and improvements

- **White's test.** Take $z_i$ as the predictors, their squares and their cross products, and use $nR^2$. This detects variance patterns that are quadratic in the predictors, at the cost of $q = O(p^2)$ degrees of freedom.
- **F form.** Some software reports the F test for the auxiliary regression, $F = \frac{R^2/q}{(1 - R^2)/(n - q - 1)}$, which is asymptotically equivalent to $nR^2/q$.
- **Exact Monte Carlo test.** If normal errors are a fair assumption, simulate the statistic for the given $X$ and $Z$ as above; this removes the error of the chi-squared approximation, which is large for small $n$.
- **Quantile-based tests.** Koenker and Bassett (1982) compare slopes of [quantile regressions](/quantile-regression/) at different quantiles; equal slopes mean the spread does not change with $x$. These tests do not need a finite fourth moment.
- **Goldfeld and Quandt.** Splitting the data by the size of one variable and comparing the residual variances of the two halves by an F ratio gives an exact test under normal errors, but only for a variance that is monotone in that variable.

## When to use it

Use the Koenker form as a diagnostic when unequal variances would change the analysis: to decide whether to model the variance with [weighted least squares](/weighted-least-squares/), or to show that a variance model is needed. Choose $z_i$ from knowledge of the problem, usually the predictors or the fitted values. Do not use it as a gate for the choice of standard errors: [heteroscedasticity-consistent standard errors](/heteroscedasticity-consistent-standard-errors/) cost little and are valid whether or not the test rejects, and a pretest changes the level of the later tests.

## Pitfalls

- **The original statistic with heavy tails.** $\mathrm{LM}_{\mathrm{BP}}$ assumes normal errors. With $t_5$ errors its 5% test rejected 15% of the time in the table above. Use $\mathrm{LM}_{\mathrm K}$ unless normality is credible.
- **Not rejecting does not prove constant variance.** With small $n$ the power is low, and the test sees only patterns that follow the chosen $z_i$.
- **Small samples.** The chi-squared approximation can be poor for $n$ below about 30, as the example shows; the Monte Carlo version helps when the errors are normal.
- **Misspecified mean.** A missing nonlinear term or interaction shows up as large residuals in some region and can make the test reject although the variance is constant. Check the mean model first.
- **Outliers.** One large residual can dominate $\sum e_i^2$ and the auxiliary regression; inspect [studentized residuals](/studentized-residual/).

## Implementations

## History

Breusch and Pagan (1979) derived the score test for a general variance $h(z_i^\top\alpha)$ and noted that it does not depend on $h$, which made it simple to apply. White (1980) gave his direct test with the squares and products of the predictors as part of his paper on the heteroscedasticity-consistent covariance. Koenker (1981) showed that the Breusch-Pagan statistic is sensitive to the kurtosis of the errors and proposed the studentized $nR^2$ version, and Koenker and Bassett (1982) developed tests based on regression quantiles.

## References
