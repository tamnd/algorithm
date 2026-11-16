---
tag: 2AW6EF
kind: concept
slug: epipolar-geometry
name: Epipolar geometry
aliases:
- epipolar constraint
- two-view geometry
area: computer-vision/multiple-view-geometry
level: core
summary: "The geometry of two views of one scene. A point in one image must have its match on a line in the other image, and all these lines pass through the image of the other camera center."
prereqs: [camera-projection-matrix, homogeneous-coordinates, pinhole-camera-model]
see_also: [fundamental-matrix, essential-matrix, eight-point-algorithm, relative-pose-problem, stereo-rectification, sampson-distance, linear-triangulation, trifocal-tensor]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Chapter 9, Epipolar Geometry and the Fundamental Matrix: Section 9.1 (epipolar geometry) and Section 9.2 (the fundamental matrix, its derivation and properties)"
  - book: isbn:9780387008936
    title: "Yi Ma, Stefano Soatto, Jana Kosecka and S. Shankar Sastry, An Invitation to 3-D Vision, Springer, 2004"
    locator: "Chapter 5, Section 5.1.1 (the epipolar constraint and the essential matrix)"
  - paper: doi:10.1038/293133a0
    title: "H. C. Longuet-Higgins, A computer algorithm for reconstructing a scene from two projections, Nature 293, 1981, 133-135"
    locator: "the coplanarity constraint between the two rays and the baseline, written as a bilinear form in the image coordinates"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 11.3, Two-frame structure from motion"
---

Epipolar geometry is the geometry of two images of one scene taken by two pinhole cameras at different places. It depends only on the two cameras, their internal parameters and their relative pose, and not on the scene. Its main result is the epipolar constraint: if $\mathbf{x}_1$ and $\mathbf{x}_2$ are images of the same 3D point, then $\mathbf{x}_2$ lies on a line in image 2 that $\mathbf{x}_1$ fixes, and the other way round. In matrices the constraint is $\mathbf{x}_2^{\mathsf T}F\mathbf{x}_1 = 0$ for the [fundamental matrix](/fundamental-matrix/) $F$ in pixel coordinates, and $\mathbf{x}_2^{\mathsf T}E\mathbf{x}_1 = 0$ for the [essential matrix](/essential-matrix/) $E$ in normalized coordinates. This page is about the geometry; the two matrices have their own pages, and the methods that find them from matches are the [eight-point](/eight-point-algorithm/), [seven-point](/seven-point-algorithm/) and [five-point](/five-point-algorithm/) algorithms.

## In plain words

Two cameras look at the same scene from two places. Pick a point in the first image. The point in space that made it lies somewhere on the ray from the first camera through that image point, but the image alone does not say how far along the ray. Seen from the second camera, that ray is a line. So the matching point in the second image must be on that line, and a search for the match can look along one line instead of over the whole image. Every such line in the second image passes through one special point: the place where the second camera sees the first camera. The same holds the other way round. The positions of these lines depend only on how the two cameras are placed, not on what they look at.

## The idea

**Setup.** We use the conventions of this area. Camera 1 has the frame $\mathbf{X}_1$, camera 2 has the frame $\mathbf{X}_2$, and the relative pose $(R, \mathbf{t})$ maps one to the other: $\mathbf{X}_2 = R\mathbf{X}_1 + \mathbf{t}$. Both frames have $Z$ forward. The camera matrices are $P_1 = K_1[I \mid \mathbf{0}]$ and $P_2 = K_2[R \mid \mathbf{t}]$, with the [intrinsic matrices](/camera-intrinsic-matrix/) $K_1$ and $K_2$. Image points are [homogeneous](/homogeneous-coordinates/) 3-vectors, and the normalized image point of a pixel $\mathbf{x}$ is $\hat{\mathbf{x}} = K^{-1}\mathbf{x}$. The center of camera 1 is $\mathbf{C}_1 = \mathbf{0}$ in frame 1, and the center of camera 2 is $\mathbf{C}_2 = -R^{\mathsf T}\mathbf{t}$ in frame 1.

**The named objects.**
- The *baseline* is the line through the two centers $\mathbf{C}_1$ and $\mathbf{C}_2$.
- An *epipolar plane* is a plane that contains the baseline. Each 3D point off the baseline lies on exactly one epipolar plane, together with the two centers.
- The *epipole* $\mathbf{e}_1$ is the image of $\mathbf{C}_2$ in camera 1, and $\mathbf{e}_2$ is the image of $\mathbf{C}_1$ in camera 2. Both are the points where the baseline meets the image planes. An epipole can be at infinity (when the baseline is parallel to the image plane) and can be the image of a center behind the camera.
- An *epipolar line* is the intersection of an epipolar plane with an image plane. In image 2, the epipolar line of $\mathbf{x}_1$ is the image of the ray of $\mathbf{x}_1$. All epipolar lines of one image pass through its epipole.

