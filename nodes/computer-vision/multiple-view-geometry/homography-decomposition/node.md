---
tag: NHSK5N
kind: algorithm
slug: homography-decomposition
name: Homography decomposition
aliases:
- Faugeras-Lustman decomposition
- Malis-Vargas decomposition
area: computer-vision/multiple-view-geometry
level: advanced
summary: Recover the rotation, the scaled translation and the plane normal from a calibrated homography of a plane, up to a few solutions told apart by visibility.
solves: []
model: real-ram
complexity:
  vars: {n: the number of point pairs used for the sign and visibility tests}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1988
  people: [Olivier Faugeras, Francis Lustman]
  note: Faugeras and Lustman showed in 1988 how to recover the motion and the plane from a plane-induced homography by an SVD, and with depth conditions to discard solutions. Ma, Soatto, Kosecka and Sastry gave the construction used here in 2004, and Malis and Vargas gave closed-form expressions in 2007.
prereqs: [homography, camera-intrinsic-matrix, singular-value-decomposition]
see_also: [homography-estimation, dlt-homography, essential-matrix-decomposition, zhang-calibration-method, perspective-n-point, cheirality, critical-configurations, visual-odometry]
sources:
  - paper: doi:10.1142/S0218001488000285
    title: "Olivier Faugeras and Francis Lustman, Motion and structure from motion in a piecewise planar environment, International Journal of Pattern Recognition and Artificial Intelligence 2(3), 1988, 485-508"
    locator: the decomposition of the homography by an SVD and the count of solutions
  - book: isbn:9780387008936
    title: "Yi Ma, Stefano Soatto, Jana Kosecka and S. Shankar Sastry, An Invitation to 3-D Vision, Springer, 2004"
    locator: "Section 5.3.3, Decomposing the planar homography matrix (the normalization by the second singular value, the construction from the SVD of H^T H, Theorem 5.19 with four solutions of which two have positive depth)"
  - url: https://inria.hal.science/inria-00174036
    title: "Ezio Malis and Manuel Vargas, Deeper understanding of the homography decomposition for vision-based control, INRIA Research Report RR-6303, 2007"
    locator: the analytical decomposition without SVD and the relations between the solutions
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 13.1, Homographies given the plane and vice versa (the plane-induced homography, with the plane written as n^T X + d = 0)"
---

Homography decomposition takes the [homography](/homography/) $G$ that a plane induces between two calibrated views and returns the camera motion and the plane: the rotation $R$, the translation divided by the distance of the plane, $\mathbf{t}/d$, and the unit normal $\mathbf{n}$. In general it finds four candidates in two pairs, and the condition that the points of the plane are in front of the first camera keeps two of them. It is the planar counterpart of [essential matrix decomposition](/essential-matrix-decomposition/), and it is used where the essential matrix fails because the scene is a plane. [Homography estimation](/homography-estimation/) and the [DLT](/dlt-homography/) find $G$ from matches; this page starts from $G$.

## In plain words

When a camera looks at a flat floor from two places, one $3 \times 3$ table maps the floor in the first photo onto the floor in the second. That table is built from three things: how the camera turned, how it moved, and how the floor is tilted. This method takes the table apart again. The amount of movement comes out only as a ratio to the distance of the floor, because a scene twice as big seen from twice as far gives the same photos. The math gives four possible answers. Two of them put the floor behind the camera, so they are dropped. The other two both fit the two photos perfectly, and only more information, such as a third photo or a rough idea of where the floor is, can tell which one is true.

## The problem

**Input.** A $3 \times 3$ matrix $G$, known only up to a nonzero factor of either sign, with $\mathbf{x}_2 \sim G\mathbf{x}_1$ for the pixels of a plane in two images; the [intrinsic matrices](/camera-intrinsic-matrix/) $K_1$ and $K_2$; and at least one pair of pixels $\mathbf{x}_1 \leftrightarrow \mathbf{x}_2$ of points on the plane, seen in front of both cameras.

