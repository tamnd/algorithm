---
tag: SJPGET
kind: algorithm
slug: five-point-algorithm
name: Five-point algorithm
aliases:
- Nister five-point algorithm
- five-point relative pose solver
area: computer-vision/multiple-view-geometry
level: advanced
summary: "Find the up to ten essential matrices consistent with five calibrated matches by solving a polynomial of degree 10 built from the cubic essential matrix constraints."
solves: [relative-pose-problem]
model: floating-point-model
complexity:
  vars: {n: "the number of point pairs, at least 5"}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2004
  people: [David Nister, Michel Demazure, Olivier Faugeras, Stephen Maybank]
  note: Demazure showed in 1988 that five calibrated matches allow 10 complex solutions. Nister gave the efficient solver through a polynomial of degree 10 in 2003 and 2004.
prereqs: [essential-matrix, essential-matrix-characterization, minimal-solver]
see_also: [relative-pose-problem, essential-matrix-decomposition, seven-point-algorithm, eight-point-algorithm, ransac, nister-visual-odometry, groebner-basis, sturm-sequence]
sources:
  - paper: doi:10.1109/TPAMI.2004.17
    title: "David Nister, An efficient solution to the five-point relative pose problem, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(6), 2004"
    locator: "the four-dimensional null space, the ten cubic constraints, the Gauss-Jordan elimination of the 10 by 20 matrix and the polynomial of degree 10"
  - paper: doi:10.1007/BF00054997
    title: "Olivier D. Faugeras and Stephen Maybank, Motion from point matches, multiplicity of solutions, International Journal of Computer Vision 4(3), 1990, 225-246"
    locator: the number of solutions of the motion problem from five point matches
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 11.3, Two-frame structure from motion (the five-point algorithm for calibrated cameras)"
---

The five-point algorithm finds every [essential matrix](/essential-matrix/) that fits five point matches between two calibrated views. Five is the fewest matches that fix the relative pose up to a finite number of choices, because $E$ has five degrees of freedom. Five linear epipolar equations leave a four-dimensional space $E = xX + yY + zZ + W$. The cubic constraints of the [characterization theorem](/essential-matrix-characterization/) then give ten equations in $x$, $y$, $z$, which Nister (2004) reduced to one polynomial of degree 10 in $z$. There are at most 10 solutions, as Demazure (1988) showed, and in practice often 2 to 4 of them are real. It is the standard [minimal solver](/minimal-solver/) for the [relative pose problem](/relative-pose-problem/) inside [RANSAC](/ransac/).

## In plain words

When the cameras are calibrated, the motion between two views has five unknowns: three for the turn and two for the direction of travel. Each matched point gives one equation, so five matches should be enough. The equations from the matches are simple, but they leave four candidate matrices that can be mixed in any way. Only special mixes are true motion matrices, and the test for that is a set of equations of the third power. The algorithm eliminates unknowns step by step until one equation in one unknown is left, of the tenth power. Each real root of it gives one candidate motion. A robust method then checks the candidates against the other matches.

## The problem

**Input.** Five point pairs $(\hat{\mathbf{x}}_{1,i}, \hat{\mathbf{x}}_{2,i})$ in normalized image coordinates $\hat{\mathbf{x}} = K^{-1}(u, v, 1)^{\mathsf T}$, given by their first two entries. The implementation also accepts $n > 5$ pairs and then uses the four-dimensional space of least algebraic error.

**Output.** The list of real essential matrices $E$ with $\hat{\mathbf{x}}_{2,i}^{\mathsf T}E\hat{\mathbf{x}}_{1,i} = 0$ for all five pairs, each with $\|E\|_F = 1$ and its entry of largest absolute value positive. It has at most 10 entries. For exact matches of points in general position, the true $E$ is in the list.

## The algorithm

```pseudo id=main
FIVE-POINT(x1_1 .. x1_5, x2_1 .. x2_5)
L1  A <- the 5 x 9 matrix with rows (x2[1] x1^T, x2[2] x1^T, x2[3] x1^T) for the pairs (x1_i, x2_i)
L2  X, Y, Z, W <- the 3 x 3 matrices of four right singular vectors that span the null space of A
L3  M <- the 10 x 20 matrix of coefficients of det E = 0 and 2 E E^T E - tr(E E^T) E = 0 for E = x X + y Y + z Z + W
L4  split M into its first 10 columns P and its last 10 columns Q
L5  C <- P^-1 Q, so that the reduced system is [I | C]
L6  B(z) <- the 3 x 3 matrix of polynomials in z with rows: row 5 - z row 6, row 7 - z row 8, row 9 - z row 10 of [I | C]
L7  for each real root z of det B(z)
L8      (x, y, 1) <- the cross product of two rows of B(z), the pair with the largest result, divided by its last entry
L9      polish (x, y, z) by Gauss-Newton steps on the ten cubic equations
L10     append the canonical form of x X + y Y + z Z + W to the list
L11 return the list
```

