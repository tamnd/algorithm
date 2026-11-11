---
title: PRESENT decryption inverts encryption, and the bit permutation has order three
proves: [correctness]
status: full
---

Let the state be $x \in \{0,1\}^{64}$, with bits $x_{63} \ldots x_0$. Write $A_K(x) = x \oplus K$, $\mathcal{S}(x)$ for the S-box layer (the 4-bit S-box $S$ on each nibble $x_{4j+3} \ldots x_{4j}$), and $\mathcal{P}(x)$ for the bit permutation: bit $i$ of $x$ becomes bit $P(i)$ of $\mathcal{P}(x)$, where $P(i) = 16 i \bmod 63$ for $i \le 62$ and $P(63) = 63$.

**Lemma 1 ($P$ is a permutation of the bit positions).** $P$ is a bijection of $\{0, \ldots, 63\}$, and $P^3$ is the identity.

*Proof.* $P(63) = 63$, and for $i \le 62$, $P(i) \in \{0, \ldots, 62\}$. Since $\gcd(16, 63) = 1$, multiplication by 16 is a bijection of $\mathbb{Z}/63$, so $P$ is a bijection of $\{0, \ldots, 62\}$, and so of $\{0, \ldots, 63\}$. For $i \le 62$, $P^3(i) = 16^3 i \bmod 63$, and $16^3 = 4096 = 65 \cdot 63 + 1 \equiv 1 \pmod{63}$, so $P^3(i) = i$. $\square$

So $\mathcal{P}$ is a bijection of $\{0,1\}^{64}$; its inverse moves bit $P(i)$ back to bit $i$ (line L10), and $\mathcal{P}^3 = \mathrm{id}$, so $\mathcal{P}^{-1} = \mathcal{P}^2$.

**Lemma 2 (the S-box layer is a bijection).** The table of $S$ lists the 16 values C, 5, 6, B, 9, 0, A, D, 3, E, F, 8, 4, 7, 1, 2, which are all different. So $S$ is a bijection of $\{0,1\}^4$ with an inverse $S^{-1}$. The layer $\mathcal{S}$ acts on 16 disjoint nibbles, so it is a bijection with inverse $\mathcal{S}^{-1}$, which applies $S^{-1}$ to each nibble (line L11). $\square$

**Lemma 3.** $A_K$ is its own inverse, since $(x \oplus K) \oplus K = x$. $\square$

**Theorem.** For each block $x$ and key $k$, PRESENT-DECRYPT(PRESENT-ENCRYPT$(x, k), k) = x$.

*Proof.* Both procedures compute the same round keys $K_1, \ldots, K_{32}$ from $k$ (lines L1 and L7), since the key schedule is a fixed function of $k$. Encryption computes
$$E = A_{K_{32}} \circ R_{31} \circ \cdots \circ R_1, \qquad R_i = \mathcal{P} \circ \mathcal{S} \circ A_{K_i}.$$
Decryption computes $D = Q_1 \circ \cdots \circ Q_{31} \circ A_{K_{32}}$ with $Q_i = A_{K_i} \circ \mathcal{S}^{-1} \circ \mathcal{P}^{-1}$ (lines L10 to L12, for $i$ from 31 down to 1). By Lemmas 1 to 3, $Q_i \circ R_i = A_{K_i} \circ \mathcal{S}^{-1} \circ \mathcal{P}^{-1} \circ \mathcal{P} \circ \mathcal{S} \circ A_{K_i} = \mathrm{id}$. Then
$$D \circ E = Q_1 \circ \cdots \circ Q_{31} \circ A_{K_{32}} \circ A_{K_{32}} \circ R_{31} \circ \cdots \circ R_1 = Q_1 \circ \cdots \circ Q_{31} \circ R_{31} \circ \cdots \circ R_1,$$
and removing the pairs $Q_{31} \circ R_{31}$, then $Q_{30} \circ R_{30}$, and so on, from the middle gives the identity. So $E$ has a left inverse on the finite set $\{0,1\}^{64}$, and it is a permutation. $\blacksquare$
