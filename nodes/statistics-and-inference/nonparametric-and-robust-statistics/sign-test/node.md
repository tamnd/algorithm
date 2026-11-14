---
tag: R4JDYX
kind: algorithm
slug: sign-test
name: Sign test
aliases:
- binomial sign test
area: statistics-and-inference/nonparametric-and-robust-statistics
level: intro
summary: Tests a median, or paired differences, by the number of positive signs, which is Binomial(n, 1/2) under the null once zeros are dropped. Exact for every n and needs almost no assumptions.
model: real-ram
complexity:
  vars: {n: the number of nonzero differences}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1710
  people: [John Arbuthnot, W. J. Dixon, A. M. Mood]
  note: Arbuthnot's comparison of male and female christenings in 82 years is a one-sided sign test. Dixon and Mood (1946) collected the earlier results with a table of significance levels.
prereqs: [binomial-test, median, statistical-hypothesis-test, p-value]
see_also: [wilcoxon-signed-rank-test, mcnemar-test, hodges-lehmann-estimator, student-t-test, order-statistic, test-interval-duality, statistical-power, permutation-test]
sources:
  - book: isbn:9780470387375
    title: Myles Hollander, Douglas A. Wolfe and Eric Chicken, Nonparametric Statistical Methods, third edition, Wiley, 2014
    locator: Chapter 3 (the one-sample location problem), Section 3.4 (the Fisher sign test and the estimators and interval that come from it)
  - book: isbn:9780387352121
    title: E. L. Lehmann, Nonparametrics, Statistical Methods Based on Ranks, revised edition, Springer, 2006
    locator: The chapter on paired comparisons and the one-sample problem (the sign test and its efficiency against the t-test)
  - paper: doi:10.1080/01621459.1946.10501898
    title: W. J. Dixon and A. M. Mood, The statistical sign test, Journal of the American Statistical Association 41(236), 1946
    locator: pp. 557 to 566 (a summary of earlier results, a table of significance levels and worked examples)
  - paper: doi:10.1098/rstl.1710.0011
    title: John Arbuthnot, An argument for Divine Providence, taken from the constant regularity observed in the births of both sexes, Philosophical Transactions of the Royal Society 27, 1710
    locator: pp. 186 to 190 (82 years of christenings, each with more males than females)
---

The sign test checks whether a [median](/median/) equals a given value $\mu_0$, or whether paired differences are as likely to be positive as negative. It keeps only the sign of each observation. Under the null hypothesis each nonzero sign is a fair coin, so the number of positive signs $S$ has the exact law $\text{Binomial}(n, 1/2)$, and the test is a [binomial test](/binomial-test/) with $p_0 = 1/2$. It needs no normality and no symmetry, it is exact for every $n$, and it is cheap. The price is power: it throws away the sizes of the differences, so when the data are close to normal the [t-test](/student-t-test/) and the [Wilcoxon signed-rank test](/wilcoxon-signed-rank-test/) find a real effect with fewer observations.

## In plain words

Ten patients try two sleeping drugs. For each patient, write a plus if the second drug gave more sleep and a minus if the first did. If the drugs are equally good, each sign is like a coin toss. Nine pluses out of nine (one patient had a tie and is left out) is very unlikely for a fair coin: the chance of a result this lopsided in either direction is 2 in 512. So the second drug looks better.

The test does not care whether the second drug gave 10 minutes or 5 hours more sleep. Only the direction counts. That makes it safe with strange data and outliers, but it also makes it slow to notice small effects.

## The problem

**Model.** $D_1, \ldots, D_n$ are independent. In the paired design $D_i = Y_i - X_i$ is the difference within pair $i$; in the one-sample design $D_i = X_i - \mu_0$. The $D_i$ need not have the same distribution. Values $D_i = 0$ are dropped, and $n$ is the number of nonzero values that remain.

**Hypotheses.** $H_0$: $P(D_i > 0) = P(D_i < 0)$ for every $i$. For identically distributed continuous data this says that $\mu_0$ is a median of the distribution. The alternatives are "greater" ($P(D_i > 0) > 1/2$), "less" ($P(D_i > 0) < 1/2$) and two-sided.

**Statistic.** $S = \#\{i : D_i > 0\}$, the number of positive signs.

**Null distribution.** Exact and conditional on the number of nonzero values: under $H_0$, given that $D_i \ne 0$, the event $D_i > 0$ has probability $1/2$, and the events are independent, so $S \sim \text{Binomial}(n, 1/2)$.

**P-values.** Write $b(k) = \binom{n}{k} / 2^n$.

