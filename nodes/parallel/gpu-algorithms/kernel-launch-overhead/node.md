---
tag: EGK2KC
kind: concept
slug: kernel-launch-overhead
name: Kernel launch overhead
aliases:
- launch latency
- launch cost
area: parallel/gpu-algorithms
level: core
summary: The fixed time that each GPU kernel launch costs on the host and the device, apart from the kernel's work; it makes tiny kernels slow, and CUDA Graphs, fusion and fewer syncs reduce it.
prereqs: [cuda-programming-model, cuda-streams]
see_also: [kernel-fusion, cuda-streams, host-device-data-transfer, persistent-threads, dynamic-parallelism, amdahls-law, occupancy, latency-hiding]
sources:
  - url: https://developer.nvidia.com/blog/cuda-graphs/
    title: Alan Gray, Getting started with CUDA Graphs, NVIDIA Technical Blog, 5 September 2019
    locator: the benchmark of 20 short kernels repeated for 1000 steps on a V100 with CUDA 10.1, and the measured times per kernel of 9.6, 3.8 and 3.4 microseconds for a sync after each kernel, one sync per step, and a graph
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 2.5.9.2 (introduction to CUDA Graphs with stream capture, Listing 2 from Gray 2019), Section 3.1.4 (programmatic dependent kernel launch), Section 4.2 (CUDA Graphs, the per-kernel overhead in a stream and its payment once at instantiation), 4.2.2 (definition, instantiation and execution) and 4.2.3 (updating instantiated graphs)
  - url: https://docs.nvidia.com/cuda/archive/12.0.0/cuda-c-programming-guide/index.html
    title: NVIDIA, CUDA C++ Programming Guide, version 12.0
    locator: Section 3.2.8.7 (CUDA Graphs, the separation of definition and execution and the reduced CPU launch cost)
  - paper: doi:10.1145/1498765.1498785
    title: Samuel Williams, Andrew Waterman and David Patterson, Roofline, an insightful visual performance model for multicore architectures, Communications of the ACM 52(4), 2009, 65 to 76
    locator: the time of a memory-bound kernel as bytes over bandwidth, used here to size a kernel against the launch cost
---

Kernel launch overhead is the fixed time that each GPU kernel launch costs, apart from the useful work of the kernel. The host spends time in the API call and the driver, the command travels to the GPU, the GPU sets up the grid, and at the end the GPU must see that the last block has finished. This cost is a few microseconds on current systems, and it does not depend on the size of the kernel. A kernel that runs for a millisecond does not notice it. A kernel that runs for a few microseconds can spend most of its time in overhead. The fixes are to launch fewer kernels (by [fusion](/kernel-fusion/) or [persistent threads](/persistent-threads/)), to avoid a host synchronization after each launch, and to launch a whole sequence at once as a CUDA Graph.

## In plain words

Think of a printing shop where each job needs a form, a check of the order and the set-up of the press before the first page comes out. If you print a book, the set-up is a small part of the job. If you print a thousand business cards one card per job, almost all the time goes to set-up. You can ask for all thousand cards in one job, or you can give the shop a standing order that it sets up once and then repeats. A GPU kernel launch is such a job, and a CUDA Graph is such a standing order.

## The idea

The model of the GPU is the [SIMT model](/simt-model/) with warps of 32 threads, and the time of a kernel body follows the [roofline model](/roofline-model/). This page adds a fixed cost per launch.

| symbol | meaning |
|---|---|
| $n$ | the number of elements a kernel processes |
| $p$ | the number of processors |
| $W$, $S$, $T_p$ | the work, the span and the time on $p$ processors |
| $M$, $B$ | the fast memory size and the memory transaction size |
| $k$ | the number of kernels in a sequence |
| $\tau$ | the time of one kernel body |
| $o$ | the overhead per kernel that is not hidden |
| $c$ | the host time to issue one launch |
| $g$ | the gap on the device between the end of one kernel and the start of the next |
| $C$ | the one-time cost of instantiating a graph |

