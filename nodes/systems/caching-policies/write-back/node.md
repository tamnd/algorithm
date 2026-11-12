---
tag: 67S2DT
kind: concept
slug: write-back
name: Write-back caching
aliases:
- copy-back
- write-behind
- write-back cache
- copy-back cache
area: systems/caching-policies
level: intro
summary: "A write hit policy: a write changes only the cached line and sets its dirty bit. The line goes to the store when it is evicted, so repeated writes cost one store write."
prereqs: [cache, write-through]
see_also: [write-through, write-around, write-ahead-logging, steal-and-force-policies, crash-recovery, multilevel-caching, lru]
sources:
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: "Appendix B, Section B.1, the question What happens on a write? (write back, the dirty bit, write allocate and no-write allocate, and the usual pairs of policies)"
  - paper: doi:10.1145/356887.356892
    title: "Alan Jay Smith, Cache memories, ACM Computing Surveys 14(3) (1982), 473-530"
    locator: the discussion of main memory update, copy-back against write-through, and the traffic of each
  - paper: doi:10.1145/165123.165154
    title: "Norman P. Jouppi, Cache write policies and performance, Proceedings of the 20th Annual International Symposium on Computer Architecture (ISCA 1993), 191-201"
    locator: the write traffic of write-back against write-through on write hits, and the write-miss policies
  - url: "https://pages.cs.wisc.edu/~remzi/OSTEP/file-implementation.pdf"
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces, Chapter 40, File System Implementation
    locator: the section on caching and buffering (write buffering in memory, the loss of buffered writes on a crash, and fsync)
---

Write-back is a write policy of a [cache](/cache/) in front of a slower store: a write that hits changes only the cached line and marks it dirty, and the cache writes a dirty line to the store only when it evicts the line or is told to flush. So many writes to one line cost one store write, and the store can be behind the cache. A crash of the cache loses every dirty line. The usual write-miss rule with write-back is write-allocate: fetch the line, then write it in the cache. Smith's survey calls the policy copy-back.

## In plain words

A cache keeps copies of some items of a big, slow store. With write-back, a write changes only the copy in the cache. The cache puts a mark on the copy, the dirty mark, to remember that the store has an old value. Later, when the cache needs the room and throws the copy out, it first writes the copy back to the store.

If a program writes the same item a thousand times, the store sees one write, at the end. This saves a lot of traffic. The price is risk and work: until the copy goes back, only the cache has the newest value. If the cache loses its contents in a crash, the newest values are gone. And when the cache throws out a dirty copy to make room, a read miss must wait for the old copy to be written first.

## The idea

### The model

A cache holds at most $k$ lines of $B$ words each, in front of a store. A request sequence $\sigma = \sigma_1 \cdots \sigma_n$ has reads $R(a)$ and writes $W(a, v)$ of word addresses, and $w$ is the number of writes. A replacement policy such as [LRU](/lru/) chooses the victim; it does not look at the dirty bits. The policy is online and the sizes are uniform. We count the line reads, the store writes (write operations on the store, one for each line written back) and the words written.

### The rules

Each cached line has a dirty bit.

- **Write hit:** change the word in the cached line and set its dirty bit. The store does not change.
- **Write miss, write-allocate:** fetch the line from the store, evict a victim if the cache is full, change the word in the cache and set the dirty bit.
- **Write miss, no-write-allocate:** write the word to the store only, as [write-around](/write-around/) does.
- **Eviction:** if the victim is dirty, write the whole line to the store and clear the bit; a clean victim is dropped.
- **Flush:** write every dirty line to the store and clear the bits.

Hennessy and Patterson give write-back with write-allocate as the usual pair: after the first write miss brings the line in, the next writes to it are hits and cost no store traffic at all.

### The dirty-bit invariant

**Claim.** After each request, every clean cached line equals the store line. *Proof by induction.* It holds for the empty cache. A read miss copies a line from the store and leaves it clean. A write hit or an allocating write changes a cached line and sets its bit, so the line leaves the set of clean lines. A non-allocating write changes the store at a line that is not cached. A write-back copies the line to the store and only then clears the bit, so the line equals the store when it becomes clean. An eviction removes a line. No step makes a line clean without making it equal to the store. $\square$

So the dirty lines are exactly the places where the store can be behind. A read returns the right value because a hit reads the cache, which holds every write to the line since it was fetched, and a miss reads the store at a line that is not cached, so the store has all writes to it.

### Never more store writes than write-through

**Claim.** For any request sequence, any $k$, $B$, replacement policy and write-miss rule, a write-back cache that flushes at the end makes at most $w$ store writes, and a [write-through](/write-through/) cache makes exactly $w$.

*Proof.* Map each store write of the write-back cache to a write request. A non-allocating write miss maps to itself. A write-back of line $x$ at time $t$ maps to the last write request to $x$ before $t$. Line $x$ was dirty at $t$, so it stayed in the cache since the request $r_0$ that last set its bit (an eviction would have cleared the bit), and every write to $x$ after $r_0$ was a hit. So the image is $r_0$ or a later write hit, and in both cases it is not a non-allocating miss. Two write-backs of $x$ at times $t_1 < t_2$ cannot have the same image: the first clears the bit, so a write to $x$ after $t_1$ sets it again before $t_2$, and the image of $t_2$ comes after $t_1$, while the image of $t_1$ comes before $t_1$. So the map is one-to-one, and the number of store writes is at most $w$. $\square$