The 20 columns of $M$ are the monomials of degree at most 3 in $x$, $y$, $z$, in Nister's order: first $x^3, y^3, x^2y, xy^2, x^2z, x^2, y^2z, y^2, xyz, xy$, then $xz^2, xz, x, yz^2, yz, y, z^3, z^2, z, 1$. The scale of $E$ is fixed by setting the weight of $W$ to 1. Line L5 is Gauss-Jordan elimination; for data in general position the left block is invertible. Rows 5 and 6 of the reduced system have leading monomials $x^2z$ and $x^2$, so row 5 minus $z$ times row 6 has no term of degree 3 in $x$ and $y$ together; the same holds for rows 7 and 8 ($y^2z$ and $y^2$) and rows 9 and 10 ($xyz$ and $xy$). What is left in each new row is $x$ times a polynomial in $z$ of degree at most 3, $y$ times one of degree at most 3, and one of degree at most 4. So $B(z)(x, y, 1)^{\mathsf T} = \mathbf{0}$, and a solution needs $\det B(z) = 0$, a polynomial of degree at most $3 + 3 + 4 = 10$. Line L8 finds the null vector of $B(z)$ from its rows. Line L9 is an addition of this implementation and not part of Nister's method: a step is kept only if it reduces the residual of the ten equations, and it restores the digits lost when two roots of $\det B(z)$ are close.

## Example

Take the first five pairs of the [eight-point example](/eight-point-algorithm/): the true pose is $R = \begin{pmatrix} 0.8 & 0 & 0.6 \\ 0 & 1 & 0 \\ -0.6 & 0 & 0.8 \end{pmatrix}$, $\mathbf{t} = (1, 0, 0)$, and the true essential matrix in canonical form is $E/\sqrt2 = \begin{pmatrix} 0 & 0 & 0 \\ 0.42426 & 0 & -0.56569 \\ 0 & 0.70711 & 0 \end{pmatrix}$.

| line | value |
|---|---|
| L1, L2 | $A$ is $5 \times 9$ of rank 5, and $X, Y, Z, W$ span its null space |
| L3 to L5 | $M$ is $10 \times 20$, and its left $10 \times 10$ block is invertible |
| L6, L7 | $\det B(z)$ has four real roots: $-19.22$, $1.6968$, $1.7031$ and $561.9$ |
| L8 | four triples $(x, y, z)$; for the root $1.6968$, which is close to $1.7031$, the matrix has third singular value $6.7 \times 10^{-6}$ instead of 0 |
| L9 | after the polish, the third singular value of every solution is below $10^{-16}$ |
| L10, L11 | four essential matrices, one of which is $E/\sqrt2$ |

All four fit the five matches exactly. The other three matches of the eight-point example, or the test of [cheirality](/cheirality/) after [decomposition](/essential-matrix-decomposition/), single out the true one. Over 60 random scenes the distance of the closest solution to the true $E$ was at most $2.4 \times 10^{-12}$.

## Correctness

Every essential matrix that fits the five matches lies in the null space of $A$, so it is $xX + yY + zZ + wW$; for data in general position $w \ne 0$, and scaling gives $w = 1$. By the characterization theorem it satisfies the ten cubic equations, so $M\mathbf{m} = \mathbf{0}$ for its vector of monomials $\mathbf{m}$, and then $[I \mid C]\mathbf{m} = \mathbf{0}$ and $B(z)(x, y, 1)^{\mathsf T} = \mathbf{0}$. So its $z$ is a root of $\det B(z)$, and when $B(z)$ has rank 2 the null vector found at line L8 is its $(x, y, 1)$. Conversely each output satisfies the five linear equations and the ten cubics, and by the characterization theorem it is a real essential matrix. The polynomial has degree at most 10, so there are at most 10 solutions. The full proof is below.

## Complexity

