---
tag: 342B4P
kind: algorithm
slug: cole-merge-sort
name: Cole's parallel merge sort
aliases:
- Cole merge sort
- Cole's pipelined merge sort
- pipelined parallel merge sort
area: sorting/parallel-sorting
level: research
summary: Pipelined merge sort that sorts n keys in O(log n) time with n processors and O(n log n) work on a PRAM.
solves: [parallel-sorting-problem]
model: crew-pram
complexity:
  vars: {n: the number of keys}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
  depth: {worst: Θ(log n)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [merge-sort, parallel-merging-problem, parallel-merge-sort, crew-pram, work-span-model]
see_also: [parallel-merge-sort, parallel-sorting-depth-lower-bound, aks-sorting-network, valiant-parallel-merge, shiloach-vishkin-merge, merge-path, erew-pram, brent-theorem]
sources:
  - paper: doi:10.1137/0217049
    title: Richard Cole, Parallel merge sort, SIAM Journal on Computing 17(4), 1988
    locator: the CREW algorithm (sampling every fourth, second and every item, the merge with the cover property, and the upkeep of ranks), the 3-cover lemma, and the EREW version
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 4, Searching, merging and sorting, the section on Cole's pipelined merge sort
  - paper: "Miklós Ajtai, János Komlós and Endre Szemerédi, An O(n log n) sorting network, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC), 1983"
    locator: the first deterministic parallel sort in O(log n) time with n processors
---

Cole's merge sort sorts $n$ keys on the [CREW PRAM](/crew-pram/) in $O(\log n)$ time with $n$ processors, so its work is $O(n \log n)$. It runs merge sort on a complete binary tree, but it does not wait for a merge to finish before the next level starts. Each node sends samples of its partial result up to its parent, every fourth item, then every second, then all of them. Because each new sample is close to the last one, every merge step at a node takes constant time. Apart from the AKS sorting network, it was the first deterministic sort that matches the $\Omega(\log n)$ [depth lower bound](/parallel-sorting-depth-lower-bound/), and Cole also gave a version for the [EREW PRAM](/erew-pram/) with the same bounds.

## In plain words

Picture a knockout tree of helpers. Each leaf helper holds one card. Each helper above merges the sorted piles of two helpers below.

In an ordinary parallel merge sort, a helper waits until both piles below are complete. Here, nobody waits. Each helper often passes up a rough preview of the pile it has so far: one card out of every four. The helper above merges the two previews it gets. When a helper's pile is complete, it passes up one card in four, then one in two, and then every card.

Each new preview is only a little finer than the previous one. So a helper can put each new card into place by looking at a few cards near where the previous preview put it. Each round then takes the same short time, and the number of rounds grows only with the height of the tree.

## The problem

The input is $n$ keys from a total order in an array, and the output is the same keys in non-decreasing order. This is the [parallel sorting problem](/parallel-sorting-problem/) on the CREW PRAM, where processors may read the same cell at the same time but must write to different cells. The goal is $O(\log n)$ time with $O(n)$ processors.

## The algorithm

Let $n = 2^k$ (pad with keys larger than all others otherwise), and make all keys distinct by breaking ties with the input index. Use a complete binary tree with the keys at its leaves. For a node $v$ of height $h$, let $L(v)$ be the sorted list of the $2^h$ keys below $v$. Each node keeps a sorted list $\mathrm{UP}(v)$, a subset of $L(v)$. Node $v$ is *full* when $\mathrm{UP}(v) = L(v)$. In each stage, every live node forms a sample $\mathrm{SUP}(v)$ of $\mathrm{UP}(v)$, and every node $u$ with children $x, y$ forms $\mathrm{NEWUP}(u) = \mathrm{SUP}(x) \cup \mathrm{SUP}(y)$. "Every fourth item" means the items at positions $4, 8, 12, \ldots$, counted from 1.

```pseudo id=main
COLE-MERGE-SORT(A[0 … n − 1]), n = 2^k
L1  for each leaf v with key A[i]: UP(v) ← [A[i]]; v is full at stage 0
L2  for t ← 1 to 3k do
L3      parallel for each node v that is not full, or became full at stage t − 1, t − 2 or t − 3:
L4          if v is not full: SUP(v) ← every fourth item of UP(v)
L5          else: SUP(v) ← every fourth, every second, or every item of UP(v), when v became full at stage t − 1, t − 2 or t − 3
L6      parallel for each node u that is not full, with children x and y, and each item e of SUP(x): take the items d < e ≤ f of UP(u) next to e
L7          find the rank of e in SUP(y) among the at most 3 items of SUP(y) in [d, f)
L8          NEWUP(u)[rank of e in SUP(x) + rank of e in SUP(y)] ← e; do the same for each item of SUP(y)
L9      update the ranks of UP(u) in SUP(x) and SUP(y), and of SUP(x) and SUP(y) in UP(u), for the next stage
L10     parallel for each such u: UP(u) ← NEWUP(u); u is full if |UP(u)| = 2^height(u)
L11 return UP(root)
```

Lines L6 to L8 need the rank of $e$ in $\mathrm{UP}(u)$ and the ranks of the items of $\mathrm{UP}(u)$ in $\mathrm{SUP}(y)$. These are the ranks that line L9 keeps. Cole shows how to compute them for stage $t + 1$ from those of stage $t$ in $O(1)$ time with one processor per item, using the same cover property one level down.

## Example

Sort $[42, 7, 93, 25, 60, 12, 88, 3]$, so $k = 3$ and there are 9 stages. The tree has the root $1$, its children $2$ and $3$, and the nodes $4, 5, 6, 7$ of height 1 above the leaves. Only the stages in which some list changes are shown.

| stage | samples sent up | new UP lists |
| --- | --- | --- |
| 3 | each leaf sends its key | $\mathrm{UP}(4) = [7, 42]$, $\mathrm{UP}(5) = [25, 93]$, $\mathrm{UP}(6) = [12, 60]$, $\mathrm{UP}(7) = [3, 88]$, all full |
| 5 | every second item of 4, 5, 6, 7: $[42], [93], [60], [88]$ | $\mathrm{UP}(2) = [42, 93]$, $\mathrm{UP}(3) = [60, 88]$ |
| 6 | all items of 4, 5, 6, 7 | $\mathrm{UP}(2) = [7, 25, 42, 93]$, $\mathrm{UP}(3) = [3, 12, 60, 88]$, both full |
| 7 | every fourth item of 2, 3: $[93], [88]$ | $\mathrm{UP}(1) = [88, 93]$ |
| 8 | every second item of 2, 3: $[25, 93], [12, 88]$ | $\mathrm{UP}(1) = [12, 25, 88, 93]$ |
| 9 | all items of 2, 3 | $\mathrm{UP}(1) = [3, 7, 12, 25, 42, 60, 88, 93]$, full |

In stages 1, 2 and 4 the samples are empty, because a list of one or two items has no fourth item, and a list of one item has no second item. Take stage 9 at the root, and $e = 42$ from $\mathrm{SUP}(2)$. The current $\mathrm{UP}(1) = [12, 25, 88, 93]$ has 2 items below $42$, so $d = 25$ and $f = 88$. In $\mathrm{SUP}(3) = [3, 12, 60, 88]$, the items below $25$ are 2, and the only item in $[25, 88)$ is $60$. One comparison shows $60 > 42$, so the rank of $42$ in $\mathrm{SUP}(3)$ is 2. Its rank in $\mathrm{SUP}(2)$ is 2, so it goes to position $2 + 2 = 4$ of the output.

## Correctness

Every list $\mathrm{UP}(v)$ and $\mathrm{SUP}(v)$ is a sorted subset of $L(v)$, and since the keys are distinct, lines L6 to L8 place each item at its rank in the union, which gives the sorted union. Line L7 finds the correct rank whatever the number of candidates, because all items of $\mathrm{SUP}(y)$ below $d$ are below $e$, and all items from $f$ on are above $e$. By induction on the height $h$, a node of height $h$ becomes full at exactly stage $3h$: its children are full at stage $3h - 3$, and in the three stages after that they send every fourth item, every second item and all of their items, so at stage $3h$ the node receives $L(x) \cup L(y) = L(v)$. Before that stage its list is too short to be full. So the root is full after stage $3k$. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

All bounds are for the CREW PRAM.

**Stages.** There are $3k = 3 \lg n$ stages.

**Time per stage.** Cole's 3-cover lemma says that the sample $\mathrm{SUP}(v)$ of the previous stage is a 3-cover of the new $\mathrm{SUP}(v)$: between two items next to each other in the old sample, with $-\infty$ and $+\infty$ added at the ends, there are at most 3 items of the new sample. Since $\mathrm{UP}(u)$ is the union of the old samples of $x$ and $y$, it is also a 3-cover of the new $\mathrm{SUP}(y)$, so line L7 makes at most 3 comparisons. Line L9 also takes $O(1)$ time per item, by Cole's construction. So each stage takes $O(1)$ time with one processor per item of the lists in use.

**Number of items.** For a node $v$ of height $h$ that is not yet full at stage $t \le 3h$, $|\mathrm{UP}(v)| \le 2^h \cdot 8^{t/3 - h}$, so the lists shrink by a factor 8 per level above the full nodes. Summed over the nodes of one height, this is at most $n \cdot 8^{t/3 - h}$, so the nodes that are not yet full hold at most $\frac{8}{7} n$ items in all. The full nodes that still send samples have heights in a range of at most two values, and they hold at most $2n$ items. So the lists in use at one stage hold $O(n)$ items. So $O(n)$ processors suffice, and the time is $O(\log n)$.

**Work.** The work is $O(n)$ per stage, $O(n \log n)$ in all, which matches the [comparison sorting lower bound](/comparison-sort-lower-bound/). By [Brent's theorem](/brent-theorem/), $p \le n$ processors take time $O((n \log n)/p + \log n)$.

**Space.** The lists in use hold $O(n)$ items, and the ranks take $O(n)$ more cells.

## Properties

- **Optimal.** Time $O(\log n)$ with $n$ processors matches the [depth lower bound](/parallel-sorting-depth-lower-bound/) for the CREW and EREW PRAM, and the work matches the sequential bound.
- **Deterministic.** No random choices are made.
- **Stable with tie-breaking.** Ties are broken by input index, so the output is stable.
- **Not oblivious.** Which cells are read depends on the keys, so it is not a [sorting network](/sorting-network/).
- **Pipelined.** At any stage, nodes of about $k - t/3$ different heights do useful work.

## Variants and improvements

- **EREW version.** Cole's paper also gives a version without concurrent reads, with the same $O(\log n)$ time and $n$ processors. It needs more care, because many items may look up the same rank.
- **Cascading divide and conquer.** Atallah, Cole and Goodrich used the same pipelining with covers for geometric problems on the PRAM, where each node of a tree must merge or search lists that come from its children.
- **Sorting networks.** The [AKS network](/aks-sorting-network/) also sorts in $O(\log n)$ depth, and it is oblivious, but its constant is much larger. Cole's constant is moderate.
- **Practical sorts.** For real machines, [sample sort](/sample-sort/) and [merge path](/merge-path/) based merge sorts are simpler and faster, and the $O(\log^2 n)$ or $O(\log^3 n)$ span of [parallel merge sort](/parallel-merge-sort/) is rarely the limit.

## When to use it

Use Cole's merge sort as the reference that sorting is possible in $O(\log n)$ PRAM time with optimal work, for example in the analysis of other PRAM algorithms that call a sort. Do not use it to sort on real hardware: the constant factors and the bookkeeping of ranks make it slower than [sample sort](/sample-sort/) or [parallel merge sort](/parallel-merge-sort/) on any machine of today.

## Pitfalls

- **Wrong sampling schedule.** Taking every fourth item of a full node at all three stages, or skipping the stage with every second item, breaks the 3-cover property, and line L7 then needs more than a constant number of comparisons.
- **Equal keys.** The ranks in lines L6 to L8 assume distinct keys. Without the tie-break by index, two equal items can get the same output position.
- **Stale ranks.** Line L9 must use the ranks of the previous stage. Recomputing them by binary search costs $O(\log n)$ per stage and gives total time $O(\log^2 n)$.
- **Counting positions from 0.** "Every fourth item" starts at the fourth item, not the first. Starting at the first item changes the sizes of the samples and the stage at which a node becomes full.

## Implementations

## History

Cole published the algorithm in 1986 at FOCS and in the SIAM Journal on Computing in 1988. Before it, the only deterministic sort in $O(\log n)$ time with $n$ processors was the AKS sorting network of 1983, with a very large constant. Cole's idea of pipelining the merges through the tree, with samples that cover each other, was later used for other problems on the PRAM.

## References
