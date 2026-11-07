---
tag: NAYDFS
kind: algorithm
slug: minres
name: MINRES
aliases:
- minimal residual method
- MINRES method
area: numerical/linear-systems
level: advanced
summary: Krylov method for symmetric indefinite systems that minimizes the residual norm.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of A", m: "the number of nonzeros of A", k: "the number of iterations"}
  time: {worst: "Θ(k (n + m))", best: "Θ(n + m)"}
  space: {extra: Θ(n)}
  flops: {worst: "k (2m + 16n)"}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [lanczos-algorithm, krylov-subspace, givens-rotations]
see_also: [conjugate-gradient-method, gmres, preconditioning, residual, sparse-linear-systems, bicgstab, chebyshev-iteration, condition-number]
sources:
  - paper: doi:10.1137/0712047
    title: C. C. Paige and M. A. Saunders, Solution of sparse indefinite systems of linear equations, SIAM Journal on Numerical Analysis 12(4), 1975
    locator: the MINRES and SYMMLQ algorithms, derived from the Lanczos process with an LQ or QR factorization of the tridiagonal matrix
  - book: isbn:9780898713961
    title: Anne Greenbaum, Iterative Methods for Solving Linear Systems, SIAM, 1997
    locator: Chapter 2, Some Iteration Methods (MINRES and its derivation from the Lanczos algorithm); Chapter 3, Error Bounds for CG, MINRES, and GMRES; Chapter 4, Effects of Finite Precision Arithmetic
  - paper: doi:10.1137/100787921
    title: Sou-Cheng T. Choi, Christopher C. Paige and Michael A. Saunders, MINRES-QLP, a Krylov subspace method for indefinite or singular symmetric systems, SIAM Journal on Scientific Computing 33(4), 2011
    locator: the behaviour of MINRES on singular and ill-conditioned systems and the minimum-length solution
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 6.6, The Symmetric Lanczos Algorithm; Section 6.8, The Conjugate Residual Method
---

MINRES solves $A x = b$ for a symmetric matrix $A$ that may be indefinite. At step $k$ it returns the vector of least residual norm $\|b - A x_k\|_2$ in the affine [Krylov space](/krylov-subspace/) $x_0 + \mathcal{K}_k(A, r_0)$, which makes it [GMRES](/gmres/) for symmetric matrices; symmetry lets the [Lanczos process](/lanczos-algorithm/) build the basis with a three-term recurrence, so each step costs one product with $A$ and about $16 n$ further flops and the storage stays at seven vectors. [Conjugate gradients](/conjugate-gradient-method/) need $A$ positive definite; MINRES does not.

## In plain words

To solve a large system, start from a guess and look for the best correction among the vectors you can make by applying the matrix again and again to the current error signal. MINRES picks, at each step, the correction that makes the leftover error in the equations as small as possible. For a symmetric matrix this best choice can be updated with a few vectors from the previous two steps only, so the work and memory per step stay fixed. It works whether the matrix has only positive, or mixed positive and negative, eigenvalues, though the mixed case needs more steps.

## The problem

**Notation.** $A \in \mathbb{R}^{n \times n}$ symmetric and nonsingular (singular $A$ is discussed below), $b \in \mathbb{R}^n$, $x = A^{-1} b$. The iterate is $x_k$, its [residual](/residual/) $r_k = b - A x_k$ and $\mathcal{K}_k = \mathrm{span}\{r_0, A r_0, \ldots, A^{k-1} r_0\}$. The Lanczos vectors $v_1, \ldots, v_{k+1}$ are orthonormal, $T_k$ is the $k \times k$ symmetric tridiagonal Lanczos matrix with diagonal $\delta_j$ and off-diagonal $\gamma_j$, and $\bar T_k$ adds the row $\gamma_{k+1} e_k^T$. $\kappa = \kappa_2(A) = \max|\lambda_i|/\min|\lambda_i|$, $u = 2^{-53}$. In floating point, a hat marks computed quantities.

**Input.** $A$, or just a routine for $v \mapsto A v$; $b$; $x_0$; a tolerance and a step limit.

**Output.** $x_k$ with $\|r_k\|_2 \le \mathrm{tol}\,\|b\|_2$ measured by the recurrence, or the last iterate and a flag. In exact arithmetic
$$x_k = \arg\min_{x \in x_0 + \mathcal{K}_k} \|b - A x\|_2 .$$
There is no iteration matrix: unlike the [stationary methods](/matrix-splitting/), MINRES is a nonlinear function of $b$, and $r_k = p_k(A) r_0$ for the polynomial $p_k$ of degree $k$ with $p_k(0) = 1$ that minimizes $\|p_k(A) r_0\|_2$.

