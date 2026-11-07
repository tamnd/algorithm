---
tag: QAMAC5
kind: algorithm
slug: conjugate-gradient-method
name: Conjugate gradient method
aliases:
- CG
- conjugate gradients
- Hestenes-Stiefel method
area: numerical/linear-systems
level: core
summary: Krylov method for symmetric positive definite systems that minimizes the A-norm error.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of A", z: "the number of nonzeros of A", κ: "the condition number κ_2(A)", ε: "the factor by which the A-norm of the error must drop"}
  time: {worst: "O((z + n) κ^(1/2) log(2/ε))"}
  space: {extra: Θ(n)}
  matvecs: {worst: "⌈κ^(1/2) ln(2/ε)/2⌉ + 1"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true, matrix_free: true}
prereqs: [krylov-subspace, positive-definite-matrix, linear-system-solving]
see_also: [gmres, minres, preconditioning, incomplete-cholesky-factorization, chebyshev-iteration, lanczos-algorithm, cholesky-decomposition, nonlinear-conjugate-gradient]
sources:
  - paper: doi:10.6028/jres.049.044
    title: Magnus R. Hestenes and Eduard Stiefel, Methods of conjugate gradients for solving linear systems, Journal of Research of the National Bureau of Standards 49(6), 1952
    locator: pp. 409 to 436 (the algorithm, the orthogonality and conjugacy relations, the minimization property and finite termination)
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 6.7, The Conjugate Gradient Algorithm; Section 6.11.3, Convergence of the CG algorithm (the Chebyshev bound)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 38, Conjugate Gradients (Theorem 38.1, the orthogonality relations; Theorem 38.2, the A-norm optimality; Theorem 38.5, the bound in terms of the square root of κ)
  - book: isbn:9780898713961
    title: Anne Greenbaum, Iterative Methods for Solving Linear Systems, SIAM, 1997
    locator: Chapter 2 (the derivation of CG), Chapter 3, Error Bounds for CG, MINRES and GMRES, and Chapter 4, Effects of Finite Precision Arithmetic
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 11.3, The Conjugate Gradient Method; Section 11.5, Preconditioning
  - paper: doi:10.1137/1031003
    title: Gene H. Golub and Dianne P. O'Leary, Some history of the conjugate gradient and Lanczos algorithms 1948 to 1976, SIAM Review 31(1), 1989
    locator: pp. 50 to 102 (the history, including the revival as an iterative method in the 1970s)
  - paper: "Anne Greenbaum, Behavior of slightly perturbed Lanczos and conjugate-gradient recurrences, Linear Algebra and its Applications 113, 1989"
    locator: pp. 7 to 63 (finite precision CG behaves like exact CG on a larger matrix with clustered eigenvalues)
  - paper: "Anne Greenbaum, Estimating the attainable accuracy of recursively computed residual methods, SIAM Journal on Matrix Analysis and Applications 18(3), 1997"
    locator: pp. 535 to 551 (the gap between the updated and the true residual)
---

The conjugate gradient method (CG) solves $A x = b$ for a [symmetric positive definite](/positive-definite-matrix/) $A$ using only products $v \mapsto A v$. Its iterate $x_k$ minimizes the $A$-norm of the error $\|x - x_k\|_A = ((x - x_k)^T A (x - x_k))^{1/2}$ over the affine [Krylov subspace](/krylov-subspace/) $x_0 + \mathcal{K}_k(A, r_0)$, with short recurrences: each step costs one product with $A$, two inner products and three vector updates, and keeps four vectors. In exact arithmetic it stops with the solution in at most $n$ steps, and the error drops by at least a factor $2 ((\sqrt\kappa - 1)/(\sqrt\kappa + 1))^k$ after $k$ steps, where $\kappa = \kappa_2(A)$. With a good [preconditioner](/preconditioning/), it is the standard solver for large sparse symmetric positive definite systems.

## In plain words

Solving the system is the same as finding the lowest point of a bowl-shaped surface, because the slope of that surface is zero exactly at the solution. Going straight downhill again and again is slow when the bowl is long and narrow: the steps zigzag across the valley. The conjugate gradient method picks each new direction so that it does not spoil the progress made along the earlier directions. As a result, each step makes the error as small as it can be using all the information gathered so far.

