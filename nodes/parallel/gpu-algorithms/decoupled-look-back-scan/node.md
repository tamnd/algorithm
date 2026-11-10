---
tag: T9HRJ5
kind: algorithm
slug: decoupled-look-back-scan
name: Decoupled look-back scan
aliases:
- single-pass GPU scan
- single-pass prefix scan with decoupled look-back
area: parallel/gpu-algorithms
level: advanced
summary: A single-pass GPU prefix scan in which each block publishes its tile total, then looks back over earlier tiles to find its prefix, so about 2n items move through memory.
solves: [all-prefix-sums]
model: simt-model
complexity:
  vars: {n: the number of items, b: the number of items per tile, p: the number of thread blocks resident at once}
  time: {worst: Θ(n)}
  depth: {worst: O(b + n/b)}
  space: {extra: O(n/b)}
properties: {deterministic: false}
prereqs: [all-prefix-sums, parallel-reduce, simt-model]
see_also: [blelloch-scan, hillis-steele-scan, segmented-scan, compaction, parallel-pack, fetch-and-add, memory-coalescing, warp-level-primitives]
sources:
  - url: https://research.nvidia.com/sites/default/files/pubs/2016-03_Single-pass-Parallel-Prefix/nvr-2016-002.pdf
    title: Duane Merrill and Michael Garland, Single-pass Parallel Prefix Scan with Decoupled Look-back, NVIDIA Technical Report NVR-2016-002, March 2016
    locator: Section 4.1 (the protocol and its three properties), Section 4.4 (the dynamic partition index, fence-free descriptor updates and the parallel look-back), and the comparison of the data movement of reduce-then-scan, scan-then-propagate and chained scan
  - paper: doi:10.1145/2442516.2442539
    title: Shengen Yan, Guoping Long and Yunquan Zhang, StreamScan, fast scan algorithms for GPUs without global barrier synchronization, PPoPP 2013, 229 to 238
    locator: the chained scan with adjacent synchronization between blocks
  - book: isbn:9780321515261
    title: Mark Harris, Shubhabrata Sengupta and John D. Owens, Parallel Prefix Sum (Scan) with CUDA, Chapter 39 of Hubert Nguyen (editor), GPU Gems 3, Addison-Wesley, 2007
    locator: Section 39.2.4, Arrays of Arbitrary Size (the multi-pass scan of block sums)
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition, Morgan Kaufmann, 2022
    locator: Chapter 11, Prefix sum (scan), the sections on hierarchical scan and single-pass scan
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 5.4.5, Atomic Functions
---

The decoupled look-back scan is a single-pass [prefix scan](/all-prefix-sums/) for GPUs, due to Merrill and Garland (2016). Each thread block takes a tile, publishes the total of its tile, and then reads the published values of the tiles before it until it reaches one that already knows its full prefix. The input is read once and the output is written once, so the scan moves about $2n$ items through global memory, against about $3n$ for the usual reduce-then-scan. A tile index taken with an atomic counter makes the method free of deadlock.

## In plain words

A long line of people each hold a number, and each person wants the total of everyone up to and including themself. The line is cut into teams. Each team first adds up its own numbers and writes the team total on a board. Then the team walks back along the board. If the team before it has written its full running total, the walk ends there. If that team has only written its own team total, the walking team adds it and keeps walking back. If a team has written nothing yet, the walking team waits a moment. When a team knows its running total, it writes that on the board too, so later teams can stop early. Each team reads its numbers once and writes its answers once.

## The problem

The input is an array $A[0 \ldots n-1]$ in GPU global memory and an [associative operator](/associative-operator/) $\oplus$. The output is the inclusive scan $Out[i] = A[0] \oplus \cdots \oplus A[i]$. The operator need not be commutative. The cost model is the [SIMT model](/simt-model/): thread blocks of threads in warps of 32, a fixed number $p$ of blocks resident at once, and a scan that is limited by the bandwidth of global memory, so the main cost is the number of items read and written.

