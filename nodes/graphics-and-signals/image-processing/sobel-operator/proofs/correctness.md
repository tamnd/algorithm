---
title: The Sobel passes compute the Sobel masks and are exact on affine images
proves: [correctness]
status: full
---

We write $c_W(x) = \min(\max(x, 0), W - 1)$ and $c_H(y) = \min(\max(y, 0), H - 1)$ for the clamp rule, so a read of $I$ at $(x, y)$ returns $I(c_W(x), c_H(y))$. Let $w = (w_{-1}, w_0, w_1) = (1, 2, 1)$ be the smoothing weights and $e = (e_{-1}, e_0, e_1) = (-1, 0, 1)$ the difference weights. Then $K_x[v][u] = w_v e_u$ and $K_y[v][u] = e_v w_u$ for $u, v \in \{-1, 0, 1\}$.

**Lemma 1 (separable form).** For every pixel $(x, y)$ of the image, the value $g_x(x, y)$ of line L3 equals $\sum_{u, v} K_x[v][u]\, I(c_W(x + u), c_H(y + v))$, and the value $g_y(x, y)$ of line L4 equals the same sum with $K_y$.

*Proof.* Line L1 gives $s(x', y) = \sum_v w_v I(x', c_H(y + v))$ for each column $x'$ of the image. Line L3 reads $s$ with the clamp rule, at the columns $x' = c_W(x + u)$ for $u = \pm 1$. Each such $x'$ is a column of the image, and $c_W(x') = x'$, so

$$g_x(x, y) = \sum_u e_u\, s(c_W(x + u), y) = \sum_u \sum_v e_u w_v\, I(c_W(x + u), c_H(y + v)).$$

The term $u = 0$ has $e_0 = 0$, so it does not matter that line L3 omits it. This is the direct sum with $K_x[v][u] = w_v e_u$. The proof for $g_y$ is the same with the roles of $x$ and $y$ changed. The key step is that the clamp rule acts on each coordinate on its own: clamping $x$ first and $y$ later gives the same pixel as clamping both at once. $\square$

**Theorem 2 (exact on affine images).** Let $I(x, y) = a x + b y + k$ for constants $a, b, k$, and let $(x, y)$ be a pixel with $1 \le x \le W - 2$ and $1 \le y \le H - 2$. Then $g_x(x, y) = 8a$ and $g_y(x, y) = 8b$.

*Proof.* At such a pixel no read is clamped. By Lemma 1,

$$g_x(x, y) = \sum_u \sum_v e_u w_v \bigl(a(x + u) + b(y + v) + k\bigr).$$

The weights have the sums $\sum_u e_u = 0$, $\sum_u u\, e_u = 2$, $\sum_v w_v = 4$ and $\sum_v v\, w_v = 0$. Each term that holds $\sum_u e_u$ is 0, so only the term with $a u$ is left:

$$g_x(x, y) = a \Bigl(\sum_u u\, e_u\Bigr) \Bigl(\sum_v w_v\Bigr) = a \cdot 2 \cdot 4 = 8a.$$

For $g_y$ the roles of $u$ and $v$ change, and the same sums give $8b$. $\square$

**Theorem 3 (second order accuracy).** Let $I$ be a function with continuous derivatives up to order 5, sampled at the spacing $h$, so that pixel $(x, y)$ holds $I(hx, hy)$. At an interior pixel,

$$\frac{g_x(x, y)}{8h} = I_x + h^2 \left( \frac{1}{6} I_{xxx} + \frac{1}{4} I_{xyy} \right) + O(h^4),$$

with the derivatives taken at $(hx, hy)$. The same holds for $g_y$ with $x$ and $y$ changed.

*Proof.* By Taylor's theorem in $y$, $I(\cdot, y - h) + 2 I(\cdot, y) + I(\cdot, y + h) = 4 I + h^2 I_{yy} + O(h^4)$, because the odd terms cancel. So $s = 4 I + h^2 I_{yy} + O(h^4)$ as a function of $x$. A central difference of a smooth function $f$ gives $f(x + h) - f(x - h) = 2h f_x + \tfrac{h^3}{3} f_{xxx} + O(h^5)$. With $f = s$,

$$g_x = 2h \bigl(4 I_x + h^2 I_{xyy}\bigr) + \frac{h^3}{3} \cdot 4 I_{xxx} + O(h^5) = 8h I_x + h^3 \left( 2 I_{xyy} + \frac{4}{3} I_{xxx} \right) + O(h^5).$$

Divide by $8h$ to get the claim. $\square$

**Lemma 4 (a smoothed Roberts gradient).** Let $B = \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$ and $D = \begin{pmatrix} -1 & 1 \\ -1 & 1 \end{pmatrix}$. The full 2D convolution of $B$ and $D$ is $K_x$.

*Proof.* Each mask is an outer product: $B = [1, 1]^T [1, 1]$ and $D = [1, 1]^T [-1, 1]$. The convolution of two outer products is the outer product of the 1D convolutions. Here $[1, 1] * [1, 1] = [1, 2, 1]$ and $[1, 1] * [-1, 1] = [-1, 0, 1]$, so the result is $[1, 2, 1]^T [-1, 0, 1] = K_x$. $\blacksquare$

The [Roberts cross](/roberts-cross-operator/) masks are $R_1 = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$ and $R_2 = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$, and $D = R_2 - R_1$. So the Sobel $g_x$ is the $2 \times 2$ box sum of the $x$ component of the Roberts gradient turned by 45 degrees, as the main page states.
