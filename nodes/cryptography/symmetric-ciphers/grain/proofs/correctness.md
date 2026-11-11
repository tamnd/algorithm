---
title: Grain-128AEADv2 decryption returns the plaintext for a valid ciphertext and tag
proves: [correctness]
status: full
---

Write $\Sigma = (S, B, A_{\mathrm{acc}}, R)$ for the full state: the 128-bit LFSR, the 128-bit NFSR, the 64-bit accumulator and the 64-bit register. Let $\mathrm{CLK}(S, B) = (y, S', B')$ be one normal clock of the page. It is a fixed Boolean map. Encryption follows lines L1 to L13. Decryption runs lines L1 to L8 in the same way. For $i < M$ it takes $m_i$ from the known string $\mathrm{ENCODE}(|A|) \| A$, and for $i \ge M$ it sets $m_i = c_{i-M} + z$. Then it runs lines L10 to L12, and it accepts if the computed tag equals $T$.

**Lemma 1 (the same state after initialization).** For the same $(K, N)$, encryption and decryption hold the same $\Sigma$ after line L5.

*Proof.* Lines L1 to L5 read only $K$, $N$ and constants, and each step is a fixed map ($\mathrm{CLK}$ with a fixed input XOR, or a copy of $y$ into $A_{\mathrm{acc}}$ or $R$). $\square$

**Lemma 2 (one step).** Let $\Sigma_i$ be the state before step $i$ of the loop at line L7 in both procedures, and suppose they are equal. Then decryption uses the same bit $m_i$ as encryption, and both reach the same state $\Sigma_{i+1}$.

*Proof.* Line L8 applies $\mathrm{CLK}$ twice to $(S, B)$. It does not read the data, so both procedures get the same $z$, $z'$ and the same new $(S, B)$. If $i < M$, $m_i$ is a bit of $\mathrm{ENCODE}(|A|) \| A$, which both sides know. If $i \ge M$, encryption output $c_{i-M} = m_i + z$, and decryption computes $c_{i-M} + z = m_i + z + z = m_i$, because $z + z = 0$ in GF(2). Lines L10 and L11 are a fixed map of $(A_{\mathrm{acc}}, R, m_i, z')$, so with the same inputs they give the same $(A_{\mathrm{acc}}, R)$. $\square$

**Theorem.** If $(C, T) = $ GRAIN-128AEADv2-ENCRYPT$(K, N, A, P)$, then decryption of $(K, N, A, C, T)$ returns $P$.

*Proof.* Both procedures build the same $M$ and the same length $|m| = M + |P|$ in bits, because $|C| = |P|$. By Lemma 1 the states agree before the loop. By Lemma 2 and induction on $i$, they agree after each step, and decryption recovers each $m_i$ for $i \ge M$, which are the bits of $P$ in order. Line L12 is the same fixed map on the same state, so the computed tag equals $T$, the check succeeds, and decryption returns $P$. $\blacksquare$

**Remark (why each message bit matters to the tag).** Unrolling lines L10 to L12 gives $T = A_{\mathrm{acc},0} + \sum_{i=0}^{|m|-1} m_i R_i + R_{|m|}$, where $R_i$ is the register before step $i$. The register values depend on the keystream only, not on the data. So $T$ is an affine function of the bits $m_i$, and flipping one bit $m_i$ adds the 64-bit value $R_i$ to the tag. This is a functional fact; the claim that an adversary cannot predict $R_i$ is the security claim of the designers, not part of this proof.
