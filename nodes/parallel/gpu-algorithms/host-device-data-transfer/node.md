---
tag: J2CVHF
kind: concept
slug: host-device-data-transfer
name: Host-device data transfer
aliases:
- PCIe transfer
- CPU-GPU transfer
- host-to-device copy
area: parallel/gpu-algorithms
level: core
summary: Moving data between CPU memory and GPU memory over a link such as PCIe, modelled as latency plus bytes over bandwidth; offloading pays only if the kernel does enough work per byte moved.
prereqs: [cuda-programming-model, gpu-memory-hierarchy]
see_also: [cuda-streams, kernel-launch-overhead, kernel-fusion, arithmetic-intensity, roofline-model, latency-hiding, parallel-matrix-multiplication, amdahls-law]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 2.5.2.3 (cudaMemcpyAsync, and the note that a copy with host memory that is not pinned reverts to synchronous behavior), Section 2.6.2 (unified memory), Section 2.6.3 (page-locked host memory, cudaMallocHost, cudaHostAlloc, cudaHostRegister) and 2.6.3.1 (mapped memory), Section 3.1.5 (batched memory transfers, cudaMemcpyBatchAsync), Section 4.1.4.1 (data prefetching, cudaMemPrefetchAsync with a cudaMemLocation)
  - url: https://docs.nvidia.com/cuda/archive/12.0.0/cuda-c-programming-guide/index.html
    title: NVIDIA, CUDA C++ Programming Guide, version 12.0
    locator: Section 3.2.6 (page-locked host memory and its benefits) and 3.2.6.3 (mapped memory), Section 3.2.8.3 (overlap of data transfer and kernel execution needs asyncEngineCount greater than zero and page-locked memory), Section 3.2.8.4 (copies in both directions overlap when asyncEngineCount is 2), Section 19.1.3 (data migration and the GPU page faulting of compute capability 6.x)
  - url: https://developer.nvidia.com/blog/how-optimize-data-transfers-cuda-cc/
    title: Mark Harris, How to optimize data transfers in CUDA C/C++, NVIDIA Technical Blog, 4 December 2012
    locator: the pinned staging buffer used for pageable copies, the measured pageable and pinned bandwidths, and the advice to batch small transfers
  - url: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf
    title: NVIDIA, A100 Tensor Core GPU datasheet
    locator: the specifications table (interconnect, PCIe Gen4 64 GB/s and NVLink 600 GB/s)
  - paper: doi:10.1145/1498765.1498785
    title: Samuel Williams, Andrew Waterman and David Patterson, Roofline, an insightful visual performance model for multicore architectures, Communications of the ACM 52(4), 2009, 65 to 76
    locator: arithmetic intensity and the bandwidth ceiling, applied here to the host link instead of DRAM
---

Host-device data transfer is the copy of data between the memory of the CPU (the host) and the memory of a discrete GPU (the device). The copy goes over a link such as PCIe or NVLink, which is much slower than the GPU's own memory. A good first model of one copy of $s$ bytes is $t(s) = L + s/\beta$, a fixed latency $L$ plus the bytes divided by the link bandwidth $\beta$. Two rules follow from this model. Small copies are slow, so you should batch them. Offloading work to the GPU pays only when the kernel does enough arithmetic for each byte that crosses the link. Pinned host memory makes copies faster and lets them run at the same time as kernels. Unified memory hides the copies behind page migration, but it does not remove them.

## In plain words

Think of a large workshop (the GPU) on the other side of a river from a store (the CPU memory). There is one bridge. Each truck that crosses the bridge must wait for a fixed time at the gate, and then it drives at a fixed speed. If you send a thousand small trucks, most of the time goes to the gate. If you put all the goods on one big truck, the gate cost is paid once. Also, the workshop is so fast that it often finishes the job before the next truck arrives. So you send work across the river only when the workshop has a lot to do with each load. If the job is small, such as adding two lists of numbers once, it is faster to do it in the store.

## The idea

The model of the GPU is the [SIMT model](/simt-model/) with warps of 32 threads and the [roofline model](/roofline-model/). This page adds a third level below device memory: the host link, which has its own latency and bandwidth.

| symbol | meaning |
|---|---|
| $n$ | the number of elements |
| $p$ | the number of processors |
| $W$, $S$, $T_p$ | the work, the span and the time on $p$ processors |
| $M$, $B$ | the fast memory size and the memory transaction size |
| $s$ | the size of one copy in bytes |
| $L$ | the fixed latency of one copy, in seconds |
| $\beta$ | the bandwidth of the host link, in bytes per second |
| $P$ | the arithmetic rate of the GPU, in FLOP per second |
| $I$ | the FLOP done per byte moved over the host link |

