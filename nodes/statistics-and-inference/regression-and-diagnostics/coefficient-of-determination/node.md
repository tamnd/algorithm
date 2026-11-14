---
tag: DCG94B
kind: definition
slug: coefficient-of-determination
name: Coefficient of determination
aliases:
- R-squared
- adjusted R-squared
area: statistics-and-inference/regression-and-diagnostics
level: intro
summary: The fraction of the variance of the response that the regression explains, one minus the residual sum of squares over the total sum of squares.
prereqs: [ordinary-least-squares]
see_also: [regression-f-test, variance-inflation-factor, linear-regression, mean-squared-error, cross-validation, akaike-information-criterion, generalized-linear-model, one-way-anova]
sources:
  - paper: doi:10.1080/00031305.1985.10479448
    title: "Tarald O. Kvålseth, Cautionary note about R^2, The American Statistician 39(4), 1985, pp. 279 to 285"
    locator: The whole paper (the competing formulas for R^2, their disagreement without an intercept, and the recommended definition 1 - RSS/TSS)
  - paper: doi:10.1080/00031305.1973.10478966
    title: "F. J. Anscombe, Graphs in statistical analysis, The American Statistician 27(1), 1973, pp. 17 to 21"
    locator: The four data sets with the same fitted line and the same correlation but very different shapes
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: Chapter 4 (the sums of squares of the fit, the multiple correlation coefficient and the overall F-test)
---

The coefficient of determination $R^2$ of a least squares fit with an intercept is the fraction of the variation of the response around its mean that the fitted values account for: $R^2 = 1 - \mathrm{RSS}/\mathrm{TSS}$. It lies between 0 and 1, equals the squared correlation between $y$ and $\hat y$, and in simple regression equals the squared correlation between $x$ and $y$. Adding a predictor never lowers it, so the adjusted $R^2$ divides each sum of squares by its degrees of freedom. $R^2$ measures how much of the spread a linear fit removes in this sample. It does not measure whether the model is right, and a low value does not mean the slopes are 0. The test of that question is the [F-test](/regression-f-test/).

## Definition

Let $y$ be the $n$-vector of responses, $X$ an $n \times p$ design matrix of rank $p$ whose $p$ columns include the intercept column $\mathbf 1$, $\hat y$ the [ordinary least squares](/ordinary-least-squares/) fitted values, $e = y - \hat y$ and $\bar y$ the mean of $y$. Define

$$\mathrm{TSS} = \sum_{i=1}^n (y_i - \bar y)^2, \qquad \mathrm{RSS} = \sum_{i=1}^n e_i^2, \qquad \mathrm{ESS} = \sum_{i=1}^n (\hat y_i - \bar y)^2.$$

With an intercept, $\mathbf 1^\top e = 0$ and $\hat y^\top e = 0$, so $\mathrm{TSS} = \mathrm{ESS} + \mathrm{RSS}$. Assume $\mathrm{TSS} > 0$. The **coefficient of determination** is

$$R^2 = 1 - \frac{\mathrm{RSS}}{\mathrm{TSS}} = \frac{\mathrm{ESS}}{\mathrm{TSS}}.$$

The **adjusted** coefficient replaces each sum of squares by its unbiased variance estimate under the model:

$$\bar R^2 = 1 - \frac{\mathrm{RSS}/(n - p)}{\mathrm{TSS}/(n - 1)} = 1 - (1 - R^2)\frac{n - 1}{n - p}.$$

With $k = p - 1$ slopes this is $1 - (1 - R^2)(n - 1)/(n - k - 1)$, the form in many texts.

**Facts.** For a model with an intercept:

1. $0 \le R^2 \le 1$. $R^2 = 1$ if and only if $e = 0$; $R^2 = 0$ if and only if all fitted slopes are 0, so $\hat y = \bar y\mathbf 1$.
2. $R^2 = \operatorname{corr}(y, \hat y)^2$, the squared multiple correlation coefficient. In simple regression, $R^2 = \operatorname{corr}(x, y)^2$.
3. Adding a column to $X$ never increases RSS (the old fit is still available), so $R^2$ never decreases. $\bar R^2$ increases if and only if the t statistic of the new coefficient satisfies $|t| > 1$, and it can be negative.
4. The overall F statistic is a monotone function of $R^2$: $F = \frac{R^2/(p - 1)}{(1 - R^2)/(n - p)}$.
5. If the errors are iid normal and all slopes are 0, $R^2$ has the Beta$\big(\frac{p-1}{2}, \frac{n-p}{2}\big)$ law, with mean $(p - 1)/(n - 1)$. So pure noise gives a positive $R^2$ on average, and $E[\mathrm{RSS}/(n - p)] = E[\mathrm{TSS}/(n - 1)] = \sigma^2$ is the reason $\bar R^2$ is centered near 0 in that case.

