---
tag: HRG7H4
kind: algorithm
slug: bca-bootstrap-interval
name: BCa bootstrap interval
aliases:
- bias-corrected and accelerated interval
- BCa interval
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: Efron's bootstrap interval that shifts the percentiles by a bias correction and an acceleration from the jackknife. It is second-order accurate.
model: real-ram
complexity:
  vars: {n: the sample size, b: the number of bootstrap replicates}
  time: {worst: Θ(b n + n^2 + b log b), best: Θ(b n + n^2)}
  space: {extra: Θ(b + n)}
properties: {deterministic: false, randomized: true, exact: false, online: false, recursive: false}
history:
  year: 1987
  people: [Bradley Efron]
  note: Efron introduced the bias-corrected and accelerated interval in Better bootstrap confidence intervals, JASA 1987, as an improvement of his percentile and bias-corrected intervals.
prereqs: [bootstrap-percentile-interval, jackknife-resampling, confidence-interval, quantile]
see_also: [bootstrap-t-interval, bootstrap-method, influence-function, delta-method, parametric-bootstrap, t-confidence-interval, test-interval-duality, subsampling-inference]
sources:
  - paper: doi:10.1080/01621459.1987.10478410
    title: Bradley Efron, Better bootstrap confidence intervals, Journal of the American Statistical Association 82(397), 1987
    locator: pp. 171 to 185 (the BCa method, the transformation model with bias z0 and acceleration a, and the jackknife estimate of a)
  - book: isbn:9780412042317
    title: Bradley Efron and Robert J. Tibshirani, An Introduction to the Bootstrap, Chapman and Hall, 1993
    locator: Chapter 14 (better bootstrap confidence intervals, the BCa method and its formulas) and Chapter 22 (justification of the method)
  - paper: doi:10.1214/aos/1176350933
    title: Peter Hall, Theoretical comparison of bootstrap confidence intervals, The Annals of Statistics 16(3), 1988
    locator: pp. 927 to 953 (the BCa interval is second-order accurate and second-order correct)
  - book: isbn:9780521574716
    title: A. C. Davison and D. V. Hinkley, Bootstrap Methods and their Application, Cambridge University Press, 1997
    locator: Chapter 5 (the adjusted percentile method, BCa, and its estimate of a by empirical influence values)
---

The BCa (bias-corrected and accelerated) interval is a [percentile interval](/bootstrap-percentile-interval/) taken at adjusted levels. Instead of the $\alpha/2$ and $1 - \alpha/2$ quantiles of the [bootstrap](/bootstrap-method/) replicates, it uses the levels $\alpha_1$ and $\alpha_2$ computed from a bias correction $z_0$, measured by the fraction of replicates below the estimate, and an acceleration $a$, measured by the skewness of the [jackknife](/jackknife-resampling/) values. It keeps the simplicity and the range of the percentile interval, it respects monotone transformations when $a$ is fixed, and Hall (1988) showed that its one-sided coverage error is of order $n^{-1}$. That accuracy is asymptotic: the coverages on this page are measured, not proved.

## In plain words

The percentile interval cuts off the same share of bootstrap values at each end. That is right only when the bootstrap values are centred on the estimate and spread out the same way on both sides. The BCa interval checks two things. First, are more than half of the bootstrap values below the estimate? If so, the bootstrap distribution sits too low, and both cut points move up. Second, does the spread of the estimate grow with its size, which shows as skewness when you leave out one data point at a time? If so, the cut points move further toward the long tail. The result is still two of the sorted bootstrap values, chosen with more care.

## The problem

**Input.** A sample $x_1, \ldots, x_n$, independent and identically distributed from an unknown $F$; a statistic $s$ with $\hat\theta = s(x)$, which estimates $\theta = t(F)$; a level $\alpha \in (0, 1)$; and a number of replicates $b$.

**Output.** An interval $[L, U]$ that should contain $\theta$ with probability close to $1 - \alpha$.

**Definition.** Let $G$ be the bootstrap distribution function of $\hat\theta^*$, $\Phi$ the standard normal distribution function and $z_p = \Phi^{-1}(p)$. With

$$z_0 = \Phi^{-1}\bigl(G(\hat\theta^-)\bigr), \qquad a = \frac{\sum_i d_i^3}{6 \bigl(\sum_i d_i^2\bigr)^{3/2}}, \qquad d_i = \hat\theta_{(\cdot)} - \hat\theta_{(i)},$$

where $G(\hat\theta^-) = P^*(\hat\theta^* < \hat\theta)$, $\hat\theta_{(i)}$ is the estimate without $x_i$ and $\hat\theta_{(\cdot)}$ is their mean, the adjusted levels are

$$\alpha_1 = \Phi\Bigl(z_0 + \frac{z_0 + z_{\alpha/2}}{1 - a (z_0 + z_{\alpha/2})}\Bigr), \qquad \alpha_2 = \Phi\Bigl(z_0 + \frac{z_0 + z_{1-\alpha/2}}{1 - a (z_0 + z_{1-\alpha/2})}\Bigr),$$

