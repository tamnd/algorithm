---
tag: KC8DHG
kind: algorithm
slug: sweep-maximum-overlap
name: Sweep for maximum overlap
aliases:
- Endpoint counting sweep
area: sequences/interval-problems
level: intro
summary: Sort the endpoints and track the running count of open intervals.
solves: [maximum-overlap]
model: comparison-model
complexity:
  vars: {n: the number of intervals}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [maximum-overlap, sweep-line-technique, sorting-problem, loop-invariant]
see_also: [sweep-union-length, interval-partitioning-greedy, interval-partitioning, interval-coloring-depth-theorem, event-point, degeneracy-in-sweeps]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.1, Interval Scheduling, the subsection on interval partitioning (depth as a lower bound on the number of resources)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 2, Line Segment Intersection (the plane sweep paradigm with an event queue and a status)
  - url: https://cp-algorithms.com/geometry/length-of-segments-union.html
    title: cp-algorithms, Length of the union of segments
    locator: the same event sort with a counter of open segments
---

The sweep for maximum overlap finds the depth of a family of $n$ intervals, the largest number of them that contain one common point, which is the [maximum overlap](/maximum-overlap/) problem. It sorts the $2n$ end points as [events](/event-point/), walks through them with a counter that goes up at a left end and down at a right end, and returns the largest value of the counter and where it occurred. It runs in $\Theta(n \log n)$ time. Unlike the [sweep for union length](/sweep-union-length/), the order of events at equal coordinates changes the answer, and it must match the type of the end points.

## In plain words

Write every interval as two events: "an interval opens here" and "an interval closes here". Put all events in order along the line and walk through them. Keep a counter of the intervals that are open right now. An opening adds one, a closing takes one away. The highest value the counter reaches is the answer.

When an opening and a closing fall on the same spot, you must decide which comes first. If the end spot belongs to the interval, two intervals that touch there do overlap, so count the opening first. If the end spot does not belong to it, count the closing first, so that the two never count together.

## The problem

The input is a list of $n$ intervals with end points $l_j \le r_j$, all of one type. The output is the depth $d = \max_x c(x)$, where $c(x)$ is the number of intervals that contain $x$, and a place where it is reached. The [maximum overlap](/maximum-overlap/) page defines $d$ and shows why the maximum is reached at a left end for closed and half-open intervals.

## The algorithm

```pseudo id=main
SWEEP-MAX-OVERLAP(I[1 .. n])
L1  E ← an empty list of events
L2  for each interval with ends l, r in I do append (l, +1) and (r, −1) to E
L3  sort E by coordinate; at equal coordinates put +1 first for closed intervals,
        and −1 first for half-open and open intervals
L4  count ← 0, best ← 0, at ← nil
L5  for each (x, δ) in E, in sorted order do
L6      count ← count + δ
L7      if count > best then best ← count, at ← x
L8  return (best, at)
```

Line L6 applies the event, and line L7 records a new maximum. A new maximum can occur only after a $+1$ event, so $at$ is always a left end. For closed and half-open intervals, $at$ is a point of depth $best$. For open intervals, the depth is reached on the open gap that starts at $at$, for example at its midpoint, but not at $at$ itself.

The tie rule is the whole difference between the types. For closed intervals $[l, r]$, an interval that ends at $x$ still contains $x$, so a start at $x$ must be counted while it is still open: starts first. For half-open $[l, r)$ and open $(l, r)$ intervals, an interval that ends at $x$ does not contain $x$, so it must be closed before a start at $x$ is counted: ends first.

## Example

Take $[1, 3], [2, 5], [3, 4], [5, 8], [6, 7], [8, 9], [7, 10]$ as closed intervals. Line L3 puts starts first at each tie.

| event | count after | best | at |
|---|---|---|---|
| $(1, +1)$ | 1 | 1 | 1 |
| $(2, +1)$ | 2 | 2 | 2 |
| $(3, +1)$ | 3 | 3 | 3 |
| $(3, -1)$ | 2 | 3 | 3 |
| $(4, -1)$ | 1 | 3 | 3 |
| $(5, +1)$ | 2 | 3 | 3 |
| $(5, -1)$ | 1 | 3 | 3 |
| $(6, +1)$ | 2 | 3 | 3 |
| $(7, +1)$ | 3 | 3 | 3 |
| $(7, -1)$ | 2 | 3 | 3 |
| $(8, +1)$ | 3 | 3 | 3 |
| $(8, -1)$ | 2 | 3 | 3 |
| $(9, -1)$ | 1 | 3 | 3 |
| $(10, -1)$ | 0 | 3 | 3 |

