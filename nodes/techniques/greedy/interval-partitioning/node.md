---
tag: TJQZTD
kind: problem
slug: interval-partitioning
name: Interval partitioning
aliases:
- Interval coloring
- Meeting rooms
- Minimum platforms
- interval coloring
- minimum number of resources for intervals
area: techniques/greedy
level: intro
summary: Partition intervals into the minimum number of resources so that no resource holds overlapping intervals.
prereqs: [activity-selection, greedy-algorithm, priority-queue]
see_also: [interval-partitioning-greedy, interval-coloring-depth-theorem, earliest-finish-time-first, k-machine-interval-scheduling, greedy-stays-ahead, chordal-graph, binary-heap]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.1, Interval Scheduling, the subsection on scheduling all intervals (the interval partitioning problem and the depth bound)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.1, An activity-selection problem (the exercise on scheduling all activities in the fewest lecture halls)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 4, Greedy Algorithms
---

Interval partitioning asks for the fewest resources that can hold $n$ given intervals, with no two overlapping intervals on the same resource. The answer equals the *depth* of the intervals, the largest number of them that contain one common point. A [greedy algorithm](/greedy-algorithm/) that takes the intervals by start time and puts each one on a free resource reaches the depth in $O(n \log n)$ time. In graph terms, the problem is the coloring of an interval graph with the fewest colors.

## In plain words

A school has many lectures, each with a start time and an end time, and every lecture must get a room. Two lectures in the same room must not overlap. How few rooms are enough?

Look at the busiest moment of the day. If four lectures run at that moment, you need at least four rooms. The surprise is that this many rooms is always enough.

To find a plan, go through the lectures in order of start time. For each lecture, look for a room that is already free. If there is one, use it. If not, open a new room. A new room is opened only when all the open rooms are busy at that moment, so the number of rooms never goes above the count at the busiest moment.

## Definition

**Input.** A finite set $S$ of $n$ intervals. Interval $a$ has a start $s(a)$ and a finish $f(a)$ with $s(a) < f(a)$, and occupies the half-open interval $[s(a), f(a))$. Two distinct intervals are compatible when $f(a) \le s(b)$ or $f(b) \le s(a)$.

**Output.** A number $k$ and a map $c : S \to \{1, \ldots, k\}$ such that each class $c^{-1}(j)$ is pairwise compatible, with $k$ as small as possible. The class $c^{-1}(j)$ is the set of intervals on resource $j$.

**Depth.** The depth of $S$ is
$$ d(S) = \max_{t} \bigl|\{\, a \in S : s(a) \le t < f(a) \,\}\bigr|, $$
the largest number of intervals that contain one point $t$. The maximum is reached at some start time, because the count changes only at start and finish times and goes up only at a start.

**Theorem.** The smallest $k$ is $d(S)$.

*Proof.* The $d(S)$ intervals that contain a point $t$ pairwise intersect, so they need $d(S)$ different resources, and $k \ge d(S)$. For the other direction, run the greedy algorithm below and let $x$ be an interval for which it opens resource number $r + 1$. The intervals are taken in order of start time, so the last interval on each of the $r$ open resources starts at or before $s(x)$. The algorithm opens a new resource only when each of them ends after $s(x)$. So these $r$ intervals and $x$ all contain the point $s(x)$, and $r + 1 \le d(S)$. Hence the greedy algorithm uses at most $d(S)$ resources. $\square$

The page [interval coloring depth theorem](/interval-coloring-depth-theorem/) treats this theorem in full.

## Variants

- **Only the number.** Compute $d(S)$ without the assignment. Sort the $2n$ end points, with a finish before a start at the same time for half-open intervals, and sweep with a counter that adds 1 at a start and subtracts 1 at a finish. The largest value of the counter is $d(S)$. This is the "minimum platforms" form.
- **Closed intervals.** With $[s(a), f(a)]$, a common end point is a conflict, and in the sweep a start comes before a finish at the same time.
- **A fixed number of resources.** With only $k$ resources, choose the most intervals that fit. This is [k-machine interval scheduling](/k-machine-interval-scheduling/). For $k = 1$ it is [activity selection](/activity-selection/).
- **Online.** The intervals arrive in an arbitrary order and each gets a resource at once. Then the greedy rule by start time is not available, and an online rule can need more than $d(S)$ resources.
- **Circular arcs.** For arcs of a circle, the depth is not always enough. The three arcs from 0 to 150 degrees, from 120 to 270 degrees and from 240 to 30 degrees pairwise overlap, so they need 3 resources, but no point lies on all three, so the depth is 2. Coloring circular-arc graphs with the fewest colors is NP-hard.

## Examples

Take nine lectures: $a = [9, 11)$, $b = [9, 13)$, $c = [9, 10)$, $d = [11, 14)$, $e = [11, 13)$, $f = [13, 15)$, $g = [14, 16)$, $h = [15, 16)$, $i = [10, 12)$.

