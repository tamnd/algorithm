---
tag: BP75ME
kind: problem
slug: rotated-sorted-array-minimum
name: Minimum of a rotated sorted array
aliases:
- pivot finding in a rotated array
area: searching/sequential-and-binary-search
level: core
summary: Find the smallest element of a rotated sorted array, which marks the pivot, in O(log n) time for distinct values.
model: comparison-model
complexity:
  vars: {n: the number of items in the array (the bound is for distinct items; with duplicates it is Θ(n))}
  time: {worst: Θ(log n)}
prereqs: [binary-search, lower-and-upper-bound-search]
see_also: [rotated-sorted-array-search, lower-and-upper-bound-search, peak-finding, unimodal-maximum, find-maximum, minimal-rotation, vector-rotation, adversary-argument]
sources:
  - url: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
    title: LeetCode 153, Find minimum in rotated sorted array
  - url: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/
    title: LeetCode 154, Find minimum in rotated sorted array II (with duplicates)
---

The minimum of a rotated sorted array is the problem of finding the smallest item of an array that was sorted and then rotated by an unknown number of places, such as $[15, 18, 22, 27, 3, 6, 9, 11, 13]$. The index of the minimum is the *pivot*: it tells how far the array was rotated, and it splits the array into two sorted runs. A scan finds it with $n - 1$ comparisons, but when the items are distinct a [binary search](/binary-search/) finds it with $\lceil \lg n \rceil$, by comparing the middle item with the last one. With duplicates the problem changes: an array of equal items with one smaller item hidden anywhere needs $n - 1$ comparisons, so no method beats the scan in the worst case.

## In plain words

Someone took a sorted row of numbers, cut it at one place, and swapped the two parts. Now the row goes up, drops once, and goes up again. You want the place of the drop, where the smallest number is.

Look at the middle number and the last number. If the middle is bigger than the last, the drop is to the right of the middle. If the middle is smaller, everything from the middle to the end goes up, so the drop is at the middle or to its left. Each look halves the part where the drop can be.

If numbers can repeat, a middle number equal to the last one tells you nothing about the side, and you may have to look at every number.

## Definition

**Input.** An array $A[0 \ldots n-1]$, $n \ge 1$, from a [total order](/total-order/), that is a *rotation* of a sorted array: there is a $p \in \{0, \ldots, n-1\}$ such that

$$ A[p] \le A[p+1] \le \cdots \le A[n-1] \le A[0] \le \cdots \le A[p-1]. $$

**Output.** An index of a minimum of $A$. For distinct items the minimum is at the unique pivot $p$ (with $p = 0$ when the array is not rotated), and the output is $p$.

**Rotation.** If $B$ is the sorted array, then $A[i] = B[(i - p) \bmod n]$: the array was rotated right by $p$ places, or left by $n - p$. So the output also gives the amount of the rotation.

## Variants

- **Distinct items.** The main case, solved in $\lceil \lg n \rceil$ comparisons.
- **Duplicates.** The minimum value is still well defined, but its index can need $\Theta(n)$ comparisons. A careful search is still $O(\log n)$ on most inputs.
- **Maximum.** For distinct items the maximum is at $p - 1$ (or $n - 1$ when $p = 0$).
- **The rotation of a string.** The lexicographically least rotation of a string is a different problem, the [minimal rotation](/minimal-rotation/), solved in linear time.
- **Search for a key.** Finding a key in a rotated array is the problem of [search in a rotated sorted array](/rotated-sorted-array-search/), which uses this one as a first step or folds it into one loop.

## Examples

**Distinct items.** For $A = [15, 18, 22, 27, 3, 6, 9, 11, 13]$ the pivot is $p = 4$.

| step | $lo$ | $hi$ | $mid$ | $A[mid]$ vs $A[hi]$ | move |
|---|---|---|---|---|---|
| 1 | 0 | 8 | 4 | $3 < 13$ | $hi = 4$ |
| 2 | 0 | 4 | 2 | $22 > 3$ | $lo = 3$ |
| 3 | 3 | 4 | 3 | $27 > 3$ | $lo = 4$ |
| end | 4 | 4 | | | return 4 |

Three comparisons. Over all $n$ rotations of a sorted array of $n$ distinct items, the largest number of comparisons is exactly $\lceil \lg n \rceil$ for every $n$ from 1 to 69, counted by running the search.

**Duplicates.** The arrays $[2, 2, 2, 0, 2]$ and $[2, 0, 2, 2, 2]$ are both rotations of $[0, 2, 2, 2, 2]$. In both, $A[0] = A[2] = A[4] = 2$, so the first item, the middle item and the last item are the same, and they cannot tell the two arrays apart.

## Known algorithms

