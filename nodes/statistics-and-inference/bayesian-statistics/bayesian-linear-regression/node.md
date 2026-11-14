---
tag: PQS5CE
kind: model
slug: bayesian-linear-regression
name: Bayesian linear regression
aliases:
- conjugate normal linear model
area: statistics-and-inference/bayesian-statistics
level: core
summary: Linear regression with a normal or normal-inverse-gamma prior on the coefficients and variance. The posterior and predictive laws are in closed form.
prereqs: [ordinary-least-squares, conjugate-prior, posterior-predictive-distribution, bayesian-inference]
see_also: [ridge-regression, gaussian-process, kalman-filter, empirical-bayes, linear-mixed-model, bayesian-information-criterion, credible-interval, gauss-markov-theorem]
sources:
  - paper: doi:10.1111/j.2517-6161.1972.tb00885.x
    title: "D. V. Lindley and A. F. M. Smith, Bayes estimates for the linear model, Journal of the Royal Statistical Society B 34(1), 1972"
    locator: pages 1 to 41, with discussion (the normal linear model with normal priors in stages, and the posterior mean as a weighted combination of least squares and prior means)
  - book: isbn:9781439840955
    title: "Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, 3rd edition, CRC Press, 2013"
    locator: Chapters 2 and 3 (conjugate normal models, the normal-inverse-chi-square prior and the t marginal) and Chapter 14 (the regression model under the prior proportional to 1/sigma^2, with its t posterior and predictive laws)
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: Section 3.3 (Bayesian linear regression with known noise, the parameter posterior and the predictive distribution) and Section 3.5 (the evidence approximation)
---

Bayesian linear regression is the linear model $y = X\beta + \varepsilon$ with normal errors, together with a prior on the coefficients $\beta$ and, if it is unknown, on the error variance $\sigma^2$. With a normal prior on $\beta$ and known $\sigma^2$, or a normal-inverse-gamma prior on $(\beta, \sigma^2)$, the prior is [conjugate](/conjugate-prior/): the posterior is in the same family, and the [posterior predictive distribution](/posterior-predictive-distribution/) of a new response is normal or Student t, all in closed form. With the prior $N(0, \tau^2 I)$ and known $\sigma$ the posterior mean is the [ridge regression](/ridge-regression/) estimate with $\lambda = \sigma^2/\tau^2$, and with the prior proportional to $1/\sigma^2$ the credible intervals have the numbers of the least squares t intervals.

## The machine

The data are $n$ responses $y = (y_1, \ldots, y_n)^\top$ and an $n \times p$ design matrix $X$ of fixed covariates, with rank $p$ unless the prior is proper. Given the parameters,

$$y \mid \beta, \sigma^2 \sim N(X\beta,\ \sigma^2 I_n), \qquad \beta \in \mathbb{R}^p,\ \sigma^2 > 0.$$

So $f(y \mid \beta, \sigma^2) = (2\pi\sigma^2)^{-n/2}\exp(-\lVert y - X\beta\rVert^2/(2\sigma^2))$. The model is the same as for [ordinary least squares](/ordinary-least-squares/); what is new is a prior, and three standard choices give closed forms.

1. **Known variance, normal prior.** $\sigma^2$ is known and $\beta \sim N(m_0, V_0)$ with $V_0$ positive definite.
2. **Normal-inverse-gamma prior.** $\beta \mid \sigma^2 \sim N(m_0, \sigma^2 V_0)$ and $\sigma^2 \sim$ inverse gamma with shape $a_0 > 0$ and scale $b_0 > 0$, so the prior density of $\sigma^2$ is proportional to $(\sigma^2)^{-a_0 - 1} e^{-b_0/\sigma^2}$. The prior variance of $\beta$ scales with $\sigma^2$, which is what makes it conjugate.
3. **The reference prior.** $\pi(\beta, \sigma^2) \propto 1/\sigma^2$ on $\mathbb{R}^p \times (0, \infty)$, an [improper prior](/improper-prior/). The posterior is proper when $X$ has rank $p$, $n > p$ and the residuals are not all 0.

