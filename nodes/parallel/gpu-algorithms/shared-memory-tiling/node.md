---
tag: BZ60WH
kind: technique
slug: shared-memory-tiling
name: Shared memory tiling
aliases:
- tiling
- blocking for GPUs
area: parallel/gpu-algorithms
level: core
summary: A block loads a tile of input into shared memory once, waits at a barrier, and reuses it many times; T by T tiles cut the global loads of matrix multiplication by a factor of T.
prereqs: [gpu-memory-hierarchy, thread-block-and-grid, naive-matrix-multiplication]
see_also: [blocked-matrix-multiplication, parallel-matrix-multiplication, stencil-computation, parallel-matrix-transpose, shared-memory-bank-conflicts, arithmetic-intensity, red-blue-pebble-game, occupancy]
sources:
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition
    locator: Chapter 5 (memory architecture and data locality, the tiled matrix multiplication kernel and its two barriers) and Chapter 6 (thread coarsening)
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 2.3.3.2 (shared memory), Section 2.3.4.2.1 (a transpose through shared memory and why __syncthreads is needed) and Section 5.4.4.1 (__syncthreads in conditional code)
  - url: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/
    title: NVIDIA, CUDA C++ Best Practices Guide, version 13.5
    locator: Section 10.2 (device memory spaces) and the subsection on shared memory in matrix multiplication
  - url: https://www.nvidia.com/content/gtc-2010/pdfs/2238_gtc2010.pdf
    title: Vasily Volkov, Better performance at lower occupancy, GPU Technology Conference 2010
    locator: slides 54 to 58 (matrix multiply with more outputs per thread)
---

**Shared memory tiling** is the technique of loading a tile of the input from global memory into the shared memory of a [thread block](/thread-block-and-grid/) once, and then using every element of the tile many times from there. Global memory is far and shared memory is near (see [GPU memory hierarchy](/gpu-memory-hierarchy/)), so the reuse cuts the global traffic. For matrix multiplication with $T \times T$ tiles, each element of the inputs is loaded $n/T$ times instead of $n$ times, so the global loads drop by a factor of $T$. It is the GPU form of [blocked matrix multiplication](/blocked-matrix-multiplication/), with a fast memory that the program manages itself and two barriers per phase.

## In plain words

A team builds a wall from bricks that sit in a yard far away. If every worker walks to the yard for each brick, most of the time goes into walking, and the same brick is fetched again and again by different workers. Instead, the team brings one cart of bricks to the site, everyone takes what they need from the cart, and then they fetch the next cart. Two rules keep this right. Nobody takes from the cart before it is full. And nobody empties the cart for the next load while a worker still takes bricks from it. So the team waits for each other twice for each cart: once after the cart is loaded and once after it is used.

## When it applies

- Each input element is used by many threads of one block, or many times by one thread. Without reuse, a tile only adds a copy.
- The reuse can be grouped into tiles that fit in shared memory, with room left for enough resident blocks (see [occupancy](/occupancy/)). On compute capability 8.0 (A100), a block can use up to 163 KB of shared memory and an SM up to 164 KB (CUDA Programming Guide v13.5, Table 34); these limits change between generations.
- The access to global memory can be arranged so that consecutive threads load consecutive words, so the tile loads are [coalesced](/memory-coalescing/).
- The cost model is the GPU model of the Parallel area: the [SIMT model](/simt-model/) with counts of global loads and of barriers, and the [roofline model](/roofline-model/) to turn traffic into time. The notation: $n$ is the matrix size, $T$ the tile size, $M$ the shared memory per block in words, and $W$ and $S$ the work and span.

## The template

```pseudo id=main
TILED-KERNEL(block b)                       ▷ every thread of block b runs this
L1  acc ← 0                                 ▷ per-thread accumulator in registers
L2  for p ← 0 to P − 1 do                   ▷ one phase per input tile
L3      each thread loads its share of tile p from global memory into shared memory
L4      BARRIER                             ▷ the tile is complete before anyone reads it
L5      each thread updates acc from the tile in shared memory
L6      BARRIER                             ▷ everyone is done before L3 overwrites the tile
L7  each thread writes acc to global memory
```

### Tiled matrix multiplication

