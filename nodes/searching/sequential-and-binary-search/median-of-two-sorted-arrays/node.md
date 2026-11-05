---
tag: FSRE1H
kind: problem
slug: median-of-two-sorted-arrays
name: Median of two sorted arrays
aliases:
- k-th element of two sorted arrays
- k-th smallest of two sorted arrays
area: searching/sequential-and-binary-search
level: advanced
summary: Find the median of the union of two sorted arrays in O(log min(m, n)) time by binary searching for a partition.
model: comparison-model
complexity:
  vars: {m: the length of the shorter array, n: the length of the longer array}
  time: {worst: Θ(log m)}
prereqs: [binary-search, median]
see_also: [median, selection-problem, order-statistic, sorted-matrix-selection, merge-path, merge-sort, lower-and-upper-bound-search, binary-search-on-answer]
sources:
  - url: https://leetcode.com/problems/median-of-two-sorted-arrays/
    title: LeetCode, Problem 4, Median of Two Sorted Arrays
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9 exercises (the median of all 2n items of two sorted arrays of n items, in O(lg n) time)
---

The median of two sorted arrays asks for the median of the multiset union of a sorted array $A$ of length $m$ and a sorted array $B$ of length $n$, without merging them. More generally it asks for the $k$-th smallest item of the union. Merging the first $k$ items takes $\Theta(m + n)$ time, but the answer is fixed by one number: how many of the $k$ smallest items come from $A$. That number $i$ is the boundary of a monotone test, so a [binary search](/binary-search/) over $i$ in the shorter array finds it with at most $\lceil \lg(m + 1) \rceil$ comparisons, for $m \le n$, and the answer is $\max(A[i-1], B[k-i-1])$. A decision-tree argument shows that $\lceil \lg m \rceil$ comparisons are needed, so $\Theta(\log \min(m, n))$ is the exact order. The same cut search splits two sorted runs for parallel merging, as in [merge path](/merge-path/).

## In plain words

Two lines of children stand in order of height, each line from short to tall. You want the child in the middle of all of them, without making one long line.

Suppose you take the first few children of the first line and the first few of the second line, so that together they are exactly half of all children. This split is right when the tallest child you took from each line is not taller than the first child you left in the other line. If you took too few from the first line, the first child you left there is too short. Then you must take more from that line. So you can find the right split by halving, on the shorter line. Then the middle child is the taller of the last two children you took.

## Definition

**Input.** Sorted arrays $A[0 \ldots m-1]$ and $B[0 \ldots n-1]$ over a [total order](/total-order/), with $m + n \ge 1$, and for the general form a rank $k$ with $1 \le k \le m + n$.

**Output.** The $k$-th smallest item of the multiset $A \cup B$, that is, the item at index $k - 1$ of the merged sorted array. The median is the case $k = \lceil (m+n)/2 \rceil$ (the lower median); for an even total, the usual median is the mean of the items of ranks $(m+n)/2$ and $(m+n)/2 + 1$, which needs two such queries or one query that returns both neighbors.

**The cut.** For $0 \le i \le m$ let $j = k - i$. The pair $(i, j)$ is a *cut* when $0 \le j \le n$ and
$$ A[i-1] \le B[j] \quad\text{and}\quad B[j-1] \le A[i], $$
with $A[-1] = B[-1] = -\infty$ and $A[m] = B[n] = +\infty$. Then the first $i$ items of $A$ and the first $j$ items of $B$ are $k$ smallest items of the union, and the answer is $\max(A[i-1], B[j-1])$.

The cost is the number of comparisons between items.

## Variants

- **$k$-th smallest.** The general rank, solved by the same cut search with the range $\max(0, k - n) \le i \le \min(k, m)$.
- **Both middle items.** For an even total, return $\max(A[i-1], B[j-1])$ and $\min(A[i], B[j])$ from the same cut.
- **Many sorted arrays.** The $k$-th smallest of $r$ sorted arrays. A binary search on the value, with a [lower bound](/lower-bound-query/) count in each array, works for numbers, at a cost of $O(r \log(\text{length}))$ per tested value.
- **[Selection in a sorted matrix](/sorted-matrix-selection/).** The $k$-th smallest of $a[i] + b[j]$, a structured union of $n$ sorted rows.
- **Unsorted input.** Without order, the problem is plain [selection](/selection-problem/), $\Theta(m + n)$ time by [quickselect](/quickselect/) or the median of medians.

## Examples

For $A = [1, 3, 8, 9, 15]$ and $B = [7, 11, 18, 19, 21, 25]$ the union has 11 items, $[1, 3, 7, 8, 9, 11, 15, 18, 19, 21, 25]$, and the median is the 6th, 11. The shorter array is $A$, with $m = 5$, and the search runs over $i \in [0, 5]$ with the test $B[k - i - 1] \le A[i]$:

| step | range of $i$ | $i$ | $j = 6 - i$ | test $B[j-1] \le A[i]$ | result |
|---|---|---|---|---|---|
| 1 | $[0, 5]$ | 2 | 4 | $19 \le 8$ is false | take more from $A$ |
| 2 | $[3, 5]$ | 4 | 2 | $11 \le 15$ is true | take at most 4 |
| 3 | $[3, 4]$ | 3 | 3 | $18 \le 9$ is false | take more from $A$ |
| end | $[4, 4]$ | 4 | 2 | | |

