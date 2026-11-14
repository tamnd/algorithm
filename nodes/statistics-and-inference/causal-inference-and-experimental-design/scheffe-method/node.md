---
tag: JFSS0K
kind: algorithm
slug: scheffe-method
name: Scheffe's method
aliases:
- Scheffe test
- Scheffe simultaneous intervals
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: Simultaneous confidence intervals for all contrasts of k group means, with multiplier sqrt((k-1)F). Exact coverage 1 - alpha, even for contrasts chosen after seeing the data.
model: real-ram
complexity:
  vars: {n: the total number of observations, k: the number of groups, m: the number of contrasts asked for}
  time: {worst: Θ(n + m·k), best: Θ(n + m·k)}
  space: {extra: Θ(k + m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1953
  people: [Henry Scheffé, Holbrook Working, Harold Hotelling]
  note: Scheffé published the method for all contrasts in Biometrika in 1953 and made it the S-method of his book The Analysis of Variance (1959). Working and Hotelling had used the same idea for a confidence band around a regression line in 1929.
prereqs: [one-way-anova, family-wise-error-rate, confidence-interval]
see_also: [tukey-hsd, bonferroni-correction, multiple-comparisons-problem, regression-f-test, linear-regression, closed-testing-principle, test-interval-duality, two-way-anova]
sources:
  - paper: doi:10.1093/biomet/40.1-2.87
    title: "Henry Scheffé, A method for judging all contrasts in the analysis of variance, Biometrika 40(1-2), 1953"
    locator: pp. 87 to 110 as given by the publisher (some indexes give 87 to 104); the S-method and its comparison with Tukey's range method
  - book: isbn:9780471345053
    title: Henry Scheffé, The Analysis of Variance, Wiley, 1959, Wiley Classics Library reprint 1999
    locator: the chapter on simultaneous confidence intervals, the S-method (general locator, chapter number not confirmed)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Chapter 11 (simultaneous estimation of contrasts in the oneway analysis of variance; chapter-level locator)
  - book: isbn:9781119492443
    title: Douglas C. Montgomery, Design and Analysis of Experiments, tenth edition, Wiley, 2019
    locator: Chapter 3 (comparisons among treatment means after the analysis of variance; chapter-level locator)
---

Scheffé's method gives [confidence intervals](/confidence-interval/) for every contrast of $k$ group means at once, with simultaneous coverage exactly $1 - \alpha$. A contrast is a weighted sum $\sum c_i\mu_i$ whose weights add up to zero, such as $\mu_1 - \mu_2$ or $\mu_1 - \frac12(\mu_2 + \mu_3)$. There are infinitely many of them, but the largest standardized contrast of the sample means is a fixed multiple of the [one-way ANOVA](/one-way-anova/) F statistic. So one critical value from the F distribution, $\sqrt{(k-1)F_{(k-1,\nu,1-\alpha)}}$ standard errors, covers them all. Because the guarantee holds for all contrasts, it holds also for contrasts chosen after looking at the data. The F-test rejects exactly when some contrast has an interval that excludes zero.

## In plain words

After an experiment with several groups, you often look at the averages and then decide which comparison to make. You may compare one group with the average of two others because the data suggest it. A comparison chosen this way looks significant too often, because you picked the most striking one. Scheffé's method protects every comparison of this kind at once, including all the ones you might have picked. It finds how large the most striking comparison can be by chance, and it makes every interval wide enough for that worst case. The price is wider intervals than methods that protect only a short list of comparisons.

## The problem

**Model.** Data $y_{ij}$ for groups $i = 1, \dots, k$ ($k \ge 2$) and units $j = 1, \dots, n_i \ge 1$, with $N = \sum n_i > k$. The model is $y_{ij} = \mu_i + e_{ij}$ with iid $N(0, \sigma^2)$ errors. $MSE = \frac1\nu\sum_{i,j}(y_{ij} - \bar y_i)^2$ with $\nu = N - k$. The group sizes may differ.

**Hypotheses.** The family of all contrasts: for every nonzero $c \in \mathbb R^k$ with $\sum c_i = 0$, $H_c: \psi_c = 0$, where $\psi_c = \sum_i c_i\mu_i$, against the two-sided alternative. The goal is the [family-wise error rate](/family-wise-error-rate/) over this infinite family, in the strong sense.

**Statistic.** For each contrast, $\hat\psi_c = \sum_i c_i\bar y_i$ with the estimated standard error $\widehat{\mathrm{se}}_c = \sqrt{MSE\sum_i c_i^2/n_i}$, and

$$f_c = \frac{\hat\psi_c^2}{(k - 1)\,\widehat{\mathrm{se}}_c^2} .$$

**Null distribution.** Exact. By the Cauchy-Schwarz inequality, $\max_c\hat\psi_c^2/\widehat{\mathrm{se}}_c^2 = SSB/MSE = (k - 1)F$, where $F$ is the one-way ANOVA statistic, and the maximum is attained at $c_i = n_i(\bar y_i - \bar y)$. Applied to the centred estimates $\hat\psi_c - \psi_c$, the same identity shows that $\max_c f_c$ computed from the errors has the $F_{k-1,\nu}$ law for every $\mu$ and $\sigma$. The single contrast fixed in advance has the smaller law $t_\nu^2/(k-1)$.

**Rejection rule and size.** The simultaneous intervals are

$$\hat\psi_c \pm M\,\widehat{\mathrm{se}}_c, \qquad M = \sqrt{(k - 1)F_{(k-1,\nu,1-\alpha)}},$$

and $H_c$ is rejected when its interval excludes 0, that is when $f_c > F_{(k-1,\nu,1-\alpha)}$. The probability that all intervals cover is exactly $1 - \alpha$, for equal or unequal sizes, and the family-wise error rate is exactly $\alpha$ under $\mu_1 = \dots = \mu_k$ and at most $\alpha$ otherwise. For $k = 3$ and $\nu = 12$, $F_{(2,12,0.95)} = 3.885294$ and $M = 2.78758$.

**p-value.** The Scheffé adjusted p-value of a contrast is $p_c = P(F_{k-1,\nu} > f_c)$. It is never smaller than the p-value of the F-test, and it equals it for the best contrast.

**Sensitivity and power.** Scheffé's method has full power against the direction in which the means actually lie: the F-test rejects if and only if some contrast is significant. For any single fixed contrast it is conservative, because it pays for the whole family. For pairwise differences [Tukey's test](/tukey-hsd/) gives shorter intervals; for contrasts with many nonzero weights Scheffé's intervals are often shorter (example below).

## The algorithm

```pseudo id=main
SCHEFFE(groups y[1..k], contrasts c[1..m], α)   ▷ k ≥ 2, N > k
L1  (n[1..k], ȳ[1..k], MSE, ν) ← sizes, means, two-pass pooled variance, ν = N - k
L2  M ← sqrt((k - 1) · F_(k-1, ν, 1-α))          ▷ the F quantile
L3  for each contrast c:                         ▷ check Σ c[i] = 0 and c ≠ 0
L4      ψ ← Σ_i c[i]·ȳ[i]
L5      se ← sqrt(MSE · Σ_i c[i]² / n[i])
L6      f ← ψ² / ((k - 1)·se²)
L7      record (ψ, se, f, P(F(k-1, ν) > f), ψ - M·se, ψ + M·se)
L8  return the records
```

A separate function returns the best contrast $c_i = n_i(\bar y_i - \bar y)$, whose $f$ equals the ANOVA $F$. L2 brackets the quantile by doubling and bisects the F upper tail, which the shared helper computes by the incomplete beta continued fraction.

## Example

The groups of the [Tukey](/tukey-hsd/) example: A = 5, 7, 6, 8, 4, B = 9, 11, 10, 12, 8, C = 6, 8, 7, 5, 9, so $n = 5$, $\bar y = (6, 10, 7)$, $MSE = 2.5$, $\nu = 12$ and $M = 2.78758$. The ANOVA F statistic is 8.667 with p-value 0.004687.

| contrast $c$ | $\hat\psi_c$ (L4) | $\widehat{\mathrm{se}}_c$ (L5) | $f_c$ (L6) | $p_c$ | 95% simultaneous interval |
|---|---|---|---|---|---|
| A - B: $(1, -1, 0)$ | $-4$ | 1 | 8 | 0.006196 | $[-6.788, -1.212]$ |
| A - C: $(1, 0, -1)$ | $-1$ | 1 | 0.5 | 0.6186 | $[-3.788, 1.788]$ |
| B - C: $(0, 1, -1)$ | $3$ | 1 | 4.5 | 0.03482 | $[0.212, 5.788]$ |
| A vs mean of B, C: $(1, -\frac12, -\frac12)$ | $-2.5$ | 0.8660 | 4.1667 | 0.04225 | $[-4.914, -0.086]$ |
| B vs mean of A, C: $(-\frac12, 1, -\frac12)$ | $3.5$ | 0.8660 | 8.1667 | 0.005772 | $[1.086, 5.914]$ |
| best: $(-\frac{25}3, \frac{35}3, -\frac{10}3)$ | $43.333$ | 10.408 | 8.6667 | 0.004687 | $[14.319, 72.347]$ |

The best contrast is $n_i(\bar y_i - \bar y)$ with $\bar y = 23/3$, and its $f$ and $p$ are those of the F-test. For the pairs, Tukey's half-width is $2.668$ against Scheffé's $2.788$. For A against the mean of B and C, Tukey's extension to contrasts gives the half-width $3.77293 \cdot \sqrt{2.5/5} \cdot \frac12\sum|c_i| = 2.668$, which includes $-2.5$, while Scheffé's half-width $2.414$ excludes 0.

**Coverage by simulation.** Groups of sizes 3, 5 and 8 with means $0, 1, -0.5$ and $\sigma = 2$, 3000 replications, seed 4: the share of data sets in which the worst contrast misses its true value, which is the share in which some contrast misses, is 0.047 (exact value 0.05, standard error 0.004).

**The cost of not adjusting.** Testing the most striking contrast, the best one, with an ordinary t-test at level 0.05 has the true size $P\big((k - 1)F_{k-1,\nu} > t_{(\nu,0.975)}^2\big)$, computed from the exact law:

| $k$, $\nu$ | true size of the unadjusted test of the best contrast |
|---|---|
| 3, 12 | 0.1353 |
| 5, 30 | 0.4017 |
| 10, 30 | 0.8874 |

## Correctness

For any numbers $d_i$ and any contrast, $\sum c_id_i = \sum (c_i/\sqrt{n_i})\cdot\sqrt{n_i}(d_i - \bar d)$ with $\bar d = \sum n_id_i/N$, because $\sum c_i = 0$. The Cauchy-Schwarz inequality gives $(\sum c_id_i)^2/\sum(c_i^2/n_i) \le \sum n_i(d_i - \bar d)^2$, with equality at $c_i = n_i(d_i - \bar d)$. With $d_i = \bar y_i$ the bound is $SSB$, so the largest $f_c$ is $F$, which proves the equivalence with the F-test. With $d_i = \bar y_i - \mu_i$ the bound is the between-group sum of squares of the errors, which is $\sigma^2\chi^2_{k-1}$ and independent of $MSE$ by the [one-way ANOVA](/one-way-anova/) proof. So the largest centred $f_c$ has the $F_{k-1,\nu}$ law, and all intervals cover exactly when it is at most $F_{(k-1,\nu,1-\alpha)}$, with probability $1 - \alpha$. A false rejection makes some interval miss, which gives strong control. The full proofs are in the correctness proof below.

## Complexity

On a [real RAM](/real-ram/), L1 makes two passes over the $N$ observations, $\Theta(N)$. Each of the $m$ contrasts costs $\Theta(k)$ for L4 and L5 and one F tail of bounded cost. L2 costs one quantile, at most 400 bisection steps after the bracket search. The total time is $\Theta(N + mk)$ and the extra space is $\Theta(k + m)$ for the means and the records. The method needs no search over contrasts: the infinite family is handled by the closed-form maximum.

**Numerical stability.** $MSE$ subtracts each group mean before squaring, which avoids [catastrophic cancellation](/catastrophic-cancellation/). $\hat\psi_c$ and the sum $\sum c_i^2/n_i$ use exact summation of the terms (`math.fsum`). The check $\sum c_i = 0$ is done with a relative tolerance of $10^{-9}$, so a contrast such as $(1, -\frac13, -\frac13, -\frac13)$ given in floating point is accepted. The p-value is the upper tail computed directly, not one minus the distribution function.

## Properties

- **Exact simultaneous coverage.** $1 - \alpha$ for all contrasts, for every $N$, every set of sizes and every $\sigma$, under the normal model.
- **Valid after data snooping.** Because every contrast is covered, a contrast chosen after looking at the means keeps the guarantee.
- **Equivalent to the F-test.** The F-test rejects if and only if some contrast interval excludes 0. No contrast can be significant when $F$ is not.
- **Scale invariance.** Multiplying $c$ by a nonzero number multiplies $\hat\psi_c$ and $\widehat{\mathrm{se}}_c$ by the same factor, so the decision does not change.
- **Conservative for small families.** For a fixed finite list of contrasts the coverage is above $1 - \alpha$, and the multiplier grows like $\sqrt{k}$ with the number of groups.
- **Works in any linear model.** For a $q$-dimensional space of estimable functions in $y = Xb + e$ with $n$ rows and $k$ columns, the multiplier is $\sqrt{qF_{(q,n-k,1-\alpha)}}$ and the equivalence is with the [regression F-test](/regression-f-test/) of that hypothesis.

## Variants and improvements

- **Regression bands.** With $q = 2$ the intervals for $b_0 + b_1x$ over all $x$ give the Working-Hotelling confidence band around a fitted [linear regression](/linear-regression/) line, $\hat y(x) \pm \sqrt{2F_{(2,n-2,1-\alpha)}}\,\widehat{\mathrm{se}}(x)$.
- **Factorial and block designs.** In a balanced [two-way ANOVA](/two-way-anova/) or a [randomized block design](/randomized-block-design/), contrasts of the levels of one factor use $q = $ the number of levels minus 1 and the error degrees of freedom of that design.
- **Smaller families.** For $m$ contrasts fixed in advance, the [Bonferroni correction](/bonferroni-correction/) with $t_{(\nu,1-\alpha/(2m))}$ is shorter when $m$ is small; for all pairs, [Tukey's test](/tukey-hsd/). Choose the shortest method before seeing the data; choosing after seeing the intervals is itself data snooping.
- **Stepwise improvement.** Applying the F-test to subsets of means in a closed family, as the [closed testing principle](/closed-testing-principle/) does, rejects more hypotheses at the same family-wise error rate but gives no simultaneous intervals.
- **Unequal variances.** Welch-type versions replace $MSE\sum c_i^2/n_i$ by $\sum c_i^2s_i^2/n_i$ with estimated degrees of freedom. Their coverage is approximate.

## When to use it

Use Scheffé's method when the contrasts of interest are not known before the data are seen, or when they include contrasts other than pairwise differences, and the errors are close to normal with a common variance. Use Tukey's test when only pairwise comparisons matter and the Bonferroni correction for a short list of planned contrasts. Use it also when a significant F-test must be followed by a contrast that explains it: the best contrast always exists and is significant.

## Pitfalls

- **Using it for pairs only.** For pairwise differences Tukey's intervals are shorter; Scheffé wastes power there.
- **Unadjusted tests of snooped contrasts.** The true size of an ordinary t-test of the most striking contrast is 0.135 with three groups and 0.887 with ten (table above).
- **Wrong degrees of freedom.** The multiplier uses $k - 1$, the dimension of the contrast space, not the number of contrasts examined, and the error degrees of freedom $\nu$ of the whole analysis.
- **A significant F with no significant pair.** This is possible. The significant contrast then involves more than two means, and the best contrast shows which.
- **Unequal variances.** The pooled $MSE$ misstates the standard error of contrasts that weight the noisy groups heavily.
- **Unchecked weights.** Weights that do not add up to 0 define a different family; the code rejects them.

## Implementations

## History

Holbrook Working and Harold Hotelling used the maximum of a standardized linear function to build a confidence band around a regression line in 1929. Henry Scheffé applied the same idea to all contrasts in the analysis of variance in his 1953 Biometrika paper, which answered the question of what further inferences are valid after the F-test rejects, and compared his method with Tukey's range method. His 1959 book The Analysis of Variance presented it as the S-method, beside Tukey's T-method.

## References
