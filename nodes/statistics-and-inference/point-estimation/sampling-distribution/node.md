---
tag: EJ454X
kind: concept
slug: sampling-distribution
name: Sampling distribution
aliases:
- distribution of a statistic
area: statistics-and-inference/point-estimation
level: intro
summary: The distribution of a statistic over repeated samples from the same population. Standard errors, tests and intervals all come from it.
prereqs: [estimator, probability-distribution, independent-random-variables]
see_also: [estimator-bias, standard-error, consistent-estimator, central-limit-theorem, bootstrap-method, empirical-distribution-function, confidence-interval, p-value]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 5.2 (the sampling distribution of a statistic of a random sample) and Section 5.3.1 (properties of the sample mean and variance of normal data, Theorem 5.3.1)
  - paper: doi:10.1214/aoms/1177731647
    title: Eugene Lukacs, A characterization of the normal distribution, Annals of Mathematical Statistics 13(1), 1942
    locator: pp. 91 to 93 (independence of the sample mean and the sample variance implies normality, under a finite variance)
  - book: isbn:9780412042317
    title: Bradley Efron and Robert J. Tibshirani, An Introduction to the Bootstrap, Chapman and Hall, 1993
    locator: Chapter 2 (the accuracy of a sample mean) and Chapter 6 (the bootstrap estimate of standard error)
---

The sampling distribution of a statistic $T = t(X_1, \ldots, X_n)$ is the probability distribution of $T$ when the sample is drawn again and again from the same population at a fixed parameter $\theta$. It is the object on which the properties of an [estimator](/estimator/) are defined: its mean gives the [bias](/estimator-bias/), its standard deviation the [standard error](/standard-error/), and its concentration as $n$ grows gives [consistency](/consistent-estimator/). Confidence intervals and the null distributions of tests are statements about it too.

## In plain words

Take a sample and compute one number from it, such as the average. A second sample from the same source gives a slightly different number, and a third gives another. If you could repeat this many times, the numbers would form their own histogram. That histogram is the sampling distribution of the average.

It is not the histogram of the data. The data show how single values vary. The sampling distribution shows how the computed number varies from sample to sample. Its center tells whether the method is right on average. Its width tells how much one result can be trusted. In practice you see only one sample, so the sampling distribution comes from theory, from a computer simulation, or from resampling the one sample you have.

## The idea

**Three distributions.** Keep three distributions apart:

- the population law $P_\theta$ of one observation, with density or mass function $f(x; \theta)$;
- the [empirical distribution](/empirical-distribution-function/) of the observed sample, which puts mass $1/n$ on each $x_i$;
- the sampling distribution of $T$, the law of $t(X_1, \ldots, X_n)$ when $X_1, \ldots, X_n$ are iid $P_\theta$: $P_\theta(T \in B) = P_\theta\big((X_1, \ldots, X_n) \in t^{-1}(B)\big)$.

The sampling distribution depends on $\theta$, on $n$ and on the function $t$. Each property in the table on [estimator](/estimator/) is a property of it at each $\theta$.

**Four ways to find it.**

1. *Exactly*, by enumeration, a change of variables or a generating function. This works for small discrete problems and for a few families, above all the normal.
2. *Asymptotically*, as $n \to \infty$. The [central limit theorem](/central-limit-theorem/) gives $\sqrt n(\bar X - \mu)$ converging in distribution to $N(0, \sigma^2)$ when $\sigma^2 < \infty$, and the [delta method](/delta-method/) carries this to smooth functions of means.
3. *By simulation* at a chosen $\theta$: draw many samples with a fixed seed, compute $T$ on each, and use the [Monte Carlo](/monte-carlo-integration/) histogram.
4. *By resampling*: the [bootstrap](/bootstrap-method/) replaces the unknown $P_\theta$ by the empirical distribution and simulates from it.

**Normal data.** Let $X_1, \ldots, X_n$ be iid $N(\mu, \sigma^2)$ with $n \ge 2$, and let $S^2$ be the [sample variance](/sample-variance/) (divisor $n - 1$). Then (Casella and Berger, Theorem 5.3.1):

