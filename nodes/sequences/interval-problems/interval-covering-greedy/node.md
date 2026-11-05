---
tag: EYK6H0
kind: algorithm
slug: interval-covering-greedy
name: Interval covering greedy
aliases:
- Greedy farthest-reach cover
area: sequences/interval-problems
level: intro
summary: Repeatedly pick the interval that extends the covered prefix farthest.
solves: [interval-covering]
model: comparison-model
complexity:
  vars: {n: the number of intervals}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [interval-covering, greedy-algorithm, greedy-stays-ahead, loop-invariant]
see_also: [interval-piercing-greedy, earliest-finish-time-first, interval-merging-sort, exchange-argument, set-cover, greedy-set-cover]
sources:
  - url: https://leetcode.com/problems/video-stitching/
    title: LeetCode 1024, Video Stitching
    locator: the problem statement (closed clips, touching clips join)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.1, Interval Scheduling, the greedy algorithm stays ahead (the proof pattern used here)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 15, Greedy Algorithms
---

The interval covering greedy finds the fewest intervals of a family whose union contains a target interval $T = \langle s, t \rangle$, or reports that no cover exists, which solves [interval covering](/interval-covering/). It sorts the intervals by left end and keeps $reach$, the right end of the prefix of $T$ that is covered so far. At each step it takes, among the intervals that start inside the covered prefix or at its end, the one that ends farthest. It runs in $\Theta(n \log n)$ time, and the proof is a [greedy stays ahead](/greedy-stays-ahead/) argument; the test "starts at or before $reach$" becomes "starts before $reach$" for open intervals.

## In plain words

Stand at the start of the stretch you must cover. Look at all the pieces that begin at or before the place where you stand. Of those, take the one that reaches farthest to the right, and walk to its end. Repeat from there.

Any other first choice ends sooner, so it can only leave you further back. That is why the farthest piece is never a mistake.

If none of the pieces that begin at or before your place reaches past it, there is a hole right after your place, and no cover exists. With pieces that do not include their end points, a piece that begins exactly where you stand does not help, because your own place is still uncovered.

## The problem

The input is a list $I[1 \ldots n]$ of intervals with end points $l \le r$ and a target with $s < t$, all of one type. The output is a list of fewest indices whose intervals cover the target, or "no cover". For closed intervals the covered part is always a prefix $[s, reach]$ and for half-open intervals a prefix $[s, reach)$; both hand over at a single point. For open intervals it is $(s, reach)$, and the point $reach$ itself is not covered.

## The algorithm

```pseudo id=main
GREEDY-COVER(I[1 .. n], s, t)    ▷ closed: cover [s, t]; half-open: cover [s, t)
L1  order ← the indices 1 .. n sorted by l ascending
L2  reach ← s, chosen ← an empty list, i ← 1
L3  while reach < t do
L4      best ← nil, far ← reach
L5      while i ≤ n and I[order[i]].l ≤ reach do     ▷ open, after the first choice: l < reach
L6          if I[order[i]].r > far then best ← order[i], far ← I[order[i]].r
            i ← i + 1
L7      if best = nil then return "no cover"
L8      append best to chosen, reach ← far
L9  return chosen
```

Line L5 reads all intervals that can join the covered prefix without a hole. For closed intervals an interval $[l, r]$ with $l = reach$ shares the point $reach$ with the prefix, and for half-open intervals $[l, r)$ with $l = reach$ starts exactly where the prefix $[s, reach)$ stops; both are allowed. For open intervals, once something is chosen, the point $reach$ is uncovered, so an interval $(reach, r)$ leaves it open and must wait. Line L6 keeps the one that ends farthest. Line L7 fails when no candidate gets past $reach$: then the points just right of $reach$ are in no interval that could still be chosen. The pointer $i$ only moves forward, because an interval that was read and not chosen ends at or before the new $reach$ and can never help again.

## Example

Cover $[0, 10]$ with the closed intervals $I[1 \ldots 7] = [0, 4], [1, 3], [4, 7], [2, 6], [6, 10], [7, 9], [8, 12]$. Line L1 gives the order $[0, 4], [1, 3], [2, 6], [4, 7], [6, 10], [7, 9], [8, 12]$.

| step | $reach$ before | read in L5 | chosen | $reach$ after |
|---|---|---|---|---|
| 1 | 0 | $[0, 4]$ | $[0, 4]$ | 4 |
| 2 | 4 | $[1, 3]$, $[2, 6]$, $[4, 7]$ | $[4, 7]$, a touch at 4 | 7 |
| 3 | 7 | $[6, 10]$, $[7, 9]$ | $[6, 10]$ | 10 |

The loop stops with $reach = 10$ and three intervals; $[8, 12]$ is never read. The half-open version $[0, 4), [4, 7), \ldots$ covering $[0, 10)$ makes the same choices.

With open intervals covering $(0, 10)$, step 2 reads only $(1, 3)$ and $(2, 6)$, because $(4, 7)$ does not start before 4, and chooses $(2, 6)$. Step 3 reads $(4, 7)$ and reaches 7, and step 4 reads $(6, 10)$ but not $(7, 9)$ and reaches 10. The cover is $(0, 4), (2, 6), (4, 7), (6, 10)$, four intervals, because the points 4, 6 and 7 each need an interval that contains them inside.

