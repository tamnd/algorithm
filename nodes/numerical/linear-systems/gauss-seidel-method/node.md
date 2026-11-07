---
tag: 2WJJ4E
kind: algorithm
slug: gauss-seidel-method
name: Gauss-Seidel method
aliases:
- Gauss-Seidel iteration
- Liebmann method
- method of successive displacements
area: numerical/linear-systems
level: core
summary: Stationary iteration that uses each newly computed unknown immediately.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of A", z: "the number of nonzeros of A", q: "the norm of the Jacobi iteration matrix in the infinity norm (q < 1)", ε: "the factor by which the error must drop"}
  time: {worst: "O(z ln(1/ε) / ln(1/q))"}
  space: {extra: Θ(n)}
  sweeps: {worst: "⌈ln(1/ε) / ln(1/q)⌉"}
properties: {deterministic: true, in_place: true, recursive: false, iterative: true, parallel: false}
prereqs: [matrix-splitting, spectral-radius, positive-definite-matrix, diagonally-dominant-matrix]
see_also: [jacobi-method, successive-over-relaxation, ostrowski-reich-theorem, multigrid-method, kaczmarz-method, preconditioning, conjugate-gradient-method, richardson-iteration]
sources:
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 4.1, Jacobi, Gauss-Seidel, and SOR; Section 4.2, Convergence (Section 4.2.5, property A and consistent orderings)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 11.2, The Classical Iterations (convergence for symmetric positive definite matrices)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 17, Stationary Iterative Methods (Section 17.2.2, the forward error analysis of SOR, which contains Gauss-Seidel)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 6.5, Basic Iterative Methods (the model problem, red-black ordering, ρ(G_GS) = ρ(G_J)^2)
  - book: isbn:9780898714623
    title: William L. Briggs, Van Emden Henson and Steve F. McCormick, A Multigrid Tutorial, second edition, SIAM, 2000
    locator: Chapter 2, Basic Iterative Methods (Gauss-Seidel and red-black Gauss-Seidel as smoothers)
  - book: "Richard S. Varga, Matrix Iterative Analysis, second edition, Springer, 2000"
    locator: Section 3.3, the Stein-Rosenberg theorem; Chapter 4, Successive Overrelaxation Iterative Methods (consistent orderings)
  - paper: "Philipp Ludwig von Seidel, Über ein Verfahren, die Gleichungen, auf welche die Methode der kleinsten Quadrate führt, sowie lineäre Gleichungen überhaupt, durch successive Annäherung aufzulösen, Abhandlungen der Mathematisch-Physikalischen Classe der Königlich Bayerischen Akademie der Wissenschaften 11, 1874"
    locator: pp. 81 to 108 (the method for the normal equations, with convergence for positive definite systems)
  - paper: "Philip Stein and R. L. Rosenberg, On the solution of linear simultaneous equations by iteration, Journal of the London Mathematical Society 23, 1948"
    locator: pp. 111 to 118 (the comparison of the Jacobi and Gauss-Seidel spectral radii for nonnegative Jacobi matrices)
---

The Gauss-Seidel method solves $A x = b$ by sweeping through the equations in order and solving equation $i$ for $x_i$ with the newest available values of the other unknowns: those with $j < i$ come from the current sweep, those with $j > i$ from the previous one. In matrix form $x_{k+1} = (D + L)^{-1}(b - U x_k)$. It converges for every start when $A$ is [symmetric positive definite](/positive-definite-matrix/) or strictly [diagonally dominant](/diagonally-dominant-matrix/), and on the model Poisson problem it needs half as many sweeps as [Jacobi](/jacobi-method/). It overwrites $x$ in place, but each sweep is sequential unless the unknowns are colored.

## In plain words

The method goes through the equations one at a time. Each equation is solved for its own unknown, and the new value replaces the old one at once, so the next equation already sees it. After the last equation, the method starts again at the first.

Using fresh values usually helps: on many practical problems the error shrinks about twice as fast per round as with the Jacobi method, which uses only the values from the previous round. For a symmetric positive definite matrix, every single update lowers a natural measure of the error, so the method can never diverge. The price is that the updates must happen in order.

## The problem

