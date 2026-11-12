---
tag: F9XWJQ
kind: algorithm
slug: first-fit-allocation
name: First-fit allocation
aliases:
- first-fit memory allocation
- first-fit storage allocation
- address-ordered first fit
area: systems/memory-allocation
level: intro
summary: "Serve each malloc from the first block on the free list that is large enough. Split off the rest as a new free block."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {F: the number of blocks on the free list, H: the heap size in words}
  time: {worst: O(F), best: O(1)}
  space: {extra: O(1)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [sequential-fit, free-list]
see_also: [next-fit-allocation, best-fit-allocation, worst-fit, coalescing, boundary-tags, knuth-fifty-percent-rule, robson-bound, first-fit-bin-packing]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: "Section 2.5, Dynamic storage allocation: Algorithm A (first-fit method) and its step A4' (do not split off a remainder below a threshold), Algorithm B (liberation with sorted list)"
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 3.4 (Sequential fits, first fit and the order of the free list) and Section 3.5 (list order and policy, splitting)
  - paper: doi:10.1145/286860.286864
    title: Mark S. Johnstone and Paul R. Wilson, The memory fragmentation problem, solved?, ISMM 1998, 26-36
    locator: Section 2.1 (sequential fit algorithms with LIFO, FIFO and address-ordered free lists) and the results on eight real C and C++ programs
  - paper: doi:10.1145/800217.806613
    title: C. J. Stephenson, New methods for dynamic storage allocation (Fast Fits), SOSP 1983, 30-32
    locator: the Cartesian tree of free blocks that finds the leftmost fit in logarithmic time on a balanced tree
---

First-fit allocation is the [sequential fit](/sequential-fit/) policy that serves a request for $n$ words from the first block on the [free list](/free-list/) that is large enough. If the block is larger than needed, the allocator splits it: it gives out one part and keeps the rest on the list as a smaller free block. When the list is kept in address order, first fit always uses the free block of lowest address that fits. A search looks at up to $F$ blocks, where $F$ is the length of the free list, and the policy has no worst-case guarantee on [fragmentation](/external-fragmentation/) better than the general [Robson bound](/robson-bound/). On real program traces, address-ordered first fit wastes little memory.

## In plain words

Think of a long shelf with some gaps between the boxes. A new box arrives. You walk along the shelf from the left end, and you put the box in the first gap that is wide enough. If the gap is wider than the box, a smaller gap stays next to it. When a box leaves, its space becomes a gap again, and you join it with any gap next to it.

First fit does not look for the best gap. It takes the first one that works. This keeps the search short when a good gap is near the start. Over time, the start of the shelf fills with small gaps that no box fits, and each search must walk past them.

## The problem

The allocator manages a heap of $H$ words, $mem[0 \ldots H-1]$, under the [allocator](/allocator/) interface: malloc$(n)$ returns the address of $n$ free words, and free$(p)$ gives back an earlier result. Requests arrive one at a time and must be answered at once, and a live block can never move. This is the [online memory allocation](/online-memory-allocation/) problem.

The heap model of this page, used on all the pages of this group:

- The heap is a sequence of blocks that tile $[0, H)$. A block at address $a$ with $s$ words has a *header* $mem[a]$ and a *footer* $mem[a + s - 1]$, both equal to $2s + u$, where $u = 1$ means used. These are [boundary tags](/boundary-tags/).
- A free block keeps its list links in its own words: NEXT in $mem[a+1]$ and PREV in $mem[a+2]$. So the smallest block is $MIN = 4$ words.
- malloc$(n)$ needs a block of $need = \max(MIN, n + 2)$ words, because of the header and the footer. It returns the payload address $a + 1$.
- free merges the block at once with each free neighbour. This is immediate [coalescing](/coalescing/).

We measure the search time as the number of free blocks that a search examines (the *probes*), the space overhead as 2 words per block, and the fragmentation of the free space.

## The algorithm

The search is lines L2 to L5. The rest is the split, which all sequential fit policies share.

```pseudo id=main
FIRST-FIT-MALLOC(h, n)                     ▷ return a payload address, or NIL
L1  need ← max(MIN, n + 2)
L2  a ← h.head
L3  while a ≠ NIL and SIZE(a) < need do
L4      a ← NEXT(a)
L5  if a = NIL then return NIL
L6  s ← SIZE(a)
L7  if s − need ≥ MIN then                 ▷ split, the low part is used
L8      r ← a + need; TAG(r, s − need, free); r takes the list place of a
L9      TAG(a, need, used)
L10 else unlink a; TAG(a, s, used)          ▷ the whole block, no tiny remainder
L11 return a + 1
```

Line L7 is Knuth's step A4': a remainder smaller than $MIN$ cannot hold the links of a free block, so the request gets the whole block, and the few extra words become [internal fragmentation](/internal-fragmentation/). Line L8 keeps the remainder at the list place of the old block, so the address order of the list stays correct with no list search. Knuth's Algorithm A gives out the *upper* end of the block instead, so that the remainder keeps the old list node; the policy is the same, only the address of the result changes.

FREE$(p)$ marks the block free, merges it with a free left or right neighbour, and links the result into the list. With an address-ordered list, the link step walks the list to find the place; with a LIFO list it pushes the block at the head in $O(1)$. The [coalescing](/coalescing/) page has the details.

## Example

Take $H = 64$. Allocate $n = 10, 2, 6, 2, 14, 2$ (blocks of 12, 4, 8, 4, 16 and 4 words at 0, 12, 16, 24, 28 and 44), then free the first, third and fifth. The free list, in address order, is $(0, 12), (16, 8), (28, 16), (48, 16)$, written as (start, size). Now serve four requests with first fit.

| request | need | probes | block used | free list after |
|---|---|---|---|---|
| malloc(6) | 8 | 1 | split (0, 12), payload 1 | (8, 4) (16, 8) (28, 16) (48, 16) |
| malloc(6) | 8 | 2 | all of (16, 8), payload 17 | (8, 4) (28, 16) (48, 16) |
| malloc(2) | 4 | 1 | all of (8, 4), payload 9 | (28, 16) (48, 16) |
| malloc(10) | 12 | 1 | split (28, 16), payload 29 | (40, 4) (48, 16) |

The first request split the 12-word block at address 0 and left a 4-word splinter at the front of the list. The second request had to step over it. The third request was lucky and fit the splinter exactly. Then free(17) gives back $(16, 8)$; both neighbours are used, so the list becomes $(16, 8), (40, 4), (48, 16)$. free(29) gives back $(28, 12)$, which merges with the free block $(40, 4)$ on its right into $(28, 16)$.

## Correctness

The proof keeps four invariants between operations: the blocks tile $[0, H)$ with matching header and footer; the free list holds each free block exactly once, with consistent links and in address order; no two free blocks are adjacent; and each live pointer lies in a used block of at least $n + 2$ words. The search returns the first block in list order with $SIZE \ge need$, because each block before it was tested and was too small. A split replaces one free block by a used block and a free block inside the same words, and the remainder keeps the list place. The full proof is below.

## Complexity

- **Search.** At most $F$ probes, where $F$ is the number of free blocks, so $O(F)$ in the worst case and $O(1)$ when the first block fits. Since free blocks are not adjacent, $F$ is at most one more than the number of used blocks.
- **Split and unlink.** $O(1)$ with a doubly linked list.
- **Free.** $O(1)$ to merge, with boundary tags. Inserting into an address-ordered list costs $O(F)$ more; a LIFO list needs $O(1)$.
- **Space.** 2 words per block for the tags, and blocks of at least 4 words.

The worst-case bounds on the heap size that first fit needs, for a given amount of live data and a given ratio of the largest to the smallest block, are on the [Robson bound](/robson-bound/) page. They are far above what real programs need. For random requests and random frees in equilibrium, the [fifty-percent rule](/knuth-fifty-percent-rule/) predicts about half as many free blocks as used blocks, which bounds the expected list length.

## Properties

- **Online and deterministic.** Each decision uses only the current heap.
- **Splinters gather at the front.** First fit splits the blocks near the head of the list first, so small free blocks pile up there and each later search must step over them (Wilson et al., Section 3.4).
- **The list order is part of the policy.** With an address-ordered list, first fit packs the low end of the heap. With a LIFO list, it reuses the block freed most recently. Wilson et al. report that in experiments with real and synthetic traces, address-ordered first fit can cause much less fragmentation than LIFO-ordered first fit, and that a FIFO order may work about as well as the address order (Section 3.4).
- **Good on real programs.** Johnstone and Wilson measured eight real C and C++ programs. Address-ordered first fit and best fit had almost no fragmentation once the costs of headers and alignment were counted apart.

## Variants and improvements

- **Next fit.** Start each search where the last one stopped. See [next-fit allocation](/next-fit-allocation/).
- **Best fit and worst fit.** Choose the smallest or the largest block that fits. See [best-fit allocation](/best-fit-allocation/) and [worst fit](/worst-fit/).
- **A tree of free blocks.** A [Cartesian tree](/cartesian-tree/) keyed by address and heap-ordered by size finds the leftmost fit by walking down the tree. Stephenson's "fast fits" uses this; the search is logarithmic when the tree is balanced.
- **Segregated lists.** Keep a list per size range, as in [segregated free lists](/segregated-free-lists/), and search only the lists that can fit. This approximates first fit or best fit with a short search.
- **Splitting threshold.** Do not split when the remainder is smaller than a threshold larger than $MIN$. Wilson et al. report that this does not appear to help in practice unless the threshold is very small (Section 3.5).

## When to use it

Use address-ordered first fit when the heap is small or the free list is short, and you want a simple allocator with low fragmentation. For a large heap with many free blocks, use the same policy with a tree or segregated lists, or move to [size classes](/size-classes/) as production allocators such as [dlmalloc](/dlmalloc/) do.

First fit here is a different problem from [first-fit bin packing](/first-fit-bin-packing/). In bin packing, items never leave, bins have a fixed capacity, and the goal is the number of bins. In memory allocation, blocks are freed in any order, the position of a block matters, and the goal is to serve each request inside one fixed heap.

## Pitfalls

- **Forgetting the header in the size.** The block needs $n + 2$ words in this model, not $n$. A search on $n$ returns blocks that are too small.
- **Leaving a tiny remainder.** A remainder smaller than $MIN$ cannot hold a header, a footer and two links. Give the whole block instead.
- **Losing the list order on a split.** In an address-ordered list, put the remainder at the place of the old block. Pushing it at the head breaks the order and changes the policy.
- **Treating NIL as "out of memory".** malloc can fail while the total free space is larger than the request. That is fragmentation, and the caller should know the difference.
- **Long searches.** A linear list scales badly when many splinters gather at the front. Measure the probes per request on your workload.

## Implementations

## History

Knuth gave first fit as Algorithm A in Section 2.5 of the first volume of The Art of Computer Programming (1968), in the same section as best fit, the boundary tag method and the buddy system. The order of the free list was studied later; Wilson, Johnstone, Neely and Boles separated the policy from the mechanism in their 1995 survey, and Johnstone and Wilson's 1998 trace study found address-ordered first fit among the policies with the least fragmentation.

## References
