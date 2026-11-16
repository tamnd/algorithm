---
tag: DJ7NTA
kind: definition
slug: essential-matrix
name: Essential matrix
aliases:
- E matrix
area: computer-vision/multiple-view-geometry
level: core
summary: "The matrix E = [t]x R of two calibrated views, with x2^T E x1 = 0 for matching normalized image points. It has 5 degrees of freedom and singular values (s, s, 0)."
prereqs: [fundamental-matrix, camera-intrinsic-matrix]
see_also: [essential-matrix-characterization, essential-matrix-decomposition, five-point-algorithm, relative-pose-problem, epipolar-geometry, cheirality, skew-symmetric-matrix-of-a-vector, special-orthogonal-group]
sources:
  - paper: doi:10.1038/293133a0
    title: "H. C. Longuet-Higgins, A computer algorithm for reconstructing a scene from two projections, Nature 293, 1981, 133-135"
    locator: "the matrix of the bilinear constraint between the two images of a point, and the recovery of the motion from it"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 9.6, The essential matrix (the definition, Result 9.17 on the singular values, and Results 9.18 and 9.19 on the factorizations)"
  - book: isbn:9780387008936
    title: "Yi Ma, Stefano Soatto, Jana Kosecka and S. Shankar Sastry, An Invitation to 3-D Vision, Springer, 2004"
    locator: "Chapter 5, Section 5.1.1 (the epipolar constraint and the essential matrix) and Section 5.1.2 (elementary properties of the essential matrix)"
  - paper: doi:10.1109/34.41368
    title: "Thomas S. Huang and Olivier D. Faugeras, Some properties of the E matrix in two-view motion estimation, IEEE Transactions on Pattern Analysis and Machine Intelligence 11(12), 1989, 1310-1312"
    locator: the conditions on the singular values of E
---

The essential matrix $E$ is the $3 \times 3$ matrix that writes the [epipolar geometry](/epipolar-geometry/) of two calibrated views. In normalized image coordinates, matching points satisfy $\hat{\mathbf{x}}_2^{\mathsf T}E\hat{\mathbf{x}}_1 = 0$, and $E = [\mathbf{t}]_\times R$ is built directly from the relative pose. It is the [fundamental matrix](/fundamental-matrix/) with the [intrinsic matrices](/camera-intrinsic-matrix/) removed. Longuet-Higgins (1981) introduced it and showed how to recover the motion from it. This page defines $E$ and its basic properties. The exact algebraic test for a matrix to be essential is the [characterization theorem](/essential-matrix-characterization/), the pose comes back by [decomposition](/essential-matrix-decomposition/), and the [five-point algorithm](/five-point-algorithm/) finds $E$ from the fewest matches.

## Definition

Let $R$ be a rotation ($R^{\mathsf T}R = I$, $\det R = 1$) and $\mathbf{t} \in \mathbb{R}^3$, $\mathbf{t} \ne \mathbf{0}$. The **essential matrix** of the relative pose $(R, \mathbf{t})$, with $\mathbf{X}_2 = R\mathbf{X}_1 + \mathbf{t}$, is
$$E = [\mathbf{t}]_\times R ,$$
taken up to a nonzero scale. Here $[\mathbf{t}]_\times$ is the [skew matrix](/skew-symmetric-matrix-of-a-vector/) with $[\mathbf{t}]_\times\mathbf{b} = \mathbf{t} \times \mathbf{b}$. A real $3 \times 3$ matrix is called an essential matrix when it equals $[\mathbf{t}]_\times R$ for some such pair.

**The constraint.** Let $\hat{\mathbf{x}}_1 = K_1^{-1}\mathbf{x}_1$ and $\hat{\mathbf{x}}_2 = K_2^{-1}\mathbf{x}_2$ be the normalized images of one point. Then $\hat{\mathbf{x}}_1 \sim \mathbf{X}_1$, $\hat{\mathbf{x}}_2 \sim \mathbf{X}_2$, and
$$\hat{\mathbf{x}}_2^{\mathsf T}E\hat{\mathbf{x}}_1 = 0 ,$$
because $\mathbf{X}_2^{\mathsf T}[\mathbf{t}]_\times R\mathbf{X}_1 = \mathbf{X}_2^{\mathsf T}(\mathbf{t} \times (\mathbf{X}_2 - \mathbf{t})) = 0$. In pixels this is the fundamental matrix constraint with
$$F = K_2^{-\mathsf T}EK_1^{-1}, \qquad E = K_2^{\mathsf T}FK_1 .$$

