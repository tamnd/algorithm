---
title: The quaternion method returns a rotation of least RMSD
proves: [correctness]
status: full
---

We use the notation of the page. The input is $x_1, \ldots, x_N$ and $y_1, \ldots, y_N$ in $\mathbb{R}^3$ with $N \ge 1$, $E(R, t) = \sum_i |R x_i + t - y_i|^2$, $a_i = x_i - \bar x$, $b_i = y_i - \bar y$, $G_A = \sum_i |a_i|^2$, $G_B = \sum_i |b_i|^2$ and $S = \sum_i a_i b_i^{\mathsf T}$ with entries $S_{rc}$, $r, c \in \{x, y, z\}$. For $q = (w, x, y, z)$ the matrix $R(q)$ is

$$R(q) = \begin{pmatrix} w^2 + x^2 - y^2 - z^2 & 2(xy - wz) & 2(xz + wy) \\ 2(xy + wz) & w^2 - x^2 + y^2 - z^2 & 2(yz - wx) \\ 2(xz - wy) & 2(yz + wx) & w^2 - x^2 - y^2 + z^2 \end{pmatrix}.$$

**Claim.** QUATERNION-SUPERPOSITION$(X, Y)$ returns $R \in SO(3)$ and $t$ with $E(R, t) = \min_{R' \in SO(3), t'} E(R', t')$, and the value of line L7 is $\sqrt{E(R, t)/N}$.

**Fact A (unit quaternions and rotations).** If $|q| = 1$, write $q = (\cos\frac{\theta}{2}, \sin\frac{\theta}{2}\, n)$ with $|n| = 1$. Then $R(q)$ is the rotation by the angle $\theta$ about the axis $n$ (the Euler-Rodrigues formula), so $R(q) \in SO(3)$. By Euler's rotation theorem each $R' \in SO(3)$ is a rotation by some angle about some axis, so $R' = R(q)$ for some unit $q$. So $q \mapsto R(q)$ maps the unit sphere in $\mathbb{R}^4$ onto $SO(3)$.

**Lemma 1 (translation).** For a fixed $R \in SO(3)$, $E(R, t)$ is smallest exactly at $t = \bar y - R\bar x$, and then $E = G_A + G_B - 2\operatorname{tr}(RS)$.

*Proof.* Write $R x_i + t - y_i = (R a_i - b_i) + c$ with $c = R\bar x + t - \bar y$. Since $\sum_i a_i = \sum_i b_i = 0$, the cross term vanishes, so $E = \sum_i |R a_i - b_i|^2 + N|c|^2$, smallest exactly at $c = 0$. Since $R$ keeps lengths, $|R a_i - b_i|^2 = |a_i|^2 + |b_i|^2 - 2 b_i^{\mathsf T} R a_i$, and $\sum_i b_i^{\mathsf T} R a_i = \operatorname{tr}(R S)$. $\square$

