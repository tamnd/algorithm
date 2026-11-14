---
tag: R7P8PD
kind: definition
slug: spike-and-slab-prior
name: Spike-and-slab prior
aliases:
- spike and slab variable selection
area: statistics-and-inference/bayesian-statistics
level: advanced
summary: A prior that gives each coefficient a probability of being exactly zero (the spike) and otherwise spreads it out (the slab). The posterior gives each variable a probability of inclusion.
prereqs: [bayesian-linear-regression, bayes-factor, bayesian-inference]
see_also: [bayesian-model-averaging, horseshoe-prior, lasso-regression, ridge-regression, gibbs-sampling, local-false-discovery-rate, savage-dickey-density-ratio, empirical-bayes]
sources:
  - paper: "Toby J. Mitchell and John J. Beauchamp, Bayesian variable selection in linear regression, Journal of the American Statistical Association 83(404), 1988"
    title: Mitchell and Beauchamp 1988
    locator: the prior with a point mass at zero and a flat slab, and the name spike and slab (general locator)
  - paper: "Edward I. George and Robert E. McCulloch, Variable selection via Gibbs sampling, Journal of the American Statistical Association 88(423), 1993"
    title: George and McCulloch 1993
    locator: stochastic search variable selection with a narrow normal spike and a wide normal slab, sampled by Gibbs sampling (general locator)
  - paper: "Hemant Ishwaran and J. Sunil Rao, Spike and slab variable selection: frequentist and Bayesian strategies, Annals of Statistics 33(2), 2005"
    title: Ishwaran and Rao 2005
    locator: rescaled spike and slab models and their selective shrinkage (general locator)
  - paper: "James G. Scott and James O. Berger, Bayes and empirical-Bayes multiplicity adjustment in the variable-selection problem, Annals of Statistics 38(5), 2010"
    title: Scott and Berger 2010
    locator: a prior on the inclusion probability and the multiplicity correction it gives, compared with empirical Bayes (general locator)
  - paper: "Maria M. Barbieri and James O. Berger, Optimal predictive model selection, Annals of Statistics 32(3), 2004"
    title: Barbieri and Berger 2004
    locator: the median probability model (general locator)
  - paper: "Veronika Ročková and Edward I. George, The spike-and-slab LASSO, Journal of the American Statistical Association 113(521), 2018"
    title: Ročková and George 2018
    locator: Laplace spike and slab densities and the fast posterior mode (general locator)
---

A spike-and-slab prior is a prior for variable selection. Each coefficient $\beta_j$ is either zero, with some prior probability, or drawn from a wide distribution, the slab. The point mass at zero is the spike. The posterior then gives each variable a posterior inclusion probability, and it is the same as [Bayesian model averaging](/bayesian-model-averaging/) over all subsets of the variables, written as one model.

## Definition

Let $\beta = (\beta_1, \ldots, \beta_p)$ be the coefficients of a model, for example a [Bayesian linear regression](/bayesian-linear-regression/) $y \sim N(X\beta, \sigma^2 I)$. Introduce indicators $\gamma_j \in \{0, 1\}$. The **spike-and-slab prior** with inclusion probability $w \in (0, 1)$ and slab density $h$ is

$$\gamma_j \sim \text{Bernoulli}(w), \qquad \beta_j \mid \gamma_j \sim (1 - \gamma_j)\, \delta_0 + \gamma_j\, h, \qquad \text{independently for } j = 1, \ldots, p.$$

Here $\delta_0$ is the point mass at 0. A common slab is $h = N(0, s^2)$, or $N(0, s^2\sigma^2)$ when $\sigma$ is unknown. Mitchell and Beauchamp (1988) used a flat slab on a bounded interval.

The **continuous form** of George and McCulloch (1993) replaces the point mass by a narrow normal, $\beta_j \mid \gamma_j \sim (1 - \gamma_j) N(0, v_0) + \gamma_j N(0, v_1)$ with $v_0 \ll v_1$. Then no coefficient is exactly zero, but the Gibbs updates are simple.

The **posterior inclusion probability** of variable $j$ is $\mathrm{PIP}_j = P(\gamma_j = 1 \mid y)$. The vector $\gamma$ names a model (the set of included variables), and $P(\gamma \mid y) \propto P(\gamma)\, m(y \mid \gamma)$ is its posterior probability, with $m(y \mid \gamma)$ the [marginal likelihood](/marginal-likelihood/) of the regression on the included columns.

**The normal means case, exact.** Let $y \sim N(\beta, 1)$ for one coefficient, with slab $N(0, s^2)$. The marginal law of $y$ is $N(0, 1)$ under the spike and $N(0, 1 + s^2)$ under the slab, so

$$\mathrm{PIP}(y) = \frac{w\, N(y; 0, 1 + s^2)}{w\, N(y; 0, 1 + s^2) + (1 - w)\, N(y; 0, 1)}, \qquad \mathbb{E}[\beta \mid y] = \mathrm{PIP}(y)\cdot \frac{s^2}{1 + s^2}\, y.$$

