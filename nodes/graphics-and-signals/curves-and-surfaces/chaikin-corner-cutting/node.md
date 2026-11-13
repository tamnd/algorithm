---
tag: A2HW9B
kind: algorithm
slug: chaikin-corner-cutting
name: Chaikin corner cutting
aliases:
- Chaikin's algorithm
- Chaikin's corner cutting algorithm
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: Replaces each edge of a polygon by its points at 1/4 and 3/4. Repeated, it converges to the uniform quadratic B-spline curve of the polygon.
solves: [curve-from-control-polygon]
model: real-ram
complexity:
  vars: {m: the number of points of the closed polygon, k: the number of rounds, d: the dimension of the points}
  time: {worst: Θ(m 2^k d), best: Θ(m 2^k d)}
  space: {extra: Θ(m 2^k d)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1974
  people: [George M. Chaikin, Richard F. Riesenfeld]
  note: Chaikin gave the method in 1974 as a fast way to draw curves, and Riesenfeld showed in 1975 that the limit is the uniform quadratic B-spline.
prereqs: [control-points, b-spline]
see_also: [lane-riesenfeld-algorithm, four-point-scheme, doo-sabin-subdivision, knot-refinement, boehm-knot-insertion, de-casteljau-algorithm, variation-diminishing-property, convex-hull-property]
sources:
  - paper: doi:10.1016/0146-664X(74)90028-8
    title: George Merrill Chaikin, An algorithm for high-speed curve generation, Computer Graphics and Image Processing 3(4), 346-349 (1974)
    locator: the corner cutting rule with the ratios 1/4 and 3/4, repeated until the polygon looks smooth
  - paper: "Richard F. Riesenfeld, On Chaikin's algorithm, Computer Graphics and Image Processing 4(3), 304-310 (1975)"
    locator: the identification of the limit curve with the uniform quadratic B-spline
  - paper: doi:10.1109/TPAMI.1980.4766968
    title: Jeffrey M. Lane and Richard F. Riesenfeld, A theoretical development for the computer generation and display of piecewise polynomial surfaces, IEEE Transactions on Pattern Analysis and Machine Intelligence 2(1), 35-46 (1980)
    locator: the general scheme of doubling and averaging, which for degree 2 is Chaikin's rule
  - book: isbn:9781558604469
    title: Joe Warren and Henrik Weimer, Subdivision Methods for Geometric Design, A Constructive Approach, Morgan Kaufmann, 2002
    locator: Chapter 2, An Integral Approach to Uniform Subdivision, for the refinement relation of the uniform B-splines
---

Chaikin corner cutting makes a polygon smooth by cutting off its corners. Each round replaces every edge $P_i P_{i+1}$ by the two points $\tfrac34 P_i + \tfrac14 P_{i+1}$ and $\tfrac14 P_i + \tfrac34 P_{i+1}$, so a closed polygon of $m$ points becomes one of $2m$ points. The polygons converge to the uniform quadratic [B-spline](/b-spline/) curve with the input as [control points](/control-points/), and after $k$ rounds they are within $D / (8 \cdot 4^k)$ of it, where $D$ is the largest second difference of the input. It is the simplest curve subdivision scheme and the degree 2 case of the [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/).

## In plain words

Take a polygon and cut every corner off with a straight cut. Each cut goes from a point one quarter along one edge to a point one quarter along the next edge, measured from the corner. The polygon now has twice as many corners, and each of them is less sharp. Do it again, and again.

After a few rounds the polygon looks like a smooth curve, and it stops changing in a visible way. That curve is a well known smooth curve, and it does not depend on how many rounds you do. The curve does not pass through the original corners. It stays inside the convex hull of the polygon and passes through the middle of each edge.

## The problem

The input is a closed polygon $P_0, \dots, P_{m-1}$ in $\mathbb{R}^d$, with indices modulo $m$, and a number of rounds $k \ge 0$. The output is the polygon after $k$ rounds, with $m 2^k$ points. The aim is to approximate the uniform quadratic B-spline curve of the polygon, which is a piecewise quadratic curve of degree $p = 2$ with $m$ control points, $m$ spans and continuous tangents. This is one method for the [curve from a control polygon](/curve-from-control-polygon/) problem. For an open polyline of $n$ points the same rule applies to the $n - 1$ edges, and each round gives $2(n - 1)$ points.

The model is the [real RAM](/real-ram/), and an operation on a point costs $O(d)$. The weights are dyadic fractions, so with integer input the output is exact in rational arithmetic.

## The algorithm

```pseudo id=main
CHAIKIN(P_0, ..., P_(m−1), k)
L1  for r ← 1 to k do
L2      Q ← an empty list
L3      for i ← 0 to m − 1 do
L4          A ← P_i, B ← P_((i+1) mod m)
L5          append 3/4 A + 1/4 B and then 1/4 A + 3/4 B to Q
L6      P ← Q, m ← 2m
L7  return P
```

So point $2i$ of the new polygon is $\tfrac34 P_i + \tfrac14 P_{i+1}$ and point $2i + 1$ is $\tfrac14 P_i + \tfrac34 P_{i+1}$. For an open polyline, line L3 stops at $m - 2$, and the end points are lost.

## Example

Take the square $P_0 = (0, 0)$, $P_1 = (4, 0)$, $P_2 = (4, 4)$, $P_3 = (0, 4)$. The edge from $(0, 0)$ to $(4, 0)$ gives $(1, 0)$ and $(3, 0)$, and the other edges give the rest of an octagon with edges of length 2 and $\sqrt2$:

$$(1, 0), (3, 0), (4, 1), (4, 3), (3, 4), (1, 4), (0, 3), (0, 1).$$

The second round cuts the edge from $(1, 0)$ to $(3, 0)$ into $(3/2, 0)$ and $(5/2, 0)$, and the edge from $(3, 0)$ to $(4, 1)$ into $(13/4, 1/4)$ and $(15/4, 3/4)$. It has 16 points, and the third round has 32.

The limit curve has 4 quadratic spans. The span at the corner $(4, 0)$ starts at the edge midpoint $(2, 0)$, ends at $(4, 2)$, and has $(4, 0)$ as its middle Bézier control point. Its point at the middle of the span is $\tfrac18 (P_0 + 6 P_1 + P_2) = (7/2, 1/2)$. The distance from the center $(2, 2)$ is $2$ at $(2, 0)$ and $3\sqrt2/2 \approx 2.121$ at $(7/2, 1/2)$, so the limit is not a circle. The second difference at each corner is $(-4, 4)$ up to sign and rotation, so $D = 4 \sqrt2$, and the distance between the polygon and the curve is at most $D / 8 \approx 0.707$ at the start, $0.177$ after one round and $0.044$ after two. At the corner $(4, 0)$ the start bound is reached exactly.

## Correctness

The uniform quadratic B-spline $N_2$ satisfies the refinement relation $N_2(x) = \tfrac14 N_2(2x) + \tfrac34 N_2(2x - 1) + \tfrac34 N_2(2x - 2) + \tfrac14 N_2(2x - 3)$. It follows from $N_0(x) = N_0(2x) + N_0(2x - 1)$ for the box function and the fact that $N_2$ is the convolution of three box functions. Put this into $C(x) = \sum_i P_i N_2(x - i)$ and collect the terms: the coefficient of $N_2(2x - j - 2)$ is point $j$ of the new polygon. So one round is the insertion of a knot in the middle of every span, and it does not change the curve. This is [knot refinement](/knot-refinement/), and the tests check it against [Boehm knot insertion](/boehm-knot-insertion/) in exact arithmetic.

Each span of $C$ is a quadratic Bézier curve with the control points $M_i, P_{i+1}, M_{i+1}$, where $M_i$ is the midpoint of the edge $P_i P_{i+1}$. Its largest distance from the two half edges is $|P_i - 2 P_{i+1} + P_{i+2}| / 8$. One round divides every second difference by exactly 4. So after $k$ rounds the polygon is within $D / (8 \cdot 4^k)$ of the curve. The full proofs are in the proof file below.

## Complexity

Round $r$ processes $m 2^{r-1}$ edges and writes $m 2^r$ points, with 4 multiplications and 2 additions per coordinate and point pair. The sum over $k$ rounds is less than $2 m 2^k$ points, so the time is $\Theta(m 2^k d)$, and the output itself takes $\Theta(m 2^k d)$ space. The error drops by the factor 4 in each round while the size doubles. To reach the error $\eta$, about $k = \log_4 (D / (8 \eta))$ rounds are needed, so the output has about $m \sqrt{D / (8 \eta)}$ points.

## Properties

- **The limit is $C^1$.** The uniform quadratic B-spline has continuous tangents but jumps in its curvature at the span ends, the edge midpoints.
- **Not interpolating.** The curve passes through the edge midpoints $M_i$ and touches the polygon there, but it does not pass through the input points. A convex polygon shrinks.
- **[Convex hull property](/convex-hull-property/).** Each new point is a convex combination of two old points, so every polygon and the curve lie in the convex hull of the input.
- **[Variation diminishing](/variation-diminishing-property/).** A line crosses the new polygon at most as often as the old one, because cutting a corner can only remove crossings.
- **Affine invariance.** The weights sum to 1, so the rule commutes with affine maps.
- **Local.** A new point depends on one edge, and a point of the curve depends on 3 control points.
- **The ends of an open polyline.** The open form loses the end points, and the curve runs from $M_0$ to $M_{n-2}$.

## Variants and improvements

- **Keep the end points.** For open polylines, output $P_0$, then only the inner cut point of the first edge, the two cut points of the inner edges, the inner cut point of the last edge and $P_{n-1}$. The ends stay fixed, and the first and the last edge keep their direction.
- **Higher degree.** The [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/) doubles the points and averages $p$ times, which gives the uniform B-spline of degree $p$. Chaikin's rule is the case $p = 2$, and $p = 3$ gives a $C^2$ cubic curve.
- **Interpolating schemes.** The [four-point scheme](/four-point-scheme/) keeps the old points and inserts new ones, so the limit passes through the input.
- **Surfaces.** On a grid of quads, Chaikin's rule in both directions gives the biquadratic B-spline surface. [Doo-Sabin subdivision](/doo-sabin-subdivision/) extends it to meshes of any topology.
- **Other ratios.** Cutting at other fractions than $\tfrac14$ also gives a limit curve, but in general it is not a quadratic B-spline. The ratio $\tfrac14$ is the one that comes from the refinement relation.

## When to use it

Use it to smooth a polyline for display, such as a hand drawn stroke, a path from a planner or a coarse outline, when the curve does not need to pass through the points. It is the right choice when you want a smooth curve with a few lines of code and exact control of the error. If the curve must pass through the points, use an interpolating scheme. If you need $C^2$ smoothness, use the cubic case of the [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/). To evaluate the curve at a given parameter, use the [de Boor algorithm](/de-boor-algorithm/) on the B-spline instead.

## Pitfalls

- **Expecting interpolation.** The curve cuts inside convex corners. Users who place points on a shape see it shrink.
- **Lost end points.** The open form drops $P_0$ and $P_{n-1}$ in the first round. Use the variant that keeps them, or repeat each end point.
- **Exponential size.** Each round doubles the points. Ten rounds turn 100 points into 102400, far more than a screen needs. Stop at the error you need.
- **The closing edge.** For a closed polygon, the edge from $P_{m-1}$ back to $P_0$ must be cut too. If it is not, the polygon opens at that point.
- **Duplicate points.** Two equal consecutive points give a zero edge and two equal new points. The curve is still correct, but code that divides by an edge length fails.

## Implementations

The Python file in this folder has `chaikin(points, rounds, closed)`, which follows the pseudocode, `chaikin_keep_ends(points, rounds)` for the variant with fixed ends, and `second_difference_max(points)` for the error bound. The tests compare one and two rounds with the control points of the uniform quadratic B-spline after Boehm insertion of all half and quarter knots, in exact fractions, and they check the factor 4 of the second differences, the bound on the distance, the open form and affine invariance on random polygons.

## History

George Chaikin presented the method in 1974 as a fast way to generate curves on a display, with repeated corner cutting in place of the evaluation of polynomials. In 1975 Richard Riesenfeld showed that the limit curve is the uniform quadratic B-spline. In 1980 Jeffrey Lane and Riesenfeld extended the idea to B-splines of every degree and to surfaces, with the doubling and averaging scheme that carries their names. Chaikin's rule became the model for curve subdivision, and the biquadratic case led to the Doo-Sabin surface scheme of 1978.

## References
