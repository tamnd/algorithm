---
tag: N20ZB0
kind: concept
slug: cache-invalidation
name: Cache invalidation
aliases:
- cache purge
area: systems/caching-policies
level: intro
summary: "Making a cache stop serving a value once the store changes: explicit deletes, TTLs, versioned keys, and leases that reject a set that carries a value read before a delete."
prereqs: [cache-aside-pattern, ttl-expiration]
see_also: [cache-stampede, write-through, write-around, load-linked-store-conditional, leader-lease, eventual-consistency, read-your-writes]
sources:
  - paper: "Rajesh Nishtala, Hans Fugal, Steven Grimm, Marc Kwiatkowski, Herman Lee, Harry C. Li, Ryan McElroy, Mike Paleczny, Daniel Peek, Paul Saab, David Stafford, Tony Tung and Venkateshwaran Venkataramani, Scaling Memcache at Facebook, 10th USENIX Symposium on Networked Systems Design and Implementation (NSDI 2013), 385-398"
    title: "Nishtala et al., Scaling Memcache at Facebook, NSDI 2013"
    locator: "Section 2 (delete on write, deletes are idempotent) and Section 3.2.1, pp. 388-389 (leases: stale sets, thundering herds, one token per key every 10 seconds by default, stale values)"
  - paper: "Cary G. Gray and David R. Cheriton, Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency, 12th ACM Symposium on Operating Systems Principles (SOSP 1989)"
    title: "Gray and Cheriton, Leases, SOSP 1989"
    locator: "the lease idea: a time-bounded grant that a server gives to a cache, cited by Nishtala et al. for the name"
  - url: "https://www.rfc-editor.org/rfc/rfc9111"
    title: "RFC 9111, HTTP Caching, 2022"
    locator: "Section 4.2 (freshness lifetime) and Section 4.3 (validation of stored responses)"
---

Cache invalidation is the work of making a [cache](/cache/) stop serving a value once the true value in the store has changed. The cache and the store are separate systems with no transaction that covers both, many processes read and write at the same time, and messages can be late, so a cache can end with an old value and keep serving it. There are four main tools: explicit invalidation, where the writer deletes the cached key; a [TTL](/ttl-expiration/), which bounds how long any value can live; versioned keys, which make an old entry unreachable instead of removing it; and leases, which let the cache reject a fill that carries a value read before a delete. A well-known saying, attributed to Phil Karlton, holds that cache invalidation is one of the two hard things in computer science; the races on this page show why.

## In plain words

A cache keeps copies, and copies become wrong when the original changes. Invalidation stops the cache from using a wrong copy.

The simplest way: when you change the original, tell the cache to throw its copy away. A second way: give every copy a time limit, so a wrong copy lives only for a short time. A third way: give each version of the data a new name, so readers ask for the new name and never find the old copy.

The hard part is timing. A reader can fetch the old original, get delayed, and put that old copy into the cache after the writer threw the copy away. A lease stops this. When the reader misses, the cache gives it a ticket. If the copy is thrown away before the reader comes back, the ticket stops being valid, and the cache refuses the late, old copy.

## The idea

### What can go wrong

Use the model of the [cache-aside pattern](/cache-aside-pattern/): a cache $C$ and a store $S$, each access to one of them atomic, no transaction over both. An entry is stale when $C(x)$ exists and differs from $S(x)$. A writer that updates $S$ and then deletes $x$ from $C$ is safe against other writers, but one reader that misses, reads $S$ before the write, and sets $C$ after the delete leaves a stale entry, in 1 of the 10 interleavings of one reader and one writer. Nothing removes that entry until the next write, an eviction, or a TTL.

### Explicit invalidation

The writer, or a process that watches the store, sends a delete for each key that a write changed. A delete is better than an update of the cached value, because two updates can arrive in the other order than the store writes, and the older value wins; two deletes in any order leave the same result. Nishtala and others also prefer deletes because they are idempotent, so a client can retry a lost one. In large systems the deletes go out as messages: the memcache paper describes daemons that read the database commit log and send the deletes to the caches. HTTP caches and content delivery networks call the same operation a purge.

Explicit invalidation needs the writer to know every key that depends on the changed data. A cached page that combines ten rows must be deleted when any of the ten change, and a missing dependency gives a stale entry with no bound on its life.

### Time to live

A [TTL](/ttl-expiration/) needs no message at all: an entry set at time $t$ with lifetime $T$ is never served at time $t + T$ or later. So with an absolute TTL no served value is older than $T$, whatever went wrong with the deletes. A short $T$ costs hit ratio, and a TTL is not a substitute for deletes when stale reads are not acceptable. Most systems use both: the delete for speed, the TTL as a bound on the damage of a lost delete or a race.

### Versioned keys

Put a version number into the key: readers look up `user:42:v7`, not `user:42`. A writer stores the new value and then increases the version in a small, authoritative place, such as the store row itself or a version key. Readers first read the current version, then the versioned key. An old entry is never deleted; it just becomes unreachable and leaves the cache by eviction or TTL. A whole group of keys can be invalidated in one step by a version number for the group, a namespace generation. The cost is one more lookup per read, and the version itself must be read from a place that is not stale, or the problem only moves. Web assets use the same idea with a content hash in the file name, which is why the alias cache busting belongs here: the old file is never invalid, it is simply never requested again.

