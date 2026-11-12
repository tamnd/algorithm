---
tag: AH1HP7
kind: abstract-type
slug: cache
name: Cache
aliases:
- Cache (abstract type)
- cache abstract data type
- cache memory
area: systems/caching-policies
level: intro
summary: "A store of bounded size that keeps copies of some items of a larger, slower store, so that repeated requests are fast. A replacement policy chooses what to drop."
prereqs: [memory-hierarchy]
see_also: [cache-hit-ratio, locality-of-reference, lru-cache, belady-optimal, paging-problem, write-back, miss-ratio-curve, cache-replacement-policy]
sources:
  - paper: doi:10.1145/356887.356892
    title: "Alan Jay Smith, Cache memories, ACM Computing Surveys 14(3) (1982), 473-530"
    locator: the survey of fetch, placement and replacement algorithms, line size, store-through and copy-back, and cold-start and warm-start miss ratios
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: Appendix B, Review of Memory Hierarchy (block placement, block identification, block replacement and write strategy)
  - url: "https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys-policy.pdf"
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces, Chapter 22, Beyond Physical Memory, Policies
    locator: Section 22.1, Cache Management, and the replacement policies of the rest of the chapter
  - paper: doi:10.1147/sj.52.0078
    title: "L. A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2) (1966), 78-101"
    locator: the replacement problem for a two-level store, and the optimal rule MIN
---

A cache is a store with room for at most $k$ items that keeps copies of some items of a larger and slower *backing store*, so that a request for an item it holds is served fast. A request for a held item is a *hit*; any other request is a *miss*, which reads the backing store and usually puts the item in the cache. When the cache is full, a *replacement policy* chooses the item to drop. The contract of a cache says only which answers are correct; the policy decides the cost, which is counted as the number of misses or the [hit ratio](/cache-hit-ratio/).

## In plain words

You keep a few books on your desk and the rest in a library across town. When you need a book that is on your desk, you take it at once. When it is not, you go to the library, which is slow, and you bring the book back. The desk has room for only a few books. If it is full, you must take one book back before you can put the new one down. Which book you take back does not change what you read. It only changes how many trips you make.

A cache is the desk. The library is the slow store. The rule that picks the book to take back is the replacement policy. Programs tend to need the same items again and items near each other, so a small desk saves many trips.

## Operations

Let $U$ be the set of keys, and let the backing store be a map $B : U \to V$. A cache $C$ holds a set of pairs $(x, B(x))$ with distinct keys. The cache size is $k \ge 1$ items, or a number of bytes when the items have sizes. The operations are:

- `get(C, x) -> (v, hit)`: if $x$ is in $C$, return its value and `hit = true`. Otherwise read $v = B(x)$, call `admit(C, x, v)`, and return $v$ with `hit = false`.
- `admit(C, x, v) -> evicted`: put $(x, v)$ in $C$. If this makes $C$ too big, remove items chosen by the replacement policy and return them.
- `invalidate(C, x)`: remove $x$ from $C$ if it is there. A program calls it when $B(x)$ changes outside the cache, see [cache invalidation](/cache-invalidation/).
- `put(C, x, v)`: change the value of $x$. A [write-through](/write-through/) cache also writes $B(x) = v$ at once. A [write-back](/write-back/) cache marks the item dirty and writes it to $B$ when it is evicted.

Many systems split `get` into `lookup(C, x) -> v or none` and a separate `admit`, so that the program reads the backing store itself. That is the [cache-aside pattern](/cache-aside-pattern/). A hardware cache does `get` on each load. A page cache of an operating system does `get` on each page access, and a miss is a [page fault](/page-fault/).

## Laws

These laws hold for each policy. They state what a cache must do; the policy chooses among the behaviors they allow.

1. **Capacity.** After each operation, $C$ holds at most $k$ items, or items of total size at most the capacity.
2. **Transparency.** If $B$ does not change, `get(C, x)` returns $B(x)$. With writes, a later `get(C, x)` returns the last value written by `put`. So the results of a program do not depend on the policy or on $k$, only its speed does.
3. **Hit condition.** `get(C, x)` is a hit if and only if $x$ was in $C$ just before the call.
4. **The request stays.** In a demand cache, $x$ is in $C$ after `get(C, x)`. A cache with an [admission policy](/cache-admission-policy/) may skip `admit` on a miss, and then this law does not hold.
5. **Invalidation.** After `invalidate(C, x)`, the key $x$ is not in $C$.

Example: a cache with $k = 2$ that drops the least recently used item gets the keys $a, b, a, c, b$. The results are miss, miss, hit, miss (drop $b$), miss (drop $a$). It has 1 hit in 5 requests. Each `get` returned the value of the backing store, as law 2 says.

The cost of a policy on a request sequence $\sigma = \sigma_1 \cdots \sigma_n$ is its number of misses, or the bytes or the total cost of the misses when items have sizes or costs. The [three Cs model](/three-cs-model/) splits the misses by cause.

## Implementations

- **A hash table and a list.** The [LRU cache](/lru-cache/) keeps a [hash table](/hash-table/) from keys to the nodes of a [doubly linked list](/doubly-linked-list/) in order of use. Each operation costs $O(1)$ time, expected because of the hash table.
- **Clock.** [CLOCK](/clock/) keeps the items in a circular array with one reference bit each. It approximates LRU and needs no list update on a hit.
- **Sets in hardware.** A [set-associative cache](/set-associative-cache/) maps each key to one small set by some bits of its address and replaces within the set. A direct-mapped cache has sets of one line, and a fully associative cache has one set.
- **Adaptive policies.** [ARC](/arc/), [LIRS](/lirs/) and [W-TinyLFU](/w-tinylfu/) keep more state per item to resist scans and to use frequency.
- **Levels.** Real systems stack caches into a [hierarchy](/multilevel-caching/): registers, the processor caches, main memory as a cache of the disk, and caches in front of databases and web servers.

## Lower bounds

The lower bounds are on the number of misses, for a sequence $\sigma$ of $n$ requests, a cache of $k$ items of size 1, and a miss cost of 1.

- **Compulsory misses.** From an empty cache, each policy misses at least once on each distinct key of $\sigma$.
- **The offline optimum.** If $\sigma$ is known in advance, [Belady's MIN](/belady-optimal/) has the fewest misses: it evicts the item whose next request is furthest in the future. No policy, online or offline, does better.
- **Online policies.** A policy that does not see the future can have up to $k$ times as many misses as MIN on some sequences, and LRU and FIFO reach this factor and no more ([LRU competitiveness](/lru-competitiveness/)). Random policies do better against an oblivious adversary, with a factor of order $\ln k$ ([the harmonic bound](/harmonic-paging-bound/)).
- **Sizes and costs.** With items of different sizes, finding the optimum offline is NP-hard ([variable-size caching](/variable-size-caching/)).

The [paging problem](/paging-problem/) is the same question in the language of online algorithms. This page gives the contract that each cache meets; that page studies the cost of the policies.

## References
