---
tag: 877716
kind: technique
slug: sweep-line-technique
name: Sweep line technique
aliases:
- plane sweep
- line sweep
- scanline
- sweep algorithm
area: techniques/sweep-line
level: intro
summary: Move an imaginary line across the plane, process events in order, and maintain a status structure of the objects it crosses.
prereqs: [sorting-problem, priority-queue, balanced-binary-search-tree, loop-invariant]
see_also: [event-point, event-queue, sweep-status-structure, sweep-invariant, degeneracy-in-sweeps, rotational-sweep, event-driven-simulation, divide-and-conquer-paradigm]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 2, Section 2.1, Line Segment Intersection (the plane sweep, the event queue and the status structure)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction
    locator: Chapter 7, Intersections (plane sweep for segment intersection), and Chapter 8, The Geometry of Rectangles
  - paper: "M. I. Shamos and D. Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science (1976), doi:10.1109/SFCS.1976.16"
    locator: pages 208 to 215 (the sweep that tests only neighbors in the status order)
  - paper: "J. L. Bentley and T. A. Ottmann, Algorithms for reporting and counting geometric intersections, IEEE Transactions on Computers C-28(9) (1979), doi:10.1109/TC.1979.1675432"
    locator: pages 643 to 647 (the sweep with intersection points as new events)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 33.2, Determining whether any pair of segments intersects
---

The sweep line technique solves a geometric problem by moving an imaginary line across the plane and stopping only at a finite set of [event points](/event-point/). At each stop it updates a [status structure](/sweep-status-structure/) that holds the objects the line crosses, in their order along the line, and it looks for the answer only among objects that are close in this order. A two-dimensional static problem becomes a sequence of one-dimensional dynamic problems, and many problems that take $\Theta(n^2)$ time by brute force take $O(n \log n)$ or $O((n + k) \log n)$ time with a sweep. Shamos and Hoey (1976) used it to detect a segment intersection, and Bentley and Ottmann (1979) used it to report all intersections.

## In plain words

Put a ruler upright at the left edge of a drawing and slide it to the right. At each moment the ruler touches some of the shapes, and you can list them from bottom to top. This list changes only at a few places: where a shape starts, where a shape ends, and where two shapes cross and swap places in the list. Between those places nothing in the list changes, so you do not have to look.

The method is: make the list of places where something can happen, sort it from left to right, and visit the places in that order. At each place, update the list of shapes that the ruler touches, and check only the shapes that are next to each other in that list. Two shapes that are far apart in the list cannot meet before the shapes between them move out of the way.

## When it applies

- **The objects are local in one direction.** Each object occupies an interval of $x$ values (a segment, a rectangle, an interval, a disk), so it is "alive" for one stretch of the sweep.
- **The answer is decided by objects alive at the same time.** Two rectangles intersect only if their $x$-intervals overlap. Two segments cross only where both are cut by the same vertical line.
- **Interaction is local in the order along the line.** The first event of interest (the leftmost crossing, the closest pair, the first overlap) happens between two objects that are neighbors in the order along the line just before it. This turns $\binom{n}{2}$ candidate pairs into $O(n)$ tests.
- **The input is known in advance.** The events are sorted before the sweep starts. The technique is offline. An online input needs a different structure.
- **A brute force looks at all pairs.** A $\Theta(n^2)$ all-pairs test is the usual sign that a sweep can do better.

## The template

The line is vertical and moves from left to right, so the key of an event is its $x$-coordinate, with a fixed rule for ties (see [degeneracy in sweeps](/degeneracy-in-sweeps/)). De Berg et al. sweep a horizontal line from top to bottom; this is the same method after a rotation of the plane. The words in angle brackets are holes that each application fills.

```pseudo id=main
SWEEP(S)                                   ▷ S: the input objects
L1  Q ← ⟨static events⟩ of S, ordered by ⟨event key⟩   ▷ the event queue
L2  T ← an empty ⟨status structure⟩                     ▷ the objects that cross the line
L3  while Q is not empty do
L4      p ← remove the first event from Q
L5      ⟨update⟩ T at p                    ▷ insert, delete or reorder the objects of p
L6      for each pair (s, t) that became neighbors in T at p do
L7          ⟨check⟩ s and t                ▷ may add a dynamic event to Q, or stop with an answer
L8      ⟨report⟩ the output found at p
L9  return ⟨answer⟩
```

**The holes.**

- **Static events** (line L1): the positions known before the sweep, usually the endpoints of the objects. See [event point](/event-point/).
- **Event key** (line L1): the $x$-coordinate, with a tie rule. The tie rule decides whether objects that touch count as meeting.
- **Status structure** (line L2): an ordered container of the objects that cross the line. A [balanced binary search tree](/balanced-binary-search-tree/) gives insert, delete, and neighbor queries in $O(\log n)$ time. When the status only needs a count or a measure, a counter or a [segment tree](/segment-tree/) is enough. See [sweep status structure](/sweep-status-structure/).
- **Update** (line L5): insert the objects that start at $p$, delete the objects that end at $p$, and reverse the order of the objects that cross at $p$.
- **Check** (lines L6 to L7): compare only the new neighbor pairs. In [Bentley-Ottmann](/bentley-ottmann-algorithm/) the check finds the crossing of two neighbors to the right of the line and adds it to $Q$ as a *dynamic* event. In a detection problem the check stops the sweep.
- **Report and answer** (lines L8 to L9): the output at $p$, or a running value such as a maximum or a sum.

