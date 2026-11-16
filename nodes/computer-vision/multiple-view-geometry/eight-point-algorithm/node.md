---
tag: ZB0KR6
kind: algorithm
slug: eight-point-algorithm
name: Eight-point algorithm
aliases:
- Longuet-Higgins eight-point algorithm
area: computer-vision/multiple-view-geometry
level: core
summary: "Estimate the essential or fundamental matrix linearly from eight or more matches by SVD, then enforce rank 2 by zeroing the smallest singular value."
solves: [relative-pose-problem]
model: floating-point-model
complexity:
  vars: {n: the number of point pairs}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1981
  people: [H. C. Longuet-Higgins, Richard Hartley]
  note: Longuet-Higgins gave the linear method for the essential matrix from eight matches in 1981. Hartley showed in 1997 that it works well on pixel data once the points are normalized.
prereqs: [fundamental-matrix, singular-value-decomposition]
see_also: [normalized-eight-point-algorithm, seven-point-algorithm, five-point-algorithm, essential-matrix, hartley-normalization, algebraic-and-geometric-error, ransac, dlt-homography]
sources:
  - paper: doi:10.1038/293133a0
    title: "H. C. Longuet-Higgins, A computer algorithm for reconstructing a scene from two projections, Nature 293, 1981, 133-135"
    locator: the linear equations in the nine entries of the essential matrix from eight point matches
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 11.1, Basic equations, and Section 11.2, The normalized 8-point algorithm (the rank 2 constraint by the SVD)"
  - paper: doi:10.1109/34.601246
    title: "Richard I. Hartley, In defense of the eight-point algorithm, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(6), 1997, 580-593"
    locator: the analysis of the plain algorithm on pixel coordinates and its condition
  - book: isbn:9780387008936
    title: "Yi Ma, Stefano Soatto, Jana Kosecka and S. Shankar Sastry, An Invitation to 3-D Vision, Springer, 2004"
    locator: "Chapter 5, Section 5.2.1 (the eight-point linear algorithm and the projection onto the essential space)"
---

The eight-point algorithm estimates the [fundamental matrix](/fundamental-matrix/) $F$, or the [essential matrix](/essential-matrix/) $E$ of calibrated cameras, from $n \ge 8$ point matches. Each match $\mathbf{x}_1 \leftrightarrow \mathbf{x}_2$ gives the equation $\mathbf{x}_2^{\mathsf T}F\mathbf{x}_1 = 0$, which is linear in the nine entries of $F$. The algorithm stacks these equations into an $n \times 9$ matrix $A$, takes the unit vector that makes $\|A\mathbf{f}\|$ smallest, and then forces the rank 2 that every fundamental matrix has. Longuet-Higgins (1981) gave it for the essential matrix. This page gives the plain form; on pixel coordinates it must be used with [Hartley normalization](/hartley-normalization/), which is the [normalized eight-point algorithm](/normalized-eight-point-algorithm/).

## In plain words

Two matching points must satisfy one equation with the unknown matrix, and in that equation each unknown entry appears only to the first power. Each match gives one such equation. The matrix has nine entries, but its overall size does not matter, so eight matches are enough to fix it. With more matches and some noise, no matrix fits all equations, so the algorithm takes the one with the smallest total leftover. A true fundamental matrix always flattens one direction to nothing, but the matrix from the equations usually does not. The last step removes the weakest direction to make it right.

## The problem

**Input.** Point pairs $(\mathbf{x}_{1,i}, \mathbf{x}_{2,i})$, $i = 1, \ldots, n$, $n \ge 8$, as 2D points $(u, v)$ that the algorithm extends to $(u, v, 1)^{\mathsf T}$. For the essential variant the points are in normalized image coordinates, $\hat{\mathbf{x}} = K^{-1}\mathbf{x}$.

**Output.** A $3 \times 3$ matrix $F$ of rank 2 (or with singular values $(s, s, 0)$ in the essential variant) with $\|F\|_F = 1$ and with its entry of largest absolute value positive. If the pairs are exact images of points in general position seen by two cameras with different centers, the output is the true matrix in this form.

## The algorithm

```pseudo id=main
EIGHT-POINT(x1_1 .. x1_n, x2_1 .. x2_n, essential)
L1  for i <- 1 to n
L2      append the row (u2 u1, u2 v1, u2, v2 u1, v2 v1, v2, u1, v1, 1) of the pair (x1_i, x2_i) to A
L3  f <- the right singular vector of A for its smallest singular value
L4  F0 <- the 3 x 3 matrix with rows f[1..3], f[4..6], f[7..9]
L5  (U, diag(s1, s2, s3), V) <- the SVD of F0
L6  F <- U diag(s1, s2, 0) V^T, or U diag(m, m, 0) V^T with m = (s1 + s2) / 2 if essential
L7  return F / ||F||_F, with the sign that makes its entry of largest absolute value positive
```