**Notation.** As in [solving linear systems](/linear-system-solving/) and the [Jacobi method](/jacobi-method/): $A = D + L + U$ with $D$ diagonal (nonzero), $L$ strictly lower and $U$ strictly upper triangular; $x$ solves $A x = b$; $x_k$ is the iterate after $k$ sweeps, $e_k = x - x_k$ and $r_k = b - A x_k$. The [splitting](/matrix-splitting/) is $M = D + L$, $N = -U$, with iteration matrix $G_{GS} = -(D + L)^{-1} U$ and Jacobi matrix $G_J = -D^{-1}(L + U)$. $\rho$ is the [spectral radius](/spectral-radius/), $q = \|G_J\|_\infty$, $\|v\|_A = (v^T A v)^{1/2}$, $u = 2^{-53}$, $\gamma_m = m u / (1 - m u)$, and $z$ is the number of nonzeros.

Input: $A$ with nonzero diagonal, $b$, a start $x_0$, a tolerance $\text{tol}$ and a sweep limit $k_{\max}$. Output: $x_k$ with $\|r_k\|_\infty \le \text{tol} \cdot \|b\|_\infty$, or the last iterate with a flag that the test was not met.

## The algorithm

```pseudo id=main
GaussSeidel(A, b, x, tol, kmax)            ▷ x is the start x₀, overwritten
L1  for k ← 0 to kmax do
L2      r ← b − A x
L3      if ‖r‖_∞ ≤ tol · ‖b‖_∞ then return (x, k, CONVERGED)
L4      if k = kmax then return (x, k, NOT-CONVERGED)
L5      for i ← 1 to n do
L6          s ← Σ_{j < i} a_ij x_j + Σ_{j > i} a_ij x_j     ▷ x_j is already new for j < i
L7          x_i ← (b_i − s) / a_ii
```

Line L2 is a separate pass over $A$ for the stopping test; it can be done every few sweeps to save time, or replaced by $r_{k+1} = U (x_k - x_{k+1})$, which follows from $(D + L) x_{k+1} = b - U x_k$ and needs only the upper part. Lines L5 to L7 are one forward sweep. Line L7 sets $x_i$ to the value that makes the $i$-th residual zero for the current vector.

## Example

The matrix of the [Jacobi example](/jacobi-method/), with $x_0 = 0$:
$$A = \begin{pmatrix} 4 & -1 & 0 \\ -1 & 4 & -1 \\ 0 & -1 & 4 \end{pmatrix}, \quad b = \begin{pmatrix} 3 \\ 2 \\ 3 \end{pmatrix}, \quad x = \begin{pmatrix} 1 \\ 1 \\ 1 \end{pmatrix}.$$
In exact arithmetic:

| $k$ | $x_k$ | $e_k$ |
|---|---|---|
| 0 | $(0, 0, 0)$ | $(1, 1, 1)$ |
| 1 | $(3/4, 11/16, 59/64)$ | $(1/4, 5/16, 5/64)$ |
| 2 | $(59/64, 123/128, 507/512)$ | $(5/64, 5/128, 5/512)$ |
| 3 | $(507/512, 1019/1024, 4091/4096)$ | $(5/512, 5/1024, 5/4096)$ |

In sweep 1, $x_1 = 3/4$ comes from $(3 + 0)/4$, then $x_2 = (2 + 3/4 + 0)/4 = 11/16$ already uses the new $x_1$, and $x_3 = (3 + 11/16)/4 = 59/64$. From sweep 1 on, each sweep multiplies the error by exactly $1/8$. This matrix is tridiagonal, so it is consistently ordered and $\rho(G_{GS}) = \rho(G_J)^2 = (\sqrt 2/4)^2 = 1/8$: one Gauss-Seidel sweep does what two Jacobi sweeps do.

## Correctness

The proofs are in `proofs/correctness.md` and `proofs/complexity.md`. In exact arithmetic:

1. **Fixed point.** $x = G_{GS} x + (D + L)^{-1} b$ exactly when $A x = b$, so $e_{k+1} = G_{GS} e_k$, and $x_k \to x$ for every $x_0$ exactly when $\rho(G_{GS}) < 1$.
2. **Symmetric positive definite $A$ (Ostrowski-Reich, proved).** Line L7 minimizes $\phi(y) = \tfrac12 y^T A y - b^T y$ along the coordinate $y_i$, and it lowers $\|e\|_A^2$ by $r_i^2 / a_{ii}$, where $r_i$ is the current residual entry. So $\|e_{k+1}\|_A < \|e_k\|_A$ unless $e_k = 0$, and $\rho(G_{GS}) \le \|G_{GS}\|_A < 1$. Conversely, if $A$ is symmetric with positive diagonal and not positive definite, Gauss-Seidel diverges for some start ([Ostrowski-Reich theorem](/ostrowski-reich-theorem/)).
3. **Strict row diagonal dominance (proved).** With $\alpha_i = \sum_{j < i} |a_{ij}| / |a_{ii}|$ and $\beta_i = \sum_{j > i} |a_{ij}| / |a_{ii}|$, $\|G_{GS}\|_\infty \le \max_i \beta_i / (1 - \alpha_i) \le q < 1$, so $\|e_k\|_\infty \le q^k \|e_0\|_\infty$.
4. **Consistent orderings (Young 1950, cited).** If $A$ is consistently ordered, for instance tridiagonal or block tridiagonal with diagonal blocks, or the 5-point Laplacian in red-black order, then the eigenvalues satisfy $\lambda_{GS} = \lambda_J^2$, so $\rho(G_{GS}) = \rho(G_J)^2$ (Saad, Section 4.2.5).
5. **Stein-Rosenberg (1948, cited).** If $G_J \ge 0$ entrywise (for instance $a_{ii} > 0$ and $a_{ij} \le 0$ for $i \ne j$), exactly one of the following holds: $\rho(G_{GS}) = \rho(G_J) = 0$; $0 < \rho(G_{GS}) < \rho(G_J) < 1$; $\rho(G_{GS}) = \rho(G_J) = 1$; or $1 < \rho(G_J) < \rho(G_{GS})$. So for such matrices the two methods converge or diverge together, and Gauss-Seidel is faster.
6. **No general comparison.** Without such hypotheses either method can win. For $A = \begin{pmatrix} 1 & 2 & -2 \\ 1 & 1 & 1 \\ 2 & 2 & 1 \end{pmatrix}$, $G_J^3 = 0$, so Jacobi gives the exact solution in 3 sweeps, while $G_{GS}$ has eigenvalues $0, 2, 2$ and Gauss-Seidel diverges. The positive definite matrix with unit diagonal and off-diagonal entries $0.8$ is the reverse case.
7. **Rounding (proved in part).** Each computed sweep satisfies $(D + L + \Delta L) \hat x_{k+1} + (U + \Delta U) \hat x_k = b + \Delta b$ with $|\Delta L| \le \gamma_{n+1} |L|$, $|\Delta U| \le \gamma_{n+1} |U|$, $|\Delta b| \le \gamma_{n+1} |b|$: each sweep is backward stable. These perturbations are amplified at most by $\sum_{j \ge 0} \|G_{GS}^j\|$, which is at most $1/(1 - \|G_{GS}\|)$ when $\|G_{GS}\| < 1$, so the limiting accuracy is $O(u)$ times that factor times $\|(D + L)^{-1}\| (\|b\| + \|L + U\| \|x\|)$. Higham, Section 17.2.2, gives the componentwise version for SOR.

## Complexity

| quantity | cost |
|---|---|
| one sweep, sparse $A$ | about $2z$ flops, each entry of $A$ read once |
| residual test (line L2) | about $2z$ flops; doing it every $m$ sweeps reduces this to $2z/m$ per sweep |
| sweeps for $\|e_k\|_\infty \le \varepsilon \|e_0\|_\infty$, strictly row diagonally dominant $A$ | at most $\lceil \ln(1/\varepsilon) / \ln(1/q) \rceil$ (proved) |
| sweeps, model problem | about $\ln(1/\varepsilon) / (\pi^2 h^2)$, half of the Jacobi count, since $\rho(G_{GS}) = \cos^2(\pi h) \approx 1 - \pi^2 h^2$ |
| extra storage | the residual for the test: $n$ numbers |

As with [Jacobi](/jacobi-method/), a sparse sweep does about 2 flops per stored nonzero, so it is limited by memory bandwidth. Gauss-Seidel has an extra cost on parallel machines: in the natural order, $x_i$ depends on $x_{i-1}$, so the sweep is as sequential as a [triangular solve](/back-substitution/). Coloring the unknowns, so that no two unknowns of one color are coupled, makes each color class a parallel Jacobi-like update; for the 5-point Laplacian two colors (red-black) suffice.