The method needs only a way to multiply the matrix by a vector, so it works for huge sparse matrices that never fit as a dense table. The number of steps depends on how stretched the bowl is: the more stretched, the more steps.

## The problem

**Notation.** As in [solving linear systems](/linear-system-solving/): $A$ is $n \times n$ symmetric positive definite, $x$ the solution of $A x = b$, $x_k$ the iterate, $r_k = b - A x_k$ the residual, $e_k = x - x_k$ the error, $\|v\|_A = (v^T A v)^{1/2}$, $\kappa = \kappa_2(A) = \lambda_{\max}/\lambda_{\min}$, and $\mathcal{K}_k(A, r_0) = \operatorname{span}\{r_0, A r_0, \ldots, A^{k-1} r_0\}$. Cost is counted in products with $A$ (matvecs) and flops; $z$ is the number of nonzeros of $A$.

Input: a way to compute $A v$, the right side $b$, a start $x_0$ (often $0$), a tolerance $\text{tol}$ and a step limit. Output: $x_k$ with $\|r_k\|_2 \le \text{tol} \cdot \|b\|_2$, or the last iterate with a flag that the test was not met. Since $\nabla \phi(y) = A y - b$ for $\phi(y) = \tfrac12 y^T A y - b^T y$, solving $A x = b$ is the same as minimizing $\phi$, and $\phi(y) - \phi(x) = \tfrac12 \|y - x\|_A^2$.

## The algorithm

```pseudo id=main
CG(A, b, x, tol, maxit)                    ▷ x is the start x₀
L1  r ← b − A x;  p ← r;  ρ ← rᵀr
L2  for k ← 0 to maxit − 1 do
L3      if ρ ≤ tol² · bᵀb then return (x, CONVERGED)
L4      q ← A p
L5      α ← ρ / (pᵀq)                      ▷ pᵀq ≤ 0 means A is not positive definite
L6      x ← x + α p
L7      r ← r − α q
L8      ρ' ← rᵀr
L9      β ← ρ' / ρ;  ρ ← ρ'
L10     p ← r + β p
L11 return (x, NOT-CONVERGED)
```

Line L5 picks the step $\alpha$ that minimizes $\phi(x + \alpha p)$ along the direction $p$. Line L7 updates the residual without a second product with $A$: $b - A(x + \alpha p) = r - \alpha A p$. Line L10 makes the new direction $A$-conjugate to the old one ($p_{k+1}^T A p_k = 0$), and the theorem below shows that it is then conjugate to all earlier directions too. That is why three-term memory is enough.

**Preconditioned CG.** With a symmetric positive definite $M \approx A$ whose systems are cheap, replace line L1 by $z \leftarrow M^{-1} r$, $p \leftarrow z$, $\rho \leftarrow r^T z$, and after line L7 set $z \leftarrow M^{-1} r$, $\rho' \leftarrow r^T z$, $p \leftarrow z + \beta p$. This is CG on $M^{-1/2} A M^{-1/2}$, so $\kappa$ in the bounds becomes $\kappa_2(M^{-1} A)$. [Incomplete Cholesky](/incomplete-cholesky-factorization/) and [algebraic multigrid](/algebraic-multigrid/) are common choices of $M$.

## Example

Let $A$ be the $5 \times 5$ tridiagonal matrix with $2$ on the diagonal and $-1$ next to it (the 1D Laplacian), $b = (1, 1, 1, 1, 1)^T$ and $x_0 = 0$. The solution is $x = (5/2, 4, 9/2, 4, 5/2)^T$. In exact arithmetic:

| $k$ | $x_k$ | $\rho_k = \|r_k\|_2^2$ | $\|e_k\|_A^2$ | $\alpha_k$ | $\beta_k$ |
|---|---|---|---|---|---|
| 0 | $(0, 0, 0, 0, 0)$ | $5$ | $35/2$ | $5/2$ | $3/2$ |
| 1 | $(5/2, 5/2, 5/2, 5/2, 5/2)$ | $15/2$ | $5$ | $3/5$ | $1/5$ |
| 2 | $(5/2, 4, 4, 4, 5/2)$ | $3/2$ | $1/2$ | $1/3$ | $0$ |
| 3 | $(5/2, 4, 9/2, 4, 5/2)$ | $0$ | $0$ | | |

