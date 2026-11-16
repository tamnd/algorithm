---
tag: N0TBTV
kind: definition
slug: camera-projection-matrix
name: Camera projection matrix
aliases:
- 3x4 camera matrix
- finite projective camera
area: computer-vision/camera-models-and-calibration
level: core
summary: The 3 by 4 matrix P = K[R | t] that maps a world point in homogeneous coordinates to its image point, with 11 degrees of freedom.
prereqs: [camera-intrinsic-matrix, camera-extrinsic-parameters]
see_also: [camera-matrix-decomposition, dlt-camera-resectioning, affine-camera-model, camera-calibration, homography, pinhole-camera-model, point-triangulation, perspective-n-point]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 6.1, Finite cameras, and Section 6.2, The projective camera (the camera center as null vector, the column and row vectors, the principal plane, axis and point, the depth of points, back-projection)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 2, Image formation (the 3 by 4 camera matrix)
  - paper: doi:10.1561/0600000023
    title: Peter Sturm, Srikumar Ramalingam, Jean-Philippe Tardif, Simone Gasparini and Joao Barreto, Camera models and fundamental concepts used in geometric computer vision, Foundations and Trends in Computer Graphics and Vision 6(1-2), 2011, 1-183
    locator: the part on the perspective camera and its projection matrix
---

The camera projection matrix is the $3 \times 4$ matrix $P$ that maps a point of 3D space, written in [homogeneous coordinates](/homogeneous-coordinates/) as $\mathbf{X} = (X, Y, Z, 1)^{\mathsf T}$, to its image point $\mathbf{x} \sim P \mathbf{X}$. For a pinhole camera $P = K [R \mid t]$, the product of the [camera intrinsic matrix](/camera-intrinsic-matrix/) $K$ and the [camera extrinsic parameters](/camera-extrinsic-parameters/) $(R, t)$. $P$ is known only up to scale, so it has $12 - 1 = 11$ degrees of freedom, which are exactly the 5 intrinsic and the 6 extrinsic ones. This page defines $P$ and lists what can be read from it. Getting $P$ from point matches is [DLT resectioning](/dlt-camera-resectioning/), and getting $K$, $R$ and $t$ back from $P$ is [camera matrix decomposition](/camera-matrix-decomposition/). The graphics page [pinhole camera model](/pinhole-camera-model/) uses the same map with the view direction $-w$; this area looks along $+Z$.

## Definition

**The pinhole camera.** Let $K$ be an intrinsic matrix, $R$ a rotation and $t$ a vector, with the conventions of this area: $X_c = R X_w + t$, the camera frame has $X$ right, $Y$ down and $Z$ forward, and the center of pixel $(u, v)$ is the point $(u, v)$. The camera matrix is
$$P = K [R \mid t] = K R [I \mid -C], \qquad C = -R^{\mathsf T} t,$$
and the pixel of the world point $X_w$ is found by
$$\begin{pmatrix} u' \\ v' \\ w' \end{pmatrix} = P \begin{pmatrix} X_w \\ 1 \end{pmatrix}, \qquad (u, v) = (u' / w', \; v' / w').$$
For a point in front of the camera, $w'$ is its depth $Z$ in the camera frame, so the division needs $w' \ne 0$.

**General and finite cameras.** A general projective camera is any real $3 \times 4$ matrix of rank 3, up to a nonzero scale (HZ section 6.2). Write $P = [M \mid p_4]$ with $M$ the left $3 \times 3$ block. If $M$ is nonsingular, $P$ is a finite camera, and then it factors as $P = \lambda K [R \mid t]$ with $K$ upper triangular with a positive diagonal and $K_{33} = 1$, $R$ a rotation and $\lambda \ne 0$; with these sign rules the factors are unique. If $M$ is singular, the center lies on the plane at infinity; the [affine camera](/affine-camera-model/), whose last row is $(0, 0, 0, 1)$, is the main case.

**Degrees of freedom.** $P$ has 12 entries and one scale, so 11 degrees of freedom. A finite camera has the same count: 5 in $K$, 3 in $R$ and 3 in $t$. Each 2D to 3D match gives two equations, so 6 matches in general position fix $P$ (5.5 in the minimum).

