---
title: Paillier decryption inverts encryption, and the ciphertexts add
proves: [correctness]
status: full
---

Let $p \ne q$ be primes with $\gcd(pq, (p-1)(q-1)) = 1$, $N = pq$, $\lambda = \operatorname{lcm}(p-1, q-1)$ and $\mu = \lambda^{-1} \bmod N$.

**Lemma 1.** $\gcd(\lambda, N) = 1$, so $\mu$ exists.

*Proof.* $\lambda$ divides $(p-1)(q-1)$, and $\gcd(N, (p-1)(q-1)) = 1$ by the choice of $p$ and $q$. So every common divisor of $\lambda$ and $N$ divides 1. $\square$

**Lemma 2.** For every integer $x \ge 0$, $(1 + N)^x \equiv 1 + xN \pmod{N^2}$.

*Proof.* By the binomial theorem, $(1+N)^x = \sum_{j=0}^{x} \binom{x}{j} N^j$. Each term with $j \ge 2$ has the factor $N^2$. The terms $j = 0$ and $j = 1$ give $1 + xN$. $\square$

**Lemma 3.** For every $w \in \mathbb{Z}_{N^2}^*$, $w^{N\lambda} \equiv 1 \pmod{N^2}$.

*Proof.* The group $\mathbb{Z}_{p^2}^*$ has order $p(p-1)$, and $p(p-1)$ divides $N\lambda$, because $p \mid N$ and $(p-1) \mid \lambda$. By Lagrange's theorem $w^{N\lambda} \equiv 1 \pmod{p^2}$. In the same way $w^{N\lambda} \equiv 1 \pmod{q^2}$. Since $\gcd(p^2, q^2) = 1$, the Chinese remainder theorem gives $w^{N\lambda} \equiv 1 \pmod{N^2}$. $\square$

**Theorem (correctness).** For every $m \in \mathbb{Z}_N$ and every $r \in \mathbb{Z}_N^*$, the ciphertext $c = (1 + mN) r^N \bmod N^2$ passes the test of line L8, and line L10 returns $m$.

*Proof.* $r$ is prime to $N$, so $r^N$ is a unit modulo $N^2$. $1 + mN$ is prime to $N$ because it is $1$ modulo $N$. So $c \in \mathbb{Z}_{N^2}^*$, and $0 < c < N^2$ after the reduction, so line L8 accepts.

By Lemma 2, $1 + mN \equiv (1+N)^m$. So

$$c^\lambda \equiv (1+N)^{m\lambda} \, r^{N\lambda} \equiv (1 + m\lambda N) \cdot 1 \pmod{N^2},$$

by Lemma 2 for the first factor and Lemma 3 for the second. Let $u = c^\lambda \bmod N^2$ (line L9) and let $t = m\lambda \bmod N$. Then $u \equiv 1 + tN \pmod{N^2}$ with $0 \le t < N$, so $1 + tN < N^2$ and $u = 1 + tN$ as integers. The division of line L10 is exact and gives $(u - 1)/N = t$. Finally $t \mu \equiv m \lambda \lambda^{-1} \equiv m \pmod N$, by Lemma 1. Since $0 \le m < N$, line L10 returns $m$. $\blacksquare$

**Theorem (homomorphism).** Let $c_1$ and $c_2$ encrypt $m_1$ and $m_2$ with randomness $r_1$ and $r_2$, and let $k \ge 0$ be an integer. Then $c_1 c_2 \bmod N^2$ is the encryption of $(m_1 + m_2) \bmod N$ with randomness $r_1 r_2 \bmod N$, and $c_1^k \bmod N^2$ is the encryption of $k m_1 \bmod N$ with randomness $r_1^k \bmod N$.

*Proof.* By Lemma 2, $c_1 c_2 \equiv (1+N)^{m_1 + m_2} (r_1 r_2)^N$. The value $(1+N)^x \bmod N^2 = 1 + (x \bmod N) N$ depends only on $x \bmod N$, by Lemma 2. The value $s^N \bmod N^2$ depends only on $s \bmod N$, because $(s + jN)^N \equiv s^N \pmod{N^2}$ by the binomial theorem (each later term has the factor $N \cdot N$). So $c_1 c_2$ equals the output of line L6 for the message $(m_1 + m_2) \bmod N$ and the randomness $r_1 r_2 \bmod N$, which is a unit. The same argument with $c_1^k \equiv (1+N)^{k m_1} (r_1^k)^N$ gives the second claim. By the correctness theorem, both results decrypt to the stated messages. $\blacksquare$
