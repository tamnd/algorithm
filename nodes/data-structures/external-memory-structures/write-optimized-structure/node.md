---
tag: SP8BJY
kind: concept
slug: write-optimized-structure
name: Write-optimized data structure
aliases:
- write-optimized index
area: data-structures/external-memory-structures
level: advanced
summary: Family of external-memory structures that batch or defer writes so that insert cost is far below a B-tree's.
prereqs: [b-tree, external-memory-model, amortized-cost]
see_also: [b-epsilon-tree, log-structured-merge-tree, buffer-tree, external-memory-priority-queue, external-searching, bloom-filter, cache-oblivious-b-tree]
sources:
  - paper: "Gerth Stolting Brodal and Rolf Fagerberg, Lower bounds for external memory dictionaries, Proceedings of the 14th ACM-SIAM Symposium on Discrete Algorithms (SODA 2003)"
    locator: pp. 546 to 554 (the trade-off between update and query costs, and its tightness)
  - paper: "Michael A. Bender, Martin Farach-Colton, William Jannen, Rob Johnson, Bradley C. Kuszmaul, Donald E. Porter, Jun Yuan and Yang Zhan, An introduction to Bε-trees and write-optimization, ;login: The USENIX Magazine 40(5) (2015)"
    locator: pp. 22 to 28 (write-optimization, the costs of B^ε-trees and LSM trees, upserts)
  - book: isbn:9781601981066
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4) (2008)
    locator: Chapter 11 (buffer trees and batched dynamic structures)
---

A write-optimized data structure is an external-memory dictionary whose updates cost much less than one I/O each, because it does not write each update to its final place at once. It collects updates in buffers or in sorted runs and moves them down in batches, so that one block transfer carries many updates. A [B-tree](/b-tree/) pays $\Theta(\log_B N)$ I/Os per insert in the [external memory model](/external-memory-model/); a write-optimized structure pays $O\big(\frac{\log_B N}{\varepsilon B^{1-\varepsilon}}\big)$ amortized, which for $\varepsilon = 1/2$ is smaller by a factor of about $\sqrt{B}$, while searches cost only a constant factor more. The main members are the [B^ε-tree](/b-epsilon-tree/), the [LSM tree](/log-structured-merge-tree/) and, for batched use, the [buffer tree](/buffer-tree/).

## In plain words

Writing one small item to disk costs about as much as writing a whole block. A B-tree pays this full price for every insert, because each new key goes straight to its leaf.

A write-optimized structure saves up. It keeps new items in a buffer and only writes when it has enough items going to the same place to fill a block. Each disk write then does the work of many inserts. The price is that a search must also look at the buffers, or wait, because recent items are not yet at their final place.

## The idea

**The trade-off.** In the external memory model with blocks of $B$ items, consider a dictionary that supports inserts and searches. Brodal and Fagerberg proved that, in a comparison-based model, if an insert costs $O\big(\frac{\log_B N}{\varepsilon B^{1-\varepsilon}}\big)$ amortized I/Os, a search must cost $\Omega\big(\frac{\log_B N}{\varepsilon}\big)$, and that this curve is reached for every $\varepsilon$ in a wide range. So there is a single dial:

| $\varepsilon$ | insert | search | structure |
|---|---|---|---|
| 1 | $O(\log_B N)$ | $O(\log_B N)$ | [B-tree](/b-tree/) |
| 1/2 | $O\big(\frac{\log_B N}{\sqrt{B}}\big)$ | $O(\log_B N)$ | [B^ε-tree](/b-epsilon-tree/), leveled [LSM tree](/log-structured-merge-tree/) with $T = \sqrt{B}$ |
| about $1/\log B$ | $O\big(\frac{\log N}{B}\big)$ | $O(\log N)$ | buffered repository tree, LSM tree with $T = 2$ |

At $\varepsilon = 1/2$, a search costs at most twice as much as in a B-tree, and an insert costs $\sqrt{B}$ times less. For $B$ in the thousands, that is a factor of 30 or more.

**Two ways to batch.**

- *Buffers in a tree.* Each internal node of a search tree keeps a buffer of pending messages, and a full buffer sends its largest batch to one child. This is the B^ε-tree. A search reads the buffers on its path.
- *Sorted runs that are merged.* Updates go into a sorted table in memory, which is written out as a run when full; runs are merged level by level, as in external merge sort. This is the LSM tree. A search looks in each run, which [Bloom filters](/bloom-filter/) make cheap.

**Why batching helps.** Moving a batch of $X$ updates down one level costs $O(1 + X/B)$ I/Os. If each batch has $\Omega(B^{1-\varepsilon})$ updates, each update pays $O(1/B^{1-\varepsilon})$ per level, over $O(\log_B N/\varepsilon)$ levels. The structures differ in how they guarantee large batches: a B^ε-tree picks the child that gets the most messages, and an LSM tree merges whole runs.

**Upserts and blind writes.** A write-optimized structure can take updates that do not need to read the old value, such as "add 1 to the counter of $k$" or "delete all keys in a range", as messages. A B-tree must read the leaf to do them, which costs a search. So write-optimized structures win most for workloads of blind writes.

**Batched versus online.** The [buffer tree](/buffer-tree/) takes the idea to its limit, with fan-out and buffers of size $\Theta(M)$, and reaches the sorting bound $O\big(\frac{1}{B}\log_{M/B}\frac{N}{B}\big)$ per update. But its queries are answered only when they reach the leaves, so it is for batched algorithms, not for online dictionaries.

## Examples

- **The B^ε-tree** with $B = 1024$ and fan-out 32: an insert costs about $1/16$ of a B-tree insert, and a search reads about twice as many nodes.
- **The leveled LSM tree** with size ratio $T = 10$: each entry is rewritten about 10 times per level, but always in long sequential runs, which suits disks and flash.
- **The buffer tree** used as an [external memory priority queue](/external-memory-priority-queue/): $N$ inserts and $N$ delete-mins cost $O\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ I/Os, the cost of sorting.
- **Cache-oblivious write-optimized structures.** The cache-oblivious lookahead array of Bender and others reaches the same insert bound as a B^ε-tree with $\varepsilon \to 0$ without knowing $B$; compare the [cache-oblivious B-tree](/cache-oblivious-b-tree/), which is read-optimized.

## Where it is used

- **Key-value stores and databases.** LevelDB, RocksDB, Cassandra, HBase and Bigtable use LSM trees; TokuDB and TokuMX used the fractal tree index, a B^ε-tree.
- **File systems.** BetrFS builds a file system on B^ε-trees, which makes small writes and metadata updates fast.
- **External algorithms.** Buffer trees and their priority queues are the base of I/O-efficient graph and geometry algorithms, such as [time-forward processing](/time-forward-processing/).
- **Indexes for streams of events.** Logs, time series and sensor data, where inserts far outnumber reads.

## References
