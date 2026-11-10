---
tag: G81808
kind: technique
slug: warp-specialization
name: Warp specialization
aliases:
- producer-consumer warps
- warp-specialized kernels
area: parallel/gpu-algorithms
level: advanced
summary: Give the warps of a thread block different jobs, such as producer warps that load tiles into shared memory and consumer warps that compute on them, joined by barriers on a ring of buffers.
prereqs: [simt-model, shared-memory-tiling, latency-hiding]
see_also: [persistent-threads, tensor-cores, kernel-fusion, flow-shop-scheduling, occupancy, gpu-memory-hierarchy, cuda-streams, decoupled-look-back-scan]
sources:
  - paper: doi:10.1145/2063384.2063400
    title: Michael Bauer, Henry Cook and Brucek Khailany, CudaDMA, optimizing GPU memory bandwidth via warp specialization, SC 2011
    locator: the split of a thread block into DMA warps and compute warps, the producer-consumer protocol on shared-memory buffers with named barriers, and the double-buffered forms
  - url: https://arxiv.org/abs/2407.08608
    title: Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani and Tri Dao, FlashAttention-3, fast and accurate attention with asynchrony and low-precision, 2024
    locator: the warp-specialized producer and consumer warp groups on Hopper with TMA loads, the circular shared-memory buffer, register reallocation between warp groups, and the ping-pong scheduling of two consumer groups
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 3.2.2.3 (asynchronous copies and barriers from compute capability 8.0, and the Tensor Memory Accelerator and asynchronous transaction barriers from compute capability 9.0), Section 3.2.4.2 (asynchronous barriers) and 3.2.4.3 (pipelines for multi-buffer producer-consumer patterns, producer_acquire, producer_commit, consumer_wait, consumer_release), Section 3.2.5 (asynchronous data copies)
  - url: https://docs.nvidia.com/cuda/parallel-thread-execution/
    title: NVIDIA, Parallel Thread Execution ISA
    locator: the bar and barrier instructions (bar.sync and bar.arrive with a barrier number and a thread count)
---

Warp specialization is a GPU technique that gives the warps of one thread block different jobs. In the common form, a few producer warps move tiles of data from global memory into a ring of buffers in shared memory, and the other warps, the consumers, compute on the tiles that are ready. Barriers on each buffer say when a buffer is full and when it is empty again. Data movement and math then overlap inside one block, each kind of warp runs a simple loop with no branches between the two jobs, and each kind can use its own number of registers. The technique appeared as CudaDMA (Bauer, Cook and Khailany 2011). It is now the standard structure of fast matrix multiplication and attention kernels on GPUs that have asynchronous copy hardware.

## In plain words

In a restaurant kitchen, one person can fetch the food from the store room and then cook it, and then fetch the next order. Or one person fetches and another cooks, with a few trays between them. While the cook works on one tray, the runner fills the next. The cook never waits for the store room if the runner keeps ahead, and the runner never fills a tray that the cook still uses. Warp specialization is this split. The trays are buffers in shared memory, and the signals "tray full" and "tray empty" are barriers.

## When it applies

Warp specialization helps when:

- a kernel works through a sequence of tiles, and each tile must be loaded from global memory before it is used, as in tiled matrix multiplication, convolution, attention and stencils;
- the loads and the math are both large enough that their overlap matters;
- the loads and the math need different resources, for example the math needs many registers while the loads need few;
- the hardware can do the copies on its own (asynchronous copies from compute capability 8.0, the Tensor Memory Accelerator from compute capability 9.0, as in the CUDA Programming Guide 13.5, Section 3.2.2.3), so that a few producer threads can keep many bytes in flight.

It is less useful when a kernel is simple enough that many warps doing the same thing already hide the latency of memory, which is the normal GPU way of [latency hiding](/latency-hiding/).

## The template

The model is the [SIMT model](/simt-model/) with warps of 32 threads and the [memory hierarchy](/gpu-memory-hierarchy/), with the [roofline model](/roofline-model/) for the time of each tile. The schedule of loads and computes is a two-stage [flow shop](/flow-shop-scheduling/) with a buffer of size $k$ between the stages.

| symbol | meaning |
|---|---|
| $n$ | the size of the problem |
| $p$ | the number of processors |
| $W$, $S$, $T_p$ | the work, the span and the time on $p$ processors |
| $M$, $B$ | the fast memory size and the memory transaction size |
| $T$ | the number of tiles that one block processes |
| $k$ | the number of buffers in the ring |
| $L$, $C$ | the time to load one tile and the time to compute on it |

