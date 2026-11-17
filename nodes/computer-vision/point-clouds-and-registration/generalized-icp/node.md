---
tag: W2QK6S
kind: algorithm
slug: generalized-icp
name: Generalized ICP
aliases:
- GICP
- plane-to-plane ICP
area: computer-vision/point-clouds-and-registration
level: advanced
summary: "ICP whose fit step weights each pair by the inverse of the summed covariances of both points, a maximum likelihood cost that contains point-to-point and, as a limit, point-to-plane ICP."
solves: [point-cloud-registration]
model: real-ram
complexity:
  vars: {n: the number of source points, m: the number of target points, N: the number of outer iterations, S: the cap on inner Gauss-Newton steps}
  time: {worst: "O(n^2 log n + m^2 log m + N n (m + S))", average: "O(n^2 log n + m^2 log m + N n (m + S))", best: "Θ(n^2 log n + m^2 log m + n m)"}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2009
  people: [Aleksandr Segal, Dirk Haehnel, Sebastian Thrun]
  note: "Segal, Haehnel and Thrun presented Generalized-ICP at Robotics: Science and Systems 2009, as a probabilistic model of the fit step with plane-to-plane covariances."
prereqs: [iterative-closest-point, point-to-plane-icp, maximum-likelihood-estimation]
see_also: [covariance-matrix, point-cloud-normal-estimation, normal-distributions-transform, gauss-newton-algorithm, conjugate-gradient-method, principal-component-analysis, trimmed-icp, point-cloud-registration]
sources:
  - paper: doi:10.15607/RSS.2009.V.021
    title: "Aleksandr Segal, Dirk Haehnel and Sebastian Thrun, Generalized-ICP, Robotics: Science and Systems V (RSS 2009)"
    locator: "The probabilistic derivation of the cost (Eq. 2), its point-to-point and point-to-plane special cases, the plane-to-plane covariances from the 20 nearest neighbors with a small variance along the normal, the distance threshold d_max, and the minimization by conjugate gradients"
  - paper: doi:10.1109/34.121791
    title: "Paul J. Besl and Neil D. McKay, A method for registration of 3-D shapes, IEEE Transactions on Pattern Analysis and Machine Intelligence 14(2), 1992, 239-256"
    locator: "The point-to-point ICP that GICP contains as the case of zero source covariance and identity target covariance"
  - paper: doi:10.1016/0262-8856(92)90066-C
    title: "Yang Chen and Gérard Medioni, Object modelling by registration of multiple range images, Image and Vision Computing 10(3), 1992, 145-155"
    locator: "The point-to-plane error that GICP contains as a limit case"
  - book: isbn:9780387303031
    title: "Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006"
    locator: "Chapter 10, Least-squares problems (the Gauss-Newton method), and Chapter 3, Line search methods (backtracking)"
---

Generalized ICP (GICP) aligns a source [point cloud](/point-cloud/) $A$ to a target cloud $B$ like [iterative closest point](/iterative-closest-point/), but it gives every point a $3 \times 3$ covariance that describes how sure its position is in each direction. With the pairs fixed, it chooses the motion $(R, t)$ that minimizes $\sum_i d_i^{\mathsf T} (C^B_j + R C^A_i R^{\mathsf T})^{-1} d_i$ with $d_i = b_j - (R a_i + t)$, which is the [maximum likelihood](/maximum-likelihood-estimation/) motion when both points are Gaussian. With zero source covariances and identity target covariances this is point-to-point ICP, and with flat target covariances it tends to [point-to-plane ICP](/point-to-plane-icp/). The usual plane-to-plane form makes every covariance flat: small along the surface normal of the point and large along its tangent plane, on both clouds. Like ICP, GICP is local and needs a good start.

## In plain words

A laser point on a wall is known well in the direction across the wall, and poorly along the wall, because the wall looks the same there. GICP writes this as a small ellipsoid for every point: thin across the surface, wide along it.

When two points are paired, their ellipsoids are added. The gap between the points is then measured in units of this combined ellipsoid. A gap along both surfaces costs little. A gap across them costs a lot.

Every gap counts according to how sure both scans are. Plain ICP treats every direction the same. Point-to-plane ICP trusts only the target surface. GICP uses both surfaces, so the result does not depend much on which scan you call the source.

## The problem

**Input.** Source points $a_1, \ldots, a_n$ with symmetric positive semidefinite covariances $C^A_i$, target points $b_1, \ldots, b_m$ with symmetric positive definite covariances $C^B_j$, a start pose $(R_0, t_0)$, an optional distance threshold $d_{\max}$, and a tolerance tol.

**Output.** A pose $(R, t)$ with $R \in SO(3)$ at which the GICP cost of the current closest-point pairs is small. For a set $\Pi$ of pairs $(i, j)$ the cost is

$$G(R, t) = \sum_{(i, j) \in \Pi} d_{ij}^{\mathsf T} \big(C^B_j + R C^A_i R^{\mathsf T}\big)^{-1} d_{ij}, \qquad d_{ij} = b_j - (R a_i + t).$$

