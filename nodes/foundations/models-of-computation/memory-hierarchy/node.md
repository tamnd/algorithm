---
tag: K1SRPF
kind: concept
slug: memory-hierarchy
name: Memory hierarchy
aliases:
- memory hierarchy model
area: foundations/models-of-computation
level: intro
summary: Layered storage from registers and caches to disk, with capacity and speed trade-offs that shape algorithm design.
prereqs: [random-access-machine]
see_also: [locality-of-reference, external-memory-model, cache-oblivious-model, cache-replacement-policy, unit-cost-model, belady-algorithm, belady-anomaly, red-blue-pebble-game]
sources:
  - book: isbn:9780128119051
    title: "John L. Hennessy and David A. Patterson, Computer Architecture: A Quantitative Approach, sixth edition"
    locator: Chapter 2 (memory hierarchy design) and Appendix B (review of memory hierarchy, average memory access time, the three kinds of miss)
  - book: isbn:9781601981066
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4) (2008)
    locator: Chapter 1 (Figure 1.1, the memory hierarchy of a typical system) and Section 2.3 (hierarchical memory models)
  - paper: doi:10.1147/sj.52.0078
    title: Laszlo A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2) (1966)
    locator: pp. 78 to 101
  - paper: doi:10.1145/363011.363155
    title: Laszlo A. Belady, Robert A. Nelson and Gerald S. Shedler, An anomaly in space-time characteristics of certain programs running in a paging machine, Communications of the ACM 12(6) (1969)
    locator: pp. 349 to 353
  - paper: doi:10.1147/sj.92.0078
    title: Richard L. Mattson, Jan Gecsei, Donald R. Slutz and Irving L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) (1970)
    locator: pp. 78 to 117 (stack algorithms and the inclusion property)
  - paper: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985)"
    locator: pp. 202 to 208 (the bound for LRU and FIFO against the optimal rule)
  - paper: doi:10.1145/28395.28428
    title: Alok Aggarwal, Bowen Alpern, Ashok K. Chandra and Marc Snir, A model for hierarchical memory, Proceedings of the 19th ACM Symposium on Theory of Computing (1987)
    locator: pp. 305 to 314
  - paper: doi:10.1145/216585.216588
    title: Wm. A. Wulf and Sally A. McKee, Hitting the memory wall, implications of the obvious, ACM SIGARCH Computer Architecture News 23(1) (1995)
    locator: pp. 20 to 24
  - paper: "Jia-Wei Hong and H. T. Kung, I/O complexity: the red-blue pebble game, Proceedings of the 13th ACM Symposium on Theory of Computing (1981)"
    locator: pp. 326 to 333 (the lower bound for matrix multiplication)
  - paper: doi:10.1145/48529.48535
    title: Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9) (1988)
    locator: pp. 1116 to 1127
---

The memory hierarchy is the layered storage of a computer: registers, caches, main memory and disk. Each layer is larger, slower and cheaper per byte than the layer above it. The machine moves data between adjacent layers in blocks, so a program is fast when it uses the same data again soon or uses data that is close together ([locality of reference](/locality-of-reference/)). The [random access machine](/random-access-machine/) gives each memory access the same cost, so it does not show this effect, and the [external memory model](/external-memory-model/) and the [cache-oblivious model](/cache-oblivious-model/) were made to capture it.

## In plain words

A cook keeps a few tools in the hand, more on the table, many in the cupboard, and the rest in a store room down the street. A trip to the store room costs a long walk, so a good cook brings back many things from one trip and keeps the ones needed soon on the table.

A computer works the same way. The processor works on a few values in registers. Next to them is a small, fast cache, then the larger and slower main memory, then the much larger and much slower disk. When a fast layer does not have a value, the machine fetches the whole block that holds it from the next layer. A program runs fast if it uses the rest of that block soon, and if it uses the same values again before they are pushed out.

## The idea

### Levels, hits and misses

