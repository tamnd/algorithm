---
title: The sum over the corners of one simplex equals the sum over the whole lattice
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. Arithmetic is exact (real-ram). Let $n \ge 1$, $F = (\sqrt{n+1} - 1)/n$ and $G = (1 - 1/\sqrt{n+1})/n$. For $x \in \mathbb{R}^n$ write $S(x) = x_1 + \dots + x_n$ and $\mathbf{1} = (1, \dots, 1)$. The skew is $\sigma(x) = x + F S(x) \mathbf{1}$ and the unskew is $\tau(y) = y - G S(y) \mathbf{1}$. For each $k \in \mathbb{Z}^n$ let $g_k$ be its hashed gradient, and let the kernel of $k$ at $x$ be
$$T_k(x) = \max(0,\, r^2 - |x - \tau(k)|^2)^4 \; g_k \cdot (x - \tau(k)).$$
The full noise is $N(x) = \sum_{k \in \mathbb{Z}^n} T_k(x)$. Lines L5 to L8 sum $T_k$ only over the $n + 1$ corners that lines L1 to L4 select. We prove that for $r^2 \le \tfrac12$ the two sums are equal.

**Lemma 1 (the skew and the unskew are inverse).** $\tau(\sigma(x)) = x$.

*Proof.* $S(\sigma(x)) = (1 + nF) S(x)$, so $\tau(\sigma(x)) = x + F S(x) \mathbf{1} - G (1 + nF) S(x) \mathbf{1}$. Now $1 + nF = \sqrt{n+1}$ and $G \sqrt{n+1} = (\sqrt{n+1} - 1)/n = F$. So the two terms cancel. $\square$

**Lemma 2 (the distance in skewed coordinates).** For $e \in \mathbb{R}^n$, $|\tau(e)|^2 = |e|^2 - S(e)^2/(n+1)$. Equivalently, if $w = (e_1, \dots, e_n, 0) \in \mathbb{R}^{n+1}$ and $\bar w$ is the mean of its $n + 1$ entries, then $|\tau(e)|^2 = \sum_{i=1}^{n+1} (w_i - \bar w)^2 = \min_{c \in \mathbb{R}} \sum_{i=1}^{n+1} (w_i - c)^2$.

*Proof.* $|e - G S \mathbf{1}|^2 = |e|^2 - 2 G S^2 + n G^2 S^2$ with $S = S(e)$. Put $a = nG = 1 - 1/\sqrt{n+1}$. Then $2G - nG^2 = (2a - a^2)/n = (1 - (1 - a)^2)/n = (1 - \tfrac{1}{n+1})/n = \tfrac{1}{n+1}$. For the second form, $\bar w = S/(n+1)$, and $\sum (w_i - \bar w)^2 = \sum w_i^2 - (n+1) \bar w^2 = |e|^2 - S^2/(n+1)$. The mean minimizes the sum of squares. $\square$

The second form does not change if the same constant is added to all $n + 1$ entries of $w$. We use this below.

**Lemma 3 (the chosen corners).** Let $y = \sigma(x)$, $k = \lfloor y \rfloor$ and $f = y - k \in [0, 1)^n$, as in lines L1 and L2. Let $\pi$ be the order of line L3, so $f_{\pi(1)} \ge \dots \ge f_{\pi(n)}$. The corners of line L4 are $c_m = k + \sum_{j \le m} e_{\pi(j)}$ for $m = 0, \dots, n$. Then $y$ is the convex combination $\sum_m \lambda_m c_m$ with $\lambda_0 = 1 - f_{\pi(1)}$, $\lambda_m = f_{\pi(m)} - f_{\pi(m+1)}$ for $0 < m < n$, and $\lambda_n = f_{\pi(n)}$.

*Proof.* The weights are nonnegative by the order and sum to 1 by telescoping. Coordinate $\pi(j)$ of $\sum_m \lambda_m c_m$ is $k_{\pi(j)} + \sum_{m \ge j} \lambda_m = k_{\pi(j)} + f_{\pi(j)}$, again by telescoping. $\square$

So by Lemma 1, $x = \tau(y)$ lies in the simplex with the vertices $\tau(c_m)$, and the code test `test_point_lies_in_chosen_simplex` checks the weights.

**Lemma 4 (every other lattice point is far).** Let $q \in \mathbb{Z}^n$ with $q - k \notin \{c_0 - k, \dots, c_n - k\}$. Then $|x - \tau(q)|^2 \ge \tfrac12$.

*Proof.* Let $z = q - k \in \mathbb{Z}^n$. By Lemma 1 and linearity, $x - \tau(q) = \tau(y - q) = \tau(f - z)$. Let $w \in \mathbb{R}^{n+1}$ have $w_i = f_i - z_i$ for $i \le n$ and $w_{n+1} = 0$. Extend $f$ and $z$ by $f_{n+1} = 0$ and $z_{n+1} = 0$, so that $w = f - z$ in $\mathbb{R}^{n+1}$ with $f \in [0, 1)^{n+1}$.

