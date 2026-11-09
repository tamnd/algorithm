---
tag: 5XWJY8
kind: algorithm
slug: shamos-hoey-algorithm
name: Shamos-Hoey algorithm
aliases: [Bentley-Ottmann detection variant, Shamos-Hoey sweep, shamos-hoey]
area: geometry/intersections
level: core
summary: Sweep-line test that decides whether any two of n segments intersect in O(n log n) time, by checking only segments that become neighbors in the sweep order.
solves: [segment-intersection-detection, intersecting-segment-pair-search]
model: real-ram
complexity:
  vars: {n: the number of segments}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1976
  people: [Michael Ian Shamos, Dan Hoey]
  note: Shamos and Hoey gave the sweep at FOCS 1976 and showed that the O(n log n) bound is optimal for the decision problem.
prereqs: [segment-intersection-detection, segment-intersection-point, sweep-line-technique, sweep-status-structure, balanced-binary-search-tree, orientation-test]
see_also: [bentley-ottmann-algorithm, segment-intersection-lower-bound, polygon-simplicity-test, event-queue, sweep-invariant, degeneracy-in-sweeps, red-blue-intersection, closest-pair-sweep-line]
sources:
  - paper: doi:10.1109/SFCS.1976.16
    title: Michael Ian Shamos and Dan Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science (FOCS 1976), 208-215
    locator: the sweep for deciding whether any two of n segments intersect, and its O(n log n) bound
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Chapter 33, Section 33.2, Determining whether any pair of segments intersects (procedure ANY-SEGMENTS-INTERSECT and its correctness proof)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 7, Section 7.2.3, Intersection of line segments (the sweep for the test and the lower bound)
---

The Shamos-Hoey algorithm decides whether any two of $n$ closed segments in the plane intersect, in $\Theta(n \log n)$ time. A vertical line sweeps from left to right over the end points, and a [balanced search tree](/balanced-binary-search-tree/) keeps the segments that cross the line in their vertical order. The key fact is that the leftmost intersection is found from two segments that become neighbors in this order, so each event needs only a constant number of [pairwise tests](/segment-intersection-point/). It solves [segment intersection detection](/segment-intersection-detection/) optimally: the [lower bound](/segment-intersection-lower-bound/) is $\Omega(n \log n)$ in the algebraic decision tree model.

## In plain words

Move a vertical line from left to right across the plane. At each moment, the segments that cross the line are stacked from bottom to top. If two segments cross, then just to the left of the first crossing they are next to each other in this stack, because nothing can be between two lines that are about to meet.

So you only need to test pairs that are neighbors in the stack. The stack changes only when the line reaches the end of a segment: a new segment goes in at its place, or a segment leaves and its two neighbors become neighbors. At each such moment you test the one or two new pairs of neighbors. If a test finds a crossing, you stop. If the line reaches the right side and no test found one, no two segments meet.

## The problem

The input is a list $S$ of $n$ closed segments with rational end points. The output is a pair of segments of $S$ that have a common point, or none if the segments are pairwise disjoint. Shared end points, a point of one segment on another, and collinear overlap all count as intersections.

