---
tag: RBAF05
kind: problem
slug: toeplitz-system-solving
name: Toeplitz system solving
aliases: [Toeplitz linear system, Toeplitz linear systems, solving Toeplitz systems]
area: algebra/exact-linear-algebra
level: advanced
summary: Solve a linear system whose coefficient matrix is constant along diagonals, exploiting its structure.
prereqs: [linear-system-solving, pade-approximation]
see_also: [levinson-durbin-algorithm, levinson-durbin-recursion, berlekamp-massey, extended-euclidean-algorithm, half-gcd, polynomial-multiplication, linear-prediction, sylvester-matrix]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 4.7, Classical Methods for Toeplitz Systems (the Yule-Walker problem, Durbin's and Levinson's algorithms, and the Trench algorithm for the inverse)
  - paper: doi:10.1016/0196-6774(80)90013-9
    title: Richard P. Brent, Fred G. Gustavson and David Y. Y. Yun, Fast solution of Toeplitz systems of equations and computation of Pade approximants, Journal of Algorithms 1(3), 1980
    locator: pp. 259 to 295 (Toeplitz and Hankel systems through the extended Euclidean algorithm and Pade approximants, in O(n log^2 n) operations, with no condition on the leading minors)
  - book: isbn:9780817642402
    title: Victor Y. Pan, Structured Matrices and Polynomials, Unified Superfast Algorithms, Birkhauser and Springer, 2001
    locator: Chapters 4 and 5 (displacement rank of Toeplitz-like matrices, and the superfast divide and conquer solution)
  - paper: "Norman Levinson, The Wiener RMS (root mean square) error criterion in filter design and prediction, Journal of Mathematics and Physics 25, 1947"
    locator: pp. 261 to 278 (the order-recursive solution of symmetric Toeplitz systems in O(n^2) operations)
---

Toeplitz system solving asks for the solution of $T x = c$ where $T$ is an $n \times n$ Toeplitz matrix, constant along each diagonal, so $T_{ij} = t_{i - j}$ and the matrix is given by only $2n - 1$ numbers. General elimination ignores this and costs $O(n^3)$ field operations. The Levinson-Durbin recursion uses the structure to solve the system in $O(n^2)$ operations when the leading principal minors are nonzero, and the superfast algorithms, which go through the extended Euclidean algorithm and Pade approximation, reach $O(n \log^2 n)$ for every nonsingular $T$.

## In plain words

A Toeplitz table has the same number all along each diagonal, so the whole table is described by its first row and first column. Such tables appear whenever the same rule is applied at every time step, as in signal processing and in the study of sequences.

Because the table has so little information, solving its equations should not need the full work of ordinary elimination. The classical method grows the solution one size at a time, reusing the answer for the smaller table. The fastest methods turn the problem into a question about polynomials and solve that with fast polynomial arithmetic.

## Definition

**Notation.** $K$ is a field. $T = (t_{i - j})_{0 \le i, j < n}$ is an $n \times n$ Toeplitz matrix over $K$ given by $t_{-(n-1)}, \ldots, t_{n-1}$, and $c \in K^n$. $M(n)$ is the cost of multiplying two polynomials of degree below $n$ over $K$, which is $O(n \log n)$ with the FFT when $K$ has suitable roots of unity and $O(n \log n \log \log n)$ in general. For integer input, $b$ is the maximum binary length of the $t_k$ and $c_i$.

**Input.** The $2n - 1$ entries of $T$ and the vector $c$.

**Output.** The unique $x \in K^n$ with $T x = c$, if $T$ is nonsingular; otherwise "singular", or a description of all solutions.

**Displacement structure.** Let $Z$ be the $n \times n$ shift matrix with ones just below the diagonal. Then $T - Z T Z^T$ is zero outside the first row and the first column, so it has rank at most $2$. Matrices for which this *displacement* has small rank $\alpha$ are called Toeplitz-like. Products and inverses of Toeplitz-like matrices are again Toeplitz-like with small $\alpha$, and the inverse of a Toeplitz matrix, although not Toeplitz, is described by $O(n)$ numbers (the Gohberg-Semencul formula).

## Variants

- **Symmetric positive definite.** Over $\mathbb{R}$, all leading principal minors are positive, and Levinson's and Durbin's recursions are numerically stable in a weak sense; see the [numerical Levinson-Durbin recursion](/levinson-durbin-recursion/).
- **Strongly nonsingular.** Every leading principal minor is nonzero. Then the exact [Levinson-Durbin algorithm](/levinson-durbin-algorithm/) works over any field in $O(n^2)$ operations.
- **General nonsingular.** Some leading minors vanish. Look-ahead versions of Levinson skip over singular blocks, and the Euclidean and Pade approach needs no condition.
- **Hankel systems.** $H_{ij} = h_{i + j}$. Reversing the order of the rows turns a Hankel matrix into a Toeplitz matrix, so the same algorithms apply. Hankel systems are the linear systems behind [Berlekamp-Massey](/berlekamp-massey/) and Pade approximation.
- **Circulant systems.** A circulant matrix is diagonalized by the discrete Fourier transform, so $T x = c$ costs $O(M(n))$.
- **Toeplitz-like and block Toeplitz.** Matrices of small displacement rank, including the [Sylvester matrix](/sylvester-matrix/) of two polynomials, which is block Toeplitz.
- **Over $\mathbb{Z}$ or $\mathbb{Q}$.** Exact solutions, with fraction-free or multimodular versions.