Let $C = AB$ with $A$ of size $m \times k$ and $B$ of size $k \times n$. A block of $T \times T$ threads computes one $T \times T$ tile of $C$; thread $(t_x, t_y)$ of block $(b_x, b_y)$ owns $C[b_y T + t_y][b_x T + t_x]$. Phase $p$ loads the tile of $A$ at rows $b_y T, \dots, b_y T + T - 1$ and columns $pT, \dots, pT + T - 1$, and the tile of $B$ at rows $pT, \dots, pT + T - 1$ and columns $b_x T, \dots, b_x T + T - 1$. Each thread loads one element of each tile.

```cpp
#define T 16
__global__ void matmulTiled(const float* A, const float* B, float* C, int m, int k, int n) {
    __shared__ float As[T][T], Bs[T][T];
    int tx = threadIdx.x, ty = threadIdx.y;
    int row = blockIdx.y * T + ty, col = blockIdx.x * T + tx;
    float acc = 0.0f;
    for (int p = 0; p < (k + T - 1) / T; ++p) {
        int ac = p * T + tx, br = p * T + ty;
        As[ty][tx] = (row < m && ac < k) ? A[row * k + ac] : 0.0f;   // coalesced in tx
        Bs[ty][tx] = (br < k && col < n) ? B[br * n + col] : 0.0f;   // coalesced in tx
        __syncthreads();                       // barrier 1: read after write
        for (int j = 0; j < T; ++j)
            acc += As[ty][j] * Bs[j][tx];      // As: broadcast, Bs: one row, no bank conflict
        __syncthreads();                       // barrier 2: write after read
    }
    if (row < m && col < n) C[row * n + col] = acc;
}
// launch: dim3 block(T, T); dim3 grid((n + T - 1) / T, (m + T - 1) / T);
```

**The traffic, derived.** The untiled kernel ([naive matrix multiplication](/naive-matrix-multiplication/) with one thread per output) loads a row of $A$ and a column of $B$ for each of the $mn$ outputs, which is $2mnk$ global loads. In the tiled kernel, the element $A[i][j]$ is loaded once by each block in block row $\lfloor i/T \rfloor$, and there are $\lceil n/T \rceil$ such blocks. The element $B[i][j]$ is loaded once by each of the $\lceil m/T \rceil$ blocks in block column $\lfloor j/T \rfloor$. So the tiled kernel makes

$$L_{\text{tiled}} = mk \left\lceil \frac{n}{T} \right\rceil + kn \left\lceil \frac{m}{T} \right\rceil$$

global loads. For square matrices with $T \mid n$, this is $2n^3/T$, a factor of $T$ below $2n^3$. The shared memory per block is $2T^2$ words, so $T$ is at most about $\sqrt{M/2}$, and the traffic is $O(n^3/\sqrt{M})$, the order of the lower bound of Hong and Kung for this class of algorithms (see the [red-blue pebble game](/red-blue-pebble-game/)).

**The arithmetic intensity.** The kernel does $2n^3$ floating-point operations, so with 4-byte floats its intensity with respect to global loads is $2n^3 / (4 \cdot 2n^3/T) = T/4$ FLOP per byte. For $T = 16$ that is 4, and for $T = 32$ it is 8. The ridge point of an A100 for FP32 is about 12.5 FLOP per byte (see the [roofline model](/roofline-model/)), so shared memory tiling alone leaves the kernel memory bound in this model, which is why fast kernels add register tiling (below). The L2 cache can serve some of the repeated tile loads, so the traffic to DRAM may be lower than $L_{\text{tiled}}$.

