---
tag: 6PNECN
kind: definition
slug: conjugate-prior
name: Conjugate prior
aliases:
- conjugate family
- natural conjugate prior
area: machine-learning/probabilistic-inference
level: intro
summary: "A family of priors that a likelihood maps to posteriors in the same family, so Bayesian updating only changes a few hyperparameters. Every exponential family has one."
history:
  year: 1961
  people: [Howard Raiffa, Robert Schlaifer, Persi Diaconis, Donald Ylvisaker]
  note: Raiffa and Schlaifer named and catalogued natural conjugate priors in 1961. Diaconis and Ylvisaker characterized the conjugate priors of exponential families in 1979.
prereqs: [bayesian-inference, probability-density-function]
see_also: [exponential-family-distribution, marginal-likelihood, bayes-theorem, binomial-distribution, poisson-distribution, naive-bayes-classifier, latent-dirichlet-allocation, thompson-sampling]
sources:
  - paper: doi:10.1214/aos/1176344611
    title: "Persi Diaconis and Donald Ylvisaker, Conjugate priors for exponential families, Annals of Statistics 7(2), 1979"
    locator: pp. 269 to 281 (the conjugate prior of a natural exponential family, the condition for it to be proper, and the linear posterior mean of the mean parameter)
  - book: "Howard Raiffa and Robert Schlaifer, Applied Statistical Decision Theory, Division of Research, Harvard Business School, 1961"
    locator: Chapter 3 (natural conjugate prior distributions)
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: Section 2.1.1 (beta), Section 2.2.1 (Dirichlet), Section 2.3.6 (Gaussian, including the normal-gamma prior) and Section 2.4.2 (conjugate priors of the exponential family)
  - book: isbn:9781439840955
    title: "Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, 3rd edition, CRC Press, 2013"
    locator: Chapter 2 (binomial, normal and Poisson models with conjugate priors) and Chapter 3 (the normal model with unknown mean and variance, the multinomial and the Dirichlet)
---

A conjugate prior for a likelihood is a family of prior distributions that the likelihood maps into itself: for every prior in the family and every data set, the posterior is again in the family. Then [Bayesian inference](/bayesian-inference/) reduces to updating a few numbers, the hyperparameters, and the posterior, the posterior predictive and the [marginal likelihood](/marginal-likelihood/) have closed forms. The beta prior for a coin is the standard case. Every [exponential family](/exponential-family-distribution/) with $k$ natural parameters has a conjugate family with $k + 1$ hyperparameters. Outside exponential families such small families exist only in special cases, such as the uniform model with a Pareto prior.

## Definition

Let $\{p(x \mid \theta) : \theta \in \Theta\}$ be a model for one observation, and let observations $x_1, \ldots, x_n$ be independent given $\theta$. A family $\mathcal{F}$ of prior distributions on $\Theta$ is **conjugate** to the model if, for every $\pi \in \mathcal{F}$, every $n \ge 1$ and every data set with $0 < \int \prod_i p(x_i \mid \theta)\,\pi(\theta)\,d\theta < \infty$, the posterior

$$
\pi(\theta \mid x_1, \ldots, x_n) \propto \pi(\theta)\prod_{i=1}^n p(x_i \mid \theta)
$$

is in $\mathcal{F}$. The family of all distributions on $\Theta$ meets this definition, so the term is useful only for a family with a fixed, small number of parameters. If $\mathcal{F}$ is closed under one update, it is closed under $n$ updates, because the posterior after $x_1, \ldots, x_{n-1}$ is the prior for $x_n$.

**The exponential family case.** Let $p(x \mid \eta) = h(x)\exp(\eta^\top T(x) - A(\eta))$, with natural parameter $\eta \in \mathbb{R}^k$, sufficient statistic $T(x)$ and log partition function $A$. For hyperparameters $\chi \in \mathbb{R}^k$ and $\nu > 0$, define

$$
\pi(\eta \mid \chi, \nu) \propto \exp\bigl(\eta^\top \chi - \nu A(\eta)\bigr).
$$

Multiplying by the likelihood $\prod_i h(x_i)\exp(\eta^\top T(x_i) - A(\eta))$ gives

$$
\chi_n = \chi + \sum_{i=1}^n T(x_i), \qquad \nu_n = \nu + n.
$$

