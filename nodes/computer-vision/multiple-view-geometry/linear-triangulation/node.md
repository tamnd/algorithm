---
tag: 8H0B6Z
kind: algorithm
slug: linear-triangulation
name: Linear triangulation
aliases:
- DLT triangulation
- homogeneous triangulation
area: computer-vision/multiple-view-geometry
level: core
summary: "Stack the cross product equations x × PX = 0 of all views and take X as the singular vector of least singular value."
solves: [point-triangulation]
model: real-ram
complexity:
  vars: {m: "the number of views, at least 2"}
  time: {worst: Θ(m), average: Θ(m), best: Θ(m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1997
  people: [Richard Hartley, Peter Sturm]
  note: The linear method follows the direct linear transformation of photogrammetry. Hartley and Sturm described and compared its homogeneous and inhomogeneous forms in their 1997 study of triangulation.
prereqs: [point-triangulation, camera-projection-matrix, singular-value-decomposition]
see_also: [optimal-triangulation, midpoint-triangulation, dlt-camera-resectioning, hartley-normalization, reprojection-error, bundle-adjustment, algebraic-and-geometric-error, homogeneous-coordinates]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 12.2, Linear triangulation methods"
  - paper: doi:10.1006/cviu.1997.0547
    title: "Richard I. Hartley and Peter Sturm, Triangulation, Computer Vision and Image Understanding 68(2), 1997, 146-157"
    locator: the linear methods, their lack of projective invariance and the comparison with the optimal method
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 11.2.4, Triangulation"
---

Linear triangulation finds a 3D point from its images in two or more views with known [camera matrices](/camera-projection-matrix/). Each view says that the image point $\mathbf{x}_i$ and the projection $P_i\mathbf{X}$ are the same point of the image, so their cross product is zero. That gives two independent linear equations in the [homogeneous](/homogeneous-coordinates/) point $\mathbf{X}$. The equations of all views form a system $A\mathbf{X} = \mathbf{0}$ with a $2m \times 4$ matrix. On exact data $A$ has rank 3, and $\mathbf{X}$ is its null vector. On noisy data the method takes the unit vector that minimizes $\|A\mathbf{X}\|$, the right [singular vector](/singular-value-decomposition/) of the smallest singular value. This is the direct linear transformation (DLT) idea, the same one used for [camera resectioning](/dlt-camera-resectioning/). It is fast and works for any number of views, but the quantity it minimizes has no geometric meaning. It is the usual first step before [optimal triangulation](/optimal-triangulation/) or [bundle adjustment](/bundle-adjustment/).

## In plain words

Each photo of a point tells you a line in space on which the point must lie: the line from the camera through the dot in the photo. With two or more photos, the point is where these lines meet. The method writes "the point lies on this line" as two simple equations for each photo, puts all equations in one table, and asks for the point that comes closest to satisfying all of them. A standard matrix tool answers this in one step. When the photos are perfect, the answer is exact. When the dots are a little off, the lines do not meet, and the answer is a good guess, but not the best possible one.

## The problem

**Input.** Camera matrices $P_1, \ldots, P_m$, $m \ge 2$, each $3 \times 4$, and image points $\mathbf{x}_i = (u_i, v_i)$ in the same units as $P_i$ (pixels for $P = K[R \mid \mathbf{t}]$).

**Output.** A 3D point $\mathbf{X}$. If the image points are exact images of a finite point that is not on the line through two of the centers, the output is that point.

## The algorithm

Write $\mathbf{p}_i^{k\mathsf T}$ for row $k$ of $P_i$. The cross product $\tilde{\mathbf{x}}_i \times P_i\mathbf{X} = \mathbf{0}$, with $\tilde{\mathbf{x}}_i = (u_i, v_i, 1)$, has three entries, of which two are independent:
$$(u_i\mathbf{p}_i^{3\mathsf T} - \mathbf{p}_i^{1\mathsf T})\mathbf{X} = 0, \qquad (v_i\mathbf{p}_i^{3\mathsf T} - \mathbf{p}_i^{2\mathsf T})\mathbf{X} = 0 .$$

```pseudo id=main
LINEAR-TRIANGULATION(P_1 .. P_m, x_1 .. x_m)
L1  A <- an empty matrix with 4 columns
L2  for each view i, with x_i = (u_i, v_i)
L3      append the rows u_i p_i^3T - p_i^1T and v_i p_i^3T - p_i^2T to A
L4  X <- the unit vector that minimizes || A X ||, the last right singular vector of A
L5  if X_4 = 0 then report a point at infinity
L6  return (X_1, X_2, X_3) / X_4
```

The inhomogeneous variant sets $X_4 = 1$ and solves the $2m \times 3$ linear least squares problem $\min\|M\mathbf{z} + \mathbf{a}_4\|$, where $M$ is the first three columns of $A$ and $\mathbf{a}_4$ the last one. The code on this page has both. On exact data they give the same point.

## Example

Take $P_1 = [I \mid \mathbf{0}]$ and $P_2 = [I \mid (-1, 0, 0)^{\mathsf T}]$, two cameras with $K = I$ and centers $(0, 0, 0)$ and $(1, 0, 0)$. The point $\mathbf{X} = (1, 2, 4)$ has the images $(0.25, 0.5)$ and $(0, 0.5)$.

| line | value |
|---|---|
| L3, view 1 | rows $(-1, 0, 0.25, 0)$ and $(0, -1, 0.5, 0)$ |
| L3, view 2 | rows $(-1, 0, 0, 1)$ and $(0, -1, 0.5, 0)$ |
| L4 | singular values $1.6391$, $1.5684$, $0.6451$, $0$; null vector $0.2132\,(1, 2, 4, 1)$ |
| L6 | $(1, 2, 4)$ |

Now move the second image point to $(0, 0.52)$, so that the two rays no longer meet. The smallest singular value becomes $0.0120$, and line L6 gives $(0.9999, 2.0393, 3.9983)$. The inhomogeneous variant gives $(0.9968, 2.0270, 3.9746)$, a different point. If the world origin is moved by 10 along the $X$ axis and the cameras are changed to match, the inhomogeneous result moves with it, but the homogeneous result changes to $(0.9975, 2.0294, 3.9791)$ in the old frame.

## Correctness

For one view, the two rows vanish exactly on the vectors $\mathbf{Y}$ with $P_i\mathbf{Y}$ a multiple of $\tilde{\mathbf{x}}_i$. Because $P_i$ has rank 3, this set is the 2-dimensional subspace spanned by the camera center $\mathbf{C}_i$ and $\mathbf{X}$: the back-projected ray. Two such subspaces with independent $\mathbf{C}_1$, $\mathbf{C}_2$, $\mathbf{X}$ meet only in the multiples of $\mathbf{X}$. So on exact data the null space of $A$ is spanned by $\mathbf{X}$, the smallest singular value is 0 and simple, and line L4 returns $\pm\mathbf{X}/\|\mathbf{X}\|$. The full proof, with the inhomogeneous variant and the invariance facts, is in the proof file of this page.

## Complexity

Building $A$ takes $\Theta(m)$ time. The SVD of a $2m \times 4$ matrix costs $\Theta(m)$ per sweep of a Jacobi method, and a fixed number of sweeps is enough in practice; with $A^{\mathsf T}A$ formed first, the work is $\Theta(m)$ plus the eigenvectors of one $4 \times 4$ matrix. The extra space is $\Theta(m)$ for $A$, or $\Theta(1)$ if only $A^{\mathsf T}A$ is kept. In the real RAM model the SVD of a fixed number of columns counts as $\Theta(m)$.

## Properties

- **Exact on exact data.** The true point is the null vector whenever the rays meet at one finite point, off the line through two centers.
- **Any number of views.** Each view adds two rows; more views reduce the effect of noise.
- **Not projective invariant.** The homogeneous method depends on the choice of the world frame. It is invariant under rotations of the world about its origin, but not under translations.
- **Affine invariant variant.** The inhomogeneous method gives the same point after any affine change of the world frame. It cannot represent a point at infinity.
- **Algebraic error.** The minimized quantity $\|A\mathbf{X}\|$ is an [algebraic error](/algebraic-and-geometric-error/), not the [reprojection error](/reprojection-error/), so the result is not the maximum likelihood estimate under Gaussian noise.

## Variants and improvements

- **Normalized coordinates.** Run the method on $\mathbf{y} = K^{-1}\mathbf{x}$ with $[R \mid \mathbf{t}]$, or apply [Hartley normalization](/hartley-normalization/) to the image points. This improves the conditioning of $A$ when the inputs are in pixels.
- **Row weights.** Dividing the two rows of a view by the depth $\mathbf{p}_i^{3\mathsf T}\mathbf{X}$ of the current estimate and solving again turns the algebraic error into the reprojection error step by step; this is an iteratively reweighted form of the method.
- **Optimal two-view method.** [Optimal triangulation](/optimal-triangulation/) corrects the two image points first and then triangulates exactly; it minimizes the reprojection error.
- **Midpoint.** The [midpoint method](/midpoint-triangulation/) works in a Euclidean frame and takes the point closest to the rays.
- **Refinement.** A few Gauss-Newton steps on the reprojection error, starting from the linear result, give the maximum likelihood estimate in most cases.

## When to use it

Use it as the default first estimate of a point in structure from motion, both for two views and for many, when the cameras are known. In a projective reconstruction, where there is no Euclidean frame, it is the natural choice. When accuracy matters, refine the result on the reprojection error, either point by point or in a full bundle adjustment.

## Pitfalls

- **Pixels with a large offset.** With $u$ and $v$ near 1000, the rows of $A$ have entries of very different size. Normalize the image points first.
- **Points at infinity.** Far points or nearly parallel rays give $X_4$ close to 0; dividing by it gives very large coordinates. Keep the homogeneous vector, or reject the point.
- **Small baseline.** When the angle between the rays is small, the depth is poorly fixed; the smallest two singular values of $A$ come close.
- **No cheirality check.** The method can return a point behind a camera. Check the sign of the depth in each view with the [cheirality](/cheirality/) test.
- **Treating it as optimal.** Its result differs from the minimum of the reprojection error under noise, and the difference depends on the world frame.

## Implementations

## History

The linear method applies the direct linear transformation, a standard tool of photogrammetry, to the triangulation of a point. Hartley and Sturm (1997) described the homogeneous and the inhomogeneous linear methods, showed that neither is projective invariant and that the inhomogeneous one is affine invariant, and compared them with the midpoint method and their optimal method. Hartley and Zisserman present the two linear methods in Section 12.2 of their book.

## References
