---
tag: T0A3TV
kind: data-structure
slug: log-structured-merge-tree
name: Log-structured merge tree
aliases:
- LSM tree
area: data-structures/external-memory-structures
level: advanced
summary: Buffers writes in memory and merges sorted runs on disk, trading read cost for high write throughput.
implements: [dictionary, ordered-set]
model: external-memory-model
prereqs: [external-memory-model, k-way-merge, binary-search]
see_also: [b-epsilon-tree, write-optimized-structure, bloom-filter, b-plus-tree, buffer-tree, log-compaction, compaction, external-merge-sort]
sources:
  - paper: "Patrick O'Neil, Edward Cheng, Dieter Gawlick and Elizabeth O'Neil, The log-structured merge-tree (LSM-tree), Acta Informatica 33(4) (1996)"
    locator: pp. 351 to 385 (the components C0 to Ck, the rolling merge, and the cost analysis against B-trees)
  - paper: "Chen Luo and Michael J. Carey, LSM-based storage techniques: a survey, The VLDB Journal 29(1) (2020)"
    locator: pp. 393 to 418, Section 2 (leveling and tiering, the costs of writes, point lookups and range queries, Bloom filters and fence pointers)
  - paper: "Niv Dayan, Manos Athanassoulis and Stratos Idreos, Monkey: optimal navigable key-value store, Proceedings of the ACM SIGMOD International Conference on Management of Data (2017)"
    locator: pp. 79 to 94 (the cost model of leveled and tiered LSM trees and the tuning of Bloom filters per level)
---

A log-structured merge tree, or LSM tree, is a dictionary for disks and flash that never updates data in place. New writes go into a small sorted table in memory, the *memtable*. When it is full, it is written out as a sorted *run*, and runs are merged with older runs in long sequential passes, as in [external merge sort](/external-merge-sort/). The runs form *levels* whose sizes grow by a factor $T$, so there are about $\log_T(N/C_0)$ levels, where $C_0$ is the size of the memtable. A delete writes a *tombstone*, a marker that hides older entries of the key. In the leveled form of this page, an insert costs $O\big(\frac{T}{B}\log_T\frac{N}{C_0}\big)$ amortized I/Os, far below the one random write per insert of a [B-tree](/b-tree/), and a lookup costs one block read per level, or about one in total with [Bloom filters](/bloom-filter/). O'Neil and others introduced it in 1996. It is the storage engine of Bigtable, LevelDB, RocksDB, Cassandra, HBase and many other key-value stores.

## In plain words

Imagine a notebook on your desk and a shelf of binders. You write every new fact in the notebook, in sorted order. When the notebook is full, you do not file each fact in its binder. You put the whole notebook on the shelf as a new sorted volume. When there are too many small volumes, you merge them into one big sorted volume, in one long sweep.

To look something up, you check the notebook first, then the newest volume, then older ones. The first entry you find is the newest one. A crossed-out entry means the fact was deleted.

## The abstract type

A [dictionary](/dictionary/) that is also an [ordered set](/ordered-set/):

- `put(k, v)` sets the value of $k$.
- `delete(k)` removes $k$.
- `get(k)` returns the value of $k$ or "absent".
- `range(a, b)` returns the pairs with $a \le k \le b$ in key order.

## Representation

There are three parameters: the block size $B$, the memtable size $C_0$, and the size ratio $T \ge 2$.

- The **memtable** in memory holds fewer than $C_0$ entries. An entry is a key with a value, or with a tombstone.
- **Level** $i \ge 1$ on disk holds one sorted run of at most $C_0 T^i$ entries with distinct keys, stored in consecutive blocks.
- For each run, memory holds the first key of each block, the *fence keys*, so that a lookup reads one block per run. Real systems also keep a [Bloom filter](/bloom-filter/) per run.

**Invariants.**

- **(M1)** Each run is sorted with distinct keys and has at most its capacity.
- **(M2)** For each key, the entries in the memtable, in level 1, in level 2, and so on are from newer to older updates.
- **(M3)** The deepest nonempty level holds no tombstones.

