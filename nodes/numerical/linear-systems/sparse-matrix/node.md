---
tag: FY3NRP
kind: abstract-type
slug: sparse-matrix
name: Sparse matrix
aliases:
- sparse matrix representation
- sparse matrix format
area: numerical/linear-systems
level: core
summary: A matrix stored by its nonzero entries only.
prereqs: [array, graph]
see_also: [compressed-sparse-row, sparse-matrix-vector-multiplication, sparse-matrix-multiplication, sparse-linear-systems, adjacency-list, hash-table, banded-matrix, fill-in]
sources:
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 2, Basic algorithms (the triplet and compressed-column forms, matrix-vector multiplication, transpose, summing duplicates, permutation and matrix multiplication)
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Chapter 3, Sparse Matrices (graph representations, permutations, storage schemes and basic operations)
  - paper: doi:10.1145/355791.355796
    title: Fred G. Gustavson, Two fast algorithms for sparse matrices, multiplication and permuted transposition, ACM Transactions on Mathematical Software 4(3), 1978
    locator: the row-wise sparse matrix product and the transpose in time linear in the number of nonzeros
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 3.1, Inner and Outer Products (the error bound for a dot product, which applies row by row to a sparse matrix-vector product)
---

A sparse matrix is an $n_r \times n_c$ matrix $A$ together with a set $S$ of positions, its *pattern*, outside which every entry is known to be zero; only the $m = |S|$ entries in $S$ are stored. It is worth the trouble when $m$ is far below $n_r n_c$, typically $m = O(n)$ for matrices from meshes, networks and circuits. The abstract type offers entry access, assembly by accumulation, traversal by rows or columns, and the product $y = A x$; implementations such as coordinate lists, hash maps and [compressed sparse row](/compressed-sparse-row/) trade the cost of insertion against the speed of traversal. The matrix-vector product then costs $2m$ flops instead of $2 n_r n_c$.

## In plain words

Many large matrices are almost all zeros: each unknown is linked to only a few neighbours. Writing out every zero would waste memory and time, so a sparse matrix keeps a list of the entries that may be nonzero, each with its row, its column and its value. Different ways of keeping that list are good at different jobs. A loose list or a lookup table is easy to add to while the matrix is being built. A packed list sorted by rows is hard to change but very fast to read, which is what solvers need. Builders usually collect entries in the first kind and convert to the second.

## Operations

**Notation.** $A \in \mathbb{R}^{n_r \times n_c}$ (often square, $n_r = n_c = n$), pattern $S \subseteq [n_r] \times [n_c]$, $m = |S|$ the number of stored entries ("nonzeros"), $d_i$ the number of stored entries in row $i$ and $d = \max_i d_i$. In floating point, $u = 2^{-53}$ and $\gamma_k = k u/(1 - k u)$ for $k u < 1$. A sparse matrix value is a map $a : S \to \mathbb{R}$; entries outside $S$ are zero.

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}(n_r, n_c) \to A$ | the zero matrix, $S = \emptyset$ |
| `get` | $\text{get}(A, i, j) \to \mathbb{R}$ | $a_{ij}$ if $(i,j) \in S$, else $0$ |
| `set` | $\text{set}(A, i, j, v) \to A$ | puts $(i, j)$ in $S$ with value $v$ |
| `add-to` | $\text{add-to}(A, i, j, v) \to A$ | $a_{ij} \leftarrow a_{ij} + v$, inserting $(i,j)$ if needed; the assembly operation of finite elements |
| `nnz` | $\text{nnz}(A) \to \mathbb{N}$ | returns $m = |S|$ |
| `row` | $\text{row}(A, i) \to$ list | the pairs $(j, a_{ij})$ with $(i, j) \in S$ |
| `col` | $\text{col}(A, j) \to$ list | the pairs $(i, a_{ij})$ with $(i, j) \in S$ |
| `matvec` | $\text{matvec}(A, x) \to y$ | $y = A x$ |
| `matvec-T` | $\text{matvec-T}(A, x) \to y$ | $y = A^T x$ |
| `transpose` | $\text{transpose}(A) \to A^T$ | pattern $\{(j, i) : (i, j) \in S\}$ |
| `permute` | $\text{permute}(A, p, q) \to B$ | $b_{ij} = a_{p(i)\, q(j)}$, the reordering used before factorization |