The array is cut into $t = \lceil n/b \rceil$ tiles of $b$ items. Write $T_g$ for the reduction of tile $g$ (its aggregate) and $I_g = T_0 \oplus \cdots \oplus T_g$ for its inclusive prefix. Each tile has a descriptor in global memory with a flag and a value. The flag is $X$ (nothing is known yet), $A$ (the value is the aggregate $T_g$) or $P$ (the value is the inclusive prefix $I_g$). All descriptors start as $X$.

## The algorithm

Every thread block runs the code below once. PUBLISH writes a flag and a value as one indivisible store, and READ loads both as one load. In the pseudocode, $v \oplus \text{none} = v$.

```pseudo id=main
LOOK-BACK-SCAN-BLOCK(A, Out, n, b, ⊕)       ▷ run by every thread block
L1   g ← ATOMIC-ADD(counter, 1)                 ▷ dynamic tile index
L2   T ← A[g·b .. min(n, (g + 1)·b) − 1]        ▷ the only read of A
L3   agg ← REDUCE(T, ⊕)                         ▷ block-wide reduce
L4   if g = 0 then
L5     PUBLISH(desc[0], P, agg); excl ← none
L6   else
L7     PUBLISH(desc[g], A, agg)                 ▷ tell later tiles the aggregate
L8     j ← g − 1; excl ← none
L9     loop                                     ▷ the look-back
L10      (f, v) ← READ(desc[j])
L11      if f = X then go to L10                ▷ tile j has published nothing yet
L12      excl ← v ⊕ excl                        ▷ v covers items before excl
L13      if f = P then exit loop
L14      j ← j − 1
L15    PUBLISH(desc[g], P, excl ⊕ agg)
L16  Out[g·b + k] ← excl ⊕ T[0] ⊕ ⋯ ⊕ T[k] for each k ▷ block-wide scan
```

Lines L2, L3 and L16 are parallel work inside one block: a coalesced load, a [block reduce](/parallel-reduce/) and a block scan such as the [Blelloch scan](/blelloch-scan/) in shared memory. The look-back in lines L8 to L14 is short serial work by one thread or one warp. The paper describes it with one more step: the block of tile 0 copies its aggregate to the inclusive prefix and skips the look-back, which is lines L4 and L5.

The essential points are three. A block publishes its aggregate on line L7 *before* it looks back, so its successors never wait for its look-back to finish; this decoupling is the difference from a chained scan. A predecessor with flag $A$ lets the look-back continue past it; only a predecessor with flag $X$ makes it wait. The index on line L1 comes from an atomic counter, not from the hardware block index, which is what rules out deadlock.

The CUDA C++ kernel below is a short version for `int` with $+$. The flag and a 32-bit value share one 64-bit word, so a single atomic store publishes both and no memory fence is needed between them, as in Section 4.4 of the paper. The block scan is a [Hillis-Steele scan](/hillis-steele-scan/) to keep the code short; real code uses a work-efficient block scan, for example CUB's `BlockScan`. The tests on this page do not run this CUDA code. They run the Python simulator described under Implementations.

