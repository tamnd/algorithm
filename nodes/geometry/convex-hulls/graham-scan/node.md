---
tag: YMCTB9
kind: algorithm
slug: graham-scan
name: Graham scan
aliases:
- Graham's scan
- Graham's algorithm
area: geometry/convex-hulls
level: core
summary: Sorts points by angle around the lowest point and keeps a stack of left turns; O(n log n).
solves: [convex-hull-problem]
model: real-ram
complexity:
  vars: {n: the number of input points}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1972
  people: [Ronald L. Graham]
  note: Graham published the angular sort followed by a stack scan in Information Processing Letters in 1972, the first planar hull algorithm with an O(n log n) bound.
prereqs: [convex-hull-problem, orientation-test, angular-sort, stack]
see_also: [andrew-monotone-chain, jarvis-march, quickhull, divide-and-conquer-convex-hull, chan-algorithm, melkman-algorithm, convex-hull-lower-bound, upper-and-lower-hull]
sources:
  - paper: doi:10.1016/0020-0190(72)90045-2
    title: R. L. Graham, An efficient algorithm for determining the convex hull of a finite planar set, Information Processing Letters 1(4), 1972
    locator: the whole paper (an interior point as the center, the angular sort, and the scan that deletes the points with a reflex angle)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Section 33.3, Finding the convex hull (GRAHAM-SCAN with the lowest point as the pivot, its loop invariant and the O(n lg n) bound)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 3, Section 3.5, Graham's algorithm (the pivot, the sort with collinear points and the code)
  - paper: doi:10.1016/0020-0190(79)90072-3
    title: A. M. Andrew, Another efficient algorithm for convex hulls in two dimensions, Information Processing Letters 9(5), 1979
    locator: the replacement of the angular sort by a sort on x
---

Graham's scan computes the [convex hull](/convex-hull/) of $n$ points in the plane. It picks the lowest point as a pivot, sorts the other points by the angle they make with the pivot, and walks through them once with a [stack](/stack/), removing every point at which the walk turns right or goes straight. It solves the [convex hull problem](/convex-hull-problem/) in $\Theta(n \log n)$ time, which is optimal by the [lower bound](/convex-hull-lower-bound/), and it needs only the [orientation test](/orientation-test/), so it is exact on integer input.

## In plain words

Stand at the lowest point. Look at all the other points and sort them by direction, from the one to your right, around to the one to your left. Now visit them in that order and draw a path, starting at the lowest point.

Keep the path on a stack. Before you add a new point, look at the last two points of the path. If going from them to the new point turns right or goes straight, the last point is not a corner of the hull, so remove it and look again. When the turn is to the left, add the new point.

When all points are visited, the path closes back at the lowest point, and the stack holds the corners of the hull in counterclockwise order. The sort is the expensive part. The walk is fast: each point is added once and removed at most once.

## The problem

The input is a finite list $P$ of points $p = (x, y)$, with repeats allowed. The output is the list of the vertices of $\operatorname{conv}(P)$ in counterclockwise order. A point in the middle of a hull edge is not a vertex and is not reported. With one distinct point the output is that point, and with all points on one line it is the two end points.

Notation: $n = |P|$, and $h$ is the number of hull vertices. $\mathrm{orient}(p, q, r)$ is the sign of

$$(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x),$$

which is positive for a left (counterclockwise) turn, zero for collinear points and negative for a right turn. The **pivot** $p_0$ is the point with the smallest $y$, and among those the smallest $x$. Every other point $q$ then lies in the half-plane above $p_0$ or on the ray to its right, so its angle $\theta(q)$ around $p_0$ is in $[0, \pi)$. No general position is assumed: duplicates, collinear points and points on one line are handled.

## The algorithm

```pseudo id=main
GRAHAM-SCAN(P)
L1  S ← the distinct points of P
L2  if S is empty then return the empty list
L3  p0 ← the point of S with the smallest y, ties broken by the smallest x
L4  s[1 .. m] ← S \ {p0}, sorted: a before b if orient(p0, a, b) > 0,
        or if orient(p0, a, b) = 0 and a is nearer to p0 than b
L5  stack ← [p0]
L6  for i ← 1 to m do
L7      while |stack| ≥ 2 and orient(stack[−2], stack[−1], s[i]) ≤ 0 do
L8          pop stack
L9      push s[i] onto stack
L10 return stack
```

Here $stack[-1]$ is the top of the stack and $stack[-2]$ the point below it.

