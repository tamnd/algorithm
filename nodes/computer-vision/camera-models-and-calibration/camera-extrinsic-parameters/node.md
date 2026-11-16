---
tag: X5VYZG
kind: definition
slug: camera-extrinsic-parameters
name: Camera extrinsic parameters
aliases:
- exterior orientation
- camera pose parameters
area: computer-vision/camera-models-and-calibration
level: intro
summary: The rotation and translation that take world coordinates to camera coordinates, six degrees of freedom in all.
prereqs: [homogeneous-coordinates, special-orthogonal-group, rigid-body-transformation]
see_also: [camera-intrinsic-matrix, camera-projection-matrix, perspective-n-point, homogeneous-transformation-matrix, special-euclidean-group, axis-angle-representation, rodrigues-rotation-formula, stereo-camera-calibration]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 6.1, Finite cameras (camera rotation and translation, the camera center and the form P = K R [I | -C])
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 2, Image formation (3D rotations and the camera extrinsics)
---

The extrinsic parameters of a camera are a rotation $R$ and a translation $t$ that take the coordinates $X_w$ of a point in a fixed world frame to its coordinates $X_c = R X_w + t$ in the frame of the camera. They say where the camera is and which way it points, with 6 degrees of freedom: 3 for the rotation and 3 for the translation. They are the outer half of the [camera projection matrix](/camera-projection-matrix/) $P = K [R \mid t]$; the inner half, the [camera intrinsic matrix](/camera-intrinsic-matrix/) $K$, maps the camera frame to pixels. Photogrammetry calls them the exterior orientation. The translation $t$ is not the position of the camera: the position is the center $C = -R^{\mathsf T} t$.

## Definition

**Frames.** The world frame is any fixed right-handed frame, for example one tied to a calibration pattern. The camera frame has its origin at the center of projection, $X$ to the right, $Y$ down and $Z$ forward along the optical axis.

**Parameters.** The extrinsic parameters are a rotation $R \in SO(3)$, so $R^{\mathsf T} R = I$ and $\det R = +1$ (see [special orthogonal group](/special-orthogonal-group/)), and a vector $t \in \mathbb{R}^3$, such that for every point
$$X_c = R X_w + t.$$
As a $4 \times 4$ matrix acting on [homogeneous coordinates](/homogeneous-coordinates/), this is the [rigid body transformation](/rigid-body-transformation/)
$$T_{cw} = \begin{pmatrix} R & t \\ 0^{\mathsf T} & 1 \end{pmatrix} \in SE(3),$$
which maps world points to camera points (see [homogeneous transformation matrix](/homogeneous-transformation-matrix/) and [special Euclidean group](/special-euclidean-group/)).

**What the entries mean.**
- The camera center $C$ is the world point with $X_c = 0$, so $R C + t = 0$ and $C = -R^{\mathsf T} t$. Then $X_c = R (X_w - C)$, and $P = K R [I \mid -C]$ (HZ section 6.1).
- The rows $r_1, r_2, r_3$ of $R$ are the camera axes written in world coordinates: $r_1$ points right, $r_2$ down, and $r_3$ along the optical axis. So the depth of a world point is $Z = r_3^{\mathsf T} (X_w - C)$, and a point is in front of the camera if this is positive.
- The inverse map, from the camera to the world, is $X_w = R^{\mathsf T} X_c + C$. Its matrix $T_{wc} = T_{cw}^{-1}$ holds $R^{\mathsf T}$ and $C$. This is the pose of the camera in the world, the form that robotics and graphics code usually store.

**Counting.** $R$ has 3 degrees of freedom and $t$ has 3, so there are 6 in all. The 9 entries of $R$ are not free; code that estimates $R$ uses a minimal form, such as the rotation vector $\theta a$ of the [axis-angle representation](/axis-angle-representation/) with $R$ from the [Rodrigues formula](/rodrigues-rotation-formula/), or a unit quaternion.

**Two cameras.** For two cameras with extrinsics $(R_1, t_1)$ and $(R_2, t_2)$ in the same world frame, the motion from the frame of camera 1 to the frame of camera 2 is $X_2 = R X_1 + t$ with $R = R_2 R_1^{\mathsf T}$ and $t = t_2 - R t_1$. This is the relative pose that [stereo camera calibration](/stereo-camera-calibration/) estimates.

## Examples and non-examples

**A camera on the X axis.** Put the center at $C = (2, 0, 0)$ and let the camera look at the world origin, with its $Y$ axis along the world $Y$ axis. The forward axis is $r_3 = (-1, 0, 0)$, the down axis is $r_2 = (0, 1, 0)$, and the right axis is $r_1 = r_2 \times r_3 = (0, 0, 1)$. So
$$R = \begin{pmatrix} 0 & 0 & 1 \\ 0 & 1 & 0 \\ -1 & 0 & 0 \end{pmatrix}, \qquad t = -R C = (0, 0, 2).$$
$R$ is the rotation by $90$ degrees about the $Y$ axis, with rotation vector $(0, \pi/2, 0)$, and $\det R = +1$. Check: the origin goes to $X_c = t = (0, 0, 2)$, straight ahead at depth 2. The world point $(0, 0, 1)$ goes to $(1, 0, 2)$, to the right of the axis. With $K$ of focal length 800 and principal point $(320, 240)$, these two points have the pixels $(320, 240)$ and $(720, 240)$.

**The translation is not the position.** In the example, $t = (0, 0, 2)$ but $C = (2, 0, 0)$. The relation $t = -C$ holds only when $R = I$.

**Two cameras.** With $R_1 = R_2 = I$, $t_1 = (0, 0, 5)$ and $t_2 = (-0.1, 0, 5)$, the relative pose is $R = I$ and $t = (-0.1, 0, 0)$: camera 2 sits $0.1$ to the right of camera 1, at $C_2 = (0.1, 0, -5)$ against $C_1 = (0, 0, -5)$.

**Non-examples.**
- A pair $(Q, t)$ with $Q$ orthogonal but $\det Q = -1$. $Q$ is a reflection, and the frame it gives is left-handed. Such a matrix appears when a linear method fits $R$ without a sign rule; the [camera matrix decomposition](/camera-matrix-decomposition/) page shows the fix.
- The camera pose $(R^{\mathsf T}, C)$ given where $(R, t)$ is expected. Both describe the same camera, but they are inverse maps. Mixing them is the most common bug with extrinsics, and it often gives images that look nearly right for cameras close to the world origin.
- A $3 \times 4$ matrix $[M \mid m]$ with $M$ not a rotation, for example a scaled or sheared one. It can be a camera matrix with $K \ne I$, but its left block is $K R$ and it must be decomposed before $R$ can be read.
- The full $P$. The extrinsics say nothing about pixels; two cameras at the same place with different lenses have the same $(R, t)$.

## Related definitions

- [Camera intrinsic matrix](/camera-intrinsic-matrix/): the matrix $K$ from the camera frame to pixels.
- [Camera projection matrix](/camera-projection-matrix/): $P = K [R \mid t]$, with 11 degrees of freedom in all, 5 intrinsic and 6 extrinsic.
- [Perspective-n-point](/perspective-n-point/): the problem of finding $(R, t)$ from known $K$ and 2D to 3D matches.
- [Homogeneous transformation matrix](/homogeneous-transformation-matrix/), [special Euclidean group](/special-euclidean-group/) and [rigid body transformation](/rigid-body-transformation/): the robotics pages on the $4 \times 4$ matrix and the group of rigid motions.

## References
