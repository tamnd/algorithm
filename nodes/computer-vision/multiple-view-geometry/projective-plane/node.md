---
tag: H56GXZ
kind: definition
slug: projective-plane
name: Projective plane
aliases:
- real projective plane
- P2
area: computer-vision/multiple-view-geometry
level: intro
summary: The plane plus a line of points at infinity, modeled as the lines through the origin of 3-space, in which any two distinct lines meet in exactly one point.
prereqs: [homogeneous-coordinates]
see_also: [homography, cross-ratio, planar-transformation-hierarchy, cross-product, vanishing-point-detection, epipolar-geometry, camera-projection-matrix]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 2.2, The 2D projective plane (points, lines, incidence, ideal points, the line at infinity and duality) and Section 2.6, Topology of the projective plane"
  - book: isbn:9783642172854
    title: "Jürgen Richter-Gebert, Perspectives on Projective Geometry, Springer, 2011"
    locator: "the chapter Projective planes (the axioms of a projective plane and the model of the real projective plane by lines through the origin)"
---

The real projective plane $\mathbb{P}^2$ is the set of lines through the origin of $\mathbb{R}^3$. A point of $\mathbb{P}^2$ is a nonzero 3-vector, and two vectors that differ by a nonzero factor are the same point. A line of $\mathbb{P}^2$ is also a nonzero 3-vector up to a factor, and the point $\mathbf{x}$ lies on the line $\mathbf{l}$ when $\mathbf{l}^{\mathsf T}\mathbf{x} = 0$. The page [homogeneous coordinates](/homogeneous-coordinates/) is about the coordinates; this page is about the space they describe, in which any two distinct lines meet in exactly one point, also two parallel lines.

## Definition

Write $\mathbf{x} \sim \mathbf{y}$ when $\mathbf{y} = \lambda\mathbf{x}$ for some real $\lambda \ne 0$. The real projective plane is the set of classes

$$\mathbb{P}^2 = (\mathbb{R}^3 \setminus \{\mathbf{0}\}) / \sim .$$

The vector $\mathbf{x} = (x_1, x_2, x_3)^{\mathsf T}$ gives the homogeneous coordinates of its class. The vector $\mathbf{0}$ is not a point.

**Finite points and points at infinity.** A point of the Euclidean plane $(x, y)$ is the class of $(x, y, 1)^{\mathsf T}$. A class with $x_3 \ne 0$ is a finite point, and it goes back to the Euclidean plane as $(x_1/x_3, x_2/x_3)$. A class $(x_1, x_2, 0)^{\mathsf T}$ is a point at infinity, also called an ideal point. It stands for the direction $(x_1, x_2)$ in the Euclidean plane: all lines with that direction pass through it.

**Lines.** A line is the class of a nonzero vector $\mathbf{l} = (a, b, c)^{\mathsf T}$, and its points are the $\mathbf{x}$ with

$$\mathbf{l}^{\mathsf T}\mathbf{x} = a x_1 + b x_2 + c x_3 = 0 .$$

For a finite point this is the line $ax + by + c = 0$ of the Euclidean plane. The ideal points form one line, the line at infinity $\mathbf{l}_\infty = (0, 0, 1)^{\mathsf T}$. The test $\mathbf{l}^{\mathsf T}\mathbf{x} = 0$ does not depend on the scale of $\mathbf{l}$ or $\mathbf{x}$, so incidence is well defined on classes.

**Join and meet.** The line through two distinct points and the point on two distinct lines are [cross products](/cross-product/):

$$\mathbf{l} = \mathbf{x} \times \mathbf{y}, \qquad \mathbf{x} = \mathbf{l} \times \mathbf{m} .$$

The claim behind this is short. If $\mathbf{x}$ and $\mathbf{y}$ are not multiples of each other, then $\mathbf{x} \times \mathbf{y} \ne \mathbf{0}$, and it is orthogonal to both, so the line it gives passes through both points. Every line $\mathbf{l}$ through both points is orthogonal to the plane of $\mathbb{R}^3$ spanned by $\mathbf{x}$ and $\mathbf{y}$, so $\mathbf{l}$ is a multiple of $\mathbf{x} \times \mathbf{y}$. Thus two distinct points lie on exactly one line. The same argument with the roles of points and lines exchanged shows that two distinct lines meet in exactly one point. For two parallel Euclidean lines that point is ideal.

