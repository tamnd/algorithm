---
tag: 6HX661
kind: problem
slug: curve-evaluation
name: Curve evaluation
aliases:
- evaluating a parametric curve
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: Given a curve by its control points (Bezier, B-spline or rational) and parameter values, compute the curve points and, if asked, derivatives. Costs are counted per point.
model: real-ram
complexity:
  vars: {n: the degree, m: the number of parameter values}
  time: {worst: O(m n)}
prereqs: [parametric-curve, bezier-curve]
see_also: [de-casteljau-algorithm, de-boor-algorithm, horner-rule, polynomial-evaluation, fast-multipoint-evaluation, spline-evaluation, arc-length-parametrization, curve-from-control-polygon]
sources:
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 4, The de Casteljau Algorithm, Chapter 5, The Bernstein Form of a Bezier Curve (the power form and its conversion), and Chapter 8, B-Spline Curves (the de Boor algorithm)
  - book: isbn:9783540437611
    title: Hartmut Prautzsch, Wolfgang Boehm and Marco Paluszny, Bezier and B-Spline Techniques, Springer, 2002
    locator: Section 2.3, The de Casteljau algorithm (page 13), Section 2.9, Conversion to monomial form (page 22), and Section 3.6, Curve generation by forward differences (page 32)
  - paper: doi:10.1016/0167-8396(88)90016-7
    title: Rida T. Farouki and V. T. Rajan, Algorithms for polynomials in Bernstein form, Computer Aided Geometric Design 5(1), 1-26 (1988)
    locator: the evaluation, arithmetic and basis conversion of polynomials in Bernstein form
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 5, Polynomials (the rounding error bound of Horner's method)
---

Curve evaluation is the problem of computing the points $C(t_1), \dots, C(t_m)$ of a [parametric curve](/parametric-curve/) that is given by its [control points](/control-points/), and sometimes its derivatives at the same parameters. It is the inner loop of drawing, of CAD and of motion along a path. The cost is counted per point, with the degree $n$ as the main variable, and the accuracy in floating point is the second measure. The algorithms are on separate pages, mainly the [de Casteljau algorithm](/de-casteljau-algorithm/) and the [de Boor algorithm](/de-boor-algorithm/).

## In plain words

A curve in a drawing program is stored as a short list of points that shape it, not as the points that you see. To draw it, or to move an object along it, the program must turn a time value into a position. That is this problem: you give the stored points and a value between the start and the end, and you get back the point on the curve at that value. Often you also want the direction of motion there.

There are several ways to do it. Some are fast, and some give fewer rounding errors. A program that draws many points of a simple curve picks a fast way. A program that must cut the curve at the point, or that needs every digit, picks a careful way.

## Definition

**Input.** A curve representation and parameter values $t_1, \dots, t_m$ in the domain. The usual representations are:

- a [Bézier curve](/bezier-curve/) of degree $n$: control points $P_0, \dots, P_n \in \mathbb{R}^d$, with $C(t) = \sum_i P_i B_i^n(t)$ on $[0, 1]$;
- a [B-spline](/b-spline/) curve of degree $p$: control points $P_0, \dots, P_n$ and a [knot vector](/knot-vector/) of $n + p + 2$ knots, with $C(t) = \sum_i P_i N_{i,p}(t)$;
- a [rational Bézier curve](/rational-bezier-curve/) or a [NURBS](/nurbs/) curve: the same with a positive weight per control point;
- a curve in power form: $C(t) = \sum_k a_k t^k$ with vector coefficients $a_k$.

**Output.** The points $C(t_j)$, and, in the variant with derivatives, $C'(t_j), \dots, C^{(k)}(t_j)$.

**Cost model.** The [real RAM](/real-ram/): one unit per arithmetic operation on real numbers, so one operation on points of $\mathbb{R}^d$ costs $d$ units. The cost is given per evaluated point. For floating point, the accuracy is the forward error of each coordinate, compared with the condition number of the value in the chosen basis.

This page is the problem. The [de Casteljau algorithm](/de-casteljau-algorithm/) and the [de Boor algorithm](/de-boor-algorithm/) are two algorithms that solve it, each for one representation.

## Variants

- **One point or many.** One parameter value, many arbitrary values, or an even grid $t_j = j/m$. On a grid, the work of one point can be reused for the next.
- **With derivatives.** Tangent, curvature and the [Frenet frame](/frenet-frame/) need the first two or three derivatives at the same parameter.
- **With subdivision.** Some uses need the control polygons of the two parts of the curve split at $t$, not only the point. This links evaluation to [curve subdivision](/curve-from-control-polygon/).
- **Exact or floating point.** With rational control points and parameters the values are rational, and an exact method gives them exactly. In floating point the error depends on the basis and the method.
- **By arc length.** Motion at constant speed needs the parameter for a given arc length first; see [arc length parametrization](/arc-length-parametrization/).
- **Surfaces.** A [tensor product surface](/tensor-product-surface/) of degree $n$ in each direction is evaluated as $n + 1$ curve evaluations in one direction followed by one in the other.

## Examples

Take the cubic Bézier curve with $P_0 = (0, 0)$, $P_1 = (1, 2)$, $P_2 = (3, 2)$, $P_3 = (4, 0)$. Its power form is $x(t) = 3t + 3t^2 - 2t^3$ and $y(t) = 6t(1 - t)$.

- **By the definition.** At $t = 1/4$ the Bernstein values are $27/64, 27/64, 9/64, 1/64$, and $C(1/4) = (29/32, 9/8)$.
- **By the Bernstein Horner scheme.** Write $C(t) = (1 - t)^n \sum_i \binom{n}{i} P_i s^i$ with $s = t / (1 - t)$. At $t = 1/4$, $s = 1/3$, and Horner's rule in $s$ gives $\sum_i \binom{3}{i} P_i s^i = (0, 0) + (1, 2) + (1, 2/3) + (4/27, 0) = (58/27, 8/3)$. Multiply by $(3/4)^3 = 27/64$: the point is $(29/32, 9/8)$ again.
- **By forward differences on a grid.** For $x(t)$ with step $1/4$, the values at $0, 1/4, 1/2, 3/4, 1$ are $0, 29/32, 2, 99/32, 4$. The first differences are $29/32, 35/32, 35/32, 29/32$, the second differences are $3/16, 0, -3/16$, and the third difference is the constant $-3/16 = 6 \cdot (-2) \cdot (1/4)^3$. After the setup, each new value costs three additions per coordinate.
- **Many points in high degree.** For a polynomial of degree $n$ and $m = n + 1$ points, fast [multipoint evaluation](/fast-multipoint-evaluation/) beats $m$ separate evaluations; it is rarely used for curves, whose degree is small.

## Known algorithms

| Method | Cost per point | Accuracy in floating point |
|---|---|---|
| [de Casteljau algorithm](/de-casteljau-algorithm/) | $\Theta(n^2 d)$ | error at most $\gamma_{3n} \sum_i \lvert P_i \rvert B_i^n(t)$ for $t \in [0, 1]$; also gives the split polygons |
| Bernstein Horner scheme in $s = t/(1-t)$ | $\Theta(n d)$, plus the binomial coefficients once | less stable than de Casteljau; use it for $t \le 1/2$, and $s = (1 - t)/t$ with the reversed points for $t > 1/2$, so that $s \le 1$ |
| Conversion to power form, then [Horner's rule](/horner-rule/) | $\Theta(n d)$ after $O(n^2 d)$ conversion | error at most $\gamma_{2n} \sum_k \lvert a_k \rvert \lvert t \rvert^k$, which can be exponentially larger |
| Forward differencing on an even grid | $\Theta(n d)$ additions after $O(n^2 d)$ setup | the error grows with the number of steps |
| [de Boor algorithm](/de-boor-algorithm/) for B-splines | $\Theta(p^2 d)$, plus $O(\log n)$ to find the span | as stable as de Casteljau |
| [Fast multipoint evaluation](/fast-multipoint-evaluation/) | $O(n \log^2 n)$ in total for $n$ points | unstable in floating point |

The rational and NURBS cases use the same methods on the homogeneous points $(w_i P_i, w_i)$ in $\mathbb{R}^{d+1}$, and one division per coordinate at the end. For derivatives, the de Casteljau and de Boor triangles give the first $k$ derivatives from their levels $n - k$ to $n - 1$ at no extra cost of order. The [polynomial evaluation](/polynomial-evaluation/) page covers the one-dimensional problem in the power basis. For the evaluation of a spline function in numerical analysis, see [spline evaluation](/spline-evaluation/).

## Bounds

- **Upper bound.** $O(n d)$ operations per point for a Bézier curve of degree $n$, by the Bernstein Horner scheme, and $O(p^2 d + \log n)$ per point for a B-spline curve of degree $p$ with $n + 1$ control points. So $m$ points cost $O(m n d)$ for a Bézier curve.
- **Input lower bound.** Each point of a Bézier curve depends on every control point, because $B_i^n(t) > 0$ for $t \in (0, 1)$. So any method that is correct for all inputs reads all $n + 1$ points, which is $\Omega(n d)$ for one point. For a B-spline only the $p + 1$ points of the active span matter.
- **Multiplications.** For a polynomial whose coefficients are part of the input, Horner's $n$ multiplications are optimal; see [Horner's rule optimality](/horners-rule-optimality/). So the $\Theta(n)$ methods are optimal up to a constant factor, and the de Casteljau algorithm pays a factor $n$ for stability and subdivision.
- **Accuracy.** For $t \in [0, 1]$, the error bound of the de Casteljau algorithm is a small multiple of $u$ times the condition number $\sum_i |P_i| B_i^n(t)$ of the value in Bernstein form (Farouki and Rajan). No method in the same basis can be much better in general, because a relative change of size $u$ in the input already changes the value by that much.

## Reductions

- A Bézier curve in $\mathbb{R}^d$ is $d$ polynomials in Bernstein form, so the problem is $d$ copies of [polynomial evaluation](/polynomial-evaluation/) in the Bernstein basis.
- A rational curve in $\mathbb{R}^d$ reduces to a polynomial curve in $\mathbb{R}^{d+1}$, followed by a division.
- A B-spline curve reduces to a Bézier curve on each span, by knot insertion until each inner knot has multiplicity $p$ ([Boehm knot insertion](/boehm-knot-insertion/)).
- The $k$-th derivative of a Bézier curve of degree $n$ is a Bézier curve of degree $n - k$ with the control points $\frac{n!}{(n-k)!} \Delta^k P_i$, so derivative evaluation reduces to point evaluation.

## Applications

- Drawing curves, after a choice of parameters that keeps the polyline within a tolerance of the curve ([curve from control polygon](/curve-from-control-polygon/)).
- Motion along paths in animation and robotics, often with the derivatives for speed and direction.
- Root finding, [ray-object intersection](/ray-object-intersection/) and [curve intersection](/curve-intersection/), which evaluate the curve or its subdivisions many times.
- Font rendering and vector graphics, which evaluate many quadratic and cubic pieces.

## References
