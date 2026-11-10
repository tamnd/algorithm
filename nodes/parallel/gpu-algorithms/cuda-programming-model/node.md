---
tag: W9JAQZ
kind: model
slug: cuda-programming-model
name: CUDA programming model
aliases:
- CUDA
- kernel programming model
area: parallel/gpu-algorithms
level: intro
summary: A host program launches kernels on the GPU over a grid of thread blocks; threads of one block share memory and a barrier, and the end of a kernel is the only barrier across blocks.
prereqs: [simt-model]
see_also: [thread-block-and-grid, gpu-memory-hierarchy, cooperative-groups, host-device-data-transfer, kernel-launch-overhead, cuda-streams, bsp-model, kernel-fusion]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 2.3.2 (thread hierarchy), Section 2.3.2.1 (block synchronization), Section 2.3.3 and 2.3.3.1 (memory spaces and the vecAdd example in global memory), Section 5.4.4.1 (__syncthreads) and Section 5.1.3, Table 33 (launch limits)
  - paper: doi:10.1145/1365490.1365500
    title: John Nickolls, Ian Buck, Michael Garland and Kevin Skadron, Scalable parallel programming with CUDA, ACM Queue 6(2) (2008)
    locator: the sections on the CUDA paradigm, thread blocks and barrier synchronization
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition
    locator: Chapter 2 (heterogeneous data parallel computing, the vector addition kernel) and Chapter 3 (multidimensional grids and data)
  - url: https://rocm.docs.amd.com/projects/HIP/en/latest/understand/hardware_implementation.html
    title: AMD, HIP documentation, Hardware implementation
    locator: the sections on the compute unit and the local data share
---

The CUDA programming model is the way a program states parallel work for an NVIDIA GPU. A program on the CPU (the host) launches a **kernel**, a function that runs once for each thread of a **grid**, and the grid is made of **thread blocks** of up to 1024 threads. Threads of one block share fast memory and can wait at a barrier, while blocks run in any order and can wait for each other only at the end of the kernel. The hardware runs the threads by the [SIMT model](/simt-model/), so the programming model fixes what is correct and the SIMT model fixes what is fast.

## The machine

### Host and device

The host is the CPU with its memory. The device is the GPU with its own memory. A typical program does four steps: allocate device memory, copy the input from the host to the device, launch one or more kernels, and copy the output back (see [host-device data transfer](/host-device-data-transfer/)). A launch returns to the host at once; the host waits with `cudaDeviceSynchronize()` or with a blocking copy. Kernels launched into one stream run one after another, in launch order (see [CUDA streams](/cuda-streams/)).

### Kernels and the launch

A kernel is a function marked `__global__`. The launch `kernel<<<grid, block, shmem, stream>>>(args)` creates $G$ blocks of $T$ threads each, where `grid` and `block` are 1D, 2D or 3D sizes of type `dim3`, `shmem` is the size in bytes of dynamic shared memory per block, and `stream` is the stream. Inside the kernel, each thread reads four built-in variables: `threadIdx` (its index in the block), `blockIdx` (the index of its block in the grid), `blockDim` (the block size) and `gridDim` (the grid size). From these it computes which data it owns. The [thread block and grid](/thread-block-and-grid/) page gives the index arithmetic and the limits.

### The hierarchy

| Level | Shares | Synchronizes with | Runs on |
|---|---|---|---|
| thread | its registers and local memory | itself | one lane of a warp |
| warp (32 threads) | registers through shuffles | `__syncwarp()`, see [warp-level primitives](/warp-level-primitives/) | one warp scheduler |
| block (up to 1024 threads) | shared memory | `__syncthreads()` | one SM, for its whole life |
| grid (all blocks) | global memory | the end of the kernel | the whole GPU |

The memory spaces, their scope and their speed are on the [GPU memory hierarchy](/gpu-memory-hierarchy/) page. On AMD GPUs the same model is called HIP, a block is a workgroup, an SM is a compute unit (CU), and shared memory is the local data share (LDS).

### Barriers

`__syncthreads()` makes every thread of the block wait until all threads of the block that have not exited reach it, and makes the shared and global memory writes before it visible to the block after it (Guide Section 5.4.4.1). It is allowed in conditional code only when the condition has the same value in every thread of the block; otherwise the kernel can hang or give wrong results.

No such barrier exists across the blocks of a plain launch. The blocks of a grid may run in any order, at the same time or one after another, so a block must never wait for another block of the same launch. The end of a kernel is a barrier for the whole grid: a kernel that is launched after it in the same stream sees all of its writes. [Cooperative groups](/cooperative-groups/) add a grid-wide barrier inside a kernel, under extra launch rules.

### A complete vector add

```cpp
#include <cuda_runtime.h>

__global__ void vecAdd(const float* A, const float* B, float* C, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;  // global index of this thread
    if (i < n) {                                    // the last block can run past n
        C[i] = A[i] + B[i];
    }
}

void add(const float* hA, const float* hB, float* hC, int n) {
    size_t bytes = n * sizeof(float);
    float *dA, *dB, *dC;
    cudaMalloc(&dA, bytes); cudaMalloc(&dB, bytes); cudaMalloc(&dC, bytes);
    cudaMemcpy(dA, hA, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(dB, hB, bytes, cudaMemcpyHostToDevice);
    int threads = 256;
    int blocks = (n + threads - 1) / threads;       // ceil(n / threads)
    vecAdd<<<blocks, threads>>>(dA, dB, dC, n);
    cudaMemcpy(hC, dC, bytes, cudaMemcpyDeviceToHost);  // waits for the kernel
    cudaFree(dA); cudaFree(dB); cudaFree(dC);
}
```

