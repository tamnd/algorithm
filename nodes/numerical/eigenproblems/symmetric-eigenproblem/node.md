---
tag: XPJ7C2
kind: problem
slug: symmetric-eigenproblem
name: Symmetric eigenproblem
aliases:
- Hermitian eigenproblem
- symmetric eigenvalue problem
- real symmetric eigenproblem
area: numerical/eigenproblems
level: core
summary: Compute all eigenvalues and eigenvectors of a real symmetric or complex Hermitian matrix. The eigenvalues are real and perfectly conditioned, and the eigenvectors are orthonormal.
model: floating-point-model
complexity:
  vars: {n: "the order of A"}
  time: {worst: O(n^3)}
  flops: {values: "4 n^3 / 3", qr_with_vectors: "9 n^3", mrrr_with_vectors: "10 n^3 / 3"}
prereqs: [spectral-theorem, eigenvalue-problem, weyls-inequality]
see_also: [tridiagonalization, tridiagonal-eigenproblem, qr-algorithm, divide-and-conquer-eigensolver, mrrr-algorithm, jacobi-eigenvalue-algorithm, lanczos-algorithm, singular-value-decomposition]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.1 (properties and perturbation theory), Section 8.3 (the symmetric QR algorithm and its flop counts), Section 8.4 (more methods for tridiagonal problems), Section 8.5 (Jacobi methods)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 26 (reduction to Hessenberg or tridiagonal form), Lectures 27 to 30 (Rayleigh quotient, QR algorithm, other eigenvalue algorithms)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 5.2 (perturbation theory), Section 5.3 (algorithms for the symmetric eigenproblem and the comparison of their costs), Section 5.4.3 (Jacobi and high relative accuracy)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics edition, 1998
    locator: Chapter 1 (basic facts), Chapter 4 and Chapter 10 (residual bounds and the Kato-Temple inequality), Chapter 8 (the QL and QR algorithms)
  - paper: "J. Demmel and K. Veselić, Jacobi's method is more accurate than QR, SIAM Journal on Matrix Analysis and Applications 13, 1992"
    title: Jacobi's method is more accurate than QR
    locator: SIAM J. Matrix Anal. Appl. 13(4) (1992), pp. 1204 to 1245
  - paper: "Inderjit S. Dhillon and Beresford N. Parlett, Multiple representations to compute orthogonal eigenvectors of symmetric tridiagonal matrices, Linear Algebra and its Applications 387, 2004"
    title: Multiple representations to compute orthogonal eigenvectors of symmetric tridiagonal matrices
    locator: Linear Algebra Appl. 387 (2004), pp. 1 to 28
---

The symmetric eigenproblem asks for the eigenvalues and eigenvectors of a real symmetric matrix $A = A^T$ or a complex Hermitian matrix $A = A^*$. By the [spectral theorem](/spectral-theorem/) the answer always exists in the cleanest possible form, $A = V \Lambda V^*$ with $V$ unitary and $\Lambda$ real diagonal, and the problem is far better behaved than the [nonsymmetric eigenproblem](/nonsymmetric-eigenproblem/): every eigenvalue moves by at most $\|E\|_2$ under a symmetric perturbation $E$, the Rayleigh quotient of an approximate eigenvector is accurate to second order, and there are no Jordan blocks. Dense solvers first reduce $A$ to tridiagonal form by an orthogonal similarity in $4n^3/3$ flops, then solve the [tridiagonal eigenproblem](/tridiagonal-eigenproblem/) in $O(n^2)$ flops for the eigenvalues, and use $O(n^3)$ more flops for the eigenvectors.

## In plain words

A symmetric table of numbers is one that reads the same across as down. For such a table there is always a set of directions at right angles to each other along which the table only stretches or shrinks, with no twisting. The stretch amounts are ordinary real numbers, and they barely move when the table is nudged a little, which makes them easy to compute accurately. The directions are harder when two stretch amounts are very close, because then a tiny nudge can turn the directions a lot. Good programs first squeeze the table into a thin band and then work on the band.