**The latency-bandwidth model.** One copy of $s$ bytes takes
$$t(s) = L + \frac{s}{\beta}.$$
$L$ includes the API call, the driver work and the setup of the copy engine. The effective bandwidth that the copy sees is
$$\beta_{\text{eff}}(s) = \frac{s}{t(s)} = \frac{\beta s}{s + L\beta}.$$
It reaches half of $\beta$ when $s = L\beta$. This is the half-bandwidth size. Copies much smaller than $L\beta$ are bound by latency, and copies much larger are bound by bandwidth. The values of $L$ and $\beta$ depend on the link, the GPU, the CPU, the driver and the kind of host memory. You must measure them on the target system. The examples below use assumed values.

**The link.** For PCIe 3.0 and later, each lane sends 128 data bits in each 130-bit block. With 8, 16 and 32 GT/s per lane for PCIe 3.0, 4.0 and 5.0, a x16 link has a raw rate per direction of $G \cdot 16 \cdot \tfrac{128}{130} / 8$ GB/s, which is about 15.75, 31.51 and 63.02 GB/s. Packet headers and flow control take some of this, so measured copies are slower. The A100 datasheet lists 64 GB/s for PCIe Gen4. That number agrees with the sum of both directions of a x16 link. NVLink is faster: the same datasheet lists 600 GB/s for the A100. These numbers change between generations of the link and of the GPU.

**Pageable and pinned memory.** Memory from `malloc`, `new` or `mmap` is pageable. The operating system can swap it out or move it, so the copy engine cannot read it directly. For a pageable copy, the driver first copies the data into a pinned staging buffer and then sends it to the GPU (Harris 2012). Page-locked (pinned) memory comes from `cudaMallocHost` or `cudaHostAlloc`, or `cudaHostRegister` can pin an existing range (CUDA Programming Guide 13.5, Section 2.6.3). The guide says that pinned memory is necessary for asynchronous copies and that it also improves synchronous copies. If you give `cudaMemcpyAsync` pageable memory, it still works, but it reverts to synchronous behavior and does not overlap with other work (Section 2.5.2.3). In Harris's measurements, pinned copies were more than twice as fast as pageable copies on a laptop with a PCIe Gen2 GPU, and only a little faster on a desktop with a GTX 680. Pinned memory is a limited resource: if you pin too much, the operating system has less memory to page.

**Overlap.** A GPU has one or more copy engines. If the device property `asyncEngineCount` is greater than zero, a copy to or from pinned memory can run at the same time as a kernel. If it is 2, copies in the two directions can also run at the same time (CUDA C++ Programming Guide 12.0, Sections 3.2.8.3 and 3.2.8.4). You get the overlap with [CUDA streams](/cuda-streams/). That page has the pipeline model. With perfect overlap, the time is near the maximum of the copy time and the compute time, not their sum.

**Mapped memory.** Pinned memory can also be mapped into the address space of the device (Section 2.6.3.1 of the 13.5 guide). A kernel then reads host memory directly over the link and needs no separate copy. This "zero-copy" access is useful for data that the kernel reads once, but each access goes over the link, so it is slow for data that the kernel reads many times.

**Unified memory.** `cudaMallocManaged` gives one pointer that is valid on the CPU and the GPU (Section 2.6.2). On compute capability 6.x and later, the GPU can take page faults, and the driver migrates pages to the processor that touches them (12.0 guide, Section 19.1.3). This makes the program simpler, but the bytes still cross the link, and each fault adds latency. A kernel that touches pages one at a time pays many small copies, which is the worst case of the model above. A prefetch with `cudaMemPrefetchAsync` moves a whole range in one stream-ordered operation before the kernel needs it (13.5 guide, Section 4.1.4.1). In the 13.5 guide this function takes a `cudaMemLocation` and a flags argument. The 12.0 guide shows an older form with an integer device number. Check the signature for your CUDA version.