*Proof.* The first formula is [Bayes's theorem](/bayes-theorem/) for $\gamma$, with the two marginal laws as likelihoods. Given $\gamma = 1$, the normal prior and likelihood give $\beta \mid y, \gamma = 1 \sim N\big(\tfrac{s^2}{1 + s^2}y, \tfrac{s^2}{1 + s^2}\big)$; given $\gamma = 0$, $\beta = 0$. Average the two conditional means with weights $\mathrm{PIP}$ and $1 - \mathrm{PIP}$. $\square$

The posterior odds of inclusion are the prior odds $w/(1 - w)$ times the [Bayes factor](/bayes-factor/) $N(y; 0, 1 + s^2)/N(y; 0, 1)$ of the slab against the spike. With $w = 1/2$, $\mathrm{PIP} = 1/2$ exactly when $y^2 = \frac{1 + s^2}{s^2}\log(1 + s^2)$.

## Examples and non-examples

**Example: selective shrinkage.** With $w = 1/2$ and $s^2 = 10$ in the normal means case, $\mathrm{PIP} = 1/2$ at $\lvert y\rvert = \sqrt{1.1\ln 11} = 1.624$, and:

| $y$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $\mathrm{PIP}$ | 0.232 | 0.322 | 0.650 | 0.947 | 0.998 | 1.000 |
| $\mathbb{E}[\beta \mid y]$, spike and slab | 0 | 0.293 | 1.182 | 2.584 | 3.628 | 4.545 |
| $\mathbb{E}[\beta \mid y]$, horseshoe ($\tau = 1$) | 0 | 0.380 | 1.063 | 2.210 | 3.448 | 4.579 |
| $\mathbb{E}[\beta \mid y]$, prior $N(0, 10)$ | 0 | 0.909 | 1.818 | 2.727 | 3.636 | 4.545 |

Small observations are pulled hard toward 0 and large ones are left almost alone, at the factor $10/11$ of the slab. A single normal prior cannot do both: it shrinks every $y$ by the same factor. The [horseshoe prior](/horseshoe-prior/) does a similar thing with a continuous prior. The posterior mean is never exactly 0 for $y \ne 0$; the posterior median is 0 whenever $\mathrm{PIP} < 1/2$, so the median is a thresholding rule.

**Example: the two-groups model.** In large-scale testing, each $z$-value is null with probability $\pi_0$ and has a slab density otherwise. This is a spike-and-slab prior on the effects, and $1 - \mathrm{PIP}$ is the [local false discovery rate](/local-false-discovery-rate/).

**Example: regression.** For $p$ regressors, the posterior over $\gamma$ is a posterior over the $2^p$ subsets, and the posterior mean of $\beta$ is the model average of the subset estimates. The median probability model keeps the variables with $\mathrm{PIP}_j \ge 1/2$; Barbieri and Berger (2004) show that it is the best single model for prediction in some normal linear models.

**Non-example: the Laplace prior.** The [lasso](/lasso-regression/) estimate is the posterior mode under independent Laplace priors, and it has exact zeros. But the Laplace prior has no point mass, so every coefficient has posterior probability 0 of being 0, and its posterior mean is never sparse. The sparsity of the lasso is a property of the mode, not of the prior.

**Non-example: a normal prior.** [Ridge regression](/ridge-regression/) is the posterior mean under $\beta_j \sim N(0, s^2)$, the slab alone. It shrinks all coefficients by the same factor in the orthogonal case and selects nothing.

**Non-example: the horseshoe.** The [horseshoe prior](/horseshoe-prior/) is a continuous scale mixture of normals with a pole at 0. It mimics the spike and slab in its posterior mean, but it has no indicator and no inclusion probability.

## Related definitions

- **[Bayesian model averaging](/bayesian-model-averaging/).** The spike-and-slab posterior is BMA over subsets with the prior $P(\gamma) = w^{\lvert\gamma\rvert}(1 - w)^{p - \lvert\gamma\rvert}$.
- **The prior on $w$ and multiplicity.** With $w$ fixed, adding more noise variables does not make the prior more cautious. A prior $w \sim$ Beta$(a, b)$ makes the model size beta-binomial, and Scott and Berger (2010) show that this gives an automatic multiplicity correction. Estimating $w$ by maximizing the marginal likelihood is [empirical Bayes](/empirical-bayes/) and behaves similarly for large $p$, but it can collapse to $\hat w = 0$.
- **Slab width and the Lindley paradox.** As $s^2 \to \infty$ the Bayes factor for the slab goes to 0, and every PIP goes to 0. At $y = 2.5$ with $w = 1/2$, $\mathrm{PIP}$ is $0.838$, $0.687$, $0.185$ and $0.022$ for $s^2 = 10$, $10^2$, $10^4$ and $10^6$. This is the [Lindley paradox](/lindley-paradox/) for one coefficient, so the slab must be proper and of a sensible width.
- **[Savage-Dickey density ratio](/savage-dickey-density-ratio/).** The Bayes factor of the spike against the slab for one coefficient is the posterior density of $\beta_j$ at 0 under the slab alone, divided by the slab density at 0, when the other coefficients have the same prior in both models.
- **Computation.** With the point mass, a [Gibbs sampler](/gibbs-sampling/) must update $\gamma_j$ with $\beta_j$ integrated out, because given $\beta_j \ne 0$ the indicator cannot change. With conjugate normal slabs, $m(y \mid \gamma)$ has a closed form and the sampler can work on $\gamma$ alone. The continuous form of George and McCulloch updates $\gamma_j$ given $\beta_j$ directly.
- **Spike-and-slab lasso.** Ročková and George (2018) use a narrow Laplace spike and a wide Laplace slab, so that the posterior mode is sparse and can be found quickly, as for the lasso.
- **Rescaled spike and slab.** Ishwaran and Rao (2005) study continuous spike and slab priors with a hypervariance and their frequentist behaviour.

## References
