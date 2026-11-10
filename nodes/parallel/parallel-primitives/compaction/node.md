---
tag: Y5JGXC
kind: problem
slug: compaction
name: Compaction (pack)
aliases:
- filter
- stream compaction
- pack
area: parallel/parallel-primitives
level: intro
summary: Keep the elements that satisfy a predicate, preserving their order.
prereqs: [all-prefix-sums, scatter-and-gather]
see_also: [parallel-pack, blelloch-scan, decoupled-look-back-scan, warp-level-primitives, simt-model, parallel-radix-sort, fetch-and-add, data-parallelism]
sources:
  - book: isbn:9780321515261
    title: Mark Harris, Shubhabrata Sengupta and John D. Owens, Parallel Prefix Sum (Scan) with CUDA, Chapter 39 of Hubert Nguyen (editor), GPU Gems 3, Addison-Wesley, 2007
    locator: Section 39.3.1, Stream Compaction (the problem, its uses in GPU programs, and the method with flags, a scan and a scatter)
  - paper: doi:10.1145/1572769.1572795
    title: Markus Billeter, Ola Olsson and Ulf Assarsson, Efficient stream compaction on wide SIMD many-core architectures, Proceedings of the Conference on High Performance Graphics 2009, 159 to 166
    locator: stream compaction on GPUs with a count per block, a scan of the counts, and a write per block
  - url: https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf
    title: Guy E. Blelloch, Prefix Sums and Their Applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990; also Chapter 1 of John H. Reif (editor), Synthesis of Parallel Algorithms, Morgan Kaufmann, 1993
    locator: Section 1.1 (item 8 of the list of uses, to delete marked elements from an array) and Section 1.3 (the split operation)
  - paper: "Duane Merrill and Michael Garland, Single-pass Parallel Prefix Scan with Decoupled Look-back, NVIDIA Technical Report NVR-2016-002, 2016"
    title: Single-pass Parallel Prefix Scan with Decoupled Look-back
    locator: the single-pass scan, which the CUB library also uses for its select (stream compaction) operations
  - paper: doi:10.1137/0215006
    title: Stephen Cook, Cynthia Dwork and Rüdiger Reischuk, Upper and lower time bounds for parallel random access machines without simultaneous writes, SIAM Journal on Computing 15(1), 87 to 97, 1986
    locator: the Ω(log n) lower bound for the OR of n bits on a CREW PRAM
  - paper: doi:10.1145/65950.65958
    title: Paul Beame and Johan Håstad, Optimal bounds for decision problems on the CRCW PRAM, Journal of the ACM 36(3), 643 to 670, 1989
    locator: the Ω(log n / log log n) lower bound for parity on a CRCW PRAM with a polynomial number of processors
---

Compaction is the problem of keeping the items of a sequence that satisfy a predicate, in their original order, and putting them next to each other in a new array. Sequentially it is a filter: one loop, $\Theta(n)$ time. In parallel it is a basic step of many algorithms, because each processor knows whether its own item is kept but not where it must go; the position of an item depends on all the items before it. On GPUs the problem is called **stream compaction**, as in Harris, Sengupta and Owens (2007), and its standard solution is a scan of the flags followed by a scatter. That algorithm, with its proof and its exact cost of $\Theta(n)$ work and $\Theta(\log n)$ span, is on the page [parallel pack](/parallel-pack/). This page is the problem: its forms, the ways to solve it on different machines, and its bounds.

## In plain words

A long line of people holds tickets, and some tickets are winners. The winners must form a new line, in the same order as before, with no gaps.

One person working alone just walks down the line and sends each winner to the end of the new line. With many workers at the same time, the hard part is that each winner must know its place in the new line, which is the number of winners in front of it. Counting the winners in front of everybody at once is a running total, and that can be done fast in parallel. On graphics hardware this task is called stream compaction, because it removes the empty items from a stream of data.

## Definition

The input is an array $A[0 \ldots n-1]$ and a predicate keep, or an array of flags $F[0 \ldots n-1]$ with $F[i] \in \{0, 1\}$. Let $i_0 < i_1 < \cdots < i_{k-1}$ be the indices with keep$(A[i])$ true, or with $F[i] = 1$. The output is the count $k$ and the array $B[0 \ldots k-1]$ with $B[r] = A[i_r]$ for every $r$. So $B$ is the subsequence of the kept items, with no gaps and with the order of $A$. Costs are counted in the [work-span model](/work-span-model/) or on a [PRAM](/pram-model/), and on GPUs in the [SIMT model](/simt-model/), where the reads and writes of memory matter most.

**Pack and compaction.** The two names mean the same problem. This site uses *compaction* for the problem and its GPU form, and [parallel pack](/parallel-pack/) for the algorithm with flags, an exclusive scan and a scatter.

## Variants

- **Ordered compaction.** The definition above, which keeps the order. This is the form that radix sort and most other uses need.
- **Unordered compaction.** The kept items must be in $B[0 \ldots k-1]$, in any order. It is easier, because a shared counter with [fetch-and-add](/fetch-and-add/) can give out the positions.
- **Approximate compaction.** The kept items must go to an array of size $O(k)$, with gaps allowed. On a randomized CRCW PRAM, this weaker form can be solved much faster than the ordered form.
- **Split, or stable partition.** All items are kept, but the items with flag 0 come first and those with flag 1 come after them, both in their order. It is two compactions with the same flags.
- **Compaction of indices.** The output is the list of the indices $i_r$, not the items. This is the `where` or `nonzero` operation of array languages.
- **Stream compaction.** On a GPU, the input is a large stream of items in global memory, many of which are empty or no longer needed, and the goal is a dense stream for the next kernel.

