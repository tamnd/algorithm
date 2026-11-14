---
tag: TCKK8T
kind: model
slug: errors-in-variables-regression
name: Errors-in-variables model
aliases:
- measurement error model
- Deming regression
area: statistics-and-inference/regression-and-diagnostics
level: advanced
summary: A regression model in which the predictors are observed with noise. Least squares is then biased toward zero, and Deming or orthogonal regression corrects it.
history:
  year: 1943
  people: [W. Edwards Deming, Olav Reiersøl, Wayne A. Fuller]
  note: Deming (1943) fitted lines with errors in both coordinates when the ratio of the error variances is known. Reiersøl (1950) showed when the slope is identified without that ratio, and Fuller (1987) collected the theory.
prereqs: [ordinary-least-squares, estimator-bias, consistent-estimator, method-of-moments]
see_also: [instrumental-variables-estimation, singular-value-decomposition, principal-component-analysis, factor-analysis, maximum-likelihood-estimation, gauss-markov-theorem, weighted-least-squares, linear-regression]
sources:
  - book: isbn:9780471861874
    title: Wayne A. Fuller, Measurement Error Models, Wiley, 1987
    locator: Chapter 1 (one explanatory variable; the attenuation of least squares, identification, and estimation when the ratio of the error variances or the reliability ratio is known)
  - paper: doi:10.2307/1907835
    title: "Olav Reiersøl, Identifiability of a linear relation between variables which are subject to error, Econometrica 18(4), 1950, pp. 375 to 389"
    locator: The whole paper (the slope of a straight line with errors in both variables is identified unless the true predictor is normal)
  - book: isbn:9780486646855
    title: W. Edwards Deming, Statistical Adjustment of Data, Wiley, 1943; Dover reprint, 1964
    locator: Parts A and B (curve fitting and the general least squares adjustment when all observed coordinates have errors with known relative weights)
  - book: isbn:9781584886334
    title: Raymond J. Carroll, David Ruppert, Leonard A. Stefanski and Ciprian M. Crainiceanu, Measurement Error in Nonlinear Models, A Modern Perspective, second edition, Chapman and Hall/CRC, 2006
    locator: Chapter 3 (linear regression and attenuation), Chapter 4 (regression calibration), Chapter 5 (simulation extrapolation) and Chapter 6 (instrumental variables)
  - paper: doi:10.1137/0717073
    title: "Gene H. Golub and Charles F. Van Loan, An analysis of the total least squares problem, SIAM Journal on Numerical Analysis 17(6), 1980, pp. 883 to 893"
    locator: The whole paper (total least squares by the singular value decomposition)
---

The errors-in-variables model is a regression in which the predictor is not observed exactly: the data contain $x_i = \xi_i + u_i$, where $\xi_i$ is the true value and $u_i$ is measurement error. [Ordinary least squares](/ordinary-least-squares/) of $y$ on $x$ is then not consistent. Its slope converges to the true slope times the reliability ratio $\lambda = \sigma_\xi^2/(\sigma_\xi^2 + \sigma_u^2) < 1$, so the effect looks weaker than it is; this is called attenuation. Without extra information the slope is not identified when all variables are normal. With extra information it can be estimated consistently. If the ratio of the two error variances is known, the maximum likelihood fit has a closed form, which Deming (1943) used. If the ratio is 1, the fit is orthogonal regression, which minimizes perpendicular distances and is computed by the [singular value decomposition](/singular-value-decomposition/). A known reliability ratio, replicate measurements or an instrument are other ways to restore identification.

## The machine

**Data.** Pairs $(x_i, y_i)$, $i = 1, \dots, n$, generated as

$$x_i = \xi_i + u_i, \qquad y_i = \alpha + \beta\xi_i + \varepsilon_i,$$

where $\xi_i$ is the true predictor, $u_i$ the measurement error with mean 0 and variance $\sigma_u^2$, and $\varepsilon_i$ the equation error with mean 0 and variance $\sigma_\varepsilon^2$. The errors $u_i$ and $\varepsilon_i$ are independent of each other, of the $\xi_j$ and across $i$. This is the classical error model: the error is added to the true value and does not depend on it.

**Two versions.** In the structural model the $\xi_i$ are independent draws from a law with mean $\mu_\xi$ and variance $\sigma_\xi^2 > 0$. In the functional model the $\xi_i$ are fixed unknown numbers, one parameter for each observation.

