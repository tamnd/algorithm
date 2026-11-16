---
title: The roots of Grunert's quartic give exactly the poses that put three points on their rays in front of the camera
proves: [correctness]
status: full
---

We use the notation of the page. The world points $\mathbf{X}_1, \mathbf{X}_2, \mathbf{X}_3$ are not collinear, and the side lengths are $a = \|\mathbf{X}_2 - \mathbf{X}_3\|$, $b = \|\mathbf{X}_1 - \mathbf{X}_3\|$ and $c = \|\mathbf{X}_1 - \mathbf{X}_2\|$. The image points are distinct, $\mathbf{f}_i$ is the unit vector along $(y_{i,1}, y_{i,2}, 1)$, and $\cos\alpha = \mathbf{f}_2 \cdot \mathbf{f}_3$, $\cos\beta = \mathbf{f}_1 \cdot \mathbf{f}_3$, $\cos\gamma = \mathbf{f}_1 \cdot \mathbf{f}_2$. A pose $(R, \mathbf{t})$ with $R \in SO(3)$ is *valid* if $R\mathbf{X}_i + \mathbf{t} = s_i\mathbf{f}_i$ with $s_i > 0$ for $i = 1, 2, 3$. The arithmetic is exact (real RAM), and the root finder of line L5 returns every real root of $G$.

Put $Q(v) = v^2 - 2v\cos\beta + 1$, $p = (a^2 - c^2)/b^2$,
$$N(v) = (p - 1)v^2 - 2p\cos\beta\,v + (1 + p), \qquad D(v) = 2(\cos\gamma - v\cos\alpha),$$
$$G(v) = N^2 - 2\cos\gamma\,ND + \Bigl(1 - \frac{c^2}{b^2}Q\Bigr)D^2 .$$

**Claim.** Assume $G$ is not the zero polynomial. (a) Every pose returned by P3P is valid. (b) Every valid pose is returned. (c) There are at most four valid poses.

**Lemma 1 (the three equations).** A pose is valid with distances $s_1, s_2, s_3 > 0$ only if
$$s_2^2 + s_3^2 - 2s_2s_3\cos\alpha = a^2, \quad s_1^2 + s_3^2 - 2s_1s_3\cos\beta = b^2, \quad s_1^2 + s_2^2 - 2s_1s_2\cos\gamma = c^2. \tag{1}$$
Conversely, if positive $s_1, s_2, s_3$ satisfy (1), then there is exactly one $R \in SO(3)$ and one $\mathbf{t}$ with $R\mathbf{X}_i + \mathbf{t} = s_i\mathbf{f}_i$, and line L11 returns them.

*Proof.* A rigid motion keeps distances, so $\|s_2\mathbf{f}_2 - s_3\mathbf{f}_3\| = a$, and expanding the square gives the first equation; the others are the same. For the converse, put $\mathbf{Y}_i = s_i\mathbf{f}_i$. By (1) the triangles $\mathbf{X}$ and $\mathbf{Y}$ have the same side lengths. For a triangle $\mathbf{P}$, line L11 builds the frame $\mathbf{e}_1 = (\mathbf{P}_2 - \mathbf{P}_1)/\|\mathbf{P}_2 - \mathbf{P}_1\|$, $\mathbf{e}_3$ the unit normal along $(\mathbf{P}_2 - \mathbf{P}_1) \times (\mathbf{P}_3 - \mathbf{P}_1)$, $\mathbf{e}_2 = \mathbf{e}_3 \times \mathbf{e}_1$. This is a right-handed orthonormal frame. In it, $\mathbf{P}_2 - \mathbf{P}_1$ has coordinates $(c, 0, 0)$, and $\mathbf{P}_3 - \mathbf{P}_1$ has coordinates $(h_1, h_2, 0)$ with $h_1 = (b^2 + c^2 - a^2)/(2c)$ by the law of cosines and $h_2 = \sqrt{b^2 - h_1^2} > 0$, because the cross product points along $+\mathbf{e}_3$. These coordinates depend only on $a$, $b$, $c$, so they are the same for $\mathbf{X}$ and $\mathbf{Y}$. Let $F_X$ and $F_Y$ be the frame matrices, with the frame vectors as columns. Both are rotations, so $R = F_YF_X^{\mathsf T} \in SO(3)$, and $R(\mathbf{X}_i - \mathbf{X}_1) = \mathbf{Y}_i - \mathbf{Y}_1$ for each $i$. With $\mathbf{t} = \mathbf{Y}_1 - R\mathbf{X}_1$ we get $R\mathbf{X}_i + \mathbf{t} = \mathbf{Y}_i$. The motion is unique, because a rigid motion is fixed by its action on three points that are not collinear: the difference of two such motions fixes $\mathbf{X}_2 - \mathbf{X}_1$, $\mathbf{X}_3 - \mathbf{X}_1$ and their cross product, which span $\mathbb{R}^3$. $\square$

**Lemma 2 (reduction to one unknown).** Let $s_1, s_2, s_3 > 0$, and put $u = s_2/s_1$ and $v = s_3/s_1$. Then (1) holds if and only if
$$s_1^2 = \frac{b^2}{Q(v)}, \qquad \text{(A)}\;\; u^2 - 2u\cos\gamma + 1 - \frac{c^2}{b^2}Q(v) = 0, \qquad \text{(B)}\;\; u^2 - 2uv\cos\alpha + v^2 - \frac{a^2}{b^2}Q(v) = 0 .$$
Moreover, for all real $u$ and $v$, $\text{(A)} - \text{(B)} = N(v) - uD(v)$, where (A) and (B) stand for their left sides.

