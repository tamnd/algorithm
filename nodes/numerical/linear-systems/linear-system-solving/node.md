---
tag: DKZGV6
kind: problem
slug: linear-system-solving
name: Solving linear systems
aliases:
- Linear system solving
- solving Ax = b
- system of linear equations
- linear equation solving
area: numerical/linear-systems
level: intro
summary: Given a square matrix A and vector b, find x with Ax = b.
model: floating-point-model
complexity:
  vars: {n: "the order of A, at least 1"}
  time: {worst: O(n^3)}
  flops: {worst: "2n^3/3 + O(n^2)"}
prereqs: [floating-point-model, condition-number, backward-error-analysis]
see_also: [gaussian-elimination, lup-decomposition, partial-pivoting, cholesky-decomposition, least-squares-problem, conjugate-gradient-method, gmres, sparse-linear-systems]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 7, Perturbation Theory for Linear Systems (Theorem 7.1, the Rigal and Gaches normwise backward error; Theorem 7.2, the normwise forward error bound; Theorem 7.3, the Oettli and Prager componentwise backward error); Chapter 9, LU Factorization and Linear Equations (Theorem 9.4 and the growth factor in Section 9.4)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 2.6, The Sensitivity of Square Systems; Chapter 3, General Linear Systems (Sections 3.1 to 3.5); Chapter 11, Large Sparse Linear System Problems
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 12, Conditioning and Condition Numbers; Lectures 20 to 22, Gaussian Elimination, Pivoting and Stability of Gaussian Elimination
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Chapter 2, Linear Equation Solving (Section 2.2, Perturbation Theory; Section 2.4, Error Analysis)
  - paper: doi:10.1145/321075.321076
    title: J. H. Wilkinson, Error analysis of direct methods of matrix inversion, Journal of the ACM 8(3), 1961
    locator: pp. 281 to 330 (the backward error analysis of Gaussian elimination and the bound 2^(n-1) on the growth with partial pivoting)
  - paper: "J. L. Rigal and J. Gaches, On the compatibility of a given solution with the data of a linear system, Journal of the ACM 14(3), 1967"
    locator: pp. 543 to 548 (the normwise backward error of an approximate solution)
---

Solving a linear system means: given an $n \times n$ real matrix $A$ and a vector $b$, find the vector $x$ with $A x = b$. In exact arithmetic the answer exists and is unique exactly when $A$ is nonsingular, and [Gaussian elimination](/gaussian-elimination/) finds it. In [floating-point arithmetic](/floating-point-model/) no method returns $x$ exactly, so the numerical problem is to return an $\hat x$ that is the exact solution of a nearby system (a small *backward error*); the distance from $\hat x$ to $x$ then depends on the [condition number](/condition-number/) $\kappa(A)$. This page fixes the notation that all pages of this area use.

## In plain words

You have as many equations as unknowns, each equation a weighted sum of the unknowns, and you want the values that make all equations true. With exact fractions, school elimination gives the answer. A computer stores each number with a fixed number of digits and rounds after each step, so the answer it gives is a little wrong.

Two questions then matter. The first is about the method: is the computed answer the exact answer of a system whose numbers differ from yours only by rounding? A method with this property is called stable. The second is about the system: does a tiny change of its numbers move the answer a lot? Such a system is called ill-conditioned, and no method can fix that. A stable method on a well-conditioned system gives an answer that is correct to almost all stored digits.

## Definition

**Notation used on all pages of this area.** $A$ is an $n \times n$ real matrix ($m \times n$ when it is rectangular), $b \in \mathbb{R}^n$ is the right side, $x$ is the exact solution and $\hat x$ the computed one. The [residual](/residual/) is $r = b - A \hat x$. A norm $\|\cdot\|$ is a vector norm and the [matrix norm](/matrix-norms/) that it induces; $|A|$ is the matrix of the absolute values $|a_{ij}|$, and inequalities between matrices hold entry by entry. The condition number is $\kappa(A) = \|A\| \, \|A^{-1}\|$, and $\kappa_p$ names the norm. The unit roundoff is $u$ ($u = 2^{-53} \approx 1.11 \times 10^{-16}$ in IEEE binary64), and $\gamma_n = n u / (1 - n u)$ for $n u < 1$. The growth factor of elimination is $\rho_n$ (see [growth factor](/growth-factor/)). For an iterative method, $x_k$ is the iterate after $k$ steps, $r_k = b - A x_k$, $\mathcal{K}_k(A, b) = \operatorname{span}\{b, A b, \ldots, A^{k-1} b\}$ is the [Krylov subspace](/krylov-subspace/), and a stationary method $x_{k+1} = G x_k + c$ has iteration matrix $G$ with [spectral radius](/spectral-radius/) $\rho(G)$. Costs are counted in flops: one flop is one floating-point addition, subtraction, multiplication or division.