A hierarchy has levels $1, 2, \ldots, k$. Level 1 is the smallest and fastest. Each level holds copies of some blocks of the level below it. A request that finds its data in a level is a *hit*. A request that does not is a *miss*, and the level then asks the level below. A miss moves one *block* (a cache line, a page or a disk block, depending on the level) up. If the upper level is full, a [replacement policy](/cache-replacement-policy/) chooses a block to evict.

The average memory access time of a level (Hennessy and Patterson, Appendix B) is

$$\text{AMAT} = \text{hit time} + \text{miss rate} \times \text{miss penalty},$$

where the miss rate is the fraction of requests to this level that miss, and the miss penalty is the time to get the block from the level below. For a level below the first, the miss penalty is itself an AMAT, so the formula is applied from the bottom up. A level with a hit time of 1 ns, a miss rate of 5 percent and a miss penalty of 100 ns has $\text{AMAT} = 1 + 0.05 \times 100 = 6$ ns. If an L2 cache with a hit time of 4 ns and a local miss rate of 20 percent sits between it and a main memory of 80 ns, the miss penalty of L1 drops to $4 + 0.2 \times 80 = 20$ ns, and the AMAT drops to $1 + 0.05 \times 20 = 2$ ns.

Hennessy and Patterson sort misses into three kinds:

- a *compulsory* miss is the first access to a block, which misses in a cache of any size;
- a *capacity* miss happens because the blocks that the program uses do not all fit in the level, so it would also happen in a fully associative cache of the same size;
- a *conflict* miss happens because too many blocks map to the same *set*. In a direct-mapped or set-associative cache, a block can go only into the few slots of one set, chosen by bits of its address.

### Typical sizes and times

The table gives orders of magnitude for a desktop or server computer of recent years. The values differ between products and change with each generation. They are not exact.

| Level | Typical capacity | Typical access time | Typical block size |
|---|---|---|---|
| Registers | hundreds of bytes to a few KB | under 1 ns | none (the compiler moves values with explicit instructions) |
| L1 cache | tens of KB | about 1 ns | 64 bytes (a cache line) |
| L2 cache | hundreds of KB to a few MB | a few ns | 64 bytes |
| L3 cache | a few MB to tens of MB | 10 to 40 ns | 64 bytes |
| Main memory (DRAM) | GB | 50 to 100 ns | 64 bytes per cache line, 4 KB per virtual memory page |
| Solid-state drive | hundreds of GB to TB | 10 to 100 microseconds | 4 KB (flash pages are often 4 to 16 KB) |
| Hard disk | TB | 5 to 10 ms (seek plus rotation) | 512 bytes to 4 KB per sector, larger logical blocks |

Two facts follow. First, the gap between levels is large: a hard disk access takes about $10^5$ times as long as a main memory access, and a main memory access takes about $10^2$ times as long as an L1 access. Wulf and McKee (1995) pointed out that processor speed grew faster than DRAM speed, so this gap grows, and they named the effect the *memory wall*. Second, most of the cost of a miss is a fixed delay before the first byte arrives, and the further bytes of the block cost little. This is the reason for block transfer, and the reason that a program should use all of each block that it loads.

### Locality

A program has *locality* when its accesses are not spread evenly over the memory. See [locality of reference](/locality-of-reference/).

- *Temporal locality*: an address that is used now is likely to be used again soon. It lets a small, fast level hold the data in use.
- *Spatial locality*: an address near one used now is likely to be used soon. It lets one block transfer serve many accesses.

The set of blocks that a program uses in a window of time is its *working set*. A level that holds the working set has few misses. See the [working set model](/working-set-model/).

### Replacement and the stack property

The replacement policy matters only for capacity and conflict misses.

