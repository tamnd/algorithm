---
tag: WEYTHZ
kind: theorem
slug: spectral-theorem
name: Spectral theorem
aliases:
- real spectral theorem
- symmetric Schur decomposition
- spectral theorem for Hermitian matrices
- principal axis theorem
area: numerical/eigenproblems
level: intro
summary: A real symmetric matrix is A = Q Λ Qᵀ with Q orthogonal and Λ real diagonal, so it has real eigenvalues and an orthonormal basis of eigenvectors. A Hermitian matrix is A = Q Λ Q* with Q unitary.
prereqs: [eigenvalue, eigenvector, similarity-transformation]
see_also: [symmetric-eigenproblem, schur-decomposition, rayleigh-quotient, courant-fischer-theorem, weyls-inequality, singular-value-decomposition, positive-definite-matrix, diagonalization]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 2.5, Normal matrices (the spectral theorems for normal, Hermitian and real symmetric matrices)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.1, Properties and Decompositions (the symmetric Schur decomposition)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 1, Basic Facts about Self-Adjoint Matrices
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 24, Eigenvalue Problems (unitary diagonalization and normal matrices)
  - paper: "Thomas Hawkins, Cauchy and the spectral theory of matrices, Historia Mathematica 2, 1975"
    title: Thomas Hawkins, Cauchy and the spectral theory of matrices
    locator: pp. 1 to 29 (Cauchy's 1829 proof that the characteristic roots of a real symmetric matrix are real)
---

The spectral theorem says that each real symmetric matrix $A$ can be written $A = Q \Lambda Q^T$ with $Q$ orthogonal and $\Lambda$ real and diagonal. So $A$ has $n$ real [eigenvalues](/eigenvalue/) and an orthonormal basis of [eigenvectors](/eigenvector/), the columns of $Q$, and it is diagonalized by an orthogonal [similarity transformation](/similarity-transformation/). The same holds for a complex Hermitian matrix with a unitary $Q$, and a complex matrix is unitarily diagonalizable exactly when it is normal. The theorem is the base of the [symmetric eigenproblem](/symmetric-eigenproblem/), of the [Rayleigh quotient](/rayleigh-quotient/) bounds, and of the [singular value decomposition](/singular-value-decomposition/).

## Statement

**Notation.** $A^*$ is the conjugate transpose, $A^T$ the transpose. For a real symmetric or complex Hermitian $A$ of order $n \ge 1$ we order the eigenvalues as $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_n$.

**Theorem (real form).** Let $A \in \mathbb R^{n \times n}$ with $A^T = A$. Then there are a real orthogonal matrix $Q$ ($Q^T Q = I$) and a real diagonal matrix $\Lambda = \operatorname{diag}(\lambda_1, \dots, \lambda_n)$ such that

$$A = Q \Lambda Q^T, \qquad \text{that is,} \qquad A = \sum_{i=1}^{n} \lambda_i q_i q_i^T,$$

where $q_i$ is column $i$ of $Q$ and $A q_i = \lambda_i q_i$. The order of the $\lambda_i$ can be chosen freely. Conversely, each matrix $Q \Lambda Q^T$ with $Q$ real orthogonal and $\Lambda$ real diagonal is symmetric.

**Theorem (complex form).** Let $A \in \mathbb C^{n \times n}$ with $A^* = A$. Then $A = Q \Lambda Q^*$ with $Q$ unitary and $\Lambda$ real diagonal.

**Theorem (normal matrices).** A matrix $A \in \mathbb C^{n \times n}$ is $A = Q \Lambda Q^*$ with $Q$ unitary and $\Lambda$ diagonal (complex) if and only if $A^* A = A A^*$.

## In plain words

A symmetric table of numbers acts on space in a very simple way. There are as many special directions as the size of the table, all at right angles to each other, and along each one the table only stretches or shrinks by a real factor. If you turn your axes to these directions, the table becomes a list of stretch factors on the diagonal, with zeros everywhere else. Tables that are not symmetric can have stretch directions that are not at right angles, too few of them, or no real ones at all.

## Proof

We prove the complex form; the real form is the same proof with real vectors, and we mark the one extra step.

*Step 1: the eigenvalues are real.* Let $A^* = A$ and $A v = \lambda v$ with $v \ne 0$. Then $v^* A v$ is a real number, because $\overline{v^* A v} = (v^* A v)^* = v^* A^* v = v^* A v$. Since $v^* A v = \lambda \, v^* v$ and $v^* v > 0$, $\lambda$ is real.

*Step 2: induction on $n$.* For $n = 1$, take $Q = (1)$ and $\Lambda = A$. Let $n \ge 2$ and assume the claim for order $n - 1$. The characteristic polynomial $\det(A - \lambda I)$ has degree $n$, so by the fundamental theorem of algebra it has a root $\lambda_1 \in \mathbb C$, which is real by step 1. Pick a unit vector $q_1$ with $A q_1 = \lambda_1 q_1$. In the real form, $A - \lambda_1 I$ is a real singular matrix, so $q_1$ can be taken real.

*Step 3: split off the eigenvector.* Extend $q_1$ to an orthonormal basis $q_1, w_2, \dots, w_n$ (apply Gram-Schmidt to $q_1, e_1, \dots, e_n$ and drop the zero vectors; in the real form all vectors stay real), and let $W = [w_2, \dots, w_n]$ and $Q_1 = [q_1, W]$, which is unitary. Then

$$Q_1^* A Q_1 = \begin{pmatrix} q_1^* A q_1 & q_1^* A W \\ W^* A q_1 & W^* A W \end{pmatrix} = \begin{pmatrix} \lambda_1 & 0 \\ 0 & A_2 \end{pmatrix}.$$

The $(2,1)$ block is $W^* (\lambda_1 q_1) = 0$ because $W^* q_1 = 0$. The $(1,2)$ block is $q_1^* A W = (A q_1)^* W = \lambda_1 q_1^* W = 0$, because $A^* = A$ and $\lambda_1$ is real. The $(1,1)$ entry is $\lambda_1 q_1^* q_1 = \lambda_1$. The block $A_2 = W^* A W$ of order $n - 1$ is Hermitian, since $(W^* A W)^* = W^* A W$.

*Step 4: finish.* By the induction hypothesis, $A_2 = Q_2 \Lambda_2 Q_2^*$ with $Q_2$ unitary and $\Lambda_2$ real diagonal. Let $Q = Q_1 \operatorname{diag}(1, Q_2)$, a product of unitary matrices. Then $Q^* A Q = \operatorname{diag}(1, Q_2^*) \operatorname{diag}(\lambda_1, A_2) \operatorname{diag}(1, Q_2) = \operatorname{diag}(\lambda_1, \Lambda_2)$. A permutation similarity puts the diagonal in any order.

*Converse.* $(Q \Lambda Q^T)^T = Q \Lambda^T Q^T = Q \Lambda Q^T$, since a diagonal matrix equals its transpose.

*Normal matrices.* If $A = Q \Lambda Q^*$ then $A^* A = Q \bar\Lambda \Lambda Q^* = Q \Lambda \bar\Lambda Q^* = A A^*$. For the other direction, write $A = Q T Q^*$ by the [Schur decomposition](/schur-decomposition/), with $T$ upper triangular. Then $T^* T = T T^*$. We show by induction on the row index that row $k$ of $T$ has no nonzero entry off the diagonal. The $(k, k)$ entry of $T^* T$ is $\sum_{i \le k} |t_{ik}|^2$, and that of $T T^*$ is $\sum_{j \ge k} |t_{kj}|^2$. The entries $t_{ik}$ with $i < k$ are zero by the induction hypothesis (they lie in earlier rows, off the diagonal). So $|t_{kk}|^2 = |t_{kk}|^2 + \sum_{j > k} |t_{kj}|^2$, and $t_{kj} = 0$ for $j > k$. Hence $T$ is diagonal. $\blacksquare$

**Orthogonality of eigenvectors, directly.** If $A^* = A$, $A x = \lambda x$ and $A y = \mu y$ with $\lambda \ne \mu$, then $\lambda \, y^* x = y^* A x = (A y)^* x = \mu \, y^* x$ (using that $\mu$ is real), so $y^* x = 0$.

## Consequences

- **Rayleigh quotient bounds.** For $x \ne 0$, $\rho(x) = x^* A x / x^* x$ satisfies $\lambda_n \le \rho(x) \le \lambda_1$; write $x$ in the basis $q_i$ to see it. This leads to the [Courant-Fischer theorem](/courant-fischer-theorem/), [Cauchy interlacing](/cauchy-interlacing-theorem/) and [Weyl's inequality](/weyls-inequality/), so the eigenvalues of a symmetric matrix move by at most $\|E\|_2$ under a symmetric perturbation $E$.
- **Positive definiteness.** A symmetric $A$ is [positive definite](/positive-definite-matrix/) if and only if all $\lambda_i > 0$, because $x^T A x = \sum_i \lambda_i (q_i^T x)^2$.
- **Functions of a matrix.** $f(A) = Q f(\Lambda) Q^T$ defines $A^{1/2}$, $e^{A}$ and $A^{-1}$ by acting on the eigenvalues, and $\|A\|_2 = \max_i |\lambda_i|$.
- **The singular value decomposition.** Applying the theorem to $A^T A$ gives the [SVD](/singular-value-decomposition/) of any real matrix.
- **Algorithms.** Every method of the [symmetric eigenproblem](/symmetric-eigenproblem/) computes an approximation of $Q$ and $\Lambda$: the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/) by plane rotations, and the [QR algorithm](/qr-algorithm/) after [tridiagonalization](/tridiagonalization/).

## Tightness

Each hypothesis is needed.

- **Real but not symmetric.** $\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$ has eigenvalues $\pm i$, so it has no real eigenvector. $\begin{pmatrix} 1 & 1 \\ 0 & 2 \end{pmatrix}$ has the real eigenvalues $1$ and $2$, but its eigenvectors $(1, 0)^T$ and $(1, 1)^T$ make an angle of $45$ degrees, so no orthogonal $Q$ diagonalizes it. $\begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$ cannot be diagonalized at all.
- **Complex symmetric but not Hermitian.** $A = \begin{pmatrix} 1 & i \\ i & -1 \end{pmatrix}$ satisfies $A^T = A$, but $A^2 = 0$ and $A \ne 0$, so its only eigenvalue is $0$ and it is not diagonalizable. The transpose must be the conjugate transpose.
- **Distinct eigenvalues are not needed, but the basis is not unique.** For $A = I$ every orthogonal $Q$ works. When an eigenvalue is repeated, only the eigenspace is determined, not the vectors.

**Examples.** $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ has $\lambda_1 = 3$, $q_1 = (1, 1)^T / \sqrt 2$ and $\lambda_2 = 1$, $q_2 = (1, -1)^T / \sqrt 2$, so $A = 3 q_1 q_1^T + q_2 q_2^T$. The matrix $\begin{pmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{pmatrix}$ has eigenvalues $2 + \sqrt 2$, $2$, $2 - \sqrt 2$ with unit eigenvectors $(1, -\sqrt 2, 1)^T / 2$, $(1, 0, -1)^T / \sqrt 2$, $(1, \sqrt 2, 1)^T / 2$, which are pairwise orthogonal.

## History

Cauchy proved in 1829 that the characteristic roots of a real symmetric matrix are real, in a paper on the secular perturbations of the planets; Hawkins (1975) traces this work and its role in the later spectral theory.

## References