Two things show here. First, CG stops after 3 steps, not 5: $b$ is symmetric about the middle, so it has components along only 3 of the 5 eigenvectors of $A$, and $\mathcal{K}_k(A, b)$ has dimension at most 3. Second, the residual norm goes up from step 0 to step 1 ($5$ to $15/2$) while the $A$-norm of the error goes down at each step ($35/2$, $5$, $1/2$, $0$): CG minimizes the error in the $A$-norm, not the residual.

## Correctness

In exact arithmetic, as long as $r_0, \ldots, r_{k-1}$ are nonzero:

1. $\mathcal{K}_k(A, r_0) = \operatorname{span}\{p_0, \ldots, p_{k-1}\} = \operatorname{span}\{r_0, \ldots, r_{k-1}\}$, and $x_k - x_0$ lies in it;
2. the residuals are orthogonal: $r_k^T r_j = 0$ for $j < k$;
3. the directions are conjugate: $p_k^T A p_j = 0$ for $j < k$;
4. $x_k$ is the unique minimizer of $\|x - y\|_A$ over $y \in x_0 + \mathcal{K}_k(A, r_0)$;
5. some $r_k$ with $k \le n$ is zero, so CG returns the exact solution after at most $n$ steps (and after at most $d$ steps, where $d$ is the number of distinct eigenvalues of $A$ whose eigenvectors appear in $r_0$).

The proof is an induction on $k$ (Hestenes and Stiefel 1952; Trefethen and Bau, Theorems 38.1 and 38.2), in [the proof](proofs/correctness.md).

**Finite precision.** Statements 2 and 3 fail in floating point: the residuals lose orthogonality, and finite termination does not hold. What survives is convergence. Greenbaum (1989) showed that CG in finite precision behaves like exact CG on a larger matrix whose eigenvalues lie in small intervals around those of $A$, so the bounds below still describe the observed behavior, with some delay when $A$ has isolated large eigenvalues (Greenbaum, Chapter 4). The updated residual of line L7 and the true residual $b - A x_k$ also drift apart. The true residual stops decreasing at a level of the order of $u \, \|A\| \max_j \|x_j\|$, while the updated one keeps decreasing (Greenbaum 1997). A stopping test on the updated residual must therefore be checked against the true residual at the end.

## Complexity

**Cost per step.** One matvec (about $2z$ flops for a matrix with $z$ nonzeros), two inner products ($4n$ flops) and three vector updates ($6n$ flops): about $2z + 10n$ flops, plus one solve with $M$ if preconditioned. The memory is four vectors $x, r, p, q$ besides $A$. For sparse $A$ these operations read each nonzero once per step, so the speed is bound by memory traffic, and the inner products need a global reduction on a parallel machine.

**Number of steps.** The proved bound (Saad, Section 6.11.3; Trefethen and Bau, Theorem 38.5) is
$$\frac{\|e_k\|_A}{\|e_0\|_A} \le 2 \left( \frac{\sqrt\kappa - 1}{\sqrt\kappa + 1} \right)^k.$$
Since $\ln((\sqrt\kappa + 1)/(\sqrt\kappa - 1)) \ge 2/\sqrt\kappa$, the error drops by a factor $\varepsilon$ after at most $\lceil \tfrac12 \sqrt\kappa \ln(2/\varepsilon) \rceil$ steps. The proof uses Chebyshev polynomials and is in [the complexity proof](proofs/complexity.md). This is a worst-case bound over the right sides, and it uses only the two extreme eigenvalues. CG often does much better: clustered eigenvalues give fast convergence, and an isolated eigenvalue costs about one extra step ("superlinear convergence" as the extreme eigenvalues are found). Compare steepest descent, whose factor per step is $(\kappa - 1)/(\kappa + 1)$, so it needs about $\kappa$ instead of $\sqrt\kappa$ steps.

