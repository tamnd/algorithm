---
tag: WF3821
kind: problem
slug: stencil-computation
name: Stencil computation
aliases:
- stencil operation
- stencil sweep
- structured grid update
area: parallel/gpu-algorithms
level: core
summary: Update every point of a regular grid from a fixed pattern of its neighbours, sweep after sweep; on a GPU the main cost is memory traffic, which tiling with halo cells and temporal blocking reduce.
prereqs: [finite-differences, simt-model, shared-memory-tiling]
see_also: [jacobi-method, heat-equation, finite-difference-method, gauss-seidel-method, wavefront-parallelism, roofline-model, arithmetic-intensity, memory-coalescing]
sources:
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition, Morgan Kaufmann, 2022
    locator: Chapter 8, Stencil (Section 8.3 shared memory tiling for stencil sweep, Section 8.4 thread coarsening, Section 8.5 register tiling)
  - paper: doi:10.1145/1513895.1513905
    title: Paulius Micikevicius, 3D finite difference computation on GPUs using CUDA, GPGPU-2, 2009, 79 to 84
    locator: the 2D tile with halo in shared memory and the streaming of the third dimension through registers
  - paper: doi:10.1109/SC.2010.2
    title: Anthony Nguyen, Nadathur Satish, Jatin Chhugani, Changkyu Kim and Pradeep Dubey, 3.5-D blocking optimization for stencil computations on modern CPUs and GPUs, SC 2010
    locator: the 2.5D spatial blocking combined with temporal blocking
  - paper: "Matteo Frigo and Volker Strumpen, Cache oblivious stencil computations, International Conference on Supercomputing (ICS), 2005"
    locator: the space-time trapezoid decomposition (DOI and pages to be checked)
  - url: https://docs.nvidia.com/cuda/cuda-programming-guide/
    title: NVIDIA, CUDA Programming Guide, version 13.5
    locator: Section 2.1.9, Variable Specifiers (the __shared__ arrays that hold the tile)
---

A stencil computation updates every point of a regular grid by the same rule, which reads the values at a fixed pattern of nearby points, called the stencil, and it usually repeats this sweep many times. Jacobi iterations, explicit time steps of the [heat equation](/heat-equation/), and image filters are stencil computations. Each output needs only a few operations but several inputs, so on a GPU the time is set by memory traffic. The standard methods load a tile with a border of halo cells into shared memory once, and do several sweeps per load with temporal blocking.

## In plain words

Think of a big sheet of graph paper with a number in each square. In one round, each square gets a new number made from its old number and the numbers of its close neighbours, for example the average of the four squares around it. All squares are updated at the same time from the old sheet, so the order does not matter, and the round is easy to do in parallel. The hard part is reading: every square is read by its neighbours too. If each worker fetches all its neighbours from far memory, every number is fetched about five times. Instead, a team copies a square patch plus a thin border into fast memory, and then works from there.

## Definition

The grid is a $d$-dimensional array $u$ of $N_1 \times \cdots \times N_d$ points. A **stencil** is a finite set $S$ of offsets in $\mathbb{Z}^d$ that contains $0$, and its **radius** $r$ is the largest coordinate of an offset in absolute value. A sweep computes, for every interior point $x$,
$$u^{(t+1)}(x) = f\big(u^{(t)}(x + o) : o \in S\big),$$
where the points within distance $r$ of the border follow a boundary condition. In this page the border points keep their values (a fixed or Dirichlet boundary). The problem is to compute $u^{(s)}$ from $u^{(0)}$ for a given number of sweeps $s$.

- A **star** stencil of radius $r$ has the offsets along the axes only: $2dr + 1$ points, so 5 points for $d = 2, r = 1$ and 7 points for $d = 3, r = 1$.
- A **box** stencil has all offsets with every coordinate at most $r$: $(2r+1)^d$ points, 9 for $d = 2, r = 1$.
- In the **Jacobi** form each sweep reads only $u^{(t)}$ and writes a new array. The 5-point Jacobi update for the Laplace equation is $u^{(t+1)}_{i,j} = \frac14 (u^{(t)}_{i-1,j} + u^{(t)}_{i+1,j} + u^{(t)}_{i,j-1} + u^{(t)}_{i,j+1})$.

The page uses this notation, in the [SIMT model](/simt-model/) with warps of 32 and the [roofline model](/roofline-model/).

| symbol | meaning |
|---|---|
| $n$ | the number of grid points, $N_1 \cdots N_d$ |
| $r$, $\lvert S \rvert$ | the radius and the number of points of the stencil |
| $T$ | the side of the output tile of one thread block |
| $s$ | the number of sweeps (time steps) |
| $p$ | the number of processors |
| $W$, $S_\infty$, $T_p$ | the work, the span and the time on $p$ processors |
| $M$, $B$ | the size of the fast memory (shared memory) and the transaction size |

