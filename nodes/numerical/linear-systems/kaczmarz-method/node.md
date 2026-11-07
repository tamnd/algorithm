---
tag: 3ES5VF
kind: algorithm
slug: kaczmarz-method
name: Kaczmarz method
aliases:
- algebraic reconstruction technique
- ART
- randomized Kaczmarz
- row-action method
area: numerical/linear-systems
level: advanced
summary: Project the iterate onto one equation's hyperplane at a time, cycling or sampling rows.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {m: "the number of rows of A", n: "the number of columns of A", z: "the number of nonzeros of A", κ: "the scaled condition number ‖A‖_F ‖A^+‖_2", ε: "the factor by which the expected squared error must drop"}
  time: {expected: "O(z + m + (n + log m) κ^2 log(1/ε))"}
  space: {extra: Θ(m + n)}
  steps: {expected: "⌈κ^2 ln(1/ε)⌉"}
  flops: {per_sweep: "6 z + O(m)"}
properties: {deterministic: false, in_place: false, recursive: false, iterative: true, matrix_free: false}
prereqs: [linear-system-solving, matrix-norms, singular-value-decomposition]
see_also: [gauss-seidel-method, least-squares-problem, stochastic-gradient-descent, conjugate-gradient-method, successive-over-relaxation, pseudoinverse, sparse-linear-systems, condition-number]
sources:
  - paper: "Stefan Kaczmarz, Angenäherte Auflösung von Systemen linearer Gleichungen, Bulletin International de l'Académie Polonaise des Sciences et des Lettres A 35, 1937"
    title: Angenäherte Auflösung von Systemen linearer Gleichungen
    locator: pp. 355 to 357 (the cyclic projection method and its convergence for square nonsingular systems)
  - paper: doi:10.1007/s00041-008-9030-4
    title: Thomas Strohmer and Roman Vershynin, A randomized Kaczmarz algorithm with exponential convergence, Journal of Fourier Analysis and Applications 15(2), 2009
    locator: pp. 262 to 278 (Theorem 2, the expected rate 1 - 1/kappa(A)^2 with rows sampled by squared norm)
  - paper: doi:10.1007/s10543-010-0265-5
    title: Deanna Needell, Randomized Kaczmarz solver for noisy linear systems, BIT Numerical Mathematics 50(2), 2010
    locator: pp. 395 to 403 (Theorem 2.1, convergence to a ball of radius sqrt(R) gamma)
  - paper: doi:10.1016/0022-5193(70)90109-8
    title: Richard Gordon, Robert Bender and Gabor T. Herman, Algebraic reconstruction techniques (ART) for three-dimensional electron microscopy and X-ray photography, Journal of Theoretical Biology 29(3), 1970
    locator: pp. 471 to 481
  - paper: doi:10.1007/BF01436376
    title: Kunio Tanabe, Projection method for solving a singular system of linear equations and its applications, Numerische Mathematik 17(3), 1971
    locator: pp. 203 to 214 (convergence to the solution nearest x_0 for consistent systems, and limit cycles for inconsistent ones)
  - book: isbn:9780898713602
    title: Åke Björck, Numerical Methods for Least Squares Problems, SIAM, 1996
    locator: Chapter 7, iterative methods (row projection methods and Kaczmarz as SOR on A A^T y = b)
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 8.2, Row Projection Methods (Kaczmarz as Gauss-Seidel on A A^T y = b)
---

The Kaczmarz method solves a linear system $A x = b$ with $A \in \mathbb{R}^{m \times n}$ by visiting one equation at a time and moving the iterate to the nearest point that satisfies it exactly: $x \leftarrow x + \frac{b_i - a_i^T x}{\|a_i\|_2^2}\, a_i$, an orthogonal projection onto the hyperplane $a_i^T x = b_i$. A step reads one row, costs about $4$ flops per nonzero, and needs no other storage, so the method suits huge, sparse or streamed systems, and it was the first image reconstruction algorithm of computed tomography (ART, 1970). For a consistent system the error never increases, and the cyclic method converges to the solution nearest the starting point. With rows chosen at random with probability proportional to $\|a_i\|_2^2$ (Strohmer and Vershynin 2009) the expected squared error drops by the factor $1 - 1/\kappa^2$ per step, where $\kappa = \|A\|_F \|A^+\|_2$. The rate depends on $\kappa^2$, so on ill conditioned problems it is slow, and on inconsistent systems it does not converge to the least squares solution without relaxation or extension.

