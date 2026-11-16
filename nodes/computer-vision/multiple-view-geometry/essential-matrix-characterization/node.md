---
tag: 7NN1Q0
kind: theorem
slug: essential-matrix-characterization
name: Characterization of essential matrices
aliases:
- Huang-Faugeras constraint
area: computer-vision/multiple-view-geometry
level: advanced
summary: "A nonzero real 3 by 3 matrix is essential exactly when its singular values are (s, s, 0), or exactly when det E = 0 and 2 E E^T E - tr(E E^T) E = 0. Minimal solvers use these cubics."
prereqs: [essential-matrix, singular-value-decomposition]
see_also: [essential-matrix-decomposition, five-point-algorithm, eight-point-algorithm, fundamental-matrix, minimal-solver, relative-pose-problem, special-orthogonal-group, skew-symmetric-matrix-of-a-vector]
sources:
  - paper: doi:10.1109/34.41368
    title: "Thomas S. Huang and Olivier D. Faugeras, Some properties of the E matrix in two-view motion estimation, IEEE Transactions on Pattern Analysis and Machine Intelligence 11(12), 1989, 1310-1312"
    locator: "the condition that one singular value of E is zero and the other two are equal, as necessary and sufficient"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 9.6, The essential matrix (Result 9.17 and its proof by the SVD)"
  - book: isbn:9780387008936
    title: "Yi Ma, Stefano Soatto, Jana Kosecka and S. Shankar Sastry, An Invitation to 3-D Vision, Springer, 2004"
    locator: "Chapter 5, Section 5.1.2 (elementary properties of the essential matrix: the characterization and the projection onto the essential space)"
  - paper: doi:10.1109/TPAMI.2004.17
    title: "David Nister, An efficient solution to the five-point relative pose problem, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(6), 2004"
    locator: the cubic constraints det E = 0 and 2 E E^T E - trace(E E^T) E = 0 as the ten equations of the solver
  - paper: doi:10.1007/BF00054997
    title: "Olivier D. Faugeras and Stephen Maybank, Motion from point matches, multiplicity of solutions, International Journal of Computer Vision 4(3), 1990, 225-246"
    locator: the algebraic constraints on E and the number of solutions from five matches
---

The characterization theorem gives two exact tests for a real $3 \times 3$ matrix to be an [essential matrix](/essential-matrix/) $E = [\mathbf{t}]_\times R$. The first is on the singular values: $(s, s, 0)$ with $s > 0$. The second is a set of polynomial equations of degree 3 in the entries: $\det E = 0$ and $2EE^{\mathsf T}E - \operatorname{tr}(EE^{\mathsf T})E = 0$. The first test is the way to project a noisy estimate onto the essential matrices, and the second is the system that the [five-point algorithm](/five-point-algorithm/) and other [minimal solvers](/minimal-solver/) solve. The word "real" matters: over the complex numbers the cubic equations have solutions that are not essential.

## Statement

**Theorem.** Let $E$ be a real $3 \times 3$ matrix, $E \ne 0$. The following three conditions are equivalent.

1. $E = [\mathbf{t}]_\times R$ for some $\mathbf{t} \in \mathbb{R}^3$, $\mathbf{t} \ne \mathbf{0}$, and some rotation $R$ ($R^{\mathsf T}R = I$, $\det R = 1$).
2. $E$ has rank 2 and its two nonzero singular values are equal, that is, its singular values are $(s, s, 0)$ with $s > 0$.
3. $\det E = 0$ and $2EE^{\mathsf T}E - \operatorname{tr}(EE^{\mathsf T})\,E = 0$.

Moreover, when they hold with $E = U\operatorname{diag}(s, s, 0)V^{\mathsf T}$, $\det U = \det V = 1$, and $\mathbf{u}_3$ the third column of $U$, one factorization is $\mathbf{t} = -s\,\mathbf{u}_3$ and $R = UWV^{\mathsf T}$ with $W = \begin{pmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}$.

**Corollary (the closest essential matrix).** Let $G$ be a real $3 \times 3$ matrix with an SVD $G = U\operatorname{diag}(s_1, s_2, s_3)V^{\mathsf T}$, $s_1 \ge s_2 \ge s_3 \ge 0$. Among all matrices with singular values $(m, m, 0)$, $m \ge 0$, the closest to $G$ in the Frobenius norm is $U\operatorname{diag}(\bar m, \bar m, 0)V^{\mathsf T}$ with $\bar m = (s_1 + s_2)/2$.

Condition 2 and its equivalence with condition 1 are the result of Huang and Faugeras (1989), and Hartley and Zisserman state it as Result 9.17. The cubic equations of condition 3 are the ones that Nister (2004) uses.

