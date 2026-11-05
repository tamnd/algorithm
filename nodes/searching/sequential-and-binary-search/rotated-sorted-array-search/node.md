---
tag: 34SK70
kind: problem
slug: rotated-sorted-array-search
name: Search in a rotated sorted array
aliases:
- cyclically shifted sorted array search
area: searching/sequential-and-binary-search
level: core
summary: Find a key in a sorted array rotated at an unknown pivot in O(log n) time when the values are distinct.
model: comparison-model
complexity:
  vars: {n: the number of items in the array (the bound is for distinct items; with duplicates it is Θ(n))}
  time: {worst: Θ(log n)}
prereqs: [rotated-sorted-array-minimum]
see_also: [rotated-sorted-array-minimum, binary-search, search-in-sorted-array, lower-bound-query, sorted-search-lower-bound, unimodal-maximum, bitonic-sequence, adversary-argument]
sources:
  - url: https://leetcode.com/problems/search-in-rotated-sorted-array/
    title: LeetCode 33, Search in rotated sorted array
  - url: https://leetcode.com/problems/search-in-rotated-sorted-array-ii/
    title: LeetCode 81, Search in rotated sorted array II (with duplicates)
---

Search in a rotated sorted array asks for the index of a key $x$ in an array that was sorted and then rotated by an unknown number of places, such as $[15, 18, 22, 27, 3, 6, 9, 11, 13]$. The array is not sorted, but it is made of two sorted runs, and with distinct items one [binary search](/binary-search/) loop solves the problem in $O(\log n)$ comparisons: at each midpoint, one of the two halves is sorted, and a test of its two ends tells whether $x$ can be in it. Another method finds the pivot first, as in [minimum of a rotated sorted array](/rotated-sorted-array-minimum/), and then searches the right run. With duplicates the worst case becomes $\Theta(n)$.

## In plain words

A sorted row of numbers was cut once and the two parts were swapped. You want to find one number in it.

Look at the middle. The cut is on one side of the middle, so the other side is in order. You can tell which side is in order by looking at its two ends: in an ordered part, the first number is smaller than the last. If your number lies between the two ends of the ordered side, it can only be there. If not, it can only be on the other side. Either way you throw away half the row.

## Definition

**Input.** An array $A[0 \ldots n-1]$, $n \ge 0$, of distinct items from a [total order](/total-order/), that is a rotation of a sorted array: for some pivot $p$, $A[p] < \cdots < A[n-1] < A[0] < \cdots < A[p-1]$. The pivot is not given. A key $x$.

**Output.** The index $i$ with $A[i] = x$, or NIL when $x$ is not in $A$.

With $p = 0$ the input is a sorted array, so the problem contains [search in a sorted array](/search-in-sorted-array/).

## Variants

- **Duplicates.** The items may repeat, and the output is any index of $x$. The one-loop method must then handle $A[lo] = A[mid]$, where it cannot tell which half is sorted, and the worst case is $\Theta(n)$.
- **Return the position.** For an absent key, return the place where $x$ would go in the rotated order. The two-phase method gives it at once, as a [lower bound](/lower-bound-query/) inside one run.
- **Unknown rotation and unknown direction.** An array that is a rotation of a sorted array in either order; first compare the ends of a few items to find the direction.
- **Bitonic arrays.** An array that rises and then falls is a [bitonic sequence](/bitonic-sequence/). A search there first finds the maximum, as in [unimodal search](/unimodal-maximum/), then searches both runs.

## Examples

For $A = [15, 18, 22, 27, 3, 6, 9, 11, 13]$, $n = 9$, the pivot is 4.

**Search for $x = 9$.** At $lo = 0$, $hi = 8$, $mid = 4$: $A[4] = 3 \ne 9$. Since $A[0] = 15 > A[4] = 3$, the left half holds the drop, so the right half $A[4 \ldots 8] = [3, 6, 9, 11, 13]$ is sorted. As $3 < 9 \le 13$, the key can only be there: $lo = 5$. At $mid = 6$, $A[6] = 9$: return 6.

**Search for $x = 20$.** At $mid = 4$ the right half is sorted, and 20 is not in $(3, 13]$, so $hi = 3$. At $lo = 0$, $hi = 3$, $mid = 1$: $A[0] = 15 \le A[1] = 18$, so the left half is sorted, and 20 is not in $[15, 18)$: $lo = 2$. At $mid = 2$, then at $mid = 3$, the same test fails, and the range becomes empty: NIL.

**Comparison counts.** The table gives the largest number of item comparisons measured on arrays $[0, 2, \ldots, 2n - 2]$ rotated by every multiple of $\max(1, \lfloor n / 100 \rfloor)$, over every key from $-1$ to $2n$, with each $\le$, $<$ and $=$ counted:

| $n$ | 10 | 100 | 1000 |
|---|---|---|---|
| one loop, bound $4(\lfloor \lg n \rfloor + 1)$ | 16 | 28 | 40 |
| pivot, then binary search, bound $2\lceil \lg n \rceil + 2$ | 10 | 16 | 22 |
| lower bound $\lceil \lg(n + 1) \rceil$ | 4 | 7 | 10 |

## Known algorithms

**One loop.**

```pseudo id=oneloop
ROTATED-SEARCH(A, x)                    ▷ distinct items
L1  lo ← 0, hi ← n − 1                  ▷ if x is in A, it is in A[lo .. hi]
L2  while lo ≤ hi do
L3      mid ← lo + ⌊(hi − lo) / 2⌋
L4      if A[mid] = x then return mid
L5      if A[lo] ≤ A[mid] then          ▷ A[lo .. mid] is sorted
L6          if A[lo] ≤ x < A[mid] then hi ← mid − 1 else lo ← mid + 1
L7      else                            ▷ A[mid .. hi] is sorted
L8          if A[mid] < x ≤ A[hi] then lo ← mid + 1 else hi ← mid − 1
L9  return NIL
```

*Why it is correct.* The range $A[lo \ldots hi]$ is always a contiguous part of a rotated sorted array, so it holds at most one drop. If $A[lo] \le A[mid]$, the drop is not in $A[lo \ldots mid]$ (a drop there would make every item from $lo$ to the drop larger than every item after it, so $A[lo] > A[mid]$), and that half is sorted. Then $x$ is in it exactly when $A[lo] \le x < A[mid]$, given $x \ne A[mid]$. Otherwise the drop is in the left half, so $A[mid \ldots hi]$ has no drop and is sorted, and $x$ is in it exactly when $A[mid] < x \le A[hi]$. In both cases the step keeps the half that can hold $x$. Each step removes $mid$ and at least half of the rest, so there are at most $\lfloor \lg n \rfloor + 1$ steps, each with at most four comparisons.

**Pivot, then binary search.** Find the pivot $p$ with $\lceil \lg n \rceil$ comparisons by the method of [minimum of a rotated sorted array](/rotated-sorted-array-minimum/). If $x \le A[n-1]$, the key can only be in the run $A[p \ldots n-1]$; otherwise only in $A[0 \ldots p-1]$. A lower bound search in that run, and one equality test, finish. The total is at most $2\lceil \lg n \rceil + 2$ comparisons, fewer than the one loop, and the code reuses two standard searches.

**Virtual index.** After finding $p$, run an ordinary binary search on the virtual sorted array $B[i] = A[(i + p) \bmod n]$, and map the result back.

**Duplicates.** In the one-loop method, when $A[lo] = A[mid] = A[hi]$, neither half is known to be sorted; move $lo$ up by one and $hi$ down by one, and go on; both items equal $A[mid]$, which is not $x$. In all other cases the test of line L5 is still valid: if the drop were in $A[lo \ldots mid]$, the items after it would give $A[mid] \le A[hi] \le A[lo]$, so $A[lo] = A[mid]$ would force $A[hi] = A[lo]$ too. This keeps the method correct, with a worst case of $\Theta(n)$.

## Bounds

**Distinct items.** The two-phase method gives at most $2\lceil \lg n \rceil + 2$ comparisons, so the problem is $\Theta(\log n)$. Since sorted arrays are inputs, the [sorted search lower bound](/sorted-search-lower-bound/) gives at least $\lceil \lg(n + 1) \rceil$ three-way comparisons.

**Duplicates.** Each deterministic algorithm reads all $n$ items on some input. *Proof.* Let the key be $x = 0$. The array of all 1 values is a valid input, with the answer NIL, and for each $j$ the array with 0 at index $j$ and 1 elsewhere is a rotation of $[0, 1, \ldots, 1]$, with the answer $j$. An [adversary](/adversary-argument/) answers every read with 1. If the algorithm stops with some index $j$ unread, then both the all-1 array and the array with 0 at $j$ fit the answers, and they need different outputs, so one of them gets a wrong output. $\blacksquare$

## Reductions

- **[Search in a sorted array](/search-in-sorted-array/) reduces to it,** with the pivot 0.
- **It reduces to the [minimum of a rotated sorted array](/rotated-sorted-array-minimum/) and two binary searches,** as in the two-phase method.
- **It reduces to search in a sorted array by a change of index,** once the pivot is known: $B[i] = A[(i + p) \bmod n]$ is sorted.

## Applications

- Search a circular buffer of sorted timestamps, such as a log that wraps around, for the entry of a given time.
- Search a sorted table that was rotated so that a chosen item comes first, such as a list of time zones that starts at the local one.
- A standard exercise in writing a correct binary search under a changed invariant.

## References