The bound is in store write operations. In words the comparison can go the other way: a write-back moves a whole line of $B$ words, so a program that writes one word in each of many lines makes write-back move $B$ times as many words as write-through. Caches that care keep a dirty bit per word or per sector.

Two more facts follow from the rules. The dirty bit does not change which lines are cached, so with the same write-miss rule and a replacement policy that sees only the requests (LRU, FIFO), write-back and write-through have the same hits, the same line reads and the same cache contents at every step; only the store writes differ. And a read miss that evicts a dirty victim costs a line write and a line read, which is why processors put the victim into a write buffer and serve the read first.

### What a crash loses

If the cache loses its contents, the store keeps every write except those in the dirty lines: the lost updates are exactly the dirty lines whose contents differ from the store. All other completed writes are safe. A system that must not lose acknowledged writes has three options: write through, keep the cache in memory that survives power loss, or log each update to stable storage before it acknowledges, as [write-ahead logging](/write-ahead-logging/) does. A database buffer pool is a write-back cache of disk pages, and its rules for when a dirty page may or must reach the disk are the [steal and force policies](/steal-and-force-policies/); [crash recovery](/crash-recovery/) then repairs the store from the log.

### Pitfalls

- **Acknowledged but not durable.** An operating system acknowledges a file write once it is in the write-back page cache. A program that needs the data on disk must ask for it (fsync on Unix), and a crash before that loses the data.
- **Partial order of write-backs.** Dirty lines reach the store in eviction order, not in program order. A store that holds two related values can show the new value of one and the old value of the other after a crash.
- **Read miss latency.** A read miss on a full cache can wait for a dirty eviction. A victim buffer hides most of this.
- **Other readers of the store.** A device or another processor that reads the store directly sees old data in the lines that are dirty in the cache, unless a coherence protocol or an explicit flush handles it.

## Examples

Take $k = 2$ lines, $B = 1$, LRU, write-allocate and an empty start, on $W(a,1)$, $W(a,2)$, $W(a,3)$, $R(a)$, $W(b,5)$, $W(b,6)$, $R(c)$, $W(a,8)$. A star marks a dirty line.

| step | request | result | cache after (LRU first) | store after | line reads | store writes |
|---|---|---|---|---|---|---|
| 1 | $W(a,1)$ | miss | $a^*{=}1$ | $a{=}0$ | 1 | 0 |
| 2 | $W(a,2)$ | hit | $a^*{=}2$ | $a{=}0$ | 1 | 0 |
| 3 | $W(a,3)$ | hit | $a^*{=}3$ | $a{=}0$ | 1 | 0 |
| 4 | $R(a)$ | hit | $a^*{=}3$ | $a{=}0$ | 1 | 0 |
| 5 | $W(b,5)$ | miss | $a^*{=}3$, $b^*{=}5$ | $a{=}0$, $b{=}0$ | 2 | 0 |
| 6 | $W(b,6)$ | hit | $a^*{=}3$, $b^*{=}6$ | $a{=}0$, $b{=}0$ | 2 | 0 |
| 7 | $R(c)$ | miss | $b^*{=}6$, $c{=}0$ | $a{=}3$, $b{=}0$, $c{=}0$ | 3 | 1 |
| 8 | $W(a,8)$ | miss | $c{=}0$, $a^*{=}8$ | $a{=}3$, $b{=}6$, $c{=}0$ | 4 | 2 |

Step 7 evicts the dirty line $a$ and writes $a = 3$; steps 1 to 3 cost one store write together. Step 8 evicts the dirty line $b$. A flush at the end writes $a = 8$, for 3 store writes in total. A write-through cache makes 6 store writes on the same sequence, one for each write. If the cache crashes after step 8 instead, the store holds $a = 3$ and the update $a = 8$ is lost; every other write is in the store. In every row, the clean line $c$ equals the store.

A non-example of a saving: one write $W(3, 1)$ to a cache with $B = 8$ words per line makes write-back move 8 words at the flush, against 1 word for write-through. Both make one store write.

## Where it is used

- **Processor caches.** Most second and last level caches are write-back with write-allocate, because write traffic to memory is expensive; see [multilevel caching](/multilevel-caching/).
- **Operating system page and buffer caches.** File writes go to memory and reach the disk later, in the background or at an explicit sync.
- **Database buffer pools.** Dirty pages stay in memory and the log makes the delay safe, see [write-ahead logging](/write-ahead-logging/) and [checkpointing](/checkpointing/).
- **Write-behind application caches.** A cache in front of a database collects writes and sends them to the database in batches. The saving is the same, and so is the risk: the cache is the only copy until the batch is written.
- **Storage controllers with battery-backed memory,** where the battery removes most of the crash risk.

## References
