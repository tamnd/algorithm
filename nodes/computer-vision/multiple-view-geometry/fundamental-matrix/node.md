---
tag: AZMVF2
kind: definition
slug: fundamental-matrix
name: Fundamental matrix
aliases:
- F matrix
area: computer-vision/multiple-view-geometry
level: core
summary: "The rank 2 matrix F of two uncalibrated views, defined up to scale, with x2^T F x1 = 0 for every pair of matching pixels x1 in image 1 and x2 in image 2. It has 7 degrees of freedom."
prereqs: [epipolar-geometry, camera-intrinsic-matrix]
see_also: [essential-matrix, eight-point-algorithm, normalized-eight-point-algorithm, seven-point-algorithm, sampson-distance, projective-reconstruction-theorem, stereo-rectification, homography]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 9.2, The fundamental matrix F (the geometric and algebraic derivations, the correspondence condition and the summary of properties in Table 9.1); Section 9.5, Retrieving the camera matrices"
  - paper: doi:10.1109/34.601246
    title: "Richard I. Hartley, In defense of the eight-point algorithm, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(6), 1997, 580-593"
    locator: the linear estimation of F from point matches and the rank 2 condition
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 11.3, Two-frame structure from motion"
---

The fundamental matrix $F$ is the $3 \times 3$ matrix that writes the [epipolar geometry](/epipolar-geometry/) of two views in pixel coordinates: matching points satisfy $\mathbf{x}_2^{\mathsf T}F\mathbf{x}_1 = 0$, with the point of the second image on the left. It needs no knowledge of the [intrinsic matrices](/camera-intrinsic-matrix/), which is why it is the matrix of two uncalibrated views. When the intrinsics are known, $F$ and the [essential matrix](/essential-matrix/) carry the same information, through $F = K_2^{-\mathsf T}EK_1^{-1}$. This page defines $F$ and lists its properties; the methods that find it from matches are the [eight-point algorithm](/eight-point-algorithm/), its [normalized form](/normalized-eight-point-algorithm/) and the [seven-point algorithm](/seven-point-algorithm/).

## Definition

Let two cameras have the matrices $P_1 = K_1[I \mid \mathbf{0}]$ and $P_2 = K_2[R \mid \mathbf{t}]$, so that a point with coordinates $\mathbf{X}_1$ in the frame of camera 1 has $\mathbf{X}_2 = R\mathbf{X}_1 + \mathbf{t}$ in the frame of camera 2. Here $K_1$ and $K_2$ are invertible, $R$ is a rotation, and $\mathbf{t} \ne \mathbf{0}$, so the two centers differ. The **fundamental matrix** of the ordered pair (camera 1, camera 2) is
$$F = K_2^{-\mathsf T}[\mathbf{t}]_\times R\,K_1^{-1},$$
taken up to a nonzero scale, where $[\mathbf{t}]_\times$ is the [skew matrix](/skew-symmetric-matrix-of-a-vector/) of $\mathbf{t}$.

**The correspondence condition.** If $\mathbf{x}_1 \sim P_1\mathbf{X}$ and $\mathbf{x}_2 \sim P_2\mathbf{X}$ are the images of one point $\mathbf{X}$, written as homogeneous pixel vectors, then
$$\mathbf{x}_2^{\mathsf T}F\mathbf{x}_1 = 0 .$$
The proof: $K_1^{-1}\mathbf{x}_1 \sim \mathbf{X}_1$ and $K_2^{-1}\mathbf{x}_2 \sim \mathbf{X}_2$, and $\mathbf{X}_2^{\mathsf T}[\mathbf{t}]_\times R\mathbf{X}_1 = \mathbf{X}_2^{\mathsf T}(\mathbf{t} \times (\mathbf{X}_2 - \mathbf{t})) = \mathbf{X}_2^{\mathsf T}(\mathbf{t} \times \mathbf{X}_2) = 0$. Hartley and Zisserman write the same condition as $\mathbf{x}'^{\mathsf T}F\mathbf{x} = 0$, with $\mathbf{x}'$ in the second image. Some libraries store the transpose; their matrix is $F^{\mathsf T}$ in this convention.

