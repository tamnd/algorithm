---
tag: RKKDT2
kind: problem
slug: matrix-vector-multiplication
name: Matrix-vector multiplication
aliases:
- matrix times vector
- matvec
- MVM
- GEMV
area: algebra/matrix-multiplication
level: intro
summary: Compute y = Ax for an m by n matrix A and a vector x of length n; the direct method uses m n multiplications, which is optimal for a general matrix.
model: algebraic-computation-tree
complexity:
  vars: {m: the number of rows of A, n: the number of columns of A}
  time: {worst: Θ(m n)}
prereqs: [dot-product, naive-matrix-multiplication]
see_also: [sparse-matrix-vector-multiplication, online-matrix-vector-multiplication, four-russians-method, black-box-matrix, krylov-subspace, power-iteration, matrix-multiplication-quadratic-lower-bound]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition
    locator: Section 1.1 (the row and column forms of gaxpy, y = y + Ax) and Section 1.4, Fast matrix-vector products (structured matrices and the FFT)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.4, Evaluation of polynomials (the part on the number of multiplications for a general set of linear forms)
  - paper: "Shmuel Winograd, On the number of multiplications necessary to compute certain functions, Communications on Pure and Applied Mathematics 23 (1970)"
    locator: the theorem on general linear forms (a general m by n matrix times a vector needs m n multiplications)
  - paper: "Ryan Williams, Matrix-vector multiplication in sub-quadratic time (some preprocessing required), Proceedings of the 18th ACM-SIAM Symposium on Discrete Algorithms (SODA 2007)"
    locator: the main theorem (Boolean matrix-vector products in O(n^2 / (ε log n)^2) time after O(n^(2+ε)) preprocessing)
---

Matrix-vector multiplication is the problem of computing $y = Ax$ for an $m \times n$ matrix $A$ and a vector $x$ of length $n$. The direct method takes the [dot product](/dot-product/) of each row with $x$, for $mn$ multiplications, and for a general matrix no method in the algebraic model can do better. Faster methods exist only when $A$ has structure (sparse, Toeplitz, low rank) or when $A$ is fixed and used many times. It is the inner step of iterative methods such as [power iteration](/power-iteration/) and [Krylov subspace](/krylov-subspace/) solvers.

## In plain words

You have a table of numbers and a list of numbers. The list has one number for each column of the table. For each row of the table, multiply each number in the row by the matching number of the list, and add the products. The result is a new list with one number for each row.

Each number of the table is used once, so the work is about the size of the table. A method that skips a number of the table can give the wrong answer, so for a general table this work cannot be avoided. Only special tables, for example tables with many zeros or with a repeating pattern, allow a shortcut.

## Definition

Let $R$ be a ring (or a semiring, see Variants). The input is a matrix $A \in R^{m \times n}$ and a vector $x \in R^n$. The output is the vector $y \in R^m$ with

$$y_i = \sum_{j=0}^{n-1} A[i][j] \, x_j, \qquad 0 \le i < m.$$

When $n = 0$, each sum is empty and $y$ is the zero vector of length $m$. The cost model counts ring operations, as on the other [matrix multiplication](/naive-matrix-multiplication/) pages.

The direct method computes each $y_i$ in turn (the row form), or adds $x_j$ times column $j$ to $y$ for each $j$ (the column form). Both use $mn$ multiplications and $m(n-1)$ additions when each sum starts with its first term.

## Variants

