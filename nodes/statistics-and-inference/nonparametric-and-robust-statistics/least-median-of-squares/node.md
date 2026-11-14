---
tag: 0GC0T5
kind: algorithm
slug: least-median-of-squares
name: Least median of squares
aliases:
- LMS regression
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: Rousseeuw's regression that minimizes the median of the squared residuals. It has breakdown point 1/2 but converges slowly, at rate n^(-1/3).
model: real-ram
complexity:
  vars: {n: the number of data points (simple regression)}
  time: {worst: O(n^3 log n), best: O(n^3 log n)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact_in_exact_arithmetic: true, regression_equivariant: true, in_place: false, online: false}
history:
  year: 1984
  people: [Peter J. Rousseeuw, J. Michael Steele, William L. Steiger, Diane L. Souvaine, Herbert Edelsbrunner]
  note: Rousseeuw proposed least median of squares in 1984, as a regression with breakdown point near 1/2 in any dimension. Exact algorithms for the line followed in 1986 to 1990.
prereqs: [median, ordinary-least-squares, breakdown-point, linear-regression]
see_also: [least-trimmed-squares, repeated-median-regression, theil-sen-estimator, ransac, minimum-covariance-determinant, mm-estimator, line-arrangement, robust-model-fitting]
sources:
  - paper: doi:10.1080/01621459.1984.10477105
    title: Peter J. Rousseeuw, Least median of squares regression, Journal of the American Statistical Association 79(388), 1984
    locator: pp. 871 to 880 (the definition, the breakdown point, the convergence rate n^(-1/3), and the random subset algorithm)
  - book: isbn:9780471852339
    title: Peter J. Rousseeuw and Annick M. Leroy, Robust Regression and Outlier Detection, Wiley, 1987
    locator: Chapter 3 (the breakdown point of LMS for the coverage h) and Chapter 5 (the PROGRESS algorithm with random subsets and the intercept adjustment)
  - paper: doi:10.1214/aos/1176347498
    title: JeongHoon Kim and David Pollard, Cube root asymptotics, The Annals of Statistics 18(1), 1990
    locator: pp. 191 to 219 (the n^(-1/3) rate and the limit distribution of estimators of this type, with least median of squares as an example)
  - paper: "J. Michael Steele and William L. Steiger, Algorithms and complexity for least median of squares regression, Discrete Applied Mathematics 14(1), 1986, pp. 93 to 100"
    locator: The whole paper (the structure of the LMS objective for a line and an exact algorithm)
  - paper: doi:10.1080/01621459.1987.10478500
    title: Diane L. Souvaine and J. Michael Steele, Time- and space-efficient algorithms for least median of squares regression, Journal of the American Statistical Association 82(399), 1987
    locator: pp. 794 to 801 (the LMS line in O(n^2) time and space, and in O(n^2 log n) time and O(n) space, by the dual line arrangement)
  - paper: "Herbert Edelsbrunner and Diane L. Souvaine, Computing least median of squares regression lines and guided topological sweep, Journal of the American Statistical Association 85(409), 1990, pp. 115 to 119"
    locator: The whole paper (the LMS line in O(n^2) time and O(n) space)
---

Least median of squares (LMS) fits a regression by making the median of the squared residuals as small as possible, where least squares makes their sum small. Rousseeuw (1984) introduced it as the first estimator with a [breakdown point](/breakdown-point/) near 1/2 in any dimension: almost half the data can be replaced before the fit can be carried away. For a line, the fit is the centre of the narrowest strip that holds just over half of the points. The price is statistical: the estimate converges at the slow rate $n^{-1/3}$, so LMS is used to find outliers and to start better estimators, not as a final fit.

## In plain words

Lay a straight band of some width over the scatter plot and slide and tilt it until it covers just over half the points. Make the band as narrow as possible. The centre line of the narrowest band is the LMS line. Points far outside the band do not matter at all, so a large group of bad points cannot pull the line, as long as the good points are the majority.

For a fixed tilt, finding the best band is easy: look at the points along the band direction, sort them, and take the shortest run that covers enough of them. The best tilt is always one where two points touch the same edge of the band, so it is enough to try the tilt through each pair of points.

## The problem

