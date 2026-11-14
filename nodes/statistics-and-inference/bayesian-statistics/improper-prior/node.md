---
tag: 9EF9PG
kind: definition
slug: improper-prior
name: Improper prior
aliases:
- flat prior
area: statistics-and-inference/bayesian-statistics
level: core
summary: A prior measure with infinite total mass, such as a uniform prior on the real line. It is usable when the posterior it gives is proper.
prereqs: [bayesian-inference, bayes-theorem, probability-density-function]
see_also: [jeffreys-prior, reference-prior, bayes-estimator, admissible-estimator, bayes-factor, lindley-paradox, gibbs-sampling, hierarchical-bayesian-model]
sources:
  - paper: "James P. Hobert and George Casella, The effect of improper priors on Gibbs sampling in hierarchical linear mixed models, Journal of the American Statistical Association 91(436), 1996"
    locator: pages 1461 to 1473 (conditions for a proper posterior in hierarchical linear mixed models, and Gibbs samplers whose conditionals are proper while the joint posterior is not)
  - book: isbn:9780387715988
    title: "Christian P. Robert, The Bayesian Choice, 2nd edition, Springer, 2007"
    locator: Chapter 1 (improper prior distributions) and Chapter 3 (noninformative priors)
  - book: isbn:9781439840955
    title: "Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, 3rd edition, CRC Press, 2013"
    locator: Chapter 2 (noninformative and improper priors, and the need to check that the posterior is proper) and Chapter 5 (hierarchical models and the prior for the group-level variance)
---

