---
tag: W2JAG5
kind: algorithm
slug: t-confidence-interval
name: Student t confidence interval
aliases:
- t interval for a mean
area: statistics-and-inference/hypothesis-testing
level: intro
summary: The interval x-bar plus or minus t_(n-1, 1-alpha/2) S/sqrt(n) for a normal mean with unknown variance. Exact coverage 1 - alpha under normal iid data; asymptotic otherwise. O(n).
model: real-ram
complexity:
  vars: {n: the number of observations}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1937
  people: [William Sealy Gosset, Jerzy Neyman]
  note: Student derived the law of the standardized mean in 1908. Neyman's 1937 theory of confidence intervals gave the frequentist meaning of the interval built from it.
prereqs: [confidence-interval, student-t-test]
see_also: [test-interval-duality, welch-t-test, z-test, sample-size-determination, bootstrap-method, credible-interval, prediction-interval, clopper-pearson-interval]
sources:
  - paper: doi:10.1098/rsta.1937.0005
    title: "Jerzy Neyman, Outline of a theory of statistical estimation based on the classical theory of probability, Philosophical Transactions of the Royal Society A 236, 1937, pp. 333 to 380"
    locator: The whole paper (confidence intervals, the coverage probability as a property of the procedure, and the statement that a computed interval contains the parameter or does not)
  - paper: doi:10.1093/biomet/6.1.1
    title: "Student, The probable error of a mean, Biometrika 6(1), 1908, pp. 1 to 25"
    locator: The whole paper (the law of the standardized mean for normal samples, the pivot behind the interval)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 9.2.1 (inverting a test statistic, the t interval as the inverted t-test) and Section 9.2.2 (pivotal quantities)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Section 5.4 (confidence intervals and families of tests) and Section 5.5 (unbiased confidence sets)
---

The Student t confidence interval for the mean $\mu$ of a normal population with unknown standard deviation is $\bar X \pm t_{(n-1, 1-\alpha/2)}S/\sqrt n$, where $S^2$ is the [sample variance](/sample-variance/) with divisor $n - 1$ and $t_{(n-1, p)}$ is the lower $p$ quantile of the t distribution with $n - 1$ degrees of freedom. Under iid normal data its [confidence](/confidence-interval/) coverage is exactly $1 - \alpha$ for every $\mu$, $\sigma$ and $n \ge 2$: it is built from a pivot whose law is free of both parameters. It is the set of null values that the two-sided [Student t-test](/student-t-test/) does not reject, an instance of [test-interval duality](/test-interval-duality/). Without normality the coverage is only asymptotic.

## In plain words

You want a range of plausible values for a true average, from a few measurements, without knowing how much single measurements scatter. Take the sample average, estimate its typical error from the same data, and go a fixed number of typical errors to each side. The number comes from Student's law of the standardized average, so it is larger than the familiar 1.96 when there are few measurements: about 2.78 with five values and 12.7 with two. If the data come from a bell curve, the procedure catches the true average in 95 of every 100 samples in the long run. Any single computed range either contains the true average or does not; the 95 describes the method, not that range.

## The problem

**Model.** $X_1, \dots, X_n$ iid $N(\mu, \sigma^2)$ with $\mu$ and $\sigma$ unknown, $n \ge 2$, and a confidence level $1 - \alpha \in (0, 1)$. Find a random interval $[L, U]$, a function of the data only, with $P_{\mu,\sigma}(L \le \mu \le U) \ge 1 - \alpha$ for all $(\mu, \sigma)$, as short as possible.

**Pivot.** $Q = (\bar X - \mu)/(S/\sqrt n)$ has the $t_{n-1}$ law for every $\mu$ and $\sigma$.

**Interval.** Two-sided: $\bar X \pm t_{(n-1, 1-\alpha/2)}S/\sqrt n$. Lower confidence bound: $[\bar X - t_{(n-1, 1-\alpha)}S/\sqrt n, \infty)$. Upper confidence bound: $(-\infty, \bar X + t_{(n-1, 1-\alpha)}S/\sqrt n]$.

**Coverage type.** Exact: under the model the coverage equals $1 - \alpha$ at every parameter value, not only as an infimum. The probability is marginal, over repeated samples. Outside normality, for iid data with finite variance, the coverage tends to $1 - \alpha$ as $n \to \infty$ by the [central limit theorem](/central-limit-theorem/) and Slutsky's theorem; it is then asymptotic, and not uniformly so.

**Duality.** $\mu_0$ lies in the open interval exactly when the two-sided level-$\alpha$ t-test of $H_0: \mu = \mu_0$ does not reject, that is when its p-value exceeds $\alpha$; at the two end points the p-value equals $\alpha$.

## The algorithm

