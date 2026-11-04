---
tag: KGSR21
kind: algorithm
slug: rectangle-intersection-sweep
name: Rectangle intersection sweep
aliases:
- sweep for rectangle overlap
area: techniques/sweep-line
level: core
summary: Sweep over x-intervals of rectangles, checking y-overlap against active rectangles.
solves: [rectangle-intersection-detection]
model: real-ram
complexity:
  vars: {n: the number of rectangles}
  time: {worst: Θ(n log n), average: Θ(n log n), best: O(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [sweep-line-technique, balanced-binary-search-tree, rectangle-intersection-detection]
see_also: [interval-tree, segment-tree, event-queue, sweep-status-structure, sweep-invariant, degeneracy-in-sweeps, segment-intersection-detection, rectangle-union-sweep]
sources:
  - paper: "J. L. Bentley and D. Wood, An optimal worst case algorithm for reporting intersections of rectangles, IEEE Transactions on Computers C-29(7) (1980), doi:10.1109/TC.1980.1675628"
    locator: pages 571 to 577 (the sweep over x with an active set of y-intervals, and the reporting bound O(n log n + k))
  - paper: "M. I. Shamos and D. Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science (1976), doi:10.1109/SFCS.1976.16"
    locator: pages 208 to 215 (the sweep that tests only neighbors in the status order)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 2 (plane sweep, event queue and status structure) and Chapter 10 (interval trees and segment trees)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction
    locator: Chapter 8, The Geometry of Rectangles
---

The rectangle intersection sweep decides whether any two of $n$ closed axis-parallel rectangles intersect, in $O(n \log n)$ time. It is a [sweep line](/sweep-line-technique/) over $x$: a rectangle is *active* while the line crosses it, and the algorithm keeps the $y$-intervals of the active rectangles in a [balanced search tree](/balanced-binary-search-tree/). Until the first intersection is found, the active $y$-intervals are pairwise disjoint, so a new interval must be tested only against its two neighbors in the tree. With an [interval tree](/interval-tree/) in place of the plain tree, the same sweep reports all $k$ intersecting pairs in $O(n \log n + k)$ time, the optimal bound that Bentley and Wood first reached.

## In plain words

Slide a vertical line across the page from left to right. At each moment, some rectangles are cut by the line. Look at the parts of the line that these rectangles cover. Two rectangles intersect only if, at some moment, both are cut by the line and their parts of the line overlap.

So the line stops only where a rectangle starts or ends. When a rectangle starts, add its part of the line to a sorted list. When it ends, remove it. As long as no overlap has been found, the parts in the list do not overlap, so they sit one above the other like floors of a building. A new part can then overlap only the part just below it or the part just above it. Two checks at each start are enough.

## The problem

The input is a list of $n$ rectangles $R_i = [a_i, b_i] \times [c_i, d_i]$ with $a_i \le b_i$ and $c_i \le d_i$. They are closed, so two rectangles that share only an edge or a corner intersect. The output is a pair $i \ne j$ with $R_i \cap R_j \ne \emptyset$, or NONE if no such pair exists. This is [rectangle intersection detection](/rectangle-intersection-detection/). Two closed rectangles intersect if and only if their $x$-intervals intersect and their $y$-intervals intersect:

$$R_i \cap R_j \ne \emptyset \iff a_i \le b_j,\ a_j \le b_i,\ c_i \le d_j \text{ and } c_j \le d_i.$$

## The algorithm

Each rectangle gives two [event points](/event-point/): an insert event at $x = a_i$ and a delete event at $x = b_i$. The events are sorted by $x$, and at equal $x$ each insert comes before each delete. The status $S$ is an ordered set of the active rectangles, ordered by the key $(c_i, i)$: the lower $y$-end, with the index to break ties.

```pseudo id=main
RECT-INTERSECT(R[1 .. n])                  ▷ R[i] = [a_i, b_i] × [c_i, d_i], closed
L1  E ← the events (a_i, 0, i) and (b_i, 1, i) for i = 1 .. n     ▷ 0 = insert, 1 = delete
L2  sort E lexicographically                ▷ equal x: inserts before deletes
L3  S ← an empty ordered set, ordered by the key (c_i, i)
L4  for each event (x, t, i) of E, in order do
L5      if t = 0 then
L6          insert i into S
L7          p ← the predecessor of i in S, s ← the successor of i in S
L8          if p exists and d_p ≥ c_i then return (p, i)
L9          if s exists and c_s ≤ d_i then return (i, s)
L10     else delete i from S
L11 return NONE
```

Line L8 tests the active interval just below the new one: the two meet if the top of the lower one reaches the bottom of the new one. Line L9 tests the interval just above. A delete event needs no test: removing an interval cannot make two other intervals overlap. The order "insert before delete" at equal $x$ makes rectangles that touch along a vertical edge active at the same time, so they are found. For open rectangles, use "delete before insert" and strict tests in lines L8 and L9 (see Pitfalls).

## Example

Take the five rectangles

| name | $i$ | $[a, b]$ | $[c, d]$ |
| --- | --- | --- | --- |
| A | 1 | $[1, 3]$ | $[1, 2]$ |
| B | 2 | $[2, 5]$ | $[4, 6]$ |
| C | 3 | $[4, 7]$ | $[0, 3]$ |
| D | 4 | $[6, 9]$ | $[5, 7]$ |
| E | 5 | $[8, 10]$ | $[1, 4]$ |

The sweep runs as follows. The status lists the active $y$-intervals from bottom to top.

| $x$ | event | neighbors of the new interval | status after the event |
| --- | --- | --- | --- |
| 1 | insert A $[1, 2]$ | none | A$[1,2]$ |
| 2 | insert B $[4, 6]$ | below: A, top 2 < 4 | A$[1,2]$, B$[4,6]$ |
| 3 | delete A | | B$[4,6]$ |
| 4 | insert C $[0, 3]$ | above: B, bottom 4 > 3 | C$[0,3]$, B$[4,6]$ |
| 5 | delete B | | C$[0,3]$ |
| 6 | insert D $[5, 7]$ | below: C, top 3 < 5 | C$[0,3]$, D$[5,7]$ |
| 7 | delete C | | D$[5,7]$ |
| 8 | insert E $[1, 4]$ | above: D, bottom 5 > 4 | E$[1,4]$, D$[5,7]$ |
| 9 | delete D | | E$[1,4]$ |
| 10 | delete E | | empty |

No test succeeds, so the answer is NONE. Now add F $= [5, 6] \times [3, 4]$ as rectangle 6. It touches B at the corner $(5, 4)$ and C along the segment from $(5, 3)$ to $(6, 3)$. At $x = 5$ there are two events: insert F and delete B. The insert comes first, so the status is C$[0,3]$, F$[3,4]$, B$[4,6]$. The neighbor below F is C, with top $3 \ge 3$, and line L8 returns the pair (C, F). If the delete of B came first, the corner touch of B and F would be lost, but the touch of C and F would still be found.

## Correctness

The returned pair always intersects: when $i$ is inserted at $x = a_i$, an active rectangle $p$ has $a_p \le a_i$ and its delete event comes later, so $b_p \ge a_i$; the $x$-intervals meet, and lines L8 and L9 test the $y$-intervals. For the converse, take the intersecting pair whose later insert event comes first in $E$. Up to that event, no two active intervals overlap, so the active intervals are pairwise disjoint and ordered by their lower ends. In such a set, a new interval that meets some active interval meets its predecessor or its successor. So line L8 or L9 succeeds at that event, if no earlier test succeeded. The full proof is below.

## Complexity

- **Sorting.** Line L2 sorts $2n$ events in $O(n \log n)$ time.
- **The loop.** Each of the $2n$ events does at most one insert or delete and at most two neighbor queries on $S$. With a [balanced binary search tree](/balanced-binary-search-tree/), such as a [red-black tree](/red-black-tree/), each costs $O(\log n)$, so the loop costs $O(n \log n)$.
- **Total.** $O(n \log n)$ time in the worst case, and $\Theta(n)$ extra space for $E$ and $S$.
- **Lower bound.** Every algorithm for the problem needs $\Omega(n \log n)$ operations in the [algebraic decision tree](/algebraic-decision-tree/) model in the worst case. The proof is on the [problem page](/rectangle-intersection-detection/). So the sweep is optimal in that model. It can stop early on an input with an intersection, so its best case is less than $n \log n$, but the sort alone costs $\Theta(n \log n)$ in the worst case.

## Properties

- **Comparison-based.** The algorithm compares coordinates only. It needs no arithmetic, so it is exact for integers and for floats.
- **Not online.** It needs all the rectangles before it starts, to sort the events.
- **Early exit.** It stops at the first pair that it finds, which is not always the pair with the smallest $x$ of contact.
- **Deterministic.** The output depends only on the input and the tie-breaking key $(c_i, i)$.

## Variants and improvements

- **Report all pairs.** Test each new interval against all the active intervals that it meets, not only against its neighbors. With an [interval tree](/interval-tree/) as the status, an [interval overlap query](/interval-overlap-query/) returns the $k_i$ active intervals that meet the new one in $O(\log n + k_i)$ time, so the whole sweep reports all $k$ pairs in $O(n \log n + k)$ time. Bentley and Wood (1980) first reached this bound, and it is optimal.
- **Count the pairs.** Count, at each insert, the active intervals that meet $[c_i, d_i]$: the number of active intervals minus those with top below $c_i$ minus those with bottom above $d_i$. Two [Fenwick trees](/fenwick-tree/) over the compressed $y$-coordinates, one for the tops and one for the bottoms of the active intervals, give $O(n \log n)$ time in total.
- **Open rectangles.** Process deletes before inserts at equal $x$, and use $d_p > c_i$ and $c_s < d_i$ in lines L8 and L9. Then only overlaps of interiors count, and the rectangles need $a_i < b_i$ and $c_i < d_i$ (an open rectangle of zero width is empty). The same key and the same proof work.
- **Broad phase of collision detection.** Games and physics engines run the same sweep on bounding boxes, under the name "sweep and prune", and keep the sorted event list from one frame to the next, since it changes little.
- **Higher dimensions.** In $d$ dimensions, sweep along one axis and keep a $(d-1)$-dimensional structure of the active boxes, built from [segment trees](/segment-tree/) or [range trees](/range-tree/).

## When to use it

Use the neighbor sweep when you need only a yes or no answer, or one witness pair, for many rectangles: it is short, exact and $O(n \log n)$. Use the interval tree version when you need all the pairs. For a few hundred rectangles, the $O(n^2)$ test of all pairs is simpler and fast enough. When the rectangles move a little at each step, as in a game, keep the sorted events and re-sort them with insertion sort at each frame.

## Pitfalls

- **Delete before insert.** If line L2 puts a delete before an insert at the same $x$, two closed rectangles that touch along a vertical edge are never active together, and the pair is missed. For closed rectangles, inserts come first.
- **Testing only one neighbor.** Line L8 alone misses a new interval that overlaps the interval above it, and line L9 alone misses the interval below. Both tests are needed.
- **Continuing after an overlap.** The neighbor test is complete only while the active intervals are disjoint. If you change the algorithm to keep going after a hit, to report more pairs, it can miss pairs: three active intervals can then overlap in a way that the neighbors of a new interval do not show. To report all pairs, use the interval tree variant.
- **Keys with equal lower ends.** Two active intervals with the same $c$ need a tie-breaker in the key, here the index $i$. A set keyed by $c$ alone would merge them or reject the second insert.

## Implementations

## History

Shamos and Hoey (1976) used a sweep that tests only neighbors in the status order to decide in $O(n \log n)$ time whether any two of $n$ segments intersect. Bentley and Wood (1980) gave a sweep algorithm for rectangles that reports all $k$ intersecting pairs in $O(n \log n + k)$ time, and showed that this is optimal. Their motivation was the design of integrated circuits, where a layout has many rectangles that must not overlap. Preparata and Shamos give the rectangle problems a chapter of their book.

## References
