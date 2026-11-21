---
tag: 83ANX4
kind: algorithm
slug: cgls
name: CGLS
aliases:
- conjugate gradient least squares
- CGNR
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: The conjugate gradient method applied to the normal equations A* A x = A* y without forming A* A; stopped early, its iteration count regularizes an ill-posed problem.
solves: [fredholm-integral-equation-first-kind, least-squares-problem]
model: real-ram
complexity:
  vars: {m: "the number of data values", n: "the number of unknowns", a: "the cost of one product with A plus one product with A*", k: "the number of iterations", r: "the rank of A"}
  time: {per_iteration: "O(a + m + n)", total: "O(k (a + m + n))", dense: "O(k m n)"}
  space: {extra: "O(m + n)"}
  iterations: {exact_termination: "r"}
properties: {deterministic: true, iterative: true, matrix_free: true, linear_in_data: false, finite_termination: true, discrepancy_stop: "O(delta^(-1 / (2 nu + 1)))"}
history:
  year: 1952
  people: [Magnus R. Hestenes, Eduard Stiefel]
  note: Hestenes and Stiefel introduced the conjugate gradient method and its form for least squares problems; Nemirovskii (1986) proved that it is an order optimal regularization method when stopped by the discrepancy principle.
prereqs: [conjugate-gradient-method, normal-equations, krylov-subspace, semi-convergence]
see_also: [landweber-iteration, lsqr, hybrid-krylov-regularization, morozov-discrepancy-principle, truncated-svd, tikhonov-regularization, spectral-filter-factors, lanczos-algorithm]
sources:
  - paper: "Magnus R. Hestenes and Eduard Stiefel, Methods of conjugate gradients for solving linear systems, Journal of Research of the National Bureau of Standards 49(6), 1952, 409 to 436"
    locator: the conjugate gradient method and its variant for least squares problems
  - paper: doi:10.1016/0041-5553(86)90002-9
    title: A. S. Nemirovskii, The regularizing properties of the adjoint gradient method in ill-posed problems, USSR Computational Mathematics and Mathematical Physics 26(2), 1986, 7 to 16
    locator: order optimality of the conjugate gradient method with the discrepancy principle
  - paper: doi:10.1007/BF01385614
    title: B. Eicke, A. K. Louis and R. Plato, The instability of some gradient methods for ill-posed problems, Numerische Mathematik 58(1), 1990, 129 to 134
    locator: the conjugate gradient iterates do not depend continuously on the data, so an a priori stopping index does not give a regularization method
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 7 (the conjugate gradient method as a regularization method)
  - book: isbn:9780898714036
    title: Per Christian Hansen, Rank-Deficient and Discrete Ill-Posed Problems, SIAM, 1998
    locator: Sections 6.3 and 6.4 (regularizing CG iterations and their convergence properties)
---

CGLS is the [conjugate gradient method](/conjugate-gradient-method/) applied to the [normal equations](/normal-equations/) $A^* A x = A^* y$, written so that it never forms $A^* A$. Each step costs one product with $A$ and one with the adjoint $A^*$, the same as one [Landweber](/landweber-iteration/) step. The iterate $x_k$ minimizes the residual $\|y - A x\|$ over the [Krylov subspace](/krylov-subspace/) $\mathcal{K}_k(A^* A, A^* y)$. For a well-posed least squares problem this is a fast solver. For an ill-posed problem with noisy data $y^\delta$, $\|y^\delta - y\| \le \delta$, the first iterates capture the dominant singular components and later ones fit the noise, so the iteration count $k$ is a regularization parameter. Stopped by the [discrepancy principle](/morozov-discrepancy-principle/), CGLS reaches the optimal rate in about the square root of the number of Landweber steps.

## In plain words

The method improves a guess step by step, like the plain gradient method, but it remembers its earlier search directions. Each new direction is chosen so that it does not undo the progress of the earlier ones. So each step fits as much of the data as is possible with the directions found so far. On a blurred or smoothed measurement, the first directions describe the coarse, reliable shape of the answer, and later directions add fine details that are mostly noise. Stop at the right moment and the answer is sharp but not noisy. Run too long and it fills with noise. The stopping point comes from the noise level: stop as soon as the misfit is as small as the noise.

