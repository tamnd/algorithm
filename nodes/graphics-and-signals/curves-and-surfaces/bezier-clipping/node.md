---
tag: FFP21G
kind: algorithm
slug: bezier-clipping
name: Bezier clipping
aliases:
- Bezier clipping for intersections
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Finds where two Bezier curves meet, or the roots of a Bernstein polynomial, by cutting away parameter ranges that a convex hull test excludes. It converges quadratically at a simple intersection.
solves: [curve-intersection, real-root-isolation, ray-object-intersection]
model: real-ram
complexity:
  vars: {n: the degree, k: the number of clipping steps}
  time: {worst: O(k n^2)}
  space: {extra: O(n + k)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1990
  people: [Thomas W. Sederberg, Tomoyuki Nishita]
  note: Sederberg and Nishita published the method in Computer-Aided Design in 1990, for curve intersection and, with Kakimoto, for ray tracing of rational patches.
prereqs: [bezier-curve, convex-hull-property, de-casteljau-algorithm]
see_also: [curve-intersection, de-casteljau-algorithm, convex-hull-property, variation-diminishing-property, real-root-isolation, interval-newton-method, quadratic-convergence, line-clipping]
sources:
  - paper: "Thomas W. Sederberg and Tomoyuki Nishita, Curve intersection using Bezier clipping, Computer-Aided Design 22(9), 538-549 (1990)"
    title: Curve intersection using Bezier clipping
    locator: the fat line, the clipping of one curve against the fat line of the other, the split rule for multiple intersections, and the tighter fat lines for cubics
  - paper: doi:10.1016/j.cagd.2007.12.006
    title: Christian Schulz, Bezier clipping is quadratically convergent, Computer Aided Geometric Design 26(1), 61-74 (2009)
    locator: the proof of quadratic convergence at a transversal intersection, and of linear convergence at a tangential one
  - paper: doi:10.1109/TPAMI.1980.4766968
    title: Jeffrey M. Lane and Richard F. Riesenfeld, A theoretical development for the computer generation and display of piecewise polynomial surfaces, IEEE Transactions on Pattern Analysis and Machine Intelligence 2(1), 35-46 (1980)
    locator: the subdivision of Bezier curves and the convex hull test, which Bezier clipping refines
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 4, The de Casteljau Algorithm (subdivision), and Chapter 5, The Bernstein Form of a Bezier Curve (the convex hull property)
---

Bézier clipping finds the parameters at which two planar [Bézier curves](/bezier-curve/) meet, or the roots of a polynomial in Bernstein form. It bounds one curve by a fat line, a strip between two parallel lines, and uses the [convex hull property](/convex-hull-property/) of the other curve's distance to that strip to cut away the parameter ranges in which no intersection can be. The two curves are clipped in turn, and a curve is split in two when a clip removes too little. Thomas Sederberg and Tomoyuki Nishita published it in 1990; near a simple intersection the interval width roughly squares at each step.

## In plain words

Two curves are given by their control points, and we want the places where they cross. Put the second curve inside a narrow strip with straight sides. Every crossing must lie in this strip. Now look at how far the control points of the first curve are from the middle of the strip. These distances tell, without any guessing, which parts of the first curve can be in the strip at all. Throw the other parts away.

Then swap the roles: put the part of the first curve that is left in a strip, and cut down the second curve. Each round removes a large part of each curve, and near a crossing the parts become small very fast. If a round removes too little, for example because there are two crossings, cut the larger curve in half and treat each half alone.

## The problem

The input is two Bézier curves $P(t) = \sum_{i=0}^m P_i B_i^m(t)$ and $Q(s) = \sum_{j=0}^n Q_j B_j^n(s)$ in the plane and a tolerance $\varepsilon > 0$. The output is a list of parameter boxes $[a, b] \times [c, d]$ of width at most $\varepsilon$ in each direction, or unions of such boxes that touch, such that every intersection $P(t) = Q(s)$ with $t, s \in [0, 1]$ has $(t, s)$ in a box. This is one method for [curve intersection](/curve-intersection/).

The root finding form takes the Bernstein coefficients $c_0, \dots, c_n$ of a polynomial $f$ and returns intervals of width at most $\varepsilon$ that contain all roots of $f$ in $[0, 1]$; this is a form of [real root isolation](/real-root-isolation/) when the intervals separate. A ray against a curve is the case in which $Q$ is a line.

The model is the [real RAM](/real-ram/). The implementation uses exact fractions and rounds each new interval end outward to a dyadic grid, so that no intersection is lost and the numbers stay short.

## The algorithm

For a curve $P$ and an interval $[a, b]$, "$P$ on $[a, b]$" is the control polygon of the part of $P$ on $[a, b]$, reparametrized to $[0, 1]$. Two splits by the [de Casteljau algorithm](/de-casteljau-algorithm/) give it from the original polygon.

The fat line of $Q'$ is the strip $\{x : d_{\min} \le \ell(x) \le d_{\max}\}$, where $\ell$ is an affine function that is zero on the line through the end points of $Q'$, and $d_{\min}$, $d_{\max}$ are the smallest and the largest values of $\ell$ at the control points of $Q'$.

```pseudo id=main
BEZIER-CLIP(P, Q, ε)
L1  S ← stack with ([0,1], [0,1]); R ← empty list
L2  while S is not empty do
L3      pop ([a,b], [c,d]) from S; P' ← P on [a,b]; Q' ← Q on [c,d]
L4      if b − a ≤ ε and d − c ≤ ε then append ([a,b], [c,d]) to R; continue
L5      [u0, u1] ← FATLINE-CLIP(P', Q'); if it is empty then continue
L6      [a,b] ← [a + u0(b − a), a + u1(b − a)], rounded outward; P' ← P on [a,b]
L7      [v0, v1] ← FATLINE-CLIP(Q', P'); if it is empty then continue
L8      [c,d] ← [c + v0(d − c), c + v1(d − c)], rounded outward
L9      if no interval wider than ε shrank to 80% or less, and not both are ≤ ε, then
            split the wider interval at its midpoint and push both pairs onto S
L10     else push ([a,b], [c,d]) onto S
L11 return R, with the boxes that touch merged

FATLINE-CLIP(P', Q')                     ▷ P' has degree m
L12 ℓ ← affine function that is zero on the line through Q'_0 and Q'_n
L13 d_min, d_max ← the smallest and largest of ℓ(Q'_j)
L14 the points (i/m, ℓ(P'_i)) for i = 0, ..., m
L15 return the range of the first coordinate over hull(L14 points) ∩ {d_min ≤ y ≤ d_max}, or empty
```

The root finding form is the same loop on one interval, with the points $(i/n, c_i)$ in line L14 and the band $\{0 \le y \le 0\}$ in line L15.

## Example

**Root finding.** Let $f$ have the Bernstein coefficients $(-1, -1, 3, 2)$, so $f(t) = -9t^3 + 12t^2 - 1$. Its roots are $1/3$ and $(9 \pm \sqrt{189})/18 \approx -0.264$ and $1.264$, so $1/3$ is the only root in $[0, 1]$.

The graph of $f$ is the Bézier curve with the control points $(0, -1), (1/3, -1), (2/3, 3), (1, 2)$. Its convex hull meets the axis $y = 0$ on the edge from $(0, -1)$ to $(2/3, 3)$ at $x = 1/6$, and on the edge from $(1/3, -1)$ to $(1, 2)$ at $x = 5/9$. So every root in $[0, 1]$ is in $[1/6, 5/9]$. On this interval the coefficients are $(-17/24, -31/108, 83/162, 94/81)$, and the next clip keeps the local range $[459/1211, 655/1407]$. Without the outward rounding, the intervals are:

| step | interval | width |
|---|---|---|
| 0 | $[0, 1]$ | 1 |
| 1 | $[0.166667, 0.555556]$ | $0.389$ |
| 2 | $[0.314066, 0.347706]$ | $3.36 \cdot 10^{-2}$ |
| 3 | $[0.333164, 0.333391]$ | $2.27 \cdot 10^{-4}$ |
| 4 | $[0.33333333, 0.33333334]$ | $7.88 \cdot 10^{-9}$ |
| 5 | around $1/3$ | $9.5 \cdot 10^{-18}$ |

The width roughly squares at each step, times a constant near $0.15$: this is quadratic convergence. Bisection would need about 57 steps for the last width.

**Two parabolas.** Let $P = (0, 0), (1, 2), (2, 0)$ and $Q = (0, 1), (1, -1), (2, 1)$. They meet where $4t(1 - t) = 1 - 4s(1 - s)$ and $2t = 2s$, that is at $t = s$ with $8t^2 - 8t + 1 = 0$, so $t = s = (2 \mp \sqrt 2)/4 \approx 0.146447$ and $0.853553$. The fat line of $Q$ is $-2 \le y - 1 \le 0$. The distances of $P$'s control points are $-1, 1, -1$, and the hull of $(0, -1), (1/2, 1), (1, -1)$ meets the band at both ends, so the first clip keeps all of $[0, 1]$, and so does the clip of $Q$. The loop splits $P$ at $1/2$, and after that each half holds one intersection and converges fast. The implementation makes 18, 22 and 22 calls of FATLINE-CLIP for $\varepsilon = 2^{-10}$, $2^{-20}$ and $2^{-30}$. Subdivision with box tests on the same curves tests 213, 453 and 693 pairs of pieces: its work grows linearly in $\log(1/\varepsilon)$.

## Correctness

The invariant is: every intersection $(t^*, s^*)$ in $[0, 1]^2$ is in a box on the stack $S$ or in $R$. It holds at line L1, and each step keeps it.

- **The strip contains $Q'$.** Each point of $Q'$ is a convex combination of the control points of $Q'$, and $\ell$ is affine, so $d_{\min} \le \ell(Q(s)) \le d_{\max}$ for $s \in [c, d]$.
- **The hull contains the distance graph of $P'$.** Because the basis sums to 1, $\ell(P'(u)) = \sum_i \ell(P'_i) B_i^m(u)$, and because $\sum_i \frac im B_i^m(u) = u$, the graph $u \mapsto (u, \ell(P'(u)))$ is the Bézier curve with the control points $(i/m, \ell(P'_i))$. By the convex hull property it lies in their hull.
- **A clip keeps all intersections.** If $P(t^*) = Q(s^*)$ with $t^*$ in $[a, b]$ and $s^*$ in $[c, d]$, then $u^* = (t^* - a)/(b - a)$ has $(u^*, \ell(P'(u^*)))$ in the hull and in the band, so $u^*$ is in the range of line L15. Rounding outward only widens the range. Line L7 uses the same argument with the roles swapped. A split covers the box by two halves.
- **Line L15 is computed exactly.** The extreme points of the hull cut by the band are input points inside the band or crossings of an edge with $y = d_{\min}$ or $y = d_{\max}$. The implementation looks at all input points in the band and all crossings of segments between two input points, which are inside the set, so the minimum and maximum of these candidates are the exact range.

**Termination.** The widths never grow, because the rounded interval is cut back to the old one. Each pass of line L10 shrinks an interval wider than $\varepsilon$ to 80% or less, and each split in line L9 halves an interval wider than $\varepsilon$. An interval wider than $\varepsilon$ can shrink by these factors only about $\log_{5/4}(1/\varepsilon)$ times, so every chain of steps from the root ends after $O(\log(1/\varepsilon))$ steps, and the loop stops. The number of chains can still be large when the curves overlap along an arc, so the implementation also has a step limit. The full proof is in the proof file below.

## Complexity

One step computes two restricted polygons by de Casteljau splits, which costs $O(m^2 + n^2)$, and two clips. A clip computes the distances in $O(m + n)$ and the range in $O(m^2)$ with all pairs of points, or $O(m \log m)$ with a convex hull. So a step costs $O(n^2)$ for curves of degree $n$, and $k$ steps cost $O(k n^2)$. The stack holds $O(k)$ pairs of intervals; the polygons of one step need $O(n)$ space.

The number of steps depends on the curves. Near an intersection where the curves cross at a nonzero angle, the widths satisfy $w_{j+1} \le C w_j^2$ (Schulz 2009), so $O(\log \log (1/\varepsilon))$ steps per intersection follow after a phase that depends on the curves and not on $\varepsilon$. At a tangential intersection the convergence is only linear, and when the curves overlap along an arc the set of boxes that must be kept is a whole arc, which needs about $1/\varepsilon$ boxes.

## Properties

- **No intersection is lost.** Every discarded range is proved empty by the convex hull property. With exact arithmetic and outward rounding, the output contains all intersections.
- **Quadratic convergence at transversal intersections.** The strip has a width of order $w^2$ when the interval width is $w$, because a curve piece of length $w$ deviates from its chord by $O(w^2)$.
- **Affine invariance.** The fat line and the distances are affine constructions, so the result does not depend on the coordinate system.
- **The output can be redundant.** Close intersections give touching boxes that are merged into one, and a box may contain no intersection when the curves come within the box size of each other without meeting. A final test, such as an [interval Newton method](/interval-newton-method/), can prove that a box holds exactly one intersection.

## Variants and improvements

- **Roots of a polynomial.** For $f = \sum c_i B_i^n$, the band is $y = 0$ and the hull of $(i/n, c_i)$ gives the clip; this is the first example. Rays and curves are the same, with $\ell$ the distance to the ray.
- **Tighter fat lines.** For a quadratic, the curve stays within half of the distance of the middle control point. For a cubic with distances $d_1, d_2$ of the inner points, Sederberg and Nishita give the factor $3/4$ when $d_1 d_2 > 0$ and $4/9$ otherwise, which narrows the strip.
- **Ray tracing of patches.** For a rational surface patch and a ray, two planes through the ray give two distance functions, and the patch is clipped in both parameter directions (Nishita, Sederberg and Kakimoto 1990).
- **Higher order clipping.** Quadratic and cubic bounding strips in place of lines give convergence of order 3 and 4 at simple roots; Bartoň and Jüttler call this quadratic clipping.
- **Spline curves.** For B-spline curves, knot insertion in place of de Casteljau splits gives a similar method that works on the spline directly (Mørken, Reimers and Schulz).

## When to use it

Use it to intersect two low degree curves, to hit a ray with a curve or a patch, and to find the roots of a Bernstein polynomial in an interval, when all solutions are needed and none may be lost. It is faster than plain subdivision because it converges quadratically, and it needs no starting guess, unlike Newton's method. For one root near a good guess, [Newton's method](/newton-raphson-method/) is cheaper. For curves of degree 2 or 3 with exact data, implicitization gives the exact algebraic answer; see [curve intersection](/curve-intersection/).

## Pitfalls

- **Overlapping curves.** If the curves share an arc, every box along the arc survives, and the work grows like $1/\varepsilon$. Detect this, for example with a step limit or a test for a common arc, and report the overlap.
- **Tangential intersections.** At a tangency the clips remove little, so the method falls back to splitting and converges linearly.
- **Floating point.** A clip computed in floating point can cut away an intersection by a rounding error. Round each new interval end outward, or widen the band by an error bound.
- **Degenerate fat lines.** If the end points of $Q'$ coincide, for a closed piece, the line through them is undefined. Use the direction to another control point, or split first.
- **Growing fractions.** In exact arithmetic the denominators grow with each clip. Round the interval ends outward to short binary fractions, and compute each restricted polygon from the original control points.
- **Not the same as line clipping.** [Line clipping](/line-clipping/) cuts a segment to a window. Bézier clipping cuts parameter intervals of a curve; the two share only the word.

## Implementations

The Python file in this folder has `bezier_clip_intersect(P, Q, eps)` for two planar curves and `bezier_clip_roots(coeffs, eps)` for a Bernstein polynomial, with the helpers `restrict`, `clip_range` and `fat_line_clip`. All arithmetic is in exact fractions, and new interval ends are rounded outward to a grid of at most $\varepsilon/16$. The tests check the clip range of the example, compare the roots of random polynomials with exact Sturm isolation and with dense exact sampling, and check intersections of curves against an exact reference by implicitization, a line against a curve, disjoint curves, and the step limit on overlapping curves.

## History

Sederberg and Nishita introduced Bézier clipping in 1990 as a refinement of the subdivision methods of Lane and Riesenfeld (1980), which cut every piece in half: clipping uses the same convex hull bound, but cuts at the place where the bound says the solutions are. In the same year Nishita, Sederberg and Kakimoto used it to ray trace trimmed rational patches. Schulz proved in 2009 that the method converges quadratically at transversal intersections.

## References