The row of line L2 is the [Kronecker product](/kronecker-product/) of $(u_2, v_2, 1)$ and $(u_1, v_1, 1)$, so that its dot product with $\mathbf{f}$, the entries of $F$ row by row, is $\mathbf{x}_2^{\mathsf T}F\mathbf{x}_1$. Line L3 minimizes $\|A\mathbf{f}\|$ over unit vectors by the [singular value decomposition](/singular-value-decomposition/). On exact data $A$ has rank 8 and $\mathbf{f}$ spans its null space. Line L6 replaces $F_0$ by the closest matrix of rank 2 in the Frobenius norm; in the essential variant it gives the closest matrix with two equal singular values and a zero one, as the [characterization theorem](/essential-matrix-characterization/) shows. Line L7 picks one of the matrices $\lambda F$ so that equal results compare equal.

## Example

Take the pose of the running example of [epipolar geometry](/epipolar-geometry/): $R = \begin{pmatrix} 0.8 & 0 & 0.6 \\ 0 & 1 & 0 \\ -0.6 & 0 & 0.8 \end{pmatrix}$, $\mathbf{t} = (1, 0, 0)$, $\mathbf{X}_2 = R\mathbf{X}_1 + \mathbf{t}$, and $E = [\mathbf{t}]_\times R = \begin{pmatrix} 0 & 0 & 0 \\ 0.6 & 0 & -0.8 \\ 0 & 1 & 0 \end{pmatrix}$. The eight points $\mathbf{X}_1$ are $(0, 0, 5)$, $(1, 1, 4)$, $(-1, 2, 6)$, $(2, -1, 5)$, $(-2, -2, 8)$, $(1, -2, 4)$, $(-1, -1, 5)$ and $(2, 2, 6)$. In normalized coordinates the first two pairs are $(0, 0) \leftrightarrow (1, 0)$ and $(\frac14, \frac14) \leftrightarrow (\frac{21}{13}, \frac{5}{13})$.

| line | value |
|---|---|
| L1, L2 | 8 rows; the row of pair 2 is $(\frac{21}{52}, \frac{21}{52}, \frac{21}{13}, \frac{5}{52}, \frac{5}{52}, \frac{5}{13}, \frac14, \frac14, 1)$ |
| L3 | the singular values of $A$ are $4.770, 1.867, 1.321, 0.3244, 0.2586, 0.1355, 0.03630, 0.01561$ and 0, so $A$ has rank 8 and $\mathbf{f}$ is the null vector |
| L4 | $F_0 = \pm E/\sqrt2$ |
| L5 | the singular values of $F_0$ are $(0.70711, 0.70711, 0)$ |
| L6 | no change: $F_0$ already has rank 2 and two equal singular values |
| L7 | $\begin{pmatrix} 0 & 0 & 0 \\ 0.42426 & 0 & -0.56569 \\ 0 & 0.70711 & 0 \end{pmatrix} = E/\sqrt2$ |

A check of pair 1: $E(0, 0, 1)^{\mathsf T} = (0, -0.8, 0)^{\mathsf T}$, and its dot product with $(1, 0, 1)$ is 0. Now add $0.01$ to $v_2$ of pair 4. Then $A$ has full rank, the singular values of $F_0$ are $(0.71388, 0.70023, 0.0071020)$, line L6 drops the third one, and line L7 gives singular values $(0.71390, 0.70025, 0)$. The essential variant gives $(0.70711, 0.70711, 0)$. The algebraic residuals $\mathbf{x}_2^{\mathsf T}F\mathbf{x}_1$ of the eight pairs are now about $0.002$ to $0.013$ instead of 0.

## Correctness

The row of line L2 makes $(A\mathbf{f})_i = \mathbf{x}_{2,i}^{\mathsf T}F\mathbf{x}_{1,i}$. On exact data the true $F$ gives $A\mathbf{f} = \mathbf{0}$, and for eight or more points in general position $A$ has rank 8, so line L3 returns the true $F$ up to scale. Line L6 then changes nothing, because the true matrix already has rank 2 (and equal singular values in the essential case). On noisy data line L3 minimizes the algebraic error and line L6 is the closest rank 2 matrix, by the theorem of Eckart and Young, or by von Neumann's trace inequality for the essential variant. If all points lie on one plane, $A$ has rank at most 6 and the result is not unique. The full proof is below.

## Complexity