and the BCa interval is $[G^{-1}(\alpha_1), G^{-1}(\alpha_2)]$. With $z_0 = 0$ and $a = 0$ the levels are $\alpha/2$ and $1 - \alpha/2$, and it is the percentile interval.

## The algorithm

```pseudo id=main
BCA-INTERVAL(x_1, ..., x_n, s, α, b)
L1  θ̂ ← s(x_1, ..., x_n)
L2  for j ← 1 to b do
L3      x* ← n independent draws from x_1 .. x_n, each with probability 1/n
L4      θ*_j ← s(x*)
L5  sort the θ*_j; c ← #{j : θ*_j < θ̂}
L6  z_0 ← Φ⁻¹(c / b)
L7  a ← Σ d_i³ / (6 (Σ d_i²)^{3/2}) with d_i = θ̂_(·) - θ̂_(i), from the n leave-one-out estimates
L8  α_1, α_2 ← Φ(z_0 + (z_0 + z)/(1 - a (z_0 + z))) for z = z_{α/2} and z = z_{1-α/2}
L9  return [θ*_(⌈b α_1⌉), θ*_(⌈b α_2⌉)]
```

Line L6 needs $0 < c < b$; if every replicate lies on one side of $\hat\theta$, $z_0$ is infinite and the implementation raises an error. Line L8 needs $1 - a(z_0 + z) > 0$; otherwise the formula breaks down and the implementation raises an error. Line L9 uses the quantile rule of the percentile interval, $\hat G_b^{-1}(p) = \theta^*_{(\lceil b p \rceil)}$. The implementation also accepts a fixed value of $a$ in place of line L7.

## Example

Take the right-skewed sample of $n = 10$ values

$$0.4,\ 0.9,\ 1.3,\ 1.6,\ 2.2,\ 2.8,\ 3.5,\ 4.9,\ 7.6,\ 13.1,$$

with $\bar x = 3.83$, the statistic the mean, $\alpha = 0.05$, $b = 2000$ and `random.Random(1)`.

1. Lines L2 to L5: 1087 of the 2000 replicates are below 3.83, so $z_0 = \Phi^{-1}(0.5435) = 0.109$. The bootstrap distribution of the mean has its median below $\bar x$, because the distribution is skewed to the right.
2. Line L7: for the mean, $d_i = (x_i - \bar x)/(n - 1)$, so $a$ is the plug-in skewness divided by $6\sqrt n$. Here the skewness is $1.488$ and $a = 1.488/(6\sqrt{10}) = 0.0784$.
3. Line L8: $\alpha_1 = \Phi(0.109 + (-1.851)/1.145) = \Phi(-1.507) = 0.0659$ and $\alpha_2 = \Phi(0.109 + 2.069/0.838) = \Phi(2.579) = 0.9950$.
4. Line L9: $\lceil 2000 \cdot 0.0659 \rceil = 132$ and $\lceil 2000 \cdot 0.9950 \rceil = 1991$. The 132nd and the 1991st smallest replicates are 2.18 and 6.97.

So the interval is $[2.18, 6.97]$. Both levels moved up from $0.025$ and $0.975$, and the interval moved right of the percentile interval $[1.80, 6.31]$. With $a = 0$ (the bias-corrected interval) the same replicates give $[2.00, 6.53]$. The bootstrap-t interval is $[1.82, 10.27]$ and the t interval $[1.04, 6.62]$.

**Transformation.** With $a$ fixed, the BCa interval for $\log\theta$ is the log of the interval for $\theta$; the tests check this exactly. With the jackknife estimate of $a$, it is not: on the log scale, line L7 gives $a = 0.0875$ instead of $0.0784$, and the interval, transformed back, is $[2.19, 6.99]$. The value $z_0 = 0.109$ is the same on both scales.

**Measured coverage.** For samples from the exponential law with mean 1, 1000 data sets of each size with $b = 1000$ (seeds 101 and 102) gave these coverages for the true mean at the nominal level 0.95:

| method | $n = 10$ | $n = 20$ |
|---|---|---|
| BCa | 0.884 | 0.916 |
| percentile | 0.869 | 0.911 |
| bootstrap-t | 0.943 | 0.950 |
| t interval | 0.911 | 0.924 |

The study used the formula $a = \text{skewness}/(6\sqrt n)$, which is the jackknife value for the mean. The BCa interval improves on the percentile interval and is better balanced than the t interval, with misses of $8.4\%$ below and $3.2\%$ above at $n = 10$. But for the mean of a small skewed sample it is still too short, because the bootstrap distribution of the mean has the plug-in variance and normal-like tails. Second-order accuracy is a statement about large $n$. The Monte Carlo standard error of each coverage is about $0.007$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). What is proved:

- Lines L5 to L9 compute the stated formulas, and with $z_0 = a = 0$ the algorithm is the percentile interval.
- $z_0$ does not change under a strictly increasing transformation of the statistic. With $a$ fixed, the interval respects such transformations. The jackknife value of $a$ does change, so the full algorithm respects them only approximately.
- In Efron's transformation model, where an increasing $\phi$ makes $\phi(\hat\theta) = \phi(\theta) + (1 + a\phi(\theta))(Z - z_0)$ with $Z$ standard normal, and the bootstrap follows the same model, the ideal BCa interval with the true $z_0$ and $a$ has coverage $1 - \alpha$, exactly when $a = 0$ and up to an error below $\Phi(-1/\lvert a \rvert + \lvert z_0 \rvert)$ otherwise.

