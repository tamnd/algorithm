---
tag: XAA2FV
kind: model
slug: affine-camera-model
name: Affine camera model
aliases:
- weak perspective camera
- orthographic camera
- paraperspective camera
area: computer-vision/camera-models-and-calibration
level: core
summary: A camera whose last row of P is (0, 0, 0, 1), so parallel lines stay parallel; a good model when the depth of the scene is small next to its distance.
prereqs: [camera-projection-matrix]
see_also: [camera-projection-matrix, tomasi-kanade-factorization, pinhole-camera-model, camera-intrinsic-matrix, dlt-camera-resectioning, homogeneous-coordinates, least-squares-problem]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 6.3, Cameras at infinity (affine cameras, the error of the affine approximation, and the hierarchy of orthographic, scaled orthographic, weak perspective and affine projection); Chapter 7 for the estimation of an affine camera
  - paper: doi:10.1007/BF00129684
    title: Carlo Tomasi and Takeo Kanade, Shape and motion from image streams under orthography, a factorization method, International Journal of Computer Vision 9(2), 1992, 137-154
    locator: the rank 3 property of the centered measurement matrix under orthographic projection, and the factorization that follows from it
  - paper: doi:10.1561/0600000023
    title: Peter Sturm, Srikumar Ramalingam, Jean-Philippe Tardif, Simone Gasparini and Joao Barreto, Camera models and fundamental concepts used in geometric computer vision, Foundations and Trends in Computer Graphics and Vision 6(1-2), 2011, 1-183
    locator: the part on affine and other parallel projection models
---

An affine camera is a [camera projection matrix](/camera-projection-matrix/) whose last row is $(0, 0, 0, 1)$. It maps a 3D point to the image by an affine map, a linear map plus a shift, with no division by the depth. So parallel lines in space stay parallel in the image, and the ratio of lengths along a line is kept. A real lens does not do this, but a pinhole camera that sees a shallow object from far away comes very close, because then all points have about the same depth. The affine camera is the limit of a finite camera whose center moves to infinity, and it is the model behind [Tomasi-Kanade factorization](/tomasi-kanade-factorization/). The graphics page [pinhole camera model](/pinhole-camera-model/) mentions parallel projection as the limit of a far camera; its view direction is $-w$, and here it is $+Z$.

## The machine

**The map.** An affine camera is a $3 \times 4$ matrix
$$P_A = \begin{pmatrix} m_{11} & m_{12} & m_{13} & t_1 \\ m_{21} & m_{22} & m_{23} & t_2 \\ 0 & 0 & 0 & 1 \end{pmatrix} = \begin{pmatrix} M_2 & \mathbf{t} \\ 0^{\mathsf T} & 1 \end{pmatrix},$$
where the $2 \times 3$ block $M_2$ has rank 2. The image of the world point $X$ is
$$x = M_2 X + \mathbf{t}.$$
In [homogeneous coordinates](/homogeneous-coordinates/), $P_A (X, 1)^{\mathsf T} = (M_2 X + \mathbf{t}, 1)$ already has last entry 1, so there is no perspective division. The model has 8 degrees of freedom: the 8 free entries of $P_A$.

**Domain.** Every point of space has an image, with no front and no back: the model has no depth sign and no field of view. The image of a point at infinity $(d, 0)$ is $(M_2 d, 0)$, again at infinity. That is the reason why parallel lines stay parallel.

**The center and the inverse.** The left $3 \times 3$ block of $P_A$ is singular, so the center is the point at infinity $(d, 0)$ with $M_2 d = 0$. All rays are parallel to $d$: this is a parallel projection. The map has no inverse. A pixel $x$ is the image of the whole line of points $X_0 + \lambda d$ with $M_2 X_0 = x - \mathbf{t}$.

**The hierarchy** (HZ section 6.3). With $R$ a rotation with rows $r_1^{\mathsf T}, r_2^{\mathsf T}, r_3^{\mathsf T}$, the affine cameras used in practice are, from the most restricted:
- **Orthographic projection**, 5 degrees of freedom: $M_2 = \begin{pmatrix} r_1^{\mathsf T} \\ r_2^{\mathsf T} \end{pmatrix}$. The point is dropped along the optical axis $r_3$ onto the image.
- **Scaled orthographic projection**, 6 degrees of freedom: $M_2 = k \begin{pmatrix} r_1^{\mathsf T} \\ r_2^{\mathsf T} \end{pmatrix}$, one scale $k$.
- **Weak perspective projection**, 7 degrees of freedom: $M_2 = \operatorname{diag}(\alpha_x, \alpha_y) \begin{pmatrix} r_1^{\mathsf T} \\ r_2^{\mathsf T} \end{pmatrix}$, two scales.
- **The general affine camera**, 8 degrees of freedom: $M_2 = \begin{pmatrix} \alpha_x & s \\ 0 & \alpha_y \end{pmatrix} \begin{pmatrix} r_1^{\mathsf T} \\ r_2^{\mathsf T} \end{pmatrix}$, which is every $M_2$ of rank 2.

