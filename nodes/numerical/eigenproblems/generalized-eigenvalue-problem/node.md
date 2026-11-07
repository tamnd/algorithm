---
tag: AY7D4K
kind: problem
slug: generalized-eigenvalue-problem
name: Generalized eigenvalue problem
aliases:
- matrix pencil problem
- A x = λ B x
- generalized eigenproblem
area: numerical/eigenproblems
level: advanced
summary: Given square A and B, find λ and x ≠ 0 with A x = λ B x. The QZ algorithm solves the general case backward stably; Cholesky reduction handles symmetric A with positive definite B.
model: floating-point-model
complexity:
  vars: {n: "the order of A and B, at least 1"}
  time: {worst: O(n^3)}
  flops: {qz_eigenvalues: "30n^3", symmetric_definite: "8n^3/3"}
prereqs: [eigenvalue-problem, cholesky-decomposition]
see_also: [qz-algorithm, schur-decomposition, symmetric-eigenproblem, eigenvalue-condition-number, courant-fischer-theorem, lanczos-algorithm, implicitly-restarted-arnoldi, finite-element-method]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.7, The Generalized Eigenvalue Problem (generalized Schur form, the QZ algorithm and its flop counts), and Section 8.7, Generalized Eigenvalue Problems with Symmetry
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 4.5, Other Nonsymmetric Eigenvalue Problems (regular pencils, the Weierstrass and Kronecker canonical forms), and Section 5.5 (the symmetric definite pencil)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, Classics in Applied Mathematics 20, SIAM, 1998
    locator: Chapter 15, The Generalized Eigenvalue Problem A x = λ M x
  - book: isbn:9780898714715
    title: Zhaojun Bai, James Demmel, Jack Dongarra, Axel Ruhe and Henk van der Vorst (editors), Templates for the Solution of Algebraic Eigenvalue Problems, SIAM, 2000
    locator: Chapter 5, Generalized Hermitian Eigenvalue Problems, and Chapter 8, Generalized Non-Hermitian Eigenvalue Problems
  - book: isbn:9780126702309
    title: G. W. Stewart and Ji-guang Sun, Matrix Perturbation Theory, Academic Press, 1990
    locator: Chapter VI, Generalized Eigenvalue Problems (the chordal metric and perturbation bounds)
  - paper: doi:10.1137/0710024
    title: C. B. Moler and G. W. Stewart, An algorithm for generalized matrix eigenvalue problems, SIAM Journal on Numerical Analysis 10, 1973
    locator: pp. 241 to 256 (the QZ algorithm)
  - paper: "R. S. Martin and J. H. Wilkinson, Reduction of the symmetric eigenproblem A x = λ B x and related problems to standard form, Numerische Mathematik 11, 1968, pp. 99 to 110"
    title: R. S. Martin and J. H. Wilkinson, Reduction of the symmetric eigenproblem to standard form
    locator: the Cholesky-based reduction and its error analysis
---

The generalized eigenvalue problem asks, for square matrices $A, B \in \mathbb{C}^{n \times n}$, for scalars $\lambda$ and nonzero vectors $x$ with $A x = \lambda B x$. The pair is called a pencil and is written $A - \lambda B$; for $B = I$ it is the standard [eigenvalue problem](/eigenvalue-problem/). When $B$ is singular some eigenvalues are infinite, and when $\det(A - \lambda B)$ is zero for every $\lambda$ the problem is ill-posed. The [QZ algorithm](/qz-algorithm/) solves the general case backward stably in about $30n^3$ flops. For Hermitian $A$ and positive definite $B$, a [Cholesky](/cholesky-decomposition/) reduction to a standard Hermitian problem is cheaper.

## In plain words

In the ordinary eigenvalue problem, you look for directions that one matrix only stretches. In the generalized problem, there are two matrices, and you look for directions where the first matrix gives the same result as the second one times a number. In a vibrating structure the first matrix describes the stiffness and the second the mass, and the numbers give the squared frequencies.

If the second matrix can be inverted, you could multiply by its inverse and get an ordinary problem. This is often a bad idea, because the inverse can magnify rounding errors. Good methods work on both matrices together. If the second matrix cannot be inverted, some answers are "infinite", and the methods must report them correctly.

