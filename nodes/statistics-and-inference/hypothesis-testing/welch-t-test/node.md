---
tag: C3KW5Q
kind: algorithm
slug: welch-t-test
name: Welch's t-test
aliases:
- unequal variances t-test
- Welch-Satterthwaite approximation
area: statistics-and-inference/hypothesis-testing
level: core
summary: Compares two normal means without assuming equal variances, using separate variance estimates and Welch-Satterthwaite degrees of freedom. Approximate, not exact. O(m + n).
model: real-ram
complexity:
  vars: {m: the size of the first sample, n: the size of the second sample}
  time: {worst: Θ(m + n), best: Θ(m + n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1947
  people: [Bernard Lewis Welch, Franklin E. Satterthwaite]
  note: Satterthwaite gave the effective degrees of freedom of a combination of variance estimates in 1941 and 1946. Welch derived the two-sample test with this approximation and its refinements in Biometrika in 1947.
prereqs: [student-t-test, sample-variance, standard-error]
see_also: [t-confidence-interval, statistical-power, sample-size-determination, effect-size, mann-whitney-u-test, permutation-test, bootstrap-method, one-way-anova]
sources:
  - paper: doi:10.1093/biomet/34.1-2.28
    title: "B. L. Welch, The generalization of 'Student's' problem when several different population variances are involved, Biometrika 34(1-2), 1947, pp. 28 to 35"
    locator: The whole paper (the statistic with separate variance estimates, the approximate degrees of freedom and the higher-order corrections)
  - paper: doi:10.2307/3002019
    title: "F. E. Satterthwaite, An approximate distribution of estimates of variance components, Biometrics Bulletin 2(6), 1946, pp. 110 to 114"
    locator: The whole paper (a linear combination of independent mean squares approximated by a scaled chi-square law with matched first two moments)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 5.3 (sampling from the normal distribution, the chi-square and t laws used in the derivation) and Chapter 8 (two-sample tests of means)
---

Welch's t-test is a [statistical hypothesis test](/statistical-hypothesis-test/) for the difference of the means of two independent normal samples whose variances may differ. It divides the difference of the sample means by the square root of $S_X^2/m + S_Y^2/n$, where each [sample variance](/sample-variance/) has its own divisor $m - 1$ or $n - 1$, and it refers the result to a t distribution with the Welch-Satterthwaite degrees of freedom, a real number between $\min(m, n) - 1$ and $m + n - 2$. The test is approximate: its size is not exactly $\alpha$, but it stays close to $\alpha$ in cases where the pooled [Student t-test](/student-t-test/) fails badly.

## In plain words

You compare the averages of two separate groups, and the two groups may scatter by different amounts. The pooled t-test assumes equal scatter and mixes the two scatters into one. When the small group is the noisy one, that mixed value is too small, the test sees differences that are only noise, and it cries "significant" far too often. Welch's test keeps the two scatters apart and adds up the uncertainty of each average separately. The cost is that the exact law of the resulting count is unknown. Welch and Satterthwaite matched it to the closest t law, with a number of degrees of freedom computed from the data. The match is not perfect, but it is good in most practical cases.

## The problem

**Model and hypotheses.** $X_1, \dots, X_m$ iid $N(\mu_X, \sigma_X^2)$ and $Y_1, \dots, Y_n$ iid $N(\mu_Y, \sigma_Y^2)$, the two samples independent, $m, n \ge 2$, with $\mu_X, \mu_Y, \sigma_X, \sigma_Y$ unknown and $\sigma_X \ne \sigma_Y$ allowed. $H_0: \mu_X - \mu_Y = \delta_0$ against $H_1: \mu_X - \mu_Y \ne \delta_0$ (two-sided), $> \delta_0$ ("greater") or $< \delta_0$ ("less"). The two variances are nuisance parameters. This is the Behrens-Fisher problem.

**Statistic.** With the means $\bar X, \bar Y$ and the sample variances $S_X^2, S_Y^2$ (divisors $m - 1$ and $n - 1$),

$$T = \frac{\bar X - \bar Y - \delta_0}{\sqrt{S_X^2/m + S_Y^2/n}}, \qquad \hat\nu = \frac{\big(S_X^2/m + S_Y^2/n\big)^2}{\dfrac{(S_X^2/m)^2}{m - 1} + \dfrac{(S_Y^2/n)^2}{n - 1}} .$$

**Null distribution.** Approximate: under $H_0$, $T$ is treated as $t_{\hat\nu}$. The numerator is exactly normal, but the denominator is the root of a weighted sum of two independent chi-square variables, which is not a scaled chi-square, and the exact law of $T$ depends on $\sigma_X^2/\sigma_Y^2$. The degrees of freedom $\hat\nu$ match the first two moments of the denominator to those of a scaled chi-square (the Welch-Satterthwaite approximation, below). The law of $T$ tends to $t_{m-1}$ exactly when $\sigma_Y \to 0$, and $T$ tends to $N(0, 1)$ as $m, n \to \infty$ for any populations with finite variances, by the [central limit theorem](/central-limit-theorem/) and Slutsky's theorem.

**Rejection rule and size.** Reject when $|T| \ge t_{(\hat\nu, 1-\alpha/2)}$ (two-sided), $T \ge t_{(\hat\nu, 1-\alpha)}$ ("greater") or $T \le -t_{(\hat\nu, 1-\alpha)}$ ("less"), where $t_{(\nu, p)}$ is the lower $p$ quantile of $t_\nu$ for real $\nu > 0$. The size is close to $\alpha$ but not equal to it; the table in the Example measures it.

**p-value.** With $\bar F_\nu(t) = P(T_\nu > t)$: $p = \bar F_{\hat\nu}(t)$ ("greater"), $\bar F_{\hat\nu}(-t)$ ("less") and $2\bar F_{\hat\nu}(|t|)$ (two-sided). It is an approximate p-value: under $H_0$ it is only approximately uniform.

**Sensitivity and power.** The test reacts to a shift $\mu_X - \mu_Y - \delta_0$ relative to $\sqrt{\sigma_X^2/m + \sigma_Y^2/n}$. Its [power](/statistical-power/) is close to that of the pooled test when the variances are equal and the sizes are similar, and lower when one sample is very small, because $\hat\nu$ is then small.

## The algorithm

```pseudo id=main
WELCH-T-TEST(x[1..m], y[1..n], δ₀, alternative)     ▷ m, n ≥ 2
L1  (x̄, S²_X) ← the mean of x and its variance with divisor m − 1, by two passes
L2  (ȳ, S²_Y) ← the mean of y and its variance with divisor n − 1, by two passes
L3  a ← S²_X / m;  b ← S²_Y / n
L4  t ← (x̄ − ȳ − δ₀) / √(a + b)
L5  ν ← (a + b)² / (a² / (m − 1) + b² / (n − 1))
L6  return (t, ν, T-P-VALUE(t, ν, alternative))
```

T-P-VALUE is the procedure of [Student's t-test](/student-t-test/): the upper tail of $t_\nu$, doubled for the two-sided test. It works for real $\nu$, because the shared helper evaluates $\bar F_\nu(t) = \tfrac12 I_{\nu/(\nu + t^2)}(\nu/2, 1/2)$ by the continued fraction of the regularized incomplete beta function, which does not need an integer $\nu$. If both samples are constant, $a + b = 0$ and the code raises an error. If only one is constant, $\hat\nu$ is the degrees of freedom of the other sample and the test is the one-sample t-test of that sample against the constant.

## Example

Two independent groups: $x = 13, 19, 10, 22, 16$ ($m = 5$) and $y = 11, 12, 10, 13, 11, 12, 11, 12$ ($n = 8$). Test $H_0: \mu_X = \mu_Y$ against $H_1: \mu_X \ne \mu_Y$ at $\alpha = 0.05$.

| line | value |
|---|---|
| L1: $\bar x$, $\sum (x_i - \bar x)^2$, $S_X^2 = 90/4$ | $16$, $90$, $22.5$ |
| L2: $\bar y$, $\sum (y_j - \bar y)^2$, $S_Y^2 = 6/7$ | $11.5$, $6$, $0.857143$ |
| L3: $a = 22.5/5$, $b = 0.857143/8$ | $4.5$, $0.107143$ |
| L4: $\sqrt{a + b}$ | $2.146426$ |
| L4: $t = 4.5/2.146426$ | $2.0965$ |
| L5: $\nu = 4.607143^2/(5.0625 + 0.001640)$ | $4.1914$ |
| L6: $p = 2\bar F_{4.1914}(2.0965)$ | $0.1009$ |

The critical value is $t_{(4.1914, 0.975)} = 2.7272$, and $2.0965 < 2.7272$, so the test does not reject. Almost all the uncertainty comes from the small noisy group, so $\hat\nu$ is close to its $m - 1 = 4$. The dual 95% interval for $\mu_X - \mu_Y$ is $4.5 \pm 2.7272 \times 2.146426 = [-1.354, 10.354]$.

The pooled test on the same data uses $S_p^2 = 96/11 = 8.7273$ (divisor $m + n - 2 = 11$), the standard error $\sqrt{8.7273(1/5 + 1/8)} = 1.6842$, $t = 2.6720$ with 11 degrees of freedom and $p = 0.0217$, and rejects. The quiet group of 8 dominates $S_p^2$ and makes the standard error too small; the table below shows that the pooled test rejects a true null far too often in exactly this situation.

**Size under the model.** Monte Carlo with $r = 20000$ replications at level 0.05, two-sided, normal data with equal means, seed 11, the same simulated data for both tests (standard error of an estimated size near 0.05: 0.0015):

| $m$, $\sigma_X$ | $n$, $\sigma_Y$ | Welch size | pooled size |
|---|---|---|---|
| 5, 3 | 25, 1 | 0.0530 | 0.2998 |
| 5, 1 | 25, 3 | 0.0485 | 0.0012 |
| 5, 1 | 25, 1 | 0.0577 | 0.0505 |
| 3, 1 | 3, 1 | 0.0354 | 0.0508 |
| 3, 3 | 3, 1 | 0.0499 | 0.0734 |
| 2, 1 | 20, 1 | 0.1191 | 0.0475 |
| 2, 5 | 20, 1 | 0.0895 | 0.5489 |
| 10, 2 | 10, 1 | 0.0490 | 0.0529 |
| 4, 1 | 4, 10 | 0.0511 | 0.0855 |

Where the variances differ, the Welch size stays within 0.004 of 0.05 in every row with both sizes at least 3, while the pooled size ranges from 0.001 to 0.55. Where the variances are equal, the pooled test is exact and Welch is off: slightly with $m = 5$, conservative with $m = n = 3$, and badly with $m = 2$, where $\hat\nu$ can be as low as 1 and its randomness matters most.

## Correctness

Within each sample, the mean and the sample variance are independent (Helmert's transformation), so the numerator of $T$ is exactly normal and independent of the denominator. The denominator squared, $A + B$ with $A = S_X^2/m$ and $B = S_Y^2/n$, has mean $\theta = \sigma_X^2/m + \sigma_Y^2/n$ and variance $2(\sigma_X^2/m)^2/(m - 1) + 2(\sigma_Y^2/n)^2/(n - 1)$. A scaled chi-square $\theta\chi^2_\nu/\nu$ with the same two moments has $\nu = 2\theta^2/\operatorname{Var}(A + B)$, and replacing the unknown variances by their estimates gives $\hat\nu$. Cauchy-Schwarz gives $\min(m, n) - 1 \le \hat\nu \le m + n - 2$, with the top value exactly when $A/(m - 1) = B/(n - 1)$. With $m = n$, $T$ equals the pooled statistic. The size tends to $\alpha$ when one variance tends to 0 (the test becomes the exact one-sample t-test of the other sample) and when $m, n \to \infty$. Nothing more is proved; between those limits the size is measured. The proofs are in the correctness proof below.

## Complexity

On a [real RAM](/real-ram/), lines L1 and L2 make two passes over each sample, about $4(m + n)$ arithmetic operations, and L3 to L5 are a constant number of operations. So the time is $\Theta(m + n)$ and the extra space is $\Theta(1)$ besides the data. The tail $\bar F_{\hat\nu}$ costs a number of continued fraction steps that does not grow with $m$ or $n$ for the values that matter. The two-pass variances avoid the [catastrophic cancellation](/catastrophic-cancellation/) of the one-pass formula, as on the Student page.

## Properties

- **Approximate.** The size depends on $m$, $n$ and the variance ratio, and in general differs from $\alpha$; it tends to $\alpha$ as one variance dominates or as both sizes grow.
- **Degrees of freedom bounds.** $\min(m, n) - 1 \le \hat\nu \le m + n - 2$. $\hat\nu$ is a random variable, not a fixed count.
- **Same statistic as pooled at equal sizes.** With $m = n$ the two statistics agree and only the degrees of freedom differ, $\hat\nu \le 2n - 2$. For the sleep data of Cushny and Peebles read as two groups of 10, $|t| = 1.8608$ for both, with $\hat\nu = 17.776$ and $p = 0.0794$ against 18 and $0.0792$.
- **Invariant.** $T$ and $\hat\nu$ do not change when both samples and $\delta_0$ are shifted together, or when both samples are scaled by the same positive factor (with $\delta_0$ scaled too).
- **Limited by the smaller sample.** The quality of the approximation depends on the smaller sample: with $m = 2$ the size can be more than twice $\alpha$.

## Variants and improvements

- **Welch-Satterthwaite approximation in general.** For a combination $\sum_i c_i S_i^2$ of independent variance estimates with $\nu_i$ degrees of freedom each, the effective degrees of freedom are $\big(\sum_i c_i S_i^2\big)^2 / \sum_i (c_i S_i^2)^2/\nu_i$. The two-sample test is the case $c_1 = 1/m$, $c_2 = 1/n$. The same formula gives approximate degrees of freedom in mixed-effects models and for combined measurement uncertainties.
- **Welch interval.** By test-interval duality, $\bar X - \bar Y \pm t_{(\hat\nu, 1-\alpha/2)}\sqrt{S_X^2/m + S_Y^2/n}$ is an approximate $1 - \alpha$ interval for $\mu_X - \mu_Y$; its coverage error is the size error of the test.
- **Conservative degrees of freedom.** Older texts use $\min(m, n) - 1$ in place of $\hat\nu$. By the lower bound this gives a larger critical value at the usual levels, so it rejects less often than the Welch rule on the same data.
- **Several groups.** Welch also gave an analogue of [one-way ANOVA](/one-way-anova/) for several means with unequal variances.
- **Resampling and rank tests.** The [bootstrap](/bootstrap-method/) of the Welch statistic is also approximate. The [Mann-Whitney U test](/mann-whitney-u-test/) and the [permutation test](/permutation-test/) are exact only for the hypothesis that both samples have the same distribution, which includes equal variances, so they do not solve the Behrens-Fisher problem either.

## When to use it

Use Welch's test to compare the means of two independent groups of roughly normal data, or of larger groups of any shape with finite variance, whenever the variances are not known to be equal. Many texts now make it the default two-sample t-test: when the variances are equal it loses little against the pooled test, and when they differ it keeps the size near $\alpha$ while the pooled test can have a size of 0.30 or 0.001. For paired data use the paired t-test instead. With a group of 2 or 3 observations, treat its p-value as rough.

## Pitfalls

- **Treating the test as exact.** It is an approximation; with $m = 2$ and equal variances the measured size is 0.119 at nominal 0.05.
- **Rounding $\hat\nu$ to an integer before looking up a table.** This is unnecessary with a tail function that accepts real $\nu$, and rounding down or up changes the p-value.
- **Choosing between pooled and Welch by a preliminary test of equal variances.** The two-stage procedure does not have the nominal size, and the variance test has little power at the small sizes where the choice matters.
- **Using it on paired data.** The groups must be independent; for paired measurements the test ignores the pairing and loses power.
- **Reading the degrees of freedom as a sample size.** $\hat\nu$ is a property of the variance estimate and changes from sample to sample.

## Implementations

## History

The problem of comparing two normal means with unknown and possibly unequal variances was posed by W.-U. Behrens in 1929, and R. A. Fisher gave a fiducial solution in 1935, so the problem carries both names. Neither gave a test whose size is exactly $\alpha$ for all variance ratios. F. E. Satterthwaite approximated the law of a linear combination of independent mean squares by a scaled chi-square with matched mean and variance, in 1941 and in the Biometrics Bulletin in 1946. B. L. Welch, in Biometrika in 1947, studied the statistic with separate variance estimates, gave the same approximate degrees of freedom for the two-sample case and higher-order corrections, and so gave the test its name.

## References
