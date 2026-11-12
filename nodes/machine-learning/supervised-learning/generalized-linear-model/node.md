---
tag: KTAMYG
kind: model
slug: generalized-linear-model
name: Generalized linear model
aliases:
- GLM
- generalised linear model
- Nelder-Wedderburn model
area: machine-learning/supervised-learning
level: advanced
summary: "A regression model whose response comes from an exponential family, with its mean linked to a linear predictor. IRLS fits it, and IRLS is Newton's method for the canonical link."
history:
  year: 1972
  people: [John Nelder, Robert Wedderburn]
  note: Nelder and Wedderburn put linear, logistic, probit, Poisson and gamma regression into one model in 1972 and fitted all of them with one weighted least squares algorithm.
prereqs: [linear-regression, exponential-family-distribution, maximum-likelihood-estimation]
see_also: [logistic-regression, softmax-regression, ordinary-least-squares, poisson-distribution, binomial-distribution, newton-method-for-systems, cross-entropy-loss, mean-squared-error]
sources:
  - paper: doi:10.2307/2344614
    title: "J. A. Nelder and R. W. M. Wedderburn, Generalized linear models, Journal of the Royal Statistical Society, Series A 135(3), 1972"
    locator: pp. 370-384, the three components of the model, the fitting algorithm by iterative weighted least squares, and the deviance
  - book: isbn:9780412317606
    title: "P. McCullagh and J. A. Nelder, Generalized Linear Models, 2nd edition, Chapman and Hall, 1989"
    locator: Chapter 2, Sections 2.2 to 2.5 (the components, the likelihood, the deviance and the fitting algorithm), and Chapter 4 for binary data
  - paper: doi:10.1093/biomet/61.3.439
    title: "R. W. M. Wedderburn, Quasi-likelihood functions, generalized linear models, and the Gauss-Newton method, Biometrika 61(3), 1974"
    locator: pp. 439-447, quasi-likelihood from a mean and a variance function only, and the same fitting equations
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: Section 4.3.3 (iterative reweighted least squares) and Section 4.3.6 (canonical link functions)
---

A generalized linear model (GLM) is a regression model for a response that need not be normal: counts, yes or no answers, proportions or positive amounts. It has three parts. The response comes from an [exponential family](/exponential-family-distribution/), the input acts through a linear predictor $\eta = x^\top\beta$, and a link function $g$ connects the two by $g(\mathbb{E}[y \mid x]) = \eta$. [Linear regression](/linear-regression/), [logistic regression](/logistic-regression/) and Poisson regression are the best known cases. Nelder and Wedderburn (1972) showed that one algorithm, iteratively reweighted least squares (IRLS), fits all of them by [maximum likelihood](/maximum-likelihood-estimation/). IRLS is Fisher scoring, and for the canonical link it is exactly Newton's method.

## The machine

The data are $n$ examples $(x_i, y_i)$ with $x_i \in \mathbb{R}^d$, the rows of the $n \times d$ matrix $X$. This page follows the GLM literature and writes the coefficients as $\beta \in \mathbb{R}^d$; an intercept is a column of ones in $X$ (other pages of the site write $w$ and $b$). The $y_i$ are independent given the $x_i$.

| Symbol | Meaning |
|---|---|
| $\theta_i$ | the natural parameter of example $i$ |
| $b(\theta)$ | the cumulant function of the family |
| $\phi$ | the dispersion, the same for all examples |
| $\mu_i = \mathbb{E}[y_i \mid x_i]$ | the mean |
| $V(\mu)$ | the variance function |
| $\eta_i = x_i^\top\beta$ | the linear predictor |
| $g$ | the link function, with $g(\mu_i) = \eta_i$ |

A GLM has three parts.

