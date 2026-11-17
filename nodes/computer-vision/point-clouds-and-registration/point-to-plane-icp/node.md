---
tag: FSJANG
kind: algorithm
slug: point-to-plane-icp
name: Point-to-plane ICP
aliases:
- Chen-Medioni ICP
area: computer-vision/point-clouds-and-registration
level: core
summary: "ICP that minimizes the squared distance from each moved source point to the tangent plane of its target match, by a Gauss-Newton step on a 6 by 6 linear system. Fast near the solution; local."
solves: [point-cloud-registration]
model: real-ram
complexity:
  vars: {n: the number of source points, m: the number of target points, N: the number of iterations}
  time: {worst: Θ(N n m), average: Θ(N n m), best: Θ(n m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1991
  people: [Yang Chen, Gérard Medioni]
  note: "Chen and Medioni registered range images by the distance to tangent planes at ICRA 1991, with the journal version in 1992. Low (2004) wrote the step as one linear least squares problem."
prereqs: [iterative-closest-point, gauss-newton-algorithm]
see_also: [point-cloud-normal-estimation, generalized-icp, nonlinear-least-squares, normal-equations, levenberg-marquardt, rodrigues-rotation-formula, icp-variants-taxonomy, point-cloud-registration]
sources:
  - paper: doi:10.1016/0262-8856(92)90066-C
    title: "Yang Chen and Gérard Medioni, Object modelling by registration of multiple range images, Image and Vision Computing 10(3), 1992, 145-155"
    locator: "The registration error as the distance from a point to the tangent plane of the other surface, the iterative least squares solution, and the pairs found along the surface normal"
  - url: https://www.cs.unc.edu/techreports/04-004.pdf
    title: "Kok-Lim Low, Linear least-squares optimization for point-to-plane ICP surface registration, Technical Report TR04-004, Department of Computer Science, University of North Carolina at Chapel Hill, 2004"
    locator: "The small-angle approximation of the rotation and the linear least squares problem in the six unknowns of the motion"
  - paper: doi:10.1007/s11263-006-5167-2
    title: "Helmut Pottmann, Qi-Xing Huang, Yong-Liang Yang and Shi-Min Hu, Geometry and convergence analysis of algorithms for registration of 3D shapes, International Journal of Computer Vision 67(3), 2006, 277-296"
    locator: "The convergence analysis: the tangent plane method as a Gauss-Newton iteration with quadratic convergence for a zero-residual problem from a good start, and the linear convergence of ICP"
  - paper: doi:10.1109/IM.2001.924423
    title: "Szymon Rusinkiewicz and Marc Levoy, Efficient variants of the ICP algorithm, Proceedings of the Third International Conference on 3-D Digital Imaging and Modeling (3DIM), 2001, 145-152"
    locator: "The comparison of the point-to-point and point-to-plane error metrics on synthetic meshes, where point-to-plane converges in fewer iterations"
  - paper: doi:10.1109/34.121791
    title: "Paul J. Besl and Neil D. McKay, A method for registration of 3-D shapes, IEEE Transactions on Pattern Analysis and Machine Intelligence 14(2), 1992, 239-256"
    locator: "The point-to-point ICP that this method changes in the error metric"
---

Point-to-plane ICP aligns a source [point cloud](/point-cloud/) $P$ to a target cloud $Q$ that has a unit normal at each point. It is [iterative closest point](/iterative-closest-point/) with another error: instead of the distance from a moved source point to its matched target point, it measures the distance to the tangent plane through the target point, $r_i = n_i \cdot (R p_i + t - q_i)$. Each iteration matches by closest point, then takes one Gauss-Newton step on $\sum_i r_i^2$: a small rotation $w$ and a translation $u$ from a $6 \times 6$ linear system, applied as an exact rigid motion. A point may slide along the target surface at no cost, so the method does not fight the sampling of the two clouds. Near the solution it converges much faster than point-to-point ICP, but it is still a local method and needs a good start.

## In plain words

Two scans of a surface never sample the same spots. Plain ICP pulls each point toward one sample of the other scan, even when the point already lies on the surface between two samples. That pull is wrong, and it slows ICP down.

Point-to-plane ICP measures only how far a point is off the surface, along the surface normal. Moving a point along the surface costs nothing. The error then depends on the motion in a nearly linear way. One small linear system with six unknowns, three for the turn and three for the slide, gives a good step. Near the answer, each step roughly squares the remaining error.

The method needs normals on the target. If the target is flat, sliding along it costs nothing in every direction of the plane, and the system has no unique answer.

## The problem

**Input.** A source cloud $P = (p_1, \ldots, p_n)$, a target cloud $Q = \{q_1, \ldots, q_m\}$ in $\mathbb{R}^3$, a unit normal $\nu_j$ for each $q_j$, a start pose $(R_0, t_0)$ with $R_0 \in SO(3)$, and a tolerance tol. The normals usually come from [normal estimation](/point-cloud-normal-estimation/); their sign does not matter, because the residual is squared.

**Output.** A pose $(R, t)$, $R \in SO(3)$, at which the point-to-plane cost

$$E_{\text{pl}}(R, t) = \sum_{i=1}^{n} \big(n_i \cdot (R p_i + t - y_i)\big)^2$$

is stationary for its closest-point match, where $y_i$ is the closest target point of $R p_i + t$ and $n_i$ its normal. As for ICP, the goal is a pose near the true one; the method does not promise a global minimum.

## The algorithm

Write $x_i = R p_i + t$ for the moved points. Turning by a small vector $w$ (the angle $|w|$ about the axis $w / |w|$) and moving by $u$ maps $x_i$ to $x_i + w \times x_i + u$ to first order, and $n_i \cdot (w \times x_i) = (x_i \times n_i) \cdot w$. So the residual becomes $r_i + a_i^{\mathsf T} z$ with $z = (w, u)$ and $a_i = (x_i \times n_i,\ n_i) \in \mathbb{R}^6$. The step minimizes $\sum_i (r_i + a_i^{\mathsf T} z)^2$, which by the [normal equations](/normal-equations/) is $A z = b$ with $A = \sum_i a_i a_i^{\mathsf T}$ and $b = -\sum_i r_i a_i$. This is one [Gauss-Newton](/gauss-newton-algorithm/) step for the residuals $r_i$ as functions of $z$.

```pseudo id=main
POINT-TO-PLANE-ICP(P, Q, ν, R0, t0, tol)
L1  R ← R0 ;  t ← t0
L2  repeat (up to an iteration cap)
L3      x_i ← R p_i + t ;  c(i) ← closest target index ;  y_i ← q_c(i) ;  n_i ← ν_c(i)
L4      r_i ← n_i · (x_i - y_i) ;  record Σ_i r_i²
L5      solve A z = b,  A = Σ a_i a_iᵀ,  b = -Σ r_i a_i,  a_i = (x_i × n_i, n_i),  z = (w, u)
L6      R ← Exp(w) R ;  t ← Exp(w) t + u
L7      if |z| ≤ tol then stop
L8  return R, t
```

Line L3 is the same closest-point step as in ICP; the code uses brute force, and a [k-d tree](/kd-tree/) is the usual choice. Line L5 builds the $6 \times 6$ symmetric matrix $A$ and solves it by Gaussian elimination. Line L6 applies the rotation $\operatorname{Exp}(w)$ of the vector $w$ by the [Rodrigues formula](/rodrigues-rotation-formula/), so $R$ stays a rotation; the new moved points are exactly $\operatorname{Exp}(w) x_i + u$. Line L7 stops when the step is tiny.

## Example

The target is a $15 \times 15$ grid on the surface $z = 0.3 \sin(2x) \cos(1.5y) + 0.1 x^2$ over $[-1, 1]^2$, with the exact normals, 225 points. The source is 60 of these points (chosen with seed 1), moved by the inverse of a rotation of 10 degrees about the axis $(1, 2, 3)$ and the translation $(0.05, -0.03, 0.04)$. The start pose is the identity. Coordinates are unitless.

| iteration | point-to-plane cost after L4 |
|---|---|
| 1 | 0.458 |
| 2 | 0.00139 |
| 3 | 1.01e-7 |
| 4 | 1.87e-17 |
| 5 | 9.41e-32 |

The final rotation differs from the true one by $6 \times 10^{-17}$ radians, which is rounding error. The square roots of the costs are 0.68, 0.037, 3.2e-4, 4.3e-9 and 9.7e-16: each one is about a constant times the square of the one before, the mark of quadratic convergence.

Point-to-point ICP on the same scene, from the same start, behaves differently. Its mean squared error falls from 0.0122 to 0.00342 in 10 fit steps, and then it stops at a fixed point that is 4.26 degrees off. Point-to-point ICP pulls each point to one target sample, and on this scene the pulls toward wrong samples balance at the wrong pose. Point-to-plane ICP lets a point slide along the surface, so these pulls do not occur.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows four facts. The change of the residual under the motion $x \mapsto \operatorname{Exp}(w) x + u$ is $a_i^{\mathsf T} z$ plus a remainder of at most $\frac12 |w|^2 |x_i|$. Line L5 returns the unique minimizer of the linearized cost when $A$ is nonsingular, and no unique minimizer exists when $A$ is singular. Line L6 keeps $R$ a rotation. A zero step means that the fixed-match cost is stationary, and the true pose of an exact copy gives zero residuals and a zero step, so it is a fixed point. The proof does not show a decrease in every iteration: a full Gauss-Newton step can overshoot.

Pottmann, Huang, Yang and Hu (2006) show that the tangent plane method is a Gauss-Newton method on the squared distance function of the target surface and, for a zero-residual problem with a good start, converges quadratically. Point-to-point ICP converges only linearly. The page cites these results and does not prove them.

## Complexity

The model is the [real RAM](/real-ram/). Per iteration, line L3 costs $\Theta(n m)$ by brute force. Line L4 is $\Theta(n)$. Line L5 adds $n$ outer products of 6-vectors, $\Theta(n)$, and solves a $6 \times 6$ system in $O(1)$ time. Line L6 is $O(1)$. So one iteration is $\Theta(n m)$, and $N$ iterations cost $\Theta(N n m)$; the best case is one iteration with a zero step, $\Theta(n m)$. With a k-d tree on $Q$, line L3 drops to about $n \log m$ on typical 3D data (an expected cost, not a worst case). The extra space holds the moved points, the match and the $6 \times 6$ system, $\Theta(n)$.

The number of iterations $N$ has no useful worst-case bound. The local rate is quadratic for zero residual (Pottmann et al. 2006). The measured gap to point-to-point ICP depends on the data; Rusinkiewicz and Levoy (2001) report fewer iterations for point-to-plane on their test meshes, which is a benchmark result.

## Properties

- **Gauss-Newton.** Each iteration is one Gauss-Newton step on the fixed-match residuals, with an exact rotation update.
- **Fast local rate.** Quadratic near a zero-residual solution from a good start, against linear for point-to-point ICP.
- **Not monotone.** Without a line search, the cost can rise in an iteration far from the solution.
- **Local.** Like all ICP forms, the result depends on the start pose.
- **Needs normals.** Normals on the target only; the source needs none.
- **Degenerate geometry.** If the target is a plane, a cylinder or another surface that can slide on itself, $A$ is singular or nearly singular.

## Variants and improvements

- **Symmetric error.** Using the normals of both clouds, as in the symmetric objective of Rusinkiewicz (2019), widens the region of fast convergence.
- **Plane-to-plane.** [Generalized ICP](/generalized-icp/) puts a flat covariance on each point of both clouds; point-to-plane is a limit case of it.
- **Damping.** Adding $\lambda I$ to $A$ gives a [Levenberg-Marquardt](/levenberg-marquardt/) step, which handles near-singular $A$ and large first steps.
- **Robust weights.** Weights $w_i$ on the residuals, from an [M-estimator](/m-estimator/), turn the step into [iteratively reweighted least squares](/iteratively-reweighted-least-squares/).
- **Normal-space sampling.** Rusinkiewicz and Levoy choose source points so that the normals spread over all directions, which keeps $A$ well conditioned; see [efficient variants of ICP](/icp-variants-taxonomy/).

## When to use it

Use point-to-plane ICP for smooth surfaces sampled by depth cameras, laser scanners or [stereo](/stereo-matching/), when normals are cheap to get and a rough pose is known. KinectFusion (Newcombe et al. 2011), for example, tracks its depth camera with point-to-plane ICP. Use point-to-point [ICP](/iterative-closest-point/) when normals are unreliable, for example on sparse or very noisy clouds, or when the clouds have no surface. Use [generalized ICP](/generalized-icp/) when both clouds are surfaces and you want a symmetric, probabilistic error. For partial overlap, add a distance threshold or [trimming](/trimmed-icp/).

## Pitfalls

- **Line L6 with $t \leftarrow t + u$.** The step turns all moved points about the origin, so the translation must turn too: $t \leftarrow \operatorname{Exp}(w)\, t + u$. With $t + u$ the pose drifts whenever $t \ne 0$.
- **Line L6 with $R \leftarrow (I + [w]_\times) R$.** The first-order matrix is not a rotation, and the error grows over the iterations. Use $\operatorname{Exp}(w)$, or orthogonalize the result.
- **A singular system in line L5.** A planar target lets the source slide in two directions and turn about the normal, so $A$ has rank 3. Check the rank or the smallest eigenvalue of $A$, sample points with varied normals, or add damping.
- **Bad normals in line L3.** Normals from a neighborhood that crosses an edge or two sheets of the surface point the wrong way. The residuals are then wrong, not only noisy. Use a neighborhood size that fits the sampling.
- **A far start.** The fast rate is local. From a far start the step can overshoot; bound the step or add a line search.

## Implementations

## History

Chen and Medioni presented the method at ICRA in 1991 and in Image and Vision Computing in 1992, for building object models from several range images. They paired a point with the place where the line along its normal meets the other surface, and minimized the distances to the tangent planes there. The closest-point pairing, shared with Besl and McKay's ICP of 1992, became the common form later. Low (2004) wrote the small-angle step as one linear least squares problem in six unknowns. Pottmann, Huang, Yang and Hu (2006) explained the fast convergence: the method is a Gauss-Newton iteration on the squared distance function of the target.

## References
