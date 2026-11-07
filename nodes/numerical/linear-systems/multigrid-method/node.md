---
tag: ZXX910
kind: algorithm
slug: multigrid-method
name: Multigrid method
aliases:
- multigrid
- geometric multigrid
- V-cycle
area: numerical/linear-systems
level: advanced
summary: Solve on a hierarchy of coarser grids to damp errors at every frequency.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the number of unknowns on the finest grid", k: "the number of cycles", a: "presmoothing sweeps", b: "postsmoothing sweeps"}
  time: {worst: Θ(k n), best: Θ(n)}
  space: {extra: Θ(n)}
  flops: {worst: "k (2 (8 (a + b) + 9) n)"}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [jacobi-method, gauss-seidel-method, poisson-equation, finite-difference-method]
see_also: [algebraic-multigrid, preconditioning, conjugate-gradient-method, successive-over-relaxation, domain-decomposition, sparse-linear-systems, thomas-algorithm, spectral-radius]
sources:
  - book: isbn:9780898714623
    title: William L. Briggs, Van Emden Henson and Steve F. McCormick, A Multigrid Tutorial, second edition, SIAM, 2000
    locator: Chapter 2, Basic Iterative Methods (smoothing by weighted Jacobi and Gauss-Seidel); Chapter 3, Elements of Multigrid (intergrid transfers, the V-cycle and full multigrid); Chapter 4, Implementation (cost and storage); Chapter 5, Some Theory
  - paper: doi:10.1090/S0025-5718-1977-0431719-X
    title: Achi Brandt, Multi-level adaptive solutions to boundary-value problems, Mathematics of Computation 31(138), 1977
    locator: local mode (Fourier) analysis of smoothing factors, the V and W cycles, full multigrid and the claim of solution to discretization accuracy in a few work units
  - paper: doi:10.1137/0720066
    title: Dietrich Braess and Wolfgang Hackbusch, A new convergence proof for the multigrid method including the V-cycle, SIAM Journal on Numerical Analysis 20(5), 1983
    locator: convergence of the V-cycle with a rate bounded independently of the mesh size for symmetric positive definite problems
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Chapter 13, Multigrid Methods (the model problem, smoothers, intergrid operations, the standard cycles and the analysis by the Galerkin variational framework)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 6.9, Multigrid (the one-dimensional model problem, the V-cycle and full multigrid with their O(n) cost)
---

Multigrid solves the linear systems of discretized elliptic equations, such as the [Poisson equation](/poisson-equation/), in $O(n)$ work for $n$ unknowns. Simple relaxations such as weighted [Jacobi](/jacobi-method/) or [Gauss-Seidel](/gauss-seidel-method/) remove the oscillatory part of the error in a few sweeps but are very slow on the smooth part. A smooth error can be represented on a grid with half the spacing, where it looks more oscillatory and relaxation works again; recursing down a hierarchy of grids gives the V-cycle. Each cycle costs a constant number of sweeps on the fine grid, and it reduces the error by a factor, about $0.13$ in the example below, that does not grow with $n$.

## In plain words

A fine grid of values has errors of every size, from wiggles between neighbours to slow drifts across the whole domain. Averaging each value with its neighbours removes the wiggles at once but takes forever to remove the drifts, because information travels one cell per sweep. On a coarser grid, a slow drift looks like a fast wiggle, so averaging there removes it quickly and cheaply. Multigrid smooths on the fine grid, passes what is left to a coarser grid, and repeats, down to a grid of one or two points. It then carries the corrections back up, smoothing again at each level.

## The problem

