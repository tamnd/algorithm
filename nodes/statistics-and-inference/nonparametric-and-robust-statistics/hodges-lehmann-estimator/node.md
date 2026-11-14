---
tag: WF6BA7
kind: algorithm
slug: hodges-lehmann-estimator
name: Hodges-Lehmann estimator
aliases:
- Hodges-Lehmann shift estimator
- median of Walsh averages
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: Estimates a location as the median of all pairwise averages, or a shift as the median of all pairwise differences. It inverts the Wilcoxon test and breaks down at 29 percent.
model: real-ram
complexity:
  vars: {n: "the sample size (m + n for two samples)", N: the number of Walsh averages or differences}
  time: {worst: O(n^3), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true, exact_in_exact_arithmetic: true, in_place: false, online: false}
history:
  year: 1963
  people: [Joseph L. Hodges Jr., Erich L. Lehmann]
  note: Hodges and Lehmann derived location estimators from rank tests in 1963. Monahan published an expected O(n log n) algorithm for the one-sample estimate in 1984.
prereqs: [median, wilcoxon-signed-rank-test, mann-whitney-u-test, quickselect, sorted-matrix-selection, breakdown-point]
see_also: [trimmed-mean, huber-m-estimator, influence-function, theil-sen-estimator, u-statistic, test-interval-duality, sign-test, median-absolute-deviation]
sources:
  - paper: doi:10.1214/aoms/1177704172
    title: J. L. Hodges Jr. and E. L. Lehmann, Estimates of location based on rank tests, The Annals of Mathematical Statistics 34(2), 1963
    locator: pp. 598 to 611 (the estimator from the signed-rank and rank-sum tests, and its asymptotic efficiency)
  - paper: doi:10.1214/aoms/1177728261
    title: J. L. Hodges Jr. and E. L. Lehmann, The efficiency of some nonparametric competitors of the t-test, The Annals of Mathematical Statistics 27(2), 1956
    locator: pp. 324 to 335 (the efficiency 3/pi at the normal and the lower bound 0.864)
  - paper: doi:10.1145/1271.319414
    title: John F. Monahan, Algorithm 616, fast computation of the Hodges-Lehmann location estimator, ACM Transactions on Mathematical Software 10(3), 1984
    locator: pp. 265 to 270 (randomized selection among the Walsh averages in expected O(n log n) time)
  - paper: doi:10.1137/0207013
    title: Donald B. Johnson and Tetsuo Mizoguchi, Selecting the Kth element in X + Y and X1 + X2 + ... + Xm, SIAM Journal on Computing 7(2), 1978
    locator: pp. 147 to 153 (deterministic selection in X + Y in O(n log n) time)
  - book: isbn:9780470129906
    title: Peter J. Huber and Elvezio M. Ronchetti, Robust Statistics, second edition, Wiley, 2009
    locator: Chapter 3 (R-estimators, their influence function and breakdown point)
  - book: isbn:9780470387375
    title: Myles Hollander, Douglas A. Wolfe and Eric Chicken, Nonparametric Statistical Methods, third edition, Wiley, 2014
    locator: Chapter 3 (the one-sample location estimator and its confidence interval) and Chapter 4 (the two-sample shift estimator)
---

The Hodges-Lehmann estimator of location is the median of the $n(n+1)/2$ Walsh averages $(x_i + x_j)/2$ with $i \le j$. The two-sample version estimates a shift as the median of the $mn$ differences $y_j - x_i$. Both come from rank tests: they are the values of the parameter at which the [Wilcoxon signed-rank test](/wilcoxon-signed-rank-test/) or the [Mann-Whitney test](/mann-whitney-u-test/) is most balanced. The estimator has 95.5 percent efficiency at the normal law and breaks down at $1 - 1/\sqrt2 \approx 29.3$ percent contamination. Listing all averages costs $\Theta(n^2)$, but a selection in a sorted matrix finds the median in expected $\Theta(n \log n)$ time.

## In plain words

Take every pair of values in the sample, and also each value with itself, and write down the midpoint of the pair. The estimate is the middle one of all these midpoints. A single wild value spoils only the midpoints that use it, and those are a small share. So the result stays near the bulk of the data. It is close to the mean when the data are clean, and close to the median when they are not.

To find the middle midpoint fast, sort the sample first. Then the midpoints form a table in which each row and each column increases. You can count how many entries of such a table are below a guess in one sweep, and that lets you close in on the middle entry without listing all of them.