There is a FULL barrier and an EMPTY barrier for each buffer. The producer arrives on FULL when a tile is in place. The consumers wait on FULL, compute, and arrive on EMPTY. The producer waits on EMPTY before it reuses the buffer.

```pseudo id=main
SPECIALIZED-BLOCK(tiles, T, k)
     ▷ producer warps
L1   for t ← 0 to T − 1 do
L2     if t ≥ k then WAIT(EMPTY[t mod k])          ▷ the consumers are done with tile t − k
L3     LOAD(tiles[t], buf[t mod k]); ARRIVE(FULL[t mod k])
     ▷ consumer warps
L4   for t ← 0 to T − 1 do
L5     WAIT(FULL[t mod k])                          ▷ tile t is in shared memory
L6     COMPUTE(buf[t mod k]); if t + k < T then ARRIVE(EMPTY[t mod k])
```

**Why it is correct.** The consumers read buffer $t \bmod k$ only after they pass FULL for tile $t$, which the producer arrives at only after the load of tile $t$. The producer writes tile $t$ into the buffer only after it passes EMPTY for tile $t - k$, which the consumers arrive at only after their compute on tile $t - k$. So no tile is read before it is written, and no buffer is overwritten while it is read. Each side handles the tiles in order, so tile $t$ meets the barriers of tile $t$ and not those of another tile. The consumers do not arrive on EMPTY for the last $k$ tiles, because the producer will not wait for them.

**Time.** Without specialization, the same warps load and then compute, and a block takes $T(L + C)$ if nothing else hides the loads. With one buffer, the producer must wait for the consumers before every load, so the time is also $T(L + C)$. With $k \ge 2$ equal tiles,
$$T_{\text{block}} = L + C + (T - 1)\max(L, C),$$
which is the fill of the pipeline, $T - 1$ steps of the slower stage, and the drain. When $L \le C$, the loads are hidden except for the first, and the block runs at the speed of its math. More buffers help when the times of tiles vary, because a fast tile can make up for a slow one. They cost shared memory, which can lower the [occupancy](/occupancy/).

**Registers.** All threads of a kernel get the same number of registers at launch. Producer warps need few, so they waste most of theirs. FlashAttention-3 (Shah and others 2024) describes register reallocation between warp groups on Hopper, so that the producer group gives registers to the consumer groups. As an example with assumed numbers: with 65 536 registers, one producer group of 128 threads and two consumer groups of 256 threads, an equal split gives at most 170 registers per thread, while producers that keep 40 registers leave 236 per consumer thread. Real limits depend on the GPU and on the allocation granularity, and they change between compute capabilities.

The CUDA C++ code below is a sketch of the CudaDMA form with named barriers. It assumes one producer warp, `NC` consumer warps and two buffers, and it uses the PTX `bar.sync` and `bar.arrive` instructions with barrier numbers 1 to 4 (number 0 is used by `__syncthreads`). The tests do not run this CUDA code. They run the Python model of the ring of buffers.

```cuda
__device__ __forceinline__ void bar_sync(int id, int n)   { asm volatile("bar.sync %0, %1;"   :: "r"(id), "r"(n) : "memory"); }
__device__ __forceinline__ void bar_arrive(int id, int n) { asm volatile("bar.arrive %0, %1;" :: "r"(id), "r"(n) : "memory"); }

template <int NC, int TILE>
__global__ void specialized(const float* in, float* out, int T) {
    __shared__ float buf[2][TILE];
    const int warp = threadIdx.x / 32, lane = threadIdx.x % 32;
    const int N = (NC + 1) * 32;                 // threads that take part in each barrier
    const float* src = in + (size_t)blockIdx.x * T * TILE;
    if (warp == NC) {                            // the producer warp
        for (int t = 0; t < T; ++t) {
            int b = t % 2;
            if (t >= 2) bar_sync(1 + b, N);      // EMPTY[b]
            for (int i = lane; i < TILE; i += 32) buf[b][i] = src[(size_t)t * TILE + i];
            bar_arrive(3 + b, N);                // FULL[b]
        }
    } else {                                     // the consumer warps
        float acc = 0.0f;
        for (int t = 0; t < T; ++t) {
            int b = t % 2;
            bar_sync(3 + b, N);                  // FULL[b]
            for (int i = threadIdx.x; i < TILE; i += NC * 32) acc += buf[b][i] * buf[b][i];
            if (t + 2 < T) bar_arrive(1 + b, N); // EMPTY[b]
        }
        out[blockIdx.x * NC * 32 + threadIdx.x] = acc;
    }
}
// Launch with (NC + 1) * 32 threads per block.
```

