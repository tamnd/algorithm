---
title: Schrage's step is exact and the minimal standard generator has period m − 1
proves: [correctness]
status: full
---

Let $m = 2^{31} - 1$, $a = 16807$, $q = \lfloor m / a \rfloor = 127773$ and $r = m \bmod a = 2836$, so that $m = aq + r$ and $0 \le r < a$.

**Lemma 1 (Schrage).** Let $m$ and $a$ be positive integers with $a < m$, and let $q$ and $r$ be as above with $r \le q$. For every integer $x$ with $0 \le x \le m - 1$, the value $t = a (x \bmod q) - r \lfloor x / q \rfloor$ of line L2 satisfies $-m < t < m$ and $t \equiv a x \pmod m$. So lines L2 and L3 return $a x \bmod m$.

*Proof.* Write $x = q h + \ell$ with $h = \lfloor x / q \rfloor$ and $\ell = x \bmod q$, so $0 \le \ell \le q - 1$.

1. *Congruence.* $a x = a q h + a \ell = (m - r) h + a \ell = m h + (a \ell - r h) = m h + t$. So $t \equiv a x \pmod m$.
2. *Upper bound.* $t \le a \ell \le a (q - 1) < a q \le m$.
3. *Lower bound.* $t \ge -r h$. Since $r \le q$, $r h \le q h \le x \le m - 1$, so $t \ge -(m - 1) > -m$.
4. *Range of each product.* $0 \le a \ell < m$ by step 2, and $0 \le r h < m$ by step 3. So both products of line L2 lie in $[0, m)$ and fit in a signed 31-bit word, and so does their difference.

By steps 1 to 3, $t \in (-m, m)$ and $t \equiv a x$. If $t \ge 0$, then $t = a x \bmod m$. If $t < 0$, line L3 gives $t + m \in (0, m)$, which is congruent to $a x$, so it is $a x \bmod m$. $\square$

For the minimal standard, $r = 2836 \le q = 127773$, so Lemma 1 applies. It also applies to $a = 48271$, where $q = 44488$ and $r = 3399$.

**Lemma 2.** Let $p$ be a prime and let $a$ be an integer with $p \nmid a$. Then the order of $a$ in the multiplicative group modulo $p$ is $p - 1$ if and only if $a^{(p-1)/\ell} \not\equiv 1 \pmod p$ for every prime $\ell$ that divides $p - 1$.

*Proof.* Let $d$ be the order of $a$. By Fermat's little theorem $a^{p-1} \equiv 1$, so $d \mid p - 1$. If $d = p - 1$, then no proper divisor $(p-1)/\ell$ is a multiple of $d$, so $a^{(p-1)/\ell} \not\equiv 1$. If $d < p - 1$, then $(p - 1)/d > 1$ has a prime factor $\ell$, and $d \mid (p-1)/\ell$, so $a^{(p-1)/\ell} \equiv 1$. $\square$

**Theorem.** For each seed $x_0 \in \{1, \ldots, m - 1\}$, the sequence $x_{i+1} = a x_i \bmod m$ of PARK-MILLER-NEXT stays in $\{1, \ldots, m-1\}$, and its period is exactly $m - 1$. The sequence visits every element of $\{1, \ldots, m - 1\}$ once in each period.

*Proof.* The number $m = 2^{31} - 1$ is prime. By Lemma 1, each call returns $a x_i \bmod m$. Since $m$ is prime and $m \nmid a$, $m \nmid x_i$, the product $a x_i$ is not divisible by $m$, so $x_{i+1} \ne 0$. By induction, $x_i = a^i x_0 \bmod m$ for all $i \ge 0$.

Now $x_{i + k} = x_i$ if and only if $a^k x_i \equiv x_i \pmod m$. Since $x_i$ is invertible modulo the prime $m$, this holds if and only if $a^k \equiv 1$. So the period is the order of $a$ modulo $m$.

The factorization $m - 1 = 2 \cdot 3^2 \cdot 7 \cdot 11 \cdot 31 \cdot 151 \cdot 331$ holds by multiplication. The seven values $16807^{(m-1)/\ell} \bmod m$, for $\ell \in \{2, 3, 7, 11, 31, 151, 331\}$, are each different from 1; they are computed exactly by [modular exponentiation](/modular-exponentiation/) in the tests of the implementation. By Lemma 2, the order of $a$ is $m - 1$. So the period is $m - 1$, and the $m - 1$ states $x_0, \ldots, x_{m-2}$ are distinct elements of a set of size $m - 1$, which means each one appears once. $\blacksquare$

**Remark.** The same proof shows that $16807 = 7^5$ is a primitive root because 7 is one and $\gcd(5, m - 1) = 1$: the order of $7^5$ is $(m-1)/\gcd(5, m-1)$.
