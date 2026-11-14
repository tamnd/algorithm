---
tag: QRYGD4
kind: technique
slug: quasi-likelihood
name: Quasi-likelihood
aliases:
- Wedderburn quasi-likelihood
- quasi-Poisson model
area: statistics-and-inference/regression-and-diagnostics
level: advanced
summary: Wedderburn's estimation that specifies only the mean and the variance function of the response. It gives GLM-like estimates and standard errors with overdispersion.
prereqs: [generalized-linear-model, iteratively-reweighted-least-squares, score-function, fisher-scoring]
see_also: [generalized-estimating-equations, heteroscedasticity-consistent-standard-errors, deviance-statistic, m-estimator, generalized-method-of-moments, logistic-regression, exponential-family-distribution, weighted-least-squares]
sources:
  - paper: doi:10.1093/biomet/61.3.439
    title: "R. W. M. Wedderburn, Quasi-likelihood functions, generalized linear models, and the Gauss-Newton method, Biometrika 61(3), 1974, pp. 439 to 447"
    locator: The whole paper (the quasi-likelihood defined from the mean and the variance function, its fit by the generalized linear model algorithm, and the leaf blotch example)
  - paper: doi:10.1214/aos/1176346056
    title: "Peter McCullagh, Quasi-likelihood functions, The Annals of Statistics 11(1), 1983, pp. 59 to 67"
    locator: The whole paper (asymptotic normality of quasi-likelihood estimates, the dispersion estimate, dependent observations and the optimality of the quasi-score among linear estimating functions)
  - book: isbn:9780412317606
    title: P. McCullagh and J. A. Nelder, Generalized Linear Models, second edition, Chapman and Hall, 1989
    locator: Chapter 9 (quasi-likelihood functions; Section 9.2 for independent observations, 9.2.4 for the leaf blotch example, 9.4 and 9.5 for optimal estimating functions, 9.6 for extended quasi-likelihood)
---

Quasi-likelihood fits a regression model when only the mean and the variance of the response are specified, not its whole distribution. The model says that $E y_i = \mu_i = g^{-1}(x_i^\top\beta)$ for a link $g$, and that $\operatorname{Var}y_i = \phi V(\mu_i)$ for a known variance function $V$ and an unknown dispersion $\phi$. Wedderburn (1974) observed that the score equations of a [generalized linear model](/generalized-linear-model/) use only these two moments. So the same equations, solved by the same [iteratively reweighted least squares](/iteratively-reweighted-least-squares/) loop, give estimates with likelihood-like properties for any $V$. The most common case is the quasi-Poisson model for overdispersed counts: the coefficients are the Poisson ones, and the standard errors are multiplied by $\sqrt{\hat\phi}$, where $\hat\phi$ is the Pearson statistic divided by $n - p$.

## In plain words

Count data often vary more than the Poisson law allows. If you fit a Poisson model anyway, the fitted line is fine, but the model claims more precision than it has, and the intervals are too narrow. Quasi-likelihood says: do not pretend to know the whole law. State only how the average depends on the predictors and how the spread grows with the average. The fitting steps are the same as for a standard model, so the fitted line does not change. What changes is the uncertainty: an extra spread factor is estimated from the data, and every standard error is widened by its square root. The same idea works for proportions and for other kinds of data where only the average and the spread can be trusted.

## When it applies

- **Independent responses** $y_1, \dots, y_n$ with a correct mean model $\mu_i = g^{-1}(x_i^\top\beta)$, $X$ of rank $p$, and a variance proportional to a known function of the mean, $\operatorname{Var}y_i = \phi V(\mu_i)$.
- **No distribution needed.** The responses need not be counts, integers or members of an exponential family; for example $y_i$ can be a proportion of leaf area.
- **The quasi-score.** With $D_i = \partial\mu_i/\partial\beta$, a row vector of length $p$,

$$U(\beta) = \sum_{i=1}^n\frac{D_i^\top(y_i - \mu_i)}{\phi V(\mu_i)}.$$

If the mean model is right, $E\,U = 0$, since each term has the factor $E(y_i - \mu_i) = 0$. If the variance model is also right,