*Proof.* The rays $\mathbf{f}_1$ and $\mathbf{f}_3$ are distinct unit vectors with positive third entries, so $|\cos\beta| < 1$, and $Q(v) = (v - \cos\beta)^2 + 1 - \cos^2\beta > 0$. Substitute $s_2 = us_1$ and $s_3 = vs_1$ in (1). The second equation becomes $s_1^2Q(v) = b^2$. The third becomes $s_1^2(u^2 - 2u\cos\gamma + 1) = c^2$, and after division by $s_1^2 = b^2/Q$ it is (A). The first becomes $s_1^2(u^2 - 2uv\cos\alpha + v^2) = a^2$, which is (B) in the same way. The steps can be reversed. For the last statement,
$$\text{(A)} - \text{(B)} = 2u(v\cos\alpha - \cos\gamma) + 1 - v^2 + \frac{a^2 - c^2}{b^2}Q(v) = -uD(v) + N(v),$$
since $1 - v^2 + p(v^2 - 2v\cos\beta + 1) = N(v)$. $\square$

**Lemma 3 (the quartic).** If $u$ and $v$ satisfy (A) and (B), then $G(v) = 0$. If $G(v) = 0$ and $D(v) \ne 0$, then $u = N(v)/D(v)$ is the only $u$ with (A) and (B). If $G(v) = 0$ and $D(v) = 0$, then $N(v) = 0$, and the $u$ with (A) and (B) are exactly the real roots of (A).

*Proof.* By Lemma 2, (A) and (B) give $uD = N$. Multiply (A) by $D^2$ and replace $uD$ by $N$: the result is $N^2 - 2\cos\gamma\,ND + (1 - \frac{c^2}{b^2}Q)D^2 = G(v) = 0$. If $D(v) \ne 0$, (B) forces $u = N/D$, and then $D^2 \cdot \text{(A)} = G(v) = 0$, so (A) holds, and (B) holds because $\text{(A)} - \text{(B)} = N - uD = 0$. If $D(v) = 0$, then $G(v) = N(v)^2$, so $N(v) = 0$, and $\text{(A)} - \text{(B)} = 0$ for every $u$: the two equations are the same, and their solutions are the roots of (A). $\square$

**Proof of part (a).** Take an output pose. It comes from a root $v > 0$ of $G$ (line L5) and a $u > 0$ (line L8). If $D(v) \ne 0$, line L6 sets $u = N/D$, and Lemma 3 gives (A) and (B). If $D(v) = 0$, line L7 takes the roots $\cos\gamma \pm \sqrt{\cos^2\gamma - 1 + \frac{c^2}{b^2}Q(v)}$ of (A), and Lemma 3 again gives (A) and (B). Line L9 sets $s_1 = b/\sqrt{Q(v)} > 0$, $s_2 = us_1 > 0$ and $s_3 = vs_1 > 0$, so (1) holds by Lemma 2, and the check of (1) in line L9 passes in exact arithmetic. By Lemma 1, line L11 returns a valid pose. $\square$

**Proof of part (b).** Take a valid pose with distances $s_i > 0$, and put $u = s_2/s_1 > 0$ and $v = s_3/s_1 > 0$. By Lemma 1 and Lemma 2, (A) and (B) hold, so $G(v) = 0$ by Lemma 3, and line L5 meets this $v$. If $D(v) \ne 0$, line L6 finds this same $u$ by Lemma 3. If $D(v) = 0$, this $u$ is a root of (A), so it is one of the values of line L7. Then lines L9 to L11 rebuild the same $s_i$ and, by the uniqueness in Lemma 1, the same pose. Line L12 drops a pose only if it equals one already stored, so the pose is in the output. $\square$

**Proof of part (c).** By Lemma 1 a valid pose is fixed by $(s_1, s_2, s_3)$, and by Lemma 2 these are fixed by $(u, v)$. So we count the pairs $(u, v)$ with (A) and (B). $G$ has degree at most 4 and is not zero, so it has at most four roots, counted with multiplicity. A root with $D(v) \ne 0$ carries one pair. A root $v_0$ with $D(v_0) = 0$ carries at most two pairs, the two roots of (A). But then $N(v_0) = 0$ too, and each of the three terms of $G$ has a factor of the form $N^2$, $ND$ or $D^2$, all of which vanish to order at least 2 at $v_0$, so $v_0$ is a root of $G$ of multiplicity at least 2. In both cases the number of pairs at a root is at most its multiplicity, so there are at most four pairs. $\blacksquare$

**Remark (floating point).** In floating point, a root of $G$ near a common root of $N$ and $D$ can have $D(v)$ small but not zero. Then $N/D$ is a quotient of two rounding errors and does not satisfy (A) and (B). The check of (1) in line L9, with a relative tolerance of $10^{-3}$, rejects such a value. This tolerance is a heuristic, not a theorem. A true root near a double root of $G$ loses about half of its digits, and on random scenes its relative residual is about $10^{-5}$; the false values of this kind miss by more than $0.1$.

**Remark (the zero polynomial).** $G$ is the zero polynomial when the problem has infinitely many solutions, for example when the camera center lies on the circle through the three points, in their own plane. Every point of the same arc of that circle sees the three points under the same angles, so each one gives a valid pose. The solver is not meant for this case.
