---
tag: B3884J
kind: technique
slug: bayesian-model-averaging
name: Bayesian model averaging
aliases:
- BMA
area: statistics-and-inference/bayesian-statistics
level: advanced
summary: Average predictions or estimates over a set of models, each weighted by its posterior probability, instead of choosing one model.
prereqs: [bayes-factor, marginal-likelihood, posterior-predictive-distribution, bayes-theorem]
see_also: [spike-and-slab-prior, stacking, reversible-jump-mcmc, bayesian-information-criterion, akaike-information-criterion, pareto-smoothed-importance-sampling-loo, kullback-leibler-divergence, bayesian-linear-regression]
sources:
  - paper: doi:10.1214/ss/1009212519
    title: "Jennifer A. Hoeting, David Madigan, Adrian E. Raftery and Chris T. Volinsky, Bayesian model averaging: a tutorial, Statistical Science 14(4), 1999"
    locator: the definition, the computation by Occam's window and MC³, and the predictive performance (general locator)
  - paper: doi:10.2307/1403615
    title: "David Madigan and Jeremy York, Bayesian graphical models for discrete data, International Statistical Review 63(2), 1995"
    locator: the Markov chain Monte Carlo model composition (MC³) sampler on the space of models (general locator)
  - paper: "David Madigan and Adrian E. Raftery, Model selection and accounting for model uncertainty in graphical models using Occam's window, Journal of the American Statistical Association 89(428), 1994"
    title: Madigan and Raftery 1994
    locator: Occam's window and the log score argument for averaging (general locator)
  - paper: "Adrian E. Raftery, David Madigan and Jennifer A. Hoeting, Bayesian model averaging for linear regression models, Journal of the American Statistical Association 92(437), 1997"
    title: Raftery, Madigan and Hoeting 1997
    locator: model averaging over subsets of regressors (general locator)
  - paper: "Feng Liang, Rui Paulo, German Molina, Merlise A. Clyde and James O. Berger, Mixtures of g priors for Bayesian variable selection, Journal of the American Statistical Association 103(481), 2008"
    title: Liang, Paulo, Molina, Clyde and Berger 2008
    locator: closed form marginal likelihoods for regression models under g priors (general locator)
  - paper: "Yuling Yao, Aki Vehtari, Daniel Simpson and Andrew Gelman, Using stacking to average Bayesian predictive distributions, Bayesian Analysis 13(3), 2018"
    title: Yao, Vehtari, Simpson and Gelman 2018
    locator: stacking of predictive distributions and its comparison with model averaging when no model is true (general locator)
  - paper: "Maria M. Barbieri and James O. Berger, Optimal predictive model selection, Annals of Statistics 32(3), 2004"
    title: Barbieri and Berger 2004
    locator: the median probability model (general locator)
  - paper: "James G. Scott and James O. Berger, Bayes and empirical-Bayes multiplicity adjustment in the variable-selection problem, Annals of Statistics 38(5), 2010"
    title: Scott and Berger 2010
    locator: priors on the model size and the multiplicity correction they give (general locator)
---

Bayesian model averaging (BMA) handles uncertainty about the model in the same way that Bayesian inference handles uncertainty about a parameter: it puts a prior on the models, computes their posterior probabilities from the [marginal likelihoods](/marginal-likelihood/), and averages over them. A prediction or an estimate is the average of the answers of the separate models, each weighted by the posterior probability of its model. In contrast to fitting one selected model, the answer keeps the uncertainty about which model is right. When the set of models and the priors are correct, the averaged predictive distribution has the best expected log score of all predictive distributions.

## In plain words

Suppose several models could explain your data, and none is clearly best. If you pick one and report its answer, you act as if you were sure of that model, and your intervals are too narrow. Model averaging asks each model for its answer and mixes the answers. A model that predicted the data well gets a large weight, and a model that predicted them badly gets a small one. The weight also includes how plausible you thought the model was before. The mix is wider than any single answer when the models disagree, which is the honest result.

## When it applies

- **A list of models for the same data.** Models $M_1, \ldots, M_K$, each with a sampling density $f_k(x \mid \theta_k)$ and a proper prior $\pi_k(\theta_k)$, and prior model probabilities $P(M_k)$ that sum to 1.
- **A quantity with the same meaning in every model.** The target $\Delta$ is a future observation, a prediction, or a parameter that every model defines in the same way. A regression coefficient whose meaning depends on the other regressors in the model is not such a quantity.
- **Marginal likelihoods that can be computed.** Exactly with conjugate priors, approximately with a Laplace approximation, the BIC, [bridge sampling](/bridge-sampling/) or [nested sampling](/nested-sampling/), or implicitly with a sampler that moves between models.
- **The true model, or a good approximation to it, is in the list.** This is the M-closed case. If no model in the list is close to the truth, the weights still converge to one model, and [stacking](/stacking/) is a better way to combine predictions.

