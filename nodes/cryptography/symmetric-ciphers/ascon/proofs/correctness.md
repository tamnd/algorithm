---
title: Ascon-AEAD128 decryption returns the plaintext for a valid ciphertext and tag
proves: [correctness]
status: full
---

Write $S^{\mathrm{r}} = S[0..127]$ for the rate (words $S_0, S_1$) and $S^{\mathrm{c}} = S[128..319]$ for the capacity. Encryption follows lines L5 to L14 of the page. Decryption runs the same lines L5 to L8, then, for each full ciphertext block $C_i$, sets $P_i = S^{\mathrm{r}} \oplus C_i$ and $S^{\mathrm{r}} \leftarrow C_i$ before ASCON-P$(S, 8)$; for the last block of $\ell < 16$ bytes it sets $P_{\mathrm{last}}$ to the first $\ell$ bytes of $S^{\mathrm{r}} \oplus C_{\mathrm{last}}$ and XORs $\mathrm{pad}(P_{\mathrm{last}})$ into $S^{\mathrm{r}}$; then it computes $T'$ by lines L12 and L13 and returns $P$ if $T' = T$.

**Lemma 1 (the same state after initialization and associated data).** For the same $(K, N, A)$, encryption and decryption hold the same state after line L8.

*Proof.* Lines L5 to L8 depend only on $K$, $N$ and $A$, and use only XOR and the deterministic map ASCON-P. $\square$

**Lemma 2 (the same state after each full block).** Let $\Sigma_i$ be the state before block $i$ in both procedures, and suppose they are equal. If $C_i$ is the ciphertext block that encryption produced from $P_i$, then decryption outputs $P_i$ and both procedures reach the same state $\Sigma_{i+1}$.

*Proof.* Encryption sets the rate to $\Sigma_i^{\mathrm{r}} \oplus P_i$ and outputs it as $C_i$, keeping the capacity $\Sigma_i^{\mathrm{c}}$. Decryption computes $\Sigma_i^{\mathrm{r}} \oplus C_i = \Sigma_i^{\mathrm{r}} \oplus \Sigma_i^{\mathrm{r}} \oplus P_i = P_i$, and sets the rate to $C_i$, keeping the same capacity. Both states are now $(C_i, \Sigma_i^{\mathrm{c}})$, and both apply ASCON-P$(\cdot, 8)$, so $\Sigma_{i+1}$ is the same. $\square$

**Lemma 3 (the last block).** If the states before the last block are equal to $\Sigma$, decryption outputs $P_{\mathrm{last}}$ and both reach the same state.

*Proof.* Encryption sets the rate to $\Sigma^{\mathrm{r}} \oplus \mathrm{pad}(P_{\mathrm{last}})$ and outputs its first $\ell$ bytes, which are the first $\ell$ bytes of $\Sigma^{\mathrm{r}} \oplus P_{\mathrm{last}}$, since $\mathrm{pad}(P_{\mathrm{last}})$ begins with $P_{\mathrm{last}}$. Decryption XORs these bytes with the first $\ell$ bytes of $\Sigma^{\mathrm{r}}$ and gets $P_{\mathrm{last}}$. It then XORs $\mathrm{pad}(P_{\mathrm{last}})$ into $\Sigma^{\mathrm{r}}$, the same operation as encryption. This also covers $\ell = 0$, where $\mathrm{pad}$ of the empty string is the byte 01 followed by zeros. $\square$

**Theorem.** If $(C, T) = $ ASCON-AEAD128-ENCRYPT$(K, N, A, P)$, then decryption of $(K, N, A, C, T)$ returns $P$.

*Proof.* By Lemma 1 the states agree after line L8. By Lemma 2 and induction on $i$, they agree after each full block, and decryption outputs each $P_i$. By Lemma 3 they agree after the last block, and decryption outputs $P_{\mathrm{last}}$. Lines L12 and L13 are deterministic functions of the state and $K$, so $T' = T$, the check succeeds, and decryption returns $P_0 \| \cdots \| P_{\mathrm{last}} = P$. $\blacksquare$

This proves functional correctness only. The security claims (128-bit confidentiality and integrity for nonce-respecting use with at most $2^{54}$ bytes per key) are those of SP 800-232 Section 4.4, which rest on the published analysis of the permutation and the keyed duplex mode.
