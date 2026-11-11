---
title: The LZO1X decoder inverts the encoder on the page
proves: [correctness]
status: full
---

We use the decoder LZO1X-DECODE (lines L1 to L14) and the encoder of the page, in version 0 or version 1. Let $x = x[0 \ldots n-1]$ and let $D$ be the distance limit: 49151 in version 0 and 49150 in version 1.

**Claim.** For every $x$ and both versions, LZO1X-DECODE returns $x$ for the encoder's stream.

The encoder cuts $x$ into *items*: literal runs, matches (a length $\ell \ge 4$ and a distance $d$ with $1 \le d \le D$ and $x[p - d + j] = x[p + j]$ for $0 \le j < \ell$, where $p$ is the start of the match) and, in version 1 only, zero runs of 4 to 2051 zero bytes at a position $p > 0$. Two literal runs are never next to each other, since the encoder writes the pending literals only before a match, a zero run or the end marker. If $n > 0$, the first item is a literal run: a match needs an earlier position in the table, and a zero run needs $p > 0$.

### 1. Lengths

The encoder writes a value $u \ge 1$ in a LEN extension as follows: while $u > 255$ it writes a zero byte and subtracts 255, then it writes $u$. So it writes $z = \lceil u/255 \rceil - 1$ zero bytes and a byte $c = u - 255 z \in [1, 255]$. The decoder reads zero bytes until it finds a byte that is not zero, so it reads the same $z$ and $c$ and returns $2^b - 1 + 255 z + c = 2^b - 1 + u$. With a zero low field, LEN$(t, b) = 2^b - 1 + u$.

### 2. The start of the stream

In version 1 the encoder writes 17 and 1, and the stream has at least these 2 bytes and the 3 bytes of the end marker, so line L1 reads $v = 1$. In version 0 with $n = 0$ the stream is 11 00 00, which has 3 bytes, so line L1 sets $v = 0$. In version 0 with $n > 0$ the first item is a literal run of $t$ bytes, and its first byte is $17 + t \ge 18$ if $t \le 238$, or 0. So it is not 17, and line L1 sets $v = 0$. In all cases $v$ is the version of the encoder.

If the first literal run has $t \le 238$ bytes, the first byte is $17 + t$, and the first byte rule copies $t$ bytes and sets the state to $t$ if $t < 4$, or else 4. If $t > 238$, the encoder writes 0 and a LEN extension of $u = t - 18$. The state is 0, so lines L4 and L5 read $3 + 15 + u = t$ and copy $t$ bytes.

### 3. The invariant

Let $q$ be the position of the encoder at the start of an item, after the first literal run if the stream starts with one.

> **(I)** When the decoder is at line L3 and the encoder's next item starts at $q$, the decoder has read exactly the bytes that the encoder wrote for the items before, its output is $x[0 \ldots q-1]$, and its state is: 4 if the last item was a literal run of 4 bytes or more; $t \in \lbrace 1, 2, 3 \rbrace$ if the last item was a first literal run of $t$ bytes, or a match or zero run with a short literal run of $t$ bytes after it; and 0 otherwise (no item yet, or a match or zero run with no literal run after it).

A literal run of 1 to 3 bytes after a match or zero run is not a separate instruction: the encoder writes its length into the $S$ bits of the instruction before it. Those two bits are 0 when the instruction is written: the M2 byte is $32(\ell - 1) + 4(e \bmod 8)$, the low byte of the LE16 of M3 and M4 is $4 e \bmod 256$, and the second byte of a zero run is FC. The encoder sets them once, before it writes the next instruction. Below, "the item" means a match or zero run together with such a short run after it.

Part 2 shows that (I) holds after the first literal run, or at the start if there is none.

### 4. A literal run of 4 bytes or more

It follows a match or zero run whose $S$ bits stay 0, so by (I) the state is 0 (at the start there is no earlier item, and part 2 covered it). If $t \le 18$, the encoder writes $t - 3 \in [1, 15]$, and line L5 reads $3 + (t - 3) = t$. If $t \ge 19$, it writes 0 and a LEN extension of $u = t - 18$, and line L5 reads $3 + 15 + u = t$ (part 1). Line L5 copies $t$ bytes and sets the state to 4, so (I) holds after the run.

### 5. A match

Let the match have length $\ell \ge 4$ and distance $d$, and let $S \in [0, 3]$ be the length of a short literal run after it, or 0. Every byte that the encoder writes for a match is 16 or more, so lines L4, L6 and L7 do not apply, whatever the state.

