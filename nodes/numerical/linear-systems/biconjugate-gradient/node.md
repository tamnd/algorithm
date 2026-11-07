---
tag: 4SSPDC
kind: algorithm
slug: biconjugate-gradient
name: Biconjugate gradient method
aliases:
- BiCG
- biconjugate gradients
- two-sided Lanczos method for linear systems
area: numerical/linear-systems
level: advanced
summary: Extends conjugate gradients to nonsymmetric systems using a shadow sequence.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of A", z: "the number of nonzeros of A", k: "the number of iterations"}
  time: {worst: O(k z + k n)}
  space: {extra: Θ(n)}
  matvecs: {per_step: "2"}
  flops: {per_step: "4 z + 16 n + O(1)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true}
prereqs: [conjugate-gradient-method, krylov-subspace, lanczos-algorithm]
see_also: [bicgstab, gmres, conjugate-gradient-method, minres, preconditioning, incomplete-lu-factorization, arnoldi-iteration, sparse-linear-systems]
sources:
  - paper: "Roger Fletcher, Conjugate gradient methods for indefinite systems, in G. A. Watson (ed.), Numerical Analysis Dundee 1975, Lecture Notes in Mathematics 506, Springer, 1976"
    title: R. Fletcher, Conjugate gradient methods for indefinite systems
    locator: pp. 73 to 89 (the biconjugate gradient algorithm in its modern form)
  - paper: doi:10.6028/jres.049.006
    title: Cornelius Lanczos, Solution of systems of linear equations by minimized iterations, Journal of Research of the National Bureau of Standards 49(1), 1952
    locator: pp. 33 to 53 (the two-sided recurrences behind BiCG)
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 7.1, Lanczos Biorthogonalization; Section 7.3.1, The Biconjugate Gradient Algorithm (Algorithm 7.3 and its biorthogonality properties); Section 7.3.2, Quasi-Minimal Residual
  - book: isbn:9780898713961
    title: Anne Greenbaum, Iterative Methods for Solving Linear Systems, SIAM, 1997
    locator: Section 2.5, Non-Hermitian Lanczos (BiCG and QMR, and the relation between their residual norms); Section 5.4, the attainable accuracy of methods based on updated residuals
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 11.5.3, the biconjugate gradient method
  - paper: doi:10.1007/BF01385726
    title: Roland W. Freund and Noël M. Nachtigal, QMR, a quasi-minimal residual method for non-Hermitian linear systems, Numerische Mathematik 60, 1991
    locator: pp. 315 to 339 (smoothing BiCG and look-ahead against breakdown)
---

The biconjugate gradient method (BiCG) extends the [conjugate gradient method](/conjugate-gradient-method/) to a nonsymmetric matrix $A$. Next to the residuals $r_k$ of $A x = b$ it runs a shadow sequence $\tilde r_k$ driven by $A^T$, and it keeps the two sequences biorthogonal, $\tilde r_i^T r_j = 0$ for $i \ne j$, instead of orthogonal. That makes the recurrences as short as in CG: $O(n)$ storage and two matvecs, one with $A$ and one with $A^T$, per step. The price is that BiCG minimizes nothing, so its residuals can rise and fall erratically, and the recurrences can break down by division by zero. In exact arithmetic, without breakdown, it terminates in at most $n$ steps. It was given in its modern form by Fletcher (1976), from Lanczos (1952), and is the parent of [BiCGSTAB](/bicgstab/), CGS and QMR.

## In plain words

Conjugate gradients works because a symmetric matrix lets each new search direction be checked against only the last one. A nonsymmetric matrix breaks that. BiCG repairs it by running a twin problem with the transposed matrix and checking each direction against the twin's directions instead. The checks stay short, so the cost per step stays small.

The cost of the trick is that nothing guarantees steady progress: the error can jump up before it goes down, and in rare cases the method has to divide by zero and stop.

## The problem

**Notation.** As in [solving linear systems](/linear-system-solving/): $A \in \mathbb{R}^{n \times n}$ nonsingular and possibly nonsymmetric, $x_k$ the iterate, $r_k = b - A x_k$, $\mathcal K_k(A, r_0)$ the [Krylov subspace](/krylov-subspace/), $\kappa(A)$ the condition number, $u = 2^{-53}$. The shadow residual $\tilde r_0$ is any vector with $\tilde r_0^T r_0 \ne 0$; the usual choice is $\tilde r_0 = r_0$. $z$ is the number of nonzeros of $A$.

Given $A$ (through products with $A$ and $A^T$), $b$, $x_0$ and a tolerance, return $x_k$ with $\|r_k\|_2 \le \mathrm{tol} \cdot \|b\|_2$, or report NOT-CONVERGED or one of two breakdowns.

## The algorithm

```pseudo id=main
BiCG(A, b, x, r̃, tol, kmax)                 ▷ x is x₀;  r̃ is the shadow r̃₀ (default r₀)
L1  r ← b − A x
L2  p ← r;  p̃ ← r̃;  ρ ← r̃ᵀ r
L3  for k ← 0 to kmax do
L4      if ‖r‖₂ ≤ tol · ‖b‖₂ then return (x, k, CONVERGED);  if ρ = 0 then return RHO-BREAKDOWN
L5      q ← A p;  q̃ ← Aᵀ p̃;  σ ← p̃ᵀ q;  if σ = 0 then return PIVOT-BREAKDOWN
L6      α ← ρ / σ
L7      x ← x + α p;  r ← r − α q
L8      r̃ ← r̃ − α q̃
L9      ρ_new ← r̃ᵀ r;  β ← ρ_new / ρ;  ρ ← ρ_new
L10     p ← r + β p;  p̃ ← r̃ + β p̃
```

Lines L5 to L10 are CG with every inner product $v^T w$ replaced by the bilinear pairing of a shadow vector with a primal one. If $A$ is symmetric and $\tilde r_0 = r_0$, the shadow vectors equal the primal ones and BiCG is CG computed twice.

## Example

$$A = \begin{pmatrix} 2 & 1 & 0 \\ -1 & 2 & 1 \\ 0 & -1 & 2 \end{pmatrix}, \quad b = \begin{pmatrix} 1 \\ 1 \\ 1 \end{pmatrix}, \quad x_0 = 0, \quad \tilde r_0 = r_0 = b.$$
The exact solution is $x = (1/3, 1/3, 2/3)$. In rational arithmetic (the test file runs this with `Fraction`):

| $k$ | $r_k$ | $\tilde r_k$ | $\|r_k\|_2^2$ |
|---|---|---|---|
| 0 | $(1, 1, 1)$ | $(1, 1, 1)$ | $3$ |
| 1 | $(-1/2, 0, 1/2)$ | $(1/2, 0, -1/2)$ | $1/2$ |
| 2 | $(1/7, -2/7, 1/7)$ | $(1/7, -2/7, 1/7)$ | $6/49$ |
| 3 | $0$ | $0$ | $0$ |

Step 0 has $\rho = 3$, $q = A p = (3, 2, 1)$, $\tilde q = A^T \tilde p = (1, 2, 3)$, $\sigma = 6$, $\alpha = 1/2$. One checks $\tilde r_0^T r_1 = 0$, $\tilde r_1^T r_2 = 1/14 - 1/14 = 0$ and $\tilde r_0^T r_2 = 0$. After three steps $x_3 = x$ exactly.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). In exact arithmetic and as long as no breakdown occurs ($\rho \ne 0$, $\sigma \ne 0$):

