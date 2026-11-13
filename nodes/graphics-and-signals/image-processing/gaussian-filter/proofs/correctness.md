---
title: The two passes of GAUSSIAN-FILTER equal the direct 2D filter with the same border rule, and n box passes form a kernel of variance n r(r+1)/3
proves: [correctness]
status: full
---

Let $f$ have $W \ge 1$ columns and $H \ge 1$ rows. For an axis of length $n$ the border rule is a map $\mathrm{ext}(\cdot, n)$ from the integers to $\{0, \dots, n-1\} \cup \{\bot\}$ that is the identity on $\{0, \dots, n-1\}$; $\bot$ means no pixel, read as the value $0$. Clamp, mirror and wrap never return $\bot$, and zero returns it for every index outside. The extended image is $\tilde f(i, j) = f[\mathrm{ext}(j, H)][\mathrm{ext}(i, W)]$, and $0$ if either index is $\bot$. For an image $h$ of the same size, $\tilde h$ is defined in the same way.

**Lemma 1 (the kernel).** After lines L1 to L3, $k[u] = e^{-u^2/(2\sigma^2)} / Z$ for $|u| \le R$ with $Z = \sum_{|t| \le R} e^{-t^2/(2\sigma^2)}$, and $\sum_u k[u] = 1$. The 2D kernel of the problem, $K[u][v] = e^{-(u^2+v^2)/(2\sigma^2)} / \sum_{|s|, |t| \le R} e^{-(s^2+t^2)/(2\sigma^2)}$, equals $k[u]\,k[v]$.

*Proof.* The first two statements are lines L2 and L3; $Z > 0$ because each term is positive. For the third, $e^{-(u^2+v^2)/(2\sigma^2)} = e^{-u^2/(2\sigma^2)} e^{-v^2/(2\sigma^2)}$, and the sum over the square $|s|, |t| \le R$ of a product of a function of $s$ and a function of $t$ is the product of the two sums, $Z^2$. $\square$

**Lemma 2 (the row pass on extended rows).** Let $h(x, y) = \sum_{u=-R}^{R} k[u]\, \tilde f(x+u, y)$ for $0 \le x < W$, $0 \le y < H$, as line L4 computes. Then for every integer $j$ and every $0 \le x < W$,

$$\tilde h(x, j) = \sum_{u=-R}^{R} k[u]\, \tilde f(x+u, j).$$

*Proof.* Since $x$ is inside the image, $\tilde h(x, j) = h[\mathrm{ext}(j, H)][x]$. If $\mathrm{ext}(j, H) = \bot$, the left side is $0$, and every $\tilde f(x+u, j)$ is $0$ as well. Otherwise let $y' = \mathrm{ext}(j, H)$. Then $\tilde h(x, j) = h(x, y') = \sum_u k[u] \tilde f(x+u, y')$, and $\tilde f(i, y') = f[y'][\mathrm{ext}(i, W)] = f[\mathrm{ext}(j, H)][\mathrm{ext}(i, W)] = \tilde f(i, j)$, because $\mathrm{ext}(y', H) = y'$. $\square$

**Theorem 1 (the filter).** GAUSSIAN-FILTER returns $g(x, y) = \sum_{v} \sum_{u} K[u][v]\, \tilde f(x+u, y+v)$, the direct 2D filter with the same border rule.

*Proof.* Line L5 computes $g(x, y) = \sum_v k[v]\, \tilde h(x, y+v)$. By Lemma 2 with $j = y + v$ this is $\sum_v k[v] \sum_u k[u] \tilde f(x+u, y+v)$, a finite double sum, which is $\sum_v \sum_u k[u] k[v] \tilde f(x+u, y+v)$, and $k[u] k[v] = K[u][v]$ by Lemma 1. $\square$

The same argument holds for any separable kernel $a[v] b[u]$, which is how the implementation tests the passes against the direct sum with exact rational weights.

**Corollary (constants).** Under clamp, mirror and wrap, a constant image $f \equiv c$ gives $g \equiv c$: every $\tilde f$ value is $c$, and $\sum_{u, v} K[u][v] = (\sum_u k[u])^2 = 1$.

**Theorem 2 (repeated boxes).** Let $b$ be the box of radius $r \ge 0$, the uniform weights $1/(2r+1)$ on $\{-r, \dots, r\}$, and let $b^{*n}$ be its $n$-fold [convolution](/convolution/). Then $b^{*n}$ is symmetric, sums to 1, and has the variance $\sum_t t^2 b^{*n}[t] = n r(r+1)/3$.

*Proof.* Read $b$ as the distribution of a random variable $X$ uniform on $\{-r, \dots, r\}$. Then $b^{*n}$ is the distribution of $X_1 + \dots + X_n$ for independent copies, because the convolution of the distributions of independent integer variables is the distribution of their sum. A sum of probability distributions is again a distribution, so it sums to 1, and it is symmetric because each $X_i$ is. Each $X_i$ has mean $0$ and variance

$$\frac{1}{2r+1} \sum_{t=-r}^{r} t^2 = \frac{2}{2r+1} \cdot \frac{r(r+1)(2r+1)}{6} = \frac{r(r+1)}{3}.$$

[Variances](/variance/) of independent variables add, so the sum has variance $n r(r+1)/3$. $\square$

By the [central limit theorem](/central-limit-theorem/), the distribution of $(X_1 + \dots + X_n)/\sqrt{n r(r+1)/3}$ tends to the standard normal distribution as $n$ grows, which is why a few box passes approximate the Gaussian of $\sigma = \sqrt{n r(r+1)/3}$.

**Theorem 3 (repeated boxes under the wrap rule).** Under the wrap rule, $n$ passes of the box sum along each axis equal one direct 2D filter with the kernel $b^{*n}[u]\, b^{*n}[v]$, up to the factor $(2r+1)^{2n}$.

*Proof.* Under the wrap rule a pass is a circular convolution along its axis, the image extended periodically. Circular convolution along one axis is associative and commutative, and passes along different axes commute because they act on different indices of the periodic extension. So the $n$ row passes are one circular convolution with $b^{*n}$ along the rows, the $n$ column passes are one along the columns, and Theorem 1 with $a = b = b^{*n}$ joins them. $\blacksquare$

Under clamp, mirror or zero the passes do not compose this way, because the extension of an already filtered image differs from the filtered extension near the border; the two agree at pixels whose distance from the border is at least $nr$, where no pass reads outside the image.
