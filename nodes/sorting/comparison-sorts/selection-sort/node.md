---
tag: 6ADSAW
kind: algorithm
slug: selection-sort
name: Selection sort
aliases: [straight selection sort]
area: sorting/comparison-sorts
level: intro
summary: Sort by repeatedly selecting the smallest remaining item and swapping it into place.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n²), average: Θ(n²), best: Θ(n²)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [loop-invariant, asymptotic-notation]
see_also: [insertion-sort, heapsort, tournament-sort, cycle-sort, pancake-sort, merge-sort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Exercise 2.2-2 (selection sort, its loop invariant and its running time)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3, Sorting by selection (Algorithm S, straight selection sort, and the analysis of the number of changes of the maximum)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.1, Elementary sorts (selection sort, Proposition A)
---

Selection sort sorts an array in place: it finds the smallest item of the part that is not yet sorted and swaps it to the front of that part. It solves the [sorting problem](/sorting-problem/) with exactly $n(n-1)/2$ comparisons on each input of $n$ items, so its time is $\Theta(n^2)$ in every case. It does at most $n - 1$ swaps, fewer than [insertion sort](/insertion-sort/) on most inputs, and it uses $\Theta(1)$ extra space. It is not stable. With a [heap](/binary-heap/) to find the minimum, the same idea becomes [heapsort](/heapsort/).

## In plain words

You have a row of cards in random order. You look at all the cards, find the smallest one, and swap it with the first card. Now the first card is in its final place. You then look at the rest of the row, find the smallest of these, and swap it with the second card. You go on in this way. Each round fixes one more card at the left end.

The method does the same amount of looking on every input. Even a row that is already in order takes all the rounds, because the method cannot know that a card is the smallest without looking at all the others. But it moves each card at most a few times, so it suits data that is costly to move.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm changes the array in place.

## The algorithm

```pseudo id=main
SELECTION-SORT(A)                          ▷ n is the length of A
L1  for i ← 0 to n − 2 do
L2      m ← i                              ▷ m is the index of the least item seen
L3      for j ← i + 1 to n − 1 do
L4          if A[j] < A[m] then
L5              m ← j
L6      swap A[i] and A[m]
```

Lines L2 to L5 scan the part $A[i \ldots n-1]$ and keep in $m$ the index of its first least item. Line L6 swaps that item into index $i$. After the step for $i$, the part $A[0 \ldots i]$ holds the $i + 1$ smallest items in sorted order, and they never move again. The loop stops at $i = n - 2$, because one item that is left is the largest and is already in place.

## Example

Sort $A = [29, 10, 14, 37, 13, 5, 22]$. The bar shows the end of the sorted part.

| $i$ | least item of $A[i \ldots 6]$ | the array after the swap |
|---|---|---|
| start | | 29 10 14 37 13 5 22 |
| 0 | 5, at index 5 | 5 \| 10 14 37 13 29 22 |
| 1 | 10, at index 1 | 5 10 \| 14 37 13 29 22 |
| 2 | 13, at index 4 | 5 10 13 \| 37 14 29 22 |
| 3 | 14, at index 4 | 5 10 13 14 \| 37 29 22 |
| 4 | 22, at index 6 | 5 10 13 14 22 \| 29 37 |
| 5 | 29, at index 5 | 5 10 13 14 22 29 \| 37 |

The run makes $6 + 5 + 4 + 3 + 2 + 1 = 21$ comparisons. Of the six swaps, two (for $i = 1$ and $i = 5$) swap an item with itself, so four swaps move items. Line L5 runs 6 times in total.

## Correctness

The proof uses a [loop invariant](/loop-invariant/) of the loop of line L1:

> Before the step for $i$, the array is a permutation of the input, $A[0 \ldots i-1]$ is sorted, and each item of $A[0 \ldots i-1]$ is at most each item of $A[i \ldots n-1]$.

At the start $i = 0$ and the sorted part is empty. The scan of lines L3 to L5 has its own invariant: $A[m]$ is a least item of $A[i \ldots j-1]$. So at the end of the scan, $A[m]$ is a least item of $A[i \ldots n-1]$. Line L6 puts it at index $i$. It is at least each item before it and at most each item after it, so the invariant holds for $i + 1$. When the loop stops, $i = n - 1$ (or $n \le 1$), the part $A[0 \ldots n-2]$ is sorted, and the last item is at least each item before it. The full proof is below.

## Complexity

**Comparisons.** For each $i$ from $0$ to $n - 2$, the scan makes $n - 1 - i$ comparisons. So on each input of $n \ge 1$ items the number of comparisons is

$$\sum_{i=0}^{n-2} (n - 1 - i) = \sum_{k=1}^{n-1} k = \frac{n(n-1)}{2}.$$

This count does not depend on the input. Each comparison comes with $O(1)$ other work, and each step of the outer loop does $O(1)$ work besides the scan. So the time is $\Theta(n^2)$ in the worst, the average and the best case. For $n = 7$ the count is 21, and for $n = 1000$ it is $499{,}500$.

**Swaps.** Line L6 runs $n - 1$ times, so the algorithm does $n - 1$ swaps, and at most $3(n-1)$ writes of items. A swap with $m = i$ moves nothing, and a program can skip it. Each swap that moves items puts one item into its final place.

**Changes of the minimum.** Line L5 runs a number of times that depends on the input. It is 0 on a sorted input. On a uniformly random permutation of distinct keys, its mean is $(n+1)H_n - 2n$, where $H_n$ is the $n$-th [harmonic number](/harmonic-series/). This is about $n \ln n$, so it is a small part of the $n^2/2$ comparisons. For $n = 4$ the mean is $29/12$. Knuth (Section 5.2.3) derives this mean.

**Space.** The algorithm keeps $i$, $j$ and $m$, and one item during a swap. So the extra space is $\Theta(1)$.

| claim | model and case | bound |
|---|---|---|
| time | comparison model, worst, average and best | $\Theta(n^2)$, with $n(n-1)/2$ comparisons |
| swaps | each input | $n - 1$ |
| extra space | | $\Theta(1)$ |

## Properties

- **Not stable.** The swap of line L6 can move an item past an equal item. On $(2, a), (2, b), (1, c)$, the first swap exchanges $(2, a)$ and $(1, c)$, and the output is $(1, c), (2, b), (2, a)$.
- **In place.** The extra space is a fixed number of variables.
- **Not adaptive.** The number of comparisons is the same on each input of $n$ items.
- **Few writes.** Each swap puts one item into its final place, so there are at most $n - 1$ swaps. [Cycle sort](/cycle-sort/) writes even fewer: each item at most once.
- **Not online.** The first step needs all items, because the least item can be the last one.

## Variants and improvements

- **[Heapsort](/heapsort/).** Keep the unsorted part as a [binary heap](/binary-heap/). Then each selection takes $O(\log n)$ time, and the sort takes $O(n \log n)$ time, still in place.
- **[Tournament sort](/tournament-sort/).** Find each minimum in a [tournament tree](/tournament-tree/), so that the comparisons of one round are reused in the next. It makes about $n \lg n$ comparisons but needs $\Theta(n)$ extra space.
- **Stable selection sort.** Instead of a swap, remove the least item and shift the items $A[i \ldots m-1]$ one place right. The sort is then stable, but it does $\Theta(n^2)$ writes in the worst case. On a linked list the move is $O(1)$, and the stable form costs nothing extra.
- **Double-ended selection.** Find the least and the largest item in one scan, and place both. With the items compared in pairs, a scan of $k$ items takes about $3k/2$ comparisons, so the total falls to about $3n^2/8$. Take care when the largest item is at index $i$: the first swap moves it to index $m$.
- **[Pancake sort](/pancake-sort/).** Select the largest item, and move it to the end with two reversals of a prefix instead of a swap.

## When to use it

Use selection sort for very small arrays, or when a write costs much more than a read, for example on flash memory or with large records that are not moved by pointer. Its time does not depend on the order of the input, which is sometimes useful.

For other cases, [insertion sort](/insertion-sort/) is better among the quadratic sorts: it makes about half as many comparisons on average, and it takes linear time on a sorted input. For more than a few dozen items, use an $O(n \log n)$ sort such as [merge sort](/merge-sort/) or [heapsort](/heapsort/).

## Pitfalls

- **Swapping during the scan.** If line L5 swaps $A[i]$ and $A[j]$ at once instead of saving $j$, the result is still sorted, but the sort can do $\Theta(n^2)$ swaps, and the main advantage of the method is lost. On a reversed input of 6 items, this version does 15 swaps against 3 swaps that move items.
- **Comparing with ≤.** With $A[j] \le A[m]$ at line L4, the scan finds the last least item instead of the first. The sort stays correct, but equal items now come out in a different order: on $(2, a), (1, b), (1, c)$ the output is $(1, c), (1, b), (2, a)$. Neither test makes the sort stable.
- **The double-ended variant.** When the largest item is at index $i$, the first swap moves it. Update its index before the second swap, or the sort is wrong. Test it on the input $[3, 1, 2]$.
- **An unsigned loop bound.** In a language with unsigned indices, $n - 2$ wraps around for $n = 0$. Test the empty array.

## Implementations

## History

Selection sort is one of the methods that people use to sort by hand. Knuth gives it as Algorithm S of Section 5.2.3, with the analysis of the number of changes of the maximum. In the same section he shows how tree selection, the idea of [tournament sort](/tournament-sort/), and then heapsort grew from the wish to keep the results of earlier comparisons.

## References
