---
tag: ECHMAV
kind: concept
slug: write-around
name: Write-around caching
aliases:
- write-no-allocate
- write-around cache
area: systems/caching-policies
level: intro
summary: "Writes go only to the backing store and never bring a line into the cache (no-write-allocate); only read misses fill it. A cached copy of a written line is dropped or updated."
prereqs: [cache, write-through]
see_also: [write-through, write-back, cache-aside-pattern, cache-invalidation, lru, cache-admission-policy]
sources:
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: "Appendix B, Section B.1, the question What happens on a write? (no-write allocate: write misses do not affect the cache and change only the lower level)"
  - paper: doi:10.1145/165123.165154
    title: "Norman P. Jouppi, Cache write policies and performance, Proceedings of the 20th Annual International Symposium on Computer Architecture (ISCA 1993), 191-201"
    locator: the policies for write misses, split into the choice to fetch on a write and the choice to allocate a line
  - paper: doi:10.1145/356887.356892
    title: "Alan Jay Smith, Cache memories, ACM Computing Surveys 14(3) (1982), 473-530"
    locator: the discussion of fetch on write and of main memory update
---

Write-around is the write policy of a [cache](/cache/) in which a write goes to the backing store only and never allocates a line in the cache: the write-miss rule is no-write-allocate, and only read misses fill the cache. If the written line is already cached, the cache either drops it or updates it in place; with the update, write-around is exactly [write-through](/write-through/) with no-write-allocate. The point of the policy is to keep data that is written but not read soon out of the cache. The cost is a miss on the first read after a write.

## In plain words

A cache keeps copies of some items of a big, slow store. With write-around, a write goes past the cache, straight to the store, as if the cache was not there. The cache takes in an item only when someone reads it and it is not there yet.

This helps when a program writes much data that nobody reads soon, such as a log or a backup. With other policies, each of those writes would take a place in the cache and push out items that readers use all the time. With write-around, the cache keeps those items.

The cost shows when a program reads what it just wrote: the item is not in the cache, so the first read goes to the slow store. If the cache already had a copy of the item, it must drop or update that copy, or readers would see the old value.

## The idea

### The model and the rules

A cache holds at most $k$ lines of $B$ words in front of a store. A request sequence $\sigma$ of length $n$ has reads $R(a)$ and writes $W(a, v)$, with $w$ writes. The replacement policy, for example [LRU](/lru/), is separate. The policy is online and the sizes are uniform. We count read hits, line reads (fetches from the store) and store writes.

- **Read:** a hit uses the cached line; a miss fetches the line from the store and inserts it, evicting a victim if the cache is full.
- **Write miss:** write the word to the store. The cache does not change (no-write-allocate).
- **Write hit, invalidate variant:** write the word to the store and remove the line from the cache.
- **Write hit, update variant:** write the word to the store and to the cached line. This is write-through with no-write-allocate, the pair that Hennessy and Patterson name as the usual one for write-through caches.

The two write-miss rules are the two answers to one question: does a write miss put the line into the cache? Write-allocate says yes, and is the usual partner of [write-back](/write-back/). Jouppi splits the question further, into whether to fetch the line on a write miss and whether to allocate it, which gives more combinations than the two named here.

### What holds for every run

**Invariant.** After each request, the store holds the last value written to every address, and every cached line equals its store line. *Proof by induction.* Both hold for the empty cache. A write changes the store word, so the store is current. In the update variant it changes the same word in the cached line; in the invalidate variant it removes the line; on a miss there is no cached line. A read miss copies a store line into the cache. No step leaves a cached line that differs from the store. $\square$

From the invariant and the rules:

- **Store writes.** Exactly one store write for each write request: $w$ in total, the same as write-through.
- **No dirty data.** No line is ever dirty, eviction is free, and a crash of the cache loses nothing.
- **Writes never fill the cache.** The set of cached lines after a write is a subset of the set before it. So the line reads are exactly the read misses, and every line in the cache was brought in by a read. A write never evicts a line, so a stream of writes cannot push the read working set out.

### When it pays

Write-around wins over write-allocate when written data is rarely read soon after the write, because each write-allocate insert of such data evicts a line that a reader might need. It loses when a read often follows a write to the same line: write-allocate would make that read a hit, and write-around makes it a miss. The update variant keeps hits on lines that are both read and written; the invalidate variant is simpler for a cache that is not on the write path, such as a software cache next to a database, where the writer only knows the key.

### Pitfalls

- **Forgetting the hit case.** A write-around cache that writes the store and ignores a cached copy serves the old value until the line is evicted. Either drop the line or update it.
- **Read after write misses.** A workload that writes a record and reads it back at once, as many web applications do after a form post, gets a miss on every such read.
- **Not a cure for all pollution.** Write-around keeps one-time writes out of the cache, but a scan of one-time reads still pollutes it. That needs a replacement or [admission policy](/cache-admission-policy/).

## Examples

Take $k = 2$, $B = 1$, LRU and an empty start, on $W(a,1)$, $W(a,2)$, $R(a)$, $W(b,4)$, $R(c)$, $W(a,6)$, $R(b)$, $R(a)$.

| step | request | invalidate variant: cache after | update variant: cache after |
|---|---|---|---|
| 1 | $W(a,1)$ | (empty) | (empty) |
| 2 | $W(a,2)$ | (empty) | (empty) |
| 3 | $R(a)$ | miss, $a{=}2$ | miss, $a{=}2$ |
| 4 | $W(b,4)$ | $a{=}2$ | $a{=}2$ |
| 5 | $R(c)$ | miss, $a{=}2$, $c{=}0$ | miss, $a{=}2$, $c{=}0$ |
| 6 | $W(a,6)$ | hit, drop $a$: $c{=}0$ | hit, update: $c{=}0$, $a{=}6$ |
| 7 | $R(b)$ | miss, $c{=}0$, $b{=}4$ | miss, $a{=}6$, $b{=}4$ |
| 8 | $R(a)$ | miss, $b{=}4$, $a{=}6$ | hit |

The invalidate variant has 0 read hits and 4 line reads; the update variant has 1 read hit and 3 line reads. Both make 4 store writes. A write-through cache with write-allocate gets 2 read hits on this sequence, at the cost of 5 line reads.

**Pollution.** Let a reader cycle over 4 hot lines with $k = 4$, and let a writer write one new line between each two reads, for 50 rounds: 200 reads and 200 writes of distinct new lines. Under write-around the hot lines enter on the first 4 reads and stay, so 196 of the 200 reads hit. Under LRU with write-allocate, between two reads of a hot line come 4 new written lines and 3 other hot lines, 7 distinct lines in all, so each read misses: 0 read hits.

A non-example: a cache that allocates a line on a write miss but does not fetch it first (it fills only the written words) is not write-around, because the write still puts the line into the cache.

## Where it is used

- **Processor caches** with write-through, where no-write-allocate is the common choice.
- **Block storage caches** on fast drives in front of slow disks, which offer write-around as a mode for workloads that write much more than they read back.
- **Application caches.** In the [cache-aside pattern](/cache-aside-pattern/), a write goes to the database and then deletes the cache key: this is write-around with the invalidate variant, done by the application.
- **Bulk loads and backups,** where a hint from the program marks the writes as streaming so that they bypass the cache.

## References