```cuda
constexpr unsigned long long FLAG_X = 0ull;            // nothing published
constexpr unsigned long long FLAG_A = 1ull << 32;      // aggregate available
constexpr unsigned long long FLAG_P = 2ull << 32;      // inclusive prefix available
constexpr unsigned long long FLAG_MASK = 0xFFFFFFFF00000000ull;

__device__ unsigned int tile_counter;   // set to 0 before every launch

__device__ unsigned long long pack(unsigned long long flag, int v) {
    return flag | (unsigned int)v;
}

// desc has one word per tile, set to 0 (FLAG_X) before every launch.
// Launch with blockDim.x == BLOCK and gridDim.x == ceil(n / BLOCK).
template <int BLOCK>
__global__ void look_back_scan(const int* in, int* out, int n,
                               unsigned long long* desc) {
    __shared__ unsigned int s_tile;
    __shared__ int s_excl;
    __shared__ int s[BLOCK];
    if (threadIdx.x == 0) s_tile = atomicAdd(&tile_counter, 1u);  // L1
    __syncthreads();
    const unsigned int g = s_tile;
    const int i = g * BLOCK + threadIdx.x;
    s[threadIdx.x] = (i < n) ? in[i] : 0;                           // L2
    __syncthreads();
    for (int d = 1; d < BLOCK; d <<= 1) {                           // tile scan
        int v = (threadIdx.x >= d) ? s[threadIdx.x - d] : 0;
        __syncthreads();
        s[threadIdx.x] += v;
        __syncthreads();
    }
    const int agg = s[BLOCK - 1];                                   // L3
    if (threadIdx.x == 0) {
        int excl = 0;
        if (g == 0) {
            atomicExch(&desc[0], pack(FLAG_P, agg));                // L5
        } else {
            atomicExch(&desc[g], pack(FLAG_A, agg));                // L7
            for (int j = g - 1;; --j) {                             // L9 to L14
                unsigned long long d;
                do {
                    d = atomicAdd(&desc[j], 0ull);                  // atomic read
                } while ((d & FLAG_MASK) == FLAG_X);
                excl += (int)(unsigned int)d;
                if ((d & FLAG_MASK) == FLAG_P) break;
            }
            atomicExch(&desc[g], pack(FLAG_P, excl + agg));         // L15
        }
        s_excl = excl;
    }
    __syncthreads();
    if (i < n) out[i] = s_excl + s[threadIdx.x];                    // L16
}
```

## Example

Take $A = [3, 1, 4, 1, \; 5, 9, 2, 6, \; 5, 3, 5, 8, \; 9, 7, 9, 3]$ with $+$ and tiles of $b = 4$, so $t = 4$ and the aggregates are $T = (9, 22, 21, 28)$. Four blocks take the indices 0 to 3 in that order, but they run at different speeds. The descriptors are written as flag:value.

| step | event | desc[0] | desc[1] | desc[2] | desc[3] |
|---|---|---|---|---|---|
| 0 | start | X | X | X | X |
| 1 | tiles 2 and 3 publish their aggregates | X | X | A:21 | A:28 |
| 2 | tile 3 reads desc[2] = A:21, so excl = 21, and moves to desc[1] | X | X | A:21 | A:28 |
| 3 | tile 3 reads desc[1] = X and waits | X | X | A:21 | A:28 |
| 4 | tile 0 publishes its prefix | P:9 | X | A:21 | A:28 |
| 5 | tile 1 publishes A:22, reads desc[0] = P:9, publishes $9 + 22$ | P:9 | P:31 | A:21 | A:28 |
| 6 | tile 3 reads desc[1] = P:31, so excl = $31 + 21 = 52$, publishes $52 + 28$ | P:9 | P:31 | A:21 | P:80 |
| 7 | tile 2 reads desc[1] = P:31, publishes $31 + 21$ | P:9 | P:31 | P:52 | P:80 |

Tile 3 did not wait for tile 2 to finish its look-back: it used the aggregate 21 and went on to tile 1. Each tile then scans its own items from its exclusive prefix, for example tile 3 from 52: $61, 68, 77, 80$. The full output is $[3, 4, 8, 9, 14, 23, 25, 31, 36, 39, 44, 52, 61, 68, 77, 80]$. The 16 items were read once and written once, and $2t - 1 = 7$ descriptors were published.

## Correctness

The full proof is in the proofs file. It rests on three hypotheses: PUBLISH and READ move the flag and the value together, the tile index comes from an atomic counter, and every resident block makes progress. Under them:

- **Values.** A descriptor with flag $A$ holds $T_g$ and one with flag $P$ holds $I_g$, and flags only move forward. By induction on the time of the writes, a look-back that passes tiles $g-1, \ldots, k+1$ with flag $A$ and stops at tile $k$ with flag $P$ computes $I_k \oplus T_{k+1} \oplus \cdots \oplus T_{g-1} = I_{g-1}$. Line L12 puts each new value on the left, so the order of the operands is right for a non-commutative $\oplus$.
- **No deadlock.** Take the smallest tile index that is taken but not finished. All smaller tiles have finished and published $P$, so this tile never waits, and it finishes. With the hardware block index in place of the counter, a resident block can wait for a tile whose block is not yet resident while all slots are full. The hardware does not promise any dispatch order, so this can happen; the simulator finds such runs.
- **Bounded look-back.** When tile $g$ takes its index, all smaller indices are already taken, and at most $p - 1$ of them are still held by resident blocks. So one of the tiles $g-1, \ldots, g-p$ has finished and published $P$, and the look-back reads at most $p$ descriptors. Merrill and Garland list this as the constant-bound look-back property.