## In plain words

Each equation of the system describes a flat surface, and the solution is the point where all the surfaces meet. Start anywhere. Pick one equation and jump straight to the closest point on its surface. Then pick another equation and do the same. Each jump can only bring you closer to the meeting point, never farther. When the surfaces cross at wide angles you get there quickly; when they are nearly parallel you zigzag for a long time. Picking the equations at random, favouring the ones with larger coefficients, gives a provable speed.

## The problem

Given $A \in \mathbb{R}^{m \times n}$ with rows $a_1^T, \ldots, a_m^T$, and $b \in \mathbb{R}^m$, find $x$ with $A x = b$. The method makes most sense when $A$ is large and sparse, or available only one row at a time, and $m$ may exceed $n$ or be smaller.

**Notation.** $x_k$ is the iterate after $k$ row steps and $r_k = b - A x_k$ its residual. For a consistent system, $x^\ast$ is a solution and $e_k = x_k - x^\ast$. The relaxation factor is $\omega \in (0, 2)$, $\omega = 1$ being the plain projection. $\sigma_{\min}$ is the smallest nonzero singular value of $A$, $A^+$ the [pseudoinverse](/pseudoinverse/), $\|A\|_F$ the Frobenius norm, and $\kappa = \|A\|_F \|A^+\|_2 = \|A\|_F / \sigma_{\min} \ge \sqrt{\operatorname{rank} A}$. A sweep is $m$ row steps. The unit roundoff is $u = 2^{-53}$.

## The algorithm

```pseudo id=main
KACZMARZ(A, b, x₀, ω, tol, maxit)
L1  x ← x₀; compute ‖a_i‖² for every row
L2  for sweep ← 1 to maxit do
L3      for t ← 1 to m do
L4          i ← t (cyclic), or i drawn with probability ‖a_i‖² / ‖A‖_F² (randomized)
L5          if ‖a_i‖² = 0 then continue
L6          δ ← ω · (b_i − a_iᵀ x) / ‖a_i‖²
L7          x ← x + δ · a_i
L8      r ← b − A x
L9      if ‖r‖₂ ≤ tol · ‖b‖₂ then return x, "converged"
L10 return x, "maxit"
```

The randomized row choice at line L4 is drawn from the cumulative sums of $\|a_i\|^2$ by binary search. The residual test at lines L8 and L9 costs one product with $A$ per sweep; implementations that only stream rows test less often or estimate the residual from the step sizes $|\delta|$.

## Example

Take $A = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$, $b = (1, 2)^T$, with solution $x^\ast = (1, 1)$, and $x_0 = 0$, cyclic order, $\omega = 1$.

| step | row | $b_i - a_i^T x$ | $\|a_i\|^2$ | $x$ | $\|e\|_2^2$ |
|---|---|---|---|---|---|
| 0 | | | | $(0, 0)$ | $2$ |
| 1 | 1 | $1$ | $1$ | $(1, 0)$ | $1$ |
| 2 | 2 | $1$ | $2$ | $(3/2, 1/2)$ | $1/2$ |
| 3 | 1 | $-1/2$ | $1$ | $(1, 1/2)$ | $1/4$ |
| 4 | 2 | $1/2$ | $2$ | $(5/4, 3/4)$ | $1/8$ |

Each squared error is the previous one minus $(b_i - a_i^T x)^2 / \|a_i\|^2$, as Theorem 2 below states: $2 - 1 = 1$, $1 - 1/2 = 1/2$, and so on. The two lines meet at $45°$, and with two hyperplanes the error after each sweep shrinks by $\cos^2 45° = 1/2$: the errors after sweeps $1$ and $2$ are $(1/2, -1/2)$ and $(1/4, -1/4)$.

## Correctness

The proofs are in `proofs/correctness.md`. Exact arithmetic.

