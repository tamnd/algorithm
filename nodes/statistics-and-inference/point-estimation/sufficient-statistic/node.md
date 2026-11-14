---
tag: NJ4S6J
kind: definition
slug: sufficient-statistic
name: Sufficient statistic
aliases:
- sufficiency
area: statistics-and-inference/point-estimation
level: core
summary: A statistic T such that the conditional distribution of the data given T does not depend on the parameter, so T holds all the information the sample has about it.
prereqs: [estimator, conditional-probability, probability-distribution]
see_also: [fisher-neyman-factorization-theorem, complete-statistic, rao-blackwell-theorem, lehmann-scheffe-theorem, exponential-family-distribution, likelihood-function, welford-algorithm, bayesian-inference]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 6.2.1 (Definition 6.2.1, Theorem 6.2.2 and the factorization Theorem 6.2.6) and Section 6.2.2 (minimal sufficiency, Definition 6.2.11 and Theorem 6.2.13)
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 1, Section 1.6 (sufficient statistics, minimal sufficiency and the order statistic)
  - paper: doi:10.1098/rsta.1922.0009
    title: R. A. Fisher, On the mathematical foundations of theoretical statistics, Philosophical Transactions of the Royal Society of London, Series A 222 (1922), pages 309 to 368
    locator: the definition of the criterion of sufficiency
  - paper: "E. L. Lehmann and Henry Scheffé, Completeness, similar regions, and unbiased estimation, Part I, Sankhya 10 (1950)"
    title: Lehmann and Scheffé 1950
    locator: minimal sufficient statistics and the likelihood ratio criterion
---

A sufficient statistic is a [statistic](/estimator/) $T = t(X_1, \ldots, X_n)$ such that the conditional distribution of the sample given $T$ is the same for every value of the parameter $\theta$. Once $T$ is known, the rest of the sample is noise whose law does not depend on $\theta$, so a procedure that uses only $T$ loses nothing. Fisher (1922) gave the definition. The [Fisher-Neyman factorization theorem](/fisher-neyman-factorization-theorem/) is the usual way to find one, and the [Rao-Blackwell theorem](/rao-blackwell-theorem/) uses one to improve an estimator.

## Definition

**The model.** The sample $X = (X_1, \ldots, X_n)$ has joint density or mass function $f(x; \theta)$, $\theta \in \Theta$. $P_\theta$ and $\mathbb{E}_\theta$ are the probability and the expectation when $\theta$ is the true value. A statistic is $T = t(X)$ for a fixed function $t$ that does not use $\theta$ ([estimator](/estimator/) gives the details).

**Sufficient statistic.** $T$ is **sufficient for $\theta$** (for the family $\{f(\cdot\,; \theta) : \theta \in \Theta\}$) when the conditional distribution of $X$ given $T$ does not depend on $\theta$. For discrete data this means: for each $x$ and each $t$ with $P_\theta(T = t) > 0$,

$$P_\theta(X = x \mid T = t) \ \text{ is the same number for every } \theta \in \Theta.$$

For continuous data the condition is on a version of the conditional distribution of $X$ given $T$, which needs measure theory (Halmos and Savage 1949); in practice one checks sufficiency with the factorization theorem.

**A test by ratios (discrete case).** Let $q(t; \theta) = P_\theta(T = t)$. Then $T$ is sufficient if and only if, for every $x$ with $f(x; \theta) > 0$ for some $\theta$, the ratio $f(x; \theta) / q(t(x); \theta)$ is the same for every $\theta$ (Casella and Berger, Theorem 6.2.2). *Proof.* The event $\{X = x\}$ is contained in $\{T = t(x)\}$, so $P_\theta(X = x \mid T = t(x)) = f(x; \theta) / q(t(x); \theta)$, and $P_\theta(X = x \mid T = t) = 0$ when $t \ne t(x)$. $\square$

