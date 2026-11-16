---
tag: PJSPY7
kind: theorem
slug: projective-reconstruction-theorem
name: Projective reconstruction theorem
aliases:
- projective ambiguity of reconstruction
area: computer-vision/multiple-view-geometry
level: advanced
summary: "From image matches alone the cameras and points of uncalibrated views are fixed only up to a projective transformation of space, and no better."
prereqs: [fundamental-matrix, camera-projection-matrix, homogeneous-coordinates]
see_also: [stratified-reconstruction, critical-configurations, self-calibration, sturm-triggs-factorization, optimal-triangulation, gauge-freedom, essential-matrix, trifocal-tensor]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 10.3, The projective reconstruction theorem, with the result on camera pairs that share a fundamental matrix in Chapter 9"
  - paper: doi:10.1007/3-540-55426-2_61
    title: "Olivier D. Faugeras, What can be seen in three dimensions with an uncalibrated stereo rig?, European Conference on Computer Vision (ECCV), 1992, Lecture Notes in Computer Science 588"
    locator: the result that an uncalibrated pair gives the scene up to a projective transformation
  - paper: doi:10.1109/CVPR.1992.223179
    title: "Richard Hartley, Rajiv Gupta and Tom Chang, Stereo from uncalibrated cameras, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 1992"
    locator: the reconstruction from uncalibrated views up to a projective transformation
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 11.3.3, on projective reconstruction from uncalibrated views"
---

The projective reconstruction theorem says what two uncalibrated views can and cannot tell about a scene. If the matched points fix the [fundamental matrix](/fundamental-matrix/), then any two reconstructions, each made of two [camera matrices](/camera-projection-matrix/) and a set of 3D points that project to the matches, differ by one invertible $4 \times 4$ projective transformation $H$ of space. The only exceptions are points on the baseline. Conversely, every such $H$ maps a reconstruction to another one that fits the images equally well. So without calibration, lengths, angles, parallelism and even the plane at infinity are lost, and the reconstruction is a projective one. [Stratified reconstruction](/stratified-reconstruction/) and [self-calibration](/self-calibration/) recover the lost structure from extra knowledge.

## Statement

A reconstruction of the matches $\mathbf{x}_i \leftrightarrow \mathbf{x}'_i$, $i = 1, \ldots, n$, is a triple $(P, P', \{\mathbf{X}_i\})$ of two $3 \times 4$ camera matrices of rank 3 with distinct centers and points $\mathbf{X}_i \in \mathbb{P}^3$ such that $P\mathbf{X}_i \sim \mathbf{x}_i$ and $P'\mathbf{X}_i \sim \mathbf{x}'_i$ for all $i$.

