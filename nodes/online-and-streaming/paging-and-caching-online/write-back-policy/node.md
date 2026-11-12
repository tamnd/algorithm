---
tag: 4ZNF9D
kind: concept
slug: write-back-policy
name: Write-back and write-through policies
aliases:
- write policy
area: online-and-streaming/paging-and-caching-online
level: intro
summary: 'Rules for when modified cached data is written to the backing store: immediately or on eviction.'
prereqs: [cache, paging-problem]
see_also: [write-back, write-through, write-around, weighted-paging-problem, landlord-algorithm, multilevel-caching, set-associative-cache, memory-hierarchy]
sources:
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: Appendix B, Section B.1 (the four questions of memory hierarchy design, question 4, what happens on a write; write-through, write-back, the dirty bit, write buffers, write allocate and no-write allocate)
  - paper: doi:10.1145/356887.356892
    title: Alan Jay Smith, Cache memories, ACM Computing Surveys 14(3), 1982, 473-530
    locator: the section on the write policy (write-through and copy-back, the memory traffic of each, and write buffers)
  - paper: "Nathan Beckmann, Phillip B. Gibbons, Bernhard Haeupler and Charles McGuffey, Writeback-aware caching, Proceedings of the Symposium on Algorithmic Principles of Computer Systems (APOCS 2020), SIAM, 1-15"
    locator: the model with a writeback cost for dirty items, the factor ω + 1 for writeback-oblivious optimal replacement, the NP-completeness of the offline problem, and Writeback-Aware Landlord with ratio k/(k - h + 1)
  - paper: doi:10.1145/3409964.3461801
    title: Nikhil Bansal, Joseph Naor and Ohad Talmon, Efficient online weighted multi-level paging, Proceedings of SPAA 2021
    locator: the equivalence of writeback-aware caching with read-write paging, an O(k)-competitive deterministic algorithm, and an O(log^2 k)-competitive randomized algorithm
---

A write policy says when a change to data in a cache reaches the slower store behind it. A *write-through* cache sends each write to the backing store at once, so the store is always up to date. A *write-back* cache only marks the cached block as *dirty*, and writes it to the store when the block is evicted. Write-back saves traffic when a block is written many times, and write-through is simpler and keeps the store consistent. In the theory of paging, write-back makes the cost of an eviction depend on whether the page is dirty, which turns plain paging into a weighted problem.

## In plain words

Think of notes copied from a library book into your notebook. When you change a note, you can walk to the library each time and fix the book too. That is write-through. Or you can mark the note as changed and fix the book only when you throw the page of your notebook away. That is write-back.

The first way costs a walk for every change, but the book is never out of date. The second way saves walks when you change the same note many times, but the book is wrong until you go back, and if you lose your notebook first, the change is lost.

## The idea

**Write-through.** On a write hit, the cache updates its copy and also sends the write to the next level. Evictions are free, because the next level already has the data. To keep the processor from waiting for each slow write, a *write buffer* holds pending writes and sends them in the background. The processor stalls only when the buffer is full.

**Write-back.** On a write hit, the cache updates its copy and sets the *dirty bit* of the block. On an eviction, a dirty block is written to the next level and a clean block is dropped. Repeated writes to one block cost one write-back in total. Reads can have to wait, because a miss that evicts a dirty block must first write it out, unless a buffer holds the victim.

**Write misses.** A separate choice says what happens on a write to a block that is not in the cache. With *write allocate*, the block is loaded and then written as on a hit. With *no-write allocate*, also called [write-around](/write-around/), the write goes to the next level and the cache does not change. Write-back caches usually use write allocate, so that later writes to the block hit. Write-through caches often use no-write allocate.

**Costs for each request.** Let a write of a word to the next level cost $u$, a load of a block cost $r$, and a write-back of a block cost $w$. Write-through with no-write allocate pays $u$ for each write and $r$ for each read miss. Write-back with write allocate pays $r$ for each miss of either kind and $w$ for each eviction of a dirty block, plus $w$ for each dirty block that is flushed at the end.