## Properties

- **In place.** New values overwrite old ones; no second vector is needed for the sweep.
- **Order dependent.** Renumbering the unknowns changes $G_{GS}$ and its spectral radius. For the 5-point Laplacian, both the natural and the red-black order are consistently ordered and give the same $\rho$, but the error behaves differently in each.
- **Coordinate descent.** For symmetric positive definite $A$, each update is exact minimization of $\phi$ along one coordinate, so $\|e\|_A$ decreases monotonically.
- **Nonsymmetric iteration.** $G_{GS}$ is not symmetric in the $A$ inner product even when $A$ is symmetric, so a forward sweep cannot be used as a preconditioner for [conjugate gradients](/conjugate-gradient-method/). A forward sweep followed by a backward sweep (symmetric Gauss-Seidel) can.

## Variants and improvements

- **[Successive over-relaxation](/successive-over-relaxation/) (SOR).** $x_i \leftarrow (1 - \omega) x_i + \omega (b_i - s)/a_{ii}$. With the optimal $\omega$ on the model problem, $\rho \approx 1 - 2 \pi h$, so the sweep count drops from $O(h^{-2})$ to $O(h^{-1})$.
- **Symmetric Gauss-Seidel (SGS) and SSOR.** A forward then a backward sweep. The iteration matrix is similar to a symmetric one with eigenvalues in $[0, 1)$ for symmetric positive definite $A$, so it can be accelerated by [CG](/conjugate-gradient-method/) or [Chebyshev iteration](/chebyshev-iteration/).
- **Block Gauss-Seidel.** Solve for groups of unknowns at once, such as grid lines (line relaxation). It is more robust for anisotropic problems.
- **Red-black and multicolor Gauss-Seidel.** Parallel within each color. It is the standard [multigrid](/multigrid-method/) smoother for Poisson-type problems.
- **Kaczmarz as Gauss-Seidel.** The [Kaczmarz method](/kaczmarz-method/) on $A x = b$ is Gauss-Seidel applied to $A A^T y = b$ with $x = A^T y$.

## When to use it

Use Gauss-Seidel as a smoother in multigrid, as a simple solver for small or strongly diagonally dominant systems, and as a building block (SGS) for preconditioners. It needs no tuning and no extra storage, and it converges for every symmetric positive definite matrix. On its own it is too slow for large discretized PDEs, where the sweep count grows like $h^{-2}$; prefer preconditioned [CG](/conjugate-gradient-method/) or [multigrid](/multigrid-method/).

## Pitfalls

- **Assuming it beats Jacobi.** The comparison holds under Stein-Rosenberg or consistent ordering hypotheses, not in general (fact 6).
- **Assuming convergence for symmetric indefinite matrices.** Positive definiteness is necessary as well as sufficient among symmetric matrices with positive diagonal.
- **Parallelizing the natural order naively.** Running the loop in line L5 in parallel gives a mixture of Jacobi and Gauss-Seidel that depends on timing and is not reproducible.
- **Using a forward sweep as a CG preconditioner.** It is not symmetric; use SGS.
- **Stopping on a small update.** As for Jacobi, $\|x_{k+1} - x_k\|$ underestimates $\|e_k\|$ by a factor of about $1/(1 - \rho)$, which is huge on fine grids.
- **Trusting a small residual.** On the [Hilbert matrix](/hilbert-matrix/) $H_6$, which is positive definite, with $x = (1, \ldots, 1)$, the error after 1000 sweeps from $x_0 = 0$ is still about $0.05$ while $\|r\|_\infty$ is about $1.4 \times 10^{-6}$. Convergence is guaranteed but slow, and the residual says little when $\kappa(A)$ is large.

## Implementations

## History

Gauss described the idea in an 1823 letter to Gerling, as a way to solve the normal equations of geodetic least squares problems by hand, one unknown at a time. Seidel published it in 1874 with a convergence argument for positive definite systems. Liebmann applied it to Laplace's equation in 1918, hence the name Liebmann method in the PDE literature. The spectral theory came in the 20th century: the Stein-Rosenberg theorem (1948), Ostrowski (1954) and Reich (1949) on positive definite matrices, and Young's theory of consistent orderings (1950), which led to SOR. Gauss-Seidel became the standard smoother when multigrid was developed by Fedorenko and Brandt in the 1960s and 1970s.

## References
