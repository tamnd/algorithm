---
tag: "271465"
kind: concept
slug: dynamic-parallelism
name: Dynamic parallelism
aliases:
- CUDA dynamic parallelism
- nested kernel launch
- CDP
- device-side kernel launch
area: parallel/gpu-algorithms
level: advanced
summary: CUDA dynamic parallelism lets a running kernel launch child kernels on the GPU for recursive and adaptive work; under CDP2 (CUDA 12) a parent cannot call cudaDeviceSynchronize.
prereqs: [cuda-programming-model, cuda-streams, kernel-launch-overhead]
see_also: [kernel-launch-overhead, persistent-threads, cuda-streams, parallel-quicksort, quadtree, work-stealing, fork-join-model, occupancy]
sources:
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 4.21.1.1 (overview, and the note that CDP2 is the default from CUDA 12.0, the only version on compute capability 9.0 and higher, and that CDP1 can be forced below 9.0 with -DCUDA_FORCE_CDP1_IF_SUPPORTED and is slated for removal), 4.21.2.1 (parent and child grids), 4.21.2.4 (ordering and concurrency), 4.21.3.3 and 4.21.3.4 (shared and local memory pointers may not go to a child), 4.21.4.2.1.1 (device launches are asynchronous), 4.21.4.2.3 (no explicit synchronization of child work), 4.21.5.1.1 (overhead of kernels linked with the device runtime), 4.21.5.2.1.2 (pending launch pool) and 4.21.5.3 (compile error if device code references cudaDeviceSynchronize); Section 5.7.4.2.1 (2048 launch slots by default, event slots twice the limit) and 5.7.4.8.1 to 5.7.4.8.3 (NULL, fire-and-forget and tail launch streams)
  - url: https://docs.nvidia.com/cuda/archive/12.0.0/cuda-c-programming-guide/index.html
    title: NVIDIA, CUDA C++ Programming Guide, version 12.0
    locator: Section 9.5.1 (differences between CDP1 and CDP2, no explicit device-side synchronization, cudaLimitDevRuntimeSyncDepth gives cudaErrorUnsupportedLimit, no virtualized pool for pending launches, streams tracked per grid) and Section 9.6.3.3.1.2 (CDP1 nesting depth limited to 24; device-side cudaDeviceSynchronize deprecated in CUDA 11.6 and removed for compute_90 and later)
  - url: https://developer.nvidia.com/blog/introduction-cuda-dynamic-parallelism/
    title: Andy Adinets, Adaptive parallel computation with CUDA dynamic parallelism, NVIDIA Technical Blog, 6 May 2014
    locator: the Mandelbrot set with the Mariani-Silver algorithm, one thread block per region and child launches for subdivided regions, measured on a Kepler K20X
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition, Morgan Kaufmann, 2022
    locator: Chapter 21, CUDA dynamic parallelism (Bezier curves, a recursive quadtree, and important considerations)
---

Dynamic parallelism is the ability of a GPU kernel to launch other kernels from the device, without a return to the host. In CUDA it is called CUDA Dynamic Parallelism (CDP). A thread of a running parent grid launches a child grid with the usual `<<<...>>>` syntax. Then the amount and shape of the parallel work can depend on data that only the GPU has, such as the size of a partition in quicksort or the detail of a region in an adaptive grid. The parent grid is not complete until all its children are complete. CUDA 12.0 made a new version, CDP2, the default. In CDP2 a parent thread cannot wait for its children with `cudaDeviceSynchronize`: device code that calls it does not compile. Work that must run after the children goes into a tail launch instead.

## In plain words

A head chef gets an order for a banquet. Without dynamic parallelism, every new task must go back to the manager in the office (the CPU), who then hands it to the kitchen. With dynamic parallelism, the chef can call helpers directly: "you two, do the sauces", and each helper can call more helpers for a big task. The kitchen decides how much help it needs while it works. But each call for help costs some time, the number of calls that can wait at once is limited, and in the newer rules a chef cannot stand and wait for the helpers to finish. The chef leaves a note: "when all of you are done, start the dessert".

## The idea

The model of the GPU is the [SIMT model](/simt-model/) with warps of 32 threads and the [roofline model](/roofline-model/). On top of it, a program is a tree of grids. Each device launch adds a fixed cost, in the same way as in [kernel launch overhead](/kernel-launch-overhead/), but paid on the GPU.

