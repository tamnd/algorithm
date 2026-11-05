---
tag: V30M7R
kind: algorithm
slug: interval-piercing-greedy
name: Interval piercing greedy
aliases:
- Greedy stabbing by earliest end point
area: sequences/interval-problems
level: intro
summary: Place a point at the earliest end point of the remaining intervals.
solves: [interval-piercing]
model: comparison-model
complexity:
  vars: {n: the number of intervals}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [interval-piercing, greedy-algorithm, loop-invariant]
see_also: [earliest-finish-time-first, activity-selection, interval-covering-greedy, greedy-stays-ahead, exchange-argument, hitting-set]
sources:
  - url: https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/
    title: LeetCode 452, Minimum Number of Arrows to Burst Balloons
    locator: the problem statement (closed intervals)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.1, Interval Scheduling (the earliest finish time rule, which chooses the same intervals)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.1, An activity-selection problem (the same greedy order by finish time)
---

The interval piercing greedy finds a smallest set of points such that every interval of a family contains one of them, which solves [interval piercing](/interval-piercing/). It sorts the intervals by right end and scans them; when an interval does not contain the last point placed, it places a new point at that interval's right end. It runs in $\Theta(n \log n)$ time, and the intervals that receive new points are pairwise disjoint, which proves that no smaller set exists. For closed intervals a touch at the point counts as a hit; for half-open and open intervals the point is placed just left of the right end, and a touch does not count.

## In plain words

Look at the interval that ends first. Some point must go inside it. Put the point at its very end: any other place inside it hits only intervals that this place also hits, because every other interval ends later.

Now skip every interval that this point hits, and repeat with the interval that ends first among the rest.

Each new point is needed. The interval that asked for it starts after the last point, so it shares nothing with the intervals that asked for earlier points. Those intervals are apart from each other, and no single point can hit two of them.

## The problem

The input is a list $I[1 \ldots n]$ of nonempty intervals of one type. The output is a list of fewest points that pierce every interval. For closed intervals $[l, r]$ a point $p$ pierces when $l \le p \le r$. For half-open $[l, r)$ it needs $l \le p < r$, and for open $(l, r)$ it needs $l < p < r$, so in those cases the right end itself is not available.

## The algorithm

```pseudo id=main
PIERCE(I[1 .. n])                     ▷ closed intervals [l, r]
L1  order ← the indices 1 .. n sorted by r ascending
L2  points ← an empty list, p ← nil
L3  for each k in order do
L4      if p = nil or I[k].l > p then          ▷ half-open and open: I[k].l ≥ p
L5          p ← I[k].r
L6          append p to points
L7  return points
```

Line L4 decides whether the last point hits $I[k]$. Since the intervals come by right end, $I[k].r \ge p$, so $I[k]$ contains $p$ exactly when $I[k].l \le p$. The test uses $>$, so an interval that starts exactly at $p$, such as $[3, 6]$ after the point 3, counts as hit.

For half-open and open intervals, read $p$ in line L5 as "just left of $I[k].r$". A later interval with $l < p \le r$ contains all points just left of $p$, so it is hit; one with $l \ge p$ is not, and line L4 tests $I[k].l \ge p$. To output a real point, keep the largest left end $m$ of the intervals hit by the current $p$: the point $m$ lies in all of them for half-open intervals, and the point $(m + p)/2$ for open intervals.

## Example

Take the closed intervals $[1, 4], [2, 3], [3, 6], [5, 7], [6, 8], [8, 9], [9, 10]$. Line L1 gives the order $[2, 3], [1, 4], [3, 6], [5, 7], [6, 8], [8, 9], [9, 10]$.

| $I[k]$ | $p$ before | test of L4 | action | points |
|---|---|---|---|---|
| $[2, 3]$ | nil | new point | $p \leftarrow 3$ | 3 |
| $[1, 4]$ | 3 | $1 \le 3$, hit | none | 3 |
| $[3, 6]$ | 3 | $3 \le 3$, hit at its left end | none | 3 |
| $[5, 7]$ | 3 | $5 > 3$ | $p \leftarrow 7$ | 3, 7 |
| $[6, 8]$ | 7 | $6 \le 7$, hit | none | 3, 7 |
| $[8, 9]$ | 7 | $8 > 7$ | $p \leftarrow 9$ | 3, 7, 9 |
| $[9, 10]$ | 9 | $9 \le 9$, hit at its left end | none | 3, 7, 9 |

The result is 3 points, and the intervals that opened them, $[2, 3], [5, 7], [8, 9]$, are pairwise disjoint, so 3 is the minimum.

