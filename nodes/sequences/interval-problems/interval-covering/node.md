---
tag: GHNZR6
kind: problem
slug: interval-covering
name: Interval covering
aliases:
- Minimum interval cover
- Video stitching
area: sequences/interval-problems
level: intro
summary: Find the fewest intervals whose union covers a target interval.
prereqs: [interval-merging, greedy-algorithm]
see_also: [interval-covering-greedy, interval-piercing, set-cover, greedy-stays-ahead, total-unimodularity, dag-shortest-paths, interval-union-length, activity-selection]
sources:
  - url: https://leetcode.com/problems/video-stitching/
    title: LeetCode 1024, Video Stitching
    locator: the problem statement (clips [start, end] that cover [0, time], where touching clips join)
  - url: https://leetcode.com/problems/minimum-number-of-taps-to-open-to-water-a-garden/
    title: LeetCode 1326, Minimum Number of Taps to Open to Water a Garden
    locator: the problem statement (the same covering problem, with one interval per integer position)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 15, Greedy Algorithms (the greedy choice property and optimal substructure)
---

Interval covering asks for the fewest intervals, chosen from a given family of $n$ intervals, whose union contains a target interval $T$. If no choice covers $T$, the answer is that no cover exists. A greedy algorithm that always extends the covered prefix as far as possible solves it in $O(n \log n)$ time. The end point types decide the answer: closed intervals that touch, such as $[0, 2]$ and $[2, 4]$, cover $[0, 4]$, half-open ones $[0, 2)$ and $[2, 4)$ cover $[0, 4)$, but open ones $(0, 2)$ and $(2, 4)$ miss the point 2.

## In plain words

You have a set of security cameras, and each one watches one stretch of a long road. You want to switch on as few cameras as possible so that every point of one given part of the road is watched.

Start at the beginning of that part. Of the cameras that watch the starting point, switch on the one that sees farthest ahead. Then stand where it stops seeing, and do the same again. If at some point no camera reaches past the place where you stand, the road cannot be covered.

Whether two cameras that meet at one spot leave a hole depends on whether each camera also sees the spot at the end of its stretch.

## Definition

**Input.** A family of $n$ intervals $I_1, \ldots, I_n$ of $\mathbb{R}$ with $I_j = \langle l_j, r_j \rangle$, and a target $T = \langle s, t \rangle$ with $s < t$, all of one type: closed, half-open $[\,\cdot, \cdot\,)$ or open.

**Output.** A set $C \subseteq \{1, \ldots, n\}$ of smallest size with

$$ T \subseteq \bigcup_{j \in C} I_j, $$

or the answer that no such set exists, which happens exactly when $T \not\subseteq \bigcup_j I_j$.

**Touching end points.** For two intervals that meet at $x$, with $s < x < t$:

| type | intervals | target | covered? |
|---|---|---|---|
| closed | $[0, 2]$, $[2, 4]$ | $[0, 4]$ | yes, 2 is in both |
| half-open | $[0, 2)$, $[2, 4)$ | $[0, 4)$ | yes, 2 is in the second |
| open | $(0, 2)$, $(2, 4)$ | $(0, 4)$ | no, 2 is in neither |

The ends of the target also count: $[1, 4]$ does not cover $[0, 4]$, and $[0, 3]$ does not cover $[0, 4]$, while $[0, 4)$ alone covers the half-open target $[0, 4)$.

**A useful form.** For closed intervals and $s < t$, $T = [s, t]$ is covered if and only if $[s, t)$ is covered, because a finite union of closed intervals is closed. So the closed and the half-open cases have the same structure: a cover must cover every prefix $[s, x)$, and two chosen intervals may hand over at one point.

## Variants

- **Integer points.** Cover the integers $s, s + 1, \ldots, t$ with integer intervals $[l_j, r_j]$. Here $[1, 2]$ and $[3, 4]$ do join, because no integer lies between 2 and 3. It is the closed problem for the intervals $[l_j, r_j + 1)$ and the target $[s, t + 1)$.
- **Weighted covering.** Each interval has a cost $w_j \ge 0$, and the goal is a cover of least total cost. The greedy choice fails, but a shortest path over the intervals sorted by right end, a [shortest path in a DAG](/dag-shortest-paths/), solves it in $O(n^2)$ time, or $O(n \log n)$ with a range minimum structure.
- **Covering a point set.** Cover a finite set of points instead of a whole interval. This is a [set cover](/set-cover/) problem whose matrix has the consecutive ones property in each column, so its linear program is integral by [total unimodularity](/total-unimodularity/), and a greedy method by the leftmost uncovered point solves it.
- **Circular arcs.** Cover a whole circle with the fewest arcs. Some arc of an optimal cover contains a fixed point $p$, so trying each arc through $p$ as the first one and running the line greedy after it gives an $O(n^2)$ algorithm after sorting.
- **Maximum coverage with $k$ intervals.** Choose $k$ intervals to cover as much length as possible. This is a different objective, solved by dynamic programming.

