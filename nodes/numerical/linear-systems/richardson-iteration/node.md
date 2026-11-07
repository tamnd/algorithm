---
tag: 5FXKP1
kind: algorithm
slug: richardson-iteration
name: Richardson iteration
aliases:
- Richardson method
- simple iteration
- stationary Richardson
- Landweber iteration (on the normal equations)
area: numerical/linear-systems
level: advanced
summary: X_{k+1} = x_k + omega (b - A x_k), a basic relaxation scheme.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of A", m: "the number of nonzeros of A", k: "the number of steps"}
  time: {worst: "Θ(k (n + m))", best: "Θ(n + m)"}
  space: {extra: Θ(n)}
  flops: {worst: "k (2m + 4n)"}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [matrix-splitting, spectral-radius, positive-definite-matrix]
see_also: [chebyshev-iteration, jacobi-method, successive-over-relaxation, conjugate-gradient-method, preconditioning, krylov-subspace, multigrid-method, tikhonov-regularization]
sources:
  - paper: doi:10.1098/rsta.1911.0009
    title: Lewis F. Richardson, The approximate arithmetical solution by finite differences of physical problems involving differential equations, with an application to the stresses in a masonry dam, Philosophical Transactions of the Royal Society A 210, 1911
    locator: the iteration with a sequence of parameters chosen to damp the error components over a range of eigenvalues
  - book: isbn:9780898713961
    title: Anne Greenbaum, Iterative Methods for Solving Linear Systems, SIAM, 1997
    locator: Chapter 2, Some Iteration Methods (simple iteration, its preconditioned form and its convergence)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 17, Stationary Iterative Methods (error analysis of splitting iterations; Richardson is the splitting with M = I / omega)
---

Richardson iteration solves $A x = b$ by repeatedly adding a fixed multiple of the residual: $x_{k+1} = x_k + \omega (b - A x_k)$. Each step costs one product with $A$. For symmetric positive definite $A$ it converges exactly when $0 < \omega < 2/\lambda_{\max}$, and with the best constant $\omega$ the error shrinks by $(\kappa - 1)/(\kappa + 1)$ per step, so about $\tfrac{\kappa}{2}\ln(1/\varepsilon)$ steps are needed. Varying $\omega$ from step to step along the reciprocals of Chebyshev roots reduces this to about $\tfrac{\sqrt\kappa}{2}\ln(2/\varepsilon)$. Every stationary splitting method is Richardson applied to a preconditioned system.

## In plain words

You have a guess. Multiply it by the matrix and see how far the result is from the right side: that gap is the residual. Add a fixed fraction of the gap to your guess and repeat. If the fraction is small enough, each round brings the guess closer, but the parts of the error that the matrix shrinks most are fixed slowly, and the parts it stretches most can overshoot. The best fixed fraction balances the two, and the method is fast only when the matrix stretches every direction by about the same amount.

## The problem

**Notation.** $A \in \mathbb{R}^{n \times n}$ nonsingular, $b \in \mathbb{R}^n$, $x$ the solution of $A x = b$. $x_k$ is the iterate after $k$ steps, $r_k = b - A x_k$ its [residual](/residual/), $e_k = x_k - x$ its error, and $\mathcal{K}_k(A, r_0) = \mathrm{span}\{r_0, A r_0, \ldots, A^{k-1} r_0\}$ the [Krylov subspace](/krylov-subspace/). The iteration matrix is $G_\omega = I - \omega A$, with [spectral radius](/spectral-radius/) $\rho(G_\omega)$. For symmetric positive definite $A$, $\lambda_{\min}$ and $\lambda_{\max}$ are the extreme eigenvalues and $\kappa = \kappa_2(A) = \lambda_{\max}/\lambda_{\min}$. $u = 2^{-53}$.

**Input.** $A$ (any representation that supports $v \mapsto A v$), $b$, a parameter $\omega$ or a list $\omega_0, \ldots, \omega_{m-1}$ used cyclically, $x_0$, a tolerance and a step limit.

**Output.** $x_k$ with $\|r_k\|_2 \le \mathrm{tol}\,\|b\|_2$, or the last iterate and a flag. In [matrix splitting](/matrix-splitting/) form, $A = M - N$ with $M = I/\omega$.

## The algorithm

```pseudo id=main
RICHARDSON(A, b, ω, x_0, tol, maxiter)
L1  x ← x_0
L2  r ← b − A x
L3  for k ← 0 to maxiter do
L4      if ‖r‖_2 ≤ tol · ‖b‖_2 then return (x, k, converged)
L5      x ← x + ω_k r                         ▷ ω_k = ω, or the k-th parameter of the cycle
L6      r ← b − A x                           ▷ the one product with A per step
L7  return (x, maxiter, not converged)
```

Line L6 can be replaced by the update $r \leftarrow r - \omega_k A r$, which uses the same one product; recomputing $r$ from $x$ keeps the residual honest in floating point.

