---
tag: V6W589
kind: concept
slug: heteroscedasticity
name: Heteroscedasticity
aliases:
- heteroskedasticity
- non-constant variance
area: statistics-and-inference/regression-and-diagnostics
level: intro
summary: Errors whose variance changes with the predictors. Least squares stays unbiased but its usual standard errors are wrong.
prereqs: [ordinary-least-squares, gauss-markov-theorem]
see_also: [weighted-least-squares, generalized-least-squares, heteroscedasticity-consistent-standard-errors, breusch-pagan-test, box-cox-transformation, studentized-residual, generalized-linear-model, regression-f-test]
sources:
  - paper: doi:10.2307/1912934
    title: "Halbert White, A heteroskedasticity-consistent covariance matrix estimator and a direct test for heteroskedasticity, Econometrica 48(4), 1980, pp. 817 to 838"
    locator: The whole paper (the sandwich estimator of the covariance of least squares, its consistency without a model for the variance, and the direct test)
  - paper: doi:10.2307/1911963
    title: "T. S. Breusch and A. R. Pagan, A simple test for heteroscedasticity and random coefficient variation, Econometrica 47(5), 1979, pp. 1287 to 1294"
    locator: The whole paper (the score test that regresses the squared residuals on candidate variables)
  - paper: doi:10.1016/0304-4076(85)90158-7
    title: "James G. MacKinnon and Halbert White, Some heteroskedasticity-consistent covariance matrix estimators with improved finite sample properties, Journal of Econometrics 29(3), 1985, pp. 305 to 325"
    locator: The whole paper (the HC1, HC2 and HC3 corrections and their finite sample behavior)
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: Chapter 10 (departures from the assumptions, unequal variances, their detection and weighted least squares)
---

Heteroscedasticity means that the errors of a regression do not all have the same variance: $\operatorname{Var}(\varepsilon_i) = \sigma_i^2$ changes from observation to observation, usually with a predictor or with the mean of the response. The opposite, one common $\sigma^2$, is homoscedasticity, and it is one of the assumptions of the [Gauss-Markov theorem](/gauss-markov-theorem/) and of the exact t and F tests. Under heteroscedasticity, [ordinary least squares](/ordinary-least-squares/) is still unbiased and consistent, but its usual standard errors estimate the wrong quantity, so its confidence intervals and tests have the wrong level, and in general a weighted fit has smaller variance. The remedies are to model the variance and weight, to keep least squares and use a sandwich standard error, or to transform the response.

## In plain words

Think of predicting spending from income. People with low incomes all spend about the same; people with high incomes differ a lot. The points fan out as income grows. A straight line through them is still aimed correctly on average. But the usual formula for its uncertainty uses one average spread for every point, so it is too sure about the part of the line that the noisy points decide. Points with small spread carry more information than points with large spread, and a fit that weights them more is more precise. Either we say how the spread changes and weight, or we use an error formula that measures the spread at each point from the data.

## The idea

**The model.** $y = Xb + \varepsilon$ with $X$ an $n \times p$ matrix of rank $p$ (the intercept is one of the $p$ columns), $E[\varepsilon] = 0$, and $\operatorname{Cov}(\varepsilon) = \Sigma = \operatorname{diag}(\sigma_1^2, \dots, \sigma_n^2)$. Homoscedasticity is $\Sigma = \sigma^2 I$. Heteroscedasticity is every other diagonal $\Sigma$. The errors are still uncorrelated; correlated errors are a different departure.

**What stays true.** $\hat b = (X^\top X)^{-1}X^\top y$ has $E[\hat b] = b$, because unbiasedness uses only $E[\varepsilon] = 0$. Under mild conditions on $X$ and the $\sigma_i$ it is also consistent.

**What goes wrong: the variance formula.** The true covariance of $\hat b$ is the sandwich

$$\operatorname{Cov}(\hat b) = (X^\top X)^{-1}X^\top\Sigma X(X^\top X)^{-1},$$

which is not $\sigma^2(X^\top X)^{-1}$ for any $\sigma^2$ in general. The usual estimate $s^2(X^\top X)^{-1}$, with $s^2 = \mathrm{RSS}/(n - p)$, has expectation $\frac{\operatorname{tr}((I - H)\Sigma)}{n - p}(X^\top X)^{-1}$, where $H$ is the [hat matrix](/hat-matrix/). This can be too small or too large. It is too small for a slope when the variance is largest at the extreme values of the predictor, which is the common fan shape. The t statistics then do not have the t law, and the [F-test](/regression-f-test/) does not have the F law, even with normal errors.

