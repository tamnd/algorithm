---
tag: HF6T4X
kind: algorithm
slug: inexact-newton-bundle-adjustment
name: Bundle adjustment in the large
aliases:
- inexact Newton bundle adjustment
- preconditioned conjugate gradient bundle adjustment
area: computer-vision/structure-from-motion
level: research
summary: Solve the reduced camera system of very large bundle adjustments approximately by conjugate gradients with block Jacobi or Schur preconditioners.
solves: [bundle-adjustment]
model: real-ram
complexity:
  vars: {N: "the number of cameras", n: "the number of points", m: "the number of observations", k: "the number of CG iterations in one step"}
  time: {per_iteration: "O(k (m + N))"}
  space: {extra: "O(m + n + N)"}
properties: {deterministic: true, iterative: true, local: true, recursive: false, monotone: true}
history:
  year: 2010
  people: [Sameer Agarwal, Noah Snavely, Steven M. Seitz, Richard Szeliski]
  note: Agarwal, Snavely, Seitz and Szeliski studied inexact Levenberg-Marquardt steps with preconditioned conjugate gradients on the reduced camera system for reconstructions from large photo collections.
prereqs: [sparse-bundle-adjustment, reduced-camera-system, conjugate-gradient-method, preconditioning]
see_also: [bundle-adjustment, levenberg-marquardt, krylov-subspace, incomplete-cholesky-factorization, newton-method-for-systems, global-structure-from-motion, incremental-structure-from-motion, schur-complement]
sources:
  - paper: doi:10.1007/978-3-642-15552-9_3
    title: "Sameer Agarwal, Noah Snavely, Steven M. Seitz and Richard Szeliski, Bundle adjustment in the large, Computer Vision ECCV 2010, Lecture Notes in Computer Science 6312, Springer, 2010, 29-42"
    locator: "the whole paper (inexact step Levenberg-Marquardt, the implicit and explicit Schur complement, the block Jacobi and Schur-Jacobi preconditioners and the experiments)"
  - paper: doi:10.1137/0719025
    title: "Ron S. Dembo, Stanley C. Eisenstat and Trond Steihaug, Inexact Newton methods, SIAM Journal on Numerical Analysis 19(2), 1982, 400-408"
    locator: "the whole paper (the forcing sequence and the local convergence theorems)"
  - paper: doi:10.1007/978-3-642-15552-9_9
    title: "Martin Byröd and Kalle Åström, Conjugate gradient bundle adjustment, Computer Vision ECCV 2010, Lecture Notes in Computer Science 6312, Springer, 2010"
    locator: "the whole paper (preconditioned conjugate gradients on the bundle adjustment least squares problem)"
  - book: isbn:9780387303031
    title: "Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006"
    locator: "Chapter 5 (the conjugate gradient method, Theorems 5.1 and 5.2, preconditioning) and Section 7.1 (inexact Newton methods)"
  - paper: doi:10.1007/3-540-44480-7_21
    title: "Bill Triggs, Philip F. McLauchlan, Richard I. Hartley and Andrew W. Fitzgibbon, Bundle adjustment, a modern synthesis, in Vision Algorithms, Theory and Practice, Lecture Notes in Computer Science 1883, Springer, 2000, 298-372"
    locator: "Section 6, Network structure and implementation (Section 6.1, the Schur complement and the reduced bundle system)"
---

Bundle adjustment in the large is [Levenberg-Marquardt](/levenberg-marquardt/) for [bundle adjustment](/bundle-adjustment/) in which each damped step is computed only approximately. It keeps the point elimination of [sparse bundle adjustment](/sparse-bundle-adjustment/), but it does not form or factor the [reduced camera system](/reduced-camera-system/) $S \delta_a = e$. It runs the preconditioned [conjugate gradient method](/conjugate-gradient-method/) on that system instead. Each product $S x = U^* x - W V^{*-1} W^{\mathsf T} x$ is computed block by block from the per-observation blocks, so the work and memory per CG iteration are linear in the number of observations. The preconditioner is block Jacobi on $S$: the inverses of its $6 \times 6$ diagonal blocks. CG stops early, when the residual is a fraction $\eta$ of the right side, as in the inexact Newton methods of Dembo, Eisenstat and Steihaug. The point steps are then recovered exactly. This is the method of choice when the number of cameras $N$ is so large that the dense $6N \times 6N$ matrix $S$, or its Cholesky factor, does not fit in memory. Among the close pages, sparse bundle adjustment solves the same system exactly, and the reduced camera system page describes the elimination itself.

