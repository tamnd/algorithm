---
tag: 65TKEM
kind: theorem
slug: kruppa-equations
name: Kruppa equations
aliases:
- Kruppa constraints
area: computer-vision/camera-models-and-calibration
level: advanced
summary: "For two views with fundamental matrix F, the duals of the absolute conic images satisfy [e']x omega*' [e']x^T ~ F omega* F^T: two equations per image pair on K K^T."
prereqs: [image-of-the-absolute-conic, fundamental-matrix, epipolar-geometry]
see_also: [self-calibration, essential-matrix, stratified-reconstruction, camera-calibration, singular-value-decomposition, skew-symmetric-matrix-of-a-vector, polynomial-system-solving, projective-reconstruction-theorem]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 19.4, The Kruppa equations (the equation on the dual image of the absolute conic, its form with the SVD of F, and the count of two equations per pair); Section 19.1 for the counting of constraints
  - paper: doi:10.1109/34.574792
    title: Richard I. Hartley, Kruppa's equations derived from the fundamental matrix, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(2), 1997, 133-135
    locator: the form of the Kruppa equations in terms of the singular value decomposition of F
  - paper: "Stephen J. Maybank and Olivier D. Faugeras, A theory of self-calibration of a moving camera, International Journal of Computer Vision 8(2), 1992, 123-151"
    title: Stephen J. Maybank and Olivier D. Faugeras, A theory of self-calibration of a moving camera, International Journal of Computer Vision 8(2), 1992, 123-151
    locator: the derivation of the Kruppa equations from the epipolar transformation, and the use of three views with a constant camera
  - paper: doi:10.1109/34.879804
    title: Peter Sturm, A case against Kruppa's equations for camera self-calibration, IEEE Transactions on Pattern Analysis and Machine Intelligence 22(10), 2000, 1199-1204
    locator: the motions for which the Kruppa equations are degenerate although self-calibration is possible
---

