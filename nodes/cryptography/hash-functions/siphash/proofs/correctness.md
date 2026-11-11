---
title: The SipHash message encoding is injective, and each SipHash-c-d input is a unique sequence of state updates
proves: [correctness]
status: full
---

We work with byte strings. For a message $m$, $n = |m|$ is its length in bytes and $w = \lfloor n/8 \rfloor + 1$. Line L3 maps $m$ to the word sequence $W(m) = (m_1, \ldots, m_w)$ of 64-bit words. The first $w - 1$ words are the full 8-byte blocks of $m$, read little-endian. The last word $m_w$ holds the $r = n \bmod 8$ remaining bytes in its low bytes, then $7 - r$ zero bytes, then the byte $n \bmod 256$ in its top byte.

**Lemma 1 (the word count gives the length up to the last block).** From $W(m)$ one can read $w$, and $8(w - 1) \le n \le 8(w - 1) + 7$.

*Proof.* The sequence has $w$ words by construction, and $w = \lfloor n/8 \rfloor + 1$ means $8(w - 1) \le n < 8w$. $\square$

**Lemma 2 (the length can be read from the words).** From $W(m)$ one can read $n$.

*Proof.* By Lemma 1, $n = 8(w - 1) + r$ with $0 \le r \le 7$. The top byte of $m_w$ is $n \bmod 256$. Since $8(w - 1)$ is known, $r \equiv (n \bmod 256) - 8(w - 1) \pmod{256}$. As $0 \le r \le 7 < 256$, this congruence has exactly one solution $r$ in the range, so $r$ and $n$ are determined. $\square$

**Theorem 1 (injectivity of the encoding).** If $W(m) = W(m')$, then $m = m'$.

*Proof.* By Lemma 2 both messages have the same length $n$, so the same $w$ and $r$. The first $w - 1$ words are the full blocks of $m$ and $m'$, and little-endian reading of 8 bytes is a bijection, so the first $8(w - 1)$ bytes agree. The low $r$ bytes of $m_w$ are the last $r$ bytes of each message, so they agree too. $\blacksquare$

Without the length byte, the theorem fails: `ab` and `ab 00` would both give the single word `0000000000006261`, and every SipHash output would collide for such pairs under every key. The test `test_length_byte_separates_zero_padding` checks this case.

**Theorem 2 (the state updates are a function of $(k, W(m))$ and are invertible for a fixed key).** For a fixed key, each step of SipHash-$c$-$d$ is a bijection on the 256-bit state $(v_0, v_1, v_2, v_3)$.

*Proof.* Each step is one of the following maps, and each has an inverse.

1. XOR of a fixed word into one state word (lines L4 and L5): it is its own inverse.
2. A SipRound. It is a sequence of the maps $v_a \leftarrow v_a \boxplus v_b$, $v_b \leftarrow (v_b \lll s) \oplus v_a$ and $v_a \leftarrow v_a \lll 32$. The inverse of $v_a \leftarrow v_a \boxplus v_b$ is $v_a \leftarrow v_a \boxminus v_b$, since $v_b$ is unchanged. The inverse of $v_b \leftarrow (v_b \lll s) \oplus v_a$ is $v_b \leftarrow (v_b \oplus v_a) \ggg s$, since $v_a$ is unchanged. A rotation is undone by the rotation the other way.

A composition of bijections is a bijection. $\blacksquare$

**Consequence.** Take a fixed key and two messages whose word sequences first differ in word $i$. Both runs have the same state before word $i$. Line L4 XORs different words into $v_3$, so the states differ, and by Theorem 2 they stay different through the $c$ rounds of word $i$. After that, the XOR of $m_i$ into $v_0$ and the later words can make the two states meet, and the 64-bit outputs can coincide even when the states do not: the final XOR of four words in line L7 maps 256 bits to 64 bits, so collisions of the output exist. This is why SipHash is not collision resistant, and why its security is the PRF claim of the designers, which says that these collisions cannot be found without the key faster than by guessing. That claim is a conjecture from cryptanalysis, not a theorem; this page proves only that the encoding loses no information before the rounds.