## The problem

**One sample.** Input $x_1, \ldots, x_n$. Output
$$\hat\theta_{HL} = \operatorname{med}\Big\{\tfrac{x_i + x_j}{2} : 1 \le i \le j \le n\Big\},$$
the median of $N = n(n+1)/2$ numbers, with the average of the two middle values when $N$ is even.

**Two samples.** Input $x_1, \ldots, x_m$ and $y_1, \ldots, y_n$. Output $\hat\Delta = \operatorname{med}\{y_j - x_i\}$ over the $N = mn$ pairs.

Both are the median of a set $\{a_i + b_j : j \ge L_i\}$ with $a$ and $b$ sorted ascending and $L$ nondecreasing. For one sample, $a = b = $ sorted $x$ and $L_i = i$; the answer is half the median sum. For two samples, $a = $ sorted $(-x)$, $b = $ sorted $y$ and $L_i = 0$. Each row $i$ is nondecreasing in $j$, and each column is nondecreasing in $i$. This is a [sorted matrix](/sorted-matrix-selection/).

## The algorithm

SELECT-SUM finds the $k$-th smallest cell. It keeps, for each row, an active column range $[lo_i, hi_i]$. Every cell left of the range is known to be at most the answer, and every cell right of it is known to be at least the answer. Each round takes a random active cell as pivot $v$, counts the cells $\le v$ and $< v$ in the whole matrix, and moves the bounds past $v$.

```pseudo id=main
SELECT-SUM(a, b, L, k)                     ▷ k-th smallest of a[i] + b[j], j ≥ L[i]
L1  for each row i: lo[i] ← L[i], hi[i] ← n − 1
L2  loop
L3      W ← Σ max(0, hi[i] − lo[i] + 1)                ▷ active cells
L4      pick an active cell (i, j) uniformly at random; v ← a[i] + b[j]
L5      (c≤, le[ ]) ← COUNT(v, ≤); (c<, lt[ ]) ← COUNT(v, <)
L6      if c< ≥ k then for each i: hi[i] ← min(hi[i], lt[i])
L7      else if c≤ ≥ k then return v
L8      else for each i: lo[i] ← max(lo[i], le[i] + 1)

HODGES-LEHMANN(x)
L9  sort x; N ← n(n + 1)/2; k ← ⌈N/2⌉
L10 s1 ← SELECT-SUM(x, x, (0, 1, ..., n − 1), k)
L11 s2 ← s1 if N is odd or COUNT(s1, ≤) ≥ k + 1, else the least cell > s1
L12 return (s1 + s2)/4

COUNT(v, ≤)                                ▷ staircase walk over the rows
L13 j ← n − 1, c ← 0; for i ← 0 to m − 1 do
L14     while j ≥ 0 and a[i] + b[j] > v do j ← j − 1
L15     le[i] ← j                          ▷ last column with a cell ≤ v
L16     c ← c + max(0, j − L[i] + 1)
```

COUNT$(v, <)$ is the same walk with $\ge$ in line L14. The walk is correct because the last column with $a_i + b_j \le v$ can only move left as $i$ grows. The least cell greater than $s_1$ in line L11 is the minimum over the rows of the first cell right of $le[i]$, one more walk.

## Example

Take $x = (3, 7, 1, 20, 4)$, sorted $(1, 3, 4, 7, 20)$. The matrix of sums $x_i + x_j$, $j \ge i$:

| row | sums |
|---|---|
| $i = 0$ ($x = 1$) | 2, 4, 5, 8, 21 |
| $i = 1$ ($x = 3$) | 6, 7, 10, 23 |
| $i = 2$ ($x = 4$) | 8, 11, 24 |
| $i = 3$ ($x = 7$) | 14, 27 |
| $i = 4$ ($x = 20$) | 40 |

$N = 15$ is odd, so $k = 8$. One run of SELECT-SUM:

| round | $W$ | pivot $v$ | $c_<$ | $c_\le$ | action |
|---|---|---|---|---|---|
| 1 | 15 | 2 | 0 | 1 | raise $lo$: the cell 2 is out |
| 2 | 14 | 11 | 8 | 9 | lower $hi$: cells $\ge 11$ are out |
| 3 | 7 | 6 | 3 | 4 | raise $lo$: cells $\le 6$ are out |
| 4 | 4 | 8 | 5 | 7 | raise $lo$: cells $\le 8$ are out |
| 5 | 1 | 10 | 7 | 8 | $c_< < 8 \le c_\le$: return 10 |

