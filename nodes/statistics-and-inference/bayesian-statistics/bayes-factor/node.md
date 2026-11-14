---
tag: T4B5GB
kind: definition
slug: bayes-factor
name: Bayes factor
aliases:
- Bayes factor test
area: statistics-and-inference/bayesian-statistics
level: core
summary: The ratio of the marginal likelihoods of the data under two models. It turns prior odds into posterior odds and does not depend on the prior probabilities of the models.
prereqs: [marginal-likelihood, bayes-theorem, bayesian-inference, likelihood-function]
see_also: [savage-dickey-density-ratio, lindley-paradox, bayesian-model-averaging, bayesian-information-criterion, e-variable, likelihood-ratio-test, bridge-sampling, nested-sampling]
sources:
  - paper: doi:10.1080/01621459.1995.10476572
    title: "Robert E. Kass and Adrian E. Raftery, Bayes factors, Journal of the American Statistical Association 90(430), 1995"
    locator: pages 773 to 795 (the definition, the scale for interpretation, the Schwarz approximation, and the methods to compute marginal likelihoods; general locator)
  - book: isbn:9780198503682
    title: "Harold Jeffreys, Theory of Probability, 3rd edition (1961), reprinted in Oxford Classic Texts in the Physical Sciences, Oxford University Press, 1998"
    locator: Chapter 5 (significance tests with one new parameter) and Appendix B (the grades of the Bayes factor K)
  - paper: doi:10.1214/09-STS284
    title: "Christian P. Robert, Nicolas Chopin and Judith Rousseau, Harold Jeffreys's Theory of Probability revisited, Statistical Science 24(2), 2009"
    locator: pages 141 to 172 (Jeffreys's tests, Appendix B and its grades of K; general locator)
  - paper: "James O. Berger and Luis R. Pericchi, The intrinsic Bayes factor for model selection and prediction, Journal of the American Statistical Association 91(433), 1996"
    title: Berger and Pericchi 1996
    locator: the intrinsic Bayes factor built from minimal training samples (general locator)
  - paper: "Anthony O'Hagan, Fractional Bayes factors for model comparison, Journal of the Royal Statistical Society, Series B 57(1), 1995"
    title: O'Hagan 1995
    locator: the fractional Bayes factor that uses a fraction b of the likelihood to train an improper prior (general locator)
  - book: isbn:9780387715988
    title: "Christian P. Robert, The Bayesian Choice, 2nd edition, Springer, 2007"
    locator: Chapter 5 (tests and confidence regions, Bayes factors, and the conflict with p-values) and Chapter 7 (model choice)
---

A Bayes factor compares two statistical models $M_0$ and $M_1$ by how well each one predicted the observed data $x$, with its parameters averaged over its prior. It is the ratio $B_{10}(x) = m_1(x)/m_0(x)$ of the two [marginal likelihoods](/marginal-likelihood/). By [Bayes's theorem](/bayes-theorem/), it is the factor that converts the prior odds of $M_1$ against $M_0$ into the posterior odds, so it does not depend on the prior probabilities of the two models. Jeffreys introduced it to test scientific hypotheses, and it is the Bayesian counterpart of the likelihood ratio.

## Definition

Let $x$ be the data. For $k = 0, 1$, model $M_k$ has a parameter $\theta_k \in \Theta_k$, a sampling density $f_k(x \mid \theta_k)$ and a proper prior density $\pi_k(\theta_k)$. The **marginal likelihood** of $M_k$ is

$$m_k(x) = \int_{\Theta_k} f_k(x \mid \theta_k)\, \pi_k(\theta_k)\, d\theta_k.$$

If $0 < m_0(x) < \infty$ and $m_1(x) < \infty$, the **Bayes factor** of $M_1$ against $M_0$ is

$$B_{10}(x) = \frac{m_1(x)}{m_0(x)}, \qquad B_{01}(x) = \frac{1}{B_{10}(x)}.$$

If $M_k$ is a simple hypothesis $\theta = \theta_k$, then $m_k(x) = f(x \mid \theta_k)$, and for two simple hypotheses $B_{10}$ is the likelihood ratio of the [Neyman-Pearson lemma](/neyman-pearson-lemma/).

**Odds form.** For prior model probabilities $P(M_0), P(M_1) > 0$,

$$\frac{P(M_1 \mid x)}{P(M_0 \mid x)} = B_{10}(x)\, \frac{P(M_1)}{P(M_0)}, \qquad P(M_1 \mid x) = \frac{B_{10}(x)\, P(M_1)}{B_{10}(x)\, P(M_1) + P(M_0)}.$$

*Proof.* $P(M_k \mid x) = P(M_k)\, m_k(x)/m(x)$ with $m(x) = P(M_0)m_0(x) + P(M_1)m_1(x)$. Divide the case $k = 1$ by the case $k = 0$. $\square$

**Three facts that follow from the definition.**

- *Chaining.* For three models, $B_{20} = B_{21} B_{10}$, so Bayes factors order any set of models consistently.
- *Null expectation 1.* If $M_0$ is simple, then $\mathbb{E}_0[B_{10}(X)] = \int m_1(x)\, dx = 1$, because $m_1$ is a probability density. By Markov's inequality $P_0(B_{10} \ge k) \le 1/k$. So $B_{10}$ is an [e-variable](/e-variable/) for a simple null. For a composite null this fails in general.
- *Bounded by the maximized ratio.* $m_1(x) \le \sup_{\theta_1} f_1(x \mid \theta_1)$, so if $M_0$ is simple, $B_{10}(x)$ is at most the maximized likelihood ratio, for every prior $\pi_1$.

**Reading the size.** Jeffreys (Appendix B) graded $K = B_{01}$ in steps of half a unit of $\log_{10}$. Against $M_0$: $1$ to $10^{1/2} \approx 3.2$ is "not worth more than a bare mention", $3.2$ to $10$ substantial, $10$ to $31.6$ strong, $31.6$ to $100$ very strong, and above $100$ decisive. Kass and Raftery (1995) give a coarser scale, quoted on the [marginal likelihood](/marginal-likelihood/) page. These words are conventions, not error rates.

**What a Bayes factor is not.** It is a ratio of predictive probabilities, not a test with a level. The rule "reject $M_0$ when $B_{10} > k$" is a test, and its type I error is at most $1/k$ for a simple null by the fact above, but the number $B_{10}$ itself has no level and no type II error. It is also not a p-value and not the posterior probability of $M_0$; the posterior probability needs the prior odds as well.

## Examples and non-examples

**Example: a coin, exact.** Toss a coin $n = 20$ times and see $y = 15$ heads. Let $M_0: \theta = 1/2$ and $M_1: \theta \sim$ Beta$(1, 1)$, the uniform prior. Then

$$m_0 = \binom{20}{15}2^{-20} = \frac{15504}{1048576} = \frac{969}{65536}, \qquad m_1 = \binom{20}{15}\int_0^1 \theta^{15}(1 - \theta)^5\, d\theta = \binom{20}{15}\frac{15!\, 5!}{21!} = \frac{1}{21}.$$

So $B_{10} = 65536/20349 \approx 3.221$, and $B_{01} = 20349/65536 \approx 0.3105$. With prior odds $1$, $P(M_1 \mid y) = 65536/85885 \approx 0.763$. On Jeffreys's grades it is just past $10^{1/2} \approx 3.16$, at the bottom of the substantial grade. The exact fractions agree with a direct sum of the binomial terms over a fine grid of $\theta$.

**Example: the prior matters.** With $M_1: \theta \sim$ Beta$(a, a)$ and the same data:

| $a$ | 0.01 | 0.1 | 0.5 | 1 | 2 | 5 | 10 | 100 | 1000 |
|---|---|---|---|---|---|---|---|---|---|
| $B_{10}$ | 0.089 | 0.768 | 2.405 | 3.221 | 3.666 | 3.298 | 2.569 | 1.198 | 1.020 |

A very diffuse prior ($a \to 0$ puts the mass near $0$ and $1$) wastes prior mass on values that the data rule out, and $B_{10}$ goes to $0$: the data then favour $M_0$. A very concentrated prior ($a \to \infty$) makes $M_1$ the same as $M_0$, and $B_{10} \to 1$. Unlike the posterior of $\theta$, the Bayes factor does not forget the prior as $n$ grows. The limit of this effect is the [Lindley paradox](/lindley-paradox/).

**Example: two simple hypotheses.** For $x \sim N(\theta, 1)$, $M_0: \theta = 0$ and $M_1: \theta = 1$, $B_{10}(x) = e^{x - 1/2}$. At $x = 2$ it is $e^{1.5} \approx 4.48$.

**Non-example: the p-value.** For the coin, the two-sided binomial p-value is $P_{1/2}(\lvert Y - 10 \rvert \ge 5) = 0.0414$. It is computed under $M_0$ alone, it is not $B_{01} = 0.31$, and it is not $P(M_0 \mid y) = 0.237$. See [p-value](/p-value/).

**Non-example: the maximized likelihood ratio.** $\sup_\theta f(y \mid \theta)/f(y \mid 1/2) = (0.75^{15}\, 0.25^{5})/0.5^{20} \approx 13.68$ is the statistic of the [likelihood ratio test](/likelihood-ratio-test/). It uses the best $\theta$ for the data, not an average over the prior, and it is an upper bound for $B_{10}$ over every prior on $M_1$.

**Non-example: a ratio with an improper prior.** If $\pi_1$ is improper, $c\,\pi_1$ is the same prior for every $c > 0$, but it multiplies $m_1$ and the "Bayes factor" by $c$. The ratio is not defined; see [improper prior](/improper-prior/). Only parameters that both models share, with the same improper prior, are safe.

**Non-example: posterior odds.** $P(M_1 \mid x)/P(M_0 \mid x)$ equals $B_{10}$ only when the prior odds are $1$.

## Related definitions

- **[Marginal likelihood](/marginal-likelihood/).** The numerator and the denominator. Most of the work in practice is computing it.
- **[Savage-Dickey density ratio](/savage-dickey-density-ratio/).** A formula, not a new quantity: when $M_0$ fixes $\phi = \phi_0$ inside $M_1$ and the priors are compatible, $B_{01}$ equals the posterior density of $\phi$ at $\phi_0$ divided by its prior density there.
- **[Lindley paradox](/lindley-paradox/).** A theorem about the behaviour of $B_{01}$ for a point null as $n$ grows with the z-statistic fixed, or as the prior spreads. It explains why $B_{01}$ and a p-value can disagree.
- **[Bridge sampling](/bridge-sampling/) and [nested sampling](/nested-sampling/).** Monte Carlo methods that estimate $m_k(x)$ or the ratio $m_1/m_0$; they compute the Bayes factor and do not change its definition.
- **[Bayesian information criterion](/bayesian-information-criterion/).** $-\tfrac12\mathrm{BIC}_k$ approximates $\log m_k(x)$ with an error of order $1$, so $\tfrac12(\mathrm{BIC}_0 - \mathrm{BIC}_1)$ is a rough approximation to $\log B_{10}$ that does not depend on the prior.
- **Intrinsic and fractional Bayes factors.** To use default improper priors, Berger and Pericchi (1996) train them into proper priors on minimal subsets of the data and average over the subsets. O'Hagan (1995) uses a fraction $b$ of the likelihood for the same purpose. Both are approximations to some Bayes factor, not Bayes factors of the original priors.
- **Posterior model probabilities.** With more than two models, $P(M_k \mid x) \propto P(M_k)\, m_k(x)$. [Bayesian model averaging](/bayesian-model-averaging/) uses them as weights.
- **[Likelihood ratio test](/likelihood-ratio-test/).** The frequentist relative: it maximizes over the parameters where the Bayes factor integrates, and it is calibrated by its distribution under $M_0$.
- **Predictive criteria.** [PSIS-LOO](/pareto-smoothed-importance-sampling-loo/) and [WAIC](/widely-applicable-information-criterion/) score prediction of each point from the posterior. The Bayes factor scores prediction of all the data from the prior. The two can disagree, and only the Bayes factor depends on how diffuse the prior is.

## References
