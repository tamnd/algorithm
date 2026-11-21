---
tag: BNV7VJ
kind: algorithm
slug: lsqr
name: LSQR
aliases:
- Paige-Saunders LSQR
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: Paige and Saunders' Krylov method for least squares, built on Golub-Kahan bidiagonalization; equal to CGLS in exact arithmetic, more stable in floating point, and a standard iterative regularizer.
solves: [least-squares-problem, fredholm-integral-equation-first-kind]
model: floating-point-model
complexity:
  vars: {m: "the number of data values", n: "the number of unknowns", a: "the cost of one product with A plus one product with A*", k: "the number of iterations", r: "the rank of A"}
  time: {per_iteration: "O(a + m + n)", total: "O(k (a + m + n))", reorthogonalized: "O(k (a + k (m + n)))"}
  space: {extra: "O(m + n)", reorthogonalized: "O(k (m + n))"}
  iterations: {exact_termination: "r"}
properties: {deterministic: true, iterative: true, matrix_free: true, linear_in_data: false, residual_estimate: free, discrepancy_stop: "O(delta^(-1 / (2 nu + 1)))"}
history:
  year: 1982
  people: [Christopher C. Paige, Michael A. Saunders]
  note: Paige and Saunders built LSQR on the bidiagonalization of Golub and Kahan (1965) and showed that it is more reliable than CGLS on ill-conditioned problems in floating point.
prereqs: [cgls, golub-kahan-svd-algorithm, condition-number]
see_also: [hybrid-krylov-regularization, lanczos-algorithm, minres, gmres, morozov-discrepancy-principle, semi-convergence, least-squares-problem, truncated-svd]
sources:
  - paper: doi:10.1145/355984.355989
    title: Christopher C. Paige and Michael A. Saunders, LSQR, an algorithm for sparse linear equations and sparse least squares, ACM Transactions on Mathematical Software 8(1), 1982, 43 to 71
    locator: the bidiagonalization, the QR update by plane rotations, the residual estimates and the stopping rules
  - paper: doi:10.1137/0702016
    title: Gene Golub and William Kahan, Calculating the singular values and pseudo-inverse of a matrix, SIAM Journal on Numerical Analysis 2(2), 1965, 205 to 224
    locator: the bidiagonalization of a matrix by orthogonal transformations and by the Lanczos-type recurrence
  - book: isbn:9780898714036
    title: Per Christian Hansen, Rank-Deficient and Discrete Ill-Posed Problems, SIAM, 1998
    locator: Sections 6.3 to 6.5 (regularizing CG and LSQR iterations, and LSQR in finite precision)
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: Chapter 6 (iterative regularization with Krylov methods)
---

LSQR, by Paige and Saunders (1982), solves $\min_x \|y - A x\|$ with one product with $A$ and one with $A^*$ per step. It runs the Golub-Kahan bidiagonalization of $A$ started from $y$, which builds orthonormal bases of the Krylov spaces, and it solves the projected least squares problem with one plane rotation per step. In exact arithmetic its iterates are those of [CGLS](/cgls/): $x_k$ minimizes $\|y - A x\|$ over $\mathcal{K}_k(A^* A, A^* y)$. In floating point it is more reliable on ill-conditioned problems. On an ill-posed problem with noisy data $y^\delta$, $\|y^\delta - y\| \le \delta$, the iteration count is the regularization parameter, and the rotations give the residual norm for free, so the [discrepancy principle](/morozov-discrepancy-principle/) costs nothing extra. The bidiagonal matrix it builds is also the starting point of [hybrid Krylov methods](/hybrid-krylov-regularization/).

## In plain words

LSQR builds, one step at a time, a small set of directions that describe the answer and a matching set that describe the data. Both sets are made of perpendicular directions, so that no direction repeats what another already says. In these directions the large problem looks like a tiny one with a simple two-diagonal shape, and the tiny problem is easy to solve exactly. Each step adds one direction to each set and updates the answer. The method also knows, at every step and without extra work, how well the answer fits the data. On noisy, blurred data, it is stopped as soon as that misfit drops to the noise level, because later steps mostly add noise.

