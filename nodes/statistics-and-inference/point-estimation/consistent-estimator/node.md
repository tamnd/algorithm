---
tag: QCXPAF
kind: definition
slug: consistent-estimator
name: Consistent estimator
aliases:
- consistency of an estimator
- weakly consistent estimator
area: statistics-and-inference/point-estimation
level: core
summary: An estimator that converges in probability to the true parameter as the sample size grows. Strong consistency asks for almost sure convergence.
prereqs: [estimator, sampling-distribution, law-of-large-numbers, chebyshev-inequality]
see_also: [estimator-bias, standard-error, maximum-likelihood-estimation, asymptotic-normality-of-mle, slutsky-theorem, method-of-moments, sample-variance, markov-inequality]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 5.5.1 to 5.5.3 (convergence in probability, almost surely and in distribution, and the laws of large numbers) and Section 10.1.1 (consistency)
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 6 (asymptotic optimality, consistency of estimators and of roots of the likelihood equation)
  - paper: doi:10.2307/1914288
    title: J. Neyman and Elizabeth L. Scott, Consistent estimates based on partially consistent observations, Econometrica 16(1), 1948
    locator: pp. 1 to 32 (the maximum likelihood estimator that is not consistent when the number of parameters grows with the sample)
---

A consistent estimator is a sequence of [estimators](/estimator/) $T_n$, one for each sample size, that converges in probability to the target $\psi(\theta)$ as $n \to \infty$, for every value of $\theta$. It is a large-sample property of the [sampling distribution](/sampling-distribution/): the law of $T_n$ piles up at the right point. It says nothing about the error at a fixed $n$, and it is neither weaker nor stronger than [unbiasedness](/estimator-bias/).

## Definition

Let $T_n = t_n(X_1, \ldots, X_n)$, $n = 1, 2, \ldots$, be estimators of $\psi(\theta) \in \mathbb{R}^k$, where $X_1, X_2, \ldots$ have the law $P_\theta$, $\theta \in \Theta$.

- **Consistent (weakly consistent).** For every $\theta \in \Theta$ and every $\varepsilon > 0$,
$$\lim_{n \to \infty} P_\theta\big(\lVert T_n - \psi(\theta) \rVert > \varepsilon\big) = 0.$$
That is, $T_n$ converges in probability to $\psi(\theta)$ under each $P_\theta$.
- **Strongly consistent.** For every $\theta \in \Theta$, $P_\theta\big(T_n \to \psi(\theta)\big) = 1$: $T_n$ converges almost surely.
- **Consistent in mean square.** For every $\theta$, $\mathbb{E}_\theta \lVert T_n - \psi(\theta) \rVert^2 \to 0$: the [mean squared error](/mean-squared-error/) tends to 0.

The quantifier "for every $\theta$" is part of the definition. An estimator that converges to $\psi(\theta_0)$ only when $\theta_0$ is true, such as the constant $\psi(\theta_0)$, is not consistent.

**How the three relate.**

