---
tag: XP4DQX
kind: technique
slug: preconditioning
name: Preconditioning
aliases:
- preconditioner
- preconditioned iteration
- left and right preconditioning
area: numerical/linear-systems
level: core
summary: Transform a system to a better-conditioned one so iterative methods converge faster.
prereqs: [condition-number, krylov-subspace, matrix-splitting]
see_also: [conjugate-gradient-method, gmres, minres, incomplete-cholesky-factorization, multigrid-method, domain-decomposition, successive-over-relaxation, schur-complement]
sources:
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Chapter 9, Preconditioned Iterations (preconditioned CG and GMRES, left, right and split preconditioning); Chapter 10, Preconditioning Techniques (Jacobi, SOR and SSOR, ILU and its variants, approximate inverses, block preconditioners)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 11.5, Preconditioning (preconditioned conjugate gradients, incomplete Cholesky, polynomial and domain decomposition preconditioners)
  - paper: doi:10.1006/jcph.2002.7176
    title: Michele Benzi, Preconditioning techniques for large linear systems, a survey, Journal of Computational Physics 182(2), 2002
    locator: the survey of incomplete factorizations, sparse approximate inverses, multilevel preconditioners and their history
  - paper: doi:10.1017/S0962492915000021
    title: Andrew J. Wathen, Preconditioning, Acta Numerica 24, 2015
    locator: the role of the spectrum and of the norm in which convergence is measured, and preconditioners built from the structure of the problem
  - book: isbn:9780898713961
    title: Anne Greenbaum, Iterative Methods for Solving Linear Systems, SIAM, 1997
    locator: Part II, Preconditioners (the comparison of preconditioners, incomplete decompositions, multigrid and domain decomposition)
---

Preconditioning replaces $A x = b$ by an equivalent system, such as $M^{-1} A x = M^{-1} b$, whose matrix has a spectrum a Krylov method can handle in a few steps. The preconditioner $M$ must do two things at once: approximate $A$ well enough that $M^{-1}A$ has clustered eigenvalues (or a small condition number), and be cheap enough that solving $M z = r$ costs about as much as a product with $A$. Between $M = I$ (no help, no cost) and $M = A$ (one step, a full solve) lie the Jacobi, SSOR, incomplete factorization, multigrid, domain decomposition and block preconditioners that make large sparse iterative solvers practical.

## In plain words

An iterative method is fast when the matrix stretches all directions by about the same amount, and slow when some directions are stretched a thousand times more than others. Preconditioning means finding a rough, cheap copy of the matrix that you can undo easily, and undoing it at every step. What is left after undoing is close to doing nothing, which the iteration handles quickly. A good rough copy captures the large-scale behavior of the problem; a perfect copy would solve the problem by itself, so the art is in how much to spend.

## When it applies

**Notation.** $A \in \mathbb{R}^{n \times n}$ nonsingular, $b$, $x$; the iterate $x_k$, residual $r_k = b - A x_k$ and Krylov space $\mathcal{K}_k(B, c)$ as on the page [Krylov subspace](/krylov-subspace/); $\kappa_2$ is the 2-norm condition number and $u = 2^{-53}$. The preconditioner is $M \approx A$, nonsingular, and $z = M^{-1} r$ is the preconditioned residual.

Three ways to apply $M$:

- **Left:** $M^{-1} A x = M^{-1} b$. The method sees the residual $M^{-1} r_k$, which is what GMRES then minimizes.
- **Right:** $A M^{-1} y = b$, $x = M^{-1} y$. The method minimizes the true residual $r_k$; the iterates are $x_k \in x_0 + M^{-1}\mathcal{K}_k(A M^{-1}, r_0)$.
- **Split:** $M = M_1 M_2$ and $M_1^{-1} A M_2^{-1}$. For symmetric positive definite $A$ and $M = L L^T$, the matrix $L^{-1} A L^{-T}$ is SPD again, which is what [conjugate gradients](/conjugate-gradient-method/) need. In practice preconditioned CG is written with $M^{-1}$ only, and it is CG in the $M$-inner product.

What decides the speed:

- **SPD case (proved).** Preconditioned CG satisfies $\|e_k\|_A \le 2\big(\frac{\sqrt{\kappa} - 1}{\sqrt\kappa + 1}\big)^k \|e_0\|_A$ with $\kappa = \kappa_2(L^{-1}AL^{-T}) = \lambda_{\max}(M^{-1}A)/\lambda_{\min}(M^{-1}A)$. If $M^{-1}A$ has only $s$ distinct eigenvalues, CG ends in at most $s$ steps in exact arithmetic. Spectral equivalence, $c_1 \le \frac{v^T A v}{v^T M v} \le c_2$ for all $v$ with constants independent of the mesh, gives a mesh-independent number of steps.
- **Nonsymmetric case.** For GMRES the eigenvalues alone do not determine convergence; clustering of eigenvalues away from the origin is the usual heuristic, and the field of values or a bound on $\|I - M^{-1}A\|$ give proved bounds. If $\|I - M^{-1}A\| \le \delta < 1$, the preconditioned residual drops at least by $\delta$ per step (a [Neumann series](/neumann-series/) argument).

It applies to any Krylov method and to stationary iterations: a [splitting](/matrix-splitting/) $A = M - N$ is Richardson iteration on $M^{-1}A$, so every splitting is a preconditioner and every preconditioner defines a splitting.

## The template

```pseudo id=main
PRECONDITIONED-KRYLOV(A, b, x_0, tol)
L1  build M ≈ A and a way to solve M z = r          ▷ hole: the preconditioner and its setup
L2  x ← x_0;  r ← b − A x
L3  z ← SOLVE(M, r)                                 ▷ hole: the application of M^-1
L4  k ← 0
L5  while ‖r‖_2 > tol · ‖b‖_2 do                    ▷ hole: the stopping test and its norm
L6      k ← k + 1
L7      one step of the Krylov method on M^-1 A,     ▷ hole: the outer method (CG, MINRES, GMRES, BiCGSTAB)
          using one product with A and z
L8      z ← SOLVE(M, r)
L9  return x
```

The holes are the preconditioner (L1), how it is applied (L3, L8: a pair of triangular solves for an incomplete factorization, a V-cycle for multigrid, a product for an approximate inverse), the outer Krylov method (L7), which must match the symmetry of $M^{-1}A$, and the stopping test (L5). The total cost is the number of steps times (one product with $A$ + one application of $M^{-1}$ + the vector work of the method), plus the setup of L1. A preconditioner pays off when the steps saved outweigh both.

## Classic examples

**Jacobi (diagonal scaling).** $M = \mathrm{diag}(A)$. Free to build and apply, and fully parallel. It helps exactly when the rows have very different scales. For $A = S\,T\,S$ with $T = \mathrm{tridiag}(-1, 2, -1)$ of order $100$ and $S$ diagonal with entries $10^{t}$, $t$ uniform in $[-3, 3]$ (seed 5), plain CG needs $18948$ steps to reach a relative residual of $10^{-8}$ in floating point, while Jacobi-preconditioned CG needs $100$, because $D^{-1/2} A D^{-1/2} = T/2$. On the 5-point Laplacian the diagonal is constant and Jacobi changes nothing.

**SSOR and symmetric Gauss-Seidel.** $M = \frac{\omega}{2-\omega}(D/\omega - E) D^{-1} (D/\omega - E^T)$ for $A = D - E - E^T$, the symmetric version of [SOR](/successive-over-relaxation/). No setup; one forward and one backward triangular sweep per application.

**Incomplete Cholesky and ILU.** Run Cholesky or LU but drop fill outside a chosen pattern: IC(0) keeps the pattern of $A$, IC($p$) and ILUT allow more by level or by size ([incomplete Cholesky](/incomplete-cholesky-factorization/), [incomplete LU](/incomplete-lu-factorization/)). Meijerink and van der Vorst (1977) proved IC exists for M-matrices. For the 5-point Laplacian on an $m \times m$ grid, $b = (1, \ldots, 1)$ and a relative residual of $10^{-8}$, preconditioned CG takes:

| $m$ | none or Jacobi | symmetric Gauss-Seidel | IC(0) |
|---|---|---|---|
| 16 | 28 | 19 | 17 |
| 32 | 59 | 34 | 29 |
| 64 | 119 | 60 | 52 |

All three columns roughly double when $m$ doubles: these preconditioners leave $\kappa(M^{-1}A) = O(h^{-2})$ and only improve the constant. Modified IC, which keeps row sums, gives $O(h^{-1})$ under conditions on the matrix (Gustafsson).

