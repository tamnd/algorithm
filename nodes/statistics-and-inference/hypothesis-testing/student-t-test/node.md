---
tag: M2JJ9R
kind: algorithm
slug: student-t-test
name: Student's t-test
aliases:
- one-sample t-test
- two-sample t-test
- paired t-test
area: statistics-and-inference/hypothesis-testing
level: intro
summary: Tests a normal mean, or two means, by the estimate over its estimated standard error. Exact t null law under normal iid data; the pooled form needs equal variances. O(n).
model: real-ram
complexity:
  vars: {n: the number of observations or pairs}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1908
  people: [William Sealy Gosset, Ronald A. Fisher]
  note: Gosset, a brewer at Guinness writing as Student, derived the small-sample law of the standardized mean in 1908. Fisher gave the t form with divisor n - 1 and the two-sample and regression uses in 1925.
prereqs: [z-test, p-value, sample-variance, standard-error]
see_also: [welch-t-test, t-confidence-interval, statistical-power, sample-size-determination, effect-size, wilcoxon-signed-rank-test, mann-whitney-u-test, one-way-anova]
sources:
  - paper: doi:10.1093/biomet/6.1.1
    title: "Student, The probable error of a mean, Biometrika 6(1), 1908, pp. 1 to 25"
    locator: The whole paper (the law of the standardized mean for normal samples, its table, and the sleep data of Cushny and Peebles as the worked example)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 5.3 (sampling from the normal distribution, the independence of X-bar and S^2, Student's t) and Chapter 8 (the one-sample t-test as a likelihood ratio test, its size and power)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Section 5.2 (testing the parameters of a normal distribution, the one-sample t-test as UMP unbiased) and Chapter 5 (the two-sample and paired comparisons)
  - url: https://psychclassics.yorku.ca/Fisher/Methods/
    title: Ronald A. Fisher, Statistical Methods for Research Workers, Oliver and Boyd, 1925, online text of the first edition
    locator: Chapter V (tests of significance of means, differences of means and regression coefficients)
---

Student's t-test is a [statistical hypothesis test](/statistical-hypothesis-test/) for a mean, or for a difference of two means, when the standard deviation is unknown. It divides the estimate minus its null value by the estimated [standard error](/standard-error/), which uses the [sample variance](/sample-variance/) $S^2$ with divisor $n - 1$. Under iid normal data, the statistic has the t distribution with $n - 1$ degrees of freedom exactly, for every $n \ge 2$, so the test has size exactly $\alpha$. It has three forms: one-sample, paired (the one-sample test on the differences) and pooled two-sample, which needs equal variances in the two groups.

## In plain words

You have a few measurements and want to know if their true average is some claimed value, but you do not know how much single measurements scatter. So you estimate the scatter from the same measurements. Then you count how many estimated "typical errors" the average is away from the claim, as in the z-test. Because the scatter itself is a guess, the count varies more than a bell curve does, most of all with few measurements. Student worked out the exact law of this count for data from a bell curve, and it has heavier tails. So the cutoff for "rare" is a bit larger than two. With before and after values on the same subjects, test the differences. With two separate groups, the pooled version assumes that both groups scatter equally.

## The problem

**One-sample test.** $X_1, \dots, X_n$ are iid $N(\mu, \sigma^2)$ with both $\mu$ and $\sigma$ unknown, $n \ge 2$. $H_0: \mu = \mu_0$ against $H_1: \mu \ne \mu_0$ (two-sided), $\mu > \mu_0$ ("greater") or $\mu < \mu_0$ ("less"); for a one-sided alternative the null may be the composite $\mu \le \mu_0$ or $\mu \ge \mu_0$. The standard deviation $\sigma$ is a nuisance parameter.

**Statistic.** With $\bar X = \frac1n\sum X_i$ and $S^2 = \frac{1}{n-1}\sum (X_i - \bar X)^2$ (divisor $n - 1$),

$$T = \frac{\bar X - \mu_0}{S/\sqrt n}.$$

**Null distribution.** Exact: $T \sim t_{n-1}$ under $H_0$, whatever $\sigma$ is. The reason is that $\bar X$ and $S^2$ are independent under normality, and $(n - 1)S^2/\sigma^2$ is chi-square with $n - 1$ degrees of freedom. Without normality, for iid data with finite variance, $T$ converges in distribution to $N(0, 1)$ by the [central limit theorem](/central-limit-theorem/) and Slutsky's theorem, so the test is only asymptotic.

**Rejection rule and size.** With the lower quantile $t_{(n-1, p)}$: reject when $|T| \ge t_{(n-1, 1-\alpha/2)}$ (two-sided), $T \ge t_{(n-1, 1-\alpha)}$ ("greater") or $T \le -t_{(n-1, 1-\alpha)}$ ("less"). Under normality the size equals $\alpha$, also for the composite one-sided null. For $\alpha = 0.05$ two-sided, $t_{(4, 0.975)} = 2.776445$, $t_{(9, 0.975)} = 2.262157$, $t_{(30, 0.975)} = 2.042272$, and the limit is $z_{0.975} = 1.959964$.

**p-value.** With $\bar F_\nu(t) = P(T_\nu > t)$ the upper tail of $t_\nu$: $p = \bar F_{n-1}(t)$ ("greater"), $\bar F_{n-1}(-t)$ ("less") and $2\bar F_{n-1}(|t|)$ (two-sided). The null law is symmetric, so doubling and the "no more likely" rule agree.

**Paired test.** Pairs $(X_i, Y_i)$, iid over $i$, measured on the same unit. With $D_i = X_i - Y_i$ iid $N(\delta, \sigma_D^2)$, test $H_0: \delta = \delta_0$ by the one-sample test on $D_1, \dots, D_n$, with $n - 1$ degrees of freedom. The pairs may be correlated; only the differences must be iid normal.

**Pooled two-sample test.** $X_1, \dots, X_m$ iid $N(\mu_X, \sigma^2)$ and $Y_1, \dots, Y_n$ iid $N(\mu_Y, \sigma^2)$, independent, with the same $\sigma$. With $S_p^2 = \big(\sum (X_i - \bar X)^2 + \sum (Y_j - \bar Y)^2\big)/(m + n - 2)$ (divisor $m + n - 2$),

$$T = \frac{\bar X - \bar Y - \delta_0}{S_p\sqrt{1/m + 1/n}} \sim t_{m+n-2} \quad \text{under } H_0: \mu_X - \mu_Y = \delta_0 .$$

The equal variance assumption is essential; see Pitfalls and the [Welch t-test](/welch-t-test/).

**Sensitivity and power.** The test reacts to a shift of the mean relative to the scatter. Its [power](/statistical-power/) depends on $\mu$ and $\sigma$ only through $\lambda = \sqrt n(\mu - \mu_0)/\sigma$: $T$ then has the noncentral t law with $n - 1$ degrees of freedom and noncentrality $\lambda$. With 10 observations at $\alpha = 0.05$ two-sided, the power is 0.293 at $\lambda/\sqrt n = 0.5$ and 0.803 at $\lambda/\sqrt n = 1$, against 0.353 and 0.885 for the [z-test](/z-test/) with $\sigma$ known. That gap is the price of estimating $\sigma$. The one-sided t-test is uniformly most powerful among unbiased tests, and so is the two-sided one (Lehmann and Romano, Section 5.2). The power computation is on [sample size determination](/sample-size-determination/).

## The algorithm

```pseudo id=main
STUDENT-T-TEST(x[1..n], μ₀, alternative)     ▷ n ≥ 2
L1  n ← the length of x
L2  x̄ ← (x[1] + ... + x[n]) / n
L3  S² ← ((x[1] − x̄)² + ... + (x[n] − x̄)²) / (n − 1)   ▷ second pass, divisor n − 1
L4  t ← (x̄ − μ₀) / √(S² / n)
L5  ν ← n − 1
L6  return (t, ν, T-P-VALUE(t, ν, alternative))

T-P-VALUE(t, ν, alternative)
L7  if alternative = two-sided then return min(1, 2 · F̄_ν(|t|))
L8  if alternative = greater then return F̄_ν(t)
L9  if alternative = less then return F̄_ν(−t)
```

The upper tail is $\bar F_\nu(t) = \tfrac12 I_{\nu/(\nu + t^2)}(\nu/2, 1/2)$ for $t \ge 0$, where $I_x(a, b)$ is the regularized incomplete beta function. The helper evaluates it by its continued fraction, so a tail of $10^{-19}$ keeps its digits. The paired test calls STUDENT-T-TEST on $x_i - y_i$. The pooled test computes both means and both sums of squared deviations by two passes, forms $S_p^2$, and calls T-P-VALUE with $\nu = m + n - 2$. If $S = 0$ (all values equal), $t$ is undefined and the code raises an error.

## Example

Student's 1908 paper used the sleep data of Cushny and Peebles: the extra hours of sleep of 10 patients under two drugs. Each patient took both drugs, so the data are paired. The differences (drug 2 minus drug 1) are

$$1.2,\ 2.4,\ 1.3,\ 1.3,\ 0.0,\ 1.0,\ 1.8,\ 0.8,\ 4.6,\ 1.4 .$$

Test $H_0: \delta = 0$ against $H_1: \delta \ne 0$ at $\alpha = 0.05$.

| line | value |
|---|---|
| L2: $\bar d = 15.8/10$ | $1.58$ |
| L3: $\sum (d_i - \bar d)^2$ | $13.616$ |
| L3: $S^2 = 13.616/9$ | $1.512889$ |
| L4: $S/\sqrt{10}$ | $0.388959$ |
| L4: $t = 1.58/0.388959$ | $4.0621$ |
| L5: $\nu$ | $9$ |
| L7: $p = 2\bar F_9(4.0621)$ | $0.002833$ |

Since $4.0621 \ge t_{(9, 0.975)} = 2.262157$, the test rejects $H_0$; the second drug gave more sleep. The one-sided p-value for $H_1: \delta > 0$ is $0.001416$.

**Ignoring the pairing.** Treat the same 20 numbers as two independent groups of 10 and run the pooled test. Then $t = 1.8608$ with $\nu = 18$ and $p = 0.0792$: no rejection at 5%. The between-patient variation, which the differences cancel, now enters the standard error. The paired design is the right one here, and the pooled analysis of paired data is a design error, not a choice of test.

**Size under the model and outside it.** Monte Carlo with $r = 4000$ replications at level 0.05 (standard error of an estimated size near 0.05: 0.0034):

| data | test | measured size | seed |
|---|---|---|---|
| normal, $n = 5$ | one-sample, two-sided | 0.0478 | 1 |
| exponential with mean 1, $n = 5$ | one-sample, two-sided | 0.1235 | 2 |
| exponential with mean 1, $n = 5$ | one-sample, "greater" / "less" | 0.0115 / 0.1553 | 2 |
| exponential with mean 1, $n = 30$ | one-sample, two-sided | 0.0800 | 3 |
| normal, $\sigma_X = \sigma_Y = 1$, $m = 5$, $n = 25$ | pooled | 0.0505 | 4 |
| normal, $\sigma_X = 3$, $\sigma_Y = 1$, $m = 5$, $n = 25$ | pooled | 0.3000 | 5 |
| normal, $\sigma_X = 1$, $\sigma_Y = 3$, $m = 5$, $n = 25$ | pooled | 0.0015 | 6 |
| normal, $\sigma_X = 3$, $\sigma_Y = 1$, $m = n = 15$ | pooled | 0.0593 | 7 |

The exponential rows show that skewness spoils the one-sided sizes in opposite directions and that $n = 30$ is not yet "large". The pooled rows show the failure with unequal variances and unequal sizes. When the small group is the noisy one, $S_p^2$ is dominated by the quiet large group. Its expectation is $(4 \cdot 9 + 24 \cdot 1)/28 = 2.143$, so the estimated variance of $\bar X - \bar Y$ is about $2.143 \times 0.24 = 0.514$, while the true variance is $9/5 + 1/25 = 1.84$. The standard error is too small by a factor $\sqrt{3.58} = 1.89$, and $P(|Z| \ge 1.96/1.89) = 0.300$, which matches the measured size. With equal sizes the error almost cancels.

## Correctness

Under iid normal data, an orthogonal change of variables (Helmert's) whose first coordinate is $\sqrt n\,\bar X$ turns the sample into $n$ independent normal coordinates. $\bar X$ depends only on the first, and $(n - 1)S^2/\sigma^2$ is the sum of squares of the other $n - 1$ standardized coordinates. So the two are independent, the second is chi-square with $n - 1$ degrees of freedom, and $T$ is a standard normal over the root of an independent chi-square divided by its degrees of freedom, which is the definition of $t_{n-1}$. The unknown $\sigma$ cancels. The same argument on both samples gives the pooled law when the variances are equal. The p-values are tail areas of a continuous symmetric law, so they are uniform under $H_0$ and the size is exactly $\alpha$. Without normality, $S \to \sigma$ in probability and Slutsky's theorem gives the normal limit. The proofs are in the correctness proof below.

## Complexity

On a [real RAM](/real-ram/), lines L2 and L3 make two passes: $n$ additions and a division for the mean, then $n$ subtractions, $n$ squarings and $n$ additions for the sum of squares. So the time is $\Theta(n)$, about $4n$ arithmetic operations, and the extra space is $\Theta(1)$ besides the stored data. The tail $\bar F_\nu$ costs a number of continued fraction steps that does not grow with $n$ for the values that matter. The pooled test is $\Theta(m + n)$.

**Numerical stability.** The one-pass formula $S^2 = (\sum x_i^2 - n\bar x^2)/(n - 1)$ subtracts two nearly equal numbers when the mean is large compared with the spread, which is [catastrophic cancellation](/catastrophic-cancellation/). For the values $10^9 + 4, 10^9 + 7, 10^9 + 13, 10^9 + 16$, whose $S^2$ is 30, it returns 0 in double precision, and with $10^{10}$ in place of $10^9$ it returns 21845.3. A variance of 0 makes $t$ infinite. Line L3 uses the two-pass formula, which subtracts the mean first. For data that arrive one at a time, the [Welford algorithm](/welford-algorithm/) gives the same accuracy in one pass. The p-value uses the upper tail directly, so a p-value of $10^{-19}$ is not rounded to 0.

## Properties

- **Exact under normality.** Size $\alpha$ for every $n \ge 2$ and every $\sigma$: the test is similar on the boundary of the null.
- **Invariant.** $T$ does not change when all data and $\mu_0$ are shifted together or scaled by a positive factor.
- **Optimal.** The two-sided t-test is the likelihood ratio test for $\mu = \mu_0$ with $\sigma$ unknown, and both the one- and two-sided forms are uniformly most powerful unbiased (Lehmann and Romano, Section 5.2).
- **Robust in level, not in power.** For symmetric non-normal data the two-sided size stays close to $\alpha$ even for moderate $n$. For skewed data the one-sided sizes are off, as the table shows. Heavy tails make $S$ large and the power low.
- **Dual to an interval.** The two-sided test at level $\alpha$ fails to reject $\mu_0$ exactly when $\mu_0$ lies in the [t confidence interval](/t-confidence-interval/) $\bar X \pm t_{(n-1, 1-\alpha/2)}S/\sqrt n$. For the sleep data this is $[0.700, 2.460]$, which excludes 0.

## Variants and improvements

- **[Welch's t-test](/welch-t-test/).** Drops the equal variance assumption for two samples. It is approximate, but its size stays near $\alpha$ where the pooled test fails. Many texts now use it as the default two-sample test.
- **Rank tests.** The [Wilcoxon signed-rank test](/wilcoxon-signed-rank-test/) (one-sample or paired) and the [Mann-Whitney U test](/mann-whitney-u-test/) (two samples) have exact null laws for continuous data without normality: the first needs a distribution symmetric about the null value, the second two samples from the same distribution.
- **[Permutation test](/permutation-test/).** Uses the t statistic but takes its null distribution from the permutations or sign flips of the data, which is exact under exchangeability.
- **More than two groups.** [One-way ANOVA](/one-way-anova/) generalizes the pooled test: with two groups, its F statistic is $T^2$.
- **Equivalence testing.** Two one-sided t-tests (TOST) show that a mean lies within a margin, which a non-significant t-test cannot show.

## When to use it

Use the one-sample or paired t-test for a mean when $\sigma$ is unknown and the data, or the differences, are close to normal, or when $n$ is large and the data are not strongly skewed. Use the paired form whenever the two measurements come from the same unit. For two independent groups, use the pooled form only when the variances are known to be equal or the group sizes are equal; otherwise use the [Welch t-test](/welch-t-test/). For small samples from a clearly skewed or heavy-tailed population, use a rank or permutation test.

## Pitfalls

- **Pooling with unequal variances and unequal sizes.** The size can be 0.30 instead of 0.05 (table above). Equal sizes protect the level; equal variances are rarely known.
- **Ignoring the pairing.** The pooled analysis of paired data includes the between-unit variation, and the sleep data lose their significance.
- **Pairing independent samples.** The paired test on two independent groups of equal size, matched by position, throws away $n - 1$ degrees of freedom and depends on an arbitrary order.
- **Using $z$ critical values.** With $n = 5$, $|T| \ge 1.96$ has null probability 0.122, not 0.05.
- **Reading the asymptotic claim as exact.** Outside normality the t-test is asymptotic only: for exponential data with $n = 5$ the "less" size is 0.155.
- **Testing for normality first and then choosing the test.** The two-stage procedure does not have the nominal size, and a normality test has little power at the small $n$ where it matters.

## Implementations

## History

William Sealy Gosset, a chemist and brewer at Guinness in Dublin, published "The probable error of a mean" in Biometrika in 1908 under the name Student. He derived the law of the mean divided by the sample standard deviation for normal samples, checked it with a sampling experiment on measurements written on cards, and applied it to the Cushny and Peebles sleep data. Student's statistic was $z = (\bar x - \mu)/s$, with $s$ computed with the divisor $n$. Fisher gave a full derivation, wrote the statistic as $t$ with the divisor $n - 1$, and extended it to the comparison of two means and to regression coefficients in Statistical Methods for Research Workers (1925).

## References
