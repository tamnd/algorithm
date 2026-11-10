---
tag: B6F7V7
kind: concept
slug: arithmetic-intensity
name: Arithmetic intensity
aliases:
- operational intensity
area: parallel/gpu-algorithms
level: core
summary: FLOP done per byte moved through a level of memory; it is 1/12 for an FP32 vector add, near 1/2 for a matrix-vector product and T/4 for a tiled matrix product.
prereqs: [gpu-memory-hierarchy]
see_also: [roofline-model, shared-memory-tiling, kernel-fusion, memory-coalescing, matrix-vector-multiplication, blocked-matrix-multiplication, sparse-matrix-vector-multiplication, stencil-computation]
sources:
  - paper: doi:10.1145/1498765.1498785
    title: Samuel Williams, Andrew Waterman and David Patterson, Roofline, an insightful visual performance model for multicore architectures, Communications of the ACM 52(4), 2009
    locator: the definition of operational intensity as operations per byte of DRAM traffic, measured after the caches filter the accesses
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition
    locator: Chapter 5 (memory architecture and data locality, the ratio of floating-point operations to global memory traffic and its effect on the tiled matrix multiplication kernel)
  - url: https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf
    title: NVIDIA, NVIDIA A100 Tensor Core GPU Architecture (whitepaper), 2020
    locator: the A100 specification table (peak FP32 19.5 TFLOPS, 1555 GB/s HBM2 for the 40 GB part)
---

The **arithmetic intensity** of a kernel is the number of floating-point operations that it does per byte that it moves through a level of memory:

$$I = \frac{W}{Q} \quad \text{FLOP/byte}.$$

Williams, Waterman and Patterson call it operational intensity and fix the level as DRAM. The intensity of a kernel, compared with the ridge point of a machine, tells whether the kernel is limited by memory bandwidth or by compute. The [roofline model](/roofline-model/) turns $I$ into an attainable rate; this page derives $I$ for common kernels.

## In plain words

A cook works in a kitchen, and a helper carries food from a store room. Some dishes need a lot of cutting and cooking but little food. For these, the cook sets the pace. Other dishes need a lot of food but almost no work, like a bowl that is only filled. For these, the helper sets the pace, and a faster cook changes nothing. Arithmetic intensity is the amount of work per amount of food carried. A modern processor is a very fast cook with a slow helper. So a fast program often changes its recipe so that each item it brings in is used many times before it goes back.

## The idea

### What is counted

- $W$ counts floating-point operations. A multiply-add counts as 2. Integer and index operations are not counted.
- $Q$ counts the bytes that cross one memory link, usually the link between the chip and DRAM (HBM or GDDR on a GPU). It counts the bytes that the memory actually moves, after the caches have filtered the accesses. So $Q$ depends on the cache sizes, and $I$ is a property of a kernel on a machine, not of the algorithm alone.
- Two counts bracket $Q$. The **compulsory** count moves each distinct word once; it is a lower bound on $Q$ and so an upper bound on $I$. The **no-cache** count sends every load to memory.
- An element of FP32 has 4 bytes and an element of FP64 has 8 bytes. With the same $W$, FP64 halves $I$ and FP16 doubles it.
- Memory moves whole sectors, not single words. An access pattern that is not [coalesced](/memory-coalescing/) moves bytes that the kernel does not use, which raises $Q$ and lowers $I$.

The derivations below use FP32 and give the limit for large $n$. The kernels are shown in CUDA C++.

### Vector add

```cpp
__global__ void vecAdd(const float* a, const float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];          // 1 FLOP; load 8 bytes, store 4 bytes
}
```

$W = n$ and $Q = 4n + 4n + 4n = 12n$, so $I = 1/12$. In FP64 it is $1/24$. Each word is used once, so no cache can change $Q$.

### Dot product

```cpp
__global__ void dot(const float* x, const float* y, float* out, int n) {
    float s = 0.0f;
    for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n; i += gridDim.x * blockDim.x)
        s += x[i] * y[i];                   // 2 FLOP; load 8 bytes
    s = blockReduce(s);                     // any block reduction, see parallel-reduce
    if (threadIdx.x == 0) atomicAdd(out, s);
}
```

$W = 2n$ and $Q = 8n + 4$ for one result, so

$$I = \frac{2n}{8n + 4} \to \frac{1}{4}.$$

The partial results of the blocks add a few bytes per block, which do not change the limit. In FP64 the limit is $1/8$. The [dot product](/dot-product/) has three times the intensity of the vector add, because it does two operations per element and writes no output array.

### Matrix-vector product

```cpp
__global__ void matvec(const float* A, const float* x, float* y, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;      // one thread per row
    if (i >= n) return;
    float s = 0.0f;
    for (int j = 0; j < n; ++j) s += A[i * n + j] * x[j];   // 2 FLOP; A[i][j] is used once
    y[i] = s;
}
```

For an $n \times n$ matrix, $W = 2n^2$. If $x$ comes from memory once, because a cache or shared memory holds it, then $Q = 4(n^2 + n + n)$ and

$$I = \frac{2n^2}{4n^2 + 8n} = \frac{n}{2n + 4} \to \frac{1}{2}.$$

For $n = 1000$ this is $1000/2004 \approx 0.499$. If $x$ comes from memory again for every row, $Q = 4(2n^2 + n)$ and $I \to 1/4$. Each element of $A$ is used once for 2 FLOP, so $I \le 1/2$ in FP32 whatever the cache does (1/4 in FP64). The simple kernel above reads $A$ with a stride of $n$ words between adjacent threads; a column-major layout or one warp per row makes the reads coalesced. See [matrix-vector multiplication](/matrix-vector-multiplication/).