The conditions are those of the linear model: the mean is linear in $\beta$, the errors are independent with equal variance and normal, and $X$ is treated as fixed (or the analysis is conditional on it). A new response at covariate row $x_*$ is $y_* = x_*^\top\beta + \varepsilon_*$ with $\varepsilon_* \sim N(0, \sigma^2)$ independent of $y$ given the parameters.

## What it counts

The parameters are $\beta$ and $\sigma^2$. The model gives, in closed form:

- the posterior law $\pi(d\beta, d\sigma^2 \mid y)$, its mean, covariance and marginals, and so [credible intervals](/credible-interval/) for each coefficient and for each mean response $x_*^\top\beta$;
- the posterior predictive law of a new response $y_*$ at $x_*$, which adds the noise $\varepsilon_*$ to the uncertainty in $x_*^\top\beta$;
- the [marginal likelihood](/marginal-likelihood/) $m(y) = \int f(y \mid \beta, \sigma^2)\, \pi(d\beta, d\sigma^2)$, used to compare designs, to choose prior scales and to compare models.

The arithmetic cost is that of least squares: forming $X^\top X$ and $X^\top y$ takes $O(np^2)$ operations, one [Cholesky factorization](/cholesky-decomposition/) of the $p \times p$ posterior precision matrix takes $O(p^3)$, and each predictive mean and variance then takes $O(p^2)$. No step needs an explicit matrix inverse.

## Relation to other models

**Ridge regression and Tikhonov regularization.** Under prior 1 with $m_0 = 0$ and $V_0 = \tau^2 I$, the posterior mean and mode are

$$m_n = (X^\top X + \lambda I)^{-1}X^\top y, \qquad \lambda = \sigma^2/\tau^2,$$

the ridge estimate, which is [Tikhonov regularization](/tikhonov-regularization/) with an identity operator. The penalty $\lambda\lVert\beta\rVert^2$ is $-2\sigma^2$ times the log prior, up to a constant. The Bayesian model adds a covariance to the point estimate. A prior with $V_0 = \tau^2 I$ shrinks the intercept as well; to leave it unshrunk, give it a flat prior or center $y$ and the columns of $X$.

**Gaussian processes.** If $\beta \sim N(0, \tau^2 I)$, the function $g(x) = \phi(x)^\top\beta$ of a feature vector $\phi(x)$ is a [Gaussian process](/gaussian-process/) with covariance $k(x, x') = \tau^2\phi(x)^\top\phi(x')$. The predictive law of this model is the Gaussian process regression predictive law with that kernel, by the Woodbury identity. The first form costs $O(np^2 + p^3)$ and the second $O(n^3)$, so the form with the smaller of $n$ and $p$ is cheaper.

**The Kalman filter.** Under prior 1 the posterior after $y_1, \ldots, y_t$ is the prior for $y_{t+1}$, and the update for one row is a rank-one correction of $V$ and $m$. This is the [Kalman filter](/kalman-filter/) for a state $\beta$ that does not change in time, observed through $y_t = x_t^\top\beta + \varepsilon_t$; it is also recursive least squares.

**Hierarchical and mixed models.** Lindley and Smith (1972) put normal priors on $\beta$ in stages, so that the prior mean of $\beta$ has its own normal prior. A [linear mixed model](/linear-mixed-model/) has the same structure for a subset of the coefficients, the random effects, whose prior variance is estimated. Choosing $\tau^2$ and $\sigma^2$ by maximizing $m(y)$ is [empirical Bayes](/empirical-bayes/), called the evidence approximation in machine learning.

**Generalized linear models.** For a binary or count response the normal likelihood is replaced and conjugacy is lost; the posterior then needs a Laplace approximation, Markov chain Monte Carlo or variational methods.

## Known results in the model

### Known variance and normal prior

Under prior 1, completing the square in $\beta$ in $\log f(y \mid \beta) + \log \pi(\beta)$ gives the posterior

$$\beta \mid y \sim N(m_n, V_n), \qquad V_n = \big(V_0^{-1} + X^\top X/\sigma^2\big)^{-1}, \qquad m_n = V_n\big(V_0^{-1}m_0 + X^\top y/\sigma^2\big).$$

