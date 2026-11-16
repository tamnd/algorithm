---
tag: C231EB
kind: algorithm
slug: sparse-bundle-adjustment
name: Sparse bundle adjustment
aliases:
- SBA
- Lourakis-Argyros bundle adjustment
area: computer-vision/structure-from-motion
level: advanced
summary: Levenberg-Marquardt for bundle adjustment that eliminates the points by the reduced camera system, so a step costs O(N^3) in the N cameras and only linear time in the points.
solves: [bundle-adjustment]
model: real-ram
complexity:
  vars: {N: "the number of cameras", n: "the number of points", m: "the number of observations"}
  time: {per_iteration: "O(m + n N^2 + N^3)"}
  space: {extra: "O(m + N^2)"}
properties: {deterministic: true, iterative: true, local: true, recursive: false, monotone: true}
history:
  year: 1958
  people: [Duane C. Brown, Manolis I. A. Lourakis, Antonis A. Argyros]
  note: Photogrammetrists, starting with Brown in the late 1950s, solved the bundle normal equations by eliminating the points first. Lourakis and Argyros released the SBA package, which made sparse Levenberg-Marquardt the standard in vision.
prereqs: [bundle-adjustment, levenberg-marquardt, reduced-camera-system]
see_also: [inexact-newton-bundle-adjustment, gauge-freedom, powell-dogleg, schur-complement, cholesky-decomposition, incremental-structure-from-motion, sliding-window-bundle-adjustment, reprojection-error]
sources:
  - paper: doi:10.1145/1486525.1486527
    title: "Manolis I. A. Lourakis and Antonis A. Argyros, SBA: A software package for generic sparse bundle adjustment, ACM Transactions on Mathematical Software 36(1), 2009"
    locator: "the whole paper (the sparse Levenberg-Marquardt algorithm, the block structure of the normal equations, the Schur complement and the software)"
  - paper: doi:10.1007/3-540-44480-7_21
    title: "Bill Triggs, Philip F. McLauchlan, Richard I. Hartley and Andrew W. Fitzgibbon, Bundle adjustment, a modern synthesis, in Vision Algorithms, Theory and Practice, Lecture Notes in Computer Science 1883, Springer, 2000, 298-372"
    locator: "Section 6, Network structure and implementation (Section 6.1, the Schur complement and the reduced bundle system), and the historical appendix"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Appendix 6, Iterative estimation methods (sparse Levenberg-Marquardt, its application to bundle adjustment and the sparse methods for solving the equations); Chapter 18, N-view computational methods (bundle adjustment)"
  - paper: doi:10.1109/ICCV.2005.128
    title: "Manolis I. A. Lourakis and Antonis A. Argyros, Is Levenberg-Marquardt the most efficient optimization algorithm for implementing bundle adjustment?, Tenth IEEE International Conference on Computer Vision (ICCV 2005), vol. 2, 1526-1531"
    locator: "the whole paper (the sparse dog leg alternative and the timing comparison)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 11, Structure from motion and SLAM (bundle adjustment and exploiting sparsity)"
---

Sparse bundle adjustment (SBA) is [Levenberg-Marquardt](/levenberg-marquardt/) applied to [bundle adjustment](/bundle-adjustment/), with each damped linear system solved in a way that uses the sparsity of the problem. In bundle adjustment each residual depends on one camera and one point only, so the Gauss-Newton matrix $J^{\mathsf T} J$ has a block diagonal camera part $U$, a block diagonal point part $V$ with $3 \times 3$ blocks, and a coupling part $W$ that is nonzero only where a camera sees a point. SBA builds these blocks from the small per-observation Jacobians, eliminates all the points at once with the [Schur complement](/schur-complement/) $S = U^* - W V^{*-1} W^{\mathsf T}$, solves the [reduced camera system](/reduced-camera-system/) in $S$ by a [Cholesky factorization](/cholesky-decomposition/), and recovers the point updates one by one. The step is exactly the Levenberg-Marquardt step, but its cost drops from cubic in all the parameters to cubic in the cameras plus linear in the points. Among the close pages, bundle adjustment is the problem, the reduced camera system is the elimination technique on its own, [inexact Newton bundle adjustment](/inexact-newton-bundle-adjustment/) solves $S$ approximately by conjugate gradients when $N$ is too large to factor, and [gauge freedom](/gauge-freedom/) explains why the undamped matrix is singular.