1. **Projection.** With $\omega = 1$, line L7 gives $a_i^T x = b_i$, and the new $x$ is the point of the hyperplane nearest to the old one.
2. **Error identity (proved).** For a consistent system and any solution $x^\ast$, one step gives $\|e_{\text{new}}\|_2^2 = \|e_{\text{old}}\|_2^2 - \omega(2 - \omega)\,(b_i - a_i^T x_{\text{old}})^2 / \|a_i\|_2^2$. So for $0 < \omega < 2$ the error is nonincreasing, and for $\omega = 2$ (reflection) its norm is constant.
3. **Cyclic convergence (proved, Kaczmarz 1937 for square nonsingular $A$; Tanabe 1971 in general).** If $A x = b$ is consistent and $0 < \omega < 2$, the cyclic iterates converge to $\bar x = A^+ b + (I - A^+ A) x_0$, the solution nearest $x_0$; for $x_0 = 0$, the minimum norm solution.
4. **Randomized rate (proved, Strohmer and Vershynin 2009, Theorem 2).** If $A x = b$ is consistent, $\omega = 1$ and rows are sampled with probability $\|a_i\|^2/\|A\|_F^2$, then $\mathbb{E}\,\|x_k - \bar x\|_2^2 \le (1 - \kappa^{-2})^k \|x_0 - \bar x\|_2^2$. Strohmer and Vershynin state it for full column rank; the same proof works with $\sigma_{\min}$ the smallest nonzero singular value, since $x_k - \bar x$ stays in the row space.
5. **Noisy systems (proved, Needell 2010).** If $b = A x^\ast + \eta$ with $A$ of full column rank, then $\mathbb{E}\,\|x_k - x^\ast\|_2 \le (1 - \kappa^{-2})^{k/2} \|x_0 - x^\ast\|_2 + \kappa\,\gamma$, where $\gamma = \max_i |\eta_i| / \|a_i\|_2$. The iterates reach a ball whose radius is set by the noise, then wander in it.
6. **Termination.** The loop stops after at most $maxit$ sweeps, reporting "maxit" if the residual test fails, which is the expected outcome for an inconsistent or very ill conditioned system.

**Floating point (observed and partly proved).** Each step is a dot product and an axpy, so the computed step has a relative error of order $n u$ in $\delta$. Errors do not accumulate in a harmful way, because the next projection corrects them, but the attainable residual is about $u\,\|A\|\,\|x\|$ times a modest factor, like a backward stable method. The tests reach normwise backward errors below $10^{-12}$ on well conditioned systems.

## Complexity

A row step with $z_i$ nonzeros costs $2 z_i$ flops for $b_i - a_i^T x$, $2$ for line L6 and $2 z_i$ for line L7. A sweep costs $4 z + 2m$ flops and the residual check $2 z + m$ more, so $6 z + O(m)$ per sweep. By the expected rate, $k = \lceil \kappa^2 \ln(1/\varepsilon) \rceil$ randomized steps make $\mathbb{E}\|e_k\|^2 \le \varepsilon \|e_0\|^2$, and each step costs $O(n + \log m)$ with the binary search, which gives the expected time in the front matter. The cyclic method has no such general bound; its rate depends on the row order and on the angles between the hyperplanes. The extra storage is the $m$ squared row norms (and their cumulative sums) and the iterate. Proofs are in `proofs/complexity.md`.

## Properties

- **Row action**: one row at a time, so $A$ can be streamed from disk or generated on the fly, and rows can be processed in any order.
- **Fejér monotone**: for consistent systems the distance to every solution is nonincreasing (Theorem 2).
- **Stays in $x_0 + \operatorname{range}(A^T)$**: each step adds a multiple of a row, which is why the limit is the solution nearest $x_0$.
- **Equivalent to Gauss-Seidel on $A A^T y = b$** with $x = A^T y$: line L6 is exactly the Gauss-Seidel update of $y_i$, and relaxation makes it SOR (Björck and Elfving 1979). So the cyclic rate is that of [Gauss-Seidel](/gauss-seidel-method/) on a matrix with condition number $\kappa_2(A)^2$.
- **Equivalent to [stochastic gradient descent](/stochastic-gradient-descent/)** on $\frac{1}{2}\sum_i (a_i^T x - b_i)^2 / \|a_i\|^2$ with unit step, sampled by row norm.
- **Not deterministic** in the randomized form; the implementation fixes a seed.

## Variants and improvements