## Definition

**Notation.** $A, B \in \mathbb{C}^{n \times n}$. The pencil $A - \lambda B$ is *regular* if $p(\lambda) = \det(A - \lambda B)$ is not the zero polynomial, and *singular* otherwise. For a regular pencil the eigenvalues are listed $\lambda_1, \dots, \lambda_n$ with multiplicity in a fixed order, the infinite ones last. Norms are 2-norms and $u$ is the unit roundoff.

**Eigenvalues.** For a regular pencil, $\lambda \in \mathbb{C}$ is a finite eigenvalue if $p(\lambda) = 0$, and then some $x \ne 0$ satisfies $A x = \lambda B x$. The degree of $p$ is at most $n$, and equals $n$ exactly when $B$ is nonsingular. If $\deg p = d < n$, the pencil has $n - d$ infinite eigenvalues. They are the zero eigenvalues of the reversed pencil $B - \mu A$, and their eigenvectors satisfy $B x = 0$. It is often better to work with pairs: $(\alpha, \beta) \ne (0, 0)$ is an eigenvalue if $\det(\beta A - \alpha B) = 0$, and $\lambda = \alpha / \beta$, with $\beta = 0$ for an infinite eigenvalue. A left eigenvector is $y \ne 0$ with $y^* A = \lambda y^* B$.

**Generalized Schur form.** For every regular pencil there are unitary $Q$ and $Z$ with
$$Q^* A Z = S, \qquad Q^* B Z = T,$$
where $S$ and $T$ are upper triangular. The eigenvalues are $(\alpha_i, \beta_i) = (s_{ii}, t_{ii})$, that is, $\lambda_i = s_{ii} / t_{ii}$. For real $A$ and $B$, real orthogonal $Q$ and $Z$ give a quasi-triangular $S$ with $2 \times 2$ blocks for complex conjugate pairs, and a triangular $T$. This is the generalized analog of the [Schur decomposition](/schur-decomposition/), and it is the output of QZ.

**Symmetric definite pencils.** If $A$ is Hermitian and $B$ is Hermitian positive definite, every eigenvalue is real and finite. There is a nonsingular $X$ with $X^* A X = \Lambda = \operatorname{diag}(\lambda_1, \dots, \lambda_n)$ and $X^* B X = I$, so the eigenvectors are orthonormal in the inner product $\langle x, z \rangle_B = z^* B x$. With $\lambda_1 \ge \dots \ge \lambda_n$, the eigenvalues satisfy the [Courant-Fischer theorem](/courant-fischer-theorem/) for the quotient $x^* A x / x^* B x$.

**The floating-point problem.** Input: $A$ and $B$ in floating point. Output: pairs $(\hat\alpha_i, \hat\beta_i)$, and optionally $\hat Q$, $\hat Z$, such that they are the exact generalized Schur data of $(A + E, B + F)$ with $\|E\|_2 \le c(n)\, u\, \|A\|_2$ and $\|F\|_2 \le c(n)\, u\, \|B\|_2$ for a modest $c(n)$. QZ gives this.

## Variants

- **Symmetric definite** ($A = A^*$, $B = B^* \succ 0$): real eigenvalues and $B$-orthogonal eigenvectors. Cholesky reduction, Jacobi-type methods and, for large sparse problems, [Lanczos](/lanczos-algorithm/) in the $B$-inner product or LOBPCG.
- **Definite in a weaker sense.** If some real combination $\cos\theta\, A + \sin\theta\, B$ of Hermitian $A$ and $B$ is positive definite, the pencil is still diagonalizable by congruence with real eigenvalues. The Crawford number $\min_{\|x\|_2 = 1} |x^* (A + iB) x|$ measures how definite it is.
- **Nonsymmetric**: complex eigenvalues, infinite eigenvalues and Jordan structure are all possible. Solved densely by QZ and, for a few eigenvalues of a large pencil, by [implicitly restarted Arnoldi](/implicitly-restarted-arnoldi/) on $(A - \sigma B)^{-1} B$, or by Jacobi-Davidson.
- **Singular pencils.** If $\det(A - \lambda B) \equiv 0$, the Kronecker canonical form has blocks of non-square shape as well as finite and infinite Jordan blocks. The problem is ill-posed: arbitrarily small changes can put eigenvalues anywhere. Algorithms such as GUPTRI first split off the singular part.
- **Polynomial eigenvalue problems.** $(\lambda^2 M + \lambda C + K) x = 0$ and higher degrees reduce to a generalized problem of order $dn$ by linearization (see Reductions).
- **A few eigenvalues near a target.** Spectral transformation with shift $\sigma$ maps the eigenvalues near $\sigma$ to the largest eigenvalues $1 / (\lambda - \sigma)$ of $(A - \sigma B)^{-1} B$.