The input is $n \ge 2$ points $(x_i, y_i)$. In the notation $y = X b + e$ with $n$ rows, this is the simple model with $X = [1, x]$. For a line $y = a + s x$, the residuals are $r_i = y_i - a - s x_i$, and the objective is
$$Q(s, a) = \text{the } h\text{-th smallest of } r_1^2, \ldots, r_n^2, \qquad h = \lfloor n/2 \rfloor + 1.$$
The output is a minimizer $(s, a)$ and the value $Q^*$. This $h$ is the "median" of the name, in the version that gives the best breakdown point for a line. For $p$ coefficients, Rousseeuw and Leroy use $h = \lfloor n/2 \rfloor + \lfloor (p+1)/2 \rfloor$.

## The algorithm

The exact algorithm for a line tries every pairwise slope and finds the best intercept for each slope by a scan.

```pseudo id=main
LMS-LINE(x, y)
L1  h ← ⌊n/2⌋ + 1
L2  T ← the slopes (y_j − y_i)/(x_j − x_i) of all pairs with x_i ≠ x_j   ▷ T ← {0} if there is none
L3  for each s in T do
L4      (a, ρ) ← BEST-INTERCEPT(s)
L5      keep (s, a, ρ) if ρ is the smallest so far
L6  return the kept s, a, and the objective ρ²

BEST-INTERCEPT(s)                         ▷ the best a for a fixed slope s
L7  z ← the values y_i − s·x_i, sorted
L8  for i ← 1 to n − h + 1: the width of window i is z[i + h − 1] − z[i]
L9  i* ← a narrowest window;  return ((z[i*] + z[i* + h − 1])/2, its width / 2)
```

**Random subsets for many predictors.** With $p$ coefficients, the same idea gives the PROGRESS algorithm of Rousseeuw and Leroy (1987): draw many random sets of $p$ points, fit the exact line or plane through each, adjust its intercept by BEST-INTERCEPT, and keep the best. The result is an approximation, and the number of draws needed to see one clean set with probability $1 - \alpha$ when a fraction $\varepsilon$ is bad is $\log \alpha / \log(1 - (1 - \varepsilon)^p)$, the same count as for [RANSAC](/ransac/) (see the [RANSAC iteration bound](/ransac-iteration-bound/)).

## Example

Take seven points; points 5, 6 and 7 are bad.

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| $x_i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| $y_i$ | 2 | 4 | 5 | 8 | 30 | 33 | 1 |

Here $h = 4$. For the slope $s = 2$ of points 1 and 2, the values $z_i = y_i - 2x_i$ are $0, 0, -1, 0, 20, 21, -13$. Sorted, they are $-13, -1, 0, 0, 0, 20, 21$, and the windows of four values have widths $13, 1, 20, 21$. The narrowest is $[-1, 0]$, so $a = -1/2$ and the half-width is $1/2$. Some other slopes give:

| slope $s$ | best $a$ | half-width $\rho$ |
|---|---|---|
| 1 | 5/2 | 3/2 |
| 3/2 | 5/4 | 3/4 |
| 2 | −1/2 | 1/2 |
| 5/2 | −3/2 | 1 |
| 3 | −5/2 | 3/2 |

The best over all 21 pairwise slopes is $s = 2$, so the LMS line is $y = -\tfrac12 + 2x$, with $Q^* = 1/4$: points 1 to 4 have residuals $\pm\tfrac12$. Least squares gives $y = 0.43 + 2.857\,x$, tilted by the three bad points. A brute force over all $\binom74 = 35$ sets of four points and their best Chebyshev lines gives the same $Q^*$; the test file checks this.

## Correctness

For a fixed slope, the $h$-th smallest $|r_i|$ is at most $\rho$ exactly when an interval of length $2\rho$ holds $h$ of the values $z_i$, and the shortest such interval is a window of $h$ consecutive sorted values. So BEST-INTERCEPT is exact. For the slope, the best band for a set $S$ of $h$ points has width $f_S(s) = \max_S z_i(s) - \min_S z_i(s)$, which is convex and piecewise linear in $s$, with breakpoints only at slopes of pairs in $S$. It tends to infinity at both ends, unless all points of $S$ share one $x$, so it attains its minimum at a pairwise slope. Taking the minimum over all slopes in $T$ therefore gives the global minimum. The full proofs are below.

## Complexity

- **LMS-LINE as written.** $\binom n2$ slopes, each with a sort: $O(n^3 \log n)$ time. It needs $O(n)$ extra space if the pairs are looped over without storing $T$.
- **Faster exact algorithms for the line.** Steele and Steiger (1986) studied the objective and gave an exact algorithm. Souvaine and Steele (1987) use the dual [line arrangement](/line-arrangement/): $O(n^2)$ time and space, or $O(n^2 \log n)$ time and $O(n)$ space. Edelsbrunner and Souvaine (1990) reach $O(n^2)$ time and $O(n)$ space with a guided topological sweep.
- **Higher dimension.** The exact problem with $p$ coefficients takes about $n^{p+1}$ time by the same kind of enumeration, which is why random subsets are used in practice. Each random subset costs $O(n \log n)$ for the intercept adjustment.

