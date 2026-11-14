---
tag: DYDSMR
kind: algorithm
slug: repeated-median-regression
name: Repeated median regression
aliases:
- Siegel's repeated median
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: 'Siegel''s slope estimate: for each point take the median of its slopes to the others, then the median of those. It is the first regression estimator with breakdown point 1/2.'
model: real-ram
complexity:
  vars: {n: the number of data points}
  time: {expected: O(n log^2 n), worst: O(n^2 log n)}
  space: {extra: O(n)}
properties: {deterministic: false, randomized: true, exact_in_exact_arithmetic: true, regression_equivariant: true, in_place: false, online: false}
history:
  year: 1982
  people: [Andrew F. Siegel, Jiří Matoušek, David M. Mount, Nathan S. Netanyahu, Peter J. Rousseeuw]
  note: Siegel proposed the repeated median in 1982 as the first regression estimator with a 50 percent breakdown point. Matoušek, Mount and Netanyahu computed it in O(n log n) expected time in 1998.
prereqs: [theil-sen-estimator, median, counting-inversions, quickselect, breakdown-point]
see_also: [least-median-of-squares, least-trimmed-squares, hodges-lehmann-estimator, ordinary-least-squares, fenwick-tree, mm-estimator]
sources:
  - paper: doi:10.1093/biomet/69.1.242
    title: Andrew F. Siegel, Robust regression using repeated medians, Biometrika 69(1), 1982
    locator: pp. 242 to 244 (the repeated median slope and intercept, and the breakdown point of 50 percent)
  - paper: doi:10.1007/PL00009190
    title: Jiří Matoušek, David M. Mount and Nathan S. Netanyahu, Efficient randomized algorithms for the repeated median line estimator, Algorithmica 20(2), 1998
    locator: pp. 136 to 150 (a randomized algorithm in O(n log n) expected time and a simpler one in O(n log^2 n))
  - paper: "Peter J. Rousseeuw, Nathan S. Netanyahu and David M. Mount, New statistical and computational results on the repeated median line, in S. Morgenthaler, E. Ronchetti and W. A. Stahel (eds.), New Directions in Statistical Data Analysis and Robustness, Birkhäuser, Basel, 1993, pp. 177 to 194"
    locator: The whole paper (statistical properties of the repeated median line and its computation)
  - book: isbn:9780471852339
    title: Peter J. Rousseeuw and Annick M. Leroy, Robust Regression and Outlier Detection, Wiley, 1987
    locator: Chapter 2 (the repeated median in simple regression, compared with the Theil-Sen slope and least median of squares)
---

Repeated median regression fits a line $y = a + b x$ in two steps of medians. For each data point, take the median of the slopes from it to all the other points. The slope $b$ is the median of these $n$ medians. Siegel (1982) introduced it as the first regression estimator whose [breakdown point](/breakdown-point/) is 50 percent: almost half the points can be replaced before the slope can be carried away. The direct method takes $O(n^2)$ time. This page gives a simple randomized selection in $O(n \log^2 n)$ expected time, built on the inversion counts of the [Theil-Sen estimator](/theil-sen-estimator/).

## In plain words

Each point votes for a slope. To choose its vote, a point looks at the lines from itself to every other point and takes the middle steepness. A good point sees mostly good partners, so its vote is sensible even if many partners are bad. Then we take the middle of all the votes.

A bad point can spoil its own vote and one line for every good point. A good point keeps a sensible vote while fewer than half of its lines are spoiled, so the fit survives almost half bad points. The Theil-Sen estimator pools all the lines in one big vote, and there the bad lines win once about 29 percent of the points are bad.

## The problem

The input is $n$ points $(x_i, y_i)$, at least two with different $x$. For $x_i \ne x_j$, $s_{ij} = (y_j - y_i)/(x_j - x_i)$. Point $i$ has $d_i$ slopes, one for each $j$ with $x_j \ne x_i$. Siegel's estimator is
$$b = \operatorname{med}_i \ \operatorname{med}_{j : x_j \ne x_i} s_{ij}, \qquad a = \operatorname{med}_i (y_i - b x_i).$$
On this page each median of the slope is an order statistic, so that $b$ is always one of the slopes: the inner median is the high median $m_i$, the $(\lfloor d_i/2 \rfloor + 1)$-th smallest of the slopes of $i$, and the outer median is the low median, the $\lceil n'/2 \rceil$-th smallest of the $m_i$ over the $n'$ points with $d_i > 0$. The intercept $a$ is the usual median, with the mean of the two middle values for even $n$. Siegel also defines a repeated median intercept; see the variants.

## The algorithm

