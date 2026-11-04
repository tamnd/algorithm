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
see_also: [locality-of-reference, external-memory-model, cache-oblivious-model, cache-replacement-policy, unit-cost-model]
sources:
  - book: isbn:9780128119051
    title: "John L. Hennessy and David A. Patterson, Computer Architecture: A Quantitative Approach, sixth edition"
    locator: Chapter 2 and Appendix B
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 18, introduction (on disks and B-trees)
  - book: isbn:9781601981066
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory
    locator: Chapter 1
  - paper: "Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9) (1988), 1116 to 1127"
  - paper: "Matteo Frigo, Charles E. Leiserson, Harald Prokop and Sridhar Ramachandran, Cache-oblivious algorithms, 40th Annual Symposium on Foundations of Computer Science (1999)"
---

The memory hierarchy is the layered storage of a computer: registers, caches, main memory and disk. Each layer is larger, slower and cheaper per byte than the one above it. The computer moves data between adjacent layers in blocks, and a program is fast when it uses the same data again and again, or data that is close together. The [random access machine](/random-access-machine/) gives each memory access the same cost, so it does not show this effect.

## In plain words

A cook has a few tools in the hand, more on the table, many in the kitchen cupboard, and a store room in the next street. Taking a tool from the hand costs nothing. Going to the store room costs a long walk. A sensible cook brings back many things from one trip, and keeps the ones needed soon on the table.

A computer does the same. The processor works on a few values in registers. Next to them is a small, fast cache. Behind the cache is the main memory, which is larger and slower. Behind that is the disk, which is much larger and much slower. Each layer copies a part of the layer below. When the fast layer lacks a value, the machine fetches the whole block that holds it. The program runs fast if it uses the rest of the block soon.

## The idea

A hierarchy has several levels. Level 1 is the fastest and smallest. A level holds copies of data from the next level down. A request that finds its data in a level is a *hit*. A request that does not is a *miss*, and the machine then asks the next level. A miss moves one *block* (a cache line, a page or a sector, depending on the level) from the lower level to the upper one. If the upper level is full, a [replacement policy](/cache-replacement-policy/) chooses a block to evict.

The average memory access time (AMAT) of a level is the hit time plus the miss rate times the miss penalty. The miss penalty is roughly the AMAT of the next level down, plus the time to transfer the block. For example, a level with a hit time of 1 ns, a miss rate of 5 percent and a miss penalty of 100 ns has an AMAT of $1 + 0.05 \times 100 = 6$ ns. A miss is *compulsory* when it is the first access to a block, a *capacity* miss when the working set does not fit in the level, and a *conflict* miss when the level has room overall but too many blocks map to the same set. In a direct-mapped or set-associative cache, each block can go only in a few fixed places, and these places form a *set*.

The table gives typical values for a desktop or server computer in recent years. They are orders of magnitude, not exact values. They differ between products and change with each generation.

| Level | Typical capacity | Typical access time | Typical block size |
|---|---|---|---|
| Registers | hundreds of bytes to a few KB | under 1 ns | none (the compiler loads values with explicit instructions) |
| L1 cache | tens of KB | about 1 ns | 64 bytes (a cache line) |
| L2 cache | hundreds of KB to a few MB | a few ns | 64 bytes |
| L3 cache | a few MB to tens of MB | 10 to 40 ns | 64 bytes |
| Main memory (DRAM) | GB | 50 to 100 ns | 64 bytes |
| Solid-state drive | hundreds of GB to TB | 10 to 100 microseconds | 4 KB (the usual read unit; flash pages are often 4 to 16 KB) |
| Hard disk | TB | 5 to 10 ms | 512 bytes to 4 KB (a sector) |

Two facts follow from the table. First, the gap between neighbouring levels is large: a hard disk access takes about $10^5$ times as long as a main memory access, and a main memory access takes about $10^2$ times as long as an L1 access. Second, the cost of a miss is mostly a fixed delay (the wait for the first byte), and the extra bytes of a block cost little. This is why the machine moves data in blocks, and why a program should use all of a block that it loads.

### Locality

A program has *locality* when its accesses are not spread evenly over the memory. There are two kinds. See [locality of reference](/locality-of-reference/).

- *Temporal locality*: a program that uses an address now is likely to use it again soon.
- *Spatial locality*: a program that uses an address now is likely to use a nearby address soon.

A hierarchy rewards both. Temporal locality lets a small fast level hold the data in use. Spatial locality lets one block transfer serve many accesses.

### Why the RAM model misses it

In the [random access machine](/random-access-machine/) with the [unit cost](/unit-cost-model/), each access to a memory cell costs one step, wherever the cell is. Two algorithms with the same operation count have the same cost in this model, even if one of them runs ten times slower on a real computer because it misses the cache on every access. The models of [external memory](/external-memory-model/) and [cache-oblivious](/cache-oblivious-model/) algorithms add the block size and the memory size as parameters, so that they can count misses. With memory size $M$ and block size $B$, scanning $N$ items costs $\Theta(N/B)$ transfers, and sorting costs $\Theta((N/B)\log_{M/B}(N/B))$ transfers (Aggarwal and Vitter, 1988).

## Examples

Take an $n \times n$ array of 8-byte numbers, stored row by row, with $n = 4096$. A cache line holds 64 bytes, which is 8 numbers. Suppose the array starts at a line boundary, the cache is empty at the start, the cache is fully associative, it holds fewer than $n$ lines, and it evicts the least recently used line.

- Summing row by row reads the numbers in memory order. Each line loaded serves 8 accesses. The sum makes $4096^2 / 8 = 2097152$ misses, out of $4096^2 = 16777216$ accesses.
- Summing column by column reads addresses $8n$ bytes apart. The $n$ lines used by one column do not fit in the cache. A line loaded for one column is evicted before the next column needs it. So every access misses, and the sum makes $4096^2 = 16777216$ misses, 8 times as many as before.

Both loops make the same $n^2$ additions, so the RAM model gives them the same cost. A real cache is set-associative, which adds a pitfall: the stride $8n = 32768$ bytes is a power of two, so the lines of one column map to a few sets of the cache. Conflict misses then appear even when the column would fit in the cache. Padding each row by one line avoids this.

A non-example: a program that reads a random address of a large array each time has no locality. If the array is much larger than the cache, almost every access misses, so the program makes about one miss per access whatever the block size. A larger block only brings in more bytes that are never used.

## Where it is used

The hierarchy is the reason for several design choices.

- [External memory algorithms](/external-memory-model/) such as [external merge sort](/external-merge-sort/) and the [B-tree](/b-tree/) count block transfers between main memory and disk.
- [Cache-oblivious algorithms](/cache-oblivious-model/) are efficient for every block size and memory size, without knowing them.
- Blocked loops (tiling) in matrix code, and array layouts that keep neighbouring items together, serve spatial and temporal locality. For matrix multiplication, tiles of size $b \times b$ with $b$ about $\sqrt{M}$ reduce the misses of the naive method from $\Theta(n^3)$ to $\Theta(n^3/(B\sqrt{M}))$, for $n \times n$ matrices, memory size $M$ and block size $B$ (Frigo, Leiserson, Prokop and Ramachandran, 1999).
- Virtual memory treats main memory as a cache of the disk, in pages of typically 4 KB. The translation lookaside buffer (TLB) caches address translations. A program with poor locality can make the system thrash, which means that it spends most of its time on page transfers.
- Operating systems and databases choose [what to evict](/cache-replacement-policy/) from main memory and from the buffer pool.

## References