**Convention.** The plane is $\mathbf{n}^{\mathsf T}\mathbf{X}_1 = d$ in the frame of camera 1, with $\|\mathbf{n}\| = 1$ and $d > 0$, and $\mathbf{X}_2 = R\mathbf{X}_1 + \mathbf{t}$. Then $G \sim K_2(R + \mathbf{t}\mathbf{n}^{\mathsf T}/d)K_1^{-1}$. Both cameras see the plane from the same side. Hartley and Zisserman write the plane as $\mathbf{n}^{\mathsf T}\mathbf{X} + d = 0$ and get a minus sign in the formula.

**Output.** Every triple $(R, \mathbf{t}' = \mathbf{t}/d, \mathbf{n})$ with $R$ a rotation, $\mathbf{n}$ a unit vector, $K_2^{-1}GK_1 \sim R + \mathbf{t}'\mathbf{n}^{\mathsf T}$, and $\mathbf{n}^{\mathsf T}K_1^{-1}\mathbf{x}_1 > 0$ for the given points. In the general case there are two. If the camera did not move ($\mathbf{t} = \mathbf{0}$), the output is $R$ alone, since then every plane induces the same homography and $\mathbf{n}$ is not defined.

## The algorithm

```pseudo id=main
DECOMPOSE-HOMOGRAPHY(G, K1, K2, pairs (x1_i, x2_i))
L1  H <- K2^-1 G K1 ; y1_i <- K1^-1 x1_i ; y2_i <- K2^-1 x2_i
L2  H <- H / sigma2(H)                                  ▷ the middle singular value
L3  if y2_i^T H y1_i < 0 for most i then H <- -H
L4  (v1, v2, v3), (s1, s2, s3) <- right singular vectors and singular values of H ; l1 <- s1^2 ; l3 <- s3^2
L5  if l1 - l3 < eps then return [ (the orthogonal factor of H, 0, undefined) ]
L6  for u in { (sqrt(1 - l3) v1 + sqrt(l1 - 1) v3) / sqrt(l1 - l3) , (sqrt(1 - l3) v1 - sqrt(l1 - 1) v3) / sqrt(l1 - l3) }
L7      U <- [ v2, u, v2 x u ] ; W <- [ H v2, H u, H v2 x H u ]          ▷ columns
L8      R <- W U^T ; n <- v2 x u ; t <- (H - R) n
L9      add (R, t, n) and (R, -t, -n) to the candidates
L10 keep the candidates with n^T y1_i > 0 for most i
L11 return the kept candidates
```

Line L1 removes the calibration, so that $H \sim R + \mathbf{t}'\mathbf{n}^{\mathsf T}$. The middle singular value of every matrix of the form $R + \mathbf{t}'\mathbf{n}^{\mathsf T}$ is exactly 1, so line L2 fixes the scale up to sign. Line L3 fixes the sign: for a point of the plane with depths $z_1, z_2 > 0$ in the two cameras, $(R + \mathbf{t}'\mathbf{n}^{\mathsf T})\mathbf{y}_1 = (z_2/z_1)\mathbf{y}_2$, so $\mathbf{y}_2^{\mathsf T}H\mathbf{y}_1 > 0$ for the right sign. Lines L4 to L8 use the fact that $H$ acts as the rotation $R$ on the plane of vectors orthogonal to $\mathbf{n}$, where it keeps lengths. The vector $v_2$ and each of the two vectors $u$ of line L6 span a plane on which $H$ keeps lengths, and there are no other such planes. On the right one, $R$ is fixed by its action on $v_2$ and $u$, and $\mathbf{n}$ is the normal of the plane up to sign. Line L9 adds the other sign of $\mathbf{n}$ with the matching $\mathbf{t}'$. Line L10 is the visibility test: a point $\mathbf{X}_1 = z_1\mathbf{y}_1$ of the plane in front of camera 1 has $\mathbf{n}^{\mathsf T}\mathbf{y}_1 = d/z_1 > 0$. Of each pair $(R, \mathbf{t}, \mathbf{n})$, $(R, -\mathbf{t}, -\mathbf{n})$ exactly one passes. The majority votes in L3 and L10 make the tests robust to a few bad points.

## Example

Take $K_1 = K_2 = I$, $R = \begin{pmatrix} 0.8 & 0 & 0.6 \\ 0 & 1 & 0 \\ -0.6 & 0 & 0.8 \end{pmatrix}$, $\mathbf{t} = (1, 0, 0)^{\mathsf T}$, $\mathbf{n} = (0, 0, 1)^{\mathsf T}$ and $d = 2$, so $G = R + \mathbf{t}\mathbf{n}^{\mathsf T}/2 = \begin{pmatrix} 0.8 & 0 & 1.1 \\ 0 & 1 & 0 \\ -0.6 & 0 & 0.8 \end{pmatrix}$. The points $(0, 0)$, $(0.2, 0.1)$, $(-0.2, 0.1)$ of image 1 map to $(1.375, 0)$, $(1.8529, 0.1471)$, $(1.0217, 0.1087)$.

| line | value |
|---|---|
| L1 to L3 | $H = G$; the singular values are $1.4173$, $1$, $0.9173$; all three votes are positive |
| L4 | $v_1 = (0.3686, 0, 0.9296)$, $v_2 = (0, 1, 0)$, $v_3 = (0.9296, 0, -0.3686)$; $l_1 = 2.0086$, $l_3 = 0.8414$ |
| L6, first $u$ | $u = (1, 0, 0)$, $\mathbf{n} = v_2 \times u = (0, 0, -1)$, $R$ is the true $R$, $\mathbf{t}' = (-0.5, 0, 0)$ |
| L6, second $u$ | $u = (-0.7283, 0, 0.6853)$, $\mathbf{n} = (0.6853, 0, 0.7283)$, $R = \begin{pmatrix} 0.5505 & 0 & 0.8349 \\ 0 & 1 & 0 \\ -0.8349 & 0 & 0.5505 \end{pmatrix}$, $\mathbf{t}' = (0.3641, 0, 0.3427)$ |
| L9 | four candidates: the two above and the two with $-\mathbf{t}'$ and $-\mathbf{n}$ |
| L10 | $\mathbf{n} = (0, 0, -1)$ and $(-0.6853, 0, -0.7283)$ fail at $\mathbf{y}_1 = (0, 0, 1)$; two remain |

The two answers are the true motion, $\mathbf{t}' = (0.5, 0, 0)$ with $\mathbf{n} = (0, 0, 1)$, and a turn of about $56.6$ degrees about the $y$ axis with the plane tilted. Both satisfy $R + \mathbf{t}'\mathbf{n}^{\mathsf T} = H$ exactly, so the two images cannot tell them apart.

## Correctness

Every matrix $R + \mathbf{t}'\mathbf{n}^{\mathsf T}$ has middle singular value 1, and the sign test is positive for the right sign, so after L3 $H$ equals $R + \mathbf{t}'\mathbf{n}^{\mathsf T}$ exactly. The quadratic form $\mathbf{w}^{\mathsf T}(H^{\mathsf T}H - I)\mathbf{w}$ vanishes on the plane orthogonal to the true $\mathbf{n}$. Its zero set is the union of the two planes spanned by $v_2$ and the two vectors of line L6, so the true plane is one of them, and the true solution is one of the four candidates. Every candidate satisfies $R + \mathbf{t}'\mathbf{n}^{\mathsf T} = H$ and has $R$ a rotation. The visibility test keeps exactly one of each pair. The full proof is below.

## Complexity

The work on $H$ is a fixed number of operations on $3 \times 3$ matrices, including two SVDs, so it costs $\Theta(1)$ in the [real RAM](/real-ram/) with square roots. The two majority votes look at each of the $n$ pairs once, so they cost $\Theta(n)$. The implementation stores the $n$ normalized points, $\Theta(n)$ extra space; the votes can also be computed while reading the pairs, in $\Theta(1)$ space. The estimate of $G$ that comes before, by the DLT, costs $\Theta(n)$ as well.

## Properties

- **Exact.** On an exact $G$ every returned triple reproduces $G$ up to scale, and the true triple is always returned.
- **Two answers in general.** Of the four candidates, two have positive depths (Ma et al., Theorem 5.19). Both reproduce $H$ exactly, so the two views alone do not decide between them.
- **One answer in special cases.** If $\mathbf{t}$ is parallel to $R\mathbf{n}$, the camera moves along the normal of the plane, the smallest or largest singular value equals 1, and the two vectors of line L6 are $\pm$ one singular vector. The two pairs then coincide, and the kept list holds one triple twice.
- **Scale.** Only $\mathbf{t}/d$ is recovered. The absolute translation needs the distance $d$ of the plane from another source.
- **Free of the scale and sign of $G$.** $G$ and $\mu G$ give the same output for every $\mu \ne 0$.

## Variants and improvements

- **Faugeras and Lustman (1988).** They work with the SVD $H = U\Lambda V^{\mathsf T}$ and solve for the motion in the frame of the singular vectors, with a case analysis on equal singular values, and use the depth conditions to discard solutions.
- **Malis and Vargas (2007).** Closed-form expressions for the solutions in terms of the entries of $H^{\mathsf T}H - I$, with no SVD, and formulas that relate the two physically valid solutions to each other. They are convenient for visual servoing.
- **Choosing between the two answers.** Use a rough prior on the normal (for a ground plane, the vertical direction), a third view, a second plane, or the [reprojection error](/reprojection-error/) of points off the plane.
- **Known normal or known rotation.** If $\mathbf{n}$ is known, for example from an inertial sensor, $H$ equals $R$ on the plane orthogonal to $\mathbf{n}$, which fixes $R$, and then $\mathbf{t}' = (H - R)\mathbf{n}$: the solution is unique.
- **Pose from a planar target.** When the plane is a calibration target with known metric coordinates, the pose comes more simply from the columns of $K^{-1}G$ (as in [Zhang's method](/zhang-calibration-method/)), which is the planar case of [perspective-n-point](/perspective-n-point/).

## When to use it

Use it to get the camera motion between two views of a scene that is mostly one plane: a drone over flat ground, a robot looking at a wall, a camera over a table or a document, the initialization of [visual odometry](/visual-odometry/) and of SLAM systems that test both a homography and an essential matrix. In such scenes the essential matrix is badly determined, since all points lie on a plane, while the homography is well determined. If the scene has depth, use the essential matrix instead; a homography then describes only the points of one plane.

## Pitfalls

- **Wrong calibration.** The method needs $K_1$ and $K_2$. With wrong intrinsics $H$ is not of the form $R + \mathbf{t}'\mathbf{n}^{\mathsf T}$, the middle singular value is not exactly 1, and the output is biased.
- **Sign conventions.** Check how the plane is written. With $\mathbf{n}^{\mathsf T}\mathbf{X} + d = 0$ the formula has a minus sign, and a formula with the wrong sign returns $-\mathbf{t}$.
- **Almost no translation.** When $\|\mathbf{t}\|/d$ is small, $s_1$ and $s_3$ are close to 1, and $\mathbf{n}$ and $\mathbf{t}'$ are badly determined by noise, although $R$ is still accurate. Choose the threshold $\varepsilon$ of line L5 with the noise level in mind.
- **Picking one answer by default.** Returning the first candidate that passes the test gives the wrong motion about half the time. Keep both until other information decides.
- **Cameras on both sides of the plane.** If camera 2 is the mirror image of camera 1 in the plane, $H$ is orthogonal with determinant $-1$, and line L5 misreads it as a pure rotation. This needs a transparent plane and is outside the convention above.

## Implementations

## History

Faugeras and Lustman (1988) gave the decomposition of the plane-induced homography by an SVD, counted the solutions and used it for motion in piecewise planar scenes. Ma, Soatto, Kosecka and Sastry (2004) gave the construction from the singular vectors of $H^{\mathsf T}H$ used on this page and proved that two solutions remain with positive depths. Malis and Vargas (2007) gave closed-form solutions without an SVD, motivated by visual servoing.

## References
