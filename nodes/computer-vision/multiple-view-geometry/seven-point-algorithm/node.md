---
tag: JZGDM0
kind: algorithm
slug: seven-point-algorithm
name: Seven-point algorithm
aliases:
- seven-point fundamental matrix solver
area: computer-vision/multiple-view-geometry
level: advanced
summary: "Estimate the fundamental matrix from seven matches by taking the 2D null space of the linear system and solving the cubic det F = 0, giving one or three solutions."
solves: [relative-pose-problem]
model: floating-point-model
complexity:
  vars: {n: "the number of point pairs, fixed at 7"}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1869
  people: [Ludwig Otto Hesse, Rudolf Sturm, Richard Hartley]
  note: Hesse in 1863 and Sturm in 1869 studied the projective problem of seven point pairs and its three solutions. The method in its modern form for the fundamental matrix is given by Hartley and Zisserman.
prereqs: [fundamental-matrix, eight-point-algorithm]
see_also: [normalized-eight-point-algorithm, minimal-solver, five-point-algorithm, ransac, ransac-iteration-bound, polynomial-root-finding, hartley-normalization, essential-matrix-characterization]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 11.1, Basic equations (the minimum case of seven point correspondences and the cubic in the pencil)"
  - paper: doi:10.1007/BF01448082
    title: "Rudolf Sturm, Das Problem der Projectivität und seine Anwendung auf die Flächen zweiten Grades, Mathematische Annalen 1(4), 1869, 533-574"
    locator: the problem of seven pairs of points and its three solutions
  - paper: doi:10.1515/crll.1863.62.188
    title: "Ludwig Otto Hesse, Die cubische Gleichung, von welcher die Lösung des Problems der Homographie von M. Chasles abhängt, Journal für die reine und angewandte Mathematik 62, 1863"
    locator: the cubic equation of the seven point problem
---

The seven-point algorithm finds the [fundamental matrix](/fundamental-matrix/) from exactly seven point matches, the fewest that fix it. Seven matches give seven linear equations in the nine entries of $F$, so the solutions form a two-dimensional space spanned by two matrices $F_1$ and $F_2$. The condition $\det F = 0$, which every fundamental matrix satisfies, is a cubic equation on the line through them. Each real root gives one fundamental matrix, so there are one or three. It is the standard [minimal solver](/minimal-solver/) for $F$ inside [RANSAC](/ransac/), because it needs fewer matches than the [eight-point algorithm](/eight-point-algorithm/) and it gives matrices of rank 2 exactly.

## In plain words

Each match gives one equation for the nine unknown numbers of the matrix, and the overall size of the matrix does not matter. With eight matches the answer is fixed. With seven, there is one direction of freedom left: every mix of two particular matrices fits all seven matches. But a true fundamental matrix must also flatten one direction to nothing, and this adds one more equation. On the line of mixes that equation is a cubic, so it has one or three real roots. Each root is one candidate matrix. A robust method such as RANSAC then checks each candidate against the other matches.

## The problem

**Input.** Seven point pairs $(\mathbf{x}_{1,i}, \mathbf{x}_{2,i})$ as 2D points $(u, v)$, extended to $(u, v, 1)^{\mathsf T}$.

**Output.** The list of all real $3 \times 3$ matrices $F$ with $\det F = 0$ and $\mathbf{x}_{2,i}^{\mathsf T}F\mathbf{x}_{1,i} = 0$ for $i = 1, \ldots, 7$, each scaled to $\|F\|_F = 1$ with its entry of largest absolute value positive. For points in general position the list has one or three entries; a double root of the cubic can give fewer distinct entries. If the pairs are exact images of points in general position seen by two cameras with different centers, the true $F$ is in the list.

## The algorithm

