---
tag: BJ70R6
kind: algorithm
slug: sweep-union-length
name: Sweep for union length
aliases:
- Endpoint sweep for covered length
area: sequences/interval-problems
level: intro
summary: Sweep endpoints in order, tracking how many intervals are open.
solves: [interval-union-length]
model: comparison-model
complexity:
  vars: {n: the number of intervals}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [interval-union-length, sweep-line-technique, sorting-problem, loop-invariant]
see_also: [sweep-maximum-overlap, interval-merging-sort, klee-measure-problem, area-of-union-of-rectangles, event-point, segment-tree]
sources:
  - url: https://cp-algorithms.com/geometry/length-of-segments-union.html
    title: cp-algorithms, Length of the union of segments
    locator: the whole page (sorted end points, a counter of open segments, and the credit to Klee, 1977)
  - paper: "Victor Klee, Can the measure of the union of intervals [a_i, b_i] be computed in less than O(n log n) steps?, American Mathematical Monthly 84(4) (1977), pages 284 to 285"
    locator: the sorting algorithm and the question of its optimality
  - paper: "Michael L. Fredman and Bruce Weide, On the complexity of computing the measure of the union of intervals [a_i, b_i], Communications of the ACM 21(7) (1978), pages 540 to 544, doi:10.1145/359545.359553"
    locator: the matching Omega(n log n) lower bound in the linear decision tree model
---

The sweep for union length computes the total length of the union of $n$ intervals, the [interval union length](/interval-union-length/) problem. It turns each interval into a start event and an end event, sorts the $2n$ [events](/event-point/) by coordinate, and walks through them with a counter of the intervals that are open. Each gap between two consecutive events where the counter is positive is covered, so its length is added. It takes $\Theta(n \log n)$ time, which is optimal in the linear decision tree model, and with the test "counter at least $k$" it also gives the length covered at least $k$ times.

## In plain words

Mark every left end on a number line with a plus sign and every right end with a minus sign. Then walk from left to right and keep a counter. At a plus sign the counter goes up by one, at a minus sign it goes down by one. Between two marks the counter does not change, and it says how many intervals cover that stretch.

So as you walk, look at each stretch between two marks. If the counter is above zero there, the stretch is covered: add its length. If the counter is zero, the stretch is a gap: skip it. When you reach the last mark, the sum is the covered length.

## The problem

The input is a list of $n$ intervals with end points $l_j \le r_j$. The output is the measure $L$ of their union, as defined on the [interval union length](/interval-union-length/) page. Whether each end point is open or closed does not change $L$, so the algorithm does not need to know it. For the length covered at least $k$ times, the test of line L6 is $count \ge k$.

## The algorithm

```pseudo id=main
SWEEP-UNION-LENGTH(I[1 .. n])
L1  E ← an empty list of events
L2  for each [l, r] in I do append (l, +1) and (r, −1) to E
L3  sort E by coordinate; at equal coordinates put +1 before −1
L4  total ← 0, count ← 0, prev ← 0
L5  for each (x, d) in E, in sorted order do
L6      if count ≥ 1 then total ← total + (x − prev)
L7      count ← count + d
L8      prev ← x
L9  return total
```

Line L6 adds the gap from the previous event to this one, before line L7 applies this event, because the counter at that moment is the coverage of the open gap $(prev, x)$. The tie rule of line L3 is not needed for $L$: two events at the same coordinate have a gap of length 0 between them, so any order of them adds the same total. With starts first, the counter never goes below 0, which is convenient when the same sweep also reports the maximum coverage. The first value of $prev$ is never used, because $count = 0$ at the first event.

## Example

Take $[1, 4], [7, 9], [2, 5], [9, 12], [8, 9], [14, 14]$. Line L3 gives the twelve events below. The column "gap" is $x - prev$, added only when the counter before the event is at least 1.

| event | count before | gap added | total | count after |
|---|---|---|---|---|
| $(1, +1)$ | 0 | none | 0 | 1 |
| $(2, +1)$ | 1 | 1 | 1 | 2 |
| $(4, -1)$ | 2 | 2 | 3 | 1 |
| $(5, -1)$ | 1 | 1 | 4 | 0 |
| $(7, +1)$ | 0 | none | 4 | 1 |
| $(8, +1)$ | 1 | 1 | 5 | 2 |
| $(9, +1)$ | 2 | 1 | 6 | 3 |
| $(9, -1)$ | 3 | 0 | 6 | 2 |
| $(9, -1)$ | 2 | 0 | 6 | 1 |
| $(12, -1)$ | 1 | 3 | 9 | 0 |
| $(14, +1)$ | 0 | none | 9 | 1 |
| $(14, -1)$ | 1 | 0 | 9 | 0 |