The event queue $Q$ is a sorted array when all events are static, and a [priority queue](/priority-queue/) when the check adds events during the sweep. See [event queue](/event-queue/).

**Why it is correct.** Each sweep has a [sweep invariant](/sweep-invariant/): before the event at position $x$, the status holds exactly the objects that cross the line just left of $x$, in order, and every output item to the left of $x$ is reported. The invariant is a [loop invariant](/loop-invariant/) of the loop at line L3. It holds because nothing changes between two consecutive events; the [event point](/event-point/) page proves this for segments.

**Cost.** Let $E$ be the number of events and let each status operation cost $O(\log n)$. Sorting or queueing the events costs $O(E \log E)$, and each event does a constant number of status operations and checks, so the sweep runs in $O(E \log E + E \log n)$ time. With $E = 2n$ static events this is $O(n \log n)$. With $k$ dynamic events, as in Bentley-Ottmann, it is $O((n + k) \log n)$, because $k \le \binom{n}{2}$ gives $\log E = O(\log n)$.

**A filled-in instance.** Take the closed intervals $[1, 4]$, $[2, 6]$, $[3, 5]$, $[8, 10]$ and $[9, 12]$ on a line. The events are the ten endpoints, with starts before ends at equal $x$. The status is one integer $c$, the number of intervals that contain the current point. The update adds 1 at a start and subtracts 1 at an end. Before each update, the length from the previous event is added to the covered length when $c > 0$.

| $x$ | event | length added | $c$ after | covered length | max $c$ |
|---|---|---|---|---|---|
| 1 | start | 0 | 1 | 0 | 1 |
| 2 | start | 1 | 2 | 1 | 2 |
| 3 | start | 1 | 3 | 2 | 3 |
| 4 | end | 1 | 2 | 3 | 3 |
| 5 | end | 1 | 1 | 4 | 3 |
| 6 | end | 1 | 0 | 5 | 3 |
| 8 | start | 0 | 1 | 5 | 3 |
| 9 | start | 1 | 2 | 6 | 3 |
| 10 | end | 1 | 1 | 7 | 3 |
| 12 | end | 2 | 0 | 9 | 3 |

The union has length 9 and the largest number of intervals with a common point is 3. These are the [interval union length](/interval-union-length/) and [maximum overlap](/maximum-overlap/) problems, solved by [sweep union length](/sweep-union-length/) and [sweep maximum overlap](/sweep-maximum-overlap/) in $O(n \log n)$ time.

## Classic examples

From simple to hard:

