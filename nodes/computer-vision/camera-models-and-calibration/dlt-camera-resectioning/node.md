---
tag: WCKDXR
kind: algorithm
slug: dlt-camera-resectioning
name: Direct linear transformation for camera resectioning
aliases:
- DLT resectioning
area: computer-vision/camera-models-and-calibration
level: core
summary: Estimate the 3 by 4 camera matrix from six or more world to image point pairs as the null vector of a linear system, found by SVD.
solves: [camera-calibration]
model: floating-point-model
complexity:
  vars: {n: the number of world to image point pairs}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1971
  people: [Y. I. Abdel-Aziz, H. M. Karara]
  note: Abdel-Aziz and Karara introduced the direct linear transformation for close-range photogrammetry in 1971. Hartley showed in 1997 why the data should be normalized first, and Hartley and Zisserman made the normalized DLT followed by a geometric fit their gold standard algorithm.
prereqs: [camera-projection-matrix, singular-value-decomposition]
see_also: [camera-matrix-decomposition, camera-calibration, hartley-normalization, dlt-homography, levenberg-marquardt, reprojection-error, perspective-n-point, condition-number]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Chapter 7, Computation of the camera matrix P (Section 7.1, the basic equations, the minimal solution and the degenerate configurations; Algorithm 7.1, the gold standard algorithm); Section 4.4 on data normalization; Section 22.1 on the degenerate configurations of resectioning
  - paper: doi:10.14358/PERS.81.2.103
    title: Y. I. Abdel-Aziz and H. M. Karara, Direct linear transformation from comparator coordinates into object space coordinates in close-range photogrammetry, Proceedings of the ASP Symposium on Close-Range Photogrammetry, 1971; reprinted in Photogrammetric Engineering and Remote Sensing 81(2), 2015, 103-107
    locator: the whole paper (the 11 parameter linear model from object space to comparator coordinates)
  - paper: doi:10.1109/34.601246
    title: Richard I. Hartley, In defense of the eight-point algorithm, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(6), 1997, 580-593
    locator: the analysis of the condition of the linear system and the isotropic normalization of the data (shown for the fundamental matrix; the same argument applies to the DLT)
---

Direct linear transformation (DLT) resectioning finds the $3 \times 4$ [camera projection matrix](/camera-projection-matrix/) $P$ from $n \ge 6$ known 3D points $X_i$ and their pixels $x_i$. Each pair gives two equations that are linear in the 12 entries of $P$, so $P$ is the null vector of a $2n \times 12$ matrix, which the [singular value decomposition](/singular-value-decomposition/) finds; with noise, it is the unit vector that makes the system smallest. The points must not lie on one plane. Among the close pages, [camera calibration](/camera-calibration/) is the problem of finding $K$ and the distortion; this page finds the full $P$ with no assumption on $K$, from a 3D target; [camera matrix decomposition](/camera-matrix-decomposition/) then splits $P$ into $K$, $R$ and $t$; [Zhang's method](/zhang-calibration-method/) uses a plane instead of a 3D target; and [Tsai's method](/tsai-calibration-method/) also models radial distortion. The same linear idea for a plane to plane map is [DLT for homographies](/dlt-homography/).

## In plain words

You have a box with marks at known places in 3D, and a photo of it. You want the one table of 12 numbers that turns each 3D mark into its spot in the photo. For each mark, the rule "the table sends this mark to that spot" can be written as two plain equations in the 12 numbers. With six marks you have 12 equations, which is enough, since the table is only known up to a common factor. With more marks and some noise, no table fits exactly, so you take the one that comes closest, which a standard matrix tool gives in one step. Before that, you shift and scale both sets of points to a standard size, or the arithmetic loses precision.

## The problem

**Input.** Pairs $X_i \leftrightarrow x_i$, $i = 1, \dots, n$, with $X_i \in \mathbb{R}^3$ world points and $x_i = (u_i, v_i)$ their pixels, with $n \ge 6$. Pixel centers are at integer points, as in HZ and OpenCV.

