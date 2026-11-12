---
tag: FMPBX3
kind: problem
slug: online-memory-allocation
name: Online memory allocation
aliases:
- online dynamic storage allocation
area: systems/memory-allocation
level: advanced
summary: "Place each block when it is requested, without knowing later requests and without moving live blocks, so that the heap stays small compared with the maximum live size M."
prereqs: [allocator, external-fragmentation, online-algorithm]
see_also: [robson-bound, offline-dynamic-storage-allocation, first-fit-allocation, best-fit-allocation, size-classes, memory-compaction, knuth-fifty-percent-rule, competitive-ratio]
sources:
  - paper: doi:10.1007/3-540-60368-9_19
    title: "Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation: a survey and critical review, IWMM 1995, LNCS 986, 1-116"
    locator: Section 2 (fragmentation and the allocator's choices) and Section 4.1 (the worst-case results of Robson)
  - paper: doi:10.1145/321832.321846
    title: "J. M. Robson, Bounds for some functions concerning dynamic storage allocation, Journal of the ACM 21(3) (1974), 491-499"
    locator: the model with maximum live size M and largest block n, the exact bound for power-of-two sizes and the general bounds
  - paper: doi:10.1093/comjnl/20.3.242
    title: "J. M. Robson, Worst case fragmentation of first fit and best fit storage allocation strategies, The Computer Journal 20(3) (1977), 242-244"
    locator: the worst cases of first fit and best fit
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition, Addison-Wesley, 1997
    locator: Section 2.5, Dynamic Storage Allocation (first fit, best fit, boundary tags, the buddy system and the fifty-percent rule)
---

Online memory allocation is the task of an [allocator](/allocator/) that must place each block at the moment the program asks for it, without knowing later requests, and must never move a block that is still in use. The program frees blocks in any order, so free memory breaks into holes, and a later request may fit in none of them. The cost is the heap size, compared with $M$, the largest amount of memory that is live at one time. [Robson's bound](/robson-bound/) shows that the worst-case ratio grows like $\log n$, where $n$ is the largest block size.

## In plain words

A parking lot has one long curb and cars of many lengths. Cars arrive and leave whenever they like. The attendant must pick a spot for each car as it arrives, and a parked car is never moved. Spots between parked cars are wasted if no arriving car is short enough to fit.

The question is how long the curb must be. If at most a fixed total length of cars is parked at once, a curb of that length would do if cars could be pushed together. They cannot, so some extra curb is needed. The study asks how much extra the best attendant needs when the arrivals are as bad as possible, and how close simple rules such as "take the first gap that fits" come to that.

## Definition

**Input.** A sequence $\sigma$ of requests, revealed one at a time:

- $\mathrm{alloc}(b, s)$: a new block $b$ of $s$ words is needed, with $1 \le s \le n$;
- $\mathrm{free}(b)$: the live block $b$ is no longer needed.

Let $L_t(\sigma)$ be the total size of the live blocks after request $t$. The program promises $L_t(\sigma) \le M$ for all $t$.

**Output.** For each $\mathrm{alloc}(b, s)$, an address $p_b \ge 0$, chosen before the next request is seen, so that the interval $[p_b, p_b + s)$ meets no interval of a block that is live at that moment. A placed block keeps its address until it is freed.

**Cost.** The heap size $H_A(\sigma) = \max_b (p_b + s_b)$ of an allocator $A$ on $\sigma$. The worst case of $A$ is
$$H_A(M, n) = \sup \{ H_A(\sigma) : \sigma \text{ keeps } L_t \le M \text{ and all sizes in } [1, n] \},$$
and the problem asks for an allocator with a small $H_A(M, n)$. The best possible value $N(M, n) = \min_A H_A(M, n)$ is the subject of [Robson's bound](/robson-bound/). Since every allocator needs at least $M$ words, $H_A(M, n)/M$ plays the role of a [competitive ratio](/competitive-ratio/) against an offline allocator that may move blocks.

## Variants

- **Power-of-two sizes.** All sizes are $1, 2, 4, \dots, n$. Robson found the exact optimum for this case.
- **Worst case against average case.** The problem above is a worst-case problem. Most practical work measures fragmentation on real or random request traces instead. Knuth's [fifty-percent rule](/knuth-fifty-percent-rule/) is a result of this kind.
- **Offline.** All requests, with their arrival and departure times, are known in advance. This is [offline dynamic storage allocation](/offline-dynamic-storage-allocation/), which is NP-hard but has constant-factor approximations.
- **With moving.** If the allocator may move live blocks, the heap can stay at $M$; the cost moves to the copying and the pointer updates. See [memory compaction](/memory-compaction/). Models that allow a bounded amount of moving per request lie between the two.
- **Alignment and headers.** Real allocators round sizes and add headers. This turns some [external fragmentation](/external-fragmentation/) into [internal fragmentation](/internal-fragmentation/), and it changes the set of sizes that the analysis must handle.
- **Unit sizes.** If every block has the same size, any allocator that reuses free slots, such as [first fit](/first-fit-allocation/), keeps the heap at $M$. Fragmentation needs at least two sizes.

## Examples

**Two sizes, $M = 4$.** The sizes are 1 and 2. The program asks for four blocks of one word. First fit places them at 0, 1, 2 and 3. The program frees the blocks at 0 and 2, so the live size is 2 and the two free words are not adjacent. It then asks for a block of two words. First fit cannot use either hole and places the block at 4, so the heap size is 6 while only 4 words are live. By Robson's formula some allocator never needs more than 5 words for $M = 4$ and sizes $\{1, 2\}$, and no allocator can promise 4.

**Size classes, $M = 4$, sizes $\{1, 2\}$.** An allocator that keeps the region $[0, 4)$ for blocks of one word and $[4, 8)$ for aligned blocks of two words never fails, and never needs more than 8 words. Its worst case is worse than that of first fit here: two requests for two words already end at address 8. The gain is that the worst case of this scheme stays $O(M \log n)$ for every $n$, with a simple proof.

**Larger cases.** For $M = 8$ and sizes $\{1, 2, 4\}$, first fit can be forced to 16 words, while the best possible allocator needs 13. The [Robson's bound](/robson-bound/) page has the table and the proof.

## Known algorithms

- [First fit](/first-fit-allocation/) (address-ordered): worst case about $M \log_2 n$ (Robson 1977), so $\Theta(M \log n)$.
- [Next fit](/next-fit-allocation/): the roving pointer also makes its worst case poor, in the discussion of Wilson et al., Section 4.1.
- [Best fit](/best-fit-allocation/): worst case about $M n$ (Robson 1977), although it does well on real traces.
- [Worst fit](/worst-fit/): poor on real traces.
- [Segregated free lists](/segregated-free-lists/) and [size classes](/size-classes/): a region per size class gives $O(M \log n)$, as in the upper-bound proof of [Robson's bound](/robson-bound/).
- [Buddy system](/buddy-system/): sizes rounded to powers of two and aligned blocks; $O(M \log n)$ in the worst case, with internal fragmentation of up to a factor of 2.
- [TLSF](/tlsf/): good-fit search in $O(1)$ time, built for real-time systems.
- Production allocators: [dlmalloc](/dlmalloc/), [jemalloc](/jemalloc/), [tcmalloc](/tcmalloc/), [mimalloc](/mimalloc/) and [Hoard](/hoard-allocator/) combine size classes with other policies and tune for speed and multithreaded use.

## Bounds

- **Lower bound, any allocator that does not move blocks** (Robson 1971 and 1974). For $n$ a power of two that divides $M$, and sizes that are powers of two, the best possible worst case is exactly $M(1 + \tfrac12 \log_2 n) - n + 1$. A program that uses general sizes can still restrict itself to powers of two, so every allocator needs about $\tfrac12 M \log_2 n$ in the worst case.
- **Upper bound.** Robson (1974) gives a strategy whose worst case is about $0.84\, M \log_2 n$, in the summary of Wilson et al. A simple segregated scheme gives $M(\log_2 n + 1)$ for power-of-two sizes and $2M(\log_2 n + 1)$ for general sizes.
- **Simple policies** (Robson 1977). First fit: about $M \log_2 n$. Best fit: about $M n$.

All these are worst cases. On real programs the gap between heap size and live size is often a few percent for good policies, which is the main finding of the survey of Wilson et al.

## Reductions

- **To the offline problem.** An online allocator gives a feasible solution of [offline dynamic storage allocation](/offline-dynamic-storage-allocation/) for the same requests, so the online worst case is an upper bound on the offline optimum. The reverse direction does not hold: the offline optimum is within a constant factor of $M$, while the online worst case is $\Theta(M \log n)$.
- **Unit sizes and coloring.** With every size equal to 1, an address is a color and a block is an interval in time. The problem becomes online coloring of an interval graph, see [online graph coloring](/online-graph-coloring-problem/). First fit by address then never uses more colors than the largest number of blocks live at one time, because a freed address is reused at once.
- **To bin packing.** Dynamic bin packing, where items arrive and depart, has the same flavor, but there each bin is a separate unit and items do not need contiguous addresses across bins. See [bin packing](/bin-packing/).

## Applications

- The malloc and free of C and C++ runtimes, and the allocators inside operating system kernels.
- Real-time and embedded systems that must prove that no request fails. SQLite sizes its power-of-two allocator memsys5 with Robson's formula so that it cannot fail from fragmentation.
- Garbage-collected runtimes that do not move objects, such as conservative collectors, which face the same fragmentation.
- Planners of GPU memory and of buffers in compilers, which often know all requests in advance and use the offline version instead.

## References