**General cameras.** For any two camera matrices with different centers, $F = [\mathbf{e}_2]_\times P_2P_1^{+}$, where $P_1^{+}$ is the pseudo-inverse of $P_1$ and $\mathbf{e}_2 = P_2\mathbf{C}_1$ is the image of the first center (Hartley and Zisserman, Section 9.2). For the two cameras above this gives the formula of the definition, up to scale.

**Properties.** Let $F$ be a fundamental matrix.
- *Rank 2.* $\det F = 0$ and $F \ne 0$. The null vector $\mathbf{e}_1$ ($F\mathbf{e}_1 = \mathbf{0}$) is the epipole of image 1, the image of the second center, and the left null vector $\mathbf{e}_2$ ($F^{\mathsf T}\mathbf{e}_2 = \mathbf{0}$) is the epipole of image 2.
- *Seven degrees of freedom.* $F$ has 9 entries, minus 1 for the scale and 1 for the condition $\det F = 0$.
- *Epipolar lines.* The epipolar line of $\mathbf{x}_1$ in image 2 is $\mathbf{l}_2 = F\mathbf{x}_1$, and that of $\mathbf{x}_2$ in image 1 is $\mathbf{l}_1 = F^{\mathsf T}\mathbf{x}_2$.
- *Order.* The matrix of the pair in the reverse order (camera 2, camera 1) is $F^{\mathsf T}$.
- *Every rank 2 matrix is one.* For every real $3 \times 3$ matrix $F$ of rank 2 there are cameras with this fundamental matrix, for example $P_1 = [I \mid \mathbf{0}]$ and $P_2 = [[\mathbf{e}_2]_\times F \mid \mathbf{e}_2]$ (Hartley and Zisserman, Section 9.5). So the conditions "rank 2" and "fundamental matrix" are the same for real matrices.
- *Projective ambiguity.* $F$ does not change when both cameras are multiplied on the right by the same invertible $4 \times 4$ matrix. So from $F$ alone the cameras, and the scene, are fixed only up to a projective transformation of space; this is the [projective reconstruction theorem](/projective-reconstruction-theorem/).
- *Change of image coordinates.* If the images are moved by homographies, $\mathbf{x}_1 \mapsto H_1\mathbf{x}_1$ and $\mathbf{x}_2 \mapsto H_2\mathbf{x}_2$, then $F$ becomes $H_2^{-\mathsf T}FH_1^{-1}$. The [normalized eight-point algorithm](/normalized-eight-point-algorithm/) uses this with similarities.

## Examples and non-examples

**The running example of this group.** Take $R = \begin{pmatrix} 0.8 & 0 & 0.6 \\ 0 & 1 & 0 \\ -0.6 & 0 & 0.8 \end{pmatrix}$, $\mathbf{t} = (1, 0, 0)$, and $K_1 = K_2 = K = \begin{pmatrix} 500 & 0 & 320 \\ 0 & 500 & 240 \\ 0 & 0 & 1 \end{pmatrix}$. The essential matrix is $E = [\mathbf{t}]_\times R = \begin{pmatrix} 0 & 0 & 0 \\ 0.6 & 0 & -0.8 \\ 0 & 1 & 0 \end{pmatrix}$, and $K^{-1}$ has rows $(1/500, 0, -0.64)$, $(0, 1/500, -0.48)$ and $(0, 0, 1)$. Then $K^{-\mathsf T}EK^{-1}$, multiplied by $500^2$, is
$$F \sim \begin{pmatrix} 0 & 0 & 0 \\ 0.6 & 0 & -592 \\ -144 & 500 & 22080 \end{pmatrix} .$$
- The point $\mathbf{X}_1 = (0, 0, 5)$ has $\mathbf{X}_2 = (4, 0, 4)$, so $\mathbf{x}_1 = (320, 240)$ and $\mathbf{x}_2 = (820, 240)$. The line $\mathbf{l}_2 = F(320, 240, 1)^{\mathsf T} = (0, -400, 96000)$ is $v = 240$, and $\mathbf{x}_2$ is on it.
- The point $\mathbf{X}_1 = (0, 2.5, 5)$ has $\mathbf{x}_1 = (320, 490)$ and $\mathbf{x}_2 = (820, 552.5)$. Then $\mathbf{l}_2 = (0, -400, 221000)$ is $v = 552.5$, and $\mathbf{l}_1 = F^{\mathsf T}(820, 552.5, 1)^{\mathsf T} = (187.5, 500, -305000)$ passes through $(320, 490)$, since $60000 + 245000 - 305000 = 0$.
- The epipoles: $\mathbf{e}_1 = K(0.8, 0, 0.6)^{\mathsf T} \sim (2960/3, 240, 1) \approx (986.67, 240)$, and $F\mathbf{e}_1 = \mathbf{0}$. The first row of $F$ is zero, so $F^{\mathsf T}(1, 0, 0)^{\mathsf T} = \mathbf{0}$ and $\mathbf{e}_2 = (1, 0, 0)$, a point at infinity: the epipolar lines of image 2 are the rows.
- $\det F = 0$, and $\|F\|_F \approx 22094.06$. The canonical form with norm 1 and a positive largest entry has $F_{33} \approx 0.99936$. Its entries differ in size by a factor of about $4 \cdot 10^4$, which is one reason why estimating $F$ on raw pixels is badly conditioned.

