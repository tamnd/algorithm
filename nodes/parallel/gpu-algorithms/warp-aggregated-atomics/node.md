---
tag: 714B67
kind: technique
slug: warp-aggregated-atomics
name: Warp-aggregated atomics
aliases:
- warp-level atomic aggregation
- aggregated atomics
area: parallel/gpu-algorithms
level: advanced
summary: The lanes of a warp that want to add to the same counter elect one leader, which does a single atomic add for the whole warp and hands each lane its own offset by a shuffle.
prereqs: [warp-level-primitives, simt-model, fetch-and-add]
see_also: [compaction, parallel-pack, histogram-computation, parallel-histogram, cooperative-groups, warp-divergence, decoupled-look-back-scan, read-modify-write]
sources:
  - url: https://developer.nvidia.com/blog/cuda-pro-tip-optimized-filtering-warp-aggregated-atomics/
    title: Andy Adinets, CUDA Pro Tip, Optimized Filtering with Warp-Aggregated Atomics, NVIDIA Technical Blog, October 2014, updated November 2017
    locator: the filtering kernel, the leader election with ballot and popc, the speedup measurements, and the remark that the compiler aggregates some atomics on its own
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 5.4.5 (atomic functions), Section 5.4.6.2 (warp vote functions) and Section 5.4.6.5 (warp shuffle functions)
  - url: https://docs.nvidia.com/cuda/archive/12.0.0/cuda-c-programming-guide/
    title: NVIDIA, CUDA C++ Programming Guide, version 12.0
    locator: Section 8.4.2.2.1, Discovery Pattern (the aggregated atomic increment with __activemask, __popc, __ffs and __shfl_sync), Section 7.19 (warp vote) and Section 7.22 (warp shuffle)
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition, Morgan Kaufmann, 2022
    locator: Chapter 9, Parallel histogram (atomic contention, privatization and aggregation)
---

Warp-aggregated atomics is a GPU technique that replaces the atomic operations of the lanes of one warp on the same address by a single atomic operation. The lanes vote to find which of them take part, the lowest such lane does one atomic add of the total, and a shuffle broadcasts the old value so that each lane can compute its own result from its rank. It turns up to 32 atomics into one, which matters most when many threads update one counter, as in stream compaction and work queues.

## In plain words

Picture a ticket desk where every person must take a numbered ticket, and the desk serves one person at a time. If a group of 32 people arrive together, they can send one person to ask for a block of tickets, as many as the group needs. That person comes back with the first number of the block. The people in the group stand in a fixed order, so each one knows how many of the group stand before them, and takes the first number plus that count. The desk now serves one request per group instead of one per person, and every person still gets a different ticket.

## When it applies

The technique applies when:

- many threads apply the same atomic read-modify-write, usually an add, to the same address, so the atomics serialize at that address;
- the operation is a [fetch-and-add](/fetch-and-add/) or another associative update whose individual results can be rebuilt from one combined result, for example $old + rank$ for an add of 1 per lane;
- the lanes that take part can find each other inside a warp, with a vote over the warp or with a match on the address.

It does not help much when the threads of a warp update different addresses with no repeats, because there is nothing to combine. It is also less needed when the compiler already aggregates the atomic on its own.

## The template

This page uses the [SIMT model](/simt-model/): warps of 32 lanes that run one instruction at a time, a global counter in device memory, and atomics on one address that are served one after another.

| symbol | meaning |
|---|---|
| $n$ | the number of threads (items) |
| $k$ | the number of threads that do an atomic update |
| $w$ | the number of warps, $\lceil n/32 \rceil$ |
| $a$ | the number of atomic operations issued |
| $p$ | the number of processors (warp schedulers) |
| $W$, $S$, $T_p$ | the work, the span and the time on $p$ processors |
| $M$, $B$ | the fast memory size and the memory transaction size |

Each lane has a predicate $keep$ that says whether it wants to add 1 to the counter.

