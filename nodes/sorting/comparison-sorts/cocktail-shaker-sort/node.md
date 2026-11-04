---
tag: 9RXP2E
kind: algorithm
slug: cocktail-shaker-sort
name: Cocktail shaker sort
aliases:
- bidirectional bubble sort
- shaker sort
area: sorting/comparison-sorts
level: intro
summary: Bubble sort that alternates passes in both directions.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items, d: the number of inversions in the input}
  time: {worst: Θ(n²), average: Θ(n²), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: true, in_place: true, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [bubble-sort, loop-invariant, inversion]
see_also: [insertion-sort, comb-sort, odd-even-transposition-sort, gnome-sort, shell-sort, comparison-cost-model]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (the discussion after Algorithm B of the cocktail-shaker sort, which alternates the direction of the passes)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2, Sorting by exchanging (the analysis of Algorithm B by inversion tables, which the bounds on rounds here follow)
---

Cocktail shaker sort is [bubble sort](/bubble-sort/) with passes in both directions. A pass to the right carries the largest remaining item to the right end, and the next pass to the left carries the smallest remaining item to the left end. Each pass stops at the place of the last exchange of the pass before. It solves the [sorting problem](/sorting-problem/) in $\Theta(n^2)$ time in the worst and average case and in $\Theta(n)$ time on sorted input. It is stable and in place. It fixes the slow case of bubble sort, a small item near the end, but on random input it saves only about a third of the comparisons, and [insertion sort](/insertion-sort/) is still better.

## In plain words

Bubble sort walks only to the right. A large item moves right very fast, because the walk carries it. A small item moves left by only one place in each walk, so a small item at the far right end makes bubble sort slow.

Cocktail shaker sort walks right, then left, then right again, like a hand that shakes a cocktail. The walk to the right puts the largest item at the right end. The walk back to the left carries the smallest item to the left end. So both ends fill up with finished items, and the unsorted part in the middle shrinks from both sides. When a walk makes no swap, the middle part is in order and you stop.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm changes the array in place.

## The algorithm

The unsorted part is $A[lo \ldots hi]$. Each pass records the place of its last exchange, and the next pass stops there, as in Knuth's Algorithm B for bubble sort.

```pseudo id=main
COCKTAIL-SHAKER-SORT(A)
L1  lo ← 0, hi ← n − 1                   ▷ A[lo..hi] is the unsorted part
L2  while lo < hi do
L3      last ← lo
L4      for j ← lo to hi − 1 do                ▷ the pass to the right
L5          if A[j] > A[j + 1] then
L6              exchange A[j] and A[j + 1], last ← j
L7      hi ← last
L8      last ← hi
L9      for j ← hi − 1 downto lo do            ▷ the pass to the left
L10         if A[j] > A[j + 1] then
L11             exchange A[j] and A[j + 1], last ← j + 1
L12     lo ← last
```

Lines L3 to L7 are a pass to the right. If its last exchange was at the pair $(j, j+1)$, then the items from $j + 1$ to $hi$ are in order and are the largest items of the part, so line L7 moves $hi$ down to $j$. Lines L8 to L12 are a pass to the left. If its last exchange was at $(j, j+1)$, then the items from $lo$ to $j$ are the smallest items of the part, in order, so line L12 moves $lo$ up to $j + 1$. A pass with no exchange sets $hi = lo$ or $lo = hi$, which ends the loop. A *round* is one pass in each direction.

## Example

Sort $A = [5, 1, 4, 2, 8, 0, 3]$, the input of the example on the [bubble sort](/bubble-sort/) page. It has 12 [inversions](/inversion/).

| pass | the array after the pass | exchanges | comparisons | new $lo$, $hi$ |
|---|---|---|---|---|
| start | 5 1 4 2 8 0 3 | | | 0, 6 |
| 1, right | 1 4 2 5 0 3 8 | 5 | 6 | 0, 5 |
| 1, left | 0 1 4 2 5 3 8 | 4 | 5 | 1, 5 |
| 2, right | 0 1 2 4 3 5 8 | 2 | 4 | 1, 4 |
| 2, left | 0 1 2 3 4 5 8 | 1 | 3 | 4, 4 |

In the first pass to the left, the item 0 moves from index 4 to index 0 in one pass. Bubble sort needs 5 passes to move it there. The run takes 2 rounds, 18 comparisons and 12 exchanges. Bubble sort takes 19 comparisons and the same 12 exchanges.

The gain is larger on $[2, 3, 4, 5, 6, 1]$. The first pass to the right moves only 6 one place, and the first pass to the left carries 1 to the front. The second pass to the right makes no exchange. The run makes 12 comparisons in 2 rounds, while bubble sort makes 15 comparisons in 5 passes.

## Correctness

The loop of line L2 keeps this [loop invariant](/loop-invariant/):

> At the test of line L2, $A[0 \ldots lo-1]$ and $A[hi+1 \ldots n-1]$ are sorted, and each item of $A[0 \ldots lo-1]$ is at most each item of $A[lo \ldots hi]$, which is at most each item of $A[hi+1 \ldots n-1]$.

A pass to the right carries the maximum of $A[lo \ldots hi]$ to the right, as in bubble sort, and leaves $A[last+1 \ldots hi]$ sorted and holding the largest items of the part. A pass to the left does the same for the smallest items at the left end. When the loop stops, $lo \ge hi$, so the unsorted part has at most one item, and the whole array is sorted. Each round lowers $hi - lo$ by at least 1, so the loop stops. Each change is an exchange, so the output is a permutation of the input. The full proof is below.

## Complexity

**Exchanges.** Each exchange is of two adjacent items that are out of order, so it removes exactly one inversion. So cocktail shaker sort makes exactly $d$ exchanges, where $d$ is the number of inversions of the input, the same as bubble sort and insertion sort. This is $n(n-1)/2$ in the worst case and $n(n-1)/4$ on average over random permutations of distinct keys.

**Rounds.** For an item $x$, let $b(x)$ be the number of larger items to its left, and $s(x)$ the number of smaller items to its right. A pass to the right lowers each positive $b(x)$ by 1, and a pass to the left lowers each positive $s(x)$ by 1, by the argument of the bubble sort page. So the number of rounds is at most $\min(\max_x b(x), \max_x s(x)) + 1$. One small item at the end gives $\max_x s(x) = 1$, and the sort takes at most 2 rounds.

**Comparisons and time.**

- **Worst case.** A reverse sorted array makes each pass one shorter than the pass before, so the passes have lengths $n - 1, n - 2, \ldots, 1$. This is $n(n-1)/2$ comparisons and $n(n-1)/2$ exchanges, which is $\Theta(n^2)$ time.
- **Best case.** A sorted array takes one pass to the right with $n - 1$ comparisons and no exchange, so $\Theta(n)$ time.
- **Average case.** The $n(n-1)/4$ exchanges give $\Theta(n^2)$ time. In a measurement on 20 random permutations of 1000 distinct keys, the mean was 335,422 comparisons and 255 rounds, against 497,390 comparisons and 971 passes for bubble sort. So the passes in both directions save about a third of the comparisons, but none of the exchanges.
- **Space.** $\Theta(1)$ extra.

## Properties

- **Stable.** Lines L5 and L10 exchange only when $A[j] > A[j+1]$, so two equal items are never exchanged.
- **In place.** It uses a fixed number of variables.
- **Adaptive.** It is fast when every item is near its final place on one side: when all $b(x)$ are small or all $s(x)$ are small. It is still slow when there are many inversions, because it makes exactly $d$ exchanges.
- **Not online.** It needs the whole array before the first pass.

## Variants and improvements

- **Plain version.** Replace lines L3, L7, L8 and L12 by $hi \leftarrow hi - 1$ and $lo \leftarrow lo + 1$. It always makes about $n/2$ rounds and $n(n-1)/2$ comparisons.
- **[Comb sort](/comb-sort/).** Compare items a shrinking gap apart, so that small items near the end move left by large steps. This reduces the number of comparisons much more than the passes in two directions do.
- **[Odd-even transposition sort](/odd-even-transposition-sort/).** Compare disjoint adjacent pairs in parallel. It is the parallel form of the same exchanges.
- **[Insertion sort](/insertion-sort/) and [Shell sort](/shell-sort/).** Insertion sort makes the same $d$ moves with at most $d + n - 1$ comparisons. Shell sort makes insertion sort fast by moving items over long distances first.

## When to use it

Use it to teach how the direction of the passes affects the slow case of bubble sort. As a real sort, insertion sort is better: it makes the same number of moves, at most $d + n - 1$ comparisons, and needs no second direction. On a nearly sorted array with a few items far from their place on both sides, cocktail shaker sort can make fewer passes than bubble sort, but insertion sort is still at least as fast.

## Pitfalls

- **The wrong new bound after a pass to the left.** The last exchange at $(j, j+1)$ puts the final items at $lo \ldots j$, so the new $lo$ is $j + 1$, not $j$. With $lo \leftarrow j$ the sort is still correct but makes extra comparisons, and with $lo \leftarrow j + 2$ it can leave an item out of order.
- **The start value of $last$.** Line L3 sets $last \leftarrow lo$ and line L8 sets $last \leftarrow hi$. Then a pass with no exchange ends the loop. Other start values can make an extra round, or an endless loop.
- **Comparing with ≥.** The test $A[j] \ge A[j+1]$ makes the sort unstable, and on all-equal keys it makes $\Theta(n^2)$ exchanges.
- **Expecting a large gain.** The second direction does not reduce the number of exchanges, which is the number of inversions. On random input the time stays $\Theta(n^2)$.

## Implementations

## History

Knuth, in Section 5.2.2, describes the cocktail-shaker sort as a refinement of bubble sort that alternates the direction of the passes, and notes that it gives only a small gain over bubble sort, because the number of exchanges does not change.

## References