| symbol | meaning |
|---|---|
| $n$ | the size of the input |
| $p$ | the number of processors |
| $W$, $S$, $T_p$ | the work, the span and the time on $p$ processors |
| $M$, $B$ | the fast memory size and the memory transaction size |
| $\ell$ | the number of device launches |
| $d$ | the depth of nesting (the host launch is level 0) |
| $o_d$ | the cost of one device launch, which depends on the GPU and the driver |
| $P$ | the size of the pending launch pool |

**Parent and child.** A thread that launches a grid belongs to the parent grid, and the new grid is a child. The guide says that the invocation and completion of child grids "is properly nested": the parent grid is not complete until all of its children have completed (CUDA Programming Guide 13.5, Section 4.21.2.1). A device launch is asynchronous, like a host launch. The child may start at any time after the launch, but it is not guaranteed to start until the parent thread reaches an implicit synchronization point (Sections 4.21.2.4 and 4.21.4.2.1.1). So a parent must never wait in a loop for a child to make progress.

**Streams on the device.** Device launches follow stream order. The implicit NULL stream is shared by the threads of one block. Named streams created on the device must be non-blocking. CDP2 adds two named streams (Sections 5.7.4.8.1 to 5.7.4.8.3):

- `cudaStreamFireAndForget`: the launch is scheduled at once and nothing in the parent waits for it, except the end of the parent grid.
- `cudaStreamTailLaunch`: the grid starts only after the parent grid and all the work it launched are complete. The guide says that a tail launch should give the same effect as `cudaDeviceSynchronize` in most cases.

**Memory.** Global memory is shared by parent and child. Shared memory and local memory are private to a block or a thread, so a pointer to them must not be passed to a child (Sections 4.21.3.3 and 4.21.3.4). Writes that the parent makes before the launch are visible to the child. Because a parent thread cannot wait for its children, it has no safe way to read their results; the work that needs them goes into a tail launch (Section 4.21.4.2.3).

**The CUDA 12 change.** From CUDA 12.0, the default is CDP2, and it is the only version on devices of compute capability 9.0 and higher (13.5 guide, Section 4.21.1.1). The CUDA 12.0 guide lists the differences from the older CDP1 (Section 9.5.1):

- explicit device-side synchronization is no longer possible, so implicit synchronization such as tail launches must be used;
- querying or setting `cudaLimitDevRuntimeSyncDepth` gives `cudaErrorUnsupportedLimit`;
- there is no longer a virtualized pool for pending launches that do not fit in the fixed pool, so `cudaLimitDevRuntimePendingLaunchCount` must be set large enough;
- the number of events at once is limited to twice the pending launch count;
- streams are tracked per grid, not per thread block;
- the tail launch and fire-and-forget streams are new, and CDP2 needs 64-bit compilation.

With CDP2, device code that references `cudaDeviceSynchronize` gives a compile error (13.5 guide, Section 4.21.5.3). Device-side `cudaDeviceSynchronize` had been deprecated in CUDA 11.6 (12.0 guide, Section 9.6.3.3.1.2). A program can still opt in to CDP1 on devices below compute capability 9.0 with `-DCUDA_FORCE_CDP1_IF_SUPPORTED`, and the guide says that CDP1 is slated for removal.

**Limits.** The pending launch pool holds the launches that have not yet started. By default it has 2048 launch slots, and the event slots are twice that number. When the pool is full, a device launch fails with `cudaErrorLaunchOutOfResources` (13.5 guide, Section 5.7.4.2.1). The limit must be set from the host before the kernel runs. For CDP1, the CUDA 12.0 guide gives a maximum nesting depth of 24 (Section 9.6.3.3.1.2). These values belong to these guide versions and can change.

**Overheads.** There are three costs. Each device launch has a cost $o_d$, so a program with $\ell$ launches pays about $\ell\, o_d$ in total, spread over the GPU. A kernel that is linked with the device runtime can run slower even when it launches nothing, because of the runtime's tracking software (Section 4.21.5.1.1). And child grids that are small leave the GPU underused, because each child is a full grid with its own start and end. Dynamic parallelism pays when it removes a larger cost: a host round trip per level, or a large amount of work on parts of the data that do not need it.

The CUDA C++ code below is a quicksort in which each grid partitions its range and launches one child per side, and a CDP2 form of "launch children, then continue". The tests do not run this CUDA code. They run Python models that record the launches.

