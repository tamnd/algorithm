---
tag: JHJ3PF
kind: problem
slug: interval-list-intersection
name: Interval list intersection
aliases:
- Intersection of two sorted interval lists
area: sequences/interval-problems
level: intro
summary: Intersect two sorted lists of disjoint intervals.
prereqs: [interval-merging, two-pointers]
see_also: [interval-list-intersection-two-pointers, interval-merging, sorted-array-intersection, k-way-merge, interval-overlap-query, allens-interval-algebra]
sources:
  - url: https://leetcode.com/problems/interval-list-intersections/
    title: LeetCode 986, Interval List Intersections
    locator: the problem statement (closed intervals; a common end point gives a point interval)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.4, Sorting by Merging (the two-way merge that the scan follows)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.3.1 (the MERGE procedure, a scan of two sorted lists in linear time)
---

Interval list intersection takes two lists of intervals, each sorted and made of pairwise disjoint intervals, and returns the sorted list of the nonempty intersections of an interval of the first list with an interval of the second. The result is the intersection of the two unions, cut into its components. A scan with [two pointers](/two-pointers/), like the merge step of [merge sort](/merge-sort/), solves it in $O(m + n)$ time for lists of lengths $m$ and $n$. For closed intervals a shared end point is a nonempty intersection, a point interval; for half-open intervals it is empty.

## In plain words

Two people each have a list of free time slots for one day. In each list the slots are in order and do not overlap. You want the slots when both are free.

Look at the first slot of each person. The time they share is from the later of the two starts to the earlier of the two ends, if that is not empty. Then drop the slot that ends first, because it cannot meet anything later in the other list. Repeat with the next slot. When one list is empty, you are done.

If one person is free until 10:00 and the other is free from 10:00, the answer depends on whether 10:00 itself belongs to the slots. If it does, they share the single moment 10:00.

## Definition

**Input.** Two lists $A = (A_1, \ldots, A_m)$ and $B = (B_1, \ldots, B_n)$ of intervals of $\mathbb{R}$, all of one type, with $A_i = \langle a_i, a'_i \rangle$ and $B_j = \langle b_j, b'_j \rangle$. Each list is sorted and pairwise disjoint: for closed intervals $a'_i < a_{i+1}$, and for half-open intervals $[a_i, a'_i)$ the weaker $a'_i \le a_{i+1}$.

**Output.** The list of all nonempty sets $A_i \cap B_j$, sorted from left to right. For closed intervals,

$$ [a, a'] \cap [b, b'] = [\max(a, b), \min(a', b')], \quad \text{nonempty if and only if } \max(a, b) \le \min(a', b'), $$

and for half-open intervals $[a, a') \cap [b, b') = [\max(a, b), \min(a', b'))$, nonempty if and only if $\max(a, b) < \min(a', b')$. Open intervals behave like half-open ones.

**Why this is the intersection of the unions.** $\bigl(\bigcup_i A_i\bigr) \cap \bigl(\bigcup_j B_j\bigr) = \bigcup_{i, j} (A_i \cap B_j)$ by distributivity. The pieces $A_i \cap B_j$ are pairwise disjoint, because two different pieces differ in $i$ or in $j$, and the $A_i$ are disjoint, as are the $B_j$. So the output is a sorted list of disjoint intervals with the intersection of the unions as its union.

**Size.** For $m, n \ge 1$ the output has at most $m + n - 1$ intervals. Order the pieces from left to right; between two consecutive pieces $A_i \cap B_j$ and $A_{i'} \cap B_{j'}$ we have $i \le i'$, $j \le j'$ and $(i, j) \ne (i', j')$, so $i + j$ grows by at least 1 from piece to piece, from at least 2 to at most $m + n$.

## Variants

- **Union and difference.** The same scan computes the union (then a merge step joins touching pieces) and the difference $A \setminus B$ of two sorted disjoint lists.
- **Unsorted or overlapping lists.** First [merge](/interval-merging/) each list into sorted disjoint form, in $O(m \log m + n \log n)$ time.
- **Many lists.** The intersection of $k$ lists, by intersecting them one by one, or the points covered by at least $t$ of the $k$ lists, by a sweep over all end points.
- **Pairs that overlap.** Report the index pairs $(i, j)$ with $A_i \cap B_j \neq \emptyset$, not the pieces. This is the same scan.
- **Very different lengths.** For $m \ll n$, binary search in $B$ for the first interval that can meet each $A_i$.

## Examples

**Closed intervals, with touching.** For $A = [1, 3], [6, 9], [12, 15], [18, 20]$ and $B = [2, 6], [9, 12], [14, 14], [16, 22]$, the output is

$$ [2, 3], \; [6, 6], \; [9, 9], \; [12, 12], \; [14, 14], \; [18, 20]. $$

Four of the six pieces are single points: $[6, 9]$ touches $[2, 6]$ at 6 and $[9, 12]$ at 9, and $[12, 15]$ touches $[9, 12]$ at 12 and contains the point interval $[14, 14]$. The output has $6 \le m + n - 1 = 7$ intervals.

**Half-open intervals.** For $A = [1, 3), [6, 9), [12, 15), [18, 20)$ and $B = [2, 6), [9, 12), [16, 22)$, the touches at 6, 9 and 12 are empty, and the output is $[2, 3), [18, 20)$.

**Edge cases.** If either list is empty, the output is empty. Lists that are equal give the same list. $A = [0, 10]$ and $B = [1, 2], [3, 4], [5, 6]$ give $B$.

## Known algorithms

- **[Two-pointer interval list intersection](/interval-list-intersection-two-pointers/).** Compare the current interval of each list, output their intersection if it is not empty, and advance the one that ends first. $\Theta(m + n)$ time and $O(1)$ extra space besides the output.
- **Binary search per interval.** For each $A_i$, find the first $B_j$ that ends at or after $a_i$ by [binary search](/binary-search/), then scan while $B_j$ starts at or before $a'_i$. $O(m \log n + k)$ time for $k$ output pieces, which is better when $m \log n < n$.
- **Sweep over all end points.** Sort the $2(m + n)$ end points and keep the number of open intervals of each list; output where both are open. $O((m + n) \log(m + n))$ time, but it also works when the lists are not sorted.

## Bounds

**Upper bound.** $O(m + n)$ time in the [comparison model](/comparison-model/) by the two-pointer scan.

**Lower bound.** $\Omega(m + n)$ in the worst case, because the output can have $m + n - 1$ intervals: for example $A = [0, 4], [6, 10], [12, 16]$ and $B = [2, 8], [9, 14]$ give the $4 = m + n - 1$ pieces $[2, 4], [6, 8], [9, 10], [12, 14]$, and the same pattern extends to any lengths with $|m - n| \le 1$. Even when the output is empty, an algorithm must look at each end point in some inputs, because changing one unread end point can create a piece.

## Reductions

- **To merging two sorted lists.** The scan visits the intervals in the order of a merge of the two lists by right end, as in the MERGE step of merge sort.
- **From set intersection of sorted arrays.** Point intervals $[x, x]$ turn [sorted array intersection](/sorted-array-intersection/) into this problem in $O(m + n)$ time.
- **Intersection of unions.** For two arbitrary lists, merge each list, then intersect.

## Applications

- **Scheduling.** The common free time of two people, or of two machines, from their sorted free lists.
- **Databases and search engines.** The intersection of two posting lists of ranges, or of two sorted range indexes.
- **Genomics.** The regions that are both in a set of genes and in a set of reads, for sorted disjoint regions.
- **Time series.** The periods when two conditions hold at the same time, each given as a sorted list of periods.

## References
