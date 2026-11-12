---
tag: WB0SXP
kind: technique
slug: arena-allocation
name: Arena allocation
aliases:
- arena allocator
- Hanson arenas
area: systems/memory-allocation
level: intro
summary: "Put objects that die together in one arena, a list of chunks served by a bump pointer, and free the whole arena in one step. The chunks go to a free list for reuse."
prereqs: [bump-pointer-allocation]
see_also: [region-based-memory-management, stack-allocation, memory-pool, slab-allocator, allocator, free-list, internal-fragmentation, thread-local-allocation-buffer]
sources:
  - paper: doi:10.1002/spe.4380200104
    title: David R. Hanson, Fast allocation and deallocation of memory based on object lifetimes, Software, Practice and Experience 20(1), 1990, 5-12
    locator: the arena interface (allocate in an arena, free a whole arena), the chunk list of each arena and the shared list of free chunks
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: the discussion of allocators that exploit object lifetimes and free groups of objects at once
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, CRC Press, 2011
    locator: Chapter 7, Allocation, Section 7.1, Sequential allocation
---

*Arena allocation* groups objects by their lifetime. A program makes an *arena* for a set of objects that will all die at the same time, such as the data of one request, one frame or one compiler phase. It allocates them in the arena by [bump-pointer allocation](/bump-pointer-allocation/) and never frees them one by one. When the set dies, one call frees the whole arena. An arena is a list of *chunks*, large blocks from the system. When the current chunk is full, the arena takes another one, so an arena can grow without a fixed size. David Hanson described this design in 1990 for the lcc compiler. Arenas are a run-time technique that the programmer controls; [region-based memory management](/region-based-memory-management/) is the related language discipline in which a compiler places objects in regions and checks that no object is used after its region is freed.

## In plain words

Imagine a party where every guest gets paper plates, cups and napkins. Nobody washes a single plate. When the party ends, you throw away the whole table cover with everything on it.

An arena works the same way for memory. Objects that belong to one job go into one arena, side by side, as fast as a pointer can move. When the job ends, the arena drops them all in one step. The large blocks of memory are not given back to the system: the next arena uses them again.

## When it applies

- Many objects share one lifetime that the program knows, for example the nodes of a parse tree, the strings of one web request or the temporary data of one game frame.
- Objects are small and many, so the cost of a general `malloc` and `free` per object, and of a header per object, matters.
- The program would otherwise need to walk a data structure only to free it.
- No object of the arena is needed after the arena is freed, or the few that are can be copied out first.

## The template

A shared list FREECHUNKS holds the chunks of freed arenas. An arena $A$ has a list of chunks and a bump range $[A.avail, A.limit)$ inside its last chunk. $K$ is the extra room of a new chunk. The size $n$ is already rounded up to the alignment.

```pseudo id=main
ARENA-ALLOC(A, n)
L1  while A.limit − A.avail < n do
L2      if FREECHUNKS is not empty then c ← pop FREECHUNKS
L3      else c ← a new chunk of n + K bytes from the system
L4      append c to the chunks of A; (A.avail, A.limit) ← (start of c, end of c)
L5  p ← A.avail; A.avail ← A.avail + n; return p

ARENA-FREE-ALL(A)
L6  move all chunks of A to FREECHUNKS; A.avail ← A.limit ← 0
```

Each block lies inside one chunk of $A$, below $A.avail$, and blocks of the same chunk do not overlap, so ARENA-ALLOC never returns memory in use. ARENA-FREE-ALL takes time in the number of chunks, not in the number of objects. This loop follows the shape of Hanson's code: a reused chunk that is too small stays in the arena, unused, until the arena is freed. The loop ends at the latest when it asks the system for a chunk of $n + K$ bytes.

## Classic examples

**A worked run.** $K = 64$ and the alignment is 8. The system gives fresh addresses from 0.

| call | rounded | result | chunks of the arena | note |
|---|---|---|---|---|
| a.alloc(10) | 16 | 0 | [0, 80) | a new chunk of $16 + 64$ bytes |
| a.alloc(20) | 24 | 16 | [0, 80) | 40 bytes left |
| a.alloc(50) | 56 | 80 | [0, 80), [80, 200) | 40 < 56: a new chunk |
| a.alloc(30) | 32 | 136 | same | |
| a.alloc(40) | 40 | 200 | three chunks, the last [200, 304) | 32 < 40 |
| a.free_all() | | | none | FREECHUNKS: [200, 304), [80, 200), [0, 80) |
| b.alloc(100) | 104 | 80 | [0, 80), [80, 200) | [0, 80) is too small; [80, 200) fits |
| b.alloc(8) | 8 | 184 | same | |

The second arena gets all its memory from FREECHUNKS: the system gave out three chunks in total. The chunk [0, 80) is held by arena $b$ but not used, which is the price of the simple loop.

**The lcc compiler.** Hanson's arenas came from lcc, a C compiler. It kept one arena for objects that live for the whole compilation, one for the objects of a function, and one for the objects of a statement, and freed each arena when its part of the program was done.

**Servers and frameworks.** The Apache Portable Runtime uses *pools* of this kind, one per connection and per request. PostgreSQL uses *memory contexts* that are freed at the end of a query or a transaction. GNU *obstacks* are arenas that also allow freeing back to a saved point.

**Library support.** C++17 has `std::pmr::monotonic_buffer_resource`, an arena that frees only when it is destroyed. Many game engines use a *frame allocator* that is reset once per frame.

## Variations

- **Mark and release.** Save the current position of the arena and later free all objects made after it. With one chunk this is [stack allocation](/stack-allocation/); obstacks allow it across chunks.
- **Reset without return.** Keep the chunks in the arena and only move the pointer back to the start of the first chunk, for an arena that is used again and again, such as a frame allocator.
- **Large objects.** Give an object larger than a chunk its own chunk, so that one large request does not waste the rest of the current chunk.
- **Nested arenas.** Make an arena for a sub-task and free it when the sub-task ends, while the parent arena lives on, as with APR subpools and PostgreSQL child contexts.
- **Per-thread arenas.** Give each thread its own arena to avoid locks, as a [thread-local allocation buffer](/thread-local-allocation-buffer/) does for one bump range.

## Pitfalls

- **Dangling pointers.** After ARENA-FREE-ALL, every pointer into the arena is invalid, and the next arena reuses the memory. A pointer that is kept by mistake reads another object's data. Region type systems exist to catch this error at compile time.
- **Mixed lifetimes.** One long-lived object in a short-lived arena keeps the whole arena alive, or forces a copy. Put each object in the arena of its lifetime.
- **Unbounded growth.** An arena that lives for the whole run and gets many short-lived objects grows without limit, because it frees nothing until the end.
- **Waste at the end of chunks.** When a request does not fit, the rest of the current chunk is lost until the arena is freed. Large requests in small chunks waste the most.
- **Destructors.** An arena frees memory, but it does not run clean-up code for objects that hold files or locks. Keep a list of clean-up actions in the arena, as APR pools do.

## Exercises

1. Show that in ARENA-ALLOC the memory wasted in an arena, at the ends of chunks, is less than the number of chunks times the largest request.
2. Change ARENA-ALLOC so that a chunk from FREECHUNKS that is too small goes back to the list instead of into the arena. What is the cost of this change?
3. Add `mark()` and `release(m)` to the arena, and state when `release` is safe.
4. A compiler frees a statement arena after each statement. Which objects of a statement must not go into it?
5. Compare an arena with a [memory pool](/memory-pool/) for objects of one size whose lifetimes differ.

## References
