---
tag: PZWGTN
kind: algorithm
slug: z-test
name: Z-test
aliases:
- normal test
- one-sample z-test
area: statistics-and-inference/hypothesis-testing
level: intro
summary: Tests a mean or proportion with a statistic that is standard normal under the null. Exact for normal data with known sigma, asymptotic for proportions. O(n) time.
model: real-ram
complexity:
  vars: {n: the number of observations}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1925
  people: [Ronald A. Fisher]
  note: Fisher's Statistical Methods for Research Workers (1925) tabulated the normal deviate and gave 1.96 as the two-sided 5% point, which made the comparison of a standardized mean with the normal table a standard test.
prereqs: [statistical-hypothesis-test, p-value, standard-error, central-limit-theorem]
see_also: [student-t-test, t-confidence-interval, statistical-power, sample-size-determination, binomial-test, wald-test, score-test, test-interval-duality]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 8.3.1 (error probabilities and the power function, with the normal mean test), Section 8.3.4 (p-values) and Section 10.3 (large-sample tests)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Chapter 3 (uniformly most powerful one-sided tests) and Chapter 4 (unbiased tests, the two-sided case)
  - book: isbn:9780387402727
    title: Larry Wasserman, All of Statistics, Springer, 2004
    locator: Section 10.1 (the Wald test, with the test of a mean and of a proportion) and Section 10.2 (p-values)
  - url: https://psychclassics.yorku.ca/Fisher/Methods/
    title: Ronald A. Fisher, Statistical Methods for Research Workers, Oliver and Boyd, 1925, online text of the first edition
    locator: Chapter III, Section 12 (the normal distribution and the 5% point 1.96)
---

The z-test is a [statistical hypothesis test](/statistical-hypothesis-test/) whose statistic is a difference between an estimate and its null value, divided by a known [standard error](/standard-error/), so that the statistic is standard normal under the null hypothesis. For iid normal data with a known standard deviation $\sigma$, the null distribution is exactly $N(0, 1)$ for every sample size, and the test has size exactly $\alpha$. For a proportion, and for any mean when $\sigma$ is replaced by a large-sample value, the normal law holds only in the limit, by the [central limit theorem](/central-limit-theorem/), and the size is only near $\alpha$. The computation is one pass over the data and one evaluation of the normal tail.

## In plain words

You know how much single measurements scatter. You want to know if their true average is some claimed value. Take the average of your measurements, subtract the claimed value, and divide by the typical scatter of an average of that many measurements. The result counts how many "typical errors" the average is away from the claim. If the claim is right, this count behaves like a draw from the bell curve, so you know how often it lands far from zero by chance. A count of about two or more is rare: it happens about one time in twenty. When it happens, you reject the claim. The same idea tests a share of yes answers, but there the bell curve is only an approximation that improves as the sample grows.

## The problem

**One-sample test of a mean.** The data are $X_1, \dots, X_n$ iid $N(\mu, \sigma^2)$, with $\sigma > 0$ known and $\mu$ unknown. The null hypothesis is $H_0: \mu = \mu_0$. The alternative is two-sided, $H_1: \mu \ne \mu_0$, or one-sided, $H_1: \mu > \mu_0$ ("greater") or $H_1: \mu < \mu_0$ ("less"). For a one-sided alternative the null can also be the composite $\mu \le \mu_0$ (or $\mu \ge \mu_0$), with the same test.

**Statistic.** With the sample mean $\bar X = \frac1n\sum X_i$,

$$Z = \frac{\bar X - \mu_0}{\sigma/\sqrt n}.$$

**Null distribution.** Exact: $Z \sim N(0, 1)$ under $H_0$ for every $n \ge 1$. In general $Z \sim N(\lambda, 1)$ with $\lambda = \sqrt n(\mu - \mu_0)/\sigma$.

**Rejection rule and size.** At level $\alpha$, with the lower quantiles $z_p$ of $N(0, 1)$: reject when $|Z| \ge z_{1-\alpha/2}$ (two-sided), $Z \ge z_{1-\alpha}$ ("greater") or $Z \le z_\alpha$ ("less"). The size equals $\alpha$ exactly. For $\alpha = 0.05$, $z_{0.975} \approx 1.959964$ and $z_{0.95} \approx 1.644854$.

