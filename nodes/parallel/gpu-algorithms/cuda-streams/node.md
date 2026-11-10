---
tag: GVJ1ZR
kind: concept
slug: cuda-streams
name: CUDA streams
aliases:
- GPU streams
- asynchronous queues
- command queues
area: parallel/gpu-algorithms
level: core
summary: A CUDA stream is an in-order queue of GPU work; work in different streams may run at the same time, which lets copies overlap kernels, and events order and time work across streams.
prereqs: [cuda-programming-model, host-device-data-transfer]
see_also: [host-device-data-transfer, kernel-launch-overhead, kernel-fusion, latency-hiding, flow-shop-scheduling, persistent-threads, dynamic-parallelism, amdahls-law]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 2.5.2 (streams, 2.5.2.2 kernels and 2.5.2.3 copies in streams, pinned memory for asynchronous copies), Section 2.5.3 (events and timing), Section 2.5.5 (in-order streams), Section 2.5.6 (blocking and non-blocking streams), 2.5.6.1 (legacy default stream) and 2.5.6.2 (per-thread default stream since CUDA 7), Section 2.5.7 (explicit synchronization, cudaStreamWaitEvent), Section 2.5.8 (implicit synchronization), Section 2.5.9.1 (stream priorities) and 2.5.9.2 (graphs by stream capture)
  - url: https://docs.nvidia.com/cuda/archive/12.0.0/cuda-c-programming-guide/index.html
    title: NVIDIA, CUDA C++ Programming Guide, version 12.0
    locator: Section 3.2.8.2 (concurrent kernel execution, the concurrentKernels property), Section 3.2.8.3 (overlap of copies and kernels, asyncEngineCount greater than zero and page-locked memory), Section 3.2.8.4 (copies in both directions when asyncEngineCount is 2) and Section 3.2.8.5.2 (default stream)
  - url: https://developer.nvidia.com/blog/how-overlap-data-transfers-cuda-cc/
    title: Mark Harris, How to overlap data transfers in CUDA C/C++, NVIDIA Technical Blog, 13 December 2012
    locator: the two issue orders of a chunked copy, kernel and copy pipeline, and the times measured on a Tesla C1060, C2050 and K20c with their explanation by copy engines and Hyper-Q
---

A CUDA stream is a queue of GPU work, such as copies and kernel launches, that runs in the order in which the host put the work in. Work in different streams has no order between it, so the GPU may run it at the same time. With streams, a program can copy one chunk of data while a kernel works on another chunk, and run small independent kernels side by side. Events mark points in a stream. A stream can wait for an event in another stream, and the host can time the work between two events. The default stream needs care: the legacy default stream synchronizes with other streams, while the per-thread default stream does not.

## In plain words

Think of a bank with a few counters. Each customer has a list of tasks, and the customer must do them in order: first the deposit, then the transfer. Two customers can be at different counters at the same time. A stream is one customer's list. The counters are the parts of the GPU: one or two copy engines and the compute units. If you send all the work as one customer, only one counter is busy at a time. If you split the work among several customers, one can use the copy counter while another uses the compute counter. An event is a note that one customer leaves when a task is done, so that another customer can wait for it.

## The idea

The model of the GPU is the [SIMT model](/simt-model/) with warps of 32 threads. The time of each operation comes from the [roofline model](/roofline-model/) for kernels and from the model of [host-device data transfer](/host-device-data-transfer/) for copies. This page adds engines that run at the same time and queues that feed them.

| symbol | meaning |
|---|---|
| $n$ | the number of elements |
| $p$ | the number of processors |
| $W$, $S$, $T_p$ | the work, the span and the time on $p$ processors |
| $M$, $B$ | the fast memory size and the memory transaction size |
| $m$ | the number of chunks, one stream per chunk |
| $H$, $K$, $D$ | the total copy-in time, kernel time and copy-out time of the job |
| $\lambda$ | a fixed cost added to each operation (launch or copy latency) |
| $T(m)$ | the time of the job in $m$ chunks |

**Order within a stream.** CUDA streams are in-order. The guide says that "the order of execution of the operations in a stream is the same as the order in which those operations were enqueued" and that an operation "cannot leap-frog other operations" (CUDA Programming Guide 13.5, Section 2.5.5). A copy into a stream always completes before the next operation in that stream starts, so a kernel after a copy in the same stream sees the data.

