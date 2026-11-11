---
title: RC4 keeps a permutation and decryption inverts encryption
proves: [correctness]
status: full
---

We write $S_0$ for the array after line L1, and $Z_1, Z_2, \ldots$ for the bytes of line L11. All index arithmetic is modulo 256.

**Lemma 1 (permutation).** At each point after line L1, $S$ is a permutation of $\{0, 1, \ldots, 255\}$, and $i, j \in \{0, \ldots, 255\}$.

*Proof.* Line L1 makes $S$ the identity, which is a permutation. The only lines that write $S$ are L5 and L10, and each swaps two entries. If $S$ is a bijection from the index set to the value set, then $S \circ \tau$ for a transposition $\tau$ of two indices is also a bijection. By induction on the number of executed swaps, $S$ stays a permutation. The indices $i$ and $j$ are set by lines L2, L3, L4, L6, L8 and L9, each to a value modulo 256, so they are in range. The index of line L11 is reduced modulo 256 too. $\square$

**Lemma 2 (determinism).** For a fixed key $K$ and length $m$, the bytes $Z_1, \ldots, Z_m$ are a function of $K$ and $m$ only.

*Proof.* The KSA reads only $K$ and the entries of $S$, and each line computes its result from values already fixed. So $S$ after line L5 is a function of $K$. The PRGA reads only $S$, $i$ and $j$, and has no other input. By induction on the step number, the state $(S, i, j)$ after step $t$ and the byte $Z_t$ are functions of $K$ and $t$. By Lemma 1 each read is in range, so each step is defined. $\square$

**Theorem.** Let $C_t = M_t \oplus Z_t$ for $1 \le t \le m$. Then $C_t \oplus Z_t = M_t$ for each $t$, so the receiver with the same key recovers $M$.

*Proof.* By Lemma 2 the receiver computes the same $Z_t$. XOR is associative, $Z_t \oplus Z_t = 0$, and $x \oplus 0 = x$. So $C_t \oplus Z_t = M_t \oplus (Z_t \oplus Z_t) = M_t$. $\blacksquare$
