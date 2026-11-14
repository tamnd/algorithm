---
tag: 9WF4CP
kind: algorithm
slug: mann-whitney-u-test
name: Mann-Whitney U test
aliases:
- Wilcoxon rank-sum test
- Mann-Whitney-Wilcoxon test
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Compares two independent samples by the number of pairs in which the first sample's value exceeds the second's, equivalently the rank sum of one sample.
model: real-ram
complexity:
  vars: {m: the size of the first sample, n: the size of the second sample}
  time: {worst: Θ(m^2 n^2), best: Θ(m^2 n^2)}
  space: {extra: "Θ(m n min(m, n))"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1945
  people: [Frank Wilcoxon, Henry B. Mann, Donald R. Whitney]
  note: Wilcoxon (1945) proposed the rank-sum test for equal sample sizes. Mann and Whitney (1947) used the pair count U, allowed unequal sizes, tabulated the null law by a recursion and proved asymptotic normality.
prereqs: [statistical-hypothesis-test, p-value, wilcoxon-signed-rank-test]
see_also: [kruskal-wallis-test, roc-auc, u-statistic, welch-t-test, hodges-lehmann-estimator, kolmogorov-smirnov-test, permutation-test, counting-subset-sum]
sources:
  - book: isbn:9780470387375
    title: Myles Hollander, Douglas A. Wolfe and Eric Chicken, Nonparametric Statistical Methods, third edition, Wiley, 2014
    locator: Chapter 4 (the two-sample location problem), the section on the Wilcoxon rank sum test
  - book: isbn:9780387352121
    title: E. L. Lehmann, Nonparametrics, Statistical Methods Based on Ranks, revised edition, Springer, 2006
    locator: The chapter on the comparison of two treatments (the Wilcoxon rank-sum test, ties and the normal approximation)
  - paper: doi:10.1214/aoms/1177730491
    title: H. B. Mann and D. R. Whitney, On a test of whether one of two random variables is stochastically larger than the other, Annals of Mathematical Statistics 18(1), 1947
    locator: pp. 50 to 60 (the statistic U, its recursion and its limit law)
  - paper: doi:10.2307/3001968
    title: Frank Wilcoxon, Individual comparisons by ranking methods, Biometrics Bulletin 1(6), 1945
    locator: pp. 80 to 83 (the rank-sum test for two samples of equal size)
---

The Mann-Whitney U test compares two independent samples $x_1, \ldots, x_m$ and $y_1, \ldots, y_n$. Its statistic $U$ counts the pairs $(x_i, y_j)$ with $x_i > y_j$, with ties counted as one half. Equivalently, rank the pooled sample and add the ranks of the $x$ values: this rank sum $W$ is Wilcoxon's statistic, and $U = W - m(m+1)/2$. Under the null hypothesis that both samples come from the same distribution, every choice of which $m$ of the pooled values form the first sample is equally likely, so $U$ has an exact law that a dynamic program counts. $U/(mn)$ estimates $P(X > Y) + \frac{1}{2} P(X = Y)$, the [area under the ROC curve](/roc-auc/), and the test is consistent exactly against alternatives where this value differs from $1/2$.

## In plain words

Two groups of plants get two fertilizers. Take every plant from the first group and every plant from the second, and count how many times the first-group plant is the taller one. A tie counts as half a win.

If the fertilizers act the same, the first group should win about half of the pairs. Winning almost all of them is unlikely by luck. To judge how unlikely, imagine the group labels shuffled at random among all plants, and count how often a shuffle gives this many wins or more. Only the order of the heights matters, so one very tall plant counts no more than a slightly tall one.

## The problem

**Model.** $X_1, \ldots, X_m$ are independent with distribution $F$, and $Y_1, \ldots, Y_n$ are independent with distribution $G$, independent of the $X$ values.

**Hypotheses.** $H_0$: $F = G$. The alternatives are about $\theta = P(X > Y) + \frac{1}{2} P(X = Y)$: "greater" is $\theta > 1/2$ (the $X$ values tend to be larger), "less" is $\theta < 1/2$, and two-sided is $\theta \ne 1/2$. In the shift model $G(t) = F(t - \Delta)$ these are $\Delta < 0$, $\Delta > 0$ and $\Delta \ne 0$.

**Statistic.** $U = \#\{(i, j) : x_i > y_j\} + \frac{1}{2} \#\{(i, j) : x_i = y_j\}$. With midranks $R_i$ of the $x$ values in the pooled sample, $U = \sum_{i=1}^m R_i - m(m+1)/2$.

**Null distribution.** Exact and conditional on the pooled values. Under $H_0$ the $N = m + n$ values are exchangeable, so given the multiset of pooled values, each of the $\binom{N}{m}$ ways to choose the positions of the first sample has probability $1/\binom{N}{m}$. The mean of $U$ is $mn/2$ and the variance is $\frac{mn}{12}\left[(N + 1) - \frac{\sum_j (t_j^3 - t_j)}{N(N-1)}\right]$, with $t_j$ the sizes of the tie groups. Without ties the law is symmetric about $mn/2$; with ties it can be asymmetric.

**P-values.** With $c(u)$ the number of choices that give $U = u$ and $C = \binom{N}{m}$:

- Greater: $P_{hi}(u) = \sum_{v \ge u} c(v) / C$.
- Less: $P_{lo}(u) = \sum_{v \le u} c(v) / C$.
- Two-sided: $p(u) = \min\{1, 2 \min(P_{lo}(u), P_{hi}(u))\}$. Without ties this equals $P(\lvert U - mn/2 \rvert \ge \lvert u - mn/2 \rvert)$.

**Rejection rule and size.** Reject at level $\alpha$ when $p(u) \le \alpha$. The size is at most $\alpha$ for every $m$ and $n$, conditionally on the tie pattern and therefore also overall.

**Sensitivity and power.** $U/(mn)$ converges to $\theta$, so the test is consistent against every alternative with $\theta \ne 1/2$ and against no alternative with $\theta = 1/2$. When $\theta = 1/2$ but $F \ne G$, the rejection rate can be far from $\alpha$ in either direction (see Properties). In the shift model its asymptotic efficiency against the two-sample t-test is $3/\pi \approx 0.955$ for normal data and at least $0.864$ for every continuous law (Hodges and Lehmann 1956), the same values as for the [signed-rank test](/wilcoxon-signed-rank-test/).

## The algorithm

```pseudo id=main
MANN-WHITNEY(x_1, ..., x_m, y_1, ..., y_n, alternative)
L1  r ← 2 · (midranks of the pooled values x_1, ..., x_m, y_1, ..., y_n)   ▷ integers
L2  u ← (r_1 + ... + r_m) - m(m + 1)   ▷ u = 2U
L3  k ← min(m, n); c[j][s] ← 0 for all j, s; c[0][0] ← 1
L4  for each pooled value i
L5      for j ← k down to 1, for s ← top down to r_i: c[j][s] ← c[j][s] + c[j - 1][s - r_i]
L6  map each s with c[k][s] > 0 to 2U: s - m(m + 1) if k = m, else 2mn - (s - n(n + 1))
L7  A ← number of choices with 2U ≥ u; B ← number with 2U ≤ u
L8  return A / C(N, m), B / C(N, m) or min(1, 2 · min(A, B) / C(N, m)) for greater, less or two-sided
```

Here $top$ is the largest sum of $k$ doubled ranks. After line L5 has processed all $N$ values, $c[j][s]$ is the number of $j$-element sets of positions whose doubled ranks add up to $s$. This is the [count of subsets by their sum](/counting-subset-sum/) with one more index for the size. Counting subsets of the smaller size $k$ keeps the table small; if $k = n$ the counted set is the second sample, and line L6 converts its rank sum to $U$ of the first sample through $U_x + U_y = mn$. Doubled midranks keep every index an integer, so the counts are exact even with ties. The code returns $U$ and the p-value, and also offers the normal approximation with the tie-corrected variance and a continuity correction of $1/2$.

## Example

**Two small samples.** Take $x = 1.1, 3.4, 2.9, 5.0$ and $y = 0.8, 2.0, 1.9, 2.9, 1.2$, so $m = 4$, $n = 5$. In the pooled order $0.8, 1.1, 1.2, 1.9, 2.0, 2.9, 2.9, 3.4, 5.0$ the $x$ values have ranks $2$, $6.5$, $8$ and $9$; the two values $2.9$ share the midrank $6.5$. So $W = 25.5$ and $U = 25.5 - 10 = 15.5$ out of $mn = 20$. Counting pairs gives the same: $1.1$ beats one $y$, $3.4$ and $5.0$ beat all five, and $2.9$ beats four and ties one. Lines L3 to L7 over the $\binom{9}{4} = 126$ choices give $13$ with $U \ge 15.5$, so the one-sided p-value is $13/126 = 0.103$ and the two-sided p-value is $13/63 = 0.206$. The normal approximation gives $z = 1.230$ and $p = 0.219$ with the continuity correction, and $z = 1.353$ and $p = 0.176$ without it. The estimate of $P(X > Y)$ is $15.5/20 = 0.775$.

**A null law.** For $m = 2$, $n = 3$ without ties, the 10 choices give $U = 0, 1, 2, 3, 4, 5, 6$ with counts $1, 1, 2, 2, 2, 1, 1$, symmetric about $mn/2 = 3$.

**Ties break the symmetry.** For pooled ranks $1, 2.5, 2.5, 4, 5$ and $m = 2$, the 10 choices give $U = 0.5, 2, 3, 3.5, 4.5, 6$ with counts $2, 2, 1, 2, 2, 1$. The mean is still $3$, but the law is not symmetric about it, so with ties the doubled tail is a valid p-value but not the same as the rule based on $\lvert U - mn/2 \rvert$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Under $H_0$ the pooled sample is exchangeable, so given the multiset of values all $\binom{N}{m}$ position sets for the first sample are equally likely. $U$ depends on the position set only through the sum of its ranks. After all values pass line L5, $c[j][s]$ counts the $j$-sets with doubled rank sum $s$, by the same include-or-exclude induction as for subset sums. Line L6 maps each sum to $2U$, lines L7 and L8 give the exact tails, and each p-value is valid by the usual argument for tail probabilities of a discrete law.

## Complexity

Line L1 sorts in $O(N \log N)$ with $N = m + n$. Let $k = \min(m, n)$. The largest doubled rank sum of $k$ values is $top = k(2N - k + 1) = \Theta(kN)$, so the table has $(k + 1)(top + 1) = \Theta(k^2 N)$ entries, which is $\Theta(m n \min(m, n))$. Line L5 does $\Theta(top)$ additions for each of the $k$ values of $j$ and each of the $N$ values of $i$, so the time is $\Theta(N^2 k^2) = \Theta(m^2 n^2)$ additions. For $m = n = 30$ the exact p-value took $0.21$ s of CPU time in the Python code. The classic recursion of Mann and Whitney on the counts by $U$ has the same order. For large samples the normal approximation costs $O(N \log N)$.

## Properties

- **Distribution-free.** Under $H_0$ the conditional law depends only on $m$, $n$ and the tie pattern.
- **Invariant.** $U$ does not change under any increasing transformation applied to both samples.
- **Connection to AUC.** $U/(mn)$ is the empirical area under the ROC curve of a score that separates the two samples, and $U$ is a two-sample [U-statistic](/u-statistic/) with kernel $\mathbf{1}\{x > y\} + \frac{1}{2}\mathbf{1}\{x = y\}$.
- **Not a test of medians.** With $X = E - \ln 2$ and $Y = \ln 2 - E'$, $E$ and $E'$ exponential with mean 1, both medians are 0 but $\theta = \frac{1}{4}(1 + 2 \ln 2) = 0.5966$. A Monte Carlo run with $m = n = 50$, $r = 1000$ samples and seed 21 rejected at $\alpha = 0.05$ in $41.2\%$ of samples, with the normal approximation.
- **Unequal spreads.** With $F = N(0, 1)$, $G = N(0, 16)$, $\theta = 1/2$ but $F \ne G$. With $m = 10$, $n = 40$, $r = 2000$ samples and seed 22, the test rejected in $0.9\%$ of samples at the nominal $5\%$. With the spreads exchanged ($m = 10$ with standard deviation 4, $n = 40$ with standard deviation 1) and seed 23 it rejected in $14.25\%$. The test does not control the size for this problem.

## Variants and improvements

- **Rank-sum form.** Wilcoxon's $W = U + m(m + 1)/2$ gives the same p-values.
- **Normal approximation.** $z = (U - mn/2 \mp 1/2)/\sigma$ with the tie-corrected $\sigma$ above. For the example it gave $0.219$ against the exact $0.206$.
- **Estimator and interval.** The [Hodges-Lehmann estimator](/hodges-lehmann-estimator/) of the shift is the median of the $mn$ differences $y_j - x_i$, and inverting the test gives an interval between two order statistics of these differences.
- **Unequal spreads.** The Brunner-Munzel test estimates the variance of $U$ under $\theta = 1/2$ without assuming $F = G$, and so keeps the size approximately when the spreads differ.
- **Several samples.** The [Kruskal-Wallis test](/kruskal-wallis-test/) extends the rank sum to $k$ groups; for $k = 2$ its statistic is the square of the $z$ of this test without the continuity correction.
- **Other two-sample tests.** The two-sample [Kolmogorov-Smirnov test](/kolmogorov-smirnov-test/) reacts to any difference between $F$ and $G$, including a difference in spread, at the cost of power against shifts. A [permutation test](/permutation-test/) on the difference of means uses the same exchangeability with the raw values.

## When to use it

Use it to compare two independent groups when the data are ordinal or skewed, or have outliers, and the question is whether one group tends to give larger values. It is a good default in place of the [Welch t-test](/welch-t-test/) when normality is in doubt, but only if the two distributions have similar shapes or the question is really about $P(X > Y)$. For paired data use the [signed-rank test](/wilcoxon-signed-rank-test/).

## Pitfalls

- **It is not a test of medians or means.** Equal medians gave a $41.2\%$ rejection rate in the Monte Carlo run above.
- **Unequal spreads.** With $F \ne G$ but $\theta = 1/2$, the size was $0.9\%$ or $14.25\%$ at the nominal $5\%$, depending on which sample is the smaller one.
- **Conventions for $U$.** Some books and programs report $\#\{x_i < y_j\}$, which is $mn - U$, or the smaller of the two, or the rank sum $W$. Check which one before using a table.
- **Ties and the normal approximation.** Without the tie correction the variance is too large and the test conservative. The exact count handles ties.
- **Paired data.** Applying the rank-sum test to paired data ignores the pairing and loses power.

## Implementations

## History

Frank Wilcoxon (1945) proposed the rank-sum test for two samples of equal size, together with the signed-rank test, in a short paper. Henry Mann and Donald Whitney (1947) wrote the statistic as the pair count $U$, allowed unequal sizes, gave a recursion for its null law with tables, and proved that $U$ is asymptotically normal under the null. Their title states the alternative that one variable is stochastically larger than the other. Hodges and Lehmann (1956) showed that the efficiency against the t-test is never below $0.864$ for shift models. Bamber (1975) and Hanley and McNeil (1982) linked $U/(mn)$ to the area under the ROC curve.

## References
