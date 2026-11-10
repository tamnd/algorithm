---
tag: R2RS59
kind: technique
slug: kernel-fusion
name: Kernel fusion
aliases:
- operator fusion
- loop fusion on GPUs
area: parallel/gpu-algorithms
level: core
summary: Merge GPU kernels that pass data through global memory into one kernel that keeps the intermediate values in registers or shared memory, which cuts memory traffic and launches.
prereqs: [gpu-memory-hierarchy, arithmetic-intensity, roofline-model]
see_also: [kernel-launch-overhead, occupancy, parallel-reduce, shared-memory-tiling, stencil-computation, host-device-data-transfer, cuda-streams, tensor-cores]
sources:
  - paper: doi:10.1109/SC.2014.21
    title: Mohamed Wahib and Naoya Maruyama, Scalable kernel fusion for memory-bound GPU applications, SC 2014, 191 to 202
    locator: the fusion of memory-bound kernels, the search over fusion choices, and the measured speedups
  - url: https://arxiv.org/abs/2205.14135
    title: Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra and Christopher Ré, FlashAttention, fast and memory-efficient exact attention with IO-awareness, NeurIPS 2022
    locator: the fused attention kernel with tiling and recomputation, and its analysis of the number of accesses to GPU high bandwidth memory
  - paper: doi:10.1145/1498765.1498785
    title: Samuel Williams, Andrew Waterman and David Patterson, Roofline, an insightful visual performance model for multicore architectures, Communications of the ACM 52(4), 2009, 65 to 76
    locator: arithmetic intensity and the memory-bound region of the roofline
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition, Morgan Kaufmann, 2022
    locator: Chapter 5, Memory architecture and data locality (registers and shared memory, and the effect of resource use on occupancy)
---

Kernel fusion is a GPU technique that merges two or more kernels into one, so that a value made by the first is used by the second while it is still in a register or in shared memory, instead of being written to global memory and read back. Most elementwise and reduction kernels are bound by memory bandwidth, so removing the round trip through global memory makes them faster almost in proportion to the traffic saved. Fusion also removes kernel launches. Its limits are the registers and shared memory of the fused kernel, and dependencies that need all blocks to finish before the next step.

## In plain words

Picture a kitchen where one cook peels all the potatoes and puts them on a far shelf, and a second cook later takes them from the shelf and cuts them. Each potato makes two trips to the shelf. If one cook peels each potato and cuts it at once, the shelf is never used. The work of peeling and cutting is the same, but the walking is gone. On a GPU, the far shelf is global memory and walking is the slow part. Fusion gives one kernel both jobs, so the middle result never goes to the shelf. The catch is that the one cook needs a bigger work table, and if the table is too big, fewer cooks fit in the kitchen.

## When it applies

Fusion applies when:

- one kernel writes an array that the next kernel reads, and each element (or each tile) of the second kernel needs only elements that the same thread or block of the first kernel made;
- the kernels are bound by memory bandwidth, so the time is about the bytes moved divided by the bandwidth (the memory-bound side of the [roofline](/roofline-model/));
- the fused kernel still fits the resources of a streaming multiprocessor with enough [occupancy](/occupancy/) to hide latency.

It does not apply directly when the second kernel needs a value that depends on *all* blocks of the first, such as a global maximum used to normalize every element, unless the work can be arranged so that one block owns all the data it needs, or a grid-wide synchronization is used.

## The template

The cost model is the [SIMT model](/simt-model/) with warps of 32, with the [memory hierarchy](/gpu-memory-hierarchy/) of registers, shared memory, caches and global memory, and the [roofline model](/roofline-model/). Traffic is counted in words of global memory.

| symbol | meaning |
|---|---|
| $n$ | the number of elements |
| $b$ | the number of elements per thread block, $t = \lceil n/b \rceil$ blocks |
| $k$ | the number of kernels in a chain |
| $p$ | the number of processors |
| $W$, $S$, $T_p$ | the work, the span and the time on $p$ processors |
| $M$, $B$ | the fast memory size and the memory transaction size |

**Map then reduce.** Compute $\sum_i f(x_i)$. The unfused program runs three kernels: a map that writes $y_i = f(x_i)$, a block reduce that writes $t$ partial sums, and a final reduce of the partials.

