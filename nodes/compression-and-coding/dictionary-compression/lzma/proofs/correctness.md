---
title: LZMA-DECODE inverts the greedy LZMA encoder
proves: [correctness]
status: full
---

We use the decoder LZMA-DECODE (lines L1 to L15), its bit decoder DECODE-BIT (lines B1 to B5) and the encoder on the page. Let $x = x[0 \ldots n-1]$ and let the header carry the size $n$.

**Claim.** LZMA-DECODE(ENCODE($x$)) $= x$.

The proof has two layers. Part 1 shows that the range decoder returns the bits that the range encoder was given, provided that both sides use the same probability for each bit. Part 2 shows that the two sides do use the same probabilities and that the decoded steps rebuild $x$.

### 1. The range coder

Write the encoder's state as an interval of real numbers. Start with $I_0 = [0, 1)$. For a bit with probability $p$ (of a 0) on an interval $I = [a, a + r)$ that the encoder holds as $low = a \cdot S$ and $range = r \cdot S$ for the current scale $S$, put $bound = \lfloor range / 2^{11} \rfloor \cdot p$ and
- for bit 0: $I' = [a, a + bound / S)$;
- for bit 1: $I' = [a + bound / S, a + r)$.

A direct bit is the same with $bound = \lfloor range / 2 \rfloor$. Normalization multiplies $S$ by 256 and does not change the interval. Since $0 < bound < range$, each $I'$ is a nonempty part of $I$, and the two choices are disjoint. So the intervals are nested: $I_0 \supseteq I_1 \supseteq \cdots \supseteq I_T$.

*The output is the low end.* The encoder holds $low$ in a register of 33 bits. On each shift it removes the top byte of $low$; it holds that byte, plus the run of FF bytes after it, as pending, because a later addition can carry into them. The carry is the bit $2^{32}$ of $low$: when it is set, the pending bytes are written plus 1 (the held byte plus 1, and each FF as 00), and when $low < \mathrm{FF000000}$ no later carry can reach them, so they are written as they are. In both cases the written bytes, followed by the pending bytes and the register, always form the exact base-256 digits of $a \cdot S'$ for the current interval start $a$ and a fixed overall scale $S'$. The flush shifts 5 times, which moves all of $low$ out. So the whole output, read as one fraction $A = 0.b_0 b_1 b_2 \ldots$ in base 256, equals the final $a_T$, and the first byte $b_0$ is the initial pending byte 0. Since $a_T \in I_T \subseteq I_t$ for every $t$, $A$ lies in every interval of the run.

*The decoder tracks $A - a$.* We show by induction on the number of coded bits that before each bit, the decoder has $range = r \cdot S$ (the same register value as the encoder) and $code = \lfloor (A - a) \cdot S \rfloor$, read from the bytes that it has consumed. At the start, $range = 2^{32} - 1$ on both sides and $code$ is the 4 bytes after $b_0$, which is $\lfloor A \cdot 2^{32} \rfloor$ minus the part in $b_0 = 0$; with $a = 0$ this is the claim. Both sides compute the same $bound$ from the same $range$ and $p$. Because $A \in I'$:

- if the bit was 0, then $A < a + bound / S$, so $code < bound$ and line B2 returns 0;
- if the bit was 1, then $A \ge a + bound / S$, so $code \ge bound$ and line B3 returns 1.

Lines B2 and B3 set $range$ and $code$ as the encoder sets $range$ and $a$, so the claim holds after the bit. Normalization multiplies $range$ by 256 on both sides and appends the next byte of $A$ to $code$, which keeps $code = \lfloor (A - a) S \rfloor$ at the new scale. Lines B2 and B3 update $p$ with the same rule as the encoder. So the decoder returns every bit, and its probabilities stay equal to the encoder's.

*The end.* Let $T$ be the last bit. The encoder flushed $low$, so $A = a_T$ exactly, and the decoder, which has read as many bytes as the encoder wrote, has $code = 0$. So the test $code = 0$ of line L4 holds after the last step. It cannot stop the decoder early in a way that loses bytes, because line L4 also needs $|out| = n$.

### 2. The steps rebuild the input

The encoder codes a sequence of steps $e_1, e_2, \ldots$, each a literal, a match $(\ell, d)$, a short rep, or a rep match $(i, \ell)$. Before each step both sides hold a *context*: the position $|out|$, the bytes $x[0 \ldots |out| - 1]$, the state $s$, the distances $rep0, \ldots, rep3$, and all probabilities.

> **(C)** Before step $j$, the decoder's context equals the encoder's.

*Initialization.* Both start at position 0 with $s = 0$, all repeated distances 0 and all probabilities 1024 (line L2).

*Maintenance.* Every bit of step $j$ uses a probability chosen by the context (IsMatch by $s$ and the position modulo $2^{pb}$; the literal tables by the previous byte, the position modulo $2^{lp}$, and after a match by the byte at distance $rep0 + 1$; the length trees by the position modulo $2^{pb}$; the slot trees by $\min(\ell - 2, 3)$, which is known when the slot is read), and each later bit of the step depends only on the context and the bits before it. By part 1 the decoder reads the same bits, so it identifies the same kind of step and the same values. The encoder writes:

- a literal only as the byte $x[p]$;
- a match only with $x[c \ldots c + \ell - 1] = x[p \ldots p + \ell - 1]$ for $c = p - d - 1 \ge 0$ (the length is the measured common prefix);
- a rep match only with the measured common prefix at distance $rep_i + 1$, of length $\ell \ge 2$;
- a short rep only when $x[p] = x[p - rep0 - 1]$.

Line L15 copies with the distance $rep0 + 1$ byte by byte. By induction on $k$, the $k$-th copied byte is the byte at position $p + k - rep0 - 1 < p + k$, which is $x[p + k - rep0 - 1]$, either from before $p$ or as an earlier copied byte; by the encoder's condition it equals $x[p + k]$. So after the step the decoder's output is $x[0 \ldots p']$ for the encoder's new position $p'$. Lines L6, L8, L11 and L13 update $s$ by the same table as the encoder, and lines L8, L9 and L12 update the distances in the same way. The probabilities are equal by part 1. So (C) holds before step $j + 1$.

*Termination.* The encoder writes no step after position $n$, and the decoder stops at line L4 when $|out| = n$ and $code = 0$, which by part 1 is the case after the last step. The checks of line L14 never fail, since every distance that the encoder uses points into the bytes before $p$. So the decoder returns $x$. If the encoder writes an end marker instead, the header has the unknown size, and line L9 returns $x$ when it reads the distance $2^{32} - 1$. $\square$

### The cost

Every step codes $O(1)$ bits (at most 9 literal bits and a few choice bits, or at most 10 length bits, 6 slot bits and 30 distance bits) and every step adds at least one byte to the output, so the number of bit decodes is $O(n)$. Each bit decode is $O(1)$ work and reads at most one byte: after a bit, $range \ge 2^{13} \cdot 31$, since $31 \le p \le 2017$ always holds under the update rule, so one shift by 8 bits restores $range \ge 2^{24}$. Copies cost one unit per output byte. So the decoder runs in $\Theta(n + m)$ time.