## In plain words

Bundle adjustment fixes many cameras and many 3D points together so that every point lands where it was seen in every photo. Written as one big system of equations, this is huge, but most of it is empty: each measurement links only one camera to one point. If you knew the cameras, each point could be fixed alone with a tiny 3 by 3 system. SBA uses this. It first writes, for every point, how its best position depends on the cameras, and folds that into one system about the cameras only. That system is small when there are few cameras. After solving it, each point is updated alone. Around this sits the usual Levenberg-Marquardt brake that keeps every accepted step an improvement.

## The problem

**Input.** A shared intrinsic matrix $K = \begin{pmatrix} f_x & s & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{pmatrix}$, start values for $N$ cameras $(R_i, t_i)$ and $n$ points $X_j$, and $m$ observations $(i, j, x_{ij})$: point $j$ seen at pixel $x_{ij}$ in camera $i$. A set of fixed cameras, usually camera 0, a damping factor $\tau$ and stopping limits. The camera frame has $X$ right, $Y$ down and $Z$ forward, $X_c = R_i X_j + t_i$, and pixel centers are at integer coordinates.

**Output.** Cameras and points at a local minimizer of the reprojection cost $F = \tfrac12 \sum_{(i, j)} \|\pi(K (R_i X_j + t_i)) - x_{ij}\|^2$, with $F$ no larger than at the start. With isotropic Gaussian pixel noise this is the maximum likelihood estimate.

**Parameters.** A free camera has 6: a rotation vector $\omega_i$ applied on the left, $R_i \leftarrow \exp([\omega_i]_\times) R_i$, and a translation step. A point has 3. The Jacobian of the residual $r_{ij}$ has two nonzero blocks: $A_{ij}$ ($2 \times 6$) for camera $i$ and $B_{ij}$ ($2 \times 3$) for point $j$.

## The algorithm

```pseudo id=main
SPARSE-BA(K, cameras, points, observations, τ, ε_1, ε_2, k_max)
L1  ν <- 2 ; for each observation (i, j): A_ij, B_ij, r_ij; U_i += A^T A ; V_j += B^T B ; W_ij <- A^T B ; g_a,i += A^T r ; g_b,j += B^T r
L2  μ <- τ · max diagonal entry of U and V
L3  for k <- 1 to k_max
L4      if ||g||_∞ <= ε_1 then return
L5      U*_i <- U_i + μ I ; V*_j <- V_j + μ I ; e_i <- -g_a,i
L6      for each point j, for each pair of cameras i, k that see j: S_ik -= W_ij V*_j^-1 W_kj^T ; e_i += W_ij V*_j^-1 g_b,j     ▷ S_ii starts at U*_i
L7      solve S δa = e by Cholesky
L8      for each point j: δb_j <- -V*_j^-1 (g_b,j + Σ_i W_ij^T δa_i)
L9      if ||δ|| <= ε_2 (||x|| + ε_2) then return
L10     ρ <- (F(x) - F(x ⊕ δ)) / (½ δ^T (μ δ - g))
L11     if ρ > 0 then x <- x ⊕ δ ; rebuild the blocks as in L1 ; μ <- μ · max(1/3, 1 - (2ρ - 1)^3) ; ν <- 2
L12     else μ <- μ ν ; ν <- 2 ν
L13 return cameras, points
```

Line L1 computes, for each observation, the residual and the two Jacobian blocks: with $D = \partial \pi / \partial X_c$, $A_{ij} = D\,(-[R_i X_j]_\times \;\; I)$ and $B_{ij} = D R_i$. It accumulates the blocks of $J^{\mathsf T} J$ and of the gradient $g = J^{\mathsf T} r$; nothing of size $m \times (6N + 3n)$ is ever stored. Lines L2, L4 and L9 to L12 are the Levenberg-Marquardt loop of Madsen, Nielsen and Tingleff. Lines L5 to L8 solve the damped system $(J^{\mathsf T} J + \mu I) \delta = -g$: line L6 forms the reduced camera matrix point by point, line L7 factors it, and line L8 back-substitutes the points, each with its own $3 \times 3$ inverse. The update $x \oplus \delta$ applies the rotation steps on the left and adds the other steps.

