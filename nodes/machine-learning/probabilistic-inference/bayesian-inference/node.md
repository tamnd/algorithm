---
tag: CSGT71
kind: concept
slug: bayesian-inference
name: Bayesian inference
aliases:
- Bayesian updating
- Bayesian parameter estimation
area: machine-learning/probabilistic-inference
level: intro
summary: "Treat unknown parameters as random. Combine a prior with the likelihood of the data by Bayes' theorem to get a posterior, and predict by averaging over it."
history:
  year: 1763
  people: [Thomas Bayes, Pierre-Simon Laplace]
  note: Bayes found the posterior of a binomial success probability under a uniform prior. Laplace used the same method for many problems from 1774 on.
prereqs: [bayes-theorem, probability-distribution]
see_also: [conjugate-prior, marginal-likelihood, maximum-a-posteriori-estimation, maximum-likelihood-estimation, metropolis-hastings, variational-inference, gaussian-process, bayesian-network]
sources:
  - book: isbn:9781439840955
    title: "Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, 3rd edition, CRC Press, 2013"
    locator: Chapter 1 (posterior and posterior predictive), Chapter 2 (the binomial model and posterior intervals) and Chapter 4 (normal approximation and large-sample theory)
  - book: isbn:9780521784504
    title: "A. W. van der Vaart, Asymptotic Statistics, Cambridge University Press, 1998"
    locator: Chapter 10, Bayes Procedures (the Bernstein-von Mises theorem)
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: Section 2.1.1 (the beta prior and sequential updating) and Section 3.3 (Bayesian linear regression and the predictive distribution)
  - book: isbn:9780471494645
    title: "José M. Bernardo and Adrian F. M. Smith, Bayesian Theory, Wiley, 1994"
    locator: Chapter 4 (exchangeability and the de Finetti representation theorem)
---

