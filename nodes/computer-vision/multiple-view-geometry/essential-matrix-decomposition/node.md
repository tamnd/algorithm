---
tag: CHAEFS
kind: algorithm
slug: essential-matrix-decomposition
name: Pose recovery from the essential matrix
aliases:
- essential matrix decomposition
area: computer-vision/multiple-view-geometry
level: core
summary: "Factor E by SVD into four candidate rotation and translation pairs and keep the one that puts triangulated points in front of both cameras."
solves: [relative-pose-problem]
model: real-ram
complexity:
  vars: {n: the number of point pairs used for the depth test}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1981
  people: [H. C. Longuet-Higgins, Richard Hartley]
  note: Longuet-Higgins recovered the rotation and translation from the essential matrix in 1981 and used the sign of the depths to choose. Hartley gave the general theory of cheirality in 1998.
prereqs: [essential-matrix, singular-value-decomposition, cheirality]
see_also: [essential-matrix-characterization, five-point-algorithm, relative-pose-problem, linear-triangulation, homography-decomposition, special-orthogonal-group, eight-point-algorithm, camera-extrinsic-parameters]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 9.6, The essential matrix (Results 9.18 and 9.19 on the factorizations and the four solutions, and Section 9.6.3 on the twisted pair)"
  - paper: doi:10.1038/293133a0
    title: "H. C. Longuet-Higgins, A computer algorithm for reconstructing a scene from two projections, Nature 293, 1981, 133-135"
    locator: the recovery of the rotation and the translation from the essential matrix and the choice by positive depths
  - paper: doi:10.1023/A:1007984508483
    title: "Richard I. Hartley, Chirality, International Journal of Computer Vision 26(1), 1998, 41-61"
    locator: the conditions for points to lie in front of the cameras and their use to remove ambiguities
  - book: isbn:9780387008936
    title: "Yi Ma, Stefano Soatto, Jana Kosecka and S. Shankar Sastry, An Invitation to 3-D Vision, Springer, 2004"
    locator: "Chapter 5, Section 5.1.2 (pose recovery from the essential matrix)"
---

Pose recovery from the essential matrix turns an [essential matrix](/essential-matrix/) $E$ into the relative pose $(R, \mathbf{t})$ of two calibrated cameras, with $\mathbf{X}_2 = R\mathbf{X}_1 + \mathbf{t}$ and $\|\mathbf{t}\| = 1$. The [singular value decomposition](/singular-value-decomposition/) $E = U\operatorname{diag}(s, s, 0)V^{\mathsf T}$, with $U$ and $V$ made rotations, gives exactly four candidates: the rotations $UWV^{\mathsf T}$ and $UW^{\mathsf T}V^{\mathsf T}$, each with the translations $\pm\mathbf{u}_3$. All four satisfy the epipolar constraint, so the images cannot tell them apart by it. Only one puts the scene points in front of both cameras, and the algorithm finds it by the [cheirality](/cheirality/) test: it computes the depths of the matched points under each candidate and keeps the one with the most positive depths. It is the last step after the [five-point algorithm](/five-point-algorithm/) or the [eight-point algorithm](/eight-point-algorithm/) in the [relative pose problem](/relative-pose-problem/).

## In plain words

The essential matrix packs the turn and the direction of travel of the camera into one table. Pulling them out again is easy with a standard matrix tool, but it gives four possible answers, not one. Two answers differ in the direction of travel: forward or backward. The other two differ by a half turn of one camera about the line that joins the two cameras. All four agree with the matched points in the same way. But in three of them some scene points end up behind a camera, which a real camera cannot see. So the algorithm rebuilds a few points for each answer and keeps the answer in which the points sit in front of both cameras.

## The problem

**Input.** An essential matrix $E$, with any nonzero scale and sign, and point pairs $(\hat{\mathbf{x}}_{1,i}, \hat{\mathbf{x}}_{2,i})$, $i = 1, \ldots, n$, $n \ge 1$, in normalized image coordinates.

**Output.** A rotation $R$, a unit vector $\mathbf{t}$ with $[\mathbf{t}]_\times R \sim E$, and the number of pairs whose reconstructed point has positive depth in both cameras, for the candidate with the largest such number. If the pairs are exact images of points in front of both cameras of a pose $(R_0, \mathbf{t}_0)$ with $E \sim [\mathbf{t}_0]_\times R_0$ and $\|\mathbf{t}_0\| = 1$, the output is $(R_0, \mathbf{t}_0)$ and the count is $n$.

## The algorithm

