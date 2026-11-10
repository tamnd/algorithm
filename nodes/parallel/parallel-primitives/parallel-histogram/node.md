---
tag: DG02CV
kind: algorithm
slug: parallel-histogram
name: Parallel histogram
aliases:
- privatized histogram
- reduce-by-key
area: parallel/parallel-primitives
level: core
summary: Count n keys into k bins in parallel. Each of p blocks counts into its own bins, and a tree of parallel adds merges them, with n + 3pk - 2k work and O(n/p + k + log p log k) span.
solves: [histogram-computation]
model: work-span-model
complexity:
  vars: {n: the number of items, k: the number of bins, p: the number of blocks}
  time: {worst: Θ(n + p k)}
  depth: {worst: Θ(n/p + k + log p log k)}
  space: {extra: Θ(p k)}
properties: {deterministic: true, recursive: true, in_place: false}
prereqs: [fork-join-model, work-span-model, parallel-reduce, histogram-computation]
see_also: [parallel-reduction, counting-sort, image-histogram, word-count, warp-aggregated-atomics, shared-memory-tiling, fork-join-parallelism, segmented-scan]
sources:
  - book: isbn:9780323912310
    title: David B. Kirk, Wen-mei W. Hwu and Izzat El Hajj, Programming Massively Parallel Processors, 4th edition, Morgan Kaufmann, 2022
    locator: Chapter 9, parallel histogram (atomic operations and privatization)
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 3rd edition, MIT Press, 2009
    locator: Chapter 27, Section 27.1 (the work-span model, spawn, sync and parallel loops)
---

A parallel histogram counts how many of $n$ items fall into each of $k$ bins, with many processors at once and no locks. The privatized form on this page cuts the input into $p$ blocks. Each block is counted in sequence into its own array of $k$ bins, so no two tasks write the same counter. Then a balanced tree of [fork-join](/fork-join-parallelism/) merges adds the arrays up, each merge a parallel loop over the bins. The work is exactly $n + 3pk - 2k$ and the span is exactly $\lceil \lg p \rceil(\lceil \lg k \rceil + 2) + k + \lceil n/p \rceil$ in the cost model of this page. The number of blocks sets the trade-off: few blocks give little work and a long span, and many blocks give a short span but $pk$ counters to merge.

Notation on this page: $x[0 \ldots n-1]$ is the input, with each key in $\{0, \ldots, k-1\}$. $p$ is the number of blocks, and each block has $s = \lceil n/p \rceil$ consecutive items, except at the end. $H$ is a histogram, an array of $k$ counters. $W$ is the work and $S$ the span in the [work-span model](/work-span-model/). $\lg$ is $\log_2$.

## In plain words

Many people must count votes for a few candidates. If all of them make marks on one sheet, they must wait for each other at the sheet.

So give each person a part of the votes and a sheet of their own. Each person counts their part alone, with no waiting.

Then the sheets are added up in pairs. Two people add their sheets, line by line, into one sheet. Then two of the new sheets are added, and so on, until one sheet is left.

More people make the counting part shorter. But each person needs a full sheet, so more people also make more sheets to add up.

## The problem

The input is an array $x$ of $n$ keys from $\{0, \ldots, k-1\}$. The output is the array $H$ with $H[j] = |\{ i : x[i] = j \}|$ for each $j$. This is the [histogram computation](/histogram-computation/) problem, which also lists the other methods. The sequential loop does $n$ additions, but in parallel the additions go to only $k$ counters, so when $k$ is small many tasks want the same counter at the same time.

## The algorithm

```pseudo id=main
PRIVATE-HISTOGRAM(x, lo, hi, k)           ▷ the histogram of the blocks lo, ..., hi - 1 of x
L1  if hi - lo = 1 then
L2      H ← a new array of k zeros
L3      for each item v of block lo do H[v] ← H[v] + 1
L4      return H
L5  mid ← ⌈(lo + hi) / 2⌉                  ▷ the left half gets the extra block
L6  H ← spawn PRIVATE-HISTOGRAM(x, lo, mid, k)
L7  G ← PRIVATE-HISTOGRAM(x, mid, hi, k)
L8  sync
L9  parallel for j ← 0 to k - 1 do H[j] ← H[j] + G[j]
L10 return H
```

