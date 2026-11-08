---
tag: TZPPQ8
kind: algorithm
slug: kirkpatrick-seidel
name: Kirkpatrick-Seidel algorithm
aliases:
- marriage-before-conquest
- ultimate planar convex hull
- ultimate planar convex hull algorithm
area: geometry/convex-hulls
level: advanced
summary: Output-sensitive 2D hull in O(n log h) time using median-based splitting and bridge finding.
solves: [convex-hull-problem]
model: real-ram
complexity:
  vars: {n: the number of input points, h: the number of hull vertices}
  time: {best: Θ(n), worst: O(n log h)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: true, output-sensitive: true}
history:
  year: 1986
  people: [David G. Kirkpatrick, Raimund Seidel]
  note: Kirkpatrick and Seidel published the algorithm and the matching Omega(n log h) lower bound in SIAM Journal on Computing in 1986, under the title The ultimate planar convex hull algorithm?
prereqs: [convex-hull-problem, upper-and-lower-hull, prune-and-search, median-of-medians]
see_also: [chan-algorithm, jarvis-march, quickhull, divide-and-conquer-convex-hull, convex-hull-output-sensitive-lower-bound, seidel-linear-programming, megiddo-fixed-dimension-lp, convex-hull-3d]
sources:
  - paper: doi:10.1137/0215021
    title: David G. Kirkpatrick and Raimund Seidel, The ultimate planar convex hull algorithm?, SIAM Journal on Computing 15(1), 1986
    locator: the whole paper (marriage-before-conquest, the linear-time bridge by pairing and median slopes, the O(n log h) analysis, and the Omega(n log h) lower bound)
  - paper: doi:10.1137/0212052
    title: Nimrod Megiddo, Linear-time algorithms for linear programming in R^3 and related problems, SIAM Journal on Computing 12(4), 1983
    locator: the prune-and-search method for two-variable linear programs, which the bridge step follows
  - paper: doi:10.1007/BF02712873
    title: Timothy M. Chan, Optimal output-sensitive convex hull algorithms in two and three dimensions, Discrete and Computational Geometry 16, 1996
    locator: Section 1, the comparison with the Kirkpatrick-Seidel algorithm, and the simpler O(n log h) method
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 3, the discussion of output-sensitive hull algorithms
---

The Kirkpatrick-Seidel algorithm computes the [convex hull](/convex-hull/) of $n$ points in the plane in $O(n \log h)$ time, where $h$ is the number of hull vertices. It splits the points at the median $x$-coordinate like a [divide-and-conquer hull](/divide-and-conquer-convex-hull/), but it finds the hull edge that crosses the split, the **bridge**, before it recurses, and then drops every point under the bridge. The authors called this "marriage before conquest". The bridge is found in linear time by [prune and search](/prune-and-search/), and the bound $O(n \log h)$ matches the $\Omega(n \log h)$ lower bound of the same paper, which is why they asked whether it is the "ultimate" planar hull algorithm.

## In plain words

Look at the bottom part of the hull. Draw a vertical line with half of the points on each side. Exactly one edge of the bottom hull crosses this line. Find that edge first.

To find it, pair up the points and look at the slopes of the pairs. Take the middle slope and slide a line with that slope up from below until it touches a point. Where it touches tells you whether the edge you want is steeper or flatter. Then, in half of the pairs, one point cannot be an end of that edge. Throw it away. Repeat until the edge is found.

Now the points between the two ends of the edge cannot be corners. Throw them away and solve the left and right parts in the same way. Each split finds a corner, so work stops soon when there are few corners.

## The problem

The input is a finite list $P$ of points $p = (x, y)$, with repeats allowed. The output is the list of the vertices of $\operatorname{conv}(P)$ in counterclockwise order, starting at the lexicographically smallest point. A point in the middle of a hull edge is not reported. With all points on one line the output is the two end points.

Notation: $n = |P|$, and $h$ is the number of hull vertices, the output size. $\mathrm{orient}(p, q, r)$ is the sign of

$$D(p, q, r) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x),$$

