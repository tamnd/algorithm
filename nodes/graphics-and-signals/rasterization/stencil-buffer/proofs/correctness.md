---
title: Stencil then cover with a triangle fan leaves the winding number modulo 2^s in each pixel and covers the pixels that the fill rule selects
proves: [correctness]
status: full
---

We use the pseudocode of the page. The buffer has $s \ge 1$ bits per pixel, so each stored value is in $\{0, \dots, 2^s - 1\}$. Pixel $(i, j)$ has its center $c = (i + 1/2, j + 1/2)$, and its shifted center is $c_\varepsilon = c + (\varepsilon, \varepsilon^2)$ for a small $\varepsilon > 0$. For points $a, b, p$ let $\operatorname{orient}(a, b, p) = (b_x - a_x)(p_y - a_y) - (b_y - a_y)(p_x - a_x)$.

**Lemma 1 (the shifted center is in general position).** Let $L$ be a finite set of lines. For all small enough $\varepsilon > 0$, the point $c_\varepsilon$ lies on no line of $L$.

*Proof.* A line $\alpha x + \beta y = \gamma$ contains $c_\varepsilon$ when $\alpha \varepsilon + \beta \varepsilon^2 = \gamma - \alpha c_x - \beta c_y$. If the right side is not zero, this fails for $\varepsilon$ small enough. If it is zero, it reads $\varepsilon(\alpha + \beta \varepsilon) = 0$, which has at most one positive root, since $\alpha$ and $\beta$ are not both zero. So each line excludes an interval near 0 or one value, and finitely many lines leave all small enough $\varepsilon$. $\square$

We take $L$ to be all lines through two distinct vertices of the path. These include the lines of all edges of the path and of all fan triangles. The procedure TRIANGLE-PIXELS covers pixel $(i, j)$ for the triangle $T$ when $c_\varepsilon$ is in the inside of $T$, and it covers nothing when $T$ has zero area. This is the top-left rule of [triangle rasterization](/triangle-rasterization/), and the implementation decides it exactly by the signs of the edge functions and of their partial derivatives.

**Lemma 2 (the fan identity).** Let $R = (v_0, v_1, \dots, v_{m-1})$ be a closed ring, and let $T_k = (v_0, v_k, v_{k+1})$ for $1 \le k \le m - 2$. Let $\sigma_k$ be the sign of $\operatorname{orient}(v_0, v_k, v_{k+1})$. For each point $p$ on no line of $L$,
$$w_R(p) = \sum_{k=1}^{m-2} \sigma_k \, [p \in T_k],$$
where $w_R(p)$ is the winding number of $R$ around $p$, with the orientation in which a triangle with $\operatorname{orient} > 0$ has winding number $+1$ at its inner points.

*Proof.* The winding number is additive over closed chains: if the oriented edges of several closed chains add up, with opposite edges cancelling, to the edges of $R$, then the winding numbers add up to $w_R(p)$ for each $p$ on none of the edges. The boundaries of $T_1, \dots, T_{m-2}$, each run as $v_0 \to v_k \to v_{k+1} \to v_0$, contain the edges $v_k v_{k+1}$ of $R$ for $1 \le k \le m - 2$, the edge $v_0 v_1$ from $T_1$ and the edge $v_{m-1} v_0$ from $T_{m-2}$, and the diagonals $v_0 v_k$ for $2 \le k \le m - 2$, each once in each direction. The diagonals cancel, and what is left is $R$. The point $p$ is on none of these segments, because it is on no line of $L$. A triangle with $\sigma_k \ne 0$ has winding number $\sigma_k$ at its inner points and 0 at its outer points. A triangle with $\sigma_k = 0$ is a segment run forward and back, with winding number 0 at each point off it. $\square$

For a path of several rings, $w(p)$ is the sum of $w_R(p)$ over the rings, so the identity holds with the sum over the fan triangles of all rings.

**Lemma 3 (the stencil pass, nonzero).** After lines L4 to L6 with INCR_WRAP for front faces and DECR_WRAP for back faces, the value of pixel $(i, j)$ is $w(c_\varepsilon) \bmod 2^s$.