| kernel | reads | writes |
|---|---|---|
| map | $n$ | $n$ |
| block reduce | $n$ | $t$ |
| final reduce | $t$ | 1 |
| **unfused total** | $2n + t$ | $n + t + 1$ |
| fused map and block reduce | $n$ | $t$ |
| final reduce | $t$ | 1 |
| **fused total** | $n + t$ | $t + 1$ |

The unfused program moves $3n + 2t + 1$ words and the fused one $n + 2t + 1$, a saving of exactly $2n$: the write of $y$ and its read. For $n = 2^{20}$ and $b = 256$, $t = 4096$, so the counts are $3\,153\,921$ and $1\,056\,769$ words, a ratio of $2.98$. With 4-byte words that is 12.6 MB against 4.2 MB. At an assumed bandwidth of 1000 GB/s, a round number and not the figure of a particular GPU, the memory time falls from about 12.6 µs to about 4.2 µs. Fusion also removes one of the three launches, which matters at this size; see [kernel launch overhead](/kernel-launch-overhead/). The work $W = \Theta(n)$ and the span $O(\log b + \log t)$ do not change; only the traffic does, and with it the [arithmetic intensity](/arithmetic-intensity/), which rises by a factor of about 3.

**Elementwise chains.** A chain of $k$ elementwise kernels $x \to f_1(x) \to \cdots \to f_k(\cdots)$ reads and writes $n$ words per kernel, $2kn$ in all, in $k$ launches. The fused kernel applies $f_k \circ \cdots \circ f_1$ in registers and moves $2n$ words in one launch.

**Register pressure.** The fused kernel holds the live values of all the fused steps, so it often needs more registers per thread. Let an SM have a register file of $R_{SM}$ registers and room for at most $w_{max}$ warps and $\beta_{max}$ blocks, and let a block have $\tau$ threads that each use $R$ registers. If we ignore the allocation granularity, the number of resident warps is
$$\text{warps} = \frac{\tau}{32} \cdot \min\left(\left\lfloor \frac{R_{SM}}{R \tau} \right\rfloor,\ \beta_{max},\ \left\lfloor \frac{32\, w_{max}}{\tau} \right\rfloor\right).$$
With the assumed values $R_{SM} = 65\,536$, $w_{max} = 64$, $\beta_{max} = 32$ and $\tau = 256$, a kernel with 32 registers per thread keeps 64 warps resident, 64 registers give 32 warps, 128 give 16, and 255 give 8. The four values are assumptions for the example. The real limits are in the tables of technical specifications per compute capability in the CUDA Programming Guide, and they change between GPU generations, so check them for the target GPU. Fewer warps hide less latency, and a kernel that needs more registers than the limit spills to local memory, which is backed by global memory.

The CUDA C++ code below shows the map-then-reduce pair and its fused form. The tests do not run this CUDA code. They run a Python model that counts the global reads, writes and launches of each version.

```cuda
// Unfused, kernel 1: the squares go to global memory.
__global__ void square(const float* x, float* y, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) y[i] = x[i] * x[i];
}

// Unfused, kernel 2: each block reads its part of y and writes one partial sum.
template <int B>
__global__ void block_sum(const float* y, float* part, int n) {
    __shared__ float s[B];
    int i = blockIdx.x * B + threadIdx.x;
    s[threadIdx.x] = (i < n) ? y[i] : 0.0f;
    __syncthreads();
    for (int h = B / 2; h > 0; h >>= 1) {
        if (threadIdx.x < h) s[threadIdx.x] += s[threadIdx.x + h];
        __syncthreads();
    }
    if (threadIdx.x == 0) part[blockIdx.x] = s[0];
}

// Fused: the square lives in a register and never reaches global memory.
template <int B>
__global__ void square_block_sum(const float* x, float* part, int n) {
    __shared__ float s[B];
    int i = blockIdx.x * B + threadIdx.x;
    float v = (i < n) ? x[i] : 0.0f;
    s[threadIdx.x] = v * v;
    __syncthreads();
    for (int h = B / 2; h > 0; h >>= 1) {
        if (threadIdx.x < h) s[threadIdx.x] += s[threadIdx.x + h];
        __syncthreads();
    }
    if (threadIdx.x == 0) part[blockIdx.x] = s[0];
}
// In both versions a last small kernel (or an atomicAdd per block) sums part[].
```

