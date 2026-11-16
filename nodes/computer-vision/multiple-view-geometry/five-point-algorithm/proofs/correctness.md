---
title: Every essential matrix that fits five point pairs is a root of the degree 10 polynomial of the five-point algorithm, and the algorithm returns it
proves: [correctness]
status: full
---

We use the notation of the page. The input is $n \ge 5$ pairs of points in normalized image coordinates, $\mathbf{x}_i = (u_i, v_i, 1)^{\mathsf T}$ and $\mathbf{x}'_i = (u'_i, v'_i, 1)^{\mathsf T}$. A real $3 \times 3$ matrix is essential when it is $[\mathbf{t}]_\times R$ for a rotation $R$ and a vector $\mathbf{t} \ne \mathbf{0}$. We use the [characterization theorem](/essential-matrix-characterization/): a real $3 \times 3$ matrix $E \ne 0$ is essential if and only if $\det E = 0$ and $2EE^{\mathsf T}E - \operatorname{tr}(EE^{\mathsf T})E = 0$. We work in exact arithmetic and with $n = 5$; the remarks at the end deal with $n > 5$, the polish of line L9 and the tolerances.

**Hypotheses.** (H1) The $5 \times 9$ matrix $A$ of line L1 has rank 5. (H2) The left $10 \times 10$ block of the matrix $M$ of line L3 is invertible. (H3) The polynomial $\det B(z)$ of line L7 is not identically zero. (H4) For each real root $z$ of $\det B(z)$, the matrix $B(z)$ has rank 2. These hold for points in general position, and the code reports nothing for a root where (H4) fails.

**Claim.** (a) Let $E$ be a real essential matrix with $\mathbf{x}'^{\mathsf T}_i E\mathbf{x}_i = 0$ for $i = 1, \ldots, 5$, and suppose that $E$ is not in the span of $X$, $Y$ and $Z$. Then the canonical form of $E$ is one of the outputs. (b) Every output satisfies the five epipolar constraints. (c) The number of outputs is at most 10. (d) If, in addition, the five pairs have exactly 10 complex solutions with distinct values of $z$, every output is an essential matrix, and the number of outputs is even.

**Lemma 1 (the solution space).** Under (H1), the real matrices $G$ with $\mathbf{x}'^{\mathsf T}_i G\mathbf{x}_i = 0$ for all $i$ are exactly $G = xX + yY + zZ + wW$ with $(x, y, z, w) \in \mathbb{R}^4$.

*Proof.* By Lemma 1 of the [eight-point proof](/eight-point-algorithm/), the constraints say $A\mathbf{g} = \mathbf{0}$. The null space of $A$ has dimension 4. The code pads $A$ to 9 rows with zeros, and the right singular vectors of the four zero singular values are orthonormal and lie in the null space, so they span it. Line L2 takes them as $X$, $Y$, $Z$ and $W$. $\square$

If $E$ is not in the span of $X$, $Y$ and $Z$, then $w \ne 0$, and $E / w = xX + yY + zZ + W$ with new values of $x$, $y$ and $z$. So it is enough to find the solutions with $w = 1$.

**Lemma 2 (the ten cubics).** For $E(x, y, z) = xX + yY + zZ + W$, the ten polynomials $\det E$ and the nine entries of $2EE^{\mathsf T}E - \operatorname{tr}(EE^{\mathsf T})E$ have degree at most 3 in $(x, y, z)$. Let $\mathbf{m}$ be the vector of the 20 monomials of degree at most 3, in the order of the page. Then the ten polynomials are $M\mathbf{m}$, where row $r$ of $M$ holds the coefficients of polynomial $r$.

*Proof.* Each entry of $E$ has degree at most 1. A determinant of a $3 \times 3$ matrix and each entry of $EE^{\mathsf T}E$ are sums of products of three entries, and $\operatorname{tr}(EE^{\mathsf T})E$ is a sum of products of two entries with one entry. So the degree is at most 3. There are exactly 20 monomials $x^a y^b z^c$ with $a + b + c \le 3$. $\square$

So $(x, y, z)$ gives an essential matrix exactly when $M\mathbf{m}(x, y, z) = \mathbf{0}$ (and $E \ne 0$, which holds because $W$ is not in the span of $X$, $Y$ and $Z$).

**Lemma 3 (the reduced system).** Under (H2), $M\mathbf{m} = \mathbf{0}$ is equivalent to $[I \mid C]\,\mathbf{m} = \mathbf{0}$, where $C$ is the matrix of line L5. Write the right part of $\mathbf{m}$ as $\mathbf{m}_R = (xz^2, xz, x, yz^2, yz, y, z^3, z^2, z, 1)$. Then for every row $r$, the row $r$ of $C$ times $\mathbf{m}_R$ equals $b^x_r(z)\,x + b^y_r(z)\,y + b^1_r(z)$, where $b^x_r$ and $b^y_r$ have degree at most 2 and $b^1_r$ has degree at most 3.

*Proof.* $M = [L \mid R]$ with $L$ invertible, and $C = L^{-1}R$. Multiplication by $L^{-1}$ is invertible, so $M\mathbf{m} = \mathbf{0}$ if and only if $L^{-1}M\mathbf{m} = [I \mid C]\mathbf{m} = \mathbf{0}$. The second statement is a regrouping of the ten terms by the factor $x$, $y$ or 1. $\square$

