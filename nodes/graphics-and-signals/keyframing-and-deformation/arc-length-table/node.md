---
tag: JYYH1E
kind: algorithm
slug: arc-length-table
name: Arc length table
aliases:
- arc length lookup table
area: graphics-and-signals/keyframing-and-deformation
level: core
summary: Tabulate the arc length of a parametric curve at sample parameters, then invert it by binary search, linear interpolation and optional Newton steps, to move along a path at a given speed.
model: real-ram
complexity:
  vars: {m: "the number of table intervals", r: "the number of Newton steps per query"}
  time: {build: "Θ(m)", query: "O(log m + r)"}
  space: {extra: "Θ(m)"}
properties: {deterministic: true, exact: false, online: false, recursive: true}
prereqs: [arc-length-parametrization, gauss-legendre-quadrature, binary-search]
see_also: [ease-in-ease-out, keyframe-interpolation, adaptive-quadrature, newton-raphson-method, catmull-rom-spline, bezier-curve, composite-quadrature, time-scaling]
sources:
  - paper: doi:10.1109/38.55155
    title: Brian Guenter and Richard Parent, Computing the arc length of parametric curves, IEEE Computer Graphics and Applications 10(3), 72-78, 1990
    locator: the whole paper (adaptive Gaussian quadrature of the speed, a table of arc lengths, and Newton iteration for the inverse)
  - book: isbn:9780124158429
    title: Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012
    locator: "Chapter 3, Section 3.2 (controlling the motion of a point along a curve: arc length tables, their inversion, and Gaussian quadrature)"
---

An arc length table lets an animation move a point along a curve $c(u)$ by distance instead of by parameter.
Most curves used in animation, such as [Bezier](/bezier-curve/) and [Catmull-Rom](/catmull-rom-spline/) curves, have no closed form for the arc length $s(u) = \int_a^u |c'(x)|\,dx$, and the parameter $u$ does not grow at a constant rate with the distance.
The table stores $s$ at $m + 1$ sample parameters, computed by adaptive [Gauss-Legendre quadrature](/gauss-legendre-quadrature/).
A query for a distance $s^*$ finds the right interval by [binary search](/binary-search/), interpolates linearly, and can refine the result with [Newton steps](/newton-raphson-method/).
Guenter and Parent (1990) gave this scheme for animation paths.

## In plain words

A curve in a drawing program has a parameter that runs from 0 to 1, but equal steps of the parameter do not give equal steps along the curve.
Where the control points are close, the curve is slow; where they are far apart, it is fast.
To move a camera at a steady speed, you need the parameter for a given distance.
The table measures the length of the curve at many evenly spaced parameter values, once.
Later, to find where the distance 3.7 is, you look in the table for the two entries around 3.7 and take the value in between.
If you need more accuracy, a few correction steps polish the answer.

## The problem

The input is a differentiable curve $c : [a, b] \to \mathbb{R}^d$, given by a function for its derivative $c'(u)$, a table size $m$, and a tolerance $\varepsilon$.
The build step outputs the sample parameters $u_k = a + kh$, $h = (b - a)/m$, and the arc lengths $s_k \approx s(u_k)$ for $k = 0, \dots, m$.
A query takes a distance $s^* \in [0, s_m]$ and outputs $u$ with $s(u) \approx s^*$.
The theory of the arc length function and of the arc length parametrization is on the page [arc length parametrization](/arc-length-parametrization/).

## The algorithm

$G_5(f, x, y)$ is the five-point Gauss-Legendre rule for $\int_x^y f$, exact for polynomials of degree 9.

