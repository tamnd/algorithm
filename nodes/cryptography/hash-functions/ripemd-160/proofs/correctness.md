---
title: RIPEMD-160 is a Merkle-Damgard hash whose compression function adds two permutations of the chaining value
proves: [correctness]
status: full
---

We prove the structure that the page uses: the padding is injective and gives whole blocks, the loop computes the Merkle-Damgard iteration, and for a fixed block each of the two lines computes a permutation of the chaining value, so COMPRESS adds the chaining value and two permutations of it. That the code is the function of Dobbertin, Bosselaers and Preneel is checked by the Bosselaers vectors and by `hashlib`, not proved. Nothing here claims that RIPEMD-160 is collision resistant.

**Lemma 1 (padding).** For a message of $n$ bytes with $8n < 2^{64}$, line L1 gives $P = M \| \texttt{80} \| 0^k \| [8n]_{64}$, with $k = (55 - n) \bmod 64$ zero bytes and the length in 8 bytes little-endian. Then 64 divides $|P|$, and $P$ determines $M$.

*Proof.* $|P| = n + 1 + k + 8 \equiv n + 1 + 55 - n + 8 = 64 \equiv 0 \pmod{64}$. The last 8 bytes of $P$ give $8n$, so $n$, and the first $n$ bytes give $M$. $\square$

**Lemma 2 (the iteration).** Let $Y_1, \ldots, Y_m$ be the blocks of $P$, $H_0 = IV$ and $H_i = \mathrm{COMPRESS}(H_{i-1}, Y_i)$. After the loop of lines L3 and L4, $H = H_m$, and line L12 returns its 20 bytes.

*Proof.* Line L2 sets $H = H_0$. If $H = H_{i-1}$ before the $i$-th run of line L4, then $H = H_i$ after it. Induction on $i$ gives the claim. $\square$

**Lemma 3 (each step is invertible).** Fix the block, so that $X$ is fixed, and fix a step $j$ of one line, so that $f$, the word $x = X[r_j]$, the constant $K$ and the rotation $s$ are fixed. The map $(A, B, C, D, E) \mapsto (E, T, B, C \lll 10, D)$ with $T = ((A + f(B, C, D) + x + K) \lll s) + E$ is a bijection of $(\{0,1\}^{32})^5$.

*Proof.* From the output $(A^*, B^*, C^*, D^*, E^*)$ we read $E = A^*$, $B = C^*$, $C = D^* \ggg 10$ and $D = E^*$. Then $T = B^*$, and $A = ((T - E) \ggg s) - f(B, C, D) - x - K$, because subtraction modulo $2^{32}$ undoes addition and right rotation undoes left rotation. So the map has an inverse. $\square$

**Corollary (two permutations).** For a fixed block $Y$, the left line (80 steps of line L8 and line L10) computes a permutation $L_Y$ of $\{0,1\}^{160}$, and the right line (line L9 and line L10) computes a permutation $R_Y$, each a composition of 80 bijections of Lemma 3. Both start from $H$ by line L6, and they do not share registers, so the order in which the code runs them does not matter.

**Lemma 4 (the combination).** Write $(A, B, C, D, E) = L_Y(H)$ and $(A', B', C', D', E') = R_Y(H)$. Then line L11 returns $\sigma(H) + \tau(L_Y(H)) + \upsilon(R_Y(H))$, word by word modulo $2^{32}$, where $\sigma$, $\tau$ and $\upsilon$ are fixed permutations of the five word positions.

*Proof.* Output word $i$ is $h_{i+1 \bmod 5}$ plus word $i + 2 \bmod 5$ of the left result plus word $i + 3 \bmod 5$ of the right result, with words numbered $A = 0, \ldots, E = 4$: for $i = 0$ this is $h_1 + C + D'$, and so on to $h_0 + B + C'$ for $i = 4$, as line L11 states. Each of the three index maps is a cyclic shift, so a permutation of the positions. $\square$

**Consequences.** By Lemmas 1 and 2, RIPEMD-160 is the Merkle-Damgard construction with MD strengthening over COMPRESS, so the [Merkle-Damgard theorem](/merkle-damgard-theorem/) applies: from any collision of RIPEMD-160 one can read off a collision of COMPRESS. By Lemma 4, COMPRESS is not a Davies-Meyer function $E_Y(H) + H$ of one permutation: it adds two different permutations of $H$ and $H$ itself. For a fixed block, a collision of COMPRESS needs $\sigma(H) + \tau(L_Y(H)) + \upsilon(R_Y(H))$ to agree on two chaining values, and a differential path must pass through both lines at once. The number of blocks is $|P|/64 = \lfloor (n + 8)/64 \rfloor + 1$, because $|P|$ is the least multiple of 64 that is at least $n + 9$.
