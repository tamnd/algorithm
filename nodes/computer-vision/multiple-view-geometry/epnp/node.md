---
tag: ATAF9X
kind: algorithm
slug: epnp
name: EPnP
aliases:
- efficient perspective-n-point
area: computer-vision/multiple-view-geometry
level: advanced
summary: "Write each 3D point as a weighted sum of four control points and solve linearly for the control points in the camera frame, an O(n) solution of PnP."
solves: [perspective-n-point]
model: real-ram
complexity:
  vars: {n: "the number of point correspondences, at least 4"}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2007
  people: [Francesc Moreno-Noguer, Vincent Lepetit, Pascal Fua]
  note: Moreno-Noguer, Lepetit and Fua presented the method at ICCV 2007. The journal version by Lepetit, Moreno-Noguer and Fua (2009) named it EPnP and added the Gauss-Newton refinement.
prereqs: [perspective-n-point, camera-intrinsic-matrix, eigenvalue, kabsch-algorithm]
see_also: [p3p, dlt-camera-resectioning, ransac, reprojection-error, minimal-solver, bundle-adjustment, incremental-structure-from-motion, gauss-newton-algorithm]
sources:
  - paper: doi:10.1007/s11263-008-0152-6
    title: "Vincent Lepetit, Francesc Moreno-Noguer and Pascal Fua, EPnP: An Accurate O(n) Solution to the PnP Problem, International Journal of Computer Vision 81(2), 2009, 155-166"
    locator: the control points, the cases N = 1 to 4, the Gauss-Newton refinement and the planar case
  - paper: doi:10.1109/ICCV.2007.4409116
    title: "Francesc Moreno-Noguer, Vincent Lepetit and Pascal Fua, Accurate Non-Iterative O(n) Solution to the PnP Problem, IEEE International Conference on Computer Vision (ICCV), 2007"
    locator: the first version of the method
  - paper: doi:10.1109/CVPR.2014.71
    title: "Luis Ferraz, Xavier Binefa and Francesc Moreno-Noguer, Very Fast Solution to the PnP Problem with Algebraic Outlier Rejection, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2014"
    locator: a later variant that builds on the control point formulation
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 11.2, Pose estimation"
---

EPnP finds the pose of a calibrated camera from $n \ge 4$ known 3D points and their images, in time linear in $n$. It solves the [perspective-n-point](/perspective-n-point/) problem without an iterative search over the pose. The method chooses four control points in the world and writes each 3D point as a weighted sum of them, with weights that add up to 1. A rigid motion keeps these weights, so the same sums hold in the camera frame. The 12 unknown camera coordinates of the control points then satisfy a homogeneous linear system with two rows per point. Its solution is a combination of a few [eigenvectors](/eigenvalue/) of a $12 \times 12$ matrix, and the coefficients follow from the known distances between the control points. A rigid alignment of the world points with the recovered camera points gives the rotation and the translation. Because the work on the points is one pass to build a $12 \times 12$ matrix, EPnP is fast for large $n$, and it is a common choice inside [RANSAC](/ransac/) and as the first estimate before [bundle adjustment](/bundle-adjustment/).

## In plain words

You know where some points are in the room, and you see them in a photo. You want to know where the camera stood. Instead of finding the camera position directly, EPnP picks four helper points that frame the whole set, and describes every real point as a mix of the four helpers. That mix stays the same when you look from the camera. So it is enough to find where the four helpers are as seen from the camera: only twelve numbers. Each photo point gives two simple equations for them. Solve these, use the known distances between the helpers to fix the size, and then turn the result into a camera position and direction.

## The problem

**Input.** World points $\mathbf{X}_1, \ldots, \mathbf{X}_n$, $n \ge 4$, not all in one plane, and their normalized images $\mathbf{y}_i = (u_i, v_i) = K^{-1}\mathbf{x}_i$.

**Output.** A rotation $R$ and a translation $\mathbf{t}$ such that $\mathbf{X}_c = R\mathbf{X}_i + \mathbf{t}$ projects to $\mathbf{y}_i$ for every $i$, exactly on exact data and in the least squares sense of the method on noisy data.

## The algorithm

