---
tag: VTG4C0
kind: algorithm
slug: camera-matrix-decomposition
name: Camera matrix decomposition
aliases:
- RQ decomposition of the camera matrix
- KRt decomposition
area: computer-vision/camera-models-and-calibration
level: core
summary: Recover K, R and the camera center from a camera matrix by an RQ decomposition of its left 3 by 3 block and the null vector of P.
solves: []
model: real-ram
complexity:
  vars: {n: "the number of entries of P, fixed at 12"}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1984
  people: [Sundaram Ganapathy]
  note: Ganapathy showed in 1984 how to recover the position, orientation and internal parameters of a camera from its 3 by 4 matrix. Hartley and Zisserman give the form with an RQ factorization of the left block.
prereqs: [camera-projection-matrix, qr-decomposition]
see_also: [dlt-camera-resectioning, camera-calibration, camera-intrinsic-matrix, camera-extrinsic-parameters, cholesky-decomposition, singular-value-decomposition, zhang-calibration-method, gram-schmidt-process]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 6.2, The projective camera (finding the camera center and the decomposition of the camera matrix into K, R and C by RQ); Appendix 4 (the RQ decomposition by Givens rotations)
  - paper: doi:10.1016/0167-8655(84)90007-2
    title: Sundaram Ganapathy, Decomposition of transformation matrices for robot vision, Pattern Recognition Letters 2(6), 1984, 401-412
    locator: the whole paper (camera parameters from the 3 by 4 transformation matrix)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 11, Structure from motion and SLAM (the part on camera matrix estimation and its decomposition)
---

Camera matrix decomposition takes a finite [camera projection matrix](/camera-projection-matrix/) $P = [M \mid p_4]$, known only up to scale, and returns the [intrinsic matrix](/camera-intrinsic-matrix/) $K$, the rotation $R$, the translation $t$ and the camera center $C$ of the [extrinsic parameters](/camera-extrinsic-parameters/), with $P \sim K [R \mid t]$. It factors the left $3 \times 3$ block as $M = K R$ by an RQ decomposition (upper triangular times orthogonal), fixes the signs so that $K$ has a positive diagonal and $\det R = +1$, and gets $C$ as the right null vector of $P$. It does no estimation: its input is a matrix, not images. Among the close pages, [camera calibration](/camera-calibration/) is the problem of finding $K$ and the distortion; [DLT resectioning](/dlt-camera-resectioning/) finds $P$ from 2D to 3D matches, and this page is its usual second step; [Zhang's method](/zhang-calibration-method/) and [Tsai's method](/tsai-calibration-method/) find $K$ from a pattern without going through a general $P$.

## In plain words

Suppose a friend hands you the one $3 \times 4$ table of numbers that describes a camera, and you want the usual camera settings back: the focal lengths, the principal point, where the camera stands and where it points. The left $3 \times 3$ part of the table is the product of the lens matrix, which has zeros below its diagonal, and the turn of the camera. A standard matrix tool splits a matrix into exactly such a product. The split is unique once you require positive focal lengths and a true turn, not a mirror. The position of the camera is the one point of space that the table sends to nothing, and the last column gives the shift.

## The problem

**Input.** A real $3 \times 4$ matrix $P = [M \mid p_4]$ with $\det M \ne 0$. $P$ is a camera matrix up to an unknown nonzero scale, which may be negative.

**Output.** An intrinsic matrix $K$ (upper triangular, positive diagonal, $K_{33} = 1$), a rotation $R$ ($R^{\mathsf T} R = I$, $\det R = +1$), a vector $t$ and the center $C = -R^{\mathsf T} t$, with $P = \lambda K [R \mid t]$ for some $\lambda \ne 0$. The conventions are those of the area: $X_c = R X_w + t$, the camera looks along $+Z$, and the depth of a point in front of the camera is positive.

If $\det M = 0$, $P$ is not a finite camera (for example it is an [affine camera](/affine-camera-model/)), and no such factorization exists.

## The algorithm

```pseudo id=main
DECOMPOSE-CAMERA(P)
L1  M <- P[:, 1..3] ; p4 <- P[:, 4]
L2  if det M = 0 then error "not a finite camera"
L3  if det M < 0 then M <- -M ; p4 <- -p4
L4  (K, R) <- RQ(M)                   ▷ K upper triangular, R orthogonal
L5  for i <- 1 to 3: if K[i][i] < 0 then negate column i of K and row i of R
L6  t <- K^-1 p4
L7  K <- K / K[3][3]
L8  C <- -R^T t
L9  return K, R, t, C
```