An improper prior is a measure on the parameter space with infinite total mass, used in [Bayes' theorem](/bayes-theorem/) in the place of a prior density. Standard cases are the flat density on the real line for a location parameter and the density $1/\sigma$ for a scale parameter. The product of likelihood and prior can still have a finite integral, and then the normalized product is a proper posterior that can be used like any other. Whether it is proper depends on the model and often on the data, so it must be checked; an improper prior also gives no joint law of parameter and data, so marginal likelihoods and Bayes factors are not defined.

## Definition

Let the data $x$ have density $f(x \mid \theta)$, $\theta \in \Theta$. An **improper prior** is a $\sigma$-finite measure on $\Theta$ with infinite total mass; on $\Theta \subseteq \mathbb{R}^d$ it is given by a density $\pi(\theta) \ge 0$ with $\int_\Theta \pi(\theta)\, d\theta = \infty$.

- The **formal marginal** is $m(x) = \int_\Theta f(x \mid \theta)\, \pi(\theta)\, d\theta$.
- If $0 < m(x) < \infty$, the **formal posterior** $\pi(\theta \mid x) = f(x \mid \theta)\pi(\theta)/m(x)$ is a probability density, and the posterior is called **proper**. If $m(x) = \infty$, there is no posterior.
- An improper prior is defined only up to a positive constant $c$. The posterior does not depend on $c$; the formal marginal $m(x)$ does.

A prior is improper because of its total mass, not because it is flat: the uniform density on $[0, 1]$ is a proper prior, and $1/\sigma$ on $(0, \infty)$ is improper without being flat. A noninformative prior can be proper, such as the [Jeffreys prior](/jeffreys-prior/) Beta$(1/2, 1/2)$ for a binomial proportion.

**Why use one.** Improper priors appear in three ways.

1. As limits of proper priors. The posterior for a normal mean under the prior $N(0, \tau^2)$ tends to the posterior under the flat prior as $\tau \to \infty$.
2. From invariance. The flat prior on a location and $1/\sigma$ on a scale are the priors left unchanged by shifts and by changes of units; the [Jeffreys prior](/jeffreys-prior/) and the [reference prior](/reference-prior/) are often improper.
3. To give estimators with good frequentist risk. The minimizer of posterior expected loss under an improper prior is a generalized [Bayes estimator](/bayes-estimator/); many [admissible estimators](/admissible-estimator/) are of this form, and some generalized Bayes estimators are not admissible, such as the sample mean of a normal vector in three or more dimensions.

**What breaks.** Under an improper prior $(\theta, X)$ has no joint probability law and $m$ is not a probability density, since $\int m(x)\, dx = \int \pi(\theta)\, d\theta = \infty$. Three consequences follow.

- **Propriety must be checked.** For each model, find the data sets with $m(x) < \infty$. The check is analytic: bound the integral of $f(x \mid \theta)\pi(\theta)$ near every place where $\pi$ or $f$ is large, such as the ends of $\Theta$ and points where a variance is 0.
- **A sampler does not check it.** The full conditional laws used by [Gibbs sampling](/gibbs-sampling/) can all be proper while the joint posterior is not. The chain then runs and gives numbers that approximate nothing (Hobert and Casella, 1996).
- **Bayes factors are undefined.** The [Bayes factor](/bayes-factor/) $m_1(x)/m_0(x)$ changes by the factor $c$ when the improper prior $\pi_1$ of model 1 is replaced by $c\,\pi_1$, so its value is arbitrary. The constant cancels only for a parameter that both models share with the same prior. A very diffuse proper prior in its place gives a Bayes factor that depends on the prior scale; that is the [Lindley paradox](/lindley-paradox/).

## Examples and non-examples

**A normal mean, flat prior.** Let $X_1, \ldots, X_n \mid \mu$ be iid $N(\mu, \sigma^2)$ with $\sigma$ known and $\pi(\mu) = 1$ on $\mathbb{R}$. Then $m(x)$ is finite for $n \ge 1$ and the posterior is $N(\bar x, \sigma^2/n)$. Its 95% credible interval has the numbers of the z confidence interval.

**A normal mean and scale, prior $1/\sigma$.** Let $\pi(\mu, \sigma) = 1/\sigma$ on $\mathbb{R} \times (0, \infty)$. For $n \ge 2$ observations that are not all equal the posterior is proper, and $\mu \mid x$ is distributed as $\bar x + (s/\sqrt n)\, t_{n-1}$, with $s^2$ the sample variance with divisor $n - 1$. For the data 2.1, 3.4, 2.9, 3.8 ($\bar x = 3.05$, $s = 0.73258$, $t_{(3, 0.975)} = 3.18245$) the 95% credible interval for $\mu$ is $[1.8843, 4.2157]$, the same numbers as the [t confidence interval](/t-confidence-interval/). For $n = 1$ the posterior is improper: integrating over $\mu$ first gives $\int_0^\infty \sigma^{-1}\, d\sigma = \infty$.

**The Haldane prior.** For $X \mid p \sim$ Binomial$(n, p)$ take $\pi(p) = p^{-1}(1 - p)^{-1}$ on $(0, 1)$, the formal Beta$(0, 0)$. The formal posterior is Beta$(x, n - x)$, which is proper only when $0 < x < n$. For $x = 0$, $m(0) = \int_0^1 p^{-1}(1 - p)^{n-1}\, dp = \infty$. A data set with no successes, the case where a prior matters most, gives no posterior at all.

**A variance component with prior $1/\tau^2$.** Let $X_i \mid \theta_i \sim N(\theta_i, 1)$ and $\theta_i \mid \tau^2 \sim N(0, \tau^2)$ for $i = 1, \ldots, k$, with $\pi(\tau^2) = 1/\tau^2$. Integrating out the $\theta_i$ gives $X_i \mid \tau^2$ iid $N(0, 1 + \tau^2)$, whose likelihood $L(\tau^2)$ tends to the positive value $\prod_i \varphi(x_i)$ as $\tau^2 \to 0$, where $\varphi$ is the standard normal density. So $\int_0^1 L(\tau^2)\, \tau^{-2}\, d\tau^2 = \infty$, and the posterior is improper for every data set. Yet both full conditionals are proper: $\theta_i \mid \tau^2, x \sim N\big(x_i\tau^2/(1 + \tau^2), \tau^2/(1 + \tau^2)\big)$, and $\tau^2 \mid \theta$ is inverse gamma with shape $k/2$ and scale $\sum_i \theta_i^2/2$.

**What the Gibbs sampler does (measured).** Take $k = 8$ and start the chain at $\tau^2 = 1$. For data drawn with seed 7 and $\theta_i \sim N(0, 1)$ ($\sum x_i^2 = 11.86$), $\tau^2$ fell below $10^{-6}$ at iteration 237 and was $2.9 \times 10^{-32}$ at iteration 2000: the chain fell into the infinite mass at 0. For data drawn with $\theta_i \sim N(0, 3^2)$ and seeds 1, 2 and 3 ($\sum x_i^2 = 93.28$, 93.59 and 63.15), 200000 iterations never went below 0.33, and the medians of the first 10000 draws were 11.5, 11.38 and 7.38. Those chains look healthy, but there is no posterior for them to approximate.

**Non-example: the uniform prior on $[0, 1]$.** It is flat and proper. The "flat prior" alias of this page refers to flat densities on unbounded sets.

**Non-example: a vague proper prior.** $N(0, 10^6)$ for a mean is proper, so the posterior always exists. When the data are informative its posterior is close to the flat-prior one, but its marginal likelihood, and so any Bayes factor that uses it, depends on the value $10^6$.

## Related definitions

- **[Jeffreys prior](/jeffreys-prior/).** The prior proportional to $\sqrt{\det I(\theta)}$; improper for location and scale families, proper for a binomial proportion.
- **[Reference prior](/reference-prior/).** Bernardo's prior that lets the data dominate; often improper, and defined as a limit of proper priors on compact sets.
- **Generalized Bayes estimator.** The minimizer of posterior expected loss under an improper prior with a proper posterior; see [Bayes estimator](/bayes-estimator/).
- **[Marginal likelihood](/marginal-likelihood/).** Defined only up to the arbitrary constant of an improper prior, so it cannot compare models.
- **[Hierarchical Bayesian model](/hierarchical-bayesian-model/).** The setting where improper priors on variance components most often give improper posteriors; proper priors such as a half-Cauchy on the standard deviation avoid the problem.

## References
