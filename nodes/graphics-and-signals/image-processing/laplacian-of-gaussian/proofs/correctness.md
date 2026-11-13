---
title: The separable LoG filter is exact on quadratics and has one zero crossing at a step
proves: [correctness]
status: full
---

The kernels are $g[k] = e^{-k^2/(2\sigma^2)} / Z$ for $|k| \le r$, with $\sum_k g[k] = 1$, and $d_2[k] = a (k^2 - \mu_2) g[k]$ with $\mu_j = \sum_k k^j g[k]$ and $a = 2 / (\mu_4 - \mu_2^2)$. The denominator is positive: it is the variance of $k^2$ when $k$ has the distribution $g$, and $k^2$ is not constant, because $r \ge 1$ and $g > 0$. Both $g$ and $d_2$ are even.

**Lemma 1 (moments of $d_2$).** $\sum_k d_2[k] = 0$, $\sum_k k\, d_2[k] = 0$ and $\sum_k k^2 d_2[k] = 2$.

*Proof.* $\sum_k d_2[k] = a (\mu_2 - \mu_2 \cdot 1) = 0$. The second sum is 0 because $k\, d_2[k]$ is odd. The third is $a (\mu_4 - \mu_2 \mu_2) = 2$. $\square$

**Lemma 2 (the separable form).** Lines L2 to L4 compute the correlation of $I$ with $K[u, v] = d_2[u] g[v] + g[u] d_2[v]$, with the clamp rule.

*Proof.* Let $\tilde I$ be the image extended by the clamp rule. Line L2 computes $A(x, y) = \sum_v g[v] \sum_u d_2[u]\, \tilde I(x + u, y + v)$. The clamp rule of the second pass reads row $y + v$ of the first output, clamped, and the first output at a clamped row is the first pass on the clamped row of $I$, because the clamp along $y$ and the sum along $x$ act on different coordinates. So $A = \sum_{u, v} d_2[u] g[v]\, \tilde I(x + u, y + v)$. Line L3 is the same with the axes exchanged, and line L4 adds the two. $\square$

**Theorem 1 (exact on quadratics).** Let $I(x, y) = c_{20} x^2 + c_{11} x y + c_{02} y^2 + c_{10} x + c_{01} y + c_{00}$, and let $(x, y)$ have $r \le x \le W - 1 - r$ and $r \le y \le H - 1 - r$. Then $L(x, y) = 2 c_{20} + 2 c_{02} = I_{xx} + I_{yy}$.

*Proof.* No read is clamped. By Lemma 2, $L = \sum_{u, v} d_2[u] g[v] I(x + u, y + v) + \sum_{u, v} g[u] d_2[v] I(x + u, y + v)$. Take the first sum, and expand $I(x + u, y + v)$ as a polynomial in $u$ and $v$. Each monomial $u^i v^j$ gives $\left(\sum_u d_2[u] u^i\right) \left(\sum_v g[v] v^j\right)$. By Lemma 1, the first factor is 0 for $i = 0$ and $i = 1$ and 2 for $i = 2$, and the only monomial with $i = 2$ is $c_{20} u^2$, with $j = 0$ and $\sum_v g[v] = 1$. So the first sum is $2 c_{20}$. By the same steps with the axes exchanged, the second sum is $2 c_{02}$. $\blacksquare$

In particular $L = 0$ on affine images and $L = 4$ on $x^2 + y^2$, as the tests check.

**Theorem 2 (one zero crossing at a step).** Let $I(x, y) = 0$ for $x \le c$ and $I(x, y) = A$ for $x \ge c + 1$, with $A > 0$ and $0 \le c \le W - 2$. Let $F(j) = \sum_{k \ge j} d_2[k]$ over $j \le k \le r$. Then in every row, $L(x) = A\, F(c + 1 - x)$, and $L(x) > 0$ for $c + 1 - r \le x \le c$, $L(x) < 0$ for $c + 1 \le x \le c + r$, $L(x) = 0$ for all other $x$, and $L(c) = -L(c + 1)$. So for $0 \le t \le 2 A F(1)$, in exact arithmetic, ZERO-CROSSINGS marks exactly the pixel $c$ in each row.

*Proof.* The clamp rule extends the image as the same step, and the step does not depend on $y$. So in line L3, the pass of $d_2$ along $y$ multiplies a constant by $\sum_k d_2[k] = 0$, and $B = 0$. In line L2, the pass along $x$ gives $A\, F(c + 1 - x)$, and the pass of $g$ along $y$ keeps it, because $\sum g = 1$.

Since $d_2$ is even, $F(j) + F(1 - j) = \sum_{k \ge j} d_2[k] + \sum_{k \le j - 1} d_2[k] = \sum_k d_2[k] = 0$. So $L(c + 1 - j) = -L(c + j)$, which gives $L(c) = -L(c + 1)$ with $j = 1$, and the signs for $x \ge c + 1$ follow from the signs for $x \le c$.

So it is enough to show $F(j) > 0$ for $1 \le j \le r$, and $F(j) = 0$ for $j > r$, which holds because the sum is empty. First, $F(1) = \tfrac{1}{2} \left(\sum_k d_2[k] - d_2[0]\right) = -\tfrac{1}{2} d_2[0] = \tfrac{1}{2} a \mu_2 g[0] > 0$, by evenness. Next, $d_2[k] < 0$ when $k^2 < \mu_2$ and $d_2[k] > 0$ when $k^2 > \mu_2$. Let $1 \le j \le r$. If $j^2 > \mu_2$, every term of $F(j)$ is positive. If $j^2 \le \mu_2$, then $F(j) = F(1) - \sum_{k = 1}^{j - 1} d_2[k]$, and each $d_2[k]$ in this sum has $k^2 < j^2 \le \mu_2$, so it is negative, and $F(j) \ge F(1) > 0$.

Now ZERO-CROSSINGS. The vertical pairs have equal values, so $L(p) L(q) = L(p)^2 \ge 0$ and line L6 never fires for them. Among the horizontal pairs, only $(c, c + 1)$ has values of opposite signs, with $|L(c) - L(c + 1)| = 2 A F(1) \ge t$. The values have the same absolute value, so line L6 marks $p = (c, y)$. The pixels with $L = 0$ have $x \le c - r$ or $x \ge c + r + 1$, and their two horizontal neighbors are 0 or of the same sign, and their vertical neighbors are equal, so line L7 never fires. $\blacksquare$

The marked pixel $c$ is half a pixel from the step at $x = c + \tfrac{1}{2}$, the least possible distance. In floating point, $L(c)$ and $-L(c + 1)$ can differ in the last bits, so the implementation can mark $c + 1$ instead, and the test accepts both.

**The marking rule.** Line L6 marks, for each pair of 4-neighbors that cross zero with a jump of at least $t$, the member of the pair with the smaller absolute value, or the first member on a tie. So a pixel $p$ is marked exactly when some 4-neighbor $q$ crosses zero with it and $p$ wins that pair, or when $L(p) = 0$ and its two neighbors on one axis cross zero. This is a rule stated per pixel, and the test checks the implementation against it on 300 random small grids.