## Examples

For $A = [3, 8, 1, 6, 4, 9, 2, 7]$ and the predicate "is even", the flags are $[0, 1, 0, 1, 1, 0, 1, 0]$, the count is $k = 4$, and the ordered output is $[8, 6, 4, 2]$. An unordered compaction may give $[6, 8, 2, 4]$ or any other order of the same items. The split with the same flags is $[3, 1, 9, 7, 8, 6, 4, 2]$.

For a stream of rays in a ray tracer, $[r_0, \varnothing, r_2, \varnothing, \varnothing, r_5]$, where $\varnothing$ marks a ray that left the scene, stream compaction gives $[r_0, r_2, r_5]$, so the next pass launches 3 threads, not 6.

## Known algorithms

| Algorithm | Order kept | Work | Time | Model |
|---|---|---|---|---|
| Sequential loop | yes | $\Theta(n)$ | $\Theta(n)$ | RAM |
| [Parallel pack](/parallel-pack/): flags, exclusive scan, scatter | yes | $\Theta(n)$ | $\Theta(\log n)$ | EREW PRAM, work-span |
| Blocked pack: count per block, scan the counts, copy per block | yes | $\Theta(n + p)$ | $O(n/p + \log p)$ | $p$ processors |
| Shared counter with fetch-and-add | no | $\Theta(n)$ | depends on contention | shared memory, GPU atomics |
| Single-pass scan with decoupled look-back | yes | $\Theta(n)$ | one pass over memory | GPU |

- **Scan-based.** The [parallel pack](/parallel-pack/) computes the position of each kept item as the exclusive $+$-scan of the flags and scatters the items. Its writes go to distinct cells. This is the method of Blelloch (1990) and of GPU Gems 3.
- **Blocked.** On a machine with $p$ processors or thread blocks, each block counts its kept items, one scan of the $p$ counts gives the offsets, and each block writes its items in order. Billeter, Olsson and Assarsson (2009) use this method on GPUs.
- **Atomic counter.** Each kept item takes a position with an atomic add on one counter. The order of the output then depends on the timing, and all threads compete for one memory cell. On GPUs, each warp can count its kept items with a ballot and a population count, and do one atomic add for the whole warp; see [warp-level primitives](/warp-level-primitives/).
- **Single pass.** A GPU compaction can run the scan of the counts with [decoupled look-back](/decoupled-look-back-scan/) (Merrill and Garland 2016), so the data is read once and written once. Libraries such as CUB (`DeviceSelect`) and Thrust (`copy_if`) offer compaction on GPUs.

## Bounds

- **Work.** Every item must be tested, so the work is $\Omega(n)$, and the scan-based pack does $\Theta(n)$.
- **Time on the CREW PRAM.** The count $k$ tells whether any flag is 1, which is the OR of $n$ bits. Cook, Dwork and Reischuk (1986) showed that OR needs $\Omega(\log n)$ time on a CREW PRAM with any number of processors. So the parallel pack, with $O(\log n)$ time, is optimal on the EREW and CREW PRAM.
- **Time on the CRCW PRAM.** From an ordered compaction in place, $k \bmod 2$ follows in $O(1)$ more steps: write the flags as the items, compact, and find the last cell that holds an item. So compaction is at least as hard as parity, which needs $\Omega(\log n / \log \log n)$ time with a polynomial number of processors (Beame and Håstad 1989). The same bound holds for prefix sums.
- **Memory traffic.** On a GPU, a compaction must read the $n$ input items and write the $k$ kept ones. The scan-based method with several kernels reads the data more than once, which is the cost that the single-pass methods remove.

## Reductions

- **To prefix sums and a scatter.** The positions of the ordered output are the exclusive [prefix sums](/all-prefix-sums/) of the flags, and the items move with one [scatter](/scatter-and-gather/) of distinct indices. So compaction costs at most one scan plus $O(n)$ work and $O(1)$ span.
- **From OR, counting and parity.** As in the bounds, the count of an ordered compaction gives OR, and the last position gives parity. So lower bounds for these problems apply to compaction.
- **Split.** A split is two compactions, of the items with flag 0 and of the items with flag 1, with the second written after the first. Radix sort is a sequence of splits, one for each bit.
- **Segmented compaction.** A compaction inside each segment of a segmented array reduces to a [segmented scan](/segmented-scan/) and a scatter.

## Applications

- **GPU pipelines.** Removing empty or finished work items between kernels: rays that left the scene, particles that died, triangles culled from a scene, cells of a grid that contain no surface. The next kernel then runs only on the live items.
- **Sorting.** The split step of the split [radix sort](/parallel-radix-sort/) and the partition step of [parallel quicksort](/parallel-quicksort/).
- **Graph algorithms.** Building the next frontier of a parallel breadth-first search from the vertices that were reached in this round.
- **Databases.** A selection that keeps the rows of a column that satisfy a condition is a compaction of the column, or of the row indices.
- **Sparse data.** Turning a dense array with many zeros into a list of the nonzero values and their indices.
- **Load balancing.** Removing the finished tasks from a list of active tasks, so that the remaining work is spread over all processors.

## References
