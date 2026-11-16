---
tag: CE8KQ1
kind: problem
slug: perspective-n-point
name: Perspective-n-point
aliases:
- PnP
- absolute pose problem
- camera pose estimation
area: computer-vision/multiple-view-geometry
level: core
summary: "Find the pose of a calibrated camera from n known 3D points and their image projections."
prereqs: [camera-projection-matrix, camera-intrinsic-matrix, rigid-body-transformation]
see_also: [p3p, epnp, dlt-camera-resectioning, relative-pose-problem, ransac, minimal-solver, reprojection-error, incremental-structure-from-motion]
sources:
  - paper: doi:10.1145/358669.358692
    title: "Martin A. Fischler and Robert C. Bolles, Random sample consensus, a paradigm for model fitting with applications to image analysis and automated cartography, Communications of the ACM 24(6), 1981, 381-395"
    locator: the location determination problem, its minimal case with three points, and its solution inside RANSAC
  - paper: doi:10.1007/BF02028352
    title: "Robert M. Haralick, Chung-Nan Lee, Karsten Ottenberg and Michael Nolle, Review and analysis of solutions of the three point perspective pose estimation problem, International Journal of Computer Vision 13(3), 1994, 331-356"
    locator: the review of the classical three-point solutions and their numerical stability
  - paper: doi:10.1007/s11263-008-0152-6
    title: "Vincent Lepetit, Francesc Moreno-Noguer and Pascal Fua, EPnP: An Accurate O(n) Solution to the PnP Problem, International Journal of Computer Vision 81(2), 2009, 155-166"
    locator: the problem for n points, the survey of earlier methods and the linear-time solution
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 11.2, Pose estimation"
---

The perspective-n-point problem (PnP) asks for the position and orientation of a camera with known [intrinsic matrix](/camera-intrinsic-matrix/) $K$, given $n$ points $\mathbf{X}_i$ whose coordinates are known in a world frame and their images $\mathbf{x}_i$. The answer is a [rigid motion](/rigid-body-transformation/) $(R, \mathbf{t})$, so that $\mathbf{X}_c = R\mathbf{X}_i + \mathbf{t}$ is the point in the camera frame and $\mathbf{x}_i \sim K(R\mathbf{X}_i + \mathbf{t})$. The pose has 6 degrees of freedom and each point gives 2 equations, so three points are the minimum. Three points give up to four poses, solved by [P3P](/p3p/); more points fix the pose and average the noise, as in [EPnP](/epnp/). With wrong matches, a minimal solver runs inside [RANSAC](/ransac/), and the best pose is refined by minimizing the [reprojection error](/reprojection-error/). If $K$ is not known, the problem becomes [camera resectioning](/dlt-camera-resectioning/).

## In plain words

You have a photo, and you know where some objects in it are in the real world, for example the corners of a building on a map. You also know the lens of the camera. You want to know where the camera stood and in which direction it pointed. Each known point seen in the photo gives a line of sight that must pass through it. Three points are enough to fix the camera, but they can allow up to four answers. A fourth point usually tells which answer is right. With many points, small errors in the photo matter less.

## Definition

**Input.** World points $\mathbf{X}_1, \ldots, \mathbf{X}_n \in \mathbb{R}^3$, their image points $\mathbf{x}_i$, and the intrinsic matrix $K$. Then the normalized image points $\mathbf{y}_i = K^{-1}\mathbf{x}_i$ are known. Some matches may be wrong.

**Output.** A rotation $R \in SO(3)$ and a translation $\mathbf{t} \in \mathbb{R}^3$ such that each correct match satisfies $\mathbf{y}_i \sim R\mathbf{X}_i + \mathbf{t}$ with positive depth $(R\mathbf{X}_i + \mathbf{t})_3 > 0$. The camera center is $C = -R^{\mathsf T}\mathbf{t}$. With noise, the output minimizes a chosen cost:

- **Reprojection error.** $\sum_i d(\mathbf{x}_i, K\pi(R\mathbf{X}_i + \mathbf{t}))^2$, where $\pi(X, Y, Z) = (X/Z, Y/Z)$. Under independent Gaussian image noise this is the [maximum likelihood estimate](/maximum-likelihood-estimation/).
- **Object space error.** The sum of the squared distances from $R\mathbf{X}_i + \mathbf{t}$ to the ray of $\mathbf{y}_i$. It has no image meaning, but it treats near and far points alike and gives simpler algebra.
- **Algebraic error.** A linear residual such as $\mathbf{y}_i \times (R\mathbf{X}_i + \mathbf{t})$, used to get a starting pose.

**Ambiguities.** Unlike [relative pose](/relative-pose-problem/), there is no free scale: the world points fix the units. For $n = 3$ several poses fit exactly, and positive depth is part of the problem.

## Variants

