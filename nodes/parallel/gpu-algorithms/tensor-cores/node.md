---
tag: 65S74S
kind: concept
slug: tensor-cores
name: Tensor cores
aliases:
- matrix units
- matrix-multiply-accumulate units
- MMA units
- WMMA
area: parallel/gpu-algorithms
level: advanced
summary: Units in NVIDIA GPUs that compute D = A x B + C on small matrix tiles per warp, with low-precision inputs and a wider accumulator, at many times the rate of the ordinary cores.
prereqs: [simt-model, parallel-matrix-multiplication, floating-point-arithmetic]
see_also: [parallel-matrix-multiplication, shared-memory-tiling, roofline-model, arithmetic-intensity, fused-multiply-add, numerical-stability, ieee-754, warp-specialization]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 5.4.11, Warp Matrix Functions (D = A*B + C on compute capability 7.0 and higher; the fragment type, load_matrix_sync, store_matrix_sync, fill_fragment and mma_sync; the unspecified mapping of fragment elements to threads; 256-bit pointer alignment and ldm a multiple of 16 bytes; the table of element types and shapes)
  - url: https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf
    title: NVIDIA, Tesla V100 GPU Architecture, whitepaper WP-08608-001_v1.1, 2017
    locator: Table 1 (640 tensor cores, GPU Boost clock 1530 MHz, 125 tensor TFLOPS based on the boost clock) and the section on tensor cores (8 per SM, each does 64 FMA operations per clock on 4x4 matrices)
  - url: https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf
    title: NVIDIA, NVIDIA A100 Tensor Core GPU Architecture, whitepaper, 2020
    locator: the A100 SM section (4 third-generation tensor cores per SM, each does 256 FP16/FP32 FMA operations per clock; 108 SMs and 432 tensor cores give up to 312 TFLOPS) and the comparison table (GPU boost clock 1410 MHz)
  - url: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf
    title: NVIDIA, A100 Tensor Core GPU datasheet
    locator: the specifications table (FP64 tensor core 19.5 TFLOPS, TF32 156 TFLOPS, BF16 and FP16 312 TFLOPS, INT8 624 TOPS, and the doubled figures with sparsity)
  - paper: doi:10.7717/peerj-cs.330
    title: Massimiliano Fasi, Nicholas J. Higham, Mantas Mikaitis and Srikara Pranesh, Numerical behavior of NVIDIA tensor cores, PeerJ Computer Science 7, e330, 2021
    locator: the tests on V100, T4 and A100 of the internal precision, the rounding of the sums, the order of the additions and the normalization of partial sums
  - url: https://arxiv.org/abs/1803.04014
    title: Stefano Markidis, Steven Wei Der Chien, Erwin Laure, Ivy Bo Peng and Jeffrey S. Vetter, NVIDIA tensor core programmability, performance and precision, 2018
    locator: the WMMA and cuBLAS programming interfaces, the measured throughput on a V100, and the study of the error of half-precision inputs
---

Tensor cores are units in NVIDIA GPUs, from the Volta generation (compute capability 7.0) on, that do one operation very fast: a matrix multiply-accumulate $D = A \times B + C$ on small tiles. The inputs $A$ and $B$ are usually in a low precision such as FP16, BF16 or TF32, and the accumulator $C$ and the result $D$ are often in FP32. This is mixed precision. In CUDA C++, a whole warp of 32 threads does one operation together through the WMMA API: each thread holds a part of each tile in a fragment, and `mma_sync` does the multiply-accumulate. A dense matrix product of large size breaks into many such tile operations. On these GPUs, the tensor cores give a much higher peak rate than the ordinary cores. The cost is the lower precision of the inputs, a fixed tile shape, and the need to feed the units fast enough from memory.

## In plain words

An ordinary GPU core is like a worker who multiplies two numbers and adds a third, one at a time. A tensor core is like a machine that takes two small grids of numbers and multiplies the whole grids in one step. The machine is very fast, but it has rules. It only takes grids of certain fixed sizes. It reads the input numbers with fewer digits, so each input is slightly rounded. It keeps the running total with more digits, so that the small errors do not pile up too fast. And it is so fast that the main problem is often to bring it the numbers quickly enough.

## The idea

The cost model is the [SIMT model](/simt-model/) with warps of 32 threads, and the [roofline model](/roofline-model/) for the balance of arithmetic and memory traffic.

| symbol | meaning |
|---|---|
| $n$ | the size of the input; here the matrices are $m \times k$ and $k \times n$ |
| $p$ | the number of processors |
| $W$, $S$, $T_p$ | the work, the span and the time on $p$ processors |
| $M$, $B$ | the fast memory size and the memory transaction size (the matrix $B$ is the second input) |
| $\mu \times \nu \times \kappa$ | the fragment shape: $A$ tile $\mu \times \kappa$, $B$ tile $\kappa \times \nu$, $C$ and $D$ tiles $\mu \times \nu$ |
| $t$ | the number of significand bits of a format, with the hidden bit |
| $u = 2^{-t}$ | the unit roundoff of a format |
| $b$ | the side of a square output tile that one block computes |

