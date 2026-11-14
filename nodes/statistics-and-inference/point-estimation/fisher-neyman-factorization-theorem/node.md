---
tag: VXGK5J
kind: theorem
slug: fisher-neyman-factorization-theorem
name: Fisher-Neyman factorization theorem
aliases:
- factorization theorem
- factorization criterion
area: statistics-and-inference/point-estimation
level: core
summary: T is sufficient if and only if the density factors as g(T(x), theta) h(x). It is the usual way to find sufficient statistics.
prereqs: [sufficient-statistic, likelihood-function, conditional-probability]
see_also: [complete-statistic, exponential-family-distribution, rao-blackwell-theorem, maximum-likelihood-estimation, bayesian-inference]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 6.2.1, Theorem 6.2.6 (the factorization theorem, with the proof for discrete data) and Theorem 6.2.10 (exponential families)
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 1, Section 1.6 (the factorization criterion for dominated families)
  - paper: "Jerzy Neyman, Su un teorema concernente le cosiddette statistiche sufficienti, Giornale dell'Istituto Italiano degli Attuari 6 (1935), pages 320 to 334"
    title: Neyman 1935
    locator: the factorization criterion for sufficiency
  - paper: doi:10.1214/aoms/1177730032
    title: Paul R. Halmos and L. J. Savage, Application of the Radon-Nikodym theorem to the theory of sufficient statistics, Annals of Mathematical Statistics 20(2) (1949), pages 225 to 241
    locator: the factorization theorem for dominated families
  - paper: doi:10.1098/rsta.1922.0009
    title: R. A. Fisher, On the mathematical foundations of theoretical statistics, Philosophical Transactions of the Royal Society of London, Series A 222 (1922), pages 309 to 368
    locator: the criterion of sufficiency
---

The Fisher-Neyman factorization theorem says that a statistic $T = t(X)$ is [sufficient](/sufficient-statistic/) for $\theta$ if and only if the joint density splits as $f(x; \theta) = g(t(x); \theta)\, h(x)$, where $g$ depends on the data only through $t(x)$ and $h$ does not depend on $\theta$. It turns the definition of sufficiency, a statement about conditional distributions, into a check that one does by looking at the [likelihood](/likelihood-function/). Neyman (1935) proved it after Fisher (1922) used it in special cases, and Halmos and Savage (1949) proved it for every dominated family.

## Statement

The sample $X = (X_1, \ldots, X_n)$ has joint density or mass function $f(x; \theta)$ for $\theta \in \Theta$, and $T = t(X)$ is a statistic.

**Theorem (discrete case).** Let $X$ take values in a countable set $\mathcal X$. Then $T$ is sufficient for $\theta$ if and only if there are functions $g(t; \theta) \ge 0$ and $h(x) \ge 0$ such that

$$f(x; \theta) = g(t(x); \theta)\, h(x) \qquad \text{for all } x \in \mathcal X \text{ and all } \theta \in \Theta.$$

**Theorem (dominated families; Halmos and Savage 1949).** Let $\{P_\theta : \theta \in \Theta\}$ be a family of distributions on a measurable space, all with densities $f(x; \theta)$ with respect to one $\sigma$-finite measure $\mu$ (the family is *dominated*). Let $t$ be measurable. Then $T$ is sufficient if and only if there are a nonnegative measurable $h$ and, for each $\theta$, a nonnegative measurable $g(\cdot\,; \theta)$ with $f(x; \theta) = g(t(x); \theta)\, h(x)$ for $\mu$-almost every $x$.

Every family of densities with respect to Lebesgue measure, and every family on a countable set, is dominated. So the theorem covers all the usual parametric models.

## In plain words

Write down the probability of the whole sample as a formula. Try to split it into two factors. The first factor may contain the unknown parameter, but it may look at the data only through one summary. The second factor may look at the data in any way, but it must not contain the parameter. If such a split exists, the summary is sufficient: two samples with the same summary give likelihoods that differ only by a constant factor, so they lead to the same conclusions about the parameter. If no split exists, the summary misses some information. The theorem says that this simple check is exactly the same as the formal definition with conditional probabilities.

