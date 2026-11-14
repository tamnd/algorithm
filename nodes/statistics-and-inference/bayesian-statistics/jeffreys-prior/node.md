---
tag: 419Q6T
kind: definition
slug: jeffreys-prior
name: Jeffreys prior
aliases:
- Jeffreys' rule
area: statistics-and-inference/bayesian-statistics
level: core
summary: The prior proportional to the square root of the determinant of the Fisher information. It is invariant under reparametrization.
prereqs: [improper-prior, fisher-information-matrix, bayesian-inference]
see_also: [reference-prior, credible-interval, wilson-score-interval, clopper-pearson-interval, kullback-leibler-divergence, likelihood-function, conjugate-prior, bernstein-von-mises-theorem]
sources:
  - paper: doi:10.1098/rspa.1946.0056
    title: "Harold Jeffreys, An invariant form for the prior probability in estimation problems, Proceedings of the Royal Society of London A 186(1007), 1946"
    locator: pages 453 to 461 (the prior proportional to the square root of the determinant of the information, and its invariance)
  - book: isbn:9780198503682
    title: "Harold Jeffreys, Theory of Probability, 3rd edition, Oxford University Press, 1961; Oxford Classic Texts reprint, 1998"
    locator: Chapter 3, Section 3.10 (invariance theory), and Chapter 3 on the priors for location and scale parameters
  - paper: doi:10.1214/ss/1009213286
    title: "Lawrence D. Brown, T. Tony Cai and Anirban DasGupta, Interval estimation for a binomial proportion, Statistical Science 16(2), 2001"
    locator: pages 101 to 133 (the Jeffreys interval for a binomial proportion and its coverage)
  - book: isbn:9780387715988
    title: "Christian P. Robert, The Bayesian Choice, 2nd edition, Springer, 2007"
    locator: Chapter 3 (noninformative priors, the Jeffreys prior and its problems in several dimensions)
---

The Jeffreys prior of a model is the prior density proportional to $\sqrt{\det I(\theta)}$, where $I(\theta)$ is the Fisher information of one observation. Harold Jeffreys proposed it in 1946 as a rule that gives the same answer whatever parametrization is used: compute it for $\theta$ and transform, or compute it for $\eta = h(\theta)$ directly, and the two priors agree. For a binomial proportion it is the proper Beta$(1/2, 1/2)$; for a normal mean it is flat and for a normal scale it is $1/\sigma$, both improper. It depends on the sampling model and not only on the likelihood, and its form for several parameters at once can give poor answers.

## Definition

Let $X$ have density $f(x \mid \theta)$, $\theta$ in an open set $\Theta \subseteq \mathbb{R}^d$, regular enough that the score $s(\theta; x) = \nabla_\theta \log f(x \mid \theta)$ has mean 0 and the [Fisher information](/fisher-information-matrix/) $I(\theta) = E[s(\theta; X)\, s(\theta; X)^\top \mid \theta]$ is finite and positive definite. The **Jeffreys prior** is

$$\pi_J(\theta) \propto \sqrt{\det I(\theta)}.$$

It may be an [improper prior](/improper-prior/), and then it can be used only when the posterior it gives is proper. For $n$ iid observations the information is $I_n(\theta) = n I(\theta)$, which changes $\pi_J$ by the constant $n^{d/2}$ only, so the prior does not depend on $n$.

**Invariance.** Let $\eta = h(\theta)$ with $h$ a smooth bijection, and let $J = \partial\theta/\partial\eta$ be the Jacobian matrix of the inverse map. By the chain rule the score in $\eta$ is $J^\top s(\theta; x)$, so

$$I_\eta(\eta) = J^\top I_\theta(\theta(\eta))\, J, \qquad \sqrt{\det I_\eta(\eta)} = |\det J|\, \sqrt{\det I_\theta(\theta(\eta))}.$$

