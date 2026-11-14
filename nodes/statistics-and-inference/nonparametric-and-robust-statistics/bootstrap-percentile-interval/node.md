---
tag: 3JWEPT
kind: algorithm
slug: bootstrap-percentile-interval
name: Bootstrap percentile interval
aliases:
- percentile bootstrap
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: A confidence interval whose endpoints are the alpha/2 and 1 - alpha/2 quantiles of the bootstrap replicates of the statistic. Simple and transformation respecting, but only first-order accurate.
model: real-ram
complexity:
  vars: {n: the sample size, b: the number of bootstrap replicates}
  time: {worst: Θ(b n + b log b), best: Θ(b n)}
  space: {extra: Θ(b + n)}
properties: {deterministic: false, randomized: true, exact: false, online: false, recursive: false}
history:
  year: 1979
  people: [Bradley Efron]
  note: Efron proposed the bootstrap in 1979 and the percentile interval soon after, with its justification through a normalizing transformation.
prereqs: [bootstrap-method, confidence-interval, quantile, order-statistic]
see_also: [bootstrap-t-interval, bca-bootstrap-interval, t-confidence-interval, quickselect, test-interval-duality, subsampling-inference, phylogenetic-bootstrap, parametric-bootstrap]
sources:
  - book: isbn:9780412042317
    title: Bradley Efron and Robert J. Tibshirani, An Introduction to the Bootstrap, Chapman and Hall, 1993
    locator: Chapter 13 (confidence intervals based on bootstrap percentiles, and the transformation-respecting property) and Chapter 22 (further topics in bootstrap confidence intervals, the orders of accuracy)
  - book: isbn:9780521574716
    title: A. C. Davison and D. V. Hinkley, Bootstrap Methods and their Application, Cambridge University Press, 1997
    locator: Chapter 5 (confidence intervals, the basic and the percentile methods, and their coverage)
  - paper: doi:10.1214/aos/1176350933
    title: Peter Hall, Theoretical comparison of bootstrap confidence intervals, The Annals of Statistics 16(3), 1988
    locator: pp. 927 to 953 (the percentile interval is first-order accurate, and the studentized and BCa intervals are second-order accurate)
  - book: isbn:9780387977201
    title: Peter Hall, The Bootstrap and Edgeworth Expansion, Springer, 1992
    locator: Chapter 3 (an Edgeworth view of the bootstrap, the coverage error of percentile intervals)
  - paper: doi:10.1214/aos/1176344552
    title: Bradley Efron, Bootstrap methods, another look at the jackknife, The Annals of Statistics 7(1), 1979
    locator: pp. 1 to 26 (the bootstrap distribution of a statistic)
---

The bootstrap percentile interval is the simplest bootstrap [confidence interval](/confidence-interval/). Draw $b$ [bootstrap](/bootstrap-method/) samples, compute the statistic $\hat\theta^*$ on each, and take the $\alpha/2$ and $1 - \alpha/2$ [quantiles](/quantile/) of the $b$ values as the endpoints. The interval needs no standard error formula, it follows the skewness of the bootstrap distribution, and it respects monotone transformations: the interval for $\log\theta$ is the log of the interval for $\theta$. Its coverage error for each endpoint is of order $n^{-1/2}$, so it is first-order accurate, and its coverage is a measured property, not a proved one.

## In plain words

You computed an average from ten numbers and want a range of plausible values for the true average. Make two thousand bootstrap samples by drawing ten numbers from your data with replacement, and compute the average of each. Sort the two thousand averages. Cut off the lowest 2.5% and the highest 2.5%. The smallest and the largest of the averages that are left are the ends of a 95% interval.

If the bootstrap averages have a long tail to the right, the interval is longer on the right too, which a "plus or minus" interval cannot do. The method is easy, but with small samples it often covers the true value less often than it claims.

## The problem

**Input.** A sample $x_1, \ldots, x_n$, independent and identically distributed from an unknown $F$; a statistic $s$ with $\hat\theta = s(x)$, which estimates $\theta = t(F)$; a level $\alpha \in (0, 1)$; and a number of replicates $b$.

**Output.** An interval $[L, U]$ that should contain $\theta$ with probability close to $1 - \alpha$.

**Definition.** Let $G$ be the bootstrap distribution function of $\hat\theta^*$, the law of $s(X^*)$ when $X^*$ is a sample of size $n$ from $\hat F_n$. With the generalized inverse $G^{-1}(p) = \inf\{t : G(t) \ge p\}$, the ideal percentile interval is

$$[\,G^{-1}(\alpha/2),\ G^{-1}(1 - \alpha/2)\,].$$

The algorithm replaces $G$ by the empirical distribution $\hat G_b$ of $b$ Monte Carlo replicates.

