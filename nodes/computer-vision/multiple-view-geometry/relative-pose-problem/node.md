---
tag: Z5A74Y
kind: problem
slug: relative-pose-problem
name: Relative pose estimation
aliases:
- relative orientation
- two-view motion estimation
area: computer-vision/multiple-view-geometry
level: core
summary: "Find the rotation and the direction of translation between two calibrated cameras from matched image points."
prereqs: [essential-matrix]
see_also: [five-point-algorithm, eight-point-algorithm, essential-matrix-decomposition, cheirality, perspective-n-point, visual-odometry, structure-from-motion-problem, gauge-freedom]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 9.6, The essential matrix (the four solutions for the pose), Chapter 11 (computation of the fundamental matrix) and Section 22.2 (degenerate configurations of two views)"
  - book: isbn:9780387008936
    title: "Yi Ma, Stefano Soatto, Jana Kosecka and S. Shankar Sastry, An Invitation to 3-D Vision, Springer, 2004"
    locator: "Chapter 5, Section 5.2.1 (pose recovery from the essential matrix) and Section 5.3 (planar scenes and the homography)"
  - paper: doi:10.1109/TPAMI.2004.17
    title: "David Nister, An efficient solution to the five-point relative pose problem, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(6), 2004"
    locator: the five-point relative pose problem and its solution inside a robust estimator
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 11.3, Two-frame structure from motion"
---

Relative pose estimation is the problem of finding the motion between two calibrated cameras from points matched in their images. The answer is a rotation $R$ and a translation $\mathbf{t}$ with $\mathbf{X}_2 = R\mathbf{X}_1 + \mathbf{t}$ for the coordinates of every scene point in the two camera frames. Images alone cannot give the length of $\mathbf{t}$, so only its direction is found, which leaves five unknowns. The usual route goes through the [essential matrix](/essential-matrix/) $E = [\mathbf{t}]_\times R$: estimate $E$ with the [five-point algorithm](/five-point-algorithm/) inside [RANSAC](/ransac/), or with the [eight-point algorithm](/eight-point-algorithm/) on clean matches, then factor it by [essential matrix decomposition](/essential-matrix-decomposition/) and choose among four poses by [cheirality](/cheirality/).

## In plain words

You take two photos of a scene with the same calibrated camera, from two places. You want to know how the camera turned and in which direction it moved between the two shots. You find points that appear in both photos. Each pair of points gives one condition on the motion. The turn has three unknowns and the direction of travel has two, so five pairs are enough in principle. How far the camera moved cannot be found from the photos alone: a scene twice as large, seen from twice as far, gives the same photos. The scene points must also end up in front of both cameras, which removes false answers.

## Definition

**Input.** Matched points $(\hat{\mathbf{x}}_{1,i}, \hat{\mathbf{x}}_{2,i})$, $i = 1, \ldots, n$, in normalized image coordinates $\hat{\mathbf{x}} = K^{-1}(u, v, 1)^{\mathsf T}$, where the [intrinsic matrices](/camera-intrinsic-matrix/) $K_1$ and $K_2$ are known. Some matches may be wrong.

**Output.** A rotation $R \in SO(3)$ and a unit vector $\mathbf{t}$, $\|\mathbf{t}\| = 1$, such that the cameras $P_1 = [I \mid \mathbf{0}]$ and $P_2 = [R \mid \mathbf{t}]$ explain the correct matches: for each such match there is a scene point $\mathbf{X}_1$ with $\hat{\mathbf{x}}_1 \sim \mathbf{X}_1$ and $\hat{\mathbf{x}}_2 \sim R\mathbf{X}_1 + \mathbf{t}$, in front of both cameras. With noise, the output minimizes a chosen cost:

- **Algebraic error.** $\sum_i (\hat{\mathbf{x}}_{2,i}^{\mathsf T}[\mathbf{t}]_\times R\,\hat{\mathbf{x}}_{1,i})^2$. Cheap but without a geometric meaning.
- **Sampson error.** The first-order approximation of the distance of a match to the epipolar constraint; see [Sampson distance](/sampson-distance/).
- **Reprojection error.** Minimize over $R$, $\mathbf{t}$ and the scene points the sum of squared image distances; under independent Gaussian image noise this is the [maximum likelihood estimate](/maximum-likelihood-estimation/). It is two-view [bundle adjustment](/bundle-adjustment/).

**Ambiguities.** The scale of $\mathbf{t}$ and of the scene is a [gauge freedom](/gauge-freedom/) and is fixed by $\|\mathbf{t}\| = 1$. The constraint $\hat{\mathbf{x}}_2^{\mathsf T}E\hat{\mathbf{x}}_1 = 0$ is the same for $(R, \mathbf{t})$, $(R, -\mathbf{t})$ and the twisted pair of each, so cheirality is part of the problem, not an extra.

## Variants

- **Uncalibrated cameras.** Without $K$ only the [fundamental matrix](/fundamental-matrix/) can be found, and the cameras only up to a projective transformation, by the [projective reconstruction theorem](/projective-reconstruction-theorem/).
- **Known rotation.** If $R$ is known, for example from a gyroscope, each match gives the linear equation $(\hat{\mathbf{x}}_2 \times R\hat{\mathbf{x}}_1) \cdot \mathbf{t} = 0$, and two matches give $\mathbf{t}$ as the cross product of two such normal vectors.
- **Pure rotation.** If $\mathbf{t} = \mathbf{0}$, the images are related by the [homography](/homography/) $K_2RK_1^{-1}$, and $E = 0$. The rotation is found from the homography, and no depth can be found.
- **Planar scene.** If all points lie on one plane, the images are related by a homography, and the pose can be found by [homography decomposition](/homography-decomposition/), up to a two-fold ambiguity.
- **Partly known calibration.** An unknown focal length, shared or separate, adds unknowns and needs more matches.
- **Many views.** With more than two views, the relative poses of pairs are the input of [rotation averaging](/rotation-averaging/) and [translation averaging](/translation-averaging/) on the [view graph](/view-graph/).

