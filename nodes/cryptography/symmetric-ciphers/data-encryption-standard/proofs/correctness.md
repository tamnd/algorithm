---
title: DES decryption inverts DES encryption, and DES has the complementation property
proves: [correctness]
status: full
---

We write blocks as bit strings, $\bar z$ for the bitwise complement of $z$, and $\|$ for concatenation. For a 64-bit string $z = L \| R$ with halves of 32 bits, let $\sigma(L \| R) = R \| L$. For a 48-bit round key $k$, let $\Phi_k(L \| R) = R \| (L \oplus f(R, k))$, where $f$ is the cipher function of lines L7 to L10. Then lines L2 to L6 compute

$$E_K(x) = \mathrm{FP}\bigl(\sigma(\Phi_{k_{16}}(\cdots \Phi_{k_1}(\mathrm{IP}(x)) \cdots))\bigr),$$

because line L4 and line L5 compute $(L_i, R_i) = \Phi_{k_i}(L_{i-1}, R_{i-1})$, and line L6 outputs FP of $R_{16} \| L_{16} = \sigma(L_{16} \| R_{16})$. DES-DECRYPT computes the same expression with $k_{17-i}$ in place of $k_i$.

**Lemma 1.** For every function $f$ and key $k$, $\Phi_k$ is a bijection of $\{0,1\}^{64}$ and $\Phi_k^{-1} = \sigma \circ \Phi_k \circ \sigma$.

*Proof.* Let $L' \| R' = \Phi_k(L \| R)$, so $L' = R$ and $R' = L \oplus f(R, k)$. Then $\sigma(L' \| R') = R' \| L'$, and $\Phi_k(R' \| L') = L' \| (R' \oplus f(L', k))$. Since $L' = R$, $R' \oplus f(L', k) = L \oplus f(R, k) \oplus f(R, k) = L$. So $\Phi_k(\sigma(L' \| R')) = R \| L$, and $\sigma$ of this is $L \| R$. Thus $\sigma \Phi_k \sigma$ is a left inverse of $\Phi_k$. The same computation with the roles exchanged shows that $\Phi_k \sigma \Phi_k \sigma$ is the identity, so it is also a right inverse, and $\Phi_k$ is a bijection. No property of $f$ is used. $\square$

**Lemma 2.** FP is the inverse of IP.

*Proof.* FIPS 46-3 defines FP as the inverse permutation $\mathrm{IP}^{-1}$: if IP moves bit $j$ to position $i$, then FP moves bit $i$ to position $j$. The code builds FP from IP by exactly this rule. $\square$

**Theorem 1 (correctness).** For every key $K$ and block $x$, DES-DECRYPT$(K$, DES-ENCRYPT$(K, x)) = x$.

*Proof.* Let $G = \sigma \circ \Phi_{k_{16}} \circ \cdots \circ \Phi_{k_1}$, so $E_K = \mathrm{FP} \circ G \circ \mathrm{IP}$. By Lemma 1 and $\sigma^{-1} = \sigma$,

$$G^{-1} = \Phi_{k_1}^{-1} \circ \cdots \circ \Phi_{k_{16}}^{-1} \circ \sigma = (\sigma \Phi_{k_1} \sigma) \cdots (\sigma \Phi_{k_{16}} \sigma) \sigma = \sigma \circ \Phi_{k_1} \circ \cdots \circ \Phi_{k_{16}},$$

since each adjacent pair $\sigma \sigma$ is the identity. The right side applies $\Phi_{k_{16}}$ first and $\Phi_{k_1}$ last, then $\sigma$: this is $G$ with the keys in the order $k_{16}, \ldots, k_1$. DES-DECRYPT computes $\mathrm{FP} \circ G^{-1} \circ \mathrm{IP}$. By Lemma 2,

$$\mathrm{FP} \circ G^{-1} \circ \mathrm{IP} \circ \mathrm{FP} \circ G \circ \mathrm{IP} = \mathrm{FP} \circ G^{-1} \circ G \circ \mathrm{IP} = \mathrm{FP} \circ \mathrm{IP},$$

which is the identity. $\square$

**Lemma 3.** For every key $K$, KEY-SCHEDULE$(\bar K)$ gives the round keys $\bar k_1, \ldots, \bar k_{16}$.

*Proof.* PC-1, the rotations of line L13 and PC-2 each output a fixed selection of input bits, possibly with repeats or omissions. A map that only selects bits commutes with the complement: each output bit of the complemented input is the complement of the same output bit. A composition of such maps has the same property. $\square$

**Theorem 2 (complementation).** For every key $K$ and block $x$, $E_{\bar K}(\bar x) = \overline{E_K(x)}$.

*Proof.* The maps IP, FP, E and $\sigma$ only select bits, so each commutes with the complement, as in Lemma 3. For the cipher function, $E(\bar R) \oplus \bar k = \overline{E(R)} \oplus \bar k = E(R) \oplus k$, so the S-box inputs, and hence $f(\bar R, \bar k) = f(R, k)$, do not change. Now $\Phi_{\bar k}(\bar L \| \bar R) = \bar R \| (\bar L \oplus f(\bar R, \bar k)) = \bar R \| \overline{L \oplus f(R, k)} = \overline{\Phi_k(L \| R)}$. By Lemma 3 the key $\bar K$ gives the round keys $\bar k_i$. By induction on $i$, the state after round $i$ under $(\bar K, \bar x)$ is the complement of the state under $(K, x)$: the base case holds because IP commutes with the complement, and each round keeps the claim by the identity above. The final $\sigma$ and FP keep it too. $\blacksquare$
