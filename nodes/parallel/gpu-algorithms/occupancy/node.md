---
tag: D8FB42
kind: concept
slug: occupancy
name: Occupancy
aliases:
- GPU occupancy
area: parallel/gpu-algorithms
level: core
summary: The ratio of resident warps on an SM to the most it can hold, set by the threads, registers and shared memory of each block; higher occupancy hides more latency but is not always faster.
prereqs: [thread-block-and-grid, gpu-memory-hierarchy]
see_also: [latency-hiding, simt-model, shared-memory-tiling, warp-level-primitives, persistent-threads, cooperative-groups, roofline-model]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 2.3.7 (kernel launch and occupancy, the compute capability 10.0 examples), Section 3.2.2.2 (registers split among warps, shared memory among blocks) and Section 5.1.3, Tables 33 and 34 (per-SM limits)
  - url: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/
    title: NVIDIA, CUDA C++ Best Practices Guide, version 13.5
    locator: Section 11.1 (occupancy, higher occupancy does not always mean higher performance), Section 11.1.1 (register pressure, the 37-register examples on compute capability 7.0) and Section 11.3 (thread and block heuristics)
  - url: https://www.nvidia.com/content/gtc-2010/pdfs/2238_gtc2010.pdf
    title: Vasily Volkov, Better performance at lower occupancy, GPU Technology Conference 2010
    locator: slide 3 (CUBLAS SGEMM at 33 percent occupancy), slides 38 and 39 (87 and 84 percent of memory bandwidth at 8 and 4 percent occupancy), slide 44 (registers per thread against occupancy on GF100) and slide 74 (summary)
---

**Occupancy** is the number of warps that are resident on a streaming multiprocessor (SM) divided by the largest number of warps that the SM can hold (CUDA Programming Guide v13.5, Section 2.3.7). A block becomes resident only when its threads, its registers and its shared memory all fit next to the blocks already there, so the resource use of one block sets the occupancy. More resident warps give the scheduler more choice for [latency hiding](/latency-hiding/), but a kernel at lower occupancy can be faster when each thread does more independent work (Volkov 2010). The cost model is the [SIMT model](/simt-model/) with per-SM resource limits.

## In plain words

A workshop has a fixed number of desks, a fixed stock of tools, and a fixed amount of table space. Teams come in, and a team may enter only when there are desks, tools and table space for all its members at once. The more teams are inside, the easier it is for the foreman to find someone ready to work while others wait for parts. Occupancy is how full the workshop is. A team that asks for many tools or much table space leaves room for fewer teams. But a full workshop is not always the fastest one. A few teams with many tools each and many jobs in hand can keep the machines just as busy as a crowd of teams that each wait for parts.

## The idea

### The formula

Fix a kernel and a GPU. Let one block have $T$ threads, use $r$ registers per thread and $s$ bytes of shared memory. Let the SM hold at most $B_{\max}$ blocks, $W_{\max}$ warps and $T_{\max}$ threads, with $R$ registers and $S_{\text{sm}}$ bytes of shared memory. A block has $w_b = \lceil T/32 \rceil$ warps. The number of resident blocks is

$$b = \min\left( B_{\max}, \left\lfloor \frac{T_{\max}}{T} \right\rfloor, \left\lfloor \frac{W_{\max}}{w_b} \right\rfloor, \left\lfloor \frac{W_R}{w_b} \right\rfloor, \left\lfloor \frac{S_{\text{sm}}}{s} \right\rfloor \right), \qquad \text{occupancy} = \frac{b \, w_b}{W_{\max}},$$

where a term with $s = 0$ is dropped and $W_R$ is the number of warps that the register file can hold. The registers are allocated per warp, rounded up to a multiple of 256 (Best Practices Guide, Section 11.1.1), so a warp takes $\rho = 256 \lceil 32r/256 \rceil$ registers. This page models the register file as 4 equal partitions, one per warp scheduler, with each warp in one partition, so

$$W_R = 4 \left\lfloor \frac{R/4}{\rho} \right\rfloor.$$

The partition rule is a model that reproduces the two examples of the Best Practices Guide below; it is not a vendor specification. The CUDA occupancy API (`cudaOccupancyMaxActiveBlocksPerMultiprocessor`) and the Nsight Compute occupancy section give the exact value for a real kernel on a real GPU, including small per-block reserves of shared memory that the formula leaves out.

### Why occupancy matters

A warp that waits for memory cannot issue. If every resident warp waits, the SM idles. By Little's law, the SM needs about (latency) times (issue rate) independent instructions in flight to stay busy, see [latency hiding](/latency-hiding/). Resident warps are one source of such instructions, so low occupancy can leave the SM idle.

### Why higher occupancy is not always faster

