---
tag: EYH51V
kind: concept
slug: internal-fragmentation
name: Internal fragmentation
aliases:
- internal waste
- internal memory fragmentation
area: systems/memory-allocation
level: intro
summary: "Memory wasted inside allocated blocks: the words a block has beyond the request, from rounding, alignment, size classes and minimum sizes."
prereqs: [allocator]
see_also: [external-fragmentation, size-classes, buddy-system, segregated-free-lists, slab-allocator, boundary-tags, first-fit-allocation, tlsf]
sources:
  - paper: doi:10.1145/363156.363158
    title: Brian Randell, A note on storage fragmentation and program segmentation, Communications of the ACM 12(7), 1969, starting on page 365
    locator: the definition of internal fragmentation as the space lost when requests are rounded up to a unit of allocation
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 2.1 (internal and external fragmentation) and Section 3.2 (header overhead and boundary tags)
  - paper: doi:10.1145/286860.286864
    title: Mark S. Johnstone and Paul R. Wilson, The memory fragmentation problem, solved?, ISMM 1998, 26-36
    locator: the separation of fragmentation from the overheads of headers, alignment and minimum block size
---

Internal fragmentation is memory that is wasted *inside* an allocated block: the block has more words than the program asked for, and nobody can use the extra words while the block is live. It comes from rounding the request up, to an alignment, to a size class or to a minimum block size, and from giving out a whole free block when the remainder would be too small to split. Randell separated it from [external fragmentation](/external-fragmentation/), the waste *between* blocks. The two trade against each other: allocators that use a few fixed block sizes, such as [size classes](/size-classes/) and the [buddy system](/buddy-system/), have little external fragmentation and more internal fragmentation.

## In plain words

You ask for a box to send 9 books, but the shop only sells boxes for 8 or 16 books. You take the box for 16, and the space for 7 books is empty for the whole trip. Nobody else can use it, because the box is yours.

That empty space is internal fragmentation. The shop has fewer box sizes to keep, which makes its work simpler, but each box carries some air.

## The idea

For a live block of $s$ words that serves a request of $n$ words, the waste is $s - n$. It has several parts.

- **Header and footer.** The allocator needs some words per block for its own data. In the heap model of the [first-fit page](/first-fit-allocation/), each block has a header and a footer, 2 words. Wilson et al. and Johnstone and Wilson count these as *overhead* apart from fragmentation, since they depend on the mechanism, not the policy.
- **The minimum block size.** A free block must hold its header, its footer and two list links, so the smallest block has 4 words, and a request of 1 word gets 4.
- **Unsplit remainders.** When the chosen free block is only a little larger than the request, the remainder is too small to be a free block, and the request gets the whole block.
- **Alignment.** Hardware or the language needs addresses that are multiples of $A$, so sizes are rounded up to a multiple of $A$. The waste is at most $A - 1$ words per block.
- **Size classes.** An allocator with classes rounds each request up to the next class.

```pseudo id=main
ROUND-UP(n, A)                             ▷ alignment
L1  return ⌈n / A⌉ · A
POW2-CLASS(n)                              ▷ the buddy system
L2  c ← 1
L3  while c < n do c ← 2c
L4  return c
CLASS-OF(n, classes)                       ▷ any sorted list of classes
L5  return the first class that is at least n (binary search)
```

**Bounds.** With power-of-two classes, a request $n > 1$ gets a class $c < 2n$, so less than half of the block is waste. With $k$ equally spaced classes in each doubling (for example 8, 10, 12, 14, 16, 20, 24, ... for $k = 4$), the gap between two classes is at most $1/(k+1)$ of the larger one, so less than $1/(k+1)$ of each block is waste. The price of more classes is more lists to manage and more memory held by partly used pages of each class.

## Examples

**One small heap.** In a heap of 16 words, malloc(1) needs 3 words and gets the minimum block of 4; malloc(7) needs 9 words, and the free block of 12 cannot be split, because a remainder of 3 words is below the minimum. So the two blocks have 4 tag words and 4 more words of slack: 1 from the minimum size and 3 from the unsplit remainder.

**The words add up.** At every moment of the heap model, the heap size equals the free words plus the requested words plus the tag words plus the slack. On a seeded random trace (seed 1, a heap of $2^{14}$ words, 3000 steps of malloc of 1 to 64 words or free of a random live block), the 30 live blocks at the end held 1051 requested words, 60 tag words and 16 words of slack.

**Rounding policies on uniform sizes.** For the request sizes $1, 2, \ldots, 1024$, each once, the fraction of the allocated words that was waste was:

| rounding | waste |
|---|---|
| to a multiple of 8 | 0.68% |
| to a multiple of 16 | 1.44% |
| to powers of two | 24.9% |
| 4 classes per doubling | 7.6% |

The power-of-two rule wastes about a quarter of the memory on these sizes. Real programs often use a few sizes many times, and then the waste depends on how well those sizes match the classes.

## Where it is used

- **Size-class allocators.** [Segregated free lists](/segregated-free-lists/) and production allocators such as [jemalloc](/jemalloc/) and [tcmalloc](/tcmalloc/) choose their classes to keep internal fragmentation low while the number of classes stays small.
- **The buddy system.** Power-of-two blocks make merging fast; the cost is internal fragmentation of up to half a block.
- **Slabs and pools.** A [slab allocator](/slab-allocator/) makes a class for each object type, so objects of that type waste nothing inside; the waste moves to the unused end of each slab.
- **Paging.** A process gets whole pages, so on average half of its last page is waste.
- **Boundary tags.** The footer of a [boundary tag](/boundary-tags/) is overhead in each used block; the common optimization keeps the footer only in free blocks and moves a used bit into the next block's header.

## References
