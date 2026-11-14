---
tag: 3EE4N8
kind: algorithm
slug: weighted-least-squares
name: Weighted least squares
aliases:
- WLS
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: Least squares with each squared residual weighted, usually by the inverse of its variance. It is the best linear unbiased estimator when the variances are known.
model: real-ram
complexity:
  vars: {n: the number of observations, p: "the number of columns of X, with p <= n"}
  time: {worst: Θ(n p^2), best: Θ(n p^2)}
  space: {extra: Θ(n p)}
  flops: {worst: "2n p^2 - 2p^3/3 + O(n p)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1935
  people: [Alexander C. Aitken]
  note: Aitken proved in 1935 that least squares weighted by the inverse of the error covariance gives the minimum variance linear unbiased estimate. Weighted least squares is the case of uncorrelated errors.
prereqs: [ordinary-least-squares, gauss-markov-theorem, heteroscedasticity, qr-decomposition]
see_also: [generalized-least-squares, iteratively-reweighted-least-squares, heteroscedasticity-consistent-standard-errors, breusch-pagan-test, regression-f-test, normal-equations, horvitz-thompson-estimator, quasi-likelihood]
sources:
  - paper: doi:10.1017/S0370164600014346
    title: "A. C. Aitken, On least squares and linear combination of observations, Proceedings of the Royal Society of Edinburgh 55, 1935 (volume dated 1936), pp. 42 to 48"
    locator: The whole paper (the estimator weighted by the inverse covariance and its minimum variance property)
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: Chapter 3 (least squares estimation, with generalized and weighted least squares as a change of variables) and Chapter 10 (unequal variances and weighting)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.3 (the full-rank least squares problem solved by QR, and why the normal equations square the condition number)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 20 (the least squares problem, the backward stability of Householder QR)
---

Weighted least squares (WLS) fits a linear model $y = Xb + \varepsilon$ by minimizing $\sum_i w_i (y_i - x_i^\top b)^2$, a sum of squared residuals in which observation $i$ counts with a known weight $w_i \ge 0$. When the errors are uncorrelated with variances $\sigma^2/w_i$, so that the weight is the inverse of the variance up to one common factor, WLS is the best linear unbiased estimator, and [ordinary least squares](/ordinary-least-squares/) is not. The computation is ordinary least squares on rows multiplied by $\sqrt{w_i}$. It is the diagonal case of [generalized least squares](/generalized-least-squares/), and it is the inner step of [iteratively reweighted least squares](/iteratively-reweighted-least-squares/).

## In plain words

Some measurements are more precise than others. A cheap sensor and a good sensor measure the same thing; a mean of 50 readings is more reliable than a single reading. If you fit a line and treat every point the same, the noisy points pull the line as hard as the precise ones. Weighted least squares gives each point a weight and makes the fit care more about the points with large weight. The best weight is one over the spread of the point's error. The trick that computes it is short: multiply each row of the data by the square root of its weight. The noise then has the same spread in every row, and the ordinary fit on the changed rows is the weighted fit.

## The problem

**Model.** $y = Xb + \varepsilon$, where $X$ is a fixed real $n \times p$ matrix (the intercept column is one of the $p$ columns, as on the [hat matrix](/hat-matrix/) page), $b \in \mathbb{R}^p$ is the coefficient vector, $\mathrm E[\varepsilon] = 0$ and

$$\operatorname{Cov}(\varepsilon) = \sigma^2 W^{-1}, \qquad W = \operatorname{diag}(w_1, \dots, w_n), \quad w_i > 0 \text{ known}, \ \sigma^2 \text{ unknown}.$$

So the errors are uncorrelated and [heteroscedastic](/heteroscedasticity/) with a known pattern: only the ratios of the weights matter, and multiplying all $w_i$ by a constant changes $\sigma^2$, not the fit.

**Input.** $X$, $y$ and the weights $w_1, \dots, w_n \ge 0$. The rows with $w_i > 0$ must give a matrix of rank $p$.

**Output.** The estimate, the weighted residual sum of squares, the variance estimate and the estimated covariance:

$$\hat b_W = \arg\min_\beta \sum_{i=1}^n w_i (y_i - x_i^\top\beta)^2 = (X^\top WX)^{-1}X^\top Wy, \qquad s^2 = \frac{\sum_i w_i e_i^2}{m - p}, \qquad \widehat{\operatorname{Cov}}(\hat b_W) = s^2 (X^\top WX)^{-1},$$

where $e_i = y_i - x_i^\top\hat b_W$ are the residuals on the original scale and $m$ is the number of positive weights.

## The algorithm

```pseudo id=main
WEIGHTED-LEAST-SQUARES(X[1..n, 1..p], y[1..n], w[1..n])
L1  for each i with w[i] > 0 do                  ▷ m such rows; rows with w[i] = 0 drop out
L2      x̃ᵢ ← √w[i] · xᵢ;  ỹᵢ ← √w[i] · y[i]
L3  (R, c) ← Householder QR of X̃, applied to ỹ    ▷ Qᵀ X̃ = (R; 0), c = Qᵀ ỹ
L4  b̂ ← solve R b = c[1..p] by back substitution
L5  RSS_w ← c[p+1]² + ... + c[m]²                 ▷ = Σ wᵢ eᵢ²
L6  s² ← RSS_w / (m - p)
L7  V ← s² · R⁻¹ R⁻ᵀ                              ▷ = s² (Xᵀ W X)⁻¹
L8  return (b̂, RSS_w, s², V)
```

Line L2 is the whole idea. If $\operatorname{Var}(\varepsilon_i) = \sigma^2/w_i$, then $\sqrt{w_i}\,\varepsilon_i$ has variance $\sigma^2$, so the scaled rows follow a model with equal variances, and the weighted sum of squares of the original rows is the plain sum of squares of the scaled rows. Lines L3 to L7 are the QR solution of [ordinary least squares](/ordinary-least-squares/) on the scaled rows. The code does not form $X^\top WX$: the [normal equations](/normal-equations/) square the condition number, and large weight ratios already make the scaled matrix badly conditioned. A $100\alpha\%$ interval for $b_j$ is $\hat b_j \pm t_{(m-p, 1-\alpha/2)}\sqrt{V_{jj}}$, with $t_{(m-p, 1-\alpha/2)}$ the lower $1 - \alpha/2$ quantile of the t law.

## Example

Take $x = (1, 2, 3, 4, 5)$, $y = (2, 5, 5, 9, 9)$, the model $y_i = b_0 + b_1 x_i + \varepsilon_i$ with $\operatorname{sd}(\varepsilon_i) \propto x_i$, so $w_i = 1/x_i^2 = (1, 1/4, 1/9, 1/16, 1/25)$.

Line L2 multiplies row $i$ by $1/x_i$. The scaled rows are $(1/x_i, 1)$ and the scaled responses are $y_i/x_i$:

| $i$ | $\sqrt{w_i}$ | scaled row | scaled response |
|---|---|---|---|
| 1 | 1 | (1, 1) | 2 |
| 2 | 1/2 | (0.5, 1) | 2.5 |
| 3 | 1/3 | (0.333, 1) | 1.667 |
| 4 | 1/4 | (0.25, 1) | 2.25 |
| 5 | 1/5 | (0.2, 1) | 1.8 |

So with these weights the slope $b_1$ becomes the intercept of a regression of $y/x$ on $1/x$. Exact arithmetic gives

$$\hat b_W = \Bigl(\tfrac{281}{1894}, \tfrac{14967}{7576}\Bigr) \approx (0.1484, 1.9756),$$

while ordinary least squares gives $(0.6, 1.8)$. The first point, the most precise one, pulls the weighted line down at small $x$. The weighted residual sum of squares is $0.44496$ with $m - p = 3$, so $s^2 = 0.14832$, $\operatorname{se}(\hat b_1) = 0.3212$, and the 95% interval for $b_1$ is $1.9756 \pm 3.1824 \cdot 0.3212 = (0.953, 2.998)$.

**Measured efficiency.** With $x = 1, 1.5, \dots, 10.5$ ($n = 20$), $y_i = 2 + 0.5x_i + \varepsilon_i$ and $\varepsilon_i \sim N(0, (0.3x_i)^2)$, $r = 2000$ samples from `random.Random(20261114)` gave: the WLS slope had variance $0.01074$ (theory $\sigma^2[(X^\top WX)^{-1}]_{22} = 0.01084$), the OLS slope $0.02565$ (theory $0.02597$), a ratio of $2.39$. The 95% WLS t interval covered the true slope in 95.2% of the samples, as the exact theory says; the OLS interval with the usual standard error covered it in 93.2%, because that standard error assumes equal variances.

## Correctness

Line L2 turns the weighted problem into an unweighted one with the same objective, because $w_i(y_i - x_i^\top\beta)^2 = (\sqrt{w_i}y_i - \sqrt{w_i}x_i^\top\beta)^2$, and the QR steps solve that problem exactly. The scaled errors $\sqrt{w_i}\varepsilon_i$ are uncorrelated with common variance $\sigma^2$, so the [Gauss-Markov theorem](/gauss-markov-theorem/) applies to the scaled model: $\hat b_W$ is unbiased with covariance $\sigma^2(X^\top WX)^{-1}$, and no other linear unbiased estimator has a smaller covariance in the Loewner order. Linear estimators in $y$ and in $W^{1/2}y$ are the same class, so the optimality transfers to the original model. Under normal errors the t intervals are exact. The proof is below.

## Complexity

For $m \ge p$ rows with positive weight, line L2 costs $\Theta(mp)$, the Householder QR of line L3 costs $2mp^2 - 2p^3/3 + O(mp)$ flops, back substitution $p^2$ flops and the covariance $\Theta(p^3)$. The total is $\Theta(np^2)$ in the real RAM model, the same as one ordinary least squares fit, and the extra space is $\Theta(np)$ for the scaled copy. Forming $X^\top WX$ instead costs about $mp^2$ flops, half as much, but squares the condition number.

## Properties

- **Only the ratios of the weights matter.** Replacing $w$ by $cw$ for a constant $c > 0$ leaves $\hat b_W$ and $\widehat{\operatorname{Cov}}(\hat b_W)$ unchanged; $s^2$ is multiplied by $c$.
- **Best linear unbiased for the right weights.** With $w_i \propto 1/\operatorname{Var}(\varepsilon_i)$, the covariance $\sigma^2(X^\top WX)^{-1}$ is the smallest among linear unbiased estimators. With wrong weights, $\hat b_W$ is still unbiased, but it is less efficient, and $s^2(X^\top WX)^{-1}$ is no longer a correct covariance.
- **Exact inference under normal errors.** With normal errors and the right weights, $(m - p)s^2/\sigma^2 \sim \chi^2_{m-p}$ independent of $\hat b_W$, so the t intervals and the [F-test](/regression-f-test/) on the scaled rows are exact.
- **Weighted residuals.** The residuals that have equal variance (up to leverage) are the scaled ones $\sqrt{w_i}e_i$. Diagnostics such as [leverage](/leverage-statistics/) and [studentized residuals](/studentized-residual/) are computed on the scaled rows, where the hat matrix is $W^{1/2}X(X^\top WX)^{-1}X^\top W^{1/2}$.

## Variants and improvements

- **Generalized least squares.** Correlated errors with $\operatorname{Cov}(\varepsilon) = \sigma^2V$ need a full whitening matrix instead of $W^{1/2}$; see [generalized least squares](/generalized-least-squares/).
- **Feasible weighted least squares.** When the variances are unknown, model them, for example $\operatorname{Var}(\varepsilon_i) = \sigma^2 \exp(z_i^\top\gamma)$, estimate $\gamma$ from the squared OLS residuals, and refit with $\hat w_i = \exp(-z_i^\top\hat\gamma)$. The estimate is no longer linear in $y$ and the exact results above do not apply; it is asymptotically as efficient as WLS with the true weights under regularity conditions. A [Breusch-Pagan test](/breusch-pagan-test/) checks whether a variance model is needed.
- **Iterated weights.** When the weights depend on the coefficients, as in generalized linear models and M-estimation, alternate between weights and fits: this is [iteratively reweighted least squares](/iteratively-reweighted-least-squares/).
- **Sandwich standard errors instead of weights.** If the variance pattern is unknown, keep OLS or a rough WLS and use [heteroscedasticity-consistent standard errors](/heteroscedasticity-consistent-standard-errors/), which stay valid when the weights are wrong.
- **Updating.** Adding or removing one weighted row is a rank-one change of $X^\top WX$; the [Sherman-Morrison formula](/sherman-morrison-formula/) or a QR update handles it in $O(p^2)$.

## When to use it

Use WLS when the error variances are known up to a common factor: each response is a mean of $k_i$ replicates ($w_i = k_i$), the variance comes from a known measurement process, or a physical model says that the spread grows like a known function of a predictor. If the pattern of the variances must be estimated from the same data, WLS with estimated weights plus a sandwich standard error is safer than trusting $s^2(X^\top WX)^{-1}$.

## Pitfalls

- **Three meanings of "weight".** Precision weights (this page) say that $\operatorname{Var}(\varepsilon_i) = \sigma^2/w_i$. Frequency weights say that row $i$ stands for $w_i$ identical observations: the estimate is the same, but the residual degrees of freedom are $\sum w_i - p$, not $m - p$. Sampling weights are inverse inclusion probabilities in a survey, as in the [Horvitz-Thompson estimator](/horvitz-thompson-estimator/): the estimate is the same again, but $s^2(X^\top WX)^{-1}$ is wrong and a sandwich or design-based variance is needed. Software that has one `weights` argument cannot know which you mean.
- **Weights that are variances.** The weight is the inverse of the variance. Using the variance itself gives the noisiest points the most influence.
- **Estimated weights treated as known.** Weights computed from the residuals of the same data make the t and F tests anticonservative in small samples.
- **Weights from a single point.** A weight that comes from a very small estimated variance (a group with two equal replicates) is huge and lets one observation fix the fit. Bound the weights or pool the variance estimates.
- **The normal equations.** Forming $X^\top WX$ squares the condition number, and weights that range over many orders of magnitude make that worse. Use QR on the scaled rows.
- **Zero and negative weights.** A zero weight removes the row and must not count in the degrees of freedom. A negative weight has no meaning as a precision, and the objective is then not convex; the code rejects it.

## Implementations

## History

Aitken (1935) proved that least squares weighted by the inverse of the error covariance matrix gives the linear unbiased estimate of minimum variance, which contains the diagonal case of this page. The computation by scaling the rows and solving with an orthogonal factorization is the standard numerical method of Golub and Van Loan, Section 5.3, applied to the scaled matrix.

## References
