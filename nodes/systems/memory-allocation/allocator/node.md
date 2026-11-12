---
tag: XRA0QR
kind: abstract-type
slug: allocator
name: Dynamic storage allocator (malloc/free)
aliases:
- malloc/free interface
- memory allocator
- dynamic storage allocator
area: systems/memory-allocation
level: intro
summary: "The interface malloc(n) and free(p) over a heap: hand out disjoint blocks that never move, and take them back in any order."
prereqs: [word-ram]
see_also: [online-memory-allocation, free-list, first-fit-allocation, external-fragmentation, internal-fragmentation, robson-bound, segregated-free-lists, tracing-garbage-collection]
sources:
  - url: https://pubs.opengroup.org/onlinepubs/9699919799/functions/malloc.html
    title: The Open Group Base Specifications Issue 7, malloc
    locator: the description and the return value of malloc (a pointer to unused space, suitably aligned, or a null pointer on failure)
  - url: https://pubs.opengroup.org/onlinepubs/9699919799/functions/free.html
    title: The Open Group Base Specifications Issue 7, free
    locator: the description of free (the space is made available for further allocation; behaviour is undefined for a pointer not returned by an allocation function or already freed)
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 1 (the allocator's task, that it cannot move or compact live blocks) and Section 1.3 (strategy, policy and mechanism)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.5, Dynamic storage allocation, the reservation and liberation of variable-size blocks
---

A dynamic storage allocator manages one region of memory, the *heap*, for a program. The program asks for $n$ words with malloc$(n)$ and gets the address of a block of at least $n$ words that no other live block uses. Later it gives the block back with free$(p)$, in any order. The allocator may not move a live block, because the program holds raw addresses to it. This is the interface of C's `malloc` and `free`, and of many runtime systems. The interface says nothing about *which* free words to use; that choice is the *policy* of an implementation, such as [first fit](/first-fit-allocation/) or [best fit](/best-fit-allocation/), and the data structure that finds the words is its *mechanism*, such as a [free list](/free-list/). The cost of the choice is [fragmentation](/external-fragmentation/): free memory that is there but cannot serve a request.

## In plain words

Think of a car park with one long row and no painted lines. Cars of different lengths arrive. The attendant gives each car a stretch of the row that no other car uses, and once a car is parked, it cannot move until it leaves. Cars leave at any time, and their stretches become free again.

The attendant's rules are the allocator. A good attendant leaves the free stretches in large pieces, so that a long bus can still park later. A bad one leaves many small gaps between cars: the free space adds up, but the bus still has nowhere to go.

## Operations

| operation | signature | what it does |
|---|---|---|
| `malloc` | $\text{malloc}(n) \to p$ or NIL | returns the address $p$ of $n$ words that are not part of any live block, or NIL if it cannot |
| `free` | $\text{free}(p)$ | gives back the live block at $p$; the words may be used again |
| `usable-size` | $\text{usable-size}(p) \to k$ | the number $k \ge n$ of words that the block at $p$ really has |
| `realloc` | $\text{realloc}(p, n) \to q$ or NIL | a block of $n$ words whose first words equal those of $p$; $p$ stays valid if it fails |
| `calloc` | $\text{calloc}(n) \to p$ or NIL | malloc$(n)$ with the words set to 0 |

Real interfaces add an alignment: C's `malloc` returns an address that is suitably aligned for any object, and `aligned_alloc` takes an explicit alignment. `realloc` can be built from the others:

```pseudo id=main
MALLOC(n)                                  ▷ an implementation, for example first fit
L1  return a payload address, or NIL
USABLE-SIZE(p)
L2  return the size of the block of p, without its tags
REALLOC(p, n)
L3  old ← USABLE-SIZE(p)
L4  if n ≤ old then return p                ▷ the block is large enough already
L5  q ← MALLOC(n)
L6  if q = NIL then return NIL             ▷ p is still live and unchanged
L7  copy the first old words from p to q
L8  FREE(p)
L9  return q
```

## Laws

Let the *live set* be the blocks returned by malloc or realloc and not yet freed, each with its address $p$ and its size $n$.

1. **Inside the heap.** If malloc$(n) = p \ne$ NIL, the words $[p, p + n)$ lie in the heap.
2. **Disjoint.** The ranges $[p, p + n)$ of two live blocks never overlap. In particular, malloc never returns an address that is live.
3. **Stable.** The allocator never moves a live block and never writes to its words. The words keep what the program wrote until the program frees the block.
4. **Free makes room.** After free$(p)$, the block is no longer live, and a later malloc may return any of its words. Freeing an address that is not live is an error; the C standard leaves it undefined.
5. **Realloc keeps the prefix.** If realloc$(p, n) = q \ne$ NIL, the first $\min(n, n_{old})$ words at $q$ equal the old words at $p$, and $p$ is no longer live unless $q = p$. If it returns NIL, $p$ is still live and unchanged.
6. **Failure is allowed.** malloc may return NIL at any time. A good implementation fails only when it must, but the interface does not promise that, and no implementation that cannot move blocks can promise it in general (see the lower bounds).

The tag words of a block, the free-list links and any other data of the allocator must lie outside every live range, or law 3 fails. Writing a known pattern into each live block and checking it after each call tests laws 1 to 3 and 5 on any implementation.

## Implementations

All the implementations below meet the laws. They differ in time per request, in space overhead and in fragmentation.

| implementation | search | notes |
|---|---|---|
| [first fit](/first-fit-allocation/), [next fit](/next-fit-allocation/), [best fit](/best-fit-allocation/), [worst fit](/worst-fit/) | a scan of one [free list](/free-list/), $O(F)$ | the [sequential fit](/sequential-fit/) family; free merges neighbours by [coalescing](/coalescing/) with [boundary tags](/boundary-tags/) |
| best fit on a balanced tree | $O(\log F)$ | the same choices as the list scan |
| [segregated free lists](/segregated-free-lists/) with [size classes](/size-classes/) | about $O(1)$ | close to best fit; used by most production allocators |
| [buddy system](/buddy-system/) | $O(\log H)$ | block sizes are powers of two; fast merging |
| [TLSF](/tlsf/) | $O(1)$ worst case | two-level bitmaps over segregated lists, for real-time systems |
| [slab allocator](/slab-allocator/), [memory pool](/memory-pool/) | $O(1)$ | blocks of one size or one type |
| [arena allocation](/arena-allocation/), [bump pointer](/bump-pointer-allocation/) | $O(1)$ | free is a no-op; the whole region is freed at once |
| [dlmalloc](/dlmalloc/), [jemalloc](/jemalloc/), [tcmalloc](/tcmalloc/), [mimalloc](/mimalloc/), [Hoard](/hoard-allocator/) | mixed | production allocators that combine the methods above, with thread caches |

The code on this page implements the interface with address-ordered first fit on the heap model of the [first-fit page](/first-fit-allocation/), and wraps it in a checker that fills each live block with a pattern and tests the laws after each call. The checker finds two broken variants at once: one that forgets to count the tag words in the block size, so a payload covers the next header, and one that leaves a block on the free list after it gives the block out.

Allocators that may move blocks, such as compacting and copying [garbage collectors](/tracing-garbage-collection/), offer a different interface: the program holds references that the runtime can update, and [memory compaction](/memory-compaction/) removes fragmentation.

## Lower bounds

**Space.** Without moving blocks, no allocator can avoid fragmentation on every request sequence. Robson proved that for each allocator there are sequences, with at most $M$ live words at any time, that force a heap much larger than $M$; the factor grows with the logarithm of the ratio of the largest to the smallest block size. The exact bounds, and matching upper bounds for particular policies, are on the [Robson bound](/robson-bound/) page. Even the best offline choice, with the whole sequence known in advance, is a hard problem: see [offline dynamic storage allocation](/offline-dynamic-storage-allocation/).

**Overhead.** An allocator must know the size of a block at free$(p)$, since free gets only the address. It stores the size in a header, or it groups blocks of one size into one page and keeps the size per page, as size-class allocators do. So each block costs some words of metadata, or each block is rounded up to a class size: either way some [internal fragmentation](/internal-fragmentation/).

**Time.** There is no useful time lower bound on the word RAM: [TLSF](/tlsf/) and segregated lists serve each request in $O(1)$ time. The price of fast methods is paid in space, by rounding up to classes.

## References