## Example

**A diagonal matrix, exactly.** For $A = \mathrm{diag}(1, 2, 4)$, $b = (1, 1, 1)^T$, $x_0 = 0$, the best constant is $\omega^* = 2/(1 + 4) = 2/5$. Then $r_k = \big((3/5)^k, (1/5)^k, (-3/5)^k\big)$: the smallest and largest eigenvalues contract at the same rate $3/5 = (\kappa - 1)/(\kappa + 1)$ with $\kappa = 4$, one from above and one with alternating sign.

**The model problem.** For $A = \mathrm{tridiag}(-1, 2, -1)$ of order $n = 20$, $\lambda_{\min} = 0.02234$, $\lambda_{\max} = 3.97766$, $\kappa = 178.1$, $\omega^* = 0.5$ and $\rho = 0.98883$. With $b = (1, \ldots, 1)^T$, $x_0 = 0$ and tolerance $10^{-8}$:

| parameters | predicted steps | observed |
|---|---|---|
| $\omega = 0.25$ | 3289 | 3275 |
| $\omega = \omega^* = 0.5$ | 1640 | 1633 |
| cycle of 16 Chebyshev parameters | about 11 cycles | 177 steps |
| $\omega = 0.6 > 2/\lambda_{\max} = 0.503$ | diverges | residual $3.9 \times 10^{11}$ after 100 steps |

The prediction for constant $\omega$ is $\ln 10^{-8}/\ln\rho(G_\omega)$; for the Chebyshev cycle each block of 16 steps reduces the residual by at least $1/T_{16}(1.0113) = 0.18$. With $\omega = 2/\lambda_{\max}$ exactly, the component along the top eigenvector is multiplied by $-1$ at each step, and for $b = e_1$ the residual neither grows nor decays: the iteration stagnates.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). From line L5, $e_{k+1} = (I - \omega_k A) e_k$ and $r_{k+1} = (I - \omega_k A) r_k$, so
$$r_k = p_k(A)\, r_0, \qquad p_k(t) = \prod_{j<k}(1 - \omega_j t), \qquad x_k \in x_0 + \mathcal{K}_k(A, r_0).$$

- **Convergence (proved).** With constant $\omega$ the iteration converges for every $x_0$ if and only if every eigenvalue of $A$ lies in the open disc with center and radius $1/\omega$. So all eigenvalues must lie in one open half plane; a symmetric indefinite $A$ admits no convergent $\omega$. For symmetric positive definite $A$ the condition is $0 < \omega < 2/\lambda_{\max}$.
- **Rate (proved, symmetric $A$).** $\|r_k\|_2 \le \rho(G_\omega)^k \|r_0\|_2$, minimized by $\omega^* = 2/(\lambda_{\min} + \lambda_{\max})$ with $\rho = (\kappa - 1)/(\kappa + 1) \approx 1 - 2/\kappa$. The bound is attained when $r_0$ has components along both extreme eigenvectors.
- **Chebyshev parameters (proved, symmetric $A$).** With $\omega_j$ the reciprocals of the roots of $T_m$ mapped to $[\lambda_{\min}, \lambda_{\max}]$, $\|r_m\|_2 \le \|r_0\|_2/T_m\big(\frac{\kappa + 1}{\kappa - 1}\big) \le 2\big(\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\big)^m \|r_0\|_2$. This is optimal among all $m$-step polynomial methods that know only $[\lambda_{\min}, \lambda_{\max}]$.
- **Exact roots.** If the $\omega_j$ are the reciprocals of the distinct eigenvalues, $r = 0$ after that many steps in exact arithmetic.

**In floating point.** Each step computes $r$ with error at most about $\gamma_{w} |A||x_k|$ componentwise, $w$ the largest number of nonzeros in a row, so the computed residual stalls near a multiple of $u\,\|A\|\,\|x\|$; for the model problem above the observed level is below $n u \|A\|_\infty \|x\|_\infty$ and the error at stagnation is $2.6 \times 10^{-13}$ (the residual $7.1 \times 10^{-15}$), while asking for $10^{-18}$ never stops. This limiting level is observed; Higham (Chapter 17) bounds it for stationary iterations in terms of $\|(I - G_\omega)^{-1}\|$ and $|M|+|N|$. The Chebyshev cycle in the natural order of the roots amplifies rounding errors for large $m$; Lebedev and Finogenov's orderings of the roots make it stable, and the three-term [Chebyshev iteration](/chebyshev-iteration/) avoids the problem.

## Complexity

