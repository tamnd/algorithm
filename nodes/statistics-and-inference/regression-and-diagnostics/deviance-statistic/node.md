---
tag: 0H7XKM
kind: definition
slug: deviance-statistic
name: Deviance
aliases:
- residual deviance
- scaled deviance
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: "Twice the log-likelihood gap between the saturated model and a fitted model. It plays the part of the residual sum of squares for a generalized linear model."
prereqs: [generalized-linear-model, likelihood-function, likelihood-ratio-test]
see_also: [akaike-information-criterion, wilks-theorem, kullback-leibler-divergence, exponential-family-distribution, iteratively-reweighted-least-squares, quasi-likelihood, logistic-regression, chi-squared-goodness-of-fit-test]
sources:
  - paper: doi:10.2307/2344614
    title: "J. A. Nelder and R. W. M. Wedderburn, Generalized linear models, Journal of the Royal Statistical Society, Series A 135(3), 1972, pp. 370 to 384"
    locator: The whole paper (the exponential family model with a link, the fit by iterative weighted least squares, and the deviance as the measure of goodness of fit that extends the residual sum of squares)
  - paper: doi:10.1080/01621459.1986.10478361
    title: "Donald A. Pierce and Daniel W. Schafer, Residuals in generalized linear models, Journal of the American Statistical Association 81(396), 1986, pp. 977 to 986"
    locator: The whole paper (deviance residuals and their near-normal distribution)
  - book: isbn:9780412317606
    title: P. McCullagh and J. A. Nelder, Generalized Linear Models, second edition, Chapman and Hall, 1989
    locator: Chapter 2 (the deviance and the generalized Pearson statistic as measures of discrepancy, and the unit deviances of the common families) and Chapter 4 (binary data, where the deviance does not measure fit)
---

The deviance of a fitted [generalized linear model](/generalized-linear-model/) is twice the difference between the log-likelihood of the saturated model, which fits every observation exactly, and the log-likelihood of the fitted model, multiplied by the dispersion. For a normal model with the identity link it is the residual sum of squares. The scaled deviance is the same quantity divided by the dispersion. The residual deviance is the deviance of the fitted model, and the null deviance is the deviance of the model with only an intercept. The difference of the scaled deviances of two nested models fitted to the same data is the [likelihood ratio](/likelihood-ratio-test/) statistic of the smaller model against the larger one. The deviance of one model alone is a test of fit only in special cases.

## Definition

Let $y_1, \dots, y_n$ be independent, and let $y_i$ have a density or mass function from an exponential dispersion family,

$$f(y; \theta_i, \phi) = \exp\Bigl\{\frac{w_i\bigl(y\theta_i - b(\theta_i)\bigr)}{\phi} + c(y, \phi/w_i)\Bigr\},$$

with known prior weights $w_i > 0$, dispersion $\phi > 0$, mean $\mu_i = b'(\theta_i)$ and variance $\phi V(\mu_i)/w_i$ (see [exponential family distribution](/exponential-family-distribution/)). Write $l(\mu; y)$ for the log-likelihood as a function of the vector of means. A model with $p$ coefficients (the coefficient vector is $b$, and $\hat b$ is its maximum likelihood estimate) gives the fitted means $\hat\mu$. The **saturated model** has one free mean per observation, so its fit is $\tilde\mu = y$. The **unit deviance** is

$$d(y, \mu) = 2\int_\mu^y \frac{y - t}{V(t)}\,dt = 2\bigl[y(\tilde\theta - \theta) - b(\tilde\theta) + b(\theta)\bigr],$$

where $\theta$ and $\tilde\theta$ are the natural parameters with means $\mu$ and $y$. The **scaled deviance** and the **deviance** are

$$D^* = 2\bigl[l(y; y) - l(\hat\mu; y)\bigr] = \frac{1}{\phi}\sum_{i=1}^n w_i\,d(y_i, \hat\mu_i), \qquad D = \phi D^* = \sum_{i=1}^n w_i\,d(y_i, \hat\mu_i).$$

The deviance $D$ does not depend on $\phi$. For the Poisson and binomial families $\phi = 1$, so $D = D^*$. The unit deviances of the common families are as follows, with $0\log 0 = 0$:

| family | $V(\mu)$ | $d(y, \mu)$ |
|---|---|---|
| normal | $1$ | $(y - \mu)^2$ |
| Poisson | $\mu$ | $2\bigl[y\log(y/\mu) - (y - \mu)\bigr]$ |
| binomial, $y$ a proportion of $m$ trials, $w = m$ | $\mu(1 - \mu)$ | $2\bigl[y\log(y/\mu) + (1 - y)\log\frac{1 - y}{1 - \mu}\bigr]$ |
| gamma | $\mu^2$ | $2\bigl[-\log(y/\mu) + (y - \mu)/\mu\bigr]$ |
| inverse Gaussian | $\mu^3$ | $(y - \mu)^2/(\mu^2y)$ |