## Examples

**The running example.** For $R = \begin{pmatrix} 0.8 & 0 & 0.6 \\ 0 & 1 & 0 \\ -0.6 & 0 & 0.8 \end{pmatrix}$ and $\mathbf{t} = (1, 0, 0)$, the essential matrix is $E = \begin{pmatrix} 0 & 0 & 0 \\ 0.6 & 0 & -0.8 \\ 0 & 1 & 0 \end{pmatrix}$. The point $\mathbf{X}_1 = (0, 0, 5)$ maps to $\mathbf{X}_2 = (4, 0, 4)$, so the match is $(0, 0) \leftrightarrow (1, 0)$, with depths 5 and 4.

**Four poses from one matrix.** The decomposition of this $E$ gives four poses. Only $(R, \mathbf{t})$ puts the point in front of both cameras, with depths $(5, 4)$. The pose $(R, -\mathbf{t})$ gives depths $(-5, -4)$, and the twisted pair gives $(-\frac57, \frac47)$ and $(\frac57, -\frac47)$; see [essential matrix decomposition](/essential-matrix-decomposition/).

**Scale.** The cameras $(R, 2\mathbf{t})$ with the point $(0, 0, 10)$ give the same images. The output has $\|\mathbf{t}\| = 1$.

**Non-example.** If all matches satisfy $\hat{\mathbf{x}}_2 \sim R\hat{\mathbf{x}}_1$ for one rotation, the camera did not move, and $\mathbf{t}$ is not defined: every direction fits.

## Known algorithms

| algorithm | matches | output | notes |
|---|---|---|---|
| [five-point algorithm](/five-point-algorithm/) | 5 | up to 10 essential matrices | minimal; used inside RANSAC |
| [eight-point algorithm](/eight-point-algorithm/), essential variant | 8 or more | one essential matrix | linear; on inliers only |
| [normalized eight-point](/normalized-eight-point-algorithm/) or [seven-point](/seven-point-algorithm/), then $E = K_2^{\mathsf T}FK_1$ | 8 or 7 | $F$, then $E$ | ignores the calibration during the fit |
| [essential matrix decomposition](/essential-matrix-decomposition/) | 1 or more for the test | $(R, \mathbf{t})$ | four candidates, chosen by cheirality |
| nonlinear refinement | all inliers | $(R, \mathbf{t})$ | [Levenberg-Marquardt](/levenberg-marquardt/) on the Sampson or reprojection error |

The usual pipeline is: [feature matching](/feature-matching/), the five-point algorithm in RANSAC with the Sampson distance to count inliers, decomposition with cheirality, [triangulation](/linear-triangulation/) of the inliers, and a nonlinear refinement.

## Bounds

- **Degrees of freedom.** 3 for $R$ and 2 for the direction of $\mathbf{t}$, so 5. Each match gives one equation, so 5 matches are the minimum.
- **Number of solutions.** Five matches in general position give at most 10 complex essential matrices, by the result of Demazure (1988). Each essential matrix gives four poses, and cheirality keeps at most one of them for each point seen in front of the cameras.
- **Exact recovery.** With exact matches of points in general position and $\mathbf{t} \ne \mathbf{0}$, eight matches fix $E$ linearly, and $E$ fixes $(R, \mathbf{t})$ up to the four choices.
- **Degenerate scenes.** If the points and both camera centers lie on certain quadric surfaces, two different poses explain the same images; these are the critical surfaces of Hartley and Zisserman (Section 22.2). Planar scenes are a special case for the eight-point algorithm but not for the five-point algorithm.
- **Conditioning.** A short baseline makes the direction of $\mathbf{t}$ uncertain. With a narrow field of view, a small rotation and a small sideways translation have similar effects on the images.

## Reductions

- **To essential matrix estimation.** Relative pose reduces to finding $E$ and then decomposing it, since $E$ and the pose determine each other up to the four choices and the scale.
- **From the fundamental matrix.** With known $K_1$ and $K_2$, any estimate of $F$ gives $E = K_2^{\mathsf T}FK_1$, which must then be projected onto the essential matrices by the [characterization](/essential-matrix-characterization/).
- **To triangulation.** Once $(R, \mathbf{t})$ is known, the scene points follow by [point triangulation](/point-triangulation/), up to the global scale.
- **Relation to absolute pose.** If the scene points are known in one frame, the pose of the second camera is a [perspective-n-point](/perspective-n-point/) problem, which also fixes the scale.

## Applications

- **Visual odometry.** The motion between successive frames, as in [Nister's visual odometry](/nister-visual-odometry/) and other [visual odometry](/visual-odometry/) systems.
- **Structure from motion.** The first pair of [incremental structure from motion](/incremental-structure-from-motion/), and the edges of the view graph in [global structure from motion](/global-structure-from-motion/).
- **Stereo calibration.** The pose between the two cameras of a rig, when no calibration target is used; compare [stereo camera calibration](/stereo-camera-calibration/).
- **Stereo rectification.** The pose is needed to warp two images so that matches lie on the same rows, as in [stereo rectification](/stereo-rectification/).

## References
