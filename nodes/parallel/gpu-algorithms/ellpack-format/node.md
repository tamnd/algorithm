---
tag: 6VRCR7
kind: data-structure
slug: ellpack-format
name: ELLPACK sparse format
aliases:
- ELL format
- ELLPACK-R
- ELLPACK/ITPACK format
area: parallel/gpu-algorithms
level: core
summary: A sparse matrix format that pads every row to the longest row length K and stores the M by K arrays column by column, so a GPU warp with one thread per row reads memory in coalesced loads.
implements: [sparse-matrix]
properties: {persistent: false, concurrent: false, external: false}
prereqs: [sparse-matrix, compressed-sparse-row, memory-coalescing]
see_also: [sparse-matrix-vector-multiplication, compressed-sparse-column, simt-model, warp-divergence, roofline-model, conjugate-gradient-method, jacobi-method, sparse-linear-systems]
sources:
  - paper: doi:10.1145/1654059.1654078
    title: Nathan Bell and Michael Garland, Implementing sparse matrix-vector multiplication on throughput-oriented processors, SC 2009, Article 18
    locator: Section 3.2 (ELL format), Section 3.4 (COO), Section 3.5 (hybrid format and the choice of K), Section 3.6 and Table 1 (bytes per FLOP of each format)
  - paper: "Nathan Bell and Michael Garland, Efficient Sparse Matrix-Vector Multiplication on CUDA, NVIDIA Technical Report NVR-2008-004, December 2008"
    locator: the ELL and HYB kernels
  - paper: doi:10.1002/cpe.1658
    title: Francisco Vázquez, José Jesús Fernández and Ester M. Garzón, A new approach for sparse matrix vector product on NVIDIA GPUs, Concurrency and Computation, Practice and Experience 23(8), 2011, 815 to 826
    locator: the ELLPACK-R format with its array of row lengths
  - paper: "Roger G. Grimes, David R. Kincaid and David M. Young, ITPACK 2.0 User's Guide, Report CNA-150, Center for Numerical Analysis, University of Texas at Austin, 1979"
    locator: the ELLPACK/ITPACK storage of a sparse matrix in two rectangular arrays
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 3.4, Storage schemes (the Ellpack-Itpack format)
  - book: isbn:9780323912310
    title: Wen-mei W. Hwu, David B. Kirk and Izzat El Hajj, Programming Massively Parallel Processors, fourth edition, Morgan Kaufmann, 2022
    locator: Chapter 14, Sparse matrix computation (the ELL format and the hybrid ELL-COO format)
---

The ELLPACK format, or ELL, stores a [sparse matrix](/sparse-matrix/) with $M$ rows and at most $K$ nonzeros per row in two dense $M \times K$ arrays: one for the values and one for the column indices, with shorter rows padded. On a GPU the arrays are stored column by column, so that in a [sparse matrix-vector product](/sparse-matrix-vector-multiplication/) with one thread per row, the 32 threads of a warp read 32 consecutive words at each step. Bell and Garland (2009) made it one of the standard GPU formats. Its weak point is the padding: one long row makes every row as long as it.

## In plain words

Write each row of the matrix as a short list of its nonzero numbers, together with the column of each one. Make all lists as long as the longest list, and fill the empty places with zeros. Now you have two neat tables of the same shape: one with the numbers and one with the columns. Store the tables so that the first entries of all rows come first, then the second entries of all rows, and so on. When many GPU threads each take one row and move along their rows together, at each step they all read neighbouring memory cells, which the GPU can fetch in one wide read. The cost is the filler: if one row is very long, every row must be padded to that length.

## The abstract type

ELL implements the static part of the [sparse matrix](/sparse-matrix/) type: BUILD from a list of entries, the product $y = Ax$, the lookup of an entry $A_{ij}$, and the scan of a row. It is meant for matrices whose rows have similar lengths, such as matrices from structured grids and [finite difference](/finite-difference-method/) stencils. It does not support cheap insertion: adding an entry to a row that already has $K$ entries forces a rebuild.

## Representation

Let $A$ have $M$ rows, $N$ columns, $r_i$ nonzeros in row $i$, and $\mathit{nnz} = \sum_i r_i$ nonzeros in all. Let $K = \max_i r_i$.

