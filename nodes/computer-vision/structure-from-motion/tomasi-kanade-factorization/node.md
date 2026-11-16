---
tag: 0876R2
kind: algorithm
slug: tomasi-kanade-factorization
name: Tomasi-Kanade factorization
aliases:
- factorization method
- affine factorization
area: computer-vision/structure-from-motion
level: core
summary: Recover affine cameras and points from tracks in all views by a rank-3 SVD of the centered measurement matrix, followed by a metric upgrade.
solves: [structure-from-motion-problem]
model: real-ram
complexity:
  vars: {N: "the number of frames", n: "the number of points"}
  time: {total: "O(N n min(N, n))"}
  space: {extra: "O(N n)"}
properties: {deterministic: true, iterative: false, local: false, recursive: false, monotone: false}
history:
  year: 1992
  people: [Carlo Tomasi, Takeo Kanade]
  note: Tomasi and Kanade showed that the centered matrix of orthographic tracks has rank 3 and factored it by the SVD. Poelman and Kanade (1997) extended the method to the paraperspective camera.
prereqs: [affine-camera-model, singular-value-decomposition, structure-from-motion-problem]
see_also: [sturm-triggs-factorization, kanade-lucas-tomasi-tracker, cholesky-decomposition, principal-component-analysis, matrix-completion, robust-pca, bundle-adjustment, incremental-structure-from-motion]
sources:
  - paper: doi:10.1007/BF00129684
    title: "Carlo Tomasi and Takeo Kanade, Shape and motion from image streams under orthography: a factorization method, International Journal of Computer Vision 9(2), 1992, 137-154"
    locator: "the whole paper (the rank theorem, the factorization by the SVD, the metric constraints and the experiments)"
  - paper: doi:10.1109/34.584098
    title: "Conrad J. Poelman and Takeo Kanade, A paraperspective factorization method for shape and motion recovery, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(3), 1997, 206-218"
    locator: "the paraperspective model and its metric constraints"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Chapter 18, N-view computational methods (the factorization algorithm for affine cameras)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 11, Structure from motion and SLAM (the section on factorization)"
---

The Tomasi-Kanade factorization recovers the shape of a rigid object and the motion of an orthographic camera from point tracks, when every point is seen in every frame. It is the classic solution of the [structure from motion problem](/structure-from-motion-problem/) for the [affine camera](/affine-camera-model/). Put the image coordinates of $n$ points in $N$ frames into one $2N \times n$ measurement matrix and subtract the mean of each row. The rank theorem says that the result has rank at most 3, because it is the product of a $2N \times 3$ motion matrix and a $3 \times n$ shape matrix. So one [singular value decomposition](/singular-value-decomposition/) that keeps the 3 largest singular values gives the motion and the shape, up to an invertible $3 \times 3$ matrix. A second, metric step fixes that matrix by asking that the camera rows be orthonormal, which leaves only a rotation of the world and a mirror reflection in depth. The method uses all data at once, has no start point and no iteration, and with noise its truncated SVD gives the best rank 3 fit in the Frobenius norm.

## In plain words

A camera far away from an object sees it almost without perspective: the image is a flat shadow of the object, turned and moved. Follow some points of the object through a video and write all their image positions into one big table, one pair of rows per frame. Remove the average position in each row. Every number in the table now comes from only three hidden numbers per point and three per row, so the table has a very simple structure. A standard matrix tool, the SVD, splits it into a camera part and a shape part. One last correction makes the camera parts look like real turns. The result is the 3D shape, but you cannot tell it from its mirror image.

## The problem

**Input.** For $N \ge 3$ frames and $n \ge 4$ points, the image point $(u_{fp}, v_{fp})$ of point $p$ in frame $f$, with every point seen in every frame.

**Camera model.** Frame $f$ is an orthographic camera without a scale factor: the world point $X_p$ maps to $u_{fp} = i_f \cdot X_p + a_f$ and $v_{fp} = j_f \cdot X_p + b_f$, where $i_f$ and $j_f$ are the first two rows of a rotation and $(a_f, b_f)$ is an image translation.