1. **Union length and maximum overlap of intervals.** The instance above. Status: a counter. $2n$ events, $O(n \log n)$ time for the sort.
2. **[Closest pair by sweep](/closest-pair-sweep-line/).** Events: the $n$ points in $x$ order. Status: the points within the current best distance $d$ to the left of the line, ordered by $y$. A new point is compared only with the points in a $2d$-high window of the status, which hold a constant number of points.
3. **[Rectangle intersection detection](/rectangle-intersection-sweep/).** Events: the left and right edges. Status: the $y$-intervals of the active rectangles. While no overlap is found the intervals are disjoint, so a new interval only needs the two neighbors. $O(n \log n)$ time.
4. **[Segment intersection detection](/shamos-hoey-algorithm/) (Shamos-Hoey).** Events: the $2n$ endpoints. Status: the segments ordered by $y$ at the line. The leftmost crossing is between two neighbors, so neighbor tests after each insert and delete find a crossing if one exists. $O(n \log n)$ time, and $\Omega(n \log n)$ is a [lower bound](/segment-intersection-lower-bound/) in the [algebraic decision tree](/algebraic-decision-tree/) model. This solves [segment intersection detection](/segment-intersection-detection/).
5. **[Bentley-Ottmann](/bentley-ottmann-algorithm/).** The same sweep, but a crossing found between neighbors becomes a dynamic event, where the two segments swap. It reports all $k$ crossings in $O((n + k) \log n)$ time.
6. **[Area of a union of rectangles](/rectangle-union-sweep/).** Events: the left and right edges. Status: a [segment tree](/segment-tree/) over the compressed $y$-coordinates that keeps the covered length of the line. Between two events, the area grows by the covered length times the $x$-gap. $O(n \log n)$ time.
7. **[Skyline](/skyline-sweep/).** Events: the left and right walls of the buildings. Status: a multiset of the heights of the active buildings. The skyline changes where the maximum changes.
8. **[Monotone partition of a polygon](/monotone-polygon-partition/).** Events: the $n$ vertices, classified as start, end, split, merge or regular. Status: the polygon edges that cross the line, each with a helper vertex. Diagonals added at split and merge vertices cut the polygon into [monotone pieces](/monotone-polygon/), which are then [triangulated](/monotone-polygon-triangulation/) in linear time. $O(n \log n)$ time.
9. **[Fortune's algorithm](/fortunes-algorithm/).** Events: the $n$ sites (static) and circle events (dynamic), where a parabolic arc of the beach line shrinks to a point. Status: the beach line, the parabolic arcs in order along the line. It builds the [Voronoi diagram](/voronoi-diagram/) in $O(n \log n)$ time.
10. **[Rotational sweep](/rotational-sweep/).** The line is a ray that turns around a point. Events: the endpoints in angular order. Status: the segments that the ray crosses, ordered by distance. It computes the [visibility polygon](/visibility-polygon/) of a point in $O(n \log n)$ time, and repeated at each vertex it builds a [visibility graph](/visibility-graph/).

## Variations

- **A rotating line.** The [rotational sweep](/rotational-sweep/) turns a ray around a center. The key is the angle, and the order along the ray is by distance from the center.
- **A sweep in time.** In an [event-driven simulation](/event-driven-simulation/), the "line" is the current time. The events are the moments when something changes, for example the next collision found by [collision prediction](/collision-prediction-and-resolution/). Most events are dynamic, and many become invalid before they happen.
- **A sweep plane.** In three dimensions, a plane moves along the $z$-axis and the status is a two-dimensional structure. For the volume of a union of $n$ boxes, solving the two-dimensional [union area](/area-of-union-of-rectangles/) problem in the plane between each pair of consecutive events gives $O(n^2 \log n)$ time. [Klee's measure problem](/klee-measure-problem/) is the general case.
- **An offline sweep over queries.** Queries become events too. For [orthogonal range counting](/offline-orthogonal-range-counting/) or [dominance counting](/dominance-counting/), sort points and queries by $x$, insert the points into a [Fenwick tree](/fenwick-tree/) on $y$ as the line passes them, and answer each query when the line reaches it. See [offline query processing](/offline-query-processing/).
- **A status with no order.** When the problem asks for a count or a measure, the status is a counter or a segment tree, and the neighbor test disappears.

## Pitfalls

- **Ties between events.** Several events with the same $x$ need a fixed order. The order decides whether touching objects meet: starts before ends make intervals and rectangles closed, ends before starts make them open. A wrong order gives a wrong answer, not only a slower one. See [degeneracy in sweeps](/degeneracy-in-sweeps/).
- **A comparator that depends on the line.** The order of segments in the status is the order of their $y$-values at the current $x$, and it changes at each crossing. A key computed once at insertion, such as the $y$ of the left endpoint, compares two segments at two different $x$-values and can corrupt the tree. Compare at the current $x$. At an event point where several segments meet, they have equal $y$; break the tie by slope, which gives the order just to the right of the point.
- **Missing a test after a deletion.** When $s$ leaves the status, its old neighbors above and below become neighbors. Shamos-Hoey and Bentley-Ottmann must test this new pair. Forgetting it misses crossings.
- **Dynamic events found twice.** A pair of segments can become neighbors, be separated, and become neighbors again before they cross. Insert a crossing into $Q$ only if it is not already there, or delete it when the pair stops being neighbors.
- **Floating point.** An intersection point computed in floating point can land a little to the left of the line, which makes an event in the past, or can make the comparator inconsistent, which breaks the search tree. With integer input, compute intersections as exact fractions, or use exact [orientation tests](/orientation-test/) for all comparisons. See [floating-point arithmetic](/floating-point-arithmetic/).
- **Testing all active objects.** Testing a new object against every object in the status is correct but gives $\Theta(n^2)$ time on inputs with many long objects. The gain of the sweep comes from testing neighbors only.

## Exercises

1. For the closed intervals $[0, 3]$, $[1, 4]$, $[3, 6]$, $[5, 8]$, $[6, 9]$ and $[8, 10]$, run the counter sweep and find the largest number of intervals with a common point and the length of the union. Then change the tie rule so that the intervals are open, and find the largest overlap again. (The answers are 3, 10 and 2.)
2. You are given $n$ horizontal and vertical segments. Count the pairs of a horizontal and a vertical segment that intersect in $O(n \log n)$ time, with a sweep and a [Fenwick tree](/fenwick-tree/) on compressed $y$-coordinates. State the order of the three kinds of events at equal $x$ for closed segments.
3. Assume [general position](/general-position/): no two endpoints have the same $x$, and no three segments meet at a point. Let $p$ be the leftmost intersection point, of the segments $s$ and $t$. Prove that $s$ and $t$ are neighbors in the status right after some event whose key is at most the $x$-coordinate of $p$. Use this to prove that Shamos-Hoey finds an intersection when one exists.
4. Adapt the segment sweep to decide in $O(n \log n)$ time whether a polygon with $n$ vertices is simple (the [polygon simplicity test](/polygon-simplicity-test/)). Explain how to treat two consecutive edges, which always share an endpoint.
5. Given $n$ points in the plane, compute for each point the number of points with a smaller $x$ and a smaller $y$, in $O(n \log n)$ time. Say what the events are, how ties in $x$ are ordered, and what the status is.

## References
