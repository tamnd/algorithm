---
tag: ZRYF9N
kind: algorithm
slug: interval-list-intersection-two-pointers
name: Two-pointer interval list intersection
aliases:
- Two-pointer interval intersection
area: sequences/interval-problems
level: intro
summary: Advance the pointer whose interval ends first and emit each nonempty overlap.
solves: [interval-list-intersection]
model: comparison-model
complexity:
  vars: {m: the length of the first list, n: the length of the second list}
  time:
    worst: Θ(m + n)
    best: "Θ(min(m, n))"
  space: {extra: Θ(1)}
properties: {stable: false, in_place: false, adaptive: false, online: true, deterministic: true, comparison: true, recursive: false}
prereqs: [interval-list-intersection, two-pointers, loop-invariant]
see_also: [sorted-array-intersection, merge-sort, interval-merging-sort, k-way-merge, two-pointer-pair-search]
sources:
  - url: https://leetcode.com/problems/interval-list-intersections/
    title: LeetCode 986, Interval List Intersections
    locator: the problem statement with closed intervals
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.3.1, the MERGE procedure and its loop invariant (the same two-pointer scan)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.4, Sorting by Merging, Algorithm M (two-way merge)
---

The two-pointer interval list intersection scans two sorted lists of disjoint intervals at the same time and outputs each nonempty intersection of an interval of one list with an interval of the other, which solves the [interval list intersection](/interval-list-intersection/) problem. At each step it compares the current interval of each list, outputs their overlap if there is one, and moves past the interval that ends first. It runs in $\Theta(m + n)$ time with $O(1)$ extra space, and it is the interval form of the [two-pointer](/two-pointers/) merge of [merge sort](/merge-sort/). The test for a nonempty overlap is $lo \le hi$ for closed intervals and $lo < hi$ for half-open ones.

## In plain words

Put a finger on the first interval of each list. The overlap of the two is from the later start to the earlier end. If that is a real stretch, write it down.

Now one of the two intervals ends first. That interval cannot meet anything further on in the other list, because everything there starts after the other interval, and the other interval reaches at least as far. So move that finger forward by one. Keep going until one finger falls off the end of its list.

## The problem

The input is two lists $A[1 \ldots m]$ and $B[1 \ldots n]$ of intervals of one type. Each list is sorted from left to right and its intervals are pairwise disjoint. The output is the sorted list of the nonempty sets $A[i] \cap B[j]$. For closed intervals $A[i] = [a_i, a'_i]$ and $B[j] = [b_j, b'_j]$, the intersection is $[\max(a_i, b_j), \min(a'_i, b'_j)]$.

## The algorithm

```pseudo id=main
INTERSECT-LISTS(A[1 .. m], B[1 .. n])       ▷ closed intervals [l, r]
L1  i ← 1, j ← 1, out ← an empty list
L2  while i ≤ m and j ≤ n do
L3      lo ← max(A[i].l, B[j].l)
L4      hi ← min(A[i].r, B[j].r)
L5      if lo ≤ hi then append [lo, hi] to out    ▷ half-open: if lo < hi
L6      if A[i].r < B[j].r then i ← i + 1         ▷ A[i] ends first
L7      else j ← j + 1                            ▷ B[j] ends first, or both end together
L8  return out
```

Lines L3 and L4 compute the intersection of the two current intervals. Line L5 keeps it only if it is not empty; this is the only line that depends on the type of the end points. For closed intervals a common end point gives a point interval $[x, x]$, and for half-open $[l, r)$ intervals it gives nothing. Lines L6 and L7 discard the interval with the smaller right end. When both right ends are equal, line L7 discards $B[j]$; the next step finds that $A[i]$ does not meet $B[j + 1]$ and discards $A[i]$.

## Example

Intersect the closed lists $A = [1, 3], [6, 9], [12, 15], [18, 20]$ and $B = [2, 6], [9, 12], [14, 14], [16, 22]$.

| step | $A[i]$ | $B[j]$ | $[lo, hi]$ | output | advance |
|---|---|---|---|---|---|
| 1 | $[1, 3]$ | $[2, 6]$ | $[2, 3]$ | $[2, 3]$ | $i$, since $3 < 6$ |
| 2 | $[6, 9]$ | $[2, 6]$ | $[6, 6]$ | $[6, 6]$ | $j$, since $9 \ge 6$ |
| 3 | $[6, 9]$ | $[9, 12]$ | $[9, 9]$ | $[9, 9]$ | $i$ |
| 4 | $[12, 15]$ | $[9, 12]$ | $[12, 12]$ | $[12, 12]$ | $j$ |
| 5 | $[12, 15]$ | $[14, 14]$ | $[14, 14]$ | $[14, 14]$ | $j$ |
| 6 | $[12, 15]$ | $[16, 22]$ | $[16, 15]$ | none, $16 > 15$ | $i$ |
| 7 | $[18, 20]$ | $[16, 22]$ | $[18, 20]$ | $[18, 20]$ | $i$, and the loop stops |