Block $b$ owns the items $bT$ to $bT + T - 1$, and thread $t$ of it owns item $i = bT + t$. With $G = \lceil n/T \rceil$ blocks, every $i$ from 0 to $n - 1$ has exactly one thread, because $i \mapsto (\lfloor i/T \rfloor, i \bmod T)$ is a bijection. The grid has $GT$ threads, and $GT - n < T$ of them fail the guard and do nothing. For $n = 1000$ and $T = 256$: $G = 4$ blocks, 1024 threads, and 24 idle threads in the last block. Consecutive threads read consecutive floats, so each warp load is [coalesced](/memory-coalescing/).

## What it counts

The model has two parts: a rule for correctness and a set of costs.

The rule for correctness: a kernel must give the same result for every order of its blocks and for every interleaving of its threads between two barriers. A data race breaks the rule. So does a block that waits for another block of the same launch.

The costs:

- **launches**, because each one is a global barrier with a fixed cost per launch that does not shrink with the problem size, see [kernel launch overhead](/kernel-launch-overhead/). An algorithm that needs $r$ global barriers needs $r + 1$ kernels, or one cooperative kernel.
- **warp instructions**, counted by the [SIMT model](/simt-model/).
- **bytes moved** at each level of the [memory hierarchy](/gpu-memory-hierarchy/), which the [roofline model](/roofline-model/) turns into a time bound.
- **resources per block** (threads, registers, shared memory), which set the [occupancy](/occupancy/).

The notation of the Parallel area holds: $n$ is the input size, $p$ the number of processors, $W$ the work, $S$ the span and $T_p$ the time on $p$ processors. On this page $T$ is the block size and $G$ the number of blocks.

### Example: a sum with two launches

A sum of $n$ numbers needs a barrier between the partial sums of the blocks and the final add. The first kernel reduces each block in shared memory with $\log_2 T$ halving steps, each one followed by a block barrier. The second kernel adds the $G$ partial sums. The kernel boundary between them is the global barrier.

```cpp
__global__ void blockSum(const int* x, int* partial, int n) {
    extern __shared__ int s[];                 // T ints, size set at launch
    int t = threadIdx.x, i = blockIdx.x * blockDim.x + t;
    s[t] = (i < n) ? x[i] : 0;
    __syncthreads();                           // all of s is written
    for (int h = blockDim.x / 2; h > 0; h /= 2) {
        if (t < h) s[t] += s[t + h];
        __syncthreads();                       // this level is done
    }
    if (t == 0) partial[blockIdx.x] = s[0];
}
// host: blockSum<<<G, T, T * sizeof(int)>>>(x, partial, n);
//       finalSum<<<1, 1>>>(partial, out, G);   runs after blockSum ends
```

If the final add is moved into the first kernel, so that block 0 adds `partial[]` after its own reduction, the result depends on the block order. When block 0 runs first, it reads zeros for the other blocks.

The Python code of this page models a launch: blocks run one after another in an order that the test chooses, each block has its own shared memory, and each `yield` in a kernel is a `__syncthreads()`. The tests check the vector add for many $n$ and $T$, check that the two-launch sum is right for shuffled block orders, and show that the fused one-launch version is wrong when block 0 runs first. The CUDA code on this page is for the reader; the tests do not run it.

## Relation to other models

- [SIMT model](/simt-model/): the execution model below this one. The programming model says what each thread does; the SIMT model says what one warp instruction costs.
- [BSP model](/bsp-model/): a sequence of kernels is a sequence of [supersteps](/superstep/). Each kernel computes locally, communicates through global memory, and ends with a [barrier](/barrier-synchronization/) for the whole grid. Inside a block, `__syncthreads()` gives a second, cheaper level of barriers.
- [Work-span model](/work-span-model/): a kernel of $n$ independent threads is a [parallel for](/parallel-for/) with span $O(1)$ plus the span of one thread. The span of a program is the sum of the spans of its kernels in one stream.
- [PRAM](/pram-model/): a PRAM step has a global barrier after it. In CUDA a global barrier costs a launch, so a PRAM algorithm with $S$ synchronous steps becomes $S$ kernels unless the steps can be grouped inside blocks.
- OpenCL uses the same structure under other names: a work-item is a thread, a work-group is a block, the NDRange is the grid, and local memory is shared memory.

## Known results in the model

- The bounds-guarded launch with $\lceil n/T \rceil$ blocks covers $n$ items with fewer than $T$ idle threads (shown above). A grid-stride loop covers any $n$ with a fixed grid, see [thread block and grid](/thread-block-and-grid/).
- A reduction of $n$ numbers in blocks of $T$ needs $\lceil \log_T n \rceil$ launches when each launch reduces by a factor of $T$, or one launch with atomic adds or a cooperative grid barrier. See [parallel reduction](/parallel-reduce/).
- A scan needs a barrier between the block sums and the final pass, so a common GPU scan uses three kernels: scan each block, scan the block sums, and add each block sum back. The [decoupled look-back scan](/decoupled-look-back-scan/) of Merrill and Garland does it in one pass without a grid barrier, by making each block wait only for blocks that started before it.
- [Kernel fusion](/kernel-fusion/) joins kernels with no global barrier between them, which saves a launch and a round trip through global memory.

## References