## The problem

Given $A: X \to Y$ (an $m \times n$ matrix, or the two functions $x \mapsto A x$ and $r \mapsto A^* r$) and data $y$, find the least squares solution of minimum norm, $x^\dagger = A^\dagger y$. For ill-posed problems the data are noisy, $\|y^\delta - A x^\dagger\| \le \delta$, and the goal is an approximation of $x^\dagger$ whose error goes to $0$ with $\delta$; then the iteration is stopped early.

## The algorithm

```pseudo id=main
LSQR(A, y, K, δ, τ)                        ▷ τ > 1; real data
L1  β u ← y;  α v ← A* u;  w ← v;  x ← 0;  φ̄ ← β;  ρ̄ ← α
L2  for k ← 1 to K do
L3      β u ← A v - α u                      ▷ β = norm, u a unit vector
L4      α v ← A* u - β v
L5      ρ ← √(ρ̄² + β²);  c ← ρ̄ / ρ;  s ← β / ρ
L6      θ ← s α;  ρ̄ ← -c α;  φ ← c φ̄;  φ̄ ← s φ̄
L7      x ← x + (φ / ρ) w;  w ← v - (θ / ρ) w
L8      if |φ̄| ≤ τ δ or α = 0 or β = 0 then return (x, k)
L9  return (x, K)
```

A line "$\beta u \leftarrow z$" means: $\beta \leftarrow \|z\|$ and $u \leftarrow z/\beta$. Lines L1, L3 and L4 are the Golub-Kahan bidiagonalization: after $k$ steps, $A V_k = U_{k+1} B_k$, where $U_{k+1}$ and $V_k$ have orthonormal columns and $B_k$ is lower bidiagonal of size $(k+1) \times k$, with $\alpha_1, \ldots, \alpha_k$ on the diagonal and $\beta_2, \ldots, \beta_{k+1}$ below it. LSQR looks for $x_k = V_k z_k$ with $z_k$ minimizing $\|\beta_1 e_1 - B_k z\|$. Lines L5 and L6 apply one plane rotation that removes the new subdiagonal entry $\beta_{k+1}$, which updates a QR factorization of $B_k$ and of the right side. Line L7 updates $x$ by a short recurrence, so no basis vectors are kept. After the rotations, $|\bar\phi|$ is exactly the residual norm $\|y - A x_k\|$, which line L8 compares with $\tau\delta$. Line L8 also returns when the bidiagonalization breaks down ($\alpha = 0$ or $\beta = 0$), which in exact arithmetic means that $x = A^\dagger y$. The code has an option that orthogonalizes each new $u$ and $v$ against all earlier ones, which costs $O(k(m + n))$ per step.

## Example

**A trace.** Take the example of the CGLS page: $A = \mathrm{diag}(1, \frac12, \frac14, \frac18, \frac1{16}, \frac1{32})$, $x^\dagger = (1, \ldots, 1)$, and $y^\delta = A x^\dagger + \frac1{20}(1, -1, 1, -1, 1, -1)$, so $\delta = 0.12247$ and, with $\tau = 1.5$, $\tau\delta = 0.18371$. Row $k$ shows the values after step $k$ (row $0$ after line L1).

| $k$ | $\alpha_{k+1}$ | $\beta_{k+1}$ | $\lvert\bar\phi_{k+1}\rvert$ | $\|y^\delta - A x_k\|$ | $\|x_k - x^\dagger\|$ |
|---|---|---|---|---|---|
| 0 | 0.90542 | 1.18896 | 1.18896 | 1.18896 | 2.4495 |
| 1 | 0.43930 | 0.37786 | 0.45791 | 0.45791 | 2.1007 |
| 2 | 0.27115 | 0.25614 | 0.24458 | 0.24458 | 1.7896 |
| 3 | 0.09064 | 0.12475 | 0.11691 | 0.11691 | 1.5720 |
| 4 | 0.09778 | 0.06136 | 0.07137 | 0.07137 | 1.1217 |
| 5 | 0.03193 | 0.01423 | 0.01289 | 0.01289 | 1.5109 |
| 6 | | 0 (rounding level) | 0 | 0 | 1.8473 |

