---
title: The magic-mask stages spread and compact the bits of a coordinate
proves: [correctness]
status: full
---

All words are 64-bit unsigned. For a word $v$ we write $v_p$ for bit $p$ of $v$. Let $0 \le x < 2^{32}$ with bits $x_0, \ldots, x_{31}$. Number the stages of SPREAD by $j = 4, 3, 2, 1, 0$, so that the stage $j$ computes $v \leftarrow (v \mathbin{|} (v \ll 2^j)) \mathbin{\&} M_j$, where $M_j$ is the 64-bit mask whose bit $p$ is 1 exactly when $p \bmod 2^{j+1} < 2^j$. The masks of lines L1 to L5 are $M_4, M_3, M_2, M_1, M_0$: for example $M_4 = \mathtt{0x0000FFFF0000FFFF}$ and $M_0 = \mathtt{0x5555555555555555}$.

**Position map.** For $0 \le j \le 5$ and $0 \le i < 32$ let
$$ p_j(i) = i + 2^j \left\lfloor i / 2^j \right\rfloor . $$
Write $i = q \cdot 2^j + r$ with $0 \le r < 2^j$; then $p_j(i) = q \cdot 2^{j+1} + r$. So $p_j(i) \bmod 2^{j+1} = r < 2^j$, and $p_j$ is injective, since $q$ and $r$ can be read back from $p_j(i)$. Also $p_5(i) = i$ for $i < 32$, and $p_0(i) = 2i$.

**Invariant.** Let $v^{(j)}$ be the word after the stage $j$, and let $v^{(5)} = x$ be the word before line L1. Then for each $j$ from 5 down to 0:
$$ v^{(j)} = \sum_{i=0}^{31} x_i \, 2^{p_j(i)} . $$
In words, bit $i$ of $x$ is at position $p_j(i)$, and every other bit of the word is 0.

**Base.** For $j = 5$, $p_5(i) = i$, so the claim is $v^{(5)} = x$.

**Step.** Assume the claim for $j + 1$, with $0 \le j \le 4$. Take a bit $i$ and write $i = q \cdot 2^{j+1} + h \cdot 2^j + r$ with $h \in \{0, 1\}$ and $0 \le r < 2^j$. Then $\lfloor i / 2^{j+1} \rfloor = q$, so by the claim for $j + 1$ the bit $x_i$ is at position $P = i + 2^{j+1} q = q \cdot 2^{j+2} + h \cdot 2^j + r$ of $v^{(j+1)}$. All positions $p_j(i)$ and $p_{j+1}(i)$ are at most $p_0(31) = 62$, so the kept copies below are inside the word; a copy that the shift moves past bit 63 is one that the mask would clear. The word $u = v^{(j+1)} \mathbin{|} (v^{(j+1)} \ll 2^j)$ has a copy of $x_i$ at $P$ and at $P + 2^j$, and the AND with $M_j$ keeps a position $p$ only when $p \bmod 2^{j+1} < 2^j$.

- If $h = 0$, then $P \bmod 2^{j+1} = r < 2^j$, so the copy at $P$ is kept, and $(P + 2^j) \bmod 2^{j+1} = r + 2^j \ge 2^j$, so the copy at $P + 2^j$ is cleared. The kept position is $q \cdot 2^{j+2} + r$.
- If $h = 1$, then $P \bmod 2^{j+1} = 2^j + r \ge 2^j$, so the copy at $P$ is cleared, and $P + 2^j = q \cdot 2^{j+2} + 2^{j+1} + r$ has remainder $r < 2^j$ modulo $2^{j+1}$, so it is kept.

In both cases the kept position is $q \cdot 2^{j+2} + h \cdot 2^{j+1} + r = i + 2^j (2q + h) = i + 2^j \lfloor i / 2^j \rfloor = p_j(i)$.

