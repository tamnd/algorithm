---
tag: K2W5YS
kind: definition
slug: leverage-statistics
name: Leverage
aliases:
- hat value
- leverage score
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: The i-th diagonal entry of the hat matrix, which measures how far x_i lies from the other predictors and how much y_i pulls its own fitted value.
prereqs: [hat-matrix]
see_also: [studentized-residual, cooks-distance, influence-function, covariance-matrix, qr-decomposition, least-trimmed-squares, cross-validation, generalized-linear-model]
sources:
  - paper: doi:10.1080/00031305.1978.10479237
    title: "David C. Hoaglin and Roy E. Welsch, The hat matrix in regression and ANOVA, The American Statistician 32(1), 1978, pp. 17 to 22"
    locator: The whole paper (the bounds 0 <= h_ii <= 1, the average p/n and the rule of thumb 2p/n for high leverage)
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: Section 10.2 (hat matrix diagonals) and Section 10.6.2 (high-leverage points)
  - book: isbn:9780471058564
    title: David A. Belsley, Edwin Kuh and Roy E. Welsch, Regression Diagnostics, Wiley, 1980
    locator: Chapter 2 (the diagonal of the hat matrix as a measure of leverage, and its cutoff 2p/n)
  - url: https://jmlr.org/papers/v13/drineas12a.html
    title: "Petros Drineas, Malik Magdon-Ismail, Michael W. Mahoney and David P. Woodruff, Fast approximation of matrix coherence and statistical leverage, Journal of Machine Learning Research 13, 2012, pp. 3475 to 3506"
    locator: Section 1 (statistical leverage scores as the squared row norms of an orthonormal basis of the column space, and coherence as their maximum)
---

