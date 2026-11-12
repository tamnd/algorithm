---
tag: 5FF734
kind: technique
slug: range-partitioning
name: Range partitioning
aliases:
- key-range sharding
area: systems/load-balancing-and-hashing
level: intro
summary: Cut the sorted key space at split points into contiguous ranges, one per partition. Range scans touch few partitions, but split points must follow the data, and ordered inserts hit one partition.
prereqs: [sharding, binary-search]
see_also: [hash-partitioning, sample-sort, distributed-sorting, b-plus-tree, histogram, load-skew, dynamic-partitioning-problem, partitioner]
sources:
  - paper: doi:10.1145/129888.129894
    title: David DeWitt and Jim Gray, Parallel database systems, the future of high performance database systems, Communications of the ACM 35(6), 1992, pages 85 to 98
    locator: the section on data partitioning (range partitioning next to round-robin and hash partitioning, its benefit for range queries and its risk of data skew)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: "Chapter 6, Partitioning: partitioning by key range, the hot spot of timestamp keys, and rebalancing by dynamic partitioning (split a partition that grows too big, merge one that shrinks)"
  - url: https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/
    title: Fay Chang, Jeffrey Dean, Sanjay Ghemawat, Wilson C. Hsieh, Deborah A. Wallach, Mike Burrows, Tushar Chandra, Andrew Fikes and Robert E. Gruber, Bigtable, a distributed storage system for structured data, OSDI 2006 (also ACM Transactions on Computer Systems 26(2), 2008)
    locator: "Section 2, Rows (rows in lexicographic order, the row range dynamically partitioned into tablets, reversed host names such as com.google.maps for locality), Section 5 (tablets of about 100 to 200 MB by default, split as a table grows) and Section 5.2 (tablet split and merge)"
---

Range partitioning splits a data set over $P$ partitions by cutting the sorted key space at $P - 1$ split points $b_1 < b_2 < \cdots < b_{P-1}$: partition $j$ holds the keys in $[b_j, b_{j+1})$, with $b_0 = -\infty$ and $b_P = +\infty$. A key is located by [binary search](/binary-search/) over the split points. Since each partition is a contiguous range, a range query touches only the partitions that overlap it, and the data inside each partition can stay sorted. The price is that the balance depends on choosing the split points from the data, and on the order of the writes: keys that grow over time, such as timestamps, send all inserts to the last partition.

## In plain words

Think of a printed phone book in several volumes: A to D, E to K, and so on. To find a name, you pick the volume whose range holds it. To list every name from "Smith" to "Snow", you open one or two volumes, not all of them.

The volumes must have about the same size, so the cut points cannot be fixed letters; they must come from the names themselves. And if new names all start with the same letters, one volume grows while the others do not. So systems cut a volume in two when it gets too big, and merge small neighbors.

## When it applies

- Range queries and ordered scans on the key are common: all events of a day, all rows of one customer when the customer ID is the key prefix, the next page of a sorted listing.
- The key distribution is known or can be sampled, or the system can split and merge partitions as it learns it.
- Writes are spread over the key space, or the key can be designed so that they are.

The model: $m$ records with keys from a total order, $P$ partitions, a set of split points, and a query load. The measures are the largest partition, the number of partitions that a range query touches, and the share of writes that go to one partition.

## The template

```pseudo id=main
ROUTE(k)                      ▷ b[1..P-1]: sorted split points
L1  return the number of j with b[j] ≤ k        ▷ binary search; partitions are 0 to P−1

RANGE-QUERY(lo, hi)
L2  for j ← ROUTE(lo) to ROUTE(hi) do send the query to partition j

CHOOSE-SPLITS(D, P, s)        ▷ from a random sample of P·s keys of the data D
L3  S ← the sample, sorted
L4  for j ← 1 to P − 1 do b[j] ← S[j·s]

ON-INSERT(j)                  ▷ dynamic splitting with a size threshold T
L5  if |partition j| > T then
L6      cut partition j at its median key into two partitions, and add the median to b
```

**Point and range cost.** ROUTE costs $O(\log P)$ comparisons. A range query that holds $q$ records touches at most $\lfloor q / L_{\min} \rfloor + 2$ partitions, where $L_{\min}$ is the size of the smallest partition: the touched partitions are consecutive, and all except the first and the last lie inside the range. Under [hash partitioning](/hash-partitioning/) the same query touches all $P$ partitions.

**Split points from a sample.** With exact quantiles of the data, every partition has $\lfloor m/P \rfloor$ or $\lceil m/P \rceil$ records. A full sort to find them is costly, so systems sort a random sample of $Ps$ keys and take every $s$-th one, as in [sample sort](/sample-sort/). With an oversampling factor $s = \Theta(\log m)$, every partition holds at most about $2m/P$ records with high probability (see the sample sort page), and a larger $s$ brings the largest partition closer to $m/P$.

