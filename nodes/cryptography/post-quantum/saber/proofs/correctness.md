---
title: Saber decryption returns the message when the rounding noise is small
proves: [correctness]
status: full
---

Let $q = 2^{\epsilon_q}$, $p = 2^{\epsilon_p}$ and $T = 2^{\epsilon_T}$ with $\epsilon_T < \epsilon_p < \epsilon_q$, and write $a = \epsilon_q - \epsilon_p$ and $c = \epsilon_p - \epsilon_T$. Then $h_1 = 2^{a-1}$ and $h_2 = 2^{\epsilon_p - 2} - 2^{c - 1} + h_1$. Polynomials are in $\mathbb{Z}[x]/(x^n + 1)$, congruences are coefficient by coefficient, and for a polynomial $y$ with coefficients in $[0, 2^k)$, $y \gg j$ is $\lfloor y / 2^j \rfloor$ coefficient by coefficient. For Saber, $a = 3$, $c = 6$ and $\epsilon_p = 10$.

**Lemma 1 (the rounding errors).** Let $b, b', c_m$ come from lines L3, L6 and L8. There are polynomials $e_1, e_2 \in [0, 2^a)^{l \times n}$ and $e_3 \in [0, 2^c)^n$ with
$$2^a b \equiv A^\mathsf{T} s + h_1 - e_1, \qquad 2^a b' \equiv A s' + h_1 - e_2 \pmod q,$$
$$2^c c_m \equiv v' + h_1 - 2^{\epsilon_p - 1} m - e_3 \pmod p.$$

*Proof.* For line L3, let $y = (A^\mathsf{T} s + h_1) \bmod q$, so $b = \lfloor y / 2^a \rfloor$, and set $e_1 = y - 2^a b \in [0, 2^a)$. Then $2^a b = y - e_1 \equiv A^\mathsf{T} s + h_1 - e_1 \pmod q$. Lines L6 and L8 are the same with $(q, a)$ and $(p, c)$. $\square$

**Lemma 2 (the difference).** Let $v' = b^\mathsf{T} s' \bmod p$ (line L7) and $v = b'^\mathsf{T} s \bmod p$ (line L10). Then $X = (h_1 - e_2)^\mathsf{T} s - (h_1 - e_1)^\mathsf{T} s'$, computed over the integers, has all coefficients divisible by $2^a$, and $v - v' \equiv \delta \pmod p$ with $\delta = X / 2^a$.

*Proof.* Since $q = 2^a p$, a congruence modulo $p$ multiplied by $2^a$ becomes a congruence modulo $q$, so $2^a v \equiv 2^a b'^\mathsf{T} s$ and $2^a v' \equiv 2^a b^\mathsf{T} s' \pmod q$. By Lemma 1,
$$2^a (v - v') \equiv (A s' + h_1 - e_2)^\mathsf{T} s - (A^\mathsf{T} s + h_1 - e_1)^\mathsf{T} s' \pmod q.$$
The ring is commutative, so $(A s')^\mathsf{T} s = \sum_{i,j} A_{ij} s'_j s_i = (A^\mathsf{T} s)^\mathsf{T} s'$, and these terms cancel. So $2^a(v - v') \equiv X \pmod q$. The left side and $q$ are multiples of $2^a$, so $X$ is too, and dividing the congruence by $2^a$ gives $v - v' \equiv \delta \pmod p$. $\square$

**Lemma 3 (PKE decryption).** If every coefficient of $\delta$ satisfies $|\delta_i| \le 2^{\epsilon_p - 2} - 2^{c - 1}$, then line L11 returns $m$.

*Proof.* Let $w = (v - 2^c c_m + h_2) \bmod p$. By Lemma 1 and Lemma 2,
$$w \equiv v - v' - h_1 + 2^{\epsilon_p - 1} m + e_3 + h_2 \equiv 2^{\epsilon_p - 1} m + 2^{\epsilon_p - 2} + t \pmod p,$$
with $t = \delta + e_3 - 2^{c-1}$. Since $e_3 \in [0, 2^c)$, the bound on $\delta$ gives $-2^{\epsilon_p - 2} \le t_i < 2^{\epsilon_p - 2}$. So the integer $2^{\epsilon_p - 1} m_i + 2^{\epsilon_p - 2} + t_i$ lies in $[2^{\epsilon_p - 1} m_i, 2^{\epsilon_p - 1} m_i + 2^{\epsilon_p - 1})$, which is inside $[0, p)$; hence it equals $w_i$, and $w_i \gg (\epsilon_p - 1) = m_i$. $\square$

For Saber the bound of Lemma 3 is $256 - 32 = 224$.

**Theorem (the KEM).** Let $(pk, sk)$ come from line L13 and $(c, K)$ from lines L14 to L17. If the condition of Lemma 3 holds for this encryption, then lines L18 to L21 return $K$.

*Proof.* The secret key holds $s$, $pk$, $H(pk)$ and $z$. The packing of $b$, $b'$ and $c_m$ into bytes is inverse to the unpacking on values below $p$ and $T$, and $s$ is stored with $\epsilon_q$ bits and read back as a signed value, so line L18 runs PKE.Dec on the values of Lemma 3 and returns $m' = m$. Line L19 hashes the same $m \| H(pk)$ as line L15, so $(\hat K', r') = (\hat K, r)$. PKE.Enc is deterministic in $(pk, m, r)$, so line L20 gives $c' = c$, and line L21 returns $H(\hat K \| H(c)) = K$. $\blacksquare$

**When the condition holds.** $h_1 - e_i$ has coefficients in $[-3, 4]$ and the secrets have coefficients in $[-4, 4]$ for Saber, so each coefficient of $X$ is a sum of $2 l n = 1536$ products of small values, and $\delta = X / 8$. In the worst case this exceeds 224, so correctness is a probability statement. The Saber papers compute the distribution of one coefficient of $\delta$ (together with $e_3$) by convolution and take a union bound over the 256 coefficients, which gives the failure rates quoted on the page.
