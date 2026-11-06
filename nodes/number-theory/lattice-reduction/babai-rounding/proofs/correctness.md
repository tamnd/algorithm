---
title: Babai rounding returns a lattice vector, decodes every error inside the dual box, and stays within a basis-dependent factor of the closest vector
proves: [correctness, termination, time.worst]
status: full
---

**Setting.** The input is $n \ge 1$ linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ of a matrix $B$, and a target $t \in \mathbb{Q}^m$. We write $L = L(B)$, $G = B B^T$ for the Gram matrix, and $D = G^{-1} B$ for the dual basis, with rows $d_1, \ldots, d_n$. They lie in $\operatorname{span}(L)$ and satisfy $\langle b_i, d_j \rangle = [i = j]$, because $B D^T = B B^T G^{-1} = I$. The nearest integer is $\lceil z \rfloor = \lfloor z + 1/2 \rfloor$, so $-1/2 \le z - \lceil z \rfloor < 1/2$, and $\lceil k + z \rfloor = k + \lceil z \rfloor$ for every integer $k$.

**Lemma 1 (the coordinates).** The vector $y$ computed at line L2 is $y_i = \langle t, d_i \rangle$. The point $p = \sum_i y_i b_i$ is the orthogonal projection of $t$ onto $\operatorname{span}(L)$.

*Proof.* Line L2 solves $G y = B t$. Since $G$ is a Gram matrix of independent vectors it is nonsingular, and $y = G^{-1} B t = D t$, that is $y_i = \langle d_i, t \rangle$. For each $j$, $\langle t - p, b_j \rangle = \langle t, b_j \rangle - (G y)_j = 0$, so $t - p$ is orthogonal to the span, and $p$ lies in it. $\square$

**Lemma 2 (the output is a lattice vector).** The output $v$ lies in $L$, and $x$ is its coefficient vector.

*Proof.* Line L3 makes every $x_i$ an integer, and line L4 sets $v = \sum_i x_i b_i = x B$. $\square$

**Lemma 3 (decoding).** Let $t = u + e$ with $u = z B \in L$ and $|\langle e, d_i \rangle| < 1/2$ for all $i$. Then the algorithm returns $x = z$ and $v = u$.

*Proof.* By Lemma 1, $y_i = \langle z B, d_i \rangle + \langle e, d_i \rangle = z_i + \varepsilon_i$ with $\varepsilon_i = \langle e, d_i \rangle$, since $\langle b_k, d_i \rangle = [k = i]$. As $|\varepsilon_i| < 1/2$, $\lceil \varepsilon_i \rfloor = 0$, so $x_i = \lceil z_i + \varepsilon_i \rfloor = z_i$. $\square$

By Cauchy-Schwarz, $|\langle e, d_i \rangle| \le \|e\| \|d_i\|$, so Lemma 3 applies whenever $\|e\| < 1 / (2 \max_i \|d_i\|)$.

**Lemma 4 (approximation).** Let $u$ be a lattice vector closest to $t$. Then

$$\|t - v\| \le \Big(1 + 2 \sum_{i=1}^n \|b_i\| \|d_i\|\Big) \|t - u\|.$$

*Proof.* Write $u = z B$ and $e = t - u$, and let $\varepsilon_i = \langle e, d_i \rangle$. As in Lemma 3, $y_i = z_i + \varepsilon_i$ and $x_i = z_i + \lceil \varepsilon_i \rfloor$. Hence $t - v = e - \sum_i \lceil \varepsilon_i \rfloor b_i$. We claim $|\lceil \varepsilon \rfloor| \le 2 |\varepsilon|$ for every rational $\varepsilon$. If $-1/2 \le \varepsilon < 1/2$, then $\lceil \varepsilon \rfloor = 0$. If $\varepsilon = 1/2$, then $\lceil \varepsilon \rfloor = 1 = 2 \varepsilon$. Otherwise $|\varepsilon| > 1/2$, and $|\lceil \varepsilon \rfloor| \le |\varepsilon| + 1/2 < 2 |\varepsilon|$. So, with the triangle inequality and Cauchy-Schwarz,

$$\|t - v\| \le \|e\| + \sum_i 2 |\varepsilon_i| \|b_i\| \le \|e\| + 2 \sum_i \|e\| \|d_i\| \|b_i\|,$$

which is the claim. $\square$

**Lemma 5 (distance from the projection).** With $p$ as in Lemma 1, $\|t - v\|^2 = \|t - p\|^2 + \|p - v\|^2$ and $\|p - v\| \le \tfrac12 \sum_i \|b_i\|$.

*Proof.* $t - p$ is orthogonal to the span and $p - v$ lies in it, which gives the first identity. Also $p - v = \sum_i (y_i - x_i) b_i$ with $|y_i - x_i| \le 1/2$, and the triangle inequality gives the bound. $\square$

**Termination and cost.** The algorithm has no loop beyond the fixed loops over indices, so it terminates. Line L1 computes $n^2$ inner products of length $m$, which is $O(n^2 m)$ arithmetic operations. Line L2 forms $B t$ in $O(n m)$ operations and solves an $n \times n$ system by Gauss-Jordan elimination in $O(n^3)$ operations. Line L3 takes $O(n)$ and line L4 takes $O(n m)$. The total is $O(n^2 m + n^3)$ arithmetic operations on rationals, and $O(n m)$ per further target once $D$ is stored.

**Theorem.** On every valid input the algorithm returns $x \in \mathbb{Z}^n$ and $v = x B \in L$ (Lemma 2). It returns the lattice vector $u$ whenever $t - u$ lies inside the box $|\langle t - u, d_i \rangle| < 1/2$ (Lemma 3), and in all cases $\|t - v\|$ is within the factor $1 + 2 \sum_i \|b_i\| \|d_i\|$ of the distance from $t$ to $L$ (Lemma 4). It uses $O(n^2 m + n^3)$ arithmetic operations. $\blacksquare$

**Remark (reduced bases).** For a basis that is LLL-reduced with $\delta = 3/4$, Babai (1986) proved that the factor can be bounded by $1 + 2n (9/2)^{n/2}$, a bound that depends only on $n$. That bound is cited, not proved here; the bound of Lemma 4 holds for every basis, and is small exactly when every $b_i$ is short compared with the inverse of the matching dual vector, that is, when the basis is close to orthogonal.
