---
title: The LZX decoder inverts the encoder on the page
proves: [correctness]
status: full
---

We use the decoder LZX-TOKENS (lines L1 to L16), the stream decoder and E8-REVERSE (lines E1 to E6) of the page, and the encoder on the page. Let $x = x[0 \ldots n-1]$ with $n \ge 1$ (for $n = 0$ both sides give the empty string), let $w = 2^b$ be the window and $t$ the translation size ($0 \le t < 2^{31}$).

**Claim.** Given the encoder's stream for $x$, with $b$ and $n$, the decoder returns $x$.

Let $y$ be $x$ after the forward E8 translation (or $y = x$ if $t = 0$). The encoder writes the E8 bit and, if $t > 0$, $t$ in 32 bits. Then it writes one block per frame $[s, e)$ of $y$, with $e - s$ in the block size, and pads to the next word after each frame. Parts 1 to 5 show that the decoder rebuilds $y$. Part 6 shows that E8-REVERSE turns $y$ into $x$.

### 1. Bits, padding and raw bytes

The writer packs bits into 16-bit words from the high bit down and stores each word low byte first. The reader loads a word only when it needs a bit and has none left, and reads from the high bit down. So the reader returns the bits in the order that they were written. At any point in the stream, if the writer has $k$ bits in its open word, the reader has $16 - k$ bits left in its current word when $k > 0$, and none when $k = 0$.

At the end of a frame the writer adds $16 - k$ zero bits if $k > 0$. The reader drops its $16 - k$ bits, which are those zeros, so the check for zero padding passes. For an uncompressed block the writer adds $16 - k$ zero bits, which is 16 when $k = 0$. The reader loads a word if it has no bits left and then drops the rest, so it drops the same 1 to 16 bits. After that both sides are at the same byte, the 12 bytes of R0, R1, R2 and the raw bytes follow, and the writer adds a zero byte if $e - s$ is odd. The reader skips that byte when it reads the next block header, or at the end of the stream. So after the last frame the reader has read exactly the stream, and the check for data after the end passes.

### 2. Tree lengths come back

Both sides keep the old lengths of the main tree and the length tree. Both start at 0. The encoder replaces them by the new lengths only when it writes a verbatim or aligned offset block, and the decoder writes the new lengths over the old ones only in such a block. So the old lengths agree before every block. Let $\mathit{old}$ and $\mathit{new}$ be the lengths of one part, from index $a$ to $c$.

The encoder cuts $\mathit{new}[a \ldots c-1]$ into tokens from left to right. Let $v = \mathit{new}[x]$ and let $r$ be the length of the run of $v$ from $x$, inside the part.

- If $v = 0$ and $r \ge 20$, it writes 18 with $k - 20$ in 5 bits, $k = \min(r, 51)$, so $0 \le k - 20 \le 31$. The decoder sets $k$ lengths to 0.
- If $v = 0$ and $4 \le r \le 19$, it writes 17 with $r - 4$ in 4 bits. The decoder sets $r$ lengths to 0.
- If $v > 0$ and $r \ge 4$, it writes 19, $k - 4$ in 1 bit with $k = \min(r, 5)$, and the symbol $z = (\mathit{old}[x] - v) \bmod 17$. The decoder has not yet changed $\mathit{lens}[x]$, so it computes $(\mathit{old}[x] - z) \bmod 17 = v$, because $0 \le v \le 16$, and sets $k$ lengths to $v$.
- Else it writes $z = (\mathit{old}[x] - v) \bmod 17 \le 16$, and the decoder sets one length to $(\mathit{old}[x] - z) \bmod 17 = v$.

Every token covers only positions of its run, so no run passes $c$, and the decoder ends exactly at $c$. By induction on the tokens, the decoder's lengths of the part equal $\mathit{new}$. The pretree for the tokens has at least two symbols and lengths at most 15, so its 20 lengths fit in 4 bits each, and by part 3 every pretree symbol comes back.

### 3. Every symbol comes back

The encoder takes package-merge lengths for at least two used symbols, which form a complete code, or gives one used symbol a partner, so that both have length 1, which is also complete. The main tree is never empty, because a frame has at least one token. The length tree is empty only if no token has a length symbol. The aligned offset tree always has two or more symbols, with lengths at most 7, so they fit in 3 bits. The decoder accepts all these trees: they are complete, or the length tree is empty.

Both sides build the canonical code from the same lengths: codes of one length are consecutive, in the order of the symbols, and the first code of length $\ell + 1$ is twice the code after the last code of length $\ell$. The decoder reads one bit at a time and returns the symbol whose code it has read, so it returns the symbol that the encoder wrote. It reads the length tree only at line L6 with $h = 7$, which means $\ell \ge 9$, so the encoder used a length symbol and the tree is not empty.