**The fixed cost.** If each of $k$ kernels has a body of time $\tau$ and an overhead $o$ that nothing hides, the sequence takes
$$T = k(\tau + o),$$
and the fraction of time spent in kernel bodies is
$$\eta = \frac{\tau}{\tau + o}.$$
The efficiency is one half when $\tau = o$. The overhead $o$ is not one number. It depends on the GPU, the driver, the host CPU, the operating system, the number of kernel arguments, and above all on how the program waits for the GPU.

**Why tiny kernels are slow.** A kernel launch is asynchronous: the host call returns before the kernel runs (CUDA Programming Guide 13.5, Section 2.5). If the host does not wait, it can issue the next launch while the GPU runs the current kernel, and the host cost $c$ is hidden behind the body $\tau$. Let the host issue launch $i$ at time $ic$, and let kernel $i$ start at the later of that time and the end of kernel $i-1$ plus a device gap $g$. Then kernel $i$ starts at $i \cdot \max(c, \tau + g)$, so a long sequence costs
$$\max(c,\ \tau + g)$$
per kernel. There are two regimes. If $\tau + g \ge c$, the device is the bottleneck, and only the small gap $g$ is lost. If $\tau + g < c$, the host is the bottleneck, and the GPU waits for each launch. Very short kernels are in the second regime. A synchronization after each launch (for example `cudaDeviceSynchronize`, or a `cudaMemcpy` that reads a flag) is worse still: it removes the overlap, so the full round trip is paid each time.

**Size of a useful kernel.** A memory-bound kernel that moves $b$ bytes per element at a device bandwidth $\beta_{\text{dev}}$ has $\tau = bn/\beta_{\text{dev}}$. Its body is as long as the overhead when
$$n = \frac{o \cdot \beta_{\text{dev}}}{b}.$$
Below this size, more than half of the time is overhead.

**CUDA Graphs.** A graph is a set of operations (kernels, copies, memory sets and others) with the dependencies between them. You can build it with the graph API or by stream capture. The work has three stages: definition, instantiation and execution (13.5 guide, Section 4.2.2). The guide says that in a stream the host driver must do the set-up for each kernel that is issued, and that for short kernels this "can be a significant fraction of the overall end-to-end execution time". With a graph, these costs "can be paid once for the entire graph during instantiation, and the graph itself can then be launched repeatedly with very little overhead" (Section 4.2). If an instantiated graph needs new parameters, you can update it without a new instantiation, within limits (Section 4.2.3). A graph pays if the savings of its launches are larger than the instantiation cost $C$. If a graph of $k$ kernels saves $\delta$ per kernel each time it runs, the break-even number of launches is
$$r = \left\lceil \frac{C}{k\,\delta} \right\rceil.$$

**Other ways to cut the cost.**

- [Kernel fusion](/kernel-fusion/) removes launches, and it also removes the traffic between the fused kernels. These are two different savings.
- [Persistent threads](/persistent-threads/) launch one grid that loops over the work, so that there is one launch for many tasks.
- Programmatic dependent launch lets a second kernel in the same stream start before the first one has finished, so that the launch of the second kernel overlaps the end of the first (13.5 guide, Section 3.1.4).
- [Dynamic parallelism](/dynamic-parallelism/) launches from the device. This removes the trip to the host, but device launches also have a cost.

Launch overhead is a different cost from the cost of [host-device data transfer](/host-device-data-transfer/) and from the concurrency that [CUDA streams](/cuda-streams/) give. A program can have little data to move and still be slow because it launches too many small kernels.

## Examples

**Gray's measurement.** Gray (2019) ran 20 copies of a kernel whose body takes 2.9 µs, repeated for 1000 steps, on a V100 with CUDA 10.1. He measured the time per kernel for three ways to launch the sequence. These are measurements of one system. Other GPUs, drivers and CPUs give other numbers, and newer drivers have changed them.

