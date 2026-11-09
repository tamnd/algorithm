---
tag: G9R6WH
kind: algorithm
slug: bentley-ottmann-algorithm
name: Bentley-Ottmann algorithm
aliases: [Bentley-Ottmann sweep, bentley-ottmann]
area: geometry/intersections
level: core
summary: Plane sweep that reports all k intersection points of n segments in O((n + k) log n) time, with the crossing points added to the event queue as they are found.
solves: [all-segment-intersections]
model: real-ram
complexity:
  vars: {n: the number of segments, k: the number of intersection points}
  time: {worst: O((n + k) log n)}
  space: {extra: O(n + k)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1979
  people: [Jon Louis Bentley, Thomas A. Ottmann]
  note: Bentley and Ottmann published the sweep for reporting and counting geometric intersections in IEEE Transactions on Computers in 1979; Brown noted in 1981 that deleting the events of pairs that stop being neighbors brings the space down to O(n).
prereqs: [all-segment-intersections, shamos-hoey-algorithm, segment-intersection-point, event-queue, sweep-status-structure, priority-queue, balanced-binary-search-tree]
see_also: [sweep-line-technique, sweep-invariant, degeneracy-in-sweeps, chazelle-edelsbrunner-algorithm, red-blue-intersection, orthogonal-segment-intersection-sweep, doubly-connected-edge-list, trapezoidal-map]
sources:
  - paper: doi:10.1109/TC.1979.1675432
    title: Jon L. Bentley and Thomas A. Ottmann, Algorithms for reporting and counting geometric intersections, IEEE Transactions on Computers C-28(9), 1979, 643-647
    locator: the whole paper (the sweep with crossing points as events and the O((n + k) log n) bound)
  - paper: doi:10.1109/tc.1981.6312179
    title: K. Q. Brown, Comments on "Algorithms for reporting and counting geometric intersections", IEEE Transactions on Computers C-30(2), 1981, 147-148
    locator: the whole note (keep in the queue only the crossings of current neighbors, O(n) space)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 2, Section 2.1, Line Segment Intersection (algorithms FINDINTERSECTIONS, HANDLEEVENTPOINT and FINDNEWEVENT, the sets U(p), L(p) and C(p), and the analysis by the planar graph)
  - paper: doi:10.1137/0220029
    title: János Pach and Micha Sharir, On vertical visibility in arrangements of segments and the queue size in the Bentley-Ottmann line sweeping algorithm, SIAM Journal on Computing 20(3), 1991, 460-470
    locator: the bound on the queue size of the version without deletions
---

The Bentley-Ottmann algorithm reports all $k$ points where $n$ segments in the plane intersect, in $O((n + k) \log n)$ time. It extends the [Shamos-Hoey sweep](/shamos-hoey-algorithm/): a vertical line moves from left to right, a [balanced search tree](/balanced-binary-search-tree/) keeps the segments that cross the line in vertical order, and a [priority queue](/priority-queue/) of [event points](/event-point/) holds the end points and the crossing points found so far. At each crossing, the segments through it are reversed in the status, and the new neighbors are tested. It is the standard output-sensitive method for [reporting all segment intersections](/all-segment-intersections/), and it is optimal up to the factor $\log n$ on the $k$ term.

## In plain words

Sweep a vertical line from left to right. Keep the segments that cross the line sorted from bottom to top. Two segments that cross are neighbors in this order just before the crossing, so you only need to test neighbors.

Unlike the yes-or-no test, the sweep does not stop at the first crossing. When the test of two neighbors finds a crossing to the right of the line, put that point into the list of upcoming stops. When the line reaches the crossing, the segments through it change their order: the one that was lowest goes to the top. Reverse them in the sorted list, report the point, and test the new neighbors at the two ends of the reversed group. Each stop costs a few steps of a search tree, so the total time grows with the number of segments plus the number of crossings.

## The problem

The input is a list $S$ of $n$ closed segments with rational end points. The output is every point that lies on two or more segments, together with the set of segments through it. When two collinear segments overlap in a segment of positive length, they have infinitely many common points, and the algorithm reports them at the end points of the overlap, which are end points of input segments. So the output is the set $R$ of points that lie on two or more segments and are either an end point or the only common point of some pair. Let $k = |R|$.

Notation: points are $p = (x, y)$, and $p < q$ in lexicographic order when $p_x < q_x$, or $p_x = q_x$ and $p_y < q_y$. Each segment $s$ has end points $l(s) \le r(s)$. $\mathrm{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$, positive for a counterclockwise turn. $Q$ is the event queue, $T$ the status (bottom to top), and $U(p)$ the set of segments of positive length with $l(s) = p$. No [general position](/general-position/) is assumed.

## The algorithm

```pseudo id=main
BENTLEY-OTTMANN(S)
L1  name the end points of each s ∈ S so that l(s) ≤ r(s); Q ← all end points, without repeats
L2  T ← empty sequence of segments, ordered from bottom to top
L3  while Q is not empty do
L4      p ← extract the smallest point of Q
L5      [i, j) ← the block of t ∈ T with orient(l(t), r(t), p) = 0, by two binary searches
L6      A ← U(p) ∪ T[i .. j) ∪ the segments of length zero at p
L7      if |A| ≥ 2 then report p with A
L8      delete T[i .. j) from T
L9      N ← U(p) and the segments of T[i .. j) with r(t) ≠ p, sorted by slope, a vertical segment last
L10     insert N into T at position i
L11     if N is empty then FIND-EVENT(T[i − 1], T[i], p)
L12     else FIND-EVENT(T[i − 1], N[first], p); FIND-EVENT(N[last], T[i + |N|], p)

FIND-EVENT(a, b, p)
L13 if a and b exist and a ∩ b is a single point x with x > p and x was never in Q then insert x into Q
```

The queue $Q$ returns points in lexicographic order. This is the order in which a line that is turned a tiny bit clockwise from the vertical meets them, so a vertical segment is swept from its lower end to its upper end like any other segment. Line L5 finds the segments of $T$ that pass through $p$: they form one block, because along $T$ the sign of $\mathrm{orient}(l(t), r(t), p)$ goes from positive ($p$ above $t$) to zero to negative. Line L6 collects all segments through $p$: those that start at $p$, those in the block, and degenerate ones. De Berg et al. call these sets $U(p)$, $L(p)$ and $C(p)$.

Lines L8 to L10 replace the block by the segments that continue to the right of $p$, in their order just to the right of $p$, which is the order of their slopes. This reverses the order of the segments that cross at $p$. Collinear overlapping segments have the same slope, and they keep a fixed order by index. Lines L11 and L12 test the pairs that became neighbors. FIND-EVENT computes the crossing exactly with the [segment intersection](/segment-intersection-point/) predicate, with coordinates of type `Fraction`, and keeps only crossings to the right of the sweep.

## Example

Take $s_0 = (0,0)$-$(6,6)$, $s_1 = (0,6)$-$(6,0)$, $s_2 = (0,3)$-$(6,3)$, $s_3 = (1,0)$-$(5,4)$ and the vertical $s_4 = (4,0)$-$(4,6)$. The table shows each event, the report, the status after line L10 (bottom to top) and the new points that FIND-EVENT puts into $Q$.

| event $p$ | reported set | $T$ after the event | new in $Q$ |
| --- | --- | --- | --- |
| (0,0) | | $s_0$ | |
| (0,3) | | $s_0, s_2$ | (3,3) |
| (0,6) | | $s_0, s_2, s_1$ | |
| (1,0) | | $s_3, s_0, s_2, s_1$ | |
| (3,3) | $s_0, s_1, s_2$ | $s_3, s_1, s_2, s_0$ | (7/2, 5/2) |
| (7/2, 5/2) | $s_1, s_3$ | $s_1, s_3, s_2, s_0$ | (4,3) |
| (4,0) | | $s_4, s_1, s_3, s_2, s_0$ | (4,2) |
| (4,2) | $s_1, s_4$ | $s_1, s_4, s_3, s_2, s_0$ | |
| (4,3) | $s_2, s_3, s_4$ | $s_1, s_2, s_3, s_4, s_0$ | (4,4) |
| (4,4) | $s_0, s_4$ | $s_1, s_2, s_3, s_0, s_4$ | |
| (4,6), (5,4), (6,0), (6,3), (6,6) | | the right end points remove $s_4, s_3, s_1, s_2, s_0$ | |

At $(3,3)$ three segments cross, and line L9 puts them in the order of their slopes $-1, 0, 1$, which reverses them. The vertical segment $s_4$ enters at its lower end $(4,0)$ at the bottom of $T$. At each event on it, it is in the block of line L5 and goes back in as the last element of $N$, so it climbs through $T$: at $(4,2)$ it passes $s_1$, at $(4,3)$ it passes $s_2$ and $s_3$, and at $(4,4)$ it passes $s_0$. The output has $k = 5$ points.

## Correctness

The invariant is that after each event, $T$ holds the segments that cross the sweep line just to the right of the event, sorted by the height of the crossing, and $Q$ holds every end point that is still ahead. The key lemma is that the next intersection point $q$ is in $Q$ when the sweep reaches it. If $q$ is not an end point, the segments through $q$ form a block of $T$ just before $q$, two consecutive ones in this block have different slopes and meet only at $q$, and they were tested at the event that made them neighbors. At $q$ itself, the binary searches find exactly the segments through $q$, and sorting the continuing segments by slope restores the invariant. Vertical segments are handled by a shear $(x, y) \mapsto (x + \delta y, y)$ for a tiny $\delta$, which changes no decision of the algorithm and makes no segment vertical. The full proof is in the correctness proof below.

## Complexity

- **Events.** The queue receives at most $2n$ end points and the $k' \le k$ crossing points that are not end points, so there are at most $2n + k$ events. Each operation on $Q$, a [binary heap](/binary-heap/) or a balanced tree, takes $O(\log(n + k)) = O(\log n)$ time, since $k \le \binom{n}{2} + 2n$.
- **Each event.** Let $m(p)$ be the number of segments through $p$. With a balanced tree for $T$, lines L5 to L10 take $O((1 + m(p)) \log n)$ time, and lines L11 to L13 take $O(\log n)$.
- **Sum over the events.** If no two segments overlap, the segments form a planar graph whose vertices are the event points and whose edges are the pieces of segments between them. A segment through $p$ adds at least 1 to the degree of $p$, so $\sum_p m(p) \le 2E \le 6V = O(n + k)$ by [Euler's formula](/euler-formula/). The total is $O((n + k) \log n)$ time in the worst case on the [real RAM](/real-ram/). With overlapping segments, replace $O(n + k)$ by the total size of the output, $\sum_{p \in R} m(p)$.
- **Space.** $O(n + k)$, because $Q$ keeps every crossing found. Brown's variant deletes the crossing of two segments when they stop being neighbors, so $Q$ holds $O(n)$ points, one per pair of neighbors, and the space is $O(n)$.
- **Optimality.** The lower bound for the problem is $\Omega(n \log n + k)$ in the algebraic decision tree model, so the algorithm is optimal when $k = O(n)$ and loses a factor $\log n$ when $k$ is large. The [Chazelle-Edelsbrunner algorithm](/chazelle-edelsbrunner-algorithm/) reaches $O(n \log n + k)$.
- **The Python code.** $T$ is a Python list with binary search, so each update also moves up to $n$ references. A balanced tree removes this term. All coordinates are exact `Fraction` values. With integer input of absolute value at most $M$, a crossing point has a denominator of order $M^2$ and numerators of order $M^3$, and every test at a crossing point works with numbers bounded by a fixed power of $M$, because crossing points are never computed from other crossing points.

## Properties

- **Output-sensitive.** The cost depends on $k$, so the algorithm is fast when the segments cross rarely, which is common in practice.
- **Exact with rational input.** Crossing points are rational, and every test is a sign of a polynomial in rational numbers. Each crossing point is computed from the input segments, never from another computed point, so the degree of the numbers stays bounded.
- **One pass, left to right.** The output comes in lexicographic order of the points.
- **Not online and not dynamic.** All segments must be known before the sweep.

## Variants and improvements

- **Optimal deterministic algorithms.** Chazelle and Edelsbrunner (1988, 1992) reach $O(n \log n + k)$ time with $O(n + k)$ space; see the [Chazelle-Edelsbrunner algorithm](/chazelle-edelsbrunner-algorithm/). Balaban (1995) reaches the same time with $O(n)$ space.
- **Randomized algorithms.** Clarkson and Shor (1989) and Mulmuley (1988) build the [trapezoidal map](/trapezoidal-map/) of the segments by [randomized incremental construction](/randomized-incremental-construction/) in $O(n \log n + k)$ expected time.
- **Map overlay.** When the segments are the edges of two [planar subdivisions](/planar-subdivision/), the same sweep builds the overlay in a [doubly connected edge list](/doubly-connected-edge-list/) in $O((n + k) \log n)$ time. When each color class has no inner crossings, faster methods exist; see [red-blue intersection](/red-blue-intersection/).
- **Orthogonal segments.** For horizontal and vertical segments, the [orthogonal sweep](/orthogonal-segment-intersection-sweep/) reports all $k$ crossings in $O(n \log n + k)$ time with no crossing events.
- **Counting.** Counting the intersecting pairs without reporting them takes $O(n^{4/3} \mathrm{polylog}\, n)$ time by cuttings, which is better than this sweep when $k$ is large.

## When to use it

Use it as the default for reporting the crossings of segments: in map overlay, in Boolean operations on polygons, in finding the self-intersections of a polygon and in building the arrangement of a set of curves. It is simpler than the optimal deterministic methods, and its $\log n$ factor rarely matters. If $k$ is close to $n^2$, the brute-force test of all pairs in $\Theta(n^2)$ time is simpler and as fast. Use exact arithmetic, or at least exact predicates, because the order of $T$ must stay consistent; rounding errors in the crossing points are the main source of failures in practice.

## Pitfalls

- **Assuming general position.** Code that assumes no vertical segments and no three segments through a point fails on real data. Use the lexicographic order of line L4, the block search of line L5 and the slope sort of line L9.
- **Swapping only two segments at a crossing.** When three or more segments meet at $p$, swapping a pair gives a wrong order. Line L9 reverses the whole block by sorting by slope.
- **Inserting a crossing twice.** Two pairs can report the same crossing, and the same pair can become neighbors again. Without the test "never in $Q$" of line L13, a point is processed twice. A set of seen points, or a queue with no repeats, prevents this.
- **Crossings to the left of the sweep.** A new pair of neighbors can meet at $p$ or before it. Line L13 inserts only points $x > p$.
- **Floating-point crossing points.** A rounded crossing point can fall on the wrong side of a nearby segment, so the binary search of line L5 sees an inconsistent order. Use `fractions.Fraction`, or snap-rounding with a proven model.

## Implementations

## History

Jon Bentley and Thomas Ottmann published the algorithm in 1979, extending the detection sweep of Shamos and Hoey (1976) to report all intersections in $O((n + k) \log n)$ time. Kevin Brown pointed out in 1981 that the queue needs only the crossings of current neighbors, which gives $O(n)$ space. Pach and Sharir (1991) studied how large the queue grows without these deletions. The question of an optimal $O(n \log n + k)$ algorithm was settled by Chazelle and Edelsbrunner in 1988, and later by Balaban in 1995 with linear space. The handling of degenerate cases with the sets $U(p)$, $L(p)$ and $C(p)$ follows the textbook of de Berg, Cheong, van Kreveld and Overmars.

## References
