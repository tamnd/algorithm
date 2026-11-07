---
title: The Kulisch accumulator holds the exact sum and rounds it correctly
proves: [correctness]
status: full
---

**Setting.** binary64. Every finite float is $x = m \cdot 2^e$ with integers $|m| < 2^{53}$ and $e \ge -1074$, and $|x| < 2^{1024}$. The register is $L = 67$ limbs of 64 bits, $W = 4288$ bits, holding $V$ in two's complement, that is, the limbs encode $V \bmod 2^W$ and $V$ is read as the representative in $[-2^{W-1}, 2^{W-1})$. Write $\Phi = 2148$.

**Lemma 1 (terms are integers on the grid).** For finite floats $a = m_a 2^{e_a}$ and $b = m_b 2^{e_b}$, $ab \cdot 2^{\Phi}$ is an integer $T$ with $|T| < 2^{2048 + \Phi} = 2^{4196}$.

*Proof.* $ab = m_a m_b 2^{e_a + e_b}$ with $e_a + e_b \ge -2148$, so $ab \cdot 2^{\Phi} = m_a m_b 2^{e_a + e_b + 2148}$ is an integer. And $|ab| < 2^{1024} \cdot 2^{1024}$. $\square$

**Lemma 2 (one addition).** Lines L1 to L5 replace the limbs encoding $V \bmod 2^W$ by limbs encoding $(V + T) \bmod 2^W$.

*Proof.* Line L3 writes $|T| = \mathrm{chunk} \cdot 2^{64 i}$ with $s = e + \Phi$ and $i = \lfloor s/64 \rfloor$. The loop of L4 and L5 is schoolbook addition (or subtraction) in base $2^{64}$ starting at limb $i$: after processing limb $j$, the limbs $i, \ldots, j$ and the pending carry represent the correct partial sum, by the usual induction on limbs. It stops when the remaining chunk and the carry are both zero, at which point the higher limbs are unchanged and correct; or at the top limb, where dropping the final carry or borrow is reduction modulo $2^W$. Subtraction modulo $2^W$ is addition of $-|T|$. $\square$

**Theorem 1 (exactness).** If $n < 2^{91}$ terms $T_1, \ldots, T_n$ have been added (each a product, or a float times 1), then the register holds $V = \sum_k T_k$, so $\mathrm{val}(R) = V 2^{-\Phi}$ is the exact sum.

*Proof.* By Lemma 2 the limbs encode $\sum_k T_k \bmod 2^W$. By Lemma 1, $|\sum_k T_k| < n \cdot 2^{4196} < 2^{4287} = 2^{W-1}$, so the sum is itself the two's complement representative. $\square$

**Theorem 2 (rounding).** ROUND returns the binary64 number nearest to $V 2^{-\Phi}$, ties to even, with overflow to $\pm\infty$ when that number would reach $2^{1024}$.

*Proof.* Let $A = |V| > 0$ with bit length $k$, so $2^{k-1} \le A < 2^k$ and the leading bit of $\mathrm{val}(R)$ has exponent $k - 1 - \Phi$. If $k - 1 - \Phi \ge -1022$ (normal range), the binary64 numbers in that binade are the multiples of $2^{k - 53 - \Phi}$, that is, $A$ must be rounded to a multiple of $2^{k - 53}$. If the leading exponent is below $-1022$ (subnormal range), the representable numbers are the multiples of $2^{-1074}$, that is, $A$ must be rounded to a multiple of $2^{\Phi - 1074}$. Line L7 takes $d = \max(k - 53, \Phi - 1074)$, which is the larger of the two exponents and hence the correct quantum in both cases (the normal case has $k - 53 \ge \Phi - 1074$ exactly when $k - 1 - \Phi \ge -1022$). If $d \le 0$, then $A$ is already a multiple of the quantum (this cannot happen with $\Phi = 2148$, since $\Phi - 1074 > 0$, but the code allows it). Otherwise, write $A = q 2^d + r$ with $0 \le r < 2^d$; the two neighbours are $q 2^d$ and $(q + 1)2^d$, the midpoint is at $r = 2^{d-1}$, and line L8 chooses $q + 1$ iff $r > 2^{d-1}$, or $r = 2^{d-1}$ and $q$ is odd. That is round to nearest, ties to even. A carry from $q$ to $q + 1 = 2^{53}$ moves the result to the next binade, where it is still representable as $2^{53} \cdot 2^{d - \Phi}$. Finally, the rounded value $q \cdot 2^{d - \Phi}$ is at least $2^{1024}$ exactly when $q$'s bit length plus $d - \Phi$ exceeds 1024, the test of line L9, and IEEE 754 round to nearest then returns $\pm\infty$. Since $q < 2^{54}$ and the scaling is by a power of two within range, `ldexp` is exact. The sign is applied last, which is correct because round to nearest, ties to even, is symmetric. $\square$

**Special values.** Inputs that are not finite never reach the register. The flags implement the IEEE rules for a sum: any NaN, or both infinities, gives NaN; otherwise any infinity gives that infinity. A product with a non-finite factor is formed in floating point first, so $\infty \cdot 0$ sets the NaN flag.