## The algorithm

```pseudo id=main
MINRES(A, b, x_0, tol, maxiter)
L1  r ← b − A x_0;  γ ← ‖r‖_2;  η ← γ
L2  v_old ← 0;  v ← r;  w_old ← 0;  w ← 0;  c_old ← c ← 1;  s_old ← s ← 0
L3  for k ← 1 to maxiter do
L4      v ← v / γ;  p ← A v;  δ ← vᵀ p                      ▷ Lanczos: δ = (T_k)_kk
L5      v_new ← p − δ v − γ v_old;  γ_new ← ‖v_new‖_2         ▷ γ_new = (T̄_k)_{k+1,k}
L6      α_3 ← s_old γ;  α_2 ← s δ + c_old c γ;  α_0 ← c δ − c_old s γ;  α_1 ← (α_0² + γ_new²)^{1/2}
L7      c_new ← α_0 / α_1;  s_new ← γ_new / α_1                ▷ new Givens rotation zeroes γ_new
L8      w_new ← (v − α_3 w_old − α_2 w) / α_1                  ▷ columns of V_k R_k^{-1}
L9      x ← x + c_new η w_new;  η ← −s_new η                  ▷ |η| = ‖r_k‖_2 in exact arithmetic
L10     if |η| ≤ tol · ‖b‖_2 then return (x, k, converged)
L11     (v_old, v, γ) ← (v, v_new, γ_new);  (w_old, w) ← (w, w_new);  (c_old, c, s_old, s) ← (c, c_new, s, s_new)
L12 return (x, maxiter, not converged)
```

Lines L4 and L5 are one Lanczos step. Line L6 applies the two previous Givens rotations to the new column of $\bar T_k$, which has only three nonzeros, and L7 builds the rotation that annihilates its subdiagonal. Lines L8 and L9 update $x$ without storing the Lanczos basis. The implementation also stops when $\alpha_1$ or $\gamma_{\text{new}}$ is below $10 n u$ times a running estimate of $\|A\|_2$: the first means $b \notin \mathrm{range}(A)$, the second that an invariant subspace was found.

## Example

**By hand.** $A = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ (eigenvalues $\pm 1$), $b = e_1$, $x_0 = 0$. Step 1: $v = e_1$, $A v = e_2$, $\delta = 0$, $v_{\text{new}} = e_2$, $\gamma_{\text{new}} = 1$; then $\alpha_0 = 0$, $\alpha_1 = 1$, $c_{\text{new}} = 0$, $s_{\text{new}} = 1$, $w_{\text{new}} = e_1$, and $x$ stays $0$ with $|\eta| = 1$. The method has *stagnated*: no multiple of $b$ reduces $\|e_1 - t\,e_2\|_2 \ge 1$. Step 2: $v = e_2$, $A v = e_1$, $\delta = 0$, $v_{\text{new}} = e_1 - e_1 = 0$, so $\gamma_{\text{new}} = 0$; $\alpha_3 = 0$, $\alpha_2 = 0$, $\alpha_0 = 0 - 1 \cdot 1 \cdot 1 = -1$, $\alpha_1 = 1$, $c_{\text{new}} = -1$, $s_{\text{new}} = 0$, $w_{\text{new}} = e_2$, and $x = 0 + (-1)(-1)e_2 = e_2$ with $\eta = 0$. The exact solution in $2 = n$ steps.

**Definite against indefinite.** For diagonal $A$ with eigenvalues spread evenly over $[1, \kappa]$ (1000 of them) or over $[-\kappa, -1] \cup [1, \kappa]$ (2000), $b = (1, \ldots, 1)^T$, $x_0 = 0$ and a relative residual of $10^{-8}$, the implementation needs:

| $\kappa$ | definite: steps | bound $2 q^k$, $q = \frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}$ | indefinite: steps | bound $2 \big(\frac{\kappa - 1}{\kappa + 1}\big)^{\lfloor k/2 \rfloor}$ |
|---|---|---|---|---|
| 10 | 29 | 30 | 182 | 192 |
| 100 | 88 | 96 | 1580 | 1912 |
| 1000 | 172 | 303 | 3008 | 19114 |

