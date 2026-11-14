---
tag: N35W2Z
kind: algorithm
slug: tukey-hsd
name: Tukey's range test
aliases:
- Tukey HSD
- honestly significant difference
- Tukey-Kramer method
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: Compares all pairs of k group means with the studentized range law. Family-wise error rate exactly alpha for balanced normal data, at most alpha with unequal sizes.
model: real-ram
complexity:
  vars: {n: the total number of observations, k: the number of groups}
  time: {worst: Θ(n + k²), best: Θ(n + k²)}
  space: {extra: Θ(k²)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1953
  people: [John W. Tukey, D. Newman, Clyde Y. Kramer, Anthony J. Hayter]
  note: Tukey gave the honestly significant difference in an unpublished 1953 manuscript, The Problem of Multiple Comparisons. Kramer (1956) extended it to unequal group sizes, and Hayter (1984) proved that the extension is conservative.
prereqs: [one-way-anova, family-wise-error-rate, student-t-test]
see_also: [scheffe-method, bonferroni-correction, multiple-comparisons-problem, closed-testing-principle, holm-bonferroni-method, two-way-anova, gauss-legendre-quadrature, order-statistic]
sources:
  - book: isbn:9780412051210
    title: "John W. Tukey, The Collected Works of John W. Tukey, Volume VIII: Multiple Comparisons 1948-1983, edited by Henry I. Braun, Chapman and Hall, 1994"
    locator: the 1953 manuscript The Problem of Multiple Comparisons, first printed in this volume (chapter-level locator)
  - paper: doi:10.2307/3001469
    title: "Clyde Young Kramer, Extension of multiple range tests to group means with unequal numbers of replications, Biometrics 12(3), 1956"
    locator: pp. 307 to 310 (the standard error with the harmonic term for unequal sizes)
  - paper: doi:10.1214/aos/1176346392
    title: "A. J. Hayter, A proof of the conjecture that the Tukey-Kramer multiple comparisons procedure is conservative, Annals of Statistics 12(1), 1984"
    locator: pp. 61 to 75 (the coverage of the Tukey-Kramer intervals is at least 1 - alpha)
  - paper: doi:10.2307/2347300
    title: "R. E. Lund and J. R. Lund, Algorithm AS 190: probabilities and upper quantiles for the studentized range, Applied Statistics 32(2), 1983"
    locator: pp. 204 to 210 (the double integral and its numerical evaluation; a correction appeared in Applied Statistics 34(1), 1985, p. 104)
  - paper: doi:10.1214/aos/1043351247
    title: "Yoav Benjamini and Henry Braun, John W. Tukey's contributions to multiple comparisons, Annals of Statistics 30(6), 2002"
    locator: pp. 1576 to 1594 (the history of the 1953 manuscript and of the honestly significant difference)
  - book: isbn:9781119492443
    title: Douglas C. Montgomery, Design and Analysis of Experiments, tenth edition, Wiley, 2019
    locator: Chapter 3 (comparing pairs of treatment means after the analysis of variance; chapter-level locator)
---

Tukey's range test, also called Tukey's honestly significant difference (HSD), compares every pair of $k$ group means after a [one-way ANOVA](/one-way-anova/). It declares two means different when their difference, divided by its standard error, exceeds a critical value of the studentized range distribution. This is the distribution of the range of $k$ independent normal means divided by an independent estimate of their standard deviation. Because the largest of all the pairwise statistics is exactly such a range, the test controls the [family-wise error rate](/family-wise-error-rate/) over all $k(k-1)/2$ pairs. With equal group sizes and normal errors with a common variance, the simultaneous confidence intervals cover all pairwise differences with probability exactly $1 - \alpha$. With unequal sizes the same formula is the Tukey-Kramer method, which is conservative.

## In plain words

After you find that several group averages are not all the same, you want to know which pairs differ. If you test every pair on its own at the 5% level, the chance of at least one false alarm grows with the number of pairs. Tukey asked a different question: how large can the biggest gap between any two averages be when nothing is going on? He took the widest gap, the largest average minus the smallest one, and measured it in units of the noise. Its chance distribution does not depend on the true averages or on the noise level. A pair is declared different only if its gap is larger than what the widest gap would reach by chance in 95% of experiments. So the chance of any false alarm over all pairs together stays at 5%.

## The problem

**Model.** Data $y_{ij}$ for groups $i = 1, \dots, k$ ($k \ge 2$) and units $j = 1, \dots, n_i$, with $N = \sum_i n_i > k$. The model is $y_{ij} = \mu_i + e_{ij}$ with iid $N(0, \sigma^2)$ errors, as in [one-way ANOVA](/one-way-anova/). The error mean square $MSE = \frac1\nu\sum_{i,j}(y_{ij} - \bar y_i)^2$ has $\nu = N - k$ degrees of freedom. The same procedure applies to the means of any balanced design whose $MSE$ is independent of the means, for example the treatment means of a [randomized block design](/randomized-block-design/) or the marginal means of a balanced [two-way ANOVA](/two-way-anova/), with that design's $\nu$.

**Hypotheses.** A family of $m = k(k-1)/2$ hypotheses $H_{ij}: \mu_i = \mu_j$ for $i < j$, each against the two-sided alternative. The goal is the family-wise error rate in the strong sense: for every configuration of the means, the probability of rejecting at least one true $H_{ij}$ is at most $\alpha$.

**Statistic.** For each pair,

$$q_{ij} = \frac{|\bar y_i - \bar y_j|}{\sqrt{\frac{MSE}{2}\left(\frac1{n_i} + \frac1{n_j}\right)}} .$$

With equal sizes $n_i = n$ the denominator is $\sqrt{MSE/n}$, the estimated standard error of one mean. The pairwise statistic is $\sqrt2$ times the absolute pooled [Student t](/student-t-test/) statistic of the pair, but its standard error uses all $k$ groups.

**Null distribution.** Exact for equal sizes. Let $Z_1, \dots, Z_k$ be iid $N(0, 1)$ and $V \sim \chi^2_\nu$ independent of them. The studentized range is $Q_{k,\nu} = (\max_i Z_i - \min_i Z_i)/\sqrt{V/\nu}$. Its upper tail is the double integral

$$P(Q_{k,\nu} > q) = \int_0^\infty g_\nu(s)\,k\int_{-\infty}^{\infty}\varphi(z)\Big(A(z)^{k-1} - \big(A(z) - A(z + qs)\big)^{k-1}\Big)dz\,ds,$$

with $A = 1 - \Phi$ the normal upper tail and $g_\nu$ the density of $\sqrt{V/\nu}$. Under the model, $\max_{i<j}|(\bar y_i - \bar y_j) - (\mu_i - \mu_j)|/\sqrt{MSE/n}$ has exactly the law of $Q_{k,\nu}$, for every $\mu$ and $\sigma$. With unequal sizes no single law is exact, and $Q_{k,\nu}$ gives a conservative bound.

**Rejection rule and size.** Reject $H_{ij}$ when $q_{ij} > q_{(k,\nu,1-\alpha)}$, the upper $\alpha$ point of $Q_{k,\nu}$. In the units of the means, the honestly significant difference is $HSD = q_{(k,\nu,1-\alpha)}\sqrt{MSE/n}$, and a pair is declared different when $|\bar y_i - \bar y_j| > HSD$. The simultaneous intervals are $\bar y_i - \bar y_j \pm q_{(k,\nu,1-\alpha)}\sqrt{\frac{MSE}2(\frac1{n_i} + \frac1{n_j})}$. For equal sizes the family-wise error rate is exactly $\alpha$ under the complete null and at most $\alpha$ under every other configuration. For example $q_{(3,12,0.95)} = 3.77293$ and $q_{(3,\infty,0.95)} = 3.314$.

**p-value.** The adjusted p-value of a pair is $p_{ij} = P(Q_{k,\nu} > q_{ij})$. Rejecting the pairs with $p_{ij} \le \alpha$ is the same as the rule above. Each $p_{ij}$ is already adjusted for the whole family, so it is compared with $\alpha$ directly.

**Sensitivity and power.** The test is built for pairwise differences. For pairs, its intervals are shorter than those of [Scheffé's method](/scheffe-method/) and of the [Bonferroni correction](/bonferroni-correction/), and the gap grows with $k$ (table under Example). Its power for one pair is lower than that of an unadjusted t-test, which is the price of the family-wise guarantee. For contrasts that involve more than two means, such as one mean against the average of the others, Scheffé's method is often shorter.

## The algorithm

```pseudo id=main
TUKEY-HSD(groups y[1..k], α)                  ▷ k ≥ 2, N > k
L1  (ȳ[1..k], MSE, ν) ← group means, two-pass pooled variance, ν = N - k
L2  q* ← upper α point of Q(k, ν)            ▷ invert the tail by false position
L3  for each pair i < j:
L4      d ← ȳ[i] - ȳ[j];  se ← sqrt((MSE / 2)·(1/n[i] + 1/n[j]))
L5      q ← |d| / se
L6      p ← P(Q(k, ν) > q)                    ▷ the double integral by Gauss-Legendre panels
L7      record (i, j, d, q, p, d - q*·se, d + q*·se)
L8  return (q*, the records)
```

The tail in L6 is the double integral above. The inner integral over $z$ uses 17 panels of a 10-point [Gauss-Legendre quadrature](/gauss-legendre-quadrature/) rule on $[-8.5, 8.5]$, and the outer integral over $s$ uses 40 panels on the range that holds all but $10^{-30}$ of the chi-square mass. For $\nu = \infty$ the outer integral is dropped. L2 finds a bracket by doubling and then runs the Illinois variant of [regula falsi](/regula-falsi/) on $P(Q > q) - \alpha$. The code rejects $N \le k$, empty groups, and $MSE = 0$.

## Example

The three groups below have equal sizes $n = 5$, so $k = 3$, $N = 15$ and $\nu = 12$:

| group | data | $\bar y_i$ | $\sum_j (y_{ij} - \bar y_i)^2$ |
|---|---|---|---|
| A | 5, 7, 6, 8, 4 | 6 | 10 |
| B | 9, 11, 10, 12, 8 | 10 | 10 |
| C | 6, 8, 7, 5, 9 | 7 | 10 |

L1 gives $MSE = 30/12 = 2.5$, and the ANOVA F statistic is $8.667$ on $(2, 12)$ degrees of freedom. L2 gives $q_{(3,12,0.95)} = 3.77293$. The standard error of one mean is $\sqrt{2.5/5} = 0.70711$, so $HSD = 3.77293 \cdot 0.70711 = 2.6679$.

| pair | $\bar y_i - \bar y_j$ | $q_{ij}$ (L5) | adjusted $p_{ij}$ (L6) | 95% simultaneous interval (L7) |
|---|---|---|---|---|
| A - B | $-4$ | 5.657 | 0.004634 | $[-6.668, -1.332]$ |
| A - C | $-1$ | 1.414 | 0.5908 | $[-3.668, 1.668]$ |
| B - C | $3$ | 4.243 | 0.02772 | $[0.332, 5.668]$ |

B differs from A and from C at the 5% family-wise level, and the data do not separate A from C.

**Width of the intervals.** The half-widths of 95% intervals for one pairwise difference, in units of its standard error $\sqrt{2MSE/n}$, are $q/\sqrt2$ for Tukey, $\sqrt{(k-1)F_{(k-1,\nu,0.95)}}$ for Scheffé, $t_{(\nu, 1 - 0.025/m)}$ for Bonferroni over the $m$ pairs, and $t_{(\nu,0.975)}$ for the unadjusted t-test:

| $k$, $\nu$ | Tukey | Scheffé | Bonferroni | unadjusted |
|---|---|---|---|---|
| 3, 12 (the example) | 2.6679 | 2.7876 | 2.7795 | 2.1788 |
| 3, 30 | 2.4653 | 2.5752 | 2.5357 | 2.0423 |
| 5, 30 | 2.9006 | 3.2800 | 3.0298 | 2.0423 |
| 10, 30 | 3.4112 | 4.4605 | 3.6067 | 2.0423 |

**Family-wise error rate by simulation.** Normal data with all means equal, $\alpha = 0.05$, 20000 replications (standard error near 0.0015):

| group sizes | measured rate of at least one false rejection | seed |
|---|---|---|
| 5, 5, 5, 5 | 0.05255 | 1 |
| 3, 5, 10, 20 | 0.0485 | 2 |
| 2, 2, 30, 30 | 0.0436 | 3 |

The balanced rate is within two standard errors of the exact 0.05. With unequal sizes the Tukey-Kramer rate falls below 0.05, as Hayter's theorem says.

**Accuracy of the studentized range.** The tail of L6 against the share of 20000 simulated values of $Q_{4,10}$ above $q$ (seed 4, standard error at most 0.0036):

| $q$ | simulated $P(Q_{4,10} > q)$ | L6 |
|---|---|---|
| 2 | 0.5207 | 0.51896 |
| 3 | 0.2115 | 0.21111 |
| 4 | 0.07085 | 0.07208 |
| 5 | 0.0244 | 0.02345 |

L2 reproduces published table values, for example $q_{(3,10,0.95)} = 3.8768$, $q_{(5,5,0.95)} = 5.6731$, $q_{(4,60,0.95)} = 3.7371$, $q_{(10,20,0.95)} = 5.0079$, $q_{(20,120,0.95)} = 5.1259$, $q_{(3,1,0.95)} = 26.976$ and $q_{(2,\infty,0.95)} = 2.7718 = 1.95996\sqrt2$.

## Correctness

Let all sizes be $n$ and put $Z_i = \sqrt n(\bar y_i - \mu_i)/\sigma$. The $Z_i$ are iid standard normal, and $V = \nu\,MSE/\sigma^2$ is $\chi^2_\nu$ and independent of the means, because the group means and the within-group residuals are projections of the data onto orthogonal subspaces (the [one-way ANOVA](/one-way-anova/) proof). Each centred pairwise statistic is $(Z_i - Z_j)/\sqrt{V/\nu}$, and the largest of them over all pairs is $(\max Z - \min Z)/\sqrt{V/\nu} = Q_{k,\nu}$. So all intervals cover at once exactly when $Q_{k,\nu} \le q_{(k,\nu,1-\alpha)}$, which has probability $1 - \alpha$. A false rejection of a true $H_{ij}$ means that the interval for $\mu_i - \mu_j$ misses, so the family-wise error rate is at most $\alpha$ for every configuration, and equal to $\alpha$ when all means are equal. The double integral comes from conditioning on the smallest $Z_i$ and then on $\sqrt{V/\nu}$. For two groups $Q_{2,\nu} = \sqrt2|T_\nu|$, so the test is the two-sided pooled t-test, which gives an exact check of the quadrature. The full proofs are in the correctness proof below. The coverage of Tukey-Kramer with unequal sizes is Hayter's theorem, cited and not proved here, and the accuracy of the quadrature is measured, not bounded.

## Complexity

On a [real RAM](/real-ram/), L1 makes two passes over the $N$ observations, $\Theta(N)$. The loop L3 to L7 runs $k(k-1)/2$ times. Each tail evaluation in L6 is a fixed number of quadrature nodes, $400$ outer times $170$ inner, independent of $N$ and $k$, so the loop costs $\Theta(k^2)$ with a large constant. L2 costs a doubling search and at most 100 false position steps of one tail each. The total time is $\Theta(N + k^2)$, and the extra space is $\Theta(k^2)$ for the records. In the Python code, one tail takes about 0.02 s and the quantile about 0.3 s.

**Numerical stability.** $MSE$ subtracts each group mean before squaring, as in the one-way code, which avoids [catastrophic cancellation](/catastrophic-cancellation/) for large values with a small spread. In the inner integrand, $A(z)^{k-1} - (A(z) - A(z + w))^{k-1}$ is the difference of two nearly equal powers when $w$ is large. The code writes it as $-A^{k-1}\,\mathrm{expm1}\big((k-1)\,\mathrm{log1p}(-r)\big)$ with $r = A(z + w)/A(z)$, which keeps its relative accuracy. It computes the upper tail directly: for $k = 2$ and $\nu = 30$, a tail of $1.14 \cdot 10^{-11}$ agrees with the exact t tail to a relative error of $2 \cdot 10^{-9}$. The check against $Q_{2,\nu} = \sqrt2|T_\nu|$ agrees to $10^{-14}$ for $\nu \le 30$ and to $10^{-12}$ for $\nu$ up to 1000.

## Properties

- **Exact for balanced data.** Simultaneous coverage $1 - \alpha$ and family-wise error rate $\alpha$ under the complete null, for every $n$, $k$ and $\sigma$.
- **Strong control.** The error rate is at most $\alpha$ under every configuration of the means, not only under the complete null.
- **Two groups.** $q = \sqrt2|t|$ and $Q_{2,\nu} = \sqrt2|T_\nu|$, so the test is the two-sided pooled t-test.
- **Single step.** Every pair uses the same critical value, so the intervals are simultaneous and consistent: the intervals and the tests give the same decisions.
- **Shortest for all pairs.** Among single-step methods for all pairwise differences with equal sizes, the Tukey intervals are shorter than the Scheffé and Bonferroni intervals for $k \ge 3$ (table above).
- **No preliminary F-test needed.** Its guarantee does not depend on the ANOVA F-test. A pair can be significant while F is not, and the reverse.
- **Not transitive.** With three ordered means, the test can separate the two outer means but neither of them from the middle one. So the results are often shown as overlapping groups of means, not as a partition.

## Variants and improvements

- **Tukey-Kramer method.** With unequal sizes, use the standard error $\sqrt{\frac{MSE}2(\frac1{n_i} + \frac1{n_j})}$ of each pair and the same $q_{(k,\nu,1-\alpha)}$ (Kramer, 1956). The code above is already this method. Hayter (1984) proved that its coverage is at least $1 - \alpha$, and the simulation above shows rates of 0.0485 and 0.0436. On the one-way ANOVA example with sizes 4, 5 and 6 ($MSE = 25/12$), it gives the adjusted p-values 0.00920 for A - B, 0.855 for A - C and 0.01275 for B - C.
- **All contrasts.** Tukey's intervals extend to every contrast $\sum c_i\mu_i$ with $\sum c_i = 0$: $\sum c_i\bar y_i \pm q_{(k,\nu,1-\alpha)}\sqrt{MSE/n}\cdot\frac12\sum|c_i|$, with simultaneous coverage at least $1 - \alpha$. For pairwise differences this is the HSD itself; for contrasts with many nonzero terms, [Scheffé's method](/scheffe-method/) is shorter.
- **Unequal variances.** The Games-Howell method uses the Welch standard error $\sqrt{(s_i^2/n_i + s_j^2/n_j)/2}$ and Welch degrees of freedom for each pair. Its error rate is approximate, not guaranteed. See the [Welch t-test](/welch-t-test/).
- **Comparisons with a control.** When only $k - 1$ comparisons with one control group are of interest, Dunnett's method uses the maximum of $k - 1$ correlated t statistics and gives shorter intervals than Tukey's.
- **Stepwise range tests.** The Newman-Keuls procedure uses $q_{(p,\nu,1-\alpha)}$ for a range of $p$ ordered means. It does not control the family-wise error rate in the strong sense for $k \ge 4$. The Ryan-Einot-Gabriel-Welsch procedure adjusts the levels so that it does, and it is a shortcut of the [closed testing principle](/closed-testing-principle/). Stepwise methods are more powerful than Tukey's test but do not give simultaneous intervals.
- **Other designs.** In a [randomized block design](/randomized-block-design/) or a balanced [two-way ANOVA](/two-way-anova/), use the means of one factor, the $MSE$ of that design and its error degrees of freedom.

## When to use it

Use Tukey's test when all pairwise comparisons of $k \ge 3$ means are of interest, the sizes are equal or close to equal, and the errors are close to normal with a common variance. Use Tukey-Kramer for unequal sizes. Use Dunnett's method when only comparisons with a control matter, the [Bonferroni correction](/bonferroni-correction/) or the [Holm-Bonferroni method](/holm-bonferroni-method/) for a few planned comparisons, and Scheffé's method when contrasts other than pairs are chosen after looking at the data. Use Games-Howell when the variances clearly differ.

## Pitfalls

- **Unequal variances with unequal sizes.** The pooled $MSE$ is wrong for each pair, and the error rate can be far from $\alpha$, as for the [one-way ANOVA](/one-way-anova/) F-test.
- **Gating on the F-test.** Running Tukey's test only after a significant F changes its error rate and its power. The test does not need the gate.
- **Reading adjusted p-values as unadjusted.** $p_{ij}$ already accounts for all $m$ pairs; do not apply another correction to it.
- **The $\sqrt2$ factor.** Some tables and programs divide by $\sqrt{MSE/n}$ and others by $\sqrt{2MSE/n}$. Compare $q$ with $q_{(k,\nu,1-\alpha)}$, or $q/\sqrt2$ with $q_{(k,\nu,1-\alpha)}/\sqrt2$, never a mixture.
- **Wrong $\nu$ or $k$.** $k$ is the number of means in the family, not the number of pairs, and $\nu$ is the error degrees of freedom of the whole analysis, not $n_i + n_j - 2$.
- **Data dredging beyond pairs.** Choosing a non-pairwise contrast after looking at the data needs Scheffé's method; see the [multiple comparisons problem](/multiple-comparisons-problem/).

## Implementations

## History

"Student" studied the distribution of the range of normal samples in 1927, and D. Newman tabulated the range divided by an independent estimate of the standard deviation in 1939. John W. Tukey proposed the honestly significant difference in a long manuscript, The Problem of Multiple Comparisons, which he circulated in 1953 and which was printed only in 1994 in his Collected Works. Clyde Y. Kramer extended the method to unequal group sizes in 1956, and the conjecture that the extension is conservative stayed open until Anthony J. Hayter proved it in 1984. Lund and Lund published a widely used algorithm for the distribution in 1983.

## References
