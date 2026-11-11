---
title: SNAPPY-DECODE inverts the Snappy encoder, in linear time
proves: [correctness]
status: full
---

We use the decoder SNAPPY-DECODE (lines L1 to L15) and the four steps of the encoder on the page. Let $x = x[0 \ldots n-1]$ with $n < 2^{32}$.

**Claim.** SNAPPY-DECODE(ENCODE($x$)) $= x$ for each byte string $x$.

### 1. The elements describe the input

The encoder works on blocks $x[b \ldots e-1]$ of at most 65536 bytes, in order. Inside a block it keeps a position $p$ and the start $q \le p$ of the pending literal.

> **(E)** At the top of each step of the block loop, the elements written so far, followed by the literal $x[q \ldots p-1]$, describe $x[0 \ldots p-1]$.

Here an element list *describes* $y$ if the rule "a literal appends its bytes; a copy $(off, \ell)$ appends, $\ell$ times, the byte at distance $off$ from the end" builds $y$ from the empty string.

*Initialization.* At the start of a block, $q = p = b$, and by (E) for the previous block (or the empty list for $b = 0$) the elements describe $x[0 \ldots b-1]$.

*Maintenance.* A failed lookup moves $p$ forward and leaves $q$, so the pending literal grows by the passed bytes and (E) still holds. On a hit at a candidate $c < p$ in the same block, the match length $\ell \ge 4$ is the length of the common prefix of $x[c \ldots e-1]$ and $x[p \ldots e-1]$: the hash table stores the position of a 4-byte string as its key, so $x[c \ldots c+3] = x[p \ldots p+3]$, and the extension keeps $x[c + i] = x[p + i]$ for $0 \le i < \ell$. The encoder writes the pending literal (if $q < p$), then the copy with $off = p - c$, cut into pieces. Each piece copies from distance $off$, so after the pieces the rule has appended $\ell$ bytes $e_0, \ldots, e_{\ell - 1}$ with $e_i$ equal to the byte at position $p + i - off = c + i$. By induction on $i$: position $c + i$ is below $p + i$, so it holds $x[c + i]$, either by (E) or as an earlier byte of this copy. So $e_i = x[c + i] = x[p + i]$. Then $p$ and $q$ move to $p + \ell$, and (E) holds.

*Termination.* Each step moves $p$ forward by at least 1, so the loop ends; the encoder then writes the last literal $x[q \ldots e-1]$, and the elements describe $x[0 \ldots e-1]$. After the last block they describe $x$.

The pieces of a long copy are valid elements: the rule of step 4 writes pieces of 64 while at least 68 bytes are left, then one of 60 if more than 64 are left, so the last piece has between 4 and 64 bytes and each earlier piece 60 or 64. A piece is element 01 only when $4 \le \ell \le 11$ and $off < 2048$, which are the ranges of that element; else it is element 10, which holds $1 \le \ell \le 64$ and $off < 65536$, and $off < 65536$ holds because $c$ and $p$ are in one block of 65536 bytes.

### 2. The decoder reads back the elements

The encoder writes the preamble $n$ as a varint, which READ-VARINT reads back, since each 7-bit group is written with the continuation bit set exactly when more groups follow. The kind of each element is the low two bits of its tag. For each kind, the number of bytes after the tag is a function of the tag alone (for a literal, of the tag and the length bytes), and lines L6 to L11 read the fields in the positions where the encoder wrote them:

- a literal with $\ell - 1 < 60$ stores $\ell - 1$ in bits 7 to 2; else bits 7 to 2 hold $59 + k$, where $k$ is the number of length bytes, and line L7 reads $\lfloor tag/4 \rfloor - 59 = k$ bytes;
- element 01 stores $\ell - 4$ in bits 4 to 2 and bits 10 to 8 of the offset in bits 7 to 5, which line L10 reads as $(\lfloor tag/4 \rfloor \bmod 8)$ and $\lfloor tag / 32 \rfloor$;
- element 10 stores $\ell - 1$ in bits 7 to 2 and the offset in 2 little-endian bytes, as line L11 reads.

So the decoder sees the same element list, in order. Each copy has $1 \le off \le p$ where $p$ is the output length at that time, so line L12 never fails, and line L13 applies the rule of part 1. By part 1 the output is $x$, its length is $n$, and line L14 passes. $\square$

### The cost

Each pass of the loop of line L3 reads at least one byte of $s$ (the tag), and its other work is $O(1)$ plus the number of bytes that it reads and appends. So the decoder runs in $\Theta(n + m)$ time for $m = |s|$. The encoder does $O(1)$ work per lookup plus $O(\ell)$ per match of length $\ell$ (the extension by comparisons of at most $\ell + 1$ bytes, and $\ell - 1$ table inserts), so with $O(1)$ expected time per hash table operation it runs in $O(n)$ expected time.
