---
title: The Bayer matrix is a permutation, and ordered dithering turns on the nearest count of pixels in every tile
proves: [correctness]
status: full
---

Let $n = 2^K$. For $0 \le x, y < n$, write $x = \sum_{i < K} x_i 2^i$ and $y = \sum_{i < K} y_i 2^i$ with binary digits $x_i, y_i \in \{0, 1\}$. Let $\delta(a, b) = 2(a \oplus b) + b$, so that $\delta(0, 0) = 0$, $\delta(1, 0) = 2$, $\delta(0, 1) = 3$ and $\delta(1, 1) = 1$. These are the entries $D(a, b)$ of line L3, and $\delta$ is a bijection from $\{0, 1\}^2$ onto $\{0, 1, 2, 3\}$.

**Claim 1 (closed form).** The matrix $M_n$ built by lines L1 to L3 is

$$
M_n(x, y) = \sum_{i = 0}^{K - 1} \delta(x_i, y_i)\, 4^{K - 1 - i}, \tag{1}
$$

so the lowest binary digits of $x$ and $y$ give the highest base-4 digit of the index.

*Proof.* By induction on $K$. For $K = 0$, both sides are 0. Let $s = 2^{K - 1}$ and assume (1) for $M_s$. For $0 \le x, y < 2s$, the numbers $x \bmod s$ and $y \bmod s$ have the digits $x_i, y_i$ for $i < K - 1$, and $\lfloor x/s \rfloor = x_{K - 1}$, $\lfloor y/s \rfloor = y_{K - 1}$. Line L3 gives

$$
M_{2s}(x, y) = 4 \sum_{i = 0}^{K - 2} \delta(x_i, y_i)\, 4^{K - 2 - i} + \delta(x_{K - 1}, y_{K - 1}),
$$

which is (1). $\square$

**Claim 2 (each threshold once).** $M_n$ holds each of $0, 1, \ldots, n^2 - 1$ exactly once.

*Proof.* By (1), $M_n(x, y)$ is the number whose base-4 digits are $\delta(x_0, y_0), \ldots, \delta(x_{K - 1}, y_{K - 1})$. The map from $(x, y)$ to the $K$ pairs of digits is a bijection, $\delta$ is a bijection on each pair, and the base-4 digits determine the number. So $(x, y) \mapsto M_n(x, y)$ is a bijection from $[0, n)^2$ onto $[0, 4^K) = [0, n^2)$. $\square$

**Claim 3 (count per tile).** Let the image have the constant value $g \in [0, 1]$, and let $c$ be the number of ones in an aligned $n \times n$ tile. Then

$$
c = \left\lceil g n^2 - \tfrac{1}{2} \right\rceil, \qquad |c - g n^2| \le \tfrac{1}{2},
$$

and $c = k$ when $g = k/n^2$ for an integer $0 \le k \le n^2$.

*Proof.* An aligned tile covers each position $(x \bmod n, y \bmod n)$ once, so by Claim 2 its thresholds of line L4 are $(m + 1/2)/n^2$ for $m = 0, \ldots, n^2 - 1$, each once. By line L6, the pixel with index $m$ is 1 if and only if $g > (m + 1/2)/n^2$, that is, $m < g n^2 - 1/2$. So $c$ is the number of integers $m \in [0, n^2)$ below $t = g n^2 - 1/2$. Since $t \in [-1/2, n^2 - 1/2]$, these integers are $0, 1, \ldots, \lceil t \rceil - 1$, and $c = \lceil t \rceil$. From $t \le \lceil t \rceil < t + 1$ follows $g n^2 - 1/2 \le c < g n^2 + 1/2$. For $g = k/n^2$, $t = k - 1/2$ and $\lceil t \rceil = k$. $\square$

The rounding of Claim 3 sends a half down: for $g n^2 = k + 1/2$, $c = k$, because a value equal to a threshold stays off.

**Claim 4 (nested patterns).** If $g \le g'$, every pixel of a tile that is 1 for the gray $g$ is also 1 for the gray $g'$.

*Proof.* The pixel with threshold $T$ is 1 for $g$ when $g > T$, and then $g' \ge g > T$. $\square$

**Claim 5 (lattice levels).** For $0 \le j \le K$, the indices below $n^2 / 4^j$ are exactly the positions with $x$ and $y$ both multiples of $2^j$.

*Proof.* By (1), $M_n(x, y) < 4^{K - j}$ if and only if its $j$ highest base-4 digits are 0, that is, $\delta(x_i, y_i) = 0$ for $i < j$. Since $\delta(a, b) = 0$ only for $a = b = 0$, this holds if and only if $x_i = y_i = 0$ for $i < j$, that is, $2^j$ divides both $x$ and $y$. $\square$

By Claims 3 and 5, the gray $4^{-j}$ turns on the square lattice of spacing $2^j$, and the gray $1/2$ turns on the indices below $n^2/2$, whose highest digit is 0 or 1, that is, $x_0 \oplus y_0 = 0$: a checkerboard. By Claim 4, each gray between two such levels adds pixels to the lattice of the lower one.
