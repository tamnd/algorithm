---
tag: TNHD1V
kind: problem
slug: tridiagonal-system-solving
name: Tridiagonal system solving
aliases:
- tridiagonal linear systems
- solving a tridiagonal system
- GTSV
area: numerical/linear-systems
level: core
summary: Solve Ax = b where A has nonzeros only on the main and two adjacent diagonals.
model: floating-point-model
complexity:
  vars: {n: "the order of A, at least 1"}
  time: {worst: Θ(n)}
  flops: {worst: "8n - 7"}
prereqs: [linear-system-solving, banded-matrix]
see_also: [thomas-algorithm, cyclic-reduction, partial-pivoting, sherman-morrison-formula, cholesky-decomposition, givens-rotations, lanczos-algorithm, condition-number]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 9.6, Tridiagonal Matrices (LU without pivoting, its backward error, the classes of matrices for which it is componentwise stable, and partial pivoting with growth factor at most 2); Chapter 15, Condition Number Estimation (exact condition numbers of tridiagonal matrices in O(n) flops)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 4.3, Banded Systems (tridiagonal LU with and without pivoting, the symmetric positive definite tridiagonal case); Section 4.5, Block Tridiagonal Systems (block cyclic reduction)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 2.7.3, Band matrices; Section 6.3, the model problem in one dimension and the eigenvalues of tridiag(-1, 2, -1)
  - paper: doi:10.1137/0707049
    title: B. L. Buzbee, G. H. Golub and C. W. Nielson, On direct methods for solving Poisson's equations, SIAM Journal on Numerical Analysis 7(4), 1970
    locator: block cyclic reduction and its stable variant
---

A tridiagonal system is a linear system $A x = d$ in which $a_{ij} = 0$ whenever $|i - j| > 1$, so each equation couples an unknown with at most its two neighbors. Such systems come from one-dimensional differential equations, cubic splines, implicit time stepping and the Lanczos process. They are solved in $\Theta(n)$ time and storage, against $\Theta(n^3)$ for a dense matrix, because Gaussian elimination on a tridiagonal matrix creates no fill, and with pivoting it creates only one extra diagonal.

## In plain words

In many problems each unknown talks only to its left and right neighbor: a temperature at a point depends on the two points next to it, a spline segment on the two segments it joins. Writing all these conditions down gives a system with a very thin structure, three numbers per equation. Solving it is a walk down the chain and back, in time proportional to its length. The questions are whether the walk is safe without reordering the equations, how accurate the answer is, and how to split the walk across many processors.

## Definition

**Input.** The subdiagonal $a_2, \ldots, a_n$, the diagonal $b_1, \ldots, b_n$, the superdiagonal $c_1, \ldots, c_{n-1}$ and a right side $d \in \mathbb{R}^n$, defining

$$A = \begin{pmatrix} b_1 & c_1 & & \\ a_2 & b_2 & \ddots & \\ & \ddots & \ddots & c_{n-1} \\ & & a_n & b_n \end{pmatrix}.$$

**Output.** The solution $x$ of $A x = d$ if $A$ is nonsingular, and a report of singularity otherwise. In floating point, a computed $\hat x$ is judged by its backward error $\eta(\hat x)$ and its forward error $\|x - \hat x\|/\|x\|$, as on the page [linear system solving](/linear-system-solving/), with residual $r = d - A\hat x$, unit roundoff $u = 2^{-53}$, $\gamma_k = k u/(1 - k u)$ and $\kappa(A) = \|A\|\,\|A^{-1}\|$.

**Structure.** $A$ is *irreducible* if all $a_i$ and $c_i$ are nonzero. If some $a_i c_{i-1} = 0$, the problem splits into smaller tridiagonal problems (block triangular). If $a_i c_{i-1} > 0$ for all $i$, $A$ is similar by a diagonal matrix to a symmetric tridiagonal matrix, so its eigenvalues are real.

**The inverse.** For an irreducible nonsingular tridiagonal $A$, the inverse is dense, but it is *semiseparable*: there are vectors $p, q, s, t$ with $(A^{-1})_{ij} = p_i q_j$ for $i \le j$ and $s_i t_j$ for $i \ge j$. So $\|A^{-1}\|_1$ and $\kappa_1(A)$ can be computed exactly in $O(n)$ flops (Higham, Chapter 15), not just estimated.

