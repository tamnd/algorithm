---
tag: A3C9X5
kind: definition
slug: explained-variance
name: Explained variance
aliases:
- explained variance ratio
area: machine-learning/dimensionality-reduction
level: intro
summary: "The fraction of the total variance that a principal component, or a subspace, captures: an eigenvalue of the covariance matrix divided by its trace."
prereqs: [principal-component-analysis, covariance-matrix]
see_also: [scree-plot, reconstruction-error, sparse-pca, probabilistic-pca, factor-analysis]
sources:
  - book: isbn:9780387954424
    title: I. T. Jolliffe, Principal Component Analysis, second edition, Springer, 2002
    locator: Section 6.1 (rules for choosing how many components, 6.1.1 the cumulative percentage of total variation, 6.1.2 the size of the variances of the components and Kaiser's rule)
  - paper: doi:10.1177/001316446002000116
    title: Henry F. Kaiser, The application of electronic computers to factor analysis, Educational and Psychological Measurement 20(1), 141-151, 1960
    locator: the rule to keep the components of the correlation matrix with eigenvalue greater than one
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 14.5.1 (principal components and the variance of each component)
  - paper: doi:10.1198/106186006X113430
    title: Hui Zou, Trevor Hastie and Robert Tibshirani, Sparse principal component analysis, Journal of Computational and Graphical Statistics 15(2), 265-286, 2006
    locator: the adjusted total variance of correlated sparse components, computed by a QR decomposition of the scores
---

The explained variance of a [principal component](/principal-component-analysis/) is the variance of the data along it, which is an eigenvalue $\lambda_j$ of the [covariance matrix](/covariance-matrix/). The explained variance ratio divides it by the total variance, the sum of all eigenvalues. The cumulative ratio of the first $k$ components tells how much of the spread a $k$-dimensional PCA keeps, and it is one minus the relative [reconstruction error](/reconstruction-error/). Rules that pick $k$ from these numbers, such as a cumulative threshold or Kaiser's rule, are heuristics.

## Definition

The data are $n$ points in $\mathbb{R}^d$ with covariance matrix $C$ (with the divisor $n$ or $n - 1$; the ratios do not depend on the choice). Let $\lambda_1 \ge \cdots \ge \lambda_d \ge 0$ be its eigenvalues, with orthonormal eigenvectors $v_1, \ldots, v_d$, and assume $\operatorname{tr} C > 0$.

- The **explained variance** of component $j$ is $\lambda_j = v_j^T C v_j$, the variance of the scores $v_j^T(x_i - \bar x)$.
- The **explained variance ratio** of component $j$ is
$$r_j = \frac{\lambda_j}{\sum_{i=1}^d \lambda_i} = \frac{\lambda_j}{\operatorname{tr} C}.$$
- The **cumulative explained variance ratio** of the first $k$ components is $R_k = r_1 + \cdots + r_k$, with $R_0 = 0$ and $R_d = 1$.
- For a general $k$-dimensional subspace with an orthonormal basis $W$ ($d \times k$, $W^T W = I$), the fraction of variance it explains is
$$\operatorname{EV}(W) = \frac{\operatorname{tr}(W^T C W)}{\operatorname{tr} C} = 1 - \frac{\operatorname{err}(W)}{\operatorname{tr} C},$$
where $\operatorname{err}(W) = \frac{1}{n}\sum_i \|(I - W W^T)(x_i - \bar x)\|^2$ with $C$ taken with the divisor $n$. The second form follows from Pythagoras: $\|y\|^2 = \|W^T y\|^2 + \|(I - WW^T)y\|^2$ for each $y$.

**Properties.** Each $r_j$ is in $[0, 1]$, the $r_j$ sum to 1, and they do not increase with $j$. So $R_k$ is non-decreasing and concave in $k$: its increments $r_k$ do not increase. By the Ky Fan inequality (proved on the [PCA](/principal-component-analysis/) page), $\operatorname{EV}(W) \le R_k$ for each $k$-dimensional subspace, with equality for the span of $v_1, \ldots, v_k$. The ratios do not change when all data are multiplied by one constant, but they do change when one feature is rescaled.

**Kaiser's rule.** On the correlation matrix (the covariance of standardized features), $\operatorname{tr} R = d$, so the mean eigenvalue is 1. Kaiser (1960) proposed to keep the components with eigenvalue greater than 1, that is, those that explain more than one original standardized feature does. Jolliffe (Section 6.1.2) argues for a lower cut-off of about 0.7. Neither rule has a statistical guarantee.

**Cumulative threshold.** Keep the smallest $k$ with $R_k \ge \tau$. Values of $\tau$ from 70% to 90% are common (Jolliffe, Section 6.1.1). The threshold is a choice, not a result.

## Examples and non-examples

**The PCA example.** The eight points of the [PCA](/principal-component-analysis/) page have covariance eigenvalues $81, 36, 9$ and total variance 126.

| component | $\lambda_j$ | $r_j$ | $R_j$ |
|---|---|---|---|
| 1 | 81 | 0.643 | 0.643 |
| 2 | 36 | 0.286 | 0.929 |
| 3 | 9 | 0.071 | 1.000 |

A threshold of 90% picks $k = 2$, and the reconstruction error is then $126 (1 - 0.929) = 9$.

**The same data, standardized.** The correlation matrix of these points has the off-diagonal entries $22/\sqrt{29 \cdot 44} \approx 0.616$, $4/\sqrt{29 \cdot 53} \approx 0.102$ and $26/\sqrt{44 \cdot 53} \approx 0.538$. Its eigenvalues are $1.870, 0.899, 0.231$, with ratios $62.3\%, 30.0\%, 7.7\%$. Kaiser's rule keeps one component; Jolliffe's cut-off 0.7 keeps two. The ratios differ from those of the covariance matrix, because standardizing changes the problem.

**Kaiser's rule on noise.** Draw $n = 100$ points with $d = 10$ independent standard normal features (`random.Random(1)`). The true correlation matrix is the identity, so no component carries structure. The sample correlation matrix has the eigenvalues $1.530, 1.437, 1.356, 1.173, 1.136, 0.926, \ldots, 0.444$, and Kaiser's rule keeps 5 components. With the seeds 2 and 3 it keeps 4 and 5. Sampling noise spreads the eigenvalues around 1, so the rule over-counts when $d / n$ is not small. [Parallel analysis](/scree-plot/) corrects for this.

**Non-examples.**

- The ratios of the eigenvalues of $\frac{1}{n}X^T X$ for uncentered data are not explained variances: the first eigenvalue then mostly measures $\|\bar x\|^2$.
- For loadings that are not orthogonal or scores that are correlated, as in [sparse PCA](/sparse-pca/), the sum of $w_j^T C w_j$ over the components can exceed $\operatorname{tr}(W^T C W)$ for the subspace, and can even exceed the total variance. Zou, Hastie and Tibshirani (2006) report an adjusted variance that removes the correlation by a QR decomposition of the scores.
- The "explained variance score" of a regression model, $1 - \operatorname{Var}(y - \hat y)/\operatorname{Var}(y)$, is a different quantity, close to the coefficient of determination of [linear regression](/linear-regression/).

## Related definitions

- [Reconstruction error](/reconstruction-error/): for PCA, $1 - R_k$ is the reconstruction error divided by the total variance.
- [Scree plot](/scree-plot/): the plot of $\lambda_j$ or $r_j$ against $j$, used to pick $k$ by eye, and parallel analysis.
- [Covariance matrix](/covariance-matrix/): the total variance is its trace.
- [Probabilistic PCA](/probabilistic-pca/) and [factor analysis](/factor-analysis/) split the variance into a shared part and a noise part; in PPCA the noise variance is the mean of the dropped eigenvalues.
- [Energy compaction](/energy-compaction/) is the same idea in transform coding: the fraction of signal energy in the first coefficients.

## References
