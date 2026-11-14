---
tag: 1R00W2
kind: definition
slug: horseshoe-prior
name: Horseshoe prior
aliases:
- horseshoe shrinkage prior
area: statistics-and-inference/bayesian-statistics
level: research
summary: A continuous shrinkage prior that is a normal scale mixture with half-Cauchy local scales. It pulls noise strongly to zero and leaves large signals almost unshrunk.
prereqs: [hierarchical-bayesian-model, spike-and-slab-prior, bayesian-inference]
see_also: [lasso-regression, ridge-regression, empirical-bayes, james-stein-estimator, gibbs-sampling, hamiltonian-monte-carlo, bayesian-linear-regression, bayesian-model-averaging]
sources:
  - paper: doi:10.1093/biomet/asq017
    title: "Carlos M. Carvalho, Nicholas G. Polson and James G. Scott, The horseshoe estimator for sparse signals, Biometrika 97(2), 2010"
    locator: pages 465 to 480; the shrinkage coefficient kappa and its Beta(1/2, 1/2) law, and Theorem 1 (the bounds K/2 log(1 + 4/theta^2) < p(theta) < K log(1 + 2/theta^2) on the marginal density, K = 1/sqrt(2 pi^3))
  - paper: doi:10.1214/17-EJS1337SI
    title: "Juho Piironen and Aki Vehtari, Sparsity information and regularization in the horseshoe and other shrinkage priors, Electronic Journal of Statistics 11(2), 2017"
    locator: the effective number of nonzero coefficients, the reference value tau0 = p0/(D - p0) sigma/sqrt(n) for the global scale, and the regularized horseshoe (general locator)
  - paper: "Nicholas G. Polson and James G. Scott, On the half-Cauchy prior for a global scale parameter, Bayesian Analysis 7(4), 2012"
    title: Polson and Scott 2012
    locator: the half-Cauchy prior for the global scale tau (general locator)
  - paper: "Stéphanie L. van der Pas, Bas J. K. Kleijn and Aad W. van der Vaart, The horseshoe estimator: posterior concentration around nearly black vectors, Electronic Journal of Statistics 8(2), 2014"
    title: van der Pas, Kleijn and van der Vaart 2014
    locator: posterior contraction at the near-minimax rate for a suitable global scale (general locator)
---

The horseshoe prior is a prior for a vector of coefficients that are believed to be mostly zero or near zero, with a few large ones. Each coefficient is normal given its own scale, and the scales have half-Cauchy distributions, so the prior has an infinitely tall peak at zero and heavy tails. In the normal means problem, the amount by which the posterior mean shrinks an observation has a Beta$(1/2, 1/2)$ prior law, whose density looks like a horseshoe: almost all mass is near "shrink completely" or near "do not shrink". It behaves like a [spike-and-slab prior](/spike-and-slab-prior/) in its posterior mean, but it is continuous and has no indicators.

## Definition

Let $\beta_1, \ldots, \beta_p$ be coefficients, for example the means in $y_j \sim N(\beta_j, \sigma^2)$ or the coefficients of a linear regression. The **horseshoe prior** with global scale $\tau > 0$ is

$$\beta_j \mid \lambda_j, \tau \sim N(0, \lambda_j^2 \tau^2), \qquad \lambda_j \sim C^+(0, 1), \qquad \text{independently for } j = 1, \ldots, p,$$

where $C^+(0, 1)$ is the half-Cauchy law with density $\frac{2}{\pi(1 + \lambda^2)}$ on $(0, \infty)$. The $\lambda_j$ are the **local scales**. The global scale $\tau$ is either fixed or given its own prior, usually $\tau \sim C^+(0, \tau_0)$. So the horseshoe is a two-level [hierarchical model](/hierarchical-bayesian-model/) for the scales.

**Shrinkage coefficient.** In the normal means problem $y_j \sim N(\beta_j, \sigma^2)$, given $\lambda_j$ and $\tau$ the prior of $\beta_j$ is normal, so

$$\mathbb{E}[\beta_j \mid y_j, \lambda_j, \tau] = (1 - \kappa_j)\, y_j, \qquad \kappa_j = \frac{1}{1 + \lambda_j^2\tau^2/\sigma^2},$$