**The operation.** One tensor core operation is $D = A \times B + C$ for fixed tile sizes. In the Volta V100, each tensor core does 64 fused multiply-adds per clock on $4 \times 4$ matrices, and each SM has 8 tensor cores (Volta whitepaper). The programmer does not see the $4 \times 4$ unit directly. CUDA C++ shows a warp-level operation on larger tiles, and the compiler maps it to the hardware instructions, which change between generations.

**The WMMA API.** The CUDA Programming Guide 13.5, Section 5.4.11, describes the warp matrix functions in the namespace `nvcuda::wmma`:

- `fragment<Use, m, n, k, T, Layout>`: a tile held across the 32 threads of a warp. `Use` is `matrix_a`, `matrix_b` or `accumulator`. The guide says that the mapping of matrix elements into the fragment is unspecified, and code must not depend on it.
- `load_matrix_sync` and `store_matrix_sync`: load or store a tile from memory. The pointer must be 256-bit aligned, and the leading dimension `ldm` must be a multiple of 16 bytes.
- `fill_fragment`: set all elements of a fragment to one value.
- `mma_sync(d, a, b, c)`: compute $D = A \times B + C$.

All these calls are collective: every thread of the warp must make the same call. The shapes in the guide (version 13.5, Section 5.4.11) include:

| inputs $A$, $B$ | accumulator $C$, $D$ | shapes $\mu \times \nu \times \kappa$ | note |
|---|---|---|---|
| `half` (FP16) | `float` or `half` | $16 \times 16 \times 16$, $32 \times 8 \times 16$, $8 \times 32 \times 16$ | from compute capability 7.0 |
| `__nv_bfloat16` | `float` only | $16 \times 16 \times 16$, $32 \times 8 \times 16$, $8 \times 32 \times 16$ | |
| `precision::tf32` | `float` | $16 \times 16 \times 8$ | inputs are converted with `__float_to_tf32` |
| `double` | `double` | $8 \times 8 \times 4$ | |
| `unsigned char`, `signed char` | `int` | $16 \times 16 \times 16$, $32 \times 8 \times 16$, $8 \times 32 \times 16$ | |
| 4-bit and 1-bit integers | `int` | $8 \times 8 \times 32$, $8 \times 8 \times 128$ | experimental |

Which types a given GPU supports depends on its compute capability, and newer GPUs add instructions that work on larger groups of threads. The table holds for this guide version.

**Mixed precision and its effect.** The formats differ in significand bits $t$ and in range:

| format | significand bits $t$ | unit roundoff $u$ | largest finite value |
|---|---|---|---|
| FP16 | 11 | $2^{-11}$ | 65 504 |
| BF16 | 8 | $2^{-8}$ | about $3.4 \times 10^{38}$, as FP32 |
| TF32 | 11 | $2^{-11}$ | about $3.4 \times 10^{38}$, as FP32 |
| FP32 | 24 | $2^{-24}$ | about $3.4 \times 10^{38}$ |

Two kinds of error come in. First, each input is rounded once to the input format, with a relative error of at most $u$ of that format. Second, the sum of $k$ products is rounded as it grows. The product of two FP16 numbers has at most 22 significand bits, so it fits exactly in FP32. If the sum is done one term at a time with unit roundoff $u$, the error is at most $\gamma_k \sum_i |a_i b_i|$ with $\gamma_k = k u / (1 - k u)$. With an FP16 accumulator, $k u$ reaches 1 at $k = 2048$, and the bound says nothing. With an FP32 accumulator, $k u = 1024 \cdot 2^{-24} = 2^{-14}$ for $k = 1024$. That is the reason for a wide accumulator. Real tensor cores do not round each sum in this simple way: Fasi, Higham, Mikaitis and Pranesh (2021) found on V100, T4 and A100 cards that several products are added together with an internal significand of about 27 or 28 bits and with truncation instead of round to nearest. The Python model below uses one rounding per addition, so it shows the effect of the accumulator format but not the exact bits of any GPU.

**Peak rates.** A peak rate is the number of units times the multiply-adds per clock times 2 operations times the clock. This is a property of one product, not of tensor cores in general, and it changes with each generation:

- Tesla V100 (Volta whitepaper, Table 1): $640 \times 64 \times 2 \times 1530 \text{ MHz} = 125\,337\,600 \times 10^6$ operations per second, which the whitepaper gives as 125 tensor TFLOPS.
- A100 (Ampere whitepaper): $432 \times 256 \times 2 \times 1410 \text{ MHz} = 311\,869\,440 \times 10^6$, given as 312 TFLOPS for dense FP16. The A100 datasheet gives 156 TFLOPS for TF32, 312 for BF16, 19.5 for FP64 on tensor cores, and twice the FP16 figure with structured sparsity.

Measured rates are lower. Markidis and others measured up to 83 TFLOPS on a V100 in their 2018 tests.

