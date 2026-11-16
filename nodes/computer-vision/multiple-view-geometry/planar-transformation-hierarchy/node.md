---
tag: R6THDN
kind: concept
slug: planar-transformation-hierarchy
name: Hierarchy of planar transformations
aliases:
- projective transformation hierarchy
area: computer-vision/multiple-view-geometry
level: intro
summary: The nested groups of Euclidean, similarity, affine and projective maps of the plane, each with more freedom and fewer invariants than the one before.
prereqs: [homography]
see_also: [projective-plane, cross-ratio, homography-estimation, image-warping, image-registration, stratified-reconstruction, rigid-body-transformation, image-stitching]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 2.4, A hierarchy of transformations (the four classes, their matrices, degrees of freedom and invariants, summed up in Table 2.1) and Section 2.7, Recovery of affine and metric properties from images"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 2.1, Geometric primitives and transformations (the 2D transformations from translation to projective, with their degrees of freedom)"
---

The hierarchy of planar transformations sorts the invertible maps of the plane that send lines to lines into four nested classes: Euclidean, similarity, affine and projective. Each class contains the one before it, has more degrees of freedom (3, 4, 6 and 8), and keeps fewer geometric properties. The projective class is the class of all [homographies](/homography/). The hierarchy tells which model to fit between two images and which measurements survive in an image.

## In plain words

Draw a square on a sheet of paper and move the sheet on a table: the square keeps its size and its angles. Copy it with a zoom: it is still a square, only bigger. Look at the sheet through a slanted glass that stretches it: the square becomes a parallelogram, but parallel sides stay parallel. Take a photo of the sheet from the side: the square becomes a general four-sided shape, and only straight lines stay straight. Each step allows more change and keeps less. A model with more freedom fits more pairs of images, but it also needs more matched points to fix it.

## The idea

All four classes act on points of the [projective plane](/projective-plane/) as $\mathbf{x}' = H\mathbf{x}$ with an invertible $3 \times 3$ matrix $H$. They differ in the form of $H$. Below, $R$ is a $2 \times 2$ rotation, $s > 0$ a scale, $A$ an invertible $2 \times 2$ matrix, $\mathbf{t}$ a translation and $\mathbf{v}$ a 2-vector.

| Class | Matrix | Degrees of freedom | New invariants (in addition to those of the rows below) |
|---|---|---|---|
| Euclidean | $\begin{pmatrix} R & \mathbf{t} \\ \mathbf{0}^{\mathsf T} & 1 \end{pmatrix}$ | 3 | length, area |
| Similarity | $\begin{pmatrix} sR & \mathbf{t} \\ \mathbf{0}^{\mathsf T} & 1 \end{pmatrix}$ | 4 | angle, ratio of any two lengths, the circular points |
| Affine | $\begin{pmatrix} A & \mathbf{t} \\ \mathbf{0}^{\mathsf T} & 1 \end{pmatrix}$ | 6 | parallel lines, ratio of lengths on parallel lines, ratio of areas, centroids, the line at infinity |
| Projective | $\begin{pmatrix} A & \mathbf{t} \\ \mathbf{v}^{\mathsf T} & v \end{pmatrix}$ | 8 | collinearity, concurrency, incidence and tangency, the [cross-ratio](/cross-ratio/) |

Read the last column from the bottom up. A projective map keeps only the properties in the last row. An affine map keeps those and the properties in its own row, and so on, so a Euclidean map keeps everything in the table. The degrees of freedom count the free entries: a rotation angle and two translations for the Euclidean class; one more for the scale; four entries of $A$ and two of $\mathbf{t}$ for the affine class; nine entries less one for the overall scale for the projective class. Hartley and Zisserman also count the reflections, with $\det R = -1$, in the Euclidean class; they keep the same invariants.

Each class is a group: the product of two maps of a class and the inverse of a map are in the class again. Three facts explain the invariants.

- An affine map has last row $(0, 0, 1)$, so it sends a point at infinity $(x_1, x_2, 0)^{\mathsf T}$ to a point at infinity. It keeps the line at infinity, so parallel lines, which meet on that line, stay parallel. A projective map with $\mathbf{v} \ne \mathbf{0}$ moves the line at infinity to a finite line, the horizon of the plane in the image.
- A similarity keeps the two complex circular points $(1, \pm i, 0)^{\mathsf T}$. Angles are defined by them, so a map that keeps them keeps angles.
- Any map $\mathbf{x} \mapsto H\mathbf{x}$ keeps the relation $\mathbf{l}^{\mathsf T}\mathbf{x} = 0$ when lines map as $\mathbf{l} \mapsto H^{-\mathsf T}\mathbf{l}$. So incidence and everything built from it, such as collinearity and the cross-ratio, survive every class.

Hartley and Zisserman also write a projective map as a product of three parts: a similarity, an affine part whose $2 \times 2$ block is upper triangular with determinant 1, and a projective part that only moves the line at infinity. Undoing the projective part from an image is affine rectification; undoing the affine part too is metric rectification.

The same ladder exists in 3D, with 6, 7, 12 and 15 degrees of freedom, and it is the basis of [stratified reconstruction](/stratified-reconstruction/).

## Examples

- **A unit square under each class.** A Euclidean map gives a unit square in another place. A similarity gives a square of another size. An affine map gives a parallelogram. A projective map can give any quadrilateral with no three corners on a line.
- **What a projective map does not keep.** The homography $H = \begin{pmatrix} 4 & 2 & 0 \\ 0 & 4 & 0 \\ 0 & 1 & 1 \end{pmatrix}$ sends the corners $(0, 0)$, $(1, 0)$, $(1, 1)$, $(0, 1)$ of the unit square to $(0, 0)$, $(4, 0)$, $(3, 2)$, $(1, 2)$, a trapezoid. The center $(\frac12, \frac12)$ goes to $(2, \frac43)$. The centroid of the four new corners is $(2, 1)$, so the centroid is not kept, as expected for a map that is not affine. The point $(2, \frac43)$ is where the diagonals of the trapezoid cross, because the center lies on both diagonals of the square and incidence is kept.
- **What an affine map keeps.** On the bottom edge $y = 0$ the same $H$ acts as $x \mapsto 4x$, so the midpoint $(\frac12, 0)$ goes to the midpoint $(2, 0)$. On the line $y = 0$ the third row gives $w = 1$, so this $H$ acts there as an affine map of the line.
- **Counting points.** A pair of matched points gives two equations. So two pairs fix a similarity, three pairs in general position fix an affine map, and four pairs with no three on a line fix a homography. A Euclidean map has 3 degrees of freedom, so two pairs over-determine it.

## Where it is used

- **Choosing the model of image alignment.** [Image registration](/image-registration/) and [image warping](/image-warping/) use a translation or a similarity for small motions of a scanner, an affine map for a far camera with a narrow field of view, and a homography for a plane seen from any camera or for any scene seen by a camera that only rotates. [Homography estimation](/homography-estimation/) and [image stitching](/image-stitching/) use the projective class.
- **The size of a minimal sample.** A robust fit draws the smallest set of matches that fixes the model: 2 pairs for a similarity, 3 for an affine map and 4 for a homography.
- **Rectification of a plane.** From an image of a plane, a vanishing line gives the affine rectification and the image of a right angle or a known ratio gives the metric rectification. After it, angles and length ratios can be measured on the plane.
- **Invariants for recognition.** The cross-ratio of four collinear points and the parallelism of lines under an affine model are features that do not depend on the camera position.
- **Rigid motions.** The Euclidean class is the 2D case of a [rigid body transformation](/rigid-body-transformation/).

## References
