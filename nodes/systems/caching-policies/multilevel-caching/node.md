---
tag: 6DVKBB
kind: concept
slug: multilevel-caching
name: Multilevel caching
aliases:
- cache hierarchy
- inclusive cache
- exclusive cache
- non-inclusive non-exclusive cache
- NINE cache
- multilevel inclusion
area: systems/caching-policies
level: intro
summary: "Caches stacked in levels, each serving the misses of the one above. Inclusive, exclusive and NINE designs differ in duplication, and AMAT adds the cost of each level."
prereqs: [cache, memory-hierarchy, cache-hit-ratio]
see_also: [set-associative-cache, mq-cache, inclusion-property, three-cs-model, write-back, prefetching, miss-ratio-curve, lru]
sources:
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: "Appendix B, Section B.1 (average memory access time) and Section B.3 (multilevel caches: local and global miss rates, the AMAT of two levels, multilevel inclusion and exclusion)"
  - paper: "Jean-Loup Baer and Wen-Hann Wang, On the inclusion properties for multi-level cache hierarchies, 15th Annual International Symposium on Computer Architecture (ISCA), 1988"
    title: "Baer and Wang, On the inclusion properties for multi-level cache hierarchies, ISCA 1988"
    locator: the definition of multilevel inclusion and the conditions on sets, ways and block sizes under which it holds
  - paper: "Yuanyuan Zhou, James F. Philbin and Kai Li, The multi-queue replacement algorithm for second level buffer caches, USENIX Annual Technical Conference, 2001"
    title: "Zhou, Philbin and Li, The multi-queue replacement algorithm for second level buffer caches, USENIX ATC 2001"
    locator: the study of second-level buffer cache traces (weak temporal locality, reuse distances mostly beyond the first-level size) and the properties a second-level policy needs
  - paper: "Theodore M. Wong and John Wilkes, My cache or yours? Making storage more exclusive, USENIX Annual Technical Conference, 2002"
    title: "Wong and Wilkes, My cache or yours? Making storage more exclusive, USENIX ATC 2002"
    locator: double caching in a client and a storage array, and the DEMOTE operation that makes the array cache exclusive
  - paper: "Norman P. Jouppi and Steven J. E. Wilton, Tradeoffs in two-level on-chip caching, 21st Annual International Symposium on Computer Architecture (ISCA), 1994"
    title: "Jouppi and Wilton, Tradeoffs in two-level on-chip caching, ISCA 1994"
    locator: exclusive two-level caching, where the L1 victim moves to L2 and an L2 hit moves the block to L1
---

Multilevel caching puts several [caches](/cache/) in a row, each larger and slower than the one before, so that a miss in level $i$ becomes a request to level $i + 1$. Processors have two or three levels before main memory, and storage systems have a client cache in front of a server or array cache. The levels may keep copies of the same blocks (inclusive), never share a block (exclusive), or follow no rule (non-inclusive non-exclusive, NINE). The average memory access time adds, level by level, the hit time and the miss rate times the cost of a miss.

## In plain words

Think of a cook with a small tray beside the stove, a fridge in the kitchen and a store down the street. Most things the cook needs are on the tray. What is not there comes from the fridge, and what is not in the fridge comes from the store, which is slow.

There are three ways to stock the fridge. It can hold a copy of all that is on the tray, which makes it easy to know where things are but wastes some space. It can hold only what is not on the tray, so the tray and the fridge together hold more. Or it can follow no rule. A strange thing about the fridge is that the cook goes there only for what the tray did not have, so the fridge sees mostly the things that are used less often.

## The idea

**Levels and the filtered stream.** Level 1 (L1) sees every request. Level 2 (L2) sees only the misses of L1, level 3 only the misses of L2, and so on. So the stream that reaches L2 has had its short-term reuse removed. A block used again soon hits in L1 and never reaches L2, and a block that comes back to L2 has usually been out of L1 for a long time. Zhou, Philbin and Li (2001) measured this in second-level buffer caches of storage servers: the reuse distances in the stream were mostly larger than the first-level cache, so [LRU](/lru/) at the second level did poorly, while the frequency of use over a long time was a better guide. This led to their [multi-queue algorithm](/mq-cache/).