If $a_i$ is Gaussian with covariance $C^A_i$ and $b_j$ is Gaussian with covariance $C^B_j$ around positions that the true motion maps onto each other, then $d_{ij}$ is Gaussian with mean 0 and covariance $C^B_j + R C^A_i R^{\mathsf T}$ at the true motion. Minimizing $G$ maximizes the likelihood of the $d_{ij}$, with the normalizing factor of each Gaussian density taken as a constant, as in the paper.

## The algorithm

The plane-to-plane covariances come first. For each point, take the covariance of its $k$ nearest neighbors, write it as $V \operatorname{diag}(\lambda_1, \lambda_2, \lambda_3) V^{\mathsf T}$ with $\lambda_1 \le \lambda_2 \le \lambda_3$, and replace the eigenvalues by $(\varepsilon, 1, 1)$. The first column of $V$ is then the estimated normal (the [principal component](/principal-component-analysis/) of least spread). The paper uses the 20 nearest neighbors and a small $\varepsilon$ without a number; the reference code uses $k = 10$ and $\varepsilon = 10^{-3}$.

The main loop holds the weights fixed during each fit. On the motion $x \mapsto \operatorname{Exp}(w) x + u$ of the moved points $x_i = R a_i + t$, the residual changes to $d_{ij} + J_i (w, u)$ to first order, with $J_i = [\,[x_i]_\times \;\; -I\,]$, where $[x]_\times$ is the skew matrix of the cross product.

```pseudo id=main
GENERALIZED-ICP(A, B, C^A, C^B, R0, t0, d_max, tol)
L1  R ← R0 ;  t ← t0
L2  repeat (up to N iterations)
L3      Π ← {(i, j) : b_j closest to R a_i + t, and |R a_i + t - b_j| ≤ d_max}
L4      M_ij ← (C^B_j + R C^A_i Rᵀ)⁻¹  for (i, j) in Π       ▷ held fixed below
L5      (R', t') ← minimize G with the weights M_ij fixed, from (R, t), by steps L6 and L7
L6          solve H δ = -g,  g = Σ J_iᵀ M_ij d_ij,  H = Σ J_iᵀ M_ij J_i,  δ = (w, u)
L7          λ ← 1 ; halve λ until G(Exp(λw) R, Exp(λw) t + λu) < G(R, t), then accept
L8      if |R' - R| + |t' - t| ≤ tol then (R, t) ← (R', t') and stop ;  (R, t) ← (R', t')
L9  return R, t
```

Line L3 is the closest-point match of ICP, with the threshold of the paper that drops pairs farther than $d_{\max}$. Line L4 computes the weights from the rotation at the start of the iteration. Line L5 is the inner minimization: [Gauss-Newton](/gauss-newton-algorithm/) steps (line L6) with step halving (line L7), up to $S$ steps, until a step is tiny or no halved step lowers $G$. The paper minimizes the cost with conjugate gradients and lets the weights change with $R$ during the minimization; the reference code freezes the weights in each outer iteration and uses Gauss-Newton, which gives a clean descent proof for the inner step. Line L8 measures the change of the pose by the sum of the absolute changes of the entries of $R$ and $t$.

## Example

The target is a $12 \times 12$ grid on the surface $z = 0.3 \sin(2x) \cos(1.5y) + 0.1 x^2$ over $[-1, 1]^2$, 144 points. The source is 70 of these points (seed 1), moved by the inverse of a rotation of 10 degrees about the axis $(1, 2, 3)$ and the translation $(0.05, -0.03, 0.04)$. Both clouds get plane-to-plane covariances from their 10 nearest neighbors with $\varepsilon = 10^{-3}$. The start pose is the identity, and $d_{\max}$ is not used. Coordinates are unitless.

| outer iteration | GICP cost at the end of the iteration |
|---|---|
| 1 | 1.3 |
| 2 | 0.129 |
| 3 | 3.2e-29 |
| 4 | 3.2e-29 (the pose no longer changes, stop) |

The final rotation differs from the true one by $5 \times 10^{-15}$ radians. The whole run takes about 0.18 s in pure Python. On the same scene, point-to-point ICP needs 14 fit steps to reach the exact pose, and GICP with $C^A = 0$ and $C^B = I$, which is the same cost, needs 15 outer iterations. These counts are measurements on this one scene, not bounds.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows five facts. Each weight $M_{ij}$ exists and is positive definite, because $C^B_j$ is positive definite and $R C^A_i R^{\mathsf T}$ is positive semidefinite. Line L7 accepts only steps that lower $G$, so the fixed-weight cost never rises in line L5, and every accepted rotation is proper. If $H$ is nonsingular and $g \ne 0$, the Gauss-Newton direction is a descent direction, so small enough steps lower $G$. With $C^A = 0$ and $C^B = I$, $G$ is the point-to-point cost, whose minimum is the [Kabsch](/kabsch-algorithm/) solution. An exact rigid copy with the true pairs has $G = 0$ at the true pose, the global minimum.

