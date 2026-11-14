---
tag: 0A2RZM
kind: model
slug: hierarchical-bayesian-model
name: Hierarchical Bayesian model
aliases:
- multilevel Bayesian model
- Bayesian hierarchical model
area: statistics-and-inference/bayesian-statistics
level: core
summary: A model whose group parameters share a prior with its own hyperparameters, so groups borrow strength from each other and estimates shrink toward the common mean.
prereqs: [bayesian-inference, conjugate-prior, de-finetti-theorem, gibbs-sampling]
see_also: [empirical-bayes, james-stein-estimator, linear-mixed-model, hamiltonian-monte-carlo, bayesian-linear-regression, horseshoe-prior, posterior-predictive-check, improper-prior]
sources:
  - book: isbn:9781439840955
    title: "Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, 3rd edition, CRC Press, 2013"
    locator: Chapter 5 (hierarchical models, the normal model with exchangeable parameters, the eight schools example and priors for the group-level variance)
  - paper: doi:10.1111/j.2517-6161.1972.tb00885.x
    title: "D. V. Lindley and A. F. M. Smith, Bayes estimates for the linear model, Journal of the Royal Statistical Society B 34(1), 1972"
    locator: pages 1 to 41, with discussion (normal priors in stages and exchangeability of the group parameters; general locator)
  - paper: "Donald B. Rubin, Estimation in parallel randomized experiments, Journal of Educational Statistics 6(4), 1981"
    title: Rubin 1981
    locator: pages 377 to 401 (the eight coaching experiments; general locator)
  - paper: doi:10.1214/06-BA117A
    title: "Andrew Gelman, Prior distributions for variance parameters in hierarchical models, Bayesian Analysis 1(3), 2006"
    locator: the improper posterior under the prior 1/tau, the problems of the inverse gamma prior with small parameters, and the half-Cauchy prior (general locator)
  - paper: "Omiros Papaspiliopoulos, Gareth O. Roberts and Martin Sköld, A general framework for the parametrization of hierarchical models, Statistical Science 22(1), 2007"
    title: Papaspiliopoulos, Roberts and Sköld 2007
    locator: centred and non-centred parametrizations and their effect on Gibbs samplers (general locator)
---

A hierarchical Bayesian model has parameters in levels. Each group $j$ of data has its own parameter $\theta_j$; the $\theta_j$ are drawn from a common distribution with a hyperparameter $\phi$; and $\phi$ has a prior of its own. Because the groups share $\phi$, the data of every group inform the estimate of every other group, and each estimate is pulled toward the common center by an amount that the data decide. This partial pooling lies between fitting each group alone and treating all groups as one.

## The machine

There are $J$ groups with data $y_1, \ldots, y_J$. The model has three levels:

$$y_j \mid \theta_j \sim f(y_j \mid \theta_j) \ \text{independently}, \qquad \theta_j \mid \phi \sim g(\theta_j \mid \phi) \ \text{i.i.d.}, \qquad \phi \sim p(\phi).$$

The joint density is $p(\phi)\prod_j g(\theta_j \mid \phi)\, f(y_j \mid \theta_j)$, and the posterior $p(\theta, \phi \mid y)$ is proportional to it. More levels (students in classes in schools) and covariates at any level (a regression for the mean of $g$) fit the same pattern.

