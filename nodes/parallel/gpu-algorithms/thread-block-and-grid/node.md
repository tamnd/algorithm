---
tag: GKFCBS
kind: concept
slug: thread-block-and-grid
name: Thread blocks and grids
aliases:
- CUDA thread hierarchy
- cooperative thread arrays
area: parallel/gpu-algorithms
level: intro
summary: A kernel launch is a grid of thread blocks; each thread finds its data from blockIdx, blockDim and threadIdx in 1D, 2D or 3D, and the block size sets warps, occupancy and the scope of shared memory.
prereqs: [cuda-programming-model]
see_also: [simt-model, occupancy, memory-coalescing, gpu-memory-hierarchy, persistent-threads, cooperative-groups, parallel-for]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 2.3.2 (thread hierarchy, the order of threads in 2D and 3D blocks), Section 3.2.2.2 (warps per block) and Section 5.1.3, Table 33 (block and grid size limits)
  - url: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/
    title: NVIDIA, CUDA C++ Best Practices Guide, version 13.5
    locator: Section 11.3 (thread and block heuristics, block sizes as multiples of 32)
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition
    locator: Chapter 3 (multidimensional grids and data, mapping threads to multidimensional data)
---

A **thread block** is a group of up to 1024 GPU threads that run on one streaming multiprocessor and share its fast memory, and a **grid** is the set of all blocks of one kernel launch. Both are 1D, 2D or 3D arrays of indices, so a thread finds the data it owns from its block index, the block size and its index in the block. This page gives the index arithmetic, the grid-stride loop and the size limits of the [CUDA programming model](/cuda-programming-model/). The PTX documents call a block a cooperative thread array (CTA).

## In plain words

Think of a large picture that a thousand painters must paint. You cut the picture into equal tiles and give each team one tile. Inside a team, each painter gets one square of the tile. A painter knows the number of the team and the place in the team, and from these two numbers it finds the square to paint. A team works in one room and can share its paint and wait for each other. Different teams never wait for each other. If the picture does not divide into whole tiles, the last tiles stick out past the edge, and the painters there do nothing. If there are fewer painters than squares, each painter paints a square, then jumps ahead by the number of painters and paints again.

## The idea

### One dimension

A launch with $G$ blocks of $T$ threads gives thread $t$ of block $b$ the global index

$$i = bT + t, \qquad 0 \le b < G, \quad 0 \le t < T.$$

The map $(b, t) \mapsto i$ is a bijection from the launch onto $\{0, \dots, GT - 1\}$, with inverse $b = \lfloor i/T \rfloor$ and $t = i \bmod T$. To cover $n$ items, launch $G = \lceil n/T \rceil$ blocks and guard the body with `if (i < n)`. Then $GT - n < T$ threads are idle.

### Two and three dimensions

Each axis works the same way: `col = blockIdx.x * blockDim.x + threadIdx.x` and `row = blockIdx.y * blockDim.y + threadIdx.y`, and for a $W \times H$ image the grid is $(\lceil W/T_x \rceil, \lceil H/T_y \rceil)$ with the guard `if (col < W && row < H)`. A row-major array element has the offset `row * W + col`.

Inside a block, the threads have a linear rank, with $x$ fastest (Guide Section 2.3.2):

$$r = x + y \cdot T_x + z \cdot T_x T_y.$$

The rank sets the warp: thread $r$ is lane $r \bmod 32$ of warp $\lfloor r/32 \rfloor$. A block of $T_x T_y T_z$ threads has $\lceil T_x T_y T_z / 32 \rceil$ warps (Guide Section 3.2.2.2), and when the size is not a multiple of 32 the last warp has idle lanes. So a $16 \times 16$ block has 8 full warps, and in it each warp covers two rows of 16 threads. Make $x$ the axis of consecutive addresses, so that the lanes of a warp read neighbouring words and the access is [coalesced](/memory-coalescing/).

### The grid-stride loop

A grid-stride loop decouples the grid size from $n$:

```cpp
__global__ void scale(float* x, float a, int n) {
    for (int i = blockIdx.x * blockDim.x + threadIdx.x;
         i < n;
         i += blockDim.x * gridDim.x) {
        x[i] = a * x[i];
    }
}
```

