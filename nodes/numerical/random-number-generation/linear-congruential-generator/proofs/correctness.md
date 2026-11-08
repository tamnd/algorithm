---
title: The linear congruential generator computes its recurrence, and Schrage's method is exact
proves: [correctness]
status: full
---

We use the pseudocode of the page. The parameters are integers $m \ge 2$, $0 < a < m$ and $0 \le c < m$, and $f(s) = (a s + c) \bmod m$ on $S = \{0, \ldots, m-1\}$.

**Lemma 1 (the state sequence).** After LCG-SEED$(x)$ and $i$ calls of LCG-NEXT, the state is $s_i$, where $s_0 = x \bmod m$ and $s_{j+1} = f(s_j)$. The $i$-th call returns $s_i$.

*Proof.* By induction on $i$. Line L1 sets $s = s_0$. If $s = s_i$ before a call, line L3 sets $s$ to $(a s_i + c) \bmod m = f(s_i) = s_{i+1}$, and line L4 returns it. When $m = 2^w$, the implementation replaces the remainder by the mask $t \mathbin{\&} (2^w - 1)$. For $t \ge 0$, write $t = q 2^w + r$ with $0 \le r < 2^w$; the low $w$ binary digits of $t$ are the digits of $r$, so the mask gives $r = t \bmod 2^w$. $\square$

**Lemma 2 (closed form).** For all $n \ge 0$,

$$s_n \equiv a^n s_0 + c \, (1 + a + \cdots + a^{n-1}) \pmod m.$$

*Proof.* For $n = 0$ the sum is empty and $s_0 \equiv s_0$. If the formula holds for $n$, then $s_{n+1} \equiv a s_n + c \equiv a^{n+1} s_0 + c\,(a + a^2 + \cdots + a^n) + c$, which is the formula for $n + 1$. $\square$

Lemma 2 is the base of [jump-ahead](/jump-ahead/): $s_{i+n}$ depends on $s_i$ through the same formula with $s_0$ replaced by $s_i$.

**Lemma 3 (the forbidden seed).** If $c = 0$, then $f(0) = 0$, so the seed 0 gives the constant sequence $0, 0, \ldots$ with period 1. If $c = 0$ and $\gcd(a, m) = 1$, then $\gcd(s_i, m) = \gcd(s_0, m)$ for all $i$; in particular a seed coprime to $m$ never leads to 0. Line L2 rejects the seed 0 when $c = 0$.

*Proof.* $f(0) = a \cdot 0 \bmod m = 0$. For the second claim, $\gcd(a s, m) = \gcd(s, m)$ when $\gcd(a, m) = 1$, and $\gcd(a s \bmod m, m) = \gcd(a s, m)$ because the two numbers differ by a multiple of $m$. Apply this at each step. $\square$

**Lemma 4 (Schrage's method).** Let $q = \lfloor m / a \rfloor$ and $r = m \bmod a$, and assume $r < q$. For each $x$ with $0 \le x < m$, lines L6 to L8 return $a x \bmod m$, and each intermediate value lies in the open interval $(-m, m)$.

*Proof.* Put $k = \lfloor x / q \rfloor$ and $j = x \bmod q$, so $x = qk + j$. Then $a x = a q k + a j = (m - r) k + a j$, so $a x \equiv a j - r k \pmod m$. For the bounds: $0 \le a j \le a (q - 1) < a q \le m$. Also $k \le x / q < m / q$, so $0 \le r k < r m / q < m$ because $r < q$. Hence $t = a j - r k$ lies in $(-m, m)$. If $t \ge 0$, then $t \in [0, m)$ and $t \equiv a x$, so $t = a x \bmod m$. If $t < 0$, line L7 gives $t + m \in [0, m)$, which is again congruent to $a x$. $\square$

For $m = 2^{31} - 1$, the multiplier $16807$ gives $q = 127773$ and $r = 2836$, and $48271$ gives $q = 44488$ and $r = 3399$, so $r < q$ in both cases and every product fits in a signed 32-bit word.

**Lemma 5 (the uniform output).** LCG-UNIFORM returns a value in $[0, 1)$, also in binary64 floating point.

*Proof.* The state $x$ is in $[0, m - 1]$. If $m \le 2^{53}$, then $x / m \le 1 - 1/m \le 1 - 2^{-53}$, and $1 - 2^{-53}$ is a binary64 number. Correct rounding is monotone and leaves a representable number unchanged, so the computed quotient is at most $1 - 2^{-53} < 1$. If $m = 2^w$ with $w > 53$, the implementation returns $\lfloor x / 2^{w - 53} \rfloor \cdot 2^{-53}$, an integer in $[0, 2^{53} - 1]$ times $2^{-53}$, which is exact and at most $1 - 2^{-53}$. $\square$

**Theorem.** The procedures of the page return the sequence $s_1, s_2, \ldots$ of the recurrence (Lemma 1), with values in $[0, m)$, and the uniform values $s_i / m$ or their 53-bit truncations in $[0, 1)$ (Lemma 5). With Schrage's method in place of line L3 (for $c = 0$ and $r < q$), the sequence is the same (Lemma 4). $\blacksquare$