The bounds give the step count at which they reach $10^{-8}$. On the definite spectrum MINRES behaves like conjugate gradients, about $\sqrt\kappa$ steps per digit; on the indefinite one it needs about $\kappa$ steps per digit, as conjugate gradients would on $A^2$. At $\kappa = 1000$ the indefinite run takes 3008 steps although $A$ has only 2000 distinct eigenvalues, so in exact arithmetic 2000 steps would end it: this is the delay caused by the loss of orthogonality of the Lanczos vectors. On this spectrum, symmetric about $0$ with equal weights, the residual stagnates at every odd step: $\|r_1\| = \|r_0\|$, $\|r_3\| = \|r_2\|$, and so on.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). By the Lanczos relation $A V_k = V_{k+1} \bar T_k$, every $x \in x_0 + \mathcal{K}_k$ has the form $x_0 + V_k y$ and $\|b - A x\|_2 = \|\beta e_1 - \bar T_k y\|_2$ with $\beta = \|r_0\|_2$. MINRES solves this small least squares problem by updating a QR factorization of $\bar T_k$ with one Givens rotation per step; the residual norm is the last entry $|\eta|$ of the rotated right side, and $x_k = x_0 + V_k R_k^{-1} t_k$ is updated through the direction vectors $W_k = V_k R_k^{-1}$, which satisfy a three-term recurrence because $R_k$ has bandwidth three.

**Convergence (proved, exact arithmetic).** $\|r_k\|_2 = \min_{p_k(0) = 1}\|p_k(A) r_0\|_2 \le \min_{p_k(0) = 1} \max_i |p_k(\lambda_i)|\,\|r_0\|_2$, because $A$ is orthogonally diagonalizable. Chebyshev polynomials give (Greenbaum, Chapter 3):
- spectrum in $[c, d]$ with $0 < c$: $\|r_k\|_2/\|r_0\|_2 \le 2\big((\sqrt\kappa - 1)/(\sqrt\kappa + 1)\big)^k$, $\kappa = d/c$;
- spectrum in $[-d, -c] \cup [c, d]$: $\|r_k\|_2/\|r_0\|_2 \le 2\big((\kappa - 1)/(\kappa + 1)\big)^{\lfloor k/2 \rfloor}$, from a polynomial in $\lambda^2$;
- finite termination: if $A$ has $d$ distinct eigenvalues, $r_d = 0$.

These are worst-case bounds over $r_0$; the table shows how close they can be. The residual norms never increase.

**In floating point.** The Lanczos vectors lose orthogonality once a Ritz value converges, which delays convergence but does not stop it; Greenbaum (Chapter 4) shows that finite precision Lanczos behaves like exact Lanczos on a larger matrix with eigenvalues clustered near those of $A$. The computed $|\hat\eta|$ is not the true residual: it keeps decreasing geometrically below the level the true residual can reach. In the tests, for a random symmetric indefinite matrix of order 30 with $\kappa \le 10$, $|\hat\eta|/\|b\|$ falls below $10^{-18}$ while $\|b - A \hat x\|_2/\|b\|_2$ stays near $10^{-15}$. The attainable accuracy is of order $u\,\|A\|\,\|x\|$ times a factor that can grow with $\kappa$; Sleijpen, van der Vorst and Modersitzki (2000) showed that the way MINRES updates $x$ can lose more accuracy than GMRES on ill-conditioned problems. A final check of the true residual is cheap and worth doing. The forward error then satisfies $\|\hat x - x\|_2/\|x\|_2 \le \kappa\,\|b - A\hat x\|_2/\|b\|_2$, a worst-case bound that holds with the residual actually computed.

## Complexity

Per step: one product with $A$ ($2m$ flops for $m$ nonzeros), two inner products and one norm ($4n$, line L4 and L5), the vector updates of L4, L5, L8 and L9 (about $12 n$), and $O(1)$ scalar work: about $2m + 16n$ flops. Storage: $x$, $v_{\text{old}}$, $v$, $v_{\text{new}}$ (or $p$), $w_{\text{old}}$, $w$, $w_{\text{new}}$, that is seven vectors of length $n$, independent of $k$. For sparse $A$ the product and the vector updates are all memory bound, each reading or writing a few words per flop. The number of steps $k$ follows the bounds above: $O(\sqrt\kappa \log(1/\varepsilon))$ for definite and $O(\kappa \log(1/\varepsilon))$ for indefinite spectra symmetric about zero, at most $n$ in exact arithmetic.

