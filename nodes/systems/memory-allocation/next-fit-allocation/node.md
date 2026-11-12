---
tag: EC8DYH
kind: algorithm
slug: next-fit-allocation
name: Next-fit allocation
aliases:
- roving pointer
- next-fit memory allocation
- first fit with a roving pointer
area: systems/memory-allocation
level: intro
summary: "First fit that starts each search at a roving pointer, where the last search stopped, and wraps around the free list."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {F: the number of blocks on the free list}
  time: {worst: O(F), best: O(1)}
  space: {extra: O(1)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [first-fit-allocation]
see_also: [first-fit-allocation, best-fit-allocation, worst-fit, sequential-fit, external-fragmentation, next-fit-bin-packing, robson-bound]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.5, Dynamic storage allocation, Algorithm A and the exercise on starting the search where the previous one ended (the roving pointer)
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 3.4, Next fit (the roving pointer, and the experiments in which next fit fragments more than best fit or address-ordered first fit) and Section 3.5 (pathologies of LIFO next fit)
  - paper: doi:10.1145/286860.286864
    title: Mark S. Johnstone and Paul R. Wilson, The memory fragmentation problem, solved?, ISMM 1998, 26-36
    locator: Section 2.1.2 (Next fit) and the results for next fit with LIFO, FIFO and address-ordered lists
---

Next-fit allocation is [first-fit allocation](/first-fit-allocation/) with a *roving pointer*: each search starts at the free block where the previous search ended, not at the head of the [free list](/free-list/), and wraps around to the head when it reaches the end. Knuth suggested it in an exercise of TAOCP Section 2.5 to stop small blocks from piling up at the front of the list. It makes the average search shorter, but it spreads the allocations over the whole heap. Wilson, Johnstone, Neely and Boles report experiments with real and synthetic traces in which next fit causes more fragmentation than best fit or address-ordered first fit.

## In plain words

Go back to the shelf with gaps. First fit always starts to look at the left end, so the left end fills with small gaps that slow each walk. Next fit remembers where it put the last box and starts the next walk from there. When it reaches the right end, it goes on from the left end.

So the walks are short, because they do not pass the same small gaps again and again. But the boxes now go everywhere on the shelf. Boxes that arrive together and leave together no longer sit together, and the free space breaks into more pieces.

## The problem

The heap model is the one of [first-fit allocation](/first-fit-allocation/): $H$ words that blocks tile, each block with a header and a footer that hold its size and a used bit, free blocks on a doubly linked list in address order, malloc$(n)$ needs $need = \max(4, n + 2)$ words, and free merges a block with its free neighbours at once. The task is [online memory allocation](/online-memory-allocation/). We count probes (free blocks examined per request) and the number of free blocks, which is a simple sign of fragmentation.

## The algorithm

The rover is a pointer to a block on the free list, or NIL, which means "start at the head". Only the search differs from first fit.

```pseudo id=main
NEXT-FIT-SEARCH(h, need)                   ▷ return a free block, or NIL
L1  ▷ need = max(MIN, n + 2), as in first fit
L2  start ← h.rover if h.rover ≠ NIL else h.head
L3  if start = NIL then return NIL           ▷ the free list is empty
L4  a ← start
L5  loop: if SIZE(a) ≥ need then
L6          h.rover ← a; return a
L7      a ← NEXT(a)
L8      if a = NIL then a ← h.head           ▷ wrap around
L9      if a = start then return NIL         ▷ one full circle, no fit
```

The caller splits the block as in first fit. Two rules keep the rover on the list:

- If the rover block is split, the rover moves to the remainder. So the next search starts just after the block that was given out.
- If the rover block leaves the list, because it was used whole or merged into a neighbour on a free, the rover moves to its successor on the list.

Implementations differ in the second rule. For example, a merge can also move the rover to the merged block. These details change the policy a little, so a description of next fit should state them.

## Example

Use the heap of the first-fit page: $H = 64$ and free blocks $(0, 12), (16, 8), (28, 16), (48, 16)$, written as (start, size). The rover is NIL. Serve malloc(6), malloc(6), malloc(2), malloc(2), with needs 8, 8, 4 and 4.

| request | probes | block used | rover after | free list after |
|---|---|---|---|---|
| malloc(6) | 1 | split (0, 12), payload 1 | 8 | (8, 4) (16, 8) (28, 16) (48, 16) |
| malloc(6) | 2 | all of (16, 8), payload 17 | 28 | (8, 4) (28, 16) (48, 16) |
| malloc(2) | 1 | split (28, 16), payload 29 | 32 | (8, 4) (32, 12) (48, 16) |
| malloc(2) | 1 | split (32, 12), payload 33 | 36 | (8, 4) (36, 8) (48, 16) |

First fit on the same requests puts the third request into the 4-word splinter at address 8 and ends with two free blocks, $(32, 12)$ and $(48, 16)$. Next fit never goes back to the splinter: it ends with three free blocks.

The wrap-around: on the start heap with the rover at 48, malloc(6) splits $(48, 16)$ and the rover moves to 56. Then malloc(10) needs 12 words; $(56, 8)$ is too small, the search wraps to the head and uses all of $(0, 12)$, with 2 probes, and the rover moves to 16.

## Correctness

Next fit keeps the four heap invariants of first fit, because it uses the same split and the same free; they do not depend on which fitting block the search picks. It adds one invariant: the rover is NIL or a block on the free list. A split moves the rover to the remainder, and an unlink moves it to the successor, so the rover never names a block that left the list. The search visits the list as a circle from the rover and stops after one full turn, so it returns the first fitting block in that cyclic order, and it fails only when no free block is large enough. The full proof is below.

## Complexity

- **Search.** At most $F$ probes in the worst case, the same as first fit. When many small blocks gather in one part of the list, next fit passes them once per turn and not once per request, so the average is often much lower.
- **Free.** The same as first fit: $O(1)$ for the merge with [boundary tags](/boundary-tags/), plus $O(F)$ to insert into an address-ordered list.
- **Measured on one trace.** In a heap of $2^{14}$ words, a seeded random trace (seed 3) of 3000 steps, each a free of a random live block or a malloc of 1 to 64 words with equal chance, had 1501 mallocs. First fit used 7527 probes in total, about 5.0 per request, and kept 9.2 free blocks on average. Next fit used 1642 probes, about 1.1 per request, and kept 11.9 free blocks on average. Random traces like this one do not predict real programs well (Wilson et al., Section 2), so take these numbers only as an illustration of the trade.

There is no worst-case bound on fragmentation that is special to next fit; see the [Robson bound](/robson-bound/) for the general bounds.

## Properties

- **Online and deterministic.**
- **More fragmentation in practice.** Wilson et al. report that in several experiments with real traces and with synthetic traces, next fit caused more fragmentation than best fit or address-ordered first fit, and that the LIFO-ordered variant can be much worse than the address-ordered one (Section 3.4). Johnstone and Wilson report that next fit generally increases fragmentation (Section 2.1.2).
- **Poor locality.** The rover cycles through the heap, so objects of different phases of the program end up next to each other, and the rover itself touches each free block once per turn.
- **A known pathology.** With a LIFO list, a loop that allocates a short-lived large object, then a long-lived small one, and then frees the large one, carves a small block out of each freed large block, so memory use grows with the ratio of the sizes (Wilson et al., Section 3.5).

## Variants and improvements

- **List order.** The rover works on an address-ordered, LIFO or FIFO list. The address order is the most studied.
- **K and R malloc.** The allocator in Kernighan and Ritchie's book keeps a circular address-ordered list and a pointer from which each search starts, so it is a next-fit allocator.
- **Trees.** As with first fit, a tree of free blocks can replace the linear list and make the search logarithmic.

## When to use it

Use next fit only when the search time of a linear first-fit list is the main problem and fragmentation does not matter much, or when a ring of blocks of one size is managed, where all fits are equal. For general heaps, address-ordered first fit or [best fit](/best-fit-allocation/) on a faster index gives less fragmentation for the same speed.

Next fit for memory differs from [next-fit bin packing](/next-fit-bin-packing/). The bin-packing rule keeps one open bin and never goes back to a closed one; the memory rule goes back to every free block on the next turn of the rover, and blocks are also freed.

## Pitfalls

- **A rover into a merged block.** When the rover block merges with a neighbour on a free, the rover can point into the middle of the merged block. Move it to a valid list block.
- **An endless loop.** Stop the search when it comes back to its start, not when it reaches NIL, or a failed request loops forever.
- **Assuming it is "first fit, only faster".** It is a different policy, with a different heap layout and more fragmentation.

## Implementations

## History

Knuth described the roving pointer in an exercise of Section 2.5 of the first volume of The Art of Computer Programming, as a change to Algorithm A. Wilson, Johnstone, Neely and Boles reviewed the experiments that compared it with first fit and best fit, and Johnstone and Wilson measured it on real programs in 1998.

## References
