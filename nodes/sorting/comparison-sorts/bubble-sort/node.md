---
tag: JS56R4
kind: algorithm
slug: bubble-sort
name: Bubble sort
aliases:
- sinking sort
- exchange sort
area: sorting/comparison-sorts
level: intro
summary: Repeatedly swaps adjacent out-of-order pairs, so large elements bubble to the end; quadratic and rarely preferred.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items, d: the number of inversions in the input}
  time: {worst: Θ(n²), average: Θ(n²), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: true, in_place: true, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [loop-invariant, inversion, asymptotic-notation]
see_also: [insertion-sort, cocktail-shaker-sort, comb-sort, odd-even-transposition-sort, gnome-sort, selection-sort, comparison-cost-model]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (Algorithm B, the bubble sort, and its analysis of passes, comparisons and exchanges by inversion tables)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 2, Problem 2-2, Correctness of bubblesort
  - paper: "Owen Astrachan, Bubble sort: an archaeological algorithmic analysis, SIGCSE Bulletin 35(1) (2003)"
    locator: pp. 1 to 5 (the history of the name and of the method)
---

Bubble sort sorts an array by passes over adjacent pairs: in each pass it compares each item with the next one and exchanges them when they are out of order. After the first pass the largest item is at the end, after the second pass the two largest items are at the end, and so on. It solves the [sorting problem](/sorting-problem/) in $\Theta(n^2)$ time in the worst and average case, and in $\Theta(n)$ time on a sorted array when it stops after a pass with no exchange. It is stable and in place, but it makes about twice as many comparisons as [insertion sort](/insertion-sort/) on average, so it is used mainly to teach.

## In plain words

Walk along the row of items from the left. At each step, look at two neighbours. If the left one is larger, swap them. The largest item you have met so far travels right with you, like a bubble that rises in water. When you reach the end, the largest item of all is at the last place.

Do the walk again, but stop before the part at the end that is already in order. Each walk puts one more large item at its place. When a walk makes no swap at all, every pair of neighbours is in order, so the whole row is sorted, and you can stop.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm changes the array in place.

## The algorithm

This is the version of Knuth's Algorithm B. Each pass stops at the place of the last exchange of the pass before, because everything after that place is already final.

```pseudo id=main
BUBBLE-SORT(A)
L1  bound ← n − 1                  ▷ the pairs (j, j + 1) with j < bound may be out of order
L2  while bound > 0 do
L3      last ← 0
L4      for j ← 0 to bound − 1 do
L5          if A[j] > A[j + 1] then      ▷ > and not ≥ keeps the sort stable
L6              exchange A[j] and A[j + 1]
L7              last ← j
L8      bound ← last
```

Lines L4 to L7 are one pass. The pass carries the largest item seen so far to the right: if $A[j] > A[j+1]$, the exchange moves the larger item to $j + 1$, and the next comparison uses it. Line L7 records where the last exchange was. If the last exchange of a pass was at $j$, no pair after $j$ was exchanged, so $A[j+1 \ldots n-1]$ is final, and line L8 lets the next pass stop before it. A pass with no exchange sets $bound$ to 0, which ends the loop.

The *plain* version replaces lines L3, L7 and L8 by $bound \leftarrow bound - 1$. It always makes $n - 1$ passes and $n(n-1)/2$ comparisons.

## Example

Sort $A = [5, 1, 4, 2, 8, 0, 3]$. The input has 12 [inversions](/inversion/).

| pass | the array after the pass | last exchange | comparisons |
|---|---|---|---|
| start | 5 1 4 2 8 0 3 | | |
| 1 | 1 4 2 5 0 3 8 | 5 | 6 |
| 2 | 1 2 4 0 3 5 8 | 4 | 5 |
| 3 | 1 2 0 3 4 5 8 | 3 | 4 |
| 4 | 1 0 2 3 4 5 8 | 1 | 3 |
| 5 | 0 1 2 3 4 5 8 | 0 | 1 |

In pass 1, the item 5 moves right until it meets 8, and then 8 moves to the end. Pass 4 ends with $last = 1$, so pass 5 compares only the pair at index 0. The run makes 19 comparisons and 12 exchanges. The plain version makes 21 comparisons and the same 12 exchanges. The item 0 had 5 larger items to its left, and it moves left by one place in each pass, so 5 passes are needed.

## Correctness

The loop of line L2 keeps this [loop invariant](/loop-invariant/):

> At the test of line L2, $A[bound+1 \ldots n-1]$ is sorted, and each of its items is at least each item of $A[0 \ldots bound]$.

A pass moves the maximum of $A[0 \ldots bound]$ to the right. After the pass, the part from $last + 1$ to $bound$ is sorted and holds the largest items of $A[0 \ldots bound]$, so the invariant holds for $bound = last$. When the loop stops, $bound = 0$, and the whole array is sorted. The loop stops because each pass makes $bound$ smaller by at least 1. The full proof is below.

## Complexity

**Exchanges.** An exchange of two adjacent items that are out of order removes exactly one inversion and creates none. The sorted array has no inversions. So bubble sort makes exactly $d$ exchanges, where $d$ is the number of inversions of the input. This is $n(n-1)/2$ for a reverse sorted array and $n(n-1)/4$ on average over random permutations of distinct keys.

**Passes.** For an item $x$, let $b(x)$ be the number of larger items to its left. In one pass, each item with $b(x) > 0$ moves left by exactly one place, because the item that the pass carries into the place left of $x$ is the largest item to the left of $x$, and it is larger than $x$. Items to the left of $x$ that are larger stay to its left, except this one. So each pass lowers each positive $b(x)$ by exactly 1. Let $b = \max_x b(x)$. Then the passes with an exchange are exactly $b$, and the algorithm makes $b$ or $b + 1$ passes in total (one more pass with no exchange may be needed to see that the array is sorted). Knuth, Section 5.2.2, counts the inversion tables with all entries at most $k$, which gives

$$\Pr[\text{at most } k \text{ passes}] = \frac{k!\, k^{n-k}}{n!}$$

for the version of Knuth's Algorithm B, and the average number of passes $n - \sqrt{\pi n / 2} + O(1)$. For $n = 1000$ this is about 960, so the early stop saves only a few passes on a random input.

**Comparisons and time.**

- **Worst case.** A reverse sorted array needs $n - 1$ passes of lengths $n - 1, n - 2, \ldots, 1$, so $n(n-1)/2$ comparisons and $n(n-1)/2$ exchanges, which is $\Theta(n^2)$ time.
- **Best case.** A sorted array takes one pass, with $n - 1$ comparisons and no exchange, so $\Theta(n)$ time.
- **Average case.** On a random permutation the number of comparisons is $\sim n^2/2$, and the number of exchanges is $n(n-1)/4$. For $n = 1000$ the mean over 50 random inputs was 496,054 comparisons and 249,477 exchanges, against $n(n-1)/2 = 499{,}500$ and $n(n-1)/4 = 249{,}750$.
- **Space.** $\Theta(1)$ extra.

## Properties

- **Stable.** Line L5 exchanges only when $A[j] > A[j+1]$, so two equal items are never exchanged, and an item never jumps over an equal item.
- **In place.** It uses a fixed number of variables.
- **Adaptive, but weakly.** It is fast when each item has few larger items to its left. A sorted array costs $n - 1$ comparisons. But one small item at the end, as in $[2, 3, \ldots, n, 1]$, needs $n - 1$ passes and $\Theta(n^2)$ comparisons, while insertion sort needs $\Theta(n)$ comparisons for it.
- **Oblivious (plain version).** The plain version makes the same comparisons on each input, so it can be written as a [sorting network](/sorting-network/) of $n(n-1)/2$ comparators.

## Variants and improvements

- **[Cocktail shaker sort](/cocktail-shaker-sort/).** Alternate passes to the right and to the left. A small item at the end then moves to the front in one backward pass.
- **[Comb sort](/comb-sort/).** First compare items a large gap apart, then shrink the gap to 1. This removes the small items near the end early, which are the slow case of bubble sort.
- **[Odd-even transposition sort](/odd-even-transposition-sort/).** Compare all pairs $(2i, 2i+1)$ at once, then all pairs $(2i+1, 2i+2)$. After $n$ rounds the array is sorted. This is a parallel form of bubble sort.
- **[Gnome sort](/gnome-sort/).** Move one item back with adjacent exchanges until it is in place. It makes the same exchanges as insertion sort.

## When to use it

There is almost no case where bubble sort is the best choice. [Insertion sort](/insertion-sort/) makes the same number of exchanges (as shifts), about half the comparisons on average, and handles the case of a small item at the end in linear time. Bubble sort is useful to teach adjacent exchanges, inversions and loop invariants, and to check in one pass with no exchange that an array is sorted.

## Pitfalls

- **Comparing with ≥.** The test $A[j] \ge A[j+1]$ in line L5 still sorts, but it exchanges equal items, so the sort is not stable, and on all-equal input it makes $n(n-1)/2$ exchanges.
- **An index out of range.** The inner loop must stop at $j = bound - 1$, because line L5 reads $A[j+1]$. A loop to $bound$ reads past the end in the first pass.
- **A flag without a bound.** A version with only a flag "an exchange happened" still stops early, but each pass then runs to the full length minus the pass number. Recording the last exchange, as in line L7, also skips the final part that a pass leaves sorted.
- **Expecting speed from the early stop.** The early stop helps only when the input is almost sorted in the sense above. On random input the number of passes is $n - O(\sqrt{n})$.

## Implementations

## History

The method was known in the 1950s as sorting by exchange. Astrachan (2003) traces it to papers on sorting for electronic computers from 1956, and finds the name "bubble sort" in print in 1962, in Iverson's book A Programming Language. Knuth, in Section 5.2.2, analyses its passes and comparisons in detail and concludes that it has little to recommend it as a practical sort.

## References
