---
tag: J9D82K
kind: algorithm
slug: point-cloud-normal-estimation
name: Point cloud normal estimation
aliases:
- PCA normal estimation
- local plane fitting
area: computer-vision/point-clouds-and-registration
level: core
summary: Estimate the normal at a point as the eigenvector of least eigenvalue of the covariance of its nearest neighbors.
model: real-ram
complexity:
  vars: {n: the number of points, k: the number of neighbors per point}
  time: {worst: O(n^2), average: O(n (log n + k log k)), best: Θ(n k)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false, rigid_motion_invariant: true, sign_ambiguous: true}
history:
  year: 1992
  people: [Hugues Hoppe, Tony DeRose, Tom Duchamp, John McDonald, Werner Stuetzle]
  note: "Hoppe and his coauthors fitted a tangent plane to the k nearest neighbors of each point by principal component analysis, as the first step of surface reconstruction from unorganized points. Pauly, Gross and Kobbelt (2002) added the surface variation, and Mitra and Nguyen (2003) analyzed the choice of k under noise."
prereqs: [point-cloud, principal-component-analysis, nearest-neighbor-search]
see_also: [consistent-normal-orientation, covariance-matrix, jacobi-eigenvalue-algorithm, point-to-plane-icp, poisson-surface-reconstruction, efficient-ransac-shape-detection, point-feature-histograms, range-image]
sources:
  - paper: doi:10.1145/142920.134011
    title: "Hugues Hoppe, Tony DeRose, Tom Duchamp, John McDonald and Werner Stuetzle, Surface reconstruction from unorganized points, Computer Graphics (Proceedings of SIGGRAPH 92) 26(2), 1992, 71-78"
    locator: "The tangent plane of each point from its k nearest neighbors: the centroid, the covariance matrix and the eigenvector of the least eigenvalue"
  - paper: doi:10.1109/VISUAL.2002.1183771
    title: "Mark Pauly, Markus Gross and Leif P. Kobbelt, Efficient simplification of point-sampled surfaces, IEEE Visualization 2002, 163-170"
    locator: "Section 2.1, Covariance Analysis (the covariance of the neighborhood, the normal as the eigenvector of the least eigenvalue, and the surface variation lambda0 / (lambda0 + lambda1 + lambda2))"
  - paper: doi:10.1145/777792.777840
    title: "Niloy J. Mitra and An Nguyen, Estimating surface normals in noisy point cloud data, Symposium on Computational Geometry 2003, 322-328"
    locator: "The analysis of the error of the least squares normal as a function of the neighborhood size, the curvature, the sampling density and the noise"
---

Point cloud normal estimation finds, for each point of a set of 3D points sampled from a surface, the direction perpendicular to the surface at that point. The points come without the surface, so the method fits a plane to the $k$ nearest neighbors of each point and takes the normal of that plane. The best plane in the least squares sense passes through the centroid of the neighbors, and its normal is the eigenvector of the smallest eigenvalue of their $3 \times 3$ [covariance matrix](/covariance-matrix/). This is local [principal component analysis](/principal-component-analysis/): the two large components span the tangent plane, and the smallest one is the normal. The method gives a line, not a direction: the sign of each normal is arbitrary, and making the signs agree is a separate problem, [consistent normal orientation](/consistent-normal-orientation/). The normals feed [point-to-plane ICP](/point-to-plane-icp/), [shape detection](/efficient-ransac-shape-detection/), [descriptors](/point-feature-histograms/) and [surface reconstruction](/poisson-surface-reconstruction/).

## In plain words

Look at one point and its closest neighbors, say 10 or 20 of them. On a smooth surface they lie almost on a flat sheet. Find the flat sheet that passes closest to all of them. The normal is the direction straight out of that sheet.

To find the sheet, measure how the neighbors spread out around their middle point. They spread a lot along the two directions of the sheet, and very little across it. The direction with the least spread is the normal. The amount of spread across the sheet, compared with the total, also tells you how flat the patch is: zero on a plane, larger at edges, corners and noise.

The method cannot tell the outside of the sheet from the inside. It gives the normal up to its sign.

## The problem

The input is a finite list $P$ of $n$ points in $\mathbb{R}^3$, sampled from a smooth surface with some noise, and a neighborhood size $k$ with $3 \le k \le n$. For each point $p_i$ the output is a unit vector $\mathbf{n}_i$ that approximates the surface normal at $p_i$, up to sign, and a number $\sigma_i$ that measures how far the neighborhood is from a plane.

