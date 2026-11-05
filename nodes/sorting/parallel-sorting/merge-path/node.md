---
tag: 8R73CV
kind: algorithm
slug: merge-path
name: Merge path
aliases:
- GPU merge path
- merge path partitioning
area: sorting/parallel-sorting
level: advanced
summary: Splits a merge into independent pieces by binary searching along the merge path of the two inputs.
solves: [parallel-merging-problem]
model: crew-pram
complexity:
  vars: {m: the length of the first input, n: the length of the second input, p: the number of processors}
  time: {worst: "Θ(m + n + p log(min(m, n) + 1))"}
  space: {extra: O(p)}
  depth: {worst: "O((m + n)/p + log(min(m, n) + 1))"}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [parallel-merging-problem, merging-sorted-lists, binary-search, crew-pram]
see_also: [parallel-merging-problem, shiloach-vishkin-merge, parallel-merge-sort, merging-sorted-lists, binary-search, valiant-parallel-merge, cole-merge-sort, sample-sort]
sources:
  - paper: "Saher Odeh, Oded Green, Zahi Mwassi, Oz Shmueli and Yitzhak Birk, Merge Path - parallel merging made simple, IEEE International Parallel and Distributed Processing Symposium Workshops (IPDPSW), 2012"
    locator: the merge path, its diagonals, and the partition into p pieces of equal output length
  - paper: "Oded Green, Robert McColl and David A. Bader, GPU merge path: a GPU merging algorithm, Proceedings of the 26th ACM International Conference on Supercomputing (ICS), 2012"
    locator: the merge path partition on GPUs, by thread blocks and then by threads
  - paper: "Selim G. Akl and Nicola Santoro, Optimal parallel merging and sorting without memory conflicts, IEEE Transactions on Computers C-36(11), 1987"
    locator: an earlier merge that splits the output into equal pieces by searching for the split points
  - paper: doi:10.1016/0196-6774(81)90010-9
    title: Yossi Shiloach and Uzi Vishkin, Finding the maximum, merging, and sorting in a parallel computation model, Journal of Algorithms 2(1), 1981
    locator: merging with p processors in time O(n/p + log n) by cutting both inputs at ranked points
---

Merge path merges two sorted arrays $A$ and $B$ on $p$ processors by cutting the output into $p$ pieces of equal length. For each cut position $k$, a [binary search](/binary-search/) finds how many of the first $k$ output items come from $A$. Then each processor merges its own piece with the ordinary sequential merge, with no further communication. On the [CREW PRAM](/crew-pram/) this takes time $O((m+n)/p + \log \min(m, n))$ and work $O(m + n + p \log \min(m, n))$, which is optimal for $p \le (m+n)/\log(m+n)$. It is the standard way to balance merges on GPUs and multicore processors.

## In plain words

Picture a grid with the first list along the top and the second down the side. A merge walks from the top-left corner to the bottom-right corner: one step right when it takes an item from the first list, one step down when it takes an item from the second. This walk is the merge path.

Every walk of this kind crosses each diagonal of the grid exactly once. The point where it crosses tells how many items of each list come before that point of the output. That point can be found by a quick halving search along the diagonal, without doing the merge.

So cut the output into equal parts by diagonals, find the crossing on each diagonal at the same time, and let each helper merge the items between two crossings.

## The problem

The input is two sorted arrays $A[0 \ldots m-1]$ and $B[0 \ldots n-1]$ of keys from a total order and a number $p$ of processors. The output is their stable merge $C[0 \ldots m+n-1]$, in which each item of $A$ comes before each equal item of $B$. This is the [parallel merging problem](/parallel-merging-problem/) on the [CREW PRAM](/crew-pram/).

For $0 \le k \le m + n$, the *co-rank* of $k$ is the pair $(i, j)$ with $i + j = k$ such that the first $k$ items of $C$ are $A[0 \ldots i-1]$ and $B[0 \ldots j-1]$. On the grid, it is the point where the merge path crosses diagonal $k$.

## The algorithm

```pseudo id=main
CO-RANK(k, A[0 .. m − 1], B[0 .. n − 1])          ▷ 0 ≤ k ≤ m + n
L1  lo ← max(0, k − n);  hi ← min(k, m)
L2  while lo < hi do
L3      i ← ⌊(lo + hi) / 2⌋
L4      if B[k − i − 1] < A[i] then hi ← i else lo ← i + 1
L5  return (lo, k − lo)

MERGE-PATH(A, B, p)
L6  parallel for t ← 0 to p − 1 do
L7      (i, j) ← CO-RANK(⌊t(m + n)/p⌋, A, B);  (i′, j′) ← CO-RANK(⌊(t + 1)(m + n)/p⌋, A, B)
L8      merge A[i .. i′ − 1] and B[j .. j′ − 1] sequentially, A first on ties, into C[i + j .. i′ + j′ − 1]
```

Line L4 asks whether $A[i]$ is among the first $k$ items of $C$. It is not exactly when the $k - i$ items $B[0], \ldots, B[k-i-1]$ all come before it, that is, when $B[k-i-1] < A[i]$. The search finds the least $i$ for which $A[i]$ is not among the first $k$ items. The indices on line L4 are always in range, because $lo \le i < hi$.

## Example

Merge $A = [1, 4, 6, 9]$ and $B = [2, 3, 7, 8, 10]$ with $p = 3$, so the cuts are at $k = 0, 3, 6, 9$.