Line L3 removes a negative scale: $P$ and $-P$ are the same camera, and only the sign with $\det M > 0$ can give $\det R = +1$. Line L4 is the RQ decomposition. It is the QR decomposition turned around: reverse the rows of $M$, transpose, take a [QR decomposition](/qr-decomposition/), and undo the reversal (the reference code does this; HZ Appendix 4 uses Givens rotations instead). Line L5 makes the diagonal of $K$ positive. Negating column $i$ of $K$ and row $i$ of $R$ leaves the product $K R$ unchanged, since it inserts $D^2 = I$ with $D$ a diagonal sign matrix. After L3 and L5, $\det R = \det M / \det K > 0$, so $R$ is a rotation. Line L6 must use $K$ before its scale is removed in L7; then $K [R \mid t] = [M \mid p_4]$ exactly. Line L8 is the center, which also is the right null vector of $P$: $P (C, 1)^{\mathsf T} = \lambda K (R C + t) = 0$.

## Example

Take $K_0 = \begin{pmatrix} 4 & 1 & 3 \\ 0 & 5 & 2 \\ 0 & 0 & 1 \end{pmatrix}$, the rotation by 90 degrees about $Z$, $R_0 = \begin{pmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}$, and $t_0 = (1, 2, 4)$. Hide the scale by $\lambda = -2$:
$$P = -2 K_0 [R_0 \mid t_0] = \begin{pmatrix} -2 & 8 & -6 & -36 \\ -10 & 0 & -4 & -36 \\ 0 & 0 & -2 & -8 \end{pmatrix}.$$

| line | value |
|---|---|
| L1, L2 | $M = \begin{pmatrix} -2 & 8 & -6 \\ -10 & 0 & -4 \\ 0 & 0 & -2 \end{pmatrix}$, $\det M = -160$ |
| L3 | negate: $M = \begin{pmatrix} 2 & -8 & 6 \\ 10 & 0 & 4 \\ 0 & 0 & 2 \end{pmatrix}$, $p_4 = (36, 36, 8)$ |
| L4 | $K = \begin{pmatrix} 8 & 2 & 6 \\ 0 & 10 & 4 \\ 0 & 0 & 2 \end{pmatrix}$, $R = R_0$ |
| L5 | the diagonal $(8, 10, 2)$ is already positive |
| L6 | back substitution: $t_3 = 8/2 = 4$, $t_2 = (36 - 4 \cdot 4)/10 = 2$, $t_1 = (36 - 2 \cdot 2 - 6 \cdot 4)/8 = 1$ |
| L7 | $K = K / 2 = K_0$ |
| L8 | $R^{\mathsf T} t = (2, -1, 4)$, so $C = (-2, 1, -4)$ |

The right null vector of $P$, scaled to last entry 1, is also $(-2, 1, -4, 1)$, and the Cholesky route of the variants below gives the same $K_0$. Without line L3, the RQ step would have to give a $K$ with a negative diagonal entry or an $R$ with $\det R = -1$.

## Correctness

Line L3 makes $\det M > 0$ by a change of sign that does not change the camera. Every real square matrix has an RQ decomposition $M = K Q$, and since $M$ is nonsingular, the diagonal of $K$ has no zero, so the sign fix of line L5 is possible and keeps the product. The determinant of the new orthogonal factor is $\det M / \det K$, a quotient of positive numbers, so it is $+1$. Lines L6 and L7 then give $P = \lambda K [R \mid t]$ with $\lambda = \pm K_{33} \ne 0$. For uniqueness, two such factorizations give an upper triangular matrix with a positive diagonal that is a multiple of an orthogonal matrix, so it is the identity times a positive scale, and the condition $K_{33} = 1$ fixes the scale. The full proof is in the proof file below.

## Complexity

The input has a fixed size. In the [real RAM](/real-ram/) with square roots, each line does a fixed number of operations: the determinant, an RQ decomposition of a $3 \times 3$ matrix by three Householder reflections (or three Givens rotations), and a $3 \times 3$ triangular solve. So the time and the extra space are $\Theta(1)$. The DLT that usually comes before it costs $\Theta(n)$ for $n$ points, so the decomposition is never the expensive step.