### 4. The fields of one match

Take a match of length $\ell \in [2, 257]$ with formatted offset $f$. The main symbol is $256 + 8p + h$ with $h = \min(\ell - 2, 7)$, so line L5 gives back $h$ and $p$. If $h < 7$, line L6 gives $\ell = h + 2$. Else the length symbol is $\ell - 9 \in [0, 248]$, and line L6 gives $7 + 2 + (\ell - 9) = \ell$.

If $f < 3$, then $p = f$, there is no footer, and line L7 handles it (part 5). Else $p$ is the largest slot with $B_p \le f$, and the footer is $f - B_p < 2^{e_p}$, since $B_{p+1} = B_p + 2^{e_p}$. The slot exists: $f = d + 2 \le (w - 3) + 2 = w - 1$, and the slots of window $w$ end at $B_s = w$. Line L11 reads the footer in $e_p$ bits. In an aligned offset block with $e_p \ge 3$, that is $p \ge 8$, the encoder writes $\lfloor \mathrm{footer} / 8 \rfloor$ in $e_p - 3$ bits and $\mathrm{footer} \bmod 8$ with the aligned offset tree. Since $B_8 = 16$ and every later step $2^{e_p}$ is a multiple of 8, $B_p$ is a multiple of 8, and line L10 gives $8 \lfloor \mathrm{footer} / 8 \rfloor + (\mathrm{footer} \bmod 8) = \mathrm{footer}$. Line L12 gives $d = B_p + \mathrm{footer} - 2 = f - 2$, the new offset.

### 5. The three offsets agree

Both lists start as (1, 1, 1). For a match at offset $d$, the encoder uses $f = 0$ if $d = R_0$; else $f = 1$ and swaps $R_0$ and $R_1$ if $d = R_1$; else $f = 2$ and swaps $R_0$ and $R_2$ if $d = R_2$; else $f = d + 2$ and sets $R \leftarrow (d, R_0, R_1)$. Line L7 returns $R[f]$, which is $d$, and makes the same swap. Line L12 pushes $d$ in the same way. So both lists agree after each match, if they agreed before it. When the encoder writes an uncompressed block, it first restores its list to the value from before the frame, and writes those three numbers; by induction they are the decoder's list, so the decoder's list does not change.

### 6. The tokens rebuild $y$, and the E8 pass gives $x$

> **(C)** Before each token, the decoder's output is $y[0 \ldots q - 1]$, where $q$ is the encoder's position at the start of that token.

A literal is appended at line L3 (part 3). For a match at $q$ with length $\ell$ and offset $d$, the parse has $y[q - d + j] = y[q + j]$ for $0 \le j < \ell$, $1 \le d \le \min(q, w - 3)$ and $q + \ell \le e$, the end of the block and of the frame. So line L13 passes, with $\mathit{left} = e - q$ and $\mathit{end} = e$. By induction on $j$, the byte at $q + j - d < q + j$ is $y[q + j - d]$ (from before $q$, or copied earlier in this match), which equals $y[q + j]$. So (C) holds with $q + \ell$. When $q$ reaches $e$, both $\mathit{left}$ and the frame end, line L1 stops, the decoder drops the padding (part 1), and the next block header follows. An uncompressed block copies $y[s \ldots e - 1]$ directly. So after the last frame, the output is $y$.

The encoder translates each frame that starts below $2^{30}$, and the decoder undoes the same frames. Within one frame, a step at position $i$ changes only the bytes $i + 1$ to $i + 4$ and then moves to $i + 5$. So the byte at every position that a scan looks at is the same in $x$ and in $y$, and by induction on $i$, the forward scan and E8-REVERSE visit the same positions. At such a position, with $c$ the position in the stream, the forward step maps a 4-byte value $v \in [-c, t - c)$ to $v + c \in [0, t)$, maps $v \in [t - c, t)$ to $v - t \in [-c, 0)$, and leaves every other value, which lies outside $[-c, t)$, unchanged. Since $c < 2^{30}$ and $t < 2^{31}$, all these values fit in 32 signed bits. Line E5 maps $u \in [0, t)$ to $u - c$ and $u \in [-c, 0)$ to $u + t$, which are the inverse maps, and leaves the rest. So E8-REVERSE gives back $x$. $\square$

### The cost

Each token reads at most three symbols of at most 16 bits and at most 17 raw bits, and writes its bytes once. Each block header reads a number of lengths bounded by the format (at most $656 + 249$ and three pretrees of 20), and a header of a verbatim or aligned offset block takes at least 267 bits. The E8 pass reads each byte once. So the decoder runs in $\Theta(n + m)$ time.
