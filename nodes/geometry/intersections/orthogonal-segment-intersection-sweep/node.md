---
tag: AM0665
kind: algorithm
slug: orthogonal-segment-intersection-sweep
name: Orthogonal segment intersection sweep
aliases: [Bentley orthogonal segment intersection, bentley-orthogonal-sweep]
area: geometry/intersections
level: core
summary: Sweep over x that keeps the active horizontal segments ordered by y and answers each vertical segment by a range query, reporting k crossings in O(n log n + k) time.
solves: [orthogonal-segment-intersection]
model: real-ram
complexity:
  vars: {n: the number of segments, k: the number of intersecting pairs}
  time: {worst: Θ(n log n + k)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1979
  people: [Jon Louis Bentley, Thomas A. Ottmann]
  note: The sweep with a one-dimensional range query for each vertical segment appears with the rectilinear case in the 1979 paper of Bentley and Ottmann and in the work of Bentley and Wood on rectangles.
prereqs: [orthogonal-segment-intersection, sweep-line-technique, orthogonal-range-reporting, balanced-binary-search-tree]
see_also: [fenwick-tree, bentley-ottmann-algorithm, rectangle-intersection-reporting, rectangle-intersection-sweep, segment-tree, interval-tree, event-queue, sweep-invariant]
sources:
  - paper: doi:10.1109/TC.1979.1675432
    title: Jon L. Bentley and Thomas A. Ottmann, Algorithms for reporting and counting geometric intersections, IEEE Transactions on Computers C-28(9), 1979, 643-647
    locator: the rectilinear case (horizontal and vertical segments, reporting in O(n log n + k) and counting in O(n log n))
  - paper: doi:10.1109/TC.1980.1675628
    title: Jon L. Bentley and Derick Wood, An optimal worst case algorithm for reporting intersections of rectangles, IEEE Transactions on Computers C-29(7), 1980, 571-577
    locator: the sweep that reduces rectangle reporting to orthogonal segment intersection plus point enclosure
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 8, The Geometry of Rectangles (intersection of orthogonal segments and of rectangles by sweeping)
---

The orthogonal segment intersection sweep reports all $k$ pairs of a horizontal and a vertical segment that meet, among $n$ segments, in $\Theta(n \log n + k)$ time. A vertical line sweeps from left to right. The horizontal segments that cross the line are kept in an ordered set by their $y$-coordinate, and each vertical segment becomes one [orthogonal range reporting](/orthogonal-range-reporting/) query in one dimension. Unlike the [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/) for general segments, it needs no crossing events, because a horizontal segment never changes its place in the order.

## In plain words

Move a vertical line from left to right. A horizontal segment is "active" while the line is over it: it starts at its left end and stops at its right end. Keep the active horizontal segments sorted by height.

When the line reaches a vertical segment, the horizontal segments that it meets are exactly the active ones whose height is between the bottom and the top of the vertical segment. In a sorted list you can find the first such height quickly and then read off the others one after the other. So the work for each vertical segment is a short search plus one step for each crossing you report.

## The problem

The input is a list $H$ of horizontal segments $h$, each given by its height $y(h)$ and its $x$-range $[x_1(h), x_2(h)]$, and a list $V$ of vertical segments $v$, each given by $x(v)$ and its $y$-range $[y_1(v), y_2(v)]$. Segments are closed. The output is every pair $(h, v)$ with $x_1(h) \le x(v) \le x_2(h)$ and $y_1(v) \le y(h) \le y_2(v)$, which is the condition for $h$ and $v$ to meet. Collinear overlaps of two horizontal or two vertical segments are not part of this problem; they are a one-dimensional interval problem on each line.

Notation: $n = |H| + |V|$ and $k$ is the number of reported pairs. $T$ is the status: the active horizontal segments ordered by $y$. Coordinates are integers or rational numbers, and the algorithm only compares them, so it is exact. Equal coordinates, segments of length zero and touching end points are all allowed.

## The algorithm

```pseudo id=main
ORTHOGONAL-SWEEP(H, V)
L1  E ← for each h ∈ H the events (x1(h), insert, h) and (x2(h), delete, h), and for each v ∈ V the event (x(v), query, v)
L2  sort E by x; at equal x, inserts come first, then queries, then deletes
L3  T ← empty ordered set of horizontal segments, keyed by y
L4  for each event (x, kind, e) of E in order do
L5      if kind = insert then insert e into T with key y(e)
L6      else if kind = query then
L7          for each h in T with y1(e) ≤ y(h) ≤ y2(e), in order of y, do
L8              report (h, e)
L9      else delete e from T
```

The order of line L2 makes touching count: a vertical segment at the left or right end of a horizontal one sees it in $T$. Line L7 is a one-dimensional range query: find the first key $\ge y_1(e)$ and walk to the next keys while they are $\le y_2(e)$.

Any ordered set with a successor step works for $T$. A [balanced binary search tree](/balanced-binary-search-tree/) with its nodes linked in order gives $O(\log n)$ updates and $O(\log n + m)$ queries for $m$ answers. The code uses the fact that all keys are known in advance: it sorts the distinct $y$ values once, keeps a [Fenwick tree](/fenwick-tree/) over the flags "some active segment has this $y$", and links the used $y$ values in a doubly linked list. The Fenwick tree finds the first used value at or after a position in $O(\log n)$ time, and the list gives each next used value in $O(1)$ time.

## Example

Take $h_0$: $y = 1$, $x \in [0, 6]$; $h_1$: $y = 3$, $x \in [2, 9]$; $h_2$: $y = 5$, $x \in [1, 4]$; $h_3$: $y = 3$, $x \in [7, 8]$, and $v_0$: $x = 2$, $y \in [0, 4]$; $v_1$: $x = 5$, $y \in [2, 6]$; $v_2$: $x = 8$, $y \in [3, 3]$ (a point); $v_3$: $x = 0$, $y \in [2, 9]$.

| $x$ | events in order | $T$ after the events (as $y$: segments) | reported |
| --- | --- | --- | --- |
| 0 | insert $h_0$, query $v_3$ | 1: $h_0$ | none, since $1 \notin [2, 9]$ |
| 1 | insert $h_2$ | 1: $h_0$; 5: $h_2$ | |
| 2 | insert $h_1$, query $v_0$ | 1: $h_0$; 3: $h_1$; 5: $h_2$ | $(h_0, v_0)$, $(h_1, v_0)$ |
| 4 | delete $h_2$ | 1: $h_0$; 3: $h_1$ | |
| 5 | query $v_1$ | 1: $h_0$; 3: $h_1$ | $(h_1, v_1)$ |
| 6 | delete $h_0$ | 3: $h_1$ | |
| 7 | insert $h_3$ | 3: $h_1, h_3$ | |
| 8 | query $v_2$, delete $h_3$ | 3: $h_1$ | $(h_1, v_2)$, $(h_3, v_2)$ |
| 9 | delete $h_1$ | empty | |

At $x = 2$ the insert of $h_1$ comes before the query of $v_0$, so the T-junction at $(2, 3)$ is reported. At $x = 8$ the query of the point $v_2$ comes before the delete of $h_3$, so the end point $(8, 3)$ of $h_3$ is reported. The output has $k = 5$ pairs.

## Correctness

The invariant is: when the query of $v$ runs, $T$ holds exactly the horizontal segments $h$ with $x_1(h) \le x(v) \le x_2(h)$. It holds because the insert of $h$ comes before the query exactly when $x_1(h) \le x(v)$, and the delete of $h$ comes before the query exactly when $x_2(h) < x(v)$, by the tie order of line L2. Then the range query of line L7 returns the active segments with $y_1(v) \le y(h) \le y_2(v)$, which are exactly the segments that meet $v$. Each vertical segment is queried once, so each pair is reported once. The full proof, with the invariant of the Fenwick tree and the linked list, is in the correctness proof below.

## Complexity

- **Sort.** $2|H| + |V| \le 2n$ events, sorted in $O(n \log n)$ time.
- **Updates.** Each insert and delete takes $O(\log n)$ time: a Fenwick update and, when a $y$ value becomes used or unused, two Fenwick searches and a constant number of list updates.
- **Queries.** A query takes $O(\log n)$ time to find the first used $y \ge y_1$, then $O(1)$ time per reported pair, because every used $y$ value it visits has at least one active segment. The sum over all queries is $O(n \log n + k)$.
- **Total.** $\Theta(n \log n + k)$ time in the worst case on the [real RAM](/real-ram/), and $\Theta(n)$ space. The bound is optimal in the algebraic decision tree model: $\Omega(k)$ to write the output, and $\Omega(n \log n)$ even to decide whether any pair meets, by a reduction from [element distinctness](/element-distinctness/).

## Properties

- **No arithmetic.** The algorithm only compares input coordinates, so it is exact for any ordered number type.
- **No crossing events.** The order of horizontal segments by $y$ never changes, so the status needs no swaps.
- **Output in sweep order.** Pairs come out by increasing $x$ of the vertical segment, and for one vertical segment by increasing $y$.
- **Offline.** All segments are needed for the sort, and the code also needs all $y$ values in advance.

## Variants and improvements

- **Counting.** To count the pairs, replace the walk of line L7 by a count of the active segments in $[y_1, y_2]$, two prefix sums in a Fenwick tree over the $y$ values. This takes $O(n \log n)$ time for any $k$.
- **Rectangles.** The [rectangle intersection reporting](/rectangle-intersection-reporting/) problem reduces to this sweep for the crossing edges plus a point-enclosure test for nested rectangles; see the [rectangle intersection sweep](/rectangle-intersection-sweep/). There, the status holds intervals instead of points, and a [segment tree](/segment-tree/) or an [interval tree](/interval-tree/) replaces the ordered set.
- **General segments.** For segments in arbitrary directions, the order of the active segments changes at crossings; use the [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/).
- **Fixed-direction sets.** Segments in a constant number $c$ of directions can be handled by running the method on each pair of directions after a shear, with $O(c^2)$ sweeps.

## When to use it

Use it for rectilinear data: wires of a circuit layout, walls of floor plans, edges of axis-parallel rectangles and grid-like maps. It is simpler and faster than a general segment sweep, and it needs no arithmetic at all. For a few hundred segments, the test of all pairs is also fine. If only a yes or no answer is needed, stop at the first non-empty query, or use counting.

## Pitfalls

- **Wrong order at equal $x$.** If deletes come before queries at the same $x$ (line L2), a vertical segment that touches the right end of a horizontal one misses it. If queries come before inserts, it misses a touch at the left end. Use inserts, then queries, then deletes.
- **A query that scans all of $T$.** Testing every active segment at line L7 costs $\Theta(|T|)$ per query and $\Theta(n^2)$ in total, even when $k = 0$. Find the first key by a search and walk only through the answers.
- **Keys that are not unique.** Several active segments can have the same $y$. A set keyed by $y$ alone loses all but one. Key by the pair (y, index), or keep a bucket per $y$ as the code does.
- **Unordered end points.** If an input has $x_1 > x_2$, its insert comes after its delete and the segment is never active. Put the end points in order before line L1.

## Implementations

## History

The rectilinear case was one of the first output-sensitive problems of computational geometry. Bentley and Ottmann treated it in their 1979 paper on reporting and counting intersections, with a one-dimensional range query for each vertical segment. Bentley and Wood (1980) used the same sweep, together with segment trees for point enclosure, to report the intersecting pairs of $n$ rectangles in optimal $O(n \log n + k)$ time. Preparata and Shamos collect these methods in their chapter on the geometry of rectangles.

## References
