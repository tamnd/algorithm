---
title: Whirlpool is a Merkle-Damgard hash over a Miyaguchi-Preneel compression function on a block cipher
proves: [correctness]
status: full
---

We prove the structure that the page uses: the padding is injective and gives whole blocks, the loop computes the Merkle-Damgard iteration, and W is a permutation of the 512-bit block for every key, so COMPRESS has the Miyaguchi-Preneel form $W_H(m) \oplus H \oplus m$. That the code is the ISO/IEC 10118-3 function is checked by the vectors, not proved. Nothing here claims that Whirlpool is collision resistant.

**Lemma 1 (padding).** For a message of $n$ bytes with $8n < 2^{256}$, line L1 gives $P = M \| \texttt{80} \| 0^k \| [8n]_{256}$ with $k = (31 - n) \bmod 64$ zero bytes and the length in 32 bytes big-endian. Then 64 divides $|P|$, and $P$ determines $M$.

*Proof.* $|P| = n + 1 + k + 32 \equiv n + 1 + 31 - n + 32 = 64 \equiv 0 \pmod{64}$. The last 32 bytes give $8n$, so $n$, and the first $n$ bytes give $M$. $\square$

**Lemma 2 (the iteration).** Let $Y_1, \ldots, Y_\ell$ be the blocks of $P$, $H_0 = 0^{512}$ and $H_i = \mathrm{COMPRESS}(H_{i-1}, Y_i)$. After the loop of lines L3 and L4, $H = H_\ell$, and line L13 returns it.

*Proof.* Line L2 sets $H = H_0$. If $H = H_{i-1}$ before the $i$-th run of line L4, then $H = H_i$ after it. Induction on $i$ gives the claim. $\square$

**Lemma 3 (the layers are bijections).** $\gamma$, $\pi$, $\theta$ and $\sigma[k]$ are bijections of the set of $8 \times 8$ byte matrices, for every $k$.

*Proof.* $\gamma$ applies $S$ to each byte, and $S$ is a permutation of the 256 bytes: the test checks that its 256 values are distinct. (It also follows from the construction: $E$ and $R$ are permutations of 16 nibbles, and the map $(u_h, u_l) \mapsto (a, b) \mapsto (a \oplus r, b \oplus r)$ with $r = R[a \oplus b]$ is invertible, because $(a \oplus r) \oplus (b \oplus r) = a \oplus b$ gives back $r$.) $\pi$ moves each byte to a new place, and $(i, j) \mapsto ((i + j) \bmod 8, j)$ is a bijection of the positions. $\theta$ multiplies each row by the matrix $C$; since $C$ is MDS, all its square submatrices are nonsingular, in particular $C$ itself, so $\theta$ is invertible. $\sigma[k]$ is XOR with $k$, which undoes itself. $\square$

**Corollary (W is a block cipher).** For each key $K$, the round keys $K^0, \ldots, K^{10}$ of lines L7 and L10 are fixed. Lines L8 to L12 then compute the composition of XOR with $K^0$ and ten rounds $\rho[K^r] = \sigma[K^r] \circ \theta \circ \pi \circ \gamma$, each a bijection by Lemma 3. So $m \mapsto W_K(m)$ is a permutation of $\{0,1\}^{512}$.

**Lemma 4 (the Miyaguchi-Preneel form).** Line L6 returns $W_H(m) \oplus H \oplus m$, where the chaining value $H$ is the key and the block $m$ is the plaintext. This is HAC Algorithm 9.43 with the identity as the map $g$ from chaining values to keys.

*Proof.* Line L5 reads the block as the matrix $m$; line L6 calls W with key $H$ and plaintext $m$ and XORs the result with $H$ and with $m$, byte by byte. The key and the block have the same size, 512 bits, so no map $g$ is needed. $\square$

**Consequences.** By Lemmas 1 and 2, Whirlpool is the Merkle-Damgard construction with MD strengthening over COMPRESS, so the [Merkle-Damgard theorem](/merkle-damgard-theorem/) applies: any collision of Whirlpool gives a collision of COMPRESS. By the Corollary and Lemma 4, COMPRESS is the Miyaguchi-Preneel function of a block cipher. If W is modeled as an ideal cipher, the Black-Rogaway-Shrimpton analysis gives collision resistance of COMPRESS up to about $2^{256}$ queries, as on the [Miyaguchi-Preneel](/miyaguchi-preneel-construction/) page. This is a statement about the mode, not a proof about the real W. The number of blocks is $\lfloor (n + 32)/64 \rfloor + 1$, because $|P|$ is the least multiple of 64 that is at least $n + 33$.
