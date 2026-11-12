---
tag: T3R2XK
kind: algorithm
slug: slab-allocator
name: Slab allocator
aliases:
- slab allocation
- Bonwick slab allocator
area: systems/memory-allocation
level: advanced
summary: "A kernel allocator with one cache per object type. Each cache cuts pages into slabs of built objects, reuses freed objects before it makes a new slab, and gives free slabs back on demand."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {p: the number of objects in a slab, m: the number of slabs of the cache}
  time: {alloc: O(1), grow: O(p), free: O(1), reap: O(p m)}
  space: {extra: Θ(m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1994
  people: [Jeff Bonwick]
  note: Bonwick designed the slab allocator for the SunOS 5.4 kernel and presented it at the USENIX Summer 1994 conference; with Jonathan Adams he added per-CPU magazines and the vmem allocator in 2001.
prereqs: [memory-pool, size-classes]
see_also: [segregated-free-lists, buddy-system, lazy-buddy-system, type-stable-memory, free-list, thread-local-allocation-buffer, internal-fragmentation, jemalloc]
sources:
  - paper: "Jeff Bonwick, The slab allocator, an object-caching kernel memory allocator, USENIX Summer 1994 Technical Conference, Boston, 87-98"
    locator: Section 3 (object caching, the cache interface, slabs and the freelist of each cache, reclaiming memory with kmem_cache_reap) and Section 4.3 (slab coloring)
  - paper: "Jeff Bonwick and Jonathan Adams, Magazines and vmem, extending the slab allocator to many CPUs and arbitrary resources, USENIX Annual Technical Conference, 2001"
    locator: the magazine layer of per-CPU caches on top of the slab layer, and the vmem resource allocator
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 10, Allocating kernel memory (the buddy system and slab allocation)
  - book: isbn:9780131019089
    title: Uresh Vahalia, UNIX Internals, The New Frontiers, Prentice Hall, 1996
    locator: Chapter 12, Kernel memory allocation (the Solaris slab allocator)
---

The slab allocator is a kernel memory allocator built around *object caches*. Each cache serves objects of one type and size, such as process descriptors or file handles. A cache gets memory from the page allocator one *slab* at a time: a page, or a few pages, cut into objects of the cache's size. Its central idea is that a freed object stays *built*: the cache runs the object's constructor once when it makes the slab, and an object that comes back keeps its built state, so the next allocation skips the constructor. A cache always reuses a free object of an existing slab before it makes a new slab, and it keeps wholly free slabs until the system asks for memory back.

## In plain words

A restaurant does not wash, fold and set a new napkin for each guest from scratch. It keeps stacks of napkins that are ready to use, one stack per kind. When a guest leaves, the napkin goes back to its stack still folded, if it is clean, and the next guest takes it as it is.

The slab allocator does the same with kernel objects. Each kind of object has its own cache. The cache takes whole pages of memory and cuts each page into objects of its kind, all set up at once. A freed object goes back to its page still set up. New pages are taken only when every page of the cache is in full use. Pages whose objects are all free stay in the cache, until the system runs short of memory and asks for them back.

## The problem

The kernel needs many small objects of a few fixed types, and it allocates and frees them very often. A general [allocator](/allocator/) wastes time here in two ways. It searches for a block of the right size, and the code that uses the object must build it again after each allocation: set its locks, its lists and its fields to their start values. The slab allocator solves the problem of [online memory allocation](/online-memory-allocation/) for a fixed set of object types, with the extra aim of keeping objects built.

**Interface.** `cache_create(size, align, ctor, dtor)` makes a cache. `cache_alloc(cache)` returns a built object, and `cache_free(cache, obj)` returns it. `cache_reap(cache)` gives the pages of wholly free slabs back to the page allocator. In Bonwick's Solaris kernel these are kmem_cache_create, kmem_cache_alloc, kmem_cache_free and kmem_cache_reap.

## The algorithm

A slab is one page of $P$ words that holds $p = \lfloor P / s \rfloor$ objects of $s$ words, a count of objects in use, and a free list of its free objects. The cache sorts its slabs into three groups: *full* (no free object), *partial* and *wholly free* (no object in use). Bonwick kept one list of slabs sorted in this order; the Linux implementation keeps three lists.

```pseudo id=main
SLAB-ALLOC(cache)
L1  if the cache has a partial slab then s ← a partial slab
L2  else if it has a wholly free slab then s ← that slab
L3  else s ← CACHE-GROW(cache); FAIL if no page is left
L4  obj ← pop the free list of s; s.inuse ← s.inuse + 1
L5  move s to the full or partial group, by its count
L6  return obj                                   ▷ already built

SLAB-FREE(cache, obj)
L7  s ← the slab of obj                          ▷ round the address down to the page
L8  push obj on the free list of s; s.inuse ← s.inuse − 1
L9  move s to the partial or wholly free group, by its count

CACHE-GROW(cache)
L10 page ← get a page from the page allocator; FAIL if none
L11 c ← the next color offset of the cache
L12 cut the page from offset c into p objects, run the constructor on each, link them

CACHE-REAP(cache)
L13 for each wholly free slab: run the destructor on each object, give back the page
```

**Coloring.** A page of $P$ words holds $p$ objects and leaves $P - p s$ words unused. Line L11 moves the first object of each new slab by $0, a, 2a, \ldots$ words, up to the unused space, and then starts again at 0. Without coloring, the objects at the same index in all slabs would sit at the same offset in their pages, and on a machine whose cache index uses low address bits, they would compete for the same cache lines. With coloring they spread over more lines.

**Finding the slab.** For small objects, Bonwick keeps the slab data at the end of the page, so line L7 finds it by rounding the address down to the start of the page. For large objects, the slab data lives outside the page, and a hash table maps each object to it.

## Example

A cache of objects of $s = 3$ words, with pages of $P = 16$ words and alignment $a = 1$. A slab holds $p = 5$ objects and leaves 1 word, so the color offsets are 0 and 1.

| step | call | result | slabs | constructor calls |
|---|---|---|---|---|
| 1 | five allocations | 0, 3, 6, 9, 12 | slab at 0 (color 0) is full | 5 |
| 2 | free(6) | | slab at 0 is partial | 5 |
| 3 | alloc | 6 | the free object of slab 0 comes back; slab 0 is full again | 5 |
| 4 | alloc | 17 | no slab has a free object: a new slab at 16 with color 1 holds 17, 20, 23, 26, 29 | 10 |
| 5 | free(17) | | slab at 16 is wholly free, but the cache keeps it | 10 |
| 6 | reap | 1 page | the destructor runs 5 times, and page 16 goes back | 10 |

Step 3 shows reuse before growth: the object at 6 comes back built, with no constructor call. Step 4 is the only step that takes a new page, and its first object sits at 17, not 16, because of the color. Step 5 shows that a wholly free slab stays in the cache until a reap.

## Correctness

The slab allocator keeps these invariants. Each object of a slab is either in use or on the free list of its slab, never both, so `alloc` never returns an object in use. Each slab is in the group that its count gives. The constructor has run on every object of every slab, exactly once since the slab was made, and the destructor runs only when a reap gives the slab back, so a free object is always built. Line L1 or L2 finds a slab with a free object whenever one exists, so a new slab is made only when every slab is full, and a reap gives back exactly the slabs with no object in use. The full proof is in the [correctness proof](proofs/correctness.md). The page's tests check all of these facts on a seeded random sequence of 2000 calls.

## Complexity

In the [word RAM](/word-ram/), with the groups as doubly linked lists:

- **alloc** takes $O(1)$ time when a slab has a free object. When it makes a new slab, it cuts the page and runs $p$ constructors, so $O(p)$ time plus the constructors. Each slab is made once for $p$ objects, so the cost per object is $O(1)$ [amortized](/amortized-cost/) as long as slabs are not made and reaped again and again.
- **free** takes $O(1)$ time: one address computation, one push and one group move.
- **reap** takes $O(p)$ time per slab, plus the destructors.
- **Space.** A slab needs a count and a free list head; the links of the free list sit in the free objects, as in a [memory pool](/memory-pool/). The waste per slab is the $P - p s$ words that do not hold an object, which is less than $s$ words. So for small objects the waste is a small share of the page, and for large objects Bonwick uses slabs of several pages to keep it small.

## Properties

- **Object caching.** Objects keep their built state between uses, so the cost of construction moves from each allocation to the creation of a slab.
- **No external fragmentation inside a cache.** All objects of a cache have the same size, so every free object fits every request of the cache.
- **Partial slabs first.** Taking from partial slabs fills them up and lets other slabs become wholly free, so that they can be reaped.
- **Type-stable memory.** Memory of a cache holds objects of one type until it is reaped, which some lock-free code relies on; see [type-stable memory](/type-stable-memory/).

## Variants and improvements

- **Magazines.** Bonwick and Adams (2001) put a per-CPU layer on top of the slab layer. Each CPU holds *magazines*, small stacks of objects, and serves most calls from them with no lock. Only full or empty magazines go to a shared depot, so the slab layer sees a small share of the calls. The same paper adds vmem, a general allocator for resources such as address ranges.
- **Linux SLAB and SLUB.** Linux adopted a slab allocator with three slab lists per cache, written by Mark Hemment, and later replaced it with SLUB, a simpler design without the object queues of SLAB.
- **Size-class caches.** A kernel can serve `kmalloc` requests of any size with a set of caches for a list of [size classes](/size-classes/), which is simple segregated storage built on slabs.
- **Reaping policy.** Bonwick's allocator reaps when the virtual memory system needs pages. Other designs reap on a timer, or keep a few wholly free slabs to avoid making and reaping the same slab again and again.

## When to use it

Use a slab allocator inside a kernel or a long-running server that allocates many objects of a fixed set of types, especially when the objects are costly to build. It is the standard allocator for small kernel objects in Solaris and its successors, and the Linux kernel uses descendants of it. For a user program with many sizes, a general allocator with thread caches, such as [jemalloc](/jemalloc/), is often a better fit. For objects that all die together, an [arena](/arena-allocation/) is simpler.

## Pitfalls

- **Returning a dirty object.** The caller must give back an object in its built state, for example with its lock released and its lists empty. Otherwise the next user gets a broken object, because the constructor does not run again.
- **Reaping too early.** Giving back a slab as soon as its last object is freed makes a program that frees and allocates one object at a slab border make and destroy a slab on each call. Keep wholly free slabs until memory is short.
- **Constructors that allocate.** A constructor that allocates from the same cache can recurse while the cache grows.
- **Coloring with no slack.** If the objects fill the page exactly, there is only one color, and coloring does nothing.

## Implementations

## History

Jeff Bonwick designed the slab allocator for the SunOS 5.4 kernel, the kernel of Solaris 2.4, and described it at the USENIX Summer 1994 conference. The paper introduced object caching with constructors and destructors, slabs with coloring, and the reaping of free slabs under memory pressure. Linux adopted the design in the late 1990s. In 2001 Bonwick and Jonathan Adams extended it with per-CPU magazines, which made it scale to many processors, and with the vmem allocator. Textbooks on operating systems now present slab allocation next to the [buddy system](/buddy-system/) as the two classic kernel allocators.

## References
