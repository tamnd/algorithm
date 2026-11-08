---
tag: VJDFF6
kind: algorithm
slug: andrew-monotone-chain
name: Andrew's monotone chain
aliases:
- Andrew's algorithm
- monotone chain algorithm
- monotone chain convex hull
area: geometry/convex-hulls
level: core
summary: Sorts points by x then builds the lower and upper hulls with a stack; O(n log n).
solves: [convex-hull-problem]
model: real-ram
complexity:
  vars: {n: the number of input points}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1979
  people: [A. M. Andrew]
  note: Andrew published the variant of Graham's scan that sorts by x-coordinate and builds the two monotone chains in Information Processing Letters in 1979.
prereqs: [convex-hull-problem, orientation-test, stack, sorting-problem]
see_also: [graham-scan, upper-and-lower-hull, jarvis-march, quickhull, chan-algorithm, kirkpatrick-seidel, melkman-algorithm, convex-hull-lower-bound]
sources:
  - paper: doi:10.1016/0020-0190(79)90072-3
    title: A. M. Andrew, Another efficient algorithm for convex hulls in two dimensions, Information Processing Letters 9(5), 1979
    locator: the whole paper (sort by x, split by the line through the two extreme points, and scan each half with the Graham test)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 1, Section 1.1, An Example, Convex Hulls (algorithm CONVEXHULL, the upper and lower hulls built by a scan in x-order, its correctness and the O(n log n) bound)
  - paper: doi:10.1016/0020-0190(72)90045-2
    title: R. L. Graham, An efficient algorithm for determining the convex hull of a finite planar set, Information Processing Letters 1(4), 1972
    locator: the whole paper (the scan with a stack that Andrew's method reuses)
---

Andrew's monotone chain algorithm computes the [convex hull](/convex-hull/) of $n$ points in the plane. It sorts the points by $x$ and then by $y$, builds the lower hull with one left-to-right scan and the upper hull with one right-to-left scan, and joins the two chains. It solves the [convex hull problem](/convex-hull-problem/) in $\Theta(n \log n)$ time, which is optimal by the [lower bound](/convex-hull-lower-bound/), and it uses only the [orientation test](/orientation-test/), so it is exact on integer input. It is the [Graham scan](/graham-scan/) with the angular sort replaced by a sort on coordinates.

## In plain words

Sort the points from left to right. Walk along them and keep a stack of points that forms a chain bent to the left, like the bottom of a bowl. When a new point would make the chain bend to the right or go straight, the last point of the chain cannot be on the bottom of the hull, so you remove it. Repeat the check until the bend is to the left, then add the new point. At the end the stack holds the lower boundary of the hull.

Walk back from right to left with the same rule to get the upper boundary. Glue the two chains at their ends. Each point goes on a stack at most twice and leaves it at most twice, so after the sort the work is linear.

## The problem

The input is a finite list $P$ of points $p = (x, y)$, with repeats allowed. The output is the list of the vertices of $\mathrm{conv}(P)$ in counterclockwise order, starting at the lexicographically smallest point. A point in the middle of a hull edge is not a vertex and is not reported. With one or two distinct points, the output is those points, and with all points on one line it is the two end points.

Notation: $n = |P|$, and $h$ is the number of hull vertices. $\mathrm{orient}(p, q, r)$ is the sign of

$$(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x),$$

which is positive when $p, q, r$ make a left (counterclockwise) turn, zero when they are collinear and negative for a right turn. We compare points lexicographically: $p < q$ when $p_x < q_x$, or $p_x = q_x$ and $p_y < q_y$. No general position is assumed.

## The algorithm

```pseudo id=main
ANDREW-HULL(P)
L1  p[1 .. n] ← the distinct points of P, sorted lexicographically
L2  if n ≤ 2 then return p[1 .. n]
L3  lower ← empty stack
L4  for i ← 1 to n do
L5      while |lower| ≥ 2 and orient(lower[−2], lower[−1], p[i]) ≤ 0 do
L6          pop lower
L7      push p[i] onto lower
L8  upper ← empty stack
L9  for i ← n downto 1 do
L10     while |upper| ≥ 2 and orient(upper[−2], upper[−1], p[i]) ≤ 0 do
L11         pop upper
L12     push p[i] onto upper
L13 return lower without its last point, then upper without its last point
```

Here $lower[-1]$ is the top of the stack and $lower[-2]$ the point below it. Line L1 removes duplicates, so the points are distinct and strictly increasing. Lines L3 to L7 build the lower hull from the smallest point $a = p[1]$ to the largest point $b = p[n]$. The test of line L5 pops the top while the last two stack points and the new point fail to make a strict left turn. The test is $\le 0$, not $< 0$, so a point in the middle of an edge is popped too, and the output has only strictly convex vertices. Lines L8 to L12 do the same scan in the reverse order, which builds the upper hull from $b$ back to $a$. Each chain ends where the other one starts, so line L13 drops the last point of each chain before it joins them.

## Example

Take the ten points $(0,0)$, $(4,0)$, $(2,1)$, $(5,3)$, $(2,2)$, $(3,5)$, $(0,4)$, $(1,2)$, $(2,4)$, $(4,4)$. In sorted order they are

$$(0,0),\ (0,4),\ (1,2),\ (2,1),\ (2,2),\ (2,4),\ (3,5),\ (4,0),\ (4,4),\ (5,3).$$

The lower scan (lines L4 to L7). The column "pops" gives each popped point with the value of the orientation determinant that caused the pop.

| new point | pops | stack after the push |
| --- | --- | --- |
| (0,0) | none | (0,0) |
| (0,4) | none | (0,0) (0,4) |
| (1,2) | (0,4): $-4$ | (0,0) (1,2) |
| (2,1) | (1,2): $-3$ | (0,0) (2,1) |
| (2,2) | none | (0,0) (2,1) (2,2) |
| (2,4) | (2,2): $0$ | (0,0) (2,1) (2,4) |
| (3,5) | (2,4): $-3$ | (0,0) (2,1) (3,5) |
| (4,0) | (3,5): $-9$, then (2,1): $-4$ | (0,0) (4,0) |
| (4,4) | none | (0,0) (4,0) (4,4) |
| (5,3) | (4,4): $-4$ | (0,0) (4,0) (5,3) |

The upper scan (lines L9 to L12) reads the same list from the right.

| new point | pops | stack after the push |
| --- | --- | --- |
| (5,3) | none | (5,3) |
| (4,4) | none | (5,3) (4,4) |
| (4,0) | none | (5,3) (4,4) (4,0) |
| (3,5) | (4,0): $-4$, then (4,4): $0$ | (5,3) (3,5) |
| (2,4) | none | (5,3) (3,5) (2,4) |
| (2,2) | none | (5,3) (3,5) (2,4) (2,2) |
| (2,1) | (2,2): $0$ | (5,3) (3,5) (2,4) (2,1) |
| (1,2) | (2,1): $-3$ | (5,3) (3,5) (2,4) (1,2) |
| (0,4) | (1,2): $-4$, then (2,4): $-2$ | (5,3) (3,5) (0,4) |
| (0,0) | none | (5,3) (3,5) (0,4) (0,0) |

Line L13 returns $(0,0), (4,0), (5,3), (3,5), (0,4)$. The point $(4,4)$ lies on the hull edge from $(5,3)$ to $(3,5)$, and the zero determinant at the push of $(3,5)$ removes it. The point $(0,4)$ is popped from the lower chain early but comes back as a vertex of the upper chain.

## Correctness

The key fact is a [loop invariant](/loop-invariant/) of the loop of line L4. After the points $p[1 \ldots i]$ are processed, the stack $v_1, \ldots, v_k$ starts at $p[1]$ and ends at $p[i]$, is lexicographically increasing, makes a strict left turn at each inner point, and has every point of $p[1 \ldots i]$ on or to the left of the line through each of its edges. The proof of maintenance compares directions: for vectors that point into the half-plane "to the right, or straight up", the sign of the cross product orders them by angle. The upper scan is the same procedure on the point set reflected through the origin. A final step shows that the closed chain has every input point inside it and that each of its vertices is extreme, so it is exactly the hull. The full proof is in the correctness proof below.

## Complexity

- **Sort.** Line L1 sorts $n$ points and removes repeats in $O(n \log n)$ time with any optimal comparison sort, for example [merge sort](/merge-sort/).
- **Scans.** In the scan of lines L4 to L7, each point is pushed once, and a point is popped at most once because it is never pushed again. So the test of line L5 is true at most $n$ times and false exactly $n$ times, and the scan takes $\Theta(n)$ time. The same holds for lines L9 to L12. Each test is one orientation determinant: two multiplications and five subtractions.
- **Total.** $\Theta(n \log n)$ in the worst case on the [real RAM](/real-ram/), dominated by the sort. When the input is already sorted, the scans alone take $\Theta(n)$ time.
- **Space.** $\Theta(n)$ for the sorted copy and the two stacks.

The bound is optimal: computing the ordered hull needs $\Omega(n \log n)$ operations in the algebraic decision tree model, by the reduction from sorting on the page [convex hull lower bound](/convex-hull-lower-bound/). The method is not output-sensitive. For $h$ hull vertices, [Chan's algorithm](/chan-algorithm/) and the [Kirkpatrick-Seidel algorithm](/kirkpatrick-seidel/) take $O(n \log h)$ time.

With integer coordinates of absolute value at most $M$, each determinant has absolute value at most $8M^2$. So 64-bit coordinates need 130-bit arithmetic for an exact test. Python integers and `fractions.Fraction` are exact with no extra care.

## Properties

- **Exact with integer input.** The only predicate is the orientation test, a polynomial of degree 2 in the coordinates.
- **Strictly convex output.** The test $\le 0$ removes collinear boundary points. Change it to $< 0$ to keep them, but then repeated points and fully collinear input need extra care.
- **Not online.** It needs all points before the sort. For points that arrive one at a time, see the [dynamic convex hull](/dynamic-convex-hull/).
- **Upper and lower hull for free.** The two stacks are the [upper and lower hulls](/upper-and-lower-hull/), which many applications use directly.

## Variants and improvements

- **Graham's scan.** [Graham's scan](/graham-scan/) sorts by polar angle around the lowest point instead of by $x$. The [angular sort](/angular-sort/) needs a careful comparator for collinear points. Andrew's version avoids it.
- **One chain only.** Lines L3 to L7 alone give the lower hull. The [convex hull trick](/convex-hull-trick/) of dynamic programming keeps such a chain of lines or points.
- **Presorted input.** When the input is sorted by $x$, or is the vertex list of a simple polygon, the hull takes linear time: the scans of this page in the first case and [Melkman's algorithm](/melkman-algorithm/) in the second.
- **Group hulls in Chan's algorithm.** [Chan's algorithm](/chan-algorithm/) runs this method on groups of $m$ points, then wraps around the groups.

## When to use it

Use it as the default planar hull. It is short, it needs no angles, no trigonometry and no special pivot, and it is exact with integer coordinates. Use [Chan's algorithm](/chan-algorithm/) only when the hull is known to be very small and $n$ is large enough for the $O(n \log h)$ bound to matter. Use [quickhull](/quickhull/) when you expect most points to be deep inside the hull and you accept an $O(n^2)$ worst case. For points in three dimensions, see the [3D convex hull problem](/convex-hull-3d/).

## Pitfalls

- **A strict test in lines L5 and L10.** With `orient(...) < 0` the stacks keep collinear points, and on all-collinear input each middle point appears twice in the output, once from each chain. Use `≤ 0`, or remove duplicates and handle the collinear case on purpose.
- **Not removing duplicates in line L1.** Two equal points give $\mathrm{orient} = 0$, so the version with $\le 0$ still works, but a version with $< 0$ outputs the point twice.
- **Floating-point orientation.** With float coordinates, the determinant can have the wrong sign for nearly collinear points, and the scan can then pop a true hull vertex or keep a point that is inside. Use integers or `fractions.Fraction`, or an exact predicate such as Shewchuk's adaptive test. Never compare the determinant with a tolerance: that makes the test inconsistent.
- **Forgetting to drop the shared end points in line L13.** Each chain contains both $a$ and $b$, so the join must drop one copy of each.
- **Sorting by $x$ only.** Points with the same $x$ must also be sorted by $y$. Otherwise a vertical edge at the left or right end can make the chains wrong.

## Implementations

## History

Ronald Graham published the stack scan for the planar hull in 1972, with an angular sort around an interior point. A. M. Andrew showed in 1979 that a sort on the $x$-coordinate suffices: split the points by the line through the leftmost and the rightmost point and scan each side. The form of this page, with one scan for the lower hull and one for the upper hull over the same sorted list, is the version that de Berg, Cheong, van Kreveld and Overmars give in the first chapter of their textbook.

## References
