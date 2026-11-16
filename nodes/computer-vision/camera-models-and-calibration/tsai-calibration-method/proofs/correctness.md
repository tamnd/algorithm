---
title: Stage one of Tsai's method is exact under radial distortion, and the linear stage is exact without it
proves: [correctness]
status: full
---

We use the notation and the camera model of the page. The true parameters are $R$ with rows $r_1, r_2, r_3$, $T = (T_x, T_y, T_z)$, $f > 0$, $s_x > 0$ and $\kappa_1$, and the data are exact. We assume that every point is in front of the camera ($z_c > 0$) and that $1 + \kappa_1 r_d^2 > 0$ at every image point, so that distortion does not flip a point through the center.

**Claim.** (a) If $T_y \ne 0$ and the $n \times 7$ matrix $A$ of line L2 has rank 7, lines L2 to L6 return the true $R$, $T_x$, $T_y$ and $s_x$, for every value of $f$, $T_z$ and $\kappa_1$. (b) If moreover $\kappa_1 = 0$ and the $n \times 2$ matrix of line L7 has rank 2, line L7 returns the true $f$ and $T_z$. (c) Line L8 never increases its cost.

**Lemma 1 (radial alignment).** For every point, $x'_i\, y_{c,i} = s_x\, y'_i\, x_{c,i}$, where $x_{c,i} = r_1 \cdot X_i + T_x$ and $y_{c,i} = r_2 \cdot X_i + T_y$.

*Proof.* Let $g = 1 + \kappa_1 r_d^2 > 0$. The model gives $X_d = f x_c / (g z_c)$ and $Y_d = f y_c / (g z_c)$, so $X_d y_c = Y_d x_c$. With $x' = s_x X_d$ and $y' = Y_d$, this is $x' y_c = s_x y' x_c$. $\square$

The lemma does not involve $f$, $T_z$ or $\kappa_1$. Dividing it by $T_y$ and moving the terms gives
$$x'_i = y'_i \frac{s_x r_1}{T_y} \cdot X_i + y'_i \frac{s_x T_x}{T_y} - x'_i \frac{r_2}{T_y} \cdot X_i,$$
which is row $i$ of line L2 applied to $a^\ast = (s_x r_1 / T_y, \; s_x T_x / T_y, \; r_2 / T_y)$. So $A a^\ast = x'$.

**Proof of (a).** Since $A a^\ast = x'$ and $A$ has rank 7, $a^\ast$ is the unique least squares solution, and line L2 returns it. Since $\|r_2\| = 1$, $\|(a_5, a_6, a_7)\| = 1 / |T_y|$, and since $\|r_1\| = 1$, $\|(a_1, a_2, a_3)\| = s_x / |T_y|$. So line L3 returns the true $|T_y|$ and $s_x$. Let $\epsilon = \operatorname{sign}(T_y)$. Line L4 sets $T_y \leftarrow |T_y| = \epsilon T_y$ and
$$r_1 \leftarrow |T_y| \frac{s_x r_1}{T_y s_x} = \epsilon r_1, \qquad r_2 \leftarrow |T_y| \frac{r_2}{T_y} = \epsilon r_2, \qquad T_x \leftarrow |T_y| \frac{s_x T_x}{T_y s_x} = \epsilon T_x.$$
So after line L4, the four quantities are the true ones times the same $\epsilon$. For the point $k$ farthest from the center, line L5 computes $\epsilon x_{c,k}$ and $\epsilon y_{c,k}$ with the true $x_{c,k}, y_{c,k}$. By the proof of Lemma 1, $x'_k = s_x f x_{c,k} / (g z_{c,k})$ and $y'_k = f y_{c,k} / (g z_{c,k})$ with $s_x, f, g, z_{c,k} > 0$, so $x'_k$ has the sign of $x_{c,k}$ and $y'_k$ that of $y_{c,k}$. The point $k$ has $(x'_k, y'_k) \ne 0$, because it is the farthest from the center and not all points are at the center (else $A$ would be 0). So at least one of $x'_k x_{c,k}$ and $y'_k y_{c,k}$ is positive. If $\epsilon = +1$, both products in line L5 are $\ge 0$ and nothing changes. If $\epsilon = -1$, both are $\le 0$ and at least one is negative, so line L5 negates all four quantities. In both cases the result is the true $T_y$, $T_x$, $r_1$ and $r_2$. Then $r_1 \times r_2 = r_3$, because the rows of a rotation form a right handed orthonormal basis, so line L6 starts from the true $R$, and the nearest rotation to a rotation $Q$ is $Q$ itself. $\square$

**Proof of (b).** With $\kappa_1 = 0$, $Y_{d,i} = f y_{c,i} / z_{c,i}$ and $z_{c,i} = w_i + T_z$ with $w_i = r_3 \cdot X_i$. So $y'_i (w_i + T_z) = f y_{c,i}$, that is, $f y_{c,i} - y'_i T_z = y'_i w_i$. By (a), the $y_{c,i}$ and $w_i$ of line L7 are the true ones, so the true $(f, T_z)$ solves the system exactly. With rank 2 it is the unique least squares solution, and line L7 returns it. $\square$

**Proof of (c).** In line L8 a step is accepted only if the new cost is strictly lower than the current one; otherwise the damping grows and the step is tried again, and the loop ends when no step is accepted. So the accepted costs strictly decrease. $\square$

**Remark (with distortion).** If $\kappa_1 \ne 0$, line L7 is biased, because it treats $Y_d$ as $Y_u$. The cost of line L8 is 0 at the true $(f, T_z, \kappa_1)$, since $Y_d (1 + \kappa_1 r_d^2) = Y_u = f y_c / z_c$ there; so with exact data the true values are a global minimizer, and Levenberg-Marquardt reaches them from the linear start when that start is close enough. This last part is a heuristic, not a theorem: Levenberg-Marquardt only guarantees a local minimum.

**Remark (rank).** If all points lie on a plane $\mathbf{m} \cdot X = d$, the first four columns $c_1, \dots, c_4$ of $A$ are the entries of $y'_i (X_i, 1)$, so $m_1 c_1 + m_2 c_2 + m_3 c_3 - d\, c_4 = 0$, and $A$ has rank at most 6; this is why the general form needs points that are not coplanar. If $T_y = 0$, the division that defines $a^\ast$ is not possible, and the system has no solution of this form.
