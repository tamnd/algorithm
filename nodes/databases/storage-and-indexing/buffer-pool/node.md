---
tag: GQQFSE
kind: data-structure
slug: buffer-pool
name: Buffer pool
aliases:
- buffer manager
- database buffer cache
area: databases/storage-and-indexing
level: intro
summary: "A fixed set of memory frames that cache disk pages, with a page table, pin counts, dirty bits and a replacement policy that picks a victim among the unpinned frames."
model: external-memory-model
complexity:
  vars: {B: the number of frames (buffer pages), n: the number of page requests}
  time: {worst: "O(n B)"}
  io: {worst: "2n"}
  space: {extra: "O(B)"}
prereqs: [hash-table, lru]
see_also: [dbmin, lru, lru-k, clock, two-q, steal-and-force-policies, write-ahead-logging, five-minute-rule]
sources:
  - paper: "Wolfgang Effelsberg and Theo Haerder, Principles of database buffer management, ACM Transactions on Database Systems 9(4), 1984, 560 to 595"
    title: Principles of database buffer management
    locator: buffer search, the allocation of frames to transactions, and the replacement algorithms
  - paper: "Joseph M. Hellerstein, Michael Stonebraker and James Hamilton, Architecture of a database system, Foundations and Trends in Databases 1(2), 2007, 141 to 259"
    title: Architecture of a database system
    locator: the section on storage management and its part on buffer management
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: "Chapter 9 (storing data: disks and files), the section on the buffer manager: pin counts, dirty bits and replacement policies"
  - paper: "Michael Stonebraker, Operating system support for database management, Communications of the ACM 24(7), 1981, 412 to 418"
    title: Operating system support for database management
    locator: the section on buffer pool management
  - paper: "Elizabeth J. O'Neil, Patrick E. O'Neil and Gerhard Weikum, The LRU-K page replacement algorithm for database disk buffering, Proceedings of ACM SIGMOD 1993, 297 to 306"
    title: The LRU-K page replacement algorithm for database disk buffering
    locator: the definition of LRU-K and the argument against plain LRU for mixed workloads
  - paper: "Hong-Tai Chou and David J. DeWitt, An evaluation of buffer management strategies for relational database systems, Proceedings of VLDB 1985, 127 to 141"
    title: An evaluation of buffer management strategies for relational database systems
    locator: the reference patterns of relational queries and the simulation of replacement algorithms
---

A buffer pool is the part of main memory where a database system keeps copies of disk pages. It has a fixed number $B$ of *frames*, each the size of one page. A *page table* maps the id of each page in memory to its frame. Each frame has a *pin count*, the number of callers that use the page now, and a *dirty bit*, set when the copy in memory differs from the copy on disk. When a requested page is not in the pool, a *replacement policy* such as [LRU](/lru/) or [CLOCK](/clock/) picks a victim among the frames with pin count zero; a dirty victim is written back first. The component that does all this is the buffer manager. [DBMIN](/dbmin/) is one policy for this pool: it gives each open file of a query its own set of frames and its own policy, and this page is about the pool and the general policies.

## In plain words

The disk is slow and memory is small. The buffer pool is a shelf in memory with room for a fixed number of pages. When some part of the database needs a page, it asks the pool. If the page is on the shelf, it gets it at once. If not, the pool reads it from disk and puts it on the shelf, and when the shelf is full it first takes a page off.

Two rules keep this safe. A page that someone is using now is pinned, and the pool never takes a pinned page off. A page that someone changed is marked dirty, and the pool writes it back to disk before it drops it.

Which unpinned page to drop is a choice. A common choice is the page that was used the longest time ago.

## The abstract type

The pool serves the rest of the system with four calls.

- `fetch(p)`: make page $p$ present in a frame, increase its pin count, and return the frame. Fail if $p$ is absent and all frames are pinned.
- `unpin(p, d)`: decrease the pin count of $p$; if $d$ is true, the caller changed the page, so set its dirty bit.
- `new_page()`: allocate a page on disk and fetch it without a read.
- `flush(p)`: write $p$ to disk if it is dirty, and clear its dirty bit.

A caller must unpin every page it fetched, once per fetch. The guarantee is that while a page is pinned, its frame does not change, and that every change a caller makes and reports reaches the disk before the frame is reused.

## Representation

