---
title: The CRC-32C code computes the CRC-32/ISCSI value, and the distance search is exact
proves: [correctness, termination]
status: full
---

**Theorem 1.** `crc32c(data)` returns the CRC with width 32, poly 0x1EDC6F41, init 0xFFFFFFFF, refin and refout true, and xorout 0xFFFFFFFF.

*Proof.* Line L1 builds the table from the reflected poly 0x82F63B78 by 8 right shifts for each byte, which is the table $T'$ of the reflected form of the [table-driven CRC](/table-driven-crc/). Lines L3 and L4 are the reflected byte step of that page. Line L2 sets the register to the reversal of init, which is 0xFFFFFFFF again, and line L5 applies xorout. Theorem 2 of the table-driven proof says this equals the bit-by-bit CRC with these parameters. $\square$

**Continuation.** `crc32c(b, crc32c(a)) = crc32c(a + b)`. The call with `crc` set to $c = \mathrm{crc32c}(a)$ starts from the register $c \oplus \text{0xFFFFFFFF}$, which is the register after $a$, before xorout. From there the loop processes $b$, which is the same as the loop over $a + b$.

**Termination.** The loop of line L1 runs 256 times with 8 steps each, and the loop of line L3 runs once for each byte.

**Lemma 2 (syndromes).** Let $s_i = x^i \bmod G$ in the normal domain. A nonzero error pattern $E = \sum_{i \in S} x^i$ on a codeword of length $N$ bits is not detected if and only if $\bigoplus_{i \in S} s_i = 0$.

*Proof.* By the [cyclic redundancy check](/cyclic-redundancy-check/) page, an error is missed exactly when $G \mid E$, that is, when $E \bmod G = 0$. The map $E \mapsto E \bmod G$ is linear over GF(2), so $E \bmod G = \sum_{i \in S} s_i$. With refin and refout the positions are permuted, but the weight of a pattern is the same. $\square$

**Lemma 3 (the search for weight 2 or 4).** `has_weight_2_or_4(N)` returns true if and only if a codeword of length at most $N$ has weight 2 or 4.

*Proof.* A codeword of weight 2 is a pair $a < b$ with $s_a = s_b$. The first test finds it exactly. If the first test fails, all $s_i$ are distinct. A codeword of weight 4 at positions $a, b, c, d$ gives $s_a \oplus s_b = s_c \oplus s_d$ for the two pairs $\{a, b\}$ and $\{c, d\}$. The loop visits every pair and stops at the first pair whose XOR it has seen before, so it finds a match if one exists. Conversely, if two different pairs $\{a, b\} \neq \{c, d\}$ have the same XOR, they share no index: if $a = c$, then $s_b = s_d$, so $b = d$ because the $s_i$ are distinct, and the pairs would be equal. So the four positions are distinct and form a codeword of weight 4. $\square$

**Lemma 4 (even weight).** If $G$ has an even number of nonzero terms, then every codeword has even weight.

*Proof.* $G(1) = 0$ in GF(2), so $(x + 1) \mid G$. Every codeword is a multiple of $G$, so it vanishes at $x = 1$, which means it has an even number of terms. $\square$

**Consequence.** The polynomial $x^{32} + $ 0x1EDC6F41 has 18 terms. So by Lemma 4 there is no codeword of weight 1, 3 or 5, and by Lemma 3 the test at $N = 1056$ shows there is none of weight 2 or 4. The minimum distance at 1024 data bits is at least 6. For the IEEE CRC-32 the test finds a set of five positions whose syndromes XOR to 0, which is a codeword of weight 5 by Lemma 2, so the minimum distance there is at most 5.
