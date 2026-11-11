---
title: LZSS decoding inverts LZSS encoding, and the output has at most 9n bits plus padding
proves: [correctness]
status: full
---

Fix the field widths $b_d \ge 0$ and $b_\ell \ge 0$, so $W = 2^{b_d}$, $m = \lfloor (1 + b_d + b_\ell)/9 \rfloor + 1$ and $L_{\max} = m + 2^{b_\ell} - 1$. Let $T = T[1..n]$ be a byte string.

**Lemma 1 (each token is valid).** Let a token be made at position $i$ by lines L3 to L9.

1. A pair $(d, \ell)$ has $1 \le d \le \min(W, i - 1)$, $m \le \ell \le L_{\max}$, $i + \ell - 1 \le n$, and $T[i - d + k] = T[i + k]$ for $0 \le k < \ell$.
2. Its fields fit: $0 \le d - 1 < 2^{b_d}$ and $0 \le \ell - m < 2^{b_\ell}$.

*Proof.* Line L3 returns a copy that starts at some $j \in [i - W, i - 1]$ with $j \ge 1$, so $d = i - j$ lies in $[1, \min(W, i - 1)]$; the copy is a prefix of $T[i..n]$ of length at most $L_{\max}$ that equals $T[j .. j + \ell - 1]$, which gives the length bound, $i + \ell - 1 \le n$ and the equalities. Line L4 adds $\ell \ge m$. Then $d - 1 \le W - 1 = 2^{b_d} - 1$ and $\ell - m \le L_{\max} - m = 2^{b_\ell} - 1$. $\square$

**Lemma 2 (the encoder ends and covers $T$).** Let $i_1 = 1 < i_2 < \cdots$ be the positions where tokens are made. A pair at $i_s$ covers $T[i_s .. i_s + \ell - 1]$ and a literal covers $T[i_s]$, and $i_{s+1}$ is the next position. The loop ends with $i = n + 1$.

*Proof.* Lines L6 and L9 add $\ell \ge m \ge 1$ or 1 to $i$, and by Lemma 1 a pair does not pass $n$. So $i$ strictly increases, never passes $n + 1$, and the loop of line L2 ends at $i = n + 1$. $\square$

**Lemma 3 (the bits can be read back).** Let $B$ be the concatenation of the token codes followed by $p$ padding bits, all 0, with $0 \le p \le 7$. The decoder reads exactly the code of each token in turn, and then stops without making a token from the padding.

*Proof.* A literal code is the bit 0 and 8 bits; a pair code is the bit 1, $b_d$ bits and $b_\ell$ bits. Assume that the decoder has read the codes of the first $s$ tokens exactly. If a token is left, line L11 sees its whole code: line L12 reads its flag, the flag fixes how many bits follow, and all of them are there. By induction the decoder reads each token code exactly. After the last token only the padding remains. If $p = 0$ the loop of line L11 stops. Otherwise line L12 reads a 0 bit, which asks for a literal of 8 more bits, but at most $p - 1 \le 6$ bits remain; so no whole token remains and the decoder stops. $\square$

A pair can have fewer than 9 bits when $m = 1$ (for example $b_d = 4$ and $b_\ell = 3$ give 8 bits), so a test such as "at least 9 bits remain" in line L11 would lose a short pair at the very end; the test must be that a whole token remains.

**Lemma 4 (the decoder).** Let $S_s$ be $S$ after the decoder has processed $s$ tokens. Then $S_s = T[1 .. i_{s+1} - 1]$.

*Proof.* By induction on $s$; $S_0$ is empty and $i_1 = 1$. Let token $s$ be made at $i = i_s$, and assume $S_{s-1} = T[1 .. i - 1]$. A literal appends $T[i]$. For a pair $(d, \ell)$, the $k$-th round of line L13 ($1 \le k \le \ell$) starts with $|S| = i + k - 2$ and appends $S[|S| - d + 1] = S[i + k - 1 - d]$. Since $d \ge 1$ the index is at most $|S|$, and since $d \le i - 1$ it is at least $k \ge 1$, so the symbol is already written; by the inner induction it is $T[i + k - 1 - d]$, and Lemma 1 with $k - 1$ in place of $k$ says this equals $T[i + k - 1]$. After $\ell$ rounds $S = T[1 .. i + \ell - 1] = T[1 .. i_{s+1} - 1]$. $\square$

**Theorem.** LZSS-DECODE(LZSS-ENCODE$(T)$) $= T$, and the encoded string has at most $9n + 7$ bits.

*Proof.* By Lemma 3 the decoder reads exactly the tokens of the encoder, and by Lemmas 4 and 2 it returns $T[1 .. n]$. For the size: a literal covers 1 symbol with 9 bits. A pair covers $\ell \ge m$ symbols with $1 + b_d + b_\ell$ bits, and the choice of $m$ gives $1 + b_d + b_\ell < 9m \le 9\ell$. So each token uses at most 9 bits per symbol it covers, the tokens use at most $9n$ bits, and the padding adds at most 7. $\square$
