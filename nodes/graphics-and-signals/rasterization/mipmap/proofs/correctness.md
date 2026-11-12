---
title: Every mipmap level holds the block means of the texture, the levels need fewer than 4/3 of the base storage when the texture is square, and the trilinear lookup is a continuous convex combination
proves: [correctness]
status: full
---

Let the texture $T$ have $W = 2^a$ columns and $H = 2^b$ rows, with $L = \max(a, b)$. Level $k$ of the mipmap has $W_k = 2^{\max(a-k, 0)}$ columns and $H_k = 2^{\max(b-k, 0)}$ rows. Put $w_k = W / W_k = 2^{\min(k, a)}$ and $h_k = H / H_k = 2^{\min(k, b)}$, and define the block of texel $(s, t)$ of level $k$ as the set of base texels

$$B_k(s, t) = \{(s', t') : s w_k \le s' < (s+1) w_k,\ t h_k \le t' < (t+1) h_k\}.$$

For each $k$, the blocks $B_k(s, t)$ with $0 \le s < W_k$ and $0 \le t < H_k$ partition the base grid into $W_k H_k$ sets of $w_k h_k$ texels each.

**Lemma 1 (block means).** After BUILD, $M_k[s, t] = \frac{1}{w_k h_k} \sum_{(s', t') \in B_k(s, t)} T[s', t']$ for every level $k$ and texel $(s, t)$.

*Proof.* By induction on $k$. For $k = 0$, $w_0 = h_0 = 1$, the block is the single texel $(s, t)$, and line L1 sets $M_0 = T$. Assume the claim for level $k < L$. Line L3 gives the new level $W_{k+1} = \max(1, W_k / 2)$ columns and $H_{k+1} = \max(1, H_k / 2)$ rows. Consider the columns. If $W_k > 1$, then $W_k$ is even, both columns $2s$ and $2s + 1$ exist in level $k$, and $w_{k+1} = 2 w_k$, so $B_k$ blocks of the columns $2s$ and $2s+1$ together span the columns $[s w_{k+1}, (s+1) w_{k+1})$. If $W_k = 1$, then $s = 0$, only column $0$ exists, and $w_{k+1} = w_k$. The rows behave in the same way. So line L5 averages $m \in \{1, 2, 4\}$ texels of level $k$ whose blocks are disjoint, all of size $w_k h_k$, and have the union $B_{k+1}(s, t)$, which has $m w_k h_k$ texels. By the induction hypothesis each of the $m$ texels is the sum over its block divided by $w_k h_k$. Their mean is therefore the sum over $B_{k+1}(s, t)$ divided by $m w_k h_k = w_{k+1} h_{k+1}$. $\square$

**Lemma 2 (termination).** The loop of lines L2 to L6 runs exactly $L$ times, and the last level is a single texel that holds the mean of the whole texture.

*Proof.* Each pass halves every side that is larger than 1 and keeps sides equal to 1. A side $2^a$ reaches 1 after $a$ passes and then stays 1. So level $k$ is $1 \times 1$ exactly when $k \ge L$, and line L2 stops after level $L$. By Lemma 1 with $w_L = W$ and $h_L = H$, the single block of level $L$ is the whole grid. $\square$

**Lemma 3 (alignment).** With texel centers at half-integers, the center of texel $(s, t)$ of level $k$, written in base texel units, is the center of its block $B_k(s, t)$.

*Proof.* A normalized coordinate $u$ is $u W_k$ in the texel units of level $k$ and $u W$ in base units, so one texel of level $k$ spans $w_k$ base texels. The center $s + 1/2$ of level $k$ is $(s + 1/2) w_k$ in base units, which is the midpoint of $[s w_k, (s+1) w_k)$. The rows are the same. $\square$

So the same $(u, v)$ addresses the same point of the texture on every level, and lines L9, L11 and L13 may pass $(u, v)$ unchanged to each level.

**Theorem 1 (storage).** The levels hold $S = \sum_{k=0}^{L} W_k H_k = (4WH + 2r - 3)/3$ texels, where $r = \max(W, H) / \min(W, H)$. If $W = H$, then $S = (4WH - 1)/3 < \frac43 WH$. In every case $S < 2WH$.

*Proof.* By symmetry let $a \ge b$, so $r = 2^{a-b}$. For $0 \le k \le b$, both sides are still halving and $W_k H_k = 2^{a+b-2k} = WH/4^k$. The geometric series gives

$$\sum_{k=0}^{b} \frac{WH}{4^k} = \frac{4}{3} WH \Big(1 - 4^{-(b+1)}\Big) = \frac{4WH - 2^{a-b}}{3} = \frac{4WH - r}{3}.$$

For $b < k \le a$, the height is 1 and $W_k H_k = 2^{a-k}$, and these terms sum to $2^{a-b-1} + \dots + 1 = r - 1$. The total is $(4WH - r)/3 + r - 1 = (4WH + 2r - 3)/3$. If $W = H$, then $r = 1$ and $S = (4WH - 1)/3$. Since $r \le WH$, we get $2r - 3 < 2WH$, so $3S < 6WH$. $\square$

The extra memory over the base texture is therefore below one third of it for a square texture, and below one full copy for any power-of-two texture.

**Theorem 2 (the lookup).** For a level of detail $\lambda$, TRILINEAR returns $\mathrm{BILINEAR}(M_0)$ if $\lambda \le 0$, $\mathrm{BILINEAR}(M_L)$ if $\lambda \ge L$, and otherwise $(1 - f)\,\mathrm{BILINEAR}(M_d) + f\,\mathrm{BILINEAR}(M_{d+1})$ with $d = \lfloor \lambda \rfloor$ and $f = \lambda - d$, all at the same $(u, v)$. The result is a convex combination of base texels, so it lies between the smallest and the largest texel value in each channel, and it is a continuous function of $\lambda$.

*Proof.* The three cases are lines L8 to L14 read directly. For $0 < \lambda < L$, $d$ is an integer in $[0, L-1]$, so both levels exist, and $f \in [0, 1)$. A bilinear lookup is a convex combination of four texels of its level, with the weights $(1-\alpha)(1-\beta)$, $\alpha(1-\beta)$, $(1-\alpha)\beta$ and $\alpha\beta$, which are nonnegative and sum to 1. By Lemma 1 each texel of a level is a convex combination of base texels. A convex combination of convex combinations is a convex combination, and so is the blend with the weights $1 - f$ and $f$. For continuity: inside each open interval $(d, d+1)$ the result is affine in $\lambda$. As $\lambda$ rises to an integer $d + 1 \le L - 1$, $f \to 1$ and the value tends to $\mathrm{BILINEAR}(M_{d+1})$, which is the value at $\lambda = d + 1$, where $f = 0$. At $\lambda = 0$ both sides give $\mathrm{BILINEAR}(M_0)$, and as $\lambda$ rises to $L$ the value tends to $\mathrm{BILINEAR}(M_L)$, the value for $\lambda \ge L$. $\blacksquare$