## Definition

**Notation.** $A \in \mathbb C^{n \times n}$ with $A = A^*$ (for real $A$, $A = A^T$ and all the matrices below are real). The eigenvalues are ordered $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_n$ with orthonormal eigenvectors $v_1, \dots, v_n$. $\rho(x) = x^* A x / x^* x$ is the [Rayleigh quotient](/rayleigh-quotient/) and $u$ is the unit roundoff. The gap of $\lambda_i$ is $\mathrm{gap}_i = \min_{j \ne i} |\lambda_i - \lambda_j|$.

**Exact problem.** Find $\Lambda = \operatorname{diag}(\lambda_1, \dots, \lambda_n)$ and a unitary $V$ with $A V = V \Lambda$. The eigenvalues are unique; a simple eigenvalue has a unique eigenvector up to a factor $e^{i\phi}$, and a multiple eigenvalue of multiplicity $k$ has a unique $k$-dimensional eigenspace, in which any orthonormal basis will do.

**Floating-point problem.** Return $\hat\lambda_1, \dots, \hat\lambda_n$ and, if asked, $\hat V$ such that

$$\hat V \operatorname{diag}(\hat\lambda) \hat V^* = A + E, \qquad E = E^*, \qquad \|E\|_2 \le c(n) \, u \, \|A\|_2, \qquad \|\hat V^* \hat V - I\|_2 \le c(n) \, u,$$

with $c(n)$ a modest polynomial, in practice of order $n$. This is what the standard dense algorithms deliver. By Weyl's inequality it gives $|\hat\lambda_i - \lambda_i| \le c(n) u \|A\|_2$ for every $i$ with no further hypothesis; small eigenvalues may still lose relative accuracy. Variants ask for a subset only: the eigenvalues in an interval $[a, b)$, or those with indices $i \le k$, or the $k$ largest of a large sparse matrix.

## Variants

- **Eigenvalues only, or eigenvalues and eigenvectors.** The former costs $4n^3/3 + O(n^2)$ flops after tridiagonalization; the latter needs the orthogonal factor of the reduction and the tridiagonal eigenvectors.
- **A subset of the spectrum.** [Bisection](/bisection-eigenvalue-algorithm/) with the [Sturm count](/sturm-sequence-eigenvalue-count/) finds the eigenvalues in an interval at $O(n)$ flops per count, and [MRRR](/mrrr-algorithm/) or [inverse iteration](/inverse-iteration/) gives their eigenvectors at $O(n)$ flops each.
- **Banded matrices.** Reduction from bandwidth $b$ to tridiagonal form costs $O(n^2 b)$ flops by bulge chasing (Schwarz, Kaufman), avoiding the dense $n^3$ term.
- **Large sparse matrices.** Only products $x \mapsto A x$ are available; the [Lanczos algorithm](/lanczos-algorithm/) with restarting, [subspace iteration](/subspace-iteration/) or LOBPCG find a few extreme eigenpairs, using the [Rayleigh-Ritz method](/rayleigh-ritz-method/) on a subspace.
- **The definite generalized problem.** $A x = \lambda B x$ with $A$ Hermitian and $B$ Hermitian [positive definite](/positive-definite-matrix/) reduces to a standard one through the Cholesky factor $B = L L^*$, giving $L^{-1} A L^{-*}$ (see the [generalized eigenvalue problem](/generalized-eigenvalue-problem/)).
- **High relative accuracy.** For a positive definite $A = D H D$ with $D$ diagonal and $H$ having unit diagonal, Jacobi's method computes every eigenvalue with relative error of order $u \, \kappa_2(H)$, which can be far smaller than the $u \, \kappa_2(A)$ of QR (Demmel and Veselić 1992).

## Examples