By (M2), the state of a key is given by its first entry in the order memtable, level 1, level 2, and so on.

## Operations

```pseudo id=main
UPDATE(T, k, x)                   ▷ x is a value, or a tombstone for a delete
L1  T.mem[k] ← x                   ▷ replaces an older entry of k in the memtable
L2  if |T.mem| = C0 then FLUSH(T)

FLUSH(T)
L3  R ← the entries of T.mem in key order; T.mem ← empty; i ← 1
L4  loop
L5      R ← MERGE(R, level i), the entry of R winning on equal keys; drop tombstones if all levels below i are empty
L6      if |R| ≤ C0·T^i then level i ← R; return
L7      level i ← empty; i ← i + 1       ▷ the merged run is too big: carry it to the next level

GET(T, k)
L8  if k is in T.mem then return its value, or "absent" for a tombstone
L9  for i ← 1, 2, … do                ▷ newest level first
L10     if level i has an entry on k then return its value, or "absent" for a tombstone   ▷ one block, found by the fence keys
L11 return "absent"
```

MERGE is the two-way merge of two sorted runs, read and written in sequential blocks; see [k-way merge](/k-way-merge/). A range query reads the part of each run that falls in the range and merges them, newest entry first. Real LSM trees run merges in the background, in pieces, so that no single write waits for a large merge; this is called *compaction*, see [compaction](/compaction/).

## Example

Take $B = 2$, $C_0 = 2$ and $T = 2$, so level 1 holds up to 4 entries, level 2 up to 8. A tombstone of $k$ is written $-k$.

1. Put 50, 20: the memtable is full, and FLUSH writes the run $[20\ 50]$ to level 1. Put 80, 10: the run $[10\ 80]$ is merged with level 1 into $[10\ 20\ 50\ 80]$, 4 entries, which fits.
2. Put 60, delete 20. The run $[-20\ 60]$ is merged into level 1. Level 1 is the last level, so the tombstone and 20 both vanish: $[10\ 50\ 60\ 80]$.
3. Put 30, 70. Merged with level 1, the run has 6 entries, more than 4, so level 1 becomes empty and the merge goes on into level 2: level 2 is $[10\ 30\ 50\ 60\ 70\ 80]$.
4. Put 40, delete 80, put 90, 25. Level 1 is now $[25\ 40\ -80\ 90]$ and level 2 is unchanged. The tombstone stays, because level 2 below still has 80.
5. `get(80)` finds $-80$ in level 1 and returns "absent", without reading level 2. `get(60)` misses in level 1, with one block read, and finds 60 in level 2. `range(20, 60)` merges both levels and returns 25, 30, 40, 50, 60.

The 12 updates made 20 block transfers in the count of the code, all of them in sequential runs.

## Correctness

By (M2), the first entry of a key in the order memtable, level 1, level 2, and so on is its newest update, which is what GET returns. UPDATE puts the newest entry in the memtable, before all others. FLUSH merges the memtable into level 1, with the newer entry winning on equal keys, and when it carries a merged run on to level $i + 1$, the run holds entries newer than all those in level $i + 1$, so (M2) holds. Dropping a tombstone at the last level is safe, because no older entry of its key exists below. The proof is below.

## Complexity

Let $L = O(\log_T \frac{N}{C_0})$ be the number of levels.

- **Insert, leveled.** An entry enters level $i$ once and is rewritten each time a new run is merged into level $i$, which happens at most about $T$ times before level $i$ overflows and carries it on. Each rewrite costs $O(1/B)$ I/Os per entry, in sequential blocks. So an insert costs $O\big(\frac{T L}{B}\big)$ amortized.
- **Point lookup.** One block read per nonempty level, using the fence keys: $O(L)$ I/Os. With a Bloom filter per run and a false positive rate $p$, a lookup of an absent key reads $O(pL)$ blocks in expectation, and a lookup of a present key about one.
- **Range query.** $O(L + K/B)$ I/Os for $K$ results, as each level gives a sorted piece of the answer.
- **Space.** $O(N/B)$ blocks, plus the space of entries that are overwritten or deleted and not yet merged away, which is at most a factor of about $1 + 1/T$ in the leveled form.