Precisions add, and the posterior mean is a precision-weighted combination of the prior mean and, when $X$ has rank $p$, the least squares estimate $\hat\beta = (X^\top X)^{-1}X^\top y$, since $X^\top y = X^\top X\hat\beta$. The predictive law of $y_*$ at $x_*$ is

$$y_* \mid y \sim N\big(x_*^\top m_n,\ \sigma^2 + x_*^\top V_n x_*\big),$$

where $\sigma^2$ is the noise and $x_*^\top V_n x_*$ is the uncertainty about the mean. The marginal law of the data is $y \sim N(Xm_0, \sigma^2 I + XV_0X^\top)$, and its density at the observed $y$ is the marginal likelihood.

**A hand example.** Take $x = (0, 1, 2, 3, 4)$, $y = (1.1, 1.9, 3.2, 3.8, 5.1)$, the model $y_i = \beta_0 + \beta_1 x_i + \varepsilon_i$ with $\sigma = 0.5$, and the prior $N(0, 2^2 I)$, so $\lambda = 0.25/4 = 0.0625$. Here $X^\top X = \begin{pmatrix} 5 & 10 \\ 10 & 30 \end{pmatrix}$ and $X^\top y = (15.1, 40.1)^\top$. The least squares estimate is $(1.04, 0.99)$. The posterior mean is $(1.01442, 0.99645)$, equal to $(X^\top X + 0.0625 I)^{-1}X^\top y$; both coefficients move a little toward 0. The posterior standard deviations are 0.37947 and 0.15572, with correlation $-0.8106$. At $x_* = 5$ the predictive law has mean 5.99668 and standard deviation 0.72197, so the 95% predictive interval is $[4.5816, 7.4117]$. A one-coefficient version, $y_i = \beta x_i + \varepsilon_i$ with the same data, $\sigma = 0.5$ and prior $N(0, 4)$, has posterior mean 1.3338877 and variance 0.0083160 in closed form; a direct numerical integration of the unnormalized posterior on 200000 equal steps of $[-5, 5]$ gives the same values to 7 digits.

### Unknown variance and normal-inverse-gamma prior

Under prior 2 the posterior is again normal-inverse-gamma:

$$V_n = (V_0^{-1} + X^\top X)^{-1}, \quad m_n = V_n(V_0^{-1}m_0 + X^\top y), \quad a_n = a_0 + \tfrac n2, \quad b_n = b_0 + \tfrac12\big(y^\top y + m_0^\top V_0^{-1}m_0 - m_n^\top V_n^{-1}m_n\big).$$

Integrating out $\sigma^2$ gives the marginal posterior of $\beta$ as a multivariate Student t with $2a_n$ degrees of freedom, location $m_n$ and scale matrix $(b_n/a_n)V_n$. The predictive law of $y_*$ is Student t with $2a_n$ degrees of freedom, location $x_*^\top m_n$ and squared scale $(b_n/a_n)(1 + x_*^\top V_n x_*)$. Its tails are heavier than those of the normal predictive law because $\sigma^2$ is uncertain. The posterior mean of $\sigma^2$ is $b_n/(a_n - 1)$ when $a_n > 1$. The marginal likelihood is

$$m(y) = (2\pi)^{-n/2}\,\frac{\det(V_n)^{1/2}}{\det(V_0)^{1/2}}\,\frac{b_0^{a_0}}{b_n^{a_n}}\,\frac{\Gamma(a_n)}{\Gamma(a_0)}.$$