## Example

The reference test uses 4 cameras looking at 20 points in a cube of side 2 from a distance of about 5, with $f_x = f_y = 800$ and $(c_x, c_y) = (320, 240)$. Every camera sees every point, so $m = 80$ and there are 160 residuals. Camera 0 is fixed, so the unknowns are $3 \cdot 6 = 18$ camera parameters and $20 \cdot 3 = 60$ point parameters. A dense Levenberg-Marquardt step would factor a $78 \times 78$ matrix; SBA factors the $18 \times 18$ matrix $S$ and inverts twenty $3 \times 3$ blocks. The start perturbs the true rotations by about $0.02$ rad, the translations by about $0.05$ and the points by about $0.05$, which gives an RMS reprojection error of 34.1 pixels. With $\tau = 10^{-3}$:

| accepted step | $F$ | RMS error (pixels) |
|---|---|---|
| 0 | $4.660 \cdot 10^{4}$ | $34.1$ |
| 1 | $1.240 \cdot 10^{2}$ | $1.76$ |
| 2 | $1.739 \cdot 10^{1}$ | $0.659$ |
| 4 | $2.950 \cdot 10^{-1}$ | $0.0859$ |
| 6 | $5.877 \cdot 10^{-5}$ | $1.21 \cdot 10^{-3}$ |
| 8 | $5.141 \cdot 10^{-8}$ | $3.59 \cdot 10^{-5}$ |
| 10 | $4.941 \cdot 10^{-14}$ | $3.52 \cdot 10^{-8}$ |
| 12 | $8.518 \cdot 10^{-24}$ | $4.62 \cdot 10^{-13}$ |

The run tries 13 steps and accepts 12. The data are exact, so the cost reaches rounding level, and the last steps show the fast local rate of Gauss-Newton on a zero residual problem. The result equals the true scene up to the one gauge freedom left, a common scale, here $s = 0.99695$; after dividing it out, all cameras and points agree with the truth to better than $10^{-6}$. With 1 pixel of Gaussian noise on the same kind of scene, the final cost is $52.9$, below the cost $95.4$ of the true scene, as it must be for a minimizer. These figures are measurements on these test scenes.

## Correctness

The blocks of line L1 are the exact derivatives of the residuals with respect to the local update (theorem). For $\mu > 0$, the damped matrix is positive definite, so its Schur complement $S$ is positive definite and line L7 succeeds (theorem). Lines L6 to L8 return the unique solution of the full damped system, by block elimination (theorem). So SBA computes the same step as dense Levenberg-Marquardt and inherits its properties: the predicted reduction is positive, accepted steps lower the cost strictly, and a non-stationary point is left after finitely many rejections (theorems). The proof file below gives the details. The global convergence result of Moré (1978) for trust region Levenberg-Marquardt applies to the same steps.

## Complexity

In the real RAM model, let $c_j$ be the number of cameras that see point $j$, so $m = \sum_j c_j$. Line L1 costs $O(m)$, since each observation does a constant amount of work. Line L6 costs $O(\sum_j c_j^2)$: one $6 \times 6$ product for each pair of cameras that share a point. Line L7 is a dense Cholesky factorization of the $6N \times 6N$ matrix, $O(N^3)$. Line L8 costs $O(m)$. So one step costs $O(m + \sum_j c_j^2 + N^3)$, which is at most $O(m + n N^2 + N^3)$ since $c_j \le N$. A dense factorization of the whole system would cost $\Theta((6N + 3n)^3)$. The extra space is $O(m)$ for the blocks $W_{ij}$ and $O(N^2)$ for $S$. When each camera sees only a few others, $S$ is itself sparse, and a sparse Cholesky factorization with a [fill-reducing ordering](/fill-reducing-ordering/) costs much less than $N^3$. When $N$ is in the thousands, even that is too much, and [inexact Newton bundle adjustment](/inexact-newton-bundle-adjustment/) is used instead.

## Properties

