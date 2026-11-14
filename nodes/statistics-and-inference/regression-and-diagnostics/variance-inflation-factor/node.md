---
tag: 1MY9SY
kind: definition
slug: variance-inflation-factor
name: Variance inflation factor
aliases:
- VIF
- multicollinearity diagnostic
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: 1 / (1 - R_j^2), where R_j^2 is from regressing predictor j on the others. It is the factor by which collinearity inflates the variance of coefficient j.
prereqs: [coefficient-of-determination, ordinary-least-squares]
see_also: [condition-number, ridge-regression, principal-component-analysis, lasso-regression, singular-value-decomposition, covariance-matrix, hat-matrix, regression-f-test]
sources:
  - paper: doi:10.1080/00401706.1970.10488699
    title: "Donald W. Marquardt, Generalized inverses, ridge regression, biased linear estimation, and nonlinear estimation, Technometrics 12(3), 1970, pp. 591 to 612"
    locator: The discussion of the diagonal of the inverse correlation matrix as variance inflation factors (often cited as the origin of the name and of the value 10 as a warning level)
  - paper: doi:10.1007/s11135-006-9018-6
    title: "Robert M. O'Brien, A caution regarding rules of thumb for variance inflation factors, Quality and Quantity 41(5), 2007, pp. 673 to 690"
    locator: The whole paper (why fixed cutoffs such as 4 or 10 are not justified, and how sample size and error variance offset a large VIF)
  - paper: doi:10.1080/01621459.1992.10475190
    title: "John Fox and Georges Monette, Generalized collinearity diagnostics, Journal of the American Statistical Association 87(417), 1992, pp. 178 to 183"
    locator: The whole paper (the generalized VIF for a set of columns as a ratio of determinants of correlation matrices)
  - book: isbn:9780471058564
    title: David A. Belsley, Edwin Kuh and Roy E. Welsch, Regression Diagnostics, Wiley, 1980
    locator: Chapter 3 (detecting and assessing collinearity, condition indexes and variance decomposition proportions)
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: The section on collinearity in Chapter 10 (variance inflation factors, the correlation matrix and its eigenvalues)
---

The variance inflation factor $\mathrm{VIF}_j$ of a predictor in a linear regression is $1/(1 - R_j^2)$, where $R_j^2$ is the [coefficient of determination](/coefficient-of-determination/) of predictor $j$ regressed on all the other predictors. It is the exact factor by which the variance of the least squares coefficient $\hat b_j$ is larger than it would be if predictor $j$ were uncorrelated with the others, for the same spread of $x_j$ and the same noise. $\mathrm{VIF}_j = 1$ means no collinearity for that column, and $\mathrm{VIF}_j = \infty$ means the column is an exact linear combination of the others. The square root of $\mathrm{VIF}_j$ is the inflation of the standard error and of the width of the confidence interval. The VIF describes the design matrix only. It says nothing about $y$, and a large VIF is not by itself a reason to drop a variable.

## Definition

Let $y = Xb + \varepsilon$ with $X$ an $n \times p$ matrix of rank $p$ whose first column is the intercept $\mathbf 1$ and whose other columns $x_1, \dots, x_{p-1}$ are the predictors. Assume the errors are uncorrelated with mean 0 and variance $\sigma^2$, and let $\hat b$ be the [ordinary least squares](/ordinary-least-squares/) estimate. For a predictor $j$, let $S_{jj} = \sum_i (x_{ij} - \bar x_j)^2 > 0$, and let $R_j^2$ be the $R^2$ of the least squares regression of $x_j$ on the intercept and the other $p - 2$ predictors. The **variance inflation factor** of predictor $j$ is

$$\mathrm{VIF}_j = \frac{1}{1 - R_j^2}.$$

Its reciprocal $1 - R_j^2$ is called the **tolerance**.

**Why the name is exact.** Let $\tilde x_j$ be the residual of $x_j$ after the regression on the other columns. By the Frisch-Waugh-Lovell argument, $\hat b_j = \tilde x_j^\top y/\tilde x_j^\top\tilde x_j$, so $\operatorname{Var}(\hat b_j) = \sigma^2/\lVert\tilde x_j\rVert^2$. Since $\lVert\tilde x_j\rVert^2 = S_{jj}(1 - R_j^2)$,

$$\operatorname{Var}(\hat b_j) = \frac{\sigma^2}{S_{jj}}\cdot\mathrm{VIF}_j.$$

The first factor, $\sigma^2/S_{jj}$, is the variance in a simple regression on $x_j$ alone, or in any design where $x_j$ is orthogonal to the other centered columns. So $\mathrm{VIF}_j$ is the inflation caused by the other predictors and nothing else. The same identity gives two equivalent formulas:

$$\mathrm{VIF}_j = S_{jj}\,[(X^\top X)^{-1}]_{jj} = [C^{-1}]_{jj},$$

where $C$ is the $(p-1) \times (p-1)$ correlation matrix of the predictors. The second form is the one Marquardt (1970) used.

**Facts.**

