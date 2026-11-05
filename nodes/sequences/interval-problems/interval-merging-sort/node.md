---
tag: ZVJBCZ
kind: algorithm
slug: interval-merging-sort
name: Interval merging by sorting
aliases:
- Sort and sweep merge
area: sequences/interval-problems
level: intro
summary: Sort by start point and merge each interval into the last one when they overlap.
solves: [interval-merging]
model: comparison-model
complexity:
  vars: {n: the number of input intervals}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [interval-merging, sorting-problem, loop-invariant]
see_also: [sweep-union-length, interval-list-intersection-two-pointers, interval-union-length, merge-sort, sweep-line-technique]
sources:
  - url: https://leetcode.com/problems/merge-intervals/
    title: LeetCode 56, Merge Intervals
    locator: the problem statement and its closed-interval convention
  - url: https://cp-algorithms.com/geometry/length-of-segments-union.html
    title: cp-algorithms, Length of the union of segments
    locator: the algorithm on sorted end points and its O(n log n) bound
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.1 (loop invariants) and Chapter 8 (the sorting lower bound used for the sort step)
---

Interval merging by sorting solves the [interval merging](/interval-merging/) problem: sort the intervals by left end, then scan them once, and either extend the last output interval or start a new one. It runs in $\Theta(n \log n)$ time for the sort and $\Theta(n)$ time for the scan, and it uses $\Theta(n)$ extra space for the sorted copy and the output. Its correctness rests on one fact: after the sort, a new interval can meet only the last component built so far. The comparison of line L4 decides how touching end points are handled.

## In plain words

Put all the intervals in order of their left end. Take the first one as the current piece. Then look at the next interval. If it starts before the current piece ends, or exactly where it ends, the two belong together: make the current piece reach as far right as the farther of the two ends. If it starts after the current piece ends, there is a gap. Close the current piece, write it to the answer, and let the new interval be the current piece.

Because the intervals come in order of their left end, an interval that starts after the gap cannot reach back into an older piece. So each piece, once closed, never changes again.

## The problem

The input is a list of $n$ closed intervals $[l_j, r_j]$ with $l_j \le r_j$. The output is the sorted list of the connected components of their union, as defined on the [interval merging](/interval-merging/) page. Half-open intervals $[l, r)$ use the same test, and open intervals $(l, r)$ use the test of the variant below.

## The algorithm

```pseudo id=main
MERGE-INTERVALS(I[1 .. n])                  ▷ closed intervals [l, r]
L1  sort I by left end l
L2  out ← an empty list
L3  for each [l, r] in I, in sorted order do
L4      if out is empty or l > out.last.r then  ▷ a gap: [l, r] starts a new component
L5          append [l, r] to out
L6      else out.last.r ← max(out.last.r, r)    ▷ [l, r] meets the last component
L7  return out
```

Line L1 sorts by left end only; the order of intervals with the same left end does not matter. Line L4 is the only place where the type of the end points matters. For closed and half-open intervals it is $l > out.last.r$, so $[1, 3]$ and $[3, 5]$ merge, and $[1, 3)$ and $[3, 5)$ merge too, because their union $[1, 5)$ is one interval. For open intervals it is $l \ge out.last.r$, so $(1, 3)$ and $(3, 5)$ stay apart. Line L6 takes a maximum, because the new interval can lie inside the last component.

## Example

Merge the closed intervals $[8, 10], [1, 3], [15, 18], [2, 6], [10, 12], [17, 17], [5, 7]$. After line L1 the order is $[1, 3], [2, 6], [5, 7], [8, 10], [10, 12], [15, 18], [17, 17]$.

| step | interval | test of line L4 | action | out after the step |
|---|---|---|---|---|
| 1 | $[1, 3]$ | out is empty | new | $[1, 3]$ |
| 2 | $[2, 6]$ | $2 > 3$ is false | extend to 6 | $[1, 6]$ |
| 3 | $[5, 7]$ | $5 > 6$ is false | extend to 7 | $[1, 7]$ |
| 4 | $[8, 10]$ | $8 > 7$ is true | new | $[1, 7], [8, 10]$ |
| 5 | $[10, 12]$ | $10 > 10$ is false | extend to 12 | $[1, 7], [8, 12]$ |
| 6 | $[15, 18]$ | $15 > 12$ is true | new | $[1, 7], [8, 12], [15, 18]$ |
| 7 | $[17, 17]$ | $17 > 18$ is false | $\max(18, 17) = 18$ | $[1, 7], [8, 12], [15, 18]$ |

Step 5 is the touching case: $[8, 10]$ and $[10, 12]$ share the point 10, and the strict test keeps them together. With open intervals, step 5 would test $10 \ge 10$, start a new component, and the output would have four intervals. Step 7 is the containment case, where the maximum of line L6 keeps the right end at 18.

