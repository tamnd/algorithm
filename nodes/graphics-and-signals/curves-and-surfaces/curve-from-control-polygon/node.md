---
tag: F0AQS1
kind: problem
slug: curve-from-control-polygon
name: Curve generation from a control polygon
aliases:
- curve subdivision from control points
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: Given a control polygon and a tolerance, produce a polyline (or a finer control polygon) that is within the tolerance of the Bezier or B-spline curve of the polygon.
model: real-ram
complexity:
  vars: {n: the degree, m: the number of output segments}
  time: {worst: O(m n)}
prereqs: [control-points, bezier-curve]
see_also: [curve-evaluation, de-casteljau-algorithm, chaikin-corner-cutting, lane-riesenfeld-algorithm, oslo-algorithm, four-point-scheme, surface-tessellation, surface-from-control-mesh]
sources:
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 4, The de Casteljau Algorithm (subdivision), Chapter 5, The Bernstein Form of a Bezier Curve, and Chapter 8, B-Spline Curves (knot insertion)
  - book: isbn:9783540437611
    title: Hartmut Prautzsch, Wolfgang Boehm and Marco Paluszny, Bezier and B-Spline Techniques, Springer, 2002
    locator: Section 3.3, Subdivision (page 27), Section 3.4, Convergence under subdivision (page 29), and Section 3.6, Curve generation by forward differences (page 32)
  - paper: doi:10.1109/TPAMI.1980.4766968
    title: Jeffrey M. Lane and Richard F. Riesenfeld, A theoretical development for the computer generation and display of piecewise polynomial surfaces, IEEE Transactions on Pattern Analysis and Machine Intelligence 2(1), 35-46 (1980)
    locator: the subdivision of Bezier and uniform B-spline curves and surfaces for display
  - paper: doi:10.1016/0146-664X(74)90028-8
    title: George M. Chaikin, An algorithm for high speed curve generation, Computer Graphics and Image Processing 3(4), 346-349 (1974)
    locator: the corner cutting rule with the ratios 1/4 and 3/4
  - paper: "Daniel Filip, Robert Magedson and Robert Markot, Surface algorithms using bounds on derivatives, Computer Aided Geometric Design 3(4), 295-311 (1986)"
    title: Surface algorithms using bounds on derivatives
    locator: the number of segments of a piecewise linear approximation from a bound on the second derivative
---

Curve generation from a control polygon is the problem of turning the [control points](/control-points/) of a [Bézier curve](/bezier-curve/) or a [B-spline](/b-spline/) curve into something that a screen, a plotter or a milling machine can use: a polyline within a tolerance $\varepsilon$ of the curve. One way samples the curve at chosen parameters. The other way refines the control polygon by subdivision until the polygon itself is close enough. The main cost measure is the number of segments needed for $\varepsilon$, which is of order $\varepsilon^{-1/2}$.

## In plain words

A curve is stored as a few points that shape it. A screen can only draw short straight lines. So a program must replace the curve by many short lines that stay close to it, closer than a given small distance.

There are two ways. You can compute many points on the curve and join them. Or you can repeatedly cut the corners of the broken line of control points. Each cut makes the broken line shorter at the corners and closer to the curve, and after a few rounds it looks smooth. The second way is called subdivision. It needs only averages of points, and it can stop early where the curve is almost straight.

## Definition

**Input.** A control polygon $P_0, \dots, P_n$ in $\mathbb{R}^d$, a curve type (Bézier of degree $n$, or B-spline of degree $p$ with a [knot vector](/knot-vector/), or the rational forms), and a tolerance $\varepsilon > 0$.

**Output.** A polyline $V_0, V_1, \dots, V_m$ such that the curve $C$ and the polyline are within distance $\varepsilon$ of each other, piece by piece: there are parameters $0 = t_0 < t_1 < \dots < t_m = 1$ such that each point of $C$ on $[t_{j-1}, t_j]$ is within $\varepsilon$ of the segment $V_{j-1} V_j$. In the subdivision form, the output is a set of control polygons, one for each piece, each within $\varepsilon$ of its own chord.

**Cost model.** The [real RAM](/real-ram/), with the cost given as a function of $n$, $m$ and $\varepsilon$.

This page is the task. The control points and their properties are on [control points](/control-points/). The computation of single points is [curve evaluation](/curve-evaluation/).

## Variants

