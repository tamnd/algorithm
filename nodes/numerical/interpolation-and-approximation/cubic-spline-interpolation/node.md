---
tag: 1BZ0EX
kind: algorithm
slug: cubic-spline-interpolation
name: Cubic spline interpolation
aliases:
- Clamped cubic spline
- spline interpolation
- interpolating cubic spline
area: numerical/interpolation-and-approximation
level: core
summary: The C^2 piecewise cubic through the data, found from its second derivatives at the knots by one tridiagonal solve in O(n). The clamped spline has error at most (5/384) h^4 max|f''''|.
solves: [interpolation-problem]
model: real-ram
complexity:
  vars: {n: "the number of intervals, with n + 1 knots", h: "the largest interval length"}
  time: {setup: Θ(n), per_point: Θ(log n)}
  space: {extra: Θ(n)}
  flops: {setup: "15n", per_point: "24"}
properties: {deterministic: true, recursive: false, local: false, smoothness: C2}
history:
  year: 1946
  people: [Isaac J. Schoenberg, John C. Holladay, Charles A. Hall, W. Weston Meyer, Carl de Boor]
  note: Schoenberg named and studied splines in 1946; Holladay proved the minimum curvature property in 1957; Hall and Meyer found the sharp error constants in 1976.
prereqs: [cubic-hermite-spline, thomas-algorithm, interpolation-problem]
see_also: [b-spline, de-boor-algorithm, smoothing-spline, spline, diagonally-dominant-matrix, bicubic-interpolation, polynomial-interpolation-error-theorem, runge-phenomenon]
sources:
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter IV, Piecewise cubic interpolation (cubic spline interpolation and its end conditions, including not-a-knot) and Chapter V (best approximation property and error of complete cubic spline interpolation)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 11, Piecewise polynomial approximation (cubic splines, the minimum property and error bounds)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 3.7, Piecewise polynomial interpolation (the tridiagonal system for the second derivatives and the end conditions)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 9, the section on tridiagonal matrices (Gaussian elimination without pivoting on diagonally dominant tridiagonal systems)
  - paper: "I. J. Schoenberg, Contributions to the problem of approximation of equidistant data by analytic functions, Quarterly of Applied Mathematics 4 (1946) 45-99 and 112-141"
    locator: Part A, the definition of splines and the name
  - paper: "J. C. Holladay, A smoothest curve approximation, Mathematical Tables and Other Aids to Computation 11 (1957) 233-243"
    locator: the natural cubic spline minimizes the integral of the squared second derivative
  - paper: "C. A. Hall and W. W. Meyer, Optimal error bounds for cubic spline interpolation, Journal of Approximation Theory 16 (1976) 105-122"
    locator: the sharp constants 5/384, 1/24 and 3/8 for the clamped spline
---

Cubic spline interpolation joins data $(x_k, y_k)$ by a cubic on each interval $[x_k, x_{k+1}]$ such that the value, the slope and the second derivative are continuous at every knot. That leaves two free conditions, fixed at the ends: zero second derivatives (the *natural* spline) or given end slopes (the *clamped* or complete spline). The unknown second derivatives $M_k = s''(x_k)$ satisfy a strictly diagonally dominant tridiagonal system, which the [Thomas algorithm](/thomas-algorithm/) solves stably in $O(n)$ without pivoting. Unlike a single high-degree polynomial, the spline never shows the [Runge phenomenon](/runge-phenomenon/): for $f \in C^4$ the clamped spline has error at most $\frac{5}{384} h^4 \|f^{(4)}\|_\infty$.

## In plain words

Bend a thin flexible strip so it passes through pegs on a board. The strip takes the smoothest shape it can: no corners, and no sudden change in how sharply it bends. Between two pegs its shape is very close to a cubic curve.

Cubic spline interpolation computes that shape. It uses one cubic per gap between neighboring points, and makes neighbors agree in height, in direction and in bending at every shared point. These matching rules link all the gaps together, so the curve is found by solving one system of equations. The system is simple: each equation involves only three neighboring unknowns, so it is solved in one sweep forward and one sweep back. You also choose what happens at the two ends: either the strip is left straight there, or you fix its direction.

## The problem

The input is knots $x_0, \ldots, x_n$ with $n \ge 1$, distinct and in any order, values $y_k$, a point $t$, and optionally two end slopes $d_a, d_b$. Sort the knots with their values. The output is $s(t)$, where $s \in C^2[x_0, x_n]$ is a cubic on each $[x_k, x_{k+1}]$ with $s(x_k) = y_k$ for all $k$ and

- natural end conditions $s''(x_0) = s''(x_n) = 0$ if no slopes are given, or
- clamped end conditions $s'(x_0) = d_a$, $s'(x_n) = d_b$ otherwise.

For $t$ outside $[x_0, x_n]$ the end cubic is extended. Both problems have exactly one solution (see Correctness).

Notation on the interpolation and approximation pages: $f$ is a function on $[a, b] = [x_0, x_n]$ with $y_k = f(x_k)$; $s$ is a spline of degree 3 with knots $x_k$; $h_k = x_{k+1} - x_k$, $h = \max_k h_k$, and $\delta_k = (y_{k+1} - y_k)/h_k$. Costs are arithmetic operations on the [real RAM](/real-ram/).

## The algorithm

Since $s''$ is linear on each interval, it is fixed by the moments $M_k = s''(x_k)$. Integrating twice and imposing $s(x_k) = y_k$, $s(x_{k+1}) = y_{k+1}$ gives, with $a = x_{k+1} - t$ and $b = t - x_k$,
$$s(t) = \frac{M_k a^3 + M_{k+1} b^3}{6 h_k} + \Big(\frac{y_k}{h_k} - \frac{M_k h_k}{6}\Big) a + \Big(\frac{y_{k+1}}{h_k} - \frac{M_{k+1} h_k}{6}\Big) b \qquad (x_k \le t \le x_{k+1}).$$
This is $C^2$ with the right values for any $M$. Continuity of $s'$ at the interior knots gives
$$h_{k-1} M_{k-1} + 2(h_{k-1} + h_k) M_k + h_k M_{k+1} = 6(\delta_k - \delta_{k-1}), \qquad k = 1, \ldots, n - 1.$$
The natural spline adds $M_0 = M_n = 0$. The clamped spline adds $2h_0 M_0 + h_0 M_1 = 6(\delta_0 - d_a)$ and $h_{n-1} M_{n-1} + 2 h_{n-1} M_n = 6(d_b - \delta_{n-1})$.

```pseudo id=main
CUBIC-SPLINE(x, y, t, da, db)          ▷ x[0 .. n] increasing, n ≥ 1; da, db optional
L1  for k ← 0 to n − 1: h[k] ← x[k+1] − x[k];  δ[k] ← (y[k+1] − y[k]) / h[k]
L2  set rows 0 and n of the tridiagonal system to M[0] = 0 and M[n] = 0
L3  for k ← 1 to n − 1: row k ← (h[k−1], 2(h[k−1] + h[k]), h[k] | 6(δ[k] − δ[k−1]))
L4  if da, db given: row 0 ← (2h[0], h[0] | 6(δ[0] − da));  row n ← (h[n−1], 2h[n−1] | 6(db − δ[n−1]))
L5  M ← solve the tridiagonal system by forward elimination and back substitution
L6  k ← the index with x[k] ≤ t < x[k+1], clamped to 0 .. n − 1   ▷ binary search
L7  hk ← x[k+1] − x[k];  a ← x[k+1] − t;  b ← t − x[k]
L8  cubic ← (M[k]·a³ + M[k+1]·b³) / (6·hk)
L9  return cubic + (y[k]/hk − M[k]·hk/6)·a + (y[k+1]/hk − M[k+1]·hk/6)·b
```

Lines L1 to L5 are the setup, done once; lines L6 to L9 evaluate at one point. Unsorted knots are sorted once with their values; the implementation does this and rejects repeated knots.

## Example

Take the knots $0, 1, 2$ with values $0, 1, 0$, so $h_0 = h_1 = 1$ and $\delta_0 = 1$, $\delta_1 = -1$.

*Natural.* The one interior equation is $M_0 + 4M_1 + M_2 = 6(-1 - 1) = -12$ with $M_0 = M_2 = 0$, so $M_1 = -3$. At $t = 1/2$, $a = b = 1/2$:
$$s(1/2) = \frac{-3 \cdot 1/8}{6} + 0 \cdot \tfrac12 + \Big(1 + \tfrac12\Big) \cdot \tfrac12 = -\tfrac{1}{16} + \tfrac34 = \tfrac{11}{16} = 0.6875.$$

*Clamped.* The data are $\sin(\pi x/2)$, so take $d_a = \pi/2$, $d_b = -\pi/2$. The system is
$$2M_0 + M_1 = 6 - 3\pi, \qquad M_0 + 4M_1 + M_2 = -12, \qquad M_1 + 2M_2 = 6 - 3\pi.$$
By symmetry $M_0 = M_2$, and then $M_1 = \pi - 6 \approx -2.858$ and $M_0 = 6 - 2\pi \approx -0.283$ (the true values of $f''$ are $0$ and $-\pi^2/4 \approx -2.467$). The formula gives $s(1/2) = 1/2 + \pi/16 \approx 0.69635$, against $\sin(\pi/4) \approx 0.70711$. Here $s'(1) = 0$ by symmetry, so this clamped spline equals the [cubic Hermite spline](/cubic-hermite-spline/) with exact slopes.

**Convergence for $f = e^x$ on $[0, 1]$** with $n$ equal intervals, maximum error on a fine grid (computed in double precision):

| $n$ | clamped, exact end slopes | bound $\frac{5}{384} h^4 e$ | natural, whole interval | natural, on $[0.25, 0.75]$ |
|---|---|---|---|---|
| 4 | 2.64e-5 | 1.38e-4 | 8.22e-3 | 2.07e-3 |
| 8 | 1.69e-6 | 8.64e-6 | 2.08e-3 | 1.48e-4 |
| 16 | 1.07e-7 | 5.40e-7 | 5.21e-4 | 2.61e-6 |
| 32 | 6.72e-9 | 3.38e-8 | 1.30e-4 | 5.88e-9 |
| 64 | 4.21e-10 | 2.11e-9 | 3.26e-5 | 3.26e-10 |

The clamped error drops by 16 per halving of $h$ and stays below the bound. The natural spline imposes $s'' = 0$ where $f'' = e^x \ne 0$, which costs two orders: the error drops only by 4 per halving and is largest at the ends. Away from the ends the effect dies out, and on $[0.25, 0.75]$ the natural spline is again fourth order once $n \ge 32$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The steps are these.

1. *Any moments give a $C^2$ interpolant of the values.* On each interval the formula is a cubic whose second derivative is $(M_k a + M_{k+1} b)/h_k$, which is linear with the values $M_k$ and $M_{k+1}$ at the ends, so $s''$ is continuous. At $t = x_k$ ($b = 0$, $a = h_k$) the formula gives $y_k$, and at $t = x_{k+1}$ it gives $y_{k+1}$.
2. *Continuity of $s'$ is the tridiagonal system.* Differentiating, the slope of piece $k$ at $x_{k+1}$ is $\delta_k + h_k(M_k + 2M_{k+1})/6$ and the slope of piece $k + 1$ at $x_{k+1}$ is $\delta_{k+1} - h_{k+1}(2M_{k+1} + M_{k+2})/6$. Equating them gives row $k + 1$ of line L3. The clamped rows are the same slope formulas at $x_0$ and $x_n$ set equal to $d_a$ and $d_b$.
3. *The system has exactly one solution.* Each row is strictly diagonally dominant: $2(h_{k-1} + h_k) > h_{k-1} + h_k$, $2h_0 > h_0$, and the natural rows are identity rows. A strictly diagonally dominant matrix is nonsingular, so the spline exists and is unique.
4. *Elimination without pivoting succeeds.* Forward elimination on a strictly diagonally dominant tridiagonal matrix keeps every pivot nonzero, and keeps it larger in magnitude than its off-diagonal neighbor in the same row (proved by induction in the proof file).
5. *Evaluation.* Line L6 finds the interval containing $t$, and L7 to L9 evaluate the formula of the algorithm section.

**Error bounds (proved, Hall and Meyer 1976).** If $f \in C^4[a, b]$ and $s$ is the clamped spline with $d_a = f'(a)$, $d_b = f'(b)$, then for any mesh
$$\|f - s\|_\infty \le \tfrac{5}{384} h^4 \|f^{(4)}\|_\infty, \qquad \|f' - s'\|_\infty \le \tfrac{1}{24} h^3 \|f^{(4)}\|_\infty, \qquad \|f'' - s''\|_\infty \le \tfrac{3}{8} h^2 \|f^{(4)}\|_\infty,$$
and the constants cannot be lowered. The first bound is due to Hall (1968). For comparison, the [cubic Hermite spline](/cubic-hermite-spline/) with exact slopes at every knot has the constant $1/384$; the spline pays a factor 5 for not being given the interior slopes. For the natural spline the error is $O(h^2)$ when $f''(a)$ or $f''(b)$ is nonzero, and $O(h^4)$ at a fixed distance from the ends; the table above shows both (observed, and in agreement with the decay argument under Properties).

**Minimum curvature (proved, Holladay 1957).** Among all functions $g$ with $g''$ square integrable and $g(x_k) = y_k$ for all $k$, the natural spline uniquely minimizes $\int_a^b g''(x)^2\,dx$. Among those that also have $g'(a) = d_a$, $g'(b) = d_b$, the clamped spline does. The proof: with $e = g - s$, integrating $\int s'' e''$ by parts on each interval leaves only boundary terms and terms $s'''\,e$ at the knots, which all vanish, so $\int g''^2 = \int s''^2 + \int e''^2$.