For five points the work is fixed: one SVD of a $5 \times 9$ matrix (padded to $9 \times 9$), the $10 \times 20$ matrix $M$, one Gauss-Jordan elimination of a $10 \times 10$ system with 10 right sides, the determinant of a $3 \times 3$ matrix of polynomials, and the real roots of a polynomial of degree 10. So the time is $\Theta(1)$. For $n > 5$ points, building $A$ and its SVD cost $\Theta(n)$, and the rest is the same, so the time and the extra space are $\Theta(n)$. Nister finds the real roots with [Sturm sequences](/sturm-sequence/) and bisection; a [companion matrix](/companion-matrix-method/) eigenvalue method or another [root finder](/polynomial-root-finding/) also works.

In [floating point](/floating-point-model/) the weak point is the roots of $\det B(z)$: close roots lose about half of their digits, as the example shows. A short Newton or Gauss-Newton polish on the original ten equations, as in line L9, removes the loss.

## Properties

- **Minimal.** Five matches is the fewest for calibrated cameras.
- **At most 10 solutions.** The polynomial has degree at most 10, and examples exist where all 10 roots are real. In practice the count of real solutions is small, often 2 to 4.
- **Even count.** If the 10 complex solutions have different values of $z$, the complex ones come in conjugate pairs, so the number of real solutions is even.
- **Works on planar scenes.** Unlike the seven-point and eight-point algorithms, it still finds the true $E$ when all points lie on one plane.
- **Exact constraints.** Every output is an exact essential matrix up to rounding; no rank step is needed.
- **Up to the twisted pair.** $E$ fixes the pose only up to four choices; [cheirality](/cheirality/) decides among them.

## Variants and improvements

- **Gröbner basis form.** Stewenius, Engels and Nister (2006) solve the same ten equations by a [Gröbner basis](/groebner-basis/) and the eigenvalues of a $10 \times 10$ action matrix. It avoids the polynomial in one variable and is often more stable.
- **Automatic generators.** Kukelova, Bujnak and Pajdla (2008) build such solvers automatically for many minimal problems.
- **More than five points.** Using the four smallest singular vectors of an $n \times 9$ matrix, as this implementation allows, gives a quick estimate for $n > 5$, but a least squares fit on all inliers is better.
- **Seven or eight points.** For uncalibrated cameras the [seven-point algorithm](/seven-point-algorithm/) finds $F$.
- **Known rotation axis or planar motion.** With extra knowledge, such as the vertical direction from an IMU, fewer points are needed, and the solvers are simpler.

## When to use it

Use the five-point algorithm when the cameras are calibrated and the matches contain outliers. Inside RANSAC it needs 146 samples for an inlier ratio of 0.5 and 99% confidence, against 588 for the seven-point algorithm and 1177 for the eight-point algorithm, as the [iteration bound](/ransac-iteration-bound/) gives. It is the core of [Nister's visual odometry](/nister-visual-odometry/) and of the initial pair in [incremental structure from motion](/incremental-structure-from-motion/). After RANSAC, refine the pose on all inliers with a geometric cost.

## Pitfalls

- **Pixel coordinates.** The input must be normalized image coordinates $K^{-1}\mathbf{x}$, not pixels.
- **Only one solution kept.** All real solutions are candidates. Score each of them against the other matches.
- **Close roots.** Two roots of $\det B(z)$ that are close lose digits. Polish the result, or use a more stable formulation.
- **Missed solutions.** Fixing the weight of $W$ to 1 misses a solution with weight 0. This happens only on a set of data of measure zero, but data near it give large $x$, $y$, $z$.
- **Sign and twist.** $E$ and $-E$ are the same, and each $E$ gives four poses. Use [cheirality](/cheirality/) to pick one.
- **Pure rotation.** If the translation is zero, $E = 0$ and the problem has no meaning. Detect this case, for example with a rotation-only model, before the five-point solver.

## Implementations

## History

Kruppa (1913) studied the motion problem for five points and stated that it has at most 11 solutions. Demazure (1988) showed that the correct number of complex solutions is 10, and Faugeras and Maybank (1990) studied the same count. Nister (2003, journal version 2004) gave an efficient method: Gauss-Jordan elimination of the ten cubic constraints, a hidden variable matrix $B(z)$, and a polynomial of degree 10 solved by Sturm sequences. It made the five-point algorithm practical inside RANSAC and for real-time visual odometry. Stewenius, Engels and Nister (2006) gave a Gröbner basis version.

## References
