---
tag: 74RKSV
kind: definition
slug: standard-error
name: Standard error
aliases:
- standard error of the mean
area: statistics-and-inference/point-estimation
level: intro
summary: The standard deviation of the sampling distribution of an estimator, or an estimate of it. For the sample mean it is sigma divided by the square root of n.
prereqs: [estimator, sampling-distribution, variance]
see_also: [estimator-bias, sample-variance, mean-squared-error, confidence-interval, t-confidence-interval, delta-method, bootstrap-method, horvitz-thompson-estimator]
sources:
  - book: isbn:9780387402727
    title: Larry Wasserman, All of Statistics, Springer, 2004
    locator: Section 6.3 (the standard error and the estimated standard error of a point estimator)
  - book: isbn:9780412042317
    title: Bradley Efron and Robert J. Tibshirani, An Introduction to the Bootstrap, Chapman and Hall, 1993
    locator: Chapter 5 (standard errors and estimated standard errors) and Chapter 6 (the bootstrap estimate of standard error)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 5.2 (the mean and variance of the sample mean) and Section 10.1.4 (bootstrap standard errors)
  - book: isbn:9780521496032
    title: A. W. van der Vaart, Asymptotic Statistics, Cambridge University Press, 1998
    locator: Section 21.2 (asymptotic normality of sample quantiles)
---

The standard error of an [estimator](/estimator/) is the standard deviation of its [sampling distribution](/sampling-distribution/): how far the estimate typically moves from one sample to the next. It depends on the unknown parameter, so in practice it is itself estimated, and the reported number is an *estimated* standard error. For the sample mean of $n$ iid observations with standard deviation $\sigma$, the standard error is $\sigma/\sqrt n$, estimated by $S/\sqrt n$.

## Definition

Let $T$ be an estimator of $\psi(\theta)$ with $\mathbb{E}_\theta[T^2] < \infty$ for every $\theta \in \Theta$.

- **Standard error.** $\operatorname{se}_\theta(T) = \sqrt{\operatorname{Var}_\theta(T)}$, a function of $\theta$. It measures the spread of $T$ around its own mean $\mathbb{E}_\theta[T]$, not around $\psi(\theta)$; the distance to the target is the [bias](/estimator-bias/). The [mean squared error](/mean-squared-error/) combines them: $\mathbb{E}_\theta[(T - \psi(\theta))^2] = \operatorname{se}_\theta(T)^2 + \operatorname{bias}_\theta(T)^2$.
- **Estimated standard error.** A statistic $\widehat{\operatorname{se}}$ that estimates $\operatorname{se}_\theta(T)$. The plug-in choice is $\operatorname{se}_{\hat\theta}(T)$, the formula evaluated at an estimate $\hat\theta$. Other choices are the [delta method](/delta-method/), the sandwich formula of [M-estimators](/m-estimator/), the inverse [Fisher information](/fisher-information-matrix/) for maximum likelihood, and the [bootstrap](/bootstrap-method/), which needs no formula.

**The standard error of the mean.** Let $X_1, \ldots, X_n$ be uncorrelated with common mean $\mu$ and common variance $\sigma^2 < \infty$. Then

$$\operatorname{Var}(\bar X) = \frac{1}{n^2} \operatorname{Var}\Big(\sum_{i=1}^n X_i\Big) = \frac{1}{n^2} \sum_{i=1}^n \sum_{j=1}^n \operatorname{Cov}(X_i, X_j) = \frac{n \sigma^2}{n^2} = \frac{\sigma^2}{n},$$

because the terms with $i \ne j$ are zero. So $\operatorname{se}(\bar X) = \sigma/\sqrt n$. Iid data with finite variance meet the condition. The usual estimate is $S/\sqrt n$, with $S^2$ the [sample variance](/sample-variance/) (divisor $n - 1$). Since $S$ is biased downward for $\sigma$, $S/\sqrt n$ is biased downward for $\sigma/\sqrt n$, although $S^2/n$ is unbiased for $\sigma^2/n$.

The factor $1/\sqrt n$ means that four times the data halve the standard error. This rate is typical of estimators that are smooth functions of averages, but it is not universal: the unbiased estimator $\frac{n+1}{n}\max_i X_i$ of $\theta$ for Uniform$(0, \theta)$ data has standard error $\theta/\sqrt{n(n + 2)}$, of order $1/n$. (The ratio $\max_i X_i/\theta$ has density $n u^{n-1}$ on $[0, 1]$, with mean $\frac{n}{n+1}$ and variance $\frac{n}{(n+1)^2(n+2)}$; multiply the variance by $(\frac{n+1}{n})^2\theta^2$.)

