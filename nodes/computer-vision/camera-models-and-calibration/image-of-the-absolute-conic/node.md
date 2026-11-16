---
tag: 733GXD
kind: concept
slug: image-of-the-absolute-conic
name: Image of the absolute conic
aliases:
- IAC
area: computer-vision/camera-models-and-calibration
level: advanced
summary: "The conic omega = (K K^T)^-1 where the absolute conic projects. It depends only on K, gives the angle between any two rays, and finding it calibrates the camera."
prereqs: [camera-intrinsic-matrix, projective-plane, homogeneous-coordinates]
see_also: [camera-calibration, zhang-calibration-method, vanishing-point-calibration, kruppa-equations, self-calibration, stratified-reconstruction, cholesky-decomposition, image-stitching]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 3.6, The absolute conic; Section 8.5, Camera calibration and the image of the absolute conic; Section 8.6, Vanishing points and vanishing lines; Section 8.8, Determining calibration K from a single view; Section 19.6 on rotating cameras
  - paper: doi:10.1109/34.888718
    title: Zhengyou Zhang, A flexible new technique for camera calibration, IEEE Transactions on Pattern Analysis and Machine Intelligence 22(11), 2000, 1330-1334
    locator: the two constraints that each view of a plane puts on B = K^-T K^-1, and their reading as the images of the circular points on the image of the absolute conic
  - paper: "Stephen J. Maybank and Olivier D. Faugeras, A theory of self-calibration of a moving camera, International Journal of Computer Vision 8(2), 1992, 123-151"
    title: Stephen J. Maybank and Olivier D. Faugeras, A theory of self-calibration of a moving camera, International Journal of Computer Vision 8(2), 1992, 123-151
    locator: the use of the image of the absolute conic as the unknown of camera self-calibration
  - paper: doi:10.1109/CVPR.1997.609388
    title: Bill Triggs, Autocalibration and the absolute quadric, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 1997, 609-614
    locator: the dual of the absolute conic (the absolute dual quadric) and its projection K K^T in each image
---