## Examples

**A symmetric definite 2 by 2.** Let $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ and $B = \begin{pmatrix} 2 & 0 \\ 0 & 1 \end{pmatrix}$. Then $\det(A - \lambda B) = (2 - 2\lambda)(2 - \lambda) - 1 = 2\lambda^2 - 6\lambda + 3$, with roots $\lambda = (3 \pm \sqrt 3)/2$, that is $2.3660$ and $0.6340$. The Cholesky factor of $B$ is $L = \operatorname{diag}(\sqrt 2, 1)$, and $C = L^{-1} A L^{-*} = \begin{pmatrix} 1 & 1/\sqrt 2 \\ 1/\sqrt 2 & 2 \end{pmatrix}$. It has trace 3 and determinant $3/2$, hence the same characteristic polynomial $\lambda^2 - 3\lambda + 3/2$. They are not the eigenvalues 3 and 1 of $A$.

**An infinite eigenvalue.** Let $A = \begin{pmatrix} 1 & 2 \\ 0 & 3 \end{pmatrix}$ and $B = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$. Then $\det(A - \lambda B) = 3(1 - \lambda)$ has degree 1, so the pencil is regular with the finite eigenvalue 1 (eigenvector $e_1$) and one infinite eigenvalue. In pair form the eigenvalues are $(\alpha, \beta) = (1, 1)$ and $(3, 0)$, read off the diagonals of the already triangular $S = A$ and $T = B$. The infinite eigenvector $x$ satisfies $B x = 0$: $x = e_2$.

**A singular pencil.** Let $A = B = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$. Then $\det(A - \lambda B) = 0$ for every $\lambda$, and $x = e_2$ satisfies $A x = \lambda B x$ for all $\lambda$. Change the $(2, 2)$ entries to $\varepsilon a$ in $A$ and $\varepsilon b$ in $B$, with $b \ne 0$. The new pencil is regular with eigenvalues 1 and $a / b$, for every $\varepsilon \ne 0$. So perturbations of any small size can produce any second eigenvalue.

**A quadratic problem.** For scalars, $\lambda^2 + 3\lambda + 2 = 0$ has roots $-1$ and $-2$. The linearization $\begin{pmatrix} 0 & 1 \\ -2 & -3 \end{pmatrix} z = \lambda z$ with $z = (x, \lambda x)$ is the companion matrix, with trace $-3$ and determinant 2, as expected.

## Known algorithms

| algorithm | input | cost (leading term) | status of the count |
|---|---|---|---|
| Hessenberg-triangular reduction | general pencil | about $8n^3$ flops without $Q$ and $Z$ (GVL 7.7) | count for the Householder and Givens version |
| [QZ algorithm](/qz-algorithm/) (Moler and Stewart 1973) | general pencil | about $30n^3$ flops for eigenvalues, more than $60n^3$ with $Q$ and $Z$ (GVL 7.7) | typical, assumes about 2 QZ steps per eigenvalue as observed |
| Cholesky reduction (Martin and Wilkinson 1968) and a [symmetric solver](/symmetric-eigenproblem/) | symmetric definite | $n^3/3$ for $B = L L^*$, about $n^3$ to form $C = L^{-1} A L^{-*}$, $4n^3/3$ for [tridiagonalization](/tridiagonalization/), $O(n^2)$ for eigenvalues: about $8n^3/3$ | exact counts for the dense phases |
| [Lanczos](/lanczos-algorithm/) in the $B$-inner product, shift and invert | large sparse symmetric definite | one product with $A$ and one solve with $B$ or $A - \sigma B$ per step | depends on the spectrum |
| [Implicitly restarted Arnoldi](/implicitly-restarted-arnoldi/) on $(A - \sigma B)^{-1} B$ | large sparse | one factorization of $A - \sigma B$, then one solve per step | depends on the spectrum |
| LOBPCG, Jacobi-Davidson, contour integral methods | large sparse | products and inexact solves | depends on the spectrum |