**Feeding the units.** A block that computes a $b \times b$ tile of $D$ reads a $b \times \kappa$ panel of $A$ and a $\kappa \times b$ panel of $B$ for each step of depth $\kappa$. It does $2 b^2 \kappa$ operations and reads $2 b \kappa$ input values, so with 2-byte inputs its intensity is $b/2$ operations per byte. A $16 \times 16$ tile gives 8, and a $128 \times 128$ tile gives 64. The roofline ridge point is the peak divided by the memory bandwidth. As an assumption for this example only, take a peak of 312 TFLOPS and a bandwidth of 2 TB/s: the ridge is 156 operations per byte. So tiles must be large and reused from [shared memory](/shared-memory-tiling/) and the L2 cache, or the tensor cores wait for memory. Fast kernels also overlap the loads with the math, for example with [warp specialization](/warp-specialization/).

The CUDA C++ kernel below lets each warp compute one $16 \times 16$ tile of $C$. It reads $A$ and $B$ straight from global memory, so it is simple but far from the peak. The tests do not run this CUDA code. They run a Python model of the rounding, the tile counts and the peak formulas.

```cuda
#include <mma.h>
using namespace nvcuda;

// C (M x N, float, row-major) = A (M x K, half, row-major) x B (K x N, half, column-major) + C.
// One warp computes one 16 x 16 tile of C. M, N and K are multiples of 16.
// blockDim.x is a multiple of 32, so all threads of a warp take the same branch.
__global__ void wmma_gemm(const half* A, const half* B, float* C, int M, int N, int K) {
    int warp = (blockIdx.x * blockDim.x + threadIdx.x) / 32;
    int tm = warp / (N / 16), tn = warp % (N / 16);
    if (tm >= M / 16) return;

    wmma::fragment<wmma::matrix_a, 16, 16, 16, half, wmma::row_major> a;
    wmma::fragment<wmma::matrix_b, 16, 16, 16, half, wmma::col_major> b;
    wmma::fragment<wmma::accumulator, 16, 16, 16, float> acc;

    float* c = C + tm * 16 * N + tn * 16;
    wmma::load_matrix_sync(acc, c, N, wmma::mem_row_major);
    for (int k = 0; k < K; k += 16) {
        wmma::load_matrix_sync(a, A + tm * 16 * K + k, K);   // 16 x 16 tile of A
        wmma::load_matrix_sync(b, B + tn * 16 * K + k, K);   // 16 x 16 tile of B
        wmma::mma_sync(acc, a, b, acc);                      // acc = a x b + acc
    }
    wmma::store_matrix_sync(c, acc, N, wmma::mem_row_major);
}
```

## Examples

**Rounding of one input.** The number $0.1$ has no exact binary form. In FP16 and in TF32 it becomes $819/8192 \approx 0.0999756$, and in BF16 it becomes $205/2048 \approx 0.1000977$. In FP16, 65 519 rounds to 65 504, the largest finite value, but 65 520 rounds to infinity: it is the midpoint between 65 504 and 65 536, the tie goes to the even significand, and 65 536 is out of range.

**The accumulator matters.** Take the dot product of two vectors of 4096 ones. With an FP32 accumulator the model gives 4096. With an FP16 accumulator it gives 2048: near 2048 the FP16 values are 2 apart, so $2048 + 1$ is a tie and rounds back to 2048, and the sum stops growing.

**A random dot product.** Take $k = 1024$ values $x_i$ and $y_i$ drawn from $\{0.001, 0.002, \dots, 1\}$ with `random.Random(5)`, and round them to FP16. Compared with the exact dot product of the rounded inputs:

| accumulator | result | relative error |
|---|---|---|
| FP16 | 245.125 | about $9.9 \times 10^{-3}$ |
| FP32 | 247.58416748046875 | about $7.7 \times 10^{-7}$ |

The rounding of the inputs to FP16 changes the exact result by a relative $5.0 \times 10^{-6}$. So with an FP32 accumulator the input rounding is the main error, and with an FP16 accumulator the sum is the main error. The FP32 error is well inside the bound $\gamma_{1024} \sum |x_i y_i|$.

**Tile counts.** A product with $m = n = k = 4096$ and $16 \times 16 \times 16$ fragments needs $256^3 = 16\,777\,216$ calls of `mma_sync`. With $m = n = k = 1000$, each size pads to 1008, so the warps make $63^3 = 250\,047$ calls, and only $(1000/1008)^3 = (125/126)^3 \approx 97.6\%$ of the multiply-adds are useful.

## Where it is used

- **Deep learning.** Training and inference spend most of their time in [matrix products](/parallel-matrix-multiplication/) and convolutions, which libraries such as cuBLAS and cuDNN map to tensor cores. Training often keeps a master copy of the weights in FP32 and scales the loss so that small FP16 gradients do not become zero.
- **Dense linear algebra.** GEMM, and through it LU and Cholesky factorizations. Mixed-precision iterative refinement factorizes in low precision on tensor cores and then corrects the solution with residuals in higher precision.
- **Scientific codes.** FP64 tensor operations on the A100 and later speed up double-precision matrix products.
- **Other operations recast as matrix products.** Attention in transformers, some FFT and stencil methods, and reductions written as products with a vector of ones.
- **Design of kernels.** Tensor cores move the bottleneck to memory, so fast kernels use [shared memory tiling](/shared-memory-tiling/), high [arithmetic intensity](/arithmetic-intensity/) and overlap of loads and math.

## References