With $P = GT$ threads, thread $g$ visits $g, g + P, g + 2P, \dots$ below $n$. The residues modulo $P$ partition $\{0, \dots, n - 1\}$, so each index is visited by exactly one thread, and each thread runs at most $\lceil n/P \rceil$ iterations. In each iteration the 32 lanes of a warp touch 32 consecutive indices, so the access stays coalesced. The loop also lets one launch with a grid sized to the GPU handle any $n$, which is the base of [persistent threads](/persistent-threads/).

### Limits

The CUDA Programming Guide v13.5, Section 5.1.3, Table 33, gives the same size limits for every compute capability that it lists (7.5 to 12.x):

| Limit | Value |
|---|---|
| threads per block | 1024 |
| block size in x, y, z | 1024, 1024, 64 |
| grid size in x, y, z | $2^{31} - 1$, 65535, 65535 |
| warp size | 32 |

The limits per SM do change with the generation. The same table gives, for example, at most 32 resident blocks and 64 resident warps per SM for compute capability 8.0 (A100) and 9.0 (H100), and 24 blocks and 48 warps for 8.9 and 12.x. These numbers set the [occupancy](/occupancy/), so check the table for the target GPU.

### Choosing the block size

- Use a multiple of 32, so that no warp has idle lanes (Best Practices Guide Section 11.3).
- A very small block wastes the SM: at most a fixed number of blocks fit on one SM, so on compute capability 8.0, blocks of 32 threads fill at most $32 \cdot 32 = 1024$ of the 2048 thread slots, which is 50% [occupancy](/occupancy/).
- A large block uses more registers and shared memory at once, so fewer blocks fit, and the SM idles more at each `__syncthreads()`.
- Use 2D blocks for 2D data when the threads share a 2D tile, as in [shared memory tiling](/shared-memory-tiling/).
- Launch at least as many blocks as the GPU has SMs, and preferably several times more, so that the load is balanced.

## Examples

- **Vector of $n = 1000$ items, $T = 256$:** $G = 4$, 1024 threads, 24 idle threads in block 3.
- **Image of $1000 \times 600$ pixels, blocks of $16 \times 16$:** the grid is $(\lceil 1000/16 \rceil, \lceil 600/16 \rceil) = (63, 38)$, so $63 \cdot 38 = 2394$ blocks of 256 threads. That is $612{,}864$ threads for $600{,}000$ pixels, and the guard idles $12{,}864$ of them.
- **Block of 100 threads:** 4 warps, and the last warp has 28 idle lanes, so 22% of the issue slots of that block carry no thread.
- **Grid-stride loop:** with 3 blocks of 64 threads and $n = 1000$, $P = 192$ and each thread runs $\lceil 1000/192 \rceil = 6$ or fewer iterations.
- **A non-example:** a launch `<<<1, dim3(32, 32, 2)>>>` asks for 2048 threads in one block and fails, because the limit is 1024 threads per block.

The Python code of this page computes the indices of every thread of a launch. The tests check that the linear rank is a bijection with $x$ fastest, that a guarded 2D grid covers a matrix exactly once, that the grid-stride loop visits each index once with at most $\lceil n/P \rceil$ steps per thread, and the limits of Table 33. The CUDA code on this page is for the reader; the tests do not run it.

## Where it is used

Every kernel uses this arithmetic. Element-wise kernels such as the vector add of the [CUDA programming model](/cuda-programming-model/) use 1D grids, and image and matrix kernels such as [parallel matrix transpose](/parallel-matrix-transpose/), [stencil computation](/stencil-computation/) and [parallel matrix multiplication](/parallel-matrix-multiplication/) use 2D grids with 2D blocks. Block-level algorithms, such as the block stage of a [parallel reduction](/parallel-reduce/) or a [scan](/all-prefix-sums/), depend on the block as the unit that shares memory and a barrier. The block is also the unit of scheduling and of resource use, so the block size enters [occupancy](/occupancy/), and the grid-stride loop is the base of [persistent threads](/persistent-threads/). [Cooperative groups](/cooperative-groups/) name the same levels as objects and add smaller tiles inside a block.

## References
