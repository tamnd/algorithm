---
title: Correctness of the histogram of oriented gradients
proves: [correctness]
status: full
---

Let $I$ be a window with $W$ columns and $H$ rows, $c$ the cell size, $B$ the number of bins, $n_x = \lfloor W / c \rfloor$ and $n_y = \lfloor H / c \rfloor$. The gradient, the magnitude $m$, the unsigned angle $\varphi \in [0°, 180°)$ and the voting are as defined on the page, with the image extended by its edge pixels at the border. Let $w = 180° / B$.

**Lemma 1 (orientation weights).** For each $\varphi \in [0°, 180°)$, line L3 gives two bins $b_0$ and $b_1 = b_0 + 1 \bmod B$ with weights $1 - f$ and $f$, where $f \in [0, 1)$. These are the two bins whose centers on the circle of 180 degrees are nearest to $\varphi$, and the weight of each bin is $1 - d / w$, where $d$ is the circular distance from $\varphi$ to its center.

*Proof.* Let $x = \varphi / w - \frac{1}{2}$, $k = \lfloor x \rfloor$ and $f = x - k \in [0, 1)$. The centers of the bins $k$ and $k + 1$ are $(k + \frac12) w$ and $(k + \frac32) w$, and $\varphi = (k + \frac12 + f) w$ lies between them, at the distance $f w$ from the first and $(1 - f) w$ from the second. Since $x \in [-\frac12, B - \frac12)$, $k$ is in $\{-1, \dots, B - 1\}$; taking $k$ and $k + 1$ modulo $B$ maps the centers $-\frac12 w$ and $(B + \frac12) w$ to the centers $(B - \frac12) w$ and $\frac12 w$, which are the same points on the circle of length $B w = 180°$. All other centers are at a distance of at least $w$. So the weights $1 - f = 1 - f w / w$ and $f = 1 - (1 - f) w / w$ are as claimed, and they are nonnegative and sum to 1. $\square$

**Lemma 2 (conservation of the votes).** Without spatial voting, each pixel inside the $n_x c \times n_y c$ grid adds exactly $m$ to the histogram of its cell. With spatial voting, a pixel $(u, v)$ whose coordinates $x = (u + \frac12)/c - \frac12$ and $y = (v + \frac12)/c - \frac12$ lie in $[0, n_x - 1] \times [0, n_y - 1]$ adds exactly $m$ to the cells in total, and every other pixel adds between 0 and $m$.

*Proof.* Without spatial voting, the pixel adds $m (1 - f) + m f = m$ to its cell by Lemma 1. With spatial voting, it adds $m \, w_y w_x w_b$ for the cell weights $w_y \in \{1 - f_y, f_y\}$, $w_x \in \{1 - f_x, f_x\}$ and the bin weights $w_b$. The sum over all four cells and both bins is $m (1 - f_y + f_y)(1 - f_x + f_x)(1 - f + f) = m$. If $x$ and $y$ are in the given range, the cells $\lfloor x \rfloor$, $\lfloor x \rfloor + 1$ (when its weight is nonzero) and the same in $y$ all exist, so no term is left out. Otherwise some terms are left out; all terms are nonnegative, so the sum is between 0 and $m$. $\square$

**Lemma 3 (offset and negation).** Let $I'(u, v) = a + s I(u, v)$ with a constant $a$ and $s \in \{1, -1\}$. Then $I'$ has the same magnitudes and unsigned angles as $I$, so the same cell histograms and the same descriptor.

*Proof.* Each gradient component is a difference of two pixel values, so $g'_u = s g_u$ and $g'_v = s g_v$, and the magnitude does not change. If $s = -1$, the vector $(g_u, g_v)$ turns by $180°$ when it is not zero, so $\operatorname{atan2}$ changes by $\pm 180°$, and the angle modulo $180°$ does not change. Pixels with a zero gradient add nothing in both cases. So the cell histograms are equal, and so are the blocks. $\square$

In floating point the offset case is exact for integer images, as in the tests; the negation case is equal up to the rounding of $\operatorname{atan2}$.

**Lemma 4 (mirror).** Let $I'(u, v) = I(W - 1 - u, v)$ with $W = n_x c$. Then the cell histograms satisfy $h'_{y, x}(b) = h_{y, n_x - 1 - x}(B - 1 - b)$.

*Proof.* At the pixel $(u, v)$ of $I'$, the gradient is $(-g_u, g_v)$ of $I$ at $(W - 1 - u, v)$; the edge extension commutes with the mirror. The magnitude is the same. The angle of $(-g_u, g_v)$ is $180° - \varphi$ modulo $180°$. The bin centers $(b + \frac12) w$ map to $180° - (b + \frac12) w = (B - 1 - b + \frac12) w$, so the circular distances from $180° - \varphi$ to the center of $B - 1 - b$ equal those from $\varphi$ to the center of $b$, and by Lemma 1 the bin weights move from $b$ to $B - 1 - b$. In space, $x' = (W - 1 - u + \frac12)/c - \frac12 = n_x - 1 - x$, so the bilinear weight of the cell $n_x - 1 - x_0$ for the mirrored pixel equals the weight of the cell $x_0$ for the original pixel. Summing over the pixels gives the claim. $\square$

**Lemma 5 (L2-Hys).** Let $z = \text{L2-Hys}(x)$ with $\varepsilon = 0$, the clip value $\tau > 0$ and $x \ne 0$ with nonnegative entries. Then $\lVert z \rVert_2 = 1$, and $\text{L2-Hys}(a x) = z$ for every $a > 0$.

*Proof.* After the first division $y = x / \lVert x \rVert_2$, which does not change when $x$ is replaced by $a x$. The clip gives $y'_k = \min(y_k, \tau)$, which is not the zero vector because some $y_k > 0$ and $\tau > 0$. The second division gives a vector of norm 1. Each step depends only on $y$, so the output does not depend on $a$. $\square$

With $\varepsilon > 0$, the first step gives $x / \sqrt{\lVert x \rVert^2 + \varepsilon^2}$, which differs from $x / \lVert x \rVert$ by a factor $1 / \sqrt{1 + \varepsilon^2 / \lVert x \rVert^2}$, close to 1 when $\lVert x \rVert \gg \varepsilon$; this is why a gain changes the descriptor only a little.

**Theorem.** HOG returns the concatenation, over the $(n_x - 1)(n_y - 1)$ blocks of $2 \times 2$ cells in row order, of the L2-Hys normalized cell histograms of the definition. The length is $4 B (n_x - 1)(n_y - 1)$. The descriptor does not change under a constant offset or under $I \mapsto a - I$, and, with $\varepsilon = 0$, each block has norm 1 and does not change when the window is multiplied by $a > 0$.

*Proof.* Lines L1 and L2 compute the magnitude and the unsigned angle. By Lemma 1, lines L3 and L4 put each vote into the bins and cells of the definition, with the weights of the definition, and by Lemma 2 no part of a vote is lost except for the pixels near the border whose cell centers do not exist. The loop of line L5 runs over the $(n_x - 1)(n_y - 1)$ blocks; line L6 joins four histograms of $B$ values, and line L7 normalizes them, which gives the length. Lemma 3 gives the invariance to an offset and to negation. Multiplying $I$ by $a$ multiplies every magnitude by $a$ and keeps every angle, so every block vector is multiplied by $a$, and Lemma 5 gives the last claim. $\square$
