---
tag: 7FMKF0
kind: definition
slug: estimator-bias
name: Bias of an estimator
aliases:
- unbiased estimator
- estimator bias
area: statistics-and-inference/point-estimation
level: intro
summary: The difference between the expected value of an estimator and the true parameter. An estimator is unbiased when this difference is zero for every parameter.
prereqs: [estimator, sampling-distribution, linearity-of-expectation]
see_also: [mean-squared-error, bias-variance-tradeoff, standard-error, sample-variance, consistent-estimator, minimum-variance-unbiased-estimator, jackknife-resampling, horvitz-thompson-estimator]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 7.3.1 (bias and mean squared error of a point estimator) and Section 7.3.2 (best unbiased estimators)
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 2 (unbiasedness, U-estimable functions and their absence)
  - book: isbn:9780387402727
    title: Larry Wasserman, All of Statistics, Springer, 2004
    locator: Section 6.3 (bias, unbiasedness and the decomposition of the mean squared error)
---

The bias of an [estimator](/estimator/) $T$ of $\psi(\theta)$ is $\mathbb{E}_\theta[T] - \psi(\theta)$, the distance from the center of its [sampling distribution](/sampling-distribution/) to the target, as a function of the true parameter $\theta$. An estimator is unbiased when its bias is zero at every $\theta$ in the parameter space. Bias is the location part of the error; the [standard error](/standard-error/) is the spread part, and the [mean squared error](/mean-squared-error/) adds the two as variance plus squared bias.

## Definition

Let $X_1, \ldots, X_n$ have a law $P_\theta$ with $\theta \in \Theta$, and let $T = t(X_1, \ldots, X_n)$ be an estimator of $\psi(\theta) \in \mathbb{R}$ with $\mathbb{E}_\theta \lvert T \rvert < \infty$ for every $\theta \in \Theta$.

- **Bias.** $\operatorname{bias}_\theta(T) = \mathbb{E}_\theta[T] - \psi(\theta)$. It is a function of $\theta$, not a number.
- **Unbiased.** $T$ is unbiased for $\psi(\theta)$ if $\mathbb{E}_\theta[T] = \psi(\theta)$ for every $\theta \in \Theta$. Zero bias at one $\theta$ is not enough: the constant $T \equiv \psi(\theta_0)$ has zero bias at $\theta_0$.
- **U-estimable.** $\psi$ is U-estimable if at least one unbiased estimator of $\psi(\theta)$ exists.
- **Asymptotically unbiased.** A sequence $T_n$ is asymptotically unbiased if $\operatorname{bias}_\theta(T_n) \to 0$ as $n \to \infty$, for every $\theta$.
- **Median-unbiased.** $T$ is median-unbiased if $P_\theta(T \le \psi(\theta)) \ge \frac12$ and $P_\theta(T \ge \psi(\theta)) \ge \frac12$ for every $\theta$. This needs no finite mean.
- **Vector estimands.** For $\psi(\theta) \in \mathbb{R}^k$ the bias is the vector $\mathbb{E}_\theta[T] - \psi(\theta)$, coordinate by coordinate.

**Relation to the mean squared error.** If $\mathbb{E}_\theta[T^2] < \infty$, then $\mathbb{E}_\theta[(T - \psi(\theta))^2] = \operatorname{Var}_\theta(T) + \operatorname{bias}_\theta(T)^2$. The proof is on [mean squared error](/mean-squared-error/). So among unbiased estimators the mean squared error is the variance, and a biased estimator with a smaller variance can have the smaller mean squared error. That page shows it for the variance of normal data with the divisors $n - 1$, $n$ and $n + 1$.

**Bias under a change of target.** By [linearity of expectation](/linearity-of-expectation/), if $T$ is unbiased for $\psi(\theta)$ then $aT + b$ is unbiased for $a\psi(\theta) + b$. A nonlinear function does not keep unbiasedness. If $g$ is strictly convex, $T$ is unbiased for $\psi(\theta)$, and $T$ is not constant under $P_\theta$, then by Jensen's inequality $\mathbb{E}_\theta[g(T)] > g(\mathbb{E}_\theta[T]) = g(\psi(\theta))$, so $g(T)$ is biased upward for $g(\psi(\theta))$. For a strictly concave $g$, such as the square root, the bias is downward.

## Examples and non-examples

**The sample mean.** If $\mathbb{E}_\theta \lvert X_1 \rvert < \infty$ and $\mu = \mathbb{E}_\theta[X_1]$, then $\mathbb{E}_\theta[\bar X] = \frac1n \sum_i \mathbb{E}_\theta[X_i] = \mu$, so $\bar X$ is unbiased for $\mu$. No independence is needed, only equal means.