So the family is conjugate. The hyperparameter $\nu$ acts as a prior sample size and $\chi$ as a prior sum of sufficient statistics. Diaconis and Ylvisaker (1979) studied this family for a regular natural exponential family, written with $\chi = n_0 x_0$ and $\nu = n_0$. They proved that the prior is proper exactly when $n_0 > 0$ and $x_0$ is in the interior of the convex hull of the support of $T(X)$, and that then the prior mean of the mean parameter $\mu(\eta) = \mathbb{E}[T(X) \mid \eta] = \nabla A(\eta)$ is $x_0$. Applied to the posterior, this gives

$$
\mathbb{E}[\nabla A(\eta) \mid x_1, \ldots, x_n] = \frac{\chi + \sum_i T(x_i)}{\nu + n},
$$

a weighted average of the prior guess $\chi/\nu$ and the sample mean of $T$. They also proved a converse under conditions on the family: a prior under which this posterior mean is linear in the sample mean must be of the conjugate form.

## Examples and non-examples

**The standard pairs.** Here $s = \sum_i x_i$ and $\bar x = s/n$.

| model for $x_i$ | prior | posterior |
|---|---|---|
| Bernoulli($\theta$) | Beta($a, b$) | Beta($a + s,\ b + n - s$) |
| Poisson($\lambda$) | Gamma(shape $\alpha$, rate $\beta$) | Gamma($\alpha + s,\ \beta + n$) |
| $\mathcal{N}(\theta, \sigma^2)$, $\sigma^2$ known | $\mathcal{N}(\mu_0, \tau_0^2)$ | $\mathcal{N}(\mu_n, \tau_n^2)$, $\tau_n^{-2} = \tau_0^{-2} + n\sigma^{-2}$, $\mu_n = \tau_n^2(\mu_0\tau_0^{-2} + s\sigma^{-2})$ |
| $\mathcal{N}(\mu, \sigma^2)$, both unknown | $\mu \mid \sigma^2 \sim \mathcal{N}(\mu_0, \sigma^2/\kappa_0)$, $\sigma^2 \sim$ InvGamma($\alpha_0, \beta_0$) | $\kappa_n = \kappa_0 + n$, $\mu_n = (\kappa_0\mu_0 + n\bar x)/\kappa_n$, $\alpha_n = \alpha_0 + n/2$, $\beta_n = \beta_0 + \tfrac12\sum_i (x_i - \bar x)^2 + \frac{\kappa_0 n (\bar x - \mu_0)^2}{2\kappa_n}$ |
| Categorical on $k$ values, counts $c_1, \ldots, c_k$ | Dirichlet($\alpha_1, \ldots, \alpha_k$) | Dirichlet($\alpha_1 + c_1, \ldots, \alpha_k + c_k$) |

Each row follows by multiplying the prior density by the likelihood and reading off the kernel. For example, $\theta^{a-1}(1-\theta)^{b-1}\cdot\theta^s(1-\theta)^{n-s}$ is the kernel of Beta($a+s, b+n-s$). For the normal-inverse-gamma row, the identity $\sum_i (x_i - \mu)^2 + \kappa_0(\mu - \mu_0)^2 = \kappa_n(\mu - \mu_n)^2 + \sum_i (x_i - \bar x)^2 + \frac{\kappa_0 n}{\kappa_n}(\bar x - \mu_0)^2$ splits the exponent into a normal kernel in $\mu$ and an inverse gamma kernel in $\sigma^2$. Under this posterior, $\mathbb{E}[\mu] = \mu_n$, $\mathbb{E}[\sigma^2] = \beta_n/(\alpha_n - 1)$ for $\alpha_n > 1$, and $\operatorname{Var}[\mu] = \beta_n/((\alpha_n - 1)\kappa_n)$.

**Worked numbers.** Each of these posteriors agrees with a direct numerical integration of prior times likelihood on a grid, in its mean and its variance.

- Beta-binomial: prior Beta(2, 2), data 1, 1, 0, 1, 1, 0, 1, 1. Posterior Beta(8, 4), mean $2/3$, variance $8 \cdot 4/(12^2 \cdot 13) = 2/117$.
- Gamma-Poisson: prior Gamma(2, 1), counts 3, 1, 4, 1, 5. Posterior Gamma(16, 6), mean $8/3$, variance $4/9$.
- Normal with known variance: $\sigma^2 = 4$, prior $\mathcal{N}(0, 1)$, data 2.1, 1.3, 3.0, 2.6 with $\bar x = 2.25$. The precision is $1 + 4/4 = 2$, so $\tau_n^2 = 1/2$ and $\mu_n = \tfrac12(0 + 9/4) = 9/8$. The prior counts like 4 observations, since $\sigma^2/\tau_0^2 = 4$, and the posterior mean is halfway between $0$ and $\bar x$.
- Normal-inverse-gamma: the same data, $\mu_0 = 0$, $\kappa_0 = 1$, $\alpha_0 = \beta_0 = 2$. Then $\sum_i(x_i - \bar x)^2 = 1.61$, $\kappa_n = 5$, $\mu_n = 1.8$, $\alpha_n = 4$, $\beta_n = 2 + 0.805 + 4 \cdot 2.25^2/10 = 4.83$, and $\mathbb{E}[\sigma^2] = 4.83/3 = 1.61$.
- Dirichlet-multinomial: prior Dirichlet(1, 1, 1), counts (5, 2, 3). Posterior Dirichlet(6, 3, 4), mean $(6/13, 3/13, 4/13)$. The prior adds one pseudo-count to each class; this is add-one smoothing in the [naive Bayes classifier](/naive-bayes-classifier/).