It remains to show that the OR does not merge two different bits, and that no other one-bits survive. Every one-bit of $u$ is a copy of some $x_i$, at $P$ or at $P + 2^j$. Suppose that a position $p$ kept by the mask holds a copy of $x_i$ and a copy of $x_{i'}$. By the case analysis, the kept copy of each bit is at $p_j(i)$ and at $p_j(i')$ respectively, and the cleared copies are not kept; so $p_j(i) = p = p_j(i')$, and $i = i'$ because $p_j$ is injective. Hence position $p_j(i)$ of $v^{(j)} = u \mathbin{\&} M_j$ holds exactly $x_i$, and every position that is not of the form $p_j(i)$ is 0. This proves the claim for $j$.

**SPREAD.** For $j = 0$ the invariant gives $\operatorname{SPREAD}(x) = \sum_i x_i 2^{2i}$. Line L7 then returns $\sum_i x_i 2^{2i} + \sum_i y_i 2^{2i+1}$, since the two terms have their ones at even and at odd positions and so the OR is a sum. This is $Z(x, y)$, and it is below $2^{64}$.

**COMPACT.** Number the stages of COMPACT by $j = 0, 1, 2, 3, 4$, with shift $2^j$ and the mask $M_{j+1}$, where $M_5 = \mathtt{0x00000000FFFFFFFF}$ is the mask of the positions with $p \bmod 64 < 32$. Let $z$ be a word whose odd bits are 0 after line D1, so $z = \sum_i x_i 2^{p_0(i)}$ for the bits $x_i = z_{2i}$. We claim that after the stage $j$ the word is $\sum_i x_i 2^{p_{j+1}(i)}$. Assume that before the stage the word is $v = \sum_i x_i 2^{p_j(i)}$. Write $i = q \cdot 2^{j+1} + h \cdot 2^j + r$ as before; then $p_j(i) = q \cdot 2^{j+2} + h \cdot 2^{j+1} + r$ and $p_{j+1}(i) = q \cdot 2^{j+2} + h \cdot 2^j + r$. The word $v \oplus (v \gg 2^j)$ has, at each position $p$, the XOR of $v_p$ and $v_{p + 2^j}$. Take a position $p$ that $M_{j+1}$ keeps, so $p = Q \cdot 2^{j+2} + s$ with $0 \le s < 2^{j+1}$. Write $s = H \cdot 2^j + R$ with $H \in \{0, 1\}$ and $0 \le R < 2^j$. Every one-bit of $v$ is at a position whose remainder modulo $2^{j+1}$ is below $2^j$.

- If $H = 0$, then $p + 2^j$ has remainder $2^j + R \ge 2^j$ modulo $2^{j+1}$, so $v_{p + 2^j} = 0$, and the result at $p$ is $v_p$, which is $x_i$ for the $i$ with $q = Q$, $h = 0$, $r = R$, if that $i$ is below 32, and 0 otherwise.
- If $H = 1$, then $p$ has remainder $2^j + R \ge 2^j$ modulo $2^{j+1}$, so $v_p = 0$, and $p + 2^j = Q \cdot 2^{j+2} + 2^{j+1} + R$, so the result is $x_i$ for $q = Q$, $h = 1$, $r = R$, or 0 if that $i$ is not below 32.

In both cases position $p$ of the result holds $x_i$ for the unique $i$ with $p_{j+1}(i) = p$, and the positions with no such $i$ hold 0. The positions that $M_{j+1}$ clears hold 0 by definition. This proves the claim. After the stage $j = 4$ the word is $\sum_i x_i 2^{p_5(i)} = \sum_i x_i 2^i$, so COMPACT returns the even bits of $z$, packed. Line D8 applies it to $z$ and to $z \gg 1$, which gives the $x$ bits and the $y$ bits of the code. Hence MORTON-DECODE inverts MORTON-ENCODE, and since both maps are between sets of $2^{64}$ elements, encoding is a bijection. $\blacksquare$