1. The random part. Each $y_i$ has a density (or mass function) from an exponential dispersion family,
$$
f(y; \theta, \phi) = \exp\!\left(\frac{y\theta - b(\theta)}{\phi} + c(y, \phi)\right).
$$
Differentiating $\int f\,dy = 1$ once and twice in $\theta$ gives $\mu = b'(\theta)$ and $\operatorname{Var}(y) = \phi\, b''(\theta)$. Since $b'$ is increasing, $\theta$ is a function of $\mu$, and the variance is $\phi V(\mu)$ with $V(\mu) = b''(\theta(\mu))$.
2. The systematic part. The input enters only through $\eta_i = x_i^\top\beta$.
3. The link. A smooth, strictly monotone $g$ maps the mean to the linear predictor: $g(\mu_i) = \eta_i$, so $\mu_i = g^{-1}(x_i^\top\beta)$. The link $g = (b')^{-1}$ is the canonical link. With it, $\theta_i = \eta_i$: the linear predictor is the natural parameter.

The common families, with $\phi$ and the canonical link:

| Family | $b(\theta)$ | $V(\mu)$ | $\phi$ | canonical link $g(\mu)$ | name of the model |
|---|---|---|---|---|---|
| normal $N(\mu, \sigma^2)$ | $\theta^2/2$ | $1$ | $\sigma^2$ | $\mu$ (identity) | linear regression |
| Bernoulli | $\log(1 + e^\theta)$ | $\mu(1-\mu)$ | $1$ | $\log\frac{\mu}{1-\mu}$ (logit) | logistic regression |
| [Poisson](/poisson-distribution/) | $e^\theta$ | $\mu$ | $1$ | $\log\mu$ (log) | Poisson regression |
| gamma | $-\log(-\theta)$ | $\mu^2$ | $1/\nu$ for shape $\nu$ | $-1/\mu$ (negative inverse) | gamma regression |
| inverse Gaussian | $-\sqrt{-2\theta}$ | $\mu^3$ | $1/\lambda$ | $-1/(2\mu^2)$ | |

Other links are often used: the probit link $\Phi^{-1}(\mu)$ for the Bernoulli family, and the log link for the gamma family, which keeps $\mu > 0$ for every $\beta$. A [binomial](/binomial-distribution/) count of $m_i$ trials is handled as the proportion $y_i/m_i$ with prior weight $m_i$.

The parameter is fitted by maximum likelihood. Up to terms free of $\beta$, the log-likelihood is
$$
\ell(\beta) = \frac{1}{\phi}\sum_{i=1}^n \bigl(y_i\theta_i - b(\theta_i)\bigr).
$$
With the chain rule $d\theta/d\mu = 1/V(\mu)$ and $d\mu/d\eta = 1/g'(\mu)$, the score (the gradient) and the expected information are
$$
U(\beta) = \frac{1}{\phi}\sum_{i=1}^n \frac{y_i - \mu_i}{V(\mu_i)\, g'(\mu_i)}\, x_i, \qquad \mathcal{I}(\beta) = \frac{1}{\phi} X^\top W X, \qquad W = \operatorname{diag}\!\left(\frac{1}{V(\mu_i)\, g'(\mu_i)^2}\right).
$$
The fitting algorithm is IRLS. Each step forms the working response $z_i = \eta_i + (y_i - \mu_i)\, g'(\mu_i)$ and solves a weighted least squares problem:
$$
\beta^{(t+1)} = \bigl(X^\top W X\bigr)^{-1} X^\top W z, \qquad W, z \text{ evaluated at } \beta^{(t)}.
$$
The Python file on this page implements IRLS with the Cholesky factorization of $X^\top W X$ and halves a step when it would lower the likelihood or leave the range of $\mu$. It has the Gaussian, Poisson, binomial and gamma families and the identity, log, logit and inverse links.

## What it counts

The cost of a GLM fit is the number of IRLS iterations times the cost of one iteration. One iteration evaluates $\eta$, $\mu$, $W$ and $z$ in $O(nd)$ operations, forms $X^\top W X$ and $X^\top W z$ in $O(nd^2)$, and solves the $d \times d$ system in $O(d^3)$. Memory is $O(nd)$ for the data plus $O(d^2)$. Solving the weighted problem by a QR factorization of $W^{1/2}X$ costs the same order and is more accurate when $X$ is ill-conditioned, for the reasons given on the [ordinary least squares](/ordinary-least-squares/) page.