## The algorithm

```pseudo id=main
PERCENTILE-INTERVAL(x_1, ..., x_n, s, α, b)
L1  for j ← 1 to b do
L2      x* ← n independent draws from x_1 .. x_n, each with probability 1/n
L3      θ*_j ← s(x*)
L4  sort θ*_1, ..., θ*_b into θ*_(1) ≤ ... ≤ θ*_(b)
L5  L ← θ*_(k), k = max(1, ⌈b α/2⌉)
L6  U ← θ*_(k'), k' = ⌈b (1 - α/2)⌉
L7  return [L, U]
```

Lines L5 and L6 compute $\hat G_b^{-1}(p)$ exactly: the empirical distribution of $b$ values reaches $p$ for the first time at the $\lceil b p \rceil$-th smallest value. The code converts $p$ to a fraction before the ceiling, so that $b p$ is not rounded to a value just above an integer. Two quick selections, as in [quickselect](/quickselect/), can replace the sort of line L4.

## Example

Take the right-skewed sample of $n = 10$ values

$$0.4,\ 0.9,\ 1.3,\ 1.6,\ 2.2,\ 2.8,\ 3.5,\ 4.9,\ 7.6,\ 13.1,$$

with mean $\bar x = 3.83$, $S = 3.90$ and $S/\sqrt{10} = 1.233$. Let $s$ be the mean, $\alpha = 0.05$ and $b = 2000$, with `random.Random(1)`. Lines L5 and L6 use $k = \lceil 2000 \cdot 0.025 \rceil = 50$ and $k' = \lceil 2000 \cdot 0.975 \rceil = 1950$. The 50th smallest replicate is 1.80 and the 1950th is 6.31, so the interval is

$$[1.80,\ 6.31].$$

It reaches $2.48$ above $\bar x$ and $2.03$ below, which follows the right skew of the data. On the same data, the [t interval](/t-confidence-interval/) is $[1.04, 6.62]$, the normal interval $\bar x \pm 1.96 \cdot \widehat{se}_{boot}$ with the bootstrap standard error $1.172$ is $[1.53, 6.13]$, the [bootstrap-t interval](/bootstrap-t-interval/) is $[1.82, 10.27]$, and the [BCa interval](/bca-bootstrap-interval/) is $[2.18, 6.97]$, all with the same seed.

**Transformation.** Running the same code with the statistic $\log \bar x$ and the same seed gives the interval $[\log 1.80, \log 6.31]$ exactly, because the logarithm does not change the order of the replicates. The tests check this, and also that the statistic $-\bar x$ gives $[-U, -L]$ when $b = 999$ and $\alpha = 0.1$, where the two order statistics $k = 50$ and $k' = 950$ are mirror images. For a decreasing transformation, other choices of $b$ can move an endpoint by one order statistic.

**Measured coverage.** For samples from the exponential law with mean 1, 1000 data sets of each size with $b = 1000$ (seeds 101 and 102) gave these coverages for the true mean at the nominal level 0.95:

| method | $n = 10$ | $n = 20$ |
|---|---|---|
| percentile | 0.869 | 0.911 |
| t interval | 0.911 | 0.924 |
| bootstrap-t | 0.943 | 0.950 |
| BCa | 0.884 | 0.916 |

The percentile interval misses mostly on one side: at $n = 10$ its upper end was below the true mean in $10.9\%$ of the data sets and its lower end above it in $2.2\%$. The Monte Carlo standard error of each coverage is about $0.007$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). What is proved:

- Lines L5 and L6 return $\hat G_b^{-1}(\alpha/2)$ and $\hat G_b^{-1}(1 - \alpha/2)$, and as $b \to \infty$ they converge to the ideal endpoints $G^{-1}(\alpha/2)$ and $G^{-1}(1 - \alpha/2)$ wherever $G$ is strictly increasing at these quantiles.
- The interval respects transformations: for a strictly increasing $g$, the interval computed for $g(\hat\theta)$ is $[g(L), g(U)]$.
- If there is an increasing transformation $\phi$ such that $\phi(\hat\theta) - \phi(\theta)$ has a continuous distribution $H$ that is symmetric about 0 and does not depend on $F$, and the bootstrap reproduces it, so that $\phi(\hat\theta^*) - \phi(\hat\theta)$ also has law $H$, then the ideal percentile interval has coverage exactly $1 - \alpha$. The method does not need to know $\phi$.

What is not proved: the coverage for a real $F$. The normalizing transformation exists only approximately, and the coverage error of each endpoint is of order $n^{-1/2}$ (Hall 1988). The table above is a measurement.

## Complexity