## Properties

- **Exact.** In exact arithmetic the output reproduces $P$ up to scale exactly.
- **Unique.** With the sign rules ($K$ with a positive diagonal and $K_{33} = 1$, $\det R = +1$), the factors $K$, $R$ and $t$ are unique for each finite camera.
- **Scale free.** $P$ and $\mu P$ give the same output for every $\mu \ne 0$, including negative $\mu$.
- **No constraints imposed.** The output $K$ has whatever skew and aspect ratio $P$ implies. If $P$ came from noisy data, the skew is small but not zero, even when the real camera has none.

## Variants and improvements

- **Cholesky route.** Since $M M^{\mathsf T} = \lambda^2 K R R^{\mathsf T} K^{\mathsf T} = \lambda^2 K K^{\mathsf T}$, the [Cholesky decomposition](/cholesky-decomposition/) of $(M M^{\mathsf T})^{-1} = L L^{\mathsf T}$ gives $K \propto (L^{\mathsf T})^{-1}$; then $R = K^{-1} M / \lambda$ with the sign of $\det M$. The reference tests use this route as an independent check. It squares the matrix, so it loses about half the digits when $M$ is badly conditioned.
- **QR of the inverse.** $M^{-1} = R^{\mathsf T} K^{-1}$ is orthogonal times upper triangular, so a plain QR decomposition of $M^{-1}$ gives $R^{\mathsf T}$ and $K^{-1}$. This avoids an RQ routine but needs the inverse.
- **Center by the SVD.** The right [singular vector](/singular-value-decomposition/) of $P$ for the smallest singular value is the center in homogeneous form. It also works when $M$ is singular; then its last entry is 0, and the center is at infinity.
- **Gram-Schmidt.** RQ is also the [Gram-Schmidt process](/gram-schmidt-process/) applied to the rows of $M$ from the last row up. The third row of $R$ is the unit vector along $m_3$, the third row of $M$, which is also the optical axis.
- **Constrained cameras.** If the camera is known to have zero skew or square pixels, the decomposition of a noisy $P$ does not give this. Fit the constrained parameters by minimizing the reprojection error over $K$, $R$ and $t$, starting from the decomposition (HZ chapter 7).

## When to use it

Use it after [DLT resectioning](/dlt-camera-resectioning/), to read focal lengths, the principal point and the pose from an estimated $P$, or to start a nonlinear refinement in the parameters of $K$, $R$ and $t$. Use it also to turn a camera matrix from a projective reconstruction, after an upgrade to a metric frame, into a camera that a graphics program or a robot can use. If $K$ is known in advance, do not decompose an unconstrained $P$; solve the [perspective-n-point](/perspective-n-point/) problem for the pose instead, which uses the known $K$.

## Pitfalls

- **Library sign conventions.** RQ routines do not agree on the signs of the diagonal. Some return negative entries, which give negative focal lengths. Always apply line L5.
- **Forgetting the sign of the scale.** If $\det M < 0$ and line L3 is skipped, a positive diagonal of $K$ forces $\det R = -1$, a reflection, which is not a camera pose. DLT returns $P$ with an arbitrary sign, so this happens half of the time.
- **Normalizing $K$ too early.** If $K$ is divided by $K_{33}$ before line L6, the computed $t$ is too large by the factor $K_{33}$, and the center is wrong by the same factor.
- **Reading $R$ from $M$ directly.** $M$ is $K R$, not $R$. Its rows are not unit vectors unless $K = I$.
- **Noise.** A small change in $P$ changes $K$ and $R$ smoothly, but the principal point can be poorly determined by the data that gave $P$ (for example a narrow field of view), so it can move by many pixels. That is a property of the estimate of $P$, not of the decomposition.

## Implementations

## History

Ganapathy (1984) gave a closed form for the camera parameters from the $3 \times 4$ matrix of a calibrated camera, for robot vision. In the same years photogrammetry used the direct linear transformation of Abdel-Aziz and Karara (1971) and then read the camera parameters from its coefficients. Hartley and Zisserman (2000, second edition 2004) wrote the decomposition as an RQ factorization of the left $3 \times 3$ block, with the sign fixes above, and this is the form used in computer vision libraries today.

## References