## The problem

Given $A: X \to Y$ (an $m \times n$ matrix, or an operator given by the functions $x \mapsto A x$ and $r \mapsto A^* r$), data $y^\delta$ with $\|y^\delta - A x^\dagger\| \le \delta$, and $\delta$, find an approximation of the minimum norm solution $x^\dagger = A^\dagger y$ whose error goes to $0$ with $\delta$. Without noise and with $k$ large enough, CGLS solves the [least squares problem](/least-squares-problem/) $\min_x \|y - A x\|$.

## The algorithm

```pseudo id=main
CGLS(A, y, K, δ, τ)                       ▷ τ > 1
L1  x ← 0;  r ← y;  s ← A* r;  p ← s;  γ ← ‖s‖²
L2  for k ← 0 to K - 1 do
L3      if ‖r‖ ≤ τ δ then return (x, k)
L4      if γ = 0 then return (x, k)          ▷ A* r = 0: least squares solution
L5      q ← A p
L6      α ← γ / ‖q‖²
L7      x ← x + α p
L8      r ← r - α q
L9      s ← A* r
L10     β ← ‖s‖² / γ;  γ ← ‖s‖²
L11     p ← s + β p
L12 return (x, K)
```

The vector $r$ is the residual $y - A x$, and $s = A^* r$ is the residual of the normal equations, that is, minus the gradient of $\frac12\|y - A x\|^2$. Line L1 starts at $x = 0$. Line L3 is the discrepancy principle, which returns the first iterate whose residual is at the noise level. The code compares $\|r\|^2$ with $(\tau\delta)^2$, so the loop takes no square roots and runs in exact rational arithmetic on rational data. Line L4 returns when the gradient is zero, which in exact arithmetic happens after at most $\operatorname{rank}(A)$ steps. Lines L5 to L8 take the exact line search step along $p$, and lines L9 to L11 build the next direction from the new gradient, with the factor $\beta$ that makes the directions $A^* A$-conjugate.

Compared with the textbook CG on $A^* A x = A^* y$, CGLS keeps $r$ and computes $s = A^* r$ in line L9, instead of updating $s$ by $s - \alpha A^* A p$. In exact arithmetic the two are equal. In floating point the CGLS form is more accurate, because it never forms $A^* A$, whose condition number is the square of that of $A$.

## Example

**A trace.** Take $A = \mathrm{diag}(1, \frac12, \frac14, \frac18, \frac1{16}, \frac1{32})$, $x^\dagger = (1, 1, 1, 1, 1, 1)$, and the noise $e = \frac1{20}(1, -1, 1, -1, 1, -1)$, so $\delta = \|e\| = 0.12247$. With $\tau = 1.5$, $\tau\delta = 0.18371$. The iterates were computed in exact rational arithmetic and are rounded here.

| $k$ | $x_k$ | $\|x_k - x^\dagger\|$ | $\|y^\delta - A x_k\|$ |
|---|---|---|---|
| 0 | $(0, 0, 0, 0, 0, 0)$ | 2.4495 | 1.18896 |
| 1 | $(1.0908, 0.2337, 0.0779, 0.0097, 0.0073, -0.0006)$ | 2.1007 | 0.45791 |
| 2 | $(1.0491, 0.9871, 0.3926, 0.0511, 0.0387, -0.0032)$ | 1.7896 | 0.24458 |
| 3 | $(1.05, 0.8993, 1.2304, 0.1897, 0.1493, -0.0126)$ | 1.5720 | 0.11691 |
| 4 | $(1.05, 0.9, 1.1979, 0.8499, 0.8081, -0.0711)$ | 1.1217 | 0.07137 |
| 5 | $(1.05, 0.9, 1.2, 0.5994, 1.8114, -0.1880)$ | 1.5109 | 0.01289 |
| 6 | $(1.05, 0.9, 1.2, 0.6, 1.8, -0.6)$ | 1.8473 | 0 |