## Complexity

The page uses this notation.

| symbol | meaning |
|---|---|
| $n$ | the number of items |
| $b$ | the number of items per tile, $t = \lceil n/b \rceil$ tiles |
| $p$ | the number of thread blocks resident at once (the processors) |
| $W$, $S$, $T_p$ | the work, the span and the time on $p$ processors |
| $M$, $B$ | the fast memory size and the memory transaction size |

The cost model is the [SIMT model](/simt-model/) with warps of 32 and the [roofline model](/roofline-model/): a scan does one $\oplus$ per item and one or two memory transfers per item, so its [arithmetic intensity](/arithmetic-intensity/) is far below the ridge point of every current GPU, and its time is the number of bytes moved divided by the memory bandwidth.

**Data movement.** Each item is read once on line L2 and written once on line L16, which is $2n$ item transfers. The descriptors add $2t - 1$ stores and at most $p$ loads per tile, not counting failed polls, so the total is $2n + O(tp) = 2n + O(np/b)$. A reduce-then-scan reads the input in a first pass to reduce each tile, scans the $t$ tile sums, then reads the input again and writes the output. Counted exactly (as the tests do), it reads $2n + 2t - 1$ values and writes $n + 2t$, which is $3n + 4t - 1$. A scan-then-propagate writes a partial scan and then reads and writes it again, about $4n$. For $n = 10^8$ items of 4 bytes, the single pass moves 800 MB and the reduce-then-scan 1200 MB. At an assumed bandwidth of 1000 GB/s, which is a round number for the example and not the figure of a given GPU, that is 0.8 ms against 1.2 ms. Bandwidths differ between GPU generations, but the ratio $2 : 3$ does not.

**Work.** The block reduces and scans do $\Theta(n)$ applications of $\oplus$, and the look-back adds at most $p$ per tile, so $W = n + O(np/b) = \Theta(n)$ when $b \ge p$. A sequential scan does $n - 1$.

**Span.** With unbounded resident blocks, a tile does $O(b)$ serial work in the simplest code, or $O(\log b)$ with a work-efficient block scan, and its look-back reads at most $t - 1 = O(n/b)$ descriptors one after another. The span is $O(b + n/b)$ for the simple code, which is $O(\sqrt{n})$ at $b = \sqrt{n}$. On a real GPU $p$ is bounded, so the look-back reads at most $p$ descriptors, and with a window of 32 threads it reads 32 descriptors per step.

**Time.** A tile does not wait for the full look-back of its predecessor, only for its predecessor to publish an aggregate, which happens right after the tile is loaded and reduced. In a chained scan, tile $g$ waits for tile $g-1$ to publish its inclusive prefix, so the waits form a chain of length $t$ in which each link is one global memory round trip. The decoupled form shortens the critical path to about one look-back per tile.

**Space.** One descriptor per tile, $O(n/b)$ words, and one counter. Both must be reset before each launch.

## Properties

- **Single pass.** The input is read once. This is the minimum for a scan, and it makes the method about $3/2$ times faster than reduce-then-scan when both are bound by memory bandwidth.
- **In place.** Each tile reads all of its items before it writes any, and no tile reads another tile's items, so $Out$ may be the same array as $A$.
- **Not deterministic in its bracketing.** Where the look-back stops depends on timing, so the bracketing of the $\oplus$ operations changes from run to run. For integers this does not matter. For floating-point addition, which is not associative, the results can differ in the last bits between runs; Merrill and Garland point this out for their implementation. The front matter marks the method as not deterministic for this reason.
- **Order-keeping.** With line L12 as written, $\oplus$ need not be commutative. The tests check string concatenation.
- **Bounded look-back.** At most $p$ descriptors per tile, so the extra traffic does not grow with $n/b$.
- **Needs atomics and progress.** It needs an atomic increment for the counter, an atomic or fenced descriptor update, and the forward progress of resident blocks.

