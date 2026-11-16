---
tag: BH2N89
kind: technique
slug: reduced-camera-system
name: Reduced camera system
aliases:
- Schur complement trick
- point elimination in bundle adjustment
area: computer-vision/structure-from-motion
level: core
summary: Eliminate the point blocks of the bundle adjustment normal equations by a Schur complement, leaving a smaller system in the camera parameters only.
prereqs: [bundle-adjustment, schur-complement]
see_also: [sparse-bundle-adjustment, inexact-newton-bundle-adjustment, gauge-freedom, cholesky-decomposition, fill-reducing-ordering, sliding-window-bundle-adjustment, domain-decomposition, gaussian-elimination]
sources:
  - paper: doi:10.1007/3-540-44480-7_21
    title: "Bill Triggs, Philip F. McLauchlan, Richard I. Hartley and Andrew W. Fitzgibbon, Bundle adjustment, a modern synthesis, in Vision Algorithms, Theory and Practice, Lecture Notes in Computer Science 1883, Springer, 2000, 298-372"
    locator: "Section 6.1, The Schur complement and the reduced bundle system, and the rest of Section 6 on the network structure and fill"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Appendix 6, Iterative estimation methods (the partitioned normal equations of sparse Levenberg-Marquardt and their solution by eliminating the point parameters)"
  - paper: doi:10.1145/1486525.1486527
    title: "Manolis I. A. Lourakis and Antonis A. Argyros, SBA: A software package for generic sparse bundle adjustment, ACM Transactions on Mathematical Software 36(1), 2009"
    locator: "the derivation of the reduced camera system from the block structure of the normal equations"
  - paper: doi:10.1007/978-3-642-15552-9_3
    title: "Sameer Agarwal, Noah Snavely, Steven M. Seitz and Richard Szeliski, Bundle adjustment in the large, Computer Vision ECCV 2010, Lecture Notes in Computer Science 6312, Springer, 2010, 29-42"
    locator: "the Schur complement section (the reduced camera system and its implicit and explicit use)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 11, Structure from motion and SLAM (bundle adjustment, exploiting sparsity)"
---

The reduced camera system is the linear system that remains when the point unknowns are eliminated from the normal equations of [bundle adjustment](/bundle-adjustment/). Each Gauss-Newton or Levenberg-Marquardt step of bundle adjustment solves
$$\begin{pmatrix} U & W \\ W^{\mathsf T} & V \end{pmatrix} \begin{pmatrix} \delta_a \\ \delta_b \end{pmatrix} = \begin{pmatrix} e_a \\ e_b \end{pmatrix},$$
where $\delta_a$ holds the camera updates, $\delta_b$ the point updates, $U$ is block diagonal with one block per camera, $V$ is block diagonal with one $3 \times 3$ block per point, and $W$ has a block $W_{ij}$ exactly where camera $i$ sees point $j$. Because $V$ is block diagonal it is cheap to invert, and block Gaussian elimination gives the [Schur complement](/schur-complement/) system
$$S \, \delta_a = e_a - W V^{-1} e_b, \qquad S = U - W V^{-1} W^{\mathsf T},$$
followed by $\delta_b = V^{-1} (e_b - W^{\mathsf T} \delta_a)$. The system in $S$ has only the camera unknowns, $6N$ for $N$ cameras with fixed intrinsics, against $6N + 3n$ for the full system with $n$ points, and $n$ is usually far larger than $N$. This is the core of [sparse bundle adjustment](/sparse-bundle-adjustment/), which factors $S$, and of [inexact Newton bundle adjustment](/inexact-newton-bundle-adjustment/), which solves it by conjugate gradients without forming it.

## In plain words

In bundle adjustment, every measurement ties one camera to one point, and no measurement ties two points together. So if the cameras were known, each point could be fixed on its own with a tiny 3 by 3 system. The trick turns this around. For each point, it works out how the best position of that point depends on the cameras that see it, and it substitutes that into the equations for the cameras. What is left is a system about the cameras only, which is much smaller. After solving it, each point is updated alone. Nothing is approximated: the answer is the same as solving the whole big system at once.

