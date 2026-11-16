---
title: Correctness of SURF
proves: [correctness]
status: full
---

Let $I$ be an image with $W$ columns and $H$ rows, extended by 0 outside. The integral image is $S(u, v) = \sum_{u' < u, v' < v} I(u', v')$ for $0 \le u \le W$ and $0 \le v \le H$. For a box $R = [u_0, u_1) \times [v_0, v_1)$ write $\Sigma(R)$ for the sum of $I$ over $R$.

**Lemma 1 (box sums).** For $0 \le u_0 \le u_1 \le W$ and $0 \le v_0 \le v_1 \le H$, $\Sigma(R) = S(u_1, v_1) - S(u_0, v_1) - S(u_1, v_0) + S(u_0, v_0)$. For any box, $\Sigma(R)$ equals the same formula applied to $R$ clipped to the image.

*Proof.* The construction gives $S(u + 1, v + 1) = S(u + 1, v) + \sum_{u' \le u} I(u', v)$, so by induction on $v$, $S$ is the sum over $u' < u$, $v' < v$. In the formula, a pixel with $u' < u_0$ or $v' < v_0$ is counted in $S(u_1, v_1)$ and in exactly one or in all three of the other terms with signs that cancel: if $u' < u_0$ and $v_0 \le v' < v_1$ it is in $S(u_1, v_1)$ and $S(u_0, v_1)$; if $u' < u_0$ and $v' < v_0$ it is in all four, with the signs $+, -, -, +$. The case $v' < v_0$, $u_0 \le u' < u_1$ is symmetric. A pixel in $R$ is only in $S(u_1, v_1)$. So the formula is $\Sigma(R)$. Pixels outside the image are 0, so clipping $R$ to the image does not change $\Sigma(R)$. $\square$

**Lemma 2 (box filters).** For an odd size $L = 3 l_0$, the values computed in line L2 equal the correlation of $I$ at $(u, v)$ with the masks defined on the page, divided by $L^2$.

*Proof.* For $D_{uu}$, let $A$ be the box of all three lobes, $u - \frac{L - 1}{2} \le u' \le u + \frac{L - 1}{2}$ and $|v' - v| \le l_0 - 1$, and $M$ the middle lobe, $|u' - u| \le \frac{l_0 - 1}{2}$ with the same rows. Since $L = 3 l_0$, $A$ is the union of three lobes of width $l_0$ each, and $M$ is the middle one. So $\Sigma(A) - 3 \Sigma(M)$ gives each pixel of the outer lobes the weight $+1$ and each pixel of $M$ the weight $1 - 3 = -2$, which is the mask. $D_{vv}$ is the same with $u$ and $v$ swapped. $D_{uv}$ is the sum of four boxes of $l_0 \times l_0$ pixels with the weights $+1, -1, -1, +1$, which is the mask by definition. By Lemma 1 each box sum is correct, and the code divides by $L^2$. $\square$

**Lemma 3 (transpose).** Let $I^T(u, v) = I(v, u)$ be the transposed image. Then $D_{uu}[I^T](v, u) = D_{vv}[I](u, v)$, $D_{vv}[I^T](v, u) = D_{uu}[I](u, v)$ and $D_{uv}[I^T](v, u) = D_{uv}[I](u, v)$, so the determinant maps satisfy $d[I^T](v, u, L) = d[I](u, v, L)$.

*Proof.* The mask of $D_{vv}$ is the transpose of the mask of $D_{uu}$, and the mask of $D_{uv}$ is its own transpose: the weight of the offset $(\delta_u, \delta_v)$ is $+1$ when $\delta_u \delta_v > 0$ and $-1$ when $\delta_u \delta_v < 0$, which is symmetric in the two offsets. Correlating $I^T$ with a mask at $(v, u)$ equals correlating $I$ with the transposed mask at $(u, v)$. By Lemma 2 the computed values are the correlations. The determinant $D_{uu} D_{vv} - (0.9 D_{uv})^2$ is symmetric in $D_{uu}$ and $D_{vv}$. $\square$

The integer box sums are exact, and the same division by $L^2$ is applied, so the equality holds exactly in floating point too.

**Lemma 4 (local maxima).** Line L4 keeps a sample $(u, v, L)$ of a middle layer if and only if $d(u, v, L)$ is larger than the threshold and larger than each of its 26 neighbors in the $3 \times 3 \times 3$ block of samples of its octave.

*Proof.* The code skips a sample if $d$ is at most the threshold, or if some neighbor has $d' \ge d$. So it keeps exactly the samples with $d$ above the threshold and $d > d'$ for all 26 neighbors. The middle layers and the inner samples have all 26 neighbors in the octave, so no neighbor is missing. The quadratic fit only moves the kept point and does not add or remove points. $\square$

**Lemma 5 (Haar responses).** Let $dx$ and $dy$ be the Haar responses of size $h$ at a point whose boxes lie inside the image. Adding a constant $a$ to $I$ does not change them, and multiplying $I$ by $c > 0$ multiplies them by $c$. On the ramp $I(u, v) = \alpha u + \beta v$, $(dx, dy) = \kappa (\alpha, \beta)$ with $\kappa = h^3 / 4 > 0$, the same for every point.

*Proof.* Each response is the difference of two boxes with the same number of pixels, so a constant cancels, and both terms scale with $c$. On the ramp, let $r = h / 2$. The response $dx$ pairs each pixel $(u', v')$ of the left half with the pixel $(u' + r, v')$ of the right half. Each pair differs by $\alpha r$, and there are $r$ pairs in each of the $h$ rows, so $dx = \alpha r \cdot r h = \alpha h^3 / 4$. In the same way $dy = \beta h^3 / 4$. $\square$

**Lemma 6 (orientation on a ramp).** If all Haar responses within the radius $6s$ lie inside the image and $(\alpha, \beta) \ne 0$, line L6 returns $\theta = \operatorname{atan2}(\beta, \alpha)$.

*Proof.* By Lemma 5 each weighted response is $g_k \kappa (\alpha, \beta)$ with $g_k > 0$, so all of them have the angle $\operatorname{atan2}(\beta, \alpha)$. Every window centered at the angle of a response contains all responses, so every window sum is a positive multiple of $(\alpha, \beta)$, and the longest one has this direction too. $\square$

**Theorem.** SURF returns as keypoints exactly the samples of the middle layers that are strict local maxima of the box determinant above the threshold, refined by the quadratic fit. The determinant map of the transposed image is the transposed map. For a keypoint whose descriptor window lies inside the image, the descriptor has length 1 (unless all its responses are 0) and does not change when a constant is added to the image or when the image is multiplied by $c > 0$.

*Proof.* Lines L1 to L3 compute the determinant by Lemmas 1 and 2, and line L4 keeps the maxima by Lemma 4. Lemma 3 gives the transpose property. In line L7 each turned response is a linear function of $(dx, dy)$, so by Lemma 5 adding a constant keeps all 64 sums and multiplying by $c$ multiplies all of them by $c$; the orientation of line L6 depends only on the directions and the relative lengths of the sums, so it does not change either. Line L8 divides by the length, which gives length 1 and removes the factor $c$. $\square$