- An array of $B$ frames. A frame holds a page id (or nothing), the bytes of the page, a pin count, a dirty bit, and whatever the policy needs: a time of last use for LRU, a reference bit for CLOCK, the times of the last $K$ uses for [LRU-K](/lru-k/).
- A page table, a [hash table](/hash-table/) from page id to frame number, for the pages now in the pool.
- The state of the policy: a list in order of last use for LRU, a clock hand for CLOCK, queues for [2Q](/two-q/).

The invariant is that the page table and the frames agree: $table[p] = f$ if and only if frame $f$ holds page $p$, each page is in at most one frame, and a frame with a page whose dirty bit is clear holds the same bytes as the disk.

## Operations

```pseudo id=main
FETCH(p)
L1  if p is in the page table then
L2      f ← table[p]; pin(f) ← pin(f) + 1; record a use of f
L3      return f
L4  if a frame f is free then use it
L5  else
L6      f ← VICTIM(), a frame with pin(f) = 0
L7      if there is none then fail: all frames are pinned
L8      if dirty(f) then write page(f) to disk
L9      remove page(f) from the page table
L10 read p from disk into f
L11 page(f) ← p; pin(f) ← 1; dirty(f) ← false; table[p] ← f
L12 record a use of f; return f

UNPIN(p, d)
L13 f ← table[p]; pin(f) ← pin(f) - 1
L14 dirty(f) ← dirty(f) or d

VICTIM() for CLOCK                        ▷ called only if some frame has pin 0
L15 loop
L16     f ← the frame at the hand; move the hand to the next frame
L17     if pin(f) = 0 then
L18         if ref(f) then ref(f) ← false
L19         else return f
```

A use of a frame sets its reference bit for CLOCK, and moves it to the most recent end of the list for LRU. VICTIM for LRU returns the unpinned frame with the oldest last use.

## Example

Take $B = 3$ frames and the requests 1 2 3 1 4 1 2 5 1 2, each fetched and unpinned at once, so no frame is pinned when a victim is chosen.

| request | 1 | 2 | 3 | 1 | 4 | 1 | 2 | 5 | 1 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|
| LRU | miss | miss | miss | hit | miss, drop 2 | hit | miss, drop 3 | miss, drop 4 | hit | hit |
| CLOCK | miss | miss | miss | hit | miss, drop 1 | miss, drop 2 | miss, drop 3 | miss, drop 4 | hit | hit |

LRU has 6 misses. When 4 arrives, the order of last use is 2, 3, 1, so 2 goes. CLOCK has 7 misses. When 4 arrives, all three reference bits are set, so the hand goes once around the frames, clears each bit, and comes back to frame 0, which holds page 1: CLOCK drops page 1 although it was used one request before. This is the cost of a single bit: CLOCK forgets the order of uses inside one turn of the hand. Both end with pages 1, 2 and 5 in the pool.

A loop over 5 pages with $B = 4$ frames misses on every request with LRU, because the page that comes next is always the one that was used longest ago. This *sequential flooding* is the classic case where the order of last use is the wrong guide for a database. A policy that drops the most recently used page, [MRU](/mru/), keeps 3 of the 4 frames useful on each pass, which is what DBMIN gives a looping scan.

## Correctness

The page table and the frames change together at lines L9 and L11, so they keep agreeing. A frame is reused only at line L6, and VICTIM returns only a frame with pin count zero, so a pinned page never leaves its frame. For CLOCK, the loop ends: some frame has pin count zero, and the first time the hand passes it, it either returns it or clears its bit, so it returns it at the latest on the next turn. A dirty bit is set at line L14 whenever a caller reports a change, and is cleared only at line L11 after a read or by `flush` after a write, and line L8 writes a dirty victim before its frame is reused. So no reported change is lost. The full proof is below.

## Complexity

The page I/O is counted in the [external memory model](/external-memory-model/) with pages as blocks. In the external memory model, the memory holds M/B blocks; this is the number of buffer pages B of this page. A request that hits costs no I/O. A miss costs one read, plus one write when the victim is dirty, so $n$ requests cost at most $2n$ I/Os, and the number of reads is the number of misses. The cost does not separate sequential and random I/O; a pool that reads ahead for scans turns many random reads into a few large sequential ones.

The CPU work per request is a hash lookup in the page table, $O(1)$ expected, plus the work of the policy on a miss.