**What goes wrong: efficiency.** The best linear unbiased estimator is now [generalized least squares](/generalized-least-squares/), which here is [weighted least squares](/weighted-least-squares/) with weights $1/\sigma_i^2$. OLS is BLUE under $\Sigma$ if and only if the column space of $X$ is invariant under $\Sigma$ (Kruskal's condition, proved on the [Gauss-Markov](/gauss-markov-theorem/) page). So heteroscedasticity makes OLS inefficient *in general*, not always. In a one-way layout with a different variance in each group, $X$ is the matrix of group indicators, $\Sigma X$ has the same column space, and the group means are BLUE whatever the group variances are; only their standard errors need care.

**Three remedies.**

1. *Model and weight.* If $\sigma_i^2 = \sigma^2 v_i$ with known $v_i$, weighted least squares with weights $1/v_i$ is BLUE and its usual standard errors are right. If $v_i$ depends on unknown parameters, estimate them from the OLS residuals and weight with the estimates (feasible GLS). The gain in efficiency depends on the variance model being right.
2. *Keep OLS and fix the standard errors.* White's (1980) estimator replaces $\Sigma$ in the sandwich by $\operatorname{diag}(e_i^2)$. It is consistent without any model for $\sigma_i^2$. The [heteroscedasticity-consistent standard errors](/heteroscedasticity-consistent-standard-errors/) page gives the algorithm and the finite sample corrections HC1 to HC3 of MacKinnon and White (1985); HC3, which divides $e_i^2$ by $(1 - h_{ii})^2$, behaves best in small samples.
3. *Transform.* If the standard deviation grows in proportion to the mean, $\log y$ has nearly constant variance; counts often stabilize under $\sqrt y$. The [Box-Cox transformation](/box-cox-transformation/) chooses a power from the data. A transformation changes the model for the mean as well, so it fits only when the new scale makes sense.

A [generalized linear model](/generalized-linear-model/) is a fourth route: it states the variance as a function of the mean (Poisson, gamma) and fits by iteratively reweighted least squares.

**Detection.** Plot the residuals, or better the [studentized residuals](/studentized-residual/), against the fitted values and against each predictor; a funnel is the typical sign. Raw residuals have variance $\sigma^2(1 - h_{ii})$ even under homoscedasticity, so they show a false pattern at high-leverage points. The [Breusch-Pagan test](/breusch-pagan-test/) regresses the squared residuals on chosen variables and refers $n R^2$ of that regression to a chi-squared law. White's test does the same with the predictors, their squares and their products. A test that does not reject does not prove constant variance; with small $n$ these tests have little power.

## Examples

**Exact variances, five points.** Take $x = (1, 2, 3, 4, 5)$, a straight line model and independent errors with $\sigma_i = x_i$. With $S_{xx} = 10$:

| quantity | value |
|---|---|
| true $\operatorname{Var}(\hat b_1)$ of OLS, $\sum(x_i - \bar x)^2\sigma_i^2/S_{xx}^2$ | $124/100 = 1.24$ |
| expected naive estimate, $E[s^2]/S_{xx} = \operatorname{tr}((I - H)\Sigma)/(3 \cdot 10)$ | $31.6/30 = 1.053$ |
| $\operatorname{Var}(\hat b_1)$ of weighted least squares with $w_i = 1/x_i^2$ | $5269/7576 = 0.6955$ |

The naive formula is 15% too small in variance on average, and OLS has 78% more variance than the weighted fit. The sandwich with the true $\Sigma$ gives 1.24 exactly, which is what White's estimator aims at.

**Simulated coverage.** With $n = 50$, $x$ evenly spaced from 0.2 to 10, slope 2, normal errors with standard deviation $x_i$, 4000 replications and seed 7, the nominal 95% t interval for the slope covered the true slope in 92.8% of runs with the usual standard error and in 94.5% with the HC3 standard error. This is a measured result for one design, not a proof; the gap grows when the variance changes more sharply or the leverage is uneven.

**Size of the F-test.** In the Monte Carlo table of the [regression F-test](/regression-f-test/) page, normal errors with standard deviation $0.1 + 3x_3^2$, where $x_3$ is a tested predictor, raised the size of a nominal 5% partial F-test to 12.4% at $n = 12$ and to 5.8% at $n = 60$. Wrong variance assumptions affect tests even when the coefficients are estimated without bias.

**No harm to the point estimate.** In every case above the OLS slope has mean exactly 2. Heteroscedasticity is a problem of uncertainty and efficiency, not of bias.

## Where it is used

- **Regression diagnostics.** Checking constant variance is one of the standard checks after a fit, together with the [Q-Q plot](/q-q-plot/) of studentized residuals for normality and [Cook's distance](/cooks-distance/) for influence.
- **Econometrics.** Cross-section data (firms, households, regions) are very often heteroscedastic, and HC standard errors are the default in much applied work.
- **Analysis of variance.** Unequal group variances affect the F-test of [one-way ANOVA](/one-way-anova/), most when the group sizes are unequal; Welch's test is the usual replacement.
- **Measurement and calibration.** Instruments with error proportional to the reading call for weighted fits or a log scale.
- **Time series.** Volatility that changes over time is heteroscedasticity in time; ARCH and GARCH models describe it.

## References