## Complexity

**Setup, $\Theta(n)$ time and space.** Line L1 costs $3n$ operations (two subtractions and one division per interval). Line L3 costs about $4n$ (one addition, two multiplications and one subtraction per row). Forward elimination costs $5n$ (one division, two multiplications and two subtractions per row) and back substitution $3n$. The total is about $15n$ operations, with $5n$ divisions among them.

**Evaluation, 24 operations plus the search.** Line L6 is a [binary search](/binary-search/) with about $\log_2 n$ comparisons, or $O(1)$ amortized when the points come in increasing order. Line L7 costs 3 subtractions, L8 costs 9 operations and L9 costs 12, for 24.

**Rounding.** Divide each interior row by $h_{k-1} + h_k$ and each clamped end row by $h_0$ or $h_{n-1}$. The scaled matrix $A$ has diagonal entries 2 (or 1 in natural rows) and off-diagonal row sums at most 1, so $\|A\|_\infty \le 3$ and $\|A^{-1}\|_\infty \le 1$, whatever the mesh. The system is well conditioned, and Gaussian elimination without pivoting on a diagonally dominant tridiagonal matrix is backward stable (Higham, Chapter 9). The right side $6(\delta_k - \delta_{k-1})$ is a difference of nearby slopes and suffers [cancellation](/catastrophic-cancellation/) when $h$ is small; its absolute error is about $u \max|y| / h$, so the moments carry an absolute error of order $u \max|y| / h^2$. In L8 and L9 the moments are multiplied by $h^2$, so the computed $s(t)$ is accurate to a modest multiple of $u \max_k |y_k|$. This last chain is a sketch, not a proved bound; the tests observe it.