So the median sum is 10 and $\hat\theta_{HL} = 5$. The sorted sums are $(2, 4, 5, 6, 7, 8, 8, 10, 11, 14, 21, 23, 24, 27, 40)$, and the 8th is 10, as found. For comparison, the mean is 7, pulled up by the value 20, and the median is 4.

## Correctness

The invariant of the loop: every cell left of the active range of its row is less than the answer $v^*$, and every cell right of it is greater than $v^*$. So every cell with value $v^*$ is active, and the active range is never empty. A round with $c_< \ge k$ shows that $v^* < v$, so every cell $\ge v$ is greater than $v^*$ and can leave on the right. A round with $c_\le < k$ shows $v^* > v$, so every cell $\le v$ can leave on the left. Otherwise $c_< < k \le c_\le$, which means that the $k$-th smallest cell equals $v$. Each round removes at least the pivot, so the loop ends. The full proof is in `proofs/correctness.md`.

## Complexity

- **One round** costs $O(m + n)$: line L3 and the random pick scan the rows, and each COUNT is one staircase walk.
- **Number of rounds.** The pivot is uniform among the $W$ active cells. With probability at least $1/2$ its rank among them is in the middle half, and then at least $W/4$ cells leave. So the expected number of rounds is $O(\log N)$, and the expected time of SELECT-SUM is $O((m + n) \log N) = O(n \log n)$. The worst case removes one cell per round: $O(N (m + n)) = O(n^3)$ for this version. It has probability close to zero, and the deterministic methods below avoid it.
- **Total.** The sort in line L9 takes $\Theta(n \log n)$. So the expected time is $\Theta(n \log n)$, with $\Theta(n)$ extra space for the bounds.
- **Naive method.** List all $N$ averages and select their median with [quickselect](/quickselect/): expected $\Theta(n^2)$ time and $\Theta(n^2)$ space. With a sort it is $\Theta(n^2 \log n)$.
- **Deterministic.** Johnson and Mizoguchi (1978) select in $X + Y$ in $O(n \log n)$ worst-case time, and Frederickson and Johnson select in a sorted matrix in $O(n)$ after the sort; see [sorted matrix selection](/sorted-matrix-selection/).

In exact arithmetic the result is exact: the implementation works with the integer or rational sums and halves once at the end.

## Properties