## The template

The holes are the list of models `M`, the priors `P(M_k)` and `π_k`, the method `ML` that computes or approximates each marginal likelihood, and the quantity `Δ`.

```pseudo id=main
BAYESIAN-MODEL-AVERAGING(x, M₁, ..., M_K, P, π, ML, Δ)
L1  for k ← 1 to K do
L2      ℓ_k ← log P(M_k) + log ML(x; f_k, π_k)         ▷ log m_k(x) = log ∫ f_k(x | θ_k) π_k(θ_k) dθ_k
L3  c ← max_k ℓ_k
L4  for k ← 1 to K do
L5      w_k ← exp(ℓ_k − c) / Σ_j exp(ℓ_j − c)         ▷ P(M_k | x), computed on the log scale
L6  p(Δ | x) ← Σ_k w_k · p(Δ | x, M_k)                 ▷ mixture of the posteriors of Δ under each model
L7  return p(Δ | x), (w₁, ..., w_K)
```

Line L5 is [Bayes's theorem](/bayes-theorem/) on the models, $P(M_k \mid x) \propto P(M_k)\, m_k(x)$, and the ratio of two weights is the prior odds times the [Bayes factor](/bayes-factor/). Line L6 is the law of total probability. From L6, the posterior mean and variance of a real $\Delta$ are

$$\mathbb{E}[\Delta \mid x] = \sum_k w_k\, \hat\Delta_k, \qquad \mathrm{Var}[\Delta \mid x] = \sum_k w_k\, \mathrm{Var}[\Delta \mid x, M_k] + \sum_k w_k\, \big(\hat\Delta_k - \mathbb{E}[\Delta \mid x]\big)^2,$$

with $\hat\Delta_k = \mathbb{E}[\Delta \mid x, M_k]$. The second sum is the part of the uncertainty that comes from not knowing the model; selecting one model sets it to zero.

**Why average: the log score.** Let $p(\Delta \mid x)$ be the averaged predictive distribution of a future observation $\Delta$ from L6. For any other predictive density $q$,

$$\mathbb{E}_{p}\big[\log p(\Delta \mid x)\big] - \mathbb{E}_{p}\big[\log q(\Delta)\big] = \mathrm{KL}\big(p(\cdot \mid x)\, \Vert\, q\big) \ge 0,$$

by Gibbs's inequality: $\mathbb{E}_p[\log(q/p)] \le \log \mathbb{E}_p[q/p] \le \log 1 = 0$ by [Jensen's inequality](/jensens-inequality/), with equality only if $q = p$ almost everywhere. Here $\mathbb{E}_p$ is the expectation under the joint model, that is, with the model, the parameter and $\Delta$ drawn from the prior and the sampling densities given the data $x$. So under its own assumptions, the averaged predictive scores at least as well in expectation as the predictive of any single model, and strictly better unless that model has all the weight. This is Madigan and Raftery's argument. It is a statement about expectations under the prior over models; it does not say that BMA wins when the data come from outside the list.

## Classic examples

