---
tag: 9E0B9K
kind: problem
slug: curve-intersection
name: Curve intersection
aliases:
- intersecting parametric curves
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Given two parametric curves, such as Bezier curves, find all parameter pairs at which they meet. Methods are subdivision with hull tests, Bezier clipping and implicitization.
model: real-ram
complexity:
  vars: {n: the degree of each curve, k: the number of pairs of pieces tested}
  time: {worst: O(k n^2)}
prereqs: [parametric-curve, bezier-curve]
see_also: [bezier-clipping, convex-hull-property, resultant, real-root-isolation, polynomial-system-solving, segment-intersection-point, ray-object-intersection, newton-method-for-systems]
sources:
  - paper: doi:10.1109/TPAMI.1980.4766968
    title: Jeffrey M. Lane and Richard F. Riesenfeld, A theoretical development for the computer generation and display of piecewise polynomial surfaces, IEEE Transactions on Pattern Analysis and Machine Intelligence 2(1), 35-46 (1980)
    locator: the subdivision of Bezier curves and the intersection test by the convex hull of the control points
  - paper: "Thomas W. Sederberg and Tomoyuki Nishita, Curve intersection using Bezier clipping, Computer-Aided Design 22(9), 538-549 (1990)"
    title: Curve intersection using Bezier clipping
    locator: the fat line clipping method and its comparison with subdivision and implicitization
  - paper: doi:10.1016/0734-189X(84)90140-3
    title: Thomas W. Sederberg, David C. Anderson and Ronald N. Goldman, Implicit representation of parametric curves and surfaces, Computer Vision, Graphics, and Image Processing 28(1), 72-84 (1984)
    locator: the implicit equation of a parametric polynomial or rational curve by the resultant, its degree, and the inversion formula for the parameter
  - paper: "Thomas W. Sederberg and Scott R. Parry, Comparison of three curve intersection algorithms, Computer-Aided Design 18(1), 58-63 (1986)"
    title: Comparison of three curve intersection algorithms
    locator: the timings of Bezier subdivision, interval subdivision and implicitization for curves of low degree
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 4, The de Casteljau Algorithm (subdivision), and Chapter 5, The Bernstein Form of a Bezier Curve (the convex hull property)
---

Curve intersection is the problem of finding all points where two [parametric curves](/parametric-curve/) meet, given as the pairs of parameters $(t, s)$ with $P(t) = Q(s)$. It is a basic step of CAD, of Boolean operations on regions with curved edges and of ray tracing. For [Bézier curves](/bezier-curve/) there are three main methods: subdivision with convex hull tests, [Bézier clipping](/bezier-clipping/) and implicitization, which turns the problem into the roots of one polynomial. The hard cases are tangent curves, curves that share an arc and intersections that are very close together.

## In plain words

Two curves are drawn on a page, and we want every place where they cross or touch. Each curve is given by a few control points, and a number along the curve tells where we are on it. The answer is a list of pairs of such numbers, one on each curve, that give the same point.

A computer cannot test every point. It uses facts that hold for whole pieces of curve: a piece lies inside a simple region around its control points, so two pieces whose regions do not overlap cannot meet. Cutting the curves into smaller and smaller pieces and throwing away the far pieces finds all crossings. Another way is to turn one curve into an equation and put the other curve into it, which leaves one equation in one unknown.

## Definition

**Input.** Two curves $P, Q : [0, 1] \to \mathbb{R}^2$. In the main case they are Bézier curves $P(t) = \sum_{i=0}^m P_i B_i^m(t)$ and $Q(s) = \sum_{j=0}^n Q_j B_j^n(s)$ with control points in the plane. A tolerance $\varepsilon > 0$ can also be given.

**Output.** The set $Z = \{(t, s) \in [0, 1]^2 : P(t) = Q(s)\}$. Since the coordinates are roots of polynomials, an algorithm in the [real RAM](/real-ram/) cannot in general give them exactly. So the usual output is a list of boxes $[a, b] \times [c, d]$ of width at most $\varepsilon$ whose union contains $Z$, or exact algebraic numbers, given as a polynomial with an isolating interval.

**The overlap case.** If the curves share an arc, $Z$ contains a curve segment and is infinite. A correct method must detect this and report the overlap, not a list of points.