Suppose first that some pair has $w_i - w_j \ge 1$. By Lemma 2, $|\tau(f - z)|^2 = \min_c \sum (w_l - c)^2 \ge \min_c ((w_i - c)^2 + (w_j - c)^2) = (w_i - w_j)^2/2 \ge \tfrac12$.

So it is enough to show: if $|w_i - w_j| < 1$ for all $i, j$, then $z$ is one of the corners $c_m - k$. Assume this. For each $i$, $w_i \in [-z_i, 1 - z_i)$. If $z_j \ge z_i + 2$, then $w_i - w_j > -z_i - 1 + z_j \ge 1$, which is false. So the values $z_i$ take at most two consecutive integers, $b$ and $b + 1$. If $z_i = b + 1$ and $z_j = b$, then $w_j - w_i = f_j - f_i + 1$, so $f_j < f_i$ by the assumption. So the set $U = \{i : z_i = b + 1\}$ is an upper set of $f$: every $i$ in $U$ has a strictly larger $f_i$ than every $j$ not in $U$. Since $f_{n+1} = 0$ is the smallest entry and $z_{n+1} = 0$, either $n + 1 \notin U$ and $b = 0$, or $U$ holds all indices and $b + 1 = 0$, so $z = 0$ in the first $n$ entries. In the second case $z = c_0 - k$. In the first case $U \subseteq \{1, \dots, n\}$ is a set of indices whose $f$ values are strictly larger than all others. An order $\pi$ that sorts $f$ in decreasing order, with any rule for ties, lists such a set first, because ties cannot cross the boundary of $U$. So $U = \{\pi(1), \dots, \pi(m)\}$ with $m = |U|$, and $z = c_m - k$. $\square$

**Theorem 1 (the corner sum is the noise).** If $r^2 \le \tfrac12$, then for every $x$ the sum of lines L5 to L8 equals $N(x) = \sum_{q \in \mathbb{Z}^n} T_q(x)$.

*Proof.* The sum of lines L5 to L8 is $\sum_{m=0}^{n} T_{c_m}(x)$, and line L7 skips exactly the terms whose factor $\max(0, \cdot)$ is 0. For every other lattice point $q$, Lemma 4 gives $|x - \tau(q)|^2 \ge \tfrac12 \ge r^2$, so $T_q(x) = 0$. $\square$

The bound $\tfrac12$ is reached. In 2D, $\tau$ maps the unit square to two equilateral triangles of side $\sqrt{2/3}$, whose height is $\sqrt{1/2}$. At the midpoint of the diagonal edge, the corner of the other triangle is at the distance $\sqrt{1/2}$. In any dimension, take $f = (\tfrac12, \tfrac12, 0, \dots, 0)$. Line L3 puts one of the first two axes first, and the unit step $z = e_j$ along the other one is not a corner. Its $w$ is $\pm \tfrac12$ in the first two entries and 0 elsewhere, so the squared distance is exactly $\tfrac12$. With a larger radius that point would add a term that the corner sum drops. The code test `test_larger_radius_breaks_corner_sum` measures such a difference with $r^2 = 0.6$ in 3D.

**Theorem 2 (smoothness and zeros).** For $r^2 \le \tfrac12$, $N$ is $C^3$ on $\mathbb{R}^n$, and $N(\tau(q)) = 0$ for every $q \in \mathbb{Z}^n$.

*Proof.* The map $t \mapsto \max(0, t)^4$ is $C^3$: on $t > 0$ its first three derivatives $4t^3$, $12 t^2$ and $24 t$ tend to 0 as $t \to 0$, which match the zero function on $t < 0$. The map $x \mapsto r^2 - |x - \tau(q)|^2$ is a polynomial, and $g_q \cdot (x - \tau(q))$ is linear. So each $T_q$ is $C^3$. On a bounded set only finitely many $T_q$ are not zero, so $N$ is $C^3$. At $x = \tau(q)$, the term $T_q$ has the factor $g_q \cdot 0 = 0$. Every other lattice point $q'$ has $q' - q \ne 0$, and with $f = 0$ every entry of $f$ ties, so the only upper set of Lemma 4 that is allowed is the empty one, and $z = q' - q$ is not a corner. So $|\tau(q) - \tau(q')|^2 \ge \tfrac12 \ge r^2$ and $T_{q'} = 0$. $\square$

By Theorem 1, the value of the code does not depend on how line L3 breaks ties, and it is the same function on both sides of a face of a simplex. So the corner sum is continuous, although the set of corners changes at the faces.

**Cost.** Lines L1 and L2 take $O(n)$. The sort of line L3 takes $O(n \log n)$ comparisons. Line L4 makes $n + 1$ corners, and for each corner lines L6 to L8 take $O(n)$: the unskew, the squared distance, the dot product, and $n$ table lookups for the hash. The total is $O(n^2)$ per point, against $\Theta(n 2^n)$ for the $2^n$ corners of a cube cell.