For the 2D Poisson equation on an $m \times m$ grid ($n = m^2$, $\kappa = \Theta(m^2)$), CG needs $O(m) = O(\sqrt n)$ steps, each $O(n)$ flops, for $O(n^{3/2})$ flops in total. Banded Cholesky costs $O(n^2)$ flops there, Cholesky after [nested dissection](/nested-dissection/) $O(n^{3/2})$ flops with $O(n \log n)$ memory, and [multigrid](/multigrid-method/) $O(n)$ flops.

## Properties

- **Matrix free.** Only products $A v$ are needed.
- **Optimal.** For each $k$, no method that takes $x_k$ from $x_0 + \mathcal{K}_k(A, r_0)$ has a smaller $A$-norm error.
- **Monotone in the $A$-norm.** $\|e_k\|_A$ is non-increasing; $\|r_k\|_2$ need not be.
- **Short recurrences.** Constant memory and work per step, unlike [GMRES](/gmres/), whose work per step grows.
- **Requires symmetry and positive definiteness.** For symmetric indefinite $A$ use [MINRES](/minres/); for nonsymmetric $A$ use GMRES or [BiCGSTAB](/bicgstab/).

## Variants and improvements

- **Preconditioned CG**, above; the most used form in practice.
- **CG on the normal equations** (CGNR, CGNE) for nonsymmetric or least squares problems, at the price of $\kappa_2(A)^2$.
- **Pipelined and communication-avoiding CG** reorder the inner products to hide the latency of global reductions on parallel machines, at some cost in stability.
- **Block CG** for many right sides.
- **Deflated CG** removes known eigenvectors of small eigenvalues.
- **Nonlinear CG** applies the same idea to minimize a general smooth function; see [nonlinear conjugate gradient](/nonlinear-conjugate-gradient/).
- **Lanczos connection.** CG computes the same Krylov basis as the [Lanczos algorithm](/lanczos-algorithm/); its coefficients $\alpha_k, \beta_k$ give the Lanczos tridiagonal matrix, and so estimates of the extreme eigenvalues and of $\kappa$.

## When to use it

Use CG (with a preconditioner) for large sparse symmetric positive definite systems, for example from elliptic partial differential equations, when a sparse [Cholesky](/cholesky-decomposition/) factor would need too much memory because of [fill-in](/fill-in/). For small or dense systems, or many right sides with the same matrix, a direct factorization is faster and more robust. If $A$ is only symmetric, CG can break down at line L5; use MINRES.

## Pitfalls

- **Using CG on a matrix that is not symmetric positive definite.** Line L5 then can divide by zero or by a negative $p^T q$, and the iteration has no meaning. Test $p^T q > 0$ at line L5, or use MINRES or GMRES.
- **A nonsymmetric preconditioner.** Preconditioned CG needs $M$ symmetric positive definite. A Gauss-Seidel sweep, for example, is not symmetric; use the symmetric (forward and backward) sweep.
- **Trusting the updated residual.** Line L7 accumulates rounding errors, so at convergence compute $b - A x_k$ once and check it.
- **Testing the residual only.** A small $\|r_k\|$ bounds the error only through $\|e_k\|_2 \le \|A^{-1}\|_2 \|r_k\|_2$, and $\|A^{-1}\|$ can be large; the forward error can be $\kappa$ times the relative residual.
- **Recomputing $\rho$ wrongly.** Line L9 needs the new $r^T r$ divided by the old one; using $r^T q$ or the old $\rho$ twice destroys conjugacy, and the method becomes steepest descent with a bad step.

## Implementations

## History

Hestenes and Stiefel published the method in 1952, after they had found it independently at the Institute for Numerical Analysis in Los Angeles and at ETH Zurich; Lanczos published a closely related method in the same year. It was first seen as a direct method that terminates after $n$ steps, and it fell out of use when rounding errors were found to destroy that property. Reid (1971) and others revived it as an iterative method for large sparse systems, and preconditioning, notably incomplete Cholesky (Meijerink and van der Vorst 1977), made it the standard method. Golub and O'Leary (1989) give the full history.

## References
