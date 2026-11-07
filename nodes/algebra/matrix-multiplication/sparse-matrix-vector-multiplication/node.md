---
tag: JJHJMQ
kind: problem
slug: sparse-matrix-vector-multiplication
name: Sparse matrix-vector multiplication
aliases:
- SpMV
- sparse matrix times vector
area: algebra/matrix-multiplication
level: core
summary: Compute y = Ax for a sparse m×n matrix A stored by its nonzeros; the compressed sparse row method takes Θ(m + nnz(A)) time, and in practice the speed is limited by memory bandwidth.
model: algebraic-computation-tree
complexity:
  vars: {m: the number of rows of A, z: the number of stored nonzero entries of A}
  time: {worst: Θ(m + z)}
prereqs: [matrix-vector-multiplication, sparse-matrix, compressed-sparse-row]
see_also: [sparse-matrix-multiplication, compressed-sparse-column, ellpack-format, conjugate-gradient-method, pagerank, roofline-model, reverse-cuthill-mckee, black-box-matrix]
sources:
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition
    locator: Chapter 3, Sparse Matrices, Section 3.4, Storage schemes, and Section 3.5, Basic sparse matrix operations (CSR, CSC, coordinate and diagonal formats, and the matrix-vector product)
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems
    locator: Chapter 2, Basic algorithms (compressed column storage and the function cs_gaxpy for y = Ax + y)
  - paper: "Michael A. Bender, Gerth Stølting Brodal, Rolf Fagerberg, Riko Jacob and Elias Vicari, Optimal sparse matrix dense vector multiplication in the I/O-model, 19th ACM Symposium on Parallelism in Algorithms and Architectures (SPAA 2007)"
    locator: the main theorems (matching upper and lower bounds on the number of I/Os for SpMV in the external memory model)
  - paper: "Samuel Williams, Leonid Oliker, Richard Vuduc, John Shalf, Katherine Yelick and James Demmel, Optimization of sparse matrix-vector multiplication on emerging multicore platforms, Proceedings of the ACM/IEEE Conference on Supercomputing (SC 2007)"
    locator: the performance results and the analysis of memory bandwidth as the limit of SpMV speed
---

Sparse matrix-vector multiplication (SpMV) computes $y = Ax$ when the $m \times n$ matrix $A$ is stored by its $z = \operatorname{nnz}(A)$ nonzero entries. In [compressed sparse row](/compressed-sparse-row/) form, each row is a short list of (column, value) pairs, and $y_i$ is the sum of the values times the matching entries of $x$; this takes $z$ multiplications and $\Theta(m + z)$ time, which is optimal since each nonzero must be read. It is the inner step of iterative solvers such as the [conjugate gradient method](/conjugate-gradient-method/) and of [PageRank](/pagerank/). On real machines its speed is bounded by memory bandwidth rather than by arithmetic, so the choice of storage format and the order of the rows matter more than the operation count.

## In plain words

A large table has mostly zeros. Store only the nonzero numbers, each with its column, row by row. To multiply the table by a list, go through each row's short list of nonzeros, multiply each by the list entry for its column, and add the products. The result has one sum for each row.

The work is the number of stored nonzeros plus the number of rows. A computer spends most of this time moving the stored numbers from memory, not doing the arithmetic, so the layout of the data decides the speed.

## Definition

Let $R$ be a ring or a semiring, $A \in R^{m \times n}$ and $x \in R^n$. The output is $y \in R^m$ with $y_i = \sum_{j : A[i][j] \ne 0} A[i][j] \, x_j$. When row $i$ has no stored entry, $y_i = 0$. The matrix is given in a sparse format. In CSR form it is three arrays: the values $v$, their column indices $c$, both of length $z$, and the row pointers $r$ of length $m + 1$, so that row $i$ holds the entries $r_i, \ldots, r_{i+1} - 1$. The direct method is

$$y_i = \sum_{t = r_i}^{r_{i+1} - 1} v_t \, x_{c_t}, \qquad 0 \le i < m.$$

The cost model counts ring operations and the index operations of a RAM. For the memory traffic, the external memory model with a fast memory of $M$ words and blocks of $B$ words is used.

## Variants

- **Transposed product.** $y = A^{\mathsf T} x$ from the CSR arrays scatters into $y$: for each stored $(i, j, v)$, add $v x_i$ to $y_j$. It has the same operation count; in parallel the scatter needs atomic additions or a CSC copy. See [compressed sparse column](/compressed-sparse-column/).
- **Symmetric matrices.** Store only the upper triangle and use each entry twice, which halves the memory traffic for the matrix.
- **Many vectors.** $Y = AX$ for a dense $n \times k$ block $X$ reads $A$ once for $k$ vectors and has a higher ratio of arithmetic to memory traffic.
- **Sparse vectors.** When $x$ is also sparse, as in a frontier of [breadth-first search](/breadth-first-search/), the cost can depend on the nonzeros of $x$ only, with a CSC matrix: $y = \sum_{j : x_j \ne 0} x_j A_{:,j}$.
- **Semirings.** Over the Boolean semiring the product gives the set of vertices with an edge into a set; over min-plus it is one relaxation round of the Bellman and Ford method.