1. $\bar X$ has the law $N(\mu, \sigma^2/n)$;
2. $(n - 1) S^2/\sigma^2$ has the chi-square law with $n - 1$ degrees of freedom;
3. $\bar X$ and $S^2$ are independent;
4. $(\bar X - \mu)/(S/\sqrt n)$ has the Student t law with $n - 1$ degrees of freedom.

Item 3 is special to the normal. Lukacs (1942) proved that if $X_1, \ldots, X_n$ ($n \ge 2$) are iid with finite variance and $\bar X$ and $S^2$ are independent, then the law is normal. Item 4 is exact only under normal iid data; for other data it holds only approximately for large $n$.

**Pivots.** The ratio in item 4 depends on $\mu$, so it is not a statistic, but its law is free of $(\mu, \sigma)$. Such a quantity is a *pivot*. Inverting a pivot gives an interval with exact coverage, as the [t interval](/t-confidence-interval/) does.

## Examples

**Exact enumeration.** Let the population be uniform on $\{1, 2, 9\}$, so $\mu = 4$ and $\sigma^2 = 38/3$ (divisor $N = 3$ for a whole population law). Draw $n = 2$ values with replacement. The 9 ordered pairs are equally likely, and $\bar X$ has this law:

| $\bar x$ | 1 | 1.5 | 2 | 5 | 5.5 | 9 |
|---|---|---|---|---|---|---|
| probability | 1/9 | 2/9 | 1/9 | 2/9 | 2/9 | 1/9 |

Its mean is $4 = \mu$ and its variance is $19/3 = \sigma^2/2$, as the general formulas $\mathbb{E}[\bar X] = \mu$ and $\operatorname{Var}(\bar X) = \sigma^2/n$ require. The law is not symmetric, even though $\bar X$ is unbiased. The sample variance $S^2 = (X_1 - X_2)^2/2$ takes the values $0$, $1/2$, $49/2$ and $32$ with probabilities $1/3$, $2/9$, $2/9$ and $2/9$. Its mean is $38/3 = \sigma^2$, so $S^2$ is unbiased, but $\mathbb{E}[S] = 2.514$ while $\sigma = 3.559$. Here $\bar X$ and $S^2$ are dependent: $S^2 = 32$ forces $\bar X = 5$.

**Counts.** For iid Bernoulli$(p)$ data, $n\bar X$ has the Binomial$(n, p)$ law exactly. Its standard error is $\sqrt{p(1-p)/n}$ on the scale of $\bar X$.

**The maximum.** For iid Uniform$(0, \theta)$ data, $P_\theta(\max_i X_i \le t) = (t/\theta)^n$ for $0 \le t \le \theta$. The law piles up just below $\theta$, with a spread of order $1/n$, not $1/\sqrt n$.

**No concentration.** For iid Cauchy data, $\bar X$ has the same standard Cauchy law for every $n$ (by the characteristic function $e^{-\lvert s \rvert}$). The sampling distribution does not narrow, so $\bar X$ is not consistent for the center, while the sample median is.

## Where it is used

- **Properties of estimators.** [Bias](/estimator-bias/), [standard error](/standard-error/), [mean squared error](/mean-squared-error/) and [consistency](/consistent-estimator/) are each a property of the sampling distribution.
- **Intervals.** A [confidence interval](/confidence-interval/) has its coverage over the sampling distribution at a fixed $\theta$.
- **Tests.** The null distribution of a test statistic is its sampling distribution under the null hypothesis, and a [p-value](/p-value/) is a tail probability of it.
- **Survey sampling.** In design-based inference the population values are fixed, and the randomness comes only from which units the design selects. The [Horvitz-Thompson estimator](/horvitz-thompson-estimator/) is unbiased over that sampling distribution.
- **The Bayesian contrast.** A posterior distribution is conditional on the observed data and treats $\theta$ as random. It is not a sampling distribution, and the two answer different questions.

## References