**Example.** The matrix
$$A = \begin{pmatrix} 4 & 0 & 0 & 1 \\ 0 & 3 & 0 & 0 \\ 2 & 0 & 5 & 0 \\ 0 & 0 & 0 & 6 \end{pmatrix}$$
has $m = 6$. In coordinate (triplet) form it is the list $(0,0,4), (0,3,1), (1,1,3), (2,0,2), (2,2,5), (3,3,6)$ in any order. In compressed sparse row form it is
$$\text{rowptr} = [0, 2, 3, 5, 6], \quad \text{colind} = [0, 3, 1, 0, 2, 3], \quad \text{val} = [4, 1, 3, 2, 5, 6],$$
where row $i$ occupies positions $\text{rowptr}[i]$ to $\text{rowptr}[i+1] - 1$. Its compressed sparse column form is $\text{colptr} = [0, 2, 3, 4, 6]$, $\text{rowind} = [0, 2, 1, 2, 0, 3]$, $\text{val} = [4, 2, 3, 5, 1, 6]$, which is also the CSR form of $A^T$.

**Graphs.** The pattern of a square $A$ is the edge set of a directed graph on $n$ vertices, and of an undirected [graph](/graph/) when $S$ is symmetric. CSR is exactly the [adjacency list](/adjacency-list/) of that graph stored in arrays, which is why orderings and elimination are studied as graph algorithms.

## Laws

For all $A$, positions $(i, j) \ne (k, l)$ and values $v$, $w$:

1. $\text{get}(\text{new}(n_r, n_c), i, j) = 0$.
2. $\text{get}(\text{set}(A, i, j, v), i, j) = v$ and $\text{get}(\text{set}(A, i, j, v), k, l) = \text{get}(A, k, l)$.
3. $\text{get}(\text{add-to}(A, i, j, v), i, j) = \text{get}(A, i, j) + v$, so assembly does not depend on the order of the `add-to` calls in exact arithmetic (in floating point it does, at the level of rounding).
4. $\text{matvec}(A, x)_i = \sum_{(i, j) \in S} a_{ij} x_j$, the same as the dense product of the matrix that `get` describes.
5. $\text{get}(\text{transpose}(A), j, i) = \text{get}(A, i, j)$ and $\text{matvec-T}(A, x) = \text{matvec}(\text{transpose}(A), x)$.
6. $\text{nnz}(\text{set}(A, i, j, v)) = \text{nnz}(A) + [(i, j) \notin S]$.

**Structural and numerical zeros.** The laws describe values, not patterns: an entry of $S$ may hold the value $0$ (a *structural* nonzero that is numerically zero). Implementations keep such entries when the pattern matters, as in symbolic factorization, where cancellation is ignored and fill is predicted from $S$ alone; a separate `drop` operation removes them.

**Rounding.** A computed product $\hat y = \text{fl}(A x)$ forms each $y_i$ as a dot product of length $d_i$, so (proved, Higham Section 3.1)
$$|\hat y - A x| \le \gamma_d\, |A|\,|x| \quad \text{componentwise}, \qquad \hat y = (A + \Delta A) x, \;\; |\Delta A| \le \gamma_d |A|,$$
with $d$ the largest row count rather than $n$; $\Delta A$ has the pattern of $A$. The order of summation within a row changes $\hat y$ at the rounding level, so two formats can give results that differ in the last digits.

## Implementations

Costs are worst case unless stated; storage counts words, an index and a value each one word.

