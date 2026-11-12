---
tag: 47FE7P
kind: definition
slug: b-spline
name: B-spline
aliases:
- Basis spline
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The B-splines N_(i,p) of a knot vector are nonnegative piecewise polynomials with small support. A B-spline curve is the sum of N_(i,p)(u) times the control points P_i.
prereqs: [knot-vector, spline]
see_also: [cox-de-boor-recursion, de-boor-algorithm, partition-of-unity, curry-schoenberg-theorem, nurbs, bezier-curve, convex-hull-property, spline-evaluation]
sources:
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter IX, The representation of piecewise polynomial functions by B-splines (the definition by divided differences, the recurrence, support, positivity and the basis property); Chapter XI, The B-spline series, control points, and knot insertion
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 2.2, Definition and properties of B-spline basis functions; Section 2.3, Derivatives of B-spline basis functions; Section 3.2, The definition and properties of B-spline curves
  - paper: doi:10.1007/BF02788653
    title: Haskell B. Curry and Isaac J. Schoenberg, On Pólya frequency functions IV, the fundamental spline functions and their limits, Journal d'Analyse Mathématique 17 (1966), 71 to 107
    locator: the B-spline as a divided difference of truncated powers, and its basic properties
  - paper: doi:10.1093/imamat/10.2.134
    title: Maurice G. Cox, The numerical evaluation of B-splines, IMA Journal of Applied Mathematics 10(2) (1972), 134 to 149
    locator: the stable recurrence for B-spline values
---

A B-spline is one of the basis functions $N_{i,p}$ that a degree $p$ and a [knot vector](/knot-vector/) define: a nonnegative piecewise polynomial of degree $p$ that is nonzero only on $p + 1$ consecutive knot spans. A B-spline curve is the combination $C(u) = \sum_{i=0}^{n} N_{i,p}(u) P_i$ of $n + 1$ control points. Every [spline](/spline/) with the same knots and degree is such a combination, by the [Curry-Schoenberg theorem](/curry-schoenberg-theorem/), so the B-splines are a basis of the spline space. Their small support gives local control, and their [partition of unity](/partition-of-unity/) puts each piece of the curve in the convex hull of $p + 1$ control points.

## Definition

Let $p \ge 0$, $n \ge p$, and let $T = (t_0, \ldots, t_{n+p+1})$ be a knot vector. The **B-splines of degree $p$** on $T$ are the functions $N_{i,p}$, $0 \le i \le n$, given by the [Cox-de Boor recursion](/cox-de-boor-recursion/):

$$N_{i,0}(u) = \begin{cases} 1 & t_i \le u < t_{i+1}, \\ 0 & \text{otherwise}, \end{cases}$$

$$N_{i,r}(u) = \frac{u - t_i}{t_{i+r} - t_i} N_{i,r-1}(u) + \frac{t_{i+r+1} - u}{t_{i+r+1} - t_{i+1}} N_{i+1,r-1}(u), \qquad 1 \le r \le p.$$

A fraction with a zero denominator is read as 0. This is safe: the denominator $t_{i+r} - t_i$ is zero only when the support $[t_i, t_{i+r})$ of $N_{i,r-1}$ is empty, so that term is $0$ anyway.

For distinct knots the same function is a divided difference of truncated powers (Curry and Schoenberg):

$$N_{i,p}(x) = (t_{i+p+1} - t_i) \, [t_i, \ldots, t_{i+p+1}] \, (\cdot - x)_+^p ,$$

where the [divided difference](/divided-differences/) acts on the function $t \mapsto (t - x)_+^p$. With repeated knots the divided difference uses derivatives, and the formula still holds.

Given control points $P_0, \ldots, P_n$ in $\mathbb{R}^d$, the **B-spline curve** is

$$C(u) = \sum_{i=0}^{n} N_{i,p}(u) \, P_i, \qquad t_p \le u \le t_{n+1}.$$

With $d = 1$ and real coefficients $c_i$ the same sum is a **spline function** $f(x) = \sum_i c_i N_{i,p}(x)$. At the right end $u = t_{n+1}$ the half-open spans give a wrong value for a clamped knot vector; programs evaluate there with the last nonempty span (see [partition of unity](/partition-of-unity/)).

The main properties follow from the recursion by [induction](/induction/) on $r$:

1. **Local support.** $N_{i,p}(u) = 0$ for $u \notin [t_i, t_{i+p+1})$. So on a nonempty span $[t_\mu, t_{\mu+1})$ only $N_{\mu-p,p}, \ldots, N_{\mu,p}$ can be nonzero.
2. **Positivity.** $N_{i,p}(u) \ge 0$ for all $u$, and $N_{i,p}(u) > 0$ for $t_i < u < t_{i+p+1}$. Both weights in the recursion are nonnegative on the support of the term they multiply.
3. **Partition of unity.** $\sum_{i} N_{i,p}(u) = 1$ for $t_p \le u < t_{n+1}$. Outside the domain the sum is less than 1.
4. **Piecewise polynomial.** On each nonempty span $N_{i,p}$ is a polynomial of degree at most $p$. At a knot of multiplicity $\mu \le p$ it is $C^{p - \mu}$, and a knot of multiplicity $p + 1$ allows a jump.
5. **Derivative.** $N_{i,p}'(u) = \frac{p}{t_{i+p} - t_i} N_{i,p-1}(u) - \frac{p}{t_{i+p+1} - t_{i+1}} N_{i+1,p-1}(u)$ away from the knots, with the same 0/0 rule (NURBS Book, Section 2.3).

