---
tag: 4V6VYK
kind: concept
slug: cooperative-groups
name: Cooperative groups
aliases:
- CUDA cooperative groups
area: parallel/gpu-algorithms
level: advanced
summary: A CUDA API that names groups of threads (block, tiles of a block, the active lanes, the grid) as objects with sync and collectives; grid.sync() needs a cooperative launch with all blocks resident.
prereqs: [cuda-programming-model, warp-level-primitives, occupancy]
see_also: [thread-block-and-grid, persistent-threads, barrier-synchronization, parallel-reduce, decoupled-look-back-scan, warp-divergence, bsp-model]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 4.4 (cooperative groups), 4.4.2 (group handles, thread_rank and num_threads), 4.4.4 (partitions, tiled_partition, labeled_partition, binary_partition), 4.4.5.1 (sync), 4.4.6.1 (reduce, hardware acceleration on compute capability 8.0 and later), 4.4.8 and 4.4.8.1 (cooperative launch and its requirements), Section 5.7.3.1.3 (grid_group), 5.7.3.1.4 (thread_block_tile sizes) and 5.7.3.6.2.1 (grid synchronization and co-residency)
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition
    locator: Chapter 6 (performance considerations) and Chapter 10 (reduction)
---

**Cooperative groups** is a part of the CUDA API that turns sets of threads into objects. A group can be the whole thread block, a tile of a fixed size inside the block, the lanes of a warp that are active at a point, or the whole grid, and each group offers `sync()`, a rank for each thread, and collectives such as shuffles and reductions (CUDA Programming Guide v13.5, Section 4.4). It gives names to the levels of the [CUDA programming model](/cuda-programming-model/) and adds one level that the plain model does not have: a barrier over the whole grid inside one kernel, `grid.sync()`, which works only when the kernel is launched as a cooperative kernel and all of its blocks are resident on the GPU at the same time.

## In plain words

In a big company, a worker can belong to a desk team, a floor, or the whole company. Cooperative groups let a program say which of these it means when it says "wait for the others" or "add up our numbers". A program can also split a floor into small teams of a fixed size, for example eight people each, and let each small team work and wait on its own. The company-wide meeting is special. Everyone must be in the building at the same time, or the people inside wait forever for people who can never come in. So a program that wants such a meeting must ask for it at the start, and it may hire only as many workers as the building can hold at once.

## The idea

### Groups and their methods

| Group | How to get it | Size | `sync()` is |
|---|---|---|---|
| `thread_block` | `this_thread_block()` | the block | `__syncthreads()` |
| `thread_block_tile<N>` | `tiled_partition<N>(block)` | $N$, a power of 2 up to 1024 | a barrier over the tile |
| `thread_group` (dynamic tile) | `tiled_partition(block, n)` | $n$ | a barrier over the tile |
| `coalesced_group` | `coalesced_threads()` | the active lanes of the warp | a barrier over those lanes |
| `grid_group` | `this_grid()` | the grid | a barrier over the whole grid |

Every group has `thread_rank()` (the rank of the calling thread in the group, from 0) and `num_threads()` (Section 4.4.2). A tile of $N$ threads cut from a block of $T$ threads gives the thread of block rank $r$ the tile rank $r \bmod N$ and the tile index $\lfloor r/N \rfloor$ (`meta_group_rank()`), with $\lceil T/N \rceil$ tiles. The Guide's example cuts a block into tiles of 8 with `tiled_partition<8>(this_thread_block())` (Section 4.4.4). Tiles of up to 32 threads live in one warp, and their methods `shfl`, `shfl_down`, `shfl_xor`, `ballot`, `any` and `all` compile to the [warp-level primitives](/warp-level-primitives/) with the right mask. `labeled_partition` and `binary_partition` split a group by a label or a predicate.

The collectives `cg::reduce(group, v, op)` and the scans `cg::inclusive_scan` and `cg::exclusive_scan` work on tiles and coalesced groups; reductions use hardware acceleration on compute capability 8.0 and later (Section 4.4.6.1).

```cpp
#include <cooperative_groups.h>
#include <cooperative_groups/reduce.h>
namespace cg = cooperative_groups;

__device__ int blockSum(int v, int* warpSums) {        // warpSums: shared, one int per warp
    cg::thread_block block = cg::this_thread_block();
    cg::thread_block_tile<32> warp = cg::tiled_partition<32>(block);
    int s = cg::reduce(warp, v, cg::plus<int>());      // 5 shuffle steps or one instruction
    if (warp.thread_rank() == 0) warpSums[warp.meta_group_rank()] = s;
    block.sync();
    int total = 0;
    for (int i = 0; i < warp.meta_group_size(); ++i) total += warpSums[i];
    return total;                                      // every thread of the block gets the sum
}
```

