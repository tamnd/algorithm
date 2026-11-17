---
title: Correctness of RoIAlign, mask pasting and the mask loss
proves: [correctness]
status: full
---

This proof covers the parts of Mask R-CNN that are not learned: RoIAlign (lines L1 to L7 of the main page), the pasting of a mask into the image (lines L8 to L11) and the mask loss. It says nothing about the quality of the network weights. That is a benchmark question.

Conventions. A grid $g$ has $W$ columns and $H$ rows, the value of cell $(i, j)$ is $g[j][i]$, and the center of the cell is the point $(i, j)$. A box is $b = (x_1, y_1, x_2, y_2)$ with $x_1 < x_2$ and $y_1 < y_2$. Let $D_x = \max |g[j][i+1] - g[j][i]|$ and $D_y = \max |g[j+1][i] - g[j][i]|$ over all valid indices.

**Lemma 1 (bilinear interpolation).** For $(x, y) \in [0, W-1] \times [0, H-1]$, BILINEAR returns
$$\hat g(x, y) = \sum_{i, j} g[j][i]\, \Lambda(x - i)\, \Lambda(y - j), \qquad \Lambda(t) = \max(0, 1 - |t|).$$
The function $\hat g$ (a) is a convex combination of at most four grid values, (b) equals $\alpha x + \beta y + \gamma$ if $g[j][i] = \alpha i + \beta j + \gamma$ for all cells, and (c) satisfies $|\hat g(x, y) - \hat g(x', y')| \le D_x |x - x'| + D_y |y - y'|$.

*Proof.* Let $x_0 = \lfloor x \rfloor$, $a_x = x - x_0$, and the same for $y$. For $i \notin \{x_0, x_0 + 1\}$ we have $|x - i| \ge 1$ and $\Lambda(x - i) = 0$. Also $\Lambda(x - x_0) = 1 - a_x$ and $\Lambda(x - x_0 - 1) = a_x$. So the sum has the four terms that the code computes, with weights $(1 - a_x)(1 - a_y)$, $a_x (1 - a_y)$, $(1 - a_x) a_y$ and $a_x a_y$. These are nonnegative with sum 1, which is (a). At $x = W - 1$ we have $a_x = 0$, so the clamped index $\min(x_0 + 1, W - 1)$ gets weight 0 and does no harm.

For (b), $\sum_i \Lambda(x - i) = 1$ and $\sum_i i\, \Lambda(x - i) = (1 - a_x) x_0 + a_x (x_0 + 1) = x$ on $[0, W - 1]$. The sums split, and $\hat g = \alpha x + \beta y + \gamma$.

For (c), in a cell $[x_0, x_0 + 1] \times [y_0, y_0 + 1]$ the partial derivative in $x$ is $(1 - a_y)(g[y_0][x_0 + 1] - g[y_0][x_0]) + a_y (g[y_0 + 1][x_0 + 1] - g[y_0 + 1][x_0])$, a convex combination of two horizontal differences, so its absolute value is at most $D_x$. The same holds in $y$. $\hat g$ is continuous across cell borders, since there one weight is zero, and so it is Lipschitz with these constants along each axis. Going first along $x$ and then along $y$ gives the bound. $\square$

Outside the grid the code first clamps $x$ to $[0, W - 1]$ and $y$ to $[0, H - 1]$. Clamping is 1-Lipschitz, so (a) and (c) still hold on $[-1, W] \times [-1, H]$. Beyond that band the code returns 0, as the Detectron code does. This makes the result jump at $x = -1$, $x = W$, $y = -1$ and $y = H$.

**Theorem 1 (RoIAlign).** Let lines L1 to L7 run on a box $b$ with $P \times P$ bins and $s \times s$ samples per bin, and let every sample point lie in $[-1, W] \times [-1, H]$.

