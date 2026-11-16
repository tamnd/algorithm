---
tag: 109XFG
kind: problem
slug: point-triangulation
name: Point triangulation
aliases:
- multiview triangulation
- structure computation
area: computer-vision/multiple-view-geometry
level: core
summary: "Find the 3D point whose projections best match its observed image points in two or more views with known cameras."
prereqs: [camera-projection-matrix, homogeneous-coordinates, reprojection-error]
see_also: [linear-triangulation, midpoint-triangulation, optimal-triangulation, perspective-n-point, relative-pose-problem, bundle-adjustment, cheirality, incremental-structure-from-motion]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Chapter 12, Structure computation"
  - paper: doi:10.1006/cviu.1997.0547
    title: "Richard I. Hartley and Peter Sturm, Triangulation, Computer Vision and Image Understanding 68(2), 1997, 146-157"
    locator: the statement of the problem, projective invariance and the comparison of the linear, midpoint and optimal methods
  - url: https://arxiv.org/abs/1907.11917
    title: "Seong Hun Lee and Javier Civera, Triangulation: Why Optimize?, British Machine Vision Conference (BMVC), 2019"
    locator: the comparison of midpoint variants with optimal methods in 3D and 2D error
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 11.2.4, Triangulation"
---

Point triangulation is the problem of finding a 3D point from its images in two or more views whose [camera matrices](/camera-projection-matrix/) $P_1, \ldots, P_m$ are known. Each image point $\mathbf{x}_i$ defines a ray from the camera center, and the point lies where the rays meet. With noise the rays do not meet, so the problem needs a cost: the [reprojection error](/reprojection-error/), a distance in space, or an algebraic residual. The [linear method](/linear-triangulation/) is fast and works in any number of views, the [midpoint method](/midpoint-triangulation/) is the simplest in a Euclidean frame, and the [optimal method](/optimal-triangulation/) of Hartley and Sturm gives the least reprojection error in two views exactly. Triangulation is the step that turns matched image points into a 3D point cloud in [structure from motion](/incremental-structure-from-motion/).

## In plain words

Two cameras look at the same point from different places. For each camera you know where it stands and where it points. In each photo, the point appears at some spot, and that spot tells you a line from the camera on which the point must lie. Where the two lines cross is the point in space. Because the photos are never perfect, the lines usually miss each other a little. So you have to choose a best point near both lines, and there are several ways to define what best means.

## Definition

**Input.** Camera matrices $P_1, \ldots, P_m$, $m \ge 2$, with distinct centers, and image points $\mathbf{x}_1, \ldots, \mathbf{x}_m$ that are images of one scene point.

**Output.** A point $\mathbf{X}$, in [homogeneous coordinates](/homogeneous-coordinates/), with $\mathbf{x}_i \sim P_i\mathbf{X}$ for all $i$ on exact data. With noise, the output minimizes a chosen cost:

- **Reprojection error.** $\sum_i d(\mathbf{x}_i, P_i\mathbf{X})^2$, the sum of squared image distances. Under independent isotropic Gaussian image noise this is the [maximum likelihood estimate](/maximum-likelihood-estimation/). It depends only on the images, so it gives the same answer in any projective frame.
- **Algebraic error.** $\sum_i \|\mathbf{x}_i \times P_i\mathbf{X}\|^2$ with $\|\mathbf{X}\| = 1$, a linear [least squares problem](/least-squares-problem/); see [linear triangulation](/linear-triangulation/).
- **Distance to the rays.** The sum of the squared distances from $\mathbf{X}$ to the back-projected rays; for two rays the answer is the midpoint of their common perpendicular. It needs a Euclidean frame.
- **Largest error.** The maximum over $i$ of the reprojection error, the $L_\infty$ cost, which can be minimized globally.

**Positive depth.** On exact data with distinct centers the rays meet in one point, unless the point lies on the line through two centers. A valid point should also lie in front of the cameras, see [cheirality](/cheirality/).

## Variants