## In plain words

Sparse bundle adjustment shrinks the big bundle adjustment system to a system about the cameras only, and solves that exactly. With tens of thousands of cameras even that small system is too big to store and solve. This method never writes it down. It only needs to know what the system does to a vector, and it can work that out from the many tiny blocks that each photo measurement gives. With that, it solves the system roughly, by a few steps of the conjugate gradient method, which improves a guess one direction at a time. A rough answer is good enough, because the outer loop corrects it at the next step, and the usual Levenberg-Marquardt test still rejects any step that does not lower the error.

## The problem

**Input.** As for [sparse bundle adjustment](/sparse-bundle-adjustment/): a shared intrinsic matrix $K$, start values for $N$ cameras $(R_i, t_i)$ and $n$ points $X_j$, $m$ observations $(i, j, x_{ij})$, the fixed cameras, and a damping factor $\tau$. In addition, a forcing parameter $\eta \in (0, 1)$ and an optional cap $k_{\max}$ on the CG iterations of one step. The camera frame has $X$ right, $Y$ down and $Z$ forward, $X_c = R_i X_j + t_i$, and pixel centers are at integer coordinates.

**Output.** Cameras and points at a local minimizer of $F = \tfrac12 \sum_{(i, j)} \|\pi(K (R_i X_j + t_i)) - x_{ij}\|^2$, with $F$ no larger than at the start.

## The algorithm

```pseudo id=main
INEXACT-NEWTON-BA(K, cameras, points, observations, τ, η, k_max)
L1  ν <- 2 ; build U_i, V_j, W_ij, g_a, g_b from the observation blocks
L2  μ <- τ · max diagonal entry of U and V
L3  loop
L4      if ||g||_∞ <= ε_1 then return
L5      V*_j^-1 <- (V_j + μ I)^-1 for each point ; e <- -g_a + W V*^-1 g_b
L6      P_i <- (U_i + μ I - Σ_j W_ij V*_j^-1 W_ij^T)^-1 for each free camera     ▷ block Jacobi
L7      δa <- PCG from 0 on S δa = e, with S x computed as U* x - W (V*^-1 (W^T x)) and preconditioner P, until ||e - S δa|| <= η ||e|| or k_max iterations
L8      for each point j: δb_j <- -V*_j^-1 (g_b,j + Σ_i W_ij^T δa_i)
L9      if ||δ|| <= ε_2 (||x|| + ε_2) then return
L10     pred <- -g^T δ - ½ ||J δ||^2 ; ρ <- (F(x) - F(x ⊕ δ)) / pred
L11     if ρ > 0 then x <- x ⊕ δ ; rebuild the blocks ; μ <- μ · max(1/3, 1 - (2ρ - 1)^3) ; ν <- 2
L12     else μ <- μ ν ; ν <- 2 ν
L13 return cameras, points
```

Lines L1 to L4 and L9 to L12 are the Levenberg-Marquardt loop of sparse bundle adjustment. Line L5 inverts the $3 \times 3$ point blocks and forms the right side of the reduced system. Line L6 builds the block Jacobi preconditioner: each diagonal block $S_{ii}$ gets one $6 \times 6$ term for each point that camera $i$ sees, so this costs $O(m)$. Line L7 is the inexact solve. A product with $S$ first gathers $W^{\mathsf T} x$ point by point, multiplies by the $3 \times 3$ inverses, and scatters the result back to the cameras. Line L8 is the exact back-substitution. Line L10 computes the predicted reduction from its definition, with $\|J \delta\|^2 = \delta_a^{\mathsf T} U \delta_a + 2 \delta_a^{\mathsf T} W \delta_b + \delta_b^{\mathsf T} V \delta_b$. The short formula $\tfrac12 \delta^{\mathsf T} (\mu \delta - g)$ of exact Levenberg-Marquardt is wrong here, because the step does not solve the damped system.