**Minimal sufficient statistic.** A sufficient statistic $T$ is **minimal sufficient** when it is a function of every other sufficient statistic: for every sufficient $U$ there is a function $r$ with $T = r(U)$. It gives the largest reduction of the data that keeps sufficiency. The **likelihood ratio criterion** (Lehmann and Scheffé 1950; Casella and Berger, Theorem 6.2.13): if for every pair of sample points $x, y$ the ratio $f(x; \theta) / f(y; \theta)$ is constant as a function of $\theta$ exactly when $t(x) = t(y)$, then $T$ is minimal sufficient.

### Properties

**(a) The sample can be rebuilt.** Let $T$ be sufficient and discrete, and let $k(x \mid t)$ be the conditional mass function of $X$ given $T = t$, which does not depend on $\theta$. Draw $X^*$ from $k(\cdot \mid T)$ with a random number generator. Then $X^*$ has the same distribution as $X$ under every $\theta$:

$$P_\theta(X^* = x) = \sum_t k(x \mid t)\, P_\theta(T = t) = \sum_t P_\theta(X = x \mid T = t)\, P_\theta(T = t) = P_\theta(X = x).$$

So any procedure that uses $X$ has a randomized copy that uses only $T$ and has the same distribution of outcomes, and so the same risk, at every $\theta$. This is the exact sense of "$T$ holds all the information about $\theta$".

**(b) Coarser and finer statistics.** If $T$ is sufficient and $T = r(U)$ for a statistic $U$, then $U$ is sufficient too. So the full sample $X$ is always sufficient, and a one-to-one function of a sufficient statistic is sufficient. A function of a sufficient statistic that loses information, such as $\bar X$ alone when the variance is unknown, is in general not sufficient.

**(c) The order statistic.** For iid data, the [order statistics](/order-statistic/) $(X_{(1)}, \ldots, X_{(n)})$ are sufficient in every model: given the sorted values, each of the $n!$ arrangements has the same conditional probability when the values are distinct, whatever $\theta$ is.

**(d) Bayesian sufficiency.** For any prior on $\theta$, the posterior given $X$ equals the posterior given $T$. By the factorization theorem $f(x; \theta) = g(t(x); \theta)\, h(x)$, and $h(x)$ cancels when the posterior is normalized (see [Bayesian inference](/bayesian-inference/)).

**(e) Information.** Under the regularity conditions of the [score function](/score-function/), the score of the sample is $\partial_\theta \log g(t(x); \theta)$, a function of $T$ only, so the [Fisher information](/fisher-information-matrix/) in $T$ equals the information in the whole sample.

## Examples and non-examples

**Bernoulli trials.** Let $X_1, X_2, X_3$ be iid Bernoulli$(p)$ and $T = X_1 + X_2 + X_3$. Given $T = 2$, the sample is one of $(1,1,0)$, $(1,0,1)$ and $(0,1,1)$. Each has probability $p^2(1-p)$, and $P_p(T = 2) = 3p^2(1-p)$, so each has conditional probability $1/3$ for every $p$. At $p = 1/4$, $P(T = 2) = 9/64$; at $p = 2/3$, $P(T = 2) = 4/9$; the conditional law is the same. In general, given $T = t$, every 0-1 sequence with $t$ ones has conditional probability $1/\binom{n}{t}$. So $T$ is sufficient.

**Bernoulli, minimal.** For two 0-1 samples $x$ and $y$ of size $n$, $f(x; p)/f(y; p) = (p/(1-p))^{\sum x_i - \sum y_i}$. It is constant in $p$ exactly when $\sum x_i = \sum y_i$, so $\sum X_i$ is minimal sufficient by the likelihood ratio criterion.

**Normal with both parameters unknown.** For iid $N(\mu, \sigma^2)$ data,

$$f(x; \mu, \sigma^2) = (2\pi\sigma^2)^{-n/2} \exp\!\Big(-\frac{\sum_i (x_i - \bar x)^2 + n(\bar x - \mu)^2}{2\sigma^2}\Big),$$