$$\operatorname{Var}U = \sum_i\frac{D_i^\top D_i\operatorname{Var}y_i}{\phi^2V(\mu_i)^2} = \sum_i\frac{D_i^\top D_i}{\phi V(\mu_i)} = -E\frac{\partial U}{\partial\beta},$$

because the derivative of $D_i^\top/V(\mu_i)$ multiplies $y_i - \mu_i$ and has expectation 0. These are exact, and they are the two properties of a likelihood score that the asymptotic theory uses. So $U$ behaves like a score, and $i(\beta) = \sum_iD_i^\top D_i/(\phi V(\mu_i))$ plays the part of the Fisher information.
- **The quasi-likelihood.** $Q(\mu; y) = \int_y^\mu\frac{y - t}{\phi V(t)}\,dt$ has $\partial Q/\partial\mu = (y - \mu)/(\phi V(\mu))$, so $U$ is the gradient of $\sum_iQ(\mu_i; y_i)$. For $V(\mu) = \mu$, $\phi Q = y\log\mu - \mu$ up to a term without $\mu$, the Poisson log-likelihood; for $V(\mu) = \mu(1 - \mu)$ it is the Bernoulli log-likelihood, and for $V = 1$ it is $-\frac12(y - \mu)^2$.

## The template

```pseudo id=main
QUASI-LIKELIHOOD(X[1..n, 1..p], y[1..n])
L1  choose LINK g and VARIANCE-FUNCTION V                  ▷ holes: the mean and variance model
L2  b ← START(y)                                            ▷ hole: e.g. least squares of g(y + c) on X
L3  repeat
L4      η ← Xb;  μᵢ ← g⁻¹(ηᵢ);  wᵢ ← 1 / (V(μᵢ) g′(μᵢ)²);  zᵢ ← ηᵢ + (yᵢ - μᵢ) g′(μᵢ)
L5      b ← weighted least squares of z on X with weights w
L6  until b stops changing
L7  φ̂ ← Σᵢ (yᵢ - μᵢ)² / V(μᵢ) / (n - p)                     ▷ Pearson X² over n - p
L8  return b, φ̂, φ̂ (Xᵀ W X)⁻¹                             ▷ W = diag(w) at the solution
```

The holes are the link and the variance function (line L1) and the start (line L2). Lines L4 and L5 are one [Fisher scoring](/fisher-scoring/) step for $U$: with $D_i = x_i^\top/g'(\mu_i)$, the step $b + i(b)^{-1}U(b)$ is exactly the weighted least squares fit of line L5, as for a generalized linear model. The dispersion $\phi$ cancels from $U = 0$, so the estimate $\hat\beta$ does not depend on it, and $\phi$ enters only the covariance in line L8.

**What is proved and what is cited.** The identities $E\,U = 0$ and $\operatorname{Var}U = -E\,\partial U/\partial\beta$ above are exact, and the step in lines L4 and L5 is exactly Fisher scoring. The following are cited: under regularity conditions $\hat\beta$ is consistent and $\sqrt n(\hat\beta - \beta)$ is asymptotically normal with covariance estimated by line L8 (McCullagh 1983); $\hat\phi$ is consistent; and among estimating equations $\sum_iA_i(y_i - \mu_i) = 0$ with weights $A_i$ that depend on $\beta$ but not on $y$, the quasi-score gives the smallest asymptotic covariance, a Gauss-Markov property for estimating functions (McCullagh 1983; McCullagh and Nelder 1989, Sections 9.4 and 9.5). If $V$ is wrong but the mean model is right, $\hat\beta$ is still consistent, and the covariance $i^{-1}\big(\sum_iD_i^\top D_i(y_i - \hat\mu_i)^2/V_i^2\big)i^{-1}$, with $i$ computed at $\phi = 1$ and $V_i = V(\hat\mu_i)$, the same form as [heteroscedasticity-consistent standard errors](/heteroscedasticity-consistent-standard-errors/), stays valid; line L8 does not.

## Classic examples

