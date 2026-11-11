---
title: TEA decryption inverts encryption, and each TEA key has three equivalent keys
proves: [correctness]
status: full
---

All words are 32-bit, $+$ and $-$ are modulo $2^{32}$, and $\ll$, $\gg$ are logical shifts. Let
$$F(x, s, a, b) = ((x \ll 4) + a) \oplus (x + s) \oplus ((x \gg 5) + b), \qquad \mathit{sum}_i = i\delta \bmod 2^{32}.$$
Cycle $i$ of TEA-ENCRYPT is the map $\Phi_i(v_0, v_1) = (v_0', v_1')$ with $v_0' = v_0 + F(v_1, \mathit{sum}_i, k_0, k_1)$ (line L4) and $v_1' = v_1 + F(v_0', \mathit{sum}_i, k_2, k_3)$ (line L5). Line L3 makes $\mathit{sum} = \mathit{sum}_i$ during cycle $i$.

**Lemma 1 (one cycle is invertible).** Let $\Psi_i(v_0', v_1') = (v_0, v_1)$ with $v_1 = v_1' - F(v_0', \mathit{sum}_i, k_2, k_3)$ and $v_0 = v_0' - F(v_1, \mathit{sum}_i, k_0, k_1)$. Then $\Psi_i(\Phi_i(v)) = v$.

*Proof.* Apply $\Psi_i$ to $(v_0', v_1') = \Phi_i(v_0, v_1)$. The first step gives $v_1' - F(v_0', \mathit{sum}_i, k_2, k_3) = v_1$, since $v_1' = v_1 + F(v_0', \mathit{sum}_i, k_2, k_3)$ and addition modulo $2^{32}$ is a group operation. The second step uses this $v_1$ and gives $v_0' - F(v_1, \mathit{sum}_i, k_0, k_1) = v_0$ for the same reason. $\square$

**Theorem 1 (decryption inverts encryption).** For each block $v$ and key $k$, TEA-DECRYPT(TEA-ENCRYPT$(v, k), k) = v$.

*Proof.* Encryption computes $\Phi_{32} \circ \cdots \circ \Phi_1$. In decryption, line L7 sets $\mathit{sum} = 32\delta = \mathit{sum}_{32}$, and line L11 subtracts $\delta$ at the end of each cycle, so decryption cycle $j$ runs with $\mathit{sum}_{33-j}$. Lines L9 and L10 with that value are exactly $\Psi_{33-j}$. So decryption computes $\Psi_1 \circ \cdots \circ \Psi_{32}$, and by Lemma 1 applied from the inside out, $\Psi_1 \circ \cdots \circ \Psi_{32} \circ \Phi_{32} \circ \cdots \circ \Phi_1$ is the identity. $\square$

So TEA-ENCRYPT$(\cdot, k)$ has a left inverse on the finite set $\{0,1\}^{64}$, and it is a permutation.

**Lemma 2 (adding the top bit).** For each word $x$, $x + 2^{31} \equiv x \oplus 2^{31} \pmod{2^{32}}$.

*Proof.* The bits $0$ to $30$ of $2^{31}$ are zero, so the addition does not change bits $0$ to $30$ of $x$ and makes no carry into bit 31. Bit 31 becomes $x_{31} \oplus 1$, and the carry out of bit 31 is dropped by the reduction modulo $2^{32}$. $\square$

**Lemma 3 (the top-bit pair cancels).** Let $t = 2^{31}$. For all $x, s, a, b$, $F(x, s, a \oplus t, b \oplus t) = F(x, s, a, b)$.

*Proof.* By Lemma 2, $a \oplus t = a + t$, so $(x \ll 4) + (a \oplus t) = ((x \ll 4) + a) + t = ((x \ll 4) + a) \oplus t$, using Lemma 2 again. In the same way $(x \gg 5) + (b \oplus t) = ((x \gg 5) + b) \oplus t$. The middle term $x + s$ does not change. So
$$F(x, s, a \oplus t, b \oplus t) = ((x \ll 4) + a) \oplus t \oplus (x + s) \oplus ((x \gg 5) + b) \oplus t = F(x, s, a, b),$$
since $t \oplus t = 0$. $\square$

**Theorem 2 (equivalent keys).** Let $t = 2^{31}$ and $k = (k_0, k_1, k_2, k_3)$. The four keys
$$k, \quad (k_0 \oplus t, k_1 \oplus t, k_2, k_3), \quad (k_0, k_1, k_2 \oplus t, k_3 \oplus t), \quad (k_0 \oplus t, k_1 \oplus t, k_2 \oplus t, k_3 \oplus t)$$
are pairwise different and give the same encryption permutation. So the $2^{128}$ keys define at most $2^{126}$ permutations, and an exhaustive key search needs at most $2^{126}$ trials.

*Proof.* The keys differ in the top bits of their words, so they are pairwise different. In TEA-ENCRYPT, $k_0$ and $k_1$ appear only in line L4, as the arguments $a, b$ of $F$, and $k_2$ and $k_3$ appear only in line L5, as $a, b$. By Lemma 3, flipping the top bits of the pair used in a line does not change the value that the line adds. So each cycle $\Phi_i$ is the same map for the four keys, and so is the composition. The relation "gives the same permutation" is an equivalence relation, and by the above each class contains at least the four keys of this form. These sets of four partition $\{0,1\}^{128}$, because the map that flips a fixed set of top bits is an involution. So there are at most $2^{128}/4 = 2^{126}$ classes. $\blacksquare$

The test `test_equivalent_keys_give_the_same_ciphertext` checks Theorem 2 on 200 random blocks and keys, and `test_one_top_bit_alone_changes_the_ciphertext` checks that a single flipped top bit is not an equivalence.
