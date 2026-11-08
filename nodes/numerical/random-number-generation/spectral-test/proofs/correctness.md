---
title: The spectral test computes the largest spacing 1/nu_t of hyperplanes covering the LCG lattice
proves: [correctness]
status: full
---

Fix a modulus $m \ge 2$, a multiplier $a$ with $\gcd(a, m) = 1$, and a dimension $t \ge 2$. Put $w = (1, a, a^2, \ldots, a^{t-1})$ and

$$\Lambda_t = \mathbb{Z}^t + \{ x w / m : x \in \mathbb{Z} \}, \qquad L^*_t = \{ s \in \mathbb{Z}^t : s \cdot w \equiv 0 \pmod m \}.$$

For the LCG $x_{n+1} = (a x_n + c) \bmod m$, the tuple $(x_n, \ldots, x_{n+t-1})$ equals $x_n w + \beta \pmod m$ with the fixed vector $\beta = c\,(0, 1, 1 + a, \ldots, 1 + a + \cdots + a^{t-2})$. So every normalized tuple $u_n = (x_n, \ldots, x_{n+t-1})/m$ lies in the shifted lattice $\Lambda_t + \beta/m$, and when $c = 0$ in $\Lambda_t$ itself. Define $\nu_t = \min \{ |s| : s \in L^*_t, s \ne 0 \}$.

**Lemma 1 (the dual lattice).** $L^*_t$ is the dual lattice of $\Lambda_t$: $\Lambda_t^* = \{ y \in \mathbb{R}^t : y \cdot \lambda \in \mathbb{Z} \text{ for all } \lambda \in \Lambda_t \} = L^*_t$. Its determinant is $m$.

*Proof.* If $y \in \Lambda_t^*$, then $y \cdot e_i \in \mathbb{Z}$ for every unit vector, so $y \in \mathbb{Z}^t$, and $y \cdot w / m \in \mathbb{Z}$, so $y \in L^*_t$. Conversely, for $s \in L^*_t$, $s \cdot (z + x w/m) = s \cdot z + x (s \cdot w)/m \in \mathbb{Z}$. The rows $(m, 0, \ldots, 0)$ and $e_j - (a^{j-1} \bmod m) e_1$ for $j = 2, \ldots, t$ (line L2) lie in $L^*_t$, and every $s \in L^*_t$ equals $\sum_{j \ge 2} s_j (e_j - (a^{j-1} \bmod m) e_1) + k (m, 0, \ldots, 0)$ for an integer $k$, because $s_1 + \sum_{j \ge 2} s_j a^{j-1} \equiv 0 \pmod m$. So they form a basis, which is triangular with diagonal $m, 1, \ldots, 1$, so the determinant is $m$. $\square$

**Theorem 1 (hyperplanes).** (a) For every non-zero $s \in L^*_t$, the points of $\Lambda_t + \beta/m$ lie on the parallel hyperplanes $\{ u : s \cdot u = k + s \cdot \beta / m \}$, $k \in \mathbb{Z}$, and adjacent hyperplanes are $1/|s|$ apart. (b) Conversely, if a family of parallel hyperplanes with spacing $d$ contains every point of $\Lambda_t + \beta/m$, then $d \le 1/\nu_t$. Hence $1/\nu_t$ is the largest possible spacing, attained by a shortest $s$.

*Proof.* (a) By Lemma 1, $s \cdot \lambda \in \mathbb{Z}$ for $\lambda \in \Lambda_t$. The hyperplanes $s \cdot u = k$ and $s \cdot u = k + 1$ are $1/|s|$ apart. (b) Write the family as $\{u : n \cdot u \in \gamma + d\mathbb{Z}\}$ with $|n| = 1$. For $\lambda \in \Lambda_t$, both $\beta/m$ and $\lambda + \beta/m$ lie on the family, so $n \cdot \lambda \in d \mathbb{Z}$. Then $y = n / d$ satisfies $y \cdot \lambda \in \mathbb{Z}$ for all $\lambda$, so $y \in \Lambda_t^* = L^*_t$ and $y \ne 0$. Hence $1/d = |y| \ge \nu_t$. $\square$