Bayesian inference treats an unknown quantity $\theta$, such as the parameters of a model, as a random variable. It starts from a prior distribution $p(\theta)$, multiplies by the likelihood $p(D \mid \theta)$ of the observed data $D$, and normalizes by [Bayes' theorem](/bayes-theorem/) to get the posterior $p(\theta \mid D)$. Every answer then comes from the posterior: point estimates, intervals, and predictions for new data, which average over $\theta$ in place of plugging in one value. This page covers the parametric case with data that are independent given $\theta$; the same rule applied to the hidden variables of a [graphical model](/graphical-model/) is [marginal inference](/marginal-inference/).

## In plain words

You start with a belief about an unknown number, written as a spread of weights over its possible values. You then look at data. Each possible value gets a score: how well it explains the data. You multiply each weight by its score and rescale so that the weights add up to one. The new spread is your updated belief. To predict the next observation, you ask each possible value for its prediction and average the answers with the new weights. If more data arrive, the updated belief is the starting belief for the next step, and the end result does not depend on the order in which the data came.

## The idea

**Notation.** $\theta \in \Theta$ is the parameter, $D = (x_1, \ldots, x_n)$ are the $n$ observations, and $p$ denotes a density or a mass function. The data model is: given $\theta$, the $x_i$ are independent with density $p(x \mid \theta)$.

**Posterior.** With prior $p(\theta)$ and likelihood $p(D \mid \theta) = \prod_{i=1}^n p(x_i \mid \theta)$,

$$
p(\theta \mid D) = \frac{p(D \mid \theta)\,p(\theta)}{p(D)}, \qquad p(D) = \int_\Theta p(D \mid \theta)\,p(\theta)\,d\theta.
$$

The normalizer $p(D)$ is the [marginal likelihood](/marginal-likelihood/). It does not depend on $\theta$, so for the shape of the posterior one writes $p(\theta \mid D) \propto p(D \mid \theta)\,p(\theta)$.

**Posterior predictive.** For a new observation $\tilde x$ that is independent of $D$ given $\theta$,

$$
p(\tilde x \mid D) = \int_\Theta p(\tilde x \mid \theta)\,p(\theta \mid D)\,d\theta = \frac{p(D, \tilde x)}{p(D)}.
$$

This average is wider than the plug-in prediction $p(\tilde x \mid \hat\theta)$ for one estimate $\hat\theta$, because it carries the uncertainty about $\theta$.

**Sequential updating equals batch updating.** Let $D_k = (x_1, \ldots, x_k)$. Because the $x_i$ are independent given $\theta$,

$$
p(\theta \mid D_k) \propto p(x_k \mid \theta)\,p(\theta \mid D_{k-1}).
$$

*Proof.* $p(\theta \mid D_k) \propto p(\theta)\prod_{i \le k} p(x_i \mid \theta) = p(x_k \mid \theta)\,\bigl[p(\theta)\prod_{i < k} p(x_i \mid \theta)\bigr] \propto p(x_k \mid \theta)\,p(\theta \mid D_{k-1})$. The constants of proportionality do not depend on $\theta$, and both sides integrate to 1, so they are equal. $\blacksquare$

By induction, updating one observation at a time, with each posterior as the next prior, gives the batch posterior. The likelihood is a product, so the result does not depend on the order of the data. Data whose joint law does not change under a permutation are *exchangeable*. De Finetti's theorem says that an infinite exchangeable sequence of 0/1 variables is a mixture of i.i.d. Bernoulli sequences, that is, conditionally i.i.d. given some $\theta$ with some prior. So for such data the model above is not an extra assumption.

**Decisions from the posterior.** Under squared loss the best point estimate is the posterior mean; under absolute loss it is a posterior median. The posterior mode is the [MAP estimate](/maximum-a-posteriori-estimation/); it is not the Bayes estimate for any fixed loss on a continuous parameter, and it depends on the parameterization.

**Credible and confidence intervals.** A 95% *credible* set $C(D)$ has $\Pr(\theta \in C(D) \mid D) = 0.95$: a probability over $\theta$, for the data at hand. A 95% *confidence* set has $\Pr_\theta(\theta \in C(D)) \ge 0.95$ for every $\theta$: a probability over repeated data, for a fixed $\theta$. The two are different statements, and one can hold without the other (see the example below).

**Large samples: the Bernstein-von Mises theorem.** Let $x_1, x_2, \ldots$ be i.i.d. from $p(\cdot \mid \theta_0)$ with $\theta_0$ an interior point of $\Theta \subseteq \mathbb{R}^k$. Assume that the model is differentiable in quadratic mean at $\theta_0$ with nonsingular Fisher information $I(\theta_0)$, that for each $\varepsilon > 0$ there are tests of $\theta = \theta_0$ against $\lVert \theta - \theta_0 \rVert \ge \varepsilon$ whose errors go to 0, and that the prior has a density that is continuous and positive near $\theta_0$. Then

$$
\Bigl\lVert\, p(\theta \mid x_1, \ldots, x_n) - \mathcal{N}\bigl(\hat\theta_n,\ (n I(\theta_0))^{-1}\bigr) \Bigr\rVert_{\mathrm{TV}} \to 0
$$

in probability, where $\hat\theta_n$ is an efficient estimator such as the [maximum likelihood estimate](/maximum-likelihood-estimation/) (van der Vaart 1998, Chapter 10). So in a regular model with a fixed number of parameters the prior washes out, and a 95% credible interval is also an approximate 95% confidence interval. The theorem says nothing at a fixed $n$, and it can fail when the number of parameters grows with $n$, when $\theta_0$ is on the boundary, or when the model is not identifiable.

**Computing the posterior.** With a [conjugate prior](/conjugate-prior/) the posterior has a closed form. In low dimension a grid or [numerical integration](/numerical-integration/) works. Otherwise one uses the Laplace approximation (see [marginal likelihood](/marginal-likelihood/)), Markov chain Monte Carlo on a [Markov chain](/markov-chain/) whose [stationary distribution](/stationary-distribution/) is the posterior, such as [Metropolis-Hastings](/metropolis-hastings/), [Gibbs sampling](/gibbs-sampling/) or [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/), [importance sampling](/importance-sampling/), or [variational inference](/variational-inference/).

## Examples

**Beta-binomial, step by step.** A coin has unknown heads probability $\theta$. The prior is $\mathrm{Beta}(2, 2)$, with density proportional to $\theta(1-\theta)$. The data are $1, 1, 0, 1, 1, 0, 1, 1$: six heads and two tails. The likelihood of $s$ heads and $f$ tails is $\theta^s(1-\theta)^f$, so the posterior is $\mathrm{Beta}(2 + s, 2 + f)$. The predictive probability of heads under $\mathrm{Beta}(a, b)$ is its mean $a/(a+b)$.

| after | $x$ | posterior | $\Pr(\text{next} = 1 \mid D)$ |
|---|---|---|---|
| prior | | Beta(2, 2) | 1/2 |
| 1 | 1 | Beta(3, 2) | 3/5 |
| 2 | 1 | Beta(4, 2) | 2/3 |
| 3 | 0 | Beta(4, 3) | 4/7 |
| 4 | 1 | Beta(5, 3) | 5/8 |
| 5 | 1 | Beta(6, 3) | 2/3 |
| 6 | 0 | Beta(6, 4) | 3/5 |
| 7 | 1 | Beta(7, 4) | 7/11 |
| 8 | 1 | Beta(8, 4) | 2/3 |

The batch update gives $\mathrm{Beta}(8, 4)$ at once, and so does every one of the 28 distinct orders of the same data. The maximum likelihood estimate is $6/8 = 3/4$; the posterior mean $2/3$ is pulled toward the prior mean $1/2$. The equal-tailed 95% credible interval of $\mathrm{Beta}(8, 4)$ is about $[0.390, 0.891]$.

**A confidence interval that is not a credible interval.** Let $x_1, x_2$ be i.i.d. uniform on $(\theta - \tfrac12, \theta + \tfrac12)$, and let $C = [\min x_i, \max x_i]$. It covers $\theta$ exactly when one point falls on each side of $\theta$, which has probability $1/2$ for every $\theta$; so $C$ is a 50% confidence interval. But if the range $r = \max x_i - \min x_i$ is at least $1/2$, the two points cannot both be on one side, so $\theta \in C$ for certain. Under a flat prior the posterior is uniform on $(\max x_i - \tfrac12, \min x_i + \tfrac12)$, and the posterior probability of $C$ is $r/(1-r)$ for $r < 1/2$ and 1 for $r \ge 1/2$. The 50% is a long-run average over data sets, not a statement about the data at hand.

**Gaussian mean.** With $x_i \sim \mathcal{N}(\theta, \sigma^2)$, $\sigma^2$ known, and prior $\mathcal{N}(\mu_0, \tau_0^2)$, the posterior is normal with precision $1/\tau_0^2 + n/\sigma^2$ and mean the precision-weighted average of $\mu_0$ and $\bar x$. The details are on the [conjugate prior](/conjugate-prior/) page. In a linear model the same computation gives Bayesian linear regression, whose posterior mean is the [ridge regression](/ridge-regression/) estimate.

## Where it is used

- [Naive Bayes](/naive-bayes-classifier/) with add-one smoothing uses the posterior predictive of a Dirichlet prior.
- [Gaussian processes](/gaussian-process/) put a prior on functions and predict with the posterior predictive.
- [Latent Dirichlet allocation](/latent-dirichlet-allocation/) and other latent variable models need approximate posteriors, by [Gibbs sampling](/gibbs-sampling/) or [variational inference](/variational-inference/).
- [Thompson sampling](/thompson-sampling/) for bandits draws a parameter from the posterior and acts as if it were true.
- Model choice compares [marginal likelihoods](/marginal-likelihood/) through Bayes factors.
- [Filtering](/filtering/) in a [state space model](/state-space-model/) is sequential Bayesian updating of a hidden state; the [Kalman filter](/kalman-filter/) and the [particle filter](/particle-filter/) are two ways to do it.
- [Bayesian phylogenetic inference](/bayesian-phylogenetic-inference/) samples trees from their posterior.

## References
