---
tag: 85HPNN
kind: theorem
slug: ostrowski-reich-theorem
name: Ostrowski-Reich theorem
aliases:
- SOR convergence theorem
- Householder-John theorem (general splitting form)
area: numerical/linear-systems
level: advanced
summary: SOR converges for symmetric positive definite A when 0 < omega < 2.
prereqs: [successive-over-relaxation, positive-definite-matrix, spectral-radius]
see_also: [gauss-seidel-method, jacobi-method, matrix-splitting, richardson-iteration, conjugate-gradient-method, diagonally-dominant-matrix]
sources:
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 4.2, Convergence (convergence of SOR and of splittings for symmetric positive definite matrices)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 11.2, The Classical Iterations (Gauss-Seidel and SOR for symmetric positive definite matrices)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 6.5, Basic Iterative Methods (the convergence theorems for Jacobi, Gauss-Seidel and SOR, including the symmetric positive definite case)
  - paper: doi:10.1090/S0002-9947-1954-0059635-7
    title: David M. Young, Iterative methods for solving partial difference equations of elliptic type, Transactions of the American Mathematical Society 76, 1954
    locator: the convergence of successive over-relaxation and the role of positive definiteness
---

The Ostrowski-Reich theorem says that for a symmetric matrix $A$ with positive diagonal, [successive over-relaxation](/successive-over-relaxation/) with parameter $0 < \omega < 2$ converges for every starting vector if and only if $A$ is positive definite. In particular Gauss-Seidel ($\omega = 1$) converges for every symmetric positive definite matrix, with no further condition such as diagonal dominance. The proof is an energy argument that works for any splitting $A = M - N$ with $M + M^T - A$ positive definite.

## Statement

**Notation.** $A \in \mathbb{C}^{n \times n}$ is Hermitian, written $A = D - E - E^*$ with $D$ block diagonal and $E$ strictly block lower triangular (point SOR is the case of $1 \times 1$ blocks). For $\omega \ne 0$, $M_\omega = D/\omega - E$, $N_\omega = M_\omega - A$, and the SOR iteration matrix is $G_\omega = M_\omega^{-1} N_\omega = I - M_\omega^{-1} A$, with [spectral radius](/spectral-radius/) $\rho(G_\omega)$. The iterates satisfy $e_{k+1} = G_\omega e_k$ for the error $e_k = x_k - x$.

**Theorem (Ostrowski-Reich).** Let $A$ be Hermitian with $D$ Hermitian positive definite, and let $0 < \omega < 2$. Then $\rho(G_\omega) < 1$ if and only if $A$ is positive definite.

**Lemma (general splitting, Householder-John form).** Let $A = M - N$ be Hermitian with $M$ nonsingular, and suppose $Q = M + M^* - A = M^* + N$ is Hermitian positive definite. Then $\rho(M^{-1} N) < 1$ if and only if $A$ is positive definite.

The theorem is the lemma with $M = M_\omega$, since $M_\omega + M_\omega^* - A = \big(\tfrac{2}{\omega} - 1\big) D$, which is positive definite exactly for $0 < \omega < 2$.

## In plain words

For a symmetric problem with positive diagonal, over-relaxation with any factor strictly between zero and two settles down from every starting guess exactly when the matrix is positive definite. The reason is that each sweep lowers an energy, the quadratic form of the matrix applied to the error, by a definite amount, and energy that keeps dropping and cannot go below zero must drain away. If the matrix is not positive definite, some error has negative energy, and the same drop then pushes it further from zero forever.

## Proof

We prove the lemma; the theorem follows as explained above. Note that $M_\omega$ is block lower triangular with diagonal blocks of $D/\omega$, so it is nonsingular.

Let $P = M^{-1} A$, so $G = M^{-1} N = I - P$. A direct expansion gives the identity
$$A - G^* A G = P^* A + A P - P^* A P = A M^{-*} A + A M^{-1} A - A M^{-*} A M^{-1} A = A M^{-*}\,(M + M^* - A)\,M^{-1} A = (M^{-1}A)^* Q\, (M^{-1} A).$$
(The middle step uses $A M^{-*} A = A M^{-*} M M^{-1} A$ and $A M^{-1} A = A M^{-*} M^* M^{-1} A$.)

**If $A$ is positive definite.** Then $A$ is nonsingular, so $M^{-1} A$ is nonsingular and $A - G^* A G$ is positive definite. Let $G v = \lambda v$ with $v \ne 0$. Then
$$v^* A v - (G v)^* A (G v) = (1 - |\lambda|^2)\, v^* A v = (M^{-1} A v)^* Q\, (M^{-1} A v) > 0.$$
Since $v^* A v > 0$, $|\lambda| < 1$. Hence $\rho(G) < 1$.

