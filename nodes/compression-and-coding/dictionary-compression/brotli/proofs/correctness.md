---
title: The Brotli decoder inverts the encoder on the page
proves: [correctness]
status: full
---

We use the decoder BROTLI-DECODE-COMMANDS (lines L1 to L12), DISTANCE (lines D1 to D4) and the encoder on the page. Let $x = x[0 \ldots n-1]$.

**Claim.** The stream decoder, given the encoder's stream for $x$, returns $x$.

The encoder writes WBITS for the smallest window $w \ge n$ (or 24), so every distance it uses is at most $w$. The meta-blocks cover $x$ in order and none is last, and the stream ends with the bits ISLAST = 1, ISLASTEMPTY = 1 and zero padding, so the decoder stops there and finds no data after it. In each meta-block header, MLEN − 1 uses the fewest nibbles (at least 4), so if there are more than 4 the top nibble is not 0. An uncompressed meta-block is read back byte for byte. So the claim reduces to compressed meta-blocks, plus the history that they share: the output so far and the ring $rb$.

### 1. The prefix codes come back

The decoder builds the canonical code from a list of code lengths, as the encoder does. So it is enough that it reads back the same lengths.

*Simple codes.* Huffman lengths for 2, 3 or 4 symbols are (1, 1), (1, 2, 2), and (2, 2, 2, 2) or (1, 2, 3, 3). Package-merge with limit 15 gives the optimal lengths, so it gives one of these shapes. The encoder lists the symbols sorted by length and sets the tree-select bit to 1 exactly for (1, 2, 3, 3). The decoder gives the listed symbols the lengths of the shape in order, so every symbol gets its own length. A code with one symbol has length 0 on both sides, and neither side writes or reads bits for it.

*Complex codes.* The encoder cuts the lengths into maximal runs up to the last nonzero length. We need one fact about the run codes.

> **(R)** Let $r \ge 3$ and let $e_1, \ldots, e_k$ be the extra values that the encoder writes for a run of $r$ with $b$ extra bits (2 for code 16, 3 for code 17). The decoder count, $c_1 = e_1 + 3$ and $c_{j+1} = (c_j - 2) \cdot 2^b + e_{j+1} + 3$, ends at $c_k = r$.

*Proof.* By induction on $r$. If $r - 3 < 2^b$, the encoder writes one value $e_1 = r - 3$, and $c_1 = r$. Else it writes $e_k = (r - 3) \bmod 2^b$ last, and before it the values for $r' = \lfloor (r - 3) / 2^b \rfloor + 2$, because its loop goes on with $r' - 3 = \lfloor (r - 3) / 2^b \rfloor - 1$. Here $3 \le r' < r$, so by induction those values end at $c_{k-1} = r'$. Then $c_k = \lfloor (r - 3) / 2^b \rfloor \cdot 2^b + (r - 3) \bmod 2^b + 3 = r$. $\square$

The decoder adds $c_j - c_{j-1}$ lengths at each step, so a run of $k$ codes adds $c_k = r$ lengths in total. The chain rule applies only to the same code twice in a row. Runs are maximal, so two runs in a row have different values. A zero run (code 17) can follow a run of code 16 and the other way around, and those do not chain. A nonzero run whose value differs from the last nonzero length starts with that value as a plain code, which resets the chain. Code 16 repeats the last nonzero length, and both sides start that length at 8 and change it only at a plain nonzero code. So each run comes back with its value and length.

Since the lengths form a complete code, the sum of $2^{15 - \ell}$ over the nonzero lengths reaches $2^{15}$ only with the last nonzero length, so the decoder stops reading exactly after the encoder's last token. The same argument holds for the code length code: its lengths are at most 5 and complete, and the encoder writes them in the order of RFC Section 3.5 up to the last nonzero one, after HSKIP zeros. If only one code length symbol is used, the encoder writes all 18 entries, the sum stays below 32, and both sides use that symbol with 0 bits. The fixed code for the 0 to 5 values is a prefix code, so those values come back. Every prefix code is written from its first bit, which is the bit-reversed code in the low-bit-first stream, and that is what the decoder's table expects.

### 2. The codes of one command

