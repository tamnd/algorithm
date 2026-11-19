---
title: ROPE returns R_pos x, the rotations keep norms and compose, and the score of a query at m and a key at n equals q^T R_(n-m) k, so it depends on the positions only through n - m
proves: [correctness]
status: full
---

We use the notation of the page. $d$ is even, $\theta_i = 10000^{-2i/d}$ for $i = 0, \ldots, d/2 - 1$, and for an angle $\phi$

$$G(\phi) = \begin{pmatrix} \cos\phi & -\sin\phi \\ \sin\phi & \cos\phi \end{pmatrix}.$$

$R_m$ is the $d \times d$ block-diagonal matrix with blocks $G(m\theta_0), \ldots, G(m\theta_{d/2-1})$, acting on the pairs $(x_{2i}, x_{2i+1})$. Positions $m$ and $n$ are any real numbers.

**Lemma 1 (the procedure).** ROPE$(x, pos, d)$ returns $R_{pos}\, x$.

*Proof.* The loop at line L1 visits each $i$ once. Line L2 sets $\theta_i$, line L3 computes $c = \cos(pos\,\theta_i)$ and $s = \sin(pos\,\theta_i)$, and lines L4 and L5 write $(y_{2i}, y_{2i+1}) = (c x_{2i} - s x_{2i+1},\; s x_{2i} + c x_{2i+1})$, which is $G(pos\,\theta_i)$ applied to the pair. The pairs are disjoint and cover all coordinates, and $R_{pos}$ acts on each pair by its own block. $\square$

**Lemma 2 (rotations).** For all angles $\alpha$ and $\beta$, $G(\alpha)^\top = G(-\alpha)$, $G(\alpha)^\top G(\alpha) = I$ and $G(\alpha) G(\beta) = G(\alpha + \beta)$.

*Proof.* Transposing $G(\alpha)$ swaps the two off-diagonal entries, which gives $\begin{pmatrix} \cos\alpha & \sin\alpha \\ -\sin\alpha & \cos\alpha \end{pmatrix} = G(-\alpha)$, since cosine is even and sine is odd. For the product,

$$G(\alpha) G(\beta) = \begin{pmatrix} \cos\alpha\cos\beta - \sin\alpha\sin\beta & -(\cos\alpha\sin\beta + \sin\alpha\cos\beta) \\ \sin\alpha\cos\beta + \cos\alpha\sin\beta & \cos\alpha\cos\beta - \sin\alpha\sin\beta \end{pmatrix} = G(\alpha + \beta)$$

by the angle-sum formulas. Then $G(\alpha)^\top G(\alpha) = G(-\alpha) G(\alpha) = G(0) = I$. $\square$

**Corollary 3.** $R_m^\top = R_{-m}$, $R_a R_b = R_{a+b}$, and $\lVert R_m x \rVert = \lVert x \rVert$.

*Proof.* Block-diagonal matrices with the same block sizes are transposed and multiplied block by block, and block $i$ of $R_a R_b$ is $G(a\theta_i) G(b\theta_i) = G((a + b)\theta_i)$ by Lemma 2. For the norm, $\lVert R_m x \rVert^2 = x^\top R_m^\top R_m x = x^\top R_0 x = x^\top x$, since $R_0 = I$. $\square$

**Theorem 4 (relative position).** For all $q, k \in \mathbb{R}^d$ and positions $m, n$,

$$\mathrm{ROPE}(q, m) \cdot \mathrm{ROPE}(k, n) = q^\top R_{n - m}\, k.$$

In particular, for every real $t$, the score of $q$ at $m + t$ and $k$ at $n + t$ equals the score of $q$ at $m$ and $k$ at $n$.

*Proof.* By Lemma 1 the left side is $(R_m q)^\top (R_n k) = q^\top R_m^\top R_n k$. By Corollary 3, $R_m^\top R_n = R_{-m} R_n = R_{n - m}$. The right side depends on $m$ and $n$ only through $n - m$, and $(n + t) - (m + t) = n - m$. $\square$

**Complex form.** Identify the pair $(x_{2i}, x_{2i+1})$ with $z_i = x_{2i} + \mathrm{i}\, x_{2i+1}$. Then $G(\phi)$ maps $z_i$ to $z_i e^{\mathrm{i}\phi}$, because $(a + \mathrm{i} b)(\cos\phi + \mathrm{i}\sin\phi) = (a\cos\phi - b\sin\phi) + \mathrm{i}(a\sin\phi + b\cos\phi)$. For two pairs $u$ and $v$ seen as complex numbers, the real dot product is $\operatorname{Re}(u \bar v)$. So the score is

$$\sum_i \operatorname{Re}\big(q_i e^{\mathrm{i} m\theta_i}\, \overline{k_i e^{\mathrm{i} n\theta_i}}\big) = \sum_i \operatorname{Re}\big(q_i \overline{k_i}\, e^{\mathrm{i}(m - n)\theta_i}\big),$$

which is Theorem 4 again in another form.

**Bound.** By the Cauchy-Schwarz inequality and Corollary 3, $|q^\top R_{n-m} k| \le \lVert q \rVert \lVert R_{n-m} k \rVert = \lVert q \rVert \lVert k \rVert$ for every offset. $\blacksquare$

The theorem is about the score before the softmax and the $1/\sqrt{d_k}$ factor; both act on the scores alone, so the attention weights of a query over keys also depend on the positions only through the offsets. With a causal mask, the mask itself depends only on the sign of $n - m$, so the property holds there too.
