---
title: The normalized DLT recovers the camera matrix from exact matches and minimizes the algebraic error
proves: [correctness]
status: full
---

We use the notation of the page. The input is $n \ge 6$ pairs $X_i \leftrightarrow x_i$, where $X_i \in \mathbb{R}^3$ and $x_i \in \mathbb{R}^2$. We write $\mathbf{X}_i = (X_i, 1)$ and $\mathbf{x}_i = (x_i, 1)$ for the homogeneous vectors, $p \in \mathbb{R}^{12}$ for the rows of a $3 \times 4$ matrix $P$ stacked in order, and $A$ for the $2n \times 12$ matrix of lines L5 and L6.

**Claim.** (a) For every $p$, $A p$ is the vector of the two rows of L5 and L6 at each pair, and the output $p$ of line L7 minimizes $\|A p\|$ over the unit vectors. (b) If the data are exact, $\mathbf{x}_i \sim P_0 \mathbf{X}_i$ for a finite camera $P_0$, and the null space of $A$ has dimension 1, then the algorithm returns $P_0 / \|P_0\|_F$ with the sign that makes $\det M > 0$, where $M$ is the left $3 \times 3$ block. (c) The similarities of lines L2 to L4 and L9 do not change the answer in (b).

**Lemma 1 (the rows).** Let $\mathbf{x} = (x, y, w)$ with $w \ne 0$, and let $q = P \mathbf{X}$. The two rows of L5 and L6 at this pair give $A_i p = (y q_3 - w q_2, \; w q_1 - x q_3)$. Both are 0 if and only if $q$ is a multiple of $\mathbf{x}$ (the multiple may be 0).

*Proof.* The row $(0^{\mathsf T}, -w \mathbf{X}^{\mathsf T}, y \mathbf{X}^{\mathsf T})$ times $p$ is $-w\, p^{2\mathsf T} \mathbf{X} + y\, p^{3\mathsf T} \mathbf{X} = y q_3 - w q_2$, where $p^{k\mathsf T}$ is row $k$ of $P$. The other row gives $w q_1 - x q_3$ in the same way. These are the first two entries of $\mathbf{x} \times q$, up to sign. If $q = c\,\mathbf{x}$, both are 0. Conversely, if both are 0, then $q_2 = (y / w) q_3$ and $q_1 = (x / w) q_3$, so $q = (q_3 / w)\,\mathbf{x}$. $\square$

The third entry of $\mathbf{x} \times q$, $x q_2 - y q_1$, adds nothing when $w \ne 0$, which is why two rows per pair are enough. After line L4, $w = 1$ times a positive scale, so $w \ne 0$ always holds.

**Proof of (a).** The first part is Lemma 1. The second part is a property of the [singular value decomposition](/singular-value-decomposition/): if $A = U S V^{\mathsf T}$ with singular values $s_1 \ge \dots \ge s_{12} \ge 0$ (padded with zeros if $2n < 12$, which line L1 excludes), then for a unit vector $p$, $\|A p\|^2 = \sum_k s_k^2 (v_k^{\mathsf T} p)^2 \ge s_{12}^2 \sum_k (v_k^{\mathsf T} p)^2 = s_{12}^2$, with equality at $p = v_{12}$. Line L7 returns $v_{12}$. $\square$

**Proof of (b), without the similarities.** Let $p_0$ be the vector of $P_0$. By Lemma 1 and $\mathbf{x}_i \sim P_0 \mathbf{X}_i$, $A p_0 = 0$. The null space of $A$ has dimension 1, so it is spanned by $p_0$, and $s_{12} = 0 < s_{11}$. By (a), line L7 returns a unit vector $p$ with $A p = 0$, so $p = \pm p_0 / \|p_0\|$. Line L8 reshapes it into $\pm P_0 / \|P_0\|_F$, and line L10 keeps the norm 1 and picks the sign with $\det M > 0$. That is the claim. $\square$

**Proof of (c).** Let $T$ be the $3 \times 3$ similarity of line L2 and $U$ the $4 \times 4$ similarity of line L3. Both are invertible, and $T$ has last row $(0, 0, 1)$, so $T \mathbf{x}_i$ has last entry 1. From $\mathbf{x}_i \sim P_0 \mathbf{X}_i$ we get
$$T \mathbf{x}_i \sim (T P_0 U^{-1})(U \mathbf{X}_i).$$
So the normalized data are exact data for the camera $\tilde P_0 = T P_0 U^{-1}$, and this camera is finite. Indeed, $U = \begin{pmatrix} s_U I & -s_U c \\ 0^{\mathsf T} & 1 \end{pmatrix}$ with $s_U > 0$, so the left $3 \times 3$ block of $T P_0 U^{-1}$ is $T M_0 / s_U$, and its determinant $\det T \det M_0 / s_U^3$ is not zero and has the sign of $\det M_0$, because $\det T = s_T^2 > 0$. The map $P \mapsto T P U^{-1}$ is a linear bijection of the $3 \times 4$ matrices, so the null space of the normalized $A$ is again one-dimensional: it is the image of the null space for the raw data under this bijection, because by Lemma 1 both null spaces are the sets of matrices that send each $\mathbf{X}_i$ (or $U \mathbf{X}_i$) to a multiple of $\mathbf{x}_i$ (or $T \mathbf{x}_i$). By (b), line L7 returns $\pm \tilde P_0$ up to scale, and line L9 returns $T^{-1} (\pm c \tilde P_0) U = \pm c P_0$ with $c > 0$. Line L10 then gives $P_0 / \|P_0\|_F$ with $\det M > 0$, since $\det(c M_0)$ has the sign of $\det M_0$ and the sign rule picks the right one. $\square$

**Remark (when the null space is larger).** If all $X_i$ lie on one plane $\mathbf{n}^{\mathsf T} \mathbf{X} = 0$, then every $P_0 + a \mathbf{n}^{\mathsf T}$ with $a \in \mathbb{R}^3$ also sends each $\mathbf{X}_i$ to $P_0 \mathbf{X}_i$, so the null space has dimension at least 4 and line L7 returns an arbitrary element of it. The other critical configurations, a twisted cubic through the camera center and the points, or a plane plus a line through the center, are in HZ section 22.1. With noise, $s_{12} > 0$ and the answer of line L7 is the minimizer of the algebraic error of (a), not of the reprojection error.