## Properties

- **Optimal.** Least residual norm over $x_0 + \mathcal{K}_k$ (exact arithmetic), so the same iterates as GMRES on symmetric $A$ and never a residual larger than that of conjugate gradients, which on SPD $A$ minimizes the $A$-norm of the error instead.
- **Short recurrences, constant memory.** Unlike GMRES, the cost per step does not grow with $k$, and no restarts are needed.
- **Monotone residuals,** with stagnation possible: $\|r_k\| = \|r_{k-1}\|$ exactly when $T_k$ is singular.
- **Needs symmetry.** With a nonsymmetric $A$ the recurrences are wrong and the iterates are not optimal; the tests show a $2 \times 2$ upper triangular matrix that GMRES solves in 2 steps and MINRES does not solve in 10.
- **Preconditioning needs an SPD preconditioner.** With $M = L L^T$ SPD, MINRES runs on $L^{-1} A L^{-T}$ and minimizes the residual in the $M^{-1}$-norm; an indefinite preconditioner destroys the symmetry it needs.

## Variants and improvements

- **Preconditioned MINRES.** One solve with $M$ per step; block diagonal SPD preconditioners for saddle point systems are the main application (Elman, Silvester and Wathen).
- **SYMMLQ** (same paper) minimizes the error in a different space and is better for computing $x$ when $A$ is singular and consistent; its iterates may not reduce the residual monotonically.
- **MINRES-QLP** (Choi, Paige and Saunders, 2011) adds a QLP factorization so that for singular or nearly singular $A$ it returns the minimum-length least squares solution; plain MINRES returns a least squares solution with a possibly large component in the null space (in the tests, $x = (1, 0.5, 1.5)$ for $\mathrm{diag}(1, 2, 0)$ and $b = (1, 1, 1)$, where the minimum-length solution has last entry $0$).
- **GMRES** for nonsymmetric $A$, with growing cost per step; **CR** (conjugate residual) gives the same iterates as MINRES for symmetric $A$ with a different recurrence.
- **Shifted systems.** $(A - \sigma I)x = b$ for many $\sigma$ share one Krylov space, so one Lanczos run serves all shifts.

## When to use it

Use MINRES for large sparse symmetric indefinite systems: saddle point systems from mixed finite elements, Stokes flow and optimization; shifted systems $A - \sigma I$ in eigenvalue solvers; and least squares problems written as augmented systems. For symmetric positive definite $A$, conjugate gradients are usually preferred because they minimize the error in the energy norm, but MINRES is a sound choice when a small residual is the goal or when the matrix may be slightly indefinite. For nonsymmetric $A$, use GMRES or BiCGSTAB.

## Pitfalls

- **Nonsymmetric input.** Nothing in the algorithm checks symmetry; a slightly nonsymmetric $A$ (from rounding in assembly) usually only slows convergence, a strongly nonsymmetric one breaks it.
- **Indefinite preconditioner.** Using an incomplete LU or an indefinite $M$ voids the theory; $M$ must be SPD.
- **Trusting the recurrence residual.** $|\hat\eta|$ can be many orders of magnitude below the true residual; a tolerance below about $u\,\kappa$ is met by $|\hat\eta|$ but not by $b - A\hat x$.
- **Odd-step stagnation.** On spectra symmetric about zero, every second step makes no progress, which doubles the count.
- **Singular inconsistent systems.** Without the breakdown test, the near-zero pivot $\alpha_1$ makes $x$ explode while $|\hat\eta|$ falls below the least possible residual; with the test, the iterate is a least squares solution, but not the minimum-length one.

## Implementations

## History

Lanczos (1950, 1952) introduced the tridiagonalization and its use for linear systems, and Hestenes and Stiefel (1952) conjugate gradients, which can fail on indefinite matrices because $T_k$ may be singular. Paige and Saunders (1975) solved the indefinite case with two algorithms built on stable factorizations of $T_k$: SYMMLQ, using an LQ factorization, and MINRES, using a QR factorization and minimizing the residual. Saad and Schultz's GMRES (1986) later generalized MINRES to nonsymmetric matrices. Paige's analysis of the Lanczos process in finite precision (1971, 1976) and Greenbaum's (1989) explain the delays seen in practice, and Choi, Paige and Saunders (2011) extended MINRES to singular systems with MINRES-QLP.

## References
