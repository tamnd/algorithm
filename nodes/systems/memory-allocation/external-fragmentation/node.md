---
tag: P2N3SK
kind: concept
slug: external-fragmentation
name: External fragmentation
aliases:
- external waste
- checkerboarding
- external memory fragmentation
area: systems/memory-allocation
level: intro
summary: "Free memory that is split into blocks too small for the requests, so a request fails while the total free space is large enough."
prereqs: [allocator]
see_also: [internal-fragmentation, coalescing, sequential-fit, knuth-fifty-percent-rule, robson-bound, memory-compaction, heap-compaction, buddy-system]
sources:
  - paper: doi:10.1145/363156.363158
    title: Brian Randell, A note on storage fragmentation and program segmentation, Communications of the ACM 12(7), 1969, starting on page 365
    locator: the distinction between external fragmentation (between blocks) and internal fragmentation (inside rounded-up blocks)
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 2.1 (internal and external fragmentation) and Section 2 (fragmentation as a result of the placement choices and the lifetimes of objects)
  - paper: doi:10.1145/286860.286864
    title: Mark S. Johnstone and Paul R. Wilson, The memory fragmentation problem, solved?, ISMM 1998, 26-36
    locator: the four definitions of fragmentation (memory used relative to memory requested, at various points in time) and the results for eight real programs
---

External fragmentation is free memory that the allocator cannot use because it lies in many small pieces between live blocks. A request for $n$ words can fail even though the free words add up to much more than $n$, because no single free block has $n$ words. The live blocks cannot move, so the pieces stay apart until their neighbours are freed. A common measure is $1 - L/T$, where $T$ is the total free memory and $L$ the size of the largest free block: it is 0 when all free memory is in one block, and close to 1 when the free memory is spread over many small blocks. Randell named the effect, and separated it from [internal fragmentation](/internal-fragmentation/), the waste inside allocated blocks.

## In plain words

A bookshelf has space for 52 books, but the empty spaces are between other books: 12 here, 8 there, 16 and 16 at the end. A set of 17 books that must stand together does not fit anywhere, although there is room for 52 books in all.

That is external fragmentation. The space exists, but it is in the wrong shape. You could fix it by moving books together, but an allocator is not allowed to move the blocks it gave out.

## The idea

**Where it comes from.** Each placement choice of an allocator and each free by the program changes the pattern of free and used blocks. When objects that die at different times sit next to each other, a free leaves a hole between live objects. Wilson, Johnstone, Neely and Boles stress that fragmentation comes from the interaction of the placement policy with the sizes and the lifetimes of the objects, not from the policy alone.

**The largest-block measure.** Let the free blocks have sizes $s_1, \ldots, s_F$, with $T = \sum s_i$ and $L = \max s_i$. Then

$$\text{frag} = 1 - \frac{L}{T}, \qquad 0 \le \text{frag} < 1,$$

and $\text{frag} = 0$ when $F \le 1$. If $\text{frag} = 0$, every request of at most $T$ words fits. If a request for $need \le T$ words fails, then $L < need \le T$, so $\text{frag} > 0$: a failure with enough total space always shows up in this measure.

```pseudo id=main
LARGEST-FREE-FRACTION(h)
L1  total ← 0; largest ← 0
L2  for each block a on the free list do
L3      total ← total + SIZE(a)
L4      largest ← max(largest, SIZE(a))
L5  return 0 if total = 0 else 1 − largest / total
```

**Other measures.** No single number captures fragmentation, and each one answers a different question.

- *The fraction of free memory in blocks smaller than a size $k$.* With $k$ the size of a typical request, this is the free memory that the program cannot use now.
- *The number of free blocks.* Easy to count, and the [fifty-percent rule](/knuth-fifty-percent-rule/) predicts it in a steady state, but it ignores the sizes.
- *The memory used against the memory requested.* Johnstone and Wilson define fragmentation by the memory that the allocator uses, its footprint, against the memory that the program has live. They give four versions: the two amounts averaged over all points in time; both at the point of maximum live memory; both at the point of maximum memory used; and the maximum memory used against the maximum live memory, at possibly different points. These measures include the costs of headers and rounding unless those are counted apart.

## Examples

**A failed request.** In the heap of the [first-fit page](/first-fit-allocation/), $H = 64$, the free blocks are $(0, 12), (16, 8), (28, 16), (48, 16)$, written as (start, size). So $T = 52$, $L = 16$ and $\text{frag} = 1 - 16/52 \approx 0.69$. A malloc(15) needs 17 words with its two tag words, and it fails. All of the free memory lies in blocks smaller than 17 words, so the second measure, with $k = 17$, is 1. With $k = 9$ it is $8/52$, since only the 8-word block is too small.

**Two policies on one trace.** A seeded random trace (seed 3) of 3000 steps, each a malloc of 1 to 64 words or a free of a random live block with equal chance, ran in a heap of $2^{16}$ words. The footprint is the end of the highest used block. Address-ordered [first fit](/first-fit-allocation/) gave a footprint 1.68 times the live words on average, and a peak footprint 1.22 times the peak live words. [Worst fit](/worst-fit/) gave 14.47 and 16.35, because it always cut the largest free block, which was the untouched end of the heap, so it spread the live blocks over the whole heap. Both figures include the tag words, so part of them is internal fragmentation.

**What reduces it.**

- Immediate or deferred [coalescing](/coalescing/), so that free neighbours become one block.
- A good placement policy: address-ordered first fit and best fit leave little fragmentation on real programs (Johnstone and Wilson).
- Moving live blocks: [memory compaction](/memory-compaction/) and compacting garbage collectors ([heap compaction](/heap-compaction/)) remove external fragmentation at the cost of updating all references.
- Fixed block sizes: [size classes](/size-classes/), the [buddy system](/buddy-system/) and paging limit external fragmentation and trade it for internal fragmentation.

## Where it is used

- **Heap allocators.** The main quality measure of a malloc implementation, together with time. The [Robson bound](/robson-bound/) gives the worst case for any allocator that cannot move blocks.
- **Operating systems.** Variable partitions and segments in main memory suffer from it; paging was one answer. "Checkerboarding" is an older name for the pattern of used and free segments.
- **File systems and disks.** Free space split into many small extents slows large files and can make a large contiguous file impossible.
- **GPU and real-time memory.** Fixed pools, [TLSF](/tlsf/) and arenas are chosen partly to bound fragmentation.

## References