**A $3 \times 3$ matrix.** $A = \begin{pmatrix} 2 & 1 & 0 \\ 1 & 3 & 1 \\ 0 & 1 & 4 \end{pmatrix}$ has eigenvalues $3 + \sqrt 3 = 4.7321$, $3$ and $3 - \sqrt 3 = 1.2679$, whose sum is the trace 9. The eigenvector for $3$ is $(1, 1, -1)^T / \sqrt 3$, since $(A - 3 I)(1, 1, -1)^T = 0$, and it is orthogonal to the other two, as the spectral theorem promises.

**Eigenvalues are stable, eigenvectors need a gap.** Let $A = \operatorname{diag}(1, 1 + \delta)$ with $\delta = 10^{-10}$ and $E = \begin{pmatrix} 0 & \epsilon \\ \epsilon & 0 \end{pmatrix}$ with $\epsilon = 10^{-10}$. The eigenvalues of $A + E$ are $1 + \delta/2 \pm (\delta^2/4 + \epsilon^2)^{1/2}$, so each moves by $\delta(\sqrt 5 - 1)/2 = 6.18 \times 10^{-11} \le \|E\|_2$, as Weyl's bound says. The eigenvectors rotate by $\tfrac12 \arctan(2\epsilon/\delta) = 31.7$ degrees, because the gap $\delta$ is as small as the perturbation. With $A = \operatorname{diag}(1, 2)$ and $\epsilon = 10^{-3}$ instead, the eigenvalues move by $9.99999 \times 10^{-7}$, which is $\epsilon^2 / \mathrm{gap}$: an off-diagonal perturbation moves a well separated eigenvalue only to second order.

**A multiple eigenvalue.** The identity has every unit vector as an eigenvector. Any algorithm returns some orthonormal basis, and any such basis is correct; comparing eigenvectors of two codes is only meaningful for simple eigenvalues, or as invariant subspaces.

## Known algorithms

| algorithm | output | flops (leading term) | status |
|---|---|---|---|
| [Householder tridiagonalization](/tridiagonalization/) | $A = Q T Q^*$, $T$ tridiagonal | $4n^3/3$, plus $4n^3/3$ to form $Q$ | exact count |
| symmetric tridiagonal QR with the [Wilkinson shift](/wilkinson-shift/) | all eigenvalues, optionally vectors | $O(n^2)$ for values; about $6n^3$ for vectors; $9n^3$ in total with the reduction (GVL Section 8.3) | typical; global convergence proved (Wilkinson 1968) |
| [dqds](/dqds-algorithm/) or Pal-Walker-Kahan QR | all eigenvalues | $O(n^2)$ | typical |
| [divide and conquer](/divide-and-conquer-eigensolver/) | all eigenpairs | at most about $4n^3/3$ on $T$, often far less by deflation, plus $2n^3$ to apply $Q$ | typical |
| [MRRR](/mrrr-algorithm/) | all or some eigenpairs | $O(n^2)$ for all, plus $2n^3$ to apply $Q$, so $10n^3/3$ in total | typical; orthogonality needs relative gaps (Dhillon and Parlett 2004) |
| [bisection](/bisection-eigenvalue-algorithm/) and [inverse iteration](/inverse-iteration/) | chosen eigenpairs | $O(n)$ per Sturm count, $O(n)$ per vector, plus reorthogonalization in clusters | proved for the values; clusters cost up to $O(n^3)$ |
| [Jacobi](/jacobi-eigenvalue-algorithm/) | all eigenpairs, high relative accuracy | $O(n^3)$ per sweep, typically 5 to 10 sweeps | quadratic convergence proved, sweep count typical |
| [Lanczos](/lanczos-algorithm/) and restarted variants | a few extreme eigenpairs | products with $A$ | rates depend on gaps (Kaniel-Paige-Saad bounds) |

The counts for QR, divide and conquer and MRRR assume the observed number of iterations, about two QR steps per eigenvalue for the symmetric tridiagonal QR algorithm; only the reduction counts are exact.

## Bounds

