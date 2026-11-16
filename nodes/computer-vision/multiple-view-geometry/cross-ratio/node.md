---
tag: JB8543
kind: definition
slug: cross-ratio
name: Cross-ratio
aliases:
- anharmonic ratio
area: computer-vision/multiple-view-geometry
level: core
summary: A number computed from four collinear points that every projective transformation preserves, the basic invariant of projective geometry.
prereqs: [projective-plane]
see_also: [homography, planar-transformation-hierarchy, homogeneous-coordinates, determinant, vanishing-point-detection, image-of-the-absolute-conic]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 2.5, The projective geometry of 1D (the cross ratio of four points of a line and its invariance, and concurrent lines)"
  - book: isbn:9783642172854
    title: "Jürgen Richter-Gebert, Perspectives on Projective Geometry, Springer, 2011"
    locator: "the chapter Lines and cross-ratios (the cross-ratio by determinants and its invariance)"
---

The cross-ratio is a number computed from four points of a line. A [homography](/homography/) changes lengths, ratios of lengths and the spacing of the points, but it keeps the cross-ratio, so the cross-ratio is the basic invariant of projective geometry. This page uses the convention of Hartley and Zisserman, in which the points with coordinates $0, 1, 2, 3$ on a line give the value $1/4$. A photograph of four points on a straight edge therefore gives the same number as the points themselves, whatever the camera position.

## Definition

Let $\bar{\mathbf{x}}_1, \bar{\mathbf{x}}_2, \bar{\mathbf{x}}_3, \bar{\mathbf{x}}_4$ be four points of the projective line $\mathbb{P}^1$, each a nonzero 2-vector up to scale (see [homogeneous coordinates](/homogeneous-coordinates/)). For two points write

$$|\bar{\mathbf{x}}_i \bar{\mathbf{x}}_j| = \det \begin{pmatrix} x_{i1} & x_{j1} \\ x_{i2} & x_{j2} \end{pmatrix} .$$

The cross-ratio is

$$\operatorname{Cross}(\bar{\mathbf{x}}_1, \bar{\mathbf{x}}_2, \bar{\mathbf{x}}_3, \bar{\mathbf{x}}_4) = \frac{|\bar{\mathbf{x}}_1 \bar{\mathbf{x}}_2| \, |\bar{\mathbf{x}}_3 \bar{\mathbf{x}}_4|}{|\bar{\mathbf{x}}_1 \bar{\mathbf{x}}_3| \, |\bar{\mathbf{x}}_2 \bar{\mathbf{x}}_4|} ,$$

defined when the points $\bar{\mathbf{x}}_1, \bar{\mathbf{x}}_3$ differ and the points $\bar{\mathbf{x}}_2, \bar{\mathbf{x}}_4$ differ. Each point appears once in the numerator and once in the denominator, so the scale of each vector cancels and the value depends only on the points.

For finite points $\bar{\mathbf{x}}_i = (t_i, 1)^{\mathsf T}$, with $t_i$ the coordinate along the line, $|\bar{\mathbf{x}}_i \bar{\mathbf{x}}_j| = t_i - t_j$ and

$$\operatorname{Cross} = \frac{(t_1 - t_2)(t_3 - t_4)}{(t_1 - t_3)(t_2 - t_4)} .$$

A point at infinity $(1, 0)^{\mathsf T}$ is allowed: its factors become constants that cancel. Other books use other orders of the four points; their value is one of the six values listed below, so state the convention before you compare numbers.

**Invariance.** A homography of the line is $\bar{\mathbf{x}} \mapsto H\bar{\mathbf{x}}$ with $H$ an invertible $2 \times 2$ matrix. The matrix with columns $H\bar{\mathbf{x}}_i$ and $H\bar{\mathbf{x}}_j$ is $H$ times the matrix with columns $\bar{\mathbf{x}}_i$ and $\bar{\mathbf{x}}_j$, so $|H\bar{\mathbf{x}}_i \, H\bar{\mathbf{x}}_j| = \det H \, |\bar{\mathbf{x}}_i \bar{\mathbf{x}}_j|$. The factor $(\det H)^2$ appears in the numerator and in the denominator and cancels. So the cross-ratio does not change. A homography of the plane maps a line to a line and acts on it as a homography of $\mathbb{P}^1$, so it keeps the cross-ratio of four collinear points too.

