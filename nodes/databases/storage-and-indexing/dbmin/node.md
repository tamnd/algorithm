---
tag: DPJZ9M
kind: algorithm
slug: dbmin
name: DBMIN buffer management
aliases:
- query locality set model
- DBMIN
area: databases/storage-and-indexing
level: advanced
summary: "Chou and DeWitt's buffer policy: each file a query opens gets its own locality set of frames, sized and replaced by its reference pattern, and a query starts only if all sets fit."
model: external-memory-model
complexity:
  vars: {B: the number of frames in the pool, n: the number of page requests, f: the number of open file instances}
  time: {worst: "O(n + f)", average: "O(n + f)"}
  io: {worst: "n"}
  space: {extra: "O(B + f)"}
properties: {deterministic: true, exact: false, external: true, online: true, in_place: false, recursive: false}
history:
  year: 1985
  people: [Hong-Tai Chou, David J. DeWitt]
  note: "Chou and DeWitt defined the query locality set model and DBMIN, and compared DBMIN by simulation with RAND, FIFO, CLOCK, the working set algorithm and the hot set algorithm."
prereqs: [buffer-pool, lru, mru]
see_also: [buffer-pool, lru, mru, lru-k, clock, two-q, working-set-model, iterator-model]
sources:
  - paper: "Hong-Tai Chou and David J. DeWitt, An evaluation of buffer management strategies for relational database systems, Proceedings of VLDB 1985, Stockholm, 127 to 141"
    title: An evaluation of buffer management strategies for relational database systems
    locator: "the query locality set model and its reference patterns, the DBMIN algorithm with its three cases and its load controller (pp. 130 to 132), and the simulation results"
  - paper: "Giovanni Maria Sacco and Mario Schkolnick, A mechanism for managing the buffer pool in a relational database system using the hot set model, Proceedings of VLDB 1982"
    title: A mechanism for managing the buffer pool in a relational database system using the hot set model
    locator: the hot set model, the predecessor that DBMIN refines
  - paper: "Wolfgang Effelsberg and Theo Haerder, Principles of database buffer management, ACM Transactions on Database Systems 9(4), 1984, 560 to 595"
    title: Principles of database buffer management
    locator: the survey of buffer allocation and replacement that the DBMIN paper builds on
  - paper: "S. Bing Yao, Approximating block accesses in database organizations, Communications of the ACM 20(4), 1977, 260 to 261"
    title: Approximating block accesses in database organizations
    locator: the formula for the expected number of pages touched by k random record accesses
---

DBMIN is a buffer management algorithm of Chou and DeWitt (1985) for relational database systems. It rests on the *query locality set model* (QLSM): the query plan already tells how each operator will read each file, for example a sequential scan, a scan that loops over the inner relation of a join, or random lookups through an index. DBMIN gives each *file instance*, one file opened by one query, its own *locality set* of frames, with a size and a local replacement policy chosen for its reference pattern. A load controller starts a query only if the locality sets of all running queries fit in the pool. A general [buffer pool](/buffer-pool/) with one global policy such as [LRU](/lru/) or [CLOCK](/clock/) treats all pages alike; DBMIN uses the plan to give each access the few frames it needs and to keep one query from taking the frames of another.

## In plain words

A database knows its future page requests better than an operating system does. When a query scans a table once, one frame is enough. When a join reads the inner table again and again in a loop, it pays to keep as much of that table as possible, and the best page to give up is the one just read, because it will be needed last. For repeated index lookups, keep the top of the index.

DBMIN gives each opened file its own small set of frames, sized for its pattern, with a rule that fits the pattern. Pages that belong to no set go to a common free list, and any query that needs one of those pages can take it back without a disk read. A new query waits until there are enough free frames for all of its sets.

## The problem

A pool of $B$ frames serves several queries at once. Each query opens files; the same file opened by two queries is two file instances. Each request names a file instance and a page. The goal is high throughput: few disk reads per query, and no *thrashing*, in which concurrent queries keep taking each other's frames so that all of them run slowly. Chou and DeWitt write $N$ for the number of frames; this page writes $B$, as in the rest of the area.

**The reference patterns of the QLSM.** Each pattern comes with the size of a locality set and a local policy.

| pattern | example | locality set size | local policy |
|---|---|---|---|
| straight sequential (SS) | a selection that scans an unordered relation once | 1 | any |
| clustered sequential (CS) | the inner input of a merge join, which backs up over the records with the same key | records of the largest cluster divided by records per page | FIFO or LRU |
| looping sequential (LS) | the inner relation of a nested loops join | the whole file if it fits | MRU if it does not fit |
| independent random (IR) | data pages read through a non-clustered index | 1 or $b$ (below) | any |
| clustered random (CR) | an inner relation read through a non-clustered, non-unique index, for an outer relation clustered on non-unique keys | about the number of records in the largest cluster | as for CS |
| straight hierarchical (SH), and H/SS | one traversal of an index, alone or followed by a scan of the leaves | 1 | any |
| hierarchical with clustered sequential (H/CS) | a traversal followed by a clustered scan of the leaves | as for CS, counting key and pointer pairs | as for CS |
| looping hierarchical (LH) | repeated traversals of an index on the join field of the inner relation | the upper levels of the tree (below) | LIFO with 3 to 4 buffers keeps the root |

