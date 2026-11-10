---
tag: 7X2269
kind: concept
slug: latency-hiding
name: Latency hiding
aliases:
- latency tolerance through multithreading
area: parallel/gpu-algorithms
level: core
summary: A GPU keeps its units busy during long latencies by issuing from other ready warps; by Little's law it needs latency times throughput independent operations in flight, from warps or from ILP.
prereqs: [simt-model, occupancy]
see_also: [gpu-memory-hierarchy, roofline-model, memory-coalescing, shared-memory-tiling, cuda-streams, persistent-threads, warp-specialization]
sources:
  - url: https://www.nvidia.com/content/gtc-2010/pdfs/2238_gtc2010.pdf
    title: Vasily Volkov, Better performance at lower occupancy, GPU Technology Conference 2010
    locator: slides 7 and 8 (latencies and throughputs), slide 10 (needed parallelism = latency x throughput), slide 11 (arithmetic parallelism per SM), slides 12 and 13 (TLP and ILP), slides 16 to 21 (threads needed against ILP on GTX 480), slides 28 and 29 (memory parallelism)
  - paper: doi:10.1287/opre.9.3.383
    title: John D. C. Little, A proof for the queuing formula L = lambda W, Operations Research 9(3) (1961)
    locator: pp. 383 to 387
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 3.2.2.2 (hardware multithreading, warp switches at no cost)
  - url: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/
    title: NVIDIA, CUDA C++ Best Practices Guide, version 13.5
    locator: Section 10.2 (global memory latency of hundreds of cycles) and Section 11.3 (low occupancy with high ILP)
  - url: https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf
    title: NVIDIA, NVIDIA A100 Tensor Core GPU Architecture (whitepaper), 2020
    locator: the A100 specification table (108 SMs, 1555 GB/s for the 40 GB part)
---

**Latency hiding** is the way a GPU keeps its pipelines busy while single operations take a long time: when one warp waits for a memory access or for the result of an arithmetic instruction, the scheduler issues an instruction from another warp that is ready. Each SM keeps the registers of all its resident warps, so a switch from one warp to another costs nothing (CUDA Programming Guide v13.5, Section 3.2.2.2). By Little's law, a pipe with latency $L$ and throughput $X$ is full only when about $L \cdot X$ independent operations are in flight. They can come from many warps (thread-level parallelism) or from independent instructions inside one thread (instruction-level parallelism), which is why [occupancy](/occupancy/) alone does not decide speed.

## In plain words

A cook makes many cakes. Each cake must stay in the oven for an hour, but the cook needs only a minute to put one in. If the cook bakes one cake at a time, the cook waits most of the hour. If sixty cakes are in the oven at once, the cook puts one in every minute and never waits. So the number of cakes that must be in the oven at once is the baking time times the rate at which the cook works. The cakes can come from many helpers who each bring one cake, or from a few helpers who each bring several cakes at once. Both work, as long as enough cakes are in the oven. A GPU works the same way with its memory and its arithmetic units.

## The idea

### Little's law

For a system in steady state, the mean number of items in the system equals the arrival rate times the mean time each item spends in it (Little 1961). For a pipeline:

$$\text{operations in flight} = \text{latency} \times \text{throughput}.$$

To keep a pipe of latency $L$ cycles busy at $X$ operations per cycle, about $LX$ independent operations must be in flight. Volkov's GTC 2010 talk states it as "needed parallelism = latency x throughput" (slide 10).

### The model of one scheduler

Let a warp scheduler issue at most one warp instruction per cycle. Let each of $w$ resident warps run $k$ independent chains of instructions, where each instruction depends on the one before it in its chain and can issue $L$ cycles after it. Then each warp can issue at most $k$ instructions in any window of $L$ cycles, so the issue rate is at most $wk/L$; the scheduler also issues at most 1 per cycle. So

$$\text{rate} \le \min\left(1, \frac{wk}{L}\right),$$

and the scheduler can be fully busy only when $wk \ge L$. A greedy round-robin scheduler comes within a few percent of this bound in the simulator below; the bound itself is all that the argument proves. The two factors are the two sources of parallelism:

- **Thread-level parallelism (TLP)** is $w$, the number of resident warps that can issue. It grows with occupancy.
- **Instruction-level parallelism (ILP)** is $k$, the number of independent instructions in one thread. It grows when each thread computes several outputs, or loads several values before it uses the first one.

The same $wk$ can come from many warps with $k = 1$ or from fewer warps with larger $k$. Fewer warps with more ILP use more registers per thread, which is often the faster choice, see [occupancy](/occupancy/).

### Memory

For memory, the throughput is the bandwidth in bytes per cycle and the operations are bytes:

$$\text{bytes in flight} = \text{memory latency} \times \text{bandwidth}.$$

The memory latency is far longer than the arithmetic latency. The Best Practices Guide (Section 10.2) gives hundreds of clock cycles for global memory, and Volkov measured about 20 cycles for arithmetic and 400 or more for memory (slide 7). So memory needs many more operations in flight. Each thread contributes the bytes of its loads that are outstanding at once, and [coalesced](/memory-coalescing/) loads make every byte in flight a useful one.

## Examples

**Arithmetic, from Volkov (slide 11).** Latency times throughput per SM:

| GPU | Latency (cycles) | Throughput (operations per cycle per SM) | Needed in flight per SM |
|---|---|---|---|
| G80 to GT200 | about 24 | 8 | about 192 |
| GF100 (Fermi) | about 18 | 32 | about 576 |
| GF104 | about 18 | 48 | about 864 |

On a GTX 480 (GF100), Volkov measured that full arithmetic throughput needs about 576 threads per SM with no ILP, 320 with ILP 2, 256 with ILP 3 and 192 with ILP 4 (slides 16 to 21). The measured counts with ILP are higher than $576/k$, because the pipeline has other limits as well, but the trend matches the model: ILP replaces threads.

**Memory, from Volkov (slides 28 and 29).** On the GTX 480, with a latency below 800 cycles and a bandwidth below 177 GB/s, less than 100 KB must be in flight for the whole GPU. At 4 bytes per thread that is 25,000 threads; at 100 bytes per thread it is 1,000 threads.

**Memory on an A100, with an assumed latency.** The A100 40 GB has 1555 GB/s of HBM2 bandwidth and 108 SMs (NVIDIA A100 whitepaper). The DRAM latency is not in the sources of this page, so assume 500 ns for the example. Then $1.555 \cdot 10^{12} \cdot 500 \cdot 10^{-9} \approx 778$ KB must be in flight for the GPU, about 7.2 KB per SM. One coalesced warp load of 4-byte words moves 128 bytes, so each SM needs about 56 such loads in flight. With one load per thread at a time, that is 56 of the 64 warps that an SM of compute capability 8.0 can hold, or 88% occupancy. With 4 independent loads per thread, 14 warps (22% occupancy) are enough. A different latency changes the numbers in proportion.

**The simulator.** The Python code of this page simulates one scheduler with $w$ warps, $k$ chains per warp and latency $L$, and issues greedily in round-robin order. The tests check that the measured rate is within 10% of $\min(1, wk/L)$ for latencies 1 to 20, 1 to 16 warps and ILP 1 to 4, and that 4 warps with ILP 4 run more than 3 times faster than 4 warps with ILP 1 at $L = 16$. The tests also check the products in the tables above. No CUDA code runs in the tests.

## Where it is used

Latency hiding is the reason that GPUs run tens of thousands of threads at once. It sets the target for [occupancy](/occupancy/) and explains when lower occupancy is fine. It is the reason the [roofline model](/roofline-model/) can use peak bandwidth and peak compute as ceilings: a kernel reaches them only when enough work is in flight, and a kernel that falls far below its roofline often lacks parallelism of this kind. Register tiling in [shared memory tiling](/shared-memory-tiling/) and loop unrolling raise ILP. Double buffering of tiles and [warp specialization](/warp-specialization/) overlap the loads of the next tile with the compute on the current one. At a larger scale, [CUDA streams](/cuda-streams/) hide the latency of host-device copies behind kernels, and [persistent threads](/persistent-threads/) keep a fixed set of warps busy with a queue of work.

## References