- **Line L1** removes duplicates, so the comparator of line L4 never sees two equal points.
- **Line L3.** The tie-break on $x$ matters: with the smallest $x$, a point with the same $y$ lies to the right of $p_0$ at angle $0$, not to the left at angle $\pi$.
- **Line L4.** For $a$ and $b$ above $p_0$, $\mathrm{orient}(p_0, a, b) > 0$ holds exactly when $\theta(a) < \theta(b)$, so the comparator sorts by angle without trigonometry; see [angular sort](/angular-sort/). Points on one ray from $p_0$ are sorted by increasing squared distance, also an exact integer.
- **Lines L7 and L8** pop the top while the last two stack points and the new point fail to make a strict left turn. The test $\le 0$ also removes a point that lies on the segment between its neighbors.
- **Collinear points on the two boundary rays.** On the first ray (the smallest angle), the points arrive nearest first, and each one pops the one before it with $\mathrm{orient} = 0$. On the last ray, the farther points come later and pop the nearer ones. So neither ray needs a special case, unlike some textbook versions that sort the last ray by decreasing distance.

## Example

Take the ten points $(0,0)$, $(4,0)$, $(2,1)$, $(5,3)$, $(2,2)$, $(3,5)$, $(0,4)$, $(1,2)$, $(2,4)$, $(4,4)$. The pivot is $(0,0)$. Line L4 sorts the others by angle, with distance as the tie-break for $(2,2), (4,4)$ (angle $45°$) and for $(1,2), (2,4)$:

$$(4,0),\ (2,1),\ (5,3),\ (2,2),\ (4,4),\ (3,5),\ (1,2),\ (2,4),\ (0,4).$$

The column "pops" gives each popped point with the value of the orientation determinant that caused the pop.

| new point | pops | stack after the push |
| --- | --- | --- |
| start | none | (0,0) |
| (4,0) | none | (0,0) (4,0) |
| (2,1) | none | (0,0) (4,0) (2,1) |
| (5,3) | (2,1): $-7$ | (0,0) (4,0) (5,3) |
| (2,2) | none | (0,0) (4,0) (5,3) (2,2) |
| (4,4) | (2,2): $-4$ | (0,0) (4,0) (5,3) (4,4) |
| (3,5) | (4,4): $0$ | (0,0) (4,0) (5,3) (3,5) |
| (1,2) | none | (0,0) (4,0) (5,3) (3,5) (1,2) |
| (2,4) | (1,2): $-1$ | (0,0) (4,0) (5,3) (3,5) (2,4) |
| (0,4) | (2,4): $-2$ | (0,0) (4,0) (5,3) (3,5) (0,4) |