- **Exact step (theorem).** The step equals the dense Levenberg-Marquardt step; only the cost differs.
- **Monotone (theorem).** The accepted costs decrease strictly.
- **Points never coupled directly.** $V$ is block diagonal because no residual involves two points, which is what makes the elimination cheap. A residual that links two points, such as a distance constraint, breaks this.
- **Gauge.** With one camera fixed, the scale is still free, so $J^{\mathsf T} J$ is singular. The damping keeps $S$ positive definite for $\mu > 0$, and the iterates may drift slowly along the scale direction.
- **The camera model can change.** Shared or per-camera intrinsics, distortion terms and other camera parameters only change the size of the camera blocks.

## Variants and improvements

- **Sparse dog leg.** Lourakis and Argyros (2005) use the same block solve inside [Powell's dog leg method](/powell-dogleg/), which reuses the Gauss-Newton step after a rejection; they report shorter run times on their tests (a benchmark result).
- **Sparse Cholesky of $S$.** When the camera graph is sparse, order $S$ with [nested dissection](/nested-dissection/) or [minimum degree](/minimum-degree-ordering/) and factor it as a sparse matrix.
- **Iterative solve of $S$.** Use the [conjugate gradient method](/conjugate-gradient-method/) with a block Jacobi preconditioner, without forming $S$; see [inexact Newton bundle adjustment](/inexact-newton-bundle-adjustment/).
- **Eliminating the cameras instead.** When there are many more cameras than points, which is rare in vision, eliminate the cameras and solve for the points.
- **Robust costs.** Weight each observation by an [M-estimator](/m-estimator/) weight; the block structure does not change.
- **Local and windowed versions.** Optimize only the latest cameras and the points they see, as in [sliding window bundle adjustment](/sliding-window-bundle-adjustment/) and local bundle adjustment in SLAM systems such as [ORB-SLAM](/orb-slam/).

## When to use it

Use SBA for bundle adjustment with up to a few thousand cameras, which covers most offline reconstructions of single objects and buildings and most incremental SfM steps. It gives the exact damped step at a cost dominated by the factorization of $S$. When $N$ reaches tens of thousands, or when $S$ is dense because many cameras see the same points, switch to inexact Newton bundle adjustment. For a fixed scene with known cameras, refine each point alone by [optimal triangulation](/optimal-triangulation/); for known points, refine each camera alone by [PnP](/perspective-n-point/) refinement.

## Pitfalls

- **Forgetting to damp $V$.** In line L5 both $U$ and $V$ get $\mu I$. Damping only $U$ gives a different, non-Levenberg-Marquardt step, and a point seen by one camera has a singular $V_j$.
- **Points with too few views.** A point seen by one camera has a rank 2 $V_j$, which only the damping makes invertible. Remove such points, or points with a tiny triangulation angle, before the run.
- **Wrong rotation derivative.** The block $-[R_i X_j]_\times$ in line L1 belongs to the left update $\exp([\omega]_\times) R$. With a right update $R \exp([\omega]_\times)$ the block is $-R [X_j]_\times$. Mixing them gives a wrong Jacobian, which a finite difference test catches.
- **Points behind a camera.** A step can move a point to $z \le 0$, where $\pi$ is not defined. Reject such steps as failed steps.
- **No gauge fix.** Without a fixed camera, $S$ has a 7-dimensional near null space when $\mu$ is small, and Cholesky can fail in floating point. The reference code then raises $\mu$; fixing camera 0 and possibly one scale parameter avoids it.

## Implementations

## History

Bundle adjustment comes from photogrammetry. Duane Brown worked out the method for aerial and close range photogrammetry in the late 1950s, and the photogrammetric literature already reduced the normal equations to the camera parameters by eliminating the points, as Triggs, McLauchlan, Hartley and Fitzgibbon (2000) recount in their historical appendix. Their survey brought this structure to computer vision, together with gauge theory and sparse factorization. Hartley and Zisserman (2000, second edition 2004) presented sparse Levenberg-Marquardt as the standard bundle method. Lourakis and Argyros released the SBA package in 2004 and described it in ACM Transactions on Mathematical Software in 2009. It was used in early large reconstruction systems such as Bundler, before solvers with iterative linear algebra took over the largest problems.

## References
