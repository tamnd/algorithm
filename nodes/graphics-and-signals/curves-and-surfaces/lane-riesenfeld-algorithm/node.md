---
tag: DS8H6B
kind: algorithm
slug: lane-riesenfeld-algorithm
name: Lane-Riesenfeld algorithm
aliases:
- Lane-Riesenfeld subdivision
- Lane-Riesenfeld refinement
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Refines a uniform B-spline control polygon of degree d by doubling every point and then taking midpoints of neighbours d times. The polygons converge to the curve.
solves: [curve-from-control-polygon, knot-refinement]
model: real-ram
complexity:
  vars: {m: the number of points of the closed polygon, k: the number of rounds, d: the degree}
  time: {worst: Θ(d m 2^k), best: Θ(d m 2^k)}
  space: {extra: Θ(m 2^k)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1980
  people: [Jeffrey M. Lane, Richard F. Riesenfeld]
  note: Lane and Riesenfeld published the doubling and averaging scheme for uniform B-spline curves and tensor product surfaces of any degree in 1980.
prereqs: [b-spline, knot-refinement]
see_also: [chaikin-corner-cutting, four-point-scheme, boehm-knot-insertion, oslo-algorithm, de-boor-algorithm, catmull-clark-subdivision, convolution, convex-hull-property]
sources:
  - paper: doi:10.1109/TPAMI.1980.4766968
    title: Jeffrey M. Lane and Richard F. Riesenfeld, A theoretical development for the computer generation and display of piecewise polynomial surfaces, IEEE Transactions on Pattern Analysis and Machine Intelligence 2(1), 35-46 (1980)
    locator: the subdivision of uniform B-splines by doubling and repeated averaging, its convergence, and the tensor product form for surfaces
  - paper: "Richard F. Riesenfeld, On Chaikin's algorithm, Computer Graphics and Image Processing 4(3), 304-310 (1975)"
    locator: the quadratic case, Chaikin's rule as subdivision of the uniform quadratic B-spline
  - book: isbn:9781558604469
    title: Joe Warren and Henrik Weimer, Subdivision Methods for Geometric Design, A Constructive Approach, Morgan Kaufmann, 2002
    locator: Chapter 2, An Integral Approach to Uniform Subdivision, for the B-spline refinement relation from repeated convolution, and Chapter 3, Convergence Analysis for Uniform Subdivision Schemes, for the difference schemes
  - paper: doi:10.1017/S0962492902000028
    title: Nira Dyn and David Levin, Subdivision schemes in geometric modelling, Acta Numerica 11, 73-144 (2002)
    locator: the symbol of a curve scheme, the factor (1 + z) and the convergence of the difference schemes
---

The Lane-Riesenfeld algorithm refines the control polygon of a uniform [B-spline](/b-spline/) curve of degree $d$. One round doubles every control point and then replaces each point by the midpoint of it and the next point, $d$ times. The result is the control polygon of the same curve on knots with half the spacing, so it is [knot refinement](/knot-refinement/) at all midpoints at once, with only additions and halvings. Repeated rounds converge to the curve, and the error drops by the factor 4 per round for $d \ge 2$.

## In plain words

Write every point of the polygon twice. Then walk around the list and put each point halfway to the next one. Do that walk a fixed number of times, the degree of the curve. You get a polygon with twice as many points, which hugs the curve more closely than the old one.

One walk on the doubled list just adds the edge midpoints. Two walks give the corner cutting rule of Chaikin. Three walks give the cubic B-spline, which is the most common smooth curve in design programs. More walks give smoother curves that stay further from the polygon. Each round is cheap, and the curve itself never changes, so you can stop at any round.

## The problem

The input is a closed polygon $P_0, \dots, P_{m-1}$ of control points in $\mathbb{R}^s$, with indices modulo $m$, a degree $d \ge 0$ and a number of rounds $k \ge 0$. The polygon describes the periodic uniform B-spline curve of degree $p = d$ with $m$ control points,

$$C(x) = \sum_{i \in \mathbb{Z}} P_i N_d(x - i),$$

where $N_d$ is the uniform B-spline with knots $0, 1, \dots, d + 1$. The output is the control polygon of the same curve after $k$ rounds of midpoint refinement, with $m 2^k$ points, so that $C(x) = \sum_j R_j N_d(2^k x - j - c)$ for a fixed shift $c$. This solves [knot refinement](/knot-refinement/) for uniform knots and the [curve from a control polygon](/curve-from-control-polygon/) problem.

The model is the [real RAM](/real-ram/), with the dimension $s$ fixed. Each midpoint is one addition and one halving per coordinate, so integer input gives exact dyadic output.

## The algorithm

```pseudo id=main
LANE-RIESENFELD(P_0, ..., P_(m−1), d, k)
L1  for r ← 1 to k do
L2      Q_j ← P_(⌊j/2⌋) for j = 0, ..., 2m − 1      ▷ double every point
L3      for s ← 1 to d do
L4          Q_j ← (Q_j + Q_((j+1) mod 2m)) / 2 for all j, from the old values
L5      P ← Q, m ← 2m
L6  return P
```

After one round, point $j$ is

$$R_j = 2^{-d} \sum_i \binom{d+1}{2i - j + 1} P_i,$$

which is the coefficient of the basis function $N_d(2x - j - d)$ with first knot $(j + d)/2$. For $d = 2$ this is Chaikin's rule $R_{2i} = \tfrac34 P_i + \tfrac14 P_{i+1}$, $R_{2i+1} = \tfrac14 P_i + \tfrac34 P_{i+1}$. For $d = 3$ it is the cubic rule: the edge point $R_{2i} = \tfrac12 (P_i + P_{i+1})$ and the vertex point $R_{2i+1} = \tfrac18 (P_i + 6 P_{i+1} + P_{i+2})$.

## Example

Take the square $P_0 = (0, 0)$, $P_1 = (4, 0)$, $P_2 = (4, 4)$, $P_3 = (0, 4)$ and $d = 3$, one round.

| Step | Polygon (8 points) |
|---|---|
| L2, double | $(0,0), (0,0), (4,0), (4,0), (4,4), (4,4), (0,4), (0,4)$ |
| L4, pass 1 | $(0,0), (2,0), (4,0), (4,2), (4,4), (2,4), (0,4), (0,2)$ |
| L4, pass 2 | $(1,0), (3,0), (4,1), (4,3), (3,4), (1,4), (0,3), (0,1)$ |
| L4, pass 3 | $(2,0), (7/2,1/2), (4,2), (7/2,7/2), (2,4), (1/2,7/2), (0,2), (1/2,1/2)$ |

Pass 1 inserts the edge midpoints, which is the case $d = 1$, and pass 2 is the Chaikin octagon of degree 2. Pass 3 gives the cubic polygon. The point $(7/2, 1/2)$ is the vertex point $\tfrac18 \big((0,0) + 6 (4,0) + (4,4)\big)$ of the corner $(4, 0)$, and $(2, 0)$ is the edge point of the edge from $(0, 0)$ to $(4, 0)$. The cubic curve of the square passes through $\tfrac16 (P_0 + 4 P_1 + P_2) = (10/3, 2/3)$ at the corner $(4, 0)$, and the refined polygon gives the same point: $\tfrac16 \big((2,0) + 4 (7/2, 1/2) + (4, 2)\big) = (10/3, 2/3)$.

## Correctness

Two facts give the result. First, the uniform B-spline is a repeated convolution of the box function $N_0$, and $N_0(x) = N_0(2x) + N_0(2x - 1)$. The convolution of two refinable functions is refinable, with half the product of the coefficient sequences, so

$$N_d(x) = 2^{-d} \sum_{k=0}^{d+1} \binom{d+1}{k} N_d(2x - k).$$

Second, doubling gives each $P_i$ the coefficient $\binom{1}{2i - j + 1}$ in point $j$, and each averaging pass adds two neighbouring rows of Pascal's triangle. After $d$ passes the coefficient is $2^{-d} \binom{d+1}{2i - j + 1}$, which is the coefficient that the refinement relation gives. So each round describes the same curve.

For convergence, the second differences of the new polygon are combinations of the old ones with the coefficients of $2^{-d} (1 + z)^{d-1}$, and each combination uses coefficients that sum to $\tfrac14$. So the largest second difference drops by the factor 4, and the distance between a B-spline polygon and its curve is at most a constant times this second difference. The full proofs are in the proof file below.

## Complexity

A round on $N$ points writes $2N$ points in line L2 and does $2N$ midpoints in each of the $d$ passes, so it costs $\Theta(d N)$ operations. The sizes are $m, 2m, \dots, 2^{k-1} m$, so $k$ rounds cost $\Theta(d m 2^k)$ in total, in the worst and in the best case. The output takes $\Theta(m 2^k)$ space, and the passes need one more array of the same size. A direct use of the formula for $R_j$ costs the same $\Theta(d)$ per point, with binomial weights. [Boehm knot insertion](/boehm-knot-insertion/) of all midpoints costs $\Theta(d)$ per new knot as well, but it needs divisions and general knot vectors, and the [Oslo algorithm](/oslo-algorithm/) handles arbitrary refinements at a higher cost.

## Properties

- **Exact refinement.** No round changes the curve. The curve has $C^{d-1}$ continuity for $d \ge 1$.
- **Convergence.** For $d \ge 2$, after $k$ rounds the polygon is within $c_d D / 4^k$ of the curve, where $D$ is the largest second difference of the input and $c_d = (d + 1)(d + 3)/8$ in the proof. For $d = 1$ the polygon is the curve. For $d = 0$ the "curve" is a step function.
- **Convex combinations.** All weights are at least 0 and sum to 1, so the [convex hull property](/convex-hull-property/) and the [variation diminishing property](/variation-diminishing-property/) hold for every round.
- **A shift.** The output is the canonical refined polygon shifted by $d$ places. For a closed polygon this is a cyclic shift. For an open polyline the shift moves the parameter range, and code that pairs points with parameters must take it into account.
- **Local.** A new point depends on $\lceil (d + 1)/2 \rceil$ or $\lfloor (d + 1)/2 \rfloor + 1$ consecutive old points.
- **Dyadic arithmetic.** Each pass divides by 2, so in floating point the passes are exact until the mantissa runs out, and integer input gives exact output.

## Variants and improvements

- **Open polylines.** Drop the wrap in line L4. Each pass then removes one point, and one round maps $n$ points to $2n - d$. The output is the first $2n - d$ points of the closed output.
- **Tensor product surfaces.** Apply the rule to each row and then to each column of a grid of control points. This refines a uniform tensor product B-spline surface. Lane and Riesenfeld used this for the display of surfaces.
- **Arbitrary topology.** [Catmull-Clark subdivision](/catmull-clark-subdivision/) generalizes the bicubic case, and [Doo-Sabin subdivision](/doo-sabin-subdivision/) the biquadratic case, to meshes whose vertices do not all have 4 neighbours.
- **Splitting the passes.** The scheme is a composition of the doubling with $d$ copies of the averaging operator, whose symbol is $(1 + z)/2$. Other smoothing rules in place of the midpoint give other schemes of the same doubling and smoothing form.
- **Interpolating schemes.** The [four-point scheme](/four-point-scheme/) keeps the old points, so its limit passes through them. It is not a B-spline scheme and gives only $C^1$ curves.

## When to use it

Use it to draw a uniform B-spline curve or surface at a few levels of detail, or to refine a control polygon for editing, when the knots are uniform. It needs only additions and halvings, and the same short loop works for every degree. For non-uniform knots use [Boehm knot insertion](/boehm-knot-insertion/) or the [Oslo algorithm](/oslo-algorithm/). To evaluate the curve at one parameter, use the [de Boor algorithm](/de-boor-algorithm/).

## Pitfalls

- **In place averaging.** Line L4 must use the old values. A loop that overwrites $Q_j$ and then reads it for $Q_{j-1}$ is wrong, and for a closed polygon the last point must read the old $Q_0$.
- **The index shift.** Point $j$ belongs to the basis function with first knot $(j + d)/2$, so the place of the point near $P_i$ depends on $d$. For $d = 1$ point $2i$ is $P_i$, and for $d = 3$ point $2i + 1$ is the vertex point of $P_{i+1}$. Code that expects point $2i$ to be the vertex point of $P_i$ for every degree is off by some places.
- **Shrinking open curves.** An open polyline loses $d$ points per round, and with clamped ends the rule near the ends is different. Uniform rules near the ends do not give the clamped B-spline.
- **Degree 0 and 1.** With $d = 0$ the rule only duplicates points, and with $d = 1$ it inserts midpoints. Neither gives a smooth curve.
- **Size.** The number of points doubles in each round, so $k$ rounds on $m$ points give $m 2^k$ points.

## Implementations

The Python file in this folder has `lane_riesenfeld(points, degree, rounds, closed)`, which follows the pseudocode, and `refine_by_mask(points, degree)`, which uses the binomial formula. The tests compare one and two rounds for degrees 1 to 5 with the control points that Boehm insertion of all half and quarter knots gives for the periodic uniform B-spline, in exact fractions. They also check the binomial formula, Chaikin's rule for $d = 2$, the cubic edge and vertex rules for $d = 3$ and the open form on random polygons.

## History

George Chaikin gave the corner cutting rule in 1974, and Richard Riesenfeld showed in 1975 that it generates the uniform quadratic B-spline. In 1980 Jeffrey Lane and Riesenfeld gave the general scheme for every degree, with the proof of convergence, and used it to display B-spline surfaces by recursive subdivision. In 1978 Catmull and Clark, and Doo and Sabin, had already extended the bicubic and biquadratic cases to meshes of arbitrary topology. The analysis by symbols and difference schemes was developed later by Dyn, Levin, Micchelli and others.

## References
