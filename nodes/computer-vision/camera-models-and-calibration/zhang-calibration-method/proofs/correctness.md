---
title: The closed form of Zhang's method recovers K and the poses from exact views of a plane, and the refinement never increases the cost
proves: [correctness]
status: full
---

We use the notation of the page. $K = \begin{pmatrix} \alpha & \gamma & u_0 \\ 0 & \beta & v_0 \\ 0 & 0 & 1 \end{pmatrix}$ with $\alpha, \beta > 0$. View $j$ has the pose $(R_j, t_j)$ with columns $R_j = [r_1 \; r_2 \; r_3]$ and $t_{j,z} > 0$ for the points of the pattern. We write $B^\ast = K^{-\mathsf T} K^{-1}$ and $b^\ast$ for its six entries in the order $(B_{11}, B_{12}, B_{22}, B_{13}, B_{23}, B_{33})$.

**Claim.** (a) If the pixels are exact, there is no distortion, the model points include 4 points with no three on one line, and the matrix $V$ of lines L2 and L3 has rank 5, then line L5 returns the true $K$ and line L6 returns the true poses. (b) Line L8 never increases the reprojection error.

We assume, as the method does, that the camera center is not on the plane of the pattern in any view.

**Lemma 1 (homography of a view).** For a model point $(X, Y)$, the pixel is $u \sim H (X, Y, 1)^{\mathsf T}$ with $H = K [r_1 \; r_2 \; t]$, and $H$ is invertible.

*Proof.* The point is $(X, Y, 0)$ in the pattern frame, so $K (R (X, Y, 0)^{\mathsf T} + t) = K (X r_1 + Y r_2 + t) = K [r_1 \; r_2 \; t] (X, Y, 1)^{\mathsf T}$. Suppose $[r_1 \; r_2 \; t] c = 0$ for some $c \ne 0$. Then $c_3 \ne 0$, because $r_1$ and $r_2$ are independent, and the point $(c_1 / c_3, c_2 / c_3, 0)$ of the plane has camera coordinates $c_1 / c_3\, r_1 + c_2 / c_3\, r_2 + t = 0$. So the camera center lies on the plane, which we excluded. Hence $[r_1 \; r_2 \; t]$ and $H$ are invertible. $\square$

By the DLT for homographies, 4 exact correspondences with no three on one line determine $H$ up to a nonzero scale, so line L1 returns $H_j = \lambda_j K [r_1 \; r_2 \; t_j]$ with $\lambda_j \ne 0$.

**Lemma 2 (the two equations).** For every view, $h_1^{\mathsf T} B^\ast h_2 = 0$ and $h_1^{\mathsf T} B^\ast h_1 = h_2^{\mathsf T} B^\ast h_2$. For every symmetric $B$ with entry vector $b$ and every pair of vectors $h_i, h_j$, $h_i^{\mathsf T} B h_j = v_{ij}^{\mathsf T} b$.

*Proof.* $K^{-1} h_1 = \lambda_j r_1$ and $K^{-1} h_2 = \lambda_j r_2$, so $h_1^{\mathsf T} B^\ast h_2 = \lambda_j^2 r_1^{\mathsf T} r_2 = 0$ and $h_k^{\mathsf T} B^\ast h_k = \lambda_j^2 \|r_k\|^2 = \lambda_j^2$ for $k = 1, 2$. For the second part, expand $h_i^{\mathsf T} B h_j = \sum_{k, l} B_{kl} h_{ik} h_{jl}$; the diagonal terms give $B_{11} h_{i1} h_{j1}$, $B_{22} h_{i2} h_{j2}$, $B_{33} h_{i3} h_{j3}$, and each off-diagonal pair $B_{kl} = B_{lk}$ gives $B_{kl} (h_{ik} h_{jl} + h_{il} h_{jk})$. These are the six entries of $v_{ij}$. $\square$

So the true $b^\ast$ satisfies $V b^\ast = 0$. The row $(0, 1, 0, 0, 0, 0)$ of line L3 says $B_{12} = 0$, and $B^\ast_{12} = -\gamma / (\alpha^2 \beta) = 0$ when the skew $\gamma$ is 0, so it holds too. If $V$ has rank 5, its null space is spanned by $b^\ast$, and line L4 returns $b = \mu\, b^\ast$ for some $\mu \ne 0$, by the minimum property of the smallest right singular vector.

**Lemma 3 (the closed form).** If $B = \mu K^{-\mathsf T} K^{-1}$ with $\mu \ne 0$, the formulas of line L5 return $K$.

