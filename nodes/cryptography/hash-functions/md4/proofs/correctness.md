---
title: MD4 is a Merkle-Damgard hash over a Davies-Meyer compression function
proves: [correctness]
status: full
---

"Correct" here means three things. The padding gives a well-defined sequence of whole blocks, from which the message can be read back. The loop of lines L3 and L4 computes the Merkle-Damgard iteration of COMPRESS. And COMPRESS is a permutation of the state, keyed by the block, followed by a feed-forward. Whether MD4 is collision resistant is a different question, and the answer is no. Whether the code matches RFC 1320 bit for bit is checked by the test vectors of Appendix A.5, not by this proof.

**Lemma 1 (padding).** For a message $M$ of $8n$ bits, line L1 gives $P = M \| 1 \| 0^k \| [8n]_{64}$ with $k = (447 - 8n) \bmod 512$. Then $|P| \equiv 0 \pmod{512}$, and the map $M \mapsto P$ is injective for $n < 2^{61}$.

*Proof.* $|P| = 8n + 1 + k + 64$. By the choice of $k$, $8n + 1 + k \equiv 448 \pmod{512}$, so $|P| \equiv 448 + 64 \equiv 0$. For injectivity, the last 64 bits of $P$ give $8n$, since $8n < 2^{64}$. Then the first $8n$ bits of $P$ give $M$. So $P$ determines $M$. $\square$

The length field is also what the [Merkle-Damgard theorem](/merkle-damgard-theorem/) needs: if two padded messages have different lengths, their last blocks differ.

**Lemma 2 (the iteration).** Let $Y_1, \ldots, Y_\ell$ be the blocks of $P$, and let $H_0 = IV$ and $H_i = \text{COMPRESS}(H_{i-1}, Y_i)$. Before the $i$-th execution of line L4, the registers hold $H_{i-1}$. After the loop, they hold $H_\ell$.

*Proof.* By induction on $i$. Line L2 sets the registers to $IV = H_0$, so the claim holds for $i = 1$. If the registers hold $H_{i-1}$ before line L4 runs on $Y_i$, they hold $\text{COMPRESS}(H_{i-1}, Y_i) = H_i$ after it, which is the claim for $i + 1$. The loop visits the blocks once each, in order, so it ends with $H_\ell$. Line L11 writes $H_\ell$ as 16 bytes, which is a bijection. $\square$

**Lemma 3 (each step is invertible).** Fix a message word $x$, a constant $K$, a shift $s$ and a round function $\Phi$. The step $(a, b, c, d) \mapsto (d, a', b, c)$ with $a' = (a + \Phi(b, c, d) + x + K) \lll s$ is a bijection of $(\{0,1\}^{32})^4$.

*Proof.* The values $b$, $c$ and $d$ are copied to the output. From the output we read $b$, $c$, $d$ and $a'$. Rotation by $s$ is a bijection of 32-bit words, so $a + \Phi(b, c, d) + x + K = a' \ggg s$. Subtraction modulo $2^{32}$ then gives $a = (a' \ggg s) - \Phi(b, c, d) - x - K$. So the map has an inverse. $\square$

**Corollary (Davies-Meyer form).** For a fixed block $Y$, lines L6 to L9 compose 48 bijections of Lemma 3, so they compute a permutation $E_Y$ of 128-bit states. Line L10 returns $E_Y(H) + H$, with word-wise addition. So COMPRESS is the [Davies-Meyer construction](/davies-meyer-construction/) over the "block cipher" $E$, with the block $Y$ as the key and addition modulo $2^{32}$ in each word in place of XOR.

By Lemma 1 and Lemma 2, MD4 is the Merkle-Damgard construction with MD strengthening over COMPRESS. By the Merkle-Damgard theorem, a collision of MD4 gives a collision of COMPRESS. The converse is not true, and the reduction does not make MD4 secure: the attacks of Dobbertin and of Wang et al. find collisions of MD4 itself. The corollary also explains the fixed points: $\text{COMPRESS}(H, Y) = H$ exactly when $E_Y(H) = 0$, so $H = E_Y^{-1}(0)$ is a fixed point for each block $Y$.
