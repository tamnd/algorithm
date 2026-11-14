---
tag: 4F0CN9
kind: algorithm
slug: trimmed-mean
name: Trimmed mean
aliases:
- truncated mean
area: statistics-and-inference/nonparametric-and-robust-statistics
level: intro
summary: The mean of the sample after removing a fixed fraction of the smallest and of the largest values. Its breakdown point is that fraction.
model: real-ram
complexity:
  vars: {n: the sample size, g: the number of values cut from each end}
  time: {worst: Θ(n²), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true, exact_in_exact_arithmetic: true, in_place: false, online: false}
history:
  year: 1963
  people: [John W. Tukey, Donald H. McLaughlin]
  note: Tukey and McLaughlin studied trimmed means and a Winsorized standard error for them in 1963. Stigler found the limit law of the trimmed mean under any distribution in 1973.
prereqs: [order-statistic, quickselect, median, breakdown-point]
see_also: [median-absolute-deviation, influence-function, huber-m-estimator, hodges-lehmann-estimator, least-trimmed-squares, trimmed-icp, sample-variance, student-t-test]
sources:
  - paper: "John W. Tukey and Donald H. McLaughlin, Less vulnerable confidence and significance procedures for location based on a single sample: trimming/Winsorization 1, Sankhyā Series A 25(3), 331 to 352, 1963"
    title: John W. Tukey and Donald H. McLaughlin, Less vulnerable confidence and significance procedures for location based on a single sample, trimming/Winsorization 1, Sankhyā A 25(3), 1963
    locator: pp. 331 to 352 (the trimmed mean and its Winsorized standard error)
  - paper: doi:10.1214/aos/1176342412
    title: Stephen M. Stigler, The asymptotic distribution of the trimmed mean, The Annals of Statistics 1(3), 1973
    locator: pp. 472 to 477 (the limit law of the trimmed mean for any distribution)
  - paper: doi:10.1093/biomet/61.1.165
    title: Karen K. Yuen, The two-sample trimmed t for unequal population variances, Biometrika 61(1), 1974
    locator: pp. 165 to 170 (the trimmed t statistic with the Winsorized variance)
  - book: isbn:9781119214687
    title: Ricardo A. Maronna, R. Douglas Martin, Victor J. Yohai and Matías Salibián-Barrera, Robust Statistics, Theory and Methods (with R), second edition, Wiley, 2019
    locator: Chapter 2 (trimmed means, their variance and their efficiency at the normal)
  - book: isbn:9780470129906
    title: Peter J. Huber and Elvezio M. Ronchetti, Robust Statistics, second edition, Wiley, 2009
    locator: Chapter 3 (L-estimators, the trimmed mean and its influence function)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 9.2 (selection in expected linear time) and Section 9.3 (selection in worst-case linear time)
---

The $\alpha$-trimmed mean drops the $g = \lfloor \alpha n \rfloor$ smallest and the $g$ largest values of a sample and averages the rest. It sits between the mean ($g = 0$) and the [median](/median/) ($g$ as large as possible). With $\alpha$ between 0.1 and 0.25 it keeps most of the efficiency of the mean at the normal law and resists a fraction $\alpha$ of outliers. Two [selections](/quickselect/) find the kept values without a sort, so the cost is expected $\Theta(n)$.

## In plain words

Judges score a performance. The organizers drop the highest score and the lowest score, then take the average of the others. One judge who gives an extreme score, by error or by bias, cannot change the result much. The trimmed mean is this rule with a fixed share of scores dropped at each end. To find the scores to keep, you do not need to put all of them in order. You only need to find the scores at the two cut points.

## The problem

The input is a sample $x_1, \ldots, x_n$ of real numbers and a fraction $0 \le \alpha < 1/2$, or directly an integer $g \ge 0$ with $n - 2g \ge 1$. Let $x_{(1)} \le \cdots \le x_{(n)}$ be the [order statistics](/order-statistic/). The output is
$$\bar x_\alpha = \frac{1}{n - 2g} \sum_{i = g+1}^{n-g} x_{(i)}, \qquad g = \lfloor \alpha n \rfloor.$$

## The algorithm