## Examples

1. Let $A = \begin{pmatrix} 2 & 0 & 0 & 1 \\ 0 & 0 & 3 & 0 \\ 0 & 0 & 0 & 0 \\ 4 & 5 & 0 & 0 \end{pmatrix}$ and $x = (1, 2, 3, 4)^{\mathsf T}$. In CSR form, $v = (2, 1, 3, 4, 5)$, $c = (0, 3, 2, 0, 1)$ and $r = (0, 2, 3, 3, 5)$. Then $y_0 = 2 \cdot 1 + 1 \cdot 4 = 6$, $y_1 = 3 \cdot 3 = 9$, $y_2 = 0$ (the row is empty, $r_2 = r_3$), and $y_3 = 4 \cdot 1 + 5 \cdot 2 = 14$. So $y = (6, 9, 0, 14)^{\mathsf T}$ with $5$ multiplications, against $16$ for the dense product.
2. A tridiagonal matrix of order $n$ has $3n - 2$ nonzeros, so one product costs $\Theta(n)$ instead of $\Theta(n^2)$.
3. The empty matrix ($z = 0$) gives the zero vector in $\Theta(m)$ time, since $y$ must still be written.

## Known algorithms

- **CSR row loop.** $\Theta(m + z)$ time, $z$ multiplications, no extra space. Rows are independent, so it parallelizes by rows; load balance needs care when row lengths vary widely.
- **Coordinate (COO) form.** A list of triples $(i, j, v)$ in any order; $\Theta(z)$ time plus the zeroing of $y$. It is easy to build but each entry needs a scatter to $y$.
- **[ELLPACK](/ellpack-format/) and sliced variants.** Pad each row to the same length $L$ and store the entries column by column. This suits vector units and GPUs, at the cost $\Theta(mL)$, which is wasteful when a few rows are long.
- **Blocked formats.** Store small dense blocks, for example $2 \times 2$ or $4 \times 4$, with one index per block. This cuts the index traffic for matrices from finite element methods.
- **Reordering.** Permuting rows and columns, for example with [reverse Cuthill and McKee](/reverse-cuthill-mckee/), reduces the bandwidth of $A$, so the accesses to $x$ stay in cache.

## Bounds

- **RAM bound.** $\Theta(m + z)$ time is tight: each stored nonzero can change the result, and each $y_i$ must be written.
- **Multiplications.** For a matrix whose nonzero entries are independent indeterminates, $z$ multiplications are needed, as for [dense matrix-vector products](/matrix-vector-multiplication/).
- **I/O bound.** In the external memory model with parameters $M$ and $B$, the direct method makes $O(z)$ I/Os in the worst case, because the accesses to $x$ are irregular, and $O(z/B + m/B + n/B)$ I/Os when the accesses to $x$ are local. Bender, Brodal, Fagerberg, Jacob and Vicari (2007) proved matching upper and lower bounds for the worst case over the sparsity patterns, which lie between these two through a sorting-like term. The exact bound is not reproduced here.
- **In practice.** Each nonzero needs a value and an index from memory (for example $8 + 4$ bytes) for $2$ floating-point operations, so SpMV runs at a small fraction of peak arithmetic speed. Williams and others (2007) measured this limit on multicore machines; the [roofline model](/roofline-model/) explains it. This is an observation about machines, not a proved bound.

## Reductions

- **Dense case.** With $z = mn$, it is the dense [matrix-vector product](/matrix-vector-multiplication/).
- **Sparse matrix products.** A product $AB$ of sparse matrices is $p$ products of $A$ with the sparse columns of $B$; see [sparse matrix multiplication](/sparse-matrix-multiplication/).
- **Black box algorithms.** Methods that use $A$ only through products $x \mapsto Ax$, such as the Lanczos and Wiedemann methods, have cost $O(k (m + z))$ for $k$ products; see [black box matrix](/black-box-matrix/).

## Applications

- Krylov subspace solvers for sparse linear systems: conjugate gradients, GMRES, BiCGSTAB.
- Eigenvalue methods: power iteration, Lanczos and Arnoldi.
- [PageRank](/pagerank/) and other random walks on large graphs.
- Graph traversal written as linear algebra, and the Wiedemann algorithm over finite fields.

## References