## Properties

- **$C^2$ and piecewise cubic.** The highest smoothness a piecewise cubic with knots at the data can have without being a single cubic.
- **Global, but with fast decay.** Changing one value $y_j$ changes the spline everywhere. On a uniform mesh the change in $M_k$ decays like $(2 - \sqrt3)^{|k - j|} \approx 0.268^{|k - j|}$, because the interior rows are $(1, 4, 1)$ and $-2 + \sqrt3$ is the root of $r^2 + 4r + 1 = 0$ inside the unit disk. The same decay limits the damage of a wrong end condition to a few intervals near the end.
- **Bounded Lebesgue constant (observed).** The norm of the natural spline interpolation operator on a uniform mesh, computed as $\max_t \sum_k |\ell_k(t)|$ with cardinal splines $\ell_k$, is 1.474 for $n = 5$, 1.5455 for $n = 10$, 1.5490 for $n = 20$ and 1.5482 for $n = 40$. Compare the exponential growth of the [Lebesgue constant](/lebesgue-constant/) of polynomial interpolation at equispaced nodes.
- **Exact on polynomials.** The clamped spline with exact slopes reproduces cubics. The natural spline reproduces only linear functions, since a cubic with nonzero $f''$ at an end violates the end condition.
- **Not shape preserving.** The spline can overshoot monotone data and oscillate near jumps.
- **Linear in the data**, and affine invariant in $x$ and $y$.

