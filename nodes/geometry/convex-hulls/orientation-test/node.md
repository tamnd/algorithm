---
tag: 76WXA9
kind: concept
slug: orientation-test
name: Orientation test
aliases:
- ccw test
- ccw-test
- cross product sign test
- cross-product-sign-test
- turn test
- turn-test
- orient2d
area: geometry/convex-hulls
level: intro
summary: The sign of a 2D cross product that tells whether three points make a left turn, right turn, or are collinear.
prereqs: [cross-product, determinant]
see_also: [oriented-triangle-area, in-circle-test, general-position, andrew-monotone-chain, graham-scan, segment-intersection-detection, shewchuk-expansion-sum, catastrophic-cancellation]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, the signed area of a triangle (Area2) and the predicates Left, LeftOn and Collinear built on it
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Section 33.1, Line-segment properties (cross products and the turn test)
  - paper: doi:10.1007/PL00009321
    title: Jonathan Richard Shewchuk, Adaptive precision floating-point arithmetic and fast robust geometric predicates, Discrete and Computational Geometry 18(3), 1997
    locator: the sections on the orientation and in-circle predicates (the adaptive evaluation and its error bounds)
  - paper: doi:10.1016/j.comgeo.2007.06.003
    title: Lutz Kettner, Kurt Mehlhorn, Sylvain Pion, Stefan Schirra and Chee Yap, Classroom examples of robustness problems in geometric computations, Computational Geometry 40(1), 2008
    locator: the whole paper (float failures of the planar orientation test near the line through (12, 12) and (24, 24), and their effect on hull algorithms)
---

The orientation test of three points $p, q, r$ in the plane is the sign of the [cross product](/cross-product/) $(q - p) \times (r - p)$, which is the sign of a 2 by 2 [determinant](/determinant/). It is positive when $p, q, r$ make a left (counterclockwise) turn, negative for a right (clockwise) turn, and zero when the three points are on one line. It is the main predicate of planar [convex hull](/convex-hull/) algorithms, and with integer coordinates it can be computed exactly with a few multiplications.

## In plain words

Walk from the first point to the second, then turn and walk to the third. The test tells you whether you turned left, turned right, or went straight on. It does not measure an angle. It multiplies and subtracts the coordinates, and only the sign of the result matters.

The size of the result is twice the area of the triangle that the three points make, so a result near zero means a thin triangle. With whole-number coordinates the computer gets the sign exactly. With decimal numbers stored in floating point, small rounding errors can flip the sign for points that are almost on one line, and a program that trusts the wrong sign can crash or give a wrong hull.

## The idea

**Definition.** For points $p = (p_x, p_y)$, $q$ and $r$ in $\mathbb{R}^2$ let

$$D(p, q, r) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x) = \det \begin{pmatrix} 1 & p_x & p_y \\ 1 & q_x & q_y \\ 1 & r_x & r_y \end{pmatrix}.$$

The orientation test is $\mathrm{orient}(p, q, r) = \operatorname{sign} D(p, q, r) \in \{-1, 0, +1\}$. The value $+1$ means that $r$ lies strictly to the left of the directed line from $p$ to $q$, the value $-1$ means strictly to the right, and $0$ means that $p, q, r$ are collinear (this includes $p = q$). The second form follows from the first: subtract the first row of the 3 by 3 matrix from the other two rows and expand along the first column.

**Geometric meaning.** $D(p, q, r) = |q - p|\,|r - p| \sin \theta$, where $\theta$ is the angle from $q - p$ to $r - p$, measured counterclockwise. So $|D|/2$ is the area of the triangle $pqr$, and $D/2$ is its [signed area](/oriented-triangle-area/). Summing the signed areas of the fan triangles of a polygon gives the [shoelace formula](/shoelace-formula/).

**Algebraic rules.** These follow from the rules of determinants, for all points:

- **Cyclic shift:** $D(p, q, r) = D(q, r, p) = D(r, p, q)$.
- **Swap:** exchanging two arguments changes the sign, for example $D(q, p, r) = -D(p, q, r)$.
- **Translation:** $D(p + t, q + t, r + t) = D(p, q, r)$ for each vector $t$.
- **Linear maps:** for a 2 by 2 matrix $A$, $D(Ap, Aq, Ar) = \det(A)\, D(p, q, r)$. A rotation or a shear ($\det A = 1$) keeps every orientation, and a reflection ($\det A = -1$) reverses every orientation.

**Exactness.** $D$ is a polynomial of degree 2 in the six coordinates. If each coordinate is an integer with absolute value at most $M$, each difference has absolute value at most $2M$, so $|D| \le 8M^2$. Coordinates of $b$ binary digits therefore need about $2b + 4$ binary digits for an exact result: 64-bit integers are safe for coordinates below $2^{30}$ in absolute value, and Python integers and `fractions.Fraction` are always exact.

**Higher dimensions.** For $d + 1$ points $p_0, \ldots, p_d$ in $\mathbb{R}^d$, the orientation is the sign of the $d$ by $d$ determinant with rows $p_1 - p_0, \ldots, p_d - p_0$, or equally of the $(d+1)$ by $(d+1)$ determinant with rows $(1, p_i)$. In $\mathbb{R}^3$ it is positive exactly when $p_3$ lies on the side of the plane through $p_0, p_1, p_2$ from which these three points appear in counterclockwise order. Shewchuk's code `orient3d` uses the opposite sign convention. The [in-circle test](/in-circle-test/) is the same kind of determinant one dimension higher, by the [lifting map](/paraboloid-lifting-map/).

**What it decides.** Most planar predicates reduce to a few orientation tests:

- Two segments $ab$ and $cd$ cross at one inner point if and only if $\mathrm{orient}(a, b, c)$ and $\mathrm{orient}(a, b, d)$ are nonzero with opposite signs, and $\mathrm{orient}(c, d, a)$ and $\mathrm{orient}(c, d, b)$ are nonzero with opposite signs.
- A point $s$ lies strictly inside the triangle $pqr$ with $\mathrm{orient}(p, q, r) = +1$ if and only if $\mathrm{orient}(p, q, s)$, $\mathrm{orient}(q, r, s)$ and $\mathrm{orient}(r, p, s)$ are all $+1$.
- For points that all lie in an open half-plane whose boundary passes through $p$, "$a$ before $b$ when $\mathrm{orient}(p, a, b) = +1$" is a strict order by angle around $p$. This is the comparator of an [angular sort](/angular-sort/) without trigonometry.

**Floating point.** The rounded value of $D$ can have the wrong sign. The subtraction of the two products cancels the leading digits when the points are almost collinear (see [catastrophic cancellation](/catastrophic-cancellation/)), so the rounding errors of the products decide the result. There are three correct ways to get the sign:

1. Use integer or rational coordinates and exact arithmetic.
2. Use a floating-point filter. Shewchuk proves that if $|D_{\mathrm{float}}| > (3 + 16\varepsilon)\,\varepsilon\,(|\ell| + |r|)$, where $\ell$ and $r$ are the two computed products and $\varepsilon = 2^{-53}$ for IEEE double precision, then the computed sign is correct. Only the rare inputs that fail the filter go to an exact or [adaptive](/shewchuk-expansion-sum/) evaluation.
3. Use an adaptive predicate, such as Shewchuk's `orient2d`, which does both steps for you.

A tolerance, such as "treat $|D| < 10^{-9}$ as zero", is not a fix. It makes "collinear" a relation that is not transitive, so an algorithm can see three points as collinear in one test and as a strict turn in another test on the same points, and its invariants break.

## Examples

**Basic signs.** With $p = (0, 0)$ and $q = (4, 0)$:

| $r$ | $D(p, q, r)$ | orientation |
|---|---|---|
| $(2, 1)$ | $4 \cdot 1 - 0 \cdot 2 = 4$ | left turn, $+1$ |
| $(2, -3)$ | $4 \cdot (-3) - 0 \cdot 2 = -12$ | right turn, $-1$ |
| $(7, 0)$ | $0$ | collinear |

For $p = (1, 1)$, $q = (4, 2)$, $r = (2, 5)$: $D = 3 \cdot 4 - 1 \cdot 1 = 11$, so the triangle has area $5.5$ and its vertices run counterclockwise.

**Three dimensions.** For $p_0 = (0,0,0)$, $p_1 = (1,0,0)$, $p_2 = (0,1,0)$ the determinant with $p_3 = (0,0,1)$ is $1$, with $p_3 = (0,0,-2)$ it is $-2$, and with $p_3 = (3,4,0)$ it is $0$ (the four points are coplanar).

**A float failure.** Take $q = (12, 12)$, $r = (24, 24)$ and $p = (0.5 + 41u,\ 0.5 + 48u)$ with $u = 2^{-53}$. Both coordinates of $p$ are double-precision numbers, since the spacing of doubles in $[0.5, 1)$ is $u$. Expanding $D$ gives exactly $D(p, q, r) = 12\,(p_y - p_x) = 12 \cdot 7u = 84u \approx 9.33 \times 10^{-15} > 0$, a left turn. The same formula in double precision returns $-5.68 \times 10^{-14}$, a right turn. For $p = (0.5, 0.5 + u)$ the exact value is $12u > 0$ but the double-precision result is exactly $0$. Over the $256 \times 256$ grid of points $p = (0.5 + iu, 0.5 + ju)$ with $0 \le i, j < 256$, the double-precision sign is wrong for 11972 of the 65536 points. These are the inputs that Kettner and others use to break textbook hull programs.

**The fix.** Convert each float to an exact rational before the arithmetic. In Python, `Fraction(0.5 + 41 * 2**-53)` is the exact value of the double, and the formula with `Fraction` inputs returns $84 \cdot 2^{-53}$, with the right sign. On the same grid of 65536 points, the filter of item 2 above accepts the float sign for 11340 points, and each of those signs is correct. The other 54196 points need the exact evaluation, because these inputs are chosen to be almost collinear.

## Where it is used

- Planar hull algorithms use it as their only geometric predicate: [Graham scan](/graham-scan/), [Andrew's monotone chain](/andrew-monotone-chain/), [Jarvis march](/jarvis-march/), [quickhull](/quickhull/), [divide-and-conquer hull](/divide-and-conquer-convex-hull/), [Melkman's algorithm](/melkman-algorithm/) and [Chan's algorithm](/chan-algorithm/).
- The 3D test drives [3D hull algorithms](/convex-hull-3d/) and the [beneath-beyond method](/beneath-beyond/): a point sees a facet when it lies on the outer side of the facet's plane.
- Segment problems: [segment intersection detection](/segment-intersection-detection/), the [Shamos-Hoey algorithm](/shamos-hoey-algorithm/) and the [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/).
- Polygons: [polygon orientation](/polygon-orientation/), [point in convex polygon](/point-in-convex-polygon/), [ear clipping](/ear-clipping/), and [point in polygon](/point-in-polygon/) by the [winding number](/winding-number-algorithm/).
- Degenerate cases are the inputs where some orientation test returns $0$. The [general position](/general-position/) assumption excludes them.
- Exact predicates by expansion arithmetic: [Shewchuk's expansion sum](/shewchuk-expansion-sum/) and the [error-free transformations](/error-free-transformations/).

## References
