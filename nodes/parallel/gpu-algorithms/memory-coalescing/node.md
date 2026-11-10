---
tag: KWEBM1
kind: concept
slug: memory-coalescing
name: Memory coalescing
aliases:
- coalesced memory access
area: parallel/gpu-algorithms
level: intro
summary: The global memory accesses of the 32 lanes of a warp are served by one 32-byte transaction per distinct sector, so neighbouring lanes should touch neighbouring addresses.
prereqs: [simt-model, gpu-memory-hierarchy]
see_also: [shared-memory-tiling, parallel-matrix-transpose, shared-memory-bank-conflicts, arithmetic-intensity, roofline-model, external-memory-model, thread-block-and-grid]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 2.3.4.1 (coalesced global memory access, 32-byte transactions, the 12.5 percent example)
  - url: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/
    title: NVIDIA, CUDA C++ Best Practices Guide, version 13.5
    locator: Section 10.2.1 (coalesced access to global memory), the subsection on misaligned accesses (cudaMalloc alignment of at least 256 bytes) and Section 10.2.1.4 (strided accesses, stride 2 on the Tesla V100)
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition
    locator: Chapter 6 (performance considerations, memory coalescing)
---

**Memory coalescing** is the merging of the global memory accesses of the 32 lanes of a [warp](/simt-model/) into as few memory transactions as possible. Global memory moves data in 32-byte sectors, and one warp load or store costs one transaction for each distinct sector that its lanes touch (CUDA Programming Guide v13.5, Section 2.3.4.1). So a warp that reads 32 consecutive 4-byte words costs 4 transactions, and a warp whose lanes are 32 bytes or more apart costs 32. The cost model is the [SIMT model](/simt-model/) with transactions per warp access as the memory measure.

## In plain words

The store sends goods only in full boxes of a fixed size. A team of thirty-two workers asks for goods at the same moment, and the store packs the order. If the workers ask for items that sit side by side, a few boxes hold all of them. If each worker asks for an item in a different part of the store, each item needs its own box, and most of each box is empty. The trip costs the same per box, full or not. So the team should ask for neighbouring items at the same moment: worker one takes the first item, worker two the next, and so on. Data laid out so that the same field of many records sits side by side helps with this.

## The idea

Fix one warp instruction. Lane $\ell$ (for $\ell = 0, \dots, 31$) accesses $w$ bytes at byte address $a_\ell$. The sectors are the aligned 32-byte ranges $[32k, 32k + 32)$. The instruction needs

$$T = \left\lvert \bigcup_{\ell \text{ active}} \left\{ \left\lfloor \tfrac{a_\ell}{32} \right\rfloor, \dots, \left\lfloor \tfrac{a_\ell + w - 1}{32} \right\rfloor \right\} \right\rvert$$

transactions, and moves $32T$ bytes. With $u$ distinct useful bytes, the **efficiency** is $u / (32T)$. For one word per lane, $u = 32w$ when the lanes read distinct words. The order of the lanes inside the sectors does not matter: any permutation of 32 consecutive words still costs 4 sectors.

### Unit and strided access

Let lane $\ell$ read element $s\ell$ of an array of $w$-byte words, with $w$ dividing 32 and the array aligned to 32 bytes. The lanes span bytes $0$ to $31ws + w - 1$. When $ws \le 32$, no sector in that range is skipped, because neighbouring lanes are at most 32 bytes apart. When $ws > 32$, every lane has its own sector. So

$$T(s) = \min\left(32, \left\lfloor \frac{31 w s}{32} \right\rfloor + 1\right).$$

For 4-byte words this is $T(s) = \min(32, \lfloor 31s/8 \rfloor + 1)$, which gives $4, 8, 12, 16, 20, 24, 28, 32$ for $s = 1, \dots, 8$. So the efficiency is $1/s$ for $s \le 8$ and $1/8$ beyond. Stride 2 gives 8 sectors per warp and 50% efficiency, the case of the Best Practices Guide, Section 10.2.1.4, for the Tesla V100. A stride of 8 words or more gives 32 sectors and 1024 bytes for 128 useful bytes, which is the 12.5% of the Programming Guide, Section 2.3.4.1.

