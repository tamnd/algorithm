---
tag: KE7D2K
kind: algorithm
slug: regression-f-test
name: F-test for nested linear models
aliases:
- overall F-test
- partial F-test
- extra sum of squares test
area: statistics-and-inference/regression-and-diagnostics
level: intro
summary: Compares a linear model with a nested smaller one by the drop in residual sum of squares per extra parameter over the residual variance. Exact F law under normal errors. One QR, O(n p^2).
model: real-ram
complexity:
  vars: {n: the number of observations, p: "the number of columns of the full design matrix, with p < n"}
  time: {worst: Θ(n p^2), best: Θ(n p^2)}
  space: {extra: Θ(n p)}
  flops: {worst: "2n p^2 - 2p^3/3 + O(n p)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1925
  people: [Ronald A. Fisher, George W. Snedecor]
  note: Fisher built the analysis of variance and its z test, which he applied to regression, in Statistical Methods for Research Workers (1925). Snedecor tabulated the variance ratio in 1934 and named it F after Fisher.
prereqs: [ordinary-least-squares, coefficient-of-determination, statistical-hypothesis-test, p-value, qr-decomposition]
see_also: [student-t-test, one-way-anova, likelihood-ratio-test, wald-test, heteroscedasticity-consistent-standard-errors, stepwise-regression, householder-reflections, normal-equations]
sources:
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: Chapter 4 (hypothesis testing in the linear model, the F-test of a linear hypothesis from the restricted least squares fit)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.2 (the Householder QR factorization) and Section 5.3 (the full-rank least squares problem and its residual from Q^T b)
  - url: https://psychclassics.yorku.ca/Fisher/Methods/
    title: Ronald A. Fisher, Statistical Methods for Research Workers, Oliver and Boyd, 1925, online text of the first edition
    locator: Chapters VII and VIII (the analysis of variance and its test, including the test of a fitted regression)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Chapter 7 (linear hypotheses, the canonical form by an orthogonal transformation and the F-test as the uniformly most powerful invariant test)
---

The F-test for nested linear models decides whether some coefficients of a linear model are 0, or more generally whether a smaller model, whose column space lies inside that of a larger one, fits as well as the larger model. It compares the drop in the residual sum of squares per removed parameter with the residual variance of the larger model. Under normal errors with equal variance and the null hypothesis, the ratio has the F distribution with $q$ and $n - p$ degrees of freedom exactly. The overall F-test (all slopes 0) and the partial F-test (one group of predictors) are special cases, and with one restriction the test is the two-sided t-test of one coefficient. This page owns the test; the fit itself is on the [ordinary least squares](/ordinary-least-squares/) page.

## In plain words

You fitted a straight-line rule with several inputs and want to know if some of the inputs help at all. Fit the rule twice: once with them and once without them. Without them, the fit can only be worse, so the leftover error grows a little even if the inputs are useless. The question is whether it grows more than chance would make it grow. The test divides the growth per dropped input by the leftover error per remaining degree of freedom of the big model. If the dropped inputs are useless and the errors are bell-shaped with equal spread, this ratio has a known law, the F law, so a large ratio is evidence that they help. One QR factorization of the big model gives both fits at once.

## The problem

**Model.** $y = Xb + \varepsilon$, where $X$ is a fixed $n \times p$ matrix of rank $p < n$ (its $p$ columns include the intercept column if there is one), $b \in \mathbb{R}^p$ is the coefficient vector, and $\varepsilon \sim N(0, \sigma^2 I_n)$ with $\sigma$ unknown. Order the columns so that the first $p_0$ form the null design $X_0$, $0 \le p_0 < p$, and let $q = p - p_0$ and $\nu = n - p$.

**Hypotheses.** $H_0$: the last $q$ coefficients are 0, so $\mathbb{E}[y] \in \operatorname{col}(X_0)$; $H_1$: they are not all 0. The general linear hypothesis $H_0: Rb = r$, with $R$ a $q \times p$ matrix of rank $q$, reduces to this form by a change of basis (see Variants).

**Statistic.** With $\mathrm{RSS}_1 = \min_\beta \lVert y - X\beta\rVert^2$ and $\mathrm{RSS}_0 = \min_\gamma \lVert y - X_0\gamma\rVert^2$,

$$F = \frac{(\mathrm{RSS}_0 - \mathrm{RSS}_1)/q}{\mathrm{RSS}_1/(n - p)} = \frac{(\mathrm{RSS}_0 - \mathrm{RSS}_1)/q}{s^2}, \qquad s^2 = \frac{\mathrm{RSS}_1}{n - p}.$$

**Null distribution.** Exact: $F \sim F_{q, n-p}$ under $H_0$, for every $b_0$ and every $\sigma$. Reject at level $\alpha$ when $F \ge F_{(q, n-p, 1-\alpha)}$, the upper $\alpha$ point (lower $1 - \alpha$ quantile) of $F_{q, n-p}$. The test is one-sided in $F$: a large $F$ is evidence against $H_0$, and a small one is not.

**Special cases.** The overall F-test has $X_0 = \mathbf 1$ (intercept only), $q = p - 1$, and then $\mathrm{RSS}_0 = \mathrm{TSS}$, so $F = \frac{R^2/(p - 1)}{(1 - R^2)/(n - p)}$ with $R^2$ the [coefficient of determination](/coefficient-of-determination/). The partial F-test drops one group of predictors. With one dropped column, $F = t^2$ for the t statistic of that coefficient, and the F-test and the two-sided t-test agree. [One-way ANOVA](/one-way-anova/) is the overall F-test on group indicator columns.

## The algorithm

```pseudo id=main
REGRESSION-F-TEST(X[1..n, 1..p], y[1..n], p₀)   ▷ the first p₀ columns span the null model
L1  for j ← 1 to p do                           ▷ Householder QR of X, applied to y
L2      a ← X[j..n, j];  α ← −sign(a₁)·‖a‖;  v ← a − α·e₁   ▷ ‖a‖ = 0 means rank < p
L3      apply I − 2vvᵀ/(vᵀv) to columns j..p of X, rows j..n
L4      apply the same reflection to y[j..n]     ▷ after the loop y holds c = Qᵀy
L5  RSS₁ ← c[p+1]² + ... + c[n]²
L6  ΔSS ← c[p₀+1]² + ... + c[p]²                  ▷ = RSS₀ − RSS₁
L7  q ← p − p₀;  ν ← n − p
L8  F ← (ΔSS / q) / (RSS₁ / ν)
L9  return (F, q, ν, Ḡ_{q,ν}(F))
```

The key fact is that the first $k$ columns of $Q$ span the first $k$ columns of $X$ for every $k$. So one factorization of the full design gives the residual sum of squares of every model made of a leading set of columns: $\mathrm{RSS}$ of the first $k$ columns is $\sum_{i > k} c_i^2$. Line L6 therefore needs no second fit. The tail is $\bar G_{q,\nu}(f) = P(F_{q,\nu} > f) = I_{\nu/(\nu + qf)}(\nu/2, q/2)$, the regularized incomplete beta function, which the helper evaluates directly, so a p-value of $10^{-15}$ keeps its digits. If $\mathrm{RSS}_1 = 0$ and $\Delta\mathrm{SS} > 0$ the code returns $F = \infty$ and $p = 0$; if both are 0, $F$ is undefined and the code raises an error, as it does for $q = 0$, $n = p$ or a rank-deficient $X$.

The implementation also has the Wald form for $Rb = r$, which uses $(X^\top X)^{-1} = R_{\text{QR}}^{-1}R_{\text{QR}}^{-\top}$ from the same factorization, and the t statistics of the single coefficients.

## Example

Eight observations, two predictors and an intercept, so $p = 3$ and $\nu = 5$:

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $x_{1}$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| $x_{2}$ | 3 | 1 | 4 | 1 | 5 | 9 | 2 | 6 |
| $y$ | 3 | 5 | 6 | 6 | 9 | 13 | 10 | 14 |

The columns are ordered $(\mathbf 1, x_1, x_2)$. The least squares fit is $\hat y = 0.7647 + 1.2310\,x_1 + 0.5022\,x_2$.

| line | value |
|---|---|
| L1 to L4: diagonal of $R$ | $-2.8284,\ 6.4807,\ -6.3892$ |
| L4: $c = Q^\top y$ | $-23.3345,\ 9.7211,\ -3.2086,\ -0.1676,\ -0.0363,\ 1.0949,\ 0.0814,\ 1.2126$ |
| $c_1^2 = n\bar y^2$ | $544.5$ |
| $c_2^2$ = drop in RSS from adding $x_1$ to the intercept | $94.5$ |
| $c_3^2$ = drop in RSS from adding $x_2$ | $10.2948$ |
| L5: $\mathrm{RSS}_1 = c_4^2 + \dots + c_8^2$ | $2.7052$ |
| $s^2 = 2.7052/5$ | $0.54103$ |

**Overall F-test** ($p_0 = 1$, $q = 2$): $\Delta\mathrm{SS} = 94.5 + 10.2948 = 104.7948$, which equals $\mathrm{TSS} - \mathrm{RSS}_1 = 107.5 - 2.7052$. Then $F = (104.7948/2)/0.54103 = 96.847$ with p-value $1.0045 \times 10^{-4}$, far above $F_{(2, 5, 0.95)} = 5.7861$. Also $R^2 = 0.97484$, and $\frac{R^2/2}{(1 - R^2)/5}$ gives the same 96.847.

**Partial F-test for $x_2$** ($p_0 = 2$, $q = 1$): $F = 10.2948/0.54103 = 19.028$, p-value $0.0072757$, above $F_{(1, 5, 0.95)} = 6.6079$. The t statistic of $x_2$ is $\hat b_2/\operatorname{se}(\hat b_2) = 0.5022/0.11512 = 4.3621$, and $4.3621^2 = 19.028$. The residual sum of squares of the intercept and $x_1$ model, fitted on its own, is $13 = 10.2948 + 2.7052$, as line L6 says.

**A hypothesis that is not a deletion.** $H_0: b_1 = b_2$ has $R = (0, 1, -1)$. The Wald form gives $F = 12.033$ with $q = 1$ and p-value $0.0179$, and the nested form on the design $(\mathbf 1, x_1 + x_2, x_2)$ with $p_0 = 2$ gives the same number.

**Size under the model and outside it.** Monte Carlo with $r = 4000$ replications at level 0.05 (standard error of an estimated size near 0.05: 0.0034); design with an intercept and three uniform predictors, testing the last two ($q = 2$):

| errors | $n$ | measured size | seed |
|---|---|---|---|
| normal, equal variance | 12 | 0.0450 | 1 |
| centered exponential, equal variance | 12 | 0.0400 | 2 |
| $t_3$, equal variance | 12 | 0.0485 | 3 |
| normal, sd $0.1 + 3x_3^2$ | 12 | 0.1240 | 4 |
| normal, sd $0.1 + 3x_3^2$ | 60 | 0.0583 | 5 |

The exactness is proved for the first row; the other rows are measurements. Non-normal errors with equal variance moved the size little here. Variance that depends on a tested predictor more than doubled it at $n = 12$.

## Correctness

Householder reflections are orthogonal, so $Q^\top$ keeps lengths, and $\lVert y - X\beta\rVert^2 = \lVert c_{1..p} - R\beta\rVert^2 + \sum_{i > p} c_i^2$. The first term can be made 0, so $\mathrm{RSS}_1 = \sum_{i>p} c_i^2$; the same argument for the first $p_0$ columns, whose factor is the leading block of $R$, gives $\mathrm{RSS}_0 = \sum_{i > p_0} c_i^2$. Under normal errors, $c = Q^\top y$ is a normal vector with covariance $\sigma^2 I$, so its coordinates are independent. Its mean is 0 below row $p$, and under $H_0$ also below row $p_0$. So $\Delta\mathrm{SS}/\sigma^2$ and $\mathrm{RSS}_1/\sigma^2$ are independent chi-square variables with $q$ and $n - p$ degrees of freedom, and their scaled ratio is $F_{q, n-p}$ by definition; $\sigma$ cancels. The p-value is the upper tail of a continuous law, so it is uniform under $H_0$ and the size is exactly $\alpha$. A Lagrange multiplier argument shows that the restricted fit under $Rb = r$ raises the residual sum of squares by exactly $(R\hat b - r)^\top[R(X^\top X)^{-1}R^\top]^{-1}(R\hat b - r)$, so the Wald and nested forms agree. The proofs are in the correctness proof below.

## Complexity

On a [real RAM](/real-ram/), step $j$ of the loop updates the $(n - j + 1) \times (p - j + 1)$ trailing block at about 4 flops per entry, which sums to $2np^2 - 2p^3/3$ flops; applying the reflections to $y$ adds $O(np)$, and lines L5 to L8 cost $O(n)$. So the time is $\Theta(np^2)$, the same as one least squares fit, and the extra space is $\Theta(np)$ for the working copy of $X$ (it can overwrite $X$, as LAPACK does). Fitting the two models separately would cost about $2np^2 + 2np_0^2$ flops; the nested order of columns makes the second fit free. The F tail costs a number of continued fraction steps that does not grow with $n$.

**Numerical stability.** The textbook route forms $X^\top X$ and solves the [normal equations](/normal-equations/). That squares the [condition number](/condition-number/) of $X$, and the subtraction $\mathrm{RSS}_0 - \mathrm{RSS}_1$ of two nearly equal numbers can lose the digits that remain. Householder QR is backward stable, and line L6 computes the difference as a sum of squares, which has no cancellation. With nearly collinear predictors (see [variance inflation factor](/variance-inflation-factor/)), this is the difference between a correct F and a negative one.

## Properties

- **Exact under normality.** Size $\alpha$ for every $n > p$, every $\sigma$ and every value of the null coefficients.
- **Invariant.** $F$ does not change when $y$ is replaced by $ay + X_0 g$ ($a \ne 0$), when the columns of $X_0$ are replaced by a nonsingular combination of them, when the tested columns are changed by a nonsingular combination plus a combination of $X_0$, or when the rows are permuted.
- **Equal to the likelihood ratio test.** For normal errors, the likelihood ratio is $(\mathrm{RSS}_0/\mathrm{RSS}_1)^{n/2} = (1 + qF/(n-p))^{n/2}$, an increasing function of $F$, so the two tests are the same test. Among tests invariant under the transformations above, it is uniformly most powerful (Lehmann and Romano, Chapter 7).
- **Power.** Under $H_1$, $F$ has the noncentral F law with noncentrality $\lambda = \lVert (I - H_0)Xb\rVert^2/\sigma^2$, where $H_0$ is the projection on $\operatorname{col}(X_0)$; the power increases with $\lambda$.
- **One restriction is the t-test.** With $q = 1$ the F-test is the two-sided t-test of $b_p = 0$, and the p-values coincide.

## Variants and improvements

- **General linear hypothesis.** $H_0: Rb = r$. The Wald form $F = (R\hat b - r)^\top[R(X^\top X)^{-1}R^\top]^{-1}(R\hat b - r)/(qs^2)$ needs only the full fit. It equals the nested F of the restricted model, which the [Wald test](/wald-test/) and [likelihood ratio test](/likelihood-ratio-test/) pages treat in general models.
- **Sequential (type I) sums of squares.** The squares $c_{p_0+1}^2, \dots, c_p^2$ are the drops in RSS as the columns enter one by one, in the given order. They depend on the order unless the columns are orthogonal; this is the analysis of variance table of a regression.
- **Robust standard errors.** Under [heteroscedasticity](/heteroscedasticity/) replace $s^2(X^\top X)^{-1}$ in the Wald form by a [heteroscedasticity-consistent](/heteroscedasticity-consistent-standard-errors/) estimate and compare $qF$ with $\chi^2_q$. This is valid only asymptotically.
- **Permutation and bootstrap versions.** Permute the residuals of the null model (Freedman and Lane) or resample them to get a null law without normality; see [permutation test](/permutation-test/) and [bootstrap method](/bootstrap-method/).
- **Model search.** [Stepwise regression](/stepwise-regression/) uses partial F statistics to add and drop variables, and [leaps and bounds](/leaps-and-bounds/) searches all subsets. The p-values of the chosen model are then not valid, because the data chose the hypothesis.

## When to use it

Use the F-test to test several coefficients at once (a group of dummy variables for one factor, a set of polynomial terms, all slopes) in a linear model with errors that are close to normal and of equal variance, or with a large $n$ and no high leverage points. Use it instead of several t-tests, which do not control the error rate of the joint question. For a single coefficient it is the t-test. For non-nested models use an information criterion such as the [Akaike information criterion](/akaike-information-criterion/), not an F-test. For generalized linear models, use the [likelihood ratio test](/likelihood-ratio-test/) on the deviance.

## Pitfalls

- **Non-nested models.** $\mathrm{RSS}_0 - \mathrm{RSS}_1$ can be negative, and the F law does not hold.
- **Heteroscedasticity.** The test is not valid even asymptotically; the table shows a size of 0.124 instead of 0.05.
- **Reading a small F as support for $H_0$.** A non-significant F says that the data cannot tell the models apart, not that the dropped coefficients are 0.
- **Testing after selection.** Choosing the variables with the data and then testing them with the same data gives p-values that are too small.
- **Wrong degrees of freedom.** The denominator uses $n - p$ of the full model, with $p$ counting the intercept. Software that reports "$k$ predictors" means $p = k + 1$.
- **Forming $X^\top X$.** The normal equations can give a negative $\Delta\mathrm{SS}$ with nearly collinear columns; use QR.
- **Order in sequential tables.** A sequential sum of squares tests a column given only the columns before it; it answers a different question for each order.

## Implementations

## History

Fisher developed the analysis of variance in the early 1920s and set it out, with its z test and its use for testing a fitted regression, in Statistical Methods for Research Workers (1925). His statistic was $z = \tfrac12 \log F$. George W. Snedecor tabulated the variance ratio itself in his 1934 booklet on the analysis of variance and named it F in honor of Fisher. The geometric view of the test as the comparison of two orthogonal projections, and its computation from a QR factorization, came with the numerical linear algebra of the 1960s, after Householder (1958) and Golub (1965) made orthogonal factorizations the standard method for least squares.

## References
