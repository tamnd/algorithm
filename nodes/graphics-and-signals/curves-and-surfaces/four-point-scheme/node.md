---
tag: YTR0BT
kind: algorithm
slug: four-point-scheme
name: Four-point scheme
aliases:
- Dyn-Levin-Gregory scheme
- four-point interpolatory subdivision scheme
- DLG four-point scheme
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: An interpolating curve subdivision scheme that keeps old points and inserts (1/2 + w)(P_i + P_(i+1)) - w(P_(i-1) + P_(i+2)) on each edge. C1 for w in a range around 1/16.
solves: [curve-interpolation]
model: real-ram
complexity:
  vars: {m: the number of points of the closed polygon, k: the number of rounds}
  time: {worst: Θ(m 2^k), best: Θ(m 2^k)}
  space: {extra: Θ(m 2^k)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1987
  people: [Nira Dyn, David Levin, John A. Gregory]
  note: Dyn, Levin and Gregory published the scheme with a tension parameter in 1987. Dubuc had studied the case w = 1/16 in 1986.
prereqs: [lagrange-interpolation, control-points]
see_also: [chaikin-corner-cutting, lane-riesenfeld-algorithm, butterfly-subdivision, catmull-rom-spline, polynomial-interpolation, curve-interpolation, cubic-spline-interpolation, spectral-radius]
sources:
  - paper: doi:10.1016/0167-8396(87)90001-X
    title: Nira Dyn, David Levin and John A. Gregory, A 4-point interpolatory subdivision scheme for curve design, Computer Aided Geometric Design 4(4), 257-268 (1987)
    locator: the rule with the tension w, convergence for |w| < 1/4, the C1 proof for 0 < w < 1/8, and the reproduction of cubics for w = 1/16
  - paper: "Serge Dubuc, Interpolation through an iterative scheme, Journal of Mathematical Analysis and Applications 114(1), 185-204 (1986)"
    locator: the dyadic interpolation by local cubic polynomials, which is the case w = 1/16
  - paper: "Nira Dyn, John A. Gregory and David Levin, Analysis of uniform binary subdivision schemes for curve design, Constructive Approximation 7, 127-147 (1991)"
    locator: the analysis by difference schemes and symbols, with the C1 range of the four-point scheme extended to 0 < w < (5^(1/2) - 1)/8
  - paper: "Jochen Hechler, Bernhard Mößner and Ulrich Reif, C1-continuity of the generalized four-point scheme, Linear Algebra and its Applications 430(11-12), 3019-3029 (2009)"
    locator: the exact C1 range 0 < w < 0.19273..., the real root of 32 w^3 + 4 w - 1 = 0
  - paper: doi:10.1017/S0962492902000028
    title: Nira Dyn and David Levin, Subdivision schemes in geometric modelling, Acta Numerica 11, 73-144 (2002)
    locator: interpolatory schemes, the four-point scheme as the basic example, and the convergence analysis by symbols
---

The four-point scheme is a curve subdivision scheme that keeps the old points and inserts one new point on each edge. The new point between $P_i$ and $P_{i+1}$ is $(\tfrac12 + w)(P_i + P_{i+1}) - w(P_{i-1} + P_{i+2})$, a weighted average of the four nearest points with a tension $w$. Because old points never move, the limit curve passes through all of them, which the B-spline schemes such as [Chaikin corner cutting](/chaikin-corner-cutting/) do not do. The limit is continuous for $|w| < \tfrac14$ and $C^1$ for $0 < w < 0.19273$, and the standard choice $w = \tfrac1{16}$ inserts the value of the local cubic interpolant.

## In plain words

Keep every point of the polygon where it is. On each edge, put a new point near the middle of the edge, pushed a little outwards. How far it moves depends on the next point before the edge and the next point after it, so the new point follows the bend of the polygon. Now you have twice as many points, and you repeat.

The old points never move, so the curve you get goes through every point you started with. After a few rounds the polygon looks smooth. A small setting controls how much each new point is pushed. With no push you keep the straight polygon. With the usual push, the new point is where a smooth cubic curve through the four nearby points would put it.

## The problem

The input is a closed polygon $P_0, \dots, P_{m-1}$ in $\mathbb{R}^s$, $m \ge 3$, with indices modulo $m$, a tension $w$ and a number of rounds $k$. The output is the polygon after $k$ rounds, with $m 2^k$ points, in which old point $i$ has index $i 2^k$. The aim is a smooth closed curve through all input points, which is one way to solve the [curve interpolation](/curve-interpolation/) problem without solving a linear system. The limit curve is not a polynomial or a spline. It is defined only by the scheme, and its values are known exactly at the dyadic parameters $i / 2^k$.

The model is the [real RAM](/real-ram/), with the dimension $s$ fixed. With a rational $w$ and rational input, the output is exact.

## The algorithm

```pseudo id=main
FOUR-POINT(P_0, ..., P_(m−1), w, k)
L1  for r ← 1 to k do
L2      for i ← 0 to m − 1 do
L3          Q_(2i) ← P_i
L4          Q_(2i+1) ← (1/2 + w)(P_i + P_(i+1)) − w (P_(i−1) + P_(i+2))       ▷ indices mod m
L5      P ← Q, m ← 2m
L6  return P
```

For $w = \tfrac1{16}$ the weights of line L4 are $-\tfrac1{16}, \tfrac9{16}, \tfrac9{16}, -\tfrac1{16}$. These are the Lagrange weights of the nodes $-1, 0, 1, 2$ at $\tfrac12$, so the new point is the value at the middle of the edge of the cubic through the four points, as in [Lagrange interpolation](/lagrange-interpolation/). For an open polyline, the end edges have no outer neighbour. The simplest rule skips them, so a round keeps $P_1, \dots, P_{n-2}$ and maps $n$ points to $2n - 5$. Other rules add a point outside each end by extrapolation.

## Example

Take the square $P_0 = (0, 0)$, $P_1 = (4, 0)$, $P_2 = (4, 4)$, $P_3 = (0, 4)$ and $w = \tfrac1{16}$. The new point on the edge from $(0, 0)$ to $(4, 0)$ uses $P_3 = (0, 4)$ before the edge and $P_2 = (4, 4)$ after it:

$$\tfrac9{16} \big((0, 0) + (4, 0)\big) - \tfrac1{16} \big((0, 4) + (4, 4)\big) = (\tfrac{36}{16} - \tfrac4{16},\ 0 - \tfrac8{16}) = (2, -\tfrac12).$$

The first round gives the 8 points

$$(0, 0), (2, -\tfrac12), (4, 0), (\tfrac92, 2), (4, 4), (2, \tfrac92), (0, 4), (-\tfrac12, 2).$$

The second round inserts $(29/32, -13/32)$ between $(0, 0)$ and $(2, -\tfrac12)$, and $(99/32, -13/32)$ between $(2, -\tfrac12)$ and $(4, 0)$. Every point that is computed stays in all later rounds. So the limit curve passes through the corners, at distance $2\sqrt2 \approx 2.828$ from the center $(2, 2)$, and through $(2, -\tfrac12)$, at distance $2.5$. After 6 rounds the lowest point has $y = -4097/8192$, a little below $-\tfrac12$, so the curve is not a circle and it bulges out of the square. [Chaikin corner cutting](/chaikin-corner-cutting/) on the same square gives a curve inside the square, which misses the corners.

## Correctness

Line L3 keeps each point at the same parameter, so the limit passes through every point that any round computes. The weights of line L4 sum to 1 and are symmetric, so linear data stay linear for every $w$. For $w = \tfrac1{16}$ the weights are the cubic Lagrange weights, so samples of a cubic polynomial stay samples of the same cubic in every round. For $f(t) = t^2$ at $-1, 0, 1, 2$ the rule gives $\tfrac12 - 4w$, which is $f(\tfrac12) = \tfrac14$ only for $w = \tfrac1{16}$, so no other tension reproduces quadratics.

For convergence, the new edge vectors are $\tfrac12 d_i \pm w (d_{i-1} - d_{i+1})$, where $d_i = P_{i+1} - P_i$. So the longest edge shrinks by at least the factor $\mu = \tfrac12 + 2|w|$, which is less than 1 for $|w| < \tfrac14$. Each round moves the polygon by at most $2|w|$ times the longest edge, so the polygons form a Cauchy sequence and converge uniformly to a continuous curve. The full proofs are in the proof file below. The proof of $C^1$ smoothness needs the scheme for the divided differences over two or more rounds, and the page cites it.

## Complexity

A round on $N$ points writes $N$ copies and $N$ new points, each with 4 point additions and 2 scalar multiplications, so it costs $\Theta(N)$. The sizes are $m, 2m, \dots, 2^{k-1} m$, so $k$ rounds cost $\Theta(m 2^k)$ in the worst and in the best case, and the output takes $\Theta(m 2^k)$ space. The distance between the polygon and the limit after $k$ rounds is at most $\frac{2|w|}{1 - \mu} \mu^k$ times the longest input edge. For $w = \tfrac1{16}$ we have $\mu = \tfrac58$, and the bound is $\tfrac13 (\tfrac58)^k$ times the longest edge. This bound is a worst case bound, and on smooth data the error is much smaller, because the new points are cubic interpolants.

## Properties

- **Interpolating.** The limit passes through all input points and all points of all rounds.
- **Smoothness depends on $w$.** The limit is continuous for $|w| < \tfrac14$. It is $C^1$ for $0 < w < \omega^*$, where $\omega^* \approx 0.19273$ is the real root of $32\omega^3 + 4\omega - 1 = 0$ (Hechler, Mößner and Reif 2009). The 1987 paper proved $C^1$ for $0 < w < \tfrac18$, and the 1991 analysis extended it to $(\sqrt5 - 1)/8 \approx 0.1545$. No tension gives a $C^2$ limit for general data.
- **Tension.** For $w = 0$ the scheme inserts midpoints, and the limit is the polygon. Small $w$ keeps the curve tight to the polygon, and larger $w$ makes it rounder.
- **Polynomial reproduction.** Linear functions for every $w$, and cubic polynomials for $w = \tfrac1{16}$ only.
- **No convex hull property.** The weight $-w$ is negative for $w > 0$, so the curve can leave the convex hull of the input, as the square example shows. It can also add wiggles to data with sharp turns.
- **Local.** A new point depends on 4 old points, and the limit near a point depends on a few neighbours only.
- **Affine invariance.** The weights sum to 1, so the scheme commutes with affine maps.

## Variants and improvements

- **Dubuc's scheme.** The case $w = \tfrac1{16}$, studied by Dubuc in 1986, is dyadic interpolation by local cubics. The $2n$-point schemes of Deslauriers and Dubuc use polynomials of degree $2n - 1$ and give smoother limits.
- **Open polylines.** The end edges need extra points. Common choices are linear extrapolation $2P_0 - P_1$ or the cubic extrapolation from the first four points.
- **Surfaces.** The [butterfly subdivision](/butterfly-subdivision/) scheme of the same authors is the triangle mesh version. On a boundary edge it uses this four-point rule with $w = \tfrac1{16}$.
- **Approximating schemes.** The [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/) gives $C^{d-1}$ curves, but they do not pass through the input. The four-point scheme trades smoothness for interpolation.
- **Non-stationary and nonlinear versions.** Tensions that change from round to round reproduce conics and circles, and nonlinear rules avoid the wiggles near sharp turns. See the survey of Dyn and Levin.

## When to use it

Use it when a smooth curve must pass through given points, such as the vertices of a sketch or keyframes of a path, and a $C^1$ curve is enough. It needs no linear system, unlike [cubic spline interpolation](/cubic-spline-interpolation/), and it is local, so moving one point changes only a short part of the curve. A [Catmull-Rom spline](/catmull-rom-spline/) gives a $C^1$ interpolating curve with a closed form at every parameter. If you need $C^2$ or the convex hull property, use an approximating B-spline scheme.

## Pitfalls

- **A tension outside the range.** For $w \ge \tfrac14$ the scheme can diverge, and between $0.19273$ and $\tfrac14$ the limit is continuous but not $C^1$. Use $w = \tfrac1{16}$ unless there is a reason not to.
- **Overshoot.** Near sharp corners or very uneven point spacing, the negative weights add bumps. The curve can leave the convex hull and cross itself.
- **Open ends.** The rule needs two points on each side of the edge. Without a rule for the ends, the curve gets shorter in each round.
- **Uneven spacing.** The scheme assumes that the points are evenly spaced in parameter. If the input has very different edge lengths, the curve has loops or flat parts, as with a uniform parametrization in other interpolants.
- **Expecting $C^2$.** The limit is not twice differentiable for any $w$, so it is not a good choice where curvature must be continuous.

## Implementations

The Python file in this folder has `four_point(points, rounds, w, closed)`, which follows the pseudocode for closed polygons and skips the end edges of open polylines. The tests check that old points stay at their indices, compare each new point for $w = \tfrac1{16}$ with the cubic through the four neighbours by Neville's method, check that samples of random cubics stay exact samples over two rounds, and check the value $\tfrac12 - 4w$ for $t^2$, all in exact fractions.

## History

Serge Dubuc studied in 1986 the dyadic interpolation in which each new value comes from the cubic through the four nearest values. In 1987 Nira Dyn, David Levin and John Gregory introduced the scheme with a tension parameter $w$ for curve design. They proved convergence and $C^1$ smoothness for a range of $w$, and the paper became the starting point of the theory of interpolating subdivision. They extended the idea to the butterfly scheme for surfaces in 1990. The range of $C^1$ tensions was extended in 1991, and its exact end point was found by Hechler, Mößner and Reif in 2009.

## References
