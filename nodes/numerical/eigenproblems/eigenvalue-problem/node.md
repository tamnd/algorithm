---
tag: S4JM0J
kind: problem
slug: eigenvalue-problem
name: Eigenvalue problem
aliases:
- eigendecomposition problem
- eigenproblem
- algebraic eigenvalue problem
- standard eigenvalue problem
area: numerical/eigenproblems
level: intro
summary: Given a square matrix A, find scalars λ and nonzero vectors v with A v = λ v. In floating point the goal is a backward stable answer.
model: floating-point-model
complexity:
  vars: {n: "the order of A, at least 1"}
  time: {worst: O(n^3)}
  flops: {nonsymmetric: "10n^3", symmetric: "4n^3/3"}
prereqs: [eigenvalue, eigenvector, backward-error-analysis]
see_also: [symmetric-eigenproblem, nonsymmetric-eigenproblem, generalized-eigenvalue-problem, singular-value-decomposition, qr-algorithm, hessenberg-reduction, schur-decomposition, eigenvalue-condition-number]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Chapter 7 (Unsymmetric Eigenvalue Problems, Section 7.5.6 for the flop counts of the practical QR algorithm), Chapter 8 (Symmetric Eigenvalue Problems) and Chapter 10 (Large Sparse Eigenvalue Problems)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lectures 24 to 31 (dense eigenvalue problems and the SVD) and Lectures 32 to 36 (iterative methods)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Chapter 4 (nonsymmetric eigenproblems), Chapter 5 (the symmetric eigenproblem and the SVD) and Chapter 7 (iterative methods for eigenvalue problems)
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapters 2 and 3 (perturbation theory and error analysis), Chapter 8 (the LR and QR algorithms)
  - paper: "J. H. Wilkinson, Global convergence of tridiagonal QR algorithm with origin shifts, Linear Algebra and its Applications 1, 1968"
    title: J. H. Wilkinson, Global convergence of tridiagonal QR algorithm with origin shifts
    locator: pp. 409 to 420 (convergence of the symmetric tridiagonal QR algorithm with the Wilkinson shift for every start)
  - paper: "Jess Banks, Jorge Garza-Vargas, Archit Kulkarni and Nikhil Srivastava, Pseudospectral shattering, the sign function, and diagonalization in nearly matrix multiplication time, Foundations of Computational Mathematics 23, 2023"
    title: Banks, Garza-Vargas, Kulkarni and Srivastava, diagonalization in nearly matrix multiplication time
    locator: the main theorem (a randomized backward-approximate diagonalization in O(T_MM(n) log^2(n/δ)) arithmetic operations)
---

The eigenvalue problem asks, for a square matrix $A$, for the scalars $\lambda$ and nonzero vectors $v$ with $A v = \lambda v$: the [eigenvalues](/eigenvalue/) and [eigenvectors](/eigenvector/) of $A$. Since the eigenvalues are the roots of a polynomial of degree $n$, no finite algorithm solves it for $n \ge 5$, and every method is iterative. In floating point the realistic goal is a backward stable answer: the computed eigenvalues are the exact eigenvalues of a matrix $A + E$ with $\|E\|$ a small multiple of $u \|A\|$. The standard dense method, [Hessenberg reduction](/hessenberg-reduction/) followed by the shifted [QR algorithm](/qr-algorithm/), reaches this goal in $O(n^3)$ flops.

## In plain words

You are given a square table of numbers that acts on vectors. You want the special directions that the table only stretches, and the stretch amounts. For a table with two rows you can solve a quadratic equation. For five rows or more, no formula exists, so every method improves a guess step by step and stops when the error is as small as the rounding of the computer allows.

Rounding means that the exact answer is out of reach. The useful promise is that the answer is exact for a table that differs from yours only in the last digits. Whether that answer is close to the exact one depends on the table: for some tables a tiny change moves the stretch amounts a lot, and no method can fix that.

## Definition

