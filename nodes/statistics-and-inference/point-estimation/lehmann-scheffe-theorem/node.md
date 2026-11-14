---
tag: QKMW8P
kind: theorem
slug: lehmann-scheffe-theorem
name: Lehmann-Scheffe theorem
aliases:
- Lehmann-Scheffe uniqueness theorem
area: statistics-and-inference/point-estimation
level: core
summary: An unbiased estimator that is a function of a complete sufficient statistic is the unique minimum variance unbiased estimator.
prereqs: [complete-statistic, rao-blackwell-theorem, minimum-variance-unbiased-estimator]
see_also: [sufficient-statistic, cramer-rao-bound, admissible-estimator, estimator-bias, exponential-family-distribution]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 7.3.3, Theorem 7.3.23 (an unbiased function of a complete sufficient statistic is the unique best unbiased estimator)
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 2, Section 2.1 (UMVU estimators through complete sufficient statistics, with the convex loss version)
  - paper: "E. L. Lehmann and Henry Scheffé, Completeness, similar regions, and unbiased estimation, Part I, Sankhya 10 (1950)"
    title: Lehmann and Scheffé 1950
    locator: completeness and the uniqueness of unbiased estimators that depend on a complete sufficient statistic
  - paper: "E. L. Lehmann and Henry Scheffé, Completeness, similar regions, and unbiased estimation, Part II, Sankhya 15 (1955)"
    title: Lehmann and Scheffé 1955
    locator: the continuation of Part I
---

The Lehmann-Scheffé theorem says that if $T$ is a [complete](/complete-statistic/) [sufficient statistic](/sufficient-statistic/) and $\delta(T)$ is an unbiased estimator of $\psi(\theta)$, then $\delta(T)$ is the unique [minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/) (UMVUE) of $\psi(\theta)$. Combined with the [Rao-Blackwell theorem](/rao-blackwell-theorem/), it gives a recipe: take any unbiased estimator and condition it on $T$. Lehmann and Scheffé proved it in 1950. In most textbook models, which are full-rank exponential families, it settles the question of the best unbiased estimator.

## Statement

Let $X$ have distribution $P_\theta$, $\theta \in \Theta$, and let $T = t(X)$ be complete and sufficient for $\theta$.

**Theorem.**

1. If $\delta(T)$ is a function of $T$ with $\mathbb{E}_\theta\, \delta(T) = \psi(\theta)$ and $\operatorname{Var}_\theta\, \delta(T) < \infty$ for every $\theta$, then $\delta(T)$ is a UMVUE of $\psi(\theta)$, and every UMVUE of $\psi(\theta)$ equals $\delta(T)$ with probability 1.
2. If $\delta_0(X)$ is any unbiased estimator of $\psi(\theta)$ with finite variance, then $\mathbb{E}[\delta_0(X) \mid T]$ is the UMVUE.
3. **Convex loss.** If the loss $L(\theta, d)$ is convex in $d$, then $\delta(T)$ has the smallest risk among all unbiased estimators of $\psi(\theta)$ with finite risk; if $L$ is strictly convex in $d$, it is the unique such estimator.

## In plain words

Some summaries of the data are both complete and sufficient: they keep all the information about the unknown quantity, and no two different formulas in them have the same average for every value of that quantity. If you find a formula in such a summary that is right on average, you are done. No other estimate that is right on average has a smaller spread, at any value of the unknown quantity. To find the formula, start from any estimate that is right on average, however simple, and average it over the data sets that share the summary.

## Proof

**Part 1.** Let $\delta'(X)$ be any unbiased estimator of $\psi(\theta)$ with finite variance, and let $\eta'(T) = \mathbb{E}[\delta'(X) \mid T]$. By sufficiency $\eta'$ is a statistic, and by the Rao-Blackwell theorem it is unbiased with

$$\operatorname{Var}_\theta(\eta') = \operatorname{Var}_\theta(\delta') - \mathbb{E}_\theta \operatorname{Var}(\delta' \mid T) \le \operatorname{Var}_\theta(\delta') \qquad \text{for every } \theta.$$

Both $\eta'(T)$ and $\delta(T)$ are unbiased for $\psi(\theta)$, so $g(T) = \eta'(T) - \delta(T)$ has $\mathbb{E}_\theta\, g(T) = 0$ for every $\theta$. By completeness, $g(T) = 0$ with probability 1, so $\eta'(T) = \delta(T)$. Hence

$$\operatorname{Var}_\theta(\delta(T)) = \operatorname{Var}_\theta(\eta') \le \operatorname{Var}_\theta(\delta') \qquad \text{for every } \theta,$$

and $\delta(T)$ is a UMVUE. If $\delta'$ is also a UMVUE, the inequality is an equality at every $\theta$, so $\mathbb{E}_\theta \operatorname{Var}(\delta' \mid T) = 0$ and $\delta' = \eta'(T) = \delta(T)$ with probability 1.

