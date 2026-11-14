---
tag: 8KPP1Q
kind: algorithm
slug: wilcoxon-signed-rank-test
name: Wilcoxon signed-rank test
aliases:
- signed-rank test
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Tests whether paired differences are symmetric about zero by the sum of the ranks of their absolute values that belong to positive differences.
model: real-ram
complexity:
  vars: {n: the number of nonzero differences}
  time: {worst: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1945
  people: [Frank Wilcoxon]
  note: Wilcoxon gave the signed-rank test and the rank-sum test in one short paper of 1945, with tables of the exact null law for small samples.
prereqs: [sign-test, statistical-hypothesis-test, p-value]
see_also: [mann-whitney-u-test, hodges-lehmann-estimator, student-t-test, permutation-test, counting-subset-sum, test-interval-duality, statistical-power, friedman-test]
sources:
  - book: isbn:9780470387375
    title: Myles Hollander, Douglas A. Wolfe and Eric Chicken, Nonparametric Statistical Methods, third edition, Wiley, 2014
    locator: Chapter 3 (the one-sample location problem), the section on the Wilcoxon signed rank test
  - book: isbn:9780387352121
    title: E. L. Lehmann, Nonparametrics, Statistical Methods Based on Ranks, revised edition, Springer, 2006
    locator: The chapter on paired comparisons and the one-sample problem (the signed-rank test, ties, zeros and efficiency)
  - paper: doi:10.2307/3001968
    title: Frank Wilcoxon, Individual comparisons by ranking methods, Biometrics Bulletin 1(6), 1945
    locator: pp. 80 to 83 (the paired-sample test by signed ranks, with a table of exact tail probabilities)
---

The Wilcoxon signed-rank test checks whether paired differences are symmetric about zero, or about a given value $\mu_0$. It ranks the absolute differences and adds the ranks of the positive ones. Under the null hypothesis each sign is a fair coin given the absolute values, so the sum has an exact law that depends only on the ranks, and a short dynamic program counts it. Unlike the [sign test](/sign-test/), it uses the sizes of the differences through their ranks, so it is nearly as powerful as the paired [t-test](/student-t-test/) for normal data and much better for heavy tails. The price is the extra assumption of symmetry: it is not a test of the [median](/median/) alone.

## In plain words

Ten patients try two drugs, and for each one we note how much more the second drug helped. Put the differences in order of size, ignoring the sign, and number them 1, 2, 3 and so on. Then add up the numbers that belong to differences where the second drug was better.

If the drugs are equally good and the differences are spread evenly around zero, each number is equally likely to land on the plus side or the minus side, like a coin toss. So the sum is usually near half the total. A sum close to the total means the large differences all point the same way, which is hard to explain by luck. Small differences count little and large ones count much, so one big outlier counts only as the largest rank, not as its full size.

## The problem

**Model.** $D_1, \ldots, D_N$ are independent. In the paired design $D_i = Y_i - X_i$; in the one-sample design $D_i = X_i - \mu_0$. Values $D_i = 0$ are dropped, and $n$ is the number of nonzero values left.

**Hypotheses.** $H_0$: each $D_i$ has a distribution symmetric about $0$, that is, $D_i$ and $-D_i$ have the same law. The $D_i$ may have different symmetric laws. The alternatives are "greater" (the $D_i$ tend to be positive), "less" and two-sided. A shift model $D_i = \theta + E_i$, with $E_i$ symmetric about 0, is the usual setting, and then $H_0$ is $\theta = 0$.

**Statistic.** Rank $\lvert D_1 \rvert, \ldots, \lvert D_n \rvert$ from $1$ to $n$, giving tied values the mean of their ranks (midranks). Then $W^+ = \sum_{i : D_i > 0} R_i$.

**Null distribution.** Exact and conditional on the absolute values. Under $H_0$, given $\lvert D_1 \rvert, \ldots, \lvert D_n \rvert$, the signs are independent fair coins, so $W^+$ has the law of $\sum_i \varepsilon_i R_i$ with independent $\varepsilon_i \in \{0, 1\}$, $P(\varepsilon_i = 1) = 1/2$. Each of the $2^n$ sign vectors has probability $2^{-n}$. The mean is $n(n + 1)/4$ and the variance is $n(n + 1)(2n + 1)/24 - \sum_j (t_j^3 - t_j)/48$, where $t_j$ are the sizes of the groups of tied $\lvert D_i \rvert$. The law is symmetric about its mean.

**P-values.** With $c(w)$ the number of sign vectors whose sum is $w$:

- Greater: $P_{hi}(w) = \sum_{v \ge w} c(v) / 2^n$.
- Less: $P_{lo}(w) = \sum_{v \le w} c(v) / 2^n$.
- Two-sided: $p(w) = \min\{1, 2 \min(P_{lo}(w), P_{hi}(w))\}$. The null law is symmetric about its mean, so doubling equals $P(\lvert W^+ - E W^+ \rvert \ge \lvert w - E W^+ \rvert)$.

**Rejection rule and size.** Reject at level $\alpha$ when $p(w) \le \alpha$. The size is at most $\alpha$ for every $n$, and with ties it is at most $\alpha$ conditionally on the tie pattern. The null law is discrete, so the size is usually below $\alpha$. For $n = 20$ without ties the two-sided test at $\alpha = 0.05$ rejects for $W^+ \le 52$ or $W^+ \ge 158$, with size $2 \cdot 0.024220 = 0.048440$.

**Sensitivity and power.** The test detects a shift of a symmetric law. It also reacts to asymmetry: a skewed law with median $0$ is outside $H_0$, and the test rejects it often (see Properties). In the shift model its asymptotic relative efficiency against the t-test is $3/\pi \approx 0.955$ under normal errors, and at least $0.864$ for every symmetric continuous law (Hodges and Lehmann 1956).

## The algorithm

```pseudo id=main
SIGNED-RANK-TEST(d_1, ..., d_n, alternative)
L1  drop every d_i = 0, and let n be the number of values left
L2  r_i ← 2 · (midrank of |d_i| among |d_1|, ..., |d_n|)   ▷ doubled, so every r_i is an integer
L3  w ← sum of r_i over the i with d_i > 0
L4  T ← r_1 + ... + r_n; c[0] ← 1; c[s] ← 0 for s = 1, ..., T
L5  for i ← 1 to n
L6      for s ← T down to r_i: c[s] ← c[s] + c[s - r_i]   ▷ c[s] counts subsets with sum s
L7  U ← c[w] + ... + c[T]; L ← c[0] + ... + c[w]
L8  return U / 2^n, L / 2^n or min(1, 2 · min(U, L) / 2^n) for greater, less or two-sided
```

The code returns $W^+ = w/2$ and the p-value. Lines L5 and L6 are the standard [count of subsets by their sum](/counting-subset-sum/); the downward loop in line L6 uses each $r_i$ at most once. Midranks of tied values can be half-integers, so the code doubles every rank and counts doubled sums; then all indices are integers and every count is exact. The division by $2^n$ in line L8 is one exact rational, rounded once to a float. The code also offers the normal approximation $z = (W^+ - n(n+1)/4 \mp 1/2) / \sigma$ with the tie-corrected variance $\sigma^2$ given above.

## Example

**Mixed signs.** Take the differences $1.8, -0.6, 3.1, 2.4, -1.3, 0.9, 2.2, 0.0, 1.5, -0.4$. Line L1 drops the zero, so $n = 9$. The absolute values in order are $0.4, 0.6, 0.9, 1.3, 1.5, 1.8, 2.2, 2.4, 3.1$, with ranks 1 to 9. The negative differences have ranks 1, 2 and 4, so $W^+ = 45 - 7 = 38$. A value $W^+ \ge 38$ means the negative ranks sum to at most 7, and 19 of the 512 subsets of $\{1, \ldots, 9\}$ have a sum of at most 7. So the one-sided p-value is $19/512 = 0.0371$ and the two-sided p-value is $19/256 = 0.0742$. The normal approximation gives $z = 1.777$ and $p = 0.0756$ with the continuity correction, and $z = 1.836$ and $p = 0.0663$ without it. The sign test on the same data gives $65/128 = 0.508$, because it ignores that the three negative values are among the four smallest.

**The counts.** For $n = 4$ without ties the doubled ranks are $2, 4, 6, 8$, and lines L5 and L6 give the counts of $W^+ = 0, 1, \ldots, 10$ as $1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1$, which add up to $16 = 2^4$. With ranks $1, 2.5, 2.5, 4$ (a tie in the middle) the doubled ranks are $2, 5, 5, 8$, and the nonzero counts are at the doubled sums $0, 2, 5, 7, 8, 10, 12, 13, 15, 18, 20$, with counts $1, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1$. Both lists are symmetric, as the proof requires.

**Paired data.** For the sleep data of Cushny and Peebles (1905) the 9 nonzero differences are all positive, so $W^+ = 45$, the largest value, and the two-sided p-value is $2/512 = 1/256$, the same as for the sign test. The normal approximation gives $0.0091$ with the continuity correction and $0.0076$ without it.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Given the absolute values, symmetry of each $D_i$ makes its sign a fair coin independent of everything else, and the ranks are fixed by the absolute values. So the conditional null law of $W^+$ gives each of the $2^n$ subsets of ranks the probability $2^{-n}$. After step $i$ of line L5, $c[s]$ is the number of subsets of $\{r_1, \ldots, r_i\}$ with sum $s$, because a subset either leaves out $r_i$ (the old $c[s]$) or contains it (the old $c[s - r_i]$). Line L7 then gives exact tail counts, and each p-value is valid by the argument used for the sign test.

## Complexity

Lines L1 to L3 cost $O(n \log n)$ for the sort. The total $T$ of the doubled ranks is $n(n + 1)$, so line L6 runs $\Theta(n^2)$ times for each of the $n$ values of $i$, and lines L5 and L6 cost $\Theta(n^3)$ additions. The array $c$ has $n(n+1) + 1$ entries, so the space is $\Theta(n^2)$. The counts are integers below $2^n$, so in bit operations the cost is $O(n^4)$. For $n$ in the hundreds the normal approximation is accurate and costs $O(n \log n)$.

## Properties

- **Distribution-free under symmetry.** The conditional null law depends only on the tie pattern, not on the law of the $D_i$.
- **Conservative and exact.** The size is at most $\alpha$, and the p-values are exact rationals.
- **Robust.** A wild value enters $W^+$ only through its rank, which is at most $n$, however large the value is.
- **Efficiency.** In the shift model the efficiency against the t-test is $3/\pi$ for normal errors and at least $0.864$ for every symmetric law; for heavy tails it can be arbitrarily large. A Monte Carlo run with $n = 20$, $D \sim N(0.5, 1)$, $r = 2000$ samples and seed 12 gave power $0.540$ at $\alpha = 0.05$, against $0.387$ for the sign test on the same samples.
- **Symmetry matters.** A Monte Carlo run with $n = 20$, $r = 2000$ samples of $D = E - \ln 2$, $E$ exponential with mean 1 (median 0 but skewed), and seed 11 rejected at $\alpha = 0.05$ in $10.1\%$ of samples. The sign test rejected in $3.9\%$. The signed-rank test is a test of symmetry about $0$, not of the median.

## Variants and improvements

- **Estimator and interval.** The [Hodges-Lehmann estimator](/hodges-lehmann-estimator/) of the center is the median of the Walsh averages $(D_i + D_j)/2$, $i \le j$. Inverting the test gives a confidence interval between two order statistics of the Walsh averages, an example of [test-interval duality](/test-interval-duality/).
- **Zeros.** Dropping the zeros is Wilcoxon's rule and the one the code uses. Pratt (1959) proposed ranking the zeros with the other values and then dropping them from the sum, which changes the null law.
- **Normal approximation.** $z$ with the tie-corrected variance and a continuity correction of $1/2$. For $n = 9$ it gave $0.0756$ against the exact $0.0742$.
- **Paired permutation test.** Using the differences themselves in place of their ranks gives the [permutation test](/permutation-test/) over sign changes. It is exact under the same hypothesis, but its null law depends on the data, so it cannot be tabulated.
- **More than two conditions.** For blocks with more than two treatments, the [Friedman test](/friedman-test/) ranks within each block.

## When to use it

Use it for paired data or for one sample about a point, when the differences are plausibly symmetric but maybe not normal: measurement errors, before and after scores on an interval scale, differences of logarithms. It loses little against the t-test for normal data and wins for heavy tails. If the distribution of the differences may be skewed and the question is about the median, use the [sign test](/sign-test/). If only the direction of each difference is reliable, the ranks of the sizes mean nothing, and the sign test is again the right choice.

## Pitfalls

- **It is not a median test.** For skewed differences with median 0 it rejected in $10.1\%$ of Monte Carlo samples at the nominal $5\%$.
- **Ranks need meaningful differences.** Ranking $\lvert D_i \rvert$ assumes that differences can be compared across pairs. For ordinal ratings this may be false.
- **Ties and the normal approximation.** Without the tie correction to the variance, the approximation is conservative. The exact count in lines L5 and L6 handles ties with no approximation.
- **Large $n$.** The exact count costs $\Theta(n^3)$ time and $\Theta(n^2)$ space; for $n$ in the thousands use the normal approximation.
- **Two different "Wilcoxon tests".** The signed-rank test is for paired data. For two independent samples, use the rank-sum test, which is the [Mann-Whitney U test](/mann-whitney-u-test/).

## Implementations

## History

Frank Wilcoxon, a chemist at the American Cyanamid Company, gave the signed-rank test for paired comparisons and the rank-sum test for two samples in one paper of 1945, with tables for small samples, as quick replacements for the t-test. Hodges and Lehmann (1956) showed that the loss of efficiency against the t-test is small, which changed the view of rank tests from quick approximations to serious tools. Pratt (1959) studied the handling of zeros and ties.

## References