The image of the absolute conic (IAC) is the conic $\omega = (K K^{\mathsf T})^{-1} = K^{-\mathsf T} K^{-1}$ in the image plane of a camera with [intrinsic matrix](/camera-intrinsic-matrix/) $K$. It is the image of the absolute conic, a conic of 3D space that lies on the plane at infinity and has no real points. Because the absolute conic does not move when the camera rotates or translates, its image depends on $K$ only. So $\omega$ holds the same information as $K$, and every statement about angles between rays becomes a statement about $\omega$. This is the reason why [Zhang's method](/zhang-calibration-method/), [vanishing point calibration](/vanishing-point-calibration/), the [Kruppa equations](/kruppa-equations/) and [self-calibration](/self-calibration/) all solve for $\omega$ or its dual first, and get $K$ from it.

## In plain words

Imagine a circle that is so far away that it stays in the same place in every photo, wherever you stand and wherever you look. Its picture then cannot tell you where the camera is or how it turns. It can only tell you about the inside of the camera: the focal length and the point where the optical axis meets the image. The absolute conic is such a far object. It is imaginary, so it never shows up as a curve that you can see. But it still has an exact formula in each image, and that formula is a compact way to write the camera's internal settings. If you know two directions in the scene are at right angles, the image of this object must agree with that fact. Enough such facts pin it down, and so they calibrate the camera.

## The idea

**The absolute conic.** In projective 3-space a point is $X = (X_1, X_2, X_3, X_4)^{\mathsf T}$ up to scale, and the plane at infinity $\pi_\infty$ holds the points with $X_4 = 0$, which are the directions $d = (X_1, X_2, X_3)$. The absolute conic $\Omega_\infty$ is the set of points on $\pi_\infty$ with
$$X_1^2 + X_2^2 + X_3^2 = 0, \qquad X_4 = 0,$$
that is, the directions with $d^{\mathsf T} d = 0$ (HZ Section 3.6). No real direction satisfies this, so $\Omega_\infty$ has only complex points. A Euclidean motion $X \mapsto R X + t$ acts on directions by $d \mapsto R d$, and $(R d)^{\mathsf T} (R d) = d^{\mathsf T} d$. So every rotation and translation maps $\Omega_\infty$ to itself; a similarity does too, because a scale factor does not change the equation. HZ shows the converse: a projective map of space that fixes $\Omega_\infty$ (as a set) is a similarity. The absolute conic is a different object from the IAC: it lives on a plane of 3D space, and the IAC lives in the image.

**Its image.** Take the camera $P = K [R \mid t]$. A point at infinity $(d, 0)$ projects to $x = K R d$, which is the vanishing point of the direction $d$. So $d = R^{\mathsf T} K^{-1} x$, and $d^{\mathsf T} d = 0$ becomes
$$x^{\mathsf T} K^{-\mathsf T} R R^{\mathsf T} K^{-1} x = x^{\mathsf T} (K K^{\mathsf T})^{-1} x = 0.$$
The rotation cancels and $t$ never appears. So the image of $\Omega_\infty$ is the conic with matrix $\omega = (K K^{\mathsf T})^{-1}$, for every pose of the camera (HZ Section 8.5). Its dual conic, the set of lines tangent to it, has the matrix $\omega^\ast = \omega^{-1} = K K^{\mathsf T}$. This dual is called the DIAC. It is the image of the absolute dual quadric of Triggs (1997), and the Kruppa equations are written in terms of it.

**Facts that follow.**
- $\omega$ is symmetric and positive definite, because $x^{\mathsf T} \omega x = \lVert K^{-1} x \rVert^2$. So $\omega$ has no real points, as $\Omega_\infty$ has none.
- $\omega$ is defined up to scale, and it has 5 degrees of freedom, the same number as $K$. The [Cholesky decomposition](/cholesky-decomposition/) gives $K$ back: if $\omega = L L^{\mathsf T}$ with $L$ lower triangular and a positive diagonal, then $L = K^{-\mathsf T}$ up to scale. So $K$ is the inverse of $L^{\mathsf T}$, divided by its last entry.
- **Angles.** The ray of pixel $x$ has the direction $K^{-1} x$ in the camera frame. So the angle $\theta$ between the rays of $x_1$ and $x_2$ is
$$\cos\theta = \frac{x_1^{\mathsf T} \omega x_2}{\sqrt{x_1^{\mathsf T} \omega x_1} \sqrt{x_2^{\mathsf T} \omega x_2}}.$$
The value does not change if $\omega$, $x_1$ or $x_2$ is scaled, because the scale of each appears the same number of times above and below the bar (HZ Section 8.5).
- **Right angles.** Two vanishing points $v_1$ and $v_2$ come from perpendicular directions if and only if $v_1^{\mathsf T} \omega v_2 = 0$. Each such pair is one linear equation on the entries of $\omega$.
- **A plane and its normal.** A scene plane with normal direction $n$ has the vanishing line $l = K^{-\mathsf T} R n$, and the normal has the vanishing point $v = K R n$. So $l = \omega v$: the vanishing line is the polar of the vanishing point of the normal with respect to $\omega$ (HZ Section 8.6).
- **Circular points.** Every plane meets $\Omega_\infty$ in two complex points, its circular points. Their images lie on $\omega$. For a plane imaged by the homography $H = [h_1 \; h_2 \; h_3]$, the images are $h_1 \pm i h_2$, and the real and imaginary parts of $(h_1 + i h_2)^{\mathsf T} \omega (h_1 + i h_2) = 0$ are the two equations $h_1^{\mathsf T} \omega h_2 = 0$ and $h_1^{\mathsf T} \omega h_1 = h_2^{\mathsf T} \omega h_2$ of Zhang's method.
- **Simple cameras.** Write $\omega = (\omega_{ij})$. Zero skew holds if and only if $\omega_{12} = 0$. Zero skew and square pixels ($f_x = f_y$) hold if and only if $\omega_{12} = 0$ and $\omega_{11} = \omega_{22}$ (HZ Section 8.8). Each known property is one more linear equation.
- **A camera that only rotates.** Two views of a camera that turns about its center are related by the homography $H = K R K^{-1}$ (if $K$ does not change). Then $\omega = H^{-\mathsf T} \omega H^{-1}$, which gives linear equations on $\omega$ from the homographies alone (HZ Section 19.6).

## Examples

**The matrix for a common camera.** Let $f_x = f_y = 800$, $s = 0$ and $(c_x, c_y) = (320, 240)$. Then
$$K^{-1} = \frac{1}{800} \begin{pmatrix} 1 & 0 & -320 \\ 0 & 1 & -240 \\ 0 & 0 & 800 \end{pmatrix}, \qquad \omega = K^{-\mathsf T} K^{-1} = \frac{1}{640000} \begin{pmatrix} 1 & 0 & -320 \\ 0 & 1 & -240 \\ -320 & -240 & 800000 \end{pmatrix}.$$
The last entry is $f^2 + c_x^2 + c_y^2 = 640000 + 102400 + 57600 = 800000$. As the rules above say, $\omega_{12} = 0$ and $\omega_{11} = \omega_{22}$. In the rest of this example we drop the factor $1/640000$, because the angle formula does not need it.

**An angle.** Take the principal point $x_1 = (320, 240, 1)$ and the pixel $x_2 = (1120, 240, 1)$, which is $800$ pixels to the right. Then $x_1^{\mathsf T} \omega x_2 = 640000$, $x_1^{\mathsf T} \omega x_1 = 640000$ and $x_2^{\mathsf T} \omega x_2 = 1280000$, so $\cos\theta = 640000 / \sqrt{640000 \cdot 1280000} = 1 / \sqrt 2$ and $\theta = 45$ degrees. This agrees with the direct view: $x_2$ is one focal length to the side of the principal point. For $x_3 = (1120, 1040, 1)$ the ray direction is $(1, 1, 1)$, and the same formula gives $\cos\theta = 1 / \sqrt 3$, so the angle to the optical axis is about $54.74$ degrees. A script with exact fractions gave these values.

**A horizon line.** The camera looks horizontally, so $R = I$, and the ground plane has the normal $n = (0, 1, 0)$ (the $Y$ axis points down). The normal has the vanishing point $v = K n = (0, 800, 0)$, a point at infinity of the image. Its polar is $\omega v \propto (0, 800, -192000) \propto (0, 1, -240)$, which is the line $v = 240$. So the horizon goes through the principal point row, as it must for a level camera.

**A non-example.** A real ellipse drawn on a wall is a conic, and it projects to a conic, but its image changes when the camera moves. The IAC is special because no motion of the camera changes it. Also, $\omega$ is not the absolute conic itself: $\Omega_\infty$ is in 3D space on $\pi_\infty$, and $\omega$ is a $3 \times 3$ matrix of the image.

## Where it is used

- **Calibration from a plane.** [Zhang's method](/zhang-calibration-method/) solves for $B = \omega$ from the images of the circular points of a planar target. Each view gives two linear equations.
- **Calibration from vanishing points.** [Vanishing point calibration](/vanishing-point-calibration/) uses $v_i^{\mathsf T} \omega v_j = 0$ for three vanishing points of perpendicular directions, plus zero skew and square pixels, to get $\omega$ and so $K$ from one image. With these assumptions, the principal point is the orthocenter of the triangle of the three points.
- **Self-calibration.** With no target at all, the [Kruppa equations](/kruppa-equations/) put constraints on $\omega^\ast = K K^{\mathsf T}$ from the [fundamental matrix](/fundamental-matrix/) of each image pair. The method of the absolute dual quadric uses $\omega_i^\ast \sim P_i Q_\infty^\ast P_i^{\mathsf T}$ in each view. See [self-calibration](/self-calibration/).
- **Metric upgrade.** In [stratified reconstruction](/stratified-reconstruction/), $\omega$ in one view and the plane at infinity give the transformation from an affine to a metric reconstruction.
- **Panoramas.** For [image stitching](/image-stitching/) with a camera that only rotates, the relation $\omega = H^{-\mathsf T} \omega H^{-1}$ gives the focal length from the homographies between the photos.
- **Measuring angles.** With a known $K$, the angle formula gives the angle between two scene directions from their vanishing points, for example to check if two walls are perpendicular.