**What the matrix holds** (HZ section 6.2). Let $m_3^{\mathsf T}$ be the third row of $M$ and $p^{i\mathsf T}$ the rows of $P$.
- **Camera center.** $C$ is the right null vector: $P (C, 1)^{\mathsf T} = 0$. For a finite camera, $C = -M^{-1} p_4$. Every point on a ray through $C$ has the same image, and $C$ itself has none.
- **Columns.** The first three columns $p_1, p_2, p_3$ are the images of the points at infinity in the directions of the world $X$, $Y$ and $Z$ axes, that is, their vanishing points. The last column $p_4$ is the image of the world origin.
- **Rows.** Each row is a plane of space. The third row $p^3$ is the principal plane: the plane through $C$ parallel to the image, whose points have $w' = 0$ and map to infinity. The rows $p^1$ and $p^2$ are the planes through $C$ that map to the image lines $u = 0$ and $v = 0$.
- **Principal axis and point.** The vector $\det(M)\, m_3$ points along the optical axis, to the front of the camera, and the principal point is $M m_3$ up to scale.
- **Depth.** For $\mathbf{X} = (X_w, 1)$ and $w' = p^{3\mathsf T} \mathbf{X}$, the depth of the point is $\operatorname{sign}(\det M)\, w' / \|m_3\|$. It is positive for a point in front of the camera, whatever the scale of $P$.
- **Back-projection.** The pixel $\mathbf{x}$ is the image of all points $C + \lambda M^{-1} \mathbf{x}$; the front half of this line is the ray that the pixel sees.
- **A plane.** For the world plane $Z_w = 0$, the map from $(X_w, Y_w, 1)$ to the image is the $3 \times 3$ matrix $K [r_1 \; r_2 \; t]$, a [homography](/homography/). [Zhang's method](/zhang-calibration-method/) is built on this fact.

## Examples and non-examples

**A camera five units back.** Let $K$ have $f_x = f_y = 800$, $s = 0$ and principal point $(320, 240)$, and let $R = I$ and $t = (0, 0, 5)$. Then
$$P = \begin{pmatrix} 800 & 0 & 320 & 1600 \\ 0 & 800 & 240 & 1200 \\ 0 & 0 & 1 & 5 \end{pmatrix}.$$
- The world point $(1, 0.5, 0)$ gives $P (1, 0.5, 0, 1)^{\mathsf T} = (2400, 1600, 5)$, so its pixel is $(480, 320)$, and its depth is 5.
- The null vector is $(0, 0, -5, 1)$: $P (0, 0, -5, 1)^{\mathsf T} = (-1600 + 1600, -1200 + 1200, -5 + 5) = 0$. So $C = (0, 0, -5) = -R^{\mathsf T} t$.
- The third column $(320, 240, 1)$ is the principal point: the world $Z$ axis is the optical axis, and its vanishing point is where the axis meets the image. The first column $(800, 0, 0)$ is a point at infinity of the image, because the world $X$ axis is parallel to the image plane.
- $2P$ and $-P$ give the same pixels. With $-P$, $w' = -5$ for the same point, but $\det M$ also changes sign, so the depth formula still gives $+5$.

**Not every matrix is a camera.**
- A $3 \times 4$ matrix of rank 2, for example one with a zero third row, is not a camera: it maps all of space into a line or to points at infinity, and its null space is a line, not a point.
- A finite camera needs $\det M \ne 0$. The matrix $\begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$ has rank 3, so it is a projective camera, but $M$ is singular: it is the orthographic projection $(X, Y, Z) \mapsto (X, Y)$, an [affine camera](/affine-camera-model/) with its center at infinity.
- A $3 \times 3$ homography is not a camera matrix. It maps one plane to the image, and it is what $P$ becomes on that plane.
- The $4 \times 4$ projection matrix of a graphics API is not $P$. It keeps a fourth row for the depth buffer and maps to clip coordinates, before the viewport transform.

## Related definitions

- [Camera intrinsic matrix](/camera-intrinsic-matrix/) and [camera extrinsic parameters](/camera-extrinsic-parameters/): the two factors of $P$.
- [Camera matrix decomposition](/camera-matrix-decomposition/): the algorithm that splits a finite $P$ into $K$, $R$, $t$ and $C$.
- [DLT resectioning](/dlt-camera-resectioning/): the linear algorithm that finds $P$ from six or more 2D to 3D matches.
- [Affine camera model](/affine-camera-model/): the cameras with last row $(0, 0, 0, 1)$, a limit of finite cameras far from the scene.
- [Point triangulation](/point-triangulation/) and [perspective-n-point](/perspective-n-point/): the problems of finding a point from known cameras, and a pose from known points and $K$.

## References
