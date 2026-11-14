---
tag: TBDQN3
kind: algorithm
slug: durbin-watson-test
name: Durbin-Watson test
aliases:
- Durbin-Watson statistic
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: Tests for first-order autocorrelation of regression residuals by the sum of squared successive differences over the sum of squares. Values near 2 mean none.
model: real-ram
complexity:
  vars: {n: the number of observations, p: "the number of columns of X, with p < n", B: the number of simulated samples}
  time: {worst: Θ(n p^2 + B n p), best: Θ(n p^2 + B n p)}
  space: {extra: Θ(n p)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1950
  people: [James Durbin, Geoffrey S. Watson]
  note: Durbin and Watson (1950, 1951) defined the statistic, showed that its null law lies between two laws that depend only on n and p, and tabulated the bounds. Imhof (1961) made the exact law for a given X computable.
prereqs: [ordinary-least-squares, statistical-hypothesis-test, p-value, autoregressive-model]
see_also: [generalized-least-squares, ljung-box-test, breusch-pagan-test, partial-autocorrelation-function, arima-model, permutation-test, heteroscedasticity-consistent-standard-errors, stationary-process]
sources:
  - paper: doi:10.1093/biomet/37.3-4.409
    title: "J. Durbin and G. S. Watson, Testing for serial correlation in least squares regression. I, Biometrika 37(3-4), 1950, pp. 409 to 428"
    locator: The whole paper (the statistic d, its null law as a ratio of quadratic forms in the eigenvalues of M A M, and the bounds d_L and d_U)
  - paper: doi:10.1093/biomet/38.1-2.159
    title: "J. Durbin and G. S. Watson, Testing for serial correlation in least squares regression. II, Biometrika 38(1-2), 1951, pp. 159 to 178"
    locator: The whole paper (the tables of the bounds d_L and d_U and the approximations for the inconclusive region)
  - paper: doi:10.1093/biomet/48.3-4.419
    title: "J. P. Imhof, Computing the distribution of quadratic forms in normal variables, Biometrika 48(3-4), 1961, pp. 419 to 426"
    locator: The whole paper (numerical inversion of the characteristic function, which gives the exact null distribution of d for a given X)
  - paper: doi:10.2307/1909547
    title: "J. Durbin, Testing for serial correlation in least-squares regression when some of the regressors are lagged dependent variables, Econometrica 38(3), 1970, pp. 410 to 421"
    locator: The whole paper (the bias of d toward 2 when a lagged response is a regressor, and the h statistic)
---

The Durbin-Watson test checks whether the errors of a linear regression on time-ordered data are correlated with their neighbours. It fits the model by [ordinary least squares](/ordinary-least-squares/) and computes $d = \sum_{t \ge 2}(e_t - e_{t-1})^2/\sum_te_t^2$ from the residuals. Without correlation $d$ is near 2; positive correlation makes successive residuals similar and $d$ small, and negative correlation makes $d$ large. Under normal errors the null law of $d$ depends on the design $X$ but not on the coefficients or the error variance. Durbin and Watson could not tabulate a law for every $X$, so they bracketed it between two laws that depend only on $n$ and $p$; this gives the classical bounds test with its inconclusive region. Today the exact p-value for the given $X$ is easy to get, here by simulation.

## In plain words

When data come in time order, an error in one period often carries over to the next. A fitted line then looks better than it is, because its standard errors assume that every error is new. The test looks at the misses of the fitted line in time order. If neighbouring misses are close to each other, the sum of their squared differences is small compared with the sum of their squares. The ratio of the two is about 2 when the misses are unrelated, much lower than 2 when misses repeat, and higher than 2 when they flip sign. To judge whether a value is unusual, the method simulates many sets of pure noise for the same design and counts how often the noise gives a value as low.

## The problem

**Model.** $y = Xb + \varepsilon$ with $X$ a fixed real $n \times p$ matrix of rank $p < n$ whose columns include the constant, $t = 1, \dots, n$ the time order of the rows, and errors from the stationary first-order [autoregressive model](/autoregressive-model/) $\varepsilon_t = \rho\varepsilon_{t-1} + u_t$ with independent $u_t \sim N(0, \sigma^2)$ and $|\rho| < 1$. The regressors must not include lagged values of $y$.

**Hypotheses.** $H_0$: $\rho = 0$, so the errors are independent $N(0, \sigma^2)$; $H_1$: $\rho > 0$. The alternatives $\rho < 0$ and $\rho \ne 0$ are handled in the same way.

**Statistic.** With the residuals $e = My$, $M = I - X(X^\top X)^{-1}X^\top$, and the lag-one residual autocorrelation $r_1$:

$$d = \frac{\sum_{t=2}^n(e_t - e_{t-1})^2}{\sum_{t=1}^ne_t^2} = 2(1 - r_1) - \frac{e_1^2 + e_n^2}{\sum_te_t^2}, \qquad r_1 = \frac{\sum_{t=2}^ne_te_{t-1}}{\sum_te_t^2}.$$

So $d \approx 2(1 - r_1)$, and $0 < d < 4$.

**Null distribution.** Under $H_0$, $d = \varepsilon^\top MAM\varepsilon/\varepsilon^\top M\varepsilon$, where $A$ is the tridiagonal matrix with $e^\top Ae = \sum_{t \ge 2}(e_t - e_{t-1})^2$. Its law depends only on $X$. It is the law of $\sum_i\nu_i\xi_i^2/\sum_i\xi_i^2$, with $\nu_1, \dots, \nu_{n-p}$ the nonzero eigenvalues of $MAM$ and independent standard normal $\xi_i$.

**Rejection rule and p-value.** Against $\rho > 0$, small $d$ is extreme. The Monte Carlo p-value is $(1 + \#\{d^*_k \le d\})/(1 + B)$, where $d^*_1, \dots, d^*_B$ are computed from $B$ standard normal response vectors with the same $X$; reject at level $\alpha$ when it is at most $\alpha$. This test has exact size $\alpha$ when $\alpha(B + 1)$ is an integer. The classical bounds test compares $d$ with tabulated points $d_L$ and $d_U$: reject if $d < d_L$, do not reject if $d > d_U$, and give no answer between them.

**Power.** The test is built for AR(1) errors and has good power against them; it also reacts to other forms of correlation that make $r_1$ positive. It has little power against correlation at longer lags only, such as a seasonal pattern.

## The algorithm

```pseudo id=main
DURBIN-WATSON(X[1..n, 1..p], y[1..n], B)
L1  Q₁ ← orthonormal basis of the columns of X by Householder QR;  e ← y - Q₁Q₁ᵀy
L2  S ← Σₜ eₜ²
L3  D ← Σ_{t=2..n} (eₜ - eₜ₋₁)²
L4  d ← D / S;  r₁ ← Σ_{t=2..n} eₜeₜ₋₁ / S
L5  for k ← 1 to B: draw ε* with independent N(0, 1) entries
L6      d*ₖ ← D / S of the residuals ε* - Q₁Q₁ᵀε*          ▷ lines L2 to L4 again
L7  p ← (1 + #{k : d*ₖ ≤ d}) / (1 + B)                     ▷ against ρ > 0
L8  return (d, r₁, p)
```

Line L1 needs the factorization only once; every simulated sample in line L6 reuses $Q_1$, so a sample costs $\Theta(np)$. Simulated samples use $\sigma = 1$ and $b = 0$; any other values give the same $d^*$, because the statistic of $ay + Xc$ equals that of $y$. Against $\rho < 0$ the count is $\#\{d^*_k \ge d\}$, and the two-sided p-value is twice the smaller one-sided p-value, at most 1.

## Example

Take $t = 1, \dots, 12$, an intercept and a linear trend, so $X$ has the rows $(1, t)$ and $p = 2$, and

$$y = (1.0, 1.9, 3.1, 3.2, 3.0, 3.6, 4.4, 5.6, 6.2, 6.1, 6.0, 6.8).$$

The residuals of the least squares line are

$$e = (-0.447, -0.055, 0.636, 0.228, -0.480, -0.388, -0.096, 0.596, 0.688, 0.080, -0.528, -0.236),$$

which stay above or below zero for runs of two to four periods. Then $r_1 = 0.3329$ and $d = 1.2189$.

| method | result at the 5% level |
|---|---|
| Monte Carlo p-value, $B = 9999$, seed 7 | $p = 0.0278$, reject |
| bounds, $P(d_L \le d)$ | 0.131 |
| bounds, $P(d_U \le d)$ | 0.0296 |
| bounds test | inconclusive, since $0.0296 < 0.05 < 0.131$ |

The two bound probabilities were estimated from 20000 draws of $\xi$ (seed 3). The exact p-value lies between them, as the theory says. Here it is close to the upper bound, because the trend column is nearly an eigenvector of $A$, and for such a design the law of $d$ is close to that of $d_U$. The bounds test gives no answer, but the test for the actual design rejects.

**Measured size and power.** With $X = [1, t]$ and the 5% level, $B = 99$ for each Monte Carlo p-value:

| errors | $n$ | $r$ | rejection rate |
|---|---|---|---|
| independent $N(0, 1)$ | 20 | 600 | 0.037 |
| independent $N(0, 1)$ | 30 | 2000 | 0.0535 |
| AR(1), $\rho = 0.3$ | 30 | 1000 | 0.401 |
| AR(1), $\rho = 0.7$ | 30 | 1000 | 0.936 |

The first two rows agree with the exact size 0.05 within the Monte Carlo error, about 0.009 for $r = 600$ and 0.005 for $r = 2000$. The power for $\rho = 0.3$ shows that $n = 30$ is too short to detect weak correlation reliably.

## Correctness

The proof shows four exact facts. First, the identity $d = 2(1 - r_1) - (e_1^2 + e_n^2)/S$, and $0 < d < 4$ when the constant is a column of $X$. Second, the matrix $A$ has the eigenvalues $\lambda_j = 2 - 2\cos(\pi j/n)$, $j = 0, \dots, n - 1$, with $\lambda_0 = 0$ for the constant vector. Third, the residuals of $ay + Xc$ are $ae$, so under normal $H_0$ the law of $d$ does not depend on $b$ or $\sigma$; the observed and simulated statistics are then exchangeable, and the Monte Carlo p-value has exact size. Fourth, by the Cauchy interlacing theorem the eigenvalues $\nu_i$ of $A$ on the residual space satisfy $\lambda_i \le \nu_i \le \lambda_{i+p-1}$, so for the same $\xi$

$$d_L = \frac{\sum_{i=1}^{n-p}\lambda_i\xi_i^2}{\sum_i\xi_i^2} \le d \le d_U = \frac{\sum_{i=1}^{n-p}\lambda_{i+p-1}\xi_i^2}{\sum_i\xi_i^2},$$

and the laws of $d_L$ and $d_U$ depend only on $n$ and $p$. This is the bounding result of Durbin and Watson.

What is cited and not proved: the numerical method of Imhof (1961) for the exact distribution function, and the limit $d \to 2(1 - \rho)$ under AR(1) errors. The size of the test for non-normal errors and all power values are measured, not proved.

## Complexity

The Householder factorization in line L1 costs $\Theta(np^2)$, and lines L2 to L4 cost $\Theta(n)$. Each of the $B$ simulated samples needs one projection, $\Theta(np)$, so the total is $\Theta(np^2 + Bnp)$ time and $\Theta(np)$ extra space for $Q_1$. The statistic alone, without a p-value, costs $\Theta(np^2)$. The exact law by Imhof's method needs the $n - p$ eigenvalues $\nu_i$, which costs $\Theta(n^3)$ by a dense symmetric eigenvalue method, and then a numerical integral.

## Properties

- **Exact test for the given design.** Under normal independent errors the Monte Carlo test has exact size for every $X$ that contains the constant, with no table and no inconclusive region.
- **Invariance.** $d$ is unchanged by $y \to ay + Xc$ for $a \ne 0$, so the unknown $b$ and $\sigma$ do not matter.
- **Range and centre.** $0 < d < 4$. Under $H_0$ the mean of $d$ is $\sum_i\nu_i/(n - p) = \operatorname{tr}(MA)/(n - p)$, which is near 2 for large $n$.
- **First order only.** The statistic uses only lag-one products of the residuals.
- **Depends on the time order.** Rows must be in time order; sorting the rows by some other key gives a test of a different hypothesis.
- **Normality.** The exact null law assumes normal errors. For other error laws with a finite variance the test is valid only for large $n$; this was not measured here.

## Variants and improvements

- **Bounds test.** The original form uses the tabulated $d_L$ and $d_U$ for given $n$ and $p$. It needs no computation of the law but has an inconclusive region, which is wide for small $n$, as the example shows.
- **Exact p-value by quadratic forms.** Compute the eigenvalues $\nu_i$ of $MAM$ and evaluate $P(\sum_i(\nu_i - d)\xi_i^2 \le 0)$ by Imhof's numerical inversion or a related algorithm for quadratic forms. The simulation on this page gives the same p-value up to Monte Carlo error.
- **Negative and two-sided alternatives.** Use $4 - d$ against $\rho < 0$, or double the smaller one-sided p-value.
- **Lagged dependent variables.** When $y_{t-1}$ is a regressor, $d$ is biased toward 2 and the test loses power. Durbin (1970) gave the $h$ statistic and an alternative test that regresses $e_t$ on $e_{t-1}$ and the regressors.
- **Higher lags.** To test several lags at once, regress $e_t$ on $X$ and $e_{t-1}, \dots, e_{t-m}$ and test the lag coefficients, or use the [Ljung-Box test](/ljung-box-test/) on the residuals; the [partial autocorrelation function](/partial-autocorrelation-function/) shows which lags matter.

## When to use it

Use it as a quick check of serial correlation after a regression on time-ordered data with fixed regressors, an intercept and no lagged response. A small $d$ means that the usual standard errors are too small. The remedies are to model the correlation, for example with [generalized least squares](/generalized-least-squares/) for AR(1) errors or an [ARIMA model](/arima-model/) for the errors, or to keep the least squares fit and use standard errors that allow for serial correlation. For data without a time order, the test has no meaning.

## Pitfalls

- **Lagged response as a regressor.** Then $d$ is biased toward 2 and can hide strong correlation; use Durbin's $h$ or the lagged-residual regression.
- **No intercept.** The bounds $d_L$ and $d_U$ in the tables assume a constant column; without it they do not apply. The Monte Carlo version works for any $X$, but the range result $d > 0$ needs the constant.
- **Inconclusive is not "no correlation".** In the example the bounds test gives no answer, yet the exact p-value is 0.028. Compute the exact p-value for the given $X$.
- **A low $d$ from a wrong mean.** A missing trend, a missing seasonal term or a nonlinear effect leaves runs of residuals of the same sign, and $d$ falls although the errors are independent. Plot the residuals against time before concluding that the errors are correlated.
- **Gaps and unequal spacing.** The statistic assumes equally spaced observations without gaps; differences across a gap compare periods that are not neighbours.
- **Not rejecting with small $n$.** With $n = 30$ the power against $\rho = 0.3$ was only 0.40 in the table above.

## Implementations

## History

Durbin and Watson (1950) defined $d$, showed that its null law under normal errors is that of a ratio of quadratic forms whose weights depend on $X$, and bracketed it between two laws that depend only on $n$ and $p$. Their second paper (1951) gave the tables of $d_L$ and $d_U$ that made the test a standard part of regression output. Imhof (1961) gave a numerical method for the distribution of quadratic forms in normal variables, which made the exact p-value for a given design computable. Durbin (1970) showed that the test fails when a lagged response is a regressor and proposed the $h$ statistic for that case.

## References
