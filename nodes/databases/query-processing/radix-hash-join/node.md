---
tag: Y1EV4Y
kind: algorithm
slug: radix-hash-join
name: Radix hash join
aliases:
- radix-partitioned hash join
- radix join
area: databases/query-processing
level: advanced
summary: "Cluster both inputs on the low bits of a hash, in passes with a small fan-out, so that each cluster fits in the cache. Then join each pair of clusters with a small hash table."
solves: [relational-join]
model: word-ram
complexity:
  vars: {n: the number of tuples of R, m: the number of tuples of S, T: the number of output tuples, P: the number of clustering passes, b: the total number of radix bits, M: the cache size in words, B: the cache line size in words}
  time: {worst: "O(P(n + m) + 2^b + n m)", average: "O(P(n + m) + 2^b + T)", best: "O(P(n + m) + 2^b + T)"}
  space: {extra: "O(n + m + 2^b)"}
  io:
    average: "O(P(n + m)/B + (n + m + T)/B + 2^b)"
properties: {deterministic: true, exact: true, external: false, online: false, in_place: false, recursive: false}
history:
  year: 1999
  people: [Peter A. Boncz, Stefan Manegold, Martin L. Kersten]
  note: "Shatdal, Kant and Naughton (1994) partitioned a hash join so that each part fits in the cache. Boncz, Manegold and Kersten (1999) added the radix-cluster in several passes to limit cache and TLB misses."
prereqs: [hash-join, radix-sort, external-memory-model]
see_also: [grace-hash-join, msd-radix-sort, hash-partitioning, all-prefix-sums, lru, cache-oblivious-model, data-skew, morsel-driven-parallelism]
sources:
  - paper: "Ambuj Shatdal, Chander Kant and Jeffrey F. Naughton, Cache conscious algorithms for relational query processing, Proceedings of the 20th International Conference on Very Large Data Bases (VLDB), 1994, pages 510 to 521"
    title: Cache conscious algorithms for relational query processing
    locator: the cache partitioning of the hash join (the partitions are sized to fit in the cache)
  - paper: "Peter A. Boncz, Stefan Manegold and Martin L. Kersten, Database architecture optimized for the new bottleneck: memory access, Proceedings of the 25th International Conference on Very Large Data Bases (VLDB), 1999, pages 54 to 65"
    title: "Database architecture optimized for the new bottleneck: memory access"
    locator: the radix-cluster algorithm with several passes and the partitioned hash join
  - paper: doi:10.1109/TKDE.2002.1019210
    title: Stefan Manegold, Peter A. Boncz and Martin L. Kersten, Optimizing main-memory join on modern hardware, IEEE Transactions on Knowledge and Data Engineering 14(4), 2002, pages 709 to 730
    locator: the radix-cluster and partitioned hash join algorithms and their cost models of cache and TLB misses
  - paper: doi:10.1109/ICDE.2013.6544839
    title: "Cagri Balkesen, Jens Teubner, Gustavo Alonso and M. Tamer Özsu, Main-memory hash joins on multi-core CPUs: tuning to the underlying hardware, ICDE 2013, pages 362 to 373"
    locator: the parallel radix join and its comparison with the no-partitioning hash join (measurements)
---

Radix hash join is a [hash join](/hash-join/) for data in main memory that first splits both inputs into many small clusters on the low bits of a hash of the key, and then joins each pair of clusters with a hash table that fits in the CPU cache. The splitting is done in one or more passes, and each pass uses only a few bits, so that it writes to few places at a time and does not thrash the cache or the TLB (the cache of page translations). The [Grace hash join](/grace-hash-join/) uses the same idea one level up, to make the parts fit in the buffer pool instead of the cache, and it counts page I/Os. This page counts cache misses, and the speed-ups on real machines are measurements.

## In plain words

You must match a large pile of order slips with a large pile of customer cards. Your desk is small. If you put all customer cards in one big filing box, you must walk to a different part of the box for each slip, and you lose time at each step.

