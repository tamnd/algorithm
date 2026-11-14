---
tag: KGGNNK
kind: definition
slug: reference-prior
name: Reference prior
aliases:
- Bernardo reference prior
area: statistics-and-inference/bayesian-statistics
level: advanced
summary: Bernardo's prior that maximizes the expected Kullback-Leibler distance from prior to posterior, so the data dominate. In one dimension it is the Jeffreys prior.
prereqs: [jeffreys-prior, kullback-leibler-divergence, shannon-entropy]
see_also: [improper-prior, channel-capacity, fisher-information-matrix, credible-interval, bernstein-von-mises-theorem, minimum-description-length]
sources:
  - paper: doi:10.1111/j.2517-6161.1979.tb01066.x
    title: "José M. Bernardo, Reference posterior distributions for Bayesian inference, Journal of the Royal Statistical Society B 41(2), 1979"
    locator: pages 113 to 147, with discussion (the definition through expected information, and the treatment of nuisance parameters)
  - paper: doi:10.1214/07-AOS587
    title: "James O. Berger, José M. Bernardo and Dongchu Sun, The formal definition of reference priors, Annals of Statistics 37(2), 2009"
    locator: pages 905 to 938 (permissible priors, the maximizing missing information property, and the explicit form for one continuous parameter)
  - paper: "James O. Berger and José M. Bernardo, On the development of reference priors, in Bayesian Statistics 4 (J. M. Bernardo, J. O. Berger, A. P. Dawid and A. F. M. Smith, eds.), Oxford University Press, 1992"
    locator: pages 35 to 60, with discussion (the one-at-a-time reference prior for an ordered list of parameters)
  - paper: doi:10.1016/0378-3758(94)90153-8
    title: "Bertrand S. Clarke and Andrew R. Barron, Jeffreys' prior is asymptotically least favorable under entropy risk, Journal of Statistical Planning and Inference 41(1), 1994"
    locator: pages 37 to 60 (the asymptotic expansion of the mutual information and the proof that the Jeffreys prior attains its maximum)
  - paper: doi:10.1016/S0169-7161(05)25002-2
    title: "José M. Bernardo, Reference analysis, in Handbook of Statistics 25 (D. K. Dey and C. R. Rao, eds.), Elsevier, 2005"
    locator: pages 17 to 90 (a survey with the formulas for nuisance parameters and many worked models)
---

A reference prior is the prior that leaves the most room for the data: among all priors, it maximizes the information that many replications of the experiment are expected to give about the parameter. José Bernardo defined it in 1979, using the expected [Kullback-Leibler divergence](/kullback-leibler-divergence/) from prior to posterior, which is the mutual information between parameter and data. For one regular continuous parameter the reference prior is the [Jeffreys prior](/jeffreys-prior/), and for a finite parameter space it is the uniform prior. With nuisance parameters it is built one parameter at a time, starting from the parameter of interest, and the result depends on that ordering.

## Definition

Let $X$ have density $f(x \mid \theta)$, $\theta \in \Theta$, and let $X^{(k)} = (X_1, \ldots, X_k)$ be $k$ independent replications. For a proper prior $p$ with posterior $p(\theta \mid x^{(k)})$, the **expected information** from $k$ replications is

$$\mathcal I(p; k) = \int_\Theta p(\theta) \int f(x^{(k)} \mid \theta) \log\frac{p(\theta \mid x^{(k)})}{p(\theta)}\, dx^{(k)}\, d\theta.$$

It is the expected Kullback-Leibler divergence of the posterior from the prior, and it equals the mutual information between $\theta$ and $X^{(k)}$, $H(\theta) - H(\theta \mid X^{(k)})$ in terms of [entropy](/shannon-entropy/) for a discrete $\theta$. The maximum of $\mathcal I(p; k)$ over $p$ is the [capacity](/channel-capacity/) of the channel that sends $\theta$ to $X^{(k)}$.