For independent random access, $b$ is the expected number of distinct pages that $k$ random record accesses touch, from Yao's formula: for $n$ records on $m$ pages, $b = m \left(1 - \prod_{i=1}^{k} \frac{n(1 - 1/m) - i + 1}{n - i + 1}\right)$. The paper calls $(k - b)/b$ the *residual value* of a page, and the set has size 1 if it is at most a threshold $\beta$ and size $b$ otherwise. For looping hierarchical access, let $b_i$ be the number of pages of level $i$ of the tree (the root is level 0) that $k$ traversals touch, again by Yao's formula; the size is about $(1 + b_1 + \cdots + b_j) + 1$, where $j$ is the deepest level whose residual value $(k - b_i)/b_i$ is above $\beta$. Since the fan-out of an index is large, the root is often the only page worth keeping. For independent random access, the paper notes that all replacement algorithms do about equally well.

## The algorithm

The state is a global table of all pages in memory, a global free list, and one locality set per file instance. Each locality set $L$ has a bound $l(L)$ and a size $r(L) \le l(L)$. A page is owned by at most one locality set; a page that no set owns is on the free list, which also holds the empty frames.

```pseudo id=main
REQUEST(L, p)                              ▷ file instance with locality set L asks for page p
L1  if p is in the global table then
L2      if owner(p) = L then
L3          update the statistics of the policy of L for p; return
L4      if owner(p) is another locality set then
L5          return p                       ▷ shared: p stays in the other set
L6      remove p from the free list        ▷ p is in memory with no owner
L7  else
L8      f ← the frame at the head of the free list; drop its page from the global table
L9      read p into f
L10 if r(L) = l(L) then
L11     q ← the victim of the policy of L; owner(q) ← none; append q to the free list
L12     r(L) ← r(L) - 1
L13 owner(p) ← L; add p to L; r(L) ← r(L) + 1

START(Q)                                   ▷ Q opens file instances with bounds l_1, ..., l_k
L14 if the bounds of all active sets plus l_1 + ... + l_k < B then
L15     activate Q with an empty locality set (r = 0) for each file instance
L16 else put Q at the end of the waiting queue

FINISH(Q)
L17 for each locality set of Q, put its pages on the free list with no owner
L18 while the first waiting query passes the test of line L14 do
L19     activate it, as at line L15
```

Lines L1 to L3 are the first case of the paper, a page found in its own locality set. Lines L4 to L6 and L10 to L13 are the second case, a page in memory but not in the set: if another set owns it, the requester just uses it; otherwise it joins the set, and if the set is then over its bound, the local policy gives a page back to the free list. Lines L7 to L9 are the third case, a page not in memory, which is read into a frame from the free list and then treated as in the second case. In the paper the usage statistics of the new page are updated after the release, so the local policy chooses among the pages that were in the set before; the implementation picks the victim before it adds the new page, which is the same choice, and MRU gives up the page used just before, not the new one. The paper notes that the local policies cause no swapping of their own; disk reads and writes come only from the global table and the free list, here line L9.

The load controller runs when a file is opened or closed. The paper places a suspended query at the front of the waiting queue and, on a close, activates the first waiting query if the condition still holds. The sample code admits a whole query at a time, appends a suspended query at the end of the queue, and also queues a new query when others are already waiting, so that small queries cannot pass a large one forever.

## Example

**A looping scan.** One query loops three times over a file of 6 pages, 0 to 5, with a locality set of $l = 3$ and $B = 4$ frames. There are 18 requests.

| pass | MRU: misses | MRU: hits | LRU: misses |
|---|---|---|---|
| 1 | 0 1 2 3 4 5 | none | 0 1 2 3 4 5 |
| 2 | 2 3 4 | 0 1 5 | all 6 |
| 3 | 1 2 3 | 0 4 5 | all 6 |
| total | 12 | 6 | 18 |

With MRU, the first pass ends with pages 0, 1 and 5 in the set: each miss on pages 3, 4 and 5 gave up the page read just before it. In pass 2, pages 0 and 1 hit. The miss on page 2 gives up page 1, the miss on 3 gives up 2, the miss on 4 gives up 3, and page 5 hits. With LRU, the page that is needed next is always the one that left the set, so every request misses, and the free list holds only one frame, which does not help.

**Load control.** Take $B = 10$. Query $Q_1$ scans $R$ once (SS, size 1) and loops over $S$ (LS, size 6), so it needs 7 frames, and $7 < 10$ admits it. Query $Q_2$ needs one set of 3 frames; $7 + 3 = 10$ is not less than 10, so it waits. Query $Q_3$ needs 1 frame; it waits behind $Q_2$. When $Q_1$ finishes, its 7 pages go to the free list with no owner, and $Q_2$ (needs 3) and then $Q_3$ (total 4) start. If $Q_2$ asks for a page of $S$ that $Q_1$ had read, it finds it on the free list without a disk read.