So you first sort both piles into a few trays by the last digit of the customer number. You only use a few trays at a time, so they all fit on the desk. If you need more trays, you sort each tray again by the next digit. At the end, each tray of cards is small. You then take one tray of cards and the tray of slips with the same digits, and you match them on your desk with a small box. Each card and each slip is touched a few times, but always close at hand.

## The problem

The input is two relations $R$ and $S$ in main memory, with $n$ and $m$ tuples, and the condition $r.a = s.b$. The output is the bag $R \bowtie S$ of the [relational join problem](/relational-join/): one tuple $r \cdot s$ for each matching pair, so a key that occurs $x$ times in $R$ and $y$ times in $S$ gives $x y$ outputs. A NULL key never matches.

**Cost model.** There are two measures. The first is the number of steps in the [word RAM](/word-ram/). The second is the number of cache misses in the [external memory model](/external-memory-model/), with a cache of $M$ words in lines of $B$ words. In the external memory model, the memory holds $M/B$ blocks; on this page the memory is the cache and a block is a cache line, so the cache holds $M/B$ lines. A tuple takes one word. The hash is $h(k) = (k \cdot 2654435761) \bmod 2^{32}$ on integer keys. Its low 4 bits are the low 4 bits of $k$, because the multiplier is 1 modulo 16, so on small integers it acts like clustering on the key bits.

## The algorithm

```pseudo id=main
RADIX-CLUSTER(X, h, b_1, ..., b_P)          ▷ X is an array of n tuples
L1  b ← b_1 + ... + b_P; the clusters are [the whole of X]
L2  for p ← 1 to P do
L3      s ← b − (b_1 + ... + b_p)            ▷ pass p uses bits s to s + b_p − 1 of h
L4      for each cluster C, in order do
L5          count[j] ← the number of x in C with digit (h(x.key) >> s) mod 2^b_p = j       ▷ histogram
L6          start[j] ← start of C + count[0] + ... + count[j − 1]      ▷ prefix sum
L7          for each x in C, in order: Y[start[j]] ← x and start[j] ← start[j] + 1, where j is the digit of x      ▷ scatter
L8      X ← Y; the clusters are the pieces of all clusters, in order
L9  return X and the bounds of its 2^b clusters
RADIX-JOIN(R, S, h, b_1, ..., b_P)
L10 cluster R and S with RADIX-CLUSTER(·, h, b_1, ..., b_P)
L11 for i ← 0 to 2^b − 1 do
L12     build a bucket-chained table on cluster i of R, indexed by the bits of h above bit b
L13     for each s in cluster i of S and each r in the bucket of s.b with r.a = s.b do output r · s
L14 return the output
```

Each pass is one step of an [MSD radix sort](/msd-radix-sort/) on the low $b$ bits of the hash: a histogram (line L5), a [prefix sum](/all-prefix-sums/) (line L6) and a stable scatter (line L7). Pass 1 uses the highest of the $b$ bits, and each later pass splits each cluster again on the next bits, so after pass $P$ cluster $i$ holds the tuples with $h(k) \bmod 2^b = i$. A pass with $b_p$ bits writes to $2^{b_p}$ places at once, its *fan-out*. More passes give a smaller fan-out per pass, at the cost of one more read and write of all tuples.

The table of line L12 must use bits of $h$ that the clustering did not use, because all tuples of a cluster share their low $b$ bits. The implementation keeps the table as an array of bucket heads and an array of next links, as in the radix join of Balkesen et al. The table and the cluster must fit in the cache, which fixes $b$: about $\log_2$ of $n$ divided by the number of tuples that fit in the cache with their table.

## Example

Let $R$ have the keys $[3, 1, 4, 1, 5, 9, 2, 6]$ (tuples $r_0$ to $r_7$) and $S$ have the keys $[1, 4, 1, 8, 5, 9]$ ($s_0$ to $s_5$). For these keys $h(k) \bmod 4 = k \bmod 4$. Take $b = 2$ in two passes of one bit each.

