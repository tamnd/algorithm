---
tag: T0XRJS
kind: algorithm
slug: shiloach-vishkin-merge
name: Shiloach-Vishkin merging
aliases:
- Shiloach-Vishkin parallel merge
area: sorting/parallel-sorting
level: research
summary: Merges two sorted lists with p processors in O(n/p + log n) PRAM time by ranking evenly spaced cuts of both lists in the other list.
solves: [parallel-merging-problem]
model: crew-pram
complexity:
  vars: {m: the length of the shorter input, n: the length of the longer input, p: the number of processors}
  time: {worst: Θ(m + n + p log n)}
  space: {extra: O(p)}
  depth: {worst: O(n/p + log n)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [parallel-merging-problem, merging-sorted-lists, binary-search, crew-pram]
see_also: [merge-path, parallel-merging-problem, valiant-parallel-merge, parallel-merge-sort, cole-merge-sort, binary-search, merging-sorted-lists, brent-theorem]
sources:
  - paper: doi:10.1016/0196-6774(81)90010-9
    title: Yossi Shiloach and Uzi Vishkin, Finding the maximum, merging, and sorting in a parallel computation model, Journal of Algorithms 2(1), 1981, 88-102
    locator: merging two sorted lists of lengths m and n, m at most n, in depth O(n/p + log n) for p at most n, and in depth O(log m / log(p/n)) for p at least n; sorting in depth O((n/p) log n + log n log p) for p at most n
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 4, Searching, merging and sorting, merging by partitioning on the CREW PRAM
  - paper: "Selim G. Akl and Nicola Santoro, Optimal parallel merging and sorting without memory conflicts, IEEE Transactions on Computers C-36(11), 1987"
    locator: a merge with p processors that splits the work into equal pieces without concurrent reads
---

Shiloach-Vishkin merging merges two sorted lists $A$ of length $m$ and $B$ of length $n$, with $m \le n$, on $p \le n$ processors. It cuts each list into $p$ blocks of equal length, and finds the place of each cut in the other list by [binary search](/binary-search/). The cuts of both lists then split the merge into at most $2p - 1$ independent pieces, each with at most one block of each list, and the pieces are merged sequentially. On the [CREW PRAM](/crew-pram/) this takes time $O(n/p + \log n)$ and work $O(n + p \log n)$, which is optimal for $p \le n / \log n$. Shiloach and Vishkin gave it in 1981, with a sort and a fast maximum in the same model.

## In plain words

Two sorted queues of people must become one sorted queue, and there are a few ushers to share the job.

Mark every tenth person in the first queue and every tenth person in the second. Each marked person finds where they would stand in the other queue, by a quick halving search. All marks together cut the final queue into short stretches. Inside one stretch, no marked person stands, so the stretch holds at most ten people from each queue.

Each usher then takes one or two stretches and merges them in the usual way. No usher has much more work than another, whatever the names in the queues.

## The problem

The input is two sorted arrays $A[0 \ldots m-1]$ and $B[0 \ldots n-1]$ of keys from a total order, with $m \le n$, and a number $p$ of processors with $1 \le p \le n$. The output is their stable merge $C[0 \ldots m+n-1]$, in which each item of $A$ comes before each equal item of $B$. This is the [parallel merging problem](/parallel-merging-problem/) on the CREW PRAM.

A *split* is a pair $(i, j)$ such that the first $i + j$ items of $C$ are $A[0 \ldots i-1]$ and $B[0 \ldots j-1]$. Consecutive splits cut $C$ into pieces that can be merged on their own.

## The algorithm

```pseudo id=main
SV-MERGE(A[0 .. m − 1], B[0 .. n − 1], p)
L1  a ← ⌈m/p⌉;  b ← ⌈n/p⌉
L2  parallel for t ← 1 to p − 1 with t·a < m: i ← t·a; j ← the number of items of B less than A[i]; the A-cut t is the split (i, j)
L3  parallel for t ← 1 to p − 1 with t·b < n: j ← t·b; i ← the number of items of A at most B[j]; the B-cut t is the split (i, j)
L4  parallel for each cut: its place among all cuts is t − 1 plus ⌈j/b⌉ − 1 for an A-cut, or plus ⌈i/a⌉ − 1 for a B-cut (at least 0)
L5  S ← (0, 0), the cuts in the order of line L4, (m, n)
L6  parallel for each pair of consecutive splits (i, j), (i′, j′) in S:
L7      merge A[i .. i′ − 1] and B[j .. j′ − 1] sequentially, A first on ties, into C[i + j .. i′ + j′ − 1]
```

Line L4 needs no search. An A-cut $(i, j)$ comes after exactly the B-cuts $t b < j$, and there are $\max(0, \lceil j/b \rceil - 1)$ of them. A B-cut $(i, j)$ comes after exactly the A-cuts $t a < i$. With $2p - 2$ cuts and $p$ processors, each processor handles at most two cuts in lines L2 to L4 and at most two pieces in lines L6 and L7.

## Example

Merge $A = [1, 4, 6, 9]$ and $B = [2, 3, 7, 8, 10]$ with $p = 3$, so $a = \lceil 4/3 \rceil = 2$ and $b = \lceil 5/3 \rceil = 2$.

| cut | index | rank in the other list | split | place by line L4 |
| --- | --- | --- | --- | --- |
| A-cut 1 | $A[2] = 6$ | 2 items of $B$ are less than 6 | $(2, 2)$ | $0 + (\lceil 2/2 \rceil - 1) = 0$ |
| B-cut 1 | $B[2] = 7$ | 3 items of $A$ are at most 7 | $(3, 2)$ | $0 + (\lceil 3/2 \rceil - 1) = 1$ |
| B-cut 2 | $B[4] = 10$ | 4 items of $A$ are at most 10 | $(4, 4)$ | $1 + (\lceil 4/2 \rceil - 1) = 2$ |

The A-cut for $t = 2$ would be at index 4, which is not less than $m = 4$, so it is left out. So $S = (0, 0), (2, 2), (3, 2), (4, 4), (4, 5)$, and the pieces are:

| piece | part of $A$ | part of $B$ | output |
| --- | --- | --- | --- |
| 1 | $[1, 4]$ | $[2, 3]$ | $C[0 \ldots 3] = 1, 2, 3, 4$ |
| 2 | $[6]$ | none | $C[4] = 6$ |
| 3 | $[9]$ | $[7, 8]$ | $C[5 \ldots 7] = 7, 8, 9$ |
| 4 | none | $[10]$ | $C[8] = 10$ |

Each piece has at most $a = 2$ items of $A$ and at most $b = 2$ items of $B$.

## Correctness

Each cut is a split: for an A-cut, the items before $A[i]$ in the stable merge are $A[0 \ldots i-1]$ and the items of $B$ less than $A[i]$, and for a B-cut, the items before $B[j]$ are $B[0 \ldots j-1]$ and the items of $A$ at most $B[j]$. All splits lie on one monotone path through the grid of $A$ and $B$, so ordering them by $i + j$ also orders both coordinates, and line L4 computes this order. Between consecutive splits, the output is exactly the merge of the two parts, and so the pieces together give $C$. No cut lies strictly inside a piece, so a piece holds items of at most one block of each list. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

All bounds are for the CREW PRAM with $p \le n$ processors.

**Cuts.** There are at most $2p - 2$ cuts. Each binary search on lines L2 and L3 takes $O(\log n)$ steps, and each processor does at most two. Line L4 takes $O(1)$ time. Concurrent reads occur because many searches read the same cells of $A$ and $B$.

**Pieces.** There are at most $2p - 1$ pieces, each with at most $\lceil m/p \rceil + \lceil n/p \rceil \le 2 \lceil n/p \rceil$ items. With two pieces per processor, lines L6 and L7 take time $O(n/p)$.

**Total.** Time $O(n/p + \log n)$ and work $O(m + n + p \log n)$. For $p \le n / \log n$ the work is $O(n)$, which is optimal, because merging needs $\Omega(m + n)$ steps in the worst case when $m = n$. See the [merging lower bound](/merging-lower-bound/).

**Space.** The cuts take $O(p)$ cells besides the output.

## Properties

- **Stable.** On equal keys, items of $A$ come first, and both lists keep their order.
- **Balanced.** Each processor merges $O(n/p)$ items whatever the keys.
- **Deterministic and comparison-based.**
- **Not in place.** The output goes to a separate array.

## Variants and improvements

- **Many processors.** For $p \ge n$, Shiloach and Vishkin merge in depth $O(\log m / \log(p/n))$, which is $O(k)$ for $p = \lceil m^{1/k} n \rceil$. The idea is to search with $p/n$ processors per item: a search over $r$ candidates with $q$ processors cuts the range by a factor of about $q$ per step.
- **Merge sort.** Using this merge on each level of a merge sort gives the sort of Shiloach and Vishkin, in depth $O((n/p) \log n + \log n \log p)$ for $p \le n$.
- **Merge path.** [Merge path](/merge-path/) cuts the output, not the inputs, into $p$ pieces of exactly equal length. It needs only $p - 1$ searches and gives perfect balance, at the cost of a search along a diagonal.
- **Without concurrent reads.** Akl and Santoro gave a merge with the same bounds on the [EREW PRAM](/erew-pram/).
- **Fewer rounds.** [Valiant's merge](/valiant-parallel-merge/) uses $O(\log \log n)$ rounds with $m + n$ processors in the parallel comparison model, where only comparisons count.

## When to use it

Use it when $p$ processors must merge two long sorted lists and a small $O(\log n)$ start-up cost is acceptable, for example inside a parallel merge sort. It is simple and needs no shared queue of work. If equal output lengths per processor matter, as on GPUs, [merge path](/merge-path/) is the better choice.

## Pitfalls

- **The same rule for ties in both searches.** If both searches count the items less than the cut, an A-cut and a B-cut with equal keys can claim the same output position. Use "less than" for A-cuts and "at most" for B-cuts.
- **Cuts at the end.** A cut at index $m$ or $n$ does not exist. Skip it, or the search reads past the end.
- **Unbalanced lengths.** If $m$ is much smaller than $n$, the blocks of $A$ are short but the blocks of $B$ still have $\lceil n/p \rceil$ items, so the time is set by $n$.
- **Sorting the cuts.** Sorting the $2p - 2$ cuts by a general sort costs $O(\log p)$ time or more. Line L4 places them in $O(1)$ time, because the place of a cut in the other list is known from its rank.

## Implementations

## History

Shiloach and Vishkin presented the merge in 1981 at CONPAR and in the Journal of Algorithms, together with an algorithm for the maximum in depth $O(n/p + \log \log p)$ and a sort. Their paper counts all steps, including the assignment of processors to jobs, and not only comparisons. Their sort for $p = n^{1 + 1/k}$ processors matches the depth $O(k \log n)$ of earlier sorts by Hirschberg and by Preparata, with a simpler method.

## References
