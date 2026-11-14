---
tag: DCECK4
kind: algorithm
slug: kruskal-wallis-test
name: Kruskal-Wallis test
aliases:
- Kruskal-Wallis H test
- one-way ANOVA on ranks
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Extends the Mann-Whitney test to k groups by comparing the mean ranks of the groups in the pooled sample. The statistic is roughly chi-squared with k - 1 degrees of freedom.
model: real-ram
complexity:
  vars: {N: the total number of observations, k: the number of groups}
  time: {worst: Θ(N log N), best: Θ(N log N)}
  space: {extra: Θ(N)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1952
  people: [William H. Kruskal, W. Allen Wallis]
  note: Kruskal and Wallis gave the statistic H, its chi-square limit, exact tables for three small groups and a long discussion of earlier rank methods.
prereqs: [mann-whitney-u-test, statistical-hypothesis-test, p-value]
see_also: [one-way-anova, friedman-test, permutation-test, multiple-comparisons-problem, tukey-hsd, bonferroni-correction, statistical-power, wilcoxon-signed-rank-test]
sources:
  - book: isbn:9780470387375
    title: Myles Hollander, Douglas A. Wolfe and Eric Chicken, Nonparametric Statistical Methods, third edition, Wiley, 2014
    locator: Chapter 6 (the one-way layout), the section on the Kruskal-Wallis test
  - book: isbn:9780387352121
    title: E. L. Lehmann, Nonparametrics, Statistical Methods Based on Ranks, revised edition, Springer, 2006
    locator: The chapter on the comparison of more than two treatments (the Kruskal-Wallis test and its limit law)
  - paper: doi:10.1080/01621459.1952.10483441
    title: William H. Kruskal and W. Allen Wallis, Use of ranks in one-criterion variance analysis, Journal of the American Statistical Association 47(260), 1952
    locator: pp. 583 to 621 (the statistic H, the chi-square approximation, the tie correction and tables for three groups)
---

The Kruskal-Wallis test compares $k \ge 2$ independent groups. It ranks all $N$ observations together, computes the mean rank of each group, and measures how far these means are from the overall mean rank $(N + 1)/2$. The statistic $H$ is the one-way [analysis of variance](/one-way-anova/) F idea applied to ranks: up to a constant, it is the between-group sum of squares of the ranks. Under the null hypothesis that all groups come from one distribution, $H$ is approximately chi-square with $k - 1$ degrees of freedom; its exact law, given the ranks, comes from counting all ways to split the ranks into groups of the given sizes. For $k = 2$ it is the two-sided [Mann-Whitney test](/mann-whitney-u-test/).

## In plain words

Several groups of students learn by different methods and then take one test. Put all the scores in one list, sort it, and give each student a place number. If the methods do not matter, each group should get a fair mix of low and high place numbers, so the average place number of every group should be near the middle.

The test adds up how far each group's average place is from the middle, giving bigger groups more weight. A large total means some group sits mostly at the top or the bottom of the list. The test then asks how often a total this large would appear if the group labels were handed out at random.

## The problem

**Model.** There are $k$ groups. Group $i$ has $n_i \ge 1$ observations $X_{i1}, \ldots, X_{i n_i}$, independent with distribution $F_i$, and the groups are independent. $N = n_1 + \cdots + n_k$.

**Hypotheses.** $H_0$: $F_1 = \cdots = F_k$. The alternative is that the $F_i$ are not all equal. The test is designed for, and consistent against, alternatives where some group tends to give larger or smaller values than the others, such as a location shift $F_i(t) = F(t - \theta_i)$ with not all $\theta_i$ equal.

**Statistic.** Rank the pooled sample from $1$ to $N$, with midranks for ties. Let $R_i$ be the rank sum and $\bar R_i = R_i / n_i$ the mean rank of group $i$. Then
$$H' = \frac{12}{N(N+1)} \sum_{i=1}^{k} n_i \left(\bar R_i - \frac{N+1}{2}\right)^2 = \frac{12}{N(N+1)} \sum_{i=1}^{k} \frac{R_i^2}{n_i} - 3(N + 1),$$
and the tie-corrected statistic is $H = H' / C$ with $C = 1 - \sum_j (t_j^3 - t_j)/(N^3 - N)$, where $t_j$ are the sizes of the tie groups. With midranks, $H = (N - 1)\, SS_B / SS_T$, where $SS_B$ and $SS_T$ are the between-group and total sums of squares of the ranks.

**Null distribution.** Under $H_0$ the pooled sample is exchangeable, so given the pooled values every split of the $N$ positions into groups of sizes $n_1, \ldots, n_k$ has probability $n_1! \cdots n_k! / N!$. This conditional law of $H$ is exact. As $\min_i n_i \to \infty$, $H$ converges in law to chi-square with $k - 1$ degrees of freedom, with or without ties (asymptotic).

**P-values.** The test is one-sided in $H$: large values are evidence against $H_0$. The asymptotic p-value is $P(\chi^2_{k-1} \ge H)$. The exact p-value is the share of splits whose $H$ is at least the observed value. There is no two-sided version; $H$ already measures departures in every direction.

**Rejection rule and size.** Reject at level $\alpha$ when $p \le \alpha$. The exact p-value gives size at most $\alpha$. The chi-square p-value is only approximate: for three groups of 3 the exact 5% critical value is $5.6$ against the chi-square value $5.991$, and $P(H \ge 5.991) = 18/1680 = 0.0107$, so the chi-square test is conservative there.

**Sensitivity and power.** For a location shift the efficiency against one-way ANOVA is $3/\pi \approx 0.955$ for normal errors and at least $0.864$ for every continuous law, as for the Mann-Whitney test. A Monte Carlo run with three groups of 10, a shift of 1 in one group, $r = 2000$ samples per law and $\alpha = 0.05$ gave power $0.541$ for the Kruskal-Wallis test against $0.586$ for ANOVA with normal errors (seed 41), and $0.184$ against $0.050$ with Cauchy errors (seed 42).

## The algorithm

```pseudo id=main
KRUSKAL-WALLIS(groups X_1, ..., X_k, method)
L1  r ← midranks of the pooled sample, computed after one sort
L2  R_i ← sum of r over group i, for i = 1, ..., k
L3  H' ← 12 / (N(N + 1)) · (R_1^2 / n_1 + ... + R_k^2 / n_k) - 3(N + 1)
L4  C ← 1 - Σ_j (t_j^3 - t_j) / (N^3 - N); H ← H' / C
L5  if method = asymptotic then return H, P(χ²_{k-1} ≥ H)
L6  count all splits of the pooled ranks into groups of sizes n_1, ..., n_k, by their rank sums
L7  A ← number of splits with Σ_i R_i^2 / n_i ≥ the observed value
L8  return H, A · n_1! ··· n_k! / N!
```

The code computes $H$ as an exact fraction from doubled midranks, so it has no rounding error, and evaluates the chi-square tail with the shared `stdist.py`. For the exact method, line L6 is a dynamic program over the pooled values: its state is the number of values placed in each group so far and the doubled rank sum of each group. Given the tie pattern, $H$ is an increasing function of $\sum_i R_i^2 / n_i$, so line L7 compares the integer $\sum_i (2R_i)^2 \cdot L / n_i$ with $L = \operatorname{lcm}(n_1, \ldots, n_k)$, which is exact.

## Example

**Three groups.** Take $A = 27, 31, 22, 35$, $B = 19, 24, 20, 18, 26$ and $C = 33, 38, 29, 40$, so $N = 13$. The pooled ranks are $7, 9, 4, 11$ for $A$, $2, 5, 3, 1, 6$ for $B$ and $10, 12, 8, 13$ for $C$. The rank sums are $R_A = 31$, $R_B = 17$ and $R_C = 43$, and they add up to $13 \cdot 14 / 2 = 91$. Line L3 gives
$$H = \frac{12}{13 \cdot 14}\left(\frac{31^2}{4} + \frac{17^2}{5} + \frac{43^2}{4}\right) - 42 = \frac{3699}{455} = 8.130.$$
There are no ties, so $C = 1$. The chi-square tail with 2 degrees of freedom gives $p = 0.0172$. The exact count over all $13!/(4!\,5!\,4!) = 90090$ splits gives $p = 4/715 = 0.00559$, three times smaller. One-way ANOVA on the raw values gives $F = 9.72$ and $p = 0.0045$.

**Ties.** For the groups $1, 2, 2, 3$, then $2, 3, 4, 4$, then $3, 4, 5, 5$, the tie correction gives $H = 1727/273 = 6.326$. The chi-square p-value is $0.0423$ and the exact conditional p-value is $19/525 = 0.0362$.

**Two groups.** For $x = 1.1, 3.4, 2.9, 5.0$ and $y = 0.8, 2.0, 1.9, 2.9, 1.2$, the Kruskal-Wallis statistic is $1.8303$, which is the square of the Mann-Whitney $z = 1.3529$ without the continuity correction.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The two expressions for $H'$ agree because $\sum_i R_i = N(N+1)/2$. With midranks the total sum of squares of the ranks is $(N^3 - N - \sum_j (t_j^3 - t_j))/12$, so dividing by $C$ gives $H = (N - 1) SS_B / SS_T$. Under $H_0$, exchangeability makes every split of the positions equally likely given the pooled values, so the exact p-value is a tail probability of a discrete law and is valid. The chi-square limit follows from the multivariate central limit theorem for the vector of mean ranks, whose covariance has rank $k - 1$.

## Complexity

Lines L1 to L4 sort once and then scan, so the asymptotic test costs $\Theta(N \log N)$ time and $\Theta(N)$ space, plus a fixed number of steps for the chi-square tail. The exact count of line L6 is much more expensive. After the first $t$ values, the sizes placed so far sum to $t$ and the rank sums add up to a known total, so the last group is determined by the others, and the number of states is at most $\prod_{i < k} (n_i + 1)(2 N n_i + 1)$. Each value updates each state in $k$ ways, so the time is $O(k N \prod_{i < k} (n_i + 1)(2N n_i + 1))$, polynomial in $N$ for fixed $k$. For the example with $N = 13$ it took $0.03$ s of CPU time.

## Properties

- **Distribution-free.** Given the tie pattern, the exact null law depends only on the group sizes.
- **Invariant.** $H$ does not change under an increasing transformation of the data.
- **Two groups.** For $k = 2$, $H = z^2$, where $z$ is the standardized Mann-Whitney statistic with the tie-corrected variance and no continuity correction.
- **Chi-square accuracy.** Monte Carlo runs with normal data and $r = 4000$ samples gave chi-square sizes at $\alpha = 0.05$ of $0.0118$ for three groups of 3 (seed 31), $0.0425$ for three groups of 5 (seed 32) and $0.048$ for three groups of 10 (seed 33).
- **Robust power.** With Cauchy errors and three groups of 10, the test kept power $0.184$ for a shift of 1 while ANOVA had $0.050$ (Monte Carlo, $r = 2000$, seed 42).

## Variants and improvements

- **Exact and Monte Carlo p-values.** For small groups use the exact count; when it is too large, sample random splits and report $(1 + \#\{H^{(b)} \ge H\})/(1 + B)$, a valid [permutation test](/permutation-test/) p-value.
- **Follow-up comparisons.** A significant $H$ says that some groups differ, not which. Dunn's test compares mean ranks of pairs with the pooled variance; pairwise Mann-Whitney tests need a [multiple-comparison](/multiple-comparisons-problem/) correction such as [Bonferroni](/bonferroni-correction/). Tukey's method for means is [Tukey HSD](/tukey-hsd/).
- **Ordered alternatives.** When the groups have a natural order, the Jonckheere-Terpstra test, which adds Mann-Whitney counts over ordered pairs of groups, has more power against monotone trends.
- **Blocks.** For a randomized block design, where observations are related within blocks, use the [Friedman test](/friedman-test/).
- **The F approximation.** Running ANOVA on the ranks gives an F statistic that is a monotone function of $H$; its F p-value is another approximation to the same exact law.

## When to use it

Use it to compare three or more independent groups when the data are ordinal, skewed or contain outliers, and the question is whether some group tends to give larger values. When the groups are close to normal with equal variances, ANOVA has slightly more power. For two groups use the [Mann-Whitney test](/mann-whitney-u-test/) directly, which also has one-sided versions.

## Pitfalls

- **The chi-square approximation at small sizes.** For three groups of 3 the chi-square test had size $0.0118$ in the Monte Carlo run, and for the example with $N = 13$ it gave $p = 0.0172$ against the exact $0.0056$. Use the exact count when the groups are small.
- **Not a test of medians.** As for the Mann-Whitney test, groups with equal medians but different shapes can give large $H$, and groups with different spreads but $P(X_i > X_j) = 1/2$ do not control the size.
- **Missing tie correction.** Without dividing by $C$ the statistic is too small and the test conservative.
- **Related groups.** Measurements on the same subjects under several conditions are not independent groups; use the Friedman test.

## Implementations

## History

William Kruskal and W. Allen Wallis published the test in 1952 as an extension of the Wilcoxon and Mann-Whitney two-sample test, with the chi-square approximation, the tie correction, tables of the exact distribution for three small groups, and a survey of earlier work on rank tests. The efficiency results of Hodges and Lehmann (1956) for the Wilcoxon test carry over to it.

## References