### Misaligned access

If the base address is shifted by $o$ bytes, with $o$ a multiple of 4 that is not a multiple of 32, the 128 bytes of a unit-stride warp straddle 5 sectors instead of 4, and the efficiency is $4/5$. `cudaMalloc` returns addresses aligned to at least 256 bytes, so misalignment comes from offsets such as `x[i + 1]`.

### Random access

If each lane picks one of $N$ sectors uniformly and independently, the expected number of distinct sectors is

$$\mathbb{E}[T] = N \left( 1 - \left( 1 - \frac{1}{N} \right)^{32} \right),$$

because each sector is missed by all 32 lanes with probability $(1 - 1/N)^{32}$. For a large array this is almost 32: with $N = 8192$ sectors (a 256 KB array), $\mathbb{E}[T] \approx 31.94$. Even inside a 1 KB region ($N = 32$), $\mathbb{E}[T] \approx 20.4$, five times the unit-stride cost.

### Structure of arrays and array of structures

An array of structures (AoS) stores the fields of each record together. A kernel that reads one field of record $\ell$ in lane $\ell$ has stride $s$ equal to the record size in words. A structure of arrays (SoA) stores each field in its own array, so the same read has stride 1.

```cpp
struct P { float x, y, z; };             // AoS: 12 bytes per record
__global__ void aos(const P* p, float* out, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) out[i] = p[i].x;           // stride 3 words: 12 sectors per warp
}
__global__ void soa(const float* x, float* out, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) out[i] = x[i];             // stride 1: 4 sectors per warp
}
```

The AoS load costs $T(3) = 12$ sectors and uses one third of the bytes. When a kernel reads all fields of a record, the other bytes are used by later loads and may hit in the cache, but the first load still moves three times the data of the SoA load.

## Examples

| Access pattern (4-byte words) | Sectors per warp | Efficiency |
|---|---|---|
| `x[i]`, aligned | 4 | 100% |
| `x[i + 1]` | 5 | 80% |
| `x[2 * i]` | 8 | 50% |
| `p[i].x` with 12-byte records | 12 | 33% |
| `x[8 * i]` or larger stride | 32 | 12.5% |
| `x[perm[i]]` with `perm` a permutation inside each group of 32 | 4 | 100% |
| `x[0]` in every lane (broadcast) | 1 | (one word used) |
| `x[rand()]` over a large array | about 32 | about 12.5% |

A whole kernel adds the counts of its warps. A copy of 1024 floats with unit stride needs $32 \cdot 4 = 128$ sectors; reading every second float of a 2048-float array needs 256 sectors for the same 1024 useful floats.

The Python code of this page computes the sectors of one warp access from the 32 addresses. The tests check the formula $T(s)$ for strides 1 to 39 and words of 4 and 8 bytes, the Guide's 12.5% case, 5 sectors for every misaligned offset, 4 sectors for any permutation inside an aligned segment, the expected count for random access over seeded trials (within 0.05), and the AoS and SoA counts. The CUDA code on this page is for the reader; the tests do not run it.

## Where it is used

Coalescing drives the data layout of most GPU kernels. [Parallel matrix transpose](/parallel-matrix-transpose/) reads rows and writes columns, so a direct version coalesces only one side; staging a tile in shared memory makes both sides coalesced, at the price of [bank conflicts](/shared-memory-bank-conflicts/) that padding then removes. [Shared memory tiling](/shared-memory-tiling/) loads each tile with consecutive threads on consecutive columns. Sparse formats such as [ELLPACK](/ellpack-format/) store the matrix column by column, so that consecutive threads, one per row, read consecutive words. [Radix sort](/radix-sort/) and [compaction](/compaction/) on GPUs first group the outputs of a block in shared memory and then write them out in runs, because a direct scatter is close to random access. The sector count is the GPU form of the block count $B$ of the [external memory model](/external-memory-model/), with $B = 32$ bytes and the transfers counted per warp instruction.

## References
