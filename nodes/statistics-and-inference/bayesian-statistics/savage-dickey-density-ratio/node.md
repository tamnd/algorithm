---
tag: WCSA76
kind: theorem
slug: savage-dickey-density-ratio
name: Savage-Dickey density ratio
aliases:
- Savage-Dickey ratio
area: statistics-and-inference/bayesian-statistics
level: advanced
summary: For nested models with compatible priors, the Bayes factor for a point null equals the posterior density at the null value divided by the prior density there.
prereqs: [bayes-factor, marginal-likelihood, bayes-theorem, conditional-probability]
see_also: [lindley-paradox, bridge-sampling, nested-sampling, gibbs-sampling, kernel-density-estimation, bayesian-linear-regression, spike-and-slab-prior, improper-prior]
sources:
  - paper: doi:10.1214/aoms/1177693507
    title: "James M. Dickey, The weighted likelihood ratio, linear hypotheses on normal location parameters, Annals of Mathematical Statistics 42(1), 1971"
    locator: the density ratio form of the weighted likelihood ratio, credited to L. J. Savage (general locator)
  - paper: "Isabella Verdinelli and Larry Wasserman, Computing Bayes factors using a generalization of the Savage-Dickey density ratio, Journal of the American Statistical Association 90(430), 1995"
    title: Verdinelli and Wasserman 1995
    locator: pages 614 to 618 (the correction factor when the priors are not compatible; general locator)
  - paper: doi:10.1214/10-EJS564
    title: "Jean-Michel Marin and Christian P. Robert, On resolving the Savage-Dickey paradox, Electronic Journal of Statistics 4, 2010"
    locator: pages 643 to 654 (the dependence on the version of the densities and how to fix it; general locator)
  - paper: doi:10.1080/01621459.1995.10476572
    title: "Robert E. Kass and Adrian E. Raftery, Bayes factors, Journal of the American Statistical Association 90(430), 1995"
    locator: the section on computing marginal likelihoods (general locator)
---

The Savage-Dickey density ratio is a formula for the [Bayes factor](/bayes-factor/) of a nested point null. If the null model $M_0$ fixes a parameter $\phi$ at $\phi_0$ inside a larger model $M_1$, and the priors of the two models agree on the other parameters, then $B_{01}$ equals the posterior density of $\phi$ at $\phi_0$ under $M_1$ divided by the prior density of $\phi$ at $\phi_0$. So a Bayes factor can be read from the posterior of the larger model alone, without computing any [marginal likelihood](/marginal-likelihood/).

## Statement

Model $M_1$ has parameters $(\phi, \psi)$, a sampling density $f(x \mid \phi, \psi)$ and a proper prior density $\pi_1(\phi, \psi)$. Model $M_0$ is the same model with $\phi = \phi_0$: its sampling density is $f(x \mid \phi_0, \psi)$ and its prior density on $\psi$ is $\pi_0(\psi)$. Write

$$\pi_1(\phi) = \int \pi_1(\phi, \psi)\, d\psi, \qquad \pi_1(\psi \mid \phi_0) = \frac{\pi_1(\phi_0, \psi)}{\pi_1(\phi_0)}, \qquad \pi_1(\phi \mid x) = \frac{\int f(x \mid \phi, \psi)\pi_1(\phi, \psi)\, d\psi}{m_1(x)}.$$

These three formulas fix the versions of the densities at the single point $\phi_0$; see the remark at the end of the proof.

**Theorem (Savage-Dickey).** Assume $0 < \pi_1(\phi_0) < \infty$, $0 < m_0(x)$, $m_1(x) < \infty$, and the compatibility condition

$$\pi_0(\psi) = \pi_1(\psi \mid \phi_0) \quad \text{for almost every } \psi.$$

Then

$$B_{01}(x) = \frac{m_0(x)}{m_1(x)} = \frac{\pi_1(\phi_0 \mid x)}{\pi_1(\phi_0)}.$$

If there is no nuisance parameter $\psi$, the condition is empty and the identity always holds. If $\phi$ and $\psi$ are independent under $\pi_1$, the condition says that $M_0$ uses the same prior on $\psi$ as $M_1$.

