---
title: The Canny detector is exact on ramps and gives one response at a step
proves: [correctness]
status: full
---

The kernels are $g[k] = e^{-k^2/(2\sigma^2)} / Z$ and $d[k] = k\, g[k] / \mu_2$ for $|k| \le r$, with $\sum_k g[k] = 1$ and $\mu_2 = \sum_k k^2 g[k] > 0$. So $g$ is even, $d$ is odd, $d[0] = 0$, $d[k] > 0$ for $k > 0$, $\sum_k d[k] = 0$ and $\sum_k k\, d[k] = 1$. Line L1 computes, with the clamp rule,

$$g_x(x, y) = \sum_{j} g[j] \sum_{k} d[k]\, I(x + k, y + j), \qquad g_y(x, y) = \sum_{j} g[j] \sum_{k} d[k]\, I(x + j, y + k).$$

Lines L2 and L3 are the algorithms of the pages on non-maximum suppression and on hysteresis thresholding, and their proofs show that line L2 keeps exactly the interior pixels $p$ with $m(p) > 0$, $m(p) > m(p - d)$ and $m(p) \ge m(p + d)$ for the rounded gradient step $d$, and that line L3 keeps exactly the pixels with $m \ge t_\ell^2$ joined by a path of such pixels to a pixel with $m \ge t_h^2$. Here we prove what line L1 gives, and what the three lines give together on a step.

**Lemma 1 (exact on affine images).** Let $I(x, y) = a x + b y + c$, and let $(x, y)$ have $r \le x \le W - 1 - r$ and $r \le y \le H - 1 - r$. Then $g_x(x, y) = a$ and $g_y(x, y) = b$.

*Proof.* No read is clamped. The inner sum of $g_x$ is $\sum_k d[k] (a(x + k) + b(y + j) + c) = a \sum_k k\, d[k] + (a x + b(y + j) + c) \sum_k d[k] = a$, because the two sums are 1 and 0. Then $g_x = \sum_j g[j]\, a = a$. The same steps with the axes exchanged give $g_y = b$. $\square$

**Lemma 2 (the response to a step).** Let $I(x, y) = 0$ for $x \le c$ and $I(x, y) = A$ for $x \ge c + 1$, with $A > 0$ and $0 \le c \le W - 2$. Let $F(i) = \sum_{k \ge i} d[k]$, with the sum over $i \le k \le r$. Then for every pixel, $g_y = 0$ and $g_x(x, y) = A\, F(c + 1 - x)$. The function $F$ has $F(0) = F(1) = S$ with $S = \sum_{k = 1}^{r} d[k] > 0$, it is strictly decreasing on $1 \le i \le r + 1$, strictly increasing on $-r \le i \le 0$, and $F(i) = 0$ for $i > r$ and for $i \le -r$.

*Proof.* The clamp rule extends the image by its border values. The left border value is 0 and the right one is $A$, so the extended image is the same step on all integers, and it does not depend on $y$. So the inner sum of $g_y$ is $I(x + j, \cdot) \sum_k d[k] = 0$. The inner sum of $g_x$ is $A \sum_{k : x + k \ge c + 1} d[k] = A\, F(c + 1 - x)$, and the outer sum multiplies by $\sum_j g[j] = 1$. For $F$: $F(1) = S$, and $F(0) = F(1) + d[0] = S$. For $1 \le i \le r$, $F(i) - F(i + 1) = d[i] > 0$, so $F$ decreases strictly from $F(1) = S$ to $F(r + 1) = 0$. For $-r < i \le 0$, $F(i) - F(i - 1) = -d[i - 1] = d[1 - i] > 0$, because $d$ is odd, so $F$ increases strictly from $F(-r) = \sum_k d[k] = 0$ to $F(0) = S$. For $i > r$ the sum is empty, and for $i \le -r$ it is the full sum, which is 0. $\square$

**Theorem (one response at the step).** In the setting of Lemma 2, let $1 \le c$, $c + 1 \le W - 2$, $H \ge 3$ and $A S \ge t_h$. Then the output of CANNY is exactly the set of pixels $(c, y)$ with $1 \le y \le H - 2$.

*Proof.* By Lemma 2, $g_y = 0$ and $m(x, y) = A^2 F(c + 1 - x)^2$, which depends only on $x$. Write $m(x)$. Where $m(x) > 0$, $g_x > 0$ and $g_y = 0$, so the sector is 0 and the step is $d = (1, 0)$. Consider an interior pixel $(x, y)$.

- If $x = c$: $m(c) = A^2 S^2$ and $m(c + 1) = A^2 F(0)^2 = A^2 S^2$, so $m(c) \ge m(c + 1)$. Also $m(c - 1) = A^2 F(2)^2 < A^2 S^2$, because $0 \le F(2) < F(1)$. So the pixel stays.
- If $x = c + 1$: the value behind is $m(c) = m(c + 1)$, so the strict test fails.
- If $x < c$ and $m(x) > 0$: $i = c + 1 - x \ge 2$, and the value in front is $A^2 F(i - 1)^2 > A^2 F(i)^2$, because $F$ decreases strictly on $[1, r + 1]$ and $F(i) > 0$ means $i \le r$. So the test $m(x) \ge m(x + 1)$ fails.
- If $x > c + 1$ and $m(x) > 0$: $i \le -1$, and the value behind is $A^2 F(i + 1)^2 > A^2 F(i)^2$, because $F$ increases strictly on $[-r, 0]$ and $F(i) > 0$ means $i > -r$. So the test $m(x) > m(x - 1)$ fails.
- Pixels with $m(x) = 0$ are skipped by suppression.

So line L2 keeps exactly the interior pixels of column $c$, each with the value $A^2 S^2 \ge t_h^2$. All of them are strong, and no other pixel has a nonzero value, so line L3 returns exactly these pixels. $\blacksquare$

So, on a step, the detector puts exactly one pixel in each interior row, and it is at distance $\tfrac{1}{2}$ from the true edge at $x = c + \tfrac{1}{2}$, the least possible distance for a pixel. By the symmetry of the grid, the same holds for a horizontal step, with the step $d = (0, 1)$.

**A remark on floating point.** The tie $m(c) = m(c + 1)$ is exact also in floating point. In the implementation, the sum of $g_x$ at $x = c$ and at $x = c + 1$ adds the same nonzero products $d[k] A$ for $k = 1, \ldots, r$ in the same order, because the products for $k \le 0$ are exact zeros. So the tie rule of line L2 decides, as in the proof.

**What the theorem does not say.** The theorem is about steps along an axis. On a step at 45 degrees, the step $d = (1, 1)$ of line L2 adds 2 to $x + y$, so the comparisons skip the neighboring anti-diagonals, and two adjacent anti-diagonals can both stay. The test of the implementation shows this on the anti-diagonal $x + y = 40$ with $\sigma = 1.5$. So Canny's single response criterion is a design goal that the rounded suppression meets along the axes and not on all directions.
