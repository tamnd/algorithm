---
tag: CR12BK
kind: algorithm
slug: piecewise-linear-interpolation
name: Piecewise linear interpolation
aliases:
- Linear interpolation
- Polygonal interpolation
area: numerical/interpolation-and-approximation
level: intro
summary: Join consecutive data points by straight segments. A query costs O(log n) by binary search, the error for f in C^2 is at most h^2/8 max |f''|, and the Lebesgue constant is 1.
solves: [interpolation-problem]
model: real-ram
complexity:
  vars: {n: "the number of intervals, with n + 1 sorted nodes", m: "the number of query points"}
  time: {query: Θ(log n), uniform_grid_query: Θ(1), sorted_queries: Θ(n + m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, exact_on_polynomials: degree 1, shape_preserving: true, local: true}
prereqs: [interpolation-problem, binary-search]
see_also: [nearest-neighbor-interpolation, cubic-spline-interpolation, b-spline, bilinear-interpolation, spline-evaluation, polynomial-interpolation-error-theorem]
sources:
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter III, Piecewise linear approximation (the broken line interpolant, its error bound and the hat function basis)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 11, Piecewise polynomial approximation (linear splines and the error bound h^2/8)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 3, Interpolation theory (the section on piecewise polynomial interpolation)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 18, Interpolation by piecewise polynomials
  - paper: "Erik Meijering, A chronology of interpolation: from ancient astronomy to modern signal and image processing, Proceedings of the IEEE 90(3) (2002) 319-342"
    locator: the sections on ancient and medieval astronomy (linear interpolation in tables)
---

Piecewise linear interpolation joins the consecutive data points $(x_j, y_j)$ and $(x_{j+1}, y_{j+1})$ by straight segments. The result $s$ is the continuous spline of degree 1 with knots at the nodes. It needs no setup, a query costs $\Theta(\log n)$ by [binary search](/binary-search/) for the interval, and the error for $f \in C^2$ is at most $h^2 \max |f''| / 8$ with $h$ the largest spacing. It never overshoots the data, so it is the default when robustness matters more than smoothness.

## In plain words

You have points on a chart and connect each point to the next with a ruler. To read the value at some place, find the two points on either side of it, and take the value on the straight line between them. If the place is a quarter of the way from the left point to the right point, the value is a quarter of the way from the left value to the right value.

This drawing never goes above the highest point or below the lowest one, and it reacts only to the two nearest points. Its corners make it a poor model of smooth curves, but the error shrinks fast: with twice as many points, it drops to about a quarter.

## The problem

Notation on the interpolation pages: $f$ is a function on $[a, b]$, the nodes are $a = x_0 < x_1 < \cdots < x_n = b$, the data are $y_j = f(x_j)$, $h_j = x_{j+1} - x_j$ and $h = \max_j h_j$. The interpolant is the unique function $s$ that is continuous on $[a, b]$, linear on each $[x_j, x_{j+1}]$, and satisfies $s(x_j) = y_j$:
$$s(t) = (1 - \lambda)\, y_j + \lambda\, y_{j+1}, \qquad \lambda = \frac{t - x_j}{x_{j+1} - x_j}, \qquad t \in [x_j, x_{j+1}].$$
In the language of splines, $s$ is the spline of degree 1 with knots $t_j = x_j$, and $s = \sum_j y_j N_j$ where the hat function $N_j$ is 1 at $x_j$, 0 at the other nodes and linear in between (a [B-spline](/b-spline/) of order 2). The input of a query is the sorted nodes, the data and a point $t \in [x_0, x_n]$; the output is $s(t)$.

## The algorithm

```pseudo id=main
PL-INTERPOLATE(x, y, t)          ▷ x[0] < … < x[n], x[0] ≤ t ≤ x[n]
L1  if n = 0 then return y[0]
L2  lo ← 0, hi ← n               ▷ invariant: x[lo] ≤ t ≤ x[hi]
L3  while hi − lo > 1 do
L4      mid ← lo + ⌊(hi − lo) / 2⌋
L5      if x[mid] ≤ t then lo ← mid else hi ← mid
L6  λ ← (t − x[lo]) / (x[lo + 1] − x[lo])
L7  return (1 − λ) · y[lo] + λ · y[lo + 1]
```

Lines L2 to L5 are a binary search for an interval $[x_{lo}, x_{lo+1}]$ that contains $t$. When $t$ is a node, either neighboring interval is fine, because both formulas give the data value there. Line L6 computes the relative position $\lambda \in [0, 1]$, and line L7 forms the convex combination of the two data values. The form of line L7 returns $y_{lo}$ exactly at $\lambda = 0$ and $y_{lo+1}$ exactly at $\lambda = 1$ in floating point.

## Example

The nodes are $0, 1, 3, 4, 6$ with data $0, 2, 3, 1, 4$, so $n = 4$.

| query $t$ | $(lo, hi)$ after each pass of line L5 | interval | $\lambda$ | $s(t)$ |
|---|---|---|---|---|
| 2.5 | (0, 2), (1, 2) | $[1, 3]$ | 0.75 | $0.25 \cdot 2 + 0.75 \cdot 3 = 2.75$ |
| 5 | (2, 4), (3, 4) | $[4, 6]$ | 0.5 | $0.5 \cdot 1 + 0.5 \cdot 4 = 2.5$ |
| 6 | (2, 4), (3, 4) | $[4, 6]$ | 1 | 4 |
| 0 | (0, 2), (0, 1) | $[0, 1]$ | 0 | 0 |

The error bound in practice. For $f$ on a uniform grid with $n$ intervals, the maximum error on a grid of 20001 points and the bound $h^2 \max|f''|/8$ are:

| $n$ | $\sin$ on $[0, \pi]$ | bound | $1/(1 + 25x^2)$ on $[-1, 1]$ | bound |
|---|---|---|---|---|
| 4 | $7.04 \times 10^{-2}$ | $7.71 \times 10^{-2}$ | $1.80 \times 10^{-1}$ | 1.56 |
| 16 | $4.79 \times 10^{-3}$ | $4.82 \times 10^{-3}$ | $5.36 \times 10^{-2}$ | $9.77 \times 10^{-2}$ |
| 64 | $3.01 \times 10^{-4}$ | $3.01 \times 10^{-4}$ | $5.85 \times 10^{-3}$ | $6.10 \times 10^{-3}$ |

For $\sin$ the error falls by 4 when $n$ doubles and the bound is nearly reached. For Runge's function ($\max|f''| = 50$ at $x = 0$) the bound is pessimistic until $h$ resolves the peak; unlike polynomial interpolation at equispaced nodes, the error converges for every continuous $f$.

## Correctness

The binary search keeps the invariant $x[lo] \le t \le x[hi]$ with $lo < hi$, and the gap $hi - lo$ drops at least to $\lceil (hi - lo)/2 \rceil$ in each pass, so it ends with $hi = lo + 1$. Then $t$ lies in $[x_{lo}, x_{lo+1}]$ and line L7 is the linear interpolant of that interval, which is $s(t)$. The full proof, with the error bound, the bound $\|s\|_\infty \le \max_j |y_j|$ and the shape properties, is in the correctness proof below.

**Error bound.** If $f \in C^2[a, b]$, then for every $t \in [a, b]$
$$|f(t) - s(t)| \le \frac{h^2}{8} \max_{[a, b]} |f''|.$$
On $[x_j, x_{j+1}]$, $s$ is the interpolating polynomial of degree 1, so by the [interpolation error theorem](/polynomial-interpolation-error-theorem/) $f(t) - s(t) = \tfrac{1}{2} f''(\xi)(t - x_j)(t - x_{j+1})$, and $|(t - x_j)(t - x_{j+1})| \le h_j^2/4$ with equality at the midpoint. The constant is sharp: for $f(t) = t^2$ the error at each midpoint is exactly $h_j^2/4 = \tfrac{h_j^2}{8} \max|f''|$. With less smoothness: if $f$ is Lipschitz with constant $L$, the error is at most $Lh/2$; if $f$ is only continuous, it is at most the modulus of continuity $\omega_f(h) = \max_{|u - v| \le h} |f(u) - f(v)|$, so $s \to f$ uniformly as $h \to 0$ for every $f \in C[a, b]$.

## Complexity

- **Query.** Each pass of lines L3 to L5 takes $O(1)$ time and the gap $hi - lo$ goes from $n$ to 1 in $\lceil \log_2 n \rceil$ passes, so a query costs $\Theta(\log n)$ in the worst case. Lines L6 and L7 cost 2 subtractions, 1 division, 2 multiplications and 2 more additions or subtractions.
- **Uniform grid.** If $x_j = a + jh$, the index is $j = \min(\lfloor (t - a)/h \rfloor, n - 1)$, found in $O(1)$.
- **Many sorted queries.** For $m$ sorted query points, walk through the intervals and the queries together, as in a merge: $\Theta(n + m)$ in total.
- **Space.** $O(1)$ beyond the data. There is no setup unless the nodes must first be sorted, which costs $O(n \log n)$.

## Properties

- **Local.** $s(t)$ depends only on the two data values of its interval. A change in $y_j$ changes $s$ only on $[x_{j-1}, x_{j+1}]$.
- **Perfectly conditioned.** The hat functions are nonnegative and sum to 1, so $|s(t)| \le \max_j |y_j|$ and the Lebesgue constant is exactly 1. Errors in the data are never amplified.
- **Shape preserving.** Monotone data give a monotone $s$, and convex data (increasing slopes) give a convex $s$.
- **Exact on linear functions.** If $f$ is linear, $s = f$. Quadratics are not reproduced.
- **Minimal energy.** Among all functions $g$ with $g' \in L^2[a, b]$ and $g(x_j) = y_j$, $s$ minimizes $\int_a^b g'(x)^2\,dx$, because $\int (g')^2 = \int (s')^2 + \int (g' - s')^2$ (the cross term vanishes on each interval). The cubic spline is the analogue for $\int (g'')^2$.
- **Only continuous.** $s'$ jumps at the nodes. Derivatives of $s$ are poor estimates of $f'$ near the nodes.

## Variants and improvements

- **Extrapolation.** Outside $[x_0, x_n]$, either extend the end segments or clamp to the end values. Both are choices of the user, not consequences of the data.
- **Several variables.** On a grid, [bilinear interpolation](/bilinear-interpolation/) applies the formula along each axis; on a triangulation, the barycentric coordinates of the triangle that contains the point play the role of $\lambda$.
- **Higher order.** [Cubic Hermite splines](/cubic-hermite-spline/), the [cubic spline](/cubic-spline-interpolation/) and [monotone cubic interpolation](/fritsch-carlson-monotone-interpolation/) give $O(h^4)$ or $O(h^3)$ errors at the cost of a setup or of derivative estimates.
- **Lower order.** [Nearest-neighbor interpolation](/nearest-neighbor-interpolation/) is piecewise constant, with error $O(h)$.
- **Best piecewise linear fit.** If the knots need not be at the data, a least squares fit with fewer knots, or the choice of the knots themselves, gives a better approximation for the same number of pieces.

## When to use it

Use piecewise linear interpolation for tables, lookups in signal processing and graphics, monotone data that must stay monotone, and noisy or rough data where a smooth interpolant would invent wiggles. Its $O(h^2)$ error is enough when the data are dense. For smooth functions sampled sparsely, a cubic spline reaches the same accuracy with far fewer points; for smooth functions where you choose the nodes, [Chebyshev interpolation](/chebyshev-interpolation/) converges much faster still.

## Pitfalls

- **The formula $y_j + \lambda (y_{j+1} - y_j)$.** In floating point it can miss $y_{j+1}$ at $\lambda = 1$: for $y_j = -1000$ and $y_{j+1} = 0.1$ it gives $0.10000000000002274$. Line L7 uses $(1 - \lambda) y_j + \lambda y_{j+1}$, which is exact at both ends.
- **Off-by-one at the right end.** At $t = x_n$ the search of line L5 must return $lo = n - 1$, not $lo = n$; otherwise line L6 reads $x[n+1]$. The invariant $hi - lo \ge 1$ guarantees this. A search with bisect must clamp the index to $n - 1$.
- **Unsorted or repeated nodes.** Binary search needs $x_0 < \cdots < x_n$. A repeated node makes line L6 divide by zero; if a jump is wanted, store it as two separate pieces.
- **Using $s'$ as a derivative.** The slope of $s$ is a first-order estimate of $f'$ inside an interval and is undefined at the nodes.

## Implementations

## History

Linear interpolation in tables is ancient; Meijering's chronology traces its use back to the astronomers of antiquity. In the theory of splines it is the case of degree 1, and it is the first spline space that de Boor's guide treats (Chapter III).

## References