*Proof.* $K^{-1} = \begin{pmatrix} 1/\alpha & -\gamma/(\alpha\beta) & (\gamma v_0 - u_0 \beta)/(\alpha\beta) \\ 0 & 1/\beta & -v_0/\beta \\ 0 & 0 & 1 \end{pmatrix}$. Write $e = \gamma v_0 - u_0 \beta$. Multiplying out $\mu K^{-\mathsf T} K^{-1}$ gives
$$B_{11} = \frac{\mu}{\alpha^2}, \quad B_{12} = -\frac{\mu \gamma}{\alpha^2 \beta}, \quad B_{22} = \mu \Big(\frac{\gamma^2}{\alpha^2 \beta^2} + \frac{1}{\beta^2}\Big), \quad B_{13} = \frac{\mu e}{\alpha^2 \beta},$$
$$B_{23} = -\mu \Big(\frac{\gamma e}{\alpha^2 \beta^2} + \frac{v_0}{\beta^2}\Big), \quad B_{33} = \mu \Big(\frac{e^2}{\alpha^2 \beta^2} + \frac{v_0^2}{\beta^2} + 1\Big).$$
Then $B_{11} B_{22} - B_{12}^2 = \mu^2 / (\alpha^2 \beta^2)$, which is positive, and
$$B_{12} B_{13} - B_{11} B_{23} = \mu^2 \Big(-\frac{\gamma e}{\alpha^4 \beta^2} + \frac{\gamma e}{\alpha^4 \beta^2} + \frac{v_0}{\alpha^2 \beta^2}\Big) = \frac{\mu^2 v_0}{\alpha^2 \beta^2}.$$
So the first formula gives $v_0$. Next, $B_{13}^2 / B_{11} = \mu e^2 / (\alpha^2 \beta^2)$ and $v_0 (B_{12} B_{13} - B_{11} B_{23}) / B_{11} = \mu v_0^2 / \beta^2$, so the formula for $\lambda$ gives $B_{33} - \mu e^2/(\alpha^2\beta^2) - \mu v_0^2/\beta^2 = \mu$. Then $\lambda / B_{11} = \alpha^2 > 0$, so the formula gives $\alpha$; $\lambda B_{11} / (B_{11} B_{22} - B_{12}^2) = \mu \cdot (\mu / \alpha^2) \cdot (\alpha^2 \beta^2 / \mu^2) = \beta^2$, so it gives $\beta$; $-B_{12} \alpha^2 \beta / \lambda = (\mu \gamma / (\alpha^2 \beta)) \cdot \alpha^2 \beta / \mu = \gamma$; and $\gamma v_0 / \beta - B_{13} \alpha^2 / \lambda = \gamma v_0 / \beta - e / \beta = u_0$. The sign of $\mu$ cancels in every step. $\square$

**Lemma 4 (the poses).** With the true $K$ and $H_j = \lambda_j K [r_1 \; r_2 \; t_j]$, line L6 returns $R_j$ and $t_j$.

*Proof.* $K^{-1} h_1 = \lambda_j r_1$ has norm $|\lambda_j|$, so $\mu = \pm 1 / |\lambda_j|$ gives $\mu K^{-1} h_1 = \pm r_1$, with the same sign $\epsilon = \pm 1$ for $r_2$ and $t_j$. The code picks the sign with a positive third entry of $\mu K^{-1} h_3 = \epsilon t_j$; since $t_{j,z} > 0$, this is $\epsilon = +1$. Then $r_3 = r_1 \times r_2$ is the third column of the rotation $R_j$, because the columns of a rotation form a right handed orthonormal basis. The matrix is already a rotation, and the nearest rotation to a rotation $Q$ is $Q$ itself ($Q = U S V^{\mathsf T}$ with $S = I$ gives $U V^{\mathsf T} = Q$). $\square$

**Proof of (a).** Lemmas 1 and 2 show $V b^\ast = 0$. With rank 5, line L4 returns a nonzero multiple of $b^\ast$. Lemma 3 shows that line L5 returns $K$, and Lemma 4 that line L6 returns the poses. $\square$

**Proof of (b).** In line L8, a step is accepted only if the new cost is strictly lower than the current one; otherwise the damping grows and the step is tried again, and the loop ends if no step is accepted. So the sequence of accepted costs is strictly decreasing, and the returned parameters have a cost no higher than the start. $\square$

**Remark (rank of V).** Lemma 2 depends on the plane only through $r_1$ and $r_2$, that is, through the orientation of the plane. Two views with the same $R_j$ give the same two rows up to scale, so pure translations of the pattern do not raise the rank of $V$. In general position, each view with a new orientation adds up to 2 to the rank, so 3 views reach rank 5 (and 2 views with the row of line L3). Finally, (b) does not say that line L8 finds the global minimum; with exact data, the start of (a) already has cost 0 when there is no distortion, and in the presence of distortion the start is close enough in practice, which is a heuristic, not a theorem.