**The limit in $k$.** For fixed $k$ the maximizing prior is in general discrete and depends on $k$, and $\mathcal I(p; k)$ grows without bound for a continuous $\theta$. So the reference prior is defined through the limit $k \to \infty$, as the prior that maximizes the information still missing about $\theta$ when the experiment can be repeated without end. Berger, Bernardo and Sun (2009) make this precise. A prior $\pi$, which may be improper, is a **reference prior** if:

1. it is **permissible**: for every data set its posterior is proper, and it is the limit of the posteriors from the restrictions of $\pi$ to an increasing sequence of compact sets; and
2. it has the **maximizing missing information** property: for every compact set $\Theta_0$ and every other permissible prior $p$, $\lim_{k \to \infty} \big(\mathcal I(\pi_0; k) - \mathcal I(p_0; k)\big) \ge 0$, where $\pi_0$ and $p_0$ are the restrictions of $\pi$ and $p$ to $\Theta_0$, normalized.

**One continuous parameter.** Let $\theta \in \mathbb{R}$ with an asymptotically normal posterior, $N(\hat\theta, 1/(k I(\theta)))$, where $I$ is the [Fisher information](/fisher-information-matrix/) of one observation. A heuristic computation gives, for large $k$,

$$\mathcal I(p; k) \approx \tfrac12\log\frac{k}{2\pi e} + \int p(\theta)\log\frac{\sqrt{I(\theta)}}{p(\theta)}\, d\theta.$$

Only the second term depends on $p$. With $Z = \int\sqrt{I(\theta)}\, d\theta$ finite, it equals $\log Z - D\big(p \,\|\, \sqrt{I}/Z\big)$, which is largest when $p \propto \sqrt{I(\theta)}$. So the reference prior is the Jeffreys prior. Clarke and Barron (1994) proved the expansion and this conclusion under regularity conditions, and Berger, Bernardo and Sun (2009) prove that the Jeffreys prior is the reference prior under the formal definition.

**A finite parameter space.** If $\Theta$ is finite and the values of $\theta$ give different distributions, the data identify $\theta$ as $k \to \infty$, $H(\theta \mid X^{(k)}) \to 0$ and $\mathcal I(p; k) \to H(p)$. The entropy is largest for the uniform prior, which is the reference prior.

**Nuisance parameters.** Let $\theta = (\psi, \lambda)$ with $\psi$ the parameter of interest. The one-at-a-time method (Berger and Bernardo, 1992) first finds the reference prior $\pi(\lambda \mid \psi)$ for $\lambda$ with $\psi$ held fixed, then the reference prior for $\psi$ in the model with $\lambda$ integrated out, on compact sets and in the limit. For two continuous parameters with Fisher information matrix $I(\psi, \lambda)$ there is a short form (Bernardo, 2005). If

$$\sqrt{I_{\lambda\lambda}(\psi, \lambda)} = a_1(\psi)\, b_1(\lambda), \qquad \sqrt{\frac{\det I(\psi, \lambda)}{I_{\lambda\lambda}(\psi, \lambda)}} = a_0(\psi)\, b_0(\lambda),$$

then the reference prior is $\pi(\psi, \lambda) \propto a_0(\psi)\, b_1(\lambda)$. The second quantity is $1/(I^{-1})_{\psi\psi}$, the information about $\psi$ after the nuisance parameter is accounted for. A different choice of the parameter of interest can give a different prior.

## Examples and non-examples

**Normal mean and scale.** For $N(\mu, \sigma^2)$, $I(\mu, \sigma) = \mathrm{diag}(1/\sigma^2, 2/\sigma^2)$. With $\psi = \mu$: $\sqrt{I_{\sigma\sigma}} = \sqrt2/\sigma$ gives $b_1(\sigma) = 1/\sigma$, and $\sqrt{\det I/I_{\sigma\sigma}} = 1/\sigma$ gives $a_0(\mu) = 1$, so $\pi(\mu, \sigma) \propto 1/\sigma$. With $\psi = \sigma$: $b_1(\mu) = 1$ and $a_0(\sigma) = \sqrt2/\sigma$, so again $\pi \propto 1/\sigma$. The joint Jeffreys prior $1/\sigma^2$ is not a reference prior here. Under $1/\sigma$ the 95% credible interval for $\mu$ has the numbers of the [t interval](/t-confidence-interval/).

