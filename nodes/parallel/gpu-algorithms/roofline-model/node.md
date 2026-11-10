---
tag: WCV5M0
kind: model
slug: roofline-model
name: Roofline model
aliases:
- roofline performance model
area: parallel/gpu-algorithms
level: core
summary: Bounds the attainable FLOP rate of a kernel by min(peak compute, intensity x bandwidth); the ridge point pi/beta splits memory-bound kernels from compute-bound ones.
prereqs: [arithmetic-intensity, gpu-memory-hierarchy]
see_also: [latency-hiding, occupancy, shared-memory-tiling, memory-coalescing, tensor-cores, kernel-fusion, external-memory-model, red-blue-pebble-game]
sources:
  - paper: doi:10.1145/1498765.1498785
    title: Samuel Williams, Andrew Waterman and David Patterson, Roofline, an insightful visual performance model for multicore architectures, Communications of the ACM 52(4), 2009
    locator: the roofline formula and graph, the ridge point, the ceilings for in-core and memory optimizations, and the case study on four multicore systems
  - url: https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf
    title: NVIDIA, NVIDIA A100 Tensor Core GPU Architecture (whitepaper), 2020
    locator: the A100 specification table (108 SMs, 1410 MHz boost clock, peak FP32 19.5 TFLOPS, peak FP64 9.7 TFLOPS, peak FP16 Tensor Core 312 TFLOPS, 1555 GB/s HBM2 for the 40 GB part)
  - url: https://www.nvidia.com/content/gtc-2010/pdfs/2238_gtc2010.pdf
    title: Vasily Volkov, Better performance at lower occupancy, GPU Technology Conference 2010
    locator: slide 8 (GTX 480 at 1.3 Tflop/s arithmetic and 177 GB/s memory throughput) and slides 54 to 58 (matrix multiply with more outputs per thread)
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition
    locator: Chapter 5 (memory architecture and data locality, the importance of memory access efficiency and the roofline model)
---

The **roofline model** bounds the speed of a kernel on a machine with two numbers of the machine and one number of the kernel. The machine has a peak compute rate $\pi$ in FLOP/s and a memory bandwidth $\beta$ in bytes/s. The kernel has an [arithmetic intensity](/arithmetic-intensity/) $I$, the floating-point operations it does per byte that it moves through memory. The attainable rate is

$$P(I) = \min(\pi,\; I \cdot \beta).$$

Williams, Waterman and Patterson introduced the model in 2009 for multicore CPUs, with the name operational intensity for $I$. It is now the usual first estimate for GPU kernels, because a GPU has a very high $\pi$ and most kernels cannot supply data fast enough to reach it.

## The machine

The machine has one processor with peak rate $\pi$ and one memory link with bandwidth $\beta$. The link is the slowest one that the data of the kernel must cross: DRAM in the original paper, HBM or GDDR on a GPU. The model assumes that computation and transfers overlap completely and that latency is hidden.

A kernel is two numbers: the work $W$ in FLOP and the traffic $Q$ in bytes on the link. $Q$ counts the bytes that the memory actually moves after the caches have filtered the accesses, not the loads in the source code. Then $I = W/Q$.

On a GPU, $\pi$ is the number of SMs times the FLOP per clock per SM times the clock. Each precision and each unit has its own $\pi$, so a GPU has several flat roofs. The NVIDIA A100 40 GB has 108 SMs at a boost clock of 1410 MHz, a peak of 19.5 TFLOP/s in FP32, 9.7 TFLOP/s in FP64, 312 TFLOP/s in FP16 on the [tensor cores](/tensor-cores/), and 1555 GB/s of HBM2 bandwidth (A100 whitepaper, specification table). These numbers change between GPU generations and between parts of one generation; the 80 GB A100 parts have more bandwidth.

A GPU also has a roof for each level of the [memory hierarchy](/gpu-memory-hierarchy/): HBM, the L2 cache and shared memory each have a bandwidth, and a kernel has an intensity against each level. The attainable rate is the minimum over all roofs. This is the hierarchical roofline. AMD names the SM a compute unit (CU) and shared memory the local data share (LDS); the model is the same.

## What it counts

### The roof and the ridge point

The time of a kernel is at least the time to do its work and at least the time to move its bytes:

$$T \ge \max\!\left(\frac{W}{\pi},\; \frac{Q}{\beta}\right) = \frac{W}{P(W/Q)}.$$

The two terms are equal at the **ridge point**

$$I^{*} = \frac{\pi}{\beta}.$$

A kernel with $I < I^{*}$ is memory-bound: its roof is the slanted line $I\beta$, and more compute units do not help. A kernel with $I \ge I^{*}$ is compute-bound: its roof is the flat line $\pi$, and faster memory does not help. On a log-log plot of $P$ against $I$, the slanted part has slope 1 and the two parts meet at $I^{*}$. The plot shows at one glance which resource limits a kernel and how far the kernel is below its roof.

For the A100 40 GB in FP32, $I^{*} = 19.5 \cdot 10^{12} / 1.555 \cdot 10^{12} \approx 12.54$ FLOP/byte. In FP64 it is about 6.24, and for FP16 on the tensor cores it is about 200.6.

### Ceilings

A roof is a peak that a kernel reaches only when it uses every feature of the machine. Williams et al. draw **ceilings** below the roofs, one for each feature that a kernel can fail to use. A ceiling lowers the roof to the minimum of all ceilings that apply.

- **Compute ceilings.** A fused multiply-add counts as 2 FLOP in one instruction, so a kernel without FMA instructions has a ceiling of $\pi/2$. A warp with half its lanes active after a [divergent branch](/warp-divergence/) does at most half the work per issue. FP16 matrix work that does not use the tensor cores has the ceiling of the plain FP16 units, far below the tensor core roof.
- **Bandwidth ceilings.** A memory link reaches $\beta$ only with enough bytes in flight. By Little's law, a kernel needs about $\beta$ times the memory latency in flight, and too few warps or too little instruction-level parallelism give a lower ceiling ([latency hiding](/latency-hiding/), [occupancy](/occupancy/)).