*Proof.* Line L4 sets the function ALWAYS, so every fragment passes the stencil test, and the depth test passes, so line L2 picks dppass. The write mask is all ones, so line L3 stores the result of the operation. The buffer starts at 0. A front-facing triangle ($\sigma_k = +1$) that covers the pixel applies INCR_WRAP, which maps $v$ to $(v + 1) \bmod 2^s$. A back-facing triangle ($\sigma_k = -1$) applies DECR_WRAP, which maps $v$ to $(v - 1) \bmod 2^s$. A triangle with $\sigma_k = 0$ covers no pixel. These maps are additions in the group of integers modulo $2^s$, so their order does not matter, and the final value is $\sum_k \sigma_k [c_\varepsilon \in T_k] \bmod 2^s$. By Lemma 2 at $p = c_\varepsilon$, this is $w(c_\varepsilon) \bmod 2^s$. $\square$

**Lemma 4 (the stencil pass, even-odd).** After lines L4 to L6 with INVERT for both faces and the write mask 1, bit 0 of pixel $(i, j)$ is $w(c_\varepsilon) \bmod 2$, and the other bits are 0.

*Proof.* INVERT maps $v$ to $\lnot v$, and the write mask 1 keeps all bits but bit 0, so each fragment flips bit 0 and changes nothing else. So bit 0 is the parity of the number $N$ of fan triangles whose inside holds $c_\varepsilon$. Since $\sigma_k \equiv [\sigma_k \ne 0] \pmod 2$ and triangles with $\sigma_k = 0$ cover nothing, $N \equiv \sum_k \sigma_k [c_\varepsilon \in T_k] = w(c_\varepsilon) \pmod 2$ by Lemma 2. $\square$

**Theorem.** FILL-PATH covers pixel $(i, j)$ under the even-odd rule exactly when $w(c_\varepsilon)$ is odd, that is, exactly when the shifted center is inside under the [even-odd fill rule](/even-odd-fill-rule/). Under the nonzero rule it covers pixel $(i, j)$ exactly when $w(c_\varepsilon) \not\equiv 0 \pmod{2^s}$. So when $|w(c_\varepsilon)| < 2^s$ for all pixels, it covers exactly the pixels whose shifted centers are inside under the [nonzero winding rule](/nonzero-winding-rule/).

*Proof.* Line L7 sets the test NOTEQUAL with reference 0 and mask $M$, where $M$ is all ones for the nonzero rule and $M = 1$ for the even-odd rule. A fragment at a pixel with stored value $v$ passes when $(0 \mathbin{\&} M) \ne (v \mathbin{\&} M)$, that is, when $v \mathbin{\&} M \ne 0$. Line L8 sends one fragment to each pixel, and the depth test passes, so a pixel is covered exactly when this test passes on the value that the stencil pass left. Each pixel gets one cover fragment, and the ZERO operation changes only that pixel, so the order of the cover fragments does not matter. For the nonzero rule, by Lemma 3, $v = w(c_\varepsilon) \bmod 2^s$, and $v \ne 0$ exactly when $2^s$ does not divide $w(c_\varepsilon)$. If $|w(c_\varepsilon)| < 2^s$, this is $w(c_\varepsilon) \ne 0$. For the even-odd rule, by Lemma 4, $v \mathbin{\&} 1 = w(c_\varepsilon) \bmod 2$. $\blacksquare$

**Saturating operations fail.** INCR maps $v$ to $\min(v + 1, 2^s - 1)$ and DECR maps $v$ to $\max(v - 1, 0)$. These maps do not commute: from $v = 0$, DECR then INCR gives 1, and INCR then DECR gives 0. A pixel covered by one back-facing and one front-facing triangle has $w = 0$, but if the back-facing triangle is drawn first, the value ends at 1 and the pixel is wrongly covered. So the result of a saturating stencil pass depends on the order of the triangles.

**Too few bits.** With $s = 1$, INCR_WRAP and DECR_WRAP both flip the single bit, so the nonzero pass computes $w \bmod 2$ and the fill is the even-odd fill. With $s$ bits, a pixel with $w = 2^s$ has value 0 and is not covered, although it is inside under the nonzero rule.