For the curve these give **local control**: a change of $P_i$ moves $C(u)$ only for $u \in [t_i, t_{i+p+1})$. They give the **strong [convex hull property](/convex-hull-property/)**: for $u$ in a span $[t_\mu, t_{\mu+1})$ of the domain, $C(u)$ is a [convex combination](/convex-combination/) of $P_{\mu-p}, \ldots, P_\mu$. They give **affine invariance**: an affine map applied to the control points maps the curve in the same way. And the curve has the [variation diminishing property](/variation-diminishing-property/). A point of the curve costs $O(p^2)$ operations with the [de Boor algorithm](/de-boor-algorithm/), after a search for the span.

## Examples and non-examples

**Degree 0 and 1.** $N_{i,0}$ is the indicator of $[t_i, t_{i+1})$. $N_{i,1}$ is the hat function that rises linearly from 0 at $t_i$ to 1 at $t_{i+1}$ and falls back to 0 at $t_{i+2}$. A B-spline curve of degree 1 is the control polygon itself, with $P_i$ at the parameter $t_{i+1}$.

**A uniform quadratic B-spline.** On the knots $0, 1, 2, 3$, $N_{0,2}$ is $u^2/2$ on $[0, 1)$, $(-2u^2 + 6u - 3)/2$ on $[1, 2)$ and $(3 - u)^2/2$ on $[2, 3)$. It is $C^1$, it is positive on $(0, 3)$, and its largest value is $3/4$ at $u = 3/2$. Every B-spline on uniform knots is a shifted and scaled copy of this shape for its degree.

**A clamped quadratic curve.** Take $p = 2$, $T = (0, 0, 0, 1, 2, 3, 3, 3)$ and the control points $P_0 = (0, 0)$, $P_1 = (1, 2)$, $P_2 = (3, 3)$, $P_3 = (5, 1)$, $P_4 = (6, 0)$. At $u = 3/2$ the span is $[1, 2)$, and the five basis values are $0, 1/8, 3/4, 1/8, 0$. So

$$C(3/2) = \tfrac{1}{8}(1, 2) + \tfrac{3}{4}(3, 3) + \tfrac{1}{8}(5, 1) = (3, 21/8).$$

The curve starts at $C(0) = P_0$ and ends at $C(3) = P_4$, because the knot vector is clamped. It does not pass through $P_1$, $P_2$ or $P_3$. A move of $P_0$ changes the curve only on $[0, 1)$, the support $[t_0, t_3)$ of $N_{0,2}$.

**The Bézier case.** With $T = (0, \ldots, 0, 1, \ldots, 1)$, $p + 1$ copies of each, and $n = p$, the B-splines are the [Bernstein polynomials](/bernstein-polynomials/) $\binom{p}{i} u^i (1 - u)^{p - i}$, and the curve is a [Bézier curve](/bezier-curve/). A B-spline curve with more control points is a chain of Bézier pieces with built-in smoothness at the joints.

**Non-examples.**

- The cardinal basis functions of the [Catmull-Rom spline](/catmull-rom-spline/) take negative values between the knots. They sum to 1, but they are not B-splines, and the curve can leave the convex hull of its control points.
- The [Lagrange](/lagrange-interpolation/) basis polynomials for $n + 1$ nodes are nonzero almost everywhere, so a change of one coefficient moves the whole curve. They have no local support.
- A B-spline curve is not an interpolating curve: in general $C(u) \ne P_i$ for all $u$. To make a curve through given points, solve the collocation system of the [Schoenberg-Whitney theorem](/schoenberg-whitney-theorem/), as in [curve interpolation](/curve-interpolation/).

## Related definitions

- [Knot vector](/knot-vector/) and [spline](/spline/): the data that a B-spline needs, and the space that the B-splines span.
- [Cox-de Boor recursion](/cox-de-boor-recursion/) computes the $p + 1$ nonzero values $N_{\mu-p,p}(u), \ldots, N_{\mu,p}(u)$. The [de Boor algorithm](/de-boor-algorithm/) computes $C(u)$ without the basis values. Both solve [spline evaluation](/spline-evaluation/).
- [Partition of unity](/partition-of-unity/), [convex hull property](/convex-hull-property/) and [variation diminishing property](/variation-diminishing-property/): the shape properties that the definition gives.
- [Curry-Schoenberg theorem](/curry-schoenberg-theorem/): the B-splines are a basis. [Schoenberg-Whitney theorem](/schoenberg-whitney-theorem/): when interpolation with them works.
- [Knot refinement](/knot-refinement/), [Boehm knot insertion](/boehm-knot-insertion/) and the [Oslo algorithm](/oslo-algorithm/): the same curve on more knots. [Chaikin corner cutting](/chaikin-corner-cutting/) and the [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/): uniform knot doubling as subdivision.
- [NURBS](/nurbs/): rational B-spline curves, with a weight per control point. [Tensor product surfaces](/tensor-product-surface/): products $N_{i,p}(u) N_{j,q}(v)$.
- [Control points](/control-points/): the coefficients $P_i$ as a geometric object.

## References
