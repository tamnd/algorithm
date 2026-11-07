---
tag: TC9AAR
kind: definition
slug: kronecker-product
name: Kronecker product
aliases:
- tensor product of matrices
- matrix direct product
- Zehfuss matrix
area: algebra/matrix-multiplication
level: core
summary: The Kronecker product of an m×n matrix A and a p×q matrix B is the mp×nq block matrix whose block (i, j) is A[i][j] times B; it satisfies the mixed-product rule (A⊗B)(C⊗D) = AC⊗BD.
prereqs: [naive-matrix-multiplication, rank]
see_also: [matrix-multiplication-tensor, tensor-rank, tensor-product, walsh-hadamard-transform, dft-matrix, sylvester-equation, strassen-algorithm, determinant]
sources:
  - book: isbn:9780521467131
    title: Roger A. Horn and Charles R. Johnson, Topics in Matrix Analysis
    locator: Chapter 4, Matrix equations and the Kronecker product (definition, mixed-product property, eigenvalues, the vec identity, and Kronecker sums)
  - paper: "Charles F. Van Loan, The ubiquitous Kronecker product, Journal of Computational and Applied Mathematics 123 (2000), doi:10.1016/S0377-0427(00)00393-9"
    locator: Sections 1 to 3 (basic properties, fast products with Kronecker structure, and the nearest Kronecker product problem)
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory
    locator: Chapter 15, Asymptotic complexity of matrix multiplication (tensor products of matrix multiplication tensors and the submultiplicativity of rank)
---