- The optimal offline rule evicts the block whose next use is farthest in the future. Belady (1966) described it. It needs the future, so it serves as a yardstick, not as a real policy. See [Belady's algorithm](/belady-algorithm/).
- Least recently used (LRU) evicts the block whose last use is oldest.
- First in, first out (FIFO) evicts the block that was loaded first.

Mattson, Gecsei, Slutz and Traiger (1970) called a policy a *stack algorithm* if, on every request sequence and at every time, the contents of a cache of $k$ blocks are a subset of the contents of a cache of $k+1$ blocks. LRU and the optimal rule have this *inclusion property*, so a larger cache never has more misses under them. FIFO does not have it. Belady, Nelson and Shedler (1969) found programs that miss more often under FIFO when the memory grows. This is [Belady's anomaly](/belady-anomaly/).

Sleator and Tarjan (1985) compared online policies with the optimal rule. Let LRU or FIFO have a cache of $k$ blocks, and the optimal rule a cache of $h \le k$ blocks. On every request sequence, the number of misses of LRU or FIFO is at most $\frac{k}{k-h+1}$ times the misses of the optimal rule, plus at most $h$. With $k = 2h$, the factor is less than 2. No online policy can do better than the factor $\frac{k}{k-h+1}$ in the worst case (same paper). The [cache-oblivious model](/cache-oblivious-model/) uses this result to move bounds from the optimal rule to LRU.

### Why the RAM model misses it

In the [random access machine](/random-access-machine/) with the [unit-cost model](/unit-cost-model/), each memory access costs one step, wherever the cell is. Two programs with the same number of operations get the same cost, even if one of them runs many times slower because it misses the cache on each access. Models of the hierarchy add parameters for the memory size and the block size:

- The [external memory model](/external-memory-model/) of Aggarwal and Vitter (1988) has two levels, a fast memory of $M$ items and a disk with blocks of $B$ items, and it counts block transfers. In it, a scan of $N$ items costs $\Theta(N/B)$ transfers and sorting costs $\Theta\big((N/B)\log_{M/B}(N/B)\big)$.
- The [cache-oblivious model](/cache-oblivious-model/) is the same model, but the program does not know $M$ and $B$. Under a mild regularity condition, an optimal algorithm in it is within a constant factor of optimal at each level of an LRU hierarchy at once.
- The hierarchical memory model (HMM) of Aggarwal, Alpern, Chandra and Snir (1987) has no blocks. An access to address $x$ costs $f(x)$ for a nondecreasing function $f$, such as $f(x) = \lceil \log x \rceil$, so that data near the start of memory is cheap.
- The [red-blue pebble game](/red-blue-pebble-game/) of Hong and Kung (1981) counts transfers between a fast memory of $M$ words and a slow memory, for a computation given as a fixed graph.

## Examples

**Rows against columns.** Take an $n \times n$ array of 8-byte numbers stored row by row, with $n = 4096$, so a row has 32768 bytes. A cache line holds 64 bytes, which is 8 numbers. The array starts at a line boundary, the cache starts empty, it is fully associative with LRU replacement, and it holds fewer than $n$ lines.

- Summing row by row reads the numbers in memory order. Each line serves 8 accesses, so the sum makes $4096^2/8 = 2097152$ misses for $4096^2 = 16777216$ accesses.
- Summing column by column reads addresses 32768 bytes apart. One column touches $n$ different lines. The cache holds fewer than $n$ lines, so under LRU a line is evicted before the next column comes back to it. Every access misses: $16777216$ misses, 8 times as many.

Both loops make the same $n^2$ additions, so the RAM model gives them the same cost.

**Conflict misses from a power-of-two stride.** Take an L1 cache of 32 KiB with lines of 64 bytes and 8 ways. It has 512 lines in $512/8 = 64$ sets, and a line with line number $\ell$ (the address divided by 64) goes to set $\ell \bmod 64$. Sum a $512 \times 512$ array of 8-byte numbers column by column. A row has 4096 bytes, which is 64 lines, so the 512 lines of one column all fall in the same set, and that set holds only 8 of them.

| Layout and cache | Misses for $512^2 = 262144$ accesses |
|---|---|
| Rows of 4096 bytes, fully associative LRU cache of 512 lines | 32768 |
| Rows of 4096 bytes, 8-way cache with 64 sets | 262144 |
| Rows padded to 4160 bytes (one extra line), 8-way cache with 64 sets | 32768 |

In the first row of the table, one column needs 512 lines and the cache holds all 512, so each line is loaded once and serves 8 columns. In the second row, the cache has the same size, but every access misses: all misses are conflict misses. With one line of padding per row, row $i$ starts at line $65i$, which falls in set $(65 i) \bmod 64 = i \bmod 64$, so the 512 lines of a column spread evenly over the 64 sets, 8 lines per set.

**Replacement policies.** Request the blocks $1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5$ from an empty cache. The numbers of misses are:

| Cache size | FIFO | LRU | Optimal rule |
|---|---|---|---|
| 3 blocks | 9 | 10 | 7 |
| 4 blocks | 10 | 8 | 6 |

FIFO makes more misses with 4 blocks than with 3, which is Belady's anomaly. LRU and the optimal rule, which are stack algorithms, do not. On this sequence LRU is worse than FIFO with 3 blocks, so neither online rule is better than the other on every sequence.

**Non-example.** A program that reads a random address of a large array each time has no locality. If the array is much larger than the cache, almost every access misses, whatever the block size. A larger block only brings in more bytes that are never used.

## Where it is used

- [External memory algorithms](/external-memory-model/), such as [external merge sort](/external-merge-sort/) and the [B-tree](/b-tree/), count block transfers between main memory and disk.
- [Cache-oblivious algorithms](/cache-oblivious-model/), such as [funnelsort](/funnelsort/) and the [van Emde Boas layout](/van-emde-boas-layout/), are efficient for every block size and memory size without knowing them.
- Blocked loops (tiling) in matrix code. For the standard $\Theta(n^3)$ product of $n \times n$ matrices, tiles of side about $\sqrt{M/3}$ keep three tiles in a fast memory of $M$ words, and the number of transfers falls to $O(n^3/(B\sqrt{M}))$ for blocks of $B$ words when $M \ge c B^2$ for a suitable constant $c$. Hong and Kung (1981) proved that every schedule of the standard method needs $\Omega(n^3/\sqrt{M})$ word transfers, so tiling is optimal up to a constant factor. See [cache-oblivious matrix multiplication](/cache-oblivious-matrix-multiplication/) for a version without $M$ and $B$.
- Virtual memory treats main memory as a cache of the disk, in pages of typically 4 KB. A program whose working set does not fit in main memory spends most of its time on page transfers, which is called *thrashing*.
- Operating systems and databases choose [what to evict](/cache-replacement-policy/) from main memory and from the buffer pool, and they read ahead ([prefetching](/prefetching/)) when they detect a sequential scan.

### Pitfalls

- **Exact numbers from the table.** The sizes and times above are orders of magnitude. A bound that depends on one exact value, such as "L1 has 32 KB", holds only for that machine. Measure the machine, or use a cache-oblivious design.
- **Counting misses as time.** A modern processor runs many misses at once and prefetches sequential lines. A scan that misses on each line can then run near the bandwidth limit, while a chain of dependent misses, as in a linked list, pays the full latency each time. Two programs with the same number of misses can differ a lot in time.
- **Ignoring associativity.** The models of the hierarchy assume a fully associative cache. A stride that is a large power of two can make every access a conflict miss, as in the example above. Pad the rows, or avoid such strides.
- **"More memory never hurts."** This is true for LRU and the optimal rule, which are stack algorithms, but false for FIFO (Belady's anomaly).
- **Bytes against items.** Hardware gives sizes in bytes. The models give $M$ and $B$ in items. Divide by the item size before using a formula.
- **Optimizing the wrong level.** The gap between main memory and disk is about $10^5$, and the gap between L1 and main memory is about $10^2$. For data on disk, the disk transfers decide the time, and cache tuning in memory changes little.

## References