## Variants

- **Symmetric positive definite.** $A = L D L^T$ with $L$ unit bidiagonal; no pivoting, about $4n$ flops for the factorization; LAPACK `xPTSV`.
- **Symmetric indefinite.** Symmetric pivoting with $1 \times 1$ and $2 \times 2$ blocks (Bunch's method) keeps symmetry and stability.
- **Diagonally dominant, M-matrix, totally nonnegative.** No pivoting is needed; see the [Thomas algorithm](/thomas-algorithm/).
- **Cyclic (periodic).** Nonzero corners $A_{1n}$ and $A_{n1}$; solved as a rank-one change of a tridiagonal matrix with the [Sherman-Morrison formula](/sherman-morrison-formula/).
- **Toeplitz tridiagonal.** $\operatorname{tridiag}(\alpha, \beta, \gamma)$ with constant diagonals has explicit eigenvalues $\beta + 2\sqrt{\alpha\gamma}\cos(k\pi/(n+1))$, and for $\alpha = \gamma$ the eigenvectors are sine vectors, so fast sine transforms solve it in $O(n \log n)$, and many such systems at once.
- **Block tridiagonal.** Blocks instead of scalars, from two- and three-dimensional grids ordered by lines; block LU, block cyclic reduction, or iterative methods.
- **Many right sides or many systems.** Factor once and solve many times at $5n$ flops each, or solve many independent systems in parallel, vectorized across systems.

## Examples

**The model problem.** $T_n = \operatorname{tridiag}(-1, 2, -1)$, from the second difference $-u''$ on $n$ interior grid points. Its eigenvalues are $2 - 2\cos(k\pi/(n+1))$, $k = 1, \ldots, n$, so it is symmetric positive definite with

$$\kappa_2(T_n) = \cot^2\!\left(\frac{\pi}{2(n+1)}\right) \approx \frac{4(n+1)^2}{\pi^2},$$

which is $48.4$ for $n = 10$, $4134$ for $n = 100$ and $4.06 \cdot 10^5$ for $n = 1000$. The Thomas algorithm gives pivots $u_i = (i+1)/i$ and a componentwise small backward error, so the forward error is at most about $u\,\kappa_2(T_n)$, tiny for all practical $n$.

**Cubic spline interpolation.** At knots $t_0 < \cdots < t_n$ with spacings $h_i$, the second derivatives $M_i$ of the natural cubic spline satisfy $h_i M_{i-1} + 2(h_i + h_{i+1}) M_i + h_{i+1} M_{i+1} = 6(\text{divided differences})$, a strictly diagonally dominant tridiagonal system.

**A system that needs pivoting.** $A = \begin{pmatrix} \varepsilon & 1 & 0 \\ 1 & 1 & 1 \\ 0 & 1 & 2 \end{pmatrix}$ with $\varepsilon = 10^{-12}$ has $\kappa_\infty(A) \approx 6$, computed exactly from its inverse. The leading pivot $\varepsilon$ is tiny relative to its column, so elimination without pivoting creates the multiplier $10^{12}$ and the pivot $1 - 10^{12}$, and the computed solution loses about twelve digits. Partial pivoting swaps rows 1 and 2, all multipliers are at most $1$ in magnitude, and the solution is accurate to working precision.

**A singular case.** $\operatorname{tridiag}(1, 2, 1)$ of order $n$ has $\det = n + 1$, but $\operatorname{tridiag}(-1, 2, -1)$ with the Neumann ends $b_1 = b_n = 1$ has the null vector $(1, \ldots, 1)$; the Thomas algorithm then ends with $u_n = 0$ and must report singularity.

## Known algorithms

- **[Thomas algorithm](/thomas-algorithm/).** Gaussian elimination without pivoting, $8n - 7$ flops, componentwise backward stable for diagonally dominant, symmetric positive definite, M-matrix and totally nonnegative matrices; it can break down otherwise.
- **Gaussian elimination with [partial pivoting](/partial-pivoting/).** LAPACK `xGTSV` and `xGTTRF`: a small multiple of $n$ flops, depending on the swaps, one extra superdiagonal in $U$, and a growth factor of at most $2$ (Higham, Section 9.6), so it is backward stable for every nonsingular tridiagonal matrix.
- **QR by [Givens rotations](/givens-rotations/).** $n - 1$ rotations triangularize $A$ into a band of upper width $2$ in $O(n)$ flops, a few times the cost of elimination; backward stable with no growth, and the basis of tridiagonal eigenvalue methods.
- **[Cyclic reduction](/cyclic-reduction/).** Eliminate the odd-numbered unknowns, which leaves a tridiagonal system of half the size, and recurse: about twice the flops of the Thomas algorithm and $O(\log n)$ parallel steps. It is stable for diagonally dominant matrices; for block systems from Poisson's equation, Buzbee, Golub and Nielson (1970) gave a stable variant.
- **Recursive doubling and partition methods.** Recursive doubling (Stone, 1973) writes the LU recurrence as a linear recurrence and evaluates it by parallel prefix; partition methods (Wang, 1981) and SPIKE split the matrix into $p$ blocks, solve them independently and couple them through a reduced system of size $O(p)$.
- **Iterative methods.** Rarely useful for a single tridiagonal system, since direct solution is linear time; tridiagonal solves are themselves the inner step of line relaxation and ADI.

## Bounds

- **Upper bound.** $8n - 7$ flops (Thomas) when no pivoting is needed, $O(n)$ with pivoting, and $O(n)$ storage.
- **Lower bound.** An algorithm correct for every irreducible tridiagonal matrix must read all $3n - 2$ entries and all of $d$, since each one changes the solution; so $\Omega(n)$ operations, and the direct methods are optimal up to a constant factor.
- **Parallel depth.** On $p = n$ processors, cyclic reduction and recursive doubling take $O(\log n)$ steps; since $x_1$ can depend on every $d_i$ and each operation has two inputs, $\Omega(\log n)$ steps are needed.
- **Accuracy.** A componentwise backward stable solver (as Thomas is on the classes above) gives $\|x - \hat x\|_\infty/\|x\|_\infty \lesssim c\,u\,\mathrm{cond}(A, x)$ with Skeel's condition number $\mathrm{cond}(A, x) = \|\,|A^{-1}||A||x|\,\|_\infty/\|x\|_\infty$, a proved bound that is often far smaller than $u\,\kappa_\infty(A)$.

## Reductions

- **A special case of banded systems.** Tridiagonal is [banded](/banded-matrix/) with $p = q = 1$; banded LU costs $O(n p q)$.
- **From one-dimensional boundary value problems.** Three-point finite differences or linear finite elements for $-(k u')' + c u = f$ give symmetric tridiagonal systems.
- **To tridiagonal eigenproblems.** The pivots $u_i(\lambda)$ of $A - \lambda I$ form the Sturm sequence: for symmetric $A$, the number of negative pivots equals the number of eigenvalues below $\lambda$ (by Sylvester's law of inertia). This drives bisection for eigenvalues, and inverse iteration solves shifted tridiagonal systems.
- **From the Lanczos process.** The [Lanczos algorithm](/lanczos-algorithm/) reduces a symmetric matrix to tridiagonal form, and the [conjugate gradient method](/conjugate-gradient-method/) and MINRES implicitly solve tridiagonal systems in $T_k$ at each step.
- **Block reductions.** A five-point Laplacian on a grid ordered by lines is block tridiagonal with tridiagonal blocks, and block methods reduce it to many tridiagonal solves.

## Applications

- Implicit time stepping for the heat equation (Crank-Nicolson) and ADI methods, which solve tridiagonal systems along each grid line.
- Cubic spline and smoothing spline interpolation.
- Line relaxation and line smoothers in multigrid for anisotropic problems.
- Computing eigenvalues and eigenvectors of symmetric tridiagonal matrices after Householder reduction.
- Tridiagonal Toeplitz and cyclic systems in signal processing and periodic boundary value problems.

## References
