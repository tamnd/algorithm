---
tag: E7EWV1
kind: technique
slug: coalescing
name: Coalescing free blocks
aliases:
- free block coalescing
- merging adjacent free blocks
- immediate coalescing
area: systems/memory-allocation
level: intro
summary: "Merge a freed block with the free blocks next to it in memory, so that free space stays in large pieces and large requests can still fit."
prereqs: [free-list, external-fragmentation]
see_also: [boundary-tags, deferred-coalescing, first-fit-allocation, buddy-system, knuth-fifty-percent-rule, memory-compaction, mark-and-sweep, dlmalloc]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.5, Dynamic storage allocation, Algorithm B (liberation with a sorted list) and Algorithm C (liberation with boundary tags)
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 2.5 (splitting and coalescing, and deferred coalescing) and Section 3.2 (boundary tags)
---

*Coalescing* joins a free block with the free blocks that are next to it in memory, so that two or three small holes become one large hole. Without it, every free block keeps the size it had when it was allocated, and the heap breaks into pieces that are too small for later requests even when the free words add up to plenty. *Immediate* coalescing merges at every free; [deferred coalescing](/deferred-coalescing/) waits and merges many blocks later in one pass. Splitting and coalescing are the two halves of every variable-size allocator: malloc cuts a block in two, and free puts the pieces back together.

## In plain words

A parking lot has no painted lines. When a car leaves, the empty space can join the empty spaces on its left and right. If the lot does not join them, it remembers three small spaces, and a bus that needs all three together is turned away.

Coalescing is the rule that joins the spaces each time a car leaves. It costs a little work at each exit, but the lot keeps big spaces for big vehicles.

## When it applies

- Blocks of many sizes share one range of memory, and the allocator may split a large free block for a small request.
- The allocator can find the neighbours of a block in memory, not only on the free list. Boundary tags, an address-ordered list, a bitmap or a buddy rule give this.
- Large requests come after many small blocks are freed, so the free space must be in large pieces again.
- It does not apply to allocators that never mix sizes in one region, such as a pool of one block size or a slab of one object type, because two neighbours there are never useful as one larger block.

## The template

The heap model is the one of [first-fit allocation](/first-fit-allocation/): each block has a header and a footer with its size and a used bit, so the block above starts at the end of this one, and the footer of the block below sits in the word just before this one. The first procedure merges at once when a block is freed. The second merges every run of free blocks in one sweep by address, which is the step that deferred coalescing and a mark-sweep collector run later.

```pseudo id=main
COALESCE-ON-FREE(h, a)                     ▷ a is the block that the program frees
L1  start ← a; end ← a + SIZE(a)
L2  if end < h.H and the block at end is free then
L3      unlink the block at end
L4      end ← end + SIZE(end)
L5  if start > 0 and the footer at start − 1 says free then
L6      start ← start − (the size in that footer)
L7      unlink the block at start
L8  write header and footer: block (start, end − start), free
L9  link the block at start
COALESCE-ALL(h)                            ▷ one sweep of the whole heap
L10 a ← 0
L11 while a < h.H: if a is used then a ← a + SIZE(a); continue
L12     end ← a + SIZE(a)
L13     while end < h.H and the block at end is free do
L14         unlink the block at end; end ← end + SIZE(end)
L15     if end > a + SIZE(a) then unlink a; tag (a, end − a) free; link a
L16     a ← end
```

The freed block has four cases: both neighbours used, only the upper one free, only the lower one free, or both free. Lines L2 to L7 handle all four with two tests. The result keeps the invariant *no two free blocks are adjacent*: before the free, no two free blocks touched, and the only blocks that can touch the new free block are its two neighbours, which it absorbs. With a doubly linked list and boundary tags, COALESCE-ON-FREE costs $O(1)$ apart from the link step, which is $O(1)$ for a LIFO or FIFO list and a scan for an address-ordered list. COALESCE-ALL costs $O(B)$ for $B$ blocks in the heap.