## Correctness

DBMIN is a heuristic, and its claims are of two kinds. The first are invariants. A page is in at most one locality set, each set has at most $l$ pages, and the load controller keeps the sum of the bounds below $B$. So the sets hold fewer than $B$ frames together, and the free list is never empty when line L8 needs a frame. A set changes only on requests of its own file instance, so one query cannot take frames from another: the sets of running queries are isolated, which is how DBMIN avoids thrashing. Without sharing, each set holds exactly what a separate cache of $l$ pages with the same policy would hold, and the free list can only save reads.

The second kind is the analysis of a pattern. For a loop over $L > l \ge 2$ pages with MRU, every pass after the first has at least $l - 1$ hits, while LRU with the same $l$ frames has none. The full proof is below. That the sizes and policies of the table are good choices is shown by measurement, not proved.

## Complexity

The I/O is counted in the [external memory model](/external-memory-model/) with pages as blocks. In the external memory model, the memory holds M/B blocks; this is the number of buffer pages B of this page. Each request causes at most one disk read, at line L9, so $n$ requests cost at most $n$ reads; this page and the paper treat only reads. The number of reads is at most the sum, over the locality sets, of the misses of a separate cache of $l$ pages with the same policy.

The CPU work per request is $O(1)$ expected with a hash table for the global table, a doubly linked list for the free list, and a doubly linked list per locality set for LRU, MRU and FIFO. START and FINISH cost $O(f)$ for $f$ file instances, if the sum of the bounds is kept as a running total, plus the pages that FINISH gives back. The sample code removes a page from the free list by a linear search, $O(B)$.

## Properties

- **Isolation.** A query's locality sets change only through its own requests. A new query cannot slow down a running one by taking its frames, since it only starts if its sets fit.
- **Sharing without ownership.** Two queries that read the same page share one frame. The page counts against the set that owns it, and the other query just uses it.
- **Cheap reuse.** Pages given back by a set or by a finished query stay in memory on the free list until their frame is needed, so a later request finds them without a read.
- **Admission, not preemption.** The load controller delays queries and never takes frames away from a running one. A query whose sets are too big for the pool never starts, so the bounds must be at most $B - 1$ in total.

## Variants and improvements

- **Hot set model.** Sacco and Schkolnick (1982) estimate for each query a *hot set*, the number of frames below which its page faults rise sharply, and run a query only if its hot set fits. The hot set is one number per query, and the replacement inside it is LRU. DBMIN makes the estimate per file instance and picks the policy per pattern.
- **Marginal gains.** Later work on flexible buffer allocation gives each additional frame to the query where one more frame saves the most reads, instead of a fixed set size per pattern.
- **General purpose policies.** [LRU-K](/lru-k/) and [2Q](/two-q/) get part of the benefit of DBMIN without hints from the plan: a page read once by a scan does not push out the hot pages.
- **Rings for scans.** Systems such as PostgreSQL give a large sequential scan a small ring of frames, which is the SS rule of DBMIN.

## When to use it

Use the ideas of DBMIN when the access pattern of each operator is known from the plan, as in a [Volcano style iterator](/iterator-model/) engine, and many queries share one pool: give scans one frame or a small ring, give looped inner relations MRU or the whole file, keep the upper levels of indexes, and control the admission of queries by their memory needs. Most systems do not implement DBMIN as a whole. They use a global policy such as CLOCK or LRU-K, and add the rules for scans and indexes as hints.

## Pitfalls

- **Wrong patterns.** The sizes come from the plan. If the optimizer misestimates a cluster size or the number of random lookups, the set is too small or too big. A set that is too small for a loop turns the loop into a stream of misses.
- **MRU outside loops.** MRU is right for a loop that does not fit. For any other pattern it gives up exactly the page with the most recent use, which is often the next one needed.
- **Admission deadlock.** A query whose total bound is at least $B$ waits forever. Cap each bound, or reduce the set of a looping scan to fit.
- **Shared pages.** The page used by a second query stays in the set of its owner. If the owner gives it up, it goes to the free list and can be dropped while the second query still uses it often; that query's next request then takes it into its own set.
- **Writes.** The paper studies a read-only setting. With updates, a victim must be written before its frame is reused, and the write-ahead rule of the [buffer pool](/buffer-pool/) applies.

## Implementations

## History

Effelsberg and Haerder (1984) surveyed database buffer management and the use of access patterns. Sacco and Schkolnick (1982) proposed the hot set model. Chou and DeWitt (1985) defined the query locality set model and DBMIN, and evaluated it with a simulation that combined real traces and distributions, with a CPU model of a VAX-11/750 and the WiSS storage system, on six query types over relations of Wisconsin benchmark style with 182-byte tuples. With 1 to 32 concurrent queries, the simple policies (RAND, FIFO, CLOCK) thrashed as the load grew, and DBMIN had 7 to 13% more throughput than the hot set algorithm.

## References