**The constraint.** Let $\mathbf{X}$ be a point with $\mathbf{X}_1 = \lambda_1\hat{\mathbf{x}}_1$ and $\mathbf{X}_2 = \lambda_2\hat{\mathbf{x}}_2$. The three vectors $\mathbf{X}_2$, $\mathbf{t}$ and $R\mathbf{X}_1 = \mathbf{X}_2 - \mathbf{t}$, all written in frame 2, lie in one plane (the epipolar plane), so
$$\mathbf{X}_2^{\mathsf T}(\mathbf{t} \times R\mathbf{X}_1) = 0 \quad\Longrightarrow\quad \hat{\mathbf{x}}_2^{\mathsf T}[\mathbf{t}]_\times R\,\hat{\mathbf{x}}_1 = 0 ,$$
where $[\mathbf{t}]_\times$ is the [skew matrix](/skew-symmetric-matrix-of-a-vector/) of $\mathbf{t}$. The matrix $E = [\mathbf{t}]_\times R$ is the essential matrix. With $\hat{\mathbf{x}} = K^{-1}\mathbf{x}$ the same equation in pixels is $\mathbf{x}_2^{\mathsf T}F\mathbf{x}_1 = 0$ with $F = K_2^{-\mathsf T}EK_1^{-1}$. This is the form of Longuet-Higgins (1981) for $E$, and of Hartley and Zisserman (Section 9.2) for $F$.

**Lines and epipoles in matrix form.** For a fixed $\mathbf{x}_1$, the equation $\mathbf{x}_2^{\mathsf T}(F\mathbf{x}_1) = 0$ says that $\mathbf{x}_2$ lies on the line $\mathbf{l}_2 = F\mathbf{x}_1$. In the same way the epipolar line of $\mathbf{x}_2$ in image 1 is $\mathbf{l}_1 = F^{\mathsf T}\mathbf{x}_2$. The epipoles are the null vectors: $F\mathbf{e}_1 = \mathbf{0}$ and $F^{\mathsf T}\mathbf{e}_2 = \mathbf{0}$. Since $\mathbf{e}_2^{\mathsf T}(F\mathbf{x}_1) = (F^{\mathsf T}\mathbf{e}_2)^{\mathsf T}\mathbf{x}_1 = 0$ for all $\mathbf{x}_1$, every line $\mathbf{l}_2$ passes through $\mathbf{e}_2$. $F$ is singular because it has a null vector; it has rank 2 whenever the centers differ.

**The two pencils.** The epipolar lines of an image form a pencil, the set of lines through the epipole, which is a projective line. The epipolar planes give a one-to-one map between the pencil of image 1 and the pencil of image 2: an epipolar line in one image matches exactly one in the other. This map is a 1D homography with 3 degrees of freedom, and with the 2 + 2 coordinates of the two epipoles it gives the 7 degrees of freedom of $F$ (Hartley and Zisserman, Section 9.2).

**What it does not fix.** The constraint is one equation per match. It says that a match is possible, not that it is right: a wrong match that falls on the epipolar line passes. It also does not see the scale of $\mathbf{t}$: $E$ and $\lambda E$ give the same constraint, so from two images alone the baseline is known only in direction. Points on the baseline have no epipolar plane, and their images are the epipoles.

**Special motions.**
- *Pure rotation*, $\mathbf{t} = \mathbf{0}$: the centers coincide, $E = 0$, and there is no epipolar geometry. The two images are related by the [homography](/homography/) $K_2RK_1^{-1}$.
- *Translation along the optical axis*, $R = I$ and $\mathbf{t} = (0, 0, t_z)$: the epipole is the principal point, and the epipolar lines are the lines through it. The image points move along these lines, away from or toward the epipole.
- *Sideways translation*, $R = I$, $K_1 = K_2$ and $\mathbf{t} = (-b, 0, 0)$: the epipoles are the point at infinity $(1, 0, 0)$, and the epipolar lines are the image rows. This is the rectified case.
- *A planar scene*: the matches also satisfy a homography. The epipolar geometry is still defined by the cameras, but the matches cannot fix it, because many matrices $F$ fit them. See the degenerate cases on the [eight-point](/eight-point-algorithm/) page.

## Examples