## Classic examples

**One hole between two holes.** In a heap of 64 words, mallocs of 10, 2, 6, 2, 14 and 2 words with their two tag words fill the heap from address 0, and freeing the first, third and fifth block leaves the free blocks $(0, 12), (16, 8), (28, 16), (48, 16)$, written as (start, size). Now free the block $(12, 4)$. With coalescing it joins both neighbours, the free list becomes $(0, 24), (28, 16), (48, 16)$, and a malloc(20), which needs 22 words, fits at address 0. Without coalescing the list is $(0, 12), (12, 4), (16, 8), (28, 16), (48, 16)$ and the same malloc(20) fails, although 56 words are free. One sweep of COALESCE-ALL makes 2 merges and gives the same list as immediate coalescing.

**A random trace.** A seeded trace (seed 3) of 3000 steps, each a first-fit malloc of 1 to 64 words or a free of a random live block with equal chance, ran on a heap of $2^{12}$ words twice.

| free | free blocks on average | probes | failed requests | largest free block at the end |
|---|---|---|---|---|
| with coalescing | 8.5 | 6407 | 0 | 2171 of 2761 |
| without coalescing | 154.7 | 128309 | 4 | 62 of 2999 |

Without coalescing, the free list grows, each first-fit search gets longer, and at the end no free block has more than 62 words. The four failed requests had enough free words in total.

**Other allocators.** Knuth's Algorithm B merges while it walks an address-ordered list to insert the freed block; Algorithm C uses [boundary tags](/boundary-tags/) to merge in constant time. The [buddy system](/buddy-system/) merges a block only with its buddy, whose address is a simple function of the block's address. [Mark-and-sweep](/mark-and-sweep/) collectors merge runs of dead objects during the sweep, as in COALESCE-ALL.

## Variations

- **Immediate or deferred.** Merge at each free, or keep freed blocks of common sizes on quick lists and merge them later; see [deferred coalescing](/deferred-coalescing/) and the fastbins of [dlmalloc](/dlmalloc/).
- **The way to find the neighbours.** Boundary tags find both neighbours in $O(1)$. An address-ordered list finds them during the insertion scan. A bitmap of used words or the buddy address rule are the other common ways.
- **Merge only one side.** A simpler design merges only with the next block, because the header of the next block is easy to find and no footer is needed. Free space before the block then stays split until a sweep.
- **Merging and the list order.** After a merge the new block must go on the free list: at its address, at the head (LIFO) or at the tail (FIFO). The choice changes which blocks the next search sees first.
- **Moving blocks instead.** Coalescing joins only holes that touch. [Memory compaction](/memory-compaction/) moves live blocks so that all holes touch, at the cost of updating all references.

## Pitfalls

- **Merging a block twice.** If a free routine does not check that the block is used, a double free can link one block twice and break the list. Check the used bit first.
- **Forgetting to unlink a neighbour.** A neighbour that is absorbed must leave the free list, or the list points into the middle of the merged block.
- **Reading past the heap.** The tests for the block above and the footer below must check the heap ends, or the code needs sentinel blocks marked used at both ends.
- **A stale pointer into the list.** A next-fit rover or a cached pointer can point to a neighbour that a merge has absorbed. Move it to a block that is still free.
- **Coalescing that undoes useful splits.** A program that frees and allocates the same small size again and again makes the allocator merge and split the same block. Deferred coalescing removes that work.

## Exercises

1. Draw the four cases of COALESCE-ON-FREE and write the free list before and after each one.
2. Prove that COALESCE-ON-FREE keeps the invariant that no two free blocks are adjacent.
3. Change COALESCE-ON-FREE so that it merges only with the block above. Find a sequence of frees after which two free blocks touch.
4. Show that a program that asks for only one size never has a failed request because of missing coalescing, and give a program with two sizes that does.
5. Count the work of COALESCE-ALL on a heap of $B$ blocks, and explain why it does not depend on the order of the free list.

## References