**Degrees of freedom.** The rotation has 3, and $\mathbf{t}$ has 3, but the scale of $E$ is not fixed by the constraint, so only the direction of $\mathbf{t}$ counts. That gives $3 + 2 = 5$. A common way to fix the scale is $\|\mathbf{t}\| = 1$, which gives $\|E\|_F = \sqrt2$.

**Properties.** Let $E = [\mathbf{t}]_\times R$.
- *Singular values.* $EE^{\mathsf T} = [\mathbf{t}]_\times[\mathbf{t}]_\times^{\mathsf T} = \|\mathbf{t}\|^2 I - \mathbf{t}\mathbf{t}^{\mathsf T}$, whose eigenvalues are $\|\mathbf{t}\|^2$, $\|\mathbf{t}\|^2$ and 0. So the singular values of $E$ are $(\|\mathbf{t}\|, \|\mathbf{t}\|, 0)$, and $E$ has rank 2.
- *The converse.* A real $3 \times 3$ matrix with singular values $(s, s, 0)$, $s > 0$, is an essential matrix. With the cubic test: a real $E \ne 0$ is essential if and only if $\det E = 0$ and $2EE^{\mathsf T}E - \operatorname{tr}(EE^{\mathsf T})E = 0$. Both are parts of the [characterization theorem](/essential-matrix-characterization/), which also shows why the word "real" is needed.
- *Epipoles.* $E^{\mathsf T}\mathbf{t} = R^{\mathsf T}[\mathbf{t}]_\times^{\mathsf T}\mathbf{t} = \mathbf{0}$, so $\mathbf{e}_2 \sim \mathbf{t}$, the image of the first center in camera 2. And $E(R^{\mathsf T}\mathbf{t}) = \mathbf{t} \times \mathbf{t} = \mathbf{0}$, so $\mathbf{e}_1 \sim R^{\mathsf T}\mathbf{t}$, the direction of the second center $-R^{\mathsf T}\mathbf{t}$ seen from camera 1.
- *Four factorizations.* Up to scale, an essential matrix is $[\mathbf{t}]_\times R$ for exactly four pairs with $\|\mathbf{t}\| = 1$: two rotations and two signs of $\mathbf{t}$. The [decomposition](/essential-matrix-decomposition/) page proves this, and [cheirality](/cheirality/) picks the right pair.
- *Closest essential matrix.* For a real matrix $G = U\operatorname{diag}(s_1, s_2, s_3)V^{\mathsf T}$, the matrix with singular values $(m, m, 0)$ closest to $G$ in the Frobenius norm is $U\operatorname{diag}(\bar m, \bar m, 0)V^{\mathsf T}$ with $\bar m = (s_1 + s_2)/2$. The [eight-point algorithm](/eight-point-algorithm/) proves this with von Neumann's trace inequality and uses it to make a linear estimate essential.

## Examples and non-examples