### Leases

The lease of Nishtala and others, in Section 3.2.1 of "Scaling Memcache at Facebook", closes the reader race of the cache-aside pattern:

1. On a miss, the cache gives the client a lease token, a 64-bit number bound to the key the client asked for.
2. The client reads the store and presents the token when it sets the value.
3. The cache stores the value only if the token is still valid. A delete of the key invalidates the token, so a set that comes after a delete is rejected.

The paper compares this to load-link and store-conditional: the get is the [load-link](/load-linked-store-conditional/), and the set succeeds only if no delete came in between.

**Claim.** Assume that every writer updates the store and then deletes the key, that every reader sets the cache only with a lease token, and that a token is voided by any delete of its key and by any newer token for the key. Then when all operations finish, no entry is stale. *Proof.* If the key is in the cache at the end, take the last successful set $s$, made by a reader that got its token at time $g$ and read the store at time $r$, with $g < r < s$. Its token was valid at $s$, so no delete of the key happened between $g$ and $s$. No delete happened after $s$ either, or the entry would be gone. So every delete came before $g$. Each store write comes before its delete, so every store write came before $g$, hence before $r$, and the reader read the final store value. $\square$

The proof does not depend on the number of readers and writers. The enumeration in the Examples section checks it for one and two readers.

Leases also handle two other problems, as described in the same section of the paper:

- **Thundering herds.** The cache regulates the rate at which it returns tokens: by default, at most one token per key every 10 seconds. A client that misses while a token is out gets a special reply that tells it to wait a short time and retry. Usually the holder of the token has set the value by then, so the retry hits. This is one of the fixes on the [cache stampede](/cache-stampede/) page. If the holder fails, the next token after the 10 seconds goes to another client, and the new token voids the old one.
- **Stale values.** When a key is deleted, the cache keeps the old value for a short time in a structure of recently deleted items. A get can then return a lease token or data marked as stale, and a client that can accept slightly old data uses it instead of waiting.

The paper reports that leases reduced the peak rate of database queries from 17,000 to 1,300 per second. The name comes from the leases of Gray and Cheriton, a time-bounded grant from a server to a cache, which is also the idea behind a [leader lease](/leader-lease/).

### Pitfalls

- **Delete before the store write.** A reader that misses in between caches the old value; this is 6 of the 10 interleavings in the cache-aside model.
- **Lost deletes.** A delete sent over the network can be lost. Retry it, which is safe because a delete is idempotent, and keep a TTL as a bound.
- **Read replicas.** If readers fill the cache from a database replica that lags the primary, a reader can miss after the delete and still read the old value from the replica. Deleting the key again after the replica catches up, or reading the primary after a recent write, closes this gap.
- **Many layers.** A value can sit in a local process cache, a shared cache and a content delivery network at once. Each layer needs its own invalidation or its own TTL, and the staleness bounds add up.

## Examples

**The reader race with and without leases.** One reader that misses and one writer (store write, then delete), starting with $S(x) = 0$. The counts come from an exhaustive enumeration of all interleavings, with each access as one atomic step:

| processes | plain cache: stale runs | lease cache: stale runs |
|---|---|---|
| 1 reader, 1 writer | 1 of 10 | 0 of 10 |
| 2 readers, 1 writer | 70 of 534 | 0 of 90 |

The runs are fewer with leases because a reader that misses while another holds a token gets a wait reply and stops. In the bad schedule of the first row (reader get, reader store read, writer store write, writer delete, reader set) the lease cache rejects the set, and the cache stays empty, so the next reader loads the value 1.

**The herd.** 50 clients miss on one key, one every millisecond, a store read takes 100 ms, and a client told to wait retries after 10 ms. With a plain cache, all 50 clients miss before the first set, and the store gets 50 reads. With leases, the first client gets the token, the other 49 wait and retry, the store gets 1 read, and every client has the value by 110 ms.

**A versioned key.** The store holds version 7 of user 42, and the cache holds `user:42:v7`. A writer saves the new row and sets the version to 8. A reader that read version 7 just before may still return the old value once, but every reader that reads the version afterwards asks for `user:42:v8`, misses, and loads the new value. The entry `user:42:v7` is never deleted; LRU or its TTL removes it later.

## Where it is used

- **Memcache at Facebook.** Delete on write, deletes sent from the commit log to the caches, and leases against stale sets and herds, all in the NSDI 2013 paper.
- **HTTP caches and content delivery networks.** Freshness lifetimes are TTLs, validation asks the origin whether a stored response is still current (RFC 9111, Sections 4.2 and 4.3), and purge requests delete objects at once. Content-hashed asset names are versioned keys.
- **Hardware caches.** A cache coherence protocol invalidates the copies of a line in the caches of other cores when one core writes it. The same pattern of delete on write appears in [write-around](/write-around/) caches; a [write-through](/write-through/) cache instead updates its copy together with the store.
- **Distributed file systems.** Leases in the sense of Gray and Cheriton let a client cache a file and be sure that no other client changes it until the lease ends.

## References
