---
tag: R75FV5
kind: algorithm
slug: jacobi-method
name: Jacobi method
aliases:
- Jacobi iteration
- simultaneous displacements
- point Jacobi
area: numerical/linear-systems
level: core
summary: Stationary iteration that updates every unknown using only old values.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of A", z: "the number of nonzeros of A", q: "the norm of the iteration matrix in the infinity norm (q < 1)", ε: "the factor by which the error must drop"}
  time: {worst: "O(z ln(1/ε) / ln(1/q))"}
  space: {extra: Θ(n)}
  sweeps: {worst: "⌈ln(1/ε) / ln(1/q)⌉"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true, parallel: true}
prereqs: [matrix-splitting, spectral-radius, diagonally-dominant-matrix]
see_also: [gauss-seidel-method, successive-over-relaxation, richardson-iteration, multigrid-method, preconditioning, conjugate-gradient-method, chebyshev-iteration, ostrowski-reich-theorem]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 17, Stationary Iterative Methods (Section 17.2, forward error analysis, with the Jacobi method treated in Section 17.2.1)
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 4.1, Jacobi, Gauss-Seidel, and SOR; Section 4.2, Convergence (diagonally dominant and symmetric positive definite matrices)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 11.2, The Classical Iterations
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 6.5, Basic Iterative Methods (the spectral radius of the Jacobi matrix for the model problem)
  - book: isbn:9780898714623
    title: William L. Briggs, Van Emden Henson and Steve F. McCormick, A Multigrid Tutorial, second edition, SIAM, 2000
    locator: Chapter 2, Basic Iterative Methods (the weighted Jacobi method as a smoother)
  - paper: doi:10.1002/asna.18450222002
    title: Carl Gustav Jacob Jacobi, Ueber eine neue Auflösungsart der bei der Methode der kleinsten Quadrate vorkommenden linearen Gleichungen, Astronomische Nachrichten 22, 1845
    locator: pp. 297 to 306 (the iteration on a diagonally dominant system, after rotations that enlarge the diagonal)
  - book: "Richard S. Varga, Matrix Iterative Analysis, second edition, Springer, 2000"
    locator: Chapter 3, Basic Iterative Methods and Comparison Theorems (the Stein-Rosenberg theorem)
---

The Jacobi method solves $A x = b$ by sweeps: in each sweep, every unknown $x_i$ is recomputed from equation $i$ with all the other unknowns held at their values from the previous sweep. In matrix form $x_{k+1} = D^{-1}(b - (L + U) x_k)$, where $D$, $L$ and $U$ are the diagonal, strictly lower and strictly upper parts of $A$. It converges for every start exactly when the spectral radius of $G_J = -D^{-1}(L + U)$ is below 1, which holds for instance when $A$ is strictly diagonally dominant. It is slow, about $(n+1)^2$ sweeps per digit on the model Poisson problem, but each sweep is fully parallel, which is why it survives as a smoother in [multigrid](/multigrid-method/) and as the diagonal [preconditioner](/preconditioning/).

## In plain words

Each equation of the system says what one unknown should be if all the others were known. The Jacobi method makes a guess for all unknowns. Then it solves every equation for its own unknown, using the guess for the others, and all these updates happen at the same time. The new values become the next guess, and the process repeats.

If every unknown is controlled mostly by its own equation, so that the other terms are small in comparison, each round shrinks the error by a fixed factor. If not, the error can grow instead. Because all updates in a round are independent, a computer can do them all at once, which is the method's main strength.

## The problem

**Notation.** As in [solving linear systems](/linear-system-solving/): $A$ is $n \times n$ with nonzero diagonal, $x$ is the solution of $A x = b$, $x_k$ the iterate after $k$ sweeps, $e_k = x - x_k$ the error and $r_k = b - A x_k$ the residual. Write $A = D + L + U$ with $D$ diagonal, $L$ strictly lower and $U$ strictly upper triangular. This is the [matrix splitting](/matrix-splitting/) $A = M - N$ with $M = D$, $N = -(L + U)$. The iteration matrix is $G_J = M^{-1} N = I - D^{-1} A$, $\rho(G_J)$ its [spectral radius](/spectral-radius/) and $q = \|G_J\|_\infty = \max_i \sum_{j \ne i} |a_{ij}| / |a_{ii}|$. $u = 2^{-53}$ and $\gamma_m = m u / (1 - m u)$. $z$ is the number of nonzeros of $A$.

