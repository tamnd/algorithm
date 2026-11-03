---
tag: 4MRG7S
kind: algorithm
slug: merge-sort
name: Merge sort
aliases: [mergesort]
area: sorting/comparison-sorts
level: intro
summary: Sort an array by divide and conquer. Sort each half, then merge the two sorted halves into one sorted array.
solves: [sorting-problem]
model: comparison-model
prereqs: [insertion-sort, loop-invariant, asymptotic-notation]
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
history:
  year: 1945
  people: [John von Neumann]
  note: Von Neumann wrote a merge sort program for the EDVAC in 1945.
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.3
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.4
see_also: [insertion-sort, binary-search]
---

## In plain words

Two people each have a sorted pile of cards, with the smallest card on top. To make one sorted pile, you look at the two top cards. You take the smaller one and put it face down on a new pile. You do this again until both piles are empty. This step is a *merge*. It looks at each card one time.

Merge sort uses the merge to sort. It cuts the array into two halves. It sorts each half with the same method. Then it merges the two sorted halves. An array with one item is already sorted, so the method stops there.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/).

## The algorithm

The call MERGE-SORT$(A, 0, n)$ sorts the full array. The range $[lo, hi)$ is half-open: it holds $A[lo \ldots hi-1]$.

```pseudo id=main
MERGE-SORT(A, lo, hi)                      ▷ sort A[lo .. hi − 1]
L1  if hi − lo ≤ 1 then return
L2  mid ← lo + ⌊(hi − lo) / 2⌋
L3  MERGE-SORT(A, lo, mid)
L4  MERGE-SORT(A, mid, hi)
L5  MERGE(A, lo, mid, hi)

MERGE(A, lo, mid, hi)                      ▷ A[lo .. mid − 1] and A[mid .. hi − 1] are sorted
L6  B ← a copy of A[lo .. mid − 1]
L7  i ← 0, j ← mid, k ← lo
L8  while i < |B| and j < hi do
L9      if B[i] ≤ A[j] then A[k] ← B[i], i ← i + 1    ▷ ≤ keeps the sort stable
L10     else A[k] ← A[j], j ← j + 1
L11     k ← k + 1
L12 while i < |B| do
L13     A[k] ← B[i], i ← i + 1, k ← k + 1
```

MERGE copies only the left half to a buffer $B$. Then it fills $A$ from the left, with the smaller of $B[i]$ and $A[j]$ at each step. The write position $k$ never passes the read position $j$, so no item of the right half is lost. When $B$ is empty, the rest of the right half is already in place. So the loop of line L12 only copies the rest of $B$.

## Example

Sort $A = [38, 27, 43, 3, 9, 82, 10]$.

| level | the parts |
|---|---|
| split | [38 27 43] [3 9 82 10] |
| split | [38] [27 43] [3 9] [82 10] |
| split | [38] [27] [43] [3] [9] [82] [10] |
| merge | [38] [27 43] [3 9] [10 82] |
| merge | [27 38 43] [3 9 10 82] |
| merge | [3 9 10 27 38 43 82] |

In the last merge, $B = [27, 38, 43]$ and the right half is $[3, 9, 10, 82]$. The merge takes 3, 9 and 10 from the right half, then 27, 38 and 43 from $B$. The item 82 is already in place at the end.

## Correctness

MERGE is correct by a [loop invariant](/loop-invariant/) of line L8: $A[lo \ldots k-1]$ holds the $k - lo$ smallest items of the two halves, in sorted order, and $B[i]$ and $A[j]$ are the smallest items that are not yet placed. MERGE-SORT is then correct by induction on the length $hi - lo$. A range of length 0 or 1 is sorted. For a longer range, both calls sort a shorter range, and MERGE makes one sorted range of the two. The full proof is below.

## Complexity

Let $T(n)$ be the time on $n$ items. The two calls take $T(\lceil n/2 \rceil)$ and $T(\lfloor n/2 \rfloor)$, and MERGE takes $\Theta(n)$. So

$$T(n) = T(\lceil n/2 \rceil) + T(\lfloor n/2 \rfloor) + \Theta(n), \qquad T(1) = \Theta(1).$$

The solution is $T(n) = \Theta(n \log n)$. The recursion has $\lceil \lg n \rceil$ levels, and the merges of one level take $\Theta(n)$ time in total.

- The number of comparisons is at most $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$. This is at most $n \lg n$.
- The time is $\Theta(n \log n)$ in the best, the average and the worst case.
- The extra space is $\Theta(n)$ for the buffer, and $\Theta(\log n)$ for the stack.

In the [comparison model](/comparison-model/), each sort needs $\lg(n!) = n \lg n - \Theta(n)$ comparisons in the worst case. So merge sort is optimal in this model, up to a lower-order term.

## Properties

- **Stable.** Line L9 takes the item from the left half when the two items are equal.
- **Not in place.** The buffer $B$ has up to $\lceil n/2 \rceil$ items. In-place merges exist, but they are complex and slow.
- **Not adaptive.** This version does the same work on a sorted input. The natural variant below is adaptive.
- **Sequential access.** MERGE reads and writes the items in order. So merge sort works well on linked lists, on tapes and on files that do not fit in memory.

## Variants and improvements

- **Bottom-up merge sort.** Merge parts of size 1, then 2, then 4, and so on. This needs no recursion.
- **A cut-off to insertion sort.** Sort the small parts, of about 16 items, with [insertion sort](/insertion-sort/). This makes the program faster.
- **Skip a sorted merge.** If $A[mid - 1] \le A[mid]$, the two halves are already in order, and MERGE is not necessary. Then a sorted input takes $\Theta(n)$ time.
- **Natural merge sort and Timsort.** Find the sorted runs that the input already has, and merge them. Timsort is the sort of Python and of Java for objects.
- **External merge sort.** Sort parts that fit in memory, write them to disk, then merge many parts at a time.
- **Parallel merge sort.** Run the two calls at the same time. With a parallel merge, the span is $O(\log^3 n)$ or less.

## When to use it

Use merge sort when you need a stable sort with a guaranteed $O(n \log n)$ time. Use it to sort a linked list, because the merge needs no random access and no buffer there. Use it for data on disk. If you need a sort in place and stability is not necessary, heapsort or quicksort uses less memory.

## Pitfalls

- **Comparing with <.** The test $B[i] < A[j]$ in line L9 also sorts, but the sort is not stable.
- **A buffer in each call.** A new buffer in each call of MERGE costs time. Allocate one buffer of $\lceil n/2 \rceil$ items, and pass it down.
- **Overflow of the midpoint.** Use $lo + \lfloor (hi - lo)/2 \rfloor$, not $\lfloor (lo + hi)/2 \rfloor$.

## Implementations

## History

John von Neumann wrote a merge sort program for the EDVAC computer in 1945. Knuth gives this as one of the first programs written for a stored-program computer. Goldstine and von Neumann described the method in a report in 1948.

## References
