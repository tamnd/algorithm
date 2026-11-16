---
tag: MD7SMD
kind: definition
slug: trifocal-tensor
name: Trifocal tensor
aliases:
- trifocal constraint
area: computer-vision/multiple-view-geometry
level: advanced
summary: "A 3 by 3 by 3 tensor that relates points and lines in three views, playing for three views the role that the fundamental matrix plays for two."
prereqs: [fundamental-matrix, camera-projection-matrix, homogeneous-coordinates]
see_also: [epipolar-geometry, homography, projective-reconstruction-theorem, critical-configurations, hartley-normalization, point-triangulation, essential-matrix, minimal-solver]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Chapter 15, The trifocal tensor, and Chapter 16, Computation of the trifocal tensor"
  - paper: doi:10.1109/34.400567
    title: "Amnon Shashua, Algebraic functions for recognition, IEEE Transactions on Pattern Analysis and Machine Intelligence 17(8), 1995"
    locator: the trilinear relations between the images of a point in three views
  - paper: doi:10.1023/A:1007936012022
    title: "Richard I. Hartley, Lines and points in three views and the trifocal tensor, International Journal of Computer Vision 22(2), 1997"
    locator: the tensor as a relation among lines and points in three views and its linear computation
---

The trifocal tensor is a $3 \times 3 \times 3$ array $\mathcal{T}$ built from three [camera matrices](/camera-projection-matrix/). It holds all the projective geometry of three views that image matches can reveal, just as the [fundamental matrix](/fundamental-matrix/) does for two views. It gives linear relations, called trilinearities, between the images of one point or one line in the three views. It transfers a point or a line seen in two views into the third. Unlike the fundamental matrix, it also works for lines, which give no constraint in two views, and it does not fail when the three camera centers lie on one line. It has 27 entries but only 18 degrees of freedom.

## Definition

Let $P = [I \mid \mathbf{0}]$, $P' = [A \mid \mathbf{a}_4]$ and $P'' = [B \mid \mathbf{b}_4]$ be three cameras, where any three cameras with distinct centers can be brought to this form by a projective change of frame. Let $\mathbf{a}_i$ and $\mathbf{b}_i$ be the $i$-th columns of $A$ and $B$. The trifocal tensor is the triple of $3 \times 3$ matrices
$$T_i = \mathbf{a}_i\mathbf{b}_4^{\mathsf T} - \mathbf{a}_4\mathbf{b}_i^{\mathsf T}, \qquad i = 1, 2, 3,$$
so that $\mathcal{T}_i^{jk} = a_i^jb_4^k - a_4^jb_i^k$. It is defined up to one common scale. For a point $\mathbf{x}$ in view 1, write $T(\mathbf{x}) = \sum_i x^iT_i$.

**Incidence relations.** Let a 3D line have images $\mathbf{l}$, $\mathbf{l}'$, $\mathbf{l}''$, and let a 3D point have images $\mathbf{x}$, $\mathbf{x}'$, $\mathbf{x}''$. Then:

- **Line, line, line.** $\mathbf{l}^{\mathsf T} \sim (\mathbf{l}'^{\mathsf T}T_1\mathbf{l}'', \mathbf{l}'^{\mathsf T}T_2\mathbf{l}'', \mathbf{l}'^{\mathsf T}T_3\mathbf{l}'')$.
- **Point, line, line.** $\mathbf{l}'^{\mathsf T}T(\mathbf{x})\mathbf{l}'' = 0$ for any lines $\mathbf{l}'$ through $\mathbf{x}'$ and $\mathbf{l}''$ through $\mathbf{x}''$.
- **Point, point, point.** $[\mathbf{x}']_\times T(\mathbf{x})[\mathbf{x}'']_\times = 0_{3 \times 3}$, which gives 4 independent equations.

**Transfer.** Given $\mathbf{x}$ and $\mathbf{x}'$, choose a line $\mathbf{l}'$ through $\mathbf{x}'$ that is not its epipolar line; then $\mathbf{x}'' \sim T(\mathbf{x})^{\mathsf T}\mathbf{l}'$.

**Degrees of freedom.** Three cameras have $3 \times 11 = 33$ parameters, less 15 for the projective frame, which leaves 18. The 27 entries less one scale leave 26, so the entries of a trifocal tensor satisfy 8 independent algebraic constraints. Each $T_i$ has rank at most 2.

**Epipoles and fundamental matrices.** The epipoles of the first center in views 2 and 3 are $\mathbf{e}' = \mathbf{a}_4$ and $\mathbf{e}'' = \mathbf{b}_4$. The left null vectors of the $T_i$ all lie in a plane whose normal is $\mathbf{e}'$, and the right null vectors in a plane whose normal is $\mathbf{e}''$. The fundamental matrix from view 1 to view 2 is $F_{21} \sim [\mathbf{e}']_\times[T_1, T_2, T_3]\,\mathbf{e}''$, where $[T_1, T_2, T_3]\,\mathbf{e}''$ is the matrix with columns $T_i\mathbf{e}''$.

## Examples and non-examples

**A worked tensor.** Take $P = [I \mid \mathbf{0}]$, $P' = [I \mid (-1, 0, 0)^{\mathsf T}]$ and $P'' = [I \mid (0, -1, 0)^{\mathsf T}]$, so $A = B = I$. Then
$$T_1 = \begin{pmatrix} 1 & -1 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}, \quad T_2 = \begin{pmatrix} 0 & 1 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 0 \end{pmatrix}, \quad T_3 = \begin{pmatrix} 0 & 0 & 1 \\ 0 & 0 & 0 \\ 0 & -1 & 0 \end{pmatrix}.$$
Each $T_i$ has rank 1 or 2. The formula for $F_{21}$ gives $\begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & 1 \\ 0 & -1 & 0 \end{pmatrix}$, the fundamental matrix of a sideways step along $x$.

**Point transfer.** The point $(1, 2, 4)$ has images $\mathbf{x} = (0.25, 0.5)$, $\mathbf{x}' = (0, 0.5)$ and $\mathbf{x}'' = (0.25, 0.25)$. Here
$$T(\mathbf{x}) = 0.25\,T_1 + 0.5\,T_2 + T_3 = \begin{pmatrix} 0.25 & 0.25 & 1 \\ 0 & -0.5 & 0 \\ 0 & -1 & 0 \end{pmatrix}.$$
The vertical line $\mathbf{l}' = (1, 0, 0)$ passes through $\mathbf{x}'$, and $T(\mathbf{x})^{\mathsf T}\mathbf{l}' = (0.25, 0.25, 1)$, which is $\mathbf{x}''$. The relation $[\mathbf{x}']_\times T(\mathbf{x})[\mathbf{x}'']_\times = 0$ also holds.

**Line transfer.** The lines $\mathbf{l}' = (1, 0, 0)$ in view 2 and $\mathbf{l}'' = (1, 0, -0.25)$ in view 3 are the images of the 3D line $\{(1, Y, 4)\}$. The line, line, line relation gives $\mathbf{l} = (1, 0, -0.25)$, the line $x = 0.25$ in view 1, which is indeed the image of that 3D line.

**Non-example: the epipolar line.** In the same example the horizontal line $\mathbf{l}' = (0, 1, -0.5)$ also passes through $\mathbf{x}'$, but it is the epipolar line of $\mathbf{x}$. Then $T(\mathbf{x})^{\mathsf T}\mathbf{l}' = \mathbf{0}$, and the transfer gives no point. The line through $\mathbf{x}'$ perpendicular to the epipolar line is the usual safe choice.

**Non-example: an arbitrary array.** A $3 \times 3 \times 3$ array with a slice $T_i$ of rank 3 is not a trifocal tensor, and neither is a general array of rank 2 slices: it must also satisfy the remaining internal constraints. A tensor estimated linearly from noisy data is usually not exactly trifocal and must be corrected.

**Non-example: three fundamental matrices.** The three pairwise fundamental matrices of three views do not replace the tensor. If the three centers lie on one line, the two epipolar lines of $\mathbf{x}$ and $\mathbf{x}'$ in view 3 coincide, so point transfer by epipolar lines fails, while transfer by the trifocal tensor still works.

## Related definitions

- **Fundamental matrix.** The [fundamental matrix](/fundamental-matrix/) is the two-view analog. The trifocal tensor determines the fundamental matrices of all three pairs, and through them the [epipolar geometry](/epipolar-geometry/).
- **Induced homographies.** For a fixed line $\mathbf{l}'$ in view 2, the matrix with columns $T_i^{\mathsf T}\mathbf{l}'$ is the [homography](/homography/) from view 1 to view 3 induced by the plane that back-projects $\mathbf{l}'$.
- **Calibrated trifocal tensor.** With normalized image coordinates, the cameras are rigid motions, and the tensor plays the role that the [essential matrix](/essential-matrix/) plays for two views.
- **Quadrifocal tensor.** A $3 \times 3 \times 3 \times 3$ tensor relates four views. There are no independent constraints of this kind for five or more views.
- **Reconstruction.** The tensor fixes the three cameras up to a projective transformation, the three-view form of the [projective reconstruction theorem](/projective-reconstruction-theorem/). Its computation from at least 7 point triples or 13 line triples uses [Hartley normalization](/hartley-normalization/) and a linear method followed by a correction that enforces the internal constraints.

## References
