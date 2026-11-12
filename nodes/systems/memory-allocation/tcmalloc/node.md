---
tag: XSTE1X
kind: algorithm
slug: tcmalloc
name: tcmalloc
aliases:
- thread-caching malloc
area: systems/memory-allocation
level: advanced
summary: "Google's malloc: a cache per thread (now per CPU) with one free list per size class, central free lists that move objects in batches, and a page heap of spans found through a radix-tree pagemap."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {b: the batch size of a size class, s: the number of free spans in the page heap}
  time: {worst: O(b + s), average: O(1)}
  space: {extra: O(s)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2005
  people: [Sanjay Ghemawat]
  note: Written at Google and released in the gperftools package. Later versions use per-CPU caches with restartable sequences and a hugepage-aware page heap (Temeraire, OSDI 2021).
prereqs: [size-classes, segregated-free-lists, free-list]
see_also: [hoard-allocator, jemalloc, mimalloc, dlmalloc, slab-allocator, thread-local-allocation-buffer, buddy-system, best-fit-allocation]
sources:
  - url: https://gperftools.github.io/gperftools/tcmalloc.html
    title: "Sanjay Ghemawat, TCMalloc: Thread-Caching Malloc, gperftools documentation"
    locator: the sections on overview, small object allocation, large object allocation, spans, deallocation, central free lists, garbage collection of thread caches (low-water mark, slow start)
  - url: https://www.usenix.org/conference/osdi21/presentation/hunter
    title: "A. H. Hunter, Chris Kennelly, Paul Turner, Darryl Gove, Tipp Moseley and Parthasarathy Ranganathan, Beyond malloc efficiency to fleet efficiency: a hugepage-aware memory allocator, OSDI 2021, 257-273"
    locator: the description of the TCMalloc design (per-CPU caches, transfer cache, central free list, page heap) and the hugepage-aware page heap Temeraire
  - url: https://google.github.io/tcmalloc/design.html
    title: "Google, TCMalloc: overview of the design"
    locator: the sections on the front-end (per-CPU and per-thread modes, restartable sequences), the transfer cache, the central free list, the pagemap and the back-end
---

tcmalloc is the [allocator](/allocator/) that Sanjay Ghemawat and colleagues wrote at Google, first released around 2005 in the gperftools package. Its name means thread-caching malloc. Each thread has a cache with one free list per [size class](/size-classes/), so most calls of malloc and free touch only that cache and take no lock. When a list is empty or too long, objects move in batches to and from a central free list for the class, which carves spans of pages into objects. Spans come from a page heap, which finds the span of any address through a radix tree called the pagemap. Current versions keep a cache per CPU instead of per thread and use a hugepage-aware page heap.

## In plain words

Think of a chain of shops. Each clerk has a small drawer of items for each size, so most sales need no trip to the back. When a drawer is empty, the clerk fetches a whole bundle from the store room, and when a drawer overflows, the clerk carries a bundle back. Bundles start small and grow for clerks who sell a lot.

The store room cuts big boxes into items of one size. The big boxes come from a warehouse that keeps empty space in runs of shelves. A map tells, for any shelf, which box it belongs to. Every so often, a clerk whose drawers hold too much returns half of the items that were never touched since the last check.

## The problem

This is [online memory allocation](/online-memory-allocation/) for C and C++ servers with many threads. A single heap with one lock, as in [dlmalloc](/dlmalloc/), serializes threads. The gperftools document reports that ptmalloc2, the glibc malloc of the time, took about 300 ns for a malloc and free pair of a small object on a 2.8 GHz Pentium 4, against about 50 ns for tcmalloc. The goal is a fast path with no lock, little memory overhead per object, and caches that do not keep too much memory away from other threads.

## The algorithm

Small objects (up to 256 KiB in current gperftools; the model uses 1 KiB) are rounded up to one of about 88 size classes, spaced 8 bytes apart for small sizes and then wider. Each class $c$ has a batch size $b(c)$, the number of objects moved at once. Memory is managed in pages of 8 KiB; a span is a run of pages, either free or used for one large object or for the objects of one class.

A thread cache list $L$ has a length, a maximum length $L.\mathit{max}$ (the slow start), and a low-water mark $L.\mathit{low}$, the smallest length since the last scavenge.

```pseudo id=main
MALLOC(n) in thread t
L1  if n > MAX_SMALL then return the start of PAGEHEAP-ALLOC(⌈n / PAGE⌉)
L2  c ← class(n); L ← cache(t).list[c]
L3  if L is not empty then pop an object, update L.low, and return it          ▷ no lock
L4  get k = min(L.max, b(c)) objects from central[c]; if central[c] has none, carve a new span from the page heap
L5  slow start: if L.max < b(c) then L.max ← L.max + 1 else L.max ← L.max + b(c), rounded down to a multiple of b(c)
L6  return one of the k objects and push the others on L

FREE(p) in thread t
L7  s ← pagemap[p / PAGE]; if s holds a large object then PAGEHEAP-FREE(s); return
L8  push p on L = cache(t).list[class of s]
L9  if length(L) > L.max then move b(c) objects of L to central[c] and adjust L.max
L10 if the size of cache(t) > its limit then SCAVENGE(t)

SCAVENGE(t)
L11 for each list L of cache(t): if L.low > 0 then move max(1, ⌊L.low/2⌋) objects to central and lower L.max; L.low ← length(L)

CENTRAL-INSERT(c, objects)
L12 for each object: push it on its span (found by the pagemap); if no object of the span is out, return the span to the page heap

PAGEHEAP-ALLOC(k) and PAGEHEAP-FREE(s)
L13 alloc: take the free span with the fewest pages ≥ k (growing the heap if none), split off k pages, record them in the pagemap
L14 free: merge s with the free spans just before and after it, found by the pagemap
```

**The fast path** (L1 to L3 and L7, L8). A malloc that finds an object in its list and a free that keeps its object in the list touch only the thread's own cache. The pagemap lookup at L7 replaces a header in each object, so small objects have no per-object overhead.

**Batches and slow start** (L4, L5, L9). Visits to the central list, which has a lock, move up to $b(c)$ objects at a time. A list starts with a maximum length of 1 and grows by 1 per visit, so a thread that allocates one object of a class does not get a whole batch; once the maximum reaches $b(c)$, it grows in steps of $b(c)$. When a list grows too long on frees, a batch goes back. In gperftools, repeated overflows also lower the maximum.

**Scavenging** (L10, L11). The total size of each thread cache is limited. When a free goes over the limit, each list returns half of its low-water mark: those objects were not used at all since the last scavenge, so they are likely not needed. The gperftools document describes this as garbage collection of thread caches. It also moves cache space between threads, which the model leaves out.

**Central lists and the page heap** (L12 to L14). A central list keeps the spans of its class that have free objects. When all objects of a span come back, the span returns to the page heap. The page heap keeps free spans by length, 128 lists for short spans and a sorted set for long ones, and uses best fit. Freed spans join their free neighbors, found through the pagemap, so the page heap behaves like [best fit](/best-fit-allocation/) with [coalescing](/coalescing/) on pages.

## Example

The code of this page is a small model of tcmalloc in Python, not the real allocator: it runs in one thread, counts locks instead of taking them, and only computes addresses. This trace uses the model with the default limits. Class 104 holds requests of 97 to 104 bytes and has a batch size of 32. The page heap grows by 16 pages at a time.

| Step | Call | Action | Central visits | Thread 0 list of class 104 | $L.\mathit{max}$ |
|---|---|---|---|---|---|
| 1 | thread 0: malloc(100) | list empty; the page heap grows to 16 pages, page 0 becomes a span of class 104; fetch min(1, 32) = 1 object; return 0 | 1 | empty | 2 |
| 2 | thread 0: malloc(100) | list empty; fetch 2; return 104, keep 208 | 2 | 208 | 3 |
| 3 | thread 0: malloc(100) | fast path: return 208 | 2 | empty | 3 |
| 4 | thread 1: free(0) | the pagemap says class 104; push on thread 1's list | 2 | empty | 3 |
| 5 | thread 0: malloc(20000) | large: 3 pages from the page heap, pages 1 to 3; return 8192 | 2 | empty | 3 |
| 6 | thread 0: free(8192) | the span joins the free pages 4 to 15 (L14) | 2 | empty | 3 |

At step 4 the object goes to the cache of the thread that frees it, not to the thread that allocated it; it will move back to the central list only in a batch or by scavenging. At step 6 the page heap again has one free span of 15 pages.

## Correctness

Every object of a span of a small class is in exactly one place: on the free list of its span, on a thread cache list, or held by the program. The span's count of objects out equals the number in the last two places, so a span returns to the page heap only when none of its objects is in use. The page heap keeps the spans as a tiling of the heap with no two free spans adjacent, and the pagemap maps every page to its span. These invariants are shown in [the correctness proof](proofs/correctness.md). The proof also shows that $L.\mathit{max}$ is a target, not a bound: after the maximum drops, a list can hold more objects than it for a while.

## Complexity

- **Fast path.** $O(1)$ time with no lock and no atomic instruction in the per-thread design.
- **Central visit.** $O(b)$ for a batch of $b$ objects, with one lock on the central list of one class. Since the list then serves up to $b$ calls, the cost per call is $O(1)$ amortized once the slow start has grown the list.
- **Page heap.** gperftools uses 128 exact lists and a red-black tree, so a search takes $O(\log s)$ for $s$ free spans; the model scans in $O(s)$. The pagemap is a radix tree with two or three levels, so a lookup is $O(1)$.
- **Space.** No header per small object; the pagemap and the span records cost a few bytes per page; the thread caches hold up to a configured total (TCMALLOC_MAX_TOTAL_THREAD_CACHE_BYTES in gperftools).

## Properties

- **No per-object header.** The pagemap gives the class of any address, so small objects use only their class size, and [internal fragmentation](/internal-fragmentation/) comes only from rounding to the class.
- **Remote frees are cheap.** A thread frees into its own cache whatever thread allocated the object. The price is that memory can move from one thread's cache to another and sit there until scavenging.
- **Bounded caches.** The total held in caches is limited, and scavenging returns objects that were not used.
- **Not a strict bound.** Unlike [Hoard](/hoard-allocator/), there is no proof of a bound on blowup; the limits are tuning parameters.

## Variants and improvements

- **Per-CPU caches.** The current tcmalloc from Google keeps one cache per logical CPU instead of per thread. A thread updates the cache of the CPU it runs on inside a restartable sequence (rseq) of Linux: if the thread is moved or interrupted in the middle, the kernel restarts the sequence, so no lock and no atomic instruction is needed. The memory in caches then scales with the number of CPUs, not of threads.
- **Transfer cache.** Between the front-end caches and the central free lists sits a transfer cache per class, an array of batches, so that a batch freed by one CPU can be handed to another with little work.
- **Temeraire.** Hunter et al. (OSDI 2021) made the page heap hugepage-aware: it places spans so that whole 2 MiB hugepages stay used or become empty, which raises hugepage coverage. In a fleet-wide study at Google they report 6% fewer TLB miss stalls and 26% less memory lost to fragmentation, and in 8 applications 7.7% more requests per second.
- **Related allocators.** [jemalloc](/jemalloc/) uses several arenas and thread caches; [mimalloc](/mimalloc/) uses pages owned by threads with separate lists for remote frees.

## When to use it

Use tcmalloc for servers with many threads that allocate many small objects, where malloc speed and lock contention matter. The per-CPU version suits machines with many threads per CPU. For programs with one thread, it gives little over a good serial allocator. For tight memory budgets, tune the cache limits, since memory in caches is not available to other threads at once.

## Pitfalls

- **Giving a full batch on the first miss.** If L4 always fetched $b(c)$ objects, a program with many threads that each allocate one object of many classes would fill every cache with unused objects. The slow start at L5 prevents this.
- **Scavenging by length instead of low-water mark.** If L11 released half of the current length, a list in steady use would be emptied and refilled again and again. The low-water mark releases only objects that were not touched.
- **Returning a span while objects are cached.** A span may return to the page heap at L12 only when no object is out, counting objects in thread caches as out. Counting only objects held by the program would free a span whose objects sit in some cache.
- **A stale pagemap.** L13 and L14 must update the pagemap for the pages of every span they split or merge; at least the first and last page of a free span, and every page of a span in use, must map to it. Otherwise L7 or L14 finds the wrong span.
- **Unbounded per-thread memory.** With thousands of threads, per-thread caches can hold a lot of memory even with a per-thread limit; this was one reason for the move to per-CPU caches.

## Implementations

## History

Sanjay Ghemawat and colleagues developed tcmalloc at Google in the early 2000s and released it with the google-perftools package (later gperftools) around 2005; the design document is by Ghemawat. It became the default allocator of many Google services and was adopted by other projects. Google later rewrote it with per-CPU caches built on restartable sequences, a feature added to Linux in version 4.18, and released this version separately in 2020. In 2021 Hunter, Kennelly, Turner, Gove, Moseley and Ranganathan described its hugepage-aware page heap, Temeraire, at OSDI and measured its effect on the whole fleet.

## References