On GPUs with compute capability 9.0, the same structure uses the Tensor Memory Accelerator: one producer thread issues a bulk copy of a whole tile, and an asynchronous transaction barrier in shared memory completes when the expected number of bytes has arrived. The `cuda::pipeline` API of the guide, with `producer_acquire`, `producer_commit`, `consumer_wait` and `consumer_release`, gives the same protocol without hand-written barriers (Section 3.2.4.3).

## Classic examples

- **CudaDMA.** Bauer, Cook and Khailany (2011) split a block into DMA warps and compute warps, with a small library of transfer patterns and named barriers for the handshake. Their aim was to reach high memory bandwidth while the compute warps keep their registers for math.
- **Matrix multiplication on Hopper and later GPUs.** Production kernels load tiles of A and B with the Tensor Memory Accelerator in a producer warp group, and one or more consumer warp groups run [tensor core](/tensor-cores/) instructions on them. The loop over output tiles is often a [persistent](/persistent-threads/) loop.
- **FlashAttention-3.** Shah and others (2024) use producer warps for the loads of K and V, consumer warp groups for the two matrix products and the softmax, and a ping-pong schedule so that the softmax of one consumer group overlaps the matrix products of the other.
- **The example in the Python file.** With $T = 8$ tiles, $L = 3$ and $C = 4$, the plain kernel takes $8 \cdot 7 = 56$ time units. With two buffers, it takes $3 + 8 \cdot 4 = 35$, a speedup of $8/5$, because each load after the first hides behind a compute.

## Variations

- **Number of buffers.** Double buffering ($k = 2$) is the simplest. Deeper rings ($k = 3$ to 8 in many matrix kernels) absorb variation and keep more copies in flight, at the cost of shared memory.
- **More than two roles.** A block can have a load role, a math role and a store role, or several math roles that take turns on the math units (the ping-pong form).
- **Synchronization primitive.** Named barriers (`bar.sync` and `bar.arrive`), `cuda::barrier` objects in shared memory (Section 3.2.4.2), and `cuda::pipeline` (Section 3.2.4.3) all give the FULL and EMPTY signals.
- **Specialization across blocks.** Some kernels give whole blocks different roles. Then the blocks communicate through global memory or through clusters of blocks, and the risks of [persistent threads](/persistent-threads/) apply.

## Pitfalls

- **Wrong barrier counts.** A named barrier completes when the stated number of threads has arrived. If a warp skips an arrive, or the count includes threads that never arrive, the block hangs. Count the threads of both roles, in multiples of 32.
- **Left-over arrivals.** An arrive that no wait matches leaves a barrier in a partial state. The template stops the EMPTY arrivals for the last $k$ tiles for this reason.
- **Divergence inside a role.** The roles should split at warp boundaries. If one warp holds threads of both roles, the two paths of the warp run one after the other.
- **Too few producers without copy hardware.** On GPUs without asynchronous copies, each producer thread waits for its own loads, so one producer warp may not keep enough bytes in flight to use the bandwidth.
- **Shared memory and occupancy.** $k$ buffers of a large tile can take most of the shared memory, so fewer blocks fit on an SM. The design depends on the limits of the GPU, which change between generations.
- **Hard to tune and to port.** The best split of warps, the number of buffers and the register counts depend on the GPU. Libraries such as CUTLASS keep these as parameters. Write a plain tiled kernel first and measure it.

## Exercises

1. Prove that the template never lets the producer write a buffer that a consumer still reads, for any $k \ge 1$.
2. Derive $T_{\text{block}} = L + C + (T - 1)\max(L, C)$ for $k = 2$, and show that $k = 3$ gives the same time when all tiles are equal.
3. Give tile times $L_t$ and $C_t$ for which $k = 3$ is faster than $k = 2$, and check the times with the Python model.
4. A block has 4 consumer warps and 1 producer warp. Write the thread counts of the four named barriers in the CUDA sketch, and explain what happens if the count is $4 \cdot 32$.
5. With 65 536 registers per SM and blocks of one producer group of 128 threads and two consumer groups of 128 threads each, find the registers per consumer thread when the producers keep 24 registers, and compare it with an equal split.

## References