The call PRIVATE-HISTOGRAM(x, 0, p, k) gives the histogram of $x$. Lines L1 to L4 are the private counting: the loop of line L3 runs in sequence, but on a private array, so it needs no atomic operation. Lines L5 to L10 are a [parallel reduce](/parallel-reduce/) of the $p$ arrays, with the addition of arrays as the operator.

## Example

Count $x = [2, 0, 1, 2, 2, 3, 0, 2, 1, 3]$ with $n = 10$, $k = 4$ and $p = 4$ blocks of $s = 3$ items.

| call | blocks | result | work | span |
|---|---|---|---|---|
| leaf, line L3 | $[2, 0, 1]$ | $[1, 1, 1, 0]$ | 7 | 7 |
| leaf, line L3 | $[2, 2, 3]$ | $[0, 0, 2, 1]$ | 7 | 7 |
| leaf, line L3 | $[0, 2, 1]$ | $[1, 1, 1, 0]$ | 7 | 7 |
| leaf, line L3 | $[3]$ | $[0, 0, 0, 1]$ | 5 | 5 |
| merge, line L9 | blocks 0 and 1 | $[1, 1, 3, 1]$ | 8 | 4 |
| merge, line L9 | blocks 2 and 3 | $[1, 1, 1, 1]$ | 8 | 4 |
| merge, line L9 | all | $[2, 2, 4, 2]$ | 8 | 4 |

A leaf costs $k$ for the zeros and one step per item. A merge costs 1 for the spawn and $2k - 1 = 7$ for the parallel loop, and adds $1 + \lceil \lg k \rceil + 1 = 4$ to the span. The total work is $26 + 3 \cdot 8 = 50 = n + 3pk - 2k$, and the span is $7 + 4 + 4 = 15$, along the leftmost leaf, which holds the largest block.

## Correctness

The blocks are disjoint and cover $x$, so each item is counted in exactly one leaf. By induction on the number of blocks, a call returns the counts of its blocks: a leaf counts its own block, and line L9 adds the counts of two disjoint ranges of blocks. The two calls of lines L6 and L7 write only arrays that they make themselves, and iteration $j$ of line L9 touches only $H[j]$ and $G[j]$, so there is no [determinacy race](/determinacy-race/), and the result is the same for each schedule. The [full proof](proofs/correctness.md) has the details.

## Complexity

The [complexity proof](proofs/complexity.md) has the details. A step costs 1, line L2 costs $k$, and a group of $r$ parallel tasks adds $r - 1$ to the work and $\lceil \lg r \rceil$ to the span.

- **Work.** The $p$ leaves cost $pk + n$, and each of the $p - 1$ merges costs $2k$. So $W = n + 3pk - 2k = \Theta(n + pk)$.
- **Span.** Each level of the tree adds $\lceil \lg k \rceil + 2$, and the leftmost leaf is the deepest and has the largest block. So $S = \lceil \lg p \rceil(\lceil \lg k \rceil + 2) + k + \lceil n/p \rceil$.
- **The choice of p.** With $p = \lceil n/k \rceil$, the work is at most $4n + 3k$ and the span is at most $2k + \lceil \lg n \rceil(\lceil \lg k \rceil + 2)$. So for a fixed number of bins the method has linear work and a span of $O(\log n)$.
- **The limit of the method.** $W \ge pk$ and $S \ge n/p$, so $W \cdot S \ge nk$. Linear work forces a span of $\Omega(k)$. For a large $k$, use one of the other methods of [histogram computation](/histogram-computation/).
- **Space.** A parallel run holds up to $pk$ counters. A run on one processor holds at most $(\lceil \lg p \rceil + 1)k$.

The tests check both formulas with equality on 800 random inputs. Two measured cases for $n = 10^6$: with $k = 256$, the choice $p = 64$ gives $W = 1048640$ and $S = 15941$, and $p = 3906$ gives $W = 3999296$ and $S = 633$. With $k = 16$ and $p = 62500$, the span is 128.

## Properties

