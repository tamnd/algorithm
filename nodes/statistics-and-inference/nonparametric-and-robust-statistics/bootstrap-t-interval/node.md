---
tag: 48PN4N
kind: algorithm
slug: bootstrap-t-interval
name: Bootstrap-t interval
aliases:
- studentized bootstrap interval
- percentile-t interval
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: Bootstraps the studentized statistic, estimate minus original over its standard error, and inverts its quantiles. It is second-order accurate when the standard error is stable.
model: real-ram
complexity:
  vars: {n: the sample size, b: the number of bootstrap replicates}
  time: {worst: Θ(b n + b log b), best: Θ(b n)}
  space: {extra: Θ(b + n)}
properties: {deterministic: false, randomized: true, exact: false, online: false, recursive: false}
history:
  year: 1981
  people: [Bradley Efron, Peter Hall]
  note: Efron described the studentized bootstrap in his early bootstrap work; Hall (1988) showed by Edgeworth expansions that it is second-order accurate.
prereqs: [bootstrap-method, bootstrap-percentile-interval, standard-error, t-confidence-interval, pivotal-quantity]
see_also: [bca-bootstrap-interval, student-t-test, welch-t-test, delta-method, jackknife-resampling, test-interval-duality, quantile, parametric-bootstrap]
sources:
  - book: isbn:9780412042317
    title: Bradley Efron and Robert J. Tibshirani, An Introduction to the Bootstrap, Chapman and Hall, 1993
    locator: Chapter 12 (confidence intervals based on bootstrap tables, Section 12.5 on the bootstrap-t interval and its transformations)
  - paper: doi:10.1214/aos/1176350933
    title: Peter Hall, Theoretical comparison of bootstrap confidence intervals, The Annals of Statistics 16(3), 1988
    locator: pp. 927 to 953 (the studentized interval is second-order accurate and second-order correct)
  - book: isbn:9780387977201
    title: Peter Hall, The Bootstrap and Edgeworth Expansion, Springer, 1992
    locator: Chapter 3 (coverage errors of percentile and percentile-t intervals)
  - book: isbn:9780521574716
    title: A. C. Davison and D. V. Hinkley, Bootstrap Methods and their Application, Cambridge University Press, 1997
    locator: Chapter 5 (the studentized bootstrap confidence limits and variance-stabilizing transformations)
  - paper: doi:10.1214/aos/1176344552
    title: Bradley Efron, Bootstrap methods, another look at the jackknife, The Annals of Statistics 7(1), 1979
    locator: pp. 1 to 26 (the bootstrap distribution of a statistic)
---

The bootstrap-t interval estimates the law of the studentized statistic $T = (\hat\theta - \theta)/\widehat{se}$ by its [bootstrap](/bootstrap-method/) copy $T^* = (\hat\theta^* - \hat\theta)/\widehat{se}^*$, and inverts it as the [t interval](/t-confidence-interval/) inverts the Student table. Each resample needs its own standard error, so the method fits statistics with a standard error formula, such as a mean, a difference of means or a regression coefficient. Its one-sided coverage error is of order $n^{-1}$, against $n^{-1/2}$ for the [percentile interval](/bootstrap-percentile-interval/), but it is not transformation respecting and it can give very long intervals. The coverage of the interval is measured on this page, not proved.

## In plain words

The usual interval for a mean is the estimate plus or minus a table number times the standard error. The table number comes from the bell curve and is correct only for normal data. The bootstrap-t method makes its own table from the data.

Take many bootstrap samples. For each one, measure how far its estimate is from the original estimate, in units of its own standard error. Sort these distances. The lower and upper cut points take the place of the table number. Because the data make the table, the two cut points can differ, and the interval can be longer on one side.

## The problem

**Input.** A sample $x_1, \ldots, x_n$, independent and identically distributed from an unknown $F$; a procedure `est` that returns an estimate $\hat\theta$ of $\theta = t(F)$ and a standard error $\widehat{se}$ for it; a level $\alpha \in (0, 1)$; and a number of replicates $b$.

**Output.** An interval $[L, U]$ that should contain $\theta$ with probability close to $1 - \alpha$.

**Definition.** Let $K$ be the bootstrap distribution function of $T^* = (\hat\theta^* - \hat\theta)/\widehat{se}^*$ under resampling from $\hat F_n$, and $K^{-1}(p) = \inf\{t : K(t) \ge p\}$. The ideal bootstrap-t interval is

$$[\,\hat\theta - K^{-1}(1 - \alpha/2)\, \widehat{se},\ \ \hat\theta - K^{-1}(\alpha/2)\, \widehat{se}\,].$$

If $T$ had the law $K$, then $P(K^{-1}(\alpha/2) \le T \le K^{-1}(1-\alpha/2)) = 1 - \alpha$, and solving the two inequalities for $\theta$ gives this interval. Note that the upper quantile gives the lower endpoint.