**Rectified cameras.** With $R = I$, $K_1 = K_2$ and the second center at $(b, 0, 0)$, $F \sim \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{pmatrix}$, and $\mathbf{x}_2^{\mathsf T}F\mathbf{x}_1 = v_1 - v_2$. The derivation is on the [epipolar geometry](/epipolar-geometry/) page.

**Pure translation.** With $R = I$ and $K_1 = K_2 = K$, the identity $K^{-\mathsf T}[\mathbf{t}]_\times K^{-1} = (\det K)^{-1}[K\mathbf{t}]_\times$ gives $F \sim [\mathbf{e}]_\times$ with $\mathbf{e} = K\mathbf{t}$, a skew-symmetric matrix. For the $K$ above and a forward step $\mathbf{t} = (0, 0, 1)$, $\mathbf{e} = (320, 240, 1)$, the principal point, and $F \sim \begin{pmatrix} 0 & -1 & 240 \\ 1 & 0 & -320 \\ -240 & 320 & 0 \end{pmatrix}$. Both epipoles are $\mathbf{e}$, and the epipolar lines are the lines through it.

**Non-examples.**
- The identity matrix has rank 3, so it is not a fundamental matrix: its "epipolar lines" $\mathbf{l}_2 = \mathbf{x}_1$ do not pass through one common point.
- The matrix $F_0$ that a linear solve returns from noisy matches usually has rank 3. It becomes a fundamental matrix only after the rank step of the eight-point algorithm.
- Two images from one center (a camera that only rotates) have no fundamental matrix: $\mathbf{t} = \mathbf{0}$ gives $F = 0$. The images are related by a [homography](/homography/) instead.
- A homography $H$ between the two images is not a fundamental matrix, since it has rank 3. But for every plane, $F = [\mathbf{e}_2]_\times H_\pi$ with the homography $H_\pi$ that the plane induces.

## Related definitions

- [Essential matrix](/essential-matrix/): the fundamental matrix of normalized coordinates, $E = K_2^{\mathsf T}FK_1$. It has 5 degrees of freedom and two equal singular values.
- [Epipolar geometry](/epipolar-geometry/): the epipoles, epipolar lines and planes that $F$ encodes.
- [Homography](/homography/): the other $3 \times 3$ map between two views, for a plane or for a camera that only rotates. A homography is compatible with $F$ when $H^{\mathsf T}F$ is skew-symmetric.
- [Camera projection matrix](/camera-projection-matrix/): $F$ is computed from two of them, and gives two of them back up to a projective transformation.
- [Sampson distance](/sampson-distance/): the first-order distance of a match from the constraint $\mathbf{x}_2^{\mathsf T}F\mathbf{x}_1 = 0$.
- [Trifocal tensor](/trifocal-tensor/): the three-view analog; it contains the three fundamental matrices of its view pairs.
- The affine fundamental matrix of two [affine cameras](/affine-camera-model/) has a zero upper-left $2 \times 2$ block and 4 degrees of freedom.

## References
