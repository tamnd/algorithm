---
tag: 5M1BYQ
kind: definition
slug: spearman-rank-correlation
name: Spearman's rank correlation coefficient
aliases:
- Spearman's rho
- Spearman correlation
area: statistics-and-inference/nonparametric-and-robust-statistics
level: intro
summary: The Pearson correlation of the ranks of two variables. It measures monotone association and is the basis of a rank test of independence.
prereqs: [order-statistic, permutation-test]
see_also: [kendall-tau-distance, spearman-footrule, ranking-comparison-kendall-tau, friedman-test, chi-squared-test-of-independence, covariance-matrix, kemeny-rank-aggregation, mann-whitney-u-test]
sources:
  - paper: doi:10.2307/1412159
    title: C. Spearman, The proof and measurement of association between two things, American Journal of Psychology 15(1), 1904
    locator: pp. 72 to 101 (the measurement of correlation from the ranks of the two variables)
  - book: isbn:9780470387375
    title: Myles Hollander, Douglas A. Wolfe and Eric Chicken, Nonparametric Statistical Methods, third edition, Wiley, 2014
    locator: The chapter on the independence problem (the Spearman rank correlation test, its exact null law and its large-sample approximation)
  - book: isbn:9780387352121
    title: E. L. Lehmann, Nonparametrics, Statistical Methods Based on Ranks, revised edition, Springer, 2006
    locator: The chapter on tests of randomness and independence (the rank correlation statistics and their null laws)
---

Spearman's rank correlation coefficient $r_S$ of paired data $(x_1, y_1), \ldots, (x_n, y_n)$ is the ordinary (Pearson) correlation coefficient of the ranks of the $x$ values and the ranks of the $y$ values. It is $+1$ when $y$ is a strictly increasing function of $x$, $-1$ when it is a strictly decreasing one, and near 0 when the order of the $y$ values has nothing to do with the order of the $x$ values. Because only ranks enter, it does not change under increasing transformations of either variable, and a single extreme value moves it by a bounded amount. Under independence of $X$ and $Y$, the ranks of the $y$ values are a uniform random permutation relative to those of the $x$ values, so $r_S$ has an exact null law that depends only on $n$, and it gives a [permutation test](/permutation-test/) of independence.

## Definition

Let $R_i$ be the rank of $x_i$ among $x_1, \ldots, x_n$ and $S_i$ the rank of $y_i$ among $y_1, \ldots, y_n$. Tied values get the average of the ranks they cover, the midrank. Both rank vectors have mean $\bar r = (n+1)/2$. **Spearman's rank correlation coefficient** is

$$r_S = \frac{\sum_i (R_i - \bar r)(S_i - \bar r)}{\sqrt{\sum_i (R_i - \bar r)^2 \sum_i (S_i - \bar r)^2}},$$

defined when neither variable is constant. Without ties, both sums of squares equal $n(n^2 - 1)/12$, and with $d_i = R_i - S_i$,

$$r_S = 1 - \frac{6 \sum_i d_i^2}{n(n^2 - 1)}.$$

With ties this short formula is not the correlation of the midranks.

**Null law.** If the pairs are independent and $X$ is independent of $Y$, with continuous distributions, then given the ranks $R$, the vector $S$ is a uniform random permutation of $1, \ldots, n$. So the law of $r_S$ is that of $1 - 6\sum_i (i - \pi(i))^2 / (n(n^2 - 1))$ for a uniform random permutation $\pi$, the same for every pair of continuous distributions. Its mean is 0 and its variance is $1/(n-1)$. With ties, the same holds conditionally on the midranks, with the midranks of $y$ permuted. The test of independence rejects for large $\lvert r_S \rvert$, or for large or small $r_S$ in one direction, with p-values from this law, computed by counting permutations for small $n$, by sampling permutations, or from the approximation $r_S \sqrt{n - 1} \approx N(0, 1)$.

**Population version.** For a pair $(X, Y)$ with continuous marginal distribution functions $F$ and $G$, $\rho_S = \mathrm{corr}(F(X), G(Y)) = 12\, E[F(X) G(Y)] - 3$, and $r_S \to \rho_S$ as $n \to \infty$.

## Examples and non-examples

