---
title: Bob recovers Alice's message in the three-pass protocol
proves: [correctness]
status: full
---

We use the notation of the page. $p$ is prime, so $\mathbb{Z}_p^* = \{1, \dots, p - 1\}$ is a group of order $p - 1$ under multiplication modulo $p$.

**Lemma 1 (the unlock keys exist).** If $\gcd(e, p - 1) = 1$, then there is an integer $e'$ with $e e' \equiv 1 \pmod{p - 1}$, and line L3 computes it.

*Proof.* By Bézout's identity there are integers $s$ and $t$ with $se + t(p - 1) = \gcd(e, p - 1) = 1$, and the extended Euclidean algorithm finds them. Then $e' = s \bmod (p - 1)$ satisfies $ee' \equiv 1 \pmod{p - 1}$. Line L2 only accepts $e$ with $\gcd(e, p - 1) = 1$. $\blacksquare$

**Lemma 2 (a lock and its key cancel).** For every $x \in \mathbb{Z}_p^*$ and every $e$, $e'$ with $ee' \equiv 1 \pmod{p - 1}$, $(x^e)^{e'} \equiv x \pmod p$.

*Proof.* Write $ee' = 1 + k(p - 1)$ with $k \ge 0$. By Fermat's little theorem $x^{p - 1} \equiv 1$, so $(x^e)^{e'} = x^{ee'} = x \cdot (x^{p - 1})^k \equiv x \pmod p$. $\blacksquare$

**Lemma 3 (locks commute).** For all $x$ and all nonnegative integers $a$ and $b$, $(x^a)^b \equiv (x^b)^a \pmod p$.

*Proof.* Both sides equal $x^{ab}$. $\blacksquare$

**Theorem (correctness).** If $2 \le m \le p - 2$ and both parties follow lines L1 to L7, then Bob's value in line L7 equals $m$.

*Proof.* Line L1 passes, and $m \in \mathbb{Z}_p^*$. By lines L4 to L6, $c_3 = ((m^a)^b)^{a'}$. By Lemma 3, $(m^a)^b = (m^b)^a$, so $c_3 = ((m^b)^a)^{a'}$, and Lemma 2 with $x = m^b \in \mathbb{Z}_p^*$ gives $c_3 \equiv m^b \pmod p$. Line L7 computes $c_3^{b'} = (m^b)^{b'}$, which is $m$ by Lemma 2. Since $m < p$, the reduced value is $m$ itself. $\blacksquare$

**Corollary (each message is a bijection of the message).** For fixed locks, the maps $m \mapsto c_1$, $m \mapsto c_2$ and $m \mapsto c_3$ are permutations of $\mathbb{Z}_p^*$.

*Proof.* The map $x \mapsto x^e$ has the inverse $x \mapsto x^{e'}$ by Lemma 2, so it is a permutation, and $c_1$, $c_2 = m^{ab}$ and $c_3 = m^b$ are such maps with $e = a$, $ab$ and $b$, each a unit modulo $p - 1$. $\blacksquare$

**Remark (the one-bit leak).** Since $p - 1$ is even and $\gcd(e, p - 1) = 1$, every lock $e$ is odd. By Euler's criterion the Legendre symbol satisfies $\left(\frac{x^e}{p}\right) = \left(\frac{x}{p}\right)^e = \left(\frac{x}{p}\right)$ for odd $e$, so $c_1$, $c_2$ and $c_3$ all have the Legendre symbol of $m$. This does not affect correctness, but it shows that the protocol hides at most all but one bit of $m$ unless $m$ is restricted to the squares. $\blacksquare$
