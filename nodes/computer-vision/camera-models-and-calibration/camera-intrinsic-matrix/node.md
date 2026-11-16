---
tag: 08K0VT
kind: definition
slug: camera-intrinsic-matrix
name: Camera intrinsic matrix
aliases:
- calibration matrix
- K matrix
area: computer-vision/camera-models-and-calibration
level: intro
summary: The upper triangular 3 by 3 matrix of focal lengths, skew and principal point that maps camera coordinates of a ray to pixel coordinates.
prereqs: [homogeneous-coordinates, pixel]
see_also: [camera-extrinsic-parameters, camera-projection-matrix, camera-calibration, camera-matrix-decomposition, image-of-the-absolute-conic, brown-conrady-distortion-model, pinhole-camera-model, viewport-transform]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 6.1, Finite cameras (the camera calibration matrix, its five parameters, and the meaning of each one)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 2, Image formation (the calibration matrix and the camera intrinsics)
  - paper: doi:10.1561/0600000023
    title: Peter Sturm, Srikumar Ramalingam, Jean-Philippe Tardif, Simone Gasparini and Joao Barreto, Camera models and fundamental concepts used in geometric computer vision, Foundations and Trends in Computer Graphics and Vision 6(1-2), 2011, 1-183
    locator: the part on central perspective cameras and their intrinsic parameters
---

The camera intrinsic matrix $K$ is the $3 \times 3$ upper triangular matrix that turns the direction of a ray, given in the frame of the camera, into the pixel where that ray meets the image. It holds the five internal parameters of a pinhole camera: two focal lengths in pixels, a skew and the two coordinates of the principal point. It does not hold the position or the turn of the camera, which are the [extrinsic parameters](/camera-extrinsic-parameters/), and it does not hold lens distortion. Together the two give the [camera projection matrix](/camera-projection-matrix/) $P = K [R \mid t]$. The graphics page [pinhole camera model](/pinhole-camera-model/) describes the same camera, but it looks along $-w$; here the camera looks along $+Z$.

## Definition

**Camera frame.** The camera frame has its origin at the center of projection, $X$ to the right, $Y$ down and $Z$ forward along the optical axis. A point $X_c = (X, Y, Z)$ is in front of the camera if $Z > 0$. Its normalized image coordinates are $x_n = (X / Z, Y / Z)$, the point where its ray meets the plane $Z = 1$.

**Pixels.** An image has $W$ columns and $H$ rows. The [pixel](/pixel/) $(u, v)$ is in column $u$ (to the right) and row $v$ (down), and the origin is the top left pixel. We put the center of pixel $(u, v)$ at the point $(u, v)$, as Hartley and Zisserman (HZ) and OpenCV do.

**The matrix.** The intrinsic matrix is
$$K = \begin{pmatrix} f_x & s & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{pmatrix}, \qquad f_x > 0, \; f_y > 0,$$
and it maps a point in the camera frame to its pixel by
$$\begin{pmatrix} u \\ v \\ 1 \end{pmatrix} \sim K \begin{pmatrix} X \\ Y \\ Z \end{pmatrix}, \qquad u = f_x \frac{X}{Z} + s \frac{Y}{Z} + c_x, \quad v = f_y \frac{Y}{Z} + c_y.$$
The symbol $\sim$ means equal up to a nonzero scale, here the scale $Z$.

- $f_x = f m_x$ and $f_y = f m_y$ are the focal length in pixels along the rows and the columns: $f$ is the distance from the center to the image plane, and $m_x$, $m_y$ are the numbers of pixels per unit length on the sensor. If the pixels are square, $f_x = f_y$. The ratio $f_y / f_x$ is the aspect ratio.
- $(c_x, c_y)$ is the principal point, the pixel where the optical axis meets the image. It is near the image center, but it is not the image center.
- $s$ is the skew. It is not zero only if the axes of the pixel grid are not perpendicular. For almost all modern cameras $s = 0$, and many calibration programs fix it to 0.

So $K$ has 5 degrees of freedom, 4 with zero skew and 3 with zero skew and square pixels. Any upper triangular $3 \times 3$ matrix with a positive diagonal is a multiple of exactly one such $K$: divide it by its last entry.

**The inverse.** $K$ is invertible, with
$$K^{-1} = \begin{pmatrix} 1/f_x & -s/(f_x f_y) & (s c_y - c_x f_y)/(f_x f_y) \\ 0 & 1/f_y & -c_y / f_y \\ 0 & 0 & 1 \end{pmatrix}.$$
For a pixel $x = (u, v, 1)^{\mathsf T}$, the vector $K^{-1} x$ is the direction of the ray that the pixel sees, in the camera frame. Its last entry is 1, and its first two entries are $x_n$. So $K$ and $K^{-1}$ convert between pixels and normalized coordinates. Lens distortion acts on normalized coordinates: project, distort, then apply $K$ (see [Brown-Conrady distortion model](/brown-conrady-distortion-model/)).