**The two divisors of the variance.** The [sample variance](/sample-variance/) $S^2$ with divisor $n - 1$ is unbiased for $\sigma^2$ when the variance is finite. The version with divisor $n$ has expectation $\frac{n-1}{n}\sigma^2$, so its bias is $-\sigma^2/n$. It is biased, and asymptotically unbiased.

**$S$ is biased for $\sigma$.** The square root is strictly concave, so $\mathbb{E}[S] < \sigma$ whenever $S^2$ is unbiased and not constant. For iid $N(\mu, \sigma^2)$ data, $Y = (n - 1)S^2/\sigma^2$ has the chi-square law with $k = n - 1$ degrees of freedom, and

$$\mathbb{E}\big[\sqrt{Y}\big] = \int_0^\infty \frac{y^{1/2}\, y^{k/2 - 1} e^{-y/2}}{2^{k/2}\,\Gamma(k/2)}\,dy = \frac{2^{(k+1)/2}\,\Gamma\big(\tfrac{k+1}{2}\big)}{2^{k/2}\,\Gamma\big(\tfrac{k}{2}\big)} = \sqrt2\, \frac{\Gamma(n/2)}{\Gamma((n-1)/2)}.$$

So $\mathbb{E}[S] = c_4(n)\,\sigma$ with $c_4(n) = \sqrt{2/(n - 1)}\; \Gamma(n/2) / \Gamma((n - 1)/2)$. The values are $c_4(2) = 0.7979$, $c_4(5) = 0.9400$ and $c_4(10) = 0.9727$. The ratio $S/c_4(n)$ is unbiased for $\sigma$ under normality only.

**A square of an unbiased estimator.** Let $X_1, X_2$ be iid Bernoulli$(p)$ and estimate $p^2$. Write $q = 1 - p$.

| $(x_1, x_2)$ | probability | $\bar x^2$ | $x_1 x_2$ |
|---|---|---|---|
| $(0, 0)$ | $q^2$ | $0$ | $0$ |
| $(0, 1)$ or $(1, 0)$ | $2pq$ | $1/4$ | $0$ |
| $(1, 1)$ | $p^2$ | $1$ | $1$ |

So $\mathbb{E}[\bar X^2] = \frac{2pq}{4} + p^2 = p^2 + \frac{p(1-p)}{2}$: the plug-in estimator $\bar X^2$ has bias $p(1-p)/2$, as the convexity argument predicts. The product $X_1 X_2$ has expectation $p^2$ and is unbiased.

**The maximum of a uniform sample.** For iid Uniform$(0, \theta)$ data, $M = \max_i X_i$ has $P(M \le t) = (t/\theta)^n$ for $0 \le t \le \theta$, so $\mathbb{E}[M] = \int_0^\theta (1 - (t/\theta)^n)\,dt = \frac{n}{n+1}\theta$. The bias is $-\theta/(n + 1)$, and $\frac{n + 1}{n} M$ is unbiased.

**Non-example: no unbiased estimator exists.** Let $X$ be Binomial$(n, p)$ with $p \in (0, 1)$, and let $\psi(p) = 1/p$. Any estimator is $t(X)$ for some function $t$ on $\{0, \ldots, n\}$, and $\mathbb{E}_p[t(X)] = \sum_{k=0}^{n} t(k) \binom{n}{k} p^k (1 - p)^{n - k}$ is a polynomial in $p$. A polynomial is bounded on $(0, 1)$, while $1/p \to \infty$ as $p \to 0$. So $1/p$ is not U-estimable.

**Non-example: unbiased but outside the range.** Unbiasedness does not keep an estimate inside $\psi(\Theta)$. The [Horvitz-Thompson estimator](/horvitz-thompson-estimator/) of a population proportion is unbiased, and it can exceed 1.

## Related definitions

- [Mean squared error](/mean-squared-error/) and the [bias-variance tradeoff](/bias-variance-tradeoff/): how bias and variance add in the squared error.
- [Standard error](/standard-error/): the standard deviation of the sampling distribution, the other part of the error.
- [Consistent estimator](/consistent-estimator/): a large-sample property. A consistent estimator can be biased at every $n$ (the divisor-$n$ variance), and an unbiased estimator can fail to be consistent ($T_n = X_1$).
- [Minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/): the best estimator inside the class of unbiased ones, when it exists.
- [Jackknife](/jackknife-resampling/) and [bootstrap](/bootstrap-method/): ways to estimate the bias of an estimator from the data.

## References
