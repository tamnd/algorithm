---
tag: JQNS8Q
kind: algorithm
slug: sturm-triggs-factorization
name: Sturm-Triggs projective factorization
aliases:
- projective factorization
area: computer-vision/structure-from-motion
level: advanced
summary: Rescale the measurement matrix by projective depths from fundamental matrices so that it has rank 4, and factor it into projective cameras and points.
solves: [structure-from-motion-problem]
model: real-ram
complexity:
  vars: {N: "the number of images", n: "the number of points"}
  time: {total: "O(N n min(N, n))"}
  space: {extra: "O(N n)"}
properties: {deterministic: true, iterative: false, local: false, recursive: false, monotone: false}
history:
  year: 1996
  people: [Peter Sturm, Bill Triggs]
  note: Sturm and Triggs (ECCV 1996) recovered the projective depths from fundamental matrices and epipoles and factored the rescaled measurement matrix by the SVD, which extends the factorization of Tomasi and Kanade to perspective cameras.
prereqs: [tomasi-kanade-factorization, fundamental-matrix, projective-reconstruction-theorem]
see_also: [structure-from-motion-problem, normalized-eight-point-algorithm, hartley-normalization, self-calibration, stratified-reconstruction, bundle-adjustment, singular-value-decomposition, epipolar-geometry]
sources:
  - paper: doi:10.1007/3-540-61123-1_183
    title: "Peter Sturm and Bill Triggs, A factorization based algorithm for multi-image projective structure and motion, Computer Vision ECCV '96, Lecture Notes in Computer Science 1065, Springer, 1996, 709-720"
    locator: "the whole paper (the recovery of the projective depths from fundamental matrices and epipoles, the balancing and the factorization)"
  - paper: doi:10.1109/CVPR.1996.517170
    title: "Bill Triggs, Factorization methods for projective structure and motion, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 1996), 845-851"
    locator: "the projective factorization and the depth recovery from matching tensors"
  - paper: doi:10.1109/TPAMI.2007.1132
    title: "John Oliensis and Richard Hartley, Iterative extensions of the Sturm/Triggs algorithm: convergence and nonconvergence, IEEE Transactions on Pattern Analysis and Machine Intelligence 29(12), 2007, 2217-2233"
    locator: "the analysis of the iterations that alternate between the depths and the factorization"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Chapter 18, N-view computational methods (projective factorization) and Chapter 10 (the projective reconstruction theorem)"
---

The Sturm-Triggs factorization recovers projective cameras and points from point tracks seen in all of $N$ perspective images. It extends the [Tomasi-Kanade factorization](/tomasi-kanade-factorization/) from affine to perspective cameras. Under perspective, the image point $x_{ip}$ of point $X_p$ in camera $P_i$ satisfies $\lambda_{ip} x_{ip} = P_i X_p$ for an unknown scalar $\lambda_{ip}$, the projective depth. If the depths were known, the $3N \times n$ matrix with the blocks $\lambda_{ip} x_{ip}$ would equal the product of the stacked cameras and the stacked points, so it would have rank 4. Sturm and Triggs found the depths, up to one scale per image and one per point, from the [fundamental matrices](/fundamental-matrix/) and epipoles of image pairs, and then factored the rescaled matrix by the [SVD](/singular-value-decomposition/). By the [projective reconstruction theorem](/projective-reconstruction-theorem/), the result is the truth up to one projective change of coordinates in space. It is a linear method that treats all images at once, and it is often the start for projective [bundle adjustment](/bundle-adjustment/) and for [self-calibration](/self-calibration/).

## In plain words

In a photo, a point tells you only along which line of sight the true 3D point lies, not how far away it is. If you knew the distances, you could write all the image points of all photos into one table, and the table would have a very simple structure that one standard matrix tool splits into cameras and points. The trick is to find the distances first. For two photos, the geometry of the pair relates the distance of a point in one photo to its distance in the other. So you fix the distances in the first photo, pass them along from photo to photo, fill the table and split it. The result is correct only up to a general distortion of space, which you remove later with extra knowledge about the cameras.

## The problem

**Input.** For $N \ge 2$ images and $n \ge 8$ points, the pixel $u_{ip}$ of point $p$ in image $i$, with every point seen in every image.