**Lemma 2 (Horn's identity).** Let $N$ be the matrix of line L3. For each $q \in \mathbb{R}^4$, $q^{\mathsf T} N q = \operatorname{tr}(R(q)\, S)$.

*Proof.* Both sides are linear in $S$, so it is enough to compare the coefficient of each entry $S_{rc}$. On the right, $\operatorname{tr}(R S) = \sum_{r, c} R_{cr} S_{rc}$, so the coefficient of $S_{rc}$ is $R(q)_{cr}$. On the left, an entry $N_{jk}$ contributes $N_{jk} q_j q_k$, and the off-diagonal pairs $N_{jk} = N_{kj}$ contribute $2 N_{jk} q_j q_k$. Reading the coefficients off $N$:

- $S_{xx}$ appears in the diagonal with signs $+, +, -, -$, which gives $w^2 + x^2 - y^2 - z^2 = R_{xx}$. In the same way $S_{yy}$ gives $w^2 - x^2 + y^2 - z^2 = R_{yy}$ and $S_{zz}$ gives $w^2 - x^2 - y^2 + z^2 = R_{zz}$.
- $S_{xy}$ appears in $N_{wz} = S_{xy} - S_{yx}$ and in $N_{xy} = S_{xy} + S_{yx}$, which gives $2wz + 2xy = R_{yx}$. $S_{yx}$ gives $-2wz + 2xy = R_{xy}$.
- $S_{xz}$ appears in $N_{wy} = S_{zx} - S_{xz}$ and in $N_{xz} = S_{zx} + S_{xz}$, which gives $-2wy + 2xz = R_{zx}$. $S_{zx}$ gives $2wy + 2xz = R_{xz}$.
- $S_{yz}$ appears in $N_{wx} = S_{yz} - S_{zy}$ and in $N_{yz} = S_{yz} + S_{zy}$, which gives $2wx + 2yz = R_{zy}$. $S_{zy}$ gives $-2wx + 2yz = R_{yz}$.

Here the rows and columns of $N$ have the names $w, x, y, z$ in this order. All nine coefficients agree. $\square$

**Lemma 3 (the maximum).** $\max_{R' \in SO(3)} \operatorname{tr}(R' S) = \lambda_{\max}(N)$, and $R(q)$ attains it when $q$ is a unit eigenvector of $\lambda_{\max}(N)$.

*Proof.* By Fact A and Lemma 2, $\max_{R'} \operatorname{tr}(R'S) = \max_{|q| = 1} q^{\mathsf T} N q$. The matrix $N$ is real and symmetric, so it has an orthonormal basis of eigenvectors $e_1, \ldots, e_4$ with eigenvalues $\lambda_1 \ge \cdots \ge \lambda_4$. For $q = \sum_k c_k e_k$ with $\sum_k c_k^2 = 1$, $q^{\mathsf T} N q = \sum_k \lambda_k c_k^2 \le \lambda_1$, with equality at $q = e_1$. $\square$

**Proof of the claim.** Lines L1 and L2 compute $\bar x$, $\bar y$, $G_A$, $G_B$ and $S$, line L3 forms $N$, and line L4 returns $\lambda_{\max}$ and a unit eigenvector $q$ (replacing $q$ with $-q$ does not change $R(q)$, since $R$ is quadratic in $q$). By Lemma 3 and Fact A, $R = R(q)$ of line L5 is in $SO(3)$ and maximizes $\operatorname{tr}(R'S)$. For each $R' \in SO(3)$ and each $t'$, Lemma 1 gives $E(R', t') \ge G_A + G_B - 2\operatorname{tr}(R'S) \ge G_A + G_B - 2\lambda_{\max}$. Line L6 sets $t = \bar y - R\bar x$, so by Lemma 1, $E(R, t) = G_A + G_B - 2\lambda_{\max}$, which is the minimum. This value is at least 0, so line L7 returns $\sqrt{E(R, t)/N}$; the $\max$ with 0 only removes rounding errors. $\blacksquare$

**Lemma 4 (the QCP iteration).** Let $P(\lambda) = \det(\lambda I - N)$ and $\lambda_0 = (G_A + G_B)/2$. Newton's method $\lambda_{k+1} = \lambda_k - P(\lambda_k)/P'(\lambda_k)$ from $\lambda_0$ gives a sequence that decreases to $\lambda_{\max}$, or stops at it.

*Proof.* The value $E_{\min} = G_A + G_B - 2\lambda_{\max}$ is a sum of squares, so $\lambda_0 \ge \lambda_{\max}$. All four roots of $P$ are real, because $N$ is symmetric, and $\lambda_{\max}$ is the largest. By Rolle's theorem the roots of $P'$ and $P''$ are real and at most $\lambda_{\max}$. So on $[\lambda_{\max}, \infty)$, $P \ge 0$, $P' > 0$ to the right of $\lambda_{\max}$, and $P'' \ge 0$. If $\lambda_k > \lambda_{\max}$, then $P(\lambda_k) > 0$ and $P'(\lambda_k) > 0$, so $\lambda_{k+1} < \lambda_k$. Convexity of $P$ on this interval gives $0 = P(\lambda_{\max}) \ge P(\lambda_k) + P'(\lambda_k)(\lambda_{\max} - \lambda_k)$, that is $\lambda_{k+1} \ge \lambda_{\max}$. A decreasing sequence that is bounded below converges, and its limit $\mu$ satisfies $P(\mu) = 0$ with $\mu \ge \lambda_{\max}$, so $\mu = \lambda_{\max}$. $\square$
