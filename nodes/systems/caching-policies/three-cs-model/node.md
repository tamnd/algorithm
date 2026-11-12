---
tag: 5TNN9R
kind: concept
slug: three-cs-model
name: Three Cs model of misses
aliases:
- 3C model
- compulsory capacity and conflict misses
- three Cs of cache misses
area: systems/caching-policies
level: intro
summary: "Hill and Smith's split of cache misses into compulsory, capacity and conflict misses, measured against an infinite cache and a fully associative LRU cache of the same size."
prereqs: [cache-hit-ratio, locality-of-reference]
see_also: [set-associative-cache, cache, reuse-distance, prefetching, multilevel-caching, miss-ratio-curve, belady-optimal, lru]
sources:
  - paper: doi:10.1109/12.40842
    title: "Mark D. Hill and Alan Jay Smith, Evaluating associativity in CPU caches, IEEE Transactions on Computers 38(12) (1989), 1612-1630"
    locator: the definitions of compulsory, capacity and conflict misses, with the fully associative cache of the same size as the reference point
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: Appendix B, Review of Memory Hierarchy (the three Cs, the fourth C of coherence misses, and the basic optimizations that reduce each kind)
  - paper: doi:10.1145/356887.356892
    title: "Alan Jay Smith, Cache memories, ACM Computing Surveys 14(3) (1982), 473-530"
    locator: the effect of set size and line size on the miss ratio
---

The three Cs model sorts the misses of a cache into three kinds by their cause. A *compulsory* miss is the first request for a block, which no cache can avoid. A *capacity* miss is a miss that would happen even in a fully associative cache of the same size, because the program uses more data than the cache holds. A *conflict* miss is a miss that happens only because the cache is set associative or direct mapped, so that too many blocks compete for one set while other sets have room. Mark Hill and Alan Jay Smith gave the model its standard form in 1989. Its point is practical: each kind of miss has a different cure.

## In plain words

Think of a parking garage where each car may park only on the floor given by the last digit of its plate. A driver who comes for the first time must look for a spot; that cost is unavoidable. When the whole garage is full, some driver must leave; that is a problem of size. But a driver may also be turned away from a full floor while other floors are empty. That last problem comes from the rule about floors, not from the size.

A hardware cache works the same way. The first use of a block always misses. Some misses come from a cache that is too small for the data. The rest come from the rule that each block may go into only a few places. To count them, compare the real cache with a perfect one of the same size, where any block may go anywhere.

## The idea

Fix a trace of block addresses, a cache of $C$ blocks with $S$ sets of $A$ ways each ($C = S A$), and its replacement policy. Run three simulations on the same trace:

1. An infinite cache. Its misses are the first references to each block, $M_{\text{inf}}$ = the number of distinct blocks.
2. A fully associative LRU cache of $C$ blocks, with misses $M_{\text{fa}}$.
3. The real cache, with misses $M$.

Then

$$\text{compulsory} = M_{\text{inf}}, \qquad \text{capacity} = M_{\text{fa}} - M_{\text{inf}}, \qquad \text{conflict} = M - M_{\text{fa}}.$$

The three numbers add up to $M$ by construction. The first two depend only on the trace and on $C$. Because a fully associative LRU cache hits exactly the requests whose [reuse distance](/reuse-distance/) is less than $C$, the capacity misses are the requests with reuse distance at least $C$, apart from first references. The conflict misses are the only part that depends on the mapping of blocks to sets and on the policy inside a set.

**Conflict misses can be negative.** The model uses LRU as the reference policy, and LRU is not optimal. A set associative cache can, by chance, keep a block that the fully associative LRU cache drops, and then its conflict count is below zero. This happens on cyclic traces, where LRU is at its worst. Some authors use [Belady's MIN](/belady-optimal/) for the fully associative cache to separate the misses of a bad policy from the misses of a small cache, and then the capacity and the conflict counts change.

**Cures.** Larger blocks and [prefetching](/prefetching/) reduce compulsory misses. A larger cache reduces capacity misses. Higher associativity, a better hash of addresses to sets, or a small fully associative victim cache reduces conflict misses. In a [set-associative cache](/set-associative-cache/) design, the three Cs show which of these is worth its cost in time and area.

**A fourth C.** In a multiprocessor, a block can also be lost because another processor wrote to it, which invalidates the copy. These *coherence* misses are often counted as a fourth kind.

## Examples

In each example a block $b$ goes to set $b \bmod S$, and the real cache has 4 blocks.

**Pure conflict.** Trace $0\,4\,0\,4\,0\,4\,1\,2$, direct mapped with 4 sets. Blocks 0 and 4 both go to set 0 and evict each other on every request.

| cache | total | compulsory | capacity | conflict |
|---|---|---|---|---|
| direct mapped, 4 sets | 8 | 4 | 0 | 4 |
| 2-way, 2 sets | 4 | 4 | 0 | 0 |

There are only 4 distinct blocks, so a fully associative cache of 4 blocks misses only on first references. With two ways per set, blocks 0 and 4 share set 0 without trouble, and all 4 conflict misses go away.

**Mixed.** Trace $0\,8\,1\,9\,0\,8\,1\,9\,2\,3\,4\,5\,6\,0$. The fully associative LRU cache of 4 blocks has 10 misses: 9 compulsory and 1 capacity miss, the last request for block 0.

| cache | total | compulsory | capacity | conflict |
|---|---|---|---|---|
| direct mapped, 4 sets | 14 | 9 | 1 | 4 |
| 2-way, 2 sets | 10 | 9 | 1 | 0 |

**Negative conflict.** Trace $0\,1\,2\,3\,4\,0\,1\,2\,3\,4$, a cycle of 5 blocks through a cache of 4. The fully associative LRU cache misses on all 10 requests, so there are 5 compulsory and 5 capacity misses. The direct-mapped cache with 4 sets has 7 misses: blocks 0 and 4 fight over set 0, but blocks 1, 2 and 3 stay in their sets and hit on the second pass. So its conflict count is $7 - 10 = -3$. A 2-way cache with 2 sets has 8 misses and a conflict count of $-2$.

## Where it is used

- **Processor cache design.** Architects use the three Cs to choose the size, the block size and the associativity of a cache, and to decide whether a victim cache or a prefetcher pays off.
- **Compiler and program tuning.** Array padding and changes of data layout remove conflict misses; loop tiling removes capacity misses, see [locality of reference](/locality-of-reference/).
- **Teaching and performance tools.** Cache simulators report misses split this way, so that a programmer can tell a working set that is too large from an unlucky mapping of addresses.
- **Other caches.** The same split applies to any cache with restricted placement, such as a translation buffer or a hash-partitioned software cache.

## References