and $\mathbb{E}[\beta_j \mid y_j, \tau] = \big(1 - \mathbb{E}[\kappa_j \mid y_j, \tau]\big)\, y_j$. The value $\kappa_j = 1$ means "set to zero" and $\kappa_j = 0$ means "keep $y_j$".

**The horseshoe law of $\kappa$.** If $\tau = \sigma = 1$, then $\kappa = 1/(1 + \lambda^2)$ has the Beta$(1/2, 1/2)$ law, with density and distribution function

$$p(\kappa) = \frac{1}{\pi\sqrt{\kappa(1 - \kappa)}}, \qquad P(\kappa \le t) = \frac{2}{\pi}\arcsin\sqrt t, \qquad 0 < \kappa < 1.$$

*Proof.* The map $\lambda \mapsto \kappa = 1/(1 + \lambda^2)$ is a decreasing bijection from $(0, \infty)$ to $(0, 1)$ with inverse $\lambda = \sqrt{(1 - \kappa)/\kappa}$ and $\lvert d\lambda/d\kappa\rvert = \frac{1}{2}\kappa^{-3/2}(1 - \kappa)^{-1/2}$. Since $1 + \lambda^2 = 1/\kappa$, the change of variables gives

$$p(\kappa) = \frac{2\kappa}{\pi}\cdot\frac{1}{2\kappa^{3/2}(1 - \kappa)^{1/2}} = \frac{1}{\pi\,\kappa^{1/2}(1 - \kappa)^{1/2}},$$

which is the Beta$(1/2, 1/2)$ density because $B(1/2, 1/2) = \pi$. The substitution $\kappa = \sin^2\varphi$ gives the distribution function. $\square$

The density is unbounded at both ends, which gives the name. For a general ratio $a = \tau^2/\sigma^2$ the same change of variables gives

$$p(\kappa) = \frac{\sqrt a}{\pi\sqrt{\kappa(1 - \kappa)}\,\big(1 + (a - 1)\kappa\big)}, \qquad P(\kappa \le \tfrac12) = \frac{2}{\pi}\arctan\sqrt a,$$

so a small $\tau$ moves the mass toward $\kappa = 1$, that is, toward more shrinkage.

**Posterior of $\kappa$.** With $\tau = \sigma = 1$, $y \mid \kappa \sim N(0, 1/\kappa)$, so

$$p(\kappa \mid y) \propto \kappa^{1/2}e^{-\kappa y^2/2}\cdot\kappa^{-1/2}(1 - \kappa)^{-1/2} = (1 - \kappa)^{-1/2}e^{-\kappa y^2/2}.$$

At $y = 0$ this is Beta$(1, 1/2)$, with mean $2/3$. For large $\lvert y\rvert$ the factor $e^{-\kappa y^2/2}$ makes $\kappa$ approximately exponential with mean $2/y^2$, so $\mathbb{E}[\beta \mid y] \approx y - 2/y$: the shrinkage of a large signal goes to 0.

**The marginal density.** The prior density of $\beta$ has no closed form. Carvalho, Polson and Scott (2010, Theorem 1) show that with $\tau = 1$ it is unbounded at 0 and satisfies

$$\frac{K}{2}\log\Big(1 + \frac{4}{\beta^2}\Big) < p(\beta) < K\log\Big(1 + \frac{2}{\beta^2}\Big), \qquad K = \frac{1}{\sqrt{2\pi^3}},$$

so it has a logarithmic pole at 0 and tails like $\beta^{-2}$. This bound is cited, not proved here; a numerical integration agrees with it at $\beta = 0.1, 0.5, 1, 2, 5$, for example $p(1) = 0.1172$ between $0.1022$ and $0.1395$.

## Examples and non-examples

**Example: the normal means rule.** With $\tau = \sigma = 1$, numerical integration of $p(\kappa \mid y)$ gives

| $y$ | 0 | 0.5 | 1 | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|---|---|
| $\mathbb{E}[\kappa \mid y]$ | 0.667 | 0.655 | 0.620 | 0.469 | 0.263 | 0.084 | 0.020 |
| $\mathbb{E}[\beta \mid y]$ | 0 | 0.172 | 0.380 | 1.063 | 2.210 | 4.579 | 9.798 |

