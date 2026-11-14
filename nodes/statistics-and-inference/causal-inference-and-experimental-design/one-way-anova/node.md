---
tag: QHQ1W6
kind: algorithm
slug: one-way-anova
name: One-way analysis of variance
aliases:
- one-way ANOVA
- ANOVA F-test
area: statistics-and-inference/causal-inference-and-experimental-design
level: intro
summary: Tests whether k group means are equal by the ratio of the between-group to the within-group mean square. Exact F law under normal errors with equal variances. O(N).
model: real-ram
complexity:
  vars: {n: "the total number of observations, N in the text", k: the number of groups}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(k)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1925
  people: [Ronald A. Fisher, George W. Snedecor, Bernard L. Welch]
  note: Fisher built the analysis of variance for field trials at Rothamsted and gave it in Statistical Methods for Research Workers (1925). Snedecor tabulated the variance ratio and named it F (1934). Welch gave the test for unequal variances (1951).
prereqs: [student-t-test, sample-variance, p-value, regression-f-test]
see_also: [two-way-anova, tukey-hsd, scheffe-method, kruskal-wallis-test, welch-t-test, randomized-block-design, linear-mixed-model, multiple-comparisons-problem]
sources:
  - url: https://psychclassics.yorku.ca/Fisher/Methods/
    title: Ronald A. Fisher, Statistical Methods for Research Workers, Oliver and Boyd, 1925, online text of the first edition
    locator: Chapter VII (intraclass correlations and the analysis of variance)
  - paper: doi:10.1093/biomet/38.3-4.330
    title: "B. L. Welch, On the comparison of several mean values: an alternative approach, Biometrika 38(3-4), 1951"
    locator: pp. 330 to 336 (the weighted statistic and its approximate F law with estimated denominator degrees of freedom)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 11.2 (oneway analysis of variance, the F-test, contrasts and the partition of sums of squares)
  - book: isbn:9781119492443
    title: Douglas C. Montgomery, Design and Analysis of Experiments, tenth edition, Wiley, 2019
    locator: Chapter 3 (experiments with a single factor, the analysis of variance, model adequacy checking)
  - book: isbn:9780471415404
    title: George A. F. Seber and Alan J. Lee, Linear Regression Analysis, second edition, Wiley, 2003
    locator: Chapter 2 (quadratic forms of normal vectors, Cochran's theorem) and Chapter 8 (analysis of variance; chapter-level locators)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Chapter 7 (linear hypotheses, the F-test as a UMP invariant test; chapter-level locator)
---

One-way analysis of variance (ANOVA) is a [statistical hypothesis test](/statistical-hypothesis-test/) of the null hypothesis that $k$ groups have the same mean. It splits the total variation of the data around the grand mean into the variation of the group means around the grand mean (between groups) and the variation of the data around their group means (within groups). It then divides the between mean square by the within mean square. Under normal errors with a common variance, this ratio has the F distribution with $k - 1$ and $N - k$ degrees of freedom exactly, for every sample size. With two groups it is the square of the pooled [Student t](/student-t-test/) statistic. The test is the [regression F-test](/regression-f-test/) for the model with one indicator column per group against the model with the intercept only.

## In plain words

You have several groups, for example plots under three fertilizers, and you want to know if the true averages differ. The group averages always differ a little, because single plots vary. So compare two kinds of spread. The first is how far the group averages lie from each other. The second is how much single plots scatter inside their own group. If the fertilizers do nothing, both kinds of spread come only from plot-to-plot noise, and their ratio is near one. If the ratio is much larger than one, the group averages are farther apart than the noise explains. Fisher worked out how large the ratio can be by chance when the noise follows a bell curve with the same width in every group. The test says only that some averages differ, not which ones.

## The problem

**Model.** Data $y_{ij}$ for groups $i = 1, \dots, k$ ($k \ge 2$) and units $j = 1, \dots, n_i$, with $N = \sum_i n_i > k$. The model is $y_{ij} = \mu_i + e_{ij}$, where the errors $e_{ij}$ are iid $N(0, \sigma^2)$. The means $\mu_i$ and the common variance $\sigma^2$ are unknown. In a [randomized experiment](/randomized-experiment/) the groups are the treatments and randomization justifies the comparison.

**Hypotheses.** $H_0: \mu_1 = \mu_2 = \dots = \mu_k$ against $H_1$: at least two means differ. The alternative has no direction.

**Statistic.** With group means $\bar y_i$, the grand mean $\bar y = \frac1N\sum_{i,j}y_{ij}$, and

$$SSB = \sum_{i=1}^k n_i(\bar y_i - \bar y)^2, \qquad SSW = \sum_{i=1}^k\sum_{j=1}^{n_i}(y_{ij} - \bar y_i)^2,$$

the statistic is

$$F = \frac{MSB}{MSW} = \frac{SSB/(k - 1)}{SSW/(N - k)} .$$

The total sum of squares splits as $SST = \sum_{i,j}(y_{ij} - \bar y)^2 = SSB + SSW$. $MSW$ is the pooled [sample variance](/sample-variance/), an unbiased estimate of $\sigma^2$ whether $H_0$ holds or not. $E[MSB] = \sigma^2 + \sum_i n_i(\mu_i - \bar\mu)^2/(k - 1)$ with $\bar\mu = \sum n_i\mu_i/N$, so $MSB$ estimates $\sigma^2$ only under $H_0$.

**Null distribution.** Exact: $F \sim F_{k-1, N-k}$ under $H_0$, for every $N > k$, whatever $\sigma$ is. $SSB$ and $SSW$ are squared lengths of the projections of the data onto two orthogonal subspaces, so they are independent scaled chi-square variables (Cochran's theorem in projection form, proved in the correctness proof). Without normality the size is only near $\alpha$; see the table under Example.

**Rejection rule and size.** Reject $H_0$ when $F \ge F_{(k-1, N-k, 0.95)}$ at $\alpha = 0.05$, with the lower quantile $F_{(\cdot, \cdot, p)}$. The size equals $\alpha$ under the model. For example $F_{(2, 12, 0.95)} = 3.885294$.

**p-value.** $p = P(F_{k-1, N-k} > F)$, the upper tail only. Small values of $F$ are not evidence against $H_0$, so there is no doubling.

**Sensitivity and power.** The test reacts to any spread of the means. Under $H_1$, $F$ has the noncentral F law with noncentrality $\lambda = \sum_i n_i(\mu_i - \bar\mu)^2/\sigma^2$, and the power depends on the means only through $\lambda$, increasing in it. For three groups of 5 with means $0, 0.5, 1$ and $\sigma = 1$, $\lambda = 2.5$ and the measured power is 0.2255 (4000 replications, seed 8). The test spreads its power over all directions. If one ordered pattern or one contrast is of interest, a test of that contrast has more power. The F-test is uniformly most powerful among tests that are invariant under the natural group of transformations (Lehmann and Romano, Chapter 7).

## The algorithm

```pseudo id=main
ONE-WAY-ANOVA(groups y[1..k])               ▷ k ≥ 2, N > k
L1  N ← n[1] + ... + n[k]
L2  for i ← 1 to k: ȳ[i] ← (y[i][1] + ... + y[i][n[i]]) / n[i]
L3  ȳ ← (n[1]·ȳ[1] + ... + n[k]·ȳ[k]) / N
L4  SSB ← Σ_i n[i]·(ȳ[i] - ȳ)²
L5  SSW ← Σ_i Σ_j (y[i][j] - ȳ[i])²          ▷ second pass, group mean subtracted first
L6  F ← (SSB / (k - 1)) / (SSW / (N - k))
L7  p ← F̄(F; k - 1, N - k)                   ▷ the upper tail of F
L8  return (F, k - 1, N - k, p)
```

$\bar F(x; a, b) = I_{b/(b + ax)}(b/2, a/2)$ is the upper tail of the F law, where $I$ is the regularized incomplete beta function. The shared helper evaluates it by its continued fraction, so a small p-value keeps its digits. If every group is constant, $SSW = 0$ and the code raises an error.

## Example

Three groups, $k = 3$, $N = 15$:

| group | data | $n_i$ | $\bar y_i$ | $\sum_j (y_{ij} - \bar y_i)^2$ |
|---|---|---|---|---|
| A | 5, 7, 6, 8 | 4 | 6.5 | 5 |
| B | 9, 11, 10, 12, 8 | 5 | 10 | 10 |
| C | 6, 8, 7, 5, 9, 7 | 6 | 7 | 10 |

| line | value |
|---|---|
| L3: $\bar y = 118/15$ | $7.8667$ |
| L4: $SSB = 4(6.5 - \bar y)^2 + 5(10 - \bar y)^2 + 6(7 - \bar y)^2 = 521/15$ | $34.7333$ |
| L5: $SSW = 5 + 10 + 10$ | $25$ |
| check: $SST = 896/15$ | $59.7333 = 34.7333 + 25$ |
| L6: $MSB = 34.7333/2$, $MSW = 25/12$ | $17.3667$, $2.0833$ |
| L6: $F = 1042/125$ | $8.336$ |
| L7: $p = P(F_{2,12} > 8.336)$ | $0.0053745$ |

$F = 8.336 > 3.885$, so the test rejects equal means at the 5% level. It does not say which groups differ; that is the job of [Tukey's test](/tukey-hsd/) or [Scheffé's method](/scheffe-method/). Welch's version on the same data gives $F^* = 7.1104$ on $(2, 7.4903)$ degrees of freedom and $p = 0.01858$.

**Two groups.** Groups A and B alone give $F = 343/27 = 12.7037$ on $(1, 7)$ degrees of freedom and the pooled t statistic $t = -3.5642$, with $t^2 = 12.7037$ exactly and the same p-value 0.009167.

**Size and power by simulation.** Monte Carlo with $r = 4000$ replications at $\alpha = 0.05$ (standard error of a size near 0.05: 0.0034):

| data | test | measured rejection rate | seed |
|---|---|---|---|
| normal, sizes 5, 5, 5, equal means and variances | F | 0.0510 | 1 |
| normal, sizes 4, 8, 16, $\sigma = 1, 2, 3$ | F | 0.0135 | 2 |
| normal, sizes 4, 8, 16, $\sigma = 3, 2, 1$ | F | 0.2073 | 3 |
| normal, sizes 8, 8, 8, $\sigma = 1, 2, 3$ | F | 0.0658 | 4 |
| normal, sizes 4, 8, 16, $\sigma = 3, 2, 1$ | Welch | 0.0608 | 5 |
| normal, sizes 4, 8, 16, $\sigma = 1, 2, 3$ | Welch | 0.0495 | 6 |
| exponential, sizes 5, 5, 5, equal means | F | 0.0420 | 7 |
| normal, sizes 5, 5, 5, means 0, 0.5, 1, $\sigma = 1$ | F (power) | 0.2255 | 8 |

The F-test keeps its level under skewed errors with equal sizes. With unequal variances and unequal sizes it fails: when the small groups are the noisy ones, $MSW$ is dominated by the quiet large group and the size is 0.21. Welch's test stays near 0.05 in both directions.

## Correctness

Let $P_1$ be the projection onto the span of the group indicator vectors and $P_0$ the projection onto the constant vector. Then $P_1 y$ holds the group means, $P_0 y$ the grand mean, $SSB = \|(P_1 - P_0)y\|^2$ and $SSW = \|(I - P_1)y\|^2$. The two projections have orthogonal ranges of dimensions $k - 1$ and $N - k$. Rotating the data into an orthonormal basis adapted to these ranges gives independent normal coordinates, so $SSB/\sigma^2$ and $SSW/\sigma^2$ are independent chi-square variables, central for $SSW$ always and for $SSB$ under $H_0$. Their ratio, each divided by its degrees of freedom, is $F_{k-1,N-k}$ by definition. With two groups, $SSB = n_1n_2(\bar y_1 - \bar y_2)^2/N$, which gives $F = t^2$. The full proofs are in the correctness proof below.

## Complexity

On a [real RAM](/real-ram/), L2 makes one pass over the $N$ values and L5 a second pass; L3 and L4 cost $O(k)$. So the time is $\Theta(N)$, about $5N$ arithmetic operations, and the extra space is $\Theta(k)$ for the group means. The F tail costs a number of continued fraction steps that does not grow with $N$.

**Numerical stability.** The textbook shortcut $SSW = \sum y_{ij}^2 - \sum_i n_i\bar y_i^2$ subtracts two nearly equal numbers when the data are large compared with their spread, which is [catastrophic cancellation](/catastrophic-cancellation/). Add $10^8$ to every value of the example: the shortcut gives $F = 6.0$ in double precision instead of 8.336, and with $10^9$ it gives $SSW = 0$ and a division by zero. L5 subtracts the group mean first and returns $F = 8.336$ in both cases. For data that arrive one at a time, the [Welford algorithm](/welford-algorithm/) gives the same accuracy in one pass. L7 computes the upper tail directly, not as one minus the distribution function.

## Properties

- **Exact under the model.** Size $\alpha$ for every set of sample sizes, under normal errors with equal variances.
- **Invariant.** $F$ does not change when all data are shifted by a constant or multiplied by a nonzero constant.
- **Two groups.** $F = t^2$, so the test is the two-sided pooled t-test.
- **Robust to non-normality, not to unequal variances.** With equal or nearly equal group sizes the size stays near $\alpha$ for moderate non-normality. With unequal sizes and unequal variances it can be far from $\alpha$ in either direction (table above).
- **Global.** A rejection says that the means are not all equal. It does not say which differ, and the follow-up comparisons need a [family-wise error rate](/family-wise-error-rate/) control.
- **Related to Scheffé.** $(k - 1)F$ is the largest squared standardized contrast of the group means, so the F-test rejects exactly when some contrast is significant by [Scheffé's method](/scheffe-method/).

## Variants and improvements

- **Welch's test.** Welch (1951) weights group $i$ by $w_i = n_i/s_i^2$ and refers $F^* = \frac{\sum w_i(\bar y_i - \bar y_w)^2/(k-1)}{1 + \frac{2(k-2)}{k^2-1}\Lambda}$, with $\Lambda = \sum_i (1 - w_i/\sum w)^2/(n_i - 1)$, to $F_{k-1, (k^2-1)/(3\Lambda)}$. Its law is approximate, but its size stays near $\alpha$ with unequal variances. With two groups it is the square of the [Welch t](/welch-t-test/) statistic.
- **Rank test.** The [Kruskal-Wallis test](/kruskal-wallis-test/) uses the ranks of the pooled data and has an exact null law for continuous data without normality.
- **Permutation test.** Refer $F$ to its distribution over the permutations of the group labels, a [permutation test](/permutation-test/), which is exact under exchangeability.
- **Blocks and more factors.** [Two-way ANOVA](/two-way-anova/) adds a second factor, and the [randomized block design](/randomized-block-design/) removes the variation between blocks from the error.
- **Random effects.** When the groups are a random sample of possible groups, the model $y_{ij} = \mu + a_i + e_{ij}$ with $a_i \sim N(0, \sigma_a^2)$ is a [linear mixed model](/linear-mixed-model/). The same F statistic tests $\sigma_a^2 = 0$, and the variance components are estimated by [restricted maximum likelihood](/restricted-maximum-likelihood/) or by equating mean squares to their expectations.
- **Effect size.** $\eta^2 = SSB/SST$ is the fraction of the variation explained by the groups, 0.581 in the example. See [effect size](/effect-size/).

## When to use it

Use the F-test as the first test for $k \ge 3$ independent groups when the errors are close to normal and the variances are close to equal, or when the group sizes are equal. Use Welch's test when the variances may differ and the sizes are unequal; many statisticians use it as the default. Use the Kruskal-Wallis test for small samples with clearly non-normal or outlying data. Plan the follow-up comparisons before the data: Tukey's test for all pairs, Scheffé's method for any contrasts chosen after looking at the data, and the [Bonferroni correction](/bonferroni-correction/) for a few planned contrasts.

## Pitfalls

- **Unequal variances with unequal sizes.** The size can be 0.21 or 0.014 instead of 0.05 (table above).
- **Many t-tests instead of one ANOVA.** Testing every pair at level $\alpha$ makes the chance of at least one false rejection grow with $k$; this is the [multiple comparisons problem](/multiple-comparisons-problem/).
- **Reading a rejection as "all means differ".** The alternative is only that some means differ.
- **Using the shortcut formula.** The one-pass formula for $SSW$ cancels catastrophically for large, nearly equal values.
- **Dependent observations.** Repeated measures on the same subject, or plots in the same field block, break the independence of the errors. Use a [randomized block design](/randomized-block-design/) analysis or a [linear mixed model](/linear-mixed-model/).
- **A non-significant F as proof of equal means.** It shows only that the data cannot rule out equal means; check the [statistical power](/statistical-power/).

## Implementations

## History

Ronald A. Fisher introduced the word "variance" in 1918 and developed the analysis of variance at Rothamsted Experimental Station for agricultural field trials. Statistical Methods for Research Workers (1925) presented the method with tables for $z = \frac12\ln(MSB/MSW)$. George W. Snedecor tabulated the variance ratio itself and named it F in honor of Fisher in 1934. Bernard L. Welch gave the test without equal variances in 1951.

## References
