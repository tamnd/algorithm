---
tag: ED04G2
kind: algorithm
slug: bicgstab
name: BiCGSTAB
aliases:
- stabilized biconjugate gradient method
- Bi-CGSTAB
area: numerical/linear-systems
level: advanced
summary: Smoothed BiCG variant with steadier convergence for nonsymmetric systems.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of A", z: "the number of nonzeros of A", k: "the number of iterations"}
  time: {worst: O(k z + k n)}
  space: {extra: Θ(n)}
  matvecs: {per_step: "2"}
  flops: {per_step: "4 z + 24 n + O(1)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true}
prereqs: [biconjugate-gradient, krylov-subspace]
see_also: [biconjugate-gradient, gmres, conjugate-gradient-method, minres, preconditioning, incomplete-lu-factorization, sparse-linear-systems, krylov-subspace]
sources:
  - paper: doi:10.1137/0913035
    title: Henk A. van der Vorst, Bi-CGSTAB, a fast and smoothly converging variant of Bi-CG for the solution of nonsymmetric linear systems, SIAM Journal on Scientific and Statistical Computing 13(2), 1992
    locator: pp. 631 to 644 (the algorithm, the product form r_k = psi_k(A) phi_k(A) r_0, and the local choice of omega)
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 7.4.1, Conjugate Gradient Squared; Section 7.4.2, BICGSTAB (Algorithm 7.7)
  - book: isbn:9780898713961
    title: Anne Greenbaum, Iterative Methods for Solving Linear Systems, SIAM, 1997
    locator: Section 5.5, transpose-free methods (CGS, BiCGSTAB, TFQMR)
  - paper: doi:10.1137/0910004
    title: Peter Sonneveld, CGS, a fast Lanczos-type solver for nonsymmetric linear systems, SIAM Journal on Scientific and Statistical Computing 10(1), 1989
    locator: pp. 36 to 52 (squaring the BiCG polynomial, the predecessor of BiCGSTAB)
  - paper: "Gerard L. G. Sleijpen and Diederik R. Fokkema, BiCGstab(l) for linear equations involving unsymmetric matrices with complex spectrum, Electronic Transactions on Numerical Analysis 1, 1993"
    title: G. L. G. Sleijpen and D. R. Fokkema, BiCGstab(l)
    locator: pp. 11 to 32 (the failure of omega for nearly imaginary eigenvalues and the degree l remedy)
  - book: "Henk A. van der Vorst, Iterative Krylov Methods for Large Linear Systems, Cambridge University Press, 2003"
    locator: Chapter 9, Bi-CGSTAB
---

BiCGSTAB solves a nonsymmetric system $A x = b$ with short recurrences, $O(n)$ memory and two products with $A$ per step, and needs no products with $A^T$. Van der Vorst (1992) derived it from the [biconjugate gradient method](/biconjugate-gradient/): where BiCG's residual is $r_k = \varphi_k(A) r_0$ for a Lanczos polynomial $\varphi_k$, BiCGSTAB produces $r_k = \psi_k(A) \varphi_k(A) r_0$, where $\psi_k(t) = (1 - \omega_1 t) \cdots (1 - \omega_k t)$ and each $\omega_j$ is chosen to minimize the residual locally, one step of the minimal residual method. The extra factor damps the erratic swings of BiCG and of CGS. BiCGSTAB is a standard default for nonsymmetric sparse systems when GMRES costs too much memory, but it can stagnate or break down, notably when $A$ has eigenvalues close to the imaginary axis.

## In plain words

BiCG makes fast but jumpy progress and needs the transposed matrix. BiCGSTAB keeps BiCG's direction-finding part but, instead of following the twin problem with the transpose, it adds a small correction step after each BiCG step: it moves along the latest residual times the matrix, by just the amount that makes the new error as small as possible.

That correction usually smooths the convergence a lot and costs one more multiplication by the matrix. But if multiplying by the matrix mostly rotates vectors, the correction step can do almost nothing and the method stalls.

## The problem

**Notation.** As in [solving linear systems](/linear-system-solving/): $A \in \mathbb{R}^{n \times n}$ nonsingular, $x_k$ the iterate, $r_k = b - A x_k$, $\mathcal K_k(A, r_0)$ the [Krylov subspace](/krylov-subspace/), $\kappa(A)$ the condition number, $u = 2^{-53}$. $\hat r_0$ is the shadow vector with $\hat r_0^T r_0 \ne 0$, usually $\hat r_0 = r_0$. $\varphi_k$ is the BiCG residual polynomial of degree $k$ with $\varphi_k(0) = 1$; $z$ is the number of nonzeros of $A$.

Given $A$ (through products $v \mapsto A v$ only), $b$, $x_0$ and a tolerance, return $x_k$ with $\|r_k\|_2 \le \mathrm{tol} \cdot \|b\|_2$, or NOT-CONVERGED, or one of three breakdowns.

## The algorithm

```pseudo id=main
BiCGSTAB(A, b, x, r̂, tol, kmax)              ▷ x is x₀;  r̂ is the shadow r̂₀ (default r₀)
L1  r ← b − A x
L2  p ← r;  ρ ← r̂ᵀ r
L3  for k ← 0 to kmax do                       ▷ return CONVERGED if ‖r‖₂ ≤ tol‖b‖₂;  RHO-BREAKDOWN if ρ = 0
L4      v ← A p;  σ ← r̂ᵀ v;  if σ = 0 then return PIVOT-BREAKDOWN;  α ← ρ / σ
L5      s ← r − α v                            ▷ the BiCG half step
L6      if ‖s‖₂ ≤ tol · ‖b‖₂ then x ← x + α p;  return (x, CONVERGED)
L7      t ← A s
L8      ω ← tᵀ s / tᵀ t;  if ω = 0 then return OMEGA-BREAKDOWN
L9      x ← x + α p + ω s;  r ← s − ω t        ▷ minimizes ‖s − ω A s‖₂ over ω
L10     ρ_new ← r̂ᵀ r;  β ← (ρ_new / ρ)(α / ω);  ρ ← ρ_new
L11     p ← r + β (p − ω v)
```

L8 is one step of the minimal residual method along $t = A s$. The scalars $\alpha$ and $\beta$ are BiCG's, recovered from the shadow vector without $A^T$ by the identity $\hat r_0^T \psi_k(A) \varphi_k(A) r_0 = \hat r_0^T \varphi_k(A) \psi_k(A) r_0$ and the leading coefficient of $\psi_k$.

## Example

The same system as on the [BiCG](/biconjugate-gradient/) page:
$$A = \begin{pmatrix} 2 & 1 & 0 \\ -1 & 2 & 1 \\ 0 & -1 & 2 \end{pmatrix}, \quad b = (1, 1, 1), \quad x_0 = 0, \quad \hat r_0 = r_0,$$
with solution $x = (1/3, 1/3, 2/3)$. In rational arithmetic:

- **Step 0.** $\rho = 3$, $v = A p = (3, 2, 1)$, $\sigma = 6$, $\alpha = 1/2$, $s = (-1/2, 0, 1/2)$, which is the BiCG residual $r_1$. Then $t = A s = (-1, 1, 1)$, $t^T s = 1$, $t^T t = 3$, so $\omega_1 = 1/3$, and $r_1 = s - t/3 = (-1/6, -1/3, 1/6)$ with $\|r_1\|_2^2 = 1/6$.
- **Step 1.** gives $\omega_2 = 7/20$ and $\|r_2\|_2^2 = 1/105$.
- **Step 2.** gives $r_3 = 0$ and $x_3 = x$.

Compare BiCG on the same data: $\|r_1\|_2^2 = 1/2$ and $\|r_2\|_2^2 = 6/49 \approx 0.122$, against $1/6$ and $1/105 \approx 0.0095$ here. The test file checks, on 500 random rational systems, that every BiCGSTAB residual equals $\psi_k(A)$ applied to the BiCG residual $r_k$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). In exact arithmetic, as long as no breakdown occurs:

1. **Invariant.** $r = b - A x$ after every line.
2. **Product form.** After step $k$, $r_k = \psi_k(A) \varphi_k(A) r_0$ and $p_k = \psi_k(A) \pi_k(A) r_0$, where $\varphi_k$ and $\pi_k$ are the BiCG residual and direction polynomials and $\psi_k(t) = \prod_{j=1}^{k} (1 - \omega_j t)$ (van der Vorst 1992). The scalars $\alpha_k$ and $\beta_k$ equal those of BiCG with shadow $\hat r_0$.
3. **Local optimality.** $\omega_{k+1}$ minimizes $\|s - \omega A s\|_2$ over $\omega \in \mathbb{R}$, so $\|r_{k+1}\|_2 \le \|s\|_2$, where $s = \psi_k(A) \varphi_{k+1}(A) r_0$.
4. **Finite termination.** BiCG terminates with $\varphi_d(A) r_0 = 0$ for some $d \le n$; then $s = 0$ at step $d$, so BiCGSTAB terminates in at most $n$ steps ($2n$ matvecs). The loop bound ensures termination of the code in every case.

There is no global convergence bound in general; the local minimization gives $\|r_{k+1}\|_2 \le \|s\|_2$ only, and $\|s\|_2$ can exceed $\|r_k\|_2$.

**Floating point.** As for BiCG, the attainable accuracy is limited by the gap between updated and true residuals, which grows with the largest intermediate $\|r_j\|$ and $\|\hat x_j\|$ (Greenbaum, Section 5.5; worst-case bounds of order $u \sum_j (\|A\| \|\hat x_j\| + \|r_j\|)$); BiCGSTAB's smoother residuals usually make this gap smaller than for CGS. If $A$ has eigenvalues $\lambda$ with $|\operatorname{Re} \lambda| \ll |\operatorname{Im} \lambda|$, then $t^T s$ is small relative to $\|t\| \|s\|$, so $\omega$ is tiny, $\psi_k$ barely reduces anything, and $\beta = (\rho_{k+1}/\rho_k)(\alpha / \omega)$ is inaccurate (Sleijpen and Fokkema 1993). The test file shows this: for 20 blocks with eigenvalues $0.01 \pm i c_k$, every $|\omega| < 0.05$ and BiCGSTAB has not reached $10^{-8}$ after 400 matvecs, while full [GMRES](/gmres/) converges in 30 (observed).