**Notation.** The model problem is $-u'' = f$ on $(0, 1)$ with $u(0) = u(1) = 0$, discretized by [finite differences](/finite-difference-method/) on level $l$ with $n_l = 2^l - 1$ interior points, spacing $h_l = 2^{-l}$ and $A_l = h_l^{-2}\,\mathrm{tridiag}(-1, 2, -1)$. The grid vectors are written $v$, so that $u$ is free for the unit roundoff. The finest level is $L$ with $n = n_L$, $A = A_L$, right side $f$ and solution $v^\ast = A^{-1} f$. The iterate after $k$ cycles is $v_k$, the residual $r_k = f - A v_k$, the error $e_k = v_k - v^\ast$. $P_l$ is linear interpolation from level $l-1$ to level $l$, $R_l$ is full weighting, $S$ is the error operator of one smoothing sweep, $\nu_1$ and $\nu_2$ (written $a$ and $b$ in the cost formula) are the numbers of sweeps before and after the coarse correction, and $M$ is the error operator of one V-cycle, the iteration matrix, with spectral radius $\rho(M)$. $\kappa_2(A) = \sin^2(n\pi h/2)/\sin^2(\pi h/2) \approx 4/(\pi h)^2$ and $u = 2^{-53}$.

**Input.** $f$ on the finest grid, a start $v_0$, $\nu_1$, $\nu_2$, a smoother, a tolerance and a cycle limit.

**Output.** $v_k$ with $\|r_k\|_2 \le \mathrm{tol}\,\|f\|_2$, or the last iterate and a flag. The V-cycle is a linear stationary iteration $e_{k+1} = M e_k$, so the theory of [matrix splittings](/matrix-splitting/) applies: it converges for every start exactly when $\rho(M) < 1$.

## The algorithm

```pseudo id=main
MULTIGRID(f, v_0, ν_1, ν_2, tol, maxiter)                ▷ levels L (finest) down to 1
L1  v_L ← v_0;  f_L ← f
L2  for k ← 1 to maxiter do
L3      for l ← L down to 2 do                              ▷ going down
L4          v_l ← SMOOTH^{ν_1}(A_l, f_l, v_l)
L5          f_{l−1} ← R_l (f_l − A_l v_l);  v_{l−1} ← 0       ▷ restrict the residual
L6      v_1 ← A_1^{-1} f_1                                  ▷ coarsest grid: one unknown, solved exactly
L7      for l ← 2 to L do                                   ▷ going up
L8          v_l ← v_l + P_l v_{l−1}                          ▷ interpolate and add the correction
L9          v_l ← SMOOTH^{ν_2}(A_l, f_l, v_l)
L10     if ‖f − A_L v_L‖_2 ≤ tol · ‖f‖_2 then return (v_L, k, converged)
L11 return (v_L, maxiter, not converged)
```

Lines L3 to L9 are one V-cycle, written with two loops instead of recursion. On level $l < L$ the unknown $v_l$ is a correction to the level above, and $f_l$ is the restricted residual. Weighted Jacobi is $v \leftarrow v + \omega D^{-1}(f - A v)$ with $\omega = 2/3$; full weighting is $(R_l r)_i = \tfrac14(r_{2i} + 2 r_{2i+1} + r_{2i+2})$; linear interpolation copies coarse values to the coincident fine points and averages neighbours at the points between.

## Example

**Why smoothing alone fails.** The eigenvectors of $A$ are the sine modes $\sin(j\pi x)$, $j = 1, \ldots, n$, and one weighted Jacobi sweep multiplies mode $j$ by $1 - 2\omega\sin^2(j\pi h/2)$. With $\omega = 2/3$, every mode with $j \ge (n+1)/2$ (the oscillatory half) is multiplied by at most $1/3$ in absolute value, the *smoothing factor*; mode 1 is multiplied by $1 - \tfrac43\sin^2(\pi h/2) \approx 1 - \pi^2 h^2/3$. For $n = 255$ that is $0.99996$, so reducing a smooth error by $10^{10}$ with Jacobi alone takes about $5 \times 10^5$ sweeps.

**Cycle counts.** Random right sides, $v_0 = 0$, relative residual $10^{-10}$; the rate is the average reduction per cycle after the first two:

| $n$ | V(2,1), weighted Jacobi: cycles | rate | V(1,1), Gauss-Seidel: cycles | rate | V(1,0), weighted Jacobi: cycles | rate |
|---|---|---|---|---|---|---|
| 7 | 10 | 0.091 | 8 | 0.041 | 21 | 0.319 |
| 63 | 11 | 0.118 | 12 | 0.141 | 22 | 0.335 |
| 511 | 12 | 0.126 | 13 | 0.143 | 24 | 0.343 |
| 4095 | 12 | 0.134 | 13 | 0.144 | 26 | 0.360 |