The cut takes $[1, 3, 8, 9]$ from $A$ and $[7, 11]$ from $B$, and the median is $\max(9, 11) = 11$. The search made 3 comparisons, $\lceil \lg 6 \rceil$, and one more for the maximum.

For $A = [1, 2]$ and $B = [3, 4]$ the two middle items are the 2nd and the 3rd, 2 and 3, and the usual median is 2.5.

## Known algorithms

- **Merge to rank $k$.** Merge the two arrays and stop after $k$ items: $\Theta(k)$ comparisons, $\Theta(m + n)$ for the median. Simple and fine for small inputs.
- **Halve $k$.** Compare $A[\lfloor k/2 \rfloor - 1]$ with $B[\lceil k/2 \rceil - 1]$ (clamped to the lengths). The smaller one and all items before it in its array are among the $k - 1$ smallest, so drop them and lower $k$. This uses $O(\log k) = O(\log(m + n))$ comparisons.
- **Binary search for the cut.** Search the smallest $i$ in $[\max(0, k-n), \min(k, m)]$ with $B[k - i - 1] \le A[i]$, on the shorter array:

```pseudo id=cut
KTH-OF-TWO(A, B, k)                       ▷ m ≤ n, 1 ≤ k ≤ m + n
L1  lo ← max(0, k − n), hi ← min(k, m)    ▷ the test is true at hi by convention
L2  while lo < hi do
L3      i ← lo + ⌊(hi − lo) / 2⌋, j ← k − i
L4      if B[j − 1] ≤ A[i] then hi ← i     ▷ i is large enough
L5      else lo ← i + 1                    ▷ i is too small
L6  i ← lo, j ← k − i
L7  return max(A[i − 1], B[j − 1])        ▷ with A[−1] = B[−1] = −∞
```

The test $B[k-i-1] \le A[i]$ is monotone in $i$: as $i$ grows, $A[i]$ grows and $B[k-i-1]$ shrinks. Inside the loop $lo \le i < hi \le m$ and $1 \le j \le n$, so both reads are real cells. At the end the test holds at $i$, which gives $B[j-1] \le A[i]$, and it fails at $i - 1$ (or $i$ is the lower end of the range), which gives $A[i-1] \le B[j]$. So $(i, j)$ is a cut. This is the FIRST-TRUE loop of [lower and upper bound search](/lower-and-upper-bound-search/), so it makes at most $\lceil \lg(m + 1) \rceil$ comparisons, and with the final maximum $O(\log m)$ time and $\Theta(1)$ space. A script checked it against sorting on 20000 random pairs of arrays with copies, for every $k$.

## Bounds

**Upper bound.** $\lceil \lg(\min(m, n) + 1) \rceil + 1$ comparisons, by the cut search.

**Lower bound.** For $m \le n$, every comparison algorithm for the lower median makes at least $\lceil \lg m \rceil$ comparisons on some input.

*Proof.* Let $k = \lceil (m + n)/2 \rceil$; since $m \le n$, we have $m \le k$ and $k - 1 \le n$. For each $i \in \{1, \ldots, m\}$, build an input of distinct numbers in which the $k$ smallest items are $A[0], \ldots, A[i-1]$ and $B[0], \ldots, B[k-i-1]$, with $A[i-1]$ the largest of them: put $B[0 \ldots k-i-1]$ at $1, \ldots, k - i$, then $A[0 \ldots i-1]$ at $k - i + 1, \ldots, k$, then all other items above $k$ in sorted order within each array. Both arrays are sorted, and the median is $A[i-1]$. So for the $m$ values of $i$ the correct output is a different input cell. A comparison algorithm for a fixed $(m, n)$ is a binary decision tree whose leaves name the output cell, so it has at least $m$ leaves and height at least $\lceil \lg m \rceil$. $\blacksquare$

So the cut search is optimal up to two comparisons, and the problem has complexity $\Theta(\log \min(m, n))$, which is much less than the $\Theta(\log(m + n))$ of the halving method when one array is short.

## Reductions

- **It is a [binary search on the answer](/binary-search-on-answer/)**, where the answer is the cut $i$ and the test is monotone.
- **[Merge path](/merge-path/) uses the same cut.** Splitting two sorted runs into $p$ pieces for $p$ processors needs the cuts of the ranks $k = (m+n)/p, 2(m+n)/p, \ldots$, each found by this search.
- **Rank in the union reduces to two [lower bound](/lower-bound-query/) queries.** The rank of a value $v$ in $A \cup B$ is the sum of its lower bounds in $A$ and $B$. This gives a value-based search for numbers.
- **[Selection](/selection-problem/) with sorted input.** It is the selection problem restricted to an input made of two sorted runs.

## Applications

- The median of two sorted data sets, such as two sorted logs of response times, without merging them.
- Splitting a merge into equal parts for parallel [merge sort](/merge-sort/), and splitting a merge between threads or disks.
- The $k$-th item of the union of two sorted index lists in a database or a search engine.
- A standard test of binary search on a derived predicate in interviews and contests.

## References