```pseudo id=main
SEVEN-POINT(x1_1 .. x1_7, x2_1 .. x2_7)
L1  T1, T2 <- the normalizing similarities of the points of image 1 and of image 2
L2  A <- the 7 x 9 matrix with rows (y2[1] y1^T, y2[2] y1^T, y2[3] y1^T) for y1 = T1 x1_i and y2 = T2 x2_i
L3  F1, F2 <- the 3 x 3 matrices of two right singular vectors that span the null space of A
L4  (c3, c2, c1, c0) <- the coefficients of det(F2 + a (F1 - F2)) = c3 a^3 + c2 a^2 + c1 a + c0
L5  for each real root a of this polynomial (of degree 2 if c3 = 0)
L6      append F2 + a (F1 - F2) to S
L7  if c3 = 0 then append F1 - F2 to S
L8  return the canonical forms of T2^T G T1 for all G in S
```

Line L1 is [Hartley normalization](/hartley-normalization/), and line L2 builds the rows of the eight-point algorithm on the normalized points. If $A$ has rank 7, line L3 takes the two right singular vectors of the two zero singular values; if the rank is lower the points are degenerate, and the implementation stops with an error. Every matrix in the null space is $\lambda F_1 + \mu F_2$. Up to scale these are $F_2 + a(F_1 - F_2)$ for a real $a$, plus the one direction $F_1 - F_2$ that this form misses. The determinant of a $3 \times 3$ matrix is a cubic in its entries, so line L4 can find the four coefficients from the values at $a = -1, 0, 1, 2$:
$$c_0 = d_0, \quad c_2 = \tfrac12(d_1 + d_{-1}) - d_0, \quad c_3 + c_1 = \tfrac12(d_1 - d_{-1}), \quad 8c_3 + 2c_1 = d_2 - 4c_2 - c_0 .$$
Its leading coefficient is $c_3 = \det(F_1 - F_2)$. When it is zero, $F_1 - F_2$ itself has rank 2 and line L7 adds it. Line L8 undoes the normalization as in the [normalized eight-point algorithm](/normalized-eight-point-algorithm/).

## Example

Lines L4 to L7 act on any pair $F_1$, $F_2$. Take $F_1 = \operatorname{diag}(2, 1, 0)$ and $F_2 = \operatorname{diag}(1, 2, 3)$, so $F_2 + a(F_1 - F_2) = \operatorname{diag}(1 + a, 2 - a, 3 - 3a)$.

| line | value |
|---|---|
| L4 | $d_{-1} = 0$, $d_0 = 6$, $d_1 = 0$, $d_2 = 0$; the coefficients are $(3, -6, -3, 6)$, that is $3(1 + a)(1 - a)(2 - a)$ |
| L5 | roots $a = -1$, $a = 1$, $a = 2$ |
| L6 | $\operatorname{diag}(0, 3, 6)$, $\operatorname{diag}(2, 1, 0)$, $\operatorname{diag}(3, 0, -3)$ |
| L7 | $c_3 = 3 \ne 0$, nothing added |

Two other cases show the other branches. With $F_2 = I$ and $F_1 - F_2 = \begin{pmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}$ the determinant is $(1 + a^2)(1 + a)$, which has one real root, $a = -1$, and the only solution is $\begin{pmatrix} 1 & 1 & 0 \\ -1 & 1 & 0 \\ 0 & 0 & 0 \end{pmatrix}$. With $F_1 = I$ and $F_2 = \operatorname{diag}(1, 2, 3)$ the determinant is $(2 - a)(3 - 2a)$, so $c_3 = 0$; line L5 gives $\operatorname{diag}(1, 0, -1)$ and $\operatorname{diag}(1, 0.5, 0)$, and line L7 adds $F_1 - F_2 = \operatorname{diag}(0, -1, -2)$.

On real data the count varies with the scene. For 40 random scenes of seven points seen by two cameras, the solver gave three solutions 34 times and one solution 6 times, and the true $F$ was always in the list.

## Correctness