## Correctness

Let $I_1, \ldots, I_n$ be the intervals in sorted order. The scan of line L3 keeps this [loop invariant](/loop-invariant/): after $i$ steps, $out$ is the sorted list of the components of $I_1 \cup \cdots \cup I_i$, and $out.last.r$ is the largest right end among $I_1, \ldots, I_i$. When $I_{i+1} = [l, r]$ arrives, $l$ is at least the left end of each component. If $l > out.last.r$, then $I_{i+1}$ is to the right of all earlier points with a gap, so it is a new component. Otherwise $l$ lies in the last component, and $I_{i+1}$ joins it; it cannot meet an earlier component, because all of them end before the last one starts. The [proof](proofs/correctness.md) gives each step, for each type of end point.

## Complexity

- **Time.** Line L1 is a sort of $n$ items, $\Theta(n \log n)$ in the worst and the average case with [merge sort](/merge-sort/) or heapsort. The loop of line L3 does $n$ steps of $O(1)$ work each. So the time is $\Theta(n \log n)$. If the input is already sorted, a check of the order in $O(n)$ time skips the sort, so the best case is $\Theta(n)$.
- **Comparisons.** The scan makes at most $2n$ comparisons of end points: one in line L4 and at most one in line L6 for each interval.
- **Space.** The sorted copy and the output use $\Theta(n)$ extra space. If the caller allows it, sort in place and write the output over the prefix of the input array, since the output position never passes the read position; then the extra space is the space of the sort.
- **Optimality.** The [interval merging](/interval-merging/) page shows an $\Omega(n \log n)$ lower bound in the algebraic decision tree model, by a reduction from element distinctness. So the sort step cannot be avoided in general.

## Properties

- **Deterministic and comparison based.** It only compares end points, so it works for any total order of the end points, such as dates or strings.
- **Not online.** It needs all intervals before the sort. The online form keeps the components in a balanced search tree.
- **Output in order.** The output is sorted by left end and its intervals are pairwise disjoint and do not touch, so it is ready for a [two-pointer intersection](/interval-list-intersection-two-pointers/) or a binary search.
- **Linear after sorting.** The scan is a single pass with $O(1)$ state besides the output.

## Variants and improvements

- **In-place merge.** Sort the array in place, keep a write index $w$, and overwrite $A[w]$ instead of appending. This is the usual form in C and Java.
- **Integer adjacency.** For sets of integers, change line L4 to $l > out.last.r + 1$, so that $[1, 3]$ and $[4, 5]$ give $[1, 5]$.
- **Count of components.** Count the times line L5 runs instead of storing the output; this needs $O(1)$ space besides the sort.
- **Union length.** Add $out.last.r - out.last.l$ when a component closes, and at the end. This is the same scan as [sweep for union length](/sweep-union-length/).
- **Insert into a merged list.** For one new interval and a list that is already merged, copy the components that end before it, merge the ones that meet it, and copy the rest, in $O(n)$ time without a sort.

## When to use it

Use it for a batch of intervals when you need the components of their union. It is shorter and faster than a [sweep over the end points](/sweep-union-length/), because it sorts $n$ items instead of $2n$ and needs no tie rule beyond line L4. If intervals arrive and leave over time, keep the components in a balanced search tree or use an [interval tree](/interval-tree/). If you only need the total covered length, the same scan without the output list is enough.

## Pitfalls

- **Overwriting the right end.** Writing $out.last.r \leftarrow r$ in line L6 instead of the maximum breaks on containment: $[1, 10], [2, 3], [4, 5]$ gives $[1, 5]$. Always take the maximum.
- **The wrong tie test.** Writing $l \ge out.last.r$ in line L4 for closed intervals keeps $[1, 3]$ and $[3, 5]$ apart, which is wrong for closed and for half-open intervals. Writing $l > out.last.r$ for open intervals merges $(1, 3)$ and $(3, 5)$, which is wrong because 3 is not covered.
- **Comparing with the previous input interval.** The test must use the right end of the last *component*, not of the previous interval in sorted order. For $[1, 10], [2, 3], [5, 6]$, the previous interval $[2, 3]$ ends before 5, but $[5, 6]$ is inside $[1, 10]$.
- **Sorting by right end.** Line L1 must sort by left end. Sorted by right end, the list is $[5, 6], [1, 10]$, line L6 extends $[5, 6]$ to $[5, 10]$, and the part from 1 to 5 is lost.
- **Aliasing the output.** If the output intervals are the same objects as the input intervals, line L6 changes the input. Copy each interval in line L5.

## Implementations

## History

The method is folklore: it is the scan that Klee's one-dimensional measure problem leads to, and cp-algorithms credits the sorted-end-point algorithm for the union of segments to Klee in 1977. It appears in many programming interview collections as "merge intervals".

## References
