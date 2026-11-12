---
tag: J9Z92K
kind: concept
slug: write-through
name: Write-through caching
aliases:
- write-through cache
- store-through cache
- write-through policy
area: systems/caching-policies
level: intro
summary: "A write hit policy: each write updates the cached copy and the backing store at once, so the store is always current and no cached line is ever dirty."
prereqs: [cache, cache-hit-ratio]
see_also: [write-back, write-around, cache-aside-pattern, cache-invalidation, lru, multilevel-caching, write-ahead-logging]
sources:
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: "Appendix B, Section B.1, the question What happens on a write? (write through, write back, write buffers, write allocate and no-write allocate)"
  - paper: doi:10.1145/356887.356892
    title: "Alan Jay Smith, Cache memories, ACM Computing Surveys 14(3) (1982), 473-530"
    locator: the discussion of main memory update, write-through (store-through) against copy-back
  - paper: doi:10.1145/165123.165154
    title: "Norman P. Jouppi, Cache write policies and performance, Proceedings of the 20th Annual International Symposium on Computer Architecture (ISCA 1993), 191-201"
    locator: the policies for write misses (fetch-on-write and write-allocate) and the trade-off of write-through and write-back on write hits
---

Write-through is a write policy of a [cache](/cache/) that sits in front of a slower backing store: each write changes the cached copy, if there is one, and the store, in the same operation. So the store always holds the latest value, every cached line is clean, and an eviction never has to write anything. The price is one store write for each write request, however often the program writes the same line. A write-through cache needs a second rule for a write that misses: fetch the line and keep it (write-allocate), or leave the cache as it is (no-write-allocate). The usual pair is write-through with no-write-allocate.

## In plain words

A cache keeps copies of some items of a big, slow store. Reads are easy: if the copy is there, use it. Writes raise a question: when does the slow store learn about the new value?

Write-through answers "now". Every write goes to the slow store at once, and to the copy in the cache if the cache has one. The store is never behind the cache. If the cache loses power, or a line is thrown out, nothing is lost, because the store already has every write.

The cost is that every write pays for a trip to the slow store. A program that writes the same counter a thousand times sends a thousand writes to the store. The [write-back](/write-back/) policy keeps the writes in the cache and sends only the final value, at the cost of a store that can be behind.

## The idea

### The model

A cache holds at most $k$ lines. A line is a block of $B$ consecutive words of the store, and the cache moves whole lines when it reads from the store. A request sequence $\sigma = \sigma_1 \cdots \sigma_n$ has reads $R(a)$ and writes $W(a, v)$ of word addresses $a$, and $a$ belongs to line $\lfloor a / B \rfloor$. The replacement policy, for example [LRU](/lru/), chooses which line to evict on a miss; the write policy is a separate choice. All sizes are uniform and the policy is online. We count three things in a run: the line reads (fetches of a line from the store), the store writes (write operations on the store) and the words written.

### The two rules

A write policy has a rule for a write hit and a rule for a write miss.

- **Write hit, write-through:** on $W(a, v)$ with the line in the cache, change the word in the cache and write $v$ to the store.
- **Write miss, no-write-allocate:** on $W(a, v)$ with the line not in the cache, write $v$ to the store only. The cache does not change. Only read misses bring lines in.
- **Write miss, write-allocate (fetch on write):** fetch the line from the store, put it in the cache (evicting a line if the cache is full), change the word, and also write $v$ to the store.

Hennessy and Patterson give write-through with no-write-allocate as the usual pair. The reason is that the write goes to the store in any case, so a fetch on a write miss pays a line read that only helps if the program reads the line again soon. Write-through with no-write-allocate is the same policy as [write-around](/write-around/) in its variant that updates a cached line on a write hit.

### What holds for every run

**Invariant.** After each request, (1) the store holds the last value written to each address, and (2) each cached line equals the store line. *Proof by induction on the requests.* Both parts hold at the start, with an empty cache. A read changes no value; on a miss it copies a line from the store, which keeps (2). A write $W(a, v)$ sets word $a$ in the store to $v$, which keeps (1), and it sets the same word in the cached line, if the line is cached or allocated, which keeps (2). An eviction removes a line and changes no value. $\square$

From the invariant:

- **Store writes.** A write-through cache makes exactly one store write of one word for each write request, so the store write count equals the number of writes $w$ in $\sigma$, for every $k$ and every replacement policy.
- **Evictions are free.** No line is dirty, so the cache drops a victim without a store write and needs no dirty bit.
- **A crash loses nothing.** If the cache loses its contents, the store already holds every completed write. Compare [write-back](/write-back/), where a crash loses the dirty lines.
- **Reads see the last write.** A read hit returns the cached word, which equals the store word by (2), which is the last written value by (1).

### The cost, and the write buffer

The weak point is the write traffic: $w$ store writes instead of at most one for each line that a write dirties. In a processor, a write to main memory takes many cycles, so a write-through cache stalls the processor unless it puts the write into a write buffer and goes on. The buffer drains to memory in the background. The processor stalls only when the buffer is full, and a read miss must check the buffer, or wait for it to drain, so that it does not read an old value from memory. Hennessy and Patterson describe both the write buffer and the priority of read misses over buffered writes in Appendix B.

### Pitfalls

- **Other writers.** The invariant assumes that all writes go through this cache. If another program writes the store directly, a cached line becomes stale and write-through does not help; the cache needs [invalidation](/cache-invalidation/) or a [TTL](/ttl-expiration/).
- **Order of the two writes in software.** An application-level write-through cache that updates the cache first and the store second shows a value that the store may never get, if the store write fails. Update the store first. Even then, two concurrent writers can leave the cache with the older value; the [cache-aside pattern](/cache-aside-pattern/) page shows the interleaving.
- **Write-allocate traffic.** With write-allocate, a write miss costs a line read and a store write. On a stream of writes to new lines this doubles the traffic and pushes useful lines out of the cache.

## Examples

Take a cache of $k = 2$ lines with $B = 1$, LRU replacement and an empty start, on the sequence $W(a,1)$, $W(a,2)$, $R(a)$, $W(b,4)$, $R(c)$, $W(a,6)$, $R(b)$, $R(a)$. With no-write-allocate:

| step | request | result | cache after (LRU first) | line reads | store writes |
|---|---|---|---|---|---|
| 1 | $W(a,1)$ | miss | (empty) | 0 | 1 |
| 2 | $W(a,2)$ | miss | (empty) | 0 | 2 |
| 3 | $R(a)$ | miss | $a{=}2$ | 1 | 2 |
| 4 | $W(b,4)$ | miss | $a{=}2$ | 1 | 3 |
| 5 | $R(c)$ | miss | $a{=}2$, $c{=}0$ | 2 | 3 |
| 6 | $W(a,6)$ | hit | $c{=}0$, $a{=}6$ | 2 | 4 |
| 7 | $R(b)$ | miss | $a{=}6$, $b{=}4$ | 3 | 4 |
| 8 | $R(a)$ | hit | $b{=}4$, $a{=}6$ | 3 | 4 |

At every step each cached value equals the store value. With write-allocate the same sequence gives 2 read hits instead of 1 (step 3 hits, because step 1 brought $a$ in), but 5 line reads instead of 3, because each write miss also fetches its line. Both runs make 4 store writes, one for each write request.

A non-example: a cache that writes to the store only every 30 seconds, or only on eviction, is not write-through, even if it writes everything in the end. Between the flushes its store is behind, and that is the behavior of [write-back](/write-back/).

## Where it is used

- **Processor caches.** Many first-level data caches have been write-through, with a write buffer, so that the second level holds the current data and the first level never has dirty lines to write when it evicts. The next level is often write-back, see [multilevel caching](/multilevel-caching/).
- **Caches that must survive a crash.** A disk or storage controller cache without battery backup runs in write-through mode, because a write-back cache would lose acknowledged writes on a power loss. The same reasoning drives the force rule of databases, see [steal and force policies](/steal-and-force-policies/).
- **Application caches.** A read-through cache library that also writes through keeps a cache in front of a database and writes each update to both. The application sees one interface, and the cache is never behind its own writes; writes from outside still need [invalidation](/cache-invalidation/).
- **Shared-memory systems.** A store that is always current simplifies I/O and keeping several caches coherent, at the cost of bus or memory traffic on every write.

## References
