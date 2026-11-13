---
title: The Prewitt passes compute the Prewitt masks, which give the least squares plane
proves: [correctness]
status: full
---

We write $c_W(x) = \min(\max(x, 0), W - 1)$ and $c_H(y) = \min(\max(y, 0), H - 1)$ for the clamp rule. Let $w = (1, 1, 1)$ and $e = (-1, 0, 1)$, indexed by $-1, 0, 1$. Then $P_x[v][u] = w_v e_u$ and $P_y[v][u] = e_v w_u$.

**Lemma 1 (separable form).** For every pixel $(x, y)$, line L3 gives $g_x(x, y) = \sum_{u, v} P_x[v][u]\, I(c_W(x + u), c_H(y + v))$, and line L4 gives the same sum with $P_y$.

*Proof.* Line L1 gives $s(x', y) = \sum_v w_v I(x', c_H(y + v))$ for each column $x'$ of the image. Line L3 reads $s$ at the columns $x' = c_W(x \pm 1)$, which are inside the image, so

$$g_x(x, y) = \sum_{u = \pm 1} e_u\, s(c_W(x + u), y) = \sum_u \sum_v e_u w_v\, I(c_W(x + u), c_H(y + v)),$$

where the term $u = 0$ is 0 because $e_0 = 0$. The clamp rule acts on each coordinate on its own, so this is the direct sum. The proof for $g_y$ is the same with the axes changed. $\square$

**Theorem 2 (exact on affine images).** If $I(x, y) = a x + b y + k$ and $1 \le x \le W - 2$, $1 \le y \le H - 2$, then $g_x(x, y) = 6a$ and $g_y(x, y) = 6b$.

*Proof.* No read is clamped, so by Lemma 1, $g_x = \sum_u \sum_v e_u w_v (a(x + u) + b(y + v) + k)$. We have $\sum_u e_u = 0$, $\sum_u u\, e_u = 2$ and $\sum_v w_v = 3$. Every term that holds $\sum_u e_u$ is 0, so $g_x = a \cdot 2 \cdot 3 = 6a$. The same sums give $g_y = 6b$. $\square$

**Theorem 3 (least squares plane).** Let $(x, y)$ be an interior pixel and $f(u, v) = I(x + u, y + v)$ for $u, v \in \{-1, 0, 1\}$. The plane $p(u, v) = \alpha u + \beta v + \kappa$ that makes $\sum_{u, v} (f(u, v) - p(u, v))^2$ smallest has $\alpha = g_x(x, y) / 6$ and $\beta = g_y(x, y) / 6$.

*Proof.* The sum of squares is a convex quadratic in $(\alpha, \beta, \kappa)$, so its minimum is where the three partial derivatives are 0. These are the normal equations

$$\sum (f - p)\, u = 0, \qquad \sum (f - p)\, v = 0, \qquad \sum (f - p) = 0,$$

with each sum over the 9 points. On the $3 \times 3$ grid, $\sum u = \sum v = \sum u v = 0$ and $\sum u^2 = \sum v^2 = 6$. So the first equation becomes $\sum f u = 6 \alpha$, the second becomes $\sum f v = 6 \beta$, and the third gives $\kappa$ as the mean of $f$. Now $\sum_{u, v} f(u, v)\, u = \sum_u \sum_v e_u w_v f(u, v) = g_x(x, y)$, because $e_u = u$ and $w_v = 1$. In the same way $\sum f v = g_y(x, y)$. $\square$

**Theorem 4 (second order accuracy).** If pixel $(x, y)$ holds $I(hx, hy)$ for a function $I$ with continuous derivatives up to order 5, then at an interior pixel

$$\frac{g_x(x, y)}{6h} = I_x + h^2 \left( \frac{1}{6} I_{xxx} + \frac{1}{3} I_{xyy} \right) + O(h^4).$$

*Proof.* By Taylor's theorem, $I(\cdot, y - h) + I(\cdot, y) + I(\cdot, y + h) = 3 I + h^2 I_{yy} + O(h^4)$, so $s = 3I + h^2 I_{yy} + O(h^4)$. The central difference gives $s(x + h) - s(x - h) = 2h s_x + \tfrac{h^3}{3} s_{xxx} + O(h^5)$. So

$$g_x = 2h (3 I_x + h^2 I_{xyy}) + \frac{h^3}{3} \cdot 3 I_{xxx} + O(h^5) = 6h I_x + h^3 (2 I_{xyy} + I_{xxx}) + O(h^5).$$

Divide by $6h$. $\blacksquare$
