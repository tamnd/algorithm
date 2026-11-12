---
tag: 6D7E5P
kind: algorithm
slug: jemalloc
name: jemalloc
aliases:
- je malloc
area: systems/memory-allocation
level: advanced
summary: "Jason Evans's malloc for FreeBSD: threads go to arenas round robin, memory comes in aligned 2 MiB chunks split into page runs by the buddy method, and small objects use a region bitmap per run."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {r: the number of regions in one run, p: the number of pages in one chunk, m: the number of chunks of the arena}
  time: {worst: O(r + log p + log m), average: O(1)}
  space: {extra: O(m p)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2006
  people: [Jason Evans]
  note: Written for the C library of FreeBSD to replace phkmalloc on machines with many processors, and presented at BSDCan 2006.
prereqs: [size-classes, buddy-system, bitmap-allocator, segregated-free-lists]
see_also: [hoard-allocator, tcmalloc, mimalloc, dlmalloc, slab-allocator, arena-allocation, internal-fragmentation, external-fragmentation]
sources:
  - url: https://people.freebsd.org/~jasone/jemalloc/bsdcan2006/jemalloc.pdf
    title: "Jason Evans, A scalable concurrent malloc(3) implementation for FreeBSD, BSDCan 2006, April 2006"
    locator: section Algorithms and data structures (arenas and round-robin assignment, chunks, Figure 4 size classes, runs and region bitmaps, Figure 5 fullness categories) and section Experiments (malloc-test with sixteen arenas)
---

jemalloc is the [allocator](/allocator/) that Jason Evans wrote for the C library of FreeBSD and described at BSDCan 2006. It was built to replace phkmalloc on machines with several processors, where one allocator lock had become a bottleneck. It spreads threads over many arenas, each with its own lock, and assigns them round robin instead of by a hash. All memory comes from the kernel in chunks of 2 MiB at addresses that are multiples of 2 MiB, so the chunk of any pointer is found by masking. An arena splits its chunks into page runs by the [buddy method](/buddy-system/), and a run for small objects holds regions of one [size class](/size-classes/) with a bitmap that marks the regions in use.

## In plain words

Think of a large office with many copy rooms. Each new worker is sent to the next room in turn, so the rooms fill evenly, and workers rarely wait for each other.

Each room cuts big sheets of paper into strips of fixed widths. A sheet for one width is cut into equal strips, and a card on the sheet shows which strips are taken. A worker who needs a strip takes the first free one on the current sheet. When a worker hands back a strip, it goes back to the room that cut it, whatever room that worker uses.

Very big requests do not go to a room at all. They get whole sheets of their own.

## The problem

This is [online memory allocation](/online-memory-allocation/) for a general-purpose C library on machines with several processors. The allocator has no control over the programs that use it, so it must be fast for one thread, scale with many threads, and keep fragmentation low. Evans names lock contention, cache locality and false sharing of cache lines between processors as the main concerns. jemalloc first tries to use little memory, and packs objects together only when that does not conflict with the first goal. It reduces false sharing through its arenas and leaves padding to the program. It also keeps the run-time options of phkmalloc for debugging.

## The algorithm

The size classes come in three groups (Figure 4 of the paper, with 4 KiB pages and a quantum of 16 bytes):

- **small**: tiny (2, 4 and 8 bytes), quantum-spaced (16, 32, 48, ..., 512 bytes) and sub-page (1 KiB and 2 KiB);
- **large**: 4 KiB, 8 KiB, ..., 1 MiB, that is, more than half a page and at most half a chunk;
- **huge**: more than half a chunk, rounded up to whole chunks.

There is one arena for a single processor, and four arenas per processor otherwise. An arena owns chunks. Each chunk has a page map that records the run of each page. A small run has a header with a region bitmap and then regions of one class. Each arena has at most one current run per small class.

```pseudo id=main
MALLOC(n) in thread t
L1  a ← ARENA(t)                ▷ at first use, the next arena in round-robin order
L2  if n > CHUNK/2 then map ⌈n/CHUNK⌉ new contiguous chunks, record them in the huge tree, return their base
L3  c ← the size class of n; lock a
L4  if c > PAGE/2 then return the start of BUDDY-ALLOC(a, c/PAGE)
L5  r ← a.current[c]; if r is none or full then r ← a non-full run of class c, preferring Q50, Q25, Q0, then Q75, or a new run from BUDDY-ALLOC; a.current[c] ← r
L6  i ← the first 0 bit of r.bitmap; set it
L7  return r.start + r.header + i · c

FREE(p) in thread t
L8  ARENA(t); k ← p rounded down to a multiple of CHUNK
L9  if k is in the huge tree then unmap its chunks and return
L10 a ← the arena that owns chunk k; r ← the run of page (p − k)/PAGE in k's page map; lock a
L11 if r holds a large object then BUDDY-FREE(a, r) and return
L12 i ← (p − r.start − r.header)/c; clear bit i of r.bitmap
L13 if r is empty and has left QINIT then remove r from a and BUDDY-FREE(a, r); else if r was full and is not current then make r a non-full run of a

BUDDY-ALLOC(a, k)
L14 j ← ⌈log₂ k⌉; take the lowest free block of the smallest order ≥ j in the chunks of a, or map a new chunk; split it in halves down to order j

BUDDY-FREE(a, r)
L15 while the buddy of the block is a free block of the same order, merge them; if the block is the whole chunk, unmap the chunk
```

**Arenas** (L1, L8). Larson and Krishnan used several arenas and picked one by hashing the thread identifier. Evans notes that good hashing of thread identifiers, which are pointers in practice, is hard, so jemalloc gives arenas in turn at a thread's first malloc or free and keeps the choice in thread-local storage. With four arenas per processor, two running threads rarely share one.

**Chunks** (L2, L8 to L10). Chunks are aligned to their size, so the chunk of a pointer is $p$ with its low 21 bits cleared, and its page is a shift away. This is how FREE finds the owner arena and the run without a header next to the object. The owner arena is the one that cut the run, not the arena of the freeing thread.

**Runs** (L4, L14, L15). The pages of a chunk are given out by the binary buddy method: runs are split in halves down to one page and merged only in the reverse way. A large object takes a run of its own.

**Regions** (L5 to L7, L12). A small run keeps its bitmap at its start, apart from the regions. The bitmap is scanned for the first free region, which packs objects at low addresses; it also keeps allocator data away from program data, and it works for 2-byte regions that could not hold a free list pointer. Bigger classes use runs of several pages so that the header and the tail waste little: about 3% for 2 KiB regions.

**Fullness** (L5, L13). A run stays current until it fills or empties. The other runs are grouped by fullness quartile, and a new current run is taken from Q50, then Q25, then Q0, then Q75; Q75 is last because a nearly full run would soon fill again. A new run starts in QINIT and is never destroyed there. Without that rule, one malloc and one free could create and destroy a run each time.

## Example

The code of this page is a small model of jemalloc in Python, not the real allocator: it runs in one thread, counts locks instead of taking them, and only computes addresses. This trace uses the model with two processors, so 8 arenas. $C_1$ and $C_2$ are the first two chunks, at 2 MiB and 4 MiB. A 1-page run of 32-byte regions has a 32-byte header and 127 regions.

| Step | Call | Arena | Path | Result |
|---|---|---|---|---|
| 1 | thread 0: malloc(20) | 0 (first use) | class 32; no run: new chunk $C_1$, buddy split of 512 pages down to page 0 (L14), region 0 | $C_1 + 32$ |
| 2 | thread 1: malloc(20) | 1 (next in turn) | the same in a new chunk $C_2$ | $C_2 + 32$ |
| 3 | thread 0: malloc(30) | 0 | class 32, current run, first free region 1 | $C_1 + 64$ |
| 4 | thread 0: malloc(3000) | 0 | large class 4096: the free 1-page buddy at page 1 | $C_1 + 4096$ |
| 5 | thread 1: free($C_1 + 32$) | 0 (owner of $C_1$) | clear bit 0; the run is in QINIT, so it stays | |
| 6 | thread 0: malloc(17) | 0 | first free region is 0 again | $C_1 + 32$ |
| 7 | thread 0: malloc(3 MiB) | none | huge: 2 new chunks, in the huge tree | 6 MiB |
| 8 | thread 0: free(6 MiB), free($C_1 + 4096$) | none, then 0 | unmap 2 chunks; page 1 cannot merge with page 0, which is in use | |

At step 5 thread 1 frees into arena 0, which costs a lock on arena 0, not on its own arena 1. At step 6 the bitmap scan returns the lowest free region, so the freed region is used again at once.

## Correctness

Each arena chunk is always tiled by runs and free buddy blocks of its arena; each block of order $o$ starts at a multiple of $2^o$ pages, and no two free buddies of the same order are both free. In each small run, bit $i$ of the bitmap is set exactly when region $i$ is held by the program. Each small run is the current run of its class, or a non-full run that has left QINIT, or full. Huge objects use chunks that no arena owns. From these invariants, no two live objects overlap, and FREE finds the right arena and run from the address alone. The proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Small objects.** L6 scans a bitmap of $r$ bits; the real code scans whole words, so the cost is $O(r/w)$ word operations, and the first words are usually not full. A malloc that needs a new current run picks one from the fullness groups; with a search tree ordered by address in each group, this takes $O(\log m)$ time, while the model scans. The paper keeps the huge objects in one red-black tree.
- **Page runs.** A buddy split or merge goes through at most $\log_2 p$ orders, with $p = 512$ pages per chunk. The model scans for the lowest free block; it computes the choices, not the speed.
- **Huge objects.** One tree lookup in $O(\log h)$ for $h$ huge objects, plus the system call.
- **Space.** Each chunk has a page map with one entry per page, and each small run has a header of 16 bytes plus one bit per region. Rounding to size classes loses less than half of each object for tiny, sub-page and large classes, and less than 16 bytes for quantum-spaced classes.

## Properties

- **Scales with threads.** Threads in different arenas never share a lock. The paper's malloc-test on four processors scales almost linearly up to four threads; with the default sixteen arenas, contention starts above sixteen threads.
- **Free goes home.** An object always returns to the arena that gave it out, so arenas do not trade memory, and a thread that frees memory of another arena takes that arena's lock.
- **Low addresses first.** The bitmap scan packs regions at the start of a run, and the run choice favors half-full runs, so lightly used runs can empty and go back.
- **No headers in objects.** The size and owner of an object come from the chunk page map, so small objects carry no per-object header.

## Variants and improvements

- **Thread caches.** Later versions of jemalloc added a small cache per thread in front of the arenas, close to the caches of [tcmalloc](/tcmalloc/).
- **Later layouts.** Later versions replaced the 2006 chunk, run and quartile design with other structures; the page here covers only the 2006 design.
- **Related designs.** [Hoard](/hoard-allocator/) also uses several heaps and returns memory to the owner; [mimalloc](/mimalloc/) makes each page belong to one thread. Evans compares against [dlmalloc](/dlmalloc/), which is fast for one thread but not built to scale.

## When to use it

Use jemalloc as the malloc of programs with many threads and long run times, where steady memory use and low fragmentation matter as much as speed. Its arenas cut contention without per-thread pools that can grow without bound. For one thread, the paper reports speed close to that of phkmalloc, so the gain of jemalloc comes with threads. A program with one thread and a fixed pattern of sizes can do as well with a simpler allocator such as [dlmalloc](/dlmalloc/).

## Pitfalls

- **Freeing into the wrong arena.** L10 must use the arena that owns the chunk. A free into the arena of the calling thread would put a region of one arena's run under another arena's lock and break the bitmap.
- **Destroying runs in QINIT.** If L13 destroyed every empty run, a loop of one malloc and one free on a fresh run would split and merge buddy blocks on each pass. The QINIT rule gives the hysteresis that stops this.
- **Unaligned chunks.** L8 finds the chunk by masking the low bits of $p$. Memory from the kernel that is not aligned to the chunk size must be trimmed or mapped again until it is.
- **More threads than arenas.** Round robin gives even counts, not even load. Above four threads per processor, some threads share an arena, and the paper's benchmark shows the cost.
- **Taking Q75 runs first.** A nearly full run fills again after a few calls, so the current run would change often. L5 takes Q75 last.

## Implementations

## History

Jason Evans wrote jemalloc for FreeBSD, where it replaced phkmalloc by Poul-Henning Kamp, and described it in a paper dated April 2006 and presented at BSDCan 2006. The design took several arenas from Larson and Krishnan (1998), an idea that Hoard and the magazine layer of the slab allocator had also used, and the paper compared it against phkmalloc and dlmalloc 2.8.3 on a four-processor Opteron system. jemalloc then went into other software, and Evans kept working on it for many years; later versions changed the design a lot.

## References