The leverage of observation $i$ in a linear regression is the $i$-th diagonal entry $h_{ii}$ of the [hat matrix](/hat-matrix/). It depends only on the predictors, not on the response. It measures two things at once: how far the predictor row $x_i$ lies from the bulk of the rows, and how strongly $y_i$ pulls its own fitted value, since $h_{ii} = \partial\hat y_i/\partial y_i$. A point with high leverage can move the fitted line a lot, but whether it does depends on its response; that combined effect is influence, measured by [Cook's distance](/cooks-distance/). In numerical linear algebra the same numbers are called leverage scores.

## Definition

Let $X$ be an $n \times p$ design matrix of rank $p$, with rows $x_1^\top, \dots, x_n^\top$ (the intercept, if any, is one of the $p$ columns). The **leverage** (or **hat value**) of observation $i$ is

$$h_{ii} = x_i^\top(X^\top X)^{-1}x_i = \lVert q_i\rVert^2,$$

where $q_i^\top$ is row $i$ of $Q_1$ in a thin QR factorization $X = Q_1R$. The second form is how it is computed: $O(np^2)$ for the factorization and $O(np)$ for all $n$ leverages.

**Basic facts.** From $H = H^\top = H^2$ and $\operatorname{tr} H = p$:

1. $0 \le h_{ii} \le 1$, because $h_{ii} = \sum_j h_{ij}^2 \ge h_{ii}^2$.
2. $\sum_i h_{ii} = p$, so the average leverage is $p/n$.
3. With an intercept, $h_{ii} \ge 1/n$.
4. $h_{ii} = 1$ if and only if $h_{ij} = 0$ for every $j \ne i$, which happens if and only if $\hat y_i = y_i$ for every response vector. Then $e_i = 0$ always and $\operatorname{Var}(e_i) = \sigma^2(1 - h_{ii}) = 0$; the model spends one parameter on fitting that point exactly. An indicator column for one observation does this, and so does a group of size 1 in a one-way layout.
5. $\operatorname{Var}(\hat y_i) = \sigma^2 h_{ii}$ and $\operatorname{Var}(e_i) = \sigma^2(1 - h_{ii})$ when the errors are uncorrelated with variance $\sigma^2$.

**Distance form.** With an intercept, write $\tilde x_i$ for row $i$ without its leading 1, $\bar x$ for the mean of these rows, and $S$ for their sample [covariance matrix](/covariance-matrix/) (divisor $n - 1$). Then

$$h_{ii} = \frac1n + \frac{(\tilde x_i - \bar x)^\top S^{-1}(\tilde x_i - \bar x)}{n - 1} = \frac1n + \frac{\mathrm{MD}_i^2}{n - 1},$$

with $\mathrm{MD}_i$ the Mahalanobis distance of $\tilde x_i$ from $\bar x$. So leverage is a distance from the center of the predictor cloud, measured in the units of its own spread. The proof: centering the predictors does not change $H$, and the centered design $(\mathbf 1, \tilde X_c)$ has orthogonal blocks, so $H = \frac1n\mathbf 1\mathbf 1^\top + \tilde X_c(\tilde X_c^\top\tilde X_c)^{-1}\tilde X_c^\top$ with $\tilde X_c^\top\tilde X_c = (n - 1)S$.

**High leverage.** A common rule flags $h_{ii} > 2p/n$, twice the average (Hoaglin and Welsch 1978; Belsley, Kuh and Welsch use the same cutoff). Some authors use $3p/n$ for small $n$. These are conventions, not tests. For a design whose rows (without the intercept) are iid multivariate normal, $\frac{n}{n-1}\big(h_{ii} - \frac1n\big)$ has the Beta$\big(\frac{p-1}{2}, \frac{n-p}{2}\big)$ law, which shows how often the rule fires by chance, but designs are rarely random normal.

## Examples and non-examples

**Simple regression.** For $X = (\mathbf 1, x)$, $h_{ii} = \frac1n + \frac{(x_i - \bar x)^2}{S_{xx}}$ with $S_{xx} = \sum_k (x_k - \bar x)^2$. Leverage grows with the squared distance of $x_i$ from $\bar x$ and is smallest, $1/n$, at $x_i = \bar x$.

**A far point.** For $x = (1, 2, 3, 4, 5, 10)$, $n = 6$ and $p = 2$, the leverages are $0.364, 0.259, 0.193, 0.167, 0.180, 0.836$, with sum 2. Only the last exceeds $2p/n = 0.667$. Check by the distance form: $\bar x = 25/6$, the sample variance is $305/30$, so $\mathrm{MD}_6^2 = (35/6)^2/(305/30) = 3.347$ and $h_{66} = 1/6 + 3.347/5 = 0.836$.

**High leverage without influence.** Fit the first five points of that example with $y = (2, 3, 5, 4, 6)$: the line is $\hat y = 1.3 + 0.9x$, which predicts 10.3 at $x = 10$. If the sixth response is $y_6 = 10.3$, the six-point fit is the same line, $e_6 = 0$ and Cook's distance of the point is 0. Its leverage is still 0.836. If instead $y_6 = 4$, the line tilts to slope 0.177 and Cook's distance is 7.89. Leverage is potential; the response decides whether it is used.

**A balanced design.** In a one-way layout with $n_g$ observations per group, every point in group $g$ has leverage $1/n_g$. In a $2^k$ factorial design with all $p = 2^k$ effects and $r$ replicates, every point has leverage $1/r$. Balanced designs have equal leverages, which is one reason they are robust.

**Non-example: a large residual.** A point with a large residual and leverage near $1/n$ is an outlier in $y$ but has low leverage. It changes the intercept a little and the slope hardly at all.

**Non-example: leverage in generalized linear models.** For a [generalized linear model](/generalized-linear-model/) fitted by iteratively reweighted least squares, the hat matrix is $W^{1/2}X(X^\top WX)^{-1}X^\top W^{1/2}$ at the fitted weights. Its diagonal depends on the fitted means, so it depends on $y$, and a point far out in $x$ can have small leverage when its weight is small (a fitted probability near 0 or 1 in logistic regression).

## Related definitions

- **[Hat matrix](/hat-matrix/).** $H$ itself; leverage is its diagonal.
- **[Studentized residual](/studentized-residual/).** Divides $e_i$ by an estimate of $\sigma\sqrt{1 - h_{ii}}$, so residuals of high-leverage points, which are small by construction, are scaled up.
- **[Cook's distance](/cooks-distance/) and DFFITS.** Combine leverage with the residual: $D_i = \frac{r_i^2}{p}\frac{h_{ii}}{1 - h_{ii}}$.
- **Leave-one-out residual.** $e_i/(1 - h_{ii})$; the closed form of leave-one-out [cross-validation](/cross-validation/) for least squares uses it.
- **Leverage scores and coherence.** In randomized numerical linear algebra, $h_{ii}$ is the leverage score of row $i$, and $\max_i h_{ii}$ is the coherence of the column space. Sampling rows with probability proportional to $h_{ii}$ gives a small subproblem whose least squares solution approximates the full one; Drineas and coauthors show how to approximate all scores faster than a QR factorization.
- **Robust alternatives.** Leverage uses the mean and covariance of the predictors, which are themselves pulled by a cluster of far points (masking). Robust distances from a minimum covariance determinant fit, or [least trimmed squares](/least-trimmed-squares/), avoid this.

## References