**A rotation about the Y axis and a sideways step.** Let $K_1 = K_2 = I$ (normalized coordinates), $R = \begin{pmatrix} 0.8 & 0 & 0.6 \\ 0 & 1 & 0 \\ -0.6 & 0 & 0.8 \end{pmatrix}$, a rotation by about $36.87$ degrees about $Y$, and $\mathbf{t} = (1, 0, 0)$. Then
$$E = [\mathbf{t}]_\times R = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{pmatrix} R = \begin{pmatrix} 0 & 0 & 0 \\ 0.6 & 0 & -0.8 \\ 0 & 1 & 0 \end{pmatrix} .$$
- *Epipoles.* $E(0.8, 0, 0.6)^{\mathsf T} = \mathbf{0}$, so $\mathbf{e}_1 = (0.8, 0, 0.6) \sim (4/3, 0, 1)$. This is the image of $\mathbf{C}_2 = -R^{\mathsf T}\mathbf{t} = (-0.8, 0, -0.6)$, which has $Z < 0$: camera 2 is behind camera 1, and the epipole is the image of a point behind the camera. $E^{\mathsf T}(1, 0, 0)^{\mathsf T} = \mathbf{0}$, so $\mathbf{e}_2 = (1, 0, 0)$, a point at infinity: $\mathbf{C}_1$ is at $\mathbf{X}_2 = \mathbf{t} = (1, 0, 0)$, with $Z = 0$. So the epipolar lines in image 2 are parallel, and all are horizontal.
- *A match.* The point $\mathbf{X}_1 = (0, 0, 5)$ gives $\mathbf{X}_2 = R\mathbf{X}_1 + \mathbf{t} = (3, 0, 4) + (1, 0, 0) = (4, 0, 4)$, so $\mathbf{x}_1 = (0, 0)$ and $\mathbf{x}_2 = (1, 0)$. The line $\mathbf{l}_2 = E(0, 0, 1)^{\mathsf T} = (0, -0.8, 0)$ is $v = 0$, and $\mathbf{x}_2$ lies on it. The depths are 5 in camera 1 and 4 in camera 2.
- *A second match.* $\mathbf{X}_1 = (0, 2.5, 5)$ gives $\mathbf{X}_2 = (4, 2.5, 4)$, $\mathbf{x}_1 = (0, 0.5)$ and $\mathbf{x}_2 = (1, 0.625)$. The line $\mathbf{l}_2 = E(0, 0.5, 1)^{\mathsf T} = (0, -0.8, 0.5)$ is $v = 0.625$; it contains $\mathbf{x}_2$. The other way, $\mathbf{l}_1 = E^{\mathsf T}(1, 0.625, 1)^{\mathsf T} = (0.375, 1, -0.5)$. It passes through $\mathbf{x}_1$, since $0 + 0.5 - 0.5 = 0$, and through $\mathbf{e}_1 = (4/3, 0)$, since $0.375 \cdot 4/3 - 0.5 = 0$.

**The same cameras in pixels.** With $K_1 = K_2 = \begin{pmatrix} 500 & 0 & 320 \\ 0 & 500 & 240 \\ 0 & 0 & 1 \end{pmatrix}$, the first match becomes $(320, 240) \leftrightarrow (820, 240)$ and the second $(320, 490) \leftrightarrow (820, 552.5)$. The [fundamental matrix](/fundamental-matrix/) page computes $F$ for this case.

**The rectified pair.** With $R = I$, $K_1 = K_2 = K$ with focal length $f$ and zero skew, and camera 2 at $\mathbf{C}_2 = (b, 0, 0)$, we get $\mathbf{t} = -R\mathbf{C}_2 = (-b, 0, 0)$, and
$$F = K^{-\mathsf T}[\mathbf{t}]_\times K^{-1} = \frac{b}{f}\begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & 1 \\ 0 & -1 & 0 \end{pmatrix} \sim \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{pmatrix} .$$
The constraint is $\mathbf{x}_2^{\mathsf T}F\mathbf{x}_1 = v_1 - v_2 = 0$ for the second form: a match is on the same row. This is why [stereo rectification](/stereo-rectification/) maps both images so that $F$ takes this form, and the search for a match becomes a search for the [disparity](/disparity/) along a row.

## Where it is used

- **Matching.** The search for the match of a point runs along its epipolar line, often in a band of a few pixels around it. This cuts a 2D search to a 1D search and removes many wrong matches. Dense [stereo matching](/stereo-matching/) works on rectified images, where the lines are rows.
- **Relative pose.** The [relative pose problem](/relative-pose-problem/) finds $(R, \mathbf{t})$ from the constraint on many matches, with the [five-point algorithm](/five-point-algorithm/) for calibrated cameras or the [eight-point](/eight-point-algorithm/) and [seven-point](/seven-point-algorithm/) algorithms for $F$. Then [pose recovery from E](/essential-matrix-decomposition/) and [cheirality](/cheirality/) give the motion.
- **Outlier rejection.** In [RANSAC](/ransac/), a match is an inlier when it is close to its epipolar line. The [Sampson distance](/sampson-distance/) is the usual first-order measure of that distance.
- **Triangulation.** A match that satisfies the constraint exactly has two rays that meet. [Optimal triangulation](/optimal-triangulation/) moves a noisy match to the nearest pair that satisfies it, and [linear triangulation](/linear-triangulation/) intersects the rays.
- **Structure from motion and visual odometry.** Two-view geometry starts [incremental structure from motion](/incremental-structure-from-motion/) and is the core of [visual odometry](/visual-odometry/) front ends. Three views add the [trifocal tensor](/trifocal-tensor/), which also transfers lines.

## References