**Quasi-Poisson for overdispersed counts.** Log link and $V(\mu) = \mu$, so $\operatorname{Var}y_i = \phi\mu_i$. The quasi-score equations are the Poisson ones, $\sum_ix_i(y_i - \mu_i) = 0$. Take $x_i = i$ for $i = 0, \dots, 9$ and

$$y = (2, 5, 1, 8, 3, 12, 6, 18, 9, 25).$$

The fit converges in 5 steps to $\hat\beta = (0.8754, 0.2406)$. One can check the equations by hand: $\sum y_i = 89 = \sum\hat\mu_i$ and $\sum x_iy_i = 562 = \sum x_i\hat\mu_i$. The Pearson statistic is $X^2 = 16.94$ on $8$ degrees of freedom, so $\hat\phi = 2.117$.

| standard errors | intercept | slope |
|---|---|---|
| Poisson, $\phi = 1$ | 0.2870 | 0.0422 |
| quasi-Poisson, $\hat\phi = 2.117$ | 0.4176 | 0.0615 |
| robust form, $V$ not trusted | 0.3339 | 0.0488 |

The quasi-Poisson errors are the Poisson ones times $\sqrt{2.117} = 1.455$. The deviance is $18.19$, and $18.19/8 = 2.27$ is a second, less stable estimate of $\phi$.

**Measured coverage.** With $n = 40$ equally spaced $x$ in $[0, 2]$, $\mu = \exp(1 + 0.7x)$ and counts with $\operatorname{Var}y = 3\mu$ (Poisson counts whose mean is drawn from a gamma law), the coverage of the nominal 95% Wald interval for the slope over 2000 data sets was 0.747 with Poisson errors, 0.942 with quasi-Poisson errors and 0.932 with the robust form; the mean of $\hat\phi$ was 2.97. With true Poisson counts ($\phi = 1$) the three were 0.959, 0.952 and 0.937. The Monte Carlo standard error of each coverage is about 0.005. These values are measured with a script, not proved.

**Quasi-binomial for overdispersed proportions.** For $y_i$ the proportion of successes out of $m_i$, take the logit link and $V(\mu) = \mu(1 - \mu)/m_i$. The estimates are those of [logistic regression](/logistic-regression/) for grouped data, and $\hat\phi > 1$ shows extra-binomial variation, for example from litter or cluster effects.

**Leaf blotch.** Wedderburn (1974) analysed the percentage of leaf area of barley affected by leaf blotch, for ten varieties at nine sites, with a logit link and $V(\mu) = \mu^2(1 - \mu)^2$. A binomial variance does not fit such continuous proportions, and no standard distribution has this variance function, but the quasi-likelihood fit needs none; McCullagh and Nelder (1989, Section 9.2.4) repeat the analysis.

**Constant coefficient of variation.** $V(\mu) = \mu^2$ with a log link gives the same equations as gamma regression, $\sum_ix_i(y_i - \mu_i)/\mu_i = 0$. With only an intercept the solution is $\hat\mu = \bar y$.

**Nonlinear least squares.** $V = 1$ and any mean function give $U = \sum_iD_i^\top(y_i - \mu_i)/\phi$, the normal equations of least squares, and line L5 becomes a Gauss-Newton step; this is the link to the Gauss-Newton method in the title of Wedderburn's paper.

## Variations

- **Correlated responses.** Replace $1/V(\mu_i)$ by the inverse of a working covariance matrix for a group of responses: this is [generalized estimating equations](/generalized-estimating-equations/), which pairs the multivariate quasi-score with the robust covariance.
- **The robust covariance in place of $\phi$.** When the form of $V$ is in doubt, keep the point estimate and use the robust covariance above; the example table shows both.
- **Extended quasi-likelihood.** To compare variance functions or to model $\phi$ as a function of covariates, one needs a function that also depends on $V$ and $\phi$; McCullagh and Nelder (1989, Section 9.6) describe the extended quasi-likelihood of Nelder and Pregibon.
- **Quasi-deviance.** $D = -2\phi\sum_iQ(\hat\mu_i; y_i)$ with $Q$ measured from $Q(y; y) = 0$ plays the role of the [deviance](/deviance-statistic/). Differences of quasi-deviances divided by $\hat\phi$ and by the difference in degrees of freedom give approximate F tests between nested mean models.
- **Other estimating equations.** Quasi-likelihood is a special case of [M-estimation](/m-estimator/) and of exactly identified [generalized method of moments](/generalized-method-of-moments/), with the estimating function chosen from the variance model.