```pseudo id=main
BUILD(c', a, b, m, ε)                              ▷ returns the table (u_k, s_k)
L1  h ← (b - a) / m; u₀ ← a; s₀ ← 0
L2  for k ← 1 to m do
L3      uₖ ← a + k h
L4      sₖ ← sₖ₋₁ + AGL(|c'|, uₖ₋₁, uₖ, ε / m)
AGL(f, x, y, ε)                                    ▷ adaptive Gauss-Legendre quadrature
L5  W ← G₅(f, x, y)
L6  L ← G₅(f, x, (x + y)/2); R ← G₅(f, (x + y)/2, y)
L7  if |L + R - W| ≤ ε then return L + R
L8  return AGL(f, x, (x + y)/2, ε/2) + AGL(f, (x + y)/2, y, ε/2)
QUERY(s*, r)                                       ▷ r Newton steps
L9  find k with sₖ ≤ s* ≤ sₖ₊₁ by binary search
L10 u ← uₖ + h (s* - sₖ) / (sₖ₊₁ - sₖ)
L11 repeat r times: u ← u - (sₖ + G₅(|c'|, uₖ, u) - s*) / |c'(u)|
L12 return u
```

Lines L1 to L4 fill the table, one interval at a time, so the cost grows linearly with $m$.
Lines L5 to L8 split an interval in half until the two halves agree with the whole to the tolerance.
Line L9 is a binary search on the sorted lengths.
Line L10 is the linear interpolation of the inverse function.
Line L11 is Newton's method on $g(u) = s(u) - s^*$, with $g'(u) = |c'(u)|$; the length from $u_k$ to $u$ comes from one Gauss-Legendre rule on a short interval.
The implementation also clamps $u$ to $[u_k, u_{k+1}]$ after each Newton step and stops if the speed is 0.

## Example

Take the parabola $c(u) = (u, u^2)$ on $[0, 1]$, with the speed $\sqrt{1 + 4u^2}$, and $m = 4$.
The exact total length is $\frac14(2\sqrt5 + \operatorname{asinh} 2) = 1.478943$.

- Lines L1 to L4 give $u = (0, 0.25, 0.5, 0.75, 1)$ and $s = (0, 0.26006, 0.57390, 0.97473, 1.47894)$. Each entry agrees with the closed form $s(u) = \frac12 u\sqrt{1 + 4u^2} + \frac14\operatorname{asinh}(2u)$ to $10^{-12}$.
- Query $s^* = 0.75$. Line L9 finds $k = 2$, since $0.57390 \le 0.75 < 0.97473$.
- Line L10: $u = 0.5 + 0.25 \cdot (0.75 - 0.57390)/(0.97473 - 0.57390) = 0.60984$.
- The exact answer is $u = 0.6173865$. One Newton step gives $0.6174145$, with the error $2.8 \cdot 10^{-5}$, and a second step gives $0.6173865$, with the error $4 \cdot 10^{-10}$.

The worst error of line L10 alone over $[0, s_m]$ is $1.9 \cdot 10^{-3}$ for $m = 8$, $4.9 \cdot 10^{-4}$ for $m = 16$, $1.2 \cdot 10^{-4}$ for $m = 32$ and $3.0 \cdot 10^{-5}$ for $m = 64$: each doubling of $m$ divides the error by 4.

## Correctness

The speed $|c'|$ is not negative, so the table values $s_k$ do not decrease, and the binary search of line L9 finds a valid interval.
If the speed is positive, $s$ is strictly increasing and has a differentiable inverse $u(s)$.

The error of a table entry is the sum of the quadrature errors of its intervals.
The five-point rule on an interval of length $\ell$ has the error $\frac{(5!)^4}{11\,(10!)^3}\,\ell^{11} f^{(10)}(\xi)$, so for a smooth curve the table is accurate to roundoff with a moderate $m$.
The stopping test of line L7 estimates the error by the difference of two rules; it is not a bound, and a curve with a sharp feature inside one interval can fool it.

The linear interpolation of line L10 is the linear interpolant of the inverse function $u(s)$ on $[s_k, s_{k+1}]$.
Its error is at most $\frac18 (s_{k+1} - s_k)^2 \max|u''(s)|$.
With $s_{k+1} - s_k \le h \max|c'|$, the error is $O(h^2)$, of the second order in the sample spacing.

Newton's method on $g(u) = s(u) - s^*$ converges quadratically near the root when $g' = |c'|$ is bounded away from 0: the new error is at most $\frac{\max|s''|}{2\min|s'|}$ times the square of the old one.
Starting from an $O(h^2)$ guess, one step gives $O(h^4)$ and two steps $O(h^8)$, until the quadrature error of line L11 dominates.
The [proof](proofs/correctness.md) gives the details.

