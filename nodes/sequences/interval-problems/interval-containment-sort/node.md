---
tag: 8YB754
kind: algorithm
slug: interval-containment-sort
name: Interval containment by sorting
aliases:
- Sort by start ascending and end descending
area: sequences/interval-problems
level: intro
summary: Sort by start and end, then compare each interval with its successors.
solves: [interval-containment]
model: comparison-model
complexity:
  vars: {n: the number of intervals}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [interval-containment, sorting-problem, loop-invariant]
see_also: [interval-merging-sort, dominance-counting, fenwick-tree, pareto-dominance, longest-increasing-subsequence, sweep-maximum-overlap]
sources:
  - url: https://leetcode.com/problems/remove-covered-intervals/
    title: LeetCode 1288, Remove Covered Intervals
    locator: the problem statement (count the intervals that no other interval covers)
  - paper: "H. T. Kung, F. Luccio and F. P. Preparata, On finding the maxima of a set of vectors, Journal of the ACM 22(4) (1975), pages 469 to 476"
    locator: the sort and scan for the maxima of a set of points in the plane
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.1, Loop invariants and the correctness of insertion sort (the proof pattern used here)
---

Interval containment by sorting finds, for each of $n$ intervals, an interval of the family that contains it, or reports that it is maximal, which solves the basic tasks of [interval containment](/interval-containment/). It sorts the intervals by left end ascending and, at equal left ends, by right end descending. In that order an interval can only contain the intervals after it, so one scan with the largest right end seen so far decides every interval. It takes $\Theta(n \log n)$ time, which is optimal, and the tests use $\le$, so intervals that share an end point are found to be nested.

## In plain words

Line the intervals up by where they start. When two start at the same place, put the longer one first.

Now walk along the line and remember the interval that reaches farthest to the right so far. Every interval you meet starts no earlier than that one. So if it also ends no later, it sits inside it. If it ends later, nothing before it can hold it, and it becomes the new farthest one.

The intervals that were never inside another one are the ones to keep. Of two equal copies, the first one in the line is kept and the second sits inside it.

## The problem

The input is a list of $n$ nonempty intervals $I[1 \ldots n]$ with end points $l \le r$, all of one type. $I[k] \subseteq I[j]$ holds exactly when $I[j].l \le I[k].l$ and $I[k].r \le I[j].r$, for closed, half-open and open intervals alike, as the [problem page](/interval-containment/) shows. The output is an array $parent$: $parent[k]$ is an index $j \ne k$ with $I[k] \subseteq I[j]$, or nil when $I[k]$ is kept as maximal. The kept intervals must be exactly one copy of each maximal interval, the intervals that no other interval properly contains.

## The algorithm

```pseudo id=main
CONTAINMENT-SORT(I[1 .. n])
L1  order ← the indices 1 .. n sorted by l ascending; ties by r descending, then by index
L2  parent[1 .. n] ← nil, best ← nil
L3  for each k in order do
L4      if best ≠ nil and I[k].r ≤ I[best].r then
L5          parent[k] ← best        ▷ I[k] lies inside I[best]
L6      else best ← k               ▷ I[k] reaches farther than all before it
L7  return parent
```

Line L1 makes every interval start no earlier than the ones before it, and puts the longer of two intervals with a common left end first. So an interval can contain only intervals that come after it in $order$. Line L4 compares the current interval with $I[best]$, the earlier interval with the largest right end, which is the best candidate to contain it. The test is $\le$: a shared right end, as in $[5, 6] \subseteq [3, 6]$, and an equal copy both count as contained. The index as the last tie key makes the result deterministic: of equal copies, the one with the smallest index is kept.

## Example

Take the closed intervals $I[1 \ldots 8] = [1, 4], [2, 3], [3, 6], [1, 2], [5, 6], [3, 6], [6, 8], [7, 8]$. Line L1 gives the order $1, 4, 2, 3, 6, 5, 7, 8$.

| $k$ | $I[k]$ | $I[best]$ before | test of L4 | action |
|---|---|---|---|---|
| 1 | $[1, 4]$ | none | none | $best \leftarrow 1$ |
| 4 | $[1, 2]$ | $[1, 4]$ | $2 \le 4$ | $parent[4] \leftarrow 1$, shared left end |
| 2 | $[2, 3]$ | $[1, 4]$ | $3 \le 4$ | $parent[2] \leftarrow 1$ |
| 3 | $[3, 6]$ | $[1, 4]$ | $6 > 4$ | $best \leftarrow 3$ |
| 6 | $[3, 6]$ | $[3, 6]$ | $6 \le 6$ | $parent[6] \leftarrow 3$, an equal copy |
| 5 | $[5, 6]$ | $[3, 6]$ | $6 \le 6$ | $parent[5] \leftarrow 3$, shared right end |
| 7 | $[6, 8]$ | $[3, 6]$ | $8 > 6$ | $best \leftarrow 7$, it only touches $[3, 6]$ |
| 8 | $[7, 8]$ | $[6, 8]$ | $8 \le 8$ | $parent[8] \leftarrow 7$, shared right end |

The kept intervals are $I[1] = [1, 4]$, $I[3] = [3, 6]$ and $I[7] = [6, 8]$. As half-open intervals the result is the same, since the test does not depend on the type: $[6, 8)$ touches $[3, 6)$ at 6 and is kept, and $[5, 6) \subseteq [3, 6)$.