**Parameter space.** $(\alpha, \beta, \mu_\xi, \sigma_\xi^2, \sigma_u^2, \sigma_\varepsilon^2)$ in the structural model, with $\sigma_\xi^2 > 0$ and nonnegative error variances. Extra information that restores identification is one of the following: the ratio $\delta = \sigma_\varepsilon^2/\sigma_u^2$ is known; $\sigma_u^2$ or the reliability ratio $\lambda$ is known, for example from replicate measurements; or an instrument $z_i$ is observed that is correlated with $\xi_i$ but not with $u_i$ or $\varepsilon_i$.

**Several predictors.** With $p$ predictors, $x_i = \xi_i + u_i$ in $\mathbb R^p$, $\Sigma_{\xi\xi}$ the covariance of $\xi_i$ and $\Sigma_{uu}$ that of $u_i$; some rows and columns of $\Sigma_{uu}$ are 0 for predictors measured without error.

## What it counts

- **The slope $\beta$ of the true predictor.** This is the target. The slope of $y$ on the observed $x$ is a different quantity, $\lambda\beta$, and it is the right target only for prediction of $y$ from future values of $x$ measured with the same error.
- **The reliability ratio** $\lambda = \sigma_\xi^2/(\sigma_\xi^2 + \sigma_u^2)$, the part of the variance of $x$ that is true signal.
- **The error variance ratio** $\delta = \sigma_\varepsilon^2/\sigma_u^2$, which fixes the direction in which the residuals are measured.
- **The true values** $\xi_i$ in the functional model; the fit gives estimates $\hat\xi_i$, the points on the fitted line that are nearest to the data in the metric that $\delta$ defines.

## Relation to other models

- **Ordinary regression** is the case $\sigma_u^2 = 0$, or $\delta = \infty$: then $x_i = \xi_i$, and least squares is unbiased and is BLUE by the [Gauss-Markov theorem](/gauss-markov-theorem/).
- **Reverse regression** is the case $\sigma_\varepsilon^2 = 0$, or $\delta = 0$: $y$ is exact, and the slope of $x$ on $y$, inverted, is consistent.
- **Orthogonal regression and total least squares.** The case $\delta = 1$ minimizes the sum of squared perpendicular distances to the line. In matrix form this is total least squares, solved by the [singular value decomposition](/singular-value-decomposition/) of the centred data matrix; the normal of the line is the right singular vector of the smallest singular value, and the line direction is the first [principal component](/principal-component-analysis/). There is no separate page for total least squares.
- **Factor analysis.** The structural model is a one-factor model: $x$ and $y$ are two noisy indicators of the factor $\xi$. With only two indicators the [factor analysis](/factor-analysis/) model is not identified, which is the same fact as Result 2 below.
- **Instrumental variables.** A variable correlated with $\xi$ and not with the errors identifies $\beta$ as a ratio of covariances; see [instrumental variables estimation](/instrumental-variables-estimation/).
- **Berkson error.** If instead $\xi_i = x_i + u_i$ with $u_i$ independent of $x_i$, as when a dose is set to $x_i$ and the true dose varies around it, least squares of $y$ on $x$ stays unbiased for $\beta$ in a linear model. The direction of the error decides which model applies.
- **Weighted least squares** fits a model where only $y$ has errors of unequal size; see [weighted least squares](/weighted-least-squares/).

## Known results in the model

**1. Attenuation (proved here).** In the structural model with $\sigma_\xi^2 > 0$, the least squares slope $\hat\beta_{\mathrm{OLS}} = s_{xy}/s_{xx}$ satisfies

$$\hat\beta_{\mathrm{OLS}} \to \lambda\beta = \frac{\sigma_\xi^2}{\sigma_\xi^2 + \sigma_u^2}\beta \quad \text{almost surely as } n \to \infty.$$

*Proof.* Here $s_{xx} = \frac1n\sum(x_i - \bar x)^2$ and $s_{xy} = \frac1n\sum(x_i - \bar x)(y_i - \bar y)$. By the strong [law of large numbers](/law-of-large-numbers/) applied to the independent rows, $s_{xx} \to \operatorname{Var}(x) = \sigma_\xi^2 + \sigma_u^2$ and $s_{xy} \to \operatorname{Cov}(x, y)$. By independence of $\xi$, $u$ and $\varepsilon$, $\operatorname{Cov}(\xi + u, \alpha + \beta\xi + \varepsilon) = \beta\sigma_\xi^2$. The ratio of the limits is $\lambda\beta$, since the limit of $s_{xx}$ is positive. $\square$

