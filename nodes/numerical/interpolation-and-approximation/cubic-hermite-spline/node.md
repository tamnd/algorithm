---
tag: 667FMQ
kind: algorithm
slug: cubic-hermite-spline
name: Cubic Hermite spline
aliases:
- Piecewise cubic Hermite interpolation
- cubic Hermite interpolation
- PCHIP
- Ferguson curve
area: numerical/interpolation-and-approximation
level: core
summary: On each interval between knots, the cubic that matches the values and slopes at both ends. The curve is C^1, local, O(1) per point after the interval search, and O(h^4) accurate with exact slopes.
solves: [hermite-interpolation]
model: real-ram
complexity:
  vars: {n: "the number of intervals, with n + 1 knots", h: "the largest interval length"}
  time: {setup: Θ(n), per_point: Θ(log n)}
  space: {extra: Θ(1)}
  flops: {per_point: "24"}
properties: {deterministic: true, recursive: false, local: true, smoothness: C1, exact_on_cubics: true}
history:
  year: 1964
  people: [Charles Hermite, James C. Ferguson, Edwin Catmull, Raphael Rom, Frederick N. Fritsch, Ralph E. Carlson]
  note: The cubic with end values and slopes is the simplest case of Hermite's 1878 interpolation; Ferguson used piecewise cubic curves with end tangents for aircraft design in 1964.
prereqs: [hermite-interpolation, divided-differences]
see_also: [hermite-interpolation, cubic-spline-interpolation, fritsch-carlson-monotone-interpolation, catmull-rom-spline, bicubic-interpolation, lagrange-interpolation, polynomial-interpolation-error-theorem, binary-search]
sources:
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter IV, Piecewise cubic interpolation (piecewise cubic Hermite interpolation, the error bound and the choice of slopes such as Bessel interpolation)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 11, Piecewise polynomial approximation (piecewise cubic Hermite interpolation and its error)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 3.6 (Hermite interpolation) and Section 3.7 (piecewise polynomial interpolation)
  - paper: doi:10.1137/0717021
    title: "F. N. Fritsch and R. E. Carlson, Monotone piecewise cubic interpolation, SIAM Journal on Numerical Analysis 17(2) (1980) 238-246"
    locator: the piecewise cubic Hermite form and conditions on the slopes for a monotone interpolant
  - paper: "James C. Ferguson, Multivariable curve interpolation, Journal of the ACM 11(2) (1964) 221-228"
    locator: parametric piecewise cubic curves with prescribed points and tangent vectors
---

A cubic Hermite spline interpolates data $(x_k, y_k)$ by a separate cubic on each interval $[x_k, x_{k+1}]$, chosen to match the values $y_k, y_{k+1}$ and given slopes $d_k, d_{k+1}$ at the two ends. Neighboring pieces share the value and the slope at each knot, so the curve is $C^1$. Each piece depends only on four numbers, so a change in one data point moves the curve on at most two intervals. With exact slopes the error is at most $h^4 \|f^{(4)}\|_\infty/384$. When the slopes are not known, they are estimated from the data: by three-point formulas (Bessel and Catmull-Rom), or by limiters that preserve monotonicity ([Fritsch and Carlson](/fritsch-carlson-monotone-interpolation/)).

## In plain words

Join data points by a smooth curve, one stretch at a time. For each stretch between two neighboring points you know where the curve starts and ends and in which direction it should leave the first point and arrive at the second. A cubic curve has exactly enough freedom to meet these four requirements, so each stretch is one cubic.

Because neighbors agree on both the position and the direction at every shared point, the whole curve has no corners. Each stretch is built from its own two points only, so editing one point changes only the curve next to it. If you do not know the directions, you can estimate them from nearby points.

## The problem