The result is $d = 3$ at the point 3, where $[1, 3]$, $[2, 5]$ and $[3, 4]$ meet. The counter also reaches 3 at 7 and at 8, but line L7 keeps the first place.

With the same numbers as half-open intervals, line L3 puts the end before the start at 3, 5, 7 and 8. The counter then goes $1, 2, 1, 2, 1, 0, 1, 2, 1, 2, 1, 2, 1, 0$, and the result is $d = 2$ at the point 2. The three touches at 3, 7 and 8 no longer count as overlaps.

## Correctness

At each step, $count$ is the number of *active* intervals: those whose start event is processed and whose end event is not. Two facts give the result.

1. **The counter never overshoots.** At each step, all active intervals contain one common point. For closed intervals at an event at $x$, each active interval has $l_j \le x \le r_j$, so all contain $x$. For half-open and open intervals, the active ones at a start event at $x$ have $l_j \le x < r_j$, because the ends at $x$ came first; at an end event they have $l_j < x \le r_j$, so they all contain the points just left of $x$. Hence $count \le d$ at every step.
2. **The counter reaches the depth.** For closed and half-open intervals the depth is reached at some left end $x$. Right after the last start event at $x$, the active intervals are exactly the intervals that contain $x$, by the tie rule, so $count = c(x) = d$. For open intervals the same holds for the points just right of $x$.

So the largest value of the counter is $d$, and line L7 records it with a left end where it occurs. The [proof](proofs/correctness.md) gives each case in full.

## Complexity

- **Time.** Building the $2n$ events takes $\Theta(n)$ time; the sort of line L3 takes $\Theta(n \log n)$ comparisons in the worst and the average case, and it dominates. The loop does $2n$ steps of $O(1)$ work.
- **Space.** $\Theta(n)$ for the events.
- **Lower bound.** Deciding $d \ge 2$ for closed point intervals is element distinctness, which needs $\Omega(n \log n)$ operations in the algebraic decision tree model. So the sweep is optimal in that model.

## Properties

- **Exact integer arithmetic.** It only compares coordinates and adds $\pm 1$, so it is exact for any ordered type of coordinates, including floats and dates.
- **Witness for free.** The variable $at$ gives a place of maximum depth without extra cost.
- **Offline.** All intervals are needed before the sort. The dynamic version uses a [segment tree](/segment-tree/) with range add and maximum.
- **Weighted form.** Replacing $\pm 1$ by $\pm w_j$ gives the largest total weight at one point, with the same proof when all $w_j \ge 0$.

## Variants and improvements

- **Two sorted arrays.** Sort the left ends into $L$ and the right ends into $R$. Walk with two pointers: take $L[i]$ when $L[i] \le R[j]$ for closed intervals, or when $L[i] < R[j]$ for half-open intervals, else take $R[j]$. This is the same sweep without pairs, and it is the usual "minimum platforms" code.
- **Encoding the tie rule in the key.** For closed intervals, sort the key $(x, 0)$ for a start and $(x, 1)$ for an end; for half-open, the opposite. This avoids a custom comparison.
- **All maximal segments.** Record each segment between consecutive events where the counter equals the final $d$; this needs a second pass or a list that is reset when $best$ grows.
- **Integer coordinates.** A difference array of size $U$ gives $O(n + U)$ time.
- **With an assignment.** The [greedy partitioning](/interval-partitioning-greedy/) algorithm sweeps the same events with a heap of free resources, and assigns each interval to one of $d$ resources.

## When to use it

Use it when you need only the depth, or the peak of a load curve, of a static batch of intervals. It is the simplest $O(n \log n)$ method and it needs no heap. Use the greedy partitioning algorithm when you also need to assign the intervals to resources, and a segment tree when intervals change over time.

## Pitfalls

- **The wrong tie rule.** With ends first on closed intervals, $[1, 3]$ and $[3, 5]$ give $d = 1$ instead of 2. With starts first on half-open intervals, they give $d = 2$ instead of 1. Line L3 must match the type.
- **Sorting by coordinate only.** A sort that leaves ties in input order, or a comparison that uses only $x$, makes the result depend on the input order. Always break ties by the event type.
- **Reporting the place of the last maximum.** Line L7 uses $>$, so it keeps the first place where $best$ is reached. With $\ge$ it keeps the last one; both are correct, but for open intervals the place must be read as "just right of $at$".
- **Counting at end events.** Testing for a new maximum only after a $-1$ event misses every peak, because the counter is highest right after a start.

## Implementations

## History

The event sort with a counter is the simplest case of the plane sweep paradigm, which de Berg et al. present in their chapter on line segment intersection. Kleinberg and Tardos use the depth of a set of intervals as the lower bound in the interval partitioning problem and show that a greedy algorithm meets it.

## References
