---
title: Byte-wise rANS keeps each state in [L, 256L), the decoder undoes each step, and the output is within 64 bits plus a tiny loss per symbol of the ideal length
proves: [correctness, termination, length]
status: full
---

Notation. $M = 2^{12}$, $L = 2^{23}$, $I = [L, 256L)$. The frequencies $f_s \ge 1$ of the symbols that occur sum to $M$, and $c_s = \sum_{t < s} f_t$. For a symbol $s$ let $I_s = [2^{11} f_s, 2^{19} f_s)$; note $2^{11} = L/M$ and $2^{19} = 256 L/M$. ENCODE-PUT is lines L1 to L3 and DECODE-GET is lines L4 to L8. Write $C(s, x) = \lfloor x/f_s \rfloor M + c_s + (x \bmod f_s)$ for line L3.

**Lemma 1 (the interval).** If $x \in I$, then the loop of line L2 stops with $x \in I_s$, and line L3 returns a state in $I$.

*Proof.* Line L1 sets $x_{\max} = 2^{19} f_s$. The loop divides $x$ by 256 while $x \ge x_{\max}$, so it stops, and then $x < 2^{19} f_s$. If it made no step, $x \ge L = 2^{23} \ge 2^{11} f_s$, because $f_s \le M = 2^{12}$. If it made a step, the last step started from a value at least $2^{19} f_s$, so it ended at a value at least $2^{11} f_s$. So $x \in I_s$, and $\lfloor x / f_s \rfloor \in [2^{11}, 2^{19})$. The two other terms of $C(s, x)$ are at least 0 and at most $c_s + f_s - 1 < M$, so $C(s, x) \in [2^{11} M, 2^{19} M) = [L, 256 L)$. $\square$

**Lemma 2 (one step back).** Let $x \in I$, let ENCODE-PUT emit the bytes $b_1, \ldots, b_k$ in this order and return $y$. If DECODE-GET starts from $y$ and its next input bytes are $b_k, b_{k-1}, \ldots, b_1$, then it returns $(s, x)$ and reads exactly these $k$ bytes.

*Proof.* Let $x_0 = x$ and $x_j = \lfloor x_{j-1} / 256 \rfloor$, so $x_{j-1} = 256 x_j + b_j$ and the loop stops at $x_k \in I_s$ by Lemma 1. Line L4 gives $slot = y \bmod M = c_s + (x_k \bmod f_s)$, because $c_s + (x_k \bmod f_s) < c_s + f_s \le M$. This lies in $[c_s, c_s + f_s)$, so line L5 finds $s$, since these ranges of the symbols do not overlap. Also $\lfloor y / M \rfloor = \lfloor x_k / f_s \rfloor$, so line L6 gives $f_s \lfloor x_k / f_s \rfloor + (x_k \bmod f_s) = x_k$. Now the loop of line L7. For $1 \le j \le k$, $x_j \le x_0 / 256 < L$, so the decoder reads a byte at each of these values, and it gets $256 x_j + b_j = x_{j-1}$. At $x_0 \in I$ it stops, because $x_0 \ge L$. If $k = 0$, then $x_k = x_0 \ge L$ and the loop does not run. $\square$

**Theorem 1 (correctness).** For each input $d_0 \ldots d_{n-1}$ whose symbols all have $f_s \ge 1$, DECODE returns $d_0 \ldots d_{n-1}$, reads the whole stream, and ends with both states equal to $L$.

*Proof.* The encoder performs, in this order, PUT for $i = n - 1, \ldots, 0$ on state $i \bmod 2$, then the flush of state 1 and the flush of state 0. Each operation appends bytes to the list $rev$, and the stream is $rev$ reversed. So the stream is the bytes of the flush of state 0, then those of the flush of state 1, then those of PUT for $i = 0$, then for $i = 1$, and so on, each group with its bytes in reverse order of writing. The decoder performs the mirror operations in this same order: line L12 reads state 0 and then state 1, and line L13 runs DECODE-GET for $i = 0, 1, \ldots$. We show by induction over the decoder's operations that each one reads exactly the bytes of its group and that each state of the decoder equals the encoder's state just after the mirror operation. The flush writes the four bytes of a state from the top byte down, so line L12 reads them back as the same 32-bit value. For a PUT, the decoder state equals the encoder state $y$ just after it, and Lemma 2 gives the symbol $d_i$ and the state $x$ just before it, after reading exactly its $k$ bytes. Each state starts at $L$ in the encoder (line L9), so at the end both decoder states are $L$, and all bytes are read. By Lemma 1 all states are in $I$, so the hypothesis $x \in I$ of Lemma 2 holds. $\square$

**Theorem 2 (length).** The output has at most $\sum_{i} \lg(M / f_{d_i}) + n \lg(1 + 2^{-11}) + 64$ bits.

*Proof.* Follow $\lg x$ for each state. Emitting a byte replaces $x$ by $\lfloor x/256 \rfloor \le x/256$, so it lowers $\lg x$ by at least 8. Line L3 starts from $x \in I_s$, so with $x = a f_s + r$, $0 \le r < f_s$,
$$C(s, x) < (a + 1) M \le \frac{x + f_s}{f_s} M = \frac{M}{f_s}\, x \left(1 + \frac{f_s}{x}\right) \le \frac{M}{f_s}\, x\, (1 + 2^{-11}),$$
because $x \ge 2^{11} f_s$. So line L3 raises $\lg x$ by at most $\lg(M/f_s) + \lg(1 + 2^{-11})$. Each state starts at $L$ and ends at least at $L$, so for each state the total rise is at least the total fall. With $B$ bytes emitted by the PUTs, $8B$ is at most the total fall, so $8B \le \sum_i \lg(M/f_{d_i}) + n \lg(1 + 2^{-11})$. The flush adds 32 bits per state. $\square$

**Termination.** A step of the loop of line L2 needs $x \ge 2^{19} f_s \ge 2^{19}$ and divides $x$ by 256. Since $x < 2^{31}$, two steps bring $x$ below $2^{15}$, so each PUT makes at most 2 steps. Each DECODE-GET reads a byte only while $x < L$, and each read multiplies $x$ by 256. So both sides do $O(1)$ work per symbol. $\blacksquare$