## Examples

**One family, three types.** Take the target with $s = 0$, $t = 10$ and the intervals with end points $(0, 4), (1, 3), (4, 7), (2, 6), (6, 10), (7, 9), (8, 12)$.

- *Closed.* $[0, 4], [4, 7], [6, 10]$ cover $[0, 10]$, with a touch at 4. Two intervals cannot cover it: an interval through 0 is $[0, 4]$, and no interval contains $[4, 10]$. So the answer is 3.
- *Half-open.* $[0, 4), [4, 7), [6, 10)$ cover $[0, 10)$, so the answer is again 3.
- *Open.* The point 4 is only in $(2, 6)$, the point 6 is only in $(4, 7)$, the point 7 is only in $(6, 10)$, and the points near 0 are only in $(0, 4)$. So $(0, 4), (2, 6), (4, 7), (6, 10)$ is the only cover with 4 intervals and there is none with fewer: the answer is 4.

**No cover.** $[0, 1], [3, 4]$ do not cover $[0, 4]$, because of the gap $(1, 3)$. $[1, 5]$ does not cover $[0, 4]$, because 0 is missing.

**Edge cases.** One interval that contains $T$ gives the answer 1. An empty family has no cover. Point intervals $[x, x]$ never help to cover a target with $s < t$, since if a cover uses $[x, x]$, the other chosen intervals cover all points of $T$ near $x$ except $x$, and their union is closed, so it contains $x$ too.

## Known algorithms

- **[Greedy farthest-reach cover](/interval-covering-greedy/).** Sort by left end. Keep the right end $reach$ of the covered prefix; among the intervals that start at or before $reach$ (before $reach$, for open intervals after the first choice), take the one that ends farthest. $O(n \log n)$ time, $O(n)$ after sorting.
- **Bucket version.** For integer end points in a range of size $U$, store for each start the farthest end, and run the greedy over the positions in $O(n + U)$ time. This is the usual solution of the "jump game" and "garden taps" exercises.
- **Dynamic programming.** For each interval, the fewest intervals that cover $[s, r_j]$ and use $I_j$ last. $O(n^2)$ time, or $O(n \log n)$ with a range minimum structure; it also handles weights.
- **Brute force.** Try all subsets in order of size, in $O(2^n n)$ time.

## Bounds

**Upper bound.** $O(n \log n)$ time in the [comparison model](/comparison-model/) by the greedy, and $O(n)$ time when the intervals come sorted by left end.

**Lower bound.** $\Omega(n)$ time, because an algorithm must read every interval in the worst case. For $n$ intervals that all lie outside $T$ there is no cover, and changing any one interval that the algorithm did not read into $T$ itself makes the answer 1.

**Size of the answer.** The answer is at most $n$. An optimal cover never needs three intervals through one point of $T$: of three intervals through a point, the one with the smallest left end and the one with the largest right end already cover the union of the three.

## Reductions

- **To merging.** A cover exists if and only if the component of $\bigcup_j I_j$ that contains $s$ also contains $T$, which [interval merging](/interval-merging/) decides. Merging does not give the minimum number, only feasibility.
- **To shortest paths.** For closed intervals, make a vertex for each interval and an edge from $I_i$ to $I_j$ when $l_j \le r_i < r_j$; the answer is the fewest vertices on a path from an interval with $l \le s$ to an interval with $r \ge t$. With weights this is the weighted variant.
- **To set cover.** It is a special case of [set cover](/set-cover/), the general NP-hard problem, made easy because the sets are intervals of a line.
- **Dual problem.** The largest set of points of $T$ no two of which lie in a common interval is a lower bound on the number of intervals in a cover, because each interval of a cover contains at most one of these points.

## Applications

- **Video stitching.** Choose the fewest clips that together show a whole time span.
- **Sensor and camera placement.** Switch on the fewest sensors whose ranges cover a road, a pipe or a fence.
- **Irrigation.** Open the fewest taps, each watering a stretch of a garden, so that the whole garden is watered.
- **Genome assembly and sequencing.** Choose the fewest reads that span a target region.
- **Time coverage.** Pick the fewest staff shifts that cover the opening hours.

## References
