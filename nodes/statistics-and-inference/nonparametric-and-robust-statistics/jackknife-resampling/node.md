---
tag: DBF7V5
kind: algorithm
slug: jackknife-resampling
name: Jackknife
aliases:
- Quenouille-Tukey jackknife
- leave-one-out jackknife
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Recompute a statistic with each observation left out in turn, and combine the n values to estimate its bias and variance. It fails for nonsmooth statistics like the median.
model: real-ram
complexity:
  vars: {n: the sample size}
  time: {worst: Θ(n^2), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, randomized: false, exact: false, online: false, recursive: false}
history:
  year: 1949
  people: [Maurice Quenouille, John Tukey]
  note: Quenouille introduced leave-out estimates to reduce bias in 1949 and 1956; Tukey added the variance estimate and the pseudo-values in 1958 and gave the method its name.
prereqs: [estimator-bias, standard-error, sample-variance, sampling-distribution]
see_also: [bootstrap-method, bca-bootstrap-interval, u-statistic, subsampling-inference, influence-function, cross-validation, delta-method, conformal-prediction]
sources:
  - paper: doi:10.1111/j.2517-6161.1949.tb00023.x
    title: M. H. Quenouille, Approximate tests of correlation in time-series, Journal of the Royal Statistical Society, Series B 11(1), 1949
    locator: pp. 68 to 84 (the bias reduction by estimates on parts of the sample)
  - paper: doi:10.1093/biomet/43.3-4.353
    title: M. H. Quenouille, Notes on bias in estimation, Biometrika 43(3-4), 1956
    locator: pp. 353 to 360 (the leave-one-out bias correction n θ̂ - (n - 1) θ̂_(·))
  - paper: "J. W. Tukey, Bias and confidence in not-quite large samples (abstract), The Annals of Mathematical Statistics 29(2), 614, 1958"
    title: J. W. Tukey, Bias and confidence in not-quite large samples, 1958
    locator: p. 614 (the pseudo-values and the jackknife variance estimate)
  - book: isbn:9780412042317
    title: Bradley Efron and Robert J. Tibshirani, An Introduction to the Bootstrap, Chapman and Hall, 1993
    locator: Chapter 11 (the jackknife, its bias and variance estimates, the failure for the median and the delete-d jackknife)
  - paper: doi:10.1214/aos/1176345462
    title: B. Efron and C. Stein, The jackknife estimate of variance, The Annals of Statistics 9(3), 1981
    locator: pp. 586 to 596 (the jackknife variance estimate is biased upward)
  - paper: doi:10.1214/aos/1176347263
    title: Jun Shao and C. F. J. Wu, A general theory for jackknife variance estimation, The Annals of Statistics 17(3), 1989
    locator: pp. 1176 to 1197 (the delete-d jackknife and its consistency for the sample quantiles)
---

The jackknife computes a statistic $n$ more times, each time with one observation left out, and uses the spread of these $n$ values to estimate the bias and the [standard error](/standard-error/) of the statistic. It needs no model and no random numbers, and it costs $n$ evaluations of the statistic. It is exact for the mean and for the [plug-in variance](/sample-variance/), it removes the $1/n$ term of the bias of smooth statistics, and it turns a V-statistic into the corresponding [U-statistic](/u-statistic/). It fails for statistics that are not smooth, such as the [median](/median/), where its variance estimate does not converge.

## In plain words

You have a statistic, such as an average or a correlation, from $n$ data points, and you want to know how much it would change with other data. Leave out the first point and compute the statistic again. Put it back, leave out the second point, and compute again. Do this for every point. If the $n$ results are close together, the statistic is stable. If they spread out, it is not. A fixed formula turns this spread into a standard error and turns the average shift into an estimate of the bias.

The method works well for statistics that change smoothly when one point moves. It works badly for the median, which jumps between only two or three values when one point is left out.

## The problem

**Input.** A sample $x_1, \ldots, x_n$, independent and identically distributed, with $n \ge 2$, and a statistic $s$ that is defined for samples of size $n$ and $n - 1$ and does not depend on the order of the data. Write $\hat\theta = s(x_1, \ldots, x_n)$.

**Output.** An estimate of the bias $E\hat\theta - \theta$, the bias-corrected estimate, and an estimate of the variance of $\hat\theta$.

**Definitions.** Let $\hat\theta_{(i)}$ be $s$ on the sample without $x_i$, and $\hat\theta_{(\cdot)} = \frac{1}{n}\sum_i \hat\theta_{(i)}$. Then

$$\widehat{\mathrm{bias}}_{jack} = (n - 1)(\hat\theta_{(\cdot)} - \hat\theta), \qquad \hat\theta_{jack} = \hat\theta - \widehat{\mathrm{bias}}_{jack} = n\hat\theta - (n - 1)\hat\theta_{(\cdot)},$$