**Angles between rays.** The angle $\theta$ between the rays of two pixels $x_1$ and $x_2$ is
$$\cos\theta = \frac{x_1^{\mathsf T} \omega x_2}{\sqrt{x_1^{\mathsf T} \omega x_1}\sqrt{x_2^{\mathsf T} \omega x_2}}, \qquad \omega = K^{-\mathsf T} K^{-1}.$$
This is the angle between $K^{-1} x_1$ and $K^{-1} x_2$. The matrix $\omega$ is the [image of the absolute conic](/image-of-the-absolute-conic/), and a known $K$ is what makes angles measurable in an image.

## Examples and non-examples

**A typical camera.** Let $f_x = f_y = 800$, $s = 0$ and $(c_x, c_y) = (320, 240)$, for an image of $640 \times 480$ pixels. The point $X_c = (0.5, -0.25, 2)$ has $x_n = (0.25, -0.125)$, so
$$u = 800 \cdot 0.25 + 320 = 520, \qquad v = 800 \cdot (-0.125) + 240 = 140.$$
The pixel $(520, 140)$ is to the right of and above the principal point, because $X > 0$ and $Y < 0$. Back the other way, $K^{-1} (520, 140, 1)^{\mathsf T} = (0.25, -0.125, 1)$, and the point at depth 2 on this ray is $X_c$ again.

**Field of view.** If the principal point is at the image center, the horizontal field of view is $2 \arctan(W / (2 f_x))$. Here $2 \arctan(320 / 800) = 2 \arctan 0.4 \approx 43.60$ degrees.

**The image center depends on the pixel convention.** With pixel centers at integer points, the image of $W = 640$ columns covers $u \in [-0.5, 639.5]$, and its center is $u = 319.5$. With the convention of the graphics [pixel](/pixel/) page and of COLMAP, where the center of pixel $u$ is at $u + 0.5$, the same image covers $[0, 640]$ and its center is 320. So a $c_x$ from such a source must be lowered by 0.5 before it is used with the formulas on this page.

**Scaling the image.** If the image is shrunk by a factor 2 in each direction, the new pixel $u'$ covers the old coordinates $[2u' - 0.5, 2u' + 1.5]$, so an old coordinate $x$ becomes $u' = x / 2 - 0.25$. Then $f_x' = f_x / 2$ and $c_x' = c_x / 2 - 0.25$: for the camera above, $f_x' = 400$ and $c_x' = 159.75$. The shift of $-0.25$ disappears in the $u + 0.5$ convention, and forgetting it is a common source of small biases.

**Non-examples.**
- A matrix with $f_y < 0$, which some graphics code uses for $Y$ up. It is a valid camera, but not an intrinsic matrix in this convention: the pages of this area keep $f_x, f_y > 0$ and put the flip in the axes.
- A lower triangular matrix, or one whose last row is not a multiple of $(0, 0, 1)$. The decomposition of $P$ into $K$ and $R$ relies on the upper triangular form.
- The $4 \times 4$ projection matrix of OpenGL. It maps to clip coordinates, keeps a depth value for the z-buffer, and is followed by the [viewport transform](/viewport-transform/). Its first two rows hold the same focal lengths and principal point, in another scale.
- A distortion model. Radial and tangential distortion are not linear in homogeneous coordinates, so no $3 \times 3$ matrix can hold them.

## Related definitions

- [Camera extrinsic parameters](/camera-extrinsic-parameters/): the rotation $R$ and the translation $t$ that take world coordinates into the camera frame used here.
- [Camera projection matrix](/camera-projection-matrix/): $P = K [R \mid t]$, the full map from world points to pixels. [Camera matrix decomposition](/camera-matrix-decomposition/) recovers $K$ from $P$ by an RQ decomposition.
- [Camera calibration](/camera-calibration/): the problem of finding $K$ (and the distortion) from images.
- [Image of the absolute conic](/image-of-the-absolute-conic/): $\omega = (K K^{\mathsf T})^{-1}$, which carries the same information as $K$; self-calibration estimates $\omega$ and then $K$ by a Cholesky factorization.
- [Pinhole camera model](/pinhole-camera-model/): the graphics page on the same camera, with the view direction $-w$ and the map to pixels in the [viewport transform](/viewport-transform/).

## References