| way to launch | time per kernel | implied overhead $o$ | efficiency $\eta$ | time per step of 20 kernels |
|---|---|---|---|---|
| sync after each kernel | 9.6 µs | 6.7 µs | 29/96, about 30% | 192 µs |
| launches back to back, one sync per step | 3.8 µs | 0.9 µs | 29/38, about 76% | 76 µs |
| one graph per step | 3.4 µs | 0.5 µs | 29/34, about 85% | 68 µs |

The first step, removing the sync after each kernel, gives the largest gain, because it lets the host cost hide behind the kernel bodies. The graph then removes most of what is left.

**Break-even of a graph.** Assume that instantiation costs $C = 100$ µs, which is an assumption for the example and not a measured value. With the savings of the table, a graph of 20 kernels saves $\delta = 3.8 - 3.4 = 0.4$ µs per kernel, which is 8 µs per launch of the graph. Then $C/(k\delta) = 100/8 = 12.5$, so the graph pays from the 13th launch. A simulation loop that runs the same graph thousands of times pays the instantiation cost back many times. A graph that is built for a single run does not.

**A tiny kernel.** Assume an overhead of $o = 3$ µs and a device bandwidth of 1000 GB/s, both round values for the example. A vector add moves 12 bytes per element, so its body is as long as the overhead at $n = 3 \cdot 10^{-6} \cdot 10^{12} / 12 = 250\,000$ elements. A vector add of 10 000 elements spends about 96% of its time in overhead. Assume further that the host needs $c = 5$ µs per launch and the gap is $g = 1$ µs. Then 100 kernels with bodies of 0.5 µs take $0.5 + 99 \cdot 5 = 495.5$ µs, because the host is the bottleneck, while 100 kernels with bodies of 20 µs take $20 + 99 \cdot 21 = 2099$ µs, of which more than 95% is useful work.

The CUDA C++ code below captures a sequence of short kernels into a graph once and then replays it. The tests do not run this CUDA code. They check the cost model and the numbers above with exact fractions.

```cuda
__global__ void step(float* out, const float* in, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) out[i] = 1.23f * in[i];
}

// Without a graph: k launches per step, and no sync between them.
for (int s = 0; s < steps; ++s) {
    for (int j = 0; j < k; ++j)
        step<<<blocks, 256, 0, stream>>>(out, in, n);
    cudaStreamSynchronize(stream);         // one sync per step, not one per kernel
}

// With a graph: capture the k launches once, instantiate once, replay.
cudaGraph_t graph;
cudaGraphExec_t exec;
cudaStreamBeginCapture(stream, cudaStreamCaptureModeGlobal);
for (int j = 0; j < k; ++j)
    step<<<blocks, 256, 0, stream>>>(out, in, n);   // recorded, not run
cudaStreamEndCapture(stream, &graph);
cudaGraphInstantiate(&exec, graph, 0);             // the one-time cost C
for (int s = 0; s < steps; ++s) {
    cudaGraphLaunch(exec, stream);                 // one launch call for k kernels
    cudaStreamSynchronize(stream);
}
cudaGraphExecDestroy(exec);
cudaGraphDestroy(graph);
```

## Where it is used

- **Deep learning inference.** A small batch runs many short kernels, one or more per layer. Frameworks capture the whole forward pass as a graph, or fuse layers, to remove launch costs.
- **Time-stepping simulations.** Each step runs the same short sequence of kernels many times, which is the case where graphs pay back their instantiation.
- **Iterative solvers.** A conjugate gradient step has several small reductions and vector updates. Fusion of these kernels and a graph per iteration both reduce the overhead.
- **Kernel design.** The overhead sets a lower bound on useful kernel size. A kernel that is too small should be fused, batched with other work, or run on the CPU.
- **Persistent and device-side designs.** [Persistent threads](/persistent-threads/) and [dynamic parallelism](/dynamic-parallelism/) are partly motivated by the cost of many host launches.

## References
