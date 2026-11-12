---
tag: 5Q3MDD
kind: algorithm
slug: dlmalloc
name: dlmalloc
aliases:
- Doug Lea's malloc
area: systems/memory-allocation
level: advanced
summary: "Doug Lea's general-purpose malloc: chunks with boundary tags, exact small bins, best-fit tree bins, a designated victim for locality, a top chunk grown by sbrk, and mmap for huge requests."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {w: "the word length, so sizes have w binary digits", n: the number of chunks in the heap}
  time: {worst: O(w)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1987
  people: [Doug Lea]
  note: Lea wrote the first version in 1987 and kept it as public domain code. Wolfram Gloger's ptmalloc, a version with several arenas for threads, is derived from it and became the malloc of GNU libc.
prereqs: [boundary-tags, segregated-free-lists, coalescing, best-fit-allocation]
see_also: [deferred-coalescing, size-classes, external-fragmentation, online-memory-allocation, jemalloc, tcmalloc, mimalloc, hoard-allocator]
sources:
  - url: https://gee.cs.oswego.edu/dl/html/malloc.html
    title: "Doug Lea, A Memory Allocator (first written 1996, last modified April 2000)"
    locator: the sections on chunks and boundary tags, bins, the wilderness chunk, memory mapping, and locality (the most recently split-off space is used first)
  - url: https://gee.cs.oswego.edu/pub/misc/malloc.c
    title: "Doug Lea, malloc.c, version 2.8.6 (August 2012)"
    locator: the comments on chunk representation, smallbins and treebins, the dv and top chunks, the order of choices for small and large requests in malloc, and DEFAULT_MMAP_THRESHOLD
  - paper: doi:10.1007/3-540-60368-9_19
    title: "Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation: a survey and critical review, IWMM 1995, LNCS 986, 1-116"
    locator: Section 3.6 (segregated fits) and Section 3.11 (quick lists and deferred coalescing, with the early Lea allocator as the example)
---

dlmalloc is the general-purpose [allocator](/allocator/) that Doug Lea first wrote in 1987. Memory is a row of chunks, each with its size in a head word and, when free, a copy of the size at its end, so that neighbors can be found and joined in constant time ([boundary tags](/boundary-tags/)). Free chunks sit in bins by size: small bins hold one exact size each, and tree bins hold ranges of larger sizes and are searched for the [best fit](/best-fit-allocation/). Two special chunks lie outside the bins: the designated victim (dv), the piece split off most recently, which serves small requests with good locality, and the top chunk at the end of memory, which grows with sbrk. Very large requests get their own pages from mmap.

## In plain words

Think of a shelf cut into boxes. Each box has a label at the front with its width, and an empty box has the same label at the back. From any box you can read the label of the box in front and the box behind, and join two empty neighbors into one.

Empty boxes are kept in drawers by width. For a small item there is a drawer for each exact width, so the right box is found at once. For a big item the drawers hold ranges of widths, and the allocator picks the narrowest box that fits. The last piece cut off a box is kept on the side and used first for the next small item, so items asked for together sit together. At the end of the shelf is an open area that the allocator can extend. Huge items get a shelf of their own.

## The problem

This is [online memory allocation](/online-memory-allocation/) for a C program: malloc(n) must return a block of at least $n$ bytes at once, free(p) gives a block back in any order, and live blocks never move. The program may hold the address anywhere, so the allocator cannot compact. The goals are low [fragmentation](/external-fragmentation/) on real programs and a short, predictable path for each call. dlmalloc is single-threaded; callers that need threads add a lock around it.

## The algorithm

The model follows malloc.c version 2.8.6 with 32-bit sizes: chunk sizes are multiples of 8, the smallest chunk has 16 bytes, and a request of $r$ bytes needs a chunk of $nb = \max(16, \lceil (r + 4)/8 \rceil \cdot 8)$ bytes. Each chunk head holds its size, a bit CINUSE for "this chunk is in use", and a bit PINUSE for "the previous chunk is in use". A free chunk also stores its size in its last word, where the next chunk can read it.

- **Small bins.** 32 lists, one for each chunk size below 256 bytes, 8 bytes apart. A new free chunk goes to the front of its list.
- **Tree bins.** 32 bins for sizes of 256 and more, two for each power of two. In malloc.c each is a bitwise trie keyed by size; it finds the smallest chunk at least as large as a request.
- **dv.** The designated victim, "the preferred chunk for servicing small requests that don't have exact fits". It is normally the remainder of the last split and it is in no bin.
- **top.** The free chunk at the end of the arena. It is in no bin, and it is treated as larger than every other chunk.

```pseudo id=main
MALLOC(r)
L1  nb ← PAD(r)
L2  if nb < 256 then                                 ▷ small request
L3      if bin[nb] or bin[nb + 8] is not empty then take its first chunk whole; return it
L4      if nb > dv.size and some bin holds a chunk of size ≥ nb then
L5          take the smallest such chunk, split off nb; the rest becomes dv, the old dv goes to its bin; return
L6  else if some tree bin chunk c fits and (dv is too small or c.size − nb < dv.size − nb) then
L7      take c, split off nb, put the rest in its bin; return
L8  if nb ≤ dv.size then split off nb from dv, the rest stays dv; return
L9  if nb < top.size then split off nb from top, the rest stays top; return
L10 if nb ≥ MMAP_THRESHOLD then return a fresh mapping of nb bytes
L11 extend top with sbrk and go to L9

FREE(p)
L12 if p is a mapped chunk then unmap it; return
L13 if PINUSE(p) = 0 then q ← p − footer size; unlink q unless q = dv; p ← q ∪ p
L14 if the next chunk is top then top ← p ∪ top; if p was dv clear dv; return
L15 if the next chunk is dv then dv ← p ∪ dv; return
L16 if the next chunk n is free then unlink n; p ← p ∪ n
L17 if p = dv then update dv.size; return
L18 put p in the bin for its size
```

A split leaves a remainder only if it has at least 16 bytes; otherwise the whole chunk is used.

**Small requests** (L2 to L5). Line L3 looks for a chunk of exactly the right size, or 8 bytes more, which cannot be split since 8 bytes is below the minimum. If there is none and dv is too small, line L5 takes the smallest larger chunk in any bin and splits it, and the remainder becomes the new dv. If dv is big enough, line L8 splits it. So a run of small requests is carved, one after the other, out of one remainder: this is the locality rule in Lea's article, "the most recently split-off space is used (and resplit) if it is big enough".

**Large requests** (L6, L7). The best fit among the tree bins is used if it leaves a smaller remainder than dv would; otherwise dv is used at L8. The remainder of a tree chunk goes back to a bin, not to dv.

**Top and the system** (L9 to L11). If no free chunk fits, the request is cut from the front of top. If top is too small, a request of at least the mmap threshold (256 KB by default in 2.8.6) gets its own mapping, which free returns to the system at once. Otherwise top grows with sbrk.

**Free** (L12 to L18). The chunk joins its free neighbors at once. PINUSE says whether the previous chunk is free, and its footer gives its size, so the previous chunk is found in constant time. The next chunk is found by adding the size. A chunk next to top merges into top, a chunk next to dv merges into dv, and other free chunks are taken out of their bins first. The result goes into its bin.

## Example

The code of this page is a small model of dlmalloc in Python, not the real allocator: it keeps the chunk layout, the bins and the choice rules, and it only computes addresses. This trace comes from the model. Start with an empty arena, a granularity of 4096 bytes for sbrk, and the calls below. Addresses are chunk starts.

| Step | Call | nb | Action | Bins after | dv after | top after |
|---|---|---|---|---|---|---|
| 1 | a = malloc(20) | 24 | top is empty: sbrk 4096 (L11), split top (L9); a = 0 | | none | [24, 4096) |
| 2 | b = malloc(100) | 104 | split top; b = 24 | | none | [128, 4096) |
| 3 | c = malloc(20) | 24 | split top; c = 128 | | none | [152, 4096) |
| 4 | d = malloc(300) | 304 | split top; d = 152 | | none | [456, 4096) |
| 5 | e = malloc(20) | 24 | split top; e = 456 | | none | [480, 4096) |
| 6 | free(b) | | neighbors in use (L18) | small 104: {24} | none | same |
| 7 | free(d) | | neighbors in use (L18) | small 104: {24}; tree: {304 at 152} | none | same |
| 8 | f = malloc(40) | 48 | no exact fit, dv empty; smallest chunk is 104 at 24; split (L5) | tree: {304 at 152} | 56 at 72 | same |
| 9 | g = malloc(48) | 56 | dv fits exactly; use all of it (L8) | tree: {304 at 152} | none | same |
| 10 | free(c) | | next chunk 152 is free: unlink and join (L16) | tree: {328 at 128} | none | same |
| 11 | h = malloc(200) | 208 | small, no exact fit; smallest chunk is 328 at 128; split (L5) | | 120 at 336 | same |
| 12 | i = malloc(1000) | 1008 | large; no tree chunk fits, dv too small; split top (L9) | | 120 at 336 | [1488, 4096) |
| 13 | free(e) | | previous chunk is dv: join backward (L13), dv grows (L17) | | 144 at 336 | same |

At step 8 the request of 40 bytes is served from the chunk freed at step 6, and its remainder becomes dv, so the request at step 9 lands right after it, at 72. At step 13 the free chunk of 24 bytes is never put in a bin: the previous chunk is free, which PINUSE shows, so the two join at once.

## Correctness

Five invariants hold after every call: (1) the chunks tile the arena from its start to the end of top, and each head holds the true size; (2) PINUSE of each chunk equals CINUSE of the chunk before it, and every free chunk other than top has a footer equal to its size; (3) no two free chunks are adjacent, and the chunk before top is in use; (4) every free chunk other than top and dv lies in exactly one bin, the bin of its size, and dv and top lie in no bin; (5) the chunk returned by malloc was free, has at least $nb$ bytes, and is disjoint from every live chunk. Each line keeps them, because a split writes the head and footer of both parts and the PINUSE bit of the next chunk, and because free joins with every free neighbor before it inserts. The proof is in [the correctness proof](proofs/correctness.md). It also shows the two choice rules: an exact small fit is taken whenever it exists, and a large request taken from a tree bin gets the smallest chunk that fits.

## Complexity

- **Small malloc.** malloc.c keeps a bitmap with one bit per nonempty small bin, so L3 and the search for the next nonempty bin at L4 take a constant number of word operations, with an instruction that finds the lowest set bit. Unlink from a doubly linked list is $O(1)$.
- **Large malloc and free of a large chunk.** A tree bin is a bitwise trie keyed on the size, so a search or an insert follows one path of length at most $w$, the number of binary digits of a size. That gives $O(w)$, which is a constant for a fixed machine.
- **Free.** Finding the neighbors uses the size and the footer, $O(1)$. Unlinking a small chunk is $O(1)$, a tree chunk $O(w)$.
- **System calls.** sbrk and mmap are rare, and their cost is outside the model.
- **Space.** One head word per chunk in use; a free chunk also stores its footer and its list or tree links inside its own unused space, so a chunk is at least 16 bytes with 4-byte sizes.

The Python model replaces the bitmaps and tries by lists and scans, so its own cost is higher; it models the choices, not the speed.

## Properties

- **Best fit, in effect.** Exact small bins and best-fit tree bins make dlmalloc close to a best-fit allocator, the policy that does best on real programs in the study of Wilson et al. The dv rule trades a little fit for locality.
- **Immediate coalescing.** Version 2.8 joins free neighbors at once. Older versions kept small freed chunks on fast lists and joined them later, a form of [deferred coalescing](/deferred-coalescing/).
- **No compaction, no thread support.** Chunks never move. Without the USE_LOCKS option there is no lock, and one lock serializes all threads.
- **Deterministic.** The same calls give the same addresses.
- **Metadata inside the heap.** Heads and links are stored next to user data. An overflow of a user buffer can corrupt them, which has been the basis of many heap exploits.

## Variants and improvements

- **ptmalloc and glibc malloc.** Wolfram Gloger's ptmalloc adds several arenas, each with its own lock, so threads rarely contend. It became the allocator of GNU libc, which later added per-thread caches.
- **mspaces.** malloc.c 2.8 can manage several independent heaps, called mspaces.
- **Thread-aware allocators.** [Hoard](/hoard-allocator/), [jemalloc](/jemalloc/), [tcmalloc](/tcmalloc/) and [mimalloc](/mimalloc/) replace the single heap with per-thread or per-CPU structures and size-class pages, at some cost in memory.
- **Older versions.** The article describes 128 bins spaced about logarithmically, smallest-first search, and a top chunk ("wilderness") that is used only when nothing else fits, with mmap above a default of 1 MB. Version 2.8 keeps the same policy with tries for large chunks and a lower mmap threshold.

## When to use it

Use dlmalloc, or a descendant, as a compact single-threaded or lightly threaded allocator with good fragmentation and no tuning: embedded systems, language runtimes that need a private malloc, and programs that create a separate heap per subsystem. For many threads that allocate at high rates, a per-thread design such as [tcmalloc](/tcmalloc/) or [mimalloc](/mimalloc/) scales better. For a real-time bound on every call, [TLSF](/tlsf/) gives $O(1)$ worst-case time with a similar good-fit policy. For many objects of one size, a [slab allocator](/slab-allocator/) or a [memory pool](/memory-pool/) is simpler and faster.

## Pitfalls

- **Taking dv for a large request without comparing.** Line L6 uses a tree chunk only if its remainder is smaller than the remainder of dv. Skipping the comparison and always using dv first (moving L8 before L6) wastes large chunks on dv splits; always using the tree first loses locality.
- **Putting the remainder of a large split into dv.** At L7 the remainder goes to a bin. Only small requests (L5) replace dv. Replacing dv at L7 would push a small dv back into a bin each time and break the run of small allocations.
- **Forgetting PINUSE on the next chunk.** Every split and every free must set or clear PINUSE in the following chunk. If it is stale, line L13 reads a footer that is user data and joins with a chunk that is in use.
- **Joining with dv by unlinking it.** dv is in no bin. Line L13 must not unlink it, and line L15 must grow dv instead of inserting the joined chunk into a bin.
- **Exact fit off by 8.** Line L3 must also try the bin for $nb + 8$: a chunk 8 bytes larger cannot be split, so it is an exact fit in effect. Missing it sends the request to dv or to a larger chunk and breaks it up for nothing.

## Implementations

## History

Doug Lea wrote the first version in 1987, for C++ programs that he found were limited by the speed and fragmentation of the allocators of the time. He described the design in the article "A Memory Allocator" in 1996 and kept the code in the public domain. The survey of Wilson, Johnstone, Neely and Boles (1995) found that its segregated fits policy, close to best fit, gave very low fragmentation on real programs. Wolfram Gloger turned it into ptmalloc, with several arenas for threads, and ptmalloc became the base of the malloc in GNU libc. Version 2.8, released in 2006 and maintained to 2.8.6 in 2012, introduced the tree bins and the designated victim chunk.

## References