```pseudo id=main
T-INTERVAL(x[1..n], 1 − α, side)     ▷ n ≥ 2
L1  n ← the length of x
L2  x̄ ← (x[1] + ... + x[n]) / n
L3  S² ← ((x[1] − x̄)² + ... + (x[n] − x̄)²) / (n − 1)   ▷ second pass, divisor n − 1
L4  se ← √(S² / n)
L5  if side = two-sided then q ← t_(n−1, 1−α/2)
L6      return [x̄ − q · se, x̄ + q · se]
L7  q ← t_(n−1, 1−α)
L8  if side = lower then return [x̄ − q · se, ∞)
L9  return (−∞, x̄ + q · se]
```

The quantile is found by bisection on the upper tail $\bar F_{n-1}(x) = P(T_{n-1} > x)$, which the helper evaluates by the continued fraction of the regularized incomplete beta function: $\bar F_\nu(x) = \tfrac12 I_{\nu/(\nu + x^2)}(\nu/2, 1/2)$ for $x \ge 0$. Bisecting on the upper tail, not on $1 - F$, keeps the digits of small tail probabilities. The code caches the quantile for each $(p, n - 1)$, which matters when the interval is computed many times, as in a simulation. If all values are equal, $S = 0$ and the interval is the single point $\bar x$; this happens with probability 0 under the model.

## Example

The paired sleep data of Cushny and Peebles, used by Student in 1908: the extra hours of sleep under drug 2 minus drug 1 for 10 patients are $1.2, 2.4, 1.3, 1.3, 0.0, 1.0, 1.8, 0.8, 4.6, 1.4$. A 95% interval for the mean difference:

| line | value |
|---|---|
| L2: $\bar d = 15.8/10$ | $1.58$ |
| L3: $S^2 = 13.616/9$ | $1.512889$ |
| L4: $se = \sqrt{1.512889/10}$ | $0.388959$ |
| L5: $q = t_{(9, 0.975)}$ | $2.262157$ |
| L6: $1.58 \mp 2.262157 \times 0.388959$ | $[0.7001, 2.4599]$ |

The interval excludes 0, matching the t-test p-value of 0.0028. The 99% interval, with $t_{(9, 0.995)} = 3.249836$, is $[0.3159, 2.8441]$, and the 95% lower bound, with $t_{(9, 0.95)} = 1.833113$, is $0.8670$. Using 1.96 in place of 2.262157 would give $[0.8177, 2.3423]$, which is too short.

**Coverage.** Monte Carlo with $r = 20000$ replications of nominal 95% intervals (standard error of an estimated coverage near 0.95: 0.0015):

| data | $n$ | two-sided | lower bound | upper bound | seed |
|---|---|---|---|---|---|
| normal, $\mu = 4$, $\sigma = 2$ | 2 | 0.9507 | | | 31 |
| normal, $\mu = 4$, $\sigma = 2$ | 5 | 0.9530 | | | 31 |
| normal, $\mu = 4$, $\sigma = 2$ | 20 | 0.9496 | | | 31 |
| exponential, mean 1 | 5 | 0.8802 | 0.9891 | 0.8423 | 32 |
| exponential, mean 1 | 30 | 0.9273 | 0.9776 | 0.9023 | 32 |
| exponential, mean 1 | 100 | 0.9427 | 0.9680 | 0.9259 | 32 |

Under normality the coverage is 0.95 within the Monte Carlo error at every $n$, even $n = 2$. For skewed data the two-sided coverage is too low and the two one-sided bounds err in opposite directions: when the sample mean is low, $S$ also tends to be low, so the upper bound misses $\mu$ far more often than 5%. At $n = 100$ the upper bound still covers only 0.926. The interval $\bar X \pm 1.96\,S/\sqrt n$ on normal data with $n = 5$ covers 0.8771 (same $r$, seed 33).

## Correctness

By Helmert's transformation, $\bar X$ and $S^2$ are independent under normality, $\sqrt n(\bar X - \mu)/\sigma$ is standard normal and $(n - 1)S^2/\sigma^2$ is chi-square with $n - 1$ degrees of freedom, so the pivot $Q$ is $t_{n-1}$ and its law does not involve $\mu$ or $\sigma$. The event $\{L \le \mu \le U\}$ is the event $\{|Q| \le t_{(n-1, 1-\alpha/2)}\}$, whose probability is $1 - \alpha$ by the symmetry and continuity of $t_{n-1}$. The one-sided bounds are the events $Q \le t_{(n-1, 1-\alpha)}$ and $Q \ge -t_{(n-1, 1-\alpha)}$. Duality follows because the two-sided p-value is a strictly decreasing function of $|\bar x - \mu_0|$ that equals $\alpha$ at the end points. Without normality, $Q$ tends to $N(0, 1)$ and the quantiles tend to the normal ones. The proofs are in the correctness proof below.

## Complexity

On a [real RAM](/real-ram/), L2 and L3 make two passes, about $4n$ arithmetic operations, and L4 to L9 a constant number. The quantile costs a bisection of at most a few hundred halvings, each an incomplete beta evaluation whose cost does not grow with $n$, and it is computed once per $(1 - \alpha, n)$. So the time is $\Theta(n)$ and the extra space $\Theta(1)$ besides the data. L3 uses the two-pass formula; the one-pass $\sum x_i^2 - n\bar x^2$ suffers [catastrophic cancellation](/catastrophic-cancellation/) when the mean is large compared with the spread.