**Model.** Image $i$ is a projective camera $P_i$, a $3 \times 4$ matrix, and point $p$ is a homogeneous 4-vector $X_p$, with $\lambda_{ip} x_{ip} = P_i X_p$, where $x_{ip} = (u, v, 1)$ and $\lambda_{ip} \ne 0$.

**Output.** Cameras $P_i$ and points $X_p$ that reproduce the data, up to $P_i \mapsto P_i H$ and $X_p \mapsto H^{-1} X_p$ for one invertible $4 \times 4$ matrix $H$, and the scales of each $P_i$ and $X_p$.

**Rank.** The matrix $W$ with the $3 \times 1$ blocks $\lambda_{ip} x_{ip}$ equals $P X$, where $P$ stacks the cameras ($3N \times 4$) and $X$ holds the points as columns ($4 \times n$). So $\operatorname{rank} W \le 4$ (theorem). With wrong depths, for example all equal to 1, the rank is larger.

**Depths from a pair.** Write $F_i$ for the fundamental matrix of the images $i - 1$ and $i$ with $x_i^{\mathsf T} F_i x_{i-1} = 0$, and $e_i$ for the epipole in image $i$, with $F_i^{\mathsf T} e_i = 0$. For suitable scales of $F_i$ and $e_i$, the true depths satisfy $e_i \times (\lambda_{ip} x_{ip}) = F_i (\lambda_{i-1,p} x_{i-1,p})$ (theorem). Taking the inner product with $e_i \times x_{ip}$ gives the depth of image $i$ from the depth of image $i - 1$.

## The algorithm

```pseudo id=main
STURM-TRIGGS(u)
L1  for each image i: T_i <- the Hartley normalization of its points; x_ip <- T_i u_ip
L2  λ_0p <- 1 for every point p
L3  for i <- 1 to N - 1: F_i <- the eight-point fundamental matrix with x_i^T F_i x_(i-1) = 0; e_i <- the null vector of F_i^T
L4      λ_ip <- λ_(i-1)p (e_i × x_ip) · (F_i x_(i-1)p) / ||e_i × x_ip||² for every point p
L5  W <- the 3N × n matrix with the blocks λ_ip x_ip
L6  balance W: scale the columns to unit norm, then each triplet of rows to unit norm, 3 times
L7  U Σ V^T <- the SVD of W; P^ <- U_4 Σ_4; X <- the columns of V_4^T
L8  P_i <- T_i^(-1) P^_i for each image i
```

Line L1 is [Hartley normalization](/hartley-normalization/), which makes the eight-point method and the SVD well conditioned. Line L3 is the [normalized eight-point algorithm](/normalized-eight-point-algorithm/) on consecutive images; any other spanning tree of image pairs works the same way. Line L4 is the least squares solution of $\lambda_{ip} (e_i \times x_{ip}) = \lambda_{i-1,p} F_i x_{i-1,p}$ for the one unknown $\lambda_{ip}$. The scales of $F_i$ and $e_i$ are arbitrary, but each choice multiplies all depths of image $i$ and of the later images by one common factor, which only rescales the cameras. Line L6 multiplies $W$ by diagonal matrices on both sides, so it keeps the rank, and it keeps the SVD from being dominated by a few large entries. Line L7 keeps the 4 largest singular values, and line L8 undoes the normalization of line L1.

## Example

The reference test draws 20 points in the cube $[-1, 1]^3$ and 4 cameras with $f = 800$ px at a distance of 4 units, each turned by up to 0.4 rad.

- **Exact data.** The singular values of the balanced $W$ are $1.2459$, $1.2318$, $0.9575$, $0.1164$, and then 0 up to rounding. So the rank is 4, and the cameras and points reproduce every pixel to $4 \cdot 10^{-13}$ px. A second test finds the $4 \times 4$ matrix $H$ that maps the recovered points to the true ones, as the theorem predicts.
- **Wrong depths.** With the cameras at a distance of 2.5 units, where perspective is strong, setting all depths to 1 gives the singular values $11.52$, $8.94$, $8.07$, $0.3545$, $0.0683$. The fifth is $0.006$ of the first, so the matrix does not have rank 4. With the chained depths of line L4, the fifth singular value drops to 0.
- **Noise.** With 4 images, 30 points and Gaussian noise of 0.5 px, the reprojection errors have a root mean square of 0.58 px and a maximum of 1.54 px.

These are benchmark results of the reference tests.

## Correctness

