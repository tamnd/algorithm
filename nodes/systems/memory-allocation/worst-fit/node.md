---
tag: VRPHKK
kind: algorithm
slug: worst-fit
name: Worst fit
aliases:
- worst-fit allocation
- worst-fit memory allocation
area: systems/memory-allocation
level: intro
summary: "Serve each malloc from the largest free block, so that the remainder stays large. It fragments badly in practice."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {F: the number of blocks on the free list}
  time: {worst: O(F), indexed: O(log F)}
  space: {extra: O(1)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [best-fit-allocation]
see_also: [best-fit-allocation, first-fit-allocation, next-fit-allocation, external-fragmentation, sequential-fit, robson-bound]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.5, Dynamic storage allocation, the discussion of first fit and best fit
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 3.5, Worst fit (it works quite badly in synthetic trace studies, probably because it ensures that no very large blocks stay available)
---

Worst fit is the [sequential fit](/sequential-fit/) policy that serves each request from the *largest* free block. The idea is the reverse of [best fit](/best-fit-allocation/): after a split, the remainder is as large as possible, so it is less likely to be a useless splinter. In practice the idea fails. Worst fit cuts into the largest block on almost every request, so soon no large block is left, and a large request fails while the total free space is still large. Wilson, Johnstone, Neely and Boles report that worst fit seems to work quite badly in synthetic trace studies.

## In plain words

Go back to the shelf with gaps. Worst fit always puts the new box into the widest gap. The hope is that the gap that stays next to the box is still wide enough for another box.

But every box goes into the widest gap, so the widest gap shrinks again and again. After a while, all gaps have about the same middle width. Then a big box arrives, and no gap holds it, even though the gaps together have plenty of room.

## The problem

The heap model is the one of [first-fit allocation](/first-fit-allocation/): $H$ words that blocks tile, each block with a header and a footer that hold its size and a used bit, free blocks on a doubly linked list in address order, malloc$(n)$ needs $need = \max(4, n + 2)$ words, and free merges a block with its free neighbours at once. The task is [online memory allocation](/online-memory-allocation/). We count probes, the number of free blocks and the size of the largest free block.

## The algorithm

```pseudo id=main
WORST-FIT-MALLOC(h, n)                     ▷ return a payload address, or NIL
L1  need ← max(MIN, n + 2)
L2  best ← NIL; a ← h.head
L3  while a ≠ NIL do
L4      if SIZE(a) ≥ need and (best = NIL or SIZE(a) > SIZE(best)) then
L5          best ← a
L6      a ← NEXT(a)
L7  if best = NIL then return NIL
L8  split best as in first fit, lines L6 to L10
L9  return best + 1
```

The strict test in line L4 keeps the first largest block, which is the lowest address on an address-ordered list. The scan can never stop early. With a max-heap or a size-ordered tree of the free blocks, the largest block is found in $O(1)$ or $O(\log F)$ time, and each update costs $O(\log F)$.

## Example

Use the heap of the first-fit page: $H = 64$ and free blocks $(0, 12), (16, 8), (28, 16), (48, 16)$, written as (start, size). Serve malloc(6), malloc(2), malloc(10) and malloc(12), with needs 8, 4, 12 and 14.

| request | probes | block used | free list after |
|---|---|---|---|
| malloc(6) | 4 | split (28, 16), payload 29 | (0, 12) (16, 8) (36, 8) (48, 16) |
| malloc(2) | 4 | split (48, 16), payload 49 | (0, 12) (16, 8) (36, 8) (52, 12) |
| malloc(10) | 4 | all of (0, 12), payload 1 | (16, 8) (36, 8) (52, 12) |
| malloc(12) | 3 | none, it fails | (16, 8) (36, 8) (52, 12) |

The last request fails with 28 free words, because worst fit cut both 16-word blocks. [Best fit](/best-fit-allocation/) serves the same four requests and ends with free blocks $(4, 8)$ and $(40, 4)$.

**Neither policy wins on every trace.** Take $H = 28$ with free blocks $(0, 8)$ and $(12, 12)$, separated by used blocks of 4 words.

- Needs 4 then 12, that is malloc(2), malloc(10). Best fit puts the 4 into the 8-word block and the 12 into the 12-word block. Worst fit puts the 4 into the 12-word block, leaves 8 and 8, and the 12 fails.
- Needs 4, 8 and 8, that is malloc(2), malloc(6), malloc(6). Best fit leaves remainders of 4 and 4 words, and the third request fails. Worst fit leaves 8 and 8 and serves all three.
## Correctness

Worst fit uses the same split and the same free as first fit, so it keeps the four heap invariants of that page. The scan keeps the first block of the largest fitting size seen so far. If the largest block does not fit, nothing does, so a NIL result means that the request cannot be served by any policy on this heap. The full proof is below.

## Complexity

- **List scan.** Exactly $F$ probes per request, since the scan cannot stop early.
- **Indexed.** $O(\log F)$ per request and per update with a balanced tree or a heap ordered by size.
- **Measured on one trace.** On the seeded random trace of the [next-fit page](/next-fit-allocation/) (a heap of $2^{14}$ words, seed 3, 1501 requests of 1 to 64 words), first fit and best fit ended with a largest free block of 13246 and 13313 words, out of about 14140 free words. Worst fit ended with a largest free block of 3151 words out of 14159. It also kept 12.0 free blocks on average, against 9.2 for first fit and 7.3 for best fit, and used 17974 probes, about 12 per request.

## Properties

- **Online and deterministic.**
- **It destroys large blocks.** Each request cuts the largest block, so the largest free block shrinks quickly. This is the probable reason for its poor results (Wilson et al., Section 3.5).
- **Free blocks of similar size.** Worst fit tends to leave many middle-sized blocks. That is good for many requests of one middle size and bad for any large request.
- **Not dominated.** On some traces it succeeds where best fit fails, as the example shows. In measured studies it is still worse on average.

## Variants and improvements

- **Indexed worst fit.** A max-heap of free blocks by size makes the search $O(1)$ and each update $O(\log F)$.
- **Almost worst fit.** In bin packing, a rule that picks the second largest gap has a better bound than worst fit. For memory allocation it has no clear benefit.
- **Splitting threshold.** As with the other fits, give the whole block when the remainder would be small.

## When to use it

Almost never for a general heap. Use [first fit](/first-fit-allocation/) on an address-ordered list or [best fit](/best-fit-allocation/) on an index instead. Worst fit is useful as a teaching example and as a baseline in experiments, and in special cases where all requests are small and of similar size.

## Pitfalls

- **Trusting the intuition.** "Large remainders are more useful" sounds right, but the policy removes the large blocks that large requests need.
- **An early stop.** The scan cannot stop at the first large block; it must see every block, unless there is an index.
- **Comparing on one trace.** One trace can show worst fit winning. Compare the policies on many traces, and on real ones where possible.

## Implementations

## History

Worst fit appears in the early literature on dynamic storage allocation as the natural opposite of best fit, and in operating-system textbooks as one of the three classic placement rules for variable partitions, next to first fit and best fit. Wilson, Johnstone, Neely and Boles summarized the experiments in 1995: in synthetic trace studies, at least, it seems to work quite badly.

## References