The factor $|\det J|$ is the change-of-variables factor for a density. So the Jeffreys prior computed in $\eta$ is the law of $h(\theta)$ when $\theta$ has the Jeffreys prior computed in $\theta$, and every posterior statement agrees between the two parametrizations. A uniform prior does not have this property: uniform in $p$ is not uniform in $\log(p/(1 - p))$. In the language of geometry, $\sqrt{\det I(\theta)}$ is the volume element of the Fisher information metric, and the Jeffreys prior is the uniform measure for that volume.

**Standard cases.** For one observation:

| Model | $I(\theta)$ | Jeffreys prior | Proper? |
|---|---|---|---|
| Bernoulli$(p)$ | $1/(p(1 - p))$ | $p^{-1/2}(1 - p)^{-1/2}$, Beta$(1/2, 1/2)$ | yes |
| [Poisson](/poisson-distribution/)$(\lambda)$ | $1/\lambda$ | $\lambda^{-1/2}$ | no |
| $N(\mu, \sigma^2)$, $\sigma$ known | $1/\sigma^2$ | $1$ (flat) | no |
| $N(\mu, \sigma^2)$, $\mu$ known, parameter $\sigma$ | $2/\sigma^2$ | $1/\sigma$ | no |
| Exponential with rate $\lambda$ | $1/\lambda^2$ | $1/\lambda$ | no |
| Failures before the $r$-th success, success probability $p$ | $r/(p^2(1 - p))$ | $p^{-1}(1 - p)^{-1/2}$ | no |
| $N(\mu, \sigma^2)$, both unknown | $\mathrm{diag}(1/\sigma^2, 2/\sigma^2)$ | $1/\sigma^2$ | no |

The binomial with $n$ trials has the same prior as the Bernoulli. The posteriors are Beta$(x + 1/2, n - x + 1/2)$ for the binomial and Gamma with shape $\sum x_i + 1/2$ and rate $n$ for the Poisson; both are always proper.

**Several parameters.** For the normal model with both parameters unknown, the joint rule gives $1/\sigma^2$, and Jeffreys himself did not use it. He took the flat prior for $\mu$ and $1/\sigma$ for $\sigma$ separately, which is the [reference prior](/reference-prior/) for this model. The joint rule loses one degree of freedom: under $1/\sigma^2$ the posterior of $\mu$ is $\bar x + \hat\sigma\, t_n/\sqrt n$, where $\hat\sigma^2 = ((n - 1)/n) s^2$ uses divisor $n$, so its intervals are too short. In models with many parameters the joint rule can be worse, which led to reference priors, where parameters are taken one at a time.

**Not the likelihood alone.** The prior is an expectation over the sample space, so two experiments with proportional likelihoods can have different Jeffreys priors. The Jeffreys prior thus breaks the likelihood principle, the rule that inference should depend on the data only through the [likelihood function](/likelihood-function/).

## Examples and non-examples

**Invariance on the log-odds scale.** For a Bernoulli $p$ and $\eta = \log(p/(1 - p))$, the score in $\eta$ is $x - p$, so $I_\eta = p(1 - p)$ and the Jeffreys prior on $\eta$ is $\sqrt{p(1 - p)}/\pi$ (it is proper, with total mass 1). The law of $\eta$ when $p \sim$ Beta$(1/2, 1/2)$ has density $\frac{1}{\pi}(p(1 - p))^{-1/2} \cdot \frac{dp}{d\eta} = \frac{1}{\pi}(p(1 - p))^{-1/2}\, p(1 - p)$, the same function. At $\eta = -2$, $-0.5$, 0 and 1.3 both give 0.10314, 0.15431, 0.15915 and 0.13058.

**Binomial against negative binomial.** In 10 Bernoulli trials, 3 successes and 7 failures were seen. If $n = 10$ was fixed in advance the model is binomial, the Jeffreys prior is Beta$(1/2, 1/2)$ and the posterior is Beta$(3.5, 7.5)$, with mean 0.3182 and 95% equal-tailed interval $[0.0927, 0.6058]$. If sampling was to stop at the third success, the model counts failures before the third success, the Jeffreys prior is $p^{-1}(1 - p)^{-1/2}$ and the posterior is Beta$(3, 7.5)$, with mean 0.2857 and interval $[0.0706, 0.5773]$. Both likelihoods are proportional to $p^3(1 - p)^7$; the answers differ because the priors do.

