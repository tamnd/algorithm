---
tag: MNJEAT
kind: problem
slug: interval-merging
name: Interval merging
aliases:
- Merge overlapping intervals
area: sequences/interval-problems
level: intro
summary: Replace a list of intervals by disjoint intervals with the same union.
prereqs: [sorting-problem, total-order]
see_also: [interval-merging-sort, interval-union-length, interval-list-intersection, maximum-overlap, sweep-line-technique, element-distinctness-lower-bound]
sources:
  - url: https://leetcode.com/problems/merge-intervals/
    title: LeetCode 56, Merge Intervals
    locator: the problem statement (closed intervals; intervals that share an end point are merged)
  - url: https://cp-algorithms.com/geometry/length-of-segments-union.html
    title: cp-algorithms, Length of the union of segments
    locator: the sweep over the sorted end points, which finds the same components of the union
  - paper: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC 1983), pages 80 to 86"
    locator: the lower bound for element distinctness, used here in the reduction
---

Interval merging takes a list of $n$ intervals on the real line and returns the shortest sorted list of pairwise disjoint intervals that has the same union. Each output interval is one connected piece of the union. The problem is solved by [sorting](/sorting-problem/) the intervals by left end and one scan, in $O(n \log n)$ time, and this is optimal in the [algebraic decision tree](/algebraic-decision-tree/) model. The exact output depends on the kind of end points: closed intervals that share an end point merge, open intervals that share an end point do not.

## In plain words

You have a list of time slots when a room is busy, for example from 9 to 11, from 10 to 12 and from 14 to 15. Some slots overlap. You want a clean list in which no two slots overlap, and in which each moment that was busy before is still busy, and no other moment is.

Here the answer is "from 9 to 12, and from 14 to 15". The first two slots become one slot, because they overlap. The rule for two slots that only touch, such as 9 to 10 and 10 to 11, depends on whether the end moments belong to the slots. If the room is busy at the moment 10 in at least one slot, then the two slots become one.

## Definition

**Input.** A finite list $I = (I_1, \ldots, I_n)$ of intervals of $\mathbb{R}$ (or of any [total order](/total-order/)), all of the same type. The main case is closed intervals $I_j = [l_j, r_j] = \{x : l_j \le x \le r_j\}$ with $l_j \le r_j$. The other types are half-open $[l_j, r_j) = \{x : l_j \le x < r_j\}$ and open $(l_j, r_j) = \{x : l_j < x < r_j\}$, each with $l_j < r_j$ so that the interval is not empty.

**Output.** The list $J = (J_1, \ldots, J_m)$ of the connected components of the union $U = I_1 \cup \cdots \cup I_n$, sorted from left to right. Each $J_i$ is an interval of the same type as the input, and

$$ J_1 \cup \cdots \cup J_m = U, \qquad \sup J_i \le \inf J_{i+1} \text{ and } J_i \cup J_{i+1} \text{ is not an interval, for } 1 \le i < m. $$

The precise "do not touch" condition for consecutive outputs $J_i = \langle a_i, b_i \rangle$ is:

| type | two consecutive outputs satisfy | so these two inputs merge |
|---|---|---|
| closed $[l, r]$ | $b_i < a_{i+1}$ | $[1, 3]$ and $[3, 5]$ give $[1, 5]$ |
| half-open $[l, r)$ | $b_i < a_{i+1}$ | $[1, 3)$ and $[3, 5)$ give $[1, 5)$ |
| open $(l, r)$ | $b_i \le a_{i+1}$ | $(1, 3)$ and $(3, 5)$ stay apart, because 3 is in neither |

For half-open intervals the union $[1, 3) \cup [3, 5)$ is the interval $[1, 5)$, so it is one component even though the two inputs are disjoint. For open intervals the point 3 is missing from the union, so $(1, 3)$ and $(3, 5)$ are two components. The output is unique, because the components of a set are unique, and $m \le n$, because each component contains at least one input interval.

## Variants

- **Integer intervals.** When the intervals are sets of integers, $[1, 3]$ and $[4, 5]$ cover $\{1, \ldots, 5\}$ and should often merge. Then two closed intervals merge when $l_{j} \le r_{i} + 1$.
- **Count only.** Return $m$, the number of components. This is the number of indices in the sorted scan where a new component starts.
- **Total length.** Return the measure of $U$, the sum of the lengths of the components. This is [interval union length](/interval-union-length/).
- **Insert one interval.** The input is a list that is already merged and sorted, plus one new interval. A scan or two binary searches find the components that the new interval meets, and the answer comes in $O(n)$ time, or $O(\log n)$ time plus the cost of the deletions with a balanced tree.
- **Online merging.** The intervals arrive one by one, and the merged list must be kept after each arrival. A balanced search tree keyed by left end does each insertion in $O(\log n)$ amortized time, since each interval is deleted at most once after it is inserted.
- **Weighted or labeled merging.** Keep, with each component, the labels or the number of input intervals in it.

