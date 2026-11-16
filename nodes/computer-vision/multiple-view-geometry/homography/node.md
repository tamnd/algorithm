---
tag: JZXEV2
kind: definition
slug: homography
name: Homography
aliases:
- projective transformation
- planar homography
- collineation
area: computer-vision/multiple-view-geometry
level: intro
summary: An invertible map of the projective plane given by a 3 by 3 matrix up to scale; it relates two images of a plane and two images taken from one center.
prereqs: [projective-plane]
see_also: [planar-transformation-hierarchy, homography-estimation, dlt-homography, homography-decomposition, image-stitching, image-warping, cross-ratio, fundamental-matrix]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 2.3, Projective transformations (the definition, the matrix form and the maps of lines and conics); Section 8.4, The importance of the camera centre (images from one center); Section 13.1, Homographies given the plane and vice versa"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 2.1, Geometric primitives and transformations (the 2D projective transformation) and Chapter 8, Image alignment and stitching"
---

A homography is an invertible map of the [projective plane](/projective-plane/) that sends lines to lines. Every homography is $\mathbf{x}' \sim H\mathbf{x}$ for an invertible $3 \times 3$ matrix $H$, defined up to a nonzero factor, so it has 8 degrees of freedom. In vision it relates two images of one plane, and two images of any scene taken by a camera that turns about its center. This page defines the map and its two sources; [homography estimation](/homography-estimation/) is the problem of finding $H$ from matched points, the [DLT](/dlt-homography/) is the linear method that solves it, and [homography decomposition](/homography-decomposition/) recovers the camera motion from $H$.

## Definition

A **homography** (also projectivity or projective transformation) of $\mathbb{P}^2$ is an invertible map $h : \mathbb{P}^2 \to \mathbb{P}^2$ such that three points lie on one line if and only if their images lie on one line.

**Matrix form.** A map $h$ is a homography if and only if there is an invertible real $3 \times 3$ matrix $H$ with $h(\mathbf{x}) = H\mathbf{x}$ for every point $\mathbf{x}$, in [homogeneous coordinates](/homogeneous-coordinates/). The matrices $H$ and $\lambda H$, $\lambda \ne 0$, give the same map, and only they do. So a homography has $9 - 1 = 8$ degrees of freedom. A common way to fix the scale is $\|H\|_F = 1$; the choice $H_{33} = 1$ fails when the true $H_{33}$ is 0.

In inhomogeneous coordinates, with $H = (h_{ij})$, the point $(x, y)$ goes to

$$x' = \frac{h_{11} x + h_{12} y + h_{13}}{h_{31} x + h_{32} y + h_{33}}, \qquad y' = \frac{h_{21} x + h_{22} y + h_{23}}{h_{31} x + h_{32} y + h_{33}} .$$

**Lines and conics.** If points map by $H$, a line $\mathbf{l}$ maps to $\mathbf{l}' = H^{-\mathsf T}\mathbf{l}$, because $\mathbf{l}'^{\mathsf T}\mathbf{x}' = \mathbf{l}^{\mathsf T} H^{-1} H \mathbf{x} = \mathbf{l}^{\mathsf T}\mathbf{x}$. A conic $C$ maps to $H^{-\mathsf T} C H^{-1}$.

**Four points fix it.** Given four points with no three on a line and four image points with no three on a line, there is exactly one homography that maps the first four to the second four. With fewer points it is not unique, and with three points on a line the problem is degenerate.

**The plane-induced homography.** Let a plane be $\mathbf{n}^{\mathsf T}\mathbf{X}_1 = d$ in the frame of camera 1, with $\mathbf{n}$ a unit normal and $d > 0$ its distance from the center of camera 1. Let a point have coordinates $\mathbf{X}_1$ in camera 1 and $\mathbf{X}_2 = R\mathbf{X}_1 + \mathbf{t}$ in camera 2, and let the images be $\mathbf{x}_1 \sim K_1\mathbf{X}_1$ and $\mathbf{x}_2 \sim K_2\mathbf{X}_2$, with $K_1, K_2$ the [intrinsic matrices](/camera-intrinsic-matrix/). On the plane $\mathbf{n}^{\mathsf T}\mathbf{X}_1 / d = 1$, so $\mathbf{X}_2 = (R + \mathbf{t}\mathbf{n}^{\mathsf T}/d)\mathbf{X}_1$ and

$$\mathbf{x}_2 \sim H\mathbf{x}_1, \qquad H = K_2 \left(R + \frac{\mathbf{t}\mathbf{n}^{\mathsf T}}{d}\right) K_1^{-1} .$$