so $(\bar X, S^2)$ is sufficient, with $S^2 = \frac{1}{n-1}\sum_i (X_i - \bar X)^2$ (divisor $n - 1$). The samples $(3, 7, 7, 9, 14)$ and $(2, 6, 10, 10, 12)$ both have $\bar x = 8$ and $\sum_i (x_i - \bar x)^2 = 64$, so $S^2 = 16$. They have the same likelihood for every $(\mu, \sigma^2)$, and under this model they lead to the same inference. The pair is also minimal sufficient.

**Uniform.** For iid Uniform$(0, \theta)$ data, $f(x; \theta) = \theta^{-n}\, \mathbf{1}\{\max_i x_i \le \theta\}$ for $x_i \ge 0$, so $\max_i X_i$ is sufficient. On $(3, 7, 7, 9, 14)$ it is $14$. The family is not an [exponential family](/exponential-family-distribution/), because the support moves with $\theta$.

**Poisson and other exponential families.** For iid Poisson$(\lambda)$ data, $\sum_i X_i$ is sufficient. Given $\sum_i X_i = t$, the vector $X$ is multinomial with $t$ trials and equal cell probabilities $1/n$, which does not involve $\lambda$. For any exponential family $h(x)\exp(\eta(\theta)^\top T(x) - A(\theta))$, the sum $\sum_i T(X_i)$ is sufficient.

**Non-example: one observation of two.** For iid Bernoulli$(p)$ $X_1, X_2$, the statistic $X_1$ is not sufficient: $P_p(X = (1, 0) \mid X_1 = 1) = 1 - p$, which is $3/4$ at $p = 1/4$ and $1/2$ at $p = 1/2$.

**Non-example: the mean alone.** For $N(\mu, \sigma^2)$ data with $\sigma^2$ unknown, $\bar X$ is not sufficient for $(\mu, \sigma^2)$: given $\bar X$, the spread of the sample around $\bar X$ still carries information about $\sigma^2$. With $\sigma^2$ known, $\bar X$ is sufficient for $\mu$.

**No reduction.** For iid Cauchy data with an unknown location, and for the Laplace location family, the order statistic is minimal sufficient (Lehmann and Casella, Section 1.6). The data cannot be reduced below the sorted sample without loss.

### Pitfalls

- **Sufficiency is relative to a model.** $(\bar X, S^2)$ is sufficient under the normal model only. Under a heavier-tailed model, two samples with the same mean and variance can carry different information. A summary that is sufficient for a wrong model can hide the evidence that the model is wrong.
- **Sufficient is not minimal.** The whole sample is sufficient. A claim of "data reduction" needs a minimal sufficient statistic, or at least one of fixed dimension.
- **A sufficient statistic for part of the parameter.** When $\theta = (\psi, \lambda)$ with a nuisance $\lambda$, "sufficient for $\psi$" has no single standard meaning. The definition here is for the whole parameter.
- **The support.** In the uniform example, forgetting the indicator $\mathbf{1}\{\max_i x_i \le \theta\}$ makes the density look free of the data, and gives the wrong statistic.

## Related definitions

- [Fisher-Neyman factorization theorem](/fisher-neyman-factorization-theorem/): $T$ is sufficient if and only if $f(x; \theta) = g(t(x); \theta)\, h(x)$.
- [Complete statistic](/complete-statistic/): no nonzero function of $T$ has mean zero for every $\theta$. A complete sufficient statistic is minimal sufficient when a minimal one exists, and it is independent of every ancillary statistic (Basu's theorem).
- Ancillary statistic: a statistic whose distribution does not depend on $\theta$, such as the range $X_{(n)} - X_{(1)}$ in a location family. It is the opposite extreme of a sufficient statistic.
- [Rao-Blackwell theorem](/rao-blackwell-theorem/) and [Lehmann-Scheffé theorem](/lehmann-scheffe-theorem/): conditioning on a sufficient statistic improves an estimator, and with completeness gives the [minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/).
- [Likelihood function](/likelihood-function/): the likelihood depends on the data only through any sufficient statistic, up to a factor free of $\theta$.
- Streaming summaries: [Welford's algorithm](/welford-algorithm/) keeps $(n, \bar x, \sum (x_i - \bar x)^2)$, a sufficient statistic of the normal model, in one pass.

## References