**Lemma 4 (the hidden variable matrix).** For $r = 0, 1, 2$, let row $r$ of $B(z)$ be the coefficients of $x$, $y$ and 1 in (row $4 + 2r$) minus $z$ times (row $5 + 2r$) of $[I \mid C]\mathbf{m}$, counting rows from 0. Then the left monomials cancel, $B(z)$ has entries of degree at most 3, 3 and 4 in its three columns, and every solution $(x, y, z)$ of $[I \mid C]\mathbf{m} = \mathbf{0}$ satisfies $B(z)(x, y, 1)^{\mathsf T} = \mathbf{0}$ and $\det B(z) = 0$. The determinant has degree at most 10.

*Proof.* In the order of the page, the left monomials of rows 4 to 9 are $x^2z$, $x^2$, $y^2z$, $y^2$, $xyz$ and $xy$. So row $4 + 2r$ is $\mu z + (\ldots)$ and row $5 + 2r$ is $\mu + (\ldots)$ with the same monomial $\mu \in \{x^2, y^2, xy\}$, and the difference removes $\mu z$. What remains is $(b^x_{4+2r} - z\,b^x_{5+2r})\,x + (b^y_{4+2r} - z\,b^y_{5+2r})\,y + (b^1_{4+2r} - z\,b^1_{5+2r})$, with degrees at most 3, 3 and 4 by Lemma 3. A solution makes every row of $[I \mid C]\mathbf{m}$ zero, so each difference is zero, which is $B(z)(x, y, 1)^{\mathsf T} = \mathbf{0}$. The vector $(x, y, 1)^{\mathsf T}$ is not zero, so $B(z)$ is singular. Each term of the determinant is a product of one entry from each column, of degree at most $3 + 3 + 4 = 10$. $\square$

**Lemma 5 (the null vector).** If a real $3 \times 3$ matrix $B$ has rank 2, its null space is spanned by the cross product of any two of its rows that are linearly independent, and the largest of the three cross products of line L8 is such a product.

*Proof.* The cross product of two independent rows is nonzero and orthogonal to both. The third row is a combination of these two, so the product is orthogonal to all rows and lies in the null space, which has dimension 1. If two rows are dependent, their cross product is $\mathbf{0}$. Since the rank is 2, at least one pair is independent, so the largest product is nonzero and comes from an independent pair. $\square$

**Proof of part (a).** Scale $E$ so that it is $xX + yY + zZ + W$. By Lemma 2 and Lemma 3, $(x, y, z)$ solves $[I \mid C]\mathbf{m} = \mathbf{0}$, and by Lemma 4, $z$ is a real root of $\det B(z)$. Line L7 finds it. By (H4) and Lemma 5, the vector $\mathbf{v}$ of line L8 spans the null space of $B(z)$, which contains $(x, y, 1)^{\mathsf T}$. So $\mathbf{v} = \kappa(x, y, 1)^{\mathsf T}$ with $\kappa \ne 0$, its third entry is not zero, and $v_1/v_3 = x$ and $v_2/v_3 = y$. At an exact solution the residual of line L9 is zero, so the Gauss-Newton step is zero (or the solve fails), the residual cannot decrease, and line L9 returns $(x, y, z)$ unchanged. Line L10 adds the canonical form of $E$. $\square$

**Proof of part (b).** Every output is a canonical form of $xX + yY + zZ + W$ for real numbers $x$, $y$ and $z$, which satisfies the constraints by Lemma 1. $\square$

**Proof of part (c).** By (H3) and Lemma 4, $\det B(z)$ is a nonzero polynomial of degree at most 10, so it has at most 10 real roots. Line L8 gives at most one output per root. $\square$

**Proof of part (d).** Let the 10 complex solutions have distinct values $z_1, \ldots, z_{10}$. Each $z_k$ is a root of $\det B$ by Lemma 4, which holds over the complex numbers with the same proof. A nonzero polynomial of degree at most 10 with 10 distinct roots has degree exactly 10 and no other roots. So each real root $z$ of $\det B$ is the $z$ of a complex solution $(x, y, z)$. By (H4), the null space of the real matrix $B(z)$ is a real line, so $x$ and $y$ are real, and line L8 returns them. Then $E(x, y, z)$ is a real matrix with $M\mathbf{m} = \mathbf{0}$, and by the characterization theorem it is essential. The non-real roots of a real polynomial come in conjugate pairs, and the roots are simple, so the number of real roots of a polynomial of degree 10 is even. $\blacksquare$

**Remark (more than five points).** For $n > 5$, line L2 takes the four right singular vectors of the four smallest singular values. They span the four-dimensional space of least algebraic error, and the rest of the algorithm is unchanged. On exact data from one essential matrix $E_0$ in general position, $A$ has rank 8, $E_0$ lies in the null space and therefore in the span, and part (a) still applies. On noisy data the outputs are essential matrices close to the space, not least squares solutions.

**Remark (the polish and the tolerances).** Line L9 is an addition of the code on this page. It takes Gauss-Newton steps on the ten cubics and keeps a step only if it lowers the norm of the residual, so in floating point it can only improve how well an output satisfies the cubics. It matters when two roots of $\det B$ are close, because then each root has few correct digits. The code skips a root when $|v_3| \le 10^{-12}\|\mathbf{v}\|$; this is the case $w = 0$ of the claim, or a failure of (H4). The roots come from the helper polyroots_real, which keeps the roots whose imaginary part is below its tolerance. Near a double root the count can then differ from the exact count.