For a value $v$ and a point $j$, let $\ell_j(v)$ and $e_j(v)$ be the numbers of slopes of $j$ that are $< v$ and $\le v$. Then $m_j < v$ exactly when $\ell_j(v) \ge k_j$, and $m_j \le v$ exactly when $e_j(v) \ge k_j$. So one pass of per-point inversion counting tells, for every point at once, on which side of $v$ its median lies, without computing the median. The algorithm is randomized [quickselect](/quickselect/) over the implicit list of point medians.

```pseudo id=main
REPEATED-MEDIAN(x, y)
L1  d_j ← the number of slopes of j, for all j    ▷ per-point inversion counts at −∞, +∞
L2  k_j ← ⌊d_j/2⌋ + 1;  K ← ⌈n'/2⌉               ▷ n' = the number of points with d_j > 0
L3  lo ← −∞;  hi ← +∞
L4  A ← the points with d_j > 0                   ▷ the points with lo < m_j < hi
L5  loop
L6      pick i uniformly from A;  v ← m_i, the k_i-th smallest slope of point i
L7      for all j: ℓ_j ← ℓ_j(v), e_j ← e_j(v)     ▷ one merge sort for each count
L8      cl ← #{j : ℓ_j ≥ k_j};  ce ← #{j : e_j ≥ k_j}   ▷ the medians < v and ≤ v
L9      if cl < K ≤ ce then b ← v and leave the loop
L10     if K ≤ cl then hi ← v else lo ← v
L11     A ← the points j of A with lo < m_j < hi       ▷ from the counts saved at lo and hi
L12 a ← the median of y_j − b·x_j
L13 return (b, a)
```

**Per-point counts.** As on the Theil-Sen page, list the points by $y - lo \cdot x$ and count the inversions of the values $y - hi \cdot x$; the inversions are the pairs with $lo < s_{ij} < hi$. During the merge sort, when a right item is output, the left items still waiting are larger, and when a left item is output, the right items already out are smaller. Adding these numbers to the items gives every point its own count in $O(n \log n)$ time. Then $\ell_j(v)$ is the count of $j$ for $(-\infty, v)$, and $e_j(v) = d_j$ minus the count for $(v, +\infty)$.

## Example

Take the data of the Theil-Sen page, with one wild value:

| $j$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $x_j$ | 1 | 2 | 3 | 4 | 5 | 6 |
| $y_j$ | 2 | 3 | 5 | 6 | 8 | 40 |
| slopes of $j$, sorted | 1, 4/3, 3/2, 3/2, 38/5 | 1, 3/2, 5/3, 2, 37/4 | 1, 3/2, 3/2, 2, 35/3 | 1, 4/3, 3/2, 2, 17 | 3/2, 3/2, 5/3, 2, 32 | 38/5, 37/4, 35/3, 17, 32 |
| $m_j$ (3rd of 5) | 3/2 | 5/3 | 3/2 | 3/2 | 5/3 | 35/3 |

Each point has $d_j = 5$ slopes and $k_j = 3$. The wild point 6 has a wild median, but it is one vote of six. With $K = 3$, the sorted medians $3/2, 3/2, 3/2, 5/3, 5/3, 35/3$ give $b = 3/2$. The residuals $y_j - \tfrac32 x_j$ are $\tfrac12, 0, \tfrac12, 0, \tfrac12, 31$, so $a = \tfrac12$. The fit is $y = \tfrac12 + \tfrac32 x$. Theil-Sen gives $y = -\tfrac16 + \tfrac53 x$, and least squares $y = -9.93 + 5.886\,x$.

**A run of the selection.** Suppose line L6 picks point 2, so $v = 5/3$. The medians below $5/3$ are those of points 1, 3, 4, so $cl = 3$; with points 2 and 5, $ce = 5$. Since $K = 3 \le cl$, line L10 sets $hi = 5/3$, and $A$ becomes $\{1, 3, 4\}$. Next, line L6 picks point 4, so $v = 3/2$, with $cl = 0$ and $ce = 3$. Now $0 < 3 \le 3$, and $b = 3/2$.

## Correctness

The per-point counts are right because a pair $\{i, j\}$ is an inversion exactly when its slope is in the open interval, and the merge sort charges each inversion once to each of its two points. The loop keeps the invariant $\#\{m_j \le lo\} < K \le \#\{m_j < hi\}$, so the answer $b$ is always the median of some point of $A$, and $v$ is returned only when $\#\{m_j < v\} < K \le \#\{m_j \le v\}$, which holds exactly when $v = b$. Each round that does not return removes at least the pivot point from $A$, so the loop ends.

**Breakdown point.** For clean data with distinct $x$, the breakdown point in the replacement sense is $\varepsilon^*_n = \lfloor n/2 \rfloor / n$. With $m = \lfloor n/2 \rfloor$ bad points far to the right on a steep parabola, every point has at least half of its slopes huge, so every high median is huge. With fewer bad points, each good point has fewer free slopes than its median needs, so its median stays within the range of the clean slopes; more than half the medians are such, so $b$ stays there too. The full proofs are below.