**Output.** The rows $i_f, j_f$ of each frame, the translations $(a_f, b_f)$ and the points $X_p$, with the origin at the centroid of the points. The answer is unique up to one orthogonal matrix applied to the world, a rotation or a rotation with a mirror.

**Rank theorem.** Let $W$ be the $2N \times n$ matrix with row $2f$ holding the $u_{fp}$ and row $2f + 1$ the $v_{fp}$. Let $t$ hold the row means. Then $\tilde W = W - t \mathbf 1^{\mathsf T} = M S$, where $M$ is $2N \times 3$ with the rows $i_f$ and $j_f$, and $S$ is $3 \times n$ with the centered points. So $\operatorname{rank} \tilde W \le 3$ (theorem).

## The algorithm

```pseudo id=main
TOMASI-KANADE(W)
L1  t <- the row means of W; W~ <- W - t 1^T
L2  U Σ V^T <- the SVD of W~
L3  M^ <- U_3 Σ_3^(1/2); X^ <- Σ_3^(1/2) V_3^T, from the 3 largest singular values
L4  for each frame f with rows a, b of M^: the equations a^T L a = 1, b^T L b = 1, a^T L b = 0, linear in the 6 entries of a symmetric L
L5  L <- the least squares solution of the 3N equations of line L4
L6  Q <- the Cholesky factor of L, so that L = Q Q^T
L7  M <- M^ Q; X <- Q^(-1) X^
L8  rotate the world so that the rows of frame 0 are e_1 and e_2
L9  return M, t, X
```

Line L3 splits the singular values evenly between the two factors; any split gives the same result after the metric step. Line L4 states that the rows of $M = \hat M Q$ have unit length and that the two rows of one frame are orthogonal, since $m^{\mathsf T} m = \hat m^{\mathsf T} Q Q^{\mathsf T} \hat m$. The unknown is $L = Q Q^{\mathsf T}$, not $Q$, because the constraints are linear in $L$. Line L6 uses the [Cholesky decomposition](/cholesky-decomposition/) and fails when the least squares $L$ is not positive definite, which happens when the data are far from orthographic; the reference code raises an error then. Line L8 only fixes the gauge.

## Example

The reference test draws 12 points in the cube $[-1, 1]^3$ and 5 orthographic frames, each turned by up to 0.6 rad about a random axis from one base rotation and moved by up to 5 units in the image.

- **Exact data.** The singular values of $\tilde W$ are $4.392848$, $3.190207$, $1.031695$, and then 0 up to rounding. So the rank is 3, as the theorem says. The factorization reproduces $W$ to $10^{-9}$, and all 66 distances between the recovered points match the true ones to $10^{-8}$.
- **Noisy data.** With 8 frames, 20 points and Gaussian noise of $0.002$ units on each coordinate, the singular values are $8.34715$, $5.9395$, $1.2151$, $0.01263$, $0.01181$ and smaller. The gap after the third value shows the rank 3 structure. The largest error over the 190 distances between points is $0.0090$, and the root mean square residual of the fit is $0.0016$, a little below the noise, because the fit absorbs part of it.
- **The mirror.** Changing the sign of the third column of $M$ and of the depth of every point gives the same images and orthonormal rows, so the data cannot tell the shape from its mirror image.
- **Two frames.** With 2 frames, the 6 equations of line L4 have rank 5 in the test, so a one-parameter family of $L$ fits, and the method needs at least 3 frames.

These are benchmark results of the reference tests.

## Correctness

On exact data, $\tilde W = M S$ has rank 3 when the true motion rows span $\mathbb{R}^3$ and the points are not coplanar (theorem). Then lines L2 and L3 give an exact factorization $\tilde W = \hat M \hat X$, and every rank 3 factorization differs from the true one by an invertible matrix $A$: $M = \hat M A$ and $S = A^{-1} \hat X$ (theorem). The true $L^* = A A^{\mathsf T}$ satisfies all equations of line L4. If these equations have rank 6, line L5 returns $L^*$, and the Cholesky factor $Q$ equals $A G$ for an orthogonal $G$, so the output is the truth up to $G$ (theorem). The rank 6 condition is generic for 3 or more frames; with 2 frames it fails, in line with Ullman's result that 3 orthographic views of 4 points are needed. With noise, the truncated SVD gives the best rank 3 approximation of $\tilde W$ in the Frobenius norm, which is the maximum likelihood estimate of the affine structure for independent Gaussian noise of equal variance and complete data (theorem). The metric step is a linear least squares fit, not a maximum likelihood estimate (heuristic). The proof file gives the details.