- **Evaluation or refinement.** The output vertices are curve points, or the output is a finer control polygon of the same curve. Refinement keeps an exact description of the curve; sampling does not.
- **Uniform or adaptive.** The same step everywhere, or more segments where the curve bends more.
- **Approximating or interpolating schemes.** Corner cutting such as [Chaikin's algorithm](/chaikin-corner-cutting/) converges to a B-spline curve that in general misses the control points. An interpolating scheme such as the [four-point scheme](/four-point-scheme/) keeps all old points and converges to a curve through them; that curve is not a polynomial spline.
- **Tolerance measure.** The distance between the curve and the polyline, or the angle between neighbor segments, or the size of a pixel after projection.
- **Surfaces.** The same task for a control net or mesh is [surface tessellation](/surface-tessellation/) and [surface generation from a control mesh](/surface-from-control-mesh/).

## Examples

Use $M = \max_i \lVert \Delta^2 P_i \rVert$, the largest second difference $P_{i+2} - 2P_{i+1} + P_i$ of the polygon.

- **A quadratic by sampling.** For $P = (0, 0), (1, 2), (2, 0)$, the curve is $B(t) = (2t, 4t(1 - t))$ and $B'' = (0, -8)$. With $N$ equal parameter steps, the chord error is at most $\frac{1}{8} N^{-2} \cdot 8 = N^{-2}$ (bound 1 below). For $\varepsilon = 0.01$, $N = 10$ segments suffice; the true largest distance is about $0.0098$.
- **The same quadratic by subdivision.** One split at $t = 1/2$ gives the polygons $(0, 0), (1/2, 1), (1, 1)$ and $(1, 1), (3/2, 1), (2, 0)$. The second difference falls from $(0, -4)$ to $(0, -1)$. With the test "each inner control point is within $\varepsilon$ of the chord", $\varepsilon = 0.01$ needs depth 4 and 16 pieces, and $\varepsilon = 0.001$ needs 58 pieces with depth at most 6. The true errors are about $0.0039$ and $0.0005$, because the test is conservative.
- **A cubic.** For $P = (0, 0), (1, 2), (3, 2), (4, 0)$, the second differences are $(1, -2)$ and $(-1, -2)$, so $M = \sqrt 5$, and $\lVert B'' \rVert \le 6 \sqrt 5$. Bound 1 gives $N = 13$ for $\varepsilon = 0.01$; the true error with 13 steps is about $0.0089$, and with 12 steps it is about $0.0104$, so the bound is close here. After one split at $1/2$, the halves have the second differences $(1/4, -1/2), (0, -1/2)$ and $(0, -1/2), (-1/4, -1/2)$, one quarter of the old ones in norm or less.
- **Chaikin on a square.** The closed polygon $(0, 0), (4, 0), (4, 4), (0, 4)$ becomes, after one round with the ratios $1/4$ and $3/4$, the octagon $(1, 0), (3, 0), (4, 1), (4, 3), (3, 4), (1, 4), (0, 3), (0, 1)$. The polygons converge to the closed uniform quadratic B-spline curve of the square. This curve passes through the edge midpoints, such as $(2, 0)$, and through $(7/2, 1/2)$ near the corner $(4, 0)$.

## Known algorithms

- **Sample, then join.** Choose parameters and use a method from [curve evaluation](/curve-evaluation/): the [de Casteljau algorithm](/de-casteljau-algorithm/), the Bernstein Horner scheme, or forward differencing on an even grid, which costs $O(n)$ additions per point. For $m$ segments the cost is $O(m n)$ operations in $\mathbb{R}^d$.
- **Recursive subdivision with a flatness test.** Split the Bézier polygon at $t = 1/2$ by the de Casteljau triangle, which costs $O(n^2)$, until each piece passes the test, and output the chords (Lane and Riesenfeld 1980). The pieces are adaptive: flat parts stop early.
- **Uniform B-spline subdivision.** For uniform knots, one round of refinement doubles the knots by averaging. Degree 2 is [Chaikin's corner cutting](/chaikin-corner-cutting/) (Chaikin 1974; Riesenfeld showed in 1975 that the limit is the quadratic B-spline). For degree $p$, the [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/) doubles the points and then takes $p$ rounds of midpoint averages. A round costs $O(p)$ per point.
- **Knot insertion for general knots.** [Boehm knot insertion](/boehm-knot-insertion/) adds one knot at a time, and the [Oslo algorithm](/oslo-algorithm/) and [knot refinement](/knot-refinement/) add many at once. After enough insertions, each span is a Bézier piece with its own control polygon.
- **Interpolating subdivision.** The [four-point scheme](/four-point-scheme/) inserts one point per edge from four old points and keeps the old points.

## Bounds

Let $B$ be a Bézier curve of degree $n \ge 2$ and $M = \max_i \lVert \Delta^2 P_i \rVert$.

1. **Uniform sampling.** $N \ge \sqrt{n (n - 1) M / (8 \varepsilon)}$ equal parameter steps give a polyline within $\varepsilon$ of the curve (Filip, Magedson and Markot 1986). Proof. On a parameter interval $[a, b]$ of length $h$, let $e(t) = B(t) - L(t)$, where $L$ is the linear interpolant of $B$ at $a$ and $b$. Then $e(a) = e(b) = 0$ and $e'' = B''$, so $e(t) = -\int_a^b G(t, s) B''(s)\, ds$ with the Green function $G(t, s) = (t - a)(b - s)/h$ for $t \le s$ and $(s - a)(b - t)/h$ for $s \le t$. Since $G \ge 0$ and $\int_a^b G(t, s)\, ds = (t - a)(b - t)/2 \le h^2/8$, we get $\lVert e(t) \rVert \le \frac{h^2}{8} \max \lVert B'' \rVert$. The second derivative is a Bézier curve with the control vectors $n (n - 1) \Delta^2 P_i$, and by the [convex hull property](/convex-hull-property/) its norm is at most $n (n - 1) M$. With $h = 1/N$, the bound is at most $\varepsilon$.
2. **Second differences shrink by 4.** If $Q_0, \dots, Q_n$ is one half of the polygon after a split at $t = 1/2$, then $\max_j \lVert \Delta^2 Q_j \rVert \le M/4$. Proof. For the left half, $L(u) = B(u/2)$, so $L''(u) = \frac14 B''(u/2)$. The control vectors of $L''$ are $n (n - 1) \Delta^2 Q_j$. The curve $u \mapsto B''(u/2)$ is the left half of the Bézier curve $B''$, whose control vectors are $n (n - 1) \Delta^2 P_i$; by the [de Casteljau algorithm](/de-casteljau-algorithm/) the control vectors of this half are convex combinations of those vectors. Bernstein coefficients are unique, so each $\Delta^2 Q_j$ is $\frac14$ times a convex combination of the $\Delta^2 P_i$. The right half is the same with the order reversed.
3. **Distance of the polygon from its chord.** With $L_i = P_0 + \frac{i}{n} (P_n - P_0)$, $\lVert P_i - L_i \rVert \le \frac{i (n - i)}{2} M \le \frac{n^2}{8} M$. Proof. The vectors $e_i = P_i - L_i$ satisfy $e_0 = e_n = 0$ and $\Delta^2 e_{i-1} = \Delta^2 P_{i-1}$. The discrete Green function $G_{ij} = i (n - j)/n$ for $i \le j$ and $j (n - i)/n$ for $i \ge j$ gives $e_i = -\sum_{j=1}^{n-1} G_{ij} \Delta^2 P_{j-1}$, with $G_{ij} \ge 0$ and $\sum_j G_{ij} = i (n - i)/2$, because $g_i = i (n - i)/2$ solves $\Delta^2 g = -1$ with $g_0 = g_n = 0$.
4. **Adaptive subdivision.** The test "each control point is within $\varepsilon$ of the chord $P_0 P_n$" is sound: the distance to a segment is a convex function, and each curve point is a convex combination of the control points, so the curve is also within $\varepsilon$ of the chord. By bounds 2 and 3, every piece at depth $k$ passes once $\frac{n^2}{8} M\, 4^{-k} \le \varepsilon$. So the recursion stops at depth $k = \lceil \log_4 (n^2 M / (8 \varepsilon)) \rceil$ or earlier, with at most $2^k < 2 n \sqrt{M / (8 \varepsilon)}$ pieces. For the quadratic and the cubic of the examples, the formula gives depth 4 at $\varepsilon = 0.01$ and depth 6 at $\varepsilon = 0.001$, and the recursion reaches these depths.
5. **Order $\varepsilon^{-1/2}$ is needed.** Along a curve with curvature at least $\kappa > 0$, a chord of length $\ell$ has a distance of about $\kappa \ell^2 / 8$ from the arc for small $\ell$. So a polyline with vertices on a curve of length $\Lambda$ needs about $\Lambda \sqrt{\kappa / (8 \varepsilon)}$ segments, and bounds 1 and 4 are optimal in their dependence on $\varepsilon$.

For a B-spline curve the same bounds hold on each Bézier span, with the Bézier polygon of the span in place of $P$.

## Reductions

- Sampling reduces the problem to [curve evaluation](/curve-evaluation/) at $m + 1$ parameters, chosen by bound 1 or adaptively.
- A B-spline curve reduces to Bézier pieces by knot insertion, and a rational curve to a polynomial curve in homogeneous coordinates, followed by division. The bounds of the polynomial case do not carry over directly, because the division distorts distances.
- The surface problem reduces to the curve problem in each parameter direction for a [tensor product surface](/tensor-product-surface/).

## Applications

- Drawing Bézier paths and font outlines in vector graphics, where the tolerance is a fraction of a pixel.
- Tool paths for numerically controlled machines, where the tolerance is the machining accuracy.
- The first stage of [curve intersection](/curve-intersection/) by subdivision, and of offsets and arc length estimates, which work on the polyline.
- Smoothing of polylines in cartography and user interfaces by corner cutting.

## References