In the unit cube, let $P$ and $N$ be the sums of the positive entries of $s$ and of the absolute values of its negative entries. For $u \in [0, 1)^t$, $s \cdot u$ lies in $[-N, P]$, and strictly inside it at an end where the corresponding entries are non-zero, so when $s$ has entries of both signs at most $P + N - 1 = |s_1| + \cdots + |s_t| - 1$ of the hyperplanes of (a) (taking $\beta = 0$) meet $[0, 1)^t$. For RANDU, $c = 0$ and $s = (9, -6, 1)$, so $9 u_1 - 6 u_2 + u_3$ is an integer in $\{-5, \ldots, 9\}$: the 15 planes of Marsaglia's observation.

**Lemma 2 (Hermite bound).** $\nu_t^2 \le \gamma_t\, m^{2/t}$, where $\gamma_t$ is Hermite's constant, with $\gamma_t^t = 4/3, 2, 4, 8, 64/3$ for $t = 2, \ldots, 6$.

*Proof.* By definition of Hermite's constant, every lattice of determinant $D$ in $\mathbb{R}^t$ has a non-zero vector of squared length at most $\gamma_t D^{2/t}$; apply it with $D = m$ (Lemma 1). The values of $\gamma_t$ for $t \le 8$ are classical (Lagrange, Gauss, Korkine and Zolotarev, Blichfeldt). $\square$

So $\mu_t = \pi^{t/2} \nu_t^t / (\Gamma(t/2 + 1)\, m)$ (line L5), the volume of the ball of radius $\nu_t$ divided by $\det L^*_t$, is a normalized figure of merit, bounded above by $\pi^{t/2} \gamma_t^{t/2} / \Gamma(t/2 + 1)$.

**Theorem 2 (the algorithm computes $\nu_t$).** SPECTRAL-TEST returns, for each $t$, the exact value $\nu_t^2$ and a vector $s \in L^*_t$ with $|s| = \nu_t$.

*Proof.* Line L2 builds a basis of $L^*_t$ (Lemma 1). Line L3 changes it only by swapping rows and subtracting integer multiples of one row from another, which are unimodular operations, so the rows still form a basis of $L^*_t$; LLL reduction serves only to make the next step fast. Line L4 enumerates exactly. Let $b_1^*, \ldots, b_t^*$ be the Gram-Schmidt vectors of the basis $b_1, \ldots, b_t$ with coefficients $\mu_{jk}$, all computed in exact rational arithmetic. For $v = \sum_i x_i b_i$,

$$|v|^2 = \sum_{k=1}^{t} \Bigl( x_k + \sum_{j > k} x_j \mu_{jk} \Bigr)^2 |b_k^*|^2,$$

since the $b_k^*$ are orthogonal. All terms are non-negative, so if $|v|^2 \le R$, then for every $k$ the partial sum over indices $\ge k$ is at most $R$. The search fixes $x_t, x_{t-1}, \ldots$ in turn and at level $k$ tries every integer $x_k$ with $(x_k - c_k)^2 |b_k^*|^2 \le R - (\text{partial sum above } k)$, where $c_k = -\sum_{j>k} x_j \mu_{jk}$; it tries a range of integers that contains all of them. $R$ starts as the squared length of a basis vector, an upper bound for $\nu_t^2$, and is lowered whenever a shorter non-zero vector is found, so it never increases. Suppose a non-zero $v \in L^*_t$ had $|v|^2 < R_{\text{final}}$. Each partial sum of $v$ is at most $|v|^2$, which is below every value that $R$ takes, so no level of $v$'s branch was pruned and $v$ was examined; at that moment $R$ was lowered to at most $|v|^2 < R_{\text{final}}$, a contradiction. So $R_{\text{final}} = \nu_t^2$, and the stored vector attains it. Every candidate is $\sum x_i b_i$ with integer $x_i$, so it lies in $L^*_t$. $\blacksquare$

The tests compare $\nu_2^2$ and $\nu_3^2$ with exhaustive search for every multiplier of three small moduli. The search box is $[-\lfloor\sqrt{2m}\rfloor, \lfloor\sqrt{2m}\rfloor]^t$: by Lemma 2, $\nu_t^2 \le \gamma_t m^{2/t} \le 2m$ for $t \ge 2$, and each coordinate of a vector is at most its length. They also compare $\nu_2^2$ with Lagrange-Gauss reduction, check RANDU's $\nu_3^2 = 118$, and check the Hermite bound for several published multipliers.