## Correctness

Let $reach_j$ be the value of $reach$ after $j$ choices, with $reach_0 = s$, and let $\rho(S)$ be the right end of the longest prefix of $T$ that a set $S$ of intervals covers. The greedy keeps this invariant: after $j$ choices, the chosen intervals cover the prefix up to $reach_j$, and $reach_j \ge \rho(S)$ for every set $S$ of $j$ intervals of the family. The step is the stays-ahead argument. Take $S$ with $\rho(S) = x > reach_{j-1}$, and an interval $J \in S$ that covers the points just left of $x$. The other $j - 1$ intervals of $S$ cover the prefix up to $l_J$, so $l_J \le reach_{j-1}$ by the invariant, and $J$ passes the test of line L5 at step $j$. So $far \ge r_J \ge x$. A cover of size $k$ has $\rho \ge t$, so the greedy stops after at most $k$ choices, and a candidate always exists while a cover exists. The [proof](proofs/correctness.md) has the details, including the open case.

## Complexity

- **Time.** Line L1 sorts in $\Theta(n \log n)$ time. In the loops, $i$ goes from 1 to at most $n + 1$ in total and each step of the outer loop chooses a new interval, so lines L3 to L8 take $O(n)$ time. With input already sorted by left end, the whole algorithm runs in $O(n)$ time.
- **Space.** $\Theta(n)$ for $order$ and $chosen$.
- **Optimality of the bound.** The sort dominates. For integer end points in a range of size $U$, a bucket per left end replaces it and gives $O(n + U)$ time.

## Properties

- **Each chosen interval passes the previous end.** $reach$ strictly increases at each choice, so no interval is chosen twice and the chosen intervals are sorted by both end points.
- **At most two chosen intervals through a point.** An interval read at step $j + 1$ ends at or before $reach_{j+1}$, so it cannot be chosen later. So the interval chosen at step $j + 2$ was not read at step $j + 1$, and it starts after $reach_j$, or at it for open intervals; it is disjoint from the interval chosen at step $j$. The cover is thin: no point lies in three chosen intervals.
- **A clear failure point.** When it reports "no cover", the prefix up to the final $reach$ is covered, every interval that starts at or before $reach$ ends at or before it, and so the points just right of $reach$ lie in no interval.
- **Comparison based.** It only compares end points.

## Variants and improvements

- **Integer points.** To cover the integers $s, \ldots, t$ with integer intervals $[l, r]$, change the test of line L5 to $l \le reach + 1$ and start with $reach = s - 1$; then $[1, 2]$ and $[3, 4]$ join.
- **Jump game form.** When each position $p$ of a range has one interval $[p, p + a_p]$, the scan of line L5 is a walk over the positions, and the algorithm is the linear "minimum jumps" method.
- **Leftmost uncovered point.** To cover a finite set of points, sort the points, and repeatedly choose, among the intervals that contain the leftmost uncovered point, the one that ends farthest. The same stays-ahead proof applies.
- **Weighted intervals.** With costs, the greedy can be wrong: for $[0, 10]$ with cost 5 against $[0, 6]$ and $[5, 10]$ with cost 1 each, it chooses the cost-5 interval. Use the dynamic program of the [problem page](/interval-covering/).
- **Circle.** For arcs of a circle, run the greedy once for each arc through a fixed point as the first choice.

## When to use it

Use it whenever every interval has the same cost and the target is one interval or a sorted set of points. If you only need to know whether a cover exists, [interval merging](/interval-merging-sort/) also answers that. If intervals have costs, use the dynamic program. For the opposite question, the fewest points that hit every interval, use the [interval piercing greedy](/interval-piercing-greedy/), which sorts by right end instead.

## Pitfalls

- **Choosing the longest interval.** Taking the interval with the largest $r - l$ among the candidates is not the same as the largest $r$ unless all candidates start together. Line L6 compares right ends only.
- **Strict test for closed intervals.** With $l < reach$ in line L5, closed intervals that touch are never joined: for $[0, 2], [2, 4]$ and target $[0, 4]$ it reports "no cover".
- **Non-strict test for open intervals.** With $l \le reach$ after the first choice, $(0, 2)$ and $(2, 4)$ are reported as a cover of $(0, 4)$, though 2 is missing.
- **Restarting the scan.** Resetting $i$ to 1 at each step is still correct but makes the loop $O(n^2)$; the pointer of line L5 never needs to go back.
- **Not checking the start.** If no interval starts at or before $s$, line L7 must fail at the first step. Code that starts with the first interval in sorted order, without the test, accepts $[1, 5]$ as a cover of $[0, 4]$.

## Implementations

## History

The farthest-reach rule is a standard greedy algorithm, and its proof follows the "greedy stays ahead" pattern that Kleinberg and Tardos use for interval scheduling. In this form it appears as the video stitching exercise, LeetCode problem 1024.

## References