```pseudo id=main
RECOVER-POSE(E, x1_1 .. x1_n, x2_1 .. x2_n)
L1  (U, diag(s1, s2, s3), V) <- the SVD of E
L2  if det U < 0 then negate the last column of U ; if det V < 0 then negate the last column of V
L3  Ra <- U W V^T ; Rb <- U W^T V^T, with W = ((0, -1, 0), (1, 0, 0), (0, 0, 1))
L4  the candidates are (Ra, u3), (Ra, -u3), (Rb, u3), (Rb, -u3), where u3 is the last column of U
L5  for each candidate (R, t)
L6      for each pair, (l1, l2) <- the depths that minimize || l1 R y1 + t - l2 y2 ||, with y = (u, v, 1)
L7      c <- the number of pairs with l1 > 0 and l2 > 0
L8  return the candidate with the largest c (the first one on a tie), and c
```

Line L2 does not change the product $U\Sigma V^{\mathsf T}$, because the third singular value is 0, and it makes $U$ and $V$ rotations, so $R_a$ and $R_b$ are rotations. Since $E^{\mathsf T}\mathbf{u}_3 = \mathbf{0}$ and $E = [\mathbf{t}]_\times R$ gives $\mathbf{t}^{\mathsf T}E = \mathbf{0}$, the translation is a multiple of $\mathbf{u}_3$. The characterization proof shows $[\mathbf{u}_3]_\times R_a \sim E$, and $R_b = R_\pi R_a$ with $R_\pi = 2\mathbf{u}_3\mathbf{u}_3^{\mathsf T} - I$, the half turn about $\mathbf{u}_3$, which also gives $[\mathbf{u}_3]_\times R_b \sim E$. Line L6 is a small [triangulation](/linear-triangulation/): $\lambda_1R\mathbf{y}_1 + \mathbf{t}$ is the point on the first ray in the second frame, and $\lambda_2\mathbf{y}_2$ is the point on the second ray. The $2 \times 2$ normal equations give $(\lambda_1, \lambda_2)$, and parallel rays give $(0, 0)$, which counts as not in front. The values $\lambda_1$ and $\lambda_2$ are the $Z$ coordinates of the point in the two camera frames.

## Example

Take the running example: $R = \begin{pmatrix} 0.8 & 0 & 0.6 \\ 0 & 1 & 0 \\ -0.6 & 0 & 0.8 \end{pmatrix}$, $\mathbf{t} = (1, 0, 0)$, $E = \begin{pmatrix} 0 & 0 & 0 \\ 0.6 & 0 & -0.8 \\ 0 & 1 & 0 \end{pmatrix}$, and the one pair $(0, 0) \leftrightarrow (1, 0)$ from $\mathbf{X}_1 = (0, 0, 5)$.

| line | value |
|---|---|
| L1, L2 | $U = \begin{pmatrix} 0 & 0 & -1 \\ 0 & 1 & 0 \\ 1 & 0 & 0 \end{pmatrix}$, $\Sigma = \operatorname{diag}(1, 1, 0)$, $V = \begin{pmatrix} 0 & 0.6 & -0.8 \\ 1 & 0 & 0 \\ 0 & -0.8 & -0.6 \end{pmatrix}$, both with determinant 1 |
| L3 | $R_a = UWV^{\mathsf T} = R$ and $R_b = UW^{\mathsf T}V^{\mathsf T} = \begin{pmatrix} 0.8 & 0 & 0.6 \\ 0 & -1 & 0 \\ 0.6 & 0 & -0.8 \end{pmatrix}$ |
| L4 | $\mathbf{u}_3 = (-1, 0, 0)$, so $-\mathbf{u}_3 = \mathbf{t}$ |
| L6, L7 for $(R_a, \mathbf{u}_3)$ | depths $(-5, -4)$, $c = 0$ |
| L6, L7 for $(R_a, -\mathbf{u}_3)$ | depths $(5, 4)$, $c = 1$ |
| L6, L7 for $(R_b, \mathbf{u}_3)$ | depths $(\frac57, -\frac47)$, $c = 0$ |
| L6, L7 for $(R_b, -\mathbf{u}_3)$ | depths $(-\frac57, \frac47)$, $c = 0$ |
| L8 | $(R, (1, 0, 0))$ with $c = 1$ |

A check of the winner: $5R(0, 0, 1)^{\mathsf T} + \mathbf{t} = (3, 0, 4) + (1, 0, 0) = (4, 0, 4) = 4\,(1, 0, 1)$. The four depth pairs follow the pattern of the proof: $(\lambda_1, \lambda_2)$, $(-\lambda_1, -\lambda_2)$, and $\pm(\lambda_1, -\lambda_2)/D$ for the twisted pair, here with $D = 7$.

## Correctness

