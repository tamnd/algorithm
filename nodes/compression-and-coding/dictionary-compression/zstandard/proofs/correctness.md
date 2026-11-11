---
title: The Zstandard decoder inverts the encoder on the page
proves: [correctness]
status: full
---

We use the decoder ZSTD-DECODE-SEQUENCES (lines L1 to L13), RESOLVE-OFFSET (lines R1 to R6) and the encoder on the page. Let $x = x[0 \ldots n-1]$.

**Claim.** The frame decoder, given the encoder's frame for $x$, returns $x$.

The frame header gives the content size $n$ and the window $w = n$, and every block is at most $\min(n, 2^{17})$ bytes, so the size checks pass. An RLE block for a run of $k$ copies of byte $b$ decodes to $b^k$, and a raw block decodes to its own bytes. So the claim reduces to compressed blocks, plus the history that they share. The checksum and the size check at the end pass because the output is $x$, and both sides compute the same XXH64.

### 1. The FSE coder

Fix a table with accuracy log $a$ and size $S = 2^a$. Let symbol $s$ have $c \ge 1$ cells (a count of $-1$ gives one cell). The construction gives these cells the numbers $y = c, c+1, \ldots, 2c - 1$, and the cell with number $y$ gets $k = a - \lfloor \log_2 y \rfloor$ bits and base $B = y \cdot 2^k - S$. Write $J(y) = [y \cdot 2^k, (y+1) \cdot 2^k)$, so that the cell's range is $[B, B + 2^k) = J(y) - S$.

> **(T)** For each symbol $s$, the ranges $[B, B + 2^k)$ of its cells are disjoint and cover $[0, S)$.

*Proof.* Let $2^j$ be the power of two with $c \le 2^j < 2c$. For $y \ge 2^j$, $\lfloor \log_2 y \rfloor = j$ and $k = a - j$. The intervals $J(y)$ for $y = 2^j, \ldots, 2c - 1$ are adjacent and cover $[2^a, 2c \cdot 2^{a-j})$. For $y < 2^j$ (only when $c < 2^j$), $\lfloor \log_2 y \rfloor = j - 1$ and $k = a - j + 1$. Those intervals are adjacent and cover $[c \cdot 2^{a-j+1}, 2^j \cdot 2^{a-j+1}) = [2c \cdot 2^{a-j}, 2^{a+1})$. Together they cover $[S, 2S)$ without overlap. Subtract $S$. $\square$

So for each symbol $s$ and each state $t \in [0, S)$ there is exactly one cell $u$ of $s$ with $t \in [B_u, B_u + 2^{k_u})$. The encoder's table ENC gives this cell.

Now take one of the three codes, say the offset codes $o_1, \ldots, o_N$ of the block's sequences. The encoder picks the states backward: $u_N$ is a cell of $o_N$, and $u_i = \mathrm{ENC}[o_i][u_{i+1}]$ for $i < N$. By (T), cell $u_i$ has symbol $o_i$ and $u_{i+1} - B_{u_i} \in [0, 2^{k_{u_i}})$. It writes $u_1$ in $a$ bits and, for $i < N$, the number $u_{i+1} - B_{u_i}$ in $k_{u_i}$ bits. If the decoder reads these numbers, then line L2 sets the state to $u_1$, and line L11 sets it to $B_{u_i} + (u_{i+1} - B_{u_i}) = u_{i+1}$. By induction on $i$, the state at step $i$ is $u_i$, and lines L4 to L6 read the symbol $o_i$. The same holds for the literal length and match length codes.

### 2. The bit order

The writer appends each field above the bits written before, and the reader of line L1 starts at the top, below the end marker. So the reader meets the fields in the reverse of the write order, and each field comes back whole, low bit at the bottom, with its exact width. The decoder reads in this order: the states L, O, M; then for each $i$: the extra bits O, M, L, and for $i < N$ the updates L, M, O. The encoder writes, for $i = N$ down to 1: for $i < N$ the updates O, M, L; then the extra bits L, M, O; and at the end the states M, O, L. This is the read order reversed, so every READ returns the field that the encoder meant for it, and all bits are read when step $N$ ends. So line L12 does not fail.

*The codes.* For a literal length $\lambda$ the encoder takes the largest code $c$ with $\mathrm{LLBASE}[c] \le \lambda$ and writes $\lambda - \mathrm{LLBASE}[c]$ in $\mathrm{LLBITS}[c]$ bits. In RFC Table 16, $\mathrm{LLBASE}[c + 1] = \mathrm{LLBASE}[c] + 2^{\mathrm{LLBITS}[c]}$, so the extra value fits. The last code covers up to 131071, and a block has at most $2^{17}$ bytes, so a code always exists. The same holds for match lengths (Table 17, up to 131074). For an offset value $v$ the code is $c = \lfloor \log_2 v \rfloor$ with extra $v - 2^c < 2^c$. Distances are below $2^{22}$, so $c \le 22$, and every code used has a cell in the predefined tables. So lines L4 to L6 give back $\lambda_i$, $\ell_i$ and $v_i$.

### 3. The steps rebuild the input

The repeat history $rep$ starts at (1, 4, 8) on both sides. The encoder chooses $v$ for distance $d$ by running RESOLVE-OFFSET on its own copy of $rep$ and checks that the result is $d$. The decoder runs the same function on the same $v$, $\lambda$ and $rep$ at line L7, so it gets the same $d$ and the same new $rep$. The encoder restores $rep$ when it writes a raw block, and the decoder changes $rep$ only in compressed blocks. So the two copies agree before every block, and by induction before every sequence.

> **(C)** Before sequence $i$ of a block, the decoder's output is $x[0 \ldots p-1]$, where $p$ is the encoder's position at that sequence's first literal, and the literals not yet used are the encoder's literals from that point on.

At the start of a block, $p$ is the block start, and the earlier blocks are in the output by induction on blocks. In sequence $i$, the encoder put the $\lambda_i$ bytes $x[p \ldots p + \lambda_i - 1]$ into the literals, so line L8 appends them. Then it took a match of $\ell_i$ bytes at distance $d_i$ with $x[q - d_i + j] = x[q + j]$ for $0 \le j < \ell_i$, where $q = p + \lambda_i$ and $1 \le d_i \le q$. So line L9 passes, as the frame output so far has $q$ bytes. Line L10 appends, by induction on $j$, the byte at position $q + j - d_i < q + j$, which is $x[q + j - d_i]$ (either from before $q$ or copied earlier in this match), and this equals $x[q + j]$. So (C) holds before sequence $i + 1$ with $p' = q + \ell_i$. After the last sequence, the literals left are the bytes from the last match end to the block end, and line L13 appends them. A block with $N = 0$ has all its bytes as literals, and the decoder appends them.

So every block decodes to its part of $x$, and the frame decodes to $x$. $\square$

### The cost

Each sequence costs $O(1)$ reads of at most 31 bits plus its literal and match bytes. Each block builds at most four tables of at most $2^{11}$ cells, and each table costs time linear in its size. A Huffman symbol costs one lookup. Since every block adds at least one byte of $m$ (its header) and the sizes are constants of the format, the decoder runs in $\Theta(n + m)$ time.