There is no useful worst case bound on the number of iterations in terms of $n$ and $d$. In practice IRLS stops after about 5 to 10 iterations when the maximum likelihood estimate exists; this is observed, not proved. The estimate itself need not exist: for logistic regression on separable data and for a Poisson model in which every count of a group is 0, the likelihood has no maximizer and the iterates go to infinity.

The fit is judged by the deviance. Let $\tilde\ell$ be the log-likelihood of the saturated model, which has $\mu_i = y_i$ for all $i$. The deviance is
$$
D = 2\phi\bigl(\tilde\ell - \ell(\hat\beta)\bigr) = 2\sum_{i=1}^n \bigl(y_i(\tilde\theta_i - \hat\theta_i) - b(\tilde\theta_i) + b(\hat\theta_i)\bigr) \ge 0.
$$
For the normal family it is the residual sum of squares $\sum_i (y_i - \hat\mu_i)^2$. For the Poisson family it is $2\sum_i \bigl(y_i\log(y_i/\hat\mu_i) - (y_i - \hat\mu_i)\bigr)$, with $0\log 0 = 0$. For the Bernoulli family it is twice the total [cross-entropy loss](/cross-entropy-loss/) of the fit, because the saturated log-likelihood is 0. A nested model with $q$ fewer coefficients is compared by $(D_{\text{small}} - D_{\text{big}})/\phi$, which is approximately $\chi^2_q$ for large $n$ under the smaller model. When $\phi$ is unknown it is estimated by the Pearson statistic $\hat\phi = \frac{1}{n - d}\sum_i (y_i - \hat\mu_i)^2/V(\hat\mu_i)$.

**Example.** Fit a Poisson model with the log link to $x = 0, 1, 2, 3, 4$ and counts $y = 1, 1, 2, 4, 7$, with an intercept, so $\log\mu_i = \beta_0 + \beta_1 x_i$. Start with $\mu_i = y_i + \frac12$. For the log link $g'(\mu) = 1/\mu$ and $V(\mu) = \mu$, so $W = \operatorname{diag}(\mu_i)$ and $z_i = \log\mu_i + (y_i - \mu_i)/\mu_i$. The iterates are

| step | $\beta_0$ | $\beta_1$ | $\ell(\beta)$ up to a constant |
|---|---|---|---|
| 1 | $-0.216634$ | $0.533567$ | $5.446113$ |
| 2 | $-0.329554$ | $0.564828$ | $5.460390$ |
| 3 | $-0.334254$ | $0.566094$ | $5.460413$ |
| 4 | $-0.334262$ | $0.566096$ | $5.460413$ |

The error is roughly squared at each step, as for Newton's method. The fitted means are $\hat\mu = 0.7159, 1.2609, 2.2209, 3.9119, 6.8904$. They add up to $15 = \sum_i y_i$, and $\sum_i x_i\hat\mu_i = 45 = \sum_i x_i y_i$: these are the score equations $X^\top(y - \hat\mu) = 0$ of the canonical link. The deviance is $0.1849$ on $n - d = 3$ degrees of freedom, so the model fits these counts well. The rate is $e^{\hat\beta_1} = 1.761$: each unit of $x$ multiplies the expected count by about $1.76$.

## Relation to other models

- [Linear regression](/linear-regression/) is the normal family with the identity link. Then $W = I$ and $z = y$, IRLS stops after one step, and the step is [ordinary least squares](/ordinary-least-squares/).
- [Logistic regression](/logistic-regression/) is the Bernoulli family with the logit link. Its negative log-likelihood is the [logistic loss](/logistic-loss/), and IRLS on it is the Newton method of that page. With the probit link the same data give the probit model, whose link is not canonical.
- [Softmax regression](/softmax-regression/) is the multinomial case. It is a multivariate GLM: the response is a vector of class indicators and the canonical link is the inverse of the softmax.
- The [exponential family](/exponential-family-distribution/) page is about the distributions themselves. A GLM is a regression model on top of one of them: it lets the natural parameter (or a function of the mean) depend linearly on $x$.
- A GLM is not the "general linear model" of classical statistics, which is linear regression with a matrix response and normal errors, as in ANOVA and MANOVA.
- Quasi-likelihood (Wedderburn 1974) keeps only the mean $\mu = g^{-1}(x^\top\beta)$ and the variance function $V(\mu)$. The estimating equations and the IRLS algorithm are the same, so a GLM program also fits overdispersed counts and proportions.
- Generalized additive models replace $x^\top\beta$ by a sum of smooth functions of the separate inputs, and they are fitted by IRLS around a smoother.
- [Quantile regression](/quantile-regression/) and [isotonic regression](/isotonic-regression/) are not GLMs: the first models a quantile instead of the mean, and the second drops the linear predictor for a monotone one.
- In a neural network, a final linear layer with a canonical link and the matching negative log-likelihood (the [mean squared error](/mean-squared-error/) for the identity, the cross-entropy for the logit or softmax) is a GLM on the learned features. Its gradient for one example has the GLM form $(\mu - y)$ times the features.

