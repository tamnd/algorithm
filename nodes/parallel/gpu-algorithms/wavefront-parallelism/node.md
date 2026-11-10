---
tag: PPA3V1
kind: technique
slug: wavefront-parallelism
name: Wavefront parallelism
aliases:
- anti-diagonal parallelism
- wavefront method
- hyperplane method
area: parallel/gpu-algorithms
level: core
summary: Run a 2D recurrence where cell (i, j) needs its upper, left and upper-left neighbours by anti-diagonals; the n + m − 1 diagonals run in order and the cells of each one run in parallel.
prereqs: [dag-dynamic-programming, simt-model, work-span-model]
see_also: [edit-distance, wagner-fischer-algorithm, smith-waterman, longest-common-subsequence, banded-smith-waterman, gauss-seidel-method, stencil-computation, critical-path]
sources:
  - url: https://lamport.azurewebsites.net/pubs/do-loops.pdf
    title: Leslie Lamport, The Parallel Execution of DO Loops, Communications of the ACM 17(2), 1974, 83 to 93
    locator: the hyperplane method, which runs all iterations on one hyperplane of the index space at the same time
  - paper: "Michael Wolfe, Loop skewing, the wavefront method revisited, International Journal of Parallel Programming 15(4), 1986, 279 to 293"
    locator: loop skewing as the compiler form of the wavefront method (pages to be checked)
  - paper: doi:10.1186/1756-0500-2-73
    title: Yongchao Liu, Douglas L. Maskell and Bertil Schmidt, CUDASW++, optimizing Smith-Waterman sequence database searches for CUDA-enabled graphics processing units, BMC Research Notes 2, 73, 2009
    locator: the inter-task parallelization (one thread per alignment) and the intra-task parallelization (one thread block per long alignment)
  - paper: doi:10.1145/321796.321811
    title: Robert A. Wagner and Michael J. Fischer, The string-to-string correction problem, Journal of the ACM 21(1), 1974, 168 to 173
    locator: the edit distance recurrence used as the running example
---

Wavefront parallelism is a technique for running a two-dimensional recurrence in parallel when each cell $(i, j)$ depends on the cells $(i-1, j)$, $(i, j-1)$ and $(i-1, j-1)$. All cells on one anti-diagonal $i + j = d$ are independent of each other, so the program processes the anti-diagonals one after another and the cells of each one in parallel. For an $n \times m$ table there are exactly $n + m - 1$ anti-diagonals, which is also the span. It is the standard way to run [edit distance](/edit-distance/), [Smith-Waterman](/smith-waterman/) and similar [dynamic programs](/dag-dynamic-programming/) on a GPU.

The name has nothing to do with the AMD "wavefront", which is AMD's word for a group of 64 (or 32) threads that run in lockstep, the counterpart of an NVIDIA warp.

## In plain words

Think of a grid of boxes where each box can be filled only after the box above it, the box to its left, and the box above-left are filled. The top-left box can go first. Then the two boxes next to it can go together. Then the three boxes on the next slanted line can go together, and so on. Each slanted line is a wave that moves from the top-left corner to the bottom-right corner. The waves must go in order, but all the boxes on one wave can be filled at the same time. The waves are short at the two corners and long in the middle, so at the start and at the end most workers have nothing to do.

## When it applies

Use it when:

- the computation is a table of cells, and each cell depends only on cells with a smaller $i$, a smaller $j$, or both; the three neighbours $(i-1, j)$, $(i, j-1)$ and $(i-1, j-1)$ are the common case;
- the cells on one anti-diagonal do the same kind of work, so that a warp can run them in lockstep;
- the table is large enough that the middle diagonals are much wider than the number of threads that work on them.

More generally, if every dependency goes from $(i', j')$ to $(i, j)$ with $a(i - i') + b(j - j') \ge 1$ for fixed positive integers $a, b$, the lines $ai + bj = c$ are independent sets. Lamport (1974) gave this hyperplane method for nested loops in any dimension.

## The template

This page counts in the work-span model for the proofs and in the [SIMT model](/simt-model/) for the GPU kernel: warps of 32 threads, a thread block that shares memory and meets at barriers.

| symbol | meaning |
|---|---|
| $n$, $m$ | the number of inner rows and columns of the table |
| $w_d$ | the number of cells on anti-diagonal $d$ |
| $p$ | the number of threads (processors) on the table |
| $W$, $S$, $T_p$ | the work, the span and the time on $p$ processors |
| $b$ | the side of a tile in the tiled form |
| $M$, $B$ | the fast memory size and the memory transaction size |

The inner cells are $(i, j)$ with $1 \le i \le n$ and $1 \le j \le m$. Row 0 and column 0 are given.

```pseudo id=main
WAVEFRONT(n, m, CELL)
L1   for d ← 2 to n + m do                         ▷ the anti-diagonals in order
L2     lo ← max(1, d − m); hi ← min(n, d − 1)
L3     for each i ∈ {lo, …, hi} in parallel do
         D[i, d − i] ← CELL(D[i − 1, d − i], D[i, d − i − 1], D[i − 1, d − i − 1])
L4     barrier                                     ▷ diagonal d is complete
```