Hartley and Zisserman (Section 13.1) write the plane as $\mathbf{n}^{\mathsf T}\mathbf{X} + d = 0$, so their formula has a minus sign: $K_2(R - \mathbf{t}\mathbf{n}^{\mathsf T}/d)K_1^{-1}$. Both describe the same map.

**The homography of a turning camera.** If the camera only turns about its center, $\mathbf{t} = \mathbf{0}$ and the formula gives $H = K_2 R K_1^{-1}$ for every point of the scene, whatever its depth. This is the basis of panoramas (HZ Section 8.4).

**Group.** The product of two homographies and the inverse of a homography are homographies. They form the projective group, the last class of the [hierarchy of planar transformations](/planar-transformation-hierarchy/). Every homography keeps incidence, collinearity and the [cross-ratio](/cross-ratio/).

## Examples and non-examples

- **A square to a trapezoid.** $H = \begin{pmatrix} 4 & 2 & 0 \\ 0 & 4 & 0 \\ 0 & 1 & 1 \end{pmatrix}$ sends $(0, 0)$, $(1, 0)$, $(1, 1)$, $(0, 1)$ to $(0, 0)$, $(4, 0)$, $(3, 2)$, $(1, 2)$. For example $(1, 1, 1)^{\mathsf T} \mapsto (6, 4, 2)^{\mathsf T} \sim (3, 2, 1)^{\mathsf T}$. The center $(\frac12, \frac12)$ goes to $(3, 2, \frac32)^{\mathsf T} \sim (2, \frac43)$. The third row $(0, 1, 1)$ is the line $y + 1 = 0$, which this $H$ sends to the line at infinity: the point $(x, -1)$ goes to $(4x - 2, -4, 0)^{\mathsf T}$.
- **A camera that turns.** Take $K = \operatorname{diag}(400, 400, 1)$, so the principal point is the origin, and a turn about the vertical axis with $\cos\theta = 0.8$, $\sin\theta = 0.6$: $R = \begin{pmatrix} 0.8 & 0 & 0.6 \\ 0 & 1 & 0 \\ -0.6 & 0 & 0.8 \end{pmatrix}$. Then $H = K R K^{-1} = \begin{pmatrix} 0.8 & 0 & 240 \\ 0 & 1 & 0 \\ -0.0015 & 0 & 0.8 \end{pmatrix}$. The image center $(0, 0)$ goes to $(240, 0, 0.8)^{\mathsf T} \sim (300, 0)$, which is $f \tan\theta = 400 \cdot 0.75$.
- **A plane seen from two cameras.** With $K_1 = K_2 = I$, the same $R$, $\mathbf{t} = (1, 0, 0)^{\mathsf T}$, $\mathbf{n} = (0, 0, 1)^{\mathsf T}$ and $d = 2$: $H = R + \mathbf{t}\mathbf{n}^{\mathsf T}/2 = \begin{pmatrix} 0.8 & 0 & 1.1 \\ 0 & 1 & 0 \\ -0.6 & 0 & 0.8 \end{pmatrix}$. The point $(0, 0)$ of image 1 goes to $(1.1, 0, 0.8)^{\mathsf T} \sim (1.375, 0)$.
- **Non-example: a scene with depth and a moving center.** If $\mathbf{t} \ne \mathbf{0}$ and the points are not on one plane, the image of a point depends on its depth (parallax), and no single $H$ maps all points of image 1 to their matches. The two images are then related by the [fundamental matrix](/fundamental-matrix/), which maps a point to a line, not to a point.
- **Non-example: a singular matrix.** A $3 \times 3$ matrix of rank 2 sends all of $\mathbb{P}^2$ to one line and is not invertible. It occurs for a plane through the center of camera 2, which that camera sees edge on.
- **Non-example: lens distortion.** Radial distortion bends straight lines, so two images of a plane through a real lens are related by a homography only after the distortion is removed (see the [Brown-Conrady model](/brown-conrady-distortion-model/)).

## Related definitions

- [Hierarchy of planar transformations](/planar-transformation-hierarchy/): the Euclidean, similarity and affine maps are the homographies of special forms.
- [Homography estimation](/homography-estimation/) and the [DLT for homographies](/dlt-homography/): how to compute $H$ from point matches.
- [Homography decomposition](/homography-decomposition/): the inverse of the plane formula, from $H$ back to $R$, $\mathbf{t}/d$ and $\mathbf{n}$.
- [Image warping](/image-warping/): resampling an image through $H^{-1}$ to apply a homography to pixels.
- [Image stitching](/image-stitching/): uses $H = K_2 R K_1^{-1}$ to put the photos of a panorama in one frame.
- [Fundamental matrix](/fundamental-matrix/): for two views and any plane with homography $H$, $F = [\mathbf{e}_2]_\times H$, where $\mathbf{e}_2$ is the epipole of image 2.

## References