**Facts.**

1. $d(y, \mu) \ge 0$, with equality only at $y = \mu$. More exactly, $w\,d(y, \mu)/\phi = 2\,\mathrm{KL}(f_{\tilde\theta} \,\|\, f_\theta)$, twice the [Kullback-Leibler divergence](/kullback-leibler-divergence/) from the member with mean $\mu$ to the member with mean $y$. Proof: $\log f_{\tilde\theta}(Y) - \log f_\theta(Y) = w[Y(\tilde\theta - \theta) - b(\tilde\theta) + b(\theta)]/\phi$, and the expectation of $Y$ under $f_{\tilde\theta}$ is $y$. So the scaled deviance is twice a sum of divergences, and the maximum likelihood fit minimizes it.
2. For the normal family with the identity link, $D = \sum(y_i - \hat\mu_i)^2$ is the residual sum of squares and $\phi = \sigma^2$.
3. **A difference of deviances is a likelihood ratio statistic.** Let $M_0 \subset M_1$ be nested models with $p_0 < p_1$ coefficients, fitted by maximum likelihood to the same data with the same $\phi$. Then $D_0^* - D_1^* = 2[l(\hat\mu_1; y) - l(\hat\mu_0; y)]$. Proof: in $D_0^* - D_1^* = 2[l(y; y) - l(\hat\mu_0; y)] - 2[l(y; y) - l(\hat\mu_1; y)]$ the saturated term is the same number and cancels. So under the conditions of [Wilks' theorem](/wilks-theorem/), with $p_1$ fixed and $n \to \infty$, $D_0^* - D_1^*$ under $M_0$ tends in law to $\chi^2_{p_1 - p_0}$. In the normal case with known $\sigma^2$ the $\chi^2$ law is exact.
4. **Unknown dispersion.** With $\phi$ unknown, the usual test uses $F = \frac{(D_0 - D_1)/(p_1 - p_0)}{\hat\phi}$ with $\hat\phi = D_1/(n - p_1)$ or, less biased for small counts, the Pearson estimate $\hat\phi = X^2/(n - p_1)$ with $X^2 = \sum w_i(y_i - \hat\mu_i)^2/V(\hat\mu_i)$. In the normal case this is the [regression F-test](/regression-f-test/) and has the exact $F_{p_1 - p_0,\, n - p_1}$ law. In the other families the F law is an approximation.
5. **The deviance of one model is not in general $\chi^2_{n - p}$.** The saturated model has $n$ parameters, so the number of parameters grows with the data and Wilks' theorem does not apply to $D^*$ itself. $D^*$ is close to $\chi^2_{n-p}$ under small-dispersion limits with $n$ fixed: Poisson counts whose means are all large, or binomial counts with all $m_i\mu_i$ and $m_i(1 - \mu_i)$ large.
6. **Binary data.** For Bernoulli responses with the logit link, $D$ depends on the data only through $\hat\mu$. Proof: for $y \in \{0, 1\}$, $d(y, \mu) = -2[y\eta - \log(1 + e^\eta)]$ with $\eta = \log\frac{\mu}{1 - \mu}$, so $D = -2\sum_i[y_i\hat\eta_i - \log(1 + e^{\hat\eta_i})]$. With $\hat\eta = X\hat b$, the score equations $X^\top(y - \hat\mu) = 0$ give $y^\top\hat\eta = (X^\top y)^\top\hat b = (X^\top\hat\mu)^\top\hat b = \hat\mu^\top\hat\eta$. So $D = -2\sum_i[\hat\mu_i\hat\eta_i - \log(1 + e^{\hat\eta_i})]$, which is fixed once $\hat\mu$ is fixed. It cannot measure how far $y$ is from $\hat\mu$.
7. **Deviance residuals.** $r_i = \operatorname{sign}(y_i - \hat\mu_i)\sqrt{w_i\,d(y_i, \hat\mu_i)}$ satisfy $\sum r_i^2 = D$. Pierce and Schafer (1986) showed that they are closer to normal than the Pearson residuals $(y_i - \hat\mu_i)\sqrt{w_i/V(\hat\mu_i)}$, so they are the usual choice for residual plots.

## Examples and non-examples

**Eight counts.** Take $x = 0, 1, \dots, 7$ and the counts $y = (1, 1, 3, 2, 5, 6, 9, 12)$. The Poisson model with $\log\mu_i = b_0 + b_1x_i$, fitted by [iteratively reweighted least squares](/iteratively-reweighted-least-squares/), gives $\hat b = (0.0254, 0.3561)$ and

$$\hat\mu = (1.026, 1.464, 2.091, 2.985, 4.262, 6.084, 8.687, 12.402).$$

The fitted counts sum to 39, the same as the observed counts: this is the score equation of the intercept under the canonical link. The unit deviances are $0.001, 0.166, 0.348, 0.368, 0.121, 0.001, 0.011, 0.013$, so the residual deviance is $D_1 = 1.029$ on $8 - 2 = 6$ degrees of freedom, and the Pearson statistic is $X^2 = 1.022$. The null model $\hat\mu_i = 39/8$ has deviance $D_0 = 22.586$ on 7 degrees of freedom. The log-likelihoods are $l_1 = -13.0816$ and $l_0 = -23.8600$, and

$$D_0 - D_1 = 21.557 = 2(l_1 - l_0),$$

as Fact 3 says. On $\chi^2_1$ its p-value is $3.4 \times 10^{-6}$, so the slope is needed. $D_1$ is small for 6 degrees of freedom, but the next example shows why that comparison is rough for counts this small.

**The mean of a unit deviance for small counts.** For one Poisson count $Y$ with mean $\mu$, the expectation of $d(Y, \mu)$ at the true mean is:

| $\mu$ | 0.1 | 0.5 | 1 | 2 | 5 | 20 |
|---|---|---|---|---|---|---|
| $\mathrm E\,d(Y, \mu)$ | 0.474 | 1.007 | 1.147 | 1.139 | 1.047 | 1.009 |

The $\chi^2_{n-p}$ reference assumes a mean near 1 per observation. With many counts below 1 the deviance is too small on average, and with means between 1 and 5 it is too large by about 5 to 15%. Across 100 cells these errors add up to many units of the reference scale.

**Non-example: deviance as a test of fit for binary data.** Fit only an intercept to $n$ Bernoulli responses with $s$ successes. Then $\hat\mu = s/n$ and $D = -2n[\hat\mu\log\hat\mu + (1 - \hat\mu)\log(1 - \hat\mu)]$. For $\hat\mu = 0.5$ this is $2n\log 2 = 1.386n$, and for $\hat\mu = 0.1$ it is $0.650n$, whatever the order of the zeros and ones. So $D/(n - 1)$ is about 1.39 or about 0.65 because of the success rate, not because of lack of fit. Fact 6 shows that the same holds for every logistic regression. Grouped binomial data with large $m_i$, or a test that compares nested models, avoid the problem.

**Non-example: deviances from different data.** If one model drops the rows with a missing value of $x_3$ and the other keeps them, the saturated terms differ and $D_0 - D_1$ is not a likelihood ratio statistic. Both models must be fitted to the same rows.

**Non-example: deviances of models that are not nested.** For a model with $\log\mu = b_0 + b_1x$ and another with $\log\mu = b_0 + b_1\log(1 + x)$, the difference of deviances is not $\chi^2$ under either model. Compare such models by an information criterion or by [cross-validation](/cross-validation/).

## Related definitions

- **Null deviance.** The deviance of the intercept-only model. $1 - D_1/D_0$ is the fraction of deviance explained, the analogue of the [coefficient of determination](/coefficient-of-determination/); for the eight counts it is $0.954$.
- **[Akaike information criterion](/akaike-information-criterion/).** For a fixed family and $\phi$, $-2l(\hat\mu; y) = D^* - 2l(y; y)$, and the last term depends only on the data. So differences of AIC between models for the same data are differences of $D^*$ plus twice the differences of the numbers of parameters.
- **Pearson statistic.** $X^2 = \sum w_i(y_i - \hat\mu_i)^2/V(\hat\mu_i)$ is the second-order expansion of $D$ in $y_i$ around $\hat\mu_i$, since $d(y, \mu) = (y - \mu)^2/V(\mu) + O\bigl((y - \mu)^3\bigr)$. In a contingency table it is the statistic of the [chi-squared goodness-of-fit test](/chi-squared-goodness-of-fit-test/), and $D$ is the likelihood ratio statistic $G^2$.
- **Quasi-deviance.** The same integral $2\int_\mu^y (y - t)/V(t)\,dt$ with any variance function $V$ defines a deviance for [quasi-likelihood](/quasi-likelihood/) models that have no full likelihood.
- **[Cross-entropy loss](/cross-entropy-loss/).** For Bernoulli responses, $D$ is $2n$ times the average cross-entropy loss of the fitted probabilities.
- **[Logistic regression](/logistic-regression/).** The usual software output reports the residual and null deviances. Fact 6 says how to read them.

## References
