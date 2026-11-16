---
tag: NVV9NG
kind: algorithm
slug: midpoint-triangulation
name: Midpoint triangulation
aliases:
- ray midpoint triangulation
area: computer-vision/multiple-view-geometry
level: intro
summary: "Take the midpoint of the shortest segment between the two back-projected rays; simple and fast, but not affine or projective invariant."
solves: [point-triangulation]
model: real-ram
complexity:
  vars: {N: "the number of rays in the N-view variant"}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1997
  people: [Richard Hartley, Peter Sturm]
  note: The point halfway between two skew lines is a classical construction. Hartley and Sturm included the midpoint method in their 1997 comparison of triangulation methods and showed that it is not projective invariant.
prereqs: [point-triangulation, rigid-body-transformation, camera-intrinsic-matrix]
see_also: [linear-triangulation, optimal-triangulation, reprojection-error, cheirality, generalized-camera-model, bundle-adjustment, incremental-structure-from-motion, essential-matrix-decomposition]
sources:
  - paper: doi:10.1006/cviu.1997.0547
    title: "Richard I. Hartley and Peter Sturm, Triangulation, Computer Vision and Image Understanding 68(2), 1997, 146-157"
    locator: the midpoint method and its comparison with the linear and optimal methods
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 11.2.4, Triangulation"
  - url: https://arxiv.org/abs/1907.11917
    title: "Seong Hun Lee and Javier Civera, Triangulation: Why Optimize?, British Machine Vision Conference (BMVC), 2019"
    locator: the weighted midpoint methods for two views
---

Midpoint triangulation finds a 3D point from two calibrated views. Each image point defines a ray in space, from the camera center through the point on the image plane. With exact data the two rays meet at the point. With noisy data they usually miss each other, and the method takes the shortest segment between them and returns its middle. The two ends of the segment follow from a $2 \times 2$ linear system, so the cost is a fixed small number of operations. The method needs a Euclidean frame: it uses lengths and right angles, so it works with [calibrated](/camera-intrinsic-matrix/) cameras in a metric reconstruction, not in a projective one. It is the simplest triangulation method, and it extends at once to many rays and to [generalized cameras](/generalized-camera-model/).

## In plain words

A photo of a point tells you a line in space on which the point lies: the line from the camera through the dot in the photo. Two photos give two lines. If the dots were perfect, the lines would cross at the point. Real dots are a little off, so the lines pass near each other without touching. Find the two places where they come closest, one on each line, and take the spot halfway between them. That spot is the answer. It is easy to compute and easy to picture, but it measures errors in space and not in the photos, so it is not the most accurate choice.

## The problem

**Input.** Two rays $\mathbf{C}_1 + \lambda_1\mathbf{d}_1$ and $\mathbf{C}_2 + \lambda_2\mathbf{d}_2$ in a Euclidean frame. For a camera with $\mathbf{X}_c = R\mathbf{X}_w + \mathbf{t}$ and a normalized image point $\mathbf{y} = K^{-1}\mathbf{x} = (u, v, 1)$, the ray has the center $\mathbf{C} = -R^{\mathsf T}\mathbf{t}$ and the direction $\mathbf{d} = R^{\mathsf T}\mathbf{y}$.

**Output.** The point $\mathbf{M}$ that minimizes the sum of the squared distances to the two lines, and the parameters $\lambda_1$, $\lambda_2$ of the closest points. With $\mathbf{d} = R^{\mathsf T}\mathbf{y}$, the parameter $\lambda_i$ is the depth of the closest point in camera $i$.

## The algorithm

The closest points $\mathbf{Q}_1 = \mathbf{C}_1 + \lambda_1\mathbf{d}_1$ and $\mathbf{Q}_2 = \mathbf{C}_2 + \lambda_2\mathbf{d}_2$ are the ones for which $\mathbf{Q}_1 - \mathbf{Q}_2$ is perpendicular to both directions. These two conditions are a $2 \times 2$ linear system in $\lambda_1$, $\lambda_2$.

```pseudo id=main
MIDPOINT-TRIANGULATION(C_1, d_1, C_2, d_2)
L1  w <- C_1 - C_2
L2  a <- d_1.d_1;  b <- d_1.d_2;  c <- d_2.d_2;  d <- d_1.w;  e <- d_2.w
L3  D <- a c - b^2; if D <= eps a c then report parallel rays
L4  l_1 <- (b e - c d) / D;  l_2 <- (a e - b d) / D
L5  Q_1 <- C_1 + l_1 d_1;  Q_2 <- C_2 + l_2 d_2
L6  return (Q_1 + Q_2) / 2, l_1, l_2
```

The N-view variant returns the point with the least sum of squared distances to $N$ lines. With unit directions $\mathbf{u}_i$ it solves the $3 \times 3$ system $\sum_i (I - \mathbf{u}_i\mathbf{u}_i^{\mathsf T})\,\mathbf{X} = \sum_i (I - \mathbf{u}_i\mathbf{u}_i^{\mathsf T})\,\mathbf{C}_i$. For two rays this is the same point. The code on this page has both forms.

## Example

Take two cameras with $R = I$, the first at $(0, 0, 0)$ and the second at $(1, 0, 0)$, so $\mathbf{t}_2 = (-1, 0, 0)$. The point $(1, 2, 4)$ has the normalized images $(0.25, 0.5)$ and $(0, 0.5)$. Move the second image point to $(0, 0.52)$, so that the rays no longer meet.