Line L10 returns $(0,0), (4,0), (5,3), (3,5), (0,4)$, the same hull that [Andrew's monotone chain](/andrew-monotone-chain/) finds for these points. The point $(4,4)$ is on the edge from $(5,3)$ to $(3,5)$, and the zero determinant removes it. The interior point $(2,1)$ is on the stack for one step: at its turn it is a corner of the hull of the points seen so far.

## Correctness

**Theorem.** For every finite list $P$, GRAHAM-SCAN returns the vertices of $\operatorname{conv}(P)$, each once, in counterclockwise order, starting at the pivot.

The key fact is a [loop invariant](/loop-invariant/) of the loop of line L6. Before the point $s[k + 1]$ is processed, the stack $v_0, \ldots, v_t$ starts at $p_0$, ends at $s[k]$, has strictly increasing angles around $p_0$, makes a strict left turn at each inner point, and its convex hull contains all of $p_0, s[1], \ldots, s[k]$. A popped point lies in the triangle formed by $p_0$, the point below it and the new point, so the hull of the stack still contains everything. At the end, a lemma on "fans" (a polygon with increasing angles around $p_0$ and only left turns is convex) shows that the stack is the hull. The full proof, with the collinear cases, is in [the correctness proof](proofs/correctness/).

## Complexity

- **Sort.** Line L4 makes $O(n \log n)$ comparisons with any optimal comparison sort, for example [merge sort](/merge-sort/). Each comparison is one orientation test, plus two squared distances on a tie.
- **Scan.** Each point is pushed once and popped at most once. So the test of line L7 is true at most $m$ times and false exactly $m$ times, and lines L6 to L9 take $\Theta(n)$ time.
- **Total.** $\Theta(n \log n)$ in the worst case on the [real RAM](/real-ram/), dominated by the sort. Line L1 takes $O(n \log n)$ by sorting, or $O(n)$ expected with hashing.
- **Space.** $\Theta(n)$ for the sorted list and the stack.

The bound is optimal: computing the ordered hull needs $\Omega(n \log n)$ operations in the [algebraic decision tree](/algebraic-decision-tree/) model, by the reduction from sorting on the page [convex hull lower bound](/convex-hull-lower-bound/). The method is not output-sensitive: it sorts all points, even the ones far inside. With integer coordinates of absolute value at most $M$, each orientation determinant has absolute value at most $8M^2$ and each squared distance at most $8M^2$.

## Properties

- **Exact with integer input.** The predicates are the orientation test and a comparison of squared distances, both polynomials of degree 2.
- **Strictly convex output.** The test $\le 0$ removes collinear boundary points.
- **Not online.** It needs all points before the sort. For points that arrive one at a time, see the [dynamic convex hull](/dynamic-convex-hull/).
- **Not stable under a change of pivot.** The output starts at the lowest point. Rotate the list if another start is needed.

## Variants and improvements

- **Andrew's monotone chain.** [Andrew's monotone chain](/andrew-monotone-chain/) sorts by $x$ and then $y$ and builds the [upper and lower hulls](/upper-and-lower-hull/) with two scans. It avoids the angular comparator and its tie rules, and it is the usual choice in practice.
- **Graham's original version.** Graham took a point strictly inside the hull as the center (the centroid of three non-collinear points) and sorted all points by angle around it, over the full circle. The scan then starts at a point known to be on the hull.
- **Keeping collinear boundary points.** Use the test $< 0$ in line L7, and sort the points on the last ray by decreasing distance, so that the scan visits them in boundary order.
- **Simple polygons.** If the input is the vertex list of a [simple polygon](/simple-polygon/), no sort is needed, and [Melkman's algorithm](/melkman-algorithm/) finds the hull in $O(n)$ time with a deque. A plain Graham scan in polygon order is not correct for every simple polygon.
- **Output-sensitive hulls.** [Chan's algorithm](/chan-algorithm/) runs a Graham-type scan on groups of points and then wraps around the groups, in $O(n \log h)$ time.

## When to use it

Use it when angles around a point are natural for the problem, for example when the points are already sorted around a center, or as the textbook first hull algorithm. For a general planar hull, [Andrew's monotone chain](/andrew-monotone-chain/) has the same cost and simpler tie rules. When $h$ is very small, the [Jarvis march](/jarvis-march/) with its $O(nh)$ time can be faster, and [Chan's algorithm](/chan-algorithm/) gets $O(n \log h)$ for all $h$.

## Pitfalls

- **Sorting by `atan2` in floating point.** Two points at almost the same angle can be sorted in the wrong order, and the scan then pops a true hull vertex. Use the orientation comparator of line L4 with exact arithmetic.
- **Choosing the pivot by $y$ only.** If line L3 takes any lowest point, another point with the same $y$ can lie to its left at angle $\pi$. The comparator is then not a total order, because $\mathrm{orient}(p_0, a, b) = 0$ for $a$ and $b$ on opposite rays. Break ties by the smallest $x$.
- **A strict test in line L7.** With `orient(...) < 0` the stack keeps collinear points, and points on the last ray, which arrive nearest first, end up in the wrong order. Use `≤ 0`, or change the sort for the last ray as in Variants.
- **Not removing duplicates in line L1.** A copy of the pivot has no angle, and the comparator of line L4 is undefined for it.
- **Floating-point orientation.** Near-collinear points can get the wrong sign. Use integers or `fractions.Fraction`, or an exact predicate such as Shewchuk's adaptive test, never a tolerance.

## Implementations

## History

Ronald Graham published the algorithm in 1972, in a two-page note in Information Processing Letters, written for a problem at Bell Laboratories. His version sorted the points by angle around an interior point and then deleted the points with a reflex angle. It was the first planar hull algorithm with an $O(n \log n)$ bound. The form with the lowest point as the pivot is the one in most textbooks, for example Cormen, Leiserson, Rivest and Stein. A. M. Andrew replaced the angular sort with a sort on $x$ in 1979. Later work by Yao (1981) and Ben-Or (1983) showed that $\Omega(n \log n)$ is a lower bound in algebraic decision tree models, so the scan is optimal in the worst case.

## References