positive for a counterclockwise turn ([orientation test](/orientation-test/)). The slope of a pair $p, q$ with $p_x < q_x$ is $(q_y - p_y)/(q_x - p_x)$, a rational number. The algorithm computes the lower hull and gets the upper hull from the points rotated by $\pi$, as on the [upper and lower hull](/upper-and-lower-hull/) page. General position is not assumed. Points with the same $x$ are grouped so that the core works on distinct $x$-coordinates, collinear points are handled by taking the leftmost and rightmost point on each bridge line, and duplicates are removed first.

## The algorithm

```pseudo id=main
KIRKPATRICK-SEIDEL(P)
L1  S ← the distinct points of P; if |S| ≤ 1 then return S
L2  L ← LOWER-HULL(S); U ← LOWER-HULL(−S), each point negated
L3  return L followed by U, without repeating an end point shared with L

LOWER-HULL(S)
L4  T ← for each x-coordinate, the point of S with that x and the smallest y
L5  a ← the point of T with the smallest x; b ← the point of T with the largest x
L6  return CONNECT(a, b, T)

CONNECT(a, b, T)
L7  if a = b then return [a]
L8  m ← the ⌈|T|/2⌉-th smallest x-coordinate in T
L9  (l, r) ← BRIDGE(T, m)
L10 T_l ← {p ∈ T : p_x ≤ l_x}; T_r ← {p ∈ T : p_x ≥ r_x}
L11 return CONNECT(a, l, T_l) + CONNECT(r, b, T_r)

BRIDGE(T, m)
L12 C ← T
L13 loop
L14     if |C| = 2 then return the two points of C, the left one first
L15     pair the points of C into ⌊|C|/2⌋ pairs (p, q) with p_x < q_x; R ← the unpaired point, if any
L16     K ← the lower median of the slopes of the pairs
L17     M ← the points of C with the smallest y − K·x; l ← the leftmost point of M; r ← the rightmost
L18     if l_x ≤ m < r_x then return (l, r)
L19     if r_x ≤ m then C ← R ∪ {q : slope(p, q) ≤ K} ∪ {p, q : slope(p, q) > K}
L20     else C ← R ∪ {p : slope(p, q) ≥ K} ∪ {p, q : slope(p, q) < K}
```

- **Line L4.** A point that is not the lowest at its $x$ has a point right below it, so it is not on the lower hull. After this step the $x$-coordinates are distinct, and every pair has a slope.
- **Line L8.** The median is taken by linear-time selection ([median of medians](/median-of-medians/)). Taking the $\lceil t/2 \rceil$-th smallest of $t \ge 2$ distinct values guarantees $\min x \le m < \max x$, so the bridge over $m$ exists, and each side gets at most half of the points.
- **Line L10.** The points strictly between $l$ and $r$ in $x$ lie on or above the bridge and are dropped. This is the step that makes the cost depend on $h$.
- **Lines L16 to L18.** The line of slope $K$ that touches $C$ from below touches it at $M$. If $M$ reaches across $m$, the line is the bridge line. Otherwise $M$ lies on one side of $m$, and this shows whether the bridge is steeper than $K$ (line L19) or less steep (line L20).
- **Lines L19 and L20.** If the bridge is steeper than $K$, the left point of a pair with slope at most $K$ cannot be on the bridge line: the right point would then be below that line. So it is dropped. The other case is symmetric. As $K$ is the median slope, about half of the pairs lose a point, so $C$ shrinks by at least a quarter in each round.

## Example

Take the ten points $(0,0)$, $(4,0)$, $(2,1)$, $(5,3)$, $(2,2)$, $(3,5)$, $(0,4)$, $(1,2)$, $(2,4)$, $(4,4)$. For the lower hull, line L4 keeps $T = (0,0), (1,2), (2,1), (3,5), (4,0), (5,3)$, and $a = (0,0)$, $b = (5,3)$. Line L8 gives $m = 2$, the third smallest $x$. With the points paired in this order, BRIDGE$(T, 2)$ runs as follows:

| round | $C$ | pairs and slopes | $K$ | $M$ | case | dropped |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | (0,0), (1,2), (2,1), (3,5), (4,0), (5,3) | (0,0)(1,2): 2; (2,1)(3,5): 4; (4,0)(5,3): 3 | 3 | (4,0), (5,3) | $l_x = 4 > 2$, line L20 | (3,5), (5,3) |
| 2 | (2,1), (4,0), (0,0), (1,2) | (2,1)(4,0): −1/2; (0,0)(1,2): 2 | −1/2 | (0,0) | $r_x = 0 \le 2$, line L19 | (2,1) |
| 3 | (4,0), (0,0), (1,2) | (0,0)(4,0): 0; (1,2) unpaired | 0 | (0,0), (4,0) | $0 \le 2 < 4$, line L18 | |

The bridge is $(0,0)$ to $(4,0)$. Line L10 drops $(1,2)$, $(2,1)$ and $(3,5)$, leaving $T_l = \{(0,0)\}$ and $T_r = \{(4,0), (5,3)\}$. The left call returns $[(0,0)]$ at once; the right call finds the bridge $(4,0)$ to $(5,3)$ at line L14 and returns $[(4,0), (5,3)]$. So $L = (0,0), (4,0), (5,3)$. For the upper hull, the highest points at each $x$ are $(0,4)$, $(1,2)$, $(2,4)$, $(3,5)$, $(4,4)$, $(5,3)$, and the same steps on the rotated points give $U = (5,3), (3,5), (0,4)$. Line L3 drops the repeated $(5,3)$ and returns $(0,0), (4,0), (5,3), (3,5), (0,4)$.

## Correctness

**Theorem.** For every finite list $P$, KIRKPATRICK-SEIDEL terminates and returns the vertices of $\operatorname{conv}(P)$, each once, in counterclockwise order from the lexicographically smallest point; for collinear input with at least two distinct points it returns the two end points.

The core is the invariant of BRIDGE: the set $C$ always contains every point of $T$ on the bridge line $\ell^*$. A line of slope $K$ that supports the points from below touches them left of the bridge if $K$ is less than the bridge slope $s^*$, at the bridge if $K = s^*$, and right of it if $K > s^*$; so lines L18 to L20 read the sign of $K - s^*$ correctly. If $s^* > K$ and a pair $(p, q)$ has slope at most $K$, then $p$ is not on $\ell^*$, since $q$ would then be below $\ell^*$; the other case is symmetric. So no point of $\ell^*$ is ever dropped, and when $C$ has two points they are the bridge ends. CONNECT is then correct by induction: the bridge is a lower hull edge, and the lower hulls of $T_l$ and $T_r$ are the parts of the lower hull of $T$ on each side of it. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

All costs are on the [real RAM](/real-ram/).

- **Bridge in linear time.** A round of BRIDGE on $c$ points costs $O(c)$, with linear-time selection for the median slope. It removes at least $(c - 1)/4$ points, so the round sizes shrink geometrically and the whole call costs $O(|T|)$.
- **One level of the recursion costs $O(n)$.** The sets $T_l$ and $T_r$ of one call are disjoint, so the sets of all calls at one depth are disjoint.
- **Only $h$ calls do work.** Each call with $a \ne b$ finds a new hull edge, so there are fewer than $h$ of them. At depth $k$ each set has fewer than $2n/2^k$ points. So the work at depth $k$ is at most $\min(n, 2hn/2^k)$, up to a constant.
- **Total $O(n \log h)$.** The first $\lceil \log_2 h \rceil$ levels cost $O(n)$ each, and the deeper levels form a geometric series that sums to $O(n)$. So the time is $O(n \log h)$ for $h \ge 2$. With $h$ bounded, for example 3 or 4 hull vertices, it is $O(n)$, which is the best case. The derivation is in [the complexity proof](proofs/complexity/).
- **Space.** $\Theta(n)$ for the sets of the current path of the recursion, whose sizes halve. The recursion depth is $O(\log n)$.

The bound is optimal: in the [algebraic decision tree](/algebraic-decision-tree/) model, computing the hull of $n$ points with $h$ vertices needs $\Omega(n \log h)$ operations in the worst case ([output-sensitive lower bound](/convex-hull-output-sensitive-lower-bound/)). The analysis of Kirkpatrick and Seidel assumes distinct $x$-coordinates. The grouping of line L4 and the removal of duplicates in line L1 use hash tables in the implementation, $O(n)$ expected time; in a pure comparison model, a step that detects equal $x$-coordinates would cost $\Omega(n \log n)$ by the element uniqueness bound, so a comparison-only version breaks ties by a symbolic perturbation instead. The constant factor is large: the bridge step does several passes and a linear-time selection per round, so in practice Andrew's monotone chain is often faster for moderate $h$.

