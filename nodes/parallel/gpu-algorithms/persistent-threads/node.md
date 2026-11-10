---
tag: NMFBCT
kind: technique
slug: persistent-threads
name: Persistent threads
aliases:
- persistent kernels
- persistent blocks
- uber-kernels
area: parallel/gpu-algorithms
level: advanced
summary: Launch only as many GPU threads as can be resident at once and let them loop, taking work from a queue, instead of one thread per item; this balances irregular work and avoids relaunches.
prereqs: [cuda-programming-model, occupancy, fetch-and-add]
see_also: [kernel-launch-overhead, warp-aggregated-atomics, warp-specialization, dynamic-parallelism, list-scheduling, decoupled-look-back-scan, cooperative-groups, cuda-streams]
sources:
  - paper: doi:10.1109/InPar.2012.6339596
    title: Kshitij Gupta, Jeff A. Stuart and John D. Owens, A study of persistent threads style GPU programming for GPGPU workloads, Innovative Parallel Computing (InPar) 2012
    locator: the definition of the persistent threads style (as many threads as the GPU can hold at once, each looping over work) and its four use cases, CPU-GPU synchronization, load balancing of irregular work, producer-consumer locality and global synchronization
  - paper: doi:10.1145/1572769.1572792
    title: Timo Aila and Samuli Laine, Understanding the efficiency of ray traversal on GPUs, High Performance Graphics 2009, 145 to 149
    locator: the persistent threads ray traversal kernel, in which warps fetch new rays from a global pool with an atomic counter instead of relying on the hardware work distribution
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 4.4.8 and 4.4.8.1 (cooperative launch and its requirements), Section 5.7.3.6.2.1 (grid synchronization, and the grid sized with cudaOccupancyMaxActiveBlocksPerMultiprocessor times the number of SMs)
  - paper: doi:10.1137/0117039
    title: Ronald L. Graham, Bounds on multiprocessing timing anomalies, SIAM Journal on Applied Mathematics 17(2), 1969, 416 to 429
    locator: the bound of list scheduling, the total work over p plus the largest job
---

Persistent threads is a style of GPU programming in which a kernel launches only as many threads (or blocks, or warps) as the GPU can hold at the same time. These threads stay alive for the whole run. Each one loops: it takes a piece of work from a queue in global memory, does it, and goes back for more, until the queue is empty. The usual style is the opposite: one thread per data item, and the hardware block scheduler gives blocks to the streaming multiprocessors. Persistent threads move that scheduling into software. This lets a program balance irregular work at the level of a warp, keep state on the chip between tasks, run many rounds in one launch, and do a grid-wide synchronization. The cost is more complex code, a global queue that can become a hot spot, and the risk of a deadlock or a GPU that no other work can use.

## In plain words

A call centre can hire a new worker for each call and send each worker home after one call. Or it can keep a fixed team at their desks all day, and each worker takes the next call from the queue when the last call ends. The second way saves the time to hire and send home, and no desk stands empty while a long call keeps one worker busy. But the team must not be larger than the number of desks. If a rule says that no one may go home until everyone has arrived, and some workers are still waiting outside for a desk, then nobody goes home.

## When it applies

Persistent threads help when:

- the cost of the tasks varies a lot, so that a static split leaves some threads idle while others still work, and a finer split than one block per task is useful (Aila and Laine 2009);
- the work comes in many dependent rounds, so that one launch per round would add a launch cost and a host round trip per round (see [kernel launch overhead](/kernel-launch-overhead/));
- tasks make new tasks during the run, as in a work list, so that the amount of work is not known at launch;
- data or state should stay in registers or shared memory from one task to the next (producer-consumer locality in Gupta, Stuart and Owens 2012);
- the program needs a barrier across the whole grid.

They do not help a regular kernel where each item costs the same. There the hardware scheduler is already good, and the software loop only adds cost.

## The template

The model is the [SIMT model](/simt-model/) with warps of 32 threads, and the time of each task follows the [roofline model](/roofline-model/). The scheduling part is [list scheduling](/list-scheduling/) of tasks on $p$ workers.

| symbol | meaning |
|---|---|
| $n$ | the number of tasks |
| $p$ | the number of persistent workers (warps or blocks) that are resident at once |
| $W$, $S$, $T_p$ | the work, the span and the time on $p$ processors |
| $M$, $B$ | the fast memory size and the memory transaction size |
| $c_i$ | the cost of task $i$ |
| $g$ | the number of tasks that one fetch takes (the batch size) |
| $a$ | the cost of one fetch (one atomic on the queue counter) |
| $r$ | the number of rounds |

