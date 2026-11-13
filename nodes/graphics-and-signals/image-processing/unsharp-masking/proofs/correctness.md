---
title: Without a threshold UNSHARP-MASK equals direct filtering with the kernel (1 + λ)δ − λK, keeps constants, and has the gain 1 + λ(1 − K̂)
proves: [correctness]
status: full
---

Let $f$ have $W \ge 1$ columns and $H \ge 1$ rows, and let $\tilde f$ be its extension by the border rule: $\tilde f(i, j) = f[\mathrm{ext}(j, H)][\mathrm{ext}(i, W)]$, or $0$ when the rule gives no pixel. Every rule is the identity inside the image, so $\tilde f(x, y) = f[y][x]$ for every pixel $(x, y)$. Let $K[u][v]$, $|u|, |v| \le R$, be the blur kernel, and $b(x, y) = \sum_{u, v} K[u][v]\, \tilde f(x + u, y + v)$ the blurred image of line L1. For a separable $K = k[u]\,k[v]$, two passes compute this $b$ with the same border rule, as the [separable filter](/separable-filter/) page proves. Let $\delta[u][v]$ be $1$ at $(0, 0)$ and $0$ elsewhere.

**Lemma 1 (the impulse).** For every pixel, $\sum_{u, v} \delta[u][v]\, \tilde f(x + u, y + v) = f[y][x]$.

*Proof.* Only the term $u = v = 0$ is nonzero, and it is $\tilde f(x, y) = f[y][x]$ because $(x, y)$ is inside the image. $\square$

**Theorem 1 (one linear filter).** With $t = 0$ and no range, UNSHARP-MASK returns $g(x, y) = \sum_{u, v} C[u][v]\, \tilde f(x + u, y + v)$ with $C = (1 + \lambda)\delta - \lambda K$, the direct 2D filter of $f$ with the kernel $C$ and the same border rule.

*Proof.* With $t = 0$ the test $|d| \ge t$ of line L4 holds for every pixel, so line L4 sets $g = f + \lambda d$ with $d = f - b$ from line L3. Hence $g = (1 + \lambda) f - \lambda b$ at every pixel. By Lemma 1, $(1 + \lambda) f[y][x] = \sum_{u, v} (1 + \lambda)\delta[u][v]\, \tilde f(x + u, y + v)$, and by the definition of $b$, $\lambda b(x, y) = \sum_{u, v} \lambda K[u][v]\, \tilde f(x + u, y + v)$. The difference of the two finite sums is the sum with $C$. $\square$

**Corollary 1 (constants).** If $\sum_{u, v} K[u][v] = 1$ and the rule is clamp, mirror or wrap, a constant image $f \equiv c$ gives $g \equiv c$.

*Proof.* Every value of $\tilde f$ is $c$, so $g(x, y) = c \sum_{u, v} C[u][v] = c\,((1 + \lambda) - \lambda) = c$. $\square$

**Theorem 2 (the gain).** Under the wrap rule, let $\hat K(\omega_1, \omega_2) = \sum_{u, v} K[u][v]\, e^{i(\omega_1 u + \omega_2 v)}$ for the frequencies $\omega_1 \in 2\pi\mathbb{Z}/W$ and $\omega_2 \in 2\pi\mathbb{Z}/H$. The complex wave $e_\omega(x, y) = e^{i(\omega_1 x + \omega_2 y)}$ is mapped to $(1 + \lambda(1 - \hat K(\omega)))\, e_\omega$. If $K$ is symmetric, $K[-u][-v] = K[u][v]$, nonnegative and sums to 1, the gain is real, lies in $[1, 1 + 2\lambda]$ for $\lambda \ge 0$, and equals 1 at $\omega = 0$.

*Proof.* Under the wrap rule $\tilde e_\omega(x + u, y + v) = e_\omega(x + u, y + v)$, because $e_\omega$ has the periods $W$ and $H$. So by Theorem 1,

$$g(x, y) = \sum_{u, v} C[u][v]\, e^{i(\omega_1 (x+u) + \omega_2 (y+v))} = e_\omega(x, y) \sum_{u, v} C[u][v]\, e^{i(\omega_1 u + \omega_2 v)} = e_\omega(x, y)\,(1 + \lambda - \lambda \hat K(\omega)).$$

For a symmetric kernel, the terms of $(u, v)$ and $(-u, -v)$ pair into $K[u][v] \cdot 2\cos(\omega_1 u + \omega_2 v)$, so $\hat K(\omega) = \sum_{u, v} K[u][v] \cos(\omega_1 u + \omega_2 v)$ is real. With $K \ge 0$ and $\sum K = 1$, it is an average of cosines, so $-1 \le \hat K(\omega) \le 1$, and $1 - \hat K(\omega) \in [0, 2]$. At $\omega = 0$, $\hat K(0) = \sum K = 1$, and the gain is 1. $\blacksquare$

With a threshold $t > 0$, line L4 keeps $g(p) = f(p)$ at the pixels with $|d(p)| < t$ and sets $g(p)$ as in Theorem 1 at the others, so the output agrees with the linear filter exactly on the pixels it changes. Clipping at line L5 replaces each value $v$ by $\min(\mathit{hi}, \max(\mathit{lo}, v))$ and changes no value already in the range.