- **Two views.** The epipolar constraint makes the problem one-dimensional, and the minimum of the reprojection error can be found exactly from a polynomial of degree 6.
- **Many views.** The reprojection error has many local minima in general, and the usual approach is a linear start followed by a few [Gauss-Newton](/gauss-newton-algorithm/) or [Levenberg-Marquardt](/levenberg-marquardt/) steps.
- **Calibrated cameras.** With known intrinsic matrices, the problem can be posed with normalized points $K_i^{-1}\mathbf{x}_i$, or with angles between rays, which is the setting of the midpoint methods.
- **Projective cameras.** In a [projective reconstruction](/projective-reconstruction-theorem/) only methods that are projective invariant, such as the optimal method and the reprojection error in general, give meaningful results.
- **Lines and other features.** Lines, conics and planes can be triangulated from their images in the same way.
- **Dense triangulation.** In stereo, each pixel match of a [stereo matcher](/stereo-matching/) is triangulated, often by the simple depth formula of a rectified pair.

## Examples

**Exact data.** Take $P_1 = [I \mid \mathbf{0}]$ and $P_2 = [I \mid (-1, 0, 0)^{\mathsf T}]$, a sideways step of 1. The point $(1, 2, 4)$ has the images $(0.25, 0.5)$ and $(0, 0.5)$, and every method returns $(1, 2, 4)$.

**Noisy data.** Move the second image to $(0, 0.52)$. The rays no longer meet, and the methods differ:

| method | point | reprojection error |
|---|---|---|
| [linear](/linear-triangulation/) | $(0.9999, 2.0393, 3.9983)$ | $2.00009 \times 10^{-4}$ |
| [midpoint](/midpoint-triangulation/) | $(0.9975, 2.0213, 3.9637)$ | $2.032 \times 10^{-4}$ |
| [optimal](/optimal-triangulation/) | $(1, 2.04, 4)$ | $2 \times 10^{-4}$ |

The optimal method moves both images to the height $0.51$, which is the least change that makes the rays meet.

**Non-example.** If the scene point lies on the baseline, the line through the two camera centers, both rays are the baseline, and the point is not determined.

## Known algorithms

| algorithm | views | cost | notes |
|---|---|---|---|
| [linear triangulation](/linear-triangulation/) | 2 or more | algebraic | one SVD of a $2m \times 4$ matrix; not projective invariant |
| [midpoint triangulation](/midpoint-triangulation/) | 2 or more | distance to the rays | closed form; needs a Euclidean frame |
| [optimal triangulation](/optimal-triangulation/) | 2 | reprojection error | global minimum from a polynomial of degree 6 |
| nonlinear refinement | 2 or more | reprojection error | Gauss-Newton from a linear start; local minimum |
| [bundle adjustment](/bundle-adjustment/) | 2 or more | reprojection error | refines the points and the cameras together |

## Bounds

- **Degrees of freedom.** A point has 3 degrees of freedom and each view gives 2 equations, so two views give one more equation than needed: the epipolar constraint, which noisy data does not satisfy.
- **Time.** Each view must be read, so $\Omega(m)$ time is needed, and the linear and midpoint methods reach $\Theta(m)$. The two-view optimal method takes constant time.
- **Local minima.** For two views the reprojection error can have more than one local minimum, but its stationary points are among the roots of a polynomial of degree 6, so all of them can be checked. For more views the number of stationary points grows quickly with $m$, and exact global methods are expensive.
- **Accuracy.** The error of the point grows with the depth and falls with the angle between the rays. With a small angle, a small image error moves the point a long way along the rays.

## Reductions

- **Two views to a polynomial.** The two-view reprojection error reduces to one unknown over the pencil of epipolar lines, and then to the real roots of a polynomial of degree 6; see [optimal triangulation](/optimal-triangulation/).
- **To least squares.** The algebraic cost is a homogeneous linear least squares problem, solved by the [singular value decomposition](/singular-value-decomposition/).
- **Dual of PnP.** Triangulation finds a point from known cameras; [perspective-n-point](/perspective-n-point/) finds a camera from known points. [Bundle adjustment](/bundle-adjustment/) solves both at once.
- **From relative pose.** After [relative pose](/relative-pose-problem/), the scene follows by triangulation, up to the global scale.

## Applications

- **Structure from motion.** Each new match in [incremental structure from motion](/incremental-structure-from-motion/) adds a point by triangulation, which bundle adjustment then refines.
- **Stereo depth.** Every pixel match in a calibrated stereo pair is triangulated into a depth.
- **Pose selection.** The four poses from an [essential matrix](/essential-matrix-decomposition/) are told apart by triangulating a point and checking its depth.
- **Motion capture and metrology.** Markers seen by several calibrated cameras are triangulated to measure positions.

## References
