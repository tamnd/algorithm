---
tag: EJVWX4
kind: concept
slug: matrix-splitting
name: Matrix splitting
aliases:
- stationary iterative method framework
- splitting A = M - N
- regular splitting
area: numerical/linear-systems
level: core
summary: Write A = M - N and iterate x_{k+1} = M^-1(N x_k + b) to get stationary methods.
prereqs: [spectral-radius, linear-system-solving]
see_also: [jacobi-method, gauss-seidel-method, successive-over-relaxation, richardson-iteration, ostrowski-reich-theorem, preconditioning, neumann-series, multigrid-method]
sources:
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 4.1, Jacobi, Gauss-Seidel and SOR; Section 4.2, Convergence (4.2.1 general convergence result, 4.2.2 regular splittings, 4.2.3 diagonally dominant matrices, 4.2.4 symmetric positive definite matrices)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 17, Stationary Iterative Methods (forward and backward error analysis of the splitting iteration in floating point; Section 17.5, stopping an iterative method)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 11.2, The Classical Iterations (splittings, the iteration matrix, convergence for diagonally dominant and symmetric positive definite matrices)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 6.5, Basic Iterative Methods (splittings, convergence of Jacobi, Gauss-Seidel and SOR on the model problem)
---

A matrix splitting writes the coefficient matrix of $A x = b$ as $A = M - N$, with $M$ nonsingular and easy to solve with. The equation becomes $M x = N x + b$, and the *stationary iteration* $M x_{k+1} = N x_k + b$ repeats it. The Jacobi, Gauss-Seidel, SOR, SSOR and Richardson methods are all instances, and they differ only in the choice of $M$. The iteration converges for every start exactly when the spectral radius of the iteration matrix $G = M^{-1} N$ is below one.

## In plain words

Split the matrix into a part that is easy to solve with and a remainder. Guess a solution, move the remainder to the right side using the guess, and solve the easy part. That gives a new guess, and you repeat. If the easy part holds most of the matrix, each step removes a fixed share of the error and the guesses settle on the answer. If the remainder is too big, the error can grow instead. One number, read off the matrix of a single step, tells which case you are in.

## The idea

**Notation.** $A \in \mathbb{R}^{n \times n}$ is nonsingular, $x = A^{-1} b$ is the exact solution, $x_k$ is the $k$-th iterate, $e_k = x - x_k$ its error and $r_k = b - A x_k = A e_k$ its residual. Norms are as on the page [matrix norms](/matrix-norms/), and $\rho$ is the [spectral radius](/spectral-radius/). The general notation of this area is on the page [linear system solving](/linear-system-solving/).

**The iteration.** With $A = M - N$,

$$x_{k+1} = M^{-1}(N x_k + b) = G x_k + M^{-1} b, \qquad G = M^{-1} N = I - M^{-1} A.$$

The same step in residual form is $x_{k+1} = x_k + M^{-1} r_k$, which is how it is coded: compute the residual, solve once with $M$, update. In this form $M^{-1}$ acts as an approximate inverse, which is the link to [preconditioning](/preconditioning/): the stationary iteration is [Richardson iteration](/richardson-iteration/) on the preconditioned system $M^{-1} A x = M^{-1} b$.

**The error equation.** The exact solution is a fixed point, $x = G x + M^{-1} b$. Subtracting gives

$$e_{k+1} = G e_k, \qquad e_k = G^k e_0, \qquad r_k = (N M^{-1})^k r_0.$$

**Convergence (proved).** The iteration converges to $x$ for every $x_0$ and every $b$ if and only if $\rho(G) < 1$ (Saad, Section 4.2.1). This follows from the fact that $G^k \to 0$ exactly when $\rho(G) < 1$, proved on the page [spectral radius](/spectral-radius/). A sufficient condition is $\|G\| < 1$ in some induced norm, and then $\|e_k\| \le \|G\|^k \|e_0\|$ and $\|e_k\| \le \frac{\|G\|}{1 - \|G\|}\|x_k - x_{k-1}\|$, which is a computable stopping test. In the long run the error shrinks by about $\rho(G)$ per step, so about $-1/\log_{10}\rho(G)$ steps are needed for each decimal digit. For a nonnormal $G$ the first steps can be much worse than $\rho(G)^k$.

