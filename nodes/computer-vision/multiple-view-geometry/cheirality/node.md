---
tag: KYFMZN
kind: concept
slug: cheirality
name: Cheirality
aliases:
- cheirality constraint
- positive depth constraint
area: computer-vision/multiple-view-geometry
level: core
summary: "The condition that reconstructed points lie in front of the cameras that see them, which removes the false solutions of many geometric problems."
prereqs: [camera-projection-matrix, homogeneous-coordinates]
see_also: [essential-matrix-decomposition, relative-pose-problem, linear-triangulation, homography-decomposition, stratified-reconstruction, projective-reconstruction-theorem, p3p, minimal-solver]
sources:
  - paper: doi:10.1023/A:1007984508483
    title: "Richard I. Hartley, Chirality, International Journal of Computer Vision 26(1), 1998, 41-61"
    locator: the definition of the sign of the depth of a point for a projective camera and the use of the cheirality inequalities to reach a quasi-affine reconstruction
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 6.2 (the depth of points in front of a camera), Section 9.6.3 (the four solutions and the choice by a single point) and Chapter 21, Cheirality (Sections 21.1 to 21.7)"
  - paper: doi:10.1038/293133a0
    title: "H. C. Longuet-Higgins, A computer algorithm for reconstructing a scene from two projections, Nature 293, 1981, 133-135"
    locator: the use of the sign of the depths to choose among the solutions for the motion
---

Cheirality is the condition that a reconstructed scene point lies in front of every camera that sees it. A projective camera maps a point and its mirror image through the camera center to the same image point, so the projection equations alone cannot tell front from back. Many geometric problems therefore have extra solutions in which some points sit behind a camera. The cheirality test removes them: it computes the sign of the depth of each point and keeps only solutions where the signs are positive. The best known use is the choice among the four poses of [essential matrix decomposition](/essential-matrix-decomposition/). Hartley (1998) gave the general theory under the name chirality, and Hartley and Zisserman write it as cheirality.

## In plain words

A camera only sees what is in front of it. The equations that describe a camera do not know this: a point behind the camera, on the same line through the lens, lands on the same spot of the image. So when we work back from images to a scene, the equations can give answers in which some points are behind a camera. Such answers fit the images, but no real camera could have taken them. The test is simple: for each candidate answer, find how far in front of each camera each point is. If the distance comes out negative, the answer is wrong. This throws away most of the false answers.

## The idea

**Depth of a point.** For a calibrated camera in its own frame, a point $(X, Y, Z)$ projects to $(X/Z, Y/Z)$, and the same image point comes from $(-X, -Y, -Z)$. The depth is $Z$, and the point is in front of the camera when $Z > 0$. For a camera $[R \mid \mathbf{t}]$ the depth of a point $\mathbf{X}$ is the third coordinate of $R\mathbf{X} + \mathbf{t}$.

**Depth for a general projective camera.** Let $P = [M \mid \mathbf{p}_4]$ be a $3 \times 4$ [camera matrix](/camera-projection-matrix/) and $\mathbf{X} = (X, Y, Z, T)^{\mathsf T}$ a point in [homogeneous coordinates](/homogeneous-coordinates/) with $T \ne 0$, and let $P\mathbf{X} = w\,(x, y, 1)^{\mathsf T}$. Hartley and Zisserman define
$$\operatorname{depth}(\mathbf{X}; P) = \frac{\operatorname{sign}(\det M)\, w}{T\,\|\mathbf{m}^3\|},$$
where $\mathbf{m}^3$ is the third row of $M$. Scaling $\mathbf{X}$ by any nonzero $k$ multiplies $w$ and $T$ by $k$; scaling $P$ by $k$ multiplies $\det M$ by $k^3$, $w$ by $k$ and $\|\mathbf{m}^3\|$ by $|k|$. In both cases the value does not change, so the depth, and in particular its sign, is a property of the point and the camera and not of the chosen representatives. For $P = K[R \mid \mathbf{t}]$ with $\det K > 0$ it is the usual depth.