Line L1 takes the centroid $\mathbf{c}_1$ of the points and adds the three principal directions of the points, each scaled by the spread of the points along it, to get $\mathbf{c}_2$, $\mathbf{c}_3$, $\mathbf{c}_4$. Line L2 finds the weights $\alpha_{ij}$ with $\mathbf{X}_i = \sum_j \alpha_{ij}\mathbf{c}_j$ and $\sum_j \alpha_{ij} = 1$. In the camera frame $\mathbf{X}_{c,i} = \sum_j \alpha_{ij}\mathbf{c}^c_j$, and the projection equations $u_i Z = X$ and $v_i Z = Y$ become two linear equations in the 12 unknowns $\mathbf{x} = (\mathbf{c}^c_1, \ldots, \mathbf{c}^c_4)$.

```pseudo id=main
EPNP(X_1 .. X_n, y_1 .. y_n)
L1  c_1 <- centroid of the X_i; c_2, c_3, c_4 <- c_1 + scaled principal directions
L2  for each i: alpha_i <- weights with X_i = sum_j alpha_ij c_j and sum_j alpha_ij = 1
L3  M <- the 2n x 12 matrix with rows (alpha_ij, 0, -alpha_ij u_i) and (0, alpha_ij, -alpha_ij v_i), j = 1..4
L4  v_1 .. v_4 <- eigenvectors of M^T M for its 4 smallest eigenvalues
L5  rho_ab <- ||c_a - c_b||^2 for the 6 pairs of control points
L6  for N = 1, 2, 3: beta <- linearized solution of ||sum_k beta_k (v_k^[a] - v_k^[b])||^2 = rho_ab
L7      refine the four betas by Gauss-Newton on the same 6 equations
L8      c^c <- sum_k beta_k v_k; p_i <- sum_j alpha_ij c^c_j; negate all p_i if their mean depth is negative
L9      (R, t) <- rigid alignment of the X_i to the p_i
L10     e <- reprojection error of (R, t)
L11 return the (R, t) of least e
```

Here $\mathbf{v}_k^{[a]}$ is the 3-vector of control point $a$ in $\mathbf{v}_k$. For $N = 1$ the camera control points are $\beta\mathbf{v}_1$, and line L6 takes $\beta = \sum \|\mathbf{v}_1^{[a]} - \mathbf{v}_1^{[b]}\|\sqrt{\rho_{ab}} / \sum \|\mathbf{v}_1^{[a]} - \mathbf{v}_1^{[b]}\|^2$ over the 6 pairs. For $N = 2$ and $N = 3$ the 6 distance equations are linear in the products $\beta_k\beta_l$; line L6 solves them by least squares and reads $\beta_k$ from the squares, with the signs from the cross terms. Line L9 is the [Kabsch algorithm](/kabsch-algorithm/).

## Example

Take the six world points $(0, 0, 0)$, $(1, 0, 0)$, $(0, 1, 0)$, $(0, 0, 1)$, $(1, 1, 0.5)$, $(0.3, 0.7, 1.2)$ and the true pose $R = R_y(0.3)R_x(0.2)$, $\mathbf{t} = (0.2, -0.1, 4)$. The normalized images are $(0.05, -0.025)$, $(0.3119, -0.027)$, $(0.0617, 0.21)$, $(0.0992, -0.0605)$, $(0.3115, 0.179)$ and $(0.1694, 0.0673)$.

| line | value |
|---|---|
| L1 | $\mathbf{c}_1 = (0.3833, 0.45, 0.45)$, $\mathbf{c}_2 = (0.1991, 0.5398, 0.9183)$, $\mathbf{c}_3 = (0.6734, 0.8382, 0.4897)$, $\mathbf{c}_4 = (0.6719, 0.2182, 0.6080)$ |
| L2 | weights of the first point: $(3.4534, -0.6908, -1.2848, -0.4778)$ |
| L4 | the four smallest eigenvalues: about $10^{-16}$, $0.0359$, $0.0701$, $0.2361$ |
| L5 | $\rho = (0.2613, 0.2364, 0.1620, 0.4977, 0.4233, 0.3984)$ |
| L6, $N = 1$ | $\beta_1 = 9.2725$ |
| L7 | no change: the distance equations already hold |
| L9, L10 | $R$ and $\mathbf{t}$ equal the true pose to about $10^{-15}$; error $3.5 \times 10^{-16}$ |

Only one eigenvalue is near 0, so the case $N = 1$ already gives the pose. Now move the image points by up to $0.002$: point $i$ gets $(0.002\,(-1)^i, -0.001\,i/3)$, for $i = 0, \ldots, 5$. All three cases then end at the same betas after Gauss-Newton, the root mean square reprojection error is $0.0017$, the rotation is off by $0.0132$ rad, and $\mathbf{t} = (0.1997, -0.0953, 3.9948)$.

## Correctness