**Work per byte.** If a job moves $D$ bytes over the link and does $F$ FLOP on the GPU, and copy and compute do not overlap, then
$$T = L + \frac{D}{\beta} + \frac{F}{P}.$$
Let $I = F/D$. The copy time is at most the compute time when
$$I \ge \frac{P}{\beta}.$$
This is the roofline rule with the host link as the memory. Because $\beta$ for the link is much smaller than the device memory bandwidth, $P/\beta$ is large, often hundreds of FLOP per byte. A kernel must do a lot of work per byte moved, or it must keep its data on the GPU across many kernels. Otherwise, the transfer, not the GPU, sets the speed, and the speedup is bounded as in [Amdahl's law](/amdahls-law/).

## Examples

All the examples use the assumed values $L = 10$ µs and $\beta = 25$ GB/s. These are round numbers in the range of a PCIe 4.0 x16 link. They are not measurements of a given system. The Python file checks every number on this page exactly with fractions.

**One small copy and one large copy.** A copy of 4000 bytes takes $10 + 4000/(25 \cdot 10^3) = 10.16$ µs. Its effective bandwidth is $4000 / 10.16\ \mu\text{s} \approx 0.394$ GB/s, which is 1.6% of $\beta$. A copy of $10^6$ bytes takes $10 + 40 = 50$ µs, which is an effective 20 GB/s. The half-bandwidth size is $L\beta = 10^{-5} \cdot 25 \cdot 10^9 = 250\,000$ bytes.

**Batching.** A program sends 1000 records of 4000 bytes each. With one copy per record, the time is $1000 \cdot 10.16$ µs $= 10.16$ ms. If the program packs the records into one pinned buffer and makes one copy of $4 \cdot 10^6$ bytes, the time is $10 + 160 = 170$ µs. This is about 60 times faster. The same rule is behind `cudaMemcpy2D` for strided data and `cudaMemcpyBatchAsync` in recent CUDA versions (13.5 guide, Section 3.1.5).

**Vector add does not pay.** Add two arrays of $n = 10^8$ floats on the GPU. The copies move $12n = 1.2 \cdot 10^9$ bytes: two inputs to the GPU and one output back. The work is $n = 10^8$ FLOP, so $I = 1/12$ FLOP per byte. With an assumed GPU rate of $P = 10$ TFLOP/s, the copies take 48 ms and the arithmetic takes 10 µs, a total of 48.01 ms. The CPU can add the arrays in about the time it takes to read them once from its own memory, so the offload is slower than doing the work in place.

**Matrix multiplication pays.** For $n \times n$ matrices of 4-byte floats, the copies move $3n^2 \cdot 4$ bytes (A and B in, C out) and the work is $2n^3$ FLOP, so $I = n/6$. With $P = 10$ TFLOP/s and $\beta = 25$ GB/s, the rule asks for $I \ge P/\beta = 400$ FLOP per byte, so the compute time is larger than the copy time when $n \ge 2400$. A [parallel matrix multiplication](/parallel-matrix-multiplication/) of that size is a good job to offload. A smaller one is not, unless its inputs are already on the GPU.

The CUDA C++ code below shows a pinned copy with timing by events, and the unified memory form with a prefetch. The tests do not run this CUDA code. They run the Python model of the copy time.

```cuda
// Pinned host memory, an asynchronous copy, and timing with events.
float *h, *d;
size_t bytes = n * sizeof(float);
cudaMallocHost(&h, bytes);              // page-locked; malloc() memory would be pageable
cudaMalloc(&d, bytes);
cudaStream_t s;
cudaStreamCreate(&s);
cudaEvent_t start, stop;
cudaEventCreate(&start);
cudaEventCreate(&stop);

cudaEventRecord(start, s);
cudaMemcpyAsync(d, h, bytes, cudaMemcpyHostToDevice, s);   // returns at once
scale<<<(n + 255) / 256, 256, 0, s>>>(d, n);              // runs after the copy, same stream
cudaMemcpyAsync(h, d, bytes, cudaMemcpyDeviceToHost, s);
cudaEventRecord(stop, s);
cudaEventSynchronize(stop);             // the host waits only here
float ms;
cudaEventElapsedTime(&ms, start, stop);

// Unified memory: one pointer, pages migrate on demand.
float* u;
cudaMallocManaged(&u, bytes);
init_on_cpu(u, n);                      // the pages are now on the host
// Move the whole range in one operation before the kernel touches it.
// CUDA 13.x form (Section 4.1.4.1 of the 13.5 guide); CUDA 12.0 took an int device instead.
cudaMemLocation loc = {cudaMemLocationTypeDevice, gpu_id};
cudaMemPrefetchAsync(u, bytes, loc, 0, s);
scale<<<(n + 255) / 256, 256, 0, s>>>(u, n);
cudaStreamSynchronize(s);
```

## Where it is used

- **Every discrete-GPU program.** The input must reach the device and the result must come back. The time of these copies is often a large part of the total.
- **Pipelines with streams.** Large inputs are cut into chunks, and the copy of one chunk overlaps the kernel on the previous chunk, as on the [CUDA streams](/cuda-streams/) page.
- **Keeping data resident.** Iterative solvers, simulations and neural network training keep their arrays on the GPU for the whole run and copy only small results back. Then the transfer cost is paid once and many kernels share it.
- **Fusion and fewer launches.** Data that stays on the GPU can be shared by kernels that are fused ([kernel fusion](/kernel-fusion/)) or launched as a graph ([kernel launch overhead](/kernel-launch-overhead/)). These are different costs from the transfer cost, and each needs its own fix.
- **Out-of-core work.** When the data is larger than device memory, unified memory with prefetch, or explicit chunked copies, moves the working set in and out. The work-per-byte rule then applies to each chunk.
- **Scheduling.** Runtimes that decide whether to run a task on the CPU or the GPU compare $L + D/\beta + F/P_{\text{GPU}}$ with $F/P_{\text{CPU}}$.

## References