```pseudo id=main
WARP-AGGREGATED-INCREMENT(keep, counter)     ▷ run by all 32 lanes of a warp
L1   mask ← BALLOT(keep)                          ▷ bit ℓ set iff lane ℓ takes part
     if mask = 0 then return
L2   leader ← FFS(mask) − 1                       ▷ the lowest lane that takes part
L3   if lane = leader then base ← ATOMIC-ADD(counter, POPC(mask))
L4   base ← SHFL(base, leader)                    ▷ every lane gets the old value
L5   rank ← POPC(mask AND (2^lane − 1))           ▷ lanes below this lane that take part
L6   if keep then return base + rank
```

**Why it is correct.** The leader's atomic add reserves the range $[base, base + \mathrm{popc}(mask))$ for the warp, and the atomic makes this range disjoint from the range of every other warp. Inside the warp, the ranks of the lanes that take part are $0, 1, \ldots, \mathrm{popc}(mask) - 1$ in lane order, each once, because the rank of lane $\ell$ counts the set bits below bit $\ell$. So the warp hands out each number of its range once, and the counter ends at the same value as with one atomic per lane.

**Counting the atomics.** With one atomic per lane, $a = k$. With aggregation, $a$ is the number of warps with at least one lane that takes part, so $\lceil k/32 \rceil \le a \le \min(k, w)$, and the reduction factor $k/a$ lies between 1 and 32. If each lane takes part independently with probability $q$, a full warp issues an atomic with probability $1 - (1-q)^{32}$, so
$$E[a] = w \left(1 - (1-q)^{32}\right), \qquad E[k] = 32 w q.$$
For $q = 0.5$ the factor is about 16; for $q = 0.05$ and $w = 64$, $E[a] = 64 \cdot 0.806 = 51.6$ against $E[k] = 102.4$, a factor of about 2. For $q = 0.01$ it is about 1.16. The gain is largest when many lanes of each warp take part.

**Time.** Atomics on one address are served one at a time, so their time is about $a \cdot t_{\text{atomic}}$, where $t_{\text{atomic}}$ is the service time of one atomic at the memory system. This time depends on the GPU generation and is not given here. The vote and the shuffle are warp instructions of a few cycles, and they add $O(1)$ to the span of each warp. The total work stays $\Theta(n)$.

The CUDA C++ kernel below is the standard filter, which copies the positive items of `src` to `dst` in some order. It assumes `blockDim.x` is a multiple of 32, so every warp is full and the full mask is valid. The tests do not run this CUDA code. They run the Python simulator under Classic examples.

```cuda
__global__ void filter_positive(int* dst, int* count, const int* src, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    int lane = threadIdx.x % 32;
    bool keep = (i < n) && (src[i] > 0);
    unsigned mask = __ballot_sync(0xffffffffu, keep);          // L1
    if (mask == 0) return;                                     // same for all lanes
    int leader = __ffs(mask) - 1;                              // L2
    int base = 0;
    if (lane == leader) base = atomicAdd(count, __popc(mask)); // L3
    base = __shfl_sync(0xffffffffu, base, leader);             // L4
    if (keep) {
        int rank = __popc(mask & ((1u << lane) - 1u));         // L5
        dst[base + rank] = src[i];                             // L6
    }
}
```

When the call site is inside divergent code, the warp does not know which lanes reach it. The form below, close to the discovery pattern of the CUDA 12.0 guide, uses the lanes that are active at the call. With Cooperative Groups, `coalesced_threads()` gives the same group with `thread_rank()`, `size()` and `shfl()`.

```cuda
__device__ int atomic_agg_inc(int* ctr) {
    unsigned active = __activemask();
    int lane = threadIdx.x % 32;
    int leader = __ffs(active) - 1;
    int base = 0;
    if (lane == leader) base = atomicAdd(ctr, __popc(active));
    base = __shfl_sync(active, base, leader);
    return base + __popc(active & ((1u << lane) - 1u));
}
```

## Classic examples

