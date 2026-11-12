---
tag: XJRN9K
kind: concept
slug: cache-aside-pattern
name: Cache-aside pattern
aliases:
- look-aside cache
- cache-aside
- demand-filled look-aside cache
area: systems/caching-policies
level: intro
summary: "The application reads the cache, on a miss reads the store and fills the cache; on a write it updates the store and then deletes the cache key, not sets it."
prereqs: [cache, race-condition]
see_also: [cache-invalidation, ttl-expiration, cache-stampede, write-through, write-around, write-back, eventual-consistency]
sources:
  - paper: "Rajesh Nishtala, Hans Fugal, Steven Grimm, Marc Kwiatkowski, Herman Lee, Harry C. Li, Ryan McElroy, Mike Paleczny, Daniel Peek, Paul Saab, David Stafford, Tony Tung and Venkateshwaran Venkataramani, Scaling Memcache at Facebook, 10th USENIX Symposium on Networked Systems Design and Implementation (NSDI 2013), 385-398"
    title: "Nishtala et al., Scaling Memcache at Facebook, NSDI 2013"
    locator: "Section 2 and Figure 1 (memcache as a demand-filled look-aside cache; a write updates the database and then deletes the key, because deletes are idempotent), and Section 3.2.1 (stale sets)"
  - url: "https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside"
    title: Microsoft, Azure Architecture Center, Cache-Aside pattern
    locator: "the Solution section (read path and invalidation on update) and the note on the order of the steps: update the data store before removing the cached item"
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: "Appendix B, Section B.1 (write-through and no-write allocate, the hardware policies that cache-aside mirrors in software)"
---

The cache-aside pattern is the usual way for an application to use a key-value [cache](/cache/) next to a database: on a read, the application tries the cache, and on a miss it reads the database and puts the value into the cache; on a write, it updates the database and then deletes the cache key. The cache knows nothing about the database; the application does all the work, so the cache "sits aside". Each entry is loaded lazily, on its first miss. The write path must delete the key, not set it, and must update the database first, because the other orders leave stale values in the cache under concurrency; one race remains even with the right order, and [leases](/cache-invalidation/) or a [TTL](/ttl-expiration/) handle it.

## In plain words

A web server keeps a fast cache next to its slow database. To read an item, it first asks the cache. If the cache has it, that is the answer. If not, the server reads the database, puts a copy in the cache for the next reader, and returns the value.

To change an item, the server changes the database and then throws away the copy in the cache. The next reader finds no copy, reads the new value from the database and caches that.

Why throw away the copy instead of writing the new value into the cache? Because two servers can change the same item at almost the same time. Their cache writes can arrive in the other order than their database writes, and then the cache keeps the older value forever. A removal has no order problem: removing twice gives the same result as removing once.

## The idea

### The model

There are two services: a cache $C$, a map from keys to values that may drop any entry at any time (eviction), and a store $S$, the database, which holds the true value of each key. Many application processes use both at the same time. Each single access to $C$ or to $S$ is atomic, but there is no transaction that covers both. We call an entry stale when $C(x)$ exists and differs from $S(x)$, and we ask which interleavings of the accesses leave a stale entry once all operations finish.

### The two paths

```pseudo id=main
READ(x)
L1  v ← C.get(x)
L2  if v is not a miss then return v
L3  v ← S.read(x)
L4  C.set(x, v)
L5  return v

WRITE(x, v)
L6  S.write(x, v)
L7  C.delete(x)
```

The read path fills the cache on demand (lines L3 and L4), which is why the pattern is also called lazy loading. The write path is the software form of [write-around](/write-around/): the write goes to the store only, and a cached copy is removed.

### Why delete, and why the store first

**Update then set has a race between writers.** Suppose line L7 were `C.set(x, v)`. Let writer $W_1$ write 1 and writer $W_2$ write 2, with $S(x) = 0$ at the start:

| step | process | access | $S(x)$ | $C(x)$ |
|---|---|---|---|---|
| 1 | $W_1$ | $S$.write(x, 1) | 1 | (none) |
| 2 | $W_2$ | $S$.write(x, 2) | 2 | (none) |
| 3 | $W_2$ | $C$.set(x, 2) | 2 | 2 |
| 4 | $W_1$ | $C$.set(x, 1) | 2 | 1 |

The store says 2 and the cache says 1, and every later read returns 1 until the next write or an eviction. In general the final cache value is the one of the last set and the final store value the one of the last store write, so the run is stale exactly when the two writers do their sets in the other order than their store writes. Of the 6 interleavings of the two writers, 2 are stale. With the delete of line L7, none of the 6 is stale: after both writers, the key is not in the cache at all. Nishtala and others give another reason for the delete: deletes are idempotent, so a client can retry one safely.