The number of cycles barely changes while $n$ grows by a factor of 585 and $\kappa_2(A)$ by more than $3 \times 10^5$. With $\omega = 1.5$ the smoother amplifies the highest modes and the residual exceeds $10^{10}$ within 30 cycles. Asking for a relative residual of $10^{-18}$ fails: for $n = 255$ the residual stalls between $10^{-16}$ and $10^{-13}$, the rounding level $u\,\|A\|\,\|v^\ast\|/\|f\|$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). For this model problem the transfer operators satisfy $R_l = \tfrac12 P_l^T$ and $R_l A_l P_l = A_{l-1}$ (the coarse matrix is the Galerkin product), so the coarse-grid correction with an exact coarse solve is the $A$-orthogonal projection onto the complement of $\mathrm{range}(P_l)$. By induction on the levels, the V-cycle is a linear iteration with the exact solution as a fixed point, and its error operator satisfies $\|M\|_A < 1$ whenever the smoother contracts in the energy norm: weighted Jacobi with $0 < \omega \le 1$, or Gauss-Seidel.

**Mesh-independent rate (proved, with stated hypotheses).** That $\|M\|_A \le \rho_0 < 1$ with $\rho_0$ independent of $h$ is proved for this model problem by Fourier analysis of the two-grid operator (Briggs, Henson and McCormick, Chapter 5), for the W-cycle and many elliptic problems by Hackbusch's smoothing and approximation properties, and for the V-cycle of symmetric positive definite problems with full elliptic regularity by Braess and Hackbusch (1983). The rates in the table are observed values; the theory gives bounds that are typically less sharp.

**In floating point.** Each cycle is a stationary iteration, so the analysis of Higham (Chapter 17) applies: the residual decreases until it reaches a level of order $u\,\|A\|\,\|v^\ast\|$ times a modest factor and then stalls. The forward error after stopping satisfies $\|v_k - v^\ast\|_2/\|v^\ast\|_2 \le \kappa_2(A)\,\|r_k\|_2/\|f\|_2$ (worst case). For discretized PDEs the relevant target is the discretization error $O(h^2)$, far above the rounding level.

## Complexity

On level $l$, a weighted Jacobi sweep costs about $8 n_l$ flops in this implementation, and the residual, restriction and interpolation about $9 n_l$ together. Since $n_{l-1} \approx n_l/2$, the levels add up to less than $2n$, so one V$(\nu_1, \nu_2)$-cycle costs about $2(8(\nu_1 + \nu_2) + 9)\,n$ flops, $66 n$ for V(2,1). In $d$ dimensions with coarsening by 2 in each direction the level sizes shrink by $2^d$, and the factor 2 becomes $2^d/(2^d - 1)$: $4/3$ in 2D and $8/7$ in 3D. Storage is $f_l$ and $v_l$ on all levels, less than $2n$ words each in 1D.

The number of cycles to reduce the residual by $\varepsilon$ is $O(\log(1/\varepsilon))$, independent of $n$, so the total is $O(n\log(1/\varepsilon))$. **Full multigrid** (FMG) starts on the coarsest grid and uses each interpolated coarse solution as the starting guess on the next finer grid, with one or two V-cycles per level; it reaches the discretization error $O(h^2)$ in $O(n)$ total work, a few fine-grid sweeps (Brandt, 1977). Each sweep streams the grid through memory once with a few flops per point, so multigrid is memory-bandwidth bound like other sparse kernels.

In one dimension the [Thomas algorithm](/thomas-algorithm/) solves the same tridiagonal system exactly in $8n$ flops, so multigrid is not needed there; the 1D problem is the clearest place to see how it works. In 2D and 3D, where direct sparse factorization costs $\Theta(n^{3/2})$ and $\Theta(n^2)$ flops, $O(n)$ multigrid is a large gain.

## Properties

