---
tag: VFQ6SW
kind: algorithm
slug: theil-sen-estimator
name: Theil-Sen estimator
aliases:
- Sen's slope estimator
- median of pairwise slopes
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Estimates the slope of a line by the median of the slopes through all pairs of points. It breaks down at about 29 percent and can be computed in O(n log n) time.
model: real-ram
complexity:
  vars: {n: the number of data points}
  time: {expected: O(n log n), worst: O(n^2 log n)}
  space: {extra: O(n)}
properties: {deterministic: false, randomized: true, exact_in_exact_arithmetic: true, regression_equivariant: true, in_place: false, online: false}
history:
  year: 1950
  people: [Henri Theil, Pranab Kumar Sen, Richard Cole, Jeffrey S. Salowe, William L. Steiger, Endre Szemerédi, Jiří Matoušek]
  note: Theil proposed the median of pairwise slopes in 1950 and Sen extended it to tied x values in 1968. Cole, Salowe, Steiger and Szemerédi found an optimal O(n log n) slope selection in 1989.
prereqs: [median, counting-inversions, quickselect, breakdown-point]
see_also: [repeated-median-regression, hodges-lehmann-estimator, kth-smallest-pair-distance, kendall-tau-distance, ordinary-least-squares, least-median-of-squares, parametric-search, tukey-median]
sources:
  - paper: "Henri Theil, A rank-invariant method of linear and polynomial regression analysis, I, II and III, Proceedings of the Koninklijke Nederlandse Akademie van Wetenschappen 53, 1950, pp. 386 to 392, 521 to 525 and 1397 to 1412"
    locator: Part I (the slope as the median of the pairwise slopes)
  - paper: doi:10.1080/01621459.1968.10480934
    title: Pranab Kumar Sen, Estimates of the regression coefficient based on Kendall's tau, Journal of the American Statistical Association 63(324), 1968
    locator: pp. 1379 to 1389 (pairs with tied x, the confidence interval from Kendall's tau, and the asymptotic distribution)
  - paper: "Richard Cole, Jeffrey S. Salowe, William L. Steiger and Endre Szemerédi, Optimal slope selection, SIAM Journal on Computing 18(4), 1989, pp. 792 to 810"
    locator: The whole paper (a deterministic O(n log n) algorithm for the k-th smallest pairwise slope)
  - paper: doi:10.1016/0020-0190(91)90177-J
    title: Jiří Matoušek, Randomized optimal algorithm for slope selection, Information Processing Letters 39(4), 1991
    locator: pp. 183 to 187 (selection by random sampling and inversion counting, O(n log n) expected time)
  - paper: "Michael B. Dillencourt, David M. Mount and Nathan S. Netanyahu, A randomized algorithm for slope selection, International Journal of Computational Geometry and Applications 2(1), 1992, pp. 1 to 27"
    locator: The whole paper (a practical randomized slope selection)
  - book: isbn:9780471852339
    title: Peter J. Rousseeuw and Annick M. Leroy, Robust Regression and Outlier Detection, Wiley, 1987
    locator: Chapter 2 (simple regression, with the Theil-Sen and repeated median slopes and their breakdown points)
---

The Theil-Sen estimator fits a line $y = a + b x$ to points in the plane. The slope $b$ is the median of the slopes of the lines through all pairs of points, and the intercept $a$ is the median of the residuals $y_i - b x_i$. It needs no tuning constant, it is exact for data on a line, and more than a quarter of the points must be bad before it can be carried away: the [breakdown point](/breakdown-point/) is $1 - 1/\sqrt 2 \approx 29.3$ percent. There are $\binom n2$ slopes, but the median can be found in $O(n \log n)$ time, because the number of slopes below a value is an [inversion](/inversion/) count.

## In plain words

Draw a line through each pair of points and write down how steep it is. A wild point spoils only the lines that go through it. Sort all the steepness values and take the middle one as the slope of the fit. Then slide the line up or down until half the points are above it.

To find the middle value we do not need to list all the lines. For a trial slope, tilt the plane so that lines of that slope become flat. Two points whose order changes when the tilt passes from very steep down to the trial slope form a line steeper than the trial slope. Counting such swaps is the classic inversion count, which merge sort does quickly. A few random trial slopes then trap the middle value in a short interval.

## The problem

The input is $n$ points $(x_1, y_1), \ldots, (x_n, y_n)$, at least two with different $x$. For $i < j$ with $x_i \ne x_j$, the slope is $s_{ij} = (y_j - y_i)/(x_j - x_i)$; pairs with $x_i = x_j$ are skipped, as in Sen (1968). Let $N$ be the number of slopes. The output is
$$b = \operatorname{med}\{s_{ij}\}, \qquad a = \operatorname{med}_i (y_i - b x_i),$$
where the median of an even number of values is the mean of the two middle ones. In the [regression notation](/ordinary-least-squares/) $y = X b + e$ with $n$ rows, this is a fit of the simple model with $X = [1, x]$ and coefficient vector $(a, b)$.

## The algorithm

For a value $v$, let $c_<(v)$ and $c_\le(v)$ be the numbers of slopes $< v$ and $\le v$. COUNT$(lo, hi)$ returns the number of slopes in the open interval $(lo, hi)$; then $c_<(v) = $ COUNT$(-\infty, v)$ and $c_\le(v) = N - $ COUNT$(v, +\infty)$. SELECT-SLOPE is the randomized slope selection of Matoušek (1991), with $r = \max(n, 32)$ and $\delta = 2\lfloor\sqrt r\rfloor + 2$.

```pseudo id=main
SELECT-SLOPE(x, y, k)                      ▷ the k-th smallest pairwise slope
L1  lo ← −∞;  hi ← +∞
L2  below ← 0                                   ▷ the number of slopes ≤ lo
L3  inside ← COUNT(lo, hi)                      ▷ the number of slopes in (lo, hi)
L4  while inside > 4r do
L5      S ← r slopes drawn uniformly from those in (lo, hi), sorted
L6      t ← (k − below) · r / inside            ▷ where the k-th slope should fall in S
L7      lo' ← S[⌊t⌋ − δ];  hi' ← S[⌊t⌋ + δ]     ▷ an index outside S keeps lo or hi
L8      if c<(lo') < k ≤ c≤(lo') then return lo';  if c<(hi') < k ≤ c≤(hi') then return hi'
L9      if c≤(lo') < k ≤ c<(hi') then
L10         lo ← lo';  hi ← hi';  below ← c≤(lo');  inside ← c<(hi') − c≤(lo')
L11     ▷ otherwise the sample missed the k-th slope: draw a new sample
L12 C ← the slopes in (lo, hi), listed by the merge sort of COUNT
L13 return the (k − below)-th smallest value of C

COUNT(lo, hi)                              ▷ the number of slopes s with lo < s < hi
L14 list the points by y − lo·x, ties by y − hi·x   ▷ at −∞ order by (x, y), at +∞ by (−x, y)
L15 return the number of inversions of the values y − hi·x in this list, by merge sort

THEIL-SEN(x, y)
L16 N ← COUNT(−∞, +∞)                           ▷ the pairs with x_i ≠ x_j
L17 b ← the median of the N slopes, by SELECT-SLOPE (two calls if N is even)
L18 a ← the median of y_i − b·x_i;  return (b, a)
```

The key fact behind COUNT: for $x_i < x_j$, $(y_j - s x_j) - (y_i - s x_i) = (x_j - x_i)(s_{ij} - s)$. So the order of the two values $y - s x$ changes exactly when $s$ passes $s_{ij}$, and a pair whose order differs at $lo$ and at $hi$ is a pair with $lo < s_{ij} < hi$. Line L5 samples a slope in $(lo, hi)$ by picking a uniform random inversion; a [Fenwick tree](/fenwick-tree/) gives the number of inversions that end at each position and finds the partner of a chosen one, all in $O(n \log n + r \log n)$ time.

## Example

Take six points with one wild value:

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $x_i$ | 1 | 2 | 3 | 4 | 5 | 6 |
| $y_i$ | 2 | 3 | 5 | 6 | 8 | 40 |

The 15 pairwise slopes, sorted, are
$$1,\ 1,\ \tfrac43,\ \tfrac32,\ \tfrac32,\ \tfrac32,\ \tfrac32,\ \tfrac53,\ 2,\ 2,\ \tfrac{38}5,\ \tfrac{37}4,\ \tfrac{35}3,\ 17,\ 32.$$
The five largest are the five slopes through point 6. The median is the 8th value, $b = 5/3$. The residuals $y_i - \tfrac53 x_i$ are $\tfrac13, -\tfrac13, 0, -\tfrac23, -\tfrac13, 30$, with median $a = -1/6$. The fit is $y = -\tfrac16 + \tfrac53 x$, close to the line of the first five points. Least squares gives $y = -9.93 + 5.886\,x$, pulled up by point 6.

**Counting by inversions.** To find $c_<(3/2)$, list the points by $x$ and compute $z_i = y_i - \tfrac32 x_i$:
$$z = \big(\tfrac12,\ 0,\ \tfrac12,\ 0,\ \tfrac12,\ 31\big).$$
The inversions, pairs $i < j$ with $z_i > z_j$, are $(1,2)$, $(1,4)$ and $(3,4)$. So $c_<(3/2) = 3$: the slopes $1, 1, 4/3$. The count $c_\le(3/2) = 7$ adds the four slopes equal to $3/2$. For the 8th slope, Lemma 4 of the proof says that $v = \sigma_8$ exactly when $c_<(v) < 8 \le c_\le(v)$:

| $v$ | $c_<(v)$ | $c_\le(v)$ | is it the 8th slope? |
|---|---|---|---|
| 3/2 | 3 | 7 | no, too small |
| 5/3 | 7 | 8 | yes |
| 2 | 8 | 10 | no, too large |

With $n = 6$ there are only 15 slopes, fewer than $4r = 128$, so the loop of line L4 does not run, and line L12 lists the slopes directly. For $n = 400$ (79 800 slopes) the test file runs the sampling rounds.

## Correctness

COUNT is correct because of the sign identity above: a pair with $x_i < x_j$ is in opposite strict order at $lo$ and at $hi$ exactly when $lo < s_{ij} < hi$. Pairs with equal $x$ keep their order at every $s$, so they are never counted, and pairs tied at $lo$ are listed in their order at $hi$, so they are not counted either. Hence COUNT returns the number of inversions of a sequence, which merge sort computes in $O(n \log n)$ time.

SELECT-SLOPE keeps the invariant $c_\le(lo) < k \le c_<(hi)$, so the $k$-th slope $\sigma_k$ stays in $(lo, hi)$. It returns an end of the interval only after it has checked $c_<(v) < k \le c_\le(v)$, which holds exactly when $v = \sigma_k$. Line L13 picks the $(k - below)$-th slope inside the interval, which is $\sigma_k$. The random sample affects only the running time, never the answer.

**Breakdown point.** Replace $m$ of $n$ points with distinct $x$. The $G = \binom{n-m}2$ slopes among the clean points do not move. A median of numbers of which $G$ are fixed and $B$ are free stays bounded if and only if $B < G$. The $m$ bad points can make $B = \binom n2 - G$ slopes as large as they like at once, by sitting far to the right on a steep parabola. So the least $m$ that breaks the estimator is the least $m$ with $\binom{n-m}2 \le \tfrac12 \binom n2$, and as $n \to \infty$, $(1 - \varepsilon)^2 = 1/2$ gives $\varepsilon^* = 1 - 1/\sqrt 2$. The full proofs are below.

## Complexity

- **COUNT** takes $O(n \log n)$ time and $O(n)$ space.
- **SELECT-SLOPE.** Each round takes $O(n \log n)$ time for a sample of $r = n$ slopes and four counts. A round succeeds with probability at least $7/8$ (the proof uses Chebyshev's inequality), and Matoušek (1991) shows that a successful round leaves $O(C/\sqrt r)$ slopes in the interval in expectation, where $C$ is the number before it. Starting from $C \le n^2/2$, about two successful rounds reach $O(n)$ slopes. So the expected time is $O(n \log n)$. In the worst case, a run of unlucky samples ends in line L12 with all $N$ slopes, which costs $O(n^2 \log n)$ time.
- **Theil-Sen** runs one or two selections and one median, in $O(n \log n)$ expected time.
- **Lower bound.** Slope selection takes $\Omega(n \log n)$ time in the algebraic decision tree model, so these bounds are optimal; Cole and others (1989) call their algorithm optimal in this sense.
- **The direct method** lists the $\binom n2$ slopes and uses [quickselect](/quickselect/): $O(n^2)$ expected time and $O(n^2)$ space. It is simpler and is fast enough for a few thousand points.

## Properties

- **Breakdown point** $\varepsilon^*_n = m^*/n$ with $m^* = \min\{m : 2\binom{n-m}2 \le \binom n2\}$, in the replacement version $\varepsilon^*_n(T, X)$ of the [breakdown point](/breakdown-point/) page, for data with distinct $x$. The values for some $n$ are below; the limit is $1 - 1/\sqrt 2 \approx 0.2929$.

| $n$ | 5 | 10 | 20 | 50 | 100 | 1000 |
|---|---|---|---|---|---|---|
| $m^*$ | 2 | 3 | 6 | 15 | 30 | 293 |

- **Exact fit.** If all points lie on one line, every slope equals its slope, so the fit is the line.
- **Regression equivariant.** Adding $c + d x$ to each $y_i$ adds $d$ to $b$ and $c$ to $a$. Scaling $y$ or $x$ by a nonzero constant scales $b$ in the same way. The test file checks the first rule exactly.
- **Efficiency.** Under normal errors the estimator is almost as precise as least squares. In a simulation with $n = 50$ equally spaced $x$ and 2000 samples of standard normal noise, the variance of the least squares slope was 0.93 of the variance of the Theil-Sen slope. This is a measured value, not a theorem; Sen (1968) gives the asymptotic theory.
- **Distribution free interval.** The slope is the value of $\beta$ at which Kendall's tau between $x$ and $y - \beta x$ is zero. Order statistics of the slopes give a confidence interval for the slope from the null distribution of Kendall's tau (Sen 1968), see [Kendall tau distance](/kendall-tau-distance/).

## Variants and improvements

- **Deterministic optimal selection.** Cole, Salowe, Steiger and Szemerédi (1989) select the $k$-th slope in $O(n \log n)$ worst-case time with [parametric search](/parametric-search/). Katz and Sharir (1993) and Brönnimann and Chazelle (1998) gave simpler deterministic algorithms, with expanders and with cuttings.
- **Other randomized versions.** Dillencourt, Mount and Netanyahu (1992) give a practical randomized algorithm in the same spirit.
- **Repeated median.** Siegel's [repeated median](/repeated-median-regression/) takes, for each point, the median of its slopes to the others, and then the median of these $n$ values. Its breakdown point is 50 percent.
- **Weighted versions.** The [weighted median](/weighted-median/) of the slopes $s_{ij}$ with weights $|x_j - x_i|$ is a rank-based estimator of the slope that gives more weight to pairs far apart in $x$. It is more efficient when the $x$ values are unevenly spread.
- **Hodges-Lehmann analogy.** The [Hodges-Lehmann estimator](/hodges-lehmann-estimator/) of location is the median of pairwise means, the same idea one dimension down. Selecting among pairwise differences is the problem of the [k-th smallest pair distance](/kth-smallest-pair-distance/).
- **Trend tests.** In hydrology and climate data, the slope is reported with the Mann-Kendall trend test as "Sen's slope".

## When to use it

Use Theil-Sen for a straight line in two variables when a minority of the points may be wrong, when the errors may be heavy tailed, or when you do not want to choose a tuning constant. It is a good default for robust trend estimates in time series. With more than about 29 percent bad points use the [repeated median](/repeated-median-regression/) or [least median of squares](/least-median-of-squares/). With many predictors there is no direct analog with the same guarantees; use a robust multiple regression such as the [MM-estimator](/mm-estimator/).

## Pitfalls

- **Tied x values.** Pairs with $x_i = x_j$ have no slope. Skipping them, as Sen does, is standard. Do not put them in as $\pm\infty$; that changes the median.
- **The intercept.** There are several conventions: the median of $y_i - b x_i$ (used here), or $\operatorname{med} y - b \operatorname{med} x$ (Conover). They differ in general. Say which one you use.
- **Even N.** With an even number of slopes, take the mean of the two middle ones, or say that you take the lower one. Libraries differ.
- **Floating-point slopes.** With almost equal $x$ values, the slope is huge and inexact. For exact answers on rational data, compare $y_j - y_i$ against $s (x_j - x_i)$ and do not divide.
- **Breakdown is not 50 percent.** About 29 percent of points with arbitrary $x$ and $y$ can carry the slope away. Bad leverage points are enough.
- **Quadratic memory.** Listing all slopes needs $\binom n2$ values, which is 5 GB of doubles for $n = 36\,000$. The selection method needs $O(n)$ memory.

## Implementations

## History

Theil (1950) proposed the median of the pairwise slopes as a rank-invariant estimate, in a series of three papers. Sen (1968) treated tied $x$ values, linked the estimator to Kendall's tau, and derived its distribution. Rousseeuw and Leroy (1987) put it in the framework of breakdown and computed its breakdown point of 29.3 percent. The computational question, selecting a slope without listing all of them, became a central problem of computational geometry in the 1980s: Cole, Salowe, Steiger and Szemerédi (1989) solved it in optimal $O(n \log n)$ time, and Matoušek (1991) gave a short randomized algorithm based on inversion counting.

## References
