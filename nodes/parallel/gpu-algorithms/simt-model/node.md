---
tag: 6ZD33P
kind: model
slug: simt-model
name: SIMT execution model
aliases:
- single instruction, multiple threads
- SIMT
area: parallel/gpu-algorithms
level: intro
summary: The GPU execution model in which threads run in warps of 32 that issue one common instruction at a time, so cost is counted per warp instruction and a divergent branch costs the sum of its paths.
prereqs: [data-parallelism]
see_also: [cuda-programming-model, thread-block-and-grid, warp-divergence, warp-level-primitives, memory-coalescing, latency-hiding, pram-model, roofline-model]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 3.2.2.1 (SIMT Execution Model), Section 3.2.2.1.1 (Independent Thread Scheduling), Section 3.2.2.2 (Hardware Multithreading) and Section 5.1.3, Table 33 (warp size 32 for all listed compute capabilities)
  - paper: doi:10.1109/MM.2008.31
    title: Erik Lindholm, John Nickolls, Stuart Oberman and John Montrym, NVIDIA Tesla, a unified graphics and computing architecture, IEEE Micro 28(2) (2008)
    locator: pp. 39 to 55, the section on the SIMT multithreaded instruction unit
  - url: https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf
    title: NVIDIA, NVIDIA Tesla V100 GPU Architecture (whitepaper), 2017
    locator: the section on independent thread scheduling
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition
    locator: Chapter 4 (compute architecture and scheduling, warps and SIMD hardware, control divergence)
  - url: https://rocm.docs.amd.com/projects/HIP/en/latest/understand/hardware_implementation.html
    title: AMD, HIP documentation, Hardware implementation
    locator: the sections on the compute unit, the RDNA architecture and the Wave32 and Wave64 modes
---

The SIMT (single instruction, multiple threads) model is the execution model of GPUs. A program describes one scalar thread, and the hardware runs the threads in groups of 32, called warps, that issue one common instruction at a time for all active threads of the group. The cost of a kernel in the model is the number of warp instructions that it issues, so a step that keeps 1 thread of a warp busy costs as much as a step that keeps all 32 busy. The model refines the [work-span model](/work-span-model/) for [data-parallel](/data-parallelism/) code on GPUs, and the [roofline model](/roofline-model/) adds the memory side.

## The machine

The machine has many streaming multiprocessors (SMs). Each SM runs many threads at once. The threads are grouped as follows, from small to large.

- A **thread** has its own registers and, in the model, its own program counter. It runs scalar code.
- A **warp** is 32 threads with consecutive thread indices in one block. Thread $t$ of a block is in warp $\lfloor t/32 \rfloor$ and is lane $t \bmod 32$ of it (for 2D and 3D blocks, $t$ is the linear index, see [thread block and grid](/thread-block-and-grid/)). The warp size is 32 for every compute capability in the CUDA Programming Guide v13.5 (Section 5.1.3, Table 33).
- A **block** of up to 1024 threads runs on one SM, and its warps share that SM's shared memory. A **grid** is all the blocks of one kernel launch. The [CUDA programming model](/cuda-programming-model/) gives the syntax.

At each issue slot, a warp scheduler picks one warp that is ready and issues its next instruction. The instruction runs on every **active** lane of the warp. A lane is inactive when it has exited or when it is on the other side of a branch. When the lanes of a warp disagree on a branch, the warp runs each path in turn and disables the lanes that did not take it (Guide Section 3.2.2.1). This is [warp divergence](/warp-divergence/). The paths join again at a reconvergence point.

AMD GPUs use the same model with other names: a warp is a **wavefront** of 64 threads (CDNA, and the Wave64 mode of RDNA) or 32 threads (the Wave32 mode of RDNA), an SM is a **compute unit** (CU), and shared memory is the **local data share** (LDS). This page uses the NVIDIA names.

### SIMT and SIMD

A SIMD instruction works on a vector of fixed width, and the program must pack its data into vectors and handle the width itself. A SIMT instruction describes the behaviour of one thread, and the hardware forms the vectors from the threads of a warp (Guide Section 3.2.2.1). So a SIMT program can branch per thread and still be correct. The width of 32 is visible only in the cost: the program is correct for any warp size, but it is fast only when the 32 lanes of a warp take the same path and touch nearby addresses.

### Independent thread scheduling

Before compute capability 7.0 (Volta), a warp had one program counter and an active mask. From compute capability 7.0, each thread has its own program counter and call stack, and the scheduler can run diverged groups of one warp in turns at sub-warp granularity (Guide Section 3.2.2.1.1; the V100 whitepaper). A consequence for correct code: the lanes of a warp are not in lockstep unless the code says so. Code that exchanges data through shared memory between the lanes of one warp without `__syncwarp()` or a `_sync` warp function has a data race on compute capability 7.0 and later. The cost model below still counts one issue for each group of lanes that runs an instruction together.

## What it counts

Let a warp $w$ run instruction $i$ with the set $A_{w,i}$ of active lanes. The model counts:

| Quantity | Formula | Meaning |
|---|---|---|
| issued warp instructions | $I = \sum_w \#\{ i \}$ | the time on one warp scheduler, in issue slots |
| lane instructions | $L = \sum_{w,i} \lvert A_{w,i} \rvert$ | the work $W$ of the work-span model |
| SIMT efficiency | $L / (32 I)$ | the fraction of lanes that do useful work |
| memory transactions | sectors touched per warp access | see [memory coalescing](/memory-coalescing/) |
| shared memory replays | conflict degree per warp access | see [shared memory bank conflicts](/shared-memory-bank-conflicts/) |