The input is a list of knots $x_0, \ldots, x_n$ with $n \ge 1$, distinct and in any order, values $y_k$, slopes $d_k$ and a point $t$. The output is $s(t)$, where $s$ is the function that is a cubic on each $[x_k, x_{k+1}]$ (after sorting the knots) with
$$s(x_k) = y_k, \qquad s'(x_k) = d_k, \qquad k = 0, \ldots, n.$$
For $t$ outside $[x_0, x_n]$ the end cubic is extended. This is the piecewise case of [Hermite interpolation](/hermite-interpolation/) with multiplicity 2 at every knot.

Notation on the interpolation and approximation pages: $f$ is a function on $[a, b] = [x_0, x_n]$ with $y_k = f(x_k)$; $s$ is a spline of degree 3 with knots $x_k$; $h_k = x_{k+1} - x_k$ and $h = \max_k h_k$. Costs are arithmetic operations on the [real RAM](/real-ram/).

## The algorithm

On $[x_k, x_{k+1}]$ write $\sigma = (t - x_k)/h_k \in [0, 1]$. The cubic Hermite basis on $[0, 1]$ is
$$h_{00}(\sigma) = (1 + 2\sigma)(1 - \sigma)^2, \quad h_{10}(\sigma) = \sigma(1 - \sigma)^2, \quad h_{01}(\sigma) = \sigma^2(3 - 2\sigma), \quad h_{11}(\sigma) = \sigma^2(\sigma - 1),$$
with $h_{00}(0) = 1$, $h_{01}(1) = 1$, $h_{10}'(0) = 1$, $h_{11}'(1) = 1$ and all other end values and end slopes zero. Then
$$s(t) = h_{00}(\sigma)\, y_k + h_k h_{10}(\sigma)\, d_k + h_{01}(\sigma)\, y_{k+1} + h_k h_{11}(\sigma)\, d_{k+1}.$$
The factor $h_k$ converts slopes in $x$ to slopes in $\sigma$.

```pseudo id=main
HERMITE-SPLINE(x, y, d, t)                ▷ x[0 .. n] increasing, n ≥ 1
L1  k ← the index with x[k] ≤ t < x[k+1], clamped to 0 .. n − 1   ▷ binary search
L2  h ← x[k+1] − x[k]
L3  σ ← (t − x[k]) / h
L4  h00 ← (1 + 2σ)(1 − σ)²;   h10 ← σ(1 − σ)²
L5  h01 ← σ²(3 − 2σ);         h11 ← σ²(σ − 1)
L6  return h00·y[k] + h·h10·d[k] + h01·y[k+1] + h·h11·d[k+1]
```

Unsorted input is sorted once, with the values and slopes, in $O(n \log n)$; the implementation does this.

**Choosing the slopes.** When only values are given:

- *Bessel (three-point) slopes*: $d_k$ is the slope at $x_k$ of the parabola through $x_{k-1}, x_k, x_{k+1}$; at the ends, the parabola through the first or last three points. On a uniform mesh, at interior knots, this is the central difference $(y_{k+1} - y_{k-1})/(2h)$, the slope of the [Catmull-Rom spline](/catmull-rom-spline/).
- *Monotone slopes*: limit the slopes so that $s$ is monotone wherever the data are ([Fritsch and Carlson](/fritsch-carlson-monotone-interpolation/); the PCHIP routine of Fritsch and Butland).
- *Spline slopes*: choose the $d_k$ so that $s''$ is also continuous; this is [cubic spline interpolation](/cubic-spline-interpolation/), which needs a tridiagonal solve and is no longer local.

## Example

Take $f(x) = \sin(\pi x/2)$ at the knots $0, 1, 2$ with exact slopes: $y = (0, 1, 0)$ and $d = (\pi/2, 0, -\pi/2)$. At $t = 0.5$, line L1 gives $k = 0$, then $h = 1$ and $\sigma = 0.5$, and
$$h_{00} = 0.5, \quad h_{10} = 0.125, \quad h_{01} = 0.5, \quad h_{11} = -0.125.$$
So $s(0.5) = 0.5 \cdot 0 + 0.125 \cdot \tfrac{\pi}{2} + 0.5 \cdot 1 - 0.125 \cdot 0 = 0.5 + \pi/16 \approx 0.69635$, against $\sin(\pi/4) \approx 0.70711$. The error $0.0108$ is within the bound $\tfrac{h^4}{384}\max|f^{(4)}| = (\pi/2)^4/384 \approx 0.0159$, and the maximum error on $[0, 1]$, measured on a fine grid, is $0.0108$ as well.