**Inclusive.** Every block in L1 is also in L2. A lookup from outside, such as a coherence probe from another core, needs to check only L2. The cost is space: the unique capacity of the pair is only that of L2. There is also a subtle problem. L2 does not see the hits of L1, so its LRU order does not know that a block is hot in L1, and it may evict it. To keep the rule, L2 must then remove the block from L1 too, a *back-invalidation*, and a hot block is lost. Baer and Wang (1988) gave conditions on the sets, ways and block sizes of the two levels under which inclusion can hold, and described how a hierarchy can enforce it with such invalidations. This multilevel inclusion is a design rule; it is not the same as the [inclusion property](/inclusion-property/) of stack algorithms, which compares one policy at two cache sizes.

**Exclusive.** A block is in at most one level. A miss in both levels loads the block into L1 only. When L1 evicts a block, the block moves down to L2, so L2 acts as a victim cache. An L2 hit moves the block up to L1 and removes it from L2. The unique capacity is the sum of the two levels, at the cost of more traffic between them. If both levels are fully associative LRU, the pair holds exactly the $c_1 + c_2$ most recent blocks, so it misses exactly as one LRU cache of size $c_1 + c_2$. Wong and Wilkes (2002) applied the same idea to storage: a client that evicts a block DEMOTEs it to the array, which then holds what the client does not.

**NINE.** A miss fills both levels, and an L2 eviction does not touch L1. Blocks are often in both levels, but a block hot in L1 can leave L2. This is the simplest design, and many recent processors use it for the last level.

**Average memory access time.** Let $h_i$ be the hit time of level $i$ and $m_i$ its *local* miss rate, the share of the requests that reach level $i$ and miss there. With two levels and memory time $M$,

$$\mathrm{AMAT} = h_1 + m_1 \,(h_2 + m_2 M),$$

as Hennessy and Patterson write it: hit time plus miss rate times miss penalty, where the penalty of L1 is itself the AMAT of L2. The *global* miss rate of L2, the share of all requests that go to memory, is $m_1 m_2$. A local miss rate of L2 near 50% may look poor, but it applies only to the few requests that L1 missed.

**Other choices.** Each level also chooses its write rule, such as [write-back](/write-back/), its block size, its associativity, and whether a write miss allocates a block. Levels may [prefetch](/prefetching/) for the level above.

## Examples

**A two-level simulation.** Take a trace of 100,000 requests to 5,000 blocks, each drawn with probability proportional to $1/i^{0.9}$ for the block of rank $i$. L1 holds 100 blocks and L2 holds 400, both LRU. Use hit times of 1 and 10 and a memory time of 100.

| design | L1 hit ratio | L2 local hit ratio | share to memory | AMAT | back-invalidations |
|---|---|---|---|---|---|
| inclusive | 0.305 | 0.270 | 0.507 | 58.7 | 581 |
| NINE | 0.310 | 0.272 | 0.503 | 58.2 | 0 |
| exclusive | 0.310 | 0.329 | 0.463 | 54.2 | 0 |

The exclusive pair misses exactly as one LRU cache of 500 blocks. The inclusive pair loses some L1 hits to back-invalidations and holds only 400 different blocks. On the stream that reaches L2, an LRU cache of 100 blocks hits about 1% of the requests, against about 31% on the original trace: the stream of L1 misses has almost no short reuse.

**A hot block lost by inclusion.** Let L1 hold 2 blocks and L2 hold 3, and request $a, b_0, a, b_1, a, b_2, \ldots, a, b_9$ with ten different blocks $b_i$. Block $a$ hits in L1 every time after the first, so L2 sees only the $b_i$. When the third of them arrives, $a$ is the oldest block in L2, and an inclusive L2 evicts it and invalidates it in L1, so $a$ misses 4 times in 20 requests. NINE and exclusive designs miss on $a$ only once.

**Storage.** A database server caches pages in its own buffer pool, and the storage array caches the same pages again. Without coordination the array holds mostly copies of what the server holds, and its hits are few. DEMOTE, or a second-level policy such as MQ that relies on frequency, makes the second cache useful.

## Where it is used

- **Processors.** Most have private L1 instruction and data caches, a private or shared L2, and a shared L3. Many Intel processors used an inclusive last level, which also served as a filter for coherence probes. Several AMD designs used an exclusive L2 or a victim L3, and many recent processors use a NINE last level.
- **Storage and file systems.** An operating system page cache above a disk or array cache, and a client cache above a file server. The second-level policies MQ and those of Wong and Wilkes aim at this case.
- **The web and content delivery.** A browser cache, then edge servers, then parent caches near the origin.
- **Performance models.** AMAT is the first estimate of the cost of a hierarchy, and the [three Cs](/three-cs-model/) and [miss ratio curves](/miss-ratio-curve/) of each level feed it.

## References