**The same example.** With $m_0 = 0$, $V_0 = 4I$, $a_0 = b_0 = 1$: $m_n = (0.94835, 1.01211)$, $a_n = 3.5$, $b_n = 1.30204$ and $E[\sigma^2 \mid y] = 0.52081$. The least squares residual variance is only $s^2 = 0.035667$ with $n - p = 3$ degrees of freedom; the prior with $b_0/a_0 = 1$ carries the weight of about $2a_0 = 2$ observations with squared error 1, and it pulls $\sigma^2$ up. The 95% interval for the slope from the $t_7$ marginal is $[0.5812, 1.4430]$, and the 95% predictive interval at $x_* = 5$, from $t_7$ with location 6.00893 and scale 0.87236, is $[3.9461, 8.0717]$. For a one-coefficient check, $y_i = \beta x_i + \varepsilon_i$ with $\beta \mid \sigma^2 \sim N(0, 4\sigma^2)$ and $\sigma^2 \sim$ inverse gamma$(1, 1)$, the t density of $\beta$ agrees with a numerical integration of the joint posterior (2001 points in $\beta$ by 1801 points in $\log\sigma^2$) to about 1 part in $10^6$ at 5 points.

### The prior proportional to 1/sigma^2

Prior 3 is the limit of prior 2 as $V_0^{-1} \to 0$, $a_0 \to -p/2$ and $b_0 \to 0$. With $s^2 = \lVert y - X\hat\beta\rVert^2/(n - p)$,

$$\beta \mid y \sim t_{n-p}\big(\hat\beta,\ s^2(X^\top X)^{-1}\big), \qquad y_* \mid y \sim t_{n-p}\big(x_*^\top\hat\beta,\ s^2(1 + x_*^\top(X^\top X)^{-1}x_*)\big),$$

and $(n - p)s^2/\sigma^2$ given $y$ is chi-square with $n - p$ degrees of freedom. The posterior mean of $\beta$ is the least squares estimate, and the equal-tailed 95% credible interval for $\beta_j$ is $\hat\beta_j \pm t_{(n-p, 0.975)}\, s\sqrt{((X^\top X)^{-1})_{jj}}$. In the example it is $[0.79994, 1.18006]$ for the slope, with $\hat\beta_1 = 0.99$, $s^2 = 0.035667$ and $t_{(3, 0.975)} = 3.18245$.

### Frequentist properties of the same numbers

The statements above are posterior probabilities given $y$. Statements about repeated samples at a fixed $\beta$ are different and are listed separately.

- Under prior 3 the credible intervals for $\beta_j$ and the predictive intervals have the same numbers as the classical t confidence and prediction intervals, so their coverage at every fixed $(\beta, \sigma^2)$ is exactly 95% when the model holds. This is an exact agreement for this prior and model only.
- Under prior 1 with $m_0 = 0$ and $V_0 = \tau^2 I$, the posterior mean has expectation $(X^\top X + \lambda I)^{-1}X^\top X\beta$, so it is biased toward 0 for every $\beta \ne 0$, and covariance $\sigma^2(X^\top X + \lambda I)^{-1}X^\top X(X^\top X + \lambda I)^{-1}$, which is smaller than the least squares covariance $\sigma^2(X^\top X)^{-1}$. Least squares is the best linear unbiased estimator by the [Gauss-Markov theorem](/gauss-markov-theorem/); the posterior mean is not unbiased, so the theorem does not rank them.
- The credible intervals under a proper prior have no exact coverage guarantee at a fixed $\beta$. As $n \to \infty$ with $p$ fixed and $X^\top X/n$ converging to a positive definite matrix, the prior's effect vanishes and they become asymptotic confidence intervals by the [Bernstein-von Mises theorem](/bernstein-von-mises-theorem/).

### Computation and checks

- Compute $m_n$ by solving $(V_0^{-1} + X^\top X/\sigma^2)\, m_n = V_0^{-1}m_0 + X^\top y/\sigma^2$ with the Cholesky factor of the left matrix, and get $x_*^\top V_n x_*$ as the squared norm of the solution of one triangular system. When $X^\top X$ is ill conditioned, the QR decomposition of $X/\sigma$ stacked on a square root of $V_0^{-1}$ is more accurate than forming $X^\top X$.
- The posterior under prior 3 exists only if $X$ has full column rank and $n > p$; with $p > n$ a proper prior on $\beta$ is required, as for ridge regression.
- The marginal likelihood under an improper prior is defined only up to a constant, so it cannot compare models; the [Bayesian information criterion](/bayesian-information-criterion/) is its large-sample approximation for proper priors.

## References
