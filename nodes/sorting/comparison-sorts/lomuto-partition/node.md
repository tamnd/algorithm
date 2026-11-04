---
tag: N086ME
kind: algorithm
slug: lomuto-partition
name: Lomuto partition scheme
aliases:
- Lomuto partitioning
area: sorting/comparison-sorts
level: core
summary: Partition scheme that scans once and places the pivot at its final index; simple but does more swaps.
model: comparison-model
complexity:
  vars: {m: the number of items in the range}
  time: {worst: Θ(m), average: Θ(m), best: Θ(m)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [loop-invariant, partition-around-pivot]
see_also: [quicksort, hoare-partition, three-way-quicksort, dutch-national-flag, quickselect, randomized-quicksort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 7.1, Description of quicksort (the procedure PARTITION and its loop invariant)
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 11, Sorting, Section 11.2 (a simple quicksort, with the partition credited to Nico Lomuto)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (partition schemes and the count of exchanges)
---

The Lomuto partition scheme rearranges a range of an array around a pivot $x$, the last item of the range, so that the items at most $x$ come first, then $x$, then the items larger than $x$. It scans the range once from left to right, makes exactly $m - 1$ comparisons on a range of $m$ items, and returns the final index of the pivot. It is the partition of [quicksort](/quicksort/) in CLRS and in many courses, because its [loop invariant](/loop-invariant/) is short. It does more swaps than the [Hoare partition](/hoare-partition/), and it is slow on ranges with many equal items.

## In plain words

You have a row of cards and one chosen card, the pivot, at the right end. You want all cards that are not larger than the pivot on the left, then the pivot, then the larger cards.

You walk along the row from the left. You keep a "small" block at the left end, which starts empty. When you see a small card, you swap it with the first card after the small block, so the small block grows by one. When you see a large card, you do nothing and walk on. The large cards collect between the small block and your position.

At the end, you swap the pivot with the first large card. Now the pivot sits between the two groups, at its final place in sorted order.

## The problem

The input is an array $A$ and a range $[lo, hi)$ with $hi - lo = m \ge 1$, of items with a total order. Let $x = A[hi - 1]$. The output is an index $p$ with $lo \le p < hi$ and a permutation of the range such that

$$A[lo \ldots p-1] \le x = A[p] < A[p+1 \ldots hi-1].$$

So $x$ is at the index that it has in the sorted range, when equal items count as smaller. This is the step of [partitioning around a pivot](/partition-around-pivot/).

## The algorithm

```pseudo id=main
LOMUTO-PARTITION(A, lo, hi)                ▷ hi − lo ≥ 1; the pivot is A[hi − 1]
L1  x ← A[hi − 1]
L2  i ← lo                                 ▷ A[lo .. i − 1] ≤ x and A[i .. j − 1] > x
L3  for j ← lo to hi − 2 do
L4      if A[j] ≤ x then
L5          swap A[i] and A[j]
L6          i ← i + 1
L7  swap A[i] and A[hi − 1]
L8  return i
```

During the loop the range has four parts. The part $A[lo \ldots i-1]$ holds the items at most $x$. The part $A[i \ldots j-1]$ holds the items larger than $x$. The part $A[j \ldots hi-2]$ is not yet seen, and $A[hi-1]$ is the pivot. An item at most $x$ at index $j$ is swapped with $A[i]$, the first item of the large part, and both parts move one place right. Line L7 swaps the pivot with the first large item, or with itself when there is no large item.

## Example

Partition $A = [6, 3, 9, 1, 7, 2, 8, 5]$. The pivot is $x = 5$.

| $j$ | $A[j]$ | action | the array after the step | $i$ |
|---|---|---|---|---|
| 0 | 6 | none | 6 3 9 1 7 2 8 5 | 0 |
| 1 | 3 | swap $A[0], A[1]$ | 3 6 9 1 7 2 8 5 | 1 |
| 2 | 9 | none | 3 6 9 1 7 2 8 5 | 1 |
| 3 | 1 | swap $A[1], A[3]$ | 3 1 9 6 7 2 8 5 | 2 |
| 4 | 7 | none | 3 1 9 6 7 2 8 5 | 2 |
| 5 | 2 | swap $A[2], A[5]$ | 3 1 2 6 7 9 8 5 | 3 |
| 6 | 8 | none | 3 1 2 6 7 9 8 5 | 3 |
| L7 | | swap $A[3], A[7]$ | 3 1 2 **5** 7 9 8 6 | 3 |

The result is $p = 3$. The items 3, 1 and 2 are left of the pivot, and 7, 9, 8 and 6 are right of it. The scan made 7 comparisons and 3 swaps in the loop. The item 6 moved twice: first from index 0 to index 3, then to index 7.

## Correctness

The invariant of the loop of line L3, before the step for $j$, is:

> $lo \le i \le j$, each item of $A[lo \ldots i-1]$ is at most $x$, each item of $A[i \ldots j-1]$ is larger than $x$, and $A[hi-1] = x$.

It is true at the start, when both parts are empty. If $A[j] > x$, the large part grows by $A[j]$. If $A[j] \le x$, line L5 moves the first large item to index $j$ and the item $A[j]$ to index $i$, so both parts keep their property. The loop stops at $j = hi - 1$. Then line L7 puts $x$ at index $i$ and moves the first large item, if there is one, to the end. Each change is a swap inside the range, so the range keeps its items. The full proof is below.

## Complexity

The loop runs $m - 1$ times, and each step makes one comparison and at most one swap. So the time is $\Theta(m)$ in every case, with exactly $m - 1$ comparisons. This is optimal: each item other than the pivot must be compared with the pivot, or the algorithm cannot know its side.

The number of swaps in the loop is the number of items other than the pivot that are at most $x$. It is $0$ when $x$ is the smallest item and $m - 1$ when $x$ is the largest. If the pivot has a uniform rank in a range of $m$ distinct items, the mean is $(m-1)/2$. The Hoare partition makes about $m/6$ swaps on average, so Lomuto does about three times more. Many of the Lomuto swaps move a large item that is already on the correct side, as the item 6 in the example shows.

The extra space is $\Theta(1)$: the pivot and two indices.

| claim | model and case | bound |
|---|---|---|
| time | comparison model, worst, average and best | $\Theta(m)$, with $m - 1$ comparisons |
| extra space | | $\Theta(1)$ |

## Properties

- **Not stable.** Line L7 swaps the pivot with the first large item, and this item jumps over the other large items. On $(2, a), (2, b), (1, c)$ with pivot $(1, c)$, the output is $(1, c), (2, b), (2, a)$, so the two items with key 2 change their order.
- **In place.** It uses $O(1)$ extra space.
- **One direction.** It reads the range once from left to right. So it also works on a singly linked list.
- **Equal items go left.** Each item equal to $x$ goes to the left part. So on a range of equal items, $p = hi - 1$, and quicksort with this partition takes $\Theta(n^2)$ time.

## Variants and improvements

- **The pivot at the left end.** Bentley's version keeps the pivot at $A[lo]$, scans from $lo + 1$, and swaps it to its place at the end. It tests $A[j] < x$, so the equal items go right.
- **A random pivot.** Swap a random item of the range to the end before the call. This gives [randomized quicksort](/randomized-quicksort/).
- **[Hoare partition](/hoare-partition/).** Scan from both ends and swap only pairs that are both on the wrong side. It makes fewer swaps and splits a range of equal items near the middle, but it does not put the pivot at a known index.
- **Three-way partition.** Keep a third part for the items equal to $x$. This is the [Dutch national flag](/dutch-national-flag/) partition of [three-way quicksort](/three-way-quicksort/).

## When to use it

Use the Lomuto partition when the code must be short and easy to prove, for teaching, and in [quickselect](/quickselect/) and quicksort on data with few equal items. It also fits a linked list, because it only reads forward. For a library sort on arrays, the Hoare partition or a three-way partition is faster, because it does fewer swaps and handles equal items well.

## Pitfalls

- **An empty range.** The algorithm reads $A[hi - 1]$, so it needs $hi - lo \ge 1$. Quicksort calls it only on ranges of two or more items.
- **The loop bound.** The loop must stop at $hi - 2$. If it runs to $hi - 1$, it compares the pivot with itself and swaps it into the left part. Then line L7 swaps a large item into index $i$, and the returned index does not hold the pivot.
- **Recursion that includes the pivot.** Quicksort must recurse on $[lo, p)$ and $[p + 1, hi)$. A call on $[lo, p + 1)$ repeats the same range forever when the pivot is the largest item, because then $p = hi - 1$.
- **Equal keys.** An input with many copies of one key makes each partition one-sided. Test quicksort on an array of equal items.

## Implementations

## History

Bentley's Programming Pearls credits this one-way partition to Nico Lomuto, and CLRS uses it as the main partition of its chapter on quicksort. Hoare's original quicksort of 1961 and 1962 uses the two-way scan that is now called the [Hoare partition](/hoare-partition/).

## References
