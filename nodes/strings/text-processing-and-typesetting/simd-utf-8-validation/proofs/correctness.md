---
title: The lookup validator accepts exactly the well-formed UTF-8 strings
proves: [correctness, termination]
status: full
---

**Claim.** For every byte string $B$ of length $n$, VALIDATE$(B)$ (lines L1 to L10) stops after $\lceil n / 16 \rceil$ passes of its loop, and it returns true if and only if $B$ is well-formed UTF-8 in the sense of D92 and Table 3-7 of the core specification.

**Setup.** Let $Z$ be the infinite byte sequence with $Z[j] = B[j]$ for $0 \le j < n$ and $Z[j] = 0$ for all other $j$, also the negative ones. A *continuation* byte is one in 80..BF and a *lead* byte one in C0..FF. For a position $j \ge 0$, define

- $sc(j)$ = the AND of the three lookups of line L12 for the previous byte $a = Z[j-1]$ and the current byte $x = Z[j]$,
- $m(j)$ = 80 if $Z[j-2] \ge \mathtt{E0}$ or $Z[j-3] \ge \mathtt{F0}$, and 0 otherwise,
- $e(j) = sc(j) \oplus m(j)$.

**Lemma 1 (the tables).** The bits of $sc(j)$ have these meanings. The test `test_meaning_of_each_error_bit` checks all 65,536 pairs $(a, x)$.

| bit | set exactly when |
|---|---|
| 01 TOO_SHORT | $a$ is a lead and $x$ is not a continuation |
| 02 TOO_LONG | $a < \mathtt{80}$ and $x$ is a continuation |
| 80 TWO_CONTS | $a$ and $x$ are both continuations |
| 20 OVERLONG_2 | $a$ is C0 or C1 and $x$ is a continuation |
| 04 OVERLONG_3 | $a = \mathtt{E0}$ and $x$ is in 80..9F |
| 10 SURROGATE | $a = \mathtt{ED}$ and $x$ is in A0..BF |
| 08 TOO_LARGE | $a \ge \mathtt{F4}$ and $x$ is in 90..BF |
| 40 | $a = \mathtt{F0}$ or $a \ge \mathtt{F5}$, and $x$ is in 80..8F |

*Proof.* A bit of the AND is set exactly when it is set in all three entries. Each entry depends on one nibble, so each condition is a product of a set of high nibbles of $a$, a set of low nibbles of $a$ and a set of high nibbles of $x$, and the table rows give these sets. For example, bit 04 is in BYTE_1_HIGH only at nibble E, in BYTE_1_LOW only at nibble 0, and in BYTE_2_HIGH at nibbles 8 and 9. Bit 40 is in BYTE_1_HIGH only at F, in BYTE_1_LOW at 0 and at 5 to F, and in BYTE_2_HIGH only at 8. The other rows follow in the same way. $\square$

**Lemma 2 (the 3 and 4 byte check).** Line L14 computes $m(j)$. For a byte $y$, the saturating difference $y \ominus \mathtt{60}$ is at least 80 exactly when $y \ge \mathtt{E0}$, and it is at most 9F, so bit 7 of it is set exactly when $y \ge \mathtt{E0}$. In the same way, bit 7 of $y \ominus \mathtt{70}$ is set exactly when $y \ge \mathtt{F0}$. The OR and the AND with 80 keep only bit 7. $\square$

**Lemma 3 (coverage).** VALIDATE$(B)$ returns false exactly when $e(j) \ne 0$ for some $j \ge 0$.

*Proof.* Split $Z[0 \ldots]$ into vectors of 16 bytes. The loop of line L2 visits the vectors that hold bytes of $B$, padded with zero bytes, and line L8 keeps the previous vector in $prev$, which starts as zeros, the bytes of $Z$ before position 0. For a vector $x$ that is not all ASCII, line L13 builds the bytes 1, 2 and 3 places back from $x$ and $prev$, so by Lemmas 1 and 2, line L6 ORs $e(j)$ into the error for each lane $j$ of $x$.

Now let $x$ be an all-ASCII vector, either one of the input or one of the zero vectors after the input. Inside it, $sc(j)$ and $m(j)$ can be nonzero only in lanes 0 to 2, because every other lane has an ASCII byte and three ASCII bytes before it. In lanes 0 to 2, $x[j]$ is not a continuation, so only TOO_SHORT and $m(j)$ can be set. Lane 0 gets an error if $prev[15] \ge \mathtt{C0}$, $prev[14] \ge \mathtt{E0}$ or $prev[13] \ge \mathtt{F0}$, lane 1 if $prev[15] \ge \mathtt{E0}$ or $prev[14] \ge \mathtt{F0}$, and lane 2 if $prev[15] \ge \mathtt{F0}$. Together, the vector has a lane with $e(j) \ne 0$ exactly when $prev$ fails the bounds C0, E0 and F0 on its last three bytes, which is when IS-INCOMPLETE$(prev)$ is nonzero. Line L7 computes this value for every vector that is not all ASCII, and line L4 or line L9 ORs it in when an all-ASCII vector follows, or when the input ends and the zero vectors follow. If $prev$ is itself all ASCII, its own value is zero, and the stored value comes from an earlier vector and was already ORed in when $prev$ was visited. All zero vectors after the first one have $e(j) = 0$ in every lane. $\square$

