---
tag: DY2NDA
kind: algorithm
slug: best-fit-allocation
name: Best-fit allocation
aliases:
- best-fit memory allocation
- best-fit storage allocation
- address-ordered best fit
area: systems/memory-allocation
level: intro
summary: "Serve each malloc from the smallest free block that is large enough. A size-ordered tree finds it in logarithmic time."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {F: the number of blocks on the free list}
  time: {worst: O(F), best: O(1), indexed: O(log F)}
  space: {extra: O(1), indexed: O(F)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [first-fit-allocation, balanced-binary-search-tree]
see_also: [first-fit-allocation, worst-fit, next-fit-allocation, external-fragmentation, robson-bound, segregated-free-lists, red-black-tree, best-fit-bin-packing]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.5, Dynamic storage allocation, the best-fit method and its comparison with the first-fit method
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 3.4, Best fit (the cost of the search and the poor worst case) and Section 3.8 (indexed fits, balanced and splay trees)
  - paper: doi:10.1145/286860.286864
    title: Mark S. Johnstone and Paul R. Wilson, The memory fragmentation problem, solved?, ISMM 1998, 26-36
    locator: Section 2.1 (best fit with a tree of lists of blocks of one size) and the results on eight real C and C++ programs
---

Best-fit allocation is the [sequential fit](/sequential-fit/) policy that serves a request from the *smallest* free block that is large enough. It splits that block as [first fit](/first-fit-allocation/) does. The idea is to keep large blocks whole for later large requests and to leave only small remainders. A plain scan of the [free list](/free-list/) must look at every free block, so it costs $O(F)$ probes. An index ordered by size, such as a [balanced binary search tree](/balanced-binary-search-tree/) keyed on (size, address), finds the same block in $O(\log F)$ time. On real programs best fit is among the policies with the least fragmentation, but its worst case is poor; see the [Robson bound](/robson-bound/).

## In plain words

Go back to the shelf with gaps. First fit puts a box in the first gap that is wide enough. Best fit looks at all the gaps and picks the narrowest one that still holds the box. A wide gap stays wide, so a big box that comes later still has a place.

The price is the walk. To know which gap is the narrowest, you must see all of them, unless you keep a list of the gaps sorted by width. The other risk is the leftover: the narrowest gap often leaves a sliver that is too thin for any box.

## The problem

The heap model is the one of [first-fit allocation](/first-fit-allocation/): $H$ words that blocks tile, each block with a header and a footer that hold its size and a used bit, free blocks on a doubly linked list in address order, malloc$(n)$ needs $need = \max(4, n + 2)$ words, and free merges a block with its free neighbours at once. The task is [online memory allocation](/online-memory-allocation/). We count probes and the number of free blocks.

## The algorithm

```pseudo id=main
BEST-FIT-MALLOC(h, n)                      ▷ return a payload address, or NIL
L1  need ← max(MIN, n + 2)
L2  best ← NIL; a ← h.head
L3  while a ≠ NIL do
L4      if SIZE(a) ≥ need and (best = NIL or SIZE(a) < SIZE(best)) then
L5          best ← a
L6          if SIZE(a) = need then break    ▷ an exact fit cannot be beaten
L7      a ← NEXT(a)
L8  if best = NIL then return NIL
L9  split best as in first fit, lines L6 to L10
L10 return best + 1
```

The strict test in line L4 keeps the first block of the least size, which is the lowest address on an address-ordered list. Line L6 stops at an exact fit, which is a common case for programs that allocate many objects of one size.

**The indexed version.** Keep the free blocks also in an ordered set keyed on the pair (size, address). The best fit is the *successor* of $(need, -\infty)$: the first pair whose size is at least $need$. A [red-black tree](/red-black-tree/) or an [AVL tree](/avl-tree/) gives the search, the insert and the delete in $O(\log F)$ time. Each link, unlink and split of the free list updates the tree. The result is the same block as the list scan on an address-ordered list. The code below uses a sorted array with binary search as the ordered set; it makes the same $O(\log F)$ comparisons, but each update moves $O(F)$ entries, so a production allocator uses a tree.

## Example

Use the heap of the first-fit page: $H = 64$ and free blocks $(0, 12), (16, 8), (28, 16), (48, 16)$, written as (start, size). Serve malloc(6), malloc(2), malloc(10) and malloc(12), with needs 8, 4, 12 and 14.

| request | probes | block used | free list after |
|---|---|---|---|
| malloc(6) | 2 | all of (16, 8), an exact fit, payload 17 | (0, 12) (28, 16) (48, 16) |
| malloc(2) | 3 | split (0, 12), payload 1 | (4, 8) (28, 16) (48, 16) |
| malloc(10) | 3 | split (28, 16), payload 29 | (4, 8) (40, 4) (48, 16) |
| malloc(12) | 3 | all of (48, 16), payload 49 | (4, 8) (40, 4) |

The first request finds the exact fit at the second block and stops. First fit would split the 12-word block at address 0 instead and leave a 4-word splinter at the front. The last request uses all of $(48, 16)$, because a remainder of 2 words is below $MIN$; those 2 words are [internal fragmentation](/internal-fragmentation/).

## Correctness

Best fit uses the same split and the same free as first fit, so it keeps the same four heap invariants: the blocks tile the heap, the free list holds exactly the free blocks, no two free blocks are adjacent, and each live pointer lies in a large enough used block. The scan keeps the first block of the least fitting size seen so far, and an exact fit is the least size possible, so the early stop is safe. In the indexed version, every change of the free list also changes the index, so the index is always the sorted set of (size, address) pairs, and its first pair with size at least $need$ is the same block. The full proof is below.

## Complexity

- **List scan.** $O(F)$ probes per request, because the scan must see every block unless it finds an exact fit. With a LIFO list the insert on free is $O(1)$; with an address-ordered list it is $O(F)$.
- **Indexed.** $O(\log F)$ for the search, the insert and the delete with a balanced tree, and $O(F)$ extra space for the tree. In a real allocator the tree nodes live inside the free blocks, so a free block must be large enough to hold them.
- **Measured on one trace.** On the seeded random trace of the [next-fit page](/next-fit-allocation/) (a heap of $2^{14}$ words, seed 3, 1501 requests of 1 to 64 words), first fit kept 9.2 free blocks on average and used 7527 probes. Best fit with a list scan kept 7.3 free blocks on average and used 10345 probes, about 6.9 per request. The indexed version made the same choices with 4298 comparisons, about 2.9 per request.

## Properties

- **Online and deterministic.**
- **Low fragmentation in practice.** Johnstone and Wilson measured eight real C and C++ programs. Best fit and address-ordered first fit had almost no fragmentation once the costs of headers and alignment were counted apart.
- **A poor worst case.** For some request sequences best fit needs a heap much larger than the live data, and the bound grows with the ratio of the largest to the smallest request. The [Robson bound](/robson-bound/) page gives the bounds; this page does not repeat them.
- **Small remainders.** The remainder of a split is as small as possible. Many of these remainders are too small for any later request (Wilson et al., Section 3.4).
- **Not always better than first fit.** On a given trace, either policy can fail where the other succeeds. The [worst-fit](/worst-fit/) page shows such traces by code.

## Variants and improvements

- **Tree of lists.** Keep one list for each size, and a tree of the distinct sizes. Standish described this layout, and Johnstone and Wilson used it for their best-fit allocator.
- **Splay trees and Cartesian trees.** A [splay tree](/splay-tree/) keyed by size adapts to repeated sizes. A [Cartesian tree](/cartesian-tree/) keyed by address and heap-ordered by size, as in Stephenson's fast fits, supports first fit and best fit searches.
- **Segregated fits.** [Segregated free lists](/segregated-free-lists/) with [size classes](/size-classes/) give a close approximation of best fit with a short search. Many production allocators do this.
- **A splitting threshold.** Give the whole block if the remainder would be below a threshold. This turns some external fragmentation into internal fragmentation.

## When to use it

Use best fit when memory is tight and fragmentation matters more than the time of one request, and back it with a size-ordered index so the search does not grow with the heap. When most requests come in a few sizes, segregated lists are faster and nearly as good. A linear best-fit scan suits only small heaps.

Best fit here is a different problem from [best-fit bin packing](/best-fit-bin-packing/). In bin packing, items never leave, the bins have a fixed capacity, and the goal is the number of bins. In memory allocation, blocks are freed in any order, the address of a block matters, and the goal is to serve each request inside one fixed heap.

## Pitfalls

- **A linear scan on a large heap.** The scan touches every free block on almost every request. Use an index.
- **Ties.** The tie rule is part of the policy. With an address-ordered list and a strict comparison, ties go to the lowest address; with a LIFO list they go to the block freed last. Write the rule down and test it.
- **A stale index.** Every split, merge and unlink must update the index in the same step as the list. A missed update gives a block that is no longer free.
- **The header in the size.** The search key is $n + 2$ words, not $n$.

## Implementations

## History

Knuth discussed best fit next to first fit in Section 2.5 of the first volume of The Art of Computer Programming (1968), and noted that first fit can do better on some sequences even though best fit seems the natural choice. Trees of free blocks indexed by size made the search logarithmic. Wilson, Johnstone, Neely and Boles surveyed the results in 1995, and Johnstone and Wilson's 1998 trace study found best fit among the policies with the least fragmentation on real programs.

## References
