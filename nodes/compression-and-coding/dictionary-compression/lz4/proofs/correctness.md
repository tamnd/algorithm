---
title: LZ4-DECODE-BLOCK inverts the greedy LZ4 encoder, in linear time
proves: [correctness]
status: full
---

We use the decoder LZ4-DECODE-BLOCK (lines L1 to L12) and the three steps of the encoder on the page. Let $x = x[0 \ldots n-1]$, and let $h$ be the history (empty for an independent block). Write $y = h \cdot x$ and $b = |h|$, so position $p$ of the block is position $b + p$ of $y$.

**Claim.** LZ4-DECODE-BLOCK(ENCODE($x$, $h$), $h$) $= x$ for each byte string $x$ and each history $h$, and the output of ENCODE keeps the three end-of-block rules.

### 1. The sequences describe the input

Say that a list of pairs (literals, match) *describes* $z$ from $h$ if the rule "append the literals; then append, $\ell$ times, the byte at distance $off$ from the end" builds $h \cdot z$ from $h$. The encoder keeps a position $p$ and the start $a \le p$ of the pending literals.

> **(E)** At the top of each step, the sequences written so far describe $x[0 \ldots a-1]$ from $h$, and $a \le p$.

*Initialization.* $a = p = 0$ and no sequence is written.

*Maintenance.* If the step writes nothing, only $p$ grows, so (E) holds. Else the table held a position $c$ with $y[c \ldots c+3] = y[b+p \ldots b+p+3]$, because the table key is the 4-byte string itself, and $1 \le b + p - c \le 65535$. The extension gives $\ell \ge 4$ with $y[c + i] = y[b + p + i]$ for $0 \le i < \ell$. The encoder writes the literals $x[a \ldots p-1]$ and the match with $off = b + p - c$. After the literals, the output is $h \cdot x[0 \ldots p-1]$. The match then appends bytes $e_0, \ldots, e_{\ell-1}$, where $e_i$ is the byte at position $b + p + i - off = c + i$ of the output. By induction on $i$: position $c + i$ is below $b + p + i$, so it holds $y[c+i]$, either because it was there before the match or because it is $e_j = y[c + j] = y[b + p + j]$ for an earlier $j$ with $c + i = b + p + j$. So $e_i = y[c + i] = x[p + i]$, and after the match the sequences describe $x[0 \ldots p + \ell - 1]$. The encoder sets $a = p = p + \ell$.

*Termination.* Each step moves $p$ forward by at least 1, so the loop ends. The last sequence has the literals $x[a \ldots n-1]$ and no match, and with (E) the whole list describes $x$ from $h$.

### 2. The end rules hold

A match starts at $p \le n - 12$ by the loop bound, so rule 3 holds. The extension stops at $n - 5$, so each match ends at or before $n - 5$; the next match starts after it, and the last sequence holds all bytes from the end of the last match, which are at least the last 5 bytes. So rules 1 and 2 hold. If $n < 13$ there is no position $p \le n - 12$ with $p \ge 1$ when $h$ is empty, so the block is one literal sequence.

### 3. The decoder reads back the sequences

A sequence with $L$ literals and a match of length $\ell$ is written as the token $16 \min(L, 15) + \min(\ell - 4, 15)$, then, if $L \ge 15$, the value $L - 15$ as $\lfloor (L-15)/255 \rfloor$ bytes 255 and one byte $(L - 15) \bmod 255$; then the literals, the offset in 2 little-endian bytes, and the extra bytes for $\ell - 4 - 15$ in the same way. A byte below 255 ends a length, and each byte of 255 is followed by another, so line L4 reads back $L$ and line L9 reads back $\ell - 4$. The last sequence is written with its literals only. Every sequence but the last has at least 2 bytes (the offset) after its literals, so line L6 stops exactly after the last sequence. The offset satisfies $1 \le off \le b + p$ and $b + p$ is the output length when the match is read, so line L8 does not fail, and line L11 applies the rule of part 1. Line L12 removes $h$. By part 1 the result is $x$. $\square$

### The cost

Each pass of the loop of line L2 reads at least one byte of $s$ (the token), and its other work is $O(1)$ plus the bytes it reads and appends, so the decoder runs in $\Theta(n + m)$ time for $m = |s|$. The encoder does $O(1)$ expected work per lookup and $O(\ell)$ per match of length $\ell$ (comparisons and $\ell - 1$ table inserts), so it runs in $O(n)$ expected time.