**The running example.** For $R = \begin{pmatrix} 0.8 & 0 & 0.6 \\ 0 & 1 & 0 \\ -0.6 & 0 & 0.8 \end{pmatrix}$ and $\mathbf{t} = (1, 0, 0)$,
$$E = \begin{pmatrix} 0 & 0 & 0 \\ 0.6 & 0 & -0.8 \\ 0 & 1 & 0 \end{pmatrix}, \qquad EE^{\mathsf T} = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix} = I - \mathbf{t}\mathbf{t}^{\mathsf T} .$$
- The singular values are $(1, 1, 0)$. An SVD with two rotations is $U = \begin{pmatrix} 0 & 0 & -1 \\ 0 & 1 & 0 \\ 1 & 0 & 0 \end{pmatrix}$ and $V = \begin{pmatrix} 0 & 0.6 & -0.8 \\ 1 & 0 & 0 \\ 0 & -0.8 & -0.6 \end{pmatrix}$; one can check that $U\operatorname{diag}(1, 1, 0)V^{\mathsf T} = E$ and $\det U = \det V = 1$.
- $E^{\mathsf T}(1, 0, 0)^{\mathsf T} = \mathbf{0}$ and $E(0.8, 0, 0.6)^{\mathsf T} = \mathbf{0}$, with $(0.8, 0, 0.6) = R^{\mathsf T}\mathbf{t}$.
- The point $\mathbf{X}_1 = (0, 0, 5)$ goes to $\mathbf{X}_2 = (4, 0, 4)$; with $\hat{\mathbf{x}}_1 = (0, 0, 1)$ and $\hat{\mathbf{x}}_2 = (1, 0, 1)$, $E\hat{\mathbf{x}}_1 = (0, -0.8, 0)$ and $\hat{\mathbf{x}}_2^{\mathsf T}E\hat{\mathbf{x}}_1 = 0$.
- The same pose seen with $K = \begin{pmatrix} 500 & 0 & 320 \\ 0 & 500 & 240 \\ 0 & 0 & 1 \end{pmatrix}$ in both cameras gives the matrix $F$ on the [fundamental matrix](/fundamental-matrix/) page, and $K^{\mathsf T}FK$ gives back $E$ up to scale.

**Pure translation.** With $R = I$, $E = [\mathbf{t}]_\times$, a skew-symmetric matrix. For $\mathbf{t} = (0, 0, 1)$, $E = \begin{pmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}$, and the constraint reads $u_1v_2 - u_2v_1 = 0$: the two image points and the image center lie on one line.

**Non-examples.**
- $E = 0$ (from $\mathbf{t} = \mathbf{0}$, a camera that only rotates) is excluded by the definition. Such images have a [homography](/homography/), not an essential matrix.
- $G = \operatorname{diag}(1, 2, 0)$ has rank 2, so it is a fundamental matrix of some pair of cameras, but its nonzero singular values differ, so it is not essential. The cubic test sees this: $GG^{\mathsf T}G = \operatorname{diag}(1, 8, 0)$, $\operatorname{tr}(GG^{\mathsf T}) = 5$, and $2GG^{\mathsf T}G - 5G = \operatorname{diag}(-3, 6, 0) \ne 0$.
- $G = \operatorname{diag}(3, 1, 0.5)$, a typical rank 3 output of a linear solve, is not essential. The closest essential matrix in the Frobenius norm is $\operatorname{diag}(2, 2, 0)$, at distance $\sqrt{1 + 1 + 0.25} = 1.5$.
- The complex matrix $\begin{pmatrix} 1 & i & 0 \\ i & -1 & 0 \\ 0 & 0 & 0 \end{pmatrix}$ satisfies $\det E = 0$ and $EE^{\mathsf T} = 0$, so it passes the cubic test, but it has rank 1. It is not an essential matrix; the cubic test characterizes essential matrices only among real matrices.

## Related definitions

- [Fundamental matrix](/fundamental-matrix/): the same constraint in pixels, with 7 degrees of freedom. Every essential matrix is a fundamental matrix of the normalized images, but not the other way round.
- [Essential matrix characterization](/essential-matrix-characterization/): the theorem that singular values $(s, s, 0)$, or the cubic equations, characterize real essential matrices.
- [Skew matrix of a vector](/skew-symmetric-matrix-of-a-vector/) and [rotation group](/special-orthogonal-group/): the two factors of $E$.
- [Relative pose problem](/relative-pose-problem/): the problem of finding $(R, \mathbf{t})$, usually through $E$.
- [Homography](/homography/): for a plane $\mathbf{n}^{\mathsf T}\mathbf{X}_1 = d$, the normalized homography $H = R + \mathbf{t}\mathbf{n}^{\mathsf T}/d$ satisfies $E = [\mathbf{t}]_\times H$, because $[\mathbf{t}]_\times\mathbf{t} = \mathbf{0}$.
- [Camera extrinsic parameters](/camera-extrinsic-parameters/): the pose of each camera; $(R, \mathbf{t})$ here is the pose of camera 2 relative to camera 1.

## References
