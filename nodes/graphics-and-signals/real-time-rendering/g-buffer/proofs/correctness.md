---
title: The octahedral normal encoding is a round trip
proves: [correctness]
status: full
---

**Setting.** $\operatorname{sgn}(x) = 1$ for $x \ge 0$ and $-1$ for $x < 0$, so that $\operatorname{sgn}(0) = 1$. The fold is $F(u, v) = ((1 - |v|) \operatorname{sgn}(u), (1 - |u|) \operatorname{sgn}(v))$. OCT-ENCODE (lines L1 to L4) maps a nonzero vector $n = (x, y, z)$ to $(x / s, y / s)$ with $s = |x| + |y| + |z|$ if $z \ge 0$, and to $F(x / s, y / s)$ if $z < 0$. OCT-DECODE (lines L5 to L7) maps $(u, v) \in [-1, 1]^2$ to the normalized vector of $(u, v, 1 - |u| - |v|)$ if $|u| + |v| \le 1$, and of $(F(u, v), 1 - |u| - |v|)$ otherwise. The claims are in exact arithmetic.

**Lemma 1 (the image is in the square).** For every nonzero $n$, OCT-ENCODE$(n) \in [-1, 1]^2$.

*Proof.* $|x / s| + |y / s| \le 1$, so both coordinates are in $[-1, 1]$. The fold keeps them there, because $1 - |v|$ and $1 - |u|$ are in $[0, 1]$ when $|u|, |v| \le 1$. $\square$

**Theorem 1 (round trip).** For every nonzero $n$, OCT-DECODE(OCT-ENCODE$(n)$) $= n / \lVert n \rVert$.

*Proof.* Let $u = x / s$, $v = y / s$, $w = z / s$. Then $|u| + |v| + |w| = 1$, so $(u, v, w)$ is $n$ scaled by the positive number $1 / s$.

Case $z \ge 0$. The encoder returns $(u, v)$. The decoder computes $1 - |u| - |v| = |w| = w$, which is not negative, so it does not fold. It returns the normalized vector of $(u, v, w)$, which is $n / \lVert n \rVert$.

Case $z < 0$. Then $|w| > 0$, so $|u| < 1$ and $|v| < 1$. The encoder returns $(u', v') = F(u, v)$, with $|u'| = 1 - |v| > 0$ and $|v'| = 1 - |u| > 0$. So $\operatorname{sgn}(u') = \operatorname{sgn}(u)$ and $\operatorname{sgn}(v') = \operatorname{sgn}(v)$; this needs $\operatorname{sgn}(0) = 1$ when $u$ or $v$ is 0. The decoder computes $1 - |u'| - |v'| = |u| + |v| - 1 = -|w| = w < 0$, so it folds:

$$F(u', v') = ((1 - |v'|) \operatorname{sgn}(u'), (1 - |u'|) \operatorname{sgn}(v')) = (|u| \operatorname{sgn}(u), |v| \operatorname{sgn}(v)) = (u, v).$$

It returns the normalized vector of $(u, v, w)$, which is again $n / \lVert n \rVert$. $\square$

**Theorem 2 (the other direction).** For every $(u, v)$ in the open square $(-1, 1)^2$, OCT-ENCODE(OCT-DECODE$(u, v)$) $= (u, v)$.

*Proof.* The decoder computes a vector $m$ proportional to $(a, b, c)$ with $|a| + |b| + |c| = 1$: for $|u| + |v| \le 1$, $(a, b, c) = (u, v, 1 - |u| - |v|)$ with $c \ge 0$; otherwise $(a, b) = F(u, v)$ and $c = 1 - |u| - |v| < 0$, and $|a| + |b| = 2 - |u| - |v| = 1 - c = 1 + |c|$. So $m = (a, b, c) / \lambda$ with $\lambda = \lVert (a, b, c) \rVert$, the encoder computes $s = 1 / \lambda$, and it gets $(m_x / s, m_y / s) = (a, b)$, with the sign of $m_z$ equal to the sign of $c$. In the first case it returns $(a, b) = (u, v)$. In the second case it returns $F(a, b)$. Here $|u|, |v| < 1$, so $|a| = 1 - |v| > 0$ and $|b| = 1 - |u| > 0$, the signs are kept, and $F(a, b) = (u, v)$ as in Theorem 1. $\square$

On the border of the square the map is not one to one: $(1, t)$ and $(1, -t)$ decode to the same vector, and all four corners decode to $(0, 0, -1)$. The encoder returns one of these points. This does not affect Theorem 1.

**Theorem 3 (quantization).** With $b$ bits per coordinate and $m = 2^{b-1} - 1$, QUANTIZE (line L8) followed by DEQUANTIZE (line L9) changes each coordinate in $[-1, 1]$ by at most $1 / (2m)$.

*Proof.* $\operatorname{round}(x m)$ differs from $x m$ by at most $1/2$, and $x m \in [-m, m]$, so the result is in $[-m, m]$ and the clamp in line L9 does not act on it. Dividing by $m$ gives the bound. $\square$

The angle error that this coordinate error causes after decoding depends on where the point is in the square. The largest values on the page and in the tests (below 1 degree for 8 bits and below 0.005 degrees for 16 bits per coordinate) are measurements on random directions, not proved bounds.

**Theorem 4 (the texel layout).** UNPACK-TEXEL(PACK-TEXEL$(c, n, r, k)$) returns each color channel, the roughness and the metallic value to within $1 / 510$ of the input, after clamping to $[0, 1]$, and returns the normal of the 16-bit octahedral code of $n$.

*Proof.* Each unorm8 value is $\operatorname{round}(255 x) \in [0, 255]$, so it fits in 8 bits, the shifts put the four values in disjoint bytes of word 0, and the masks in the unpack read them back unchanged. Division by 255 gives a value within $1/510$ of $x$. The two 16-bit codes are stored as two's complement in the two halves of word 1 and read back with sign extension, so DECODE receives the same pair of integers. $\square$