The functions take a group as a parameter, so a function such as `blockSum` states in its type which threads must call it together. That is the main gain over raw `__syncthreads()` and masks.

### The grid barrier and co-residency

In a plain launch, blocks run in any order, and a block may not start until another block has ended. So a block that waits for all other blocks can wait forever: the blocks it waits for need its slot on the SM. Before cooperative groups, blocks could synchronize only at a kernel boundary (Section 5.7.3.6.2.1).

`grid.sync()` makes the barrier safe by a launch rule. The kernel must be launched with `cudaLaunchCooperativeKernel` instead of `<<< >>>`, and the grid must be no larger than the number of blocks that can be resident at once:

$$G \le (\text{number of SMs}) \times b,$$

where $b$ is the number of resident blocks per SM from [occupancy](/occupancy/), as returned by `cudaOccupancyMaxActiveBlocksPerMultiprocessor` for this kernel, block size and shared memory (Section 5.7.3.6.2.1). A cooperative launch with a larger grid fails with an error instead of starting. `grid.is_valid()` tells a kernel whether it was launched cooperatively (Section 5.7.3.1.3).

The Guide lists the systems that support cooperative launch: compute capability 6.0 or later, on Linux without MPS, on Linux with MPS on compute capability 7.0 or later, or on the latest Windows versions (Section 4.4.8.1). The multi-device cooperative launch was removed in CUDA 13. These rules change between CUDA versions; check the Guide for the version in use.

```cpp
__global__ void twoPhase(const float* x, float* partial, float* out, int n) {
    cg::grid_group grid = cg::this_grid();
    float s = 0.0f;
    for (int i = grid.thread_rank(); i < n; i += grid.num_threads()) s += x[i];   // grid-stride
    s = blockReduce(s);                                // any block reduction
    if (threadIdx.x == 0) partial[blockIdx.x] = s;
    grid.sync();                                       // all partial sums are written
    if (grid.thread_rank() == 0) {
        float t = 0.0f;
        for (int b = 0; b < gridDim.x; ++b) t += partial[b];
        *out = t;
    }
}
// host: int b; cudaOccupancyMaxActiveBlocksPerMultiprocessor(&b, twoPhase, 256, smemBytes);
//       launch b * numSMs blocks of 256 threads with cudaLaunchCooperativeKernel.
```

The grid size no longer depends on $n$, so the kernel uses a grid-stride loop, as in [persistent threads](/persistent-threads/).

## Examples

- **Tile ranks.** A block of 256 threads cut into tiles of 8 has 32 tiles. Thread 7 is rank 7 of tile 0, thread 8 is rank 0 of tile 1, and thread 255 is rank 7 of tile 31. A tile size of 6 is not allowed for `thread_block_tile`, because the size must be a power of 2.
- **The largest cooperative grid.** On an A100 (108 SMs), a kernel whose resources allow 4 resident blocks per SM can be launched cooperatively with at most $108 \cdot 4 = 432$ blocks. With different registers or shared memory the bound changes, and other GPUs have other SM counts.
- **A deadlock without co-residency.** Model a GPU with 8 block slots and a grid of 16 blocks that all call a grid barrier. The first 8 blocks start, reach the barrier and wait. The other 8 cannot start, because no slot is free, and no slot will be freed, because the 8 resident blocks never end. The cooperative launch rule forbids exactly this grid.

The Python code of this page computes the tile ranks, and models a grid with a fixed number of resident block slots in which a block holds its slot from start to end and a grid barrier releases only when every block has reached it. The tests check the tile ranks for tile sizes 1 to 32, that a two-phase grid sum with a barrier is correct when the grid fits in the slots, and that it deadlocks for every slot count below the grid size. No CUDA code runs in the tests.

## Where it is used

Tiles and `cg::reduce` are the modern way to write the warp level of [reductions](/parallel-reduce/), [scans](/all-prefix-sums/) and [compaction](/compaction/), with sub-warp tiles for small problems such as one tile of 4 or 8 lanes per item. `coalesced_threads()` gives the active lanes after a [divergent](/warp-divergence/) branch, which [warp-aggregated atomics](/warp-aggregated-atomics/) use to elect one lane. The grid barrier serves iterative algorithms that would otherwise launch one kernel per step, such as the levels of a breadth-first search or the sweeps of an iterative solver, together with [persistent threads](/persistent-threads/). Each `grid.sync()` acts as a [barrier](/barrier-synchronization/) between [BSP](/bsp-model/) supersteps inside one kernel. The [decoupled look-back scan](/decoupled-look-back-scan/) avoids the grid barrier altogether and so needs no cooperative launch.

## References
