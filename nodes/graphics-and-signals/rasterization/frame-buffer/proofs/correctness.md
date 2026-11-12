---
title: The frame buffer operations keep the bytes equal to the abstract image
proves: [correctness]
status: full
---

Let the buffer have width $W$, height $H$, $C \ge 1$ bytes per pixel and pitch $P \ge WC$, and let $M[0 \,..\, HP - 1]$ be its bytes. The abstract value is the map $A$ from the pixels $(i, j)$ with $0 \le i < W$ and $0 \le j < H$ to colors $(c_0, \dots, c_{C-1})$ of bytes. The abstraction function reads pixel $(i, j)$ as $A(i, j) = (M[o(i, j) + k])_{k < C}$ with $o(i, j) = jP + iC$. We prove that the bytes of different pixels do not overlap, and that each operation changes $A$ as its specification says and changes no pad byte.

**Lemma (the address map is one to one).** The map $\phi(i, j, k) = jP + iC + k$ on $0 \le i < W$, $0 \le j < H$, $0 \le k < C$ is injective, its values are in $[0, HP)$, and each value $u$ has $u \bmod P < WC$.

*Proof.* Let $s = iC + k$. Then $0 \le s \le (W - 1)C + C - 1 = WC - 1 < P$, so $s = u \bmod P$ and $j = \lfloor u / P \rfloor$ for $u = \phi(i, j, k)$. Also $0 \le k < C$ gives $i = \lfloor s / C \rfloor$ and $k = s \bmod C$. So $(i, j, k)$ is a function of $u$, and $\phi$ is injective. The bounds follow from $j \le H - 1$ and $s \le WC - 1$. $\square$

So each byte of $M$ belongs to at most one pixel, and the bytes with $u \bmod P \ge WC$, the pad, belong to none.

**WRITE-PIXEL.** If $(i, j)$ is outside the buffer, line L1 fails and nothing changes. Otherwise line L2 computes $a = o(i, j)$, and line L3 writes $M[a + k] = c_k$ for $k < C$. These are the bytes $\phi(i, j, k)$, so $A(i, j)$ becomes $c$. By the lemma no other pixel and no pad byte uses these bytes, so the rest of $A$ and the pad do not change.

**READ-PIXEL.** Line R1 returns nothing for a pixel outside the buffer, and line R2 reads the bytes $\phi(i, j, k)$, which is $A(i, j)$ by definition.

**FILL-RECT.** Line F1 intersects the half-open rectangle $[x_0, x_1) \times [y_0, y_1)$ with $[0, W) \times [0, H)$. If the result is empty, nothing changes. Otherwise, for each row $j$, line F3 writes the $(x_1 - x_0)C$ bytes of the span of line F2 at the offsets $jP + x_0 C$ to $jP + x_1 C - 1$. These are exactly the values $\phi(i, j, k)$ for $x_0 \le i < x_1$ and $k < C$, in increasing order of $iC + k$, and the span holds $c_k$ at the position $(i - x_0)C + k$. So each pixel in the clipped rectangle gets the color $c$. All these offsets are below $jP + WC$, so no pad byte changes, and by the lemma no pixel outside the rectangle changes.

**CLEAR** is FILL-RECT of the whole buffer, so it sets $A(i, j) = c$ for all pixels and keeps the pad.

**The scan order.** Row $j$ is the block $M[jP \,..\, jP + WC - 1]$, with pixel $(i, j)$ at the bytes $iC$ to $iC + C - 1$ of the block. So a display that reads $WC$ bytes from each multiple of $P$, for $j = 0, 1, \dots, H - 1$, gets the pixels of the image in the order of the scan, from the top row down. $\blacksquare$