- $\mathit{data}[0 \ldots MK-1]$ holds the values. Slot $s$ of row $i$ is at position $sM + i$ (column-major order).
- $\mathit{indices}[0 \ldots MK-1]$ holds the column of each value at the same position.
- A padding slot holds the value 0 and a padding index, either a sentinel such as $-1$ or a valid column such as 0 or $i$.
- **ELLPACK-R** is a variant that adds $\mathit{rowlen}[0 \ldots M-1]$ with $\mathit{rowlen}[i] = r_i$, so a thread can stop at the end of its row and need not read the padding (Vázquez, Fernández and Garzón 2011).

Column-major order is the GPU choice. The original ELLPACK/ITPACK storage of Grimes, Kincaid and Young (1979) was written in Fortran, which stores two-dimensional arrays column by column too, and its target was vector machines.

## Operations

BUILD needs the row lengths first, to find $K$; with a CSR matrix as input they are the differences of the row pointers. The product runs one thread per row.

```pseudo id=main
ELL-BUILD(rows, M)                       ▷ rows[i] = list of (column, value)
L1   K ← max over i of |rows[i]|
L2   data[0 .. MK − 1] ← 0; indices[0 .. MK − 1] ← PAD
L3   for i ← 0 to M − 1 do
L4     for each s-th entry (c, v) of rows[i], s = 0, 1, … do
L5       data[s·M + i] ← v; indices[s·M + i] ← c

ELL-SPMV(data, indices, M, K, x)
L6   for each row i ∈ {0, …, M − 1} in parallel do   ▷ one thread per row
L7     acc ← 0; for s ← 0 to K − 1 do
L8       c ← indices[s·M + i]
L9       if c ≠ PAD then
L10        acc ← acc + data[s·M + i] · x[c]
L11    y[i] ← acc
```

GET$(i, j)$ scans the $K$ slots of row $i$, in $O(K)$ time, or in $O(\log K)$ with binary search if each row is sorted by column. Row iteration visits the $K$ slots of a row with a stride of $M$.

The CUDA C++ kernels below are the GPU form of ELL-SPMV, for plain ELL and for ELLPACK-R. They are written for this page; Bell and Garland give a kernel of the same shape. The tests do not run this CUDA code; they run the Python simulator described under Implementations.

```cuda
// Plain ELL: padding slots have index -1.
__global__ void spmv_ell(int M, int K, const int* indices, const float* data,
                         const float* x, float* y) {
    int row = blockIdx.x * blockDim.x + threadIdx.x;
    if (row < M) {
        float acc = 0.0f;
        for (int s = 0; s < K; ++s) {
            int col = indices[s * M + row];        // consecutive across the warp
            if (col >= 0) acc += data[s * M + row] * x[col];
        }
        y[row] = acc;
    }
}

// ELLPACK-R: each thread stops at the end of its own row.
__global__ void spmv_ellr(int M, const int* rowlen, const int* indices,
                          const float* data, const float* x, float* y) {
    int row = blockIdx.x * blockDim.x + threadIdx.x;
    if (row < M) {
        float acc = 0.0f;
        for (int s = 0; s < rowlen[row]; ++s)
            acc += data[s * M + row] * x[indices[s * M + row]];
        y[row] = acc;
    }
}
```

## Example

Take the $4 \times 4$ matrix

$$A = \begin{pmatrix} 1 & 7 & 0 & 0 \\ 0 & 2 & 8 & 0 \\ 5 & 0 & 3 & 9 \\ 0 & 6 & 0 & 4 \end{pmatrix}.$$

The row lengths are $(2, 2, 3, 2)$, so $K = 3$, $\mathit{nnz} = 9$, and there are $MK - \mathit{nnz} = 12 - 9 = 3$ padding slots. In column-major order, with $*$ for padding:

| position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| slot $s$, row $i$ | 0, 0 | 0, 1 | 0, 2 | 0, 3 | 1, 0 | 1, 1 | 1, 2 | 1, 3 | 2, 0 | 2, 1 | 2, 2 | 2, 3 |
| data | 1 | 2 | 5 | 6 | 7 | 8 | 3 | 4 | 0 | 0 | 9 | 0 |
| indices | 0 | 1 | 0 | 1 | 1 | 2 | 2 | 3 | * | * | 3 | * |