## Example

The test scene is the one of the sparse bundle adjustment page: 4 cameras, camera 0 fixed, 20 points, 80 observations, an $18 \times 18$ matrix $S$, and a start with an RMS reprojection error of 34.1 pixels. With $\tau = 10^{-3}$:

| setting | steps tried | accepted | CG iterations in all | final RMS (pixels) |
|---|---|---|---|---|
| $\eta = 10^{-10}$, no cap | 13 | 12 | 226 | $4.6 \cdot 10^{-13}$ |
| $\eta = 0.1$, no cap | 13 | 12 | 68 | $7.9 \cdot 10^{-12}$ |
| $\eta = 0.5$, at most 3 per step | 42 | 41 | 97 | $7.5 \cdot 10^{-11}$ |

With $\eta = 10^{-10}$ the costs agree with the exact solve of sparse bundle adjustment to the printed digits ($1.240 \cdot 10^{2}$, $1.739 \cdot 10^{1}$, $3.41$ after the first three steps), and CG uses up to 18 iterations, the size of $S$. With $\eta = 0.1$ the costs after the first three steps are $1.201 \cdot 10^{2}$, $1.551 \cdot 10^{1}$ and $3.28$: almost the same progress for a third of the CG work. The CG count per step grows from 2 near the start to 8 near the end, because the right side becomes small and the same relative accuracy needs more iterations. With a loose $\eta = 0.5$ and a cap of 3, the method still converges and every accepted step lowers the cost, but it needs three times as many outer steps, each with a full rebuild of the blocks. On the first reduced system, block Jacobi preconditioning reaches a relative residual of $10^{-3}$ in 4 CG iterations and $10^{-6}$ in 9, against 9 and 15 without a preconditioner. These numbers are measurements on this small scene; on large scenes the counts and the trade-offs differ.

## Correctness

The implicit product equals $S x$, and $S$ and the block Jacobi preconditioner are symmetric positive definite for $\mu > 0$ (theorem). With the exact back-substitution, the full step is the minimizer of the damped model over $\delta_b$ for the given $\delta_a$, so the damped model equals a quadratic $q(\delta_a)$ in the cameras; CG from $0$ never increases $q$, and so the damped model at the step is at most $q(0) \le 0$, and below it when $g \ne 0$. It follows that the predicted reduction is at least $\tfrac12 \mu \|\delta\|^2 > 0$ for any number of CG iterations, that accepted steps lower $F$ strictly, and that a non-stationary point is left after finitely many rejections (theorems). The forcing parameter $\eta$ only affects the speed. For Newton's method on systems of equations, Dembo, Eisenstat and Steihaug proved local linear convergence for a relative residual bounded by a constant below 1, and superlinear convergence when it tends to 0 (theorem, for that setting). The proof file below gives the details.

## Complexity

In the real RAM model, with $m \ge n$ and $m \ge N$ (every point and camera is observed): building the blocks costs $O(m)$, line L5 costs $O(m)$, and line L6 costs $O(m + N)$ for the products and the $N$ inversions of $6 \times 6$ blocks. One product with $S$ costs $O(m + N)$, and one preconditioner application $O(N)$. So one outer step with $k$ CG iterations costs $O((k + 1)(m + N))$, written $O(k (m + N))$ for $k \ge 1$. The memory is $O(m + n + N)$: the blocks $W_{ij}$, $V_j$, $U_i$ and a few vectors. Nothing of size $N^2$ is stored. Sparse bundle adjustment needs $O(m + \sum_j c_j^2 + N^3)$ time and $O(N^2)$ memory per step instead. In exact arithmetic CG needs at most $6N$ iterations, but the point of the method is to stop much earlier; the count depends on the conditioning of the preconditioned $S$, which in turn depends on the scene.

## Properties

