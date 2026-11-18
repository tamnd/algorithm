---
title: The BC1 decoder is a fixed function of the block, and the encoder is lossless on palette colors
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. The decoder works on integers and exact fractions. For the encoder we assume exact real arithmetic (real-ram) for the principal axis and the projections. The code uses floats there, and the code tests check the same claims in floats.

For an RGB565 word $w$, let $E(w) = (R/31, G/63, B/31)$ with $R = \lfloor w / 2^{11} \rfloor$, $G = \lfloor w / 2^5 \rfloor \bmod 64$ and $B = w \bmod 32$. The map $E$ is one to one from $\{0, \dots, 65535\}$ to colors, because the three fields of $w$ are disjoint bit ranges and each field divides by a fixed number.

**Theorem 1 (the rate and the layout).** A block has $64$ bits and codes 16 texels, so the rate is $64/16 = 4$ bits per texel. Every 64-bit string is a valid block, and lines L1 to L5 give a texel for each one.

*Proof.* Lines L1 and L2 read two 16-bit words and a 32-bit word, $16 + 16 + 32 = 64$ bits. Line L5 reads 16 fields of 2 bits, $32$ bits, so the fields of texels $i$ and $j \ne i$ do not overlap. Each 2-bit field is a number in $\{0, 1, 2, 3\}$, and both palettes of lines L3 and L4 have 4 entries, so every index is valid. $\square$

So decoding is a fixed function of the block alone. A texel at $(x, y)$ needs only the block $(\lfloor x/4 \rfloor, \lfloor y/4 \rfloor)$, which gives random access at a fixed address. The code test `test_random_access_and_determinism` checks this.

**Lemma 1 (the palettes).** If $c_0 > c_1$, the palette is $C_0$, $C_1$, $\tfrac23 C_0 + \tfrac13 C_1$, $\tfrac13 C_0 + \tfrac23 C_1$ with $C_j = E(c_j)$, all opaque. These lie on the segment from $C_1$ to $C_0$ at the parameters $1, 0, \tfrac23, \tfrac13$, and they are four different colors. If $c_0 \le c_1$, the palette is $C_0$, $C_1$, $\tfrac12 (C_0 + C_1)$ and transparent black.

*Proof.* This is lines L3 and L4. If $c_0 > c_1$, then $c_0 \ne c_1$, so $C_0 \ne C_1$ because $E$ is one to one. The four parameters are different, and a segment of nonzero length maps different parameters to different points. $\square$

**Lemma 2 (the index choice is optimal).** For fixed endpoints, line L9 gives each texel an index of a palette color nearest to it. So no other choice of the 16 indices gives a smaller total squared error for these endpoints.

*Proof.* The total error is a sum of 16 terms, and the index of texel $i$ appears only in term $i$. Line L9 minimizes each term on its own. $\square$

The endpoints themselves are not optimal. The range fit of lines L6 to L8 is a heuristic. Its error is a measurement, given on the page.

**Theorem 2 (lossless on palette colors).** Let $c_0 > c_1$ be two RGB565 words, and let every texel of a block be one of the four palette colors of Lemma 1, with both $C_0$ and $C_1$ present. Then the encoder returns a block that decodes to exactly the input texels.

*Proof.* Let $d = C_0 - C_1 \ne 0$. Each texel is $C_1 + s_i d$ with $s_i \in \{0, \tfrac13, \tfrac23, 1\}$. The mean is $\mu = C_1 + \bar s d$, and the covariance is $\Sigma = \sigma d d^T$ with $\sigma = \sum_i (s_i - \bar s)^2 > 0$, since both $s = 0$ and $s = 1$ occur.

Line L6 starts the power iteration at the unit axis $e_a$ with the largest diagonal entry $\Sigma_{aa} = \sigma d_a^2$. Some coordinate of $d$ is not zero, so $d_a \ne 0$. Then $\Sigma e_a = \sigma d_a d$, a nonzero multiple of $d$, and every later step maps a multiple of $d$ to a multiple of $d$, because $\Sigma d = \sigma |d|^2 d$. So the axis is $\alpha d$ for some $\alpha \ne 0$.

The projection of texel $i$ on the axis is $(s_i - \bar s) \alpha |d|^2$, a strictly monotone function of $s_i$. So line L7 picks a texel with $s = 0$ and a texel with $s = 1$ as the two extremes, which are the colors $C_1$ and $C_0$ (in some order, by the sign of $\alpha$). Line L8 rounds each to the nearest RGB565 word. $C_j = E(c_j)$ has the components $R/31$, $G/63$ and $B/31$, so the rounding gives back $R$, $G$ and $B$ exactly, and the words are $c_0$ and $c_1$. Line L8 orders them so that the first is larger, which is $(c_0, c_1)$, and $c_0 \ne c_1$, so the encoder does not take the branch for equal words. The palette is the palette of Lemma 1. Each texel equals one palette color, at distance 0, and the other three colors are different from it, so line L9 picks that color. The decoder returns it. $\square$

**Cost.** Decoding a texel takes $O(1)$ time: two words, one palette and one 2-bit field. Encoding a block of 16 texels takes $O(1)$ time for a fixed number of power iterations: the covariance is $3 \times 3$, and line L9 compares each texel with 4 colors. An image of $W \times H$ texels takes $\Theta(WH)$ time to encode and $W H / 2$ bytes.