## Examples and non-examples

**Five points.** For $x = (1, 2, 3, 4, 5)$ and $y = (1, 3, 2, 5, 4)$: $\bar y = 3$, $\mathrm{TSS} = 10$, the fit is $\hat y = 0.6 + 0.8x$, $\mathrm{RSS} = 3.6$, so $R^2 = 0.64$, which is $\operatorname{corr}(x, y)^2 = 0.8^2$. With $n = 5$ and $p = 2$, $\bar R^2 = 1 - 0.36 \cdot 4/3 = 0.52$.

**A useless predictor.** Add the column $z = (2, -1, 0, 1, -2)$, unrelated to the story. RSS drops to 3.5, so $R^2$ rises to 0.65, while $\bar R^2 = 1 - 0.35 \cdot 4/2 = 0.30$ falls.

**Out-of-sample.** The leave-one-out version, $1 - \mathrm{PRESS}/\mathrm{TSS}$ with $\mathrm{PRESS} = \sum_i e_i^2/(1 - h_{ii})^2$, is $1 - 9.057/10 = 0.094$ for the five points: most of the in-sample 0.64 does not survive prediction of new points. On a test set, $1 - \sum(y_i - \hat y_i)^2/\sum(y_i - \bar y)^2$ can be negative.

**The same $R^2$ for four different pictures.** In each of Anscombe's four data sets of 11 points, the fitted line is close to $\hat y = 3 + 0.5x$ and $R^2 = 0.667$ to three digits. One set is a linear cloud, one an exact parabola, one a line with one outlier, and one a vertical stack with a single far point that decides the slope. $R^2$ cannot tell them apart; a plot can.

**Range dependence.** In simple regression with slope $b_1$ and error variance $\sigma^2$, the population value is $b_1^2\operatorname{Var}(x)/(b_1^2\operatorname{Var}(x) + \sigma^2)$. The same law, sampled over a wider range of $x$, gives a larger $R^2$. Comparing $R^2$ across studies with different designs compares the designs as much as the models.

**Non-example: a fit without an intercept.** Fit $y = (5, 4, 3, 2, 1)$ on $x = (1, 2, 3, 4, 5)$ through the origin. The slope is $7/11$ and $\mathrm{RSS} = 360/11 = 32.73$, larger than $\mathrm{TSS} = 10$, so $1 - \mathrm{RSS}/\mathrm{TSS} = -2.27$. The decomposition $\mathrm{TSS} = \mathrm{ESS} + \mathrm{RSS}$ fails because $\mathbf 1^\top e \ne 0$. Many programs then report the uncentered $1 - \mathrm{RSS}/\sum y_i^2 = 0.405$, which compares the fit with the zero model, not with the mean, and is not comparable with an ordinary $R^2$. Kvålseth (1985) lists eight formulas that agree with an intercept and disagree without it.

**Non-example: a large $R^2$ as proof of a good model.** A curved relation fitted by a line, trending time series, or many predictors for few points all give a high $R^2$. A low $R^2$ with a clearly nonzero slope is common when the noise is large, and the slope can still be estimated well.

## Related definitions

- **Overall [F-test](/regression-f-test/).** Tests whether all slopes are 0. It is a function of $R^2$, $n$ and $p$; $R^2$ alone has no level.
- **Partial $R^2$.** $(\mathrm{RSS}_0 - \mathrm{RSS}_1)/\mathrm{RSS}_0$ for a nested pair of models: the fraction of the remaining variation that the added columns remove.
- **$R_j^2$ and the [variance inflation factor](/variance-inflation-factor/).** The $R^2$ of predictor $j$ regressed on the other predictors, with $\mathrm{VIF}_j = 1/(1 - R_j^2)$.
- **Pseudo-$R^2$.** For a [generalized linear model](/generalized-linear-model/) there is no unique analogue; McFadden's $1 - \log L_1/\log L_0$ and the deviance-based versions are common, and they are not on the same scale as $R^2$.
- **[Mean squared error](/mean-squared-error/).** $\mathrm{RSS}/n$; $R^2$ is one minus the ratio of the mean squared error of the fit to that of the constant predictor $\bar y$.
- **[Cross-validation](/cross-validation/) and information criteria.** For model choice, out-of-sample error or the [Akaike information criterion](/akaike-information-criterion/) penalize size properly; $\bar R^2$ penalizes it weakly.

## References
