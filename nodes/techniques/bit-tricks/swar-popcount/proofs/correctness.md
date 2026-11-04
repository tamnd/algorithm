---
title: The SWAR population count sums the bits field by field without carries between fields
proves: [correctness]
status: full
---

Fix $w \in \{8, 16, 32, 64, 128\}$. A word is an integer $0 \le x < 2^w$ with bits $x_t$. For a field width $f$ that divides $w$, the field $i$ of a word $y$ is $F_i^f(y) = \lfloor y / 2^{fi} \rfloor \bmod 2^f$, for $0 \le i < w/f$, so $y = \sum_i F_i^f(y)\, 2^{fi}$. Let $x_0$ be the input, and let $\nu_i^f = \sum_{t = fi}^{fi + f - 1} (x_0)_t$ be the number of 1-bits of $x_0$ in field $i$ of width $f$. Note $\nu_i^{2f} = \nu_{2i}^f + \nu_{2i+1}^f$.

**Tool (addition by fields).** Let $f$ divide $w$, and let $a = \sum_i a_i 2^{fi}$ and $b = \sum_i b_i 2^{fi}$ with $0 \le a_i, b_i$ and $a_i + b_i < 2^f$ for each $i$. Then $a + b = \sum_i (a_i + b_i) 2^{fi} < 2^w$, and $F_i^f(a + b) = a_i + b_i$. *Proof.* The sum is the stated series by the distributive law. Each coefficient $a_i + b_i$ lies in $[0, 2^f)$, so the series is the base-$2^f$ expansion of $a + b$, its fields are the coefficients, and the value is at most $\sum_i (2^f - 1) 2^{fi} = 2^w - 1$. So no reduction modulo $2^w$ happens. $\square$

The same argument with $a_i \ge b_i \ge 0$ gives $F_i^f(a - b) = a_i - b_i$ and $0 \le a - b < 2^w$.

**Step L1.** Let $x = x_0$, $f = 2$. The word $(x \gg 1) \wedge M_1$ has field $i$ equal to $(x_0)_{2i+1}$: the shift moves bit $2i + 1$ to position $2i$, and $M_1$ keeps exactly the even positions. Field $i$ of $x$ is $2(x_0)_{2i+1} + (x_0)_{2i} \ge (x_0)_{2i+1}$. By the subtraction form of the tool, field $i$ of the result is $(x_0)_{2i+1} + (x_0)_{2i} = \nu_i^2$.

**Step L2.** Let $x$ have $F_i^2(x) = \nu_i^2 \le 2$. The word $x \wedge M_2$ has 4-bit field $j$ equal to $F_{2j}^2(x) = \nu_{2j}^2$, since $M_2$ keeps the low 2 bits of each 4-bit field. The word $(x \gg 2) \wedge M_2$ has 4-bit field $j$ equal to $F_{2j+1}^2(x) = \nu_{2j+1}^2$. Their sum per field is $\nu_j^4 \le 4 < 16$. By the tool, $F_j^4$ of the result is $\nu_j^4$.

**Step L3.** Let $x$ have $F_j^4(x) = \nu_j^4 \le 4$. The word $x + (x \gg 4)$ is a sum by 4-bit fields: field $j$ gets $\nu_j^4 + \nu_{j+1}^4 \le 8 < 16$ (with $\nu_{w/4}^4 = 0$ at the top). By the tool, field $j$ of the sum is $\nu_j^4 + \nu_{j+1}^4$. The mask $M_4$ keeps the even 4-bit fields $j = 2k$ and clears the odd ones. So byte $k$ of the result is $\nu_{2k}^4 + \nu_{2k+1}^4 = \nu_k^8$.

**Step L4.** Let $x = \sum_k c_k 2^{8k}$ with $c_k = \nu_k^8 \le 8$ and $m = w/8$ bytes. With $H = \sum_{l=0}^{m-1} 2^{8l}$,
$$ x \cdot H = \sum_{j=0}^{2m-2} \Big( \sum_{k + l = j} c_k \Big) 2^{8j}. $$
For $j \le m - 1$, the coefficient is $s_j = \sum_{k=0}^{j} c_k \le \nu(x_0) \le w \le 128 < 256$. Reduce modulo $2^w = 2^{8m}$: the terms with $j \ge m$ are multiples of $2^w$ and vanish, so $x \cdot H \bmod 2^w = \sum_{j=0}^{m-1} s_j 2^{8j}$. Each $s_j < 256$, so this is the base-256 expansion, and its top byte is $s_{m-1} = \sum_k c_k = \nu(x_0)$. The shift right by $w - 8 = 8(m - 1)$ returns that byte. For $w = 8$, $m = 1$, $H = 1$ and the shift is 0, so the result is $c_0 = \nu(x_0)$ directly.

**Theorem.** For each word $x_0$, SWAR-POPCOUNT$(x_0)$ returns $\nu(x_0)$.

*Proof.* Chain the four steps: after line L1 the 2-bit fields hold $\nu_i^2$, after line L2 the 4-bit fields hold $\nu_j^4$, after line L3 the bytes hold $\nu_k^8$, and line L4 returns $\sum_k \nu_k^8 = \nu(x_0)$. Each step used only the hypothesis given by the step before it. The procedure has no loop, so it stops after a fixed number of operations. $\blacksquare$

**Where the width bound is used.** Step L4 needs $s_j < 256$, which holds because $s_j \le w \le 128$. For $w \ge 256$ a byte cannot hold the count $w$, and the fields must first be doubled to 16 bits.