Input: $A$ (dense or sparse) with $a_{ii} \ne 0$, $b$, a start $x_0$, a tolerance $\text{tol}$ and a sweep limit $k_{\max}$. Output: $x_k$ with $\|r_k\|_\infty \le \text{tol} \cdot \|b\|_\infty$, or the last iterate with a flag that the test was not met. A zero diagonal entry is an error.

## The algorithm

Sweep $k$ computes, for each $i$, the off-diagonal sum $s_i = \sum_{j \ne i} a_{ij} x_j$ from the old vector. The residual comes for free from the same sums, $r_i = b_i - s_i - a_{ii} x_i$, so the stopping test costs no extra pass over $A$. The new vector is written to separate storage.

```pseudo id=main
Jacobi(A, b, x, tol, kmax)                 ▷ x is the start x₀
L1  for k ← 0 to kmax do
L2      for i ← 1 to n do
L3          s_i ← Σ_{j ≠ i} a_ij x_j
L4          r_i ← b_i − s_i − a_ii x_i
L5      if ‖r‖_∞ ≤ tol · ‖b‖_∞ then return (x, k, CONVERGED)
L6      if k = kmax then return (x, k, NOT-CONVERGED)
L7      for i ← 1 to n do
L8          x_i ← (b_i − s_i) / a_ii           ▷ uses only the old x through s
```

Lines L2 to L4 compute $s$ and $r_k$ for the current $x = x_k$. Line L5 is the stopping test, line L6 the sweep limit, and lines L7 and L8 form $x_{k+1} = D^{-1}(b - (L + U) x_k)$. The loop in line L7 has no dependences, so it can run in any order or in parallel.

## Example

Take
$$A = \begin{pmatrix} 4 & -1 & 0 \\ -1 & 4 & -1 \\ 0 & -1 & 4 \end{pmatrix}, \quad b = \begin{pmatrix} 3 \\ 2 \\ 3 \end{pmatrix}, \quad x = \begin{pmatrix} 1 \\ 1 \\ 1 \end{pmatrix}, \quad x_0 = 0.$$
Here $G_J = \tfrac14 \begin{pmatrix} 0 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 0 \end{pmatrix}$, with eigenvalues $0$ and $\pm \sqrt 2 / 4$, so $\rho(G_J) = \sqrt 2 / 4 \approx 0.354$ and $q = 1/2$. The sweeps, in exact arithmetic:

| $k$ | $x_k$ | $e_k$ |
|---|---|---|
| 0 | $(0, 0, 0)$ | $(1, 1, 1)$ |
| 1 | $(3/4, 1/2, 3/4)$ | $(1/4, 1/2, 1/4)$ |
| 2 | $(7/8, 7/8, 7/8)$ | $(1/8, 1/8, 1/8)$ |
| 3 | $(31/32, 15/16, 31/32)$ | $(1/32, 1/16, 1/32)$ |
| 4 | $(63/64, 63/64, 63/64)$ | $(1/64, 1/64, 1/64)$ |

Every two sweeps the error drops by exactly $1/8 = \rho(G_J)^2$, since $e_0$ has no component along the eigenvalue $0$. The per-sweep factor in the infinity norm, $\|e_{k+1}\|_\infty / \|e_k\|_\infty$, alternates between $1/2 = q$ and $1/4$; the bound $\|e_{k+1}\|_\infty \le q \|e_k\|_\infty$ is attained at $k = 0$.

## Correctness

The full proofs are in `proofs/correctness.md` and `proofs/complexity.md`. The facts, all for exact arithmetic unless stated otherwise:

1. **Fixed point.** $x$ solves $A x = b$ exactly when $x = G_J x + D^{-1} b$. So $e_{k+1} = G_J e_k$ and $e_k = G_J^k e_0$.
2. **Convergence criterion.** $x_k \to x$ for every $x_0$ if and only if $\rho(G_J) < 1$. The asymptotic factor per sweep is $\rho(G_J)$.
3. **Diagonal dominance.** If $A$ is strictly diagonally dominant by rows, then $q < 1$ and $\|e_k\|_\infty \le q^k \|e_0\|_\infty$. The same holds by columns in the norm $\|D \cdot\|_1$. Weak dominance with irreducibility also gives $\rho(G_J) < 1$ (Saad, Section 4.2).
4. **Symmetric positive definite $A$ is not enough.** For symmetric positive definite $A$, Jacobi converges if and only if $2D - A$ is also positive definite (Saad, Section 4.2). The matrix with $1$ on the diagonal and $a = 0.8$ elsewhere ($n = 3$) is positive definite, but $\rho(G_J) = 2a = 1.6$ and Jacobi diverges, while [Gauss-Seidel](/gauss-seidel-method/) converges on it.
5. **Rounding (proved here).** Let $A$ be strictly row diagonally dominant with $q (1 + \gamma_{n+1}) < 1$, and let $\hat x_k$ be the computed iterates in the [floating point model](/floating-point-model/). Then for all $k$
$$\|x - \hat x_k\|_\infty \le \bigl(q(1 + \gamma_{n+1})\bigr)^k \|x - \hat x_0\|_\infty + \frac{\gamma_{n+1}(1 + 2q)}{1 - q(1 + \gamma_{n+1})} \|x\|_\infty.$$
So the attainable relative forward error is about $3 \gamma_{n+1} / (1 - q)$. For such matrices $\kappa_\infty(A) \le \frac{1 + q}{1 - q} \cdot \frac{\max_i |a_{ii}|}{\min_i |a_{ii}|}$, so this is no worse than the bound $\kappa_\infty(A) u$ for a backward stable direct solver up to the spread of the diagonal. Higham, Section 17.2.1, reaches the same conclusion (Jacobi is forward stable for these matrices) with componentwise bounds. The bound is proved; in practice the error levels off far below it.

The loop terminates after at most $k_{\max} + 1$ residual evaluations. Whenever it returns "converged", $\|b - A x\|_\infty \le \text{tol} \cdot \|b\|_\infty$ held for the returned $x$ as computed in line L4, up to the rounding in that line.

## Complexity

| quantity | cost |
|---|---|
| one sweep, sparse $A$ | $2z + 3n$ flops for $s$, $r$ and the update; each of the $z$ entries of $A$ read once |
| one sweep, dense $A$ | $2n^2$ flops |
| sweeps for $\|e_k\|_\infty \le \varepsilon \|e_0\|_\infty$ | at most $\lceil \ln(1/\varepsilon) / \ln(1/q) \rceil$ when $q < 1$ (proved) |
| sweeps, asymptotically | about $\ln(1/\varepsilon) / \ln(1/\rho(G_J))$ (observed for generic $e_0$; the transient can be long when $G_J$ is far from normal) |
| extra storage | the vectors $s$ and $r$ plus the new $x$: $3n$ numbers |

On the model problem, the 1D or 2D Laplacian on a grid with spacing $h = 1/(m+1)$, the eigenvalues of $G_J$ are $\cos(j \pi h)$ (1D) or $\tfrac12(\cos(i\pi h) + \cos(j \pi h))$ (2D), so $\rho(G_J) = \cos(\pi h) \approx 1 - \pi^2 h^2 / 2$ (Demmel, Section 6.5). One digit then costs about $2 \ln(10) / (\pi^2 h^2) \approx 0.47 (m+1)^2$ sweeps, and the total work for an $N = m^2$ point 2D grid is $O(N^2)$ flops, against $O(N^{3/2})$ for [conjugate gradients](/conjugate-gradient-method/) and $O(N)$ for [multigrid](/multigrid-method/).

A sparse sweep does about 2 flops per stored nonzero, which needs at least 12 bytes from memory in CSR with 8-byte values and 4-byte indices. On current hardware this ratio makes the sweep limited by memory bandwidth, not by flops, so the time per sweep is close to the time to stream $A$ once.