On this site $Q$ counts the bytes that the memory moves. So an access pattern that is not [coalesced](/memory-coalescing/) does not lower $\beta$; it raises $Q$ and so lowers $I$. A stride-2 read of 4-byte words moves twice the useful bytes and halves $I$.

### A worked example

The kernels are shown in CUDA C++. The counts are in the comments.

```cpp
__global__ void vecAdd(const float* a, const float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];      // W = 1 FLOP, Q = 4 + 4 + 4 = 12 bytes, I = 1/12
}

// inner loop of the tiled matrix product (see shared-memory-tiling), tile width T
for (int k = 0; k < T; ++k)
    acc += As[ty][k] * Bs[k][tx];       // 2 FLOP per 2 shared-memory words = 8 bytes
```

On the A100 40 GB in FP32 ($\pi = 19.5$ TFLOP/s, $\beta = 1555$ GB/s, $I^{*} \approx 12.54$):

| Kernel | $I$ against HBM | Roof | Share of FP32 peak |
|---|---|---|---|
| vector add | 1/12 | 129.6 GFLOP/s | 0.66% |
| tiled matrix product, $T = 32$ | 8 | 12.44 TFLOP/s | 64% |
| any kernel with $I = 32$ | 32 | 19.5 TFLOP/s | 100% |

The derivations of the intensities are on the [arithmetic intensity](/arithmetic-intensity/) page. A vector add of $10^8$ floats moves $1.2 \cdot 10^9$ bytes, so it needs at least $1.2 \cdot 10^9 / 1.555 \cdot 10^{12} \approx 0.77$ ms on this GPU, whatever the code does.

The HBM roof is not the only roof of the tiled kernel. Its inner loop reads 8 bytes of shared memory per 2 FLOP, so its intensity against shared memory is $1/4$. The peak shared memory bandwidth, derived from 32 banks of 4 bytes per clock per SM with no [bank conflicts](/shared-memory-bank-conflicts/), is $128 \cdot 108 \cdot 1.41 \cdot 10^{9} \approx 19.49$ TB/s. This is a derived number, not a vendor figure. The shared-memory roof is then $19.49/4 \approx 4.87$ TFLOP/s, 25% of the FP32 peak, and it is lower than the HBM roof. So the plain tiled kernel is bound by shared memory. A thread that computes several outputs keeps operands in registers and reuses each shared-memory word several times, which raises the intensity against shared memory (Volkov, GTC 2010, slides 54 to 58).

The Python code of this page computes the roofs with exact fractions. The tests check every number of this example, that the roof is the minimum of the two terms and is continuous at the ridge point, that the time bound equals $W/P(W/Q)$ on random inputs, and that ceilings only lower the roof. The tests do not run the CUDA code.

## Relation to other models

- [Arithmetic intensity](/arithmetic-intensity/) is the horizontal axis of the model. That page derives $I$ for common kernels; this page turns $I$ into a rate.
- The [external memory model](/external-memory-model/) counts block transfers between a fast and a slow memory and ignores computation. The roofline model takes that count as $Q$, divides it by $\beta$ and adds a compute term.
- The [red-blue pebble game](/red-blue-pebble-game/) gives lower bounds on $Q$ for a computation with a fast memory of $M$ words. A lower bound on $Q$ is an upper bound on $I$, and so an upper bound on $P$ for every schedule.
- The [work-span model](/work-span-model/) counts $W$ and the span but no memory traffic. The roofline model counts $W$ and $Q$ but no span: it assumes that the kernel has enough parallelism to keep the machine busy.
- [Latency hiding](/latency-hiding/) gives the condition for the slanted roof: the kernel must keep about $\beta$ times the latency in bytes in flight.

## Known results in the model

- **Time bound.** $T \ge \max(W/\pi, Q/\beta)$ for every kernel, and the bound is reached only with complete overlap of compute and transfers.
- **Kernels with constant intensity.** Vector add, dot product, matrix-vector product and sparse matrix-vector product have an intensity that does not grow with the input size. On a machine whose ridge point is above their intensity, they stay on the slanted roof for every input size, and only less traffic helps. [Kernel fusion](/kernel-fusion/) removes the store and the load of an intermediate array and so raises $I$.
- **Matrix multiplication.** Tiling with a fast memory of $M$ words gives $I = \Theta(\sqrt{M})$, and the red-blue pebble game shows $Q = \Omega(n^{3}/\sqrt{M})$ for the standard algorithm, so no schedule does better by more than a constant factor ([blocked matrix multiplication](/blocked-matrix-multiplication/)). Matrix multiplication is therefore compute-bound once the fast memory is large enough. With the intensity $T/4$ of the plain tiled kernel against HBM, the A100 FP32 ridge point needs $T/4 \ge 12.54$, so $T \ge 51$ if the L2 cache gives no extra reuse.
- **Ridge points move to the right.** Peak compute has grown faster than memory bandwidth. Volkov gives 1.3 Tflop/s and 177 GB/s for the GTX 480 (GTC 2010, slide 8), a ridge point of about 7.3 FLOP/byte. The A100 40 GB has about 12.5 in FP32 and about 200.6 for FP16 on the tensor cores. As the ridge point grows, more kernels become memory-bound. The exact values depend on the GPU.
- **The original case study.** Williams et al. apply the model to floating-point kernels, among them sparse matrix-vector multiplication and a stencil, on four multicore systems. They use the ceilings to order the optimizations that each kernel needs on each system.

## References
