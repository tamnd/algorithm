---
title: bcrypt verification is correct, its encoding loses no information, and only the first 72 password bytes count
proves: [correctness]
status: full
---

We use the notation of the page: BCRYPT$(k, s, p)$ returns the string $\texttt{\$2b\$} \| k \| \texttt{\$} \| \mathrm{b64}(s) \| \mathrm{b64}(c)$, where $c$ is the first 23 bytes of the final ciphertext.

**Lemma 1 (the encoding of bcrypt is injective on its inputs).** The map $\mathrm{b64}$ from $n$-byte strings to strings of $\lceil 8n/6 \rceil$ characters over the 64-letter alphabet is injective, and its inverse reads the first $8n$ bits.

*Proof.* Each character stands for 6 bits, by a bijection between the alphabet and $\{0, \ldots, 63\}$. The encoder writes the $8n$ bits of the input in order, padded with zero bits to a multiple of 6. The decoder concatenates the $6 \lceil 8n/6 \rceil$ bits and keeps the first $8n$, which are the input bits. So decode(encode($x$)) $= x$, and encode is injective. For the salt, $n = 16$ gives 22 characters; for the hash, $n = 23$ gives 31 characters. $\square$

**Lemma 2 (the setting can be parsed back).** From the string BCRYPT$(k, s, p)$ one reads $k$ and $s$.

*Proof.* The prefix has 4 characters, the cost 2 digits, then one `$`. The next 22 characters are $\mathrm{b64}(s)$, which by Lemma 1 give $s$. The base64 alphabet has no `$`, so the fields cannot run into each other. $\square$

**Theorem 1 (verification).** Let $h$ = BCRYPT$(k, s, p)$. Then CHECKPW$(p, h)$ returns true.

*Proof.* CHECKPW takes the first 29 characters of $h$, which by Lemma 2 give the same $k$ and $s$, and computes BCRYPT$(k, s, p)$ again. Every step of BCRYPT is deterministic: INITSTATE is a constant, EXPANDKEY is a fixed function of its inputs, and the 64 encryptions of a constant text are fixed functions of the state. So the result equals $h$. $\blacksquare$

**Lemma 3 (the key enters only through 72 bytes).** In EXPANDKEY$(\text{state}, \text{salt}, K)$, the key $K$ is used only to XOR the 18 words of the P-array with the first 72 bytes of the cyclic stream $K K K \cdots$.

*Proof.* By the definition of EXPANDKEY, the key is read only in its first loop, which runs over $P_1, \ldots, P_{18}$ and takes 4 bytes of the cyclic key stream for each. That is 72 bytes. The rest of EXPANDKEY uses only the salt and the state. $\square$

**Theorem 2 (the 72-byte limit).** If two passwords $p$ and $p'$ have the same first 72 bytes, then BCRYPT$(k, s, p)$ = BCRYPT$(k, s, p')$.

*Proof.* Line L1 sets $K = p_{[0, 72)} \| 00$ when $|p| \ge 72$, so for $|p|, |p'| \ge 72$ the keys are equal and the outputs are equal. In the code and in OpenBSD with $|p| \ge 72$, the cyclic key stream begins with the 72 bytes of $p_{[0,72)}$, and by Lemma 3 nothing after them is read. So passwords of 72 bytes or more that agree on 72 bytes give the same output, which the tests check. $\blacksquare$

**A remark on shorter passwords.** For $|p| < 72$ the zero byte at the end of the key is part of the cyclic stream. It separates, for example, `ab` from `abab`: their streams are `ab0ab0...` and `abab0abab0...`, which differ in the third byte. Without the zero byte, the streams of `ab` and `abab` would both be `ababab...`, and the two passwords would collide. This is one reason the `$2a$` version made the zero byte part of the key.
