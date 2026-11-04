---
tag: PWR6WE
kind: algorithm
slug: strand-sort
name: Strand sort
area: sorting/comparison-sorts
level: intro
summary: Repeatedly extracts an increasing subsequence (strand) and merges it into the output.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items, k: the number of strands}
  time: {worst: Θ(n²), average: O(n^(3/2)), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: true, in_place: false, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [merging-sorted-lists]
see_also: [natural-merge-sort, patience-sorting, merging-sorted-lists, longest-increasing-subsequence, linked-list, adaptive-sorting, selection-sort]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.10, Analysis of an algorithm (Algorithm M, the number of changes of the maximum, with mean H_n - 1)
  - paper: "David Aldous and Persi Diaconis, Longest increasing subsequences: from patience sorting to the Baik-Deift-Johansson theorem, Bulletin of the American Mathematical Society 36(4), 1999"
    locator: the introduction, on the length of the longest increasing subsequence of a random permutation, about 2 sqrt(n)
  - paper: "Paul E. Black (editor), Dictionary of Algorithms and Data Structures, National Institute of Standards and Technology"
    locator: the entry strand sort
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.2, Mergesort (the abstract in-place merge, and merging of sorted sequences)
---

Strand sort takes the items of a list in order and pulls out a *strand*: the first item, then each later item that is at least the last item taken. The strand is sorted, and it is [merged](/merging-sorted-lists/) into the result. The method repeats on the items that are left until none are left. It is stable, it takes $\Theta(n)$ time on a sorted input, and $\Theta(n^2)$ time in the worst case. The number of strands equals the length of the longest strictly decreasing subsequence of the input, about $2\sqrt{n}$ on a random input, so the average time is $O(n^{3/2})$. It suits [linked lists](/linked-list/), where taking an item out of the list costs $O(1)$.

## In plain words

You have a row of cards and want them in order. Take the first card. Walk along the row, and each time you see a card that is not smaller than the last card you took, take it as well. The cards that you took form a sorted pile, the strand.

Now merge the strand into the sorted result: walk through both, and always put down the smaller front card. Then do the same with the cards that are left in the row: take a new strand, and merge it in. When the row is empty, the result holds all the cards in order.

A row that is almost sorted gives a few long strands, so the method is fast. A row in reverse order gives one strand per card, so the method is slow.

## The problem

The input is a list $A$ of $n$ items with a total order. The output is a list of the same items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm below builds new lists; the implementation copies the result back into the input list.

## The algorithm

```pseudo id=main
STRAND-SORT(A)                              ▷ returns the items of A, sorted
L1  R ← empty list
L2  while A is not empty do
L3      S ← [A[0]];  U ← empty list         ▷ S is the strand, U the rest
L4      for each x in A[1 ..], in order do
L5          if x < last(S) then append x to U
L6          else append x to S
L7      R ← MERGE(R, S)                     ▷ on a tie, take the item of R
L8      A ← U
L9  return R
```

Lines L3 to L6 split $A$ into the strand $S$ and the rest $U$, in one scan. The strand is non-decreasing by its construction. Line L7 merges two sorted lists into one, with $|R| + |S| - 1$ comparisons at most; it takes the item of $R$ when the two front items are equal, which keeps the sort stable. Each round removes at least one item from $A$, the first one.

## Example

Sort $A = [5, 1, 4, 2, 8, 3, 7, 6]$.

| round | $A$ at the start | strand $S$ | $R$ after the merge |
|---|---|---|---|
| 1 | 5 1 4 2 8 3 7 6 | 5 8 | 5 8 |
| 2 | 1 4 2 3 7 6 | 1 4 7 | 1 4 5 7 8 |
| 3 | 2 3 6 | 2 3 6 | 1 2 3 4 5 6 7 8 |

The scans make $7 + 5 + 2 = 14$ comparisons. The merges make $0 + 4 + 6 = 10$, so the total is 24. There are 3 strands, and the longest decreasing subsequence of the input, for example $5, 4, 3$ or $8, 7, 6$, also has length 3.

## Correctness

Each strand is sorted, because line L6 appends $x$ only when $x$ is at least the last item of $S$. Each round moves each item of $A$ to exactly one of $S$ and $U$, and the merge of two sorted lists is a sorted list of their items. So the loop keeps this invariant: $R$ is sorted, and $R$ and $A$ together hold the items of the input. Each round makes $A$ shorter by at least one item, so the loop stops, and then $R$ holds all the items in sorted order.

For stability, take two equal items $y$ and $z$ with $y$ before $z$ in the input. Inside one scan they keep their order, and the merge keeps the order of $R$ before $S$ on ties. So it is enough that $z$ is never in an earlier strand than $y$. If $z$ joins a strand while $y$ is still in $A$, then the scan passed $y$ first and skipped it, so at that moment the last item of the strand was larger than $y$; the last item never gets smaller, so it is also larger than $z$, and $z$ is skipped too. The full proof is below.

## Complexity

**The number of strands.** Let $k$ be the number of strands. The items of a strictly decreasing subsequence of the input must be in different strands, because each strand is non-decreasing. Conversely, each item $x$ of strand $j > 1$ was skipped in round $j - 1$, so some earlier item of strand $j - 1$ is larger than $x$. Following these links back from an item of the last strand gives a strictly decreasing subsequence of length $k$. So $k$ is exactly the length of the longest strictly decreasing subsequence, the [longest increasing subsequence](/longest-increasing-subsequence/) of the reversed input. On a random permutation this is about $2\sqrt{n}$ (Aldous and Diaconis). The first strand of a permutation is the sequence of its left-to-right maxima, with mean length $H_n$ ([harmonic number](/harmonic-series/)), the quantity of Knuth's Section 1.2.10.

**Comparisons.** Round $j$ scans the $n_j$ items that are left, with $n_j - 1$ comparisons, and the merge makes fewer than $n$ comparisons. So the total is less than $2nk$, and the time is $O(nk)$.

| input | strands $k$ | comparisons |
|---|---|---|
| sorted, $n$ items | 1 | $n - 1$ |
| reversed, $n = 10$ | 10 | 54 |
| reversed, $n = 1000$ | 1000 | 500,499 |
| random, $n = 1000$ | 57 | 37,835 |
| random, $n = 10{,}000$ | 191 | 1,298,241 |

On a reversed input, each strand is one item, the scans make $n(n-1)/2$ comparisons, and each merge makes one, so the time is $\Theta(n^2)$. On a random input, $k$ is about $2\sqrt{n}$, so the time is $O(n^{3/2})$ on average. The best case is a sorted input: one scan and no real merge, $\Theta(n)$.

**Space.** The lists $R$, $S$ and $U$ hold $\Theta(n)$ items. On a linked list, the nodes can be moved between the lists, and the extra space is $O(1)$.

| claim | model and case | bound |
|---|---|---|
| time | comparison model, worst | $\Theta(n^2)$ |
| time | random permutation, average | $O(n^{3/2})$ |
| time | sorted input | $\Theta(n)$, with $n - 1$ comparisons |
| time | in terms of $k$ | $O(nk)$ |
| extra space | array form | $\Theta(n)$ |

## Properties

- **Stable.** Equal items stay in the order of the input, if the merge takes the item of $R$ on a tie.
- **Adaptive.** The time is $O(nk)$, small when the input has a short longest decreasing subsequence. A sorted input takes one scan.
- **Not in place on arrays.** The array form copies items into new lists. On a linked list, it relinks nodes.
- **Not online.** The first strand needs a scan of all the items.

## Variants and improvements

- **Linked lists.** Remove each item of the strand from the input list as the scan passes it. Then the scan and the merge relink nodes, and no new list is needed.
- **Merge the strands at the end.** Keep all strands and merge them pairwise, as in [natural merge sort](/natural-merge-sort/), or with a heap. This gives $O(n \log k)$ for the merging, but the scans still cost $O(nk)$.
- **[Patience sorting](/patience-sorting/).** Put each item on the first pile whose top is larger, using binary search. This builds the same kind of decomposition into monotone sequences in one pass, in $O(n \log n)$ time, and then merges the piles.
- **[Natural merge sort](/natural-merge-sort/).** It also exploits runs, but it uses the runs that are already contiguous in the input, and it takes $O(n \log r)$ time for $r$ runs.

## When to use it

Use strand sort on linked lists that are close to sorted, or that have a few interleaved sorted sequences, for example the output of several sorted sources mixed in time. For general data, use [merge sort](/merge-sort/) or a library sort: strand sort is quadratic on a reversed input.

## Pitfalls

- **The test for the strand.** Use $x < \text{last}(S)$ to skip an item, so that an item equal to the last item joins the strand. With $\le$, equal items are split over several strands, and the sort does more work; it stays correct.
- **The tie in the merge.** Take the item of $R$ on a tie. Taking the item of $S$ breaks the stability.
- **A reversed input.** It makes $n$ strands and $\Theta(n^2)$ comparisons. Do not use strand sort where such input can occur.
- **Quadratic copying.** In the array form, each merge copies all of $R$. A reversed input makes this $\Theta(n^2)$ moves even when the comparisons are few.

## Implementations

## History

Strand sort is a folk method; the NIST Dictionary of Algorithms and Data Structures lists it under this name. Its first strand is the sequence of left-to-right maxima, whose mean length Knuth analyses in Section 1.2.10 of Volume 1. The link between the number of strands and the longest decreasing subsequence is the same kind of link that underlies [patience sorting](/patience-sorting/), which Aldous and Diaconis survey.

## References