The surface is unknown, so the true normal is not available, and "approximates" has no exact meaning without a model of the sampling and the noise. The algorithm solves an exact problem in its place: for each neighborhood, the plane that minimizes the sum of the squared orthogonal distances to the neighbors.

## The algorithm

```pseudo id=main
ESTIMATE-NORMALS(P, k, o)                ▷ o is an optional viewpoint
L1  for each point p_i in P do
L2      Q ← the k points of P nearest to p_i, with p_i itself
L3      c ← (1/k) Σ_{q ∈ Q} q
L4      C ← (1/k) Σ_{q ∈ Q} (q - c)(q - c)ᵀ
L5      (λ₀ ≤ λ₁ ≤ λ₂, v₀, v₁, v₂) ← the eigenvalues and unit eigenvectors of C
L6      n_i ← v₀
L7      σ_i ← λ₀ / (λ₀ + λ₁ + λ₂)
L8      if o is given and n_i · (o - p_i) < 0 then n_i ← -n_i
L9  return the pairs (n_i, σ_i)
```

Line L2 is a $k$-nearest neighbor query, usually on a [k-d tree](/kd-tree/) built once, or a fixed radius query. On a [range image](/range-image/) the neighbors are the cells of a small window. Lines L3 and L4 build the covariance around the centroid, not around $p_i$. Line L5 solves a symmetric $3 \times 3$ eigenproblem, for example by the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/) or by the closed form for the roots of a cubic. Line L7 is the surface variation of Pauly, Gross and Kobbelt (2002). Line L8 is the usual quick fix for the sign when the cloud comes from one sensor at $o$: a surface seen by the sensor faces it.

The same normal is the right singular vector of the smallest singular value of the $k \times 3$ matrix of centered neighbors. The SVD is a little more accurate in floating point, and the covariance is cheaper.

## Example

Take a neighborhood of five points: the corners $(\pm 1, \pm 1, 0)$ of a square, and a bump $(0, 0, 0.5)$ at its center.

| step | value |
|---|---|
| centroid $c$ | $(0, 0, 0.1)$ |
| $C_{xx}$, $C_{yy}$ | $4/5 = 0.8$ each |
| $C_{zz}$ | $(4 \cdot 0.1^2 + 0.4^2)/5 = 0.04$ |
| $C_{xy}$, $C_{xz}$, $C_{yz}$ | 0, by symmetry |
| eigenvalues | $0.04, 0.8, 0.8$ |
| normal $v_0$ | $(0, 0, \pm 1)$ |
| surface variation | $0.04 / 1.64 = 0.0244$ |

The covariance is diagonal, so its eigenvectors are the axes. The least spread is along $z$, and the normal is $\pm z$, as the shape of the square says. The bump pulls the centroid up to $z = 0.1$ but does not tilt the plane, because it sits at the center. The surface variation is small but not zero: the five points are not coplanar. Moving the bump to a corner, $(1, 1, 0.5)$, would tilt the fitted plane toward it.

## Correctness

For a fixed unit normal $n$, the sum of squared distances to the plane $n \cdot x = d$ is least when the plane passes through the centroid, and it then equals $k\, n^\top C n$. By the spectral theorem, $n^\top C n$ over unit vectors is least at the eigenvector of the least eigenvalue, so line L6 gives the normal of the total least squares plane of the neighborhood. The surface variation lies in $[0, 1/3]$. It is 0 exactly when the neighbors are coplanar, and $1/3$ exactly when the three eigenvalues are equal. A rigid motion of the cloud rotates every normal with it and keeps every $\sigma_i$. The full proof is below.

This is a statement about the fit, not about the true surface. How close $v_0$ is to the true normal depends on the noise, the curvature, the sampling density and $k$, as analyzed by Mitra and Nguyen (2003): a larger $k$ averages out more noise but sees more curvature, so there is a best neighborhood size that depends on the data.

## Complexity

The model is the [real RAM](/real-ram/), with $n$ points and $k$ neighbors per point.

- **Per point, after the search.** Lines L3 and L4 cost $\Theta(k)$. Line L5 is a $3 \times 3$ problem and costs $O(1)$. Lines L6 to L8 cost $O(1)$.
- **Neighbor search.** Brute force costs $\Theta(n)$ per point, so $\Theta(n^2)$ in total. With a k-d tree on well-spread points in 3D, the build costs $O(n \log n)$ and a query costs $O(\log n + k \log k)$ on average, for $O(n (\log n + k \log k))$ in total. On a range image the search is free.
- **Space.** $\Theta(n)$ for the tree and the output.