**Duality.** Points and lines are both 3-vectors, and the incidence relation $\mathbf{l}^{\mathsf T}\mathbf{x} = 0$ is symmetric. So every true statement about points, lines and incidence gives a second true statement with the words point and line exchanged. The join and meet formulas above are one such pair.

**Shape.** Each point of $\mathbb{P}^2$ is a pair of opposite points $\pm\mathbf{x}$ of the unit sphere. So $\mathbb{P}^2$ is the sphere with opposite points glued together. It is a closed surface without a boundary, and it is not orientable. In particular, a projective line separates nothing: removing one line from $\mathbb{P}^2$ leaves one connected piece, the Euclidean plane.

## Examples and non-examples

- **One point, many vectors.** The Euclidean point $(2, 3)$ is the class of $(2, 3, 1)^{\mathsf T}$, which also contains $(4, 6, 2)^{\mathsf T}$ and $(-2, -3, -1)^{\mathsf T}$.
- **The line through two points.** For $(1, 2)$ and $(3, 4)$, $(1, 2, 1)^{\mathsf T} \times (3, 4, 1)^{\mathsf T} = (-2, 2, -2)^{\mathsf T} \sim (1, -1, 1)^{\mathsf T}$. This is the line $x - y + 1 = 0$, and both points satisfy it: $1 - 2 + 1 = 0$ and $3 - 4 + 1 = 0$.
- **Two parallel lines meet.** The lines $x = 1$ and $x = 2$ are $(1, 0, -1)^{\mathsf T}$ and $(1, 0, -2)^{\mathsf T}$. Their cross product is $(0, 1, 0)^{\mathsf T}$, the point at infinity in the direction of the $y$ axis, which is the direction of both lines.
- **Where a line meets the line at infinity.** $(1, -1, 1)^{\mathsf T} \times (0, 0, 1)^{\mathsf T} = (-1, -1, 0)^{\mathsf T} \sim (1, 1, 0)^{\mathsf T}$, the direction $(1, 1)$ of the line $x - y + 1 = 0$.
- **Non-example: the zero vector.** $(0, 0, 0)^{\mathsf T}$ is neither a point nor a line. A computation that returns it, such as the cross product of two equal points, signals that the input does not define a unique answer.
- **Non-example: the Euclidean plane.** In $\mathbb{R}^2$ two parallel lines have no common point, so the statement "two distinct lines meet in one point" fails. $\mathbb{R}^2$ is the projective plane with the line at infinity removed.
- **Non-example: $\mathbb{R}^3$ itself.** The vectors $(1, 0, 0)^{\mathsf T}$ and $(2, 0, 0)^{\mathsf T}$ are two vectors of $\mathbb{R}^3$ but one point of $\mathbb{P}^2$. Code that compares homogeneous points entry by entry treats them as different; compare them after a normalization, or test whether their cross product is zero.

## Related definitions

- [Homogeneous coordinates](/homogeneous-coordinates/): the coordinate vectors used here, also for points of 3-space.
- [Homography](/homography/): an invertible linear map of $\mathbb{R}^3$ seen as a map of $\mathbb{P}^2$. It maps lines to lines.
- [Hierarchy of planar transformations](/planar-transformation-hierarchy/): the Euclidean, similarity, affine and projective maps of $\mathbb{P}^2$ and what each one keeps.
- [Cross-ratio](/cross-ratio/): the number that four points on a line keep under every homography.
- A conic is the set of points with $\mathbf{x}^{\mathsf T} C \mathbf{x} = 0$ for a symmetric $3 \times 3$ matrix $C$. Its dual is the set of tangent lines, $\mathbf{l}^{\mathsf T} C^{-1} \mathbf{l} = 0$ when $C$ is invertible.
- The projective space $\mathbb{P}^3$ is built from $\mathbb{R}^4$ in the same way. A camera maps it to $\mathbb{P}^2$ (see [camera projection matrix](/camera-projection-matrix/)), and an image of a point at infinity of $\mathbb{P}^3$ is a vanishing point (see [vanishing point detection](/vanishing-point-detection/)).
- In two views, the epipolar lines of [epipolar geometry](/epipolar-geometry/) are lines of $\mathbb{P}^2$, and the epipole is the point where they meet.

## References
