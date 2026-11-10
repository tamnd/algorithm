---
tag: SE4S1M
kind: concept
slug: gpu-memory-hierarchy
name: GPU memory hierarchy
aliases:
- registers, shared memory and global memory
- GPU memory spaces
area: parallel/gpu-algorithms
level: intro
summary: GPU memory spaces (registers, shared, local, constant, global, L1 and L2) differ in scope, lifetime, size and speed; fast kernels keep reused data in the small, near spaces.
prereqs: [memory-hierarchy, cuda-programming-model]
see_also: [memory-coalescing, shared-memory-tiling, shared-memory-bank-conflicts, occupancy, roofline-model, arithmetic-intensity, external-memory-model, host-device-data-transfer]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 2.3.3 and 2.3.3.1 to 2.3.3.7 (global, shared, registers, local, constant, caches, texture), Section 2.3.4.2 (32 banks of 32 bits per clock) and Section 5.1.3, Tables 34 and 35 (registers, shared memory and unified data cache per SM)
  - url: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/
    title: NVIDIA, CUDA C++ Best Practices Guide, version 13.5
    locator: Section 10.2, Table 1 (salient features of device memory) and the text after it on the order of latencies; Section 10.2.7 (registers)
  - url: https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf
    title: NVIDIA, NVIDIA A100 Tensor Core GPU Architecture (whitepaper), 2020
    locator: the A100 specification table (108 SMs, 1410 MHz boost clock, 40 MB L2, 1555 GB/s HBM2 for the 40 GB part)
  - url: https://www.nvidia.com/content/gtc-2010/pdfs/2238_gtc2010.pdf
    title: Vasily Volkov, Better performance at lower occupancy, GPU Technology Conference 2010
    locator: slide 7 (about 20 cycles for arithmetic, 400 or more for memory) and slides 46 and 47 (shared memory bandwidth below register bandwidth on Fermi)
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition
    locator: Chapter 5 (memory architecture and data locality)
---

The **GPU memory hierarchy** is the set of memory spaces that a GPU kernel can use: registers, local memory, shared memory, the L1 and L2 caches, constant memory and global memory. The spaces differ in who can see the data (the scope), how long the data lives (the lifetime), and how large, how far and how fast they are. Unlike a CPU, the GPU gives the program direct control of one fast level, the shared memory of a block. This page gives the GPU view; the general idea is on the [memory hierarchy](/memory-hierarchy/) page.

## In plain words

A GPU thread has a few private slots in its pocket, which are the fastest of all. Each team of threads shares a small table in its room, which is fast and which the team itself fills and empties. Every room has its own cache, and all rooms share a bigger cache down the hall. The large store of all data is far away in the basement. A trip to the basement takes hundreds of times longer than a reach into a pocket. The store is wide, though: it serves many trips at once, so it is fast when many threads go at the same time and fetch neighbouring items. A fast kernel fetches each item from the basement once, keeps it on the table or in a pocket while the team uses it many times, and lets other teams work while one team waits.

## The idea

### The spaces

The table follows the Best Practices Guide, Section 10.2, Table 1, and the Programming Guide, Section 2.3.3. The levels go from near to far.

| Space | Where | Scope | Lifetime | Cached | Access |
|---|---|---|---|---|---|
| registers | on the SM | one thread | the thread | (no cache needed) | read and write |
| shared memory | on the SM | one block | the block | (on chip) | read and write |
| L1 cache | on the SM, same storage as shared memory | the threads of one SM | managed by hardware | | |
| L2 cache | on the chip | all SMs | managed by hardware | | |
| constant memory | device memory, 64 KB | the grid, and the host | until freed by the host | yes | read only in a kernel |
| local memory | device memory | one thread | the thread | in L1 and L2 | read and write |
| global memory | device memory | the grid, and the host | until freed by the host | in L1 and L2 | read and write |

- **Registers** hold the scalar variables of a thread. An access costs no extra cycles in the normal case (Best Practices Section 10.2.7). The register file is split among the resident warps, so more registers per thread mean fewer resident threads, see [occupancy](/occupancy/).
- **Shared memory** is a scratchpad that the block fills and reads under program control, with `__syncthreads()` between the writes and the reads. It has 32 banks, each 32 bits wide per clock (Programming Guide Section 2.3.4.2), so a warp can read 32 words in one pass when the addresses fall in different banks, see [bank conflicts](/shared-memory-bank-conflicts/).
- **L1 and shared memory** are one physical store per SM, and the program can choose the split (Programming Guide Section 2.3.3.6).
- **Local memory** is private to a thread but lives in device memory, so it has the latency and bandwidth of global memory (Section 2.3.3.4). The compiler puts there the registers that do not fit (spills) and arrays that are indexed with values that are not known at compile time.
- **Constant memory** is a 64 KB read-only space with its own cache. It serves a warp best when all its lanes read the same address.
- **Global memory** is the large device memory (DRAM, often HBM on data-center GPUs). It is accessed in 32-byte sectors, so a warp access is fast only when its 32 addresses fall in few sectors, see [memory coalescing](/memory-coalescing/).
- **Texture memory** is a read-only path through the cache with addressing modes for images. On current GPUs it brings no speed advantage for general kernels (Section 2.3.3.7).