**Correctness.** Each of the three inputs of cell $(i, j)$ has a coordinate sum of $i + j - 1$ or $i + j - 2$, so it lies on an earlier anti-diagonal or in row 0 or column 0. The loop of line L1 handles the diagonals in increasing order, and the barrier on line L4 makes every cell of a diagonal visible before the next diagonal starts. So every cell reads final values. The cells of one diagonal do not read each other, so they can run in any order or at the same time. In other words, the order by $i + j$ is a topological order of the dependency DAG.

**The number of diagonals.** The coordinate sum $d = i + j$ of an inner cell takes every integer value from $1 + 1 = 2$ to $n + m$, and no others. That is $n + m - 1$ values, so there are $n + m - 1$ anti-diagonals and $n + m - 1$ parallel rounds.

**The span.** With one time unit per cell, the span is exactly $n + m - 1$. It is at most that, because the rounds above take one unit each. It is at least that, because the cells $(1,1), (1,2), \ldots, (1,m), (2,m), \ldots, (n,m)$ form a chain of $n + m - 1$ cells in which each depends on the one before, and no schedule can run a chain faster than its length.

**The work on each diagonal.** On diagonal $d$ the row index runs from $\max(1, d - m)$ to $\min(n, d - 1)$, so
$$w_d = \min(n, d - 1) - \max(1, d - m) + 1 = \min(d - 1,\ n,\ m,\ n + m + 1 - d).$$
The widths rise by one from 1 to $\min(n, m)$, stay there, and fall by one back to 1. They add up to $W = \sum_d w_d = nm$, the same work as the row-by-row program. For $n = 3$ and $m = 5$ the widths are $1, 2, 3, 3, 3, 2, 1$.

