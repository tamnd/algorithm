---
tag: AGKZS1
kind: algorithm
slug: parallel-pack
name: Parallel pack
aliases:
- parallel filter
- pack by scan
area: parallel/parallel-primitives
level: intro
summary: Compaction via a flag array, an exclusive scan, and a scatter.
solves: [compaction]
model: work-span-model
complexity:
  vars: {n: "the number of items, with the predicate taking constant time"}
  time: {worst: Θ(n)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, stable: true}
prereqs: [compaction, blelloch-scan, scatter-and-gather]
see_also: [all-prefix-sums, parallel-map, segmented-scan, parallel-radix-sort, parallel-quicksort, data-parallelism, decoupled-look-back-scan, counting-sort]
sources:
  - url: https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf
    title: Guy E. Blelloch, Prefix Sums and Their Applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990; also Chapter 1 of John H. Reif (editor), Synthesis of Parallel Algorithms, Morgan Kaufmann, 1993
    locator: Section 1.1 (item 8 of the list of uses, to delete marked elements from an array) and Section 1.3, Line-of-Sight and Radix-Sort (the split operation with a prescan of the flags and a permute, Figure 1.9, and its time O(n/p + lg p) on an EREW PRAM)
  - paper: doi:10.1109/12.42122
    title: Guy E. Blelloch, Scans as primitive parallel operations, IEEE Transactions on Computers 38(11), 1526 to 1538, 1989
    locator: the scan vector model, with packing and the split radix sort built from scans and a permute
  - book: isbn:9780321515261
    title: Mark Harris, Shubhabrata Sengupta and John D. Owens, Parallel Prefix Sum (Scan) with CUDA, Chapter 39 of Hubert Nguyen (editor), GPU Gems 3, Addison-Wesley, 2007
    locator: Section 39.3.1, Stream Compaction (flags, an exclusive scan of the flags, and a scatter to the scanned addresses)
  - paper: doi:10.1145/1572769.1572795
    title: Markus Billeter, Ola Olsson and Ulf Assarsson, Efficient stream compaction on wide SIMD many-core architectures, Proceedings of the Conference on High Performance Graphics 2009, 159 to 166
    locator: the three-phase method (count per block, scan the counts, write per block)
  - book: isbn:9780124159938
    title: Michael McCool, Arch D. Robison and James Reinders, Structured Parallel Programming, Morgan Kaufmann, 2012
    locator: Chapter 6, Data Reorganization (the pack pattern, its implementation with a scan, and the related split and unpack)
---

A parallel pack keeps the items of an array that satisfy a predicate, in their original order, with $\Theta(n)$ work and $\Theta(\log n)$ span. It has three steps: a [map](/parallel-map/) that sets a flag of 1 for each item to keep, an exclusive $+$-[scan](/blelloch-scan/) of the flags, which gives each kept item the number of kept items before it, and a [scatter](/scatter-and-gather/) that writes each kept item to that position. The positions are distinct, so the scatter needs only exclusive writes, and the whole algorithm runs on the EREW PRAM. This page is the work-span algorithm with its proof; the [compaction](/compaction/) page is the problem, with its other names (filter, stream compaction) and its use on GPUs.

## In plain words

A teacher wants the papers of the students who passed, in the same order as the class list, and many helpers can work at the same time.

First, every helper looks at one paper and writes 1 on it if the student passed and 0 if not. Then the helpers compute, for each paper, how many passing papers come before it. That number is the place of the paper in the new pile: the first passing paper goes to place 0, the next to place 1, and so on. Finally, every helper puts each passing paper in its place, all at once. No two papers get the same place, so nobody has to wait for anybody else.

## The problem

The input is an array $A[0 \ldots n-1]$ and a predicate keep that takes $O(1)$ time. Let $i_0 < i_1 < \cdots < i_{k-1}$ be the indices with keep$(A[i])$ true. The output is the array $B[0 \ldots k-1]$ with $B[r] = A[i_r]$. This is the [compaction](/compaction/) problem. The costs are in the [work-span model](/work-span-model/), where each parallel loop is one round.

## The algorithm

```pseudo id=main
PARALLEL-PACK(A, n, keep)
L1  for i ← 0 to n − 1 in parallel do F[i] ← 1 if keep(A[i]) else 0
L2  (X, k) ← EXCLUSIVE-SCAN(F, +, 0)      ▷ X[i] = F[0] + ⋯ + F[i − 1], k = total
L3  allocate B[0 … k − 1]
L4  for i ← 0 to n − 1 in parallel do
L5    if F[i] = 1 then B[X[i]] ← A[i]
L6  return B
```

Line L2 uses the [Blelloch scan](/blelloch-scan/), which also returns the total $k$ of the flags. The total is needed before line L3 can allocate the output, so the algorithm has a synchronization point between the scan and the scatter.

## Example

Let $A = [3, 8, 1, 6, 4, 9, 2, 7]$ and keep the even numbers.

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $A[i]$ | 3 | 8 | 1 | 6 | 4 | 9 | 2 | 7 |
| $F[i]$ | 0 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| $X[i]$ | 0 | 0 | 1 | 1 | 2 | 3 | 3 | 4 |

