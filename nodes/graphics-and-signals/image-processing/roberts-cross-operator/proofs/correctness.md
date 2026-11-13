---
title: The Roberts cross gives exact diagonal differences on affine images
proves: [correctness]
status: full
---

Lines L1 and L2 visit each pixel once, and lines L3 and L4 compute $g_1(x, y) = I(x, y) - I(x + 1, y + 1)$ and $g_2(x, y) = I(x + 1, y) - I(x, y + 1)$, with the reads at $x + 1 = W$ or $y + 1 = H$ clamped to the last column or row. This is the correlation with $R_1$ and $R_2$ by definition, so we only have to show what the outputs estimate.

**Theorem 1 (exact on affine images).** Let $I(x, y) = a x + b y + k$, and let $(x, y)$ be a pixel with $x \le W - 2$ and $y \le H - 2$. Then $g_1 = -(a + b)$, $g_2 = a - b$, $g_2 - g_1 = 2a$, $-(g_1 + g_2) = 2b$, and $g_1^2 + g_2^2 = 2 (a^2 + b^2)$.

*Proof.* No read is clamped. Then $g_1 = (a x + b y + k) - (a (x + 1) + b (y + 1) + k) = -(a + b)$ and $g_2 = (a (x + 1) + b y + k) - (a x + b (y + 1) + k) = a - b$. The sum and the difference follow at once. Last, $(a + b)^2 + (a - b)^2 = 2 a^2 + 2 b^2$, because the cross terms $\pm 2ab$ cancel. $\square$

So the map $(a, b) \mapsto (g_1, g_2)$ is $\sqrt{2}$ times an orthogonal map: the matrix $\begin{pmatrix} -1 & -1 \\ 1 & -1 \end{pmatrix}$ has orthogonal rows of length $\sqrt{2}$. This is why the magnitude $\sqrt{g_1^2 + g_2^2}$ is $\sqrt{2}\, |\nabla I|$ for every direction of an affine gradient, and why $g_x = g_2 - g_1$, $g_y = -(g_1 + g_2)$ undo the turn up to the factor 2.

**Theorem 2 (accuracy at the center of the block).** Let pixel $(x, y)$ hold $I(hx, hy)$ for a function $I$ with continuous derivatives up to order 3, and let $p = (h(x + \tfrac{1}{2}), h(y + \tfrac{1}{2}))$ be the center of the block. Then

$$g_1 = -h (I_x + I_y)(p) + O(h^3), \qquad g_2 = h (I_x - I_y)(p) + O(h^3),$$

so $(g_2 - g_1) / (2h) = I_x(p) + O(h^2)$ and $-(g_1 + g_2) / (2h) = I_y(p) + O(h^2)$.

*Proof.* Let $d_1 = \tfrac{h}{2}(1, 1)$ and $d_2 = \tfrac{h}{2}(1, -1)$. The four pixels of the block are $p - d_1$, $p + d_1$, $p + d_2$ and $p - d_2$, in the order top left, bottom right, top right, bottom left. So $g_1 = I(p - d_1) - I(p + d_1)$ and $g_2 = I(p + d_2) - I(p - d_2)$. For a function $f$ with continuous derivatives up to order 3, Taylor's theorem gives $f(p + d) - f(p - d) = 2\, d \cdot \nabla f(p) + O(|d|^3)$, because the second order terms cancel. With $d = d_1$, $2\, d_1 \cdot \nabla I = h (I_x + I_y)$, which gives the formula for $g_1$ with its sign. With $d = d_2$, $2\, d_2 \cdot \nabla I = h (I_x - I_y)$, which gives $g_2$. Then $g_2 - g_1 = 2h I_x + O(h^3)$ and $-(g_1 + g_2) = 2h I_y + O(h^3)$. $\blacksquare$

At the pixel $(x, y)$ itself instead of at $p$, the gradient differs by $O(h)$, because $|p - (hx, hy)| = h / \sqrt{2}$. This is the half pixel shift of the pitfalls.

**Step response.** Let $I(x, y) = 0$ for $x \le c$ and $I(x, y) = A$ for $x \ge c + 1$. At $x = c$, $g_1 = 0 - A = -A$ and $g_2 = A - 0 = A$. At every other $x$, both pixels of each diagonal are on the same side of the step, so $g_1 = g_2 = 0$. The response is one block wide, at $x = c + \tfrac{1}{2}$.