- **Stream compaction (filtering).** Each thread that keeps its item needs a slot in the output, so it increments a global counter; this is the kernel above and the example of Adinets (2014). The output order is not the input order, because warps reach the counter in any order. When the order must be kept, use a scan-based [compaction](/compaction/) or [parallel pack](/parallel-pack/), or the [decoupled look-back scan](/decoupled-look-back-scan/). The simulator runs the filter with per-thread atomics and with aggregation. For 50 full warps in which all items pass, it counts 1600 atomics against 50.
- **Work queues.** In GPU breadth-first search and other frontier methods, each thread that finds new work appends to a global queue with an atomic on the tail index. Aggregation reserves one block of queue slots per warp.
- **Histograms with few bins.** When the lanes add to several counters, `__match_any_sync` (compute capability 7.0 and higher) groups the lanes by bin, and the lowest lane of each group adds the group size. The number of atomics drops from $n$ to the sum over warps of the number of distinct bins in the warp. This complements privatization in shared memory, as in [parallel histogram](/parallel-histogram/) and [histogram computation](/histogram-computation/).
- **Bump allocation.** A device-side allocator that hands out memory from a pool by advancing a pointer can reserve the total size for the warp with one atomic, and give each lane an offset from an exclusive [warp scan](/warp-level-primitives/) of the sizes.

## Variations

- **Different amounts per lane.** If lane $\ell$ adds $v_\ell$ instead of 1, the leader adds the warp sum of the $v_\ell$, and each lane adds the exclusive warp scan of the $v$ values to $base$. The rank by `popc` is the special case $v_\ell \in \{0, 1\}$.
- **Block-level aggregation.** Combine first in shared memory over the whole block, then do one atomic per block. This cuts the global atomics further, at the cost of a barrier.
- **Other operations.** Any atomic whose per-lane result can be rebuilt works: max, min, and the bitwise operations, if the lanes do not need their own old values, or if the lanes are ordered as for the add. Compare-and-swap loops cannot be aggregated in the same way.
- **Compiler aggregation.** Adinets reports that NVCC aggregates simple atomic increments on its own in many cases, from CUDA 7.5 for GPUs after Kepler and from CUDA 9 for Kepler. Write the explicit form when the pattern is not simple, or check the generated code.

## Pitfalls

- **Wrong mask with `_sync` intrinsics.** `__ballot_sync(0xffffffff, ...)` requires all 32 lanes to execute it. A partial last warp, or an early `return` by some lanes before the vote, gives undefined behaviour. Compute the predicate with `i < n` instead of returning early, or use `__activemask()`.
- **Assuming the lanes are converged.** `__activemask()` returns the lanes that run together at that moment, which can be fewer than all the lanes that will reach the call. The result is still correct, because each group reserves its own range, but the aggregation is weaker. Since the Volta generation, independent thread scheduling makes this more likely.
- **Expecting ordered output.** The base of each warp depends on the order in which warps reach the counter. The output is a permutation of the kept items, which differs between runs.
- **Using a private intrinsic.** Some example code uses `__lanemask_lt()`, which is not part of the documented CUDA API. Write `(1u << lane) - 1u`, or read the `%lanemask_lt` register with inline PTX.
- **No contention, no gain.** If every warp has only one lane that takes part, aggregation adds the vote and the shuffle and saves nothing.

## Exercises

1. Show that $\lceil k/32 \rceil \le a \le \min(k, \lceil n/32 \rceil)$ for the number of aggregated atomics, and give inputs that reach each bound.
2. For lanes that take part with probability $q$ each, find the value of $q$ for which aggregation halves the expected number of atomics. (Solve $32q = 2(1 - (1-q)^{32})$ numerically.)
3. Change the filter so that lane $\ell$ writes $c_\ell \in \{0, 1, 2, 3\}$ output items. Use a warp scan with `__shfl_up_sync` for the offsets.
4. Write the `__match_any_sync` histogram for 8 bins and count its atomics for a warp whose keys are $0, 1, \ldots, 7$ repeated four times.
5. Explain why the filter above can produce a different output order in two runs on the same input, and why the set of output items is always the same.

## References