**If $\rho(G) < 1$.** Then $1$ is not an eigenvalue of $G$, so $P = I - G$ is nonsingular and so is $A = M P$. Hence $A - G^* A G$ is positive definite. For $v \ne 0$, telescoping gives
$$v^* A v = \sum_{j=0}^{k-1} \big((G^j v)^* A\, G^j v - (G^{j+1} v)^* A\, G^{j+1} v\big) + (G^k v)^* A\, G^k v \ge v^*(A - G^* A G) v + (G^k v)^* A\, G^k v,$$
because every term of the sum is nonnegative. As $k \to \infty$, $G^k v \to 0$, so $v^* A v \ge v^*(A - G^* A G) v > 0$. Hence $A$ is positive definite. $\blacksquare$

## Consequences

- **Gauss-Seidel.** For $\omega = 1$, $Q = D$: Gauss-Seidel, point or block, converges for every Hermitian positive definite matrix.
- **Energy decrease.** With $\|v\|_A^2 = v^* A v$, the proof shows $\|e_k\|_A^2 - \|e_{k+1}\|_A^2 = \|M^{-1} A e_k\|_Q^2 > 0$ whenever $e_k \ne 0$. So for SPD $A$ each SOR sweep decreases the $A$-norm of the error; this is why Gauss-Seidel is the method of coordinate descent on $\tfrac12 x^T A x - b^T x$.
- **Jacobi.** For Jacobi, $M = D$ and $Q = 2D - A$. So Jacobi converges for SPD $A$ if and only if $2D - A$ is also positive definite. For $A = \begin{pmatrix} 1 & a & a \\ a & 1 & a \\ a & a & 1 \end{pmatrix}$, $A$ is positive definite for $-\tfrac12 < a < 1$ but $2D - A$ only for $-1 < a < \tfrac12$. At $a = 0.8$ the Jacobi eigenvalues are $-1.6, 0.8, 0.8$ and Jacobi diverges, while Gauss-Seidel converges with observed rate $0.708$ per sweep, and SOR converges in 68, 88 and 495 sweeps for $\omega = 1, 1.5, 1.9$ to a residual of $10^{-10}$.
- **SSOR and other splittings.** The lemma applies to SSOR, to block versions, and to [Richardson iteration](/richardson-iteration/) with $M = I/\omega$, where $Q = \tfrac{2}{\omega} I - A$ is positive definite exactly when $\omega < 2/\lambda_{\max}$.
- **Indefinite systems.** For symmetric indefinite $A$ with positive diagonal, SOR diverges for every $\omega \in (0, 2)$ and some starting vector: $\begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$ is an example.

The theorem gives convergence, not a rate: $\rho(G_\omega)$ can be arbitrarily close to $1$, and for the Poisson model problem it is $1 - O(h^2)$ for Gauss-Seidel. The optimal $\omega$ needs Young's theory of consistently ordered matrices. The theorem concerns exact arithmetic; in floating point the iterates stall near a residual of order $u\,\|A\|\,\|x\|$, $u = 2^{-53}$, which is observed rather than part of the statement.

## Tightness

- **The range of $\omega$.** For every matrix $\det G_\omega = (1 - \omega)^n$, so $\rho(G_\omega) \ge |1 - \omega|$ (Kahan); for $\omega \notin (0, 2)$ SOR fails even for $A = I$, where $G_\omega = (1 - \omega) I$. So $(0, 2)$ cannot be enlarged, and as $\omega \to 0$ or $\omega \to 2$ the rate degrades to $1$.
- **Symmetry is needed.** $A = \begin{pmatrix} 1 & 3 \\ -3 & 1 \end{pmatrix}$ has positive definite symmetric part $I$, yet Gauss-Seidel has $G_1 = \begin{pmatrix} 0 & -3 \\ 0 & -9 \end{pmatrix}$ and $\rho(G_1) = 9$.
- **A positive diagonal is needed for the converse.** For $A = -I$, $D = -I$ and $G_1 = 0$, so Gauss-Seidel converges in one sweep, yet $A$ is negative definite. With a zero diagonal entry SOR is not even defined.
- **Positive definite $A$ is not needed for convergence in general.** Nonsymmetric matrices, such as strictly diagonally dominant ones, can make SOR converge; the theorem characterizes only the Hermitian case.

## History

Reich (1949) proved that Gauss-Seidel converges for symmetric positive definite matrices, and Ostrowski (1954) extended the result to SOR with $0 < \omega < 2$, including the converse. Young's 1954 paper proved convergence in the same setting for his analysis of over-relaxation, and Kahan's 1958 thesis gave the necessary condition $|1 - \omega| < 1$. The general splitting form, often attributed to Householder and to John, is the version in modern texts.

## References