### The order of latency and bandwidth

The Best Practices Guide (after Table 1 of Section 10.2) gives the order: global, local and texture memory have the greatest latency, then constant memory, then shared memory, then the register file. An access to global memory that misses the caches takes hundreds of clock cycles. Volkov measured about 20 cycles for an arithmetic instruction and 400 or more for a memory access on GPUs of 2010 (GTC 2010 talk, slide 7). Bandwidth goes the other way: per SM, the register file is faster than shared memory (Volkov, slides 46 and 47, on Fermi), shared memory is faster than L2, and L2 is faster than device memory. The exact values change with every generation; take them from the whitepaper of the target GPU.

### How the GPU differs from a CPU

- A CPU hides the latency of memory with large caches per thread. A GPU hides it with many warps in flight, see [latency hiding](/latency-hiding/). The cache per resident thread is small, so a GPU kernel should not count on the cache to keep a large working set.
- The fast level that matters most for algorithms is shared memory, which the program manages itself. This is the explicit fast memory of size $M$ of the [external memory model](/external-memory-model/) and of the [red-blue pebble game](/red-blue-pebble-game/), with one copy per block.
- The register file is the largest store on the SM. A GPU kernel that keeps a tile of results in registers, as in [shared memory tiling](/shared-memory-tiling/) with register blocking, uses it as one more level of the hierarchy.

## Examples

All numbers below are for the NVIDIA A100 (Ampere, compute capability 8.0, 40 GB part). They come from the CUDA Programming Guide v13.5, Section 5.1.3, Tables 34 and 35, and the A100 whitepaper, and they change between generations.

| Level | Size on A100 | Source |
|---|---|---|
| registers | 64K 32-bit registers per SM, 256 KB, at most 255 per thread | Table 34 |
| shared memory | up to 164 KB per SM, up to 163 KB per block (opt-in above 48 KB) | Table 34 |
| L1 plus shared memory | 192 KB per SM | Table 35 |
| L2 | 40 MB for the chip | whitepaper |
| global memory | 40 GB of HBM2 at 1555 GB/s | whitepaper |

From these numbers:

- **Registers per thread at full occupancy:** an SM holds at most 2048 threads (Table 33), and $65536 / 2048 = 32$ registers per thread. A kernel that needs 64 registers per thread can have at most 1024 resident threads per SM.
- **The register file is larger than the cache:** 256 KB of registers against 192 KB of L1 and shared memory per SM.
- **L2 per resident thread:** $108 \cdot 2048 = 221{,}184$ resident threads share 40 MB, which is under 200 bytes each.
- **Shared memory bandwidth:** 32 banks of 4 bytes per clock give 128 bytes per clock per SM. At 108 SMs and 1.41 GHz, that is $128 \cdot 108 \cdot 1.41 \cdot 10^9 \approx 19.5$ TB/s for the chip, about 12.5 times the 1.555 TB/s of HBM2. This is a peak that assumes no bank conflicts.

A kernel that reads each input word from global memory once and uses it $k$ times from shared memory or registers cuts its global traffic by a factor of $k$. The [arithmetic intensity](/arithmetic-intensity/) and [roofline](/roofline-model/) pages turn this into a speed bound.

## Where it is used

Every GPU algorithm is designed around this hierarchy. [Shared memory tiling](/shared-memory-tiling/) stages tiles of the inputs in shared memory, as in [parallel matrix multiplication](/parallel-matrix-multiplication/) and [stencil computation](/stencil-computation/). [Parallel matrix transpose](/parallel-matrix-transpose/) goes through shared memory so that both the reads and the writes of global memory are [coalesced](/memory-coalescing/). [Parallel reduction](/parallel-reduce/) and [scans](/all-prefix-sums/) combine values in registers with [warp-level primitives](/warp-level-primitives/), then in shared memory across warps, and only then in global memory. [Kernel fusion](/kernel-fusion/) keeps intermediate values in registers instead of writing them to global memory between kernels. The copy between host memory and device memory is one more, slower level, see [host-device data transfer](/host-device-data-transfer/).

## References