| line | exact data | noisy data |
|---|---|---|
| L1 | $\mathbf{w} = (-1, 0, 0)$ | $\mathbf{w} = (-1, 0, 0)$ |
| L2 | $a = 1.3125$, $b = 1.25$, $c = 1.25$, $d = -0.25$, $e = 0$ | $a = 1.3125$, $b = 1.26$, $c = 1.2704$, $d = -0.25$, $e = 0$ |
| L3 | $D = 0.078125$ | $D = 0.0798$ |
| L4 | $\lambda_1 = 4$, $\lambda_2 = 4$ | $\lambda_1 = 3.9799$, $\lambda_2 = 3.9474$ |
| L5 | $\mathbf{Q}_1 = \mathbf{Q}_2 = (1, 2, 4)$ | $\mathbf{Q}_1 = (0.9950, 1.9900, 3.9799)$, $\mathbf{Q}_2 = (1, 2.0526, 3.9474)$ |
| L6 | $(1, 2, 4)$ | $(0.9975, 2.0213, 3.9637)$ |

On the noisy data the gap between the rays is $0.0708$. The output projects to $(0.2517, 0.5100)$ in the first view and $(-0.0006, 0.5100)$ in the second. On the same data [linear triangulation](/linear-triangulation/) gives $(0.9999, 2.0393, 3.9983)$, a different point.

## Correctness

The squared distance $\|\mathbf{w} + \lambda_1\mathbf{d}_1 - \lambda_2\mathbf{d}_2\|^2$ between two points of the lines is a quadratic function of $(\lambda_1, \lambda_2)$ whose Hessian has determinant $4D$. By the Cauchy-Schwarz inequality $D > 0$ unless the directions are parallel, so the function has one minimizer, where its gradient is zero. The gradient condition says that $\mathbf{Q}_1 - \mathbf{Q}_2$ is perpendicular to $\mathbf{d}_1$ and $\mathbf{d}_2$, and Cramer's rule gives line L4. If a point has distances $r_1$, $r_2$ to the lines, the triangle inequality gives $r_1 + r_2 \ge \|\mathbf{Q}_1 - \mathbf{Q}_2\|$, so $r_1^2 + r_2^2 \ge \|\mathbf{Q}_1 - \mathbf{Q}_2\|^2/2$, with equality only at the midpoint. When the rays meet, the gap is zero and the output is the meeting point. The full proof is in the proof file of this page.

## Complexity

Two rays need a fixed number of dot products and one division by $D$: $\Theta(1)$ time and space. The N-view variant forms a $3 \times 3$ sum in $\Theta(N)$ time and solves it in $\Theta(1)$.

## Properties

- **Exact on exact data.** If the rays meet at one point, the output is that point.
- **Depths for free.** The parameters $\lambda_1$, $\lambda_2$ are the depths of the closest points; a negative value shows a point behind the camera.
- **Similarity invariant.** Rotating, moving or scaling the world frame moves the output in the same way.
- **Not affine or projective invariant.** An affine change of the frame does not keep right angles, so the common perpendicular, and with it the output, changes. On exact data the output is the meeting point in every frame.
- **Error in space.** The quantity it minimizes is a distance in 3D, not the [reprojection error](/reprojection-error/). A far point has a large gap for a small image error, and a near point a small one.

## Variants and improvements

- **N rays.** The least squares point of $N$ lines, as above, works for any number of views and for rays from a [generalized camera](/generalized-camera-model/).
- **Weighted midpoint.** Lee and Civera (2019) move the output along the segment in proportion to the depths of the two ends, instead of taking the middle. This brings the result closer to the optimum in the images, at the same cost.
- **Cheirality check.** Reject the point if $\lambda_1 \le 0$ or $\lambda_2 \le 0$. This test is part of choosing the right pose in [essential matrix decomposition](/essential-matrix-decomposition/).
- **Refinement.** A few Gauss-Newton steps on the reprojection error, starting from the midpoint, give the maximum likelihood estimate in most cases.

## When to use it

Use it when the cameras are calibrated and the frame is metric, and a quick first estimate is enough: for the [cheirality](/cheirality/) test of relative pose, for new points in [incremental structure from motion](/incremental-structure-from-motion/) that [bundle adjustment](/bundle-adjustment/) will refine, and for systems of many rays. In a projective reconstruction use [linear triangulation](/linear-triangulation/) instead. For the best two-view estimate under Gaussian image noise use [optimal triangulation](/optimal-triangulation/).

## Pitfalls

- **Pixels as directions.** The direction must be $R^{\mathsf T}K^{-1}\tilde{\mathbf{x}}$. Using pixel coordinates without $K^{-1}$ gives wrong rays.
- **Parallel rays.** For a far point or a small baseline, $D$ is close to 0 and the depths are poorly fixed. Reject such points, or keep only the direction.
- **Points behind a camera.** The lines extend in both directions, so the output can lie behind a camera. Check the signs of $\lambda_1$ and $\lambda_2$.
- **Projective frames.** In a frame that is only projective, distances and right angles have no meaning, and the output depends on the arbitrary choice of frame.

## Implementations

## History

The common perpendicular of two skew lines is a classical construction of solid geometry, and its midpoint is a natural way to intersect two rays that do not meet. Hartley and Sturm (1997) included the midpoint method in their study of triangulation, noted that it is not projective invariant, and found it less accurate than their optimal method in their tests. Lee and Civera (2019) returned to midpoint methods and proposed weighted forms that are closed form and accurate for small parallax.

## References