So the bias does not shrink with $n$. With $\beta = 2$, $\sigma_\xi^2 = 1$ and $\sigma_u^2 = 0.25$, $\lambda = 0.8$ and the slope converges to 1.6. If $\lambda$ is known, $\hat\beta_{\mathrm{OLS}}/\lambda$ is consistent; this is a [method of moments](/method-of-moments/) correction.

With $p$ predictors and an intercept, the same argument gives $\hat b \to (\Sigma_{\xi\xi} + \Sigma_{uu})^{-1}\Sigma_{\xi\xi}\beta$. Error in one predictor then biases the coefficients of the other predictors as well, when they are correlated with it; the direction of that bias depends on the correlations.

**2. Not identified for normal data, and the bounds (proved here).** Let $(\xi, u, \varepsilon)$ be jointly normal. Then $(x, y)$ is bivariate normal, and its law fixes only the means and $a = \operatorname{Var}(x)$, $b = \operatorname{Cov}(x, y)$, $c = \operatorname{Var}(y)$. Suppose $b > 0$. Every $\beta' \in [b/a, c/b]$ gives the same law with

$$\sigma_\xi'^2 = b/\beta', \qquad \sigma_u'^2 = a - b/\beta' \ge 0, \qquad \sigma_\varepsilon'^2 = c - \beta'b \ge 0,$$

and suitable means, and no $\beta'$ outside the interval does.

*Proof.* The model gives $\operatorname{Var}(x) = \sigma_\xi^2 + \sigma_u^2$, $\operatorname{Cov}(x, y) = \beta\sigma_\xi^2$ and $\operatorname{Var}(y) = \beta^2\sigma_\xi^2 + \sigma_\varepsilon^2$. The three choices above satisfy these equations with $(a, b, c)$, and they are valid variances exactly when $\beta' \ge b/a$ and $\beta' \le c/b$; the interval is not empty, since $b^2 \le ac$ by the Cauchy-Schwarz inequality. Conversely, any parameter set with $\operatorname{Cov} = b > 0$ has $\beta' > 0$ and $\sigma_\xi'^2 = b/\beta'$, and then $\sigma_u'^2 \ge 0$ and $\sigma_\varepsilon'^2 \ge 0$ force the interval. $\square$

So the data can bound the slope between the least squares slope of $y$ on $x$ and the inverse of the slope of $x$ on $y$, but no estimator can do better without extra information. Reiersøl (1950) proved the converse direction, which is cited and not proved here: if the errors are normal and $\xi$ is not normal, $\beta$ is identified, because higher moments of $(x, y)$ then carry information.

**3. The closed form for a known variance ratio (proved here).** Let $\delta = \sigma_\varepsilon^2/\sigma_u^2 > 0$ be known, and let $s_{xx}$, $s_{yy}$, $s_{xy} \ne 0$ be the sample moments. In the functional model with normal errors, the maximum likelihood estimate minimizes

$$\sum_i\big[\delta(x_i - \xi_i)^2 + (y_i - \alpha - \beta\xi_i)^2\big]$$

over $\alpha$, $\beta$ and $\xi_1, \dots, \xi_n$, and the minimizing slope is

$$\hat\beta_\delta = \frac{s_{yy} - \delta s_{xx} + \sqrt{(s_{yy} - \delta s_{xx})^2 + 4\delta s_{xy}^2}}{2s_{xy}}, \qquad \hat\alpha = \bar y - \hat\beta_\delta\bar x.$$

*Proof.* For fixed $\alpha$ and $\beta$, put $r_i = y_i - \alpha - \beta x_i$ and $s = \xi_i - x_i$. The term for $i$ is $\delta s^2 + (r_i - \beta s)^2$, a quadratic in $s$ with minimum at $s = \beta r_i/(\delta + \beta^2)$ and minimum value $\delta r_i^2/(\delta + \beta^2)$. So the problem is to minimize $\delta\sum_ir_i^2/(\delta + \beta^2)$. For fixed $\beta$ the best $\alpha$ is $\bar y - \beta\bar x$, and the objective becomes $n\delta f(\beta)$ with

$$f(\beta) = \frac{s_{yy} - 2\beta s_{xy} + \beta^2s_{xx}}{\delta + \beta^2}.$$