- **Weyl.** If $A$ and $E$ are Hermitian, $|\lambda_i(A + E) - \lambda_i(A)| \le \|E\|_2$ for every $i$ ([Weyl's inequality](/weyls-inequality/); GVL Section 8.1). The absolute condition number of every eigenvalue is 1.
- **Hoffman-Wielandt.** Under the same hypotheses, $\sum_i (\lambda_i(A + E) - \lambda_i(A))^2 \le \|E\|_F^2$ ([Hoffman-Wielandt theorem](/hoffman-wielandt-theorem/)).
- **Residual bounds.** For a unit vector $x$, $\rho = \rho(x)$ and $r = A x - \rho x$, there is an eigenvalue $\lambda_j$ with $|\lambda_j - \rho| \le \|r\|_2$. If moreover $\rho$ lies in an interval $(\alpha, \beta)$ that contains $\lambda_j$ and no other eigenvalue, then the Kato-Temple bound gives $-\|r\|_2^2 / (\beta - \rho) \le \lambda_j - \rho \le \|r\|_2^2 / (\rho - \alpha)$, which is quadratic in the residual (Parlett Chapter 10; for $A = \operatorname{diag}(0, 1)$, $x = (s, c)^T$ and $\alpha \to 0$ the upper bound is attained).
- **Eigenvectors.** If $\lambda_i$ is simple and $\delta = \min_{j \ne i} |\lambda_i(A) - \lambda_j(A + E)| > 0$, the eigenvector $\hat v_i$ of $A + E$ satisfies $\sin\angle(v_i, \hat v_i) \le \|E\|_2 / \delta$ ([Davis-Kahan theorem](/davis-kahan-theorem/)). The bound degrades as the gap closes, as the second example shows; for clusters, the invariant subspace of the whole cluster is well determined instead.
- **Backward stability.** Tridiagonalization by Householder reflectors and the tridiagonal QR algorithm together return the exact eigendecomposition of $A + E$ with $\|E\|_2 = O(n u) \|A\|_2$ in the worst-case analysis, and $\hat V$ orthogonal to $O(n u)$ (Wilkinson 1965 Chapter 3; GVL Section 8.3).
- **Lower bound on finite methods.** For $n \ge 5$ there is no finite formula in arithmetic operations and radicals: every polynomial with $n$ distinct real roots is the characteristic polynomial of a symmetric tridiagonal matrix whose entries are obtained from its coefficients by the Euclidean algorithm and square roots, and [Abel-Ruffini](/abel-ruffini-theorem/) excludes such formulas for the roots. So every method is iterative.

## Reductions

- **To the tridiagonal problem.** $A = Q T Q^*$ by [tridiagonalization](/tridiagonalization/); the eigenvalues of $T$ are those of $A$, and $V = Q V_T$. For complex Hermitian $A$, a diagonal unitary scaling makes $T$ real.
- **From the SVD and back.** The [singular values](/singular-value-decomposition/) of $B$ are the eigenvalues of the Hermitian matrix $\begin{pmatrix} 0 & B \\ B^* & 0 \end{pmatrix}$ up to sign; conversely the eigendecomposition of a positive semidefinite $A = B^* B$ is the SVD of $B$.
- **From the definite generalized problem.** By Cholesky, as above.
- **From the nonsymmetric problem.** Not in general; a nonsymmetric $A$ is similar to a symmetric matrix only when it is diagonalizable with real eigenvalues, and finding the similarity is as hard as the eigenproblem.

## Applications

Vibration and structural analysis (the normal modes of $K x = \omega^2 M x$), quantum mechanics (the Hamiltonian is Hermitian), [principal component analysis](/principal-component-analysis/) on the covariance matrix, [spectral clustering](/spectral-clustering/) and graph partitioning by the Laplacian, Gaussian quadrature (the Golub-Welsch algorithm reads the nodes off the eigenvalues of a Jacobi matrix), optimization (testing that a Hessian is [positive definite](/positive-definite-matrix/)), and the computation of the [SVD](/singular-value-decomposition/).

## References