**A coin, exact.** Toss a coin $n = 20$ times and see $y = 15$ heads. $M_0: \theta = 1/2$ and $M_1: \theta \sim$ Beta$(1, 1)$, with prior odds 1. The [Bayes factor](/bayes-factor/) is $B_{10} = 65536/20349$, so $w_1 = 65536/85885 \approx 0.7631$. The probability that the next toss is a head is $8/11$ under $M_1$ (Laplace's rule, $(y + 1)/(n + 2)$) and $1/2$ under $M_0$, and the average is

$$w_1 \cdot \tfrac{8}{11} + w_0 \cdot \tfrac12 = \frac{254483}{377894} \approx 0.6734.$$

For $\theta$ itself, the averaged posterior has mean $0.6734$ and variance $0.01592$: $0.00658$ within the models plus $0.00934$ between them. Model $M_1$ alone gives the variance $0.00862$, so selecting $M_1$ almost halves the reported variance. If the next toss is drawn from the averaged predictive, its expected log score is $-0.6317$ for the average, $-0.6388$ for $M_1$ alone and $-0.6931$ for $M_0$ alone, in line with the inequality above.

**Variable selection in linear regression.** With $p$ candidate regressors there are $2^p$ models. Under Zellner's $g$ prior on the coefficients, or a mixture of $g$ priors (Liang et al. 2008), each marginal likelihood is a closed form function of the $R^2$ of the model, so L2 is cheap. Raftery, Madigan and Hoeting (1997) average over the subsets, and the posterior inclusion probability of regressor $j$ is the sum of $w_k$ over the models that contain it. A [spike-and-slab prior](/spike-and-slab-prior/) on the coefficients of one [Bayesian linear regression](/bayesian-linear-regression/) is the same thing written as one model: its posterior is the model average.

**Model composition by Markov chain (MC³).** When $2^p$ is too large to list, Madigan and York (1995) run a [Metropolis-Hastings](/metropolis-hastings/) chain on the models. A proposal adds or removes one regressor or edge, and the move from $M$ to $M'$ is accepted with probability $\min\big(1, P(M')m(M') / (P(M)m(M))\big)$. The visit frequencies estimate the $w_k$. When the marginal likelihoods have no closed form, [reversible jump MCMC](/reversible-jump-mcmc/) moves between models and parameters at once.

**BIC weights.** If each $\log m_k$ is replaced by $-\tfrac12 \mathrm{BIC}_k$, the weights become $w_k \propto P(M_k)\, e^{-\mathrm{BIC}_k/2}$. This is a large-sample approximation to BMA that ignores the priors $\pi_k$. Weights $e^{-\mathrm{AIC}_k/2}$ from the [Akaike information criterion](/akaike-information-criterion/) look similar but aim at the predictive Kullback-Leibler risk, not at posterior model probabilities, and they are not BMA.

## Variations

- **Occam's window.** Madigan and Raftery (1994) drop the models whose posterior probability is below a fraction of the best one, and the models that have a simpler submodel with higher probability. The average is over the much smaller set that remains.
- **Stacking.** [Stacking](/stacking/) chooses the weights that maximize the leave-one-out log score of the mixture, with the leave-one-out densities from [PSIS-LOO](/pareto-smoothed-importance-sampling-loo/). Yao et al. (2018) show that it predicts better than BMA when no model in the list is true. Pseudo-BMA uses weights proportional to $\exp(\widehat{\mathrm{elpd}}_k)$ instead.
- **Median probability model.** If one model must be reported, the model with the regressors whose inclusion probability is at least $1/2$ is optimal for prediction under squared error in some normal linear models (Barbieri and Berger, 2004).
- **Averaging inside one model.** A continuous mixture over a model index, such as a prior on the degree of a polynomial or on the number of components of a mixture, is BMA over an infinite list.

## Pitfalls

- **Prior sensitivity of the weights.** The marginal likelihoods depend on how diffuse the priors $\pi_k$ are, and they do not forget them as $n$ grows. A very wide prior on the extra parameters of a model drives its weight to 0, as the [Lindley paradox](/lindley-paradox/) shows. Improper priors give undefined weights.
- **The model prior is not neutral.** A uniform prior on $2^p$ regression models puts most of its mass on models with about $p/2$ regressors. A prior on the model size, such as a beta-binomial prior, gives a multiplicity correction (Scott and Berger, 2010).
- **Weights collapse.** As $n$ grows, the weights concentrate on one model, even when no model is true. Then BMA is model selection with extra steps, and it does not express that the models are all wrong.
- **Averaging quantities that differ between models.** The coefficient of a regressor in a model with a correlated second regressor is not the same quantity as its coefficient in a model without it. Average predictions, or define $\Delta$ so that it has one meaning.
- **Bad marginal likelihood estimates.** The harmonic mean of the likelihood over posterior draws has infinite variance in common cases. Errors of a few units in $\log m_k$ change the weights by large factors.

## Exercises

1. Prove the variance decomposition after the template from the law of total variance.
2. In the coin example, compute the averaged predictive probability that the next two tosses are both heads, and check that it is not the square of $0.6734$.
3. Show that for two models with prior odds 1, the weight of $M_1$ is $B_{10}/(1 + B_{10})$, and compute it for $B_{10} = 3$, $10$ and $100$.
4. Write the MC³ acceptance probability for a proposal that adds one of the $p - \lvert M\rvert$ absent regressors or removes one of the $\lvert M\rvert$ present ones with probability $1/2$ each, chosen uniformly. Show that the proposal is not symmetric in general and correct the acceptance probability.
5. Let the data come from $N(\mu, 4)$ while $M_0: x \sim N(0, 1)$ and $M_1: x \sim N(\mu, 1)$ with $\mu \sim N(0, 1)$. Argue that the weight of $M_1$ goes to 1 when $\mu \ne 0$, and explain why the averaged predictive is still too narrow.

## References
