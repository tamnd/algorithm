---
title: UTF-16 is a bijection from scalar values to well-formed unit sequences, and the decoder inverts it
proves: [correctness, termination]
status: full
---

**Claim.** (a) UTF16-ENCODE (lines L1 to L3) maps each Unicode scalar value to a well-formed UTF-16 code unit sequence of length 1 or 2, and this map is a bijection between the scalar values and the well-formed sequences of one character. (b) For every sequence $U$ of $n$ code units, UTF16-DECODE (lines L4 to L11) stops after at most $n$ iterations. If $U$ is well-formed, it outputs the scalar values that $U$ encodes. If not, it outputs one U+FFFD for each unpaired surrogate and decodes the rest.

**Setup.** A code unit is an integer in $0 \ldots \mathtt{FFFF}$. A high surrogate is a unit in D800..DBFF and a low surrogate a unit in DC00..DFFF. By D91 of the core specification, a well-formed UTF-16 sequence of one character is either one unit that is not a surrogate or a high surrogate followed by a low surrogate. A sequence is well-formed if it is a concatenation of such pieces. A surrogate that is not part of such a pair is *unpaired*: a high surrogate that is not followed by a low surrogate, or a low surrogate that does not follow a high surrogate of a pair.

**Lemma 1 (encoding).** If $c < \mathtt{10000}$, line L1 returns the one unit $c$, which is not a surrogate because $c$ is a scalar value. If $\mathtt{10000} \le c \le \mathtt{10FFFF}$, then $v = c - \mathtt{10000}$ is in $0 \ldots \mathtt{FFFFF}$, a 20-bit number. Its high 10 bits $v \gg 10$ are in $0 \ldots \mathtt{3FF}$, so the first unit of line L3 is in D800..DBFF. Its low 10 bits are in $0 \ldots \mathtt{3FF}$, so the second unit is in DC00..DFFF. So the output is well-formed.

The map is injective. One-unit outputs are the values $c$ themselves. Two-unit outputs carry the 20 bits of $v$ without loss, and $c = v + \mathtt{10000}$. It is onto. A non-surrogate unit $u$ is the scalar value $u$ and encodes to itself. A pair $h, l$ gives $v = 2^{10}(h - \mathtt{D800}) + (l - \mathtt{DC00})$ in $0 \ldots \mathtt{FFFFF}$, and $c = v + \mathtt{10000}$ is a scalar value of 10000..10FFFF that encodes to $h, l$. $\square$

**Lemma 2 (one step).** Let $0 \le i < n$ and $u = U[i]$. One iteration of the loop of line L5 does one of three things.

1. $u$ is not a surrogate (line L7). It outputs $u$ and moves $i$ by 1.
2. $u$ is a high surrogate and $U[i+1]$ exists and is a low surrogate (line L8). Line L9 outputs $\mathtt{10000} + 2^{10}(u - \mathtt{D800}) + (U[i+1] - \mathtt{DC00})$, which is the scalar value that the pair encodes by Lemma 1, and moves $i$ by 2.
3. Otherwise $u$ is a low surrogate, or a high surrogate without a low surrogate after it (line L10). It outputs U+FFFD and moves $i$ by 1.

**Invariant.** At the start of each iteration, $U[i]$ is not the second unit of a pair whose first unit is before $i$. This holds for $i = 0$. Case 2 skips both units of the pair. Cases 1 and 3 move past one unit that is not a high surrogate followed by a low surrogate, so the unit at the new $i$ cannot be the second unit of a pair that starts at the old $i$.

**Proof of (b).** Each iteration raises $i$ by 1 or 2, so the loop stops after at most $n$ iterations, at line L11. By the invariant, case 3 meets a low surrogate only when that surrogate does not follow a high surrogate of a pair, so it is unpaired. A high surrogate meets case 3 only when no low surrogate follows it, so it is unpaired too. Conversely, every unpaired surrogate is reached as $U[i]$ in some iteration, because the scan skips only the second units of pairs, and it then falls into case 3. So the output has one U+FFFD per unpaired surrogate. If $U$ is well-formed, there are no unpaired surrogates, every piece is handled by case 1 or case 2, and by Lemma 1 the output is the sequence of encoded scalar values. In strict mode, case 3 raises an error at offset $i$ instead. $\blacksquare$

**Byte layer.** UTF-16BE and UTF-16LE write each unit as two bytes, high byte first or low byte first. A byte string of even length maps one to one to a unit sequence, so the claim carries over. For odd length, the last byte is a truncated unit. The decoder outputs one more U+FFFD for it, and when the unit before it is a high surrogate, which then cannot have a partner, it counts the 3 bytes as one truncated sequence. This matches Python's codecs and changes nothing for well-formed input, which always has even length.