## In plain words

An essential matrix is made of a rotation and a direction of travel. The theorem says how to tell, from the nine numbers alone, whether a matrix can be written that way. One test looks at how the matrix stretches space: it must flatten one direction to nothing and stretch the other two by the same amount. The other test is a short list of equations that the nine numbers must satisfy. The equations are what a solver can use, because they are polynomials. The stretch test is what a program uses to clean up a noisy estimate: keep the two main directions, give them the same stretch, and drop the third. Both tests work only for matrices of ordinary real numbers.

## Proof

We use two facts. First, for a rotation $U$ and a vector $\mathbf{a}$, $[U\mathbf{a}]_\times = U[\mathbf{a}]_\times U^{\mathsf T}$, because a rotation keeps cross products: $U\mathbf{p} \times U\mathbf{q} = U(\mathbf{p} \times \mathbf{q})$. Second, $[\mathbf{e}_3]_\times = Z = \begin{pmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}$, and a direct product gives $ZW = \operatorname{diag}(-1, -1, 0)$.

**1 implies 2.** $EE^{\mathsf T} = [\mathbf{t}]_\times RR^{\mathsf T}[\mathbf{t}]_\times^{\mathsf T} = -[\mathbf{t}]_\times^2 = \|\mathbf{t}\|^2 I - \mathbf{t}\mathbf{t}^{\mathsf T}$. This matrix maps $\mathbf{t}$ to $\mathbf{0}$ and each vector orthogonal to $\mathbf{t}$ to $\|\mathbf{t}\|^2$ times itself. So its eigenvalues are $\|\mathbf{t}\|^2, \|\mathbf{t}\|^2, 0$, and the singular values of $E$, their square roots, are $(\|\mathbf{t}\|, \|\mathbf{t}\|, 0)$ with $\|\mathbf{t}\| > 0$.

**2 implies 1.** Take an SVD $E = U\operatorname{diag}(s, s, 0)V^{\mathsf T}$ with orthogonal $U$ and $V$. If $\det U = -1$, change the sign of the third column of $U$; this does not change the product, because the third singular value is 0. Do the same for $V$. Now $U$ and $V$ are rotations. Then
$$E = sU\operatorname{diag}(1, 1, 0)V^{\mathsf T} = -sUZWV^{\mathsf T} = -s\,(UZU^{\mathsf T})(UWV^{\mathsf T}) = [-s\,U\mathbf{e}_3]_\times\,(UWV^{\mathsf T}) .$$
$UWV^{\mathsf T}$ is a product of rotations, so it is a rotation, and $\mathbf{t} = -s\,\mathbf{u}_3 \ne \mathbf{0}$. This also proves the factorization in the statement.

**2 is equivalent to 3.** Let $E = U\operatorname{diag}(s_1, s_2, s_3)V^{\mathsf T}$ be any SVD, and put $S = s_1^2 + s_2^2 + s_3^2 > 0$. Then $EE^{\mathsf T}E = U\operatorname{diag}(s_1^3, s_2^3, s_3^3)V^{\mathsf T}$ and $\operatorname{tr}(EE^{\mathsf T}) = S$, so
$$2EE^{\mathsf T}E - \operatorname{tr}(EE^{\mathsf T})E = U\operatorname{diag}\big(s_1(2s_1^2 - S),\ s_2(2s_2^2 - S),\ s_3(2s_3^2 - S)\big)V^{\mathsf T} .$$
This is zero if and only if each $s_i$ is 0 or satisfies $s_i^2 = S/2$. If singular values $(s, s, 0)$, $s > 0$, are given, then $S = 2s^2$, the two nonzero values satisfy $s^2 = S/2$, and $\det E = \pm s \cdot s \cdot 0 = 0$. So 2 implies 3. For the converse, let $k$ be the number of nonzero singular values; $k \ge 1$ because $E \ne 0$. Each of them has square $S/2$, so $S = kS/2$, and since $S > 0$, $k = 2$. The two nonzero singular values are both $\sqrt{S/2}$, which is condition 2. $\square$

**Proof of the corollary.** By von Neumann's trace inequality, $\operatorname{tr}(G^{\mathsf T}H) \le \sum_i s_i h_i$ for real $3 \times 3$ matrices with singular values $s_i$ and $h_i$ in decreasing order. For $H$ with singular values $(m, m, 0)$ this gives
$$\|G - H\|_F^2 = \|G\|_F^2 + \|H\|_F^2 - 2\operatorname{tr}(G^{\mathsf T}H) \ge (s_1 - m)^2 + (s_2 - m)^2 + s_3^2 .$$
The right side is smallest at $m = \bar m = (s_1 + s_2)/2$, and $H = U\operatorname{diag}(\bar m, \bar m, 0)V^{\mathsf T}$ attains it, since then $G - H = U\operatorname{diag}(s_1 - \bar m, s_2 - \bar m, s_3)V^{\mathsf T}$. $\blacksquare$

