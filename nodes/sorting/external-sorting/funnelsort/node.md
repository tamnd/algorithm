---
tag: VCKGXK
kind: algorithm
slug: funnelsort
name: Funnelsort
aliases:
- cache-oblivious merge sort
- cache-oblivious sort
- lazy funnelsort
area: sorting/external-sorting
level: research
summary: A cache-oblivious sort that merges with a recursive k-merger, achieving the optimal block transfer bound without knowing M or B.
solves: [sorting-problem]
model: cache-oblivious-model
complexity:
  vars: {N: the number of items, M: the cache size in items, B: the cache line size in items, n: the number of lines N/B, m: the number of lines M/B}
  time: {worst: O(N log N), average: O(N log N), best: O(N log N)}
  space: {extra: Θ(N)}
  io:
    worst: "O(n log_m n)"
    average: "O(n log_m n)"
    best: "O(n log_m n)"
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
prereqs: [merge-sort, k-way-merge, cache-oblivious-model, van-emde-boas-layout]
see_also: [external-merge-sort, external-sorting-io-lower-bound, external-memory-model, memory-hierarchy, cache-oblivious-b-tree, buffer-tree, insertion-sort]
sources:
  - paper: "Matteo Frigo, Charles E. Leiserson, Harald Prokop and Sridhar Ramachandran, Cache-oblivious algorithms, 40th Annual Symposium on Foundations of Computer Science (FOCS 1999)"
    locator: Section 4, Funnelsort (the k-merger, its recursive layout with buffers of size 2k^(3/2), and the bound on cache misses under the tall-cache assumption)
  - paper: "Gerth Stolting Brodal and Rolf Fagerberg, Cache oblivious distribution sweeping, 29th International Colloquium on Automata, Languages and Programming (ICALP 2002)"
    locator: the section on lazy funnelsort (binary mergers with buffers that are filled when they are empty)
  - paper: "Gerth Stolting Brodal, Rolf Fagerberg and Kristoffer Vinther, Engineering a cache-oblivious sorting algorithm, ACM Journal of Experimental Algorithmics 12, 2007"
    locator: the implementation choices for lazy funnelsort and the experiments against quicksort and other sorts
  - paper: "Gerth Stolting Brodal and Rolf Fagerberg, On the limits of cache-obliviousness, Proceedings of the 35th ACM Symposium on Theory of Computing (STOC 2003)"
    locator: abstract and the results on sorting (a tall cache is necessary for an optimal cache-oblivious sort)
---

Funnelsort is a [merge sort](/merge-sort/) for the [cache-oblivious model](/cache-oblivious-model/): it does not know the cache size $M$ or the line size $B$, and still makes $O\big(\frac NB \log_{M/B} \frac NB\big)$ cache misses, which is the [I/O lower bound for sorting](/external-sorting-io-lower-bound/). It cuts the input into $N^{1/3}$ parts of $N^{2/3}$ items, sorts each part recursively, and merges the parts with a *funnel*, a tree of binary mergers with buffers between them, laid out recursively like the [van Emde Boas layout](/van-emde-boas-layout/). Because it is optimal for every $M$ and $B$ at the same time, it is optimal on every level of a [memory hierarchy](/memory-hierarchy/) at once.

## In plain words

An [external merge sort](/external-merge-sort/) merges as many sorted pieces at once as the memory allows, so it must know the size of the memory. Funnelsort does not know it. It cuts the input into a few large pieces, sorts each piece in the same way, and then merges the pieces through a funnel.

The funnel is a tree of small merges. Each merge takes items from two boxes below it and puts them in a box above it. When a box is empty, the merge below it runs until the box is full again. The boxes have carefully chosen sizes, and the tree is stored in memory so that each small part of it is close together. Then, whatever the size of the cache, a part of the funnel fits in it and does a lot of work before the cache must load something else.

## The problem

The input is an array $A$ of $N$ items with a total order. The output is the same array in non-decreasing order. This is the [sorting problem](/sorting-problem/). The cost is the number of cache misses in the [cache-oblivious model](/cache-oblivious-model/): an ideal cache of $M$ items in lines of $B$ items, with $M = \Omega(B^2)$ (a *tall cache*). The algorithm may not use $M$ or $B$.

## The algorithm