**Output.** A $3 \times 4$ matrix $P$ with $\|P\|_F = 1$ such that $x_i \sim P (X_i, 1)$ for all $i$ when the data are exact. With noise, $P$ minimizes the algebraic error $\|A p\|$ below. The sign is chosen so that the left $3 \times 3$ block $M$ has $\det M > 0$; then $P = \lambda K [R \mid t]$ with $\lambda > 0$, and points in front of the camera have a positive third coordinate.

**Counting.** $P$ has 11 degrees of freedom and each pair gives 2 equations, so 5.5 pairs are the minimum: 6 pairs, using one of the two equations of the sixth.

## The algorithm

For the homogeneous pixel $\mathbf{x}_i = (x_i, y_i, w_i)$ and the homogeneous world point $\mathbf{X}_i$, the condition $\mathbf{x}_i \sim P \mathbf{X}_i$ is $\mathbf{x}_i \times P \mathbf{X}_i = 0$. Its first two entries are linear in $p$, the 12 entries of $P$ row by row:
$$\begin{pmatrix} 0^{\mathsf T} & -w_i \mathbf{X}_i^{\mathsf T} & y_i \mathbf{X}_i^{\mathsf T} \\ w_i \mathbf{X}_i^{\mathsf T} & 0^{\mathsf T} & -x_i \mathbf{X}_i^{\mathsf T} \end{pmatrix} p = 0.$$
The third entry depends on these two when $w_i \ne 0$. Stacking the rows of all pairs gives $A p = 0$ with $A$ of size $2n \times 12$.

```pseudo id=main
DLT-RESECTION(X_1..X_n, x_1..x_n)
L1  if n < 6 then error "need at least 6 point pairs"
L2  T <- similarity: centroid of x_i to 0, mean distance sqrt(2)
L3  U <- similarity: centroid of X_i to 0, mean distance sqrt(3)
L4  x~_i <- T x_i ; X~_i <- U X_i             ▷ homogeneous
L5  for i <- 1 to n: add row (0^T, -w~_i X~_i^T, y~_i X~_i^T) to A
L6      add row (w~_i X~_i^T, 0^T, -x~_i X~_i^T) to A
L7  p <- unit right singular vector of A for the smallest singular value
L8  P~ <- rows p[1..4], p[5..8], p[9..12]
L9  P <- T^-1 P~ U
L10 P <- P / ||P||_F, negated if det P[:, 1..3] < 0
L11 return P
```

Lines L2 to L4 are the normalization of Hartley (1997), the step of the [Hartley normalization](/hartley-normalization/) page applied to both sets: the pixels move to centroid 0 and mean distance $\sqrt 2$, and the 3D points to centroid 0 and mean distance $\sqrt 3$, so that the average point is $(1, 1, 1)$ in size. The normalized data are exact data for the camera $T P U^{-1}$, and line L9 undoes the change. Lines L5 and L6 are the two equations above. Line L7 is the least squares solution of $A p = 0$ with $\|p\| = 1$. Line L10 fixes the scale and the sign, so that two runs can be compared entry by entry.

## Example

Take the camera with $f_x = f_y = 800$, principal point $(320, 240)$, $R = I$ and $t = (-0.5, -0.5, 5)$:
$$P_0 = \begin{pmatrix} 800 & 0 & 320 & 1200 \\ 0 & 800 & 240 & 800 \\ 0 & 0 & 1 & 5 \end{pmatrix}, \qquad \|P_0\|_F \approx 1876.17,$$
and six corners of a unit cube, not all on one plane.

| $X_i$ | $(0,0,0)$ | $(1,0,0)$ | $(0,1,0)$ | $(0,0,1)$ | $(1,1,0)$ | $(1,0,1)$ |
|---|---|---|---|---|---|---|
| $x_i$ | $(240, 160)$ | $(400, 160)$ | $(240, 320)$ | $(253.333, 173.333)$ | $(400, 320)$ | $(386.667, 173.333)$ |