## Complexity

The build step calls AGL $m$ times.
For a smooth curve and a fixed tolerance, the recursion stops after a bounded number of splits, so the build costs $\Theta(m)$ evaluations of the speed.
For a curve with a corner or a cusp the recursion goes deeper near the bad point, and the implementation caps its depth.
The table takes $\Theta(m)$ space.
A query costs $O(\log m)$ for the binary search and $O(1)$ for each Newton step, five speed evaluations for $G_5$ and one for $|c'(u)|$.
If the queries come in increasing order of $s^*$, as in an animation that moves forward, a pointer that walks through the table replaces the binary search, at $O(1)$ amortized cost per query.

## Properties

- **Second order in the spacing.** The inverse by linear interpolation has the error $O(h^2)$; doubling $m$ divides it by 4, as in the example.
- **Exact for constant speed.** On a curve with a constant speed, such as an arc of a circle, $s$ is linear in $u$ and line L10 is exact.
- **Monotone queries.** Without Newton steps, the returned $u$ is a monotone function of $s^*$, so the point never moves backwards.
- **A speed that jumps.** The piecewise linear inverse has a derivative that jumps at the table entries, by $O(h)$, so the speed of the moving point jumps slightly there. Newton steps remove this to the accuracy of the iteration.
- **Independence of the motion.** The table depends only on the curve. One table serves every speed curve, such as each [ease curve](/ease-in-ease-out/) of a shot.

## Variants and improvements

- **Newton with full quadrature.** Find $u$ by Newton iteration on $s(u) - s^*$, with adaptive quadrature for each value of $s(u)$. The table then only gives the start value and the length up to $u_k$.
- **Uniform in distance.** Resample the table so that the lengths, not the parameters, are evenly spaced. Then line L9 becomes a division, at the cost of an inverse at build time.
- **Polyline tables.** Sum the chord lengths of a fine polyline. It is simple, but its error is $O(n^{-2})$ for $n$ chords, much worse than Gauss-Legendre quadrature.
- **Higher-order inverse.** Interpolate $u(s)$ with a cubic Hermite segment, using $u'(s) = 1/|c'(u)|$ at the table entries. The error is then $O(h^4)$ with no iteration.
- **Arc length of a spline.** For a spline, build one table per segment, or one table with entries at the knots, so that no interval contains a knot.

## When to use it

Use an arc length table to move a camera, a character or an object along a path at a speed that the animator controls, with the distance from an [ease curve](/ease-in-ease-out/) or from a [time scaling](/time-scaling/).
It also places objects at equal distances along a curve, such as the posts of a fence or the dashes of a line.
If the curve has a known arc length, as a line or a circle does, use the closed form.

## Pitfalls

- **Points where the speed is 0.** At a cusp or at repeated control points, $|c'(u)| = 0$, the inverse function is not differentiable, and Newton's method divides by 0. Stop the iteration there, or keep $u$ in the interval of line L9.
- **Too few entries.** The error of line L10 grows with the square of the spacing and with the variation of the speed. Check it on the curve, not only on the total length.
- **A tolerance that is too tight.** The quadrature cannot be more accurate than the roundoff of the sum of the lengths. A tolerance below about $10^{-14}$ times the length only makes the recursion deeper.
- **Changing curves.** If the control points move, the table is wrong. Rebuild it, or tabulate only the segments that changed.
- **Arc length is not timing.** The table gives a constant speed only if $s^*$ grows linearly with time. Easing and pauses come from the curve that gives $s^*$.

## Implementations

## History

Guenter and Parent (1990) described the computation of the arc length of parametric curves for animation, with adaptive Gaussian quadrature of the speed, a table of lengths, and Newton iteration for the inverse.
Parent's textbook (2012) presents the arc length table as the standard way to control the speed along a path.
The quadrature rules come from Gauss and the error estimate by halving the interval is the usual one of adaptive quadrature.

## References