The residual estimate $|\bar\phi|$ equals the true residual, and the residuals and errors agree with those of CGLS to all digits shown. Line L8 returns $k = 3$. At $k = 6$ the bidiagonalization has exhausted $\mathbb{R}^6$ and $\beta_7$ is zero up to rounding.

**Loss of orthogonality.** For the $60 \times 60$ rectangle-rule matrix of $(A x)(s) = \int_0^s x(t)\,dt$ and smooth data, the largest entry of $|V_k^T V_k - I|$ was $2.3 \cdot 10^{-5}$ after 5 steps and $0.76$ after 8 steps without reorthogonalization; with full reorthogonalization it stayed at $2.2 \cdot 10^{-16}$ (a measurement). After 20 steps the residual was $7.2 \cdot 10^{-5}$ without and $5.7 \cdot 10^{-6}$ with reorthogonalization: the loss of orthogonality delays convergence, but the computed residual estimate still matched the true residual of the computed $x$.

## Correctness

The proof is in proofs/correctness.md, in exact arithmetic.

- **Bidiagonalization (theorem).** By induction, the vectors $u_j$ are orthonormal, the vectors $v_j$ are orthonormal, $A V_k = U_{k+1} B_k$, and $V_k$ spans $\mathcal{K}_k(A^* A, A^* y)$.
- **Rotations (theorem).** After $k$ rotations, $Q_k [B_k \mid \beta_1 e_1] = \begin{bmatrix} R_k & f_k \\ 0 & \bar\phi_{k+1} \end{bmatrix}$ with $R_k$ upper bidiagonal and nonsingular.
- **Minimization (theorem).** For $x = V_k z$, $\|y - A x\|^2 = \|f_k - R_k z\|^2 + \bar\phi_{k+1}^2$. So $x_k = V_k R_k^{-1} f_k$ minimizes the residual over the Krylov space, which makes it the CGLS iterate, and its residual norm is $|\bar\phi_{k+1}|$. The recurrence of line L7 computes $V_k R_k^{-1} f_k$ without storing $V_k$.
- **Breakdown (theorem).** If $\alpha_{k+1} = 0$ or $\beta_{k+1} = 0$, then $x_k = A^\dagger y$, and this happens after at most $\operatorname{rank}(A)$ steps.
- **Discrepancy stop (theorem).** If $y^\delta - A x^\dagger$ has norm at most $\delta$ and $\tau > 1$, line L8 returns the first $k$ with $\|y^\delta - A x_k\| \le \tau\delta$.

The regularization properties are those of CGLS: with the discrepancy principle, LSQR is order optimal under the source condition for every $\nu > 0$ (Nemirovskii 1986; EHN Chapter 7), a theorem cited and not proved here.

## Complexity

- **Per iteration (floating-point model).** One product with $A$ (line L3), one with $A^*$ (line L4), two norms, and about $3m + 5n$ further operations for the vector updates. That is $O(a + m + n)$, or $O(m n)$ for a dense matrix.
- **Iterations.** In exact arithmetic, at most $\operatorname{rank}(A)$ steps. With the discrepancy principle under the source condition, the stopping index is $O(\delta^{-1/(2\nu+1)})$ (a theorem, as for CGLS). In floating point more steps can be needed, because the bases lose orthogonality.
- **Space.** $u, v, w, x$: $O(m + n)$. Full reorthogonalization stores $U_{k+1}$ and $V_k$, $O(k(m + n))$ space, and costs $O(k(m + n))$ more time in step $k$.

The [condition number](/condition-number/) matters for accuracy, not for the count above. CGLS forms the gradient $A^* r$ as LSQR does, but its recurrences for the scalars amplify rounding errors more when $A$ is ill-conditioned (Paige and Saunders 1982, an observed behavior with analysis in their paper).

## Properties

