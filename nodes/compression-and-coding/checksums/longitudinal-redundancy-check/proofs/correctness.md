---
title: The two LRC forms compute their check values, and the errors they miss
proves: [correctness, termination]
status: full
---

Notation. A message is $M = M[0] \ldots M[n-1]$, bytes read as integers in $0..255$. A *frame* is $M$ followed by its check byte $v$. Bit $j$ of a byte is the bit of weight $2^j$; the bit *column* $j$ of a frame is bit $j$ of each of its bytes.

**Theorem 1 (XOR form).** `lrc_xor(M)` returns $M[0] \oplus \cdots \oplus M[n-1]$, and `check_xor(M, v)` is true if and only if $v$ equals this value.

*Proof.* Invariant of the loop of lines L2 and L3: before the step for index $i$, $x = M[0] \oplus \cdots \oplus M[i-1]$. It holds with $i = 0$ after line L1, since the empty XOR is 0, and line L3 extends it by $M[i]$. After the last step, line L4 returns the XOR of all bytes. Line L9 tests $\mathrm{lrc\_xor}(M) \oplus v = 0$, which holds if and only if $v = \mathrm{lrc\_xor}(M)$. $\square$

**Theorem 2 (Modbus form).** `lrc_modbus(M)` returns the $v \in 0..255$ with $\sum_i M[i] + v \equiv 0 \pmod{256}$, and `check_modbus(M, v)` is true if and only if $v$ is this value.

*Proof.* Invariant of the loop of lines L6 and L7: before the step for index $i$, $s = \sum_{t < i} M[t] \bmod 256$. Line L5 makes it true for $i = 0$, and line L7 keeps it, because reduction modulo 256 can be done after each addition. Line L8 returns $(256 - s) \bmod 256$, which is in $0..255$ and adds to $s$ to give a multiple of 256; it is the only such value in $0..255$. Line L10 tests $\sum M + v \equiv 0$, which by uniqueness holds exactly for this $v$. This is the function of Section 6.2.1 of the Modbus serial line guide: an 8-bit unsigned sum, negated in two's complement. $\square$

**Termination.** Each loop runs once for each byte of $M$, and each step does a constant amount of work.

**Errors missed by the XOR form.** Let the frame $F$ change into $F'$, and let $E[t] = F[t] \oplus F'[t]$ be the error bytes, including the check byte. The receiver accepts $F'$ if and only if the XOR of all bytes of $F'$ is 0. The XOR of all bytes of $F$ is 0 by Theorem 1, so the receiver accepts if and only if $E[0] \oplus \cdots \oplus E[n] = 0$, that is, if and only if every bit column has an even number of errors. Consequences:

1. Every error of odd weight is detected: the weights of the columns add up to an odd number, so one column is odd.
2. Two errors are missed if and only if they are in the same column.
3. Every burst of length at most 8 in the serial bit stream is detected, in either bit order inside a byte. Eight consecutive bits of the stream, with 8 bits per byte, fall in 8 different columns, so a burst of length $b \le 8$ puts at most one error in each column, and at least one column has exactly one.

**Errors missed by the Modbus form.** Let $d_t = F'[t] - F[t]$ as integers. Then $\sum F' + 0 \equiv \sum F + \sum_t d_t$, and $\sum F \equiv 0$ by Theorem 2. So the receiver accepts if and only if $D = \sum_t d_t \equiv 0 \pmod{256}$. An error in bit $j$ that changes a 0 into a 1 adds $+2^j$, and one that changes a 1 into a 0 adds $-2^j$.

4. A single error gives $D = \pm 2^j$ with $0 \le j \le 7$, and $0 < 2^j < 256$, so it is detected.
5. Two errors in bits $a \le b$ give $D = \pm 2^a \pm 2^b$. If $a < b$, then $0 < |D| \le 2^6 + 2^7 < 256$ when the signs agree, and $0 < |D| < 256$ when they differ, so $D \not\equiv 0$: detected. If $a = b < 7$, then $D = 0$ when the directions are opposite, and $D = \pm 2^{a+1}$ with $0 < 2^{a+1} < 256$ when they agree. If $a = b = 7$, then $D \in \{0, \pm 256\}$, always $\equiv 0$. So two errors are missed if and only if they are in the same column and either the directions are opposite or the column is bit 7.
6. Every burst of length $b \le 8$ in the serial bit stream is detected, in either bit order inside a byte. A burst of at most 8 bits lies in one byte or in two adjacent bytes. In one byte, $D$ is the change of that byte, with $0 < |D| \le 255$. In two bytes, the burst covers bits $c..7$ of one byte, with an error in bit $c$, and bits $0..a$ of the other byte, with an error in bit $a$. With the most significant bit first, the low part $0..a$ ends the first byte and the high part $c..7$ starts the second; with the least significant bit first, the high part ends the first byte and the low part starts the second. The burst covers $(8 - c) + (a + 1) \le 8$ bits, so $a + 1 \le c$. The change $d_H$ of the byte with bits $c..7$ is a multiple of $2^c$, and the change $d_L$ of the byte with bits $0..a$ satisfies $d_L \ne 0$, because the term $\pm 2^a$ is larger than the sum of the lower terms, and $|d_L| \le 2^{a+1} - 1 < 2^c$. If $D = d_H + d_L \equiv 0 \pmod{256}$, then $d_L \equiv -d_H \equiv 0 \pmod{2^c}$, which is false for $0 < |d_L| < 2^c$. So the burst is detected.

The implementation checks claims 2, 3, 5 and 6 exhaustively: every pair of positions in a frame of 7 bytes, and every burst of length 1 to 8 at every position in both bit orders.
