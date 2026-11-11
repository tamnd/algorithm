---
title: MD5 is a Merkle-Damgard hash over a Davies-Meyer compression function
proves: [correctness]
status: full
---

We prove the structure that the page uses: the padding is injective and gives whole blocks, the loop computes the Merkle-Damgard iteration, and each step of COMPRESS is a bijection of the state, so that COMPRESS has the Davies-Meyer form. That the code is the RFC 1321 function is checked by the seven vectors of Appendix A.5 and by `hashlib.md5`, not proved. Nothing here claims that MD5 is collision resistant; it is not.

**Lemma 1 (padding).** For a message of $8n$ bits with $8n < 2^{64}$, line L1 gives $P = M \| 1 \| 0^k \| [8n]_{64}$ with $k = (447 - 8n) \bmod 512$. Then $512$ divides $|P|$, and $P$ determines $M$.

*Proof.* $|P| = 8n + 1 + k + 64 \equiv 448 + 64 \equiv 0 \pmod{512}$. The last 64 bits of $P$ give $8n$, and then the first $8n$ bits give $M$. $\square$

**Lemma 2 (the iteration).** Let $Y_1, \ldots, Y_\ell$ be the blocks of $P$, $H_0 = IV$ and $H_i = \text{COMPRESS}(H_{i-1}, Y_i)$. After the loop of lines L3 and L4, the registers hold $H_\ell$, and line L12 returns its 16 bytes.

*Proof.* Line L2 sets the registers to $H_0$. If they hold $H_{i-1}$ before the $i$-th run of line L4, they hold $H_i$ after it. Induction on $i$ gives the claim. $\square$

**Lemma 3 (each step is invertible).** For fixed $i$ (so fixed $\Phi_r$, $T[i]$, $s = s_r[i \bmod 4]$) and a fixed word $x = X[k_i]$, the map $(a, b, c, d) \mapsto (d, a', b, c)$ with $a' = b + ((a + \Phi_r(b, c, d) + x + T[i]) \lll s)$ is a bijection of $(\{0,1\}^{32})^4$.

*Proof.* The output gives $a'$ and the old $b$, $c$, $d$. Then $t = (a' - b) \ggg s$, because subtraction modulo $2^{32}$ undoes the addition of $b$ and right rotation undoes left rotation. Then $a = t - \Phi_r(b, c, d) - x - T[i]$. So the map has an inverse. $\square$

**Corollary.** For a fixed block $Y$, lines L6 to L10 compute a permutation $E_Y$ of the 128-bit state, the composition of 64 bijections of Lemma 3. Line L11 returns $E_Y(H) + H$ word by word. So COMPRESS is a [Davies-Meyer](/davies-meyer-construction/) compression function with addition modulo $2^{32}$ in place of XOR. It has a fixed point $H = E_Y^{-1}(0)$ for each block $Y$.

With Lemmas 1 and 2, MD5 is the Merkle-Damgard construction with MD strengthening, so the [Merkle-Damgard theorem](/merkle-damgard-theorem/) applies: each collision of MD5 contains a collision of COMPRESS. The Wang and Yu collision in the tests shows this directly. After the first block the two chaining values differ; after the second block they are equal. So the second block pair is a collision of COMPRESS from two different chaining values (a pseudo-collision), and the first block pair is a near-collision that sets up the difference.