## The algorithm

```pseudo id=main
BOOTSTRAP-T-INTERVAL(x_1, ..., x_n, est, α, b)
L1  (θ̂, se) ← est(x_1, ..., x_n)
L2  for j ← 1 to b do
L3      x* ← n independent draws from x_1 .. x_n, each with probability 1/n
L4      (θ̂*, se*) ← est(x*)
L5      t*_j ← (θ̂* - θ̂) / se*
L6  sort t*_1, ..., t*_b into t*_(1) ≤ ... ≤ t*_(b)
L7  t_lo ← t*_(⌈b α/2⌉), t_hi ← t*_(⌈b (1 - α/2)⌉)
L8  return [θ̂ - t_hi · se, θ̂ - t_lo · se]
```

Line L7 uses the same quantile rule as the percentile interval: $\hat K_b^{-1}(p)$ is the $\lceil b p \rceil$-th smallest replicate. For the mean, `est` returns $\bar x$ and $S/\sqrt n$, with $S^2$ the [sample variance](/sample-variance/) with divisor $n - 1$.

**Zero standard errors.** A resample can have $\widehat{se}^* = 0$, for example when every draw is the same value. The implementation sets $t^* = 0$ if also $\hat\theta^* = \hat\theta$, and $t^* = \pm\infty$ otherwise, with the sign of $\hat\theta^* - \hat\theta$. Such a replicate stays in the tail where it belongs. If about $b\alpha/2$ or more replicates are infinite on one side, the corresponding endpoint is infinite, which is the honest answer; the proof gives the exact counts. For the mean, a resample has $\widehat{se}^* = 0$ with probability $n^{1-n}$, which is $10^{-9}$ for $n = 10$.

## Example

Take the right-skewed sample of $n = 10$ values

$$0.4,\ 0.9,\ 1.3,\ 1.6,\ 2.2,\ 2.8,\ 3.5,\ 4.9,\ 7.6,\ 13.1,$$

with $\bar x = 3.83$ and $\widehat{se} = S/\sqrt{10} = 1.233$. With $\alpha = 0.05$, $b = 2000$ and `random.Random(1)`, line L7 gives

$$t_{lo} = t^*_{(50)} = -5.224, \qquad t_{hi} = t^*_{(1950)} = 1.626.$$

The Student table would give $\mp 2.262$. The bootstrap table is strongly skewed: resamples that miss the large values have a small mean and also a small standard error, so their $t^*$ is very negative. The smallest of the 2000 values was $-18.5$, the largest $4.65$. Line L8 gives

$$[\,3.83 - 1.626 \cdot 1.233,\ \ 3.83 + 5.224 \cdot 1.233\,] = [1.82,\ 10.27].$$

With the same seed, the [t interval](/t-confidence-interval/) is $[1.04, 6.62]$, the [percentile interval](/bootstrap-percentile-interval/) is $[1.80, 6.31]$ and the [BCa interval](/bca-bootstrap-interval/) is $[2.18, 6.97]$. The bootstrap-t interval is by far the longest on the right.

**Equivariance and its limit.** The data $3x_i + 5$ give $[10.47, 35.82]$, which is $3 \cdot [1.82, 10.27] + 5$, because $t^*$ does not change under such a map. The method is not transformation respecting: the bootstrap-t interval for $\log\theta$, with the [delta method](/delta-method/) standard error $\widehat{se}/\bar x$, transformed back, is $[1.97, 12.30]$, not $[1.82, 10.27]$.

**Measured coverage.** For samples from the exponential law with mean 1, 1000 data sets of each size with $b = 1000$ (seeds 101 and 102) gave these coverages for the true mean at the nominal level 0.95:

| method | $n = 10$ | $n = 20$ |
|---|---|---|
| bootstrap-t | 0.943 | 0.950 |
| t interval | 0.911 | 0.924 |
| percentile | 0.869 | 0.911 |
| BCa | 0.884 | 0.916 |

At $n = 10$ the bootstrap-t interval was entirely below the true mean in $4.5\%$ of the data sets and entirely above it in $1.2\%$, against $8.4\%$ and $0.5\%$ for the t interval. The Monte Carlo standard error of each coverage is about $0.007$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). What is proved:

- Lines L6 and L7 return $\hat K_b^{-1}(\alpha/2)$ and $\hat K_b^{-1}(1 - \alpha/2)$, and line L8 inverts them in the right order.
- If $T$ and $T^*$ have the same continuous law, the ideal interval has coverage exactly $1 - \alpha$. This holds, for example, in a location-scale family where $T$ is a pivot and the [parametric bootstrap](/parametric-bootstrap/) is used.
- The interval is equivariant under maps $x \mapsto c x + d$ with $c > 0$ when $\hat\theta$ and $\widehat{se}$ are equivariant.
- With the convention for $\widehat{se}^* = 0$, line L5 never divides by zero, and an infinite endpoint arises only when at least $b\alpha/2$ of the replicates lie in one infinite tail.