## Correctness

On $[x_k, x_{k+1}]$, line L6 is a cubic in $t$ with value $y_k$ and slope $d_k$ at $x_k$, and value $y_{k+1}$ and slope $d_{k+1}$ at $x_{k+1}$, by the end values of the basis. By the uniqueness of [Hermite interpolation](/hermite-interpolation/), it is the only such cubic. Two neighboring pieces have the same value and slope at their common knot, so $s \in C^1[x_0, x_n]$. If the data come from a cubic polynomial with its exact slopes, each piece is that cubic. The [full proof](proofs/correctness.md) also proves the error bound.

**Error with exact slopes.** If $f \in C^4[x_0, x_n]$ and $d_k = f'(x_k)$, then for $t \in [x_k, x_{k+1}]$
$$|f(t) - s(t)| \le \frac{\|f^{(4)}\|_\infty}{4!}\, (t - x_k)^2 (t - x_{k+1})^2 \le \frac{h_k^4}{384}\, \|f^{(4)}\|_{\infty, [x_k, x_{k+1}]}.$$
This is a proved bound: the Hermite error formula with the nodes $x_k, x_k, x_{k+1}, x_{k+1}$, and $\max (t - x_k)^2(t - x_{k+1})^2 = h_k^4/16$ at the midpoint.

**Error with estimated slopes.** If the slopes have errors $|d_k - f'(x_k)| \le \varepsilon$, the result changes by at most $h_k (|h_{10}| + |h_{11}|)\varepsilon \le \tfrac{8}{27} h_k \varepsilon$, since $\max_{[0,1]} |h_{10}| = \max |h_{11}| = 4/27$. Bessel slopes have $\varepsilon = O(h^2)$ for $f \in C^3$, so the error is $O(h^3)$, one order less than with exact slopes.

| intervals $n$ on $[0, 1]$, $f = e^x$ | 4 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|
| exact slopes, max error | $2.4 \times 10^{-5}$ | $1.6 \times 10^{-6}$ | $1.1 \times 10^{-7}$ | $6.7 \times 10^{-9}$ | $4.2 \times 10^{-10}$ |
| bound $e/(384 n^4)$ | $2.8 \times 10^{-5}$ | $1.7 \times 10^{-6}$ | $1.1 \times 10^{-7}$ | $6.8 \times 10^{-9}$ | $4.2 \times 10^{-10}$ |
| Bessel slopes, max error | $2.2 \times 10^{-3}$ | $3.1 \times 10^{-4}$ | $4.0 \times 10^{-5}$ | $5.2 \times 10^{-6}$ | $6.6 \times 10^{-7}$ |

These are measured on a grid of 5001 points. The exact-slope errors fall by 16 per halving of $h$ and stay just under the bound, which is nearly attained for $e^x$; the Bessel errors fall by about 8, the observed third order, with the largest errors near the ends.

## Complexity

Line L1 is a [binary search](/binary-search/) with about $\log_2 n$ comparisons; when many points are evaluated in increasing order, a moving pointer finds the interval in $O(1)$ amortized time. Lines L2 to L6 take a fixed number of operations: 1 subtraction in L2, 2 operations in L3, 6 in L4 (reusing $(1 - \sigma)^2$), 6 in L5 (reusing $\sigma^2$), and 9 in L6, for 24 in all. Estimating the slopes costs $\Theta(n)$ once. Extra space is $\Theta(1)$ per evaluation.

