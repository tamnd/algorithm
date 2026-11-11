---
title: SNOW 3G decrypts correctly, and its keystream-mode update is a bijection
proves: [correctness]
status: full
---

Write $\sigma = (s_0, \ldots, s_{15}, R_1, R_2, R_3)$ for the state, a vector of 19 words of 32 bits. Let $\Phi$ be one clock of lines L8 and L10 of the page (the keystream mode), and $\Phi_F$ one clock of lines L3 and L4 (the initialization mode).

**Lemma 1 (determinism).** The keystream $z_1, \ldots, z_n$ is a function of $(K, IV, n)$ only.

*Proof.* Line L1 sets $\sigma$ from $K$, $IV$ and constants. Every later line applies a fixed map to $\sigma$: XOR, addition modulo $2^{32}$, the fixed bijections $S_1$ and $S_2$, the fixed linear maps $c \mapsto \alpha c$ and $c \mapsto \alpha^{-1} c$, and shifts of the word list. By induction on the number of clocks, each state and each output $z_t = F \oplus s_0$ is a function of $(K, IV)$. $\square$

**Theorem 1 (correctness).** For each key $K$, IV and message $m$ of $n$ words, the receiver recovers $m$ from $c = m \oplus z$.

*Proof.* By Lemma 1 the receiver computes the same $z$, and $(m_t \oplus z_t) \oplus z_t = m_t$ for each word, since $z_t \oplus z_t = 0$. $\blacksquare$

**Lemma 2.** $S_1$ and $S_2$ are bijections of the 32-bit words.

*Proof.* Each is a byte-wise S-box followed by a MixColumn. The AES S-box $S_R$ and $S_Q$ are permutations of the 256 bytes (Section 5 of the specification lists them; the test file checks that each table is a permutation). The MixColumn of $S_1$ is the AES matrix with rows $(x, x+1, 1, 1)$ and its cyclic shifts over $\mathrm{GF}(2^8)$, which is invertible (it is the AES MixColumns, and AES decryption uses its inverse). The MixColumn of $S_2$ has the same circulant shape over $\mathrm{GF}(2^8)$ defined by $x^8 + x^6 + x^5 + x^3 + 1$. A circulant $\mathrm{circ}(a_0, a_1, a_2, a_3)$ over a field of characteristic 2 has determinant $\prod_{\omega^4 = 1} (a_0 + a_1 \omega + a_2 \omega^2 + a_3 \omega^3)$, and the only fourth root of unity is $\omega = 1$, so the determinant is $(a_0 + a_1 + a_2 + a_3)^4 = (x + (x+1) + 1 + 1)^4 = 1^4 = 1 \ne 0$. So both matrices are invertible, and the composition of two bijections is a bijection. $\square$

**Theorem 2 ($\Phi$ is a bijection).** The keystream-mode clock $\Phi$ is a permutation of the $2^{608}$ states.

*Proof.* Let $\sigma' = \Phi(\sigma)$. We recover $\sigma$ from $\sigma'$. Line L15 gives $s_i = s'_{i-1}$ for $1 \le i \le 15$. Line L13 gives $R_1 = S_1^{-1}(R'_2)$ and $R_2 = S_2^{-1}(R'_3)$, by Lemma 2. Line L12 gives $R'_1 = R_2 \boxplus (R_3 \oplus s_5)$, so $R_3 = (R'_1 \boxminus R_2) \oplus s_5$, where $s_5 = s'_4$ is known. Last, line L14 with $F = 0$ gives $s'_{15} = \alpha s_0 \oplus s_2 \oplus \alpha^{-1} s_{11}$, so $s_0 = \alpha^{-1} (s'_{15} \oplus s_2 \oplus \alpha^{-1} s_{11})$, with $s_2 = s'_1$ and $s_{11} = s'_{10}$ known and $\alpha \ne 0$ in $\mathrm{GF}(2^{32})$. So $\Phi$ is injective on a finite set, hence a bijection. $\blacksquare$

**Remark.** The initialization clock $\Phi_F$ is also a bijection: the same steps recover $R_1, R_2, R_3$ and $s_1, \ldots, s_{15}$, then $F = (s_{15} \boxplus R_1) \oplus R_2$ is known, and $s_0 = \alpha^{-1}(s'_{15} \oplus s_2 \oplus \alpha^{-1} s_{11} \oplus F)$. So for a fixed key, different IVs give different states after line L6, and the keystream-mode state sequence is purely periodic. These are functional facts only. They do not bound the period from below, and the security of SNOW 3G rests on public analysis, not on a proof.
