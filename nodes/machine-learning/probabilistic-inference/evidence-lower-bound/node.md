---
tag: 9XGGSJ
kind: definition
slug: evidence-lower-bound
name: Evidence lower bound
aliases:
- ELBO
- variational lower bound
- negative variational free energy
area: machine-learning/probabilistic-inference
level: advanced
summary: "ELBO(q) = E_q[log p(x, z) - log q(z)]. It is at most log p(x), and the gap is exactly KL(q || p(z | x))."
prereqs: [bayes-theorem, marginal-likelihood, jensens-inequality, shannon-entropy]
see_also: [variational-inference, mean-field-approximation, expectation-maximization, variational-autoencoder, black-box-variational-inference, wake-sleep-algorithm, bethe-free-energy, partition-function]
sources:
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 9.4 (the decomposition ln p(X | theta) = L(q, theta) + KL(q || p) for EM) and Section 10.1 (the same decomposition for variational inference)"
  - paper: doi:10.1080/01621459.2017.1285773
    title: "David M. Blei, Alp Kucukelbir and Jon D. McAuliffe, Variational inference: a review for statisticians, Journal of the American Statistical Association 112(518), 2017"
    locator: "Section 2.2 (the evidence lower bound, its two forms and the relation to the KL divergence)"
  - paper: doi:10.1023/A:1007665907178
    title: "Michael I. Jordan, Zoubin Ghahramani, Tommi S. Jaakkola and Lawrence K. Saul, An introduction to variational methods for graphical models, Machine Learning 37(2), 1999"
    locator: "the block approach to variational methods (the lower bound on the log likelihood from Jensen's inequality, and its gap as a KL divergence)"
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: "Section 2.3 (relative entropy) and Section 2.6 (Jensen's inequality and the information inequality D(p || q) >= 0)"
  - paper: "Radford M. Neal and Geoffrey E. Hinton, A view of the EM algorithm that justifies incremental, sparse, and other variants, in M. I. Jordan (ed.), Learning in Graphical Models, Kluwer, 1998, pages 355 to 368"
    title: Neal and Hinton 1998
    locator: the free energy F(q, theta) as a function of both q and theta, with EM as coordinate ascent on it
  - paper: "Yuri Burda, Roger Grosse and Ruslan Salakhutdinov, Importance weighted autoencoders, ICLR 2016, arXiv:1509.00519"
    title: Burda, Grosse and Salakhutdinov 2016
    locator: "the k-sample importance weighted bound, which equals the ELBO for k = 1 and does not decrease as k grows"
---

The evidence lower bound (ELBO) is a function of a distribution $q$ over the hidden variables $z$ of a model: the expected value under $q$ of $\log p(x, z) - \log q(z)$. It is a lower bound on the log of the evidence $p(x)$, the [marginal likelihood](/marginal-likelihood/) of the data, and the gap is exactly the Kullback-Leibler divergence from $q$ to the posterior $p(z \mid x)$. So to make the bound large is the same as to bring $q$ close to the posterior. This is the objective of [variational inference](/variational-inference/), of the E-step of [EM](/expectation-maximization/), and of the training of a [variational autoencoder](/variational-autoencoder/).

## Definition

**The model.** A joint distribution $p(x, z)$ over observed data $x$ and hidden variables $z$, for one fixed observed $x$. In the notation of this area, $x$ can be the whole data set $x_1, \ldots, x_n$, and $z$ holds all latent variables and parameters that are treated as random. The query is the posterior $p(z \mid x) = p(x, z) / p(x)$, and the evidence is $p(x) = \sum_z p(x, z)$ (an integral for a continuous $z$). Assume $p(x) > 0$. The sums below become integrals for densities.

**KL divergence.** For two distributions $q$ and $r$ over the same set, the Kullback-Leibler divergence (relative entropy) is

$$\mathrm{KL}(q \,\|\, r) = \sum_z q(z) \log \frac{q(z)}{r(z)},$$

with the conventions $0 \log(0/r) = 0$ and $q \log(q/0) = +\infty$ for $q > 0$. It is the [cross-entropy](/cross-entropy-loss/) of $r$ under $q$ minus the [entropy](/shannon-entropy/) of $q$. By Gibbs' inequality, $\mathrm{KL}(q \,\|\, r) \ge 0$, with equality if and only if $q = r$. It is not symmetric: $\mathrm{KL}(q \,\|\, r) \ne \mathrm{KL}(r \,\|\, q)$ in general.

**The ELBO.** For a distribution $q$ over $z$,

$$\mathrm{ELBO}(q) = \mathbb{E}_{q}\bigl[\log p(x, z) - \log q(z)\bigr] = \sum_z q(z) \log \frac{p(x, z)}{q(z)}.$$