### Matrix multiplication

For $C = AB$ with $n \times n$ matrices, $W = 2n^3$.

- **No reuse.** One thread per output reads its row of $A$ and its column of $B$ from memory: $Q = 4(2n^3 + n^2)$ and $I \to 1/4$.
- **Shared-memory tiles.** With [tiles](/shared-memory-tiling/) of $T \times T$, a block computes $T \times T$ outputs in $n/T$ phases. Each phase loads one tile of $A$ and one tile of $B$, $2T^2$ words, so a block loads $2Tn$ words. There are $(n/T)^2$ blocks, so the loads are $2n^3/T$ words, and the stores are $n^2$ words:

$$Q = 4\left(\frac{2n^3}{T} + n^2\right), \qquad I = \frac{2n}{8n/T + 4} \to \frac{T}{4}.$$

  The limit is 4 FLOP/byte for $T = 16$ and 8 FLOP/byte for $T = 32$. For $n = 4096$ and $T = 32$, $I \approx 7.97$.
- **Compulsory traffic.** If each word of $A$, $B$ and $C$ crosses the link once, $Q = 12n^2$ and $I = n/6$.

With a fast memory of $M$ words, a tiled schedule reaches $I = \Theta(\sqrt{M})$, and the [red-blue pebble game](/red-blue-pebble-game/) shows that no schedule of the standard algorithm does better by more than a constant factor ([blocked matrix multiplication](/blocked-matrix-multiplication/)). Of the kernels on this page, only matrix multiplication has an intensity that grows with the size of the fast memory.

## Examples

| Kernel (FP32) | $W$ | $Q$ in bytes | $I$ for large $n$ |
|---|---|---|---|
| vector add | $n$ | $12n$ | 1/12 |
| dot product | $2n$ | $8n + 4$ | 1/4 |
| matrix-vector, $x$ read once | $2n^2$ | $4n^2 + 8n$ | 1/2 |
| matrix product, no reuse | $2n^3$ | $8n^3 + 4n^2$ | 1/4 |
| matrix product, tiles of $T$ | $2n^3$ | $8n^3/T + 4n^2$ | $T/4$ |
| matrix product, compulsory | $2n^3$ | $12n^2$ | $n/6$ |

- **Against a ridge point.** The A100 40 GB has a peak of 19.5 TFLOP/s in FP32 and 1555 GB/s of HBM2 bandwidth (A100 whitepaper, specification table), so its ridge point is about 12.54 FLOP/byte. Every kernel in the table except the matrix product with large tiles or high reuse is far below it and is memory-bound on this GPU. The tiled product needs $T/4 \ge 12.54$, that is $T \ge 51$, if the L2 cache gives no extra reuse. The ridge point changes between GPU generations and precisions; the [roofline model](/roofline-model/) page has more cases.
- **Fusion.** Two kernels $d = a + b$ and then $e = d \cdot c$ do $2n$ FLOP and move $12n + 12n = 24n$ bytes, so $I = 1/12$. One [fused kernel](/kernel-fusion/) $e = (a + b) \cdot c$ keeps $d$ in a register and moves $16n$ bytes, so $I = 1/8$, and the memory-bound time drops by a third.
- **Sparse matrix-vector product in CSR.** Assume FP64 values, 4-byte column indices and row pointers, and 10 nonzeros per row. Each nonzero needs an 8-byte value, a 4-byte index and an 8-byte read of $x$ when $x$ is not reused, for 2 FLOP. Each row adds a 4-byte row pointer and an 8-byte write of $y$. So a row does 20 FLOP for 212 bytes, $I \approx 0.094$. Even if every read of $x$ hits in a cache, a row moves 132 bytes and $I \approx 0.152$, and the limit for long rows is $2/12 = 1/6$. See [compressed sparse row](/compressed-sparse-row/) and [sparse matrix-vector multiplication](/sparse-matrix-vector-multiplication/).

The Python code of this page computes $W$ and $Q$ for each kernel in two ways: from the closed forms above, and by walking the loops of the kernel and counting each access under the stated cache assumption. The tests check that the two ways agree for several sizes and tile widths, and check every intensity on this page with exact fractions. The tests do not run the CUDA code.

## Where it is used

- The [roofline model](/roofline-model/) uses $I$ as its horizontal axis to bound the rate of a kernel.
- [Shared-memory tiling](/shared-memory-tiling/) raises the intensity of the matrix product from $1/4$ to $T/4$ against DRAM. Computing several outputs per thread from registers raises it again against shared memory.
- [Kernel fusion](/kernel-fusion/) raises $I$ by keeping intermediate values on the chip.
- [Stencil computation](/stencil-computation/) raises $I$ by loading a tile with its halo once and, with temporal blocking, by doing several time steps per load.
- Sparse formats such as [ELLPACK](/ellpack-format/) and [CSR](/compressed-sparse-row/) differ in the bytes of index data per nonzero, which sets the intensity of the sparse product.
- A lower precision moves fewer bytes per element, which is one reason the [tensor cores](/tensor-cores/) work on FP16 and similar formats.
- On CPUs the same count guides cache blocking in the [memory hierarchy](/memory-hierarchy/), as in [blocked matrix multiplication](/blocked-matrix-multiplication/).

## References