- **Deterministic.** The counts are integers and each counter has one writer at a time, so the result does not depend on the schedule. For floating point weights, the fixed tree also fixes the order of the additions.
- **No atomic operations.** The private arrays remove all contention, whatever the distribution of the keys.
- **Not sensitive to skew.** The cost does not change when all keys are the same, which is the worst case for shared atomic counters.
- **Not in place.** It needs $\Theta(pk)$ counters beside the input.

## Variants and improvements

- **Shared counters with atomics.** All tasks add to one array with an atomic [fetch and add](/fetch-and-add/). The work is $\Theta(n + k)$, but the additions to one counter run one after the other, so the span is at least $\max_j H[j]$, which is $n$ when all keys are the same.
- **Merge by bins.** In place of the tree of line L9, the $k$ bins can be summed one at a time over the $p$ arrays, as $k$ parallel reductions of $p$ numbers. The work is of the same order, and the span of the merge is $O(\log p + \log k)$, not $O(\log p \log k)$.
- **Sort and segment.** Sort the keys, for example by [radix sort](/radix-sort/), and count the length of each run of equal keys with a [segmented scan](/segmented-scan/). The work does not depend on $p k$, so this suits a large $k$.
- **Keyed values.** Any associative and commutative operator works in place of $+ 1$, for example the sum or the maximum of values attached to the items, which is the core of [word count](/word-count/) in MapReduce.
- **On a GPU.** Each thread block keeps a private histogram in shared memory, adds to it with fast shared memory atomics, and adds it to the global histogram with one atomic per bin at the end; see [warp aggregated atomics](/warp-aggregated-atomics/), [shared memory tiling](/shared-memory-tiling/), [shared memory bank conflicts](/shared-memory-bank-conflicts/), [occupancy](/occupancy/) and the [SIMT model](/simt-model/). The sketch below is in CUDA and is not run by the tests.

```cuda
__global__ void hist(const unsigned char *x, int n, unsigned int *h) {
    __shared__ unsigned int s[256];                  // private bins of this block
    for (int j = threadIdx.x; j < 256; j += blockDim.x) s[j] = 0;
    __syncthreads();
    for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n; i += gridDim.x * blockDim.x)
        atomicAdd(&s[x[i]], 1);                       // contention only inside the block
    __syncthreads();
    for (int j = threadIdx.x; j < 256; j += blockDim.x)
        if (s[j]) atomicAdd(&h[j], s[j]);             // one global add per bin and block
}
```

The loop with a stride of the whole grid reads $x$ with [coalesced](/memory-coalescing/) accesses, and the number of thread blocks plays the part of $p$.

## When to use it

- Use it when $k$ is small compared with $n/p$, for example 256 bins for the bytes of an image or a file, or a few dozen buckets for one pass of a radix sort.
- Use it when the keys can be skewed, since the private arrays make the cost the same for each distribution.
- Use it when the result must be the same on each run, for example with floating point weights.
- Do not use it when $k$ is close to $n$ or larger. Then the $pk$ counters cost more than the counting; sort and segment, or use shared atomics, which have little contention when the keys spread over many bins.

## Pitfalls

- **Too many blocks.** Each block costs $k$ at line L2 and $2k$ at line L9, so with $p > n/k$ the merges cost more than the counting. Choose $p$ near $n/k$ or less.
- **A shared array at line L2.** If the leaves share one array, the additions of line L3 race and counts are lost. The array must be new in each leaf, or the additions must be atomic.
- **Merging in the wrong array.** Line L9 must add into an array that only this call owns. If it adds into a third array shared by other merges, the merges race.
- **Uneven blocks.** If the split of line L5 gives the larger part to the right, the span grows, and blocks of very different sizes make the longest leaf set the span. Cut blocks of equal size.
- **Keys out of range.** Line L3 writes $H[v]$ for each key $v$, so a key outside $\{0, \ldots, k-1\}$ writes outside the array. The implementation checks the keys first.

## Implementations

## History

Counting into private copies and then combining them is the reduction pattern for any associative and commutative update, and it is as old as parallel reductions. On GPUs, where atomics on a few hot bins were slow, the private histogram in shared memory became the standard method, and textbooks such as Kirk, Hwu and El Hajj present it as the main example of privatization. Faster atomics in later GPUs reduced the gap but did not remove the gain for skewed keys.

## References
