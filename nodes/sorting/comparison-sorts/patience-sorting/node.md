---
tag: JTB25B
kind: algorithm
slug: patience-sorting
name: Patience sorting
aliases:
- O(n log n) LIS
- card-pile sorting
- patience sorting LIS
area: sorting/comparison-sorts
level: advanced
summary: Deals elements onto piles by binary search and merges them; the pile count equals the longest increasing subsequence length.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items, k: the number of piles}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: true, in_place: false, adaptive: true, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [binary-search, k-way-merge]
see_also: [longest-increasing-subsequence, strand-sort, k-way-merge, binary-search, young-tableau, binary-heap, natural-merge-sort]
sources:
  - paper: "David Aldous and Persi Diaconis, Longest increasing subsequences: from patience sorting to the Baik-Deift-Johansson theorem, Bulletin of the American Mathematical Society 36(4), 1999"
    locator: Section 1 (the patience sorting game, the greedy strategy, and the lemma that the number of piles equals the length of the longest increasing subsequence), and the asymptotics 2 sqrt(n)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.4, Tableaux and involutions (Algorithm I, insertion into a tableau, and Schensted's theorem on the length of the first row)
  - paper: "C. Schensted, Longest increasing and decreasing subsequences, Canadian Journal of Mathematics 13, 1961"
    locator: the main theorem, the longest increasing subsequence equals the length of the first row
  - paper: "Badrish Chandramouli and Jonathan Goldstein, Patience is a virtue: revisiting merge and sort on modern processors, ACM SIGMOD 2014"
    locator: the description of patience sort with ping-pong merging and its speed on almost sorted data
---

Patience sorting deals the items, in input order, onto piles like cards in the solitaire game of the same name: each item goes on the leftmost pile whose top is greater than it, or starts a new pile at the right. The tops of the piles stay in order from left to right, so a [binary search](/binary-search/) finds the pile. Each pile, read from the top, is sorted, and a [k-way merge](/k-way-merge/) of the piles with a heap gives the sorted output. The sort takes $O(n \log n)$ time, and $O(n \log k)$ for $k$ piles. The number of piles is the length of the longest non-decreasing subsequence of the input, so the first phase alone solves the [longest increasing subsequence](/longest-increasing-subsequence/) problem in $O(n \log n)$ time.

## In plain words

You deal a shuffled deck of cards, one card at a time. Each card goes on top of the leftmost pile whose top card is higher than it. If no top card is higher, the card starts a new pile on the right. So on each pile, each card is lower than the card under it.

The top cards, from left to right, are always in order, from low to high. So you can find the right pile fast, by looking at the middle pile first and then halving the search.

Each pile, read from the top down, is sorted. To finish the sort, you take the lowest top card of all the piles, again and again, until all piles are empty.

The number of piles tells you something more: it is the length of the longest sequence of cards in the deck that rises from left to right.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm uses piles of total size $n$ and a heap of the piles as extra memory.

## The algorithm

```pseudo id=main
PATIENCE-SORT(A)                           ▷ n is the length of A
L1  P ← an empty list of piles             ▷ P[0], P[1], ... from left to right
L2  for each x in A, in order do
L3      i ← the least index with x < top(P[i]), by binary search; |P| if none
L4      if i = |P| then append an empty pile to P
L5      push x on P[i]
L6  H ← a min-heap of the piles, by (top, index)
L7  for t ← 0 to n − 1 do
L8      p ← the pile at the root of H;  A[t] ← pop(p)
L9      if p is empty then remove it from H; restore the heap order of H
```

Lines L2 to L5 deal the items. The tops of the piles are non-decreasing from left to right, so the binary search of line L3 is valid: it makes $\lceil \lg(|P| + 1) \rceil$ comparisons at most. Lines L6 to L9 merge the piles. The heap compares two piles by their top items, and on equal tops by their index, so that the pile further left wins. This rule makes the sort stable.

## Example

Deal $A = [5, 1, 4, 2, 8, 3, 7, 6]$. The piles are written from the bottom to the top.

| item | the tops before it | pile | the piles after it |
|---|---|---|---|
| 5 | none | new pile 0 | [5] |
| 1 | 5 | 0, since $1 < 5$ | [5 1] |
| 4 | 1 | new pile 1 | [5 1] [4] |
| 2 | 1 4 | 1 | [5 1] [4 2] |
| 8 | 1 2 | new pile 2 | [5 1] [4 2] [8] |
| 3 | 1 2 8 | 2 | [5 1] [4 2] [8 3] |
| 7 | 1 2 3 | new pile 3 | [5 1] [4 2] [8 3] [7] |
| 6 | 1 2 3 7 | 3 | [5 1] [4 2] [8 3] [7 6] |

The binary searches make 11 comparisons. There are 4 piles, and the longest increasing subsequence has length 4: following the top of the pile to the left at the time each item was placed, back from 6, gives $1, 2, 3, 6$. The merge takes the least top each time: 1, 2, 3, 4, 5, 6, 7, 8.

## Correctness

Each item $x$ goes on the leftmost pile whose top is greater than $x$. So the new top $x$ is less than the old top of that pile, and each pile, read from the top down, is increasing. The tops stay non-decreasing from left to right: the pile to the left of the chosen one has a top at most $x$, by the choice, and the new top $x$ is less than the old top, which was at most the top to the right. So the binary search is valid at each step. The merge of sorted piles by a heap outputs the least remaining item each time, so the output is sorted, and it holds each item once. The full proof, with stability and the number of piles, is below.

## Complexity

**The deal.** Each of the $n$ binary searches makes at most $\lceil \lg(k + 1) \rceil$ comparisons, where $k$ is the final number of piles. So the deal makes $O(n \log k)$ comparisons.

**The merge.** Building the heap of $k$ piles takes $O(k)$ time. Each of the $n$ steps pops one item and restores the heap in $O(\log k)$ time. So the merge takes $O(n \log k)$ time.

**The number of piles.** It equals the length of the longest non-decreasing subsequence of the input. On a random permutation this is about $2\sqrt{n}$ (Aldous and Diaconis). So on random input both phases cost about $\tfrac{1}{2} n \lg n$ comparisons each up to the constant of the heap, and the total is $\Theta(n \log n)$. On a sorted input there are $n$ piles of one item, so the merge is a full heapsort, with $\Theta(n \log n)$ time. On a reversed input there is one pile, each binary search makes one comparison, and the merge needs no comparisons: $\Theta(n)$ time.

| input | piles $k$ | deal comparisons | total comparisons |
|---|---|---|---|
| reversed, $n = 1000$ | 1 | 999 | 999 |
| sorted, $n = 1000$ | 1000 | 7,987 | 29,577 |
| random, $n = 1000$ | 59 | 5,124 | 16,836 |
| random, $n = 10^4$ | 191 | 68,921 | 225,822 |
| random, $n = 10^5$ | 623 | 858,730 | 2,831,406 |

The counts are for the implementation on this page, whose heap makes up to two comparisons to order two piles. For $n = 10^5$, $n \lg n$ is about 1,660,964.

**Space.** The piles hold the $n$ items, and the heap and the tops take $O(k)$ more. So the extra space is $\Theta(n)$.

| claim | model and case | bound |
|---|---|---|
| time | comparison model, worst | $\Theta(n \log n)$ |
| time | in terms of the piles | $O(n \log k)$ |
| time | reversed input | $\Theta(n)$ |
| extra space | | $\Theta(n)$ |

## Properties

- **Stable.** Two equal items never share a pile, and the later one always goes to a pile further right. The merge breaks ties by the index of the pile, so the earlier item comes out first.
- **Not in place.** The piles need $\Theta(n)$ extra space.
- **Adaptive.** The time is $O(n \log k)$, small when the input has a short longest non-decreasing subsequence, such as a decreasing input. A variant below also makes it fast on increasing runs.
- **The deal is online.** Each item can be placed as it arrives, and the number of piles at each moment is the longest non-decreasing subsequence of the prefix.

## Variants and improvements

- **Longest increasing subsequence.** Keep only the tops, and for each item a link to the top of the pile to its left when it was placed. The number of piles is the length, and the links give a longest subsequence. For a strictly increasing subsequence, put $x$ on the leftmost pile whose top is at least $x$ instead.
- **Tableaux.** If the items that are covered are pushed into a second row, and so on, the deal becomes Schensted's insertion into a [Young tableau](/young-tableau/), the row insertion of the Robinson-Schensted correspondence (Knuth, Section 5.1.4). The first row has the length of the longest increasing subsequence.
- **Fast paths for runs.** Test the last pile before the binary search, and allow items to go on the tail of a pile as well as its head. Chandramouli and Goldstein use this, with a balanced merge of the piles instead of a heap, to make patience sort fast on data that is almost sorted.
- **[Strand sort](/strand-sort/).** It also splits the input into sorted sequences and merges them, but it builds one sequence per scan, and its number of strands is the longest decreasing subsequence.

## When to use it

Use the dealing phase to find a longest increasing subsequence in $O(n \log n)$ time, which is its main use. As a sort, patience sorting is useful for data that is almost sorted in reverse, or that consists of a few interleaved sequences, and in the tuned form for event streams that arrive nearly in order. For general data, [merge sort](/merge-sort/) or a library sort is simpler and as fast.

## Pitfalls

- **The binary search on the tops.** The search must look for the leftmost top greater than $x$. Searching for the first top at least $x$ is also correct as a sort, but then equal items share a pile, the sort is no longer stable, and the number of piles is the strictly increasing length.
- **Ties in the heap.** Order the piles by top and then by index. A heap of pairs in a language that compares the second field only on an exact equality of the first may lose the tie rule for items that are equal but not identical.
- **Sorted input.** It makes $n$ piles, and the merge is then a heapsort. Add the fast path for the last pile if sorted input is common.
- **Back links for the subsequence.** Each link must point to the top of the pile to the left at the moment the item is placed, not at the end. The top changes later.

## Implementations

## History

The name comes from a solitaire card game. Aldous and Diaconis trace the use of the game to sort and to study increasing subsequences to Mallows in the early 1960s, and they show that the greedy deal gives the least number of piles, equal to the length of the longest increasing subsequence. Schensted had proved the related theorem for the first row of a tableau in 1961. The question of the typical length, about $2\sqrt{n}$, led to the work of Vershik and Kerov, Logan and Shepp, and Baik, Deift and Johansson, which Aldous and Diaconis survey. Chandramouli and Goldstein revived the method as a practical sort in 2014.

## References