For $k = 3$, the search starts with $lo = 0$ and $hi = 3$. At $i = 1$, $B[1] = 3 < A[1] = 4$, so $hi = 1$. At $i = 0$, $B[2] = 7$ is not less than $A[0] = 1$, so $lo = 1$. The co-rank is $(1, 2)$: the first three output items are $A[0]$ and $B[0], B[1]$. In the same way the co-rank of $6$ is $(3, 3)$.

| processor | co-ranks | piece of $A$ | piece of $B$ | output |
| --- | --- | --- | --- | --- |
| 0 | $(0, 0)$ to $(1, 2)$ | $[1]$ | $[2, 3]$ | $C[0 \ldots 2] = 1, 2, 3$ |
| 1 | $(1, 2)$ to $(3, 3)$ | $[4, 6]$ | $[7]$ | $C[3 \ldots 5] = 4, 6, 7$ |
| 2 | $(3, 3)$ to $(4, 5)$ | $[9]$ | $[8, 10]$ | $C[6 \ldots 8] = 8, 9, 10$ |

Each processor merges exactly three items, whatever the keys.

## Correctness

The items of $A$ among the first $k$ items of $C$ form a prefix of $A$, because the stable merge keeps the order of $A$, and the same holds for $B$. So the co-rank exists and is unique. The predicate on line L4 holds for $i$ exactly when $A[i]$ is not among the first $k$ items, and it is monotone in $i$, so the binary search returns the co-rank. The items of $C[k_t \ldots k_{t+1} - 1]$ are then the pieces of $A$ and $B$ between the two co-ranks, and their stable merge is that part of $C$. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

All bounds are for the [CREW PRAM](/crew-pram/) with $p \le m + n$ processors.

**Search.** The search range on line L1 has at most $\min(k, m) - \max(0, k - n) \le \min(m, n)$ values, so CO-RANK makes at most $\lceil \lg(\min(m, n) + 1) \rceil$ probes. All processors search the same arrays at the same time, which needs concurrent reads.

**Merge.** Each piece has $\lfloor (t+1)(m+n)/p \rfloor - \lfloor t(m+n)/p \rfloor \le \lceil (m+n)/p \rceil$ items, so the sequential merges take time $O((m+n)/p)$.

**Total.** The time is $O((m+n)/p + \log \min(m, n))$ and the work is $O(m + n + p \log \min(m, n))$. For $p \le (m + n) / \lg(m + n)$ the work is $O(m + n)$, and the time is $O((m+n)/p)$, which is linear speedup.

**Work-span form.** In the [work-span model](/work-span-model/), with $p = \lceil (m+n) / \lg(m+n) \rceil$ pieces, the work is $O(m + n)$ and the span is $O(\log(m + n))$. Used inside [parallel merge sort](/parallel-merge-sort/), this gives a sort with work $O(n \log n)$ and span $O(\log^2 n)$.

**Space.** Each processor uses $O(1)$ extra words besides the output.

## Properties

- **Perfect balance.** Every processor merges $\lfloor (m+n)/p \rfloor$ or $\lceil (m+n)/p \rceil$ items, for every input. Methods that cut only one input, or both inputs at evenly spaced positions, can give pieces of very different sizes.
- **Stable.** The test on line L4 and the sequential merge both put $A$ first on ties.
- **No synchronization between pieces.** Each processor computes its own two co-ranks, so the pieces need no communication after the searches.
- **Comparison-based and deterministic.**

## Variants and improvements

- **Two levels on GPUs.** GPU merge path first cuts the output into one piece per thread block, then each block cuts its piece again into one piece per thread, in fast local memory.
- **Reuse of co-ranks.** Each co-rank except the first and the last is the end of one piece and the start of the next. Computing it once and sharing it halves the number of searches.
- **Merging k lists.** For $k$ sorted lists, the co-rank of a position is a vector of $k$ indices. It can be found by a search over the values, as in the multiway merge of [sample sort](/sample-sort/) and of parallel sorting by regular sampling.
- **Merge sort.** Using merge path for every merge of a [merge sort](/merge-sort/) gives a parallel merge sort whose levels are each perfectly balanced.
- **Other cut methods.** The [Shiloach-Vishkin merge](/shiloach-vishkin-merge/) cuts both inputs at evenly spaced items and finds their ranks in the other input. This gives up to $2p$ pieces of uneven size, with the same bounds.

## When to use it

Use merge path whenever a merge of two sorted arrays must run on several processors or GPU threads. It is short, deterministic, stable and perfectly balanced. It is also the base of the merges in GPU merge sorts and of the merge phase of sort-merge joins. For very many processors with $p$ close to $m + n$, the $\log$ term of the search dominates, and [Valiant's merge](/valiant-parallel-merge/) has fewer rounds in the comparison model.

## Pitfalls

- **Wrong tie test.** If line L4 tests $B[k-i-1] \le A[i]$, the result is the co-rank of the merge that puts $B$ first on ties, while line L8 puts $A$ first. Then the pieces overlap or leave gaps when there are equal keys across the two inputs.
- **Search range.** Without the bounds $\max(0, k - n)$ and $\min(k, m)$ on line L1, the search reads outside $A$ or $B$.
- **Integer overflow.** For very long arrays, $t(m+n)$ can overflow a 32-bit integer. Compute the cut positions with wider integers.
- **Writing in place.** The output must not overlap the inputs, since other processors still read them.

## Implementations

## History

Shiloach and Vishkin in 1981 and Akl and Santoro in 1987 merged in parallel by finding split points with binary searches. The name merge path, and the picture of the merge as a path in a grid crossed by diagonals, are due to Odeh, Green, Mwassi, Shmueli and Birk in 2012. In the same year Green, McColl and Bader adapted it for GPUs.

## References
