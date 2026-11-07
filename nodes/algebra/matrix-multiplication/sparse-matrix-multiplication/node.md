---
tag: SGVJ72
kind: problem
slug: sparse-matrix-multiplication
name: Sparse matrix multiplication
aliases:
- sparse matrix product
- SpGEMM
- sparse general matrix-matrix multiplication
area: algebra/matrix-multiplication
level: core
summary: Multiply two matrices with few nonzero entries in time that depends on the nonzeros and on the elementary products, not on n^3, as in Gustavson's row-by-row method.
model: algebraic-computation-tree
complexity:
  vars: {n: the order of the matrices, z: the number of nonzero entries of A and B together, f: the number of elementary products with both factors nonzero (pairs of a nonzero of A in column k and a nonzero of B in row k)}
  time: {worst: O(n + z + f)}
prereqs: [naive-matrix-multiplication, sparse-matrix, compressed-sparse-row]
see_also: [sparse-matrix-vector-multiplication, boolean-matrix-multiplication, compressed-sparse-column, hash-table, triangle-counting, matrix-multiplication-exponent, breadth-first-search, ellpack-format]
sources:
  - paper: doi:10.1145/355791.355796
    title: Fred G. Gustavson, Two fast algorithms for sparse matrices, multiplication and permuted transposition, ACM Transactions on Mathematical Software 4(3) (1978)
    locator: pp. 250 to 269 (the row-by-row product with a dense accumulator, in time linear in the number of elementary products)
  - paper: "Raphael Yuster and Uri Zwick, Fast sparse matrix multiplication, ACM Transactions on Algorithms 1(1) (2005)"
    locator: the main theorem (combining the row-by-row method with fast rectangular products; O(m^0.7 n^1.2 + n^(2+o(1))) for m nonzeros with the exponents known in 2004)
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems
    locator: Chapter 2, Basic algorithms (the compressed column format and the function cs_multiply for C = AB)
  - paper: "Rasmus Resen Amossen and Rasmus Pagh, Faster join-projects and sparse matrix multiplications, 12th International Conference on Database Theory (ICDT 2009)"
    locator: the main theorem (output-sensitive Boolean sparse products with fast matrix multiplication)
---

Sparse matrix multiplication asks for $C = AB$ when $A$ and $B$ have mostly zero entries and are stored in a [sparse format](/sparse-matrix/) that lists only the nonzeros. The useful cost measure is not $n^3$ but the number $f$ of nonzero elementary products $A[i][k] B[k][j]$, which the row-by-row method of Gustavson (1978) computes in $O(n + z + f)$ time, where $z$ is the number of input nonzeros. The output can be much denser than the inputs, up to $n^2$ entries from $2n$ nonzeros, and it can also have fewer nonzeros than $f$ because of cancellation. For dense enough inputs, fast rectangular products beat the row-by-row method in theory.

## In plain words

Most entries of the two tables are zero, and a zero times anything is zero. So skip them. For each row of the first table, look only at its nonzero entries. Each such entry picks out one row of the second table; scale that row by the entry and add it into the answer row. Keep a scratch row to collect the sums, and write out only the places that became nonzero.

The work is the number of nonzero pairs that meet, plus the size of the tables. It does not depend on how many zeros there are. But two tables with few nonzeros can still have a full answer, and then the work is large.

## Definition

Let $R$ be a ring or a semiring. The input is $A \in R^{n \times m}$ and $B \in R^{m \times p}$, each given as a list of nonzero entries, for example in [compressed sparse row](/compressed-sparse-row/) (CSR) or [compressed sparse column](/compressed-sparse-column/) (CSC) form. The output is $C = AB$ in the same kind of format:

$$C[i][j] = \sum_{k} A[i][k] \, B[k][j].$$

Let $\operatorname{nnz}(X)$ be the number of stored nonzeros of $X$, $z = \operatorname{nnz}(A) + \operatorname{nnz}(B)$, and

$$f = \sum_{k=0}^{m-1} \operatorname{nnz}(A_{:,k}) \cdot \operatorname{nnz}(B_{k,:}),$$

the number of pairs $(A[i][k], B[k][j])$ with both factors nonzero. Then $\operatorname{nnz}(C) \le \min(f, np)$. The cost counts ring operations plus the index operations of a RAM, so the time includes reading the input and writing the output.

## Variants

- **Sparse times dense.** One factor is dense, as in sparse neural network layers or block Krylov methods. The cost is $\operatorname{nnz}(A) \cdot p$.
- **Masked product.** Compute $C$ only at the positions of a given mask $M$, as $C = M \circ (AB)$. Triangle counting uses $\operatorname{sum}(A \circ A^2)$ and needs only the entries of $A^2$ on the edges of $A$.
- **Boolean and other semirings.** Over the Boolean semiring the product is a join of two binary relations followed by projection, the join-project of databases. Over min-plus it is one step of a shortest path method on a sparse graph.
- **Structure only.** Compute the nonzero pattern of $C$, which is the Boolean product of the patterns. Solvers often do this first, to allocate the output.
- **Square of one matrix.** $A^2$ or $A A^{\mathsf T}$, for example to form the normal equations or a graph of common neighbors.

## Examples