**Multigrid as a preconditioner.** One V-cycle of [multigrid](/multigrid-method/) or [algebraic multigrid](/algebraic-multigrid/) is spectrally equivalent to $A$ for elliptic problems, so the number of CG steps stays bounded as the mesh is refined, at $O(n)$ cost per step.

**Domain decomposition.** Additive Schwarz solves on overlapping subdomains in parallel; with a coarse space the condition number becomes independent of the number of subdomains ([domain decomposition](/domain-decomposition/)).

**Block preconditioners for saddle points.** For $\begin{pmatrix} A & B^T \\ B & 0 \end{pmatrix}$, the block diagonal $M = \mathrm{diag}(A, B A^{-1} B^T)$ gives a preconditioned matrix with exactly three eigenvalues $1$ and $\tfrac12(1 \pm \sqrt5)$, so [MINRES](/minres/) converges in three steps; in practice $A$ and the [Schur complement](/schur-complement/) are replaced by cheap approximations.

## Variations

- **Polynomial preconditioners.** $M^{-1} = p(A)$, for example a truncated Neumann series or a Chebyshev polynomial; only products with $A$, good on vector and parallel hardware, but rarely better than more steps of the Krylov method.
- **Sparse approximate inverses.** Choose $M^{-1}$ with a given sparsity pattern to minimize $\|I - A M^{-1}\|_F$ column by column; application is a sparse product, fully parallel.
- **Flexible preconditioning.** If $M$ changes from step to step (an inner iteration, a multigrid cycle with a tolerance), use flexible GMRES or flexible CG, which store the preconditioned vectors.
- **Physics-based and operator preconditioning.** Use a simpler PDE, a coarser discretization or the right norm of the continuous problem to design $M$ (Wathen, 2015).
- **Deflation and augmentation.** Remove a few known small eigenvalues by projection, which a fixed $M$ cannot do cheaply.

## Pitfalls

- **Checking the wrong residual.** With left preconditioning, $\|M^{-1} r_k\|$ can be small while $\|r_k\|$ is not; with an ill-conditioned $M$, report and test the true residual.
- **Breaking symmetry.** CG needs a symmetric positive definite $M$; SOR, ILU of a symmetric matrix with a nonsymmetric pattern or a nonsymmetric multigrid cycle break it, and CG may fail. Use the symmetric version or a nonsymmetric method.
- **Breakdown of incomplete factorizations.** IC(0) can meet a nonpositive pivot on SPD matrices that are not M-matrices, and ILU can produce huge unstable triangular factors on indefinite or strongly nonsymmetric matrices; diagonal shifts and pivoting are the usual cures.
- **Counting steps instead of time.** A preconditioner that halves the steps but doubles the cost per step, or does not parallelize (triangular solves are sequential), may be slower overall. Setup cost matters when only one system is solved.
- **Rounding in the preconditioner.** $M$ need only be applied approximately, but the outer method assumes the same $M$ every step; an inexact inner solve needs a flexible method.
- **Ill-conditioned $M$.** If $M$ is much worse conditioned than $A$, the computed $M^{-1} r$ can be inaccurate and the attainable accuracy of the outer iteration drops; this is observed in practice rather than covered by a general bound.

## Exercises

1. Show that preconditioned CG with $M = L L^T$ produces the same $x_k$ as CG applied to $L^{-1} A L^{-T} y = L^{-1} b$ with $x_k = L^{-T} y_k$, and that it can be written with $M^{-1}$ only.
2. Show that $M^{-1}A$, $A M^{-1}$ and $L^{-1}AL^{-T}$ (for $M = L L^T$) have the same eigenvalues.
3. For $A = S T S$ with $S$ diagonal positive, prove that the Jacobi preconditioner removes $S$ completely, and that $\kappa_2(A)$ can be as large as $\kappa_2(T)\,\kappa_2(S)^2$.
4. For the saddle point matrix with $M = \mathrm{diag}(A, B A^{-1} B^T)$, $A$ SPD and $B$ of full row rank, prove that $M^{-1}\mathcal{A}$ has the eigenvalues $1$ and $\tfrac12(1 \pm \sqrt5)$ only.
5. Show that if $\|I - M^{-1}A\|_2 \le \delta < 1$, then GMRES on $M^{-1}A$ reduces the preconditioned residual by at least $\delta^k$ in $k$ steps.
6. Implement IC(0) for the 5-point Laplacian and reproduce the table above; then implement modified IC and measure how the step count grows with $m$.

## References