**Size of the grid.** The grid must not be larger than what the GPU can hold at once. With $s$ streaming multiprocessors and $k$ resident blocks per multiprocessor for this kernel, launch $p = s \cdot k$ blocks. The CUDA Programming Guide 13.5 (Section 5.7.3.6.2.1) shows this with `cudaOccupancyMaxActiveBlocksPerMultiprocessor` and `multiProcessorCount`. The value of $k$ depends on the registers and shared memory of the kernel, and on the limits of the GPU, which change between compute capabilities (see [occupancy](/occupancy/)).

**The worker loop.** A global counter `next` starts at 0. Each worker repeats the steps below. In the warp form, one lane does the atomic add and broadcasts the result with a shuffle, and the lanes share the $g$ tasks.

```pseudo id=main
PERSISTENT-WORKER(next, tasks, n, g)          ▷ run by each of the p resident workers
L1   loop
L2     base ← ATOMIC-ADD(next, g)               ▷ take the next g tasks
L3     if base ≥ n then return                  ▷ the queue is empty
L4     for i ← base to min(n, base + g) − 1 do PROCESS(tasks[i])
L5   end loop                                    ▷ go back for more work
```

**Why every task runs once.** The atomic add gives each fetch a different value of `base`, and the values are $0, g, 2g, \ldots$ in some order. So the ranges $[base, base + g)$ are disjoint and together cover $[0, n)$. A worker stops only when its range starts at or after $n$, so no task is lost.

**Time.** Each fetch is a job of cost $a$ plus the costs of its tasks. A worker takes a new job as soon as it is free, which is list scheduling, so Graham's bound gives
$$T_p \le \frac{W + a\lceil n/g \rceil}{p} + \max_{\text{batch}}\Big(a + \sum_{i \in \text{batch}} c_i\Big) + a,$$
where $W = \sum_i c_i$ and the last $a$ is the failed fetch at the end. The number of atomics on the counter is $\lceil n/g \rceil + p$. A larger $g$ means fewer atomics, but larger batches, and so a worse last term. With $g = 1$ and $a$ small, the time is close to $W/p + \max_i c_i$, which is near the best possible.

**Rounds.** A job of $r$ dependent rounds, each of time $t$, takes $r(o + t)$ with one launch of cost $o$ per round. In one persistent kernel with a grid barrier of cost $b$ per round, it takes $o + r(t + b)$. The persistent form wins when $b < o$, and it also saves the host round trip if the host had to decide whether to launch the next round.

The CUDA C++ kernel below is the warp form of the loop. It assumes that `blockDim.x` is a multiple of 32. The tests do not run this CUDA code. They run the Python model of the queue and of the grid barrier.

```cuda
__device__ unsigned int next_task = 0;    // reset to 0 before each launch

__global__ void persistent(const Task* tasks, unsigned int n) {
    const unsigned int lane = threadIdx.x % 32;
    const unsigned int G = 32;                          // one task per lane per fetch
    while (true) {
        unsigned int base = 0;
        if (lane == 0) base = atomicAdd(&next_task, G); // one atomic per warp
        base = __shfl_sync(0xffffffffu, base, 0);       // every lane gets the same base
        if (base >= n) return;                          // the whole warp leaves together
        unsigned int i = base + lane;
        if (i < n) process(tasks[i]);
    }
}

// Host: one grid that fits on the GPU at once.
int per_sm = 0, sms = 0;
cudaOccupancyMaxActiveBlocksPerMultiprocessor(&per_sm, persistent, 256, 0);
cudaDeviceGetAttribute(&sms, cudaDevAttrMultiProcessorCount, 0);
persistent<<<sms * per_sm, 256>>>(d_tasks, n);
```

## Classic examples