- **Same iterates as CGLS** in exact arithmetic, with the same residual and solution norm curves: $\|y - A x_k\|$ decreases and $\|x_k\|$ increases.
- **Free residual norm.** $\|y - A x_k\| = |\bar\phi_{k+1}|$, and $\|A^*(y - A x_k)\| = |\bar\phi_{k+1}|\,\alpha_{k+1}|c_k|$, also at no cost (Paige and Saunders).
- **Free projected problem.** The bidiagonal $B_k$ and the bases are available, so the small problem can be solved again with Tikhonov regularization (hybrid methods), and the singular values of $B_k$ approximate the largest singular values of $A$.
- **Nonlinear in the data**, as CGLS, so the stopping index must depend on the data.
- **Damped form.** LSQR also solves $\min \|A x - y\|^2 + \lambda^2\|x\|^2$ with one more rotation per step, which is Tikhonov regularization with a fixed parameter.

## Variants and improvements

- **Damped LSQR.** As in the paper, solve the Tikhonov problem by applying LSQR to the stacked matrix $\begin{bmatrix} A \\ \lambda I \end{bmatrix}$ without forming it.
- **Hybrid LSQR.** Choose a Tikhonov parameter for the projected problem at each step, by the discrepancy principle or by a cross-validation rule; see [hybrid Krylov regularization](/hybrid-krylov-regularization/).
- **Reorthogonalization.** Full, partial or selective reorthogonalization keeps the bases orthogonal and makes the computed iterates follow the exact ones, at extra cost in time and memory.
- **LSMR.** Fong and Saunders (2011) apply MINRES to the normal equations in the same bidiagonal framework, so that $\|A^*(y - A x_k)\|$ decreases monotonically. Compare [MINRES](/minres/).
- **Preconditioning.** As for CGLS, a right preconditioner changes the penalized norm, for example to a smoothness seminorm.

## When to use it

LSQR is the standard Krylov solver for large sparse or matrix-free least squares problems, well-posed or ill-posed. Use it instead of CGLS when the matrix is ill-conditioned and you care about the late iterates, when you want the residual norm without an extra product, or when you need the bidiagonal matrix for a hybrid method or for estimates of the singular values. CGLS is a little cheaper per step and simpler to write; for an early stop on a regularization problem the two usually give the same result (a heuristic). For small dense problems, [truncated SVD](/truncated-svd/) gives more insight at a cost of $O(m n^2)$.

## Pitfalls

- **Running without a stopping rule.** Line L2 run to the end converges to the least squares solution of the noisy data, which is dominated by noise. Keep the test $|\bar\phi| \le \tau\delta$ of line L8, with $\tau > 1$.
- **Testing a breakdown with $= 0$ in floating point.** In the example, $\beta_7$ is not exactly $0$ but at rounding level, and the normalization of line L3 then produces a vector of rounding noise. Line L8 should compare $\alpha$ and $\beta$ with a tolerance such as $10^{-14}$ times $\|A\|$ in production code.
- **Trusting orthogonality.** Without reorthogonalization, $V_k$ loses orthogonality after a few steps once a singular value has converged (in the example, from step 8). The iterates then lag behind the exact ones, and the singular values of $B_k$ contain spurious copies. Use reorthogonalization at lines L3 and L4 when you need the bases, as in hybrid methods.
- **Damped LSQR as a parameter search.** Running damped LSQR once per value of $\lambda$ repeats the whole bidiagonalization each time. The bidiagonalization does not depend on $\lambda$; a hybrid method reuses it.
- **A wrong adjoint at line L4.** The recurrences assume that the code for $A^*$ is the adjoint of the code for $A$. Check it by an adjoint test.

## Implementations

## History

Golub and Kahan described the bidiagonalization of a matrix in 1965, as the first step of a stable SVD algorithm, both by orthogonal transformations and by a Lanczos-type recurrence. Paige (1974) studied the recurrence for large sparse problems. Paige and Saunders published LSQR in 1982 in ACM Transactions on Mathematical Software, with the QR update by rotations, the residual estimates and a careful comparison with CGLS. Its use as an iterative regularization method, and as the core of hybrid methods, goes back to O'Leary and Simmons (1981) and Björck (1988), and is described in Hansen's books of 1998 and 2010.

## References