## Consequences

- **Five degrees of freedom.** Condition 1 gives the count directly: 3 for $R$ and 2 for the direction of $\mathbf{t}$, so the essential matrices up to scale form a set of dimension 5 inside the 8-dimensional space of $3 \times 3$ matrices up to scale. Each match gives one linear equation, so five matches are the minimum for calibrated cameras.
- **The ten equations of the five-point solver.** Condition 3 is one equation of degree 3 ($\det E = 0$) and nine of degree 3 (the entries of the matrix equation). Five matches leave a four-dimensional space of matrices $E = xX + yY + zZ + W$, and the [five-point algorithm](/five-point-algorithm/) solves these ten cubics in $(x, y, z)$. That the problem has at most 10 complex solutions for five points in general position is a result of Demazure (1988) and of Faugeras and Maybank (1990); it is cited here, not proved.
- **Over the reals one equation is enough.** The proof shows that for a real $E \ne 0$ the matrix equation alone forces $k = 2$ nonzero singular values, so it already implies $\det E = 0$. Solvers keep $\det E = 0$ anyway, because they work with polynomials whose roots can be complex.
- **Projection of a noisy estimate.** The corollary is the last step of the essential matrix form of the [eight-point algorithm](/eight-point-algorithm/), and of many other linear methods: replace the singular values by $(\bar m, \bar m, 0)$. Since $E$ is defined up to scale, $(1, 1, 0)$ is just as common. The projection is optimal in the Frobenius norm of the matrix, which has no direct meaning in the images; it is a convenient step, not a statistically optimal estimate.
- **Pose from the SVD.** The factorization in the statement is one of four; the [decomposition page](/essential-matrix-decomposition/) proves that there are exactly four and shows how [cheirality](/cheirality/) picks one.
- **Fundamental matrices are not constrained this way.** In pixel coordinates, $F = K_2^{-\mathsf T}EK_1^{-1}$ only has rank 2. The equal singular values come back only after the intrinsics are removed. This is the basis of some [self-calibration](/self-calibration/) methods, which look for $K$ that makes $K^{\mathsf T}FK$ essential.

## Tightness

- **"Real" is needed.** The complex matrix $E = \begin{pmatrix} 1 & i & 0 \\ i & -1 & 0 \\ 0 & 0 & 0 \end{pmatrix}$ has $\det E = 0$ and $EE^{\mathsf T} = 0$ (the transpose, not the conjugate transpose: the first row times itself is $1 + i^2 = 0$, and the rows are orthogonal in the same sense). So $2EE^{\mathsf T}E - \operatorname{tr}(EE^{\mathsf T})E = 0$, and condition 3 holds. But $E$ has rank 1, since its second row is $i$ times the first. The proof breaks because a complex matrix has no SVD of the form $U\Sigma V^{\mathsf T}$ with real orthogonal factors.
- **$E \ne 0$ is needed.** The zero matrix satisfies condition 3 and is not essential.
- **Rank 2 alone is not enough.** $G = \operatorname{diag}(1, 2, 0)$ has rank 2 and is a [fundamental matrix](/fundamental-matrix/), but $2GG^{\mathsf T}G - 5G = \operatorname{diag}(-3, 6, 0) \ne 0$.
- **Equal singular values alone are not enough.** The identity has singular values $(1, 1, 1)$ and rank 3; condition 3 fails with $2I - 3I = -I$.
- **The scale is free.** All three conditions hold for $\lambda E$ whenever they hold for $E$, $\lambda \ne 0$; a negative $\lambda$ is absorbed by the sign of $\mathbf{t}$.

## History

Longuet-Higgins (1981) introduced the matrix $E$ of the bilinear constraint and gave a linear method to find it from eight matches. Huang and Faugeras (1989) proved that a real matrix is essential if and only if one singular value is zero and the other two are equal, and noted that the linear method does not enforce this. The cubic equations appear in the study of how many solutions five matches allow: Demazure (1988) showed that there are 10 complex solutions in general, against the 11 that Kruppa (1913) had claimed, and Faugeras and Maybank (1990) studied the same count. Nister (2004) built his five-point solver on these ten cubics. Hartley and Zisserman (2000, second edition 2004) and Ma, Soatto, Kosecka and Sastry (2004) give textbook proofs by the SVD.

## References