SELECT$(A, lo, hi, k)$ is [quickselect](/quickselect/) on $A[lo \ldots hi]$ with a random pivot and a three-way partition. It rearranges the range so that $A[k]$ holds the value of rank $k - lo$ in the range, with $A[lo \ldots k-1] \le A[k] \le A[k+1 \ldots hi]$.

```pseudo id=main
TRIMMED-MEAN(x, α)                         ▷ x[0 .. n − 1], 0 ≤ α < 1/2
L1  n ← |x|, g ← ⌊α n⌋ (in exact arithmetic), A ← a copy of x
L2  if n − 2g < 1 then error
L3  SELECT(A, 0, n − 1, g)                  ▷ A[g] = x(g+1)
L4  SELECT(A, g, n − 1, n − g − 1)          ▷ A[n − g − 1] = x(n−g)
L5  s ← A[g] + A[g + 1] + ... + A[n − g − 1]
L6  return s / (n − 2g)
```

Line L3 puts the $g$ smallest values in $A[0 \ldots g-1]$. Line L4 works only on the rest, $A[g \ldots n-1]$, and puts the $g$ largest values at its right end. What is left in the middle is exactly the multiset of kept values, in some order. The order does not matter for a sum.

## Example

Take $x = (12, 7, 3, 95, 5, 8, 6, 1, 10, 4)$ and $\alpha = 0.2$. Then $n = 10$ and $g = 2$.

| step | content of $A$ (one possible order) | what is fixed |
|---|---|---|
| L3, rank 2 in $A[0..9]$ | (3, 1, **4**, 12, 7, 95, 5, 8, 6, 10) | $A[0..1] = \{1, 3\}$, $A[2] = 4$ |
| L4, rank 7 in $A[2..9]$ | (3, 1, 4, 7, 5, 8, 6, **10**, 12, 95) | $A[8..9] = \{12, 95\}$, $A[7] = 10$ |
| L5 | $A[2..7] = (4, 7, 5, 8, 6, 10)$ | sum 40 |

The result is $40/6 = 20/3 \approx 6.667$. The sorted sample is $(1, 3, 4, 5, 6, 7, 8, 10, 12, 95)$, so the kept values are $x_{(3)}, \ldots, x_{(8)}$, as claimed. The mean of the sample is $15.1$, pulled up by the value 95. The median is $6.5$. The exact order inside each part depends on the random pivots.

## Correctness

The key fact: after SELECT on a range with result position $k$, the range is a permutation of its old content, and $A[lo \ldots k-1] \le A[k] \le A[k+1 \ldots hi]$. So if you sort each part, the concatenation is sorted. It follows that $A[lo \ldots k-1]$ holds the $k - lo$ smallest values of the range, as a multiset, even with ties. After L3, $A[0 \ldots g-1]$ is $\{x_{(1)}, \ldots, x_{(g)}\}$ and $A[g \ldots n-1]$ is $\{x_{(g+1)}, \ldots, x_{(n)}\}$. L4 applies the same fact to this range and splits off its $g$ largest values. So $A[g \ldots n-g-1]$ is $\{x_{(g+1)}, \ldots, x_{(n-g)}\}$. The proof, with the correctness of the three-way partition, is in `proofs/correctness.md`.

## Complexity

- **Time.** Each SELECT takes expected $\Theta(m)$ comparisons on a range of $m$ items, and at most $\Theta(m^2)$. The two calls work on $n$ and $n - g$ items, and the sum takes $n - 2g$ additions. So the expected time is $\Theta(n)$ and the worst case is $\Theta(n^2)$. With the [median of medians](/median-of-medians/) pivot rule, SELECT and the whole method take $\Theta(n)$ in the worst case.
- **Space.** $\Theta(n)$ for the copy $A$. If you may change the input, the method runs in place with $O(1)$ extra words.
- **Sorting.** Sorting and summing the middle takes $\Theta(n \log n)$. It is simpler and fast enough for most samples. The selection method matters for large $n$ or for repeated use.

In exact arithmetic (integers or fractions) the result is exact. In floating point the sum in line L5 has the usual rounding error of a sum. Use [Kahan summation](/kahan-summation/) or `math.fsum` for long samples.

## Properties

