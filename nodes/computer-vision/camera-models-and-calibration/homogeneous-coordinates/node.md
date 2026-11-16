---
tag: CXYFKE
kind: concept
slug: homogeneous-coordinates
name: Homogeneous coordinates
aliases:
- projective coordinates
area: computer-vision/camera-models-and-calibration
level: intro
summary: Represent a point of the plane by a 3-vector up to scale, so that projective maps are linear, points at infinity are finite vectors and lines are vectors too.
prereqs: [cross-product]
see_also: [projective-plane, homography, camera-projection-matrix, homogeneous-transformation-matrix, pinhole-camera-model, cross-ratio, epipolar-geometry, graphics-pipeline]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Chapter 2, Projective geometry and transformations of 2D (points and lines, ideal points and the line at infinity, duality, projective transformations); Chapter 3 for the same ideas in 3D
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 2, Image formation (geometric primitives and 2D and 3D transformations in homogeneous coordinates)
---

Homogeneous coordinates write a point $(x, y)$ of the plane as any vector $(k x, k y, k)$ with $k \ne 0$, so that a point is a 3-vector up to a nonzero scale. With this one extra coordinate, translations, perspective projections and other projective maps all become products with a matrix, a point "at infinity" (a direction) is the ordinary vector $(x, y, 0)$, and a line is also a 3-vector. The same idea in 3D writes $(X, Y, Z)$ as $(kX, kY, kZ, k)$. This page is about the coordinates themselves and the rules for points, lines and maps in the plane. Two close pages use them for one purpose each: the robotics page [homogeneous transformation matrix](/homogeneous-transformation-matrix/) is about the $4 \times 4$ matrix of a rigid motion, which always keeps the last coordinate equal to 1, and the graphics page [pinhole camera model](/pinhole-camera-model/) is about the camera that maps a 3D point to an image point. That graphics page looks along $-w$, as is usual in graphics. The computer vision pages look along $+Z$.

## In plain words

A point on a sheet of paper has two numbers, $x$ and $y$. Add a third number, and agree that $(x, y, 1)$, $(2x, 2y, 2)$ and $(-x, -y, -1)$ all name the same point. To get the ordinary point back, divide by the last number.

Why do this? First, a vector whose last number is 0 now names a direction, a point infinitely far away where parallel lines meet. Second, a straight line also becomes three numbers, and one cross product gives the line through two points or the point where two lines cross. Third, moves, turns and the picture a camera takes all become a multiplication by a matrix. So the geometry of images turns into simple linear algebra.

## The idea

**Points.** A vector $\mathbf{x} = (x_1, x_2, x_3)^{\mathsf T} \ne 0$ is a homogeneous vector of a point. Two vectors name the same point if one is a nonzero multiple of the other; we write $\mathbf{x} \sim \mathbf{y}$. If $x_3 \ne 0$, the point is the ordinary point $(x_1 / x_3, x_2 / x_3)$. If $x_3 = 0$, it is an ideal point, or point at infinity, in the direction $(x_1, x_2)$. The zero vector names no point. The set of all classes is the [projective plane](/projective-plane/) $\mathbb{P}^2$, which is the ordinary plane plus one point at infinity for each direction. In code, `to_h` appends a 1, and `from_h` divides by the last entry and refuses a zero last entry. Vectors are column vectors.

**Lines.** The line $a x + b y + c = 0$ has the homogeneous vector $\mathbf{l} = (a, b, c)^{\mathsf T}$, also up to scale. A point $\mathbf{x}$ lies on $\mathbf{l}$ if and only if $\mathbf{l}^{\mathsf T} \mathbf{x} = 0$. This test does not depend on the two scales, so it is well defined. The vector $\mathbf{l}_\infty = (0, 0, 1)^{\mathsf T}$ is the line at infinity: it holds exactly the ideal points.

**Join and meet.** The line through two different points $\mathbf{x}$ and $\mathbf{y}$ is $\mathbf{l} = \mathbf{x} \times \mathbf{y}$, the [cross product](/cross-product/). The proof is short: $\mathbf{x}^{\mathsf T} (\mathbf{x} \times \mathbf{y}) = \det[\mathbf{x}, \mathbf{x}, \mathbf{y}] = 0$, and the same holds for $\mathbf{y}$; and $\mathbf{x} \times \mathbf{y} \ne 0$ because the two vectors are not proportional. By the same argument with the roles swapped, two different lines $\mathbf{l}$ and $\mathbf{m}$ meet at the point $\mathbf{l} \times \mathbf{m}$. Two parallel lines meet at an ideal point, so in $\mathbb{P}^2$ any two different lines meet in exactly one point. Each statement about points and lines has a dual statement with the two words swapped (HZ chapter 2).

**Maps.** A map of the plane that sends lines to lines is a product with a nonsingular $3 \times 3$ matrix $H$: $\mathbf{x}' \sim H \mathbf{x}$. This is a [homography](/homography/), with 8 degrees of freedom because the scale of $H$ does not matter. The affine map $x \mapsto A x + b$ is the special case
$$H = \begin{pmatrix} A & b \\ 0^{\mathsf T} & 1 \end{pmatrix},$$
so a translation, which is not linear in two coordinates, is linear in three. Lines map with the inverse transpose: if $\mathbf{x}' = H \mathbf{x}$, then $\mathbf{l}' = H^{-\mathsf T} \mathbf{l}$, because $\mathbf{l}'^{\mathsf T} \mathbf{x}' = \mathbf{l}^{\mathsf T} H^{-1} H \mathbf{x} = \mathbf{l}^{\mathsf T} \mathbf{x}$. An affine map keeps $\mathbf{l}_\infty$ fixed, so it keeps parallel lines parallel. A general homography moves $\mathbf{l}_\infty$ to a finite line, the horizon of a plane in a photograph.

