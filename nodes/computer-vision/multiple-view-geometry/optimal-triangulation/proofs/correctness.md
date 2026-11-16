---
title: The real roots of the degree 6 polynomial and the point at infinity of the pencil contain the minimizer of the two-view reprojection error
proves: [correctness]
status: full
---

We use the notation of the page. $F$ is a fundamental matrix of rank 2 with $\tilde{\mathbf{x}}_2^{\mathsf T}F\tilde{\mathbf{x}}_1 = 0$ for matching points. The measured points $\mathbf{x}_1$, $\mathbf{x}_2$ are not at the epipoles. Image coordinates are Euclidean, so $d(\cdot, \cdot)$ is the Euclidean distance in each image. The arithmetic is exact (real RAM). The cost of a pair is $C(\hat{\mathbf{x}}_1, \hat{\mathbf{x}}_2) = d(\mathbf{x}_1, \hat{\mathbf{x}}_1)^2 + d(\mathbf{x}_2, \hat{\mathbf{x}}_2)^2$.

**Claim.** (a) The pair $(\hat{\mathbf{x}}_1, \hat{\mathbf{x}}_2)$ returned by lines L1 to L9 satisfies $\hat{\mathbf{x}}_2^{\mathsf T}F\hat{\mathbf{x}}_1 = 0$ and has the least cost among all pairs that satisfy it. (b) If $F$ comes from finite cameras $P_1$, $P_2$ with distinct centers and the rays of the corrected points meet at a finite point $\hat{\mathbf{X}}$, then line L10 returns $\hat{\mathbf{X}}$, and $\hat{\mathbf{X}}$ has the least reprojection error $d(\mathbf{x}_1, P_1\mathbf{X})^2 + d(\mathbf{x}_2, P_2\mathbf{X})^2$ among all points $\mathbf{X}$ off the baseline.

**Lemma 1 (Euclidean changes of frame).** Let $A_1$, $A_2$ be Euclidean motions of the two images (here $A_i = R_iT_i$). Replacing each point $\mathbf{p}$ of image $i$ by $A_i\mathbf{p}$ and $F$ by $A_2^{-\mathsf T}FA_1^{-1}$ keeps the epipolar constraint and all distances. So it is enough to prove part (a) in the new frames.

*Proof.* $(A_2\tilde{\mathbf{p}}_2)^{\mathsf T}A_2^{-\mathsf T}FA_1^{-1}(A_1\tilde{\mathbf{p}}_1) = \tilde{\mathbf{p}}_2^{\mathsf T}F\tilde{\mathbf{p}}_1$, and Euclidean motions keep distances. Line L9 applies the inverse motions. $\square$