## Properties

- **Exact with integer input.** Slopes are rational numbers, compared exactly as fractions. Line L17 compares values $y - Kx$ with a rational $K$.
- **Output-sensitive and optimal.** $O(n \log h)$ in the worst case, deterministic, matching the lower bound.
- **No presort.** Unlike Graham's scan or the monotone chain, it never sorts the input; it uses only medians.
- **Bridge as a linear program.** The bridge over $m$ is the solution of a linear program in two variables: find the line $y = sx + c$ with every point on or above it that is highest at $x = m$. Lines L12 to L20 solve this program by Megiddo's prune and search.

## Variants and improvements

- **Other bridge finders.** Any linear-time solver for two-variable linear programs can replace BRIDGE, for example [Megiddo's method](/megiddo-fixed-dimension-lp/) or the randomized incremental method of [Seidel](/seidel-linear-programming/), which takes expected linear time and is simpler to code.
- **Chan's algorithm.** [Chan's algorithm](/chan-algorithm/) (1996) reaches $O(n \log h)$ with a much simpler method: it guesses $h$, computes hulls of small groups, and wraps around them with the [Jarvis march](/jarvis-march/) step. It also extends to three dimensions.
- **Pruning first.** Dropping the points inside the quadrilateral of the extreme points in $x$ and $y$ before the recursion does not change the bound but removes many points on typical inputs.
- **Three dimensions.** Edelsbrunner and Shi (1991) applied marriage before conquest to 3D hulls in $O(n \log^2 h)$ time; Chan's method gives $O(n \log h)$ in three dimensions. See [3D convex hull](/convex-hull-3d/).
- **Upper hull only.** Many uses need only one chain, which halves the work.

## When to use it

Use it when a deterministic worst-case $O(n \log h)$ bound matters and the hull is expected to be much smaller than the input. It is mostly of theoretical value: [Chan's algorithm](/chan-algorithm/) has the same bound with simpler steps, [Quickhull](/quickhull/) is often faster in practice on random data, and [Andrew's monotone chain](/andrew-monotone-chain/) is simpler and fast for any $h$. The bridge step by itself is useful wherever a supporting line over a given $x$ must be found in linear time without sorting.

## Pitfalls

- **Choosing $m$ as the plain median.** If $m$ can equal the largest $x$-coordinate, no point lies right of $m$ and BRIDGE has no answer. Line L8 takes the $\lceil t/2 \rceil$-th smallest value of $t \ge 2$ distinct values, which is always below the maximum.
- **Swapping the pruning rules.** In line L19 the bridge is steeper than $K$ and the left point $p$ of a flat pair is dropped; in line L20 the right point $q$ of a steep pair is dropped. With the rules swapped, a bridge end can be dropped and the result is a wrong edge.
- **Equal $x$-coordinates.** Two points with the same $x$ have no slope. Without line L4, a pair with equal $x$ breaks line L15. Keep only the lowest point at each $x$ for the lower hull.
- **Collinear points on the bridge.** Line L17 must return the leftmost and the rightmost point of $M$. Returning an arbitrary point of $M$ can put a point from the middle of a hull edge into the output.
- **Floating-point slopes.** Slopes computed in floating point can tie or swap order, and then line L18 may misread the side of the bridge. Use exact rationals, as the implementation does with `Fraction`.

## Implementations

## History

David Kirkpatrick and Raimund Seidel presented the algorithm at a conference in the early 1980s and published it in SIAM Journal on Computing in 1986, under the title "The ultimate planar convex hull algorithm?". The same paper proved the $\Omega(n \log h)$ lower bound in the algebraic decision tree model, so the algorithm is optimal as a function of both $n$ and $h$. Its bridge step uses the prune-and-search idea that Megiddo developed for linear programming in fixed dimension at the same time. Ten years later Timothy Chan found a simpler optimal algorithm, and the Kirkpatrick-Seidel method is now mainly taught as an example of output-sensitive design and of prune and search.

## References
