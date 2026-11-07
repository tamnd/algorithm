---
tag: J1RF7H
kind: definition
slug: positive-definite-matrix
name: Positive definite matrix
aliases:
- SPD matrix
- symmetric positive definite matrix
- positive semidefinite matrix
area: numerical/linear-systems
level: intro
summary: A symmetric matrix with x^T A x > 0 for every nonzero x.
prereqs: [eigenvalue]
see_also: [cholesky-decomposition, conjugate-gradient-method, schur-complement, diagonally-dominant-matrix, hilbert-matrix, spectral-theorem, normal-equations, minres]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Chapter 7, Positive definite and semidefinite matrices (Section 7.1, definitions and properties; Section 7.2, characterizations, including the leading principal minors and the Cholesky factorization)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 4.2, Positive Definite Systems (the properties used by the algorithms, the bound on the off-diagonal entries, and the Cholesky factorization)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 10, Cholesky Factorization (Section 10.1, symmetric positive definite matrices, Theorem 10.1 on the existence of the factorization)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 23, Cholesky Factorization (Hermitian positive definite matrices and their properties)
---

A real *symmetric positive definite* (SPD) matrix is a symmetric $n \times n$ matrix $A$ with $x^T A x > 0$ for each nonzero vector $x$. These matrices are the matrices of the [Cholesky decomposition](/cholesky-decomposition/) and of the [conjugate gradient method](/conjugate-gradient-method/): for them, Gaussian elimination needs no pivoting, is backward stable, and costs half as much, and the solution of $A x = b$ minimizes a convex quadratic. They arise as covariance matrices, as the [normal equations](/normal-equations/) $A^T A$ of a full-rank least squares problem, and as stiffness matrices of finite element methods.

## Definition

Let $A \in \mathbb{R}^{n \times n}$ with $A = A^T$. The matrix $A$ is

- *positive definite* when $x^T A x > 0$ for each $x \in \mathbb{R}^n$ with $x \ne 0$;
- *positive semidefinite* when $x^T A x \ge 0$ for each $x \in \mathbb{R}^n$;
- *negative definite* (or semidefinite) when $-A$ is positive definite (or semidefinite);
- *indefinite* when $x^T A x$ takes both signs.

The number $x^T A x$ is the *quadratic form* of $A$ at $x$. The symmetry is part of the definition on this page, as in numerical linear algebra. (A nonsymmetric $B$ with $x^T B x > 0$ for each $x \ne 0$ is sometimes also called positive definite; then only its symmetric part $(B + B^T)/2$ matters for the form, because $x^T B x = x^T \frac{B + B^T}{2} x$.) For complex matrices the same definitions use a Hermitian $A$ and $x^* A x$.

**Equivalent conditions.** For a symmetric $A$, the following are equivalent (Horn and Johnson, Sections 7.1 and 7.2; Higham, Theorem 10.1):