Setting $f'(\beta) = 0$ and simplifying gives $s_{xy}\beta^2 + (\delta s_{xx} - s_{yy})\beta - \delta s_{xy} = 0$. The product of its two roots is $-\delta < 0$, so one root is positive and one is negative. At a root, the equation gives $f(\beta) = s_{xx} - s_{xy}/\beta$, which is smaller at the root with the same sign as $s_{xy}$; that is the root with the plus sign. Since $f(\beta) \to s_{xx}$ as $\beta \to \pm\infty$ and $f$ at that root is below $s_{xx}$, the root is the global minimum. $\square$

As $\delta \to \infty$, $\hat\beta_\delta \to s_{xy}/s_{xx}$, the least squares slope; as $\delta \to 0$, $\hat\beta_\delta \to s_{yy}/s_{xy}$, the inverted reverse slope. In between, for $s_{xy} > 0$, $\hat\beta_\delta$ lies in the sample version of the interval of Result 2: the quadratic $g(\beta) = s_{xy}\beta^2 + (\delta s_{xx} - s_{yy})\beta - \delta s_{xy}$ equals $s_{xy}(s_{xy}^2 - s_{xx}s_{yy})/s_{xx}^2 \le 0$ at $s_{xy}/s_{xx}$ and $\delta(s_{xx}s_{yy} - s_{xy}^2)/s_{xy} \ge 0$ at $s_{yy}/s_{xy}$. Since $\partial g/\partial\delta = s_{xx}\beta - s_{xy} \ge 0$ there and $\partial g/\partial\beta > 0$ at the positive root, $\hat\beta_\delta$ decreases as $\delta$ grows. With $\delta = 1$, $f(\beta)$ is the mean squared perpendicular distance from the points to the line, and its minimum is the smallest eigenvalue of the $2 \times 2$ matrix of sample moments, which is the squared smallest singular value of the centred data divided by $n$. The estimator is consistent in the functional and in the structural model when $\delta$ is right (Fuller 1987, Chapter 1); this is cited. With a wrong $\delta$ it converges to a wrong slope inside the interval of Result 2.

**4. Unknown variance ratio in the functional model (shown here).** If $\delta$ is not known, the normal functional likelihood has no maximum: put every $\xi_i$ at $x_i$, fix $\sigma_\varepsilon > 0$ and let $\sigma_u \to 0$; the factor $\prod_i\sigma_u^{-1}\exp(-(x_i - \xi_i)^2/2\sigma_u^2) = \sigma_u^{-n}$ grows without bound. So the functional model needs extra information, such as a known $\delta$, before maximum likelihood makes sense.

**5. Other corrections (cited).** Carroll, Ruppert, Stefanski and Crainiceanu (2006) treat regression calibration, which replaces $x_i$ by an estimate of $E[\xi_i \mid x_i]$ and is exact for linear models with normal $\xi$; simulation extrapolation, which adds more error in steps, watches how the estimate changes and extrapolates back to zero error; and instrumental variables. These also apply to nonlinear models such as [logistic regression](/logistic-regression/), where no closed form exists.

**6. A worked example.** Take $x = (1, 2, 3, 4, 5)$ and $y = (2, 3, 5, 4, 6)$. The centred sums are $\sum(x - \bar x)^2 = 10$, $\sum(y - \bar y)^2 = 10$ and $\sum(x - \bar x)(y - \bar y) = 9$, with $\bar x = 3$ and $\bar y = 4$.

| method | $\delta$ | slope | intercept |
|---|---|---|---|
| least squares of $y$ on $x$ | $\infty$ | 0.9 | 1.3 |
| known ratio | 2 | 0.9639 | 1.1084 |
| orthogonal regression | 1 | 1 | 1 |
| known ratio | 0.5 | 1.0375 | 0.8875 |
| inverted reverse regression | 0 | 1.1111 | 0.6667 |

For $\delta = 1$ the formula gives $(10 - 10 + \sqrt{0 + 4 \cdot 81})/18 = 1$ exactly. The residuals from the line $y = 1 + x$ are $(0, 0, 1, -1, 0)$, so the sum of squared perpendicular distances is $2/(1 + 1^2) = 1$. This equals the smallest eigenvalue of $\begin{pmatrix}10 & 9\\ 9 & 10\end{pmatrix}$, whose eigenvalues are 1 and 19; the eigenvector $(1, -1)/\sqrt2$ is the normal of the line. The fitted true values are $\hat\xi = x + r/2 = (1, 2, 3.5, 3.5, 5)$. A grid search over the slope with step $10^{-5}$ gives the same minimizers for each $\delta$ in the table.

## References