A *$k$-funnel* is a complete binary tree with $k$ leaves, rounded up to a power of 2. Each leaf is a sorted input. Each inner node is a binary merger with an output buffer. For a funnel with $k = 2^h$ leaves, cut the tree at height $\lfloor h/2 \rfloor$ from the top: this gives a top funnel with about $\sqrt k$ leaves and about $\sqrt k$ bottom funnels. The buffers at the roots of the bottom funnels hold $\lceil k^{3/2} \rceil$ items, and the same rule applies inside the top funnel and inside each bottom funnel. In memory, the top funnel comes first, then each bottom funnel with its buffer, each in the same recursive layout.

```pseudo id=main
FUNNELSORT(A)                           ▷ A has n items
L1  if n ≤ 8 then sort A by insertion sort and return
L2  k ← ⌈n^(1/3)⌉; cut A into k consecutive parts of at most ⌈n/k⌉ items
L3  for each part P do FUNNELSORT(P)
L4  build a k-funnel with the sorted parts as its leaves and a root buffer of n items; FILL(root)
L5  copy the root buffer back to A

FILL(v)                                 ▷ v is an inner node with children c₁ and c₂
L6  while the buffer of v is not full do
L7      for each child c whose buffer is empty and not exhausted do FILL(c)
L8      if the buffers of both children are empty then mark v exhausted and return
L9      move the smaller head of the two child buffers to the end of the buffer of v, the left one on ties
```

FILL is *lazy*: a node runs only when its parent needs items and its own buffer is empty, and then it fills its buffer completely. A leaf is exhausted from the start, because its whole input is already in its buffer. Line L8 marks a node exhausted when both children have no more items, which ends the merge from the bottom up. This form of the funnel is the *lazy funnelsort* of Brodal and Fagerberg. The original form of Frigo et al. is equivalent: a $k$-merger outputs $k^3$ items per call, and calls its bottom mergers when the buffers that feed the top merger are empty.

## Example

Sort the 27 items $A = (21, 4, 17, 9, 26, 1, 12, 23, 6, 15, 19, 3, 25, 8, 11, 14, 2, 20, 27, 5, 10, 16, 24, 7, 13, 18, 22)$. Line L2 gives $k = 3$, so there are three parts of 9 items. Line L3 sorts them recursively:

- $P_1 = (1, 4, 6, 9, 12, 17, 21, 23, 26)$
- $P_2 = (2, 3, 8, 11, 14, 15, 19, 20, 25)$
- $P_3 = (5, 7, 10, 13, 16, 18, 22, 24, 27)$

The 3-funnel has 4 leaves: $P_1$, $P_2$, $P_3$ and an empty one. The root merges two nodes, $L$ over $P_1, P_2$ and $R$ over $P_3$ and the empty leaf. With $h = 2$, the buffers of $L$ and $R$ hold $4^{3/2} = 8$ items.

| step | call | buffer after the call | root output so far ends with |
|---|---|---|---|
| 1 | FILL($L$) | 1, 2, 3, 4, 6, 8, 9, 11 | |
| 2 | FILL($R$) | 5, 7, 10, 13, 16, 18, 22, 24 | |
| 3 | root merges until $L$ is empty | $R$: 13, 16, 18, 22, 24 | 9, 10, 11 |
| 4 | FILL($L$) | 12, 14, 15, 17, 19, 20, 21, 23 | |
| 5 | root merges until $L$ is empty | $R$: 24 | 21, 22, 23 |
| 6 | FILL($L$), then $L$ is exhausted | 25, 26 | |
| 7 | root merges until $R$ is empty | $L$: 25, 26 | 23, 24 |
| 8 | FILL($R$), then $R$ is exhausted | 27 | |
| 9 | root merges the rest | | 25, 26, 27 |

Each call of FILL fills a whole buffer, or empties its subtree. The root never waits for one item at a time from the leaves.

## Correctness

