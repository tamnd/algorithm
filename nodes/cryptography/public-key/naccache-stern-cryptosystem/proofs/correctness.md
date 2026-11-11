---
title: Naccache-Stern decryption returns the message
proves: [correctness]
status: full
---

Let $p_1, \ldots, p_k$ be distinct odd primes, $u = p_1 \cdots p_{k/2}$, $v = p_{k/2+1} \cdots p_k$ and $\sigma = uv$. Let $a \ne b$ be primes different from every $p_i$ and from 2, such that $p = 2au + 1$ and $q = 2bv + 1$ are prime. Let $N = pq$ and $\varphi = (p-1)(q-1) = 4abuv$.

**Lemma 1.** The group $\mathbb{Z}_N^*$ contains a square $g$ of order $\varphi/4$, and the test of line L5 recognizes such a $g$.

*Proof.* The groups $\mathbb{Z}_p^*$ and $\mathbb{Z}_q^*$ are cyclic, of orders $2au$ and $2bv$. Let $\alpha$ and $\beta$ generate them, and by the Chinese remainder theorem let $h \in \mathbb{Z}_N^*$ satisfy $h \equiv \alpha \pmod p$ and $h \equiv \beta \pmod q$. Then $h^2$ has order $au$ modulo $p$ and $bv$ modulo $q$. The numbers $au$ and $bv$ are coprime, because all the primes $a, b, p_1, \ldots, p_k$ are distinct, so $h^2$ has order $abuv = \varphi/4$ in $\mathbb{Z}_N^*$.

For the test: the order of every square divides $\mathrm{lcm}(au, bv) = \varphi/4$. The number $\varphi/4$ is a product of distinct primes. An element $g$ whose order divides $\varphi/4$ has order exactly $\varphi/4$ if and only if $g^{\varphi/(4f)} \ne 1$ for every prime $f$ of $\varphi/4$. Line L5 checks this condition for $f \in \{p_1, \ldots, p_k, a, b\}$. $\square$

**Lemma 2.** For each $i$, $g_i = g^{\varphi/p_i} \bmod N$ has order exactly $p_i$.

*Proof.* Write $\varphi/4 = p_i t$, so $\varphi / p_i = 4t$. The order of $g^{4t}$ is $(\varphi/4)/\gcd(\varphi/4, 4t) = p_i t / \gcd(p_i t, 4t)$. Since $p_i$ is odd, $\gcd(p_i, 4) = 1$, so $\gcd(p_i t, 4t) = t$ and the order is $p_i$. $\square$

**Theorem.** For every $m \in \{0, \ldots, \sigma - 1\}$ and every $x \in \mathbb{Z}_N^*$, NS-DECRYPT applied to $c = g^m x^\sigma \bmod N$ returns $m$.

*Proof.* Fix $i$. Line L10 computes

$$c_i = c^{\varphi/p_i} = g^{m \varphi/p_i} \cdot x^{\sigma \varphi / p_i} = g_i^{m} \cdot \left(x^{\varphi}\right)^{\sigma/p_i} \pmod N.$$

Since $p_i \mid \sigma$, $\sigma / p_i$ is an integer, and $x^\varphi = 1$ by Euler's theorem, so $c_i = g_i^m = g_i^{m \bmod p_i}$ by Lemma 2. The values $g_i^0, \ldots, g_i^{p_i - 1}$ are distinct by Lemma 2, so line L11 finds exactly $m_i = m \bmod p_i$.

The $p_i$ are distinct primes, so they are pairwise coprime and their product is $\sigma$. By the Chinese remainder theorem there is exactly one $m' \in \{0, \ldots, \sigma - 1\}$ with $m' \equiv m_i \pmod{p_i}$ for all $i$. The message $m$ is such a number, so line L12 returns $m' = m$. $\blacksquare$

**Homomorphism.** For $c_1 = g^{m_1} x_1^\sigma$ and $c_2 = g^{m_2} x_2^\sigma$, $c_1 c_2 = g^{m_1 + m_2} (x_1 x_2)^\sigma$. Write $m_1 + m_2 = (m_1 + m_2 \bmod \sigma) + j\sigma$ with $j \in \{0, 1\}$; then $c_1 c_2 = g^{(m_1 + m_2) \bmod \sigma} (g^j x_1 x_2)^\sigma$, which is an encryption of $(m_1 + m_2) \bmod \sigma$, so by the theorem it decrypts to that value. The same argument with $c^e = g^{em} (x^e)^\sigma$ shows that $c^e$ decrypts to $em \bmod \sigma$.
