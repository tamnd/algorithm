---
title: Okamoto-Uchiyama decryption returns the message, and returns M mod p for any exponent
proves: [correctness]
status: full
---

Let $p \ne q$ be primes of $k$ binary digits, $N = p^2 q$, $\Gamma = \{x \in \mathbb{Z}_{p^2}^* : x \equiv 1 \pmod p\}$ and $L(x) = (x-1)/p$ on $\Gamma$. Let $g$ satisfy $\gcd(g, N) = 1$ and $g_p = g^{p-1} \bmod p^2 \ne 1$, and let $h = g^N \bmod N$ and $\ell = L(g_p)^{-1} \bmod p$.

**Lemma 1.** For every $y \in \mathbb{Z}_{p^2}^*$, $y^{p-1} \bmod p^2 \in \Gamma$.

*Proof.* By Fermat's little theorem $y^{p-1} \equiv 1 \pmod p$. $\square$

**Lemma 2.** $L$ maps $\Gamma$ one to one onto $\{0, \ldots, p-1\}$, and for $x \in \Gamma$ and every integer $e \ge 0$, $L(x^e \bmod p^2) \equiv e \, L(x) \pmod p$.

*Proof.* The elements of $\Gamma$ are $1 + ap$ for $0 \le a < p$, and $L(1 + ap) = a$, so $L$ is a bijection. By the binomial theorem $(1 + ap)^e = 1 + eap + \binom{e}{2}a^2p^2 + \cdots \equiv 1 + (ea \bmod p)\,p \pmod{p^2}$, so $L(x^e \bmod p^2) = ea \bmod p$. $\square$

**Lemma 3.** $L(g_p) \not\equiv 0 \pmod p$, so $\ell$ exists.

*Proof.* $g_p \in \Gamma$ by Lemma 1 and $g_p \ne 1$, so $g_p = 1 + ap$ with $1 \le a < p$, and $L(g_p) = a$. $\square$

**Theorem.** For every integer $M \ge 0$ and every integer $r \ge 0$, let $C = g^M h^r \bmod N$. Then OU-DECRYPT returns $M \bmod p$. In particular, for $0 \le m < 2^{k-1}$ it returns $m$.

*Proof.* Since $p^2 \mid N$, reductions modulo $N$ do not change values modulo $p^2$, so $C \equiv g^{M + Nr} \pmod{p^2}$. Then

$$C^{p-1} \equiv g^{(p-1)M} \cdot g^{N r (p-1)} \pmod{p^2}.$$

The group $\mathbb{Z}_{p^2}^*$ has order $p(p-1)$, and $N(p-1) = pq \cdot p(p-1)$ is a multiple of it, so by Lagrange's theorem the second factor is 1. The first factor is $g_p^M$. By Lemma 2, $L(C^{p-1} \bmod p^2) \equiv M \, L(g_p) \pmod p$. Line L10 multiplies by $\ell = L(g_p)^{-1}$ (Lemma 3) and reduces modulo $p$, which gives $M \bmod p$.

A prime of $k$ binary digits is at least $2^{k-1}$, and $p$ is odd, so $p > 2^{k-1}$. For $0 \le m < 2^{k-1}$ this gives $m \bmod p = m$. $\blacksquare$

**Corollary (the chosen ciphertext attack).** For every $M \ge 0$, $p$ divides $M - \text{OU-DECRYPT}(g^M h^r \bmod N)$. If moreover $q \nmid M - (M \bmod p)$ and $p^2 \nmid M - (M \bmod p)$, then $\gcd(M - (M \bmod p), N) = p$.

*Proof.* The first claim is the theorem. The divisors of $N = p^2 q$ are $1, p, p^2, q, pq, p^2 q$. The gcd is a divisor of $N$ that is a multiple of $p$, so it is one of $p, p^2, pq, p^2q$. The two conditions exclude every choice except $p$. $\square$

**Homomorphism.** For $c_1 = g^{m_1} h^{r_1}$ and $c_2 = g^{m_2} h^{r_2}$, $c_1 c_2 \bmod N = g^{m_1 + m_2} h^{r_1 + r_2} \bmod N$, so by the theorem it decrypts to $(m_1 + m_2) \bmod p$, which is $m_1 + m_2$ when the sum is below $p$.