- **Location and scale equivariant.** $\hat\theta_{HL}(ax + b) = a\,\hat\theta_{HL}(x) + b$, also for $a < 0$, because the set of Walsh averages maps in the same way.
- **Link to the signed-rank test (Tukey's identity).** For differences $d_i = x_i - \theta$ with no zeros and distinct $|d_i|$, the signed-rank statistic is $W^+ = \#\{i \le j : d_i + d_j > 0\}$. *Proof.* A pair with $d_i + d_j > 0$ has its member of larger $|\cdot|$ positive. Assign each such pair to that member. A positive $d_i$ with rank $R_i$ of $|d_i|$ gets exactly the $R_i$ pairs $(i, j)$ with $|d_j| \le |d_i|$, each with a positive sum. So the count is $\sum_{d_i > 0} R_i = W^+$. $\square$ So $W^+(\theta)$ counts the Walsh averages above $\theta$, and $\hat\theta_{HL}$ is the $\theta$ where $W^+$ crosses its null mean $N/2$. Inverting the test the same way gives a [confidence interval](/test-interval-duality/) between two order statistics of the Walsh averages.
- **Breakdown point (proved here).** Let $N = n(n+1)/2$ and
$$m^* = \min\Big\{ m : N - \tfrac{(n-m)(n-m+1)}{2} \ge \lceil N/2 \rceil \Big\}.$$
Then the finite-sample [breakdown point](/breakdown-point/) is $m^*/n$, and it tends to $1 - 1/\sqrt2 \approx 0.2929$.

*Proof.* Replace $m$ points. The Walsh averages of two clean points, $C = (n-m)(n-m+1)/2$ of them, lie in the range $[c_-, c_+]$ of the clean points. The other $N - C$ averages use a replaced point. If $N - C < \lceil N/2 \rceil$, at most $\lceil N/2 \rceil - 1$ averages are outside $[c_-, c_+]$. For odd $N = 2r + 1$ that is at most $r$, so the $(r+1)$-th smallest average has at most $r$ values below it and above it that could leave the range, and it stays in $[c_-, c_+]$. For even $N = 2r$ at most $r - 1$ averages leave, so the $r$-th and $(r+1)$-th smallest stay in the range, and so does their mean. If $N - C \ge \lceil N/2 \rceil$, move the $m$ points to $t$. Each average with a replaced point is at least $(c_- + t)/2$, and there are at least $\lceil N/2 \rceil$ of them, so the upper middle average, and with it the median, tends to infinity. For the limit, $m^*$ is the least $m$ with $(n-m)(n-m+1) \le 2\lfloor N/2 \rfloor$, and $2\lfloor N/2 \rfloor = n^2/2 + O(n)$. So $(1 - m^*/n)^2 \to 1/2$, which gives $m^*/n \to 1 - 1/\sqrt 2$. $\square$

For $n = 5, 10, 20, 100$ the values of $m^*$ are $2, 4, 6, 30$. In the contamination model the same number appears: a Walsh average of two independent draws is clean with probability $(1-\varepsilon)^2$, and the median of their law stays bounded while $(1-\varepsilon)^2 > 1/2$.
- **Efficiency (cited).** At a law $F$ symmetric about $\theta$ with density $f$, the influence function is $(F(x) - 1/2)/\int f^2$ and the asymptotic variance is $1/(12 (\int f^2)^2)$. At the normal this gives $\pi/3$, so the efficiency relative to the mean is $3/\pi \approx 0.955$. Hodges and Lehmann (1956) showed that the efficiency is at least $108/125 = 0.864$ for every symmetric $F$, and it can be infinite for heavy tails.
- **Assumptions.** The one-sample estimator targets the center of a symmetric law. For a skewed law it estimates the pseudo-median, the median of the law of $(X_1 + X_2)/2$, which is neither the mean nor the median.

## Variants and improvements

- **Two-sample shift.** The median of $y_j - x_i$; see above. It inverts the Mann-Whitney test, and it estimates the shift $\Delta$ in the model $G(x) = F(x - \Delta)$.
- **Excluding $i = j$.** Some texts use only $i < j$. The two versions differ by $O(1/n)$ and have the same asymptotics.
- **Deterministic selection.** Use the Johnson and Mizoguchi or the Frederickson and Johnson selection for a guaranteed $O(n \log n)$.
- **Confidence intervals.** The interval with the $C$-th smallest and $C$-th largest Walsh average, with $C$ from the null law of $W^+$, has exact coverage under symmetry. The same selection routine computes both ends.
- **Regression.** The [Theil-Sen estimator](/theil-sen-estimator/) is the analogue for a slope: the median of the pairwise slopes, with the same breakdown point $1 - 1/\sqrt2$.

## When to use it

Use it for a location or a shift when the law is roughly symmetric and may have heavy tails. It is the natural point estimate to report next to a Wilcoxon or Mann-Whitney test. It is more efficient than the median at the normal (0.955 against 0.637) and more robust than the mean. Use the [median](/median/) when more than about 29 percent of the data can be bad, and the [Huber M-estimator](/huber-m-estimator/) when you also want a smooth estimating equation for a regression.

## Pitfalls

- **Listing all averages.** For $n = 10^5$ there are $5 \times 10^9$ Walsh averages. The naive method runs out of memory; the selection method does not.
- **Even $N$.** When $N$ is even, the median is the mean of two cells. The second one is not always equal to the first. Find it with one more count, as in line L11.
- **Halving early.** Halving each sum in floating point before the comparison is harmless, but halving integers with integer division is not. Select on the sums and halve once.
- **The breakdown point is not 1/2.** About 29 percent bad data is enough to carry the estimate away.
- **Ties.** Ties in the data are harmless for the estimate, but the exact null law of the test with ties needs the tie-corrected version.

## Implementations

## History

Hodges and Lehmann (1963) showed how to turn a rank test into an estimator of location or shift, and they derived the median of the Walsh averages from the signed-rank test. Their 1956 paper had already found the efficiency of the Wilcoxon tests relative to the $t$ test: $3/\pi$ at the normal and never below 0.864. Johnson and Mizoguchi (1978) gave an $O(n \log n)$ selection in $X + Y$, and Monahan (1984) published a practical randomized algorithm for the Hodges-Lehmann estimate as ACM Algorithm 616.

## References