The symbols follow the Parallel area: $n$ is the input size, $p$ the number of processors, $W$ the work, $S$ the span, $T_p$ the time on $p$ processors, and $M$ and $B$ the fast memory size and the transaction size. The model ignores the time of one instruction. [Latency hiding](/latency-hiding/) and [occupancy](/occupancy/) add it back.

### A worked count

The vector add kernel below has the usual bounds guard.

```cpp
__global__ void vecAdd(const float* a, const float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;   // 1 instruction
    if (i < n) {                                     // 1 instruction
        c[i] = a[i] + b[i];                          // 2 loads, 1 add, 1 store
    }
}
```

Count the six instructions as shown in the comments. Every warp of the grid issues the first two. A warp issues the last four when at least one of its lanes has $i < n$. With $n$ items and blocks of $T$ threads, the grid has $\lceil n/T \rceil \cdot \lceil T/32 \rceil$ warps, and $\lceil n/32 \rceil$ of them have an active lane, so

$$I = 2 \left\lceil \frac{n}{T} \right\rceil \left\lceil \frac{T}{32} \right\rceil + 4 \left\lceil \frac{n}{32} \right\rceil, \qquad L = 2 \left\lceil \frac{n}{T} \right\rceil T + 4n.$$

For $n = 33$ and $T = 64$: one block of 2 warps, both with an active lane, so $I = 4 + 8 = 12$ and $L = 128 + 132 = 260$. The SIMT efficiency is $260/384 \approx 0.68$. Warp 1 has one useful lane, but it costs as much as warp 0.

### A worked branch

```cpp
if (lane < k) { x = f(x); x = g(x); }   // path 1: 2 instructions
else          { x = h(x); }             // path 2: 1 instruction
```

With the condition and one instruction after the join, a warp issues $2 + 2\,[k > 0] + [k < 32]$ instructions, where $[\cdot]$ is 1 when the condition holds. For $0 < k < 32$ that is 5, the sum of both paths, while the lane instructions number $64 + 2k + (32 - k)$. When all lanes agree, the warp skips the other path.

### The simulator

The Python code of this page is a small SIMT simulator. A kernel is a Python function of one thread. Each `yield` is a `__syncthreads()` barrier, and the code between two barriers is a phase. Each thread records named events, and the events of one warp with the same label form one warp instruction. The tests check the two formulas above for many $n$, $T$ and $k$, check the mapping of 2D and 3D thread indices to warps, and show that a shared-memory reverse is correct with the barrier and wrong without it. The CUDA code on this page is for the reader; the tests do not run it.

## Relation to other models

- [PRAM](/pram-model/): one warp is close to a synchronous PRAM with 32 processors that run the same program. Different warps are not synchronous, and blocks synchronize only at barriers, so the whole GPU is not a PRAM. A PRAM step that keeps $k$ processors busy costs $\lceil k/32 \rceil$ warp issues in the SIMT model.
- [Work-span model](/work-span-model/): the lane instructions $L$ are the work $W$. The SIMT model adds a constant factor of up to 32 for idle lanes, which the work-span model does not see. It has no general span bound of its own; the span of a kernel sequence is the sum of the spans of its kernels.
- [BSP](/bsp-model/): the phases of one block between `__syncthreads()` barriers are like [supersteps](/superstep/) inside the block. Across blocks, the only barrier inside the plain model is the end of a kernel, see the [CUDA programming model](/cuda-programming-model/) and [cooperative groups](/cooperative-groups/).
- [Memory hierarchy](/memory-hierarchy/) and [external memory model](/external-memory-model/): the CPU models count block transfers of size $B$. The GPU counts 32-byte sectors per warp access, a count over the 32 addresses of one instruction rather than over a stream of addresses in time. The [GPU memory hierarchy](/gpu-memory-hierarchy/) page gives the levels.
- [Roofline model](/roofline-model/): it bounds the speed of a kernel from its [arithmetic intensity](/arithmetic-intensity/). The SIMT counts give the numerator and the denominator.

## Known results in the model

- A divergent branch inside a warp costs the sum of its paths, and a branch whose condition is uniform over a warp costs only the path taken (Guide Section 3.2.2.1). See [warp divergence](/warp-divergence/).
- A warp load of 32 consecutive 4-byte words touches 4 sectors of 32 bytes, and a load with a stride of 32 bytes or more touches 32 (Guide Section 2.3.4.1). See [memory coalescing](/memory-coalescing/).
- A sum or a scan over the 32 lanes of a warp takes $\log_2 32 = 5$ shuffle steps with no shared memory and no barrier. See [warp-level primitives](/warp-level-primitives/).
- Shared memory with 32 banks serves a warp access in one pass when no two lanes hit different words in one bank. See [shared memory bank conflicts](/shared-memory-bank-conflicts/).
- Switching between warps costs no time, because each warp keeps its registers on the SM (Guide Section 3.2.2.2). So the SM hides the latency of one warp with the work of others, see [latency hiding](/latency-hiding/).
- The algorithms of the model, such as [parallel reduction](/parallel-reduce/), [prefix sums](/all-prefix-sums/), [stream compaction](/compaction/), [histograms](/parallel-histogram/) and [matrix multiplication](/parallel-matrix-multiplication/), are analysed with these counts.

## References