| step | what happens to $R$ | result |
|---|---|---|
| pass 1, L5 | digit = bit 1 of the hash: keys 1, 4, 1, 5, 9 give 0, keys 3, 2, 6 give 1 | count = [5, 3] |
| pass 1, L6 to L7 | scatter in input order | $[r_1, r_2, r_3, r_4, r_5 \mid r_0, r_6, r_7]$ |
| pass 2, first cluster | digit = bit 0: key 4 gives 0, keys 1, 1, 5, 9 give 1 | $[r_2 \mid r_1, r_3, r_4, r_5]$ |
| pass 2, second cluster | keys 2, 6 give 0, key 3 gives 1 | $[r_6, r_7 \mid r_0]$ |
| L9 | clusters 0 to 3 | $[r_2 \mid r_1, r_3, r_4, r_5 \mid r_6, r_7 \mid r_0]$, bounds $[0, 1, 5, 7, 8]$ |

$S$ gives cluster 0 = $[s_1, s_3]$ (keys 4 and 8) and cluster 1 = $[s_0, s_2, s_4, s_5]$ (keys 1, 1, 5, 9); clusters 2 and 3 of $S$ are empty, so line L11 skips them. Cluster 0 gives $r_2 \cdot s_1$, and $s_3$ finds only $r_2$ with key $4 \ne 8$ in its bucket. Cluster 1 gives 6 tuples: $s_0$ and $s_2$ each find $r_1$ and $r_3$, $s_4$ finds $r_4$ and $s_5$ finds $r_5$. The output has 7 tuples, the bag join, and the join phase makes 8 key comparisons. Each pass moved all 8 tuples of $R$.

**Simulated cache misses.** The implementation can record every word it reads or writes and run the trace through a fully associative [LRU](/lru/) cache. With $n = m = 200$ tuples, keys drawn from 0 to 999 with seed 1, and a cache of 16 lines of 4 words, the counts are:

| run | cache misses |
|---|---|
| cluster $R$ on 6 bits in one pass (fan-out 64) | 472 |
| cluster $R$ on 6 bits in two passes of 3 bits (fan-out 8) | 305 |
| join phase without clustering (one table on all of $R$) | 808 |
| join phase after clustering on 4 bits | 147 |
| join phase after clustering on 6 bits | 105 |

A fan-out of 64 needs more lines than the cache has, so many scatter writes miss, and the two passes of fan-out 8 miss less although they move each tuple twice. The table on all of $R$ is far larger than the cache, so most probes miss, while the tables of small clusters stay in the cache. These are counts in this toy model, not timings of a real machine.

## Correctness

After the last pass, cluster $i$ holds exactly the tuples with $h(k) \bmod 2^b = i$: each pass is a stable counting scatter of each cluster on the next digit. Two tuples with the same key have the same hash, so every matching pair lies in one pair of clusters with the same number, and the hash join of that pair finds it once. The full proof, with the bounds on work and on cache misses, is in [the proof page](proofs/correctness.md).

## Complexity

- **Work.** Each pass reads every tuple twice and writes it once, and it does $O(2^{b_p})$ work per cluster for the counters, so the clustering costs $O(P(n + m) + 2^b)$ steps. Under the simple uniform hashing assumption for the bucket bits, the join phase does expected $O(n + m + T)$ work. The worst case, when every key of a cluster shares one bucket, is $O(n m)$ comparisons (a theorem in the word RAM).
- **Cache misses.** If every pass has a fan-out that fits in the cache with one line per output cursor, and every cluster of $R$ with its table fits in the cache, the radix join has $O(P(n + m)/B + (n + m + T)/B + 2^b)$ misses (a theorem in the external memory model). A hash join with one table much larger than the cache misses on almost every probe, about $m$ misses.
- **TLB misses.** The same count with a memory page in place of a line and the number of TLB entries in place of $M/B$ limits the fan-out of a pass to about the number of TLB entries. This was the reason for several passes in Boncz et al. (1999) and Manegold et al. (2002).
- **Space.** The clustering needs a second array of $n + m$ tuples and $2^{b_p}$ counters. The join phase needs one table at a time.
- **Measurements.** Boncz, Manegold and Kersten (1999) and Manegold, Boncz and Kersten (2002) measured the radix join on the machines of their time and fitted models of the cache and TLB misses to the measured times. Balkesen et al. (2013) compared a tuned parallel radix join with a no-partitioning hash join on several multi-core machines, and the radix join was faster in most of their settings. These results depend on the hardware; this page does not repeat their numbers.