**The depth.** The number of lectures that run at each hour:

| time $t$ | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| lectures that contain $t$ | $a, b, c$ | $a, b, i$ | $b, d, e, i$ | $b, d, e$ | $d, f$ | $f, g$ | $g, h$ |
| count | 3 | 3 | 4 | 3 | 2 | 2 | 2 |

So $d(S) = 4$, reached at $t = 11$, and at least 4 rooms are necessary.

**The greedy assignment.** Sort by start time ($a, b, c, i, d, e, f, g, h$) and keep a [min-heap](/binary-heap/) of pairs (time when the room becomes free, room).

| lecture | interval | smallest free time in the heap | action |
| --- | --- | --- | --- |
| $a$ | $[9, 11)$ | none | open room 1 |
| $b$ | $[9, 13)$ | 11 (room 1) | $11 > 9$, open room 2 |
| $c$ | $[9, 10)$ | 11 (room 1) | $11 > 9$, open room 3 |
| $i$ | $[10, 12)$ | 10 (room 3) | $10 \le 10$, use room 3 |
| $d$ | $[11, 14)$ | 11 (room 1) | $11 \le 11$, use room 1 |
| $e$ | $[11, 13)$ | 12 (room 3) | $12 > 11$, open room 4 |
| $f$ | $[13, 15)$ | 12 (room 3) | use room 3 |
| $g$ | $[14, 16)$ | 13 (room 2) | use room 2 |
| $h$ | $[15, 16)$ | 13 (room 4) | use room 4 |

The rooms are $\{a, d\}$, $\{b, g\}$, $\{c, i, f\}$ and $\{e, h\}$: 4 rooms, equal to the depth. When $e$ opens room 4, the other three rooms hold $b$, $i$ and $d$, which all contain time 11, as the proof says.

**Order matters.** If the same greedy rule takes the intervals in a different order, it can use more than $d(S)$ resources. For $[0, 2)$, $[3, 5)$, $[1, 4)$, $[4, 6)$ in this order, "first free resource" gives $[0, 2)$ and $[3, 5)$ to resource 1, $[1, 4)$ to resource 2, and $[4, 6)$ cannot go to resource 1 (busy until 5) but goes to resource 2 (free at 4). That uses 2, which is the depth. The order $[0, 2)$, $[4, 6)$, $[1, 4)$, $[3, 5)$ gives $[0, 2)$ and $[4, 6)$ to resource 1, $[1, 4)$ to resource 2, and $[3, 5)$ meets both, so it needs resource 3, while the depth is 2.

## Known algorithms

- **[Greedy by start time](/interval-partitioning-greedy/).** Sort by start time, keep a min-heap of the times when the open resources become free, and give each interval the resource that becomes free first if it is free by the start, else a new resource. $O(n \log n)$ time and $O(n)$ space. It is optimal by the theorem above.
- **Sweep for the depth.** Sort the $2n$ end points and count. $O(n \log n)$ time, $O(1)$ extra space besides the sort. It gives the number, not the assignment.
- **Coloring by a perfect elimination order.** Interval graphs are [chordal graphs](/chordal-graph/). A chordal graph is colored with the fewest colors by greedy coloring in the reverse of a perfect elimination order. For intervals, the order by decreasing start time is a perfect elimination order, because the neighbors of an interval $x$ that start earlier all contain $s(x)$ and so form a clique. Its reverse is the order by start time, so this is the same algorithm seen from graph theory.

## Bounds

- **Upper bound.** $O(n \log n)$ time in the [comparison model](/comparison-model/), by sorting and $n$ heap operations of $O(\log d(S))$ time each. If the end points are integers in a range of size $O(n)$, a counting sort gives $O(n)$ time for the depth.
- **Value of the answer.** $1 \le d(S) \le n$ for $n \ge 1$. Both ends are reached, by $n$ disjoint intervals and by $n$ intervals that share a point.

## Reductions

- **To graph coloring.** Build the interval graph with one vertex per interval and an edge between intersecting intervals. A valid assignment is a proper coloring, so the problem is the chromatic number of an interval graph. In an interval graph the largest clique is a set of intervals that share a point (the [Helly property](/helly-property-intervals/) of intervals), so the theorem says that the chromatic number equals the clique number. This makes interval graphs [perfect graphs](/perfect-graph/).
- **Relation to activity selection.** Activity selection asks for the largest set that fits on one resource. Interval partitioning asks for the fewest resources for all intervals. The first is an independent set and the second a coloring of the same graph.

## Applications

- **Room and gate assignment.** Lectures to rooms, flights to gates, trains to platforms, when the times are fixed.
- **Register allocation for straight-line code.** The live ranges of variables in a block of code without branches are intervals, and the fewest registers without spills is the depth. Linear scan register allocation is based on this view.
- **Bandwidth and channel assignment.** Calls or transmissions with fixed times on the fewest channels.

## References
