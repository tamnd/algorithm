---
title: Folding keeps the value modulo P, and Barrett reduction over GF(2) gives the exact remainder
proves: [correctness, termination]
status: full
---

Notation. All polynomials are in GF(2)[x], and a word is the polynomial with bit $i$ as the coefficient of $x^i$. $P = x^{32} + \text{poly}$. The bytes, after the reversal of each byte when refin is true, form the polynomial $M$ of $k = 8n$ bits, first bit highest. $I$ is init. By the [cyclic redundancy check](/cyclic-redundancy-check/) page the register to compute is $\mathrm{reg} = (I x^k + M x^{32}) \bmod P$.

**Lemma 1 (fold).** Let $X = H x^{64} + L$ with $\deg H, \deg L < 64$, let $k_a = x^{T+64} \bmod P$ and $k_b = x^{T} \bmod P$. Then $F = H k_a + L k_b$ satisfies $F \equiv X x^T \pmod P$ and $\deg F < 96$.

*Proof.* $X x^T = H x^{T+64} + L x^T \equiv H k_a + L k_b$. Each product has degree less than $64 + 32 = 96$. $\square$

So a fold followed by an XOR of the next 128-bit chunk $C$ maps $X$ to a value congruent to $X x^{128} + C$ when $T = 128$, and to $X x^{512} + C$ when $T = 512$. The result has degree less than 128, so it fits in a 128-bit register again.

**Lemma 2 (Barrett over GF(2)).** Let $\deg t < 64$, write $t = t_h x^{32} + t_l$ with $\deg t_l < 32$, and let $\mu = \lfloor x^{64} / P \rfloor$. Let $q = \lfloor t_h \mu / x^{32} \rfloor$. Then $t + qP = t \bmod P$. No correction step is necessary.

*Proof.* Write $x^{64} = \mu P + \rho$ with $\deg \rho < 32$, and $t_h \mu = q x^{32} + s$ with $\deg s < 32$. Then
$$(t + qP)\, x^{32} = t_h x^{64} + t_l x^{32} + q x^{32} P = t_h \mu P + t_h \rho + t_l x^{32} + (t_h \mu + s) P = t_h \rho + t_l x^{32} + s P,$$
because the two terms $t_h \mu P$ cancel in characteristic 2. Each of the three terms has degree less than 64: $\deg t_h + \deg \rho < 32 + 32$, $\deg t_l + 32 < 64$, and $\deg s + 32 < 64$. So $\deg(t + qP) < 32$. Since $t + qP \equiv t \pmod P$, it is the remainder. $\square$

Lines L9 and L10 compute this: $t_h$ is `t >> 32`, the product with $\mu$ shifted right by 32 is $q$, and the low 32 bits of $t \oplus qP$ are $t + qP$, which has degree less than 32 by the lemma.

Over the integers the same method can leave a remainder that is too large by a small multiple of the modulus, and needs a final subtraction. Over GF(2) there are no carries, so the degree count above is exact.

**Theorem.** `crc32_fold` returns the CRC with the given parameters.

*Proof.* Case $k \ge 32$. Line L1 sets $V = M + I x^{k-32}$, so $V x^{32} = M x^{32} + I x^k$, and the result must be $V x^{32} \bmod P$. Zero bits added at the high end of $V$ do not change it, so $V = \sum_{i=0}^{N-1} C_i\, x^{128(N-1-i)}$ for the $N$ chunks $C_i$ of 128 bits.

Invariant of the loop of line L3: after the chunks $C_0, \ldots, C_{p-1}$ are used, the four accumulators satisfy
$$\sum_{j=0}^{3} A_j\, x^{128(3-j)} \equiv \sum_{i<p} C_i\, x^{128(p-1-i)} \pmod P.$$
At line L2, $A_j = C_j$ and $p = 4$, so it holds. One round maps $A_j$ to $F_j + C_{p+j}$ with $F_j \equiv A_j x^{512}$ by Lemma 1, so the left side becomes congruent to (old left side)$\cdot x^{512} + \sum_j C_{p+j} x^{128(3-j)}$, which is the right side for $p + 4$.

Line L4 folds the four accumulators into one value $X \equiv \sum_j A_j x^{128(3-j)}$ by Horner's rule with $T = 128$ (Lemma 1). Line L5 adds the remaining chunks by Horner's rule with $T = 128$. When $N < 4$, the same steps start from $C_0$. After line L5, $X \equiv V \pmod P$ and $\deg X < 128$.

Line L6 writes $X = H x^{64} + L$ and computes $t_{96} = H \cdot (x^{96} \bmod P) + L x^{32} \equiv X x^{32}$, of degree less than 96. Line L7 writes $t_{96} = A x^{64} + B$ with $\deg A < 32$ and computes $t = A \cdot (x^{64} \bmod P) + B \equiv t_{96}$, of degree less than 64. By Lemma 2, line L8 gives $t \bmod P = V x^{32} \bmod P$. Line L11 applies refout and xorout, as in the bit-by-bit CRC.

Case $k < 32$. The value $I x^k + M x^{32}$ has degree less than 64, and Lemma 2 reduces it directly. $\square$

**The constants.** $k_1, \ldots, k_6$ and $\mu$ come from GF(2) division of a power of $x$ by $P$. The tests compare them with the values in the white paper for the IEEE polynomial, both the normal ones and the reflected ones of the gzip example.

**Termination.** There are $\lceil k / 128 \rceil$ chunks. Each round of line L3 uses 4 of them, each step of lines L4 and L5 a fixed number, and lines L6 to L11 run once.