The Kruppa equations are the constraints that the fundamental matrix of two views puts on the intrinsic matrices of the cameras. They are written with the dual of the [image of the absolute conic](/image-of-the-absolute-conic/), $\omega^\ast = K K^{\mathsf T}$: if $F$ is the [fundamental matrix](/fundamental-matrix/) and $e'$ the epipole in the second image, then $[e']_\times \omega^{\ast\prime} [e']_\times^{\mathsf T} \sim F \omega^\ast F^{\mathsf T}$. Both sides are symmetric and both have $e'$ in their kernel, so the relation holds two equations per image pair. They do not use the plane at infinity or a common projective frame for several views, only the $F$ of each pair. That made them the first route to [self-calibration](/self-calibration/), in the work of Faugeras, Luong and Maybank in 1992. Sturm (2000) showed that they lose information for some motions where other self-calibration methods still work.

## Statement

**Setting.** Two pinhole cameras $P = K [I \mid 0]$ and $P' = K' [R \mid t]$ with invertible upper triangular $K$ and $K'$, a rotation $R$ and $t \ne 0$ (the centers differ). Let
$$F = K'^{-\mathsf T} [t]_\times R K^{-1}, \qquad e' = K' t, \qquad \omega^\ast = K K^{\mathsf T}, \qquad \omega^{\ast\prime} = K' K'^{\mathsf T},$$
so that $x'^{\mathsf T} F x = 0$ for matching pixels and $F^{\mathsf T} e' = 0$. Here $[a]_\times b = a \times b$.

**Theorem (Kruppa equations).**
1. $[e']_\times \, \omega^{\ast\prime} \, [e']_\times^{\mathsf T} = (\det K')^2 \, F \, \omega^\ast F^{\mathsf T}$. So for any scaling of $F$ and $e'$, the two sides are equal up to a nonzero factor.
2. Let $F = U \operatorname{diag}(r, s, 0) V^{\mathsf T}$ be a [singular value decomposition](/singular-value-decomposition/) with $r \ge s > 0$, and let $u_i$ and $v_i$ be the columns of $U$ and $V$. Then
$$\frac{u_2^{\mathsf T} \omega^{\ast\prime} u_2}{r^2 \, v_1^{\mathsf T} \omega^\ast v_1} = \frac{-u_1^{\mathsf T} \omega^{\ast\prime} u_2}{r s \, v_1^{\mathsf T} \omega^\ast v_2} = \frac{u_1^{\mathsf T} \omega^{\ast\prime} u_1}{s^2 \, v_2^{\mathsf T} \omega^\ast v_2},$$
read as equalities of cross products when a denominator is zero. These are two equations, each quadratic in the entries of $\omega^\ast$ when $\omega^{\ast\prime} = \omega^\ast$, and part 1 holds if and only if both hold.

Part 1 is the form of HZ Section 19.4. Part 2 is the form of Hartley (1997), which needs only $F$, because $u_3$ is the epipole.

## In plain words

Two photos of the same scene from two places fix a matrix, the fundamental matrix, that says which points can match. This matrix mixes two things: how the camera moved, and how each camera is built inside. The Kruppa equations separate a part of the inside. They say that a certain shape, made only from the camera's insides, must look the same when seen through the matrix as when seen around the point where the other camera's center appears. From each pair of photos you get two such conditions. If the camera does not change, three photos give enough conditions to solve for its focal length, principal point and the rest, with no known object in the scene.

## Proof

**Step 1: the fundamental matrix and the epipole.** A point $X$ has $x \sim K X$ and $x' \sim K' (R X + t)$. The vectors $t$, $R X + t$ and $R X$ are coplanar, so $(R X + t)^{\mathsf T} [t]_\times R X = 0$, which is $x'^{\mathsf T} K'^{-\mathsf T} [t]_\times R K^{-1} x = 0$. So $F$ is as stated. Also $F^{\mathsf T} e' = K^{-\mathsf T} R^{\mathsf T} [t]_\times^{\mathsf T} K'^{-1} K' t = -K^{-\mathsf T} R^{\mathsf T} (t \times t) = 0$.

**Step 2: a lemma.** For an invertible $3 \times 3$ matrix $M$ and any $a$,
$$[M a]_\times = \det(M) \, M^{-\mathsf T} [a]_\times M^{-1}.$$
Proof: for all $b$ and $c$, $(M a \times M b) \cdot M c = \det[M a, M b, M c] = \det(M) \det[a, b, c] = \det(M) (a \times b) \cdot c$. The right side equals $\det(M) \, (M^{-\mathsf T} (a \times b)) \cdot (M c)$. As $M c$ runs over all of $\mathbb R^3$, $M a \times M b = \det(M) M^{-\mathsf T} (a \times b)$, that is $[M a]_\times M = \det(M) M^{-\mathsf T} [a]_\times$. Multiply by $M^{-1}$ on the right.

**Step 3: part 1.** By the lemma with $M = K'$ and $a = t$, $[e']_\times = \det(K') K'^{-\mathsf T} [t]_\times K'^{-1}$. Then
$$[e']_\times \omega^{\ast\prime} [e']_\times^{\mathsf T} = (\det K')^2 K'^{-\mathsf T} [t]_\times K'^{-1} K' K'^{\mathsf T} K'^{-\mathsf T} [t]_\times^{\mathsf T} K'^{-1} = (\det K')^2 K'^{-\mathsf T} [t]_\times [t]_\times^{\mathsf T} K'^{-1},$$
$$F \omega^\ast F^{\mathsf T} = K'^{-\mathsf T} [t]_\times R K^{-1} K K^{\mathsf T} K^{-\mathsf T} R^{\mathsf T} [t]_\times^{\mathsf T} K'^{-1} = K'^{-\mathsf T} [t]_\times [t]_\times^{\mathsf T} K'^{-1},$$
using $R R^{\mathsf T} = I$. The two lines differ by the factor $(\det K')^2 > 0$. If $F$ and $e'$ are scaled by $\alpha \ne 0$ and $\beta \ne 0$, the sides are scaled by $\beta^2$ and $\alpha^2$, so they stay equal up to a nonzero factor.

**Step 4: part 2.** The matrix $F$ has rank 2, because $[t]_\times$ has rank 2 and the other factors are invertible. So $s > 0$, the third singular value is 0, and $F^{\mathsf T} u_3 = V \operatorname{diag}(r, s, 0) U^{\mathsf T} u_3 = 0$. So $u_3 = \gamma e'$ for some $\gamma \ne 0$, and by Step 3 part 1 holds with $u_3$ in place of $e'$, up to a nonzero factor. Write both sides in the basis $U$. For the right side,
$$U^{\mathsf T} F \omega^\ast F^{\mathsf T} U = \operatorname{diag}(r, s, 0) \, V^{\mathsf T} \omega^\ast V \, \operatorname{diag}(r, s, 0),$$
whose upper left $2 \times 2$ block is $\begin{pmatrix} r^2 v_1^{\mathsf T} \omega^\ast v_1 & r s \, v_1^{\mathsf T} \omega^\ast v_2 \\ r s \, v_1^{\mathsf T} \omega^\ast v_2 & s^2 v_2^{\mathsf T} \omega^\ast v_2 \end{pmatrix}$, with zeros in the third row and column. For the left side, the lemma with the orthogonal $M = U^{\mathsf T}$ (for which $M^{-\mathsf T} = M$ and $\det M = \pm 1$) gives $U^{\mathsf T} [u_3]_\times U = \pm [U^{\mathsf T} u_3]_\times = \pm [e_3]_\times$. Let $N = U^{\mathsf T} \omega^{\ast\prime} U$, so $N_{ij} = u_i^{\mathsf T} \omega^{\ast\prime} u_j$. A direct product with $[e_3]_\times = \begin{pmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}$ gives
$$[e_3]_\times N [e_3]_\times^{\mathsf T} = \begin{pmatrix} N_{22} & -N_{12} & 0 \\ -N_{12} & N_{11} & 0 \\ 0 & 0 & 0 \end{pmatrix}.$$
The sign $\pm$ appears twice and cancels. So part 1 holds if and only if the two symmetric $2 \times 2$ blocks are proportional with a nonzero factor. The block of the right side is not zero, because $V^{\mathsf T} \omega^\ast V$ is positive definite and $r, s > 0$. Two symmetric $2 \times 2$ matrices, the second nonzero, are proportional if and only if their three pairs of entries have equal ratios, in the cross product sense. This is the chain of part 2, with two independent equalities. When $\omega^{\ast\prime} = \omega^\ast$, each side of each equality is linear in $\omega^\ast$, so each cross product is quadratic. $\square$

**A numeric check.** With $K = K'$, $f = 800$, $c = (320, 240)$, $R$ a turn of 10 degrees about $Y$ and $t = (1, 0.2, 0.1)$, a script built $F$ and $e' = K t = (832, 184, 0.1)$, which is the pixel $(8320, 1840)$. Every entry of $[e']_\times \omega^\ast [e']_\times^{\mathsf T}$ divided by the matching entry of $(\det K)^2 F \omega^\ast F^{\mathsf T}$ was $1$ within $10^{-15}$, and the lemma held for a random $M$ within $5 \cdot 10^{-16}$.

## Consequences

- **Counting with a constant camera.** If $K' = K$, the unknown $\omega^\ast$ is symmetric and defined up to scale, so it has 5 unknowns. Each pair gives 2 equations. Three views give three pairs and 6 equations, which in general fix $\omega^\ast$; Maybank and Faugeras (1992) used three views for this reason. Any 5 of the quadratic equations have at most $2^5 = 32$ isolated complex solutions, by the Bezout bound. Then $K$ follows from $\omega^\ast$ by a triangular factorization, as on the [image of the absolute conic](/image-of-the-absolute-conic/) page.
- **Fewer unknowns.** Each known property of $K$ removes unknowns. With zero skew, square pixels and a known principal point, only the focal lengths remain. If both views have such cameras with different unknown focal lengths, one pair gives 2 equations in 2 unknowns.
- **Why only two.** A fundamental matrix has 7 degrees of freedom. The relative pose of two calibrated cameras, a rotation and a translation up to scale, has 5. So a pair can constrain at most $7 - 5 = 2$ parameters of the calibration. The Kruppa equations reach this count in general.
- **No plane at infinity.** The equations involve only $F$, never the plane at infinity or a projective reconstruction that is consistent across views. This is their advantage. It is also their weakness: the methods based on the absolute dual quadric use the plane at infinity, which is shared by all views, and that extra coupling is lost here (see [self-calibration](/self-calibration/)).
- **Calibrated case.** If $K$ and $K'$ are known, the equations reduce to a property of the [essential matrix](/essential-matrix/) $E = K'^{\mathsf T} F K$: $E E^{\mathsf T} \sim [t]_\times [t]_\times^{\mathsf T}$, whose nonzero eigenvalues are equal. This is the equal singular value condition of $E$.
- **Heuristic note on numerics.** The equations are quadratic and are formed from $F$, which is estimated with noise. In practice, solutions from Kruppa equations are often used only as start values for a [bundle adjustment](/bundle-adjustment/) with the intrinsics as unknowns. This is a practice, not a theorem.

## Tightness

- **Pure translation gives nothing.** If $K' = K$ and $R = I$, then $F = K^{-\mathsf T} [t]_\times K^{-1} = [e']_\times / \det K$ by the lemma. Then $F \omega^\ast F^{\mathsf T} = [e']_\times \omega^\ast [e']_\times^{\mathsf T} / (\det K)^2$ for every $\omega^\ast$, so both equations hold for every symmetric $\omega^\ast$ and give no information. A script confirmed $F / [e']_\times = 1 / 640000 = 1 / \det K$ entry by entry for the camera of the check above. In this case no self-calibration method can find $K$ from the pair, because the views are related by translation only.
- **Degenerate although calibration is possible.** Sturm (2000) showed motions for which the Kruppa equations of all pairs do not fix $K$, while the methods that use the plane at infinity do. One such case is a camera whose centers lie on a sphere and whose optical axes all pass through the center of the sphere, as for a camera that moves around an object and keeps it in the middle of the view. So the equations can be strictly weaker than full self-calibration.
- **Critical motions.** For some motion sequences no method recovers $K$ (Sturm 1997); the Kruppa equations then fail too.
- **No translation.** If the camera only rotates about its center, then $t = 0$, $F$ is not defined, and the theorem does not apply. $K$ can then be found from the homographies between the views instead (HZ Section 19.6).
- **The counts are over the complex numbers.** The 32 is a bound on isolated complex solutions of 5 quadrics. Some solutions are complex or give an $\omega^\ast$ that is not positive definite, and those are rejected.

## History

Erwin Kruppa derived the equations in 1913, in work on finding an object from two perspective views with known inner orientation. Faugeras, Luong and Maybank brought them into computer vision at ECCV 1992, and Maybank and Faugeras gave the theory in the International Journal of Computer Vision in the same year, as the first method for the self-calibration of a moving camera from point matches only. Hartley (1997) gave the short form with the singular value decomposition of $F$. Sturm (2000) analyzed when the equations lose information, which helped to move the field toward methods based on the absolute dual quadric and on stratification.

## References