## Known results in the model

**IRLS is Fisher scoring.** Fisher scoring replaces the negative Hessian in Newton's method by the expected information: $\beta^{(t+1)} = \beta^{(t)} + \mathcal{I}(\beta^{(t)})^{-1}U(\beta^{(t)})$.

*Proof.* By the formulas of the machine, $\phi\,U = X^\top W v$ with $v_i = (y_i - \mu_i)\,g'(\mu_i)$, because $\frac{1}{V g'} = \frac{1}{V g'^2}\,g'$. So $\beta + \mathcal{I}^{-1}U = (X^\top W X)^{-1}\bigl(X^\top W X\beta + X^\top W v\bigr) = (X^\top W X)^{-1}X^\top W(\eta + v)$, and $\eta + v = z$. The dispersion $\phi$ cancels. $\square$

So $\phi$ need not be known to fit $\beta$, and each step is a weighted least squares problem that any regression program can solve.

**For the canonical link, IRLS is Newton's method.** The observed and the expected information are equal.

*Proof.* With $\theta_i = \eta_i = x_i^\top\beta$, the log-likelihood is $\ell(\beta) = \frac1\phi\sum_i (y_i x_i^\top\beta - b(x_i^\top\beta))$. Its gradient is $\frac1\phi X^\top(y - \mu)$ and its Hessian is $-\frac1\phi\sum_i b''(\theta_i)\,x_i x_i^\top$, which does not depend on $y$. For the canonical link $g'(\mu) = d\theta/d\mu = 1/V(\mu)$, so $W_{ii} = V(\mu_i)^2/V(\mu_i) = V(\mu_i) = b''(\theta_i)$, and $-\nabla^2\ell = \frac1\phi X^\top W X = \mathcal{I}$. $\square$

For a link that is not canonical the observed information has an extra term that is linear in $y_i - \mu_i$. Its expectation is 0, so the two matrices agree on average but not at a given $\beta$. Fisher scoring then converges linearly near the estimate, not quadratically. For the gamma family with the log link, for example, $W = I$, while the observed information is $\sum_i (y_i/\mu_i)\,x_i x_i^\top$.

**Concavity for the canonical link.** The function $b$ is convex, because $b'' = V \ge 0$. So for the canonical link $\ell(\beta)$ is concave in $\beta$, every solution of the score equations $X^\top(y - \hat\mu) = 0$ is a global maximizer, and if $X$ has full column rank and $V > 0$ the maximizer is unique when it exists. With the step halving of the program the likelihood never decreases. That alone does not prove convergence, but near the maximizer the full Newton step is accepted and the convergence is quadratic. For other links $\ell$ need not be concave and IRLS can stop at a local maximum.

**Moment matching.** For the canonical link and a model with an intercept, the first score equation is $\sum_i \hat\mu_i = \sum_i y_i$: the fitted total equals the observed total, as in the example. Each other column $x_{\cdot j}$ gives $\sum_i x_{ij}\hat\mu_i = \sum_i x_{ij}y_i$.

**Large sample distribution.** Under regularity conditions and a fixed $d$, $\hat\beta$ is consistent and approximately normal with mean $\beta$ and covariance $\phi(X^\top W X)^{-1}$, evaluated at $\hat\beta$. The standard errors that GLM programs report come from this matrix, which IRLS has already formed at its last step.

## References