## Properties

- **Breakdown point** $\lfloor n/2 \rfloor / n$ for a line in general position (Rousseeuw 1984; Rousseeuw and Leroy 1987, Chapter 3), in the replacement version $\varepsilon^*_n(T, X)$. Bad points may have any $x$ and $y$; leverage points cannot break it either.
- **Exact fit property.** If at least $\lceil n/2 \rceil + 1$ points lie exactly on one line, the LMS line is that line, whatever the others are: that line has objective 0, and no other line can hold $h$ points, because two lines share at most one point. The test file checks this with 6 of 10 points on a line.
- **Slow convergence.** For clean data with a smooth error density, the LMS estimate converges at the rate $n^{-1/3}$, not $n^{-1/2}$ (Rousseeuw 1984). Kim and Pollard (1990) prove limit theorems for estimators of this kind, with LMS as an example. This rate is cited here, not proved. In practice, LMS has very low efficiency under normal errors.
- **Regression, scale and affine equivariant.** Adding a line to $y$, scaling $y$, or changing the coordinates of $x$ by an affine map changes the fit in the matching way.
- **Not unique, not continuous.** Several lines can tie, and a small change of one point can make the fit jump between two far-apart lines. The objective has many local minima.

## Variants and improvements

- **[Least trimmed squares](/least-trimmed-squares/)** minimizes the sum of the $h$ smallest squared residuals. It has the same breakdown point, converges at the rate $n^{-1/2}$, and has a fast heuristic, FAST-LTS. Rousseeuw and Van Driessen recommend it over LMS.
- **Reweighted least squares.** After LMS, give weight 0 to points whose standardized residual is large (for example above 2.5 in units of a robust scale), and fit least squares to the rest. This recovers efficiency and keeps the breakdown point.
- **MM-estimators.** An [MM-estimator](/mm-estimator/) starts from a high-breakdown fit such as LMS or LTS and improves it by an M-step with a fixed robust scale, reaching high efficiency.
- **Least quantile of squares.** Any $h$ between $n/2$ and $n$ gives a valid estimator, with breakdown point about $(n - h)/n$.
- **Approximation algorithms.** In computational geometry, LMS is the problem of the narrowest slab that holds $h$ points, and there are approximation algorithms with a guaranteed factor.

## When to use it

Use LMS as an exploratory tool and as a starting point: to find which points do not fit the main linear pattern, and to start an iterative estimator. For a line in two variables with fewer than a few thousand points, the exact algorithm is practical. For a final fit, use a reweighted fit, LTS, or an MM-estimator. For a quick robust line with less than 29 percent of bad points, [Theil-Sen](/theil-sen-estimator/) is simpler and more efficient.

## Pitfalls

- **Using LMS as the final fit.** Its $n^{-1/3}$ rate means large sampling error, even with clean data.
- **Too few random subsets.** With PROGRESS, the number of draws must grow quickly with $p$ and with the fraction of bad points; with too few draws the result is just a poor fit, with no warning.
- **Forgetting the intercept adjustment.** The line through $p$ points is rarely the best line with that slope. BEST-INTERCEPT is cheap and lowers the objective.
- **The meaning of median.** With $h = \lceil n/2 \rceil$, as some software uses, the breakdown point is lower by about $1/n$ and the exact fit property needs more points. Say which $h$ you use.
- **Floating point.** The narrowest window compares differences of nearly equal values. Ties between bands are common in rounded data; report them.

## Implementations

## History

Rousseeuw introduced least median of squares in 1984, following Hampel's suggestion to replace the sum in least squares by a median. It was the first regression estimator equivariant under affine changes of $x$ with a breakdown point near 1/2 in every dimension. The book of Rousseeuw and Leroy (1987) made it a standard tool, with the PROGRESS program. Exact algorithms for the line came from computational geometry: Steele and Steiger (1986), Souvaine and Steele (1987), and Edelsbrunner and Souvaine (1990). Kim and Pollard (1990) put its slow rate in the general theory of cube root asymptotics. From the 1990s, least trimmed squares, with FAST-LTS (Rousseeuw and Van Driessen 2006), replaced LMS as the default high breakdown regression.

## References