## Examples and non-examples

**A sample of five.** For $x = (3, 7, 7, 9, 14)$, $\bar x = 8$ and $S^2 = 64/4 = 16$, so $S = 4$ and $\widehat{\operatorname{se}}(\bar X) = 4/\sqrt 5 = 1.7889$. The number $4$ describes the spread of one observation. The number $1.7889$ describes the spread of the mean of five observations.

**A proportion.** For $n$ iid Bernoulli$(p)$ trials, $\operatorname{se}(\hat p) = \sqrt{p(1 - p)/n}$, with $\hat p = \bar X$. With 37 successes in 100 trials, the plug-in estimate is $\sqrt{0.37 \cdot 0.63 / 100} = 0.0483$.

**A difference of independent estimators.** If $T_1$ and $T_2$ are independent, $\operatorname{se}(T_1 - T_2) = \sqrt{\operatorname{se}(T_1)^2 + \operatorname{se}(T_2)^2}$, because the covariance term is zero. For two independent sample means this is $\sqrt{\sigma_1^2/n_1 + \sigma_2^2/n_2}$.

**The median has a different standard error.** If the distribution function $F$ is differentiable at the median $m$ with $F'(m) = f(m) > 0$, the sample [median](/median/) is asymptotically normal with standard error about $1/(2 f(m) \sqrt n)$. For normal data $f(m) = 1/(\sigma\sqrt{2\pi})$, which gives $\sqrt{\pi/2}\,\sigma/\sqrt n = 1.2533\,\sigma/\sqrt n$, about 25 percent more than the mean. For heavy-tailed data the order can reverse.

**Under random sampling from a finite population.** For a simple random sample of $n$ units drawn without replacement from $N$, the standard error of the sample mean has the extra factor $\sqrt{1 - n/N}$. The [Horvitz-Thompson estimator](/horvitz-thompson-estimator/) page gives the general design-based variance.

**Non-example: the standard deviation of the data.** $S$ estimates the spread of one observation, $\sigma$. It is not the standard error of $\bar X$, and it does not shrink as $n$ grows.

**Non-example: $\sigma/\sqrt n$ for correlated data.** If $X_1, X_2, \ldots$ is stationary with variance $\sigma^2$ and $\operatorname{Cov}(X_i, X_j) = \sigma^2 \rho^{\lvert i - j \rvert}$, $\lvert \rho \rvert < 1$, the double sum above gives

$$\operatorname{Var}(\bar X) = \frac{\sigma^2}{n}\Big(1 + 2 \sum_{h=1}^{n-1} \Big(1 - \frac{h}{n}\Big) \rho^h\Big) \to \frac{\sigma^2}{n} \cdot \frac{1 + \rho}{1 - \rho} \quad \text{in ratio, as } n \to \infty.$$

For $\rho = 0.5$ the factor in parentheses is $2.225$ at $n = 5$, $2.96$ at $n = 100$, and tends to $3$. The iid formula then understates the standard error by a factor of about $\sqrt 3 = 1.73$.

**Non-example: infinite variance.** For iid Cauchy data $\bar X$ has the same Cauchy law for every $n$. It has no variance, so it has no standard error, and $S/\sqrt n$ estimates nothing.

## Related definitions

- [Sampling distribution](/sampling-distribution/): the standard error is its standard deviation.
- [Bias of an estimator](/estimator-bias/) and [mean squared error](/mean-squared-error/): the other parts of the error.
- [Confidence interval](/confidence-interval/): intervals of the form estimate $\pm$ quantile $\times$ estimated standard error. Under normal iid data, $\bar X \pm t_{(n-1, 0.975)} S/\sqrt n$ is the exact [t interval](/t-confidence-interval/).
- [Delta method](/delta-method/): $\operatorname{se}(g(T)) \approx \lvert g'(\theta) \rvert \operatorname{se}(T)$ for a smooth $g$ with $g'(\theta) \ne 0$.
- [Bootstrap](/bootstrap-method/) and [jackknife](/jackknife-resampling/): estimated standard errors by resampling.

## References
