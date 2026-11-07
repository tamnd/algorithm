---
title: Dekker's TwoProduct returns the exact error of a rounded product
proves: [correctness]
status: full
---

**Setting.** Radix 2, precision $p \ge 4$, round to nearest with a symmetric tie rule, $s = \lceil p/2 \rceil$, and normal floats $a$, $b$ with $e_a + e_b \ge e_{\min} + p - 1$. No operation overflows. We use one fact.

- **(F1)** If $U \ge 2^{e_{\min} - p + 1}$ is a power of two and $k$ is an integer with $|k| \le 2^p$, then $kU$ is a float (when it does not overflow).

**Theorem.** Lines L1 to L7 return $x = \mathrm{fl}(ab)$ and $y = ab - x$ exactly.

*Proof.* Multiplying $a$ or $b$ by a power of two, or negating it, scales every intermediate value by the same factor, as long as no unit drops below the subnormal spacing; Step 6 checks that. So assume $1 \le a, b < 2$ and write $q = 2^{1-p}$, so $a$ and $b$ are multiples of $q$.

**Step 1: the parts.** By the theorem on [Veltkamp splitting](/veltkamp-splitting/) with split point $s$, $a = a_h + a_l$ with $a_h = k_a 2^s q$, $|k_a| \le 2^{p-s}$, $|a_h| \le 2$, and $a_l = m_a q$ with $|m_a| \le 2^{s-1}$; the same holds for $b$.

**Step 2: the products of parts are exact.** $a_h b_h = k_a k_b\, 2^{2s} q^2$ with $|k_a k_b| \le 2^{2p - 2s} \le 2^p$ because $2s \ge p$. $a_h b_l = k_a m_b\, 2^s q^2$ with $|k_a m_b| \le 2^{p-1}$, and likewise $a_l b_h$. $a_l b_l = m_a m_b\, q^2$ with $|m_a m_b| \le 2^{2s - 2} \le 2^{p-1}$ because $2s \le p + 1$. By (F1) all four are floats, so the inner multiplications in lines L4 to L7 are exact. In size, $|a_h b_l|, |a_l b_h| \le 2^s q$ and $|a_l b_l| \le 2^{2s-2} q^2 = 2^{2s - 1 - p} q \le q$.

**Step 3: the rounding error of $x$.** $ab \in [1, 4)$, so $\mathrm{ulp}(x) \le 2q$ and $|ab - x| \le q$. Also $x$ is a multiple of $q$.

**Step 4: lines L4, L5 and L6 are exact.** Since $ab = a_h b_h + a_h b_l + a_l b_h + a_l b_l$,

$$a_h b_h - x = (ab - x) - a_h b_l - a_l b_h - a_l b_l.$$

- $a_h b_h$ is a multiple of $2^{2s+1-p} q$, and $2s + 1 - p \ge 1$, so $a_h b_h - x$ is a multiple of $q$. Its size is at most $q + 2 \cdot 2^s q + q = (2^{s+1} + 2) q$. Since $s + 1 \le p - 1$ for $p \ge 4$, $2^{s+1} + 2 \le 2^p$ and by (F1) $t_1 = a_h b_h - x$ exactly.
- Let $q' = 2^{s+1-p} q = 2^s q^2$; $q$ is a multiple of $q'$, and so are $a_h b_l$ and $a_l b_h$. The exact value $t_1 + a_h b_l = (ab - x) - a_l b_h - a_l b_l$ is a multiple of $q'$ of size at most $(2^s + 2)q = (2^s + 2) 2^{p-s-1} q'$. That integer factor is $2^{p-1} + 2^{p-s} \le 2^p$, so $t_2 = t_1 + a_h b_l$ exactly.
- The exact value $t_2 + a_l b_h = (ab - x) - a_l b_l$ is a multiple of $q'$ of size at most $2q = 2^{p-s} q'$, so $t_3 = t_2 + a_l b_h$ exactly.

**Step 5: line L7 is exact.** $t_3 + a_l b_l = ab - x$ is a multiple of $q^2$ (both terms are) with $|ab - x| \le q = 2^{p-1} q^2$. By (F1) it is a float, so $y = ab - x$ exactly.

**Step 6: the exponent condition.** Before scaling, the finest unit used is $q^2$ times $2^{e_a + e_b}$, that is $2^{e_a + e_b + 2 - 2p}$. (F1) requires it to be at least $2^{e_{\min} - p + 1}$, which is $e_a + e_b \ge e_{\min} + p - 1$. The coarser units $q'$ and $q$ then satisfy (F1) too, and the splits operate on normal $a$ and $b$. $\square$

**The FMA variant.** With $x$ any faithful rounding of $ab$ (in particular round to nearest with any tie rule), $|ab - x| < \mathrm{ulp}(x) \le 2q = 2^p q^2$, and $ab - x$ is a multiple of $q^2$, so under the same exponent condition it is a float by (F1). The FMA computes $\mathrm{fl}(ab - x)$ with one rounding, and the rounding of a float is that float, so $\mathrm{fma}(a, b, -x) = ab - x$. This needs no split and so no condition on overflow of $Ca$, only that $ab$ does not overflow.