With $x = (1, 2, 3, 4)$, the four threads read positions 0 to 3 at $s = 0$, positions 4 to 7 at $s = 1$, and positions 8 to 11 at $s = 2$, where three of them find padding. The result is $y = (1 + 14,\ 4 + 24,\ 5 + 9 + 36,\ 12 + 16) = (15, 28, 50, 28)$.

**A matrix where ELL fails.** Take $M = 10^6$ rows with 5 nonzeros each, except one row with 1000. Then $\mathit{nnz} = 5\,000\,995$ and $K = 1000$, so ELL has $10^9$ slots, of which 99.5 percent are padding. With 4-byte values and indices, ELL needs 8 GB, CSR needs $8 \cdot \mathit{nnz} + 4(M + 1) = 44\,007\,964$ bytes, and HYB with $K = 5$ puts the 995 extra entries of the long row into COO, for $8 \cdot 5M + 12 \cdot 995 = 40\,011\,940$ bytes.

## Correctness

The proof is in the proofs file. The map $(s, i) \mapsto sM + i$ is a bijection from slot pairs to positions, so BUILD puts each nonzero of row $i$ into its own slot of row $i$, and every other slot holds padding. ELL-SPMV adds exactly the nonzeros of row $i$ times the matching entries of $x$, so $y = Ax$. If the padding index is a valid column instead of a sentinel, a padding slot adds $0 \cdot x_c$, which is 0 unless $x_c$ is infinite or NaN in floating point.

The same bijection gives the access pattern: at slot $s$, a warp of threads $w, \ldots, w+31$ reads the 32 consecutive words $sM + w, \ldots, sM + w + 31$ of each array. With 4-byte words and 32-byte sectors that is 4 sectors when $sM + w$ is a multiple of 8, and at most 5 in any case.

## Complexity

The page uses this notation. The cost model is the [SIMT model](/simt-model/) with warps of 32, where the time of SpMV is set by the bytes it moves (the [roofline model](/roofline-model/)).

| symbol | meaning |
|---|---|
| $M$, $N$ | the number of rows and columns |
| $n$ | the input size, here $\mathit{nnz}$ |
| $K$ | the width, the longest row length |
| $p$ | the number of threads, one per row |
| $W$, $S$, $T_p$ | the work, the span and the time on $p$ processors |
| $B$ | the memory sector size, 32 bytes in the counts below |

**Storage.** With 4-byte values and indices:

| format | words | bytes |
|---|---|---|
| ELL | $2MK$ | $8MK$ |
| ELLPACK-R | $2MK + M$ | $8MK + 4M$ |
| [CSR](/compressed-sparse-row/) | $2\,\mathit{nnz} + M + 1$ | $8\,\mathit{nnz} + 4(M+1)$ |
| COO | $3\,\mathit{nnz}$ | $12\,\mathit{nnz}$ |
| HYB of width $K_h$ | $2MK_h + 3e$ | $8MK_h + 12e$ |

Here $e = \sum_i \max(0, r_i - K_h)$ is the number of entries that do not fit in the ELL part. ELL is no larger than CSR exactly when $2MK \le 2\,\mathit{nnz} + M + 1$, that is, when the padding $MK - \mathit{nnz}$ is at most about $M/2$ slots.

**SpMV traffic.** Each slot loads one value and one index, so plain ELL reads $8MK$ bytes of matrix data whatever the padding. A padding slot with a sentinel skips the load of $x$, so there are $\mathit{nnz}$ gathers from $x$ and $M$ stores to $y$. In the best case $MK = \mathit{nnz}$, each nonzero moves 12 bytes (value, index and the $x$ entry, with no cache reuse) for 2 floating-point operations, which is 6 bytes per FLOP. This is the figure in Table 1 of Bell and Garland, and it puts SpMV far to the memory-bound side of the roofline on every GPU. ELLPACK-R lets each lane stop after $r_i$ slots, but a warp still runs for the longest row among its 32 lanes, so it saves bandwidth only when the lengths within each group of 32 rows differ.

**Coalescing.** For 64 rows of 8 entries each, the simulator counts $2 \cdot 8 \cdot 2 \cdot 4 = 128$ sectors for ELL (2 warps, 8 slots, 2 arrays, 4 sectors per load) and $2 \cdot 8 \cdot 2 \cdot 32 = 1024$ for CSR with one thread per row, whose lanes are 8 words apart and so hit 32 different sectors at each step.