**Notation of this area.** $A \in \mathbb{C}^{n \times n}$ (often real). Its eigenvalues are $\lambda_1, \dots, \lambda_n$ with multiplicity, ordered $|\lambda_1| \ge |\lambda_2| \ge \dots \ge |\lambda_n|$ for a general matrix and $\lambda_1 \ge \dots \ge \lambda_n$ for a Hermitian one; $v_i$ is an eigenvector of $\lambda_i$. The Schur form is $A = Q T Q^*$ with $Q$ unitary and $T$ upper triangular; $H$ is an upper Hessenberg matrix ($h_{ij} = 0$ for $i > j + 1$). The singular values of an $m \times n$ matrix are $\sigma_1 \ge \dots \ge \sigma_{\min(m,n)} \ge 0$. The Rayleigh quotient is $\rho(x) = x^* A x / x^* x$. The Krylov space is $\mathcal{K}_k(A, b) = \operatorname{span}\{b, A b, \dots, A^{k-1} b\}$. In floating point, $u$ is the unit roundoff ($2^{-53}$ in IEEE double), and a flop is one real addition, subtraction, multiplication or division.

**The exact problem.** Input: $A \in \mathbb{C}^{n \times n}$. Output: the list $\lambda_1, \dots, \lambda_n$ of the roots of $\det(tI - A)$, and, if asked, a nonzero $v_i$ with $A v_i = \lambda_i v_i$ for each $i$, or a Schur decomposition $A = Q T Q^*$. A full set of eigenvectors exists only when $A$ is [diagonalizable](/diagonalization/); the Schur form exists for every $A$ and is the standard output of dense codes.

**The floating-point problem.** Input: $A$ in floating point. Output: $\hat\lambda_1, \dots, \hat\lambda_n$ (and optionally $\hat Q$, $\hat T$, $\hat v_i$) such that there exist $E$ and an exactly unitary $Q$ with
$$Q^* (A + E) Q = \hat T, \qquad \|E\|_2 \le c(n) \, u \, \|A\|_2, \qquad \|\hat Q - Q\|_2 \le c(n) \, u,$$
where $\hat T$ is upper triangular (or quasi-triangular with $2 \times 2$ blocks for conjugate pairs of a real matrix), $\hat\lambda_i$ are its diagonal entries (or block eigenvalues), and $c(n)$ is a modest polynomial in $n$. This is backward stability. The forward error then follows from perturbation theory: to first order, $|\hat\lambda_i - \lambda_i| \lesssim \kappa(\lambda_i) \, c(n) \, u \, \|A\|_2$ for a simple eigenvalue with [condition number](/eigenvalue-condition-number/) $\kappa(\lambda_i)$.

**Checking an answer.** For a computed pair $(\hat\lambda, \hat v)$ with $\|\hat v\|_2 = 1$, the residual norm $\|A \hat v - \hat\lambda \hat v\|_2$ is the smallest $\|E\|_2$ for which the pair is exact for $A + E$. A residual of order $u \|A\|_2$ certifies backward stability of that pair. The sum and the product of the computed eigenvalues must match $\operatorname{tr} A$ and $\det A$ up to rounding.

## Variants

- **Symmetric or Hermitian** ($A = A^*$): real eigenvalues, an orthonormal eigenvector basis, and well-conditioned eigenvalues. See the [symmetric eigenproblem](/symmetric-eigenproblem/) and, after reduction, the [tridiagonal eigenproblem](/tridiagonal-eigenproblem/).
- **Nonsymmetric**: complex eigenvalues even for real input, possibly defective, and eigenvalues of any condition. See the [nonsymmetric eigenproblem](/nonsymmetric-eigenproblem/).
- **All eigenvalues, or a few.** Dense methods return all $n$. For a large sparse $A$ one asks for the $k \ll n$ largest, smallest or closest to a target $\sigma$, and uses only products $x \mapsto A x$: [Lanczos](/lanczos-algorithm/), [Arnoldi](/arnoldi-iteration/), [implicitly restarted Arnoldi](/implicitly-restarted-arnoldi/), [subspace iteration](/subspace-iteration/).
- **Eigenvalues only, or with vectors.** Vectors add work (about $25n^3$ flops instead of $10n^3$ for a real nonsymmetric matrix) and, for close eigenvalues, are much less accurate than the eigenvalues.
- **Generalized**: $A x = \lambda B x$, the [generalized eigenvalue problem](/generalized-eigenvalue-problem/), solved by the [QZ algorithm](/qz-algorithm/).
- **Singular values**: the [singular value decomposition](/singular-value-decomposition/) $A = U \Sigma V^*$, which is a Hermitian eigenproblem for $A^* A$ in disguise but is solved without forming it.
- **High relative accuracy**: for special classes (bidiagonal matrices, graded positive definite matrices), each eigenvalue or singular value can be computed with a small relative error, not only an error relative to $\|A\|$. See [dqds](/dqds-algorithm/) and the [Jacobi algorithm](/jacobi-eigenvalue-algorithm/).