**p-value.** With the observed value $z$ and $\bar\Phi(z) = 1 - \Phi(z)$ the upper tail: $p = \bar\Phi(z)$ ("greater"), $p = \Phi(z)$ ("less"), and $p = 2\bar\Phi(|z|)$ (two-sided). The null law is symmetric, so doubling the smaller tail and summing the outcomes no more likely than the observed one give the same two-sided p-value.

**Sensitivity and power.** The test reacts to a shift of the mean. Its [power](/statistical-power/) at $\mu$ is, for the two-sided test,

$$\pi(\mu) = \Phi(\lambda - z_{1-\alpha/2}) + \Phi(-\lambda - z_{1-\alpha/2}), \qquad \lambda = \frac{\sqrt n(\mu - \mu_0)}{\sigma},$$

and $\Phi(\lambda - z_{1-\alpha})$ for "greater". The one-sided test is uniformly most powerful for its alternative (by the [Neyman-Pearson lemma](/neyman-pearson-lemma/) and the [Karlin-Rubin theorem](/karlin-rubin-theorem/)), and the two-sided test is uniformly most powerful among unbiased tests (Lehmann and Romano, Chapters 3 and 4).

**Two other forms.** The two-sample test compares independent normal samples of sizes $m$ and $n$ with known $\sigma_X$ and $\sigma_Y$, with $H_0: \mu_X - \mu_Y = \delta_0$ and $Z = (\bar X - \bar Y - \delta_0)/\sqrt{\sigma_X^2/m + \sigma_Y^2/n}$; it is exact. The one-proportion test takes $K$ successes in $n$ Bernoulli trials ([binomial distribution](/binomial-distribution/)), $H_0: p = p_0$, and $Z = (K - np_0)/\sqrt{np_0(1 - p_0)}$, with the standard error computed at $p_0$. Its null distribution is $N(0, 1)$ only asymptotically, so its size is only near $\alpha$.

## The algorithm

```pseudo id=main
Z-TEST(x[1..n], μ₀, σ, alternative)        ▷ σ > 0 known, n ≥ 1
L1  n ← the length of x
L2  s ← x[1] + x[2] + ... + x[n]              ▷ an accurate sum, see below
L3  x̄ ← s / n
L4  z ← (x̄ − μ₀) / (σ / √n)
L5  return (z, NORMAL-P-VALUE(z, alternative))

NORMAL-P-VALUE(z, alternative)
L6  if alternative = two-sided then return min(1, 2 · Φ̄(|z|))
L7  if alternative = greater then return Φ̄(z)
L8  if alternative = less then return Φ(z)
```

Here $\bar\Phi(z) = \tfrac12\operatorname{erfc}(z/\sqrt2)$ and $\Phi(z) = \tfrac12\operatorname{erfc}(-z/\sqrt2)$, where erfc is the complementary error function of the math library. The test rejects at level $\alpha$ when the returned $p \le \alpha$, which is the same as the quantile rules above. The two-sample and proportion forms change only lines L1 to L4: they compute their own $z$ and call NORMAL-P-VALUE.

## Example

A filling machine is set to put 500 g in each pack, and the scatter of single packs is known from long experience: $\sigma = 4$ g. Nine packs weigh

$$502,\ 498,\ 505,\ 503,\ 501,\ 507,\ 499,\ 504,\ 506 .$$

Test $H_0: \mu = 500$ against $H_1: \mu \ne 500$ at $\alpha = 0.05$.

| step | value |
|---|---|
| L2: $s$ | $4525$ |
| L3: $\bar x = 4525/9$ | $502.7778$ |
| L4: $\sigma/\sqrt n = 4/3$ | $1.3333$ |
| L4: $z = (25/9)/(4/3) = 25/12$ | $2.0833$ |
| L6: $p = 2\bar\Phi(2.0833)$ | $0.037221$ |

Since $p = 0.0372 \le 0.05$ (equivalently $2.0833 \ge 1.959964$), the test rejects $H_0$ at the 5% level. The one-sided p-value for $H_1: \mu > 500$ is $0.018610$, half of the two-sided one. The test does not reject at the 1% level, where the two-sided critical value is $z_{0.995} \approx 2.575829$.