One step costs a product with $A$ ($2\,\mathrm{nnz}(A)$ flops for a sparse matrix, $2n^2$ for a dense one), an axpy ($2n$) and a norm ($2n$), so $2\,\mathrm{nnz}(A) + 4n$ flops; storage is $x$, $r$ and $b$. The matrix is streamed once per step at two flops per nonzero, so the speed is bounded by memory bandwidth. The number of steps to reduce the residual by $\varepsilon$ is about $\tfrac{\kappa}{2}\ln(1/\varepsilon)$ with $\omega^*$ and about $\tfrac{\sqrt\kappa}{2}\ln(2/\varepsilon)$ with Chebyshev parameters. For the $d$-dimensional Poisson model with $h = 1/(n+1)$, $\kappa = O(h^{-2})$, so plain Richardson needs $O(n^2)$ steps. [Conjugate gradients](/conjugate-gradient-method/) attain the Chebyshev rate without knowing the spectrum.

## Properties

- **Matrix free.** Only products $v \mapsto A v$ are needed; neither $A$'s entries nor its diagonal are used, unlike [Jacobi](/jacobi-method/) or [SOR](/successive-over-relaxation/).
- **Polynomial method.** The iterate lies in $x_0 + \mathcal{K}_k(A, r_0)$, so Richardson is the simplest Krylov method, with a residual polynomial fixed in advance.
- **Fully parallel.** Each step is one product and one vector update, with one reduction for the norm.
- **Invariant under orthogonal changes of basis.** Replacing $A$ by $Q^T A Q$, $b$ by $Q^T b$ and $x_0$ by $Q^T x_0$ gives $Q^T x_k$.
- **Needs spectral information.** Without bounds on the eigenvalues there is no safe choice of $\omega$.

## Variants and improvements

- **Preconditioned Richardson.** $x_{k+1} = x_k + \omega M^{-1} r_k$. With $M = D$ and $\omega = 1$ it is [Jacobi](/jacobi-method/), with $M = D - E$ Gauss-Seidel, with $M = D/\omega - E$ [SOR](/successive-over-relaxation/): every splitting method is Richardson for $M^{-1} A$, which is why [preconditioning](/preconditioning/) and splitting are two names for one idea.
- **Chebyshev (nonstationary) Richardson.** Richardson's own 1911 scheme used varying parameters; with Chebyshev roots it gives the $\sqrt\kappa$ rate. The three-term [Chebyshev iteration](/chebyshev-iteration/) gets the same polynomials stably.
- **Steepest descent and minimal residual.** Choosing $\omega_k = r_k^T r_k / r_k^T A r_k$ (steepest descent, SPD $A$) or $\omega_k = r_k^T A r_k / \|A r_k\|_2^2$ (minimal residual) needs no spectral bounds but converges no faster than the optimal stationary rate in the worst case.
- **Landweber iteration.** Richardson on the normal equations, $x_{k+1} = x_k + \omega A^T(b - A x_k)$ with $0 < \omega < 2/\sigma_{\max}^2$. Stopping early acts as a regularization, comparable to [Tikhonov regularization](/tikhonov-regularization/), for ill-posed problems.
- **Smoother in multigrid.** Damped Richardson or damped Jacobi removes the high frequency error in a few steps, which is all a [multigrid](/multigrid-method/) smoother must do.

## When to use it

Use Richardson when $A$ is available only as an operator, its spectrum is known to lie in a known interval of the positive axis, and simplicity or parallelism matter more than the number of steps; or as a smoother, or as the outer loop around a good preconditioner, where $M^{-1}A$ is close to $I$ and $\omega = 1$ works. For a stand-alone solver of an SPD system, conjugate gradients are almost always better, since they need no $\omega$ and attain the Chebyshev rate.

## Pitfalls

- **$\omega$ too large.** For $\omega > 2/\lambda_{\max}$ the top component grows by $|1 - \omega\lambda_{\max}| > 1$ per step; overestimating $\lambda_{\max}$ is safe, underestimating it is not.
- **$\omega = 2/\lambda_{\max}$ exactly.** The top component oscillates with factor $-1$ and the iteration stagnates.
- **Indefinite or complex spectrum.** With eigenvalues on both sides of the origin, as for $\begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$ with eigenvalues $3$ and $-1$, no constant $\omega$ converges.
- **Large $\kappa$.** The step count grows like $\kappa$, so even well chosen parameters are slow on discretized PDEs without preconditioning.
- **Unstable parameter order.** Chebyshev parameters applied in increasing or decreasing order can amplify the error between cycles by huge factors for large $m$ in floating point.
- **Stopping below the rounding level.** The residual stalls near $u\,\|A\|\,\|x\|$.

## Implementations

## History

Lewis Fry Richardson (1911) introduced the method to compute stresses in a masonry dam by hand, choosing a sequence of parameters to damp the error over a range of frequencies. Its analysis as a matrix iteration came with the splitting methods of the 1950s. Young, Shortley, and Golub and Varga (1961) connected the parameter choice to Chebyshev polynomials and to the second-order Richardson method, which is the [Chebyshev iteration](/chebyshev-iteration/); Lebedev and Finogenov (around 1971) found stable orderings of the parameters. Landweber (1951) applied the iteration to the normal equations of integral equations of the first kind.

## References