What is not proved: the coverage for a nonparametric $F$. Under smoothness conditions, Hall (1988) shows by Edgeworth expansions that the coverage error of each one-sided endpoint is $O(n^{-1})$. The table above is a measurement.

## Complexity

Each replicate draws $n$ indices and calls `est`, which for the mean costs $\Theta(n)$. The sort costs $\Theta(b \log b)$; two selections instead of the sort give $\Theta(b)$ for this step. So the time is $\Theta(b n + b \log b)$, and the extra space is $\Theta(b + n)$. If no formula for $\widehat{se}^*$ exists, a nested bootstrap with $b_2$ inner replicates estimates it, and the time becomes $\Theta(b\, b_2\, n)$.

## Properties

- **Second-order accurate.** For smooth statistics, $T$ is asymptotically pivotal, and the bootstrap captures the skewness term of its Edgeworth expansion, so the one-sided coverage error is $O(n^{-1})$.
- **Equivariant, not transformation respecting.** The interval moves with affine changes of the data, but the result depends on the scale on which the method is run. Running it on a variance-stabilized scale and transforming back usually helps.
- **Not range preserving.** An endpoint can fall outside the parameter space, for example a correlation above 1.
- **Sensitive to the standard error.** The method is only as good as $\widehat{se}^*$. Small, unstable standard errors in some resamples give extreme $t^*$ values and long intervals, as the example shows.
- **Monte Carlo error.** The endpoints depend on extreme order statistics of $t^*$; use $b \ge 1000$.

## Variants and improvements

- **Nested bootstrap standard error.** When there is no formula, an inner bootstrap of size $b_2 \approx 25$ to $50$ estimates $\widehat{se}^*$ in each outer resample. The [jackknife](/jackknife-resampling/) standard error is a cheaper choice.
- **Variance-stabilized bootstrap-t.** Tibshirani (1988) estimates a variance-stabilizing transformation from a first bootstrap, runs the bootstrap-t on the new scale and transforms back. The result is shorter and more stable, and it is close to transformation respecting.
- **Symmetric bootstrap-t.** Uses the $1 - \alpha$ quantile $c$ of $\lvert T^* \rvert$ and returns $\hat\theta \pm c\, \widehat{se}$. Its two-sided coverage error is $O(n^{-2})$ under smoothness, but it cannot follow skewness.
- **Bootstrap tests.** Inverting the interval gives a bootstrap t test of $\theta = \theta_0$, by the [duality of tests and intervals](/test-interval-duality/). For two samples with unequal variances, studentizing with the Welch standard error gives a bootstrap version of the [Welch test](/welch-t-test/).
- **Regression.** Resampling residuals or pairs, with the usual standard error of a coefficient, gives bootstrap-t intervals for the coefficients.

## When to use it

Use it for a mean, a difference of means or a regression coefficient when the data are skewed and $n$ is small or moderate, which is where the t interval is least accurate. Avoid it for statistics without a stable standard error, such as the median, and for bounded parameters such as a correlation, unless you first move to a scale where the parameter is unbounded and the variance is stable. For a general smooth statistic without a standard error formula, the [BCa interval](/bca-bootstrap-interval/) is often simpler.

## Pitfalls

- **Using the original standard error.** Dividing $\hat\theta^* - \hat\theta$ by $\widehat{se}$ instead of $\widehat{se}^*$ gives a rescaled percentile interval and loses the second-order accuracy.
- **Swapping the quantiles.** The upper quantile $t_{hi}$ gives the lower endpoint. Swapping them reflects the interval and badly damages the coverage of skewed statistics.
- **Very long intervals.** In small skewed samples the lower tail of $t^*$ is long, and so is the upper part of the interval. The interval is valid but may be too wide to be useful.
- **Dropping replicates with zero standard error.** Removing them biases the tails. Keep them as $\pm\infty$, as line L5 does in the implementation.
- **Outliers.** One large value can control both $\hat\theta^*$ and $\widehat{se}^*$ in many resamples.

## Implementations

## History

The idea of studentizing before resampling is in Bradley Efron's early work on the bootstrap, around 1979 to 1982, as the natural bootstrap version of Student's t. Efron noted that the method can be erratic, and he later preferred the BCa interval for general statistics. Peter Hall (1988) used Edgeworth expansions to show that the studentized interval is second-order accurate and that its endpoints agree with those of the interval based on the exact law of $T$ up to terms of order $n^{-3/2}$; Hall called it the "percentile-t" method, which is the second alias of this page. Robert Tibshirani (1988) proposed the variance-stabilized version to make it more stable.

## References