| | leveled | tiered |
|---|---|---|
| insert, amortized | $O\big(\frac{T}{B}\log_T\frac{N}{C_0}\big)$ | $O\big(\frac{1}{B}\log_T\frac{N}{C_0}\big)$ |
| point lookup, no filters | $O\big(\log_T\frac{N}{C_0}\big)$ | $O\big(T\log_T\frac{N}{C_0}\big)$ |
| space amplification | about $1 + 1/T$ | up to about $T$ |

With $T = B^\varepsilon$, the leveled LSM tree has the same update and lookup bounds as the [B^ε-tree](/b-epsilon-tree/), $O\big(\frac{\log_B N}{\varepsilon B^{1-\varepsilon}}\big)$ and $O\big(\frac{\log_B N}{\varepsilon}\big)$, which are optimal by the lower bound of Brodal and Fagerberg.

## Variants

- **Leveling and tiering.** In *tiering*, each level holds up to $T$ runs that are not merged with each other until the level is full; then all of them are merged into one run of the next level. Writes are cheaper by a factor of about $T$, lookups more costly. Cassandra's size-tiered compaction is of this kind, while LevelDB and RocksDB use leveling.
- **The original LSM tree.** O'Neil and others had components $C_0, C_1, \ldots, C_k$, with $C_0$ in memory and the others B-trees on disk, kept in shape by a *rolling merge* that moves entries continuously from each component to the next.
- **Partitioned levels.** LevelDB cuts each level into files of a fixed size with disjoint key ranges and merges one file at a time into the next level, which keeps each merge small.
- **Bloom filters per level.** Monkey sets the false positive rate of each level's filter in proportion to its size, which lowers the total cost of lookups for a fixed memory budget.
- **Key-value separation.** WiscKey keeps only keys and pointers in the LSM tree and the values in a separate log, which cuts the rewrite cost for large values.

## When to use it

Use an LSM tree when writes are many and small, data lives on disk or flash, and reads can afford a few extra block reads or are helped by Bloom filters: time series, logs, message stores, and the storage layers of distributed databases. Sequential writes suit flash well, as they avoid small random writes. For read-heavy workloads with many range queries, a [B+ tree](/b-plus-tree/) or a [B^ε-tree](/b-epsilon-tree/) reads less.

## Pitfalls

- **Merges that stall writes.** A merge of a large level can take minutes. Systems that merge only when a level is full see long pauses; real engines merge in the background and throttle writes when merges fall behind.
- **Tombstones that never die.** A tombstone can be dropped only at the last level that may hold its key. Workloads that delete and reinsert keys can fill the tree with tombstones, which also slow range queries.
- **Write amplification.** Each entry is rewritten about $T$ times per level. With large values, this dominates the cost; separate keys from values or use tiering.
- **The order of merging.** When two runs hold the same key, the newer must win. Merging levels in the wrong order brings back deleted or old values.
- **Memory for fence keys and filters.** Fence keys and Bloom filters take memory in proportion to $N/B$ and to $N$ bits per key. Without them, a lookup reads more than one block per level.

## Implementations

## History

The LSM tree was introduced by Patrick O'Neil, Edward Cheng, Dieter Gawlick and Elizabeth O'Neil in Acta Informatica in 1996, for databases with heavy insert loads such as history tables; its name comes from the log-structured file system of Rosenblum and Ousterhout. Google's Bigtable (Chang and others, OSDI 2006) used memtables and immutable sorted files, and its open-source successors LevelDB and RocksDB made leveled LSM trees the standard engine for key-value stores. Luo and Carey's survey of 2020 covers the many later designs.

## References