What is not proved: the coverage for a general $F$. Hall (1988) shows by Edgeworth expansions that the one-sided coverage error is $O(n^{-1})$ under smoothness conditions; the table above is a measurement.

## Complexity

The $b$ replicates cost $\Theta(b n)$ for the mean, the sort costs $\Theta(b \log b)$, and the counting of line L5 costs $\Theta(b)$. Line L7 computes $n$ leave-one-out estimates; done naively for a statistic that costs $\Theta(n)$, this is $\Theta(n^2)$, and for the mean it can be done in $\Theta(n)$ by subtracting each value from the total. Two selections at the levels $\alpha_1$ and $\alpha_2$ can replace the sort. The extra space is $\Theta(b + n)$.

## Properties

- **Second-order accurate.** For smooth statistics, the one-sided coverage error is $O(n^{-1})$, and the endpoints agree with those of the bootstrap-t interval up to terms of order $n^{-3/2}$ (Hall 1988).
- **Transformation respecting** for a fixed $a$, and approximately so with the jackknife $a$, as the example shows.
- **Range preserving.** The endpoints are replicate values, as in the percentile interval.
- **No standard error needed.** Unlike the [bootstrap-t interval](/bootstrap-t-interval/), it needs only the statistic itself and its $n$ leave-one-out values.
- **More replicates.** The adjusted levels can be far in the tails, as $\alpha_2 = 0.995$ in the example, so $b$ should be at least 1000, and better 2000 or more.

## Variants and improvements

- **Bias-corrected (BC) interval.** Efron's earlier method sets $a = 0$. It corrects the median bias but not the change of the standard error with $\theta$, and it is only first-order accurate.
- **Acceleration from influence values.** In place of the jackknife, $a$ can be computed from the empirical [influence function](/influence-function/) values $\ell_i$ as $\sum \ell_i^3 / (6 (\sum \ell_i^2)^{3/2})$. For the mean both give $\text{skewness}/(6\sqrt n)$.
- **Parametric BCa.** With a [parametric bootstrap](/parametric-bootstrap/), $a$ is computed from the score function of the model instead of the jackknife.
- **ABC interval.** DiCiccio and Efron's approximate bootstrap confidence interval replaces the resampling by a few numerical derivatives of the statistic. It gives nearly the same endpoints for smooth statistics, without Monte Carlo error.
- **Iterated bootstrap calibration.** A second level of bootstrap estimates the actual coverage and adjusts the nominal level. It also gives second-order or better accuracy, at the cost of $b^2$ evaluations.

## When to use it

Use it as the default bootstrap interval for a smooth statistic without a reliable standard error formula, such as a correlation, a ratio or a quantile of moderate order, when $n$ is moderate or large. It needs only the statistic, which you must already compute. For a mean or a regression coefficient in a small skewed sample, the bootstrap-t interval covered better in the study above. For a statistic that is not smooth, such as an extreme order statistic, neither method is valid, and [subsampling](/subsampling-inference/) is the safer tool.

## Pitfalls

- **Ties at the estimate.** Counting replicates with $\theta^*_j \le \hat\theta$ instead of $< \hat\theta$ changes $z_0$ when many replicates equal $\hat\theta$, as for a median. Some software splits the ties in half; state the rule.
- **Extreme levels.** If $\lvert z_0 \rvert$ or $\lvert a \rvert$ is large, $\alpha_1$ or $\alpha_2$ can be very close to 0 or 1, and the endpoint is then an extreme replicate with a large Monte Carlo error. If $1 - a(z_0 + z) \le 0$, the formula is not defined.
- **Wrong sign of $a$.** The jackknife differences are $d_i = \hat\theta_{(\cdot)} - \hat\theta_{(i)}$. The reversed sign gives an acceleration with the wrong sign, which moves the interval the wrong way.
- **Small samples.** The interval inherits the narrowness of the bootstrap distribution. Second-order accuracy does not mean good coverage at $n = 10$.
- **Statistics where the bootstrap fails.** The correction cannot repair an inconsistent bootstrap, for example for the sample maximum.

## Implementations

## History

Bradley Efron proposed the percentile interval with the bootstrap and, in 1981 and 1982, the bias-corrected interval, which adds $z_0$. In Better bootstrap confidence intervals (JASA, 1987) he added the acceleration $a$, derived the interval from a transformation model in which the standard deviation of the normalized estimate changes linearly with the parameter, and gave the jackknife estimate of $a$. Peter Hall's 1988 paper, which used Edgeworth expansions, showed that BCa and the bootstrap-t interval are both second-order accurate, while the percentile and BC intervals are first-order accurate. DiCiccio and Efron later developed the ABC approximation and reviewed the methods.

## References