**Concurrency across streams.** Operations in different streams have no order between them, unless the program adds one. The GPU may run them at the same time, but it does not have to. Whether it does depends on the hardware resources. On a GPU with `asyncEngineCount` greater than zero, a copy to or from page-locked host memory can run at the same time as a kernel. With `asyncEngineCount` equal to 2, a copy to the device and a copy from the device can also run at the same time (CUDA C++ Programming Guide 12.0, Sections 3.2.8.3 and 3.2.8.4). On a GPU with the `concurrentKernels` property, kernels from different streams can run at the same time if each one leaves room on the GPU (Section 3.2.8.2). These properties and their limits change between compute capabilities, so query them on the target GPU. A copy with pageable host memory does not overlap at all: `cudaMemcpyAsync` then reverts to synchronous behavior (13.5 guide, Section 2.5.2.3).

**Events.** `cudaEventRecord(e, s)` puts an event into stream `s`. The event completes when all earlier work in `s` is done. `cudaStreamWaitEvent(s2, e)` makes all later work in stream `s2` wait for `e`. This gives an order between two streams without a stop on the host. Two events around a kernel give its time with `cudaEventElapsedTime` (Sections 2.5.3 and 2.5.7).

**Synchronization with the host.** `cudaStreamSynchronize(s)` blocks the host until stream `s` is empty, and `cudaDeviceSynchronize()` waits for all streams. `cudaStreamQuery(s)` and `cudaEventQuery(e)` test without a block (Section 2.5.7).

**The default stream.** A launch or a copy with no stream argument goes to the default stream. There are two kinds.

- The **legacy default stream** (also called the NULL stream) is shared by all host threads. An operation in it waits for all earlier work in all blocking streams, and later work in blocking streams waits for it. Streams made with `cudaStreamCreate` are blocking. Streams made with `cudaStreamCreateWithFlags(&s, cudaStreamNonBlocking)` do not synchronize with the legacy default stream (13.5 guide, Sections 2.5.6 and 2.5.6.1).
- The **per-thread default stream**, available since CUDA 7, gives each host thread its own default stream that acts like a normal stream and does not synchronize with the others. You turn it on with the `nvcc` option `--default-stream per-thread` or the macro `CUDA_API_PER_THREAD_DEFAULT_STREAM` (Section 2.5.6.2).

With the legacy default stream, one stray `cudaMemcpy` or launch without a stream between two streams' work can remove all overlap. The guide says that two operations from different streams cannot run at the same time if any operation on the NULL stream is submitted between them, unless the streams are non-blocking (Section 2.5.8). It gives two rules: issue all independent operations before dependent ones, and delay synchronization as long as possible.

**Priorities and graphs.** Streams made with `cudaStreamCreateWithPriority` have a priority, and lower numbers mean higher priority (Section 2.5.9.1). A sequence of work in streams, with its events, can be captured into a CUDA Graph and replayed (Section 2.5.9.2). That reduces the [launch overhead](/kernel-launch-overhead/), which is a different cost from the lack of overlap that streams fix.

**The pipeline model.** Split a job with copy-in time $H$, kernel time $K$ and copy-out time $D$ into $m$ equal chunks, one stream per chunk, and give each operation a fixed extra cost $\lambda$. Each chunk then has three stages of time $H/m + \lambda$, $K/m + \lambda$ and $D/m + \lambda$. With two copy engines, the chunks flow through three engines like jobs through a three-stage [flow shop](/flow-shop-scheduling/), and the time is
$$T(m) = \left(\tfrac{H}{m} + \tfrac{K}{m} + \tfrac{D}{m} + 3\lambda\right) + (m - 1)\max\left(\tfrac{H}{m}, \tfrac{K}{m}, \tfrac{D}{m}\right) + (m-1)\lambda.$$
The first term is the time of the first chunk through all stages. Each later chunk adds one step of the slowest stage. With $\lambda = 0$, $T(m)$ falls from $H + K + D$ toward $\max(H, K, D)$ as $m$ grows. With $\lambda > 0$, too many chunks add too much fixed cost, and the best $m$ is near $\sqrt{(H + K + D - \max(H,K,D))/\lambda}$. Overlap can at best hide the shorter stages behind the longest one. It cannot make the longest one faster.

**Issue order.** On GPUs where each engine takes work in the order the host issued it, the issue order matters. With one copy engine, the copy-out of chunk 1 sits in the same queue as the copy-in of chunk 2 and blocks it until the kernel of chunk 1 is done. Harris (2012) measured this effect on three GPUs. GPUs from compute capability 3.5 have several hardware queues (Hyper-Q), which removes most of the sensitivity to issue order. The model in the Python file uses one first-in first-out queue per engine, so it shows the older behavior.

## Examples

**The effect of chunking and issue order.** A job has $H = K = D = 4$ ms, and $\lambda = 0$. All numbers are assumptions for the example.