**The Jeffreys interval (measured).** The equal-tailed 95% interval of Beta$(x + 1/2, n - x + 1/2)$, with the lower end set to 0 when $x = 0$ and the upper end set to 1 when $x = n$ as Brown, Cai and DasGupta (2001) suggest, is a [credible interval](/credible-interval/). Its exact frequentist coverage, a sum of binomial probabilities, was computed on the grid $p = 0.001, \ldots, 0.999$. For $n = 10$ the mean over the grid is 0.9531 and the lowest value is 0.8683, at $p = 0.218$ and $p = 0.782$; the Wald interval has mean 0.7699. For $n = 30$ the mean is 0.9506 and the lowest 0.8887 (Wald mean 0.8757). For $n = 100$ the mean is 0.9498 and the lowest 0.8806, at $p = 0.025$ (Wald mean 0.9231). The coverage is close to 0.95 on average but not at every $p$; it is not a confidence interval in the strict sense. The [Wilson score interval](/wilson-score-interval/) behaves much the same, and the [Clopper-Pearson interval](/clopper-pearson-interval/) is the one with coverage at least 0.95 at every $p$.

**The joint prior for a normal sample (exact coverage).** For the data 2.1, 3.4, 2.9, 3.8 ($\bar x = 3.05$, $s = 0.73258$), the prior $1/\sigma$ gives the 95% interval $[1.8843, 4.2157]$ for $\mu$, the numbers of the [t interval](/t-confidence-interval/). The joint Jeffreys prior $1/\sigma^2$ gives $3.05 \pm t_{(4, 0.975)}\sqrt{3/4}\, s/2 = [2.1693, 3.9307]$. Its frequentist coverage is $P(|t_{n-1}| \le t_{(n, 0.975)}\sqrt{(n - 1)/n})$, which is 0.7978 for $n = 2$, 0.9045 for $n = 4$, 0.9363 for $n = 10$ and 0.9460 for $n = 30$. For $\sigma^2$ the 95% equal-tailed intervals are $[0.1722, 7.4608]$ under $1/\sigma$ (the chi-square confidence interval with $n - 1 = 3$ degrees of freedom) and $[0.1445, 3.3236]$ under $1/\sigma^2$ (4 degrees of freedom, too short).

**Non-example: the uniform prior on $p$.** Beta$(1, 1)$ is a fine proper prior, but it is not the Jeffreys prior and it is not invariant: on the log-odds scale it becomes the logistic density $p(1 - p)$, not a uniform density.

**Non-example: a model without Fisher information.** For $X \sim$ Uniform$(0, \theta)$ the support depends on $\theta$, the score does not have mean 0, and the formula does not apply. The prior $1/\theta$, often used here, comes from scale invariance, not from Jeffreys' rule.

## Related definitions

- **[Reference prior](/reference-prior/).** Bernardo's prior from an information criterion; it equals the Jeffreys prior for one regular parameter and differs from the joint Jeffreys prior with nuisance parameters.
- **[Improper prior](/improper-prior/).** Most Jeffreys priors for unbounded parameters are improper; the posterior must be checked.
- **[Kullback-Leibler divergence](/kullback-leibler-divergence/).** $I(\theta)$ is the second derivative of $\theta' \mapsto D(f_\theta \,\|\, f_{\theta'})$ at $\theta' = \theta$, which explains why the information gives a parametrization-free volume.
- **[Minimum description length](/minimum-description-length/).** The Jeffreys prior gives the leading terms of the optimal code length for a parametric model.
- **[Bernstein-von Mises theorem](/bernstein-von-mises-theorem/).** In large samples any smooth positive prior, Jeffreys or not, gives the same normal posterior to first order.

## References