- LRU with a doubly linked list of the unpinned frames: $O(1)$ per request. The sample code finds the oldest frame by a scan, $O(B)$ per miss.
- CLOCK: at most $2B$ steps of the hand per victim, since one turn clears every bit of an unpinned frame. If no frame is ever pinned during a victim search, the total number of steps over $n$ requests is at most $n + m$ for $m$ misses: each step either clears a bit that an earlier request set, or ends at a victim. Pinned frames add steps that the hand passes over.

The number of misses depends on the policy and the workload, and there is no best policy for all workloads. For the [paging problem](/paging-problem/) with $B$ frames, the optimal offline policy, [Belady's algorithm](/belady-algorithm/), drops the page whose next use is farthest away, and LRU makes at most $B$ times as many misses as it on any sequence, up to an additive constant (Sleator and Tarjan 1985). Database policies are judged by measurement on workloads, not by such bounds.

## Variants

- **LRU-K.** O'Neil, O'Neil and Weikum (1993) drop the page whose $K$-th most recent use is the oldest. With $K = 2$, a page used once by a scan has no second use and goes first, so scans do not flush the pages that are used often. See [LRU-K](/lru-k/).
- **2Q.** Johnson and Shasha (1994) get much of the effect of LRU-2 at the cost of LRU: new pages enter a FIFO queue and move to the main LRU queue only on a second use. See [2Q](/two-q/).
- **CLOCK with counts.** PostgreSQL uses a clock sweep in which each buffer has a usage count up to 5 instead of one bit. The hand decreases the count and takes a buffer only when its count is zero.
- **Rings for scans.** A large sequential scan, a bulk write or a vacuum in PostgreSQL uses a small ring of buffers of its own, so that it does not push the rest of the pool out.
- **Per query allocation.** DBMIN gives each file that a query opens a locality set of frames and a policy that fits its access pattern, and admits a query only if its sets fit in the pool. See [DBMIN](/dbmin/).
- **Hints and priorities.** Some systems let the query layer mark pages as likely to be reused, such as the root and the inner nodes of a [B+ tree](/b-plus-tree/), or as used once.
- **Adaptive policies.** [CLOCK-Pro](/clock-pro/) and [CAR](/car/) adapt between recency and frequency.

## When to use it

Every disk-based database system has a buffer pool. The choices are the policy and the size. Use CLOCK or one of its variants when the cost per request must be small and there are many concurrent threads, since a hit only sets a bit and takes no lock on a shared list. Use LRU-K or 2Q when scans and point lookups mix, so that scans do not flush the hot pages. Give scans a ring or an MRU set of their own. The [five-minute rule](/five-minute-rule/) is a guide for the size: a page that is used more often than once per break-even interval should stay in memory.

## Pitfalls

- **A missing unpin.** A caller that forgets an unpin leaves the page pinned forever, and the pool loses one frame. With enough of them, every fetch fails. Tie each pin to a scope that ends it.
- **Pins and latches.** A pin keeps the page in its frame. It does not stop another thread from reading a page that is being changed. Changes need a latch on the page as well, and the pin count must not be used as a lock.
- **Write-ahead logging.** With [write-ahead logging](/write-ahead-logging/), a dirty page must not reach the disk before the log records that describe its changes. Before line L8 writes a dirty page, the pool must force the log up to the log sequence number of the page. Whether dirty pages of uncommitted transactions may be written at all is the steal policy; see [steal and force policies](/steal-and-force-policies/).
- **Double buffering.** If the operating system also caches the file, each page can be in memory twice. Database systems often open their files with direct I/O, which also gives them control over the order of writes. Stonebraker (1981) described these problems with the file systems of that time.
- **Sequential flooding.** Plain LRU with a scan larger than the pool misses on every request of the scan, and pushes out all other pages. Use a ring for scans, MRU for loops, or LRU-K.
- **The page table under concurrency.** One lock on the whole page table is a bottleneck. Systems split the table into partitions, each with its own lock.

## Implementations

## History

Effelsberg and Haerder (1984) gave the first full account of database buffer management: how to find a page in the pool, how to share frames among transactions, and how replacement policies compare. Stonebraker (1981) argued that the buffer caches of operating systems do not serve databases well, because their LRU ignores the known access patterns of queries. Sacco and Schkolnick (1982) proposed the hot set model, and Chou and DeWitt (1985) the query locality set model with the DBMIN algorithm, both based on those access patterns. O'Neil, O'Neil and Weikum (1993) gave LRU-K, and Johnson and Shasha (1994) gave 2Q. Hellerstein, Stonebraker and Hamilton (2007) describe the buffer pool as it exists in current systems.

## References