With the same numbers as half-open intervals, the touches at 3 and 9 no longer hit, and neither does the touch of $[6, 8)$ at 6. The groups are $\{[2, 3), [1, 4)\}$, $\{[3, 6), [5, 7)\}$, $\{[6, 8)\}$, $\{[8, 9)\}$ and $\{[9, 10)\}$, with the real points $2, 5, 6, 8, 9$, the largest left end of each group. The openers $[2, 3), [3, 6), [6, 8), [8, 9), [9, 10)$ are pairwise disjoint, so 5 points are needed. As open intervals, the groups are the same and the points are $2.5, 5.5, 7, 8.5, 9.5$.

## Correctness

Call the intervals that make line L5 run the *openers* $J_1, \ldots, J_m$, in order. The scan keeps this [loop invariant](/loop-invariant/): every interval read so far contains one of the points placed, and the openers so far are pairwise disjoint. An interval $I[k]$ that the test sends to line L5 starts after $p$, the right end of the last opener, so it is disjoint from all openers, which end at or before $p$. An interval that passes the test has $l \le p \le r$, since $r \ge p$ by the sort. At the end the $m$ points pierce all intervals, and the $m$ openers are disjoint, so every piercing set has at least $m$ points: each point lies in at most one opener. The [proof](proofs/correctness.md) covers the half-open and open cases and the choice of real points.

## Complexity

- **Time.** The sort of line L1 takes $\Theta(n \log n)$ time; the loop does $n$ steps of $O(1)$ work, also when it keeps the largest left end for half-open and open intervals. With input sorted by right end, it runs in $\Theta(n)$ time.
- **Space.** $\Theta(n)$ for $order$, and the output.
- **Lower bound.** Computing the minimum number of points needs $\Omega(n \log n)$ operations in the algebraic decision tree model, by the reduction from element distinctness on the [problem page](/interval-piercing/), so the greedy is optimal.

## Properties

- **It also solves activity selection.** The openers are a largest set of pairwise disjoint intervals, the same set that [earliest finish time first](/earliest-finish-time-first/) chooses, so one scan gives the packing and the piercing and proves that their sizes are equal.
- **Points are right ends.** For closed intervals every point is a right end of some interval, so the candidates can be restricted to right ends.
- **Online in the sorted order.** Once sorted, it decides each interval at once and never revisits a point.
- **Comparison based.** It only compares end points; the open case adds one midpoint per group for the output.

## Variants and improvements

- **Candidate points.** If the points must come from a sorted set $Q$, place the new point at the largest element of $Q$ that is at most $I[k].r$, and fail if it is less than $I[k].l$. Any point of $Q$ inside $I[k]$ is at most this element, and moving it right to this element keeps every later interval that it hits, because those end at or after $I[k].r$.
- **Counting only.** If only the number is needed, skip the output list and count the executions of line L5.
- **Integer points for half-open intervals.** With integer end points, $[l, r)$ is the integer interval $[l, r - 1]$, and the greedy point is $r - 1$.
- **Arcs of a circle.** Try each right end as the first point, and run the line greedy on the arcs that it misses, in $O(n)$ time per try after one sort.
- **Sort by left end, backward.** Scanning by left end descending and placing points at left ends is the mirror image and gives the same number.

## When to use it

Use it whenever the points are free to be placed anywhere, or among a sorted candidate set, and all points cost the same. For points with costs, use a dynamic program. For the reverse task, the fewest intervals that cover a target, use the [interval covering greedy](/interval-covering-greedy/), which sorts by left end and looks for the farthest right end. For many queries about which intervals contain a given point, use an [interval tree](/interval-tree/) instead.

## Pitfalls

- **Sorting by left end.** Sorting by left end and placing points at right ends fails: for $[1, 10], [2, 3], [4, 5]$ it places 10 for $[1, 10]$, then treats $[2, 3]$ and $[4, 5]$ as hit because they start before 10, and returns the single point 10, which misses both. The right answer is two points, 3 and 5. Line L1 sorts by right end.
- **Strict test for closed intervals.** With $I[k].l \ge p$ in line L4, $[1, 3]$ and $[3, 5]$ get two points instead of one.
- **Placing the point at $r$ for half-open intervals.** The point $r$ is not in $[l, r)$, so code that outputs right ends for half-open intervals returns points that miss the interval that opened each group.
- **Updating $p$ to the smaller right end.** Some code sets $p \leftarrow \min(p, I[k].r)$ when $I[k]$ is hit; with the sort of line L1 this is never needed, because $I[k].r \ge p$.

## Implementations

## History

The rule of choosing the interval that ends first is the earliest finish time rule that Kleinberg and Tardos and CLRS prove optimal for interval scheduling; the openers of the piercing greedy are exactly the intervals it schedules. The piercing form is a common exercise, for example LeetCode problem 452.

## References