1. Let $A = \begin{pmatrix} 1 & 0 & 2 \\ 0 & 0 & 0 \\ 0 & 3 & 0 \end{pmatrix}$ and $B = \begin{pmatrix} 0 & 4 & 0 \\ 5 & 0 & 0 \\ 0 & 6 & 7 \end{pmatrix}$. Row $0$ of $C$ is $1 \cdot (0, 4, 0) + 2 \cdot (0, 6, 7) = (0, 16, 14)$, row $1$ is empty because row $1$ of $A$ is empty, and row $2$ is $3 \cdot (5, 0, 0) = (15, 0, 0)$. Here $f = 1 \cdot 1 + 1 \cdot 1 + 1 \cdot 2 = 4$ multiplications, against $27$ for the triple loop, and $\operatorname{nnz}(C) = 3$.
2. Fill. Let $A$ have nonzeros only in column $0$ and $B$ only in row $0$, all equal to $1$. Then $z = 2n$ but $C$ is the all-ones matrix, so $\operatorname{nnz}(C) = f = n^2$. Every method needs $\Omega(n^2)$ time here.
3. Cancellation. $\begin{pmatrix} 1 & 1 \end{pmatrix} \begin{pmatrix} 1 \\ -1 \end{pmatrix} = (0)$. Here $f = 2$ but $\operatorname{nnz}(C) = 0$ if exact zeros are removed. With floating-point numbers, such a result may be a tiny nonzero instead.

## Known algorithms

- **Gustavson's row-by-row method.** For each row $i$ of $A$ and each nonzero $A[i][k]$, add $A[i][k]$ times row $k$ of $B$ into a dense accumulator of length $p$, and keep a list of the columns that were touched. Then copy the touched entries into row $i$ of $C$ and clear only those. This is $O(n + p + z + f)$ time and $O(p)$ extra space (Gustavson, 1978). With CSC input, the same method works by columns. Davis's CSparse function cs_multiply is a standard implementation.
- **Hash accumulator.** Replace the dense accumulator by a [hash table](/hash-table/) of the touched columns. It saves memory for very wide matrices and is common on GPUs, at expected $O(1)$ cost per elementary product.
- **Heap or merge methods.** Merge the scaled rows of $B$ for row $i$ with a heap, which gives the columns of row $i$ of $C$ in sorted order, at $O(f \log n)$ cost.
- **Outer-product form.** $C = \sum_k A_{:,k} B_{k,:}$, a sum of $m$ sparse rank-one matrices, followed by a sort or a merge of the partial products. It reads each input once but stores $f$ partial products.
- **Fast rectangular products.** Yuster and Zwick (2005) split the middle index $k$ into heavy indices (with many nonzeros in $A_{:,k}$ or $B_{k,:}$) and light ones. They use a dense fast rectangular product for the heavy part and the row-by-row method for the light part. With the exponents known in 2004, this takes $O(m^{0.7} n^{1.2} + n^{2+o(1)})$ for $n \times n$ matrices with at most $m$ nonzeros each, which is better than both the dense and the row-by-row bounds in a middle range of densities. This method is only of theoretical interest.

## Bounds

- **Upper bounds.** $O(n + z + f)$ by the row-by-row method, $O(n^{\omega})$ by a dense fast product, and the Yuster and Zwick bound in between. Note $f \le \operatorname{nnz}(A) \cdot \max_k \operatorname{nnz}(B_{k,:})$ and $f \le n \cdot \operatorname{nnz}(A)$ for square matrices.
- **Output size.** Each method needs $\Omega(\operatorname{nnz}(C))$ time to write the output, and $\operatorname{nnz}(C)$ can be $\Theta(n^2)$ when $z = O(n)$ (Example 2).
- **No general improvement on $f$ without algebra.** For algorithms that form each nonzero elementary product, $f$ is a lower bound by definition, and over a semiring without subtraction no other approach is known in general. Output-sensitive methods for the Boolean case (Amossen and Pagh, 2009) use fast dense products on subproblems.
- **In practice.** Sparse products are limited by memory traffic and by irregular access to $B$ and to the accumulator, not by arithmetic. The speed in floating-point operations per second is typically a small fraction of that of dense products on the same machine. This is an observation, not a bound.

## Reductions

- **Matrix-vector products.** Each column of $C$ is $A$ times a sparse column of $B$, so the problem is $p$ sparse [matrix-vector products](/sparse-matrix-vector-multiplication/) with sparse vectors.
- **Graphs.** For adjacency matrices, $(A^2)[i][j]$ counts the walks of length two from $i$ to $j$. So the number of triangles is $\frac{1}{6}\operatorname{sum}(A \circ A^2)$, see [triangle counting](/triangle-counting/). A [breadth-first search](/breadth-first-search/) from many sources is a sparse product of the adjacency matrix with a sparse matrix of frontiers.
- **Databases.** The Boolean product of two sparse 0/1 matrices is the join-project of two binary relations on their common attribute.

## Applications

- Algebraic multigrid, which forms the coarse operator $P^{\mathsf T} A P$ with two sparse products.
- Graph algorithms written as linear algebra over semirings: triangle counting, multi-source search, clustering by the Markov cluster method.
- The normal equations $A^{\mathsf T} A$ and the elimination graphs of sparse direct solvers.
- Sparse neural networks and the contraction of sparse tensors.

## References
