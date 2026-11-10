---
tag: EQNK0G
kind: concept
slug: warp-divergence
name: Warp divergence
aliases:
- branch divergence
area: parallel/gpu-algorithms
level: intro
summary: When the lanes of a warp take different branches, the warp runs each taken path in turn under an active mask, so a branch costs the sum of its paths and a loop costs its longest trip.
prereqs: [simt-model]
see_also: [warp-level-primitives, parallel-reduce, compaction, occupancy, thread-block-and-grid, warp-aggregated-atomics, persistent-threads]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 3.2.2.1 (SIMT execution model, divergent paths run with the other threads disabled) and Section 3.2.2.1.1 (independent thread scheduling from compute capability 7.0)
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition
    locator: Chapter 4 (control divergence) and Chapter 10 (reduction, minimizing control divergence)
  - url: https://developer.download.nvidia.com/assets/cuda/files/reduction.pdf
    title: Mark Harris, Optimizing parallel reduction in CUDA, NVIDIA, 2007
    locator: the slides on interleaved addressing with a divergent branch and on sequential addressing
---

**Warp divergence** happens when the lanes of one [warp](/simt-model/) take different paths at a branch. The warp issues one instruction at a time for all its lanes, so it runs each path that some lane takes, one after another, and disables the lanes that are not on the current path (CUDA Programming Guide v13.5, Section 3.2.2.1). The cost of a divergent branch in the [SIMT model](/simt-model/) is the sum of the costs of its paths, and the cost of a loop is the trip count of its slowest lane. Branches whose condition is the same for all lanes of a warp cost only the path taken.

## In plain words

A team of thirty-two workers gets one order at a time from a single foreman. When the order is "if your box is red, paint it; else, sand it", the foreman cannot give both orders at once. He first tells the workers with red boxes to paint while the others stand still, and then tells the others to sand while the painters stand still. The team takes the time of both jobs. If all boxes of a team are red, the sanding order is skipped. The same happens with repeated work: if one worker must repeat a job ten times and the others only twice, the whole team waits until the ten are done. So it pays to put workers with the same kind of box, or the same amount of work, in one team.

## The idea

### Masks

At each instruction, a warp has an **active mask**: a 32-bit word whose bit $\ell$ is 1 when lane $\ell$ runs the instruction. At a branch with condition $c$, the warp computes $c$ in every active lane. The lanes with $c$ true form the mask $m_1$ and the others $m_0$. If $m_1$ or $m_0$ is empty, the warp runs only one path. Otherwise it runs the first path with mask $m_1$ and the second with mask $m_0$, and after both paths it continues with the union.

### The cost

Let each lane $\ell$ of a warp run the sequence of instructions $P_\ell$. In the SIMT model, the warp issues each distinct instruction of $\bigcup_\ell P_\ell$ once, so

$$\text{issued} = \Bigl\lvert \bigcup_{\ell} P_\ell \Bigr\rvert, \qquad \text{lane instructions} = \sum_\ell \lvert P_\ell \rvert, \qquad \text{efficiency} = \frac{\sum_\ell \lvert P_\ell \rvert}{32 \cdot \text{issued}}.$$

For a branch with paths of $a$ and $b$ instructions, a divergent warp issues $a + b$ of them, against $a$ or $b$ for a warp that agrees. For a loop, the instruction in iteration $j$ is distinct from the same instruction in iteration $j'$, so the warp runs $\max_\ell t_\ell$ iterations, where $t_\ell$ is the trip count of lane $\ell$. Divergence is a cost, not an error: the result is the same as if each thread ran alone.

### Reconvergence

Before compute capability 7.0, a warp had one program counter and joined its paths again at a fixed point after the branch. From compute capability 7.0, each thread has its own program counter, and the scheduler can interleave the diverged groups of a warp at sub-warp granularity (Guide Section 3.2.2.1.1). This lets code with locks between lanes of one warp make progress, but the groups are not guaranteed to join right after the branch. Code that needs the whole warp together, such as a [warp shuffle](/warp-level-primitives/), must say so with `__syncwarp()` or a `_sync` function with a mask.

