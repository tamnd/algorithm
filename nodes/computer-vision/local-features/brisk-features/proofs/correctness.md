---
title: Correctness of BRISK
proves: [correctness]
status: full
---

Pixels are $(u, v)$ with $u$ the column and $v$ the row. For a pixel $p$ of a layer, let $\delta_0, \dots, \delta_{15}$ be the differences $I(c_k) - I(p)$ for the 16 pixels $c_k$ of the circle of radius 3, in order around the circle. The point is a FAST 9-16 corner for the threshold $T$ when there is a start $j$ with $\delta_{j + k} > T$ for $k = 0, \dots, 8$, or with $-\delta_{j + k} > T$ for $k = 0, \dots, 8$, indices modulo 16.

**Lemma 1 (FAST score).** Let $s = \max(0, \max_j \min_{0 \le k \le 8} \delta_{j + k}, \max_j \min_{0 \le k \le 8} (-\delta_{j + k}))$. For every $T \ge 0$, the point is a corner for $T$ if and only if $T < s$.

*Proof.* If the point is a corner for $T$ with a bright run starting at $j$, then $\min_k \delta_{j + k} > T$, so $s > T$; a dark run is the same with $-\delta$. Conversely, if $T < s$, then $s > 0$, and $s$ equals $\min_k \delta_{j + k}$ or $\min_k (-\delta_{j + k})$ for some $j$. In the first case all nine $\delta_{j + k} \ge s > T$, which is a bright run; the second case gives a dark run. The code takes the minimum over the nine values of the doubled list $\delta_0, \dots, \delta_{15}, \delta_0, \dots, \delta_7$ starting at $j = 0, \dots, 15$, which are exactly the cyclic runs. $\square$

So $s$ is the largest threshold, in the sense of a supremum, for which the point is a corner, which is the FAST score that BRISK uses.

**Lemma 2 (selection).** A pixel $p$ of layer $k$ with score $s$ is returned by the detector if and only if $s > T$; every neighbor $q$ of $p$ in the layer has a score below $s$, or the same score and comes after $p$ in raster order; and the largest score in the $3 \times 3$ pixels of the layers $k - 1$ and $k + 1$ around the place of $p$ is at most $s$.

*Proof.* The code skips $p$ exactly when $s \le T$, or when some neighbor has a larger score or the same score and an earlier place in raster order (an offset $(\delta_v, \delta_u) < (0, 0)$ in the lexicographic order), or when the largest nearby score of an adjacent layer is larger than $s$. All other pixels inside the margin are returned. $\square$

Two neighbors with the same score cannot both be returned, since one of them comes first, so a plateau of equal scores gives at most one point per $3 \times 3$ neighborhood of the plateau's first pixel.

**Lemma 3 (the parabola).** Let $\ell_0 < \ell_1 < \ell_2$ be the log scales of the three layers and $s_0, s_1, s_2$ the scores with $s_1 > s_0$, $s_1 > s_2$ or with $s_1 \ge s_0, s_2$ and not both equal. Then the parabola through the three points is concave, and its vertex lies in $[\ell_0, \ell_2]$ before the clip, which the code computes as $\ell_1 - \frac{1}{2} N / D$ with $N = (\ell_1 - \ell_0)^2 (s_1 - s_2) - (\ell_1 - \ell_2)^2 (s_1 - s_0)$ and $D = (\ell_1 - \ell_0)(s_1 - s_2) - (\ell_1 - \ell_2)(s_1 - s_0)$.

*Proof.* $D = (\ell_1 - \ell_0)(s_1 - s_2) + (\ell_2 - \ell_1)(s_1 - s_0)$ is a sum of nonnegative terms, and it is positive when not both differences are 0. The vertex formula is the standard one for the parabola through three points: write the parabola as $s(\ell) = s_1 + \beta (\ell - \ell_1) + \gamma (\ell - \ell_1)^2$; the two equations at $\ell_0$ and $\ell_2$ give $\gamma = -D / ((\ell_1 - \ell_0)(\ell_2 - \ell_1)(\ell_2 - \ell_0)) < 0$, so the parabola is concave, and the vertex $\ell_1 - \beta / (2 \gamma)$ simplifies to $\ell_1 - \frac{1}{2} N / D$. Since the parabola is concave and $s(\ell_1) \ge s(\ell_0)$, the vertex is not left of the midpoint of $\ell_0$ and $\ell_1$; in the same way it is not right of the midpoint of $\ell_1$ and $\ell_2$. So it lies in $[\ell_0, \ell_2]$. $\square$

**Lemma 4 (gain).** If every pixel is multiplied by $c > 0$, the orientation and the descriptor do not change.

*Proof.* Each smoothed value is a weighted mean $\sum w_q I(q) / \sum w_q$ with weights that depend only on the positions, so it is multiplied by $c$. In line L4 each term of $g$ is a difference of two smoothed values times a vector that depends only on the pattern, so $g$ is multiplied by $c$, and $\operatorname{atan2}$ does not change. With the same $\alpha$, line L6 reads the same positions, and each comparison of line L7 compares two values both multiplied by $c > 0$, so each bit is the same. When $c$ is a power of 2, every floating point step is scaled exactly, so the equality also holds bit for bit in the code. $\square$

**Lemma 5 (ramp).** Suppose the smoothed values are exact on the ramp $I(u, v) = a u + b v$, that is, $I(p, \sigma) = a p_u + b p_v$ plus a constant. Then $g = M (a, b)$ with $M = \frac{1}{|\mathcal{L}|} \sum_{(i, j) \in \mathcal{L}} e_{ij} e_{ij}^\top$, where $e_{ij}$ is the unit vector from $p_i$ to $p_j$. $M$ does not depend on the scale $t$.

*Proof.* For a long pair let $\Delta = p_j - p_i$. Then $I(p_j) - I(p_i) = (a, b) \cdot \Delta$, so $g(p_i, p_j) = \Delta (\Delta \cdot (a, b)) / \lVert \Delta \rVert^2 = e_{ij} e_{ij}^\top (a, b)$. Taking the mean gives $M (a, b)$. Scaling the pattern by $t$ does not change the unit vectors. $\square$

For the pattern of the page, the reflection $v \mapsto -v$ maps each ring onto itself, so the off-diagonal entry of $M$ is 0, and a direct computation gives $M \approx \operatorname{diag}(0.5014, 0.4986)$. So the angle of $M(a, b)$ differs from the angle of $(a, b)$ by at most about 0.16 degrees. In the code the smoothed values are means over pixels, which are exact on a ramp only when the window is symmetric about the point; the tests check the angle to within one degree.

**Theorem.** The detector returns exactly the points of Lemma 2, with a scale in the range of the adjacent layers by Lemma 3. For each returned point far enough from the border, the descriptor is the string of 512 comparisons of the short pairs of the pattern turned by the orientation of the long pairs. It does not change when the image is multiplied by a positive constant, and on a ramp the orientation follows the direction of the ramp as in Lemma 5.

*Proof.* Line L1 computes the scores by Lemma 1, and line L2 keeps the points by Lemma 2 and refines the scale by Lemma 3. Lines L3 to L5 compute $g$ and $\alpha$ as defined, and lines L6 and L7 set bit $k$ for the short pair $k$ as defined. Lemma 4 gives the invariance to a gain and Lemma 5 the behavior on a ramp. $\square$