**Lemma 4.** $B$ is well-formed exactly when $e(j) = 0$ for every $j \ge 0$.

*Proof that well-formed implies no error.* $Z[0 \ldots]$ is then a concatenation of Table 3-7 sequences, and the bytes before position 0 are zeros, which also end a sequence. Take a position $j$ and the sequence that holds $Z[j]$.

- $Z[j]$ starts its sequence. Then $Z[j-1]$ ends a sequence, so it is not a lead and TOO_SHORT is clear, and the other bits need $x$ to be a continuation. So $sc(j) = 0$. If $Z[j-2] \ge \mathtt{E0}$ or $Z[j-3] \ge \mathtt{F0}$, that byte would start a sequence long enough to contain $Z[j]$, which is not the case. So $m(j) = 0$.
- $Z[j]$ is the second byte. Then $a = Z[j-1]$ is a lead of Table 3-7 and $x$ is in the range of its row. TOO_SHORT, TOO_LONG and TWO_CONTS are clear, $a$ is not C0, C1 or F5..FF, and the row ranges exclude the four cases of OVERLONG_3, SURROGATE, TOO_LARGE and bit 40. So $sc(j) = 0$. The bytes $Z[j-2]$ and $Z[j-3]$ belong to earlier sequences, so a value at least E0 or F0 there would start a sequence that contains $Z[j-1]$, but $Z[j-1]$ is a lead. So $m(j) = 0$.
- $Z[j]$ is the third byte. Then $a$ is a continuation, so $sc(j) = $ TWO_CONTS $= \mathtt{80}$, and $Z[j-2] \ge \mathtt{E0}$ is the lead, so $m(j) = \mathtt{80}$ and $e(j) = 0$.
- $Z[j]$ is the fourth byte. Again $sc(j) = \mathtt{80}$, and $Z[j-3] \ge \mathtt{F0}$ is the lead, so $e(j) = 0$.

*Proof that ill-formed implies an error.* Run the scan of a UTF-8 decoder on $Z[0 \ldots]$ and let $i$ be the start of the first sequence that does not match Table 3-7. Everything before $i$ consists of complete sequences, so $Z[i-1] < \mathtt{C0}$, $Z[i-2] < \mathtt{E0}$ and $Z[i-3] < \mathtt{F0}$. Bits 01 to 40 of $sc$ cannot be cancelled by $m$, which has only bit 80.

1. $Z[i]$ is a continuation. If $Z[i-1] < \mathtt{80}$, TOO_LONG is set in $sc(i)$. Otherwise $Z[i-1]$ is a continuation, TWO_CONTS is set, and $m(i) = 0$ by the bounds above, so $e(i) \ne 0$.
2. $Z[i]$ is C0, C1 or in F5..FF, which start no row. At $j = i + 1$, TOO_SHORT is set if $Z[i+1]$ is not a continuation. If it is one, OVERLONG_2 is set for C0 and C1, and TOO_LARGE or bit 40 for F5..FF.
3. $Z[i]$ is a lead of a row with $k$ continuation bytes, and byte $i + t$ with $1 \le t \le k$ is the first one out of range. Bytes after the end of $B$ are zeros, so this covers a truncated end too. If $t = 1$ and $Z[i+1]$ is not a continuation, TOO_SHORT is set at $i + 1$. If $t = 1$ and it is a continuation outside the row's second byte range, then by Table 3-7 the pair is E0 with 80..9F, ED with A0..BF, F0 with 80..8F, or F4 with 90..BF, and OVERLONG_3, SURROGATE, bit 40 or TOO_LARGE is set. If $t \ge 2$, then $Z[i+t]$ is not a continuation, because the later ranges are all of 80..BF, and its previous byte is a continuation, so $sc(i+t) = 0$. But $Z[i] \ge \mathtt{E0}$ if $t = 2$, and $Z[i] \ge \mathtt{F0}$ if $t = 3$, so $m(i+t) = \mathtt{80}$ and $e(i+t) \ne 0$. $\square$

**Proof of the claim.** Lemmas 3 and 4. Each pass of the loop of line L2 does a fixed number of vector operations and moves 16 bytes forward, so the procedure stops after $\lceil n / 16 \rceil$ passes. $\blacksquare$
