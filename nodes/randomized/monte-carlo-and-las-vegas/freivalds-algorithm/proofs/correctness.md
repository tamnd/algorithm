---
title: Freivalds' algorithm has one-sided error at most 2^-k
proves: [correctness]
status: full
---

We write $D = AB - C$, an $n \times p$ matrix over the ring $R$ of the entries. One round is lines L2 to L6 with one vector $r$. Lines L3 to L5 compute $y = A(Br)$ and $z = Cr$, and by the associative law $y - z = (AB)r - Cr = Dr$. So a round returns NOT-EQUAL exactly when $Dr \ne 0$.

**Lemma 1 (no false "not equal").** If $AB = C$, the algorithm returns EQUAL.

*Proof.* Then $D = 0$, so $Dr = 0$ for every $r$, and line L6 never returns. After $k$ rounds, line L7 returns EQUAL. $\square$

**Lemma 2 (a "not equal" is always right).** If line L6 returns NOT-EQUAL, then $AB \ne C$.

*Proof.* Line L6 returns only when $Dr \ne 0$ for the current $r$, and then $D \ne 0$. $\square$

**Lemma 3 (one round, bits).** Let $R$ be any ring and let $r$ be uniform on $\{0, 1\}^p$. If $D \ne 0$, then $\Pr[Dr = 0] \le 1/2$.

*Proof.* Pick $i, j$ with $D_{ij} \ne 0$. Let $\varphi$ map $r$ to the vector $r'$ that differs from $r$ only in coordinate $j$ ($r'_j = 1 - r_j$). Then $\varphi$ is a bijection of $\{0, 1\}^p$ with $\varphi(\varphi(r)) = r$ and $\varphi(r) \ne r$, so it splits $\{0, 1\}^p$ into $2^{p-1}$ pairs $\{r, r'\}$. In a pair with $r_j = 0$ and $r'_j = 1$,

$$(Dr')_i - (Dr)_i = D_{ij}(r'_j - r_j) = D_{ij} \ne 0.$$

So $(Dr)_i$ and $(Dr')_i$ are not both 0, and at most one vector of each pair has $Dr = 0$. Hence at most $2^{p-1}$ of the $2^p$ vectors have $Dr = 0$. This uses only subtraction, so it holds in every ring. $\square$

**Lemma 4 (one round, a larger set).** Let $R$ be an integral domain, $S \subseteq R$ a finite set, and $r$ uniform on $S^p$. If $D \ne 0$, then $\Pr[Dr = 0] \le 1/|S|$.

*Proof.* Pick $i, j$ with $D_{ij} \ne 0$. Fix all coordinates of $r$ except $r_j$, and write $(Dr)_i = D_{ij} r_j + c$, where $c$ does not depend on $r_j$. If two values $u \ne v$ of $S$ both gave 0, then $D_{ij}(u - v) = 0$ with both factors nonzero, which is impossible in an integral domain. So at most one value of $r_j$ makes $(Dr)_i = 0$, and the conditional probability is at most $1/|S|$ for every choice of the other coordinates. Averaging over them gives $\Pr[(Dr)_i = 0] \le 1/|S|$, and $\{Dr = 0\} \subseteq \{(Dr)_i = 0\}$. This is the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) for the polynomial $\sum_j D_{ij} x_j$ of degree 1. $\square$

**Theorem.** If $AB = C$, FREIVALDS$(A, B, C, k)$ returns EQUAL. If $AB \ne C$, it returns EQUAL with probability at most $2^{-k}$ when $r$ is uniform on $\{0, 1\}^p$ (any ring), and at most $|S|^{-k}$ when $r$ is uniform on $S^p$ (an integral domain).

*Proof.* The first claim is Lemma 1. For the second, the algorithm returns EQUAL only if all $k$ rounds have $Dr = 0$. Line L2 draws the $k$ vectors independently, so this probability is the product of the $k$ probabilities of one round, each at most $1/2$ by Lemma 3, or at most $1/|S|$ by Lemma 4. $\blacksquare$

**Tightness.** Both bounds are reached. If $D$ has exactly one nonzero entry, at $(i, j)$, then over an integral domain $Dr = 0$ if and only if $r_j = 0$. This has probability exactly $1/2$ for bits, and exactly $1/|S|$ for a set $S$ that contains 0.

**Over a ring with zero divisors, Lemma 4 fails.** Over $\mathbb{Z}/2^{64}\mathbb{Z}$ with $D = (2^{63})$ and $S = \{0, 1, 2, 3\}$, every even $r$ gives $Dr = 2^{64} r/2 \equiv 0$, so $\Pr[Dr = 0] = 1/2 > 1/|S|$. Lemma 3 still holds.
