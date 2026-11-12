---
tag: 3DQ7H1
kind: concept
slug: variation-diminishing-property
name: Variation diminishing property
aliases:
- variation diminishing
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: A Bezier or B-spline curve crosses any line (any plane in space) at most as often as its control polygon does. So the curve does not wiggle more than its polygon.
prereqs: [control-points, bernstein-polynomials, descartes-rule-of-signs]
see_also: [convex-hull-property, b-spline, boehm-knot-insertion, chaikin-corner-cutting, lane-riesenfeld-algorithm, de-casteljau-algorithm, sturm-sequence, bezier-clipping]
sources:
  - paper: "I. J. Schoenberg, On variation diminishing approximation methods, in R. E. Langer (ed.), On Numerical Approximation, University of Wisconsin Press, Madison, 1959"
    title: On variation diminishing approximation methods
    locator: pages 249-274, the variation diminishing spline approximation by totally positive kernels
  - paper: doi:10.1016/0021-9045(83)90111-9
    title: Jeffrey M. Lane and Richard F. Riesenfeld, A geometric proof for the variation diminishing property of B-spline approximation, Journal of Approximation Theory 37(1), 1-4 (1983)
    locator: the proof by knot insertion and the variation diminishing property of piecewise linear interpolation
  - paper: doi:10.1016/0167-8396(92)90011-D
    title: Hartmut Prautzsch and Timothy Gallagher, Is there a geometric variation diminishing property for B-spline or Bezier surfaces?, Computer Aided Geometric Design 9(2), 119-124 (1992)
    locator: the examples that show that the simple geometric forms fail for tensor product and triangular surfaces
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 5, The Bernstein Form of a Bezier Curve, and Chapter 8, B-Spline Curves (the variation diminishing property)
  - book: isbn:9783540437611
    title: Hartmut Prautzsch, Wolfgang Boehm and Marco Paluszny, Bezier and B-Spline Techniques, Springer, 2002
    locator: Chapter 3, Bezier techniques (subdivision and the variation diminishing property)
---

The variation diminishing property says that a [Bézier curve](/bezier-curve/) or a [B-spline](/b-spline/) curve crosses any line in the plane, or any plane in space, at most as often as its control polygon does. For a polynomial in Bernstein form, the same fact says that the number of roots in $(0, 1)$ is at most the number of sign changes of its coefficients. So the curve is a smoothed form of its polygon: it never oscillates more than the polygon. The usual proofs use total positivity, after Schoenberg, or corner cutting, after Lane and Riesenfeld.

## In plain words

Draw a straight line across a curve and its control polygon. Count how many times the line cuts through the polygon, and how many times it cuts through the curve. The second count is never larger than the first.

This is a statement about wiggles, not about position. It means that the curve cannot have a bump or a wave that the polygon does not have. If the broken line of control points goes up all the time, the curve goes up all the time. If the broken line is convex, the curve is convex. So a designer who sees a calm polygon knows that the curve is calm too.

## The idea

**The statement.** Let $C(t) = \sum_{i=0}^n P_i B_i^n(t)$ for $t \in [0, 1]$ and let $H$ be a line in the plane or a hyperplane in $\mathbb{R}^d$ that does not contain the whole curve. Then the number of times the curve crosses $H$ is at most the number of times the polygon $P_0 P_1 \cdots P_n$ crosses $H$. The same holds for a B-spline curve with its de Boor points, and for rational curves with positive weights.

**The function form.** Write $H = \{x : \ell(x) = 0\}$ with an affine function $\ell$. Because the basis sums to 1, $\ell(C(t)) = \sum_i \ell(P_i) B_i^n(t)$. So a crossing of $H$ is a sign change of the polynomial $f(t) = \sum_i c_i B_i^n(t)$ with $c_i = \ell(P_i)$, and the polygon crosses $H$ at least $S^-(c)$ times, where $S^-(c)$ is the number of strict sign changes in the sequence $c_0, \dots, c_n$, zeros ignored. The curve form follows from the function form: for $f \not\equiv 0$,

$$Z_{(0,1)}(f) \le S^-(c_0, \dots, c_n),$$

where $Z_{(0,1)}$ counts the roots in $(0, 1)$ with multiplicity.

**Proof by Descartes' rule.** For $t \in (0, 1)$ put $s = t / (1 - t)$, which maps $(0, 1)$ onto $(0, \infty)$ one to one and increasing. Then $f(t) = (1 - t)^n \sum_i \binom{n}{i} c_i s^i$. The factor $(1 - t)^n$ has no root in $(0, 1)$, and the binomial coefficients are positive, so the sign changes of the coefficients $\binom{n}{i} c_i$ are those of $c$. By [Descartes' rule of signs](/descartes-rule-of-signs/), the number of positive roots of the polynomial in $s$, with multiplicity, is at most $S^-(c)$ and differs from it by an even number. The same is true for $f$ on $(0, 1)$.

**Proof by corner cutting.** This proof works for the crossings themselves and carries over to B-splines.