## Proof

We prove the discrete case in full. Let $q(t; \theta) = P_\theta(T = t) = \sum_{y : t(y) = t} f(y; \theta)$.

**If $T$ is sufficient, the density factors.** By sufficiency, for each $x$ the number $k(x) = P_\theta(X = x \mid T = t(x))$ is the same for every $\theta$ with $q(t(x); \theta) > 0$. Set $h(x) = k(x)$ when some $\theta$ has $q(t(x); \theta) > 0$, and $h(x) = 0$ otherwise. Set $g(t; \theta) = q(t; \theta)$. Fix $x$ and $\theta$.

- If $q(t(x); \theta) > 0$: since $\{X = x\} \subseteq \{T = t(x)\}$, $f(x; \theta) = P_\theta(X = x, T = t(x)) = q(t(x); \theta)\, P_\theta(X = x \mid T = t(x)) = g(t(x); \theta)\, h(x)$.
- If $q(t(x); \theta) = 0$: then $f(x; \theta) \le q(t(x); \theta) = 0$, and $g(t(x); \theta) h(x) = 0$ as well.

**If the density factors, $T$ is sufficient.** Assume $f(x; \theta) = g(t(x); \theta)\, h(x)$ for all $x, \theta$. Then

$$q(t; \theta) = \sum_{y : t(y) = t} g(t; \theta)\, h(y) = g(t; \theta)\, H(t), \qquad H(t) = \sum_{y : t(y) = t} h(y).$$

Take $x$, $t$ and $\theta$ with $q(t; \theta) > 0$; then $g(t; \theta) > 0$ and $H(t) > 0$. If $t(x) \ne t$, then $P_\theta(X = x \mid T = t) = 0$. If $t(x) = t$, then

$$P_\theta(X = x \mid T = t) = \frac{f(x; \theta)}{q(t; \theta)} = \frac{g(t; \theta)\, h(x)}{g(t; \theta)\, H(t)} = \frac{h(x)}{H(t)}.$$

In both cases the conditional probability does not depend on $\theta$, so $T$ is sufficient. $\blacksquare$

**The dominated case (sketch).** The proof of Halmos and Savage has two steps. First, a dominated family contains a countable subfamily $P_{\theta_1}, P_{\theta_2}, \ldots$ such that the mixture $\lambda = \sum_i c_i P_{\theta_i}$, with $c_i > 0$ and $\sum_i c_i = 1$, has the same null sets as the whole family. Second, $T$ is sufficient if and only if each density $dP_\theta / d\lambda$ can be chosen as a function of $t(x)$; the Radon-Nikodym theorem and the properties of conditional expectation give this step, and then $h = d\lambda/d\mu$. The full proof is in Halmos and Savage (1949) and in Lehmann and Casella, Section 1.6.

## Consequences

**Exponential families.** If $f(x; \theta) = h(x) \exp(\eta(\theta)^\top T(x) - A(\theta))$ for one observation, then for an iid sample

$$\prod_{i=1}^n f(x_i; \theta) = \exp\Big(\eta(\theta)^\top \sum_i T(x_i) - nA(\theta)\Big) \cdot \prod_i h(x_i),$$

so $\sum_i T(X_i)$ is sufficient, and its dimension does not grow with $n$ (see [exponential family](/exponential-family-distribution/)).

**Worked examples.** Each line gives $g$ and $h$ for an iid sample of size $n$.