Each of the $b$ replicates draws $n$ indices and evaluates the statistic, which for the mean costs $\Theta(n)$. The sort of line L4 costs $\Theta(b \log b)$. So the time is $\Theta(b n + b \log b)$, and $\Theta(b n)$ with two linear-time selections instead of the sort. The replicates take $\Theta(b)$ space and one resample $\Theta(n)$. For a statistic that costs $C_s(n)$, replace $n$ by $C_s(n)$ in the first term.

## Properties

- **Transformation respecting.** The interval for $g(\theta)$ is $g$ applied to the interval for $\theta$, for every strictly increasing $g$. The [t interval](/t-confidence-interval/) and the normal interval do not have this property.
- **Range preserving.** The endpoints are values that the statistic takes, so an interval for a correlation stays in $[-1, 1]$ and one for a variance stays positive.
- **First-order accurate.** The coverage error of each one-sided endpoint is $O(n^{-1/2})$. In an equal-tailed two-sided interval the leading errors of the two ends partly cancel, but the interval can still be badly unbalanced, as the table shows.
- **Too narrow in small samples.** For the mean, the bootstrap distribution has variance $\frac{n-1}{n} S^2/n$ and uses normal-like quantiles instead of $t$ quantiles, so the interval is short by a factor of about $\sqrt{(n-1)/n} \cdot z_{0.975}/t_{n-1, 0.975}$, which is $0.82$ for $n = 10$.
- **Monte Carlo error.** The endpoints are extreme order statistics of the replicates, so they need more replicates than a standard error: use $b \ge 1000$, and better $2000$ or more.

## Variants and improvements

- **Basic (reverse percentile) interval.** $[2\hat\theta - G^{-1}(1 - \alpha/2),\ 2\hat\theta - G^{-1}(\alpha/2)]$. It assumes that $\hat\theta - \theta$ and $\hat\theta^* - \hat\theta$ have the same law, so it reflects the skewness the other way. It is not transformation respecting.
- **BCa interval.** Moves the two levels $\alpha/2$ and $1 - \alpha/2$ to correct for bias and skewness, keeps the transformation-respecting property, and is second-order accurate; see the [BCa interval](/bca-bootstrap-interval/).
- **Bootstrap-t interval.** Studentizes each replicate; second-order accurate when a good standard error is available; see the [bootstrap-t interval](/bootstrap-t-interval/).
- **Ideal percentile interval.** For small $n$ the bootstrap distribution can be enumerated over the $\binom{2n - 1}{n}$ multisets of indices, which removes the Monte Carlo error. The tests compare the code with the enumeration of all $n^n$ resamples for $n \le 5$.
- **Phylogenetics.** The [phylogenetic bootstrap](/phylogenetic-bootstrap/) reports the fraction of replicates that contain a clade, which is a percentile-type support value rather than an interval.
- **Subsampling intervals.** When the bootstrap is not consistent, quantiles of a subsampling distribution give valid intervals; see [subsampling](/subsampling-inference/).

## When to use it

Use it for a quick interval when the bootstrap distribution looks roughly symmetric after some monotone transformation, when the parameter has a restricted range, and when $n$ is moderate or large. For a mean or another statistic with a good standard error formula, the bootstrap-t interval covers better in skewed small samples. For a general smooth statistic, the BCa interval is the usual improvement at little extra cost.

## Pitfalls

- **Small samples.** At $n = 10$ from an exponential law, the nominal 95% interval covered the mean in only $86.9\%$ of the data sets.
- **Statistics for which the bootstrap fails.** For the sample maximum of a uniform sample the upper endpoint is always the observed maximum, and the interval cannot contain larger values; the method inherits every failure of the [bootstrap](/bootstrap-method/).
- **Biased statistics.** If $\hat\theta$ is biased, the bootstrap distribution is centred near $\hat\theta$ plus the bias, and the percentile interval moves the wrong way. The BCa correction $z_0$ handles this.
- **Interpolating quantiles.** Library quantile functions often interpolate between order statistics. That gives slightly different endpoints and loses the exact transformation-respecting property. Use the order statistic, as lines L5 and L6 do.
- **Too few replicates.** With $b = 200$ the 2.5% quantile is the 5th smallest value, and its Monte Carlo error is large.

## Implementations

## History

Bradley Efron introduced the bootstrap in 1979 and, in his 1981 and 1982 work, the percentile interval and its justification by a normalizing transformation. The weakness of the method in small and skewed samples led him to the bias-corrected interval and in 1987 to the BCa interval. Peter Hall (1988) compared the methods by Edgeworth expansions and showed that the percentile interval is first-order accurate and the studentized and BCa intervals second-order accurate. Hall also pointed out that the basic interval, which some authors call the percentile interval, reflects the bootstrap distribution, and that the two methods differ when the distribution is skewed.

## References