- **Ray traversal.** Aila and Laine (2009) found that rays of very different lengths made the hardware work distribution waste time on GPUs of that period. In their persistent kernel, each warp takes a new batch of rays from a global pool with an atomic counter as soon as its rays are done. The example in the Python file shows the same effect: for 8 tasks with costs $10, 10, 10, 10, 1, 1, 1, 1$ on 2 workers, a static split into halves takes 40, while fetching one task at a time takes 22, which equals $W/p$. Fetching 4 tasks at a time takes 40 again, because the batch is the same as the static half.
- **The four uses of Gupta, Stuart and Owens (2012).** They studied the style on micro-benchmarks for CPU-GPU synchronization, load balancing of irregular work, producer-consumer locality and global synchronization, and they discussed when it helps and when it does not.
- **Single-pass scans.** A [decoupled look-back scan](/decoupled-look-back-scan/) takes tile numbers from a global counter, so that tiles start in the order of their numbers. This is the same fetch as in the template, and it avoids a deadlock that depends on the order in which the hardware starts blocks.
- **Work lists in graph algorithms.** Traversals keep a queue of vertices and run many rounds inside one kernel. They use a grid barrier or a counter per round.
- **Fused multi-stage kernels.** Large matrix multiplication and attention kernels on recent GPUs often launch one block per SM that loops over output tiles. This keeps the pipeline of copies and math busy across tiles, and it is often combined with [warp specialization](/warp-specialization/).

## Variations

- **Static persistent loop.** Each worker takes tasks $w, w + p, w + 2p, \ldots$ with no counter. This gives the reuse of state and the single launch, but not the load balance.
- **Batch size.** The fetch size $g$ trades the atomic traffic against the balance at the end. Some codes start with large batches and make them smaller as the queue empties.
- **Per-block or per-warp queues with stealing.** Each worker has its own queue and steals from others when it is empty, as in [work stealing](/work-stealing/). This removes the single hot counter.
- **Fetch with aggregated atomics.** One lane fetches for the whole warp, as in [warp-aggregated atomics](/warp-aggregated-atomics/).
- **Cooperative launch.** `cudaLaunchCooperativeKernel` checks that all blocks of the grid can be resident at once, and allows `grid.sync()` from [cooperative groups](/cooperative-groups/) (13.5 guide, Sections 4.4.8 and 4.4.8.1). This is the supported way to get a grid barrier.

## Pitfalls

- **Deadlock at a grid barrier.** If the grid has more blocks than the GPU can hold, the resident blocks wait at the barrier for blocks that cannot start until a resident block ends. The Python model shows this: 8 blocks on room for 8 finish, and 9 blocks deadlock. A hand-written barrier with a spin on a global counter has this risk. Use cooperative launch, which fails at launch if the grid is too large.
- **The size of the GPU is not fixed.** The number of SMs and of resident blocks per SM depends on the GPU and on the kernel's resources. A grid size that is safe on one GPU can deadlock on another. Compute it at run time.
- **Other work on the same GPU.** Other kernels, other streams or other processes can take part of the GPU. Then fewer of your blocks are resident than you computed.
- **Spinning wastes the machine.** A worker that waits in a loop on a flag uses an issue slot, and on some GPUs it can stop the progress of the warp it waits for. Use the barriers of cooperative groups, or `__nanosleep` in the spin loop on GPUs that support it.
- **Hot counter.** All workers hit one atomic counter. With small tasks, the atomics become the bottleneck. Fetch in batches, aggregate per warp, or use several queues.
- **The hardware scheduler was good enough.** For regular work, the plain one-thread-per-item kernel is often as fast and much simpler. Gupta, Stuart and Owens (2012) found that the benefit depends on the workload. Measure first.
- **Long kernels.** A kernel that never ends can hit a watchdog on a GPU that also drives a display, and it can hold the GPU against other users.
- **Forgetting to reset the counter.** The queue counter must be reset before each launch, with a copy or a memset in the same stream.

## Exercises

1. Prove that the template runs every task exactly once, also when $g$ does not divide $n$.
2. Show that the number of atomic fetches is $\lceil n/g \rceil + p$, and give the time bound of the template for $g = 32$, $a = 1$ and task costs that are all 1, with $n = 3200$ and $p = 10$.
3. For the costs $10, 10, 10, 10, 1, 1, 1, 1$ on 2 workers, find the time with $g = 2$, and the order of tasks that makes the static split as good as the dynamic one.
4. A job has $r = 1000$ rounds of $10$ µs each. With an assumed launch cost of 5 µs and a grid barrier cost of 2 µs, compare one launch per round with one persistent kernel. At what barrier cost do the two take the same time?
5. A persistent kernel uses a hand-written grid barrier and is tuned on a GPU with 80 SMs and 2 resident blocks per SM. Explain what happens when it runs with a grid of 160 blocks on a GPU with 68 SMs, and how cooperative launch changes the outcome.

## References