## Variants and improvements

- **Not-a-knot.** Require $s'''$ to be continuous at $x_1$ and $x_{n-1}$, so the first two and last two pieces are each one cubic. This needs no derivatives and keeps the $O(h^4)$ accuracy; it is the default in de Boor's routines and in many libraries. It needs $n \ge 3$ (with fewer knots the result is the interpolating polynomial).
- **Periodic.** For periodic data require $s, s', s''$ to agree at $x_0$ and $x_n$; the system becomes cyclic tridiagonal.
- **Second derivatives given.** Prescribing $M_0$ and $M_n$ generalizes the natural condition and is fourth order when the true values are used.
- **B-spline form.** The same spline written in the [B-spline](/b-spline/) basis gives a banded system and the evaluation of [de Boor's algorithm](/de-boor-algorithm/); this form extends to any degree and to general knots.
- **Smoothing splines.** For noisy data, minimize $\sum (g(x_k) - y_k)^2 + \lambda \int g''^2$; the minimizer is still a natural cubic spline ([smoothing spline](/smoothing-spline/), Reinsch 1967).
- **Shape-preserving alternatives.** Give up $C^2$ for $C^1$: the [cubic Hermite spline](/cubic-hermite-spline/) with [Fritsch-Carlson](/fritsch-carlson-monotone-interpolation/) slopes, or Akima's method.
- **Parametric splines** for curves in the plane or space, and tensor-product splines such as [bicubic interpolation](/bicubic-interpolation/) for grids.

## When to use it

Use a cubic spline to interpolate smooth data on many points, especially on a mesh you do not choose, when you want a $C^2$ curve: for plotting, for curves with continuous curvature, and as a smooth model of tabulated functions that will be differentiated. Prefer clamped or not-a-knot end conditions for accuracy; use natural ends when nothing is known and the ends matter little. When the data are monotone or positive and overshoot is unacceptable, use a shape-preserving $C^1$ method. When you can choose the points and the function is analytic, [Chebyshev interpolation](/chebyshev-interpolation/) converges much faster. For noisy data use a smoothing spline instead.

## Pitfalls

- **The natural end condition is not neutral.** It forces $s'' = 0$ at the ends, which is wrong for most functions and drops the accuracy there to $O(h^2)$ (see the table).
- **Overshoot.** Steps or sharp corners in the data produce wiggles that decay only geometrically away from the jump; spline fits of monotone data can be nonmonotone.
- **Extrapolation.** Outside $[x_0, x_n]$ the end cubics grow quickly; do not trust them beyond a fraction of an interval.
- **Repeated or nearly equal knots.** Equal knots make $h_k = 0$; nearly equal knots with different values produce huge slopes. The implementation rejects exact duplicates.
- **Mixing up the end conditions.** Clamped slopes must be derivatives with respect to the same variable as the knots; supplying only one slope is an error.
- **Global effect.** Editing one point moves the whole curve slightly; when locality matters, use a Hermite spline.

## Implementations

## History

Draftsmen drew smooth curves with thin wooden or metal strips held by weights, called splines. Isaac Schoenberg (1946) introduced the mathematical spline, named it after the drafting tool, and studied cubic splines on uniform meshes. Holladay (1957) proved that the natural cubic spline is the interpolant of least integrated squared second derivative, which links it to the bending energy of the physical strip. The book of Ahlberg, Nilson and Walsh (1967) collected the early theory, including the tridiagonal moment equations. Hall (1968) proved the $5/384$ bound, and Hall and Meyer (1976) the sharp constants for the derivatives. Carl de Boor's work and his 1978 book (revised 2001) made B-splines and the not-a-knot condition standard in numerical software.

## References