## Variants

- **Jacobi against Gauss-Seidel.** A [Gauss-Seidel](/gauss-seidel-method/) sweep updates the grid in place and reads new values of earlier points, so the points of one sweep depend on each other. Its parallel forms use a red-black ordering or [wavefront parallelism](/wavefront-parallelism/). The Jacobi form has no dependencies inside a sweep.
- **Constant or variable coefficients.** With variable coefficients each point also reads its own weights, which adds memory traffic per point.
- **Order and radius.** Higher-order [finite differences](/finite-differences/) use larger $r$, for example $r = 4$ for the eighth-order stencils of seismic codes.
- **Several fields.** Systems of equations update several arrays per point, as in fluid dynamics and lattice Boltzmann methods.
- **Boundaries.** Fixed, periodic or reflecting boundaries change only the border points, but they add branches or extra halo exchanges.

## Examples

**Three Jacobi sweeps.** On a $6 \times 6$ grid that is 0 everywhere except a top row of ones, the 5-point Jacobi update gives $u_{1,1} = 1/4$ after one sweep, $5/16$ after two, and $23/64$ after three. For instance, after two sweeps $u_{1,2} = 3/8$ and $u_{2,1} = 1/16$, so the third sweep gives $u_{1,1} = \frac14 (1 + \frac{1}{16} + 0 + \frac38) = \frac{23}{64}$. The tests compute this with exact fractions, both with the direct loop and with tiles.

**Loads per output for one tile.** Let a thread block compute a $T \times T$ tile of a 2D stencil of radius $r$. The inputs it needs are the tile and a halo of width $r$ around it.

- With a **box halo** the block loads the full $(T + 2r) \times (T + 2r)$ square, so the loads per output are
$$\frac{(T + 2r)^2}{T^2} = \left(1 + \frac{2r}{T}\right)^2.$$
- A **star** stencil does not read the corners of the halo, so the block needs only the tile and four strips of $r \times T$ cells: $T^2 + 4rT$ loads, or $1 + 4r/T$ per output.
- Without any reuse, each output loads its $\lvert S \rvert = 4r + 1$ inputs from global memory.

For the 5-point stencil with $T = 16$: no reuse gives 5 loads per output, the box halo $324/256 = 81/64 \approx 1.27$, and the star halo $320/256 = 5/4$. In 3D with a 7-point stencil and $T = 8$, the star halo needs $T^3 + 6rT^2 = 512 + 384$ loads, that is $7/4$ per output, and the box $10^3/512 \approx 1.95$. The large ratio in 3D is why Micikevicius (2009) keeps only a 2D tile in shared memory and streams the third dimension through registers. The simulator counts the loads of each tile and checks these formulas.

**Temporal blocking.** If the block loads a halo of width $rs$ and does $s$ sweeps in shared memory before it writes, the loads per output per sweep become
$$\frac{(T + 2rs)^2}{s T^2}.$$
For $T = 16$ and $r = 1$ this is $81/64 \approx 1.27$ for $s = 1$, $400/512 \approx 0.78$ for $s = 2$, and $576/1024 \approx 0.56$ for $s = 4$. The price is redundant work: in sweep $k$ the block also updates the part of the halo that is still valid, which neighbouring blocks update too, and it needs shared memory for the larger tile. The simulator checks that $s$ overlapped sweeps give the same grid as $s$ separate sweeps.

The CUDA C++ kernel below does one 5-point Jacobi sweep with a $T \times T$ tile and a star halo of width 1 in shared memory. The grid has `h` rows and `w` columns, the border is fixed, and the kernel is launched with blocks of $T \times T$ threads over the $(h-2) \times (w-2)$ interior. The tests do not run this CUDA code; they run the Python simulator.

```cuda
#define T 16
__global__ void jacobi5(const float* u, float* v, int h, int w) {
    __shared__ float s[T + 2][T + 2];
    int i = blockIdx.y * T + threadIdx.y + 1;      // interior rows 1 .. h-2
    int j = blockIdx.x * T + threadIdx.x + 1;      // interior columns 1 .. w-2
    int li = threadIdx.y + 1, lj = threadIdx.x + 1;
    bool inside = (i < h - 1) && (j < w - 1);
    if (inside) {
        s[li][lj] = u[i * w + j];
        if (threadIdx.y == 0)                   s[0][lj]      = u[(i - 1) * w + j];
        if (threadIdx.y == T - 1 || i == h - 2) s[li + 1][lj] = u[(i + 1) * w + j];
        if (threadIdx.x == 0)                   s[li][0]      = u[i * w + j - 1];
        if (threadIdx.x == T - 1 || j == w - 2) s[li][lj + 1] = u[i * w + j + 1];
    }
    __syncthreads();                               // the tile and halo are loaded
    if (inside)
        v[i * w + j] = 0.25f * (s[li - 1][lj] + s[li + 1][lj] +
                                s[li][lj - 1] + s[li][lj + 1]);
}
```