- **Relaxation.** $\omega \in (0, 2)$ in line L6. For inconsistent systems, relaxation parameters $\omega_k \to 0$ with $\sum \omega_k = \infty$ give convergence to a weighted least squares solution (Censor, Eggermont and Gordon 1983); with a fixed $\omega$ the cyclic limit points depend on $\omega$, and on the example $x \in \mathbb{R}$, rows $x = 0$ and $x = 2$ the end-of-sweep limit is $2/(2 - \omega)$, which tends to the least squares solution $1$ only as $\omega \to 0$.
- **Randomized extended Kaczmarz** (Zouzias and Freris 2013). Alternate Kaczmarz steps with steps that remove the component of $b$ outside $\operatorname{range}(A)$; converges in expectation to the minimum norm least squares solution, with rate again governed by $\kappa^2$.
- **Block Kaczmarz** (Elfving 1980; Needell and Tropp 2014). Project onto the intersection of a block of rows, $x \leftarrow x + A_\tau^+ (b_\tau - A_\tau x)$; better use of cache and parallelism.
- **SIRT, Cimmino and Landweber.** Average the projections onto all rows simultaneously, $x \leftarrow x + \omega A^T D (b - A x)$; slower per step, but fully parallel and with built-in regularization by early stopping, popular in tomography.
- **Sketch and project** (Gower and Richtárik 2015). A framework that contains randomized Kaczmarz, randomized coordinate descent and block variants, with a unified rate.
- **Greedy and adaptive row selection.** Choose the row with the largest scaled residual (Motzkin's relaxation, or the greedy randomized Kaczmarz of Bai and Wu 2018); each step costs a full residual update.
- **Acceleration.** CGMN applies [CG](/conjugate-gradient-method/) to the symmetric Kaczmarz sweep (forward then backward), turning the $\kappa^2$ dependence of the stationary method into $\kappa$ for the number of sweeps (Björck and Elfving).

## When to use it

Use it when the rows of $A$ are expensive to store or arrive one at a time (tomography, online estimation), when $A$ is huge and very sparse with rows of very different sizes, or as a smoother or inner solver. For a well conditioned system that fits in memory, [CG](/conjugate-gradient-method/) on the normal equations (CGLS, LSQR) or a direct [least squares](/least-squares-problem/) solver is faster, because Kaczmarz needs $O(\kappa^2)$ steps where Krylov methods need $O(\kappa)$ iterations. For square systems with known structure, preconditioned Krylov methods are usually better.

## Pitfalls

- **Inconsistent systems do not converge.** With noise, the cyclic method settles into a limit cycle and the randomized one into a ball of radius about $\kappa \gamma$; neither gives the least squares solution. The tests show the example of two rows $x = 0$, $x = 2$: every sweep ends at $x = 2$ while the least squares solution is $1$. Use relaxation tending to zero, the extended method, or LSQR.
- **Slow on ill conditioned problems.** The rate $1 - \kappa^{-2}$ means about $\kappa^2$ steps per digit. On the $8 \times 8$ [Hilbert matrix](/hilbert-matrix/) $200$ sweeps leave the relative residual far above $10^{-10}$; the error still decreases at every step.
- **Row scaling changes the randomized method.** Sampling by $\|a_i\|^2$ depends on the scaling of the equations. Strohmer and Vershynin's rate is not invariant under row scaling, while the cyclic iteration's projections are.
- **Row order matters for the cyclic method.** Sweeping rows of a mesh problem in a coherent order can be much slower than a random order; random permutation of the rows per sweep is a cheap fix.
- **Zero rows.** A zero row with $b_i \ne 0$ means the system is inconsistent; line L5 skips the row, so the method cannot detect it unless the residual test is used.
- **Stopping on $|\delta|$ alone.** Small steps can mean slow progress rather than convergence; test the residual.

## Implementations

## History

Stefan Kaczmarz published the method in a three page note in 1937 and proved its convergence for square nonsingular systems; he was killed in the Second World War a few years later. Gordon, Bender and Herman rediscovered it in 1970 as the algebraic reconstruction technique for electron microscopy and X-ray photography, and it was used in the first CT scanner built by Hounsfield. Tanabe (1971) analysed singular and inconsistent systems, Björck and Elfving (1979) connected it to SOR and CG on $A A^T$, and Censor and coauthors developed the theory of row action methods. The randomized version with a proved exponential rate, by Strohmer and Vershynin in 2009, started a large literature on randomized iterative solvers, including Needell's noisy analysis and the sketch and project framework.

## References