1. Almost sure convergence implies convergence in probability, so a strongly consistent sequence is consistent.
2. Mean square consistency implies consistency. By [Markov's inequality](/markov-inequality/) applied to $\lVert T_n - \psi(\theta) \rVert^2$,
$$P_\theta\big(\lVert T_n - \psi(\theta) \rVert > \varepsilon\big) \le \frac{\mathbb{E}_\theta \lVert T_n - \psi(\theta) \rVert^2}{\varepsilon^2} \to 0.$$
For real $T_n$ the mean squared error is $\operatorname{Var}_\theta(T_n) + \operatorname{bias}_\theta(T_n)^2$, so a bias and a [standard error](/standard-error/) that both tend to 0 give consistency.
3. The converses fail. Consistency does not need a finite variance, or any moment of $T_n$.

**Continuous maps keep consistency.** If $T_n$ is consistent for $\theta$ and $g$ is continuous at $\theta$, then $g(T_n)$ is consistent for $g(\theta)$. *Proof.* Fix $\varepsilon > 0$ and take $\delta > 0$ with $\lVert g(u) - g(\theta) \rVert \le \varepsilon$ whenever $\lVert u - \theta \rVert \le \delta$. Then the event $\lVert g(T_n) - g(\theta) \rVert > \varepsilon$ lies inside the event $\lVert T_n - \theta \rVert > \delta$, whose probability tends to 0. $\blacksquare$ Unbiasedness, in contrast, is lost under nonlinear maps.

**Uniform consistency.** If $\sup_{\theta \in \Theta} P_\theta(\lVert T_n - \psi(\theta) \rVert > \varepsilon) \to 0$, the sequence is uniformly consistent. The plain definition allows the sample size needed for a given accuracy to depend on $\theta$.

## Examples and non-examples

**The sample mean.** If $\mathbb{E}_\theta \lvert X_1 \rvert < \infty$, the strong [law of large numbers](/law-of-large-numbers/) gives $\bar X \to \mu$ almost surely, so $\bar X$ is strongly consistent for $\mu$. With $\sigma^2 < \infty$ there is a one-line proof of weak consistency: by [Chebyshev's inequality](/chebyshev-inequality/), $P(\lvert \bar X - \mu \rvert > \varepsilon) \le \sigma^2/(n\varepsilon^2)$.

**Exact numbers.** For iid Bernoulli$(1/2)$ data and $\varepsilon = 0.1$, summing binomial probabilities gives

| $n$ | $P(\lvert \bar X - 0.5 \rvert > 0.1)$ | Chebyshev bound $0.25/(n \cdot 0.01)$ |
|---|---|---|
| 10 | 0.34375 | 2.5 |
| 100 | 0.03520 | 0.25 |
| 1000 | $1.80 \times 10^{-10}$ | 0.025 |

The probability tends to 0, as consistency requires. The bound is valid but loose; the true probability falls exponentially in $n$.

**The sample variance.** If $\sigma^2 < \infty$, then $\frac1n \sum_i X_i^2 \to \sigma^2 + \mu^2$ and $\bar X \to \mu$ in probability, by the law of large numbers. The map $(a, b) \mapsto a - b^2$ is continuous, so $\frac1n\sum_i (X_i - \bar X)^2 = \frac1n \sum_i X_i^2 - \bar X^2 \to \sigma^2$ in probability. Multiplying by $n/(n-1) \to 1$ shows that the [sample variance](/sample-variance/) $S^2$ is consistent too. The divisor-$n$ version is biased at every $n$ and still consistent.

**The maximum of a uniform sample.** For iid Uniform$(0, \theta)$ data and $0 < \varepsilon < \theta$, $P_\theta(\lvert \max_i X_i - \theta \rvert > \varepsilon) = ((\theta - \varepsilon)/\theta)^n \to 0$. The maximum is biased and consistent.

**Non-example: one observation.** $T_n = X_1$ is unbiased for $\mu$ at every $n$, but $P(\lvert X_1 - \mu \rvert > \varepsilon)$ does not depend on $n$. It is positive for small $\varepsilon$ unless $X_1$ is constant, so $T_n$ is not consistent.

**Non-example: the Cauchy mean.** For iid Cauchy data with center $\theta$, $\bar X$ has the same Cauchy law for every $n$, so it is not consistent for $\theta$. The sample median is.

**Non-example: a maximum likelihood estimator.** Neyman and Scott (1948) gave this model. For $i = 1, \ldots, m$, let $X_{i1}, X_{i2}$ be iid $N(\mu_i, \sigma^2)$, independent over $i$, with a new mean $\mu_i$ for each pair. The [maximum likelihood](/maximum-likelihood-estimation/) estimator of $\sigma^2$ is
$$\hat\sigma^2 = \frac{1}{2m} \sum_{i=1}^{m} \sum_{j=1}^{2} (X_{ij} - \bar X_i)^2 = \frac{1}{4m} \sum_{i=1}^{m} (X_{i1} - X_{i2})^2.$$
Each $X_{i1} - X_{i2}$ is $N(0, 2\sigma^2)$, so the terms $(X_{i1} - X_{i2})^2/4$ are iid with mean $\sigma^2/2$, and the law of large numbers gives $\hat\sigma^2 \to \sigma^2/2$ in probability. The number of parameters grows with the data, and the estimator converges to the wrong value. Doubling it gives a consistent estimator.

**Consistent and useless.** $T_n = \bar X + 1000/n$ is consistent for $\mu$, and its bias is 100 at $n = 10$. Consistency is a statement about the limit only.

## Related definitions

- [Law of large numbers](/law-of-large-numbers/): the source of most consistency proofs.
- [Bias](/estimator-bias/) and [standard error](/standard-error/): if both tend to 0, the estimator is consistent.
- [Asymptotic normality of the MLE](/asymptotic-normality-of-mle/): the next order, the rate $\sqrt n$ and the limiting law of $\sqrt n(\hat\theta_n - \theta)$, for a consistent root of the likelihood equation.
- [Slutsky's theorem](/slutsky-theorem/): combines a consistent estimator with a sequence that converges in distribution.
- [Method of moments](/method-of-moments/): consistent by the law of large numbers and the continuity argument above.

## References