**The standardized mean.** Let the parameter of interest be $\phi = \mu/\sigma$, with nuisance $\sigma$. In the parameters $(\phi, \sigma)$, with $\mu = \phi\sigma$, the information matrix is

$$I(\phi, \sigma) = \begin{pmatrix} 1 & \phi/\sigma \\ \phi/\sigma & (2 + \phi^2)/\sigma^2 \end{pmatrix}, \qquad \det I = 2/\sigma^2.$$

Then $\sqrt{I_{\sigma\sigma}} = \sqrt{2 + \phi^2}\cdot(1/\sigma)$, so $b_1(\sigma) = 1/\sigma$, and $\sqrt{\det I/I_{\sigma\sigma}} = \sqrt{2/(2 + \phi^2)}$, so $a_0(\phi) \propto (1 + \phi^2/2)^{-1/2}$. The reference prior is $\pi(\phi, \sigma) \propto (1 + \phi^2/2)^{-1/2}\sigma^{-1}$, which is $\pi(\mu, \sigma) \propto (1 + \mu^2/(2\sigma^2))^{-1/2}\sigma^{-2}$ in the original parameters. The prior $1/\sigma$, the reference prior when $\mu$ is of interest, is the flat density in $(\phi, \sigma)$. The two differ, so the reference prior depends on which parameter is of interest.

**Approaching Jeffreys, measured.** Take $X \mid p \sim$ Bernoulli$(p)$, so $k$ replications give $X^{(k)}$ with a sufficient Binomial$(k, p)$ count, and search for the prior Beta$(a, a)$ with the largest $\mathcal I$. The mutual information was computed exactly as a sum over the $k + 1$ outcomes, with digamma functions for the posterior expectations, and $a$ was searched on a grid of step 0.005 and then 0.0001. The best $a$ is 0.2113 for $k = 10$, 0.3767 for $k = 100$ and 0.4531 for $k = 1000$, moving toward the Jeffreys value $1/2$. At $k = 1000$ the information is 3.19922 nats for the best $a$, 3.19617 for $a = 1/2$ and 3.037 for the uniform prior $a = 1$; the expansion above with $Z = \int_0^1 (p(1 - p))^{-1/2}\, dp = \pi$ gives $\tfrac12\log(1000/(2\pi e)) + \log\pi = 3.180$. This search is within one family of priors; it shows the trend and proves nothing.

**Non-example: the maximizer for a fixed $k$.** For $k = 1$ the information is $\log 2$ minus the expected entropy of a Bernoulli$(p)$ variable when the prior is symmetric, so it is largest, $\log 2 = 0.6931$ nats, for the prior with mass 1/2 at each of $p = 0$ and $p = 1$. That two-point prior is not a reference prior; the limit in $k$ is essential.

**Non-example: a prior chosen for its own entropy.** Maximizing the differential entropy of a prior density on a continuous parameter gives the uniform density, and the answer changes with the parametrization. The reference prior maximizes information about $\theta$ from the data, which is invariant.

## Related definitions

- **[Jeffreys prior](/jeffreys-prior/).** The reference prior for one regular continuous parameter.
- **[Improper prior](/improper-prior/).** Reference priors are often improper; permissibility asks for proper posteriors from limits of compact restrictions.
- **[Channel capacity](/channel-capacity/).** The maximum of $\mathcal I(p; k)$ over priors; the prior that attains it is the capacity-achieving input distribution.
- **Probability matching.** A prior whose one-sided credible bounds have frequentist coverage $1 - \alpha + o(n^{-1/2})$; for one parameter it is the Jeffreys prior, and with nuisance parameters reference priors often match.
- **[Bernstein-von Mises theorem](/bernstein-von-mises-theorem/).** For large $n$ the choice among smooth positive priors matters less; reference priors matter most for small samples and many nuisance parameters.

## References