| setup | time |
|---|---|
| one stream | 12 ms |
| 4 streams, 2 copy engines, any issue order | 6 ms |
| 4 streams, 1 copy engine, each chunk issued in full (copy-in, kernel, copy-out) | 12 ms |
| 4 streams, 1 copy engine, all copies-in, then all kernels, then all copies-out | 8 ms |

With two copy engines, the four chunks take $3 \cdot 1 + 3 \cdot 1 = 6$ ms, which is half of the serial time. With one engine in first-in first-out order, the copy engine runs copy-in 1, then waits for kernel 1 before copy-out 1, and only then starts copy-in 2. So there is no overlap. When all copies-in are issued first, the copy engine is busy for 8 ms in total ($4$ in and $4$ out), and that is the time.

**The best number of chunks.** Now let $\lambda = 0.1$ ms per operation. Then $T(1) = 12.3$ ms, $T(4) = 6.6$ ms, $T(8) = 6$ ms, $T(9) = 539/90 \approx 5.99$ ms and $T(10) = 6$ ms. The best choice is $m = 9$, close to $\sqrt{8/0.1} \approx 8.9$. More chunks than this add more fixed cost than they save.

**Harris's measurements.** Harris (2012) ran a job in four streams with the two issue orders: per chunk ("version 1") and per kind of operation ("version 2"). The times in ms were as follows. They hold only for those GPUs and that code.

| GPU | serial | version 1 | version 2 |
|---|---|---|---|
| Tesla C1060 (compute capability 1.3, one copy engine) | 12.9 | 13.6 | 8.8 |
| Tesla C2050 (compute capability 2.0, two copy engines) | 10.0 | 5.7 | 7.6 |
| Tesla K20c (compute capability 3.5, Hyper-Q) | 7.1 | 4.0 | 4.0 |

The C1060 shows the one-engine effect of the first example. On the C2050, version 2 was slower for a reason the simple model does not have: Harris explains that when several kernels run at the same time, the signal that a kernel is complete is delayed until all of them finish, so the copies-out cannot overlap the kernels. On the K20c, the issue order no longer matters.

The CUDA C++ code below shows the chunked pipeline and an order between two streams by an event. The tests do not run this CUDA code. They run the Python model of engines and queues, and they check the numbers above exactly with fractions.

```cuda
// h_in, h_out: page-locked host buffers (cudaMallocHost); d_in, d_out: device buffers.
const int S = 4;
cudaStream_t st[S];
for (int i = 0; i < S; ++i) cudaStreamCreateWithFlags(&st[i], cudaStreamNonBlocking);
int chunk = n / S;                                    // assume S divides n
for (int i = 0; i < S; ++i) {                         // each chunk: in, kernel, out
    int off = i * chunk;
    cudaMemcpyAsync(d_in + off, h_in + off, chunk * sizeof(float), cudaMemcpyHostToDevice, st[i]);
    work<<<(chunk + 255) / 256, 256, 0, st[i]>>>(d_in + off, d_out + off, chunk);
    cudaMemcpyAsync(h_out + off, d_out + off, chunk * sizeof(float), cudaMemcpyDeviceToHost, st[i]);
}

// An order between streams without a host stop: st[1] waits for the work in st[0].
cudaEvent_t ready;
cudaEventCreateWithFlags(&ready, cudaEventDisableTiming);
produce<<<g, b, 0, st[0]>>>(buf);
cudaEventRecord(ready, st[0]);
cudaStreamWaitEvent(st[1], ready, 0);
consume<<<g, b, 0, st[1]>>>(buf);                     // starts after produce is done

for (int i = 0; i < S; ++i) cudaStreamSynchronize(st[i]);
for (int i = 0; i < S; ++i) cudaStreamDestroy(st[i]);
```

## Where it is used

- **Copy and compute pipelines.** Large inputs that come from the host, such as video frames, batches of a dataset or tiles of an out-of-core matrix, go through a chunked pipeline so that the copies hide behind the kernels.
- **Many small independent kernels.** Batched small problems, or independent branches of a computation graph, run in separate streams so that they can share the GPU.
- **Libraries.** Most GPU libraries take a stream argument, so that the caller can order library work with its own work without a global synchronization.
- **Multi-threaded hosts.** Servers with one host thread per request use per-thread default streams or explicit streams, so that the requests do not block each other.
- **Priorities.** A latency-sensitive task runs in a high-priority stream next to a long background task.
- **Graph capture.** A fixed sequence of work in several streams, joined by events, is captured as a graph to cut [launch overhead](/kernel-launch-overhead/).

## References