The power of this design ($n = 9$, $\sigma = 4$, two-sided, $\alpha = 0.05$) at a few true means:

| true $\mu$ | $\lambda = 3(\mu - 500)/4$ | power $\pi(\mu)$ |
|---|---|---|
| 500.5 | 0.375 | 0.0663 |
| 501 | 0.75 | 0.1165 |
| 502 | 1.5 | 0.3230 |
| 503 | 2.25 | 0.6141 |
| 504 | 3.0 | 0.8508 |
| 505 | 3.75 | 0.9633 |

A true overfill of 3 g is detected only 61% of the time with nine packs. [Sample size determination](/sample-size-determination/) turns this table around.

The proportion form shows what "only near $\alpha$" means. With $n = 100$ and $p_0 = 1/2$, $Z = (K - 50)/5$, and the two-sided test at $\alpha = 0.05$ rejects exactly when $|K - 50| \ge 10$. The exact size, a sum of binomial probabilities, is $0.056888$, not $0.05$. More exact sizes of the same nominal 5% test:

| $n$ | $p_0$ | exact size |
|---|---|---|
| 20 | 0.5 | 0.041389 |
| 50 | 0.5 | 0.064909 |
| 100 | 0.5 | 0.056888 |
| 1000 | 0.5 | 0.053678 |
| 30 | 0.1 | 0.025827 |
| 100 | 0.1 | 0.063602 |

The size moves above and below $\alpha$ because $K$ is discrete, and it is far from $\alpha$ when $np_0$ is small. The exact [binomial test](/binomial-test/) has size at most $\alpha$ for every $n$.

## Correctness

Under the normal model, $\bar X$ is a sum of independent normals divided by $n$, so it is normal with mean $\mu$ and variance $\sigma^2/n$. Then $Z$ is an affine function of a normal variable with mean $\lambda$ and variance 1, which is $N(0, 1)$ under $H_0$. Each p-value of lines L6 to L8 is the probability under $H_0$ of a statistic at least as extreme as $z$, and since $\Phi$ is continuous and strictly increasing, $P_{H_0}(p \le u) = u$ for each $u$, so the size is exactly $\alpha$. For the composite one-sided null $\mu \le \mu_0$, the rejection probability increases in $\mu$, so its maximum over the null is at $\mu_0$. The proportion statistic is a standardized sum of iid Bernoulli variables and converges in distribution to $N(0, 1)$ by the central limit theorem, so its size tends to $\alpha$. The proofs, with the power function and its monotonicity, are in the correctness proof below.

## Complexity

On a [real RAM](/real-ram/), lines L1 to L3 make $n$ additions and one division, line L4 a constant number of operations, and lines L6 to L8 one evaluation of erfc. So the time is $\Theta(n)$ and the extra space is $\Theta(1)$. The test is online: the running sum can take one observation at a time, and $z$ is available after each one. The proportion form needs only $K$ and $n$, so it costs $O(1)$ after counting.

**Numerical stability.** Two places lose accuracy if they are written carelessly.

- **The upper tail.** For large $z$, computing $1 - \Phi(z)$ cancels: in double precision $1 - \Phi(9)$ is exactly 0, while $\bar\Phi(9) = 1.1286 \times 10^{-19}$. Line L7 evaluates $\tfrac12\operatorname{erfc}(z/\sqrt2)$ directly, which keeps its relative accuracy far into the tail. This is [catastrophic cancellation](/catastrophic-cancellation/) in its simplest form.
- **The sum.** A naive running sum of $n$ numbers has a rounding error that can grow like $n$ times the unit roundoff times the sum of the absolute values. When the mean is close to $\mu_0$ and the values are large (a mean of 500.001 tested against 500), this error can be a large part of $\bar x - \mu_0$. The implementation uses an exactly rounded sum (math.fsum); [Kahan summation](/kahan-summation/) or [pairwise summation](/pairwise-summation/) also work. Subtracting $\mu_0$ from each value before summing is another remedy.

## Properties