If $q(z) > 0$ for some $z$ with $p(x, z) = 0$, the ELBO is $-\infty$.

**The identity.** For each $q$,

$$\log p(x) = \mathrm{ELBO}(q) + \mathrm{KL}\bigl(q \,\|\, p(\cdot \mid x)\bigr).$$

*Proof.* If the ELBO is finite, then $p(x, z) > 0$ wherever $q(z) > 0$, and for such $z$ the [Bayes rule](/bayes-theorem/) gives $\log p(x) = \log p(x, z) - \log p(z \mid x)$. Multiply by $q(z)$ and sum over the support of $q$, where $\sum_z q(z) = 1$:

$$\log p(x) = \sum_z q(z) \Bigl[\log \frac{p(x, z)}{q(z)} + \log \frac{q(z)}{p(z \mid x)}\Bigr] = \mathrm{ELBO}(q) + \mathrm{KL}\bigl(q \,\|\, p(\cdot \mid x)\bigr).$$

If the ELBO is $-\infty$, then some $z$ has $q(z) > 0$ and $p(z \mid x) = 0$, so the KL term is $+\infty$. In this case the identity has no finite meaning, but the bound below still holds, because $-\infty < \log p(x)$. $\square$

**The bound.** $\mathrm{ELBO}(q) \le \log p(x)$, with equality if and only if $q(z) = p(z \mid x)$ for all $z$. There are two standard derivations.

