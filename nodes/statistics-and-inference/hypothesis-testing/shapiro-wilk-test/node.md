---
tag: F6R58F
kind: algorithm
slug: shapiro-wilk-test
name: Shapiro-Wilk test
aliases:
- Shapiro-Wilk W test
area: statistics-and-inference/hypothesis-testing
level: core
summary: Tests normality by the squared correlation of the ordered sample with weights built from the means and covariances of normal order statistics. It is a powerful omnibus test.
model: real-ram
complexity:
  vars: {n: the sample size}
  time: {worst: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1965
  people: [Samuel S. Shapiro, Martin B. Wilk]
  note: Shapiro and Wilk defined W in 1965 with tables of coefficients and percentage points for n up to 50. Royston gave the approximations for large n that software uses today.
prereqs: [statistical-hypothesis-test, p-value, order-statistic, q-q-plot]
see_also: [anderson-darling-test, kolmogorov-smirnov-test, chi-squared-goodness-of-fit-test, box-cox-transformation, studentized-residual, student-t-test]
sources:
  - paper: doi:10.1093/biomet/52.3-4.591
    title: S. S. Shapiro and M. B. Wilk, An analysis of variance test for normality (complete samples), Biometrika 52(3-4) (1965), pages 591 to 611
    locator: the definition of W, its invariance and its range, and the exact null distribution for n = 3
  - paper: doi:10.1007/BF01891203
    title: Patrick Royston, Approximating the Shapiro-Wilk W-test for non-normality, Statistics and Computing 2(3) (1992), pages 117 to 119
    locator: the polynomial approximations of the coefficients and the normalizing transform of W
  - paper: doi:10.2307/2986146
    title: Patrick Royston, Remark AS R94, A remark on algorithm AS 181, the W-test for normality, Journal of the Royal Statistical Society Series C (Applied Statistics) 44(4) (1995), pages 547 to 551
    locator: the algorithm with the constants used here, for 3 <= n <= 5000
---

The Shapiro-Wilk test checks whether a sample comes from some normal distribution, with the mean and variance unknown. It sorts the sample and measures how well the sorted values lie on a straight line against a fixed set of weights $a_1, \dots, a_n$, which come from the means and covariances of the order statistics of a standard normal sample. The statistic $W$ is the squared correlation between the sorted sample and the weights. It is at most 1, and small values are evidence against normality. $W$ itself is computed exactly. The p-value comes from a normalizing transform by Royston, which is an approximation for every $n \ge 4$; for $n = 3$ the null distribution of $W$ is known exactly. In power studies it is among the best general tests of normality.

## In plain words

Sort the data. If the data are normal, the sorted values plotted against the values that a normal sample of the same size would have on average fall close to a straight line. The test turns "how straight is this line" into one number between 0 and 1, where 1 means a perfect line. The weights that define the line also take into account that neighboring sorted values are related. Because the number is a correlation, it does not change when you shift the data or change the unit. A number much below what normal samples of the same size give is evidence that the data are not normal. A table or a formula turns the number into a p-value.

## The problem

**Model and hypotheses.** The data $x_1, \dots, x_n$ are iid from a continuous distribution $F$, with $3 \le n \le 5000$. The null hypothesis is that $F$ is normal with some mean $\mu$ and some variance $\sigma^2 > 0$, both unknown. The alternative is every other $F$. It is a composite null, and the test is omnibus: it does not target one kind of departure.

**Statistic.** Let $y_1 \le \dots \le y_n$ be the sorted sample. Let $m = (m_1, \dots, m_n)$ be the expected values of the [order statistics](/order-statistic/) of $n$ iid standard normal variables, and $V$ their covariance matrix. The weights are
$$a = \frac{V^{-1}m}{\lVert V^{-1}m \rVert}, \qquad W = \frac{\left(\sum_{i=1}^n a_i y_i\right)^2}{\sum_{i=1}^n (y_i - \bar y)^2}.$$
The weights are antisymmetric, $a_i = -a_{n+1-i}$, so $\sum_i a_i = 0$, and $\sum_i a_i^2 = 1$. Thus $W$ is the squared correlation between $(y_i)$ and $(a_i)$. The vector $V^{-1}m$ is proportional to the coefficients of the generalized least squares estimate of $\sigma$ from the ordered sample, so the numerator is a constant times the square of that estimate, and the denominator is $(n - 1)$ times the sample variance.

**Null distribution.** $W$ is location and scale invariant, so under $H_0$ its law depends on $n$ only. For $n = 3$ it is exact: $P(W \le w) = \frac6\pi\left(\arcsin\sqrt w - \frac\pi3\right)$ for $\frac34 \le w \le 1$. For $n \ge 4$ there is no closed form. Royston fitted a transform $t(W)$ whose null law is close to normal, with mean $\mu_n$ and standard deviation $\sigma_n$ given as polynomials in $n$ or in $\log n$. This is an empirical fit to simulated values. It is not a theorem.

**Rejection rule and size.** Reject at level $\alpha$ when $p \le \alpha$, that is when $W$ is small. For $n = 3$ the size is exactly $\alpha$. For $n \ge 4$ the size is close to $\alpha$ but not exactly $\alpha$. The Monte Carlo sizes below are measured, not proved.

**p-value.** $p = P_{H_0}(W \le W_{\text{obs}})$, a lower tail of $W$, which is the upper tail of the normal approximation of $t(W)$: $p \approx 1 - \Phi\left((t(W) - \mu_n)/\sigma_n\right)$.

**Sensitivity and power.** The test detects skewness and heavy or light tails, and it detects skewness best. In a seeded simulation with 2000 samples for each case, the power at 5% against exponential data was 0.07, 0.17, 0.45, 0.83 and 0.999 for $n = 3, 5, 10, 20, 50$, and against uniform data it was 0.06, 0.06, 0.07, 0.21 and 0.75. With small $n$ the test cannot see much. With very large $n$ it rejects for departures from normality too small to matter.

## The algorithm

```pseudo id=main
SHAPIRO-WILK(x₁, …, xₙ)        ▷ 3 ≤ n ≤ 5000, not all equal
L1  y ← x sorted in increasing order
L2  a ← Royston coefficients for n           ▷ antisymmetric, Σaᵢ² = 1; exact ±√½ for n = 3
L3  ȳ ← Σ yᵢ / n;  SS ← Σ (yᵢ − ȳ)²
L4  b ← Σ_{i=1}^{⌊n/2⌋} a_{n+1−i} (y_{n+1−i} − yᵢ)   ▷ equals Σ aᵢ yᵢ
L5  W ← min(b²/SS, 1)
L6  if n = 3 then return (W, (6/π)(arcsin √W − π/3))   ▷ exact
L7  if n ≤ 11 then
        γ ← −2.273 + 0.459 n
        if log(1 − W) ≥ γ then return (W, 0)
        t ← −log(γ − log(1 − W));  μ, σ ← polynomials in n
    else
        t ← log(1 − W);  μ, σ ← polynomials in log n
L8  z ← (t − μ)/σ
L9  return (W, 1 − Φ(z))
```

**The coefficients (line L2).** The exact $a$ needs the $n \times n$ covariance matrix of normal order statistics, which has no closed form. Royston's approximation, in the form of Algorithm AS R94, uses Blom's scores $\tilde m_i = \Phi^{-1}\left((i - 3/8)/(n + 1/4)\right)$ in place of $m_i$. With $u = 1/\sqrt n$ and $\lVert\tilde m\rVert^2 = \sum_i \tilde m_i^2$,
$$a_n = \frac{\tilde m_n}{\lVert\tilde m\rVert} + 0.221157u - 0.147981u^2 - 2.071190u^3 + 4.434685u^4 - 2.706056u^5,$$
and for $n \ge 6$ also $a_{n-1}$ by a second polynomial with constants $0.042981, -0.293762, -1.752461, 5.682633, -3.582633$. The middle weights are $a_i = \tilde m_i/\sqrt\phi$, with $\phi$ chosen so that $\sum_i a_i^2 = 1$, and the lower half is the mirror image. The mean and log standard deviation of $t$ are
$$\mu_n = 0.544 - 0.39978n + 0.025054n^2 - 0.0006714n^3, \quad \log\sigma_n = 1.3822 - 0.77857n + 0.062767n^2 - 0.0020322n^3$$
for $4 \le n \le 11$, and, with $v = \log n$,
$$\mu_n = -1.5861 - 0.31082v - 0.083751v^2 + 0.0038915v^3, \quad \log\sigma_n = -0.4803 - 0.082676v + 0.0030302v^2$$
for $n \ge 12$.

## Example

**Eleven measurements.** Take $x = 148, 154, 158, 160, 161, 162, 166, 170, 182, 195, 236$, already sorted. Then $\bar y = 172$ and $SS = 6226$. Line L4 pairs the largest value with the smallest, the second largest with the second smallest, and so on:

| $i$ | $a_{12-i}$ | $y_{12-i} - y_i$ | product |
|---|---|---|---|
| 1 | 0.5600 | 236 − 148 = 88 | 49.2822 |
| 2 | 0.3315 | 195 − 154 = 41 | 13.5914 |
| 3 | 0.2260 | 182 − 158 = 24 | 5.4243 |
| 4 | 0.1433 | 170 − 160 = 10 | 1.4329 |
| 5 | 0.0698 | 166 − 161 = 5 | 0.3488 |

The products use the unrounded weights. Their sum is $b = 70.0797$, and $W = 70.0797^2/6226 = 0.78881$. For $n = 11$, line L7 gives $\gamma = 2.776$, $\log(1 - W) = -1.55502$, $t = -\log(2.776 + 1.55502) = -1.46580$, $\mu_n = -1.71568$ and $\sigma_n = 0.10105$. Line L8 gives $z = 2.4728$, and $p = 0.006704$. The test rejects normality at 1%. The value 236 is far from the others. Without it, $W = 0.9080$ and $p = 0.268$. With all eleven values on the log scale, $W = 0.8362$ and $p = 0.028$: the log removes part of the skewness, but not all.

**Three values, exact.** For $x = 1, 2, 4$, $a = (-\sqrt{1/2}, 0, \sqrt{1/2})$, $b = 3/\sqrt2$, $SS = 14/3$ and $W = 4.5/(14/3) = 27/28 = 0.96429$. Line L6 gives $p = \frac6\pi\left(\arcsin\sqrt{27/28} - \frac\pi3\right) = 0.6369$. The smallest possible value for $n = 3$ is $W = 3/4$, for two equal values and one different value, and there $p = 0$.

## Correctness

Line L4 computes $\sum_i a_i y_i$, because $a_i = -a_{n+1-i}$ lets each pair be written as $a_{n+1-i}(y_{n+1-i} - y_i)$, and the middle term is 0 when $n$ is odd. Because $\sum_i a_i = 0$ and $\sum_i a_i^2 = 1$, $b^2/SS$ is the squared correlation of $y$ and $a$, so $W \le 1$ by the Cauchy-Schwarz inequality, and the minimum in line L5 only removes rounding above 1. $W$ does not change when every $x_i$ becomes $c + dx_i$ with $d \ne 0$: for $d > 0$ the order is kept, and for $d < 0$ the order is reversed and the antisymmetry of $a$ changes only the sign of $b$. So the null law of $W$ does not depend on $\mu$ and $\sigma$. $W$ is at least $na_n^2/(n - 1)$, with equality for $n - 1$ equal values and one different value; the proof reduces this to an inequality on the coefficients, which was checked by computation for every $n$ from 3 to 5000. For $n = 3$ the p-value in line L6 is the exact null distribution, so the size is exactly $\alpha$. This is proved.

Two things are only measured. The approximate coefficients are within $1.5 \times 10^{-3}$ of the exact ones for $n = 4, 5, 6$, computed from the order statistic integrals: for $n = 6$ the exact upper half is $0.6431, 0.2806, 0.0876$, and the approximation gives $0.6430, 0.2807, 0.0883$. The p-value is an approximation: with 20000 seeded normal samples of each size (4000 for $n = 200$), the size of the nominal 5% test was 0.0538 at $n = 4$, 0.0464 at $n = 5$, 0.0511 at $n = 10$, 0.0498 at $n = 20$, 0.0495 at $n = 50$ and 0.0505 at $n = 200$. The correctness proof gives each step.

## Complexity

On a [real RAM](/real-ram/) with $\Phi^{-1}$ and $\Phi$ as unit-cost operations, line L1 takes $\Theta(n\log n)$ comparisons, line L2 $\Theta(n)$ evaluations of $\Phi^{-1}$, and lines L3 to L9 $\Theta(n)$ more. The total is $\Theta(n\log n)$ time and $\Theta(n)$ extra space for the sorted copy and the weights. Computing the exact weights $V^{-1}m$ instead would need $\Theta(n^2)$ numerical integrals and a $\Theta(n^3)$ solve. The original tables stop at $n = 50$, and all later algorithms use approximate weights.

**Numerical stability.** $SS$ is computed in two passes, mean first, which avoids the cancellation of $\sum y_i^2 - n\bar y^2$ when the values are large and close together. When $SS = 0$ the implementation stops with an error, because $W$ is undefined. Rounding can make $b^2/SS$ slightly larger than 1 for data that are exactly on a line, so line L5 clips it. Line L7 uses $\log(1 - W)$ through `log1p(-W)`, which keeps relative accuracy when $W$ is near 1, as it is for large normal samples. Line L9 computes the upper normal tail directly, so very small p-values do not round to 0. For $n \le 11$ the transform needs $\log(1 - W) < \gamma$. The implementation returns $p = 0$ otherwise, but this guard never acts on valid data: $\gamma \ge 0.022$ for $5 \le n \le 11$, and for $n = 4$, $\gamma = -0.437$ would need $W \le 0.354$, below the minimum $0.6298$.

## Properties

- **Invariant.** $W$ does not change under $x \mapsto c + dx$ with $d \ne 0$, so the test needs no estimate of $\mu$ or $\sigma$.
- **Bounded.** $na_n^2/(n - 1) \le W \le 1$. The lower bound is $0.75$ for $n = 3$, $0.6298$ for $n = 4$, $0.5522$ for $n = 5$, $0.4961$ for $n = 6$ and $0.3657$ for $n = 10$ (with the weights of line L2). $W = 1$ only when the sorted sample is exactly a linear function of $a$.
- **Exact for $n = 3$ only.** For $n = 3$ the null density of $W$ is $\frac3\pi\left(w(1 - w)\right)^{-1/2}$ on $[\frac34, 1]$. For larger $n$ both the weights and the p-value are approximations.
- **Close to Shapiro-Francia.** For large $n$, $V^{-1}m$ is close to a multiple of $m$, so $W$ is close to the squared correlation of the sorted sample with $m$, which is the Shapiro-Francia statistic.
- **Not distribution free.** The null law of $W$ is for the normal family only. It cannot be used for another family without new weights and new tables.

## Variants and improvements

- **Shapiro-Francia W'.** Shapiro and Francia (1972) replaced $V^{-1}m$ by $m$ itself, which avoids $V$. Then $W'$ is the squared correlation of a normal [Q-Q plot](/q-q-plot/). Royston's approximation of $W$ uses Blom's scores for the middle weights, so for large $n$ the two statistics are close.
- **D'Agostino-Pearson $K^2$.** It combines the sample skewness and kurtosis, each with a normalizing transform. It tells which moment is wrong, but it has less power against some alternatives.
- **Anderson-Darling and Lilliefors.** The [Anderson-Darling test](/anderson-darling-test/) and the [Kolmogorov-Smirnov test](/kolmogorov-smirnov-test/) compare the empirical distribution function with a normal one. With $\mu$ and $\sigma$ estimated from the data, the plain tables are wrong, and the Lilliefors tables or a [parametric bootstrap](/parametric-bootstrap/) are needed. Anderson-Darling is close to Shapiro-Wilk in power; Kolmogorov-Smirnov has much less power.
- **Algorithm AS 181.** Royston (1982) gave the first algorithm for $n$ up to 2000. AS R94 (1995) replaced it with the approximations used here and extended the range to $3 \le n \le 5000$.
- **Censored samples.** Royston's AS R94 also handles samples where the largest values are censored, by using only the first $n_1$ order statistics.
- **Residuals.** Applied to the residuals of a linear model, for example the [studentized residuals](/studentized-residual/), the test is a common check of the normal error assumption. The null law is then only approximate, because residuals are not independent.

## When to use it

Use the Shapiro-Wilk test when you need a formal check of normality for a sample of moderate size, from about 10 to a few thousand, for example before a procedure whose validity depends on normality in small samples. Always look at a Q-Q plot as well: it shows the kind and the size of the departure, which a p-value does not. For very large samples, judge the size of the departure from the plot and from the effect on the procedure you plan to use, not from the p-value. To test a fully specified distribution, or a family other than the normal, use the [Kolmogorov-Smirnov test](/kolmogorov-smirnov-test/), the Anderson-Darling test or the [chi-squared goodness of fit test](/chi-squared-goodness-of-fit-test/).

## Pitfalls

- **"Not rejected" is not "normal".** At $n = 10$ the test rejects exponential data less than half the time, and uniform data less than one time in ten, as the power figures above show. A large p-value from a small sample says little.
- **Large samples reject small departures.** With thousands of values, a skewness too small to affect a t-test gives a tiny p-value.
- **Testing before choosing the test.** Choosing a t-test or a rank test from the result of a normality test on the same data changes the error rates of the second test.
- **Ties and rounding.** Data rounded to a coarse grid have many ties, which lower $W$ and can make the test reject normal data. Constant data have no $W$ at all.
- **Out of range.** The constants are fitted for $3 \le n \le 5000$. The implementation refuses other $n$.
- **Wrong tail.** Small $W$ is evidence against normality. Values of $W$ near 1 are what normal data give.

## Implementations

## History

Samuel Shapiro and Martin Wilk published the test in Biometrika in 1965. They called it an analysis of variance test, because $W$ compares a generalized least squares estimate of $\sigma^2$ from the ordered sample with the usual estimate. They gave the weights and the percentage points of $W$ for $n$ up to 50, and the exact null distribution for $n = 3$. Because the weights for larger $n$ needed the covariances of normal order statistics, Shapiro and Francia (1972) proposed the simpler $W'$. Patrick Royston extended the test to $n = 2000$ with Algorithm AS 181 in 1982, gave new approximations of the weights and a normalizing transform in 1992, and published Algorithm AS R94 in 1995 with the range $3 \le n \le 5000$. AS R94 is the algorithm behind the Shapiro-Wilk functions in most statistical software.

## References