- Greater: $P_{hi}(s) = \sum_{k \ge s} b(k)$.
- Less: $P_{lo}(s) = \sum_{k \le s} b(k)$.
- Two-sided: $p(s) = \min\{1, 2 \min(P_{lo}(s), P_{hi}(s))\}$. The null law is symmetric about $n/2$, so doubling gives the same value as the rule of the binomial test that sums the probabilities of all outcomes at most as likely as $s$. The tests check this for every $n \le 29$.

**Rejection rule and size.** Reject at level $\alpha$ when $p(s) \le \alpha$. The size is at most $\alpha$ for every $n$, so the test is exact in the sense of valid, but conservative: the size equals $\alpha$ only when $\alpha$ is an attainable tail sum. For $n = 20$ and $\alpha = 0.05$ the two-sided test rejects for $S \le 5$ or $S \ge 15$, and its size is $2 \cdot 0.020695 = 0.041389$.

**Sensitivity and power.** The test detects any shift of $P(D > 0)$ away from $1/2$. Its power depends only on $\pi = P(D > 0 \mid D \ne 0)$ and $n$, through $\text{Binomial}(n, \pi)$. For $D \sim N(0.5, 1)$ and $n = 20$, $\pi = \Phi(0.5) = 0.6915$, and the exact two-sided power at $\alpha = 0.05$ is $0.3842$.

## The algorithm

```pseudo id=main
SIGN-TEST(d_1, ..., d_n, alternative)
L1  drop every d_i = 0, and let n be the number of values left
L2  S ← number of d_i > 0
L3  w[0] ← 1; w[k + 1] ← w[k] · (n - k) / (k + 1) for k = 0, ..., n - 1   ▷ w[k] = C(n, k), exact integers
L4  U ← w[S] + ... + w[n]; L ← w[0] + ... + w[S]
L5  if alternative = greater then return U / 2^n
L6  if alternative = less then return L / 2^n
L7  return min(1, 2 · min(U, L) / 2^n)
```

Lines L3 and L4 work with exact integers, and the code divides by $2^n$ only at the end. Python divides two integers with one correct rounding, so the float p-value is the exact rational rounded once, even when it is far below the smallest tail that $1 - P_{lo}$ could show. The code also offers the normal approximation $z = (\lvert S - n/2 \rvert - 1/2) / (\sqrt{n}/2)$ with its continuity correction, and the distribution-free interval for the median described below.

## Example

**Paired data.** The sleep data of Cushny and Peebles (1905), which Student (1908) used, give the extra hours of sleep of 10 patients under two drugs. The differences, drug 2 minus drug 1, are

$$1.2,\ 2.4,\ 1.3,\ 1.3,\ 0.0,\ 1.0,\ 1.8,\ 0.8,\ 4.6,\ 1.4.$$

Line L1 drops the zero, so $n = 9$. Line L2 gives $S = 9$. Line L3 gives the row 1, 9, 36, 84, 126, 126, 84, 36, 9, 1 of Pascal's triangle, and line L4 gives $U = 1$ and $L = 512$. The one-sided p-value is $1/512 = 0.00195$ and the two-sided p-value is $2/512 = 1/256 = 0.00391$. The normal approximation with the continuity correction gives $0.00766$, about twice the exact value; without the correction it gives $0.00270$. At $n = 9$ neither approximation is good.

**Mixed signs.** For the differences $1.8, -0.6, 3.1, 2.4, -1.3, 0.9, 2.2, 0.0, 1.5, -0.4$, again $n = 9$ after the zero is dropped, and $S = 6$. Then $L = 1 + 9 + 36 + 84 + 126 + 126 + 84 = 466$ and $U = 84 + 36 + 9 + 1 = 130$, so the two-sided p-value is $260/512 = 65/128 = 0.508$. The [signed-rank test](/wilcoxon-signed-rank-test/) on the same data gives $0.074$, because the three negative values are the small ones.

**A small tail.** With 900 positive signs out of 1000, the exact one-sided p-value is $6.70 \times 10^{-162}$. Computing it as $1$ minus the sum of $b(k)$ for $k < 900$ in double precision gives exactly $0$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Under $H_0$, condition on the set of indices with $D_i \ne 0$. Each such $D_i$ is positive with probability $1/2$, independently, so $S$ is $\text{Binomial}(n, 1/2)$ given $n$. Lines L3 and L4 compute $2^n P_{hi}$ and $2^n P_{lo}$ exactly. Each p-value is a tail probability of an ordering of the outcomes, or twice the smaller of two such tails, so $P(p \le \alpha) \le \alpha$ given $n$, and therefore also without conditioning.

## Complexity

Line L1 and line L2 scan the data once. Line L3 does $n$ multiplications and divisions and line L4 does at most $2n$ additions, so the time is $\Theta(n)$ arithmetic operations and the list $w$ takes $\Theta(n)$ space. The integers have up to $n$ bits, so counted in bit operations lines L3 and L4 cost $\Theta(n^2)$. With the regularized incomplete beta function, $P_{hi}(s) = I_{1/2}(s, n - s + 1)$ costs much less for large $n$, at the price of floating-point error.