**Why images do not fix the sign.** If $P\mathbf{X} \sim \mathbf{x}$, then also $P\mathbf{X}' \sim \mathbf{x}$ for every point $\mathbf{X}'$ on the line through $\mathbf{X}$ and the camera center, including points behind the camera. In two views, the epipolar constraint $\hat{\mathbf{x}}_2^{\mathsf T}E\hat{\mathbf{x}}_1 = 0$ only says that the two rays lie in one plane. It holds when the rays meet in front of both cameras, behind both, or behind one of them.

**The four poses.** An [essential matrix](/essential-matrix/) has four factorizations into a rotation and a translation of unit length. For a point with depths $(\lambda_1, \lambda_2)$ under the true pose, the other three give depths of the signs of $(-\lambda_1, -\lambda_2)$, $(-\lambda_1, \lambda_2)/D$ and $(\lambda_1, -\lambda_2)/D$ for a nonzero number $D$ that depends on the point. Whatever the sign of $D$, each of the three has at least one negative depth when the true depths are positive. So one point in front of both cameras picks the right pose; the proof is on the [decomposition page](/essential-matrix-decomposition/).

**Projective reconstructions.** A reconstruction from uncalibrated images is fixed only up to a projective transformation, by the [projective reconstruction theorem](/projective-reconstruction-theorem/). A projective transformation can move the plane at infinity through the scene, which puts some points behind the cameras. Hartley (1998) showed that the cheirality inequalities, one for each point and each camera, restrict the transformation to those that keep the plane at infinity off the convex hull of the points and the camera centers. The result is a quasi-affine reconstruction, a step between the projective and the affine level in [stratified reconstruction](/stratified-reconstruction/).

## Examples

**One match, two signs.** Take the running example: $R = \begin{pmatrix} 0.8 & 0 & 0.6 \\ 0 & 1 & 0 \\ -0.6 & 0 & 0.8 \end{pmatrix}$, $\mathbf{t} = (1, 0, 0)$. The point $\mathbf{X}_1 = (0, 0, 5)$ has $\mathbf{X}_2 = (4, 0, 4)$: depths 5 and 4, and the match is $(0, 0) \leftrightarrow (1, 0)$. The point $\mathbf{X}_1 = (0, 0, -5)$ has $\mathbf{X}_2 = (-3, 0, -4) + (1, 0, 0) = (-2, 0, -4)$: depths $-5$ and $-4$, and the match is $(0, 0) \leftrightarrow (0.5, 0)$. Both matches satisfy the epipolar constraint with $E = [\mathbf{t}]_\times R$; only cheirality shows that the second point cannot be seen.

**The four poses.** For the first match, the four candidates of the decomposition give depths $(5, 4)$, $(-5, -4)$, $(\frac57, -\frac47)$ and $(-\frac57, \frac47)$. Only the first pair is positive.

**An epipole from behind.** The center of camera 2 in the frame of camera 1 is $-R^{\mathsf T}\mathbf{t} = (-0.8, 0, -0.6)$, which has depth $-0.6$: it is behind camera 1. Its image, the epipole $\mathbf{e}_1 \sim (0.8, 0, 0.6) \sim (\frac43, 0)$, is still a valid image point, because projection forgets the sign.

**A homography.** For a planar scene, [homography decomposition](/homography-decomposition/) gives up to four candidate poses and plane normals. The condition that the points of the plane are in front of both cameras removes two of them in general, and the true one is then picked with more information.

## Where it is used

- **Pose recovery.** The choice among the four poses of the essential matrix, in [essential matrix decomposition](/essential-matrix-decomposition/) and so in every solution of the [relative pose problem](/relative-pose-problem/).
- **Minimal solvers.** Solutions of the [five-point algorithm](/five-point-algorithm/) or of [P3P](/p3p/) that put the sample points behind a camera can be dropped before scoring in [RANSAC](/ransac/).
- **Triangulation checks.** After [linear triangulation](/linear-triangulation/), points with negative depth are outliers or badly conditioned, and are removed before [bundle adjustment](/bundle-adjustment/).
- **Robust scoring.** Some RANSAC scores count a match as an inlier only if it fits the model and its point is in front of both cameras.
- **Uncalibrated reconstruction.** The cheirality inequalities give a quasi-affine reconstruction, which helps [self-calibration](/self-calibration/) and the upgrade to an affine reconstruction.

## References