- **Breakdown point $(g + 1)/n$**, which tends to $\alpha$. The [breakdown point](/breakdown-point/) page proves it: the kept values stay inside the range of the clean points as long as at most $g$ points are replaced.
- **Influence function.** At a law $F$ symmetric about $\mu$ with quantile $q = F^{-1}(1 - \alpha)$, it is $(x - \mu)/(1 - 2\alpha)$ for $|x - \mu| \le q$, and $\pm q/(1 - 2\alpha)$ outside. It is bounded but not redescending (cited, Huber and Ronchetti 2009, Chapter 3).
- **Asymptotic variance.** For symmetric $F$, it is the variance of the $\alpha$-Winsorized law divided by $(1 - 2\alpha)^2$. Stigler (1973) gave the limit law for every $F$; when the cut quantiles are not unique, the limit is not normal.
- **Efficiency at the normal.** A numerical integration gives these efficiencies relative to the mean:

| $\alpha$ | 0.05 | 0.10 | 0.20 | 0.25 |
|---|---|---|---|---|
| efficiency | 0.974 | 0.943 | 0.874 | 0.837 |

At the median end the efficiency tends to $2/\pi \approx 0.637$. For heavy tails, such as a $t$ law with 3 degrees of freedom, the trimmed mean beats the mean by a wide margin.
- **Equivariance.** $\bar x_\alpha$ is location and scale equivariant: $\overline{(a x + b)}_\alpha = a\,\bar x_\alpha + b$ for $a \ne 0$.
- **An L-estimator.** It is a linear combination of order statistics with weights $1/(n-2g)$ in the middle and 0 at the ends.

## Variants and improvements

- **Winsorized mean.** Replace the $g$ smallest values by $x_{(g+1)}$ and the $g$ largest by $x_{(n-g)}$, then average. It has the same breakdown point.
- **Tukey and McLaughlin standard error.** Use $s_w/((1 - 2\alpha)\sqrt n)$, where $s_w^2$ is the sample variance of the Winsorized sample. Yuen's trimmed $t$ test uses it for two samples with unequal variances.
- **Asymmetric trimming.** Cut $g_1$ values at the bottom and $g_2$ at the top. It estimates a different parameter when $F$ is skewed.
- **Interquartile mean.** The case $\alpha = 1/4$.
- **Adaptive trimming.** Choose $\alpha$ from the data, for example from a measure of tail weight.
- **Streaming.** Over a sliding window, keep the window in an [order-statistic tree](/order-statistic-tree/); see the [sliding window median](/sliding-window-median/) for the same structure.

## When to use it

Use a trimmed mean when the data are roughly symmetric but may have a few gross errors or heavy tails, and you want an estimate that is easy to explain. Sports judging, price indices and many lab protocols use it. Use the [median](/median/) if up to half of the data can be bad. Use the [Huber M-estimator](/huber-m-estimator/) if you want a smoother weighting and a better efficiency at the same robustness. Use the plain mean if the data are clean and light-tailed.

## Pitfalls

- **$g = 0$ for small samples.** With $\alpha = 0.1$ and $n \le 9$, $g = 0$, and the trimmed mean is the mean, with breakdown point $1/n$.
- **Rounding of $\alpha n$.** In floating point, $0.29 \times 100 = 28.999999999999996$, so $\lfloor \alpha n \rfloor$ gives 28 and not 29. Compute $g$ in exact arithmetic, or take $g$ as the input.
- **Skewed data.** For a skewed $F$, the trimmed mean estimates neither the mean nor the median of $F$. It estimates its own functional.
- **Standard error.** Do not use $s/\sqrt{n - 2g}$ with the variance of the kept values. It is too small. Use the Winsorized variance.
- **Ties at the cut.** With ties at $x_{(g)} = x_{(g+1)}$, the kept multiset is still well defined. A three-way partition keeps the time linear when many values are equal.

## Implementations

## History

Tukey and McLaughlin (1963) studied trimmed means for small samples and gave a $t$-like statistic with a Winsorized variance. Bickel studied their large-sample behaviour in 1965. Stigler (1973) found the limit law for every distribution and showed that it can fail to be normal when a cut quantile is not unique. Yuen (1974) gave the two-sample trimmed $t$ test.

## References