The QZ count is a flop count times an observed number of iterations; no theorem bounds the number of QZ iterations, just as for the QR algorithm.

## Bounds

- **No finite algorithm.** The case $B = I$ contains the standard problem, so the Abel-Ruffini obstruction applies: no finite sequence of arithmetic operations and radicals solves every pencil with $n \ge 5$.
- **Input size.** Every entry of $A$ and $B$ can affect an eigenvalue, so $\Omega(n^2)$ operations are needed. The dense methods use $O(n^3)$.
- **Accuracy.** QZ is backward stable in the sense above. The forward error of a simple eigenvalue follows from the first-order formula $\delta\lambda \approx y^* (E - \lambda F) x / (y^* B x)$ for unit $x$ and $y$; see the [eigenvalue condition number](/eigenvalue-condition-number/). Large and infinite eigenvalues are better measured in the chordal metric $|\alpha \hat\beta - \beta \hat\alpha| / (\sqrt{|\alpha|^2 + |\beta|^2} \sqrt{|\hat\alpha|^2 + |\hat\beta|^2})$, in which they are often well conditioned (Stewart and Sun, Chapter VI).
- **Cholesky reduction.** For the symmetric definite pencil, the computed $C$ is close to $L^{-1} A L^{-*}$ with errors of order $u\, \|A\|_2 \|B^{-1}\|_2$. When $B$ is ill conditioned the method can lose accuracy that QZ keeps, and the loss depends on the problem; GVL 8.7 discusses examples.

## Reductions

- **Standard to generalized.** Take $B = I$.
- **Generalized to standard, by inversion.** If $B$ is nonsingular, $A x = \lambda B x$ is the standard problem for $B^{-1} A$. Forming $B^{-1} A$ costs $O(n^3)$ and adds errors of order $u\, \kappa_2(B)$, and it destroys symmetry. Use it only when $B$ is well conditioned.
- **Symmetric definite to symmetric standard.** With $B = L L^*$, the problem is $C y = \lambda y$ with $C = L^{-1} A L^{-*}$ and $x = L^{-*} y$.
- **Shift and invert.** For $\sigma$ not an eigenvalue, $A x = \lambda B x$ is equivalent to $(A - \sigma B)^{-1} B x = \theta x$ with $\theta = 1 / (\lambda - \sigma)$. Infinite eigenvalues map to $\theta = 0$.
- **Polynomial to generalized.** $(\lambda^2 M + \lambda C + K) x = 0$ is equivalent to $\begin{pmatrix} 0 & I \\ -K & -C \end{pmatrix} z = \lambda \begin{pmatrix} I & 0 \\ 0 & M \end{pmatrix} z$ with $z = (x, \lambda x)$, a pencil of order $2n$. Singular $M$ gives infinite eigenvalues.
- **Generalized singular values.** The generalized SVD of $(A, B)$ gives the eigenvalues of the symmetric semidefinite pencil $A^* A - \lambda B^* B$ without forming the products.

## Applications

- **Vibration analysis.** Undamped vibration of a structure leads to $K x = \omega^2 M x$ with symmetric stiffness $K$ and positive definite mass $M$, often from the [finite element method](/finite-element-method/). Damping gives a quadratic problem.
- **Statistics and machine learning.** [Linear discriminant analysis](/linear-discriminant-analysis/) solves $S_b w = \lambda S_w w$, and [canonical correlation analysis](/canonical-correlation-analysis/) is also a symmetric definite pencil. The normalized cut in [spectral clustering](/spectral-clustering/) uses $L x = \lambda D x$ with the graph Laplacian $L$ and degree matrix $D$.
- **Quantum chemistry.** The Roothaan-Hall equations $F c = \varepsilon S c$ have a positive definite overlap matrix $S$.
- **Control and descriptor systems.** Systems $E \dot x = A x + B u$ with singular $E$ lead to pencils $A - \lambda E$ with infinite eigenvalues.

## References