**Why this prior.** Before the data, the groups are exchangeable: nothing tells them apart, so the joint prior of $(\theta_1, \ldots, \theta_J)$ is symmetric. By [de Finetti's theorem](/de-finetti-theorem/), an exchangeable sequence that can be extended without limit is a mixture of i.i.d. sequences, and the mixing variable is $\phi$. So the second level is not an extra assumption, only a choice of form for the mixture.

**The normal model.** The main example, used below, is

$$y_j \mid \theta_j \sim N(\theta_j, \sigma_j^2) \ (\sigma_j \text{ known}), \qquad \theta_j \mid \mu, \tau \sim N(\mu, \tau^2), \qquad p(\mu, \tau) \propto p(\tau).$$

Here $y_j$ is the estimate from group $j$ and $\sigma_j$ its standard error, as in a random effects meta-analysis.

**Conditions.** The model needs exchangeability of the groups given the covariates that are in the model, and a posterior that is proper. If the hyperprior is improper, propriety must be checked; the last known result below shows that the common prior $p(\tau) \propto 1/\tau$ fails.

## What it counts

- **The group parameters.** The posterior of each $\theta_j$, its mean, its credible interval and the posterior probability that one group is ahead of another.
- **The population.** The posterior of $\phi$, for example the center $\mu$ and the spread $\tau$ of the group effects.
- **A new group.** The predictive law of $\theta_{J+1}$ and of its data, $\int g(\theta_{J+1} \mid \phi)\, p(\phi \mid y)\, d\phi$, which a model without the second level cannot give.
- **Model checks and comparisons.** [Posterior predictive checks](/posterior-predictive-check/) at either level, and the [marginal likelihood](/marginal-likelihood/) $\int p(\phi)\prod_j \int f(y_j \mid \theta_j) g(\theta_j \mid \phi)\, d\theta_j\, d\phi$.

With conjugate choices at each level, [Gibbs sampling](/gibbs-sampling/) draws each block from its full conditional in closed form. In general, [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/) is used, usually in the non-centred form below.

## Relation to other models

- **Complete pooling and no pooling.** In the normal model, $\tau = 0$ forces all $\theta_j = \mu$, one parameter for all groups. $\tau \to \infty$ makes the groups unrelated, and each $\theta_j$ is estimated by $y_j$ alone. The hierarchical model estimates $\tau$ and so chooses between the two from the data.
- **[Empirical Bayes](/empirical-bayes/).** Fixes $\phi$ at an estimate $\hat\phi$, usually by maximizing the marginal likelihood, and then uses $p(\theta \mid y, \hat\phi)$. The full model integrates over $\phi$ instead. The answers agree when $J$ is large; with few groups the plug-in hides the uncertainty in $\phi$, and the eight schools below are a case where $\hat\tau = 0$.
- **[James-Stein estimator](/james-stein-estimator/).** For equal $\sigma_j$ and $\mu = 0$, the posterior mean with $\tau^2$ estimated from the data is a James-Stein type estimator, and its frequentist risk results apply to the shrinkage that this model does.
- **[Linear mixed model](/linear-mixed-model/).** The same structure with the group effects as random effects and a regression at the first level. The frequentist analysis estimates the variance components by REML and predicts the effects; the Bayesian analysis puts a prior on them.
- **[Bayesian linear regression](/bayesian-linear-regression/).** Lindley and Smith (1972) wrote the normal linear model with normal priors in stages, which is a hierarchical model with a linear second level.
- **Shrinkage priors.** A [horseshoe prior](/horseshoe-prior/) is a hierarchical model with one local scale per coefficient and a global scale; there the aim is sparsity rather than pooling.

## Known results in the model

All results are for the normal model with a flat prior on $\mu$, unless stated.

**1. The group parameters given the hyperparameters.** Given $\mu$ and $\tau > 0$, the $\theta_j$ are independent with

$$\theta_j \mid \mu, \tau, y \sim N\Big(\frac{y_j/\sigma_j^2 + \mu/\tau^2}{1/\sigma_j^2 + 1/\tau^2},\ \frac{1}{1/\sigma_j^2 + 1/\tau^2}\Big).$$

*Proof.* The full conditional of $\theta_j$ is proportional to $\exp\big(-(y_j - \theta_j)^2/(2\sigma_j^2) - (\theta_j - \mu)^2/(2\tau^2)\big)$, a normal density whose precision is the sum of the two precisions and whose mean is the precision-weighted average. $\square$

The posterior mean is $\mu + (1 - B_j)(y_j - \mu)$ with the shrinkage factor $B_j = \sigma_j^2/(\sigma_j^2 + \tau^2)$, so it lies between $\mu$ and $y_j$, and a group with a larger standard error is pulled further toward $\mu$.

**2. The center given the spread.** Integrating out the $\theta_j$ gives $y_j \mid \mu, \tau \sim N(\mu, \sigma_j^2 + \tau^2)$ independently, so with $w_j = 1/(\sigma_j^2 + \tau^2)$,

$$\mu \mid \tau, y \sim N(\hat\mu, V_\mu), \qquad \hat\mu = \frac{\sum_j w_j y_j}{\sum_j w_j}, \qquad V_\mu = \frac{1}{\sum_j w_j}.$$

*Proof.* The log density in $\mu$ is $-\tfrac12\sum_j w_j (y_j - \mu)^2$, a quadratic with minimum at $\hat\mu$ and curvature $\sum_j w_j$. $\square$

**3. The marginal posterior of the spread.** With $\hat\mu$ and $V_\mu$ as functions of $\tau$,

$$p(\tau \mid y) \propto p(\tau)\, V_\mu^{1/2} \prod_{j=1}^J (\sigma_j^2 + \tau^2)^{-1/2} \exp\Big(-\frac{(y_j - \hat\mu)^2}{2(\sigma_j^2 + \tau^2)}\Big).$$

*Proof.* $p(\tau \mid y) \propto p(\tau)\int \prod_j N(y_j; \mu, \sigma_j^2 + \tau^2)\, d\mu$. Write $\sum_j w_j (y_j - \mu)^2 = \sum_j w_j (y_j - \hat\mu)^2 + (\mu - \hat\mu)^2/V_\mu$; the Gaussian integral over $\mu$ gives $\sqrt{2\pi V_\mu}$. $\square$

So the posterior can be computed by a one-dimensional grid over $\tau$, then draws of $\mu$ from result 2 and of $\theta$ from result 1, with no Markov chain.

**4. Propriety.** As $\tau \to \infty$, $V_\mu^{1/2} \sim \tau/\sqrt J$, the product is $\sim \tau^{-J}$, and the exponential factor goes to 1, so the likelihood factor of result 3 decays like $\tau^{1 - J}$. At $\tau = 0$ it is finite and positive. Hence:

- a uniform prior on $\tau$ gives a proper posterior if and only if $J \ge 3$;
- the prior $p(\tau) \propto 1/\tau$, or a uniform prior on $\log\tau$, gives an improper posterior for every data set, because $\int_0 d\tau/\tau$ diverges at 0.

For the eight schools ($J = 8$) the log of the likelihood factor has slope $-7.00$ in $\log\tau$ between $\tau = 1000$ and $10000$, as the formula says. Gelman (2006) made this point and recommended a half-Cauchy prior on $\tau$ as a default.

**5. The eight schools.** Rubin (1981) analysed coaching effects on a test in eight schools. The estimates are $y = (28, 8, -3, 7, -1, 1, 18, 12)$ with standard errors $\sigma = (15, 10, 16, 11, 9, 11, 10, 18)$. Results 1 and 2 give, for fixed $\tau$:

| $\tau$ | $\hat\mu$ | $\sqrt{V_\mu}$ | posterior means of $\theta_1, \ldots, \theta_8$ given $\tau$ |
|---|---|---|---|
| 0 | 7.69 | 4.07 | all 7.7 (complete pooling) |
| 5 | 7.85 | 4.49 | 9.9, 7.9, 6.9, 7.7, 5.8, 6.7, 9.9, 8.1 |
| 10 | 8.13 | 5.52 | 14.2, 8.1, 5.0, 7.6, 3.1, 4.9, 13.1, 9.0 |
| 25 | 8.55 | 9.89 | 22.9, 8.1, 0.4, 7.3, 0.1, 2.2, 16.7, 10.8 |
| 100 | 8.73 | 35.65 | 27.6, 8.0, -2.7, 7.0, -0.9, 1.1, 17.9, 11.9 |

With a uniform prior on $\tau$ (on $[0, 200]$, which holds all but a negligible part of the mass), result 3 on a grid of step $0.01$ gives $\mathbb{E}[\tau \mid y] = 6.57$, posterior median $5.24$ and 95% quantile $17.17$. Averaging over $\tau$ gives $\mathbb{E}[\mu \mid y] = 7.93$ and

$$\mathbb{E}[\theta \mid y] = (11.40, 7.89, 6.13, 7.64, 5.13, 6.14, 10.67, 8.46).$$

School A's raw $28$ shrinks to $11.4$, because its standard error is large and the other schools suggest that effects that large are rare. The maximum of the marginal likelihood is at $\tau = 0$, so [empirical Bayes](/empirical-bayes/) would pool completely; the full posterior keeps a real chance that $\tau$ is 10 or more.

**6. Centred and non-centred forms.** In the centred form above, when $\tau$ is small the $\theta_j$ must all be close to $\mu$, and when $\tau$ is large they are free. The posterior of $(\theta, \log\tau)$ then has the shape of a funnel, with a narrow neck that Gibbs samplers and [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/) explore poorly. The non-centred form writes $\theta_j = \mu + \tau\eta_j$ with $\eta_j \sim N(0, 1)$ a priori, which removes the prior dependence between $\eta$ and $\tau$. Papaspiliopoulos, Roberts and Sköld (2007) show that the centred form mixes better when the data are informative about each $\theta_j$ (small $\sigma_j$ relative to $\tau$), and the non-centred form when they are not, as in the eight schools.

## References