### How to reduce divergence

- **Make conditions uniform per warp.** Use a condition on `threadIdx.x / 32` or on the block, not on the lane. For data-dependent work, sort or bucket the items so that a warp gets items of the same kind or size.
- **Pack the active threads.** Instead of keeping every second thread active, keep the first half active, so that whole warps go idle and skip the path. The [tree reduction](/parallel-reduce/) below shows the effect.
- **Make the paths short.** Move common code out of the branch, so that only the different part is repeated. The compiler may turn a short branch into predicated instructions, which issue both sides but avoid the branch.
- **Compact the work.** Use a ballot or a [compaction](/compaction/) to collect the items that need the expensive path, and process them with full warps.
- **Do not fear the bounds guard.** `if (i < n)` diverges in at most one warp of the grid.

## Examples

**Odd and even lanes.** `if (threadIdx.x % 2 == 0) { a instructions } else { b instructions }` diverges in every warp, and each warp issues the condition, $a + b$ path instructions and the join. With $a = b$, the efficiency of the branch is 50%. With `if ((threadIdx.x / 32) % 2 == 0)`, each warp runs one path and the efficiency is 100%.

**A tree sum in shared memory.** A block of $T = 256$ threads (8 warps) sums 256 values in $\log_2 256 = 8$ levels. Both layouts below do the same $255$ adds.

```cpp
// interleaved: divergent in every warp while the stride s is below 32
for (int s = 1; s < blockDim.x; s *= 2) {
    if (tid % (2 * s) == 0) sh[tid] += sh[tid + s];
    __syncthreads();
}
// sequential: the active threads are tid < s, so whole warps go idle
for (int s = blockDim.x / 2; s > 0; s /= 2) {
    if (tid < s) sh[tid] += sh[tid + s];
    __syncthreads();
}
```

Count the warps that issue the add. Interleaved: at $s = 1, 2, 4, 8, 16$ every one of the 8 warps has an active lane, at $s = 32$ four warps do, at $s = 64$ two, and at $s = 128$ one, for $5 \cdot 8 + 4 + 2 + 1 = 47$ warp issues. Sequential: $4 + 2 + 1$ warps for $s = 128, 64, 32$, then one warp for each of the 5 levels with $s < 32$, for $12$ warp issues. This is the step from the first to the second kernel in Harris's reduction slides. The sequential layout also avoids [bank conflicts](/shared-memory-bank-conflicts/), because the active lanes read consecutive words.

**Loops with uneven trip counts.** For 1024 items with trip counts drawn uniformly from 1 to 63 (seed 13 in the tests), a loop with one body instruction and one test per trip issues 3940 warp instructions for 64,526 lane instructions, an efficiency of 51%. Sorting the items by trip count first, so that each warp gets 32 similar counts, cuts the issues to 2076 and raises the efficiency to 97%.

The Python code of this page records the labels that each thread runs and counts one issue per distinct label per warp. The tests check that a divergent branch costs $2 + a + b$ for path lengths 0 to 4, that a warp-uniform branch costs one path, the masks of a branch, that a loop costs $3 \max_\ell t_\ell + 1$ issues for a body of 2 on 50 seeded trip-count vectors, the sorting example, and the 47 and 12 of the tree sum. The CUDA code on this page is for the reader; the tests do not run it.

## Where it is used

Divergence shapes the design of most GPU kernels with control flow. [Parallel reduction](/parallel-reduce/) and [scans](/all-prefix-sums/) pack the active threads at each level. Graph kernels on GPUs, which give one thread per vertex, diverge when degrees differ, so they group vertices by degree or give high-degree vertices a whole warp. [Compaction](/compaction/) removes inactive items so that later kernels run on full warps. [Warp-aggregated atomics](/warp-aggregated-atomics/) let one elected lane do the atomic for the warp, and [persistent threads](/persistent-threads/) with work queues let warps pick up new work instead of idling. Ray tracing and Monte Carlo kernels with paths of random length often regroup their threads for the same reason.

## References