**Delete then update has a race with a reader.** If the writer deletes first, a reader can miss in the gap, read the old value from the store and cache it, and the writer's store write comes too late to remove it. Of the 10 interleavings of one reader that misses (3 accesses) and one such writer (2 accesses), 6 leave a stale entry.

### The race that remains

Even with lines L6 and L7 in the right order, one interleaving of one reader $R$ and one writer $W$ is stale. Start with $S(x) = 0$ and an empty cache:

| step | process | access | $S(x)$ | $C(x)$ |
|---|---|---|---|---|
| 1 | $R$ | $C$.get(x): miss | 0 | (none) |
| 2 | $R$ | $S$.read(x) returns 0 | 0 | (none) |
| 3 | $W$ | $S$.write(x, 1) | 1 | (none) |
| 4 | $W$ | $C$.delete(x) | 1 | (none) |
| 5 | $R$ | $C$.set(x, 0) | 1 | 0 |

**Claim.** In a run of one cache-aside reader that misses and one cache-aside writer, the final entry is stale if and only if the reader's store read comes before the writer's store write and the reader's cache set comes after the writer's delete. *Proof.* Only the reader sets $x$ in the cache; the writer only deletes it. If the reader's set comes before the delete, the delete removes the entry and the cache ends without $x$, which is not stale. If the set comes after the delete, the cache ends with the value that the reader read, and the store ends with 1. That value is 0 if the read came before the store write, which is stale, and 1 otherwise, which is not. $\square$

So the reader's window from line L3 to line L4 must contain the writer's whole window from L6 to L7. That is 1 of the 10 interleavings. It is rare in practice because a database write usually takes longer than a read, but a reader that pauses between L3 and L4, for example for garbage collection, makes it happen. Then the stale value stays until the next write, an eviction or the expiry of a [TTL](/ttl-expiration/). The fix in "Scaling Memcache at Facebook" is a lease: the cache gives the missing reader a token at line L1, the delete at line L7 voids the token, and the cache rejects the set of step 5 in the table above. The [cache invalidation](/cache-invalidation/) page describes the mechanism.

### Cache-aside and the other patterns

| pattern | who talks to the store | read miss | write | main risk |
|---|---|---|---|---|
| cache-aside | the application | application reads store, fills cache | store, then delete key | the read and write race above |
| read-through | the cache | the cache loads from the store | (separate choice) | the cache library must know the store |
| [write-through](/write-through/) | the cache | (separate choice) | cache writes store, then keeps the new value | slower writes; concurrent writers still need ordering |
| [write-back](/write-back/) or write-behind | the cache | (separate choice) | cache keeps the value, writes the store later | loss of writes if the cache fails |

A read-through cache does the read path of cache-aside inside the cache, so many readers that miss on the same key can be served by one load. With cache-aside, each reader loads by itself, which leads to the [cache stampede](/cache-stampede/) when a hot key expires.

### Pitfalls

- **Setting the new value on write.** This brings back the writer race above. Delete instead.
- **Deleting before the write.** This opens a wider window, 6 of 10 interleavings in the small model above.
- **Caching a failed or empty read.** If line L3 fails or finds nothing, caching that answer hides later inserts; give such entries a short TTL or do not cache them.
- **No TTL at all.** Without leases, the remaining race leaves a stale entry with no bound on its life. A TTL turns "stale forever" into "stale for at most the TTL".

## Examples

All the counts in this section come from an exhaustive enumeration of the interleavings, with each access as one atomic step. With one reader that misses (accesses get, read, set) and one writer (write, delete), there are $\binom{5}{2} = 10$ interleavings:

| writer code | stale interleavings |
|---|---|
| store write, then cache delete (cache-aside) | 1 of 10 |
| store write, then cache set | 1 of 10 |
| cache delete, then store write | 6 of 10 |

With two writers and no reader there are $\binom{4}{2} = 6$ interleavings: 2 are stale when each writer sets the cache, and 0 when each deletes. So the correct cache-aside write is the only one of the three that is safe against concurrent writers and has the smallest window against a reader.

A non-example: a cache that the database updates itself, through a trigger or a change stream, is not cache-aside, because the application does not fill the cache on a miss and does not delete on write.

## Where it is used

- **Memcached and Redis in front of SQL databases.** The NSDI 2013 paper describes memcache at Facebook as a demand-filled look-aside cache with delete on write.
- **Web application frameworks.** Fragment and query caches are filled on demand and cleared on update.
- **Multi-region systems.** The delete on write turns into [invalidation](/cache-invalidation/) messages to the caches of other regions, and the remaining races into [eventual consistency](/eventual-consistency/) of the cached view.

## References