By induction on the height of a node, the sequence of items that a node $v$ puts into its buffer, over all calls, is the stable merge of the leaves below $v$, from left to right. Line L9 always takes the smaller head, and the heads are the next items of the children's sequences, which are sorted by induction. Line L8 stops $v$ only when both children are exhausted and empty, so no item is lost. So the root buffer holds the stable merge of the sorted parts, and by induction on $n$, FUNNELSORT sorts. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **Cache misses.** $O\big(1 + \frac NB \log_{M/B} \frac NB\big)$ with a tall cache, $M = \Omega(B^2)$. The proof is in the [cache-oblivious model](/cache-oblivious-model/) page: a $k$-funnel uses $O(k^2)$ space, and if its subfunnels of size about $M$ fit in the cache, merging $k^3$ items makes $O\big(k + \frac{k^3}{B} \log_M k\big)$ misses. The recursion of lines L2 and L3 then gives the bound.
- **Optimal on every level.** The bound matches the [I/O lower bound for sorting](/external-sorting-io-lower-bound/) for all $M$ and $B$ at once. With LRU instead of the ideal cache, the bound holds up to a constant factor, as the model page explains.
- **Work.** Each item passes through $\lceil \log_2 k \rceil$ mergers at line L4, with one comparison each. So the merge of line L4 makes about $n \log_2 k \approx \frac13 n \log_2 n$ comparisons, and the recursion gives $O(N \log N)$ comparisons in total.
- **Space.** The funnel of line L4 has buffers of $O(k^2) = O(n^{2/3})$ items, plus the output buffer of $n$ items. Together with the copies of the recursion, the extra space is $\Theta(N)$.

## Properties

- **Stable.** Line L9 takes the left item on ties, the parts of line L2 are in the order of $A$, and line L1 uses a stable sort.
- **Cache-oblivious.** No line uses $M$ or $B$. Only the recursive layout of the funnel makes the misses few.
- **Not in place.** The buffers and the output need $\Theta(N)$ extra space.
- **Not adaptive.** A sorted input costs as much as a random one.

## Variants and improvements

- **Eager $k$-merger.** Frigo et al. define a recursive $k$-merger that outputs exactly $k^3$ items per call, with buffers of $2k^{3/2}$ items between its top and bottom mergers. The lazy form of lines L6 to L9 is simpler to implement and has the same bound.
- **Other parameters.** Brodal and Fagerberg give the lazy funnelsort with a parameter that changes the number of parts and the buffer sizes. It trades a weaker tall-cache assumption, $M = \Omega(B^{1 + \varepsilon})$, for a larger constant in the bound.
- **Engineering.** Brodal, Fagerberg and Vinther tuned lazy funnelsort with a larger base case, mergers with more than two inputs and a careful memory layout. In their experiments it was competitive with good quicksorts in memory and faster than them when the data was on disk.
- **Distribution.** Frigo et al. also give a cache-oblivious distribution sort with the same bound. Funnels are also the core of cache-oblivious distribution sweeping and of cache-oblivious priority queues.

## When to use it

Use funnelsort when data moves through several levels of memory with sizes that the program does not know, or that change, such as caches, main memory and disk at the same time. When the memory size is known, a tuned [external merge sort](/external-merge-sort/) with the full fan-in $M/B - 1$ is simpler and usually faster on disk. In memory, for small arrays, a good quicksort or merge sort is faster in practice, because funnelsort has more overhead per item.

## Pitfalls

- **Base case too small.** Line L1 with a base case of 1 or 2 items makes a funnel for each tiny part, and the overhead per item becomes large. Practical versions use a base case of hundreds of items.
- **Buffers too small.** If line L4 gives the middle buffers much fewer than $k^{3/2}$ items, a bottom funnel runs often for few items, and each run loads it into the cache again. The bound then fails.
- **Layout by levels.** If the nodes of the funnel of line L4 are stored level by level, the nodes of a small subfunnel are far apart in memory. The work is the same, but the misses are much more.
- **Ties to the right.** If line L9 takes the right item on ties, the sort is still correct, but not stable.
- **Exhaustion too early.** Line L8 must test that both child buffers are empty after line L7 has tried to fill them. A node that stops when one child is empty loses the items of the other child.

## Implementations

## History

Frigo, Leiserson, Prokop and Ramachandran defined the cache-oblivious model and funnelsort in 1999, with Prokop's master's thesis at MIT. Brodal and Fagerberg gave lazy funnelsort in 2002, as part of their work on cache-oblivious distribution sweeping. In 2003 they showed that the tall-cache assumption cannot be removed: no cache-oblivious comparison sort is optimal for all $M$ and $B$ without it. Brodal, Fagerberg and Vinther published an engineered implementation and experiments in 2007.

## References
