---
tag: 1XC0FB
kind: technique
slug: heap-compaction
name: Heap compaction
aliases:
- garbage-collected heap compaction
area: systems/garbage-collection
level: core
summary: "In a garbage-collected heap, move the live objects together so that the free space forms one block, and rewrite every pointer to a moved object. Mark-compact and copying collectors both do it."
prereqs: [external-fragmentation, pointer]
see_also: [mark-compact, two-finger-compaction, lisp2-compaction, copying-collection, memory-compaction, bump-pointer-allocation, robson-bound, immix-collector]
sources:
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 3 (mark-compact; the arbitrary, linearising and sliding orders), and Chapter 4 (copying garbage collection, including the traversal order of Section 4.2)
  - book: isbn:9780471941484
    title: Richard Jones and Rafael Lins, Garbage Collection, Algorithms for Automatic Dynamic Memory Management, Wiley, 1996
    locator: Chapter 5 (mark-compact garbage collection) and Chapter 6 (copying garbage collection)
  - paper: doi:10.1145/321650.321658
    title: J. M. Robson, An estimate of the store size necessary for dynamic storage allocation, Journal of the ACM 18(3), 416-423, 1971
    locator: the lower bound on the memory that an allocator needs when it never moves blocks
---

Heap compaction moves the live objects of a garbage-collected heap next to each other, so that the free space becomes one block, and then rewrites every pointer to an object that moved. A garbage collector can do this safely because it knows where all the pointers are. Compaction removes [external fragmentation](/external-fragmentation/), lets the allocator use a [bump pointer](/bump-pointer-allocation/), and can improve locality. The two great families that compact are [mark-compact](/mark-compact/) collectors, which move objects inside one space, and [copying](/copying-collection/) collectors, which move them to a second space. For compaction by a general allocator, with handles or page tables, see [memory compaction](/memory-compaction/).

## In plain words

Over time a heap becomes a mix of live objects and holes. A new object may not fit in any hole, although the holes together have much more space than it needs.

To compact is to push all the live objects together, so that the holes join into one free area. The hard part is not the moving. Other objects point to the ones you move, and every one of those pointers must be changed to the new place. So every compaction has the same steps: know which objects are live, decide where each one goes, record that decision, fix the pointers, and move the objects.

## When it applies

- **The collector can find every pointer.** The runtime knows which words are pointers, in the heap and in the roots. This is a *precise* collector. A conservative collector cannot move an object that an ambiguous word may point to; it can only pin it.
- **Fragmentation hurts.** Allocation fails, or the heap must grow, although the total free space is large; or a free-list allocator is too slow.
- **Locality matters.** Objects used together should be near each other in memory, for the cache and for the pages.
- **There is time for a pause, or a way to move objects while the program runs.** Moving objects needs the mutator stopped, or a [read barrier](/read-barrier/) that hides the moves.

Without moving, fragmentation can be very bad: an allocator that never moves blocks can be forced to use about $\tfrac12 M \log_2 n$ words for $M$ live words with block sizes up to $n$ ([Robson's bound](/robson-bound/)). Compaction removes this cost.

## The template

```pseudo id=main
COMPACT(H, roots)
L1  find the live set R                                 ▷ hole: tracing, usually a mark phase
L2  choose a new address φ(x) for each x in R           ▷ hole: the order, and the target space
L3  record φ                                            ▷ hole: header word, vacated cell, side table, or threads
L4  for each root slot s and each field s of an object in R do s ← φ(s)
L5  move each x in R to φ(x)                            ▷ in a safe order, or into a second space
L6  the free space is everything outside the images of R
```

The holes are filled as follows by the main algorithms.

- **Line L1.** Tracing from the roots. Copying collectors merge L1 with the later lines: they find an object, move it, and record its new address in one step.
- **Line L2.** In one space or into a second space, and in which order:
  - *arbitrary*: any free place, as in [two-finger compaction](/two-finger-compaction/);
  - *linearising*: next to related objects, for example in the order of a [depth-first](/depth-first-search/) or [breadth-first](/breadth-first-search/) traversal, as in copying collectors;
  - *sliding*: in the old address order, as in [Lisp 2 compaction](/lisp2-compaction/).
- **Line L3.** A forwarding word in each object (Lisp 2), the old place of a moved object (two-finger, copying), a side table, or chains of threaded pointers (Morris 1978, Jonkers 1979).
- **Lines L4 and L5.** Within one space, the moves must not overwrite an object that has not moved yet. The sliding order is safe when objects move to lower addresses in address order, because then $\varphi(x) \le x$. A copy into a second space has no overlap at all.

## Classic examples

- **[Two-finger compaction](/two-finger-compaction/).** Cells of one size. One finger finds holes from the bottom, the other finds live cells from the top; each moved cell leaves its new address behind. Two passes, arbitrary order.
- **[Lisp 2 compaction](/lisp2-compaction/).** Any sizes. Three passes: compute the forwarding addresses, update the pointers, slide. The order is kept.
- **[Mark-compact](/mark-compact/) with a side table.** The same three phases, with the new addresses in a table, or computed from a mark bitmap and a few offsets for each block in one-pass compactors.
- **[Copying collection](/copying-collection/) and [Cheney's algorithm](/cheney-copying-collector/).** The live objects are copied to an empty second space, and a forwarding pointer is left in each old copy. The work is proportional to the live data only, but half the memory is held in reserve.
- **Partial compaction.** [Immix](/immix-collector/) and the [Garbage-First collector](/garbage-first-collector/) move only the objects of the most fragmented regions, and leave the rest in place.

## Variations

- **Whole heap or some regions.** Compacting only the sparse regions costs less and still frees whole regions.
- **In place or to a second space.** In place saves memory; a second space saves passes.
- **Stopped or concurrent.** A concurrent compactor, such as those of the [Shenandoah](/shenandoah-collector/) and [Z](/z-garbage-collector/) collectors, moves objects while the program runs, and a read barrier or a load barrier sends each access to the current copy.
- **Pinning.** Objects that native code or ambiguous roots refer to stay in place, and the compactor works around them, as in [mostly-copying collection](/mostly-copying-collection/).

## Pitfalls

- **A missed pointer.** If one pointer is not rewritten, it points to the old place, which will hold another object. Every root, including registers and the stacks of all threads, must be found.
- **Updating after moving.** The new address is found through the old address, so a pointer must be updated before its target is overwritten.
- **Overlapping moves.** Within one space, an object that moves down must be copied from its low end, and the objects must be moved in a safe order.
- **Address-based hashing.** An identity hash code that uses the address changes when the object moves. Runtimes store the hash in the object when it is first used.
- **The cost of moving.** Each pass over the heap and each copy cost time. Compacting a heap that has little fragmentation wastes it.

## Exercises

1. A heap holds cells of one size at the addresses $0$ to $9$, and the live cells are $2, 3, 5, 8, 9$. Give the moves of two-finger compaction and the moves of sliding compaction. Which keeps more cells in place?
2. Show that sliding compaction in address order never overwrites a live object that has not moved yet, if each object is copied from its low end.
3. A linearising compactor places the objects in breadth-first order from the roots. Give a heap where this order differs from the sliding order, and say which one puts a list's cells next to each other.
4. Explain why a conservative collector, which does not know if a word is a pointer, can still compact the objects that only precise pointers refer to.
5. Give a sequence of allocations and frees, with sizes 1 and 2, where an allocator that never moves blocks needs more memory than the live data, and show how compaction avoids it.

## References
