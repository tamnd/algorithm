---
tag: GBRJQD
kind: algorithm
slug: inversion-count-by-merge-sort
name: Counting inversions by merge sort
aliases:
- merge-sort inversion count
area: sequences/inversions-and-permutations
level: core
summary: Count cross-inversions while merging two sorted halves; runs in O(n log n).
solves: [counting-inversions]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
prereqs: [merge-sort, inversion, loop-invariant]
see_also: [counting-inversions, inversion-count-with-fenwick-tree, kendall-tau-distance, ranking-comparison-kendall-tau, lehmer-code, natural-merge-sort]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 5.3 (counting inversions, the procedures Merge-and-Count and Sort-and-Count, and their O(n log n) bound)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 2, Problem 2-4, part d (count inversions by modifying merge sort)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 2 (divide-and-conquer algorithms and mergesort)
---

Counting inversions by merge sort computes the number of [inversions](/inversion/) of an array in $\Theta(n \log n)$ time by running [merge sort](/merge-sort/) and counting, at each merge, the pairs that cross the middle. When the merge takes an item from the right half, each item still waiting in the left half is larger and comes earlier, so the count grows by the number of waiting left items. The method solves the [counting inversions](/counting-inversions/) problem with the optimal number of comparisons up to a lower-order term, and it sorts the array as a side effect. Kleinberg and Tardos call it Sort-and-Count.

## In plain words

Cut the list into a left half and a right half. Every out-of-order pair is of one of three types: both numbers in the left half, both in the right half, or one in each. Count the first two types by doing the same thing to each half. That also sorts each half.

For the third type, merge the two sorted halves, always taking the smaller front number. When you take a number from the right half, every number still waiting in the left half is bigger than it, and all of them came before it in the list. So all of them form an out-of-order pair with it, and you add how many are waiting. One merge counts all the crossing pairs at once, without looking at them one by one.

## The problem

The input is an array $A[0 \ldots n-1]$ of items from a [total order](/total-order/). The output is $\operatorname{inv}(A) = |\{(p, q) : p < q,\ A[p] > A[q]\}|$. This is the [counting inversions](/counting-inversions/) problem. The algorithm also leaves $A$ sorted. To keep the input, run it on a copy.

## The algorithm

The call SORT-AND-COUNT$(A, 0, n)$ returns $\operatorname{inv}(A)$ and sorts $A$. The range $[lo, hi)$ is half-open.

```pseudo id=main
SORT-AND-COUNT(A, lo, hi)                ▷ count the inversions of A[lo .. hi − 1] and sort it
L1  if hi − lo ≤ 1 then return 0
L2  mid ← lo + ⌊(hi − lo) / 2⌋
L3  x ← SORT-AND-COUNT(A, lo, mid)
L4  y ← SORT-AND-COUNT(A, mid, hi)
L5  return x + y + MERGE-AND-COUNT(A, lo, mid, hi)

MERGE-AND-COUNT(A, lo, mid, hi)          ▷ both halves are sorted
L6  B ← a copy of A[lo .. mid − 1]
L7  i ← 0, j ← mid, k ← lo, c ← 0
L8  while i < |B| and j < hi do
L9      if B[i] ≤ A[j] then A[k] ← B[i], i ← i + 1
L10     else A[k] ← A[j], j ← j + 1, c ← c + (|B| − i)   ▷ B[i .. |B| − 1] are all larger
L11     k ← k + 1
L12 while i < |B| do
L13     A[k] ← B[i], i ← i + 1, k ← k + 1
L14 return c
```

The merge is the merge of [merge sort](/merge-sort/), with one counter. Line L10 is the only new work. It runs when the front item $A[j]$ of the right half is strictly smaller than the front item $B[i]$ of the left half. Since $B$ is sorted, $B[i], B[i+1], \ldots, B[|B|-1]$ are all larger than $A[j]$, and all of them were to the left of $A[j]$ in the range. The items $B[0 \ldots i-1]$ are already placed and are at most $A[j]$. So $A[j]$ is the right element of exactly $|B| - i$ crossing inversions. When $B$ is used up first, the rest of the right half is larger than or equal to each left item and adds nothing.

## Example

Count the inversions of $A = [7, 5, 3, 1, 8, 6, 4, 2]$.

| merge | left half | right half | result | items taken from the right, with the waiting left items | crossing count |
| --- | --- | --- | --- | --- | --- |
| 1 | [7] | [5] | [5 7] | 5 (1 waiting) | 1 |
| 2 | [3] | [1] | [1 3] | 1 (1) | 1 |
| 3 | [5 7] | [1 3] | [1 3 5 7] | 1 (2), 3 (2) | 4 |
| 4 | [8] | [6] | [6 8] | 6 (1) | 1 |
| 5 | [4] | [2] | [2 4] | 2 (1) | 1 |
| 6 | [6 8] | [2 4] | [2 4 6 8] | 2 (2), 4 (2) | 4 |
| 7 | [1 3 5 7] | [2 4 6 8] | [1 2 ... 8] | 2 (3), 4 (2), 6 (1) | 6 |