**Multiplicity.** At a transversal intersection the tangents $P'(t)$ and $Q'(s)$ are not parallel, and the intersection is stable under small changes of the control points. At a tangential intersection they are parallel, and a small change can split the point into two or remove it.

## Variants

- **Ray or line against a curve.** If $Q$ is a line $\ell(x) = 0$, the problem is the roots of $\ell(P(t))$, a polynomial in Bernstein form of degree $m$. This is the 2D case of [ray-object intersection](/ray-object-intersection/), and the case $m = n = 1$ is [segment intersection](/segment-intersection-point/).
- **Self-intersection.** The pairs $t < t'$ with $P(t) = P(t')$. Split $P$ into pieces without loops, for example at the points where the hodograph turns by more than a half turn, and intersect the pieces.
- **Rational curves and splines.** For [rational Bézier curves](/rational-bezier-curve/) the hull test uses the hull of the control points when the weights are positive, and the implicit equation exists in the same way. B-spline curves are split into Bézier pieces by knot insertion first.
- **Space curves and surfaces.** Two curves in 3D rarely meet, so the question is usually the closest points. The intersection of two surfaces is a curve, and surface-surface intersection is a harder problem with the same tools.
- **Detection only.** Decide whether the curves meet at all, which needs only the first box that survives with a proof that it contains an intersection.

## Examples

**Two parabolas, by implicitization.** Let $P = (0, 0), (1, 2), (2, 0)$ and $Q = (0, 1), (1, -1), (2, 1)$. Then $P(t) = (2t, 4t(1 - t))$ and $Q(s) = (2s, (1 - 2s)^2)$. The implicit equation of $Q$ is $y = (1 - x)^2$: the resultant in $s$ of $2s - x$ and $(1 - 2s)^2 - y$ is $4\big((1 - x)^2 - y\big)$. Put $P(t)$ into it:
$$g(t) = 4t(1 - t) - (1 - 2t)^2 = -8t^2 + 8t - 1.$$
The roots are $t = (2 \mp \sqrt 2)/4 \approx 0.146447$ and $0.853553$. The inverse of $Q$ is $s = x/2$, so $s = t$ at both points.

**The same curves, by subdivision and by clipping.** The bounding box method of Lane and Riesenfeld tests 213, 453 and 693 pairs of pieces for $\varepsilon = 2^{-10}$, $2^{-20}$ and $2^{-30}$: about 24 more tests for each halving of $\varepsilon$, so its work grows linearly in $\log(1/\varepsilon)$. Bézier clipping needs 18, 22 and 22 clips, because it converges quadratically.

**The most intersections.** Let $T_k$ be the [Chebyshev polynomials](/chebyshev-polynomials/). The curve $y = T_m(x)$ and the curve $x = T_n(y)$, for $x$ and $y$ in $[-1, 1]$, are polynomial curves of degrees $m$ and $n$. They meet where $x = T_n(T_m(x)) = T_{mn}(x)$; the last step holds because $T_k(\cos\theta) = \cos(k\theta)$. With $x = \cos\theta$, $\theta \in [0, \pi]$, this is $\cos(mn\theta) = \cos\theta$, so $\theta = 2\pi j/(mn - 1)$ or $\theta = 2\pi j/(mn + 1)$. Counting these values in $[0, \pi]$, and removing the ones that both forms give, leaves exactly $mn$ values. So the curves meet in $mn$ points, the most that is possible. For $m = 2$, $n = 4$ the box method with $\varepsilon = 2^{-12}$ returns 9 boxes, and one of them contains no intersection: the curves cross at a small angle there, and the boxes of two near pieces overlap. Bézier clipping returns 8 boxes.

**Tangency and overlap.** The parabola $(0, 0), (1, 1), (2, 0)$ touches the line $y = 1/2$ at $t = 1/2$; subdivision still finds it, but $g$ has a double root, and a small change of the line removes the intersection. A curve against itself makes every box along the curve survive, and the number of boxes grows like $1/\varepsilon$.

## Known algorithms

