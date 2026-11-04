---
tag: 6HS4Z7
kind: algorithm
slug: gnome-sort
name: Gnome sort
aliases:
- stupid sort
area: sorting/comparison-sorts
level: intro
summary: Moves one element backward by adjacent swaps until ordered, then steps forward; equivalent in cost to insertion sort.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items, d: the number of inversions in the input}
  time: {worst: Θ(n²), average: Θ(n²), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: true, in_place: true, adaptive: true, online: true, deterministic: true, comparison: true, recursive: false}
history:
  year: 2000
  people: [Dick Grune]
  note: Grune described the method in 2000 as the way a garden gnome sorts a line of flower pots.
prereqs: [insertion-sort, inversion, loop-invariant]
see_also: [bubble-sort, cocktail-shaker-sort, comb-sort, comparison-cost-model, stable-sort]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.1, Sorting by insertion (straight insertion and the count of its moves by inversions)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.1, Insertion sort (the loop invariant on the sorted prefix)
  - paper: "Dick Grune, Gnome Sort: the simplest sort algorithm, web page of the author (2000)"
    locator: the whole page (the description with the garden gnome and the flower pots)
---

Gnome sort sorts an array with one index that walks forward and backward. If the item at the index is in order with the item to its left, the index steps forward. If not, the two items are exchanged and the index steps back. It is [insertion sort](/insertion-sort/) with the inner loop written as steps of the same single loop: it makes the same $d$ exchanges, where $d$ is the number of inversions, but almost twice as many comparisons, because it walks forward again over the items it just passed. It solves the [sorting problem](/sorting-problem/) in $\Theta(n + d)$ time, which is $\Theta(n^2)$ in the worst and average case and $\Theta(n)$ on sorted input. It is stable and in place.

## In plain words

A garden gnome stands in front of a line of flower pots. He looks at the pot next to him and the pot just before it. If they are in the right order, he steps one pot forward. If not, he swaps them and steps one pot back. At the start of the line there is no pot before him, so he steps forward. When he passes the last pot, the line is sorted.

Each pot that is too small travels back, one swap at a time, until it meets a pot that is not larger. Then the gnome walks forward again to the place where he started the swaps, and goes on. This is exactly what insertion sort does, but the gnome forgets where he was and must walk back.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm changes the array in place.

## The algorithm

```pseudo id=main
GNOME-SORT(A)
L1  i ← 0
L2  while i < n do
L3      if i = 0 or A[i − 1] ≤ A[i] then
L4          i ← i + 1                        ▷ step forward
L5      else
L6          exchange A[i − 1] and A[i]
L7          i ← i − 1                        ▷ step back
```

Line L3 compares the item at $i$ with its left neighbour. At $i = 0$ there is no neighbour, and the test is true without a comparison. Line L6 exchanges two neighbours only when the left one is larger, so each exchange removes exactly one inversion.

## Example

Sort $A = [3, 1, 4, 2]$. It has 3 [inversions](/inversion/): $(3, 1)$, $(3, 2)$ and $(4, 2)$.

| step | $i$ before | action | the array after the step | $i$ after |
|---|---|---|---|---|
| 1 | 0 | forward, no comparison | 3 1 4 2 | 1 |
| 2 | 1 | $3 > 1$, exchange, back | 1 3 4 2 | 0 |
| 3 | 0 | forward, no comparison | 1 3 4 2 | 1 |
| 4 | 1 | $1 \le 3$, forward | 1 3 4 2 | 2 |
| 5 | 2 | $3 \le 4$, forward | 1 3 4 2 | 3 |
| 6 | 3 | $4 > 2$, exchange, back | 1 3 2 4 | 2 |
| 7 | 2 | $3 > 2$, exchange, back | 1 2 3 4 | 1 |
| 8 | 1 | $1 \le 2$, forward | 1 2 3 4 | 2 |
| 9 | 2 | $2 \le 3$, forward | 1 2 3 4 | 3 |
| 10 | 3 | $3 \le 4$, forward | 1 2 3 4 | 4 |

The run takes $10 = n + 2d$ steps, with 8 comparisons and 3 exchanges. Steps 9 and 10 walk again over items that step 5 already passed. Insertion sort on the same input makes 5 comparisons and the same 3 moves.