**Work and span.** BUILD does $O(MK)$ work, plus $O(\mathit{nnz} \log K)$ if the rows must be sorted. SpMV does $W = \Theta(MK)$ work for plain ELL and has span $S = \Theta(K)$ with one thread per row, since the rows are independent. GET is $O(K)$.

## Variants

- **ELLPACK-R.** The array of row lengths lets each thread skip its padding (Vázquez, Fernández and Garzón 2011). It does not reduce storage.
- **HYB (ELL plus COO).** Bell and Garland store the first $K_h$ entries of each row in ELL and the rest in a coordinate (COO) list of (row, column, value) triples, which a separate kernel processes. They choose $K_h$ as the largest width such that at least $\max(4096, M/3)$ rows have $K_h$ or more entries, because in their tests ELL was about three times faster than COO when it was full. The tests implement this rule.
- **Sliced ELL.** Cut the rows into slices of a fixed number of rows, for example 32, and pad each slice only to its own longest row. With rows sorted by length inside a window, as in SELL-C-$\sigma$, the padding becomes small.
- **DIA.** For a matrix with a few full diagonals, the diagonal format stores each diagonal as one array and needs no index array; it is the special case of ELL where the column of slot $s$ in row $i$ is $i + \mathit{offset}_s$.
- **Row-major ELL.** Row-major storage suits a CPU that runs one row per core with SIMD across the slots. On a GPU with one thread per row it breaks coalescing.

## When to use it

Use ELL when the rows have nearly the same number of nonzeros and the matrix is multiplied by many vectors, as in [Jacobi](/jacobi-method/) or [conjugate gradient](/conjugate-gradient-method/) iterations for [sparse linear systems](/sparse-linear-systems/) on a GPU. Matrices from finite-difference and finite-element meshes are typical cases. Use HYB or sliced ELL when most rows are short but a few are long. Use [CSR](/compressed-sparse-row/) with a warp per row, or a merge-based CSR kernel, for matrices with power-law row lengths, and for matrices that change often.

## Pitfalls

- **One long row.** $K$ is the maximum, not the mean. Check $MK / \mathit{nnz}$ before you choose ELL; the example above has a ratio near 200.
- **Row-major layout on a GPU.** Storing slot $s$ of row $i$ at $iK + s$ makes the lanes of a warp $K$ words apart, which turns one 4-sector load into up to 32 sectors.
- **Padding index.** A valid column such as 0 is safe in exact arithmetic but gives NaN when $x_0$ is infinite or NaN. A sentinel needs a branch, which is cheap here because all lanes of a warp test the same slot.
- **Alignment.** If $M$ is not a multiple of the warp width, the loads of later slots start at unaligned addresses and touch 5 sectors instead of 4. Pad the leading dimension to a multiple of 32.
- **Integer overflow in $sM + i$.** For large $M K$ the product exceeds $2^{31}$; use 64-bit indices.
- **Expecting ELLPACK-R to save memory.** It saves reads of padding, not storage.

## Implementations

The Python file builds ELL, ELLPACK-R and HYB from rows or a dense matrix, and runs SpMV in a SIMT simulator with one thread per row in warps of 32. The simulator counts the 32-byte sectors of each warp load for 4-byte words, the active lane slots, the gathers from $x$ and the floating-point operations. The tests check SpMV against a dense product with exact integers on seeded random matrices, the padding count $MK - \mathit{nnz}$ and the storage formulas, the sector counts 128 and 1024 of the coalescing example, the bound of 5 sectors per warp load, and the HYB split and its rule for $K_h$.

## History

The format comes from the ELLPACK and ITPACK packages for elliptic problems and iterative solvers, developed at Purdue and the University of Texas around 1980; the ITPACK 2.0 guide of Grimes, Kincaid and Young (1979) describes it. It was used on vector machines, where a loop over the rows of one slot is a long vector operation. Bell and Garland (2008 report, 2009 paper) showed that the same property makes it coalesce on GPUs, and they introduced the HYB format in the CUSP library. Vázquez, Fernández and Garzón (2011) added the row-length array of ELLPACK-R, and sliced and sorted variants followed.

## References