The result is $L = 9$. The gap from 5 to 7 is skipped because the counter is 0 there. At 9 the touching intervals $[7, 9]$ and $[9, 12]$ hand over without a drop to 0, so no gap opens. The point interval $[14, 14]$ raises the counter only across a gap of length 0. With $k = 2$ the added gaps are $(2, 4)$ and $(8, 9)$, so the length covered at least twice is $2 + 1 = 3$.

## Correctness

The key fact is about two consecutive events $x_i < x_{i+1}$ in the sorted list. After line L7 has processed event $i$, all events at coordinates up to $x_i$ are processed, so

$$ count = |\{j : l_j \le x_i\}| - |\{j : r_j \le x_i\}| = |\{j : l_j \le x_i < r_j\}|, $$

and no end point lies strictly between $x_i$ and $x_{i+1}$. So $count$ is the coverage $c(x)$ at every point $x$ of the open gap $(x_i, x_{i+1})$. The invariant of the loop is: before event $i + 1$, $total$ is the measure of the covered part of $(-\infty, x_i]$. Line L6 adds the gap exactly when it is covered, and gaps of length 0 add nothing. The [proof](proofs/correctness.md) gives the details, for any tie order and any threshold $k$.

## Complexity

- **Time.** Lines L1 and L2 build $2n$ events in $\Theta(n)$ time. Line L3 sorts them in $\Theta(n \log n)$ time with any optimal comparison sort; it is the dominant step in every case, since even a sorted list of intervals does not give sorted events in general. The loop of line L5 does $2n$ steps of $O(1)$ work.
- **Space.** The event list has $2n$ entries, so $\Theta(n)$ extra space.
- **Arithmetic.** The algorithm does $O(n)$ subtractions and additions of coordinates. With integer coordinates the result is exact; with floating point coordinates each gap is rounded once, and the sum of $2n$ rounded gaps has the usual rounding error of a sum.
- **Optimality.** Fredman and Weide proved an $\Omega(n \log n)$ lower bound in the linear decision tree model, so the sweep is optimal there up to a constant factor.

## Properties

- **Independent of end point types.** The same code is right for closed, open and half-open intervals, because each end point has measure zero.
- **Threshold for free.** Changing the test to $count \ge k$ gives the length covered at least $k$ times; recording the gap under its count gives the whole coverage histogram.
- **Offline.** It needs all intervals before the sort. For insertions and deletions, a [segment tree](/segment-tree/) over the coordinates keeps the covered length in $O(\log n)$ time per change.
- **Comparison based on coordinates.** Apart from the subtractions in line L6, it only compares coordinates.

## Variants and improvements

- **Sort only the left ends.** Merge the intervals by left end with [interval merging by sorting](/interval-merging-sort/) and add the component lengths. This sorts $n$ keys instead of $2n$.
- **Two sorted arrays.** Sort the left ends and the right ends separately and merge the two arrays during the scan. This avoids the event pairs and has the same bound.
- **Counting integer points.** For closed integer intervals, run the sweep on $[l_j, r_j + 1)$ to count the covered integers.
- **Difference array.** For integer coordinates in a range of size $U$, add $+1$ at $l_j$ and $-1$ at $r_j$ in an array, take prefix sums, and count the positive cells, in $O(n + U)$ time.
- **Rectangles.** In two dimensions, sweep a vertical line over the $x$ events and keep the union length of the active $y$-intervals in a segment tree, as in the [area of a union of rectangles](/area-of-union-of-rectangles/).

## When to use it

Use it when you need the covered length, or the length covered at least $k$ times, of a static batch of intervals. If you also need the components themselves, use [interval merging by sorting](/interval-merging-sort/), which gives the length as a by-product. If you need the largest coverage instead of a length, the same events with the counter give the [sweep for maximum overlap](/sweep-maximum-overlap/), where the tie order does matter.

## Pitfalls

- **Adding after the update.** If lines L6 and L7 change places, the gap before an event is tested with the counter after that event. For $[1, 3]$ alone, the gap $(1, 3)$ is then tested with $count = 0$, and the result is 0 instead of 2. Test the old counter in line L6, then update it in line L7.
- **Summing the lengths.** Adding $r_j - l_j$ for each interval counts overlaps several times: 12 instead of 9 in the example.
- **A tie rule that matters elsewhere.** The tie order of line L3 does not change $L$, but code that reuses the counter for the maximum coverage needs the right tie rule for the type of the end points. Do not copy one sweep into the other without checking it.
- **Integer points.** Counting integers with $r_j - l_j$ instead of $r_j - l_j + 1$ undercounts each closed integer interval by one.

## Implementations

## History

Klee asked in the American Mathematical Monthly in 1977 whether the measure of a union of $n$ intervals can be computed in fewer than $O(n \log n)$ steps; the sort and sweep gives $O(n \log n)$, and cp-algorithms credits this algorithm to Klee. Fredman and Weide showed in 1978 that $\Omega(n \log n)$ is needed in the linear decision tree model.

## References