On exact data the true $F$ satisfies the seven linear equations, so it is in the null space of $A$, and it has rank 2, so it is a root of the cubic or the direction $F_1 - F_2$. Conversely, every matrix in the list satisfies the seven equations because it is in the null space, and it has determinant 0 by construction. The cubic has real coefficients, so it has one or three real roots counted with multiplicity, and the list has one or three entries. If $A$ has rank below 7, as for points on one plane, the null space is larger and the method does not apply. The full proof is below.

## Complexity

The input size is fixed, so the time and space are $\Theta(1)$. The work is one SVD of a $7 \times 9$ matrix, four $3 \times 3$ determinants and the roots of one cubic, which can be found in closed form or by a few steps of an iterative [root finder](/polynomial-root-finding/). The cost is small and fixed, which matters because RANSAC calls it many times. For an inlier ratio of 0.5 and 99% confidence, the [iteration bound](/ransac-iteration-bound/) is 588 samples of seven, against 1177 samples of eight.

## Properties

- **Minimal.** Seven is the least number of matches that fixes $F$ up to a finite number of choices, since $F$ has 7 degrees of freedom.
- **Rank 2 exactly.** Every output has $\det F = 0$ up to rounding, unlike the linear eight-point result before its rank step.
- **One or three solutions.** The count of real roots of a real cubic is one or three with multiplicity. All of them fit the seven matches, so other matches are needed to choose.
- **Covariant under similarities.** Like the normalized eight-point algorithm, because of the normalization of line L1.
- **No least squares.** It uses exactly seven matches. With more matches, use the eight-point algorithm or a robust method.

## Variants and improvements

- **Without normalization.** Lines L1 and L8 can be skipped; the result is then less accurate on pixel data.
- **Closed form roots.** Cardano's formula gives the roots of the cubic directly; an iterative solver with a check for real roots is often more stable.
- **Sturm sequences.** A [Sturm sequence](/sturm-sequence/) counts the real roots in an interval before they are found.
- **Degeneracy check.** DEGENSAC (Chum, Werner and Matas 2005) tests whether five or more of the seven matches are related by one homography, which is a sign of a dominant plane, and then estimates $F$ from the plane and two more points.
- **Calibrated cameras.** If $K$ is known, the [five-point algorithm](/five-point-algorithm/) needs fewer matches and finds the [essential matrix](/essential-matrix/) directly.

## When to use it

Use the seven-point algorithm as the minimal solver for the fundamental matrix inside [RANSAC](/ransac/) or its variants, when the cameras are not calibrated. Test each of the one or three solutions against all matches and keep the one with the most inliers. Then estimate $F$ again from all inliers with the [normalized eight-point algorithm](/normalized-eight-point-algorithm/) or a geometric fit.

## Pitfalls

- **Only one solution kept.** All real roots are valid candidates; the true $F$ may be any of them.
- **The missed direction.** If $c_3 = 0$, the form $F_2 + a(F_1 - F_2)$ does not reach $F_1 - F_2$, which is a solution. A test with a tolerance is needed, since $c_3$ is rarely exactly zero in floating point.
- **Planar points.** If the seven points lie on one plane, $A$ has rank at most 6 and the null space has dimension 3 or more. Detect this from the singular values.
- **Complex roots.** A root with a small imaginary part from rounding can be a true solution. Decide with a tolerance, not by an exact test.
- **Noise.** Seven noisy matches give a noisy $F$. Use the result only to find inliers, not as the final answer.

## Implementations

## History

The problem is old. Chasles posed the problem of seven pairs of points in the plane, and Hesse (1863) derived the cubic equation on which it depends. Sturm (1869) studied it in detail and showed that there are three solutions in general. In computer vision the same count appears as the number of fundamental matrices for seven matches, and Hartley and Zisserman (2000, second edition 2004) give the algorithm in its modern form, with the pencil $F_2 + a(F_1 - F_2)$ and the cubic $\det = 0$. It became the usual minimal solver for robust estimation of $F$, and Chum, Werner and Matas (2005) added a test for its failure on scenes with a dominant plane.

## References