1. **Biorthogonality.** $\tilde r_i^T r_j = 0$ and $\tilde p_i^T A p_j = 0$ for $i \ne j$ (Saad, Section 7.3.1).
2. **Petrov-Galerkin condition.** $x_k \in x_0 + \mathcal K_k(A, r_0)$ and $r_k \perp \mathcal K_k(A^T, \tilde r_0)$. When this has a solution it is unique, so BiCG is well defined exactly when the $k \times k$ matrix $\tilde W_k^T A W_k$ is nonsingular for bases $W_k$, $\tilde W_k$ of the two Krylov spaces.
3. **Finite termination.** The residuals $r_0, r_1, \dots$ that are nonzero are linearly independent (by 1), so some $r_k = 0$ with $k \le n$, or a breakdown occurs first.
4. **Termination of the code** after at most $\mathrm{kmax} + 1$ passes, by the loop bound.

There is no general convergence bound: BiCG is not optimal in any norm. Its residual is related to the QMR residual, which is quasi-minimal: $\|r_k^{\mathrm{QMR}}\|_2 \le \sqrt{k + 1} \, \kappa_2(\tilde V_{k+1}) \min \|r\|$ over $x_0 + \mathcal K_k$ (Freund and Nachtigal 1991), and BiCG residual norms are large exactly when QMR stagnates (Greenbaum, Section 2.5; a theorem about QMR, not a bound on BiCG itself).

**Floating point.** Biorthogonality is lost gradually, as orthogonality is in CG, which delays convergence but does not stop it. The attainable accuracy is limited by the gap between the updated residual $r_k$ and the true residual $b - A \hat x_k$, which is at most about $u \sum_j (\|A\| \|\hat x_j\| + \|r_j\|)$ (Greenbaum, Section 5.4; worst case, proved), so large intermediate residuals, typical of BiCG's erratic phases, lower the final accuracy. Breakdowns are rarely exact in floating point but near breakdowns ($|\rho|$ or $|\sigma|$ tiny relative to the norms) give huge $\alpha$ or $\beta$ and wreck the iteration.

