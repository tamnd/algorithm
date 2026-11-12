---
tag: Q000WF
kind: technique
slug: bump-pointer-allocation
name: Bump-pointer allocation
aliases:
- bump allocation
- linear allocation
- bump-pointer allocator
area: systems/memory-allocation
level: intro
summary: "Allocate from one free range by moving a pointer past each new block: round up for alignment, check the limit, add the size. Blocks are freed only all at once."
prereqs: [allocator]
see_also: [arena-allocation, stack-allocation, copying-collection, cheney-copying-collector, thread-local-allocation-buffer, generational-garbage-collection, region-based-memory-management, memory-pool]
sources:
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, CRC Press, 2011
    locator: Chapter 7, Allocation, Section 7.1, Sequential allocation
  - paper: doi:10.1016/0020-0190(87)90175-X
    title: Andrew W. Appel, Garbage collection can be faster than stack allocation, Information Processing Letters 25(4), 1987, 275-279
    locator: the cost of allocation by a pointer increment and a limit check in a copying collector, set against the cost of freeing stack frames
  - paper: doi:10.1002/spe.4380200104
    title: David R. Hanson, Fast allocation and deallocation of memory based on object lifetimes, Software, Practice and Experience 20(1), 1990, 5-12
    locator: allocation inside an arena block by a pointer increment and a limit check
---

*Bump-pointer allocation* serves requests from one free range of memory with a single pointer, *top*, that marks where the free part starts. To allocate $n$ bytes, round top up to the alignment, check that the block ends before the *limit*, and move top past it. That is a few machine instructions, with no search and no header. The cost is that single blocks cannot be freed: the range is freed all at once, by a reset of top, by dropping a whole [arena](/arena-allocation/), or by a [copying collector](/copying-collection/) that moves the live objects away and makes the whole range free again.

## In plain words

Think of a roll of paper tape. To give someone a piece, cut it from the end of the roll and move your mark along. You never look for a gap, because there are no gaps: all the used tape is behind the mark, and all the free tape is in front of it.

The trick is fast because it is so simple. The price is that you cannot glue a piece back into the middle of the roll. You can only start a new roll when every piece is no longer needed.

## When it applies

- All blocks in the range die at about the same time, or a collector finds the live ones and moves them out. Then there is no need to free single blocks.
- Allocation is very frequent and must be cheap, as in functional and object-oriented programs that make many small objects.
- The free memory is one range, so that a pointer and a limit describe it. A [copying collector](/copying-collection/) gives this after each collection, because it packs the live objects together.
- Each thread can own its range, so the pointer needs no lock. A [thread-local allocation buffer](/thread-local-allocation-buffer/) is a small range of this kind inside a shared heap.

## The template

The range is $[base, limit)$, and $top$ starts at $base$. The alignment $a$ is a power of two, so rounding up is a mask.

```pseudo id=main
BUMP-ALLOC(n, a)                                 ▷ an a-aligned block of n bytes, or FAIL
L1  p ← (top + a − 1) AND NOT (a − 1)            ▷ round top up to a multiple of a
L2  if p + n > limit then return FAIL            ▷ or take the slow path
L3  top ← p + n
L4  return p

RESET()                                          ▷ free all blocks at once
L5  top ← base
```

The blocks lie in the order of their allocation, each below the next, and all of them lie in $[base, top)$. So BUMP-ALLOC never returns a byte that is in use, and each call takes $O(1)$ time. Line L2 is the only branch. In a real system the failure path is not FAIL but a *slow path*: start a new chunk, as in an [arena](/arena-allocation/), ask for a new thread buffer, or run the garbage collector.

## Classic examples

**A worked run.** Take $base = 0$ and $limit = 64$.

| call | top before | p | top after | note |
|---|---|---|---|---|
| alloc(5, 1) | 0 | 0 | 5 | |
| alloc(8, 8) | 5 | 8 | 16 | 3 bytes of padding |
| alloc(3, 1) | 16 | 16 | 19 | |
| alloc(4, 4) | 19 | 20 | 24 | 1 byte of padding |
| alloc(50, 1) | 24 | | 24 | FAIL, because $24 + 50 > 64$ |
| alloc(40, 1) | 24 | 24 | 64 | the range is now full |
| reset, then alloc(50, 1) | 0 | 0 | 50 | |

The only waste is the padding for alignment. The page's tests check, on seeded random runs, that each block is aligned, inside the range and above every earlier block since the last reset.

**Copying garbage collection.** A [copying collector](/copying-collection/) allocates new objects by bumping a pointer through the free half of the heap. When the pointer reaches the limit, the collector copies the live objects into the other half, packed together, and allocation goes on from the end of the copies. [Cheney's algorithm](/cheney-copying-collector/) also copies by bumping a pointer through the new half. Appel (1987) argued that, with enough memory, this allocation plus the collection can cost less per object than freeing objects from a stack.

**Generational nurseries.** A [generational collector](/generational-garbage-collection/) allocates in a small young area by bumping a pointer. Most young objects die soon, so the collector copies only a few survivors out, and the nursery is reset.

**Arenas.** An [arena](/arena-allocation/) is a list of chunks, and each chunk is a bump range. Hanson (1990) used this for objects that die together, such as the data of one compiler phase.

**Thread buffers.** Each thread takes a [thread-local allocation buffer](/thread-local-allocation-buffer/) from the shared heap and bumps through it with no lock.

## Variations

- **Bump down.** Start top at the limit and subtract: $p \leftarrow (top - n)$ AND NOT $(a - 1)$, then check $p \ge base$. The rounding down is one mask with no add.
- **Inline fast path.** Compilers for garbage-collected languages put lines L1 to L4 into the code at each allocation, and keep top and limit in registers or in thread-local storage.
- **Mark and release.** Save top and later set it back to the saved value, which frees every block made after the save. This is [stack allocation](/stack-allocation/).
- **Bump allocation in free lines.** Some collectors bump through free gaps between live objects, for example the free lines of the [Immix collector](/immix-collector/), so that the heap need not be packed first.

## Pitfalls

- **Overflow in the limit check.** If $p + n$ can overflow, check $n > limit - p$ instead.
- **Freeing a single block.** A bump allocator cannot take back one block. Code that frees single blocks into it has a bug, or needs a different allocator.
- **Memory held by one live object.** A reset frees the whole range, so it waits for the last object. One long-lived object keeps the whole range in use.
- **Forgetting the alignment.** Without line L1, a block can start at an address that the hardware or the language does not allow for its type.
- **A shared pointer without a lock.** Two threads that bump one pointer at the same time can get the same block. Use an atomic add, or a buffer per thread.

## Exercises

1. Show that the total padding over $k$ calls of BUMP-ALLOC is less than $k \cdot (a_{max} - 1)$, where $a_{max}$ is the largest alignment.
2. Write the bump-down version, with the check against $base$, and run the worked example on it.
3. A program allocates objects of sizes 8 and 24 with alignment 8 in random order. What share of the range is padding?
4. Add `mark()` and `release(m)` to the allocator. What must a caller promise for `release` to be safe?
5. In a copying collector with a heap of $H$ words, half of which is free after each collection, $L$ words are live at each collection. How many words can the program allocate between two collections, and how does the cost of a collection per allocated word change when $H$ grows?

## References