The residual decreases at every step and is $0$ after six steps, where $x_6 = A^{-1} y^\delta$ (finite termination). The error decreases until $k = 4$ and then increases: this is [semi-convergence](/semi-convergence/). Line L3 returns $k = 3$, the first iterate with a residual below $0.18371$. Each step "finishes" one more component: the first component is $1.05$ from $k = 3$ on, which is $x^\dagger_1$ plus the noise $0.05/\sigma_1$.

**An integral operator.** For the diagonal model of $(A x)(s) = \int_0^s x(t)\,dt$ with 200 components, $x^\dagger = 1 - t$ (the source condition with $\nu = \frac12$) and Gaussian noise with seed 3, CGLS with $\tau = 1.5$ gave (a measurement):

| $\delta$ | stop at $k$ | error at the stop | best error (at $k$) |
|---|---|---|---|
| $10^{-2}$ | 2 | 0.0206 | 0.0126 (3) |
| $10^{-3}$ | 3 | 0.0080 | 0.0048 (4) |
| $10^{-4}$ | 5 | 0.0026 | 0.00175 (7) |
| $10^{-5}$ | 10 | 0.00071 | 0.00053 (13) |

Landweber needs hundreds to tens of thousands of steps for the same errors (see its page). The errors fall with slope about $0.5$ in $\log\delta$, as the theory gives for $\nu = \frac12$.

## Correctness

The full proof is in proofs/correctness.md, in exact arithmetic.

- **CG on the normal equations (theorem).** By induction, $r = y - A x$ and $s = A^* r$ hold after every step, and the iterates are those of CG for $A^* A z = A^* y$. On the range of $A^*$, where all vectors stay, $A^* A$ is positive definite, so the CG theorems apply.
- **Residual minimization (theorem).** $x_k$ minimizes $\|y - A x\|$ over $\mathcal{K}_k(A^* A, A^* y)$, so the residual does not increase.
- **Finite termination (theorem).** Line L4 returns after at most $\operatorname{rank}(A)$ steps with $x = A^\dagger y$.
- **Growing norm (theorem).** $\|x_k\|$ increases strictly until the end.
- **Filter factors (theorem).** $x_k = \sum_i f_i^{(k)} (u_i^T y/\sigma_i) v_i$ with $f_i^{(k)} = 1 - \prod_{j=1}^k (1 - \sigma_i^2/\theta_j)$, where $\theta_j$ are the Ritz values of $A^* A$ on the Krylov space. The filter depends on the data through the $\theta_j$, so $x_k$ is not a linear function of $y$.
- **Discrepancy stop (theorem).** If $y \in \operatorname{range}(A)$ and $\tau > 1$, line L3 passes at the latest at the breakdown step.

That CGLS with the discrepancy principle is order optimal, with error $O(\delta^{2\nu/(2\nu+1)})$ under the source condition $x^\dagger = (A^* A)^\nu w$ for every $\nu > 0$, is a theorem of Nemirovskii (1986); see EHN Chapter 7. It is cited, not proved here.

## Complexity

- **Per iteration (real-ram).** Line L5 is one product with $A$, line L9 one product with $A^*$, and lines L6 to L11 cost $O(m + n)$ for norms and vector updates. That is $O(a + m + n)$, or $O(m n)$ for a dense matrix. Line L1 costs one more product with $A^*$.
- **Iterations.** Without noise, at most $r = \operatorname{rank}(A)$ steps in exact arithmetic. With the discrepancy principle under the source condition, the stopping index is $O(\delta^{-1/(2\nu+1)})$ (a theorem, EHN Chapter 7), against $O(\delta^{-2/(2\nu+1)})$ for Landweber.
- **Space.** Four vectors $x, p$ of length $n$ and $r, q$ of length $m$, plus $s$: $O(m + n)$. The code also keeps every iterate for the tests, which takes $O(k n)$; a production version does not.

## Properties