On exact data, the chained depths of line L4 equal the true depths times one factor per image and one per point, $\lambda_{ip} = \alpha_i \beta_p \lambda_{ip}^{\mathrm{true}}$, if each consecutive pair has two distinct centers, the eight-point method is exact for it, and no point lies on an epipole (theorem). The matrix $W$ is then $\operatorname{diag}(\alpha_i I_3) \, P X \operatorname{diag}(\beta_p)$, which has rank 4, and the balancing keeps this. Any rank 4 factorization of $W$ differs from the true one by an invertible $4 \times 4$ matrix, so the cameras and points of line L8 are the truth up to a projective change of coordinates and the scales of each camera and point (theorem), and they reproduce every image point exactly. With noise, the SVD minimizes the Frobenius norm of the change to the rescaled matrix, an algebraic error, not the reprojection error, and the chained depths carry errors from image to image, so the result is a good start but not an optimal estimate (heuristic). The proof file gives the details.

## Complexity

In the real RAM model, line L1 costs $O(N n)$. Line L3 runs the eight-point method $N - 1$ times on $n$ points, $O(n)$ each, and line L4 costs $O(1)$ per point and image, so the depths cost $O(N n)$. Lines L5 and L6 cost $O(N n)$. The SVD of the $3N \times n$ matrix costs $O(N n \min(N, n))$ and dominates. The space is $O(N n)$.

## Properties

- **Linear and global.** No start point, and all images are treated together in the SVD.
- **Projective only.** The output is fixed up to a $4 \times 4$ projective change of coordinates. A metric result needs [self-calibration](/self-calibration/) or other knowledge, as in [stratified reconstruction](/stratified-reconstruction/).
- **Signs of the depths.** Nothing forces the recovered depths to be positive. A projective reconstruction with all points in front of all cameras needs an extra step.
- **Complete data.** Every point must be seen in every image.
- **Chain errors.** Depths found along a chain of pairs collect the errors of all pairs on the way.

## Variants and improvements

- **Iterative depths.** Alternate between the factorization and a new estimate of the depths from the projected points, to fit the rank 4 model better. Oliensis and Hartley (2007) studied the convergence of such iterations and showed that the simplest form need not converge to a correct solution.
- **Other depth sources.** The depths can also come from other matching tensors, such as the [trifocal tensor](/trifocal-tensor/), as discussed by Triggs (1996).
- **Missing data.** Fit the rank 4 model only to the observed entries, by alternation or by [matrix completion](/matrix-completion/) methods, and re-estimate the depths at the same time.
- **Affine special case.** For affine cameras all depths can be set to 1. Then the matrix with a row of ones per image has rank 4, and the method is an affine factorization without the centering step of Tomasi and Kanade.

## When to use it

Use it to start a projective or, after self-calibration, a metric reconstruction from a short sequence where all points are tracked in all images, for example a turntable or a short video. It is also a useful baseline for projective methods. For large photo collections with missing data and outliers, use [incremental structure from motion](/incremental-structure-from-motion/) or [global structure from motion](/global-structure-from-motion/). For weak perspective, the [Tomasi-Kanade factorization](/tomasi-kanade-factorization/) is simpler and more stable.

## Pitfalls

- **No normalization.** Without the normalization of line L1, pixel coordinates near 1000 dominate the entry 1 of each homogeneous point, and both the eight-point method and the SVD lose accuracy.
- **Points near an epipole.** Then $e_i \times x_{ip}$ is close to 0, and the depth of line L4 is unstable. The reference code raises an error for an exact hit.
- **Small baselines.** A pair with nearly the same center gives a poor fundamental matrix and poor depths for all later images in the chain.
- **Planar scenes.** Coplanar points make the fundamental matrix undetermined, and the method fails.
- **Reading the result as metric.** The cameras are projective. Distances and angles in the recovered space have no meaning until the projective ambiguity is removed.

## Implementations

## History

Tomasi and Kanade (1992) factored the measurement matrix for orthographic cameras. Sturm and Triggs (1996) showed that the same idea works for perspective cameras once each image point is multiplied by its projective depth, and that these depths follow from the fundamental matrices and epipoles of image pairs. Triggs (1996) gave the theory in terms of matching tensors. Later work studied iterative depth estimation, missing data and the conditions for convergence, among them the analysis of Oliensis and Hartley (2007).

## References