**When $\rho(G) < 1$ is guaranteed.** Write $A = D - E - F$ with $D$ diagonal, $-E$ the strictly lower and $-F$ the strictly upper part.

- *Strictly diagonally dominant $A$* (by rows). For Jacobi, $\|D^{-1}(E + F)\|_\infty < 1$, so Jacobi converges, and Gauss-Seidel converges as well (Saad, Section 4.2.3).
- *Symmetric positive definite $A$.* If $M + M^T - A$ is positive definite, then $\rho(M^{-1} N) < 1$; indeed $\|G\|_A < 1$ in the energy norm $\|v\|_A = (v^T A v)^{1/2}$. Gauss-Seidel has $M + M^T - A = D$, so it always converges. SOR with $0 < \omega < 2$ has $M + M^T - A = (2/\omega - 1) D$, which gives the [Ostrowski-Reich theorem](/ostrowski-reich-theorem/). Jacobi has $M + M^T - A = 2D - A$, which need not be positive definite, so Jacobi can fail on an SPD matrix.
- *Regular splittings.* If $M^{-1} \ge 0$ and $N \ge 0$ entrywise, the splitting is *regular*. For such a splitting, $\rho(M^{-1} N) < 1$ if and only if $A^{-1} \ge 0$, and then $\rho(M^{-1} N) = \rho(A^{-1} N)/(1 + \rho(A^{-1} N))$ (Saad, Section 4.2.2; the theory goes back to Varga's Matrix Iterative Analysis, 1962). This covers the Jacobi and Gauss-Seidel splittings of an M-matrix, and the comparison theorem built on it says that of two regular splittings of the same such $A$, the one with the entrywise smaller $N$ has the smaller or equal spectral radius.

**Cost.** One step costs one product with $N$ (or with $A$, in residual form), about $2\,\mathrm{nnz}(A)$ flops, plus one solve with $M$. For Jacobi the solve is $n$ divisions; for Gauss-Seidel and SOR it is a [triangular solve](/triangular-system-solving/) with the lower part of $A$, again about $2\,\mathrm{nnz}(A)$ flops in total for the sweep. Storage is $\mathrm{nnz}(A) + O(n)$. A sweep does about one flop per byte of matrix data loaded, so on current machines it runs at the speed of memory, not of the floating-point units. Gauss-Seidel and SOR are sequential across rows unless the unknowns are colored; Jacobi is fully parallel.

**Floating point.** In floating point the iteration does not reach the exact solution. Higham, Chapter 17, bounds the error of the computed iterates in terms of $u$, $\rho(G)$ and the size of $|M^{-1}|(|M| + |N|)$, and shows that the limiting forward error can be well above $u\,\kappa(A)$ when $G$ is far from normal (proved bounds; on many matrices the observed limit is near $u\,\kappa(A)$). Section 17.5 discusses stopping tests based on the residual.

## Examples

**Jacobi and Gauss-Seidel on a small diagonally dominant matrix.** Take

$$A = \begin{pmatrix} 4 & -1 & 0 \\ -1 & 4 & -1 \\ 0 & -1 & 4 \end{pmatrix}, \qquad b = \begin{pmatrix} 3 \\ 2 \\ 3 \end{pmatrix}, \qquad x = \begin{pmatrix} 1 \\ 1 \\ 1 \end{pmatrix}.$$

Jacobi uses $M = D = 4I$, so $G_J = \frac14 \operatorname{tridiag}(1, 0, 1)$ with eigenvalues $\frac12 \cos(k\pi/4)$, and $\rho(G_J) = \sqrt2/4 \approx 0.354$. Gauss-Seidel uses $M = D - E$ and has $\rho(G_{GS}) = \rho(G_J)^2 = 1/8$. From $x_0 = 0$ the Jacobi iterates are $(0.75, 0.5, 0.75)$, $(0.875, 0.875, 0.875)$, $(0.96875, 0.9375, 0.96875)$, and the Gauss-Seidel iterates are $(0.75, 0.6875, 0.921875)$, $(0.921875, 0.9609375, 0.990234375)$, $(0.990234375, 0.995117\ldots, 0.998779\ldots)$. To reach a max-norm error below $10^{-10}$, Jacobi takes $23$ steps and Gauss-Seidel $12$. The predictions $10/(-\log_{10}\rho)$ are $22.1$ and $11.1$ steps.

**Jacobi converges and Gauss-Seidel diverges.** For

$$A = \begin{pmatrix} 1 & 2 & -2 \\ 1 & 1 & 1 \\ 2 & 2 & 1 \end{pmatrix},$$

the Jacobi matrix has characteristic polynomial $\lambda^3$, so $\rho(G_J) = 0$ and Jacobi gives the exact solution after three steps in exact arithmetic. The Gauss-Seidel matrix has characteristic polynomial $\lambda(\lambda - 2)^2$, so $\rho(G_{GS}) = 2$ and Gauss-Seidel diverges.

**Gauss-Seidel converges and Jacobi diverges.** For

$$A = \begin{pmatrix} 2 & -1 & 1 \\ 2 & 2 & 2 \\ -1 & -1 & 2 \end{pmatrix},$$

the Jacobi matrix has characteristic polynomial $\lambda^3 + \frac54 \lambda$, with eigenvalues $0$ and $\pm i\sqrt5/2$, so $\rho(G_J) = \sqrt5/2 \approx 1.118$. The Gauss-Seidel matrix has $\lambda(\lambda + \frac12)^2$, so $\rho(G_{GS}) = 1/2$. Neither method is better in general; the two examples are why the comparison needs hypotheses such as an M-matrix or a consistent ordering.

**The family of classical methods.** With $A = D - E - F$:

| Method | $M$ | $G = M^{-1} N$ |
|---|---|---|
| [Richardson](/richardson-iteration/) | $\alpha^{-1} I$ | $I - \alpha A$ |
| [Jacobi](/jacobi-method/) | $D$ | $D^{-1}(E + F)$ |
| [Gauss-Seidel](/gauss-seidel-method/) | $D - E$ | $(D - E)^{-1} F$ |
| [SOR](/successive-over-relaxation/) | $\omega^{-1} D - E$ | $(D - \omega E)^{-1}((1 - \omega) D + \omega F)$ |
| SSOR | $\frac{1}{\omega(2 - \omega)} (D - \omega E) D^{-1} (D - \omega F)$ | the product of a forward and a backward SOR sweep |
| Block Jacobi | the block diagonal of $A$ | as Jacobi, by blocks |

An incomplete factorization $M = \tilde L \tilde U \approx A$ (see [incomplete LU](/incomplete-lu-factorization/)) also defines a splitting, and so does one cycle of a [multigrid method](/multigrid-method/), whose iteration matrix is the two-grid or multigrid error operator.

## Where it is used

- **Smoothers in multigrid.** Damped Jacobi and Gauss-Seidel reduce the oscillatory part of the error quickly even when $\rho(G)$ is close to one; a [multigrid method](/multigrid-method/) uses a few sweeps as its smoother.
- **Preconditioners for Krylov methods.** The matrix $M$ of a splitting is used as a [preconditioner](/preconditioning/) for the [conjugate gradient method](/conjugate-gradient-method/) or [GMRES](/gmres/); the Krylov method then chooses better combinations of the iterates than the fixed recurrence.
- **Iterative refinement.** [Iterative refinement](/iterative-refinement/) is the splitting iteration with $M = \hat L \hat U$, the computed LU factors, and $N = \hat L \hat U - A$.
- **Fixed-point analysis.** The [Neumann series](/neumann-series/) $A^{-1} = \sum_k G^k M^{-1}$, valid when $\rho(G) < 1$, is the closed form of the iteration started at $x_0 = 0$.
- **Theory of the classical methods.** The comparison of Jacobi, Gauss-Seidel and SOR on consistently ordered matrices, and the optimal SOR parameter, are statements about the spectra of these iteration matrices.

## References