For an insert length $\lambda$ the encoder takes the largest code $c$ with $\mathrm{BASE}[c] \le \lambda$ and writes $\lambda - \mathrm{BASE}[c]$ in $\mathrm{EXTRA}[c]$ bits. In the tables of RFC Section 5, $\mathrm{BASE}[c + 1] = \mathrm{BASE}[c] + 2^{\mathrm{EXTRA}[c]}$, and the last code reaches past $2^{18}$, so the extra value fits. The same holds for the copy length (from 2). The command symbol is $64 g + 8 (i \bmod 8) + (j \bmod 8)$, where $g$ is the cell for the ranges of the insert code $i$ and the copy code $j$. Line L4 reads back $i$ and $j$ from the cell and bits 3 to 5 and 0 to 2.

For a general distance $d$ (NPOSTFIX = NDIRECT = 0), let $v = d + 3 \ge 4$, $b = \lfloor \log_2 v \rfloor - 1 \ge 1$ and $t = \lfloor v / 2^b \rfloor \in \lbrace 2, 3 \rbrace$. The encoder writes code $16 + c$ with $c = 2(b - 1) + (t - 2)$ and the extra value $v \bmod 2^b$ in $b$ bits. Line D3 gives $1 + \lfloor c / 2 \rfloor = b$ extra bits and $h = c$ with $h \bmod 2 = t - 2$. Line D4 gives $(t \cdot 2^b - 4) + (v \bmod 2^b) + 1 = v - 3 = d$. Since $d \le w < 2^{24}$, $b \le 24$ and the code is below 64, the size of the distance alphabet.

### 3. The ring of distances

Both rings start as (16, 15, 11, 4). For a match at distance $d$ the encoder looks at its own ring: if $d$ is the last entry, it uses distance code 0 (or a command symbol below 128, if $i < 8$ and $j < 16$); if $d$ is an older entry, it uses code 1, 2 or 3 for it; else a general code. Lines D1 and L9 then give $d$. The encoder pushes $d$ exactly when it does not use code 0 or a symbol below 128, and the decoder pushes at line L11 under the same condition. The encoder makes no dictionary references. When the encoder falls back to an uncompressed meta-block, it restores its ring, and the decoder does not change its ring in that meta-block. So the two rings agree before every command.

### 4. The commands rebuild the input

With one block type per category, every block count is $2^{24}$, more than a meta-block can use, so no block switch happens. With one tree of each kind, both context maps are all 0, so every literal uses the one literal tree and every distance the one distance tree, whatever the context.

> **(C)** Before each command of a meta-block, the decoder's output is $x[0 \ldots p-1]$, where $p$ is the encoder's position at the start of that command.

At the start of a meta-block, $p$ is its start, and the earlier meta-blocks are in the output by induction. A command (anchor $p$, insert $\lambda$, copy $\ell$, distance $d$) of the greedy parse has $x[q - d + j] = x[q + j]$ for $0 \le j < \ell$, with $q = p + \lambda$, $1 \le d \le \min(w, q)$, and $q + \ell$ at most the end of the meta-block. Lines L5 to L7 append $x[p \ldots q - 1]$, because the literal tree returns each symbol (part 1). If the command is the last one with $\ell = 0$, then $q$ is the end, and line L8 ends the loop. Else $|out| = q < $ end, the distance comes back as $d$ (parts 2 and 3), and $d \le \min(w, |out|)$, so line L11 copies. By induction on $j$, the byte at $q + j - d < q + j$ is $x[q + j - d]$ (either from before $q$ or copied earlier in this match), and this equals $x[q + j]$. So (C) holds with $p' = q + \ell$. When $p'$ reaches the end, line L2 ends the loop.

So every meta-block decodes to its part of $x$, and the stream decodes to $x$. $\square$

### The cost

Each command reads one command symbol, two extra fields, its literals, and at most one distance symbol and one extra field, each in $O(1)$ time; the copy costs $O(\ell)$. Each meta-block header reads and builds a number of trees and context maps that is bounded by constants of the format. Every meta-block with a header adds at least one byte of $m$, so the decoder runs in $\Theta(n + m)$ time.
