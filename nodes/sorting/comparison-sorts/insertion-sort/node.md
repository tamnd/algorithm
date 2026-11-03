---
tag: 3NS7RT
kind: algorithm
slug: insertion-sort
name: Insertion sort
area: sorting/comparison-sorts
level: intro
summary: Sort an array one item at a time. Take the next item and move it left until the item before it is not larger.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items, d: the number of inversions in the input}
  time: {worst: Θ(n²), average: Θ(n²), best: Θ(n), total: Θ(n + d)}
  space: {extra: Θ(1)}
properties: {stable: true, in_place: true, adaptive: true, online: true, deterministic: true, comparison: true, recursive: false}
history:
  year: 1946
  people: [John Mauchly]
  note: Mauchly described insertion sort, with binary insertion, in the Moore School Lectures in 1946. Knuth gives this as the first published account of the method.
prereqs: [loop-invariant, asymptotic-notation]
see_also: [merge-sort, binary-search]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.1
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.1, Algorithm S
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 11, Sorting
---

Insertion sort sorts an array in place. It takes each item in turn and moves it left into the sorted part before it. It solves the [sorting problem](/sorting-problem/) in $\Theta(n^2)$ time in the worst case and in $\Theta(n)$ time on an array that is already sorted. It is stable and uses $\Theta(1)$ extra space. Because it is fast on small and nearly sorted arrays, many library sorts use it for short runs.

## In plain words

You hold some playing cards in your left hand, in order. You take one new card with your right hand. You move it from the right to the left past each card that is larger. Then you put it in the gap. Now the cards in your left hand are in order again, and they are one more. You do this for each new card.

Insertion sort does this on an array. The left part of the array is sorted. The algorithm takes the first item to the right of this part, and inserts it at the correct place in the left part.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm changes the array in place.

## The algorithm

```pseudo id=main
INSERTION-SORT(A)
L1  for i ← 1 to n − 1 do
L2      key ← A[i]
L3      j ← i − 1
L4      while j ≥ 0 and A[j] > key do     ▷ > and not ≥ keeps the sort stable
L5          A[j + 1] ← A[j]
L6          j ← j − 1
L7      A[j + 1] ← key
```

Line L2 takes the next item and keeps it in $key$. Lines L4 to L6 move each larger item of the sorted part one place to the right. This opens a gap. Line L7 puts $key$ in the gap.

## Example

Sort $A = [5, 2, 4, 6, 1, 3]$. The bar shows the end of the sorted part.

| i | key | the array after the step |
|---|---|---|
| start | | 5 \| 2 4 6 1 3 |
| 1 | 2 | 2 5 \| 4 6 1 3 |
| 2 | 4 | 2 4 5 \| 6 1 3 |
| 3 | 6 | 2 4 5 6 \| 1 3 |
| 4 | 1 | 1 2 4 5 6 \| 3 |
| 5 | 3 | 1 2 3 4 5 6 \| |

In step 4, the key 1 moves past four items. In step 3, the key 6 moves past no item.

## Correctness

The proof uses a [loop invariant](/loop-invariant/) for the loop of line L1:

> Before the step for $i$, the part $A[0 \ldots i-1]$ holds the items that were at the start in $A[0 \ldots i-1]$, in non-decreasing order.

At the start $i = 1$, and a part with one item is sorted. The inner loop moves the items of the sorted part that are larger than $key$ one place right, and line L7 puts $key$ after the items that are not larger. So after the step, $A[0 \ldots i]$ is sorted. When the loop stops, $i = n$, and the full array is sorted. The full proof is below.

## Complexity

The inner loop runs once for each pair of indices $j < i$ with $A[j] > A[i]$. Such a pair is an *inversion*. Let $d$ be the number of inversions of the input. Then the time is $\Theta(n + d)$.

- The worst case is an array in decreasing order. It has $d = n(n-1)/2$ inversions, so the time is $\Theta(n^2)$. The algorithm does $n(n-1)/2$ comparisons and $n(n-1)/2$ moves.
- The best case is an array that is already sorted. It has $d = 0$, so the time is $\Theta(n)$, with $n - 1$ comparisons.
- On a random permutation, the expected number of inversions is $n(n-1)/4$, so the average time is $\Theta(n^2)$.
- The extra space is $\Theta(1)$: the key and two indices.

## Properties

- **Stable.** Line L4 stops at an item equal to $key$, so equal items keep their order.
- **In place.** The extra space is a fixed number of variables.
- **Adaptive.** An input with few inversions sorts fast.
- **Online.** The algorithm can sort the items while they arrive, because each step needs only the items before it.

## Variants and improvements

- **Binary insertion sort.** Use [binary search](/binary-search/) to find the place of $key$. This makes the number of comparisons $O(n \log n)$, but the number of moves stays $\Theta(n^2)$ in the worst case.
- **Shell sort.** Do insertion sort on items that are far apart first, with a decreasing sequence of gaps. Good gap sequences make the time much less than $\Theta(n^2)$.
- **A sentinel.** Put the smallest item at $A[0]$ first. Then the test $j \ge 0$ in line L4 is not necessary.

## When to use it

Use insertion sort for small arrays, of about 10 to 30 items. For such sizes it is often faster than [merge sort](/merge-sort/) and quicksort, because its loop is simple. Many library sorts, such as introsort and Timsort, switch to insertion sort for small parts. Also use it when the input is almost sorted.

Do not use it for large arrays in random order. The time grows as $n^2$.

## Pitfalls

- **Comparing with ≥.** The test $A[j] \ge key$ in line L4 also gives a sorted array, but the sort is not stable.
- **Swapping instead of shifting.** A swap in each step of the inner loop does three writes. A shift does one.
- **The index $j$ becomes $-1$.** In a language with unsigned indices, $j - 1$ can wrap around. Test $j > 0$ and use $A[j-1]$, or use a signed type.

## Implementations

## History

Insertion sort is the method that a person uses to sort a hand of playing cards, so it is older than computers. John Mauchly described it, together with binary insertion, in the Moore School Lectures in 1946. Knuth gives this as its first published account. Donald Shell published his faster variant with decreasing gaps in 1959.

## References