| model | $g(t; \theta)$ | $h(x)$ | sufficient $T$ |
|---|---|---|---|
| Bernoulli$(p)$ | $p^{t}(1-p)^{n-t}$ | $1$ | $\sum_i x_i$ |
| Poisson$(\lambda)$ | $\lambda^{t} e^{-n\lambda}$ | $1/\prod_i x_i!$ | $\sum_i x_i$ |
| $N(\mu, \sigma^2)$ | $(2\pi\sigma^2)^{-n/2} e^{-(t_2 - 2\mu t_1 + n\mu^2)/(2\sigma^2)}$ | $1$ | $(t_1, t_2) = (\sum_i x_i, \sum_i x_i^2)$ |
| Gamma$(\alpha, \beta)$, rate $\beta$ | $\frac{\beta^{n\alpha}}{\Gamma(\alpha)^n} e^{(\alpha - 1)t_1 - \beta t_2}$ | $\mathbf{1}\{\text{all } x_i > 0\}$ | $(\sum_i \log x_i, \sum_i x_i)$ |
| Uniform$(0, \theta)$ | $\theta^{-n}\,\mathbf{1}\{t \le \theta\}$ | $\mathbf{1}\{\text{all } x_i \ge 0\}$ | $\max_i x_i$ |
| Uniform$(\theta, \theta + 1)$ | $\mathbf{1}\{\theta \le t_1\}\,\mathbf{1}\{t_2 \le \theta + 1\}$ | $1$ | $(\min_i x_i, \max_i x_i)$ |

**A numerical check.** For the Poisson model and the sample $x = (3, 7, 7, 9, 14)$, $t = 40$ and $h(x) = 1/(3!\,7!\,7!\,9!\,14!) \approx 2.074 \times 10^{-25}$. The likelihood ratio between $\lambda = 8$ and $\lambda = 5$ is $g(40; 8)/g(40; 5) = (8/5)^{40} e^{-15} \approx 44.71$. The factor $h$ cancels, so the sample $(8, 8, 8, 8, 8)$, which has the same total, gives the same ratio. Every comparison of two values of $\lambda$ depends on the data only through $t$.

**The likelihood and its maximizer.** Because $h(x)$ does not depend on $\theta$, the [likelihood](/likelihood-function/) is proportional to $g(t(x); \theta)$. So a [maximum likelihood estimate](/maximum-likelihood-estimation/), when it is unique, is a function of every sufficient statistic, and the posterior of [Bayesian inference](/bayesian-inference/) depends on the data only through $T$, for every prior.

**Minimal sufficiency.** The factorization gives a sufficient statistic, but not always a minimal one. The likelihood ratio criterion on the page [sufficient statistic](/sufficient-statistic/) checks minimality; for a full-rank exponential family, $\sum_i T(X_i)$ is minimal sufficient and [complete](/complete-statistic/).

## Tightness

**The factorization must hold for every $x$ and every $\theta$.** A split that holds only on the support for one $\theta$ is not enough. For Uniform$(0, \theta)$ the density is $\theta^{-n}$ on the support, which looks free of the data. The indicator $\mathbf{1}\{\max_i x_i \le \theta\}$ depends on both $x$ and $\theta$, and it must go into $g$. Putting it into $h$ is the most common error with this theorem.

**The split is not unique.** If $f = g h$, then $f = (g c)(h/c)$ for any positive function $c(t(x))$. Only the existence of a split matters.

**A sufficient statistic can be larger than the parameter.** For Uniform$(\theta, \theta + 1)$ the parameter is one number, but the minimal sufficient statistic $(\min_i X_i, \max_i X_i)$ has two. For the Cauchy location family no factorization reduces the data below the order statistic. By the Pitman-Koopman-Darmois theorem, under smoothness conditions and with a support that does not depend on $\theta$, a sufficient statistic of fixed dimension for every $n$ exists only for exponential families (see [exponential family](/exponential-family-distribution/)).

**Domination is needed for the general form.** The proof of the dominated case uses densities with respect to one $\sigma$-finite measure. Without domination, there is no density to factor. The discrete case needs no extra condition, because counting measure on a countable set dominates every family on it.

## History

Fisher (1922) defined sufficiency and showed in examples that a sufficient statistic makes the likelihood depend on the data only through it. Neyman (1935) proved the factorization criterion under general conditions, so the theorem carries both names. Halmos and Savage (1949) gave the measure-theoretic form for dominated families, with the Radon-Nikodym theorem; Casella and Berger, Section 6.2.1, and Lehmann and Casella, Section 1.6, give the textbook versions.

## References