**The exact problem.** Input: $A \in \mathbb{R}^{n \times n}$ and $b \in \mathbb{R}^n$. Output: $x \in \mathbb{R}^n$ with $A x = b$, or the report that $A$ is singular. The solution exists and is unique for each $b$ if and only if $\det A \neq 0$.

**The floating-point problem.** The input is $A$ and $b$ with floating-point entries, and the output is $\hat x$. Two measures of quality are used.

- The *normwise backward error* of $\hat x$ is
$$\eta(\hat x) = \min\{\varepsilon : (A + \Delta A) \hat x = b + \Delta b,\ \|\Delta A\| \le \varepsilon \|A\|,\ \|\Delta b\| \le \varepsilon \|b\|\}.$$
Rigal and Gaches (1967) proved that $\eta(\hat x) = \|r\| / (\|A\| \, \|\hat x\| + \|b\|)$ (Higham, Theorem 7.1). So the backward error can be computed from the residual. A solver is *normwise backward stable* if $\eta(\hat x) \le c_n u$ for each input, with $c_n$ a modest function of $n$.
- The *forward error* is $\|x - \hat x\| / \|x\|$.

**Forward error from backward error.** Assume $(A + \Delta A) \hat x = b + \Delta b$ with $\|\Delta A\| \le \varepsilon \|A\|$, $\|\Delta b\| \le \varepsilon \|b\|$ and $\varepsilon \kappa(A) < 1$, and $x \ne 0$. Then
$$\frac{\|x - \hat x\|}{\|x\|} \le \frac{2 \varepsilon \kappa(A)}{1 - \varepsilon \kappa(A)}.$$
*Proof.* Subtract $A x = b$ to get $A(\hat x - x) = \Delta b - \Delta A \, \hat x$, so $\|\hat x - x\| \le \|A^{-1}\| (\varepsilon \|b\| + \varepsilon \|A\| \, \|\hat x\|)$. Use $\|b\| \le \|A\| \, \|x\|$ and $\|\hat x\| \le \|x\| + \|\hat x - x\|$. This gives $\|\hat x - x\| \le \varepsilon \kappa(A) (2 \|x\| + \|\hat x - x\|)$, and the claim follows when $\varepsilon \kappa(A) < 1$. $\square$ This is Higham, Theorem 7.2, in a slightly weaker form. To first order, some perturbations of relative size $\varepsilon$ reach a forward error of $\varepsilon \kappa(A)$, so for a backward stable solver the forward error is of the order of $\kappa(A) u$ in the worst case, and no algorithm that works on rounded data can promise better.

**Componentwise backward error.** Oettli and Prager (1964) proved that the smallest $\omega$ with $(A + \Delta A)\hat x = b + \Delta b$, $|\Delta A| \le \omega |A|$, $|\Delta b| \le \omega |b|$ is $\omega = \max_i |r_i| / (|A| \, |\hat x| + |b|)_i$, with $0/0$ read as $0$ (Higham, Theorem 7.3). It is the right measure when $A$ has zeros or entries of very different sizes.

## Variants