```pseudo id=pivot
ROTATED-MIN(A)                           ▷ n ≥ 1, distinct items
L1  lo ← 0, hi ← n − 1                   ▷ the minimum is in A[lo .. hi]
L2  while lo < hi do
L3      mid ← lo + ⌊(hi − lo) / 2⌋        ▷ lo ≤ mid < hi
L4      if A[mid] > A[hi] then lo ← mid + 1   ▷ the drop is after mid
L5      else hi ← mid                    ▷ A[mid .. hi] is increasing
L6  return lo
```

**Why it is correct.** The loop keeps this invariant: $A[lo \ldots hi]$ is a rotation of a sorted array, and it holds the minimum of $A$. A contiguous part of a rotated sorted array is again one: it holds at most one drop, and if it holds the drop, its last item is less than its first. In a step, if the part $A[mid + 1 \ldots hi]$ holds the drop, then all items before the drop are larger than all items after it, so $A[mid] > A[hi]$. So if $A[mid] > A[hi]$ there is a drop between $mid$ and $hi$, every item of $A[lo \ldots mid]$ is larger than $A[hi]$, and the minimum is in $A[mid + 1 \ldots hi]$. If $A[mid] < A[hi]$, the part $A[mid \ldots hi]$ has no drop and increases, so its minimum is $A[mid]$, and the minimum is in $A[lo \ldots mid]$. When $lo = hi$, the one item is the minimum.

**Cost.** The range shrinks from $s$ to $\lfloor s/2 \rfloor$ or $\lceil s/2 \rceil$ items, so the loop makes at most $\lceil \lg n \rceil$ comparisons. It is the boundary search of [lower and upper bound search](/lower-and-upper-bound-search/) for the test $P(i) = (A[i] \le A[n-1])$, which is false before the pivot and true from the pivot on.

**Duplicates.** Replace line L5 by two cases: if $A[mid] < A[hi]$ then $hi \gets mid$; if $A[mid] = A[hi]$ then $hi \gets hi - 1$. The last step is safe: if $A[hi]$ is a minimum, then so is $A[mid]$, which stays in the range. This finds the minimum value with $O(\log n)$ comparisons when few items are equal, and with up to $n - 1$ when many are. On $[1, 1, \ldots, 1, 0]$ it is fast (9 comparisons for $n = 1000$), but on $[0, 1, 1, \ldots, 1]$ it moves $hi$ one place at a time and makes 999.

**Scan.** A scan for the minimum, as in [finding the maximum](/find-maximum/), makes $n - 1$ comparisons on any input.

## Bounds

**Distinct items.** $\lceil \lg n \rceil$ comparisons are enough, and needed. *Lower bound.* Each of the $n$ rotations of a sorted array of distinct items has a different answer, so a decision tree with two-way comparisons needs $n$ leaves and height at least $\lceil \lg n \rceil$. $\blacksquare$

**Duplicates.** Each deterministic algorithm reads at least $n - 1$ items, and makes at least $\lceil (n-1)/2 \rceil$ comparisons, on some input with only the values 0 and 1.

*Proof.* For each index $j$ let $E_j$ be the array with 0 at index $j$ and 1 elsewhere; it is a rotation of $[0, 1, \ldots, 1]$, and its only correct output is $j$. The array of all 1 values is also a valid input. An [adversary](/adversary-argument/) answers every read with 1, and every comparison with "equal". These answers fit $E_j$ for each index $j$ that the algorithm never read. Let $o$ be the output. If some index $j \ne o$ was never read, the answers fit $E_j$, for which $o$ is wrong. So at least $n - 1$ indices are read. A comparison reads two items, so at least $\lceil (n - 1)/2 \rceil$ comparisons are made. $\blacksquare$

So with duplicates the worst case is $\Theta(n)$, and the scan is optimal up to a constant factor.

## Reductions

- **[Search in a rotated sorted array](/rotated-sorted-array-search/) reduces to it.** Find the pivot $p$, then run binary search on $A[0 \ldots p-1]$ or $A[p \ldots n-1]$, chosen by comparing the key with $A[n-1]$. The total is about $2\lg n$ comparisons.
- **It is a boundary search** for $P(i) = (A[i] \le A[n - 1])$, so it reduces to the first-true search of [lower and upper bound search](/lower-and-upper-bound-search/).
- **It is close to [unimodal search](/unimodal-maximum/).** The maximum of a rotated array is the last item before the drop; for distinct items, the array read from the pivot is sorted, so the maximum is at $p - 1$.

## Applications

- Find the start of a circular log or a ring buffer whose entries carry increasing timestamps and that was written over in place, without a pointer to the oldest entry.
- Undo a rotation: find how far a sorted list was rotated, for example after a shift of a sorted circular schedule.
- The first step of key search in a rotated array, and of merging such an array with another sorted array.

## References
