---
tag: VDFPMX
kind: concept
slug: locality-of-reference
name: Locality of reference
aliases:
- principle of locality
- spatial locality
- temporal locality
- locality principle
area: systems/caching-policies
level: intro
summary: "Programs tend to reuse data they used recently (temporal locality) and to use data near data they used recently (spatial locality). Caches, paging and prefetching depend on it."
prereqs: [cache]
see_also: [reuse-distance, working-set-model, cache-hit-ratio, independent-reference-model, prefetching, memory-hierarchy, cache-oblivious-model, external-memory-model]
sources:
  - paper: doi:10.1145/1070838.1070856
    title: "Peter J. Denning, The locality principle, Communications of the ACM 48(7) (2005), 19-24"
    locator: the history of the principle from 1966 to 1980, and its uses in replacement algorithms and in systems design
  - paper: doi:10.1145/363095.363141
    title: "Peter J. Denning, The working set model for program behavior, Communications of the ACM 11(5) (1968), 323-333"
    locator: the working set as the set of recently used pages, as the measure of the locality of a program
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: Chapter 2, Memory Hierarchy Design (the principle of locality), and Appendix B (block size and spatial locality)
  - paper: doi:10.1145/356887.356892
    title: "Alan Jay Smith, Cache memories, ACM Computing Surveys 14(3) (1982), 473-530"
    locator: the discussion of temporal and spatial locality as the reason caches work, and of line size
---

Locality of reference is the observed tendency of programs to use, in a short time, a small part of their data and code, and to use it again and again. *Temporal locality* means that an item used now is likely to be used again soon. *Spatial locality* means that items near an item used now, at nearby addresses, are likely to be used soon. Locality is a property of real request sequences, not a theorem. It is the reason why a small [cache](/cache/) in front of a large slow store can serve most requests.

## In plain words

When you cook, you use the same few tools and spices many times, and you keep them on the counter. That is reuse in time. When you take a plate from a stack, you will likely take the next plate soon. That is use of things that sit close together.

Programs behave the same way. A loop runs the same instructions many times and updates the same few variables. A program that reads an array reads the next element after this one. A cache keeps the items used lately, which pays off with reuse in time. It also loads a whole block of nearby bytes when it loads one byte, which pays off with use of nearby things. A program without either habit gets little help from any cache.

## The idea

**Temporal locality.** For a request $\sigma_t$, let its *reuse time* be $t - p$, where $p < t$ is the previous request for the same item, and its [reuse distance](/reuse-distance/) be the number of distinct other items requested between $p$ and $t$. A trace has strong temporal locality when most reuse distances are small. An LRU cache of $k$ items hits exactly the requests with reuse distance less than $k$, so the histogram of reuse distances is a precise measure of temporal locality for LRU.

**Spatial locality.** A cache moves data in blocks, called *lines* in hardware (often 64 bytes) and *pages* in virtual memory (often 4 KiB). A request for one byte brings in the whole block. If the program then uses the other bytes of the block, those requests hit. The block size is a trade-off: larger blocks exploit more spatial locality, but they hold more bytes that are never used and take more time to load.

**Phases.** Denning described programs as moving through a sequence of *phases*, each with a small set of pages in use, the *locality set*, with short transitions between phases. The [working set model](/working-set-model/) estimates the current locality set by the set of pages used in the last window of time.

**What locality is not.** Locality is not the same as skewed popularity. In the [independent reference model](/independent-reference-model/), each request is a fresh random draw, so a few popular items get most requests, but the chance of a request does not depend on the recent past. Real traces have both effects. Policies such as LRU bet on recency, and policies such as LFU bet on frequency.

## Examples

**Spatial locality and loop order.** Take a $64 \times 64$ array of 8-byte numbers stored row by row, so each 64-byte line holds 8 numbers of one row, and the array fills 512 lines. Use a fully associative LRU cache.

| cache size | misses, row by row | misses, column by column |
|---|---|---|
| 32 lines (2 KiB) | 512 of 4,096 | 4,096 of 4,096 |
| 64 lines (4 KiB) | 512 of 4,096 | 512 of 4,096 |

Row by row, each line gives one miss and then 7 hits, so the miss ratio is $1/8$ for each cache size. Column by column, one column touches 64 different lines. The next column uses the same lines again, but 63 other lines come between two uses of a line. With 32 lines, each line is gone by then, and every access misses. With 64 lines, the lines survive, and the miss count drops back to 512. The same arithmetic is done in a different order, and the miss count changes by a factor of 8.

**Temporal locality and a cliff.** A loop sums an array of 100 numbers of 8 bytes, which fill 13 lines, ten times. An LRU cache of 13 or more lines has only the 13 compulsory misses. An LRU cache of 12 lines has 130 misses: each line is evicted just before its next use, so every access to a new line misses on each pass. This is the cyclic pattern on which LRU is worst, see [LRU competitiveness](/lru-competitiveness/).

**Non-examples.** Lookups in a [hash table](/hash-table/) much larger than the cache go to random places, so they have little spatial locality and, if the keys are distinct, no temporal locality. A scan that reads a large file once has spatial locality inside each block but no reuse at all, and it pushes useful items out of an LRU cache. Following pointers through a linked structure spread over memory has neither.

## Where it is used

- **Caches and virtual memory.** All the caches of the [memory hierarchy](/memory-hierarchy/) depend on locality. Without it, a cache much smaller than the data would have a hit ratio near the ratio of the two sizes.
- **Replacement policies.** LRU keeps the items with the smallest reuse distance so far. [CLOCK](/clock/) approximates LRU. Scan-resistant policies such as [2Q](/two-q/), [LIRS](/lirs/) and [ARC](/arc/) try not to lose items with real reuse to a one-time scan.
- **Prefetching.** A [prefetcher](/prefetching/) loads the next blocks of a sequential or strided stream before the program asks, which turns spatial locality into hits on the first access.
- **Algorithm design.** Loop tiling, B-trees and the algorithms of the [external memory model](/external-memory-model/) and the [cache-oblivious model](/cache-oblivious-model/) arrange the work so that each block is used fully while it is in fast memory.
- **Memory management.** The [working set model](/working-set-model/) uses locality to decide how many pages each process needs, and so to prevent thrashing.

## References