## Complexity

- **One round** sorts the slopes of one point and runs three merge sorts: $O(n \log n)$ time and $O(n)$ space.
- **Number of rounds.** The pivot is the median of a random active point, so this is quickselect on the $n'$ medians: $O(\log n)$ rounds in expectation, at most $n'$ in the worst case.
- **Total.** $O(n \log^2 n)$ expected time and $O(n)$ space. The worst case is $O(n^2 \log n)$, and the answer is always exact.
- **Faster algorithms.** Matoušek, Mount and Netanyahu (1998) give a randomized algorithm in $O(n \log n)$ expected time. It keeps an interval of slopes and samples slopes inside it, as Matoušek's slope selection does, and tracks for each point how many of its slopes lie below, inside and above. Their paper also gives a simpler algorithm in $O(n \log^2 n)$ time.
- **The direct method** computes each point's median by quickselect: $O(n^2)$ time and $O(n)$ space. For a few thousand points this is fast enough.

## Properties

- **Breakdown point** $\lfloor n/2 \rfloor / n$, the most a regression equivariant estimator can have, up to rounding. The values are $2/5$, $5/10$, $50/100$, $500/1000$ for $n = 5, 10, 100, 1000$; compare $2/5$, $3/10$, $30/100$, $293/1000$ for Theil-Sen.
- **Exact fit.** If all points lie on one line, every slope equals its slope, and so does $b$.
- **Regression equivariant.** Adding $c + d x$ to $y$ adds $d$ to $b$ and $c$ to $a$.
- **Not affine equivariant in x and y together.** The fit depends on which variable is called $y$; this is true of all the slope methods on these pages.
- **Efficiency.** In a simulation with $n = 50$ equally spaced $x$ and 2000 samples of standard normal noise, the variance of the least squares slope was 0.73 of the variance of the repeated median slope. Theil-Sen gave 0.93 in the same setting. These are measured values, not theorems. The repeated median buys its higher breakdown with some efficiency.

## Variants and improvements

- **Repeated median intercept.** Siegel (1982) also defines $a = \operatorname{med}_i \operatorname{med}_{j \ne i} (x_j y_i - x_i y_j)/(x_j - x_i)$, the repeated median of the intercepts of the pairwise lines. It is also robust; the median of the residuals used here is simpler.
- **Several predictors.** Siegel's definition extends to a model with $q$ coefficients: compute the exact fit through each $q$-subset of points, then take $q$ nested medians over the indices. The breakdown point stays near 1/2, but the cost grows like $n^q$.
- **Averaged medians.** Siegel uses the usual median, with the mean of the two middle values. Then $b$ need not be a slope, and the selection above does not apply directly; the direct method is easy.
- **Online and moving windows.** For time series, the repeated median over a sliding window gives a robust trend filter, updated in $O(n)$ time per step by keeping the slopes in sorted order.

## When to use it

Use the repeated median for a robust line in two variables when up to half the points may be wrong, and when you want a fit with a closed form, no random search and no tuning constant. It is a good start for an iterative method, such as an [MM-estimator](/mm-estimator/) step. If at most a quarter of the points may be bad, [Theil-Sen](/theil-sen-estimator/) is more efficient. For a fit that also gives an outlier map, [least trimmed squares](/least-trimmed-squares/) is the common choice.

## Pitfalls

- **Median conventions.** Libraries differ in the inner and outer medians: mean of the middle pair, low median, or high median. The breakdown point is the same, but the answers differ on small samples. Say which one you use.
- **Tied x values.** Pairs with $x_i = x_j$ have no slope. A point whose $x$ is shared by all others has no slopes; leave it out of the outer median.
- **Bounded is not unbiased.** Below the breakdown point the slope stays in the range of the clean slopes, but almost half bad points can still move it far inside that range. A high breakdown point is a guarantee against disaster, not a promise of a good fit.
- **Quadratic memory.** Storing all slopes is not needed; compute the slopes of one point at a time.

## Implementations

## History

Andrew Siegel published the repeated median in Biometrika in 1982. It answered the question, raised by the work of Hampel and others on breakdown, whether a regression estimator can resist almost half of the data being bad. Rousseeuw and Leroy (1987) placed it next to least median of squares, the other early estimator with a 50 percent breakdown point. The question of computing it fast was studied in computational geometry: Stein and Werman gave an $O(n \log^2 n)$ deterministic algorithm in 1992, and Matoušek, Mount and Netanyahu (1998) an $O(n \log n)$ expected time algorithm.

## References