1. $\mathrm{VIF}_j \ge 1$, with equality if and only if $x_j - \bar x_j\mathbf 1$ is orthogonal to every other centered predictor.
2. With two predictors, both have $\mathrm{VIF} = 1/(1 - r^2)$, where $r$ is their correlation.
3. $\mathrm{VIF}_j$ does not change when any predictor is shifted or rescaled, because $R_j^2$ does not.
4. If the eigenvalues of $C$ are $\lambda_1 \ge \dots \ge \lambda_{p-1} > 0$, then $\max_j \mathrm{VIF}_j \le 1/\lambda_{p-1}$ and $\sum_j \mathrm{VIF}_j = \sum_k 1/\lambda_k$. A small eigenvalue of $C$ means a near linear dependence, and the VIFs show which columns take part in it.
5. The VIF of the intercept is not defined in this way, because the intercept column has $S_{jj} = 0$.

**Thresholds are conventions.** Values above 10 (or 5) are often called a sign of serious collinearity. The value 10 is usually attributed to Marquardt (1970); we did not confirm the exact wording there. No threshold has a theoretical basis: the variance of $\hat b_j$ also depends on $\sigma^2$ and $S_{jj}$, which grows with $n$. A coefficient with $\mathrm{VIF} = 20$ from a large, well spread sample can be more precise than one with $\mathrm{VIF} = 1$ from a small sample (O'Brien 2007).

## Examples and non-examples

**Two predictors.** For $x_1 = (1, 2, 3, 4, 5)$ and $x_2 = (2, 1, 4, 3, 6)$, $S_{11} = 10$, $S_{22} = 14.8$ and the cross product is 10, so $r^2 = 100/148 = 25/37$ and both VIFs are $37/12 = 3.08$. The standard errors are $\sqrt{3.08} = 1.76$ times what an orthogonal design with the same spreads would give.

**Near dependence.** Add $x_3 = (3, 4, 7, 7, 11)$, which equals $x_1 + x_2$ except in the second entry. Then $R_1^2 = 1687/1735$, $R_2^2 = 1099/1147$ and $R_3^2 = 97/98$, so

$$\mathrm{VIF} = (36.15,\ 23.90,\ 98.0).$$

Each value agrees with $S_{jj}[(X^\top X)^{-1}]_{jj}$ computed in exact rational arithmetic. All three columns take part in the dependence, and all three are inflated. The standard error of $\hat b_3$ is $\sqrt{98} \approx 9.9$ times the orthogonal value.

**From a fitted model.** In the [regression F-test](/regression-f-test/) example, with $x_1 = 1, \dots, 8$ and $x_2 = (3, 1, 4, 1, 5, 9, 2, 6)$, the squared correlation is $r^2 = 75/329$ and both VIFs are $329/254 = 1.30$: mild collinearity.

**Non-essential collinearity.** For $x = (1, 2, 3, 4, 5)$, the columns $x$ and $x^2$ have $r^2 = 3600/3740$ and $\mathrm{VIF} = 3740/140 = 26.7$. With the centered $u = x - 3$, the columns $u$ and $u^2 = (4, 1, 0, 1, 4)$ have $r = 0$ and $\mathrm{VIF} = 1$. The fitted values and the quadratic coefficient are the same in both fits; only the meaning and variance of the linear coefficient change. A large VIF caused by a choice of origin is a property of the parametrization, not of the data.

**Non-example: an uncentered VIF.** Some programs compute $\lVert x_j\rVert^2[(X^\top X)^{-1}]_{jj}$ without centering, or include the intercept. Then shifting $x_j$ by a constant changes the value, and a predictor that lies far from 0 shows a large "VIF" with no collinearity among the predictors. The [condition number](/condition-number/) of the scaled, uncentered $X$ (Belsley, Kuh and Welsch) is the diagnostic that is meant to include the intercept.

**Non-example: a test.** The VIF has no null distribution and no level. It also does not tell whether predictions are harmed: inside the region where the data lie, fitted values can be precise when the individual coefficients are not.

## Related definitions

- **[Coefficient of determination](/coefficient-of-determination/).** $R_j^2$ is an ordinary $R^2$, with $x_j$ as the response.
- **Condition indexes.** Belsley, Kuh and Welsch scale the columns of $X$ to unit length, take the singular values $\mu_1 \ge \dots \ge \mu_p$ from the [singular value decomposition](/singular-value-decomposition/), and use $\mu_1/\mu_k$ together with the share of each $\operatorname{Var}(\hat b_j)$ that comes from each singular value. Where the VIF says which coefficient is hurt, the variance decomposition proportions say which dependence hurts it.
- **Generalized VIF.** For a set of columns that belong together, such as the indicator columns of one factor, Fox and Monette (1992) define $\mathrm{GVIF} = \det C_{11}\det C_{22}/\det C$, where $C_{11}$ is the correlation block of the set and $C_{22}$ that of the rest. It is invariant to the coding of the set, and $\mathrm{GVIF}^{1/(2d)}$ for a set of $d$ columns is comparable to $\sqrt{\mathrm{VIF}}$.
- **Remedies.** [Ridge regression](/ridge-regression/) adds $\lambda I$ to the correlation matrix and so lowers the variance of every coefficient; the [lasso](/lasso-regression/) selects among correlated columns; regression on leading [principal components](/principal-component-analysis/) removes the small-eigenvalue directions. All three trade bias for variance. Centering, more data in the missing directions, or a combined variable remove the cause.
- **[Covariance matrix](/covariance-matrix/) of $\hat b$.** $\sigma^2(X^\top X)^{-1}$; the VIFs are its diagonal, rescaled by $S_{jj}/\sigma^2$.

## References