**The general form gives the special cases.** For Bernoulli data, $T(x) = x$ and $A(\eta) = \log(1 + e^\eta)$ with $\theta = 1/(1 + e^{-\eta})$. The change of variable $d\eta = d\theta/(\theta(1-\theta))$ turns $\exp(\eta\chi - \nu A(\eta))$ into $\theta^{\chi-1}(1-\theta)^{\nu-\chi-1}$, the Beta($\chi, \nu - \chi$) density. For Poisson data, $A(\eta) = e^\eta$ with $\lambda = e^\eta$, and the prior becomes Gamma($\chi, \nu$). In the Poisson example the posterior mean of $\lambda = \nabla A(\eta)$ is $(2 + 14)/(1 + 5) = 8/3$, the Diaconis-Ylvisaker formula.

**Uniform with a Pareto prior.** For $x_i$ uniform on $(0, \theta)$, the likelihood is $\theta^{-n}\,[\theta \ge \max_i x_i]$. A Pareto prior $\pi(\theta) \propto \theta^{-(\alpha+1)}[\theta \ge m]$ gives the Pareto posterior with $\alpha + n$ and $\max(m, \max_i x_i)$. This family is conjugate although the uniform is not an exponential family; its support depends on $\theta$.

**Mixtures.** If $\mathcal{F}$ is conjugate, so is the set of finite mixtures $\sum_j w_j \pi_j$ with $\pi_j \in \mathcal{F}$. The posterior is $\sum_j w_j' \pi_j(\cdot \mid D)$ with $w_j' \propto w_j\,p_j(D)$, where $p_j(D)$ is the marginal likelihood under $\pi_j$. So a prior with two bumps can still be updated in closed form.

**Non-examples.**

- A beta prior for a Poisson rate is not conjugate: the posterior kernel $\lambda^{a-1+s}(1-\lambda)^{b-1}e^{-n\lambda}$ on $(0, 1)$ is not a beta kernel.
- [Logistic regression](/logistic-regression/) with a Gaussian prior on the weights is not conjugate: the posterior is $\propto e^{-\lVert w \rVert^2/2\tau^2}\prod_i \sigma(y_i w^\top x_i)$, which is not Gaussian. One uses the Laplace approximation, sampling or [variational inference](/variational-inference/).
- A conjugate family can contain improper members. Beta($a, b$) with $a = 0$ is not a distribution, and the posterior is proper only after at least one success.

## Related definitions

- [Exponential family distribution](/exponential-family-distribution/): the models with the general conjugate family above. By the Pitman-Koopman-Darmois theorem, under smoothness conditions they are also the only models with a fixed support that have a sufficient statistic of fixed dimension for every sample size.
- [Marginal likelihood](/marginal-likelihood/): for a conjugate pair it is a ratio of normalizing constants, for example $B(a+s, b+n-s)/B(a, b)$ for one ordered Bernoulli sequence.
- [Bayesian inference](/bayesian-inference/): the posterior and the posterior predictive. Under a conjugate prior the predictive is also closed form: beta-binomial, negative binomial for gamma-Poisson, Student t for normal-inverse-gamma, Dirichlet-multinomial.
- [MAP estimation](/maximum-a-posteriori-estimation/): with a Beta($a, b$) prior and $a, b \ge 1$, the MAP estimate is $(a + s - 1)/(a + b + n - 2)$, the MLE with pseudo-counts.
- [Latent Dirichlet allocation](/latent-dirichlet-allocation/) and the [Dirichlet process](/dirichlet-process/) are built on Dirichlet-multinomial conjugacy, which makes collapsed [Gibbs sampling](/gibbs-sampling/) possible.
- [Thompson sampling](/thompson-sampling/) with Bernoulli rewards keeps one beta posterior per arm.

## References
