---
tag: MPYB8D
kind: algorithm
slug: de-casteljau-algorithm
name: de Casteljau algorithm
aliases:
- de Casteljau's algorithm
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: Evaluates a Bezier curve of degree n at t by n rounds of linear interpolation between neighbouring control points, in O(n^2) operations, and splits the curve at t as a by-product.
solves: [curve-evaluation, curve-from-control-polygon]
model: real-ram
complexity:
  vars: {n: the degree, d: the dimension of the points}
  time: {worst: Θ(n^2 d), best: Θ(n^2 d)}
  space: {extra: Θ(n d)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1959
  people: [Paul de Faget de Casteljau]
  note: De Casteljau described the method in internal reports at Citroen from 1959. The reports were not published, and the method became widely known in the 1970s.
prereqs: [bezier-curve, bernstein-polynomials]
see_also: [de-boor-algorithm, horner-rule, lane-riesenfeld-algorithm, rational-bezier-curve, bezier-clipping, numerical-stability, curve-evaluation, curve-from-control-polygon]
sources:
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 4, The de Casteljau Algorithm (pages 43 to 55), Chapter 5 for the derivative from the last two levels, and Section 13.2 for the rational form
  - book: isbn:9783540437611
    title: Hartmut Prautzsch, Wolfgang Boehm and Marco Paluszny, Bezier and B-Spline Techniques, Springer, 2002
    locator: Section 2.3, The de Casteljau algorithm (page 13), Section 2.4, Derivatives (page 15), and Section 3.3, Subdivision (page 27)
  - paper: doi:10.1016/S0167-8396(99)00023-0
    title: Wolfgang Boehm and Andreas Muller, On de Casteljau's algorithm, Computer Aided Geometric Design 16(7), 587-605 (1999)
    locator: the algorithm, its geometric meaning, subdivision and its relation to other evaluation methods
  - paper: doi:10.1016/S0167-8396(99)00024-2
    title: Paul de Faget de Casteljau, De Casteljau's autobiography, My time at Citroen, Computer Aided Geometric Design 16(7), 583-586 (1999)
    locator: the origin of the method at Citroen in 1959
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 2.2 (the standard model of floating point arithmetic) and Chapter 3, Lemma 3.1 (products of factors 1 + delta and the constant gamma_n)
  - paper: doi:10.1016/0167-8396(87)90012-4
    title: Rida T. Farouki and V. T. Rajan, On the numerical condition of polynomials in Bernstein form, Computer Aided Geometric Design 4(3), 191-216 (1987)
    locator: the condition number of a value in Bernstein form, which the error bound of the algorithm matches
  - paper: doi:10.1016/0167-8396(89)90032-0
    title: Lyle Ramshaw, Blossoms are polar forms, Computer Aided Geometric Design 6(4), 323-358 (1989)
    locator: the polar form of a polynomial curve and the de Casteljau triangle as a table of its values
---

The de Casteljau algorithm computes the point $B(t)$ of a [Bézier curve](/bezier-curve/) of degree $n$. It replaces the $n + 1$ [control points](/control-points/) by the $n$ points that divide each edge of the control polygon in the ratio $t : (1 - t)$, and repeats this $n$ times. The last point is $B(t)$, the last two points give the tangent, and the first and last points of each round are the control points of the two parts of the curve split at $t$. It costs $\Theta(n^2)$ operations per point, more than the $O(n)$ of a Horner scheme, but each step is a convex combination, so the rounding error stays small.

## In plain words

Draw the control polygon. Put a mark on each edge, the same fraction of the way along each one. Join the marks: this gives a polygon with one corner less. Mark that polygon at the same fraction, and go on until one point is left. That point is on the curve.

You get more than the point. The last edge that you drew touches the curve at that point, so it gives the direction of the curve. And the first corners of all the polygons, read in order, are the control points of the part of the curve before the point. The last corners give the part after it. So the same work also cuts the curve in two, and each part is again a curve of the same kind.

## The problem

The input is a list of $n + 1$ control points $P_0, \dots, P_n$ in $\mathbb{R}^d$ and a parameter $t$, usually in $[0, 1]$. The output is $B(t) = \sum_{i=0}^n P_i B_i^n(t)$, with the [Bernstein polynomials](/bernstein-polynomials/) $B_i^n$, and, if asked, the control points of the curve on $[0, t]$ and on $[t, 1]$, each reparametrized to $[0, 1]$. This is one method for [curve evaluation](/curve-evaluation/) and for [curve subdivision](/curve-from-control-polygon/).

The model is the [real RAM](/real-ram/): each addition, subtraction and multiplication of real numbers costs one unit. A point operation on $d$ coordinates costs $d$ units. The implementation uses Python fractions, so all results are exact; the error analysis below is for floating point.

## The algorithm

Write $b_i^0 = P_i$. Round $r$ computes $b_i^r$ for $i = 0, \dots, n - r$.

```pseudo id=main
DE-CASTELJAU(P_0, ..., P_n, t)
L1  b_i ← P_i for i = 0, ..., n                     ▷ level 0 of the triangle
L2  left_0 ← P_0, right_n ← P_n
L3  for r ← 1 to n do
L4      for i ← 0 to n − r do                        ▷ increasing i, so b_(i+1) is still old
L5          b_i ← (1 − t) b_i + t b_(i+1)            ▷ now b_i = b_i^r
L6      left_r ← b_0, right_(n−r) ← b_(n−r)
L7  return b_0, (left_0, ..., left_n), (right_0, ..., right_n)
```

The points form a triangle. Level 0 is the control polygon, level $r$ has $n + 1 - r$ points, and level $n$ is the single point $b_0^n = B(t)$:

$$b_i^r = (1 - t)\, b_i^{r-1} + t\, b_{i+1}^{r-1}, \qquad 1 \le r \le n,\ 0 \le i \le n - r.$$

The left edge of the triangle, $b_0^0, b_0^1, \dots, b_0^n$, is the control polygon of the part on $[0, t]$. The right edge, $b_0^n, b_1^{n-1}, \dots, b_n^0$, is the control polygon of the part on $[t, 1]$. The tangent is $B'(t) = n\,(b_1^{n-1} - b_0^{n-1})$.

The loop of line L4 overwrites the array in increasing order of $i$. When it writes $b_i$, the entry $b_{i+1}$ still holds level $r - 1$. So one array of $n + 1$ points is enough for the point $B(t)$.

## Example

Take the cubic with $P_0 = (0, 0)$, $P_1 = (1, 2)$, $P_2 = (3, 2)$, $P_3 = (4, 0)$ and $t = 1/4$. Each new point is $\frac34$ of the left point plus $\frac14$ of the right point.

| Level $r$ | Points $b_0^r, \dots, b_{3-r}^r$ |
|---|---|
| 0 | $(0, 0)$, $(1, 2)$, $(3, 2)$, $(4, 0)$ |
| 1 | $(1/4, 1/2)$, $(3/2, 2)$, $(13/4, 3/2)$ |
| 2 | $(9/16, 7/8)$, $(31/16, 15/8)$ |
| 3 | $(29/32, 9/8)$ |

So $B(1/4) = (29/32, 9/8)$. The direct sum with the Bernstein values $27/64, 27/64, 9/64, 1/64$ gives the same point: its $x$ is $\frac{27 \cdot 1 + 9 \cdot 3 + 1 \cdot 4}{64} = \frac{58}{64}$. The tangent is $3\,\big((31/16, 15/8) - (9/16, 7/8)\big) = (33/8, 3)$.

The split at $t = 1/4$ gives the left polygon $(0, 0), (1/4, 1/2), (9/16, 7/8), (29/32, 9/8)$ and the right polygon $(29/32, 9/8), (31/16, 15/8), (13/4, 3/2), (4, 0)$. At $t = 1/2$ the same cubic gives the levels $(1/2, 1), (2, 2), (7/2, 1)$, then $(5/4, 3/2), (11/4, 3/2)$, then $B(1/2) = (2, 3/2)$, with the horizontal tangent $3\,(3/2, 0) = (9/2, 0)$. The halves are $(0, 0), (1/2, 1), (5/4, 3/2), (2, 3/2)$ and $(2, 3/2), (11/4, 3/2), (7/2, 1), (4, 0)$.

## Correctness

By induction on $r$, with the recursion $B_j^r = (1 - t) B_j^{r-1} + t B_{j-1}^{r-1}$ of the Bernstein basis, each point of the triangle is

$$b_i^r = \sum_{j=0}^{r} P_{i+j} B_j^r(t).$$

So $b_0^n = \sum_j P_j B_j^n(t) = B(t)$. The left edge gives the curve on $[0, t]$ because of the identity $\sum_j B_j^n(u) B_k^j(t) = B_k^n(tu)$, and the right edge follows by reversing the polygon. The tangent comes from the derivative formula $B'(t) = n \sum_i (P_{i+1} - P_i) B_i^{n-1}(t)$ and the lemma at level $n - 1$. The full proofs, and the proof of the rounding error bound, are in the proof file below.

## Complexity

Round $r$ computes $n + 1 - r$ points, so there are $\sum_{r=1}^n (n + 1 - r) = n(n + 1)/2$ interpolations. Each costs $2d$ multiplications and $d$ additions, and $1 - t$ is computed once. So one point costs $\Theta(n^2 d)$ operations in the worst and in the best case. For the plane, $d = 2$, a cubic needs 6 interpolations, which is 24 multiplications and 12 additions. The point alone needs $\Theta(n d)$ extra space for one array. The two split polygons need $2(n + 1)$ more points, which is also $\Theta(n d)$.

A [Horner scheme](/horner-rule/) on the Bernstein form, or on the power form, takes $\Theta(n d)$ operations per point, and $n$ multiplications are needed in general (see [Horner's rule optimality](/horners-rule-optimality/)). The de Casteljau algorithm pays the extra factor $n$ for stability and for the subdivision, which Horner does not give.

## Properties

- **Every step is a convex combination.** For $t \in [0, 1]$, each $b_i^r$ is a convex combination of $P_i, \dots, P_{i+r}$. So every point of the triangle lies in the convex hull of the control points, and this gives a direct proof of the [convex hull property](/convex-hull-property/).
- **Small rounding error.** In floating point with unit roundoff $u$ and $t \in [0, 1]$, each coordinate of the computed point satisfies $|\hat b - B(t)| \le \gamma_{3n} \sum_i |P_i| B_i^n(t) \le \gamma_{3n} \max_i |P_i|$, with $\gamma_k = k u / (1 - k u)$, when $3 n u < 1$. The right side is the condition number of the value in Bernstein form (Farouki and Rajan 1987) times $u$, up to the factor $3n$. A Horner scheme on the power form has the bound $\gamma_{2n} \sum_k |a_k| t^k$, and $\sum_k |a_k| t^k$ can be exponentially larger. For $(1 - t)^{20}$, the Bernstein coefficients are $1, 0, \dots, 0$, and the power coefficients are $\binom{20}{k}(-1)^k$. At the double nearest to $0.7$, de Casteljau in double precision returns the correctly rounded value, and Horner on the power form has a relative error of $1.4 \cdot 10^{-2}$. At the double nearest to $0.9$, the Horner result is off by a factor of about $7.7 \cdot 10^{7}$.
- **Affine invariance.** The steps are affine combinations, so the algorithm commutes with affine maps of the points. It works in any dimension $d$, one coordinate at a time.
- **Subdivision is exact.** The two split polygons describe exactly the two parts of the curve, with no approximation. Repeated splitting makes the polygons converge to the curve, which is the base of [Bézier clipping](/bezier-clipping/), of subdivision methods for [curve intersection](/curve-intersection/) and of adaptive drawing.
- **Exact in rational arithmetic.** With rational points and a rational $t$, all points are rational, and the output is exact.

## Variants and improvements

- **Rational curves.** For a [rational Bézier curve](/rational-bezier-curve/) with weights $w_i$, run the algorithm on the homogeneous points $(w_i P_i, w_i)$ in $\mathbb{R}^{d+1}$ and divide by the last coordinate at the end. The weights must be positive for the steps to stay convex combinations.
- **Polar form (blossom).** Use a different parameter $t_r$ in round $r$. The result $b[t_1, \dots, t_n]$ is symmetric and affine in each argument, and $b[t, \dots, t] = B(t)$. The control points are $P_i = b[0^{n-i}, 1^{i}]$, and the points of the triangle are blossom values with arguments $0$, $1$ and $t$ (Ramshaw 1989).
- **Derivatives of higher order.** The $k$-th forward differences of level $n - k$ give $B^{(k)}(t) = \frac{n!}{(n-k)!} \Delta^k b_0^{n-k}$.
- **Midpoint subdivision.** At $t = 1/2$ each step is a sum and a halving. The [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/) and [Chaikin corner cutting](/chaikin-corner-cutting/) use repeated averaging of the same kind for B-splines.
- **B-splines.** The [de Boor algorithm](/de-boor-algorithm/) is the same triangle with weights that come from the knots. With the knot vector that has $n + 1$ zeros and $n + 1$ ones, it is the de Casteljau algorithm.
- **Faster evaluation.** For many points of low degree, the Bernstein Horner scheme in the variable $s = t / (1 - t)$ costs $O(n)$ per point, and forward differencing costs $O(n)$ per point on an even grid. Both are less stable; see [curve evaluation](/curve-evaluation/).

## When to use it

Use it when the degree is small or moderate, when accuracy matters, and when you need the split polygons: in clipping, intersection, adaptive flattening for drawing, and in any code that refines a curve near a point. Use it also for rational curves, through the homogeneous form. For a B-spline curve use the [de Boor algorithm](/de-boor-algorithm/). For millions of points on one cubic, where speed matters and a small error is acceptable, a Horner scheme or forward differencing is cheaper.

## Pitfalls

- **Parameters outside $[0, 1]$.** The algorithm still computes the polynomial, because the identity $b_i^r = \sum_j P_{i+j} B_j^r(t)$ holds for all $t$. But the weights $1 - t$ and $t$ then have opposite signs, the steps are no longer convex combinations, and the error bound above no longer holds.
- **The wrong overwrite order.** In place, $i$ must run upwards in line L4. With $i$ downwards, $b_{i+1}$ already holds level $r$ when $b_i$ needs level $r - 1$.
- **The factor $n$ of the tangent.** $b_1^{n-1} - b_0^{n-1}$ is the tangent direction. The derivative is $n$ times it. For a curve on an interval $[a, b]$, divide the derivative by $b - a$.
- **Weights in rational curves.** Running the algorithm on the Cartesian points and ignoring the weights gives a different curve. Use the homogeneous points, and divide only at the end.
- **Growing numbers in repeated splitting.** In exact arithmetic, each split multiplies the size of the denominators. In floating point, each split adds rounding error. Code that splits many times, such as [Bézier clipping](/bezier-clipping/), rounds the parameters to short binary fractions or uses the original polygon with a new interval each time.

## Implementations

The Python file in this folder has the function `de_casteljau(points, t)`, which returns the point and the two split polygons, and helpers for the derivative and the rational form. The tests compare it in exact fractions with the direct Bernstein sum, the halves with the original curve at the mapped parameters, and the convex hull and variation diminishing properties on random control polygons.

## History

Paul de Faget de Casteljau developed the method at Citroën from 1959 for the design of car bodies with curves and surfaces defined by "poles", which are the control points. Citroën kept his reports internal. At the same time, Pierre Bézier at Renault developed the same curves in another form, and the curves carry his name because he published. De Casteljau described his time at Citroën in 1999, in a special issue of Computer Aided Geometric Design, where Boehm and Müller also surveyed the algorithm.

## References