The proof does not show that the full cost falls from one outer iteration to the next: the weights change with $R$, and the pairs change in line L3. The paper gives no convergence proof either.

## Complexity

The model is the [real RAM](/real-ram/). The reference code finds the $k$ nearest neighbors of each point by sorting all distances, so the covariances cost $\Theta(n^2 \log n + m^2 \log m)$; each one then needs a $3 \times 3$ eigendecomposition, $O(1)$. A [k-d tree](/kd-tree/) brings this to about $(n + m) \log(n + m)$ on typical 3D data. In each outer iteration, line L3 costs $\Theta(n m)$ by brute force, and line L4 inverts $n$ matrices of size $3 \times 3$, $\Theta(n)$. Each inner step builds $H$ and $g$ in $\Theta(n)$ time, solves a $6 \times 6$ system in $O(1)$, and evaluates $G$ at most 31 times in line L7, $\Theta(n)$ each. With at most $S$ inner steps, an outer iteration costs $O(n m + S n)$. The extra space holds the covariances and the weights, $\Theta(n + m)$.

There is no bound on the number $N$ of outer iterations beyond the cap. Measured counts are benchmark results.

## Properties

- **Contains ICP.** $C^A = 0$ and $C^B = I$ give point-to-point ICP; flat target covariances give point-to-plane ICP in the limit.
- **Nearly symmetric.** With plane-to-plane covariances on both clouds, swapping source and target changes the result little, unlike point-to-plane ICP, which uses the target normals only.
- **Monotone inside an iteration.** The fixed-weight cost never rises in line L5. Across iterations, no monotone result is proved.
- **Local.** The result depends on the start pose.
- **Robust to pairs that slide.** A pair whose points lie on the same flat patch adds almost no cost for a slide along the patch, so wrong pairs on smooth surfaces hurt less.

## Variants and improvements

- **Full weights in the minimizer.** The paper keeps $R C^A_i R^{\mathsf T}$ inside the cost during the minimization and uses conjugate gradients; see the [nonlinear conjugate gradient](/nonlinear-conjugate-gradient/) method.
- **Distributions instead of points.** The [normal distributions transform](/normal-distributions-transform/) fits points to a grid of Gaussian cells, a related probabilistic cost without point pairs.
- **Voxelized GICP.** Later work replaces the single closest target point by the Gaussian of a voxel, which removes most nearest neighbor queries.
- **Robust kernels.** A Huber or Cauchy kernel on the Mahalanobis residual, as in an [M-estimator](/m-estimator/), replaces the hard threshold $d_{\max}$.
- **Trimming.** Keeping only the best fraction of pairs, as in [trimmed ICP](/trimmed-icp/), handles partial overlap.

## When to use it

Use GICP for laser or depth scans of scenes made of smooth surfaces, such as buildings, roads and rooms, when a rough pose is known. It is a good default when both clouds are dense enough for covariances, because it combines the speed of point-to-plane ICP with a symmetric use of both surfaces. Use plain [ICP](/iterative-closest-point/) on sparse clouds where neighbors do not describe a surface. Use [point-to-plane ICP](/point-to-plane-icp/) when the target has good normals and the source is sparse. Without a rough pose, start with a global method.

## Pitfalls

- **$\varepsilon = 0$ in the covariances.** Then $C^B_j$ is singular, and line L4 can fail when $C^A_i$ is also flat in the same direction. Keep $\varepsilon > 0$.
- **The wrong rotation of $C^A$ in line L4.** The source covariance moves with the source points, so it is $R C^A_i R^{\mathsf T}$. Writing $R^{\mathsf T} C^A_i R$ rotates it the wrong way and gives wrong weights for every turned pose.
- **No threshold in line L3.** Points of the source with no partner in the target get a closest point anyway, and flat covariances do not remove their error across the surface. Set $d_{\max}$ or trim.
- **Neighborhoods across edges.** A neighborhood that crosses a corner gives a covariance that is not flat, and line L4 then treats the point as a blob. Use a neighborhood size that fits the sampling.
- **Expecting monotone outer costs.** The cost recorded after line L5 in each outer iteration can rise from one iteration to the next, because the weights and pairs change. Do not stop on the first rise.

## Implementations

## History

Segal, Haehnel and Thrun presented Generalized-ICP at Robotics: Science and Systems in 2009. They wrote the fit step of ICP as a maximum likelihood problem with a covariance on each point, showed that point-to-point and point-to-plane ICP are special cases, and proposed the plane-to-plane model with covariances from local neighborhoods. Their experiments on simulated and real laser data showed fewer failures than point-to-point and point-to-plane ICP over a range of start poses and thresholds, which are benchmark results. GICP became a standard registration method in laser mapping and is included in common point cloud libraries.

## References