## Examples

**A matrix with a known spectrum.** Let $S = \begin{pmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \\ 1 & 0 & 1 \end{pmatrix}$ and $A = S \operatorname{diag}(2, 4, 6) S^{-1}$:
$$A = \begin{pmatrix} 3 & 1 & -1 \\ -1 & 5 & 1 \\ -2 & 2 & 4 \end{pmatrix}.$$
The eigenvalues are 2, 4 and 6 and the eigenvectors are the columns of $S$: $A (1, 0, 1)^T = (2, 0, 2)^T$, $A (1, 1, 0)^T = (4, 4, 0)^T$ and $A (0, 1, 1)^T = (0, 6, 6)^T$. The checks hold: $2 + 4 + 6 = 12 = \operatorname{tr} A$ and $2 \cdot 4 \cdot 6 = 48 = \det A$. Matrices built this way, with a rational or orthogonal $S$, are the standard test inputs for the algorithms of this area.

**A non-example of a good method.** Computing $\det(tI - A)$ and then its roots is exact in rational arithmetic, but in floating point the roots can be far less accurate than the eigenvalues: for $\operatorname{diag}(1, 2, \dots, 20)$ the eigenvalues are perfectly conditioned, while the roots of the expanded characteristic polynomial (Wilkinson's polynomial) move into the complex plane under a relative change of less than $10^{-9}$ in one coefficient.

**An ill-conditioned problem.** The $n \times n$ Jordan block with eigenvalue 0, with $\varepsilon$ put in the bottom-left corner, has the eigenvalues $\varepsilon^{1/n}$ times the $n$-th roots of unity. For $n = 16$ and $\varepsilon = 10^{-16}$, they have modulus $0.1$. A backward stable method can return any of these, since the perturbation is at the rounding level.

## Known algorithms

| algorithm | input | cost (leading term) | status of the count |
|---|---|---|---|
| [Hessenberg reduction](/hessenberg-reduction/) | general | $10n^3/3$ flops | exact count |
| [QR algorithm](/qr-algorithm/) with [Francis double shift](/francis-double-shift-qr/) | Hessenberg | about $10n^3$ flops in total for eigenvalues, $25n^3$ with Schur vectors | typical, assumes about 2 iterations per eigenvalue |
| [tridiagonalization](/tridiagonalization/) | symmetric | $4n^3/3$ flops | exact count |
| symmetric tridiagonal QR | tridiagonal | $O(n^2)$ for eigenvalues, about $6n^3$ more for vectors (Demmel, Section 5.3) | typical |
| [divide and conquer](/divide-and-conquer-eigensolver/) | tridiagonal | $O(n^2)$ to about $4n^3/3$ with vectors, often much less with deflation | typical |
| [bisection](/bisection-eigenvalue-algorithm/) plus [inverse iteration](/inverse-iteration/) | tridiagonal | $O(n)$ flops per bisection step and one step per bit of accuracy; $O(n)$ per vector | proved for bisection |
| [MRRR](/mrrr-algorithm/) | tridiagonal | $O(n^2)$ for all pairs | typical |
| [Jacobi](/jacobi-eigenvalue-algorithm/) | symmetric | $O(n^3)$ per sweep, about 6 to 10 sweeps | typical, quadratic convergence proved |
| [Golub-Kahan SVD](/golub-kahan-svd-algorithm/) | general $m \times n$ | $4mn^2 - 4n^3/3$ for the bidiagonalization | exact count for that phase |
| [power iteration](/power-iteration/), [Lanczos](/lanczos-algorithm/), [Arnoldi](/arnoldi-iteration/) | large sparse | matrix-vector products | depends on the spectrum |

## Bounds

- **No finite algorithm.** Each monic polynomial of degree $n$ is the characteristic polynomial of its companion matrix, so by the [Abel-Ruffini theorem](/abel-ruffini-theorem/) no algorithm that uses finitely many arithmetic operations and radicals finds the eigenvalues of every matrix with $n \ge 5$ (Trefethen and Bau, Lecture 25). Iterative methods are the only option.
- **Reading the input.** A dense matrix has $n^2$ entries and each eigenvalue depends on each of them, so $\Omega(n^2)$ operations are necessary. No better general lower bound is known.
- **Upper bounds.** The dense methods above use $O(n^3)$ flops. The bound for the QR algorithm counts a typical, observed number of iterations per eigenvalue; it is not a theorem. For the symmetric tridiagonal QR algorithm with the [Wilkinson shift](/wilkinson-shift/), global convergence is proved (Wilkinson 1968). For the nonsymmetric QR algorithm with Francis shifts, there are matrices on which it stalls without exceptional shifts, and no proof of global convergence exists. A randomized algorithm of Banks, Garza-Vargas, Kulkarni and Srivastava (2023) computes an approximate diagonalization, with backward error $\delta$, in $O(T_{MM}(n) \log^2(n/\delta))$ arithmetic operations, where $T_{MM}(n)$ is the cost of a matrix product.
- **Accuracy.** Backward stability is the best that a method can promise in general. The forward error is the backward error times the condition: [Bauer-Fike](/bauer-fike-theorem/) for diagonalizable matrices, [Weyl](/weyls-inequality/) for Hermitian ones ($|\hat\lambda_i - \lambda_i| \le \|E\|_2$), and the [Davis-Kahan theorem](/davis-kahan-theorem/) for eigenvectors. A defective eigenvalue of index $m$ can move by about $\|E\|^{1/m}$.

## Reductions

- **Polynomial roots to eigenvalues.** The roots of $t^n + c_{n-1} t^{n-1} + \dots + c_0$ are the eigenvalues of its companion matrix. MATLAB's `roots` works this way.
- **Eigenvalues to polynomial roots.** In exact arithmetic, compute the [characteristic polynomial](/characteristic-polynomial-computation/) and isolate its roots. This is right for exact or symbolic input and wrong in floating point.
- **SVD to a Hermitian eigenproblem.** The eigenvalues of $\begin{pmatrix} 0 & A \\ A^* & 0 \end{pmatrix}$ are $\pm \sigma_i$ (and zeros), and those of $A^* A$ are $\sigma_i^2$.
- **Generalized to standard.** If $B$ is nonsingular, $A x = \lambda B x$ is the standard problem for $B^{-1} A$; if $B$ is Hermitian positive definite with Cholesky factor $B = L L^*$, it is the Hermitian problem for $L^{-1} A L^{-*}$.
- **Shift and invert.** The eigenvalues of $A$ near $\sigma$ are the largest eigenvalues of $(A - \sigma I)^{-1}$, so a method for extremal eigenvalues finds interior ones at the cost of one factorization of $A - \sigma I$.
- **Deflation.** A known eigenpair reduces the problem to order $n - 1$; see [deflation](/deflation/).

## Applications

Stability of linear and linearized dynamical systems, natural frequencies and modes of structures (as a generalized problem $K x = \lambda M x$), energy levels in quantum chemistry, principal component analysis, ranking by a dominant eigenvector, spectral graph partitioning, Markov chain mixing, and the convergence analysis of iterative methods for linear systems through the spectral radius.

## References