**Four collinear points of the plane.** For points $\mathbf{x}_1, \ldots, \mathbf{x}_4$ of one line of the [projective plane](/projective-plane/), take any point $\mathbf{o}$ not on the line and replace $|\bar{\mathbf{x}}_i \bar{\mathbf{x}}_j|$ by the $3 \times 3$ [determinant](/determinant/) $\det(\mathbf{o}, \mathbf{x}_i, \mathbf{x}_j)$. The value does not depend on $\mathbf{o}$. Read in the dual way, it is also the cross-ratio of the four lines through $\mathbf{o}$ and the points: four concurrent lines have a cross-ratio, and every line that misses their common point cuts them in four points with that same cross-ratio.

**Permutations.** The 24 orders of four points give at most six values. If one order gives $\lambda$, the others give $1 - \lambda$, $1/\lambda$, $1/(1 - \lambda)$, $(\lambda - 1)/\lambda$ and $\lambda/(\lambda - 1)$.

**Harmonic sets.** Four distinct points are a harmonic set when the six values are $-1$, $2$ and $1/2$. In the convention of this page, $\operatorname{Cross}(\mathbf{a}, \mathbf{c}, \mathbf{d}, \mathbf{b}) = -1$ means that the pairs $\{\mathbf{a}, \mathbf{b}\}$ and $\{\mathbf{c}, \mathbf{d}\}$ separate each other harmonically. The midpoint of a segment and the point at infinity of its line are the classic example.

## Examples and non-examples

- **The check value.** For $t = 0, 1, 2, 3$: $\frac{(0 - 1)(2 - 3)}{(0 - 2)(1 - 3)} = \frac{1}{4}$.
- **Invariance under a homography.** The map $t \mapsto 1/(t + 1)$ is a homography of the line, with matrix $\begin{pmatrix} 0 & 1 \\ 1 & 1 \end{pmatrix}$. It sends $0, 1, 2, 3$ to $1, \frac12, \frac13, \frac14$. The cross-ratio is $\frac{(1 - \frac12)(\frac13 - \frac14)}{(1 - \frac13)(\frac12 - \frac14)} = \frac{1/24}{1/6} = \frac14$, the same value, although no length or ratio of lengths is kept.
- **The six values.** For the points $0, 1, 2, 3$ in all 24 orders the values are $\frac14$, $\frac34$, $4$, $\frac43$, $-3$ and $-\frac13$.
- **Measuring in a photograph.** Four posts stand at equal distances along a straight fence, at $0, 1, 2, 3$ units. In the image, the first three are at $0$, $2$ and $3$ pixels along the image of the fence. The fourth is at $x$ with $\frac{(0 - 2)(3 - x)}{(0 - 3)(2 - x)} = \frac14$, so $8(3 - x) = 3(2 - x)$ and $x = 3.6$. The homography $t \mapsto 3t/(t/2 + 1)$ maps $0, 1, 2, 3$ to $0, 2, 3, 3.6$, which confirms the value.
- **A harmonic set.** The points $-1$, $1$, the midpoint $0$ and the point at infinity: $\operatorname{Cross}(-1, 0, \infty, 1) = -1$.
- **Non-example: three points.** Three distinct points of a line have no invariant: a homography of the line can send any three distinct points to any other three. The cross-ratio needs four.
- **Non-example: the ratio of lengths.** For $0, 1, 3$ the ratio of the two segments is $1/2$; under $t \mapsto 1/(t + 1)$ the images $1, \frac12, \frac14$ give the ratio $2$. The simple ratio is an affine invariant, not a projective one (see the [hierarchy of planar transformations](/planar-transformation-hierarchy/)).
- **Non-example: points not on one line.** For four points in general position in the plane there is no single cross-ratio, because a homography can map any four such points to any other four.

## Related definitions

- [Projective plane](/projective-plane/): the space in which the points and lines live.
- [Homography](/homography/): the maps that keep the cross-ratio. A map of the line that keeps every cross-ratio is a homography of the line.
- [Hierarchy of planar transformations](/planar-transformation-hierarchy/): the cross-ratio is the invariant of the projective group; ratios of lengths along a line belong to the affine group.
- The formula of Laguerre gives the angle between two lines from the cross-ratio of the two lines and the two lines through their meeting point and the circular points. This is the link between angles and the [image of the absolute conic](/image-of-the-absolute-conic/).
- [Vanishing point detection](/vanishing-point-detection/): with equally spaced points on a line in the scene, the cross-ratio locates the vanishing point of the line in the image.

## References