The rows of the tile are contiguous in global memory, so the loads of a warp are [coalesced](/memory-coalescing/); the left and right halo columns are single words per row and are not. The host swaps `u` and `v` between sweeps.

## Known algorithms

- **Direct loop.** One thread per output reads its $\lvert S \rvert$ inputs from global memory. The L1 and L2 caches catch part of the reuse, so it is a fair baseline on recent GPUs, but its traffic depends on the cache.
- **Shared memory tiling with halo cells.** Each block loads its tile and halo once, as in the kernel above and in Chapter 8 of Hwu, Kirk and El Hajj. See [shared memory tiling](/shared-memory-tiling/). Larger $T$ cuts the halo overhead but needs more shared memory and threads per block, which lowers [occupancy](/occupancy/).
- **Thread coarsening and register tiling.** Each thread computes several outputs along one axis and keeps the values it reuses in registers. In 3D, the 2.5D method of Micikevicius (2009) moves a 2D tile through the third dimension and keeps the planes above and below in registers, so shared memory holds only one plane.
- **Temporal blocking.** Overlapped (ghost zone) tiling, as in the example, recomputes the halo. Trapezoid, diamond and wavefront tilings avoid the recomputation by ordering the tiles in space-time. Nguyen et al. (2010) combine 2.5D spatial blocking with temporal blocking in their 3.5D blocking, on CPUs and GPUs. The cache-oblivious method of Frigo and Strumpen (2005) cuts space-time into trapezoids recursively.
- **Autotuning and code generators.** The best tile shape depends on the GPU, the radius and the precision, so stencil compilers and DSLs search over the tile sizes.

## Bounds

The bounds below are derived on this page in the cost model above.

- **Work and span.** A sweep does $W = \Theta(\lvert S \rvert \, n)$ operations. In the Jacobi form all outputs of a sweep are independent, so a sweep has span $O(1)$ (or $O(\log \lvert S \rvert)$ if the sum of the stencil is a tree), and $s$ sweeps have span $\Theta(s)$. A Gauss-Seidel sweep in lexicographic order has a longer span: $\Theta(N_1 + \cdots + N_d)$ with wavefronts.
- **Traffic of one sweep.** Without reuse across sweeps, every point must be read and written at least once per sweep, so the traffic is at least $2n$ words. Tiling reaches $(1 + 4r/T)\,n$ reads plus $n$ writes for a 2D star stencil. For the 5-point Jacobi update in single precision, at most about 5 floating-point operations per 8 bytes moved gives an [arithmetic intensity](/arithmetic-intensity/) of at most about $0.6$ FLOP per byte. This is below the ridge point of current GPUs, so the sweep is bound by memory bandwidth. The ridge point depends on the GPU and changes between generations.
- **Temporal blocking.** With $s$ sweeps per load, the reads per output per sweep fall to $(T + 2rs)^2 / (sT^2)$, which for fixed $T$ is smallest for $s$ near $T/(2r)$. The redundant updates grow with $s$, and the halo of width $rs$ must fit in shared memory with the tile.

## Reductions

- **To sparse matrix-vector multiplication.** A linear stencil sweep with constant coefficients is $u^{(t+1)} = A u^{(t)}$ for a banded matrix $A$ with $\lvert S \rvert$ nonzero diagonals. It can be run as a [sparse matrix-vector product](/sparse-matrix-vector-multiplication/), for example in the [ELLPACK](/ellpack-format/) or DIA format, but the matrix-free stencil kernel avoids reading $A$ at all and is faster.
- **From Gauss-Seidel to wavefronts.** An in-place sweep whose new value at $(i, j)$ uses the new values at $(i-1, j)$ and $(i, j-1)$ has the dependency pattern of [wavefront parallelism](/wavefront-parallelism/).

## Applications

- Iterative solvers: the [Jacobi method](/jacobi-method/) and the smoothers of multigrid for the Poisson and Laplace equations.
- Explicit time stepping of partial differential equations by the [finite difference method](/finite-difference-method/): heat and diffusion, wave propagation in seismic imaging, and weather and climate models.
- Image processing: blurs, edge filters and other convolutions with small kernels.
- Cellular automata such as the Game of Life, and lattice Boltzmann methods in fluid dynamics.

## References