| format | storage | `get` | `set` / `add-to` | `row` | `col` | `matvec` |
|---|---|---|---|---|---|---|
| dense [array](/array/) | $n_r n_c$ | $O(1)$ | $O(1)$ | $O(n_c)$ | $O(n_r)$ | $2 n_r n_c$ flops |
| coordinate (COO, triplet) | $3m$ | $O(m)$ | $O(1)$ amortized append; duplicates summed later | $O(m)$ | $O(m)$ | $2m$ flops, scattered writes |
| dictionary of keys ([hash table](/hash-table/)) | $O(m)$ | $O(1)$ expected | $O(1)$ expected | $O(m)$ | $O(m)$ | $2m$ flops, poor locality |
| list of lists (one sorted list per row) | $2m + n_r$ | $O(\log d_i)$ | $O(d_i)$ | $O(d_i)$ | $O(m)$ | $2m$ flops |
| compressed sparse row (CSR) | $2m + n_r + 1$ | $O(\log d_i)$ if sorted | $O(m)$ for a new position | $O(d_i)$ | $O(m)$ | $2m$ flops |
| compressed sparse column (CSC) | $2m + n_c + 1$ | $O(\log d_j)$ if sorted | $O(m)$ for a new position | $O(m)$ | $O(d_j)$ | $2m$ flops, column-wise |
| ELLPACK (padded rows) | $2 n_r d$ | $O(\log d)$ | $O(d)$ while $d$ fits | $O(d)$ | $O(n_r d)$ | $2 n_r d$ flops, regular, good on vector units and GPUs |
| diagonal (DIA) | $n \times$ number of diagonals | $O(1)$ | $O(1)$ on stored diagonals | $O(\text{diagonals})$ | same | for stencils and [banded matrices](/banded-matrix/) |
| block CSR (BSR) | $b^2$ per block plus indices | as CSR on blocks | as CSR | as CSR | as CSR | dense $b \times b$ kernels, fewer indices |

Conversions are cheap: COO to CSR or CSC is a counting sort in $O(m + n)$ time, and the transpose of a CSR matrix (equivalently, CSR to CSC) also takes $O(m + n)$ time (Gustavson, 1978; Davis, Chapter 2). The usual pattern is to assemble in COO or a hash map, convert once to CSR or CSC, and then never change the pattern. Direct solvers such as CSparse, CHOLMOD and UMFPACK use CSC; iterative solvers and SciPy's default products use CSR.

**Memory traffic dominates.** In CSR with 8-byte values and 4-byte indices, `matvec` reads at least 12 bytes per nonzero for 2 flops, plus the scattered reads of $x$. That is at most $1/6$ flop per byte, far below what processors can do per byte of memory bandwidth, so the speed of a sparse product is set by memory bandwidth and the locality of the column indices, not by the flop count. Reorderings such as [reverse Cuthill-McKee](/reverse-cuthill-mckee/) and blocked formats such as BSR help mostly by improving locality.

## Lower bounds

- **Storage.** A format that represents every pattern with $m$ entries in an $n \times n$ matrix must distinguish $\binom{n^2}{m}$ patterns, which needs $\log_2 \binom{n^2}{m} \approx m \log_2(n^2/m)$ binary digits; for $m = O(n)$ that is $\Theta(m \log n)$, the same order as CSR's $m$ indices of $\log_2 n$ digits each. Patterns with structure (banded, stencils, blocks) can be stored with fewer indices.
- **Product.** Any algorithm for `matvec` on a general sparse matrix must read every stored value, so it needs $\Omega(m)$ time; CSR and CSC meet this bound with $2m$ flops.
- **Updates versus traversal.** In a contiguous packed format, inserting a new position shifts $\Theta(m)$ entries in the worst case; keeping $O(1)$ expected insertion (hash maps) gives up contiguous row traversal. No single format is best at both, which is why the type has several implementations.

## References