Counting arithmetic operations, the loop costs $\Theta(n)$ and builds an $n \times 9$ matrix. The SVD of a matrix with a fixed number of 9 columns costs $\Theta(n)$: a [QR decomposition](/qr-decomposition/) reduces it to a $9 \times 9$ triangle in $\Theta(n)$, and the rest takes a fixed amount of work. Lines L4 to L7 work on $3 \times 3$ matrices and cost $\Theta(1)$. So the time is $\Theta(n)$ in all cases, and the extra space is $\Theta(n)$ for $A$; a version that keeps only $A^{\mathsf T}A$ needs $\Theta(1)$ but squares the [condition number](/condition-number/).

In [floating point](/floating-point-model/) the accuracy depends on the condition of $A$. With pixel coordinates the nine columns have sizes from about $10^5$ (products of two coordinates) down to 1, and the smallest nonzero singular value is tiny compared with the largest. The [normalized version](/normalized-eight-point-algorithm/) shows a measured case where the ratio drops from about $10^6$ to about 65.

## Properties

- **Exact on exact data.** For exact matches of points in general position, with at least eight pairs and two different camera centers, the output is the true matrix in canonical form.
- **Linear and non-iterative.** One SVD of an $n \times 9$ matrix and one of a $3 \times 3$ matrix.
- **Algebraic, not geometric.** On noisy data line L3 minimizes $\sum_i (\mathbf{x}_{2,i}^{\mathsf T}F\mathbf{x}_{1,i})^2$, which is not a distance in the images. See [algebraic and geometric error](/algebraic-and-geometric-error/).
- **Two steps, not one.** The rank step is done after the least squares step. The result is not the rank 2 matrix with the smallest algebraic error.
- **Not covariant.** The plain algorithm depends on the origin and the unit of the image coordinates. The normalized form removes this.
- **Swap gives the transpose.** Exchanging the two images gives the canonical form of $F^{\mathsf T}$.

## Variants and improvements

- **Normalized eight-point algorithm.** Move and scale the points of each image first. This is the standard form; see [normalized eight-point algorithm](/normalized-eight-point-algorithm/).
- **Essential variant.** For normalized image coordinates, line L6 sets the singular values to $(m, m, 0)$. The pose then comes from [essential matrix decomposition](/essential-matrix-decomposition/).
- **Seven points.** With seven matches $A$ has a two-dimensional null space, and $\det F = 0$ gives a cubic. See [seven-point algorithm](/seven-point-algorithm/).
- **Five points for calibrated cameras.** The [five-point algorithm](/five-point-algorithm/) uses the cubic constraints of the essential matrix and needs fewer matches, which matters inside [RANSAC](/ransac/): for an inlier ratio of 0.5 and 99% confidence the [iteration bound](/ransac-iteration-bound/) is 1177 samples of eight, against 146 samples of five.
- **Geometric refinement.** Use the output to start a minimization of the [Sampson distance](/sampson-distance/) or of the [reprojection error](/reprojection-error/) with [Levenberg-Marquardt](/levenberg-marquardt/).

## When to use it

Use the eight-point algorithm when there are eight or more matches with few or no outliers, for example on the inliers that RANSAC found, or as a fast first estimate. Always normalize pixel coordinates first. For calibrated cameras with outliers, the five-point solver inside RANSAC needs fewer samples. When accuracy matters, refine the linear result with a geometric cost.

## Pitfalls

- **Raw pixel coordinates.** Without normalization the result can be wrong by several pixels even for small noise.
- **No rank step.** Without line L6 the epipolar lines do not meet in one epipole.
- **Planar scenes and pure rotation.** If all points lie on one plane, or the cameras share their center, $A$ has rank at most 6 and many matrices fit. Use a [homography](/homography/) for these cases.
- **Outliers.** One wrong match can move the result far. Use the algorithm inside [RANSAC](/ransac/) or on its inliers.
- **Direction.** The output satisfies $\mathbf{x}_2^{\mathsf T}F\mathbf{x}_1 = 0$. The other order of the images needs $F^{\mathsf T}$.
- **Sign and scale.** $F$ and $-F$ are the same. Compare canonical forms or epipolar distances, not raw entries.

## Implementations

## History

Longuet-Higgins (1981) showed that eight point matches in two calibrated views give linear equations for the nine entries of the essential matrix, and that the relative pose follows from it. The method was then used for uncalibrated cameras, where the same equations give the fundamental matrix, with the rank 2 condition added by the SVD. For years it was thought too sensitive to noise for practical use. Hartley (1997) showed that the trouble came from the bad condition of $A$ on pixel coordinates and that a simple normalization makes the linear result nearly as good as iterative methods. Hartley and Zisserman (2000, second edition 2004) describe it in Chapter 11.

## References