## Complexity

In the real RAM model, line L1 costs $O(N n)$. The SVD of the $2N \times n$ matrix costs $O(N n \min(N, n))$, and it dominates. Only the 3 leading singular vectors are needed, so an iterative method such as [power iteration](/power-iteration/) or a Lanczos method can find them in $O(N n)$ per iteration. Lines L4 and L5 build and solve a $3N \times 6$ least squares problem in $O(N)$. Line L7 costs $O(N + n)$. The space is $O(N n)$ for $W$.

## Properties

- **Closed form.** No start point and no iteration, apart from the SVD itself.
- **Global.** It uses all frames and points at once, so no frame is preferred.
- **Optimal affine fit.** With complete data and equal Gaussian noise, the affine part is the maximum likelihood estimate (theorem).
- **Ambiguities.** A world rotation and a depth mirror remain; with a perspective camera, the mirror is the Necker reversal that perspective cues can resolve.
- **Complete data only.** The plain method needs every point in every frame.

## Variants and improvements

- **Paraperspective and weak perspective.** Poelman and Kanade (1997) used the same factorization with metric constraints for the paraperspective camera, which models the change of scale and position with distance.
- **Missing data.** Tomasi and Kanade (1992) also described how to fill in entries that are missing because of occlusion. Later methods fit the rank 3 model by alternating least squares, Wiberg's method or [matrix completion](/matrix-completion/).
- **Outliers.** [Robust PCA](/robust-pca/) and $L_1$ factorizations handle wrong tracks.
- **Projective cameras.** The [Sturm-Triggs factorization](/sturm-triggs-factorization/) scales each image point by its projective depth so that a rank 4 factorization works for perspective cameras.
- **Multiple bodies and nonrigid shapes.** Costeira and Kanade separated independent motions by the structure of the shape interaction matrix, and nonrigid factorization models the shape as a combination of a few basis shapes.
- **Sequential factorization.** Updates of the factorization frame by frame avoid recomputing the full SVD.

## When to use it

Use it when the camera is far from the object compared with the depth of the object, for example for a telephoto lens or a small object, and when tracks are complete, as in a short video from a [KLT tracker](/kanade-lucas-tomasi-tracker/). It is also a good start for [bundle adjustment](/bundle-adjustment/) with a perspective model. For wide angle views of a deep scene, use a perspective method such as the [Sturm-Triggs factorization](/sturm-triggs-factorization/) or [incremental structure from motion](/incremental-structure-from-motion/).

## Pitfalls

- **Perspective effects.** Strong perspective makes the fourth singular value large and can make $L$ indefinite, so the Cholesky step fails.
- **Planar scenes.** Coplanar points give rank 2, and the third column of the motion is not fixed.
- **Too little rotation.** If all frames have almost the same rotation, the motion rows span less than $\mathbb{R}^3$ in practice, and the depth is poorly determined.
- **Centering with missing data.** The row means must be over the same points in every frame, or the rank theorem fails.
- **The mirror.** The output can be the mirror shape. Use another cue, such as a perspective effect or occlusions, to choose.

## Implementations

## History

Ullman (1979) proved that three orthographic views of four points that are not coplanar determine the structure, up to a reflection. Tomasi and Kanade (1992) observed that the centered measurement matrix of orthographic tracks has rank 3 and factored it with the SVD, which gave a stable method that uses all frames and points together. Poelman and Kanade (1997) extended the method to the paraperspective model. Sturm and Triggs (1996) carried the idea to projective cameras, and the factorization idea became a standard part of multiple view geometry.

## References