## Properties

- **Exact.** Coverage exactly $1 - \alpha$ for every $\mu$, $\sigma$ and $n \ge 2$ under iid normal data.
- **Equivariant.** If every $x_i$ is replaced by $a + b x_i$ with $b \ne 0$, the interval is mapped by the same affine map (with its ends swapped when $b < 0$).
- **Random width.** The width $2t_{(n-1, 1-\alpha/2)}S/\sqrt n$ varies from sample to sample. Its expectation is $2t_{(n-1, 1-\alpha/2)}c_4(n)\sigma/\sqrt n$ with $c_4(n) = \sqrt{2/(n - 1)}\,\Gamma(n/2)/\Gamma((n - 1)/2)$. For 95% intervals the expected width in units of $\sigma$ is 14.34 at $n = 2$, 4.40 at $n = 3$, 2.334 at $n = 5$, 1.392 at $n = 10$ and 0.740 at $n = 30$, against $2 \times 1.96/\sqrt n$ = 2.772, 2.263, 1.753, 1.240 and 0.716 for the z interval with $\sigma$ known.
- **Optimal among unbiased intervals.** It inverts the uniformly most powerful unbiased family of t-tests, so it is uniformly most accurate unbiased: it covers each false value with the smallest possible probability (Lehmann and Romano, Sections 5.4 and 5.5).
- **One-sided bounds.** The $1 - \alpha$ lower bound is the left end of the two-sided $1 - 2\alpha$ interval.

## Variants and improvements

- **z interval.** With $\sigma$ known, $\bar X \pm z_{1-\alpha/2}\sigma/\sqrt n$ is exact and has a fixed width; see the [z-test](/z-test/).
- **Paired and two-sample intervals.** The interval for a mean difference of paired data is the t interval of the differences. For two independent samples, the pooled interval uses $S_p$ and $m + n - 2$ degrees of freedom (exact under equal variances), and the [Welch interval](/welch-t-test/) uses separate variances and the Welch-Satterthwaite degrees of freedom (approximate).
- **Bootstrap intervals.** The [bootstrap](/bootstrap-method/) percentile-t interval estimates the law of $Q$ from the data. It corrects the one-sided errors for skewed data at a rate faster than the normal approximation, but is still approximate.
- **Intervals for a proportion.** For binomial data the analogue is the Wilson score or [Clopper-Pearson](/clopper-pearson-interval/) interval, not a t interval.
- **Prediction interval.** $\bar X \pm t_{(n-1, 1-\alpha/2)}S\sqrt{1 + 1/n}$ covers the next observation, not the mean, with probability $1 - \alpha$ under normality; see [prediction interval](/prediction-interval/).
- **Credible interval.** Under the improper prior with density proportional to $1/\sigma$, the Bayesian posterior of $\mu$ is $\bar x + (s/\sqrt n)t_{n-1}$, so the equal-tailed [credible interval](/credible-interval/) has the same end points. The numbers agree; the statements do not: the credible interval assigns posterior probability $1 - \alpha$ to $\mu$ given the data, while the confidence statement is about the procedure over repeated samples.

## When to use it

Use the t interval for the mean of one sample, or of paired differences, when $\sigma$ is unknown and the data are close to normal, or when $n$ is large and the data are not strongly skewed. Report it together with or instead of a t-test p-value: it shows both the estimate and its precision. For strongly skewed data with small $n$, or for one-sided bounds on skewed data even at $n = 100$, use a transformation, a bootstrap interval or a method built for the distribution.

## Pitfalls

- **Reading 95% as a probability for the computed interval.** For the sleep data, $\mu$ is in $[0.7001, 2.4599]$ or not; the 0.95 is the long-run hit rate of the procedure.
- **Using $z$ quantiles with $S$.** At $n = 5$ the interval $\bar X \pm 1.96\,S/\sqrt n$ covers only about 0.88.
- **Trusting one-sided bounds on skewed data.** The upper 95% bound for exponential data covers 0.84 at $n = 5$ and 0.93 at $n = 100$.
- **Applying it to dependent data.** Autocorrelated measurements make $S/\sqrt n$ a wrong standard error, and the coverage can be far from nominal at any $n$.
- **Comparing two groups by overlap of their intervals.** Two 95% intervals can overlap while the two-sample test rejects at 5%; use an interval for the difference.
- **Choosing the level after seeing the data.** Picking the level that just excludes 0 turns the interval into a p-value with the wrong meaning.

## Implementations

## History

Student's 1908 paper gave the law of $(\bar x - \mu)/s$ for normal samples and used it to state probable limits for a mean. R. A. Fisher reached the same numerical limits with his fiducial argument from 1930. Jerzy Neyman's 1937 paper in the Philosophical Transactions of the Royal Society set out the theory of confidence intervals: a confidence coefficient is the probability, over repeated samples, that the random interval covers the fixed parameter, and a computed interval either contains the parameter or does not. The t interval is the standard example of that theory.

## References