## Complexity

Proof in [proofs/complexity.md](proofs/complexity.md). Each step does two products with $A$ ($4 z$ flops), six inner products or squared norms ($\hat r^T v$, $s^T s$, $t^T s$, $t^T t$, $\hat r^T r$, $r^T r$; $12 n$) and vector updates for $s$, $x$, $r$ and $p$ ($12 n$): $4 z + 24 n + O(1)$ flops, with seven vectors of storage. A step costs as much as two CG steps and, roughly, one BiCGSTAB step reduces the residual about as much as one BiCG step squared, when convergence is regular.

On parallel machines the six inner products are global reductions; they, not the flops, dominate the time for sparse $A$ with few nonzeros per row. Pipelined variants (Cools and Vanroose 2017) merge the reductions at the cost of extra recurrences and a larger residual gap.

## Properties

- **Transpose-free**, short recurrences, $\Theta(n)$ memory.
- **Two matvecs per step**, both with $A$; a preconditioner is applied twice per step.
- **Not monotone**, but usually much smoother than BiCG and CGS (observed, not proved).
- **Three breakdowns**: $\rho = 0$ and $\sigma = 0$ inherited from BiCG, and $\omega = 0$ when $t \perp s$. Example: $A = \begin{pmatrix} 0 & 2 \\ 2 & 1 \end{pmatrix}$, $b = (0, -2)$: $s = (4, 0)$ and $t = A s = (0, 8)$ are orthogonal, so $\omega = 0$ at the first step.
- **Same Krylov space** as BiCG of twice the degree: $x_k \in x_0 + \mathcal K_{2k}(A, r_0)$.

## Variants and improvements

- **BiCGSTAB($\ell$)** (Sleijpen and Fokkema 1993) replaces the degree-one factors by degree-$\ell$ minimal residual polynomials, curing the imaginary-spectrum stagnation; $\ell = 2$ (BiCGSTAB2, Gutknecht 1993) is common.
- **IDR(s)** (Sonneveld and van Gijzen 2008) generalizes the induced dimension reduction idea behind CGS and BiCGSTAB with $s$ shadow vectors, and is equivalent to BiCGSTAB for $s = 1$.
- **TFQMR** (Freund 1993) smooths CGS with a quasi-minimization.
- **Residual replacement** (van der Vorst and Ye 2000) sets $r \leftarrow b - A x$ at selected steps to keep the residual gap near $u \|A\| \|x\|$.
- **Preconditioning.** Right preconditioning ($A M^{-1} y = b$) keeps the true residual in the recurrences; [ILU](/incomplete-lu-factorization/) is the usual $M$.

## When to use it

Use BiCGSTAB for nonsymmetric sparse systems with a good preconditioner when GMRES would need a restart length too large for memory, or when $A^T$ is not available. If it stagnates or breaks down, try BiCGSTAB(2) or IDR(s), or GMRES. For symmetric positive definite systems use [CG](/conjugate-gradient-method/), which costs half as much per step.

## Pitfalls

- **Stopping on $\|s\|$.** The half-step test in L6 must update $x$ before returning, or the returned $x$ does not match the residual that passed the test.
- **Tiny $\omega$.** A near-zero $\omega$ makes $\beta$ huge and the next steps garbage; monitor $|t^T s| / (\|t\| \|s\|)$ and switch to BiCGSTAB($\ell$) or restart.
- **Shadow choice.** $\hat r_0 = r_0$ can be poor when $r_0$ is nearly an eigenvector; a random $\hat r_0$ is a common fix.
- **Singular A.** For $A = \operatorname{diag}(1, 0)$ and $b = e_2$, $v = A p = 0$ so $\sigma = 0$: the code reports PIVOT-BREAKDOWN; for an inconsistent $b = (1, 1)$ it never converges and returns NOT-CONVERGED.
- **Updated versus true residual.** Always check $\|b - A \hat x\|_2$ at the end.

## Implementations

## History

Sonneveld's CGS (1989) showed that BiCG's polynomial can be applied twice without $A^T$, but squaring also squared its erratic behavior. Van der Vorst (1992) replaced one copy by a product of local minimal residual steps and called the result Bi-CGSTAB; it became one of the most cited papers in numerical analysis. Gutknecht (1993) and Sleijpen and Fokkema (1993) extended the stabilizing polynomial to degree two and $\ell$, and Sonneveld and van Gijzen (2008) recast the family as IDR(s).

## References