1. *Cutting corners does not add sign changes.* Let $c_0, \dots, c_m$ be values, and let $x_j$ be a number between $c_j$ and $c_{j+1}$ for each $j$. Then $S^-(c_0, x_0, x_1, \dots, x_{m-1}, c_m) \le S^-(c)$. Proof. Insert each $x_j$ between $c_j$ and $c_{j+1}$: a value between two neighbors adds no strict sign change, so $S^-$ is unchanged. Then delete $c_1, \dots, c_{m-1}$: deleting entries never adds a strict sign change.
2. *Subdivision is corner cutting.* In round $r$ of the [de Casteljau algorithm](/de-casteljau-algorithm/), the points $b_i^r$ lie on the edges $b_i^{r-1} b_{i+1}^{r-1}$, one per edge, in order. Replace the inner part $b_0^{r-1}, \dots, b_{n-r+1}^{r-1}$ of the current polygon by $b_0^{r-1}, b_0^r, \dots, b_{n-r}^r, b_{n-r+1}^{r-1}$. After $n$ rounds the polygon is the left half followed by the right half. Apply $\ell$ and step 1 in each round: the joined polygon of the two halves has at most $S^-(c)$ sign changes.
3. *Pass to the limit.* Repeat the split on all pieces. If $f$ has $k$ sign changes, there are parameters $\tau_0 < \dots < \tau_k$ in $(0, 1)$ at which $f$ has alternating strict signs. After enough rounds, the control points of the piece that contains $\tau_j$ are all close to $C(\tau_j)$, because the pieces shrink to points and lie in the hulls of their control points. So the refined polygon has values with the same alternating signs, and $k \le S^-(c)$.

**B-splines.** [Knot insertion](/boehm-knot-insertion/) computes each new de Boor point as a convex combination of two neighbor old points, one new point per edge of a range of edges, so step 1 applies. Under repeated insertion the polygons converge to the curve, and step 3 applies. This is the proof of Lane and Riesenfeld (1983). The older proofs, which go back to Schoenberg (1959), use total positivity: the B-spline collocation matrices $\big(N_{j,p}(t_i)\big)$ for $t_0 < t_1 < \cdots$ have only nonnegative minors, and a totally positive basis is variation diminishing.

**Rational curves.** For $R(t) = \sum_i w_i P_i B_i^n(t) / \sum_i w_i B_i^n(t)$ with all $w_i > 0$, the denominator is positive, so $\ell(R(t))$ has the sign of $\sum_i w_i \ell(P_i) B_i^n(t)$. The coefficients $w_i \ell(P_i)$ have the same signs as $\ell(P_i)$, and the property holds.

**Consequences.**

- If the coefficients $c_i$ are monotone, $f$ is monotone, and if they are convex, $f$ is convex. Both follow from $f' = n \sum_i \Delta c_i B_i^{n-1}$ and $f'' = n (n - 1) \sum_i \Delta^2 c_i B_i^{n-2}$.
- A planar control polygon that is convex together with its closing edge $P_n P_0$ gives a convex curve: a line meets this closed polygon at most twice, so it meets the closed curve (the curve plus the same edge) at most twice.
- In the plane, a line meets a Bézier curve at most $n$ times, by the function form, unless it contains the curve.
- If $S^-(c) = 0$, $f$ has no root in $(0, 1)$. If $S^-(c) = 1$, $f$ has exactly one simple root there, by the parity part of Descartes' rule.

**A different property.** The [convex hull property](/convex-hull-property/) bounds the region of the curve, and this property bounds the number of its crossings. The convex hull property follows from nonnegativity and the sum 1 alone. The variation diminishing property needs more, namely total positivity of the basis in the order of the points. The convex hull page has a basis with the first and not the second.

**Surfaces.** For tensor product Bézier and B-spline surfaces and for Bézier triangles, the simple geometric forms of the property, with planes and the control net, fail (Prautzsch and Gallagher 1992).

## Examples

- **One sign change.** The cubic with the coefficients $(-1, -1, 3, 2)$ is $f(t) = -9t^3 + 12t^2 - 1$. There is one sign change, so $f$ has exactly one root in $(0, 1)$. It is $t = 1/3$; the other two roots, $(9 \pm \sqrt{189})/18 \approx -0.264$ and $1.264$, are outside the interval.
- **The bound is reached.** The coefficients $(1, -1, 1)$ give $f(t) = (1 - t)^2 - 2t(1 - t) + t^2 = (2t - 1)^2$. There are two sign changes and a double root at $t = 1/2$.
- **The bound is not reached.** The coefficients $(1, -1/2, 1)$ give $f(t) = 1 - 3t + 3t^2 > 0$. There are two sign changes and no root, a difference of 2, which is even, as Descartes' rule says.
- **An arch and two lines.** The curve with the control points $(0, 0), (1, 2), (2, 0)$ is the arch $(2t, 4t(1 - t))$ with top $(1, 1)$. The line $y = 1/2$ crosses the polygon twice and the curve twice. The line $y = 3/2$ crosses the polygon twice and the curve not at all.
- **Non-example: polynomial interpolation.** The cubic that interpolates the values $0, 0, 0, 1$ at $t = 0, 1/3, 2/3, 1$ is $L(t) = \frac92\, t (t - \frac13)(t - \frac23)$, and $L(1/2) = -1/16$. The data polygon through $(0, 0), (1/3, 0), (2/3, 0), (1, 1)$ never goes below the line $y = -1/32$, but the graph of $L$ crosses it twice. An interpolating basis has negative functions and is not variation diminishing.

## Where it is used

- **Design.** Shape preservation: monotone, convex or calm data polygons give monotone, convex or calm curves. This is the main reason that Bézier and B-spline curves are used in design rather than interpolating polynomials.
- **Root isolation.** Counting the sign changes of the Bernstein coefficients bounds the roots in an interval. With subdivision this gives a root isolation method, the Bernstein form of the Descartes method, and an alternative to [Sturm sequences](/sturm-sequence/).
- **Intersection with lines.** The number of hits of a ray with a planar curve is at most the number of polygon crossings. [Bézier clipping](/bezier-clipping/) and subdivision methods use this to stop early: a piece whose distance coefficients have no sign change has no hit.
- **Spline approximation.** Schoenberg's variation diminishing spline approximation $\sum_i f(\xi_i) N_{i,p}$ at the Greville points $\xi_i$ does not oscillate more than $f$, in the same way.

## References