## Examples

**Closed intervals.** The input $[8, 10], [1, 3], [15, 18], [2, 6], [10, 12], [17, 17], [5, 7]$ has the union $[1, 7] \cup [8, 12] \cup [15, 18]$, so $m = 3$. The intervals $[8, 10]$ and $[10, 12]$ share only the point 10 and merge into $[8, 12]$. The point interval $[17, 17]$ lies inside $[15, 18]$ and leaves no trace. The gap between 7 and 8 keeps $[1, 7]$ and $[8, 12]$ apart.

**Touching end points.** $[1, 3], [3, 5]$ gives $[1, 5]$. $[1, 3), [3, 5)$ gives $[1, 5)$. $(1, 3), (3, 5)$ gives $(1, 3), (3, 5)$. As integer intervals, $[1, 3], [4, 5]$ gives $[1, 5]$, but as real intervals it gives $[1, 3], [4, 5]$.

**Containment.** $[1, 10], [2, 3], [4, 5]$ gives $[1, 10]$. An algorithm that sets the right end of the current component to the right end of the newest interval, instead of the larger of the two, returns $[1, 5]$, which is wrong.

**Edge cases.** The empty list gives the empty list. One interval gives itself. $n$ copies of one interval give that interval once.

## Known algorithms

- **[Interval merging by sorting](/interval-merging-sort/).** Sort by left end, then scan and either extend the last output interval or start a new one. $O(n \log n)$ time in the [comparison model](/comparison-model/), $O(n)$ time for the scan when the input is already sorted, and $O(n)$ extra space for the output.
- **Sweep over the end points.** Sort the $2n$ end points and keep a counter of open intervals, as in [sweep for union length](/sweep-union-length/). A component starts when the counter goes from 0 to 1 and ends when it goes back to 0. This is the same bound, with the order of ties at equal coordinates set by the type of the intervals.
- **Integer end points.** If the end points are integers in a range of size $O(n)$, a [counting sort](/counting-sort/) or a [radix sort](/radix-sort/) replaces the comparison sort, and the total time is $O(n)$.

## Bounds

**Upper bound.** $O(n \log n)$ comparisons and time in the comparison model, by the algorithm above.

**Lower bound.** $\Omega(n \log n)$ in the algebraic decision tree model. The reduction is from [element distinctness](/element-distinctness/): given numbers $x_1, \ldots, x_n$, merge the closed point intervals $[x_j, x_j]$. The output has $m = n$ components if and only if the numbers are distinct. The reduction costs $O(n)$, and element distinctness needs $\Omega(n \log n)$ operations in this model by [Ben-Or's theorem](/element-distinctness-lower-bound/). So no algorithm in the model merges $n$ intervals faster in the worst case, even when it only reports $m$.

**Output size.** $1 \le m \le n$ for $n \ge 1$. Both ends are reached: $n$ intervals that share a point give $m = 1$, and $n$ pairwise far intervals give $m = n$.

## Reductions

- **To sorting.** After one sort by left end, the problem takes $O(n)$ more time. So merging costs at most a sort plus a linear scan.
- **From element distinctness.** As above, with point intervals, in $O(n)$ time.
- **Union length.** The length of the union is the sum of $b_i - a_i$ over the merged output, so [interval union length](/interval-union-length/) reduces to merging in $O(n)$ extra time.
- **Intersection of two unions.** To intersect the unions of two lists, merge each list, then run the [two-pointer intersection](/interval-list-intersection-two-pointers/) on the two merged lists.

## Applications

- **Calendars and free time.** Merge the busy slots of several people, then the gaps between the components are the common free times.
- **Genome annotation.** Merge the regions of reads or features on a chromosome to get the covered regions, as the merge command of interval tools does.
- **Memory and disk ranges.** Merge freed address ranges into larger free blocks, and merge byte ranges in a download that arrives in pieces.
- **Preprocessing.** Many interval algorithms need a sorted list of disjoint intervals as input, for example the [interval list intersection](/interval-list-intersection/) problem.

## References