The total is $1 + 1 + 4 + 1 + 1 + 4 + 6 = 18$. In the last merge, 1 goes first from the left. Then 2 is taken from the right while 3, 5 and 7 wait, which counts the inversions $(3, 2)$, $(5, 2)$ and $(7, 2)$. The item 8 is left over at the end and adds nothing, because the left half is empty by then.

## Correctness

The key fact is a [loop invariant](/loop-invariant/) of line L8: $c$ is the number of pairs (left item, right item) with the left item larger, among the right items already placed, and each placed left item is at most each right item not yet placed. With it, MERGE-AND-COUNT returns the number of crossing inversions of the range. The inversions of $A[lo \ldots hi-1]$ split into the inversions inside the left half, inside the right half, and across the middle. Sorting a half does not change the number of crossing pairs, because that number depends only on the two sets of values. So SORT-AND-COUNT is correct by strong induction on $hi - lo$, as in merge sort. The full proof is below.

## Complexity

**Time.** The recursion is that of merge sort, and the counter adds $O(1)$ work to each step of the merge. So

$$T(n) = T(\lceil n/2 \rceil) + T(\lfloor n/2 \rfloor) + \Theta(n), \qquad T(1) = \Theta(1),$$

and $T(n) = \Theta(n \log n)$ in every case. The number of comparisons is the number of merge sort, at most $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$.

**Optimality.** In the [comparison model](/comparison-model/), each algorithm that counts inversions needs at least $\lceil \lg n! \rceil = n \lg n - O(n)$ comparisons in the worst case, as the [counting inversions](/counting-inversions/) page proves. So this algorithm is optimal up to a lower-order term.

**Space.** The buffer $B$ holds at most $\lceil n/2 \rceil$ items, and the recursion stack has depth $\lceil \lg n \rceil$. With one shared buffer the extra space is $\Theta(n)$.

**Size of the answer.** The count is at most $\binom n2$. This exceeds the largest signed 32-bit integer $2^{31} - 1$ once $n \ge 65\,537$, so the counter must be a 64-bit integer.

## Properties

- **Exact for repeated keys.** Equal items are not counted, because line L9 takes the left item when $B[i] = A[j]$.
- **Stable.** The sort that comes with the count is the stable merge sort.
- **Destroys the input order.** The array ends sorted. Count on a copy to keep the original.
- **Not adaptive.** It does $\Theta(n \log n)$ work even on a sorted array.

## Variants and improvements

- **Count for each item.** To get, for each item, the number of smaller items to its right, sort pairs (value, original index). When line L9 places a left item, add $j - mid$ to its count: these are the right items already placed, which are smaller and later. For a permutation the result is its [Lehmer code](/lehmer-code/).
- **Significant inversions.** To count pairs with $A[p] > 2A[q]$, run a separate two-pointer pass over the two sorted halves before the merge. The merge itself stays unchanged, so the time stays $\Theta(n \log n)$.
- **Bottom-up.** Merge runs of length 1, 2, 4, and so on, adding the counts of all merges. This needs no recursion.
- **Natural runs.** Start from the maximal non-decreasing runs of the input. A sorted run has no inversions, so the count starts at 0 for each run and the time is $O(n \log r)$ for $r$ runs, as in [natural merge sort](/natural-merge-sort/).
- **Kendall tau.** Relabel one ranking by the positions in the other, then count. See [ranking comparison by Kendall tau](/ranking-comparison-kendall-tau/).

## When to use it

Use it when the keys can only be compared, or when you also want the sorted order. Its time does not depend on the range of the keys. When the keys are small integers, the [Fenwick tree count](/inversion-count-with-fenwick-tree/) is shorter to write, does not move the data, and gives the count of each prefix online. When the count is known to be small, [insertion sort](/insertion-sort/) counting its shifts takes $\Theta(n + \operatorname{inv}(A))$ time.

## Pitfalls

- **Strict and non-strict tests.** With $B[i] < A[j]$ in line L9, equal keys go to line L10 and each pair of equal keys across the middle counts as an inversion. The test must be $B[i] \le A[j]$.
- **Adding 1 instead of $|B| - i$.** Line L10 must add the number of waiting left items. Adding 1 counts only the pairs whose left item is the front one.
- **Counting on the wrong side.** Adding $|B| - i$ when a *left* item is placed counts something else. The count goes with each item taken from the right.
- **A 32-bit counter.** The answer reaches $\binom n2$, which overflows a signed 32-bit integer for $n \ge 65\,537$ on a decreasing input.
- **A buffer in each call.** As in merge sort, allocate one buffer of $\lceil n/2 \rceil$ items and reuse it.

## Implementations

## History

Counting inversions by divide and conquer is a classic textbook exercise. CLRS asks for it in Problem 2-4 of Chapter 2, and Kleinberg and Tardos use it in Section 5.3, under the names Merge-and-Count and Sort-and-Count, with the comparison of two rankings of songs or films as the motivating use.

## References
