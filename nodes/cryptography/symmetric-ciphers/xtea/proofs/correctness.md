---
title: XTEA decryption inverts encryption
proves: [correctness]
status: full
---

All words are 32-bit, $+$ and $-$ are modulo $2^{32}$, and $\ll$, $\gg$ are logical shifts. Let $G(x) = ((x \ll 4) \oplus (x \gg 5)) + x$, let $\sigma_i = i\delta \bmod 2^{32}$, and let $\kappa(s) = k[s \bmod 4]$ and $\kappa'(s) = k[\lfloor s / 2^{11} \rfloor \bmod 4]$.

**Lemma 1 (one encryption cycle).** At the start of encryption cycle $i$ (line L2), $\mathit{sum} = \sigma_{i-1}$. Cycle $i$ is the map $\Phi_i(v_0, v_1) = (v_0', v_1')$ with
$$v_0' = v_0 + \bigl(G(v_1) \oplus (\sigma_{i-1} + \kappa(\sigma_{i-1}))\bigr), \qquad v_1' = v_1 + \bigl(G(v_0') \oplus (\sigma_i + \kappa'(\sigma_i))\bigr),$$
and at its end $\mathit{sum} = \sigma_i$.

*Proof.* Line L1 sets $\mathit{sum} = 0 = \sigma_0$. If $\mathit{sum} = \sigma_{i-1}$ at the start of cycle $i$, line L3 computes $v_0'$ as stated, line L4 sets $\mathit{sum} = \sigma_{i-1} + \delta = \sigma_i$, and line L5 computes $v_1'$ with that value. Induction on $i$ completes the proof. $\square$

**Lemma 2 (one decryption cycle).** At the start of decryption cycle $j$ (line L8), $\mathit{sum} = \sigma_{r-j+1}$. With $i = r - j + 1$, cycle $j$ is the map $\Psi_i(v_0', v_1') = (v_0, v_1)$ with
$$v_1 = v_1' - \bigl(G(v_0') \oplus (\sigma_i + \kappa'(\sigma_i))\bigr), \qquad v_0 = v_0' - \bigl(G(v_1) \oplus (\sigma_{i-1} + \kappa(\sigma_{i-1}))\bigr),$$
and at its end $\mathit{sum} = \sigma_{i-1}$.

*Proof.* Line L7 sets $\mathit{sum} = r\delta = \sigma_r$, the case $j = 1$. If $\mathit{sum} = \sigma_i$ at the start, line L9 computes $v_1$ as stated, line L10 sets $\mathit{sum} = \sigma_{i-1}$, and line L11 computes $v_0$ with that value. So the next cycle starts with $\sigma_{i-1} = \sigma_{r-(j+1)+1}$. $\square$

**Lemma 3.** $\Psi_i(\Phi_i(v)) = v$ for each block $v$.

*Proof.* Let $(v_0', v_1') = \Phi_i(v_0, v_1)$. The first step of $\Psi_i$ subtracts from $v_1'$ the same value $G(v_0') \oplus (\sigma_i + \kappa'(\sigma_i))$ that $\Phi_i$ added, and gets $v_1$, because addition modulo $2^{32}$ is a group operation. The second step now has $v_1$, so it subtracts from $v_0'$ the same value $G(v_1) \oplus (\sigma_{i-1} + \kappa(\sigma_{i-1}))$ that $\Phi_i$ added, and gets $v_0$. $\square$

**Theorem.** For each $r \ge 0$, key $k$ and block $v$, XTEA-DECRYPT(XTEA-ENCRYPT$(v, k, r), k, r) = v$. So XTEA-ENCRYPT$(\cdot, k, r)$ is a permutation of $\{0,1\}^{64}$.

*Proof.* By Lemma 1, encryption is $\Phi_r \circ \cdots \circ \Phi_1$. By Lemma 2, decryption cycle $j$ is $\Psi_{r-j+1}$, so decryption is $\Psi_1 \circ \cdots \circ \Psi_r$. Applying Lemma 3 from the inside out, $\Psi_1 \circ \cdots \circ \Psi_r \circ \Phi_r \circ \cdots \circ \Phi_1$ is the identity. A map of a finite set to itself with a left inverse is a bijection. $\blacksquare$