**Theorem (Verdinelli and Wasserman).** Drop the compatibility condition, and assume that $\pi_0(\psi) > 0$ implies $\pi_1(\psi \mid \phi_0) > 0$. Then

$$B_{01}(x) = \frac{\pi_1(\phi_0 \mid x)}{\pi_1(\phi_0)} \cdot \mathbb{E}\Big[\frac{\pi_0(\psi)}{\pi_1(\psi \mid \phi_0)}\Big],$$

where the expectation is over $\psi \sim \pi_1(\psi \mid \phi_0, x) \propto f(x \mid \phi_0, \psi)\, \pi_1(\psi \mid \phi_0)$, the posterior of $\psi$ under $M_1$ with $\phi$ fixed at $\phi_0$. Under compatibility the factor is 1.

## In plain words

Before seeing data, the larger model gives some belief to the value in the null. After seeing data, it gives that value more or less belief. If the belief went up, the data favour the null, and if it went down, they favour the larger model. The theorem says that the size of this change is exactly the Bayes factor, as long as both models describe the remaining parameters in the same way. So one fit of the larger model is enough: you look at how high its posterior is at the null value and compare it with how high its prior was there.

## Proof

**Savage-Dickey.** By the definition of $\pi_1(\phi \mid x)$ at $\phi_0$, then the definition of $\pi_1(\psi \mid \phi_0)$, then compatibility,

$$\pi_1(\phi_0 \mid x) = \frac{1}{m_1(x)}\int f(x \mid \phi_0, \psi)\, \pi_1(\phi_0)\, \pi_1(\psi \mid \phi_0)\, d\psi = \frac{\pi_1(\phi_0)}{m_1(x)}\int f(x \mid \phi_0, \psi)\, \pi_0(\psi)\, d\psi = \frac{\pi_1(\phi_0)\, m_0(x)}{m_1(x)}.$$

The last integral is $m_0(x)$ by definition. Divide by $\pi_1(\phi_0) > 0$. $\square$

**Verdinelli and Wasserman.** Let $c(x) = \int f(x \mid \phi_0, \psi)\, \pi_1(\psi \mid \phi_0)\, d\psi$. The first equality above, without the compatibility step, says $c(x) = m_1(x)\, \pi_1(\phi_0 \mid x)/\pi_1(\phi_0)$. Also $\pi_1(\psi \mid \phi_0, x) = f(x \mid \phi_0, \psi)\pi_1(\psi \mid \phi_0)/c(x)$. By the support assumption,

$$m_0(x) = \int f(x \mid \phi_0, \psi)\, \pi_1(\psi \mid \phi_0)\, \frac{\pi_0(\psi)}{\pi_1(\psi \mid \phi_0)}\, d\psi = c(x)\, \mathbb{E}\Big[\frac{\pi_0(\psi)}{\pi_1(\psi \mid \phi_0)}\Big].$$

Divide by $m_1(x)$ and substitute $c(x)$. $\square$

**Remark on versions.** A density is defined only up to a set of measure zero, and $\{\phi_0\}$ has measure zero. If one changes $\pi_1(\phi)$ at the single point $\phi_0$, the prior is the same distribution, but the right side of the identity changes and the left side does not. In the same way, the conditional density $\pi_1(\psi \mid \phi = \phi_0)$ is not determined by the joint distribution, which is the Borel-Kolmogorov problem. The proof uses the three formulas of the statement at $\phi_0$, so it holds for those versions. When $\pi_1(\phi, \psi)$ and $f$ are continuous, these are the continuous versions, which is what any practical computation uses. Marin and Robert (2010) show that with other versions the "identity" can give any value, and they recommend fixing the versions in this way.

## Consequences

**A Bayes factor from one posterior.** Only the posterior of $\phi$ under $M_1$ is needed, at one point. With Markov chain draws $(\phi^{(s)}, \psi^{(s)})$ from $M_1$, for example by [Gibbs sampling](/gibbs-sampling/), the posterior density at $\phi_0$ can be estimated by a [kernel density estimate](/kernel-density-estimation/) of the $\phi^{(s)}$, or better by the Rao-Blackwell average $\frac1S\sum_s \pi_1(\phi_0 \mid \psi^{(s)}, x)$ when the full conditional of $\phi$ has a closed form. In contrast, [bridge sampling](/bridge-sampling/) and [nested sampling](/nested-sampling/) estimate $m_0$ and $m_1$ separately, and they work for models that are not nested and for priors that are not compatible.

