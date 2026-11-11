---
title: Goldwasser-Micali decryption returns the encrypted bit
proves: [correctness]
status: full
---

**Setting.** Let $p$ and $q$ be distinct odd primes and $N = pq$ (line L1). Line L2 accepts $y \in \mathbb{Z}_N^*$ only if $y^{(p-1)/2} \not\equiv 1 \pmod p$ and $y^{(q-1)/2} \not\equiv 1 \pmod q$. Encryption of a bit $b$ (lines L5 and L6) outputs $c = y^b r^2 \bmod N$ for some $r \in \mathbb{Z}_N^*$. Decryption (line L9) outputs 0 if $c^{(p-1)/2} \equiv 1 \pmod p$ and 1 otherwise.

**Claim.** For every bit $b$ and every $r \in \mathbb{Z}_N^*$, line L9 returns $b$. Also, the key $y$ of line L2 is a pseudosquare: it is not a square modulo $N$, and its [Jacobi symbol](/jacobi-symbol/) is $\left(\frac{y}{N}\right) = 1$.

*Proof.* We use Euler's criterion.

**Fact (Euler's criterion).** Let $a$ be an integer with $p \nmid a$. Then $a^{(p-1)/2} \equiv 1 \pmod p$ if $a$ is a square modulo $p$, and $a^{(p-1)/2} \equiv -1 \pmod p$ otherwise. *Proof of the fact.* The group $\mathbb{Z}_p^*$ is cyclic of order $p - 1$; let $w$ generate it and write $a \equiv w^k$. The squares are exactly the even powers of $w$: $(w^j)^2 = w^{2j}$, and if $w^k \equiv s^2$ with $s \equiv w^j$, then $k \equiv 2j \pmod{p-1}$, and $p - 1$ is even, so $k$ is even. Now $a^{(p-1)/2} = w^{k(p-1)/2}$. If $k = 2j$, this is $(w^{p-1})^j \equiv 1$. If $k$ is odd, then $p - 1$ does not divide $k(p-1)/2$, so $w^{k(p-1)/2} \not\equiv 1$ because $w$ has order $p - 1$. Its square is $a^{p-1} \equiv 1$, and the only roots of $X^2 - 1$ in the field $\mathbb{Z}_p$ are $1$ and $-1$, so it is $-1$. $\square$

Write $\chi(a) \in \{1, -1\}$ for the value of $a^{(p-1)/2} \bmod p$, read as $1$ or $-1$. By the fact, $\chi(a) = \left(\frac{a}{p}\right)$, the [Legendre symbol](/legendre-symbol/), and $\chi(a a') \equiv (a a')^{(p-1)/2} = a^{(p-1)/2} a'^{(p-1)/2}$, so $\chi(a a') = \chi(a)\chi(a')$.

*Step 1: the key.* Line L2 ensures $\chi(y) \ne 1$, so $\chi(y) = -1$ and $y$ is not a square modulo $p$. A square modulo $N$ would be a square modulo $p$, so $y$ is not a square modulo $N$. In the same way $\left(\frac{y}{q}\right) = -1$, so $\left(\frac{y}{N}\right) = \left(\frac{y}{p}\right)\left(\frac{y}{q}\right) = (-1)(-1) = 1$.

*Step 2: the ciphertext is a unit modulo $p$.* $y$ and $r$ are units modulo $N$, so neither is divisible by $p$, and $c \equiv y^b r^2 \pmod p$ is not divisible by $p$. So the fact applies to $c$.

*Step 3: line L9 returns $b$.* Reducing modulo $p$ does not change $c^{(p-1)/2} \bmod p$. By multiplicativity,

$$\chi(c) = \chi(y)^b \, \chi(r)^2 = (-1)^b \cdot 1 = (-1)^b.$$

If $b = 0$, then $\chi(c) = 1$, the test of line L9 holds, and the line returns 0. If $b = 1$, then $\chi(c) = -1 \ne 1$ and the line returns 1. So line L9 returns $b$ in both cases.

Lines L8 to L10 apply this to each ciphertext of the list in order, so decryption of the output of lines L4 to L7 returns the input bits in order. $\blacksquare$