**Rounding.** The basis values satisfy $0 \le h_{00}, h_{01} \le 1$ and $|h_{10}|, |h_{11}| \le 4/27$ on $[0, 1]$, so no step amplifies errors: the computed value has an error of a small multiple of $u(|y_k| + |y_{k+1}| + h_k(|d_k| + |d_{k+1}|))$. This is observed in the tests rather than proved here. At a knot, $\sigma = 0$ or $\sigma = 1$, and the value $y_k$ is returned exactly.

## Properties

- **Local.** The piece on $[x_k, x_{k+1}]$ depends only on $y_k, y_{k+1}, d_k, d_{k+1}$ (and, with Bessel slopes, on at most four neighboring data points).
- **$C^1$, not $C^2$.** The second derivative jumps at the knots unless the slopes come from a cubic spline.
- **Exact on cubics** with exact slopes, and exact on quadratics with Bessel slopes (the parabola through three points of a quadratic is the quadratic itself).
- **Affine invariant.** Translating or scaling $x$ and $y$ transforms the curve in the same way.
- **Not monotone in general.** Between two increasing data points the cubic can overshoot if the slopes are too large; see [Fritsch and Carlson](/fritsch-carlson-monotone-interpolation/).

## Variants and improvements

- **Catmull-Rom and cardinal splines**: slopes $d_k = (1 - c)(y_{k+1} - y_{k-1})/(x_{k+1} - x_{k-1})$ with a tension $c$; $c = 0$ gives the [Catmull-Rom spline](/catmull-rom-spline/).
- **Monotone variants**: [Fritsch and Carlson](/fritsch-carlson-monotone-interpolation/), PCHIP (Fritsch and Butland 1984, with a weighted harmonic mean of the neighboring secants) and Akima's slopes, which resist wiggles near outliers.
- **Parametric curves**: apply the same formula to each coordinate of points in the plane or in space, with tangent vectors as slopes; these are Ferguson curves, equivalent to cubic Bézier curves with control points $P_k + \tfrac{h}{3} D_k$ and $P_{k+1} - \tfrac{h}{3} D_{k+1}$.
- **Two dimensions**: the tensor product gives [bicubic interpolation](/bicubic-interpolation/), with values, two first derivatives and the cross derivative at each grid point.
- **Higher order**: quintic Hermite splines match values, first and second derivatives, and are $C^2$.

## When to use it

Use a cubic Hermite spline when slopes are known (positions and velocities, ODE solutions with derivatives), when locality matters (interactive editing, streaming data), or when shape must be preserved (with monotone slopes). It is the standard dense output for ODE solvers with derivative information. When only values are known and the data are smooth, a [cubic spline](/cubic-spline-interpolation/) is more accurate for the same knots, $O(h^4)$ instead of $O(h^3)$, and $C^2$.

## Pitfalls

- **Overshoot.** With Bessel or Catmull-Rom slopes, monotone data can give a non-monotone curve, and positive data a negative curve, near steep changes. Use a monotone slope rule when the data must keep their shape.
- **Unsorted or repeated knots.** The interval search needs strictly increasing knots. Sort first, and reject repeated knots.
- **Slopes in the wrong units.** The slopes $d_k$ are derivatives with respect to $x$; forgetting the factor $h_k$ in line L6 gives a wrong curve on any mesh with $h_k \ne 1$.
- **Extrapolation.** Outside $[x_0, x_n]$ the end cubic is extended, and it grows like $t^3$; clamp or use linear extrapolation if values far outside are requested.
- **Expecting $C^2$.** Curvature jumps at the knots are visible in graphics and in derived quantities such as acceleration; use a $C^2$ spline where they matter.

## Implementations

## History

The cubic with prescribed end values and slopes is the simplest case of the interpolation formula Hermite published in 1878. Piecewise cubic curves with prescribed tangents were introduced into computer-aided design by James Ferguson at Boeing (1964), and Catmull and Rom (1974) proposed estimating the tangents from neighboring points in computer graphics. De Boor's book treats the method and its error bounds systematically. Fritsch and Carlson (1980) found conditions on the slopes that make the curve monotone, and with Butland (1984) they produced the PCHIP software that most libraries now use.

## References