$$\widehat{\mathrm{var}}_{jack} = \frac{n - 1}{n} \sum_{i=1}^n \bigl(\hat\theta_{(i)} - \hat\theta_{(\cdot)}\bigr)^2.$$

The factor $n - 1$ in both formulas makes them exact for the mean. **Pseudo-values** $\tilde\theta_i = n\hat\theta - (n - 1)\hat\theta_{(i)}$ give the same results: $\hat\theta_{jack}$ is their mean, and $\widehat{\mathrm{var}}_{jack}$ is their sample variance divided by $n$, as if they were $n$ independent observations.

## The algorithm

```pseudo id=main
JACKKNIFE(x_1, ..., x_n, s)
L1  θ̂ ← s(x_1, ..., x_n)
L2  for i ← 1 to n do
L3      θ̂_(i) ← s(x_1, ..., x_{i-1}, x_{i+1}, ..., x_n)
L4  θ̂_(·) ← (1/n) Σ_i θ̂_(i)
L5  bias ← (n - 1) (θ̂_(·) - θ̂)
L6  var ← ((n - 1)/n) Σ_i (θ̂_(i) - θ̂_(·))²
L7  return θ̂ - bias, bias, var
```

The implementation uses only addition, subtraction, multiplication and division, so with `Fraction` data it computes every quantity exactly. This is how the tests check the identities below.

## Example

The treatment group of the mouse data of Efron and Tibshirani (Table 2.1) has $n = 7$ survival times

$$94,\ 197,\ 16,\ 38,\ 99,\ 141,\ 23.$$

**Mean.** $\hat\theta = 86.86$. Leaving out each value in turn gives $85.67, 68.50, 98.67, 95.00, 84.83, 77.83, 97.50$, whose mean is again $86.86$, so the bias estimate is 0. Line L6 gives $636.83$, and the jackknife standard error is $\sqrt{636.83} = 25.24$, which is exactly $S/\sqrt 7$. The exact bootstrap standard error is $23.36 = \sqrt{6/7} \cdot 25.24$; the bootstrap uses the plug-in variance with divisor $n$.

**Plug-in variance.** $\hat\theta = \frac{1}{7}\sum(x_i - \bar x)^2 = 3820.98$. The bias estimate is $-636.83 = -S^2/7$, and the corrected value is $4457.81 = S^2$, the unbiased sample variance.

**Median.** $\hat\theta = 94$. The seven leave-one-out medians take only three values: $96.5$ three times, $66$ three times and $68.5$ once. The jackknife standard error is $36.27$, close to the bootstrap value $37.83$ by chance. The bias estimate is $-87.4$, and the "corrected" median is $181.4$, larger than every value but one. Do not use the jackknife for the median.

**Measured failure for the median.** For 2000 uniform samples of each size, the ratio of the jackknife variance of the median to its true variance had these summaries (seed 11):

| $n$ | mean ratio | median ratio | ratio below 0.5 |
|---|---|---|---|
| 10 | 1.62 | 0.48 | 51% |
| 40 | 1.79 | 0.47 | 51% |
| 160 | 1.96 | 0.49 | 51% |

The ratio does not concentrate at 1 as $n$ grows. It converges in law to $(\chi^2_2/2)^2$, which has mean 2 and median $(\ln 2)^2 = 0.48$ (Efron and Tibshirani, Chapter 11).

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows these facts, all exact:

- For the mean, the bias estimate is 0 and $\widehat{\mathrm{var}}_{jack} = S^2/n$, with $S^2$ the sample variance with divisor $n - 1$.
- If $E\hat\theta_n = \theta + a_1/n + a_2/n^2$ for every $n$, then $E\hat\theta_{jack} = \theta - a_2/(n(n-1))$. The $1/n$ term of the bias is removed completely.
- For every symmetric kernel $h$ of degree 2, the jackknife-corrected V-statistic $\frac{1}{n^2}\sum_{i,j} h(x_i, x_j)$ equals the U-statistic $\binom{n}{2}^{-1}\sum_{i<j} h(x_i, x_j)$. With $h(x, y) = (x - y)^2/2$ this turns the plug-in variance into $S^2$.
- The pseudo-value form gives the same estimate and variance.
- For the median with $n = 2m$, $\widehat{\mathrm{var}}_{jack} = \frac{n - 1}{4}(x_{(m+1)} - x_{(m)})^2$, a function of a single spacing.

The tests check each identity with `Fraction` data, and check the U-statistic against its definition as a sum over all pairs.

## Complexity

Lines L2 and L3 evaluate $s$ on $n$ samples of size $n - 1$. For a statistic that costs $\Theta(n)$, such as a mean or a variance, this is $\Theta(n^2)$ time, and lines L4 to L6 add $\Theta(n)$. For the mean and other statistics built from sums, each $\hat\theta_{(i)}$ follows from the full sums by one subtraction, and the whole jackknife costs $\Theta(n)$. The extra space is $\Theta(n)$ for the $n$ values. The delete-$d$ jackknife over all $\binom{n}{d}$ subsets is much more expensive and is usually done on a random selection of subsets.