**Theorem.** Suppose the matches determine the fundamental matrix $F$ uniquely up to scale: $F$ is, up to scale, the only matrix of rank 2 with $\mathbf{x}'^{\mathsf T}_iF\mathbf{x}_i = 0$ for all $i$. Let $(P_1, P'_1, \{\mathbf{X}_{1i}\})$ and $(P_2, P'_2, \{\mathbf{X}_{2i}\})$ be two reconstructions. Then there is an invertible $4 \times 4$ matrix $H$ such that
$$P_2 \sim P_1H^{-1}, \qquad P'_2 \sim P'_1H^{-1}, \qquad \mathbf{X}_{2i} \sim H\mathbf{X}_{1i}$$
for all $i$ except those with $F\mathbf{x}_i = \mathbf{0}$ and $\mathbf{x}'^{\mathsf T}_iF = \mathbf{0}$, the matches at the two epipoles, whose points lie on the baseline.

**Converse.** For every invertible $H$, $(P_1H^{-1}, P'_1H^{-1}, \{H\mathbf{X}_{1i}\})$ is again a reconstruction.

Hartley and Zisserman state the theorem in Section 10.3, and it was found at the same time by Faugeras (1992) and by Hartley, Gupta and Chang (1992).

## In plain words

Two photos are taken with cameras whose lens and settings are not known. You match points between them and build a 3D model that explains the photos. The theorem says that the model you get is right only in a weak sense. Straight lines stay straight and points on a line stay on it. But lengths, angles and even the fact that two lines are parallel can be wrong, because a whole family of distorted models explains the same photos equally well. Any two good models are related by one such distortion, and nothing in the photos can tell them apart.

## Proof

**Step 1 (the converse).** $(P_1H^{-1})(H\mathbf{X}_{1i}) = P_1\mathbf{X}_{1i} \sim \mathbf{x}_i$, and the same for $P'_1$. The matrices $P_1H^{-1}$ and $P'_1H^{-1}$ have rank 3, and their centers $H\mathbf{C}$ and $H\mathbf{C}'$ are distinct, because $H$ is invertible.

**Step 2 (the fundamental matrix of a reconstruction).** For any camera pair $(P, P')$ with distinct centers there is a matrix $F(P, P')$ of rank 2 with $(P'\mathbf{X})^{\mathsf T}F(P, P')(P\mathbf{X}) = 0$ for all $\mathbf{X}$. In each reconstruction the matches satisfy this constraint, so by the hypothesis $F(P_1, P'_1) \sim F(P_2, P'_2) \sim F$.

**Step 3 (a canonical frame).** Let $\mathbf{C}$ be the null vector of $P$, and choose $\mathbf{w}$ with $\mathbf{w}^{\mathsf T}\mathbf{C} \ne 0$. The $4 \times 4$ matrix $G$ with rows $P$ and $\mathbf{w}^{\mathsf T}$ is invertible, and $PG^{-1}$ is the first three rows of $GG^{-1} = I$, that is, $PG^{-1} = [I \mid \mathbf{0}]$. The last column of $G^{-1}$ is sent to $\mathbf{0}$ by $P$, so it is a multiple of $\mathbf{C}$. Write $P'G^{-1} = [A \mid \mathbf{a}]$; then $\mathbf{a}$ is a nonzero multiple of $P'\mathbf{C}$, and $\mathbf{a} \ne \mathbf{0}$ because $\mathbf{C}$ is not the center of $P'$. Apply this to both reconstructions, with matrices $G_1$ and $G_2$. By Step 1 the transformed triples are again reconstructions of the same matches, and if they are related by $H$, the original ones are related by $G_2^{-1}HG_1$. So it is enough to prove the theorem for camera pairs of the form $([I \mid \mathbf{0}], [A \mid \mathbf{a}])$.

**Step 4 (the fundamental matrix of a canonical pair).** For $P = [I \mid \mathbf{0}]$ and $P' = [A \mid \mathbf{a}]$, a point $\mathbf{X} = (\mathbf{x}, s)$ gives $P\mathbf{X} = \mathbf{x}$ and $P'\mathbf{X} = A\mathbf{x} + s\mathbf{a}$. Then
$$(A\mathbf{x} + s\mathbf{a})^{\mathsf T}[\mathbf{a}]_\times A\mathbf{x} = (A\mathbf{x})^{\mathsf T}(\mathbf{a} \times A\mathbf{x}) + s\,\mathbf{a}^{\mathsf T}(\mathbf{a} \times A\mathbf{x}) = 0,$$
so $F = [\mathbf{a}]_\times A$. For every $\mathbf{u}$, $\mathbf{a}^{\mathsf T}[\mathbf{a}]_\times\mathbf{u} = \mathbf{a} \cdot (\mathbf{a} \times \mathbf{u}) = 0$, so $\mathbf{a}^{\mathsf T}F = \mathbf{0}$. Since $F$ has rank 2, its left null space is spanned by $\mathbf{a}$.

**Step 5 (two camera pairs with the same $F$).** Let $([I \mid \mathbf{0}], [A \mid \mathbf{a}])$ and $([I \mid \mathbf{0}], [\tilde A \mid \tilde{\mathbf{a}}])$ have fundamental matrices $[\mathbf{a}]_\times A$ and $[\tilde{\mathbf{a}}]_\times\tilde A$ that agree up to scale. Both $\mathbf{a}$ and $\tilde{\mathbf{a}}$ span the left null space of the same rank 2 matrix, so $\tilde{\mathbf{a}} = k\mathbf{a}$ with $k \ne 0$. Write $[\tilde{\mathbf{a}}]_\times\tilde A = \lambda[\mathbf{a}]_\times A$ with $\lambda \ne 0$. Then $[\mathbf{a}]_\times(k\tilde A - \lambda A) = 0$, so every column of $k\tilde A - \lambda A$ is a multiple of $\mathbf{a}$, and $k\tilde A - \lambda A = \mathbf{a}\mathbf{v}^{\mathsf T}$ for some $\mathbf{v}$. Put
$$H^{-1} = \begin{pmatrix} k^{-1}\lambda I & \mathbf{0} \\ k^{-1}\mathbf{v}^{\mathsf T} & k \end{pmatrix}.$$
This matrix is block triangular with nonzero diagonal blocks, so it is invertible. Also $[I \mid \mathbf{0}]H^{-1} = k^{-1}\lambda[I \mid \mathbf{0}] \sim [I \mid \mathbf{0}]$, and $[A \mid \mathbf{a}]H^{-1} = [k^{-1}(\lambda A + \mathbf{a}\mathbf{v}^{\mathsf T}) \mid k\mathbf{a}] = [\tilde A \mid \tilde{\mathbf{a}}]$. So the second camera pair is the first one times $H^{-1}$.

**Step 6 (the points).** With $H$ from Step 5, the points $H\mathbf{X}_{1i}$ and $\mathbf{X}_{2i}$ both project to $\mathbf{x}_i$ and $\mathbf{x}'_i$ under $P_2$ and $P'_2$. So both lie on the ray of $\mathbf{x}_i$ from the center $\mathbf{C}_2$ and on the ray of $\mathbf{x}'_i$ from $\mathbf{C}'_2$. Two distinct lines meet in at most one point, so $H\mathbf{X}_{1i} \sim \mathbf{X}_{2i}$ unless the two rays are the same line. The rays coincide only if both are the baseline, that is, if $\mathbf{x}_i$ and $\mathbf{x}'_i$ are the epipoles, which is the case $F\mathbf{x}_i = \mathbf{0}$ and $\mathbf{x}'^{\mathsf T}_iF = \mathbf{0}$. $\blacksquare$

## Consequences

- **Projective reconstruction is possible.** Any camera pair with the right $F$ will do, for example $P = [I \mid \mathbf{0}]$ and $P' = [[\mathbf{e}']_\times F \mid \mathbf{e}']$ with $\mathbf{e}'$ the left epipole, followed by triangulation of the matches with a projective invariant method such as [optimal triangulation](/optimal-triangulation/).
- **What is kept.** Projective transformations keep incidence (a point on a line or a plane), collinearity, tangency, and the [cross-ratio](/cross-ratio/) of four points on a line. These can be measured in a projective reconstruction.
- **What is lost.** Lengths, angles, ratios of lengths, parallelism and the plane at infinity are not kept. A projective reconstruction can even put the plane at infinity through the scene, so that the scene appears split in two.
- **The cost of the ambiguity.** $H$ has 15 degrees of freedom: these are the [gauge freedom](/gauge-freedom/) of uncalibrated reconstruction, against 7 for a similarity in the calibrated case.
- **Removing it.** Knowing the plane at infinity reduces $H$ to an affine map, and knowing the absolute conic reduces it to a similarity; this is [stratified reconstruction](/stratified-reconstruction/). With known intrinsics, the [essential matrix](/essential-matrix/) gives a reconstruction up to a similarity directly.
- **More views.** The same holds for any number of views: the cameras $P_j$ and the points are fixed up to $P_jH^{-1}$ and $H\mathbf{X}_i$, if the matches fix the multiview relations. Methods such as [Sturm-Triggs factorization](/sturm-triggs-factorization/) compute such a reconstruction.

## Tightness

- **The ambiguity is attained.** By the converse, every invertible $H$ gives a reconstruction that fits the images exactly. So no method that uses only the matches can do better than "up to a projective transformation".
- **An example.** Let $P = [I \mid \mathbf{0}]$, $P' = [I \mid (-1, 0, 0)^{\mathsf T}]$ and $\mathbf{X} = (1, 2, 4, 1)$, with images $(0.25, 0.5)$ and $(0, 0.5)$. Take $H$ equal to the identity except for the last row $(0, 0, 1, 1)$. Then $H\mathbf{X} = (1, 2, 4, 5) \sim (0.2, 0.4, 0.8, 1)$, $PH^{-1} = [I \mid \mathbf{0}]$, and $P'H^{-1}$ has rows $(1, 0, 1, -1)$, $(0, 1, 0, 0)$, $(0, 0, 1, 0)$. It maps $(0.2, 0.4, 0.8, 1)$ to $(0, 0.4, 0.8) \sim (0, 0.5)$, the same image. The plane at infinity $X_4 = 0$ is sent to the plane $Z = 1$ of the new reconstruction, where lines that were parallel now meet.
- **Unique $F$ is needed.** If the points and camera centers lie on a [critical configuration](/critical-configurations/), two fundamental matrices fit the matches, and there are reconstructions that are not projectively related. With fewer than seven matches, $F$ is never fixed.
- **Baseline points are an exception.** A match at the two epipoles is the image of every point on the baseline, so its point can be anywhere on that line in each reconstruction.
- **Distinct centers are needed.** If the two centers coincide, the views are related by a [homography](/homography/), no $F$ of rank 2 exists, and no depth can be found.

## History

Faugeras (1992) and Hartley, Gupta and Chang (1992) showed independently, at ECCV and CVPR in the same year, that two uncalibrated views give the scene up to a projective transformation, and that this is the most that can be found without further knowledge. The result led to the stratified approach of later work, in which a projective reconstruction is upgraded to an affine and then a metric one. Hartley and Zisserman give the theorem with a proof through camera pairs that share a fundamental matrix, and extend it to more views.

## References