- **M2** ($\ell \le 8$, $d \le 2048$). Let $e = d - 1 \in [0, 2047]$. The byte $t = 32(\ell - 1) + 4(e \bmod 8) + S$ is at least $32 \cdot 3 = 96$, so line L8 applies. It gives $\lfloor t/32 \rfloor + 1 = \ell$, $d = 1 + (e \bmod 8) + 8 \lfloor e/8 \rfloor = 1 + e$ (the next byte is $\lfloor e/8 \rfloor \le 255$) and $t \bmod 4 = S$.
- **M3** ($d \le 16384$, and not M2). Let $e = d - 1 \in [0, 16383]$. The byte is $32 + (\ell - 2)$ if $\ell \le 33$, which is in $[34, 63]$ with a nonzero low field, or 32 with a LEN extension of $u = \ell - 33$. Line L9 applies and gives $2 + (\ell - 2) = \ell$, or $2 + 31 + u = \ell$. The two bytes after it are $4 e \bmod 256 + S$ and $\lfloor e/64 \rfloor$, so $w = 4 e + S$, since $4 e < 2^{16}$. So $d = 1 + \lfloor w/4 \rfloor = 1 + e$ and $w \bmod 4 = S$.
- **M4** ($16384 < d \le D$). Let $e = d - 16384 \in [1, 32767]$, and let $h \in \lbrace 0, 1 \rbrace$ be bit 14 of $e$. The byte is $16 + 8h + (\ell - 2)$ if $\ell \le 9$, or $16 + 8h$ with a LEN extension of $u = \ell - 9$. The two bytes after it are $4 e \bmod 256 + S$ and $\lfloor e/64 \rfloor \bmod 256$, so $w = 4 (e \bmod 16384) + S$. If line L11 applies, it gives $\ell$ by part 1, and $2048 \cdot 8h + \lfloor w/4 \rfloor = 16384 h + (e \bmod 16384) = e \ne 0$, so line L12 does not end the stream and sets $d = e + 16384$.

It remains to show that line L10 does not apply to an M4 match in version 1 (in version 0, $v = 0$). Line L10 needs $\lfloor t/8 \rfloor = 3$, which means $h = 1$, and needs the two bytes after $t$ to form a word $w'$ with $\lfloor w'/4 \rfloor = 16383$, that is, a first byte of 252 or more and a second byte of 255.

- If $\ell \le 9$, these bytes are $w$, and $\lfloor w/4 \rfloor = e \bmod 16384 = 16383$ with $h = 1$ gives $e = 32767$ and $d = 49151 > D$. This is not possible.
- If $\ell > 9$ and the extension starts with a zero byte, the first byte is 0. This is not possible.
- Else the extension is one byte $c = \ell - 9 \in [1, 255]$, followed by the low byte $4 (e \bmod 64) + S$ of $w$. The test needs $c \ge 252$, so $261 \le \ell \le 264$, and $4 (e \bmod 64) + S = 255$, so $e \bmod 64 = 63$. With $h = 1$ this means $e \text{ AND } 4003F_{16} = 4003F_{16}$. The encoder cuts exactly such a match to $\ell = 260$, which is still a match. This is not possible.

So the decoder gets $\ell$, $d$ and $S$ of the match. Now $d \le p = q$, since the earlier position $p - d$ is at least 0, so line L13 passes, with $|out| = q$ by (I). By induction on $j$, the byte that line L13 appends in step $j$ is $out[q + j - d]$, which is $x[q + j - d]$, because $q + j - d < q + j$ is either before $q$ or was appended earlier in this match. That byte equals $x[q + j]$. Then line L14 copies the $S$ literal bytes $x[q + \ell \ldots q + \ell + S - 1]$, which the encoder wrote after the instruction, and sets the state to $S$. So (I) holds after the item: the state is $S$, which is 0 if no short run follows.

### 6. A zero run (version 1)

Let the run have $r + 4$ zero bytes, $0 \le r \le 2047$. The encoder writes $t = 18_{16} + (r \bmod 8) \in [24, 31]$, then FC + $S$, FF and $\lfloor r/8 \rfloor \le 255$. Lines L4 to L9 do not apply, since $16 \le t < 32$. Line L10 applies: $v = 1$, $\lfloor t/8 \rfloor = 3$, and $w = \mathrm{FFFC}_{16} + S$ gives $\lfloor w/4 \rfloor = 16383$. It appends $8 \lfloor r/8 \rfloor + (r \bmod 8) + 4 = r + 4$ zero bytes, which are $x[q \ldots q + r + 3]$. Then line L14 copies the $S$ literal bytes and sets the state to $S$. So (I) holds after the item.

### 7. The end

After the last item, the encoder writes 11 00 00 (any last literals were written before it, by part 4 or into the $S$ bits). The byte $t = 11_{16} = 17$ is not below 16 and not 32 or more, and $\lfloor t/8 \rfloor = 2 \ne 3$, so line L11 applies. Its low field is 1, so $\ell = 3$, and $w = 0$ and $t \text{ AND } 8 = 0$ give $d = 0$. These are the last 3 bytes of the stream, so line L12 returns the output, which by (I) is $x[0 \ldots n-1] = x$. $\square$

### The cost

Each instruction reads at least one byte of the stream, does $O(1)$ work besides that, and appends each output byte once. A LEN extension reads one byte per zero byte. So the decoder reads each of the $m$ stream bytes once and writes each of the $n$ output bytes once, in $\Theta(n + m)$ time, with $O(1)$ memory besides the output.