1. $A$ is positive definite.
2. Each eigenvalue of $A$ is positive.
3. $A = B^T B$ for some nonsingular $B$.
4. Each leading principal minor is positive: $\det A_k > 0$ for $k = 1, \ldots, n$, where $A_k$ is the leading $k \times k$ block (Sylvester's criterion).
5. $A$ has a Cholesky factorization $A = R^T R$ with $R$ upper triangular and $r_{jj} > 0$, and $R$ is unique.

*Proof of 1 ⇔ 2 ⇔ 3.* By the [spectral theorem](/spectral-theorem/), $A = Q \Lambda Q^T$ with $Q$ orthogonal and $\Lambda$ the diagonal of the eigenvalues. With $y = Q^T x$, $x^T A x = \sum_i \lambda_i y_i^2$, and $y$ runs over all nonzero vectors when $x$ does. So the form is positive for each nonzero $x$ exactly when each $\lambda_i > 0$. If 2 holds, $B = \Lambda^{1/2} Q^T$ is nonsingular and $B^T B = A$. If 3 holds, $x^T A x = \|Bx\|_2^2 > 0$ for $x \ne 0$, because $Bx \ne 0$. $\square$ The equivalence with 4 and 5 is proved on the page of the [Cholesky decomposition](/cholesky-decomposition/): the algorithm runs to completion exactly when each $\det A_k > 0$.

**Consequences.** Let $A$ be positive definite. Then:

- each principal submatrix $A(I, I)$ is positive definite (take $x$ zero outside $I$), so in particular $a_{ii} > 0$;
- $|a_{ij}| < \sqrt{a_{ii} a_{jj}}$ for $i \ne j$, from the $2 \times 2$ principal submatrix with positive determinant, so the largest entry in modulus is on the diagonal;
- $A^{-1}$ is positive definite, with eigenvalues $1/\lambda_i$;
- $X^T A X$ is positive definite for each $X \in \mathbb{R}^{n \times k}$ of rank $k$;
- each [Schur complement](/schur-complement/) $A_{22} - A_{21} A_{11}^{-1} A_{12}$ of a block partition is positive definite, which is why elimination without pivoting keeps positive pivots;
- $\|A\|_2 = \lambda_{\max}$ and $\kappa_2(A) = \lambda_{\max}/\lambda_{\min}$, where $\lambda_{\max}$ and $\lambda_{\min}$ are the largest and smallest eigenvalues;
- $\langle x, y \rangle_A = x^T A y$ is an inner product, and $\|x\|_A = (x^T A x)^{1/2}$ is a norm, the *energy norm* in which the conjugate gradient method is optimal;
- $x_* = A^{-1} b$ is the unique minimizer of $\phi(x) = \frac12 x^T A x - b^T x$, because $\phi(x) - \phi(x_*) = \frac12 (x - x_*)^T A (x - x_*)$.

## Examples and non-examples

**A $2 \times 2$ example.** $A = \begin{pmatrix} 4 & 2 \\ 2 & 3 \end{pmatrix}$ is positive definite: $x^T A x = 4 x_1^2 + 4 x_1 x_2 + 3 x_2^2 = (2 x_1 + x_2)^2 + 2 x_2^2$, which is zero only for $x = 0$. The leading minors are $4$ and $8$. The eigenvalues are $(7 \pm \sqrt{17})/2 \approx 5.5616$ and $1.4384$. The Cholesky factor is $R = \begin{pmatrix} 2 & 1 \\ 0 & \sqrt 2 \end{pmatrix}$, and the sum of squares above is $\|R x\|_2^2$.

**The second difference matrix.** The tridiagonal $T_n = \operatorname{tridiag}(-1, 2, -1)$ of order $n$ has eigenvalues $2 - 2\cos(k\pi/(n+1))$, $k = 1, \ldots, n$, all positive, and leading minors $\det T_k = k + 1$. For $n = 4$ the eigenvalues are about $0.3820$, $1.3820$, $2.6180$ and $3.6180$, so $\kappa_2(T_4) \approx 9.4721$. In general $\kappa_2(T_n) \approx 4(n+1)^2/\pi^2$, which is why the model Poisson problem gets harder to solve iteratively as the grid is refined.

**The Hilbert matrix.** The [Hilbert matrix](/hilbert-matrix/) $H_n = (1/(i + j - 1))$ is positive definite for each $n$, because $x^T H_n x = \int_0^1 (\sum_i x_i t^{i-1})^2 \, dt$. It is also very ill conditioned: $\kappa_2(H_{12}) \approx 1.7 \times 10^{16}$. Positive definite does not mean well conditioned.

**A Gram matrix.** For $B \in \mathbb{R}^{m \times n}$ of full column rank, $B^T B$ is positive definite by condition 3. If the rank is less than $n$, $B^T B$ is only semidefinite.

**Non-example: positive entries.** $\begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$ has positive entries but eigenvalues $3$ and $-1$, so it is indefinite: at $x = (1, -1)^T$ the form is $-2$. Its determinant is $-3$.

**Non-example: positive diagonal and positive eigenvalues of a nonsymmetric matrix.** $\begin{pmatrix} 1 & 4 \\ 0 & 1 \end{pmatrix}$ has both eigenvalues equal to $1$, but at $x = (1, -1)^T$ the form is $1 - 4 + 1 = -2$. Without symmetry, condition 2 does not imply condition 1.

**Non-example: singular semidefinite.** $\begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix} = (1, 2)^T (1, 2)$ is positive semidefinite, with eigenvalues $5$ and $0$, and is not positive definite: the form vanishes at $x = (2, -1)^T$.

**A sufficient test.** A symmetric matrix with a positive diagonal that is strictly [diagonally dominant](/diagonally-dominant-matrix/) is positive definite, because by the [Gershgorin circle theorem](/gershgorin-circle-theorem/) each eigenvalue lies in a disc $|\lambda - a_{ii}| \le \sum_{j \ne i} |a_{ij}| < a_{ii}$ on the positive axis. The converse fails: $T_n$ is positive definite and only weakly dominant.

**Testing in floating point.** The practical test is to run the Cholesky decomposition and see whether it completes. Computing all eigenvalues costs several times more, and the leading minors are a by-product of the same elimination, so they add nothing. A matrix within a few units of roundoff of a singular matrix can pass or fail either way, so the test answers the question for a nearby matrix, not always for the stored one.

## Related definitions

- [Cholesky decomposition](/cholesky-decomposition/): the factorization $A = R^T R$ that exists exactly for positive definite $A$.
- [Schur complement](/schur-complement/): the matrix that elimination leaves; it is positive definite when $A$ is.
- [Diagonally dominant matrix](/diagonally-dominant-matrix/): a sufficient condition, with a positive diagonal and symmetry.
- [Condition number](/condition-number/): for a positive definite matrix, $\kappa_2 = \lambda_{\max}/\lambda_{\min}$.
- [Conjugate gradient method](/conjugate-gradient-method/): the Krylov method for positive definite systems; [MINRES](/minres/) handles symmetric indefinite ones.
- [Eigenvalue](/eigenvalue/): condition 2 is a statement about the spectrum.

## References