**Why both barriers are needed.** At L5, thread $(t_x, t_y)$ reads `As[ty][j]`, which thread $(j, t_y)$ wrote, and `Bs[j][tx]`, which thread $(t_x, j)$ wrote. Without barrier 1, it can read before the writer has written, a read-after-write race. At L3 of the next phase, thread $(t_x, t_y)$ overwrites `As[ty][tx]`, which threads $(t_x', t_y)$ still read in L5 of this phase. Without barrier 2, a fast thread can overwrite a value that a slow thread has not yet used, a write-after-read race. The Python simulator runs the threads of a block one after another between barriers, which is one legal schedule, and under it both broken versions give wrong products.

**Work and span.** The work is the $mnk$ multiply-adds of the triple loop. The span of one block is $\lceil k/T \rceil$ phases of $T$ steps each, plus $2 \lceil k/T \rceil$ barriers, so $S = \Theta(k)$, the same as the untiled kernel.

The Python code of this page runs the tiled kernel on a SIMT simulator with $T \times T$ threads per block, shared tiles as lists and `yield` as the barrier. The tests compare it with the triple loop on exact integers for many shapes, including sizes that are not multiples of $T$; check its global load count against $L_{\text{tiled}}$; check $L_{\text{tiled}} \cdot T = 2n^3$ for square matrices; and show that removing either barrier gives a wrong product. The CUDA code on this page is for the reader; the tests do not run it.

## Classic examples

- [Parallel matrix multiplication](/parallel-matrix-multiplication/): the kernel above, and the base of GPU GEMM libraries together with register tiling and [tensor cores](/tensor-cores/).
- [Stencil computation](/stencil-computation/): a block loads a tile plus a halo of neighbours, and each loaded point is used by up to as many outputs as the stencil has points.
- [Parallel matrix transpose](/parallel-matrix-transpose/): the tile gives no reuse, but it lets the block read rows and write rows, so both global accesses are coalesced; padding the tile avoids [bank conflicts](/shared-memory-bank-conflicts/).
- [Parallel histogram](/parallel-histogram/): each block keeps a private histogram in shared memory and merges it into the global one at the end, which cuts the global atomic operations.
- [Blocked matrix multiplication](/blocked-matrix-multiplication/): the CPU form, with the cache in place of shared memory and no barriers.

## Variations

- **Register tiling (thread coarsening).** Each thread computes a $r \times r$ block of outputs in registers. Then one element loaded from shared memory feeds $r$ multiply-adds, and the block computes a $Tr \times Tr$ tile, so the global intensity rises to about $Tr/4$ FLOP per byte. Volkov's GTC 2010 talk shows a matrix multiply that gets faster with more outputs per thread at lower [occupancy](/occupancy/).
- **Double buffering.** Two copies of each tile alternate. Phase $p$ computes on one copy while the loads of phase $p + 1$ go to the other, so one barrier per phase is enough and load latency overlaps with compute. On compute capability 8.0 and later, asynchronous copies from global to shared memory support this directly.
- **Rectangular tiles.** Tiles of $T_m \times T_k$ and $T_k \times T_n$ let the shapes fit the block size, the shared memory and the register budget separately.
- **Halo tiles.** For stencils, a block of $T$ outputs loads $T + 2r$ inputs for a stencil of radius $r$; the halo is the overhead.
- **Tiling for the cache only.** On recent GPUs the L1 cache can capture some reuse without shared memory. Explicit tiling stays more predictable.

## Pitfalls

- **A missing barrier.** Each of the two barriers guards a different race, as shown above. Both races may stay hidden in tests on small inputs and appear on other GPUs or other block counts.
- **A barrier in divergent code.** `__syncthreads()` is allowed in conditional code only when the condition is the same in every thread of the block (Programming Guide Section 5.4.4.1). A kernel that does `if (row >= m || col >= n) return;` before the phase loop breaks this rule at the edge of the matrix. Guard the loads and the final store, and let every thread run every phase, as the kernel above does.
- **Edge tiles.** When $T$ does not divide the sizes, out-of-range tile entries must be set to zero, or the products pick up garbage.
- **Bank conflicts.** A warp that reads a column of a tile has a 32-way conflict. Choose the layout so that warps read rows or broadcasts, or pad the tile.
- **Too large a tile.** A large tile raises the reuse, but it uses more shared memory per block, so fewer blocks fit on an SM, and the GPU may not hide latency. The best $T$ is found by measurement.
- **Counting the wrong traffic.** $L_{\text{tiled}}$ counts loads issued to global memory. DRAM traffic can be lower because of the L2 cache, and the true bound may be the shared memory bandwidth or the issue rate, not DRAM.

## Exercises

1. For $m = 1000$, $k = 600$, $n = 800$ and $T = 16$, compute $L_{\text{tiled}}$ and compare it with $2mnk$.
2. Show that with $r \times r$ register tiling inside $T \times T$ thread blocks, the global loads for square matrices are $2n^3/(Tr)$ when $Tr \mid n$.
3. Rewrite the kernel with two shared buffers so that it needs one barrier per phase, and explain why the remaining barrier is enough.

## References