## Classic examples

- **Reductions of a transformed array.** Norms, dot products and sums of squares fuse the map into the [parallel reduce](/parallel-reduce/), as in the template. Libraries offer this through transform iterators or a map argument to the reduce.
- **Elementwise chains in deep learning.** Bias, activation, scaling and residual additions are short elementwise kernels. Graph compilers for neural networks fuse them into one kernel, and they fuse such operations into the epilogue of a matrix multiplication, so that the result tile is changed while it is still in registers, before it is stored.
- **Attention.** FlashAttention (Dao et al. 2022) fuses the product $QK^T$, the softmax and the product with $V$ into one kernel. It processes the keys and values in tiles that fit in shared memory and keeps running softmax statistics, so the $N \times N$ attention matrix is never written to global memory. The softmax needs the maximum of each row, which is the kind of dependency that blocks naive fusion; the running maximum with rescaling removes it.
- **Stencil pipelines.** Two [stencil](/stencil-computation/) sweeps in a row can be fused if each block also computes the halo of the first sweep that the second needs. Wahib and Maruyama (2014) search over such fusions of memory-bound kernels in real applications and report speedups over the unfused code.
- **Scan-based primitives.** Stream [compaction](/compaction/) fuses the predicate, the scan and the scatter into one pass in single-pass designs such as the [decoupled look-back scan](/decoupled-look-back-scan/).

## Variations

- **Vertical fusion** merges a producer and its consumer, as above, and saves traffic. **Horizontal fusion** merges independent kernels that run side by side, which saves launches and fills a GPU that one small kernel cannot fill. Horizontal fusion saves no traffic.
- **Fusion with recomputation.** When the consumer needs neighbours of the producer's output, the fused kernel recomputes the overlapping part in each block, which trades work for traffic, as in temporal blocking of stencils.
- **Partial fusion through shared memory.** When a block needs values that other threads of the same block made, the fused kernel passes them through shared memory with a barrier, not through global memory.
- **Kernel fission.** The reverse step splits a kernel that uses too many registers into two, when the lost occupancy costs more than the extra traffic.
- **Persistent fused kernels.** A [persistent](/persistent-threads/) kernel can run several phases with grid-wide synchronization between them and keep data on chip across phases.

## Pitfalls

- **Register spills.** A fused kernel can exceed the register budget and spill to local memory, which is in global memory. Check the compiler's report of registers and spill stores.
- **Lost occupancy.** More registers or shared memory per block means fewer resident warps, by the formula above. If the kernel was latency bound rather than bandwidth bound, fusion can make it slower.
- **Global dependencies.** A step that needs a result from all blocks, such as a global sum used by every element, cannot be fused across the dependency without grid synchronization or an algorithmic change.
- **Different parallel shapes.** A map over $n$ elements and a reduction to $t$ values use different grids. The fused kernel must use the grid of the larger step and let some threads idle in the smaller one.
- **Losing tuned library kernels.** Fusing your code into a call to a vendor library is usually not possible, and a hand-fused kernel can be slower than the library kernel plus one extra pass.
- **Floating-point results change.** Fusion can change the order of operations or the use of fused multiply-add, so results can differ in the last bits from the unfused code.

## Exercises

1. Derive the traffic $3n + 2t + 1$ and $n + 2t + 1$ of the template for the case where the final reduce is replaced by one `atomicAdd` per block.
2. A chain of $k$ elementwise kernels moves $2kn$ words. If each kernel also has a fixed launch cost $\lambda$ and the bandwidth is $\beta$ words per second, write the time of the chain before and after fusion and find the $n$ below which the launch cost dominates.
3. Two 5-point stencil sweeps on a $T \times T$ tile are fused with recomputation. Count the global loads per output of the fused kernel and the extra updates it does, and compare them with two separate tiled sweeps.
4. Using the register formula with the assumed values of the template, find the largest number of registers per thread that keeps 32 warps resident with blocks of 128 threads.
5. Explain why softmax over the rows of a matrix can be fused into one kernel per row when a row fits in one thread block, and what changes when it does not.

## References
