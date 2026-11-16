---
title: The seven-point algorithm returns every singular matrix in the two-dimensional solution space, and there are 1 or 3 of them over the reals
proves: [correctness]
status: full
---

We use the notation of the page. The input is 7 pairs of 2D points, written as $\mathbf{x}_i = (u_i, v_i, 1)^{\mathsf T}$ and $\mathbf{x}'_i = (u'_i, v'_i, 1)^{\mathsf T}$. Lines L1 and L2 move them to $\mathbf{y}_i = T\mathbf{x}_i$ and $\mathbf{y}'_i = T'\mathbf{x}'_i$ and build the $7 \times 9$ matrix $A$ with rows $(\mathbf{y}'_i \otimes \mathbf{y}_i)^{\mathsf T}$. Two nonzero matrices are equal up to scale when one is a nonzero multiple of the other. We work in exact arithmetic; the remarks at the end deal with the two tolerances of the code.

**Claim.** Let $A$ have rank 7, and let $\det$ not vanish on the whole null space of $A$. Then:
(a) the output is a list of matrices of rank at most 2 that satisfy $\mathbf{x}'^{\mathsf T}_i F\mathbf{x}_i = 0$ for $i = 1, \ldots, 7$;
(b) every real matrix $F \ne 0$ with $\det F = 0$ and $\mathbf{x}'^{\mathsf T}_i F\mathbf{x}_i = 0$ for all $i$ is equal up to scale to one of the outputs;
(c) counted with multiplicity, the number of such matrices up to scale is 1 or 3.

**Lemma 1 (the solution space).** If $A$ has rank 7, then the matrices $G$ with $\mathbf{y}'^{\mathsf T}_i G\mathbf{y}_i = 0$ for all $i$ are exactly $G = aF_1 + bF_2$, $(a, b) \in \mathbb{R}^2$, where $F_1$ and $F_2$ are the matrices of line L3.

*Proof.* By Lemma 1 of the [eight-point proof](/eight-point-algorithm/), the constraints say $A\mathbf{g} = \mathbf{0}$. The null space of $A$ has dimension $9 - 7 = 2$. The code pads $A$ with two zero rows and takes the SVD. The right singular vectors of the two smallest singular values, which are both 0, are orthonormal and lie in the null space, so they span it. $\square$

**Lemma 2 (the projective line of solutions).** Every nonzero $aF_1 + bF_2$ is equal up to scale to exactly one of the matrices $P(\alpha) = F_2 + \alpha(F_1 - F_2) = \alpha F_1 + (1 - \alpha)F_2$, $\alpha \in \mathbb{R}$, or to $F_1 - F_2$.

*Proof.* If $a + b \ne 0$, then $aF_1 + bF_2 = (a + b)\,P(\alpha)$ with $\alpha = a/(a + b)$. If $a + b = 0$, then $aF_1 + bF_2 = a(F_1 - F_2)$ with $a \ne 0$. The matrices $F_1$ and $F_2$ are linearly independent, so different $\alpha$ give matrices that are not equal up to scale, and no $P(\alpha)$ is a multiple of $F_1 - F_2$. $\square$

**Lemma 3 (the cubic).** $p(\alpha) = \det P(\alpha)$ is a polynomial of degree at most 3, $p(\alpha) = c_3\alpha^3 + c_2\alpha^2 + c_1\alpha + c_0$, with $c_3 = \det(F_1 - F_2)$ and $c_0 = \det F_2$. Line L4 computes its coefficients exactly from the values $d_{-1}, d_0, d_1, d_2$ at $\alpha = -1, 0, 1, 2$:
$$c_0 = d_0,\quad c_2 = \tfrac12(d_1 + d_{-1}) - d_0,\quad c_3 = \tfrac16\big(d_2 - 4c_2 - c_0 - (d_1 - d_{-1})\big),\quad c_1 = \tfrac12(d_1 - d_{-1}) - c_3 .$$

*Proof.* Each entry of $P(\alpha)$ has degree at most 1 in $\alpha$, and the determinant is a sum of products of three entries, so $p$ has degree at most 3. Write $P(\alpha) = \alpha(F_1 - F_2) + F_2$. The coefficient of $\alpha^3$ comes from taking the $\alpha$ part of every entry, which gives $\det(F_1 - F_2)$, and $p(0) = \det F_2$. For the formulas: $d_1 + d_{-1} = 2c_2 + 2c_0$ and $d_1 - d_{-1} = 2c_3 + 2c_1$, which give $c_2$ and the odd sum $c_3 + c_1$. Next $d_2 = 8c_3 + 4c_2 + 2c_1 + c_0$, so $d_2 - 4c_2 - c_0 = 8c_3 + 2c_1 = 6c_3 + 2(c_3 + c_1)$, which gives $c_3$, and then $c_1$. $\square$

**Proof of part (a).** Every output is $T'^{\mathsf T} G T$, scaled, where $G$ is $P(\alpha)$ for a real root $\alpha$ of $p$ (line L6), or $F_1 - F_2$ when $c_3 = 0$ (line L7). In both cases $\det G = 0$ (for $F_1 - F_2$ because $c_3 = \det(F_1 - F_2) = 0$), so $G$ has rank at most 2, and $G \ne 0$ because $F_1$ and $F_2$ are independent. $G$ lies in the null space of $A$ by Lemma 1. By Lemma 1 of the [normalized eight-point proof](/normalized-eight-point-algorithm/), $T'^{\mathsf T} G T$ has the same rank and satisfies the constraints on the input points. Line L8 only scales it. $\square$

**Proof of part (b).** Let $F$ be such a matrix and put $G = T'^{-\mathsf T} F T^{-1}$. Then $G \ne 0$, $\det G = 0$, and $G$ satisfies the constraints on the moved points, so by Lemma 1 it is in the span of $F_1$ and $F_2$. By Lemma 2 it is equal up to scale to some $P(\alpha)$ or to $F_1 - F_2$. In the first case $p(\alpha) = 0$ and $\alpha$ is real, so line L5 finds $\alpha$ and line L6 adds $P(\alpha)$. In the second case $\det(F_1 - F_2) = 0$, so $c_3 = 0$, and line L7 adds $F_1 - F_2$. Line L8 maps the matrix back to a multiple of $F$. $\square$

**Proof of part (c).** We count the solutions on the projective line of Lemma 2, with multiplicity: a real root $\alpha$ of $p$ counts with its multiplicity as a root, and the point $F_1 - F_2$ counts $3 - \deg p$ times. This is the count of the roots of the homogeneous cubic $q(a, b) = \det(aF_1 + bF_2)$ on the projective line, which is not identically zero by hypothesis. If $\deg p = 3$, a real cubic has 1 or 3 real roots counted with multiplicity, because its complex roots that are not real come in conjugate pairs. If $\deg p = 2$, the real roots number 0 or 2, and $F_1 - F_2$ adds 1. If $\deg p = 1$, there is 1 real root and $F_1 - F_2$ counts twice. If $\deg p = 0$, then $p$ is a nonzero constant and $F_1 - F_2$ counts three times. In every case the total is 1 or 3. $\blacksquare$

**Remark (the true matrix).** If the points are exact images under two cameras with fundamental matrix $F_{\mathrm{true}}$, then $F_{\mathrm{true}}$ is real, has rank 2 and satisfies the constraints, so by part (b) it is among the outputs. The other outputs satisfy the same seven constraints, and seven pairs alone cannot tell them apart; an eighth pair or a consensus test is needed.

**Remark (tolerances).** The code stops with an error when $\sigma_7 \le 10^{-10}\sigma_1$, which is its test of the hypothesis that $A$ has rank 7. It treats $c_3$ as 0 when $|c_3| \le 10^{-10}\max_j |c_j|$. In floating point both tests are thresholds, so near the boundary a solution close to $F_1 - F_2$ can be reported as $F_1 - F_2$ itself, or as a root $\alpha$ of large absolute value. The real roots come from the helper polyroots_real, which returns the roots whose imaginary part is below its tolerance; a double root may then appear once or twice.