| line | value |
|---|---|
| L2 | centroid of the pixels $(320, 217.78)$, scale $0.0137475$: $T$ has translation $(-4.3992, -2.9939)$ |
| L3 | centroid of the points $(0.5, 0.333, 0.333)$, scale $2.09333$ |
| L5, L6 | $A$ is $12 \times 12$; its smallest singular value is 0 up to rounding ($5 \cdot 10^{-19} s_1$) |
| L7 | the null vector, then L9 and L10 give the matrix below |

$$P = \begin{pmatrix} 0.4264 & 0 & 0.17056 & 0.6396 \\ 0 & 0.4264 & 0.12792 & 0.4264 \\ 0 & 0 & 0.000533 & 0.002665 \end{pmatrix} = \frac{P_0}{\|P_0\|_F}.$$

The effect of lines L2 to L4 shows in the singular values of $A$. On this example the ratio $s_1 / s_{11}$ of the largest to the smallest nonzero singular value is $8686.3$ for the raw data and $3.957$ after normalization. The raw matrix mixes entries near $1$ (the 3D coordinates) with entries near $10^5$ (pixel times pixel), and its [condition number](/condition-number/) grows with the size of the pixel values. This ratio is a measurement on this example only. In a test with 7 points and pixel noise of $\sigma = 1$, the two versions gave almost the same reprojection error; normalization protects against bad conditioning, but it does not make a well conditioned small problem better.

## Correctness

By the two rows above, $A p = 0$ holds exactly when every $P \mathbf{X}_i$ is a multiple of $\mathbf{x}_i$. So with exact data, the true $P_0$ is in the null space of $A$. If the configuration is not degenerate, the null space has dimension 1, and the unit singular vector of the zero singular value is $\pm P_0 / \|P_0\|_F$. The normalization maps the exact data for $P_0$ to exact data for $T P_0 U^{-1}$, and line L9 maps back. Line L10 picks the sign with $\det M > 0$. With noise, the singular vector minimizes $\|A p\|$ over unit vectors, which is the algebraic error, not the reprojection error. The full proof is in the proof file below.

Degenerate configurations (HZ sections 7.1 and 22.1): all points on one plane, where every $P_0 + a\, \mathbf{n}^{\mathsf T}$ fits as well and the null space has dimension at least 4; the camera center and the points on one twisted cubic; and the points on the union of a plane and one line through the camera center.

## Complexity

The model is the [floating-point model](/floating-point-model/), because the page is about conditioning; the operation counts are the same in the real RAM. Lines L2 to L6 cost $\Theta(n)$. Line L7 is the SVD of a $2n \times 12$ matrix. One-sided Jacobi, as in the reference code, costs $\Theta(n)$ per sweep, and a fixed number of sweeps is enough for full precision in practice; a Householder bidiagonalization costs $\Theta(n \cdot 12^2) = \Theta(n)$ with no iteration in $n$. Lines L8 to L11 are $\Theta(1)$. So the time is $\Theta(n)$, which is optimal, since each pair must be read. The extra space is $\Theta(n)$ for $A$; it drops to $\Theta(1)$ if one accumulates the $12 \times 12$ matrix $A^{\mathsf T} A$ and takes its smallest eigenvector, at the price of squaring the condition number.

## Properties

- **Exact on exact data.** Without noise, and outside the degenerate configurations, the output is the true camera up to scale.
- **Not invariant without normalization.** The algebraic error depends on the coordinate frames of the image and of the world. With the normalization of lines L2 to L4, the result does not depend on a similarity of the input frames.
- **Algebraic, not geometric.** With noise, the answer minimizes $\|A p\|$. It is not the maximum likelihood estimate, which minimizes the [reprojection error](/reprojection-error/) under Gaussian pixel noise.
- **No constraints.** The result has 11 free parameters. It does not force zero skew or square pixels, so with noise its $K$ has a small skew.