- **Exact under its model.** For iid normal data with known $\sigma$, size and power are given by closed forms for every $n$. Nothing is asymptotic.
- **Uniform p-value.** Under a simple null the p-value is uniform on $(0, 1)$, because the null distribution is continuous.
- **Optimal.** The one-sided test is uniformly most powerful at its level, and the two-sided test is uniformly most powerful unbiased. No other level-$\alpha$ test of $\mu = \mu_0$ with known $\sigma$ has more power at every alternative in its class.
- **Dual to an interval.** The two-sided test at level $\alpha$ fails to reject $\mu_0$ exactly when $\mu_0$ lies in $\bar X \pm z_{1-\alpha/2}\,\sigma/\sqrt n$. For the example this interval is $[500.16, 505.39]$, which excludes 500. See [test-interval duality](/test-interval-duality/).
- **Robust in level for large $n$, not for small $n$.** If the data are not normal but iid with finite variance $\sigma^2$ (still known), $Z$ converges in distribution to $N(0, 1)$ and the size tends to $\alpha$. For small $n$ and skewed data the one-sided size can be far off.
- **Scale and location equivariant.** Changing the unit of measurement or shifting all values and $\mu_0$ together leaves $z$ and $p$ unchanged.

## Variants and improvements

- **[Student's t-test](/student-t-test/).** When $\sigma$ is unknown, replace it by the sample standard deviation $S$ (divisor $n - 1$). The statistic then has the t distribution with $n - 1$ degrees of freedom, not $N(0, 1)$. Using the z critical value with $S$ makes the test anti-conservative for small $n$: with $n = 5$, $P(|T| \ge 1.96) \approx 0.12$ under the null.
- **Large-sample z-test with estimated $\sigma$.** For large $n$ and any iid data with finite variance, $(\bar X - \mu_0)/(S/\sqrt n)$ converges in distribution to $N(0, 1)$, by the central limit theorem and [Slutsky's theorem](/slutsky-theorem/). This is the [Wald test](/wald-test/) for a mean. The size is only near $\alpha$.
- **Proportion test with $\hat p$ in the standard error.** Using $\sqrt{\hat p(1 - \hat p)/n}$ gives the Wald test for a proportion, whose size and interval coverage are worse than with $p_0$. The version on this page, with $p_0$, is the [score test](/score-test/), and inverting it gives the [Wilson score interval](/wilson-score-interval/).
- **Two proportions.** The same idea with the pooled estimate of $p$ under $H_0$ gives the two-proportion z-test. Its square is the chi-square statistic of a $2 \times 2$ table.
- **Continuity correction.** Subtracting $1/2$ from $|K - np_0|$ moves the size of the proportion test toward the exact binomial test. With small $n$, use the [binomial test](/binomial-test/) itself.

## When to use it

Use the normal-data z-test when $\sigma$ really is known from outside the sample: a calibrated instrument, a process with a long stable record, or a simulation where the variance is a design choice. Use the large-sample form for means and proportions when $n$ is large, and say that the size is approximate. When $\sigma$ is estimated from a small or moderate sample, use the [t-test](/student-t-test/), and for a proportion with small $n$ or extreme $p_0$, use the exact [binomial test](/binomial-test/).

## Pitfalls

- **Plugging in $S$ for $\sigma$ with a small sample.** The statistic is then t-distributed, and the z critical value rejects too often. The real size is 0.122, about 2.4 times the nominal size, at $n = 5$ and $\alpha = 0.05$.
- **Computing the p-value as $1 - \Phi(z)$.** For $z \ge 8.3$ this returns 0 in double precision. Report the upper tail with erfc.
- **Reading the asymptotic size as exact.** The proportion test at $n = 50$, $p_0 = 1/2$ has size 0.065, not 0.05. State the exact size or use an exact test.
- **Choosing the side after seeing the data.** A one-sided p-value is half the two-sided one. Picking the side that matches the observed sign doubles the real type I error rate.
- **Treating "not significant" as "no effect".** In the example design, a true shift of 2 g is missed 68% of the time. A large p-value says that the data are compatible with $H_0$, and also with many alternatives. Look at the power or the interval.

## Implementations

## History

Fisher's Statistical Methods for Research Workers (1925) gave tables of the normal distribution in a form for testing and named 1.96, "or nearly 2", as the deviation exceeded with probability 0.05. Comparing a standardized mean or proportion with the normal law is older: it rests on the normal approximation and the [central limit theorem](/central-limit-theorem/). In the Neyman-Pearson theory of the 1930s, the one-sided z-test became the standard example of a uniformly most powerful test.

## References