## Variants and improvements

- **Chained scan.** Yan, Long and Zhang (2013) chain the blocks: block $g$ waits for the inclusive prefix of block $g-1$, adds its own aggregate and passes it on. This also moves about $2n$ items, but the serial chain of waits limits it. The tests run this mode in the simulator too.
- **Parallel look-back.** Merrill and Garland let a whole warp read a window of 32 descriptors at once, use a warp vote to find the nearest $P$, and reduce the window with [warp-level primitives](/warp-level-primitives/). The simulator has a window parameter for this.
- **Fence-free descriptors.** When the value fits beside the flag in one machine word, as in the CUDA code above, one atomic store publishes both. For larger values the code must store the value, issue a memory fence, and then store the flag.
- **Other single-pass operations.** The same tile protocol drives [stream compaction](/compaction/) and [parallel pack](/parallel-pack/), run-length encoding, and the single-pass radix sort Onesweep of Adinets and Merrill (2022), which uses decoupled look-back for its digit histograms.
- **Segmented scan.** With the segmented operator in place of $\oplus$, the same code computes a [segmented scan](/segmented-scan/).

## When to use it

Use it for large scans on a GPU, where the scan is limited by memory bandwidth and the number of passes over the data sets the time. It is the method behind the device-wide scan of NVIDIA's CUB library. For a scan inside one thread block, use a block scan such as the [Blelloch scan](/blelloch-scan/) or the [Hillis-Steele scan](/hillis-steele-scan/) instead, because there is nothing to look back at. On hardware without forward progress for resident blocks, or without fast global atomics, use reduce-then-scan.

## Pitfalls

- **Using `blockIdx.x` as the tile index.** The code then depends on the order in which the hardware starts blocks. That order is not promised, and the result is a rare deadlock. Take the index from an atomic counter.
- **Forgetting to reset the counter and the descriptors.** Both must be zero at every launch. A second launch without a reset reads stale $P$ flags and gives wrong results without any error.
- **Torn or reordered descriptors.** If the flag and the value are separate words, a reader can see the new flag with the old value. Pack them, or put a fence between the two stores, and read with a load that the compiler cannot cache, such as an atomic or a volatile load.
- **Operand order in the look-back.** Adding the predecessor's value on the right of $excl$ works for $+$ but gives wrong results for non-commutative operators.
- **Expecting bitwise-equal floating-point results.** The bracketing depends on timing. Use an integer or fixed-point type, or a reduce-then-scan with a fixed tree, when runs must match bit for bit.
- **Small tiles.** The descriptor traffic is $O(np/b)$ and each look-back step is a global memory round trip, so tiles must hold many items per thread for the single pass to pay off.

## Implementations

The Python file is a simulator, not a GPU program. Each thread block is a Python generator that yields after each step that touches global memory, and a scheduler picks the next resident block with a seeded `random.Random`. The hardware dispatch order is also a seeded shuffle, and at most $p$ blocks are resident at a time. The simulator counts item reads and writes, descriptor writes and reads, failed polls and atomics, and it reports a deadlock when every resident block waits on a descriptor that no running block can change. The tests check the output against `itertools.accumulate` on random sizes and orders, the counts $n$ reads and $n$ writes, $2t - 1$ descriptor writes, at most $p$ descriptors per look-back, the $3n + 4t - 1$ count of reduce-then-scan, and that the static block index deadlocks in some seeded runs while the dynamic index never does.

## History

GPU scans first ran in several passes: Harris, Sengupta and Owens (2007) scanned each block in shared memory, scanned the block sums in a second kernel, and added the sums back in a third. Yan, Long and Zhang (2013) removed the extra passes with StreamScan, which chains adjacent blocks through global memory. Merrill and Garland (2016) decoupled the publication of a block's aggregate from the computation of its prefix, which removed the serial chain, and they used a dynamic tile index to make the method safe under any dispatch order. The method is part of the CUB library and of the device-wide scans built on it.

## References