The search dominates. The fit itself is $\Theta(n k)$ in total.

## Properties

- **Sign ambiguous.** $v_0$ and $-v_0$ are both eigenvectors. Without a viewpoint, the sign of each normal is arbitrary.
- **Rigid motion invariant.** Rotating and moving the cloud rotates the normals with it and keeps the surface variation.
- **Smoothing.** The fitted plane averages over the neighborhood, so it rounds off sharp edges: a point on an edge gets a normal between the normals of the two faces.
- **Not robust.** One outlier in the neighborhood can tilt the plane as much as it likes. Remove outliers first, for example with [statistical outlier removal](/statistical-outlier-removal/).
- **Degenerate neighborhoods.** If the neighbors lie on a line, $\lambda_0 = \lambda_1 = 0$ and every direction perpendicular to the line fits equally well.

## Variants and improvements

- **Weighted covariance.** Weight each neighbor by a function of its distance to $p_i$, such as a Gaussian. This makes the result depend less on the exact choice of $k$.
- **Radius neighborhoods.** Use the points within a radius $r$ in place of the $k$ nearest. This fixes the scale of the fit in meters, which helps on clouds of even density.
- **Adaptive $k$.** Choose $k$ per point from estimates of the noise and the curvature, as Mitra and Nguyen propose, or take the $k$ that minimizes the surface variation.
- **Robust fits.** Fit the plane with [RANSAC](/ransac/) or an M-estimator, which keeps sharp edges and ignores outliers. Methods that use a randomized Hough transform or that fit several planes near edges follow the same idea.
- **Quadric fits and jets.** Fit a quadratic or cubic height function in the frame of the PCA plane. This gives better normals on curved surfaces and also the curvatures.
- **Normals from a grid.** On a [range image](/range-image/), the cross product of the differences to the grid neighbors gives a normal in $O(1)$ time with no search.
- **Learned estimators.** Networks trained on synthetic shapes predict normals from neighborhoods. They are outside this page.

## When to use it

Use PCA normals as the default for any point cloud that lacks normals: they are cheap, stable on smooth surfaces and need only $k$. Remove outliers and downsample to an even density first, and choose $k$ to cover a patch that is flat at the scale of the noise, often 10 to 30 points. Use a robust or a jet fit when the shapes have sharp edges or high curvature. If the normals must point outward, follow with a viewpoint test or with [consistent normal orientation](/consistent-normal-orientation/).

## Pitfalls

- **The wrong eigenvector.** Libraries return eigenvalues in different orders. Line L6 needs the eigenvector of the least eigenvalue. With an SVD, which sorts singular values from large to small, it is the last right singular vector, not the first.
- **No centering.** Using $\sum (q - p_i)(q - p_i)^\top$ at line L4, around the point and not the centroid, mixes the offset of the point into the matrix and tilts the normal. Subtract the centroid of line L3.
- **One-pass covariance at large coordinates.** Computing $C$ as $\frac1k \sum q q^\top - c c^\top$ cancels most of its digits when the coordinates are large compared with the size of the neighborhood, as in georeferenced lidar. Subtract the centroid first, or a local origin.
- **Neighbors from one scan line.** A lidar samples densely along each scan line and sparsely across lines. The $k$ nearest neighbors can all come from one line, so $\lambda_0 \approx \lambda_1$ and the normal is noise. Use a radius large enough to reach the next line, or a grid of the scan.
- **Trusting the sign.** Line L6 gives no sign. Code that uses the normals as if they pointed outward, for shading, for ICP rejection rules or for reconstruction, fails at random. Orient them at line L8 or with a propagation method.
- **Too large a neighborhood across thin parts.** For a thin plate, the $k$ nearest neighbors can include points of the other side. The fit then sees two parallel sheets and still finds a good plane, but the curvature and the orientation step later go wrong.

## Implementations

## History

Hoppe, DeRose, Duchamp, McDonald and Stuetzle (1992) needed an oriented tangent plane at each point to reconstruct a surface from unorganized points. They fitted the plane to the $k$ nearest neighbors through their centroid and took its normal as the eigenvector of the least eigenvalue of the covariance matrix; they then oriented the normals by propagation along a spanning tree. Pauly, Gross and Kobbelt (2002) used the same covariance analysis for the simplification of point-sampled surfaces and defined the surface variation as a measure of curvature. Mitra and Nguyen (2003) analyzed the error of the least squares normal under noise and derived a neighborhood size from the noise, the curvature and the density. The method is the normal estimator of the Point Cloud Library and of most point cloud software.

## References
