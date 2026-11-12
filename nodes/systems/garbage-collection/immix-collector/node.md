---
tag: 2YV2TJ
kind: algorithm
slug: immix-collector
name: Immix collector
aliases:
- Immix
area: systems/garbage-collection
level: research
summary: "A mark-region collector. The heap is cut into 32 KB blocks of 128-byte lines; marking frees whole lines, the allocator bumps into free lines, and sparse blocks are copied out opportunistically."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {n: the live objects (the bounds are for one collection), p: the pointer fields per object, B: the blocks, l: the lines per block}
  time: {worst: O(n p + B l), best: Θ(B l)}
  space: {extra: O(B l + n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2008
  people: [Stephen M. Blackburn, Kathryn S. McKinley]
  note: Blackburn and McKinley named the mark-region family and gave Immix, which marks lines of 128 bytes in blocks of 32 KB, allocates with a bump pointer into free lines, and copies objects out of fragmented blocks in the same pass as marking.
prereqs: [mark-and-sweep, bump-pointer-allocation, external-fragmentation]
see_also: [mark-compact, copying-collection, heap-compaction, lazy-sweeping, segregated-free-lists, garbage-first-collector, reference-counting, generational-garbage-collection]
sources:
  - paper: doi:10.1145/1375581.1375586
    title: "Stephen M. Blackburn and Kathryn S. McKinley, Immix: a mark-region garbage collector with space efficiency, fast collection, and mutator performance, PLDI 2008, 22-32"
    locator: The mark-region design, blocks and lines, conservative line marking, the allocator of holes with overflow allocation, and opportunistic defragmentation
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 10 (other partitioned schemes, mark-region collection and Immix)
---

Immix is a tracing collector of the *mark-region* family, by Blackburn and McKinley (2008). The heap is cut into blocks of 32 KB, and each block into 256 *lines* of 128 bytes. The mutator allocates with a fast [bump pointer](/bump-pointer-allocation/), but into *holes*, runs of free lines, and not only into empty space. The collector marks live objects and also the lines they occupy; after marking, every unmarked line is free and the next allocations fill it. There is no sweep of objects and no free list. Small objects can spill into the next line, so the marking is *conservative*: the allocator skips one free line after each marked line. To fight [fragmentation](/external-fragmentation/), the collector can pick the most fragmented blocks before it traces and copy their objects out during the same trace, while free space lasts. Immix combines the space use of [mark-and-sweep](/mark-and-sweep/), the speed of a bump allocator, and the locality of a [copying collector](/copying-collection/).

## In plain words

Picture a parking lot cut into rows, and each row into short stripes of equal length. Cars park one after another along the free stripes.

To clean up, the collector finds the cars that are still in use and puts a tick on each stripe that such a car touches. Every stripe without a tick is free again, and new cars park in runs of free stripes, one after another. Nothing is moved, and no list of free gaps is kept.

A small car may stick out of its stripe into the next one, and only its first stripe gets a tick. So the parking attendant always leaves the first free stripe after a ticked one empty.

When a row is full of small gaps, the collector moves its cars to an empty row while it walks over them, if there is room.

## The problem

**Heap model.** The heap has $B$ blocks of $l$ lines of $s$ bytes; Immix uses $l = 256$ and $s = 128$. An object has a size in bytes and some pointer fields. It is *small* if its size is at most $s$, *medium* if it is larger but at most a quarter of a block; larger objects live in a separate space and are not part of this page. The mutator holds a fixed set of root registers; it allocates objects, loads fields into registers and stores registers into fields. An object never crosses a block boundary.

**Goal.** When an allocation finds no space, reclaim the objects that are not reachable from the roots and give their space to later allocations, without ever handing out a byte of a live object. Allocation should be a bump of a pointer in the common case, and the collector should be able to reduce fragmentation without a separate compaction pass.

## The algorithm

The mutator has a bump region $[\textit{cursor}, \textit{limit})$ in its current block. A block is *free* if no line of it is marked, and *recyclable* if it has a hole. The allocator keeps a few free blocks, the *headroom*, for the copies of the collector.

```pseudo id=main
ALLOCATE(n)                              ▷ the mutator asks for n bytes
L1  if cursor + n ≤ limit then return BUMP(n)
L2  if n > s and an overflow block can be had then bump in the overflow block
L3  while NEXT-HOLE() do
L4      if cursor + n ≤ limit then return BUMP(n)
L5  COLLECT, then try once more; fail if there is still no space

NEXT-HOLE()                              ▷ the current block, then recyclable blocks, then free blocks
L6  find the next run of unmarked lines, but skip an unmarked line just after a marked line;
        cursor ← its first byte; limit ← its end

COLLECT
L7  C ← ∅, or to defragment, the blocks with the most holes while their marked lines fit in the free blocks
L8  clear the marks; for each root r do r ← PROCESS(r)
L9  while the mark stack is not empty do x ← POP()
L10     for each field f of x do x.f ← PROCESS(x.f)
L11 for each block b: b is free if no line of b is marked, else recyclable if it has a hole

PROCESS(x)
L12 if x = nil then return nil; if x is forwarded then return its new address
L13 if x is marked then return x
L14 if x is in a block of C and a free block has room y then copy x to y; forward x to y; x ← y
L15 mark x; mark the first line of x if x is small, else every line of x
L16 push x; return x
```

**Lines and holes.** Line marks are one byte per line, set during the trace (line L15). A small object marks only its first line, which is cheap, but it can end in the next line; line L6 therefore treats the first unmarked line after a marked line as used. A medium object marks every line it covers, so the skip only wastes space after it.

**Overflow allocation.** A small object always fits in a hole, since a hole has at least one line. A medium object may not fit in the current hole; if the allocator skipped to the next hole that fits, it would waste the holes in between. So a medium object that does not fit goes to a separate *overflow* block (line L2), and the small objects keep filling the holes. When no free block is left, the model falls back to the search of holes.

**Opportunistic evacuation.** Line L7 picks the candidate blocks $C$ from the counts of the previous collection: those with the most holes first, while their marked lines fit in the free blocks. During the trace, line L14 copies an object of $C$ the first time the trace reaches it, and leaves a forwarding address; later pointers to it are fixed at line L12. If the free blocks run out, the object is marked in place, so evacuation never fails. In the real system an object can also be pinned and is then never moved.

## Example

**The skipped line.** Blocks of 32 KB with lines of 128 bytes. The mutator allocates an object of 64 bytes at address 0 and an object of 100 bytes at address 64, keeps only the second, and the collector runs. The live object covers bytes $[64, 164)$, which is lines 0 and 1, but only line 0 is marked.

| line | marked | with the skip | without the skip |
|---|---|---|---|
| 0 | yes | used | used |
| 1 | no | skipped: implicitly used | first hole starts here |
| 2 to 255 | no | first hole $[2, 256)$ | part of the hole $[1, 256)$ |

The next allocation of 64 bytes gets address 256 with the skip. Without the skip it gets address 128, inside the live object.

**Defragmentation.** Blocks of 16 lines of 16 bytes, 16 blocks, a headroom of 2. The mutator allocates 160 objects of one line in 10 blocks and keeps every fourth one on a list. A collection without defragmentation marks lines 0, 4, 8 and 12 of each of the 10 blocks; each block has the 4 holes $[2, 4)$, $[6, 8)$, $[10, 12)$, $[14, 16)$, and 6 blocks are free. A second collection with defragmentation picks all 10 blocks as candidates, since their 40 marked lines (640 bytes) fit in the 6 free blocks. The trace copies all 40 live objects into 3 blocks, and 13 blocks are free afterward. The list is the same, cell by cell.

## Correctness

The proof in the proofs section has three parts.

1. **The trace is right.** The marking argument of [mark-and-sweep](/mark-and-sweep/) holds, with the forwarding of [copying collection](/copying-collection/) for the objects that move. Each object is copied at most once, since a copy is marked and the old place holds a forwarding address. Every pointer to a moved object passes through PROCESS and is replaced by the new address, so the graph of objects, by identity, is the same after the collection.
2. **No hole holds a live byte.** A small object lies in its first line and the next one. Its first line is marked, and the next line is marked or is the first unmarked line after a marked line, which line L6 skips. Every line of a medium object is marked. A hole has only unmarked lines that are not just after a marked line, so it holds no byte of a live object.
3. **No byte is handed out twice between collections.** The cursor only moves forward within a hole, the holes of a block are found in order, each block is taken once from the recyclable or free list, and the overflow and copy regions use blocks taken from the free list.

The tests run random programs on small and full-size geometries, and check after each step that the graph matches a model with no collector and that no two objects overlap, and after each collection that no hole holds a byte of a live object. With the skip of line L6 turned off, all 12 random runs on the full-size geometry break one of these checks.

## Complexity

The model is the [word RAM](/word-ram/) with the heap model above.

- **A collection.** The trace costs $O(n p)$ for $n$ live objects with $p$ fields, plus the copies. Clearing the line marks and counting the holes of each block costs $O(B l)$.
- **Allocation.** A bump in the common case. Over the time between two collections, the hole search reads each line of the heap at most once, so it costs $O(B l)$ in total.
- **Space.** One mark byte per line and a mark bit per object, the mark stack, and the headroom blocks. The lost space is the skipped line after each marked line and the ends of holes too short for the next object.

## Properties

- **Not moving, unless it helps.** Without defragmentation Immix never moves an object, like mark-and-sweep; with it, only the objects of the candidate blocks move, in the same pass.
- **No sweep of objects.** The collector reads the line marks, not the dead objects. Dead objects are never touched.
- **Contiguous allocation.** New objects that are allocated together are placed together, as in a copying collector, which gives good cache locality.
- **Coarse reclamation.** Space comes back in lines, not in objects. One small live object holds a line of 128 bytes, plus the next line.
- **Two kinds of free space.** Free blocks serve medium objects and copies; holes in recyclable blocks serve small objects.

## Variants and improvements

- **Sticky marks.** A generational form that keeps the marks of old objects and collects only the new ones, without copying the young objects out.
- **Reference counting Immix.** Shahriyar, Blackburn, Yang and McKinley (2013) reclaimed lines with [reference counting](/reference-counting/) and used Immix copying for cycles and fragmentation; the LXR collector (2022) builds on this.
- **Generational Immix.** A copying nursery, with Immix for the old generation; see [generational collection](/generational-garbage-collection/).
- **Other line sizes.** Smaller lines lose less space per live object but cost more marks and more skipped space. The paper chose 128 bytes and 32 KB by measurement.

## When to use it

Use it as the main collector of a managed runtime that wants the fast allocation and locality of a copying collector but cannot afford to keep half of the heap empty. It suits languages that allocate many small objects. Prefer a [copying collector](/copying-collection/) for a nursery where almost everything dies; prefer [segregated free lists](/segregated-free-lists/) or [mark-and-sweep](/mark-and-sweep/) when objects must never move and are mostly of a few sizes; prefer a concurrent region collector such as [Garbage-First](/garbage-first-collector/) when pauses matter more than throughput.

## Pitfalls

- **Forgetting the spill of small objects.** If only the first line of a small object is marked and the allocator does not skip the next line, the next allocation can overwrite the tail of a live object. In the example the new object lands at address 128, inside the live object at $[64, 164)$.
- **Medium objects in small holes.** Without overflow allocation, a medium object skips hole after hole, and the skipped holes are wasted until the next collection.
- **No headroom.** If every block holds a live line, there is no free block to copy into, and defragmentation cannot start. Keep a few blocks back for it.
- **Stale counts.** Candidates are chosen from the counts of the previous collection; the live data in a block may have changed since. Evacuation must therefore be opportunistic and fall back to marking in place.
- **Interior pointers and pinning.** Objects that native code or conservative roots point to cannot move. They must be pinned, and their blocks cannot be fully freed.

## Implementations

## History

McCarthy's mark-sweep (1960) reclaimed single cells, and copying collectors from Cheney (1970) gave fast bump allocation at the cost of half the heap. Bartlett's mostly-copying collector (1988) already used pages as a coarse unit. Blackburn and McKinley (2008) named the mark-region family and built Immix in the MMTk toolkit of the Jikes RVM, with lines inside blocks, a skip for small objects, and copying in the same pass as marking. Later work added a sticky generational form, reference counting Immix (2013), and low-latency collectors built on its heap layout.

## References
