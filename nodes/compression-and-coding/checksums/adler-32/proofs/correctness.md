---
title: The deferred Adler-32 loop computes the sums of RFC 1950, the combine rule holds, and errors in two nearby bytes are always detected
proves: [correctness]
status: full
---

Let $P = 65521$ and let the bytes be $d_1, \ldots, d_n \in [0, 255]$. For a start pair $(u, w)$ with $0 \le u, w < P$, define $s_1^{(0)} = u$, $s_2^{(0)} = w$, and for $t \ge 1$, $s_1^{(t)} = (s_1^{(t-1)} + d_t) \bmod P$ and $s_2^{(t)} = (s_2^{(t-1)} + s_1^{(t)}) \bmod P$. Adler-32 is $(s_1^{(n)}, s_2^{(n)})$ for $(u, w) = (1, 0)$, packed as $s_2 \cdot 2^{16} + s_1$.

**Lemma 1 (closed form).** $s_1^{(n)} \equiv u + \sum_{i=1}^{n} d_i$ and $s_2^{(n)} \equiv w + n u + \sum_{i=1}^{n} (n - i + 1) d_i \pmod P$.

*Proof.* The first claim is immediate. For the second, $s_2^{(n)} \equiv w + \sum_{t=1}^{n} (u + \sum_{i \le t} d_i) = w + nu + \sum_{i=1}^{n} d_i \cdot (n - i + 1)$, since $d_i$ appears in the inner sum for $t = i, \ldots, n$. $\square$

**Lemma 2 (no overflow).** If a block starts with $s_1, s_2 \le P - 1$, then after $k$ runs of lines L6 and L7 we have $s_1 \le (P - 1) + 255k$ and $s_2 \le (k + 1)(P - 1) + 255 k(k + 1)/2$. For $k \le 5552$ this is at most $2^{32} - 1$.

*Proof.* After $t$ bytes, $s_1 \le (P - 1) + 255t$. Line L7 adds this value for $t = 1, \ldots, k$ to an $s_2 \le P - 1$, which gives the bound. For $k = 5552$ the bound is $5553 \cdot 65520 + 255 \cdot 5552 \cdot 5553 / 2 = 4{,}294{,}690{,}200 \le 4{,}294{,}967{,}295$. $\square$

**Theorem 1 (correctness).** ADLER32 with the running value $v = w \cdot 2^{16} + u$ returns $s_2^{(n)} \cdot 2^{16} + s_1^{(n)}$.

*Proof.* Lines L1 and L2 set $s_1 = u$ and $s_2 = w$. We show the invariant: after $p$ runs of lines L6 and L7, the integers $s_1, s_2$ are congruent to $s_1^{(p)}, s_2^{(p)}$ modulo $P$. It holds for $p = 0$. Line L6 adds $d_{p+1}$ to $s_1$, so $s_1 \equiv s_1^{(p+1)}$. Line L7 adds that $s_1$ to $s_2$, so $s_2 \equiv s_2^{(p)} + s_1^{(p+1)} \equiv s_2^{(p+1)}$. Lines L8 and L9 replace both by their residues, which keeps the invariant and restores the start condition of Lemma 2, so by Lemma 2 the integer arithmetic never overflows. When the loop of line L3 ends, $p = n$ and both values are residues in $[0, P - 1]$, so they equal $s_1^{(n)}$ and $s_2^{(n)}$. Line L10 packs them. $\square$

**Theorem 2 (combine).** Let $A$ and $B$ be byte strings, $\ell = |B|$, and let $(a_1, a_2)$, $(b_1, b_2)$ be the Adler-32 pairs of $A$ and $B$. Then the pair of $AB$ is $((a_1 + b_1 - 1) \bmod P, (a_2 + b_2 + \ell(a_1 - 1)) \bmod P)$.

*Proof.* By Theorem 1 the run over $AB$ equals the run over $B$ started from $(u, w) = (a_1, a_2)$. Lemma 1 with $B = e_1, \ldots, e_\ell$ gives $s_1 \equiv a_1 + \sum e_i$ and $s_2 \equiv a_2 + \ell a_1 + \sum (\ell - i + 1) e_i$. Lemma 1 for $B$ alone, from $(1, 0)$, gives $b_1 \equiv 1 + \sum e_i$ and $b_2 \equiv \ell + \sum (\ell - i + 1) e_i$. Substituting, $s_1 \equiv a_1 + b_1 - 1$ and $s_2 \equiv a_2 + \ell a_1 + b_2 - \ell = a_2 + b_2 + \ell(a_1 - 1)$. $\square$

**Theorem 3 (errors in at most two bytes).** Let an error change the bytes at positions $i \le j$ by $\delta_i, \delta_j \in [-255, 255]$, not both 0, with $j - i < P$, and keep the length. Then the Adler-32 value changes.

*Proof.* By Lemma 1, the error is missed if and only if $\delta_i + \delta_j \equiv 0$ and $(n - i + 1)\delta_i + (n - j + 1)\delta_j \equiv 0 \pmod P$ (for $i = j$, read $\delta_j = 0$). Subtracting $(n - j + 1)$ times the first condition from the second gives $(j - i)\delta_i \equiv 0$. If $i = j$, the first condition says $\delta_i \equiv 0$. Otherwise $0 < j - i < P$, and since $P$ is prime, $j - i$ is invertible modulo $P$, so again $\delta_i \equiv 0$. Since $|\delta_i| \le 255 < P$, $\delta_i = 0$, and then the first condition gives $\delta_j = 0$, a contradiction. $\square$

**Corollary 1 (swaps).** Swapping two different bytes less than $P$ positions apart is detected. In particular the change 0x00 to 0xFF of one byte, which Fletcher-16 misses, is detected.

*Proof.* Both are errors in at most two bytes, with $\delta \ne 0$. $\square$

**Lemma 3 (short messages).** If $n \le 128$, then $s_1 \le 32641 < 2^{15}$, and over all $65536$ messages of length 2, $s_1$ takes exactly 511 values.

*Proof.* $s_1 = 1 + \sum d_i \le 1 + 255n$, with no reduction since this is below $P$. For $n = 2$, $s_1 = 1 + d_1 + d_2$ takes every value in $[1, 511]$ and no other. $\square$

**Cost.** Lines L6 and L7 run once per byte, and lines L8 and L9 once per 5552 bytes, so the time is $\Theta(n)$ with $O(1)$ extra space. Combine uses a fixed number of operations. $\blacksquare$
