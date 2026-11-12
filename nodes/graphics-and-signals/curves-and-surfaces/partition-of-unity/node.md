---
tag: QS43SM
kind: concept
slug: partition-of-unity
name: Partition of unity
aliases:
- partition of unity property
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Basis functions that are nonnegative and sum to 1. B-splines of degree p do so on the domain [t_p, t_(n+1)), not on the whole knot range, which gives affine invariance and the convex hull property.
prereqs: [b-spline]
see_also: [convex-hull-property, cox-de-boor-recursion, knot-vector, bernstein-polynomials, nurbs, de-boor-algorithm, convex-combination, finite-element-method]
sources:
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 2.2, Definition and properties of B-spline basis functions (the partition of unity on a span); Section 3.2, B-spline curves (affine invariance and the strong convex hull property); Section 4.2, NURBS curves (the rational basis)
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter IX, the B-splines as a partition of unity (from the recurrence and from Marsden's identity)
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: the chapters on Bézier and B-spline curves (affine invariance from the partition of unity)
  - paper: "Ivo Babuška and Jens M. Melenk, The partition of unity method, International Journal for Numerical Methods in Engineering 40 (1997), 727 to 758"
    locator: the use of a partition of unity to build finite element spaces
---

A family of functions $\varphi_0, \ldots, \varphi_n$ is a partition of unity on a set $D$ when every $\varphi_i$ is nonnegative on $D$ and $\sum_i \varphi_i(u) = 1$ for every $u \in D$. For a curve $C(u) = \sum_i \varphi_i(u) P_i$ the sum condition makes each point an affine combination of the control points, so the curve does not depend on the choice of the origin, and the sign condition makes it a [convex combination](/convex-combination/). The [Bernstein polynomials](/bernstein-polynomials/) are a partition of unity on $[0, 1]$. The [B-splines](/b-spline/) of degree $p$ on a [knot vector](/knot-vector/) $t_0, \ldots, t_{n+p+1}$ are a partition of unity on the domain $[t_p, t_{n+1})$, and not on the whole range $[t_0, t_{n+p+1}]$ of the knots.

## In plain words

Think of a set of weights that tell how much each control point pulls on the curve at one moment. A partition of unity means two things. No weight is negative, so no point pushes the curve away. And the weights always add up to one whole, so at each moment the curve point is a proper average of the control points.

Because of this, the curve point always lies inside the region that the control points surround. If you move, turn or stretch all the control points in the same way, the curve moves, turns or stretches in that way too, with no need to recompute it.

For B-splines the weights add up to one only on the middle part of the parameter range. Near the two ends of the knot list too few weights exist, and their sum falls below one.

## The idea

**Why the sum matters.** Let $A(x) = Lx + b$ be an affine map, with $L$ linear and $b$ a vector. Then

$$A\Bigl(\sum_i \varphi_i(u) P_i\Bigr) = \sum_i \varphi_i(u) \, L P_i + b \quad\text{and}\quad \sum_i \varphi_i(u) \, A(P_i) = \sum_i \varphi_i(u) \, L P_i + \Bigl(\sum_i \varphi_i(u)\Bigr) b .$$

The two are equal for every $b$ if and only if $\sum_i \varphi_i(u) = 1$. So the sum condition is exactly **affine invariance**: to transform the curve, transform the control points. With $\varphi_i \ge 0$ as well, $C(u)$ is a convex combination of the $P_i$ with $\varphi_i(u) > 0$, which gives the [convex hull property](/convex-hull-property/). The curve is not invariant under perspective maps; [NURBS](/nurbs/) are.

**Bernstein polynomials.** By the binomial theorem, $\sum_{i=0}^{n} \binom{n}{i} u^i (1 - u)^{n-i} = (u + (1 - u))^n = 1$ for every real $u$, and each term is nonnegative for $u \in [0, 1]$. So a [Bézier curve](/bezier-curve/) is affinely invariant, and for $u \in [0, 1]$ it lies in the hull of its control points.

**B-splines.** Let $p \ge 0$, $n \ge p$ and $t_0 \le \cdots \le t_{n+p+1}$, with the B-splines $N_{i,p}$ of the [Cox-de Boor recursion](/cox-de-boor-recursion/), half-open spans and the rule $0/0 = 0$. Each $N_{i,p}$ is nonnegative everywhere. The exact statement of the sum is:

1. For $t_p \le u < t_{n+1}$: $\sum_{i=0}^{n} N_{i,p}(u) = 1$.
2. At $u = t_{n+1}$: if $t_{n+1} < t_{n+p+1}$, the sum is $1$. If $t_{n+1} = t_{n+p+1}$, as for a clamped right end, no half-open span contains $u$, every $N_{i,p}(u)$ is $0$, and the sum is $0$. The **closing rule**, which evaluates at $u = t_{n+1}$ with the last nonempty span as a closed interval, gives the limits from the left and restores the sum $1$.
3. For $t_0 \le u < t_p$ and for $t_{n+1} < u < t_{n+p+1}$: the sum is less than $1$.

*Proof of 1.* Let $\mu$ be the span of $u$, with $p \le \mu \le n$ and $t_\mu \le u < t_{\mu+1}$. Only $N_{\mu-r,r}, \ldots, N_{\mu,r}$ can be nonzero at $u$, by local support. With $\omega_{j,r} = (u - t_j)/(t_{j+r} - t_j)$ the recursion gives

$$\sum_{i=\mu-r}^{\mu} N_{i,r}(u) = \sum_{i=\mu-r}^{\mu} \Bigl(\omega_{i,r} N_{i,r-1}(u) + (1 - \omega_{i+1,r}) N_{i+1,r-1}(u)\Bigr) = \sum_{j=\mu-r+1}^{\mu} \bigl(\omega_{j,r} + (1 - \omega_{j,r})\bigr) N_{j,r-1}(u),$$

because the terms with $N_{\mu-r,r-1}(u)$ and $N_{\mu+1,r-1}(u)$ are zero. For $\mu - r + 1 \le j \le \mu$ the denominator $t_{j+r} - t_j$ is at least $t_{\mu+1} - t_\mu > 0$, so the bracket is $1$. So the sum is the same for every degree $r$, and for $r = 0$ it is $N_{\mu,0}(u) = 1$. The indices $\mu - p, \ldots, \mu$ lie in $0, \ldots, n$, because $p \le \mu \le n$, so this is the whole sum over $i = 0, \ldots, n$.

*Proof of 2.* First a lemma: if $N_{i,r}(t_i) \ne 0$, then $t_i = t_{i+r}$. For $r = 0$ it is empty. For $r \ge 1$, the first term of the recursion at $u = t_i$ has the weight $\omega_{i,r}(t_i) = 0$, so $N_{i+1,r-1}(t_i) \ne 0$. By local support $t_{i+1} \le t_i$, so $t_{i+1} = t_i$, and by induction $t_{i+1} = t_{i+r}$. Now let $t_{n+1} < t_{n+p+1}$, and add knots larger than $t_{n+p+1}$ at the right end; this does not change $N_{0,p}, \ldots, N_{n,p}$, which use only $t_0, \ldots, t_{n+p+1}$. Let $\nu$ be the largest index with $t_\nu = t_{n+1}$. Then $n + 1 \le \nu \le n + p$, $u = t_{n+1}$ lies in the nonempty span $[t_\nu, t_{\nu+1})$, and the argument of part 1 gives $\sum_{i=\nu-p}^{\nu} N_{i,p}(u) = 1$ on the longer vector. A term with $i \ge n + 1$ is nonzero at $u$ only if $t_i \le u$, that is $t_i = t_{n+1}$, and then the lemma needs $t_i = t_{i+p} \ge t_{n+p+1} > t_{n+1}$, which is false. So the terms with $i \ge n + 1$ are zero, and $\nu - p \ge 1 > 0$, so the sum over $i = 0, \ldots, n$ is $1$. In the clamped case $t_{n+1} = \cdots = t_{n+p+1}$, a span $[t_i, t_{i+1})$ with $i \le n + p$ that contains $t_{n+1}$ would need $t_{i+1} > t_{n+p+1}$, which no knot is. So every $N_{i,0}(u)$ is $0$, and then every $N_{i,p}(u)$ is $0$.

*Proof of 3.* Add knots smaller than $t_0$ at the left end and larger than $t_{n+p+1}$ at the right end, and let $u$ lie in a nonempty span $\nu$ of the range. On the longer vector part 1 gives a sum of $1$ over the $p + 1$ B-splines of span $\nu$. If $u < t_p$, then $\nu \le p - 1$, and the missing B-spline with index $\nu - p < 0$ has its support $(t_{\nu-p}, t_{\nu+1})$ around $u$, because $t_{\nu-p} < t_0 \le u$. If $u > t_{n+1}$, the missing B-spline with index $n + 1 \le \nu$ has $u$ inside $(t_{n+1}, t_{n+p+2})$. A B-spline is positive inside its support, so the missing term is positive, and the sum of the true B-splines is less than $1$. $\square$

The same statement is the coefficient of $y^p$ in Marsden's identity $(y - x)^p = \sum_i \psi_{i,p}(y) N_{i,p}(x)$ with $\psi_{i,p}(y) = \prod_{r=1}^{p} (y - t_{i+r})$, which de Boor uses to prove that B-splines reproduce all polynomials of degree at most $p$ on the domain. The coefficient of $y^{p-1}$ gives $x = \sum_i t_i^{*} N_{i,p}(x)$ with the Greville abscissae $t_i^{*}$ of the [knot vector](/knot-vector/) page.

**The rational basis.** For weights $w_i > 0$, the functions $R_i = w_i N_{i,p} / \sum_j w_j N_{j,p}$ are nonnegative and sum to 1 wherever the denominator is positive. This is why a [NURBS](/nurbs/) curve keeps the convex hull property and affine invariance for any positive weights.

## Examples

**Bernstein at one point.** For $n = 2$ and $u = 1/4$ the three Bernstein values are $9/16$, $6/16$ and $1/16$, with sum $1$.

**A clamped quadratic basis.** For $p = 2$ and $t = (0, 0, 0, 1, 2, 3, 3, 3)$ the domain is $[0, 3]$. At $u = 1/2$ the basis values are $1/4, 5/8, 1/8, 0, 0$, at $u = 1$ they are $0, 1/2, 1/2, 0, 0$, and at $u = 3/2$ they are $0, 1/8, 3/4, 1/8, 0$. Each list sums to 1.

**A uniform basis outside its domain.** For $p = 2$ and $t = (0, 1, 2, 3, 4, 5, 6)$ there are four B-splines, and the domain is $[t_2, t_4] = [2, 4]$. The sum is $1/8$ at $u = 1/2$, $7/8$ at $u = 3/2$, $1$ for every $u \in [2, 4]$, $7/8$ at $u = 9/2$ and $1/8$ at $u = 11/2$. A curve drawn on $[0, 6]$ is pulled toward the origin near both ends, and moving the origin changes it there.

**The right end.** For $p = 2$:

| Knot vector | $t_{n+1}$ | $t_{n+p+1}$ | Sum at $u = t_{n+1}$ (half-open) | With the closing rule |
|---|---|---|---|---|
| $(0, 1, 2, 3, 3, 4, 5)$ | 3 | 5 | 1 | 1 |
| $(0, 1, 2, 3, 3, 3, 5)$ | 3 | 5 | 1 | 1 |
| $(0, 0, 0, 1, 2, 2, 2)$ | 2 | 2 | 0 | 1 |

The last row is the usual clamped case. Code that evaluates a clamped curve at the end of its domain without the closing rule returns the origin.

**Affine invariance at work.** For the control points $(0, 0), (1, 2), (3, 3), (5, 1), (6, 0)$ on the clamped knots above, $C(3/2) = (3, 21/8)$. Add $(1, 1)$ to each control point: the new curve point is $(4, 29/8)$, the old one moved by $(1, 1)$, because the weights $1/8, 3/4, 1/8$ sum to 1.

**Non-examples.**

- The power basis $1, u, u^2$ does not sum to 1, so the coefficients of a curve in this basis are not points, and a translation changes only the constant coefficient.
- The [Lagrange](/lagrange-interpolation/) basis and the weights of the [Catmull-Rom spline](/catmull-rom-spline/) sum to 1, so those curves are affinely invariant. But they take negative values, so they are not a partition of unity in the sense of this page, and the curves can leave the convex hull of their points.
- A rational basis with a negative weight sums to 1 where it is defined, but its denominator can be zero, and the values are not all nonnegative.

## Where it is used

- **Curve and surface design.** Every curve given by control points, [Bézier](/bezier-curve/), [B-spline](/b-spline/) or [NURBS](/nurbs/), relies on it for affine invariance and the [convex hull property](/convex-hull-property/). Tensor products of two partitions of unity are again one, so [tensor product surfaces](/tensor-product-surface/) keep both properties.
- **Evaluation algorithms.** The [de Boor algorithm](/de-boor-algorithm/) and the [de Casteljau algorithm](/de-casteljau-algorithm/) compute only convex combinations, which is the partition of unity in each step, and this keeps them stable.
- **Finite elements.** The hat functions of linear elements are a partition of unity, and the partition of unity method of Babuška and Melenk builds new element spaces by multiplying local functions by a partition of unity; see the [finite element method](/finite-element-method/).
- **Scattered data.** Shepard's method of inverse distance weighting uses weights that are a partition of unity; see [scattered data interpolation](/scattered-data-interpolation/).

## References
