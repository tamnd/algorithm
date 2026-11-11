---
title: SHA-1 is a Merkle-Damgard hash over a Davies-Meyer compression function
proves: [correctness]
status: full
---

We prove the structure of SHA-1 that the page uses. Whether the code is the FIPS 180-4 function is checked by the NIST examples (the registers after steps 0 and 1, and two digests) and by `hashlib.sha1`. Collision resistance is not claimed: SHA-1 has known collisions.

**Lemma 1 (padding).** For $8n < 2^{64}$, line L1 gives $P = M \| 1 \| 0^k \| [8n]_{64}$ with $k = (447 - 8n) \bmod 512$, where $[8n]_{64}$ is big-endian. Then $512$ divides $|P|$ and $P$ determines $M$.

*Proof.* $8n + 1 + k \equiv 448 \pmod{512}$, so $|P| \equiv 0$. The last 64 bits give $8n$, and the first $8n$ bits give $M$. $\square$

**Lemma 2 (the iteration).** With the blocks $Y_1, \ldots, Y_\ell$ of $P$, $H^{(0)} = IV$ and $H^{(i)} = \text{COMPRESS}(H^{(i-1)}, Y_i)$, the loop of lines L3 and L4 ends with $H = H^{(\ell)}$, and line L11 returns its 20 bytes.

*Proof.* Induction on $i$, as for MD4: line L2 starts at $H^{(0)}$, and one run of line L4 turns $H^{(i-1)}$ into $H^{(i)}$. $\square$

**Lemma 3 (the schedule is a bijection).** Line L5 maps the 16 block words to $W[0 \ldots 79]$ injectively, and $W[0 \ldots 15]$ are the block words themselves.

*Proof.* The first 16 words are copied. So two different blocks give two different schedules. (More: any 16 consecutive words $W[j \ldots j+15]$ determine all the others, since the recurrence can be run forward and, solved for $W[t-16]$, backward. This is what the attacks use to place differences.) $\square$

**Lemma 4 (each step is invertible).** For fixed $t$ and $W[t]$, the map $(a, b, c, d, e) \mapsto (T, a, \mathrm{ROTL}^{30}(b), c, d)$ with $T = \mathrm{ROTL}^5(a) + f_t(b, c, d) + e + K_t + W[t]$ is a bijection of $(\{0,1\}^{32})^5$.

*Proof.* From the output $(a', b', c', d', e')$ we read $a = b'$, $b = \mathrm{ROTL}^{2}(c')$ (rotation by 30 and then by 2 is the identity on 32 bits), $c = d'$ and $d = e'$. Then $e = a' - \mathrm{ROTL}^5(a) - f_t(b, c, d) - K_t - W[t]$ modulo $2^{32}$. So the map has an inverse. $\square$

**Corollary.** For a fixed block $Y$, lines L6 to L9 compute a permutation $E_Y$ of the 160-bit state (this permutation family is the block cipher SHACAL-1), and line L10 returns $E_Y(H) + H$ word by word: the [Davies-Meyer](/davies-meyer-construction/) form with addition modulo $2^{32}$.

So SHA-1 is the Merkle-Damgard construction with MD strengthening over COMPRESS, and the [Merkle-Damgard theorem](/merkle-damgard-theorem/) says that each SHA-1 collision contains a COMPRESS collision. In SHAttered, the chaining values after the common 192-byte prefix are equal, they differ after the first different block (a near-collision), and they are equal again after the second, which is the compression collision the theorem predicts.