## Pitfalls

- **No likelihood, so no AIC and no likelihood ratio test.** $\sum Q$ is not a log-likelihood of any distribution in general. Use F tests based on the quasi-deviance and $\hat\phi$, or Wald tests with the scaled covariance.
- **Overdispersion that grows with the mean.** Quasi-Poisson assumes $\operatorname{Var}y = \phi\mu$. If the variance grows like $\mu + \mu^2/k$, as in a negative binomial law, the weights are wrong for large counts. The estimates stay consistent, but they lose efficiency, and line L8 is off; check plots of squared Pearson residuals against $\hat\mu$.
- **Estimating $\phi$ from a wrong mean model.** A missing predictor or a wrong link inflates $X^2$, and $\hat\phi > 1$ is then a sign of a bad mean, not of overdispersion. Larger standard errors do not repair a biased mean.
- **Small expected counts.** With many $\hat\mu_i$ below about 1, $X^2/(n - p)$ is a poor estimate of $\phi$; the deviance-based estimate is worse.
- **Underdispersion.** $\hat\phi < 1$ is allowed and shrinks the errors. Be careful: it is often a sign of a design feature, such as counts with a fixed total, that should be modelled.

## Exercises

1. Find the quasi-likelihood $Q(\mu; y)$ for $V(\mu) = \mu$ and for $V(\mu) = \mu^2$, with $\phi = 1$.
   *Answer.* For $V = \mu$, $\int_y^\mu(y - t)/t\,dt = y\log(\mu/y) - (\mu - y)$, which is $y\log\mu - \mu$ plus a term without $\mu$. For $V = \mu^2$, $\int_y^\mu(y - t)/t^2\,dt = -y/\mu - \log\mu + 1 + \log y$, which is $-y/\mu - \log\mu$ plus a term without $\mu$, the gamma log-likelihood with shape 1.
2. Show that the quasi-Poisson estimate $\hat\beta$ equals the Poisson maximum likelihood estimate, and that its standard errors are the Poisson ones times $\sqrt{\hat\phi}$.
   *Answer.* $U = 0$ is $\sum_iD_i^\top(y_i - \mu_i)/\mu_i = 0$ after $\phi$ cancels, which is the Poisson score equation. The covariance is $\hat\phi\,i_1(\hat\beta)^{-1}$, where $i_1$ is the Poisson information.
3. With $V(\mu) = \mu^2$, a log link and only an intercept, show that $\hat\mu = \bar y$ and that $\hat\phi = \frac{1}{n - 1}\sum_i(y_i/\bar y - 1)^2$.
   *Answer.* $D_i = \mu$, so $U \propto \sum_i(y_i - \mu)/\mu = 0$ gives $\mu = \bar y$. Then $X^2 = \sum_i(y_i - \bar y)^2/\bar y^2$, and $p = 1$.
4. Prove $\operatorname{Var}U = -E\,\partial U/\partial\beta$ when the mean and variance models are right and the responses are independent.
   *Answer.* $\partial U/\partial\beta = \sum_i\partial_\beta(D_i^\top/(\phi V_i))(y_i - \mu_i) - \sum_iD_i^\top D_i/(\phi V_i)$. The first sum has expectation 0. The variance of $U$ is the sum of the variances of independent terms, $\sum_iD_i^\top D_i\,\phi V_i/(\phi V_i)^2$, which is the same matrix.
5. In the quasi-Poisson example, the slope estimate is $0.2406$ with quasi-Poisson standard error $0.0615$. Give an approximate 95% interval for the factor by which the mean count grows per unit of $x$.
   *Answer.* $0.2406 \pm 1.96 \cdot 0.0615 = (0.120, 0.361)$, so the factor $e^\beta$ lies in about $(1.13, 1.43)$. With $n = 10$, a $t_8$ quantile 2.306 in place of 1.96 is a common, more cautious choice and gives $(1.10, 1.47)$.

## References
