---
title: The reversible path of JPEG 2000 (level shift, RCT, 5/3 lifting DWT) is exactly invertible on integers, and the dead-zone quantizer has a bounded error
proves: [correctness]
status: full
---

**Setup.** The input is one or three components of $H \times W$ unsigned integers with $B$ bits. Line L1 subtracts $2^{B-1}$, line L2 applies the RCT to three components, line L3 cuts tiles, line L4 applies $N_L$ levels of the 2D 5/3 DWT to each tile, and line L5 quantizes with step 1. The 1D transform LIFT-53 (lines L7 to L9) acts on a sequence $x[0 \ldots n-1]$ whose first sample has an even coordinate. It uses *whole-sample symmetric extension*: an index $i$ outside $[0, n-1]$ is replaced by $m(i)$, its mirror image about the end samples, $m(-i) = i$ and $m(n - 1 + i) = n - 1 - i$, repeated as often as needed. For $n = 1$ the sample is passed through unchanged.

**Lemma 1 (the mirror keeps the parity).** For $n \ge 2$ and every integer $i$, $m(i) \equiv i \pmod 2$.

*Proof.* The mirror is periodic with period $2(n - 1)$, an even number, and inside one period it maps $i$ to $i$ or to $2(n-1) - i$. Both have the parity of $i$. $\square$

So the predict step (line L7), which computes odd samples, reads only even samples of $x$, and the update step (line L8), which computes even samples, reads only odd samples of $y$.

**Lemma 2 (a lifting step is invertible for any function).** Let $x$ be split into its even part $e$ and odd part $o$. For any function $P$ of $e$ and any function $U$ of a sequence like $o$, possibly nonlinear and with rounding, the map
$$o' = o - P(e), \qquad e' = e + U(o')$$
is a bijection, with inverse $e = e' - U(o')$, $o = o' + P(e)$.

*Proof.* From $(e', o')$ the decoder knows $o'$, so it computes $U(o')$, the same value the encoder added, and subtracts it to get $e$. Then it knows $e$, so it computes $P(e)$ and adds it to get $o$. Composing the two inverse steps with the forward ones gives the identity in both orders. $\square$

**Lemma 3 (LIFT-53 maps integers to integers and is exactly invertible).** With $P(e)[i] = \lfloor (x[i-1] + x[i+1]) / 2 \rfloor$ for odd $i$ and $U(o')[i] = \lfloor (y[i-1] + y[i+1] + 2) / 4 \rfloor$ for even $i$, both under the symmetric extension, LIFT-53 maps $\mathbb{Z}^n$ into $\mathbb{Z}^{\lceil n/2 \rceil} \times \mathbb{Z}^{\lfloor n/2 \rfloor}$ bijectively, and the procedure that undoes line L8 and then line L7 is its inverse.

*Proof.* By Lemma 1, $P$ depends only on the even samples and $U$ only on the odd outputs of line L7, so Lemma 2 applies. The floor of an integer divided by 2 or 4 is an integer, so all values stay integers. For $n = 1$ the map is the identity. $\square$

**Lemma 4 (the 2D transform is invertible).** One level of the 2D DWT applies LIFT-53 to every column of the current LL region and then to every row of it. The region of the next level is the top-left $\lceil h/2 \rceil \times \lceil w/2 \rceil$ block. The inverse that undoes the levels from the last to the first, at each level undoing the rows and then the columns of the same region, recovers the input exactly.

*Proof.* At each level the column step is a product of independent bijections, one per column, so it is a bijection of the region, and so is the row step. Samples outside the region do not change. The region sizes depend only on $H$, $W$ and the level, so the decoder knows them. Undoing a composition of bijections in the reverse order gives the identity, by induction on the number of levels. $\square$

**Lemma 5 (the RCT is exactly invertible).** For integers $R, G, B$ let $Y = \lfloor (R + 2G + B)/4 \rfloor$, $U = B - G$, $V = R - G$. Then $G = Y - \lfloor (U + V)/4 \rfloor$, $R = V + G$ and $B = U + G$.

*Proof.* $R + 2G + B = 4G + (R - G) + (B - G) = 4G + U + V$. Since $4G$ is a multiple of 4, $\lfloor (4G + U + V)/4 \rfloor = G + \lfloor (U + V)/4 \rfloor$. So $Y - \lfloor (U+V)/4 \rfloor = G$, and the other two follow. $\square$

**Theorem (the reversible path is lossless).** The decoder that undoes lines L6 to L1 in reverse order (inverse 2D DWT per tile, joining the tiles, inverse RCT, adding $2^{B-1}$) returns the input exactly. Every intermediate value is an integer, so the coefficients that reach tier 1 are integers and step 1 does not change them.

*Proof.* The level shift is a bijection on integers. The tiles are a partition of the samples, and each tile is transformed on its own; since each tile starts at an even coordinate when the tile size is even, Lemma 4 applies to each tile. Lemma 5 gives the inverse of the RCT. On integers, $\mathrm{sign}(y) \lfloor |y| / 1 \rfloor = y$. A composition of bijections is undone by their inverses in reverse order. $\blacksquare$

The entropy coding of tier 1 and tier 2 is lossless when no pass is dropped, so the full reversible codec is lossless. That part is described on the page, not proved here.

**Theorem (the dead-zone quantizer).** For a step $\Delta > 0$ let $q = \mathrm{sign}(y) \lfloor |y| / \Delta \rfloor$ and let the decoder output $\hat y = 0$ for $q = 0$ and $\hat y = \mathrm{sign}(q) (|q| + r) \Delta$ otherwise, with $0 \le r < 1$. Then $|y - \hat y| < \Delta$ when $q = 0$, and $|y - \hat y| \le \max(r, 1 - r) \Delta$ when $q \ne 0$, which is $\Delta/2$ for $r = 1/2$.

*Proof.* If $q = 0$ then $|y| < \Delta$ and $\hat y = 0$. If $q \ne 0$ then $y$ has the sign of $q$ and $|q| \Delta \le |y| < (|q| + 1) \Delta$, an interval of length $\Delta$ that contains $(|q| + r) \Delta$ at distance $r \Delta$ from its left end. Every point of the interval is within $\max(r, 1-r) \Delta$ of it. $\blacksquare$

On the irreversible path, the 9/7 lifting steps of Table F.4 are also bijections by Lemma 2 in exact arithmetic, and the scaling by $K$ and $1/K$ is invertible. In floating point the round trip is exact only up to rounding errors of the order of the machine precision, and the quantizer above is the only intended loss.