## Properties

- **Parallel.** All $n$ updates of a sweep are independent, unlike [Gauss-Seidel](/gauss-seidel-method/).
- **Not in place.** It needs the old vector until the sweep ends.
- **Order independent.** The result does not depend on the numbering of the unknowns: a symmetric permutation $P A P^T$ gives the permuted iterates.
- **Invariant under diagonal scaling of rows.** Replacing $A$, $b$ by $S A$, $S b$ with $S$ diagonal and nonsingular gives the same iterates.
- **Matrix-free in part.** It needs $D$ and products with $L + U$, not a factorization.

## Variants and improvements

- **Weighted (damped) Jacobi.** $x_{k+1} = x_k + \omega D^{-1} r_k$. For the model problem, $\omega = 2/3$ damps the upper half of the spectrum by a factor of at least $1/3$ per sweep, which makes it a standard multigrid smoother (Briggs et al., Chapter 2), although it makes $\rho$ itself slightly worse.
- **Block Jacobi.** $D$ is replaced by a block diagonal $M$; each sweep solves the diagonal blocks. It converges faster when the blocks hold strongly coupled unknowns, and it is the simplest [domain decomposition](/domain-decomposition/) method.
- **Jacobi preconditioning.** Using $M = D$ inside [conjugate gradients](/conjugate-gradient-method/) or [GMRES](/gmres/) rather than as a stationary method. Van der Sluis showed that for symmetric positive definite $A$ this diagonal scaling is within a factor $n$ of the best diagonal scaling in $\kappa_2$ (Higham, Section 7.3).
- **Acceleration.** Chebyshev acceleration of the Jacobi iteration ([Chebyshev iteration](/chebyshev-iteration/)) reduces the sweep count from $O(1/(1-\rho))$ to $O(1/\sqrt{1-\rho})$ when $G_J$ has real eigenvalues.
- **Asynchronous Jacobi.** Processors update their unknowns with whatever values have arrived. It converges when $\rho(|G_J|) < 1$ (Chazan and Miranker 1969).

## When to use it

Use Jacobi when the matrix is strongly diagonally dominant, as with implicit time steps with a small step size or mass matrices, when massive parallelism matters more than the number of sweeps, or as a smoother inside multigrid. For general sparse systems it is too slow as a solver on its own; use [conjugate gradients](/conjugate-gradient-method/) or [GMRES](/gmres/) with a preconditioner. Its diagonal is often the first preconditioner to try.

## Pitfalls

- **Assuming convergence for positive definite matrices.** Unlike [Gauss-Seidel](/gauss-seidel-method/), Jacobi can diverge on a symmetric positive definite matrix (fact 4).
- **Updating in place.** Overwriting $x_i$ during the sweep turns the method into Gauss-Seidel, which changes the convergence and loses the parallelism.
- **Stopping on the step size.** A small $\|x_{k+1} - x_k\|$ means $\|e_k\| \lesssim \|x_{k+1} - x_k\| / (1 - q)$; when $q$ is near 1 the error can be much larger than the step. Test the residual, as line L5 does, or scale the step by $1/(1 - q)$.
- **Zero or tiny diagonal entries.** The method is undefined for $a_{ii} = 0$ and badly scaled for tiny $a_{ii}$; reorder the equations first.
- **Expecting a smooth error to decrease fast.** For the Laplacian, the error component of lowest frequency drops by only $\cos(\pi h)$ per sweep; this is what multigrid fixes.

## Implementations

## History

Jacobi described the method in 1845 for the normal equations of least squares problems in astronomy, after first applying plane rotations to make the diagonal dominate. Gauss had used a sequential variant earlier (see [Gauss-Seidel](/gauss-seidel-method/)). The convergence theory in terms of the spectral radius, including the Stein-Rosenberg theorem (1948) comparing Jacobi and Gauss-Seidel for matrices with $G_J \ge 0$, was developed in the 1950s and collected by Varga (1962) and Young (1971). The rounding error analysis of stationary methods is due to Higham and Knight (1993), and is presented in Higham, Chapter 17.

## References