- **Minimal case, P3P.** $n = 3$ gives a polynomial of degree 4 and up to four poses; see [P3P](/p3p/).
- **Planar scenes.** If all points lie on one plane, the image of the plane is a [homography](/homography/) $H \sim K[\mathbf{r}_1\ \mathbf{r}_2\ \mathbf{t}]$, and four points in general position on the plane give the pose by [homography decomposition](/homography-decomposition/).
- **Unknown focal length.** With only the focal length unknown, the problem has 7 unknowns and needs four points.
- **Unknown calibration.** With $K$ fully unknown, the $3 \times 4$ matrix $P = K[R \mid \mathbf{t}]$ has 11 degrees of freedom and six points are needed; see [DLT camera resectioning](/dlt-camera-resectioning/) and [camera matrix decomposition](/camera-matrix-decomposition/).
- **Generalized cameras.** Rays that do not pass through one center, as in a multi-camera rig, give the generalized pose problem; see [generalized camera model](/generalized-camera-model/).
- **Lines and points.** Known 3D lines and their images give more equations and can replace points.
- **Known rotation.** If $R$ is known, for example from an inertial sensor, each point gives two linear equations in $\mathbf{t}$, and two points are enough.

## Examples

**Two poses from three points.** Take the world points $(0, 0, 0)$, $(1, 0, 0)$ and $(0, 1, 0)$, and the camera $R = I$, $\mathbf{t} = (0.5, -0.3, 4)$. The normalized images are $(0.125, -0.075)$, $(0.375, -0.075)$ and $(0.125, 0.175)$. P3P finds two poses with positive depths: the true one, with depths $(4, 4, 4)$, and a second one, turned by about $44$ degrees, with $\mathbf{t} = (0.4906, -0.2944, 3.9248)$ and depths $(3.9248, 3.2356, 4.0107)$. Both fit the three images exactly.

**A fourth point decides.** The point $(1, 1, 1)$ has the image $(0.3, 0.14)$ under the true pose and $(0.4739, 0.1693)$ under the second one, so its observed image selects the true pose.

**Non-example.** If all points lie on one line, every rotation about that line fits as well as any other, and the pose is not determined.

## Known algorithms

| algorithm | points | output | notes |
|---|---|---|---|
| [P3P](/p3p/), Grunert's method and its variants | 3 | up to 4 poses | minimal; used inside RANSAC; a fourth point selects |
| [EPnP](/epnp/) | 4 or more | one pose | $\Theta(n)$ time; four virtual control points |
| [DLT camera resectioning](/dlt-camera-resectioning/) | 6 or more | $P$, then $K$, $R$, $\mathbf{t}$ | does not use the known $K$; linear |
| [homography decomposition](/homography-decomposition/) | 4 or more on a plane | one pose | for planar targets |
| nonlinear refinement | all inliers | one pose | [Levenberg-Marquardt](/levenberg-marquardt/) on the reprojection error, from any of the above |

The usual pipeline is: match image features to known 3D points, run P3P inside RANSAC to find the inliers, compute EPnP on the inliers, and refine with Levenberg-Marquardt on the reprojection error.

## Bounds

- **Degrees of freedom.** 3 for $R$ and 3 for $\mathbf{t}$, so 6. Each point gives 2 equations, so 3 points are the minimum.
- **Number of solutions.** Three points not on a line give at most four poses with positive depths, the real positive roots of a quartic; up to four can occur.
- **Uniqueness.** Four or more points on a plane, no three on a line, give a unique pose. Six or more points in general position give a unique pose by the linear method, even without $K$.
- **Time.** Any method must read the $n$ points, so $\Omega(n)$ time is needed. EPnP reaches $\Theta(n)$; the minimal solvers take constant time.
- **Degenerate cases.** Points on a line never fix the pose. For three points, poses near the danger cylinder, the cylinder through the three points perpendicular to their plane, are unstable, because two solutions meet there.

## Reductions

- **To absolute orientation.** Once the depths of the points are known, the camera frame coordinates $R\mathbf{X}_i + \mathbf{t}$ are known, and $(R, \mathbf{t})$ follows by aligning two point sets, the [Kabsch algorithm](/kabsch-algorithm/), a form of [Wahba's problem](/wahba-problem/). P3P and EPnP both end this way.
- **From resectioning.** With $K$ known, a camera matrix $P$ from [DLT resectioning](/dlt-camera-resectioning/) gives $K^{-1}P \sim [R \mid \mathbf{t}]$, but the left $3 \times 3$ block must then be forced to be a rotation.
- **Dual of triangulation.** [Point triangulation](/point-triangulation/) finds a point from known cameras; PnP finds a camera from known points. [Bundle adjustment](/bundle-adjustment/) refines both.
- **Relation to relative pose.** [Relative pose](/relative-pose-problem/) works from 2D to 2D matches and leaves the scale free; PnP works from 3D to 2D matches and fixes it.

## Applications

- **Structure from motion.** Each new image in [incremental structure from motion](/incremental-structure-from-motion/) is registered by PnP against the points already reconstructed.
- **Visual odometry and SLAM.** Tracking the camera against a local map, as in [visual odometry](/visual-odometry/).
- **Calibration.** The pose of a calibration target in each image, as in [Zhang's calibration method](/zhang-calibration-method/), is a planar PnP problem.
- **Augmented reality and robotics.** Placing virtual objects on a known marker, or finding the pose of a known object for a robot to grasp.
- **Localization.** Finding where a photo was taken from matches with a 3D model of a place.

## References