**Time on $p$ threads.** With a barrier per diagonal, round $d$ takes $\lceil w_d / p \rceil$ steps, so
$$T_p = \sum_{d=2}^{n+m} \left\lceil \frac{w_d}{p} \right\rceil \le \frac{nm}{p} + n + m - 1,$$
the bound of [Brent's theorem](/brent-theorem/). The average parallelism is $W/S = nm/(n + m - 1)$, which is about $n/2$ for a square table. For $n = m = 32$ and $p = 32$ threads, there are 63 rounds of 32 thread slots for 1024 cells, so only $1024/2016 \approx 51$ percent of the slots do useful work.

**On a GPU.** A diagonal of the table is not contiguous in a row-major array: its cells are $m$ words apart. Kernels therefore keep only the last two diagonals, stored by row index, in shared memory or registers, so that the threads of a warp touch consecutive words. The kernel below computes the edit distance of two strings with one thread block. It assumes $n, m \le$ `MAXN` and rotates three diagonal buffers in shared memory. The tests do not run this CUDA code; they run a Python simulator with the same buffers and barriers.

```cuda
#define MAXN 1024
// Diagonal d is stored by row index i: buffer[i] holds cell (i, d - i).
__global__ void edit_distance_wavefront(const char* a, int n, const char* b, int m,
                                        int* result) {
    __shared__ int buf[3][MAXN + 1];
    int* d2 = buf[0];          // diagonal d - 2
    int* d1 = buf[1];          // diagonal d - 1
    int* cur = buf[2];         // diagonal d
    if (threadIdx.x == 0) { d2[0] = 0; d1[0] = 1; d1[1] = 1; }
    __syncthreads();
    for (int d = 2; d <= n + m; ++d) {                         // L1
        int lo = max(1, d - m), hi = min(n, d - 1);           // L2
        if (threadIdx.x == 0) {                                // row 0 and column 0
            if (d <= m) cur[0] = d;
            if (d <= n) cur[d] = d;
        }
        for (int i = lo + threadIdx.x; i <= hi; i += blockDim.x) {   // L3
            int j = d - i;
            int sub = d2[i - 1] + (a[i - 1] != b[j - 1]);
            cur[i] = min(min(d1[i - 1], d1[i]) + 1, sub);
        }
        __syncthreads();                                       // L4
        int* t = d2; d2 = d1; d1 = cur; cur = t;               // each thread rotates
    }
    if (threadIdx.x == 0) *result = (n + m == 0) ? 0 : d1[n];
}
```

One barrier per diagonal is enough: the buffer that round $d + 1$ overwrites held diagonal $d - 2$, and every read of it in round $d$ happens before the barrier of round $d$.

## Classic examples

- **Edit distance.** The [Wagner-Fischer](/wagner-fischer-algorithm/) table has $D[i, j] = \min(D[i-1, j] + 1, D[i, j-1] + 1, D[i-1, j-1] + [a_i \ne b_j])$. For "kitten" and "sitting" the 42 inner cells lie on 12 diagonals of widths $1, 2, 3, 4, 5, 6, 6, 5, 4, 3, 2, 1$, and the distance is 3. For $a = $ GAT and $b = $ GCAT the table below gives each inner cell with its round number $i + j - 1$ in brackets; the distance is 1.

| | | G | C | A | T |
|---|---|---|---|---|---|
| | 0 | 1 | 2 | 3 | 4 |
| G | 1 | 0 [1] | 1 [2] | 2 [3] | 3 [4] |
| A | 2 | 1 [2] | 1 [3] | 1 [4] | 2 [5] |
| T | 3 | 2 [3] | 2 [4] | 2 [5] | 1 [6] |

- **Longest common subsequence.** The [LCS table](/lcs-dynamic-programming/) has the same three dependencies, so the same template applies with a different cell rule. See [longest common subsequence](/longest-common-subsequence/).
- **Smith-Waterman local alignment.** The [Smith-Waterman](/smith-waterman/) recurrence adds a floor of 0 and takes the largest cell as the score; with affine gaps it keeps three tables with the same dependencies. GPU programs such as CUDASW++ (Liu, Maskell and Schmidt 2009) use two forms: for database search, one thread aligns the query against one database sequence, which gives parallelism across many alignments; for long sequences, a thread block works on one alignment and moves through its table along diagonals. The [banded](/banded-smith-waterman/) variant restricts the wave to a band around the main diagonal, so each diagonal has at most the band width cells.
- **Gauss-Seidel sweeps.** An in-place [Gauss-Seidel](/gauss-seidel-method/) sweep of a 5-point [stencil](/stencil-computation/) in row-major order reads new values at $(i-1, j)$ and $(i, j-1)$, so its points can be updated by anti-diagonals. The red-black ordering is the usual alternative.
- **Triangular solves and other loop nests.** Loop skewing in compilers (Wolfe 1986) turns any loop nest with such dependencies into an outer serial loop over wavefronts and inner parallel loops.

## Variations

- **Tiled wavefront.** Cut the table into $b \times b$ tiles. A tile depends on the tiles above, to the left and above-left, so the tiles themselves form a wavefront with $\lceil n/b \rceil + \lceil m/b \rceil - 1$ rounds. Each thread block computes a tile, often with a wavefront inside the tile, and passes its last row and column to the neighbouring tiles. This trades a longer span for less synchronization and more reuse in shared memory.
- **One kernel launch per diagonal.** The simplest multi-block form launches one kernel per diagonal. It pays the [kernel launch overhead](/kernel-launch-overhead/) $n + m - 1$ times, which dominates for thin diagonals.
- **Many independent tables.** When there are many small problems, as in database search, give each thread or warp its own table and run them row by row. There is no wavefront at all, and all threads are busy.
- **Higher dimensions.** A recurrence on a 3D table with dependencies on smaller coordinates runs by the planes $i + j + k = d$, with $n_1 + n_2 + n_3 - 2$ rounds.
- **Bit-parallel forms.** For edit distance with small alphabets, bit-vector methods such as Myers' algorithm compute a whole column with word operations and can replace the wavefront.

## Pitfalls

- **Low utilization at the corners.** The first and the last $\min(n, m) - 1$ diagonals are short. For a square table half of the thread slots are idle, as computed above. Give each block many tables, or overlap independent tables.
- **Row-major storage of the full table.** The cells of a diagonal are $m$ words apart in a row-major array, which breaks [coalescing](/memory-coalescing/). Store diagonals, or tiles, contiguously.
- **A missing barrier, or one too few buffers.** With two buffers, round $d$ overwrites diagonal $d - 2$ while a slow thread may still read it. Use three buffers and one barrier per round, or two buffers with a second barrier between the reads of a round and its writes.
- **Off-by-one in the range.** The row range is $\max(1, d - m)$ to $\min(n, d - 1)$. Using $0$ or $d$ as the bounds writes row 0 or column 0.
- **Confusing the term.** In AMD documentation a wavefront is a hardware thread group, not this technique.

## Exercises

1. Prove that $w_d = \min(d - 1, n, m, n + m + 1 - d)$ for $2 \le d \le n + m$, and that $\sum_d w_d = nm$.
2. For a square table with $n = m$ and $p$ threads, compute $T_p$ exactly when $p$ divides $n$, and find the utilization $n^2 / (p T_p)$.
3. Show that the tiled wavefront with $b \times b$ tiles has $\lceil n/b \rceil + \lceil m/b \rceil - 1$ rounds, and write its span when each tile takes $2b - 1$ steps inside.
4. A recurrence has $D[i, j]$ depending on $D[i-1, j]$ and $D[i-2, j+1]$. Find positive integers $a, b$ such that the lines $ai + bj = c$ are independent, and count the rounds for an $n \times m$ table.
5. Change the CUDA kernel to compute the score of Smith-Waterman local alignment with a linear gap penalty, and say what extra reduction it needs at the end.

## References