A real matrix with singular values $(s, s, 0)$ has exactly four factorizations $[\mathbf{t}]_\times R$ with $\|\mathbf{t}\| = s$ and $R$ a rotation, and they are the four candidates of line L4 up to the scale of $\mathbf{t}$. For a point with true depths $(\lambda_1, \lambda_2)$ under one of them, the other three give $(-\lambda_1, -\lambda_2)$, $(-\lambda_1/D, \lambda_2/D)$ and $(\lambda_1/D, -\lambda_2/D)$ for a number $D$ that depends on the point. So for exact data with all points in front of both cameras, only the true pose has all depths positive, and the count rule returns it. Under noise, the majority over many points is a practical rule, not a theorem. The full proof is below.

## Complexity

The SVD of a $3 \times 3$ matrix and the four candidates take a fixed amount of work. The depth test costs $\Theta(1)$ for each pair and each of the four candidates, so the total time is $\Theta(n)$. The extra space is $\Theta(1)$, since only the four candidates and the counts are kept. In the real RAM model the SVD is exact; in floating point it is found by an iterative method that converges in a few sweeps for $3 \times 3$ matrices.

## Properties

- **Exactly four candidates.** For each essential matrix, up to the scale of $\mathbf{t}$.
- **Sign of $E$ does not matter.** $-E$ gives the same four candidates in another order.
- **Scale of $\mathbf{t}$ is lost.** The output has $\|\mathbf{t}\| = 1$; the true length needs other information.
- **One point is enough on exact data.** A single point in front of both cameras, not on the baseline, picks the right pose.
- **Twisted pair.** $R_b = R_\pi R_a$ with $R_\pi$ the half turn about the baseline; the two rotations differ by 180 degrees.
- **Robust by voting.** With noisy data or a few wrong matches, the majority of the depth tests still picks the right pose in most cases.

## Variants and improvements

- **Test with one point.** Many systems test only one point, or the first inlier. It is cheaper but fragile when that point is far away or noisy.
- **Triangulation method.** Line L6 can use [linear triangulation](/linear-triangulation/) or the [midpoint method](/midpoint-triangulation/) instead of the $2 \times 2$ least squares; any method that gives the signs of the depths works.
- **Far points.** Points with very large depth give unreliable signs. Some implementations ignore points whose depth is above a threshold.
- **Closed forms without the SVD.** The translation is the null vector of $E^{\mathsf T}$, found from a cross product of two rows of $E$, and the rotation can be written from the rows of $E$ and $\mathbf{t}$; this is Longuet-Higgins' original form.
- **Homography case.** For a planar scene or a homography, the analogous step is [homography decomposition](/homography-decomposition/), which has its own four candidates.

## When to use it

Use it after any method that estimates $E$: the five-point algorithm in RANSAC, the eight-point algorithm on inliers, or $E = K_2^{\mathsf T}FK_1$ from a fundamental matrix. Run the depth test on the inliers, not on all matches. If the estimate of $E$ is not exactly essential, the SVD step still works, because it uses only $U$ and $V$; that is the same as first projecting onto the closest essential matrix.

## Pitfalls

- **Forgetting line L2.** If $\det U = -1$ or $\det V = -1$, the matrices $UWV^{\mathsf T}$ have determinant $-1$ and are reflections, not rotations.
- **Two candidates only.** Testing only $\pm\mathbf{t}$ for one rotation misses the twisted pair, and can return a pose that puts the points behind a camera.
- **Wrong frame convention.** This page uses $\mathbf{X}_2 = R\mathbf{X}_1 + \mathbf{t}$ and $\hat{\mathbf{x}}_2^{\mathsf T}E\hat{\mathbf{x}}_1 = 0$. Libraries that use the camera center or the other direction give $R^{\mathsf T}$ and $-R^{\mathsf T}\mathbf{t}$.
- **Pure rotation.** If the true $\mathbf{t}$ is zero, $E$ is zero or pure noise, and the result has no meaning.
- **Points near the epipoles.** A point close to the baseline gives rays that are nearly parallel, and its depths are unreliable.
- **Ties.** On degenerate data two candidates can get the same count. Report the count, so that the caller can detect a weak decision.

## Implementations

## History

Longuet-Higgins (1981) introduced the essential matrix, recovered the rotation and the translation from it, and used the sign of the reconstructed depths to choose among the solutions. The SVD form of the factorization, with the matrix $W$ and the four candidates, is given by Hartley and Zisserman (2000, second edition 2004) as Results 9.18 and 9.19, with the twisted pair in Section 9.6.3. Hartley (1998) developed the general theory of cheirality, the condition that points lie in front of the cameras, and its use to remove such ambiguities.

## References