- **Transposed product.** Compute $x^{\mathsf T} A$, or $A^{\mathsf T} y$. It costs the same. By the transposition principle (Tellegen's principle), a linear straight-line program for $x \mapsto Ax$ gives one for $y \mapsto A^{\mathsf T} y$ of about the same size.
- **GEMV.** The BLAS routine computes $y \leftarrow \alpha A x + \beta y$, with scalars $\alpha$ and $\beta$.
- **Over a semiring.** Over the Boolean semiring, $y_i = \bigvee_j (A[i][j] \wedge x_j)$: the set of vertices with an edge into the set $x$. Over the min-plus semiring, $y_i = \min_j (A[i][j] + x_j)$: one relaxation round of the Bellman-Ford method.
- **Sparse matrices.** When $A$ has $\mathrm{nnz}(A)$ nonzero entries, the product takes $\Theta(\mathrm{nnz}(A) + m + n)$ time with a compressed format. See [sparse matrix-vector multiplication](/sparse-matrix-vector-multiplication/).
- **With preprocessing.** $A$ is known in advance and many vectors $x$ arrive. This is the setting of the [four Russians method](/four-russians-method/) and of [online matrix-vector multiplication](/online-matrix-vector-multiplication/).
- **Structured matrices.** A circulant or Toeplitz matrix of order $n$ times a vector takes $O(n \log n)$ operations with the [fast Fourier transform](/fast-fourier-transform/). A matrix given as a [black box](/black-box-matrix/) is known only through this operation.

## Examples

1. Over $\mathbb{Z}$: $\begin{pmatrix} 2 & 0 & 1 \\ 1 & 3 & 0 \end{pmatrix} \begin{pmatrix} 4 \\ 5 \\ 6 \end{pmatrix} = \begin{pmatrix} 2 \cdot 4 + 0 \cdot 5 + 1 \cdot 6 \\ 1 \cdot 4 + 3 \cdot 5 + 0 \cdot 6 \end{pmatrix} = \begin{pmatrix} 14 \\ 19 \end{pmatrix}$. Here $m = 2$, $n = 3$, and the direct method does $6$ multiplications.
2. Over the Boolean semiring: $A = \begin{pmatrix} 1 & 0 & 1 \\ 0 & 0 & 0 \\ 0 & 1 & 1 \end{pmatrix}$ and $x = (0, 1, 0)^{\mathsf T}$ give $y = (0, 0, 1)^{\mathsf T}$. Row 1 is empty, so $y_1 = 0$ for every $x$.
3. A circulant matrix: the first column $c = (1, 2, 3)$ gives $C[i][j] = c_{(i - j) \bmod 3}$, so $C = \begin{pmatrix} 1 & 3 & 2 \\ 2 & 1 & 3 \\ 3 & 2 & 1 \end{pmatrix}$. With $x = (1, 0, 2)^{\mathsf T}$, $Cx = (5, 8, 5)^{\mathsf T}$, which is the cyclic convolution of $c$ and $x$. For large $n$ this product is computed with three FFTs instead of $n^2$ multiplications.

## Known algorithms

- **Direct method** (row form or column form): $mn$ multiplications, $\Theta(mn)$ time. It is the matrix case of [naive matrix multiplication](/naive-matrix-multiplication/) with $p = 1$.
- **Sparse formats** such as [compressed sparse row](/compressed-sparse-row/) and [ELLPACK](/ellpack-format/): $\Theta(\mathrm{nnz}(A) + m)$ time.
- **[Four Russians method](/four-russians-method/)** over a finite semiring such as $\mathbb{F}_2$ or the Boolean semiring: after $O(n^2)$ preprocessing of $A$, each product takes $O(n^2 / \log n)$ word operations. Williams (2007) reduced this to $O(n^2 / (\varepsilon \log n)^2)$ for Boolean matrices, after a preprocessing time of $O(n^{2+\varepsilon})$, for each fixed $\varepsilon > 0$.
- **Structured matrices**: $O(n \log n)$ for circulant and Toeplitz matrices with the [FFT](/fast-fourier-transform/), and $O((m + n) r)$ for a matrix given as a product $UV$ of an $m \times r$ and an $r \times n$ matrix.

## Bounds

- **Upper bound.** $O(mn)$ ring operations for every ring and semiring.
- **Lower bound by reading.** For a general matrix, each algorithm must read every entry of $A$ on some input: if it does not read $A[i][j]$ on an input with $x_j \ne 0$, changing $A[i][j]$ changes $y_i$ but not the output. So $\Omega(mn)$ is a tight bound in the worst case on a RAM, and this problem, unlike [matrix multiplication](/matrix-multiplication-exponent/), is solved up to constant factors.
- **Lower bound on multiplications.** When the entries of $A$ and $x$ are independent indeterminates, each algorithm that uses $+$, $-$, $\times$ and $\div$ needs at least $mn$ multiplications and divisions (Winograd, 1970). So the direct method is optimal even in its count of multiplications.
- **With preprocessing.** When $A$ is fixed, the cost per vector can drop below $mn$ word operations (see Known algorithms). The OMv conjecture says that the online version, with $n$ vectors that arrive one at a time, has no algorithm with total time $O(n^{3 - \varepsilon})$ over the Boolean semiring. See [online matrix-vector multiplication](/online-matrix-vector-multiplication/).

## Reductions

- **From matrix multiplication.** The product $AB$ is the list of the $p$ products $A b_j$ for the columns $b_j$ of $B$. So $MM(n) \le n \cdot MV(n)$, where $MV(n)$ is the cost of one product. The converse does not hold: a fast matrix product gives no fast single matrix-vector product, because one product already has the optimal cost $\Theta(n^2)$.
- **To a dot product.** Each $y_i$ is one dot product, so the problem is $m$ independent dot products of length $n$.
- **Polynomial evaluation.** Evaluating a polynomial of degree $n - 1$ at $m$ points is the product of an $m \times n$ [Vandermonde matrix](/vandermonde-matrix/) with the coefficient vector. [Multipoint evaluation](/multipoint-evaluation/) does it faster than $mn$ by using this structure.

## Applications

- Iterative methods: [power iteration](/power-iteration/), [PageRank](/pagerank/), [Krylov subspace](/krylov-subspace/) methods, and the [Wiedemann algorithm](/wiedemann-algorithm/) over finite fields.
- Steps of a [Markov chain](/markov-chain/): the next distribution is the current one times the [transition matrix](/transition-matrix/).
- Graph search: one step of breadth-first search is a Boolean matrix-vector product with the [adjacency matrix](/adjacency-matrix/).
- Linear layers of neural networks, and the evaluation of linear recurrences one step at a time.

## References