**Part 2.** $\mathbb{E}[\delta_0 \mid T]$ is an unbiased function of $T$ with finite variance (by the Rao-Blackwell theorem), so part 1 applies to it.

**Part 3.** Repeat the proof of part 1 with risk in place of variance. The Rao-Blackwell theorem for convex loss gives $R(\theta, \eta') \le R(\theta, \delta')$, and completeness gives $\eta' = \delta(T)$, so $R(\theta, \delta(T)) \le R(\theta, \delta')$. With strict convexity, equality forces $\delta' = \eta'(T)$ with probability 1. $\blacksquare$

## Consequences

**Worked UMVUEs.** In each case $T$ is complete and sufficient (see [complete statistic](/complete-statistic/)), and the estimator is unbiased, so it is the UMVUE.

- **Bernoulli$(p)$, $T = \sum_i X_i$.** $\bar X$ for $p$. For $p^k$ with $k \le n$, the estimator $\frac{T(T-1)\cdots(T-k+1)}{n(n-1)\cdots(n-k+1)}$, which is the conditional probability that the first $k$ trials are all successes given $T$. For $p(1-p)$, $T(n-T)/(n(n-1))$, the Rao-Blackwellized form of $X_1(1 - X_2)$.
- **Poisson$(\lambda)$, $T = \sum_i X_i$.** $\bar X$ for $\lambda$. For $e^{-\lambda} = P(X_1 = 0)$, $(1 - 1/n)^T$, the Rao-Blackwellized form of $\mathbf{1}\{X_1 = 0\}$.
- **$N(\mu, \sigma^2)$, $T = (\bar X, S^2)$.** $\bar X$ for $\mu$; $S^2$, with divisor $n - 1$, for $\sigma^2$; $\bar X^2 - S^2/n$ for $\mu^2$, because $\mathbb{E}\,\bar X^2 = \mu^2 + \sigma^2/n$.
- **Uniform$(0, \theta)$, $T = \max_i X_i$.** $\mathbb{E}_\theta T = n\theta/(n+1)$, so $\frac{n+1}{n}\max_i X_i$ is the UMVUE of $\theta$.

**The method does not depend on the start.** Any unbiased starting estimator gives the same answer after conditioning on $T$. For the normal variance, the crude estimator $(X_1 - X_2)^2/2$ is unbiased, and its conditional expectation given $(\bar X, S^2)$ is $S^2$. The same holds for every other unbiased estimator of $\sigma^2$ with finite variance.

**Exponential families.** In a full-rank exponential family, $\sum_i T(X_i)$ is complete and sufficient, so every estimand that has an unbiased estimator has a UMVUE, and it is the unique unbiased function of $\sum_i T(X_i)$.

## Tightness

**Completeness is needed for uniqueness.** In the curved family $N(\theta, \theta^2)$, $\theta > 0$, the minimal sufficient statistic $(\bar X, S^2)$ is not complete: $g = \frac{n}{n+1}\bar X^2 - S^2$ has mean zero. Then $\bar X$ and $\bar X + a g$ are different unbiased functions of the same sufficient statistic for every $a \ne 0$, and the theorem says nothing about which is better.

**An unbiased estimator must exist.** If $X$ is Binomial$(n, p)$, no unbiased estimator of $1/p$ exists, because $\mathbb{E}_p\, \delta(X)$ is a polynomial in $p$ of degree at most $n$. The theorem then has nothing to find.

**The UMVUE can be a poor estimator.** For one Poisson$(\lambda)$ observation $X$, $(-1)^X$ is unbiased for $e^{-2\lambda}$ and $X$ is complete, so $(-1)^X$ is the UMVUE. It takes the values $\pm 1$ although $e^{-2\lambda} \in (0, 1)$.

**Best unbiased is not best.** The theorem compares unbiased estimators only. In the normal model, $S^2$ is the UMVUE of $\sigma^2$, with mean squared error $2\sigma^4/(n-1)$. The biased estimator $\sum_i (X_i - \bar X)^2/(n+1)$ has mean squared error $2\sigma^4/(n+1)$, smaller at every $(\mu, \sigma^2)$: at $n = 5$, $\sigma^4/3$ against $\sigma^4/2$. So the UMVUE can be [inadmissible](/admissible-estimator/).

**Relation to the Cramér-Rao bound.** The UMVUE given by the theorem can have variance above the [Cramér-Rao bound](/cramer-rao-bound/); then no unbiased estimator attains the bound. For Poisson data with $n = 5$ and $\lambda = 1$, the UMVUE $(1 - 1/n)^T$ of $e^{-\lambda}$ has variance about $0.02996$, and the bound is about $0.02707$.

## History

Lehmann and Scheffé (1950) defined completeness and proved that an unbiased estimator depending only on a complete sufficient statistic has minimum variance among all unbiased estimators, and is unique. Part II (1955) continued the work. The result built on the [Rao-Blackwell theorem](/rao-blackwell-theorem/) of Rao (1945) and Blackwell (1947), which gives the improvement step but not uniqueness.

## References