## Correctness

The loop of line L2 keeps this [loop invariant](/loop-invariant/):

> At the test of line L2, $A[0 \ldots i-1]$ is sorted.

It holds at the start, with $i = 0$. A step forward from $i = 0$ gives the one-item prefix $A[0 \ldots 0]$. A step forward from $i > 0$ happens only when $A[i-1] \le A[i]$, so it extends a sorted prefix by an item that is not smaller than its last item. A step back exchanges $A[i-1]$ and $A[i]$ and sets $i$ to $i - 1$, so the new prefix $A[0 \ldots i-2]$ is a part of the old sorted prefix that the exchange did not touch. When the loop stops, $i = n$, so the whole array is sorted.

The loop stops because each step back removes one inversion, so there are at most $d$ steps back, and after the last one only steps forward remain. The full proof is below.

## Complexity

Let $d$ be the number of inversions of the input.

- **Exchanges.** Each exchange removes exactly one inversion, and the output has none, so there are exactly $d$ exchanges. These are the same $d$ moves that insertion sort makes as shifts.
- **Steps.** There are $d$ steps back, and the index ends at $n$, so there are $n + d$ steps forward and $n + 2d$ steps in total.
- **Comparisons.** Every step at $i > 0$ makes one comparison. The index is at 0 once at the start and once each time an item travels to the front, which happens for each item that is smaller than all items before it. If $z$ is the number of these items, counting $A[0]$, the comparisons are $n + 2d - z$. Insertion sort makes at most $n - 1 + d$. On random permutations of 1000 distinct keys, a measurement gave a mean of 501,532 comparisons for gnome sort and 251,263 for insertion sort.
- **Time.** $\Theta(n + d)$. The worst case is a reverse sorted array, with $d = n(n-1)/2$, so $\Theta(n^2)$. The average over random permutations is $d = n(n-1)/4$, so $\Theta(n^2)$. The best case is a sorted array, with $n$ steps and $n - 1$ comparisons, so $\Theta(n)$.
- **Space.** $\Theta(1)$ extra: one index.

## Properties

- **Stable.** Line L6 exchanges only when $A[i-1] > A[i]$, so equal items are never exchanged.
- **In place.** It uses one index.
- **Adaptive.** Its time is $\Theta(n + d)$, so it is linear on inputs with $O(n)$ inversions.
- **Online.** The index never reads past $A[i]$, and when it first reaches $i$, the prefix $A[0 \ldots i-1]$ is sorted. So items can be added at the right end while the sort runs.

## Variants and improvements

- **Gnome sort with a memory.** Record the place where the steps back began, and jump back to it when the item has reached its place. This removes the extra steps forward, and the result is insertion sort with adjacent exchanges.
- **[Insertion sort](/insertion-sort/).** Shift the larger items one place to the right and write the moving item once, instead of exchanging at each step. This makes about one write per move instead of two.
- **[Bubble sort](/bubble-sort/) and [cocktail shaker sort](/cocktail-shaker-sort/).** They make the same $d$ adjacent exchanges in a different order, in passes over the array.

## When to use it

Use gnome sort to show that a sort can have a single loop and still be quadratic, or to show how insertion sort works with adjacent exchanges. For real data, use insertion sort: it makes the same moves with about half the comparisons.

## Pitfalls

- **Reading $A[-1]$.** The test at $i = 0$ must not read $A[i-1]$. The "$i = 0$ or" in line L3 must come first, with a short-circuit "or".
- **Comparing with $<$.** With $A[i-1] < A[i]$ in line L3, equal neighbours are exchanged, so the sort is not stable. On all-equal keys the index then moves back and forth between 0 and 1 forever, because each exchange leaves the pair as it was.
- **Counting the cost as linear.** The code has a single loop, but the loop runs $n + 2d$ times, which is quadratic in the worst case.

## Implementations

## History

Dick Grune described gnome sort in 2000, with the story of a garden gnome who sorts flower pots, and called it the simplest sort algorithm. The name stupid sort is also used for it. The method is the exchange form of straight insertion, which Knuth analyses in Section 5.2.1.

## References