- **Matrix free.** Only products with $S$ are needed; $S$ is never formed.
- **Safe at any accuracy (theorem).** Any number of CG iterations gives a step with positive predicted reduction, as long as the points are back-substituted exactly.
- **Monotone (theorem).** Accepted costs decrease strictly.
- **Slower final convergence.** With a fixed $\eta$ the last steps are only as accurate as $\eta$ allows; to get a fast final rate, $\eta$ must go to $0$.
- **Parallel.** The products and the preconditioner are sums over observations and points, and parallelize well.

## Variants and improvements

- **Explicit Schur complement.** Form $S$ as a sparse matrix and run CG on it. This saves work per iteration when $S$ is sparse, at the price of storing it.
- **Other preconditioners.** Agarwal et al. compare several preconditioners, among them the block diagonal of $S$, which they call Schur-Jacobi and which is the one used here. Visibility based preconditioners group the cameras by the points they share, and [incomplete Cholesky](/incomplete-cholesky-factorization/) of $S$ is another option.
- **CG on the full system.** Byröd and Åström (2010) run preconditioned conjugate gradients on the least squares problem itself instead of on the reduced system.
- **Adaptive forcing.** Choose $\eta$ per step, for example smaller as the gradient shrinks, so that the final convergence is fast. The ideas come from the inexact Newton literature, such as the choices of Eisenstat and Walker.
- **Trust region version.** Run truncated CG inside a trust region, stopping when the iterate reaches the boundary, as in the Steihaug method; this fits [Powell's dog leg method](/powell-dogleg/) and other trust region frameworks.
- **Software.** The Ceres Solver library provides an iterative Schur solver of this kind, next to the direct sparse solvers.

## When to use it

Use it for bundle adjustment with many thousands of cameras, such as [global structure from motion](/global-structure-from-motion/) on large internet photo collections, where $S$ is too large to factor or its factor too dense. For up to a few thousand cameras, the exact solve of [sparse bundle adjustment](/sparse-bundle-adjustment/), with a sparse Cholesky factorization when $S$ is sparse, is usually faster and more robust, because it needs fewer outer steps and does not depend on the conditioning. For small windows in real time systems, such as [sliding window bundle adjustment](/sliding-window-bundle-adjustment/), a direct dense solve is simplest.

## Pitfalls

- **Using the exact pred formula.** $\tfrac12 \delta^{\mathsf T} (\mu \delta - g)$ assumes the damped system is solved exactly. With an inexact step it gives a wrong $\rho$. Compute $-g^{\mathsf T} \delta - \tfrac12 \|J \delta\|^2$.
- **Approximate back-substitution.** The safety argument needs the exact point steps of line L8. Computing them only roughly can give a step with a negative predicted reduction.
- **Poor conditioning.** Scenes with long camera chains, such as a street sequence, give an $S$ with a large condition number, and CG with block Jacobi needs many iterations. A stronger preconditioner helps.
- **Too strict a tolerance.** A tiny $\eta$ throws away the advantage: the example needs 226 CG iterations with $\eta = 10^{-10}$ against 68 with $\eta = 0.1$, for the same outer steps.
- **Too loose a tolerance.** A large $\eta$ or a small cap makes each step cheap but increases the number of outer steps, each of which rebuilds all blocks.
- **Gauge.** As in sparse bundle adjustment, the undamped $S$ is singular when the gauge is not fixed. CG with a small $\mu$ then works on a nearly singular matrix and converges slowly in the gauge directions.

## Implementations

## History

Triggs, McLauchlan, Hartley and Fitzgibbon (2000) described the reduced bundle system and the sparse direct methods to solve it. Inexact Newton methods with a forcing sequence were analyzed by Dembo, Eisenstat and Steihaug in 1982. Agarwal, Snavely, Seitz and Szeliski (2010) combined the two for reconstructions from community photo collections with thousands of cameras and millions of points: inexact Levenberg-Marquardt steps, CG on the reduced camera system with the Schur complement applied implicitly, and block preconditioners. In the same year Byröd and Åström studied preconditioned conjugate gradients for bundle adjustment. The iterative Schur approach became a standard solver in open source bundle adjustment software.

## References
