---
title: SHA-2 is a Merkle-Damgard hash over a Davies-Meyer compression function
proves: [correctness]
status: full
---

We prove the structure that the page uses for all six functions. That the code is the FIPS 180-4 function is checked by the NIST examples, by the registers after rounds 0 and 1 for "abc", by the constants printed in FIPS 180-4, and by `hashlib`. We write $R$ for the number of rounds (64 or 80) and $B = 16w$ for the block length in bits.

**Lemma 1 (padding).** Line L1 gives $P = M \| 1 \| 0^k \| [8n]_{2w}$ with $k = (B - 2w - 1 - 8n) \bmod B$. If $8n < 2^{2w}$, then $B$ divides $|P|$ and $P$ determines $M$.

*Proof.* $|P| = 8n + 1 + k + 2w \equiv 8n + 1 + (B - 2w - 1 - 8n) + 2w = B \equiv 0 \pmod B$. The last $2w$ bits hold $8n$, which is less than $2^{2w}$, so they give $n$, and the first $8n$ bits give $M$. $\square$

**Lemma 2 (the iteration).** Let $Y_1, \ldots, Y_\ell$ be the blocks of $P$, $H^{(0)} = IV$ and $H^{(i)} = \text{COMPRESS}(H^{(i-1)}, Y_i)$. The loop of lines L3 and L4 ends with $H = H^{(\ell)}$, and line L14 returns the first $d$ bits of its big-endian encoding.

*Proof.* Line L2 starts at $H^{(0)}$, and each run of line L4 maps $H^{(i-1)}$ to $H^{(i)}$. Induction on $i$. $\square$

**Lemma 3 (each round is invertible).** For fixed $t$ and $W[t]$, the map of lines L10 to L12 from $(a, b, c, d, e, f, g, h)$ to $(a', b', c', d', e', f', g', h') = (T_1 + T_2, a, b, c, d + T_1, e, f, g)$ is a bijection of $(\{0,1\}^w)^8$.

*Proof.* From the output, $a = b'$, $b = c'$, $c = d'$, $e = f'$, $f = g'$, $g = h'$. These give $T_2 = \Sigma_0(a) + \mathrm{Maj}(a, b, c)$. Then $T_1 = a' - T_2$, $d = e' - T_1$, and $h = T_1 - \Sigma_1(e) - \mathrm{Ch}(e, f, g) - K[t] - W[t]$, all modulo $2^w$. So the map has an inverse. $\square$

**Corollary.** For a fixed block $Y$, lines L8 to L12 compute a permutation $E_Y$ of $\{0,1\}^{8w}$, the composition of $R$ bijections. Line L13 returns $E_Y(H) + H$, the [Davies-Meyer](/davies-meyer-construction/) form with word-wise addition. (Lines L5 to L7 only compute the round keys $W[t]$ from $Y$.)

**Lemma 4 (truncation).** Let $F$ be a function to $\{0,1\}^{8w}$ and $\pi_d$ the map to the first $d$ bits. A collision of $\pi_d \circ F$ is either a collision of $F$ or a pair with $F(x) \ne F(x')$ that agrees on the first $d$ bits.

*Proof.* If $\pi_d(F(x)) = \pi_d(F(x'))$, then either $F(x) = F(x')$ or the two values differ only in the last $8w - d$ bits. $\square$

So a truncated member is collision resistant only up to $2^{d/2}$, which matches the table of FIPS 202. In return, the hidden $8w - d$ bits of the final chaining value are what stops [length extension](/length-extension-attack/): to continue the iteration from a digest, an attacker must guess them, which takes about $2^{8w - d}$ tries (only $2^{32}$ for SHA-224).

With Lemmas 1 and 2, every member is the Merkle-Damgard construction with MD strengthening over COMPRESS, followed by $\pi_d$, so the [Merkle-Damgard theorem](/merkle-damgard-theorem/) applies to the untruncated functions: a collision of SHA-256 or SHA-512 gives a collision of its compression function.