**Lemma 2 (the normal form of $F$).** After lines L1 to L3, $\mathbf{x}_1 = \mathbf{x}_2 = (0, 0)$, the epipoles are $\mathbf{e}_1 = (1, 0, f)$ and $\mathbf{e}_2 = (1, 0, f')$, and
$$F = \begin{pmatrix} ff'd & -f'c & -f'd \\ -fb & a & b \\ -fd & c & d \end{pmatrix}, \qquad ad - bc \ne 0 .$$

*Proof.* Line L1 moves the points to the origin. Line L2 scales the epipole $\mathbf{e} = (e_1, e_2, e_3)$ so that $e_1^2 + e_2^2 = 1$; this is possible because the point at the origin is not the epipole, so $(e_1, e_2) \ne (0, 0)$. The rotation $R$ of line L3 maps it to $(e_1^2 + e_2^2, -e_2e_1 + e_1e_2, e_3) = (1, 0, e_3)$ and fixes the origin. Now $F\mathbf{e}_1 = \mathbf{0}$ says that the first column of $F$ is $-f$ times the third, and $\mathbf{e}_2^{\mathsf T}F = \mathbf{0}$ says that the first row is $-f'$ times the third. Naming the lower right block $\begin{pmatrix} a & b \\ c & d\end{pmatrix}$ gives the form above. The first row and the first column are combinations of the others, so the rank of $F$ equals the rank of this block, which must be 2. $\square$

**Lemma 3 (the pencil).** For $t \in \mathbb{R}$, let $\mathbf{l}_1(t) = (tf, 1, -t)$, the line through $\mathbf{e}_1$ and $(0, t)$, and $\mathbf{l}_2(t) = F(0, t, 1)^{\mathsf T} = (-f'(ct + d), at + b, ct + d)$. For $t = \infty$, let $\mathbf{l}_1 = (f, 0, -1)$, the line through $\mathbf{e}_1$ in the direction $(0, 1)$, and $\mathbf{l}_2 = F(0, 1, 0)^{\mathsf T} = (-f'c, a, c)$. Then every point $\hat{\mathbf{x}}_1 \ne \mathbf{e}_1$ lies on exactly one $\mathbf{l}_1(t)$, and its epipolar line $F\hat{\mathbf{x}}_1$ is $\mathbf{l}_2(t)$ up to a nonzero factor.

*Proof.* The lines through $\mathbf{e}_1$ meet the line $x = 0$ in one point $(0, t)$, or are parallel to it ($t = \infty$); the two vectors $(\mathbf{e}_1, (0, t, 1))$ span the line, and the cross product gives $\mathbf{l}_1(t)$. A point $\hat{\mathbf{x}}_1 \ne \mathbf{e}_1$ on this line is $\alpha\mathbf{e}_1 + \beta(0, t, 1)$ with $\beta \ne 0$, so $F\hat{\mathbf{x}}_1 = \beta F(0, t, 1)^{\mathsf T}$. This is not zero, because the null space of $F$ is spanned by $\mathbf{e}_1$, whose first entry is 1. The case $t = \infty$ is the same with $(0, 1, 0)$. $\square$

**Lemma 4 (the cost along the pencil).** The distance from the origin to the line $(\lambda, \mu, \nu)$ is $|\nu|/\sqrt{\lambda^2 + \mu^2}$, reached at the point $(-\lambda\nu, -\mu\nu, \lambda^2 + \mu^2)$. So
$$s(t) = d(\mathbf{0}, \mathbf{l}_1(t))^2 + d(\mathbf{0}, \mathbf{l}_2(t))^2 = \frac{t^2}{1 + f^2t^2} + \frac{(ct + d)^2}{(at + b)^2 + f'^2(ct + d)^2},$$
with the value $+\infty$ where the second denominator is 0, and $s(\infty) = 1/f^2 + c^2/(a^2 + f'^2c^2)$.

*Proof.* The foot of the perpendicular from the origin to $\lambda x + \mu y + \nu = 0$ is $-\nu(\lambda, \mu)/(\lambda^2 + \mu^2)$, which is the stated homogeneous point, at the stated distance. Insert the lines of Lemma 3. The second denominator is 0 only if $f' = 0$ and $at + b = 0$, and then $\mathbf{l}_2(t)$ is the line at infinity (it is not $\mathbf{0}$, since $at + b$ and $ct + d$ do not vanish together when $ad - bc \ne 0$). $\square$

**Lemma 5 (reduction to the pencil).** The least cost over pairs that satisfy the epipolar constraint equals $\min_t s(t)$ over $t \in \mathbb{R} \cup \{\infty\}$, and the feet of the perpendiculars at a minimizing $t$ give an optimal pair.

*Proof.* Take a pair that satisfies the constraint with $\hat{\mathbf{x}}_1 \ne \mathbf{e}_1$. By Lemma 3, $\hat{\mathbf{x}}_1$ lies on $\mathbf{l}_1(t)$ and $\hat{\mathbf{x}}_2$ on $\mathbf{l}_2(t)$ for one $t$, so its cost is at least $s(t)$. Conversely, the two feet at any $t$ satisfy the constraint: the foot on $\mathbf{l}_1(t)$ is $\mathbf{e}_1$, for which $F\mathbf{e}_1 = \mathbf{0}$, or a point whose epipolar line is $\mathbf{l}_2(t)$, which contains the second foot. Their cost is $s(t)$.

It remains to treat the pairs with $\hat{\mathbf{x}}_1 = \mathbf{e}_1$, which have cost at least $d(\mathbf{0}, \mathbf{e}_1)^2 = 1/f^2$ (infinite if $f = 0$). If $c \ne 0$, then $t = -d/c$ gives $s(t) = t^2/(1 + f^2t^2) \le 1/f^2$. If $c = 0$, then $a \ne 0$ and $s(\infty) = 1/f^2$. So such pairs are never better than the pencil. The pairs with $\hat{\mathbf{x}}_2 = \mathbf{e}_2$ cost at least $1/f'^2$, and $s(0) = d^2/(b^2 + f'^2d^2) \le 1/f'^2$, with $d \ne 0$ if $b = 0$. So they are never better either. $\square$

**Lemma 6 (the stationary points).** Where the second denominator $Q(t) = (at + b)^2 + f'^2(ct + d)^2$ is positive,
$$s'(t) = \frac{2t}{(1 + f^2t^2)^2} - \frac{2(ad - bc)(at + b)(ct + d)}{Q(t)^2},$$
so $s'(t) = 0$ if and only if $g(t) = tQ(t)^2 - (ad - bc)(1 + f^2t^2)^2(at + b)(ct + d) = 0$.

*Proof.* The derivative of $t^2/(1 + f^2t^2)$ is $2t/(1 + f^2t^2)^2$. For the second term,
$$\frac{d}{dt}\frac{(ct + d)^2}{Q} = \frac{2(ct + d)\left[cQ - (ct + d)\left(a(at + b) + f'^2c(ct + d)\right)\right]}{Q^2} = \frac{2(ct + d)(at + b)\left[c(at + b) - a(ct + d)\right]}{Q^2},$$
and $c(at + b) - a(ct + d) = bc - ad$. Multiplying $s'(t)$ by the positive number $(1 + f^2t^2)^2Q^2/2$ gives $g(t)$. $\square$

**Proof of part (a).** On the projective line $\mathbb{R} \cup \{\infty\}$, which is compact, $s$ is continuous as a map to $[0, +\infty]$, so it reaches its minimum, and the minimum is finite by Lemma 5 (for example $s(0)$ or $s(-d/c)$ is finite). A minimizer is either $t = \infty$ or a finite point with $Q > 0$ where $s' = 0$, that is, a real root of $g$ by Lemma 6. If $g$ is the zero polynomial, then $s$ is constant where $Q > 0$, and $t = \infty$ is also a minimizer. Line L6 evaluates $s$ at all real roots of $g$ and at $\infty$ and keeps the least, so it finds a minimizer. Lines L7 and L8 build the feet of Lemma 4, which form an optimal pair by Lemma 5, and line L9 maps them back by Lemma 1. $\square$

**Proof of part (b).** The corrected points satisfy the epipolar constraint, so their back-projected rays lie in one epipolar plane. By assumption they meet at the finite point $\hat{\mathbf{X}}$, so $P_i\hat{\mathbf{X}} \sim \hat{\mathbf{x}}_i$, and the linear method of line L10 returns $\hat{\mathbf{X}}$ (see [linear triangulation](/linear-triangulation/)). The reprojection error of $\hat{\mathbf{X}}$ equals the cost of the corrected pair. Any point $\mathbf{X}$ off the baseline projects to a pair that satisfies the epipolar constraint, so by part (a) its reprojection error is at least that cost. $\square$

**Remark (projective invariance).** The output of lines L1 to L9 depends only on $F$ and the measured points. If the cameras are replaced by $P_iH^{-1}$ for an invertible $4 \times 4$ matrix $H$, the fundamental matrix stays the same up to scale, so the corrected points do not change, and the triangulated point becomes $H\hat{\mathbf{X}}$.

**Remark (floating point).** The roots of $g$ are found numerically, so line L6 compares a few values of $s$ that carry rounding errors; near a double root the chosen $t$ can be off by about the square root of the machine precision, which changes $s$ only to second order.
