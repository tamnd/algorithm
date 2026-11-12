---
tag: CQMDE4
kind: technique
slug: memory-compaction
name: Memory compaction
area: systems/memory-allocation
level: core
summary: "Move live blocks together so that the free memory becomes one large region, then fix every reference to a moved block, either directly or through a table of handles."
prereqs: [allocator, external-fragmentation]
see_also: [heap-compaction, mark-compact, lisp2-compaction, two-finger-compaction, copying-collection, robson-bound, mostly-copying-collection, bump-pointer-allocation]
sources:
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, CRC Press, 2011
    locator: Chapter 3, Mark-compact garbage collection (two-finger compaction, the Lisp 2 algorithm, threaded compaction, one-pass algorithms) and the discussion of the order of moved objects
  - url: https://lwn.net/Articles/368869/
    title: "Jonathan Corbet, Memory compaction, LWN.net, January 6, 2010"
    locator: the migration scanner from the bottom of a zone, the free scanner from the top, and the triggers
  - paper: doi:10.1007/3-540-60368-9_19
    title: "Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation: a survey and critical review, IWMM 1995, LNCS 986, 1-116"
    locator: Section 1 (why a C allocator cannot move blocks) and Section 4.1 (the worst-case bounds without compaction)
---

Memory compaction moves live blocks so that they sit next to each other, and the free memory between them joins into one large region. It is the only cure for [external fragmentation](/external-fragmentation/) once the free memory has broken into holes: without moving, an allocator can be forced to use about $\tfrac12 M \log_2 n$ words for $M$ live words, by [Robson's bound](/robson-bound/). The work has two parts: copying the blocks, and fixing every reference to a block that moved. The second part decides where compaction is possible at all.

## In plain words

A bookshelf fills up, and you take out books here and there. Now there are many small gaps, and a big new book fits in none of them, though the gaps together are wide enough. The fix is to slide all books to the left, so that all the free space is at the right end.

For memory there is a catch. Other parts of the program remember where each block was, like notes that say "the red book is third from the left". After the books move, every note is wrong. So compaction must also find every note and correct it, or the program must use notes that point to a fixed index card, and the card says where the book is now.

## When it applies

- The free memory is large in total, but no free hole is big enough for a request, or the holes make allocation slow.
- The system can find every reference to a block that it moves. A garbage collector with exact type information can do this. A C allocator cannot, because any word in the program may hold an address, so malloc implementations never compact.
- Or the program reaches blocks only through handles, so a move changes one table entry.
- Or the moved units have no direct references that matter, such as physical pages behind virtual addresses: the operating system moves a page and updates the page table.
- The pause or the copying cost is acceptable. Compaction touches every live block that moves, and often the whole heap.

## The template

The template moves the live blocks to the bottom of a region, in an order chosen by a hole, and fixes the references with forwarding addresses.

```pseudo id=main
COMPACT(region, LIVE, ORDER, RECORD, REFS)
L1  free ← the lowest address of region
L2  for each block b in LIVE, taken in the order ORDER
L3      RECORD(b, free)                     ▷ remember forward(b) = free
L4      free ← free + size(b)
L5  for each reference slot r in REFS (roots and slots inside live blocks)
L6      if r points to a block b that moves, set r ← forward(b)
L7  for each block b in LIVE, in the order ORDER
L8      copy b to forward(b)
L9  return free                              ▷ [free, end of region) is now one hole
```

The holes are:

- **LIVE**: which blocks survive. An allocator knows its allocated blocks. A [mark-compact](/mark-compact/) collector finds them by marking from the roots.
- **ORDER**: the order of the new addresses. Address order gives sliding compaction, which keeps the relative order of blocks. Any other order gives arbitrary compaction.
- **RECORD**: where the forwarding address lives. It may be a header word in the block, a side table, or a handle table.
- **REFS**: how to find every reference slot. With handles, REFS is only the handle table.

**Walk-through.** Lines L1 to L4 compute a new address for each live block, packing them one after another. Lines L5 and L6 fix the references while the old copies are still in place, so that each slot can still be read and each forwarding address found. Lines L7 and L8 move the data. With address order, every block moves to a lower or equal address, and the blocks are moved from the lowest up, so a copy can only overwrite memory that is free or that belongs to a block already moved. That is why sliding needs no second region. Line L9 returns the start of the single free region, from which a [bump pointer](/bump-pointer-allocation/) can allocate.

**Example.** A region has 16 words. Live blocks are $A = [0, 3)$, $C = [5, 9)$ and $E = [10, 12)$; the words $[3, 5)$, $[9, 10)$ and $[12, 16)$ are free, so the largest hole has 4 words. A root points to $C$, and a slot inside $C$ points to $E$.

| Step | A | C | E | Root | Slot in C | Largest hole |
|---|---|---|---|---|---|---|
| before | 0 | 5 | 10 | 5 | 10 | 4 |
| after L1 to L4 | forward 0 | forward 3 | forward 7 | 5 | 10 | 4 |
| after L5, L6 | 0 | 5 | 10 | 3 | 7 | 4 |
| after L7, L8 | 0 | 3 | 7 | 3 | 7 | 7 |

The data of 6 words moved (blocks $C$ and $E$), two references changed, and the free space became the single hole $[9, 16)$ of 7 words.

## Classic examples

- [Two-finger compaction](/two-finger-compaction/): one pointer scans up for holes, one scans down for live blocks, and each live block from the top moves into a hole at the bottom. It is arbitrary compaction, needs blocks of one size (or one size class per region), and takes two passes.
- [LISP 2 compaction](/lisp2-compaction/): the template above with address order and a forwarding word in each header. Three passes over the heap: compute addresses, update references, move. It is the standard sliding compactor.
- [Mark-compact](/mark-compact/): marking plus one of these compaction schemes; the [heap compaction](/heap-compaction/) page covers the garbage collection view.
- [Copying collection](/copying-collection/): compacts as a side effect, by copying live objects into an empty space in the order of a graph traversal. It needs twice the space but touches only live objects.
- [Mostly-copying collection](/mostly-copying-collection/): moves objects except those named by ambiguous roots, which are pinned. This is the usual answer when not every reference is known.
- **Linux memory compaction.** The kernel compacts physical memory to build large runs of free pages, for example for huge pages. A migration scanner starts at the bottom of a memory zone and collects movable pages in use. A free scanner starts at the top and collects free pages. When they meet, the used pages are migrated into the free pages at the top, and the bottom becomes one block of free pages. References are virtual addresses, so the move only changes page table entries. It runs when a large allocation fails, or when asked through a control file.

## Variations

- **Sliding against arbitrary.** Sliding keeps the address order of blocks, which keeps blocks that were allocated together close together, and keeps the cache behavior of the program. Arbitrary compaction is simpler and faster per pass, but it scatters related blocks.
- **Forwarding addresses against handles.** A forwarding address stored in the block costs one word per block and a pass over all references. A handle is a fixed table entry that holds the current address; the program holds the handle. Moving a block then changes one entry and needs no search for references, but every access pays one extra indirection, and the table is itself a structure that must be managed. Early object-oriented systems used an object table, and early personal computer memory managers used relocatable blocks reached through handles.
- **Threaded compaction.** References to a block are linked into a chain through the block header, so no extra forwarding word is needed (Jonkers, Morris). See the GC Handbook, Chapter 3.
- **Partial or incremental compaction.** Only the most fragmented regions are evacuated, as in the region-based collectors [G1](/garbage-first-collector/), [Shenandoah](/shenandoah-collector/) and [ZGC](/z-garbage-collector/), and as in the opportunistic defragmentation of [Immix](/immix-collector/).
- **Compaction in allocators without references.** Pools of fixed-size objects reached by index, and databases that store records in slotted pages, compact freely because no outside pointer names an address.

## Pitfalls

- **A missed reference.** If REFS skips one slot, that slot still names the old address after the move, and the program reads stale or foreign data. This is why conservative collectors pin blocks named by ambiguous words instead of moving them.
- **Moving before updating, without keeping the forwarding data.** If line L8 runs before L6 and the forwarding address was stored in the header of the old copy, the copy of another block may overwrite that header first. Keep the forwarding data where no move can overwrite it, or update before moving, as in the template.
- **Copying in the wrong order.** Sliding down is safe only in increasing address order, with a copy that allows overlap. Moving the blocks from the highest down can overwrite a block that has not moved yet.
- **Interior pointers.** A slot may point inside a block, not at its start. The update must add the offset: the new value is forward(b) plus the old offset.
- **Cost out of proportion.** Compaction may move almost the whole heap to win a little space. Real systems compact only when fragmentation passes a threshold, or only the worst regions.
- **Pinned blocks.** Blocks shared with hardware or foreign code, and pages locked in memory, cannot move. They split the free region, and the result is less than one hole.

## Exercises

1. Prove that the template with address order never overwrites a live block before it is copied, if blocks are copied in increasing address order with a copy routine that allows the source and target to overlap.
2. Give a heap of blocks of sizes 1 and 2 on which two-finger compaction, using the first hole that fits the block at the top, does not end with all free space in one hole.
3. A heap has $k$ live blocks and $r$ reference slots. Count the words written by the template with header forwarding words, and by a scheme with one handle per block, for one compaction and for $q$ later accesses.

## References
