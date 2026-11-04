---
tag: HR9MYC
kind: algorithm
slug: hoare-partition
name: Hoare partition scheme
aliases:
- Hoare partitioning
area: sorting/comparison-sorts
level: core
summary: Partition scheme scanning from both ends that swaps out-of-place pairs; fewer swaps and handles duplicates well.
model: comparison-model
complexity:
  vars: {m: the number of items in the range}
  time: {worst: Θ(m), average: Θ(m), best: Θ(m)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1961
  people: [C. A. R. Hoare]
  note: Hoare published Partition and Quicksort as Algorithms 63 and 64 of the Communications of the ACM in 1961, and described the method in full in The Computer Journal in 1962.
prereqs: [loop-invariant, partition-around-pivot]
see_also: [quicksort, lomuto-partition, bentley-mcilroy-partitioning, three-way-quicksort, dual-pivot-quicksort, quickselect, median-of-three-pivot]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 7, Problem 7-1, Hoare partition correctness (the procedure HOARE-PARTITION and the three properties to prove)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (Algorithm Q, quicksort, with the two scans that meet)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.3, Quicksort (the partitioning method with two scans, and the discussion of keys equal to the partitioning item)
  - paper: doi:10.1093/comjnl/5.1.10
    title: C. A. R. Hoare, Quicksort, The Computer Journal 5(1) (1962)
    locator: pp. 10 to 16
  - paper: "C. A. R. Hoare, Algorithm 63: Partition, and Algorithm 64: Quicksort, Communications of the ACM 4(7) (1961)"
    locator: p. 321
---

The Hoare partition scheme rearranges a range of an array around a pivot with two scans, one from the left and one from the right. Each scan stops at an item on the wrong side, the two items are exchanged, and the scans go on until they cross. It returns an index $j$ such that each item up to $j$ is at most each item after $j$. It is the partition of Hoare's original [quicksort](/quicksort/), it makes about three times fewer exchanges than the [Lomuto partition](/lomuto-partition/) on random input, and it splits a range of equal keys near the middle.

## In plain words

Pick the first item of the range as the pivot. Put one finger at the left end and one at the right end. Move the right finger to the left until it points at an item that is not larger than the pivot. Move the left finger to the right until it points at an item that is not smaller than the pivot. These two items are each on the wrong side, so swap them. Then go on from there.

When the fingers meet or cross, stop. Everything left of the meeting point is at most the pivot, and everything right of it is at least the pivot. The pivot itself is somewhere in the range, not always at the meeting point.

## The problem

The input is a range $A[lo \ldots hi]$ of an array, with $lo < hi$, of items with a total order. The output is a rearrangement of the range and an index $j$ with $lo \le j < hi$ such that

$$A[k] \le A[l] \quad \text{for each } k \text{ with } lo \le k \le j \text{ and each } l \text{ with } j < l \le hi.$$

This is a weak form of [partition around a pivot](/partition-around-pivot/): both parts are not empty, but the pivot is not put at a fixed place. Quicksort then sorts $A[lo \ldots j]$ and $A[j+1 \ldots hi]$.

## The algorithm

This is the form of CLRS, Problem 7-1. The range is closed: it holds $A[lo]$ to $A[hi]$.

```pseudo id=main
HOARE-PARTITION(A, lo, hi)                 ▷ lo < hi
L1  x ← A[lo]                              ▷ the pivot
L2  i ← lo − 1, j ← hi + 1
L3  loop
L4      repeat j ← j − 1 until A[j] ≤ x
L5      repeat i ← i + 1 until A[i] ≥ x
L6      if i < j then exchange A[i] and A[j]
L7      else return j
```

Line L4 moves $j$ left past the items that are greater than the pivot. Line L5 moves $i$ right past the items that are less than the pivot. Both scans stop at an item equal to the pivot. If the two indices have not crossed, line L6 exchanges the two items, so that each one is now on its correct side. The scans need no test of the array bounds. In the first round, the pivot $A[lo]$ itself stops both scans. In each later round, the item that line L6 put at the old $i$ is at most $x$ and stops the scan of $j$, and the item at the old $j$ is at least $x$ and stops the scan of $i$.

## Example

Partition $A = [5, 3, 8, 4, 9, 2, 7, 1, 6]$ with $lo = 0$ and $hi = 8$. The pivot is $x = 5$.

| round | scan of $j$ stops at | scan of $i$ stops at | action | the array after the round |
|---|---|---|---|---|
| 1 | $j = 7$ ($A[7] = 1$) | $i = 0$ ($A[0] = 5$) | exchange | 1 3 8 4 9 2 7 5 6 |
| 2 | $j = 5$ ($A[5] = 2$) | $i = 2$ ($A[2] = 8$) | exchange | 1 3 2 4 9 8 7 5 6 |
| 3 | $j = 3$ ($A[3] = 4$) | $i = 4$ ($A[4] = 9$) | return $j = 3$ | 1 3 2 4 9 8 7 5 6 |

The result is $j = 3$. The left part $[1, 3, 2, 4]$ is at most 5 and the right part $[9, 8, 7, 5, 6]$ is at least 5. The pivot 5 is in the right part, at index 7. The run makes 11 comparisons of items with the pivot and 2 exchanges.

## Correctness

The proof uses this [loop invariant](/loop-invariant/) at the start of each round after the first: $lo \le i < j \le hi$, each item of $A[lo \ldots i]$ is at most $x$, and each item of $A[j \ldots hi]$ is at least $x$. The items at $i$ and $j$ then stop the next scans, so the indices stay in the range. When the scans cross, $A[lo \ldots j]$ is at most $x$ and $A[j+1 \ldots hi]$ is at least $x$. The returned $j$ is less than $hi$, because $j$ can stay at $hi$ only in the first round, and then $i = lo < j$ and the loop goes on. The full proof is below.

## Complexity

Let $m = hi - lo + 1$.

- **Comparisons.** Each index of the range is compared by the scan of $i$ or by the scan of $j$, and at most two indices are compared by both, where the scans cross. So a call makes $m + 1$ or $m + 2$ comparisons with the pivot. Each comparison costs $O(1)$, so the time is $\Theta(m)$ in each case.
- **Exchanges.** Each exchange moves $i$ and $j$ closer by at least 2, so there are at most $\lfloor m/2 \rfloor$ exchanges. On a random permutation of distinct keys, the mean number of exchanges over all $m!$ orders is $(m+1)/6$ for each $m$ from 2 to 8, so about $m/6$. The Lomuto partition makes about $m/2$ exchanges on average.
- **Equal keys.** If all keys are equal, both scans stop at each item, so there are $\lfloor m/2 \rfloor$ exchanges, and $j$ ends at the middle: for $m = 8$ the parts have 4 and 4 items, and for $m = 9$ they have 5 and 4. So quicksort with this partition takes $\Theta(m \log m)$ time on all-equal keys, while quicksort with the Lomuto partition takes $\Theta(m^2)$.
- **Space.** $\Theta(1)$ extra.

## Properties

- **Not stable.** Line L6 exchanges items far apart, so equal items can change their order.
- **In place.** Two indices and the pivot.
- **The pivot is not placed.** Unlike the Lomuto partition, the scheme does not return the final place of the pivot. Quicksort must recurse on $A[lo \ldots j]$ and $A[j+1 \ldots hi]$, both of which can hold items equal to the pivot.
- **Both parts are not empty.** Since $lo \le j < hi$, each recursive call of quicksort is on a strictly shorter range. This is what makes the recursion stop.

## Variants and improvements

- **The pivot at the end of the scans.** Sedgewick and Wayne exclude the pivot from the scans, and at the end exchange it into $A[j]$. Then the pivot is at its final place, and quicksort recurses on $A[lo \ldots j-1]$ and $A[j+1 \ldots hi]$.
- **A random or median-of-three pivot.** Exchange a random item, or the median of three items, into $A[lo]$ before line L1. See [median-of-three pivot](/median-of-three-pivot/) and [randomized quicksort](/randomized-quicksort/).
- **[Bentley-McIlroy partitioning](/bentley-mcilroy-partitioning/).** Use the same two scans, but move the items equal to the pivot to the two ends and then into the middle. This gives a three-way partition with few extra exchanges.
- **[Dual-pivot quicksort](/dual-pivot-quicksort/).** Partition around two pivots into three parts.

## When to use it

Use the Hoare scheme in a quicksort or a [quickselect](/quickselect/) when speed matters: it makes fewer exchanges than Lomuto and handles many equal keys well. Use the Lomuto scheme when the code must be short and must put the pivot at its final place, for example to teach. When there are very many equal keys, a three-way partition is better than both.

## Pitfalls

- **The pivot at the right end.** With $x \leftarrow A[hi]$ in line L1, the result can be $j = hi$, for example on $[1, 2]$. Then quicksort calls itself on the same range again, and the recursion never stops. Take the pivot from $A[lo]$, or exchange the chosen pivot there first.
- **Strict tests in the scans.** With "until $A[j] < x$" and "until $A[i] > x$" in lines L4 and L5, the scans no longer stop at equal items. On all-equal keys a scan then runs off the end of the range, because no sentinel stops it.
- **Recursing on the wrong ranges.** Quicksort must call itself on $[lo, j]$ and $[j+1, hi]$. The calls on $[lo, j-1]$ and $[j+1, hi]$, as with Lomuto, can leave an item out of place, because $A[j]$ is not the pivot in general.
- **Returning $i$ instead of $j$.** With the test $i < j$ in line L6, the split point is $j$. Code that returns $i$ must use the ranges $[lo, i-1]$ and $[i, hi]$, and then the case $i = lo$ makes an empty part.

## Implementations

## History

C. A. R. Hoare invented quicksort in 1959 and 1960, and published the procedures Partition and Quicksort as Algorithms 63 and 64 in the Communications of the ACM in July 1961. His paper Quicksort in The Computer Journal in 1962 describes the partition with two scans from the two ends, and analyses the method. Knuth's Algorithm Q in Section 5.2.2 and the procedure HOARE-PARTITION in CLRS, Problem 7-1, are close to Hoare's form.

## References