The total is $k = 4$. The kept items 8, 6, 4 and 2 have $X$ values 0, 1, 2 and 3, so $B = [8, 6, 4, 2]$. The items that are not kept also have $X$ values, but line L5 does not use them; item 3 at $i = 0$ has $X[0] = 0$, the same as item 8, which is why the test on the flag is needed. With $n = 8$ the algorithm does $8 + 14 + 8 = 30$ operations in $1 + 6 + 1 = 8$ rounds, which the tests check.

## Correctness

The scan gives $X[i]$ as the number of kept indices before $i$. For the kept index $i_r$, those are exactly $i_0, \ldots, i_{r-1}$, so $X[i_r] = r$. So line L5 writes $A[i_r]$ to $B[r]$ for every $r$: each cell of $B$ is written exactly once, no write leaves the array, and the order of the kept items is kept. Because the kept items have distinct positions, no two processors write the same cell. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

The field `time` of this page is the work, and the field `depth` is the span.

**Work and span.** Let $K = \lceil \lg n \rceil$ and $m = 2^K$. Line L1 does $n$ predicate tests in one round. The Blelloch scan does $2(m - 1)$ additions in $2K$ rounds. Lines L4 and L5 do $n$ steps in one round. So
$$
W = 2n + 2(m - 1) < 6n, \qquad S = 2 + 2K,
$$
which is $\Theta(n)$ work and $\Theta(\log n)$ span. The tests check both counts exactly for all $n < 300$. A greedy scheduler runs it on $p$ processors in time $T_p \le W/p + S = O(n/p + \log n)$.

**Compared with the sequential loop.** The sequential filter does $n$ tests and $k$ writes, with no extra space. The parallel pack does about three times as many operations and reads the data more than once, so it is work-efficient only up to a constant factor. It is faster when there are enough processors to pay for this.

**Blocked version.** On $p$ processors, a practical pack cuts the array into $p$ blocks. Each block counts its kept items, a scan of the $p$ counts gives each block its offset, and each block copies its kept items in order from that offset. This takes $\Theta(n + p)$ work and $O(n/p + \log p)$ time, the bound that Blelloch gives for split on an EREW PRAM. It is the method of Billeter, Olsson and Assarsson (2009) on GPUs.

**Space.** The flags and the scan take $\Theta(n)$ extra space, besides the output.

## Properties

- **Stable.** The kept items stay in their original order. This is what makes pack useful for radix sort.
- **Exclusive writes.** The positions of the kept items are distinct, so the scatter needs no CRCW rule.
- **Deterministic.** The result and the sequence of operations depend only on the input.
- **Not in place.** The output is a new array. A parallel pack inside the input array would need to avoid overwriting items that are not yet moved.

## Variants and improvements

- **Split.** Blelloch's split moves the items with flag 0 to the front and those with flag 1 to the back, both in order. It is a pack of the 0 items followed by a pack of the 1 items, done with one exclusive scan of the inverted flags, one scan in reverse order, and one permute. A split on each bit, from the lowest up, is the split radix sort; see [parallel radix sort](/parallel-radix-sort/).
- **Multiway split.** With $b$ buckets, count the items per block and bucket, scan the counts in bucket-major order, and scatter, as in a parallel [counting sort](/counting-sort/).
- **Pack of indices.** Packing the indices $i$ with $F[i] = 1$ gives the positions of the kept items, for example the segment starts of a [segmented scan](/segmented-scan/) from its flags.
- **Segmented pack.** A pack inside each segment of a segmented array, with a segmented scan in place of the plain scan, as in the quicksort of Blelloch's Section 1.5.1.
- **Single-pass GPU versions.** A GPU pack can run the scan with [decoupled look-back](/decoupled-look-back-scan/), so the data is read once and written once.
- **Unpack.** The inverse operation puts the items of $B$ back at the positions with $F[i] = 1$. It is a gather with the same scan.

## When to use it

Use a pack to delete marked items, to remove inactive items between the rounds of an iterative algorithm, to build the next frontier of a parallel breadth-first search, to drop the rays that left a scene in a ray tracer, or to collect the results of a parallel search. Use the split form for radix sort and for the partition step of [parallel quicksort](/parallel-quicksort/). For small arrays, or when only the count of kept items is needed, a sequential loop or a [reduction](/parallel-reduce/) is cheaper.

## Pitfalls

- **Inclusive scan as positions.** An inclusive scan gives each kept item its position plus 1. Using it as is writes out of range at the last kept item. The tests check this bug.
- **The total.** The number of kept items is the total of the scan, or $X[n-1] + F[n-1]$, not $X[n-1]$, which misses the last item.
- **Missing flag test.** Writing every item to $B[X[i]]$ gives write conflicts, because an item that is not kept has the same position as the next kept item.
- **Predicate called twice.** The blocked version tests each item twice, once to count and once to copy. The predicate must give the same answer both times, so it must not depend on random numbers or on shared state.
- **Memory cost.** On a GPU, each step reads or writes all of the data, and the scatter writes may not be coalesced. A pack is usually limited by memory bandwidth, not by arithmetic.

## Implementations

## History

Blelloch (1989, 1990) defined pack and split with scans and a permute in the scan vector model, listed "to delete marked elements from an array" among the uses of all-prefix-sums, and built the split radix sort and quicksort from these operations. NESL took over pack as a basic operation. On GPUs, Harris, Sengupta and Owens (2007) described stream compaction with a scan in GPU Gems 3, and Billeter, Olsson and Assarsson (2009) gave a fast blocked version for wide SIMD hardware. McCool, Robison and Reinders (2012) present pack as one of the data reorganization patterns.

## References