## When it applies

The trick applies to any symmetric positive definite system whose unknowns split into two groups, where the second group has a block diagonal (or otherwise cheap to factor) diagonal block. In bundle adjustment the two groups are the cameras and the points. The matrix is $J^{\mathsf T} J$ for Gauss-Newton, or $J^{\mathsf T} J + \mu I$ (or $+ \mu D$) for Levenberg-Marquardt, and the right side is $-J^{\mathsf T} r$. $V$ is block diagonal because each residual involves one point only. If $V$ (or the damped $V$) is positive definite, the elimination is exact and $S$ is positive definite too. It pays off when the eliminated group is the large one: $3n \gg 6N$.

## The template

```pseudo id=main
REDUCE-AND-SOLVE(U, V, W, e_a, e_b)
L1  for each point j: compute V_j^-1                         ▷ 3 x 3, independent
L2  S <- U ; r <- e_a
L3  for each point j, for each camera i that sees j: Y_ij <- W_ij V_j^-1 ; r_i <- r_i - Y_ij e_b,j
L4      for each camera k that sees j: S_ik <- S_ik - Y_ij W_kj^T
L5  solve S δa = r                                            ▷ dense or sparse Cholesky, or PCG
L6  for each point j: δb_j <- V_j^-1 (e_b,j - Σ_i W_ij^T δa_i)
L7  return δa, δb
```

Lines L1 to L4 build $S$ and the reduced right side point by point. Point $j$ contributes one $6 \times 6$ term to $S_{ik}$ for every pair of cameras $(i, k)$ that both see it, so $S_{ik}$ is nonzero only when cameras $i$ and $k$ share a point. Line L5 solves the reduced system. Line L6 recovers each point from the cameras that see it. With $c_j$ cameras seeing point $j$ and $m = \sum_j c_j$ observations, lines L1, L3 and L6 cost $O(n + m)$, line L4 costs $O(\sum_j c_j^2)$, and a dense Cholesky factorization in line L5 costs $O(N^3)$, against $O((6N + 3n)^3)$ for a dense solve of the full system.

**Why it is exact (theorem).** The second block row gives $\delta_b = V^{-1}(e_b - W^{\mathsf T} \delta_a)$. Substituting it into the first block row gives $(U - W V^{-1} W^{\mathsf T}) \delta_a = e_a - W V^{-1} e_b$. Conversely, any solution of the reduced system, with $\delta_b$ from line L6, solves the full system. If the full matrix $H$ is positive definite, then for $a \ne 0$ and $b = -V^{-1} W^{\mathsf T} a$ one gets $(a, b)^{\mathsf T} H (a, b) = a^{\mathsf T} S a > 0$, so $S$ is positive definite and its Cholesky factorization exists.

**What $S$ means (theorem).** The camera block of $H^{-1}$ is $S^{-1}$. When $H$ is the information matrix of a Gaussian estimate, $S$ is the information matrix of the cameras alone, with the points marginalized out; this is why the same operation is called marginalization in SLAM.

## Classic examples

**A small worked case.** Take two cameras and three points, each with one scalar unknown, with $U = \operatorname{diag}(5, 6)$, $V = \operatorname{diag}(2, 2, 1)$, camera 1 seeing points 1 and 2, camera 2 seeing points 2 and 3, all $W_{ij} = 1$, $e_a = (1, 2)$ and $e_b = (2, 2, 1)$. Then
$$W V^{-1} W^{\mathsf T} = \begin{pmatrix} 1 & 0.5 \\ 0.5 & 1.5 \end{pmatrix}, \quad S = \begin{pmatrix} 4 & -0.5 \\ -0.5 & 4.5 \end{pmatrix}, \quad r = e_a - W V^{-1} e_b = (-1, 0).$$
The off-diagonal $-0.5$ comes from point 2, the only point both cameras see. Solving gives $\delta_a = (-18/71, -2/71)$, and line L6 gives $\delta_b = (80/71, 81/71, 73/71)$. Substituting all five values into the original $5 \times 5$ system confirms every equation; for example the first row is $5 \cdot (-18/71) + 80/71 + 81/71 = 1$.

