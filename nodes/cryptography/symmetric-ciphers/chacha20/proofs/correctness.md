---
title: ChaCha20 decryption inverts encryption, and no block input repeats
proves: [correctness]
status: full
---

All words are 32-bit and $+$ is addition modulo $2^{32}$.

**Lemma 1 (the rounds are a permutation).** The map of lines L7 to L9 on the 16-word state is a bijection.

*Proof.* Each of lines L1 to L4 is a composition of three steps of the forms $u \leftarrow u + v$, $u \leftarrow u \oplus v$ and $u \leftarrow u \lll r$, where $u$ and $v$ are different words. Each step has an inverse: $u \leftarrow u - v$, $u \leftarrow u \oplus v$ and $u \leftarrow u \ggg r$, because $v$ is unchanged by the step. A composition of bijections is a bijection, so QR is a bijection of its four words, and it leaves the other twelve words fixed. Lines L8 and L9 and the loop of line L7 are compositions of such maps. $\square$

Lemma 1 explains the feedforward of line L10: without it the block output would be the image of a known-structure input under a public bijection, and inverting it would reveal the key words. With it, the output is $P(x) + x$, which is not invertible in general.

**Lemma 2 (determinism).** BLOCK$(K, ctr, N)$ depends only on $K$, $ctr$ and $N$.

*Proof.* Line L5 builds $x$ from the fixed constants and the three inputs. Lines L6 to L10 compute their result from $x$ alone by fixed operations. $\square$

**Theorem.** Let $C$ = ENCRYPT$(K, c_0, N, M)$ with $c_0 + \lceil m/64 \rceil - 1 < 2^{32}$. Then ENCRYPT$(K, c_0, N, C) = M$. Also, within one message the block inputs $(K, c_0 + j, N)$ for $0 \le j < \lceil m/64 \rceil$ are pairwise distinct.

*Proof.* For each $j$, line L12 computes the same block $Z_j$ in both calls, by Lemma 2. Line L13 sets byte $t$ of block $j$ of $C$ to $M_t \oplus Z_{j,t}$, and the second call sets it to $(M_t \oplus Z_{j,t}) \oplus Z_{j,t} = M_t$, because XOR is associative and $z \oplus z = 0$. The lengths agree, since line L13 truncates to the length of its input in both calls. For the second claim, the counters $c_0 + j$ are distinct integers below $2^{32}$ by the precondition, so they are distinct as 32-bit words, and no wrap-around occurs. $\blacksquare$