## Properties

- **Deterministic.** The same data always give the same result, unlike the [bootstrap](/bootstrap-method/).
- **Exact for linear statistics.** For a statistic of the form $\frac{1}{n}\sum g(x_i)$, the variance estimate is exactly the unbiased estimate $S_g^2/n$.
- **Second-order bias reduction.** The corrected estimate has bias $O(n^{-2})$ when the bias has an expansion in powers of $1/n$. The variance of the corrected estimate can be larger than that of $\hat\theta$.
- **Conservative variance.** Efron and Stein (1981) showed that, for any symmetric statistic $S$ of $n - 1$ observations, $E\sum_{i=1}^n (S_{(i)} - S_{(\cdot)})^2 \ge \mathrm{Var}\, S(X_1, \ldots, X_{n-1})$. So the jackknife variance tends to be too large rather than too small.
- **A linear approximation of the bootstrap.** The jackknife variance is, up to the factor $\frac{n}{n-1}$, the bootstrap variance of the best linear approximation of the statistic in the resampling weights. It agrees with the bootstrap for smooth statistics and differs for nonsmooth ones.
- **Inconsistent for the median and other quantiles.** The delete-1 estimate depends on one or two spacings of the order statistics, as the example shows.

## Variants and improvements

- **Delete-$d$ jackknife.** Leave out $d$ observations at a time and use $\frac{n - d}{d\binom{n}{d}}\sum_S (\hat\theta_S - \bar\theta)^2$ over the subsets $S$. For the mean it gives $S^2/n$ for every $d$. Shao and Wu (1989) proved that it is consistent for the sample quantiles when $d/\sqrt n \to \infty$ and $n - d \to \infty$. With $d = n - m$ it is closely related to [subsampling](/subsampling-inference/) with subsamples of size $m$.
- **Grouped jackknife.** Split the data into $g$ groups and leave out one group at a time. This is Quenouille's original form and reduces the cost to $g$ evaluations.
- **Infinitesimal jackknife.** Replace the leave-one-out differences by derivatives of the statistic in the direction of each point, which are the empirical [influence function](/influence-function/) values. This gives the delta-method variance $\frac{1}{n^2}\sum \ell_i^2$.
- **Acceleration of BCa.** The skewness of the leave-one-out values gives the acceleration $a$ of the [BCa interval](/bca-bootstrap-interval/).
- **Jackknife+ prediction intervals.** In predictive inference, leave-one-out residuals give prediction intervals with guaranteed coverage; see [conformal prediction](/conformal-prediction/).
- **Leave-one-out cross-validation.** The same loop that leaves out each point, applied to prediction error rather than to bias and variance, is [cross-validation](/cross-validation/).

## When to use it

Use the jackknife for a quick, deterministic standard error or bias correction of a smooth statistic: a mean, a ratio of means, a correlation, a regression coefficient or a smooth function of moments. It is useful when the statistic is expensive and $n$ is small, so that $n$ evaluations are cheaper than the $b \ge 200$ of the bootstrap. Use the bootstrap or the delete-$d$ jackknife for quantiles and other nonsmooth statistics, and the bootstrap when you need a confidence interval rather than a standard error.

## Pitfalls

- **The median and other quantiles.** The variance estimate is inconsistent, and the bias correction can be absurd, as the example shows.
- **Using the usual variance formula.** The leave-one-out values are much closer together than independent replicates, because any two of them share $n - 2$ observations. Their ordinary sample variance, with the factor $1/(n - 1)$ in place of $(n - 1)/n$, is too small by the factor $(n - 1)^2/n$.
- **Variance of the corrected estimate.** The jackknife variance estimates the variance of $\hat\theta$; it is often used for $\hat\theta_{jack}$ too, which is only approximately right.
- **Dependent data.** Leaving out single observations of a time series ignores the dependence. Leave out blocks, as the [block bootstrap](/block-bootstrap/) resamples blocks.
- **Bias correction can increase the error.** Removing a small bias can add more variance than it removes in mean squared error; report both $\hat\theta$ and $\hat\theta_{jack}$.

## Implementations

## History

Maurice Quenouille introduced the idea in 1949, to reduce the bias of estimates of serial correlation by combining estimates on parts of the sample, and in 1956 gave the leave-one-out form $n\hat\theta - (n - 1)\hat\theta_{(\cdot)}$. John Tukey, in a 1958 abstract, saw that the pseudo-values behave approximately like independent observations, which gives a variance estimate and approximate t intervals, and named the method after the pocket knife that serves many purposes. Rupert Miller studied its theory in the 1960s and 1970s. Bradley Efron's 1979 bootstrap paper presented the bootstrap as "another look at the jackknife", and Efron and Stein (1981) proved that the jackknife variance is biased upward. Shao and Wu (1989) developed the delete-$d$ jackknife.

## References
