---
tag: KSN49K
kind: algorithm
slug: permutation-test
name: Permutation test
aliases:
- randomization test
- Fisher-Pitman permutation test
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Get the null distribution of a statistic by recomputing it over permutations of the labels, which are exchangeable under the null. The test is exact at any sample size.
model: real-ram
complexity:
  vars: {n: the pooled sample size, m: the size of the first group, b: the number of random permutations}
  time: {worst: Θ(b n), exact: "Θ(n · n!/(m! (n - m)!))"}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true, exact: true, online: false, recursive: false}
history:
  year: 1935
  people: [R. A. Fisher, E. J. G. Pitman]
  note: Fisher computed the exact sign-flip distribution for Darwin's paired plant heights in The Design of Experiments (1935). Pitman (1937) gave the two-sample test for any samples.
prereqs: [statistical-hypothesis-test, p-value, sampling-distribution, type-i-and-type-ii-errors]
see_also: [sign-test, mann-whitney-u-test, fisher-exact-test, welch-t-test, bootstrap-method, randomized-experiment, westfall-young-procedure, fisher-yates-shuffle]
sources:
  - book: "R. A. Fisher, The Design of Experiments, Oliver and Boyd, Edinburgh, 1935"
    locator: Chapter III, Section 21 (the test of a wider hypothesis on Darwin's Zea mays data, 1726 of 32768 sign combinations)
  - paper: doi:10.2307/2984124
    title: E. J. G. Pitman, Significance tests which may be applied to samples from any populations, Supplement to the Journal of the Royal Statistical Society 4(1), 1937
    locator: pp. 119 to 130 (the two-sample test on all divisions of the pooled sample, and its moments)
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Section 15.2 (permutation and randomization tests, the randomization hypothesis and the exact level)
  - book: isbn:9780412042317
    title: Bradley Efron and Robert J. Tibshirani, An Introduction to the Bootstrap, Chapman and Hall, 1993
    locator: Chapter 15 (permutation tests, on the mouse survival data of Table 2.1)
  - paper: doi:10.2202/1544-6115.1585
    title: Belinda Phipson and Gordon K. Smyth, Permutation p-values should never be zero, Statistical Applications in Genetics and Molecular Biology 9(1), 2010
    locator: Article 39 (the Monte Carlo p-value (1 + c)/(1 + b) and why c/b is not valid)
---

A permutation test gets the null distribution of a test statistic from the data themselves. Under the null hypothesis some rearrangements of the data are equally likely, for example all ways to split a pooled sample into two groups of the given sizes. The test recomputes the statistic on each rearrangement and reports the fraction that is at least as extreme as the observed value. This p-value is exact for every sample size and every statistic, and a Monte Carlo version with $b$ random permutations and the p-value $(1 + c)/(1 + b)$ keeps the exact level.

## In plain words

Seven mice get a new drug and nine do not. The treated mice live longer on average. Is the drug the reason, or did the lucky mice fall into the treated group by chance?

If the drug does nothing, the labels "treated" and "control" are only names. Each mouse would have lived the same time with the other label. So write each survival time on a card, shuffle the 16 cards, deal 7 into a "treated" pile and 9 into a "control" pile, and compute the difference of the averages. Do this for every possible deal, or for a few thousand random deals. If the real difference is larger than almost all of the shuffled differences, the labels matter, and the drug probably has an effect. If many shuffled deals give a difference as large as the real one, chance explains the data well.

## The problem

**Data.** A pooled sample $z = (z_1, \ldots, z_n)$. In the two-sample case the first $m$ values come from group 1 and the other $n - m$ from group 2. In the paired case the data are differences $d_1, \ldots, d_n$.

**Null hypothesis.** The randomization hypothesis of Lehmann and Romano: there is a finite group $G$ of transformations of the data such that $gZ$ has the same distribution as $Z$ for every $g \in G$ under $H_0$.

- Two samples: $H_0$ says that $Z_1, \ldots, Z_n$ are exchangeable, for example independent and identically distributed with any common distribution. $G$ is the group of the $n!$ permutations, and a statistic of the two groups depends only on which $m$ values fall in group 1, so it takes at most $\binom{n}{m}$ values.
- Paired data: $H_0$ says that each $D_i$ is symmetric about 0, independently. $G$ is the group of the $2^n$ sign changes $d_i \mapsto \pm d_i$.
- Independence of $X$ and $Y$ in pairs $(X_i, Y_i)$: permute the $Y$ values against the fixed $X$ values.

**Statistic.** Any function $T$ of the data for which large values are evidence against $H_0$, for example the difference of the means $T = \bar z_{1:m} - \bar z_{m+1:n}$. Use $\lvert T \rvert$ for a two-sided test.

**P-value.** The exact p-value is

$$p = \frac{\#\{g \in G : T(gz) \ge T(z)\}}{\lvert G \rvert}.$$

The Monte Carlo p-value with $b$ independent uniform draws $g_1, \ldots, g_b$ from $G$ is

$$p_b = \frac{1 + \#\{j : T(g_j z) \ge T(z)\}}{1 + b}.$$

## The algorithm

```pseudo id=main
PERMUTATION-TEST(z_1, ..., z_n, m, T, b)      ▷ group 1 is z_1 .. z_m
L1  t ← T(z_1 .. z_m ; z_{m+1} .. z_n)
L2  c ← 0
L3  for j ← 1 to b do
L4      w ← a uniform random permutation of z        ▷ Fisher-Yates shuffle
L5      t_j ← T(w_1 .. w_m ; w_{m+1} .. w_n)
L6      if t_j ≥ t then c ← c + 1
L7  return (1 + c) / (1 + b)

EXACT-PERMUTATION-TEST(z_1, ..., z_n, m, T)
L8  c ← 0
L9  for each set S ⊆ {1, ..., n} with |S| = m do
L10     if T(z_S ; z_{not S}) ≥ t then c ← c + 1     ▷ t from line L1
L11 return c / C(n, m)
```

Line L4 uses a [Fisher-Yates shuffle](/fisher-yates-shuffle/), which gives each of the $n!$ orders probability $1/n!$, so each split has probability $1/\binom{n}{m}$. Line L9 lists the $\binom{n}{m}$ splits once each, in lexicographic order of the index sets. Listing all $n!$ permutations, as in [generating all permutations](/generating-all-permutations/), gives the same p-value, because each split appears $m!(n - m)!$ times. The "+1" in line L7 counts the observed data as one of the permutations; it is what makes the Monte Carlo test valid. For a two-sided test, compare $\lvert t_j \rvert \ge \lvert t \rvert$. With floating-point data, two splits with the same multiset of values can give statistics that differ in the last bit, so the code accepts $t_j \ge t - 10^{-9} \max(1, \lvert t \rvert)$ in lines L6 and L10.

The paired version is the same with sign vectors in place of splits: line L4 draws each sign independently with probability $1/2$, and line L9 lists the $2^n$ sign vectors.

## Example

**A trace.** Take group 1 $= (12, 15, 19)$ and group 2 $= (9, 11, 10, 14)$, so $n = 7$, $m = 3$ and $\binom{7}{3} = 35$ splits. For a fixed $n$ and $m$ the difference of the means is an increasing function of the sum of group 1, so the test can rank the splits by that sum. The observed sum is 46 (line L1, difference of means $13/3$). The largest sums are 48 ($19 + 15 + 14$), 46 (the observed split), then 45. Line L10 counts 2 splits, and line L11 returns $p = 2/35 = 0.0571$. The two-sided p-value is $4/35 = 0.114$.

**The mouse data.** Efron and Tibshirani (Table 2.1) give survival times in days for 7 treated mice, 94, 197, 16, 38, 99, 141, 23, and 9 controls, 52, 104, 146, 10, 51, 30, 40, 27, 46. The difference of the means is $1930/63 = 30.63$. Of the $\binom{16}{7} = 11440$ splits, 1613 give a difference at least as large, so the exact one-sided p-value is $1613/11440 = 0.1410$; the two-sided value is $3184/11440 = 0.2783$. The Monte Carlo test with $b = 1000$ and `random.Random(1)` counted $c = 133$ and returned $134/1001 = 0.1339$. Its standard error is about $\sqrt{0.141 \cdot 0.859/1000} = 0.011$, so the difference from the exact value is normal noise. The drug effect is not significant.

**Darwin's plants.** Darwin grew 15 pairs of Zea mays plants, one cross-fertilized and one self-fertilized in each pair. Fisher used the differences in height, in eighths of an inch: 49, $-67$, 8, 16, 6, 23, 28, 41, 14, 29, 56, 24, 75, 60, $-48$, with sum 314. Under $H_0$ each difference is symmetric about 0, so each of the $2^{15} = 32768$ sign vectors is equally likely. Exactly 1726 of them give $\lvert \sum \pm d_i \rvert \ge 314$, so the two-sided p-value is $1726/32768 = 0.0527$, the value that Fisher reported. The one-sided p-value is $863/32768 = 0.0263$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Under the randomization hypothesis, the observed data $Z$ and the transformed data $gZ$ have the same law. Condition on the orbit $\{gZ : g \in G\}$. Given the orbit, the observed point is uniform on it, so the rank of $T(Z)$ among the $\lvert G \rvert$ values $T(gZ)$ is uniform, with ties broken against rejection. Hence $P(p \le \alpha \mid \text{orbit}) \le \alpha$ for every $\alpha$, and the same bound holds without conditioning. For the Monte Carlo version, $T(Z), T(g_1 Z), \ldots, T(g_b Z)$ are exchangeable under $H_0$, because $(g_1 Z, \ldots, g_b Z)$ given $Z$ is a sample of $b$ uniform points of the orbit and $Z$ is itself a uniform point. So the rank of $T(Z)$ among the $b + 1$ values is uniform, and $P(p_b \le \alpha) \le \lfloor \alpha (b + 1) \rfloor/(b + 1) \le \alpha$ for every $b$.

The bound is the true size, not only an upper bound, when $\alpha \lvert G \rvert$ is an integer and the values $T(gz)$ are distinct. The tests check both claims: all splits of an 8-point sample give exactly the size $1/70$ at $\alpha = 1/70$, and 3000 Monte Carlo tests with $b = 19$ on normal data and seed 11 rejected at $\alpha = 0.05$ in $5.0\%$ of cases.

## Complexity

Let $C_T(n)$ be the cost of the statistic; for the difference of the means $C_T(n) = \Theta(n)$.

- **Monte Carlo.** Each of the $b$ rounds shuffles in $\Theta(n)$ and computes the statistic, so the time is $\Theta(b (n + C_T(n))) = \Theta(b n)$ for the mean difference. The space is $\Theta(n)$ for one copy of the data.
- **Exact.** $\binom{n}{m}$ splits at $\Theta(n)$ each, or $2^n$ sign vectors for the paired test. This is feasible up to about $\binom{n}{m} \approx 10^7$. A revolving-door order of the subsets changes one element per step and updates the sum in $\Theta(1)$, which removes the factor $n$.
- **Integer data.** For a sum statistic with integer values of total size $S$, a dynamic program counts the subsets of size $m$ with each sum in $O(m n S)$ time, which is much less than $\binom{n}{m}$ for large balanced groups.

The Monte Carlo p-value estimates the exact $p$ with standard error $\sqrt{p(1 - p)/b}$, so $b = 10^4$ gives two correct decimals for $p$ near $0.05$.

## Properties

- **Exact level.** $P_{H_0}(p \le \alpha) \le \alpha$ for every sample size, every statistic and every $b$. No normal or large-sample approximation is used.
- **Conditional.** The test is conditional on the observed set of values (the order statistics in the two-sample case), which is a sufficient statistic under $H_0$. The null distribution changes from one data set to the next.
- **Discrete.** The p-value takes only the values $k/\lvert G \rvert$, so the size is at most $\alpha$ and can be below it. A randomized test that rejects with a suitable probability at the boundary value has size exactly $\alpha$.
- **Any statistic.** The level does not depend on the choice of $T$; only the power does. Choose the statistic for the alternative you care about.
- **Power.** Hoeffding (1952) showed that the permutation test based on the mean difference has asymptotically the same power as the [two-sample t-test](/student-t-test/) under normality, so little is lost when the t-test is right.

## Variants and improvements

- **Sign-flip test.** For paired data or a one-sample test of symmetry, flip signs instead of permuting labels, as in the Darwin example. The [sign test](/sign-test/) and the [Wilcoxon signed-rank test](/wilcoxon-signed-rank-test/) are sign-flip tests on signs and on signed ranks.
- **Rank tests.** The [Mann-Whitney U test](/mann-whitney-u-test/) is the permutation test with the rank sum as the statistic. Its null law does not depend on the data, so it can be tabled.
- **Tests of independence.** Permute the $Y$ values against the $X$ values and recompute a correlation. With ranks this is [Spearman's rank correlation](/spearman-rank-correlation/) test; on a $2 \times 2$ table it is [Fisher's exact test](/fisher-exact-test/).
- **Randomization tests in experiments.** In a [randomized experiment](/randomized-experiment/), the sharp null hypothesis of no effect on any unit fixes all [potential outcomes](/potential-outcomes-framework/). Then the known randomization scheme, not a model, gives the null distribution, and the units need not be a random sample.
- **Studentized statistics.** With unequal variances, the permutation distribution of a studentized statistic, such as Welch's $t$, is asymptotically valid for equal means, and it stays exact under full exchangeability (Janssen 1997; Chung and Romano 2013).
- **Multiple testing.** Permuting whole rows keeps the dependence between many statistics. The [Westfall-Young procedure](/westfall-young-procedure/) uses the permutation law of the maximum statistic to control the family-wise error rate.
- **Comparison with the bootstrap.** A bootstrap test resamples with replacement from an estimate of the null distribution and is only approximate. The permutation test resamples without replacement and is exact, but it needs a null hypothesis that makes the data exchangeable. See the [bootstrap method](/bootstrap-method/).

## When to use it

Use it when the null hypothesis states that the labels do not matter: two groups that come from the same distribution, a randomized treatment with no effect, or two variables that are independent. Use it when the sample is small or the distribution is skewed and you do not trust a t-test or a normal approximation, and when the statistic has no known null distribution, such as a difference of medians or of trimmed means. If you want a confidence interval for an effect, invert a family of shifted permutation tests ([test-interval duality](/test-interval-duality/)), or use the bootstrap.

## Pitfalls

- **The wrong null hypothesis.** The test checks that the distributions are equal, not that the means are equal. With group 1 of size 5 and standard deviation 4 and group 2 of size 20 and standard deviation 1, both with mean 0, the two-sided test of the mean difference at level $0.05$ rejected in $30.3\%$ of 1000 runs ($b = 199$, seed 21). Use a studentized statistic, or use [Welch's t-test](/welch-t-test/), when the variances can differ.
- **A p-value of 0.** The estimate $c/b$ can be 0 and is not a valid p-value: it rejects too often for small $b$. Use $(1 + c)/(1 + b)$ (Phipson and Smyth 2010).
- **Data that are not exchangeable.** Time series, clustered data and paired data are not exchangeable as single values. Permute whole clusters, flip signs within pairs, or use a block method. A plain permutation of positively autocorrelated data can give a size far above $\alpha$.
- **A biased shuffle.** Swapping each position with a uniform position in $1..n$ does not give uniform permutations. Use the [Fisher-Yates shuffle](/fisher-yates-shuffle/).
- **Ties in floating point.** The observed split must count as "at least as extreme" as itself. Compare with a small tolerance, or with exact arithmetic, as the code does.
- **Reusing the same random permutations.** For one test this is fine. But to compare the power of two statistics, use the same permutations for both, or the comparison has extra noise.

## Implementations

## History

R. A. Fisher gave the idea in *The Design of Experiments* (1935). In Section 21 he took Darwin's 15 pairs of plants, assumed under the null hypothesis that each difference was equally likely to have either sign, and counted that 1726 of the 32768 sign combinations gave a total at least as large as the observed 314 in absolute value. The result, $5.27\%$, was close to the $t$-test's value, and Fisher used it to argue that the t-test is a good approximation to the exact test. E. J. G. Pitman (1937) gave the two-sample test for samples from any populations and computed the moments of its permutation distribution. Hoeffding (1952) proved the large-sample equivalence with the t-test. With fast computers, the Monte Carlo version became a standard method; Phipson and Smyth (2010) showed why the "+1" correction is necessary.

## References
