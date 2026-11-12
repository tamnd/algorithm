---
tag: 2S5369
kind: algorithm
slug: mimalloc
name: mimalloc
area: systems/memory-allocation
level: research
summary: "Microsoft's malloc with free list sharding: each page has its own free list, a local free list and a thread free list, so the fast paths need no atomic operation and the slow path runs regularly."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {k: the number of pages of one size class in the heap of the thread}
  time: {worst: O(k), average: O(1)}
  space: {extra: O(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2019
  people: [Daan Leijen, Benjamin Zorn, Leonardo de Moura]
  note: Written at Microsoft Research as the allocator of the runtimes of the Koka and Lean languages, which use reference counting, and released as a general malloc.
prereqs: [segregated-free-lists, size-classes, free-list]
see_also: [hoard-allocator, tcmalloc, jemalloc, lock-free-memory-allocator, compare-and-swap, treiber-stack, thread-local-allocation-buffer, dlmalloc]
sources:
  - paper: doi:10.1007/978-3-030-34175-6_13
    title: "Daan Leijen, Benjamin Zorn and Leonardo de Moura, Mimalloc: free list sharding in action, APLAS 2019, LNCS 11893, 244-265"
    locator: Section 2 (free list sharding, the local free list, the thread free list), Section 3 (segments and pages, free, the generic allocation routine, the full list)
  - url: https://www.microsoft.com/en-us/research/publication/mimalloc-free-list-sharding-in-action/
    title: "Daan Leijen, Benjamin Zorn and Leonardo de Moura, Mimalloc: free list sharding in action, Microsoft Research technical report MSR-TR-2019-18, June 2019"
    locator: the same sections; the code fragments for malloc_in_page, free and malloc_generic
---

mimalloc is a general-purpose [allocator](/allocator/) by Leijen, Zorn and de Moura, published in 2019. Its main idea is free list sharding: instead of one free list per size class, it keeps a free list per page, a region of usually 64 KiB that holds blocks of one size. It goes further and gives each page three free lists. Allocation pops from the first; frees by the owning thread go to the second; frees by other threads go to the third with an atomic push. Because the first list only shrinks between visits to the slow path, the slow path is guaranteed to run after a bounded number of allocations, and mimalloc uses it for all the expensive work.

## In plain words

Think of a library where each reading table has its own small stack of free cards. When you need a card, you take one from the stack at your table. When you are done with a card, you do not put it back on that stack; you put it in a tray next to it. Cards that people from other tables return go in a locked box at the table.

When the stack is empty, you stop and do your chores: move the cards from the tray and the box to the stack, throw away tables that nobody uses, and check the clock. Because the stack runs out after a known number of cards, the chores happen often and on a fixed rhythm.

## The problem

This is [online memory allocation](/online-memory-allocation/) for programs with many threads, and in particular for language runtimes with reference counting, such as those of Koka, Lean, Swift and Python. They allocate and free very many small objects, often in long chains when a large structure is freed. Their authors wanted a malloc with a fast path that has one test and no atomic operation, good locality, bounded worst-case time, and a regular point at which to do deferred work, for example the rest of a long chain of reference count decrements.

## The algorithm

Memory comes from the system in segments of 4 MiB, aligned to 4 MiB. A segment holds small pages (64 pages of 64 KiB for objects under 8 KiB) or one large page; the segment belongs to one thread. Each thread has a heap: for each size class, a list of its pages and a direct pointer to the page to allocate from. A page holds blocks of one size and has:

- free: the list that malloc pops from;
- local_free: blocks freed by the owning thread;
- thread_free: blocks freed by other threads, pushed atomically;
- used: blocks handed out and not yet freed locally or collected;
- thread_freed: blocks on thread_free.

So the blocks in use in a page number used − thread_freed.

```pseudo id=main
MALLOC(n) in thread t
L1  page ← heap(t).direct[class(n)]
L2  if page.free is empty then return GENERIC(n)
L3  pop a block b from page.free; page.used ← page.used + 1; return b

FREE(p) in thread t
L4  segment ← p rounded down to a multiple of 4 MiB; page ← segment.pages[(p − segment) / page size]
L5  if t is the thread of segment then
L6      push p on page.local_free; page.used ← page.used − 1
L7      if page.used − page.thread_freed = 0 then free the page
L8  else atomically push p on page.thread_free; atomically add 1 to page.thread_freed

GENERIC(n) in thread t
L9  call deferred_free                                 ▷ the heartbeat for the runtime
L10 for each page of class(n) in heap(t) do
L11     move page.local_free to page.free; atomically take page.thread_free, move it to page.free,
            and subtract its length from used and thread_freed
L12     if page.used − page.thread_freed = 0 then free the page
L13     else if page.free is not empty then heap(t).direct[class(n)] ← page; return MALLOC(n)
L14 take a fresh page for class(n) from a segment of t, or from a new segment; make it direct; return MALLOC(n)
```

**The fast paths.** MALLOC (L1 to L3) has one test and a pop. The paper's version for objects under 1 KiB indexes the direct array by $(n + 7)/8$. FREE (L4 to L8) finds the segment by masking the low bits of $p$ and the page by a shift, so it needs no header in the block. A free by the owner pushes on local_free with plain stores. Only a free by another thread uses atomic operations, and it touches only the page, so threads that free into different pages do not contend.

**The three lists.** Frees never go to page.free. So between two calls of GENERIC, page.free only shrinks, and a thread can do at most as many fast allocations in a size class as one page has blocks before L2 sends it to GENERIC. That is the temporal cadence of the paper: deferred_free at L9 is called regularly, and the Lean runtime uses it as a deterministic heartbeat, a timer that gives the same result on every machine.

**The generic routine** (L9 to L14). It walks the pages of the size class, collects their local and thread free lists, frees pages that have no live blocks, and stops at the first page with a free block. Only if no page has room does it take a fresh page. The paper notes that the real code bounds the number of pages freed in one call, keeps some freed pages in a cache, and rotates the list so that the next search starts where this one stopped.

## Example

The code of this page is a small model of mimalloc in Python, not the real allocator: it runs in one thread, counts atomic operations instead of doing them, and only computes addresses. This trace uses the model with pages of 128 bytes, so a page holds 8 blocks of 16 bytes; addresses are written as offsets from the start of the segment. Thread 0 owns the page.

| Step | Call | Path | free | local_free | thread_free | used, thread_freed |
|---|---|---|---|---|---|---|
| 1 | thread 0: malloc(16) | no page: GENERIC, fresh page (L14), then pop (L3): 0 | 16 to 112 | | | 1, 0 |
| 2 | thread 0: malloc(16) seven times | fast (L3): 16, 32, ..., 112 | | | | 8, 0 |
| 3 | thread 0: free(16) | local (L6) | | 16 | | 7, 0 |
| 4 | thread 1: free(32) | remote (L8): 2 atomic operations | | 16 | 32 | 7, 1 |
| 5 | thread 0: malloc(16) | free is empty: GENERIC collects (L11), 1 atomic swap; pop: 16 | 32 | | | 7, 0 |
| 6 | thread 0: malloc(16) | fast (L3): 32 | | | | 8, 0 |
| 7 | thread 0: free all 8 blocks | local (L6); at the last one used − thread_freed = 0, so the page is freed (L7) | | | | page gone |

At step 3 the block does not go back to free, though the owner frees it, so step 5 must take the slow path. That is the point: after at most 8 fast allocations here, GENERIC runs and the heartbeat ticks. In the whole trace the owning thread did no atomic operation except the swap at step 5.

## Correctness

Every block of a page is in exactly one place: on free, on local_free, on thread_free, or handed out. L3 moves a block from free to the caller, L6 and L8 move it from the caller to one of the other two lists, and L11 moves whole lists to free. The counters follow the same moves, so used = (blocks handed out) + (blocks on thread_free) and thread_freed = (blocks on thread_free). Hence used − thread_freed is the number of live blocks, and a page is freed at L7 or L12 only when none of its blocks is live. The free list only shrinks between calls of GENERIC, which gives the bound on fast allocations. The proof, including the case of a concurrent remote free, is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Fast paths.** MALLOC with a nonempty free list and FREE take $O(1)$ time with a few instructions; a local free needs no atomic operation, a remote free needs one compare-and-swap loop and one atomic increment.
- **Generic.** One call walks up to $k$ pages of the size class, so it takes $O(k)$ time plus the length of the lists it joins (the real code links lists in $O(1)$ by keeping their ends). The real code also bounds the work per call. Each call is preceded by many fast allocations when pages are large, so the amortized cost per allocation is $O(1)$.
- **Space.** Page and segment metadata are about 0.2% of memory by the paper's count, and the size classes waste at most a fixed fraction of each block.

## Properties

- **Locality.** A thread allocates from one page until the page is full, so objects allocated together lie together, whatever was freed in other pages. The paper credits much of mimalloc's speed to this.
- **No locks.** All interaction between threads is through atomic operations on the thread_free list of one page (and, in the real code, a per-heap list for delayed frees).
- **Regular slow path.** The generic routine is guaranteed to run after a bounded number of allocations, which supports deferred freeing and a deterministic heartbeat.
- **Bounded worst-case time.** With a bound on the work of one generic call, every call takes bounded time.
- **Remote frees are delayed.** A block freed by another thread becomes reusable only when the owner runs GENERIC on that page.

## Variants and improvements

- **The full list.** Pages that are full are moved to a separate list so that GENERIC does not walk them. A remote free into a full page then pushes the block on a per-heap delayed free list instead, so the owner learns that the page has room. Two low bits of the thread_free pointer encode the states NORMAL, DELAYED and DELAYING.
- **Secure mode.** A variant with guard pages, encoded free list pointers and randomized free lists in fresh pages, at a small cost in speed.
- **Related designs.** [Hoard](/hoard-allocator/) introduced superblocks owned by one heap; a mimalloc page plays the same role. [tcmalloc](/tcmalloc/) and [jemalloc](/jemalloc/) use thread or CPU caches over shared size-class structures instead of thread-owned pages.

## When to use it

Use mimalloc as a drop-in malloc for programs with many threads and many small objects, and as the allocator of a language runtime that needs regular callbacks for deferred work. Its fast paths are short and its locality is good, which the paper reports as faster than tcmalloc and jemalloc on redis by 7% and 14%. It is less suited to workloads where one thread allocates and others free most objects, because remote frees are delayed until the owner collects them; the paper notes such asymmetric workloads as a case it had to handle with care.

## Pitfalls

- **Putting freed blocks back on page.free.** If L6 pushed on page.free instead of local_free, a thread that frees and allocates in one page would never empty page.free, GENERIC would never run, and the heartbeat and deferred frees would stop.
- **Overwriting page.free when collecting.** The paper's sketch of page_collect writes page.free ← page.local_free. That is correct only when page.free is empty, which is the case for the direct page at L2 but not for the other pages that L10 walks. L11 must append the lists, or blocks are lost.
- **Counting live blocks with used alone.** A remote free changes thread_freed, not used. A test of used = 0 at L7 would never free a page whose last block was freed by another thread before collection; the test is used − thread_freed = 0.
- **Reading thread_freed without care.** L7 reads thread_freed, which other threads change, without a barrier. The paper accepts that it may miss the moment when the page becomes empty, because GENERIC will find and free the page later.
- **Allocating from another thread's heap.** MALLOC uses only the heap of the calling thread. Taking blocks from a page of another heap would race with its owner's plain pops at L3.

## Implementations

## History

Daan Leijen, Benjamin Zorn and Leonardo de Moura wrote mimalloc at Microsoft Research for the runtimes of Koka and Lean, which use reference counting and needed bounded pause times and a regular point for deferred decrements. The technical report MSR-TR-2019-18 appeared in June 2019, and the paper was presented at APLAS 2019. Free list sharding per page had appeared before in other allocators, such as VAM and early versions of phkmalloc, as the paper notes; mimalloc combined it with the local and thread free lists. The core library had less than 3500 lines in 2019, against about 20,000 for tcmalloc and 25,000 for jemalloc by the paper's count.

## References