On exact data the true camera control points $R\mathbf{c}_j + \mathbf{t}$ satisfy $M\mathbf{x} = \mathbf{0}$, because the weights sum to 1 and so hold in every frame. If the null space of $M$ has dimension 1, the eigenvector of the eigenvalue 0 is a multiple of the true control points. Rigid motions keep distances, so the formula of the case $N = 1$ gives exactly the right scale, the sign follows from the positive depths, and the alignment gives the true pose with error 0. Any candidate with error 0 and positive depths has control points in the same null space, which forces it to be the true pose, so line L11 returns it. The full proof is in the proof file of this page. For $n = 4$ and $n = 5$ the null space has dimension at least 4 and 2; the cases $N = 2$ and $N = 3$ handle such cases in practice but carry no guarantee.

## Complexity

Lines L1 to L3 and the product $M^{\mathsf T}M$ take $\Theta(n)$ time. Everything after that works on matrices of fixed size: the eigenvectors of a $12 \times 12$ matrix, least squares problems with 6 equations, and a few Gauss-Newton steps on 4 unknowns. Lines L8 to L10 take $\Theta(n)$ time for each of the three cases. So the total is $\Theta(n)$ time and $\Theta(n)$ space for the weights and $M$. Iterative methods such as Gauss-Newton on the full pose also cost $\Theta(n)$ per step; the gain of EPnP is that it needs no starting pose.

## Properties

- **Exact on exact data** when the null space of $M$ is one-dimensional, which is the usual case for $n \ge 6$ points in general position.
- **Linear in $n$.** The number of points enters only in building $M^{\mathsf T}M$, the weights and the final error.
- **No starting pose.** The method is closed form up to a fixed number of Gauss-Newton steps on four unknowns.
- **Not a maximum likelihood estimate.** On noisy data it minimizes an algebraic error, not the [reprojection error](/reprojection-error/). A short refinement of the pose on the reprojection error improves it.
- **Depends on the control points.** The result on noisy data changes a little with the choice of the control points, for example with the signs of the principal directions.

## Variants and improvements

- **Planar points.** If the points lie in a plane, three control points in that plane are enough, and $M$ has 9 columns. The page code only covers the general case and rejects planar input.
- **The case $N = 4$.** For four points the null space is at least four-dimensional, and the journal paper solves this case with a relinearization step. The code here leaves it out, so it can fail for $n = 4$.
- **Outlier rejection.** Ferraz, Binefa and Moreno-Noguer (2014) build on the same control point system and reject outliers inside the linear solve, instead of with an outer [RANSAC](/ransac/) loop.
- **Refinement.** Running [Gauss-Newton](/gauss-newton-algorithm/) or Levenberg-Marquardt on the reprojection error from the EPnP pose gives the maximum likelihood pose under Gaussian noise in most cases.

## When to use it

Use EPnP when there are many correspondences, say 6 or more, and the camera is calibrated: for example to find the pose of a new image in [incremental structure from motion](/incremental-structure-from-motion/), or to refit the pose on all inliers after a [RANSAC](/ransac/) loop. For the minimal case of three points inside RANSAC, a [P3P](/p3p/) solver is the usual choice. When the camera is not calibrated, use [DLT resectioning](/dlt-camera-resectioning/) instead.

## Pitfalls

- **Pixels instead of normalized points.** The rows of $M$ assume $K = I$. Apply $K^{-1}$ to the pixels first, or put the focal lengths and the principal point into $M$.
- **Nearly planar points.** When the smallest principal spread is tiny, the weights become large and the system is badly conditioned. Use the planar variant.
- **Few points.** With 4 or 5 points the null space is large and the linearized cases can miss the true pose. Check the reprojection error, or use a minimal solver.
- **Wrong sign.** The eigenvectors have no fixed sign. Without the depth test in line L8, half the results would place the points behind the camera.
- **Outliers.** One wrong match can spoil the linear solve. Run EPnP inside RANSAC, or reject outliers before it.

## Implementations

## History

Moreno-Noguer, Lepetit and Fua presented the control point formulation at ICCV 2007 as an accurate non-iterative $O(n)$ solution of PnP. The journal version by Lepetit, Moreno-Noguer and Fua (2009) gave the method its name, described the cases $N = 1$ to $4$, the planar case and a Gauss-Newton refinement of the betas, and compared it with iterative and other non-iterative methods. Later work, such as that of Ferraz, Binefa and Moreno-Noguer (2014), kept the control point idea and added outlier rejection.

## References