- **Nonlinear in the data.** The step lengths and the Ritz values depend on $y$. Eicke, Louis and Plato (1990) showed that $y \mapsto x_k$ is not continuous for a fixed $k$, so a stopping index fixed in advance does not give a regularization method. The stopping index must depend on the data, as with the discrepancy principle.
- **Monotone curves.** $\|y - A x_k\|$ decreases and $\|x_k\|$ increases, the same shape as the curves of [truncated SVD](/truncated-svd/) and [Tikhonov regularization](/tikhonov-regularization/).
- **Adaptive filter.** The Ritz values converge first to the largest squared singular values (a property of the [Lanczos algorithm](/lanczos-algorithm/), which CGLS runs implicitly on $A^* A$), so CGLS filters like a truncated SVD whose cut adapts to the components that are present in the data.
- **Optimal among Krylov methods.** No other method with iterates in the same Krylov space has a smaller residual.

## Variants and improvements

- **[LSQR](/lsqr/).** The same iterates in exact arithmetic, computed by Golub-Kahan bidiagonalization. It is the more common choice in floating point and gives the bidiagonal matrix for free.
- **[Hybrid Krylov methods](/hybrid-krylov-regularization/).** Apply Tikhonov regularization to the small projected problem at each step, so the result no longer depends strongly on the exact stopping index.
- **CGME (Craig's method).** CG on $A A^* z = y$ with $x = A^* z$. It minimizes the error $\|x - x^\dagger\|$ over the same Krylov space $\mathcal{K}_k(A^* A, A^* y)$, and needs a different stopping rule (EHN Chapter 7).
- **Preconditioning.** A right preconditioner $x = L^{-1}\xi$ changes the norm that is penalized, for example to a smoothness norm. A left preconditioner changes the residual norm and the meaning of the discrepancy test.
- **Reorthogonalization.** Keeping the vectors $s_k$ orthogonal in floating point delays the effects of rounding, at $O(k n)$ extra cost per step.

## When to use it

CGLS is the standard first choice for a large ill-posed linear problem with a fast forward and adjoint code and a known noise level. It needs far fewer products than [Landweber](/landweber-iteration/) for the same error. Prefer LSQR when you also want the bidiagonal matrix, for hybrid methods or for estimates of the singular values. Prefer Landweber or a projected gradient method when you need constraints such as $x \ge 0$, or a stopping index that changes smoothly with the data. Without a reliable noise level, CGLS is fragile, because the error can increase fast after the best step; a hybrid method is then safer.

## Pitfalls

- **Updating $s$ from the normal equations.** Writing line L9 as $s \leftarrow s - \alpha A^* q$ is the same in exact arithmetic, but writing CG for an explicit $A^* A$ squares the condition number. Keep $r$ and compute $s = A^* r$ as in line L9.
- **Testing the wrong residual.** The discrepancy test of line L3 uses $\|y - A x\|$, not $\|s\| = \|A^* (y - A x)\|$. A test on $\|s\|$ has no relation to $\delta$.
- **A fixed number of steps.** Choosing $K$ in advance, without line L3, is not a regularization method (Eicke, Louis and Plato). Use a stopping rule that looks at the data.
- **Running past the stop.** Because the error can grow fast after the best $k$ (in the integral example with $\delta = 10^{-2}$, the error at $k = 6$ is $0.2627$, twenty times the best error $0.0126$ at $k = 3$), a few extra steps can ruin the result. Use $\tau$ between $1.01$ and $2$, and check line L3 at every step.
- **A wrong adjoint at line L9.** If the code for $A^*$ is not the adjoint of the code for $A$, the directions lose conjugacy and the method can stall or diverge. Run an adjoint test first.
- **Expecting exact termination.** In floating point the vectors $s_k$ lose orthogonality, and the method may need more than $\operatorname{rank}(A)$ steps to converge. For regularization this matters little, because the stop comes early.

## Implementations

## History

Hestenes and Stiefel introduced the conjugate gradient method in 1952, and their paper already gives a form for least squares problems that never forms $A^T A$. Its use for ill-posed problems grew in the 1970s and 1980s. Nemirovskii (1986) proved that it is an order optimal regularization method when it is stopped by the discrepancy principle, and Eicke, Louis and Plato (1990) showed that a stopping index fixed in advance does not give a regularization method. Hanke's 1995 monograph and Chapter 7 of Engl, Hanke and Neubauer (1996) give the full theory. Paige and Saunders (1982) gave LSQR, which computes the same iterates with better behavior in floating point.

## References