| Method | Idea | Convergence | Notes |
|---|---|---|---|
| Subdivision with hull or box tests (Lane, Riesenfeld 1980) | split both curves in half, drop pairs whose hulls or boxes are disjoint | linear: the width halves per level | simple and robust; many pairs near shallow crossings |
| [Bézier clipping](/bezier-clipping/) (Sederberg, Nishita 1990) | clip each curve against a fat line around the other | quadratic at transversal intersections | split when a clip removes too little |
| Implicitization (Sederberg, Anderson, Goldman 1984) | write $Q$ as $f(x, y) = 0$ by a [resultant](/resultant/), solve $f(P(t)) = 0$ | exact, then [root isolation](/real-root-isolation/) | best for low degree; the degree of $f(P(t))$ is $mn$ |
| [Newton's method for systems](/newton-method-for-systems/) | solve $P(t) - Q(s) = 0$ from a start point | quadratic near a simple root | needs a start; may miss solutions; good to refine |
| [Interval Newton method](/interval-newton-method/) | certify that a box has exactly one solution | quadratic | used after subdivision or clipping |
| [Polynomial system solvers](/polynomial-system-solving/) | Gröbner bases, [homotopy continuation](/homotopy-continuation/) | exact or path tracking | general, for two equations in two unknowns |

The roots of $g$ can be isolated with [Sturm sequences](/sturm-sequence/) or with [Descartes' rule of signs](/descartes-rule-of-signs/) on the Bernstein coefficients. Sederberg and Parry compared subdivision, interval subdivision and implicitization in 1986 and found implicitization the fastest for curves of low degree.

## Bounds

- **At most $mn$ intersections.** A polynomial curve $Q$ of degree $n$ lies on an algebraic curve $f(x, y) = 0$ of degree at most $n$ (Sederberg, Anderson and Goldman). So the parameters $t$ of the intersections are roots of $g(t) = f(P(t))$, a polynomial of degree at most $mn$. If $g$ is not identically zero, there are at most $mn$ values of $t$. If $g \equiv 0$, all of $P$ lies on the algebraic curve of $Q$, which is the overlap case. The Chebyshev example shows that the bound $mn$ is reached; it is the bound of Bézout's theorem for plane curves.
- **Cost per test.** A split by the de Casteljau algorithm costs $O(n^2)$ and a box or hull test $O(n)$ or $O(n \log n)$, so $k$ tests cost $O(k n^2)$. This is the bound in the front matter. The number $k$ depends on the curves and on $\varepsilon$: for subdivision it is $O(\log(1/\varepsilon))$ per transversal intersection after a start phase that depends on the curves, for clipping it is $O(\log\log(1/\varepsilon))$, and for an overlap it is of order $1/\varepsilon$ for every method that returns boxes.
- **Output size.** The output can have $mn$ boxes, so every method needs $\Omega(mn)$ time to write it.
- **Conditioning.** Where $g$ has a root of multiplicity $r$, a change of size $\delta$ in the data can move the intersection by about $\delta^{1/r}$, so no method can give it to better than that accuracy in floating point.

## Reductions

- **From root finding.** The roots in $[0, 1]$ of $f = \sum_i c_i B_i^n$ are the intersections of the graph curve with the control points $(i/n, c_i)$ and the line $y = 0$. So curve intersection is at least as hard as [polynomial root finding](/polynomial-root-finding/) on an interval.
- **To root finding.** Implicitization reduces the intersection of two polynomial curves to the real roots of $g$, of degree $mn$, followed by the inversion of $Q$ at each point.
- **To a polynomial system.** The equations $P_x(t) = Q_x(s)$ and $P_y(t) = Q_y(s)$ are two polynomial equations in two unknowns, and every method for [polynomial systems](/polynomial-system-solving/) applies.
- **To collision tests.** The box test is the same test that [bounding volume hierarchies](/bounding-volume-hierarchy/) use in [collision detection](/collision-detection/), applied to pieces of curve.

## Applications

- CAD: trimming of curves and surfaces, fillets, and the Boolean operations of solid modeling, which need the points where boundary curves cross.
- Rendering of filled shapes with curved edges: the crossings of a ray with the edges decide whether a point is inside.
- Ray tracing of curves and surfaces, where the ray is the second curve.
- Path planning and machining, where an offset curve is intersected with itself to remove loops.

## References