1. *From the identity.* The KL term is at least 0, and it is 0 only at $q = p(\cdot \mid x)$. So the gap $\log p(x) - \mathrm{ELBO}(q)$ is exactly $\mathrm{KL}(q \,\|\, p(\cdot \mid x))$.
2. *From [Jensen's inequality](/jensens-inequality/).* Let $S$ be the support of $q$. Then $\log p(x) \ge \log \sum_{z \in S} p(x, z) = \log \mathbb{E}_q\bigl[p(x, z)/q(z)\bigr] \ge \mathbb{E}_q\bigl[\log (p(x, z)/q(z))\bigr] = \mathrm{ELBO}(q)$, because $\log$ is concave. This derivation shows the bound but not the size of the gap.

**Two other forms.** Expand $\log p(x, z) = \log p(z) + \log p(x \mid z)$, or split the terms:

$$\mathrm{ELBO}(q) = \mathbb{E}_q[\log p(x \mid z)] - \mathrm{KL}(q \,\|\, p(z)) = \mathbb{E}_q[\log p(x, z)] + H(q),$$

where $p(z)$ is the prior and $H(q) = -\sum_z q(z) \log q(z)$. The first form is "fit the data, but stay near the prior"; it is the loss of a [variational autoencoder](/variational-autoencoder/). The second form is "expected negative energy plus entropy". Its negative, $F(q) = -\mathrm{ELBO}(q)$, is the *variational free energy* of statistical physics.

**With parameters.** If the model has parameters $\theta$, write $\mathcal{L}(q, \theta) = \mathbb{E}_q[\log p_\theta(x, z) - \log q(z)]$. Then $\mathcal{L}(q, \theta) \le \log p_\theta(x)$ for all $q$ and $\theta$. Maximizing over $q$ makes the bound tight, and maximizing over $\theta$ with $q$ fixed raises the bound. This is EM as coordinate ascent (Neal and Hinton 1998). When $q$ is restricted to a family that does not hold the posterior, the maximum over $q$ is not tight, and maximizing $\mathcal{L}$ over $\theta$ is variational EM.

**Unnormalized models.** For a [Markov random field](/markov-random-field/) $p(z) = \tilde p(z) / Z$ with no data, the same algebra gives $\log Z = \mathbb{E}_q[\log \tilde p(z)] + H(q) + \mathrm{KL}(q \,\|\, p)$. So $\mathbb{E}_q[\log \tilde p] + H(q)$ is a lower bound on the log [partition function](/partition-function/). The [mean-field approximation](/mean-field-approximation/) maximizes it over fully factorized $q$.

## Examples and non-examples

**A three-state example.** Let $z \in \{1, 2, 3\}$ with prior $p(z) = (1/2, 1/3, 1/6)$, and let the observed $x$ have likelihood $p(x \mid z) = (1/4, 1/2, 3/4)$. Then $p(x, z) = (1/8, 1/6, 1/8)$, the evidence is $p(x) = 5/12$, and the posterior is $p(z \mid x) = (3/10, 2/5, 3/10)$.

| $q$ | ELBO | KL to the posterior | sum |
|---|---|---|---|
| $(1/3, 1/3, 1/3)$ | $\tfrac13 \log \tfrac{9}{128} \approx -0.8849$ | $\tfrac13 \log \tfrac{250}{243} \approx 0.0095$ | $\log \tfrac{5}{12} \approx -0.8755$ |
| $(1/2, 1/2, 0)$ | $\tfrac12 \log \tfrac{1}{12} \approx -1.2425$ | $\tfrac12 \log \tfrac{25}{12} \approx 0.3670$ | $\log \tfrac{5}{12}$ |
| $(3/10, 2/5, 3/10)$ | $\log \tfrac{5}{12}$ | $0$ | $\log \tfrac{5}{12}$ |

For the uniform $q$, the ratio $p(x, z)/q(z)$ is $(3/8, 1/2, 3/8)$, so the ELBO is $\tfrac13 \log(\tfrac38 \cdot \tfrac12 \cdot \tfrac38) = \tfrac13 \log \tfrac{9}{128}$. In the sum column, $\tfrac{9}{128} \cdot \tfrac{250}{243} = \tfrac{125}{1728} = (5/12)^3$, so the identity holds exactly, not only to four places. The implementation checks the identity with no rounding: it writes the log of a rational number as a sum of integer multiples of logs of primes, and it compares the coefficients as fractions.

The second row shows the Jensen derivation with a smaller support: $\log \mathbb{E}_q[p(x, z)/q(z)] = \log(1/8 + 1/6) = \log(7/24) \approx -1.232$, which is below $\log p(x)$ because $q$ ignores $z = 3$, and the ELBO $-1.2425$ is below that.

**A Gaussian example.** Let $z \sim \mathcal{N}(0, 1)$ and $x \mid z \sim \mathcal{N}(z, 1)$. Then $p(x) = \mathcal{N}(x; 0, 2)$ and $p(z \mid x) = \mathcal{N}(x/2, 1/2)$. For $q = \mathcal{N}(m, s^2)$, the second form gives the closed expression $\mathrm{ELBO} = -\log(2\pi) - \tfrac12\bigl((x - m)^2 + m^2 + 2 s^2\bigr) + \tfrac12 \log(2\pi e s^2)$. Its maximum is at $m = x/2$, $s^2 = 1/2$, the exact posterior, and there it equals $\log \mathcal{N}(x; 0, 2)$.

**Non-example: the reverse KL.** The quantity $\log p(x) - \mathrm{KL}(p(\cdot \mid x) \,\|\, q)$ is not an ELBO, and it can not be computed without the posterior. The direction matters: the ELBO gap is $\mathrm{KL}(q \,\|\, p)$, which is large where $q$ puts mass that $p$ does not have. So a $q$ that maximizes the ELBO over a restricted family avoids regions of low posterior mass, and it tends to under-cover the posterior. [Expectation propagation](/expectation-propagation/) and the sleep phase of the [wake-sleep algorithm](/wake-sleep-algorithm/) use the other direction, and they do not maximize an ELBO.

**Non-example: a single sample.** The value $\log p(x, z) - \log q(z)$ at one draw $z \sim q$ is an unbiased estimate of the ELBO, but it is not a lower bound on $\log p(x)$: it can be larger. Only its expectation is a bound.

**Non-example: the importance weighted bound.** $\mathbb{E}\bigl[\log \tfrac1k \sum_{j=1}^k p(x, z_j)/q(z_j)\bigr]$ with $z_1, \ldots, z_k$ drawn independently from $q$ is also a lower bound on $\log p(x)$, by Jensen. It equals the ELBO for $k = 1$ only, and it does not decrease as $k$ grows (Burda, Grosse and Salakhutdinov 2016). Its gap is not $\mathrm{KL}(q \,\|\, p(\cdot \mid x))$.

## Related definitions

- [Variational inference](/variational-inference/) maximizes the ELBO over a family of distributions; [coordinate ascent](/mean-field-approximation/), [black-box](/black-box-variational-inference/) and [stochastic](/stochastic-variational-inference/) variational inference are three ways to do it.
- [Expectation-maximization](/expectation-maximization/) alternates between the best $q$ (the exact posterior) and the best $\theta$ for $\mathcal{L}(q, \theta)$.
- The [Bethe free energy](/bethe-free-energy/) replaces the entropy term $H(q)$ by an approximation built from local marginals. It is not a bound in general.
- The [marginal likelihood](/marginal-likelihood/) $p(x)$ is the quantity that the ELBO bounds; Bayesian model comparison uses the ELBO as a cheap replacement for it.
- The [partition function](/partition-function/) $Z$ plays the role of $p(x)$ for an unnormalized model.
- The [Shannon entropy](/shannon-entropy/) and the [cross-entropy](/cross-entropy-loss/) are the two parts of the KL divergence.

## References
