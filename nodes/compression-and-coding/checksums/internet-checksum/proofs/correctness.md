---
title: The Internet checksum is the complement of the ones' complement sum, and its exact miss rule
proves: [correctness]
status: full
---

Let the message, after the padding of line L1, have the words $x_1, \ldots, x_m \in [0, 65535]$, and let $T = x_1 + \cdots + x_m$ as an integer. Write $\mathrm{oc}(T)$ for $0$ if $T = 0$, and for the unique value in $[1, 65535]$ that is congruent to $T$ modulo 65535 otherwise. On [ones' complement arithmetic](/ones-complement-arithmetic/) we show that the ones' complement sum $S = x_1 \oplus \cdots \oplus x_m$ equals $\mathrm{oc}(T)$.

**Lemma 1 (the loop).** After the loop of lines L3 and L4, $s = T$.

*Proof.* The invariant at the test of line L3 is that $s$ is the plain sum of the words before position $i$. Line L2 starts it at 0, and line L4 adds the next word. No reduction takes place. $\square$

**Lemma 2 (the fold).** Lines L5 and L6, started with $s = T$, stop with $s = \mathrm{oc}(T)$.

*Proof.* Write $s = 2^{16} h + l$ with $h \ge 1$ and $0 \le l < 2^{16}$. Line L6 sets $s$ to $h + l$. Since $2^{16} \equiv 1 \pmod{65535}$, the residue of $s$ modulo 65535 does not change. Since $h \ge 1$ and $2^{16} h > h$, the value strictly decreases, so the loop stops, and when it stops $s < 2^{16}$. If $T = 0$ the loop does not run, and $s = 0$. If $T > 0$, each step keeps $s > 0$, because $h \ge 1$. So the final $s$ is in $[1, 65535]$ and congruent to $T$, which is $\mathrm{oc}(T)$. $\square$

**Theorem 1 (output).** Line L7 returns $C = 65535 - S$, and a message that holds $C$ in its checksum field has the ones' complement sum 0xFFFF.

*Proof.* By Lemmas 1 and 2, $s = S$ before line L7. The bitwise complement of a 16-bit value $S$ is $65535 - S$. With $C$ in the field (which held 0 before), the new total is $T' = T + C$. If $T = 0$, then $S = 0$, $C = 65535$ and $\mathrm{oc}(T') = 65535$. If $T > 0$, then $T' > 0$ and $T' \equiv S + C = 65535 \equiv 0 \pmod{65535}$, so $\mathrm{oc}(T') = 65535$. $\square$

**Theorem 2 (exact miss rule).** Let a message with total $T$ change into a message with the same number of words and total $T'$. The receiver misses the change if and only if $\mathrm{oc}(T') = \mathrm{oc}(T)$, that is, if and only if $T' \equiv T \pmod{65535}$ and ($T = 0 \Leftrightarrow T' = 0$).

*Proof.* The receiver computes the checksum of the received data with the field zeroed and compares it with the received field, or sums everything and tests for 0xFFFF. In both cases the received data passes if and only if its ones' complement sum equals that of the sent data, by Theorem 1. The two sums are $\mathrm{oc}(T)$ and $\mathrm{oc}(T')$, and the definition of $\mathrm{oc}$ gives the second form. $\square$

**Corollary 1 (bursts).** Let an error change only bits inside a window of $r$ consecutive bits of the message, in the order in which the bytes are sent and with the high bit of each byte first. If $r \le 15$, the error is detected. If $r = 16$, the error is detected unless the 16 bits of the window go from all zeros to all ones, or from all ones to all zeros.

*Proof.* Give each bit of the message its position $b \in \{0, \ldots, 15\}$ inside its 16-bit word, counted from the low bit. In big-endian words, the bits of byte $2j$ have positions 15 down to 8 and the bits of byte $2j + 1$ have positions 7 down to 0. So along the message, the position goes 15, 14, ..., 0, then 15 again for the next word: consecutive bits have consecutive positions modulo 16. A window of $r \le 16$ consecutive bits therefore has $r$ distinct positions $b_1, \ldots, b_r$. A bit at position $b$ adds $2^b$ to $T$, so the error changes $T$ by $\Delta = \sum_t \epsilon_t 2^{b_t}$ with $\epsilon_t \in \{-1, 0, +1\}$, not all 0. Since the positions are distinct, $\Delta \ne 0$: its lowest nonzero term decides its residue modulo the next power of two. Also $|\Delta| \le \sum_t 2^{b_t} \le 65535$. If $r \le 15$, one position $b$ is missing, so $|\Delta| \le 65535 - 2^b < 65535$. Then $0 < |\Delta| < 65535$, so $\Delta \not\equiv 0 \pmod{65535}$, and the error is detected by Theorem 2. If $r = 16$, the same holds unless $|\Delta| = 65535$, which needs all 16 terms to be nonzero with the same sign: every bit of the window goes from 0 to 1, or every bit from 1 to 0. $\square$

**Corollary 2 (single errors).** Every single-bit error is detected, and every change of one word is detected except 0x0000 to 0xFFFF and back.

*Proof.* A single-bit error is a burst of length 1. A change of one word from $a$ to $a'$ changes $T$ by $a' - a$ with $|a' - a| \le 65535$, which is a multiple of 65535 only for $\{a, a'\} = \{0, 65535\}$. $\square$

**Corollary 3 (order).** Any permutation of the words of the message is missed.

*Proof.* A permutation leaves $T$ unchanged. $\square$

**Cost.** Line L4 runs $\lceil n/2 \rceil$ times. Each run of line L6 on a value below $2^{32}$ gives a value below $2^{16} + 2^{16}$, and a second run gives a value below $2^{16}$, so the fold takes at most two steps for a 32-bit total. So the time is $\Theta(n)$, with $O(1)$ extra space. $\blacksquare$