**Paraperspective projection** (Aloimonos, 1990) is also an affine camera, but its parameters depend on a reference point $X_0$ of the scene, usually the centroid, at depth $Z_0$. It first moves each point onto the plane $Z = Z_0$ along the direction from the camera center to $X_0$, and then projects that plane by the true camera. In camera coordinates with focal length $f$, $u - c_x = (f / Z_0)\,(X - (X_0 / Z_0)(Z - Z_0))$, and the same for $v$. It keeps the first order effect of the position of the object off the optical axis.

**As an approximation.** Take a pinhole camera with focal length $f$ in pixels and a point at depth $Z_0 + \Delta$ in the camera frame. The pinhole gives $u - c_x = f X / (Z_0 + \Delta)$, and weak perspective projection, which uses the same depth $Z_0$ for all points, gives $f X / Z_0$. The error is
$$f X \left(\frac{1}{Z_0} - \frac{1}{Z_0 + \Delta}\right) = \frac{f X \Delta}{Z_0 (Z_0 + \Delta)},$$
which is small when the depth relief $\Delta$ is small next to $Z_0$ and the point is close to the optical axis ($X$ small). This is the content of the error analysis in HZ section 6.3.

## What it counts

The model predicts the image position $x = M_2 X + \mathbf{t}$ of each point, in pixels. A fit of the model to matches $X_i \leftrightarrow x_i$ minimizes the reprojection error $\sum_i \|x_i - M_2 X_i - \mathbf{t}\|^2$. Because the image coordinates are linear in the 8 parameters, this geometric error is the same as the algebraic error, so a single [least squares problem](/least-squares-problem/) gives the maximum likelihood camera under isotropic Gaussian noise on the image points. Each match gives 2 equations, so 4 matches with points that are not coplanar fix the 8 parameters. A finite camera needs 6 matches and a nonlinear fit for the same cost function.

## Relation to other models

- **Finite camera.** Let a finite camera with $P = K [R \mid t]$ move back along its optical axis by a distance $D$ and zoom in by the factor $(t_3 + D) / t_3$, so that the image of the object keeps its size. As $D \to \infty$, $P$ (after a rescale) tends to an affine camera (HZ section 6.3). So the affine camera is the limit of a camera at infinity, which is why HZ calls the class cameras at infinity.
- **Graphics.** Parallel projections in graphics, for example the orthographic view of a CAD drawing, are orthographic projection with a viewport transform after it.
- **Homography.** Restricted to a world plane, an affine camera is an affine map of that plane, a homography with last row $(0, 0, 1)$, with 6 degrees of freedom instead of 8.

## Known results in the model

- **Parallelism and centroids** (theorem). An affine camera maps parallel lines to parallel lines, and the centroid of a set of points to the centroid of their images. Proof: the map $X \mapsto M_2 X + \mathbf{t}$ is affine, so it keeps the means of points and sends a direction $d$ to the direction $M_2 d$.
- **Linear estimation** (theorem). From $n \ge 4$ matches with points not all on one plane, the affine camera of least reprojection error is the solution of a linear least squares problem in its 8 entries, as shown above. No iteration is needed.
- **Rank 3 factorization** (theorem; Tomasi and Kanade, 1992). Take $N$ affine views of $n$ points, subtract from the image points of each view their centroid, and stack the results into a $2N \times n$ matrix. Without noise, this matrix equals the product of the stacked $2N \times 3$ matrix of the $M_2$ blocks and the $3 \times n$ matrix of centered points, so its rank is at most 3. A truncated [SVD](/singular-value-decomposition/) then gives motion and shape up to an affine transformation of space; Tomasi and Kanade fix it to a similarity with the constraints of orthographic projection.
- **Depth reversal** (theorem). Under orthographic projection, a scene and its mirror image in a plane parallel to the image give the same image. More views do not remove this: with $S = \operatorname{diag}(1, 1, -1)$, the mirrored points $S X$ and the rotations $S R S$ give exactly the same images as $X$ and $R$ in every view, because the first two rows of $S R S$ applied to $S X$ give the first two rows of $R$ applied to $X$.
- **Size of the error** (a worked bound). At $f = 800$, a point at $X = 1$ off the axis, with $Z_0 = 10$ and $\Delta = 0.5$, the weak perspective error is $800 \cdot 1 \cdot 0.5 / (10 \cdot 10.5) \approx 3.81$ pixels: $76.19$ pixels from the principal point against $80$. For a point at $X = 2.5$, $Z = 10.5$ with reference point $X_0 = 2$, $Z_0 = 10$, the true value is $190.48$, weak perspective gives $200$ (error $9.52$) and paraperspective projection gives $192.0$ (error $1.52$). These numbers come from the formulas above and hold only for this example.

## References