**Bundle adjustment.** With 6 parameters per camera and 3 per point, a scene of 100 cameras and 100000 points has a full system of order 300600, but $S$ has order 600. This is the step of [sparse bundle adjustment](/sparse-bundle-adjustment/).

**Large photo collections.** With tens of thousands of cameras, $S$ itself is too large to factor densely. [Inexact Newton bundle adjustment](/inexact-newton-bundle-adjustment/) applies $S$ to vectors as $U x - W (V^{-1} (W^{\mathsf T} x))$ and solves by preconditioned conjugate gradients.

**Marginalization in sliding windows.** In [sliding window bundle adjustment](/sliding-window-bundle-adjustment/) and visual-inertial odometry, old states leave the window by the same Schur complement, which keeps their information as a prior on the remaining states.

**Outside vision.** The same block elimination is static condensation in the [finite element method](/finite-element-method/) and the interface system of nonoverlapping [domain decomposition](/domain-decomposition/).

## Variations

- **Eliminate the cameras instead.** When there are far more cameras than points, which is rare, eliminate the camera blocks and solve for the points.
- **Sparse $S$.** When each camera shares points with only a few others, as in a long street sequence, $S$ is sparse, and a sparse Cholesky factorization with a [fill-reducing ordering](/fill-reducing-ordering/) is much cheaper than a dense one.
- **Implicit $S$.** Never form $S$; compute products with it, and solve iteratively.
- **Shared intrinsics.** Parameters that all cameras share, such as one focal length, add a dense border to $U$; they stay in the reduced system.
- **Points with extra structure.** Inverse depth points (1 parameter) or line features change only the size of the $V_j$ blocks.
- **Damping.** For Levenberg-Marquardt, add $\mu$ to both $U$ and $V$ before the elimination, so that the result is the exact damped step.

## Pitfalls

- **Singular point blocks.** A point seen by one camera has a rank 2 $V_j$ in Gauss-Newton, and a point with a tiny triangulation angle has a nearly singular one. Damp $V$, or remove such points, before line L1.
- **Damping only $S$.** Adding $\mu$ to $S$ after the elimination is not the Levenberg-Marquardt step. Damp $U$ and $V$ first.
- **Gauge.** Without fixed gauge parameters, $H$ and $S$ are singular in the undamped case; see [gauge freedom](/gauge-freedom/). Fix a camera and a scale, or keep $\mu > 0$.
- **Dense fill.** If one point is seen by all cameras, it alone makes $S$ dense. Many shared points in large scenes make $S$ dense even when $J$ is very sparse.
- **Assuming $S$ is small.** $S$ has order $6N$; with $N$ in the tens of thousands it does not fit in memory as a dense matrix.

## Exercises

1. Show that $S$ is positive definite when $H$ is, and that $\det H = \det V \cdot \det S$.
2. In the worked case, change $W_{22}$ from $1$ to $0$ (camera 2 no longer sees point 2). Show that $S$ becomes diagonal and explain why.
3. Count the nonzero $6 \times 6$ blocks of $S$ for $N$ cameras in a line, where each point is seen by two neighboring cameras only. What is the cost of a banded Cholesky factorization of $S$?
4. Prove that the camera block of $H^{-1}$ equals $S^{-1}$.
5. For a damped system with $\mu > 0$, show that eliminating the points and then solving gives the same step as the dense Levenberg-Marquardt solve, even when the undamped $V_j$ are singular.

## References