## Complexity

Proof in [proofs/complexity.md](proofs/complexity.md). Each step does one product with $A$ and one with $A^T$ ($4 z$ flops), two inner products ($4 n$), one norm for the stopping test ($2 n$) and five vector updates ($10 n$): $4 z + 16 n + O(1)$ flops. Storage is seven vectors of length $n$ besides $A$, independent of $k$. So $k$ steps cost $O(k (z + n))$ time and $\Theta(n)$ extra space.

The product with $A^T$ costs the same flops as one with $A$, but for a matrix in CSR it is a scatter (column access) rather than a gather, which parallelizes poorly and reads memory less regularly; for a matrix available only as a function, $A^T$ may not be available at all. That is the practical reason for transpose-free variants such as CGS and BiCGSTAB.

## Properties

- **Short recurrences, constant memory**, like CG.
- **No minimization**: residual norms can increase; the test file observes this on a convection-diffusion matrix.
- **Two kinds of breakdown.** Lanczos (serious) breakdown $\rho = \tilde r_k^T r_k = 0$ with $r_k \ne 0$, and pivot breakdown $\sigma = \tilde p_k^T A p_k = 0$ when the tridiagonal Lanczos matrix has no LU factorization. Example: $A = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$, $b = e_1$ gives $\sigma = e_1^T A e_1 = 0$ at once.
- **Reduces to CG** for symmetric $A$ with $\tilde r_0 = r_0$ (the iterates coincide; the work doubles).
- **Dual solve for free**: the shadow recurrence solves $A^T \tilde x = \tilde b$ at the same time if $\tilde r_0 = \tilde b - A^T \tilde x_0$ and $\tilde x$ is updated with $\alpha \tilde p$; this is used for adjoint and error estimates.

## Variants and improvements

- **QMR** (Freund and Nachtigal 1991) uses the same Lanczos basis but chooses $x_k$ by minimizing a quasi-residual, which gives smooth convergence; with look-ahead it also avoids serious breakdowns.
- **CGS** (Sonneveld 1989) squares the BiCG polynomial, $r_k = \varphi_k(A)^2 r_0$, avoiding $A^T$; it converges about twice as fast when BiCG converges, and amplifies erratic behavior otherwise.
- **[BiCGSTAB](/bicgstab/)** (van der Vorst 1992) replaces one factor $\varphi_k$ by a product of local residual-minimizing steps; BiCGSTAB($\ell$) and IDR(s) improve it further.
- **Look-ahead Lanczos** (Parlett, Taylor and Liu 1985) skips over near breakdowns by building blocks of the tridiagonal matrix.
- **Preconditioning** with $M$: replace $A$ by $M^{-1} A$ and $A^T$ by $A^T M^{-T}$; [ILU](/incomplete-lu-factorization/) is the usual choice.

## When to use it

Use BiCG rarely on its own: when products with $A^T$ are cheap and an adjoint solution is wanted too, or as a building block. For a general nonsymmetric system, [GMRES](/gmres/) with a preconditioner is more robust when the number of steps is moderate; BiCGSTAB, QMR or IDR(s) are better short-recurrence choices when memory rules out GMRES.

## Pitfalls

- **Breakdown without warning.** Test $\rho$ and $\sigma$ against a tolerance relative to $\|\tilde r\| \|r\|$ and $\|\tilde p\| \|A p\|$, not only against zero; restart with a new shadow vector on near breakdown.
- **Erratic residuals** spoil the final accuracy through the residual gap; residual replacement (periodically setting $r \leftarrow b - A x$) helps.
- **Wrong transpose.** With a preconditioner or a complex matrix, the shadow recurrence needs $A^T M^{-T}$ (or $A^H$), not $M^{-1} A^T$.
- **Singular A.** With $A = \operatorname{diag}(1, 0)$ and $b = e_2$, $\sigma = 0$ at the first step: the code reports PIVOT-BREAKDOWN, not a solution.

## Implementations

## History

Lanczos (1950, 1952) introduced the two-sided recurrences for eigenvalues and for linear systems at the same time as Hestenes and Stiefel published CG. Fletcher (1976) wrote the biconjugate gradient algorithm in the CG-like form above while studying CG for indefinite systems. Interest grew in the 1980s with sparse nonsymmetric problems from fluid dynamics: Sonneveld's CGS (1989), Freund and Nachtigal's QMR (1991) and van der Vorst's BiCGSTAB (1992) are all built on BiCG, and look-ahead (Parlett, Taylor and Liu 1985; Freund, Gutknecht and Nachtigal 1993) addressed breakdowns.

## References
