---
title: Tiger is a Merkle-Damgard hash whose compression function combines the chaining value with a permutation of it
proves: [correctness]
status: full
---

We prove the structure that the page uses: the padding is injective and gives whole blocks, the loop computes the Merkle-Damgard iteration, and for a fixed block the 24 rounds compute a permutation of the three registers, which line L13 combines with the input word by word. That the code is the function of Anderson and Biham is checked by the vectors of the Tiger page, not proved. Nothing here claims that Tiger is collision resistant.

**Lemma 1 (padding).** Let the pad byte $p$ be $\texttt{01}$ (Tiger) or $\texttt{80}$ (Tiger2). For a message of $n$ bytes with $8n < 2^{64}$, line L1 gives $P = M \| p \| 0^k \| [8n]_{64}$, with $k = (55 - n) \bmod 64$ zero bytes and the length in 8 bytes little-endian. Then 64 divides $|P|$, and $P$ determines $M$.

*Proof.* $|P| = n + 1 + k + 8 \equiv n + 1 + 55 - n + 8 = 64 \equiv 0 \pmod{64}$. The last 8 bytes of $P$ give $8n$, so $n$, and the first $n$ bytes give $M$. $\square$

**Lemma 2 (the iteration).** Let $Y_1, \ldots, Y_m$ be the blocks of $P$, $H_0 = IV$ and $H_i = \mathrm{COMPRESS}(H_{i-1}, Y_i)$. After the loop of lines L3 and L4, $(a, b, c) = H_m$, and line L14 returns its 24 bytes.

*Proof.* Line L2 sets $(a, b, c) = H_0$. If $(a, b, c) = H_{i-1}$ before the $i$-th run of line L4, then $(a, b, c) = H_i$ after it. Induction on $i$ gives the claim. $\square$

**Lemma 3 (each round is invertible).** Fix a message word $x$ and an odd multiplier $\mathit{mul}$. Let $F(c) = t_1[c_0] \oplus t_2[c_2] \oplus t_3[c_4] \oplus t_4[c_6]$ and $G(c) = t_4[c_1] \oplus t_3[c_3] \oplus t_2[c_5] \oplus t_1[c_7]$. The map $(a, b, c) \mapsto (a', b', c')$ with $c' = c \oplus x$, $a' = a - F(c')$ and $b' = (b + G(c')) \times \mathit{mul}$ (lines L9 to L12) is a bijection of $(\{0,1\}^{64})^3$.

*Proof.* Since $\mathit{mul}$ is odd, it is a unit modulo $2^{64}$; let $u$ be its inverse. From $(a', b', c')$ we get $c = c' \oplus x$, then $a = a' + F(c')$ and $b = b' \times u - G(c')$, because $F$ and $G$ depend only on $c'$, which we know. So the map has an inverse. $\square$

**Lemma 4 (the key schedule is invertible).** KEY-SCHEDULE is a bijection of $(\{0,1\}^{64})^8$.

*Proof.* Each of its 16 steps changes one word $x_i$ by XOR, addition or subtraction with a value computed from other words only: for example $x_3 \mathrel{-}= x_2 \oplus (\neg x_1 \ll 19)$ uses $x_2$ and $x_1$, and $x_7 \mathrel{-}= x_6 \oplus \texttt{0123456789ABCDEF}$ uses $x_6$. Such a step is undone by the opposite operation with the same value, which the inverse can compute because those other words are unchanged by the step. A composition of bijections is a bijection. $\square$

**Corollary (a permutation of the chaining value).** For a fixed block $Y$, the words $x$ of each pass are fixed: the first pass uses the words of $Y$, and the next two use KEY-SCHEDULE applied once and twice. So lines L6 to L12 compute a composition of 24 maps of Lemma 3, each followed by a fixed renaming of the registers, which is a permutation of the three positions. The result is a permutation $E_Y$ of $\{0,1\}^{192}$. By Lemma 4, the words of the second pass alone, and also those of the third pass alone, determine $Y$.

**Lemma 5 (the feed-forward).** Write $(a, b, c) = E_Y(a_0, b_0, c_0)$. Line L13 returns $(a \oplus a_0, b - b_0, c + c_0)$, so $\mathrm{COMPRESS}(H, Y) = E_Y(H) \star H$, where $\star$ is $\oplus$ on the first word, $-$ on the second and $+$ on the third.

*Proof.* Line L5 copies the input into the registers, and the passes change only the registers and $x$. Line L13 combines the final registers with the saved input, one word at a time, as stated. $\square$

**Consequences.** By Lemmas 1 and 2, Tiger and Tiger2 are the Merkle-Damgard construction with MD strengthening over COMPRESS, so the [Merkle-Damgard theorem](/merkle-damgard-theorem/) applies: from any collision of Tiger one can read off a collision of COMPRESS. By the Corollary and Lemma 5, COMPRESS has the Davies-Meyer form, with the block as the key of the permutation $E_Y$, except that the feed-forward uses a different group operation on each word. Without the feed-forward, anyone could invert $E_Y$ by Lemmas 3 and 4 and so find preimages of COMPRESS at once; with it, an output fixes only $E_Y(H) \star H$, and Lemma 3 gives no way to solve for $H$. The number of blocks is $|P|/64 = \lfloor (n + 8)/64 \rfloor + 1$, because $|P|$ is the least multiple of 64 that is at least $n + 9$.