## Correctness

The loop keeps this [loop invariant](/loop-invariant/): before each step, $best$ is the first index in $order$, among the processed ones, whose right end is the largest so far, and $parent[best] = $ nil. The main fact is that $I[k]$ lies in an earlier interval of $order$ exactly when $I[k].r \le I[best].r$. If the test holds, $I[best]$ is earlier, so $I[best].l \le I[k].l$, and its right end is at least $I[k].r$. If it fails, every earlier interval ends before $I[k]$ ends. Then the sort order gives the rest: if $I[k]$ lies properly in some $I[j]$, then $j$ comes before $k$, because either $I[j].l < I[k].l$, or the left ends are equal and $I[j].r > I[k].r$. And of two equal copies, the one with the larger index comes later. So $parent[k] \ne$ nil exactly when $I[k]$ is properly contained in another interval or has an equal copy with a smaller index. The [proof](proofs/correctness.md) gives the details.

## Complexity

- **Time.** Line L1 sorts $n$ keys with $O(n \log n)$ comparisons. The loop of lines L3 to L6 does $n$ steps of $O(1)$ work. So the total is $\Theta(n \log n)$ in every case with a comparison sort.
- **Space.** $\Theta(n)$ for $order$ and $parent$.
- **Lower bound.** Deciding whether some interval contains another needs $\Omega(n \log n)$ operations in the algebraic decision tree model, by the reduction from element distinctness on the [problem page](/interval-containment/). The algorithm answers this question, since a nested pair exists exactly when some $parent[k] \ne$ nil, so it is optimal.

## Properties

- **Independent of the end point type.** The same code is right for closed, half-open and open intervals. With mixed types, it works on the key encoding of the problem page, because it only compares end points.
- **The container is maximal.** Each $parent[k]$ is a kept interval, so following $parent$ once always reaches a maximal interval.
- **The container ends farthest.** $parent[k]$ is the container with the largest right end among those before $k$, not the smallest container.
- **The kept intervals form a proper family.** In $order$ their left ends do not decrease and their right ends strictly increase.

## Variants and improvements

- **Adjacent pairs decide.** In the order of line L1, the family has a nested pair if and only if some two adjacent intervals are nested. If no adjacent pair is nested, each next interval has a strictly larger right end, and then also a strictly larger left end, because equal left ends with a smaller right end are nested; so the family is proper. This gives a decision without the variable $best$.
- **Count the containers.** In the same order, insert the right ends into a [Fenwick tree](/fenwick-tree/) over the ranks of the right ends, and for each interval count the earlier right ends at least its own. This counts, for each interval, the containers that come before it in the order, which are all its containers except the equal copies with a larger index, in $O(n \log n)$ time. It is [dominance counting](/dominance-counting/) on the points $(-l, r)$.
- **Smallest container in a laminar family.** If any two intervals are nested or disjoint, keep a stack in the same order: pop while the top interval is disjoint from $I[k]$, then the top is the smallest container of $I[k]$, and push $I[k]$. This builds the nesting tree in $O(n)$ time after the sort.
- **Longest nested chain.** After the sort with duplicates removed, a longest non-increasing subsequence of the right ends is a longest chain $J_1 \supsetneq J_2 \supsetneq \cdots$, found by the [patience method](/longest-increasing-subsequence/) in $O(n \log n)$ time.
- **Maxima of points.** The same sort and scan finds the maximal points of a set in the plane, as in the algorithm of Kung, Luccio and Preparata, with the point $(-l, r)$ for $[l, r]$.

## When to use it

Use it to remove covered intervals, to test whether a family is proper, or to attach each interval to a container, on a static batch. If you need all contained pairs, combine the same order with a range search structure, since the output can be quadratic. If you need the smallest container in a general family, the simple scan is not enough; use the laminar stack when the family is laminar, or a search tree over right ends otherwise.

## Pitfalls

- **Ties by right end ascending.** If line L1 puts $[1, 2]$ before $[1, 4]$, the scan sees $[1, 2]$ first, makes it $best$, and then sets $best \leftarrow [1, 4]$, so $[1, 2]$ is wrongly kept. The longer interval must come first at equal left ends.
- **A strict test in line L4.** With $I[k].r < I[best].r$, the scan misses every shared right end, such as $[5, 6]$ in $[3, 6]$ and $[7, 8]$ in $[6, 8]$, and it keeps both copies of $[3, 6]$.
- **Updating $best$ every step.** If line L6 runs for every $k$, the scan compares only with the previous interval. For $[1, 10], [2, 3], [4, 5]$ it compares $[4, 5]$ with $[2, 3]$ and keeps it, though $[1, 10]$ contains it.
- **Containment is not overlap.** Testing $I[k].l \le I[best].r$, the merging test, finds overlapping pairs, not nested ones. $[6, 8]$ touches $[3, 6]$ but is not inside it.

## Implementations

## History

The scan is the planar maxima algorithm applied to the points $(-l, r)$: Kung, Luccio and Preparata sort the points by one coordinate and keep the running maximum of the other. In the interval form it is a common programming exercise, for example LeetCode problem 1288.

## References