- **Special matrices.** Triangular ([back substitution](/back-substitution/), $n^2$ flops), symmetric positive definite ([Cholesky decomposition](/cholesky-decomposition/), $n^3/3$ flops), banded ([banded matrix](/banded-matrix/)), tridiagonal ([tridiagonal system solving](/tridiagonal-system-solving/), $O(n)$ flops), Toeplitz ([Levinson-Durbin recursion](/levinson-durbin-recursion/), $O(n^2)$ flops) and diagonally dominant ([diagonally dominant matrix](/diagonally-dominant-matrix/), no pivoting needed).
- **Sparse systems.** $A$ has few nonzeros, and the cost is measured in nonzeros and fill; see [sparse linear systems](/sparse-linear-systems/) and [fill-in](/fill-in/).
- **Many right sides.** $A X = B$ with $B \in \mathbb{R}^{n \times k}$. Factor once, then each column costs $2 n^2$ flops.
- **Rectangular systems.** For $m > n$ an exact solution usually does not exist, and the [least squares problem](/least-squares-problem/) asks for $\min_x \|b - A x\|_2$. For $m < n$ one asks for the solution of least norm.
- **Exact solution.** Over $\mathbb{Q}$ or a finite field the algebra is the same, but the costs are in bit operations or field operations; see [LU decomposition](/lu-decomposition/) and [Gaussian elimination](/gaussian-elimination/).
- **Approximate solution to a tolerance.** Iterative methods stop when $\|r_k\| \le \text{tol} \cdot \|b\|$ or a similar test holds; the output is then good only to the tolerance.

## Examples

**A small pivot.** Let $A = \begin{pmatrix} 10^{-20} & 1 \\ 1 & 1 \end{pmatrix}$ and $b = (1, 2)^T$ in binary64. The exact solution is $x_1 = 1/(1 - 10^{-20})$, $x_2 = (1 - 2 \cdot 10^{-20})/(1 - 10^{-20})$, both equal to $1$ to about 20 digits, and $\kappa_\infty(A) \approx 4$. Elimination without a row swap computes the multiplier $10^{20}$, then $1 - 10^{20}$ rounds to $-10^{20}$, and the result is $\hat x = (0, 1)$: the first entry is wrong in all digits. With [partial pivoting](/partial-pivoting/) the rows are swapped first, and the result is $\hat x = (1, 1)$. The system is well-conditioned; the first method is unstable.

**An ill-conditioned system.** Let $H_8$ be the $8 \times 8$ [Hilbert matrix](/hilbert-matrix/) with entries $1/(i + j - 1)$, rounded to binary64, and let $b$ be the sum of its columns, rounded. Then $\kappa_\infty(H_8) \approx 3.39 \times 10^{10}$. Elimination with partial pivoting gives an $\hat x$ with normwise backward error $\eta_\infty(\hat x) \approx 2.6 \times 10^{-17}$, below $u$, but with forward error $\|x - \hat x\|_\infty / \|x\|_\infty \approx 2.3 \times 10^{-7}$ against the exact solution $x$ of the stored system. The bound $\kappa_\infty(H_8) u \approx 3.8 \times 10^{-6}$ covers this. The method is stable; the loss of nine digits comes from the matrix.