## Examples

**A symmetric system.** With $t_0 = 4$, $t_{\pm 1} = 2$, $t_{\pm 2} = 1$,

$$T = \begin{pmatrix} 4 & 2 & 1 \\ 2 & 4 & 2 \\ 1 & 2 & 4 \end{pmatrix}, \qquad c = \begin{pmatrix} 7 \\ 8 \\ 7 \end{pmatrix}, \qquad x = \begin{pmatrix} 1 \\ 1 \\ 1 \end{pmatrix}.$$

The leading principal minors are $4$, $12$ and $36$, all nonzero, so the Levinson recursion applies. The inverse is

$$T^{-1} = \frac{1}{12} \begin{pmatrix} 4 & -2 & 0 \\ -2 & 5 & -2 \\ 0 & -2 & 4 \end{pmatrix},$$

which is not Toeplitz (the middle entry differs from the corners of the diagonal), but it is symmetric about both diagonals and is determined by its first column, as the Gohberg-Semencul formula says.

**A vanishing leading minor.** $T = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ is Toeplitz and nonsingular, but $t_0 = 0$, so the Levinson recursion fails at its first step. A look-ahead step or the Euclidean method is needed, although the solution of $T x = c$ is simply $x = (c_2, c_1)$.

**Edge cases.** For $n = 1$, $t_0 x_1 = c_1$. The zero matrix is Toeplitz, and every vector solves $0 x = 0$.

## Known algorithms

- **Gaussian elimination:** $O(n^3)$ field operations, ignoring the structure.
- **Levinson (1947), Durbin (1960), Trench (1964), Zohar (1974):** order-recursive algorithms in $O(n^2)$ field operations for strongly nonsingular $T$. Durbin's version solves the Yule-Walker equations, Levinson's solves general right-hand sides, and Trench's computes $T^{-1}$ in $O(n^2)$. See the [Levinson-Durbin algorithm](/levinson-durbin-algorithm/).
- **Bareiss (1969) for Toeplitz matrices:** an $O(n^2)$ elimination that keeps the Toeplitz structure of the reduced matrices, closely related to the Schur algorithm.
- **Superfast algorithms:** Brent, Gustavson and Yun (1980) solve every nonsingular Toeplitz or Hankel system in $O(M(n) \log n)$, so $O(n \log^2 n)$ with the FFT, by computing Pade approximants with the fast [extended Euclidean algorithm](/half-gcd/). Bitmead and Anderson (1980) and Morf (1980) gave divide and conquer methods on displacement rank with the same bound, for strongly nonsingular matrices.
- **Black box methods:** a Toeplitz matrix times a vector is a [polynomial product](/polynomial-multiplication/), so $T v$ costs $O(M(n))$, and Wiedemann's method solves $T x = c$ in $O(n M(n))$ operations.

## Bounds

**Algebraic model.** $O(M(n) \log n)$ field operations suffice for every nonsingular Toeplitz system (Brent, Gustavson and Yun, 1980), and $O(n)$ is a lower bound because every input entry can matter. Whether the $\log n$ factor can be removed is open. These are proved.

**Bit sizes over $\mathbb{Z}$.** By Cramer's rule, $x = \operatorname{adj}(T) c / \det T$, and the Hadamard bound gives at most $n (b + \tfrac12 \log_2 n) + \log_2 n$ binary digits for each numerator and the common denominator. So the output has $O(n^2 (b + \log n))$ digits in total, which is much larger than the $O(n b)$ digits of the input. Levinson's recursion over $\mathbb{Q}$ with reduced fractions stays within these sizes, because its intermediate values are quotients of minors of $T$; without reduction they can grow much faster. These are proved bounds; the full size is reached on random input, an observation.

## Reductions

- **To Pade approximation and the Euclidean algorithm.** Solving a nonsingular Hankel system with right-hand side built from the same sequence is the computation of a Pade approximant of $\sum_i h_i x^i$, which the extended Euclidean algorithm gives; a general right-hand side needs a few such computations and a Gohberg-Semencul type formula (Brent, Gustavson and Yun, 1980).
- **To polynomial multiplication.** Toeplitz matrix-vector products are polynomial products, and conversely.
- **From linear recurrences.** Finding the minimal recurrence of a sequence of length $2n$ is a Hankel system, solved by [Berlekamp-Massey](/berlekamp-massey/) in $O(n^2)$ or by the half-gcd in $O(M(n) \log n)$.

## Applications

- **Linear prediction and signal processing.** The Yule-Walker equations of autoregressive models and Wiener filters are symmetric Toeplitz systems; see [linear prediction](/linear-prediction/).
- **Sequence and coding problems.** Decoding BCH and Reed-Solomon codes and computing linear complexity of sequences solve Hankel systems.
- **Polynomial computations.** Polynomial division, gcd, and the [resultant](/resultant/) are expressed with Toeplitz or Sylvester matrices.
- **Black box linear algebra.** Random Toeplitz matrices are cheap preconditioners in the methods of Kaltofen and Saunders for the rank and solution of sparse systems.

## References