**Exact check: a coin.** Toss a coin $n = 20$ times and see $y = 15$ heads. $M_1: \theta \sim$ Beta$(1, 1)$ and $M_0: \theta = 1/2$; there is no nuisance parameter. The posterior is Beta$(16, 6)$, and its density at $1/2$ is

$$\frac{21!}{15!\, 5!}\, 2^{-20} = \frac{21 \cdot 15504}{1048576} = \frac{20349}{65536},$$

while the prior density is 1. This is exactly $B_{01}$ on the [Bayes factor](/bayes-factor/) page. With the priors Beta$(2, 2)$, Beta$(3, 1)$ and Beta$(5, 5)$ the ratio is $0.2728$, $0.1925$ and $0.3032$, and in exact rational arithmetic it equals $m_0/m_1$ in each case.

**Example with a nuisance parameter.** Fit $y_i = \psi + \phi\, t_i + e_i$, $e_i \sim N(0, 1)$, at $t = (-2, -1, 0, 1, 2)$ with $y = (0.1, 0.9, 1.2, 2.3, 2.4)$, and test $M_0: \phi = 0$. Take independent priors $\psi \sim N(0, 4)$ and $\phi \sim N(0, 1)$ under $M_1$, and $\psi \sim N(0, 4)$ under $M_0$, so the priors are compatible. Because $\sum t_i = 0$, the posterior of $\phi$ is $N(6/11, 1/11)$: precision $1 + \sum t_i^2 = 11$ and mean $\sum t_i y_i / 11 = 6/11$. Its density at 0 is $0.25760$, the prior density there is $0.39894$, and the ratio $0.64570$ equals $m_0/m_1$ computed from the two marginal normal densities of $y$. The least squares slope is $0.6$, and the data mildly favour the slope, with $B_{10} \approx 1.55$.

**The Lindley paradox in one line.** If the prior of $\phi$ under $M_1$ is spread out, $\pi_1(\phi_0)$ goes to 0 while the posterior density at $\phi_0$ does not, so $B_{01} \to \infty$. This is Part 3 of the [Lindley paradox](/lindley-paradox/).

**Several parameters.** The statement and proof do not use the dimension of $\phi$, so the identity holds for a vector $\phi$ with joint densities. Testing several coefficients of a [Bayesian linear regression](/bayesian-linear-regression/) at once is an example.

## Tightness

**Compatibility cannot be dropped.** In the regression example, change only the prior of $M_0$ to $\psi \sim N(0, 1)$. The density ratio is still $0.64570$, because it does not look at $\pi_0$, but the true $B_{01}$ is $0.68535$. The Verdinelli-Wasserman factor is $\mathbb{E}[2e^{-3\psi^2/8}]$ over $\psi \sim N(6.9/5.25, 1/5.25)$, which is $1.06141$, and $0.64570 \times 1.06141 = 0.68535$.

**The prior density must be positive at $\phi_0$.** If $\pi_1(\phi_0) = 0$, as for non-local priors, the ratio is $0/0$ and the theorem says nothing. The Bayes factor is still defined through the marginal likelihoods.

**The prior must be proper.** If $\pi_1(\phi)$ is improper, $\pi_1(\phi_0)$ has no fixed scale, and neither has the Bayes factor; see [improper prior](/improper-prior/). An improper prior on the shared parameter $\psi$ is allowed, because it cancels in the proof as long as both models use it.

**The version matters.** As the remark in the proof shows, the identity is about the densities defined by the formulas of the statement, not about every version.

## History

Dickey (1971) gave the density ratio form of the Bayes factor for linear hypotheses on normal means and credited the idea to L. J. Savage, which gave the name. Verdinelli and Wasserman (1995) removed the compatibility condition with the correction factor above and used it with Markov chain Monte Carlo output. Marin and Robert (2010) pointed out that the identity depends on the choice of version of the densities, which they called the Savage-Dickey paradox, and showed how to fix it. Kass and Raftery (1995) list the ratio among the ways to compute Bayes factors.

## References