**Dynamic splitting.** With ON-INSERT, every partition right after a split has about $T/2$ records, and no partition exceeds $T$. If records are only inserted, every partition except a first one that was never split has between $T/2$ and $T$ records, so the number of partitions is between $m/T$ and $2m/T + 1$. Merging two neighbors whose total falls below a lower threshold keeps the same bounds under deletions.

## Classic examples

**Split points from a sample.** Draw $m = 1{,}000{,}000$ keys as $\lfloor e^{X} \rfloor$ with $X$ normal with mean 10 and standard deviation 2 (seed 11), so the keys run from 1 to 483,208,169 and most are small. Cut them into $P = 8$ ranges, where the mean is 125,000 keys:

| split points | largest partition | ratio to the mean |
|---|---|---|
| equal width over the key domain | 999,968 | 8.00 |
| from a sample of 8 keys ($s = 1$) | 280,890 | 2.25 |
| from a sample of 32 keys ($s = 4$) | 265,015 | 2.12 |
| from a sample of 128 keys ($s = 16$) | 174,444 | 1.40 |
| from a sample of 800 keys ($s = 100$) | 140,961 | 1.13 |
| exact quantiles | 125,030 | 1.00 |

Equal-width ranges are useless here: almost all keys fall in the first range. Even a small sample is much better, and the largest partition approaches the mean as $s$ grows.

**Splitting as data arrives.** Start with one partition, threshold $T = 10{,}000$, and insert 100,000 keys. If the keys are uniform at random (seed 12), 15 splits give 16 partitions of 6,076 to 6,445 keys. If the keys arrive in increasing order, like timestamps, the result is 19 partitions: 18 of exactly 5,000 keys that never receive another insert, and a last one of 10,000 that received every insert. The sizes are fine, but the write load is all on one partition.

**Bigtable.** Bigtable keeps the rows of a table in lexicographic order of the row key and partitions the row range dynamically into tablets, the unit of distribution and load balancing. A tablet is about 100 to 200 MB by default and splits as it grows. To keep the pages of one web site together, the Webtable stores a URL with the host name reversed, for example com.google.maps/index.html, so that a scan of one domain reads a few contiguous tablets. HBase regions, and the ranges of several distributed SQL databases, follow the same design.

**Parallel databases and sorting.** DeWitt and Gray (1992) list range partitioning with hash and round-robin partitioning as the basic ways to spread a relation over the disks of a parallel database, and note that it suits range queries and clustered access but risks skew. [Distributed sorting](/distributed-sorting/) is range partitioning followed by a local sort, and the MapReduce [partitioner](/partitioner/) uses range partitioning for a totally ordered output.

## Variations

- **Static split points from statistics.** An equi-depth [histogram](/histogram/) of the key gives the split points. This is fine for data that is loaded once.
- **Split and merge.** Split a partition at its median when it exceeds a size or a load threshold, and merge small neighbors. A split by load, not by size, moves a hot range onto its own node.
- **Hash then range.** Range partition the hash values instead of the keys. The order of keys is lost, but the dynamic splitting remains, and sequential keys no longer pile up.
- **Key design.** Put a well-spread attribute first in a compound key, for example a customer ID before a timestamp, so that writes spread over customers while the events of one customer stay in order. Or prefix a small bucket number, which splits a sequential stream into a few streams at the cost of a few range scans per query.
- **Range partitioning in an index.** A [B+ tree](/b-plus-tree/) splits its leaves in the same way inside one machine; the split points of a range-partitioned table play the role of the upper levels of a B+ tree over the partitions.

## Pitfalls

- **Monotone keys.** Timestamps, auto-increment IDs and other keys that grow send every insert to the last partition. Splitting does not help, because the new partition is again the last. Change the key or add a prefix.
- **Equal-width ranges.** Cutting the key domain into equal intervals ignores the data and can put almost all keys in one partition, as in the example above.
- **A stale sample.** Split points from an old sample drift away from the data. Partitions that grow faster than others need splitting or a new sample.
- **Hot ranges.** Balance of record counts does not imply balance of requests. A small range of popular keys, such as the newest items, can carry most of the reads; see [load skew](/load-skew/).
- **One key larger than a partition.** A key that has many records, or one popular key, cannot be split by range alone. A tie-break on a second field makes the keys distinct and allows a split.
- **Routing metadata.** Clients must know the current split points. After a split or a move, a stale client sends a request to the wrong node, so the protocol needs a redirect or a version check.

## Exercises

1. Prove that a range query that holds $q$ records touches at most $\lfloor q / L_{\min} \rfloor + 2$ partitions, and give an example where the bound is reached.
2. With dynamic splitting at threshold $T$ and only inserts, show that each partition that resulted from a split has at least $\lfloor T/2 \rfloor$ records. What goes wrong if the split is at the mean key instead of the median key?
3. A table of events uses the key (device ID, timestamp) with 10,000 devices. Explain why inserts spread over the partitions, and how many partitions a query for the last hour of one device touches.
4. Keys arrive in increasing order with threshold $T$. After $m$ inserts, how many partitions are there, and what fraction of the inserts in the last $T/2$ steps went to the last partition?

## References