**The competitive view.** In plain [paging](/paging-problem/), every miss costs the same. With write-back, the eviction of a dirty page costs extra, so the cost of a decision depends on the state of the page. Beckmann, Gibbons, Haeupler and McGuffey (2020) study this *writeback-aware caching* problem, where each item has a load cost and a writeback cost $\omega$ when it is dirty. They show:

- The optimal replacement for plain paging, which ignores writebacks, can cost $\omega + 1$ times the optimum of the writeback-aware problem.
- The offline writeback-aware problem is NP-complete, unlike plain paging, where [Belady's rule](/belady-algorithm/) is optimal.
- Writeback-Aware Landlord, a variant of the [Landlord](/landlord-algorithm/) rule that gives dirty items more credit, has competitive ratio $k / (k - h + 1)$ against an optimum with $h \le k$ slots. For $h = k$ this is $k$, which is the best possible for deterministic rules, since plain paging is a special case.

Bansal, Naor and Talmon (2021) show that the problem is equivalent to read-write paging, a two-level form of [weighted paging](/weighted-paging-problem/), and give a randomized $O(\log^2 k)$-competitive algorithm.

The write policy itself is not an online algorithm with a competitive ratio. It fixes the cost model, and the replacement rule is then judged inside that model. Write-through makes every eviction free, so the replacement problem is plain paging for the read misses. Write-back makes the replacement rule matter twice: it decides which misses happen and which evictions cost a write-back.

## Examples

**Memory traffic of one trace.** A cache holds $2$ blocks with LRU replacement. The requests are: write $a$, write $a$, read $b$, write $a$, write $c$, read $b$, write $c$, read $a$. A script counted the traffic for the two usual pairs.

| request | write-through, no-write allocate | write-back, write allocate |
|---|---|---|
| write a | miss, write a to memory | miss, load a, mark a dirty |
| write a | miss, write a to memory | hit |
| read b | miss, load b | miss, load b |
| write a | miss, write a to memory | hit |
| write c | miss, write c to memory | miss, load c, evict b (clean, dropped), mark c dirty |
| read b | hit | miss, load b, evict a (dirty, write back a) |
| write c | miss, write c to memory | hit |
| read a | miss, load a | miss, load a, evict b (clean, dropped) |

Write-through sends $5$ word writes and loads $2$ blocks. Write-back loads $5$ blocks, writes back $1$ block, and still holds $1$ dirty block, $c$, at the end. Which one sends fewer bytes depends on the block size and the number of writes to each block: with $4$ words in a block and the costs above, write-through moves $5 + 2 \cdot 4 = 13$ words, and write-back moves $(5 + 1 + 1) \cdot 4 = 28$ words. With many more writes to $a$ and $c$, write-through grows by one word for each write, while write-back does not grow at all.

**A long run of writes.** A loop writes the same counter $10^6$ times. Write-through sends $10^6$ writes to memory. Write-back sends one write-back, when the block is evicted at last.

**Durability.** A database that writes a log record must know that the record is on disk. A write-back disk cache without power protection can lose it. For this reason, disks and file systems offer a flush command, and some storage uses write-through or a battery-backed cache.

## Where it is used

- **Processor caches.** Most L2 and L3 caches, and many L1 data caches, are write-back, to save bandwidth to the next level. Some L1 caches are write-through to a write-back L2, which makes the L1 simpler and keeps one up-to-date copy in the L2. The systems pages on [write-back](/write-back/) and [write-through](/write-through/) caching give more detail.
- **Coherence.** In a multiprocessor, a dirty block is the only up-to-date copy, so coherence protocols such as MESI track the dirty state and supply the block from the cache that owns it.
- **Operating systems.** The page cache of an operating system is write-back: modified pages are written to disk later, by a background thread or when memory is needed. The dirty bit in each page table entry lets the system skip the write for clean pages.
- **Storage and databases.** Disk controllers, SSDs and database buffer pools use write-back caches with logs or batteries for durability. A database buffer pool writes a dirty page only after its log records are on disk.
- **Distributed caches.** In front of a database, a write-through cache updates both the cache and the database on each write, and a write-behind cache queues the database writes. See also [multilevel caching](/multilevel-caching/).

## References