## Variants and improvements

- **Gold standard algorithm** (HZ Algorithm 7.1). Use the normalized DLT as a start, then minimize the reprojection error $\sum_i d(x_i, P \mathbf{X}_i)^2$ over $P$ with [Levenberg-Marquardt](/levenberg-marquardt/). This is the maximum likelihood estimate when the 3D points are exact and the pixel noise is Gaussian.
- **Inhomogeneous solution.** Fix $p_{34} = 1$ and solve 11 equations by least squares. With 6 points and 11 of the 12 equations, this is the minimal solution; the reference tests use it as an independent check. It fails when the true $p_{34}$ is 0, that is, when the world origin lies on the principal plane of the camera.
- **Restricted cameras.** If $K$ is partly known (zero skew, square pixels), fit those parameters by minimizing the reprojection error over the restricted set, starting from the DLT (HZ chapter 7). If $K$ is fully known, solve the [perspective-n-point](/perspective-n-point/) problem instead.
- **Radial distortion.** Fit a distortion model jointly in the geometric refinement (HZ chapter 7), or use [Tsai's method](/tsai-calibration-method/), whose first stage is not affected by radial distortion.
- **Lines.** A 3D line and its image line $\mathbf{l}$ give two equations $\mathbf{l}^{\mathsf T} P \mathbf{X} = 0$, one for each of two points $\mathbf{X}$ on the 3D line. They can be stacked into $A$ with the point rows.

## When to use it

Use the DLT when you have a 3D calibration target, or any set of known 3D points that are not on one plane, and you do not know $K$: it gives $P$ and, through [camera matrix decomposition](/camera-matrix-decomposition/), $K$, $R$ and $t$, with no starting guess. Use it as the start of a geometric refinement whenever accuracy matters. With a flat target, use [Zhang's method](/zhang-calibration-method/). With known $K$, use a PnP solver, which needs fewer points and fits fewer unknowns. With strong lens distortion, add a distortion model, since the DLT assumes a pinhole camera.

## Pitfalls

- **No normalization.** With raw pixel values of a few hundred and world coordinates of size 1, the entries of $A$ differ by a factor near $10^5$, and the result can lose many digits. Always apply lines L2 to L4 and undo them in L9.
- **Coplanar points.** A planar target gives a null space of dimension at least 4, and the SVD returns an arbitrary member. Test the ratio of the second smallest to the largest singular value, and use a homography based method for planar data.
- **Few points near the minimum.** With 6 or 7 points, the result follows the noise closely, and the principal point can be far off. Use many points spread over the image and over a range of depths.
- **The sign.** The SVD returns $p$ or $-p$. Without line L10, half of the results have $\det M < 0$, and a decomposition without a sign fix then gives a reflection.
- **Equation choice.** Using the third row of $\mathbf{x} \times P \mathbf{X}$ instead of one of the first two fails for points with $w_i = 0$ and adds nothing otherwise. Keep the two rows of lines L5 and L6.
- **Pixel convention.** Mixing pixel centers at $u$ with pixel centers at $u + 0.5$ moves the principal point by half a pixel.

## Implementations

## History

Abdel-Aziz and Karara presented the direct linear transformation at the ASP Symposium on Close-Range Photogrammetry in 1971, as a linear model with 11 parameters from object space to the coordinates measured on a photograph, which needs no starting values. It became a standard tool of close-range photogrammetry, and computer vision adopted it as the basic linear method for the camera matrix. Hartley (1997) explained the poor accuracy of the raw linear methods by the condition of the system and showed that a simple normalization of the data fixes it. Hartley and Zisserman (2000, second edition 2004) present the normalized DLT followed by a fit of the geometric error as the gold standard algorithm.

## References