1. *Sample points.* Bin $(r, c)$ is the rectangle $[x_1 + c\, b_w, x_1 + (c + 1) b_w] \times [y_1 + r\, b_h, y_1 + (r + 1) b_h]$, with $b_w = (x_2 - x_1)/P$ and $b_h = (y_2 - y_1)/P$. Its samples are the centers of the $s \times s$ equal sub-rectangles of the bin, so the output is the midpoint rule for the mean of $\hat g$ over the bin.
2. *Affine maps.* If $g$ is affine as in Lemma 1(b) and the bin lies in $[0, W - 1] \times [0, H - 1]$, then output $(r, c)$ is the value of the affine function at the bin center.
3. *Continuity.* If $b$ and $b'$ are two boxes with all samples in $[0, W - 1] \times [0, H - 1]$, then every output changes by at most $D_x \max(|x_1 - x_1'|, |x_2 - x_2'|) + D_y \max(|y_1 - y_1'|, |y_2 - y_2'|)$.
4. *Integer shifts.* If $g'[j + \delta_y][i + \delta_x] = g[j][i]$ for integers $\delta_x$, $\delta_y$, and the samples of $b$ in $g$ and of the shifted box $b + (\delta_x, \delta_y, \delta_x, \delta_y)$ in $g'$ both lie in the region where the two grids agree up to the shift, then the outputs are equal.

*Proof.* (1) Line L5 places sample $(a, b)$ of bin $(r, c)$ at $y = y_1 + (r + (a + \tfrac12)/s) b_h$ and $x = x_1 + (c + (b + \tfrac12)/s) b_w$. The bin has width $b_w$, the sub-rectangles have width $b_w / s$, and sub-rectangle $b$ has its center at $x_1 + c\, b_w + (b + \tfrac12) b_w / s$. Line L7 divides the sum of line L6 by $s^2$.

(2) By Lemma 1(b), $\hat g$ is affine on the bin, so the mean of the samples is the affine function at the mean of the sample points. The mean of $(b + \tfrac12)/s$ over $b = 0, \ldots, s - 1$ is $\tfrac12$, so the mean point is $(x_1 + (c + \tfrac12) b_w, y_1 + (r + \tfrac12) b_h)$, the bin center.

(3) Each sample point has $x = (1 - t) x_1 + t x_2$ with $t = (c + (b + \tfrac12)/s)/P \in (0, 1)$. So $|x - x'| \le (1 - t)|x_1 - x_1'| + t |x_2 - x_2'| \le \max(|x_1 - x_1'|, |x_2 - x_2'|)$, and the same for $y$. Lemma 1(c) bounds the change of each sample, and an average of numbers that each change by at most $\epsilon$ changes by at most $\epsilon$.

(4) The sample points of the shifted box are the old ones plus $(\delta_x, \delta_y)$. An integer shift keeps the fractions $a_x$ and $a_y$ and adds $(\delta_x, \delta_y)$ to the four grid indices. So the four weights are the same, and the four grid values are the same by the hypothesis. $\square$

Quantized RoI pooling does not satisfy (3). It rounds the box to whole cells, so its output is a step function of $x_1$: in the example of the main page a move of $0.01$ cell changes every output by 1, while the RoIAlign output changes by $0.01$.

**Lemma 2 (feature coordinates).** Let pixel $u$ cover the interval $[u - \tfrac12, u + \tfrac12]$ and let cell $i$ of a feature map of stride $S$ cover pixels $iS$ to $iS + S - 1$. The affine map $\phi(x) = (x + \tfrac12)/S - \tfrac12$ sends the interval of cell $i$, $[iS - \tfrac12, iS + S - \tfrac12]$, onto $[i - \tfrac12, i + \tfrac12]$, and the center $iS + (S - 1)/2$ to $i$.

*Proof.* $\phi(iS - \tfrac12) = i - \tfrac12$ and $\phi(iS + S - \tfrac12) = i + \tfrac12$, and $\phi$ is affine, so the midpoint goes to the midpoint $i$. $\square$

So the function image_to_feature puts a box on the feature map without the half-cell shift that the map $x \mapsto x / S$ would cause. This is the alignment that the option aligned=True of Detectron2 gives, written for integer pixel centers.

**Theorem 2 (pasting).** Let the mask $M$ have $m \times m$ values in $[0, 1]$, and let lines L8 to L11 paste it for box $b$ into a $w \times h$ image with threshold $\theta$.