At $y = 10$, $\mathbb{E}[\kappa \mid y] = 0.0202$ is close to $2/y^2 = 0.02$. The table on the [spike-and-slab prior](/spike-and-slab-prior/) page puts this rule next to the spike-and-slab and normal rules.

**Example: a Monte Carlo check of the law of $\kappa$.** Draw $\lambda = \lvert\tan(\pi(U - 1/2))\rvert$ with $U$ uniform, which is half-Cauchy, $200000$ times with `random.Random(2024)`, and set $\kappa = 1/(1 + \lambda^2)$. The Kolmogorov-Smirnov distance to $\frac{2}{\pi}\arcsin\sqrt t$ is $0.00228$, so $\sqrt N D = 1.02$, below the 5% critical value $1.36$. This is a check of the proof above, not a replacement for it.

**Example: sparse regression.** For a regression with $D$ coefficients of which about $p_0$ are expected to be nonzero, Piironen and Vehtari (2017) suggest the global scale $\tau_0 = \frac{p_0}{D - p_0}\cdot\frac{\sigma}{\sqrt n}$, so that the prior expected number of effectively nonzero coefficients is about $p_0$.

**Non-example: the Laplace prior.** The Bayesian version of the [lasso](/lasso-regression/) uses $\beta_j \sim$ Laplace, which is a normal scale mixture with exponential mixing on $\lambda_j^2$. Its density is bounded at 0 and its tails are exponential, so it shrinks small values less than the horseshoe and large values by a constant amount that does not vanish.

**Non-example: a normal prior.** A fixed scale, $\lambda_j = 1$, gives the normal prior of [ridge regression](/ridge-regression/), with the same $\kappa$ for every coefficient. There is no adaptation to the size of each signal.

**Non-example: the spike-and-slab prior.** The [spike-and-slab prior](/spike-and-slab-prior/) has a point mass at 0 and gives inclusion probabilities. The horseshoe has neither: every $\beta_j$ is nonzero with probability 1. Values of $1 - \mathbb{E}[\kappa_j \mid y]$ are often used like inclusion probabilities, but they are shrinkage weights.

## Related definitions

- **Global-local shrinkage priors.** The horseshoe is the main example of the family $\beta_j \sim N(0, \lambda_j^2\tau^2)$ with a heavy-tailed law for the local scales $\lambda_j$ and a small global scale $\tau$. The global scale sets the overall level of sparsity; the local scales let single coefficients escape.
- **The global scale.** Polson and Scott (2012) argue for $\tau \sim C^+(0, 1)$, or $C^+(0, \tau_0)$ after scaling. Estimating $\tau$ by maximizing the marginal likelihood is [empirical Bayes](/empirical-bayes/), and the estimate can collapse to 0, which shrinks every coefficient to zero.
- **Regularized horseshoe.** Piironen and Vehtari (2017) replace $\lambda_j^2$ by $\tilde\lambda_j^2 = \frac{c^2\lambda_j^2}{c^2 + \tau^2\lambda_j^2}$. Small coefficients are treated as before, and large ones see a normal slab of width $c$, which helps when the data do not identify the large coefficients well, as in logistic regression with separation.
- **Theory.** Van der Pas, Kleijn and van der Vaart (2014) show that, for a suitable choice of $\tau$ depending on the number of nonzero means, the posterior contracts around a sparse mean vector at the minimax rate up to a constant.
- **Computation.** Given the scales, the model is a [Bayesian linear regression](/bayesian-linear-regression/), so [Gibbs sampling](/gibbs-sampling/) alternates between the coefficients and the scales, often with auxiliary inverse gamma variables for the half-Cauchy laws. [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/) also works, but the funnel shape between $\beta_j$ and $\lambda_j\tau$ needs a non-centred form, $\beta_j = \lambda_j\tau z_j$ with $z_j \sim N(0, 1)$.
- **Relation to James-Stein.** With one common scale and no local scales, the normal means rule shrinks every coordinate by the same factor, as the [James-Stein estimator](/james-stein-estimator/) does; the local scales are what let the horseshoe treat noise and signals differently.

## References