The Best Practices Guide states that higher occupancy does not always mean higher performance (Section 11.1), and Volkov's GTC 2010 talk shows it with measurements:

- The second source of independent instructions is instruction-level parallelism inside one thread. A thread with 4 independent operations in flight needs a quarter of the warps to cover the same latency.
- More registers per thread lower the occupancy, but registers are the fastest memory and let each thread compute several outputs. On GF100, a kernel could use 20 registers per thread at 100% occupancy and 63 at 33% (slide 44).
- CUBLAS 2.0 SGEMM ran at 33% occupancy and 204 Gflop/s, while CUBLAS 1.1 ran at 67% and 128 Gflop/s on the same G80-class GPU (slide 3).
- A memory copy reached 87% of the pin bandwidth at 8% occupancy and 84% at 4% when each thread moved several words at once (slides 38 and 39, GTX 480).

So occupancy is a means, not a goal: it should be high enough to hide latency, and resources beyond that point are better spent on more work per thread.

## Examples

All limits below come from the CUDA Programming Guide v13.5, Section 5.1.3, Tables 33 and 34, or from the guides' examples, and they change between generations. Each SM has $R = 65536$ registers in every listed compute capability.

**Compute capability 8.0 (A100).** Here $B_{\max} = 32$, $W_{\max} = 64$, $T_{\max} = 2048$ and $S_{\text{sm}} = 164$ KB. Take $T = 256$, $r = 40$ and $s = 40$ KB, so $w_b = 8$.

| Resource | Computation | Blocks |
|---|---|---|
| block slots | $B_{\max}$ | 32 |
| threads | $\lfloor 2048/256 \rfloor$ | 8 |
| warps | $\lfloor 64/8 \rfloor$ | 8 |
| registers | $\rho = 256 \lceil 1280/256 \rceil = 1280$, $W_R = 4 \lfloor 16384/1280 \rfloor = 48$, $\lfloor 48/8 \rfloor$ | 6 |
| shared memory | $\lfloor 164/40 \rfloor$ | 4 |

So $b = 4$, 32 warps, and the occupancy is $32/64 = 50\%$, limited by shared memory. With $s = 16$ KB, shared memory allows 10 blocks and registers become the limit: $b = 6$, 75%. With $s = 16$ KB and $r = 32$, $W_R = 64$ and $b = 8$, 100%.

**The Programming Guide's examples (Section 2.3.7, compute capability 10.0).** There $B_{\max} = 32$, $T_{\max} = 2048$ and $S_{\text{sm}} = 233472$ bytes. A launch with blocks of 768 threads fits $\lfloor 2048/768 \rfloor = 2$ blocks, so $1536/2048 = 75\%$. Blocks of 32 threads would allow 64 blocks by threads, but $B_{\max} = 32$ caps them at 32 blocks, which is $1024/2048 = 50\%$. A block that uses 100 KB of shared memory fits only 2 times.

**The Best Practices Guide's examples (Section 11.1.1, compute capability 7.0).** With 65,536 registers, 64 warps and $r = 37$: $\rho = 1280$ and $W_R = 4 \lfloor 16384/1280 \rfloor = 48$. Blocks of 128 threads (4 warps) give 12 blocks and 75%. Blocks of 320 threads (10 warps) give $\lfloor 48/10 \rfloor = 4$ blocks, 40 warps, and 62.5%, which the guide rounds to 63%. Without the partition rule, $\lfloor 65536/1280 \rfloor = 51$ warps would give 5 blocks and 78%, which does not match the guide.

The Python code of this page computes $b$ by the formula and by a brute force that places blocks one at a time, warp by warp, on 4 register partitions, until one resource runs out. The tests check that the two agree for 10 block sizes, 11 register counts and 5 shared memory sizes on three compute capabilities, and they check every example above. No CUDA code runs in the tests.

## Where it is used

Occupancy is the first number to check when a kernel is slow and the [roofline model](/roofline-model/) says that it should be faster. A kernel that is limited by latency gains from higher occupancy, by fewer registers per thread (`__launch_bounds__` or `-maxrregcount`), by less shared memory per block, or by a block size that fits the SM limits; the Best Practices Guide recommends block sizes that are multiples of 32 (Section 11.3). A kernel that is limited by bandwidth or compute gains nothing from it. [Shared memory tiling](/shared-memory-tiling/) and register tiling trade occupancy for reuse, as in Volkov's matrix multiply. [Persistent threads](/persistent-threads/) and the grid barrier of [cooperative groups](/cooperative-groups/) launch exactly as many blocks as can be resident, which is $b$ times the number of SMs. [Warp-level primitives](/warp-level-primitives/) save shared memory and so can raise occupancy.

## References