**Space and cameras.** A point of 3D space is a 4-vector $\mathbf{X} = (X, Y, Z, 1)^{\mathsf T}$ up to scale, and the ideal point $(d_1, d_2, d_3, 0)^{\mathsf T}$ is the direction $d$. A rigid motion is the $4 \times 4$ matrix $\begin{pmatrix} R & t \\ 0^{\mathsf T} & 1 \end{pmatrix}$ of the [homogeneous transformation matrix](/homogeneous-transformation-matrix/) page. A camera is a $3 \times 4$ matrix $P$, and the image of $\mathbf{X}$ is $\mathbf{x} \sim P \mathbf{X}$ (see [camera projection matrix](/camera-projection-matrix/)). The division by the last entry at the end is the perspective division: it is the only step that is not linear, and homogeneous coordinates put it off to the very end.

**Distances need the scale.** Incidence ($\mathbf{l}^{\mathsf T}\mathbf{x} = 0$) does not depend on the scales, but a distance does. The distance from the ordinary point $\mathbf{x}$ to the line $\mathbf{l} = (a, b, c)$ is $|\mathbf{l}^{\mathsf T} \mathbf{x}| / (|x_3| \sqrt{a^2 + b^2})$. To compare two homogeneous vectors numerically, first scale both to unit norm and fix the sign, for example so that the entry of largest size is positive.

**The sign.** In $\mathbb{P}^2$ the vectors $\mathbf{x}$ and $-\mathbf{x}$ are the same point. A camera does keep one more piece of information: for $P = K[R \mid t]$ with the last row of $K$ equal to $(0, 0, 1)$, the last entry of $P (X, Y, Z, 1)^{\mathsf T}$ is the depth of the point, so its sign says whether the point is in front of the camera or behind it (HZ chapter 6). Code that tests visibility must keep the last entry of $\mathbf{X}$ equal to 1, or at least positive, and must not throw the sign away.

## Examples

All numbers below can be checked by hand.

1. **One point, many vectors.** $(2, 3)$ has the homogeneous vectors $(2, 3, 1)$, $(4, 6, 2)$ and $(-2, -3, -1)$. Dividing any of them by its last entry gives $(2, 3)$ back.
2. **The line through two points.** For $(1, 0)$ and $(0, 1)$: $(1, 0, 1) \times (0, 1, 1) = (-1, -1, 1)$. This is the line $-x - y + 1 = 0$, that is $x + y = 1$. Both points satisfy it.
3. **Parallel lines meet at infinity.** The lines $x = 1$ and $x = 2$ are $(1, 0, -1)$ and $(1, 0, -2)$. Their cross product is $(0, 1, 0)$: the ideal point in the direction of the $y$ axis, which is the direction of both lines.
4. **Two lines that meet.** $x + y = 1$ is $(1, 1, -1)$ and $x = y$ is $(1, -1, 0)$. The cross product is $(-1, -1, -2) \sim (0.5, 0.5, 1)$, the point $(0.5, 0.5)$.
5. **Translation keeps directions.** The translation by $(3, -1)$ is $T = \begin{pmatrix} 1 & 0 & 3 \\ 0 & 1 & -1 \\ 0 & 0 & 1 \end{pmatrix}$. It moves $(2, 3, 1)$ to $(5, 2, 1)$, but leaves the ideal point $(1, 0, 0)$ where it is: a direction does not move when the plane slides.
6. **A distance.** The distance from $(3, 4)$ to $x + y = 1$, with $\mathbf{l} = (1, 1, -1)$, is $|3 + 4 - 1| / \sqrt{2} = 6 / \sqrt{2} \approx 4.2426$.
7. **A vanishing point.** Take the camera $P = K [I \mid 0]$ with $K = \begin{pmatrix} 800 & 0 & 320 \\ 0 & 800 & 240 \\ 0 & 0 & 1 \end{pmatrix}$. The 3D direction $(1, 0, 1)$ is the ideal point $(1, 0, 1, 0)$, and $P (1, 0, 1, 0)^{\mathsf T} = K (1, 0, 1)^{\mathsf T} = (1120, 240, 1)$. So every 3D line with this direction has an image that runs toward the pixel $(1120, 240)$. For the line $(0, 0, 2) + s (1, 0, 1)$, the image is $(320 + 800 s / (2 + s), 240)$, which tends to $(1120, 240)$ as $s$ grows. The ideal point of 3D space has a finite image.

## Where it is used

- **Camera models.** The [camera projection matrix](/camera-projection-matrix/) $P = K [R \mid t]$, the [camera intrinsic matrix](/camera-intrinsic-matrix/) and the [camera extrinsic parameters](/camera-extrinsic-parameters/) are all written in homogeneous coordinates, and calibration methods such as [DLT resectioning](/dlt-camera-resectioning/) are linear only in this form.
- **Two-view and plane geometry.** A [homography](/homography/) maps points of a plane between two images. In [epipolar geometry](/epipolar-geometry/), the fundamental matrix maps a point of one image to a line of the other, and the epipole is a null vector. The [cross ratio](/cross-ratio/) is the basic number that a homography keeps.
- **Robotics.** Chains of rigid motions multiply as $4 \times 4$ [homogeneous transformation matrices](/homogeneous-transformation-matrix/).
- **Graphics.** The [graphics pipeline](/graphics-pipeline/) carries vertices as 4-vectors through the model, view and projection matrices, and divides by the last entry after clipping.
- **Computational geometry.** Points with integer homogeneous coordinates give predicates, such as the side of a line, as signs of determinants with no division. The sign rule above matters there too.

## References