**A singular matrix.** For $A = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$ the second row is twice the first. Elimination meets a zero pivot, and the problem has no solution for $b = (1, 0)^T$ and infinitely many for $b = (1, 2)^T$. In floating point a matrix that is singular only after rounding can give a tiny pivot instead of a zero one, so a solver reports a near-singular matrix by an estimate of $\kappa(A)$ (see [Hager's condition estimator](/hagers-condition-estimator/)), not by a test for exact zero.

## Known algorithms

- **Dense direct methods.** [LUP decomposition](/lup-decomposition/) with [partial pivoting](/partial-pivoting/) costs $2n^3/3 + O(n^2)$ flops and is the default; it satisfies $(A + \Delta A)\hat x = b$ with $|\Delta A| \le \gamma_{3n} |\hat L| |\hat U|$ (Higham, Theorem 9.4). [Complete pivoting](/complete-pivoting/) adds $\Theta(n^3)$ comparisons and has a much smaller worst-case growth. [Cholesky decomposition](/cholesky-decomposition/) costs $n^3/3$ flops for symmetric positive definite $A$ and needs no pivoting. QR by [Householder reflections](/householder-reflections/) costs $4n^3/3$ flops and is backward stable with no growth factor.
- **Improving a computed solution.** [Iterative refinement](/iterative-refinement/) reuses the factors to reduce the error, and in mixed precision it gives a forward error of order $u$ when $\kappa(A) u$ is small enough.
- **Structured and sparse direct methods.** The [Thomas algorithm](/thomas-algorithm/) for tridiagonal systems, [cyclic reduction](/cyclic-reduction/), band LU in $O(n p q)$ flops, and sparse Cholesky or LU after a [fill-reducing ordering](/fill-reducing-ordering/), organized by the [elimination tree](/elimination-tree/).
- **Stationary iterations.** The [Jacobi method](/jacobi-method/), the [Gauss-Seidel method](/gauss-seidel-method/) and [successive over-relaxation](/successive-over-relaxation/) converge for each start exactly when $\rho(G) < 1$.
- **Krylov methods.** The [conjugate gradient method](/conjugate-gradient-method/) for symmetric positive definite $A$, [GMRES](/gmres/), [BiCG](/biconjugate-gradient/) and [BiCGSTAB](/bicgstab/) for general $A$; each step costs one or two products with $A$. They are used with [preconditioning](/preconditioning/), for example [incomplete LU](/incomplete-lu-factorization/) or [algebraic multigrid](/algebraic-multigrid/).
- **Multilevel and parallel methods.** [Multigrid](/multigrid-method/) solves model elliptic problems in $O(n)$ flops; [domain decomposition](/domain-decomposition/) splits the problem for parallel machines.

## Bounds

- **Upper bound on arithmetic.** Elimination uses $\Theta(n^3)$ flops. With fast matrix multiplication, Bunch and Hopcroft (1974) solve a nonsingular system in $O(n^\omega)$ arithmetic operations, where $\omega < 2.372$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/). In floating point these fast methods are stable only in a weaker normwise sense, and they are not used in standard libraries.
- **Lower bound.** A dense system has $n^2 + n$ inputs, and each one can change $x$, so each algorithm reads all of them: $\Omega(n^2)$ operations.
- **Accuracy.** Gaussian elimination with partial pivoting is backward stable when the growth factor $\rho_n$ is small: $\|\Delta A\|_\infty$ is at most a small multiple of $n^2 \gamma_{3n} \rho_n \|A\|_\infty$ (Higham, Theorem 9.5). The worst case $\rho_n = 2^{n-1}$ is proved and attained (Wilkinson 1961); in practice $\rho_n$ is small, and for random matrices it grows like a small power of $n$ (Trefethen and Schreiber 1990, an observed result). A forward error of order $\kappa(A) u$ is the best that a backward stable method can guarantee, by the bound in the definition.
- **Memory traffic.** On current machines the cost of a dense solve is set by the transfer of data between memory and the processor more than by the flop count. Blocked algorithms (LAPACK) do most of the work as matrix-matrix products for this reason.

## Reductions

- **Inversion and solving.** With the inverse, $x = A^{-1} b$ costs $2n^2$ flops; with a solver, the inverse is the solution of $A X = I$ ($n$ solves). Computing $A^{-1}$ to solve a system costs about three times as much as LU ($2n^3$ flops against $2n^3/3$), and the residual of $\hat x = A^{-1} b$ can be larger than that of an LU solve by a factor of order $\kappa(A)$ (Higham, Chapter 14). Matrix multiplication and inversion have the same exponent; see [matrix multiplication and inversion equivalence](/matrix-multiplication-inversion-equivalence/).
- **Least squares to a square system.** $\min \|b - A x\|_2$ reduces to the [normal equations](/normal-equations/) $A^T A x = A^T b$, but $\kappa_2(A^T A) = \kappa_2(A)^2$, so QR is used instead.
- **Eigenvectors to solves.** [Inverse iteration](/inverse-iteration/) finds an eigenvector by repeated solves with $A - \mu I$.

## Applications

- Discretized partial differential equations, for example the [Poisson equation](/poisson-equation/) by [finite differences](/finite-difference-method/) or [finite elements](/finite-element-method/), give large sparse systems.
- Newton's method for nonlinear equations solves one linear system for each step.
- Data fitting and [linear regression](/linear-regression/) lead to least squares problems.
- Circuit simulation, structural analysis and interior point methods of optimization solve a sequence of sparse systems.

## References