```cuda
// Compile with: nvcc -rdc=true ... -lcudadevrt
#define CUTOFF 32

__global__ void quicksort(int* a, int lo, int hi) {
    if (hi - lo <= CUTOFF) { small_sort(a, lo, hi); return; }   // done in this grid
    int p = partition(a, lo, hi);       // a[lo..p) <= a[p] <= a(p..hi)
    if (p - lo > 1)
        quicksort<<<1, 1, 0, cudaStreamFireAndForget>>>(a, lo, p);
    if (hi - (p + 1) > 1)
        quicksort<<<1, 1, 0, cudaStreamFireAndForget>>>(a, p + 1, hi);
}

// CDP1 style, which no longer compiles under CDP2:
//     child<<<g, b>>>(data);  cudaDeviceSynchronize();  use(data);
// CDP2 style: the tail launch runs after the parent grid and all its children.
__global__ void parent(float* data) {
    if (threadIdx.x == 0 && blockIdx.x == 0) {
        child<<<64, 256, 0, cudaStreamFireAndForget>>>(data);
        use_results<<<1, 256, 0, cudaStreamTailLaunch>>>(data);
    }
}

// Host side: make room for the launches that can be pending at once.
cudaDeviceSetLimit(cudaLimitDevRuntimePendingLaunchCount, 8192);
quicksort<<<1, 1>>>(d_a, 0, n);
cudaDeviceSynchronize();                 // on the host this is still allowed
```

## Examples

**Quicksort.** The Python model sorts 1000 random keys with a random pivot and a cutoff of 32. It makes 112 child launches, and the deepest launch is at level 10. With sorted input and the first item as the pivot, each level removes only one item: 200 sorted keys give 168 launches, one per level, with a depth of 168. That is far beyond the CDP1 nesting limit of 24, and each level is a grid of one thread, so the GPU is almost idle. A good pivot rule and a cutoff are necessary, and many fast GPU sorts use radix sort or merge sort instead.

**Adaptive refinement.** The Mariani-Silver method for the Mandelbrot set, as in Adinets (2014), computes the values on the border of a square region. If all border values are the same, it fills the region. Else it splits the region into children, each a child launch, until a minimum size or depth, and then computes every pixel. The Python model uses a test image of $128 \times 128$ pixels with values $\min(3, \lfloor (x^2 + y^2)/4096 \rfloor)$, a minimum region size of 4 and a split into $2 \times 2$. For this image the fill is exact, because the value grows in $x$ and in $y$, so the smallest and largest values of a square lie on its border.

| maximum depth | child launches | pixel evaluations |
|---|---|---|
| 0 (one flat grid) | 0 | 16 384 |
| 3 | 68 | 12 260 |
| 4 | 188 | 11 612 |
| 5 | 396 | 12 620 |

Depth 4 does the least work. Depth 5 does more work and more launches, because the regions of $4 \times 4$ pixels have 12 border pixels out of 16, so their border tests cost almost as much as the pixels. Whether depth 4 is faster than the flat grid depends on how $188\, o_d$ compares with the cost of $16\,384 - 11\,612 = 4772$ evaluations. For the real Mandelbrot set with a high maximum dwell, each evaluation is expensive, and Adinets reports speedups from 1.3 to almost 6 on a Kepler K20X.

## Where it is used

- **Adaptive grids and meshes.** Refinement where the data is complex, as in the Mandelbrot example and in adaptive mesh refinement for simulations. Recursion in the style of the [fork-join model](/fork-join-model/) maps to nested launches.
- **Recursive algorithms.** [Quicksort](/parallel-quicksort/), [quadtree](/quadtree/) and octree builds, and recursive subdivision of Bezier curves, as in Chapter 21 of Hwu, Kirk and El Hajj.
- **Irregular nested loops.** In graph algorithms, a vertex with a very large degree can launch a child grid for its edges, while small vertices are handled in the parent.
- **Libraries called from kernels.** A kernel can launch a library kernel on data it made, without a return to the host.
- **Alternatives.** The same problems can often be solved with a level-by-level loop on the host, with [persistent threads](/persistent-threads/) and a work queue, or with [work stealing](/work-stealing/). These avoid the device launch cost and the limits of the launch pool, at the price of more complex code.

## References
