---
title: The one-time pad decrypts correctly and is perfectly secret, and key reuse and bit flips break it
proves: [correctness]
status: full
---

Let $N = 8n$ and let $\oplus$ be the bitwise exclusive or on $\{0, 1\}^N$. It is associative and commutative, $0^N$ is its identity, and $a \oplus a = 0^N$ for every $a$. So $(\{0,1\}^N, \oplus)$ is a group in which each element is its own inverse.

**Claim 1.** For every key $k$ and message $m$, $\mathrm{Dec}_k(\mathrm{Enc}_k(m)) = m$.

*Proof.* Lines L2 and L3 compute $c = m \oplus k$ byte by byte, which is the bitwise XOR of the whole strings. Then $c \oplus k = m \oplus k \oplus k = m \oplus 0^N = m$. $\square$

**Claim 2.** For every message $m$ and ciphertext $c$, exactly one key maps $m$ to $c$, namely $k = m \oplus c$.

*Proof.* If $m \oplus k = c$, then $k = m \oplus m \oplus k = m \oplus c$. Conversely $m \oplus (m \oplus c) = c$. $\square$

**Claim 3.** Let $M$ have any distribution on $\{0,1\}^N$, and let the key $K$ be uniform on $\{0,1\}^N$ and independent of $M$. Then for every $m$ with $\Pr[M = m] > 0$ and every $c$, $\Pr[C = c \mid M = m] = 2^{-N}$, and for every $c$, $\Pr[M = m \mid C = c] = \Pr[M = m]$.

*Proof.* Given $M = m$, the event $C = c$ is the event $K = m \oplus c$ by Claim 2. Since $K$ is independent of $M$ and uniform, $\Pr[C = c \mid M = m] = \Pr[K = m \oplus c] = 2^{-N}$. Summing over $m$, $\Pr[C = c] = \sum_m \Pr[M = m] \cdot 2^{-N} = 2^{-N} > 0$. By Bayes' rule,
$$\Pr[M = m \mid C = c] = \frac{\Pr[C = c \mid M = m] \Pr[M = m]}{\Pr[C = c]} = \frac{2^{-N} \Pr[M = m]}{2^{-N}} = \Pr[M = m].$$
For $m$ with $\Pr[M = m] = 0$ both sides are 0. $\square$

**Claim 4.** If $c_1 = m_1 \oplus k$ and $c_2 = m_2 \oplus k$ with the same key, then $c_1 \oplus c_2 = m_1 \oplus m_2$. If a word $w$ occurs in $m_1$ at offset $i$, then line L6 at offset $i$ gives $m_2[i .. i + \lvert w \rvert)$.

*Proof.* $c_1 \oplus c_2 = m_1 \oplus k \oplus m_2 \oplus k = m_1 \oplus m_2$. At offset $i$, line L6 computes $(m_1 \oplus m_2)[i..i+\lvert w \rvert) \oplus w$, and since $w = m_1[i..i+\lvert w \rvert)$, this is $m_2[i..i+\lvert w \rvert)$. Line L5 visits every offset, so the true offset is tested, and it is reported if that piece of $m_2$ consists of letters and spaces. By symmetry the same holds with $m_1$ and $m_2$ swapped. $\square$

**Claim 5.** For every key $k$, message $m$ and difference $\delta$, $\mathrm{Enc}_k(m) \oplus \delta = \mathrm{Enc}_k(m \oplus \delta)$. So an attacker who knows the bytes $u$ of the message at some offset can make the receiver decrypt $u'$ there, by XOR of the ciphertext with $u \oplus u'$ at that offset.

*Proof.* $(m \oplus k) \oplus \delta = (m \oplus \delta) \oplus k$. With $\delta$ equal to $u \oplus u'$ at the offset and 0 elsewhere, $m \oplus \delta$ holds $u \oplus u \oplus u' = u'$ at the offset and the bytes of $m$ elsewhere. $\square$

Claims 1 to 3 prove that the one-time pad is correct and perfectly secret, and Claims 4 and 5 prove that the two attacks shown on the page work whenever the conditions of the pad are broken or integrity is needed. $\blacksquare$