- **Optimal order.** Work $O(n)$ per digit of accuracy, and $O(n)$ to discretization accuracy with FMG, on elliptic problems where the theory applies.
- **Mesh-independent convergence.** The contraction factor per cycle does not depend on $h$.
- **Linear and stationary.** A fixed V-cycle is a linear operator $v \mapsto M v + N f$; with $\nu_1 = \nu_2$ and a symmetric smoother (such as weighted Jacobi, or Gauss-Seidel forward before and backward after), it is a symmetric preconditioner for [conjugate gradients](/conjugate-gradient-method/).
- **Not in place.** It needs the coarse grids, less than $2n$ extra words in 1D and $n/3$ in 2D.
- **Problem dependent.** The smoother and transfer operators must match the problem; for strongly anisotropic or discontinuous coefficients the standard components lose their efficiency.

## Variants and improvements

- **Cycle shapes.** The W-cycle visits each coarse level twice per visit of the next finer one; it is more robust and costs a constant factor more in 2D and 3D. F-cycles lie between V and W.
- **Full multigrid (FMG),** described above.
- **Smoothers.** Gauss-Seidel in lexicographic or red-black order (smoothing factor $1/2$ in 2D for lexicographic Gauss-Seidel, by Brandt's local mode analysis), weighted Jacobi with $\omega = 4/5$ in 2D (smoothing factor $3/5$), line relaxation and semicoarsening for anisotropic problems, and incomplete factorizations.
- **Multigrid as a preconditioner.** One V-cycle as $M^{-1}$ inside [conjugate gradients](/conjugate-gradient-method/) or GMRES, which adds robustness when some modes are poorly handled.
- **[Algebraic multigrid](/algebraic-multigrid/).** Builds the coarse levels from the matrix entries alone, for unstructured meshes and problems without a grid hierarchy.
- **Nonlinear problems.** The full approximation scheme (FAS) applies the same idea to nonlinear equations without linearizing globally.

## When to use it

Use multigrid for large elliptic problems: Poisson and diffusion equations, linear elasticity, and the pressure equation in flow solvers, especially in 2D and 3D on structured grids, where it is the fastest known method. Use algebraic multigrid when there is no natural grid hierarchy, and use multigrid as a preconditioner when the problem is not quite elliptic. For small problems, or problems that are strongly indefinite (high-frequency Helmholtz) or convection dominated, standard multigrid loses its advantage, and direct solvers or other preconditioned Krylov methods may be better.

## Pitfalls

- **A smoother that does not smooth.** Unweighted Jacobi ($\omega = 1$) leaves the highest mode almost unchanged (factor $\approx -1$), and $\omega > 1$ amplifies it; Gauss-Seidel or $\omega = 2/3$ are safe for the model problem.
- **Mismatched transfers.** If $R_l$, $P_l$ and the coarse matrix are inconsistent (for example, the wrong scaling of $h^{-2}$ on the coarse grid), the coarse correction has the wrong size and convergence slows or fails. Galerkin coarse matrices $R A P$ avoid this.
- **Anisotropy and jumps in coefficients.** Point smoothers do not smooth errors that are smooth in one direction only; line smoothers, semicoarsening or algebraic multigrid are needed.
- **Grid sizes.** Standard coarsening needs grids that can be halved repeatedly, such as $2^L - 1$ points; other sizes need care at the boundaries.
- **Tolerance below rounding level.** The residual stalls near $u\,\|A\|\,\|v^\ast\|$; for PDEs, stopping at the discretization error saves most of the work.

## Implementations

## History

Fedorenko (1961, 1964) introduced the method for the Poisson equation on a square and proved its convergence, and Bakhvalov (1966) showed that its work is $O(n)$ for general elliptic problems with variable coefficients. The idea became practical through Brandt's 1973 and 1977 papers, which introduced local mode analysis, full multigrid and adaptive refinement, and through Hackbusch's convergence theory (1976 onward) and his 1985 book *Multi-Grid Methods and Applications*. Braess and Hackbusch (1983) proved mesh-independent V-cycle convergence. Ruge and Stüben developed algebraic multigrid in the 1980s. *A Multigrid Tutorial* by Briggs (1987; second edition with Henson and McCormick, 2000) made the method widely known.

## References