The Kronecker product $A \otimes B$ of an $m \times n$ matrix $A$ and a $p \times q$ matrix $B$ is the $mp \times nq$ block matrix whose block in block row $i$ and block column $j$ is $A[i][j] \, B$. It is the matrix of the tensor product of the two linear maps in the product basis. Its main rule, the mixed-product property $(A \otimes B)(C \otimes D) = AC \otimes BD$, turns products of structured matrices into products of small ones. In matrix multiplication it describes the recursion of [Strassen's algorithm](/strassen-algorithm/), since the [matrix multiplication tensors](/matrix-multiplication-tensor/) satisfy $\langle n, m, p \rangle \otimes \langle n', m', p' \rangle = \langle n n', m m', p p' \rangle$.

## Definition

Let $R$ be a commutative ring, $A \in R^{m \times n}$ and $B \in R^{p \times q}$. With indices from $0$, the Kronecker product $A \otimes B \in R^{mp \times nq}$ is

$$(A \otimes B)[i p + k][j q + l] = A[i][j] \, B[k][l], \qquad 0 \le i < m, \; 0 \le j < n, \; 0 \le k < p, \; 0 \le l < q.$$

In block form,

$$A \otimes B = \begin{pmatrix} A[0][0] B & \cdots & A[0][n-1] B \\ \vdots & \ddots & \vdots \\ A[m-1][0] B & \cdots & A[m-1][n-1] B \end{pmatrix}.$$

The definition needs only a ring. Commutativity is needed for the rules below that move scalars from one factor to the other, such as the mixed-product property. The main rules, for matrices of compatible sizes:

- **Bilinear.** $(A + A') \otimes B = A \otimes B + A' \otimes B$, $A \otimes (B + B') = A \otimes B + A \otimes B'$, and $(cA) \otimes B = A \otimes (cB) = c (A \otimes B)$.
- **Associative, not commutative.** $(A \otimes B) \otimes C = A \otimes (B \otimes C)$. In general $A \otimes B \ne B \otimes A$, but $B \otimes A = P (A \otimes B) Q$ for two permutation matrices $P$ and $Q$ (perfect shuffles) that depend only on the sizes.
- **Mixed product.** $(A \otimes B)(C \otimes D) = (AC) \otimes (BD)$ when $AC$ and $BD$ are defined. Proof: if $D$ has $s$ columns, the entry of the left side in row $i p + k$ and column $j s + l$ is $\sum_{r, t} A[i][r] B[k][t] C[r][j] D[t][l] = (AC)[i][j] \, (BD)[k][l]$.
- **Transpose and inverse.** $(A \otimes B)^{\mathsf T} = A^{\mathsf T} \otimes B^{\mathsf T}$. If $A$ and $B$ are invertible, so is $A \otimes B$, with $(A \otimes B)^{-1} = A^{-1} \otimes B^{-1}$, by the mixed-product rule.
- **Rank, determinant and eigenvalues.** Over a field, $\operatorname{rank}(A \otimes B) = \operatorname{rank}(A) \operatorname{rank}(B)$. For $A$ of order $n$ and $B$ of order $q$, $\det(A \otimes B) = \det(A)^q \det(B)^n$, and over an algebraically closed field the eigenvalues of $A \otimes B$ are the $nq$ products $\lambda_i \mu_j$ of eigenvalues of $A$ and $B$.
- **The vec rule.** Let $\operatorname{vec}_r(X)$ list the entries of $X$ row by row. For $X \in R^{n \times q}$, $(A \otimes B) \operatorname{vec}_r(X) = \operatorname{vec}_r(A X B^{\mathsf T})$. In the column-by-column order $\operatorname{vec}$ used in numerical texts, the same fact reads $\operatorname{vec}(A X C) = (C^{\mathsf T} \otimes A) \operatorname{vec}(X)$.

The vec rule gives a fast product. For $A$ of order $n$ and $B$ of order $q$, the matrix $A \otimes B$ has $(nq)^2$ entries, but $(A \otimes B) x$ costs only $n q (n + q)$ multiplications through $A X B^{\mathsf T}$, without forming $A \otimes B$. For a product of $k$ factors of order $2$, the same idea costs $O(N \log N)$ for $N = 2^k$.

## Examples and non-examples

- **A small product.** $\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix} \otimes \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} = \begin{pmatrix} 0 & 1 & 0 & 2 \\ 1 & 0 & 2 & 0 \\ 0 & 3 & 0 & 4 \\ 3 & 0 & 4 & 0 \end{pmatrix}$.
- **The determinant rule.** For $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$ with $\det A = -2$ and $B = \begin{pmatrix} 2 & 1 & 0 \\ 0 & 1 & 1 \\ 1 & 0 & 3 \end{pmatrix}$ with $\det B = 7$, the $6 \times 6$ matrix $A \otimes B$ has determinant $(-2)^3 \cdot 7^2 = -392$.
- **Identity factors.** $I_m \otimes B$ is block diagonal with $m$ copies of $B$. $A \otimes I_p$ has the same entries as $A$, spread out: each entry $A[i][j]$ becomes the block $A[i][j] I_p$. And $I_m \otimes I_p = I_{mp}$.
- **Hadamard matrices.** With $H_2 = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$, the Sylvester matrices $H_{2^k} = H_2^{\otimes k}$ are the matrices of the [Walsh-Hadamard transform](/walsh-hadamard-transform/). The fast transform is the factorization $H_{2^k} = \prod_{t=1}^{k} (I_{2^{t-1}} \otimes H_2 \otimes I_{2^{k-t}})$, with $N \lg N$ additions and subtractions for $N = 2^k$.
- **Matrix multiplication tensors.** The tensor $\langle n, m, p \rangle$ of the $n \times m$ by $m \times p$ product satisfies $\langle n, m, p \rangle \otimes \langle n', m', p' \rangle = \langle n n', m m', p p' \rangle$. So $\langle 2, 2, 2 \rangle^{\otimes k} = \langle 2^k, 2^k, 2^k \rangle$, and a rank $7$ decomposition of $\langle 2, 2, 2 \rangle$ gives one of rank $7^k$ for $\langle 2^k, 2^k, 2^k \rangle$, which is the recursion of Strassen's algorithm. See [tensor rank](/tensor-rank/).
- **Matrix equations.** The [Sylvester equation](/sylvester-equation/) $AX + XB = C$ is the linear system $(A \otimes I + I \otimes B^{\mathsf T}) \operatorname{vec}_r(X) = \operatorname{vec}_r(C)$. The matrix $A \otimes I + I \otimes B^{\mathsf T}$ is a Kronecker sum.
- **Graphs.** If $A$ and $B$ are [adjacency matrices](/adjacency-matrix/) of graphs $G$ and $H$, then $A \otimes B$ is the adjacency matrix of their tensor product graph, where $(u, v)$ and $(u', v')$ are adjacent exactly when $uu'$ is an edge of $G$ and $vv'$ is an edge of $H$.
- **Non-example: entrywise product.** The Hadamard product $A \circ B$ multiplies entries in the same place. It needs equal sizes and has the same size as $A$, while $A \otimes B$ has $mp \times nq$ entries. The two are related: $A \circ B$ is a principal submatrix of $A \otimes B$ when $A$ and $B$ are square of the same order.
- **Non-example: not every block matrix is a Kronecker product.** $\operatorname{diag}(1, 0, 0, 1)$ is not $A \otimes B$ for any $2 \times 2$ matrices. A $4 \times 4$ matrix is a Kronecker product of two $2 \times 2$ matrices exactly when the $4 \times 4$ matrix whose rows are the four $2 \times 2$ blocks, each read as a row of length $4$, has rank at most $1$. For $\operatorname{diag}(1, 0, 0, 1)$ the rows from blocks $(0, 0)$ and $(1, 1)$ are $(1, 0, 0, 0)$ and $(0, 0, 0, 1)$, of rank $2$.
- **Non-example: commutativity.** With $P = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ and $D = \begin{pmatrix} 1 & 0 \\ 0 & 2 \end{pmatrix}$, row $0$ of $P \otimes D$ is $(0, 0, 1, 0)$ and row $0$ of $D \otimes P$ is $(0, 1, 0, 0)$, so $P \otimes D \ne D \otimes P$. The two products are equal up to a reordering of rows and columns.

## Related definitions

- **Tensor product.** For vector spaces $V$ and $W$ with bases $(v_j)$ and $(w_l)$, the [tensor product](/tensor-product/) $V \otimes W$ has the basis $(v_j \otimes w_l)$. If $f : V \to V'$ and $g : W \to W'$ have matrices $A$ and $B$, then $f \otimes g$ has the matrix $A \otimes B$ in the product bases ordered as in the definition.
- **Kronecker sum.** For square $A$ of order $n$ and $B$ of order $q$, $A \oplus B = A \otimes I_q + I_n \otimes B$. Its eigenvalues are the sums $\lambda_i + \mu_j$.
- **Tensor product of tensors.** For 3-tensors $T \in U \otimes V \otimes W$ and $T' \in U' \otimes V' \otimes W'$, the product $T \otimes T'$ lives in $(U \otimes U') \otimes (V \otimes V') \otimes (W \otimes W')$. [Tensor rank](/tensor-rank/) is submultiplicative under it: $\operatorname{R}(T \otimes T') \le \operatorname{R}(T) \operatorname{R}(T')$.
- **DFT factorizations.** The Cooley and Tukey factorization of the [DFT matrix](/dft-matrix/) of order $N = N_1 N_2$ writes it as a product of $F_{N_1} \otimes I_{N_2}$, a diagonal matrix of twiddle factors, $I_{N_1} \otimes F_{N_2}$ and a permutation.
- **Outer product.** For column vectors, $u \otimes v^{\mathsf T} = u v^{\mathsf T}$, a matrix of rank at most $1$.

## References