**A small sample.** Hours of study $x = 2, 5, 1, 8, 4, 6$ and scores $y = 55, 70, 52, 80, 75, 68$. The ranks are $R = 2, 4, 1, 6, 3, 5$ and $S = 2, 4, 1, 6, 5, 3$, so $d = 0, 0, 0, 0, -2, 2$, $\sum d_i^2 = 8$ and $r_S = 1 - 48/210 = 27/35 = 0.7714$. The Pearson correlation of the raw values is $0.8873$, and Kendall's tau is $0.6$.

**Monotone but not linear.** For $x = 1, \ldots, 10$ and $y = e^x$, $r_S = 1$, since the order is the same. The Pearson correlation is $0.7169$, because the relation is far from a line.

**One extreme value.** For $x = 1, \ldots, 10$ and $y = 5, 3, 6, 2, 7, 4, 1, 8, 3.5, 60$, $r_S = 0.2848$ and the Pearson correlation is $0.5203$. Replace $60$ by $9$: $r_S$ stays $0.2848$, since $9$ is still the largest value, while the Pearson correlation drops to $0.3041$.

**Ties.** For $x = 1, 2, 2, 3, 4, 4, 5$ and $y = 2, 1, 3, 3, 5, 4, 4$, the midranks are $1, 2.5, 2.5, 4, 5.5, 5.5, 7$ and $2, 1, 3.5, 3.5, 7, 5.5, 5.5$. The correlation of the midranks is $r_S = 5/6 = 0.8333$. The short formula gives $1 - 6 \cdot 9/336 = 47/56 = 0.8393$, a different number.

**The exact null law for $n = 4$.** The 24 permutations give $\sum d_i^2 = 0, 2, 4, \ldots, 20$ with counts $1, 3, 1, 4, 2, 2, 2, 4, 1, 3, 1$, so $r_S$ takes the values $1, 0.8, 0.6, \ldots, -1$, and the law is symmetric about 0. $P(r_S = 1) = 1/24 = 0.0417$, so with four pairs no one-sided test at level $0.01$ can reject. Counting all permutations gives the upper 5% points below; each is the smallest value $c$ with $P(r_S \ge c) \le 0.05$:

| $n$ | $c$ | $P(r_S \ge c)$ |
|---|---|---|
| 5 | 0.9 | 0.0417 |
| 6 | 0.8286 | 0.0292 |
| 7 | 0.7143 | 0.0440 |
| 8 | 0.6429 | 0.0481 |
| 9 | 0.6 | 0.0484 |

The same counts confirm the mean 0 and the variance $1/(n-1)$ for $n = 4, \ldots, 9$. For $n = 9$, $P(r_S \ge 2/3) = 0.02944$, and the normal approximation with standard deviation $1/\sqrt{8}$ gives $0.02967$.

**A population value.** For a bivariate normal pair with correlation $r$, $\rho_S = (6/\pi) \arcsin(r/2)$, which is $0.4826$ for $r = 0.5$. In a Monte Carlo run with $n = 2000$ pairs, $200$ samples and seed 81, the mean of $r_S$ was $0.4815$.

**Non-example: a relation that is not monotone.** For $x = -3, \ldots, 3$ and $y = x^2$, $r_S = 0$, although $y$ is a function of $x$. $r_S$ measures monotone association only; $r_S = 0$ does not mean independence.

**Non-example: Pearson's coefficient.** The Pearson correlation of the raw values measures linear association and can change under increasing transformations, as the examples above show. Spearman's coefficient is Pearson's coefficient applied to the ranks, not to the values.

## Related definitions

- **Kendall's tau.** The share of concordant minus the share of discordant pairs, a linear function of the [Kendall tau distance](/kendall-tau-distance/) between the two rankings. Enumeration of all permutations for $n = 5, \ldots, 8$ found $-1 \le 3\tau - 2r_S \le 1$, with both ends reached. See also [comparing rankings with Kendall's tau](/ranking-comparison-kendall-tau/).
- **Spearman's footrule.** $\sum_i \lvert R_i - S_i \rvert$, the [footrule distance](/spearman-footrule/), with absolute differences in place of squares.
- **Kendall's coefficient of concordance.** For $b$ rankings of the same $k$ items, $W$ measures agreement, and the mean of the $\binom{b}{2}$ pairwise Spearman coefficients is $(bW - 1)/(b - 1)$. Its test is the [Friedman test](/friedman-test/).
- **Rank tests of association.** For categorical data the [chi-squared test of independence](/chi-squared-test-of-independence/) plays the role that the Spearman test plays for ordered data.

## References