## Properties

- **Not pipelined.** Both inputs must be fully clustered before the first output, so the operator is a pipeline breaker on both sides, unlike the probe side of a hash join.
- **Stable clusters.** Each cluster keeps the input order, because the scatter is stable.
- **Output order.** The output comes cluster by cluster, so it is grouped by the low bits of the hash, not by key order.
- **Equality only.** Like every hash join, it cannot answer a band or an inequality condition.
- **Deterministic.** With a fixed hash function, the clusters and the output order are fixed.

## Variants and improvements

- **Number of passes.** One pass is best when $2^b$ is below the number of cache lines and TLB entries. With more clusters, two passes are usually used. Choosing $P$ and the $b_p$ is a tuning decision on measured hardware.
- **Partition the build side only.** Some systems cluster only $R$ and probe the clusters with an unclustered $S$, which saves a pass but gives up the cache locality of the probes.
- **Parallel radix join.** Each thread builds a histogram of its part of the input, a global prefix sum gives each thread its own output ranges, and then the threads scatter without locks. Balkesen et al. (2013) tune this form, and [morsel-driven parallelism](/morsel-driven-parallelism/) schedules the work.
- **Software write-combining buffers.** The scatter can write each output cluster first into a small buffer of one cache line and copy the full line at once, which reduces TLB misses for larger fan-outs.
- **Grace hash join.** The [Grace hash join](/grace-hash-join/) is the disk form: it partitions until each part fits in the buffer pool, and counts page I/Os instead of cache misses. A [hybrid hash join](/hybrid-hash-join/) keeps one part in memory.
- **Sort-merge instead.** A radix sort of both inputs followed by a merge, as in [sort-merge join](/sort-merge-join/), uses the same clustering steps and gives sorted output.

## When to use it

Use it for a large equi-join in main memory when the smaller input is much larger than the cache, for example two tables of millions of rows in a column store. When the smaller input fits in the cache, a plain [hash join](/hash-join/) is simpler and as fast. When the input does not fit in memory, partition it on disk first with a [Grace hash join](/grace-hash-join/).

## Pitfalls

- **Too many clusters in one pass.** A fan-out above the number of cache lines or TLB entries makes most writes of line L7 miss. Split the bits over several passes.
- **Reusing the radix bits in the table.** Line L12 must index the table with bits that line L5 did not use. Inside a cluster the low $b$ bits are equal, so a table on them puts every tuple in one bucket.
- **A weak hash.** The low bits of a multiplicative hash of small integers are the low bits of the key. Keys with a common pattern in their low bits, for example all even, fill only part of the clusters. Use a hash with good low bits when the keys are not uniform.
- **Skew.** A key with many tuples makes one cluster that no number of bits can split. Its table does not fit in the cache, and in a parallel join one thread gets most of the work (see [data skew](/data-skew/)).
- **Treating measured speed-ups as guarantees.** The gain over a plain hash join depends on the cache size, the TLB, the tuple width and the number of threads. It is a measurement, not a theorem.

## Implementations

## History

Shatdal, Kant and Naughton (1994) studied cache-conscious algorithms for query processing and partitioned the hash join so that each part fits in the cache. Boncz, Manegold and Kersten (1999) showed that on the machines of that time a single-pass partitioning with many parts was limited by TLB misses, and they introduced the radix-cluster algorithm with several passes, each with a small fan-out, in the Monet system. Manegold, Boncz and Kersten (2002) gave detailed cost models of cache and TLB misses for these algorithms. Blanas, Li and Patel (2011) argued that a simple hash join without partitioning is competitive on multi-core machines, and Balkesen, Teubner, Alonso and Özsu (2013) showed that a radix join tuned to the hardware is faster in most of their measured cases.

## References
