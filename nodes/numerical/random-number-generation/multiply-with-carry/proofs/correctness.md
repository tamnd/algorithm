---
title: A lag-1 multiply-with-carry generator is a multiplicative LCG modulo a b - 1, so its period is the order of b
proves: [correctness]
status: full
---

Fix integers $b \ge 2$ (the base, $2^{32}$ in practice) and $a \ge 1$ (the multiplier), and put $m = a b - 1$. A state is a pair $(x, c)$ of integers with $0 \le x < b$ and $0 \le c < a$. MWC-NEXT computes $t = a x + c$ (line L1), $x' = t \bmod b$ (line L2) and $c' = \lfloor t / b \rfloor$ (line L3), and outputs $x'$.

**Lemma 1 (the carry stays small).** If $0 \le x < b$ and $0 \le c < a$, then $0 \le c' < a$. So the state set is closed under the step.

*Proof.* $t \le a(b - 1) + (a - 1) = a b - 1$, so $c' = \lfloor t / b \rfloor \le \lfloor (a b - 1)/b \rfloor = a - 1$. $\square$

**Lemma 2 (the coding).** The map $\phi(x, c) = a x + c$ is a bijection from the state set onto $\{0, 1, \ldots, m\}$, with inverse $z \mapsto (\lfloor z / a \rfloor, z \bmod a)$.

*Proof.* This is division with remainder by $a$: every $z$ with $0 \le z \le a b - 1 = m$ is $a x + c$ for exactly one pair with $0 \le c < a$, and then $0 \le x \le \lfloor m / a \rfloor = b - 1$. $\square$

**Lemma 3 (the step is multiplication by $a$).** Let $z = \phi(x, c)$ and $z' = \phi(x', c')$. Then $b z' = m x' + z$, so $z' \equiv a z \pmod m$. Moreover $z = 0$ and $z = m$ are fixed points, and for $0 < z < m$ we have $z' = a z \bmod m$ exactly.

*Proof.* By lines L1 to L3, $t = b c' + x'$ and $t = z$. Then

$$b z' = a b x' + b c' = (m + 1) x' + (t - x') = m x' + z.$$

Since $a b = m + 1 \equiv 1 \pmod m$, $a$ is the inverse of $b$ modulo $m$, and multiplying by $a$ gives $z' \equiv a z \pmod m$. If $z = 0$ then $x = c = 0$, $t = 0$ and $z' = 0$. If $z = m$ then $x = b - 1$ and $c = a - 1$, $t = m$, $x' = m \bmod b = b - 1$ and $c' = a - 1$, so $z' = m$. If $0 < z < m$, then $a z \not\equiv 0 \pmod m$ because $a$ is invertible modulo $m$, so $z' \notin \{0, m\}$; as $0 \le z' \le m$ by Lemma 2, $z'$ is the unique residue in $(0, m)$ congruent to $a z$, that is $z' = a z \bmod m$. $\square$

**Theorem.** Let $(x_0, c_0)$ be a state with $z_0 = a x_0 + c_0 \notin \{0, m\}$ and put $g = \gcd(z_0, m)$. Then:

1. $z_n = a^n z_0 \bmod m$ and the output is $x_n = \lfloor z_n / a \rfloor$, so the generator is the multiplicative [linear congruential generator](/linear-congruential-generator/) with multiplier $a$ and modulus $m$, read through the output map $z \mapsto \lfloor z / a \rfloor$.
2. The state sequence is purely periodic, and its period is the multiplicative order of $a$ modulo $m / g$. When $g = 1$, for instance for every $z_0 \in (0, m)$ when $m$ is prime, the period is the order of $b$ modulo $m$.
3. If $b$ is a square modulo $m$ (for instance $b = 2^{32}$), then the period divides $(m - 1)/2$ when $m$ is prime. If moreover $m$ is a safe prime, that is $q = (m - 1)/2$ is prime, and $b \not\equiv 1 \pmod m$, the period is exactly $q$ for every $z_0 \in (0, m)$.

*Proof.* (1) By Lemma 3 and induction, using that $(0, m)$ is closed under the step. The output formula is the inverse in Lemma 2.

(2) By Lemma 2, the state returns to $(x_0, c_0)$ after $k \ge 1$ steps if and only if $z_k = z_0$, that is, $m \mid (a^k - 1) z_0$. Write $z_0 = g z_1$ and $m = g m_1$ with $\gcd(z_1, m_1) = 1$; the condition becomes $m_1 \mid (a^k - 1) z_1$, that is $m_1 \mid a^k - 1$. Since $\gcd(a, m) = 1$, $a$ has an order modulo $m_1$, and the least such $k$ is that order. Pure periodicity holds because $z \mapsto a z \bmod m$ is a bijection of $(0, m)$. When $g = 1$, the period is the order of $a$ modulo $m$, which equals the order of $b$ because $a = b^{-1}$ modulo $m$ and an element and its inverse have the same order.

(3) If $m$ is prime and $b \equiv s^2 \pmod m$, then $b^{(m-1)/2} \equiv s^{m-1} \equiv 1$ by Fermat's little theorem, so the order of $b$ divides $(m - 1)/2$. If $q = (m - 1)/2$ is prime, the order is 1 or $q$, and it is not 1 since $b \not\equiv 1$. By (2), with $g = 1$, every $z_0 \in (0, m)$ has period $q$. $\blacksquare$

The tests check the theorem exhaustively for all multipliers $2 \le a < b$ with $b \in \{8, 16, 32\}$, check (3) for $a = 4294957665$ and $a = 698769069$ with $b = 2^{32}$ and for Marsaglia's 16-bit multipliers 36969 and 18000 with $b = 2^{16}$, using the Miller-Rabin test with the first 13 prime bases, which is exact below $3.3 \cdot 10^{24}$, and check the jump formula $z_{n + k} = a^k z_n \bmod m$ against stepping. For the lag-$r$ generator, $m = a b^r - 1$; the tests only check by brute force on small cases that every cycle length divides the order of $b$ modulo $m$ and that this order is reached, as Couture and L'Ecuyer prove in general.