1. *The pixel set.* A pixel $(u, v)$ is visited if and only if $0 \le u < w$, $0 \le v < h$, $x_1 \le u < x_2$ and $y_1 \le v < y_2$. All other pixels are 0.
2. *Mask cells.* Split the box into $m \times m$ equal cells. The center of cell $(j, k)$, the point $(x_1 + (j + \tfrac12)(x_2 - x_1)/m,\ y_1 + (k + \tfrac12)(y_2 - y_1)/m)$, goes to the point $(j, k)$ under the map of line L9. So a pixel at the center of a mask cell reads exactly that mask value.
3. *Constant masks.* If all values of $M$ are $\mu$, the output is 1 exactly on the pixels of (1) when $\mu \ge \theta$, and 0 everywhere when $\mu < \theta$.
4. *Step masks.* Let $m$ be even and let $M[k][j] = 1$ for $j < m/2$ and 0 otherwise, with $\theta = \tfrac12$. Then a visited pixel is 1 if and only if $u \le (x_1 + x_2)/2$.

*Proof.* (1) For an integer $u$, $u \ge x_1$ if and only if $u \ge \lceil x_1 \rceil$, and $u < x_2$ if and only if $u \le \lceil x_2 \rceil - 1$. Line L8 loops over exactly these integers, cut to the image.

(2) Put $x = x_1 + (j + \tfrac12)(x_2 - x_1)/m$ into $m_x = (x - x_1) m / (x_2 - x_1) - \tfrac12$. This gives $m_x = j$. The same holds for $y$.

(3) By Lemma 1(a) with clamping, every interpolated value is $\mu$.

(4) The value at $m_x$ does not depend on $m_y$, since all rows are equal. For $m_x \le m/2 - 1$ it is 1, for $m_x \ge m/2$ it is 0, and in between it is $1 - (m_x - (m/2 - 1)) = m/2 - m_x$. Clamping only moves points into the parts where the value is constant. So the value is at least $\tfrac12$ if and only if $m_x \le (m - 1)/2$, that is $(u - x_1) m / (x_2 - x_1) \le m / 2$, that is $u \le (x_1 + x_2)/2$. $\square$

Part 4 shows that the 0.5 level of the interpolated mask is at the true position of the step, not shifted by half a mask cell. A map $m_x = (u - x_1) m / (x_2 - x_1)$ without the $-\tfrac12$ would shift the edge by half a mask cell to the right.

**Theorem 3 (the mask loss).** For logits $z$ and a binary target $t$, the per-pixel term of mask_loss is $\ell(z, t) = \max(z, 0) - t z + \log(1 + e^{-|z|})$. Then:

1. $\ell(z, t) = -t \log \sigma(z) - (1 - t) \log(1 - \sigma(z))$ with $\sigma(z) = 1/(1 + e^{-z})$, the binary cross-entropy of the sigmoid.
2. $\partial \ell / \partial z = \sigma(z) - t$, $\ell$ is strictly convex in $z$, $\ell \ge 0$, and $\ell(0, t) = \log 2$.
3. The loss for an RoI of class $k$ does not depend on the logits of the other $K - 1$ masks, so their gradients from this RoI are zero.

*Proof.* (1) $\max(z, 0) + \log(1 + e^{-|z|}) = \log(1 + e^z)$, checked separately for $z \ge 0$ and $z < 0$. Also $-\log \sigma(z) = \log(1 + e^{-z}) = \log(1 + e^z) - z$ and $-\log(1 - \sigma(z)) = \log(1 + e^z)$. So the right side is $t (\log(1 + e^z) - z) + (1 - t) \log(1 + e^z) = \log(1 + e^z) - t z$.

(2) The derivative of $\log(1 + e^z)$ is $\sigma(z)$, and the second derivative is $\sigma(z)(1 - \sigma(z)) > 0$. Both terms of (1) are nonnegative because $\sigma \in (0, 1)$. At $z = 0$ the value is $\log 2$.

(3) The code reads only logits[k]. $\square$

Part 3 is the point of the design in the paper: with a softmax over the classes at each pixel the masks of different classes would compete, and with independent sigmoids they do not. That this gives better masks is a benchmark result of the paper, not a consequence of the theorem.

**Cost.** Line L6 costs $O(1)$ per channel, so RoIAlign on a map with $C$ channels costs $O(C P^2 s^2)$ per box. Pasting costs $O(1)$ per visited pixel, at most $O(w h)$ per box. The loss costs $O(m^2)$ per RoI. All counts are in the real-RAM model.