Notation: points are $p = (x, y)$, and $p < q$ in lexicographic order means $p_x < q_x$, or $p_x = q_x$ and $p_y < q_y$. Each segment $s$ has end points $l(s) \le r(s)$. $\mathrm{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$, positive for a counterclockwise turn. $T$ is the status: the segments that cross the sweep line, from bottom to top. No [general position](/general-position/) is assumed: the code handles vertical segments, segments of length zero, repeated segments and collinear overlaps.

## The algorithm

```pseudo id=main
SHAMOS-HOEY(S)
L1  name the end points of each s ∈ S so that l(s) ≤ r(s)
L2  T ← empty sequence of segments, ordered from bottom to top
L3  for each end point p, in increasing lexicographic order do
L4      E ← the segments of S with an end point at p
L5      if |E| ≥ 2 then return two segments of E
L6      s ← the only segment of E
L7      [i, j) ← the block of t ∈ T with orient(l(t), r(t), p) = 0, by two binary searches
L8      if the block holds a segment t ≠ s then return (s, t)
L9      if l(s) = r(s) then continue with the next p
L10     if p = l(s) then insert s at position i of T, and for each neighbor t of s: if s ∩ t ≠ ∅ then return (s, t)
L11     else let a, b be the neighbors of s; delete s from T; if a and b exist and a ∩ b ≠ ∅ then return (a, b)
L12 return none
```

The sweep handles the end points in lexicographic order (line L3). This is a sweep by a line that is turned a tiny bit clockwise from the vertical, so a vertical segment is met from its lower end to its upper end, like any other segment. Lines L4 and L5 catch shared end points at once. After that, exactly one segment $s$ has an end point at $p$.

Line L7 locates $p$ in $T$. For a segment $t$ of $T$, $\mathrm{orient}(l(t), r(t), p)$ is positive when $p$ is above $t$, zero when $p$ is on $t$, and negative when $p$ is below. Along $T$ these signs go from positive to zero to negative, so two binary searches find the block of segments through $p$. A segment of that block other than $s$ contains $p$, and line L8 reports it. A segment of length zero is never stored (line L9). At a left end point, line L10 inserts $s$ at its place and tests it against its new neighbors, with the exact test of the [segment intersection point](/segment-intersection-point/) page. At a right end point, line L11 deletes $s$ and tests the two segments that become neighbors.

## Example

Take the four segments $s_0 = (0,0)$-$(6,2)$, $s_1 = (1,4)$-$(7,5)$, $s_2 = (2,3)$-$(5,2)$ and $s_3 = (8,0)$-$(8,6)$, which are pairwise disjoint. The status is written from bottom to top.

| event $p$ | kind | position (line L7) | $T$ after the event | pairs tested |
| --- | --- | --- | --- | --- |
| (0,0) | left of $s_0$ | empty $T$ | $s_0$ | none |
| (1,4) | left of $s_1$ | above $s_0$ (orient $= 22$) | $s_0, s_1$ | $s_0, s_1$: disjoint |
| (2,3) | left of $s_2$ | above $s_0$ ($14$), below $s_1$ ($-7$) | $s_0, s_2, s_1$ | $s_2, s_0$ and $s_2, s_1$: disjoint |
| (5,2) | right of $s_2$ | above $s_0$ ($2$), below $s_1$ ($-16$) | $s_0, s_1$ | $s_0, s_1$: disjoint |
| (6,2) | right of $s_0$ | below $s_1$ ($-17$) | $s_1$ | none |
| (7,5) | right of $s_1$ | | empty | none |
| (8,0) | left of $s_3$ | empty $T$ | $s_3$ | none |
| (8,6) | right of $s_3$ | | empty | none |

The sweep ends at line L12 with none. Now change $s_2$ to $(2,3)$-$(5,0)$. At the event $(2,3)$ the new segment goes between $s_0$ and $s_1$ as before, and the test of $s_2$ against $s_0$ finds the crossing point $(15/4, 5/4)$, so line L10 returns the pair $s_0, s_2$ before the sweep reaches that point.

## Correctness

Let $q$ be the lexicographically smallest point that lies on two segments. The invariant is: at every event $p \le q$, the segments of $T$ are sorted by the $y$-coordinate of their points on the line $x = p_x$, so line L7 finds the right block. Two segments in $T$ cannot change their order before they cross, and no crossing is smaller than $q$. Then there are three cases. If $q$ is an end point of two segments, line L5 finds it. If $q$ is an end point of one segment and inside another, line L8 finds it. If $q$ is inside every segment through it, two of these segments are neighbors in $T$ just before $q$, and the event that made them neighbors tested them. Every reported pair is checked exactly, so the algorithm never reports a false pair. The full proof, with the cases for vertical segments, is in the correctness proof below.

## Complexity

- **Events.** There are at most $2n$ distinct end points. Sorting them takes $O(n \log n)$ time.
- **Each event.** With a [balanced binary search tree](/balanced-binary-search-tree/) for $T$, such as a [red-black tree](/red-black-tree/), the binary searches of line L7 and the update of line L10 or L11 take $O(\log n)$ orientation tests and pointer steps, and at most two pairwise tests follow. Line L8 stops at the first member of the block other than $s$.
- **Total.** $\Theta(n \log n)$ time in the worst case on the [real RAM](/real-ram/), and $\Theta(n)$ space for the events and the tree. On disjoint input the sweep does all $2n$ events, and the sort alone needs $\Omega(n \log n)$ comparisons in the worst case.
- **Optimality.** Deciding whether $n$ segments intersect needs $\Omega(n \log n)$ operations in the algebraic decision tree model, by a reduction from [element distinctness](/element-distinctness/); see [segment intersection lower bound](/segment-intersection-lower-bound/).
- **The Python code.** It keeps $T$ in a Python list and finds positions by binary search, so each insert or delete also moves up to $n$ references in memory. This adds an $O(n^2)$ term in the worst case with a very small constant. A balanced tree removes it.

With integer coordinates of absolute value at most $M$, each orientation value has absolute value at most $8M^2$, and the code never needs a division: the sweep compares only signs.

## Properties

- **Exact.** All decisions are signs of orientation determinants of input points. No intersection point is ever computed.
- **Stops early.** It returns at the first intersection it finds, which is at or before the leftmost intersection point.
- **Not a reporting algorithm.** It finds one pair, not all pairs. Its order invariant holds only up to the first crossing.
- **Not online.** It needs all end points before the sweep starts.

## Variants and improvements

- **Reporting all intersections.** The [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/) adds the crossing points as events and swaps the two segments there, which keeps the order invariant after crossings. It reports all $k$ intersections in $O((n + k) \log n)$ time.
- **Simple polygons.** A polygon is simple when no two non-adjacent edges meet. Run the sweep on the edges with the shared vertex of adjacent edges excused, as in the [polygon simplicity test](/polygon-simplicity-test/).
- **Other curves.** The same sweep works for $x$-monotone arcs that cross at most a constant number of times, such as circles split into upper and lower halves. Shamos and Hoey used it to test whether any two of $n$ circles intersect.
- **Two colors.** To test whether a red segment meets a blue one when the reds are pairwise disjoint and the blues are too, see [red-blue intersection](/red-blue-intersection/).

## When to use it

Use it when only a yes or no answer, or one witness pair, is needed, for example to check that a polygon is simple, that a drawing of a graph has no crossings, or that a set of wires does not touch. It is never slower than the reporting algorithms and computes no intersection points, so it has no growth in the size of the numbers. For a few dozen segments, the quadratic test of all pairs is simpler and fast enough.

## Pitfalls

- **Comparing only $y$-coordinates at the sweep line.** A comparison by the computed $y$ of each segment at $x = p_x$ needs a division and ties are hard. Compare the event point with each segment by $\mathrm{orient}(l(t), r(t), p)$, as in line L7.
- **Vertical segments ordered by $x$ only.** If events with the same $x$ are not ordered by $y$, a vertical segment is inserted and deleted in the wrong order. Use the lexicographic order of line L3.
- **Testing only proper crossings.** If the pairwise test of lines L10 and L11 ignores touching cases, the sweep misses T-junctions and overlaps. Use the full test of [segment intersection point](/segment-intersection-point/).
- **Forgetting line L8.** An end point can lie inside another segment that is not a neighbor of $s$ after the insert, for example when several segments pass through it. The block search of lines L7 and L8 catches this case.
- **Continuing after the first crossing.** After a crossing, the order in $T$ is wrong, and a later binary search can fail. The detection algorithm must stop at the first intersection. To go on, use [Bentley-Ottmann](/bentley-ottmann-algorithm/).

## Implementations

## History

Michael Shamos and Dan Hoey presented the sweep at FOCS 1976 in "Geometric intersection problems". They showed that the test for $n$ segments takes $O(n \log n)$ time, that this is optimal, and that the same idea decides whether simple polygons or circles intersect. Bentley and Ottmann extended the sweep to report all intersections in 1979. The proof by "neighbors just before the leftmost crossing" is the standard textbook argument, given for example by Cormen, Leiserson, Rivest and Stein under the assumptions that no segment is vertical and no three segments meet in a point. The version of this page removes those assumptions with the lexicographic event order and the block search of line L7.

## References