The output is $[2, 3], [6, 6], [9, 9], [12, 12], [14, 14], [18, 20]$. Steps 2, 3 and 4 are touching cases: as half-open intervals they would give $[6, 6)$, $[9, 9)$ and $[12, 12)$, which are empty, and line L5 with $lo < hi$ drops them. The loop ran 7 times, which is $m + n - 1$.

## Correctness

The scan keeps this [loop invariant](/loop-invariant/): before each test of line L2, $out$ holds, in sorted order, every nonempty $A[p] \cap B[q]$ with $p < i$ or $q < j$, and nothing else. The key step is the discard. Say $A[i].r < B[j].r$. Every later interval $B[q]$, $q > j$, starts after $B[j].r$, because $B$ is sorted and disjoint, so it starts after $A[i].r$ and does not meet $A[i]$. So once the pair $(i, j)$ is handled, $A[i]$ has no pair left, and it can go. The symmetric argument covers line L7, including the tie. The pieces come out in left-to-right order because each new piece starts at or after the end of the previous one. The [proof](proofs/correctness.md) has the details.

## Complexity

- **Time.** Each step of the loop advances $i$ or $j$ by one, so there are at most $m + n - 1$ steps when $m, n \ge 1$, each with $O(1)$ work: at most three comparisons and one append. The loop stops when either list is used up, so in the best case it takes $\min(m, n)$ steps, for example when every interval of the shorter list ends before the first interval of the longer one ends.
- **Space.** Apart from the output, the scan uses $O(1)$ extra space: two indices and two values.
- **Output.** At most $m + n - 1$ intervals, since each step outputs at most one.
- **Lower bound.** The output can have $m + n - 1$ intervals, so $\Omega(m + n)$ time is necessary in the worst case, and the scan is optimal.

## Properties

- **Online in both lists.** It reads each list once from left to right and never goes back, so it works on two streams, or on two files that do not fit in memory.
- **Output sorted and disjoint.** The output is again a sorted list of disjoint intervals, so it can feed another intersection.
- **Comparison based.** It only compares end points and copies them.
- **Symmetric.** Swapping $A$ and $B$ gives the same output, though the tie in line L7 then discards the other interval first.

## Variants and improvements

- **Report pairs.** Output $(i, j)$ instead of the piece, for a join of two sorted interval tables.
- **Union.** In the same scan, output the merged union of the two lists: take the interval with the smaller left end, and join it with the current output interval when they meet or touch.
- **Difference $A \setminus B$.** Keep a current start $s$ in $A[i]$, cut out each $B[j]$ that meets $A[i]$, and output the remaining pieces.
- **Galloping.** When $m \ll n$, jump in $B$ with exponential search to the first interval that ends at or after $A[i].l$. This gives $O(m \log(n/m) + k)$ comparisons for $k$ output pieces.
- **$k$ lists.** Intersect the lists in pairs, or use a [$k$-way merge](/k-way-merge/) with a heap of the current intervals.

## When to use it

Use it whenever both inputs are already sorted and disjoint, which is the usual form of free slots, posting lists and merged region lists. If an input is not in that form, first run [interval merging by sorting](/interval-merging-sort/) on it. If one list is much shorter than the other, a binary search per interval of the short list is faster. If you need the overlaps of many intervals with one query, store the long list in an [interval tree](/interval-tree/) instead.

## Pitfalls

- **Advancing by the start.** Advancing the pointer with the smaller *left* end in line L6 loses pieces. For $A = [0, 10]$ and $B = [1, 2], [3, 4]$, it outputs $[1, 2]$ and then drops $A[1]$, so $[3, 4]$ is lost. Advance the one that *ends* first.
- **Advancing both on a tie.** Advancing both pointers when $A[i].r = B[j].r$ is correct only because the lists are disjoint. If an input list has overlapping intervals, it can skip a piece; merge such lists first.
- **The wrong emptiness test.** For half-open intervals, line L5 with $lo \le hi$ outputs empty pieces $[x, x)$. For closed intervals, $lo < hi$ drops the point intersections, such as $[6, 6]$ in the example.
- **Unsorted input.** The scan is wrong on unsorted lists, with no error. If the order is not guaranteed, check it in $O(m + n)$ time or sort first.

## Implementations

## History

The scan is the merge of two sorted sequences, which Knuth treats as Algorithm M in Section 5.2.4 and CLRS as the MERGE procedure of merge sort, applied to intervals. In this form it is a common programming exercise, for example LeetCode problem 986.

## References