## Properties

- **Distribution-free.** The null law does not depend on the distribution of the $D_i$, and the $D_i$ may even have different distributions, as long as each has median $\mu_0$ and no mass there.
- **Conservative.** The size is at most $\alpha$; for $n = 20$ and $\alpha = 0.05$ it is $0.0414$.
- **Robust.** One wild value changes $S$ by at most 1.
- **Power.** For $D \sim N(\theta, 1)$, the asymptotic relative efficiency of the sign test against the t-test is $2/\pi \approx 0.637$; for the Laplace (double exponential) law it is $2$, and the sign test is then the better test (Lehmann 2006). At $n = 20$ and $D \sim N(0.5, 1)$, the exact power is $0.384$. A Monte Carlo run with $r = 2000$ samples and seed 12 gave power $0.387$ for the sign test and $0.540$ for the signed-rank test on the same samples.
- **Validity without symmetry.** A Monte Carlo run with $n = 20$, $r = 2000$ samples of $D = E - \ln 2$, $E$ exponential with mean 1 (median 0, skewed), and seed 11 rejected at $\alpha = 0.05$ in $3.9\%$ of samples. The signed-rank test rejected in $10.1\%$, because it tests symmetry, not the median.

## Variants and improvements

- **Interval for the median.** Inverting the test gives the interval $[X_{(k)}, X_{(n + 1 - k)}]$ between two [order statistics](/order-statistic/), where $k$ is the largest index with $2 P(\text{Binomial}(n, 1/2) \le k - 1) \le \alpha$. Its coverage is exactly $1 - 2 P(\text{Binomial}(n, 1/2) \le k - 1)$ for every continuous distribution. For $n = 20$ and $\alpha = 0.05$, $k = 6$ and the coverage is $0.9586$. For the 10 sleep differences, $k = 2$, the interval is $[0.8, 2.4]$ and its coverage is $501/512 = 0.9785$. This is an example of [test-interval duality](/test-interval-duality/).
- **Normal approximation.** $z = (S - n/2)/(\sqrt{n}/2)$, with the continuity correction of $1/2$ toward $n/2$. It is fine for large $n$ but has no advantage over the exact sum.
- **Ties at $\mu_0$.** Dropping the zeros is the usual rule and keeps the test exact given the number of zeros. Two other rules count each zero as half a success, or assign the zeros a sign at random. Both change the null law, and neither is used by the code.
- **Mid-p and randomized tests.** As for the [binomial test](/binomial-test/), the mid-p value reduces the conservatism at the cost of an exact size bound.
- **McNemar's test.** On a paired $2 \times 2$ table, the exact [McNemar test](/mcnemar-test/) is the sign test applied to the discordant pairs.
- **Signed ranks.** The [Wilcoxon signed-rank test](/wilcoxon-signed-rank-test/) also uses the sizes of the differences, through their ranks. It is more powerful near the normal but needs symmetry.

## When to use it

Use it when only the direction of each difference is reliable (ratings, before and after preferences), when the data have heavy tails or outliers, or when the question is about the median and the distribution may be skewed. For differences that are close to normal, the paired t-test or the signed-rank test needs fewer pairs for the same power. The sign test is also a good first check, because it can be done by hand.

## Pitfalls

- **Zeros.** Count $n$ after dropping the zeros. Using the full sample size with the zeros counted as negative makes the test biased.
- **The normal approximation at small $n$.** For the sleep data at $n = 9$ the approximation with the continuity correction gave $0.0077$ against the exact $0.0039$. Compute the exact value; it costs nothing.
- **Small p-values.** Sum the upper tail directly, or in exact integers as line L4 does. $1 - P(S < s)$ in double precision returned $0$ for a p-value of $6.7 \times 10^{-162}$.
- **Dependent pairs.** The test needs the signs to be independent. Repeated measures on the same subject, or a time series, break this.
- **Not a test of the mean.** For a skewed distribution the median and the mean differ, and the sign test says nothing about the mean.

## Implementations

## History

John Arbuthnot (1710) observed that in each of the 82 years from 1629 to 1710 more boys than girls were christened in London. Under even chances this has probability $(1/2)^{82}$, so his argument is a one-sided sign test with $n = 82$ and $S = 82$, and it is often called the first published significance test. The test was used informally for two centuries. Dixon and Mood (1946) brought the earlier results together in one paper with a table of significance levels and worked examples, and noted that tests such as the t-test are more efficient when the sizes of the differences can be trusted. Hollander, Wolfe and Chicken name it the Fisher sign test.

## References
