---
title: Salsa20 decryption inverts encryption, and the rounds are a permutation
proves: [correctness]
status: full
---

All words are 32-bit, $+$ is addition modulo $2^{32}$ and $\lll$ is left rotation.

**Lemma 1 (the quarterround is invertible).** QUARTERROUND is a bijection of $(\{0,1\}^{32})^4$.

*Proof.* Given the output $(z_0, z_1, z_2, z_3)$, we recover the input in the reverse order of lines L4 to L1. Line L4 gives $y_0 = z_0 \oplus ((z_3 + z_2) \lll 18)$, and $z_3, z_2$ are known. Line L3 gives $y_3 = z_3 \oplus ((z_2 + z_1) \lll 13)$. Line L2 gives $y_2 = z_2 \oplus ((z_1 + y_0) \lll 9)$, and $y_0$ is now known. Line L1 gives $y_1 = z_1 \oplus ((y_0 + y_3) \lll 7)$. So the map has a left inverse on a finite set, and it is a bijection. $\square$

**Lemma 2 (the rounds are a permutation).** The map of lines L5 to L8 is a bijection of the 16-word state.

*Proof.* COLUMNROUND applies QUARTERROUND to four disjoint sets of four words, and ROWROUND does the same for four other disjoint sets. Each is a bijection by Lemma 1, so each round is a bijection, and so is a composition of rounds. $\square$

Lemma 2 is the reason for the feedforward of line L9: the rounds alone could be inverted from an output block to the input, which holds the key.

**Lemma 3 (determinism).** The keystream block for counter $i$ is a function of $(k, v, i)$ only.

*Proof.* Line L10 builds the 16 words from the fixed constants, $k$, $v$ and $i$. Lines L5 to L9 apply fixed operations to them. $\square$

**Theorem.** Let $c$ = ENCRYPT$(k, v, m)$. Then ENCRYPT$(k, v, c) = m$. For one message, the hash inputs of different blocks are different.

*Proof.* By Lemma 3, both calls compute the same block $Z_i$ for each $i$. Byte $t$ of block $i$ of the second output is $(m_t \oplus Z_{i,t}) \oplus Z_{i,t} = m_t$, because XOR is associative and $z \oplus z = 0$. Both calls truncate the last block to the same length. The 64-bit counter $i$ takes distinct values for $0 \le i < \lceil |m|/64 \rceil < 2^{64}$, and it is part of the hash input, so the inputs differ. $\blacksquare$
